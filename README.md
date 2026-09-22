# Marvis

A memory and working-habits system for Claude Code.

Claude Code forgets you between sessions. Every conversation starts from zero, so you
re-explain your stack, your preferences, and the same correction you made last Tuesday.
Marvis is the scaffolding that fixes that: a file layout, a few conventions, and a backup
script, so the assistant accumulates instead of resetting.

There is no application to run. It is a structure plus the discipline to use it.

## What it actually is

**One fact per file.** Not one big notes document. Hundreds of small files with
frontmatter, each holding a single thing that stays true. Small files can be added,
corrected and deleted without touching anything else.

**An index that always loads.** `MEMORY.md` is one line per memory, read at the start of
every session. The assistant scans the index, then opens only the files the task needs.

**Corrections become permanent.** This is the core move. When you correct the assistant,
that correction gets written to a `feedback_*` file along with the reason. Next session it
is already known. This is the mechanism that makes the thing improve instead of repeating
itself.

**Rules that load by topic.** Standing instructions scoped to a subject, in
`.claude/rules/`. Security rules load for client work, writing rules load for anything with
your name on it.

## Install

```bash
git clone https://github.com/<you>/marvis
```

1. Copy `memory/` into `~/.claude/projects/<your-project-dir>/memory/`
2. Copy `.claude/rules/` into `~/.claude/rules/`
3. Copy `CLAUDE.md` to your home or project root and fill it in
4. Read `docs/memory-system.md`
5. Write memories as you go, or ask the assistant to

On day one it knows nothing. That is correct. It is supposed to start empty.

## Skills

`.claude/skills/` holds three skills: reading links that sit behind a login, grading a post
before it ships, and pay-as-you-go image and video generation. The rest of the working set
comes from other authors, and [`docs/skills.md`](docs/skills.md) lists every one of them
with its author, license and install command.

## Start here

- [`docs/memory-system.md`](docs/memory-system.md) — the design, and why one fact per file
- [`docs/feedback-loop.md`](docs/feedback-loop.md) — turning corrections into permanent behaviour
- [`docs/getting-started.md`](docs/getting-started.md) — the first week
- [`scripts/backup_brain.py`](scripts/backup_brain.py) — nightly backup with a secret scanner
- [`docs/skills.md`](docs/skills.md) — the skill set, who wrote each one, how to install it
- [`docs/browser-automation.md`](docs/browser-automation.md) — reading links behind a login, and filling forms

## A warning worth reading

A mature memory directory is a detailed profile of you. Addresses, employers, medical
details, case numbers, whatever you have been working on.

**Back it up to a private repo. Never a public one.** The backup script excludes key files
by name and aborts the commit if it finds anything matching a live credential, but the real
protection is that the repo is private.

MIT licensed. Fork it, gut it, make it yours.
