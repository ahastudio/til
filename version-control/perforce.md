# Perforce P4: 대형 바이너리 에셋을 위한 중앙 집중형 버전 관리

<https://www.perforce.com/products/helix-core>

HN 토론: <https://news.ycombinator.com/item?id=48965886> (53점, 87개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=40842968> (62점, 63개 댓글)

## 소개

Perforce P4는 Perforce Software가 만드는 중앙 집중형 버전 관리 시스템이다.
1995년 창업자 Christopher Seiwald가
캘리포니아 앨러미다에서 회사를 세우며 만든 제품으로,
처음 이름은 “Perforce”였고 흔히 “P4”라고 줄여 불렀다.[^p4-rebrand]
2016년 회사 소유가 바뀌고 Seapine Software를
인수하면서 이름이 Helix Core로 바뀌었다가,
2025년 3월 다시 P4로 돌아왔다.[^p4-rebrand]
`p4 sync`, `p4 submit` 같은 명령과 P4V, P4Merge 같은 클라이언트 이름에
이미 P4가 쓰이고 있었다는 것이 이유다.[^p4-rebrand]
같은 개편으로 Helix Swarm은 P4 Code Review, Helix DAM은 P4 DAM이 되는 등
관련 제품들도 P4 Platform이라는 이름 아래 묶였다.[^p4-rebrand]

Perforce는 P4를 대용량 바이너리와 에셋이 많은 프로젝트용으로 내세운다.
배타적 파일 잠금, 스트림 기반 브랜치, 세밀한 권한과 감사 로그,
델타 전송과 프록시 서버를 통한 빠른 동기화를 주요 기능으로 꼽고,
상위 20개 AAA 게임 스튜디오 중 19곳이 P4를 쓴다고 홍보한다.[^p4-free]

개발자들의 평가는 “쓸 수밖에 없는 표준”에 가깝다.
2026년 7월 Perforce가 AI 내레이션 교육 영상에 500달러를 받는다는 HN 글에서
forrestthewoods는 인디가 아닌 게임 개발사는 사실상 전부 Perforce를 쓰지만
Perforce가 좋으냐 하면 그렇지 않고 15년째 정체되어 있으며,
그래도 Git은 게임 개발의 요구를 채우기에 한참 모자라다고 했다.[^forrestthewoods]
dijit은 Perforce가 SVN보다 확실히 낫고 Git LFS보다는 훨씬 낫지만
제품은 버그가 많고 회사는 방향을 잃었다며,
그래도 게임과 자동차 업계의 표준이라는
점에서 운이 좋은 위치라고 평했다.[^dijit-p4]
반례도 있다.
invader는 자신이 일한 AAA 스튜디오는 미리보기와 파이프라인 통합을 갖춘
Alienbrain으로 테라바이트 규모의 에셋을 다뤘다고 했다.[^invader]

## 동작 방식

### 서버가 정본이고, 작업 공간은 그 일부를 받는다

P4는 서버의 저장소(depot)가 유일한 정본이고,
각 사용자는 그중 필요한 부분을 자기 작업 공간(client workspace)으로 받는다.
Git처럼 모든 이력을 가진 로컬 저장소를 만들지 않는다.

a-dub은 P4의 작업 공간 매핑과 템플릿 모델이 우아하다고 평가했다.
임베디드처럼 거대한 디바이스 트리를 다룰 때 하위 트리를
골라 넣고 뺄 수 있기 때문이다.[^a-dub]
j1elo는 가상 스트림을 예로 들었다.
같은 저장소라도 아티스트는 아트 원본을 받고,
프로그래머는 아트 원본 대신 이미 만들어진 바이너리를 받게 할 수 있다는 것이다.
코드를 빌드하려는 엔지니어는 800GB짜리 아트 원본이 필요 없다.[^j1elo]

### 편집 전에 “연다”

P4의 작업 흐름은 Git과 순서가 다르다.
파일을 고치기 전에 `p4 edit`로 파일을 편집용으로 열어야 하고,
그러면 서버가 그 파일의 운영체제 쓰기 권한을 켠다.[^p4-edit]
연 파일은 변경 목록(changelist)에 묶이고,
`p4 submit`으로 변경 목록을 제출해야 서버의 저장소가 바뀐다.[^p4-edit]

