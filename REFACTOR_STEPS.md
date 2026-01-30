# Refactor plan: Python static site generator

## Overview

Content moves into **Markdown** and **JSON data files**. A small Python script (Jinja2 + Markdown) renders them into the same HTML structure you have today. Output goes to `_site/`; deploy that folder. Your existing `style.css` and images are copied as-is.

---

## Step 1: Set up generator structure ✓

- `content/` – Markdown files and data (JSON/YAML)
- `templates/` – Jinja2 layout and page templates
- `_site/` – Generated HTML and copied assets (gitignored or deployed)
- `build.py` – Build script
- `requirements.txt` – markdown, jinja2, pyyaml

---

## Step 2: Extract base layout and add dependencies

- One **base layout** template with: `<head>`, CSS link (path from `base_path`), nav sidebar, wrapper, `{% block main %}` for main content.
- Nav links use `base_path` so they work from any page depth.
- Install deps: `pip install -r requirements.txt`

---

## Step 3: Implement build.py

- Load base layout, render each page with the right `base_path`.
- Copy `style.css` and `images/` into `_site/`.
- Helper: `base_path` from output path (e.g. `writing/essays/foo.html` → `../..`).

---

## Step 4: Data files

- `content/updates.json` – "Last few updates" (date, title, url, category).
- `content/projects.json` – Projects (title, dateRange, url, image, description).
- Optional: `content/writing_index.json` or derive from Markdown front matter.

---

## Step 5: Migrate About page

- `content/about.md` with body text.
- Page template that extends base and renders Markdown in `<section class="main">`.
- Build outputs `_site/about/about.html`. Verify design matches current about.

---

## Step 6: Migrate essays, poetry, short stories

- One `.md` per piece in e.g. `content/essays/`, `content/poetry/`, `content/shortstories/`.
- Front matter: `title`, `date` (and optional `category`).
- Build discovers all `.md` in those dirs, renders each with the article layout (same structure as current essay/poetry pages).
- Copy any per-project assets (e.g. descriptify) or keep under `static/` and copy.

---

## Step 7: Writing index and Projects page

- **Writing index**: Build script collects all essays/poetry/short stories (from front matter or a manifest), groups by category, sorts by date; one template renders `writing/writing.html` with the dated rows.
- **Projects page**: Template loops over `content/projects.json`, outputs `_site/projects/projects.html` with current `section.project` markup.

---

## Step 8: Index (now) page

- "What I am doing now" → `content/now.md` (or embedded in template).
- "Last few updates" → template loops over `content/updates.json`.
- Build outputs `_site/index.html`. Optionally keep "Updated on" date in data or template.

---

## Step 9: Descriptify and cleanup

- Either copy `projects/descriptify/` into `_site/projects/descriptify/` during build, or leave as static and document.
- Remove or archive old hand-written HTML from repo (after you’re happy with `_site/`).
- Document in README: how to run `python build.py`, what to deploy (`_site/`).

---

## Order of work

We do 1 → 2 → 3, then 4 (data), then 5 (about) so you have one full page working. Then 6 (content migration), 7 (indexes), 8 (now page), 9 (cleanup and docs).
