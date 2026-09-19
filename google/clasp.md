# Clasp: Apps Script 프로젝트를 로컬에서 개발하는 CLI

> Develop Apps Script projects locally using clasp
> (**C**ommand **L**ine **A**pps **S**cript **P**rojects).
>
> Note: This is not an officially supported Google product.

<https://github.com/google/clasp>

- [Use the command-line interface with clasp  |  Apps Script  |  Google for Developers](https://developers.google.com/apps-script/guides/clasp)
- [clasp와 함께 명령줄 인터페이스 사용  |  Apps Script  |  Google for Developers](https://developers.google.com/apps-script/guides/clasp?hl=ko)

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

## clasp가 다루지 않는 것

이 절이 이 문서에서 가장 실용적인 부분이다.
“Apps Script를 Git으로 관리한다”고 말할 때 실제로 Git에 들어가는 것이 무엇인지가 여기서 정해지기 때문이다.

Google 공식 문서가 이 경계를 한 문장으로 명시한다.
clasp가 독립 스크립트와 컨테이너 바운드 스크립트를 모두 관리하지만, 트리거와 문서 속성과 사용자 속성은 직접 관리하지 않으며 그것들은 Apps Script 런타임 환경 안에 남는다는 것이다.

| 프로젝트 상태                   | clasp가 다루는가 | 어디에 사는가                     |
| ------------------------------- | ---------------- | --------------------------------- |
| 스크립트 파일(`.gs`/`.js`)      | 예               | 파일                              |
| HTML 파일                       | 예               | 파일                              |
| 매니페스트(`appsscript.json`)   | 예               | 파일                              |
| 시간 기반·이벤트 트리거         | 아니오           | 서버 측 프로젝트 상태             |
| Script/User/Document Properties | 아니오           | 서버 측 속성 저장소               |
| 배포본과 배포 ID                | 명령으로만       | 서버 측. 파일로 표현되지 않음     |
| 버전 번호와 설명                | 명령으로만       | 서버 측                           |
| 라이브러리 의존 버전            | 부분적           | 매니페스트에 선언되나 승인은 서버 |
| 컨테이너 바운드 연결            | 아니오           | 생성 시점에 고정                  |
| OAuth 승인 상태                 | 아니오           | 사용자 계정                       |
| 편집자·뷰어 권한                | 아니오           | Drive 권한                        |

트리거가 특히 중요하다.
매니페스트에 선언할 수 있는 것은 애드온용 단순 트리거 정도이고, `ScriptApp.newTrigger()`로 만들었거나 웹 편집기에서 손으로 만든 설치형 트리거는 서버에만 존재한다.
즉 저장소를 새 스크립트에 통째로 push해도 트리거는 따라오지 않으며, 그 사실을 모르면 “코드는 배포했는데 아무것도 안 돈다”가 된다.

Properties도 같다. API 키나 시트 ID를 `PropertiesService`에 넣어 두었다면 그것은 코드가 아니라 데이터이고 clasp의 시야 밖이다.
이 성질은 보안상 바람직하지만(키가 저장소에 들어가지 않는다) 재현성 면에서는 공백이다.

## 메타데이터를 관리하는 방법

파일이 아닌 상태를 다루는 방법은 셋이고, 셋을 함께 써야 빈틈이 없다.

| 방법              | 대상                  | 저장소에 들어가는 것     |
| ----------------- | --------------------- | ------------------------ |
| 선언을 코드로     | 트리거, 필수 속성 키  | 생성·검증 함수           |
| 스냅숏을 파일로   | 현재 트리거·속성 구성 | 내보낸 JSON(값은 마스킹) |
| 명령을 스크립트로 | 버전·배포             | 배포 스크립트와 배포 ID  |

### 트리거를 코드로 선언하기

트리거 생성을 부트스트랩 함수 한곳에 모으면, 파일이 아닌 상태가 최소한 **선언**으로는 저장소에 남는다.

```javascript
/**
 * 프로젝트를 재현 가능한 상태로 만드는 부트스트랩.
 * 새 환경에 push한 뒤 이 함수를 한 번 실행하면 트리거가 선다.
 * 웹 편집기에서 손으로 만든 트리거는 Git이 볼 수 없으므로,
 * 트리거 생성은 반드시 이 함수 한 곳에만 둔다.
 */
function bootstrapTriggers() {
  // 기존 트리거를 먼저 지운다. 그래야 이 함수가 멱등해진다.
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));

  ScriptApp.newTrigger('dailySync')
    .timeBased()
    .atHour(3)               // 운영 시간대를 피한다
    .everyDays(1)
    .create();

  const formId = PropertiesService.getScriptProperties().getProperty('FORM_ID');
  ScriptApp.newTrigger('onFormSubmitHandler')
    .forForm(formId)
    .onFormSubmit()
    .create();
}
```

### 필수 속성을 코드로 선언하기

값은 저장소에 두지 않고 **어떤 키가 필요한지**만 코드로 남긴다.

```javascript
/** 이 프로젝트가 요구하는 Script Properties 계약. */
const REQUIRED_PROPERTIES = ['FORM_ID', 'SHEET_ID', 'WEBHOOK_URL'];

/**
 * 배포 직후와 각 트리거 진입점에서 호출한다.
 * 런타임 중간이 아니라 시작 시점에 실패시키는 것이 목적이다.
 */
function assertRequiredProperties() {
  const props = PropertiesService.getScriptProperties();
  const missing = REQUIRED_PROPERTIES.filter(k => !props.getProperty(k));
  if (missing.length) {
    throw new Error(`Missing script properties: ${missing.join(', ')}`);
  }
}
```

### 메타데이터를 파일로 내보내기

선언만으로는 “지금 서버가 어떤 상태인가”를 알 수 없다.
그래서 현재 상태를 JSON으로 덤프하는 함수를 두고, 그 출력을 저장소의 `metadata/`에 커밋한다.

```javascript
/**
 * 현재 프로젝트의 트리거와 속성 키를 JSON으로 덤프한다.
 * clasp run-function 으로 호출해 출력을 파일로 저장한다.
 * 속성 값은 비밀일 수 있으므로 키와 존재 여부만 남긴다.
 */
function exportMetadata() {
  const triggers = ScriptApp.getProjectTriggers().map(t => ({
    handlerFunction: t.getHandlerFunction(),
    eventType: String(t.getEventType()),
    triggerSource: String(t.getTriggerSource()),
    // 소스 ID 는 폼·시트 ID 라서 환경마다 다르다. 키로만 남긴다.
    triggerSourceId: t.getTriggerSourceId() ? '<set>' : null,
  }));

  const scriptProps = PropertiesService.getScriptProperties().getProperties();
  const propertyKeys = Object.keys(scriptProps).sort().map(k => ({
    key: k,
    // 값 자체는 내보내지 않는다. 설정 여부와 길이만 기록한다.
    isSet: scriptProps[k] !== '',
    length: scriptProps[k].length,
  }));

  return JSON.stringify({ triggers, propertyKeys }, null, 2);
}
```

```bash
# 내보낸 스냅숏을 저장소에 넣는다
clasp run-function exportMetadata --user prod > metadata/prod.json
git diff metadata/prod.json    # 서버 상태가 바뀌었는지 리뷰에서 보인다
```

이 파일이 하는 일은 재현이 아니라 **검출**이다.
누군가 웹 편집기에서 트리거를 추가하면 다음 덤프에서 diff로 드러나고, 그때 그것을 `bootstrapTriggers()`에 반영할지 지울지 결정하면 된다.

### 속성 값을 환경별로 주입하기

값 자체는 저장소에 두지 않되, 주입 절차는 자동화한다.

```bash
#!/usr/bin/env bash
# set-properties.sh — 환경별 속성을 한 번에 주입한다
# 값은 비밀 관리자에서 읽고 저장소에는 키 목록만 둔다
set -euo pipefail

env="${1:?usage: set-properties.sh <staging|prod>}"

# 임시 Apps Script 함수에 넘길 JSON 을 만든다
payload=$(jq -n \
  --arg form "$(op read "op://apps-script/$env/FORM_ID")" \
  --arg sheet "$(op read "op://apps-script/$env/SHEET_ID")" \
  '{FORM_ID: $form, SHEET_ID: $sheet}')

clasp run-function setProperties --user "$env" -p "[$payload]"
```

```javascript
/** 외부에서 주입받은 속성을 일괄 설정한다. */
function setProperties(values) {
  PropertiesService.getScriptProperties().setProperties(values, false);
  assertRequiredProperties();
}
```

`setProperties`의 두 번째 인자를 `false`로 두는 것이 결정 지점이다.
`true`로 하면 기존 속성을 모두 지우고 교체하므로, 주입 목록에 없는 키가 사라진다.

### 저장소 구조

```text
.
├── src/                     # 소스. 번들러 입력
├── build/                   # rootDir. push 대상
├── metadata/
│   ├── prod.json            # exportMetadata 출력
│   └── staging.json
├── scripts/
│   ├── clasp-drift-check.sh
│   ├── deploy.sh
│   └── set-properties.sh
├── .clasp.prod.json         # scriptId 등 환경별 설정
├── .clasp.staging.json
└── .claspignore
```

배포 ID는 비밀이 아니므로 환경별 설정 파일이나 저장소의 별도 파일에 두는 편이 낫다.
웹 앱 URL을 유지하려면 `update-deployment`에 이 ID가 필요한데, 이것을 사람의 기억이나 콘솔 조회에 의존하면 결국 새 배포를 만들어 URL을 깨뜨리게 된다.

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

### 생성과 복제

`create-script`는 새 프로젝트를 만든다. 타입을 지정하지 않으면 프롬프트로 묻는다.

```bash
clasp create-script --type standalone              # 기본. 독립 스크립트
clasp create-script --type sheets                  # 새 스프레드시트에 바운드
clasp create-script --type webapp
clasp create-script --type api
clasp create-script --title "My Script" --rootDir ./dist
clasp create-script --parentId "1D_Gxyv...NXO7o"   # 기존 문서에 바운드
```

`--parentId`가 지정되면 `--type`은 무시된다.
`--parentId`는 Google 문서·시트·폼·슬라이드의 Drive ID이며 URL의 `/d/{id}/edit`에서 얻는다.
지정하지 않으면 독립 스크립트가 만들어진다.

`clone-script`는 스크립트 ID나 URL을 받고, 버전 번호도 받는다.

```bash
clasp clone-script "15ImUCpyi1Jsd8yF8Z6wey_7cw793CymWTLxOqwMka3P1CzE5hQun6qiC"
clasp clone-script "https://script.google.com/d/15Im.../edit"
clasp clone-script "15Im..." --rootDir ./src
clasp clone-script "15Im..." 23                    # 특정 버전을 복제
```

버전 번호를 주면 그 시점의 코드를 가져온다. 사고 원인을 과거 버전과 비교할 때 쓴다.

### pull의 옵션이 중요한 이유

| 옵션                  | 동작                                                                       |
| --------------------- | -------------------------------------------------------------------------- |
| `--versionNumber <n>` | 특정 버전을 가져온다                                                       |
| `--deleteUnusedFiles` | push 대상이었을 로컬 파일 중 서버가 돌려주지 않은 것을 삭제. 확인을 묻는다 |
| `--force`             | `--deleteUnusedFiles`와 함께 써서 확인을 건너뛴다                          |

기본 `pull`은 로컬에만 있는 파일을 지우지 않는다.
그래서 기본 동작은 “덮어쓰기”이지 “동기화”가 아니며, 원격과 로컬을 정확히 같게 만들려면 `--deleteUnusedFiles`가 필요하다.
`--force`까지 붙이면 확인 없이 지우므로 저장소가 깨끗한 상태에서만 쓰는 것이 안전하다.

### 버전과 배포는 다른 개념이다

이 둘을 혼동하는 것이 Apps Script에서 가장 흔한 운영 실수다.

| 개념 | 명령                      | 성질                                                  |
| ---- | ------------------------- | ----------------------------------------------------- |
| 버전 | `clasp create-version`    | 코드의 **불변** 스냅숏. 번호가 붙는다                 |
| 배포 | `clasp create-deployment` | 특정 버전을 실행 가능한 형태로 노출. 배포 ID가 붙는다 |

```bash
clasp create-version "Bump the version."   # 현재 코드를 버전으로 고정
clasp list-versions

clasp create-deployment                    # 새 버전 + 새 배포
clasp create-deployment --versionNumber 4  # 기존 버전으로 새 배포
clasp update-deployment abcd1234 -V 7 -d "설명"
clasp list-deployments
clasp delete-deployment --all
```

웹 앱에서는 배포마다 고유 URL이 생긴다는 점이 결정적이다.
`create-deployment`를 반복하면 URL이 계속 바뀌고, 이미 배포한 URL을 쓰는 곳이 있다면 전부 깨진다.
기존 URL을 유지하면서 코드를 갱신하려면 `update-deployment <배포ID>`를 써야 한다.

그리고 `push`는 배포에 영향을 주지 않는다.
`push`가 바꾸는 것은 편집 중인 HEAD 상태이며 배포된 버전은 그대로다.
개발 중에 `push` 후 웹 앱을 열었는데 변경이 안 보이는 것은 대개 이 이유다.

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

## run-function 설정하기

`clasp run-function`은 설정이 가장 까다로운 명령이다. `docs/run.md`가 다섯 가지 선행 조건을 든다.

| 단계 | 내용                                                                                 |
| ---- | ------------------------------------------------------------------------------------ |
| 1    | `.clasp.json`에 `projectId` 설정                                                     |
| 2    | `Desktop Application` 타입 OAuth 클라이언트 ID 생성 후 `client_secret.json`으로 저장 |
| 3    | `clasp login --creds client_secret.json --user <key>`                                |
| 4    | `appsscript.json`에 `executionApi` 추가                                              |
| 5    | 프로젝트를 API Executable로 배포                                                     |

매니페스트에 넣을 항목은 이것이다.

```json
{
  "executionApi": {
    "access": "ANYONE"
  }
}
```

그리고 Apps Script 프로젝트와 GCP 프로젝트를 연결해야 한다.
`clasp open-script` 후 `프로젝트 설정 > Google Cloud Platform(GCP) 프로젝트`에서 프로젝트 **번호**를 넣는다.
`.clasp.json`에는 프로젝트 **ID**를, 웹 편집기에는 프로젝트 **번호**를 넣는다는 점을 혼동하기 쉽다.

스코프가 필요한 함수를 실행하려면 로그인 명령이 달라진다.

```bash
# appsscript.json 의 스코프 + clasp 기본 스코프를 한 프로필에 합친다
clasp login --user prod --use-project-scopes --include-clasp-scopes --creds client_secret.json

clasp push
clasp run-function --user prod sendMail
clasp run-function 'addOptions' -p '["string", 123, {"test": "for"}, true]'
```

`-p`는 JSON 문자열 배열이며 함수 인자로 전달된다.
`--nondev`를 붙이면 devMode가 아닌 상태, 즉 마지막으로 배포된 버전으로 실행된다. 붙이지 않으면 현재 HEAD 코드로 실행된다.
이 차이가 “로컬에서는 되는데 배포본에서는 안 된다”를 진단하는 가장 빠른 방법이다.

`Script API executable not published/deployed.` 오류가 나면 웹 편집기에서 `배포 > 새 배포 > 유형 API Executable`로 배포해야 한다.
이 단계는 아직 CLI로 되지 않으므로 GUI가 필요하다.

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

## Git을 진실 공급원으로 두기

`push`가 전체 교체라는 사실은, Git을 단일 진실 공급원으로 두면 대부분 무해해진다.
어차피 매번 전체를 올리는 것이고 되돌릴 근거는 원격이 아니라 저장소에 있다.
오히려 전체 교체가 더 단순하다. 원격 파일 상태가 항상 특정 커밋과 1:1로 대응하기 때문이다.

그래서 규율은 한 줄로 정리된다. 웹 편집기는 읽기 전용으로 취급한다.

```bash
# .gitignore
.clasprc.json
client_secret.json
node_modules/
build/
.clasp.json
```

`.clasp.json` 자체는 무시하고 `.clasp.prod.json` 같은 환경별 파일을 커밋하는 편이 깔끔하다. `scriptId`가 환경마다 다르기 때문이다.

Git이 못 보는 것이 하나 남는다. 웹 편집기에서 누군가 고친 변경이다.
그 변경은 저장소에 들어온 적이 없으므로 작업 트리는 깨끗하고 충돌도 diff도 없으며, `push` 시점에 조용히 덮인다.
도구가 막아 주지는 않지만 검사할 수는 있다.

```bash
#!/usr/bin/env bash
# scripts/clasp-drift-check.sh
# 원격이 저장소와 다른지 확인한다. push 전에 실행한다.
set -euo pipefail

project_file="${1:-.clasp.json}"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# 임시 디렉터리에서 원격 상태만 따로 받는다.
# rootDir 를 제거해 원격 파일이 임시 디렉터리 루트로 떨어지게 한다.
python3 - "$project_file" "$tmp/.clasp.json" <<'PY'
import json, sys
cfg = json.load(open(sys.argv[1]))
cfg.pop("rootDir", None)
json.dump(cfg, open(sys.argv[2], "w"))
PY

(cd "$tmp" && clasp pull --deleteUnusedFiles --force >/dev/null)

local_dir=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('rootDir','.'))" "$project_file")

if diff -ru --exclude='.clasp.json' "$tmp" "$local_dir"; then
  echo "원격과 로컬이 동일합니다."
else
  echo "경고: 원격에 저장소가 모르는 변경이 있습니다. push 하면 덮어씁니다." >&2
  exit 1
fi
```

이 스크립트를 `pre-push` 훅이나 배포 스크립트 앞에 두면 웹 편집기 편집이 사고가 아니라 경고가 된다.
완벽하지는 않다. `pull`이 파일만 가져오므로 트리거나 속성의 변경은 여전히 감지되지 않으며, 그쪽은 `exportMetadata` 덤프의 diff가 맡는다.

배포까지 포함한 전체 흐름은 이렇게 된다.

```bash
#!/usr/bin/env bash
# scripts/deploy.sh — 저장소의 현재 커밋을 지정 환경에 배포한다
set -euo pipefail

env="${1:?usage: deploy.sh <staging|prod>}"
project=".clasp.${env}.json"

# 커밋되지 않은 변경이 있으면 멈춘다. 배포는 커밋과 대응해야 한다.
git diff --quiet && git diff --cached --quiet || {
  echo "커밋되지 않은 변경이 있습니다." >&2; exit 1
}

./scripts/clasp-drift-check.sh "$project"

npm run build                                       # 번들러가 build/ 를 만든다
clasp push --project "$project" --user "$env" -f

# 버전 설명에 커밋 해시를 넣어야 나중에 역추적할 수 있다
clasp create-version --project "$project" --user "$env" \
  "$(git rev-parse --short HEAD) $(git log -1 --pretty=%s)"

# 웹 앱이라면 URL 유지를 위해 반드시 update-deployment 를 쓴다
if [[ -n "${DEPLOYMENT_ID:-}" ]]; then
  clasp update-deployment "$DEPLOYMENT_ID" --project "$project" --user "$env"
fi

# 서버 측 메타데이터 스냅숏을 갱신한다
clasp run-function exportMetadata --project "$project" --user "$env" \
  > "metadata/${env}.json"
```

CI에서 돌리려면 자격 증명을 비밀로 넣어야 한다.
공식 문서도 GitHub Actions 예제에서 `CLASPRC_JSON`과 `CLASP_JSON` 두 비밀을 쓴다.

```bash
gh secret set CLASPRC_JSON < ~/.clasprc.json
gh secret set CLASP_JSON < .clasp.prod.json
```

```yaml
# .github/workflows/deploy.yml 의 핵심 부분
- run: npm install -g @google/clasp
- run: printf '%s' "${{ secrets.CLASPRC_JSON }}" > ~/.clasprc.json
- run: printf '%s' "${{ secrets.CLASP_JSON }}" > .clasp.json
- run: npm run build && clasp push -f
```

이 방식의 한계는 아래 트레이드오프 절에서 다룬다. 서비스 계정을 쓸 수 없어 사람 계정의 토큰을 넣는 것이기 때문이다.

## 값 정하기

| 결정 항목               | 시작값                            | 근거                                                                |
| ----------------------- | --------------------------------- | ------------------------------------------------------------------- |
| `rootDir`               | `build/`                          | 번들러 출력과 push 대상을 일치시킨다. 소스와 산출물이 섞이지 않는다 |
| `.clasp.json` 커밋 여부 | 무시하고 환경별 파일을 커밋       | `scriptId`가 환경마다 다르다                                        |
| OAuth 클라이언트        | 개인은 기본, 조직은 자체 프로젝트 | 조직은 허용 목록 요청이 결재로 가고, 나중에 옮기면 재인증이 필요    |
| `--user` 프로필         | 환경마다 하나                     | 프로덕션 자격 증명으로 스테이징에 push하는 사고를 구조적으로 막는다 |
| 웹 편집기 정책          | 읽기 전용                         | `push`가 전체 교체이므로 양방향 편집은 반드시 손실을 만든다         |
| 배포 갱신 방식          | `update-deployment`               | `create-deployment`는 웹 앱 URL을 바꾼다                            |
| 버전 설명               | 커밋 해시 + 제목                  | Apps Script 버전 목록에서 커밋을 역추적할 수 있다                   |
| 트리거 관리             | 부트스트랩 함수 하나              | 트리거는 Git에 담기지 않으므로 생성 코드를 한곳에 모은다            |
| 비밀값                  | Script Properties + 주입 스크립트 | 저장소에 값이 들어가지 않으면서 주입 절차는 재현 가능해진다         |
| 메타데이터 스냅숏       | 배포 때마다 갱신                  | 서버 측 변경이 diff로 드러난다                                      |

`rootDir`를 빌드 출력으로 두는 결정이 나머지 여럿을 따라오게 만든다.
`.claspignore` 패턴의 기준이 되고, `filePushOrder`의 경로 기준이 되며, 소스 파일이 실수로 올라가는 것을 막는다.

## 트레이드오프

### 전체 교체는 Git으로 대부분 닫히고, 남는 것은 파일이 아닌 상태다

README가 경고 블록으로 명시한다.
Google의 scripts API가 원자적 연산도 파일 단위 연산도 지원하지 않으므로, `push`가 항상 온라인 프로젝트의 전체 내용을 교체한다는 것이다.

이 경고를 처음 읽으면 위험해 보이지만, Git을 진실 공급원으로 두면 실질적 위험이 거의 사라진다.
전체 교체는 “저장소의 이 커밋 = 원격의 현재 파일 상태”라는 단순한 대응을 만들어 주고, 부분 갱신이 만드는 어중간한 상태가 없다.
되돌리기도 `git checkout` 후 다시 `push`면 끝난다.

실제로 남는 위험은 둘이다.
하나는 Git이 자기가 못 본 변경을 경고해 주지 못한다는 것이다. 웹 편집기 편집은 저장소를 거치지 않으므로 충돌로 나타나지 않고 조용히 덮인다.
이것은 드리프트 검사 스크립트로 검출 가능하며, 도구가 아니라 규율과 자동화의 문제다.

다른 하나가 더 본질적이다. 프로젝트 상태의 상당 부분이 애초에 파일이 아니라는 것이다.
트리거, Properties, 배포본, 컨테이너 연결, 권한은 `push`로 올라가지도 `pull`로 내려오지도 않는다.
그래서 “저장소를 통째로 새 스크립트에 올리면 같은 것이 만들어진다”가 성립하지 않으며, 부트스트랩 함수와 메타데이터 덤프 같은 장치로 그 간극을 코드로 메워야 한다.

즉 이 절의 결론은 “전체 교체가 위험하다”가 아니라 “Git이 관리하는 경계가 프로젝트 경계보다 좁다”이다.
그 경계를 알고 나머지를 코드로 끌어들이는 것이 실무 설계의 핵심이며, 도구를 바꿔도 이 경계는 그대로다.

### TypeScript를 뺀 것은 더 나은 TypeScript를 위한 선택이지만 진입 비용을 올린다

3.x가 TypeScript 트랜스파일을 제거한 논리는 타당하다.
clasp가 내장한 변환기는 Apps Script가 이해하는 부분집합으로만 변환할 수 있었고, ESM 모듈이나 npm 패키지를 다룰 수 없었다.
Rollup 같은 번들러를 앞에 두면 그 제약이 사라진다.

대가는 설정 복잡도다.
2.x에서는 `.ts` 파일을 두고 `clasp push`만 하면 됐는데, 3.x에서는 번들러 설정, 빌드 스텝, `rootDir`를 빌드 출력으로 맞추는 작업이 추가된다.
README가 템플릿 저장소 넷을 나열하는 것 자체가 이 설정이 처음부터 쓰기에는 부담스럽다는 인정이다.

그리고 그리고 번들링에는 Apps Script 특유의 함정이 하나 더 있다.
트리거와 메뉴 핸들러는 전역 스코프에 이름으로 존재해야 하는데, 번들러는 기본적으로 모든 것을 감싸고 이름을 망가뜨린다.
그래서 진입점 함수들을 명시적으로 전역에 노출하는 코드가 필요하다.

```javascript
// 번들 후에도 트리거가 찾을 수 있도록 전역에 노출한다.
// 이 목록이 사실상 이 프로젝트의 공개 API 다.
globalThis.dailySync = dailySync;
globalThis.onFormSubmitHandler = onFormSubmitHandler;
globalThis.onOpen = onOpen;
```

이 변화가 clasp의 대상 사용자를 이동시킨다.
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

그러면 그 계정의 권한 전체가 CI에 노출되고, 계정 소유자가 퇴사하면 파이프라인이 멈춘다.
대안은 자동화 전용 Google 계정을 만드는 것인데, 조직 정책상 금지되는 경우가 많고 2단계 인증 관리도 별도 문제가 된다.

현실적인 타협은 CI가 빌드와 검증까지만 하고 배포는 사람이 로컬에서 실행하는 것이며, 그 배포 스크립트를 저장소에 두어 재현 가능하게 만드는 것이다.
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

`clasp pull`은 기본적으로 로컬 전용 파일을 지우지 않는다. 원격과 정확히 맞추려면 `--deleteUnusedFiles`가 필요하다.

트리거는 push로 따라오지 않는다. 새 환경에 코드를 올려도 자동 실행은 시작되지 않는다.

Script Properties도 따라오지 않는다. 새 환경에서는 필수 속성이 비어 있어 런타임에 실패한다.

`create-deployment`를 반복하면 웹 앱 URL이 매번 바뀐다. 기존 URL을 유지하려면 `update-deployment <배포ID>`다.

`push`만 하고 배포하지 않으면 배포된 웹 앱의 동작은 바뀌지 않는다. 버전 고정과 배포 갱신이 별도 단계다.

`PropertiesService.setProperties(values, true)`는 목록에 없는 기존 키를 전부 지운다. 주입 스크립트에서 두 번째 인자를 확인한다.

번들러를 쓰면 트리거 대상 함수가 전역에서 사라질 수 있다. `globalThis`에 명시적으로 노출해야 한다.

`run-function` 설정에서 `.clasp.json`에는 GCP 프로젝트 ID를, 웹 편집기에는 프로젝트 번호를 넣는다. 둘은 다른 값이다.

`clasp delete-script -f`는 확인 없이 스크립트를 지운다. README도 스크립트에서 clasp를 돌리는 경우가 아니면 좋은 생각이 아니라고 적는다.

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

웹 편집기 편집이 실제로 조용히 덮이는지 직접 재현해 보면 규율의 필요성이 체감된다.

```bash
# 1. 웹 편집기를 열어 hello.js 에 한 줄을 추가하고 저장한다
clasp open-script

# 2. 로컬은 건드리지 않은 상태로 상태를 본다. 아무 경고도 없다
clasp show-file-status

# 3. push 하면 웹에서 추가한 줄이 사라진다
clasp push && clasp pull && cat hello.js
```

드리프트 검사 스크립트를 넣으면 3번이 실패로 바뀐다.

```bash
./scripts/clasp-drift-check.sh && clasp push
```

파일이 아닌 상태는 따로 확인한다.

```bash
# 웹 편집기에서 트리거를 하나 추가한 뒤 덤프를 다시 뜬다
clasp run-function exportMetadata > /tmp/after.json
diff metadata/prod.json /tmp/after.json
```

차이가 나오면 그 트리거를 `bootstrapTriggers()`에 반영할지 지울지 결정한다.
차이가 안 나오면 덤프 함수가 그 종류의 상태를 보고 있지 않은 것이므로 덤프를 넓혀야 한다.

`.claspignore`를 고쳤을 때도 같은 방식으로 확인한다.

```bash
# 패턴을 고친 뒤 실제로 무엇이 제외되는지 본다
clasp show-file-status --json | python3 -m json.tool
```

`node_modules` 안의 파일이 목록에 보이면 패턴이 `.gitignore` 문법으로 쓰여 있는 것이다.

## 체크리스트

- Node 22 이상인가
- `https://script.google.com/home/usersettings`에서 Apps Script API를 켰는가
- 웹 편집기를 읽기 전용으로 취급하기로 팀이 합의했는가
- `push` 전에 드리프트를 검사하거나 최소한 `show-file-status`로 확인하는가
- 트리거 생성을 부트스트랩 함수 한곳에 모았는가
- 필수 Script Properties 목록을 코드에 선언하고 시작 시점에 검증하는가
- 속성 값 주입을 스크립트로 자동화했는가, 값이 저장소에 들어가지 않는가
- 메타데이터 스냅숏(`exportMetadata` 출력)을 저장소에 두고 배포마다 갱신하는가
- 배포 ID를 저장소나 환경별 설정에 기록했는가
- 웹 앱이라면 `update-deployment`로 갱신하고 있는가(URL 유지)
- 버전 설명에 커밋 해시를 넣고 있는가
- `.claspignore`의 디렉터리 패턴을 `**/dir/**` 형태로 썼는가
- `.claspignore` 패턴이 `rootDir` 기준이라는 것을 반영했는가
- `.clasprc.json`과 `client_secret.json`이 `.gitignore`에 있는가
- 환경이 여럿이면 `--project`로 설정 파일을, `--user`로 자격 증명을 분리했는가
- 조직 자산을 다룬다면 자체 GCP 프로젝트와 OAuth 클라이언트를 준비했는가
- 필요한 API 넷(`script`, `serviceusage`, `drive`, `logging`)을 켰는가
- CI 배포가 필요하다면 서비스 계정이 동작하지 않는다는 제약을 알고 대안을 정했는가
- TypeScript를 쓴다면 번들러 설정과 `rootDir`를 빌드 출력으로 맞췄는가
- 번들러를 쓴다면 트리거 대상 함수를 `globalThis`에 노출했는가
- `filePushOrder`가 필요한 전역 초기화 파일이 있는지 확인했는가
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

### README가 파일만 다룬다는 사실을 말하지 않는다

이 README에서 가장 큰 누락이다.
clasp를 쓰면 Apps Script 프로젝트를 로컬에서 개발하고 소스 관리에 넣을 수 있다고 첫 줄에서 말하는데, 실제로 소스 관리에 들어가는 것이 파일뿐이라는 사실은 어디에도 없다.

Google 공식 가이드 쪽에는 그 문장이 있다. 트리거와 문서·사용자 속성은 직접 관리하지 않는다는 진술이다.
그런데 대부분의 사용자가 먼저 읽는 것은 저장소 README이고, 두 문서 사이에 이 정보에 대한 상호 참조가 없다.

이 누락이 비싼 이유는 실패 시점이 늦기 때문이다.
개발 중에는 아무 문제가 없고, 새 환경에 배포하거나 재해 복구를 시도하는 순간에 드러난다.
“저장소에 다 있으니 괜찮다”고 믿고 있던 시점과 그것이 틀렸다는 것을 아는 시점 사이가 몇 달일 수 있다.

한 문단이면 될 일이었다. clasp가 관리하는 것은 프로젝트의 파일 집합이며 트리거와 속성과 배포 설정은 별도로 관리해야 한다는 문장이다.
그리고 그 별도 관리를 어떻게 하는지에 대한 권장 패턴이 어느 문서에도 없다는 점이 더 아쉽다.

### MCP 모드를 실험적이라고 하면서 설치 안내에서는 대등하게 제시한다

설치 절에서 Gemini CLI 확장과 Claude Code 플러그인이 npm 설치 바로 다음에 나온다.
Claude Code 쪽은 플러그인 설치를 권장으로 표시하기까지 한다.

그런데 명령 목록으로 내려가면 `clasp mcp`가 실험적이며 에이전트를 위한 제한된 도구 부분집합만 제공한다고 적혀 있다.
두 서술이 같은 문서에 있고 서로를 참조하지 않는다.

이 불일치가 실무에서 문제가 되는 이유는, 에이전트로 Apps Script를 다루려는 사람이 설치 절만 보고 결정하기 때문이다.
어떤 도구가 노출되는지, 어떤 작업이 CLI로만 가능한지를 알려면 문서를 더 내려가야 하며, 그 정보도 “제한된 부분집합”이라는 말 외에는 없다.

그리고 에이전트에게 `push` 권한을 준다는 것이 이 플랫폼에서 무엇을 뜻하는지도 다루지 않는다.
전체 교체이므로 에이전트의 잘못된 `push` 한 번이 원격 전체를 바꾸고, 트리거가 걸린 프로덕션 스크립트라면 그 즉시 실행된다.
Git처럼 되돌릴 수 있다고 해도 그 사이에 실행된 부작용은 되돌아오지 않는다.

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

### 버전 관리의 경계는 도구가 아니라 “무엇이 파일인가”가 정한다

clasp를 쓰면 Apps Script가 Git으로 관리된다고 말할 수 있다.
그 문장이 참인 범위는 정확히 파일로 표현되는 것까지다.

이 구분이 Apps Script만의 이야기가 아니다.
Kubernetes에서 매니페스트는 Git에 있지만 클러스터의 실제 상태는 아니고, Terraform에서 코드는 Git에 있지만 상태 파일과 수동 변경은 아니며, 데이터베이스에서 스키마 마이그레이션은 Git에 있지만 데이터는 아니다.
어느 경우든 “코드를 버전 관리한다”와 “시스템을 재현할 수 있다”는 다른 주장이다.

그래서 새 플랫폼을 코드로 관리하려 할 때 던져야 할 질문이 정해진다.
이 시스템의 상태 중 파일로 표현되는 것과 그렇지 않은 것을 나누어 적어 보는 것이다.
그 목록의 두 번째 열이 비어 있으면 운이 좋은 것이고, 비어 있지 않다면 그것을 코드로 끌어들일 방법을 따로 설계해야 한다.

끌어들이는 방법은 대개 둘이다. 상태를 만드는 **절차**를 코드로 쓰는 것과, 현재 상태의 **스냅숏**을 파일로 내보내는 것이다.
전자는 재현을 담당하고 후자는 검출을 담당하며, 둘 중 하나만으로는 부족하다.
절차만 있으면 서버가 언제 어긋났는지 모르고, 스냅숏만 있으면 어긋난 것을 되돌릴 방법이 없다.

### 조용한 덮어쓰기는 도구가 아니라 검사 절차로 막는다

Git이 웹 편집기 편집을 경고해 주지 못하는 이유는 단순하다. 그 변경이 Git을 거치지 않았기 때문이다.
어떤 버전 관리 도구도 자기가 관측하지 못한 변경에 대해서는 충돌을 낼 수 없다.

이 구조가 반복적으로 나타난다.
누군가 프로덕션 서버에 직접 접속해 설정 파일을 고치면 Ansible이 조용히 덮고, 콘솔에서 보안 그룹을 바꾸면 Terraform이 조용히 되돌린다.
공통점은 시스템에 쓰기 경로가 둘인데 한쪽만 이력을 남긴다는 것이다.

해법은 두 가지뿐이고 둘 다 도구 바깥에 있다.
하나는 두 번째 경로를 막는 것이다. 권한으로 웹 편집기 접근을 제한하거나 콘솔 쓰기 권한을 회수하는 것이다.
다른 하나는 적용 직전에 실제 상태를 읽어 기대 상태와 비교하는 것이다. Terraform의 plan, Kubernetes의 diff, 그리고 여기서는 `clasp pull` 후 비교다.

두 번째가 거의 항상 더 현실적이다. 첫 번째는 조직 정책 변경을 요구하고 예외 요청을 낳기 때문이다.
그리고 이 검사는 사람이 기억해야 하는 절차가 아니라 배포 스크립트의 한 줄이어야 한다.
기억에 의존하는 규율은 바쁜 날에 가장 먼저 무너지고, 조용한 덮어쓰기는 바쁜 날에 일어난다.

### 배포 단위를 코드 단위와 명시적으로 연결하지 않으면 추적이 끊긴다

Apps Script는 코드의 스냅숏(버전)과 실행되는 것(배포)을 분리한다.
그리고 그 둘 어디에도 커밋 해시가 자동으로 들어가지 않는다.

이 공백을 메우지 않으면 몇 달 뒤 “지금 프로덕션에 도는 게 어느 코드인가”에 답할 수 없다.
Apps Script 콘솔은 버전 7이라고 말해 주고 Git은 커밋 `a1b2c3`이 있다고 말해 주는데, 둘을 잇는 것이 아무것도 없다.

해법은 저렴하다. 버전을 만들 때 설명에 커밋 해시를 넣는 것이다.
`clasp create-version "$(git rev-parse --short HEAD) $(git log -1 --pretty=%s)"` 한 줄이면 된다.

이 원칙은 Apps Script 바깥에서도 같다.
Docker 이미지 태그에 커밋 해시를 넣고, 빌드 산출물에 버전 정보를 심고, 배포 이벤트에 리비전을 기록하는 것이 전부 같은 일이다.
런타임이 자기 출처를 말할 수 있어야 사고 조사가 성립하며, 그 연결은 배포 시점에 한 줄로 만드는 것이 나중에 역추적하는 것보다 압도적으로 싸다.

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
