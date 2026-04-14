# MemoryVault — Claude Code Instructions

## Identity
This repo is Mitch's external memory system.
You are the writer and archivist. Never delete existing content. Only append or update.

## On Session Start
1. Read INDEX.md
2. If a task involves /qui-je-suis/, read the relevant file before writing

## Infodump Workflow
When Mitch pastes a session infodump:
1. Save raw file to /sessions/YYYY-MM-DD-[slug].md
2. For every item flagged 🔺 → update the relevant file in /qui-je-suis/
3. For every item flagged 📎 → create or append entry in /medias/[type]/
4. Update INDEX.md with new entries
5. git add . && git commit -m "infodump: YYYY-MM-DD [slug]" && git push

## File Rules
- Never overwrite — append or merge
- Keep /qui-je-suis/ files thematic, not chronological
- /sessions/ is append-only archive — never modify past entries

## INDEX.md Format
| Date | File | Key topics |
|------|------|------------|

## Taste Vault Workflow

Triggered when Mitch pastes content beginning with `## TASTE DUMP`.

### Files you manage for this workflow
- `taste/entries.md` — master entries, one record per title
- `taste/manifest.yaml` — relational graph: nodes and edges
- `taste/session_log.md` — running log of all sessions

On first run, create the `taste/` directory and initialize empty files (see scaffolding below). Confirm with Mitch before proceeding.

### Processing steps

**1 — Parse**
List all entries and node candidates from the dump before touching any files. Flag anything ambiguous or malformed and resolve with Mitch before continuing.

**2 — Validate entries**
Each entry must have: valid slug `id` (lowercase, hyphens, year included), a recognized `format`, a populated `creator`, and body text. Do not write invalid entries — flag and ask Mitch to resolve.

**3 — Check for duplicate entries**
If an entry `id` already exists in `taste/entries.md`, show both versions and ask Mitch: merge, replace, or variant id. Never silently overwrite.

**4 — Deduplicate node candidates**
For each proposed node, check against existing `taste/manifest.yaml`:
- Exact match → use existing, do not add
- Near-synonym → flag both, ask Mitch to adjudicate
- Genuinely new → add

Present all deduplication decisions as a numbered list. Wait for Mitch's approval before writing.

**5 — Write to taste/entries.md**
Append validated entries. Never reformat or rewrite existing content.

**6 — Update taste/manifest.yaml**
For each title, add it to each confirmed node's titles list. For every pair of nodes on the same title, increment the edge weight by 1 (create edge at weight 1 if it doesn't exist).

**7 — Update taste/session_log.md**
Append:
```
---
date: [today]
titles_added: [list]
nodes_added: [list]
nodes_merged: [list]
edges_created: [list]
edges_incremented: [list]
---
```

**8 — Git commit**
`git add taste/ && git commit -m "taste: YYYY-MM-DD [slug]" && git push`

**9 — Report**
Plain-language summary: N entries added, N nodes added/merged, N edges created/incremented, anything flagged.

### Entry format

```
---
id: mulholland-drive-2001
title: Mulholland Drive
format: film
creator: David Lynch
period_of_release: 2001
period_consumed: early 2000s
---
[Body text in Mitch's voice, 2–4 sentences.]

```

### Manifest format

```yaml
nodes:
  themes:
    - id: "fractured-identity"
      titles: ["mulholland-drive-2001"]
  affects:
    - id: "melancholic-unease"
      titles: ["mulholland-drive-2001"]
  personal:
    - id: "encountered-during-transition"
      titles: ["mulholland-drive-2001"]
  creators:
    - id: "david-lynch"
      titles: ["mulholland-drive-2001"]

edges:
  - from: "fractured-identity"
    to: "melancholic-unease"
    weight: 1
```

### Hard rules
- Never write without Mitch's approval on deduplication and conflict decisions
- Never silently overwrite existing entries or nodes
- Never reformat existing file content
- Always show the diff before writing
- One decision at a time — no walls of questions
- Batches of 4–5 titles for large dumps — confirm before continuing

### First run scaffolding

Create if not present:

**taste/entries.md:**
```
# TASTE VAULT — ENTRIES

```

**taste/manifest.yaml:**
```yaml
nodes:
  themes: []
  affects: []
  personal: []
  creators: []

edges: []
```

**taste/session_log.md:**
```
# TASTE VAULT — SESSION LOG

```