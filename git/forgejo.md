# Forgejo: 비영리가 운영하는 가벼운 자체 호스팅 포지

<https://forgejo.org/>

HN 토론: <https://news.ycombinator.com/item?id=42753523> (391점, 269개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/giyb8x/forgejo_v16_0_is_available>

## 소개

Forgejo는 자신을 “self-hosted lightweight software forge”라고 소개한다.
슬로건은 “Beyond coding. We forge.”이고, 설치가 쉽고 유지 부담이 낮으며 그저 제 일을 한다는 것이
첫 문단의 요지다.

이 프로젝트는 Codeberg e.V.라는 민주적 비영리 조직 아래에 있다.
홈페이지는 그 사실을 신뢰의 근거로 내세운다 — Forgejo는 전적으로 자유 소프트웨어임을 신뢰할 수
있다는 것이다.
Codeberg나 다른 공개 인스턴스에 계정을 만들 수도 있고, 직접 내려받아 자체 호스팅할 수도 있다.
보안, 확장성, 연합(federation), 프라이버시에 초점을 둔다고 밝힌다.

홈페이지가 내세우는 것은 여섯 가지다.
협업과 생산성을 위해 설계된 사용 경험, GitHub 사용자에게 익숙한 환경을 제공하는 자체 호스팅
대안, 전문 기술 없이도 가능한 설치와 유지, 풍부한 기능에도 다른 포지보다 한 자릿수 적은 자원을
요구하는 낮은 서버 부담, 영구적인 100% 자유 소프트웨어 보장, 그리고 탈중앙 플랫폼으로 협업
소프트웨어 개발을 가능케 하겠다는 지향이다.

기여 경로는 현지화, 코드와 연합과 릴리스 관리, 사용자 조사, UX, 커뮤니티 관리, 문서, 웹 디자인,
거버넌스로 나뉘어 있다.
개발은 Codeberg 위에서 이루어지고 후원은 Liberapay로 받는다.

## Gitea 포크와 GPL 재라이선싱

Forgejo는 2022년 12월 Codeberg가 Gitea를 포크해 시작했다.
계기는 기능이 아니라 소유 구조였다.
Gitea 측이 영리 법인을 세워 기업 대상 맞춤 기능을 만들기로 한 것이 발단이었고[^geek_at],
KingMob이 정리한 대로 이는 MIT 라이선스가 허용하는 무임승차자 앞에서 재정을 감당하지 못한 FOSS
메인테이너들의 또 하나의 사례이기도 했다[^KingMob].

2024년 8월 Forgejo는 GPL로 재라이선싱했다.
발표문의 제목은 “Forgejo is now copyleft, just like Git”이었다.
Lobste.rs에서 PuercoPop은 커뮤니티를 세우려는 프로젝트에게 카피레프트가 옳은 선택이라며
환영했다[^PuercoPop].
그 논거를 두고 steveno와 yawaramin 사이에 긴 공방이 이어졌는데, 카피레프트가 이념적으로 움직이는
사람을 더 끌어들인다는 주장[^yawaramin]에 steveno는 그것이 근거 없는 희망 아니냐고 되물었고,
카피레프트가 더 낫다는 증거도 더 못하다는 증거도 없다고 정리했다[^steveno].

## 릴리스와 채택 현황

현재 최신 버전은 v16.0.2(2026-07-30)다.
v16.0.0이 2026년 7월 16일에 나왔고, v15 계열도 같은 날 v15.0.6으로 유지 보수됐다.
v16에서는 다중 행 리뷰, 리뷰 코멘트 배치 개선, 세분화된 watch 설정 같은 것들이 들어갔다.

조직 단위 채택 사례가 쌓였다.
Fedora 프로젝트가 Pagure에서 Forgejo로 옮기기로 했고[^nikodunk], FFmpeg도 Forgejo로 이동했다.
개인 사례는 더 많다 — eeue56는 GitHub에 있던 저장소 500개를 k8s 안의 Forgejo와 러너로 옮겼고
이주가 거의 고통 없었다고 했다[^eeue56].

## 분석

### 이 포크는 코드에 대한 불만이 아니라 신뢰에 대한 불만이었다

