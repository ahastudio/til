# Bubbles.town

<https://bubbles.town/>

HN 토론: <https://news.ycombinator.com/item?id=48567155> (610점, 209개 댓글)

## 소개

Bubbles.town은 5천여 개의 독립 개인 블로그 포스트를 한 화면에 모아
커뮤니티 투표와 최신성으로 순위를 매기는 피드 서비스다.
HN이 기술 뉴스에 특화된 것처럼, Bubbles는 기술 외 영역 — 예술, 음식, 음악, 자연, 삶 —
을 포괄하는 비기술 인터넷을 위한 HN이라는 포지셔닝을 갖는다.
독일 Mülheim 출신 개발자 Ben이 개인 프로젝트로 만들었다.

블로그 목록은 큐레이션된 출처에서 수동으로 검토해 선정하며,
새 포스트는 블로거가 제출하지 않아도 RSS를 통해 자동으로 등록된다.
계정은 Fediverse 계정(Mastodon, Pixelfed, GoToSocial 등)으로 생성한다.
이메일·패스워드·추적 쿠키 없이 Fediverse 핸들, 투표 기록, 팔로우 목록만 저장한다.
분석 도구는 Plausible를 자체 호스팅하며 공개 대시보드를 운영한다.

## 랭킹 알고리즘

순위 공식은 아래와 같다.

```text
Score = (1 + Votes × 25) / (EffectiveAge + 2) ^ 1.4
```

- 투표 가중치: 고정 승수 25
- 유효 나이(EffectiveAge): 마지막 투표 이후 경과 시간, 최소값은 실제 나이의 50%
- 중력 계수 1.4 — HN의 1.8보다 낮아 포스트가 더 오래 노출됨
- 댓글 수는 랭킹에 포함하지 않음 (2인 대화로 인한 부풀리기 방지)

## 주요 기능

- **세 가지 뷰**: Top(투표+최신성), New(시간순), Hot(활발한 토론)
- **카테고리 필터**: Art, Crafts, Culture, Film & TV, Food, Gaming,
  History, Life, Music, Nature, Politics, Science, Tech, Writing
- **투표 임계값 필터**: 3+, 5+, 10+ 투표
- **데일리·위클리 브리핑**: 편집된 선별 목록
- **RSS 피드 및 Fediverse 연동**
- **랜덤 포스트 탐색**

## 분석

### "비기술 인터넷을 위한 HN"이라는 포지셔닝의 논리

Bubbles가 채우려는 공백은 명확하다.
HN과 Lobsters는 기술 편향이 강하고, Kagi Small Web은 커뮤니티 랭킹이 없으며,
블로그 디렉토리는 "오늘 읽을 만한 것"을 알려주지 않는다.
소셜 플랫폼은 알고리즘이 대화를 통제하고, RSS는 구독자 개인 안에 고립된다.
Bubbles는 이 빈칸에 "집단적 신호(collective signal)"를 배치한다.

랭킹 공식에서 중력 계수를 HN(1.8)보다 낮은 1.4로 설정한 것은 의미 있는 선택이다.
기술 뉴스는 빠르게 구식이 되지만, 개인 블로그의 에세이나 삶의 기록은
시간이 지나도 가치가 유지된다.
수명이 긴 콘텐츠에 더 긴 노출 기회를 주는 것은 도메인 특성에 맞춘 조정이다.

Fediverse 계정을 인증 수단으로만 사용하는 설계도 주목할 만하다.
Fediverse의 분산 정체성 레이어를 차용하되, Bubbles 자체는
별도의 소셜 그래프를 구축하지 않는다.
이는 플랫폼 락인을 줄이면서도 스팸·어뷰징 방지를 위한 계정 장벽을 유지하는 균형이다.

### "스몰 웹"이라는 이상과 실제 콘텐츠 사이의 긴장

HN 토론에서 가장 자주 등장한 반응은 실망이었다.
여러 사용자가 방문 직후 정치적·문화 전쟁 성격의 포스트를 접하고 떠났다.[^NoSalt][^sph][^halyconWays]
"스몰 웹"이라는 개념이 기대하게 만드는 것 — 소박하고 개인적인 기록들 — 과
실제 커뮤니티 투표가 부상시키는 것 — 논쟁적이고 클릭 유발적인 제목들 — 사이에
간극이 존재한다는 지적이다.[^1317]

이 문제는 Bubbles가 해결하기 어려운 구조적 긴장이다.
커뮤니티 투표 기반 랭킹은 논쟁적 콘텐츠를 자연스럽게 부상시키는 경향이 있다.
"비기술 HN"을 만들면 HN의 기술 편향은 사라지지만,
투표 메커니즘이 낳는 감정적 편향은 그대로 이어진다.

## 비평

