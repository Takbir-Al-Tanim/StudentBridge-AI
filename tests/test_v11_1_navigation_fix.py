"""V11.1: prevent the old V10 initialization script from breaking redesigned views."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'app/static/app.js').read_text()
HTML = (ROOT / 'app/templates/index.html').read_text()


def test_navigation_registered_before_catalog_request():
    start = JS.index('async function init(){')
    end = JS.index('init().catch(', start)
    bootstrap = JS[start:end]
    assert bootstrap.index("$$('.nav-link')") < bootstrap.index("catalog=await api('/api/catalog')")
    assert 'initProfile()' in bootstrap
    assert 'initRouteCompareSimple()' in bootstrap
    assert 'initRemittance()' in bootstrap


def test_legacy_planner_elements_not_initialized():
    start = JS.index('async function init(){')
    end = JS.index('init().catch(', start)
    bootstrap = JS[start:end]
    for selector in ('#university', '#add-quote', '#build-plan', '#fetch-rate', '#scholarship'):
        assert selector not in bootstrap
    assert 'app.js?v=11.1' in HTML


def test_profile_and_transfer_elements_exist():
    for item in ('profile', 'auth-form', 'top-profile-button', 'remit-form', 'beneficiary-save-button', 'compare-routes-simple'):
        assert f'id="{item}"' in HTML
