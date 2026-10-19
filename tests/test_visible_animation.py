from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_visible_country_route_controls_exist():
    html = (ROOT / 'app/templates/index.html').read_text()
    assert 'id="hero-route-name"' in html
    assert 'id="hero-motion-toggle"' in html
    assert 'id="hero-route-try"' in html
    assert 'href="/static/styles.css?v=11.1"' in html
    assert 'src="/static/app.js?v=11.1"' in html
    assert 'PAYMENTS · CLEAR AND SECURE' in html

def test_country_route_animation_and_reduced_motion_controls():
    css = (ROOT / 'app/static/styles.css').read_text()
    js = (ROOT / 'app/static/app.js').read_text()
    assert '@keyframes v4-orbit-clockwise' in css
    assert '@keyframes v4-progress' in css
    assert '@media(prefers-reduced-motion:reduce)' in css
    assert 'function initVisibleRouteAnimation()' in js
    assert 'document.visibilityState' in js
    assert "use.addEventListener('click'" in js
    assert 'svg.pauseAnimations' in js
