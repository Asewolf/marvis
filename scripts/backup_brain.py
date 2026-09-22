"""Nightly backup of your memory directory, rules and config to a git repo.

A mature memory directory is genuinely hard to reconstruct and usually lives on one disk.
This copies the parts that matter into a git repo, scans for leaked credentials, and
commits. Point it at a PRIVATE remote.

    python backup_brain.py --dry-run     see what it would stage, commit nothing
    python backup_brain.py               stage, scan, commit, push

Schedule it nightly. On Windows use Task Scheduler, on macOS or Linux use cron.
"""
import os, re, shutil, subprocess, sys, time
from datetime import datetime

# ---------------------------------------------------------------- configure
HOME = os.path.expanduser("~")
REPO = os.path.join(HOME, "brain-backup")          # your private repo
LOG = os.path.join(REPO, "backup.log")

# (source directory, destination inside the repo)
INCLUDE = [
    (os.path.join(HOME, ".claude", "projects"), "claude/projects"),
    (os.path.join(HOME, ".claude", "rules"),    "claude/rules"),
    (os.path.join(HOME, ".claude", "skills"),   "claude/skills"),
    # add your own work directories here
]
FILES = [
    (os.path.join(HOME, "CLAUDE.md"),                      "claude/CLAUDE.md"),
    (os.path.join(HOME, ".claude", "settings.json"),       "claude/settings.json"),
]

# Never leaves the machine.
SKIP_NAMES = re.compile(
    r"(config\.json$|token\.json$|credential|secret|password|cookies|"
    r"\.env$|_profile$|browser_state)", re.I)
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
SKIP_EXT = {".pyc", ".pyo", ".log", ".tmp", ".jsonl"}   # .jsonl = raw transcripts, large
MAX_FILE_MB = 95                                        # GitHub rejects over 100


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {msg}"
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    # A scheduled task may have no stdout. A bare print() would raise and kill the run.
    if sys.stdout is not None:
        print(line)


def wanted(path, name):
    if SKIP_NAMES.search(name) or os.path.splitext(name)[1].lower() in SKIP_EXT:
        return False
    try:
        return os.path.getsize(path) <= MAX_FILE_MB * 1024 * 1024
    except OSError:
        return False


def sync(src, dst_rel, stats):
    if not os.path.isdir(src):
        return
    dst = os.path.join(REPO, dst_rel)
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not SKIP_NAMES.search(d)]
        rel = os.path.relpath(root, src)
        out = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(out, exist_ok=True)
        for fn in files:
            s = os.path.join(root, fn)
            if not wanted(s, fn):
                stats["skipped"] += 1
                continue
            d = os.path.join(out, fn)
            try:
                if (not os.path.exists(d)
                        or os.path.getmtime(s) > os.path.getmtime(d)
                        or os.path.getsize(s) != os.path.getsize(d)):
                    shutil.copy2(s, d)
                    stats["copied"] += 1
                stats["total"] += 1
                stats["bytes"] += os.path.getsize(s)
            except Exception as e:
                log(f"  copy failed {s}: {e}")


def secret_scan():
    """Last line of defence. Nothing commits if this finds anything."""
    pat = re.compile(r"(sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_\-]{30,}|"
                     r"ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9\-]{20,}|"
                     r"-----BEGIN [A-Z ]*PRIVATE KEY-----)")
    text_ext = {".md", ".txt", ".json", ".py", ".js", ".ts", ".html", ".yml", ".yaml",
                ".toml", ".sh", ".env"}
    hits = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            if os.path.splitext(fn)[1].lower() not in text_ext:
                continue
            p = os.path.join(root, fn)
            try:
                m = pat.search(open(p, encoding="utf-8", errors="ignore").read())
            except Exception:
                continue
            if m:
                hits.append((os.path.relpath(p, REPO), m.group(0)[:12] + "..."))
    return hits


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True)


def main(dry=False):
    os.makedirs(REPO, exist_ok=True)
    stats = {"copied": 0, "total": 0, "skipped": 0, "bytes": 0}

    for src, dst in INCLUDE:
        sync(src, dst, stats)
    for src, dst in FILES:
        if os.path.isfile(src):
            d = os.path.join(REPO, dst)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(src, d)
            stats["total"] += 1

    gi = os.path.join(REPO, ".gitignore")
    if not os.path.exists(gi):
        open(gi, "w").write("*config.json\n*token.json\n*credential*\n*secret*\n"
                            "*.env\n*cookies*\n*_profile/\n__pycache__/\n*.pyc\n"
                            "*.log\n*.jsonl\n")

    leaks = secret_scan()
    if leaks:
        log("ABORTED. Possible credentials found, nothing was committed:")
        for f, s in leaks:
            log(f"   {f}  ->  {s}")
        return 2

    log(f"staged {stats['total']} files, {stats['copied']} changed, "
        f"{stats['bytes'] / 1048576:.1f} MB, {stats['skipped']} filtered out")
    if dry:
        log("dry run, nothing committed")
        return 0

    if not os.path.isdir(os.path.join(REPO, ".git")):
        git("init", "-b", "main")
        log("initialised repo. Add a PRIVATE remote: git remote add origin <url>")

    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        log("no changes since last run")
        return 0

    msg = f"backup {datetime.now():%Y-%m-%d %H:%M}"
    git("commit", "-m", msg)
    log(f"committed: {msg}")

    if git("remote", "get-url", "origin").returncode == 0:
        p = git("push", "origin", "main")
        log("pushed" if p.returncode == 0 else f"push failed: {p.stderr.strip()[:200]}")
    else:
        log("no remote configured, commit is local only")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main("--dry-run" in sys.argv))
    except Exception as e:
        log(f"FAILED: {type(e).__name__}: {e}")
        sys.exit(1)
