"""StudentBridge AI - competition sandbox app (no real-money transfer)."""
from __future__ import annotations
import base64, hashlib, hmac, json, os, re, secrets, uuid, time
from datetime import datetime, timezone, date
from pathlib import Path
from urllib.parse import urlparse
from typing import Any
from contextlib import asynccontextmanager
from . import database

from io import BytesIO
from pypdf import PdfReader
import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator, model_validator
from starlette.templating import Jinja2Templates
from .logic import evaluate, simulate
from .journey import planning_preview, prepare_steps, calendar_bytes
from .assistant import make_answer
from . import secure_card

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
CATALOG=json.loads((BASE/'data'/'catalog.json').read_text())
SOURCES=json.loads((BASE/'data'/'sources.json').read_text())
COUNTRY={i['name']:i for i in CATALOG['countries']}
SOURCE_MAP={s['id']:s for s in SOURCES}
SECRET=os.getenv('APP_SECRET','local-sandbox-only-change-before-deploy').encode()
if os.getenv('APP_ENV')=='production' and (len(SECRET)<32 or SECRET==b'local-sandbox-only-change-before-deploy'):
    raise RuntimeError('Production requires a unique, strong APP_SECRET of at least 32 characters.')
@asynccontextmanager
async def lifespan(app:FastAPI):
    database.initialize()
    if database.research_counts()['countries'] == 0:
        database.import_research_csv(ROOT/'data/research/corrected')
    yield

app=FastAPI(title='StudentBridge AI | Cross-border Finance Agent',version='9.0.0',description='MySQL-powered six-country finance planning and sandbox execution',lifespan=lifespan)
app.mount('/static',StaticFiles(directory=BASE/'static'),name='static')
templates=Jinja2Templates(directory=str(BASE/'templates'))

def stamp(): return datetime.now(timezone.utc).isoformat()

def sign_fx(base:str, quote:str, rate:float, observation:str|None)->str:
    fact={'base':base,'quote':quote,'rate':rate,'date':observation,'issued':int(time.time())}
    raw=base64.urlsafe_b64encode(json.dumps(fact,sort_keys=True,separators=(',',':')).encode()).decode().rstrip('=')
    signature=hmac.new(SECRET,raw.encode(),hashlib.sha256).hexdigest()
    return raw+'.'+signature

def verify_fx(proof:str|None,base:str,quote:str,rate:float,observation:str|None)->bool:
    if not proof:return False
    try:
        raw,sig=proof.rsplit('.',1)
        expected=hmac.new(SECRET,raw.encode(),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig,expected):return False
        item=json.loads(base64.urlsafe_b64decode(raw+'='*((-len(raw))%4)))
        return (item['base']==base and item['quote']==quote and item['rate']==rate and
                item.get('date')==observation and 0<=time.time()-item['issued']<=3600)
    except (ValueError,KeyError,TypeError,OverflowError):return False
def digest(value:Any)->str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def audit(event_type:str,object_id:str,details:dict):
    database.audit(event_type,object_id,details,SECRET)

def get_plan(id:str)->dict:
    item=database.load_plan(id)
    if item is None:raise HTTPException(404,'Plan not found')
    return item

def valid_url(url:str|None)->bool:
    if not url:return True
    p=urlparse(url)
    return p.scheme=='https' and bool(p.netloc)

class Quote(BaseModel):
    id:str|None=None
    provider:str=Field(min_length=2,max_length=100)
    rate:float=Field(gt=0,le=1e8)
    fixed_fee:float=Field(default=0,ge=0,le=1e9)
    fee_percent:float=Field(default=0,ge=0,le=100)
    eta_days:int=Field(default=3,ge=0,le=365)
    eligible:bool=False
    source_url:str|None=None
    expires_on:str|None=None
    @field_validator('source_url')
    @classmethod
    def check_url(cls,v):
        if not valid_url(v):raise ValueError('Source URL must be HTTPS')
        return v