```bash
p4 sync                 # 작업 공간을 서버의 최신 상태로 맞춘다
p4 edit Art/Hero.fbx    # 편집 전에 연다. 이때 쓰기 권한이 켜진다
# 파일을 편집한다
p4 submit -d "Update hero mesh"
```

제출된 파일은 이전 리비전을 덮어쓰지 않는다.
새 리비전은 다음 번호를 받고 이전 리비전도 그대로 남으며,
명령은 기본적으로 가장 최신 리비전(head revision)을 쓴다.[^p4-edit]

### 배타적 잠금

`+l` 파일 형식을 붙이면 한 사람이 파일을 연 동안 다른 사람은
그 파일을 편집용으로 열 수 없다.[^p4-edit]
병합할 수 없는 바이너리 에셋에서 두 사람이 같은 파일을 동시에 고치는 사고를
제출 시점이 아니라 편집을 시작하는 시점에 막는 장치다.
Perforce가 첫 번째 기능으로 내세우는 것도 이 배타적 잠금이다.[^p4-free]
Lobste.rs의 rs545837은 레벨 파일이나 PSD처럼 병합할 수 없는 파일은
조율이 편집 전에 일어나야 하며, 그것이 Perforce가 맞게 한 일이자
Git이 진지하게 다루지 않은 일이라고 정리했다.[^rs545837]

잠금만큼 자주 언급되는 것이 디렉터리 단위 권한이다.
LugosFergus는 P4에서는 NDA에 서명한 사람만 특정 디렉터리에 접근하게 할 수 있지만
Git은 전부 아니면 전무라고 지적했다.[^LugosFergus]

## 가격

| 플랜     | 가격                        | 주요 조건                                                   |
| -------- | --------------------------- | ----------------------------------------------------------- |
| Free     | 0달러                       | 사용자 5명, 작업 공간 20개, Git 저장소 3개, 평생 지원 3건   |
| Cloud    | 사용자당 월 39달러(월 청구) | Perforce가 운영하는 단일 테넌트, 저장 공간 64GiB, 100명까지 |
| Scale    | 문의(연 청구)               | 작업 공간과 Git 저장소 무제한, P4 DAM 추가 가능             |
| Platform | 문의(연 청구)               | Scale에 P4 DAM과 P4 Plan 포함                               |

가격은 2026년 10월 14일 Perforce 가격 페이지 기준이다.[^p4-pricing]
교사와 학생에게는 무료 교육용 라이선스를 따로 제공한다.[^p4-pricing]

## 다른 버전 관리 시스템과 비교

| 항목          | Git              | Perforce P4          | Lore                          | Scion                        |
| ------------- | ---------------- | -------------------- | ----------------------------- | ---------------------------- |
| 구조          | 분산             | 중앙 서버            | 중앙 서버, 로컬 커밋 가능     | 중앙 서버, 클라이언트는 얇음 |
| 대상          | 텍스트 소스 코드 | 대형 바이너리와 코드 | 게임·엔터테인먼트 에셋과 코드 | 에이전트 규모의 모노레포     |
| 바이너리 잠금 | 없음             | `+l` 배타적 잠금     | 알림만, 강제는 로드맵         | 언급 없음                    |
| 라이선스      | 오픈소스         | 상용 (5명까지 무료)  | MIT                           | 비공개 사내 시스템           |

Lore와 Scion의 내용은 각각 [Lore](lore.md)와
[Scion](scion.md) 문서에 정리되어 있다.
Lore의 FAQ는 대형 바이너리용 중앙 집중형 시스템들이
일상 작업에도 서버 왕복을 요구하고 독점 통신 프로토콜을 쓴다고 지적하며
Lore가 그 부분을 바꾸겠다고 한다.[^lore-faq]
Anthropic의 Scion 발표에 대해서는 HN과 Lobste.rs에서
“결국 Perforce로 돌아왔다”는 반응이 나왔다.[^scion-lobsters]

