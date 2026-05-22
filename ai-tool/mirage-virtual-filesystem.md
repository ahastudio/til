# Mirage — AI 에이전트를 위한 통합 가상 파일시스템

<https://github.com/strukto-ai/mirage>

## 소개

Mirage는 S3, Google Drive, Slack, Gmail, Redis 등 다양한 백엔드를 단일 파일시스템 트리로 마운트하는 AI 에이전트용 통합 가상 파일시스템(VFS)이다.
AI 에이전트가 각 서비스별 SDK를 별도로 학습하는 대신, Unix 배시(bash) 명령어로 모든 백엔드에 동일하게 접근할 수 있게 해준다.
“어떤 LLM이든 bash를 이미 알고 있으면 Mirage를 바로 사용할 수 있다”는 설계 철학이 핵심이다.

Apache 2.0 라이선스로 공개되어 있으며, Python(`mirage-ai`)과 TypeScript(`@struktoai/mirage-node`) SDK를 모두 제공한다.
OpenAI Agents SDK, LangChain, Pydantic AI, CAMEL, OpenHands 같은 주요 에이전트 프레임워크와 호환된다.
Claude Code와 Codex 같은 코딩 에이전트에서도 배시를 통해 마운트된 모든 리소스에 접근할 수 있다.

## 아키텍처

Mirage의 아키텍처는 에이전트와 애플리케이션이 Mirage의 bash/VFS 인터페이스를 통해 명령을 실행하면, 디스패처와 캐시 레이어가 이를 처리해 적절한 인프라 및 원격 서비스로 라우팅하는 구조다.

```text
AI Agent / Application
        │
   Mirage Bash + VFS
        │
  Dispatcher & Cache
        │
Infrastructure & Remote Services
(S3, GDrive, Slack, GitHub, Redis, MongoDB, SSH, ...)
```

워크스페이스는 클론, 스냅샷, 버전 관리가 가능하여 머신 간 마이그레이션 시 재설정 없이 에이전트 실행 환경을 이전할 수 있다.

## 사용법

### Python

```python
from mirage import Workspace
from mirage.resource.ram import RAMResource
from mirage.resource.s3 import S3Config, S3Resource
from mirage.resource.slack import SlackConfig, SlackResource

ws = Workspace({
    "/data":  RAMResource(),
    "/s3":    S3Resource(S3Config(bucket="my-bucket")),
    "/slack": SlackResource(SlackConfig()),
})

await ws.execute("cp /s3/report.csv /data/report.csv")
await ws.execute("grep alert /s3/data/log.jsonl | wc -l")
```

### TypeScript

```ts
const ws = new Workspace({
  '/data':   new RAMResource(),
  '/s3':     new S3Resource({ bucket: 'logs' }),
  '/slack':  new SlackResource({}),
  '/github': new GitHubResource({}),
})

await ws.execute('grep alert /slack/general/*.json | wc -l')
await ws.execute('cat /github/mirage/README.md')
await ws.execute('cp /s3/report.csv /data/local.csv')
```

커스텀 커맨드 등록과 특정 리소스·파일타입에 대한 커맨드 오버라이드도 지원한다. 예를 들어 S3의 Parquet 파일에 `cat`을 실행하면 raw 바이트 대신 JSON 행으로 렌더링하도록 설정할 수 있다.

### CLI

```bash
# pip
uv add mirage-ai

# npm
npm install -g @struktoai/mirage-cli
```

## 분석

### LLM 훈련 코퍼스를 활용한 추상화 전략

Mirage의 핵심 설계 결정은 에이전트 인터페이스로 bash를 선택한 것이다.
이것은 편의성의 문제가 아니라 전략적 선택이다.
현대 LLM은 방대한 bash 스크립트, Linux 문서, Unix 튜토리얼 데이터로 훈련되었다.
즉, `ls`, `cat`, `grep`, `cp`, `find` 같은 명령어는 이미 모델이 가장 유창하게 다루는 언어다.

새로운 API 문법을 도입하는 대신 모델이 이미 잘 아는 인터페이스를 파일시스템으로 추상화한 것은 fine-tuning이나 few-shot 프롬프팅 없이도 즉시 활용 가능하다는 것을 의미한다.
이 선택은 에이전트 도구 설계에서 “모델이 이미 아는 것을 활용하라”는 원칙의 좋은 사례다.

### N개의 SDK 대신 하나의 파일시스템

현실의 AI 에이전트 파이프라인은 Slack 메시지를 읽고, S3 파일을 처리하고, GitHub 이슈를 참조하고, Gmail을 발송하는 여러 단계를 포함한다.
각 서비스마다 SDK를 초기화하고, 인증을 처리하고, API 변경에 대응하는 것은 에이전트 코드베이스의 복잡성을 급격히 증가시킨다.
Mirage의 단일 파일시스템 추상화는 이 복잡성을 VFS 계층 안으로 캡슐화한다.

