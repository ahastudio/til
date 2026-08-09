---
name: analyze-article
description:
  Read a web source — an article OR a non-article (GitHub repo, project
  homepage, service site) — and write a TIL document (in Korean) with
  analysis, critique, and insights. The H1 title is written in Korean.
  Published pieces (articles, posts, papers, tweets, videos) get a
  `원문: [원문 제목](URL)` titled-link source line and a `## 요약` section;
  non-articles get bare `<URL>` line(s) with NO `원문:` label, no titled link,
  and a fitting first heading like `## 소개`. Takes a URL as an argument. Use
  when the user asks to analyze an article/repo/site, document it, or organize
  a technical post.
argument-hint: '<url> [output-path]'
disable-model-invocation: true
---

Read a web article and write a TIL document
with a summary / analysis / critique / insights structure.

**The output document MUST be written in Korean.**
All section content (summary, analysis, critique, insights) is
written in Korean.
Technical terms may be written alongside their original English form.

## Usage

```text
/analyze-article https://example.com/article [security/article-name.md]
```

- First argument: source URL (required)
- Second argument: output file path (optional; if omitted, ask the user)

### Multiple URLs in one invocation

The user often pastes several URLs at once, sometimes each on its own
`/analyze-article` line. Treat that as a queue, not as an error.

- Run the full procedure below once per URL, in the order given.
- Finish one document completely — write, quote-convert, weave community
  reactions — before starting the next. Do NOT write all summaries first and
  circle back.
- If a URL turns out to be a duplicate or cannot be fetched, report that one
  and continue to the next. A single failure never aborts the queue.
- Report at the end as a table: one row per URL, with the resulting path or
  the reason it was skipped.
- If the queue is long enough that finishing it in one run is implausible,
  say so up front with a count, then start working through it in order
  rather than waiting for permission.

## Procedure

### 1. Fetch the source

Fetch the content of the $0 URL with WebFetch.

If WebFetch returns a summary rather than the text, or returns too little to
summarize accurately, fetch again asking for the body verbatim, or retrieve
the page directly and strip the markup. Never write the 요약 section from a
thin summary — numbers, names, and quoted phrasing must come from the actual
text. For sources WebFetch cannot handle, see step 4a and
`_agent/rules/web-fetching.md`.

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

### 3. Classify the subject — article vs. non-article (CRITICAL)

**Before writing anything, decide what the source actually IS. This decision
controls the source-link line AND the first section heading. Getting it wrong
is a defect, not a style choice.**

There are two kinds of subjects:

- **Article / blog post / news / paper** — the source is a *piece of writing*
  by an author making an argument. Examples: a blog post, a newsletter issue,
  a news story, an academic paper, an essay, a documentation *article* that
  reads as prose.

- **Non-article** — the source is a *thing you use or explore*, not a piece of
  writing. Examples: a GitHub repository, a project/product homepage, a
  library or framework landing page, a service marketing site, an API
  reference index, a tool's docs root.

When in doubt, ask: "Is there an author advancing a thesis I can summarize, or
am I describing a tool/project/site?" A README that pitches a product is a
**non-article** (it describes the project), even though it contains prose.

### 3a. Document title (H1) — write it in Korean

**The `#` heading is written in Korean, not copied from the source.**
The document is a Korean note; its title is the first thing the reader sees
and must read as Korean prose.

- Convey what the source is about. Do not transliterate the English title into
  Hangul, and do not paste the original title as the H1.
- Keep product names, project names, and established technical terms in their
  original form: `SwiftUI`, `ClickHouse`, `Soppo`, `PostgreSQL`, `MCP`.
  Translate the surrounding words, not these.
- A `<제품명>: <한국어 설명>` shape works well when the subject is a named
  thing. A plain Korean sentence or noun phrase works well when the subject is
  an argument.
- If the source title carries a claim, the Korean H1 should carry that claim
  too — do not flatten it into a neutral topic label.

Examples:

| 원문 제목                                        | H1                                            |
| ------------------------------------------------ | --------------------------------------------- |
| SwiftUI After 7 Years: A Story of Mediocrity      | SwiftUI 7년, 평범함의 기록                    |
| Devtools must be open source                      | 개발 도구는 오픈소스여야 한다                 |
| GitHub has alternatives, but no replacement       | GitHub에는 대안이 있지만 대체재는 없다        |
| Soppo (project homepage)                          | Soppo: Go에 빠진 기능을 더한 언어             |
| The next chapter of our AI momentum               | Google AI 모멘텀의 다음 장                    |

