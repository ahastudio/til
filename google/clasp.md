# clasp: Apps Script 프로젝트를 로컬에서 개발하는 CLI

<https://github.com/google/clasp>

HN 토론: <https://news.ycombinator.com/item?id=19926835> (2점, 1개 댓글)

## 소개

clasp는 Google Apps Script 프로젝트를 로컬에서 개발하게 해 주는 CLI다.
이름은 Command Line Apps Script Projects의 약자다.

README 첫 줄에 중요한 단서가 있다. 공식적으로 지원되는 Google 제품이 아니라는 것이다.
저장소는 `google/clasp`이고 Apache-2.0이며 별 5,800개, 포크 510개다.
npm 패키지는 `@google/clasp`이고 기본 브랜치는 `master`다.

계약이 무엇인지가 명확하다.
Apps Script는 원래 `script.google.com`의 웹 편집기에서만 편집할 수 있고, 프로젝트는 평평한 파일 목록이다.
clasp는 그 프로젝트를 로컬 파일 시스템으로 내리고 다시 올리는 통로를 제공한다.

그래서 얻는 것이 넷으로 정리된다.

| 기능           | 내용                                                                |
| -------------- | ------------------------------------------------------------------- |
| 로컬 개발      | 코드를 소스 관리에 넣고, 다른 개발자와 협업하고, 원하는 도구를 쓴다 |
| 배포 버전 관리 | 여러 배포본을 만들고 갱신하고 조회한다                              |
| 코드 구조화    | 평평한 온라인 프로젝트를 로컬에서는 폴더 구조로 변환한다            |
| 원격 실행      | 명령줄에서 Apps Script 함수를 실행한다                              |

폴더 변환의 예가 README에 있다.
`script.google.com`에서 `tests/slides.gs`와 `tests/sheets.gs`인 것이, 로컬에서는 `tests/` 디렉터리 아래 `slides.js`와 `sheets.js`가 된다.
이름에 슬래시를 넣는 관례를 실제 디렉터리로 바꿔 주는 것이다.

Node.js 22.0.0 이상이 필요하다.

## 설치와 최초 설정

설치는 npm 전역 설치다.

```bash
npm install -g @google/clasp
```

그다음 반드시 해야 하는 단계가 있다. `https://script.google.com/home/usersettings`에서 Google Apps Script API를 켜는 것이다.
이것을 빠뜨리면 이후 모든 명령이 실패한다.

에이전트 도구로 붙이는 경로도 제공된다.

```bash
# Gemini CLI 확장으로 설치하면 MCP 서버로 쓸 수 있다
gemini extensions install https://github.com/google/clasp

# Claude Code 플러그인으로 설치
/plugin install @google/clasp

# 또는 MCP 서버로 직접 등록
claude mcp add clasp -- npx -y @google/clasp mcp
claude mcp add-json clasp "$(cat claude-mcp.json)"
```

어느 경로로 붙이든 Apps Script API를 켜고 `clasp login`을 먼저 해야 한다고 명시한다.

MCP 모드 자체는 실험적이라고 표시되어 있다.
STDIO 전송으로 로컬 도구로 설정하며, CLI로 쓸 때와 같은 자격 증명을 쓴다.
MCP 모드에서는 프로젝트 디렉터리에서 시작할 필요가 없고 도구 호출에서 디렉터리를 지정한다.
프로젝트를 바꾸는 데는 서버 재시작이 필요 없지만 자격 증명을 바꾸는 데는 필요하다.

## 명령 구성

기본 명령이 프로젝트 수명 주기를 따라간다.

| 명령                      | 하는 일                                  |
| ------------------------- | ---------------------------------------- |
| `clasp login`             | 인증. 홈 디렉터리에 `.clasprc.json` 저장 |
| `clasp create-script`     | 새 스크립트 프로젝트 생성                |
| `clasp clone-script`      | 기존 스크립트를 로컬로 복제              |
| `clasp pull`              | 원격 내용을 로컬로 가져오기              |
| `clasp push`              | 로컬 내용을 원격으로 올리기              |
| `clasp show-file-status`  | `push`에서 올라갈 파일 목록 확인         |
| `clasp create-version`    | 버전 생성                                |
| `clasp create-deployment` | 배포 생성                                |
| `clasp open-script`       | 웹 편집기 열기                           |

