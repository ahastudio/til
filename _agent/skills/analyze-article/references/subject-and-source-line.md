# Subject classification and source-link line (steps 3, 3-1, 3a, 4)

## Contents

- [3. Classify the subject — article vs. non-article (CRITICAL)](#3-classify-the-subject-article-vs-non-article-critical)
- [3-1. A product is the subject, its page is only a source (STRICT RULE)](#3-1-a-product-is-the-subject-its-page-is-only-a-source-strict-rule)
- [3a. Document title (H1) — short, plain, easy for a Korean reader](#3a-document-title-h1-short-plain-easy-for-a-korean-reader)
- [4. Source-link line — STRICT RULE (NO EXCEPTIONS)](#4-source-link-line-strict-rule-no-exceptions)
- [4-1. A GitHub repository always brings its project site (ABSOLUTE)](#4-1-a-github-repository-always-brings-its-project-site-absolute)

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

## 3a. Document title (H1) — a name, never a sentence

**The H1 is a LABEL for the document, the way a file name or a book spine is a
label. It names the subject. It is never a sentence, never a claim, never a
verdict, and it never sounds like an analyst saying something clever.**

Root cause of a repeated failure: the title was used to show that the author
understood the source, so it became a one-line thesis ("X는 Y이다", "A는 B로
옮겨 간다", "더 나은 …를"). That is the smart-analyst pose the user finds
repellent. The title carries no insight. The insight goes in `## 분석` and
`## 인사이트`.

Write the H1 by filling one of these shapes, and nothing else:

| Subject                          | Shape                          | Example                               |
| -------------------------------- | ------------------------------ | ------------------------------------- |
| Product, tool, project, release  | `<이름> <공개/출시/정식 출시>`  | `Solid 2.0 정식 출시`                 |
| Named thing with one descriptor  | `<이름>: <무엇인지 명사구>`     | `Soppo: Go에 빠진 기능을 더한 언어`   |
| Incident, outage, vulnerability  | `<대상> <장애/취약점/사고>`     | `Apple 서비스 장애`                   |
| Essay, opinion, argument         | `<주제> <글 종류 명사>`         | `SaaS 바이럴 루프 사례`               |
| Report, benchmark, paper         | `<이름>` or `<이름> <보고/논문>` | `FrontierHarness Eval v1.1`           |
| Log, diary, post-mortem          | `<대상> 개발 로그`              | `The Golden Cut 개발 로그`            |

- The last word of the H1 is a NOUN (`공개`, `장애`, `사례`, `로그`, `방식`,
  `구조`, `가이드`, `비교`, `정리`) or a proper name. Never a verb, an
  adjective, an ending like `~다`, `~이다`, `~한다`, `~든다`, `~간다`, a
  question, or a particle (`~를`, `~에게`, `~에서`).
- One clause. No `~고`, `~지만`, `~며`, `~면서`, no comma list, no second
  claim. At most 50 display columns (Hangul counts 2).
- Say WHAT the document is about. Do not say what you conclude about it. If the
  title would be wrong when the argument turns out false, it is a claim: delete
  it and name the subject instead.
- Keep product names, project names, and established technical terms in their
  original form: `SwiftUI`, `ClickHouse`, `PostgreSQL`, `MCP`.
- English or mixed titles are fine. Do not force a stiff Korean translation and
  do not transliterate the English title into Hangul.
- Do not copy the source's title when it is long, clickbait, or a claim. Restate
  it as a name.
- No wit, no metaphor, no slogan, no rhetorical flourish, no "the end of …",
  no "…의 기록", no "…를 위한 …". Plain labels only.

Forbidden, with the repair:

| Bad (sentence / claim / pose)                   | Good (name)                        |
| ----------------------------------------------- | ---------------------------------- |
| 디자인 도구는 흩어졌고 기준은 밑으로 내려간다   | 디자인 도구의 흩어짐               |
| AI를 잘 쓰려면 시간과 연습이 든다               | AI를 잘 쓰는 기술                  |
| 새 앱 말고 더 나은 오픈소스를                   | 오픈소스 개선 제안                 |
| OpenCode Browse: 내 브라우저를 에이전트에게     | OpenCode Browse: 브라우저 연결 도구 |
| GitHub에는 대안이 있지만 대체재는 없다          | GitHub 대안 정리                   |
| 개발 도구는 오픈소스여야 한다                   | 개발 도구 오픈소스 논쟁            |

**Tone of the title and the whole document: a respectful reader, not a judge.**
The author of the source is a person who wrote something. The document reports
what they wrote and where the evidence stops. It never sneers, scolds, lectures,
issues orders, grades the author, or talks down to the source or the reader.

- Forbidden in titles and prose: contempt and dismissal (`쓰레기`, `엉터리`,
  `허접`, `한심`, `뻔한 소리`), verdicts on the person, commands to the reader
  or the author (`~하라`, `~해야 한다`, `~하지 마라`), sarcasm, rhetorical
  questions, and a know-it-all voice that announces what the source "really"
  means. Quote a harsh word only when a commenter said it, and attribute it.
- Criticism is about the claim and its evidence, in plain polite register:
  `근거가 제시되지 않았다`, `이 문서가 확인하지 못했다`. Never about the
  author's character, competence or motives.
- Write as if the author would read the document. If a sentence would be rude
  said to their face, rewrite it.

Mandatory self-check before saving the file, every time: read the H1 aloud.
If it could be spoken as a sentence ending in `다`, or if a reader could
agree or disagree with it, rewrite it as a name. The gate (`check_format.py`)
fails sentence endings, `~고` joins, particle endings, connectives, stacked
numbers and critique words in the H1, but a passing gate does not prove the
title is a name. The check above does.

This rule governs the H1 only. Two things stay in their original language:

- The `원문:` link text keeps the source's own title, untranslated (step 4).
- The file name stays lowercase English kebab-case.

When the user says a title is wrong, retitle EVERY document written in the same
session in the same pass, then run the gate on all of them. Do not retitle
documents from other days unless the user asks.

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

**A bare address that has only a domain ends with a slash.** Write
`<https://www.google.com/>`, never `<https://www.google.com>`, so
the line reads as an address and not as a stray word. An address that already
has a path takes no added slash: `<http://www.google.com/ncr>`,
`<https://github.com/org/project>`. This applies to every bare `<URL>` source
line (homepages, sites, repositories) and the gate fails a domain-only address
without the slash.

There is ZERO case where a GitHub repository or a product/service homepage
gets an `원문:` label or a `[text](url)` link. If you catch yourself typing
either one for a repo or a homepage, STOP — you misclassified the subject in
step 3.

**Checklist before writing the source line:**

1. Is the subject a published piece or a thing?
2. Published piece → `원문: [실제 제목](URL)`, never a bare `<URL>`.
3. Thing → bare `<URL>`, never `원문:` and never `[text](url)`.

If any answer is wrong, fix it before writing the first section.

### 4-1. A GitHub repository always brings its project site (ABSOLUTE)

**When the subject is a GitHub repository, resolve its website BEFORE writing
anything, read it, and put its address in the header. A repository document
that omits the project site the repository itself points to is a defect.**

Resolve it in this order, and do all of it:

1. Call the GitHub API for the repository and read the `homepage` field:
   `curl -s https://api.github.com/repos/<owner>/<repo>` and take
   `.homepage`. The same response gives the star, fork and issue counts, the
   license, the dates and the language, which the document states with the
   date they were read.
2. If `homepage` is empty or only repeats the repository, read the top of the
   README for links labeled website, docs, home, demo or the product name, and
   check the organization or user profile and the package manifest
   (`package.json`, `pyproject.toml`, `Cargo.toml`) for a `homepage` or `url`
   field.
3. Normalize the address: add `https://` when the field has no scheme, follow
   redirects, and keep the final canonical address without tracking
   parameters (`utm_*`).
4. Open the site and read its first screen and its main sections in full
   (step 1 applies: a thin fetch is not reading). When it needs JavaScript,
   open it in the browser. Docs, pricing and blog sub-pages are optional, and
   the document says which were not opened.
5. Write the header with the site first and the repository second, each a bare
   `<URL>` on its own line:

   ```markdown
   # 이름: 설명

   <https://www.google.com/>

   <https://github.com/org/project>
   ```

   The site is the subject's own page, so it is stated in prose and never takes
   a footnote. Pages the site links to that were opened are outside pages and
   take titled footnotes.
6. State in `## 소개` that the site was read, and attribute what it says to the
   maker. When the site says something the README does not (pricing, funding,
   a hosted service, a claim), say so, and criticize the difference in
   `## 비평`.
7. When no site exists after steps 1 and 2, say so once in `## 소개`
   (`저장소에 홈페이지가 등록되어 있지 않다`) and keep only the repository
   line. A site that cannot be opened is reported with the address and the
   reason, and the address still goes in the header.

The user may also give a project site and ask for its repository, or the
reverse. Resolve the other side the same way: the site's links to GitHub, and
the repository whose `homepage` is the site.

This rule also covers other code hosts (GitLab, Codeberg, Hugging Face): read
the project's website field or its sidebar link.

Discussion links added later (`HN 토론:`, `Lobste.rs 토론:`, `GN 토론:`) also
keep the bare `<URL>` form, because their score/comment count already
identifies them.
