import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app import database

client=TestClient(app)
ROOT=Path(__file__).resolve().parents[1]

def test_research_is_available_and_clearly_classified():
    r=client.get('/api/research/summary')
    assert r.status_code==200
    assert r.json()['verified_provider_quotes']==0
    p=client.get('/api/catalog').json()
    assert len(p['historical_reference_fx'])==7
    assert all(x['status']=='HISTORICAL_UPLOADED_REFERENCE_RECHECK' for x in p['historical_reference_fx'])
    assert any(x['program']=='Computer Science BSc' and x['amount']==46700 for x in p['tuition'])
    assert any(x['country']=='Japan' and x['amount']==105000 for x in p['financial_benchmarks'])

def test_benchmarks_api_filters_country_and_preserves_type():
    r=client.get('/api/research/benchmarks?country=United%20Kingdom')
    assert r.status_code==200
    assert all(x['country']=='United Kingdom' for x in r.json()['data'])
    assert client.get('/api/research/benchmarks?country=Atlantis').status_code==422

def test_research_seed_loaded_into_application_db():
    counts=database.research_counts()
    assert counts['countries']==6
    assert counts['payment_quotes']==7
    from sqlalchemy import select,func
    with database.engine().connect() as conn:
        verified=conn.execute(select(func.count()).select_from(database.payment_quotes).where(
            database.payment_quotes.c.quoted_fx_rate.is_not(None))).scalar_one()
    assert verified==0

def test_payment_quote_csv_repaired():
    import csv
    with (ROOT/'data/research/corrected/payment_quotes.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    assert rows[0]['verification_status']=='unverified_quote_required'
    assert rows[0]['notes'].startswith('No provider-specific')
    assert None not in rows[0]
