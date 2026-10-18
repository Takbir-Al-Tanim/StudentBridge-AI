"""New independently implemented V8 workflow tests (uses disposable SQLite fixture)."""
from datetime import date, timedelta
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app import main
from app.journey import calendar_bytes, deadline_check, planning_preview
from app.logic import evaluate

client=TestClient(app)

def test_budget_shield_requires_extra_funds():
    payload={'origin':'Bangladesh','destination':'Australia','origin_currency':'BDT','destination_currency':'AUD',
        'tuition_amount':1000,'scholarship_amount':0,'available_balance':110000,'emergency_reserve':10000,
        'monthly_living_cost':500,'living_months':3,'deadline':(date.today()+timedelta(days=35)).isoformat(),
        'quotes':[{'provider':'Entered provider','rate':80,'fixed_fee':0,'fee_percent':0,'eta_days':2,'eligible':True,'source_url':'https://example.org'}]}
    unprotected=evaluate(payload)
    assert unprotected['recommended_quote_id'] is not None
    payload['protect_living_costs']=True
    protected=evaluate(payload)
    assert protected['recommended_quote_id'] is None
    assert protected['quotes'][0]['protected_living_origin']==120000
    assert protected['quotes'][0]['viable'] is False

def test_journey_preview_no_rate_does_not_fabricate():
    r=planning_preview(amount=1000,scholarship=0,available=100000,reserve=10000,
        living_per_month=600,months=3,reference_rate=None,reference_date=None,
        origin_currency='BDT',destination_currency='AUD',deadline=date.today()+timedelta(days=25))
    assert r['estimated_tuition_origin'] is None
    assert r['protection_status']=='unknown'


def test_journey_preview_with_explicit_reference_rate():
    r=planning_preview(amount=1000,scholarship=0,available=300000,reserve=10000,
        living_per_month=600,months=3,reference_rate=80,reference_date='2026-10-17',
        origin_currency='BDT',destination_currency='AUD',deadline=date.today()+timedelta(days=25))
    assert r['estimated_tuition_origin']==80000
    assert r['estimated_living_origin']==144000
    assert r['remaining_after_protection']==66000


def test_calendar_endpoint_and_ics_injection_protection():
    d=(date.today()+timedelta(days=35)).isoformat()
    r=client.get('/api/journey/calendar',params={'deadline':d,'title':'Invoice;\nATTACK:1','remind_days':7})
    assert r.status_code==200
    assert r.headers['content-type'].startswith('text/calendar')
    assert b'DTSTART;VALUE=DATE:' in r.content
    assert b'\nATTACK:1' not in r.content
    assert b'Invoice\\;' in r.content


def test_journey_automates_safe_tools_only(monkeypatch):
    async def stub_fx(*,base,quote):
        assert base=='AUD' and quote=='BDT'
        return {'available':True,'rate':80,'date':'2026-10-17','source_url':'https://example.org/reference'}
    monkeypatch.setattr(main,'fx',stub_fx)
    payload={'goal':'help with tuition','origin':'Bangladesh','destination':'Australia',
             'tuition_amount':1000,'scholarship_amount':100,'available_balance':300000,
             'emergency_reserve':10000,'monthly_living_cost':600,'living_months':3,
             'deadline':(date.today()+timedelta(days=35)).isoformat()}
    r=client.post('/api/journey/prepare',json=payload)
    assert r.status_code==200,r.text
    j=r.json()
    assert j['preview']['estimated_tuition_origin']==72000
    assert len(j['steps'])==5
    assert 'bank or card payment' in j['actions_needing_approval']
    assert 'reference_fx_lookup' in j['tools_used']


def test_journey_rejects_invalid_corridor():
    r=client.post('/api/journey/prepare',json={'origin':'Australia','destination':'Australia',
         'tuition_amount':1,'available_balance':1000,'deadline':date.today().isoformat()})
    assert r.status_code==422

def test_finance_agent_recommends_studio_for_automation():
    from app.assistant import make_answer
    from app.main import CATALOG,SOURCES
    r=make_answer('Please do everything for me and plan my tuition in Australia',CATALOG,SOURCES)
    assert any(x['target']=='studio' for x in r['actions'])
    assert 'real bank quote' in r['message'].lower()


def test_plain_pdf_without_text_is_not_invented():
    from io import BytesIO
    from pypdf import PdfWriter
    stream=BytesIO();writer=PdfWriter();writer.add_blank_page(width=200,height=200);writer.write(stream)
    response=client.post('/api/invoices/analyze',files={'file':('blank.pdf',stream.getvalue(),'application/pdf')})
    assert response.status_code==200,response.text
    assert response.json()['text_found'] is False
    assert response.json()['fields']=={}


def test_public_production_demo_restricts_shared_history(monkeypatch):
    monkeypatch.setenv('APP_ENV','production')
    assert client.get('/api/audit').status_code==403
    assert client.get('/api/audit/verify').status_code==403
    assert client.get('/api/sandbox/history').status_code==403
