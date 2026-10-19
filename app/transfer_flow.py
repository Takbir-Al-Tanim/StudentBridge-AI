"""Country-aware beneficiary validation and short-lived, tamper-evident transfer reviews.

This is a planning/review flow, NOT a funds-movement integration. Never accept PAN/CVC.
No beneficiary bank information is written to a database or signed token.
"""
from __future__ import annotations
import base64
import hashlib
import hmac
import json
import re
import time
import uuid
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, Field, ConfigDict, model_validator

COUNTRY_ROUTING = {
    'Bangladesh': {'label': 'Routing number', 'pattern': r'^\d{9}$', 'example': '9 digits', 'area': 'District / city', 'hint': '9-digit Bangladesh bank routing number'},
    'Australia': {'label': 'BSB', 'pattern': r'^\d{6}$', 'example': '6 digits', 'area': 'State / suburb', 'hint': '6-digit BSB (branch code)'},
    'United Kingdom': {'label': 'Sort code', 'pattern': r'^\d{6}$', 'example': '6 digits', 'area': 'City / county', 'hint': '6-digit UK sort code'},
    'China': {'label': 'CNAPS / branch clearing code', 'pattern': r'^\d{12}$', 'example': '12 digits', 'area': 'Province / city', 'hint': '12-digit CNAPS for relevant CNY routes; confirm with bank'},
    'Japan': {'label': 'Bank code / branch code', 'pattern': r'^\d{4}-\d{3}$', 'example': '1234-567', 'area': 'Prefecture / city', 'hint': '4-digit bank code and 3-digit branch code'},
    'South Korea': {'label': 'Bank code', 'pattern': r'^\d{3}$', 'example': '3 digits', 'area': 'City / province', 'hint': '3-digit Korean bank code'},
}
ACCOUNT_PATTERNS = {
    'Bangladesh': r'^\d{8,20}$',
    'Australia': r'^\d{6,10}$',
    'United Kingdom': r'^\d{8}$',
    'China': r'^\d{8,30}$',
    'Japan': r'^\d{7}$',
    'South Korea': r'^\d{8,16}$',
}

class TransferDetails(BaseModel):
    model_config=ConfigDict(extra='forbid', str_strip_whitespace=True)
    origin: str
    destination: str
    sender_name: str=Field(min_length=2,max_length=90)
    beneficiary_name: str=Field(min_length=2,max_length=90)
    bank_name: str=Field(min_length=2,max_length=120)
    account_number: str=Field(min_length=6,max_length=30)
    routing_number: str=Field(min_length=3,max_length=20)
    swift_bic: str=Field(default='',max_length=11)
    area: str=Field(min_length=2,max_length=90)
    amount: Decimal=Field(gt=Decimal('0'),le=Decimal('10000000'),max_digits=12,decimal_places=2)
    method: str='bank'

    @model_validator(mode='after')
    def validate(self):
        if self.origin not in COUNTRY_ROUTING or self.destination not in COUNTRY_ROUTING or self.origin==self.destination:
            raise ValueError('Choose two different supported countries.')
        if self.method!='bank':
            raise ValueError('Card transfers require an authorized provider-hosted payment for an approved invoice. Use Tuition payments.')
        for field in ('sender_name','beneficiary_name','bank_name','area'):
            s=getattr(self,field)
            if not re.fullmatch(r"[^<>\x00-\x1f]{2,120}",s):
                raise ValueError(f'Invalid {field.replace("_", " ")}.')
        bank_account=self.account_number.replace(' ','').replace('-','')
        route=self.routing_number.replace(' ','')
        if self.destination=='Australia' or self.destination=='United Kingdom':
            route=route.replace('-','')
        if not re.fullmatch(ACCOUNT_PATTERNS[self.destination],bank_account):
            raise ValueError('Account number has an invalid format for the receiving country.')
        if not re.fullmatch(COUNTRY_ROUTING[self.destination]['pattern'],route):
            raise ValueError(f"{COUNTRY_ROUTING[self.destination]['label']} format is invalid ({COUNTRY_ROUTING[self.destination]['example']}).")
        self.account_number=bank_account
        self.routing_number=route
        if self.swift_bic:
            bic=self.swift_bic.upper()
            if not re.fullmatch(r'[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?',bic):
                raise ValueError('SWIFT/BIC must contain 8 or 11 characters.')
            self.swift_bic=bic
        return self

class TransferApproval(BaseModel):
    details: TransferDetails
    quote_token: str=Field(min_length=20,max_length=1500)
    confirmed: bool

def details_hash(details:TransferDetails):
    return hashlib.sha256(details.model_dump_json().encode()).hexdigest()

def seal(details:TransferDetails,rate:float,observation:str|None,currency:str,secret:bytes):
    # Only digest, not bank account, is included in the token.
    payload={'v':1,'digest':details_hash(details),'rate':rate,'date':observation,
             'currency':currency,'expires':int(time.time())+900,'nonce':uuid.uuid4().hex}
    raw=base64.urlsafe_b64encode(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).decode().rstrip('=')
    mac=hmac.new(secret,raw.encode(),hashlib.sha256).hexdigest()
    return raw+'.'+mac

def unseal(token:str,details:TransferDetails,secret:bytes):
    try:
        raw,signature=token.rsplit('.',1)
        expected=hmac.new(secret,raw.encode(),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature,expected):raise ValueError('Review signature does not match.')
        obj=json.loads(base64.urlsafe_b64decode(raw+'='*((-len(raw))%4)))
        if obj.get('v')!=1 or obj['digest']!=details_hash(details):raise ValueError('Transfer information changed. Generate a new review.')
        if not int(time.time())<=int(obj['expires'])<=int(time.time())+901:raise ValueError('Review expired. Generate a new review.')
        return obj
    except (KeyError,TypeError,OverflowError,ValueError,IndexError) as exc:
        raise ValueError('Invalid or expired transfer review. Please review again.') from exc

def make_estimate(details:TransferDetails,rate:float,currency:str):
    amount=(details.amount*Decimal(str(rate))).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
    return {'sending_amount':float(details.amount),'receiving_estimate':float(amount),
            'sending_currency':currency,'bank_name':details.bank_name,
            'receiving_country':details.destination,'beneficiary_name':details.beneficiary_name,
            'account_last4':details.account_number[-4:], 'routing_label':COUNTRY_ROUTING[details.destination]['label'],
            'payment_method':'Bank transfer review','reference_only':True,
            'warning':'Reference-rate estimate before provider fees and charges. Not a bank quote or a completed transfer.'}
