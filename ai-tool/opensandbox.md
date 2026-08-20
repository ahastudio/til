# OpenSandbox - AI 애플리케이션용 범용 샌드박스 플랫폼

<https://open-sandbox.ai/>

<https://github.com/opensandbox-group/OpenSandbox>

Alibaba가 만든 오픈소스 샌드박스 플랫폼. AI 애플리케이션이
격리된 환경에서 코드를 실행하고 파일을 조작하며 네트워크를
제어할 수 있도록 멀티 언어 SDK, 통합 API, Docker/Kubernetes
런타임을 제공한다.

Apache 2.0 라이선스.

저장소 경로가 `alibaba/OpenSandbox`에서 `opensandbox-group/OpenSandbox`로 옮겨졌고
이전 주소는 리다이렉트된다.

## 프로젝트 상태

수치는 2026년 8월 20일 기준이다.

| 항목        | 값                                                    |
| ----------- | ----------------------------------------------------- |
| 스타        | 14,409                                                |
| 포크        | 1,267                                                 |
| 열린 이슈   | 160                                                   |
| 언어        | Python (제어 평면), Go (데이터 평면)                  |
| 라이선스    | Apache-2.0                                            |
| 저장소 생성 | 2025-12-17                                            |
| 마지막 푸시 | 2026-08-20                                            |
| 토픽        | `ai`, `ai-agent`, `ai-infra`, `kubernetes`, `sandbox` |

조직 이름은 중립화됐지만 패키지 좌표는 그대로다 —
Maven은 `com.alibaba.opensandbox:sandbox`,
npm은 `@alibaba-group/opensandbox`,
NuGet은 `Alibaba.OpenSandbox`,
Go 모듈 경로는 `github.com/alibaba/OpenSandbox/sdks/sandbox/go`다.
SDK는 Python, Java/Kotlin, JavaScript/TypeScript, C#/.NET, Go를 제공하고
`osb` CLI와 MCP 서버 통합이 함께 있다.

## 설치 및 시작

```bash
# 서버 설치 (Python 3.10+ 필요)
uv pip install opensandbox-server

# 설정 초기화 (Docker 모드)
opensandbox-server init-config ~/.sandbox.toml --example docker

# 서버 실행
opensandbox-server

# Python SDK 설치
uv add opensandbox
```

## 핵심 아키텍처: 두 API 레이어 분리

OpenSandbox의 가장 중요한 설계 결정은 API를 두 레이어로
분리한 것이다.

```text
[외부 클라이언트]
       │
       ▼
[Lifecycle API] ← 샌드박스 생성/삭제/일시정지/재개
       │           (컨테이너 오케스트레이션 레이어)
       ▼
[컨테이너 런타임] Docker / Kubernetes
       │
       ▼
[execd 데몬] ← 컨테이너 내부에서 실행
       │
       ▼
[Execd API] ← 코드 실행/명령어/파일 조작
              (샌드박스 실행 레이어)
```

이 분리를 통해 런타임이 바뀌어도(Docker → Kubernetes)
실행 API는 동일하게 유지된다. 인프라 교체 비용이 0이다.

### Lifecycle API

샌드박스의 외부 생애주기를 관리한다.

| 엔드포인트                              | 역할                   |
| --------------------------------------- | ---------------------- |
| `POST /sandboxes`                       | 컨테이너 이미지로 생성 |
| `DELETE /sandboxes/{id}`                | 종료                   |
| `POST /sandboxes/{id}/pause`            | 상태 보존하며 일시정지 |
| `POST /sandboxes/{id}/resume`           | 재개                   |
| `POST /sandboxes/{id}/renew-expiration` | 만료 시간 연장         |
| `GET /sandboxes/{id}/endpoints/{port}`  | 서비스 접근 URL        |

인증: `OPEN-SANDBOX-API-KEY` 헤더

### Execd API

컨테이너 내부의 execd 데몬이 처리한다.