Git과의 차이를 가장 짧게 정리한 것은 tikotus의 말이다.
VCS는 중앙형과 분산형, 파일 단위와 커밋 단위로 나뉘는데,
게임에는 Perforce 같은 중앙형 파일 단위가 맞고
Git은 분산형 커밋 단위라는 것이다.[^tikotus]
flohofwoe는 게임 프로젝트에서 텍스트는 파일 수로 1~5%에 불과하고
원본 아트 파일은 보통 5~20MB, 100MB도 드물지 않아
LFS를 써도 Git이 무너진다고 했다.[^flohofwoe]
Lore에 대해서는 기대와 신중함이 섞인다.
jordand는 Lore가 게임 제작에서 Perforce를 대체하려면 아직 2~3년은 걸리겠지만,
원치 않는 P4 라이선스에 수만 달러를 쓰는
스튜디오들이 있어 관심이 크다고 했다.[^jordand]
lazypenguin은 코드는 Git, 에셋은 SVN으로 나눠 쓰고 있다며
Git, SVN,
Perforce 모두 최선이라서가 아니라 달리 없어서
고르는 것이라고 했다.[^lazypenguin]

## 트레이드오프

### 잠금은 충돌을 막지만 동시 작업을 막는다

배타적 잠금은 병합할 수 없는 파일에서 가장 확실한 충돌 방지책이다.
대가는 한 사람이 파일을 잡고 있는 동안 다른 사람이 기다려야 한다는 점이다.
잠근 사람이 퇴근하거나 휴가를 가면 관리자가 잠금을 풀어야 하고,
잠금 상태를 모두가 서버에서 확인해야 하므로 서버 의존이 커진다.
Lore가 잠금을 아직 “알림”으로만 두고 강제와 확장성을 로드맵에 올린 것도
이 문제가 쉽지 않다는 뜻이다.[^lore-faq]

### 통합은 편하지만 고장 나면 진단이 어렵다

LinearIO는 P4가 IDE와 Unreal Editor에 잘 통합되어 있어 잠금, 해제, 스트림 병합이
매끄럽지만, 잘 안 될 때는 원인을 찾기가 매우 어렵다고 했다.[^LinearIO]
retroflexzy는 업무의 상당 부분이 Perforce가 망가뜨린 작업 공간을 고치고
그러지 못하게 막는 래퍼를 만드는 일이라고 했다.[^retroflexzy]
게임 스튜디오에 Perforce 전담 도구 엔지니어가 생기는 이유다.

### 서버 중심은 큰 저장소를 다루게 하지만 오프라인을 어렵게 한다

작업 공간에 필요한 부분만 받으므로 수백 기가바이트짜리 저장소도 다룰 수 있다.
그러나 파일을 열고 제출하는 일이 서버를 거치므로
서버에 닿지 못하면 정상적인 흐름으로 일할 수 없다.
`p4 edit -k` 같은 옵션은 서버와 끊긴 상태에서
한 작업을 나중에 맞추기 위한 것이지,
오프라인 작업을 일상적인 흐름으로 만들어 주지는 않는다.[^p4-edit]

### 상용 라이선스와 생태계

P4는 무료 플랜이 있지만 5명을 넘으면 비용이 생기고,
서버 운영 경험이 있는 사람도 필요하다.
Perforce는 이를 보완하려고 관리형 Cloud 플랜과
서버 관리, 이전, 점검 같은 유료 서비스를 함께 판다.[^p4-pricing]
a-dub은 20여 년 전 좌석당 600달러 정도였다고 기억했고,[^a-dub]
jordand는 원치 않는 P4 라이선스에 수만
달러를 쓰는 스튜디오가 있다고 했다.[^jordand]
떠나는 비용도 크다.
rty32는 자기 회사가 Perforce에서 Git으로의 이전에 실패했다며,
버전 관리는 시스템 하나가 아니라 그 주변의 생태계 전체라고 했다.[^rty32]
Git처럼 누구나 쓰는 도구가 아니라서
신입 개발자나 외부 협력사가 익숙하지 않을 가능성도 고려해야 한다.

## 기억할 원칙

### 버전 관리의 설계는 무엇을 다루느냐가 정한다

