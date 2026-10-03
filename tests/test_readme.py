from pathlib import Path


def test_readme_exists():
    assert Path("README.md").exists()


def test_readme_has_single_img():
    t = Path("README.md").read_text(encoding="utf-8")
    assert 'assets/escape.svg' in t
    assert t.count("<img") == 1


def test_readme_no_resume_leak():
    t = Path("README.md").read_text(encoding="utf-8").lower()
    for banned in ["shields.io", "github-readme-stats", "tech stack", "experience", "my skills"]:
        assert banned not in t, f"banned token {banned}"


def test_readme_has_broadcast():
    t = Path("README.md").read_text(encoding="utf-8")
    assert "EMERGENCY BROADCAST" in t
    assert "Don't look at him" in t
