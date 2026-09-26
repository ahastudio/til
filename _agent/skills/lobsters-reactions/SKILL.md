---
name: lobsters-reactions
description:
  Find the Lobste.rs discussion for the article in the current TIL document
  and weave the key comments into the document body with precise footnote links.
  Use when the user wants to reflect community reactions from Lobste.rs into
  an existing TIL file.
argument-hint: '[file-path]'
---

Find the Lobste.rs discussion for a TIL document's source article and enrich
the document with key community reactions, each linked to the exact comment.

**This skill must actually run to completion every time it is invoked — NO
EXCEPTIONS.** Skipping the search, or assuming "this probably isn't a
Lobste.rs kind of article" without actually searching, is a defect. Every
invocation must end in one of three concrete states:

- A matching Lobste.rs story was found and its comments were actually
  fetched and screened (comments woven in, or confirmed none worth
  weaving), with the `Lobste.rs 토론:` line added.
- No matching story exists after the search strategies in step 2 actually
  ran against endpoints that returned real data — report this explicitly
  ("Lobste.rs 스레드 없음 확인") rather than silently omitting any mention
  of Lobste.rs.
- The search could not be performed because every avenue was blocked —
  report that, and say which endpoints were tried. This is NOT the same as
  "no thread exists" and must never be written up as such.

**A zero-result response is not a result.** Lobste.rs serves an anti-bot
challenge with HTTP 200 on several endpoints (see step 2), and a scraper
reads that as "no matches". Before concluding absence, confirm that the
endpoint you used actually returned data.

Never substitute a check of HN or GeekNews for actually searching
Lobste.rs — each platform is searched independently, because a thread
existing (or not) on one platform says nothing about whether one exists on
another.

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

#### The `/search` endpoint is bot-blocked — never conclude from it (ABSOLUTE PRIORITY)

**`https://lobste.rs/search` and `https://lobste.rs/search.json` return an
anti-bot challenge page with HTTP 200, not search results.** The body starts
with `<title>Making sure you're not a bot!</title>`. A link-extraction script
run against that page finds zero stories and looks exactly like a genuine
"no results" — which is how a real 170-point thread with 64 comments was once
reported as "no Lobste.rs thread".

An empty result from `/search` is evidence that the search did not run. It is
never evidence that the thread does not exist. Do not use `/search` as the
basis for any conclusion.

Known endpoint status (verified):

| Endpoint                                | Status  |
| --------------------------------------- | ------- |
| `/search`, `/search.json`               | blocked |
| `/domains/<domain>[.json]`              | blocked |
| `/newest/page/<N>.json`                 | blocked |
| `/newest.json`, `/newest.json?page=N`   | works   |
| `/hottest.json`, `/hottest.json?page=N` | works   |
| `/page/<N>.json`                        | works   |
| `/t/<single-tag>.json`                  | works   |
| `/s/<short_id>.json`                    | works   |
| `/rss`                                  | works   |

Comma-joined tags (`/t/ai,ml.json`) are blocked; use one tag per request.

The table above describes **scripted access** (`curl`, `WebFetch`). Inside a
real browser session the picture differs, and that difference is usable:

| Path in Claude in Chrome | Behavior (verified)                              |
| ------------------------ | ------------------------------------------------ |
| `/domain/<host>`         | 404 if that host was never posted, 200 if it was |
| `/search?q=<keywords>`   | renders real results (`N results for ...`)       |
| `/search?q=<full URL>`   | login wall, not a result set                     |

`/domain/<host>` is the cleanest check that exists for a homepage- or
project-type subject, because it does not depend on how the search tokenizes
your query: the host either has a story or it does not. Fetch it from a page
already on `lobste.rs` (a cross-origin `fetch` from another site is blocked
by CORS), and read the status code.

The login wall on URL-form search is a **"could not search"**, not an
absence. Re-run the query as title keywords instead.


#### Strategy A — web search restricted to the domain (primary)

Use the `WebSearch` tool with `allowed_domains: ["lobste.rs"]` and the
article title plus a distinctive term (author, product, or domain). This
returns story URLs in `/s/<short_id>/<slug>` form, which gives you both the
id and the slug needed for footnote anchors.

