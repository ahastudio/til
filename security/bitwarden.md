# Bitwarden: 오픈소스와 셀프호스팅을 내세우며 AI 에이전트 자격 증명까지 넓히는 비밀번호 관리자

<https://bitwarden.com/>

HN 토론: <https://news.ycombinator.com/item?id=37640816> (455점, 299개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/huzx4s/bitwarden_opensource_password_manager> (8점, 28개 댓글)

## 소개

Bitwarden은 Bitwarden, Inc.가 만드는 비밀번호 관리자다.
홈페이지는 이 제품을 “THE MOST TRUSTED PASSWORD MANAGER”라고 부른다.
사람과 AI 에이전트(AI agent)와 기계가 쓰는 자격 증명, 패스키, 민감한 정보를
한곳에서 저장하고 공유하고 관리하게 한다는 설명이 이어진다.
이 문서는 홈페이지와 회사가 공개한 요금, 감사, 라이선스, 설치 문서,
GitHub 저장소 정보를 읽고 정리한 것이며 직접 설치하거나 써 보지 않았다.
홈페이지의 서술은 모두 회사의 주장이다.
이 문서는 따로 확인한 것과 확인하지 못한 것을 나누어 적는다.

홈페이지가 앞세우는 근거는 숫자와 평가다.
수백만 고객이 쓴다는 문구와 크롬과 앱 스토어 평점,
GitHub와 포럼과 Reddit의 커뮤니티 구성원 10만 명 이상,
Top 50 Best Software Products 선정이 나온다.
G2의 2026년 가을 비밀번호 관리자 보고서에서 고객 만족도 1위(99점)를 받았다는
주장도 있다.
NASA, Glovo, Namecheap 같은 조직의 담당자 인용문이 그 뒤를 잇는다.

## 제품 구성과 요금

홈페이지의 요금표는 미화 기준이고 연간 결제 값이며 세금은 포함하지 않는다.

| 요금제     | 가격                                | 회사가 밝힌 내용                                       |
| ---------- | ----------------------------------- | ------------------------------------------------------ |
| 무료       | 0달러                               | 기본 비밀번호 관리                                     |
| Premium    | 월 1.65달러(연 19.80달러)           | 통합 인증기, 파일 첨부, 비상 접근, 보안 보고서         |
| Families   | 월 3.99달러(연 47.88달러), 최대 6명 | 프리미엄 계정 6개, 무제한 공유와 컬렉션                |
| Teams      | 사용자당 월 4달러                   | 공유, 이벤트 로그, 디렉터리 동기화, SCIM               |
| Enterprise | 사용자당 월 6달러                   | 세분화된 접근 제어, 패스워드리스 SSO, 정책, 셀프호스팅 |

요금 페이지도 같은 값을 보여 주고,
모든 계정에 기기와 비밀번호 개수 제한이 없고
패스키 관리와 Bitwarden Send와 다른 한 사용자와의 무료 공유가 들어간다고 적는다.[^pricing]
Enterprise 요금제에는 모든 사용자에게 무료 Families 요금제가 붙는다고 한다.[^pricing]

비밀번호 관리자 외의 제품도 메뉴에 있다.
개발자와 DevOps 팀을 위한 Secrets Manager,
패스키 인증 API를 주는 Passwordless.dev,
단독 앱인 Bitwarden Authenticator가 그것이다.
홈페이지 상단 배너는 새 기능으로 시간 제한 자격 증명 대여(credential leasing),
비밀번호 자동 교체, 접근 규칙을 알린다.

## TOTP와 인증기

홈페이지의 Personal 메뉴는 Integrated TOTP를 비밀번호와 함께 2FA 코드를
자동 입력하는 기능으로 소개한다.
회사의 도움말은 조건을 더 자세히 적는다.
TOTP 키를 저장하는 것은 모든 계정이 할 수 있지만
코드를 생성하는 것은 Premium이나 유료 조직(Families, Teams, Enterprise)
소속일 때만 가능하다.
코드는 6자리이고 SHA-1을 쓰며 30초마다 바뀐다.[^integrated]

Bitwarden Authenticator는 별개의 앱이다.
회사는 이 앱이 iOS와 Android에서 무료이고 오픈소스이며
Bitwarden 계정 없이도 쓸 수 있다고 말한다.[^authapp]

## 오픈소스와 라이선스

