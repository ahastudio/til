---
name: llm-wiki
description:
  Build or refresh a `_wiki/<slug>/` mini-wiki for one topic by searching the
  entire TIL repository for related notes, discovering the topic's natural
  sub-themes, and compiling them into an index page plus linked sub-pages.
  Re-running on the same topic re-scans the whole repository, updates pages
  with anything new, re-clusters sub-pages if the natural grouping has
  shifted, and prunes content no longer backed by source notes. Use when the
  user wants a standing knowledge-base for a topic, distinct from a one-off
  article analysis.
argument-hint: '<topic sentence>'
disable-model-invocation: true
---

Compile a small multi-page wiki under `_wiki/<slug>/` for one topic by
finding every relevant TIL note across the repository (regardless of which
folder it lives in), discovering the sub-themes those notes naturally form,
and synthesizing them into an index page plus linked sub-pages — Karpathy's
"LLM Wiki" pattern applied to this repository.

## Usage

```text
/llm-wiki Claude Code에서 커스텀 서브에이전트를 만들고 조율하는 방법
/llm-wiki RAG 없이 LLM 에이전트가 지식을 축적하는 패턴들
```

- Argument: the topic, as a full, specific sentence — not a bare keyword.
  The sentence sets the scope: it tells this skill what counts as relevant
  and what doesn't. If the user gives only a short keyword, ask them to
  restate it as a fuller sentence before proceeding.
- Standing topic sentences already agreed with the user are recorded in
  `AGENTS.md` under "LLM Wiki Topics". Check there first — reuse an existing
  entry's exact wording rather than inventing a new phrasing for the same
  topic.

## Core rule: this always re-compiles from scratch

There is no separate "first run" vs "update" mode. Every invocation:

1. Re-searches the entire repository for notes relevant to the topic
   sentence, not just what the existing wiki pages already cite.
2. Re-derives the sub-theme clustering from that fresh source set — the
   previous page split is a hint, not a fixed skeleton.
3. Rebuilds each page's content set from the current cluster.
4. Removes claims/sections/pages whose source notes were deleted,
   reorganized, or no longer support them.

Treat the previous `_wiki/<slug>/` directory (if any) as a draft to revise,
not as a fixed structure to append to. The source notes are the ground
truth; the wiki pages are a compiled artifact that must stay in sync with
them.

## Procedure

### 1. Derive the topic slug and target directory

From the topic sentence, derive a short kebab-case slug that captures the
core subject (e.g. "Claude Code에서 커스텀 서브에이전트를 만들고 조율하는
방법" → `claude-code-subagents`). Target directory: `_wiki/<slug>/`, with
`_wiki/<slug>/index.md` as the entry page.

Check `_wiki/` for an existing directory covering the same or a
near-duplicate topic (Glob `_wiki/*/index.md`, read topic lines). If a close
match exists, reuse that exact directory instead of creating a
near-duplicate wiki — this keeps `_wiki/` a small set of topics, not one
directory per invocation.

### 2. Search the repository for relevant notes

Search broadly and by multiple angles — do not rely on a single grep
pattern. Use Explore (or direct Glob/Grep for quick lookups) across the
whole repository, ignoring folder boundaries:

- Keyword search on the topic's key terms and close synonyms (English and
  Korean forms — this repo mixes both).
- Search for the topic's key tools/products/APIs by name.
- If wiki pages already exist for this slug, re-check each cited file still
  exists and still supports its claim.

For each candidate file found, judge relevance against the topic sentence —
not against a loose keyword match. A file that merely mentions a keyword in
passing is not automatically in scope; a file that substantively informs the
topic sentence is.

### 3. Read and extract

Read each relevant file (or the relevant sections of long files). Extract:

- Concrete facts, patterns, opinions, and critiques bearing on the topic.
- The file's path, so wiki pages can cite it.

### 4. Discover sub-themes

Do not impose a fixed template (e.g. "concepts / cases / criteria") on every
topic. Instead, let the sub-themes emerge from what the source notes
actually cluster around — recurring entities, recurring failure modes,
recurring points of disagreement, natural phases of a workflow, whatever the
material itself groups into.

Aim for 3–7 sub-pages. Fewer than that usually means the topic didn't need
splitting (reconsider whether a single page would serve better — see step
6). More than that usually means some clusters should merge.

Each source note may inform more than one sub-page if it substantively
speaks to more than one sub-theme.

### 5. Compile the pages

Write in Korean, following `.agent/rules/writing-guidelines.md`.

**`_wiki/<slug>/index.md`:**

```markdown
# <Topic title>

주제: <the topic sentence, verbatim or lightly cleaned up>

## 개요

<3-5 sentence synthesis of what this repository's notes collectively say
about the topic, and how the sub-pages below relate to each other>

## 하위 주제

- [<sub-page title>](<sub-page-slug>.md) — <1-line description of what it
  covers and why it's split out>
- ...
```

**Each `_wiki/<slug>/<sub-page-slug>.md`:**

```markdown
# <Sub-page title>

[← <Topic title>](index.md)

<synthesized content for this sub-theme, organized by point not by walking
through source files one at a time>

## 출처

- [<note title or path>](<relative path from repo root>)
- ...
```

Rules for the body:

- Organize by sub-theme, not by walking through source files one at a time.
  A wiki page is a synthesis, not a list of summaries.
- Where source notes disagree or take different angles, say so explicitly —
  that tension is valuable, don't flatten it.
- Cite the source note's relative path inline (as a markdown link) at the
  point a specific claim draws on it, in addition to the `## 출처` list at
  the end.
- Cross-link sub-pages to each other where their content genuinely relates
  (`[관련: <title>](<slug>.md)`) — this is what makes it a wiki rather than
  a set of independent documents.
- Do not quote large blocks verbatim from source notes — synthesize in your
  own words. Short direct quotes are fine when the original phrasing
  matters.
- Keep each page as short as it can be while still covering its sub-theme
  substantively. This is a living reference, not an exhaustive archive —
  favor tight, well-organized pages over long ones.

### 6. Re-cluster if needed

If this is a re-run and the freshly-derived sub-themes no longer match the
existing page split:

- Merge pages whose sub-themes have converged.
- Split a page whose sub-theme has grown into two distinct ones.
- Rename a page whose scope has drifted from its original title.
- If the topic turns out too thin to sustain multiple pages, collapse back
  to a single `_wiki/<slug>/index.md` with no sub-pages.

Delete sub-page files that no longer correspond to any current cluster —
don't leave orphaned pages behind. Update `index.md`'s "하위 주제" list to
match the final set exactly.

### 7. Prune

After drafting, re-check every page and every `## 출처` entry against the
current repository state:

- If a cited file no longer exists or no longer supports the claim, remove
  or rewrite that part.
- If a sub-page's source notes turn out to be thin (one weak mention) and it
  doesn't hold up on its own, fold it into a related sub-page or cut it
  rather than padding it out.
- If a cross-link points to a page that was merged or deleted in step 6,
  fix or remove it.

Do not keep content "just in case" — an unused or unsupported claim is worse
than a shorter wiki. This pruning step is not optional; run it every time,
even when the wiki is new.

### 8. Report

Tell the user, briefly: the target directory, the sub-pages produced, how
many source notes were used, and — on a re-run — what changed (added /
updated / merged / split / pruned), not just that the wiki was refreshed.
