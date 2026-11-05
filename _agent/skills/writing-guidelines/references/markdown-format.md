# Markdown Format Rules

## Contents

- Structure Belongs to Headings: never bold text where a heading belongs
- Heading Spacing, One Table Row Is One Record, Table Alignment: blank lines around headings, no split rows, CJK counts as 2 columns
- Footnote Spacing: one blank line between definitions
- Inline Code Formatting, Fenced Code Block Language: wrap code-like tokens; every fence has a language
- Note Document Structure: article vs. project headings
- Line Breaks in Body Text: sentence per line, at most 80 columns, CJK counts as 2

## Structure Belongs to Headings (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**Never use bold text where a heading belongs.** If a run of text opens a
distinct part of the document, that part gets a real heading. Emphasis markup
is for a word or a clause inside a sentence, never for the thing that announces
what the next several paragraphs are about.

Why this is a defect and not a style choice: a heading is structure and
emphasis is decoration. Headings enter the document outline, can be linked to,
can be counted, and tell a reader scanning the page where they are. Bold text
does none of that. A document whose sections are marked with emphasis has no
structure at all — it only looks like it does.

Rules:

- If it introduces a section, it is a heading. Use the heading level that
  matches its depth in the document.
- If a section is too small to deserve a heading, it is not a section. Fold it
  into the surrounding prose, or merge it with a neighbour, or give the group a
  single heading that covers all of it.
- Never let a bold line stand alone on its own line followed by body text. That
  shape is a heading wearing a disguise.
- Emphasis stays inside a sentence and marks a word or phrase, not a topic.
- Do not restructure to avoid the rule. Choosing bold because you did not want
  to think about the outline is the exact failure this rule exists to prevent.

**Mandatory check before finishing ANY `.md` write or edit:**

1. Find every line that consists mostly or entirely of bold text.
2. For each one, ask: does body text follow it that this line introduces?
3. If yes, it is a heading. Convert it, or dissolve the section.
4. Only emphasis that sits inside a running sentence may remain.

This check runs on every document, including ones where the sections are short
and the bold form looks tidy. Tidiness is not a reason. If you catch yourself
writing a bold line as a section opener: STOP and decide the outline instead.

## Heading Spacing

Always add blank lines before and after headings. This is required for markdown
linters and improves readability.

## One Table Row Is One Record (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**Never split one cell's content across two table rows.**
A markdown table has no line continuation.
A second row with an empty first cell is not a continuation of the row
above; it is a separate record with a blank key, and it renders as one.

Why this is a defect and not a style choice: it changes what the table
says. The reader sees a record with no name, and the content of one cell
is torn into two unrelated cells.

Rules:

- Every row holds one complete record. Each cell holds its whole value on
  one line, however long the line becomes.
- Never wrap a cell to fit 80 columns. Tables are exempt from the
  line-length limit; a long row is correct, a split row is wrong.
- A row whose key cell is empty is forbidden unless the source data itself
  has an empty key.
- If a cell is too long to read comfortably, shorten the wording or move the
  detail into prose below the table. Never continue it on the next row.

**Mandatory check before finishing ANY `.md` write or edit that contains a
table:** scan every row for an empty first cell. If one exists and the
source data does not have an empty key there, merge it into the row above
before finishing.

## Table Alignment

When formatting markdown tables with Korean text:

1. Count Korean characters as 2 columns each (same as CJK width rule)
2. Align table pipes by padding cells with spaces
3. Find the longest content in each column
4. Pad shorter cells with trailing spaces to match column width

Example:

```markdown
| 항목   | Description |
| ------ | ----------- |
| 이름   | Name        |
| 설명   | Explanation |
| 작성자 | Author      |
| 상태   | Status      |
```

- "작성자" (3 Korean chars = 6 columns) is longest in left column
- "Explanation" (11 English chars = 11 columns) is longest in right
- All cells padded to match their column's maximum width

