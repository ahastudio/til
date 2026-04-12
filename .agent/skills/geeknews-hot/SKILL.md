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
- Fetch the body summary and comments of the GeekNews topic page with
  WebFetch.

### 5. Write the documents

Write each document with the same structure as analyze-article:

```markdown
# Title

> Source: <URL>

## Summary
## Analysis
## Critique
## Insights
```

Create the file in a directory that matches the topic. Criteria for choosing
the directory:
- Refer to the existing TIL directory structure.
- Place it in the most appropriate existing directory.
- If there is no suitable existing directory, do NOT create a new one — ask
  the user.

### 6. Writing rules

- Follow the writing guidelines in AGENTS.md.
- Write in Korean.
- Write insights sharply and richly.
  Cover deep implications, second-order effects, historical analogies, and
  structural patterns — not surface-level observations.
  Write at least 3 insights.
- If GeekNews comments contain meaningful perspectives, reflect them in the
  analysis or critique.
- Never recreate a document that already exists.
