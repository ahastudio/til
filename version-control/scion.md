# Anthropic이 Git을 버리고 자체 버전 관리 시스템 Scion을 만든 이유

원문: [Redesigning source control at Anthropic \ Anthropic](https://www.anthropic.com/engineering/redesigning-source-control)

HN 토론: <https://news.ycombinator.com/item?id=50073633> (725점, 710개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/5ucftp/redesigning_source_control_at_anthropic> (21점, 13개 댓글)

GN 토론: <https://news.hada.io/topic?id=35309>

## 요약

Anthropic 엔지니어링 블로그에 2026년 10월 13일 올라온 글로,
Nick G.와 소스 관리 팀이 썼다.
요지는 Claude가 코드를 쓰는 속도가 사람 규모로 설계된 개발 인프라를 넘어섰고,
그 첫 병목이 소스 관리였다는 것이다.
Anthropic은 2026년 5월 하루 평균 약 2,500개의 변경을 병합했는데,
9월에는 하루 3만 개를 넘겼다.
글은 병합 수요가 사실상 무한하며,
병목 하나를 없앨 때마다 코드 양이 곧바로 더 늘어난다고 본다.

모노레포의 규모는 Git의 설계와 맞지 않게 되었다.
main 브랜치 이력만 100GB 가까이 되고, 압축한 작업 사본은 25GB가 넘는다.
CI만으로 하루 약 2,500만 번 체크아웃이 일어나므로,
그대로 받으면 하루 600PB가 넘는 Git 트래픽이 된다.
얕은 클론, 희소 체크아웃, promisor remote,
내부 미러, 블롭 저장소의 스냅숏(seed)을
모두 써 봤고,
한때 내부 Git 미러를 수백 대 운영했지만 병합 속도를 따라가지 못했다.
팀은 자신들이 Git을 권위 있는 사본 하나를 둔 중앙 집중 시스템으로 쓰고 있고,
클라이언트 대부분이 항상 온라인인 에이전트와 작업이라는 점에 주목했다.

그래서 5개월 만에 자체 버전 관리 시스템 Scion을
만들고 모노레포를 Git에서 완전히 옮겼다.
같은 기간에 코드 리뷰 도구 Antique, 코드 검색, 소스 관리 IAM 등도 만들었다.
Scion의 원칙은 여섯 가지다.
클라이언트는 항상 온라인이다.
서버가 이력, blame, 커밋, 병합, 리베이스를 맡고 클라이언트는 제한된 캐시만 둔다.
클라이언트가 쓰는 모든 질의를 API로도 열어 작업이 로컬 저장소 없이 묻게 한다.
모든 구성 요소를 수평 확장한다.
커밋은 변경 크기에 비례하는 비용으로, 잠금 없이 만든다.
작업 사본은 선택 사항이며 희소 체크아웃과 가상화 체크아웃이 기본이다.
Google의 Piper와 Meta의 Sapling을 선행 사례로 참고했다고 밝힌다.

구조의 중심은 “changeset”이다.
Git 커밋이 트리를 가리키는 것과 달리 changeset은
첫 번째 부모 대비 바뀐 파일 목록과
블롭 저장소의 내용 주소를 담는 쓰기 전 로그(write-ahead log) 항목이다.
packfile도, 잠금도, 서버 간 조율도 없어 높은 처리량을 받을 수 있고,
ref 이동은 Spanner 행 하나에 대한 compare-and-swap이다.
blame, 경로 이력, 커밋 그래프의 skip list 같은 구조는
부모의 값에서 재귀적으로 계산하는 “파생 데이터”로 만든다.
체크아웃은 클라이언트가 필요한 트리와 블롭을 요청하는 방식이라
노드별 `scion-daemon`, 지역별 `scion-cache`, 권위 있는 `scion-server`의
계층 캐시로 처리되며, 각 계층의 캐시 적중률은 99%가 넘는다.
결과적으로 CPU와 메모리 기준 인프라가 기존 Git 미러링보다 200배 작아졌고,
체크아웃은 분 단위에서 초 단위로 빨라졌으며 CI는 CPU 용량의 25%를 아꼈다.

글은 교훈도 정리한다.
Scion과 Antique, 관련 시스템 여섯 개 정도를 7명이 만들고 5개월 만에 이전했다.
엔지니어 모두가 Claude가 자기보다 코드를 잘 쓴다고 평가하지만,
시스템 간 설계와 트레이드오프는 사람이 맡았고
Claude에게 “아니”라고 말하는 일이 많았다.
변경은 여전히 사람이 모두 리뷰하지만 코드 한 줄 한 줄이 아니라 의도를 본다.
Claude Mythos Preview는 손으로 쓴 Git→Scion 수집 파이프라인을
메모리 20배 적게, 4배 빠르게 다시 썼다.
각 구성 요소를 감시하는 “superfan” Claude를 Slack 채널마다 두었고,
전역 저장소 잠금이 있는 병합 큐 대신 병합 후와 배포 전 자동 테스트에 투자했다.
Scion은 일반 용도로 Git을 대체할 수 없고 공개할 계획도 없으며,
대신 Git 서버 구조, 서버 측 RPC, 협상 프로토콜 개선 아이디어를
GitHub, GitLab, 오픈소스 커뮤니티와 나누겠다고 한다.

## 분석

### 핵심 주장: Git의 분산 설계가 에이전트 규모에서는 비용이 된다

글의 논리는 Git의 강점을 부정하지 않는다.
모든 클론이 완전한 저장소라서 오프라인으로 diff,
이력, blame을 계산할 수 있다는 설계는
대부분의 저장소에 맞는 선택이라고 먼저 인정한다.
문제는 그 설계가 전제하는 사용 패턴이다.
Git은 사람이 노트북에서 오프라인으로 일하는
상황을 위해 모든 데이터를 클라이언트로 보낸다.
Anthropic의 클라이언트는 대부분 CI 작업과 에이전트이고, 정의상 항상 온라인이다.

이 관찰에서 나머지 원칙이 모두 따라 나온다.
클라이언트가 항상 온라인이라면 계산을 서버로 옮길 수 있고,
그러면 클라이언트는 전체 이력을 가질 필요가 없으며,
서버가 계산을 맡으려면 수평 확장이 필수가 된다.
Scion은 Git의 대안이라기보다 Git의 분산 기능을 제거하고
그 자리를 서버 API로 채운 시스템이다.

### 맥락: 대형 모노레포 회사들이 이미 걸어간 길

이 결론 자체는 새롭지 않다.
Google은 Piper로, Meta는 Mercurial을 고쳐 만든 Sapling으로
이미 같은 방향의 답을 냈고, 글도 이를 선행 사례로 밝힌다.
Microsoft가 Windows 저장소를 위해 만든 VFS for Git도
파일을 필요할 때만 받는 가상화 체크아웃이라는 같은 발상이었다.
새로운 것은 규모에 이른 경로다.
Google과 Meta는 수만 명의 엔지니어가 10년 넘게 쌓은 코드로 그 규모에 도달했지만,
Anthropic은 병합 수를 4개월 만에 12배로 늘린 에이전트로 도달했다.

HN에서도 비슷한 지적이 많았다.
tancop은 Subversion이나 Perforce 같은
서버 중심 버전 관리를 현대적으로 다시 만든 것이며
Epic Games의 Lore와 닮았다고 했고,[^tancop]
cube00은 GitHub가 멈추는 것보다 온라인 전용 클라이언트가
멈추는 쪽이 더 괴로울 것이라고 경고했다.[^cube00]
LinkedIn에서도 seok won yoon이 SVN 느낌이 좀 난다고 했다.[^seokwonyoon]
East River Source Control의 steveklabnik은
대형 팀과 에이전트가 함께 일하는 모노레포라면
Git의 확장 한계에 부딪힌다는 자신들의 가설을
Anthropic이 확인해 주었다고 반겼다.[^steveklabnik]

Lobste.rs의 fzakaria도 읽으면서 “다시 Perforce로 돌아왔다”는 생각이 들었다고 했다.[^fzakaria]
GeekNews의 dudnspa0203은 Google에도 같은 이름의 Scion 프로젝트가
있어 헷갈리기 쉽다고 짚었다.[^dudnspa0203]

그래서 글이 진짜로 전하는 것은 기술이 아니라 시간표다.
대형 모노레포의 문제는 원래 수십 년이 걸려 찾아왔는데,
에이전트를 많이 쓰는 조직에는 몇 달 만에 찾아온다.
글이 6~12개월 안에 이런 문제가 흔해질 것이라고 예측하는 근거가 여기에 있다.

### 구조적 패턴: 사람 규모의 절차가 하나씩 무너진다

소스 관리는 첫 사례일 뿐이다.
글은 병합 큐도 에이전트 규모에서는 의미가 없다고 말한다.
테스트가 도는 동안 수백, 수천 개의 변경이 병합되는 상황에서는
전역 저장소 잠금을 유지할 수 없어서
병합 후 테스트와 배포 전 테스트로 옮겼고,
동시 변경이 충돌하면 Claude가 사람보다 빨리 고친다고 설명한다.

이는 “병합 전에 반드시 초록불”이라는 지속적 통합의 기본 계약을 바꾼 것이다.
코드 리뷰도 같은 방향으로 바뀌었다.
사람은 모든 줄을 읽지 않고 변경의 의도를 보며,
리뷰 도구는 주석만 바뀐 변경과 민감한 로직 변경을 구분해
사람의 주의를 중요한 변경에 모은다.
사람이 매 단계를 확인하던 절차가 사후 검증과 자동 분류로 옮겨 가는 패턴이다.

### 저자가 당연하게 여기는 것: 토큰 예산과 항상 온라인인 세계

글은 스스로 Anthropic이 특이하다고 인정한다.
내부용으로 쓸 수 있는 토큰이 다른 회사가
현실적으로 쓸 양을 훨씬 넘는다고 적는다.
그러나 이 특이성은 결론의 일반화를 크게 제한한다.
병합 수가 12배로 는 것은 수요가 무한해서이기도 하지만,
그 수요를 채울 토큰을 제한 없이 쓸 수 있었기 때문이기도 하다.

“클라이언트는 항상 온라인”이라는 전제도 마찬가지다.
CI와 에이전트는 온라인이지만, 그 에이전트를 지휘하는 사람은
비행기 안에서도, 장애 중에도 코드를 봐야 할 수 있다.
글은 사람 개발자가 오프라인 상황에서 무엇을 잃는지는 다루지 않는다.

amluto는 이 대목에서 등을 돌렸다.
Git과 jj의 핵심은 로컬에서 작은 커밋을 쌓고 고치고 버릴 수 있다는 것인데,
모든 커밋을 서버에서 만들면 그 장점이 사라진다는 것이다.[^amluto]
저자 nickg-anthropic는 즉시 올리는 방식 덕분에 연구 작업, CI, 여러 개발 환경이
같은 커밋 해시를 바로 쓸 수 있다고 답했다.[^nickg-anthropic-hash]
서버가 꺼졌을 때를 위한 로컬 커밋 버퍼도 만들 수는 있지만,
그러면 클라이언트가 서버의 일을 다시 배워야 하고
이력이나 blame 같은 질문에는 여전히 답할 수 없으며,
가장 많이 쓰는 사용자인 Claude가 어차피 온라인이라 우선순위가
아니었다고 덧붙였다.[^nickg-anthropic-offline]

## 비평

### 성과 지표가 병합 수에 묶여 있다

글의 출발점은 “하루 병합 3만 개”라는 숫자다.
병합 수가 늘었다는 것은 시스템이 더 많은 변경을 소화했다는 뜻이지,
더 많은 가치를 만들었다는 뜻은 아니다.
글은 병합 수요가 사실상 무한하다고 하면서도
그 변경들이 어떤 결과로 이어졌는지,
되돌린 변경이나 충돌 수정 변경이 얼마나 포함되어 있는지는 밝히지 않는다.

병합 큐를 버리고 병합 후 테스트로 옮겼으며
동시 변경의 충돌을 Claude가 고친다는 설명은 이 우려를 키운다.
충돌을 고치는 변경도 병합 수에 들어간다.
변경 수가 증가할수록 그 변경이 만든 문제를 고치는 변경도 같이 증가하는 구조라면,
병합 수는 생산성 지표보다는 시스템이 감당하는 부하의 지표에 가깝다.

HN에서 joshheitzman은 커밋 수가 코드 줄 수보다 나은 지표가 아니라며
실제 소프트웨어는 어디 있느냐고 물었다.[^joshheitzman]
저자는 같은 코드를 반복해서 고치는 것이 아니라 “더 넓게”,
즉 더 많은 일을 하는 방향으로
늘어난 것이라고 답했다.[^nickg-anthropic-wider]
모델 학습과 서빙 시스템, 내부 도구와 인프라, 연구, 제품과 API 등
매주 새 프로젝트가 생긴다는 설명도 붙였다.[^nickg-anthropic-what]
충돌에 대해서는 텍스트 충돌은 허용하지 않지만,
함수 로직 변경과 새 호출 추가가 동시에 일어나는 식의 의미적 충돌은
일정 병합 속도를 넘으면 피할 수 없다고 인정했다.[^nickg-anthropic-conflict]
altcognito는 하루 2,500만 체크아웃이
병합 하나당 833번이라고 계산했는데,[^altcognito]
저자는 병렬로 도는 테스트 샤드마다 코드를
체크아웃하기 때문이라고 설명했다.[^nickg-anthropic-shard]

Anthropic이 Twitter에 글을 소개하며 앞세운 것도 이 숫자였다.
5월 하루 약 2,500개이던 병합이 9월 3만 개를 넘었고,
사람 규모에 맞춰 만든 개발 인프라가 병목이 되어
새 버전 관리 시스템을 만들고 모노레포를 Git에서
다섯 달 만에 옮겼다고 썼다.[^AnthropicAI]
이 트윗은 550만 회 넘게 조회됐고, 답글은 숫자 자체를 비꼬는 쪽으로 몰렸다.
Natural Stupidity는 하루 3만 개가 병합된다는데
자기는 3월부터 README 오타 수정 PR 하나가 열려 있다고 했다.[^NattyStupidity]
Ed는 결국 main 브랜치에서 FTP로 작업하는
방식을 발명한 것이냐고 물었고,[^edinwaw]
azim은 회사에서 가장 귀찮은 동료가
우리도 이렇게 하자고 제안할 날이 기다려진다고 했다.[^_azims]
Ed의 농담은 병합 큐를 버리고 병합 후 테스트로 옮긴 구조를,
azim의 농담은 Anthropic 규모에서만 성립하는 결정이
규모가 다른 조직에 그대로 옮겨질 위험을 꼬집는다.

### 7명이 5개월 만에 만들었다는 서사의 조건이 숨어 있다

7명이 소스 관리 시스템, 리뷰 도구,
관련 시스템 여섯 개를 5개월 만에 만들었다는 대목은
글에서 가장 인상적인 주장이다.
그러나 이 팀은 출시 전 내부 스냅숏인 Claude Mythos Preview를 썼고,
토큰을 사실상 무제한으로 쓸 수 있었으며,
Piper와 Sapling이라는 검증된 설계를 참고할 수 있었다.
또 Spanner와 클라우드 저장소, 내부 IAM 같은 기반이 이미 있었다.

이 조건을 빼고 “작은 팀의 빠른 개발이 흔해질 것”이라고 일반화하면
다른 조직이 같은 기대를 품게 된다.
글이 공개하지 않은 것은 이 프로젝트에 쓴 토큰 비용과
같은 일을 공개 모델로 했을 때의 결과다.

bob1029는 순수한 Git과 자체 버전 관리 시스템 사이에 단계가 많은데
글이 Git으로는 정말 안 된다는 점을 설득하지 못했다고 비판했다.[^bob1029]
ragtagtag는 CI/CD 문제를 버전 관리를 바꿔서 풀었다며,
가장 잘 다듬어진 부분을 덜 다듬어진 것으로 바꾸고
위태로운 나머지는 그대로 두었다고 꼬집었다.[^ragtagtag]
저자는 Git 앞에 API를 두는 방식이 단순해
보여도 저장소 유지보수를 위한 repack 같은
운영상의 문제가 많다고 답했다.[^nickg-anthropic-repack]
zmmmmm이 모노레포 자체를 재고했어야 하지 않느냐고 묻자,[^zmmmmm]
저자는 모노레포가 일관된 도구 기반을 주고 수천 개 저장소에 걸친 캠페인 대신
원자적 커밋 하나로 대규모 변경을 할 수 있게
해 준다고 답했다.[^nickg-anthropic-monorepo]

### 사람의 역할에 대한 설명이 구체적이지 않다

글은 엔지니어의 역할이 Claude에게 “아니”라고 말하는 것이라고 하고,
그 예로 main 병합 시점을 커밋 로그를 선형으로 읽어 찾으려던 시스템과,
적대적 리뷰가 다른 내부 서비스를 과하게 의심해 불필요한 검증을 추가한 일을 든다.
이 예시는 흥미롭지만, 사람이 그런 판단을 내리려면
무엇을 알아야 했는지는 설명하지 않는다.

모든 엔지니어가 Claude가 자기보다 코드를 잘 쓴다고 평가하는 조직에서
그 판단력이 어떻게 유지되고 다음 세대에게 전해지는지가
이 구조의 지속 가능성을 결정한다.
코드를 직접 쓰지 않는 엔지니어가 시스템 제약을 몸으로 아는 상태를
얼마나 오래 유지할 수 있는지에 대해 글은 답하지 않는다.

duttish는 Claude의 코드 리뷰를 멈출 때마다 나중에 엉성한 코드를 발견한다며,
의도만 리뷰하는 속도에서 그런 코드를 어떻게 걸러 내는지,
아니면 그냥 받아들이는지 물었다.[^duttish]
Lobste.rs의 emk는 더 날카롭게,
터미널 그리기 버그가 고쳐졌다가 일주일 뒤 다시 나타나는 Claude Code를 예로 들며
버전 관리처럼 신뢰성이 중요한 소프트웨어를
그런 방식으로 만드는 것이 불안하다고 했다.[^emk]

LinkedIn에서도 여러 의견이 나왔다.
Jooeon Kim은 이 일을 병목이 사람에서
사람에 맞춰진 기존 시스템으로 넘어가는 신호로 읽고,
아직 사람이 코드를 검수하는 단계라면 뒤처진 것이라고 봤다.[^kimjooeon]
이준승은 기존 개발 시스템이 AI 기반 패턴으로 바뀌면서
사람용으로는 채팅창 하나만 남을 것 같다고 했고,[^leejunseung-chat]
Jung Min Kang은 누구를 위한 것인가가
앞으로의 과제가 될 것 같다고 했다.[^jungminkang]
원문은 사람이 모든 변경을 여전히 리뷰하되 의도를 본다고 설명하므로,
사람의 검수가 빠진다는 읽기와는 거리가 있다.

### Git 생태계에 대한 제안이 추상적이다

마지막 절은 Git 서버 구조, 표준화된 서버 측 RPC,
새로운 협상 프로토콜 같은 개선 방향을 제시하며
GitHub, GitLab, 오픈소스 커뮤니티와 협력하겠다고 한다.
그러나 구체적인 명세나 코드, 협력 계획은 없다.
Scion을 공개하지 않는 이유로 다른 조직이 쓰기 어렵다는 점을 들지만,
그렇다면 공유할 수 있는 부분,
예를 들어 협상 프로토콜이나 파생 데이터 메커니즘의 명세를
따로 공개하는 방법도 있었다.

Lobste.rs의 zg도 코드는 하나도 공유하지 않으면서 긴 기술 글을 쓰는 이유를 모르겠다며,
비슷한 글을 쓰면서 Sapling을 공개한 Meta와 대조했다.[^zg]
prime은 직접 만들기 전에 다른 버전 관리 시스템을 어떻게 검토했는지,
그 비교와 트레이드오프를 보고 싶었다고 했다.[^prime]

## 인사이트

### 에이전트 규모의 병목은 소스 관리에서 끝나지 않는다

소스 관리를 고치면 병목은 다음 단계로 옮겨 간다.
글이 이미 병합 큐와 CI를 언급하듯, 다음은 빌드, 테스트, 배포, 관측이다.
하루 3만 개의 변경이 병합된다면 하루 3만 번 배포 판단이 필요하고,
사고가 났을 때 원인이 된 변경을 찾는 일도 그만큼 어려워진다.
글이 자동 bisect와 revert 파이프라인을 언급하는 것은 이 흐름의 예고다.

kburman은 AI로 코드가 싸지면서 작은 스타트업도
바퀴를 다시 발명하는 일이 늘 것이라며,
그 맞춤 소프트웨어를 유지하는 비용도 싸게
유지될지는 별개의 문제라고 했다.[^kburman]

이 흐름은 제조업의 병목 이론과 같다.
한 공정의 처리량을 높이면 그 다음 공정이 병목이 되고,
전체 처리량은 가장 느린 공정이 정한다.
에이전트가 코딩 공정을 거의 무한하게 만들었으므로,
개발 조직의 성과는 이제 그 뒤의 공정들이 얼마나 빨리 따라오느냐로 정해진다.
[코드는 30% 늘었지만 소프트웨어는 늘지 않았다](../agentic-coding/more-code-not-more-software.md)는
관찰도 같은 병목 이동을 다른 각도에서 본 것이다.

### 개발 도구의 승자는 클라이언트가 아니라 서버를 가진 쪽이 된다

Scion의 설계는 계산을 서버로 옮기고 클라이언트를 얇게 만든다.
이 방향이 일반화되면 개발 도구의 무게 중심도 옮겨 간다.
Git은 누구나 서버를 띄울 수 있고 클라이언트가 모든 것을 계산할 수 있어서
특정 호스팅 업체에 종속되지 않았다.
서버 측 RPC가 표준이 되면 저장소 질의, blame, 병합을 서버가 맡게 되고,
그 서버를 운영하는 쪽의 영향력이 커진다.

글이 제안한 “포지(forge) 간 표준 서버 RPC”는 이 종속을 줄이는 장치가 될 수 있다.
반대로 표준이 만들어지지 않으면 GitHub, GitLab 같은 호스팅 업체가
각자 다른 API로 에이전트 규모의 기능을 제공하게 되고,
저장소를 옮기는 비용은 지금보다 훨씬 커진다.

LinkedIn의 이준승은 이제 GitHub가 버전 관리보다
SNS나 앱스토어가 되어 버렸다고 했다.[^leejunseung-github]
버전 관리의 계산이 서버로 옮겨 가면,
호스팅 업체가 차별화할 지점은
저장소 기능보다 그 위의 사회적 기능과 배포 채널이 된다.

cometkim은 Anthropic의 트윗을 인용하며
“이럴 거면 왜 Git 쓰지”의 시대가 돌아왔다고 했다.
그러면서 이 시대를 기다리던 비즈니스들은
이미 말라 죽어서 없다고 덧붙였다.[^cometkim]
Perforce처럼 서버 중심 버전 관리를 팔던 회사와
Git 이후의 대안을 내놓던 도구들은 Git의 표준화 앞에서 자리를 잃었다.
이제 수요가 돌아왔지만, 그 수요를 가진 회사는
Anthropic처럼 직접 만들 능력도 함께 가졌다.
서버 중심 버전 관리가 다시 필요해진 시점에
그것을 사 줄 고객은 이미 스스로 만드는 쪽으로 옮겨 간 셈이다.

### 오프라인 개발의 가치가 사람에게만 남는다

Git이 분산 시스템이 된 이유 중 하나는
네트워크가 느리고 불안정하던 시절 개발자가 어디서든 일할 수 있게 하는 것이었다.
에이전트가 대부분의 코드를 쓰게 되면 그 가치는 사람에게만 남는다.
Scion은 이 비대칭을 받아들여 서버 중심으로 설계했다.

이 선택은 장애 때 드러난다.
Git에서는 서버가 죽어도 각자의 클론으로 계속 일할 수 있었지만,
Scion에서는 서버가 이력과 병합을 계산하므로 서버 장애가 곧 개발 중단이다.
글이 계층 캐시와 장애 영역 분리를 강조하는 이유다.
에이전트 규모의 효율을 얻는 대가로 개발 전체가
중앙 인프라의 가용성에 묶이는 구조가 된다.

### 리뷰는 코드를 읽는 일에서 의도를 승인하는 일로 바뀐다

글에서 지나가듯 언급된 변화 중 가장 큰 것은 리뷰다.
사람은 모든 변경을 리뷰하지만 줄 단위가 아니라 의도를 본다.
리뷰 도구는 변경의 의미를 분류해 사람의 주의를 배분한다.
이것은 리뷰의 목적을 “코드가 맞는가”에서 “이 변경을 원하는가”로 바꾼다.

이 전환이 성공하려면 의도를 확인하는 것만으로 충분하다는 보장이 필요하다.
그 보장은 시뮬레이션, 퍼징, 병합 후 테스트, 자동 롤백 같은 장치에서 온다.
글이 Scion을 “가장 잘 테스트된 코드베이스”라고 강조하는 것은 우연이 아니다.
사람이 코드를 읽지 않는 만큼 테스트가 그 자리를 채워야 하고,
테스트를 쓰는 것도 Claude라면 결국 사람이 확인할 수 있는 것은
테스트가 무엇을 검증하는지에 대한 설계뿐이다.

## 다른 조직에서 검증할 조건

Scion의 성과를 재현하려면 먼저 병합량이 아니라
저장소 운영의 실제 병목을 확인해야 한다.
클론과 체크아웃에 드는 시간,
CI가 전송하는 데이터,
서버 질의의 지연과 장애가 현재 비용을 얼마나 차지하는지 측정한다.
그 수치가 작다면 중앙 서버로 옮겨 얻는 이익보다
새 시스템의 구축과 운영 비용이 더 클 수 있다.

시험 이전에서는 일상 개발, 대규모 자동화 변경,
서버 장애와 복구를 각각 따로 연습한다.
에이전트가 온라인이라는 가정이 깨지는 상황,
개발자가 전체 이력에 접근해야 하는 상황,
Git 생태계 도구와의 호환이 필요한 상황을
성공 기준에 포함해야 한다.

따라서 Scion은 모든 팀에 권할 Git 대체품이 아니라
온라인 모노레포와 높은 자동화 처리량을 가진 조직을 위한
특수한 설계 사례로 읽는 편이 정확하다.
적용 가능성은 코드 생성량이 아니라
서버 의존을 감당할 수 있는지,
대체 경로와 복구 시간이 요구 수준을 만족하는지로 판정해야 한다.

---

[^tancop]: <https://news.ycombinator.com/item?id=50076658>

[^cube00]: <https://news.ycombinator.com/item?id=50077008>

[^steveklabnik]: <https://news.ycombinator.com/item?id=50075405>

[^amluto]: <https://news.ycombinator.com/item?id=50075586>

[^nickg-anthropic-hash]: <https://news.ycombinator.com/item?id=50078963>

[^nickg-anthropic-offline]: <https://news.ycombinator.com/item?id=50079495>

[^joshheitzman]: <https://news.ycombinator.com/item?id=50076046>

[^nickg-anthropic-wider]: <https://news.ycombinator.com/item?id=50079916>

[^nickg-anthropic-what]: <https://news.ycombinator.com/item?id=50081892>

[^nickg-anthropic-conflict]: <https://news.ycombinator.com/item?id=50082255>

[^altcognito]: <https://news.ycombinator.com/item?id=50077231>

[^nickg-anthropic-shard]: <https://news.ycombinator.com/item?id=50078883>

[^bob1029]: <https://news.ycombinator.com/item?id=50078314>

[^ragtagtag]: <https://news.ycombinator.com/item?id=50083082>

[^nickg-anthropic-repack]: <https://news.ycombinator.com/item?id=50080629>

[^zmmmmm]: <https://news.ycombinator.com/item?id=50079137>

[^nickg-anthropic-monorepo]: <https://news.ycombinator.com/item?id=50080247>

[^duttish]: <https://news.ycombinator.com/item?id=50082912>

[^kburman]: <https://news.ycombinator.com/item?id=50075611>

[^fzakaria]: <https://lobste.rs/s/5ucftp/redesigning_source_control_at_anthropic#c_xgqqig>

[^zg]: <https://lobste.rs/s/5ucftp/redesigning_source_control_at_anthropic#c_nyyjha>

[^prime]: <https://lobste.rs/s/5ucftp/redesigning_source_control_at_anthropic#c_zsohvz>

[^emk]: <https://lobste.rs/s/5ucftp/redesigning_source_control_at_anthropic#c_mpdtps>

[^dudnspa0203]: <https://news.hada.io/topic?id=35309#cid67628>

[^AnthropicAI]: <https://twitter.com/AnthropicAI/status/2110047081414987957>

[^NattyStupidity]: <https://twitter.com/NattyStupidity/status/2110051706939793645>

[^edinwaw]: <https://twitter.com/edinwaw/status/2110053206260916412>

[^_azims]: <https://twitter.com/_azims/status/2110068676456006142>

[^cometkim]: <https://twitter.com/cometkim/status/2110308594310873322>

[^kimjooeon]: LinkedIn, [Jooeon Kim의 #scion 게시물](https://www.linkedin.com/posts/kimjooeon_scion-share-7515929354011586560-j3LX/)

[^seokwonyoon]: LinkedIn, [Jooeon Kim의 #scion 게시물](https://www.linkedin.com/posts/kimjooeon_scion-share-7515929354011586560-j3LX/)에 seok won yoon이 쓴 댓글

[^leejunseung-chat]: LinkedIn, [Jooeon Kim의 #scion 게시물](https://www.linkedin.com/posts/kimjooeon_scion-share-7515929354011586560-j3LX/)에 이준승이 쓴 댓글(채팅창)

[^jungminkang]: LinkedIn, [Jooeon Kim의 #scion 게시물](https://www.linkedin.com/posts/kimjooeon_scion-share-7515929354011586560-j3LX/)에 Jung Min Kang이 쓴 댓글

[^leejunseung-github]: LinkedIn, [Jooeon Kim의 #scion 게시물](https://www.linkedin.com/posts/kimjooeon_scion-share-7515929354011586560-j3LX/)에 이준승이 쓴 댓글(GitHub)
