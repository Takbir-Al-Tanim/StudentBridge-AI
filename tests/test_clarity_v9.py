"""V9 copy and stylesheet regression tests; no production DB required."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'app/templates/index.html').read_text()
CSS = (ROOT / 'app/static/clarity-v9.css').read_text()


def test_feature_first_navigation_and_less_copy():
    assert 'Your money.<br><em>One clear plan.</em>' in HTML
    assert HTML.count('class="topic-c-card"') == 4
    assert '<div class="feature-grid">' not in HTML  # removed duplicate marketing cards
    assert HTML.count('<article class="metric">') == 3
    for view in ('studio','remit','pay','planner','currencies','twin','credit','sources','activity'):
        assert f'<section id="{view}"' in HTML or f'<section id="{view}" class=' in HTML


def test_loads_new_css_last_with_busted_cache():
    assert 'clarity-v9.css?v=9.1' in HTML
    assert 'styles.css?v=9.1' in HTML
    assert 'app.js?v=9.1' in HTML
    assert HTML.index('experience-v8.css?v=9.1') < HTML.index('clarity-v9.css?v=9.1')


def test_design_keeps_originality_and_readability():
    assert '--sb-primary' in CSS
    assert 'font-size:16px!important' in CSS
    assert 'font-size:15px!important' in CSS
    assert '@media(prefers-reduced-motion:reduce)' in CSS
    assert not any(name in HTML.lower() for name in ('fonts.googleapis.com','fonts.gstatic.com'))
    assert (ROOT / 'docs/ORIGINALITY_AND_LICENSES.md').exists()
    assert not (ROOT / 'docs/Competition_Rules.pdf').exists()
