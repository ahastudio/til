# Keep Android Open: 개발자 등록 의무화에 반대하는 캠페인

<https://keepandroidopen.org/>

HN 토론: <https://news.ycombinator.com/item?id=45742488> (2693점, 889개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50208558> (480점, 333개 댓글)

GN 토론: <https://news.hada.io/topic?id=35864>

## 소개

Keep Android Open은 Google의 Android 개발자 등록 의무화에 반대하는 캠페인
사이트다.
사이트가 설명하는 정책은 이렇다.
Google이 2025년 8월에 발표한 요구로, 2027년부터 모든 Android 앱 개발자가
소프트웨어를 어느 기기에든 설치하기 전에 Google에 중앙 등록해야 한다.
Play 스토어 앱뿐 아니라 친구끼리 공유하는 앱, F-Droid로 배포되는 앱, 취미로 만든
개인용 앱도 포함한다고 한다.
등록 조건은 Google에 요금을 내고, Google의 약관에 동의하고, 정부 발급 신분증을
제출하고, 개인 서명 키의 증거를 내고, 현재와 미래의 모든 애플리케이션 식별자를
나열하는 것이다.
따르지 않는 개발자의 앱은 전 세계 모든 기기에서 조용히 차단된다고 사이트는 쓴다.
이 문서가 읽은 시점에 페이지 상단에는 “잠금까지 70일”이라는 카운트다운이 있었다.
정책 내용과 시행 시점의 사실 확인은 이 사이트의 서술에 의존하며, 이 문서는
Google의 발표를 직접 열어 확인하지 못했다.

사이트는 Google이 내세우는 예외 경로를 함정이라고 부른다.
고급 사용자가 미등록 앱을 설치하는 절차는 시스템 설정에서 휴대폰 정보를 찾고,
빌드 번호를 일곱 번 눌러 개발자 모드를 켜고, 강압에 대한 경고 화면을 넘기고,
PIN을 입력하고, 재시작하고, 24시간을 기다리고, 돌아와 경고를 더 넘기고,
임시(7일) 또는 무기한 허용을 고르고, 위험을 이해한다는 것을 다시 확인하는 아홉
단계라고 한다.
이 절차가 Android OS가 아니라 Google Play Services를 거치므로 Google이 OS
업데이트 없이 바꾸거나 없앨 수 있다는 점을 사이트는 강조한다.

해결책으로 사이트는 일반 사용자에게 F-Droid 설치, 규제 당국에 연락, 페이지 공유,
탄원서(change.org, 서명 10만 명 이상) 서명, 공개서한 공유를 권한다.
개발자에게는 Android Developer Console에 가입하지 말고 동료도 말리라고 한다.
공개서한에는 EFF, F-Droid, GrapheneOS, Tor Project, Nextcloud, Brave, Proton,
GNOME Foundation, VideoLAN 등 23개국 71개 단체가 서명했다고 한다.

## 분석

### 글의 중심 주장: 보안 명분 아래 이뤄지는 신원 기반 통제다

사이트의 논증은 보안이 연막이라는 것이다.
Google Play Protect가 개발자 신원과 무관하게 악성코드를 이미 검사하며, 정부
신분증을 요구해도 코드가 더 안전해지지 않고 개발자를 식별해 통제하기 쉬워질
뿐이라고 한다.
악성코드 제작자는 등록할 수 있는 반면 독립 개발자와 반체제 인사는 못 할 수
있다는 점이 그 논거다.
사이트는 이를 EFF가 identity-based gatekeeping을 검열 도구로 본다는 주장에
기댄다.

### 예상되는 반론에 하나씩 답하는 구조

사이트는 FAQ 형태로 다섯 반론을 먼저 꺼내 답한다.
단지 보안 문제라는 반론, 고급 흐름으로 사이드로딩이 된다는 반론, 숨길 것이
없다면 문제없다는 반론, Apple도 그렇다는 반론, 25달러와 서류 정도라는 반론이다.
애플은 처음부터 폐쇄 정원이었고 사람들이 Android를 고른 이유가 달랐다는 답,
그리고 25달러는 미국 개발자에게나 사소하다는 답이 눈에 띈다.
설득의 핵심은 비용을 금액이 아니라 신분증과 서명 키 증거를 한 회사에 넘기는 일로
재정의하는 것이다.

