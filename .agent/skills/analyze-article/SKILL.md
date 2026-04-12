---
name: analyze-article
description:
  Read a web article and write a TIL document (in Korean) that includes a
  summary, analysis, critique, and insights. Takes a URL as an argument. Use
  when the user asks to analyze an article, document it, or organize a
  technical post.
argument-hint: '<url> [output-path]'
disable-model-invocation: true
---

Read a web article and write a TIL document with a summary / analysis /
critique / insights structure.

**The output document MUST be written in Korean.** All section content
(summary, analysis, critique, insights) is written in Korean. Technical terms
may be written alongside their original English form.

## Usage

```text
/analyze-article https://example.com/article [security/article-name.md]
```

- First argument: source URL (required)
- Second argument: output file path (optional; if omitted, ask the user)

## Procedure

### 1. Fetch the source

Fetch the content of the $0 URL with WebFetch.

### 2. Check for duplicates

Use Glob and Grep to check whether a document on the same topic already exists
in the TIL. If one exists, notify the user and stop.

### 3. Write the document

Write a markdown document with the following structure:

```markdown
# Title

원문: <URL>

## 요약

Summarize the core content in 3-5 paragraphs.
Convey technical details accurately.

## 분석

Analyze the logical structure, strength of evidence, and context of the
article.
Point out connections to related technologies or trends.
If there are multiple sub-items, separate each with a sub-heading (###).

## 비평

Evaluate the strengths and weaknesses of the article in a balanced way.
Examine whether the claims are sufficiently supported and whether any
perspectives are missing.
Offer concrete counter-arguments or complementary points.
If there are multiple sub-items, separate each with a sub-heading (###).

## 인사이트

Write sharply and richly.
Each insight MUST be separated with a sub-heading (###) and developed over
3-5 paragraphs.
Cover deep implications, second-order effects, historical analogies, and
structural patterns — not surface-level observations.
Write at least 3 insights.
```

### 4. Writing rules

- Follow the writing guidelines in AGENTS.md (heading spacing, table
  alignment, line breaks, etc.).
- Write in Korean. Technical terms may be written alongside their original
  English form.
- Insights are the most important part of the document. Write them sharply
  and richly so the reader gains an insight they could not have obtained
  from the source alone.
- Maintain the same tone and depth as existing TIL documents.

### 5. Output

If $1 is provided, create the file at that path.
If it is not provided, propose an appropriate directory and filename and
confirm with the user.
