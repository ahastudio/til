---
name: quotes-curly
description:
  Convert ASCII double quotes (") in a markdown file to Unicode curly quotes
  ("\u201c", "\u201d"). Use when the user asks to convert double quotes, apply
  Unicode quotes, or use typographic/curly quotes.
argument-hint: <file-path>
allowed-tools: Bash
---

Convert ASCII double quotes (`"`, U+0022) in a markdown file to Unicode curly
quotes (`\u201c` / `\u201d`).
Double quotes inside fenced code blocks (````...````) are left as plain ASCII
double quotes.

## Usage

```
/quotes-curly path/to/file.md
```

## How to run

1. Run the following Python script against the file path passed as an argument:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/convert_quotes.py $ARGUMENTS
```

2. Show the execution result to the user.
3. Verify the conversion is correct by checking the before/after with
   `git diff`.
