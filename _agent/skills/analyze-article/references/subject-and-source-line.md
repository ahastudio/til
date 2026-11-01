# Subject classification and source-link line (steps 3, 3-1, 3a, 4)

## Contents

- [3. Classify the subject — article vs. non-article (CRITICAL)](#3-classify-the-subject-article-vs-non-article-critical)
- [3-1. A product is the subject, its page is only a source (STRICT RULE)](#3-1-a-product-is-the-subject-its-page-is-only-a-source-strict-rule)
- [3a. Document title (H1) — write it in Korean](#3a-document-title-h1-write-it-in-korean)
- [4. Source-link line — STRICT RULE (NO EXCEPTIONS)](#4-source-link-line-strict-rule-no-exceptions)

## 3. Classify the subject — article vs. non-article (CRITICAL)

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

## 3-1. A product is the subject, its page is only a source (STRICT RULE)

**When the URL is a product's page (a launch page, a product site, a pricing
page, a spec sheet), the document is about the product, not about the page.**
Writing "이 페이지는 …한다", "제품 페이지이다", "페이지의 수치" makes the
document read as a summary of marketing copy, which is the wrong subject.

- Name the subject as the product and its maker. Attribute claims to the
  maker ("제조사는 … 말한다", "회사는 … 주장한다"), never to "the page".
- Organize the body around the product: what it is, its specifications,
  price and availability, how people reacted, what the claims rest on, and
  what to check before buying or adopting. Do not follow the page's own
  section order.
- Everything a maker says about its own product is a claim, and the document
  says so. Separate it from what an independent source, a user report, or the
  document's own calculation shows.
- Other pages that were actually opened (a press release, a localized
  edition, documentation, a terms page, a pricing page of a different tier or
  deployment mode) are outside pages and carry titled footnotes. The product
  page the user gave is the analyzed source and takes no footnote, so what it
  says is stated in prose without one.
- The gate still requires one source line in the header (step 4). Keep the
  bare URL there. Do not label it `원문:` and do not describe it in prose as
  "the page".
- When the user supplies a second page as a supplement (a localized edition),
  treat it as an outside page: footnote it, and say where the two disagree.
- Read an evidence table from the rendered page, not from extracted text.
  Plan tables flatten, and a misaligned column turns a limit into its
  opposite. When extracted text and the rendered table cannot be matched
  with certainty, open the page in the browser and read the cells.

## 3a. Document title (H1) — write it in Korean

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

| 원문 제목                                    | H1                                     |
| -------------------------------------------- | -------------------------------------- |
| SwiftUI After 7 Years: A Story of Mediocrity | SwiftUI 7년, 평범함의 기록             |
| Devtools must be open source                 | 개발 도구는 오픈소스여야 한다          |
| GitHub has alternatives, but no replacement  | GitHub에는 대안이 있지만 대체재는 없다 |
| Soppo (project homepage)                     | Soppo: Go에 빠진 기능을 더한 언어      |
| The next chapter of our AI momentum          | Google AI 모멘텀의 다음 장             |

This rule governs the H1 only. Two things stay in their original language:

- The `원문:` link text keeps the source's own title, untranslated (step 4).
- The file name stays lowercase English kebab-case.

If the H1 is in English, the document is wrong regardless of how good the body
is. Fix it before writing the first section.

**This rule applies to documents written from now on only.** Many existing TIL
documents have English H1 titles. That is a settled decision, not a backlog:
do NOT retitle them, and do NOT propose a sweep. Touch an existing H1 only
when the user asks for that specific file.

## 4. Source-link line — STRICT RULE (NO EXCEPTIONS)

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
