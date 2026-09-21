#!/usr/bin/env python3
"""Restore straight quotes inside inline code spans.

quotes-curly converts straight quotes to curly ones and correctly skips
fenced code blocks, but it does not skip inline `code spans`. A span like
`"` therefore comes back as `“`, which is wrong: code is quoted verbatim.
Run this right after convert_quotes.py.

Usage:
    python3 _agent/skills/analyze-article/scripts/fix_code_spans.py <file.md> [...]
"""
import io
import re
import sys

CURLY = {"“": '"', "”": '"', "‘": "'", "’": "'"}


def straighten(match):
    text = match.group(0)
    for curly, plain in CURLY.items():
        text = text.replace(curly, plain)
    return text


def fix(path):
    original = io.open(path, encoding="utf-8").read()
    out, changed, in_fence = [], 0, False
    for line in original.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        new = re.sub(r"`[^`\n]*`", straighten, line)
        if new != line:
            changed += 1
        out.append(new)
    text = "\n".join(out)
    if text != original:
        io.open(path, "w", encoding="utf-8").write(text)
    print(f"{path} | 인라인 코드 보정: {changed}줄")
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    for p in argv:
        fix(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
