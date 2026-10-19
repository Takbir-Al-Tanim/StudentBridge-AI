"""V10 transfer workflow, PDF upload, and UI regressions."""
import io
from pathlib import Path
from fastapi.testclient import TestClient
from app import main
from app.transfer_flow import TransferDetails, seal, unseal
from app.main import app
from pypdf import PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
client=TestClient(app)

ROOT=Path(__file__).resolve().parents[1]
SAMPLE={
 'origin':'China','destination':'Australia','sender_name':'Jane Customer',
 'beneficiary_name':'Australian Student','bank_name':'Approved Test Bank',
 'account_number':'123456789','routing_number':'123456','swift_bic':'TESTAU2S',
 'area':'Melbourne, Victoria','amount':'1000.00','method':'bank',
}
HEADERS={'X-SB-Intent':'transfer-review','Origin':'http://testserver'}

def test_bank_requirements_change_by_country():
    r=client.get('/api/transfers/requirements')
    assert r.status_code==200
    assert r.json()['countries']['Australia']['label']=='BSB'
    assert r.json()['countries']['Bangladesh']['label']=='Routing number'
    assert r.json()['countries']['Japan']['example']=='1234-567'

def test_transfer_review_quotes_are_from_server(monkeypatch):
    async def fake_fx(base,quote):
        assert (base,quote)==('CNY','AUD')
        return {'available':True,'rate':0.22,'date':'2026-10-18',
                'source_url':'https://api.frankfurter.dev/v2/rate/CNY/AUD'}
    monkeypatch.setattr(main,'fx',fake_fx)
    r=client.post('/api/transfers/quote',json=SAMPLE,headers=HEADERS)
    assert r.status_code==200,r.text
    quote=r.json()
    assert quote['receiving_estimate']==220.0
    assert quote['account_last4']=='6789'
    assert SAMPLE['account_number'] not in quote['quote_token']
    assert client.post('/api/transfers/prepare',json={'details':SAMPLE,'quote_token':quote['quote_token'],'confirmed':False},headers=HEADERS).status_code==403
    altered={**SAMPLE,'account_number':'55556666'}
    assert client.post('/api/transfers/prepare',json={'details':altered,'quote_token':quote['quote_token'],'confirmed':True},headers=HEADERS).status_code==409
    done=client.post('/api/transfers/prepare',json={'details':SAMPLE,'quote_token':quote['quote_token'],'confirmed':True},headers=HEADERS)
    assert done.status_code==200,done.text
    assert done.json()['status']=='INSTRUCTIONS_PREPARED_ONLY'
    assert 'No money was sent' in done.json()['message']
    assert done.json()['beneficiary_account_last4']=='6789'

def test_bank_details_require_correct_country_format():
    bad={**SAMPLE,'routing_number':'12345'}
    bad_response=client.post('/api/transfers/quote',json=bad,headers=HEADERS)
    assert bad_response.status_code==422
    assert SAMPLE['account_number'] not in bad_response.text
    bad={**SAMPLE,'destination':'Bangladesh','routing_number':'123456789','account_number':'12345678'}
    assert client.post('/api/transfers/quote',json=bad,headers=HEADERS).status_code in (200,503)
    card={**SAMPLE,'method':'card'}
    assert client.post('/api/transfers/quote',json=card,headers=HEADERS).status_code==422

def test_transfer_csrf_intent_header_required():
    assert client.post('/api/transfers/quote',json=SAMPLE).status_code==403
    assert client.post('/api/transfers/quote',json=SAMPLE,headers={'X-SB-Intent':'transfer-review','Origin':'https://other.example'}).status_code==403

def test_pdf_invoice_upload_extracts_fields():
    b=io.BytesIO()
    writer=PdfWriter()
    page=writer.add_blank_page(width=595,height=842)
    font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    ref=writer._add_object(font)
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):ref})})
    stream=DecodedStreamObject()
    stream.set_data(b'BT /F1 12 Tf 60 700 Td (Official tuition invoice AUD 12,345.50 due 2026-12-20) Tj ET')
    page[NameObject('/Contents')]=writer._add_object(stream)
    writer.write(b)
    r=client.post('/api/invoices/analyze',files={'file':('university.pdf',b.getvalue(),'application/pdf')})
    assert r.status_code==200,r.text
    assert '12345.50' not in r.text or '12,345.50' in r.text
    assert '12,345.50' in r.json()['fields']['amount_candidates']
    assert '2026-12-20' in r.json()['fields']['date_candidates']
    assert r.headers['Cache-Control'].startswith('no-store')

def test_ui_and_pdf_are_wired_up():
    html=(ROOT/'app/templates/index.html').read_text()
    js=(ROOT/'app/static/app.js').read_text()
    for name in ('remit-routing','remit-area','remit-bank','remit-beneficiary','remit-account','invoice-file','invoice-result'):
        assert f'id="{name}"' in html
    assert '/api/invoices/analyze' in js
    assert 'finance-v10.css?v=11.1' in html
