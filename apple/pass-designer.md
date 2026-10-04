# Apple Pass Designer: Wallet 패스를 미리 보며 디자인하는 macOS 앱

<https://developer.apple.com/pass-designer/>

<https://developer.apple.com/documentation/walletpasses/creating-a-pass-with-pass-designer>

HN 토론: <https://news.ycombinator.com/item?id=49937276> (541점, 323개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49908808> (2점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34680>

## 소개

Pass Designer는 Apple Wallet에 들어가는 패스, 곧 탑승권, 이벤트 티켓,
멤버십 카드, 쿠폰 같은 것을 디자인하고 미리 보는 Apple의 macOS 앱이다.
제품 페이지는 동네 피트니스 센터부터 소규모 공연장, 글로벌 항공사,
전국 커피 체인까지 어떤 사업자든 자기 브랜드를 담은 패스를 쉽게 만들고
미리 볼 수 있다고 소개한다.
현재 베타이며 macOS 27 이상이 필요하고,
내려받으려면 Apple Account로 로그인해야 한다.
요청을 받으면 무료 등록을 마치고 Apple Developer Agreement에 동의해야 한다.

이 문서는 제품 페이지와 Apple 개발자 문서의
‘Creating a pass with Pass Designer’를 함께 읽고 썼다.
나는 이 앱을 직접 실행하지 않았다.
Wallet 패스 파일의 내부 구조와 손으로 만드는 과정은 이 저장소의
`apple/ios-wallet-library-card.md`에 정리되어 있다.

## 동작 방식

### 템플릿에서 시작해 실시간으로 미리 본다

새 문서를 만들면 템플릿 선택기가 열리고,
패스 스타일을 고르면 그 스타일에 맞는 텍스트 필드와 이미지 자리가 미리 채워진다.
개발자 문서는 만들 수 있는 주요 패스 유형이 여섯 가지라고 하고, 빈 패스에서
시작할 수도 있다고 설명한다.
Apple이 제공하는 템플릿 말고 자기 템플릿을 써도 된다.

왼쪽 사이드바에는 패스의 구성 요소가 모여 있고,
요소를 누르면 편집 패널이 열린다.
오른쪽은 미리 보기다.
제품 페이지에 따르면 미리 보기는 iOS와 watchOS가 쓰는 것과 같은 렌더링을 써서
iPhone과 Apple Watch에서의 모습을 그대로 보여 준다.
흰 배경 패스를 디자인할 때는 캔버스 배경을 검게 바꾸어 보는 식으로 작업 화면의
배경색도 바꿀 수 있다.

### 시맨틱 태그와 하위 호환 구조

탑승권과 이벤트 티켓에는 시맨틱 태그를 붙일 수 있다.
시맨틱 태그는 이벤트 날짜, 장소, 항공편 정보 같은 구조화된 데이터이고,
시스템은 이를 Siri 제안, 캘린더 연동, 지도 길찾기 같은 기능에 쓴다.
Pass Designer는 이 태그를 UI에서 바로 편집하게 해 주고,
시맨틱 패스와 비시맨틱 패스를 나란히 보여 준다.
또 시맨틱 데이터로부터 시맨틱 태그가 없어도 동작하는 하위 호환 패스 구조를
자동으로 만들어서, 태그를 지원하지 않는 환경에서도 패스가 동작하게 한다.

개발자 문서는 시맨틱 태그를 쓰는 패스도 하위 호환을 위해
텍스트 필드를 함께 채우라고 한다.
필드를 패스가 보여 줄 수 있는 것보다 많이 넣으면 넘치는 필드는 패스 앞면에
나오지 않지만 Wallet 앱의 패스 정보에는 포함된다.
시맨틱 태그는 Wallet 앱에서 이벤트의 가방 규정이나 호텔 예약 정보 같은 추가
동작을 보여 주는 데도 쓰인다.

### 검증

