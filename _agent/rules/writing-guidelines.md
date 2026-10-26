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

### Collocation Is Part of Correctness (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**A Korean sentence is wrong when its noun and predicate do not belong
together, even if every word in it is a real word.**
Root cause of a repeated failure: an English collocation was carried over
word for word, so the sentence pairs a noun with a verb that Korean writers
never pair with it. A reader stops at it, and the whole document loses
credibility. The user treats this as a severe defect, not a style issue.

- Each noun takes the predicate that Korean writing actually uses with it.
  Abstract nouns such as a definition, a standard, a consensus, or a
  meaning take the predicates established in Korean prose for that noun,
  never a physical or sensory verb borrowed from an English idiom.
- Never render an English idiom or metaphor by its literal words. Find the
  plain Korean predicate for what it means, or drop the metaphor.
- If you cannot name a common Korean phrase that uses this exact noun and
  predicate pair, the pair is suspect. Rewrite it with a plainer predicate.
- Sentences translated from a source deserve the most suspicion: you wrote
  them with the English still in mind.
- This applies equally to documents, headings, table cells, footnotes, and
  chat messages.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message in Korean:**

1. Read every sentence you produced as a Korean reader would, without the
   source in mind.
2. For each noun and predicate pair, ask whether a Korean writer would
   naturally write that pair. Any doubt means rewrite.
3. For each sentence that came from an English source, rebuild it from the
   meaning instead of adjusting the translated words.
4. Do this for the whole text you produced, not just the sentence a
   previous correction pointed at. A correction to one sentence means the
   same failure may exist elsewhere; search for it.

## Never Force an English Term Into Korean (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**A word that the field uses in English stays in English. Inventing a Korean
word for it, or picking a dictionary equivalent that readers have never
seen in that role, is forbidden in every document, heading, table cell,
footnote, and chat message.**

Root cause of a repeated failure: an English term was swapped for a Korean
word that is not what Korean practitioners write, and the swap also collides
with another established meaning. A reader then asks what the word refers to,
and the document loses credibility. The user treats this as a severe defect.

- Before writing a Korean word for a foreign term, ask whether Korean
  practitioners actually write that word for that concept. If you cannot name
  a document, product, or standard that does, keep the original term.
- Design, graphics, and platform vocabulary is the highest-risk area. Terms
  such as material, surface, backdrop, layer, shader, and sample belong to
  their field in English. Do not turn them into coined Korean nouns or
  common-noun look-alikes.
- A Korean word that already carries another established meaning in the same
  field is never reused for the English term. If the reader could mistake it
  for that other thing, the word is wrong.
- When no settled Korean form exists, write the original term, or describe the
  concept in a plain phrase once and then keep using the original term. Do not
  create a shorthand.
- Do not translate a product's own vocabulary (API names, parameter names, the
  names of styles or modes). Keep it exactly as the product writes it.
- Never force a sentence structure, metaphor, or compound noun from the
  source into Korean word for word. If the Korean reads as a translation, the
  sentence is rebuilt from its meaning.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:** list every Korean noun that stands in for a
foreign technical term, and for each one confirm that practitioners write it
that way. Replace every failure with the original term or a plain description.
When the user points at one such word, search the whole document and every
other document written in the same session for the same family of word and fix
them all in the same edit.

## Every Sentence Must Make Sense (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**A sentence is finished only when a reader who has not seen the source can
say plainly what it means. A sentence that parses but says nothing, or says
something other than what was meant, is a defect in every document, heading,
table cell, footnote, and chat message.**

Root cause of repeated failures: the writer compressed or translated while
thinking in another language and never read the result as a stranger would.
The usual forms are these:

- Compressing a source's phrase into a fragment whose referent disappears,
  so the reader cannot tell what the phrase points at.
- Carrying a foreign sentence structure or idiom into Korean word for word.
  Each word is real and the sentence still means nothing to a Korean reader.
- Coining a shorthand name for a source, an idea, or a section, and using it
  as if the reader already knew it.
- Filler sentences that talk about the document itself instead of its
  subject, repeated in the same stock shape across paragraphs.
- Metaphors that only work in the original language.

Rules:

- Before finishing any text, read every sentence cold. For each one ask what
  exactly it claims and what each noun refers to. If the answer cannot be
  given in one plain sentence, rebuild the sentence from its meaning. Do not
  patch it cosmetically.