Git은 텍스트를 다루는 분산된 사람들을 위해 만들어졌고,
P4는 병합할 수 없는 대형 에셋을 다루는 한 조직을 위해 만들어졌다.
Lore는 그 둘을 합치려 하고,
Scion은 사람보다 에이전트가 많은 조직을 위해 다시 중앙으로 돌아갔다.
어느 쪽이 더 낫다기보다, 저장소에 무엇이 들어가고 누가 그것을 바꾸는지가
분산과 중앙, 잠금과 병합 사이의 선택을 정한다.

## 도입 또는 이전 전에 확인할 것

P4가 맞는지는 파일 확장자보다 협업 방식으로 판단한다.
병합할 수 없는 파일을 여러 사람이 고치는지,
사용자마다 필요한 경로가 다른지,
파일별 접근 권한과 감사 기록이 필요한지를 확인한다.
이 요구가 약하다면 서버 중심 작업 흐름과 라이선스 비용을
추가로 떠안을 이유가 있는지 다시 따져야 한다.

시험 운영에서는 동기화 범위, 잠금 대기 시간,
잠금 해제 권한, 서버 장애 시 업무 중단 시간을 측정한다.
아티스트 도구와 빌드 파이프라인을 함께 시험하고,
클라이언트 손상과 실수로 잠근 파일을 복구하는 절차도 연습한다.
도구 통합이 원활한 정상 경로뿐 아니라
전담 운영자가 개입해야 하는 예외 경로가 총비용을 좌우한다.

Git에서 옮길 때는 저장소 전체를 한 번에 바꾸지 않는다.
파일 이력과 권한을 보존해야 하는 범위를 정하고,
Git과 P4가 동시에 수정 가능한 기간,
최종 동기화와 되돌리기 기준을 미리 합의한다.
이미 P4를 쓰는 조직은 비용과 장애 대응을 개선할 대안이 있는지,
새 조직은 중앙 서버의 장점을 오프라인 자율성보다
우선할 이유가 있는지 각각 따로 판단해야 한다.

---

[^p4-rebrand]: Perforce Software, [Re-Introducing P4: A Name Rooted in History and a Platform for the Future](https://www.perforce.com/blog/vcs/introducing-the-p4-platform), 2025-03-13

[^p4-free]: Perforce Software, [Free Version Control Software | P4 (Helix Core)](https://www.perforce.com/products/helix-core/free-version-control), 게시일 표시 없음

[^p4-edit]: Perforce Software, [p4 edit](https://perforce.com/manuals/cmdref/Content/CmdRef/p4_edit.html), 게시일 표시 없음

[^p4-pricing]: Perforce Software, [Perforce P4 Pricing and Plans](https://www.perforce.com/products/p4/pricing), 게시일 표시 없음 (2026-10-14 열람)

[^lore-faq]: Epic Games, [FAQ - Lore Developer Documentation](https://epicgames.github.io/lore/faq/), 게시일 표시 없음

[^scion-lobsters]: Lobste.rs, [Redesigning source control at Anthropic](https://lobste.rs/s/5ucftp/redesigning_source_control_at_anthropic#c_xgqqig), 2026-10-13

[^forrestthewoods]: <https://news.ycombinator.com/item?id=48966355>

[^dijit-p4]: <https://news.ycombinator.com/item?id=48966633>

[^invader]: <https://news.ycombinator.com/item?id=48967385>

[^a-dub]: <https://news.ycombinator.com/item?id=48966803>

[^j1elo]: <https://news.ycombinator.com/item?id=48574986>

[^rs545837]: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version#c_shgnpy>

[^LugosFergus]: <https://news.ycombinator.com/item?id=48571625>

[^tikotus]: <https://news.ycombinator.com/item?id=48581537>

[^flohofwoe]: <https://news.ycombinator.com/item?id=48966578>

[^jordand]: <https://news.ycombinator.com/item?id=48966629>

[^lazypenguin]: <https://news.ycombinator.com/item?id=48966403>

[^LinearIO]: <https://news.ycombinator.com/item?id=48573214>

[^retroflexzy]: <https://news.ycombinator.com/item?id=48572947>

[^rty32]: <https://news.ycombinator.com/item?id=40845578>
