# OpenSandbox - AI 애플리케이션용 범용 샌드박스 플랫폼

<https://github.com/alibaba/OpenSandbox>

Alibaba가 만든 오픈소스 샌드박스 플랫폼. AI 애플리케이션이
격리된 환경에서 코드를 실행하고 파일을 조작하며 네트워크를
제어할 수 있도록 멀티 언어 SDK, 통합 API, Docker/Kubernetes
런타임을 제공한다. Apache 2.0 라이선스.

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

| 엔드포인트                         | 역할                  |
| ---------------------------------- | --------------------- |
| `POST /sandboxes`                  | 컨테이너 이미지로 생성 |
| `DELETE /sandboxes/{id}`           | 종료                  |
| `POST /sandboxes/{id}/pause`       | 상태 보존하며 일시정지 |
| `POST /sandboxes/{id}/resume`      | 재개                  |
| `POST /sandboxes/{id}/renew-expiration` | 만료 시간 연장   |
| `GET /sandboxes/{id}/endpoints/{port}` | 서비스 접근 URL  |

인증: `OPEN-SANDBOX-API-KEY` 헤더

### Execd API

컨테이너 내부의 execd 데몬이 처리한다.

| 엔드포인트              | 역할                        |
| ----------------------- | --------------------------- |
| `POST /code`            | Jupyter 커널로 코드 실행    |
| `POST /code/context`    | 실행 컨텍스트(세션) 생성    |
| `GET /code/contexts`    | 활성 컨텍스트 목록          |
| `POST /command`         | 셸 명령어 실행              |
| `GET /files/download`   | 파일 다운로드               |
| `POST /files/upload`    | 파일 업로드                 |
| `POST /files/replace`   | 배치 텍스트 치환            |
| `GET /files/search`     | 글로브 패턴으로 파일 검색   |

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

| 컴포넌트           | 역할                              |
| ------------------ | --------------------------------- |
| `server/`          | FastAPI 기반 라이프사이클 서버    |
| `components/execd/` | 명령 실행·파일 조작 데몬         |
| `components/ingress/` | 통합 인그레스 게이트웨이        |
| `components/egress/` | 샌드박스별 네트워크 접근 제어   |
| `sdks/`            | 멀티 언어 클라이언트 SDK         |
| `specs/`           | OpenAPI 명세 (두 API 각각)        |
| `kubernetes/`      | K8s 배포 설정                    |

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

| 카테고리       | 도구                                        |
| -------------- | ------------------------------------------- |
| 샌드박스 관리  | `sandbox_create`, `sandbox_connect`,        |
|                | `sandbox_kill`, `sandbox_list`,             |
|                | `sandbox_renew`, `sandbox_get_endpoint`     |
| 명령어 실행    | `command_run`, `command_interrupt`          |
| 파일 조작      | `file_read`, `file_write`, `file_delete`,   |
|                | `file_search`, `file_move`,                 |
|                | `file_replace_contents`                     |

AI 에이전트가 MCP를 통해 격리된 컨테이너 안에서 코드를 실행하고
파일을 수정하는 패턴이다. 호스트 시스템을 보호하면서 에이전트에
풀 코드 실행 권한을 부여한다.

## 예제 생태계 (19개)

LLM 통합:

| 예제           | 설명                            |
| -------------- | ------------------------------- |
| `claude-code`  | Anthropic Claude CLI 실행       |
| `gemini-cli`   | Google Gemini 실행              |
| `codex-cli`    | OpenAI Codex 실행               |
| `kimi-cli`     | Moonshot AI Kimi 실행           |
| `langgraph`    | LangGraph 에이전트 오케스트레이션 |
| `google-adk`   | Google ADK 에이전트 연동        |

환경 유형:

| 예제          | 설명                              |
| ------------- | --------------------------------- |
| `playwright`  | Headless Chrome + Playwright      |
| `chrome`      | 원격 디버깅용 Chromium            |
| `desktop`     | VNC 데스크톱 (Xvfb + x11vnc)     |
| `vscode`      | 브라우저 기반 VS Code Web         |
| `rl-training` | CartPole + DQN 강화학습 루프      |

특정 LLM에 종속되지 않는다. 어떤 에이전트 프레임워크와도
연동 가능하다는 것이 설계 철학이다.

## 언어 선택: 제어 평면 Python, 데이터 평면 Go

| 역할           | 컴포넌트      | 언어            |
| -------------- | ------------- | --------------- |
| 제어 평면      | 생명주기 서버 | Python (FastAPI) |
| 데이터 평면    | execd         | Go (Beego)      |
| 네트워크 입구  | ingress       | Go              |
| 네트워크 출구  | egress        | Go              |
| 클라이언트     | SDK           | Python/JS/Kotlin/C# |

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

"컨테이너 실행 중" 이상의 레디니스 개념을 API 수준에서
표현하는 패턴이다.

## OSEP: 설계 방향을 보여주는 제안서

OpenSandbox Enhancement Proposals(OSEP)가 공개되어 있다.

| OSEP | 제목                              | 상태    |
| ---- | --------------------------------- | ------- |
| 0001 | FQDN 기반 이그레스 제어           | 구현 완료 |
| 0002 | Kubernetes SIGs 에이전트 샌드박스 | 계획    |
| 0003 | 볼륨·볼륨 바인딩 지원             | 계획    |
| 0004 | 보안 컨테이너 런타임              | 계획    |

OSEP-0004(보안 컨테이너 런타임)는 gVisor, Kata Containers 같은
강화된 격리 레이어를 추가하는 방향으로 추측된다. 현재 Docker
컨테이너보다 강한 격리가 필요한 시나리오를 목표로 한다.

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

## 관련 저장소

- 메인: <https://github.com/alibaba/OpenSandbox>
