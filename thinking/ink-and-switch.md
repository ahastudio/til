# Ink & Switch: 생각을 위한 도구의 미래를 연구하는 독립 연구소, 10년째의 홈페이지

<https://www.inkandswitch.com/>

HN 토론: <https://news.ycombinator.com/item?id=49842270> (241점, 25개 댓글)

GN 토론: <https://news.hada.io/topic?id=34277>

## 소개

Ink & Switch는 “생각을 위한 도구(tools for thought)의 미래를 탐구하는 독립 연구소”다.
홈페이지는 연구소가 인간의 지능을 증폭하는 새 컴퓨터, 곧 더 분명하게 생각하고 더 효과적으로 협업하며 언제 어디서나 쓸 수 있는 시스템을 그린다고 소개하고, 작업의 세부는 계속 바뀌어도 모든 일이 그 비전을 향한다고 적는다.
현재 소장은 Peter van Hardenberg다.

2026년 홈페이지의 첫 화면은 “Tenfold”다.
연구소의 10주년을 맞아 친구들의 도움을 받아 만든 인터랙티브 작품으로, 열 글자와 열 해라는 뜻을 담았고, 연구소의 연구에서 나온 기술로 만들었다고 한다.
방문자는 화면 곳곳을 클릭하고 끌면서 글자마다 다른 반응을 볼 수 있고, 그 디자인은 티셔츠와 포스터로도 판다.

## 연구 영역

홈페이지는 연구를 네 주제로 나눈다.

| 주제                   | 설명                                                                 |
| ---------------------- | -------------------------------------------------------------------- |
| 로컬 우선 소프트웨어   | 데이터를 사용자에게 돌려주고 모든 도구에서 협업을 가능하게 하는 구조 |
| 가변 소프트웨어        | 사람들이 그 순간의 필요에 맞게 도구를 고칠 수 있는 소프트웨어 환경   |
| 프로그래밍 가능한 잉크 | 종이에 잉크를 긋듯 자연스럽게 동작과 상호작용을 더하는 스케치 매체   |
| 보편적 버전 관리       | 모든 종류의 매체에서 대안을 탐색하고 이력을 추적하며 협업하는 도구   |

대표 작업으로는 2025년 에세이 “Malleable Software”, 시나리오를 탐색하는 스프레드시트 Ambsheets, 로컬 우선 접근 제어 Keyhive, 로컬 우선 가변 소프트웨어 Patchwork, 협업 프로그래밍 커널 Livelymerge, 여행 계획을 위한 동적 문서 Embark, 손그림을 스프레드시트처럼 프로그래밍하는 Inkbase, 그리고 2019년 에세이 “Local-first software”를 든다.
연구에서 자라 실제로 널리 쓰이는 도구가 된 것도 둘 있다.
캔버스 위에 노트와 스케치와 PDF를 모아 생각을 정리하는 Allume(옛 이름 Muse)과, CRDT로 오프라인에서도 기기 사이의 변경을 자동으로 동기화하는 협업 라이브러리 Automerge다.

연구소는 결과를 웹사이트와 학술 행사에 발표하며, 개인과 기업 후원자, 세계 여러 기관의 연구비로 운영된다.
2026년 7월 베를린 Local-First Conf에는 연구소 전원이 참석해 Patchwork, PlayBook, Automerge 등의 진행 상황을 공유했고, 4월 GodotCon에서는 Godot 엔진에 Automerge 기반 버전 관리와 협업을 더하는 플러그인 Backstitch를 발표했다.

## 분석

### 홈페이지 자체가 연구의 시연이다

Tenfold는 연구소의 기술로 만들었다고 소개된다.
Hacker News에서 hnisjafx40은 연구소의 작업은 늘 뭔가를 다시 만들고 싶게 한다며, 홈페이지가 놀 수 있는 것이 무척 그들답다고 적고, 얼마나 직접 만들었고 얼마나 자체 Automerge 도구에서 나왔는지 궁금해했다.[^hnisjafx40]
연구소 쪽의 pvh는 글자 하나를 다시 만들어 보고 싶다면 최근 공개한 편집 가능한 판본, 곧 그 자체로 하나의 Patchwork인 시스템이 있다고 답했다.[^pvh]

