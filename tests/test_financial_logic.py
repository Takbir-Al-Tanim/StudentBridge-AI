from datetime import date, timedelta
import pytest
from app.logic import evaluate, simulate

def request(days=7):
    return dict(origin='Japan',destination='United Kingdom',origin_currency='JPY',destination_currency='GBP',
                university='Example verified university invoice',tuition_amount=20000,scholarship_amount=3000,
                available_balance=6000000,emergency_reserve=1000000,monthly_living_cost=1400,living_months=9,
                deadline=(date.today()+timedelta(days=days)).isoformat(),
                quotes=[dict(provider='Student entered bank quote',rate=190.0,fixed_fee=1000,
                             fee_percent=1.0,eta_days=3,eligible=True,source_url='https://example.org/quote')])

def test_supported_corridor_and_amount_math():
    r=evaluate(request())
    assert r['required_tuition']==17000
    assert r['quotes'][0]['base_cost']==3230000
    assert r['quotes'][0]['fee_total']==33300
    assert r['quotes'][0]['total']==3263300
    assert r['recommended_quote_id']=='quote-1'

def test_scholarship_cannot_exceed_tuition():
    p=request();p['scholarship_amount']=25000
    with pytest.raises(ValueError,match='Scholarship'):evaluate(p)

def test_no_recommendation_when_deadline_missed():
    r=evaluate(request(days=1))
    assert r['recommended_quote_id'] is None
    assert 'deadline' in ' '.join(r['quotes'][0]['issues'])

def test_no_recommendation_when_not_eligible():
    p=request();p['quotes'][0]['eligible']=False
    assert evaluate(p)['recommended_quote_id'] is None

def test_protected_reserve_enforced():
    p=request();p['available_balance']=4000000;p['emergency_reserve']=900000
    r=evaluate(p)
    assert not r['quotes'][0]['reserve_maintained']
    assert r['recommended_quote_id'] is None

def test_empty_quotes_does_not_fabricate_transfer_offer():
    p=request();p['quotes']=[]
    r=evaluate(p,{'rate':195.0,'date':'2026-10-10','classification':'FRANKFURTER_LIVE'})
    assert r['recommended_quote_id'] is None
    assert r['reference_only_estimate']==3315000

def test_expired_quote_blocked():
    p=request();p['quotes'][0]['expires_on']=(date.today()-timedelta(days=1)).isoformat()
    assert evaluate(p)['recommended_quote_id'] is None

def test_fx_stress_test_uses_correct_percentage():
    r=evaluate(request());s=simulate(r,10,500)
    assert s['ready']
    assert s['scenario_total']>r['quotes'][0]['total']
    assert s['cost_change']==326730.0

def test_cannot_exceed_stress_limits():
    with pytest.raises(ValueError):simulate(evaluate(request()),999)

def test_no_cross_border_same_country():
    p=request();p['destination']='Japan'
    with pytest.raises(ValueError):evaluate(p)

def test_cheapest_unsuitable_is_not_recommended():
    p=request()
    p['quotes']=[
      dict(provider='Cheap late route',rate=180.0,fixed_fee=0,fee_percent=0,eta_days=10,eligible=True,source_url='https://example.org/late'),
      dict(provider='Affordable on time',rate=190.0,fixed_fee=0,fee_percent=0,eta_days=2,eligible=True,source_url='https://example.org/on-time'),
    ]
    r=evaluate(p)
    assert r['recommended_quote_id']=='quote-2'
    assert r['quotes'][0]['provider']=='Affordable on time'

def test_fee_percent_and_fixed_fee_applied():
    p=request();p['quotes'][0].update(rate=100,fee_percent=2,fixed_fee=50)
    r=evaluate(p)
    assert r['quotes'][0]['total']==1734050.0


def test_source_evidence_is_required_for_shortlist():
    p=request();p['quotes'][0]['source_url']=None
    r=evaluate(p)
    assert r['recommended_quote_id'] is None
    assert 'Missing quote evidence URL' in r['quotes'][0]['issues']
