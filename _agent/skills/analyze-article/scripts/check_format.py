#!/usr/bin/env python3
"""Format gate for analyze-article documents.

Usage:
    python3 _agent/skills/analyze-article/scripts/check_format.py <file.md> [...]

Exits non-zero when any document fails. Every rule here is stated in
_agent/skills/analyze-article/SKILL.md; this script only enforces them.
"""
import io
import os
import re
import sys
import unicodedata

ARTICLE_LABELS = (
    "원문", "트윗", "영상", "논문",
    "Ask GN", "Show GN", "Ask HN", "Show HN",
)
DISCUSSION_ORDER = ("HN", "Lobste.rs", "GN")


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def split_fences(lines):
    """Return (in_fence flags, fence language ok errors)."""
    flags = [False] * len(lines)
    errors = []
    open_at = None
    lang = None
    for i, line in enumerate(lines):
        if line.startswith("```"):
            if open_at is None:
                open_at = i
                lang = line[3:].strip()
                if not lang:
                    errors.append(f"{i + 1}: 코드펜스에 언어 식별자가 없음")
            else:
                open_at = None
            flags[i] = True
            continue
        if open_at is not None:
            flags[i] = True
    if open_at is not None:
        errors.append(f"{open_at + 1}: 닫히지 않은 코드펜스")
    return flags, errors


def check_header(lines, issues):
    if not lines or not lines[0].startswith("# "):
        issues.append("1: 첫 줄이 H1이 아님")
        return None
    if not re.search(r"[가-힣]", lines[0]):
        issues.append("1: H1에 한글이 없음 (H1은 한국어 산문)")
    if len(lines) > 1 and lines[1].strip():
        issues.append("2: H1 다음에 빈 줄이 없음")

    # locate the source line: first non-blank line after the H1
    idx = None
    for i in range(1, len(lines)):
        if lines[i].strip():
            idx = i
            break
    if idx is None:
        issues.append("출처 줄이 없음")
        return None

    src = lines[idx].strip()
    labeled = re.match(r"^(%s): (.+)$" % "|".join(ARTICLE_LABELS), src)
    bare = re.match(r"^<https?://[^>]+>$", src)

    kind = None
    if labeled:
        kind = "article"
        body = labeled.group(2)
        if re.match(r"^<https?://", body):
            issues.append(
                f"{idx + 1}: 레이블 있는 출처 줄이 맨 URL — [제목](URL) 형태여야 함"
            )
        elif not re.match(r"^\[[^\]]+\]\(https?://[^)]+\)$", body):
            issues.append(f"{idx + 1}: 출처 줄이 `레이블: [제목](URL)` 형태가 아님")
    elif bare:
        kind = "non-article"
        # a subject may carry both a homepage and a repo, one bare URL per line
        while idx + 2 < len(lines) and re.match(
            r"^<https?://[^>]+>$", lines[idx + 2].strip()
        ):
            if lines[idx + 1].strip():
                issues.append(f"{idx + 2}: 맨 URL 줄 사이에 빈 줄이 없음")
            idx += 2
    else:
        issues.append(
            f"{idx + 1}: 출처 줄이 `원문: [제목](URL)` 도 `<URL>` 도 아님"
        )
        return None

    # discussion lines
    seen = []
    i = idx + 1
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("## "):
            break
        m = re.match(r"^(HN|Lobste\.rs|GN) 토론: (.+)$", line)
        if not m:
            issues.append(f"{i + 1}: 헤더 블록에 허용되지 않은 줄")
            break
        if not lines[i - 1].strip() == "":
            issues.append(f"{i + 1}: 토론 줄 앞에 빈 줄이 없음")
        plat, rest = m.group(1), m.group(2)
        if plat == "GN":
            if not re.match(r"^<https?://[^>]+>$", rest):
                issues.append(f"{i + 1}: GN 토론 줄은 `<URL>` 만 와야 함")
        else:
            if not re.match(r"^<https?://[^>]+> \(\d+점, \d+개 댓글\)$", rest):
                issues.append(
                    f"{i + 1}: {plat} 토론 줄이 `<URL> (N점, N개 댓글)` 형태가 아님"
                )
        seen.append(plat)
        i += 1

    ranks = [DISCUSSION_ORDER.index(p) for p in seen]
    if ranks != sorted(ranks):
        issues.append("토론 줄 순서가 HN → Lobste.rs → GN 이 아님")

    return kind


def check_sections(lines, in_fence, kind, issues):
    sections = [
        (i, lines[i][3:].strip())
        for i in range(len(lines))
        if lines[i].startswith("## ") and not in_fence[i]
    ]
    if not sections:
        issues.append("## 섹션이 없음")
        return []
    names = [s[1] for s in sections]

    # The opening heading is chosen by document type (step 5); only the
    # non-article rule from writing-guidelines.md is mechanical.
    if kind == "non-article" and names[0] == "요약":
        issues.append("비문서(맨 URL) 문서의 첫 섹션이 `## 요약`")

    # The analytical body is all-or-nothing (step 5a). `## 분석` is the marker
    # that the document was built on that spine; a practical note may close
    # with a lone `## 비평` or `## 인사이트` without owing the other two.
    analytic = ("분석", "비평", "인사이트")
    present = [n for n in names if n in analytic]
    if "분석" in present:
        missing = [n for n in analytic if n not in present]
        if missing:
            issues.append(
                "분석 구조가 불완전함 — `## "
                + "`, `## ".join(missing)
                + "` 누락 (분석/비평/인사이트는 셋이 함께 간다)"
            )
        expected = [n for n in analytic if n in present]
        if present != expected:
            issues.append(
                f"분석 → 비평 → 인사이트 순서가 아님 (실제: {' → '.join(present)})"
            )

    banned = {"반응 현황", "반응", "커뮤니티 반응", "토론 반응"}
    for n in names:
        if n in banned:
            issues.append(
                f"`## {n}` 섹션 금지 — 반응 부재는 문서가 아니라 채팅으로 보고"
            )
    return names


