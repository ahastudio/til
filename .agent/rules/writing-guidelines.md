---
paths:
  - "**/*.md"
---

# Writing Guidelines

## Heading Spacing

Always add blank lines before and after headings. This is required for markdown
linters and improves readability.

## Table Alignment

When formatting markdown tables with Korean text:

1. Count Korean characters as 2 columns each (same as CJK width rule)
2. Align table pipes by padding cells with spaces
3. Find the longest content in each column
4. Pad shorter cells with trailing spaces to match column width

Example:

```markdown
| 항목   | Description |
| ------ | ----------- |
| 이름   | Name        |
| 설명   | Explanation |
| 작성자 | Author      |
| 상태   | Status      |
```

- "작성자" (3 Korean chars = 6 columns) is longest in left column
- "Explanation" (11 English chars = 11 columns) is longest in right
- All cells padded to match their column's maximum width

## Inline Code Formatting

Wrap code-like tokens in backticks for readability. This applies to
both notes and commit messages. Examples of what to wrap:

- File and directory names: `README.md`, `openai/`, `src/main.py`
- Commands and CLI flags: `git rebase`, `--no-verify`
- Identifiers: function names, variable names, class names
- Technical keywords that refer to code: `return await`, `null`,
  `useState`
- URLs that would otherwise be autolinked when you do not want them
  linked (e.g. `http://127.0.0.1:8080`)

Do not wrap plain prose, product names, or concepts (OpenAI, ESLint,
RLHF) in backticks.

## Fenced Code Block Language

Every fenced code block MUST have a language identifier. No exceptions.

- Use the actual language when known: `bash`, `yaml`, `go`, `python`, etc.
- Use `text` for diagrams, ASCII art, plain output, or anything that has
  no specific language.
- A bare ` ``` ` with no identifier is always wrong.

## Note Document Structure

TIL notes vary by the nature of their subject. Match the section structure to
what the subject actually is, not to a fixed template.

- **Article or blog post** (the subject is a piece of writing):
  Use `## 요약` as the first section.
- **Project, tool, framework, or collection** (the subject is something you
  use or explore):
  Do NOT use `## 요약`. Choose a heading that fits what the section actually
  covers — e.g., `## 소개`, `## 명세`, `## 사용법`, `## 주요 법칙`, `## CLI`.
  A single subject may warrant multiple top-level sections if its content
  naturally splits (e.g., spec + CLI for a tool with both).

Regardless of subject type, always include `## 비평` immediately after
`## 분석`, and end with `## 인사이트`.

## Line Breaks in Body Text

Break body text at sentence boundaries, not at a fixed column width. Each
sentence ends on its own line. Within a single sentence, break at a natural
semantic unit (e.g. before a conjunction or after a clause) only when the
sentence is long enough to warrant it.

**Rules:**

- Every sentence starts on a new line.
- A period (`.`), question mark (`?`), or exclamation mark (`!`) ends the
  line — do not continue the next sentence on the same line.
- For long sentences, break once at the most natural semantic boundary
  (before 이며/하지만/그러나/그리고/하면/때문에 etc.) and continue on the
  next line with NO indentation — indented continuation lines become
  code blocks in most markdown renderers.
- Do NOT break at 80 columns or any other fixed character count.
- This rule applies to all `.md` body text. Code blocks, tables, and list
  items are excluded.

**Example:**

```markdown
Revo는 Zig로 작성된 동적 타입 언어다.
README는 기술 사양보다 사용 경험을 먼저 보여주는 구성이다.
파이프, 패턴 매칭, 채널 루프, 테스트 블록은
Revo를 짧은 시간에 이해시키는 데 효과적이지만,
운영 의사결정자 관점에서 필요한 릴리스 정책은 상대적으로 얇다.
```

## Twitter Links

Always use `twitter.com` instead of `x.com` for tweet URLs.

## Tweet Terminology

Call it a "트윗" unless the user explicitly says "스레드". Long tweets are still
tweets.
