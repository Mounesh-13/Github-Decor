from pathlib import Path
import re
import xml.etree.ElementTree as ET


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


def test_act2_present():
    t = _svg()
    assert 'id="act2"' in t
    assert 'id="eyes-wide"' in t
    assert 'knock-ripple' in t
    assert 'begin="4s"' in t


def test_act3_present():
    t = _svg()
    assert 'id="act3"' in t
    assert 'id="mallet"' in t
    assert 'id="crack"' in t
    assert 'begin="8s"' in t


def test_act4_present():
    t = _svg()
    assert 'id="act4"' in t
    assert 'leak-drop' in t
    assert 'big-red-button' in t


def test_act5_present():
    t = _svg()
    assert 'id="act5"' in t
    assert 'id="spinner"' in t
    assert 'begin="19s"' in t


def test_no_placeholders():
    t = _svg()
    assert "ACT2" not in t and "ACT3" not in t and "ACT4" not in t and "ACT5" not in t


def test_svg_is_valid_xml():
    ET.fromstring(_svg())


def test_dark_mode_halo():
    t = _svg()
    assert 'paint-order="stroke"' in t, "texts/fills need paint-order halo"
    assert "#fff" in t, "white halo underlays required for #111 shapes on dark"


def test_loop_timing():
    t = _svg()
    # walker must hide after its ~4.5s window
    assert 'values="1;1;0;0"' in t and 'keyTimes="0;0.15;0.19;1"' in t
    # outer 24s gates must be narrow and sequential (act2 -> mallet -> leak -> button -> spinner -> blackout)
    gates = re.findall(r'keyTimes="([\d.;]+)"[^>]*dur="24s"', t)
    assert '0;0.16;0.33;0.37' in gates, "act2 gate must be 3.8-8.9s"
    assert '0;0.94;0.97;1' in gates, "blackout must be ~0.5s"
    starts = []
    for g in ['0;0.16;0.33;0.37', '0;0.33;0.54;0.58', '0;0.58;0.71;0.75',
              '0;0.67;0.79;0.83', '0;0.79;0.96;1', '0;0.94;0.97;1']:
        assert g in gates, f"missing gate {g}"
        starts.append(float(g.split(';')[1]))
    assert starts == sorted(starts), "gates must run sequentially"
    for g in gates:
        ks = [float(k) for k in g.split(';')]
        assert all(0 <= k <= 1 for k in ks), f"keyTimes out of range: {g}"
    # every timed begin must land inside the 24s loop
    for m in re.finditer(r'begin="([\d.]+)s"[^>]*dur="([\d.]+)s"', t):
        begin, dur = float(m.group(1)), float(m.group(2))
        assert 0 <= begin <= 24, f"begin out of loop: {m.group(0)}"
        assert dur <= 24, f"dur out of loop: {m.group(0)}"
    # short one-shots must freeze (no strobing), loop gates keep indefinite
    for m in re.finditer(r'<animate[^>]*begin="(6s|6\.6s|10s|14s|15s)"[^>]*>', t):
        tag = m.group(0)
        assert 'repeatCount="1"' in tag, f"one-shot must not strobe: {tag}"
        assert 'fill="freeze"' in tag, f"one-shot must freeze: {tag}"