### 반대 서명의 분포가 보여 주는 이해관계

공개서한 서명 단체는 디지털 권리 단체(EFF, EDRi, Article 19), 대체 OS와
스토어(GrapheneOS, LineageOS, F-Droid, Aurora Store), 앱 제작자(Signal 계열이
아닌 Molly, VideoLAN, Tuta, Proton, Fastmail)로 갈린다.
정책으로 가장 직접 타격을 받는 사람들이 앞장선 구도다.
이는 반대 여론이 넓다는 증거이기도 하고, 서명자가 정책의 영향을 받는 당사자라는
한계이기도 하다.

## 비평

### 캠페인 문구는 반대편의 가장 강한 논거를 다루지 않는다

HN에서 FiloSottile은 이 사이트의 숨 가쁜 분노 수사가 완화하려는 실제 위험, 즉
사용자를 단계별로 이끌어 앱을 설치하게 하고 폰을 장악해 돈과 개인정보를 빼 가는
기술 지원 사기를 한 번도 인정하지 않는다면 선전일 뿐이라고 했다.[^filosottile]
lookeey는 불법 앱과 사기가 광고로 퍼지고 평범한 사용자가 짧은 안내만 보고
설치하는 일이 많으며, 숙련된 사용자는 거의 영향을 받지 않고 절차가 평범한 사람을
막을 만큼만 복잡하다고 보았다.[^lookeey]
사이트는 보안이 연막이라고 하지만 사기 피해라는 구체적 위해에 대한 수치나 사례를
따로 다루지 않는다.
반론을 FAQ에서 다룬다고 하면서도 가장 강한 형태(사기 피해를 줄이는 마찰이
필요한가)로 마주하지는 않는다.

### 사이트의 표현이 사실과 해석을 섞는다

nonconsensually pushed, silent update, no opt-out 같은 문구는 사이트의 평가다.
rjh29는 사이트가 언급하지 않았지만 옵트아웃이 있다고 지적했다.
개발자 모드를 켜고 24시간을 기다리는 방법이며, 이 흐름이 Google Play Services를
거치므로 Google이 앞으로 더 어렵게 만들 가능성이 높다고 했다.[^rjh29]
같은 스레드에서 ChrisRR은 서명되지 않은 APK를 ADB로 설치할 수 있고 24시간 대기를
한 번 거치면 설치할 수 있다고 정리했다.[^chrisrr]
사이트가 옵트아웃이 없다고 쓰면서 아홉 단계의 예외 경로를 따로 설명하는 것은
서로 어긋나지 않고, 옵트아웃이라는 말의 정의가 다를 뿐이다.
이 차이는 독자가 직접 판단해야 한다.

### 규제 준수 때문일 가능성은 다루지 않는다

PurelyApplied는 이것이 고객 신원 확인(KYC) 규제를 지키려는 시도처럼 보인다고
했다.[^purelyapplied]
contravariant는 사용자가 쓰는 소프트웨어를 통제하는 KYC가 무엇이냐고
되물었다.[^contravariant]
사이트는 규제 압력이라는 설명을 언급하지 않고 Google의 의도를 시장 지배력과 규제
포획으로만 해석한다.
이 문서는 어느 쪽이 맞는지 확인하지 못했다.

### Apple이 더 폐쇄적이라는 비교는 사용자 이동을 가린다

사이트는 Apple 비교를 약한 tu quoque라고 하지만, HN에서 kykat은 이 때문에
가족에게 iPhone을 권하게 됐다고 했다.[^kykat]
habitue는 이후에도 iPhone이 더 폐쇄적이며 24시간 예외 경로도 없다고
반박했다.[^habitue]
사이트가 사용자에게 권하는 행동에는 iPhone으로의 이동이 없지만, 이 정책이 실제로
사용자를 Apple 쪽으로 밀 수 있다는 점은 스레드가 보여 준다.

