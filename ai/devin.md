# Devin - AI Software Engineer

<https://devin.ai/>

Cognition(<https://cognition.ai/>)이 만든
자율형 AI 소프트웨어 엔지니어.
2024년 3월 공개, 2024년 12월 정식 출시(GA).

## 주요 특징

- **자율적 개발 환경**:
  클라우드 샌드박스에 쉘, 에디터, 브라우저를 갖추고
  사람처럼 도구를 전환하며 작업을 수행한다.
- **계획 수립과 실행**:
  작업 지시를 받으면 단계별 계획을 세우고 실행한다.
  타임라인으로 진행 상황을 보여주며,
  사용자가 중간에 개입할 수 있다.
- **풀스택 개발**:
  프론트엔드, 백엔드, 인프라를 가리지 않는다.
  프로젝트 세팅, 버그 수정, 리팩터링 등을 처리한다.
- **외부 도구 학습**:
  문서 URL을 제공하면 읽고 학습하여 적용한다.
  익숙하지 않은 기술도 문서를 통해 파악할 수 있다.
- **Git/GitHub 연동**:
  브랜치 생성, 커밋, PR 생성을 자동 수행한다.
  GitHub Issue 할당이나 리뷰 코멘트 반영도 가능하다.
- **Slack 통합**:
  Slack에서 멘션하여 작업을 요청하고
  결과를 받을 수 있다.
  비개발 직군도 접근할 수 있다.
- **세션 기반 작업**:
  각 작업이 독립된 세션으로 실행되어
  여러 작업을 병렬로 진행할 수 있다.
  스냅샷으로 특정 시점의 환경을 재현할 수도 있다.

## Claude Code와 비교

|                    | Devin                  | Claude Code            |
|--------------------|------------------------|------------------------|
| 작업 방식          | 비동기. 맡기고 기다림  | 동기. 실시간 협업      |
| 실행 환경          | 클라우드 샌드박스      | 로컬 터미널            |
| 인터페이스         | 웹 UI, Slack           | CLI, IDE 확장          |
| 컨텍스트           | Knowledge 설정으로     | 로컬 코드베이스 탐색,  |
|                    | 보완                   | CLAUDE.md로 규칙 전달  |
| 요금               | $500/월 (시트당)       | Pro/Max $20~$200/월    |

### 코드 퀄리티

Devin은 자율적으로 작업하는 만큼 품질 편차가 크다.
잘 정의된 소규모 작업에서는 좋은 결과를 내지만,
복잡한 로직에서는 의도와 다른 코드를 생성하거나
기존 컨벤션을 무시하는 경우가 있다.

Claude Code는 과정을 실시간으로 보면서
잘못된 방향을 바로 교정할 수 있다.
자율성과 품질 제어는 트레이드오프 관계다.

### 적합한 사용 사례

| Devin                        | Claude Code                |
|------------------------------|----------------------------|
| 독립적인 기능 개발           | 탐색적 코딩, 프로토타이핑 |
| 잘 정의된 버그 수정          | 복잡한 디버깅              |
| 반복적인 마이그레이션        | 코드 리뷰와 리팩터링      |
| CI/CD 실패 수정              | 아키텍처 논의와 설계       |
| 비개발자의 작업 요청         | 학습과 코드 이해           |

## PR 리뷰 대응

PR 코멘트에서 `@devin`을 멘션하면
피드백을 읽고 코드를 수정한다.
단순한 수정 요청은 잘 처리하지만,
설계 수준의 피드백이나 다중 파일에 걸친 코멘트는
맥락을 놓칠 수 있다.

### CodeRabbit과 조합

[CodeRabbit](./coderabbit.md)과 함께 사용하면
Devin이 PR을 만들고 CodeRabbit이 자동 리뷰하는
파이프라인을 구성할 수 있다.

```text
Devin PR 생성 → CodeRabbit 자동 리뷰
→ Devin 리뷰 반영 → 사람 최종 확인 후 머지
```

다만 AI가 만든 코드를 AI가 리뷰하는 구조이므로
설계 오류, 비즈니스 로직, 보안 취약점은
사람이 반드시 확인해야 한다.

## 문서

<https://docs.devin.ai/>

## Coding Agents 101

[Coding Agents 101: The Art of Actually Getting Things Done](https://devin.ai/agents101)

## 요금제

<https://devin.ai/pricing>

| 플랜       | 가격              |
|------------|-------------------|
| Core       | $500/월 (시트당)  |
| Enterprise | 별도 문의         |

## Articles

[Cognition introduces Devin, an AI software engineering teammate - TechCrunch](https://techcrunch.com/2024/03/12/cognitions-new-ai-agent-devin-can-write-and-execute-code/)

[Cognition's AI coding agent, Devin, is now generally available - TechCrunch](https://techcrunch.com/2024/12/06/cognitions-ai-coding-agent-devin-is-now-generally-available/)
