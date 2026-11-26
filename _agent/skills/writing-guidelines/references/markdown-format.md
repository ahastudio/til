# Markdown Format Rules

## Contents

- Structure Belongs to Headings: never bold text where a heading belongs
- Lists And Prose: judge every list on its own; reasoning is never a bullet list, a short parallel enumeration is never flattened into a sentence
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

## Lists And Prose: Judge Every List On Its Own (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**A list is neither good nor bad. The shape of the content decides, one list at
a time. Habit in either direction is a defect, and a blanket rule such as
"remove the bullets" or "use bullets for clarity" is the exact way this goes wrong.**

Root cause of a repeated failure: documents were written with reasoning chopped
into bullets, and the repair was a blanket conversion that also flattened short
parallel lists into one long sentence. Both are wrong. The reader lost the
count and the scanning that a list gives, in the one case, and lost the argument
that prose gives, in the other.

### Two defects, with their tests

- **Defect A: reasoning chopped into bullets.** Each of these makes a list the
  wrong form:
  - an item holds a reason, a contrast, a condition or a conclusion;
  - an item runs to two sentences or more;
  - an item depends on the one before it (because, but, so, therefore);
  - the list is the whole content of a section whose job is to argue.
  Write it as prose: one paragraph per claim, connected by the words that carry
  the logic.
- **Defect B: a parallel enumeration flattened into prose.** A list is right
  and must be kept or restored when all of these hold:
  - three or more items, each the same kind of thing (named parts, steps of a
    procedure, commands, criteria, claims to verify, cases);
  - each item is a noun phrase or one short clause that stands alone;
  - the reader will scan it, count it, compare it or tick it off.
  A sentence of the form "A, B, C 세 가지다" that hides a count the reader needs
  is Defect B. An item with several attributes each is a table, not a list.

### Sections that are never bullet lists (ABSOLUTE)

`## 인사이트` is never a bullet list, and neither is `## 비평`, `## 분석`, or any
section that argues. A heading that only contains the word, such as `## 코드 분석`
in a practical document, is judged by the five questions like any other section. Give each point a `###` heading that is a name (a noun
phrase, never a sentence) and write short prose under it, two to four
sentences. What to verify next is its own `### 확인할 것` in prose.
A bullet list inside such a section is a violation even when the items are
short. An enumeration that is part of the evidence (the three claims a source
makes, the parts of a design) may be a short list inside the prose of 요약 or
분석, because it enumerates facts and does not argue.

### Ordinal enumeration in prose

When prose names its items with ordinals (첫째, 둘째, 셋째, 넷째), each
ordinal opens its own paragraph, with a blank line between paragraphs. An
ordinal block of one short sentence may stay inside the paragraph that
introduces it only when the whole enumeration is three sentences or fewer.
A long passage that runs the ordinals together under one paragraph is a
defect. The check is a paragraph that holds two or more lines starting with
an ordinal.

### Judging a list before keeping, writing or converting it

Answer each question for the list in front of you, in this order:

1. Does any item need another item to be understood? Yes: prose.
2. Is any item longer than one short line? Yes: prose, or split the item.
3. Are there three or more items of the same kind that the reader will scan or
   count? Yes: keep the list.
4. Does each item have two or more attributes of its own? Yes: a table.
5. Is this an insight, a critique or an analysis? Yes: prose under `###`
   headings, whatever the answers above.

### Worked examples (decide by these, not by taste)

Keep as a list (Defect B if flattened): three short items of one kind.

```markdown
트윗은 논란이 된 세 가지를 든다.
- 기본으로 켜진 텔레메트리(telemetry)
- 로컬 인증 설정을 읽어 사용자 식별자를 만드는 동작
- 원격 연결의 신뢰 경계
```

Flattened wrongly into one sentence: `트윗이 논란으로 든 것은 기본으로 켜진
텔레메트리, 로컬 인증 설정을 읽어 식별자를 만드는 동작, 원격 연결의 신뢰 경계
세 가지다.` The count and the scanning are lost. Restore the list.

Also lists: the thirteen parts of a product, the steps of a procedure, the
parameters of a command, a release's headline features when each is one short
line, the claims a source makes when each is one short clause, the criteria of
a checklist.

Prose (Defect A if listed): each item gives a reason or a contrast.

```markdown
- 점진적 공개는 토큰을 줄인다.
- 그래서 비용이 준다.
- 하지만 지연이 늘어난다.
```

This is one argument cut into three lines. Write it as a paragraph: `점진적 공개는
토큰을 줄여 비용을 낮추지만, 모델 호출이 하나 늘어 지연이 커진다.`

Ordinal passages whose items each need two or more sentences are prose: one
paragraph per ordinal, a blank line between. Ordinal items that are each one
short clause are a list, written with `- `, not with 첫째, 둘째.

An insight, critique or analysis section is prose under `###` headings, even
when its points are short.

### When converting an existing document

- Never convert wholesale. Open every list, answer the five questions, and
  decide that list alone.
- Never merge a three-item list into a sentence with commas. If the rule says
  keep it, keep the list and its line breaks.
- When the task is delegated to another agent, the instruction must carry this
  section in full. An instruction that says only to remove bullets produces
  Defect B.
- Report, for every list touched, what was kept as a list, what was converted
  and the reason, and which lists were restored after an earlier wrong
  conversion. A report that says only that the bullets were removed is not a
  report.
- Before finishing, reread every converted passage once as the reader and ask
  whether a scanning reader lost a count, an order or a comparison. If so, restore
  the list.

**Mandatory check before finishing any `.md` write or edit:**

1. List every bullet or numbered line under `## 인사이트`, `## 비평`,
   `## 분석`. The count must be zero:
   `awk '/^## /{s=$0} /^[ ]*([-*]|[0-9]+\.) /{if(s ~ /^## (인사이트|비평|분석)$/) print FILENAME": "s": "$0}' <file>`
2. Search for the phrases `세 가지다`, `네 가지다`, `다섯 가지다` and a line
   that ends in a comma and runs on for three or more same-kind noun phrases. Each
   hit is a candidate for Defect B; apply the five questions.
3. Search for any bullet whose item has two or more sentences or contains
   because, but or so. Each hit is Defect A.

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

## Bare Addresses: Domain-Only Ends With A Slash

A bare address written on its own line (`<URL>`) that has only a domain ends
with a slash: `<https://www.google.com/>`, never
`<https://www.google.com>`. An address with a path takes no added slash
(`<https://example.com/docs>`, `<https://github.com/org/project>`). The
format gate of `analyze-article` fails a domain-only address without the
slash. When editing any document, fix such a line in the same pass.