Forgejo가 Gitea에서 갈라진 이유를 코드에서 찾으면 아무것도 찾지 못한다.
homebrewer는 하드 포크 직후 다시 평가해 봤을 때 몇 가지 외형적 차이를 빼면 사실상 차이가
없었다고 했다[^homebrewer].
그런데도 사람들이 옮겼다.

blacklight의 설명이 가장 직접적이다 — Gitea가 VC 자금을 받은 영리 조직을 분사하면서 신뢰를
잃었고, 그것이 애초에 GitHub을 떠난 이유와 정확히 같은 것이었다는 것이다[^blacklight].
GitHub이 Microsoft에 인수된 것을 이유로 자체 호스팅으로 옮긴 사람에게, 자체 호스팅 소프트웨어가
같은 경로를 밟기 시작하는 것은 이주 자체를 무의미하게 만든다.

lolinder는 논점을 더 밀었다 — FOSS는 비즈니스 모델이었던 적이 없고 앞으로도 아니라는 것이다.
자유 소프트웨어는 애초에 지속 가능한 개발이 아니라 사용자의 자유를 목표로 한 윤리 운동이었으므로
수입원을 우선할 필요가 없었다고 봤다[^lolinder].
nirui는 반대편에서 읽었다 — 많은 오픈소스 개발자가 15~20년 전처럼 오픈소스가 잘 벌리는 본업을
가진 취미 개발자들의 작업이라고 여기는 착각에 빠져 있고, 상황을 제대로 읽은 것은 GitLab이라는
것이다[^nirui].

이 두 입장 사이에 Codeberg e.V.라는 답이 있다.
영리도 취미도 아닌 민주적 비영리 법인이라는 형태 자체가 Forgejo의 제품 사양 중 하나다.

### GPL 전환은 그 신뢰 문제를 라이선스로 잠근 것이다

포크만으로는 재발을 막지 못한다.
MIT로 남아 있는 한 다음번 무임승차와 다음번 영리 분사가 다시 가능하다.
2024년의 GPL 전환은 그 구멍을 닫는 조치였고, “Git처럼 카피레프트”라는 표현은 카피레프트를 꺼리는
기업을 향한 방어 논리이기도 했다.

pcrock은 그 문장의 기능을 정확히 짚었다 — 라이선스 호환성이 카피레프트 선택의 이유였다기보다,
카피레프트 알레르기가 있는 기업들이 Forgejo를 그만 쓸까 걱정해서 “Git을 쓸 수 있다면 Forgejo도
계속 쓸 수 있다”는 논증을 만든 것으로 읽었다[^pcrock].

그런데 그 논증에는 결함이 있다.
nia가 지적한 대로, Git과의 라이선스 호환성을 근거로 들면서 실제로는 Git의 라이선스와 호환되지
않는 GPL 버전을 골랐다 — Git은 GPLv2 단독이고 Forgejo가 택한 것은 GPLv3 계열이다[^nia].
수사로는 통하지만 법적으로는 통하지 않는 문장이었던 셈이다.

### 경량성은 마케팅 문구가 아니라 실제 이주 동기였다

“다른 포지보다 한 자릿수 적은 자원”이라는 주장은 검증 가능한 형태로 여러 번 확인된다.

jwildeboer는 GitLab CE를 살려 두려 애쓰다 포기한 뒤 Forgejo로 옮겼고, 루트리스 컨테이너로
돌면서 메모리와 CPU를 거의 쓰지 않으며 업데이트는 `podman pull` 한 번이면 된다고 했다[^jwildeboer].
HankB99은 Atom 기반 서버에 GitLab CE를 올렸다가 페이지 로드가 타임아웃되는 지경을 겪었고
Gitea로 옮긴 것이 숨통이었다고 했다[^HankB99].
kstrauser는 Gogs에서 Gitea로, 다시 Forgejo로 옮겨 온 이력을 밝히며, 개인 저장소 90%는 그냥 SSH
서버로 충분하지만 친구들과 비공개로 코드를 나누는 나머지 10%에서 훌륭하다고 평가했다[^kstrauser].