This rule governs the H1 only. Two things stay in their original language:

- The `원문:` link text keeps the source's own title, untranslated (step 4).
- The file name stays lowercase English kebab-case.

If the H1 is in English, the document is wrong regardless of how good the body
is. Fix it before writing the first section.

**This rule applies to documents written from now on only.** Many existing TIL
documents have English H1 titles. That is a settled decision, not a backlog:
do NOT retitle them, and do NOT propose a sweep. Touch an existing H1 only
when the user asks for that specific file.

### 4. Source-link line — STRICT RULE (NO EXCEPTIONS)

**This is the rule most often gotten wrong. Follow it exactly.**

The link form depends on whether the subject is a **published piece** (an
article, post, paper, tweet, or video) or a **thing** (a site address, a
GitHub repository, a project homepage).

- **Published piece** → labeled source line directly under the title, written
  as a **titled markdown link** with the source's own title as the link text:

  ```markdown
  원문: [<원문 제목>](<URL>)
  ```

  Use the title exactly as the source presents it, including its site suffix
  when the page title carries one (e.g. `... | Google Search Central Blog`).
  Do not translate it, do not shorten it, do not invent one. If the page has
  no usable title, use the most specific heading on the page.
  A bare `<URL>` here is a defect: the reader cannot tell what they are about
  to open.

- **Non-article (GitHub repo, homepage, service site, etc.)** → **NEVER write
  `원문:`, and NEVER use a titled link.** An `원문:` label means "original
  *writing*," which a repo or homepage is not. Place the **bare URL(s)** under
  the title with no label and no link text:

  ```markdown
  <https://github.com/org/project>
  ```

  If the subject has both a homepage and a repo, list both as separate bare
  URL lines (homepage first, then repo), each on its own line separated by a
  blank line.

There is ZERO case where a GitHub repository or a product/service homepage
gets an `원문:` label or a `[text](url)` link. If you catch yourself typing
either one for a repo or a homepage, STOP — you misclassified the subject in
step 3.

**Checklist before writing the source line:**

1. Is the subject a published piece or a thing?
2. Published piece → `원문: [실제 제목](URL)`, never a bare `<URL>`.
3. Thing → bare `<URL>`, never `원문:` and never `[text](url)`.

If any answer is wrong, fix it before writing the first section.

Discussion links added later (`HN 토론:`, `Lobste.rs 토론:`, `GN 토론:`) also
keep the bare `<URL>` form, because their score/comment count already
identifies them.

### 4a. Special source types

Some sources need a fetch strategy or a link form of their own. Handle these
explicitly rather than improvising.

| Source type       | Fetch method                              | Source line                                  |
| ----------------- | ----------------------------------------- | -------------------------------------------- |
| Twitter / X       | `agent-browser` (see `web-fetching.md`)   | `트윗: [<제목 또는 첫 문장>](URL)`           |
| YouTube           | Transcript or description via WebFetch     | `영상: [<영상 제목>](URL)`                   |
| Paper (PDF/arXiv) | WebFetch, or Read the PDF                  | `논문: [<논문 제목>](URL)`                   |
| Press release     | WebFetch                                   | `원문: [<제목>](URL)`                        |

For Twitter / X, `twitter.com` is used instead of `x.com` per
`writing-guidelines.md`. For a long tweet, call it a `트윗`, not a `스레드`,
unless the user says otherwise.

For YouTube, the first section is `## 요약` only if the video advances an
argument (a talk, an essay video). For a demo or a walkthrough, choose a
heading that fits — e.g. `## 내용`, `## 데모`.

If the source cannot be fetched at all, STOP and tell the user which URL
failed and what was tried. Never write a document from the title alone or
from prior knowledge of the subject.

### 5. Choose the first section heading

The first top-level section depends on the same classification:

- **Article** → `## 요약` (summary).
- **Non-article** → do NOT use `## 요약`. Choose a heading that fits what the
  section actually covers — e.g. `## 소개`, `## 명세`, `## 사용법`,
  `## 주요 기능`, `## CLI`. A single subject may warrant multiple top-level
  sections if its content naturally splits.

Regardless of subject type, always include `## 분석`, then `## 비평`
immediately after, and end with `## 인사이트`.

### 6. Write the document

Write a markdown document with the following structure. **The `원문:` line and
`## 요약` heading shown below apply to ARTICLES ONLY — for non-articles,
substitute per steps 4 and 5.**