| 엔드포인트            | 역할                      |
| --------------------- | ------------------------- |
| `POST /code`          | Jupyter 커널로 코드 실행  |
| `POST /code/context`  | 실행 컨텍스트(세션) 생성  |
| `GET /code/contexts`  | 활성 컨텍스트 목록        |
| `POST /command`       | 셸 명령어 실행            |
| `GET /files/download` | 파일 다운로드             |
| `POST /files/upload`  | 파일 업로드               |
| `POST /files/replace` | 배치 텍스트 치환          |
| `GET /files/search`   | 글로브 패턴으로 파일 검색 |

인증: `X-EXECD-ACCESS-TOKEN` 헤더

## 샌드박스 상태 머신

```text
Pending → Running → Pausing → Paused
                 ↘           ↙
                  Stopping → Terminated
                  ↕
                 Failed
```

Pause/Resume은 컨테이너를 종료하지 않고 상태를 보존한다.
RL 학습처럼 장시간 실행되는 작업에서 핵심 기능이다.

## 구성 요소

| 컴포넌트              | 역할                           |
| --------------------- | ------------------------------ |
| `server/`             | FastAPI 기반 라이프사이클 서버 |
| `components/execd/`   | 명령 실행·파일 조작 데몬       |
| `components/ingress/` | 통합 인그레스 게이트웨이       |
| `components/egress/`  | 샌드박스별 네트워크 접근 제어  |
| `sdks/`               | 멀티 언어 클라이언트 SDK       |
| `specs/`              | OpenAPI 명세 (두 API 각각)     |
| `kubernetes/`         | K8s 배포 설정                  |

## SDK 설계: API-First 멀티 언어

OpenAPI 명세에서 4개 언어 SDK를 파생한다. 명세가 진실의
단일 원천(Single Source of Truth)이다.

지원 언어: Python, JavaScript/TypeScript, Java/Kotlin, C#/.NET
(Go 계획 중)

### Python SDK 예시

```python
import asyncio
from opensandbox.sandbox import Sandbox
from opensandbox.config import ConnectionConfig

async def main():
    config = ConnectionConfig(
        domain="api.opensandbox.io",
        api_key="your-api-key"
    )
    sandbox = await Sandbox.create(
        "ubuntu",
        connection_config=config
    )
    async with sandbox:
        result = await sandbox.commands.run(
            "echo 'Hello Sandbox!'"
        )
        print(result.logs.stdout[0].text)
        await sandbox.kill()

asyncio.run(main())
```

동기(`SandboxSync`)와 비동기(`Sandbox`) API를 모두 제공한다.
`async with` 컨텍스트 매니저로 자원 정리를 보장한다.

## MCP 통합: AI 에이전트의 네이티브 도구화

`opensandbox-mcp` 서버가 SDK를 MCP 도구로 노출한다.
Claude Code, Cursor 등이 직접 샌드박스를 조작할 수 있다.

노출 도구:

| 카테고리      | 도구                                      |
| ------------- | ----------------------------------------- |
| 샌드박스 관리 | `sandbox_create`, `sandbox_connect`,      |
|               | `sandbox_kill`, `sandbox_list`,           |
|               | `sandbox_renew`, `sandbox_get_endpoint`   |
| 명령어 실행   | `command_run`, `command_interrupt`        |
| 파일 조작     | `file_read`, `file_write`, `file_delete`, |
|               | `file_search`, `file_move`,               |
|               | `file_replace_contents`                   |

AI 에이전트가 MCP를 통해 격리된 컨테이너 안에서 코드를 실행하고
파일을 수정하는 패턴이다. 호스트 시스템을 보호하면서 에이전트에
풀 코드 실행 권한을 부여한다.

## 예제 생태계 (19개)

LLM 통합:

| 예제          | 설명                              |
| ------------- | --------------------------------- |
| `claude-code` | Anthropic Claude CLI 실행         |
| `gemini-cli`  | Google Gemini 실행                |
| `codex-cli`   | OpenAI Codex 실행                 |
| `kimi-cli`    | Moonshot AI Kimi 실행             |
| `langgraph`   | LangGraph 에이전트 오케스트레이션 |
| `google-adk`  | Google ADK 에이전트 연동          |

