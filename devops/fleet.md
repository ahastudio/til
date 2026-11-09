# Fleet: osquery 위에 MDM을 얹은 오픈코어 장치 관리 플랫폼

<https://fleetdm.com/>

<https://github.com/fleetdm/fleet>

HN 토론: <https://news.ycombinator.com/item?id=28793778> (4점, 0개 댓글)

## 소개

Fleet는 수천 대 규모의 컴퓨터를 가진 IT·보안 팀을 위한 오픈소스 플랫폼이다.
회사는 API, GitOps, 웹훅(webhook), YAML을 전제로 설계했다고 말하고,
한 시스템으로 모든 기기를 무선(over the air)으로 보호하고 유지한다고 소개한다.
MDM, 패치, 소프트웨어 배포, 상태 검증을 한곳에서 하고,
조직이 쓰는 모든 운영체제를 한꺼번에 다룬다는 것이 핵심 주장이다.
Fleet는 osquery, nanoMDM, Nudge, swiftDialog 위에 만들어졌다고 밝힌다.

이 문서는 세 층을 겹쳐 읽는다.
회사가 말하는 내용, 회사의 문서와 가격표가 적은 조건, 그리고
저장소를 내려받아 읽은 코드다.
코드는 읽기만 했고 실행하지 않았다.

2026-11-09에 읽은 저장소 수치는 다음과 같다.
스타(star) 7,162개, 포크 1,128개, 열린 이슈 3,771건, 열린 풀 리퀘스트 400건이다.
GitHub의 `open_issues_count`는 4,171인데, 이슈와 풀 리퀘스트를 합친 값이다.
저장소는 2020-11-03에 만들어졌고, 읽은 날에도 푸시가 있었다.
익명을 포함한 기여자는 551명이다.

### 제품 범위가 넓어지는 방향

Fleet는 자신을 모든 운영체제를 위한 열린 MDM, 패치, 취약점 관리라고 소개한다.
최근의 문구는 모든 운영체제를 위한 AI 기기 관리, 패치,
활성화(enablement)를 하나의 에이전트로 한다는 쪽으로 옮겨 갔다.
순환하는 홍보 문구에는 그림자 AI·그림자 IT, MCP와 IDE 확장, 브라우저 플러그인,
로컬 에이전트 세션이 들어 있다.
기기 관리에 더해 기기에서 돌아가는 AI 도구의 가시성까지 제품 범위로 보겠다는
뜻이다.

### 회사가 말하는 규모

Fleet는 수천 대를 관리하는 IT·보안 팀이 실제로 운영한다고 말한다.
많은 배포가 수만 대 호스트를 지원하고,
일부 대형 조직은 40만 대 이상을 관리한다고 한다.
같은 문장이 Fleet 문서의 소개에도 그대로 있다.[^why]
이보다 큰 합계로는 1,300곳 이상의 조직, 90개국 이상,
컴퓨팅 기기 200만 대 이상을 내세우고, 지원 응답 시간은 평균 21분이라고 한다.
고객 인용으로는 Stripe의 클라이언트 플랫폼 엔지니어가 Mac 1만 대를 Fleet로
옮겼다고 말한 문장을 싣는다.
40만 대는 가장 큰 단일 조직의 규모 주장이고,
200만 대는 전체 고객의 합계 주장이다.
어느 쪽에도 고객 이름, 배포 구성, 집계 기준이 없다.

### 지원 플랫폼

회사가 나열하는 대상은 다음과 같다.

- Linux(모든 배포판), macOS, Windows, Chromebook
- iOS와 Android(개인 소유 BYOD 또는 회사 소유)
- AWS, Google Cloud(GCP), Azure
- 데이터센터, 컨테이너(Kubernetes 등), Linux 기반 IoT 기기

가격표는 MDM 지원 대상을 Apple, Windows(amd64와 Arm), Linux(amd64와 Arm), iOS,
iPadOS, Android, ChromeOS로 적는다.[^pricing]
회사의 목록은 기기 종류와 클라우드·컨테이너 환경을 한 줄에 섞어 놓는다.
MDM으로 관리하는 것과 에이전트로 상태만 읽는 것은 다른 일이므로,
어느 대상이 어느 쪽인지는 이 목록만으로 알 수 없다.

## 코드를 열어 본 결과

### 저장소의 구성과 규모

저장소를 얕게 복제해 Go 소스의 줄 수를 쟀다.

