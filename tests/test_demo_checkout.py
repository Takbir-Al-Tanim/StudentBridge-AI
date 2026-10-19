"""End-to-end sandbox checkout; uses disposable SQLite via conftest, not the user's MySQL database."""
from datetime import date, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def req(**changes):
    value={'origin':'Japan','destination':'United Kingdom', 'tuition_amount':2500,
           'available_balance':800000,'emergency_reserve':50000,
           'deadline':(date.today()+timedelta(days=8)).isoformat(),
           'rate':185.0,'university':'Example University'}
    value.update(changes)
    return value

def test_demo_prepare_creates_three_illustrative_methods():
    r=client.post('/api/demo/prepare',json=req())
    assert r.status_code==200,r.text
    result=r.json()
    assert result['demo_only'] is True
    assert result['reference_rate_source']=='USER_ENTERED_DEMO_RATE'
    assert len(result['quotes'])==3
    assert all(q['simulation_only'] for q in result['quotes'])
    assert all(q['source_url'] is None for q in result['quotes'])
    assert result['recommended_quote_id'] in {'demo-bank','demo-card','demo-student'}
    assert 'real transfer' in result['display_notice'].lower() or 'no real banking connection' in result['display_notice'].lower()

def test_demo_checkout_approval_receipt_and_idempotency():
    p=client.post('/api/demo/prepare',json=req()).json()
    quote=p['quotes'][0]
    k='V5-'+str(uuid4())
    payload={'plan_id':p['plan_id'],'quote_id':quote['quote_id'],
       'confirmed':True,'approval_phrase':'APPROVE SANDBOX','idempotency_key':k}
    assert client.post('/api/sandbox/execute',json={**payload,'confirmed':False}).status_code==403
    t=client.post('/api/sandbox/execute',json=payload)
    assert t.status_code==200,t.text
    tx=t.json()['transaction_id']
    receipt=client.get('/api/sandbox/receipt/'+tx)
    assert receipt.status_code==200
    d=receipt.json()
    assert d['receipt_type']=='SIMULATION_ONLY'
    assert d['sending_currency']=='JPY'
    assert d['receiving_currency']=='GBP'
    assert d['method']==quote['provider']
    assert d['sending_amount']==quote['total']
    duplicate=client.post('/api/sandbox/execute',json=payload)
    assert duplicate.status_code==200 and duplicate.json()['duplicate_prevented']

def test_demo_rejects_same_country_and_bad_reserve():
    assert client.post('/api/demo/prepare',json=req(destination='Japan')).status_code==422
    assert client.post('/api/demo/prepare',json=req(emergency_reserve=999999)).status_code==422

def test_short_deadline_disables_slow_methods():
    p=client.post('/api/demo/prepare',json=req(deadline=date.today().isoformat())).json()
    slow=next(x for x in p['quotes'] if x['quote_id']=='demo-student')
    fast=next(x for x in p['quotes'] if x['quote_id']=='demo-card')
    assert not slow['viable']
    assert fast['viable']

def test_regular_quote_cannot_bypass_provenance_with_demo_flag():
    payload={'origin':'China','destination':'Australia','origin_currency':'CNY','destination_currency':'AUD',
       'university':'Demo','tuition_amount':200,'available_balance':10000,'deadline':(date.today()+timedelta(days=10)).isoformat(),
       'quotes':[{'provider':'Unverified test pretending to be real','rate':5,
                  'eligible':True,'simulation_only':True,'eta_days':1}]}
    r=client.post('/api/plans',json=payload)
    assert r.status_code==200
    assert r.json()['recommended_quote_id'] is None

def test_checkout_has_clear_ui_labels():
    home=client.get('/').text
    for expected in ['Tuition payments','Show payment methods','Approve test payment','Download receipt','id="demo-stage-4"']:
        assert expected in home
