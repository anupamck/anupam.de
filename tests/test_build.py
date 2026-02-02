"""Smoke tests: run build and assert key outputs exist."""

from pathlib import Path

import pytest

from build import OUT_DIR, get_jinja_env, run_build


@pytest.fixture(scope="module")
def built_site():
    """Run full build once for all tests."""
    env = get_jinja_env()
    run_build(env)
    return OUT_DIR


def test_index_html_exists(built_site):
    path = built_site / "index.html"
    assert path.exists(), "index.html should exist"
    assert path.read_text().strip().endswith("</html>")

def test_about_page_exists(built_site):
    assert (built_site / "about" / "about.html").exists()

def test_writing_index_exists(built_site):
    assert (built_site / "writing" / "writing.html").exists()

def test_projects_page_exists(built_site):
    assert (built_site / "projects" / "projects.html").exists()