고급 명령은 GCP 프로젝트 ID 설정이 필요하다.

| 명령                 | 하는 일                                    |
| -------------------- | ------------------------------------------ |
| `clasp setup-logs`   | 로그를 보기 위한 GCP 프로젝트 ID 설정 확인 |
| `clasp tail-logs`    | Cloud Logging 로그 출력                    |
| `clasp list-apis`    | 고급 서비스로 켤 수 있는 Google API 목록   |
| `clasp enable-api`   | API 활성화                                 |
| `clasp run-function` | 원격 함수 실행                             |

로그 명령에 중요한 단서가 붙어 있다.
출력되는 것은 Cloud Logging 로그이며 `console.log`에서 온 것이지 `Logger.log`에서 온 것이 아니라는 점이다.
Apps Script에서 두 로깅 함수가 다른 곳으로 가는 것을 모르면 로그가 비어 보인다.

## 2.x에서 3.x로

3.x는 두 가지 큰 변화를 가져왔다.

첫째는 TypeScript 지원 제거다.
clasp가 더 이상 TypeScript 코드를 트랜스파일하지 않으며, TypeScript 프로젝트는 Rollup 같은 번들러로 먼저 변환한 뒤 push하라고 안내한다.
이것이 장점이 있다고 README가 주장한다. TypeScript 기능에 대한 더 견고한 지원과 함께 ESM 모듈과 NPM 패키지 지원을 제공한다는 것이다.
템플릿 프로젝트로 `WildH0g/apps-script-engine-template`, `tomoyanakano/clasp-typescript-template`, `google/aside`, `sqrrrl/apps-script-typescript-rollup-starter`를 든다.

둘째는 명령 이름 변경이다. 일관성을 위해 덜 쓰이는 명령들이 재구성되었다.

| 2.x                    | 3.x                              |
| ---------------------- | -------------------------------- |
| `open`                 | `open-script`                    |
| `open --web`           | `open-web-app`                   |
| `open --addon`         | `open-container`                 |
| `open --creds`         | `open-credentials-setup`         |
| `login --creds <file>` | `login -u <name> --creds <file>` |
| `logs --open`          | `open-logs`                      |
| `logs --setup`         | 없음                             |
| `apis --open`          | `open-api-console`               |
| `apis enable <api>`    | `enable-api <api>`               |
| `apis disable <api>`   | `disable-api <api>`              |
| `deploy -i <id>`       | `update-deployment <id>`         |
| `settings`             | 없음                             |

다른 명령들도 이름이 바뀌었지만 호환성을 위해 별칭이 남아 있다고 적는다.
`logs --setup`과 `settings`는 대체 없이 사라졌다.

## 인증 설계

인증이 이 도구에서 가장 결정할 것이 많은 부분이다.

기본은 `clasp login`이고 홈 디렉터리의 `.clasprc.json`에 자격 증명을 저장한다.

여러 계정을 쓰려면 전역 `--user` 옵션을 쓴다.

```bash
clasp login                                    # 기본 자격 증명으로 저장
clasp clone                                    # 사용자 미지정, 기본 자격 증명 사용
clasp login --user testaccount                 # 이름 붙인 새 자격 증명 승인
clasp run-function --user testaccount myFunction  # 테스트 계정으로 함수 실행
```

`clasp run-function`을 다른 계정으로 실행할 수 있다는 점이 중요하다.
스크립트가 어떤 사용자의 권한으로 도는지가 결과를 바꾸는 경우가 많기 때문이다.

로그인 옵션이 많은 이유는 OAuth 스코프 때문이다.

