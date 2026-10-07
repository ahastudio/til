# Show HN: HN 18년 댓글 트렌드 분석기

<https://hackernewstrends.com/>

HN 토론: <https://news.ycombinator.com/item?id=48673671>

GeekNews: <https://news.hada.io/topic?id=30833>

## 도구 소개

ytkimirti가 만든 hackernewstrends.com은 18년치 Hacker News 댓글 아카이브(약 48GB)를
인덱싱해 단어나 구절의 언급 빈도 변화를 시각화하는 도구다.
Google Trends와 비슷한 인터페이스로 여러 용어를 동시에 비교할 수 있고,
특정 시점의 원본 포스트나 댓글로 바로 이동할 수 있다.
별도로 “Who is Hiring?” 월간 스레드에서 프로그래밍 언어 언급 빈도를 추적하는 페이지도 제공한다.
작자는 “48GB 아카이브를 다운받아 가지고 놀다 보니 만들게 됐다”고 밝혔다.

Show HN으로 올라온 이 포스트는 759점을 받고 151개 댓글이 달렸다.
론칭 직후 트래픽이 몰려 사이트가 여러 차례 다운됐고, 백엔드가 Upstash 레이트 리밋에 걸리기도 했다.
작자는 잠시 사이트를 내리고 복구했다.

사이트 첫 화면은 각 선을
4,500만 건의 게시물과 댓글 위에서 계산한 날짜 히스토그램이라고 설명한다.
그래프 아래에는 선을 만든 실제 스토리와 댓글이 용어별로 걸러져 나온다.
월을 클릭하면 그 달로 거르고, 드래그하면 기간을 고를 수 있다.
작자가 말한 48GB는 아카이브의 크기이고,
사이트가 말하는 4,500만 건은 인덱싱된 항목 수다.

첫 화면에는 “Popular Comparisons”라는 미리 만든 비교 목록이 있고,
비교마다 한 문장짜리 해설이 붙어 있다.
Webpack이 2015~20년 빌드 단계를 차지하다가 2022년부터 Vite가 앞선다는 식이다.
CoffeeScript와 TypeScript, Jenkins와 GitHub Actions, Docker와 Kubernetes,
Apache와 nginx와 Caddy도 같은 세대교체 서사로 묶인다.
OpenAI와 Anthropic 비교에는 2023년부터 OpenAI가 앞서다가
2026년 Anthropic이 급등해 선두가 바뀐다는 해설이 달렸다.
Unity, Unreal, Godot 세 엔진은
2023년 9월 Unity 런타임 요금 사태 때 같은 달에 함께 치솟는다.
그 아래에는 사람, AI와 LLM, 보안 사고, 오픈소스 라이선스 전쟁, 업계 분위기 같은
분류별 용어 묶음이 있다.
보안 사고 묶음에는 log4j, xz, heartbleed, stuxnet 등이,
라이선스 전쟁 묶음에는 sspl, opentofu, valkey 등이 들어 있다.

GeekNews 토픽은 이 사이트의 `?q=anthropic` 화면을 가리키며,
본문은 사이트의 이런 비교들을 기술의 세대교체,
모델 출시마다 계단식으로 오르는 AI 언급량,
보안 사고의 날카로운 급등, 라이선스 변경에 따른 생태계 재편으로 정리했다.
GN 댓글에서 laeyoung은 올해 2월에 Show HN 게시물이 유독 많았다며,
연말에 만든 프로젝트가 2월에 한꺼번에 올라온 것 아니냐고 추측했다.[^gn-laeyoung]
xguru는 그 시점이 Claude Opus 4.6 출시와 Claude Code 확산이 맞물린 때라
첫 결과물이 몰린 것으로 보인다고 답하고,
Show GN도 늘어나는 추세라고 덧붙였다.[^gn-xguru]

## 동작 방식

코드는 Upstash 조직의 GitHub 저장소 `upstash/hacker-trends`에
MIT 라이선스로 공개돼 있다.
README는 이 도구 전체를 Upstash Redis Search 위에 얹은 얇은 UI라고 소개한다.
저장소의 커밋은 모두 ytkimirti가 했고,
그의 GitHub 프로필에는 Upstash 소프트웨어 엔지니어라고 적혀 있다.
HN 스레드에서 docheinestages는 이 프로젝트가 Upstash 광고라면
“Highly Available, Infinitely Scalable”을 내세우는 회사에
접속 폭주는 가장 피하고 싶은 일이었을 것이라고 꼬집었다.[^docheinestages]
stopachka는 왜 다른 검색 엔진이 아니라 Upstash Redis Search를 골랐는지
인프라 설명을 청했다.[^stopachka]

