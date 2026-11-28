# tidy

<https://tidy.lukeed.com/>

<https://github.com/lukeed/tidy>

GN 토론: <https://news.hada.io/topic?id=37927>

## 소개

tidy는 Luke Edwards가 Rust로 만든 코드 포매터다.
프로젝트는 “Prettier의 스타일을 네이티브 속도로” 출력한다고 소개한다.
단일 바이너리이고 Node에 위임하지 않으며, 원하면 쓸 수 있는 Node 바인딩이 따로
있다.

지원하는 언어와 기준 스타일은 다음과 같다.

| 언어                                                | 기준                     |
| --------------------------------------------------- | ------------------------ |
| JavaScript, TypeScript, JSX                         | Prettier                 |
| HTML, Vue, Handlebars, MJML                         | Prettier                 |
| CSS, SCSS, Less, JSON 계열, YAML, GraphQL, Markdown | Prettier                 |
| XML, SVG                                            | @prettier/plugin-xml     |
| TOML                                                | taplo                    |
| Dockerfile                                          | dprint-plugin-dockerfile |
| INI, .editorconfig, .npmrc, .gitconfig              | prettier-plugin-ini      |

설치는 `cargo binstall tidy`, `cargo add tidy`, `bun add tidyrs` 중 하나다.
명령은 `tidy check`로 서식이 맞지 않는 파일을 나열하고,
`tidy up`으로 제자리에서 고친다.
설정은 `tidy.json`, `tidy.jsonc`, `tidy.toml`과 `.editorconfig`에서 읽고,
`tidy init`은 Prettier나 oxfmt 설정이 있으면 옮겨 준다.

## 벤치마크와 일치율

README가 제시한 수치는 M1 Max에서 모든 코어를 쓰고 파일 전체를 검사한 평균이다.
JavaScript, TypeScript, JSON, CSS 등 XML을 뺀 12,071개 파일 전체는 tidy가 280ms,
bun fmt가 569ms, oxfmt가 1.2초, Prettier가 18.5초다.
JavaScript만 보면 3,906개 파일에서 tidy 78ms, bun fmt 100ms, oxfmt 123ms,
Prettier 8,528ms다.
Prettier와의 출력 일치율은 JavaScript 3,906개 전부,
TypeScript 3,309개 중 3,308개이며 JSDoc 서식을 끈 조건이다.

tidy는 의도적으로 Prettier와 다르게 출력하는 곳도 있다.
Prettier의 출력이 코드의 의미를 바꾸는 경우,
다음 실행에서 출력이 또 달라지는 경우,
JSDoc 주석을 기본으로 정리하는 선택이다.
JavaScript와 TypeScript에서는 Prettier가 다음에 다시 바꿀 출력 대신 안정된
지점의
출력을 내서 CI에서 `tidy check`가 초록으로 유지되게 한다.
각 차이는 `docs/deviations.md`에 예제와 함께 있다.

## 분석

### 속도 주장의 범위

비교 대상이 Prettier 한 종류가 아니라 bun fmt, oxfmt, dprint, Biome 등으로
넓어 보이지만,
표에서 가장 큰 차이는 Prettier와의 것이다.
Prettier를 쓰는 팀에는 18.5초와 280ms라는 숫자가 눈에 띄고,
이미 oxfmt나 bun fmt를 쓰는 팀에는 2배 안팎의 차이만 남는다.

### 차이를 관리하는 방식

`docs/deviations.md`는 tidy가 Prettier와 다르게 출력하는 모든 경우를 항목으로
관리한다.
기준은 Prettier 3.9.9이며 Markdown은 3.9.10, XML은 플러그인 3.4.2,
TOML은 taplo 0.14.0 등으로 도구별 버전이 명시된다.
차이는 조용히 배포하지 않고 `proposed` 상태로 항목을 추가한 뒤 저자의 승인을
받아 `approved`와 날짜를 남기는 절차를 밟는다.
유지하는 기준은 Prettier의 출력이 코드의 뜻을 바꾸거나 다시 포맷하면 또 바뀌는
경우로 한정하고, 단순한 배치 차이는 Prettier를 따른다.
검사한 입력은 `tests/deviations.json`에 모여 있고
`cargo test --test deviations`가 항목과 실제 출력의 일치를 검사한다.
Handlebars, CSS, HTML, XML, TOML, Dockerfile, INI, GraphQL, JavaScript 등
언어별 항목이 나뉘어 있으며 대부분은 bun의 Rust 포팅이 바로잡은 부분에서 왔다고
적혀 있다.

### 일치율이라는 기준

Prettier 호환을 목표로 한 포매터에서 일치율은 도입 비용을 좌우한다.
JavaScript 100%, TypeScript 3,308/3,309라는 수치는 프로젝트가 고른 말뭉치에서의
것이고, JSDoc 서식을 끈 조건이 붙어 있다.
기본 설정에서는 JSDoc까지 정리하므로 처음 `tidy up`을 돌릴 때 Prettier와 다른
diff가 생길 수 있다.
도입하려는 팀은 자신의 저장소에서 `tidy check`를 돌려 비교하는 것이 확실하다.

## 비평

### 성숙도에 대한 의문

저장소의 별은 175개, 커밋은 478개이며 설치 스크립트 예시의 버전이 v0.1.0이다.
이는 공개 초기 단계임을 시사한다.
README는 `docs/deviations.md`로 차이를 공개하고 있지만,
말뭉치 밖의 코드에서 어떤 차이가 나는지는 사용자가 확인해야 한다.

### 설치 방식

`curl -fsSL https://tidy.lukeed.com`로 받아 셸에서 실행하는 설치 스크립트가
제공된다.
스크립트 첫머리는 실행 전에 읽어 보라고 안내하고,
받은 체크섬이 같은 호스트에서 제공되어 변조가 아니라 불완전한 다운로드만
잡는다고
스스로 밝힌다.
서명된 매니페스트가 필요하면 packslip이나 mise로 설치하라고 안내한다.
macOS에는 HTML Tidy가 `/usr/bin/tidy`로 있어서 PATH 순서가 다르면 엉뚱한
프로그램이 실행된다는 경고도 있다.

## 인사이트

### 포매터를 바꾸는 비용

속도가 빨라져도 팀이 포매터를 바꾸는 일은 diff 한 번의 비용이 든다.
tidy는 설정 이전 기능과 Prettier 일치율 공개로 이 비용을 낮추려 한다.
도입은 전체 교체보다 `tidy check`를 CI의 비교 단계에 먼저 붙여 보는 쪽이
작게 시작할 수 있다.
