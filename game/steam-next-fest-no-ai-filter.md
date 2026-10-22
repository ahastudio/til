# Steam Next Fest의 No-AI 필터 요구: 공개 항목은 있는데 필터는 없는 이유와 라벨이 풀어야 할 정의 문제

원문: [Steam Fans Are Begging for a No-AI Filter as Steam Next Fest Is Filled With Slop](https://www.ign.com/articles/steam-fans-are-begging-for-a-no-ai-filter-as-steam-next-fest-is-filled-with-slop)

HN 토론: <https://news.ycombinator.com/item?id=50168190> (177점, 210개 댓글)

GN 토론: <https://news.hada.io/topic?id=35732>

## 목차

- [요약](#요약)
- [기사가 말하는 것](#기사가-말하는-것)
- [직접 확인한 것과 확인하지 못한 것](#직접-확인한-것과-확인하지-못한-것)
- [Steam이 지금 알려 주는 것](#steam이-지금-알려-주는-것)
  - [콘텐츠 설문의 AI 항목](#콘텐츠-설문의-ai-항목)
  - [상점 페이지에서 보이는 공개 문구](#상점-페이지에서-보이는-공개-문구)
  - [공개 비율을 세 번 세어 보면](#공개-비율을-세-번-세어-보면)
  - [공개는 있지만 공식 필터는 없다](#공개는-있지만-공식-필터는-없다)
- [다른 장터와 규제는 어떻게 다루나](#다른-장터와-규제는-어떻게-다루나)
  - [itch.io: 범주를 고르게 하는 공개](#itchio-범주를-고르게-하는-공개)
  - [Epic: 공개 요구에 반대하는 쪽](#epic-공개-요구에-반대하는-쪽)
  - [EU AI Act: 게임에 일괄 라벨을 요구하지 않는다](#eu-ai-act-게임에-일괄-라벨을-요구하지-않는다)
- [반응 지도](#반응-지도)
- [시각별 분석](#시각별-분석)
  - [필터는 금지가 아니다](#필터는-금지가-아니다)
  - [라벨의 정의가 무너진다](#라벨의-정의가-무너진다)
  - [자기 신고는 거짓말을 부른다](#자기-신고는-거짓말을-부른다)
  - [문제는 AI가 아니라 노력의 신호다](#문제는-ai가-아니라-노력의-신호다)
  - [코드와 아트는 다르게 읽힌다](#코드와-아트는-다르게-읽힌다)
  - [문턱과 큐레이션](#문턱과-큐레이션)
  - [Next Fest의 구조가 문제를 키운다](#next-fest의-구조가-문제를-키운다)
  - [소규모 개발자에게 닿는 영향](#소규모-개발자에게-닿는-영향)
- [비평](#비평)
- [인사이트](#인사이트)
- [개발자가 상점 페이지에 쓸 공개 문구](#개발자가-상점-페이지에-쓸-공개-문구)
- [플레이어가 지금 할 수 있는 것](#플레이어가-지금-할-수-있는-것)
- [이 문서가 확인하지 못한 것](#이-문서가-확인하지-못한-것)

## 요약

IGN이 2026년 10월 19일에 올린 이 기사는
Steam Next Fest가 시작된 날의 분위기를 전한다.
AI로 만든 듯한 저품질 게임이 평소보다 많아
보인다는 불만이 Steam 커뮤니티에 올라왔고,
한 이용자는 AI 생성 콘텐츠가 들어간 게임을 걸러 내는 필터를 달라고 요청했다.
Steam이 이미 AI 사용 공개를 요구하니 그 정보로 필터를 만들면 된다는 논리다.
Steam Next Fest는 2026년 10월 19일 16시 47분(UTC)에 올라온 Steam 공지에서
“LIVE NOW”로 표시된 행사다.[^nf-live]

이 문서의 중심 주장은 이렇다.
“No AI” 이진 필터는 지금 형태로는 사람들이 실제로 걸러 내고
싶은 것을 걸러 주지 못한다.
첫째, Steam이 받는 공개의 내용은 자유 서술 문구라서
범주별로 거를 수 있는 구조화된 값이 페이지에서 보이지 않았다.[^ages]
다만 공개 구역이 있느냐 없느냐는 페이지에서 읽히고,
그 값으로 거르는 SteamDB 필터가 2025년 2월에 나왔다고 보도됐다.[^steamdb-gol]
둘째, 코딩 보조까지 치면 거의 모든 게임이 걸린다는 주장은
Valve의 현재 문서와 실제 공개 비율(3분의 1 안팎)에 맞지 않는다.[^cs][^pcg-haro]
그래도 라벨이 약속하는 범위는 개발사의 서술 습관이 정한다.
셋째, 라벨을 다는 쪽이 불이익을 보는 구조에서는 자기 신고가 줄어든다.
HN 토론에서 가장 많이 반복된 말은
사람들이 원하는 것이 AI 없는 게임이 아니라
노력이 들어간 게임이라는 것이다.

근거가 닿는 곳은 여기까지다.
이 문서가 처음 시금석으로 삼은 것은
이진 필터로 걸러지는 게임의 비율이 절반을 넘는지,
10%에도 못 미치는지였다.
공개 구역의 비율을 세 가지 방법으로 세어 보았다.
Sulka Haro의 전수 조사에서 2026년 신작의 30.8%가 공개를 달았고,[^pcg-haro]
PC Gamer가 6월의 한 주에 직접 센 신작은 338개 중 120개였으며,[^pcg-week]
이 문서가 Next Fest 첫날 전후의 데모 80개를 뽑아 센 값은 36개(45%)였다.
어느 값도 절반을 확실히 넘거나 10%에 못 미치지 않는다.
이진 필터는 지금 신작의 3분의 1에서 절반쯤을 걸러 내는 도구이고,
쓸모가 없어질 만큼 포화된 것도 무시해도 될 만큼 드문 것도 아니다.
다만 이 값은 AI를 얼마나 썼는지가 아니라 썼다고 적었는지를 센다.
이 문서는 Steam 내부에 구조화된 AI 필드가 있는지는 보지 못했고,
범주별 비율이 공개되면 결론이 다시 바뀔 수 있다.
개발자에게 당장 쓸모 있는 결론은 상점 페이지의 공개 문구를 범주별로,
사람이 한 일과 함께 구체적으로 쓰라는 것이다.

## 기사가 말하는 것

기사는 IGN의 Senior Tech Editor인 Jackie Thomas가 썼고,
페이지 메타데이터상 게시 시각은 2026년 10월 19일 21시 38분(UTC)이다.
첫 문장은 Steam Next Fest가 시작된 날 저품질 게임이
평소보다 많아 보인다는 문제 제기다.
ChatGPT에 짧게 명령해서 뽑은 듯한 그림을 쓴 게임이 눈에 띈다고 쓴다.
Claude Opus 5.5가 나온 뒤 decompilation과
mashup mod가 늘어난 흐름이 배경으로 언급된다.

기사가 인용하는 Steam 이용자 반응은 세 개다.
첫 번째는 Reddit의 r/Steam에 글을 올린 이용자 ScalesGhost다.
Discovery Queue에서 AI 생성 콘텐츠가 있는 게임을 빼고,
Incremental Games 같은 태그도 제외할 수 있게 해 달라고 요청했다.
두 번째는 AI가 Next Fest를 망쳤다는 별도 글에 달린 EmmaBooney의 댓글이다.
세 번째는 vibe coding으로 만든 게임의 과잉이 참여 지표를 떨어뜨리고
Steam이 제출 기준을 강화하기를 바란 aesoprowwy의 댓글이다.

기사의 판단은 이렇다.
Steam에는 이미 태그 체계가 있으니 필터를 만드는 일이 크지 않지만,
Valve가 5월에 태그를 줄였기 때문에 필터가 생기려면 AI 태그를 새로 넣어야 한다.
Valve는 오래전부터 큐레이션에 느슨했고
알고리즘이 인기작을 올리고 저품질작을 묻는 방식에 기댔으며,
그래서 이번 행사가 더 나빠 보여도 며칠 기다리면
인기 데모가 위로 올라올 것이라고 조언한다.
마지막 단락에서는 Epic이 AI 우선 방향을 이유로 Star Wars 슈터를 미뤘다는 보도와,
Epic Games Store 런처를 vibe coding으로 만들었다는 CEO의 발언,
Capcom이 RE Engine 개선에 AI를 쓰는 REX 프로그램을 들어 게임 업계에서
AI가 흔해지고 있음을 짚는다.

기사에는 두 가지 한계가 보인다.
첫째, 어떤 게임이 AI 산물인지는 그림이 그렇게 보인다는 인상에 기대고 있다.
기사가 예시 게임 이름이나 공개 문구를 대조한 흔적은 없다.
둘째, 필터가 무엇을 걸러야 하는지, AI를 어디까지 AI로 칠지는 다루지 않는다.
이 두 빈칸을 HN 토론이 채웠다.

## 직접 확인한 것과 확인하지 못한 것

| 항목                                 | 상태   | 비고                                                                                       |
| ------------------------------------ | ------ | ------------------------------------------------------------------------------------------ |
| Next Fest 진행 중                    | 확인   | Steam 공지가 2026년 10월 19일에 올라와 있고 제목에 LIVE NOW가 있다.[^nf-live]              |
| 행사 첫 며칠은 무작위 노출           | 확인   | Steamworks 문서에 적혀 있다.[^nfdoc]                                                       |
| Steam의 AI 공개 요구                 | 확인   | 콘텐츠 설문의 세 번째 영역이다.[^cs]                                                       |
| 5월 태그 개편                        | 확인   | 28개 삭제, 17개 추가가 보도됐고 AI 태그는 두 목록에 없다.[^tags]                           |
| 상점 페이지의 AI 공개 구역           | 확인   | 내용 설명자와 같은 `game_area_content_descriptors` 구역 안에 들어 있다.[^ages]             |
| AI 공개의 기계 판독 가능성           | 확인   | 구역의 유무는 페이지에서 읽히고, 공개 `appdetails` 응답에는 AI 항목이 없었다.[^appdetails] |
| SteamDB AI 필터의 현재 동작          | 미확인 | 2025년 보도만 확인했고 SteamDB는 접속이 막혀 지금의 동작을 보지 못했다.[^steamdb-gol]      |
| 최근 데모 80개의 공개 비율           | 확인   | 36개(45%)가 공개 구역을 달았다. 표본의 한계는 아래에 적었다.                               |
| Reddit 글 세 개의 원문               | 미확인 | Reddit이 자동 요청과 브라우저 도구 모두에서 막혀 열지 못했다.                              |
| Epic, Capcom 관련 서술               | 미확인 | 기사가 링크한 별도 기사를 열지 않았다.                                                     |
| Opus 5.5와 decompilation 증가의 관계 | 미확인 | 기사의 배경 설명이며 이 문서는 검증하지 않았다.                                            |

기사가 말한 “Valve가 5월에 사용자 정의 태그를
줄였다”는 표현은 IGN의 5월 기사와 결이 다르다.
그 기사는 Valve가 공식 태그 28개를 지우고 17개를 더했으며
몇 개를 합치거나 이름을 바꿨다고 쓴다.[^tags]
같은 기사는 태그를 개발자, 계정 제한이 없는 플레이어,
Steam 중재자가 붙일 수 있다고 전한다.[^tags]
그러니 줄어든 것은 사용자가 만드는 태그가 아니라 Valve가 정한 공식 목록이며,
그 목록에 AI 항목은 없다.

## Steam이 지금 알려 주는 것

### 콘텐츠 설문의 AI 항목

Steamworks의 Content Survey는 상점 페이지와 빌드를
심사에 올리기 전에 반드시 채우는 설문이다.[^cs]
설문은 일반 콘텐츠, 성인 콘텐츠, 생성형 AI 콘텐츠의 세 영역으로 나뉜다.[^cs]

AI 영역이 겨냥하는 대상은 게임과 함께
배포되어 플레이어가 소비하는 콘텐츠다.[^cs]
문서는 요즘 개발 환경에 AI 도구가 내장된 경우가 많다고 인정하고,
그런 도구로 얻는 효율은 이 영역의 초점이 아니라고 적는다.[^cs]
이 한 문장이 HN 토론에서 오간 논쟁의 상당 부분을 비껴간다.
코딩 보조를 썼다는 이유만으로 라벨이 붙는다는
가정이 Valve의 문서와 맞지 않기 때문이다.

설문은 AI 콘텐츠를 두 가지로 가른다.
Pre-Generated는 개발 중에 AI 도구로 만들어 게임에 담은 콘텐츠다.[^cs]
Live-Generated는 게임이 돌아가는 동안 AI가 만드는 콘텐츠이고,
이 경우 불법 콘텐츠를 막는 방어책을 설문에 적어야 한다.[^cs]
심사에서는 AI가 만든 결과물도 다른 콘텐츠와 같은 기준으로 보고,
게임이 판매 약관의 약속과 마케팅 자료에 맞는지를 확인한다.[^cs]

설문 FAQ는 설문만 채우면 무엇이든 낼 수 있느냐는 물음에 아니라고 답한다.[^cs]
공개했느냐와 별개로 Steam의 콘텐츠 규칙을 지켜야 한다는 뜻이다.
이 문서는 설문 본문에서 코드를 따로 거론한 문장을 찾지 못했다.
본문이 예로 든 것은 미술, 소리, 서사, 현지화다.[^cs]

이 서술은 2026년 1월에 바뀐 판본이다.
PCGamesN은 2026년 1월 17일에 Valve가 양식을 고쳐
“플레이어가 소비하는 것”에 초점을 맞추었다고 전했다.[^pcgn-jan26]
같은 보도에 따르면 이 범위에는 게임 속 콘텐츠뿐 아니라
상점 페이지, 커뮤니티 에셋, 마케팅 자료가 들어가고,
효율을 위한 개발 도구는 공개 없이 쓸 수 있는 것으로 보인다.[^pcgn-jan26]
2025년 11월에 GamingOnLinux가 인용한 이전 판본은
Pre-Generated를 미술, 코드, 소리 같은 개발 중 콘텐츠로 풀이했고,[^gol-sweeney]
현재 문서는 괄호 속 예에서 코드를 빼고 서사와 현지화를 넣었다.[^cs]
그러니 현재 설문 본문에 코드가 예로 나오지 않는 것은
이 개정에서 예시 목록이 바뀐 결과로 보인다.

문서의 나머지 부분에도 눈여겨볼 대목이 있다.
Live-Generated에 대해서는 성인 전용 성적 콘텐츠를
실시간으로 생성하는 게임을 지금은 내놓지 않겠다고 적는다.[^cs]
실시간 AI 서비스에 건당 비용이 든다면
Steam이 지원하는 결제 수단으로 받아야 한다는 안내도 있다.[^cs]
승인이 난 뒤에는 설문의 일부 항목을 Steam 지원팀을 거쳐야 고칠 수 있다.[^cs]

### 상점 페이지에서 보이는 공개 문구

HN에서 한 댓글러가 이번 Next Fest 첫 화면에서
가져왔다며 게임 네 개를 링크했다.[^freeone]
그 네 상점 페이지를 로그인 없이 열어 AI 공개 항목이 있는지 보았다.
페이지의 AI 공개는 “AI Generated Content Disclosure”라는
제목 아래 개발사가 직접 쓴 문장으로 나온다.
페이지 소스에서는 이 구역이 내용 설명자와 같은
`game_area_content_descriptors` 구역 안에 들어 있고,
개발사가 AI 콘텐츠 사용을 이렇게 설명한다는
고정 안내 문장 아래에 개발사 문구가 붙는다.[^ages]

| 게임                           | 공개 항목 | 공개 문구의 내용                                                                                                |
| ------------------------------ | --------- | --------------------------------------------------------------------------------------------------------------- |
| Ages TD Demo                   | 있음      | 미술 제작 과정에 AI 보조 도구를 쓰며, 아티스트가 직접 수정하고 마무리한다.[^ages]                               |
| BATTLE: PARTS & POWER Demo     | 있음      | 개발 중 코딩 보조와 미리 만든 시각 에셋에 생성형 AI를 썼고, 플레이 중에는 AI 콘텐츠가 생성되지 않는다.[^battle] |
| Leverage Real Estate Simulator | 없음      | 페이지 본문에 공개 항목이 보이지 않는다.[^leverage]                                                             |
| Naval Supremacy                | 없음      | 본문의 AI는 게임 속 AI 국가를 가리키며 공개 항목은 보이지 않는다.[^naval]                                       |

이 표가 말하는 범위를 좁게 읽어야 한다.
공개 항목이 없다는 사실이 그 게임이 AI를 쓰지 않았다는 뜻은 아니고,
있다는 사실이 공개가 정확하다는 뜻도 아니다.
이 문서는 게임의 실제 에셋이나 코드를 검사하지 않았다.
확인한 것은 개발사가 상점 페이지에 무엇을 적었느냐뿐이다.

그래도 읽을 만한 대비가 있다.
네 게임 중 둘은 AI 사용을 구체적으로 적었고, 하나는 코딩까지 적었다.
HN 댓글러는 이 네 게임이 코드부터 상점 페이지까지 전부 AI 산물이라고
주장했는데,[^freeone]
적어도 둘의 상점 페이지는 개발사 스스로 AI 사용을 밝히고 있다.
공개 의무가 작동하는 부분과 작동하지 않는 부분이 한 화면에 같이 보이는 셈이다.

### 공개 비율을 세 번 세어 보면

HN 토론에서는 신작의 대부분이 AI 게임이 된다는 예상과
“No AI”로 남을 게임이 거의 없을 것이라는 예상이 오갔다.[^preg-zero][^0x457]
공개 구역의 비율은 세 가지 방법으로 셀 수 있다.

첫째는 Haro의 전수 조사다.
Haro는 2023년 7월부터 2026년 7월까지 출시된
게임 53,597개의 상점 페이지에서 공개 구역의 유무를 세었다.[^haro1]
제도가 시작된 2024년 1월 이전의 값은 사후에 달린 공개라
거의 0에 가깝고, 2024년 2월에 공개 비율이 약 1%에서 약 7%로 뛰었다.[^haro1]
PC Gamer는 이 조사를 인용해 연도별 비율을
2024년 10.9%, 2025년 19.9%, 2026년 7월까지 30.8%로 전했다.[^pcg-haro]
Haro는 AI 공개를 단 신작이 제도 이전에는 월 13개 안팎이었다가
월 530개 안팎으로 늘었고, 같은 기간 공개가 없는 신작은
월 1,030개에서 1,320개로 완만하게 늘었다고 쓴다.[^haro1]
월 출시량 증가의 60~90%가 공개를 단 게임이라는 계산도 있다.[^haro1]

둘째는 PC Gamer 기자의 손으로 센 값이다.
2026년 6월 9일부터 약 일주일 동안 Steam에 나온 신작
338개의 상점 페이지를 일일이 열어 보니 120개가 공개를 달고 있었다.[^pcg-week]
기자는 공개가 있다고 해서 게임이 AI로 만들어졌다는 뜻은 아니라며,
상점 캡슐 이미지에만 AI를 쓴 경우가 많다고 덧붙였다.[^pcg-week]

셋째는 이 문서가 직접 센 값이다.
2026년 10월 21일에 Steam 검색에서 데모를 출시일 내림차순으로 놓고
첫 800개를 모았다. 이 가운데 612개가 10월 19일, 129개가 20일,
57개가 18일에 나온 것이었다.
이 800개에서 무작위로 80개를 뽑아(난수 시드를 고정했다)
상점 페이지를 로그인 없이 1.3초 간격으로 한 번씩 열었다.
나이 확인 화면을 넘기는 쿠키를 보냈다.
80개 모두 페이지가 열렸고 36개(45%)에 공개 구역이 있었다.
95% 신뢰구간(Wilson 방식)은 약 35~56%다.

| 출시일    | 데모 수 | 공개 구역 있음 | 비율 |
| --------- | ------- | -------------- | ---- |
| 10월 18일 | 5       | 0              | 0%   |
| 10월 19일 | 55      | 21             | 38%  |
| 10월 20일 | 19      | 15             | 79%  |
| 10월 21일 | 1       | 0              | 0%   |
| 합계      | 80      | 36             | 45%  |

이 표본에는 분명한 한계가 있다.
Steam 검색의 데모 목록이어서 Next Fest 참가작만 모은 것이 아니다.
표본이 80개이고 날짜별 칸은 더 작아서,
10월 20일의 79%가 우연인지 구조인지는 말할 수 없다.
스냅샷 하루의 값이며, 공개 구역의 유무만 세었다.
그래도 Haro의 연간 비율과 같은 방향의 값이며
신작의 3분의 1에서 절반쯤이라는 범위 안에 들어온다.

공개 36개의 문구를 사람이 읽고 분류해 보았다.
상점이나 마케팅 에셋을 언급한 것이 17개였고,
그 가운데 3개는 상점 이미지나 라이브러리 로고만 적었다.
번역과 현지화만 적은 것이 2개였다.
코드나 프로그래밍을 명시한 것은 8개, 음성은 5개,
음악이나 소리는 9개, 번역이나 현지화는 10개였다.
게임이 플레이 중에는 AI 콘텐츠를 만들지 않는다고 적은 것이 18개였고
실시간 생성을 밝힌 것은 하나도 없었다.
문구 길이는 3단어에서 104단어까지이고 중앙값은 30단어 안팎이다.
(영어가 아닌 문구 셋은 단어로 세기 어려워 어림값이다.)
한 문구는 “Translations of some texts.” 한 줄이었다.
분류는 한 사람이 읽고 한 것이라 경계 사례에서 달라질 수 있다.

Next Fest 자체의 규모도 보아 둘 만하다.
PC Gamer는 행사가 시작되기 직전인 10월 19일에
보도자료 미리보기 페이지에 8,011개가 올라 있고
이는 2026년 6월 행사의 약 두 배라고 썼다.[^pcg-nf]
다만 Steamworks 문서에서 미리보기는 데모 상태와 무관하게
등록된 모든 게임을 담고,
행사 화면에는 데모가 공개된 게임만 나온다.[^nfdoc]
그러니 8,011은 등록 수이지 플레이할 수 있는 데모의 수가 아니다.
RespawnFirst는 페이지 설명문에서 AI 보조 데모가 2,500개를 넘는다고 적었는데,
이 문서는 그 수치의 산출 방법을 확인하지 못했다.[^rf]

### 공개는 있지만 공식 필터는 없다

HN의 한 댓글러는 Steam이 AI 사용 여부를 이미 공개시키니
예와 아니오의 토글 하나만 추가하면 된다고 말했다.[^freeone2]
위에서 연 페이지들의 공개 항목은 자유 서술 문장이었고,
이 문서가 본 페이지에서는 범주별 체크 표시나 구조화된 값이 드러나지 않았다.
범주별 필터가 걸러 낼 수 있으려면 “미리 만든 시각 에셋”,
“미리 만든 오디오”, “실시간 생성”처럼
값이 나뉘어 있어야 하고, 지금 보이는 서술형 문구는 그 값을 담고 있지 않다.

그러나 예와 아니오의 토글은 기술적으로 이미 가능하다.
공개 구역이 있느냐 없느냐는 페이지 HTML에서 읽히고,
Haro는 이 값을 작은 기계 판독 흔적이라 부르며 게임 5만 3천여 개를 셌다.[^haro1]
SteamDB는 이 값으로 `AI Content Disclosed` 태그를 만들어
2025년 2월부터 목록에서 포함하거나
제외할 수 있게 했다고 보도됐다.[^steamdb-gol][^steamdb-lv]
공개 `appdetails` 응답에는 AI 항목이 없었으니
SteamDB가 값을 읽는 경로는 이 문서가 확인하지 못했다.[^appdetails]
받아 본 인기 태그 429개 가운데에는 AI 사용을 뜻하는 태그가 없고
`Artificial Intelligence` 태그만 있는데,
Haro는 이 태그가 달린 게임의 43%가 공개를 달았다고 센다.[^tagdata][^haro2]

이 간극은 필터의 난도를 올린다.
“AI 보조 도구를 쓴다”는 문장 하나와 “코딩
보조와 미리 만든 시각 에셋에 썼다”는 문장은
사람이 읽으면 다르지만 기계가 가르려면 해석이 필요하다.
Valve가 범주별 필터를 만든다면 먼저 공개 항목을 구조화해야 하고,
그 순간부터 범주를 어떻게 나눌지가 정책 결정이 된다.
이진 필터는 그 결정 없이도 만들 수 있고 SteamDB가 그 길을 먼저 갔다.

## 다른 장터와 규제는 어떻게 다루나

Steam의 공개는 법이 아니라 Valve가 장터에 거는 규칙이다.[^cs]
다른 장터와 법은 같은 문제를 다르게 푼다.
여기에 적은 것은 이 문서가 열어 본 자료의 범위다.

### itch.io: 범주를 고르게 하는 공개

80 Level은 itch.io가 2024년 11월에
생성형 AI 공개 항목을 에셋 제작자에게 필수로 만들었다고 전했다.[^itch]
“예”를 고르면 AI-Generated 태그가 붙고
그래픽, 소리, 텍스트와 대화, 코드를 따로 골라 하위 태그를 받는다.[^itch]
“아니오”를 고르면 No AI 태그가 붙는다.[^itch]
공개하지 않은 AI 에셋은 둘러보기 목록 노출에서 빠진다고 안내했다.[^itch]
80 Level은 공지가 에셋만 언급해
게임에도 적용되는지는 불분명하다고 덧붙였다.[^itch]

Steam과의 차이는 두 가지다.
itch.io는 코드를 독립 범주로 두고 범주별 태그로 만들었다.[^itch]
Steam은 코드를 예시 목록에서 뺐고 공개를 자유 서술로 받는다.[^cs][^ages]
이 문서는 itch.io 쪽 필터의 현재 동작을 직접 확인하지 못했다.

### Epic: 공개 요구에 반대하는 쪽

Tim Sweeney는 2025년 11월에
AI 태그가 미술 전시와 디지털 콘텐츠 라이선스 장터에는 의미가 있지만
앞으로 거의 모든 제작에 AI가 쓰일
게임 장터에는 맞지 않는다고 썼다.[^sweeney-tweet][^gol-sweeney]
mp1st는 2026년 6월 PC Gamer 인터뷰에서 Sweeney가
Valve의 요구를 무책임하다고 부르고
공개가 “주홍글씨”가 되어
적대적인 공동체가 게임을 죽이려 든다고 말했다고 전했다.[^mp1st]
그는 생산성을 높이는 도구를 쓰지 않으면
경쟁에서 질 것이라고도 말했다고 한다.[^mp1st]

이 문서가 확인한 범위에서
Epic이 공개 요구를 두었다가 없앴다는 근거는 찾지 못했다.
Epic Games Store에 공개 요구가 있는지는 문서로 확인하지 못했고
Sweeney의 반대 발언만 확인했다.
GOG, Nintendo, Sony의 공개 규칙은 이 문서가 열어 보지 못했다.

### EU AI Act: 게임에 일괄 라벨을 요구하지 않는다

AI Act 50조는 네 가지 상황을 다룬다.
AI와 직접 상호작용하는 시스템에 대한 알림,
생성형 시스템 제공자의 기계 판독 가능한 표시,
감정 인식과 생체 분류의 알림,
딥페이크와 공익 목적 글의 공개다.[^eu50]
50조는 2026년 8월 2일부터 적용되기 시작했다.[^aljaz]

게임 개발사가 맞닥뜨릴 수 있는 것은 딥페이크 조항이다.
딥페이크를 만드는 AI 시스템의 배포자(deployer)는
그것이 인공적으로 생성되었음을 밝혀야 하고,
명백히 예술적, 창작적, 풍자적, 허구적이거나 그에 준하는 작품의 일부라면
작품의 감상을 해치지 않는 방식으로
그런 콘텐츠가 있다는 사실만 밝히면 된다.[^eu50]
이 문서가 읽은 조항 본문에는 AI로 만든 게임에 일괄 라벨을 붙이라는 요구가 없다.
게임을 직접 겨냥한 위원회 지침은 열지 못했다.

## 반응 지도

HN 토론은 210개 댓글로, 필터를 사실상 환영하는 쪽과
라벨 자체가 무의미하다는 쪽이 갈렸다.
반응은 여덟 개의 시각으로 정리된다.

| 시각                        | 핵심 주장                                     | 대표 댓글                          |
| --------------------------- | --------------------------------------------- | ---------------------------------- |
| 필터는 금지가 아니다        | 걸러 내는 선택권이지 금지가 아니다            | ncallaway, alpaca128               |
| 라벨의 정의가 무너진다      | 코드까지 치면 거의 모든 게임이 AI 게임이 된다 | underyx, preg_match, pantsforbirds |
| 자기 신고는 거짓말을 부른다 | 라벨이 불이익이면 숨긴다                      | fireant, preg_match, ympb121       |
| 문제는 AI가 아니라 노력이다 | 원하는 건 성의 있는 게임이다                  | andai, sosodev, joshstrange        |
| 코드와 아트는 다르게 읽힌다 | 플레이어는 눈에 보이는 에셋으로 판단한다      | dgunay, linuxftw, spencerflem      |
| 문턱과 큐레이션             | 수수료, 심사, 사람 큐레이터가 답이다          | ThrowawayR2, tintor, himata4113    |
| Next Fest의 구조            | 첫 며칠 무작위 노출이 문제를 키운다           | Corence, POiNTx                    |
| 소규모 개발자의 처지        | 복제와 낙인이 모두 위협이다                   | mr_freeman, vegnus                 |

## 시각별 분석

### 필터는 금지가 아니다

토론의 출발점은 “금지”라는 말을 둘러싼 오해다.
한 댓글러는 “ban Z”가 문제 해결책으로 게으르다고 썼다.[^rivet]
이에 한 댓글러가 사용자가 고르는 필터와 금지는 아주 다르지 않으냐고
되물었고,[^ncallaway]
또 다른 댓글러는 요청의 내용이 금지가 아니라 선택권이라고
정리했다.[^alpaca-filter]
기사의 ScalesGhost 요청도 Discovery Queue에서
“내가” 거르게 해 달라는 개인 설정이다.
한 댓글러는 AI를 얼마나 썼는지는 상관없고 썼느냐만 보고 싶다며,
좋은 게임을 놓치는 것은 자기 몫이라고 썼다.[^weezing]
다른 댓글러는 새 게임의 90%가 걸려도 상관없다고 했다.
개발사가 낙인을 신경 쓰지 않는다면 정직한 것이고,
품질은 이미 리뷰가 말해 주니
걸러진 목록이 품질을 뜻할 필요는 없다는 것이다.[^alpaca-90pct]

**분석.** 금지는 플랫폼이 공급자에게 가하는 제재이고
필터는 소비자가 쓰는 도구다.
금지는 정의가 틀리면 억울한 개발자를 낳지만,
필터는 정의가 틀려도 소비자가 그 필터를 쓰지 않으면 그만이다.

**비평.** 이 구분은 맞지만 필터의 비용을 줄여 주지는 않는다.
필터가 결과를 가르는 순간 개발자에게는 사실상 금지와 같은 압력이 된다.
HN에서도 필터가 생기면 매출에 영향이 갈 테니 공개를 피하게 된다는 반론이 나왔다.

**인사이트.** 필터의 정당성은 의도가 아니라 정확도에 달려 있다.
소비자 선택권이라는 말이 방패가 되려면
라벨이 소비자가 원하는 것을 정확히 가리켜야 한다.
이 구분은 숫자로 시험해 볼 수 있다.
한 댓글러가 가정한 90%도,
최근 게임 중 “No AI”로 남을 것이 거의 없을 것이라는
다른 댓글러의 예상도[^0x457]
공개 구역을 센 값인 신작의 3분의 1 안팎보다 크다.[^pcg-haro]

### 라벨의 정의가 무너진다

가장 큰 논쟁은 무엇을 AI 게임으로 부를지였다.
한 댓글러는 파티클 효과, 메뉴 배치, 아이콘,
애니메이션 키프레임이 모두 코드로 표현되므로
AI가 코드 일부를 썼다는 이유만으로 라벨이 붙으면
대다수 게임이 걸려 의미를 잃는다고 주장했다.[^underyx]
이에 대해 라벨이 싫으면 AI를 쓰지 않으면 된다는 반론이 나왔다.[^no-multitudes]
반론자는 디버깅에 AI를 쓴 프로젝트도 라벨이 붙어야 하고
개발사는 공개문에 사정을 적으면 된다고 답했다.[^no-multitudes2]

다른 댓글러는 그렇게 하면
새 게임 중 AI 없음으로 인정될 게임이 0%라고 단정했다.[^preg-zero]
반론은 특정 개발사가 생성형 AI를 쓰지 않는다는
구체적 사례를 들었고,[^no-multitudes3]
재반론은 사례를 믿지 않는다며
라이브러리와 검색 요약까지 끌어들였다.[^preg-zero2]
또 한 댓글러는 이진 플래그는 결국 거의 모두가 AI와 접촉했으니 쓸모가 없어지고,
엔진과 프레임워크에 들어간 AI까지 공개해야 하느냐고 물었다.[^pants-binary]
한 댓글러는 AI가 쓰인 디버깅 세션 하나로 “AI 없음” 라벨이 뒤집히는 것이 맞느냐고
따졌다.[^pants-debug]
이 단정을 측정과 견주어 볼 수 있다.
단정대로라면 새 게임의 공개 비율이 100%에 가까워야 하지만
2026년 신작의 공개 비율은 30.8%였고,[^pcg-haro]
퍼블리셔 3만 7천여 곳 가운데 80%는 공개를 단 게임을 한 번도 내지 않았다.[^haro2]
공개 구역은 AI를 썼는지가 아니라 썼다고 적었는지를 세므로,
이 차이를 곧바로 AI 사용률의 차이로 읽을 수는 없다.
GDC 조사에서 생성형 AI를 일에 쓰는 업계 종사자는 36%,
게임 스튜디오 소속은 30%였고, 쓰는 사람의 47%가 코드 보조에 썼다.[^gdc]
사실상 모든 개발자가 쓴다고 단언한 댓글과는
조사 범위가 달라 단순 비교는 안 되지만,
스튜디오 종사자 전체가 쓴다는 근거는
이 조사에서 나오지 않는다.[^preg-all]

라벨을 어떻게 나눌지는 장터마다 다르다.
itch.io는 그래픽, 소리, 텍스트와 대화, 코드를 따로 고르게 하고,[^itch]
Polygon Treehouse가 2025년 2월에 낸 No Gen AI Seal은 반대로
생성형 AI를 쓰지 않았다는 쪽을 표시하는 도장이며
그림, 영상, 소리, 글을 생성형 AI의 범위로 정의한다.[^treehouse]
한 댓글러는 대부분의 플레이어에게는 단순한 필터면 충분하겠지만
AI 미술과 AI 코드를 나눈 태그도 가치가 있을 것이라고 덧붙였다.[^summermusic]

**분석.** 이 논쟁에는 두 개의 서로 다른 라벨이 섞여 있다.
하나는 개발 과정의 AI 사용이고,
다른 하나는 플레이어에게 배달되는 콘텐츠가 AI 산물이냐다.
앞의 정의로는 단정적 주장대로 거의 모두가 걸리고,
뒤의 정의로는 대부분의 코딩 보조가 빠진다.

**비평.** Valve 문서는 뒤의 정의에 가깝다.
문서는 효율을 위한 도구 사용이 초점이 아니라고
말하고 배달되는 콘텐츠를 본다.[^cs]
그러니 “코딩에 AI를 한 번이라도 쓰면
라벨이 붙는다”는 전제 위에 쌓인 반론 상당수는
Valve의 현재 정의에 정확히 들어맞지 않는다.
다만 개발사가 BATTLE 사례처럼 코딩까지 자발적으로 적는 경우가 있어서,[^battle]
라벨의 실제 범위는 문서가 아니라 개발사의 서술 습관이 정한다.

**인사이트.** 필터에서 먼저 정할 것은 어떤 단계의 AI인지다.
한 댓글러가 제시한 순서가 쓸 만하다.
사무와 문서화, 조사, 임시 에셋, 업스케일링, UI 번역,
최종 에셋, 최종 코드의 순으로 심해진다는 기울기다.[^dijit]
이 기울기를 서술형 공개 문구에서
구조화된 항목으로 옮기는 것이 필터의 선행 조건이다.

### 자기 신고는 거짓말을 부른다

공개는 개발사가 스스로 적는 방식이라는 점이 다음 쟁점이다.
한 댓글러는 지금 AI 라벨을 달면 손해뿐이라 아무도 달지 않을 것이므로
필터가 쓸모없을 것이라고 썼다.[^fireant]
다른 댓글러는 모두가 거짓말할 유인이 있다고 말했고,
게임이 비공개 소스라 아무도 코드를 읽지 않으니
확인할 수 없다는 점을 근거로 들었다.[^preg-lie]
이에 대해 공개해야 할 항목에 대해 거짓을 쓰면
구매 결정에 영향을 주는 사실을 속이는 것이라
사기가 될 수 있다는 응수가 나왔다.[^alpaca-fraud]
누가 AI를 표시할지도 문제로 제기됐다.
업로더는 거짓말하기 쉽고, 플레이어는 오탐이 많고,
Steam 중재자는 일이 너무 많다는 것이다.[^ympb]
단속이 없는 규칙은 지켜지지 않는다는 비유도 나왔다.
유턴 금지 표지판이 있어도 경찰이 지켜보지 않으면
사람들은 유턴한다는 것이다.[^yipinwong]

한 댓글러는 밝히지 않는 개발사를 의심하며 AI를 자랑스러워하면서
라벨은 싫어하는 모순을 짚었다.[^slowhadoken]
반대로 공개한 개발사가 어디선가 나타난 사람에게 모든
작업을 무효화당하는 일이 있다는 답이 이어졌다.[^vegnus]
공개의 비용이 불균등하다는 이야기다.

RespawnFirst는 올해 일찍 Tainted Grail과 RideShare Stimulator가 Steam에서
AI 사용을 숨겼다고 보도했다며,
필터가 생기면 더 많은 게임이 숨기려 할 것이라고 예상한다.[^rf]
이 보도는 숨김의 사례이자 필터가 만들 유인을 추정한 글이며,
이 문서는 해당 보도의 사실관계를 따로 확인하지 못했다.

공개가 사후에 바뀌는 흔적은 데이터에도 보인다.
Haro가 Wayback Machine으로 공개 구역이 처음 나타난 시점을 확인하니
매출이 의미 있는 AI 게임의 22%가 출시 뒤에 공개를 달았고,
그런 추가가 2026년 1월 Valve의 정책 개정 무렵에 몰려 있었다.[^haro1]
Haro는 이를 일종의 준수 점검에 따른 현상으로 읽는다.[^haro1]
그래서 2026년의 공개 비율 증가에는
옛 게임이 공개를 뒤늦게 단 몫이 섞여 있다.[^haro1]
Steamworks 문서는 심사를 통과한 데모 빌드를 고쳐도
그 변경은 다시 심사하지 않는다고 적는다.[^nfdoc]

**분석.** 자기 신고 제도는 제재가 신고를 상회해야 작동한다.
Steam 심사는 AI 결과물을 일반 콘텐츠와 같은 기준으로 보고
상점 페이지와 빌드를 대조한다고 밝힌다.[^cs]
그러나 심사가 에셋의 출처까지 판별한다는 말은 문서에 없다.

**비평.** 거짓 신고의 문제는 필터가 있든 없든 존재한다.
다만 필터가 신고를 불이익과 직결하면 정직한 개발사만 걸리는 역선택이 생긴다.
범주별 필터라면 정직하게 구체적으로 쓴 개발사가
대충 쓴 개발사보다 더 많이 걸러질 수 있다.
이진 필터에서는 한 줄만 쓴 개발사도 같은 칸에 들어간다.

**인사이트.** 필터를 설계하는 쪽의 과제는 정직의 이득을 만드는 일이다.
공개가 상세할수록 노출에서 손해를 보지 않거나,
허위 공개가 드러났을 때의 제재를 명시하는 방법이 있다.
개발사 쪽에서는
지금 쓰는 문구가 몇 달 뒤 필터의 입력이 될 수 있음을 전제로 써야 한다.

### 문제는 AI가 아니라 노력의 신호다

토론에서 가장 많이 반복된 진단이다.
한 댓글러는 사람들이 원하는 것이 “no dogshit” 필터,
즉 노력과 성의의 필터라고 했고,
슬롭은 투입한 시간에 반비례한다고 썼다.[^andai]
다른 댓글러는 사람들이 실제로 원하는 것은 슬롭이 아닌 게임인데
그 정의는 불가능에 가깝다고 말했고,[^sosodev]
또 다른 댓글러는 슬롭이라는 말의 뜻이 변해 AI 산물이면
무엇이든 슬롭이라 부르게 되었다고 지적했다.[^sohcahtoa]
한 댓글러는 슬롭이 품질뿐 아니라 냉소의 정도를 가리킨다고 설명했다.
진심을 쏟은 형편없는 게임은 슬롭이 아니고,
영혼 없이 잘 다듬은 대량 생산물은 슬롭이라는 구분이다.[^boba]

다른 쪽에서는 이전에도 쓰레기는 있었다는 반응이 나왔다.
에셋 플립은 AI 이전에도 있었고
Steam은 그 시절에도 큐레이션이 약했다는 말이다.[^ox-rs]
이에 한 댓글러는 “AI 이전에도 있었다”는 논법이 지겹다며
양의 차이가 어느 순간 종류의 차이가 된다고 받아쳤다.[^mort]
또 한 댓글러는 걸러야 할 집합이 10배 늘면 필터 정확도가 올라도
새어 나오는 나쁜 게임의 수가 오히려 늘 수 있다고 계산해 보였다.[^ben-w]

앞서 게임 네 개를 링크한 그 댓글러는
이번 슬롭은 코드도 엉망이고 상점 페이지까지 AI가 만들어서,
오타가 많고 스톡 에셋을 쓴 페이지로 저성의를 알아보던 전통적 단서마저 사라졌다고
했다.[^freeone]
이 주장 중 게임의 질은 이 문서가 직접 확인하지 못했다.
그러나 단서의 소실이라는 지적은 필터 논쟁의 핵심과 맞닿아 있다.
AI가 저성의의 겉모습을 지워서,
플레이어가 쓰던 휴리스틱이 무효가 됐다는 이야기다.

공개 구역이 노력의 대리 변수로 얼마나 쓸 만한지는 Haro의 자료로 일부 볼 수 있다.
평점이 있는 게임 2만 6천여 개에서 공개가 있는 쪽의 평균 긍정률은 77%,
없는 쪽은 81%였고(중앙값은 80%와 85%),[^haro2]
리뷰 100개에 이르는 비율은 공개가 있는 쪽이 없는 쪽의 약 55%였다.[^haro1]
Haro는 이를 붕괴가 아니라 4~6점의 일관된 불이익으로 읽는다.[^haro2]
성공한 AI 게임 138개와 실패한 AI 게임 400개의 공개 문구도 달랐다.
실패 쪽은 중앙값이 13단어이고 열 단어 이하 한 줄이 35%였는데,
성공 쪽은 중앙값이 22단어이고 그런 한 줄은 13%였다.[^haro1]

AI에 대한 일반적 반감을 두고도 논쟁이 있었다.
한 댓글러는 Gallup 조사에서 미국인의 39%가
AI가 득보다 해가 크다고 답했고 득이 더 크다는 응답은 9%라고 들었다.[^lambda]
Gallup 본문에서 이 값은 2026년 조사 결과이고
52%는 득과 해가 같다고 답했다.[^gallup]
다른 댓글러는 그 조사가 AI 슬롭을 싫어하는 것과
AI의 어떤 사용이든 싫어하는 것을 가르지 못한다고 반박했다.[^0x457]
게임 플레이어만 대상으로 한 조사로는 Quantic Foundry가 있다.
2025년 10~12월에 게이머 1,799명에게 물은 결과
85%가 게임 속 생성형 AI에 중립 이하의 태도를 보였고
63%가 가장 부정적인 응답을 골랐다.[^qf]

**분석.** 플레이어의 진짜 질문은 이 게임에 누가 얼마나 마음을 썼는가다.
AI 사용 여부는 그 질문의 대리 변수로 쓰일 뿐이다.
대리 변수는 과거에 쓰던 단서(스톡 에셋, 어색한 문장)가 무너지면서 수요가 커졌다.

**비평.** 대리 변수가 부정확하면 오탐과 미탐이 모두 생긴다.
AI로 만든 좋은 게임이 걸리고, AI 없이 만든 게으른 게임이 통과한다.
한 댓글러가 말했듯 어떤 필터도 실제 재미와는 다른 차원의 정보이고,[^dogleash]
그것이 필터를 쓰지 말아야 할 이유는 아니지만 믿을 근거도 아니다.

**인사이트.** 노력을 직접 보여 주는 신호가 필요하다.
한 댓글러가 낸 제안 중 한 시간 분량의 실제 플레이 영상을 제출시키자는 아이디어는
가짜로 만들기 비싼 신호라는 점에서 눈여겨볼 만하다.[^himata]
데모에 평점을 달 수 없다는 구조적 한계를 지적한 댓글도 같은 방향이다.[^syabro]

### 코드와 아트는 다르게 읽힌다

코드에 쓴 AI와 에셋에 쓴 AI를 같은 라벨 아래 둘 것인지를 놓고 논쟁이 이어졌다.
한 댓글러는 코드를 쓰는 개발자는 결국 에셋도 같은 식으로 대충 만들게 된다고
썼다.[^archagon]
다른 댓글러는 소비자는 코드를 예술적 표현으로 여기지 않으며
아트가 훨씬 명확한 AI 단서라고 말했다.[^dgunay]
이에 대해 게임의 재미는 코드가 구현한 규칙에서 나오므로
아트가 더 중요하다는 근거가 없다는 반박이 나왔다.[^linuxftw]
재반박은 AI가 규칙을 충실히 구현하게 시키는 것은 가능해도 세부가
중요한 예술적 비전을 AI에게 맡기면 손실이 크다는 것이었다.[^spencer]
같은 질문에 npteljes는 실용적인 차이로 아트는 직접 마주하지만 코드는
그렇지 않다는 점을 들었다.
아트는 사람의 표현과도 이어져 있어, 이미 영혼이 덜한 아트가 많았는데
AI가 그것을 전에 없던 수준으로 밀어붙였다고 덧붙였다.[^npteljes]

코드에 AI가 들어갔는지는 이미 질문이 아니라고 본 댓글도 있었다.
슬롭과 아닌 것을 가르는 것은 AI 사용 여부가 아니라 개발자가 들인 정성이고,
게임에서 코드는 결과물로만 쓸모가 있으며
플레이어는 코드의 깔끔함에 감탄하지 않는다는 주장이다.[^jerf]
이 댓글은 미술은 더 복잡한 문제라며 따로 떼어 놓았다.
다른 댓글러는 플레이어가 코드를 모르니
코드에 대한 감정을 말하기 어렵다고 짚었다.[^dugidugout]
또 다른 댓글러는 미술 에셋이 가장 깊은 쪽이고 코드는 그 뒤에 두겠다고 했다.
코드 안에도 가벼운 Copilot 사용부터
바이브 코딩까지 기울기가 따로 있기 때문이다.[^debugnik-gradient]

플레이어 조사도 이 구분과 맞물린다.
Quantic Foundry의 조사에서 가장 부정적인 용도는
미술, 음악과 효과음, 서사와 대화 같은 창작 용도였고,
난이도 조정 같은 비창작 용도는 상대적으로 덜 부정적이었다.[^qf]
조사 본문에는 코드에 쓰는 AI를 다룬 항목이 보이지 않고,
한 독자가 다음 조사에서는 프로그래밍을 물어 달라는 댓글을 남겼다.[^qf]
GDC의 2026년 조사에서는 업계 종사자의 52%가
생성형 AI가 업계에 부정적 영향을 준다고 답했고
이는 전년 30%, 전전년 18%에서 늘어난 값이다.[^gdc]

실무자 쪽 증언도 있었다.
한 댓글러는 아는 보드게임 디자이너가 JS를
모르면서도 AI로 웹 프로토타입을 만든다고 하면서,
엉성한 코드가 엉성하지 않은 기능 요구를 충족시킬
수 있다는 점을 받아들이게 되었다고 했다.[^debugnik]
다른 댓글러는 종이에 그림을 그려 모델링한
뒤 Claude에게 비율을 맞추게 하는 방식이라면
출발점에 사람이 넣은 정보의 밀도가 높을수록 마음이 놓인다고 말했다.[^mrnotcrazy]

**분석.** 분기점은 에셋이냐 코드냐보다 사람이 넣은 정보가 시작점에 있느냐다.
토론에서 가장 설득력 있던 조건은 사람이 낸 씨앗에서 시작했는가였다.

**비평.** 이 기준은 정직하게 적기도 검증하기도 어렵다.
씨앗의 크기를 라벨 하나로 담을 수 없다.

**인사이트.** 공개 문구에서 가장 값진 정보는 사람이 한 일이다.
Ages TD Demo의 공개 문구가 이 점에서 모범에 가깝다.
AI 보조 도구를 썼다는 말에서 멈추지 않고,
아티스트의 직접 수정과 마무리를 적었다.[^ages]

### 문턱과 큐레이션

정책 쪽 해법도 많이 나왔다.
한 댓글러는 등록 수수료를 크게 올리고
그 수익으로 사람 큐레이션을 늘리자고 했다.[^throwaway-fee]
다른 댓글러는 지금 100달러인 등록 수수료가 코딩 에이전트로
게임을 만드는 비용에 맞지 않는다고 썼다.[^tintor]
이 수치는 댓글러의 서술이며 이 문서는
Steamworks의 현재 등록 수수료를 확인하지 못했다.
수수료를 올리자는 제안에는 가난한 나라의 진짜 인디 개발자는 어떻게 출시하느냐는
반문이 달렸다.[^dmantis]
답은 다른 마켓플레이스를 쓰거나 사전 예약 캠페인을 열라는 것이었다.[^ekaros-alt]
이 답은 Steam 밖에서 판매하라는 뜻이어서, 수수료가 문턱이 되는 사람에게는
플랫폼을 포기하라는 말과 같다.
한 댓글러는 한때 엄격한 큐레이션이 있었을 때 인디 게임이
막힌다는 불만이 컸다는 점을 상기시켰다.[^throwaway-curation]
또 다른 댓글러는 Greenlight를 되살리고
한 시간짜리 실제 플레이 영상 제출을 요구하자고 제안했다.[^himata]

반대편에는 Valve가 승자를 가르는 역할을 맡는 것이 불편하다는 의견이 있었다.
이 댓글러는 호스팅하고 수익을 가져가는 쪽이 시장의 승자까지 정하면
안 되며 서로 다른 취향의 인간 큐레이터가 필요하다고 했다.[^tadpole]
다른 댓글러는 필요한 것은 AI/비AI가 아니라 Reddit 같은 메타 중재 같은 것이라고
말했다.[^jrm4]

환불과 평점이라는 기존 장치에 대한 평가는 갈렸다.
2시간 이내 환불과 사용자 리뷰가 이미 있다는 의견이 있었고,[^tintor]
이에 대해 리뷰는 구매 후에야 달리고
합의 평점이 보이기 전에 슬롭 제출자는 이미 목적을 이루며,[^throwaway-rating]
평점이 LLM이 쓴 짧은 댓글과 낮은 플레이 시간으로 조작되고
있다는 목격담도 나왔다.[^mh-rating]
또 한 댓글러는 리뷰를 달 의욕이 슬롭의 홍수 앞에서 꺾인다고 말했다.[^overfeed]

**분석.** 논점은 누가 비용을 지느냐다.
수수료를 올리면 개발사가 비용을 지고,
사람 큐레이션은 Valve가 지고, 필터는 플레이어가 선택적으로 진다.
환불과 평점은 플레이어가 구매 후에야 지는 비용이다.

**비평.** 제안은 대체로 저성의 게임이 늘어난 양에 대한 처방이고
AI와 직접 관련이 없다.
이 점이 필터 요구가 AI라는 이름을 달고 나온 이유와 해법의 간극이다.

**인사이트.** 양 문제에는 양을 건드리는 도구가,
질 문제에는 질을 보여 주는 도구가 필요하다.
AI 필터는 그 중간쯤의 도구이며 둘 다 해결하지 못한다.

### Next Fest의 구조가 문제를 키운다

한 댓글러는 Next Fest의 처음 이틀은 페이지의 기본 화면이 무작위라서
슬롭이 특히 나빠 보인다고 설명했다.[^corence]
Steamworks 문서가 이를 뒷받침한다.
문서는 모든 참가작에 가시성을 주려는 취지에서
행사 첫 며칠은 이름이 붙은 목록과 개인화 구역을 제외한 모든 곳이 완전 무작위라고
적는다.[^nfdoc]
며칠이 지나면
로그인한 사용자에게는 행사 중 사용자 행동에
기반한 알고리즘 추천이 나타난다고도 한다.[^nfdoc]
다른 한 댓글러는 참가 개발자로서 이틀이 지나면
인기 게임이 올라오니 이틀 뒤에 보라고 권했다.[^poin]
기사의 마지막 조언과 같은 취지다.

Next Fest의 참가 요건은 낮다.
문서가 적은 요건은 이전에 Next Fest에 참가한 적이 없을 것,
공개 상점 페이지가 있을 것, 행사 시작 때 공개 데모가 있을 것 등이다.[^nfdoc]
이 요건은 AI 여부를 묻지 않으며, 품질을 보장하는 문턱도 아니다.

**분석.** 무작위 노출은 취지상 작은 팀에 유리하게 설계되었고,
슬롭 제출자에게도 똑같이 유리하다.
행사 첫날의 인상이 나쁜 이유는 AI 때문만이 아니라 노출 설계 때문이다.

**비평.** 그래서 첫날 인상으로 AI를 비난하는 것은 원인을 헷갈리는 일일 수 있다.
다만 AI가 제출의 양과 형식을 바꿨는지는 이 문서가 보지 못했다.
HN 참가자 중에는 이번 행사의 게임 수가 지난 행사보다 크게 늘지 않은 것 같다고
말한 사람도 있지만,[^poin]
PC Gamer는 행사 시작 직전 미리보기 페이지의 등록 수가
2026년 6월 행사의 약 두 배라고 적어 이 인상과 어긋난다.[^pcg-nf]
등록 수와 실제 플레이할 수 있는 데모의 수는 다르다는 점을 감안해도,
참가작의 양이 늘었다는 쪽에 무게가 실린다.[^nfdoc]

**인사이트.** 첫 며칠에 한해 임시 필터나 신뢰 신호를 두는
것이 전면적 AI 필터보다 비용 대비 효과가 클 수 있다.
이는 이 문서의 추정이며 근거는 위의 구조 설명뿐이다.

### 소규모 개발자에게 닿는 영향

필터는 양쪽 개발자에게 다르게 작용한다.
한 댓글러는 코딩 에이전트 사용이 인디와 1인 개발자에게 생존 문제가 되었고,
게임이 공개되는 순간 vibe coder가 개념을 복제해 낼 수 있다고
걱정했다.[^mr-freeman]
RespawnFirst는 퍼블리셔 Alliance Arts와 개발사 WHO YOU가
Drunken Goddess Reflux의 공개 데모를 취소하고
비공개 플레이테스트로 돌렸다고 전한다.[^rf]
이 보도는 복제를 막으려는 조치라고 설명하지만,
이 문서는 그 인과를 확인하지 못했다.

다른 댓글러는 높은 눈높이를 가진 경험 많은 개발자가 AI로 에셋을 뽑아도
재미있는 게임은 인내와 미세 조정에서 나온다고 썼다.[^wincy]
다른 댓글러는 AI를 도구로 쓰는 경우와 통째로 vibe coding한
경우는 같은 통에 담기지 않는다고 구분했다.[^mysterydip]
반면 성공한 인디 개발자 중에는 AI를 전면
거부하는 이들이 많다는 증언과,[^archagon2]
쓰는 사람이 많아도 홍보 때문에 말하지 않을 뿐이라는 반론이 부딪쳤다.[^cubefox]
한 댓글러는 AI를 쓴 개발사가 소비자 반응을 두려워해 손을 들지 않는다고
했고,[^joshstrange]
공개하면 불이익을 받는 현실과 숨기는 개발사를 의심하는 정서가 서로를 키운다.

**분석.** 필터의 비용은 AI를 도구로 정직하게 쓰는 소규모 개발자에게 몰린다.
AAA는 공개 여부와 무관하게 마케팅과 브랜드로 버틴다.

**비평.** 반대로 필터가 없는 쪽의 비용은 AI 없이
만드는 소규모 개발자의 발견 가능성에 몰린다.
어느 쪽 비용이 더 큰지를 이 문서는 측정하지 못했다.

**인사이트.** 개발자가 지금 할 일은 라벨 논쟁의 승패를 기다리는 것이 아니다.
사람이 한 일을 구체적으로 적어 두면 필터가 생겨도, 생기지 않아도 손해가 없다.

## 비평

중심 주장을 가장 강하게 세우면 이렇다.
“No AI” 이진 필터는 정의가 불가능하고 신고는 검증되지 않으며
그 결과 정직한 쪽만 불이익을 받으므로,
필터가 아니라 노력과 품질을 보여 주는 신호가 필요하다.

이 주장을 받치는 근거는 세 가지다.
Valve의 현재 공개 항목은 서술형이다.[^ages]
Valve의 문서는 효율을 위한 도구 사용을 초점에서
제외하므로 라벨의 범위가 이미 모호하다.[^cs]
HN 토론에서 정의 문제가 가장 길게, 가장 해결되지 않은 채 남았다.

근거가 멈추는 곳도 분명하다.
첫째, 서술형이라는 관찰은 이 문서가 연 네 페이지와 표본 80개에서 나온 것이다.
Valve가 내부적으로 구조화된 값을 따로 저장하고 있을 가능성은 배제하지 못한다.
둘째, 거의 모든 개발자가 AI를 쓴다는 단정은 HN 댓글러들의 서술이며
근거 자료가 제시되지 않았고, GDC 조사의 사용률과도 거리가 있다.[^gdc]
셋째, 라벨이 있어도 플레이어가 거의 쓰지 않을 것이라는 예측이나
라벨이 있으면 플레이어가 넓게 쓸 것이라는 예측이나 모두 데이터가 없는 추정이다.

기사와 토론에서 약한 고리는 이렇다.
“AI라서 나쁘다”와 “나쁜 게임이 AI로 쏟아진다”를 섞는 논법이다.
기사 속 이용자들도 AI 자체보다 슬롭을 말하고 있다.
첫날의 인상을 근거로 삼는 점도 약하다.
행사 구조상 첫날은 가장 무작위한 화면이다.[^nfdoc]

이 문서의 중심 주장에도 한계가 있다.
공개 구역의 유무만으로 만든 이진 필터는 이미 있다.[^steamdb-gol]
Haro는 같은 값으로 신작의 3분의 1 안팎이 공개를 달았음을 셌다.[^haro1]
그러므로 병목은 데이터의 유무가 아니라 값이 무엇을 뜻하느냐다.
이 문서가 센 공개 36개 중 3개는 상점 에셋만, 2개는 번역만 적었으니
이진 값은 미술 전체를 만든 게임과 로고 한 장에 쓴 게임을 같은 칸에 넣는다.
반대로 공개가 없다는 사실은 AI를 쓰지 않았다는 뜻이 아니다.
공개 비율의 증가에는 사후에 달린 공개가 섞여 있고,[^haro1]
GDC의 사용률 36%와 공개율 31%가 같은 양을 재는 값이라는 근거도 없다.[^gdc]

반대로 정의 불가능론에도 약점이 있다.
정의가 어렵다는 이유로 라벨을 포기하는 것은 영화 등급이나
성인 콘텐츠 표시에도 똑같이 적용되는 논리이고,
Steam은 이미 콘텐츠 설문으로 성인 콘텐츠를 가르고 있다.[^cs]
한 댓글러가 말했듯 필터는 불완전해도 쓰는 사람에게는
1차 걸러내기로 충분히 쓸모가 있다.[^dogleash]
정의의 난점은 라벨을 만들지 말아야 한다는 근거가 아니라
라벨을 어떻게 나눠야 하는지를 정해야 한다는 근거다.

## 인사이트

첫째, 이진 필터에는 데이터가 이미 있고 모자란 것은 값의 뜻이다.
공개 구역의 유무는 페이지에서 읽히고
SteamDB가 그 값으로 필터를 냈다.[^steamdb-gol]
그 값은 상점 이미지 한 장에만 AI를 쓴 게임과
미술 전체를 만든 게임을 같은 칸에 넣는다.
범주별 필터를 원한다면 그때는 데이터 구조가 병목이다.
이 문서가 본 공개 항목은 서술형이었고, 서술형으로는 범주별 필터를 만들 수 없다.
Valve가 그 필터를 낸다면 첫 단계는 공개 항목의 범주화이고,
그 범주에서 정책적 선택이 벌어진다.
이 점이 HN 토론의 정의 논쟁보다 앞선다.

둘째, 범주를 나눈 필터는 이진 필터보다 방어하기 쉽다.
토론에서
나온 기울기와 Valve가 이미 가르는 Pre-Generated와 Live-Generated의 구분을 합치면
최소한 세 칸이 나온다.
개발 중 도구만 쓴 경우, 배달되는 미리 만든 콘텐츠, 실시간 생성이다.
이 세 칸은 자기 신고의 부담도 줄이고 오탐도 줄인다.
이 구성은 이 문서의 제안이며 Valve의 계획이 아니다.

셋째, 정직한 공개가 이득이 되는 구조를 만들어야 한다.
지금은 공개를 달기만 하면 문구가 길든 짧든 같은 칸에 들어가는 구조라서
구체적으로 쓴 쪽에 돌아가는 보상이 없고, 아예 달지 않는 쪽이 가장 유리하다.
상세 공개를 가진 게임을 “공개 있음”으로 묶어
숨김 쪽보다 낫게 보여 주는 방법도 있지만,
이 역시 설계의 문제이고 검증된 것이 아니다.

넷째, 결론을 바꿀 관찰은 일부 나와 있다.
걸러지는 비율은 신작의 3분의 1에서 절반쯤으로 측정됐다.[^pcg-haro]
공개가 있는 게임은 평점이 평균 4점 낮았고
리뷰 100개에 이르는 비율은 55% 수준이었다.[^haro2][^haro1]
이 값은 이진 필터가 노력의 대리 변수 구실을 어느 정도 한다는 쪽에 가깝지만,
인과가 아니라 상관이고 질이 낮은 게임을 가려내기에는 차이가 작다.
그러니 이진 필터가 무의미하다는 주장도 충분하다는 주장도 지금은 서지 않는다.
결론이 바뀔 다음 관찰은 범주별 비율이다.
상점 에셋만 적은 경우, 미술, 코드, 실시간 생성의 비율이 공개되면
어느 칸이 노력의 대리 변수로 쓸 만한지가 드러난다.

다섯째, 구체적으로 쓰는 일은 이미 성공한 쪽의 습관이다.
Haro가 읽은 공개 문구에서 성공한 AI 게임은 더 길었고(중앙값 22단어 대 13단어),
사람이 검토했다는 안심 문구를 더 자주 붙였다(21% 대 12%).[^haro1]
같은 자료에서 “보조”, “부수적” 같은 축소 표현도
성공 쪽이 더 흔했다(59% 대 41%).[^haro1]
구체성과 축소가 함께 늘어난다는 뜻이어서 긴 문구를 정직의 증거로 읽을 수는 없다.
개발사가 쓸 수 있는 가장 믿을 만한 구체성은
사람이 한 일을 검증할 수 있게 쓰는 것이다.

## 개발자가 상점 페이지에 쓸 공개 문구

Steam은 설문의 답을 상점 페이지와 빌드에 대조한다고 밝힌다.[^cs]
그러니 공개 문구는 페이지, 빌드, 설문의 세 곳에서 서로 맞아야 한다.
다음은 이 문서의 관찰에서 나온 작성 원칙이다.

1. 범주를 나눠 쓴다. 미술, 소리, 글, 목소리,
코드 가운데 AI가 관여한 것을 각각 적는다.
2. 미리 만든 것과 실시간 생성을 구분한다. Steam 설문이 이 구분을 쓰고,
실시간 생성이면 방어책도 적어야 한다.[^cs]
3. 사람이 한 일을 적는다. 아티스트의 수정, 선별,
마무리처럼 사람의 몫을 구체적으로 쓴 문구가 가장 정보량이 많다.[^ages]
4. 개발 중 도구는 따로 적는다. 효율을 위한 도구 사용은 Steam 설문의
초점이 아니지만,[^cs] 적고 싶다면 배달되는 콘텐츠와 분리해서 적는다.
5. 상점 에셋과 게임 속 에셋을 나눠 적는다. Steam의 현재 범위에는
상점 페이지와 마케팅 자료가 들어간다.[^pcgn-jan26]
이 문서가 센 공개 36개 중 17개가 상점이나 마케팅 에셋을 적었고,
3개는 그것만 적었다. 캡슐 이미지에만 쓴 경우가 많다는 지적도 있다.[^pcg-week]
6. 마케팅 자료도 같은 기준으로 쓴다. 트레일러와 스크린샷이 게임에
실제로 들어 있는 것과 다르면 판매 약관의 약속에서 문제가 된다.[^cs]
7. 모호한 한 줄로 끝내지 않는다. “AI 도구를 활용했습니다” 한 문장은
해석을 독자에게 떠넘기고, 필터가 생길 때 가장 거친 칸에 들어간다.

예시는 다음과 같은 모양이다.
이 문구는 가상의 개발사 예시이며 어떤 실제 게임의 문구도 아니다.

```txt
AI Generated Content Disclosure
- Pre-generated: 배경 일러스트 초안 12장을 생성형 이미지 모델로 만들었고,
  아티스트가 전부 다시 그려 최종본으로 교체했다. 캐릭터와 UI는 AI를 쓰지 않았다.
- Code: 개발 중 코딩 보조 도구를 사용했고, 모든 코드는 개발자가 검토했다.
- Live-generated: 없음. 플레이 중 AI가 콘텐츠를 만들지 않는다.
```

## 플레이어가 지금 할 수 있는 것

Valve는 AI 필터를 아직 내놓지 않았다.
이 문서가 관찰한 범위에서
Discovery Queue의 AI 제외 설정이나 공식 AI 태그는 확인되지 않았다.
RespawnFirst는 대안으로 “AI warning for Steam”이라는
오픈 소스 브라우저 확장을 소개했다.[^rf]
이 문서는 그 확장을 설치하거나 검증하지 않았으니 쓰기 전에 직접 확인해야 한다.
SteamDB는 2025년 2월부터 공개 구역을 근거로 한 `AI Content Disclosed` 태그를
목록 사이드바의 사용자 태그 필터에서 고를 수 있게 했다고 보도됐다.[^steamdb-gol]
이 필터는 개발사가 적은 공개에만 의존하고,
이 문서는 SteamDB에 접속하지 못해 지금도 같은 방식인지 확인하지 못했다.

행사 구조를 이용하는 방법이 더 확실하다.
행사 첫 며칠은 화면이 무작위이므로,
며칠 뒤 개인화와 인기순이 자리를 잡은
뒤에 보는 편이 기사의 조언과도 같다.[^nfdoc]
상점 페이지에서는 AI Generated Content Disclosure 항목이 있는지 보고,
있으면 범주와 사람이 한 일이 구체적으로 적혀 있는지를 읽는다.
항목이 없다는 사실은 AI를 쓰지 않았다는 보증이 아니다.

## 이 문서가 확인하지 못한 것

- Reddit 글 세 개의 원문은 열지 못했다. 기사가 인용한 문장을 대조하지 못했다.
- 기사가 언급한 Epic, Capcom, mashup mod 관련 기사들은 열지 않았다.
- 상점 페이지 네 개는 공개 항목의 유무만 보았다. 게임의 실제 에셋,
코드, 품질은 검사하지 않았다.
- Valve가 구조화된 AI 필드를 내부적으로 갖고 있는지,
필터를 준비 중인지는 확인하지 못했다.
- Steamworks 등록 수수료의 현재 금액은 확인하지 못했다.
- Lobste.rs의 vibecoded 태그 소동은 열지 못했다.
- SteamDB가 공개 값을 읽는 경로와 지금의 필터 동작은 확인하지 못했다.
- Epic Games Store에 공개 요구가 있는지, GOG, Nintendo, Sony의 규칙은
확인하지 못했다. Sweeney의 2026년 6월 발언은 PC Gamer 원문이 아니라
mp1st의 전언으로만 읽었다.
- EU AI Act 50조는 조항 본문만 읽었고
게임을 겨냥한 위원회 지침과 업계의 해석은 열지 못했다.
- 데모 80개 표본은 Next Fest 참가작만 모은 것이 아니고,
하루의 스냅샷이며, 공개 문구의 분류는 한 사람이 읽고 한 것이다.
- Quantic Foundry와 GDC의 조사는 요약된 결과만 읽었고
원자료나 문항 전체는 보지 못했다.
- Lobste.rs는 브라우저에서 검색을 직접 돌려 Steam Next Fest, Steam AI,
AI slop games 같은 검색어를 확인했고(대조 검색어는 정상 결과를 돌려주었다),
ign.com 도메인 목록에도 이 기사가 없었다. 이 기사의 토론은 없는 것으로 본다.
Haro의 글(fragwyz.substack.com)은 도메인 목록에 없었고
검색 결과 상위 10건에도 보이지 않았다.
- GeekNews에는 이 기사를 다룬 글이 있지만 달린 것은 Hacker News 의견을
요약해 올린 GN⁺ 항목 하나뿐이어서 GN 이용자 고유의 댓글은 반영하지 못했다.
- HN 댓글의 작성자 주장(예: Expedition 33에 대한 서술,
대다수 개발자의 AI 사용 비율)은 근거가 제시되지 않았으므로
그대로 사실로 취급하지 않았다.

[^nf-live]: Steam Store, [Next Fest October 2026 - LIVE NOW](https://store.steampowered.com/sale/nextfest), 2026-10-19
[^nfdoc]: Steamworks Documentation, [Steam Next Fest](https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest)
[^cs]: Steamworks Documentation, [Content Survey](https://partner.steamgames.com/doc/gettingstarted/contentsurvey)
[^tags]: IGN, [Steam Adds, Edits, and Removes Dozens of Store Tags](https://www.ign.com/articles/steam-adds-edits-and-removes-dozens-of-store-tags), 2026-05-19
[^ages]: Steam Store, [Ages TD Demo on Steam](https://store.steampowered.com/app/5155900/)
[^battle]: Steam Store, [BATTLE: PARTS & POWER Demo on Steam](https://store.steampowered.com/app/5200920/)
[^leverage]: Steam Store, [Leverage Real Estate Simulator on Steam](https://store.steampowered.com/app/5106420/)
[^naval]: Steam Store, [Naval Supremacy on Steam](https://store.steampowered.com/app/4609270/)
[^rf]: RespawnFirst, [Demands for AI Filter on Steam Grow as Next Fest Is Flooded with AI Slop](https://respawnfirst.com/demands-for-ai-filter-steam-next-fest-ai-slop/), 2026-10-20
[^freeone]: <https://news.ycombinator.com/item?id=50169883>
[^freeone2]: <https://news.ycombinator.com/item?id=50170106>
[^rivet]: <https://news.ycombinator.com/item?id=50169096>
[^ncallaway]: <https://news.ycombinator.com/item?id=50169547>
[^alpaca-filter]: <https://news.ycombinator.com/item?id=50171356>
[^underyx]: <https://news.ycombinator.com/item?id=50169695>
[^no-multitudes]: <https://news.ycombinator.com/item?id=50169867>
[^no-multitudes2]: <https://news.ycombinator.com/item?id=50172359>
[^no-multitudes3]: <https://news.ycombinator.com/item?id=50175296>
[^preg-zero]: <https://news.ycombinator.com/item?id=50173277>
[^preg-zero2]: <https://news.ycombinator.com/item?id=50175767>
[^pants-binary]: <https://news.ycombinator.com/item?id=50174233>
[^pants-debug]: <https://news.ycombinator.com/item?id=50172217>
[^dijit]: <https://news.ycombinator.com/item?id=50169791>
[^fireant]: <https://news.ycombinator.com/item?id=50172110>
[^preg-lie]: <https://news.ycombinator.com/item?id=50173407>
[^alpaca-fraud]: <https://news.ycombinator.com/item?id=50173741>
[^ympb]: <https://news.ycombinator.com/item?id=50172353>
[^slowhadoken]: <https://news.ycombinator.com/item?id=50170235>
[^vegnus]: <https://news.ycombinator.com/item?id=50170409>
[^andai]: <https://news.ycombinator.com/item?id=50170022>
[^sosodev]: <https://news.ycombinator.com/item?id=50169861>
[^sohcahtoa]: <https://news.ycombinator.com/item?id=50170258>
[^boba]: <https://news.ycombinator.com/item?id=50172120>
[^ox-rs]: <https://news.ycombinator.com/item?id=50170898>
[^mort]: <https://news.ycombinator.com/item?id=50170715>
[^ben-w]: <https://news.ycombinator.com/item?id=50172101>
[^dogleash]: <https://news.ycombinator.com/item?id=50170119>
[^himata]: <https://news.ycombinator.com/item?id=50170748>
[^syabro]: <https://news.ycombinator.com/item?id=50175229>
[^archagon]: <https://news.ycombinator.com/item?id=50170488>
[^dgunay]: <https://news.ycombinator.com/item?id=50170126>
[^linuxftw]: <https://news.ycombinator.com/item?id=50170413>
[^spencer]: <https://news.ycombinator.com/item?id=50170784>
[^debugnik]: <https://news.ycombinator.com/item?id=50173008>
[^mrnotcrazy]: <https://news.ycombinator.com/item?id=50171105>
[^throwaway-fee]: <https://news.ycombinator.com/item?id=50170607>
[^tintor]: <https://news.ycombinator.com/item?id=50170166>
[^throwaway-curation]: <https://news.ycombinator.com/item?id=50170554>
[^tadpole]: <https://news.ycombinator.com/item?id=50170474>
[^jrm4]: <https://news.ycombinator.com/item?id=50169858>
[^throwaway-rating]: <https://news.ycombinator.com/item?id=50171401>
[^mh-rating]: <https://news.ycombinator.com/item?id=50174004>
[^overfeed]: <https://news.ycombinator.com/item?id=50170506>
[^corence]: <https://news.ycombinator.com/item?id=50174216>
[^poin]: <https://news.ycombinator.com/item?id=50170135>
[^mr-freeman]: <https://news.ycombinator.com/item?id=50171352>
[^wincy]: <https://news.ycombinator.com/item?id=50169881>
[^mysterydip]: <https://news.ycombinator.com/item?id=50170179>
[^archagon2]: <https://news.ycombinator.com/item?id=50170577>
[^cubefox]: <https://news.ycombinator.com/item?id=50170718>
[^joshstrange]: <https://news.ycombinator.com/item?id=50170504>
[^dmantis]: <https://news.ycombinator.com/item?id=50175958>
[^ekaros-alt]: <https://news.ycombinator.com/item?id=50176724>
[^npteljes]: <https://news.ycombinator.com/item?id=50177336>
[^pcgn-jan26]: PCGamesN, [Valve's new Steam AI disclosure cares about what you actually see, stressing that behind-the-scenes dev tools are “not the focus”](https://www.pcgamesn.com/steam/new-gen-ai-disclosure-form), 2026-01-17
[^gol-sweeney]: GamingOnLinux, [According to Epic CEO Tim Sweeney - game stores don't need an AI label as it will be everywhere](https://www.gamingonlinux.com/2025/11/according-to-epic-ceo-tim-sweeney-game-stores-dont-need-an-ai-label-as-it-will-be-everywhere/), 2025-11-27
[^sweeney-tweet]: Twitter, [Tim Sweeney on X: “@mattworkman Agreed. The AI tag is relevant to art exhibits for authorship disclosure…”](https://twitter.com/TimSweeneyEpic/status/1993687499621728312)
[^mp1st]: mp1st, [Epic CEO Tim Sweeney Criticizes Steam’s AI Disclosure Requirement, Calls It “Irresponsible”](https://mp1st.com/news/epic-ceo-criticizes-steams-ai-disclosure-requirement), 2026-06-25
[^haro1]: Sulka Haro(Substack), [Three years of AI on Steam](https://fragwyz.substack.com/p/three-years-of-ai-on-steam), 2026-07-13
[^haro2]: Sulka Haro(Substack), [AI flagged games on Steam, Part 2](https://fragwyz.substack.com/p/ai-on-steam-part-2), 2026-07-13
[^pcg-haro]: PC Gamer, [Steam Week in Review: Take cover, because it looks like more than half of new Steam games will have an AI-disclosure by 2027-2028](https://www.pcgamer.com/gaming-industry/steam-week-in-review-take-cover-because-it-looks-like-more-than-half-of-steam-games-will-have-an-ai-disclosure-by-2027-2028/), 2026-07-20
[^pcg-week]: PC Gamer, [Steam Week in Review: More than 300 games released on Steam last week, and 120 of them had AI disclosures](https://www.pcgamer.com/gaming-industry/steam-week-in-review-more-than-300-games-released-on-steam-last-week-and-120-of-them-had-ai-disclosures/), 2026-06-15
[^pcg-nf]: PC Gamer, [Steam Week in Review: Steam Next Fest has over 8,000 demos, as worthless vibe coded slop levels up](https://www.pcgamer.com/gaming-industry/steam-week-in-review-steam-next-fest-has-over-8-000-demos-as-worthless-vibe-coded-slop-levels-up/), 2026-10-19
[^steamdb-gol]: GamingOnLinux, [SteamDB now lets you filter out Steam games with AI Generation](https://www.gamingonlinux.com/2025/02/steamdb-now-lets-you-filter-out-steam-games-with-ai-generation/), 2025-02-25
[^steamdb-lv]: 80 Level, [While Players Wish to Filter Out AI-Generated Games on Steam, SteamDB Makes It Possible](https://80.lv/articles/while-players-wish-to-filter-out-ai-generated-games-steamdb-makes-it-possible/), 2025-02-25
[^itch]: 80 Level, [Asset Creators on Itch.io Must Now Disclose the Use of Generative AI](https://80.lv/articles/asset-creators-on-itch-io-now-have-to-disclose-the-use-of-generative-ai/), 2024-11-21
[^treehouse]: GamingOnLinux, [Indie devs have begun adding a no generative AI stamp to their store pages](https://www.gamingonlinux.com/2025/02/indie-devs-have-begun-adding-a-no-generative-ai-stamp-to-their-store-pages/), 2025-02-24
[^eu50]: AI Act Service Desk, [Article 50: Transparency obligations for providers and deployers of certain AI systems](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50)
[^aljaz]: Al Jazeera, [What came into force with the EU’s AI Act this week – and what didn’t](https://www.aljazeera.com/economy/2026/8/6/what-came-into-force-with-the-eus-ai-act-this-week-and-what-didnt), 2026-08-06
[^gdc]: GDC, [GDC 2026 State of the Game Industry Reveals Impact of Layoffs, Generative AI, and More](https://gdconf.com/article/gdc-2026-state-of-the-game-industry-reveals-impact-of-layoffs-generative-ai-and-more/), 2026-01-29
[^qf]: Quantic Foundry, [Gamers Are Overwhelmingly Negative About Gen AI in Video Games, but Attitudes Vary by Gender, Age, and Gaming Motivations.](https://quanticfoundry.com/2025/12/18/gen-ai/), 2025-12-18
[^gallup]: Gallup, [Americans Cool Toward AI](https://news.gallup.com/poll/712751/americans-cool-toward.aspx), 2026-07-28
[^appdetails]: Steam Store, [appdetails API 응답: Ages TD Demo](https://store.steampowered.com/api/appdetails?appids=5155900&l=english)
[^tagdata]: Steam Store, [인기 태그 목록(populartags)](https://store.steampowered.com/tagdata/populartags/english)
[^weezing]: <https://news.ycombinator.com/item?id=50170758>
[^alpaca-90pct]: <https://news.ycombinator.com/item?id=50171268>
[^0x457]: <https://news.ycombinator.com/item?id=50172817>
[^lambda]: <https://news.ycombinator.com/item?id=50170549>
[^yipinwong]: <https://news.ycombinator.com/item?id=50171043>
[^summermusic]: <https://news.ycombinator.com/item?id=50170038>
[^jerf]: <https://news.ycombinator.com/item?id=50170148>
[^debugnik-gradient]: <https://news.ycombinator.com/item?id=50169891>
[^dugidugout]: <https://news.ycombinator.com/item?id=50170316>
[^preg-all]: <https://news.ycombinator.com/item?id=50175745>