| 옵션                      | 의미                                                      |
| ------------------------- | --------------------------------------------------------- |
| `--no-localhost`          | 로컬 서버를 띄우지 않고 코드를 직접 입력                  |
| `--creds <file>`          | 자체 자격 증명 사용. 현재 디렉터리에 `.clasprc.json` 저장 |
| `--use-project-scopes`    | clasp 기본 스코프 대신 `appsscript.json`의 스코프 사용    |
| `--include-clasp-scopes`  | 프로젝트 스코프에 더해 clasp 기본 스코프도 포함           |
| `--extra-scopes <scopes>` | 쉼표로 구분한 추가 OAuth 스코프                           |
| `--redirect-port <port>`  | 로그인 중 로컬 리디렉션 서버의 포트 지정                  |

`--creds`로 저장되는 파일이 현재 작업 디렉터리에 생긴다는 점이 함정이다.
README도 이 파일이 비공개여야 한다고 경고한다.

## 자체 GCP 프로젝트 쓰기

clasp는 기본 OAuth 클라이언트를 포함하지만, 자체 프로젝트를 쓰는 것을 권장한다.
사용자가 어떤 서드파티 앱을 승인할 수 있는지 제한하는 환경에서 보안과 컴플라이언스를 개선할 수 있기 때문이다.

설정 절차는 셋이다.
Google Cloud 콘솔에서 새 프로젝트를 만들고, `Desktop Application` 타입의 OAuth 클라이언트를 만들어 클라이언트 시크릿 파일을 받고, 필요한 서비스를 켠다.

| API                           | 필요한 이유                                       |
| ----------------------------- | ------------------------------------------------- |
| `script.googleapis.com`       | 필수                                              |
| `serviceusage.googleapis.com` | API 목록 조회·활성화·비활성화에 필요              |
| `drive.googleapis.com`        | 스크립트 목록 조회, 컨테이너 바운드 스크립트 생성 |
| `logging.googleapis.com`      | 로그 읽기                                         |

외부 사용을 위해 OAuth 스코프를 등록해야 한다면 다음을 포함하라고 안내한다.

```text
https://www.googleapis.com/auth/script.deployments
https://www.googleapis.com/auth/script.projects
https://www.googleapis.com/auth/script.webapp.deploy
https://www.googleapis.com/auth/drive.metadata.readonly
https://www.googleapis.com/auth/drive.file
https://www.googleapis.com/auth/service.management
https://www.googleapis.com/auth/logging.read
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
https://www.googleapis.com/auth/cloud-platform
```

조직이 서드파티 앱 승인을 제한한다면 두 선택지가 있다.
관리자에게 clasp의 클라이언트 ID `1072944905499-vm2v2i5dvn0a0d2o4ca36i1vge8cvbn0.apps.googleusercontent.com`를 허용 목록에 넣어 달라고 요청하거나, 내부 전용 GCP 프로젝트를 위와 같이 설정하는 것이다.

서비스 계정 지원은 `--adc` 옵션으로 제공되지만 README가 명시적으로 “실험적 / 동작하지 않음”이라고 표시한다.
그리고 근본적인 제약을 밝힌다. 서비스 계정은 스크립트를 소유할 수 없으므로, 서비스 계정으로 push나 pull을 하려면 스크립트를 그 계정과 적절한 역할로 공유해야 한다는 것이다. push하려면 `Editor`다.

## 프로젝트 설정 파일

`clone`이나 `create`를 실행하면 현재 디렉터리에 `.clasp.json`이 만들어진다.

```json
{
  "scriptId": "",
  "rootDir": "build/",
  "projectId": "project-id-xxxxxxxxxxxxxxxxxxx",
  "fileExtension": "ts",
  "filePushOrder": ["file1.ts", "file2.ts"]
}
```

| 키                   | 필수   | 의미                                                                |
| -------------------- | ------ | ------------------------------------------------------------------- |
| `scriptId`           | 예     | 대상 Apps Script 프로젝트의 ID                                      |
| `rootDir`            | 아니오 | clasp가 프로젝트 파일을 둘 로컬 디렉터리. 기본은 현재 디렉터리      |
| `projectId`          | 아니오 | 대상 GCP 프로젝트 ID. 설정하지 않으면 필요한 시점에 프롬프트로 물음 |
| `fileExtension`      | 아니오 | 사용 중단됨                                                         |
| `scriptExtensions`   | 아니오 | 스크립트로 간주할 확장자. 기본 `[".js", ".gs"]`                     |
| `htmlExtensions`     | 아니오 | HTML로 간주할 확장자. 기본 `[".html"]`                              |
| `filePushOrder`      | 아니오 | 먼저 push할 파일 목록. 실행 순서에 의존하는 스크립트에 유용         |
| `skipSubdirectories` | 아니오 | 하위 디렉터리를 무시하던 이전 동작과의 호환용                       |

