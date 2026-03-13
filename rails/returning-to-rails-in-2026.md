# Returning To Rails in 2026

DevOps 아키텍트이자 베이시스트인 Mark Dastmalchi-Round가 커버 밴드의 셋리스트
관리 앱([setlist.rocks](https://setlist.rocks))을 만들며 13~14년 만에 Rails로
돌아온 경험을 공유한 글이다.

## 요약

저자는 Rails 3~4 시절 이후 오랫동안 Rails를 떠나 있었다.
2025 Stack Overflow 설문에서 Rails는 20위, Ruby는 Lua와 어셈블리 아래에 위치할
정도로 인기가 식었지만, 순수하게 즐기기 위한 사이드 프로젝트에서 Ruby를 다시
선택했다.

Rails 8에서 달라진 핵심은 세 가지다.

**프론트엔드 혁신.** Webpack을 걷어내고 "No Build" 방식을 채택했다.
Hotwire(Turbo + Stimulus)로 SPA 같은 반응성을 서버 사이드 렌더링 위에 얹었고,
`importmap`으로 JS 패키지를 NPM·번들러 없이 관리한다.

**Solid 라이브러리.** Solid Cache, Solid Queue, Solid Cable이 Redis를 대체한다.
데이터베이스만으로 캐싱, 백그라운드 Job, 웹소켓(WebSocket)을 처리하므로 인프라
복잡도가 대폭 줄었다.

**SQLite 프로덕션 지원.** Rails 8은 WAL 모드, `synchronous: normal` 등 성능
최적화 PRAGMA를 기본으로 설정하여 SQLite를 중소 규모 프로덕션에서 실제로 쓸 수
있게 만들었다. `database.yml`에 `pragmas:` 블록이 추가되어 과거처럼
monkey-patch할 필요가 없다.

**배포.** Kamal이 기본 배포 도구로 자리잡았다.
`kamal deploy` 한 줄로 컨테이너 빌드, 푸시, 무중단 배포까지 처리한다.
kamal-proxy가 헬스 체크와 트래픽 전환을 담당하며, Let's Encrypt TLS도
기본 지원한다. 과거 Capistrano나 Ansible 플레이북으로 고생하던 배포가 Heroku
수준으로 단순해졌다.

저자는 AI를 이용해 프론트엔드 UI를 생성한 것에 대해 윤리적 갈등을 고백한다.
음악·예술·글쓰기에서의 AI 생성물은 혐오하면서 코드에서는 활용하는 모순을
스스로 인지하고 있다.

## 분석

### Rails의 "One Person Framework" 전략이 현실화되었다

DHH가 주창한 "한 사람이 전체 웹 앱을 만들 수 있는 프레임워크"라는 비전이
Rails 8에서 비로소 완성형에 가까워졌다.
Solid 라이브러리가 Redis를 없앴고, SQLite PRAGMA 기본값이 별도 DB 서버를
없앴고, Kamal이 별도 PaaS를 없앴다.
각각은 작은 변화지만 합치면 의존성 스택 전체가 사라진다.
Django나 Laravel이 비슷한 방향을 모색하고 있지만 이 정도로 극단적인 단순화를
이룬 프레임워크는 아직 없다.

### importmap은 JS 생태계에 대한 의미 있는 반론이다

Node.js 런타임, NPM, 번들러라는 삼중 의존성을 브라우저 네이티브 ES 모듈
import로 대체한 것은 단순한 편의가 아니다.
프론트엔드 빌드 파이프라인이라는 개념 자체에 도전하는 아키텍처적 결정이다.
물론 대규모 SPA에서는 트리 셰이킹이나 코드 스플리팅이 여전히 필요하지만,
Rails가 겨냥하는 "풀스택 한 명" 시나리오에서는 이 트레이드오프가 합리적이다.

### SQLite 프로덕션 전환은 인프라 패러다임 전환이다

SQLite의 WAL 모드 + `synchronous: normal` 조합은 읽기 동시성 문제를 해결하고
쓰기 성능을 극적으로 개선한다.
여기에 Solid Cache까지 SQLite에 올리면, 단일 파일 데이터베이스 하나로
애플리케이션, 캐시, Job 큐, 케이블 채널을 모두 운영하게 된다.
이는 Litestack, Litestream 같은 프로젝트와 합류하여 "SQLite 위의 풀스택"이라는
새로운 배포 패턴을 형성하고 있다.

### Kamal은 Heroku의 빈자리를 정확히 겨냥한다

Heroku가 "sustaining engineering model"로 전환하면서 사실상 혁신이 멈췄다.
Kamal은 `deploy.yml` 하나로 컨테이너 빌드·배포·프록시·시크릿 관리를
통합하여 "셀프 호스팅 PaaS"를 구현했다.
SSH만 있으면 되므로 VPS 한 대에서 시작해 쿠버네티스(Kubernetes) 클러스터로
확장하는 경로가 열려 있다.

## 비평

### 저자가 회피한 논점들

**동시 쓰기(Concurrent Writes) 문제를 과소평가했다.**
WAL 모드에서도 SQLite는 쓰기 잠금이 단일이다.
읽기 동시성은 해결되지만, 쓰기가 몰리는 워크로드에서는 여전히 병목이 된다.
"중소 규모"라는 조건부를 달았지만 그 경계선이 어디인지에 대한 언급이 없다.

**Hotwire의 한계를 다루지 않았다.**
Turbo Frames/Streams는 서버 의존적이라 오프라인이나 복잡한 클라이언트 사이드
상태 관리가 필요한 경우 한계가 명확하다.
셋리스트 앱 수준에서는 문제가 안 되지만, 일반론으로 확장하기엔 무리가 있다.

**커뮤니티 축소에 대해 감성적으로 접근했다.**
"stubborn bastard"라는 자조적 표현으로 유머를 섞었지만, 생태계 축소가
실무적으로 의미하는 것, 즉 채용 어려움, 라이브러리 유지보수 중단, 보안 패치
지연 같은 현실적 리스크에 대한 분석이 부족하다.

### AI 활용에 대한 윤리적 갈등은 정직하지만 얕다

저자는 AI 생성 음악·예술을 혐오하면서 코드에서는 AI를 활용하는 모순을
인정한다.
그러나 "코드도 창작이 아닌가?"라는 질문을 던져놓고 답하지 않는다.
Bootstrap 템플릿을 쓰는 것과 AI가 생성한 UI를 쓰는 것의 차이가 정말
없는지, "도구"와 "대체"의 경계는 어디인지 더 파고들었으면 훨씬 풍부한
논의가 되었을 것이다.

## 인사이트

### 1. "지루한 기술"의 역설

Rails가 다시 매력적인 이유는 역설적으로 "지루해졌기" 때문이다.
유행을 좇는 개발자들이 떠난 자리에서 프레임워크는 조용히 성숙했다.
Solid 라이브러리, SQLite 최적화, Kamal 같은 실용적 개선은 화제성이 아닌
실효성을 추구한 결과다.
Dan McKinley의 "Choose Boring Technology" 테제가 프레임워크 수준에서 입증된
사례라 할 수 있다.

### 2. 복잡도 제거가 곧 기능이다

Rails 8의 진짜 신기능은 추가된 것이 아니라 제거된 것에 있다.
Redis 없이 캐싱, NPM 없이 JS 관리, PostgreSQL 없이 프로덕션 운영, Heroku 없이
무중단 배포.
소프트웨어 아키텍처에서 가장 과소평가되는 작업이 "의존성 제거"인데, Rails 8은
이것을 체계적으로 실행했다.
각 Solid 라이브러리는 그 자체로 대단한 기술이 아니라, "왜 이걸 위해 별도
인프라가 필요했지?"라는 질문에 대한 답이다.

### 3. "Full-Stack Solo Developer" 시대의 도래

Solid 스택 + SQLite + Kamal 조합은 혼자서 프로덕션급 웹 애플리케이션을
운영하는 비용을 극적으로 낮춘다.
VPS 한 대, 도메인 하나, `kamal deploy` 한 줄이면 된다.
이는 인디 해커(Indie Hacker)와 소규모 SaaS 창업자에게 특히 의미가 크다.
Pieter Levels가 PHP + SQLite로 보여준 "1인 개발 제국"의 가능성이 Rails에서도
열리는 것이다.

### 4. 프레임워크의 생존 전략으로서의 "의견(Opinionated) 강화"

React 생태계가 선택 피로(Decision Fatigue)로 몸살을 앓는 동안 Rails는 정반대
방향으로 갔다.
배포 도구도 정해주고(Kamal), 캐시 백엔드도 정해주고(Solid Cache), JS 관리
방식도 정해준다(importmap).
이 "독선적" 접근이 오히려 경쟁 우위가 되고 있다.
개발자가 내려야 할 결정의 수를 줄이는 것 자체가 생산성 향상이기 때문이다.

### 5. 인기 지표와 기술 성숙도의 괴리

Stack Overflow 설문에서 Ruby가 어셈블리 아래에 있다는 것은 "인기"의 측정이
"가치"의 측정이 아님을 보여준다.
Shopify, GitHub, Basecamp 같은 대규모 서비스가 여전히 Rails 위에서 돌아간다.
Devise의 릴리스 빈도 감소를 "쇠퇴"로 볼 수도 있지만, 2010년부터 매년 꾸준히
릴리스하는 Rails 본체의 그래프는 다른 이야기를 한다.
"활동량"과 "건강함"은 다르다.
성숙한 프로젝트는 조용한 법이다.

### 6. 베이시스트의 시선

저자가 자신을 "엔진 룸" 개발자로, 베이스 기타리스트로 위치시키는 것은 단순한
비유가 아니다.
베이스는 눈에 띄지 않지만 밴드의 기반을 잡아주는 악기다.
마찬가지로 Rails는 "섹시한" 기술이 아니지만 웹의 기반 인프라로서 묵묵히
작동한다.
이 관점은 기술 선택에서 "유행"보다 "기반"을 우선하는 사고방식을 함축한다.
화려한 솔로보다 단단한 그루브가 중요할 때가 있다.

---

- <https://www.markround.com/blog/2026/03/05/returning-to-rails-in-2026/>
- [Hacker News 토론](https://news.ycombinator.com/)
- [lobste.rs 토론](https://lobste.rs/)
- <https://setlist.rocks>
- <https://kamal-deploy.org/>
- <https://github.com/rails/solid_cache>
- <https://github.com/rails/solid_queue>
- <https://github.com/rails/solid_cable>
- <https://github.com/hotwired/turbo-rails>
- <https://stimulus.hotwired.dev/>
