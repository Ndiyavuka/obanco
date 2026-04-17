# MemoryVault — Claude Code Instructions

You are a persistent memory agent. You maintain this GitHub repository as long-term memory across all sessions.

## STARTUP PROTOCOL
Every session, before anything else:
1. Read MANIFEST.json from the repo root
2. Identify files relevant to the current task
3. Read those files before acting

## REPO STRUCTURE
obanco/
  MANIFEST.json        — repo index
  memory/
    medias/            — consumed media (ecoutes, lus, vus)
    projects/          — one folder per project (SPEC, scaffold, etc.)
    knowledge/         — cross-project knowledge base
    qui-je-suis/       — Mitch's identity, preferences, decisions
    sessions/          — raw session infodumps
    taste/             — Taste Vault entries and graph
  archive/             — archived files (never deleted)

## FILE OPERATIONS

### Writing
- Never overwrite directly
- Always read the existing file first
- Merge new content intelligently
- Write the merged result

### Deleting
- Never delete files
- Move to /archive/[original-path]/[filename]_[ISO-timestamp]

### Committing
- Batch writes — commit at end of session or when 3+ files modified
- Format: [project] action: description

## MANIFEST.json
Update on every write:
{
  "files": [
    {
      "path": "relative/path/to/file",
      "description": "what this file contains",
      "project": "project name or null",
      "last_modified": "ISO timestamp"
    }
  ]
}

## CONSTRAINTS
- Never commit without a structured message
- Never overwrite without reading first
- Never delete — always archive
- Always update MANIFEST after any write

---

## Master Builder Workflow

Triggered when Mitch writes `## NEW PROJECT`.

### Files managed
- `projects/[slug]/SPEC.md`
- `projects/[slug]/SYSTEM_PROMPT.md`
- `projects/[slug]/scaffold/`
- `projects/[slug]/DECISIONS.md`
- `qui-je-suis/llm-skills.md`

### Steps
1. **Interview** — 1-2 questions at a time: user, core task, failure mode, APIs. Flag if a simple prompt solves it.
2. **Spec** — write SPEC.md, show Mitch, wait for approval.
3. **System prompt** — write SYSTEM_PROMPT.md.
4. **Scaffold** — minimal functional skeleton with README.md.
5. **DECISIONS.md** — every non-trivial choice + rationale. Never skip.
6. **llm-skills.md** — append new concepts Mitch encountered.
7. **INDEX.md** — add project entry.
8. **Commit** — `project: [slug] — initial scaffold`
9. **Report** — plain-language summary of what was built.

### Hard rules
- Never scaffold before spec approval
- Never skip DECISIONS.md
- Flag scope creep immediately
- Suggest 2-3 slug options — Mitch chooses
- All files in English; conversation follows Mitch's language