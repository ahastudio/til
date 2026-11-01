# Document shape and footnotes (steps 7a, 7b)

## Contents

- [7a. Document shape — CLOSED SPEC (NO EXCEPTIONS)](#7a-document-shape-closed-spec-no-exceptions)
- [7b. Footnotes — STRICT RULE (NO EXCEPTIONS)](#7b-footnotes-strict-rule-no-exceptions)

## 7a. Document shape — CLOSED SPEC (NO EXCEPTIONS)

**A document produced by this skill has exactly the shape below. The set of
line kinds allowed above the first `##` is closed: nothing else may appear
there, however useful it seems.**

```markdown
# <한국어 제목>

원문: [<원문 제목>](<URL>)

HN 토론: <URL> (<점수>점, <댓글 수>개 댓글)

Lobste.rs 토론: <URL> (<점수>점, <댓글 수>개 댓글)

GN 토론: <URL>

## <첫 섹션>

...본문...

---

[^handle]: <URL>
```

Rules that follow from it:

- The H1 is line 1, Korean prose, followed by one blank line.
- Exactly one source line, in the form step 4 selected. When the user asks
  for several published pieces to be combined into one document (a
  multi-part tutorial, for example), write one labeled source line per piece,
  in order, each separated by a blank line. A non-article may use
  two or more consecutive bare `<URL>` lines (homepage first, then repo), each
  separated by a blank line.
- Discussion lines come after the source line, one per line, separated by
  blank lines, in the order HN → Lobste.rs → GN. HN and Lobste.rs carry
  `(N점, N개 댓글)`, copied as the site reports it, including a negative
  score such as `(-1점, 4개 댓글)`; GN carries the bare URL alone. A `Show GN:` /
  `Ask GN:` line takes the GN slot and a `Show HN:` / `Ask HN:` line takes
  the HN slot, as `[<제목>](URL)`. Two threads on the same
  platform for the same subject get two lines of that platform, adjacent.
- Existing documents in this repository also use four older header forms,
  and the gate accepts them so those documents are left as they are: a
  `원문: <URL>` source line without a title, a
  `> <제목>` quote line directly above a bare source URL, a `GeekNews: <URL>`
  line in the GN slot, and an `HN 토론:` / `Lobste.rs 토론:` line without
  counts. New documents still use the forms above.
- **No other labeled line exists.** `제품 페이지:`, `저자:`, `발표:`,
  `관련 글:` and every other invented label is forbidden. Information like
  that belongs in a body section, in prose.
- The discussion lines are written by the reaction skills in step 9. Do not
  invent, guess, or pre-fill them.

**Sections are a closed set too.** Use the headings the step 6 template for
your chosen body gives you, plus subject-fitting sections for a non-article.
Never add a section that reports on the *process* of writing the document.
`## 반응 현황`, `## 반응`, `## 커뮤니티 반응` and the like are forbidden: when
a platform has no thread, that is reported to the user in chat, never as a
section of the document. A document records what is true about the subject,
not what the search turned up.

## 7b. Footnotes — STRICT RULE (NO EXCEPTIONS)

**Footnotes for outside pages are complete and exact; the analyzed source needs
none per sentence.** When the prose names where something came from, the
footnote closes that sentence and links that exact page. References go at
sentence ends, not mid-sentence. **The analyzed source itself never takes a footnote — ABSOLUTE, ZERO
TOLERANCE.** The source line under the title is its only link: no footnote
for a sentence, a quotation, a figure, the date, or the author, and none in
the titled form. Say what is needed in the prose. Before the gate and again
after the reaction skills, compare every footnote definition's URL with the
source line's URL; any match is deleted with all of its references. A
document you enhance is checked the same way.
Every sentence that rests on an outside page — a page the source quotes that
was also opened and read, or material fetched to check or extend the source —
carries its own footnote in the titled form of `writing-guidelines.md`
(`[^label]: <매체>, [<원문 제목>](<URL>), <YYYY-MM-DD>`), and two pages mean two
references. Rules 2 and 5 below govern the community-comment footnotes only.

A woven-in reaction is attributed inline and carried by a footnote whose label
is the commenter's handle:

```markdown
tttttaa는 회색지대 사례를 살펴볼수록 미묘해진다고 적었다.[^tttttaa]

[^tttttaa]: <https://news.hada.io/topic?id=33582#cid123456>
```

1. Definitions collect at the bottom, after the last body section, under a
   `---` rule, one per line, separated by blank lines.
2. Every comment footnote definition is a bare `<URL>` in angle brackets. No prose, no quoted
   comment text, no trailing commentary.
3. The target is a permalink to the individual comment, never the thread root.
4. Labels and definitions are one-to-one. A defined label that nothing
   references, and a reference with no definition, are both defects.
5. The label is the handle exactly as that site spells it. On a collision with
   an existing label, disambiguate with a suffix (`[^handle-lobsters]`), never
   by renaming the person.
6. **Never write an anchor you have not observed.** Comment ids are read off
   the page or the API response you actually fetched. Constructing one that
   looks plausible — guessing a `#cid`, incrementing an id, reusing a
   neighbouring comment's anchor — is fabrication, and it has happened in this
   repository before. If you cannot see the id, do not cite the comment.
7. A footnote reference must not sit inside a code fence or an inline code
   span. Regex character classes like `[^,]` and `[^)]` inside a fence read as
   footnote syntax to some tooling; rewrite the expression or move it out of
   the snippet rather than leaving the collision in place.