환경 유형:

| 예제          | 설명                         |
| ------------- | ---------------------------- |
| `playwright`  | Headless Chrome + Playwright |
| `chrome`      | 원격 디버깅용 Chromium       |
| `desktop`     | VNC 데스크톱 (Xvfb + x11vnc) |
| `vscode`      | 브라우저 기반 VS Code Web    |
| `rl-training` | CartPole + DQN 강화학습 루프 |

특정 LLM에 종속되지 않는다. 어떤 에이전트 프레임워크와도
연동 가능하다는 것이 설계 철학이다.

## 언어 선택: 제어 평면 Python, 데이터 평면 Go

| 역할          | 컴포넌트      | 언어                |
| ------------- | ------------- | ------------------- |
| 제어 평면     | 생명주기 서버 | Python (FastAPI)    |
| 데이터 평면   | execd         | Go (Beego)          |
| 네트워크 입구 | ingress       | Go                  |
| 네트워크 출구 | egress        | Go                  |
| 클라이언트    | SDK           | Python/JS/Kotlin/C# |

빠른 개발이 필요한 오케스트레이션 레이어는 Python, 낮은
지연과 높은 동시성이 필요한 실행 레이어는 Go. 각 요구사항에
맞는 언어를 선택한 실용적인 결정이다.

## Kubernetes BatchSandbox: O(1) 배치 생성

일반적으로 N개 샌드박스를 생성하려면 N번의 API 호출이 필요하다.
`BatchSandbox` CRD는 단일 리소스 생성으로 N개를 일괄
프로비저닝한다. 대규모 병렬 에이전트 실행(예: 에이전트 평가,
RL 훈련)에서 핵심 차별점이다.

`Pool` CRD도 제공한다. 사전 워밍된 컨테이너 풀에서 꺼내오는
방식으로 샌드박스 생성 지연을 제거한다.

## Egress: DNS + nftables 이중 방어

단순 IP 필터링이나 DNS 필터링 중 하나만 쓰지 않는다. 두 레이어를
조합한다.

```text
컨테이너 DNS 요청
       │
       ▼
[DNS 프록시 (127.0.0.1:15353)]
  ├─ 허용 도메인 → NXDOMAIN이 아닌 정상 응답
  │               + 해석된 IP를 nftables에 동적 등록
  └─ 거부 도메인 → NXDOMAIN 반환
       │
       ▼
[nftables IP 필터]
  ├─ 등록된 IP → 통과 (TTL 기반 자동 만료)
  └─ 미등록 IP → 차단 (기본 거부)
```

DNS TTL이 만료되면 nftables 규칙도 자동으로 제거된다. DNS
레이어만으로는 막을 수 없는 직접 IP 접근을 nftables가 차단하고,
nftables만으로는 표현하기 어려운 도메인 정책을 DNS가 처리한다.

## 이후 들어온 기능

첫 정리 이후 README의 기능 목록에 세 항목이 추가됐다.

| 항목                     | 내용                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------ |
| Credential Vault         | 실제 시크릿을 워크로드에 노출하지 않고 샌드박스의 아웃바운드 요청에 자격 증명을 주입 |
| 강한 격리                | gVisor, Kata Containers, Firecracker microVM 같은 보안 컨테이너 런타임 지원          |
| 통합 인그레스 게이트웨이 | 여러 라우팅 전략을 지원하는 단일 인그레스와 샌드박스별 이그레스 제어의 결합          |

연동 예제도 늘었다.
LangGraph와 Google ADK 연동이 있고,
Claude Code와 Gemini CLI와 Codex CLI 같은 벤더 CLI를 샌드박스 안에서 실행하는 예제가 있으며,
Harbor 기반 에이전트 평가 예제가 포함된다.

