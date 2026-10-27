# ARTEMIS: 자연어 지시를 안드로이드 자동화로 바꾸는 구글의 테스트 에이전트

<https://github.com/google/artemis>

## 소개

ARTEMIS는 구글 Pixel-Test-Engineering(PTE) Fusion 팀이
2026년 8월 13일에 공개한 안드로이드 테스트 자동화 에이전트다.
자연어로 쓴 지시를 실제 단말 조작으로 바꾸는 것이 목표이며,
Apache-2.0 라이선스에 Python으로 작성되어 있다.
공개 시점부터 한 달이 채 되지 않은 2026년 9월 10일 기준
별 1,171개, 포크 104개를 기록하고 있었고,
하루 뒤인 9월 11일에는 별 1,603개, 포크 144개, 열린 이슈 10개로 늘었다.
이후 GitHub API로 확인한 최근 값은 별 14,210개이고 마지막 푸시는
2026년 10월 1일이다.
요구 사양은 Python 3.12 이상이며, 영문과 중문 README를 함께 제공하고
Discord 커뮤니티를 운영한다.

저장소가 내세우는 핵심은 네 가지다.
앱 경계를 넘나드는 크로스 앱 자동화,
접근성 트리와 OCR과 시각 모델을 함께 쓰는 멀티모달 요소 탐색,
MCP를 통한 IDE 진단 연결, 그리고 단계당 3~5초로 도는 Flash 실행 프로파일이다.
저장소 상단 배지가 밝히는 멀티모달 지원 대상은
Gemini와 Claude와 GPT-4o와 Qwen-VL로, 자사 모델에 묶여 있지 않다.
MCP로 연결된 IDE는 단말을 조작하는 데 그치지 않고
Logcat 출력과 스크린샷을 회수한다.
요소 탐색은 접근성 계층과 OCR에 시각 모델을 결합해
Canvas와 Compose와 Flutter로 그린 맞춤 인터페이스까지 다룬다고 밝힌다.
README 첫머리의 데모는 Google 지도에서 주행 경로를 설정하고
총 소요 시간을 계산한 뒤 YouTube를 열어 Coldplay 곡을 재생하는 흐름으로,
한 지시 안에서 앱 세 개를 오가는 장면을 내세운다.
성능 지표로는 구글 리서치의 AndroidWorld 벤치마크에서
20개 이상 앱과 100개 이상 다단계 과제에 대해 99% 이상 완료율을 주장한다.

설치는 저장소를 복제한 뒤
`./start.sh`(macOS·리눅스) 또는 `.\start.bat`(윈도우 PowerShell)를
실행하는 한 번의 명령으로 끝난다.
이 스크립트는 ADB, scrcpy, FFmpeg, `uv`를 자동으로 설치하고,
`http://localhost:8000`에
단말 연결 마법사와 화면 미러링, 프롬프트 샌드박스, 실행 리플레이를 갖춘
웹 콘솔을 띄운다.
동시에 감지된 AI IDE에
전역 MCP 설정과 테스트 사고방식 규칙 파일(`mcp_server/rules.md`)을
설치할지 묻는다.

## 사용 방식

ARTEMIS는 네 가지 표면을 제공한다.

| 표면       | 진입점                  | 쓰임새                                        |
| ---------- | ----------------------- | --------------------------------------------- |
| 웹 콘솔    | `uv run artemis ui`     | 화면 실시간 투사, 자연어 지시, 실행 리플레이  |
| MCP 서버   | `artemis mcp --install` | IDE 채팅에서 실제 단말로 버그 재현과 테스트   |
| CLI        | `uv run artemis run`    | 자동화 케이스, 탐색적 안정성 점검, 벤치마크   |
| Python SDK | `artemis-client`        | pytest·CI 파이프라인 통합, Pydantic 구조 출력 |

MCP 설치 대상으로 이름이 올라간 클라이언트는
Antigravity, Cursor, Claude Code, Codex, Windsurf, VS Code, Cline/Roo,
OpenClaw다.
`uv run artemis mcp --install all` 한 번으로 전부 설정되고,
`--generate-config <client>`로 TOML이나 JSON 조각만 출력받아
직접 붙일 수도 있다.
Antigravity 설정에는
`mobile_run_task`, `mobile_manage_task`, `mobile_get_device_state`,
`mobile_inspect_trace`, `mobile_diagnose` 다섯 도구를
`eager: true`로 올리는 항목이 들어 있다.

Claude Code용 설치는 규칙을 사용자 전역 규칙 디렉터리에 넣으며,
README는 두 곳에 중복 설치하지 말라고 명시한다.
`CLAUDE.md`와 `rules/*.md`를 둘 다 읽기 때문에
중복은 컨텍스트 낭비라는 이유다.

## 설치와 첫 실행

준비물은 USB 디버깅을 켠 안드로이드 단말이나 에뮬레이터 한 대다.
저장소의 시작 스크립트가 ADB, scrcpy, FFmpeg, Python 의존성(`uv`)을 찾아
없으면 설치하고, 감지한 IDE에 MCP 설정과 테스트 규칙을 넣을지 묻는다.

```bash
# macOS와 Linux
git clone https://github.com/google/artemis.git && cd artemis
./start.sh
```

```powershell
# Windows PowerShell (CMD에서는 start.bat)
git clone https://github.com/google/artemis.git
cd artemis
.\start.bat
```