`scriptExtensions`와 `htmlExtensions`에서 첫 번째 확장자가 pull 시 파일을 쓸 때 쓰인다는 점이 세부 규칙이다.

`filePushOrder`의 경로는 `.clasp.json`이 있는 디렉터리 기준이며, `rootDir`도 설정했다면 그 경로까지 포함해야 한다.

전역 옵션으로 파일 위치를 바꿀 수 있다.

| 옵션               | 용도                                                         |
| ------------------ | ------------------------------------------------------------ |
| `--user <name>`    | 이름 붙인 자격 증명 사용. 생략하면 `default`                 |
| `--adc`            | 환경의 애플리케이션 기본 자격 증명 사용. CI의 서비스 계정용  |
| `--project <file>` | `.clasp.json` 대신 다른 파일에서 설정 읽기. 다중 배포 대상용 |
| `--auth <file>`    | 사용 중단됨. `--user`를 쓸 것                                |
| `--ignore <file>`  | `.claspignore` 대신 다른 파일에서 무시 패턴 읽기             |
| `--json`           | JSON 형식 출력                                               |

`--project`가 스테이징과 프로덕션을 나누는 표준 경로다.

## 무시 규칙

`.claspignore`가 `push`에서 올리지 않을 파일을 정한다.

```text
**/**
!build/main.js
!appsscript.json
```

이것이 매니페스트와 `build/main.js`만 남기는 예다.

중요한 차이가 하나 있다.
패턴이 multimatch로 적용되며 이것이 `.gitignore`와 다르고 특히 디렉터리에서 그렇다는 것이다.
디렉터리를 무시하려면 `**/node_modules/**` 같은 문법을 써야 한다.
그리고 패턴은 `rootDir` 기준 상대 경로로 적용된다.

`.claspignore`가 없으면 기본 패턴이 적용된다.

```text
# 모든 파일을 무시하고…
**/**

# 이 확장자만 예외로 두되…
!appsscript.json
!**/*.gs
!**/*.js
!**/*.ts
!**/*.html

# 이 디렉터리 안이면 유효한 파일도 무시한다
.git/**
node_modules/**
```

기본값에서 `.git`과 `node_modules`를 제외한 하위 폴더는 처리된다는 점이 2.x와의 차이이며, `skipSubdirectories`가 그 호환을 위해 존재한다.

## 트레이드오프

### push가 전체 교체이므로 원격 편집과 로컬 편집을 동시에 할 수 없다

README가 경고 블록으로 명시한다.
Google의 scripts API가 현재 원자적 연산도 파일 단위 연산도 지원하지 않으므로, `push` 명령이 항상 온라인 프로젝트의 전체 내용을 push하는 파일들로 **교체**한다는 것이다.

이 한 문장이 clasp를 쓰는 팀의 워크플로를 사실상 결정한다.
누군가 웹 편집기에서 고친 것이 있으면 `push` 한 번에 사라지고, 되돌릴 방법은 Apps Script 자체의 버전 이력뿐이다.
git의 3방향 병합 같은 것이 존재하지 않는다.

그래서 실무에서 가능한 규율은 둘 중 하나다.
웹 편집기를 읽기 전용으로 취급하고 모든 편집을 로컬에서 하거나, 반대로 clasp를 `pull` 전용으로 써서 백업과 버전 관리에만 쓰는 것이다.
두 방향을 섞으면 반드시 누군가의 작업이 사라진다.

그리고 이 제약은 clasp의 결함이 아니라 API의 성질이다.
파일 단위 연산이 없으면 어떤 클라이언트도 부분 갱신을 할 수 없고, 여러 클라이언트가 동시에 쓰는 것을 안전하게 만들 수 없다.
clasp가 고칠 수 있는 문제가 아니라는 점이 중요하다. 대안 도구로 옮겨도 같은 벽에 부딪힌다.