| 디렉터리    | 역할                                   | 구현 줄 수(Go) | 시험 줄 수(Go)    |
| ----------- | -------------------------------------- | -------------- | ----------------- |
| `server`    | 서버 본체, MDM, 취약점, 라이브 쿼리 등 | 373,777        | 571,543           |
| `ee/server` | 유료(source-available) 기능            | 36,435         | 49,766(`ee` 전체) |
| `orbit`     | 기기에 설치되는 에이전트(fleetd)       | 58,183         | 33,240            |
| `cmd`       | `fleet` 서버와 `fleetctl` 진입점       | 39,892         | 54,324            |
| `pkg`       | 공용 라이브러리                        | 16,425         | 16,682            |

프런트엔드 TypeScript(시험 제외)는 224,773줄이다.
Go 파일은 모두 3,297개이고 그중 시험 파일이 1,261개다.
`server`에서 시험 코드가 구현 코드의 1.5배 정도여서 시험에 투자가 큰 저장소다.
`ee/server`는 `server`와 `ee/server`를 합친 410,212줄의 8.9%다.

저장소에는 코드 말고도 `handbook`(회사 핸드북), `it-and-security`,
`infrastructure`, `terraform`, `charts`, `website`, `proposals`,
`openspec` 같은 디렉터리가 같이 있다.
회사 핸드북을 저장소에 둔다는 말이 문자 그대로다.
루트의 `CHANGELOG.md`는 8,339줄이고,
아직 릴리스에 묶이지 않은 변경 기록이 `changes/`에 201개 쌓여 있다.

### 무료판과 프리미엄이 한 코드 안에서 나뉘는 방식

`ee/server/service`의 주석은 이 서비스가 무료 서비스를 감싸고
그 위에 프리미엄 기능을 구현한다고 적는다.[^repo-ee-service]
구조는 데코레이터다.
프리미엄 서비스는 무료 `fleet.Service`를 내장하고,
같은 인터페이스의 메서드를 덮어써서 유료 동작을 더한다.[^repo-ee-service]
무료 쪽 코드는 유료 기능이 필요한 경로에서 `ErrMissingLicense`를 돌려주고,
이 오류를 쓰는 서버 파일이 69개다.

라이선스는 서명된 토큰이다.
`ee/server/licensing`은 ES256으로 서명된 JWT를 바이너리에 내장된 공개키로
검증하고, 키가 없으면 무료 등급으로 처리한다.[^repo-licensing]
토큰에는 등급, 조직 이름, 허용 기기 수, 만료일, 추가 조건 메모,
텔레메트리 끄기 허용 여부가 담긴다.[^repo-app]
등급은 무료와 프리미엄, 시험판이다.[^repo-app]
만료되었다는 오류만 있으면 토큰을 유효로 처리하고, 서버는 만료 경고
배너를 출력하고 응답 헤더에 만료를 표시한다.[^repo-licensing][^repo-handler]
이 설계에서 만료는 기능 차단이 아니라 경고다.

텔레메트리를 끌 수 있는지도 라이선스가 정한다.
코드는 무료 사용자에게는 끄기를 허용하고,
프리미엄 사용자는 라이선스에 허용 표시가 있을 때만 끌 수 있다고
정의한다.[^repo-app]
수집 범위의 세부는 이 문서에서 읽지 않았다.

### 에이전트 fleetd(Orbit)

`orbit`은 기기에 설치되는 에이전트이고 Go로 58,183줄이다.
하위 패키지 이름이 하는 일을 그대로 보여 준다.
`bitlocker`, `luks`, `lvm`은 디스크 암호화를, `swiftdialog`, `zenity`,
`kdialog`, `toast`는 운영체제별 사용자 알림 창을, `osquery`, `update`,
`profiles`, `setup_experience`, `managedaccount`는 osquery 실행, 업데이트,
프로파일, 초기 설정 경험, 관리 계정을 맡는다.[^repo-orbit]
플랫폼별 빌드 설정(goreleaser)이 Linux, macOS,
Windows와 각각의 Arm에 있다.[^repo-orbit]
이 에이전트는 서버와 달리 MIT 라이선스 파일을 따로 가진다.[^repo-orbit-license]
서버 쪽에서는 `server/mdm` 아래에 `nanomdm`과 `nanodep`이 서버 코드로 들어와
있어서, 회사가 밝힌 바탕 프로젝트가 코드에서도 확인된다.[^repo-mdm]

### 서버 안의 MCP 서버