작업하는 동안 Pass Designer가 패스를 계속 검증해서 필수 키 값이 빠졌거나
예상하지 못한 정의가 있으면 알려 준다.
손으로 `pass.json`을 쓸 때는 Wallet에 넣어 보기 전까지 무엇이 틀렸는지 알기
어려웠다는 점을 생각하면 이 기능이 실질적인 변화다.
이 평가는 내 해석이다.

## 패스 만들기

### 정체성과 서명 정보

Identity & Signing 섹션에 사업자 정보를 넣으며,
이 메타데이터는 패스 정보에서 사람들에게 보인다.
이미 Pass Type ID 인증서를 만들어 두었다면 인증서에서 정보를
바로 가져올 수 있다.
HN의 Tepix는 개발자 인증서가 적어도 필요하지 않으냐고 물었는데,[^Tepix]
배포까지 가려면 서명이 필요하다는 점은 개발자 문서의 흐름과 같다.

### 스타일과 색

Style 섹션에서 패스 종류를 고른다.
탑승권은 운송 수단으로 항공, 기차, 배, 버스, 일반 중 하나를 고를 수 있다.
배경색, 전경색, 라벨 색을 바꿀 수 있고,
개발자 문서는 배경 이미지를 쓸 때 라벨이 읽히도록 대비를 확인하라고 권한다.
제품 페이지는 최신 Wallet 레이아웃을 모두 쓰는 디자인과 하위 호환 패스를
함께 지원한다고 적는다.

### 이미지 크기

이미지는 PNG로, 2x와 3x 크기를 모두 넣는다.
어떤 이미지가 필요한지는 Pass Designer가 패스마다 알려 준다.
개발자 문서가 밝힌 크기는 다음과 같다.

| 이미지        | 크기                  | 쓰이는 곳                                                          |
| ------------- | --------------------- | ------------------------------------------------------------------ |
| 아이콘        | 38×38 정사각형        | 모든 패스, 잠금 화면 배너, Mail                                    |
| 로고          | 높이 50, 너비 50~160  | 일반·쿠폰·스토어 카드, iOS 26 이전 탑승권, iOS 18 이전 이벤트 패스 |
| 기본 로고     | 높이 30, 너비 30~126  | iOS 26 이후 탑승권, iOS 18 이후 이벤트 패스                        |
| 보조 로고     | 12×12에서 12×135까지  | iOS 18 이후 이벤트 패스 오른쪽 아래                                |
| 스트립 이미지 | 375×144               | 쿠폰, 스토어 카드                                                  |
| 썸네일        | 높이 90, 너비 60~90   | 일반 패스, 포스터형이 아닌 이벤트 티켓                             |
| 푸터 이미지   | 문서에 크기 명시 없음 | iOS 26 이후 항공 탑승권                                            |

기본 로고를 쓰는 새 디자인이라도 이전 OS에서 볼 사람을 위해 일반 로고를 함께
넣으라고 문서는 당부한다.
스트립 이미지는 기본 필드와 같은 자리에 있어서 기본 필드에 넣은 텍스트가
스트립 이미지 위에 겹친다.
배경 이미지는 포스터형이 아닌 이벤트 티켓에서는 흐리게,
포스터형 이벤트 티켓과 포스터형 일반 패스에서는 선명하게 나온다.

### 바코드

바코드 정보는 앱에 직접 넣고 바코드 그림은 자동으로 만들어지므로
이미지로 넣지 않는다.
지원하는 형식은 QR, PDF417, Aztec, Code128, Code 39, Codabar, EAN-13,
Interleaved 2 of 5(ITF)다.
문서는 이미지 안에 바코드를 넣지 말라고 명시한다.
HN의 kenferry도 바코드를 Apple이 그리기 때문에 바코드를 그림에 섞는 디자인은
iPhone 패스에서는 불가능하다고 답했다.[^kenferry]

### 저장하고 배포하기