class PlanRequest(BaseModel):
    origin:str
    destination:str
    origin_currency:str
    destination_currency:str
    university:str=Field(default='',max_length=160)
    tuition_amount:float=Field(ge=0,le=2e9)
    scholarship_amount:float=Field(default=0,ge=0,le=2e9)
    available_balance:float=Field(ge=0,le=2e12)
    emergency_reserve:float=Field(default=0,ge=0,le=2e12)
    monthly_living_cost:float=Field(default=0,ge=0,le=1e9)
    living_months:int=Field(default=6,ge=0,le=60)
    protect_living_costs:bool=False
    deadline:str
    reference_rate:float|None=Field(default=None,gt=0,le=1e8)
    reference_date:str|None=None
    reference_source:str|None=None
    reference_proof:str|None=None
    quotes:list[Quote]=Field(default_factory=list,max_length=8)
    @model_validator(mode='after')
    def check_country_currency(self):
        if self.origin not in COUNTRY or self.destination not in COUNTRY or self.origin==self.destination:
            raise ValueError('Origin and destination must be two different supported countries.')
        if COUNTRY[self.origin]['currency']!=self.origin_currency or COUNTRY[self.destination]['currency']!=self.destination_currency:
            raise ValueError('Currency must match the selected country.')
        from datetime import date
        try: date.fromisoformat(self.deadline)
        except ValueError: raise ValueError('Deadline must use YYYY-MM-DD.')
        return self

class DemoPaymentRequest(BaseModel):
    origin:str
    destination:str
    tuition_amount:float=Field(gt=0,le=2e9)
    available_balance:float=Field(gt=0,le=2e12)
    emergency_reserve:float=Field(default=0,ge=0,le=2e12)
    deadline:str
    rate:float=Field(gt=0,le=1e8)
    reference_date:str|None=None
    reference_proof:str|None=None
    university:str=Field(default='Sample university',max_length=160)
    @model_validator(mode='after')
    def check_corridor(self):
        from datetime import date
        if self.origin not in COUNTRY or self.destination not in COUNTRY or self.origin==self.destination:
            raise ValueError('Choose two different supported countries.')
        try: date.fromisoformat(self.deadline)
        except ValueError: raise ValueError('Choose a valid payment deadline.')
        if self.emergency_reserve>self.available_balance:
            raise ValueError('Emergency savings cannot exceed your available money.')
        return self

class ScenarioRequest(BaseModel):
    plan_id:str
    fx_change_percent:float=Field(ge=-80,le=200)
    extra_fee:float=Field(default=0,ge=0,le=1e9)
    living_cost_change_percent:float=Field(default=0,ge=-80,le=200)

class PaymentRequest(BaseModel):
    plan_id:str
    quote_id:str
    confirmed:bool
    approval_phrase:str
    idempotency_key:str=Field(min_length=8,max_length=120)

class JourneyRequest(BaseModel):
    goal:str=Field(default='Plan tuition and living costs',max_length=250)
    origin:str
    destination:str
    tuition_amount:float=Field(ge=0,le=2e9)
    scholarship_amount:float=Field(default=0,ge=0,le=2e9)
    available_balance:float=Field(ge=0,le=2e12)
    emergency_reserve:float=Field(default=0,ge=0,le=2e12)
    monthly_living_cost:float=Field(default=0,ge=0,le=1e9)
    living_months:int=Field(default=3,ge=0,le=60)
    deadline:date
    invoice_verified:bool=False
    quote_verified:bool=False
    @model_validator(mode='after')
    def validate_journey(self):
        if self.origin not in COUNTRY or self.destination not in COUNTRY or self.origin == self.destination:
            raise ValueError('Select two different supported countries.')
        if self.scholarship_amount > self.tuition_amount:
            raise ValueError('Scholarship cannot exceed tuition.')
        if self.emergency_reserve > self.available_balance:
            raise ValueError('Emergency savings cannot exceed available money.')
        return self

