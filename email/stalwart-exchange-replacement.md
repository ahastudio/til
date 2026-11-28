# Stalwart 1.2.0의 Exchange 호환

원문: [Stalwart is now a drop-in replacement for Microsoft Exchange](https://stalw.art/blog/microsoft-exchange-replacement/)

HN 토론: <https://news.ycombinator.com/item?id=50620349> (555점, 300개 댓글)

GN 토론: <https://news.hada.io/topic?id=37744>

## 요약

Stalwart 프로젝트 관리자 Mauro D.가 2026년 11월 23일에 올린 릴리스 글이다.
Stalwart 1.2.0이 Microsoft Exchange 클라이언트가 쓰는 프로토콜을 구현해
Exchange의 드롭인 대체가 되었다고 주장한다.

글의 내용은 다음과 같다.

- 구현한 프로토콜: MAPI over HTTP, Exchange Web Services(EWS), Exchange ActiveSync 14.1과 16.1,
  Autodiscover이다. 모두 JMAP와 WebUI가 쓰는 같은 HTTPS 포트에서 제공한다.
  Outlook, Apple Mail, 휴대폰 메일 앱이 Exchange 서버로 보고 연결한다고 한다.
  Exchange 지원은 AGPL 커뮤니티 에디션에 들어 있다.
- 지원하지 않는 것: 공용 폴더, 보관 사서함, 모바일 기기 관리, Outlook 2010 이하의 RPC over HTTP,
  NTLM과 Kerberos 로그인이다. 인증은 비밀번호, 앱 비밀번호, OAuth로 한다.
- 새 Outlook: 새 Outlook for Windows는 Stalwart와도, 어떤 자체 호스팅 서버와도 작동하지 않는다고 한다.
  IMAP 계정을 추가하면 Microsoft 클라우드가 대신 접속하므로 자체 호스팅의 목적에 어긋난다며
  쓰지 말라고 권한다.
- 왜 지금인가: Exchange 2016과 2019는 2025년 10월 14일에 지원이 끝났고,
  Exchange Online의 EWS는 2026년 10월부터 꺼지기 시작해 2027년 4월에 사라진다.
  글은 서버를 먼저 바꾸고 클라이언트를 천천히 JMAP 기반 도구로 옮기는 경로를 제안한다.
- 규모와 분리: Exchange 호환은 약 20만 줄을 더하며 별도 crate와 `exchange` Cargo 기능 뒤에 있고
  기본값은 꺼짐이다. Exchange 전용 속성은 메타데이터로 따로 저장해 지울 수 있다고 한다.
- 이전 도구: Vandelay가 Exchange Server는 EWS로, Microsoft 365는 Graph로 읽어 JMAP으로 옮긴다.
- 그 밖의 1.2.0 기능: 메일 규칙(Sieve로 컴파일), 수신 확인, 근무 시간, 회의실과 장비 자원,
  네이티브 FoundationDB 클라이언트(점 읽기 처리량 4.5~6.9배, 회사 벤치마크)가 있고
  stalwart-cli 2.0은 Ratatui 기반 전체 화면 콘솔을 갖는다.
- FOSDEM 2027에서 2027년 1월 30일에 Exchange 이전 발표를 한다.

## 분석

### 사업 논리

글의 논리는 장벽이 서버가 아니라 클라이언트라는 것이다.
서버만 먼저 바꾸고 사용자는 같은 Outlook을 계속 쓰면 이전의 저항이 줄어든다.
이를 위해 프로토콜 호환을 임시 다리로 두고 최종 목적지는 JMAP 같은 개방형 표준이라고 한다.
이 논리는 프로젝트의 서술이며 실제 이전 사례나 호환성 시험 결과는 글에 없다.

### 약속의 범위

글은 드롭인 대체를 내세우지만 지원하지 않는 기능을 스스로 열거한다.
공용 폴더와 보관 사서함, 모바일 기기 관리가 빠져 있어
이를 쓰는 조직에게는 이 표현이 그대로 맞지 않을 수 있다.

## 비평

### 벤더 종속을 연장하는가

HN의 andreashaerter는 종속 효과는 프로토콜과 클라이언트에 내재하며
MAPI 같은 표준을 지원하는 것은 시간을 벌고 라이선스 비용을 줄일 뿐이고
개방형 이메일 생태계에 해를 끼친다고 보았다.[^andreashaerter]
mitchweaver는 Exchange의 가치는 메일이 아니라 나머지에 있다고 반박했고,[^mitchweaver]
iamnothere는 JMAP도 지원하므로 눈감아 줄 만하다고 했다.[^iamnothere]
k_g_b는 이를 역방향의 포용, 확장, 소멸로 읽었다.[^k_g_b]
이는 의도에 대한 해석이며 글은 호환 지원이 이전 경로라는 입장이다.

### 독일의 보관 규정

rmoriz는 독일의 프리랜서와 회사는 메일을 삭제와 변경이 불가능한 방식으로 최대 10년 보관해야 하는데(GoBD)
Stalwart의 일반 요금제와 OSS판에는 그 기능이 없다고 썼다.[^rmoriz]
FinnKuhn은 공식 사이트의 컴플라이언스 애드온에 관리자도 줄일 수 없는 최소 보존 기간 설정이 있다고 알렸다.[^FinnKuhn]
WA는 보관해야 하는 것은 봉투(메일)가 아니라 청구서이며 DATEV 같은 회계 도구로 보내면 된다고 했다.[^WA]
stymaar는 GDPR과의 충돌을 지적했다.[^stymaar]

### 도입의 위험

999900000999는 Exchange가 필요하면 Exchange를 써야 하고
이 전환을 정한 사람은 메일이 가지 않는 순간 해고될 것이라고 했다.[^999900000999]
vanviegen은 Stalwart는 품질이 뛰어난 FOSS이고 강점은 JMAP이라고 반박했다.[^vanviegen]
smithbob은 직접 운영하는 IP가 Outlook의 /24 대역 차단에 걸렸다고 했지만 layer8은 Stalwart와 무관하다고 답했다.[^smithbob][^layer8]
rzerowan은 이것이 Exchange 내부가 아니라 프로토콜 호환 계층이므로
드롭인이라는 표현이 이전의 노력을 가릴 수 있다고 했다.[^rzerowan]

### Outlook 지원 중단 논란

hobo123은 Outlook이 온프레미스 Exchange를 지원하지 않는데 어떻게 대체 서버를 쓰느냐고 물었다.[^hobo123]
ZenoArrow는 클래식 Outlook에는 다른 메일 서버 설정이 남아 있고 빠진 것은 새 Outlook뿐이라고 했다.[^ZenoArrow]
글의 설명과 같다.

### 개발 방식

LoganDark는 AI 덕분이라고 덧붙였고 greggoB는 글에 AI 언급이 없다고 되물었다.[^LoganDark][^greggoB]

## 인사이트

### 가져갈 것

자체 호스팅 서버로 Exchange를 벗어나려는 조직에게 이 릴리스는 클라이언트 교체를 미루는 선택지를 준다.
다만 글 스스로 인정하듯 새 Outlook은 제외되고 일부 Exchange 기능이 없다.
현실적인 판단 방법은 시험 계정으로 자신이 쓰는 Outlook 기능(공용 사서함, 위임, 규칙)이 작동하는지 확인하는 것이다.
규제가 있는 업종은 보관과 삭제 요건을 먼저 확인해야 한다.

### 확인할 관찰

1. 실제 조직의 이전 사례와 Outlook 연결 안정성에 대한 독립 보고.
2. 공용 폴더와 보관 사서함 같은 빠진 기능이 추가되는지.
3. 약속한 FoundationDB 성능 수치의 독립 재현.
4. 2029년 클래식 Outlook 지원 종료 이후의 사용자 이동.

---

[^andreashaerter]: <https://news.ycombinator.com/item?id=50620882>

[^mitchweaver]: <https://news.ycombinator.com/item?id=50620975>

[^iamnothere]: <https://news.ycombinator.com/item?id=50621076>

[^k_g_b]: <https://news.ycombinator.com/item?id=50621227>

[^rmoriz]: <https://news.ycombinator.com/item?id=50622997>

[^FinnKuhn]: <https://news.ycombinator.com/item?id=50625616>

[^WA]: <https://news.ycombinator.com/item?id=50624908>

[^stymaar]: <https://news.ycombinator.com/item?id=50624754>

[^999900000999]: <https://news.ycombinator.com/item?id=50621043>

[^vanviegen]: <https://news.ycombinator.com/item?id=50621178>

[^smithbob]: <https://news.ycombinator.com/item?id=50621567>

[^layer8]: <https://news.ycombinator.com/item?id=50621597>

[^rzerowan]: <https://news.ycombinator.com/item?id=50621259>

[^hobo123]: <https://news.ycombinator.com/item?id=50624418>

[^ZenoArrow]: <https://news.ycombinator.com/item?id=50624672>

[^LoganDark]: <https://news.ycombinator.com/item?id=50620671>

[^greggoB]: <https://news.ycombinator.com/item?id=50620739>
