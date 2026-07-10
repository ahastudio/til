---
name: analyze-article
description:
  Read a web source — an article OR a non-article (GitHub repo, project
  homepage, service site) — and write a TIL document (in Korean) with
  analysis, critique, and insights. Articles get a `원문:` source line and a
  `## 요약` section; non-articles get bare URL line(s) with NO `원문:` label
  and a fitting first heading like `## 소개`. Takes a URL as an argument. Use
  when the user asks to analyze an article/repo/site, document it, or organize
  a technical post.
argument-hint: '<url> [output-path]'
disable-model-invocation: true
---

Read a web article and write a TIL document with a summary / analysis /
critique / insights structure.

**The output document MUST be written in Korean.** All section content
(summary, analysis, critique, insights) is written in Korean. Technical terms
may be written alongside their original English form.

## Usage

```text
/analyze-article https://example.com/article [security/article-name.md]
```

- First argument: source URL (required)
- Second argument: output file path (optional; if omitted, ask the user)

## Procedure

### 1. Fetch the source

Fetch the content of the $0 URL with WebFetch.

### 2. Check for duplicates

Use Glob and Grep to check whether a document on the same topic already exists
in the TIL. If one exists, notify the user and stop.

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

### 4. Source-link line — STRICT RULE (NO EXCEPTIONS)

**This is the rule most often gotten wrong. Follow it exactly.**

- **Article** → put a labeled source line directly under the title:

  ```markdown
  원문: <URL>
  ```

- **Non-article (GitHub repo, homepage, service site, etc.)** → **NEVER write
  `원문:`.** An `원문:` label means "original *writing*," which a repo or
  homepage is not. Instead, place the bare URL(s) under the title with no
  label:

  ```markdown
  <https://github.com/org/project>
  ```

  If the subject has both a homepage and a repo, list both as separate bare
  URL lines (homepage first, then repo), each on its own line separated by a
  blank line.

There is ZERO case where a GitHub repository or a product/service homepage
gets an `원문:` label. If you catch yourself typing `원문:` for a repo or a
homepage, STOP — you misclassified the subject in step 3.

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
# Title

원문: <URL>

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
- Each section must do different work: 요약/소개 reports, 분석 explains,
  비평 challenges, 인사이트 extends. Do not let sections overlap.
- The document should read as if written by someone who disagrees with
  parts of the source and has thought carefully about why.
- Maintain the same tone and depth as existing TIL documents.

### 8. Output

If $1 is provided, create the file at that path.
If it is not provided, propose an appropriate directory and filename and
confirm with the user.

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