### TypeScript를 뺀 것은 더 나은 TypeScript를 위한 선택이지만 진입 비용을 올린다

3.x가 TypeScript 트랜스파일을 제거한 논리는 타당하다.
clasp가 내장한 변환기는 Apps Script가 이해하는 부분집합으로만 변환할 수 있었고, ESM 모듈이나 npm 패키지를 다룰 수 없었다.
Rollup 같은 번들러를 앞에 두면 그 제약이 사라진다.

대가는 설정 복잡도다.
2.x에서는 `.ts` 파일을 두고 `clasp push`만 하면 됐는데, 3.x에서는 번들러 설정, 빌드 스텝, `rootDir`를 빌드 출력으로 맞추는 작업이 추가된다.
README가 템플릿 저장소 넷을 나열하는 것 자체가 이 설정이 처음부터 쓰기에는 부담스럽다는 인정이다.

그리고 이 변화가 clasp의 대상 사용자를 이동시킨다.
Apps Script를 쓰는 사람의 상당수는 프런트엔드 빌드 도구에 익숙하지 않은 업무 자동화 담당자이고, 그들에게 Rollup 설정은 새로운 학습 영역이다.
결과적으로 3.x는 전문 개발자에게 더 나은 도구가 되면서 원래 사용자층에게는 문턱을 올렸다.

중간 지대가 없다는 점도 짚을 만하다.
간단한 타입 주석만 원하는 경우에도 번들러 전체를 세워야 하며, JSDoc 타입 주석으로 대체하는 경로는 README가 언급하지 않는다.

### 자체 OAuth 클라이언트를 쓰는 것이 권장이지만 그 비용이 명시되지 않는다

기본 클라이언트를 쓰면 즉시 시작할 수 있고, 자체 클라이언트를 쓰면 승인 범위를 통제할 수 있다.
README는 후자를 권장하면서 설정 절차를 셋으로 요약한다.

실제 비용은 그보다 크다.
OAuth 동의 화면 설정, 테스트 사용자 등록 또는 조직 내부 게시, 그리고 민감 스코프가 포함된 경우의 검증 절차가 뒤따른다.
나열된 스코프 중 `drive.file`, `cloud-platform`, `service.management`는 가볍게 승인되는 종류가 아니다.

그리고 개인이 쓰는 경우와 조직이 쓰는 경우의 계산이 다르다.
개인이면 기본 클라이언트가 편하고 위험도 낮지만, 조직이면 그 클라이언트 ID를 허용 목록에 넣는 결정이 IT 관리자에게 간다.
README가 그 요청 문구까지 제공한다는 것은 이 상황이 흔하다는 뜻이다.

여기서 실질적인 선택 기준이 나온다.
혼자 쓰고 스크립트가 민감 데이터를 다루지 않으면 기본 클라이언트, 조직 자산을 다루거나 CI에서 돌릴 계획이면 처음부터 자체 프로젝트다.
나중에 옮기는 것이 가능하지만 재인증과 스코프 재승인이 따르므로, 처음에 정하는 편이 싸다.

### 서비스 계정이 동작하지 않는다는 사실이 자동화의 상한을 정한다

`--adc` 옵션이 있고 CI 워크플로의 서비스 계정을 지원하려는 의도라고 적혀 있지만, 제목에 “실험적 / 동작하지 않음”이 붙어 있다.

그리고 그 아래 설명이 왜 어려운지를 말해 준다.
서비스 계정은 스크립트를 소유할 수 없으므로, push나 pull을 하려면 스크립트를 서비스 계정과 공유해야 한다는 것이다.

이 제약이 CI 설계를 바꾼다.
서비스 계정이 쓸 수 없다면 CI가 쓸 수 있는 것은 사람 계정의 리프레시 토큰뿐이고, 그 토큰을 비밀 저장소에 넣어야 한다.
그러면 그 계정의 권한 전체가 CI에 노출되고, 계정 소유자가 퇴사하면 파이프라인이 멈춘다.

