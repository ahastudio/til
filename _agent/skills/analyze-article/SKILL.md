---
name: analyze-article
description: >-
  Read a web source — an article OR a non-article (GitHub repo, project
  homepage, service site) — and write a TIL document (in Korean). The H1 title
  is written in Korean. Published pieces (articles, posts, papers, tweets,
  videos) get a `원문: [원문 제목](URL)` titled-link source line and a
  `## 요약` section; non-articles get bare URL line(s) with NO `원문:`
  label, no titled link, and a fitting first heading like `## 소개`. Body
  structure follows the source's own job — analytical for a piece that argues,
  practical for one that teaches. The document shape is a closed spec enforced
  by scripts/check_format.py, which must print OK before the file is reported
  as written. Takes a URL as an argument. Use when the user asks to analyze an
  article/repo/site, document it, or organize a technical post.
argument-hint: '<url> [output-path]'
disable-model-invocation: true
---

Read a web source and write a TIL document whose structure follows what the
source is for: analytical when it argues, practical when it teaches.

**The output document MUST be written in Korean.**
Every section is written in Korean, whichever body structure step 5a selects.
Technical terms may be written alongside their original English form.

## Contents

Details live in `references/`, one level below this file. Read the file a step
points to when you reach that step instead of relying on an earlier read.

- Usage, Multiple URLs in one invocation: queue handling, one document at a time
- 1. Fetch the source; 2. Check for duplicates: both are in this file
- 3, 3-1, 3a, 4. Classify the subject and choose the source-link line: [references/subject-and-source-line.md](references/subject-and-source-line.md) (article vs. non-article, product pages, Korean H1, `원문:` vs. bare URL)
- 4a. Special source types: [references/special-sources.md](references/special-sources.md) (Twitter, YouTube with `yt-dlp`, papers, press releases, forum threads)
- 5, 5a, 6, 7. Choose the body structure and write: [references/body-structure.md](references/body-structure.md) (argue vs. teach, both templates) and [references/writing-rules.md](references/writing-rules.md) (line breaks, headings, code fences)
- 7a, 7b. Keep the document shape and the footnotes exact: [references/document-shape-and-footnotes.md](references/document-shape-and-footnotes.md) (closed header, closed section set, footnote rules)
- 8. Output; 8a, 8b, 8c: [references/output-and-gate.md](references/output-and-gate.md) (file name, four post-processing commands, the gate, what it cannot check)
- 9, 10. Community reactions and the final gate: [references/reactions.md](references/reactions.md)

## Non-negotiables

These hold even if only the top of this file is read. The steps below and the
reference files give the full rules.

- Never write from a title, a summary or memory. If the source cannot be read, stop and report.
- Source line: a published piece gets `원문: [제목](<URL>)` (or its labeled variant); a thing (repository, homepage) gets bare URL line(s), never `원문:`.
- The header is closed: H1, one source line, then HN, Lobste.rs, GN lines. The analyzed source never takes a footnote.
- An analytical body carries `## 분석`, `## 비평`, `## 인사이트`, all three, in that order.
- After writing, run the four post-processing commands of step 8b; the last one (`check_format.py`) must print `OK`.
- Then run the three reaction skills on the file, and run `check_format.py` again; the file is finished only when that run prints `OK`, and the report quotes that printed line.

## Progress checklist

Copy this list into the reply and tick it off per document (a queue repeats it per URL).

```text
- [ ] 1. Fetch the source in full (stop and report if unreadable)
- [ ] 2. Duplicate check: URL, proper nouns, directory
- [ ] 3-4a. Classify the subject; choose the source line and the fetch method
- [ ] 5-7b. Choose the body structure; write; check header and footnotes
- [ ] 8. Write the file; run the four post-processing commands; last prints OK
- [ ] 9. Run the three reaction skills on the file
- [ ] 10. Run check_format.py again; finished only on OK
```

## Usage

```text
/analyze-article https://example.com/article [security/article-name.md]
```

- First argument: source URL (required)
- Second argument: output file path (optional; if omitted, choose it yourself
  under step 8 and ask only when step 8 says to)

### Multiple URLs in one invocation

The user often pastes several URLs at once, sometimes each on its own
`/analyze-article` line. Treat that as a queue, not as an error.

- Run the full procedure below once per URL, in the order given.
- Finish one document completely — write, run the post-processing and the
  format gate of step 8b, weave community reactions, run the gate again in
  step 10 — before starting the next. Do NOT write all summaries first and
  circle back.
- A long queue never justifies skipping the gate for a file. A file that has
  not printed `OK` is not finished and does not belong in the summary table.
- If a URL turns out to be a duplicate or cannot be fetched, report that one
  and continue to the next. A single failure never aborts the queue.
- Report at the end as a table: one row per URL, with the resulting path or
  the reason it was skipped.
- If the queue is long enough that finishing it in one run is implausible,
  say so up front with a count, then start working through it in order
  rather than waiting for permission.

## Procedure

Step numbers below keep the labels other skills and the gate refer to
(2, 4a, 8a, 8b, 9, 10 and so on). A heading that lists several labels covers
all of them.

### 1. Fetch the source

Fetch the content of the $0 URL with WebFetch.

If WebFetch returns a summary rather than the text, or returns too little to
summarize accurately, fetch again asking for the body verbatim, or retrieve
the page directly and strip the markup. Never write the 요약 section from a
thin summary — numbers, names, and quoted phrasing must come from the actual
text. For sources WebFetch cannot handle, see step 4a and
`_agent/skills/web-fetching/SKILL.md`.