## OSEP: 설계 방향을 보여주는 제안서

OpenSandbox Enhancement Proposals(OSEP)가 공개되어 있다.

| OSEP | 제목                              | 상태      |
| ---- | --------------------------------- | --------- |
| 0001 | FQDN 기반 이그레스 제어           | 구현 완료 |
| 0002 | Kubernetes SIGs 에이전트 샌드박스 | 계획      |
| 0003 | 볼륨·볼륨 바인딩 지원             | 계획      |
| 0004 | 보안 컨테이너 런타임              | 계획      |

OSEP-0004(보안 컨테이너 런타임)는 gVisor, Kata Containers 같은
강화된 격리 레이어를 추가하는 방향으로 추측된다. 현재 Docker
컨테이너보다 강한 격리가 필요한 시나리오를 목표로 한다.

그 제안은 이후 실현됐다.
README의 기능 목록에 gVisor와 Kata Containers와 Firecracker microVM 지원이
올라와 있으므로 위 표의 0004는 계획이 아니라 반영된 상태로 읽어야 한다.

## 분석

### 두 API 레이어의 분리가 구현이 아니라 규격을 겨냥한 것이었음이 확인된다

처음 정리할 때 두 API 레이어 분리는 런타임 교체를 위한 내부 설계로 읽혔다.
지금 README는 그것을 샌드박스 프로토콜이라고 부르고,
라이프사이클 관리 API와 실행 API를 정의해
커스텀 샌드박스 런타임을 확장할 수 있게 한다고 적으며 별도의 API 명세를 둔다.

그 규격 주장의 첫 증명이 강한 격리 항목이다.
gVisor와 Kata Containers와 Firecracker microVM을 지원한다는 것은
격리 수준이 다른 세 런타임 아래에서 같은 API가 유지된다는 뜻이며,
이것이 성립하면 사용자 코드는 격리 강도를 설정으로 고를 수 있게 된다.
Docker에서 Kubernetes로 가는 경로에 이어 두 번째 축이 열린 것이다.

이 방향이 프로젝트의 위치도 정한다.
LangGraph와 Google ADK 연동이 있고 벤더 CLI 실행 예제가 있다는 것은
자기를 에이전트 프레임워크의 경쟁자가 아니라 그 아래 계층으로 규정한다는 뜻이며,
프레임워크가 무엇이든 실행 환경은 하나면 된다는 주장이다.

### Credential Vault가 격리의 문제 정의를 바꾼다

기존 이그레스 제어는 “밖으로 나가지 못하게” 하는 문제였다.
DNS와 nftables 이중 방어가 그 구현이고, 목표는 차단이다.

Credential Vault는 반대 방향의 문제를 다룬다 —
나가게 하되 비밀은 주지 않는 것이다.
에이전트가 실제로 일을 하려면 API 키가 필요하고,
키를 워크로드 안에 넣으면 격리의 의미가 크게 줄어든다.
샌드박스가 아웃바운드 요청에 자격 증명을 대신 주입하면
워크로드는 키를 본 적이 없는 상태로 인증된 요청을 보낼 수 있다.

이 패턴 자체는 새롭지 않다 — 프록시가 대신 서명하는 방식이며
서비스 메시와 API 게이트웨이가 오래 써 온 구조다.
새로운 것은 샌드박스 런타임이 그것을 내장 기능으로 올렸다는 사실이고,
그 선택이 대상 워크로드를 알려 준다.
사람이 쓰는 개발 환경이라면 키를 넣어 주는 것으로 끝나지만,
[에이전트가 위임자의 권한을 넘지 못하게 해야 하는 문제](../business/k-skill-blue-ribbon.md)에서는
키를 주지 않는 것이 유일한 해법이다.

### 8개월에 스타 14,409개가 만든 상태

저장소가 2025년 12월에 만들어졌고 스타 14,409개에 포크 1,267개,
열린 이슈 160개다.
이 범주에서 가장 빠르게 커진 프로젝트 중 하나이며,
그 속도가 기능 목록의 성격을 설명한다.

