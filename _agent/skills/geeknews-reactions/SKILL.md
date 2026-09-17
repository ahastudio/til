---
name: geeknews-reactions
description:
  Find the GeekNews (news.hada.io) discussion for the article in the current
  TIL document and weave the key native GN comments into the document body
  with precise footnote links. Use when the user wants to reflect community
  reactions from GeekNews into an existing TIL file.
argument-hint: '[file-path]'
---

Find the GeekNews discussion for a TIL document's source article and enrich
the document with key GN-native community reactions, each linked to the exact
comment.

**This skill must actually run to completion every time it is invoked — NO
EXCEPTIONS.** GeekNews requires a browser (no public search API), which
makes it the easiest of the three reaction skills to skip under time
pressure or when a queue is long. Skipping it, or declaring "probably no
thread" without searching, is a defect. Every invocation must end in one of
two concrete states, ever:

- A GN thread was found and searched for native comments (woven in, or
  confirmed none worth weaving), with the `GN 토론:` line added.
- No matching GN thread exists after an actual search with narrower/broader
  keyword variants — report this explicitly ("GN 스레드 없음 확인") rather
  than silently omitting any mention of GN.

Never substitute "I already checked HN/Lobste.rs" for actually searching
GN — each platform is searched independently, because GN's own userbase and
discussion patterns differ from HN's and Lobste.rs's, and a thread on one
platform says nothing about whether one exists on another.

## Usage

```text
/geeknews-reactions
/geeknews-reactions mac/some-tool.md
```

- Argument: path to an existing TIL file (optional; if omitted, use the file
  currently open in the IDE, or ask the user)

## Procedure

### 1. Identify the source URL and any existing GN link

Read the target TIL file. Extract the source URL from the `원문:` line (or
the first link at the top of the document).

If the document already has a `GN 토론:` line, use that URL directly and
skip to step 3.

### 2. Find the GN discussion

Two things about GeekNews, both verified:

- **`/search?q=...` is JavaScript-rendered.** `curl` and `WebFetch` both get
  the page shell with zero results and HTTP 200. An empty result from it is
  not evidence of absence (see `web-fetching.md`, «An Empty Result Is Not a
  Result»). The shell is also the **same size for every query** — roughly
  52KB whether the term has 484 hits or none — so a length or diff heuristic
  will not reveal that the search never ran.
- **Topic pages are NOT JavaScript-rendered.** `https://news.hada.io/topic?id=N`
  returns full server-rendered HTML including every comment and its `cid`
  anchor. No browser is needed for step 3.

So the browser is only ever needed for *finding* the topic id, and there is a
better way to do that.

#### Strategy A — web search restricted to the domain (primary)

Use the `WebSearch` tool with `allowed_domains: ["news.hada.io"]`. GN titles
are Korean, so search Korean keywords describing the article, not the English
title:

```text
WebSearch(query: "<한국어 주제 키워드>", allowed_domains: ["news.hada.io"])
```

This returns `news.hada.io/topic?id=NNNNN` URLs with their Korean titles.
Try two or three phrasings — a literal rendering of the title, and a
description of what the thing does — because GN titles are frequently
rewritten rather than translated.

#### Strategy B — browser (only if Strategy A fails)

Per `web-fetching.md`, use Claude in Chrome; fall back to `agent-browser`
only when Chrome is not connected, and say so:

```text
agent-browser open "https://news.hada.io/search?q=<keywords>"
agent-browser snapshot -i
```

Read the rendered result count, not the HTML. A search that ran shows
`검색결과 약 N개(0.NN초)` near the top; extract that line and the
`topic?id=` links beneath it.

**Wait before concluding zero.** Immediately after navigation the count line
is often absent because the results have not been injected yet, and that
state is indistinguishable from a genuine zero. Before reporting absence,
wait ~2–3 seconds, re-read, and require one of these two:

- the `검색결과 약 N개` line with a count, and no matching topic among the
  results, or
- an explicit no-result phrase in the body (`결과가 없`, `일치하는`,
  `찾을 수 없`).

If neither is present, the page has not finished rendering — read it again
rather than writing a conclusion.

**Run a control query.** `ripgrep` returns ~484 results through this path.
If a control returns nothing, the search is not running and no negative
conclusion may be drawn from that session.

#### Verify the match

Fetch the topic page (step 3) and confirm the source URL appears in it. A
matching title is not enough — GN carries many topics on the same subject
from different sources.

If nothing matches after both strategies, report that and stop — do not
guess a topic id.

**Never sweep a range of topic ids.** Fetching topic pages sequentially to
hunt for one triggers an IP-level block: GN starts returning HTTP 403 with a
10-byte body for every request, across every language subdomain
(`es.`, `ja.`, …), and it persists for hours. This has already cost a
session the ability to read GN at all. If you are tempted to scan ids,
Strategy A is the answer instead.

### 3. Fetch the discussion page and comment anchors