README가 밝히는 구조는 단순하다.
수집 스크립트가 HuggingFace에 올라온 월별 HN Parquet 파일로
과거 데이터를 채우고,
매일 도는 GitHub Action이 공식 HN API에서 새 항목을 가져온다.
각 항목은 Upstash Redis에 `hn:<id>` 형태의 일반 해시로 저장된다.
그 위에 `title`, `text`, `by`, `type`, `time`, `score`, `ndesc`, `parent`
필드를 가진
검색 인덱스 하나를 정의한다.
UI의 모든 검색은 `hn.query` 한 번이고, 모든 추세선은 `hn.aggregate` 한 번이다.
추세선은 `$dateHistogram` 집계를 `fixedInterval: "30d"`로 돌려 만든다.
따라서 화면의 “월별” 막대는 달력상의 월이 아니라
30일 간격이라고 보는 것이 정확하다.
이 마지막 문장은 README의 예제 코드에서 끌어낸 해석이며,
운영 코드가 같은 값을 쓰는지는 확인하지 않았다.
프런트엔드는 Next.js App Router이고 Vercel에 배포된다.
“Who is hiring?” 페이지는 별도 스크립트로 채용 게시물 인덱스를 따로 만든다.

## 분석

### 토론이 드러낸 HN 커뮤니티의 18년 데이터 패턴

토론에서 가장 많이 회자된 관찰은 “trump”가 거의 모든 기술 용어를 압도한다는 것이다.
Petersipoi는 “trump가 다른 거의 모든 용어를 왜소하게 만든다. 진정한 해커 포럼이네”라고 비꼬았다.
정치와 기술이 교차하는 커뮤니티에서 특정 인물이 언어적으로 얼마나 공간을 차지하는지를 보여주는 관찰이다.

jtolmar는 암호화폐에서 AI로의 화제 전환이 그래프에서 명확하게 보인다고 지목했다.
그가 함께 링크한 것은 crypto와 chatgpt를 겹친 그래프로,
암호화폐 논의가 ChatGPT 쪽으로 넘어가는 모습을 가리킨 것이다.[^jtolmar]
linzhangrun은 “LLM이 언제부터 HN의 압도적 주제가 됐는지 확인하고 싶었다. 이제 포스트 절반이 LLM에 관한 것처럼 보인다”고 말했다.
kpw94는 2023년 lk-99(초전도체) 스파이크가 흥미롭다고 지목했다.
단기간에 폭발적으로 논의되고 빠르게 사그라드는 과학 미스터리 특유의 패턴이다.

dwoosley는 보안 취약점과 해킹 관련 용어들이 대부분 사건 발생 시점에만 스파이크를 보이고 이후 급감한다는 것을 발견했다.
예외가 하나 있는데 Stuxnet이다.
“거의 모든 주요 취약점과 해킹은 사건 당시 단발 스파이크만 있는데 Stuxnet만 예외다.”
Stuxnet이 HN 커뮤니티에서 단순한 뉴스 사건이 아니라 반복적으로 참조되는 역사적 개념이 됐다는 것을 보여준다.
dwoosley가 든 이유는 그 공격이 매우 정치적이었고 공개적으로 분석됐으며,
공격 대상이던 사안이 지금도 뉴스 헤드라인에 오른다는 것이었다.[^dwoosley]

작자 자신도 이런 발견을 의도적으로 찾았다.
ytkimirti는 LLM에게 용어 수백 개를 만들게 한 뒤
“shock value” 지표를 계산하는 스크립트로
흥미로운 것을 골라냈다고 밝혔다.[^ytkimirti]
첫 화면의 비교 목록과 분류별 용어 묶음은 이렇게 걸러진 결과로 보인다.
이는 작자의 설명에서 끌어낸 추정이며,
목록의 어느 항목이 그 스크립트에서 나왔는지는 원문에 없다.
wodenokoto는 Anthropic이 2008년에도 언급된 것을 보고,
AI 회사가 이 단어를 차지하기 전에는 무슨 뜻으로 쓰였는지 물었다.[^wodenokoto]
Cakez0r는 “Genuinely” 그래프를 링크하며 LLM의 흔적을 찾았다고 했고,[^Cakez0r]
joshmaker는 그 곡선이 HN 전체 물량과 닮았지만
최근 1년의 급등이 더 크다고 답했다.[^joshmaker-2]