- Say who did what, which thing is meant, and which source said it. Do not
  leave the reader to infer a subject, an object, or a time.
- When a reader points at one unclear sentence, search the whole document, and
  every other document written in the same session, for the same form of
  failure, and fix them all in the same edit.
- Never explain a source's circumstances (hosting, archiving, mirroring) unless
  they change how the content should be read.

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

## Source Footnotes in Source-Based Documents (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**When a document reports what outside pages say — several articles compiled,
reports, official pages, search results, or pages that a single analyzed
article quotes or that were fetched to check it — every factual claim that
rests on such a page carries a footnote that points to it. Footnotes for
outside pages are complete and exact: every claim has its page, and each
footnote sits where the claim is made — never sparse, never padded.**
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
- Abundance is the default for every page other than the document's own
  analyzed source. Every sentence that rests on such a page — a claim, a
  number, an example, a quotation, a comparison — carries its own footnote
  reference, and a sentence resting on two pages carries two. A paragraph of
  such content with no footnote, or one reference parked at the end of
  several sentences, is a defect. When in doubt, add the footnote.
- A named source gets its own footnote. When the prose says where something
  came from — taken from an encyclopedia entry, quoted from a report, said in
  an interview — the footnote for that page sits at the end of that very
  sentence, not several sentences later and not on a different page. Link the
  page the words actually come from: confirm that the quoted or paraphrased
  words appear there, and use the same language edition or version the source
  drew on. When the exact page cannot be identified, say so in the text
  instead of linking a near match.
- Placement: the reference goes at the end of the sentence it supports, after
  the final punctuation, whenever it can. A reference in the middle of a
  sentence is allowed only when one sentence rests on different pages and the
  clauses cannot be separated; even then, prefer splitting the sentence in two
  so that each reference lands at a sentence end. Never leave a reference in
  the middle of a phrase.
- **The analyzed source never gets a footnote. Not one. (ABSOLUTE
  PRIORITY — ZERO TOLERANCE)** In a document built around one article, post,
  paper, tweet, video, or repository, the source line under the title is the
  only link to that page. No footnote may point at that page: not on the
  first sentence, not on a quotation, not on a figure, not on the publication
  date, not for the author's name, and not in the titled
  `[^label]: <매체>, [<제목>](<URL>), <날짜>` form either. A label such as
  `essay`, `source`, `original`, `post`, or the author's name whose definition
  is the source URL is a defect, and so is the same URL with a trailing slash,
  a tracking parameter, or a different scheme. When a sentence needs the
  author, the date, or the exact wording of the source, say it in the prose;
  the reader already has the source line. Footnotes exist for the pages the
  reader does not already have — never to repeat the page the document is
  about. If you notice this defect in a document you are touching, delete
  every reference and the definition, then reread the sentences to confirm
  they still stand without the mark.
- When the analyzed source quotes or relies on another page and that page was
  also opened and read (an essay quoting an encyclopedia entry, a report citing
  a paper), footnote that page on the sentence that reports the fact. The
  source line covers the essay; the footnote covers the encyclopedia.
- Material the writer fetched to check, extend, or contrast with the source
  is footnoted like any other outside page.
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
  publication date, leave the date out; write no placeholder in its place.
- Footnote definitions follow `## Footnote Spacing` and sit at the end of
  the document after a `---` rule.
- This format is for researched sources. Footnotes that cite a community
  comment (Hacker News, Lobste.rs, GeekNews) keep the bare `<URL>` form
  their skills specify.
- A separate reference-list section is not added on top of the footnotes.
- Claims that could not be confirmed are stated as such in the text, never
  footnoted to a source that does not actually say them.

**Mandatory check before finishing a source-based document:**

1. Scan every paragraph, table row, and list item for numbers, dates, names,
   quotations, and any sentence that rests on a page other than the analyzed
   source.
2. For each one, confirm a footnote reference sits next to it. A sentence
   resting on an outside page with none is a violation, including in the
   summary section.
3. For each footnote, confirm the page it points to was actually read and
   says what the sentence claims.
4. Compare every footnote definition's URL with the URL on the source line.
   If any definition points at that same page, it is a violation: delete the
   definition and every reference to it before doing anything else. This
   check runs on every document you write, enhance, or edit, and it runs
   again after the reaction skills have added their footnotes.
