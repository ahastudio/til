# git-bug: git 저장소 안에 이슈를 보관하고 push와 pull로 주고받는 분산 버그 트래커

<https://github.com/git-bug/git-bug>

HN 토론: <https://news.ycombinator.com/item?id=49843174> (330점, 107개 댓글)

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

### 신원 체계가 git의 신원과 따로 논다

git-bug는 `git bug user create`로 자기만의 신원을 만든다.
Hacker News에서 deprave는 git이 쓰는 신원을 그대로 쓸 줄 알았다며 사용자 신원 관리 방식에 놀랐다고 적었다.[^deprave]
저자는 로드맵에서 신원을 조금 다시 만들고, Bluesky의 신원 체계인 `did:plc`에 뿌리를 둬 공개 키를 배포하겠다고 밝혔다.[^michaelmure-roadmap]
그러면 저장소 사이에서 신원을 훨씬 자연스럽게 공유할 수 있다는 것이다.

이 문제는 분산 버그 트래커의 근본 과제다.
중앙 서비스에서는 계정이 곧 신원이지만, 분산 시스템에서는 누가 이 댓글을 썼는지를 서명과 공개 키로 증명해야 한다.
git 커밋의 작성자 정보는 누구나 바꿀 수 있으니 그대로 쓸 수 없고, 별도의 신원 체계를 두면 사용자는 또 하나의 신원을 관리해야 한다.

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

이 방향은 v0.11.0의 코드 브라우저가 왜 들어갔는지를 설명한다.
이슈 트래커가 코드를 보여 주기 시작하면, 다음은 코드 리뷰이고, 그다음은 PR이다.
GitHub이 코드 호스팅에서 이슈와 PR로 확장했다면, git-bug는 반대로 이슈에서 시작해 포지의 나머지를 git 저장소 안에 채워 넣으려 한다.
이 저장소의 [[ink-and-switch]]가 연구하는 로컬 우선 소프트웨어의 아이디어가, 개발 도구의 가장 중앙화된 부분인 포지에 적용되는 셈이다.

### 1인 유지보수 오픈소스가 인프라가 될 때 생계 문제가 드러난다

저자는 로드맵 끝에 이 일을 전업으로 하는 것을 고민하고 있다며, 스스로를 부양할 방법에 대한 조언이나 기회가 있으면 알려 달라고 적었다.[^michaelmure-roadmap]
sebiw는 특정 기능과 보장된 지원을 담은 “엔터프라이즈” 등급을 제안했고,[^sebiw] ok_dad는 비기술 사용자도 쉽게 쓰게 만드는 것이 유료 고객을 얻는 길일 것이라고 답했다.[^ok_dad]

커널 커뮤니티가 시연할 만큼 쓸모 있어진 도구가, 여전히 한 사람의 여가에 기대고 있다.
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