대안은 자동화 전용 Google 계정을 만드는 것인데, 이것은 조직 정책상 금지되는 경우가 많고 2단계 인증 관리도 별도 문제가 된다.
즉 “Apps Script 코드를 CI로 배포한다”는 요구는 clasp의 문제가 아니라 Apps Script 플랫폼의 계정 모델 때문에 깔끔한 답이 없다.

## 함정

Apps Script API를 켜지 않으면 모든 명령이 실패하는데, 오류 메시지가 그 원인을 바로 가리키지 않는다.
설치 직후 첫 명령이 실패하면 `https://script.google.com/home/usersettings`를 먼저 확인하는 것이 가장 빠르다.

`clasp push`는 전체 교체다. 웹 편집기에서의 변경은 `push` 전에 반드시 `pull`로 가져와야 한다.

`.claspignore`의 패턴이 `.gitignore`와 다르게 동작한다.
`node_modules/`로 쓰면 디렉터리가 무시되지 않으며 `**/node_modules/**`라고 써야 한다.
`.gitignore` 문법이라고 생각하고 쓰면 `node_modules` 전체가 올라간다.

`.claspignore` 패턴이 `rootDir` 기준이라는 점도 놓치기 쉽다.
`rootDir`를 `build/`로 두고 패턴을 저장소 루트 기준으로 쓰면 아무것도 매칭되지 않는다.

`clasp tail-logs`가 보여 주는 것은 `console.log`의 출력이지 `Logger.log`의 출력이 아니다.
`Logger.log`로 쓴 로그는 웹 편집기의 실행 기록에서만 보인다.

`login --creds`는 `.clasprc.json`을 현재 디렉터리에 만든다. 저장소 루트에서 실행하면 자격 증명이 커밋될 수 있다.
`.gitignore`에 `.clasprc.json`을 먼저 넣어 두는 편이 안전하다.

`filePushOrder`의 경로는 `rootDir`까지 포함해야 한다. 빌드 출력 디렉터리를 쓰면서 소스 경로를 적으면 순서가 적용되지 않는다.

Node 22 미만에서는 동작하지 않는다.

`--auth` 옵션은 사용 중단되었다. 여러 계정을 쓰려면 `--user`다.

3.x로 올리면 `logs --setup`과 `settings`가 사라진다. 스크립트에서 이 명령을 쓰고 있었다면 대체가 없다.

## 확인하기

설치부터 왕복까지를 한 번에 확인하는 절차다.

```bash
# 1. 버전 요건을 먼저 본다
node -v        # 22.0.0 이상이어야 한다
clasp --version

# 2. 인증 상태와 어떤 클라이언트를 쓰는지 확인한다
#    clientType 이 google-provided 인지 user-provided 인지가 핵심이다
clasp show-authorized-user --json

# 3. 빈 프로젝트를 만들어 왕복을 시험한다
mkdir /tmp/clasp-test && cd /tmp/clasp-test
clasp create-script --title "clasp-roundtrip-test" --type standalone

# 4. 파일 하나를 만들고 무엇이 올라갈지 먼저 본다
echo 'function hello() { console.log("hi"); }' > hello.js
clasp show-file-status --json

# 5. 올리고 다시 내려서 내용이 같은지 본다
clasp push
rm hello.js
clasp pull
cat hello.js

# 6. 원격 실행과 로그를 확인한다
clasp run-function hello
clasp tail-logs
```

4번이 이 도구에서 가장 값진 습관이다.
`push`가 전체 교체이므로, 무엇이 올라가는지 모른 채 `push`하는 것이 사고의 대부분을 만든다.

`.claspignore`를 고쳤을 때도 같은 방식으로 확인한다.

```bash
# 패턴을 고친 뒤 실제로 무엇이 제외되는지 본다
clasp show-file-status --json | python3 -m json.tool
```

`node_modules` 안의 파일이 목록에 보이면 패턴이 `.gitignore` 문법으로 쓰여 있는 것이다.

## 체크리스트