```markdown
# <한국어 제목>

원문: [<원문 제목>](<URL>)

## 요약

Summarize the core content in 3-5 paragraphs.
Convey technical details accurately — preserve numbers, names, and
technical terms. Do not editorialize; save judgment for later sections.

## 분석

Analyze the logical structure and context. Go beyond restating what the
article says — ask WHY the argument is structured this way, WHAT it
assumes, and WHERE it connects to broader trends.

Each sub-section (###) should make a distinct analytical point:
- What is the article's core claim, and what does it rest on?
- What historical or technical context explains why this matters now?
- What structural pattern does this represent — and where else does it
  appear?
- What does the author take for granted that deserves scrutiny?

Aim for 3–4 sub-sections. Each sub-section is 2–4 paragraphs.
Do NOT list observations — build an argument within each sub-section.

## 비평

Do NOT use "강점 / 약점" sub-headings. A list of pros and cons is not
critique — it is a summary with opinions attached.

Real critique means: identify a specific flaw in the article's logic,
generalizability, omissions, or framing — and develop that flaw into a
substantive argument with evidence or counter-examples. Each sub-section
targets one such flaw.

Frame sub-headings as focused critical claims, not generic categories:

Good examples:
- "글의 논리는 성공 조건을 숨긴다"
- "저자가 인식하고도 답하지 않은 문제"
- "이 워크플로는 특정 맥락에서만 성립한다"
- "결론의 일반화는 근거 없이 확장된다"

Bad examples (forbidden):
- "강점"
- "약점"
- "한계"
- "긍정적 측면 / 부정적 측면"

Aim for 3–4 sub-sections of 3–5 paragraphs each. The critique must be
harder and sharper than the analysis — find the places where the article
fails to hold up under scrutiny.

## 인사이트

Insights are the most important section. They must offer something the
reader could NOT have obtained by reading the source alone.

Each insight (###) must be developed over 3–5 paragraphs. The sub-heading
names the insight as a declarative claim — not a question or topic label.

Mandatory coverage across the insights:
- A second-order effect or consequence the article does not anticipate
- A historical analogy or structural pattern that reframes the issue
- A tension or trade-off the article glosses over but that will matter
  at scale or over time

What to avoid:
- Restating the article's own conclusions as insights
- Surface-level observations ("this is an important trend")
- Insights that follow directly from the article without adding a new
  frame

Write at least 3 insights. 4 is better if the subject warrants it.
```

### 7. Writing rules

- Follow the writing guidelines in AGENTS.md (heading spacing, table
  alignment, line breaks, etc.).
- Write in Korean. Technical terms may be written alongside their original
  English form.
- The H1 is Korean (step 3a). Every `##` and `###` heading is Korean too.
- Sections are marked with headings, never with bold text. When the first
  section runs long enough to need internal divisions, give those divisions
  real sub-headings at the right level. A bold line standing alone above body
  text is a structural defect, not a formatting choice.
- Each section must do different work: 요약/소개 reports, 분석 explains,
  비평 challenges, 인사이트 extends. Do not let sections overlap.
- The document should read as if written by someone who disagrees with
  parts of the source and has thought carefully about why.
- Maintain the same tone and depth as existing TIL documents.

### 8. Output

If $1 is provided, create the file at that path.
If it is not provided, propose an appropriate directory and filename and
confirm with the user.

### 8a. File name — STRICT RULE (NO EXCEPTIONS)

**The file name is the subject. Nothing else.**

Use lowercase English kebab-case. Include only words that identify which
subject this is. Never include words that state what category, medium, or
kind of artifact the subject is, and never describe what this document does
to the subject.

Name a named thing by its name. Name an argument by its claim. Name a
specific release or incident by its identifier. Add words only to
disambiguate, and only words that narrow the subject.

Keep it short. Do not transliterate Korean; the name stays English even
though the H1 is Korean (step 3a).

**Mandatory check before writing the file:**

1. Read the file name back without the extension.
2. Ask of each word: does it answer *which* thing this is, or *what kind of*
   thing this is?
3. Delete every word that answers the second question.

### 9. Post-processing

After creating the file, invoke the `quotes-curly` skill via the Skill tool
with the output file path as the argument. Show the conversion result to the
user.

### 10. Community reactions

After post-processing, automatically invoke the following two skills in
sequence via the Skill tool, passing the output file path as the argument to
each:

1. `hackernews-reactions` — finds the Hacker News thread and weaves key
   comments into the document.
2. `lobsters-reactions` — finds the Lobste.rs thread and weaves key comments
   into the document.

Run them regardless of whether the user asked. If a skill reports that no
thread was found, that is a normal result — note it briefly and continue to
the next skill.