Fleet 서버 안에 `server/fleetmcp`라는 MCP 서버가 들어 있다.[^repo-mcp]
도구는 열아홉 개로, 기기 목록과 상세(`get_endpoints`, `get_host`),
정책과 준수 여부(`get_policies`, `get_policy_compliance`),
소프트웨어와 취약점(`get_software`, `get_vulnerability_hosts`), osquery 스키마,
라이브 쿼리(`prepare_live_query`, `run_live_query`)를 다룬다.[^repo-mcp]
인증은 고정 토큰의 Bearer 헤더를 상수 시간 비교로 확인한다.[^repo-mcp-auth]
`vetted_queries.go`는 CIS 벤치마크에서
글자 그대로 옮긴 정책 쿼리만 담는다는 규칙을 주석으로
명시한다.[^repo-mcp-vetted]
서버 지시문은 라이브 쿼리를 실행하기 전에 운영자에게 정확한 SQL과 대상 범위를
보여 주고 명시적 확인을 기다리며, 자동 승인은 하지 않는다고
에이전트에게 지시한다.[^repo-mcp-server]
라이브 쿼리는 호스트에서 임의 SQL을 실행하는 기능이므로,
이 확인 절차가 지시문에만 있는지 코드로도 강제되는지는 이 문서가 확인하지
못했다.

### AI 에이전트로 일하는 저장소

루트의 `AGENTS.md`는 이 저장소에서
일하는 AI 코딩 에이전트에게 풀 리퀘스트 설명에 `## AI` 섹션을 넣고
쓴 도구와 정확한 모델 ID를 적으라고 요구한다.[^repo-agents]
`.claude`, `.coderabbit.yaml`, `.pr_agent.toml`이 저장소에 있다.
이 프로젝트의 개발 자체가 AI 에이전트의 기여를 전제로 짜여 있다는 뜻이다.

## 기능과 접근 방식

### 관리 표면: GitOps, 명령줄, API, AI

Fleet는 GitOps로 관리하거나, GUI, REST API, 웹훅 이벤트,
`fleetctl` 명령줄 도구로 관리할 수 있다고 말한다.
Fleet 문서는 여기에 MCP 서버를 더하고 선호하는 AI 도구로 기기를 다스릴 수 있다고
소개한다.[^why]
가격표에서 GitOps, 명령줄 도구, REST API, 웹훅,
SSO는 무료판에도 들어 있다.[^pricing]
기기 관리 설정을 코드로 다루는 길이 유료 기능 뒤에 있지 않다는 뜻이다.

변경 절차는 세 단계로 소개된다.
관리자가 이미 쓰는 AI에 설정 변경이나 CVE 수정을 자연어로 설명해 제안하게 하고,
팀원이나 봇이 올린 변경을 사람이 검토해 승인하며, 병합하면
Fleet가 기기 전체에 적용하고 필요하면 즉시 되돌린다.
GitOps 위에 AI 제안 단계를 얹은 흐름으로 읽힌다.

### 가시성과 규정 준수

Fleet는 기기에서 수백 가지 속성을 보고할 수 있고,
macOS와 Windows용 CIS 벤치마크를 함께 제공한다고 말한다.
운영체제, 하드웨어, 소프트웨어 데이터는 table 참조 문서에서
항목을 확인할 수 있다.
Fleet 문서는 Fleet가 osquery 생성에 참여했고 계속 개선하겠다고 밝힌다.[^why]
가격표에서 정책(policy), 보고서, 파일 무결성 모니터링(FIM),
파일 수집(file carving), YARA 기반 악성코드 탐지는 무료판에 있다.[^pricing]

### 연동

회사가 꼽는 연동 대상은 Snowflake, Splunk, GitHub Actions, Vanta, Elastic, Jira,
Zendesk 등이다.
Munki, Chef, Puppet, Ansible, CrowdStrike, SentinelOne과도 함께 쓸 수 있다고
한다.
Fleet를 보안 제품이나 구성 관리 도구의 대체재가 아니라 이웃으로 놓겠다는 태도다.

### 수집 범위의 투명성

Fleet는 키 입력, 이메일, 웹캠 같은 사생활은 수집하지 않고
기기 관리와 보안에 필요한 데이터만 모은다고 말한다.
최종 사용자가 에이전트의 동작을 직접 확인할 수 있다는 점을 근거로 든다.
Fleet 문서는 수집 대상으로 사용자 계정, 기기 상태, 설치된 소프트웨어,
보안 설정을 예로 든다.[^why]
이 범위가 바뀌면 사용자에게 보이는가는 회사 설명에도 문서에도 적혀 있지 않다.

### 경쟁 제품 비교