스크립트가 끝나면 `http://localhost:8000`이 열리고,
단말 연결 마법사, 실시간 화면 미러링, 프롬프트 샌드박스, 실행 리플레이가 나온다.
README는 PowerShell이 현재 디렉터리의 스크립트를 찾지 않으므로
`.\start.bat`처럼 앞에 `.\`를 붙이되 끝에 `\`는 붙이지 말라고 적는다.

모델 키는 두 가지로 넣는다.
`uv run artemis init`이 공급자를 Gemini, OpenAI, Anthropic, OpenRouter 중에서
고르게 하고
키를 입력받은 뒤 연결된 단말을 `adb devices -l`로 찾아 준다.
직접 하려면 `.env.example`을 `.env`로 복사해 키를 채운다.

```bash
cp .env.example .env
# GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY 등 하나 이상을 채운다
uv run artemis doctor
```

`artemis doctor`는 시스템 의존성, 단말 연결, 설정을 점검해 표로 보여 준다.
`--fix`는 손상된 ADB 인증 키와 비정상 종료한 실행기가 남긴 단말 잠금처럼
고칠 수 있는 문제를 고치고, `--json`은 같은 진단을 JSON으로 낸다.
첫 지시는 `uv run artemis run "설정에서 배터리 잔량을 찾아 알려 줘"`처럼 작게
시작한다.

전역으로 `artemis` 명령을 쓰고 싶으면 저장소 루트에서
`uv tool install -e .`를 한 번 실행한다.
웹 콘솔을 다루는 명령은 `artemis restart`, `artemis stop`, `artemis status`다.

## CLI로 실행하기

`artemis run`은 지시 하나를 끝까지 실행한다.
코드의 기본 프로파일은 `pro`이고,
README의 예제는 `--profile flash`를 붙인다.
같은 명령을 아무 옵션 없이 쓰면 Flash보다 느린 Pro가 돈다는 뜻이다.

```bash
# 빠른 반응형 루프로 한 번 실행
uv run artemis run "Open Settings, find Battery and tell me current level" --profile flash

# 특정 단말에 고정하고, 앱 하나로 행동 범위를 제한
uv run artemis run "로그인 화면에서 틀린 비밀번호를 넣고 오류 문구를 확인해 줘" \
  --profile pro \
  --device-serial emulator-5554 \
  --locked-app com.example.app