이것이 Forgejo와 [Radicle](radicle.md) 같은 P2P 접근의 결정적 차이다.
Radicle은 프로토콜을 바꿔 문제를 풀려 하고, Forgejo는 이미 익숙한 모델을 훨씬 싸게 돌아가게 만들어
문제를 푼다.
전자는 세계관을 바꾸라고 요구하고, 후자는 서버 한 대만 요구한다.
채택 실적의 차이가 여기서 나온다.

## 비평

### 연합은 창립 강령이었지만 아직 없다

홈페이지는 지금도 연합을 초점 중 하나로 적고 있고, 마지막 문단은 탈중앙 플랫폼으로 협업 개발을
가능케 하겠다고 말한다.
그러나 2022년 창립 이후 그것은 계속 미래 시제였다.

lloeki는 2025년 초 시점에 Forgejo의 흥미로운 측면으로 진행 중인 연합 작업을 들었고, 이상적으로는
GitHub과 GitLab도 연합을 지원해야 하지만 그럴 일은 없을 것이라고 봤다[^lloeki].
DicIfTEx는 더 냉정하다 — 웹사이트의 연합 페이지는 2023년 1월 것으로 오래됐고 링크 대부분이
깨졌으며, 연례 진행 보고서도 2023년까지만 나오다 그 사이트마저 접근되지 않는다고 했다[^DicIfTEx].
jimjimwii은 연합 지원 상태를 물으며 인스턴스 간 PR과 버그 리포트가 되면 협업이 훨씬 쉬워질
것이라고 했지만[^jimjimwii], 그 질문은 스레드에서 답을 받지 못했다.

franga2000는 원인을 다른 데서 찾았다.
요즘 “연합”이 사실상 “ActivityPub 구현”과 동의어가 되어 버려서, 많은 프로젝트가 자기 데이터
모델을 AP에 어떻게 대응시킬지 논쟁하고 확장 제안을 쓰는 복잡한 늪에 빠진다는 것이다[^franga2000].
Forgejo 인스턴스들 사이의 유용한 연합에 그 표준이 꼭 필요하지는 않은데, 표준을 통과하려다 아무것도
못 내놓게 된 형국이다.

이 지적은 [Forge 연합이 필요하다](../github/forge-federation.md)의 논지와 정면으로 만난다.
연합의 필요성에는 광범위한 합의가 있고, 4년째 구현이 없다는 것도 사실이다.
그렇다면 문제는 동기가 아니라 난이도이며, 홈페이지가 그것을 진행 중인 초점처럼 적는 것은
정직하지 않다.

### 자기를 설명하지 못하는 것이 이 프로젝트의 만성 결함이다

HN 스레드에서 반복적으로 올라온 불만은 기능이 아니라 첫 화면이었다.

jmpavlec은 태그라인이 별로 정보를 주지 않으며, 자체 호스팅 GitHub 대안이라는 목적을 파악하기까지
한두 번 스크롤해야 했다고 했다 — 소프트웨어 맥락에서 “forge”라는 단어는 다양하게 해석될 수 있으니
더 앞에서 분명히 하라는 조언이었다[^jmpavlec].
andsoitis는 FAQ의 “Forgejo는 자체 호스팅 경량 소프트웨어 포지입니다”라는 자기 순환적 답변을 그대로
인용하며 물음표를 남겼다[^andsoitis].
tmountain도 첫 화면만 보고는 이게 정확히 무엇인지 확신할 수 없다고 했다[^tmountain].

이름 문제도 컸다.
thiht는 발음조차 못 하는 도구 대신 Gitea를 설치할 것이라고 했고 포크 이유도 빈약하다고
봤다[^thiht].
TNorthover는 커뮤니케이션이 총체적으로 산만하고 영어권에서 이름이 어색하다고 지적했다 — 에스페란토
이름이라지만 사이트의 다른 어떤 것도 에스페란토가 아니니 대부분의 사람은 그렇게 읽지 않는다는
것이다[^TNorthover].
criticalfault의 요약이 가장 짧다 — 프로젝트는 훌륭하고 이름은 끔찍하다[^criticalfault].

