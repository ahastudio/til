---
paths:
  - "**/*.md"
---

# Writing Guidelines

## Natural Korean — No Literal Translation (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**Never translate English words or expressions literally into Korean prose.**
Literal translation is the most common cause of unnatural-sounding Korean.

**Forbidden pattern — mechanically mapping an English verb to a Korean verb:**

| English concept | Literal (forbidden) | Natural Korean       |
| --------------- | ------------------- | -------------------- |
| twist (mockery) | 비틀다              | 꼬집다, 비꼬다       |
| cut (dismiss)   | 자르다              | 단정하다, 정리하다   |
| capture         | 포착하다            | 담다, 잡아내다       |
| highlight       | 하이라이트하다      | 강조하다, 부각하다   |
| navigate        | 내비게이트하다      | 탐색하다, 다루다     |

This table is illustrative, not exhaustive.
Whenever you thought of the English word first and then translated it,
stop and rethink.

**Test:** Before writing a verb, ask "Would a native Korean speaker say this
naturally?" If you reached for the English word first, that is a warning sign.
In that case, express the intended meaning in Korean from scratch.

**Verb selection:** Prefer pure Korean verbs that express the meaning directly.
Sino-Korean verbs are acceptable when they are more natural and precise.
Foreign-origin `-하다` verbs are only allowed when they are established
industry-standard terms.

## Forbidden Vocabulary — 박다 계열 (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**NEVER use the verb `박다` or any of its conjugated or compound forms in TIL
prose.** This verb carries a coarse, crude, and unpleasant connotation in
Korean that does not fit the tone of these documents. Its use is a defect, not
a style choice.

Forbidden forms include, but are NOT limited to:

- `박다`, `박는다`, `박지`, `박았다`, `박은`, `박힌`, `박혀`, `박혀 있다`
- `박아 넣다` / `박아넣다`, `박아 두다` / `박아두다`
- `박제`, `박제하다`, `박제되다`

This list is illustrative, not exhaustive. Any word built on the `박-` stem
with this "drive in / nail in / embed" meaning is forbidden, even forms not
spelled out above.

Use a plainer verb that states the actual meaning instead:

- embedding / inserting → `넣다`, `삽입하다`, `포함하다`
- persisting / remaining → `남다`, `남기다`, `유지되다`
- imprinting on memory → `각인시키다`, `각인되다`
- repeating for emphasis → `반복하다`, `강조하다`
- hardcoding → `하드코딩하다`, `고정하다`

**Mandatory check:** Before finishing ANY `.md` write or edit, scan the text
you produced for the `박` character used as this verb. If you find even one
instance, replace it before completing. "It reads fine" is not an excuse —
the verb is banned regardless of how natural it sounds in context.

If you catch yourself typing `박아`, `박힌`, `박제`, or any sibling form:
STOP and rewrite with a neutral verb.

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

## Source Footnotes in Researched Documents (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**When a document is assembled from collected material — web searches,
several articles, reports, official pages — every factual claim carries a
footnote that points to the source it came from.**
A reference list at the end of the document is not a substitute.
A list says what was read; only a footnote says which source supports which
sentence, and that is what a reader needs in order to check a number.

Why this is a defect and not a style choice: a researched document is only
as trustworthy as the reader's ability to trace each claim. When sources
disagree — and in researched topics they routinely do — an unattributed
number cannot be weighed against its rivals, and an error cannot be traced
back to where it entered.

Rules:

- Every number, date, name, quotation, and specific factual claim that came
  from a source gets a footnote reference right after it, in the same
  sentence or table cell.
- The footnote points to the page the claim was actually read from.
  If the claim was read in a secondary report that cites a primary source,
  footnote the page that was read, and name the primary source in the prose.
  Never footnote a primary source you did not open.
- A quotation is footnoted to the page where the quoted words appear.
- One footnote label per source page, reused wherever that page supports a
  claim. Choose a short, readable label that identifies the source.
- A table that compiles figures from several sources carries a footnote in
  each row or cell, not one note for the whole table.
