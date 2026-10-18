"""Opt-in real MySQL *sandbox* API smoke test. Writes one synthetic plan/payment.

REQUIRES: APP_ENV!=production, MYSQL_SMOKE_TEST=YES, a private test DB.
This performs NO bank transfer.
"""
import os,sys,uuid
from datetime import date,timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import database
from app.main import app
from fastapi.testclient import TestClient

def run():
    if os.getenv('MYSQL_SMOKE_TEST')!='YES' or os.getenv('APP_ENV')=='production':
        raise SystemExit('Safety check: set MYSQL_SMOKE_TEST=YES and use a NON-PRODUCTION MySQL database.')
    if database.engine().dialect.name!='mysql':raise SystemExit('Expected MySQL DATABASE_URL')
    with TestClient(app) as client:
        health=client.get('/api/health')
        assert health.status_code==200 and health.json()['database_engine']=='mysql',health.text
        data={'origin':'Japan','destination':'United Kingdom','origin_currency':'JPY',
              'destination_currency':'GBP','university':'SYNTHETIC SMOKE TEST',
              'tuition_amount':1000,'scholarship_amount':0,'available_balance':1000000,
              'emergency_reserve':100000,'monthly_living_cost':0,'living_months':0,
              'deadline':(date.today()+timedelta(days=10)).isoformat(),
              'quotes':[{'provider':'TEST ONLY - NOT AN ACTUAL BANK QUOTE','rate':180,
                         'fixed_fee':400,'fee_percent':0.5,'eta_days':2,'eligible':True}]}
        r=client.post('/api/plans',json=data)
        assert r.status_code==200,r.text
        plan=r.json()
        assert plan['recommended_quote_id'],plan
        passport=client.get('/api/passport/'+plan['plan_id'])
        assert passport.status_code==200
        key='TEST-'+str(uuid.uuid4())
        req={'plan_id':plan['plan_id'],'quote_id':plan['recommended_quote_id'],
             'confirmed':True,'approval_phrase':'APPROVE SANDBOX','idempotency_key':key}
        paid=client.post('/api/sandbox/execute',json=req)
        assert paid.status_code==200,paid.text
        replay=client.post('/api/sandbox/execute',json=req)
        assert replay.status_code==200 and replay.json()['duplicate_prevented'] is True
        chain=client.get('/api/audit/verify').json()
        assert chain['valid'],chain
        print('LIVE MYSQL SMOKE TEST: PASS')
        print('Plan:',plan['plan_id'])
        print('Sandbox transaction:',paid.json()['transaction_id'],'(NO REAL MONEY)')
        print('Audit chain:',chain['checked'],'entries checked')
if __name__=='__main__':run()