홈페이지는 이 플랫폼을 오픈소스이고 종단 간 암호화(end-to-end encrypted)된
플랫폼으로 소개하고, 누구나 검사할 수 있는 공개 코드를 신뢰의 근거로 든다.
오픈소스 페이지는 서버, 브라우저 확장, 웹 보관함, 모바일, 데스크톱, CLI의
저장소를 안내하고 AES-256과 PBKDF2 SHA-256 인증을 쓴다고 적는다.[^os]

라이선스 FAQ는 구분이 더 복잡하다고 알려 준다.
개인 보관함의 핵심 클라이언트는 GPL 3.0이고 주 서버는 AGPL 3.0이다.
주로 큰 조직을 위한 일부 모듈은 Bitwarden License라는 “source available”
상용 라이선스를 따르며, 운영 환경에서 쓰려면 유료 구독이 필요하다.
FAQ는 이 라이선스가 OSI 정의에 따른 오픈소스가 아니라고 스스로 밝힌다.[^faq]

2026년 11월 9일에 GitHub API가 보고한 `bitwarden/server`는 별 20,604개,
포크 1,837개, 열린 이슈 295개이고 주 언어가 C#이다.[^gh-server]
`bitwarden/clients`는 별 14,182개, 포크 2,203개, 열린 이슈 1,448개이고
주 언어가 TypeScript다.[^gh-clients]
두 저장소 모두 GitHub의 라이선스 필드가 `NOASSERTION`이어서
하나의 SPDX 식별자로 표시되지 않는다.
스토어 배포판을 상용 라이선스 빌드로 바꾼 일은 이 저장소의
`security/bitwarden-app-store-license.md`에 따로 정리되어 있다.

## 감사와 인증

회사의 감사 페이지는 연간 외부 감사를 받는다고 하며 보고서를 연도별로 나열한다.
2025년 항목은 Cure53이 맡은 브라우저 확장과 자동 입력 오버레이, 핵심 애플리케이션,
데스크톱, RustCrypto 크레이트와 라이브러리, 웹 보관함 평가가 있다.
ETH Zurich의 응용 암호 그룹이 서버가 완전히 악의적이라는 가정에서
핵심 암호 연산을 감사한 보고서도 있다.
Unit 42의 모바일 앱 평가와 Fracture Labs의 웹 앱과 네트워크 평가가 더해진다.
2024년 항목에는 IOActive, Paragon Initiative Enterprises, Mandiant, Fracture Labs,
Cure53의 보고서가 올라 있다.
같은 페이지는 GDPR, CCPA, Data Privacy Framework, HIPAA, ISO 27001을
준수하거나 인증받았다고 적는다.[^audit]
오픈소스 페이지는 여기에 SOC 2를 더한다.[^os]
이 문서는 보고서 본문을 읽지 않았다.

## 셀프호스팅

오픈소스 페이지는 Docker로 전체 서버 구성을 직접 운영할 수 있다고 하며
설치 스크립트를 내려받아 실행하는 명령을 보여 준다.[^os]
Linux 표준 배포 문서의 최소 사양은 x64 1.4GHz, 메모리 2GB, 저장 공간 12GB이고
권장은 2GHz 듀얼 코어, 4GB, 25GB다.
Docker Engine은 26 이상이 필요하다.[^install]

셀프호스팅 자체는 무료지만 일부 기능은 등록된 라이선스 파일로 풀어야 한다.
이 파일은 클라우드 계정의 구독 설정에서 내려받아 자체 서버에 적용하며,
개인 Premium 라이선스와 조직 라이선스가 따로 있다.[^licensing]
공식 서버 대신 호환 서버를 쓰는 길은 이 저장소의 `otp/vaultwarden.md`가 다룬다.

## AI 에이전트와 특권 접근

홈페이지는 AI 에이전트의 자격 증명 관리를 새 방향으로 내세운다.
관련 페이지는 Access Intelligence로 조직 안의 비공식 AI 사용을 찾고,
Secrets Manager로 코드의 하드코딩된 비밀을 대체하며,
오픈소스 Agent Access SDK로 승인된 에이전트에 사람 검토를 거친 즉시 접근을 주고,
Bitwarden MCP 서버로 관리 작업을 자연어로 한다고 설명한다.[^agent-sec]

상단 배너의 특권 접근 기능은 Privileged Controls라는 이름이다.
회사의 블로그는 이 기능이 비공개 프리뷰 단계이고,
출시 시점의 자동 비밀번호 교체는 Microsoft Entra ID만 지원하며
다른 대상은 관리자에게 앱 안에서 알려 직접 교체하게 한다고 밝힌다.[^privileged]
이 문서는 두 기능을 시험하지 않았다.