방어 논리는 두 가지 나왔다.
yawaramin은 GitHub이나 GitLab을 언급하지 않고 그것들이 무엇인지 설명해 보라고 되물었고[^yawaramin-desc],
baobun은 GitHub을 범주 정의자로 대하는 것 자체가 Forgejo 정신에 반하며 Forgejo는 스스로 서 있다고
했다[^baobun].
stevekemp은 “forge”가 SourceForge 이래로 이런 종류의 호스팅 패키지를 가리키는 말로 쓰여 왔다고
역사를 짚었다[^stevekemp].

이 방어들은 옳지만 대가가 있다.
정체성을 지키려고 사용자 이해를 희생하는 선택이며, 그것이 신규 사용자 유입에서 얼마를 비용으로
치르는지는 프로젝트가 측정하지 않는다.
그리고 이 프로젝트에게 신규 사용자 유입은 부차적인 지표가 아니다 — 앞 절에서 본 대로 연합이
없는 상황에서 채택은 순전히 개별 설치의 누적으로만 늘어난다.

### GitHub의 리뷰 모델을 물려받은 대가를 아직 치르고 있다

Forgejo의 강점으로 꼽히는 “GitHub 사용자에게 익숙한 환경”은 동시에 한계다.
bjackman은 최근 GitHub에서 제법 진지한 코드 리뷰를 하다가 그것이 리뷰 도구의 유아용 장난감
버전임을 알게 됐다고 했고, 소스 관리 모델 전체를 그것에 맞춰 설계하지 않으면 진지한 엔지니어링에는
쓸 수 없어 보인다고 평가했다[^bjackman].
prakashn27는 Meta 내부 도구의 계층형 PR 같은 기능을 어디에서도 못 봤다고 아쉬워했고[^prakashn27],
lima는 패치를 주고받는 방식보다 Gerrit식의 커밋 하나가 리뷰 단위 하나가 되는 접근이 UX가 훨씬
낫다고 정리했다[^lima].

Forgejo는 Gitea를 통해 GitHub의 리뷰 모델을 그대로 물려받았으므로 이 한계도 함께 물려받았다.
v16에서 다중 행 리뷰와 리뷰 코멘트 배치가 개선된 것[^nicoco]은 반가운 일이지만, 그것이 2026년에
들어왔다는 사실이 격차의 크기를 말해 준다.

여기에 구조적 딜레마가 있다.
GitHub과 다른 리뷰 모델을 도입하면 “익숙한 환경”이라는 이주 유인이 약해지고, 같은 모델을 유지하면
리뷰 품질에서 GitHub을 넘어설 이유가 없어진다.
“Beyond coding, we forge ahead”라는 문구가 무엇을 넘어서겠다는 것인지 이 지점에서 가장 불분명하다.

## 인사이트

### 포크의 진짜 자산은 코드가 아니라 법인 형태다

Gitea와 Forgejo의 코드가 갈라진 직후 거의 같았다는 사실[^homebrewer]과, 그럼에도 사람들이 옮겼다는
사실을 나란히 놓으면 이렇게 정리된다 — 이 포크가 실제로 복제한 것은 소스가 아니라 소유 구조다.

이것은 오픈소스 포크의 성격이 바뀌었다는 신호다.
전통적으로 포크는 기술적 이견에서 나왔다 — 방향이 다르니 갈라진다.
Gitea에서 Forgejo로, Terraform에서 OpenTofu로, Redis에서 Valkey로 이어지는 최근의 포크들은
기술적 이견이 아니라 라이선스와 지배 구조에서 나왔다.
코드는 그대로 두고 소유 구조만 바꾸는 것이 목적이었다.

그렇다면 포크의 성공 여부를 판단하는 기준도 달라져야 한다.
“기능이 더 좋은가”가 아니라 “이 법인 형태가 다음 10년을 견딜 것인가”다.
Codeberg e.V.라는 민주적 비영리는 후자에 대한 답이고, GPL 전환은 그 답을 코드에까지 새긴
것이다 — 다만 그 새김이 Git과의 호환성을 잘못 주장했다는 흠[^nia]을 남겼다.

