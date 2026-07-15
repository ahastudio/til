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

GeekNews has no public search API, so use `agent-browser` (per
`web-fetching.md`) — GN is a JavaScript-rendered page and WebFetch will not
reliably return comment content.

```text
agent-browser open "https://news.hada.io/search?q=<title-or-domain-keywords>"
agent-browser snapshot -i
```

Look for a topic link whose title matches the source article and whose
target URL matches the source domain. If nothing matches, try narrower or
broader keyword variants (title words, then bare domain). If still not
found, report that to the user and stop — do not guess a topic id.

### 3. Fetch the discussion page and comment anchors

```text
agent-browser open "https://news.hada.io/topic?id=<topic-id>"
agent-browser eval "
  const comments = document.querySelectorAll('[id^=cid]');
  let result = [];
  comments.forEach(c => result.push(c.id + ' :: ' + c.innerText));
  result.join('\n---\n');
"
```

Each comment element's `id` attribute (e.g. `cid56704`) is the exact anchor
to use in footnote URLs: `https://news.hada.io/topic?id=<topic-id>#<cid>`.

Close the browser when done reading (`agent-browser close`).

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