## 비평

### 신뢰의 근거가 자사 수치와 선별된 인용문에 머문다

수백만 고객, 10만 명 이상의 커뮤니티, Top 50 선정,
G2 1위와 99점은 모두 홈페이지가 직접 적은 숫자다.
홈페이지는 이 수치의 집계 방식과 기준 시점을 알려 주지 않고,
이 문서는 G2 보고서를 열어 보지 않았다.
담당자 인용문도 회사가 고른 것이다.
그러므로 홈페이지만으로는 가장 신뢰받는다는 문구를 판단할 수 없다.
확인할 수 있는 것은 공개된 코드와 감사 보고서 목록이며,
그 보고서의 범위와 발견 사항은 보고서를 읽어야 안다.
2023년 HN 스레드에서 nichtverstehen은 감사 목록이 클라이언트 구현에 집중되어 있고
전체 보안 모델은 판단하지 않는다고 썼다.
비밀번호 하나가 로그인과 보관함 복호화에 모두 쓰인다는 점도 걱정했다.[^nichtverstehen]
이는 한 사용자의 평가이며 이 문서는 확인하지 못했다.
2016년 Lobste.rs 스레드에서 vale는 당시 홈페이지의 가장 안전하다는 문구의 근거와
위협 모델을 물었다.[^vale]
자신을 주 개발자라고 밝힌 xxkylexx는 그 주장이 주관적이고 편향이 있다고 인정하면서,
전체가 오픈소스라는 점이 다른 서비스와의 차이라고 답했다.[^xxkylexx]
지금의 홈페이지도 공개 코드를 신뢰의 근거로 앞세운다.

### 오픈소스라는 말이 코드 전체에 같은 뜻으로 쓰이지 않는다

홈페이지의 오픈소스 문구는 플랫폼 전체에 붙어 있다.
라이선스 FAQ는 핵심 클라이언트와 서버는 GPL과 AGPL이지만
일부 모듈은 OSI 기준의 오픈소스가 아닌 상용 라이선스라고 구분한다.
GitHub의 라이선스 필드가 하나의 식별자를 주지 못하는 것도 같은 사정이다.
기존 문서가 정리한 스토어 배포판의 상용 빌드 전환은
이 구분이 사용자가 받는 앱에까지 닿는다는 점을 보여 준다.
홈페이지는 이 구분을 말하지 않는다.
HN에서 wmal은 서버가 AGPL과 source available 라이선스로 나뉘어 있어
제목의 free and open-source가 오해를 부른다고 지적했다.[^wmal]
skjoldr는 상용 라이선스가 일부 모듈에 한정되고 나머지는 자유롭다고 반박했다.[^skjoldr]
따라서 오픈소스를 이유로 고른다면 어느 모듈과 어느 빌드를 쓰는지를 따로 봐야 한다.

### 무료와 유료의 경계가 도움말에 가서야 드러난다

요금표는 Premium을 월 1.65달러로 보여 주지만 월 결제가 아니라 연 19.80달러의
연간 결제 값이다.
Personal 메뉴는 Integrated TOTP를 설명하면서 Premium이 필요하다는 말을 하지 않는다.
이 조건은 도움말에 있고, 무료로 코드를 만들려면 별개의 Authenticator 앱을
써야 한다.
셀프호스팅도 비슷하다.
홈페이지와 요금 페이지는 셀프호스팅 유연성을 Enterprise 항목에 적지만,
도움말은 셀프호스팅 자체는 무료이고 일부 기능만 라이선스 파일로 푼다고 하며
개인 Premium 라이선스를 적용하는 절차도 싣는다.
홈페이지만 읽은 사람은 개인이 셀프호스팅할 수 있는지 알기 어렵다.
HN의 antioxidant는 2FA 코드 추가에 돈이 들고
셀프호스팅은 일부러 어렵게 되어 있어 클라우드를 쓰게 된다고 썼다.[^antioxidant]
bad_user는 셀프호스팅이 비싸고 Vaultwarden은 감사를 받은 적이 없는 것으로 안다고 했다.[^bad_user]
Jnr은 집의 서버에서 여러 서비스와 함께 돌리면
한 달 전기료가 3유로 정도이고 유지도 쉽다고 답했다.[^Jnr]
비용과 난이도 평가가 사람마다 갈린다는 뜻이며 이 문서는 어느 쪽도 시험하지 않았다.

