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

Push it. The `build index` Action regenerates `index.json` in about five seconds, and the page picks it up on next load. No deploy needed.

Optional frontmatter:

- `weight: 1-4` forces the heatmap level for that day when the writing is short but the work was heavy.

## How the colours work

Green intensity is relative to the longest entry in the repo, not a fixed word count: `level = ceil(4 * words / max_words)`. The longest entry is always the brightest cell, and every earlier cell is re-graded whenever a new longest entry lands.

## Files

- `entries/` one markdown file per day, the source of truth
- `index.json` generated, do not edit by hand
- `scripts/build_index.py` the generator, Python standard library only
