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