class ChatRequest(BaseModel):
    message:str=Field(min_length=1,max_length=1000)
    plan_id:str|None=None
    country:str|None=None

@app.get('/',response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(request,'index.html',{})


# Card information and billing address are entered only on the provider's
# hosted payment page, never in a StudentBridge form or database.
@app.get('/api/card/availability')
def card_availability():
    return secure_card.public_status()

@app.post('/api/card/checkout')
def card_checkout():
    try:
        import stripe
        result=secure_card.checkout(stripe)
        audit('CARD_CHECKOUT_CREATED',result['session_id'],{'mode':result['mode']})
        return result
    except ImportError:
        raise HTTPException(503,'Payment provider library is not installed.')
    except ValueError as exc:
        raise HTTPException(503,str(exc))
    except Exception:
        raise HTTPException(502,'Unable to create a secure payment session. Try again later.')

@app.get('/api/card/session/{session_id}')
def card_session(session_id:str):
    try:
        import stripe
        return secure_card.session_status(stripe,session_id)
    except ValueError as exc:
        raise HTTPException(400,str(exc))
    except Exception:
        raise HTTPException(502,'Unable to verify payment status with the provider.')

@app.post('/api/card/webhook')
async def card_webhook(request:Request):
    key=os.getenv('STRIPE_WEBHOOK_SECRET','')
    if not key.startswith('whsec_'):
        raise HTTPException(503,'Payment webhooks are not configured.')
    payload=await request.body()
    if len(payload)>128000:raise HTTPException(413,'Webhook too large')
    try:
        import stripe
        event=stripe.Webhook.construct_event(payload,request.headers.get('stripe-signature',''),key)
    except Exception:
        raise HTTPException(400,'Invalid payment webhook signature')
    if event['type'] in ('checkout.session.completed','checkout.session.async_payment_succeeded'):
        obj=event['data']['object']
        config=secure_card.details()
        if (obj.get('payment_status')=='paid' and
            obj.get('client_reference_id')==config['invoice_reference'] and
            (obj.get('metadata') or {}).get('authorized_payee')==config['payee']):
            # Minimal provider references only, no PAN, CVC, or billing addresses.
            database.record_gateway_event(event['id'],obj['id'],event['type'],
                'PAID_LIVE' if obj.get('livemode') else 'PAID_TEST',SECRET)
    return {'received':True}

@app.get('/api/health')
def health():
    try: dialect=database.check_health()
    except Exception:raise HTTPException(503,'Database unavailable; check MySQL connection settings.')
    return {'status':'ok','version':'9.0.0','mode':'SANDBOX_NO_REAL_MONEY',
            'database':True,'database_engine':dialect}


@app.get('/api/catalog')
def catalog():return {**CATALOG,'sources':SOURCES,'country_pair_count':30,'sandbox':True}

@app.get('/api/research/summary')
def research_summary():
    return json.loads((BASE/'data'/'research_summary.json').read_text())

@app.get('/api/research/benchmarks')
def research_benchmarks(country:str|None=None):
    if country and country not in COUNTRY:raise HTTPException(422,'Unsupported country')
    country_code=COUNTRY[country]['code'] if country else None
    items=database.research_financial_benchmarks(country_code)
    return {'data':items,'count':len(items),
            'warning':'Visa financial requirements and historical survey estimates are not actual current living bills.'}


@app.get('/api/fx')
async def fx(base:str='GBP',quote:str='AUD'):
    supported={c['currency'] for c in CATALOG['countries']}
    if base not in supported or quote not in supported or base==quote:raise HTTPException(422,'Choose different supported currencies.')
    endpoint=f'https://api.frankfurter.dev/v2/rate/{base}/{quote}'
    try:
        async with httpx.AsyncClient(timeout=8,follow_redirects=False) as client:
            res=await client.get(endpoint)
            res.raise_for_status(); data=res.json()
        if not isinstance(data,dict) or not isinstance(data.get('rate'),(float,int)) or data['rate']<=0:
            raise ValueError('Unexpected provider response')
        return {'available':True,'base':base,'quote':quote,'rate':data['rate'],'date':data.get('date'),
                'source':'Frankfurter reference FX API','source_url':endpoint,'classification':'LIVE_REFERENCE_NOT_PROVIDER_QUOTE',
                'proof':sign_fx(base,quote,data['rate'],data.get('date')),
                'warning':'Reference rate, not a bank transfer quote. Fees and spreads are excluded.'}
    except (httpx.HTTPError,ValueError,KeyError) as exc:
        return {'available':False,'base':base,'quote':quote,'rate':None,'source_url':endpoint,
                'classification':'UNAVAILABLE','warning':'The reference FX service could not be reached. Enter an actual documented quote or try again later.'}

@app.post('/api/plans')
def make_plan(request:PlanRequest):
    raw=request.model_dump()
    ref=None
    if request.reference_rate is not None:
        authentic=verify_fx(request.reference_proof,request.destination_currency,request.origin_currency,
                             request.reference_rate,request.reference_date)
        ref={'rate':request.reference_rate,'date':request.reference_date,
             'classification':'FRANKFURTER_LIVE_SERVER_VERIFIED' if authentic else 'USER_ENTERED_UNVERIFIED',
             'pair':f'{request.destination_currency}/{request.origin_currency}',
             'warning':'Reference conversion only. It is not an executable quote.'}
    try: result=evaluate(raw,ref)
    except ValueError as exc:raise HTTPException(422,str(exc))
    id='SB-'+uuid.uuid4().hex[:12].upper()
    plan_digest=digest(result)
    result['plan_id']=id; result['decision_hash']=plan_digest
    result['data_integrity_note']='SHA256 of deterministic plan result excluding the identifier and hash.'
    database.save_plan(id,raw,result,result['decision_hash'],SECRET)
    return result

@app.post('/api/demo/prepare')
def demo_prepare(request:DemoPaymentRequest):
    """Build a real, audit-logged sandbox workflow with openly fictional providers/fees.

    The conversion can use a fresh signed Frankfurter reference rate, or an
    explicitly user-entered *demo* value. Neither constitutes a bank quote.
    """
    orig=COUNTRY[request.origin]['currency']; dest=COUNTRY[request.destination]['currency']
    authenticated=verify_fx(request.reference_proof,dest,orig,request.rate,request.reference_date)
    method_specs=[
        ('demo-bank','Sample Bank Transfer',1.0,2),
        ('demo-card','Sample Card Payment',1.8,0),
        ('demo-student','Sample Student Transfer',0.6,4),
    ]
    quotes=[{'id':i,'provider':name,'rate':request.rate,'fixed_fee':0,
             'fee_percent':fee,'eta_days':eta,'eligible':True,'simulation_only':True,
             'source_url':None} for i,name,fee,eta in method_specs]
    payload={'origin':request.origin,'destination':request.destination,
             'origin_currency':orig,'destination_currency':dest,'university':request.university,
             'tuition_amount':request.tuition_amount,'scholarship_amount':0,
             'available_balance':request.available_balance,'emergency_reserve':request.emergency_reserve,
             'monthly_living_cost':0,'living_months':0,'deadline':request.deadline,
             'quotes':quotes}
    provenance='FRANKFURTER_LIVE_SERVER_VERIFIED' if authenticated else 'USER_ENTERED_DEMO_RATE'
    reference={'rate':request.rate,'date':request.reference_date,'classification':provenance,
               'pair':f'{dest}/{orig}', 'warning':'Reference or sample rate ONLY. Not a bank offer.'}
    result=evaluate(payload,reference)
    plan_id='SB-'+uuid.uuid4().hex[:12].upper()
    result['plan_id']=plan_id;result['decision_hash']=digest(result)
    result['demo_only']=True;result['reference_rate_source']=provenance
    result['display_notice']='Illustrative payment methods, fees and delivery times. No real banking connection.'
    database.save_plan(plan_id,payload,result,result['decision_hash'],SECRET)
    return result

@app.get('/api/sandbox/receipt/{transaction_id}')
def get_sandbox_receipt(transaction_id:str):
    row=database.get_transaction(transaction_id)
    if not row:raise HTTPException(404,'Practice receipt not found')
    plan=get_plan(row['plan_id'])
    quote=next((q for q in plan['quotes'] if q['quote_id']==row['quote_id']),None)
    if quote is None:raise HTTPException(409,'Payment option not available in saved plan')
    return {'receipt_type':'SIMULATION_ONLY','transaction_id':row['id'],
        'date':row['created_at'],'status':row['status'],'origin':plan['origin'],
        'destination':plan['destination'],'university':plan['university'],
        'method':quote['provider'],'sending_amount':float(row['approved_amount']),
        'sending_currency':row['currency'],'receiving_amount':plan['required_tuition'],
        'receiving_currency':plan['destination_currency'],'fee_amount':quote['fee_total'],
        'reference_type':quote['provenance'],'plan_id':plan['plan_id'],
        'warning':'TEST RECEIPT. No bank was contacted and no real money moved.'}

@app.get('/api/plans/{plan_id}')
def read_plan(plan_id:str):return get_plan(plan_id)

@app.post('/api/scenarios')
def stress(request:ScenarioRequest):
    plan=get_plan(request.plan_id)
    try:return simulate(plan,request.fx_change_percent,request.extra_fee,request.living_cost_change_percent)
    except ValueError as exc:raise HTTPException(422,str(exc))

@app.get('/api/passport/{plan_id}')
def passport(plan_id:str):
    plan=get_plan(plan_id)
    return {'title':'StudentBridge AI - Explainable Decision Passport','version':'1.0','plan_id':plan_id,
            'integrity_hash':plan['decision_hash'],'date':plan['generated_at'],
            'goal':f"Plan {plan['required_tuition']:,.2f} {plan['destination_currency']} from {plan['origin']} to {plan['destination']} by {plan['deadline']}",
            'recommended_quote_id':plan['recommended_quote_id'],'reasoning':plan['recommendation'],
            'examined_quotes':plan['quotes'],'reference_rate':plan['reference_rate'],
            'source_registry':[s for s in SOURCES if s['category'] in ['exchange_rates','regulation','bank_fees','tuition']],
            'limitations':plan['cautions'],'label':'DECISION SUPPORT ONLY / SANDBOX'}

@app.post('/api/sandbox/execute')
def sandbox_execute(request:PaymentRequest):
    if request.confirmed is not True or request.approval_phrase!='APPROVE SANDBOX':
        audit('SANDBOX_BLOCKED',request.plan_id,{'reason':'Missing explicit user confirmation'})
        raise HTTPException(403,'You must explicitly approve the simulated payment.')
    plan=get_plan(request.plan_id)
    quote=next((q for q in plan['quotes'] if q['quote_id']==request.quote_id),None)
    if quote is None:raise HTTPException(404,'Provider quote not found in plan')
    if not quote['viable']:
        audit('SANDBOX_BLOCKED',request.plan_id,{'reason':'Route did not pass all required planner constraints'})
        raise HTTPException(409,'This option does not pass the entered deadline, funds, or eligibility conditions.')
    transaction_id='TX-TEST-'+uuid.uuid4().hex[:10].upper()
    outcome=database.save_sandbox_payment(plan,quote,request.idempotency_key,transaction_id,SECRET)
    if outcome.get('conflict'):raise HTTPException(409,'This idempotency key belongs to a different request.')
    return outcome

@app.get('/api/sandbox/history')
def sandbox_history():
    if os.getenv('APP_ENV')=='production':
        raise HTTPException(403,'Shared sandbox history is private in the public demo.')
    return {'transactions':database.get_history()}

@app.get('/api/audit')
def audit_log():
    if os.getenv('APP_ENV')=='production':
        raise HTTPException(403,'Audit entries are restricted in the public demo.')
    return {'audit_events':database.get_audit(),
            'integrity':'HMAC-SHA256 chain stored in MySQL; not externally timestamped.'}

@app.get('/api/audit/verify')
def verify_audit():
    if os.getenv('APP_ENV')=='production':
        raise HTTPException(403,'Audit verification is restricted in the public demo.')
    return database.verify_audit_chain(SECRET)

@app.get('/api/credit/{country}')
def credit(country:str):
    data=CATALOG['credit_guidance'].get(country)
    if not data:raise HTTPException(404,'Not a supported country')
    return {**data,'country':country,'source':SOURCE_MAP.get(data['source_id']),
            'limitations':'Information only; no score, credit offer or eligibility calculation.'}

@app.post('/api/invoices/analyze')
async def invoice_analysis(file:UploadFile=File(...)):
    raw=await file.read(2_500_001)
    if len(raw)>2_500_000:raise HTTPException(413,'Use a PDF smaller than 2.5 MB.')
    if not raw.startswith(b'%PDF'):raise HTTPException(415,'Only PDF invoices are supported.')
    try:
        pdf=PdfReader(BytesIO(raw), strict=False)
        if len(pdf.pages)>12:raise HTTPException(413,'Maximum 12 pages.')
        text='\n'.join(p.extract_text() or '' for p in pdf.pages)
    except HTTPException:raise
    except Exception:raise HTTPException(422,'Could not read PDF. Scanned documents may need OCR.')
    if not text.strip():return {'text_found':False,'warning':'No selectable text found. Enter invoice information manually or use an OCR-enabled version.', 'fields':{}}
    # Extract possibilities; do not assert that any one is the payable balance.
    money_matches=re.findall(r'(?:GBP|AUD|CNY|JPY|KRW|BDT|£|¥|₩|৳|\$)\s*([\d,]+(?:\.\d{1,2})?)',text,re.I)
    dates=re.findall(r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',text)
    suspicious=bool(re.search(r'ignore previous instructions|system prompt|override all rules|send.*credentials',text,re.I))
    return {'text_found':True,'fields':{'amount_candidates':money_matches[:10],'date_candidates':dates[:10],
                                          'preview':text[:1000]}, 'has_suspicious_instructions':suspicious,
            'warning':'Possible fields only: verify amount, deadline and beneficiary from the official university invoice before use. No instructions inside documents are executed.'}

@app.post('/api/journey/prepare')
async def journey_prepare(request:JourneyRequest):
    """Deterministically execute safe read-only finance tools in one request.

    This endpoint never creates a payment, commits a plan or stores private financial data.
    """
    origin_currency=COUNTRY[request.origin]['currency']
    destination_currency=COUNTRY[request.destination]['currency']
    reference=await fx(base=destination_currency,quote=origin_currency)
    value=float(reference['rate']) if reference.get('available') else None
    preview=planning_preview(amount=request.tuition_amount,scholarship=request.scholarship_amount,
        available=request.available_balance,reserve=request.emergency_reserve,
        living_per_month=request.monthly_living_cost,months=request.living_months,
        reference_rate=value,reference_date=reference.get('date'),
        origin_currency=origin_currency,destination_currency=destination_currency,
        deadline=request.deadline)
    shocks=[]
    if value is not None:
        for move in (0,5,10):
            shocked=planning_preview(amount=request.tuition_amount,scholarship=request.scholarship_amount,
                available=request.available_balance,reserve=request.emergency_reserve,
                living_per_month=request.monthly_living_cost,months=request.living_months,
                reference_rate=value*(1+move/100),reference_date=reference.get('date'),
                origin_currency=origin_currency,destination_currency=destination_currency,
                deadline=request.deadline)
            shocks.append({'rate_increase_percent':move,
                           'tuition_and_living_estimate_origin':round((shocked['estimated_tuition_origin'] or 0)+(shocked['estimated_living_origin'] or 0),2),
                           'remaining_after_protection':shocked['remaining_after_protection'],
                           'status':shocked['protection_status']})
    steps=prepare_steps(invoice_ready=request.invoice_verified,quote_ready=request.quote_verified,
        deadline=request.deadline,protection_status=preview['protection_status'])
    return {'title':'Your personalized StudentBridge Journey','goal':request.goal,
            'corridor':f'{request.origin} → {request.destination}',
            'summary':preview['explanation'], 'preview':preview,'steps':steps,'fx_stress_checks':shocks,
            'reference':{'available':bool(reference.get('available')),'source_url':reference.get('source_url'),
                         'date':reference.get('date'),'rate':value},
            'tools_used':['country_currency_validation','deadline_guard','reference_fx_lookup',
                          'tuition_budget_shield','fx_stress_scenarios','action_plan_generator'],
            'actions_needing_approval':['bank or card payment','application submission','any transfer of money'],
            'notice':'A prepared plan, not financial advice or a payment instruction. No transaction was made.'}

@app.get('/api/journey/calendar')
def journey_calendar(deadline:date,title:str='University tuition payment',remind_days:int=7):
    if len(title)>120 or not 0<=remind_days<=60:
        raise HTTPException(422,'Invalid calendar reminder settings.')
    raw=calendar_bytes(deadline,title,remind_days)
    return Response(content=raw,media_type='text/calendar',headers={'Content-Disposition':'attachment; filename="tuition-reminder.ics"',
                                                                     'Cache-Control':'no-store'})

@app.post('/api/chat')
async def chat(request:ChatRequest):
    plan=get_plan(request.plan_id) if request.plan_id else None
    result=make_answer(request.message,CATALOG,SOURCES,plan,request.country)
    # Use the same real reference-rate endpoint when the user names a pair.
    # If the provider cannot be reached we say so rather than fabricating data.
    requested_fx=result.pop('fx_pair',None)
    if requested_fx:
        fx_result=await fx(**requested_fx)
        if fx_result.get('available'):
            result['message']=(f"Published reference: 1 {requested_fx['base']} = "
                 f"{fx_result['rate']:,.5f} {requested_fx['quote']} "
                 f"(observation {fx_result.get('date') or 'date not reported'}). "
                 "This is NOT a provider quote and excludes charges. Use a real bank quote before making a payment.")
            result['tools_used'].append('frankfurter_live_reference_rate')
            result['sources'].append({'title':'Frankfurter published reference exchange rate','url':fx_result['source_url']})
        else:
            result['message']=(f"I could not load the current {requested_fx['base']} to "
                f"{requested_fx['quote']} reference rate. I will not guess it. "
                "You can retry in the Payment Planner or check the dated reference sources.")
            result['tools_used'].append('live_reference_unavailable')
    # Optional LLM: strictly a stylistic rewrite of the verified tool output.
    # Deterministic results and source links remain authoritative.
    key=os.getenv('GEMINI_API_KEY','').strip()
    if key and 'frankfurter_live_reference_rate' not in result['tools_used']:
        prompt=("You explain finance in simple English. Rewrite the following TOOL RESULT only. "
                "Keep ALL numbers, qualifiers, country names, uncertainty and warnings exactly as given. "
                "Do not add facts, links, providers, guarantees or recommendations. "
                "Return at most 150 words, plain text.\n"
                f"QUESTION: {request.message}\nTOOL RESULT: {result['message']}")
        try:
            model=os.getenv('GEMINI_MODEL','gemini-2.5-flash')
            async with httpx.AsyncClient(timeout=8) as client:
                res=await client.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                                     headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'text':prompt}]}]})
            if res.status_code==200:
                # Keep the deterministic finance answer unchanged for traceability.
                # AI phrasing is supplementary, not a replacement for checked values.
                result['ai_explanation']=res.json()['candidates'][0]['content']['parts'][0]['text'][:1000]
                result['tools_used'].append('gemini_optional_explanation')
        except (httpx.HTTPError,KeyError,IndexError,TypeError,ValueError):
            pass
    return result
