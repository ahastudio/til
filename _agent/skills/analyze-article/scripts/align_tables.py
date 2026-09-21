#!/usr/bin/env python3
"""Pad markdown table cells so the pipes line up, counting CJK as two columns.

writing-guidelines.md requires aligned tables and check_format.py enforces it.
This fixes them. Fenced code blocks are left alone.

Usage:
    python3 _agent/skills/analyze-article/scripts/align_tables.py <file.md> [...]
"""
import io
import sys
import unicodedata


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s, target):
    return s + " " * (target - width(s))


def is_separator(row):
    return all(c.strip() and set(c.strip()) <= set("-:") for c in row)


def render(rows):
    n = max(len(r) for r in rows)
    if any(len(r) != n for r in rows) or len(rows) < 2:
        return None
    widths = [0] * n
    for r in rows:
        if is_separator(r):
            continue
        for i, c in enumerate(r):
            widths[i] = max(widths[i], width(c.strip()) + 2)
    widths = [max(w, 5) for w in widths]
    out = []
    for r in rows:
        if is_separator(r):
            out.append("|" + "|".join(" " + "-" * (w - 2) + " " for w in widths) + "|")
        else:
            out.append(
                "|" + "|".join(pad(" " + c.strip(), widths[i]) for i, c in enumerate(r)) + "|"
            )
    return out


def align(path):
    lines = io.open(path, encoding="utf-8").read().split("\n")
    out, buf, in_fence, changed = [], [], False, 0

    def flush():
        nonlocal buf, changed
        if not buf:
            return
        rows = [l.strip().strip("|").split("|") for l in buf]
        rendered = render(rows)
        if rendered is None:
            out.extend(buf)
        else:
            if rendered != buf:
                changed += 1
            out.extend(rendered)
        buf = []

    for line in lines:
        if line.startswith("```"):
            flush()
            in_fence = not in_fence
            out.append(line)
            continue
        t = line.strip()
        if not in_fence and t.startswith("|") and t.endswith("|") and len(t) > 1:
            buf.append(line)
            continue
        flush()
        out.append(line)
    flush()

    io.open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"{path} | 표 정렬: {changed}개")


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    for p in argv:
        align(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
