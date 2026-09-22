# CLAUDE.md

Project instructions. Loads with every session in this directory. Replace everything here.

## Response style

- Short and direct. No preamble, no "Great question", no summary of what you just did
- Code comments explain the why, not the what
- End when done. No "let me know if" sign-offs

## Behavioural rules

- Do what is asked. Nothing more
- Prefer editing an existing file over creating a new one
- Never create documentation unless asked
- Always read a file before editing it
- Never modify a test to make it pass. Fix the code or ask
- Verify state before listing what is left to do

## Stack

Replace with yours. Language, framework, package manager, test runner, the commands you
actually type.

```
Build:  <command>
Test:   <command>
Lint:   <command>
Run:    <command>
```

## Paths that matter

```
Source:  <path>
Tests:   <path>
Config:  <path>
```

## Never

- Commit secrets, credentials or .env files
- Push to the default branch without asking
- Skip hooks or bypass signing

## Memory

Persistent memory lives in `~/.claude/projects/<this-project>/memory/`, indexed by
`MEMORY.md`, which loads automatically. See `docs/memory-system.md`.
