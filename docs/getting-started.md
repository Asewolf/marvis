# Getting started

## Day one

Copy the folders, then write four files. Do not try to write down everything you know.

1. **user_*** - one file about you. Role, stack, hardware, how you like to be talked to.
2. **project_*** - one file about what you are working on right now.
3. **MEMORY.md** - the index, one line each pointing at those two.
4. **CLAUDE.md** - copy the template, fill in your paths and response style.

That is enough to start. The system fills itself in from here.

## The first week

Every time you catch yourself explaining something for the second time, stop and write it
down. That reflex is the whole practice. The second explanation is the signal.

Every time you correct the assistant, ask it to write a `feedback_*` file with the reason.
It can do this itself. "Save that as a feedback memory" is usually all it takes.

Expect twenty or thirty files by the end of the week, and expect half of them to be
feedback.

## The first month

**Add a rule when a subject earns its own standards.** Once you have four memories about
deployment, they probably want to be `.claude/rules/deployment.md` instead, loaded
whenever that subject comes up.

**Prune.** Once a month, read the index and delete what is no longer true. A finished
project is not a memory, it is history. Ten minutes, and it is the difference between a
system and a junk drawer.

**Set up the backup.** `scripts/backup_brain.py`, nightly. By month two this directory is
genuinely hard to reconstruct and it lives on one disk.

## Signs it is working

- You stop opening conversations by explaining your setup
- Corrections stop repeating
- It starts referring to decisions you made weeks ago
- You get slightly uneasy about how much it knows, which is the correct reaction, and the
  reason the backup repo is private
