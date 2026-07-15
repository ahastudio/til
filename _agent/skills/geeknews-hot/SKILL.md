---
name: geeknews-hot
description:
  Pick hot articles from GeekNews (news.hada.io) and write a TIL document for
  each. Select top articles by points and only process articles that do not
  duplicate existing documents.
argument-hint: '[count (default 5)]'
disable-model-invocation: true
---

Pick popular GeekNews articles and, for each one, write a TIL document in the
same format as the analyze-article skill.

**Every document this skill produces MUST subsequently be run through
`/hackernews-reactions`, `/lobsters-reactions`, AND `/geeknews-reactions`
(step 6). This is a hard requirement of the skill, not an optional
enrichment — see step 6 for why it is not redundant with step 4.**

## Usage

```text
/geeknews-hot
/geeknews-hot 3
```

- Argument: number of documents to write (default: 5)

## Procedure

### 1. Collect popular articles

Fetch https://news.hada.io/ with WebFetch.
Extract the list of articles ordered by points, highest first.
Collect each article's title, source URL, point count, and GeekNews topic URL.

### 2. Remove duplicates

Use Glob and Grep to search existing TIL documents and exclude any article
that already has a document on the same topic. Judge duplicates by title,
source URL, project name, etc.

After excluding duplicates, pick the requested number of articles by point
order.

### 3. Report the selection

Show the selected list of articles to the user. Format:

```text
1. Title (points) — expected path
2. Title (points) — expected path
...
```

If any articles were excluded, show them along with the reason.

### 4. Gather materials

For each selected article, in parallel:
- Fetch the source URL content with WebFetch.
- Fetch the GeekNews topic page with WebFetch to read the body summary and
  check for external discussion links.

**Comment source determination:** Inspect the GeekNews topic page to see
whether it links to an upstream discussion on Hacker News
(`news.ycombinator.com`) or Lobsters (`lobste.rs`). These links appear as
"HN에서 보기", "Lobsters에서 보기", or similar labels.

- If an upstream HN or Lobsters discussion link is present, fetch that
  upstream discussion page instead of the GeekNews comments. The upstream
  page is the primary reaction source for this article.
- If no upstream link is present, fetch the GeekNews comments as the
  reaction source.

### 5. Write the documents

For each selected article, invoke the `/analyze-article` skill with the
source URL, the chosen file path, and the reaction source URL as arguments.

**Document title:** Do NOT reuse the GeekNews topic title verbatim as the
document's `# ` heading. GeekNews titles are often a translated or edited
paraphrase of the original and can distort the source's actual framing or
emphasis. Read the fetched source content and write a title that reflects
what the source itself says — this may end up identical to the GeekNews
title when that title is already an accurate rendering, but it must be a
deliberate choice based on the source, not a copy-paste default.

Additional context to pass when invoking:
- Never recreate a document that already exists.
- Weave comments from the reaction source into the document body as
  substantive content.
  Do NOT add a standalone inline link to any discussion page anywhere in
  the file.
- Use the fetched comments to enrich the `## 분석`, `## 비평`,
  or `## 인사이트` sections. For each referenced comment, mark the
  reference with a footnote (`[^handle]`) in the body text, using the
  commenter's handle as the footnote key. Write the reaction content in
  Korean; the handle stays in its original form.

**Footnote URL rules by reaction source:**

- **GeekNews** — point to the specific comment using its row id:
  `https://news.hada.io/topic?id=<TOPIC_ID>#cid<COMMENT_ID>`

  Each GeekNews comment row has `id=cid<number>` (e.g. `cid59313`).
  Use that number as the fragment.

- **Hacker News** — point to the specific comment item:
  `https://news.ycombinator.com/item?id=<COMMENT_ID>`

  Each HN comment has its own numeric item id in the DOM.

- **Lobsters** — point to the specific comment anchor:
  `https://lobste.rs/s/<STORY_ID>/<SLUG>#c_<COMMENT_ID>`

  Each Lobsters comment has a unique short id used as the fragment.