Fleet는 Intune, Jamf Pro, Workspace ONE, Ivanti, PatchMyPC를 고르면
Fleet와 항목별로 비교하는 표를 보여 준다.
항목은 기기 인벤토리, 소프트웨어 업데이트, 구성·스크립팅·진단, 기기 보고
속도(30초 미만), API, 코드로서의 인프라, 배포 방식이다.
경쟁 제품 쪽 칸에는 모바일 미지원, Apple 전용, Windows 중심, 보고 6시간,
일회성 스크립트, 클라우드 전용 같은 표현이 들어간다.
어느 칸이 어느 제품의 것인지는 선택기에 따라 바뀌어서 짝을 확정할 수 없다.

## 라이선스 구조

Fleet는 무료판이 MIT 라이선스이고,
상용 라이선스는 유료 기능에 기여하려는 사람도 받아들이도록 설계했다고 적는다.
GitHub는 이 저장소의 라이선스를 `NOASSERTION`, 곧 판별하지 못한 것으로 표시한다.
이유는 `LICENSE` 파일이 디렉터리별로 라이선스를 나누기 때문이다.[^license]

- `docs/` 아래 문서는 CC BY-SA 4.0이다.
- `ee/` 아래는 `ee/LICENSE`를 따른다.
- 클라이언트 쪽 JavaScript는 MIT Expat이다.
- 그 밖의 내용은 MIT Expat이다.

`ee/LICENSE`는 운영 환경에서 쓰려면 Fleet 구독 약관에 동의하고
호스트 수에 맞는 구독을 가져야 한다고 적는다.
개발과 테스트 목적의 복사와 수정은 구독 없이 허용한다.
복사, 병합, 게시, 배포, 재라이선스, 판매는 금지한다.[^eelicense]
Fleet 핸드북은 유료 기능도 소스는 공개(source-available)이고,
회사는 오픈코어(open-core) 모델 위에 있다고 말한다.[^opensrc]

## 가격과 무료·유료 구분

Fleet는 세 단계를 둔다.
무료(Free)는 호스트당 월 0달러, 프리미엄(Premium)은 호스트당 월 7.00달러,
커스텀(Custom)은 대규모 배포용으로 영업팀과 상담한다.[^pricing]
환율은 1달러에 1,361.4원이다.[^fx]
프리미엄 7달러는 약 9,530원이다.
100대를 쓰면 월 700달러(약 952,980원)이고 연 8,400달러(약 11,435,760원)다.
1,000대를 쓰면 월 7,000달러(약 9,529,800원)다.
이 계산은 가격표의 정가만 곱한 값이고,
대량 할인이나 계약 조건은 확인하지 못했다.

가격표의 기능 표에서 무료와 프리미엄을 가르는 항목을 골라 정리하면
다음과 같다.[^pricing]

| 기능                                 | 무료 | 프리미엄 |
| ------------------------------------ | ---- | -------- |
| 다중 플랫폼 MDM 지원                 | 포함 | 포함     |
| BYOD 등록                            | 포함 | 포함     |
| OS 설정 강제                         | 포함 | 포함     |
| 스크립트 실행                        | 포함 | 포함     |
| 정책, 보고서, FIM, YARA 탐지         | 포함 | 포함     |
| GitOps, 명령줄, REST API, 웹훅, SSO  | 포함 | 포함     |
| 자체 호스팅                          | 포함 | 포함     |
| 제로터치 설정                        | 없음 | 포함     |
| 다른 MDM에서 이전                    | 없음 | 포함     |
| 디스크 암호화 강제                   | 없음 | 포함     |
| OS 업데이트 강제                     | 없음 | 포함     |
| 애플리케이션 배포와 셀프 서비스 설치 | 없음 | 포함     |
| 잠금과 초기화 명령                   | 없음 | 포함     |
| 취약점 점수, CISA KEV                | 없음 | 포함     |
| 역할 기반 접근 제어, 감사 로그       | 없음 | 포함     |
| 관리형 클라우드                      | 없음 | 포함     |

관리형 클라우드는 현재 호스트 700대 이상인 고객에게만 제공한다는 주석이 붙어
있다.[^pricing]
Fleet는 회사가 호스팅해 주거나 직접 배포할 수 있고 어느 쪽이든 같은 경험이라고
말하는데, 작은 팀에게 같은 경험으로 고를 수 있는 것은 자체 배포뿐이다.

## 개발 속도

GitHub 릴리스 목록에서 가장 최근 8개는 2026-10-04부터 2026-10-28 사이에 나왔다.
2026-10-04 하루에 4.89.3, 4.90.3, 4.91.2, 4.92.3이 함께 나왔고, 이어서
4.93.0(10월 8일), 4.93.1(10월 20일), 4.93.2(10월 21일),
4.94.0(10월 28일)이 나왔다.[^releases]
같은 날 네 개 마이너 버전에 패치가 나갔다는 것은 여러 버전 줄을 동시에
유지보수한다는 뜻으로 읽힌다.
이 해석은 릴리스 이름만 보고 한 추정이다.

