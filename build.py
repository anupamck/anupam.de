#!/usr/bin/env python3
"""
Static site generator: content (Markdown + JSON) + Jinja2 templates -> HTML.
Output goes to _site/. Copy style.css and images/ there; deploy _site/.

Preview locally: python build.py --serve
"""

import argparse
import http.server
import os
import shutil
import socketserver
import webbrowser
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "site"
TEMPLATES_DIR = ROOT / "templates"
OUT_DIR = ROOT / "_site"
STATIC_SOURCES = ["style.css", "images", "audio", "projects"]


def base_path_from_output_path(output_rel: str) -> str:
    """Relative path from output file to site root, for links and CSS."""
    parts = Path(output_rel).parent.parts
    if not parts or parts == ("."):
        return "."
    return "/".join(".." for _ in parts)


def copy_static():
    """Copy style.css and images/ into _site/."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in STATIC_SOURCES:
        src = ROOT / name
        if not src.exists():
            continue
        dst = OUT_DIR / name
        if src.is_file():
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True)


def load_md(path: Path) -> str:
    """Read Markdown file and return HTML body."""
    text = path.read_text(encoding="utf-8")
    return markdown.markdown(text, extensions=["extra"])


def load_md_with_frontmatter(path: Path, extensions=None):
    """Read Markdown file with YAML front matter, return (frontmatter_dict, html_body)."""
    extensions = extensions or ["extra"]
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2]
            return frontmatter or {}, markdown.markdown(body, extensions=extensions)
    # No front matter, return empty dict and full markdown
    return {}, markdown.markdown(text, extensions=extensions)


def get_jinja_env():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    return env


def build_now(env: Environment):
    """Render homepage from site/now.yaml."""
    now_yaml = CONTENT_DIR / "now.yaml"
    if not now_yaml.exists():
        return
    data = yaml.safe_load(now_yaml.read_text(encoding="utf-8")) or {}
    sections = data.get("sections", [])
    for section in sections:
        content = section.get("content", "")
        section["content_html"] = markdown.markdown(content, extensions=["extra"])
    out_rel = "index.html"
    template = env.get_template("now.html")
    html = template.render(
        title="Now",
        section="now",
        base_path=base_path_from_output_path(out_rel),
        profile_image=data.get("profile_image", "images/nowPic.jpeg"),
        profile_alt=data.get("profile_alt", ""),
        updates=data.get("updates", []),
        updated=data.get("updated", ""),
        sections=sections,
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / out_rel).write_text(html, encoding="utf-8")
    print(f"  {out_rel}")


def build_about(env: Environment):
    """Render About page from site/about.md."""
    about_md = CONTENT_DIR / "about.md"
    if not about_md.exists():
        return
    main_html = load_md(about_md)
    out_rel = "about/about.html"
    (OUT_DIR / "about").mkdir(parents=True, exist_ok=True)
    template = env.get_template("about.html")
    html = template.render(
        title="About",
        section="about",
        base_path=base_path_from_output_path(out_rel),
        main_html=main_html,
    )
    (OUT_DIR / out_rel).write_text(html, encoding="utf-8")
    print(f"  {out_rel}")


def build_projects(env: Environment):
    """Render Projects page from site/projects.yaml."""
    projects_yaml = CONTENT_DIR / "projects.yaml"
    out_rel = "projects/projects.html"
    (OUT_DIR / "projects").mkdir(parents=True, exist_ok=True)
    template = env.get_template("projects.html")
    base_path = base_path_from_output_path(out_rel)

    if not projects_yaml.exists():
        return

    data = yaml.safe_load(projects_yaml.read_text(encoding="utf-8")) or {}
    projects = data.get("projects", [])
    for project in projects:
        description = project.get("description", "")
        project["description_html"] = markdown.markdown(description, extensions=["extra"])
    html = template.render(
        title="Projects",
        section="projects",
        base_path=base_path,
        projects=projects,
    )

    (OUT_DIR / out_rel).write_text(html, encoding="utf-8")
    print(f"  {out_rel}")


def build_collection(
    env: Environment,
    content_subdir: str,
    template_name: str,
    out_subdir: str,
    md_extensions=None,
):
    """Render a content collection from site/<subdir>/*.md."""
    content_dir = CONTENT_DIR / content_subdir
    if not content_dir.exists():
        return
    template = env.get_template(template_name)
    for md_file in content_dir.glob("*.md"):
        frontmatter, content_html = load_md_with_frontmatter(md_file, extensions=md_extensions)
        title = frontmatter.get("title", md_file.stem.replace("_", " ").title())
        date = frontmatter.get("date", "")
        slug = md_file.stem
        out_rel = f"writing/{out_subdir}/{slug}.html"
        (OUT_DIR / "writing" / out_subdir).mkdir(parents=True, exist_ok=True)
        html = template.render(
            title=title,
            date=date,
            section="writing",
            base_path=base_path_from_output_path(out_rel),
            content_html=content_html,
        )
        (OUT_DIR / out_rel).write_text(html, encoding="utf-8")
        print(f"  {out_rel}")


def build_essays(env: Environment):
    """Render all essays from site/essays/*.md."""
    build_collection(env, "essays", "essay.html", "essays")


def build_poetry(env: Environment):
    """Render all poems from site/poetry/*.md."""
    build_collection(env, "poetry", "poem.html", "poetry", md_extensions=["extra", "nl2br"])


def build_shortstories(env: Environment):
    """Render all short stories from site/shortstories/*.md."""
    build_collection(env, "shortstories", "essay.html", "shortstories")


def build_older_blogs(env: Environment):
    """Render all legacy blog posts (Pom-Musings, Sculptures in Sand)."""
    # Pom-Musings
    build_collection(env, "poMusing", "essay.html", "poMusing")
    # Sculptures in Sand
    build_collection(env, "sculpturesInSand", "essay.html", "sculpturesInSand")


def build_combined_older_blogs_page(env: Environment):
    """Render a single Older Blogs page from poMusing.yaml and sculpturesInSand.yaml.
    """
    collections = []
    for yaml_name, heading in [
        ("sculpturesInSand.yaml", "Sculptures in Sand"),
        ("poMusing.yaml", "Pom-Musings"),
    ]:
        index_yaml = CONTENT_DIR / yaml_name
        if not index_yaml.exists():
            continue
        data = yaml.safe_load(index_yaml.read_text(encoding="utf-8")) or {}
        items = data.get("items", [])
        if items:
            collections.append({"heading": heading, "entries": items})

    if not collections:
        return

    out_rel = "writing/olderBlogs.html"
    (OUT_DIR / "writing").mkdir(parents=True, exist_ok=True)
    template = env.get_template("olderBlogs.html")
    html = template.render(
        title="Older Blogs",
        heading="Older Blogs",
        section="writing",
        base_path=base_path_from_output_path(out_rel),
        collections=collections,
    )
    (OUT_DIR / out_rel).write_text(html, encoding="utf-8")
    print(f"  {out_rel}")


def build_writing_index(env: Environment):
    """Render writing/writing.html from site/writing.yaml."""
    writing_yaml = CONTENT_DIR / "writing.yaml"
    if not writing_yaml.exists():
        return

    data = yaml.safe_load(writing_yaml.read_text(encoding="utf-8")) or {}
    out_rel = "writing/writing.html"
    (OUT_DIR / "writing").mkdir(parents=True, exist_ok=True)

    template = env.get_template("writing.html")
    html = template.render(
        title="Writing",
        section="writing",
        base_path=base_path_from_output_path(out_rel),
        daily_blog=data.get("daily_blog", {}),
        older_blogs=data.get("older_blogs", []),
        sections=data.get("sections", []),
    )
    (OUT_DIR / out_rel).write_text(html, encoding="utf-8")
    print(f"  {out_rel}")


def run_build(env: Environment):
    """Run the full build (static + all pages)."""
    copy_static()
    build_now(env)
    build_about(env)
    build_projects(env)
    build_essays(env)
    build_poetry(env)
    build_shortstories(env)
    build_older_blogs(env)
    build_combined_older_blogs_page(env)
    build_writing_index(env)


def serve(port: int = 8000):
    """Serve _site/ at http://127.0.0.1:port/ and open in browser."""
    if not OUT_DIR.exists():
        print("_site/ not found. Run build first.")
        return
    os.chdir(OUT_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/"
        print(f"Serving at {url}  (Ctrl+C to stop)")
        webbrowser.open(url)
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Build static site into _site/")
    parser.add_argument("--serve", action="store_true", help="Build, then serve _site/ locally and open in browser")
    parser.add_argument("--port", type=int, default=8000, help="Port for --serve (default: 8000)")
    args = parser.parse_args()

    print("Building site -> _site/")
    env = get_jinja_env()
    run_build(env)
    print("Done.")

    if args.serve:
        serve(args.port)


if __name__ == "__main__":
    main()