이 답은 홈페이지의 성격을 보여 준다.
Tenfold는 연구 결과를 설명하는 페이지가 아니라, 연구 결과로 만든 작품이고, 방문자가 그 작품을 고쳐 볼 수 있다.
가변 소프트웨어, 곧 사용자가 그 순간에 도구를 고칠 수 있어야 한다는 연구 주제가 홈페이지의 구조로 구현된 셈이다.

### 연구소의 가장 큰 영향은 제품보다 글에서 나왔다

홈페이지는 연구소가 무엇보다 글로 알려져 있다고 스스로 말한다.
Hacker News에서 zazuke는 연구소가 최고의 글들을 갖고 있다며 가장 좋아하는 글로 로컬 우선 에세이를, 최근 읽은 것으로 Embark를 꼽았고,[^zazuke] hencq는 “Potluck: 개인 소프트웨어로서의 동적 문서”([[dynamic-documents-as-personal-software]])를 좋아한다고 덧붙였다.[^hencq]
Topfi는 특히 CRDT에 관한 작업이 UX를 개선하는 데 큰 영감을 준다고 적었다.[^Topfi]

2019년의 로컬 우선 에세이는 연구소를 넘어 하나의 운동이 됐다.
evek는 연구소가 Local-First 콘퍼런스를 만든 사람들이기도 하다고 짚었다.[^evek]
연구소가 만든 Automerge 같은 라이브러리보다, 그 라이브러리가 왜 필요한지를 설명한 글이 더 많은 사람의 생각을 바꿨다.

## 비평

### “클릭하고 끌어 보라”는 안내는 일관성 없는 경험을 남긴다

Tenfold는 놀라움을 주지만, 모든 방문자에게 즐거운 것은 아니었다.
Hacker News에서 krisoft는 멋져 보이지만 아무것도 일관되지 않아 답답하다며, 어떤 것은 클릭하면 바뀌고, 어떤 것은 끌면 바뀌고, 어떤 것은 아무 일도 하지 않는 것 같다고 적었다.[^krisoft]
monkeydust도 멋지다에서 짜증 난다로 금방 바뀌었다고 답했다.[^monkeydust]

연구소의 spiralganglion은 그 책임을 자신이 지겠다며 배경을 설명했다.[^spiralganglion-input]
샌드박스를 처음 만들 때 글자를 직접 클릭하고 끌기, 작은 토큰을 끄는 제어판, 타임라인 스크럽, 큰 전역 모드 전환 같은 여러 입력을 선택적으로 쓸 수 있게 했는데, 개발자마다 자기 글자의 아이디어에 맞는 입력만 골라 썼다는 것이다.
열 명이 각자 한 글자씩 만든 작품이라는 구조가 그대로 드러난 셈이다.
Vishal_Max가 끌어 보기 전에는 왜 멋진지 몰랐다고 적고, low_tech_punk가 마우스 사용자는 누르고 끌어야 소리와 효과를 볼 수 있다고 힌트를 남긴 것도,[^Vishal_Max][^low_tech_punk] 발견 가능성이 설계의 약점이라는 것을 보여 준다.

### 로컬 우선을 말하는 연구소의 제품이 구독으로 팔린다

홈페이지는 Allume을 연구에서 자란 제품으로 소개한다.
Hacker News에서 throwaw12는 앱이 멋져 보이지만 로컬 전용 소프트웨어가 왜 구독이냐고 물었다.[^throwaw12]
subjars는 Mac, iPad, iPhone 사이의 동기화에는 여전히 서버가 필요하지만 한 기기에서는 완전히 오프라인으로 쓸 수 있고, 지금 혼자 개발하는 Adam Wulf가 로컬 P2P 동기화를 준비 중이라고 답했다.[^subjars]

