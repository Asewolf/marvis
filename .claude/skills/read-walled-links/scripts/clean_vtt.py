#!/usr/bin/env python3
"""Clean a WebVTT subtitle file (yt-dlp --write-auto-sub output) into plain deduped text.

Usage:
  clean_vtt.py <in.vtt> [out.txt]   # out.txt omitted -> UTF-8 stdout
  clean_vtt.py -                    # read VTT from stdin
  clean_vtt.py --selftest           # runnable check, exits 0 if clean() works

Output is always UTF-8 (Windows console is cp1252 — redirect to a file, don't print emoji).
"""
import re
import sys

HEADER_PREFIXES = ("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE", "REGION")


def clean(vtt_text):
    lines = []
    for raw in vtt_text.splitlines():
        line = re.sub(r"<[^>]+>", "", raw).strip()  # <c>, <00:00:00.000> inline tags
        if (not line
                or line.startswith(HEADER_PREFIXES)
                or "-->" in line
                or line.isdigit()):  # cue numbers
            continue
        # ponytail: consecutive-dupe removal only; auto-subs roll captions so each
        # line appears twice — this catches that. Fancier overlap-merge if ever needed.
        if lines and line == lines[-1]:
            continue
        lines.append(line)
    return "\n".join(lines)


def selftest():
    sample = """WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000
<c>hello world</c>

00:00:02.000 --> 00:00:04.000
hello world

00:00:02.000 --> 00:00:04.000
this is <00:00:03.000>the second line

2
00:00:04.000 --> 00:00:06.000
final line
"""
    out = clean(sample)
    assert out == "hello world\nthis is the second line\nfinal line", repr(out)
    print("selftest OK")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
        sys.exit(0)
    if sys.argv[1] == "-":
        text = sys.stdin.read()
    else:
        with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
            text = f.read()
    out = clean(text) + "\n"
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.buffer.write(out.encode("utf-8"))