### 도구에 대한 기능 요청이 보여주는 사용자의 분석 욕구

가장 많이 요청된 기능은 총 포스트 수 대비 정규화(normalization)다.
arjie와 scarecrw 모두 독립적으로 같은 요청을 했다.
HN은 18년 동안 크게 성장했기 때문에, 정규화 없이는 모든 주제가 시간이 지날수록 증가하는 것처럼 보인다.
“AI가 요즘 많이 언급된다”는 것이 “AI가 상대적으로 더 많이 논의된다”는 의미인지,
아니면 그냥 “포스트가 전체적으로 늘었다”는 의미인지를 구분하려면 정규화가 필수다.

sinuhe69는 AI 기반 동의어 그룹화를 제안했다.
“auto pilot”, “self driving”, “FSD”를 같은 카테고리로 묶어야 진짜 트렌드가 보인다는 것이다.
현재는 단어 단위 매칭이기 때문에 같은 개념을 지칭하는 다양한 표현이 분산된다.
marky1991은 바로 반대했다.[^marky1991]
그런 변화가 Google 검색을 짜증 나게 만든 원인이며,
영업 문구에서 “self-driving”과 “auto pilot”의 역사를
따로 보고 싶을 수도 있다는 것이다.
그는 시스템이 사용자의 뜻을 짐작하게 하기보다
`|` 같은 고전적인 검색 문법으로 사용자가 말한 대로 동작하게 하자고 했다.
kpw94는 각 댓글의 감성 점수를 계산해 “cloudflare(긍정)”와 “cloudflare(부정)”를
따로 그리는 기능을 제안했다.[^kpw94]

linmer는 그래프의 특정 시점을 클릭하면 해당 날짜의 HN 프론트 페이지로 이동하는 기능을 제안했다.
이것은 데이터 탐색 도구와 원본 컨텍스트를 연결하는 유용한 확장이다.
cloudkj는 “Show HN” 포스트만 필터링하는 기능을 요청했다.
작자는 linmer의 제안은 기록해 두겠다고,[^ytkimirti-2]
cloudkj의 제안은 꼭 추가하겠다고 답했다.[^ytkimirti-3]
ltrg는 HN 언급이 기업 실적이나 가치평가의 선행 지표가 되는지
보고 싶다고 했다.[^ltrg]

### 이미 존재하는 대안이 보여주는 생태계

zX41ZdbW는 이미 HN 데이터를 SQL로 쿼리할 수 있는 공개 ClickHouse 데이터베이스를 운영 중이라고 밝혔다.
이 데이터베이스는 실시간 업데이트를 받으며, SQL 쿼리와 HTML만으로 이 도구가 하는 것들을 직접 만들 수 있다.
hackernewstrends.com이 기술적으로 새로운 것이 아니라 접근성을 낮춘 것임을 보여주는 맥락이다.
프로그래머 커뮤니티에서는 원시 데이터베이스 접근이 이미 가능하지만,
시각화 인터페이스가 없으면 그 접근성은 제한적이다.

다만 ClickHouse 쪽 데이터에도 범위의 한계가 있었다.
jstrieb은 그 플레이그라운드의 `hackernews_history` 테이블을
가장 오래된 갱신 시각 순으로 조회하면
2024년 4월 6일까지만 거슬러 올라간다고 짚었다.[^jstrieb]
그는 그래도 매우 유용하다고 했지만,
원 댓글만 읽어서는 HN 전체 데이터를 조회하는 것이 아니라는 점이
분명하지 않았다고 덧붙였다.
같은 댓글 아래에서 GeoAtreides는
HN 이용 약관상 자기 데이터는 HN에만 사용을 허락했다며
데이터셋에서 자신의 데이터를 빼 달라고 요청했다.[^GeoAtreides]
공개 아카이브를 가공해 서비스로 내놓을 때
데이터 권리 문제가 따라온다는 점을 보여 주는 장면이다.

