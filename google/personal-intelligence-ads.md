# Google이 Gmail과 사진 데이터를 맞춤 광고에 쓸 수 있도록 약관을 고쳤다

원문: [Now Google says it might use your Gmail and Google Photos data to target ads | The Verge](https://www.theverge.com/tech/1017600/google-personal-intelligence-privacy-policy-ads-update)

HN 토론: <https://news.ycombinator.com/item?id=50214218> (292점, 156개 댓글)

GN 토론: <https://news.hada.io/topic?id=35889>


## 요약

The Verge의 Jess Weatherbed가 2026년 10월 23일에 쓴 뉴스다.
Google이 개인정보 처리방침을 고쳐서, 개인화 AI 기능을 쓰는 사용자에게 개인
데이터를 바탕으로 한 맞춤 광고가 보일 수 있게 됐다는 내용이다.
변경은 Android Authority가 먼저 발견했다고 기사는 밝히며,
이 문서는 Android Authority 기사와 Google의 방침 원문을 열어 보지 못했다.
기존 문구는 Drive, Gmail, Google Photos의 내용을 개인화 광고에 쓰지 않겠다는
약속이었는데, 10월 16일부로 “이 서비스들의 데이터를 개인화 광고를 지원하는 다른
Google 서비스에서 쓸 수 있게 사용자가 선택하지 않는 한”이라는 예외가 붙었다고
한다.

기사는 영향 범위를 이렇게 풀이한다.
Google의 Personal Intelligence 기능으로 Drive, Gmail, Google Photos를 AI Mode와
다른 검색 도구에 연결한 사용자는 그 내용을 바탕으로 한 광고를 볼 수 있다.
광고주는 Drive, Gmail, Photos의 정보나 이름과 이메일 같은 식별 정보를 얻지
못하고, Google은 인종, 성적 지향, 종교, 건강 같은 민감 범주를 바탕으로 광고를
보여 주지 않는다고 한다.
기사가 인용한 방침 문구는 두 대목이다.
사용자는 Search나 Gemini 앱 같은 서비스가 Google Photos와 Gmail과 Drive 같은
다른 서비스의 데이터에 접근하도록 허용할 수 있고, 이는 더 개인화된 경험을 위한
것이다.
또 설정에 따라 관심사와 활동, 개인화된 콘텐츠를 바탕으로 개인화 광고를 보여 줄
수 있으며, 예컨대 Search에서 마운틴 바이크를 검색하면 YouTube에서 스포츠 용품
광고를 볼 수 있다.
막는 방법으로는 Search의 Personal Intelligence에서 연결을 끊을 앱을 고르거나
Search 서비스 개인화 설정 페이지에서 개인화 추천을 끄는 것을 안내한다.

## 분석

### 글의 중심 주장: 선택이라는 말이 광고 목적까지 포함하게 됐다

기사의 소제목은 더 나은 AI 추천을 위해 데이터를 공유하는 것이 더 개인화된 광고를
위해 데이터를 여는 것도 뜻한다는 것이다.
변경의 핵심은 새 데이터 수집이 아니라 기존 약속의 예외다.
데이터는 사용자가 연결했을 때만 쓰이지만, 연결의 이유(AI 응답의 품질)와
쓰임(광고)이 분리되지 않는다.
이는 동의의 범위를 목적별로 나누지 않고 하나의 연결 선택에 묶는 구조다.

### 광고주에게 데이터를 주지 않는다는 방어의 의미

기사가 전하는 방어(광고주는 내용이나 식별 정보를 얻지 못함, 민감 범주 제외)는
광고 시스템의 일반적인 설명이다.
광고주가 내용을 보지 못해도 Google의 광고 시스템이 그 내용을 신호로 쓰는 것은
같다.
따라서 쟁점은 누가 데이터를 보는가가 아니라, 이 데이터가 광고 선택의 입력이
되는가다.
기사는 이 구분을 명시하지 않고 나란히 둔다.

## 비평

### 더 합리적이라는 읽기와 이를 위한 조건

HN에서 zmmmmm은 댓글이 방침을 직접 접근으로 오해할 것이므로 실제 한정
조건(사용자가 선택해서 다른 서비스가 쓸 수 있게 한 경우)을 짚으며 생각보다
합리적이라고 했다.[^zmmmmm]
shevy-java는 이를 Google 편들기라 하고 악하다고 했고,[^shevy-java] josephg는
안드로이드 공식 앱의 정보 공유 요청이 끝없이 뜨고 거절하기 어려운 다크 패턴이
많았다고 했다.[^josephg]
이 대화가 보여 주는 것은 선택의 질이다.
방침상 선택이 있어도 선택 화면이 반복되고 거절이 어렵다면 선택은 형식이 된다.
기사는 선택 화면의 설계나 기본값을 확인하지 않았고, 이 문서도 확인하지 못했다.

### 원래의 약속이 어떤 약속이었는지에 대한 논쟁

cowlevel은 Google이 늘 이렇게 해 왔고 Gmail이 존재하는 이유가 이것이며 이제
말하는 것뿐이라고 했다.[^cowlevel]
ViktorRay는 이것이 사실이 아니고 Google은 한때 Gmail을 그렇게 썼으나 수년 뒤
멈췄으며 이는 프라이버시의 큰 승리였다고 반박했다.[^viktorray]
changoplatanero는 멈춘 이유가 Gmail 정보의 한계 가치가 줄어서(특히 구매 영수증
이메일을 소매업체가 줄여서)라고 짚었다.[^changoplatanero]
이 대화는 약속의 지속이 윤리가 아니라 경제성에 달려 있었을 수 있음을 시사하나,
이 서술들은 모두 댓글의 기억과 추측이며 확인되지 않았다.
기사는 이 역사를 다루지 않는다.

### 민감 범주의 정의에서 빠진 것

benoau는 인종, 성적 지향, 종교, 건강이 민감 범주로 열거됐고 정치 성향이 눈에
띄게 빠졌다고 했다.[^benoau]
pureagave는 미래에는 정치 성향이 광고가 아니라 더 나쁜 일에 쓰일 것이라고
했다.[^pureagave]
기사는 이 문장을 방침의 서술로 전할 뿐 범주의 전체 목록이나 이 목록이 어디에
명시됐는지는 밝히지 않는다.
이 지적은 열거된 범주가 닫힌 목록인지에 따라 달라진다.

### 규제 비교가 빠져 있다

actapp80은 Google이 EU에서 디지털시장법(DMA) 제5조 2항에 따라 Search, YouTube,
광고 서비스, Play, Chrome, 쇼핑, 지도를 연결할지 사용자가 고르게 한다고
인용했다.[^actapp80]
기사는 이번 변경이 지역별로 다르게 적용되는지 다루지 않는다.
이 문서는 Google의 EU 안내문을 직접 확인하지 못했다.

## 인사이트

### 개인화의 두 얼굴은 같은 연결에서 나온다

Personal Intelligence의 가치는 내 메일과 사진을 AI가 아는 데서 나오고, 광고의
가치도 같은 지식에서 나온다.
한쪽만 쓰고 다른 쪽은 끌 수 있느냐가 사용자의 실제 통제다.
기사가 알려 주는 방법(앱별 연결 해제, 개인화 추천 끄기)은 부분 통제인데, 개인화
추천을 끄면 AI 응답의 개인화도 줄어드는지는 기사에 없다.
이 상충이 기능과 광고의 분리가 설계 수준에서 가능한지를 가른다.
이 서술은 이 문서의 추론이다.

### 이탈 비용의 문제는 변경이 아니라 이전에 있다

댓글의 상당수는 Google을 떠나라는 조언이었다.
jmathai는 Immich와 Google Takeout으로 Google Photos를 벗어나기가 쉽고 보람
있다고 했으나,[^jmathai] boplicity는 Takeout이 중간에 실패하는 일이 많다고
반박했다.[^boplicity]
munk-a는 도메인을 직접 소유해 주소를 바꿀 수 있게 하라고 했고,[^munk-a] TFNA는
은행 앱이 Play 서비스를 필수로 요구하는 나라가 있다고 짚었다.[^tfna]
이 대화는 선택이 이론상 열려 있어도 이전 비용이 실제 선택을 좌우한다는 점을 보여
준다.
방침 변경에 대한 가장 강한 방어는 정책이 아니라 이전 가능성이라는 것이 댓글의
일관된 흐름이다.

### 이 글을 읽는 방법

이 기사는 방침 문구의 변경을 알리는 짧은 뉴스이며, 개인에게 실제 영향은 설정
화면에서 확인해야 한다.
오늘 할 수 있는 일은 Personal Intelligence에 연결한 앱 목록과 Search 서비스
개인화 설정을 열어 보고, 광고 개인화에 쓰이길 원하지 않는 서비스의 연결을 끊는
것이다.
이 기사의 주장을 가를 관찰은 두 가지다.
연결을 허용하지 않은 사용자의 광고에 이 데이터가 쓰이지 않는다는 것이 독립적으로
확인되는지, 그리고 연결 화면이 광고 목적을 사용자에게 어떻게 알리는지다.
둘 다 이 기사에는 없다.

---

[^zmmmmm]: <https://news.ycombinator.com/item?id=50215720>

[^shevy-java]: <https://news.ycombinator.com/item?id=50216147>

[^josephg]: <https://news.ycombinator.com/item?id=50215945>

[^cowlevel]: <https://news.ycombinator.com/item?id=50215274>

[^viktorray]: <https://news.ycombinator.com/item?id=50215321>

[^changoplatanero]: <https://news.ycombinator.com/item?id=50215740>

[^benoau]: <https://news.ycombinator.com/item?id=50215911>

[^pureagave]: <https://news.ycombinator.com/item?id=50216239>

[^actapp80]: <https://news.ycombinator.com/item?id=50216043>

[^jmathai]: <https://news.ycombinator.com/item?id=50216317>

[^boplicity]: <https://news.ycombinator.com/item?id=50216687>

[^munk-a]: <https://news.ycombinator.com/item?id=50216387>

[^tfna]: <https://news.ycombinator.com/item?id=50216684>