기능이 축적되는 방향이 넓이 쪽이다 —
런타임 세 종류, SDK 다섯 언어, CLI, MCP, 인그레스, 이그레스, 자격 증명 보관소,
그리고 코딩 에이전트와 브라우저 자동화와 데스크톱 예제다.
좁고 깊은 도구가 아니라 플랫폼을 표방하는 목록이고,
열린 이슈 160개가 그 넓이의 유지 비용으로 보인다.

## 비평

### 조직 이름은 중립화됐는데 소유의 표시는 그대로 남아 있다

저장소 경로가 `alibaba/OpenSandbox`에서 `opensandbox-group/OpenSandbox`로 옮겨졌다.
새 이름은 회사가 아니라 프로젝트 이름을 딴 중립적 형태이고,
이런 이동은 통상 재단 이관이나 거버넌스 개방의 신호로 읽힌다.

그런데 패키지 좌표는 전부 그대로다.
Maven 그룹 ID가 `com.alibaba.opensandbox`이고
npm 스코프가 `@alibaba-group`이며 NuGet 패키지가 `Alibaba.OpenSandbox`이고,
Go 모듈 경로는 여전히 `github.com/alibaba/OpenSandbox`를 가리킨다.
즉 이동은 저장소 URL에서 일어났고 배포 아티팩트에서는 일어나지 않았다.

이 상태가 중립적이지 않은 이유는 채택 결정에 필요한 정보가 빠져 있기 때문이다.
사용자가 알고 싶은 것은 이름이 아니라 거버넌스다 —
릴리스 권한이 누구에게 있는지, CLA를 요구하는지,
로드맵을 정하는 주체가 회사인지 위원회인지다.
새 조직 이름은 그 질문에 답하지 않으면서 답한 것처럼 보이게 만든다.

GN 댓글의 반응 — 이제 ‘오픈’이라는 단어에 염증을 느낀다는 것[^heim2] — 이
정확히 이 지점을 겨냥한 것으로 읽힌다.
짧은 냉소이지만 근거가 있다.
저장소 어디에도 이 이동이 브랜딩인지 거버넌스 변화인지가 적혀 있지 않고,
패키지 이름은 전자라고 말한다.
한 줄의 설명이면 해소되는 오해이며, 그 한 줄이 없는 것이 선택으로 읽힌다.

### 세 격리 런타임을 한 줄에 나열하고 검증 조합을 밝히지 않는다

강한 격리 항목은 gVisor와 Kata Containers와 Firecracker microVM을 함께 든다.
셋은 격리 방식과 성숙도와 제약이 서로 다르다 —
gVisor는 시스템 콜을 사용자 공간에서 가로채므로 커버리지 밖의 호출에서 문제가 생기고,
Kata는 경량 VM이므로 오버헤드와 커널 관리가 따라오고,
Firecracker는 microVM이라 컨테이너 이미지와 디바이스 호환성이 별도 과제다.

이 프로젝트의 다른 기능들이 그 제약과 정면으로 만난다.
Code Interpreter는 Jupyter 커널을 띄우고,
데스크톱 예제는 VNC와 VS Code Web을 돌리며,
브라우저 자동화 예제는 Chrome과 Playwright를 실행한다.
셋 다 시스템 콜과 디바이스 요구가 큰 워크로드이므로,
“지원한다”가 어느 조합에서 검증됐는지가 실무 질문이 된다.

필요한 것은 런타임과 환경의 교차표 한 개다.
어느 격리 런타임에서 어느 예제가 검증됐고 무엇이 미지원인지를 표로 두면
사용자가 자기 워크로드에 맞는 격리 강도를 고를 수 있다.
지금은 목록만 있어서 선택의 근거가 문서 밖에 있다.

### 범용을 표방하면서 예제가 벤더 CLI의 약관 위에 서 있다