디자인을 저장하면 `.pkpasstemplate` 번들이 만들어진다.
이 번들을 Pass Builder에 올려 패스를 만들고 서명하고 배포한다.
Pass Builder는 Wallet 패스를 프로그램으로 만들고 배포하는 Swift on Server 패키지이며
패스를 만들고 서명하는 타입 안전한 API를 제공한다.
배포 방식이 Pass Builder와 맞지 않으면 `.pkpasstemplate` 번들을 풀어서
기존 문서의 방식대로 직접 빌드하고 서명하면 된다.

## 누구를 위한 도구인가

제품 페이지는 소규모 사업자까지 겨냥하지만,
실제 결과물은 서명과 배포가 남은 템플릿이다.
HN의 jameshart는 패스 배포 문서의 단계를 보면 일반 사용자를 위한 도구로 보기
어렵다고 했다.[^jameshart]
philo23과 MBCook은 iOS 27의 Wallet 앱에서 기존 바코드와 QR 코드를 스캔해 직접
패스를 만들 수 있지만 디자인은 고를 수 없다고 짚었다.[^philo23][^MBCook]
정리하면 개인은 Wallet 앱에서,
디자인이 필요한 사업자와 개발자는 Pass Designer와 Pass Builder로 나뉘는 구도다.
이 구분은 댓글과 문서를 합쳐 내가 내린 해석이다.

쓰임새에 대한 증언도 있다.
brandall10은 멕시코시티에서는 온라인으로 산 이벤트, 주요 버스 노선, 극장 체인,
박물관 입장권에 Wallet 패스가 흔하다고 했다.[^brandall10]
giarc는 바코드를 띄우는 것 말고는 쓸모가 없는 앱 몇 개를 지우고 Wallet 패스로
대신하고 싶다고 했다.[^giarc]
moontear는 위치(Locations) 필드를 넣으면 그 매장에 갔을 때 패스가 자동으로
떠오른다는 점이 과소평가되어 있다고 했다.[^moontear]

## 함정

### macOS 27 전용이다

베타는 macOS 27 이상에서만 돈다.
rock_artist는 이 요구 사항에 구체적인 이유가 있는지 의문을 던졌다.[^rock_artist]
ladberg는 Apple이 앱 사이에 공유하는 코드를 OS 라이브러리로
빼는 습관이 있어서 최신 OS 의존이 생기기 쉽다고 설명했는데,[^ladberg]
이는 내부 사정에 대한 추정이다.
결과적으로 Windows나 Linux, 이전 macOS를 쓰는 조직은 지금 이 도구를 쓸 수 없다.

### 이름이 비슷한 서드파티 사이트

HN에서 bahrtw가 온라인 대안으로 `passdesigner.app`을 소개하자,
cube00은 이 사이트가 Apple 개발자 문서로 링크하며 Apple 제품처럼 보이게
만들어졌지만 Apple 것이 아니고 댓글 작성자 본인의 사이트라고 경고했다.[^cube00]
Pass Type ID 인증서처럼 민감한 서명 자료를 다룰 도구라면 공식 다운로드 경로인
`developer.apple.com`에서 받았는지 확인해야 한다.

### 시맨틱 패스의 지원 범위가 문서 안에서도 엇갈린다

개발자 문서의 Style 섹션 메모는
iOS 26 이후의 새 시맨틱 패스 디자인을 항공 탑승권만 지원한다고 적는다.
그런데 시맨틱 태그 섹션은 탑승권은 iOS 27 이후,
이벤트 패스는 iOS 18 이후에 시맨틱 태그를 쓸 수 있다고 적는다.
새 시맨틱 디자인과 시맨틱 태그가 서로 다른 개념일 수도 있지만 문서는 둘의
관계를 설명하지 않는다.
대상 OS 버전별로 실제 기기에서 확인하는 수밖에 없다.

### 동적 바코드는 다루지 않는다