4.94.0 릴리스 노트는 구성 프로파일(configuration profile)에 이름과 설명 필드를
더하고, 프로파일 추가·편집 화면을 모달에서 별도 페이지로 바꿨다고 적는다.
Windows용 최종 사용자 계약(EULA)을 올려 Microsoft Entra와 Autopilot 등록 때 약관
화면으로 보여 주는 기능도 들어갔다.
BYOD Android 기기의 초기화(wipe)는 무료와 프리미엄 모두에서
API와 `fleetctl`로 쓸 수 있게 됐고, 이때는 업무 프로필만 지워진다.[^rel-494]

## 분석

### 하나의 저장소에 두 제품이 들어 있다

Fleet의 뿌리는 osquery 기반의 가시성이다.
osquery는 SQL로 운영체제를 계측하고 감시하고 분석하는 프레임워크이며, Linux,
macOS, Windows에서 쓸 수 있다.[^osquery]
함께 거명되는 나머지 셋은 성격이 다르다.
nanoMDM은 Apple MDM 서버와 라이브러리이고,[^nanomdm] Nudge는 macOS 보안 업데이트
설치를 독려하는 도구이며,[^nudge] swiftDialog는 macOS에 사용자 알림을 만드는
도구다.[^swiftdialog]
코드에서도 이 구성이 보인다.
서버에는 `nanomdm`과 `nanodep`이,
에이전트에는 `swiftdialog` 패키지가 있다.[^repo-mdm][^repo-orbit]
Fleet는 가시성 도구에 MDM을 붙여 한 제품으로 묶었다.

회사는 Fleet가 가볍고 모듈식이어서 MDM만 쓰고 보안은 쓰지 않을 수도,
그 반대도 가능하며 쓰지 않는 기능은 끌 수 있다고 한다.
묶음 제품이면서 분리해 쓸 수 있다는 주장이다.
이 주장이 얼마나 성립하는지는 기능을 끄고 켜 보지 않고서는 판단할 수 없다.

### 설정을 코드로 둔다는 전제

Fleet는 첫 문장에서 API, GitOps, YAML을 앞세운다.
관리자는 설정을 YAML 파일로 저장소에 두고
`fleetctl`이 그 상태를 Fleet 서버에 반영한다.
MDM 설정은 보통 관리 콘솔의 화면에서 조작하는 상태로 존재한다.
Fleet는 그 상태를 코드 리뷰와 변경 이력이 닿는 곳으로 옮기려 한다.

4.94.0 릴리스 노트가 이 방향을 보여 준다.
구성 프로파일의 `name`과 `description`은 화면, API, GitOps YAML에서
모두 지정할 수 있다.[^rel-494]
이름 변경은 원칙적으로 기기에 프로파일을 다시 보내지 않는다.
다만 Windows, Android, DDM 프로파일의 이름을 GitOps로 바꾸면
프로파일이 다시 만들어진다.[^rel-494]
YAML 한 줄의 수정이 기기에 미치는 영향이 대상 종류에 따라 다르다.

### 오픈코어가 무료판에 허용하는 일

가격표에서 무료판은 정보를 읽고 정책을 평가하고 스크립트를 실행하고
OS 설정을 강제하는 쪽을 대부분 갖는다.
유료판은 기기 상태를 바꾸는 쪽, 곧 디스크 암호화 강제, OS 업데이트 강제,
앱 배포, 잠금과 초기화, 제로터치 등록을 가진다.[^pricing]
조직 운영에 필요한 접근 제어(RBAC)와 감사 로그, 취약점 점수도 유료다.

이 선은 코드의 구조와 같은 방향이다.
유료 기능은 `ee/server`에 모여 있고
무료 서비스를 감싸는 한 겹으로 구현되어 있어서,
라이선스 토큰의 유무가 어느 겹을 활성화할지를 정한다.
회사는 사업 모델이 GitLab에서 영향을 받았다고 적는데 이 구조와 같은 방향이다.
무료판은 작은 팀이 가시성과 정책 평가를 써 보고,
기기에 변경을 가하는 기능을 쓰는 단계에서 구독으로 넘어가도록 되어 있다.

## 비평

### 소개 문장은 무료판이 무엇을 못 하는지 말하지 않는다

