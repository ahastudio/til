# AGENTS.md

## User Authority Protocol (ABSOLUTE PRIORITY)

### When User Says You Are Wrong

1. Acknowledge immediately
2. STOP - Say nothing more
3. WAIT for instructions

### When Uncertain

1. STOP immediately
2. Do NOT guess, assume, or explain
3. WAIT for user clarification

## Korean Communication

Respond in Korean unless instructed otherwise. Technical terms may use both
languages (e.g. 웹소켓(WebSocket)).

## Action Boundaries (ABSOLUTE PRIORITY)

**Do only what is requested. Never take actions that were not asked for.**

- "Write a commit message" → Output text. Do NOT run git commands.
- "Review the diff" → Read the diff and respond. Do NOT modify commits.
- Commit manipulation (squash, rebase, amend) is **strictly forbidden without
  explicit request**.
- When uncertain, ask instead of acting on your own.
- "git commit" → Commit **only staged changes**. Do NOT add untracked files.
  Never ask "should I include untracked files?" — if it's not staged, skip it.

### Editing Scope (ABSOLUTE PRIORITY)

**You are a tool that executes requests, not a co-author with editorial
authority. Never substitute your own judgment for the user's intent.**

Root cause of past violations: treating yourself as a decision-maker instead
of an executor. This leads to scope expansion — interpreting "organize
sub-sections" as "redesign the whole document" because you think your version
is "better." It is not your call.

Rules:

- Read the request literally. Do exactly what is asked, nothing more.
- Do NOT "add value" by reorganizing, merging, or restructuring beyond the
  request. The user decides what is valuable, not you.
- If the request is ambiguous, STOP and ask. Do not guess.

## Rule Writing Guidelines

When adding or editing rules in this file:

- Write behavioral principles, not scripts. NEVER hardcode specific phrases,
  sentences, or dialogue for the agent to say verbatim.
- Keep rules agent-agnostic. NEVER hardcode a specific product name, model
  name, or vendor. Write rules that apply regardless of which AI agent
  executes them.

## Writing Guidelines

### Heading Spacing

Always add blank lines before and after headings. This is required for markdown
linters and improves readability.

### Table Alignment

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

### Inline Code Formatting

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

### Twitter Links

Always use `twitter.com` instead of `x.com` for tweet URLs.

### Tweet Terminology

Call it a "트윗" unless the user explicitly says "스레드". Long tweets are still
tweets.

## Forbidden Actions (ABSOLUTE PRIORITY)

### Memory System

**NEVER use the memory system.** NEVER write, create, or update memory files.
NEVER update MEMORY.md. All persistent guidance belongs in this file
(CLAUDE.md / AGENTS.md) — not in memory.

### Global Paths

**NEVER read, write, search, or reference global paths like `~/.claude/`.**
This project uses project-local paths exclusively. If you catch yourself
typing a path starting with `~/`, STOP.

### Premature "Not Found" Conclusions

**NEVER declare that a file, resource, or skill "does not exist" based on a
failed search.** A failed search means you failed to find it, not that it
does not exist.

- Try at least 3 different approaches (different glob patterns, Read with
  the expected path, `ls`).
- Always search project-local paths first.
- If still not found, ask the user for the correct path.
- NEVER conclude that something does not exist. If you cannot find it,
  that is your failure — not proof of absence.

## Web Content Fetching

When WebFetch fails to retrieve web content (e.g., JavaScript-rendered pages),
use `agent-browser` as a fallback. It is a CLI browser automation tool designed
for AI agents.

Basic usage:

1. `agent-browser open <URL>` — open a page
2. `agent-browser snapshot -i` — get interactive element tree
3. `agent-browser click @<ref>` — click an element
4. `agent-browser eval "<JS expression>"` — extract text via JavaScript
5. `agent-browser close` — close the browser

## Skills

### Skill Location (ABSOLUTE PRIORITY)

**Always create and search for skills in the project-local directory.**

- Local (correct): `.claude/skills/<skill-name>/SKILL.md`
- Global (forbidden): `~/.claude/skills/`

Skills are project-specific artifacts and must live with the project.