Plain HTTP with a browser User-Agent is enough:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
curl -s -A "$UA" "https://news.hada.io/topic?id=<topic-id>" | python3 -c "
import re,sys,html
h=sys.stdin.read()
print('출처 URL 포함:', '<source-domain>' in h)
parts=re.split(r\"id=['\\\"]?(cid\d+)['\\\"]?\", h)
for i in range(1, len(parts), 2):
    t=re.sub(r'<script.*?</script>','',parts[i+1],flags=re.S)
    t=re.sub('<[^>]+>',' ', t)
    t=re.sub(r'\s+',' ', html.unescape(t)).strip()
    t=re.sub(r'^data-comment[^>]*>\s*','',t)
    m=re.search(r'▲\s*(\S+)', t)
    print(parts[i], '|', m.group(1) if m else '?', '::', t[:600])
"
```

Each comment element's `id` attribute (e.g. `cid56704`) is the exact anchor
to use in footnote URLs: `https://news.hada.io/topic?id=<topic-id>#<cid>`.

If this returns HTTP 403 with a tiny body, you are IP-blocked; `WebFetch` on
the same topic URL still returns the comment text and handles, but it strips
HTML attributes, so you will get the comments without their `cid` anchors.
In that state you can read the discussion but cannot footnote it — say so
rather than guessing anchors.

### 4. Filter out re-aggregated HN/Lobste.rs comments

GN topic pages often embed a "Hacker News 의견들" or "Lobste.rs 의견들"
block that just republishes comments from those other sites (attributed to
the `GN⁺` account, not a real GN user). These are NOT native GN reactions.

- Skip any comment block introduced by "Hacker News 의견들" or
  "Lobste.rs 의견들" headings.
- Only consider comments posted by real GN usernames (not `GN⁺`) as
  candidates for step 5.
- If the document already has `/hackernews-reactions` or
  `/lobsters-reactions` footnotes covering the same underlying quote, treat
  it as already covered and skip it — do not duplicate the same reaction
  under a new GN footnote just because GN also republished it.

### 5. Select significant comments

Identify native GN comments that add something not already in the TIL
document. Criteria:

- A concrete counter-argument, counter-example, or rebuttal
- A real-world anecdote, case study, or hands-on usage report (GN threads
  often include Korean users' first-hand trial results)
- A useful distinction or re-framing of the article's concepts
- A notable criticism of the article's logic or scope
- A well-received alternative interpretation

Skip: pure praise, off-topic jokes, one-liners with no substance, or content
already covered in the document (including content already covered via
`/hackernews-reactions` or `/lobsters-reactions`).

Aim for 3–8 comments — GN threads are typically much smaller than HN ones.
Quality over quantity; it is fine to integrate fewer than 5 if that is all
the thread offers.

### 6. Add the GN link to the document header

If the document does not already have a `GN 토론:` line, add it after any
existing `HN 토론:` / `Lobste.rs 토론:` lines, otherwise immediately after
the `원문:` line:

```markdown
GN 토론: <https://news.hada.io/topic?id=TOPIC_ID>
```

### 7. Weave reactions into the document body

For each selected comment, integrate it into the most relevant existing
section (`## 분석`, `## 비평`, or `## 인사이트`). Rules:

- Do NOT add a new top-level section for GN comments in general — integrate
  inline: expand an existing paragraph, add a new sub-section (###), or add
  a new paragraph within an existing sub-section.
- A new sub-section (e.g. `### GN 반응: ...`) is acceptable when the
  reaction is a distinct, self-contained anecdote that does not fit
  naturally into an existing paragraph — follow the existing document's own
  precedent for this.
- Use a footnote reference in the body text and add the exact comment URL
  at the bottom of the file.
- The footnote URL must point to the specific comment using its `cid` as
  the anchor: `https://news.hada.io/topic?id=<topic-id>#<cid>`.
- Write the reaction content in Korean (GN comments are usually already in
  Korean — keep the meaning faithful rather than translating loosely). The
  commenter's handle stays in its original form.
- If a footnote key conflicts with an existing one (e.g. from a prior
  `/hackernews-reactions` or `/lobsters-reactions` run), disambiguate with
  a `gn-` prefix or descriptive suffix, e.g. `[^gn-handle-topic]`.
- When a question-and-answer pair between two GN users is being reflected,
  use separate footnotes for each comment rather than one footnote covering
  both — each must point to its own `cid`.

Footnote block format (at the very end of the file, after `---`):

```markdown
---

[^gn-handle]: <https://news.hada.io/topic?id=TOPIC_ID#cidCOMMENT_ID>
```

If footnotes already exist, append new ones to the existing block.

### 8. Writing rules

- Follow all writing guidelines in AGENTS.md, including `writing-guidelines.md`
  (natural Korean, sentence-per-line body text, heading spacing, etc.).
- Do not alter sections that have no relevant GN reactions.
- Do not remove or rewrite existing content — only add or extend.
- New content must match the tone and depth of the existing document.
- Each integrated reaction should make the document richer, not longer for
  its own sake.
