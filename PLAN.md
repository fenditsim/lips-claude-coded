# LinkedIn Post Archive — Claude Code Build Plan

## Goal
Build a local, static website to **search and filter LinkedIn posts** stored as Markdown files in this repository. No frameworks, no build tools beyond a single Python script — just `build.py`, `index.html`, and `posts.js`.

---

## Project Structure

```
/
├── posts/              ← your .md files live here
│   └── ai-ai-bias.md
├── build.py            ← parses .md files → generates posts.js
├── posts.js            ← auto-generated data file (do not edit by hand)
└── index.html          ← the website (plain HTML/CSS/JS)
```

---

## Markdown File Format

Each `.md` file has YAML frontmatter followed by the post body:

```yaml
---
title: "Laurito et al. (2025)"
source_title: "AI–AI bias: Large language models favor AI-generated content"
source_url: "https://doi.org/10.1073/pnas.2415697122"
linkedin_url: "https://www.linkedin.com/posts/..."
keywords:
- AIBias
- AgenticAI
- MachineLearning
---

Post body text here...
```

**Fields:**
- `title` — short label (usually author/year)
- `source_title` — the paper or article being discussed
- `source_url` — DOI or link to the source material
- `linkedin_url` — link to the live LinkedIn post
- `keywords` — array of hashtags/topics (no `#` prefix)

---

## Component 1: `build.py`

A Python script that scans `./posts/*.md`, parses frontmatter and body, then outputs a `posts.js` file.

### Requirements
- Parse YAML frontmatter (no external libraries — use regex or manual line parsing)
- Extract: `title`, `source_title`, `source_url`, `linkedin_url`, `keywords[]`, `body`
- Generate a `snippet` from the first ~220 characters of the body
- Output as `const POSTS = [ ... ];` so `index.html` can load it with a `<script>` tag
- CLI usage: `python build.py --dir ./posts --out posts.js`
- Print a summary: `✓ Built N posts → posts.js`

---

## Component 2: `index.html`

A single-file website. All CSS and JS are inline — no external files except Google Fonts and `posts.js`.

### Layout
```
┌─────────────────────────────────────────────────────┐
│  HEADER: wordmark + post count                      │
├──────────────┬──────────────────────────────────────┤
│  SIDEBAR     │  MAIN                                │
│              │                                      │
│  [ Search ]  │  "Showing N of M posts"              │
│              │                                      │
│  Keywords:   │  ┌─ Card ─────────────────────────┐  │
│  [tag] [tag] │  │ Title (Playfair serif)          │  │
│  [tag] [tag] │  │ Source title (italic)           │  │
│              │  │ Snippet text                    │  │
│  [Clear]     │  │ [tag] [tag]    [↗ LinkedIn]     │  │
│              │  └─────────────────────────────────┘  │
│              │  ┌─ Card ─────────────────────────┐  │
│              │  │ ...                             │  │
└──────────────┴──────────────────────────────────────┘
```

### Functionality
- **Full-text search** across title, source_title, body, and keywords — with highlighted matches using `<mark>` tags
- **Keyword filter pills** in the sidebar — multi-select (AND logic: post must match ALL active tags)
- **Clear filters** button resets both search and tag filters
- **Status bar** shows "Showing N of M — filtered by X"
- **Click card body → modal** with full post body, all tags, LinkedIn link, and paper link
- **Keyboard**: `Escape` closes modal
- **Empty state** if no posts match

### Design
- Dark theme (`#0d0e0f` background)
- Typography: `Playfair Display` (serif, titles) + `DM Mono` (labels/tags) + `DM Sans` (body)
- Accent color: warm gold `#c9a84c`
- Cards have a subtle left-border reveal animation on hover
- Cards fade in with staggered `animation-delay` on render
- Responsive: sidebar stacks above cards on mobile

---

## Build & Run

```bash
# Step 1: generate data file from your .md posts
python build.py --dir ./posts --out posts.js

# Step 2: open in browser (no server needed)
open index.html
```

Re-run `build.py` whenever you add or edit a `.md` file.

---

## Progress Checklist

- [ ] `build.py` — parses all `.md` files correctly
- [ ] `build.py` — generates valid `posts.js`
- [ ] `index.html` — loads and displays all posts
- [ ] Search works with highlighted matches
- [ ] Keyword filter pills work (multi-select, AND logic)
- [ ] Clear button resets all filters
- [ ] Status bar shows correct count
- [ ] Modal opens on card click with full body text
- [ ] Modal closes on Escape and overlay click
- [ ] LinkedIn and paper links open in new tab
- [ ] Empty state shows when no results
- [ ] Mobile layout is usable
- [ ] Tested with multiple `.md` files

---

## Notes for Claude Code

- Do **not** use any npm packages or bundlers — the site must work by opening `index.html` directly in a browser
- `posts.js` is the only data source — `index.html` should never try to read `.md` files directly (browsers can't access the filesystem)
- The `build.py` YAML parser should handle both string values and list values without importing `pyyaml`
- Keep all CSS and JS inline in `index.html` — one file, fully self-contained