- Node 22 이상인가
- `https://script.google.com/home/usersettings`에서 Apps Script API를 켰는가
- 팀에서 웹 편집기 편집을 금지하거나, 반대로 clasp를 pull 전용으로 쓰기로 합의했는가
- `push` 전에 `show-file-status`로 올라갈 목록을 확인하는 습관이 있는가
- `.claspignore`의 디렉터리 패턴을 `**/dir/**` 형태로 썼는가
- `.claspignore` 패턴이 `rootDir` 기준이라는 것을 반영했는가
- `.clasprc.json`이 `.gitignore`에 있는가
- 조직 자산을 다룬다면 자체 GCP 프로젝트와 OAuth 클라이언트를 준비했는가
- 필요한 API 넷(`script`, `serviceusage`, `drive`, `logging`)을 켰는가
- 여러 배포 대상이 있다면 `--project`로 설정 파일을 분리했는가
- CI 배포가 필요하다면 서비스 계정이 동작하지 않는다는 제약을 알고 대안을 정했는가
- TypeScript를 쓴다면 번들러 설정과 `rootDir`를 빌드 출력으로 맞췄는가
- 3.x로 올릴 때 `logs --setup`이나 `settings`를 쓰는 스크립트가 없는지 확인했는가

## 비평

### 공식 지원 제품이 아니라는 문구와 이 도구의 위치가 어긋난다

README 두 번째 줄이 공식적으로 지원되는 Google 제품이 아니라고 밝힌다.
그런데 이 도구는 `google` 조직 아래 있고, `@google/clasp`라는 npm 스코프를 쓰며, Apps Script를 로컬에서 개발하는 유일한 실질적 경로다.

이 조합이 사용자에게 어려운 위치를 만든다.
Apps Script를 소스 관리에 넣으려면 clasp 말고 선택지가 없는데, 그 도구는 지원 약속이 없다.
기업이 Apps Script로 만든 내부 도구를 정식 소프트웨어 자산으로 관리하려 할 때, 그 파이프라인 전체가 비공식 도구 위에 서게 된다.

API 자체의 제약이 이 문제를 키운다.
파일 단위 연산도 원자적 연산도 없다는 것은 API 설계에서 로컬 개발이 일급 사용 사례가 아니었다는 뜻이고, clasp가 그 위에서 할 수 있는 최선을 하고 있는 것이다.
즉 진짜 공백은 clasp가 아니라 Apps Script API에 있으며, 비공식 도구가 그 공백을 메우고 있다는 구조가 여러 해째 유지되고 있다.

### MCP 모드를 실험적이라고 하면서 설치 안내에서는 대등하게 제시한다

설치 절에서 Gemini CLI 확장과 Claude Code 플러그인이 npm 설치 바로 다음에 나온다.
Claude Code 쪽은 플러그인 설치를 권장으로 표시하기까지 한다.

그런데 명령 목록으로 내려가면 `clasp mcp`가 실험적이며 에이전트를 위한 제한된 도구 부분집합만 제공한다고 적혀 있다.
두 서술이 같은 문서에 있고 서로를 참조하지 않는다.

이 불일치가 실무에서 문제가 되는 이유는, 에이전트로 Apps Script를 다루려는 사람이 설치 절만 보고 결정하기 때문이다.
어떤 도구가 노출되는지, 어떤 작업이 CLI로만 가능한지를 알려면 문서를 더 내려가야 하며, 그 정보도 “제한된 부분집합”이라는 말 외에는 없다.

그리고 자격 증명 전환에 서버 재시작이 필요하다는 제약이 MCP 절에만 있다.
여러 계정으로 스크립트를 다루는 것이 이 도구의 주요 사용 패턴인데, 에이전트 경로에서는 그것이 매끄럽지 않다는 사실이 설치 안내에 없다.

### 명령 이름 변경이 일관성을 개선했다는 주장이 절반만 맞다

3.x가 명령을 재구성한 이유를 일관성 개선이라고 적는다.
확실히 개선된 부분이 있다. `apis enable`이 `enable-api`가 되고 `logs --open`이 `open-logs`가 된 것은 동사-목적어 형태로 통일한 결과다.