For a YouTube URL (`youtube.com`, `youtu.be`), skip WebFetch entirely and go
straight to `yt-dlp` as described in step 4a. WebFetch returns only the title.

### 2. Check for duplicates

Check in this order, and do all three before concluding anything:

1. Grep the TIL for the **source URL itself** (and its slug). An existing
   document that already cites the URL is a duplicate, full stop.
2. Grep for distinctive proper nouns from the title and body.
3. List the likely directory to see whether a differently-named document
   covers the same subject.

If a duplicate exists, do NOT skip it and do NOT write a second document on
the same source. Enhance the existing file instead.

Enhancing means: fetch the source again in full, then compare it against the
existing document and add what is missing. Look for content the source
carries that the document never captured, community reactions not yet woven
in, sections the current structure requires but the document lacks, and
passages where the existing text misreads the source — a document written
from a thin fetch often critiques the source for an omission the source does
not actually have. Correct those. Preserve everything already there that is
still accurate, and keep the existing H1 unless the user asks otherwise.
Report which file was enhanced and what was added or corrected.

A near-miss is not a duplicate: a document that merely *mentions* the subject
(e.g. cites the project in passing) does not block a document *about* the
source. Say which case it is when reporting.

### 3, 3-1, 3a, 4. Classify the subject and choose the source-link line

Read [references/subject-and-source-line.md](references/subject-and-source-line.md)
before writing anything. It decides the source-link line and the Korean H1.

- A published piece (article, post, paper, tweet, video) gets
  `원문: [<원문 제목>](<URL>)` or its labeled variant, never a bare URL.
- A thing (GitHub repository, project homepage, service site) gets bare
  `<URL>` line(s) with no label and no link text. Never `원문:`.
- A product page is a source about the product; the document is about the
  product and attributes claims to its maker.
- The H1 is Korean prose that carries the source's claim.

### 4a. Special source types

Twitter, YouTube, papers, press releases and forum threads each have their own
fetch method and source-line label. Read
[references/special-sources.md](references/special-sources.md) for any of them.

- Tweets open in a real browser, never WebFetch. The service is Twitter, never
  X, and tweet URLs use `twitter.com`.
- YouTube is read with `yt-dlp` (info JSON plus one caption track), never
  WebFetch.
- A source that cannot be read at all stops the work: report which URL failed
  and what was tried. Never write from a title or from memory.

### 5, 5a, 6, 7. Choose the body structure and write

Read [references/body-structure.md](references/body-structure.md) for the
headings and the two templates, and
[references/writing-rules.md](references/writing-rules.md) for the prose rules.

- A source that argues gets `## 분석` → `## 비평` → `## 인사이트`, all three, in
  that order. Half of the structure is a defect.
- A source that teaches gets practical headings and may borrow a single
  `## 비평`; it never carries `## 분석` without the other two.
- Prose is sentence-per-line, at most 80 columns (CJK counts as 2), Korean,
  with `한국어(English)` for any ambiguous term.

### 7a, 7b. Keep the document shape and the footnotes exact

Read
[references/document-shape-and-footnotes.md](references/document-shape-and-footnotes.md)
before writing the header and again before finishing.

- The header is closed: H1, one source line, then HN, Lobste.rs, GN lines in
  that order. No other labeled line and no process-report section exists.
- The analyzed source never takes a footnote. Outside pages that were opened
  get titled footnotes. Comment footnotes are bare permalinks that were
  actually observed.


### 8. Output

If $1 is provided, create the file at that path.
If it is not provided, choose the directory and file name yourself: the
directory that already holds the closest existing documents on the subject,
and a file name that follows step 8a. Do not ask the user to confirm it, and
state the chosen path in the report.

Ask the user only when one of these holds:

- **A conflict**: the path you would choose already exists, or an existing
  document that covers the same source or subject would be overwritten or
  duplicated by it.
- **Real doubt**: two or more directories fit equally well and nothing in the
  repository settles which one the user would expect.

In either case ask one short question that names the candidates, then
continue with the answer.


File name rules (step 8a), the four post-processing commands (step 8b) and what
the gate cannot check (step 8c) are in
[references/output-and-gate.md](references/output-and-gate.md). Run the four
commands in this order on every file this skill writes or enhances:

```bash
python3 .claude/skills/quotes-curly/scripts/convert_quotes.py <file>
python3 .claude/skills/analyze-article/scripts/fix_code_spans.py <file>
python3 .claude/skills/analyze-article/scripts/align_tables.py <file>
python3 .claude/skills/analyze-article/scripts/check_format.py <file>
```

The last command must print `OK`. A `FAIL` is not advisory: fix the file and
run it again. Do not edit the gate to make a document pass; if the gate seems
wrong about a rule, say so and stop.

### 9. Community reactions

After the gate prints `OK`, run `hackernews-reactions`, `lobsters-reactions`
and `geeknews-reactions` on the file, in that order, each with the file path as
the argument, even when no thread is expected. Each search is independent: a
result on one platform says nothing about another. A document is not done until
all three have run with a concrete outcome (comments woven in, or no thread
found). Details and the per-file checklist are in
[references/reactions.md](references/reactions.md).

### 10. Run the format gate again

The reaction skills edit the header, the body and the footnotes, so run
`check_format.py` once more after the last one. A document is finished only
when this second run prints `OK`; in a queue, report only files that reached
it.
