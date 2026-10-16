"""Competition feature visibility and no fabricated provider transfer data."""
from pathlib import Path
from app.assistant import make_answer
import json

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'app/templates/index.html').read_text()
JS = (ROOT/'app/static/app.js').read_text()
CATALOG = json.loads((ROOT/'app/data/catalog.json').read_text())
SOURCES = json.loads((ROOT/'app/data/sources.json').read_text())

def test_four_topic_c_views_and_nav():
    for view in ('remit','pay','credit','currencies'):
        assert f'<section id="{view}"' in HTML
        assert f'data-target="{view}"' in HTML
        assert f'data-go="{view}"' in HTML
    assert len(CATALOG['countries']) == 6

def test_remittance_marks_reference_not_quote():
    assert "async function calculateRemittance()" in JS
    assert "Actual rates, intermediary charges, transfer availability" in JS
    assert "route eligibility" in HTML.lower()

def test_multicurrency_missing_rates_are_not_guessed():
    assert "async function calculateCurrencies()" in JS
    assert "Rate unavailable" in JS
    assert "rates, not bank quotes" in JS

def test_credit_checklist_present():
    assert HTML.count('class="credit-check"') == 4
    assert '0 of 4 steps checked' in HTML

def test_assistant_mentions_four_services():
    reply = make_answer('What can you do?',CATALOG,SOURCES)
    for word in ('money transfers','tuition payments','credit','currencies'):
        assert word in reply['message']