## 비평

### Google Trends와의 유비가 도구의 한계를 가린다

Aachen은 이 도구를 Google Trends와 비교하는 것이 정확하지 않다는 예리한 지적을 했다.
Google Trends는 사람들이 *검색한* 것을 측정한다.
hackernewstrends.com은 사람들이 *글로 쓴* 것을 측정한다.
이 차이는 중요하다.
사람들은 치킨 배달을 매일 검색하지만 인터넷에 치킨에 대한 글을 쓰지는 않는다.
반면 “인공지능이 일자리를 빼앗는다”처럼 뉴스가 된 사안은 글로 많이 쓰인다.

이 도구는 Google Trends보다 Google Books Ngrams에 가깝다.
특정 단어가 *출판된 텍스트에서* 얼마나 자주 등장했는지를 추적하는 것이다.
차이는 HN 댓글이 책보다 훨씬 짧은 시간 단위로 반응한다는 것이다.
도구의 이름이 “Google Trends for Hacker News”이기 때문에 이 오해는 사용자가 결과를 해석하는 방식에 영향을 준다.
“AI가 요즘 HN에서 많이 *논의된다*”는 것이 “사람들이 AI를 많이 *검색한다*”와 같지 않다.

원 댓글에서 Aachen이 든 예는 치킨이 아니라 버거 배달이었고,
그는 이 도구가 Google Ngrams가 책 대신 웹페이지를 센 것에
더 가깝다고 했다.[^Aachen]
이어진 답글에서 그는 제목과 화면 생김새가 같은 지표라고 믿게 만들기 때문에
그 틀로 데이터를 읽으면 잘못된 결론에 이른다고 설명했다.[^Aachen-2]
작자도 서비스 이름은 괜찮지만
게시물 제목은 다소 오해를 부른다고 인정했다.[^ytkimirti-4]

반론도 있었다.
hn_throwaway_99는 이 도구가 게시물과 댓글을 함께 세기 때문에
사람들이 무엇을 더 알고 싶어 하고 이야기하고 싶어 하는지라는 관점에서는
검색과 꽤 비슷하다고 반박했다.[^hn_throwaway_99]
인기 있는 스토리는 댓글이 많아 관련 용어가 늘고,
관심 없는 주제는 댓글이 붙지 않아 점수가 낮다는 이유다.
그는 “blockchain”과 “OpenAI”를 비교하면
이 도구와 Google Trends의 그래프가 매우 비슷하게 나온다고 했다.
이 반론은 두 지표가 같다는 주장이 아니라 큰 흐름에서는 수렴한다는 주장이다.
따라서 Aachen의 경고는 큰 화제의 추세보다,
검색은 많지만 글로는 잘 쓰이지 않는 일상적 주제에서
더 크게 작동한다고 읽는 편이 맞다.

### 정규화 없는 절대값 그래프가 기본값이라는 설계 선택

가장 많이 요청된 기능이 정규화라는 것은, 현재 기본 표시 방식이 분석에 한계가 있음을 시사한다.
HN은 2007년부터 2026년 사이 사용자 수와 포스트 수가 크게 증가했다.
정규화 없는 절대값 그래프에서는 거의 모든 용어가 최근으로 올수록 높게 나타난다.
이것이 해당 주제에 대한 관심이 증가했기 때문인지,
아니면 단순히 전체 포스트 수가 증가했기 때문인지를 구분할 수 없다.

“LLM이 HN의 절반을 차지한다”는 관찰도 정규화 없이는 확인하기 어렵다.
절대값으로는 LLM 언급이 폭발적으로 늘었어도,
전체 포스트 수 대비 비율로 보면 다른 그림이 나올 수 있다.
정규화는 사후 기능이 아니라 기본 표시 방식이어야 분석 도구로서의 가치가 높아진다.

