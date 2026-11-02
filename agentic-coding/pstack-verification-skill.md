# pstack 가이드 1편: 에이전트가 자기 결과를 검증하는 스킬이 가장 중요한 도구다

트윗: [The Complete Guide to pstack Pt. 1](https://twitter.com/poteto/status/2094457600259842065)

## 소개

Twitter 사용자 lauren(@poteto)가 2026년 9월 1일에 올린 12분 분량의 Twitter
Article이다.
lauren은 자신을 SpaceXSI의 Grok @Bot 담당이며 React Compiler 핵심 팀과 Cursor,
Meta, Netflix를 거쳤다고 소개한다.
글은 자신의 개인 스킬 모음 pstack을 쓰는 방법을 연재로 풀어 쓰는 첫 편이고,
페이지에는 조회수 120만이 찍혀 있었다.
lauren은 pstack으로 한 달에 2,000개의 풀 리퀘스트(PR)를 높은 확신으로 운영
환경에 올린다고 쓴다.

1편의 주장은 한 줄이다.
가장 중요한 도구는 품질 높은 검증 스킬이고,
이 스킬은 스킬이라기보다 핵심 인프라처럼 다뤄야 한다.
검증(verification)은 에이전트가 자기 작업을 스스로 확인하는 일이며,
사람이 병목이 되지 않아도 에이전트가 성공할 때까지 계속 갈 수 있게 만든다.
lauren은 이것이 팀 전체의 산출을 100배에서 1,000배로 늘릴 수 있다고 쓴다.

## 검증 스킬 만들기

시작은 pstack을 설치하고 `/create-verification-skill`을 실행하는 것이다.
글은 pstack에 들어 있는 Dr Eggbot이라는 봇을 곁들일 것을 권한다.
Dr Eggbot에게 엔지니어 봇을 만들게 한 뒤,
그 봇에게 검증 스킬 생성을 시키고 매일 `/maintain-verification-skill`을 돌리는
루틴을 맞추라는 식이다.
이 스킬은 lauren이 Grok @Bot과 Cursor에서 쓰는 검증 스킬들을 증류한 일종의 메타
스킬이어서, 에이전트가 내 앱에 맞는 검증 스킬을 직접 만들게 한다.

기술 스택이 여기서 중요하다고 글은 말한다.
Electron이나 웹 앱이면 Chrome DevTools Protocol(CDP)로 브라우저 개발자 도구와
같은 도구를 쓸 수 있고, iOS 앱이면 시뮬레이터가 있다.
앱을 조작하고, 디버깅하고, 성능 트레이스를 뜨는 일을 사람이 직접 개발할 때처럼
에이전트가 할 수 있어야 한다.
풍부한 런타임이 없으면 `lldb`나 개발 환경의 사이드카 패키지 같은 도구를
에이전트에게 만들게 하라고 한다.

## 되풀이할 수 있게 만들기: CLI

pstack에는 Build the Lever라는 원칙이 있다.
스킬을 만들 때 마크다운만 쓰지 말고 에이전트에게 도구를 주라는 뜻이다.
검증 스킬이라면 앱의 조작과 디버깅을 스크립트로 묶은 작은 CLI를 만든다.
에이전트가 클릭 한 번을 위해 일회용 스크립트를 쓰는 대신 CLI 명령 하나를
실행하게 되어 토큰이 줄고, 스킬을 재현하고 시험하기 쉬워진다.

글이 드는 가상의 Electron 앱 예시는 다음과 같은 모양이다.

```bash
# health
node .cursor/skills/verify-atlas/control-atlas.mjs doctor

# open a blank thread and send
node .cursor/skills/verify-atlas/control-atlas.mjs new-session
node .cursor/skills/verify-atlas/control-atlas.mjs send "list open tasks in this project"

# accessibility snapshot of the live UI
node .cursor/skills/verify-atlas/control-atlas.mjs snapshot

# screenshot for evidence
node .cursor/skills/verify-atlas/control-atlas.mjs screenshot /tmp/atlas-proof.png

# wait for streaming / layout to settle
node .cursor/skills/verify-atlas/control-atlas.mjs wait-settle
```

글은 개발 환경도 함께 생각하라고 한다.
개발용 데이터베이스 시딩, 인증과 테스트 사용자,
테스트나 스테이징 환경에 대한 API 호출, 일관된 개발 환경 기동이 그 항목이다.

에이전트에게 친절한 CLI의 성질로 다음을 꼽는다.

- 조합하기 쉬운 API(John Ousterhout의 deep modules 철학)
- 파괴적일 수 있는 명령의 `--dry-run` 옵션
- 기능을 한꺼번에 보여 주지 않고 하위 명령으로 점진적으로 드러내기
- 에이전트가 대신 무엇을 해야 하는지 알려 주는 상세한 오류 메시지
- 충실한 `--help`
- JSON 같은 기계가 읽는 출력

CLI를 더 고급으로 만들기 전에 먼저 이 CLI를 좋게 만들고 오류를 없애는 데 시간을
쓰라고 권한다.

## 병렬화: worktree 대신 Cloud Agents

검증 스킬로 PR 몇 개를 올려 보고 나면 병렬 실행을 생각하게 된다.
첫 본능은 에이전트마다 git worktree로 저장소의 격리된 복사본을 주는 것이다.
글은 이를 권하지 않는다.
저장 공간과 기계 자원을 많이 쓰고, 저장소 크기와 기계 성능에 따라 병렬
에이전트를 많아야 10개쯤 돌릴 수 있다는 이유다.

대신 Cursor의 Cloud Agents를 권한다.
Cursor의 인프라에서 실제 컴퓨터를 가진 에이전트로,
의존성을 설치하고 앱을 실행하고 영상과 스크린샷을 찍고 실제 사용자처럼 앱과
상호작용할 수 있다.
처음 환경을 구성할 때는 에이전트를 보내 설정을 돕게 하고,
첫 빌드 뒤에 스냅샷을 떠 두어 이후 실행이 빨리 시작된다고 한다.
개발 경험을 앞 단계에서 충분히 다듬었다면 Cloud Agents 설정이 큰 일이 아니라는
것이 글의 말이다.

## Feature Map으로 에이전트를 똑똑하게 유지하기

앱이 복잡해지면 에이전트가 기능을 찾고 조작하려면 안내가 더 필요하다.
lauren은 Feature Map이라는 것을 고안했다고 한다.
앱의 모든 기능이 무엇을 하는지와 사용자 관점에서 거기에 어떻게 가는지를 검색하기
쉽게 담은 지도다.
`/create-verification-skill`은 스킬 옆에 `references/features` 디렉터리와
`README.md`를 만들고, README가 주요 기능의 개요와 세부 문서 링크를 담은
지도 자체다.

기능 문서 하나는 다음을 담는다.

- 하위 기능 목록
- 사용자 관점에서 거기에 가는 방법
- CLI로 그 기능을 조작하는 명령
- 함정(예: 설정 창을 중간에 닫으면 포커스가 갈 곳을 잃으니 `new-session`이나 `home`으로 복구한다)

글은 Feature Map을 구체화된 기억(materialized memory)으로 본다.
lauren은 코드베이스가 기억의 궁극적인 형태이고,
Feature Map은 그것을 토큰을 아끼도록 압축한 형태라고 쓴다.
스킬 안의 마크다운이므로 코드베이스에 기여하는 모든 사람이 이 공유 기억의 혜택을
본다고 한다.
그래서 검증 스킬의 유지보수가 중요하며,
`/maintain-verification-skill`을 하루 한 번 이상 돌리라고 권한다.

## 쓰는 법

프롬프트는 `/poteto-mode`로 시작한다.
Cursor에서는 자동 완성할 때 Enter 대신 Opt + Enter를 누르면 스킬이 Custom Mode로
고정되어 에이전트가 매 턴마다 스킬을 쓰라는 상기를 받는다.

새 기능을 만들 때의 프롬프트는 이런 모양이다.

```text
/poteto-mode build <description of feature, any useful context>. use /control-app to verify your changes and show me a video and screenshots as proof
```

`/control-app`은 `/create-verification-skill`이 만들어 낸 결과물이다.
Grok @Bot에서는 같은 일을 직접 하게 하지 않고 Cloud Agent를 띄우게 한다.
봇의 컨텍스트 창이 깨끗하게 유지되고 봇이 다른 일을 할 수 있어서,
봇을 에이전트를 감독하는 조정자로 쓰는 쪽을 선호한다고 한다.

성능 작업에서는 현재 상태의 트레이스를 먼저 뜨고, 개선 기회를 찾고,
표적 수정을 한 뒤 `/control-app`과 `/swarm`으로 개선을 확인하게 한다.
`/swarm`은 검증 스킬을 여러 Cloud Agent에 퍼뜨려 표본을 충분히 키우거나 앱을
퍼징하는 스킬이다.

사용자 제보를 자동으로 재현하는 데도 쓴다.
검증 스킬이 마음에 들면 Grok @Bot의 routines나 Cursor Automations에 넣어
일정이나 이벤트로 실행할 수 있다.
사용자 피드백을 Slack으로 흘려 보내면 봇이 제보마다 Cloud Agent로 재현을
시도하고, 지도와 스킬이 충분히 좋으면 자동 수정까지 맡길 수 있다고 한다.

## 비평

### 숫자는 저자의 주장이고 품질의 증거는 없다

글은 한 달 2,000개 PR과 팀 산출 100배에서 1,000배라는 숫자를 든다.
저자 스스로 이전에는 PR 수나 코드 줄 수를 신경 쓰지 않았고 그것이 허영
지표(vanity metric)였다고 쓴 뒤, 에이전트가 품질을 유지하거나 높일 수 있을 때는
양이 중요하다고 입장을 바꾼다.
품질이 유지된다는 근거는 Grok @Bot이 가장 효율적이고 성능 좋은 AI 데스크톱 앱
가운데 하나라는 주장과 코드 품질이 높다는 서술뿐이다.
되돌림(revert) 비율, 결함 비율, 리뷰 시간 같은 수치는 글에 없다.
이 문서는 앱을 설치해 보거나 PR을 확인하지 못했고,
숫자를 독립적으로 확인하지 못했다.

### 추천하는 도구는 저자의 현재와 과거 소속과 겹친다

글은 Cursor의 Cloud Agents와 Grok @Bot, pstack, Dr Eggbot을 권한다.
저자는 SpaceXSI에서 Grok @Bot을 맡고 있고 이전에 Cursor에 있었다고 소개한다.
소속은 글 끝의 소개란에 있지만, 본문이 그것을 추천의 이해관계로 짚지는 않는다.
독자는 같은 원칙(검증 루프, CLI, 기능 지도)이 이 제품들 없이도 성립하는지를 따로
따져야 한다.

### 자기 작업을 자기가 검증하는 구조의 맹점을 다루지 않는다

검증을 에이전트가 자기 작업을 확인하는 일로 정의하는 순간,
코드를 쓴 에이전트와 확인하는 에이전트가 같은 가정과 같은 맹점을 공유할 수 있다.
글이 드는 안전장치는 영상과 스크린샷을 증거로 받는 것과 `/swarm`으로 표본을
키우는 것이다.
영상과 스크린샷은 사람이 보아야 증거가 되는데, 하루 수백 개 PR이 들어오는 규모에서 그 시간이 어디서 나오는지는 쓰여 있지 않다.

### 병렬화 조언은 비용과 데이터 문제를 다루지 않는다

worktree를 말리고 Cloud Agents를 권하는 근거는 저장 공간과 기계 자원이다.
Cloud Agent는 외부 인프라에서 앱을 실행하므로 소스 코드와 테스트 데이터,
시크릿이 그 환경에 올라가고, 실행 시간만큼 비용이 든다.
글은 이 비용과 보안 쪽의 대가를 말하지 않는다.
도입 조건으로 읽으면, 코드를 외부 인프라에서 실행해도 되는 조직인지가 먼저
확인할 일이다.

### 기술 스택을 바꾸라는 조언은 근거가 한 줄이다

글은 검증이 중요해서 풍부한 디버깅 도구를 직접 만들거나 아예 다른 기술 스택을
고르는 것을 진지하게 권한다고 쓴다.
이유는 스택이 디버깅하고 제어하기 어려울수록 에이전트를 생산적으로 쓰기
어렵다는 것이다.
스택 변경의 비용(재작성, 채용, 기존 자산)과 얻는 것의 크기를 견주는 논의는 없다.

## 체크리스트

- [ ] 앱을 조작하고 디버깅하고 트레이스를 뜨는 수단(CDP, 시뮬레이터, 자체 도구)이 있는가
- [ ] 에이전트가 쓰는 CLI에 `doctor`, `snapshot`, `screenshot`, `wait-settle`에 해당하는 명령이 있는가
- [ ] 파괴적일 수 있는 명령에 `--dry-run`이 있고, 오류 메시지가 에이전트가 다음에 할 일을 알려 주는가
- [ ] CLI 출력이 JSON처럼 기계가 읽는 형태인가
- [ ] 개발용 데이터, 테스트 사용자, 스테이징 API 호출 방법이 문서화되어 있는가
- [ ] 기능마다 사용자 관점의 진입 방법과 조작 명령, 함정을 적은 Feature Map이 있는가
- [ ] 검증 스킬을 매일 유지보수하는 루틴(또는 담당자)이 있는가
- [ ] Cloud Agent에 소스와 테스트 데이터를 올려도 되는지 조직에서 확인했는가
- [ ] 영상과 스크린샷 증거를 누가 언제 보는지 정해져 있는가