연동 예제에 Claude Code와 Gemini CLI와 Codex CLI 실행이 포함된다.
샌드박스 안에서 벤더 CLI를 돌리는 것은 실용적이고 수요가 분명한 시나리오다.

그런데 그 CLI들은 각자 계정 인증을 요구하고 약관이 다르다.
샌드박스 안에서 어떤 계정으로 로그인할지,
그 계정을 여러 샌드박스가 공유해도 되는지,
자동화된 다수 실행이 각 벤더의 이용 조건에 맞는지가 사용자에게 남는 질문이다.
그리고 Credential Vault가 있으므로 기술적으로는 자격 증명 공유가 아주 쉬워졌다 —
그 편의가 정확히 위험이 되는 자리다.

[한 사람의 구독 권한을 여러 사람의 것으로 바꾼 프록시가
문제가 된 사례](../business/k-skill-blue-ribbon.md)와 같은 구조이며,
차이는 여기서는 그 기능이 제품에 내장되어 있다는 점이다.
예제 문서에 “벤더 계정 자격 증명을 여러 샌드박스에 공유하는 것은
각 벤더 약관의 문제이며 이 예제는 개인 사용을 전제한다”는 한 줄이 있으면
사용자가 조직 단위로 그것을 돌릴 때의 판단이 달라진다.
지금은 편의만 제공되고 경계는 언급되지 않는다.

## 인사이트

### 두 API 분리가 만드는 유연성

대부분의 샌드박스 솔루션은 실행 환경과 오케스트레이션을
하나로 묶는다. OpenSandbox는 이를 분리해서 런타임을 교체해도
코드가 바뀌지 않는다. Docker에서 시작해 Kubernetes로 확장하는
전형적인 성장 경로를 마찰 없이 지원한다.

### execd 데몬 패턴

컨테이너 내부에 항상 실행 중인 데몬을 둔다. 이 데몬이 외부
API 호출을 받아 명령을 실행하고 결과를 반환한다. 단순하지만
강력하다. 어떤 베이스 이미지도 execd만 포함하면 OpenSandbox
호환 환경이 된다.

### Code Interpreter = Jupyter-as-a-Service

`POST /code`는 Jupyter 커널을 호출하며 SSE(Server-Sent Events)로
실시간 스트리밍한다. 컨텍스트(세션)가 지속되므로 이전 실행의
변수와 상태를 유지한다. `import numpy as np` 같은 초기화 비용을
한 번만 지불하고 이후 실행에서 재사용한다. 단발성 스크립트
실행이 아닌 대화형 REPL 환경을 API로 노출한 것이다.

### Pause/Resume = 비용 최적화

컨테이너를 종료하지 않고 일시정지하면 재시작 비용(이미지 풀,
의존성 설치)이 없다. RL 학습처럼 중단점이 필요한 작업에서
Pause → 체크포인트 저장 → Resume 패턴으로 비용을 절감한다.

### MCP가 뒤집는 통합 방향

기존: 에이전트 코드 안에 샌드박스 SDK를 임포트.
MCP: 샌드박스가 도구를 에이전트에 노출.

에이전트가 샌드박스를 소유하는 게 아니라, 샌드박스가 도구로서
에이전트에 등록된다. 에이전트 코드 변경 없이 샌드박스 교체가
가능하다.

### Egress 제어 = 진짜 격리

네트워크 접근을 샌드박스 단위로 제어한다. AI 에이전트가 임의의
외부 서버와 통신하는 것을 막을 수 있다. 보안 규정이 엄격한 환경
(금융, 의료)에서 에이전트를 운용하는 핵심 요건이다.

### 커스텀 헬스 체크 주입

기본 헬스 체크는 execd의 `/ping` 응답 여부만 확인한다.
VS Code Web이나 Playwright처럼 내부 서비스 준비가 필요한 경우
커스텀 함수를 주입해 실제 레디니스를 표현한다.