같은 기준이 지금 진행 중인 다른 이동에도 적용된다.
[Cursor Origin](../cursor/cursor-origin.md)에 대한 거부 반응의 대부분이 기능이 아니라 소유자를 향한
것이었던 이유가 바로 이것이다.
사용자들이 포지를 고를 때 이미 코드가 아니라 법인을 본다.

### 워크플로 포맷의 호환성이 이주를 가능하게 하면서 GitHub의 설계를 영속화한다

eeue56의 이주 보고에서 결정적인 문장은 저장소 500개가 아니라 그다음이다 — Forgejo Runner가
GitHub Actions와 같은 워크플로 정의를 쓰기 때문에, 로컬 러너용 레이블만 올바르게 만들면
됐다는 것이다[^eeue56].

이 한 가지 호환성이 자체 호스팅 이주의 실질적 관문이었다.
저장소와 이슈는 API로 옮길 수 있지만 CI 파이프라인은 재작성 대상이고, 그 재작성 비용이 조직 단위
이주를 막는 가장 큰 항목이었다.
Forgejo Actions는 그 항목을 0에 가깝게 만들었다.

그런데 이것은 GitHub의 워크플로 문법이 사실상 업계 표준이 되었음을 뜻하기도 한다.
호환 계층은 이주를 열어 주는 동시에 그 설계를 영속화한다 — GitHub을 떠나도 GitHub이 정한 형식으로
CI를 쓰게 된다.
[Cursor Origin](../cursor/cursor-origin.md)이 워크플로 포맷을 통해 락인을 만들려 한다는 관측과
같은 구조가 여기서는 반대 방향으로 작동하는 것이다.

장기적 함의는 양날이다.
포맷이 공용재가 되었으므로 어떤 호스팅으로든 옮길 수 있고, 동시에 어떤 호스팅도 그 포맷의 결함을
고치기 어렵다.
호환성을 깨는 개선은 이주 유인을 스스로 없애는 일이 되기 때문이다.

### 조직은 자체 호스팅으로 갈 수 있지만 개인은 갈 수 없다

Fedora와 FFmpeg가 옮길 수 있었던 이유는 서버를 감당할 수 있어서가 아니다.
커뮤니티가 이미 그들에게 있기 때문이다.
Fedora 기여자는 Fedora가 어디에 있든 따라가고, FFmpeg에 패치를 보내려는 사람은 그것이 어느 포지에
있든 계정을 만든다.

개인에게는 그 조건이 없다.
[Radicle](radicle.md) 스레드에서 einpoklum이 함께 시도할 사람을 찾기 어렵다고 한 것과 같은 문제다.
kstrauser가 개인 저장소 90%는 SSH 서버로 충분하고 나머지 10%가 친구들과 비공개로 나눌 때라고 한
것[^kstrauser]은 이 조건을 정확히 반영한 사용 패턴이다 — 자체 호스팅 포지의 개인 사용은 공개
협업이 아니라 사적 공유에 최적화되어 있다.

그래서 연합의 부재가 계층별로 다르게 작용한다.
조직에게 연합은 편의 기능이고, 개인에게는 존재 조건이다.
공개 프로젝트를 자체 호스팅 인스턴스에 올려 두고 외부 기여를 받으려면, 기여자가 그 인스턴스에
계정을 만들어야 하고 그 마찰이 대부분의 기여를 죽인다.
Forgejo의 채택 곡선이 조직 사례와 홈랩 사례로 양극화되어 있고 중간이 비어 있는 것은 이 때문이다.

### 자체 호스팅의 비용 구조가 AI 크롤러 때문에 바뀌었다

Forgejo와 관련해 HN에서 189점을 받은 게시물 중 하나는 기능 발표도 채택 사례도 아니었다 — 자기
Forgejo 인스턴스를 AI 웹 크롤러로부터 지키는 방법이었다.

이것은 “한 자릿수 적은 자원”이라는 Forgejo의 핵심 소구점을 근본에서 흔든다.
가벼운 포지의 전제는 트래픽이 사람 규모라는 것이었다.
Git 저장소의 웹 인터페이스는 커밋마다, 파일마다, diff마다 URL을 만들어 내므로 크롤러에게는 사실상
무한한 페이지 공간이고, 대규모 스크래핑 앞에서 Atom 서버 한 대짜리 배포는 성립하지 않는다.