- The document's own analysis, comparison, and judgment are not footnoted;
  the facts they rest on are.
- Every footnote definition carries the publisher, the source's own title
  as a link, and the source's publication date. A bare URL is not enough:
  the reader must be able to tell what the source is and how current it is
  without opening it.

  ```markdown
  [^label]: <매체>, [<원문 제목>](<URL>), <YYYY-MM-DD>
  ```

  The title is copied as the source presents it, untranslated. The date is
  the publication date read from the page itself (its byline, metadata, or
  URL), never a guess and never the date it was read. If a page shows no
  publication date, say so in the definition rather than leaving the field
  out silently.
- Footnote definitions follow `## Footnote Spacing` and sit at the end of
  the document after a `---` rule.
- This format is for researched sources. Footnotes that cite a community
  comment (Hacker News, Lobste.rs, GeekNews) keep the bare `<URL>` form
  their skills specify.
- A separate reference-list section is not added on top of the footnotes.
- Claims that could not be confirmed are stated as such in the text, never
  footnoted to a source that does not actually say them.

**Mandatory check before finishing a researched document:**

1. Scan every paragraph, table row, and list item for numbers, dates, names,
   and quotations.
2. For each one, confirm a footnote reference sits next to it.
3. For each footnote, confirm the page it points to was actually read and
   says what the sentence claims.

## Social Posts as a Starting Point (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**When the user brings a social post (a Threads post or thread, a tweet,
and the like) and asks for a document on its subject, the document is
built from facts, and the post is reflected only to the extent that it
can carry a footnote.**

The post is a lead, not the backbone. Root cause of a past failure: the
post's framing, numbers, and claims drove the structure, and the critique
section ended up arguing with the post instead of explaining the subject.

Rules:

- Find and read the primary sources the post points to or relies on
  (original documents, reports, official pages), and build every section
  from them.
- The title, sections, and conclusions describe the subject, not the post.
  Do not organize the document as a claim-by-claim check of the post, and
  do not write a critique section aimed at the post.
- Use the post only where it adds something citable: a fact the primary
  sources lack, a firsthand account, or an interpretation worth noting in
  a sentence or two. Every such use carries a footnote to the exact post.
- The post always appears in at least one footnote.
- When the post disagrees with the sources, state the sourced fact in the
  body and note the discrepancy briefly, with the post footnoted.
- Claims from the post that could not be verified are attributed to the
  person, never stated as fact.
- In prose, attribute to the person, never to the post. Name the platform
  and the handle as a user: `Threads 사용자 <handle>는 ...라고 했다`
  (or `적었다`, `짚었다`). Never call it 게시물, 타래, 글, 작성자, or
  댓글 in the document, and never write that "the post claims" something.
  This applies to the author and to repliers alike.
- Footnote link text is the cited post's own opening words, not a label
  such as 후속 게시물, 타래 3, or 댓글.

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

## Twitter Links

Always use `twitter.com` instead of `x.com` for tweet URLs.

In prose, always call the service Twitter, never X.
This applies to documents, chat messages, and headings alike, including
compound names such as a Twitter Article.
The domain `x.com` may still appear where the literal domain is the point,
such as a rule about which URLs to rewrite.

## Tweet Terminology

Call it a "트윗" unless the user explicitly says "스레드". Long tweets are still
tweets.

## Argument and Evidence

An analytical document must make three layers distinguishable:

- **Reported fact:** what the cited material directly says.
- **Inference:** what follows from those facts, including the assumptions
  needed to connect them.
- **Judgment:** what the writer recommends, doubts, or considers important.

Do not let a sourced fact silently carry a broader conclusion. Name the
bridge between them, and state when it is an assumption rather than a
verified fact.

When a claim is disputed, address its strongest plausible form. A useful
critique identifies the evidence that would support the claim, the evidence
that would weaken it, and the observation that could distinguish between
competing explanations.

For practical notes, end the reasoning with a decision rule, a sequence of
actions, or a failure condition the reader can apply. Avoid adding a
generic summary when the document already states its conclusion.
