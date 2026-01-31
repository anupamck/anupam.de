# anupam.de

Welcome to my personal site! It's a collection of my written creations, projects, and a bit about what I'm doing now.

## How this site evolved

The site began in 2021 as a learning project when I moved into web development. I wanted a single place for my work and chose to build it from scratch with vanilla HTML and CSS — no frameworks, minimal design. 

Over time, editing every page by hand became cumbersome. The site was refactored to a static site generator: content now lives in Markdown and YAML, and a small Python build (Jinja2 + Markdown) generates the HTML. This was done in one morning using Cursor. 

---

# Site refactor: static generator

The site was refactored from hand-written HTML to a Python static site generator. Editing happens  in Markdown and YAML; Jinja2 templates and Python scripts produce HTML files from these and deploy them to a folder. 

## How it works

- **Content** (`content/`) – Markdown (with optional YAML front matter) and YAML data files.
- **Templates** (`templates/`) – Jinja2 base layout and page templates; `base_path` keeps nav and assets correct at any depth.
- **Build** – `python build.py` copies static assets into `_site/`, then renders each page. `python build.py --serve` builds and serves locally.

## What is generated vs legacy

**Generated from content/templates:**

- **Homepage** – `content/now.yaml` + `templates/now.html` → `_site/index.html`
- **About** – `content/about.md` → `_site/about/about.html`
- **Projects** – `content/projects.yaml` → `_site/projects/projects.html`
- **Writing index** – `content/writing.yaml` → `_site/writing/writing.html`
- **Essays** – each `content/essays/*.md` → `_site/writing/essays/<slug>.html`
- **Poetry (migrated)** – each `content/poetry/*.md` → `_site/writing/poetry/<slug>.html` (only `growingUp` so far)

**Still legacy (HTML copied as static):**

- **Poetry** – Most poems are still in `writing/poetry/*.html` and are **copied** into `_site/writing/poetry/`. Only items with a matching `content/poetry/*.md` are built; the rest stay as legacy HTML.
- **Short stories** – `writing/shortstories/*.html` are copied as-is; no Markdown migration yet.
- **Descriptify** – `projects/descriptify/` is copied as static HTML and linked from the projects page.

## Quick reference

| Task                  | Command                           |
| --------------------- | --------------------------------- |
| Build                 | `python build.py`                 |
| Build + local preview | `python build.py --serve`         |
| Install               | `pip install -r requirements.txt` |