urbandw311er는 모바일 티켓 업계에서 일할 때 바코드를 바꿀 수 없다는 점이
인터넷이 약한 곳의 보안상 장애물이었다며
동적 바코드 지원 여부를 물었다.[^urbandw311er]
ACCount39도 화면을 한 번 보면 영원히 베낄 수 있는 코드 대신
TOTP 코드를 바랐다.[^ACCount39]
제품 페이지와 개발자 문서 어디에도 시간 기반 바코드는 나오지 않는다.
위조 방지가 중요하다면 패스 디자인과 별개로 서버 측 검증을 설계해야 한다.

### Apple 전용이다

frabcus는 Google과 공동 표준을 만들어 한 번만 만들면 되게 해야지 Apple 전용
작업 흐름을 하나 더 늘렸다고 비판했다.[^frabcus]
Pass Designer의 결과물은 Apple Wallet 패스이므로 Android 사용자를 위한
Google Wallet 패스는 따로 만들어야 한다.

## 비평

### 늦게 나온 도구가 드러내는 것은 그동안의 문서 공백이다

전직 Apple 직원이라고 밝힌 msephton은 12년쯤 전 Apple에서 일할 때 이런 도구를
만들자고 강하게 밀었다고 했다.[^msephton]
multiplegeorges는 예전에 부실한 문서로 패스를 만들려다 너무 고통스러워 방향을
틀었다고 했다.[^multiplegeorges]
danpalmer는 스키마가 명확하고 표준 UI 요소로 거의 다 만들 수 있는
이런 소프트웨어가 LLM 이전에는 우선순위를 받기 어려웠고 이제는 쉽게 만들 수 있게
되었다고 보았다.[^danpalmer]
pradn이 소개한 무료 웹 마법사 WalletWallet처럼 이미 대안도 있었다.[^pradn]
이 증언들을 합치면 Pass Designer의 가치는 새로운 기술이 아니라,
Apple 렌더러와 같은 미리 보기와 공식 검증이라는 두 가지에 있다.
이 둘은 서드파티 도구가 흉내 내기 어려운 부분이다.

## 기억할 원칙

### 미리 보기가 실제 렌더러와 같을 때만 디자인 도구는 믿을 만하다

Wallet 패스의 어려움은 JSON을 쓰는 데 있지 않고,
기기와 OS 버전마다 같은 데이터가 다르게 그려진다는 데 있다.
그래서 이 도구가 내세우는 핵심 문장은 미리 보기가 iOS와 watchOS와 같은
렌더링을 쓴다는 것이다.
여러 OS 버전에 걸친 결과물을 만드는 도구를 고를 때는 기능 목록보다 미리 보기가
실제 렌더러와 같은지를 먼저 확인해야 한다.

---

[^Tepix]: <https://news.ycombinator.com/item?id=49937538>

[^kenferry]: <https://news.ycombinator.com/item?id=49942302>

[^jameshart]: <https://news.ycombinator.com/item?id=49937594>

[^philo23]: <https://news.ycombinator.com/item?id=49937634>

[^MBCook]: <https://news.ycombinator.com/item?id=49939556>

[^brandall10]: <https://news.ycombinator.com/item?id=49937927>

[^giarc]: <https://news.ycombinator.com/item?id=49938546>

[^moontear]: <https://news.ycombinator.com/item?id=49938193>

[^rock_artist]: <https://news.ycombinator.com/item?id=49937513>

[^ladberg]: <https://news.ycombinator.com/item?id=49937646>

[^cube00]: <https://news.ycombinator.com/item?id=49943671>

[^urbandw311er]: <https://news.ycombinator.com/item?id=49942338>

[^ACCount39]: <https://news.ycombinator.com/item?id=49939092>

[^frabcus]: <https://news.ycombinator.com/item?id=49941976>

[^msephton]: <https://news.ycombinator.com/item?id=49939336>

[^multiplegeorges]: <https://news.ycombinator.com/item?id=49939851>

[^danpalmer]: <https://news.ycombinator.com/item?id=49940447>

[^pradn]: <https://news.ycombinator.com/item?id=49938171>
