---
name: lobsters-reactions
description:
  Find the Lobste.rs discussion for the article in the current TIL document
  and weave the key comments into the document body with precise footnote links.
  Use when the user wants to reflect community reactions from Lobste.rs into
  an existing TIL file.
argument-hint: '[file-path]'
disable-model-invocation: true
---

Find the Lobste.rs discussion for a TIL document's source article and enrich
the document with key community reactions, each linked to the exact comment.

## Usage

```text
/lobsters-reactions
/lobsters-reactions thinking/some-article.md
```

- Argument: path to an existing TIL file (optional; if omitted, use the file
  currently open in the IDE, or ask the user)

## Procedure

### 1. Identify the source URL

Read the target TIL file. Extract the source URL from the `원문:` line.

### 2. Find the Lobste.rs discussion

If the document already has a `Lobste.rs 토론:` line, extract the story ID
from that URL directly and skip to step 3.

Otherwise, try the following search strategies **in order**, stopping as soon
as a matching thread is found:

**Strategy A — search by source URL:**

```text
https://lobste.rs/search?q=<percent-encoded-source-url>&what=stories&order=relevance
```

Example: for `https://example.com/my-article`, search
`https://lobste.rs/search?q=https%3A%2F%2Fexample.com%2Fmy-article&what=stories&order=relevance`

**Strategy B — search by article title keywords:**

Extract 2–4 significant words from the article title and search:

```text
https://lobste.rs/search?q=<title-keywords>&what=stories&order=relevance
```

Use underscores as well as hyphens and spaces, because Lobste.rs story slugs
use underscores (e.g. `towards_understandable_software`).

**Strategy C — search by domain name:**

```text
https://lobste.rs/search?q=<domain-without-tld>&what=stories&order=relevance
```

Example: for `gracefulliberty.com`, search `q=gracefulliberty`.

**Strategy D — search by full domain:**

```text
https://lobste.rs/search?q=<full-domain>&what=stories&order=relevance
```

Example: `q=gracefulliberty.com`.

After each strategy, look for a story whose URL matches the source article.
Pick the thread with the highest score among matches. If all four strategies
return no matching thread, report that to the user and stop.

### 3. Fetch comments

Fetch the story JSON from the Lobste.rs API to get comments:

```text
https://lobste.rs/s/<story-id>.json
```

This returns the story object with a `comments` array. Each comment has:
- `short_id`: unique comment identifier used in anchor URLs
- `commenting_user`: object with `username` field
- `comment`: comment text (HTML)
- `score`: upvote count
- `parent_comment`: short_id of parent (null for top-level)

For top-level comments with substantive replies, also read the first level
of child comments.

### 4. Select significant comments

Identify comments that add something not already in the TIL document. Criteria:

- A concrete counter-argument, counter-example, or rebuttal
- A real-world anecdote, case study, or historical example
- A useful distinction or re-framing of the article's concepts
- A notable criticism of the article's logic or scope
- A high-scored alternative interpretation

Skip: pure praise, off-topic jokes, one-liners with no substance, or content
already covered in the document.

Aim for 5–10 comments. Quality over quantity.

### 5. Add the Lobste.rs link to the document header

If the document does not already have a `Lobste.rs 토론:` line, add it
after the `HN 토론:` line if one exists, otherwise immediately after the
`원문:` line:

```markdown
Lobste.rs 토론: <https://lobste.rs/s/STORY_ID/STORY_SLUG>
```

### 6. Weave reactions into the document body

For each selected comment, integrate it into the most relevant existing
section (`## 분석`, `## 비평`, or `## 인사이트`). Rules:

- Do NOT add a new top-level section for Lobste.rs comments.
- Integrate inline: expand an existing paragraph, add a new sub-section (###),
  or add a new paragraph within an existing sub-section.
- Use a footnote reference (`[^handle]`) in the body text and add the exact
  comment URL at the bottom of the file.
- The footnote URL must point to the specific comment using its `short_id`
  as the anchor:
  `https://lobste.rs/s/<story-id>/<story-slug>#<comment-short-id>`
- Write the reaction content in Korean. The commenter's handle stays in its
  original form.
- If a footnote key conflicts with an existing one (e.g. from a prior
  `/hackernews-reactions` run), append `-lobsters` to the key:
  `[^handle-lobsters]`.

Footnote block format (at the very end of the file, after `---`):

```markdown
---

[^handle]: <https://lobste.rs/s/STORY_ID/STORY_SLUG#COMMENT_SHORT_ID>
```

If footnotes already exist, append new ones to the existing block.

### 7. Writing rules

- Follow all writing guidelines in AGENTS.md.
- Do not alter sections that have no relevant Lobste.rs reactions.
- Do not remove or rewrite existing content — only add or extend.
- New content must match the tone and depth of the existing document.
- Each integrated reaction should make the document richer, not longer for
  its own sake.