Fleet는 MDM, 패치, 소프트웨어 배포, 검증을 한 시스템에서 한다고 말한다.
같은 문장이 무료판에도 해당하는지는 적혀 있지 않다.
가격표에서 앱 배포, OS 업데이트 강제, 디스크 암호화 강제,
제로터치 설정은 프리미엄에만 있다.[^pricing]
패치와 소프트웨어 배포를 기대하는 독자가 소개만 읽고 무료판을 설치하면,
핵심 기능 몇 가지를 쓸 수 없다는 사실을 설치 뒤에 알게 된다.

Fleet는 무료판이 항상 무료일 것이라고 말하고 가격 안내로 연결한다.
이는 무료로 제공하는 범위가 어디까지인지 설명하지 않고
무료라는 사실만 강조하는 구성이다.
소개 문장 바로 아래에 무료판의 범위 한 줄이 있었다면 오해를 줄였을 것이다.

### 무료와 유료의 구분은 릴리스마다 움직인다

4.94.0 노트에서 BYOD Android 초기화는 무료와 프리미엄 모두에 들어갔다.[^rel-494]
같은 가격표에서 잠금과 초기화 명령은 프리미엄 전용으로 표시된다.[^pricing]
두 문장은 모순이 아닐 수 있다.
표는 기능군을 묶어 요약하고 노트는 기능 하나를 설명하기 때문이다.
그러나 표만 읽는 독자는 무료판에서 초기화가 안 된다고 결론짓게 된다.

이 사례가 보이는 문제는 구분의 출처가 하나가 아니라는 점이다.
가격표, 릴리스 노트, 문서가 각각 구분을 말하고 갱신 시점도 다르다.
도입하는 쪽은 쓸 기능 하나하나를 자신이 쓸 버전의 문서에서 확인해야 한다.
코드의 `ErrMissingLicense` 69개 파일도 어느 기능이 막히는지 확인하는 마지막
근거가 된다.

### 규모 수치는 어느 것도 검증할 수 없다

가장 큰 규모를 말하는 문장에는 근거가 없다.
40만 대는 고객 이름이 없고, 단일 서버 구성인지 여러 인스턴스 합계인지도 알 수
없다.
회사의 소개와 문서가 같은 문장을 되풀이하므로 서로 근거가 되지도 못한다.
1,300곳, 200만 대도 집계 기준이 없고
어느 시점의 등록 대수인지 활성 대수인지 알 수 없다.
이 숫자들은 마케팅 문장으로 읽어야 하며 용량 계획에 쓰면 안 된다.

열린 이슈 3,771건도 이 숫자만으로 프로젝트의 건강을 판단할 수 없다.
이슈가 많다는 것은 사용자가 많다는 신호일 수도,
처리 속도가 따라가지 못한다는 신호일 수도 있다.
닫힌 이슈의 처리 시간이나 라벨별 분포를 보지 않았으므로 어느 쪽인지는 모른다.

### 소스가 공개된다는 말과 검증할 수 있다는 말은 다르다

Fleet는 최종 사용자가 에이전트의 동작을 직접 확인할 수 있다고 말한다.
에이전트(`orbit`)는 MIT 라이선스 파일을 따로 갖고 있어서
이 말이 가장 성립하는 부분이다.[^repo-orbit-license]
반면 `ee/` 아래 코드는 소스가 공개되어 있지만 운영 환경 사용에 구독이 필요하고
복사·배포가 금지된다.[^eelicense]
읽는 것은 자유롭고 고쳐서 배포하는 것은 자유롭지 않다.
서버의 텔레메트리 수집 범위가 `ee/`와 무료 코드 어디에 구현되어 있는지는 이
문서가 확인하지 못했다.

### 라이브 쿼리 MCP는 사람의 확인에 기대고 있다

서버에 들어 있는 MCP 서버는 라이브 쿼리를 에이전트에게 노출한다.
지시문은 실행 전 SQL과 대상 범위를 운영자에게 보이고 확인을 받으라고 적지만,
이것은 에이전트에게 주는 문장이다.[^repo-mcp-server]
인증은 하나의 고정 토큰이다.[^repo-mcp-auth]
토큰이 새면 호스트 전체에 임의 SQL을 실행하는 길이 열린다는 점에서,
이 기능을 켜기 전에 토큰 보관과 대상 범위 제한(fleet 단위)을 점검해야 한다.
이 위험은 코드에서 읽은 구조로 추론한 것이고 실제 악용 사례는 확인하지 못했다.

### 비교표와 호스팅 문장은 가격표와 함께 읽어야 한다

