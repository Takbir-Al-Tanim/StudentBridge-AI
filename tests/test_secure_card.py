from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from app import secure_card, database
from app.main import app

client=TestClient(app)

def configure_test(monkeypatch):
    monkeypatch.setenv('STRIPE_SECRET_KEY','sk_test_example_for_unit_tests')
    monkeypatch.setenv('STRIPE_PRICE_ID','price_test_1')
    monkeypatch.setenv('AUTHORIZED_PAYEE_NAME','Authorized Institution')
    monkeypatch.setenv('AUTHORIZED_INVOICE_REFERENCE','INV-2026-ABC')
    monkeypatch.setenv('PUBLIC_BASE_URL','http://127.0.0.1:8000')

def test_absent_credentials_disable_card_checkout(monkeypatch):
    for k in ['STRIPE_SECRET_KEY','STRIPE_PRICE_ID','AUTHORIZED_PAYEE_NAME','AUTHORIZED_INVOICE_REFERENCE']:
        monkeypatch.delenv(k,raising=False)
    response=client.get('/api/card/availability')
    assert response.status_code==200 and response.json()['enabled'] is False
    result=client.post('/api/card/checkout')
    assert result.status_code==503

def test_card_checkout_creates_hosted_address_required_session(monkeypatch):
    configure_test(monkeypatch)
    stripe=Mock()
    stripe.Price.retrieve.return_value=SimpleNamespace(active=True,type='one_time')
    stripe.checkout.Session.create.return_value=SimpleNamespace(id='cs_test_123',url='https://checkout.stripe.com/c/something')
    result=secure_card.checkout(stripe)
    assert result['checkout_url'].startswith('https://checkout.stripe.com/')
    kwargs=stripe.checkout.Session.create.call_args.kwargs
    assert kwargs['billing_address_collection']=='required'
    assert kwargs['payment_method_types']==['card']
    assert kwargs['line_items']==[{'price':'price_test_1','quantity':1}]
    assert 'card_number' not in kwargs
    assert 'cvc' not in kwargs
    assert 'amount' not in kwargs

def test_unverified_merchant_cannot_enable_live_mode(monkeypatch):
    configure_test(monkeypatch)
    monkeypatch.setenv('STRIPE_SECRET_KEY','sk_live_placeholder')
    monkeypatch.setenv('CARD_LIVE_ENABLED','true')
    monkeypatch.setenv('MERCHANT_AUTHORIZED_TO_COLLECT','false')
    monkeypatch.setenv('APP_ENV','production')
    monkeypatch.setenv('PUBLIC_BASE_URL','https://example.com')
    assert secure_card.public_status()['enabled'] is False

def test_rejects_bad_payment_provider_url(monkeypatch):
    configure_test(monkeypatch)
    stripe=Mock()
    stripe.Price.retrieve.return_value=SimpleNamespace(active=True,type='one_time')
    stripe.checkout.Session.create.return_value=SimpleNamespace(id='cs_test_123',url='http://not-secure.example/')
    with pytest.raises(ValueError,match='secure checkout'):
        secure_card.checkout(stripe)

def test_session_status_is_provider_verified(monkeypatch):
    configure_test(monkeypatch)
    stripe=Mock()
    stripe.checkout.Session.retrieve.return_value=SimpleNamespace(
        client_reference_id='INV-2026-ABC',
        metadata={'authorized_payee':'Authorized Institution'},
        payment_status='paid',livemode=False,status='complete',
        currency='gbp',amount_total=10000)
    result=secure_card.session_status(stripe,'cs_test_abcdef')
    assert result['status']=='paid' and result['mode']=='TEST'

def test_card_security_promises_are_visible():
    page=client.get('/').text
    assert 'Pay securely by card' in page
    assert 'billing address' in page.lower()
    assert 'never sees or saves your full card number or CVC' in page
    assert 'No real money was moved.' in page

def test_gateway_events_are_idempotent():
    import uuid
    eid='evt_unit_'+uuid.uuid4().hex
    assert database.record_gateway_event(eid,'cs_test_456','checkout.session.completed','PAID_TEST',b'test-secret') is True
    assert database.record_gateway_event(eid,'cs_test_456','checkout.session.completed','PAID_TEST',b'test-secret') is False