```text
WebSearch(query: "<article title> <author or domain>",
          allowed_domains: ["lobste.rs"])
```

Take the `/s/<short_id>/<slug>` hit and go to step 2a to verify it.

#### Strategy B — scan the JSON listings (fallback for recent stories)

If Strategy A returns nothing usable and the article is recent, scan the
listing APIs for a story whose `url` matches the source URL:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
for ep in hottest newest; do
  for p in 1 2 3; do
    curl -s -A "$UA" "https://lobste.rs/$ep.json?page=$p" | python3 -c "
import json,sys
for s in json.load(sys.stdin):
    if '<source-domain>' in (s.get('url') or ''):
        print(s['short_id'], s['comments_url'], s.get('comment_count'))
"
  done
done
```

This only covers stories still on the front pages. Not finding one here says
nothing about older stories.

#### Strategy C — tag listing

If the article's topic maps to a Lobste.rs tag, scan `/t/<tag>.json` the same
way. One tag per request.

### 2a. Verify the match before using it

Fetch `https://lobste.rs/s/<short_id>.json` and confirm that the story's
`url` field equals the source URL from the TIL document. A title that merely
looks similar is not a match — the same title can appear on a different
domain, and the same article can be submitted with a tracking suffix.

The JSON also gives you `comments_url`, which contains the canonical slug
(e.g. `https://lobste.rs/s/1ifr5f/contagion_fear`). Use that slug in footnote
URLs rather than guessing it from the title.

### 2b. Concluding that no thread exists

You may report "Lobste.rs 스레드 없음 확인" only when **both** hold:

1. Strategy A ran and returned no `/s/...` URL whose story `url` matches the
   source.
2. Strategy B (or C) ran against a working JSON endpoint — one that returned
   parseable JSON, not a challenge page.

A `/domain/<host>` 404 read inside Claude in Chrome satisfies both conditions
on its own for a subject whose source URL is that host's own page, since it
answers the question directly rather than through a search index.

If every avenue you tried was blocked, that is a different outcome: say the
search could not be performed and why, rather than reporting absence.

**Sanity check before any negative conclusion:** if you used any HTML
endpoint, run one control query you know should match (e.g. a well-known
story) through the same code path. If the control also returns zero, your
extraction is broken or you are being challenged — fix that before
concluding anything.

### 3. Fetch comments

Fetch the story JSON from the Lobste.rs API to get comments:

```text
https://lobste.rs/s/<story-id>.json
```

This returns the story object with a `comments` array. Each comment has:
- `url`: the canonical permalink for this comment, already anchored
  (`https://lobste.rs/s/<id>/<slug>#c_<short_id>`) — use this for footnotes
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
- **Use each comment's own `url` field from the story JSON, verbatim.** It is
  already the exact permalink, in the form
  `https://lobste.rs/s/<story-id>/<story-slug>#c_<comment-short-id>`.
  Never assemble this URL by hand: Lobste.rs shortens slugs in ways that are
  not derivable from the title (for example `The contagion of fear` becomes
  `contagion_fear`, dropping `the` and `of`), so a constructed link will be
  wrong even when the id is right.
- Write the reaction content in Korean. The commenter's handle stays in its
  original form.
- If a footnote key conflicts with an existing one (e.g. from a prior
  `/hackernews-reactions` run), append `-lobsters` to the key:
  `[^handle-lobsters]`.

Footnote block format (at the very end of the file, after `---`):

```markdown
---

[^handle]: <https://lobste.rs/s/STORY_ID/STORY_SLUG#COMMENT_SHORT_ID>

[^other-handle]: <https://lobste.rs/s/STORY_ID/STORY_SLUG#COMMENT_SHORT_ID>
```

Separate every footnote definition from the next with one blank line.
If footnotes already exist, append new ones to the existing block.

### 7. Writing rules

- Follow all writing guidelines in AGENTS.md.
- Do not alter sections that have no relevant Lobste.rs reactions.
- Do not remove or rewrite existing content — only add or extend.
- New content must match the tone and depth of the existing document.
- Each integrated reaction should make the document richer, not longer for
  its own sake.
