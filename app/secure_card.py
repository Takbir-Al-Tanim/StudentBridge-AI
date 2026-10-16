"""Provider-hosted card checkout. Never collects PAN, CVC, or card expiry.

NOTE: These functions are not a remittance or university settlement service.
Enabling real charges needs merchant eligibility and authorization to collect
for the invoice/recipient. Default is disabled.
"""
from __future__ import annotations
import os
from urllib.parse import urlparse


def details():
    key=os.getenv('STRIPE_SECRET_KEY','').strip()
    payee=os.getenv('AUTHORIZED_PAYEE_NAME','').strip()
    invoice=os.getenv('AUTHORIZED_INVOICE_REFERENCE','').strip()
    price=os.getenv('STRIPE_PRICE_ID','').strip()
    base=os.getenv('PUBLIC_BASE_URL','http://127.0.0.1:8000').rstrip('/')
    is_test=key.startswith('sk_test_')
    is_live=key.startswith('sk_live_')
    complete=bool((is_test or is_live) and payee and invoice and price.startswith('price_'))
    permitted_live=(os.getenv('APP_ENV')=='production' and
        os.getenv('CARD_LIVE_ENABLED')=='true' and
        os.getenv('MERCHANT_AUTHORIZED_TO_COLLECT')=='true' and
        urlparse(base).scheme=='https')
    enabled=bool(complete and (is_test or permitted_live))
    why=''
    if not complete:why='Card checkout is not connected. A merchant must configure the payment provider and authorized invoice.'
    elif is_live and not permitted_live:why='Live charges are locked until merchant verification, HTTPS and the live-authorization settings are complete.'
    return dict(enabled=enabled,mode=('TEST' if is_test else 'LIVE' if is_live else 'UNCONFIGURED'),
        payee=payee,invoice_reference=invoice,base_url=base,secret=key,price_id=price,reason=why)


def public_status():
    d=details()
    return {k:d[k] for k in ('enabled','mode','payee','invoice_reference','reason')}


def checkout(provider):
    d=details()
    if not d['enabled']:
        raise ValueError(d['reason'] or 'Card payment is currently unavailable')
    if d['mode']=='LIVE' and not os.getenv('STRIPE_WEBHOOK_SECRET','').startswith('whsec_'):
        raise ValueError('A verified payment webhook is required before accepting live charges.')
    provider.api_key=d['secret']
    # Price is configured in the merchant dashboard. Never take a card charge
    # amount from a browser request or an unverified reference conversion.
    price=provider.Price.retrieve(d['price_id'])
    if not getattr(price,'active',False):raise ValueError('The merchant payment item is not active.')
    if getattr(price,'type',None)!='one_time':raise ValueError('Only a one-time authorized invoice is supported.')
    session=provider.checkout.Session.create(
        mode='payment',payment_method_types=['card'],
        line_items=[{'price':d['price_id'],'quantity':1}],
        billing_address_collection='required',
        client_reference_id=d['invoice_reference'],
        metadata={'invoice_reference':d['invoice_reference'],'authorized_payee':d['payee']},
        success_url=d['base_url']+'/?card_session_id={CHECKOUT_SESSION_ID}',
        cancel_url=d['base_url']+'/?card_checkout=cancelled',
    )
    url=session.url
    if not url or not url.startswith('https://checkout.stripe.com/'):
        raise ValueError('The payment provider did not return a secure checkout link.')
    return {'checkout_url':url,'mode':d['mode'],'session_id':session.id}


def session_status(provider,session_id):
    d=details()
    if not d['enabled']:raise ValueError('Card checkout is not configured.')
    if not (session_id.startswith('cs_test_') or session_id.startswith('cs_live_')):
        raise ValueError('Invalid checkout reference')
    provider.api_key=d['secret']
    session=provider.checkout.Session.retrieve(session_id)
    meta=session.metadata or {}
    if session.client_reference_id != d['invoice_reference'] or meta.get('authorized_payee')!=d['payee']:
        raise ValueError('Checkout reference does not match the authorized invoice.')
    return {'status':session.payment_status,'mode':'LIVE' if session.livemode else 'TEST',
            'provider_status':session.status,'payee':d['payee'],
            'currency':session.currency,'amount_total':session.amount_total,
            'invoice_reference':d['invoice_reference'], 'session_id':session_id}
