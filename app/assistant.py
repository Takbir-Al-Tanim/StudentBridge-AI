"""Source-aware, plain-English finance guidance for the StudentBridge demo.

The answerer only uses bundled catalog entries and saved deterministic plans.
It does not claim that a published reference rate is a transferable bank offer.
"""
from __future__ import annotations
import re
from typing import Any
from .logic import simulate

ALIASES = {
    'South Korea': ('south korea', 'korea', 'korean'),
    'United Kingdom': ('united kingdom', 'uk', 'britain', 'british', 'england'),
    'Australia': ('australia', 'australian'),
    'Bangladesh': ('bangladesh', 'bangladeshi'),
    'China': ('china', 'chinese'),
    'Japan': ('japan', 'japanese'),
}
CURRENCY = {'CNY':'China','GBP':'United Kingdom','JPY':'Japan',
            'KRW':'South Korea','AUD':'Australia','BDT':'Bangladesh'}

def countries_in(text: str) -> list[str]:
    seen = []
    for m in re.finditer(r'\b(?:south korea|united kingdom|bangladesh|australia|britain|england|chinese|bangladeshi|australian|japanese|korean|china|japan|korea|uk)\b',text.lower()):
        token=m.group(0)
        for country, aliases in ALIASES.items():
            if token in aliases and country not in seen:
                seen.append(country)
                break
    return seen

