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

For each selected article, invoke the `/analyze-article` skill with the
source URL, the chosen file path, and the GeekNews topic URL as arguments.

Additional context to pass when invoking:
- Never recreate a document that already exists.
- Weave GeekNews comments into the document body as substantive content —
  do NOT add a standalone `[GeekNews 댓글]` link anywhere in the file.
- Use the fetched GeekNews comments to enrich the `## 분석` or `## 비평`
  sections. When the text explicitly references those comments (e.g.,
  "댓글에서 제기된 우려"), render the reference as an inline hyperlink:
  `[GeekNews 댓글](URL)에서 제기된 우려`.
- Only add the `[GeekNews 댓글](URL)` link when the body text actually
  mentions the comments. If no comment is referenced, omit the link entirely.

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
