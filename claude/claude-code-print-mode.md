# `claude -p`: Claude Code를 프로그램으로 실행하는 비상호작용 모드(print mode)

<https://code.claude.com/docs/en/headless>

## 목차

- [소개](#소개)
  - [이름이 여러 개인 이유](#이름이-여러-개인-이유)
  - [이 문서의 범위](#이-문서의-범위)
- [기본 실행](#기본-실행)
  - [종료 코드와 오류의 위치](#종료-코드와-오류의-위치)
  - [슬래시 명령은 일부만 된다](#슬래시-명령은-일부만-된다)
- [입력](#입력)
  - [프롬프트 인자와 표준 입력](#프롬프트-인자와-표준-입력)
  - [스트리밍 입력](#스트리밍-입력)
  - [빌드 스크립트에 넣기](#빌드-스크립트에-넣기)
- [출력 형식](#출력-형식)
  - [json](#json)
  - [구조화 출력](#구조화-출력)
  - [stream-json](#stream-json)
  - [subagent 메시지 따라가기](#subagent-메시지-따라가기)
  - [API 재시도 이벤트](#api-재시도-이벤트)
  - [세션 메타데이터: system/init](#세션-메타데이터-systeminit)
  - [CI에서 플러그인이나 MCP 서버가 안 뜬 것을
잡기](#ci에서-플러그인이나-mcp-서버가-안-뜬-것을-잡기)
  - [플러그인 설치 이벤트](#플러그인-설치-이벤트)
- [권한](#권한)
  - [도구 자동 승인: --allowedTools](#도구-자동-승인---allowedtools)
  - [규칙 문법](#규칙-문법)
  - [세션 전체 기준: --permission-mode](#세션-전체-기준---permission-mode)
  - [승인해 줄 사람이 없을 때: --permission-prompts
none](#승인해-줄-사람이-없을-때---permission-prompts-none)
- [--bare: 재현 가능한 실행](#--bare-재현-가능한-실행)
  - [인증](#인증)
  - [필요한 맥락은 플래그로 직접](#필요한-맥락은-플래그로-직접)
  - [실행 중의 제한](#실행-중의-제한)
  - [신뢰하지 않은 폴더에서의 -p](#신뢰하지-않은-폴더에서의--p)
- [시스템 프롬프트](#시스템-프롬프트)
- [세션 이어가기](#세션-이어가기)
- [실행 제어](#실행-제어)
  - [턴 수와 예산](#턴-수와-예산)
  - [끝난 뒤의 백그라운드 작업](#끝난-뒤의-백그라운드-작업)
  - [SIGTERM과 SIGINT](#sigterm과-sigint)
  - [작업 디렉터리가 지워졌을 때](#작업-디렉터리가-지워졌을-때)
- [CI 통합](#ci-통합)
  - [두 가지 동작 방식](#두-가지-동작-방식)
  - [CLI 인자 전달](#cli-인자-전달)
  - [비용과 자격 증명](#비용과-자격-증명)
- [비용과 요금제](#비용과-요금제)
  - [2026년에 있었던 두 번의 변화](#2026년에-있었던-두-번의-변화)
  - [월별 API 크레딧](#월별-api-크레딧)
  - [개발자 반응](#개발자-반응)
  - [비용을 줄이는 선택](#비용을-줄이는-선택)
- [실전 스크립트](#실전-스크립트)
  - [감싸개 스크립트: 재시도와 성공 판정](#감싸개-스크립트-재시도와-성공-판정)
  - [커밋 전 검사: 비밀 값 먼저, 모델은 나중,
실패하면 통과](#커밋-전-검사-비밀-값-먼저-모델은-나중-실패하면-통과)
  - [파일별 일괄 작업: 하나씩 하고 검증하고
되돌리기](#파일별-일괄-작업-하나씩-하고-검증하고-되돌리기)
  - [주기 실행(cron): 환경이 비어 있다는
전제](#주기-실행cron-환경이-비어-있다는-전제)
  - [PR 리뷰 게시](#pr-리뷰-게시)
- [현장에서 보고된 문제](#현장에서-보고된-문제)
  - [입력이 끝나지 않으면 조용히 멈춘다](#입력이-끝나지-않으면-조용히-멈춘다)
  - [3초 동안 입력이 없으면 입력 없이
진행한다](#3초-동안-입력이-없으면-입력-없이-진행한다)
  - [터미널 없는 부모 프로세스에서 병렬 subagent가
멈춘다](#터미널-없는-부모-프로세스에서-병렬-subagent가-멈춘다)
  - [이 보고들에서 얻는 점검표](#이-보고들에서-얻는-점검표)
- [커뮤니티가 쓰는 방식](#커뮤니티가-쓰는-방식)
- [레시피](#레시피)
- [비평](#비평)
  - [종료 코드만으로는 성공을 알 수 없다](#종료-코드만으로는-성공을-알-수-없다)
  - [조용히 사라지는 실패가 많다](#조용히-사라지는-실패가-많다)
  - [--bare는 안전하지만 가볍지는 않다](#--bare는-안전하지만-가볍지는-않다)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)

## 소개

`claude -p`(`--print`)는 Claude Code에 프롬프트 하나를 주고,
에이전트가 일을 마치면 결과를 출력한 뒤 끝나는 비상호작용 실행이다.
공식 문서는 이를 “CLI로 쓰는 Agent SDK”로 설명한다.
같은 도구, 같은 에이전트 루프, 같은 컨텍스트 관리를 셸 스크립트와 CI에서 쓰게 해
주는 입구라는 뜻이다.
Python이나 TypeScript 패키지가 주는 구조화 출력, 도구 승인 콜백,
타입이 있는 메시지가 필요하면 Agent SDK 문서를 보라고 같은 페이지가 안내한다.
SDK와의 비교는 [Claude Agent SDK](agent-sdk.md) 문서에 있고,
이 문서는 `claude -p` 자체만 다룬다.

### 이름이 여러 개인 이유

같은 기능을 문서마다 다르게 부른다.
헤드리스 페이지의 제목은 “Run Claude Code programmatically”이고,
주소는 옛 이름을 따라 `/headless`다.
CLI reference는 `-p` 전용 플래그를 “print mode only”로 적는다.[^cli]
이 문서는 기능 이름으로 print mode를, 명령어로 `claude -p`를 쓴다.

### 이 문서의 범위

기본 실행, 입력, 출력 형식, 권한, `--bare`, 시스템 프롬프트, 세션,
실행 제어와 종료, CI 통합을 순서대로 다룬다.
각 절은 플래그가 무엇을 하는지에 더해, 스크립트에서 무엇이 어긋나기 쉬운지를
함께 적는다.
뒤쪽에는 요금제와 비용, 바로 가져다 쓸 수 있는 스크립트, 현장에서 보고된 문제,
커뮤니티 사례를 모았다.
버전 조건은 공식 문서가 적은 것만 옮겼다.

## 기본 실행

`claude` 명령 어디에나 `-p`를 붙이면 비상호작용으로 실행된다.

```bash
claude -p "What does the auth module do?"
```

모든 CLI 옵션이 `-p`와 함께 쓰이지는 않는다.
Claude Code는 `--bg`를 거부하고, 작업 설명이 붙은 `--cloud`도 충돌한 옵션 이름을
밝히는 오류와 함께 거부한다.
세션 ID를 준 `--cloud`와 `-p`의 조합은 오류가 아니라 그 클라우드 세션에 메시지를
대기열로 넣고 끝난다.
자주 함께 쓰는 옵션은 `--continue`, `--allowedTools`, `--output-format`이다.

### 종료 코드와 오류의 위치

성공하면 종료 코드 0, 실행이 실패하면 0이 아닌 값이다.
스크립트는 종료 상태로 분기할 수 있다.
잘못된 플래그는 실행 전에 stderr로 오류가 나온다.
반면 인증 누락처럼 실행 도중 생긴 실패는 오류가 아니라 결과로 stdout에 찍힌다.
그래서 `json` 출력을 파싱하는 스크립트는 종료 코드만 믿지 말고 결과 객체의
내용도 확인해야 한다.

### 슬래시 명령은 일부만 된다

`-p`에서는 사용자가 부르는 skills와 사용자 정의 명령이 동작한다.
프롬프트 문자열에 `/skill-name`을 넣으면 Claude Code가 실행 전에 펼친다.
`/login`처럼 터미널 인터페이스에서만 도는 내장 명령은 쓸 수 없다.
`/model`, `/effort`, `/fast`, `/color`,
`/rename`은 `/model sonnet`처럼 값을 인자로 받는다.
인자 없는 `/mcp`는 서버 상태를 텍스트로 요약해 출력한다.
설정은 `/config thinking=false`처럼 `key=value`로 바꾼다.
`/output-style <style>`은 출력 스타일을 바꾸고 인자 없이 쓰면 목록을 보여 주며,
Claude Code v2.1.269 이상이 필요하다.

## 입력

### 프롬프트 인자와 표준 입력

프롬프트는 명령줄 인자로 주고, 데이터는 표준 입력으로 파이프한다.
다른 명령줄 도구처럼 입력을 넣고 응답을 리디렉션할 수 있다.
빌드 로그를 넘겨 설명을 파일에 저장하는 식이다.

```bash
cat build-error.txt | claude -p "이 빌드 오류의 근본 원인을 설명해줘" > output.txt
```

파이프로 넘기는 stdin은 10MB까지다.
넘으면 Claude Code는 분명한 오류와 함께 0이 아닌 상태로 끝난다.
더 큰 입력은 파일에 쓰고 프롬프트에서 그 경로를 가리키라고 공식 문서가 안내한다.
stdin을 읽을 수 없으면, 예컨대 실행한 프로세스가 입력 끝을 끊어 버렸으면,
Claude Code는 stderr에 경고를 내고 명령줄의 프롬프트로 계속한다.

### 스트리밍 입력

`--input-format stream-json`은 입력도 JSON 이벤트로 받는다.[^cli]
프롬프트를 텍스트로 넘긴 실행과 이 모드는 종료 시 동작이 다르다.
예약된 `/loop` 깨우기를 기다리는 동작은 프롬프트를 텍스트로 넘긴
실행에만 적용된다.

### 빌드 스크립트에 넣기

비상호작용 호출을 스크립트로 감싸면 프로젝트 전용 린터나 리뷰어로 쓸 수 있다.
공식 문서의 예는 `main`과의 diff를 파이프로 넘겨 오타만 보고하게 하는
`package.json` 스크립트다.
diff를 파이프로 넘기면 Claude에게 그것을 읽을 Bash 권한을 줄 필요가 없다는
점이 요지다.
이스케이프한 큰따옴표는 스크립트를 Windows에서도 쓰이게 한다.

```json
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

`npm run lint:claude`로 실행한다.

## 출력 형식

`--output-format`은 세 가지다.[^cli]

| 값            | 내용                                            |
| ------------- | ----------------------------------------------- |
| `text` (기본) | 일반 텍스트                                     |
| `json`        | 결과, 세션 ID, 메타데이터를 가진 JSON 객체 하나 |
| `stream-json` | 실시간 스트리밍을 위한 줄바꿈 구분 JSON(NDJSON) |

### `json`

결과 텍스트는 `result` 필드에 들어 있다.

```bash
claude -p "이 프로젝트를 요약해줘" --output-format json | jq -r '.result'
```

`json` 응답에는 `total_cost_usd`와 모델별 비용 내역이 들어 있어서,
스크립트가 사용량 대시보드를 보지 않고도 지출을 추적할 수 있다.
`--continue`나 `--resume`으로 이어간 실행은 이전 실행의 지출을 포함한 대화 전체
합계를 보고한다.
두 값 모두 클라이언트가 계산한 추정치라서 실제 청구액과 다를 수 있다.[^cost]

### 구조화 출력

`--json-schema`에 JSON Schema를 주면 스키마에 맞는 값이 응답의
`structured_output` 필드에 들어온다.
요청에 대한 메타데이터(세션 ID, 사용량 등)는 같은 응답에 함께 있다.

```bash
claude -p "auth.py에서 함수 이름을 모두 뽑아줘" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

스키마가 유효한 JSON Schema가 아니면 `claude`는 `Error: --json-schema is not a
valid JSON Schema`와 검증기의 진단 메시지를 내고 끝난다.
`"format": "email"` 같은 `format` 키워드는 받아들이지만 주석으로만 취급하고
강제하지 않는다.
Claude가 요청을 거절했을 때처럼 유효한 구조화 출력 없이 실행이 끝나면 응답에
`structured_output` 필드가 없다.
따라서 스크립트는 `structured_output`을 쓰기 전에 그 필드가 있는지 먼저
확인해야 한다.

### `stream-json`

토큰이 생성되는 대로 받으려면 `--output-format stream-json`에 `--verbose`와
`--include-partial-messages`를 함께 준다.
각 줄이 이벤트 하나를 나타내는 JSON 객체다.

```bash
claude -p "재귀를 설명하는 시를 써줘" \
  --output-format stream-json --verbose --include-partial-messages
```

스트림의 마지막 줄은 최종 응답 텍스트, 비용,
세션 메타데이터를 담은 `result` 메시지다.
소비자가 스트림을 느리게 읽으면 Claude Code는 대기 중인 출력이 빠질 때까지
기다린 뒤 끝나며, 남은 양에 비례해 기다리되 30초를 넘기지 않는다.
다음은 `jq`로 텍스트 조각만 골라 이어 붙여 보여 주는 공식 예제의 형태다.
`-r`은 따옴표 없는 원시 문자열을, `-j`는 줄바꿈 없는 이어 붙이기를 뜻한다.

```bash
claude -p "재귀를 설명하는 시를 써줘" \
  --output-format stream-json --verbose --include-partial-messages \
  | jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

콜백과 메시지 객체로 스트리밍하려면 Agent SDK의 실시간 응답 문서를 보라고 공식
문서는 안내한다.

### subagent 메시지 따라가기

subagent와, subagent에서 실행되는 skill의 메시지는 스트림에 `assistant`와 `user`
메시지로 나온다.
`parent_tool_use_id` 필드가 각 메시지가 어느 실행에 속하는지 알려 준다.
메인 대화의 메시지는 이 필드가 `null`이다.
포그라운드에서 도는 subagent나 forked skill의 첫 메시지는 그 실행을 구동하는
프롬프트나 skill 내용을 가진 `user` 메시지다.
그 뒤에는 기본적으로 `tool_use`와 `tool_result` 블록만 나온다.
`--forward-subagent-text` 또는 환경 변수 `CLAUDE_CODE_FORWARD_SUBAGENT_TEXT`를
켜면 텍스트와 생각(thinking) 블록도 나와서 각 실행의 기록을 재구성할 수 있다.
켜면 모든 중첩 깊이의 subagent 메시지가 전달되고,
각 메시지의 `parent_tool_use_id`는 그것을 시작시킨 Agent 또는 Skill 도구 호출의
ID라서 ID를 따라가면 중첩 트리를 복원한다.

| 실행이 시작되는 방식                                    | `parent_tool_use_id`            | 메시지가 도착하는 때                     |
| ------------------------------------------------------- | ------------------------------- | ---------------------------------------- |
| Claude가 메인 대화에서 Agent 도구를 호출                | 그 Agent `tool_use` 블록의 ID   | subagent가 일하는 동안                   |
| Claude가 메인 대화에서 forked skill용 Skill 도구를 호출 | 그 Skill `tool_use` 블록의 ID   | forked skill이 일하는 동안               |
| 프롬프트로 `/<skill-name>`을 직접 전달                  | `forked-command-`로 시작하는 값 | forked skill이 끝난 뒤 한꺼번에 순서대로 |

프롬프트로 시작한 forked skill은 `forked-command-` 뒤의 이름이 입력한 것과 다를
수 있으므로 접두사로 매칭해야 한다.
메시지가 스트림에서 빠져 있다면 버전을 확인한다.
Claude가 Skill 도구로 시작한 forked skill은 `tool_use`와 `tool_result` 블록이
v2.1.86 이상, 첫 `user` 메시지와 텍스트·생각 블록이 v2.1.265 이상이다.
forked skill이 띄운 subagent의 메시지와 subagent 안에서 시작한 forked skill의
메시지는 v2.1.275 이상이다.
프롬프트로 직접 전달한 forked skill의 메시지는 v2.1.287 이상이다.

### API 재시도 이벤트

API 요청이 재시도 가능한 오류로 실패하면 Claude Code는 재시도 전에
`system/api_retry` 이벤트를 낸다.
이 이벤트로 자체 인터페이스에 재시도 진행 상황을 보여 줄 수 있다.
`apiKeyHelper` 자격 증명이 `401`이나 `403`으로 거부되면,
v2.1.246 이상에서는 처음 두 번의 재시도를 이벤트 없이 조용히 하고 세 번째 연속
재시도부터 이벤트를 낸다.
조용한 재시도도 `attempt`에는 센다.

| 필드             | 타입           | 설명                                                              |
| ---------------- | -------------- | ----------------------------------------------------------------- |
| `type`           | `"system"`     | 메시지 종류                                                       |
| `subtype`        | `"api_retry"`  | 재시도 이벤트임을 나타냄                                          |
| `attempt`        | 정수           | 현재 시도 번호(1부터)                                             |
| `max_retries`    | 정수           | 이 실패 원인에 허용된 총 재시도 횟수                              |
| `retry_delay_ms` | 정수           | 다음 시도까지 밀리초                                              |
| `error_status`   | 정수 또는 null | 실패한 시도의 HTTP 상태 코드, API에서 HTTP 응답이 없었으면 `null` |
| `no_response`    | 객체, 선택     | 응답 헤더를 제때 받지 못한 시도에만 있고, v2.1.261 이상이 필요함  |
| `error`          | 문자열         | 오류 범주(`rate_limit`, `overloaded`, `billing_error` 등 12가지)  |
| `uuid`           | 문자열         | 이벤트 고유 식별자                                                |
| `session_id`     | 문자열         | 이벤트가 속한 세션                                                |

`error` 범주는 `authentication_failed`, `oauth_org_not_allowed`,
`account_on_hold`, `billing_error`, `rate_limit`, `overloaded`,
`invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`,
`cloud_credential_error`, `unknown`이다.

### 세션 메타데이터: `system/init`

`system/init` 이벤트는 모델, 도구, MCP 서버,
로드된 플러그인을 포함한 세션 메타데이터를 알린다.
시작 이벤트가 앞서지 않는 한 스트림의 첫 이벤트다.
앞서 나올 수 있는 것은 `CLAUDE_CODE_SYNC_PLUGIN_INSTALL`을 설정했을 때의
`plugin_install` 이벤트, 그리고 `SessionStart`나 `Setup` hook이 도는 동안 나오는
`hook_started`, `hook_progress`, `hook_response` 이벤트다.
이 이벤트에는 선택 필드 `capabilities`(문자열 배열)도 있어서 그 Claude Code
버전이 구현한 프로토콜 동작을 이름으로 알려 준다.
버전 문자열을 비교하는 대신 이 배열로 기능을 감지하고,
모르는 값은 무시하라는 것이 공식 안내다.

### CI에서 플러그인이나 MCP 서버가 안 뜬 것을 잡기

`system/init`의 필드로 로드 실패를 CI에서 잡을 수 있다.

| 필드                | 내용                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `plugins`           | 성공적으로 로드된 플러그인(`name`, `path`)                                                                                                       |
| `plugin_errors`     | 로드 시점 오류(`plugin`, `type`, `message`). 오류가 없으면 키가 없음                                                                             |
| `mcp_servers`       | 세션의 MCP 서버(`name`, `status`)                                                                                                                |
| `mcp_server_errors` | 구성 검증에서 건너뛴 `--mcp-config` 항목(`name`, `type`, `message`). 오류가 없으면 키가 없어서 비어 있지 않은 배열을 CI 실패 조건으로 쓸 수 있음 |

`--mcp-config`를 `-p`와 함께 주면 Claude Code는 첫 턴 전에 아직 연결 중인 서버를
기다리고, 시작 타임아웃 `MCP_TIMEOUT`(기본 30초)까지 기다린다.
캐시된 도구 목록이 있는 원격 서버는 기다리지 않고 `system/init`에 `pending`으로
나타나 첫 도구 호출에서 연결한다.
이 대기는 v2.1.221 이상이 필요하다.
Claude Code는 시작 시 `--mcp-config` 항목을 각각 검증하고 실패한 항목(예:
`type`이 없는 `url` 항목)을 건너뛰며, 실행은 계속되고 정상 종료한다.
그래서 서버가 아예 안 떴는지는 `mcp_server_errors`를 봐야 안다.
터미널에서 직접 실행하면 stderr에 `Warning: 1 MCP server skipped due to invalid
config:` 같은 경고가 나오지만, stderr를 리디렉션하거나 CI 실행기와 SDK 호스트가
캡처하면 경고는 나오지 않는다.
이때는 `mcp_server_errors` 필드가 유일한 보고 수단이다.

### 플러그인 설치 이벤트

`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`을 설정하면 첫 턴 전에 마켓플레이스 플러그인이
설치되는 동안 `system/plugin_install` 이벤트가 나온다.
`status`는 `started`, `installed`, `failed`, `completed` 중 하나이며,
`started`와 `completed`는 전체 설치를 감싸고 `installed`와 `failed`는
마켓플레이스별 결과를 알린다.

## 권한

### 도구 자동 승인: `--allowedTools`

`--allowedTools`는 승인 질문 없이 쓸 도구를 정한다.
`Read`와 `Edit`을 나열하면 네트워크 경로 읽기를 제외하고 파일을 묻지 않고
읽고 고친다.
`Bash`를 나열하면 셸 명령도 같다.
다만 자동 모드(auto mode)로 시작한 실행에서는 맨 `Bash` 항목을 너무 넓은 허용
규칙으로 보고 버리며 명령을 하나씩 평가한다.

```bash
claude -p "테스트를 실행하고 실패를 고쳐줘" \
  --allowedTools "Bash,Read,Edit"
```

나열하지 않은 도구의 호출은 승인이 필요 없으면 그대로 실행된다.
수동(Manual) 모드의 `-p` 실행에서 승인이 필요한 호출은 `PermissionRequest`
hook이나 `--permission-prompt-tool` 같은 승인 주체가 없으면 거부된다.
Claude Code v2.1.302 이상에서는 권한 모드를 정하는 것이 없을 때 `-p` 실행이 수동
모드로 시작한다.

### 규칙 문법

`--allowedTools`는 권한 규칙 문법을 쓴다.
끝의 ` *`는 접두사 매칭이라서 `Bash(git diff *)`는 `git diff`로 시작하는 모든
명령을 허용한다.
`*` 앞의 공백이 중요하다.
공백이 없는 `Bash(git diff*)`는 `git diff-index`까지 맞는다.

```bash
claude -p "스테이지된 변경을 보고 적절한 메시지로 커밋을 만들어줘" \
  --allowedTools "Bash(git diff *)" "Bash(git log *)" "Bash(git status *)" "Bash(git commit *)"
```

### 세션 전체 기준: `--permission-mode`

`--permission-mode`는 도구별 목록 대신 세션 전체의 기준을 정한다.
`-p`에서 공식 문서가 다루는 값은 셋이다.

| 모드          | 동작                                                                                                                                                |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auto`        | 대부분의 동작을 사람 대신 분류기(classifier)가 검토                                                                                                 |
| `dontAsk`     | 원래 승인을 물었을 호출을 모두 거부해서 잠긴 CI 실행에 맞음. 설치된 mod는 그 호출 일부를 여전히 승인할 수 있음                                      |
| `acceptEdits` | 파일 쓰기를 묻지 않고 하며 `mkdir`, `touch`, `mv`, `cp` 같은 흔한 파일 시스템 명령을 자동 승인. 나머지 셸 명령과 네트워크 요청은 허용 항목이 필요함 |

`dontAsk`에서도 수동 모드에서 승인이 필요 없던 동작(작업 디렉터리의 파일 읽기,
읽기 전용 명령 집합)은 그대로 돌고, `--allowedTools` 항목이나
`permissions.allow` 규칙이 덮는 동작도 돈다.
`AskUserQuestion`, 조직이 `ask`로 정한 커넥터 도구,
`requiresUserInteraction`으로 표시된 MCP 도구,
네트워크 경로 읽기는 허용 규칙이 맞아도 거부된다.

```bash
claude -p "린트 오류를 고쳐줘" --permission-mode acceptEdits
```

### 승인해 줄 사람이 없을 때: `--permission-prompts none`

예약된 작업처럼 승인에 답할 사람이 없을 때 쓴다.
이 플래그가 가장 중요한 경우는 실행에 권한 호스트(permission host)가 있을 때다.
`canUseTool` 콜백을 가진 Agent SDK 앱이나 `--permission-prompt-tool`로 준 MCP
도구가 그 예다.
플래그가 없으면 실행은 그 호스트가 각 요청에 답하기를 기다린다.
플래그가 있으면 호스트에 묻지도 기다리지도 않고,
물었을 모든 것은 `PermissionRequest` hook이 허용하지 않는 한 거부된다.
Claude에게는 아무도 승인할 수 없으니 다시 시도하지 말라고 알리고
실행은 계속된다.
호스트가 없는 `-p` 실행에서는 어느 쪽이든 요청이 거부되지만,
플래그는 재시도하지 말라는 말도 Claude에게 전한다.
권한 규칙, `PermissionRequest` hook, 정해 둔 권한 모드가 여전히 먼저 호출마다
결정을 내리고, 그 어느 것도 풀지 못한 요청만 거부한다.

```bash
claude -p "의존성 버전을 갱신하고 테스트를 실행해줘" \
  --permission-mode auto --permission-prompts none
```

이 플래그를 쓰면 `AskUserQuestion`처럼 사람의 답이 필요한 도구는 Claude의 도구
목록에서 빠지고, `Elicitation` hook이 답하지 않는 MCP
요청(elicitation)은 취소된다.
`--output-format stream-json`에서는 거부가 `permission_denied` 시스템 메시지로
나오고, 최종 결과 메시지의 `permission_denials`에 목록이 담긴다.
이 플래그는 Claude Code v2.1.259 이상이 필요하고,
이전 버전은 알 수 없는 옵션 오류를 낸다.

## `--bare`: 재현 가능한 실행

`--bare`는 hooks, skills, 사용자 정의 명령, subagents, 설치된 플러그인,
MCP 서버, 자동 메모리, CLAUDE.md의 자동 탐색을 건너뛰어 스크립트 호출을 더
빠르게 시작한다.
`--bare`가 없으면 `claude -p`는 작업 디렉터리와 `~/.claude`에 설정된 것을
상호작용 세션처럼 모두 로드한다.
머신마다 같은 결과가 나와야 하는 CI와 스크립트에 쓰라는 것이 공식 권고이며,
앞으로 `-p`의 기본값이 될 예정이다.
동료의 `~/.claude`에 있는 hook이나 프로젝트 `.mcp.json`의 MCP 서버는 bare 모드가
읽지 않으므로 돌지 않는다.
`--add-dir`로 지정한 디렉터리는 부분 예외라서,
그 `.claude/skills/`의 skills는 로드하지만 `.claude/commands/`와
`.claude/agents/`는 건너뛴다.

```bash
claude -p "이 파일을 요약해줘" --bare --allowedTools "Read"
```

### 인증

bare 모드는 OAuth 자격 증명과 시스템 키체인을 읽지 않는다.
Anthropic API에는 환경 변수 `ANTHROPIC_API_KEY`를 두거나 `--settings` JSON에
`apiKeyHelper`를 준다.
Amazon Bedrock, Google Cloud, Microsoft Foundry는 평소처럼 자기 자격
증명을 읽는다.

### 필요한 맥락은 플래그로 직접

bare 모드의 Claude가 쓸 수 있는 도구는 Bash와 파일 읽기, 파일 수정이다.
다른 맥락은 플래그로 준다.

| 로드할 것            | 플래그                                                  |
| -------------------- | ------------------------------------------------------- |
| 시스템 프롬프트 추가 | `--append-system-prompt`, `--append-system-prompt-file` |
| 설정                 | `--settings <파일 또는 JSON>`                           |
| MCP 서버             | `--mcp-config <파일 또는 JSON>`                         |
| 사용자 정의 에이전트 | `--agents <파일 또는 JSON>`                             |
| 플러그인             | `--plugin-dir <경로>`, `--plugin-url <URL>`             |

### 실행 중의 제한

bare 모드는 세션이 도는 동안의 동작도 제한한다.
명령줄로 준 MCP 서버만 연결된다.
Claude는 프롬프트와 도구 결과를 받되 Claude Code가 곁들일 시스템 리마인더(system
reminder)는 받지 않는다.
그래서 앞서 읽은 파일이 디스크에서 바뀌어도 알려 주지 않고,
사용 가능한 skills 목록도 받지 못한다.
백그라운드 명령과 백그라운드 subagent는 쓸 수 없고,
타임아웃에 닿은 명령은 백그라운드로 옮겨지지 않고 멈춘다.
v2.1.286 이전에는 이 제한이 일부만 적용됐다.

### 신뢰하지 않은 폴더에서의 `-p`

`--bare`가 없는 `-p` 실행은 한 번도 신뢰하지 않은 폴더에서도 프로젝트
`.claude/settings.json`의 hooks를 돌리고 `.mcp.json`의 서버를 연결한다.
`-p` 세션은 작업 공간 신뢰 대화상자도 서버별 승인 질문도 보여 주지 않는다.
외부에서 받은 저장소를 대상으로 하는 자동화라면 `--bare`가 속도 선택이면서
동시에 보안 선택이다.

## 시스템 프롬프트

`--append-system-prompt`는 Claude Code의 기본 동작을 유지하면서 지시를 더한다.
공식 예제는 PR diff를 넘겨 보안 취약점을 검토시키는 스크립트(`review.sh`)다.

```bash
#!/bin/bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

`bash review.sh 123`으로 실행하면 셸이 `"$1"`을 `123`으로 바꿔 PR 123의 diff를
가져오고, 검토 결과는 JSON의 `result` 필드에 담겨 나온다.
다른 시스템 프롬프트 플래그는 아래와 같다.

| 플래그                        | 동작                                        |
| ----------------------------- | ------------------------------------------- |
| `--system-prompt`             | 기본 시스템 프롬프트 전체를 교체[^cli]      |
| `--system-prompt-file`        | 파일 내용으로 교체[^cli]                    |
| `--append-system-prompt`      | 기본 프롬프트 뒤에 덧붙임[^cli]             |
| `--append-system-prompt-file` | 파일 내용을 기본 프롬프트 뒤에 덧붙임[^cli] |

기본 프롬프트를 교체하면 그 실행은 git 상태 스냅샷(git status snapshot) 없이
시작한다는 점도 공식 문서가 밝힌다.

## 세션 이어가기

`--continue`는 가장 최근 대화를 이어가고,
`--resume`은 세션 ID로 특정 대화를 이어간다.
v2.1.257 이상에서 `--continue`는 끝난 백그라운드 세션은 열지만 아직 돌고 있는
것은 열지 않는다.
`--continue`만 쓰면 `claude -p`나 Agent SDK로 만든 세션은 건너뛰고,
`claude -p --continue`로 쓸 때만 그런 세션이 포함된다.[^cli]

```bash
claude -p "이 코드베이스의 성능 문제를 검토해줘"
claude -p "이번엔 데이터베이스 쿼리에 집중해줘" --continue
claude -p "발견한 문제를 요약해줘" --continue
```

여러 대화를 동시에 돌리면 세션 ID를 잡아 두었다가 특정 대화를 이어간다.

```bash
session_id=$(claude -p "리뷰를 시작해줘" --output-format json | jq -r '.session_id')
claude -p "그 리뷰를 이어가줘" --resume "$session_id"
```

두 명령은 다른 디렉터리에서 실행해도 된다.
Claude Code는 이 머신의 어느 프로젝트에서든 ID로 세션을 찾는다.
세션 ID 대신 세션의 `.jsonl` 기록(transcript) 파일의 절대 경로를 `--resume`에 줄
수도 있고, 그러면 그 파일에 든 대화를 이어간다.
`--resume`이나 `--continue`와 `--fork-session`을 함께 쓰면 원래 세션 ID를
재사용하지 않고 새 ID로 갈라진다.[^cli]
세션을 디스크에 남기지 않으려면 `--no-session-persistence`를 쓰며,
이 플래그는 print mode 전용이다.[^cli]

## 실행 제어

### 턴 수와 예산

`--max-turns`는 에이전트 턴 수를 제한하며, 한계에 닿으면 오류로 끝난다.
기본값은 제한 없음이다.
`--input-format stream-json`과 함께 쓰면 턴이 끝나는 시점에 아직 대기 중인
메시지는 대기열에 남아 새 턴을 시작한다.[^cli]
`--max-budget-usd`는 API 호출의 추정 지출이 이 값에 닿으면 실행을 멈추며 print
mode 전용이다.
이 상한은 클라이언트가 계산한 추정치를 기준으로 하므로 청구와 일치하지 않을
수 있다.[^cli]
예산 상한에 닿으면 Claude Code는 남은 백그라운드 작업을 기다리지 않고 멈춘다.

### 끝난 뒤의 백그라운드 작업

Claude의 턴이 끝나고 stdin이 닫힌 뒤에도 `claude -p`는 Claude가 시작한
백그라운드 작업을 기다리느라 열려 있을 수 있다.
메인 대화가 시작한 백그라운드 명령이 아직 돌고 있지 않으면,
Claude Code는 연속 10분 유휴 대기 후 남은 작업을 멈추고 그 부분 결과를 버린다.
상한은 `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`로 바꾸며,
`0`이면 상한 없이 기다린다.

| 작업                          | 기다리는 방식                                                                                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 백그라운드 명령               | 개발 서버나 watch 빌드 같은 명령은 종료하거나 시간 제한에 닿을 때까지 기다린 뒤 Claude가 결과로 한 턴 더 진행. 이 동안은 10분 상한이 대기를 끝내지 않음 |
| 백그라운드 subagent, workflow | 결과가 최종 출력의 일부이므로 끝날 때까지 열려 있음                                                                                                     |
| Monitor 감시                  | 감시가 타임아웃(기본: 시작 5분 뒤)하거나 10분 상한이 끝낼 때까지                                                                                        |
| 예약된 `/loop` 깨우기         | 프롬프트를 텍스트로 넘긴 실행에서는 루프가 끝날 때까지 각 깨우기를 기다리고, 10분 상한을 넘어도 기다림                                                  |

stderr가 터미널이고 5초 넘게 기다리면 `Waiting for background work to finish`로
시작하는 줄이 stderr에 나온다.
`json`이나 `stream-json` 출력에서는 stdout이 터미널이 아닐 때만 이 줄이 나오므로
스크립트가 읽는 JSON에는 섞이지 않는다.
백그라운드 작업이 새 턴을 시작시키면 기본 `text` 출력은 매 턴의 결과를,
`json` 출력은 마지막 턴의 결과를 출력한다.
v2.1.295 이전에는 `text`도 마지막 턴의 결과만 출력했다.
MCP 작업은 기다리지 않는다.
원격 서버의 MCP 작업은 계속되지만 다시 따라가려면 일회성 `claude -p "<prompt>"`
실행이 아니라 그 세션을 이어가야 하고, 자동 백그라운드 전환으로 옮겨진 MCP
호출의 결과는 사라진다.

### SIGTERM과 SIGINT

`kill`이나 프로세스 감독자로 SIGTERM을 보내 멈추면 Claude Code는 종료 코드
143으로 끝난다.
진행 중이던 턴은 끝나지 않은 채 남고 그 턴의 결과는 기록되지 않는다.
턴을 끝내고 멈추려면 프로세스를 멈추기 전에 SIGINT를 보내거나 Agent SDK의
`interrupt()`를 부른다.
SIGTERM을 받으면 아직 도는 Bash 명령의 프로세스 트리를 종료하고,
`SessionEnd` hooks를 실행한 뒤 끝난다.
종료 중에는 새 도구 호출도, 새 모델 요청도,
`SessionEnd` 외의 hook도 시작하지 않는다.
명령 실행 중이었다면 세션에 그 명령이 종료된 것으로 기록한다.
권한 질문에 답을 기다리던 중이었다면, 프로세스에 SIGTERM을 보낸 경우 질문을 답
없이 남기고, Agent SDK로 세션을 닫은 경우에는 SDK가 신호를 보내기 전에 입력을
끝내므로 입력이 끝나는 즉시 질문이 취소된다.
세션을 다시 이어가면 중단된 턴은 그대로 두고 다음 프롬프트가 대화를 이끈다.
중단된 턴을 이어서 진행하게 하려면
`CLAUDE_CODE_RESUME_INTERRUPTED_TURN=1`을 설정한다.

### 작업 디렉터리가 지워졌을 때

세션 도중 `claude -p`나 Agent SDK 세션의 작업 디렉터리가 지워져도
세션은 계속 돈다.
디렉터리가 없는 동안 턴이 시작되면 `stream-json` 출력에 경고 메시지가 나오고,
디렉터리가 다시 생길 때까지 셸 명령은 실패한다.

## CI 통합

`claude -p`를 매번 직접 감싸는 대신 GitHub Actions의 Claude Code 액션을
쓸 수도 있다.
공식 문서는 이 액션이 Agent SDK 위에 만들어졌다고 설명한다.[^actions]
GitLab 파이프라인용 통합은 별도 문서가 있다.

### 두 가지 동작 방식

워크플로 구성에 따라 액션이 방식을 정한다.[^actions]

| 방식          | 조건                            | 동작                                                                                         |
| ------------- | ------------------------------- | -------------------------------------------------------------------------------------------- |
| 상호작용 모드 | 워크플로에 `prompt` 입력이 없음 | `@claude` 같은 트리거 문구를 기다렸다가 응답하고, 진행과 결과가 해당 이슈나 PR의 댓글로 나옴 |
| 자동화 모드   | 워크플로에 `prompt` 입력이 있음 | 멘션을 기다리지 않고 실행하며, 결과는 기본적으로 워크플로 실행 로그에 나옴                   |

두 모드 모두 Claude가 시작하기 전에 행위자를 두 가지로 검사하고,
거부되면 실행이 실패한다.[^actions]
이슈와 PR 이벤트에서는 쓰기 권한이 있어야 하고,
모든 이벤트에서 봇 행위자는 `allowed_bots`에 올리지 않으면 거부된다.[^actions]

### CLI 인자 전달

`claude_args` 입력은 Claude Code CLI 인자를 그대로 받는다.[^actions]
예를 들면 `--max-turns 5 --model <모델> --mcp-config /path/to/config.json`
같은 값이다.
즉 이 문서의 플래그가 액션 안에서도 같은 뜻으로 쓰인다.
이 대응은 문서의 설명이며 모든 플래그를 액션에서 시험한 것은 아니다.

### 비용과 자격 증명

실행마다 GitHub Actions 분과 API 토큰을 쓴다.[^actions]
비용을 줄이는 방법으로 공식 문서는 요청을 구체적으로 쓰기,
`CLAUDE.md`를 짧게 두기, `claude_args`에 `--max-turns` 두기,
워크플로 수준 타임아웃, GitHub 동시 실행 제어를 든다.[^actions]
API 키와 OAuth 토큰은 저장소에 커밋하지 말고 GitHub Secrets에 두며,
문서의 예는 `${{ secrets.ANTHROPIC_API_KEY }}`다.[^actions]

## 비용과 요금제

`claude -p`가 구독 한도를 쓰는지 API 요금을 쓰는지는 로그인 방식에 달려 있다.
Anthropic 지원 문서는 두 경우를 이렇게 나눈다.[^support-sdk][^support-credits]

| 실행 방식                                          | 쓰는 한도                                                                  |
| -------------------------------------------------- | -------------------------------------------------------------------------- |
| Claude 요금제로 로그인한 `claude -p`와 Agent SDK   | 구독 한도[^support-sdk]                                                    |
| 연결한 Console 조직의 API 키로 실행한 `claude -p`  | 월별 API 크레딧, 다 쓰면 구매한 크레딧[^support-credits]                   |
| GitHub Action, IDE 확장, 데스크톱 앱이 시작한 실행 | Claude Code 사용으로 집계되어 API 크레딧이 적용되지 않음[^support-credits] |

### 2026년에 있었던 두 번의 변화

2026년 6월 15일 갱신에서, 앞서 발표했던 Agent SDK 사용량 변경은 보류되어 달라진
것이 없다고 지원 문서는 적는다.[^support-sdk]
같은 문서의 10월 7일 갱신은 Max와 Team 요금제에 월별 API 크레딧이 생겼다고
알린다.[^support-sdk]
이 크레딧은 Claude API, Claude Managed Agents,
그리고 연결한 Console 조직의 API 키로 쓰는 Agent SDK와 `claude -p`에
적용된다.[^support-sdk]
요금제로 로그인한 상태에서는 SDK와 `claude -p`가 여전히 구독 한도를
쓴다.[^support-sdk]

### 월별 API 크레딧

| 요금제             | 월 크레딧                                      |
| ------------------ | ---------------------------------------------- |
| Max 5x             | $100[^support-credits]                         |
| Max 20x            | $200[^support-credits]                         |
| Team 표준 좌석     | 좌석당 $20, 합산해 $500까지[^support-credits]  |
| Team 프리미엄 좌석 | 좌석당 $100, 합산해 $500까지[^support-credits] |

Free, Pro, Enterprise는 대상이 아니고, 대상 요금제에 7일 이상 있어야
한다.[^support-credits]
Max는 설정의 결제 화면에서, Team은 조직 설정의 결제 화면에서 Console 조직을
연결해 받는다.[^support-credits]
연결할 수 있는 Console 조직은 요금제당 하나이며 직접 바꿀 수
없다.[^support-credits]
크레딧은 이월되지 않고 결제 주기 끝에 사라지며,
연결한 조직의 API 키를 가진 모두가 같은 잔액을 나눠 쓴다.[^support-credits]
다 쓴 뒤에는 구매한 크레딧이나 자동 충전이 있으면 그것으로 이어지고,
없으면 다음 크레딧이 들어올 때까지 API 요청이 멈추며 요금제로 청구되지는
않는다.[^support-credits]
이 크레딧은 터미널, IDE, 데스크톱, 웹의 상호작용 Claude Code와 Amazon Bedrock,
Google Cloud, Microsoft Foundry의 Claude에는 적용되지 않는다.[^support-credits]

### 개발자 반응

발표 당시 Hacker News에서는 문구가 헷갈린다는 반응이 먼저 나왔다.
`ramoz`는 보도 문구가 혼란스러워서 `claude -p`를 쓰던 사람이 API 요금을 내게
되는지 확신하지 못하겠다고 적었다.[^hn-ramoz]
`puglr`는 Max 요금제 사용량의 99%가 비상호작용이고,
같은 사용량을 API로 환산하면 하루에 세 자릿수 달러가 든다고 했다.[^hn-puglr]
`sigseg1v`는 모든 작업을 `claude -p`로 도는 Ralph 루프에 넣고 주간 한도를
100%까지 쓰는 사용자를 수익이 안 나는 예외로 볼 수 있느냐고
되물었다.[^hn-sigseg1v]
구독과 API 크레딧이 다르다는 점을 짚은 댓글도 있다.
`gcr`는 구독 사용량은 5시간마다 다시 채워지지만 월 크레딧은 다 쓰면 다음 달까지
끝이라고 했다.[^hn-gcr]
이 스레드의 댓글은 보류되기 전에 발표된 안을 두고 나온 것이다.
지금의 공식 상태는 위 지원 문서가 기준이며,
정책은 바뀐 전례가 있으므로 도입 전에 해당 문서를 다시 확인해야 한다.

### 비용을 줄이는 선택

단순 분류나 요약에는 작은 모델을 `--model`로 지정하라는 조언이 실전 글에
나온다.[^shelf]
공식 문서는 `--max-turns`와 `--max-budget-usd`로 상한을 걸라고 안내한다.
비용 수치는 추정치라서 예산 상한용으로만 쓴다.[^cost]

## 실전 스크립트

아래 스크립트는 실전 글의 구성[^devtk]과 이 문서의 공식 플래그를 맞춰
다시 쓴 것이다.
이 문서를 쓰면서 모든 스크립트를 실행해 보지는 않았고,
인증 없이 실행했을 때의 결과만 직접 확인했다(아래 비평 절).

### 감싸개 스크립트: 재시도와 성공 판정

스크립트마다 같은 검사를 반복하지 않도록 `claude -p`를 한 번 감싼다.
핵심은 종료 코드가 아니라 결과 객체로 판정하는 것이다.

```bash
#!/usr/bin/env bash
# claude-job.sh "<프롬프트>" [추가 claude 옵션...]
set -euo pipefail
prompt=$1; shift

for attempt in 1 2 3; do
  # 실패해도 JSON이 stdout에 나오므로 종료 코드는 일단 무시한다
  out=$(claude -p "$prompt" --bare --output-format json \
          --permission-mode dontAsk --max-turns 25 --max-budget-usd 3.00 \
          "$@" </dev/null) || true
  jq -e '.type == "result"' >/dev/null 2>&1 <<<"$out" && break
  sleep $((attempt * 30))
done

jq -e '.type == "result"' >/dev/null 2>&1 <<<"$out" \
  || { echo "결과 객체가 없습니다" >&2; exit 1; }

# subtype만 보면 안 된다: success이면서 is_error가 true인 실행이 있다
jq -e '.subtype == "success" and .is_error == false' >/dev/null <<<"$out" \
  || { jq -r '.result' <<<"$out" >&2; exit 1; }

# 거부된 도구 호출이 있으면 실패로 본다
if [ "${ALLOW_DENIALS:-0}" != 1 ] \
   && jq -e '.permission_denials | length > 0' >/dev/null <<<"$out"; then
  jq '.permission_denials' <<<"$out" >&2; exit 1
fi

printf '%s\n' "$out"
```

실전 글은 이 판정에서 jq의 `//` 연산자를 조심하라고 짚는다.[^devtk]
`.is_error // true`는 `false`를 값이 없는 것으로 취급해서 성공한 실행에도
`true`를 돌려준다.
위 스크립트가 `.is_error == false`로 비교하는 이유다.
`set -e` 아래에서 재시도 논리를 쓰려면 실패할 수 있는 명령을 `&&`, `||`,
`if` 안에 두어야 한다.[^devtk]
`</dev/null`은 cron처럼 stdin이 없는 환경에서 입력 대기를 아예
없애려는 선택이다.

### 커밋 전 검사: 비밀 값 먼저, 모델은 나중, 실패하면 통과

`.git/hooks/pre-commit`에 두고 `chmod +x`를 한다.
git은 실행 권한이 없는 hook을 건너뛴다.[^devtk]
모델을 부르기 전에 결정적인 검사(`gitleaks`)를 먼저 하고,
모델 검사가 끝나지 못하면 커밋을 막지 않는다.
모델 검사를 커밋의 필수 관문으로 만들면 API 장애나 한도 소진이 곧 개발 중단이
되기 때문이다.

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit
set -uo pipefail

gitleaks git --staged || { echo "비밀 값 의심: 커밋을 중단합니다" >&2; exit 1; }

schema='{"type":"object","properties":{"verdict":{"enum":["pass","block"]},"reason":{"type":"string"}},"required":["verdict","reason"]}'

out=$(git diff --cached --no-color | claude -p \
  "이 diff에 치명적인 버그가 있으면 block, 아니면 pass로 판정하고 이유를 한 줄로 적어줘" \
  --bare --output-format json --json-schema "$schema" \
  --tools "" --permission-mode dontAsk --max-turns 3 --max-budget-usd 0.50) \
  || { echo "모델 검사를 끝내지 못해 통과시킵니다. push 전에 다시 실행하세요" >&2; exit 0; }

if [ "$(jq -r '.structured_output.verdict // empty' <<<"$out")" = block ]; then
  jq -r '.structured_output.reason' <<<"$out" >&2
  exit 1
fi
```

우회는 `git commit --no-verify`다.
`structured_output`이 없는 응답은 위 조건에서 `block`이 아니므로 통과한다.
이것이 의도한 동작인지는 팀이 정해야 한다.

### 파일별 일괄 작업: 하나씩 하고 검증하고 되돌리기

여러 파일을 한 세션에 몰아서 고치게 하면 한 파일의 실패가 다른 파일의 결과에까지 영향을 준다.
파일마다 `claude -p`를 한 번씩 돌리고, 편집 권한을 그 파일 하나로 좁히고,
테스트를 통과해야 남기는 방식이 더 안전하다.[^devtk]

```bash
for f in $(git grep -l "from 'moment'" -- ':(glob)src/**/*.ts'); do
  ./claude-job.sh "$f에서 moment를 date-fns로 바꿔줘. 이 파일만 고쳐." \
      --allowedTools "Edit(./$f)" >/dev/null || { echo "$f" >> failures.txt; git checkout -- .; continue; }

  # 다른 파일을 건드렸으면 실패로 본다
  [ "$(git diff --name-only)" = "$f" ] \
    || { echo "$f (범위 이탈)" >> failures.txt; git checkout -- .; continue; }

  npx vitest related "$f" --run \
    || { echo "$f (테스트 실패)" >> failures.txt; git checkout -- .; continue; }
done
```

이 반복은 `git checkout -- .`로 되돌리므로 작업 트리가 깨끗한 상태에서만
돌려야 한다.
한 파일당 커밋이 필요하면 통과 뒤에 `git add -- "$f"`와 커밋을 더한다.
병렬로 돌리는 스크립트는 참고한 글에도 없다.
그 글은 대신 번들된 `/batch` skill이 작업을 5~30개 단위로 나눠 각각 별도
워크트리에서 돌린다고 소개한다.[^devtk]
파일마다 커밋을 하나씩 남기고 실패 목록을 받고 싶으면 위 셸 반복이 낫다고
한다.[^devtk]

### 주기 실행(cron): 환경이 비어 있다는 전제

cron 작업은 PATH도 환경 변수도 거의 없는 상태로 시작한다.
스크립트 안에서 PATH를 지정하고 키를 읽어 오는 파일을 `source`한다.
`--bare`를 쓰면 OAuth를 읽지 않으므로 키는 `ANTHROPIC_API_KEY`여야 하고,
OAuth 토큰을 쓰려면 `--bare`를 포기해야 한다.
cron과 같은 빈 환경을 재현하려면 `env -i HOME=“$HOME” /bin/bash
/opt/jobs/dep-audit.sh`로 먼저 돌려 본다.[^devtk]

```bash
# crontab: 정각에 몰리지 않도록 7분에 실행
7 6 * * 1  /opt/jobs/dep-audit.sh >> /var/log/dep-audit.log 2>&1
```

```bash
#!/usr/bin/env bash
# /opt/jobs/dep-audit.sh
set -euo pipefail
export PATH=/usr/local/bin:/usr/bin:/bin
source /opt/jobs/claude.env   # ANTHROPIC_API_KEY를 export하는 파일
cd /srv/repo
git fetch -q origin && git checkout -q -B chore/dep-audit origin/main

/opt/jobs/claude-job.sh "npm audit 결과를 reports/dep-audit.md에 정리해줘" \
  --allowedTools "Bash(npm audit *)" "Bash(npm outdated *)" "Edit(./reports/**)"
```

### PR 리뷰 게시

`gh pr diff`의 결과를 읽기 전용으로 검토시키고 `gh pr comment`로 게시하는 흐름이
실전 글에 나온다.[^shelf]
검토 단계에는 `--allowedTools "Read"`만 주면 되고,
게시는 모델이 아니라 스크립트가 한다.
게시를 모델에 맡기면 GitHub 쓰기 권한을 모델에게 줘야 하지만,
스크립트가 게시하면 모델은 읽기만 한다.

## 현장에서 보고된 문제

아래는 공식 문서가 아니라 사용자들이 GitHub에 올린 보고다.
세 건 모두 유지보수자가 원인을 확정하지 못한 채 닫혔으므로,
재현되는 사실이 아니라 점검할 후보로 읽어야 한다.

### 입력이 끝나지 않으면 조용히 멈춘다

`claude -p`는 프롬프트를 stdin에서 EOF까지 읽는다.
Claude Code 유지보수자 `bcherny`는 EOF를 전달하지 않는 파이프가 있으면 조용히
멈출 수 있다고 설명했다.[^gh-73373]
한 사용자는 `echo "next turn" | claude -p -r <session_id>`가 WSL2의 2.1.198에서
90초 넘게 출력 없이 멈추고, 같은 입력을 위치 인자로 주면 40턴 연쇄 실행이 된다고
보고했다.[^gh-73373]
유지보수자는 Linux에서 재현하지 못했고 WSL과 Windows 사이의 파이프 경계를
의심했으며, 작성자의 추가 정보가 없어 이슈는 계획 없음으로 닫혔다.[^gh-73373]
자동화에서는 프롬프트를 위치 인자나 `< file` 리디렉션으로 주고,
파이프가 필요하면 먼저 파일로 받는 쪽이 안전하다.

### 3초 동안 입력이 없으면 입력 없이 진행한다

다른 사용자는 `vipe`로 편집기를 열어 쓴 내용을 `claude -p`에 넘기는 흐름이
깨진다고 보고했다.[^gh-60998]
보고에 따르면 stdin에 3초 동안 바이트가 없으면 Claude Code가 `Warning: no stdin
data received in 3s, proceeding without it...`를 내고,
프롬프트 인자도 없으면 `Input must be provided either through stdin or as a
prompt argument when using --print` 오류로 끝난다.[^gh-60998]
원인은 파이프라인의 각 단계가 동시에 시작되어,
편집기가 열려 있는 동안 상류가 쓰기 끝을 열어 둔 채 아무것도 보내지 않기
때문이라고 작성자는 추정했다.[^gh-60998]
작성자가 든 우회는 명령 치환(`claude -p "$(vipe < /dev/null)"`)과 임시
파일이다.[^gh-60998]
이 이슈도 계획 없음으로 닫혔다.
사람이 입력을 늦게 주는 파이프라인에는 `-p`를 직접 연결하지 말고 입력을 먼저
확정한 뒤 넘겨야 한다.

### 터미널 없는 부모 프로세스에서 병렬 subagent가 멈춘다

macOS에서 cron이나 launchd처럼 제어 터미널이 없는 부모가 `claude -p`를 실행했을
때, 한 메시지에 `Task` 호출 5개를 병렬로 내는 작업이 10분 넘게 출력 없이
멈췄다고 한 사용자가 보고했다.[^gh-56540]
`Task` 하나만 내는 작업은 끝났고, 작성자의 우회는 subagent를 하나씩 순서대로
부르는 것으로 약 2분이 더 걸렸다.[^gh-56540]
원인은 확인되지 않았고 이슈는 활동 없음으로 닫혔다.[^gh-56540]
주기 작업에서 병렬 subagent를 쓴다면 프로세스 감독자의 시간 제한을 걸고,
멈췄을 때 SIGINT를 먼저 보내는 경로를 두어야 한다.

### 이 보고들에서 얻는 점검표

| 증상                                | 먼저 볼 것                                          |
| ----------------------------------- | --------------------------------------------------- |
| 출력 없이 멈춤                      | 프롬프트를 위치 인자로 바꿔 보기, `</dev/null`      |
| `no stdin data received in 3s` 경고 | 입력을 파일로 먼저 확정한 뒤 `< file`               |
| 터미널 없는 환경에서만 멈춤         | 병렬 subagent를 순차로 바꿔 보기                    |
| 큰 입력에서 결과 없음               | 10MB 상한 안인지 확인, 파일에 쓰고 경로로 가리킴    |
| 종료 코드 0인데 내용이 이상함       | `is_error`, `terminal_reason`, `permission_denials` |

## 커뮤니티가 쓰는 방식

`claude -p`를 두고 Hacker News에서는 쓰임새가 두 갈래로 갈린다.
하나는 CI와 어디서나 쓰는 유틸리티로 보는 시각이다.
Claude Code 팀과의 인터뷰를 정리한 댓글에서 `swyx`는 헤드리스 Claude Code를 CI
어디에나 쓰는 리눅스 도구처럼 쓰는 방식이 설득력 있다고 요약했다.[^hn-swyx]
다른 하나는 정교한 오케스트레이션도 `-p`만으로 된다는 시각이다.
한 스레드에서 `hombre_fatal`은 `--resume <sessionId>`와 `--fork-session`으로
고정한 대화를 기반 맥락으로 삼아 여러 프롬프트에 재사용할 수 있다고
했다.[^hn-hombre]
이 방식은 이 문서의 세션 절이 설명하는 플래그의 조합이다.

## 레시피

| 하고 싶은 일                 | 명령                                                                                     |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| 질문 하나 던지기             | `claude -p "질문"`                                                                       |
| 로그를 설명시켜 파일에 저장  | `claude -p "설명해줘" < log.txt > out.txt`                                               |
| 결과를 JSON으로 받기         | `claude -p "…" --output-format json`, 결과는 `.result` 필드                              |
| 스키마에 맞는 값 받기        | `claude -p "…" --output-format json --json-schema '{…}'`, 값은 `.structured_output` 필드 |
| 토큰 단위로 스트리밍         | `claude -p "…" --output-format stream-json --verbose --include-partial-messages`         |
| CI에서 재현 가능하게 실행    | `claude -p "…" --bare --allowedTools "Read"`                                             |
| 무인 실행에서 승인 질문 끄기 | `claude -p "…" --permission-mode auto --permission-prompts none`                         |
| 비용과 턴 제한               | `claude -p "…" --max-turns 5 --max-budget-usd 2`                                         |
| 직전 대화 이어가기           | `claude -p "…" --continue`                                                               |
| 특정 세션 이어가기           | `claude -p "…" --resume "$session_id"`                                                   |
| 세션을 디스크에 남기지 않기  | `claude -p "…" --no-session-persistence`                                                 |

## 비평

### 종료 코드만으로는 성공을 알 수 없다

공식 문서는 실행 도중의 실패가 오류가 아니라 결과로 stdout에 찍힌다고 적는다.
이 문서를 쓰면서 이를 직접 확인했다.
Claude Code 2.1.308에서 인증 정보 없이 `claude -p “hi” --bare --output-format
json`을 실행하자 종료 코드는 1이었고, stdout에는 결과 객체가 나왔다.
그 객체의 `subtype`은 `success`, `is_error`는 `true`,
`result`는 `Not logged in · Please run /login`,
`terminal_reason`은 `api_error`였다.
Python SDK 레퍼런스도 `subtype="success"`이면서 `is_error=True`인 경우를 따로
설명한다.[^python]
그러므로 `subtype`만 보고 성공으로 판정하는 스크립트는 로그인 실패를
성공으로 처리한다.
판정은 `subtype == "success"`와 `is_error == false`를 함께 요구해야 한다.
이 확인은 한 버전, 한 실패 유형에 한정된다.
다른 실패(한도 소진, 네트워크 오류)에서 종료 코드와 필드가 어떻게 나오는지는
확인하지 않았다.

### 조용히 사라지는 실패가 많다

잘못된 `--mcp-config` 항목은 건너뛰고 정상 종료하고,
stderr를 캡처하는 환경에서는 경고도 나오지 않는다.
스키마를 못 채운 실행에는 `structured_output` 필드가 아예 없고,
자동 백그라운드 전환으로 옮겨진 MCP 호출은 결과가 사라진다.
공통점은 세 경우 모두 실행이 성공으로 끝난 것처럼 보인다는 것이다.
각각에 대응하는 확인 지점이 문서에 있다.
`mcp_server_errors`가 비었는지, `structured_output`이 있는지,
`permission_denials`가 비었는지다.

### `--bare`는 안전하지만 가볍지는 않다

`--bare`를 권하는 이유는 재현성과 보안이다.
그러나 쓰는 쪽에서 치르는 값도 있다.
시스템 리마인더가 없어서 Claude는 읽은 뒤 바뀐 파일을 모르고,
skills 목록도 받지 못하며, 백그라운드 작업도 못 쓴다.
무엇을 로드할지 플래그로 전부 지정해야 하는 부담도 있다.
앞으로 `-p`의 기본값이 된다고 하므로, 지금 `--bare` 없이 `.mcp.json`이나
프로젝트 hooks에 의존하는 스크립트는 기본값이 바뀌는 시점에 동작이
달라질 수 있다.
이 위험은 기본값 변경이 실제로 일어날 때 확인된다.

## 체크리스트

1. 스크립트에 `--bare`를 붙였고 `ANTHROPIC_API_KEY`(또는 클라우드 자격 증명)를 환경에 두었는가.
2. `--allowedTools`나 `--permission-mode`로 승인 정책을 정했고, 사람이 없으면 `--permission-prompts none`을 더했는가.
3. 성공 판정에 `subtype == "success"`와 `is_error == false`를 함께 쓰는가(`jq`의 `//`로 `false`를 기본값 처리하지 않았는가).
4. `--json-schema`를 쓴다면 `structured_output` 필드가 있는지 먼저 검사하는가.
5. `--mcp-config`나 플러그인을 쓴다면 `system/init`의 `mcp_server_errors`와 `plugin_errors`를 CI 실패 조건에 넣었는가.
6. `--max-turns`와 `--max-budget-usd`를 걸었고, 비용 값을 청구 근거로 쓰지 않는가.
7. 파이프 입력이 10MB를 넘지 않는가. 넘는다면 파일로 쓰고 경로를 가리키는가.
8. 세션을 이어갈 스크립트는 `session_id`를 저장해 두고 `--resume`을 쓰는가.
9. 프로세스를 멈출 때 SIGTERM 대신 SIGINT를 먼저 보내는 경로가 있는가.
10. 외부에서 받은 저장소를 여는 자동화에 `--bare`를 적용했는가.
11. 자동화가 어떤 한도(구독, API 크레딧)를 쓰는지 로그인 방식으로 확인했는가.
12. stdin 파이프를 쓰는 자동화에서 EOF가 오지 않을 가능성을 처리했는가(위치 인자, `< file`, `</dev/null`).
13. 모델 검사를 커밋이나 배포의 필수 관문으로 만들었다면 모델이 실패했을 때의 동작(통과 또는 중단)을 정했는가.

## 기억할 원칙

`claude -p`의 결과는 사람이 읽는 화면이 아니라 프로그램이 읽는 입력이다.
그래서 출력 형식을 `json`이나 `stream-json`으로 고정하고, 성공의 증거(종료 코드,
`result`, `structured_output`, `*_errors`,
`permission_denials`)를 하나씩 검사하며,
환경에서 오는 설정은 `--bare`로 끊고 필요한 것만 플래그로 명시한다.

---

[^cli]: Anthropic, [CLI reference](https://code.claude.com/docs/en/cli-reference)

[^cost]: Anthropic, [Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

[^actions]: Anthropic, [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)

[^python]: Anthropic, [Agent SDK reference - Python](https://code.claude.com/docs/en/agent-sdk/python)

[^support-sdk]: Anthropic, [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

[^support-credits]: Anthropic, [Monthly API credits for Max and Team plans](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)

[^devtk]: Developer Toolkit, [Script Automation](https://developertoolkit.ai/en/claude-code/automate/script-automation/), 2025-07-24

[^shelf]: The Prompt Shelf, [Claude Code Print Mode and stream-json: Automate Everything with -p](https://thepromptshelf.dev/blog/claude-code-print-mode-stream-json-automation-2026/), 2026-06-24

[^gh-73373]: GitHub, [Headless: `claude -p -r <session_id>` combined with stdin input hangs indefinitely; argv positional works](https://github.com/anthropics/claude-code/issues/73373), 2026-07-02

[^gh-60998]: GitHub, [\[FEATURE\] `claude -p` 3-second stdin timeout breaks `vipe`-style edit-in-pipeline workflows](https://github.com/anthropics/claude-code/issues/60998), 2026-05-20

[^gh-56540]: GitHub, [claude -p headless under non-TTY parent: parallel Task fan-out hangs + subagent path-scope ignores prompt scoping](https://github.com/anthropics/claude-code/issues/56540), 2026-05-06

[^hn-ramoz]: <https://news.ycombinator.com/item?id=48126282>

[^hn-puglr]: <https://news.ycombinator.com/item?id=48127790>

[^hn-sigseg1v]: <https://news.ycombinator.com/item?id=48128464>

[^hn-gcr]: <https://news.ycombinator.com/item?id=48128946>

[^hn-swyx]: <https://news.ycombinator.com/item?id=44033069>

[^hn-hombre]: <https://news.ycombinator.com/item?id=47438501>
