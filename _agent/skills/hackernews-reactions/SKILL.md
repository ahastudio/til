---
name: hackernews-reactions
description:
  Find the Hacker News discussion for the article in the current TIL document
  and weave the key comments into the document body with precise footnote links.
  Use when the user wants to reflect community reactions from Hacker News into
  an existing TIL file.
argument-hint: '[file-path]'
---

Find the Hacker News discussion for a TIL document's source article and enrich
the document with key community reactions, each linked to the exact comment.

**This skill must actually run to completion every time it is invoked — NO
EXCEPTIONS.** Skipping the search, or assuming "this is niche, there's
probably no HN thread" without actually calling the Algolia API, is a
defect. Every invocation must end in one of two concrete states:

- A matching HN story was found and its top-level comments were actually
  fetched and screened (comments woven in, or confirmed none worth
  weaving), with the `HN 토론:` line added.
- No matching HN story exists after an actual Algolia search (title, then
  URL, then domain) — report this explicitly ("HN 스레드 없음 확인")
  rather than silently omitting any mention of HN.

Never substitute a check of Lobste.rs or GeekNews for actually searching
HN — each platform is searched independently, because a thread existing (or
not) on one platform says nothing about whether one exists on another.

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

Algolia is a plain JSON API and is not bot-walled, so an empty response here
is usually a genuine absence rather than a blocked request. Confirm it is
before reporting one:

- Read `nbHits`, not just the length of `hits`. `nbHits: 0` with HTTP 200 is
  a real empty result set.
- Search by **URL and by keywords separately.**
  `restrictSearchableAttributes=url` matches only the submitted link, so a
  thread posted under a different URL (a mirror, a `nitter` link, a release
  page) will not appear. A keyword query catches those.
- Keyword queries are fuzzy and will return unrelated stories with a large
  `nbHits`. Check the returned titles and URLs against the actual subject —
  `termcn` returns 13,392 hits, none of them the project.
- If several queries in a row return `nbHits: 0`, run one control
  (`ripgrep` returns ~184 stories) through the same code path before
  concluding.

When several threads exist for one article, note that the highest-scoring one
may have no comments at all. A link to a 0-comment thread is worth little, so
prefer the thread that actually holds the discussion even if it scored lower.

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

**Fetch every id in `kids`, not a prefix.** Slicing the array to the first
20–30 to save time is the most common way this skill produces a thin
document: `kids` is not ordered by quality, and substantive material sits at
the end as often as at the front. Both APIs are unauthenticated JSON with no
rate limit in practice — fetch them all concurrently.

**Then fetch the replies. This is where the best material is.**

A first pass over top-level comments gives you positions. The replies give
you the argument: the rebuttal, the correction, the concrete number, and
very often the article's own author answering a criticism. Every time this
step has been skipped, a second pass later found something that changed the
document.

At minimum, fetch the first level of children under:

- every comment you are considering citing,
- the highest-scoring comments, and
- any comment that reads as a strong objection — objections attract the
  replies that test them.

**Look specifically for the author.** Blog authors routinely turn up in their
own threads, and their reply is the single most citable comment available:
it is a direct response to the criticism you are about to write up. Check
whether any commenter's handle matches the article's author or their
project, and read those first. Citing a critique the author already answered,
without the answer, misrepresents the discussion.

Extract `id`, `by`, and `text` (HTML-unescape the text).

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

[^other-handle]: <https://news.ycombinator.com/item?id=COMMENT_ID>
```

Separate every footnote definition from the next with one blank line.
If footnotes already exist, append new ones to the existing block.

### 7. Writing rules

- Follow all writing guidelines in AGENTS.md.
- Do not alter sections that have no relevant HN reactions.
- Do not remove or rewrite existing content — only add or extend.
- New content must match the tone and depth of the existing document.
- Each integrated reaction should make the document richer, not longer for
  its own sake.
