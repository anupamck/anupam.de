# anupam.de

Welcome to my personal site! It's a collection of my written creations, projects, and a bit about what I'm doing now.

## How this site evolved

The site began in 2021 as a learning project when I moved into web development. I wanted a single place for my work and chose to build it from scratch with vanilla HTML and CSS — no frameworks, minimal design. 

Over time, editing every page by hand became cumbersome. The site was refactored to a static site generator: content now lives in Markdown and YAML, and a small Python build (Jinja2 + Markdown) generates the HTML. This was done in one morning using Cursor. 

---

# Site refactor: static generator

The site was refactored from hand-written HTML to a Python static site generator. Editing happens  in Markdown and YAML; Jinja2 templates and Python scripts produce HTML files from these and deploy them to a folder. 

## How it works

- **Content** (`site/`) – Markdown (with optional YAML front matter) and YAML data files. This is the only place to edit.
- **Templates** (`templates/`) – Jinja2 base layout and page templates; `base_path` keeps nav and assets correct at any depth.
- **Build** – `python build.py` copies static assets into `_site/`, then renders each page. `python build.py --serve` builds and serves locally.

## What is generated vs legacy

**Generated from site/templates:**

- **Homepage** – `site/now.yaml` + `templates/now.html` → `_site/index.html`
- **About** – `site/about.md` → `_site/about/about.html`
- **Projects** – `site/projects.yaml` → `_site/projects/projects.html`
- **Writing index** – `site/writing.yaml` → `_site/writing/writing.html`
- **Essays** – each `site/essays/*.md` → `_site/writing/essays/<slug>.html`
- **Poetry** – each `site/poetry/*.md` → `_site/writing/poetry/<slug>.html`
- **Short stories** – each `site/shortstories/*.md` → `_site/writing/shortstories/<slug>.html`
- **Older blogs (Pom-Musings, Sculptures in Sand)** – `site/poMusing/*.md` and `site/sculpturesInSand/*.md` → `_site/writing/{poMusing,sculpturesInSand}/<slug>.html`

**Still legacy (HTML copied as static):**

- **Descriptify** – `projects/descriptify/` is copied as static HTML and linked from the projects page.

Non-Markdown assets referenced from content (images, audio) live in top-level `images/` and `audio/` folders and are copied into `_site/` as static sources.

## Quick reference

| Task                  | Command                           |
| --------------------- | --------------------------------- |
| Build                 | `python build.py`                 |
| Build + local preview | `python build.py --serve`         |
| Install               | `pip install -r requirements.txt` |