rightbyte는 y축이 당시 전체 댓글 수로 정규화됐는지 묻고,
그래프를 클릭해 보니 절대 건수인 것 같다고 스스로 정정했다.[^rightbyte]
jcgl은 정규화가 없으면 사이트가 성장한 기간의 검색 대부분이
어느 지표든 결국 인구 분포와 똑같아지는 히트맵을 꼬집은
xkcd 1138번 “Heatmap”의 한 버전이 될 것이라고 했다.[^jcgl]
joshmaker는 구체적인 예를 들었다.[^joshmaker]
“iPhone” 검색은 2025년 무렵 떨어지는데,
“the”나 “is” 같은 일반 단어를 검색해 보면 관심이 줄었다기보다
그해 HN 댓글 자체가 적었던 것으로 보인다는 것이다.
이 방법은 그대로 사용자가 직접 할 수 있는 임시 정규화다.
흔한 기능어의 추세선을 분모로 삼아 관심 대상 용어를 나눠 보면
전체 물량 변화를 어느 정도 걷어낼 수 있다.

### 데이터 품질 문제가 신뢰도를 흔든다

Insanity는 Java, Go, Amazon 같은 자주 언급되는 주제가 결과에 나타나지 않는다고 지적했다.
gslepak는 특정 쿼리에서 데이터가 2018년 10월에서 잘린다는 버그를 발견했다.
“Who is Hiring?” 페이지는 “이 기간에 언급된 직업이 없습니다”를 전 항목에 표시하는 오류를 보였다.
gslepak이 링크한 vim, emacs, zed 비교의 잘림은
작자가 고쳤다고 답했다.[^ytkimirti-5]
jianfenglin은 openai 대 anthropic 그래프에
2019년 이후 데이터가 없다고 물었고,[^jianfenglin]
dacox도 어떤 쿼리든 2019년 이후 데이터가 없다고 보고했다.[^dacox]
작자는 오류 때문에 데이터셋을 다시 채워야 했다며
몇 분 안에 고쳐질 것이라고 답했다.[^ytkimirti-6]
Insanity 자신은 “go”가 일반 단어여서 걸러진 것 아닐까 하고 추측했다.[^Insanity]

론칭 첫날의 “hug of death”는 서비스 안정성 문제이므로 일시적이지만,
데이터 인덱싱 자체의 불완전성은 더 근본적인 문제다.
48GB 아카이브를 완전히 인덱싱했다고 해도, 검색 가능한 형태로 변환하는 과정에서 누락이 생겼다면
트렌드 분석의 신뢰도 자체가 흔들린다.
도구가 “무엇이 많이 논의됐는가”를 보여주려면 “무엇이 인덱싱에서 빠졌는가”를 먼저 명확히 해야 한다.

### 문자열 일치는 같은 이름의 다른 대상을 구분하지 못한다

누락보다 더 조용한 문제는 잘못 세는 것이다.
chfritz는 이 도구가 Google Trends가 풀어야 했던
용어 중의성 문제에 똑같이 부딪혔다고 지적했다.[^chfritz]
Sublime, Atom, VS Code를 비교하는 편집기 그래프에서
“atom”은 편집기만 가리키지 않는다.
al_borland도 Atom이 아직 VS Code와 엇비슷하게 나오는 것을 보고
사람들이 정말 편집기 Atom을 그렇게 많이 이야기하는지,
다른 원자를 이야기하는지 물었다.[^al_borland]
zarlss43은 Grunt 추세가 태스크 러너가 아니라
“grunt work”를 잡고 있다고 봤다.[^zarlss43]
paravz는 Prometheus 대 Grafana 비교의 상위 스토리가
모니터링 도구가 아니라
공기 중 CO2를 제거하는 다른 Prometheus라고 짚었다.[^paravz]

토큰 처리에서 오는 오류도 있다.
jayd16은 C#이 그래프에서는 사실상 C와 일치하는데
예시 글 제목에서는 C#만 강조된다고 보고했다.[^jayd16]
svara는 Fastly를 검색하면 “fast”가 잡힌다고 했고,[^svara]
jasonjmcghee는 공백이 들어간 용어가
“or”로 처리되는 것 같다고 했다.[^jasonjmcghee]
화면의 하이라이트와 그래프의 집계가 서로 다른 규칙을 따르면,
사용자는 아래의 예시 글을 보고 그래프가 맞다고 믿게 된다.