비교표는 Fleet가 직접 만든 것이고 비교 기준과 측정 조건이 적혀 있지 않다.
기기 보고 속도 30초 미만이 어떤 규모와 어떤 쿼리에서 잰 값인지 알 수 없다.
경쟁 제품 칸의 표현도 각 제품의 어느 버전과 어느 요금제를 기준으로 했는지 없다.
이 표는 후보를 좁히는 출발점으로는 쓸 수 있지만,
경쟁 제품의 기능 판정은 각 제품의 문서에서 따로 확인해야 한다.

## 인사이트

### 도입 판단은 무료판으로 되는지가 아니라 어느 기능이 필요한지에서 시작한다

Fleet는 가시성 도구로는 무료로 많은 것을 준다.
기기를 바꾸는 기능은 구독 뒤에 있다.
결과적으로 무료판은 osquery식 질의와 정책 평가 도구로 쓰기 좋고,
MDM 대체재로 쓰기에는 부족하다.
기능 표를 읽는 순서를 바꾸면 도입 판단이 쉬워진다.
쓰려는 기능 목록을 먼저 만들고, 각 기능이 무료인지 프리미엄인지 표시하는 것이다.

프리미엄이 필요하다면 비용 구조도 달라진다.
호스트당 월 7달러(약 9,530원)는 100대에서 월 약 952,980원이다.
같은 비용으로 다른 MDM을 쓰는 경우와 비교하려면
그쪽의 정가와 지원 범위를 같은 기준으로 놓아야 한다.
이 문서는 경쟁 제품의 가격을 확인하지 않았다.

### 라이선스가 코드 구조 안에 있어서 켜고 끄는 비용이 낮다

유료 기능이 무료 서비스를 감싸는 한 겹이라는 구조는 구독을 시작하고
멈추는 비용이 낮다는 뜻이기도 하다.
토큰만 바꾸면 같은 바이너리에서 기능이 켜지고, 만료는 차단이 아니라 경고다.
도입하는 쪽에는 시범 운영이 쉽다는 장점이 있지만,
만료 뒤에도 돌아간다는 사실을 조직이 구독 없이 쓴다는 허락으로 읽으면 안 된다.
`ee/LICENSE`는 운영 환경 사용에 구독을 요구한다.[^eelicense]

### 설정을 코드로 둔 조직에서는 변경 검토가 핵심 기능이 된다

GitOps가 무료판에도 있다는 점은 작은 팀에게도 의미가 있다.
기기 설정의 변경 이력이 저장소에 남고 풀 리퀘스트로 검토할 수 있다.
조직이 이미 코드 리뷰 문화를 갖고 있다면
MDM 변경에도 같은 절차를 적용할 수 있다.

반대로 이 방식은 변경이 곧 배포라는 위험을 안는다.
4.94.0의 이름 변경 사례처럼 YAML 한 줄이 기기에 프로파일을 다시 보낼 수
있다.[^rel-494]
GitOps를 쓰는 조직은 저장소 변경을 기기에 반영하기 전에 드라이런을 확인하는
절차를 갖춰야 한다.
릴리스 노트는 라벨 이름 길이 오류를 드라이런에서 거부하도록 고쳤다고
적는다.[^rel-494]
드라이런이 실제 검증 단계로 쓰이고 있다는 증거다.

### AI가 변경을 제안하는 시대에는 승인 절차의 강제가 제품 기능이 된다

Fleet는 AI가 제안하고 사람이 승인한다는 흐름을 내세우고,
저장소 자체도 AI 에이전트의 기여에 모델 ID 공개를 요구한다.[^repo-agents]
승인 단계가 문장으로만 존재하는지 시스템이 강제하는지가 차이를 만든다.
MCP 서버의 확인 지시문이 지시문에 머무는 한, 승인 강제는 이 제품에서
아직 열린 문제다.
GitOps 쪽에서는 풀 리퀘스트 리뷰가 강제 장치가 되지만,
라이브 쿼리 쪽에서는 그런 장치가 코드에서 보이지 않는다.

### 도입 전 시험은 무료판 10대 규모로 실패 조건을 정해 놓고 한다

도입을 고민하는 팀이 할 수 있는 가장 작은 시험은 다음과 같다.
자체 호스팅한 무료판에 시험 기기 10대 안팎을 등록하고,
실제로 쓸 기능 세 가지를 골라 끝까지 돌려 본다.
각 기능에 합격 조건을 먼저 적어 둔다.
예를 들어 설정 프로파일이 기기에 도착하는 시간,
정책 평가 결과가 실제 설정과 일치하는지, 에이전트가 기기에 주는 부하다.

