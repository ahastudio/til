# git-bug: git 저장소 안에 이슈를 보관하고 push와 pull로 주고받는 분산 버그 트래커

<https://github.com/git-bug/git-bug>

HN 토론: <https://news.ycombinator.com/item?id=49843174> (364점, 111개 댓글)

Show HN: [Show HN: git-bug – Distributed bug tracker embedded in git](https://news.ycombinator.com/item?id=17782121) (447점, 94개 댓글)

Show HN: [Show HN: Git-bug – Distributed bug tracker, or what to do when GitHub is down](https://news.ycombinator.com/item?id=22831604) (153점, 55개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=33730417> (380점, 79개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=43971620> (312점, 107개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/2e1une/distributed_offline_first_bug_tracker> (38점, 3개 댓글)

GN 토론: <https://news.hada.io/topic?id=34272>

## 소개

git-bug는 git에 완전히 통합된 분산 버그 트래커다.
README는 특징을 이렇게 정리한다.
버그 트래커를 갖는 데 git 저장소만 있으면 되고, 평소의 git 원격으로 버그를 push하고 pull하며, 비행기 안이나 바닷속에서도 버그를 읽고 쓸 수 있고, 쓰던 서비스가 멈추거나 나빠져도 이미 전체 백업을 갖고 있어 벤더 종속을 막는다.
버그 목록을 보거나 여는 데 밀리초가 걸리고, 프로젝트에 파일을 하나도 더하지 않으며, CLI, 터미널 UI, 웹 UI 중 원하는 것을 쓰거나 CLI와 GraphQL API로 기존 도구에 붙일 수 있다.
GitHub, GitLab, Jira, Launchpad와 가져오기, 내보내기를 하는 브리지도 있다.

저장소는 2018년 7월에 만들어졌고, Go로 작성됐으며, GPL-3.0 라이선스다.
2026년 9월 26일 기준 스타는 1만 개를 넘는다.
2026년 9월 22일 나온 v0.11.0은 v0.10.1 이후 16개월, 약 300개 커밋 만의 릴리스로, 처음부터 다시 쓴 웹 UI와 오래된 버그 몇 가지를 닫는 정확성 개선이 핵심이다.

## 사용법

```bash
git bug user create                  # 신원을 만든다
git bug add                          # 편집기가 열려 제목과 본문을 쓴다
git bug push [<remote>]              # 버그를 원격으로 보낸다
git bug pull [<remote>]              # 원격의 변경을 받는다
git bug ls "status:open sort:edit"   # 질의로 거르고 정렬한다
git bug termui                       # 대화형 터미널 UI
git bug webui                        # 로컬 HTTP 서버로 웹 UI를 띄운다
```

작업 흐름은 세 가지다.
순수한 git-bug 방식은 코드처럼 `git bug push`와 `git bug pull`로 팀원과 버그를 주고받는 것이다.
브리지 방식은 다른 버그 트래커를 개인용 로컬 원격 인터페이스처럼 쓰는 것으로, `git bug bridge pull`과 `git bug bridge push`로 동기화하고 터미널이나 편집기에서 오프라인으로 일한다.
웹 UI 방식은 누구나 문제를 올릴 수 있는 공개 포털을 목표로 하지만, 외부 OAuth 인증이 아직 없어 진행 중이다.

v0.11.0의 새 웹 UI에서는 이슈를 검색, 필터, 페이지 나눔으로 보고, 새로 열고, 댓글을 달고, 제목과 레이블과 상태를 바꿀 수 있다.
필터가 URL에 남아 보고 있는 화면을 그대로 링크로 보낼 수 있다.
웹 UI는 저장소의 코드 브라우저도 겸해, 파일 트리, 줄 범위를 링크할 수 있는 구문 강조 파일, 파일이나 디렉터리별 커밋 이력, 접을 수 있는 diff를 보여 주고, 이 모든 것이 같은 GraphQL API로 노출된다.

## 동작 방식

### 엔티티는 편집 연산의 연속이다

설계 문서에 따르면, 엔티티는 여러 프로세스에서 동시에 저장되고 편집되므로 일반 앱처럼 현재 상태를 저장할 수 없다.
두 프로세스가 같은 엔티티를 바꾸고 나중에 상태를 합치려 하면, 어느 쪽이 우선인지 알 수 없기 때문이다.
그래서 최종 버그 데이터 대신 편집 `Operation`의 연속을 저장하며, 이것은 연산 기반 CRDT에서 흔한 아이디어다.
최종 상태는 이 연산들을 올바른 순서로 빈 상태에 적용해 “컴파일”한다.

### git 객체로 저장한다

한 번의 편집 세션에서 나온 연산들은 `OperationPack`이라는 JSON 배열로 묶여 git `Blob`에 저장된다.
각 연산에는 유형, 작성자, 타임스탬프, 연산에 필요한 데이터, 그리고 식별자가 데이터의 해시이므로 충분한 엔트로피를 위한 난수가 들어간다.
이 `Blob`을 가리키는 git `Tree`를 만들고, 그 `Tree`를 가리키는 `Commit`을 만든다.
연산을 더할 때마다 새 `Commit`이 이어져 사슬을 이루고, 이 사슬은 `refs/<namespace>/<id>` 아래의 git 참조가 된다.
git이 필요한 데이터를 모두 push하므로, 첨부 미디어까지 원격으로 간다.
작업 디렉터리에 파일이 하나도 생기지 않는 이유가 여기 있다.

### 시간은 믿을 수 없다

연산의 타임스탬프로 순서를 정하고 싶겠지만, 다른 사람의 시계는 틀릴 수 있고 시스템을 속이려는 사람도 있을 수 있다.
그래서 git-bug는 Lamport 논리 시계를 쓴다.
무언가를 더할 때마다 알고 있는 가장 큰 시간 값에 1을 더해 붙이며, 두 값이 같으면 어느 쪽이 먼저인지 알 수 없는 동시 편집이다.
시계 값은 `create-clock-14`, `edit-clock-137` 같은 `Tree` 항목 이름에 직접 적히고, 그 항목은 모두 빈 `Blob` 하나를 가리키므로 네트워크 전송이 거의 없다.

엔티티의 식별자는 첫 연산의 해시이고, git처럼 7자로 잘라 보여 주며, 모호하지 않은 한 몇 글자만 입력해도 된다.

### 병합은 리베이스이고, 상태 대신 의도를 저장한다

2018년 첫 Show HN에서 notduncansmith가
git의 병합을 두고 왜 연산 묶음을 따로 만드느냐고 묻자,
저자 michaelmure는 git-bug의 병합 코드가
사실상 리베이스라고 답했다.[^michaelmure-rebase]
git에는 인덱스를 건드리지 않고 한 브랜치를 다른 브랜치 위로 옮기는
저수준 명령이 없어서 직접 구현했을 뿐이라는 것이다.
각 커밋은 서로 독립적이므로,
병합은 새 연산을 편집 사슬 끝으로 옮기는 일이고 충돌이 생기지 않는다.
이미 닫힌 버그를 또 닫았다면,
버그는 그대로 닫혀 있고 그 행동이 타임라인에 남는다.

2020년 스레드에서 그는 이 설계를
“상태 대신 사용자의 의도를 저장한다”고 다시 설명했다.[^michaelmure-intent]
동시 편집을 합칠 때는 연산을 가능한 한 잘 다시 정렬해 상태를 새로 계산한다.
그 결과가 완벽한 상태는 아닐 수 있지만,
버그는 항상 읽을 수 있는 합법적 상태에 있고,
누가 무엇을 했는지가 남아 있어 연산을 더해 손으로 바로잡을 수 있다.
그는 완전한 P2P 상황에서는 깨질 수 있다고 인정하며,
선형 사슬 대신 연산의 DAG로 옮기고 싶다고 밝혔다.
대신 상태를 git에, 특히 코드 옆에 그대로 저장하는 방식은
확실히 나쁘다고 단언했다.

`refs/bugs/` 아래의 참조가 `git gc`에 지워지지 않느냐는 질문도
첫 스레드에서 나왔다.
저자는 `refs/bugs/`와 `refs/remotes/<remote>/bugs/` 아래 참조는
수집 대상이 아니라고 답했고,[^michaelmure-refs]
avar는 `refs/` 아래의 모든 참조가 도달 가능성의 기준이 된다고
git의 동작을 확인해 주었다.[^avar-gc]
버그를 지우면 그 버그가 가리키던 blob도
다음 `git gc`에서 함께 정리된다.[^michaelmure-gc]

## 분석

### git의 참조 공간을 데이터베이스로 쓰는 오래된 아이디어의 가장 성숙한 구현이다

git 저장소에 이슈를 넣는다는 아이디어는 새롭지 않다.
Hacker News에서 teddyh는 이런 분산 버그 트래커가 꽤 많다고 알렸고,[^teddyh] khimaros와 sscaryterry는 git-issue와 ticgit을,[^khimaros][^sscaryterry] lolakutty는 이것이 fossil-scm에게서 배운 것 같다고 적었다.[^lolakutty]
mcepl은 그 어느 것도 정말 잘 동작하지 않는다며, 10년도 더 된 블로그 글의 상황이 크게 나아지지 않았다고 지적했다.[^mcepl]

AceJohnny2는 이런 도구가 가능한 이유를 git의 구조로 설명했다.[^AceJohnny2]
git은 해시로 참조되는 객체의 모음과 그 끝을 가리키는 참조로 이루어지고, 핵심 git은 `refs/` 아래 `heads/`와 `tags/` 정도만 쓰며, 흔히 잊히는 `git notes`가 `refs/notes/`를 쓴다.
그 밖의 이름은 무엇이든 붙일 수 있고, git 기반 버그 트래커는 모두 이 열린 공간을 쓴다.
Gerrit도 가상 네임스페이스 `refs/for/`로 push하면 변경이 만들어지게 한다.
git-bug가 다른 시도들과 다른 점은, 이 공간 위에 연산 기반 CRDT와 Lamport 시계라는 분산 시스템의 정석을 얹어 병합 충돌을 설계로 푼다는 데 있다.

선배들이 왜 실패했는지는 지난 스레드들에 꽤 구체적으로 남아 있다.
2022년 Izkata는 2010년부터 2015년 사이 이런 도구가 여럿 나왔지만
어느 것도 자리 잡지 못했다고 회고했다.[^Izkata]
가장 큰 문제는 바로 그 특징이어서, 이슈 상태가 개발자마다,
구현에 따라서는 로컬 브랜치마다 달라지기 쉬웠고,
회사에서는 프로젝트 관리자가 이슈를 보고 만들고 고칠 자리가 없었다는 것이다.
2020년 theamk는 Bugs Everywhere가
기본적으로 버그를 코드와 같은 브랜치에 파일로 두므로,
대개 누구에게나 열려 있는 버그 제출 권한이
대개 제한되는 main 커밋 권한을 요구하게 된다고 지적했다.[^theamk]
git-bug가 버그를 작업 트리 밖 별도 참조에 두고 연산을 합치는 구조를 택한 것은,
정확히 이 두 실패를 피하려는 선택으로 읽힌다.

다만 이 선택에도 비용이 있다.
첫 스레드에서 avar는 git 메일링 리스트에 설계를 올려 보라고 권하면서,
버그마다 참조를 하나씩 두는 설계에 대해
git의 일부 연산이 참조 수에 비례해 느려진다는 점을 알아 두라고 조언했다.[^avar]
버그가 수만 개인 저장소에서는 이 비용이 드러날 수 있다.
2025년 cryptonector는 더 근본적인 비용을 짚었다.[^cryptonector]
버그 트래커는 본래 SQL 애플리케이션인데,
git으로 옮기면 이슈 사이의 참조 무결성이 쉽게 깨지고,
git에는 이슈 질의에 맞는 색인이 없어
데이터가 커질수록 검색이 문제가 된다는 것이다.
jFriedensreich는 데이터가 이미 버전 관리되고 있으니 증분으로 갱신되는
SQLite 보조 색인을 두는 것이 그렇게 어렵지 않다고 답했다.[^jFriedensreich]
목록을 밀리초 만에 보여 준다는 README의 약속도, 원본은 git에 두고
질의는 별도 캐시에서 하는 이런 이중 구조를 전제로 해야 지켜질 수 있다.

### 커널 커뮤니티가 쓰기 시작했다는 것이 이번 릴리스의 가장 큰 신호다

Hacker News에서 Aissen은 b4의 관리자이자 Linux Foundation IT 책임자인 Konstantin Ryabitsev가 바로 이번 주 Kernel Recipes 콘퍼런스에서 b4와 kernel.org의 cgit 포크에서 git-bug를 지원하는 것을 시연했다고 알렸다.[^Aissen]
커널처럼 메일링 리스트와 분산된 도구로 일해 온 커뮤니티에게, 중앙 서비스 없이 저장소와 함께 움직이는 이슈는 기존 작업 방식과 잘 맞는다.

GitHub 같은 포지에 이슈를 두면, 이슈는 저장소와 다른 수명을 가진다.
저장소를 옮기면 이슈는 남고, 서비스가 사라지면 이슈도 사라진다.
int_19h는 해결된 버그 목록이 코드 이력의 필수 부분이라며, 디버깅은 흔히 `git blame`에서 커밋과 연결된 이슈를 찾는 일이고, 그 메타데이터가 특정 플랫폼에 묶이지 않고 저장소에 있으면 좋다고 적었다.[^int_19h]

## 비평

### 이슈는 코드보다 훨씬 많은 사람이 쓰는데, 그 사람들은 git을 쓰지 않는다

Hacker News에서 cush는 이런 도구가 성립하려면 이슈가 너무 넓게 접근 가능해야 한다고 지적했다.[^cush]
이슈를 만드는 데 장벽이 있으면 사람들은 이슈를 올리지 않고, 모든 역할과 모든 직급이 이슈를 보고 고치므로, 중앙 서비스를 원하지 않더라도 이것은 중앙 서비스의 이상적인 쓰임새라는 것이다.
Lobste.rs에서 Vaelatern도 이슈를 저장소에 두면서 허가되지 않은 접근을 막는 것이 요령이라며, 공개 환경에서는 이슈를 저장소 밖에 두는 편이 훨씬 쉽다고 적었다.[^Vaelatern]

저자 michaelmure는 cush에게 동의하며, 곧 웹 UI가 OAuth와 OIDC를 받아 평범한 버그 트래커 경험을 쉽게 호스팅하고 복제할 수 있게 하면서도 일반 포지가 가질 수 없는 다른 흐름의 이점을 누리게 하겠다고 답했다.[^michaelmure-oauth]
그는 이것이 분산 버그 트래커가 실제로 작동하게 하는 핵심 기능이라고 말했다.
그러나 그 기능은 아직 없다.
README가 공개 포털을 “진행 중”으로 표시하는 동안, git-bug는 git을 쓰는 사람들끼리의 버그 트래커로 남는다.

지난 스레드들을 나란히 놓으면 이 약속이 얼마나 오래됐는지 드러난다.
2018년 첫 Show HN에서 katzgrau가
QA와 지원 인력은 어떻게 쓰느냐고 묻자,[^katzgrau]
저자는 웹 UI를 앞으로 공개 인터페이스로도 쓰게 할 계획이며
사용자 인증이 필요하다고 답했다.[^michaelmure-2018]
같은 자리에서 rout39574는 티켓을 고칠 수 있어야 하는 사람이
코드를 고칠 수 있는 사람보다
훨씬 많다며 권한 모델이 문제가 될 것이라고 반박했다.[^rout39574]
2022년에는 저자가 널리 쓰이려면
PR 지원과 웹 UI의 외부 인증이 먼저 필요하다고 적었고,[^michaelmure-2022]
2025년에는 댓글을 달려면 저장소에 push 권한이 있어야 하느냐는
IshKebab의 질문에,[^IshKebab]
지금은 그렇지만 웹 UI에 외부 인증을 붙여 공개 포털로 만들 것이고
거의 다 왔다고 답했다.[^michaelmure-2025]
그리고 2026년 스레드에서도 같은 기능이 다음 계획으로 나온다.
8년 동안 같은 기능이 “곧”이었다는 사실은, 이것이 시간 문제가 아니라
분산 모델 위에 공개 참여를 얹는 일 자체가 어렵다는 신호로 읽어야 한다.

그 사이의 우회로는 브리지다.
2025년 관리자 sudoforge는
push 권한이 없는 외부 기여자의 흐름을 이렇게 정리했다.[^sudoforge]
빈 저장소를 만들고 git-bug 신원을 만든 뒤,
GitHub 브리지를 설정해 이슈를 로컬로 가져오고,
로컬에서 이슈를 만들거나 댓글을 단 다음 브리지로 내보낸다.
이때 쓰이는 것은 브리지에 넣은 API 자격 증명이고,
로컬 `refs/bugs`는 원격으로 push하지 않는다.
결국 외부 참여는 아직 중앙 포지의 계정을 빌려서만 가능하다.

### 신원 체계가 git의 신원과 따로 논다

git-bug는 `git bug user create`로 자기만의 신원을 만든다.
Hacker News에서 deprave는 git이 쓰는 신원을 그대로 쓸 줄 알았다며 사용자 신원 관리 방식에 놀랐다고 적었다.[^deprave]
저자는 로드맵에서 신원을 조금 다시 만들고, Bluesky의 신원 체계인 `did:plc`에 뿌리를 둬 공개 키를 배포하겠다고 밝혔다.[^michaelmure-roadmap]
그러면 저장소 사이에서 신원을 훨씬 자연스럽게 공유할 수 있다는 것이다.

이 문제는 분산 버그 트래커의 근본 과제다.
중앙 서비스에서는 계정이 곧 신원이지만, 분산 시스템에서는 누가 이 댓글을 썼는지를 서명과 공개 키로 증명해야 한다.
git 커밋의 작성자 정보는 누구나 바꿀 수 있으니 그대로 쓸 수 없고, 별도의 신원 체계를 두면 사용자는 또 하나의 신원을 관리해야 한다.

### 해시 식별자는 사람이 부르는 이슈 번호가 되지 못한다

분산 시스템에서는 자동 증가 번호를 쓸 수 없으니,
git-bug는 첫 연산의 해시를 식별자로 쓴다.
2022년 foreigner는 이것이 이해는 되지만
실무에서는 꽤 불편할 것이라고 지적했다.[^foreigner]
커밋 해시와 달리 버그 번호는 테스트 팀, 관리자와의 대화나 릴리스 노트에서
훨씬 자주 인쇄되고 입으로 불리기 때문이다.
fdye도 QA 흐름에서는 `SEC-3640`처럼
짧은 Jira식 약칭으로 티켓을 부르고 맡기는 것이 보통이라며,
사람이 읽고 말할 수 있는 식별자가 필요할 것이라고 거들었다.[^fdye]

해법이 없지는 않다.
jedberg는 기여자마다 접두 글자를 하나씩 맡겨
A로 시작하는 번호, B로 시작하는 번호를 따로 매기고,
동기화하다 겹치면 늦게 맡은 쪽이 이름을 바꾸게 하자고 제안했다.[^jedberg]
그러나 이런 제안은 모두 어딘가에 조정 지점을 다시 만든다.
번호를 누가 먼저 맡았는지 정하는 순간, 분산 시스템은 작은 중앙을 하나 갖게 된다.
식별자 문제는 분산 버그 트래커가 사람의 습관과 부딪히는 지점 가운데
가장 작지만 매일 마주치는 곳이다.

### 실사용의 걸림돌은 여전히 push와 pull에 있다

Hacker News에서 jason_oster는 몇 달 전 git-bug를 써 봤는데 SSH 에이전트 관련 이슈 하나가 치명적이었다며, 우회책은 있지만 예쁘지 않다고 적었다.[^jason_oster]
저자는 곧 고치겠다며, 보안 때문에 git 바이너리를 부르지 않으려 했지만 go-git이 어떤 경우에는 충분히 견고하지 않다는 것을 인정해야 한다고 답했다.[^michaelmure-git]
push와 pull에 git 바이너리를 쓰는 선택지를 두고, 결과에 따라 기본값으로 만들 수도 있다는 것이다.

버그 트래커의 핵심 약속이 “평소의 git 원격으로 주고받는다”인데, 그 주고받기가 평소의 git과 다르게 동작하면 약속이 흔들린다.
외부 git 바이너리를 부르지 않으려는 보안상의 선택이 오히려 사용자의 기존 git 설정과 어긋나는 것은, 도구가 git에 “통합”된다는 말의 경계를 보여 준다.

## 인사이트

### 로컬 우선 포지로 가는 길은 이슈에서 시작해 PR과 CI로 이어진다

michaelmure의 로드맵은 웹 UI의 외부 인증, 웹 UI를 통한 git 원격 엔드포인트, 신원 재설계, 그리고 PR과 CI 지원이다.[^michaelmure-roadmap]
그는 이것이 누구나 손쉽게 직접 호스팅할 수 있는 꽤 완결된 로컬 우선 포지가 될 것이라고 적었다.
이름에 대해서도 PR로 넓히려면 CLI 명령에 자리를 마련해야 하는데, `git bug pr` 옆에 `git bug bug`가 있는 것은 꽤 못생겼다고 답했다.[^michaelmure-name]
이 고민은 2022년에도 있었다.
git 이름을 쓰는 프로젝트에 대한 상표 문제가 거론되자,
저자는 git 쪽이 상표 면에서는 꽤 너그러웠지만
네임스페이스를 차지한다는 지적에는
일리가 있다고 인정했다.[^michaelmure-trademark]
프로젝트 보드나 PR 같은 새 엔티티가 들어오면 git 하위 명령으로 늘어놓는 것이
헷갈리거나 충돌할 수 있어, git 통합에서 빠지는 것까지 고려하고 있다는 것이다.

이 방향은 v0.11.0의 코드 브라우저가 왜 들어갔는지를 설명한다.
이슈 트래커가 코드를 보여 주기 시작하면, 다음은 코드 리뷰이고, 그다음은 PR이다.
GitHub이 코드 호스팅에서 이슈와 PR로 확장했다면, git-bug는 반대로 이슈에서 시작해 포지의 나머지를 git 저장소 안에 채워 넣으려 한다.
이 저장소의 [[ink-and-switch]]가 연구하는 로컬 우선 소프트웨어의 아이디어가, 개발 도구의 가장 중앙화된 부분인 포지에 적용되는 셈이다.

### 분산 트래커의 자리는 고객용 창구가 아니라 개발자용 내부 장부다

2018년 첫 스레드에서 ken은
가장 성공적이었던 회사가 트래커를 두 개 썼다고 회고했다.[^ken]
하나는 고객이 이슈를 올리고 계약 요구 사항과 연결하는
사용자 친화적인 외부용이고,
다른 하나는 개발자가 어느 줄이 틀렸고
어느 변경 해시가 버그를 들여왔는지 이야기하는 내부용이었다.
고객은 소스 코드와 내부 로드맵을 보면 안 되고,
개발자는 요청에 딸린 고객 데이터를 보면 안 되었다.
그는 이 분리가 놀랍도록 잘 동작했다며,
git-bug가 내부용으로 훌륭할 것 같다고 적었다.

2022년 몇 년째 쓰고 있다는 njt의 경험도 같은 결론에 닿는다.[^njt]
커미터가 많은 큰 프로젝트에는 GitHub이나 GitLab의 내장 기능이 낫고,
혼자 쓰거나 규모가 작은 수십, 수백 개의 저장소에서
이 도구가 가장 빛난다는 것이다.
비평에서 본 공개 참여의 어려움은, 이 자리매김에서는 결함이 아니라 범위가 된다.

브리지는 이 두 세계를 잇는 장치다.
wankle이 독립적으로 분산되는 도구가
브리지를 제공하는 것은 자기모순이라고 하자,[^wankle]
저자는 브리지가 프로젝트 전체가 갈아타기로 합의하지 않아도
개인이 먼저 쓸 수 있게 해 네트워크 효과를 깨는 진입로이고,
이력을 잃지 않는 이전 경로이며,
중앙 포지를 계속 쓰더라도 백업이 된다고 반박했다.[^michaelmure-bridges]
외부용은 중앙 포지에 두고, 내부용 장부만 저장소 안에 두는 ken의 구조를
git-bug는 브리지 하나로 개인 단위에서 재현할 수 있다.

### 1인 유지보수 오픈소스가 인프라가 될 때 생계 문제가 드러난다

저자는 로드맵 끝에 이 일을 전업으로 하는 것을 고민하고 있다며, 스스로를 부양할 방법에 대한 조언이나 기회가 있으면 알려 달라고 적었다.[^michaelmure-roadmap]
sebiw는 특정 기능과 보장된 지원을 담은 “엔터프라이즈” 등급을 제안했고,[^sebiw] ok_dad는 비기술 사용자도 쉽게 쓰게 만드는 것이 유료 고객을 얻는 길일 것이라고 답했다.[^ok_dad]

커널 커뮤니티가 시연할 만큼 쓸모 있어진 도구가, 여전히 한 사람의 여가에 기대고 있다.
2022년에도 저자는 이 범위의 일이 멀지 않았지만
본업이 바빠 기여자의 도움에 기대고 있다고 적었다.[^michaelmure-dayjob]
2025년 스레드에서는 저장소가 `MichaelMure/git-bug`에서
`git-bug` 조직으로 옮겨 가 있었고,
sudoforge가 관리자로서 질문에 답했다.[^sudoforge]
일손은 조금 늘었지만,
전업으로 할 방법을 묻는 2026년의 글은 그 구조가 아직 바뀌지 않았음을 보여 준다.
그리고 그 도구를 유료로 만들 가장 자연스러운 방법, 곧 호스팅 서비스를 파는 것은 도구의 존재 이유, 곧 중앙 서비스에 의존하지 않는 것과 부딪힌다.
로컬 우선 소프트웨어가 [[ink-and-switch]]의 Allume처럼 구독으로 팔릴 때 “로컬 전용인데 왜 구독이냐”는 질문을 받았듯, 분산 버그 트래커도 무엇을 팔 것인지라는 같은 질문 앞에 선다.

---

[^teddyh]: <https://news.ycombinator.com/item?id=49844367>

[^khimaros]: <https://news.ycombinator.com/item?id=49847870>

[^sscaryterry]: <https://news.ycombinator.com/item?id=49847977>

[^lolakutty]: <https://news.ycombinator.com/item?id=49843813>

[^mcepl]: <https://news.ycombinator.com/item?id=49844806>

[^AceJohnny2]: <https://news.ycombinator.com/item?id=49848226>

[^Aissen]: <https://news.ycombinator.com/item?id=49843901>

[^int_19h]: <https://news.ycombinator.com/item?id=49851814>

[^cush]: <https://news.ycombinator.com/item?id=49845173>

[^Vaelatern]: <https://lobste.rs/s/2e1une/distributed_offline_first_bug_tracker#c_jvzwcs>

[^michaelmure-oauth]: <https://news.ycombinator.com/item?id=49845225>

[^deprave]: <https://news.ycombinator.com/item?id=49847770>

[^michaelmure-roadmap]: <https://news.ycombinator.com/item?id=49844476>

[^jason_oster]: <https://news.ycombinator.com/item?id=49846348>

[^michaelmure-git]: <https://news.ycombinator.com/item?id=49847079>

[^michaelmure-name]: <https://news.ycombinator.com/item?id=49844586>

[^sebiw]: <https://news.ycombinator.com/item?id=49844691>

[^ok_dad]: <https://news.ycombinator.com/item?id=49849265>

[^michaelmure-rebase]: <https://news.ycombinator.com/item?id=17783910>

[^michaelmure-intent]: <https://news.ycombinator.com/item?id=22840482>

[^michaelmure-refs]: <https://news.ycombinator.com/item?id=17784339>

[^michaelmure-gc]: <https://news.ycombinator.com/item?id=17783027>

[^avar-gc]: <https://news.ycombinator.com/item?id=17785477>

[^Izkata]: <https://news.ycombinator.com/item?id=33734698>

[^theamk]: <https://news.ycombinator.com/item?id=22833607>

[^avar]: <https://news.ycombinator.com/item?id=17785501>

[^cryptonector]: <https://news.ycombinator.com/item?id=43987872>

[^jFriedensreich]: <https://news.ycombinator.com/item?id=43989395>

[^katzgrau]: <https://news.ycombinator.com/item?id=17782374>

[^michaelmure-2018]: <https://news.ycombinator.com/item?id=17782416>

[^rout39574]: <https://news.ycombinator.com/item?id=17782526>

[^michaelmure-2022]: <https://news.ycombinator.com/item?id=33732730>

[^IshKebab]: <https://news.ycombinator.com/item?id=43992352>

[^michaelmure-2025]: <https://news.ycombinator.com/item?id=43992423>

[^sudoforge]: <https://news.ycombinator.com/item?id=43992735>

[^foreigner]: <https://news.ycombinator.com/item?id=33732262>

[^fdye]: <https://news.ycombinator.com/item?id=33733726>

[^jedberg]: <https://news.ycombinator.com/item?id=33734902>

[^michaelmure-trademark]: <https://news.ycombinator.com/item?id=33731141>

[^ken]: <https://news.ycombinator.com/item?id=17783253>

[^njt]: <https://news.ycombinator.com/item?id=33732470>

[^wankle]: <https://news.ycombinator.com/item?id=33733085>

[^michaelmure-bridges]: <https://news.ycombinator.com/item?id=33733132>

[^michaelmure-dayjob]: <https://news.ycombinator.com/item?id=33733747>
