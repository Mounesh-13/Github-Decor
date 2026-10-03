from pathlib import Path
import re
def _svg():
    return Path("assets/escape.svg").read_text(encoding="utf-8")
def test_svg_exists_and_size():
    p = Path("assets/escape.svg")
    assert p.exists()
    assert p.stat().st_size < 100 * 1024, "must be <100KB"
def test_svg_no_js_or_external():
    t = _svg()
    assert "<script" not in t.lower()
    assert "foreignobject" not in t.lower()
    # strip mandatory SVG namespace declaration before checking for externals
    t_no_ns = t.replace('xmlns="http://www.w3.org/2000/svg"', '')
    assert "http://" not in t_no_ns and "https://" not in t_no_ns
def test_svg_has_viewbox_and_loop():
    t = _svg()
    assert 'viewBox="0 0 800 400"' in t
    assert 'repeatCount="indefinite"' in t
def test_act1_present():
    t = _svg()
    assert 'id="act1"' in t
    assert 'id="walker"' in t
    assert 'id="banana"' in t