## Footnote Spacing

Separate every footnote definition from the next with one blank line.
Never stack definitions on consecutive lines. When appending to an existing
footnote block, keep the same spacing and fix any stacked entries you find
in that block.

```markdown
[^first]: <https://example.com/1>

[^second]: <https://example.com/2>
```

## Inline Code Formatting

Wrap code-like tokens in backticks for readability. This applies to
both notes and commit messages. Examples of what to wrap:

- File and directory names: `README.md`, `openai/`, `src/main.py`
- Commands and CLI flags: `git rebase`, `--no-verify`
- Identifiers: function names, variable names, class names
- Technical keywords that refer to code: `return await`, `null`,
  `useState`
- URLs that would otherwise be autolinked when you do not want them
  linked (e.g. `http://127.0.0.1:8080`)

Do not wrap plain prose, product names, or concepts (OpenAI, ESLint,
RLHF) in backticks.

## Fenced Code Block Language

Every fenced code block MUST have a language identifier. No exceptions.

- Use the actual language when known: `bash`, `yaml`, `go`, `python`, etc.
- Use `text` for diagrams, ASCII art, plain output, or anything that has
  no specific language.
- A bare ` ``` ` with no identifier is always wrong.

## Note Document Structure

TIL notes vary by the nature of their subject. Match the section structure to
what the subject actually is, not to a fixed template.

- **Article or blog post** (the subject is a piece of writing):
  Use `## 요약` as the first section.
- **Project, tool, framework, or collection** (the subject is something you
  use or explore):
  Do NOT use `## 요약`. Choose a heading that fits what the section actually
  covers — e.g., `## 소개`, `## 명세`, `## 사용법`, `## 주요 법칙`, `## CLI`.
  A single subject may warrant multiple top-level sections if its content
  naturally splits (e.g., spec + CLI for a tool with both).

Sections beyond the first are chosen to fit the subject. A note that exists to
teach a task may use practical headings (procedure, trade-offs, checklist); a
note that examines a piece of writing may use analytical ones. Do not impose an
analytical structure on a document whose job is something else.

## Line Breaks in Body Text

Break body text at sentence boundaries first, then keep every line within
80 columns by breaking at natural semantic units. Each sentence starts on its
own line, and no line may exceed 80 columns.

**Rules:**

- Every sentence starts on a new line.
- A period (`.`), question mark (`?`), or exclamation mark (`!`) ends the
  line — do not continue the next sentence on the same line.
- No body line may exceed 80 columns. Count Korean (CJK) characters as 2
  columns each and everything else as 1, the same as the table alignment
  rule.
- When a sentence does not fit within 80 columns, break it at the most
  natural semantic boundary: after a comma, before a conjunction or
  connective (이며/하지만/그러나/그리고/하면/때문에 etc.), or between
  clauses. Break as many times as needed to stay within 80 columns.
- Never break mid-phrase just to fill the line (e.g. between a noun and its
  particle-bearing modifier, or inside a title or name). Prefer a shorter
  line that ends at a semantic boundary over a full line that splits a unit.
- Continue on the next line with NO indentation — indented continuation
  lines become code blocks in most markdown renderers.
- Do not break inside a link, an inline code span, or a footnote reference.
- This rule applies to all `.md` body text. Code blocks, tables, headings,
  footnote definitions, URL lines, and list items are excluded, and the
  80-column limit does not apply to them either. Never wrap or reflow a
  table row, code line, heading, or URL line to fit 80 columns.

**Example:**

```markdown
Revo는 Zig로 작성된 동적 타입 언어다.
README는 기술 사양보다 사용 경험을 먼저 보여주는 구성이다.
파이프, 패턴 매칭, 채널 루프, 테스트 블록은
Revo를 짧은 시간에 이해시키는 데 효과적이지만,
운영 의사결정자 관점에서 필요한 릴리스 정책은 상대적으로 얇다.
```
