# Outlook.com이 DMARC 레코드 없는 도메인의 메일을 일부 거부하기 시작했다는 보고

원문: [Outlook.com Is Quietly Rejecting Email From Domains Without DMARC | MailRoute](https://mailroute.net/blog/outlook-rejecting-email-without-dmarc)

HN 토론: <https://news.ycombinator.com/item?id=50416158> (531점, 358개 댓글)

GN 토론: <https://news.hada.io/topic?id=36840>

## 요약

### 무엇이 일어났다고 하는가

글쓴이는 이메일 보안 서비스 MailRoute의 창업자이자 대표로 소개되고,
글의 날짜는 2026년 11월 6일이다.
11월 5일부터 Microsoft의 개인용 메일(outlook.com, hotmail.com, live.com,
msn.com)이 DMARC 레코드가 없는 도메인에서 오는 메일 일부를 거부하고
있다는 것이 글의 주장이다.
발신자에게는
`550 5.7.1 Message rejected: Message lacks SPF/DKIM/DMARC Auth Records (AS9031519)`라는
반송 메시지가 돌아오고, 첫날에는 같은 메시지에 괄호 안의 코드가 없었다고 한다.
글쓴이는 반송된 도메인 대부분이 SPF를 제대로 갖췄고 상당수가 DKIM도 갖췄는데,
둘을 보내는 주소(From)와 연결하는 DMARC 레코드가 빠져 있었다고 적는다.

### 기존 규칙과 다른 점

Microsoft는 2025년 5월부터 하루 5,000통을 넘게 보내는 도메인에 SPF, DKIM,
DMARC 통과를 요구했고, 위반하면 `550 5.7.515 Access denied`가 돌아온다고
글쓴이는 설명한다.
이번 거부는 세 가지가 다르다고 한다.
소규모 사무실의 한 줄 답장 같은 적은 양의 메일에도 생기고,
11월 6일 기준으로 포스트마스터 공지, 블로그 글, 서비스 상태 공지가 없으며,
반송 메시지가 무엇이 실패했는지 알려 주지 않고 레코드가 없다고만 한다.
글쓴이는 MailRoute가 11월 5일 자기 발신 로그에서 처음 확인했고,
다른 관리자들의 공개 보고도 같은 날 나오기 시작했다고 적는다.

### 부분적으로만 거부된다

영향을 받는 도메인에서도 일부 메일만 거부된다.
Hotmail로 보낸 한 통은 도착하고 다음 통은 반송되며, 다시 보내면 성공할 수 있다.
글쓴이는 이 불규칙함이 위험하다고 말한다.
발신자는 약어투성이 반송 메시지를 일시적 장애로 여겨 넘기고,
받는 쪽은 메일이 발송된 사실도 모른다는 것이다.
환자, 주택 소유자, 지원자, 학부모,
회원처럼 개인 주소로 연락하는 사업에서는 청구서와 예약 확인이 조용히 사라진다고
한다.

### 확인과 조치

DMARC 레코드가 있는지는 `dig +short TXT _dmarc.example.com`으로 확인한다.
`"v=DMARC1`로 시작하는 줄이 나오면 있는 것이고, 출력이 없으면
영향을 받을 수 있다.
조치는 DNS에 이름 `_dmarc`, 값 `v=DMARC1; p=none`인 TXT 레코드를 추가하는
것이다.
`p=none`은 도메인이 DMARC를 쓴다고 선언하고 수신 서버에 보고서를 요청하되,
인증에 실패한 메일에는 아무 조치도 하지 말라는 시작 정책이다.
글쓴이는 Gmail, Yahoo 같은 다른 수신 서비스가 메일을 다루는 방식은 바뀌지
않는다고 한다.
단, DMARC는 SPF나 DKIM 중 하나가 보내는 주소의 도메인과 정렬되어 통과해야
성립하므로 레코드만으로 항상 해결되지는 않는다.
글은 MailRoute의 발신 중계(relay)를 쓰는 경우 SPF와 DKIM이 이미 통과하므로 DMARC
레코드가 해결의 전부라고 안내한다.
이때 DKIM 키를 돌려도 서명이 깨지지 않도록 CNAME 레코드 `mr01`, `mr02`,
`mr03`을 모두 게시하라고 한다.
MailRoute를 쓰지 않는 발신자에게는 자매 회사 mxio의 안내와 점검 도구를
소개하고, 글은 무료 체험을 권하며 끝난다.
`p=none`이 이후 `p=reject`로 가는 첫걸음이라는 말도 덧붙인다.
글쓴이는 이것이 모든 대형 메일 서비스가 따르는 패턴이라고 말한다.
처음에는 대량 발송자에게 요구하고, 기한을 공지하고, 이어서
조용히 모두의 기본 조건이 된다는 것이다.
`p=none`은 이제 모범 사례가 아니라 최소 조건이라고 한다.

## 분석

### 이 보고가 맞다면 바뀐 것은 대상 범위다

Microsoft의 2025년 4월 2일자 공식 블로그는 하루 5,000통을 넘게 보내는 도메인에
SPF와 DKIM의 통과, 그리고 최소 `p=none`의 DMARC와 정렬을 요구한다고
밝혔다.[^ms-blog]
이 글이 주장하는 변화는 같은 요구가 발송량과 상관없이 모든 도메인에 적용되는
것이다.
HN의 hedgehog는 공식 문서가 대량 발송자를 기준으로 하지만
이제는 발송량과 상관없이 같은 규칙을 적용한다고 썼다.[^hedgehog]
대량 발송자용 규칙은 공지와 기한이 있었고,
소량 발송자에게는 아직 같은 절차가 없다는 것이 글 전체의 불만이다.

### 반송 코드가 다르다는 점이 새 규칙이라는 근거다

반송 코드가 기존 규칙의 `5.7.515`가 아니라 `5.7.1`이라는 점이 글의 핵심 근거다.
글은 문구 끝의 괄호 안 서버 이름과 ID가 메시지마다 다르다고 적고,
첫날에는 이 괄호가 없었다고 한다.
따라서 `AS9031519`는 글이 보여 주는 한 예일 뿐 고정된 표지로 읽을 수 없다.
HN에서 이 코드를 직접 본 사람 한 명이 같은 설명을 했다.
그에 따르면 `5.7.1`은 여러 실패 유형을 묶는 코드이고,
`AS9031519`가 도메인에 DMARC가 없다는 뜻이며
(글의 서술과 달리 이 사람은 괄호 값을 고정된 것으로 본다),
이 새 실패 유형에 대한 공식 공지는 못 봤다.[^jared_stewart]
다른 사용자는 이것이 오래된 공지와 다른 변경이어서 전혀 예고 없이 왔다고
반박했다.[^donmcronald]

### 거부가 조용하지 않다는 반론이 실제 쟁점이다

제목의 “조용히(quietly)”에 대해 HN에서는 두 갈래의 반박이 나왔다.
하나는 5xx는 영구 실패이므로 조용한 것이 아니라 오히려 명시적으로 거부한
것이라는 지적이다.[^dwm]
다른 하나는 Microsoft가 이 요구를 1년 넘게 전부터 여러 번 공지했다는
지적이다.[^twoninefive]
앞의 지적에는 제목이 공지 없이라는 뜻으로 쓰였을 수 있다는 해석이
달렸다.[^lelandfe]
공지 여부는 어느 변경을 말하느냐에 달려 있어서,
글이 말하는 “공지가 없다”는 소량 발송자에 대한 이번 변경에 한정해 읽어야 한다.

## 비평

### 글쓴이는 판매 대상 제품을 가진 당사자다

글은 맨 끝에서 MailRoute의 무료 체험을 권하고,
본문 중간에도 MailRoute 사용자에게는 “DMARC 레코드가 해결의 전부”라고 안내한다.
상황을 알리는 글이 경보 역할과 판촉을 함께 한다.
HN에서는 이 글을 광고성 글이라고 보는 반응도 있었다.[^twoninefive]
이것이 보고의 사실 여부를 바꾸지는 않지만,
“다른 곳에서의 확인”이 글 안에는 없다.
글이 근거로 드는 것은 MailRoute 자신의 발신 로그와 “다른 관리자들의 공개
보고”라는 문장뿐이고, 그 보고의 링크는 없다.
HN에서는 이 회사 글 밖에 실제 증거가 있느냐는 질문이 나왔다.[^ranger_danger_q]

### “quietly”와 “one DNS record” 같은 표현이 정확하지 않다

글은 해결이 “DNS 레코드 하나”라고 하지만, DMARC가 성립하려면
SPF나 DKIM이 보내는 주소와 정렬되어야 한다.
글도 본문 뒤쪽에서 이 조건을 적고 있어 스스로 모순을 알고 있다.
HN의 한 사용자는 DMARC 단독으로는 쓸모가 없고 SPF,
DKIM이라는 다른 두 레코드에 기대므로 “레코드 하나”는 틀렸다고
지적했다.[^gnabgib]
다른 사용자는 DMARC 레코드 자체는 하나뿐이라고 반박했다.[^jared_stewart_one]
두 말이 모두 맞는 것은 “레코드가 있는가”와 “메일이 통과하는가”가 다른 질문이기
때문이다.
Microsoft 365가 자기 도메인으로 DKIM을 켜기 전까지 `onmicrosoft.com`으로 서명해
DMARC 정렬에 쓰이지 않는다는 글의 예시가 이 차이를 보여 준다.

### 글의 날짜 서술이 Microsoft의 문서와 다르다

글은 2025년 5월부터 하루 5,000통 초과 도메인이 `550 5.7.515`를 받는다고 쓴다.
그런데 Microsoft의 공식 블로그 갱신 문구는 2025년 5월 5일 이후 이런 도메인의
메일을 먼저 정크 폴더로 보내고, 거부는 나중에 날짜를 공지하여 시작한다고
적었다.[^ms-blog]
5.7.515 반송 문구가 블로그에 명시된 것도 사실이어서,
글의 서술은 블로그의 두 단계 일정 중 뒤쪽을 이미 시행 중인 것처럼 쓴 것이다.
이 블로그 문서 이후에 날짜가 공지되었는지는 이번에 확인하지 못했다.

## 인사이트

### 메일 수신 측의 조용한 거부 대신 반송을 택한 것이 오히려 공지의 일부다

HN에서 가장 강한 옹호는 거부가 오류 메시지를 남기므로 몇 분 안에 고칠 수 있고,
스팸 폴더로 보내면 낮은 발송량의 발신자가 몇 해 동안 문제를 모를 수 있다는
것이다.[^mike_hearn]
반대편에서는 수락하고 나중에 버리는 방식이 가장 나쁘고,
거부 시점에 알려 주는 쪽이 낫다고 한다.[^stevekemp]
두 의견은 같은 방향이다.
SMTP 단계에서 거부하는 것이 수신자 쪽 시스템이 남길 수 있는 가장 직접적인
피드백이다.
이번 변경이 비판받는 이유는 거부가 아니라 반송 문구에 실패한 이유가 한 줄도 없고
부분적으로만 적용되어 발신자가 원인을 짐작하기 어렵다는 점이다.

### 거부가 일부 메일에만 적용되면 발신자가 문제를 장애로 오해한다

글이 강조하는 불규칙함은 이 변경의 더 큰 위험이다.
모든 메일이 같은 오류로 막히면 발신자가 원인을 찾지만, 일부만 막히면
재전송으로 해결되어 원인 추적이 끝난다.
수신 측의 점진적 적용(일부 비율만 거부)은 영향을 평가하고
서버 부하를 조절하는 일반적 방법이어서,
이 불규칙함이 단계적 도입이라는 의도일 수도 있다.
그렇다면 앞으로 거부 비율이 점점 올라가고,
지금 “가끔 반송되는” 도메인이 결국 모두 반송될 수 있다.
이 해석은 글쓴이의 보고에서 나온 추정이 아니라 내가 세운 가설이고,
반송 비율이 시간에 따라 바뀌는지를 관측해야 확인된다.

### 소수의 수신 서비스가 정하는 기본 조건이 개인 운영자의 비용이 된다

HN에서는 자기 서버를 운영하는 사람들이 Outlook에서 공개되지 않은 차단 목록,
수락한 뒤 사라지는 메일, 몇 시간 늦은 전달을 겪었다고
적었다.[^neikius][^codethief]
한 댓글은 고객의 IP 대역이 막혀도 지원 도구는 문제가 없다고 하며,
개인 계정으로만 거부되고 업무용 계정은 받는다고 한다.[^efesak]
다른 사람은 이 불만의 대부분을 Microsoft가 차지하는 이유를 자신의 사용자 비중이
크기 때문에 생기는 협상력으로 설명했다.[^miki123211]
DMARC 요구 자체는 스팸과 사칭을 줄이는 공통 방향이지만,
요구를 바꾸는 쪽이 수신 서비스 한 곳이고 공지 절차가 없다면
요구 사항을 따라가는 비용은 발신 쪽 개인 운영자에게 전부 간다.
공개된 기한과 반송 코드의 문서화가 이 비용을 줄이는 가장 작은 단위다.

---

[^ms-blog]: Microsoft, [Strengthening Email Ecosystem: Outlook’s New Requirements for High‐Volume Senders](https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730), 2025-04-02

[^hedgehog]: <https://news.ycombinator.com/item?id=50416719>

[^jared_stewart]: <https://news.ycombinator.com/item?id=50417826>

[^jared_stewart_one]: <https://news.ycombinator.com/item?id=50417873>

[^donmcronald]: <https://news.ycombinator.com/item?id=50420284>

[^dwm]: <https://news.ycombinator.com/item?id=50418108>

[^twoninefive]: <https://news.ycombinator.com/item?id=50418806>

[^lelandfe]: <https://news.ycombinator.com/item?id=50418153>

[^ranger_danger_q]: <https://news.ycombinator.com/item?id=50416824>

[^gnabgib]: <https://news.ycombinator.com/item?id=50418001>

[^mike_hearn]: <https://news.ycombinator.com/item?id=50417017>

[^stevekemp]: <https://news.ycombinator.com/item?id=50416580>

[^neikius]: <https://news.ycombinator.com/item?id=50416963>

[^codethief]: <https://news.ycombinator.com/item?id=50418296>

[^efesak]: <https://news.ycombinator.com/item?id=50422565>

[^miki123211]: <https://news.ycombinator.com/item?id=50423019>