## 비평

### 강점: 이식 가능한 에이전트 환경

워크스페이스 스냅샷과 복원 기능은 에이전트 디버깅과 재현성 측면에서 실질적인 가치를 갖는다.
에이전트가 특정 상태에서 실패했을 때, 그 상태를 스냅샷으로 저장하고 재현하는 것은 디버깅을 크게 단순화한다.
또한 CI/CD 파이프라인에서 에이전트 테스트를 격리된 환경에서 실행하는 데도 활용할 수 있다.

### 약점: 파일시스템 추상화의 임피던스 불일치

모든 서비스가 파일시스템 의미론(semantics)에 자연스럽게 매핑되지는 않는다.
Slack의 채널-스레드-메시지 구조, Gmail의 레이블 시스템, Notion의 블록 계층은 `/slack/general/message_123.json` 같은 파일 경로로 표현될 때 추상화 누수(abstraction leak)가 발생할 수 있다.
에이전트가 이 매핑의 한계를 이해하지 못하면 잘못된 가정 위에서 동작할 위험이 있다.

## 인사이트

### 도구 인터페이스는 인지 부하의 함수다

AI 에이전트 개발에서 가장 과소평가된 설계 과제 중 하나는 도구 인터페이스의 인지 부하다.
에이전트에게 Slack API, GitHub API, S3 API를 각각 가르치는 것은 사람에게 서로 다른 방언을 쓰는 세 나라의 전화 교환원 역할을 동시에 맡기는 것과 같다.
Mirage는 이 문제를 공통 언어(bash)로 방언을 통일함으로써 해결하려 한다.

이 접근의 함의는 AI 에이전트의 성능이 모델 능력만의 함수가 아님을 보여준다는 것이다.
동일한 모델이라도 인터페이스 설계에 따라 성공률이 달라진다.
“이 도구를 어떻게 사용하는가”를 모델이 얼마나 쉽게 추론할 수 있는지가 에이전트 도구 설계의 핵심 메트릭이 되어야 한다.
Mirage의 bash 선택은 이 메트릭을 의도적으로 최적화한 결과다.

### 에이전트 환경의 이식성 문제는 아직 미해결이다

현재 에이전트 시스템의 가장 큰 실용적 장벽 중 하나는 환경의 이식성이다.
로컬에서 개발한 에이전트가 프로덕션 환경에서 동일하게 작동하지 않거나, 특정 실패를 재현하기 어려운 상황이 흔하다.
Mirage의 스냅샷 기능은 이 문제에 대한 파일시스템 레이어에서의 부분적 해결책이다.

그러나 에이전트 환경의 완전한 이식성은 파일시스템 상태만의 문제가 아니다.
외부 API의 상태, 모델의 버전, 프롬프트의 버전, 도구의 스키마 등이 모두 얽혀 있다.
Docker가 애플리케이션 환경을 컨테이너화한 것처럼, 에이전트 실행 환경 전체를 재현 가능하게 만드는 표준 도구가 아직 없다.

Mirage는 이 퍼즐의 한 조각이다.
파일시스템 계층의 이식성을 해결하는 것은 전체 에이전트 환경 이식성 문제의 중요한 시작점이 될 수 있다.
이 방향이 성숙할수록, 에이전트 파이프라인의 재현성과 디버깅 가능성은 크게 개선될 것이다.

### 파일시스템 추상화는 AI 에이전트의 POSIX가 될 수 있다

POSIX는 서로 다른 Unix 구현들이 호환되는 인터페이스를 갖도록 표준화한 규격이다.
Mirage가 제안하는 것은 AI 에이전트 도구 생태계의 유사한 역할이다.
에이전트가 어떤 데이터 소스에 접근하든 동일한 파일시스템 인터페이스를 사용한다면, 에이전트 로직과 데이터 소스 구현이 분리되어 더 모듈화된 에이전트 시스템이 가능해진다.

이것이 단순한 편의 라이브러리를 넘어 인프라 표준이 되려면 더 많은 커뮤니티 참여와 파일시스템 의미론의 공식화가 필요하다.
MCP(Model Context Protocol)가 Claude 생태계에서 도구 인터페이스를 표준화하려는 시도와 비교했을 때, Mirage는 더 낮은 수준(OS 추상화)에서 표준화를 제안한다.
두 접근이 서로 경쟁하는지, 보완하는지는 앞으로의 생태계 발전에 달려 있다.