5. Wherever the prose names where something came from, confirm the footnote
   sits at the end of that sentence and links that exact page. Look for
   references stranded mid-sentence and move them to a sentence end.
6. Count the references per paragraph. A paragraph resting on outside pages
   with a single reference at its end means footnotes were written too
   thinly: split them out per sentence. Equally, remove footnotes that only
   repeat the analyzed source sentence by sentence.

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

## Twitter Naming (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**The service is called Twitter. Never X. Not in a document, a heading, a
footnote, a table cell, a chat message, or a commit message.** The user
treats every appearance of X as the service name as a severe defect.

Root cause of a repeated failure: the source (a Korean news article, an
English post, the platform's own page) wrote X or 엑스 or X(옛 트위터), and
the writer mirrored the source's wording instead of the repository's rule.
A source's naming never overrides this rule. When a source says X, the
document says Twitter; when a source says X(옛 트위터) or formerly Twitter,
the document says Twitter and drops the parenthetical.

- Every form is covered: 트위터 is allowed and means the same thing, but
  X, 엑스, X에, X 게시물, X 계정, X(옛 트위터), the X platform, and
  compound names such as a Twitter Article are not. Write Twitter 게시물,
  Twitter 계정, Twitter에 올렸다.
- Tweet URLs use `twitter.com`, never `x.com`. The domain `x.com` may appear
  only where the literal domain is the point, such as a rule about which URLs
  to rewrite.
- Quoting is not an exception. A quotation that contains X as the service
  name is paraphrased in prose or the service name inside it is replaced by
  Twitter. Never keep the source's X for fidelity.
- A different thing that is also written X is not this rule's concern: the
  Tesla Model X, a variable named X, Xbox, Xcode. Do not rename those.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:**

1. Search the text for the capital letter X standing alone, for 엑스, and for
   x.com.
2. For each hit, decide whether it names the service. If it does, rewrite it
   as Twitter now.
3. The format gate of the analyze-article skill fails any document that calls
   the service X in prose. A pass from the gate does not replace this check,
   because the gate recognises only the common phrasings.
4. When the user corrects this once, search every document written in the
   same session for the same failure and fix them all in the same edit.

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

## Terminology (ABSOLUTE PRIORITY — NO EXCEPTIONS — ZERO TOLERANCE)

**Every technical term must be its standard, full, established name.
Clipped, coined, slangy, or loosely translated terms are forbidden in every
document, every heading, every table cell, every footnote, and every chat
message. There is no "it is understandable" exception.**

Root cause of repeated failures: a term was picked because it was quick to
write or sounded close enough, not because it is what the field calls the
thing. The reader pays for that every time: they stop to decode it, they
doubt the writer, and sometimes the sentence now says something else. A
sloppy term in one place poisons trust in the rest of the document.

Forbidden, without exception:

- **Clipped forms** that people say aloud but the field does not write: a
  half-word cut from a longer standard name. Write the whole name.
- **Coined words and ad-hoc shorthand** invented for the document. If the
  field has no settled word, describe the concept in a plain phrase and use
  that same phrase every time.
- **Word-for-word translation** of a technical word. A term that is settled
  in English stays in English. A term that has a settled Korean form uses
  that form. Never pick a Korean word only because a dictionary lists it.
- **Near-synonyms that shift the meaning.** Two words that are loosely
  related are different terms. Use the one that matches the concept.
- **Mixing names for one thing.** One concept gets one term for the whole
  document, headings and footnotes included.
- **Overriding the user's term.** When the user names, corrects, or
  rejects a term, that choice is final for the rest of the conversation and
  for every later document. Apply it everywhere it appears, including
  quotations of code or plans that you reproduce, unless the user says
  otherwise.
- **Unexplained abbreviations.** Write the full name at first use. Never
  invent an abbreviation.

Process, not intention:

1. Before writing a term, ask: is this the name the field writes in its
   documentation? If you are not sure, look it up in the repository's own
   notes or the primary source before using it.
2. When the user corrects one term, search the whole document, and every
   other file you touched this session, for every variant of it. Fix all of
   them in the same edit. Fixing only the sentence the user pointed at is a
   violation.
3. Do not wait to be told twice. A term the user has rejected once must
   never reappear.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:** list every technical noun and verb you used,
and confirm each is the standard full name. Replace each failure now. This
check runs every time, including for short edits and short replies.
