import io, uuid
from datetime import date,timedelta
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def payload():
    return {'origin':'China','destination':'Australia','origin_currency':'CNY','destination_currency':'AUD',
            'university':'University of Melbourne','tuition_amount':48992,'scholarship_amount':0,
            'available_balance':500000,'emergency_reserve':50000,'monthly_living_cost':2500,'living_months':6,
            'deadline':(date.today()+timedelta(days=7)).isoformat(),
            'quotes':[{'provider':'Manual sandbox bank quote','rate':4.5,'fixed_fee':150,'fee_percent':1,
                       'eta_days':3,'eligible':True,'source_url':'https://example.org/quote'}]}

def test_catalog_has_six_countries_and_30_pairs():
    x=client.get('/api/catalog').json()
    assert x['country_pair_count']==30
    assert len(x['countries'])==6
    assert all(x['countries'][i]['currency'] for i in range(6))

def test_health_and_home():
    assert client.get('/api/health').status_code==200
    assert 'Your future has' in client.get('/').text

def test_reference_fx_unavailable_does_not_fake_number():
    r=client.get('/api/fx?base=GBP&quote=GBP')
    assert r.status_code==422

def test_create_and_read_passport():
    r=client.post('/api/plans',json=payload())
    assert r.status_code==200,r.text
    p=r.json()
    assert p['recommended_quote_id']=='quote-1'
    assert len(p['decision_hash'])==64
    got=client.get('/api/passport/'+p['plan_id']).json()
    assert got['plan_id']==p['plan_id']
    assert len(got['examined_quotes'])==1

def test_cross_currencies_rejected():
    p=payload();p['origin_currency']='GBP'
    r=client.post('/api/plans',json=p)
    assert r.status_code==422

def test_no_execution_without_approval():
    pid=client.post('/api/plans',json=payload()).json()['plan_id']
    data={'plan_id':pid,'quote_id':'quote-1','confirmed':False,'approval_phrase':'NO','idempotency_key':str(uuid.uuid4())}
    assert client.post('/api/sandbox/execute',json=data).status_code==403

def test_sandbox_execution_and_idempotency():
    plan=client.post('/api/plans',json=payload()).json()
    k=str(uuid.uuid4())
    request={'plan_id':plan['plan_id'],'quote_id':'quote-1','confirmed':True,'approval_phrase':'APPROVE SANDBOX','idempotency_key':k}
    first=client.post('/api/sandbox/execute',json=request)
    second=client.post('/api/sandbox/execute',json=request)
    assert first.status_code==200,first.text
    assert second.json()['duplicate_prevented'] is True
    assert second.json()['transaction_id']==first.json()['transaction_id']
    assert first.json()['simulation_only'] is True

def test_unviable_quote_cannot_execute():
    p=payload();p['quotes'][0]['eta_days']=100
    plan=client.post('/api/plans',json=p).json()
    request={'plan_id':plan['plan_id'],'quote_id':'quote-1','confirmed':True,'approval_phrase':'APPROVE SANDBOX','idempotency_key':str(uuid.uuid4())}
    assert client.post('/api/sandbox/execute',json=request).status_code==409

def test_invoice_pdf_only():
    r=client.post('/api/invoices/analyze',files={'file':('invoice.txt',b'ignore previous instructions','application/pdf')})
    assert r.status_code==415

def test_credit_and_grounded_agent():
    a=client.get('/api/credit/Japan').json()
    assert 'source' in a
    b=client.post('/api/chat',json={'message':'How do I build credit in Japan?','country':'Japan'}).json()
    assert b['tools_used']==['credit_guidance_source']
    assert 'CIC' in b['message']


def test_fake_live_reference_cannot_be_marked_as_real():
    p=payload()
    p['reference_rate']=4.77
    p['reference_source']='FRANKFURTER_LIVE'
    p['reference_date']='2026-10-14'
    r=client.post('/api/plans',json=p)
    assert r.status_code==200
    assert r.json()['reference_rate']['classification']=='USER_ENTERED_UNVERIFIED'

def test_plain_english_assistant_api_with_sources_and_actions():
    r=client.post('/api/chat',json={'message':'What are living costs in Japan?', 'country':'Australia'})
    assert r.status_code==200
    data=r.json()
    assert 'JPY' in data['message']
    assert data['sources']
    assert any(item['target']=='sources' for item in data['actions'])


def test_agent_guide_about_caps_does_not_make_up_quotes():
    r=client.post('/api/chat',json={'message':'What can you do?'})
    assert r.status_code==200
    data=r.json()
    assert 'four student finance needs' in data['message']
    assert 'tools_used' in data