### 콘텐츠 다양성은 서비스 초기의 취약점이기도 하다

nathell은 자신의 블로그가 Bubbles에 신디케이트된 사실을 몇 주 전에 발견했고,
그 이후 점점 자주 방문하게 됐다고 썼다.[^nathell]
"소셜 미디어의 둠스크롤링과 비교해 정말 새롭고, 다양하고, 인간적"이라는 평이었다.
이 반응은 서비스가 잘 작동할 때 어떤 경험을 주는지 보여준다.

그러나 초기 단계에서 투표 모수가 적으면 소수 사용자의 취향이 전체 프런트페이지를 지배한다.
1~3점짜리 포스트가 Top 뷰에 노출되는 현상은
KerryJones가 지적한 것처럼 "Top 알고리즘이 실제로 무엇을 의미하는가"라는
질문을 낳는다.[^KerryJones]
커뮤니티가 충분히 성장하기 전까지는 투표 신뢰도가 낮을 수밖에 없다.

### Fediverse 전용 인증은 잠재적 사용자를 배제한다

exitnode는 Mastodon 계정 없이 이메일로 가입할 수 없다는 점을 지적했다.[^exitnode]
소셜 미디어를 피하려는 사람에게 Fediverse 계정 개설을 요구하는 것은
"소셜 미디어 대안"이라는 서비스 취지와 어긋날 수 있다.
Fediverse 가입 경험이 낯선 사용자에게 진입 장벽이 된다.

### 콘텐츠 조정 정책이 명시되지 않는다

TacticalCoder와 sph는 프런트페이지의 특정 포스트에 강한 불쾌감을 표했다.[^sph]
Bubbles는 "손으로 선정한 블로그"를 내세우지만,
개별 포스트 수준의 조정 정책은 문서화되어 있지 않다.
커뮤니티가 성장하면서 어떤 콘텐츠가 허용되는지에 대한 기준이
더 명확히 필요해질 것이다.

## 인사이트

### 투표 메커니즘이 없는 스몰 웹과, 있는 스몰 웹은 다른 것을 만든다

Kagi Small Web이나 개인 RSS 리더와 Bubbles의 결정적 차이는 투표다.
커뮤니티 투표가 없으면 스몰 웹은 조용하고 개인적인 공간이다.
투표가 생기면 가시성 경쟁이 시작되고, 콘텐츠의 성격이 그 경쟁에 적응한다.
Bubbles는 의도적으로 후자를 선택했다 — 발견 가능성을 높이는 대신
HN이 가진 문제를 어느 정도 함께 수입한 셈이다.

wwfn이 주목한 점은 이 서비스가 HN 프런트페이지에 오르기까지 7번 시도했다는 것이다.[^wwfn]
"X but for Y" 제목 패턴이 성공한 것이 LLM 시대의 커뮤니케이션 방식을 반영한다는
그의 관찰은 흥미롭다 — 서비스 자체의 이름(Bubbles.town)이 아니라
기존 레퍼런스에 기댄 설명이 바이럴 포인트가 됐다.

### RSS + Fediverse 조합은 탈중앙화 웹의 현실적 조합이다

아티팩트로서의 설계가 흥미롭다.
콘텐츠 생산(개인 블로그 RSS)과 정체성·상호작용(Fediverse)을 모두 외부에 위임하고,
Bubbles 자체는 랭킹 레이어만 담당한다.
이 구조는 서비스가 사라져도 콘텐츠와 정체성이 살아남는다는 의미다.
rsolva가 GoToSocial 인스턴스로 로그인해 즉시 사용했다는 반응은[^rsolva]
이 설계가 실제로 작동한다는 검증이다.

이 조합이 성숙하면 "Bubbles 없는 Bubbles" — 랭킹 레이어 자체를 누구나 운영할 수 있는
프로토콜 — 으로 발전할 가능성이 있다.
RobotToaster가 Lemmy 커뮤니티로의 Fediverse 연동을 제안한 것은[^RobotToaster]
같은 방향을 가리키는 요청이다.

---

[^nathell]: <https://news.ycombinator.com/item?id=48568285>
[^exitnode]: <https://news.ycombinator.com/item?id=48567721>
[^KerryJones]: <https://news.ycombinator.com/item?id=48571695>
[^NoSalt]: <https://news.ycombinator.com/item?id=48571520>
[^sph]: <https://news.ycombinator.com/item?id=48581504>
[^halyconWays]: <https://news.ycombinator.com/item?id=48579025>
[^1317]: <https://news.ycombinator.com/item?id=48570748>
[^rsolva]: <https://news.ycombinator.com/item?id=48568585>
[^RobotToaster]: <https://news.ycombinator.com/item?id=48568888>
[^wwfn]: <https://news.ycombinator.com/item?id=48575433>
