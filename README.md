# today

Daily work log for [jagdishverma.com/today](https://jagdishverma.com/today).

## Add an entry

Create `entries/YYYY-MM-DD.md` (GitHub web UI, the GitHub app, or git) with:

```markdown
---
title: What the day was about
tags: [threejs, paper-plane]
---

Body in normal markdown. Headings, lists, tables and code all render.
```

Push it. The `build index` Action regenerates `index.json` in about five seconds, and the page picks it up on the next load. No deploy needed.

Frontmatter is optional. A file with no frontmatter still publishes: the title falls back to the date and the whole file renders as the body. Tags are optional too.

## How the page reads

- The latest entry opens by default, full width of the reading column.
- Previous and next links skip days you did not write.
- The calendar fills a day in the accent colour when it has an entry. Length does not matter: a 20 word day looks exactly like a 500 word day.
- The address bar stays at `/today`. The day you opened is kept in history, so back and forward walk through entries without a date appearing in the url. Older `?d=YYYY-MM-DD` links still open the day they name, then clean the address bar. Reloading shows the latest entry again.

## Files

- `entries/` one markdown file per day, the source of truth
- `index.json` generated, do not edit by hand
- `scripts/build_index.py` the generator, Python standard library only
