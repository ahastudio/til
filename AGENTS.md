# AI Agents Configuration for TIL Repository

## Git Commit Message Guide

This guide is based on:

- <https://github.com/agis/git-style-guide>
- <https://cbea.ms/git-commit/>

### Core Principles

1. Write commit messages in the imperative mood (e.g., "Add feature",
   "Fix bug") to clearly state what the commit will do when applied.
2. Always focus on communicating the intent, core purpose, and any important
   notes (such as cautions or breaking changes) rather than listing every
   minor detail or enumerating small changes.
3. The summary (title) of the commit message must be concise and must not
   exceed 50 characters, allowing for quick and clear understanding in logs.
4. The body of the commit message should be wrapped at 72 characters per line,
   with each sentence placed on its own line to enhance readability and
   maintain a clean commit history.
5. Do not use bullet points or lists in the commit message body; instead,
   write in full sentences and paragraphs to provide clear and continuous
   explanations.
6. Every commit message must be written in English to ensure consistency and
   accessibility for all contributors. Korean translation is optional and may
   be included as a supplement for reference, but it can be removed before
   committing if not needed.

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

### Line Length Rule

The body of the commit message must never exceed 72 characters per line.
This applies equally to both English and Korean. Always verify line length
before committing. This rule is strictly enforced, even for AI-generated
messages.

**If any line exceeds 72 characters, the entire message must be rewritten
immediately. This is non-negotiable.**

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