그런데 그 통일이 완전하지 않다.
`push`와 `pull`은 그대로 남았고 `create-script`와 `clone-script`는 접미사가 붙었으며, `show-file-status`와 `list-deployments`는 동사가 다르다.
가장 자주 쓰는 명령들은 짧게 두고 덜 쓰는 것만 길게 만든 것인데, 그것은 일관성이 아니라 사용 빈도에 따른 타협이다.

타협 자체는 합리적이다. 매일 치는 `push`를 `push-files`로 바꾸는 것은 개선이 아니다.
문제는 README가 그 이유를 밝히지 않고 일관성이라고만 말한다는 점이다.
그래서 사용자는 규칙을 추론할 수 없고 명령마다 외워야 한다.

그리고 대체 없이 사라진 둘이 문서에서 가볍게 처리된다.
`settings`는 프로젝트 설정을 조회하던 명령이고 `logs --setup`은 `setup-logs`로 옮겨 간 것처럼 보이지만 표에는 “N/A”로 적혀 있어, 실제로 어떻게 대응해야 하는지가 표만으로는 판단되지 않는다.

## 기억할 원칙

### 플랫폼 API가 부분 갱신을 제공하지 않으면 그 위의 모든 도구가 전체 교체 도구가 된다

clasp의 가장 중요한 제약은 clasp 안에 없다.
Apps Script API가 파일 단위 연산과 원자적 연산을 제공하지 않으므로, 그 위의 어떤 클라이언트도 “이 파일만 갱신”을 할 수 없다.

이 관계가 일반적이다.
동기화 도구의 안전성 상한은 그 도구의 설계가 아니라 원격 API가 제공하는 연산의 입도가 정한다.
조건부 갱신(ETag, If-Match)이 없으면 낙관적 동시성 제어를 구현할 수 없고, 부분 갱신이 없으면 병합을 구현할 수 없다.

그래서 어떤 서비스를 코드로 관리하려 할 때 먼저 확인할 것이 정해진다.
읽기와 쓰기가 되는지가 아니라, 조건부 쓰기가 되는지와 부분 쓰기가 되는지다.
둘 다 없으면 그 서비스에 대한 GitOps나 IaC 스타일 워크플로는 “마지막에 쓴 사람이 이긴다”로 귀결되며, 그 사실을 팀 규율로 보완할 수밖에 없다.

그리고 이 확인은 도구를 고르기 전에 해야 한다.
도구를 바꿔도 이 상한은 그대로이므로, 도구 비교에 시간을 쓰는 대신 워크플로를 단방향으로 설계하는 데 쓰는 편이 낫다.

### 무시 규칙의 문법이 `.gitignore`와 다르면 그 차이가 가장 비싼 버그가 된다

`.claspignore`가 multimatch를 쓰고 디렉터리 처리가 `.gitignore`와 다르다는 사실은 README의 한 문장이다.
그런데 이 한 문장을 놓치면 `node_modules` 전체가 Apps Script 프로젝트로 올라간다.

이런 종류의 차이가 특히 비싼 이유는 실패가 조용하기 때문이다.
잘못된 패턴은 오류를 내지 않고 그냥 매칭되지 않으며, 결과는 push가 느려지거나 프로젝트가 커지는 형태로 나타난다.
그리고 push가 전체 교체이므로 잘못 올라간 파일을 지우려면 다시 전체를 push해야 한다.

일반화하면, 익숙한 파일 이름을 쓰는 설정 파일이 다른 문법을 쓰는 것이 가장 위험한 조합이다.
`.claspignore`, `.dockerignore`, `.npmignore`, `.eslintignore`가 전부 `.gitignore`처럼 생겼고 전부 조금씩 다르게 동작한다.
이름이 비슷하면 사람은 문서를 읽지 않고 기존 지식을 적용한다.

그래서 이런 파일을 처음 쓸 때 해야 할 일이 하나 정해진다.
패턴을 쓴 뒤 그 도구가 제공하는 “무엇이 포함되는지” 조회 명령을 반드시 한 번 돌려 보는 것이다.
clasp에서는 `clasp show-file-status`이고, Docker에서는 빌드 컨텍스트 크기이며, npm에서는 `npm pack --dry-run`이다.
이 한 번의 확인이 문법 차이로 생기는 사고의 대부분을 막는다.
