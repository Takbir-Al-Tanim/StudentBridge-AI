"""Create LOCAL example transactions in the configured MySQL DB. NO REAL MONEY.

Run only against a non-production demonstration database; the script never
resets/deletes plans or financial data. The input quotes are synthetic.
"""
from pathlib import Path
from datetime import date,timedelta,datetime,timezone
import sys,json,uuid
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from app import database
from app.main import app
from fastapi.testclient import TestClient

if __name__ == '__main__':
    if database.engine().dialect.name != 'mysql':
        raise SystemExit('Configure a dedicated MySQL sandbox database first.')
    if __import__('os').environ.get('APP_ENV','development')=='production':
        raise SystemExit('Refusing to seed the production database.')
    database.initialize()
    client=TestClient(app)
    def req(o,d,oc,dc,u,tuition,savings,reserve,rate):
        return {'origin':o,'destination':d,'origin_currency':oc,'destination_currency':dc,
        'university':u,'tuition_amount':tuition,'scholarship_amount':0,'available_balance':savings,
        'emergency_reserve':reserve,'monthly_living_cost':0,'living_months':6,
        'deadline':(date.today()+timedelta(days=8)).isoformat(),
        'quotes':[{'provider':'TEST ONLY: illustrative student quote','rate':rate,'fixed_fee':100,
                   'fee_percent':0.5,'eta_days':3,'eligible':True,'source_url':None}]}
    cases=[('CHINA_TO_AUSTRALIA',req('China','Australia','CNY','AUD','Melbourne TEST invoice',48992,500000,50000,4.55)),
           ('JAPAN_TO_UK',req('Japan','United Kingdom','JPY','GBP','UK TEST invoice',20000,6000000,800000,190))]
    result=[]
    for name,data in cases:
        response=client.post('/api/plans',json=data)
        assert response.status_code==200,response.text
        plan=response.json()
        simulation=client.post('/api/scenarios',json={'plan_id':plan['plan_id'],
            'fx_change_percent':5,'extra_fee':100,'living_cost_change_percent':10}).json()
        paid=None
        if plan['recommended_quote_id']:
            paid_response=client.post('/api/sandbox/execute',json={'plan_id':plan['plan_id'],
                'quote_id':plan['recommended_quote_id'],'confirmed':True,
                'approval_phrase':'APPROVE SANDBOX','idempotency_key':'EXAMPLE-'+str(uuid.uuid4())})
            assert paid_response.status_code==200,paid_response.text
            paid=paid_response.json()
        result.append({'case':name,'inputs':'SYNTHETIC_NOT_REAL_BANK_QUOTES',
            'plan':plan,'scenario':simulation,'payment':paid})
    evidence={'mode':'MYSQL_SANDBOX_ONLY','created_at_utc':datetime.now(timezone.utc).isoformat(),
        'warning':'No real money; quotes and student profiles are hypothetical demo inputs.',
        'cases':result,'audit_verification':client.get('/api/audit/verify').json()}
    path=root/'evidence'/'mysql_sandbox_example.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print('Wrote',path,'with',len(result),'test scenarios.')
