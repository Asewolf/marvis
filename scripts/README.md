# scripts

## backup_brain.py

Copies your memory directory, rules and config into a git repo, scans for leaked
credentials, commits, and pushes.

**Configure the paths at the top of the file first.** `REPO` is where the backup repo
lives, `INCLUDE` is what gets copied.

```bash
python backup_brain.py --dry-run     # see what it would stage
python backup_brain.py               # stage, scan, commit, push
```

### The remote must be private

A memory directory after a few months is a detailed profile of you. The script excludes
files by name and aborts on anything matching a live credential pattern, but those are
backstops. The actual protection is the repo being private.

### What it excludes

Config and token files, anything matching credential or secret or cookies, browser
profiles, caches, and `.jsonl` transcripts. Transcripts are large and the memory files are
already their distillation.

### Scheduling

**Windows**

```
schtasks /Create /TN BrainBackup /SC DAILY /ST 03:17 /F ^
  /TR "'C:\path\to\pythonw.exe' 'C:\path\to\backup_brain.py'"
```

Use `pythonw.exe`, not `python.exe`, so no console window appears. The script guards
against a missing stdout for exactly this reason.

**macOS / Linux**

```
17 3 * * *  /usr/bin/python3 /path/to/backup_brain.py
```