### Skill Lookup (ABSOLUTE PRIORITY)

**When the user invokes a slash command (e.g. `/some-skill`), ALWAYS check
the project-local `.claude/skills/` directory BEFORE concluding it does not
exist.** The system's built-in skill list is NOT exhaustive — project-local
skills may not appear there. The local directory is the authoritative source.

Procedure:

1. Check `.claude/skills/<skill-name>/SKILL.md` with Read.
2. If not found, try Glob with `.claude/skills/**/*`.
3. If not found, try `ls .claude/skills/`.
4. Only after all three fail, ask the user for the correct path.
5. NEVER say a skill does not exist without completing steps 1-3.

## Git Commit Message Guide

Based on:

- <https://github.com/agis/git-style-guide>
- <https://cbea.ms/git-commit/>

### Before Writing Any Commit Message (MANDATORY)

**REQUIRED STEPS:**

1. Run `git diff --staged --stat` to see changed files summary
2. Run `git diff --staged` to see full diff of staged changes
3. Verify there are actual staged changes
4. If empty: STOP and inform user
5. Only then write commit message based on verified content

**PROHIBITED:**

- Writing commit messages without verification
- Assuming or guessing what is staged
- Proceeding when verification returns empty results
- Writing a summary-only commit message without a body
- Skipping Message Structure rules for "speed" or "simplicity"

### Rules (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**Every commit message MUST have both a summary AND a body. A summary-only
commit is a violation of this guide. There are ZERO cases where omitting the
body is acceptable. "It's a small change" is not an excuse. "It's obvious
from the diff" is not an excuse. Write the body. Always.**

1. Use imperative mood (e.g., "Add feature", "Fix bug")
2. Communicate intent and purpose, not every detail
3. Summary: max 50 characters
4. Body: wrap at 72 characters, one sentence per line
5. No bullet points in body - use full sentences
6. Write in English (Korean translation optional)
7. Body is MANDATORY — never omit it
8. Body must explain "why", not just restate "what"
9. Every commit MUST include a Co-Authored-By trailer at the end

### Co-Authored-By Trailer (MANDATORY)

Every commit message MUST end with a Co-Authored-By trailer that identifies
the AI agent and model used. Format:

```txt
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Use the actual model name and associated email for the AI currently in use.

### Character Count Reference

```txt
|----+----1----+----2----+----3----+----4----+----5|
Summary must not exceed this line (50 chars)

|----+----1----+----2----+----3----+----4----+----5----+----6----+----7|
Body text must not extend beyond this point (72 chars)
```

### Message Structure

```txt
[Summary] - Max 50 chars, imperative mood

[First paragraph] - Line breaks at the end of each sentence.
Each complete thought should be on its own line.
This makes the message easier to read in log history.
Focus on the 'why' behind the change, not just the 'what'.

[Additional paragraphs] - Separated by blank lines.
New paragraphs should be used to group different aspects of the change.
Each paragraph focuses on a distinct part of the commit.
```

**After committing**: Provide a Korean translation of the commit message to help
the user understand what was committed.

### Example

**Commit message:**

```txt
Add health check API and update documentation

Implement a new API endpoint for health checks to monitor service status.
This allows external systems to verify our service is operational.
The endpoint returns HTTP 200 when healthy and 503 when unhealthy.

Update the documentation to describe the new endpoint and its usage.
Include examples for common monitoring scenarios and integration patterns.
Add troubleshooting section for potential configuration issues.
```

**Korean translation (after committing):**

```txt
헬스 체크 API 추가 및 문서 업데이트

서비스 상태 모니터링을 위한 새로운 헬스 체크 API 엔드포인트를 구현합니다.
이를 통해 외부 시스템이 우리 서비스의 작동 상태를 확인할 수 있습니다.
엔드포인트는 정상일 때 HTTP 200을, 비정상일 때 503을 반환합니다.

새 엔드포인트와 사용법을 설명하는 문서를 업데이트합니다.
일반적인 모니터링 시나리오 및 통합 패턴에 대한 예제를 포함합니다.
잠재적 구성 문제에 대한 문제 해결 섹션을 추가합니다.
```