이 문제는 첫 화면의 서사와 직접 부딪힌다.
비교마다 붙은 해설은 그래프를 세대교체 이야기로 읽어 주지만,
그 그래프가 동음이의어와 토큰 분리 문제를 안고 있다면
해설은 잡음 위에 지은 이야기가 될 수 있다.
실제로 nailer는 REST가 2012~15년 웹의 기본이 되고
2016년 gRPC, 2017년 GraphQL로 갈라진다는 해설에
그래프를 보면 REST는 2017년까지 기본이었고,
GraphQL은 2020년대 초 잠깐 인기를 끈 뒤
다시 REST로 돌아온다고 반박했다.[^nailer]
corv도 Flash 대 HTML5 그래프가
해설의 결론과 나란히 놓으니 이상해 보인다고 했다.[^corv]
chfritz가 제안한 대로 문맥을 담은 임베딩 벡터로 인덱싱하면
이 문제가 줄어들 수 있지만,
그 경우에는 marky1991이 경계한 것처럼
시스템이 사용자의 뜻을 대신 해석하는 문제가 다시 생긴다.
이 긴장은 이 도구만이 아니라 텍스트 빈도로 관심을 재는 모든 도구에 남는다.

## 인사이트

### HN은 기술 트렌드 예측기가 아니라 기술 담론 기록이다

이 도구가 보여주는 것은 기술의 트렌드가 아니라 HN 커뮤니티가 무엇에 대해 *이야기하기로 선택했는가*다.
이 두 가지는 다르다.
어떤 기술이 실제로 성장했어도 HN에서 별로 논의되지 않으면 그래프에 나타나지 않는다.
반대로 HN에서 폭발적으로 논의됐어도 실제로는 실패한 기술이 있다.
lk-99 스파이크가 그 예다.

그럼에도 불구하고 HN의 담론이 기술 업계의 관심과 높은 상관관계를 가지는 이유가 있다.
HN 사용자들은 기술 스타트업, 투자자, 엔지니어 커뮤니티를 대표한다.
이 커뮤니티가 무엇을 논의하는지는 이 집단이 무엇에 투자하고 채용하고 만들지와 연결된다.
hackernewstrends.com이 보여주는 것은 기술 트렌드의 거울이 아니라
기술 업계 특정 집단의 관심 이동 역사다.

### 커뮤니티 규모 측정 도구가 드러내는 집단 기억의 구조

대부분의 사건은 “단발 스파이크”를 보이지만 Stuxnet은 예외라는 관찰은 흥미롭다.
이것은 어떤 사건이 집단 기억에 지속적으로 남는지를 보여준다.
Stuxnet이 반복적으로 언급되는 이유는 그것이 사이버 전쟁의 교과서적 사례가 됐기 때문이다.
새로운 악성코드나 해킹이 등장할 때마다 Stuxnet과 비교하는 방식으로 언급된다.

이런 패턴을 분석하면 “무엇이 기준점(reference point)이 됐는가”를 알 수 있다.
한 번만 크게 언급되고 사라지는 사건과, 시간이 지나도 계속 참조되는 사건의 차이가 무엇인지를 추적하는 것이다.
이것은 단순한 빈도 분석을 넘어 커뮤니티의 지식 구조를 이해하는 방법이 될 수 있다.

### 데이터 민주화의 패턴 — 동일 데이터의 접근 경로가 달라질 때

이 도구가 나오기 전에도 HN 전체 데이터는 공개되어 있었고, SQL로 쿼리할 수 있었다.
그럼에도 759점과 151개 댓글이 달렸다.
접근 가능한 데이터와 사용 가능한 데이터는 다르다.

원시 ClickHouse 데이터베이스는 SQL을 쓸 수 있는 사람만 사용한다.
hackernewstrends.com은 웹 브라우저와 텍스트 입력만 알면 사용한다.
같은 정보에 접근하는 경로가 달라지면, 누가 그 정보를 사용하는지가 달라지고,
그 결과 어떤 질문이 제기되는지가 달라진다.
sinuhe69의 동의어 그룹화 제안, Petersipoi의 “trump가 모든 것을 압도한다”는 관찰,
dwoosley의 Stuxnet 예외 발견 — 이것들은 SQL 쿼리로 도달하기 어려운 관찰이다.
직관적 인터페이스는 데이터에서 다른 종류의 발견을 가능하게 한다.

### 한 개인의 48GB 아카이브 탐색이 커뮤니티 도구가 되는 경로