# APK를 먼저 설치한 뒤 실행
uv run artemis run "앱을 열고 첫 화면의 팝업을 모두 닫아 줘" --app-path ./app-debug.apk
```

주요 옵션은 다음과 같다.

| 옵션                                     | 하는 일                                                           |
| ---------------------------------------- | ----------------------------------------------------------------- |
| `--profile`, `-p`                        | `flash` 또는 `pro`. 기본값은 `pro`                                |
| `--device-serial`, `-s`                  | 단말 일련번호 지정. 에뮬레이터는 `emulator-5554` 형식             |
| `--locked-app`, `-a`                     | 에이전트가 건드릴 수 있는 패키지를 하나로 제한                    |
| `--app-path`                             | 실행 전에 설치할 로컬 APK 경로                                    |
| `--verification-level`                   | Pro의 Checker 수준. `off`, `final`(기본), `checkpoints`, `strict` |
| `--explorer-flash-mode`                  | Flash의 Explorer 등급. `flash`, `pro`, `ultra`                    |
| `--explorer-pro-mode`                    | Pro의 Explorer 등급                                               |
| `--enable-checker/--disable-checker`     | Checker 켜고 끄기                                                 |
| `--enable-outputter/--disable-outputter` | 실행 뒤 보고서와 구조화 출력 합성 켜고 끄기                       |
| `--force-output-synthesis`               | 출력 스키마가 없어도 보고서 합성을 강제                           |
| `--enable-committee`                     | 여러 에이전트가 토론하는 Committee 도구 켜기                      |
| `--standalone`                           | 데몬을 자동으로 띄우지 않고 프로세스 안에서 실행                  |
| `--session-id`                           | 트레이스와 스트림 텔레메트리에 쓸 세션 UUID                       |

`--verification-level`의 네 단계는 이렇게 읽는다.
`off`는 점검이 없고, `final`은 끝날 때 목표 대비 최종 검토만 한다.
`checkpoints`는 계획에 적힌 모든 체크포인트와 최종 검토를 하고,
`strict`는 체크포인트에 수리 예산을 더 주며 assert가 실패하면 멈춘다.
검증을 강하게 할수록 모델 호출이 늘어나므로 비용과 시간이 함께 늘어난다.
이는 이 문서의 추론이다.

여러 지시를 이어서 돌릴 때는 `artemis batch`를 쓴다.
지시를 명령줄 인자로 주거나 `--file`로 한 줄에 하나씩 적은 텍스트 파일
또는 JSON 배열 파일을 준다.

```bash
uv run artemis batch --file tasks.txt --profile flash --delay 5
uv run artemis batch "Wi-Fi를 켜 줘" "블루투스 상태를 알려 줘" --profile pro
```

`batch`의 기본 프로파일도 `pro`이고 기본 간격은 5초다.
모든 지시가 한 에이전트에서 차례로 실행되고 끝나면 성공과 실패를 표로 요약한다.

실행 기록은 `artemis trace list`로 목록을 보고
`artemis trace view <세션 이름>`으로 한 세션을 들여다본다.
`--path`로 트레이스 디렉터리를 바꿀 수 있고, `list`는 `--limit`으로 개수를
제한한다.

## MCP로 IDE에서 쓰기

IDE 안에서 단말을 다루게 하려면 MCP 서버를 설치한다.
한 번에 모든 IDE에 설치하거나 하나만 고를 수 있다.

```bash
uv run artemis mcp --install all          # 지원하는 IDE 전부
uv run artemis mcp --install claude       # Claude Code만
uv run artemis mcp --generate-config codex  # 설정 조각만 출력
```

`--install` 대상은 `antigravity`, `claude`, `cursor`, `windsurf`, `vscode`,
`cline`, `roo`, `openclaw`, `codex`, `all`이다.
수동 설정이 필요하면 `--generate-config`가 출력한 조각을 붙이되,
`command`는 저장소의 `.venv` 파이썬을, `cwd`는 저장소 경로를 가리켜야 한다.
Codex는 `~/.codex/config.toml`에 `[mcp_servers.artemis]` 표를,
Antigravity는 `~/.gemini/jetski/mcp_config.json`에,
Claude Desktop은 `claude_desktop_config.json`에 같은 모양의 JSON을 넣는다.
서버를 직접 띄울 때는 `uv run artemis mcp`이고, 전송 방식은 `--transport`로
`stdio`나 `sse`를 고른다.

설치기는 MCP 설정과 함께 테스트 규칙 파일(`rules.md`)을 IDE별 전역 위치에 둔다.
Claude Code는 `~/.claude/rules/artemis.md`다.
Claude Code가 `~/.claude/CLAUDE.md`와 `~/.claude/rules/*.md`를 둘 다 읽으므로
규칙을 두 곳에 넣으면 컨텍스트만 낭비된다고 README가 경고한다.
규칙 파일은 AI가 화면 전환을 추측하지 말고 먼저 MCP 도구로 앱을 탐색해
실제 경로를 확인한 뒤 테스트 코드를 쓰게 하고,
빠른 동작에는 Flash를, 계획과 검증 지점과 진단이 필요한 일에는 Pro를 고르게
한다.
또 도구가 오류를 내면 먼저 `mobile_diagnose`를 부르게 하고,
키를 채팅으로 주고받지 말라고 한다.

MCP가 여는 도구는 다섯 개다.

| 도구                      | 하는 일                                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| `mobile_run_task`         | 지시를 백그라운드로 시작한다. `device_serial`, Pro의 `verification_level`과 `explorer_mode`를 줄 수 있다 |
| `mobile_manage_task`      | 작업 상태 조회, 중지, 실행 중 지시 주입(`inject_instruction`)                                            |
| `mobile_get_device_state` | 스크린샷이나 OCR과 XML 계층을 실시간으로 본다                                                            |
| `mobile_inspect_trace`    | 트레이스, 동작 오버레이, 에이전트의 추론을 본다                                                          |
| `mobile_diagnose`         | `artemis doctor`와 같은 점검을 IDE 안에서 실행한다                                                       |

`mobile_run_task`는 작업을 분리된 백그라운드 프로세스로 돌리므로 IDE의
에이전트가 막히지 않는다.
끝나거나 실패하면 알림이 간다.
Antigravity는 에이전트를 깨우는 방식, 다른 IDE는 OS 알림 배너와
`notifications.jsonl` 기록이 기본이다.
웹훅은 `OPENCLAW_WEBHOOK_URL`, `MCP_NOTIFICATION_WEBHOOK`, `ARTEMIS_WEBHOOK_URL`
중 하나로,
임의의 명령은 `ARTEMIS_NOTIFY_CMD`에 `{title}`, `{message}`, `{trace_id}`
자리표시자를 넣어 연결한다.

단말이 여러 대면 `device_serial`을 직접 주면 단말마다 잠금이 걸려 병렬로 돌고,
생략하면 준비된 단말을 자동으로 고른다.
README는 단말이 여럿일 때 AI가 사용자에게 어느 단말인지 먼저 물어야 한다고
적는다.

IDE 채팅에서는 이렇게 지시한다.

```text
최신 변경을 APK로 빌드해서 연결된 단말에 설치하고,
테스트 계정으로 로그인 화면을 열어 로그인 뒤 예상치 못한 팝업이 있는지 확인한 다음
마지막 화면의 스크린샷을 돌려줘.
```

## Python SDK로 CI에 붙이기

SDK `artemis-client`는 개발 머신에서 돌고, 단말을 쥔 호스트의 데몬과 HTTP로만
통신한다.
ADB, 에이전트, 모델, 이미지 처리 코드가 없고 런타임 의존성도 0이다.

```bash
uv add "artemis-client @ git+https://github.com/google/artemis.git#subdirectory=packages/artemis-client"
```

```python
import asyncio
import os

from artemis_client import ArtemisClient


async def main() -> None:
    client = ArtemisClient(
        os.environ["ARTEMIS_BASE_URL"],
        token=os.environ.get("ARTEMIS_TOKEN"),
    )

    handle = await client.submit(
        "설정에서 배터리 페이지를 열고 배터리 잔량이 보이는지 확인해 줘",
        profile="flash",
        device_serial="emulator-5554",
    )
    result = await client.wait_for_task(handle.task_id, timeout=600)
    if not result.succeeded:
        raise RuntimeError(result.error or result.status)


asyncio.run(main())
```

한 번에 제출하고 기다리려면 `await client.run("...")`을 쓴다.
`health()`는 서버와 스케줄러가 살아 있는지, `readiness()`는 단말과 도구 체인
진단을,
`list_devices()`는 호스트의 단말 목록을, `stop()`은 작업 하나를 멈춘다.
`submit()`은 클라이언트가 만든 UUID를 `session_id`로 보내 네트워크 재시도에서도
같은 `task_id`를 쓰므로 작업이 중복 생성되지 않는다.

보안 주의가 하나 있다.
현재 데몬의 관리 API에는 원격 인증이 없으므로 포트를 인터넷에 직접 열면 안 된다.
README는 초기에는 SSH 터널을 쓰라고 한다.

```bash
ssh -L 8000:127.0.0.1:8000 user@artemis-host
```

운영에서는 HTTPS와 베어러 토큰 인증을 강제하고 작업 관련 API만 노출하는
리버스 프록시를 앞에 두라고 안내한다.
SDK 0.1이 부르는 엔드포인트는 `POST /api/run`, `GET /api/sessions/{session_id}`,
`GET /api/status`, `POST /api/stop`, `GET /api/devices`,
`GET /api/system/readiness`다.

## 설정 파일

모델과 에이전트 동작은 `config/artemis.jsonc`가 정한다.
최상위 구성은 네 덩어리다.

| 항목      | 역할                                                                                  |
| --------- | ------------------------------------------------------------------------------------- |
| `default` | 모든 하위 에이전트가 따르는 기본 공급자, 모델, `thinking_level`과 대체(fallback) 모델 |
| `presets` | `gemini-flagship`, `gemini-flash`, `openai-gpt4o`, `cost-saving`, `local-ollama`      |
| `nodes`   | planner, operator, explorer, checker 같은 노드별 덮어쓰기                             |
| `agent`   | Flash와 Pro 프로파일 옵션, 기록 압축과 메모리, 영상 분석, Explorer 등급               |

기본 모델은 Gemini 3.8 Flash(`gemini-3.8-flash`)이고 대체 모델은 3.7 Flash다.
`planner`는 `thinking_level`이 `high`, `operator`와 `checker`는 `medium`이다.
Flash의 `max_turns`는 0이라 횟수 상한이 없고,
기록을 상한 대신 압축으로 관리한다.
컨텍스트 예산은 `context_budget_tokens` 80,000이고,
`start_ratio` 0.35, `soft_ratio` 0.7, `hard_ratio` 0.9에서
오래된 스크린샷이 시각 요약으로 바뀌는 시점을 정한다.
Pro의 Checker 설정에는 `final_check`(기본 켜짐), `midway_checks`(기본 꺼짐),
`assert_failure_policy`(`continue`나 `halt`)가 있고,
Committee는 기본으로 꺼져 있다.
`local-ollama` 프리셋은 공급자를 `openai`로 두고 모델을 `llama3.2-vision`으로
지정한다.
OpenAI 분기에만 `base_url`이 있으므로 로컬 Ollama와 vLLM은 OpenAI 호환
엔드포인트로 붙이는 방식으로 읽힌다.
이 해석은 이 문서의 추정이다.

환경 변수로 바꾸는 값도 있다.

| 변수                          | 기본값              | 뜻                                                                      |
| ----------------------------- | ------------------- | ----------------------------------------------------------------------- |
| `ARTEMIS_DEFAULT_PROFILE`     | `flash`             | 프로파일을 주지 않을 때의 기본 프로파일                                 |
| `ARTEMIS_KEEP_DEVICE_AWAKE`   | `true`              | 실행 중 화면을 켜 둔다. 개인 단말이면 `false`                           |
| `ARTEMIS_HIERARCHY_BACKEND`   | `auto`              | UI 계층 수집 방식. `auto`, `helper`, `uiautomator`                      |
| `ARTEMIS_HELPER_AUTO_INSTALL` | `true`              | 첫 작업에서 접근성 도우미 APK를 자동 설치. 공용이나 개인 폰이면 `false` |
| `ADB_HOST`, `ADB_PORT`        | `127.0.0.1`, `5037` | ADB 서버 주소                                                           |
| `ADB_DEVICE_SERIAL`           | 없음                | 기본으로 쓸 단말 일련번호                                               |
| `OCR_API_KEY`                 | 없음                | 고급 OCR을 위한 Google Cloud Vision 키(선택)                            |

`.env.example`의 `ARTEMIS_DEFAULT_PROFILE`은 `flash`인데
CLI의 `--profile` 기본값은 `pro`다.
둘의 우선순위는 이 문서가 코드로 확인하지 못했다.
혼동을 피하려면 `--profile`을 항상 명시하는 편이 안전하다.
이는 이 문서의 권고다.

## 문제가 생겼을 때

가장 먼저 `uv run artemis doctor`를 돌린다.
IDE 안이면 AI에게 `mobile_diagnose`를 부르게 하면 같은 점검이 돈다.
ADB 인증 키가 깨졌거나 이전 실행이 단말 잠금을 남겼다면 `doctor --fix`가 고친다.

접근성 도우미가 말썽이면 다음을 쓴다.
`uv run artemis helper status`로 상태를 보고,
`uv run artemis helper install`로 미리 설치해 첫 작업의 약 3초 지연을 없애고,
`uv run artemis helper uninstall`로 지운다.
도우미가 작업 중 실패하면 ARTEMIS는 UIAutomator2로 되돌아가고,
작업 타임라인과 `mobile_manage_task` 상태와 최종 보고서에 그 사실을 적는다.
UiAutomation 연결을 쥐는 다른 도구가 있으면 도우미가 억제될 수 있으므로,
그 경우 `ARTEMIS_HIERARCHY_BACKEND=uiautomator`로 바꾼다.

## 실행 프로파일

Flash와 Pro는 같은 도구를 얇게 쓰느냐 두껍게 쓰느냐의 차이가 아니라,
구조가 다른 두 개의 실행 모델이다.

Flash는 단계당 3~5초의 반응형 루프다.
모델 하나가 화면을 보고 생각하고 행동하며, 그래프 오케스트레이션이 없다.
기본값으로 턴 수 제한이 없는데
(`agent.flash.max_turns`, 0이면 무제한),
히스토리를 잘라내는 대신 압축하기 때문이다.
오래된 스크린샷은 시각 요약으로 접히고,
끝난 단계는 시대(era) 단위로 묶여
`search_history`와 `replay_steps`로 다시 꺼낼 수 있으며,
세션 녹화는 `video_analyzer`로 질의한다.
사라지는 컨트롤 바나 토스트 같은 일시적 UI는
여러 탭을 `click_sequence` 하나로 이어서 처리한다.
대신 작업 계획도 노트도 없고,
실행 전 안전망도 체크포인트 검증도 최종 보고도 없으며,
ADB 셸도 쓰지 못한다.

Pro는 단계당 15~40초가 걸리는 다중 에이전트 그래프다.
Planner가 마일스톤과 `verify`·`assert` 점검 항목을 담은
살아 있는 마크다운 작업 계획을 유지하고,
Operator가 전체 도구를 써서 그것을 실행한다.
모든 개별 행동은 XML을 먼저 보고 픽셀로 보조 확인하는
Safety Net을 통과하며,
여러 행동을 연달아 쏘는 fast-action burst로 일시적 UI의 지연을 앞지른다.
행동이 막히거나 실패하면 실행 인시던트가 열려
이후 행동이 성공할 때까지 Operator의 컨텍스트에 남는다.
읽기 전용 Checker가 계획 체크포인트를 검증하고
종료 시 원래 목표에 대한 최종 리뷰를 수행한다
(`--verification-level`: `off`/`final`/`checkpoints`/`strict`).

주목할 설계 하나는
Explorer 그라운딩의 등급(`flash`/`pro`/`ultra`)이 사용자 설정이라는 점이다.
`config/artemis.jsonc`의 `pro.explorer.mode`나 `flash.explorer_mode`,
또는 `--explorer-pro-mode`로 정하며, 에이전트가 스스로 고르지 못한다.

## 모델과 인증

ARTEMIS가 내부 에이전트에 쓰는 모델은 `artemis/llm/router.py`의 라우터가 고른다.
이 문서가 읽은 라우터는 Gemini(`google`), Vertex AI, OpenAI,
Anthropic, OpenRouter, 로컬 Ollama와 vLLM을 공급자로 구분한다.
`.env.example`에는 `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`,
`ANTHROPIC_API_KEY`, `OPEN_ROUTER_API_KEY`, `XAI_API_KEY`가 있고,
적어도 하나를 채우라고 안내한다.

Claude를 고르면 라우터는 LangChain의 `ChatAnthropic`을 만들고
`api_key`에 엔드포인트 설정, `ANTHROPIC_API_KEY` 설정값,
같은 이름의 환경 변수 중 처음 잡히는 값을 넘긴다.
이 분기에는 로그인이나 OAuth 토큰을 받는 코드가 없고,
OpenAI 분기에 있는 `base_url` 지정도 없다.
확장 사고(thinking)는 `reasoning_effort`를 토큰 예산 2,048, 8,192, 32,768로
옮겨 켠다.

따라서 Claude Pro나 Max 같은 월정액만으로는 ARTEMIS 내부 모델로 Claude를 쓸 수
없다.
월정액 계정은 API 키를 주지 않고,
Anthropic은 구독 계정의 OAuth 인증을 Claude Code와 자사 앱을 위한 것으로
한정한다.
제3자 개발자가 구독 자격으로 요청을 보내게 하는 것도 허용하지 않고
API 키나 지원되는 클라우드 공급자 자격을 쓰라고 한다.[^anthropic-legal]
Claude를 내부 모델로 쓰려면 종량제 API 키가 필요하다.

키 하나로 끝나지도 않는다.
기본 설정 파일은 화면 좌표를 잡는 `object_detector` 노드에
`gemini-robotics-er-2-preview`를 지정해 두었고,
주석은 Claude를 포함한 일반 모델에는 정밀한 좌표 탐지용 미세 조정이 없어
이 노드는 Gemini ER 계열이어야 하며 다른 모델은 좌표 탐지에 실패한다고 경고한다.
Flash 프로파일의 Explorer 기본 등급 `flash`가 이 노드에 일을 넘기므로,
Claude만 쓰는 구성은 Explorer 등급을 `pro`나 `ultra`로 올려야 한다.
`pro`와 `ultra`는 Gemini 네이티브 엔진과 범용 LangChain 엔진을 둘 다 지원한다고
적혀 있다.
단계 요약기, 기록 압축, 패키지 찾기 노드의 기본 모델도 Gemini라서
Claude로 바꾸려면 `nodes`와 `agent` 항목을 따로 고쳐야 한다.
이 내용은 설정 파일의 주석을 읽은 것이고,
Claude 전용 구성을 이 문서가 실행해 보지는 못했다.

월정액을 쓸 수 있는 길은 MCP 쪽에 있다.
구독으로 로그인한 Claude Code가 ARTEMIS의 MCP 서버를 통해 단말을 다루는 구성은
Claude Code의 정상적인 사용이고,
Anthropic도 사용자가 수정하지 않은 Claude Code에 자기 구독으로 로그인하는 것은
막지 않는다고 적는다.[^anthropic-legal]
다만 README는 ADB, 에이전트, 모델, 이미지 처리가 단말을 쥔 호스트에 남는다고
설명한다.
그래서 `mobile_run_task`가 돌리는 ARTEMIS 내부 에이전트의 모델은
여전히 호스트의 공급자 설정을 따를 것으로 보인다.
`mobile_run_task`가 항상 내부 에이전트를 거치는지는 이 문서가 코드로 확인하지
못했고,
이는 이 문서의 추정이다.
정리하면 구독은 Claude Code의 두뇌에 쓰이고,
ARTEMIS 내부의 화면 인식과 행동 결정에는 따로 고른 모델의 키가 든다.

## 단말에 설치되는 것

첫 작업을 돌리면 Artemis Accessibility Helper라는 작은 접근성 서비스가
단말에 설치된다.
UiAutomation 연결을 점유하지 않고 화면 구조를 읽기 위한 것이며,
UiAutomation을 쓰는 다른 도구는 `FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES`를
켜지 않으면 이 서비스를 억제할 수 있다고 README가 설명한다.
사용자에게는 “Artemis test helper is running”이라는 접힌 알림과
설정의 접근성 메뉴에 생긴 항목으로 보이고, 단말 안에서만 수신하며
다른 곳으로 아무것도 보내지 않는다고 한다.
첫 작업의 약 3초 지연은 `uv run artemis helper install`로 미리 설치해 피한다.
상태는 `uv run artemis helper status`나 `uv run artemis doctor`로 보고,
`uv run artemis helper uninstall`로 언제든 지운다.
UIAutomator2를 대신 쓰려면 `.env`에 `ARTEMIS_HIERARCHY_BACKEND=uiautomator`를,
자동 설치를 막으려면 `ARTEMIS_HELPER_AUTO_INSTALL=false`를 둔다.
작업 도중 이 서비스가 실패하면 UIAutomator2로 되돌아가며,
그 사실을 작업 타임라인과 `mobile_manage_task` 상태와 최종 보고서에 밝힌다고
한다.
수신 범위에 대한 README의 설명을 이 문서가 코드로 확인하지는 못했다.

## 출처 표기 논란

README 하단의 라이선스 항목은 Google 소유가 아닌 코드가 `third_party/` 아래에
업스트림 프로젝트별 디렉터리로 들어 있다고 하며,
그 예로 Minitap, Inc.의 mobile-use 일부(Apache License 2.0)를 든다.
이 문구는 처음부터 있던 것이 아니다.
2026년 9월 11일 mobile-use 팀은 ARTEMIS가 자신들의 코드를 포함하는데
Minitap과 mobile-use와 기여자에 대한 언급이 없다는 이슈를
열었다.[^mobile-use-issue]
이슈는 초기 `pyproject.toml`에 mobile-use의 버전 번호 3.6.3과 원저자 세 명이
Google LLC 저작권 머리말 아래 있었고,
교체된 커밋에서 그 이름들이 다른 저자로 바뀌었으며
나머지 228개 파일은 그대로였다고 주장했다.[^mobile-use-issue]
공유된 코드의 예로 ADB 터널 구현, 플래너 보조 함수, 앱 잠금 유틸리티,
에이전트 프롬프트, SDK 예제를 들었다.[^mobile-use-issue]
요구 사항은 README 감사 문구, 관련 파일의 업스트림 저작권 고지 복원,
원저자와 기여자 표기였다.[^mobile-use-issue]

이슈는 9월 15일에 닫혔다.
댓글에 따르면 저장소가 커밋 371aa6d에서 README에 Minitap 표기를 넣고
관련 파일의 업스트림 저작권 머리말을 되살렸다.[^mobile-use-issue]
다만 다른 참가자는 그 조치가 완전하지 않다며
여전히 mobile-use와 비슷한 파일 열세 개의 목록을 제시했고,
한 참가자는 이를 바로잡는 풀 리퀘스트를 냈다고 적었다.[^mobile-use-issue]
이 문서는 코드를 대조해 보지 않았고, 이슈 안의 주장과 조치 보고를
그 내용대로 전할 뿐이다.
AndroidWorld 점수를 둘러싼 비교(mobile-use 쪽 100%, ARTEMIS 99.1%)도
이슈 댓글 한 건의 주장이며 이 문서가 확인하지 못했다.[^mobile-use-issue]

## 분석

### 테스트 팀이 만든 도구라는 출신이 설계 전반에 드러난다

이 저장소를 만든 팀은 연구 조직이 아니라 Pixel의 테스트 엔지니어링 조직이다.
그 차이는 기능 목록보다 무엇을 기본값으로 두었는지에서 더 잘 보인다.
실행 리플레이, 트레이스 검사 도구, 구조화된 단언(assertion) 출력,
pytest 통합, `--verification-level` 같은 항목은
데모를 인상적으로 만드는 기능이 아니라
실패한 실행을 사후에 설명해야 하는 사람이 요구하는 기능이다.

특히 Pro의 실행 인시던트 처리 방식이 그렇다.
막힌 행동을 별도의 복구 에이전트에게 넘기지 않고,
인시던트를 Operator의 컨텍스트에 남겨 두어 스스로 빠져나오게 한다.
복구 전용 에이전트를 두는 설계가 더 깔끔해 보이지만,
실패 원인이 Operator가 보고 있던 화면 맥락에 있을 때
그 맥락을 다른 에이전트에게 옮기는 비용이 회수되지 않는다는 판단이다.

### 무제한 루프를 가능하게 하는 것은 모델이 아니라 히스토리 압축이다

Flash가 턴 수 상한을 기본으로 두지 않는다는 선택은 대담해 보이지만,
실제로 그것을 지탱하는 것은 압축 설계다.
스크린샷을 시각 요약으로 바꾸고 끝난 단계를 시대 단위로 묶은 다음,
필요할 때만 `search_history`로 되꺼내는 구조는
컨텍스트를 선형으로 쌓지 않겠다는 뜻이다.
장기 실행 에이전트에서 상한을 두는 관행은
대부분 모델 능력의 한계가 아니라 컨텍스트 비용의 한계에서 나왔고,
여기서는 그 비용을 구조로 눌렀다.

이 접근의 대가는 검색 실패다.
압축된 히스토리에서 필요한 조각을 되찾는 일은 그 자체로 검색 문제이며,
잘못된 조각을 꺼내면 상한을 두었을 때보다 더 조용하게 틀린다.
저장소는 이 실패 모드를 어떻게 다루는지 설명하지 않는다.

### Explorer 등급을 에이전트에게 맡기지 않은 것이 이 프로젝트의 가장 분명한 판단이다

Explorer의 `flash`/`pro`/`ultra` 등급을 사용자 설정으로 고정하고
에이전트가 고르지 못하게 막은 것은 작은 설정 항목처럼 보이지만,
실제로는 비용 통제에 대한 입장 표명이다.
에이전트가 자기 추론 예산을 스스로 올릴 수 있게 두면,
어려운 화면을 만날 때마다 등급을 올리는 것이
국소적으로는 항상 합리적인 선택이 된다.
그 결과가 예측 불가능한 청구서라는 것은 이미 여러 에이전트 제품이 겪은 일이다.

### 자사 모델에 묶지 않은 것이 배포 전략의 두 번째 축이다

MCP로 여러 IDE를 겨냥한 것이 배포의 가로축이라면,
멀티모달 지원 대상을 Gemini와 Claude와 GPT-4o와 Qwen-VL로 열어
둔 것은 세로축이다.
구글이 만든 도구가 자사 모델을 요구하지 않는다는 사실은
이 프로젝트가 스스로를 모델 제품이 아니라 인프라로 규정한다는 뜻이다.

이 선택의 논리는 안드로이드 사업의 구조와 같다.
단말 제조사를 묶지 않고 OS를 무료로 풀어 생태계 전체의 기본값을 차지한 방식이
여기서는 모델을 묶지 않고 조작 계층을 푸는 방식으로 반복된다.
모델은 계속 교체되지만 “안드로이드 단말을 에이전트가 조작하는 방법”은
한 번 굳으면 오래 간다. 굳힐 대상을 정확히 고른 셈이다.

동시에 이 개방성은 벤치마크 수치의 해석을 더 어렵게 만든다.
AndroidWorld 99% 이상이라는 결과가 어느 모델에서 나온 것인지
README가 밝히지 않는데,
지원 모델이 넷이면 그 공백의 크기도 넷 배가 된다.
도구의 성능인지 특정 모델의 성능인지를 분리할 수 없다는 점에서,
모델 비종속성은 마케팅에는 이점이고 측정에는 부담이다.

### MCP를 통해 IDE 여덟 개를 동시에 겨냥한 배포 전략

설치 스크립트가 Antigravity, Cursor, Claude Code, Codex, Windsurf,
VS Code, Cline/Roo, OpenClaw를 한 번에 설정한다는 것은,
이 도구가 스스로를 제품이 아니라 기존 코딩 에이전트에 붙는 능력으로
규정한다는 뜻이다.
구글 자사 제품인 Antigravity가 목록 맨 앞에 있고
README 상단에 별도의 워크플로 표까지 있지만,
경쟁 제품을 배제하지 않는다.
안드로이드 단말 조작이라는 능력을 어느 에이전트에서든 쓸 수 있게 하는 편이,
그 능력을 자사 IDE에 가두는 것보다 안드로이드 생태계 전체에 이롭다는 계산이다.

## 비평

### 99%라는 숫자는 벤치마크의 성격을 밝히지 않고 제시된다

AndroidWorld에서 99% 이상이라는 주장은
README에서 가장 먼저 눈에 띄는 수치지만,
어떤 조건에서 측정했는지가 리더보드 이미지 한 장 말고는 제시되지 않는다.
어떤 프로파일로 돌렸는지, 시도 횟수는 몇 번인지,
실패한 1% 미만이 어떤 종류의 과제였는지가 README 본문에 없다.
Flash와 Pro의 단계당 시간이 3~5초와 15~40초로 다섯 배 이상 차이 나는데,
벤치마크 수치가 어느 쪽 것인지 밝히지 않는 것은 사소한 누락이 아니다.

더 근본적인 문제는 AndroidWorld 자체가 구글 리서치의 벤치마크라는 점이다.
같은 회사의 팀이 같은 회사의 벤치마크에서 SOTA를 기록했다는 구성은
그 자체로 부정한 것이 아니지만,
벤치마크 설계가 암묵적으로 가정하는 과제 분포와 도구의 최적화 방향이
겹칠 가능성을 독자가 스스로 할인해야 한다는 뜻이다.
실제 앱 회귀 테스트에서 99%가 재현되리라는 기대는
이 문서가 근거를 대지 않는 기대다.

### 한 번의 스크립트로 여덟 개 IDE 설정을 건드리는 설치 방식은 편의와 침습의 경계에 있다

`./start.sh` 한 줄이 ADB, scrcpy, FFmpeg, `uv`를 설치하고,
감지된 모든 AI IDE의 전역 설정 파일에 MCP 서버 항목과 규칙 파일을 넣는다.
프롬프트로 묻는다고는 하지만,
묻는 대상이 사용자의 홈 디렉터리에 있는 여러 개의 전역 설정이라는 점은
짚어야 한다.
Codex의 `AGENTS.md`나 Antigravity의 `mcp_config.json` 같은
전역 설정 파일은 사용자가 다른 목적으로 이미 손질해 둔 곳이다.

규칙 파일을 전역에 설치한다는 선택은 더 문제적이다.
`rules.md`는 모바일 테스트 사고방식을 담은 문서이며,
안드로이드 작업이 아닌 모든 세션에서도 컨텍스트를 차지한다.
README 스스로 Claude Code에서 규칙을 두 곳에 넣지 말라며
컨텍스트 낭비를 경고하는데,
한 곳에 넣는 것도 안드로이드와 무관한 세션에서는 같은 낭비다.
워크스페이스 단위 설치를 기본으로 하고
전역을 선택지로 두는 편이 일관됐을 것이다.

### 결정론이 필요한 테스트에 비결정적 실행기를 놓는 긴장이 다뤄지지 않는다

회귀 테스트의 가치는 같은 입력에 같은 결과가 나온다는 데 있다.
자연어 지시를 매번 모델이 해석해서 화면을 조작하는 구조는
그 성질을 보장하지 않는다.
README는 Pro 프로파일의 검증 계층으로 신뢰성을 확보한다는 입장이지만,
검증은 결과가 목표에 부합하는지를 보는 것이지
실행 경로가 같았는지를 보는 것이 아니다.

이 차이는 테스트가 실패했을 때 드러난다.
CI에서 어제는 통과하고 오늘은 실패한 케이스를 받았을 때,
앱이 회귀한 것인지 에이전트가 다른 경로를 골랐는지 구분해야 한다.
트레이스와 리플레이가 그 구분을 돕지만 자동화하지는 못하며,
사람이 매번 영상을 봐야 한다면 자동화로 얻은 시간의 상당 부분이
되돌아간다.
Flash의 단계당 3~5초가 매력적인 이유는 빠르기 때문인데,
실패 분석이 사람 손에 남으면 병목은 실행 속도가 아니게 된다.

### 로드맵이 통합보다 확장을 먼저 놓는다

로드맵 네 항목은
안드로이드 스튜디오 통합, iOS 확장, 온디바이스 경량 VLM, 실시간 음성 조작이다.
이 중 앞서 제기한 문제들(결정론, 실패 분석, 벤치마크 조건의 투명성)을
다루는 항목은 없다.
음성 조작은 테스트 자동화에서 어떤 문제를 푸는지 설명되지 않은 채
올라와 있고,
iOS 확장은 안드로이드에서 아직 검증되지 않은 구조를
두 배로 넓히자는 제안이다.

## 인사이트

### 에이전트의 추론 예산을 누가 정하는지가 제품의 성격을 가른다

ARTEMIS가 Explorer 등급을 사용자 설정으로 고정한 것은
지금 에이전트 도구 전반에서 벌어지는 더 큰 문제의 한 사례다.
추론 시간을 늘리면 대체로 결과가 좋아지므로,
에이전트에게 그 결정을 맡기면 에이전트는 거의 항상 늘리는 쪽을 고른다.
개별 결정마다는 타당하지만 합계는 통제되지 않는다.

이 구조는 조직 안의 예산 결정과 같은 모양이다.
각 팀에게 “필요하면 더 쓰라”고 하면
각 팀은 언제나 필요하다고 판단하며,
그래서 예산은 팀이 아니라 상위 층위에서 정해진다.
에이전트 설계에서 아직 이 유비가 충분히 받아들여지지 않았고,
자율성을 늘리는 것이 곧 개선이라는 전제가 남아 있다.

앞으로 이 경계선은 제품 차별화 지점이 될 것이다.
어떤 결정이 에이전트의 것이고 어떤 결정이 설정 파일의 것인지를
명시적으로 그은 도구가,
모든 것을 에이전트에게 맡긴 도구보다 조직 안에서 채택되기 쉽다.
비용을 예측할 수 있어야 승인이 떨어지기 때문이다.

### 모바일 테스트 자동화의 병목은 실행이 아니라 실패 해석으로 옮겨 간다

Appium이나 Espresso 시대에
테스트 자동화의 비용은 대부분 작성과 유지보수에 있었다.
화면이 바뀌면 셀렉터가 깨지고, 깨진 셀렉터를 고치는 일이 반복됐다.
ARTEMIS 같은 도구는 그 비용을 실제로 줄인다.
자연어 지시는 셀렉터보다 화면 변경에 강하다.

그런데 비용은 사라지지 않고 자리를 옮긴다.
셀렉터가 깨졌을 때는 실패 원인이 명확했다.
요소를 못 찾았다는 것이 로그에 그대로 남는다.
모델이 화면을 잘못 읽었을 때는 그런 명확한 신호가 없다.
에이전트는 그럴듯한 다른 행동을 하고, 결과만 틀린다.
ARTEMIS가 트레이스, 리플레이, `video_analyzer`, `mobile_inspect_trace`에
이만큼 투자한 것은 이 이동을 이미 알고 있다는 증거다.

두 번째 효과가 여기서 나온다.
테스트 인프라의 저장 비용과 관측 비용이 실행 비용을 앞지르게 된다.
셀렉터 기반 테스트는 실패 로그 몇 줄이면 됐지만,
에이전트 기반 테스트는
실패마다 영상과 단계별 스크린샷과 추론 기록을 남겨야 설명이 가능하다.
CI에서 하루 수천 건을 돌리는 조직에게 이것은 새로운 종류의 예산 항목이며,
아직 아무도 그 크기를 공개하지 않았다.

### 구글이 안드로이드 조작 능력을 모든 IDE에 열어 준 것은 관대함이 아니라 표준 선점이다

설치 스크립트가 경쟁 제품인 Cursor, Windsurf, Claude Code, Codex까지
한 번에 설정한다는 사실은 선의로 읽히기 쉽지만,
플랫폼 소유자의 전략으로 보면 다르게 보인다.
안드로이드 단말을 에이전트가 조작하는 방식이 표준화되지 않은 지금,
여러 도구가 각자의 방식으로 ADB를 감싸기 시작하면 파편화된다.
구글이 먼저 무료로 잘 만든 것을 모든 IDE에 깔아 두면,
그 인터페이스가 사실상의 표준이 된다.

역사적 유비는 안드로이드 스튜디오 자체다.
구글은 IntelliJ 위에 무료 IDE를 얹어 안드로이드 개발 환경을 통일했고,
그 결과 안드로이드 개발자가 어떤 도구로 무엇을 하는지에 대한
기본값을 구글이 정하게 됐다.
MCP 서버는 같은 일을 에이전트 층위에서 시도하는 것이며,
이번에는 IDE를 만들 필요도 없다.
남의 IDE에 도구 다섯 개를 등록하면 된다.

여기서 장기적 긴장이 생긴다.
`mobile_run_task`나 `mobile_diagnose`가
안드로이드 자동화의 공용 어휘가 되면, 그 어휘의 변경권은 구글에 남는다.
Apache-2.0 라이선스는 포크할 자유를 주지만,
인터페이스 표준의 힘은 코드가 아니라 채택률에서 나온다.
지금 이 저장소를 편의로 받아들이는 결정은 몇 년 뒤 의존으로 읽힐 수 있다.

### 실행 인시던트를 컨텍스트에 남겨 두는 방식은 다중 에이전트 설계의 유행에 대한 반례다

지난 몇 년 다중 에이전트 설계의 기본 문법은 역할 분리였다.
계획자, 실행자, 검증자, 복구자를 나누고
각자에게 좁은 책임을 주는 구성이 반복해서 제안됐다.
ARTEMIS는 Planner와 Operator와 Checker는 나누면서 복구자만 두지 않고,
실패를 Operator의 컨텍스트에 남기는 쪽을 골랐다.

이 선택이 시사하는 것은 역할 분리의 비용이 맥락 이전에 있다는 점이다.
계획과 검증은 실행 맥락 없이도 가능한 작업이지만,
복구는 실패 직전에 화면에서 무엇을 보고 있었는지를 알아야 하는 작업이다.
그 맥락을 요약해서 넘기는 순간
복구자는 실패의 재현이 아니라 실패의 설명을 받게 되고,
설명은 대개 실패의 원인을 이미 놓친 상태다.

이 기준은 다른 에이전트 시스템에도 적용된다.
역할을 나눌지 말지는 책임의 논리적 구분이 아니라,
그 역할이 필요로 하는 맥락이 요약을 견디는지로 판단해야 한다.
요약을 견디는 작업은 나누고,
원본 맥락이 있어야 하는 작업은 같은 에이전트 안에 두는 것이 낫다.

---

[^mobile-use-issue]: GitHub, [Missing attribution to mobile-use and its contributors](https://github.com/google/artemis/issues/40), 2026-09-11

[^anthropic-legal]: Claude Code Docs, [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
