# The memory system

## The problem

Claude Code starts every session blank. You re-explain your stack, your constraints, and
the correction you already made twice. The assistant is capable and amnesiac, and the
amnesia is what makes it feel like a tool instead of a colleague.

The obvious fix is a big notes file. That fails at scale. A 4,000 line
`everything-about-me.md` either burns your whole context window or gets skimmed. And you
cannot correct one line of it without rereading the rest.

## The design

**One fact per file.**

```
memory/
  MEMORY.md                        the index, loaded every session
  user_timezone.md
  project_acme_migration.md
  feedback_no_em_dashes.md
  reference_staging_login.md
```

Each file holds a single thing that stays true, with frontmatter:

```markdown
---
name: no-em-dashes
description: Never use em dashes in anything I put my name on
metadata:
  type: feedback
---

No em dashes in prose. Not in posts, emails, docs, or code comments.

**Why:** They read as AI-written and I have to edit every one out by hand.

**How to apply:** Use a comma, a full stop, or restructure. Applies to en dashes and
double hyphens too. Normal hyphens in compounds are fine.

Related: [[writing-voice]]
```

**Four types, and the type tells you what belongs there:**

| Type | Holds |
|---|---|
| `user` | Who you are. Role, expertise, hardware, preferences |
| `feedback` | How to work with you. Corrections, and confirmed approaches |
| `project` | Ongoing work, goals, constraints not derivable from the code |
| `reference` | Pointers outward. URLs, dashboards, tickets, where credentials live |

**MEMORY.md is the index, and it is the only file that always loads.** One line per
memory, with a hook that tells the assistant whether to open it:

```markdown
## Read every session
- [Active client work](project_client_work.md) - check before any outreach
- **[Never deploy on Fridays](feedback_no_friday_deploys.md)** - hard rule, ask why

## Reference
- [Staging login](reference_staging_login.md) - where the credentials live, not the values
```

The index is a table of contents, never the content. If a memory's text is sitting in
MEMORY.md, the system is already breaking.

## Why one fact per file

**Correcting is cheap.** A fact turns out wrong, you delete one file. In a monolith you
are editing a paragraph inside a wall of text and hoping nothing else referenced it.

**Context stays small.** The index is a few hundred lines. Individual memories load only
when relevant. A monolith is all or nothing.

**Links make a graph.** A `[[wiki-link]]` in the body connects related facts. A link to a
file that does not exist yet is fine and useful: it marks something worth writing later.

**Conflicts surface.** Two files saying different things about the same subject is
visible. Two contradictory sentences 200 lines apart in one document is not.

## What does not belong in memory

- **Anything the repo already says.** Code structure, past fixes, git history, your
  CLAUDE.md. If reading the code answers it, it is not a memory.
- **Anything true only for one conversation.** "We are debugging the auth bug" is not a
  memory, it is a sentence.
- **Relative dates.** "Last Tuesday" is meaningless in three weeks. Write the date.
- **Secrets.** Write where a credential lives, never the credential.

## Maintenance

Memories go stale. A file that names a flag, a file path, or a person should be verified
before you act on it, not trusted because it is written down. An old memory describes what
was true when it was written, which is not the same as what is true.

Delete aggressively. A wrong memory is worse than a missing one, because the assistant
will act on it with confidence.
