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

**요청한 것만 한다. 요청하지 않은 행동은 절대 하지 않는다.**

- "커밋 메시지 써줘" → 텍스트를 출력한다. git 조작이 아니다.
- "diff 보고" → diff를 읽고 응답한다. 커밋을 수정하지 않는다.
- squash, rebase, amend 등 커밋 조작은 **명시적 요청 없이 절대 금지**.
- 확신이 없으면 멋대로 행동하지 말고 묻는다.

## Guides

- [Writing Guidelines](./.agent/guides/writing-guidelines.md)
- [Git Workflow](./.agent/guides/git-workflow.md)