spiralganglion은 개발자는 일한 만큼 돈을 받아야 하고 Allume 작업이 계속되니 지속적인 수입이 필요하다고 답했다.[^spiralganglion-pay]
6gvONxR4sf7o는 로컬 전용 소프트웨어를 만드는 것이 클라우드에 어려운 일을 맡기는 것보다 오히려 더 어렵다며, 로컬 우선이라면 더 낼 의향이 있지만 이상하게 느껴지는 것은 사실이라고 적었다.[^6gvONxR4sf7o]
이 문답은 로컬 우선 운동이 풀지 못한 숙제를 보여 준다.
데이터를 사용자에게 돌려주는 소프트웨어가 어떻게 지속 가능한 사업이 되느냐는 질문에, 연구소의 에세이는 기술적 답을 줬지만 사업적 답은 아직 없다.

## 인사이트

### 연구소의 형식은 기업 연구소와 학계 사이의 세 번째 길이다

Ink & Switch는 제품을 팔기 위한 기업 연구소도, 논문을 쓰기 위한 대학 연구실도 아니다.
후원자와 연구비로 운영되고, 결과를 에세이와 연구 노트로 공개하며, 일부 연구가 제품이 되면 그 제품은 독립한다.
Allume이 한 명의 개발자에게 넘어가 계속 개발되는 것이 그 예다.

이 형식은 Xerox PARC가 1970년대에 했던 일과 닮았지만, 결과를 회사가 소유하지 않는다는 점에서 다르다.
PARC의 많은 아이디어가 Xerox가 아닌 다른 회사에서 제품이 됐던 것처럼, Ink & Switch의 로컬 우선과 CRDT 아이디어도 여러 제품에 스며들었다.
차이는 Ink & Switch가 그 확산을 처음부터 목표로 삼았다는 것이다.
10년을 이어 온 이 형식은, 연구가 반드시 한 회사의 이익이나 한 학계의 평가에 묶이지 않아도 된다는 것을 보여 준다.

### 열 명이 한 글자씩 만든 작품은 가변 소프트웨어의 실험이기도 하다

spiralganglion의 설명처럼 Tenfold의 글자들은 같은 샌드박스에서 각자 다른 입력을 골라 만들어졌다.[^spiralganglion-input]
그 결과는 일관성 없는 경험이었지만, 동시에 한 플랫폼 위에서 여러 사람이 각자의 방식으로 도구를 만들 수 있다는 시연이었다.
iFreilicht가 지적했듯 글자마다 한두 명의 구성원이 직접 만든 것으로 적혀 있다.[^iFreilicht]

이것은 가변 소프트웨어가 마주할 긴장을 작은 규모로 보여 준다.
사용자 각자가 도구를 고칠 수 있으면, 도구는 각자에게 맞게 되지만 서로에게는 낯설어진다.
krisoft가 느낀 답답함은, 모두가 자기 방식으로 만든 소프트웨어를 다른 사람이 쓸 때 생기는 비용이다.[^krisoft]
Ink & Switch가 앞으로 풀어야 할 질문은 사용자가 고칠 수 있는 소프트웨어를 어떻게 만들지를 넘어, 여러 사람이 고친 소프트웨어가 서로에게 어떻게 읽히게 할지일 것이다.

---

[^hnisjafx40]: <https://news.ycombinator.com/item?id=49842463>

[^pvh]: <https://news.ycombinator.com/item?id=49846376>

[^zazuke]: <https://news.ycombinator.com/item?id=49842754>

[^hencq]: <https://news.ycombinator.com/item?id=49847978>

[^Topfi]: <https://news.ycombinator.com/item?id=49843055>

[^evek]: <https://news.ycombinator.com/item?id=49842767>

[^krisoft]: <https://news.ycombinator.com/item?id=49843410>

[^monkeydust]: <https://news.ycombinator.com/item?id=49843596>

[^spiralganglion-input]: <https://news.ycombinator.com/item?id=49846982>

[^Vishal_Max]: <https://news.ycombinator.com/item?id=49844023>

[^low_tech_punk]: <https://news.ycombinator.com/item?id=49845222>

[^throwaw12]: <https://news.ycombinator.com/item?id=49842869>

[^subjars]: <https://news.ycombinator.com/item?id=49843180>

[^spiralganglion-pay]: <https://news.ycombinator.com/item?id=49847038>

[^6gvONxR4sf7o]: <https://news.ycombinator.com/item?id=49846400>

[^iFreilicht]: <https://news.ycombinator.com/item?id=49843162>