여기에 역설이 있다.
자체 호스팅으로 옮기는 동기 중 하나는 자기 코드가 학습 데이터로 쓰이는 것에 대한 거부감인데,
자체 호스팅은 바로 그 스크래핑을 자기 비용으로 막아야 하는 처지를 만든다.
GitHub에 있으면 크롤러 대응 비용은 GitHub이 내고, 대신 학습 데이터 제공에는 동의하게 된다.
자체 호스팅은 동의를 거두는 대가로 방어 비용을 인수하는 거래다.

중기적으로 이것은 Codeberg 같은 공용 인스턴스의 역할을 키울 것이다.
크롤러 방어에는 규모의 경제가 작동하므로, 개인 인스턴스보다 비영리가 운영하는 공용 인스턴스가
유리해진다.
그렇다면 Forgejo 생태계의 무게 중심은 자체 호스팅에서 Codeberg로 이동할 가능성이 있고, 그것은
탈중앙을 지향하며 시작한 프로젝트가 다시 중앙 인스턴스에 기대게 되는 경로다.
연합이 완성되지 않는 한 이 경로를 막을 방법이 없다.

---

[^geek_at]: <https://news.ycombinator.com/item?id=42758617>
[^KingMob]: <https://news.ycombinator.com/item?id=42756453>
[^nikodunk]: <https://news.ycombinator.com/item?id=42754236>
[^eeue56]: <https://lobste.rs/s/giyb8x/forgejo_v16_0_is_available#c_cceqpy>
[^homebrewer]: <https://news.ycombinator.com/item?id=42755732>
[^blacklight]: <https://news.ycombinator.com/item?id=42755375>
[^lolinder]: <https://news.ycombinator.com/item?id=42756871>
[^nirui]: <https://news.ycombinator.com/item?id=42756865>
[^jwildeboer]: <https://news.ycombinator.com/item?id=42755584>
[^HankB99]: <https://news.ycombinator.com/item?id=42758956>
[^kstrauser]: <https://news.ycombinator.com/item?id=42754131>
[^lloeki]: <https://news.ycombinator.com/item?id=42755416>
[^DicIfTEx]: <https://news.ycombinator.com/item?id=42755647>
[^jimjimwii]: <https://news.ycombinator.com/item?id=42757922>
[^franga2000]: <https://news.ycombinator.com/item?id=42755625>
[^jmpavlec]: <https://news.ycombinator.com/item?id=42753966>
[^andsoitis]: <https://news.ycombinator.com/item?id=42753932>
[^tmountain]: <https://news.ycombinator.com/item?id=42755096>
[^thiht]: <https://news.ycombinator.com/item?id=42755500>
[^TNorthover]: <https://news.ycombinator.com/item?id=42754725>
[^criticalfault]: <https://news.ycombinator.com/item?id=42755434>
[^yawaramin-desc]: <https://news.ycombinator.com/item?id=42754032>
[^baobun]: <https://news.ycombinator.com/item?id=42754121>
[^stevekemp]: <https://news.ycombinator.com/item?id=42754922>
[^bjackman]: <https://news.ycombinator.com/item?id=42756000>
[^prakashn27]: <https://news.ycombinator.com/item?id=42757179>
[^lima]: <https://news.ycombinator.com/item?id=42763242>
[^PuercoPop]: <https://lobste.rs/s/4hmcum/forgejo_is_now_copyleft_just_like_git#c_vdtswv>
[^yawaramin]: <https://lobste.rs/s/4hmcum/forgejo_is_now_copyleft_just_like_git#c_c7k5kn>
[^steveno]: <https://lobste.rs/s/4hmcum/forgejo_is_now_copyleft_just_like_git#c_lzjkj2>
[^nia]: <https://lobste.rs/s/4hmcum/forgejo_is_now_copyleft_just_like_git#c_nanb7r>
[^pcrock]: <https://lobste.rs/s/4hmcum/forgejo_is_now_copyleft_just_like_git#c_b0pbhr>
[^nicoco]: <https://lobste.rs/s/giyb8x/forgejo_v16_0_is_available#c_zpsoyw>