- If a footnote key conflicts with one from a prior `/hackernews-reactions`
  or `/lobsters-reactions` run, append `-geeknews` to the key:
  `[^handle-geeknews]`.

Footnote block format (at the very end of the file, after `---`):

```markdown
---

[^handle]: <https://news.hada.io/topic?id=TOPIC_ID#cidCOMMENT_ID>
```

If footnotes already exist, append new ones to the existing block. If no
comment is referenced in the body, omit the footnote block entirely.

### 6. Mandatory post-processing: run `/hackernews-reactions`, `/lobsters-reactions`, and `/geeknews-reactions`

**This step is NOT optional. Skipping it is a failure to complete this
skill, no matter how good the document from step 5 looks.**

For EVERY document written in step 5 — with ZERO exceptions — after it is
written, you MUST invoke all three:

1. the `/hackernews-reactions` skill, then
2. the `/lobsters-reactions` skill, then
3. the `/geeknews-reactions` skill,

passing that document's file path as the argument to each, one after the
other, for that document specifically. This applies regardless of:

- whether step 4 already found and used an upstream HN or Lobsters
  discussion link from the GeekNews topic page,
- whether the reaction source used in step 5 was GeekNews comments, HN, or
  Lobsters,
- how many comments are already woven into the document,
- whether the source is an article or a GitHub repository/project,
- point count, topic, or directory.

Do NOT treat "the GeekNews page already linked to HN" as a substitute for
running `/hackernews-reactions`. Do NOT treat "I already used Lobsters
comments in step 5" as a substitute for running `/lobsters-reactions`. Do
NOT treat "I already used GeekNews comments in step 5" as a substitute for
running `/geeknews-reactions`.
Step 4's upstream-link check and this step serve different purposes: step 4
picks the reaction source to write the first draft with, this step
independently re-searches HN, Lobsters, and GeekNews from scratch for that
same document and enriches it further. They are not redundant with each
other even when they end up finding the same thread — in particular,
`/geeknews-reactions` looks specifically for native GN-user reactions
(hands-on trial reports, Korean-specific context) that are distinct from
whatever HN or Lobsters comments were already woven in, and it filters out
the re-aggregated "Hacker News 의견들" / "Lobste.rs 의견들" blocks that a
GeekNews topic page may already display.

If a document is skipped by mistake, that is a defect — go back and run
all three skills against it before reporting the overall task as done.

All three skills are expected to sometimes find nothing (no matching HN
thread, no matching Lobsters thread, no native GN comments worth weaving
in) — that is a valid outcome and is NOT the same as skipping the step.
Running the skill and it finding nothing is compliant; not running the
skill at all is not.

Only after all three skills have been invoked for every document —
successfully or with a "nothing found" result — is step 5's work for that
document considered complete.

#### Document structure by source type

The structure of each document depends on the nature of the source:

- **Article or blog post** (the subject is a piece of writing):
  Follow the standard `analyze-article` structure. Use `원문: <URL>` for
  the source link and `## 요약` as the first section.

- **GitHub repository or other project/tool** (source URL is
  `github.com/…` or the subject is a software project, framework, or
  library):
  Use a bare URL with no label for the source link.
  Do NOT use `## 요약`. Instead, open with sections that fit what the
  project actually is — for example `## 소개`, `## 아키텍처`, `## 사용법`,
  `## CLI`, `## 주요 기능`, `## 라이선스 및 상태`. Choose headings that
  reflect the content; a single project may warrant multiple top-level
  sections. Then continue with `## 분석`, `## 비평`, and `## 인사이트` as
  usual.

Create the file in a directory that matches the topic. Criteria for choosing
the directory:
- Refer to the existing TIL directory structure.
- Place it in the most appropriate existing directory.
- If there is no suitable existing directory, do NOT create a new one — ask
  the user.
