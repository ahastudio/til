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

## Contents

Section titles match the headings below; search for a title to jump to it.

- Usage: `/geeknews-reactions [file-path]`
- 1. Identify the source URL and any existing GN link
- 2. Find the GN discussion: search the GN search box in a real browser (Strategy A); web search alone never proves absence; never sweep topic ids
- Verify the match: the source URL must appear in the topic page
- 3. Fetch the discussion page and comment anchors: topic pages are server-rendered, `cid` anchors
- 4. Filter out re-aggregated HN/Lobste.rs comments: skip the aggregator account
- 5. Select significant comments: native GN comments only
- 6. Add the GN link to the document header
- 7. Weave reactions into the document body: handle footnotes, one permalink per comment
- 8. Writing rules

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

If the document already has a `GN 토론:`, `Show GN:` or `Ask GN:` line,
use that URL directly and skip to step 3.

### 2. Find the GN discussion

Two things about GeekNews, both verified:

- **`/search?q=...` is JavaScript-rendered.** `curl` and `WebFetch` both get
  the page shell with zero results and HTTP 200. An empty result from it is
  not evidence of absence (see the `web-fetching` skill, «An Empty Result Is Not a
  Result»). The shell is also the **same size for every query** — roughly
  52KB whether the term has 484 hits or none — so a length or diff heuristic
  will not reveal that the search never ran.
- **Topic pages are NOT JavaScript-rendered.** `https://news.hada.io/topic?id=N`
  returns full server-rendered HTML including every comment and its `cid`
  anchor. No browser is needed for step 3.

So the browser is needed to *find* the topic id, and a web search engine is
not a substitute for it: in one queue, domain-restricted `WebSearch` reported
no GN thread for six documents whose threads existed, found afterwards through
the GN search box. A negative conclusion from `WebSearch` alone is never
allowed.

#### Strategy A — the GN search box in a real browser (primary)

Per the `web-fetching` skill, use a real browser (Claude in Chrome; fall back to
`agent-browser` only when Chrome is not connected, and say so). Open
`https://news.hada.io/search?q=<keywords>` and read the rendered page, not the
HTML.

Search Korean keywords, because GN titles are Korean and often rewritten
rather than translated. Try at least three phrasings per document: a literal
rendering of the title, the product or project name alone, and a description
of what it does.

To run several phrasings in one call, from a tab already on `news.hada.io`,
load each query in a hidden same-origin iframe, wait about 2.5 seconds, and
read `d.body.innerText` plus the `topic?id=` links:

```javascript
const qs = ["<phrasing 1>", "<phrasing 2>", "<phrasing 3>"];
const res = [];
for (const q of qs) {
  const f = document.createElement("iframe");
  f.style.cssText = "position:fixed;left:-9999px;width:800px;height:600px";
  f.src = "/search?q=" + encodeURIComponent(q);
  document.body.appendChild(f);
  await new Promise(r => f.onload = r);
  await new Promise(r => setTimeout(r, 2500));
  const d = f.contentDocument;
  const count = (d.body.innerText.match(/검색결과 약 \d+개/) || ["no count line"])[0];
  const seen = new Set(), items = [];
  for (const a of d.querySelectorAll("a")) {
    const m = (a.getAttribute("href") || "").match(/topic\?id=(\d+)/);
    if (m && !seen.has(m[1])) { seen.add(m[1]); items.push(m[1] + " " + a.textContent.trim().slice(0, 40)); }
  }
  res.push(q + " [" + count + "] " + items.slice(0, 5).join(" ; "));
  f.remove();
}
res.join("\n").replace(/[?=&]/g, " ")
```

Two limits of that call: keep it to about six queries (the tool times out near
45 seconds), and strip `?`, `=` and `&` from what it returns, because a return
value that looks like query-string data is replaced wholesale with a blocked
notice.

**Wait before concluding zero.** Immediately after loading, the count line is
often absent because the results have not been injected yet, and that state is
indistinguishable from a genuine zero. Before reporting absence, require one of
these two:

- the `검색결과 약 N개` line with a count, and no matching topic among the
  results, or
- an explicit no-result phrase in the body (`결과가 없`, `일치하는`,
  `찾을 수 없`).

If neither is present, the page has not finished rendering — read it again
rather than writing a conclusion.

**Run a control query.** `ripgrep` returns about 500 results through this
path. If the control returns nothing, the search is not running and no
negative conclusion may be drawn from that session.

#### Strategy B — domain-restricted web search (supplement only)

`WebSearch(query: "<한국어 주제 키워드>", allowed_domains: ["news.hada.io"])`
can surface a topic quickly, but its index is incomplete and recent topics are
often missing. Use it to add candidates, never to rule a thread out.

#### Verify the match

Fetch the topic page (step 3) and confirm the source URL appears in it. A
matching title is not enough — GN carries many topics on the same subject
from different sources.

If no candidate's source URL matches after Strategy A with three phrasings and
a passing control query, report that GN has no thread and stop — do not guess a
topic id.

**Never sweep a range of topic ids.** Fetching topic pages sequentially to
hunt for one triggers an IP-level block: GN starts returning HTTP 403 with a
10-byte body for every request, across every language subdomain
(`es.`, `ja.`, …), and it persists for hours. This has already cost a
session the ability to read GN at all. If you are tempted to scan ids,
the GN search box (Strategy A) is the answer instead.

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
In that state read the topic page inside the browser instead: from a tab on
`news.hada.io`, `fetch("/topic?id=<topic-id>")`, parse it with `DOMParser`, and
take every `[id^=cid]` element's `id` and `innerText`. The browser is not
subject to the block the plain HTTP client hit, and the `cid` anchors are
intact. Only if that also fails, read the discussion with `WebFetch` and say
that it cannot be footnoted rather than guessing anchors.

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

If the document already has a `Show GN:` or `Ask GN:` line, that line is
the GN discussion line; do not add a `GN 토론:` line next to it.
Otherwise, if the document does not already have a `GN 토론:` line, add it after any
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

[^gn-other-handle]: <https://news.hada.io/topic?id=TOPIC_ID#cidCOMMENT_ID>
```

Separate every footnote definition from the next with one blank line.
If footnotes already exist, append new ones to the existing block.

### 8. Writing rules

- Follow all writing guidelines in AGENTS.md, including the `writing-guidelines` skill
  (natural Korean, sentence-per-line body text, heading spacing, etc.).
- Do not alter sections that have no relevant GN reactions.
- Do not remove or rewrite existing content — only add or extend.
- New content must match the tone and depth of the existing document.
- Each integrated reaction should make the document richer, not longer for
  its own sake.