def check_tables(lines, in_fence, issues):
    block, start = [], None
    for i, line in enumerate(lines + [""]):
        t = line.strip()
        if i < len(lines) and in_fence[i]:
            t = ""
        if t.startswith("|") and t.endswith("|") and len(t) > 1:
            if start is None:
                start = i + 1
            block.append(t.strip("|").split("|"))
            continue
        if block:
            if len(block) >= 2:
                widths = [[width(c) for c in row] for row in block]
                n = len(widths[0])
                if any(len(r) != n for r in widths) or any(
                    len({r[c] for r in widths}) > 1 for c in range(n)
                ):
                    issues.append(f"{start}행 표: 열 너비가 맞지 않음 (한글 2칸)")
            block, start = [], None


def check_footnotes(text, lines, in_fence, issues):
    defs = re.findall(r"^\[\^([^\]]+)\]:", text, re.M)
    refs = []
    for i, line in enumerate(lines):
        if in_fence[i] or re.match(r"^\[\^[^\]]+\]:", line):
            continue
        clean = re.sub(r"`[^`\n]*`", "", line)
        refs += re.findall(r"\[\^([^\]]+)\]", clean)

    dup = {d for d in defs if defs.count(d) > 1}
    if dup:
        issues.append(f"각주 정의 중복: {sorted(dup)}")

    orphan = sorted(set(defs) - set(refs))
    missing = sorted(set(refs) - set(defs))
    if orphan:
        issues.append(f"본문에서 참조되지 않는 각주 정의: {orphan}")
    if missing:
        issues.append(f"정의가 없는 각주 참조: {missing}")

    for i, line in enumerate(lines):
        if in_fence[i]:
            continue
        m = re.match(r"^\[\^([^\]]+)\]: (.+)$", line)
        if not m:
            continue
        target = m.group(2).strip()
        has_link = re.search(r"https?://", target) or re.search(r"\]\([^)]+\)", target)
        if not has_link:
            issues.append(f"{i + 1}: 각주 정의에 링크가 없음")
        elif re.match(r"^https?://", target):
            issues.append(f"{i + 1}: 각주 URL은 `<...>` 로 감싸야 함")


def check_prose(lines, in_fence, issues):
    list_open = False
    for i, line in enumerate(lines):
        if in_fence[i]:
            continue
        t = line.strip()
        if re.fullmatch(r"\*\*[^*]+\*\*", t):
            issues.append(f"{i + 1}: 굵은 글씨만 있는 줄 — 제목이어야 함")
        if re.match(r"^\s*([-*+]|\d+\.)\s", line):
            list_open = True
        elif not t:
            list_open = False
        elif re.match(r"^\s{4,}\S", line) and not list_open and not t.startswith("["):
            issues.append(f"{i + 1}: 들여쓴 이어짐 줄 — 코드블록으로 렌더링됨")
        if line.startswith("#"):
            prev_bad = i > 0 and lines[i - 1].strip() != ""
            next_bad = i + 1 < len(lines) and lines[i + 1].strip() != ""
            if prev_bad or next_bad:
                issues.append(f"{i + 1}: 제목 앞뒤에 빈 줄이 없음")


def check_vocab_and_quotes(lines, in_fence, issues):
    for i, line in enumerate(lines):
        if in_fence[i]:
            # inside fences quotes stay straight; only check nothing here
            continue
        if re.search(r"박(다|는|았|힌|혀|제|아)", line):
            issues.append(f"{i + 1}: `박-` 어간 금지어")
        outside = re.sub(r"`[^`\n]*`", "", line)
        if '"' in outside:
            issues.append(f"{i + 1}: 곧은 큰따옴표 — quotes-curly 미적용")
        inside = re.findall(r"`[^`\n]*`", line)
        if any("“" in c or "”" in c for c in inside):
            issues.append(f"{i + 1}: 인라인 코드 안의 굽은 따옴표 — 곧은 따옴표여야 함")


def check_filename(path, issues):
    base = os.path.basename(path)
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.md", base):
        issues.append(f"파일명 `{base}` 이 소문자 kebab-case 가 아님")


def check(path):
    text = io.open(path, encoding="utf-8").read()
    lines = text.split("\n")
    in_fence, issues = split_fences(lines)

    check_filename(path, issues)
    kind = check_header(lines, issues)
    names = check_sections(lines, in_fence, kind, issues) if kind else []
    check_tables(lines, in_fence, issues)
    check_footnotes(text, lines, in_fence, issues)
    check_prose(lines, in_fence, issues)
    check_vocab_and_quotes(lines, in_fence, issues)

    print(f"{path} | {'OK' if not issues else 'FAIL'}")
    if kind:
        print(f"  종류: {'글' if kind == 'article' else '비문서'}")
    if names:
        print("  섹션: " + " → ".join(names))
    for m in issues:
        print(f"  - {m}")
    return not issues


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    ok = True
    for p in argv:
        ok = check(p) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