ytkimirti는 “그냥 48GB를 다운받아서 가지고 놀다 보니 만들었다”고 밝혔다.
개인의 호기심이 공공 인프라가 되는 이 경로는 Show HN의 전형적인 패턴이다.
그러나 이 도구는 순수한 개인 취미 프로젝트가 아니었다.
저장소는 Upstash 조직 소유이고 라이선스 표기도 Upstash이며,
작자는 Upstash 소프트웨어 엔지니어이고,
사이트는 Upstash Redis Search를 내세운다.
작자의 호기심에서 출발했더라도 결과물은 회사 제품의 시연을 겸한다.
그래서 론칭 첫날의 다운은 개인 도구의 한계라기보다
시연 대상인 Upstash 데이터베이스의 레이트 리밋이 그대로 드러난 장면이 됐고,
docheinestages가 꼬집은 것도 바로 그 점이었다.

더 중요한 것은 지속성의 문제다.
작자가 관심을 잃거나 비용 부담이 커지면 도구는 사라진다.
회사가 운영하는 시연이라면 비용 부담은 개인보다 덜하겠지만,
이번에는 지속 여부가 회사의 마케팅 우선순위에 달린다.
HN 커뮤니티가 이런 도구를 지속적으로 가치 있게 여긴다면,
이것이 개인 프로젝트로 남을 것인지,
아니면 Y Combinator나 Algolia(HN 검색을 운영하는)가 공식적으로 제공해야 할 인프라인지를 생각해볼 필요가 있다.

---

[^docheinestages]: <https://news.ycombinator.com/item?id=48674778>

[^stopachka]: <https://news.ycombinator.com/item?id=48675984>

[^jtolmar]: <https://news.ycombinator.com/item?id=48675903>

[^dwoosley]: <https://news.ycombinator.com/item?id=48675954>

[^ytkimirti]: <https://news.ycombinator.com/item?id=48677595>

[^wodenokoto]: <https://news.ycombinator.com/item?id=48694382>

[^Cakez0r]: <https://news.ycombinator.com/item?id=48679240>

[^joshmaker-2]: <https://news.ycombinator.com/item?id=48679973>

[^marky1991]: <https://news.ycombinator.com/item?id=48675087>

[^kpw94]: <https://news.ycombinator.com/item?id=48675696>

[^ytkimirti-2]: <https://news.ycombinator.com/item?id=48677615>

[^ytkimirti-3]: <https://news.ycombinator.com/item?id=48674945>

[^ltrg]: <https://news.ycombinator.com/item?id=48675965>

[^jstrieb]: <https://news.ycombinator.com/item?id=48690636>

[^GeoAtreides]: <https://news.ycombinator.com/item?id=48676387>

[^Aachen]: <https://news.ycombinator.com/item?id=48675818>

[^Aachen-2]: <https://news.ycombinator.com/item?id=48676119>

[^ytkimirti-4]: <https://news.ycombinator.com/item?id=48677561>

[^hn_throwaway_99]: <https://news.ycombinator.com/item?id=48678866>

[^rightbyte]: <https://news.ycombinator.com/item?id=48674773>

[^jcgl]: <https://news.ycombinator.com/item?id=48680206>

[^joshmaker]: <https://news.ycombinator.com/item?id=48679946>

[^ytkimirti-5]: <https://news.ycombinator.com/item?id=48677575>

[^jianfenglin]: <https://news.ycombinator.com/item?id=48676496>

[^dacox]: <https://news.ycombinator.com/item?id=48676642>

[^ytkimirti-6]: <https://news.ycombinator.com/item?id=48676538>

[^Insanity]: <https://news.ycombinator.com/item?id=48676096>

[^chfritz]: <https://news.ycombinator.com/item?id=48676066>

[^al_borland]: <https://news.ycombinator.com/item?id=48675751>

[^zarlss43]: <https://news.ycombinator.com/item?id=48677781>

[^paravz]: <https://news.ycombinator.com/item?id=48682463>

[^jayd16]: <https://news.ycombinator.com/item?id=48679993>

[^svara]: <https://news.ycombinator.com/item?id=48684754>

[^jasonjmcghee]: <https://news.ycombinator.com/item?id=48678039>

[^nailer]: <https://news.ycombinator.com/item?id=48676338>

[^corv]: <https://news.ycombinator.com/item?id=48675274>

[^gn-laeyoung]: <https://news.hada.io/topic?id=30833#cid60348>

[^gn-xguru]: <https://news.hada.io/topic?id=30833#cid60351>