다음 관찰이 나오면 결론이 바뀐다.
쓰려던 핵심 기능이 무료판에 없다면 프리미엄 견적이 필요하다.
GitOps 반영이 예상과 다르게 기기를 건드린다면 변경 절차를 먼저 설계해야 한다.
에이전트의 수집 범위를 코드에서 확인할 수 없다면
보안 검토를 통과하지 못할 수 있다.
이 세 가지는 이 문서가 확인하지 못한 부분이므로, 시험에서 직접 확인할 대상이다.

---

[^why]: Fleet, [Fleet | Why Fleet | Fleet documentation](https://fleetdm.com/docs/get-started/why-fleet), 2026-11-09

[^pricing]: Fleet, [Fleet | Pricing](https://fleetdm.com/pricing), 2026-11-09

[^license]: Fleet Device Management, [LICENSE](https://github.com/fleetdm/fleet/blob/main/LICENSE), 2026-11-09

[^eelicense]: Fleet Device Management, [ee/LICENSE](https://github.com/fleetdm/fleet/blob/main/ee/LICENSE), 2026-11-09

[^opensrc]: Fleet, [Fleet | 💭 Why this way? | Fleet handbook](https://fleetdm.com/handbook/company/why-this-way#why-open-source), 2026-11-09

[^osquery]: GitHub, [osquery/osquery](https://github.com/osquery/osquery), 2026-11-09

[^nanomdm]: GitHub, [micromdm/nanomdm](https://github.com/micromdm/nanomdm), 2026-11-09

[^nudge]: GitHub, [macadmins/nudge](https://github.com/macadmins/nudge), 2026-11-09

[^swiftdialog]: GitHub, [swiftDialog/swiftDialog](https://github.com/swiftDialog/swiftDialog), 2026-11-09

[^releases]: GitHub, [Releases · fleetdm/fleet](https://github.com/fleetdm/fleet/releases), 2026-11-09

[^rel-494]: GitHub, [Fleet 4.94.0 (Oct 28, 2026)](https://github.com/fleetdm/fleet/releases/tag/fleet-v4.94.0), 2026-10-28

[^repo-ee-service]: GitHub, [fleetdm/fleet ee/server/service/service.go](https://github.com/fleetdm/fleet/blob/main/ee/server/service/service.go), 2026-11-09

[^repo-licensing]: GitHub, [fleetdm/fleet ee/server/licensing/licensing.go](https://github.com/fleetdm/fleet/blob/main/ee/server/licensing/licensing.go), 2026-11-09

[^repo-app]: GitHub, [fleetdm/fleet server/fleet/app.go](https://github.com/fleetdm/fleet/blob/main/server/fleet/app.go), 2026-11-09

[^repo-handler]: GitHub, [fleetdm/fleet server/service/handler.go](https://github.com/fleetdm/fleet/blob/main/server/service/handler.go), 2026-11-09

[^repo-orbit]: GitHub, [fleetdm/fleet orbit/pkg](https://github.com/fleetdm/fleet/tree/main/orbit/pkg), 2026-11-09

[^repo-orbit-license]: GitHub, [fleetdm/fleet orbit/LICENSE](https://github.com/fleetdm/fleet/blob/main/orbit/LICENSE), 2026-11-09

[^repo-mdm]: GitHub, [fleetdm/fleet server/mdm](https://github.com/fleetdm/fleet/tree/main/server/mdm), 2026-11-09

[^repo-mcp]: GitHub, [fleetdm/fleet server/fleetmcp](https://github.com/fleetdm/fleet/tree/main/server/fleetmcp), 2026-11-09

[^repo-mcp-auth]: GitHub, [fleetdm/fleet server/fleetmcp/auth.go](https://github.com/fleetdm/fleet/blob/main/server/fleetmcp/auth.go), 2026-11-09

[^repo-mcp-vetted]: GitHub, [fleetdm/fleet server/fleetmcp/vetted_queries.go](https://github.com/fleetdm/fleet/blob/main/server/fleetmcp/vetted_queries.go), 2026-11-09

[^repo-mcp-server]: GitHub, [fleetdm/fleet server/fleetmcp/mcp_server.go](https://github.com/fleetdm/fleet/blob/main/server/fleetmcp/mcp_server.go), 2026-11-09

[^repo-agents]: GitHub, [fleetdm/fleet AGENTS.md](https://github.com/fleetdm/fleet/blob/main/AGENTS.md), 2026-11-09

[^fx]: ExchangeRate-API, [USD 기준 환율 조회](https://open.er-api.com/v6/latest/USD), 2026-11-09