### 새 영역의 주장은 검증할 근거가 얇다

배너는 특권 접근 기능을 NEW로 알리지만 프리뷰 단계라는 말은 블로그에만 나온다.
AI 에이전트 페이지는 도구와 SDK를 나열하며 83%와 같은 통계는 외부 조사를
인용한다.
이 문서는 그 통계의 원문을 열지 않았고, 두 기능의 동작과 한계도 확인하지 못했다.
회사가 이 방향에 무게를 두는 만큼 핵심인 비밀번호 보관 기능과 새 영역의
성숙도는 따로 구분해서 봐야 한다.

## 도입 전에 따져볼 것

- 필요한 기능이 무료 요금제로 되는지 확인한다. TOTP 코드 생성은 Premium이나 유료 조직이 필요하고, 무료로는 별개의 Authenticator 앱이 있다.
- 셀프호스팅을 계획하면 쓰려는 기능이 라이선스 파일을 요구하는지 먼저 확인한다. Linux 서버는 최소 메모리 2GB와 저장 공간 12GB가 필요하다.
- 오픈소스가 이유라면 스토어에서 받는 클라이언트가 어느 빌드인지, 쓰려는 모듈이 GPL과 AGPL 쪽인지 확인한다. 재배포나 서비스 제공이 목적이면 라이선스 FAQ를 먼저 읽는다.
- 감사 보고서를 직접 열어 범위, 발견 사항, 수정 여부를 확인한다. 이 문서는 목록만 읽었다.
- 특권 접근과 AI 에이전트 기능은 프리뷰 여부와 지원 대상을 확인한 뒤 도입을 판단한다.
- 비용 없이 직접 운영하는 쪽이 목적이라면 공식 서버 외에 호환 서버를 쓰는 선택지와 그 위험을 함께 본다.

---

[^pricing]: Bitwarden, [Bitwarden Password Manager Pricing & Plans | Bitwarden](https://bitwarden.com/pricing/)

[^integrated]: Bitwarden, [Integrated Authenticator | Bitwarden](https://bitwarden.com/help/integrated-authenticator/)

[^authapp]: Bitwarden, [Bitwarden Authenticator | Bitwarden](https://bitwarden.com/products/authenticator/)

[^os]: Bitwarden, [Open Source Password Manager | Bitwarden](https://bitwarden.com/open-source/)

[^faq]: Bitwarden, [Bitwarden and Open Source](https://github.com/bitwarden/server/blob/main/LICENSE_FAQ.md)

[^gh-server]: GitHub, [bitwarden/server](https://github.com/bitwarden/server)

[^gh-clients]: GitHub, [bitwarden/clients](https://github.com/bitwarden/clients)

[^audit]: Bitwarden, [Compliance, Audits, and Certifications | Bitwarden](https://bitwarden.com/help/is-bitwarden-audited/)

[^install]: Bitwarden, [Linux Standard Deployment | Bitwarden](https://bitwarden.com/help/install-on-premise-linux/)

[^licensing]: Bitwarden, [License Organizations or Premium | Bitwarden](https://bitwarden.com/help/licensing-on-premise/)

[^agent-sec]: Bitwarden, [Securing Agentic AI with Bitwarden | Bitwarden](https://bitwarden.com/solutions/agentic-ai-security/)

[^privileged]: Bitwarden, [Bitwarden Privileged Controls: Secure your most sensitive accounts in minutes | Bitwarden](https://bitwarden.com/blog/bitwarden-privileged-controls-secure-your-most-sensitive-accounts-in-minutes/)

[^nichtverstehen]: <https://news.ycombinator.com/item?id=37641632>

[^wmal]: <https://news.ycombinator.com/item?id=37641408>

[^skjoldr]: <https://news.ycombinator.com/item?id=37642130>

[^antioxidant]: <https://news.ycombinator.com/item?id=37641080>

[^bad_user]: <https://news.ycombinator.com/item?id=37641280>

[^Jnr]: <https://news.ycombinator.com/item?id=37644035>

[^vale]: <https://lobste.rs/s/huzx4s/bitwarden_opensource_password_manager#c_nzzhxx>

[^xxkylexx]: <https://lobste.rs/s/huzx4s/bitwarden_opensource_password_manager#c_tuqqrk>
