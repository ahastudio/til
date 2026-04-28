---
name: hackernews-reactions
description:
  Find the Hacker News discussion for the article in the current TIL document
  and weave the key comments into the document body with precise footnote links.
  Use when the user wants to reflect community reactions from Hacker News into
  an existing TIL file.
argument-hint: '[file-path]'
disable-model-invocation: true
---

Find the Hacker News discussion for a TIL document's source article and enrich
the document with key community reactions, each linked to the exact comment.

## Usage

```text
/hackernews-reactions
/hackernews-reactions thinking/some-article.md
```

- Argument: path to an existing TIL file (optional; if omitted, use the file
  currently open in the IDE, or ask the user)

## Procedure

### 1. Identify the source URL

Read the target TIL file. Extract the source URL from the `원문:` line.

### 2. Find the HN discussion

Search for the HN thread using the Algolia HN search API:

```text
https://hn.algolia.com/api/v1/search?query=<encoded-title-or-url>&tags=story
```

Pick the thread with the highest `points`. If multiple threads exist for the
same article, prefer the one with the most comments. If no thread is found,
report that to the user and stop.

### 3. Fetch top-level comments

Fetch the story item from the HN Firebase API to get the `kids` array
(top-level comment IDs):

```text
https://hacker-news.firebaseio.com/v0/item/<story-id>.json
```

Then fetch each top-level comment individually:

```text
https://hacker-news.firebaseio.com/v0/item/<comment-id>.json
```

For comments that have substantive replies, also fetch the first level of
child comments. Extract `id`, `by`, and `text` (HTML-unescape the text).

### 4. Select significant comments

Identify comments that add something not already in the TIL document. Criteria:

- A concrete counter-argument, counter-example, or rebuttal
- A real-world anecdote, case study, or historical example
- A useful distinction or re-framing of the article's concepts
- A notable criticism of the article's logic or scope
- A strongly upvoted alternative interpretation

Skip: pure praise, off-topic jokes, one-liners with no substance, or content
already covered in the document.

Aim for 5–10 comments. Quality over quantity.

### 5. Add the HN link to the document header

If the document does not already have an `HN 토론:` line, add it immediately
after the `원문:` line:

```markdown
HN 토론: <https://news.ycombinator.com/item?id=STORY_ID> (N점, N개 댓글)
```

### 6. Weave reactions into the document body

For each selected comment, integrate it into the most relevant existing
section (`## 분석`, `## 비평`, or `## 인사이트`). Rules:

- Do NOT add a new top-level section for HN comments.
- Integrate inline: expand an existing paragraph, add a new sub-section (###),
  or add a new paragraph within an existing sub-section.
- Use a footnote reference (`[^handle]`) in the body text and add the exact
  comment URL at the bottom of the file.
- The footnote URL must point to the specific comment:
  `https://news.ycombinator.com/item?id=<comment-id>`
- Write the reaction content in Korean. The commenter's handle stays in its
  original form.

Footnote block format (at the very end of the file, after `---`):

```markdown
---

[^handle]: <https://news.ycombinator.com/item?id=COMMENT_ID>
```

If footnotes already exist, append new ones to the existing block.

### 7. Writing rules

- Follow all writing guidelines in AGENTS.md.
- Do not alter sections that have no relevant HN reactions.
- Do not remove or rewrite existing content — only add or extend.
- New content must match the tone and depth of the existing document.
- Each integrated reaction should make the document richer, not longer for
  its own sake.
