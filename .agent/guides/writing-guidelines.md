# Writing Guidelines

## Markdown Line Length

Keep all markdown documents within 80 columns.
Count Korean characters as 2 columns each (CJK width).
Break lines at natural boundaries (sentence ends, clause breaks).

## Heading Spacing

Always add blank lines before and after headings.
This is required for markdown linters and improves readability.

## Table Alignment

When formatting markdown tables with Korean text:

1. Count Korean characters as 2 columns each (same as CJK width rule)
2. Align table pipes by padding cells with spaces
3. Find the longest content in each column
4. Pad shorter cells with trailing spaces to match column width

Example:

```markdown
| 항목   | Description |
|--------|-------------|
| 이름   | Name        |
| 설명   | Explanation |
| 작성자 | Author      |
| 상태   | Status      |
```

- "작성자" (3 Korean chars = 6 columns) is longest in left column
- "Explanation" (11 English chars = 11 columns) is longest in right
- All cells padded to match their column's maximum width

## Twitter Links

Always use `twitter.com` instead of `x.com` for tweet URLs.

## Tweet Terminology

Call it a "트윗" unless the user explicitly says "스레드".
Long tweets are still tweets.