def make_answer(message: str, catalog: dict, sources: list[dict], plan: dict | None = None,
                country: str | None = None) -> dict[str, Any]:
    """Return a safe answer, clickable sources, next actions and tool trace."""
    query=message.strip().lower()
    named=countries_in(message)
    chosen=named[-1] if named else (country if country in ALIASES else (plan or {}).get('destination','Australia'))
    by_source={s['id']:s for s in sources}
    citations=[]
    tools=[]
    actions=[]
    def source(source_id: str | None = None, url: str | None = None, title: str | None = None):
        s=by_source.get(source_id) if source_id else None
        link=url or (s or {}).get('url')
        if link and link.startswith('https://') and not any(x['url']==link for x in citations):
            citations.append({'title':title or (s or {}).get('title','Original source'), 'url':link})
    def action(title: str, target: str):
        if not any(a['target']==target for a in actions):actions.append({'label':title,'target':target})
    def complete(text: str, trace: str) -> dict:
        tools.append(trace)
        return {'message':text,'tools_used':tools,'sources':citations[:5], 'actions':actions[:3],
                'mode':'SOURCE_AWARE_ASSISTANT',
                'safety':'Information and sandbox tools only. No real payment is possible.'}
    # A useful tool call: perform a real deterministic financial what-if calculation.
    whatif=bool(re.search(r'\b(?:what if|if the rate|rate (?:rises|falls|goes up|drops)|exchange rate (?:rises|falls|changes))\b',query))
    percent=re.search(r'(\d+(?:\.\d+)?)\s*%',query)
    if whatif and percent and any(k in query for k in ('rate','exchange','fx','currency')):
        action('Open interactive budget simulator','twin')
        if plan:
            change=float(percent.group(1))
            if any(word in query for word in ('fall','drop','decrease','down','lower')):
                change=-change
            if not -80 <= change <= 200:
                return complete('That rate change is outside the allowed simulation range (minus 80% to plus 200%). Try a smaller value.','scenario_validation')
            result=simulate(plan,change)
            if result['ready']:
                c=plan['origin_currency']
                direction='higher' if change>=0 else 'lower'
                message=(f"If the entered exchange rate becomes {abs(change):g}% {direction}, "
                         f"your simulated tuition cost changes from {result['baseline_total']:,.2f} {c} "
                         f"to {result['scenario_total']:,.2f} {c}. "
                         f"You would have {result['remaining_origin_currency']:,.2f} {c} left. "
                         f"Your protected emergency reserve {'is still covered' if result['reserve_protected'] else 'would be at risk'}. "
                         'This uses your saved, user-entered bank quote; it is a what-if calculation, not a forecast.')
                return complete(message,'financial_digital_twin_calculation')
            return complete(result['message'],'financial_digital_twin')
        action('Create a tuition plan first','planner')
        return complete('I can calculate that scenario, but you need a saved tuition plan with a suitable entered bank quote first. Open the Payment Planner, compare your options, then ask the question again.','financial_digital_twin')
    if any(x in query for x in ('what can you do','what do you do','how do i use','how to use','help me start','what is this','how does this work','features of','what can i ask','your use')):
        action('Send money across borders','remit');action('Pay tuition','pay');action('Manage currencies','currencies')
        return complete('I can help with four student finance needs: (1) estimate international money transfers, (2) plan tuition payments, (3) explain how credit works abroad, and (4) manage six currencies. I also explain living costs and budget scenarios. Choose a sending and destination country in the Payment Planner. I will show sources and tell you when information is missing.','assistant_capabilities')
    if any(x in query for x in ('real money','send money for me','can you pay','make a payment','transfer money now','execute payment')):
        action('Open the test-payment planner','planner')
        return complete('I cannot send real money. StudentBridge is a planning and testing tool. You can compare provider quotes that you enter, then approve a test-only transaction. For an actual tuition transfer, contact an eligible licensed bank or payment provider and check the university payment instructions.','sandbox_policy')
    if any(x in query for x in ('credit','credit score','credit history','loan','borrow')):
        info=catalog.get('credit_guidance',{}).get(chosen)
        action('Open credit tips','credit')
        if info:
            source(info.get('source_id'))
            parts=' '.join(f'{i+1}. {step}' for i,step in enumerate(info['steps']))
            return complete(f'Credit basics for {chosen}: {parts} {info.get("disclaimer", "")} These are general steps, not a credit score or loan approval.','credit_guidance_source')
    if any(x in query for x in ('living','rent','visa money','visa fund','cost of life','cost of living','maintenance','financial requirement','monthly cost','student costs')):
        kind_visa=any(x in query for x in ('visa','maintenance','financial requirement'))
        data=[x for x in catalog.get('financial_benchmarks',[]) if x.get('country')==chosen and x.get('amount') is not None]
        if kind_visa:data=[x for x in data if 'visa_' in x.get('category','')]
        else:
            living=[x for x in data if 'living' in x.get('category','') or 'rent' in x.get('category','')]
            if living:data=living
        action('View published numbers','sources');action('Try the budget planner','planner')
        if data:
            text=[]
            for x in data[:4]:
                figure=f"{float(x['amount']):,.0f} {x.get('currency','')}"
                label=x.get('label') or x.get('category','published figure')
                detail=x.get('unit') or x.get('period') or ''
                status=x.get('status','')
                note=' Historical survey data.' if 'historical' in status.lower() else ''
                text.append(f"{label}: {figure} ({detail}).{note}")
                source(url=x.get('source_url'),title=f'{chosen} published financial guidance')
            intro=f'Published information for {chosen}: '
            return complete(intro+' '.join(text)+' Visa evidence rules are not the same as your actual monthly spending. Check the source date and enter your personal costs in the planner.','financial_benchmark_lookup')
        return complete(f'I do not have a verified country-wide living-cost amount for {chosen} in this dataset. Check official university housing pages and enter your real living costs in the planner. I will not invent a monthly figure.','missing_data_check')
    if any(x in query for x in ('tuition','university fee','course fee','course cost','study fee','program fee','programme fee','college fee')):
        data=[t for t in catalog.get('tuition',[]) if (not named or t['country']==chosen) and t.get('amount') is not None and t.get('input_ready') is not False]
        words=[t for t in re.findall('[a-z]{4,}',query) if t not in {'tuition','university','fees','fee','program','programme','cost','much','what','have','does','about','international','student','course','year'}]
        scored=sorted(data,key=lambda t:sum(1 for w in words if w in (t.get('institution','')+' '+t.get('program','')).lower()),reverse=True)
        if words and scored and sum(1 for w in words if w in (scored[0].get('institution','')+' '+scored[0].get('program','')).lower())>0:
            data=[t for t in scored if any(w in (t.get('institution','')+' '+t.get('program','')).lower() for w in words)][:3]
        else: data=data[:3]
        action('Choose a university','planner');action('Check the original sources','sources')
        if data:
            parts=[]
            for t in data:
                parts.append(f"{t['institution']} — {t['program']}: {float(t['amount']):,.0f} {t['currency']} ({t['year']}, {t['period']}).")
                source(t.get('source_id'))
            return complete(f'Here are published fee examples for {chosen if named else "the supported universities"}: '+' '.join(parts)+' These are not your final tuition invoice. Check your exact program, study load, and due date.','official_tuition_catalog')
        return complete(f'I cannot find a verified program tuition amount for {chosen} matching your question. You can enter the amount shown on your university invoice in the Payment Planner.','missing_tuition_check')
    if any(x in query for x in ('exchange','fx','currency','convert','rate today','rate now','how much is','live rate')):
        action('Fetch a reference rate','planner');action('See historical data','sources')
        used=[m.group(0).upper() for m in re.finditer(r'\b(?:cny|gbp|jpy|krw|aud|bdt)\b',message,re.I)]
        if len(used)<2:
            used=[CURRENCY_KEY for CURRENCY_KEY,c in CURRENCY.items() if c in named]
        if len(used)>=2 and used[0]!=used[1]:
            return {**complete(f'I can look up the published {used[0]} → {used[1]} reference rate. Click “Fetch a reference rate” in the Payment Planner to retrieve the latest available observation. Bank payment rates include their own spread and fees; reference rates are not transfer offers.','fx_reference_guidance'),'fx_pair':{'base':used[0],'quote':used[1]}}
        return complete('Choose two different currencies (CNY, GBP, JPY, KRW, AUD or BDT). In the Payment Planner, click “Fetch reference rate”. I will show the date and source, not invent a bank quote.','fx_reference_guidance')
    if any(x in query for x in ('quote','remittance','transfer','route','bank charges','bank fee','which bank','cheapest','best option','payment method','pay my fees')):
        action('Compare payment options','planner')
        if plan:
            viable=[x for x in plan.get('quotes',[]) if x.get('viable')]
            best=next((x for x in plan.get('quotes',[]) if x.get('quote_id')==plan.get('recommended_quote_id')),None)
            if best:
                failures=[f"{x['provider']}: {', '.join(x['issues'])}" for x in plan.get('quotes',[]) if not x['viable']]
                message=f"Your saved plan's lowest-cost eligible entered quote is {best['provider']}: {best['total']:,.2f} {plan['origin_currency']}, including {best['fee_total']:,.2f} in entered fees. Estimated arrival: {best['eta_days']} days. {plan['days_remaining']} days remain until the deadline. "
                if failures:message+='Other quotes need review: '+'; '.join(failures[:2])+'. '
                return complete(message+'All quotes were entered by the user; the app has not verified their providers or prices.','edu_route_engine')
            return complete(plan['recommendation']+' I will not recommend an unsupported or undocumented transfer method.','edu_route_engine')
        if len(named)>=2:
            pair=f'{named[0]} → {named[1]}'
            return complete(f'For {pair}, check which provider actually supports sending tuition in that direction. Get a dated written rate, fees, delivery estimate, and eligibility confirmation. Then enter the quote in the Payment Planner. We do not have a verified live provider quote for this route.','corridor_eligibility_guidance')
        return complete('To compare transfer options, choose the sending and receiving countries, enter your tuition and deadline, then add actual bank/provider quotes. I check cost, expected arrival, available funds, reserve, and the eligibility you have confirmed. A provider link alone does not mean the app independently verified the offer.','edu_route_workflow')
    if any(x in query for x in ('digital twin','scenario','what if','budget','remaining','savings','reserve','afford','risk','deadline')):
        action('Open budget scenarios','twin');action('Build or review a plan','planner')
        if plan:
            best=next((x for x in plan.get('quotes',[]) if x.get('quote_id')==plan.get('recommended_quote_id')),None)
            if best:
                msg=f"In your saved plan, you have {plan['available_balance']:,.2f} {plan['origin_currency']} in available funds and want to keep {plan['emergency_reserve']:,.2f} as an emergency reserve. The chosen entered quote costs {best['total']:,.2f} {plan['origin_currency']}; that leaves {best['remaining']:,.2f}. There are {plan['days_remaining']} days left before the due date. Try a 5% rate increase in the Digital Twin."
            else:msg=plan['recommendation']+' Add an eligible quote to simulate the impact on your budget.'
            return complete(msg,'financial_digital_twin')
        return complete('The Financial Digital Twin tests a plan before you pay: what if the exchange rate rises, an extra charge appears, or living costs go up? Start by creating a tuition plan with your own funds and a real provider quote. These scenarios are tests, not future predictions.','financial_digital_twin')
    if any(x in query for x in ('scholarship','stipend','sponsor','funding')):
        action('Update the tuition amount','planner')
        return complete('If your scholarship is already confirmed, enter only the tuition waiver or award that applies to this payment in the Payment Planner. We do not have a complete, verified live scholarship database and cannot promise an award. Use the official university offer or scholarship letter for the amount and payment date.','funding_guidance')
    if any(x in query for x in ('passport','why did','why this','explain decision','source','proof','trust')):
        action('View original data','sources');action('Review the payment plan','planner')
        if plan:
            return complete(plan['recommendation']+' The Decision Passport shows which quotes passed the budget and deadline checks, why others failed, and which data are unverified. It is a planning record, not a bank guarantee.','decision_passport')
        return complete('A Decision Passport explains a saved payment plan: fees, deadline checks, rejected quotes, warnings and data sources. Build a payment plan first, then select “View decision passport”.','decision_passport')
    action('Start a payment plan','planner');action('See supported countries','sources');action('View credit tips','credit')
    return complete('I can answer questions about tuition, student living costs, financial requirements, reference exchange rates, credit basics, and your saved payment plan. Try “Tuition in the UK”, “Living costs in Japan”, or “Why was my payment quote rejected?”. If something is not in the available data, I will tell you.','intent_router')