```python
async def wait_for_vscode(sandbox):
    endpoint = await sandbox.get_endpoint(8443)
    resp = await http_get(endpoint)
    return resp.status_code == 200

await sandbox.check_ready(
    timeout=60,
    health_check=wait_for_vscode
)
```

“컨테이너 실행 중” 이상의 레디니스 개념을 API 수준에서
표현하는 패턴이다.

### 에이전트 샌드박스의 경쟁축이 격리에서 자격 증명으로 이동한다

Credential Vault가 기능 목록에 오른 것은 이 범주의 무게 중심이 옮겨 가는 신호다.
격리 자체는 상품화되는 중이다 — gVisor와 Kata와 Firecracker가 이미 있고,
어느 프로젝트든 그것을 가져다 쓰면 되므로 차별점이 되지 못한다.

남는 문제는 격리된 워크로드가 실제로 일을 하게 만드는 것이다.
에이전트는 저장소에 푸시하고 API를 호출하고 결제를 조회해야 하는데,
그러려면 자격 증명이 필요하고 자격 증명을 넣는 순간 격리의 값이 줄어든다.
이 긴장을 푸는 유일한 방향이 워크로드가 비밀을 보지 못한 채
인증된 요청을 보내게 하는 것이며, 그것이 곧 프록시 계층이다.

여기서 따라오는 2차 효과가 위치의 집중이다.
샌드박스가 자격 증명을 주입하려면 모든 아웃바운드 요청이 그것을 지나야 하고,
그러면 샌드박스는 실행 환경이면서 동시에 네트워크 게이트웨이가 된다.
그 위치는 감사 지점으로서 값이 크지만 —
어느 에이전트가 무엇에 접근했는지가 한곳에 남는다 —
동시에 단일 실패점이며 침해 시 피해 범위가 가장 넓은 지점이다.

그러므로 이 범주를 평가하는 질문이 바뀐다.
얼마나 강하게 격리하는지가 아니라
자격 증명 주입의 범위와 감사 기록과 폐기 절차가 어떻게 되어 있는지이며,
[제어면과 실행면의 소유가 다르면 능력은 제어면에 있다는 관찰](../github/github-is-not-just-git.md)이
여기서도 그대로 적용된다.

### 중립적 조직 이름은 거버넌스의 대리 지표로 쓸 수 없다

기업이 후원하는 오픈소스 프로젝트가 회사 조직에서 중립적 이름의 조직으로 옮기는 일은 늘고 있다.
채택 장벽을 낮추는 알려진 수단이고, 재단 이관의 준비 단계이기도 하다.
문제는 같은 동작이 브랜딩만으로도 가능하다는 것이다.

구별할 수 있는 지표가 몇 개 있고 전부 확인 가능하다.
배포 아티팩트의 이름 공간, 기여자 라이선스 동의 요구 여부,
커밋 작성자 이메일 도메인의 분포, 릴리스 태그를 만들 권한을 가진 계정,
그리고 로드맵과 제안 절차를 누가 승인하는지다.
이 프로젝트의 경우 첫 번째 지표가 이동이 아직 표면적임을 알려 준다.

이것이 흠이라는 뜻은 아니다.
회사가 만들고 회사가 유지하는 프로젝트는 정당하며,
Apache-2.0에 API 명세와 제안서 절차까지 공개한 상태는 오히려 성실한 편이다.
문제는 이름이 주는 인상과 실제 상태가 다를 때 생기는 오해이고,
그 오해를 프로젝트가 아니라 사용자가 부담한다는 점이다.

그러므로 이런 이동을 만나면 이름을 신호로 읽지 않는 습관이 필요하다.
`pip install`과 `go get`에 적히는 문자열이 조직도보다 정확하며,
[저장소 이름과 검색 단위가 발견 가능성을 정한다는 관찰](../architecture/system-design-notes.md)의
반대편에서 같은 원리가 작동한다 — 이름은 값싸게 바꿀 수 있고, 그래서 정보량이 적다.

---

[^heim2]: <https://news.hada.io/topic?id=32685#cid63796>
