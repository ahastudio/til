# Slack 이모지 계수

원문: [Company Culture = Slack Emoji ÷ √Headcount](https://lia.mg/posts/measuring-company-culture-with-slack-emoji/)

HN 토론: <https://news.ycombinator.com/item?id=50659640> (436점, 213개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/fin7at/company_culture_slack_emoji_sqrt> (20점, 6개 댓글)

GN 토론: <https://news.hada.io/topic?id=37937>

## 요약

Liam Galvin이 2026년 11월 26일에 올린 글이다.
읽은 시점(2026년 11월 27일)의 페이지에는 수정일이 11월 27일로 표시되어 있다.
회사가 문화를 재려고 쓰는 설문, 펄스 체크, eNPS, 오프사이트를
농담 섞어 비판한 뒤, 더 싼 대안이라며 공식 하나를 내놓는다.
저자는 이 방법이 자신의 경험상 더 정확하다고 쓰는데,
글 전체가 과장과 반어로 쓰인 풍자이므로 진지한 측정법으로 읽을 글은 아니다.

공식은 Slack 워크스페이스의 커스텀 이모지 수를
사용자 수의 제곱근으로 나눈 값이며
저자는 이를 이모지 계수(Emoji Coefficient)라고 부른다.
제곱근을 쓰는 이유는 이모지가 공유 자원이라서
1만 명의 회사에 10명 회사의 1,000배인 이모지가 있을 필요가 없다는 것이다.

점수 해석은 네 구간이다.
5 미만이면 기본 이모지와 회사 로고뿐이라 사람들이 월급 때문에 다니는 회사다.
5 이상 20 미만은 건강하고 기능하는 조직이다.
20 이상 50 미만은 번성하는 조직이다.
50 이상은 후기 단계 문화로, 이모지가 서로를 인용하고
인사팀이 용어집을 요청하지만 아무도 전체 맥락을 모르는 상태다.

이모지 계수만으로는 한 사람이 전부 올렸을 가능성을 가리지 못한다.
그래서 이모지를 한 개 이상 올린 사용자의 비율인
참여율(Participation Rate)을 함께 본다.
20% 미만이면 문화가 소수에게 의존하고 그들이 떠나면 사라진다고 한다.

주의 사항으로 저자는 지표가 조작될 수 있다고 적는다.
중간 관리자가 회사 로고 변형을 수백 개 올리는 경우가 그렇다.
변화율도 봐야 하는데 갑작스러운 이모지 증가는 긍정 신호이고,
작별이나 애도 이모지의 급증은 구조 조정과 겹치며
사용자 수가 줄어들어 오히려 점수가 오른다고 한다.
Teams를 쓰는 회사에는 같은 공식이 없고 필요하지도 않다고 쓴다.
결론은 문화가 가치 포스터가 아니라
팀이 정말 필요한 것은 놀란 콜리플라워 이모지라고
판단한 엔지니어에게서 나온다는 것이다.

## 분석

### 풍자의 대상은 문화 측정의 형식이다

글이 겨냥하는 것은 이모지가 아니라
문화를 숫자와 슬라이드로 만들어 보여 주려는 관행이다.
설문 결과가 인사팀을 거쳐 채용 페이지의 문구로 바뀌는 과정을 그리고,
그 맞은편에 참여 없이 쌓이는 흔적을 세우는 구도다.
이모지 수는 누가 시키지 않았는데도 사람들이 남긴 기록이라는 점에서
설문과 정반대 성격의 데이터로 제시된다.
이 글이 풍자인지는 독자마다 달랐다.
Lobste.rs의 pyfisch는 풍자 태그가 맞느냐고 물으며
HN에서는 사람들이 글을 진지하게 받아들인다고 지적했다.[^pyfisch]
글을 올린 ducdetronquito는 풍자라기보다
자신이 일한 곳과 매우 닮은 재미있는 글이라고 답하며,
회사가 10명에서 40명 사이였을 때
내부 농담이 담긴 이모지 모음이 인상적이었다고 했다.[^ducdetronquito]

### 제곱근은 공유 자원이라는 가정에서 나온다

공식에서 가장 그럴듯한 부분은 제곱근이다.
한 이모지가 부서 전체에서 몇 년씩 쓰일 수 있다는 전제는
사람이 늘어도 이모지 수가 같은 비율로 늘지 않는다는 직관과 맞는다.
이 가정은 저자가 설명으로 덧붙인 것이고 실제 데이터로 검증한 것은 아니다.
다만 글이 풍자임을 감안하면 검증이 목적이 아니라 형식의 패러디다.

### 참여율은 소수 의존을 보는 장치다

저자는 이모지를 한 사람이 도맡는 상황을 우려해 참여율을 둔다.
공식 두 개로 규모와 분포를 따로 보려는 구성은
문화 지표가 흔히 평균만 보여 주는 문제를 흉내 낸 것이다.
기준을 20%로 잡은 근거는 글에 없다.

## 비평

### 이모지 수는 문화보다 설정의 영향을 크게 받는다

HN에서 wakamoleguy는 Teams에도 관리자 설정으로 커스텀 이모지를 쓸 수 있고
자신이 지난주 하나를 추가했다고 썼다.[^wakamoleguy]
MrGilbert는 Microsoft의 안내 문서를 가리켰고,[^MrGilbert]
StingyJelly는 정책으로 꺼 둘 수 있어서
IT에 켜 달라는 요청을 고민 중이라고 했다.[^StingyJelly]
horticulturist는 새로 온 인사 책임자가 이모지 삭제를 지시해
수천 개와 인기 있던 것들이 사라졌고
그날 회사가 죽었다고 적었다.[^horticulturist]
이모지 수는 구성원의 습관과 함께 관리자의 허용 범위에도 좌우되므로
글의 Teams 문단은 사실로 보기 어렵다.

### 만든 수와 쓰이는 수가 다르다

eclipticplane은 누군가 파티 패럿 변형 500개를 일괄 등록했지만
실제로 쓰이는 것은 5~10개뿐이라며 사용량으로 재야 한다고 썼다.[^eclipticplane]
이에 tavavex는 글에 이미 조작 가능성 항목이 있다고 짚었다.[^tavavex]
그러나 저자의 대응은 참여율이 조작을 드러낸다는 것인데,
일괄 등록을 사용자 여럿이 나눠 올리는 경우는 참여율로 가려지지 않는다.

### 구간이 큰 회사에서는 의미를 잃는다

Washuu는 직원이 1,000명을 넘는 회사에
이모지가 5만 7천 개가 넘는다고 썼다.[^Washuu]
이 값을 공식에 넣으면 사용자가 1,000명일 때 약 1,800이며,
50 아래로 내려가려면 사용자가 130만 명을 넘어야 한다.
이는 이 문서가 계산한 값이고,
후기 단계의 기준이 현실의 큰 워크스페이스를 담지 못한다는 뜻이다.
풍자에서 구간 기준이 엄밀할 필요는 없지만 지표로 쓰려면 상한이 필요하다.

### 문화의 정의가 없어서 검증할 방법도 없다

gerikson은 이 글에서 문화가 정의되지 않은 용어이며
풍자 태그를 떼려면 어떤 업종의 회사가 이 지표로 좋은 문화로 평가되고
경쟁사는 그렇지 않아 실적이 갈린다는 식의
경험적 기준이 필요하다고 썼다.[^gerikson]
글은 이모지 계수가 문화를 반영한다는 근거를 저자의 경험 외에 내놓지 않는다.

### 직접 세는 방법이 글에 없다

zaps는 회사 직원이 이모지 수를 어떻게 알아내느냐고 물으며
IT에 요청해야 한다면 곤란하다고 했다.[^zaps]
steve_adams_86은 워크스페이스의 이모지 관리 페이지에서 개수를 볼 수 있고
API 목록을 jq로 세는 방법도 있다고 답했다.[^steve_adams_86]
글에는 수집 방법이 없다.

## 인사이트

### 소속감은 이모지 수보다 공간의 쓰임에서 나타난다

HN에서 가장 큰 가지는 이모지가 아니라 대화 공간 이야기였다.
locallylinear는 회사마다 스포츠나 반려동물 같은 잡담 채널의 유무가 다르고
어떤 곳은 수십 개가 활발했다고 썼다.[^locallylinear]
이모지 수는 그 여러 신호 중 하나로 보인다.
측정 가능성이 낮을수록 사람들이 지표를 신경 쓰지 않는다는 점이 이 글의 역설이다.

### 반응의 양과 응답의 질은 다르다

redloon은 메시지에 달리는 이모지 반응의 양과 다양성으로
문화 지표를 확장할 수 있다고 했다.[^redloon]
vigilantpuma는 이모지 반응만 오는 것이 실제 응답을 대신하지 못하고
조용함처럼 느껴진다고 답했다.[^vigilantpuma]
같은 이모지 활동이 소통의 풍부함이 될 수도, 대화의 대체물이 될 수도 있다.

---

[^wakamoleguy]: <https://news.ycombinator.com/item?id=50661888>

[^MrGilbert]: <https://news.ycombinator.com/item?id=50664332>

[^StingyJelly]: <https://news.ycombinator.com/item?id=50664911>

[^horticulturist]: <https://news.ycombinator.com/item?id=50662300>

[^eclipticplane]: <https://news.ycombinator.com/item?id=50662467>

[^tavavex]: <https://news.ycombinator.com/item?id=50662516>

[^Washuu]: <https://news.ycombinator.com/item?id=50661563>

[^zaps]: <https://news.ycombinator.com/item?id=50660695>

[^steve_adams_86]: <https://news.ycombinator.com/item?id=50661040>

[^locallylinear]: <https://news.ycombinator.com/item?id=50662624>

[^redloon]: <https://news.ycombinator.com/item?id=50662397>

[^vigilantpuma]: <https://news.ycombinator.com/item?id=50662419>

[^pyfisch]: <https://lobste.rs/s/fin7at/company_culture_slack_emoji_sqrt#c_ypd608>

[^ducdetronquito]: <https://lobste.rs/s/fin7at/company_culture_slack_emoji_sqrt#c_twudlx>

[^gerikson]: <https://lobste.rs/s/fin7at/company_culture_slack_emoji_sqrt#c_vm5gs9>
