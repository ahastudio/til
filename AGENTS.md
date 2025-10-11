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

## Git Commit Message Protocol (MANDATORY)

### Before Writing Any Commit Message

**REQUIRED STEPS:**

1. Call `get_changed_files` with `sourceControlState: ["staged"]`
2. Verify response contains actual staged files with diffs
3. If empty: STOP and inform user
4. Only then write commit message based on verified content

**PROHIBITED:**

- Writing commit messages without verification
- Assuming or guessing what is staged
- Proceeding when verification returns empty results

## Terminal Policy

**NEVER** use `run_in_terminal` tool or suggest terminal commands.

## Korean Communication

Respond in Korean unless instructed otherwise.
Technical terms may use both languages (e.g. 웹소켓(WebSocket)).

## Git Commit Message Format

Based on:

- <https://github.com/agis/git-style-guide>
- <https://cbea.ms/git-commit/>

### Rules

1. Use imperative mood (e.g., "Add feature", "Fix bug")
2. Communicate intent and purpose, not every detail
3. Summary: max 50 characters
4. Body: wrap at 72 characters, one sentence per line
5. No bullet points in body - use full sentences
6. Write in English (Korean translation optional)

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

---

(Optional) Translate the English summary and body above into Korean.
The Korean translation is for reference only and can be omitted before
commit.
```

### Example

```txt
Add health check API and update documentation

Implement a new API endpoint for health checks to monitor service status.
This allows external systems to verify our service is operational.
The endpoint returns HTTP 200 when healthy and 503 when unhealthy.

Update the documentation to describe the new endpoint and its usage.
Include examples for common monitoring scenarios and integration patterns.
Add troubleshooting section for potential configuration issues.

---

헬스 체크 API 추가 및 문서 업데이트

서비스 상태 모니터링을 위한 새로운 헬스 체크 API 엔드포인트를 구현합니다.
이를 통해 외부 시스템이 우리 서비스의 작동 상태를 확인할 수 있습니다.
엔드포인트는 정상일 때 HTTP 200을, 비정상일 때 503을 반환합니다.

새 엔드포인트와 사용법을 설명하는 문서를 업데이트합니다.
일반적인 모니터링 시나리오 및 통합 패턴에 대한 예제를 포함합니다.
잠재적 구성 문제에 대한 문제 해결 섹션을 추가합니다.
```