## 인사이트

### 개방성의 일부는 은행과 정부 앱이 쥐고 있다

liendolucas가 왜 Google에 구걸해야 하느냐며 완전히 새 플랫폼이 필요하다고 하자,
TeMPOraL은 은행과 금융, 기업, 정부 앱과 저작권 있는 미디어가 기기에 과도한
통제를 요구하는 주체이고, 새 모바일 플랫폼이 아니라 개방형 플랫폼이 성공하지
못하는 이유라고 답했다.[^liendolucas][^tempoRal]
Aerroon도 이런 OS들이 규제상 종속(regulatory lock-in)에 놓였다고 했는데, 은행
앱이 대체 OS에서 돌지 않고 일부 나라에서는 온라인 정부 서비스도 표준 경로로 쓸
수 없다는 것이다.[^aerroon]
ajnin은 기기 증명(SafetyNet 등)이 비공식 기기에서 실패해 GrapheneOS 같은 OS에서
은행·신분증 앱이 거부된다고 짚었다.[^ajnin]
그렇다면 사이트가 지적하는 통제는 Google 하나의 결정이 아니라, 앱을 내는 쪽이
기기를 신뢰할 수 있는 상태로 요구하는 구조의 한 단계다.
이 구조는 대체 OS를 만들어도 앱이 따라오지 않는 문제를 낳고, 캠페인의
해법(F-Droid 설치)이 풀 수 없는 부분이다.

### 증명은 이미 우회 가능하다는 개발자 증언이 있다

crowbahr는 대기업 Android 개발자로서 Graphene 팀과 협의했는데 Google API 없이도
증명을 할 수 있다고 했다.
GrapheneOS의 인증서 체인을 백엔드 서비스에 추가하면 되고, 번거롭지만 스프린트
하나 정도의 일이라는 설명이다.[^crowbahr]
이는 한 개발자의 증언이며, 팀 규모와 우선순위에 따라 현실적이지 않을 수 있다고
본인이 덧붙였다.
앱을 내는 쪽이 대체 OS를 받아들이도록 설득하는 비용이 구조의 열쇠라는 점을 보여
준다.

### 이 글을 읽는 방법

캠페인 사이트는 한쪽의 가장 강한 주장을 모은 문서이므로, 정책의 실제 내용은
Google의 발표와 개발자 문서에서 따로 확인해야 한다.
설치를 자주 하는 사용자와 개발자가 오늘 할 수 있는 일은 두 가지다.
자신이 쓰는 앱 가운데 F-Droid나 APK 직접 설치에 의존하는 것이 얼마나 되는지 세어
보고, 개발자라면 미등록 상태의 배포 경로(ADB, 개발자 모드 흐름)가 시행 후에
어떻게 되는지 공식 문서로 확인하는 것이다.
이 캠페인의 주장을 가를 관찰은 두 가지다.
2027년 시행 뒤 24시간 대기 절차가 유지되는지 더 어려워지는지, 그리고 정책이
실제로 사기 피해를 줄였다는 수치가 나오는지다.
둘 다 시행 전에는 확인되지 않는다.

---

[^filosottile]: <https://news.ycombinator.com/item?id=50208812>

[^lookeey]: <https://news.ycombinator.com/item?id=50208804>

[^rjh29]: <https://news.ycombinator.com/item?id=50208756>

[^chrisrr]: <https://news.ycombinator.com/item?id=50209946>

[^purelyapplied]: <https://news.ycombinator.com/item?id=50210236>

[^contravariant]: <https://news.ycombinator.com/item?id=50210255>

[^kykat]: <https://news.ycombinator.com/item?id=50208958>

[^habitue]: <https://news.ycombinator.com/item?id=50209052>

[^liendolucas]: <https://news.ycombinator.com/item?id=45745309>

[^tempoRal]: <https://news.ycombinator.com/item?id=45745827>

[^aerroon]: <https://news.ycombinator.com/item?id=50208896>

[^ajnin]: <https://news.ycombinator.com/item?id=45744547>

[^crowbahr]: <https://news.ycombinator.com/item?id=45754604>
