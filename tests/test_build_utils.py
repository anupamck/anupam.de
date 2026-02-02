"""Unit tests for pure functions in build.py."""

import tempfile
from pathlib import Path

from build import base_path_from_output_path, load_md_with_frontmatter


class TestBasePathFromOutputPath:
    def test_root_level(self):
        assert base_path_from_output_path("index.html") == "."

    def test_one_level_deep(self):
        assert base_path_from_output_path("about/about.html") == ".."

    def test_two_levels_deep(self):
        assert base_path_from_output_path("writing/essays/foo.html") == "../.."

    def test_dot_parent(self):
        assert base_path_from_output_path(".") == "."


class TestLoadMdWithFrontmatter:
    def test_with_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.md"
            path.write_text(
                "---\n"
                "title: Foo\n"
                "date: Jan-2024\n"
                "---\n"
                "\n"
                "Hello **world**."
            )
            frontmatter, html = load_md_with_frontmatter(path)
            assert frontmatter == {"title": "Foo", "date": "Jan-2024"}
            assert "<strong>world</strong>" in html
            assert "Hello" in html

    def test_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.md"
            path.write_text("Plain markdown.\n\nNo front matter.")
            frontmatter, html = load_md_with_frontmatter(path)
            assert frontmatter == {}
            assert "Plain markdown" in html

    def test_empty_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.md"
            path.write_text("---\n---\n\nBody text.")
            frontmatter, html = load_md_with_frontmatter(path)
            assert frontmatter == {}
            assert "Body text" in html
