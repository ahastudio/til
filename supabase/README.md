# Supabase: Postgres 하나를 중심에 두고 Firebase의 기능을 오픈소스로 다시 짠 개발 플랫폼

<https://supabase.com/>

<https://github.com/supabase/supabase>

HN 토론: <https://news.ycombinator.com/item?id=23319901> (1120점, 366개 댓글)

GN 토론: <https://news.hada.io/topic?id=3347>

## 소개

Supabase는 스스로를 “Postgres 개발 플랫폼”이라고 부른다.
홈페이지의 첫 문구는 “주말에 만들고, 수백만 명까지 확장하라”이고,
프로젝트를 Postgres 데이터베이스로 시작한 뒤 인증, Data API, Edge Functions,
Realtime, Storage, 벡터 임베딩을 더하라고 권한다.
모든 프로젝트가 온전한 Postgres 데이터베이스이며,
“100% 이식 가능하다”는 것이 홈페이지가 앞세우는 약속이다.

GitHub 저장소의 README는 더 직접적으로 쓴다.
엔터프라이즈급 오픈소스 도구로 Firebase의 기능을 만들고 있다는 것이다.
적절한 도구와 커뮤니티가 MIT, Apache 2 같은 열린 라이선스로 이미 있으면 그것을
쓰고, 없으면 직접 만들어 공개한다.
다만 Supabase는 Firebase를 1대1로 옮긴 것이 아니며,
목표는 오픈소스 도구로 Firebase 같은 개발 경험을 주는 것이라고 덧붙인다.

저장소는 2019년 10월에 만들어졌고, 2026년 10월 기준 별 11만 1천여 개,
포크 1만 6천여 개를 기록하고 있다.
라이선스는 Apache 2.0이고 주 언어는 TypeScript다.
다만 이 저장소에 Supabase 전체가 들어 있지는 않다.
대시보드 Studio(`apps/studio`), 문서(`apps/docs`), 웹사이트(`apps/www`),
자체 호스팅용 Docker Compose 구성(`docker/`), 예제(`examples/`)를 담은
모노레포이고, Auth, Realtime, Storage 같은 서버는 각자의 저장소에 있다.

### 구성 요소

공식 아키텍처 문서는 하나의 Postgres 인스턴스 앞에 API 게이트웨이 Envoy가 서고,
그 사이에 여러 서비스가 놓이는 그림을 보여 준다.

| 구성 요소       | 하는 일                                      | 언어                | 라이선스   |
| --------------- | -------------------------------------------- | ------------------- | ---------- |
| Postgres        | 모든 데이터의 중심. 권한 제한 없이 접근 가능 | C                   | PostgreSQL |
| Studio          | 데이터베이스와 서비스를 관리하는 대시보드    | TypeScript          | Apache 2   |
| GoTrue(Auth)    | 사용자 관리와 JWT 발급, RLS와 연동           | Go                  | MIT        |
| PostgREST       | Postgres를 그대로 REST API로 노출            | Haskell             | MIT        |
| `pg_graphql`    | GraphQL API를 제공하는 Postgres 확장         | Rust                | Apache 2   |
| Realtime        | Presence, 브로드캐스트, DB 변경 스트리밍     | Elixir              | Apache 2   |
| Storage API     | S3 호환 객체 저장소. 메타데이터는 Postgres   | Node.js, TypeScript | Apache 2   |
| Edge Functions  | Deno 기반 서버 측 TypeScript 함수            | TypeScript, Rust    | MIT        |
| `postgres-meta` | 테이블 조회, 역할 추가 등 관리용 REST API    | Node.js, TypeScript | Apache 2   |
| Supavisor       | 멀티테넌트 Postgres 연결 풀러                | Elixir              | Apache 2   |
| Envoy           | API 게이트웨이                               | C++                 | Apache 2   |

`pg_graphql`의 언어와 라이선스는 아키텍처 문서에 적혀 있지 않아 표에서 저장소
기준으로 보충했다.
README의 아키텍처 목록에는 Supavisor가 빠져 있고,
아키텍처 문서에는 들어 있다.

### 제품 원칙

아키텍처 문서는 대기업이 스스로 설계할 법한 구조를 제공하고,
그 위에 개인 개발자와 작은 팀도 쓰기 쉬운 도구를 얹는 것이 목표라고 밝힌다.
그 목표를 지키는 원칙은 네 가지다.

첫째, 모든 것은 따로 동작한다.
“Postgres 데이터베이스 하나만으로 이 제품을 돌릴 수 있는가”가 판별 기준이다.
둘째, 모든 것은 통합된다.
각 도구는 API와 웹훅을 노출해 다른 제품의 가치를 열 배로 키워야 한다.
셋째, 모든 것은 확장 가능하다.
새 도구를 늘리기보다 기존 도구를 확장하고, 틈새 기능 대신 기본 요소를 준다.
넷째, 모든 것은 이식 가능하다.
`pg_dump`와 CSV 같은 기존 표준을 쓰고, Supabase 방식과 경쟁하는 새 표준이
나오면 자기 방식을 폐기하겠다고 약속한다.

### 쓰는 방법

호스팅 플랫폼에 가입하면 아무것도 설치하지 않고 바로 쓸 수 있다.
CLI로 로컬 개발 환경을 띄울 수 있고, Docker Compose로 자체 호스팅도 가능하다.
공식 클라이언트는 JavaScript(TypeScript), Flutter, Swift, Python이고,
C#, Go, Java, Kotlin, Ruby, Rust, Godot용은 커뮤니티가 관리한다.
클라이언트도 모듈식이어서, 예컨대 `supabase-js`는 `postgrest-js`,
`auth-js`, `realtime-js`, `storage-js`, `functions-js`를 묶은 것이다.

홈페이지의 React 예제는 이 플랫폼의 성격을 한눈에 보여 준다.
`createClient`로 클라이언트를 만든 뒤 컴포넌트 안에서
`supabase.from('todos').select('*')`로 테이블을 바로 읽는다.
그 사이에 직접 만든 서버는 없다.

## 분석

### Postgres를 감추지 않는다는 선택이 제품 전체를 정한다

Firebase는 데이터베이스를 추상화된 문서 저장소로 감추고,
그 위에서 보안 규칙이라는 별도 언어를 쓰게 했다.
Supabase는 정반대로 간다.
아키텍처 문서는 Postgres를 추상화하지 않으며 모든 권한으로 접근할 수 있다고
분명히 적는다.
NoSQL 대신 Postgres를 고른 것은 의도된 선택이었고,
Firebase와 경쟁할 기능과 그 너머로 갈 확장성을 함께 주는 데이터베이스가
Postgres밖에 없다고 봤다는 것이다.

2020년 HN 출시 스레드에서 RNCTX는 이 방향을 “데이터베이스로 돌아가기”라고
불렀다.
프레임워크가 하나같이 루트 권한의 DB 연결부터 요구하면서,
수십 년 동안 데이터베이스에 쌓인 보안 기능을 무시하고 DB를 멍청한 저장소로
만든다는 불만이었다.[^RNCTX]
공동 창업자 kiwicopple은 이 말에 전적으로 동의한다고 답했다.[^kiwicopple-db]
반면 pm90은 DB 수준의 접근 제어가 하나의 DB를 여러 앱이 나눠 쓰던 시대의
산물이라고 반박했다.
앱마다 DB를 따로 두는 지금은 오히려 마이그레이션 사용자가 테이블에 접근하지
못하는 식의 장애물이 된다는 것이다.[^pm90]
Supabase는 이 논쟁에서 분명히 한쪽을 골랐고,
이후 RLS가 플랫폼 전체의 권한 모델이 되었다.

이 선택은 다른 모든 구성 요소의 모양을 정한다.
권한은 Postgres의 Row Level Security로 표현하고,
API는 PostgREST가 스키마를 읽어 자동으로 만들며,
Storage는 파일 메타데이터와 권한을 Postgres에 둔다.
Queues는 `pgmq`, Cron은 `pg_cron`, 외부 HTTP 호출은 `pg_net`이라는 확장으로
들어온다.
제품 원칙의 “Postgres 데이터베이스 하나만으로 돌릴 수 있는가”라는 기준이
여기서 실제 설계 규칙으로 작동한다.

Realtime의 출발점도 같은 선택에서 나왔다.
kiwicopple에 따르면 창업자들은 이전 회사에서 Firebase로 채팅 앱을 만들었는데,
고객의 메시지가 순서가 뒤바뀌어 도착하는 문제를 겪고
Postgres로 옮겼다.[^kiwicopple-realtime]
처음에는 트리거와 `NOTIFY`로 변경을 알렸지만,
테이블마다 트리거를 만들어야 했고 `NOTIFY`의 페이로드가 8000바이트로 제한돼
알림이 유실됐다.
그래서 Postgres의 논리적 디코딩을 읽는 Elixir 서버를 만들었고,
장애가 나도 메시지를 다시 재생할 수 있다는 점을
장점으로 꼽았다.[^kiwicopple-notify]

결과적으로 Supabase를 쓰는 개발자는 Firebase 사용자보다 훨씬 많은 것을
데이터베이스에 대해 알아야 한다.
아키텍처 문서는 이를 “편한 수준을 고르라”는 말로 누그러뜨린다.
Postgres를 단순한 테이블 저장소로 써도 괜찮고, 익숙해지면 더 깊이 들어가라는
것이다.
kiwicopple은 출시 당시 개발자들을 만나 보니 대부분 Postgres가 훌륭하다고
생각하면서도 더 쉽다는 이유로 Firebase를 골랐고,
그래서 “데이터베이스 UX”를 회사의 핵심 목표로 삼았다고 설명했다.[^kiwicopple-ux]

### 이 저장소는 Supabase 그 자체가 아니라 그 얼굴이다

`supabase/supabase` 저장소의 별 수는 Supabase의 인기를 대표하는 숫자로
자주 인용된다.
그러나 저장소의 실제 내용은 Studio, 문서, 웹사이트, 디자인 시스템,
자체 호스팅 구성이다.
사용자의 요청을 실제로 처리하는 Auth, PostgREST, Realtime, Storage,
Supavisor는 다른 저장소에 있고, 그중 PostgREST와 Envoy는 Supabase가 만든
것도 아니다.

이것은 README가 말하는 전략과 정확히 맞는다.
이미 좋은 오픈소스 도구가 있으면 그것을 쓰고, 없을 때만 만든다.
그 결과 Supabase의 고유한 코드는 서버보다 통합 계층, 즉 대시보드, CLI,
클라이언트 라이브러리, 문서, 그리고 여러 도구를 한 Postgres 위에 묶는 설정에
몰려 있다.
이 저장소가 TypeScript 모노레포인 이유도 거기에 있다.

### 홈페이지가 겨냥하는 사용자는 이미 바뀌었다

홈페이지의 고객 사례 첫 자리는 Lovable이다.
“AI가 만든 수백만 개의 앱을 완전한 Supabase 백엔드로 돌린다”는 문구가 붙어 있고,
eXp Realty 사례도 AI로 생성하거나 보조한 개발을 강조한다.
푸터의 솔루션 목록에는 “AI Builders”, “Vibe Coders”, “Agents”가 있고,
커뮤니티 후기에는 Supabase MCP로 RLS를 설정하고 마이그레이션 스크립트를
짰다는 이야기가 여러 개 실려 있다.

README가 그리는 사용자는 Firebase의 대안을 찾는 개발자다.
홈페이지가 그리는 사용자는 코드를 직접 다 쓰지 않는 사람, 그리고 그 사람을
대신해 백엔드를 고르는 에이전트다.
Supabase가 매주 100만 개가 넘는 데이터베이스를 만든다고 밝히며 Turso 인수를
발표한 것도 같은 방향이다.

2020년 출시 스레드와 비교하면 변화가 더 뚜렷하다.
당시 Firebase 개발자였던 habosa는 DB를 고르고, 서버를 띄우고, REST API를 만들고,
그것을 어떻게든 안전하게 만들고, 클라이언트에 CRUD 코드를 쓰는 과정을 2020년에도
모든 앱이 반복한다며 시간 낭비라고 썼다.[^habosa]
그 반복을 없애려던 도구가 이제는 코드를 쓰지 않는 사람을 위한
기본 백엔드가 됐다.
의료 데이터를 맡겨도 되느냐는 질문에 kiwicopple은 아직 너무 이르고 보안 감사도
받아야 하니 좋은 선택이 아니라고 답했다.[^kiwicopple-medical]
지금 홈페이지 푸터는 SOC2 Type 2, ISO 27001 인증과 HIPAA 준수를 내건다.

## 비평

### “100% 이식 가능”은 데이터에 대해서만 참이다

Postgres 데이터는 `pg_dump`로 그대로 옮길 수 있다.
이 점에서 이식성 약속은 대부분의 BaaS보다 훨씬 진지하다.
그러나 Supabase 위에서 만든 앱은 데이터만으로 이루어지지 않는다.
RLS 정책은 `auth.uid()`와 `anon`, `authenticated` 역할에 기대고,
클라이언트 코드는 PostgREST의 쿼리 문법과 `supabase-js`에 묶이며,
Edge Functions는 `withSupabase`와 Supabase의 환경 변수 규칙을 따른다.

이 범위는 처음부터 그랬다.
출시 스레드에서 Firebase에서 옮겨 오는 길을 묻자 kiwicopple은 데이터 저장소가
그냥 Postgres이므로 자유롭게 들어오고 나갈 수 있어
잠금이 없다고 답했다.[^kiwicopple-lockin]
잠금이 없다는 약속은 처음부터 데이터에 대한 것이었다.

이것들을 다른 곳으로 옮기려면 결국 같은 구성 요소를 직접 띄우는 수밖에 없다.
즉 “Supabase를 떠날 수 있다”는 말은 실제로는 “Supabase를 직접 운영하는
쪽으로 옮길 수 있다”에 가깝다.
그것도 의미 있는 선택지이지만, 홈페이지의 “never locked in”이 주는 인상보다는
좁다.

### 자체 호스팅은 같은 제품이 아니다

아키텍처 문서는 클라우드 제품이 자체 호스팅 제품과 호환된다고 쓴다.
그러나 자체 호스팅 문서는 관리형 플랫폼의 일부 기능을 쓸 수 없다고 따로 밝힌다.
브랜칭, 로그 이상의 고급 지표, 관리형 백업과 시점 복구(PITR),
분석 및 벡터 버킷, ETL, Management API가 그 목록이다.
Docker Compose 구성은 한 달에 한 번쯤 안정 스냅숏으로 나오며,
개별 서비스의 이미지 태그를 바꾸면 호환성은 보장되지 않는다.

이 간극은 초기부터 지적됐다.
HN 출시 스레드에서 x_stealth는 Supabase로 백엔드를 만들면 Realtime, PostgREST,
서버리스 함수, Postgres를 따로따로 관리하게 되는 것 아니냐고 물었고,
kiwicopple은 모든 것을 하나의 배포로
묶겠다고 답했다.[^x_stealth][^kiwicopple-selfhost]
같은 해 12월 GeekNews의 공개 베타 토픽에서도
zihado가 사내 구축 방법을 물었다.[^zihado]
xguru는 오픈소스라 구축할 수 있지만 컴포넌트별 Docker 이미지를 조합하기가 조금
번거로울 것이라고 답했다.[^xguru]
공동 창업자 awalias는 그 이미지들이 꽤 오래됐다고 인정하며,
엔터프라이즈 고객용 온프레미스 배포를
이듬해 가을에 완전히 지원하겠다고 했다.[^awalias]
하나의 배포로 묶는 일은 Docker Compose로 이루어졌지만,
운영 기능의 격차는 그 뒤로도 남았다.

빠진 목록을 보면 성격이 분명하다.
백업과 복구, 관찰 가능성, 환경 분리처럼 운영을 안전하게 만드는 기능이 빠져
있다.
API 호환이라는 의미의 이식성은 지켜지지만,
프로덕션을 책임질 수 있는 수준의 운영 경험은 호스팅 플랫폼에 남아 있다.
오픈소스 회사가 수익을 내는 자리가 거기라는 점을 생각하면 자연스러운
구조이지만, 이식성 약속을 평가할 때는 함께 봐야 한다.

### 클라이언트가 DB에 직접 붙는 구조는 기본값이 안전해야만 성립한다

홈페이지 React 예제는 서버 없이 테이블을 읽는다.
이 구조에서 보안은 전적으로 Postgres의 권한과 RLS에 달려 있다.
그런데 공식 문서에 따르면 기존 프로젝트에서는 `public` 스키마에 새로 만든
테이블에 `anon`과 `authenticated`의 읽기, 쓰기 권한이 자동으로 붙고,
정책을 추가해도 그 권한은 회수되지 않는다.
Supabase는 이 기본값을 바꾸는 중이라고 밝히고 있다.

출시 스레드에서도 이 구조는 가장 먼저 의심받았다.
idoby는 예제의 JavaScript가 브라우저에서 돈다면 클라이언트 코드를 서버 DB의
구현 세부에 묶는 셈이라며, 그런 구조에 데인 적이 많아 사양하겠다고 썼다.[^idoby]
kiwicopple은 서버 쪽에서도 돌릴 수 있고
자신들도 그렇게 한다고 답했다.[^kiwicopple-coupling]
InvOfSmallC는 그렇다면 비즈니스 로직은 어디에 구현하느냐고 물었고,[^InvOfSmallC]
bradyo는 PostgREST가 여러 테이블에 걸친 트랜잭션 API를 지원하지 않는다고
지적했다.[^bradyo]
이 질문들에 대한 지금의 답은 RLS, 데이터베이스 함수, Edge Functions의 조합이고,
그 조합을 올바르게 쓰는 책임은 여전히 개발자에게 있다.

“주말에 만든다”는 약속과 “기본적으로 모든 것이 노출된다”는 기본값은 같은 뿌리를
가진다.
테이블을 만들자마자 API로 쓸 수 있어야 빠르게 만들 수 있기 때문이다.
홈페이지가 겨냥하는 AI 빌더와 바이브 코더는 바로 이 기본값을 의심하지 않을
가능성이 가장 큰 사용자들이다.
Security Advisor와 MCP가 RLS 설정을 돕는다는 후기가 홈페이지에 실린 것은,
제품이 이 위험을 알고 도구로 메우려 한다는 뜻이기도 하다.

## 인사이트

### Supabase의 해자는 Postgres가 아니라 Postgres를 둘러싼 기본값이다

Supabase의 구성 요소는 거의 모두 따로 구할 수 있다.
Postgres는 어디서나 호스팅되고, PostgREST와 GoTrue 계열 인증 서버도 공개돼
있으며, Neon이나 RDS 위에 같은 조합을 얹을 수도 있다.
그런데도 사람들이 Supabase를 고르는 이유는 이 조각들이 서로를 이미 알고 있기
때문이다.
JWT의 `sub`가 `auth.uid()`로 이어지고, 그것이 RLS 정책에 쓰이며,
같은 정책이 REST, Realtime, Storage에 똑같이 적용된다.

이 연결은 코드가 아니라 기본값과 관례의 형태로 존재한다.
역할 이름, 스키마 배치, 환경 변수 이름, 클라이언트가 헤더를 보내는 방식이
그렇다.
그래서 경쟁자가 같은 오픈소스 조각을 모아도 같은 경험을 재현하기 어렵다.
제품 원칙이 “새 표준이 나오면 우리 방식을 버리겠다”고 약속할 수 있는 것도,
가치가 개별 방식이 아니라 그것들을 맞물리게 한 설계에 있기 때문이다.

이 관점은 이식성 논쟁도 다르게 보게 한다.
데이터와 각 조각은 쉽게 떠날 수 있지만, 조각 사이의 약속은 떠나는 순간 직접
다시 써야 한다.
잠금 효과가 낮다는 주장과 전환 비용이 높다는 현실은 서로 모순되지 않는다.

### LAMP가 그랬듯 기본 조합이 되는 순간 선택의 기준이 바뀐다

홈페이지에 실린 후기 하나는 Supabase가 새 스타트업에게 “유망한 선택”에서
“표준”으로 아주 빨리 넘어갔다고 쓴다.
2000년대의 LAMP, 2010년대 초의 Rails와 Heroku 조합이 그랬듯,
기본 조합이 된 도구는 장단점을 따져서 고르는 대상에서 벗어나 고르지 않을
이유를 찾아야 하는 대상이 된다.

이 변화는 AI 코드 생성에서 더 강하게 일어난다.
에이전트는 학습 데이터와 예제가 가장 많은 조합을 고르고,
Lovable 같은 도구는 아예 백엔드를 Supabase로 고정한다.
사용자는 Supabase를 고른 적이 없는데 Supabase 위에서 앱을 운영하게 된다.

그때 중요한 것은 선택의 품질이 아니라 기본값의 품질이다.
Supabase가 자동 권한 부여를 없애는 방향으로 바꾸는 것은,
표준이 된 플랫폼이 감당해야 하는 책임이 무엇인지 보여 준다.
고르지 않은 사람에게도 안전해야 한다.

### 오픈소스 통합 플랫폼의 경계는 운영에서 그어진다

Supabase의 코드는 거의 전부 공개돼 있다.
그런데 자체 호스팅에서 빠지는 기능은 백업, 시점 복구, 브랜칭, 지표처럼
운영을 대신해 주는 것들이다.
이것은 GitLab이나 Sentry 같은 오픈 코어 회사의 경계와 다르다.
그들은 기능 자체를 유료 판에 남겼지만,
Supabase는 기능 대신 “그 기능을 안전하게 운영하는 일”을 플랫폼에 남겼다.

이 방식은 오픈소스 커뮤니티와 덜 부딪친다.
누구도 코드를 빼앗겼다고 느끼지 않기 때문이다.
대신 자체 호스팅을 고르는 팀은 공개된 코드만으로는 얻을 수 없는 운영 역량을
스스로 갖춰야 하고,
그 비용이 대부분의 팀을 다시 호스팅 플랫폼으로 이끈다.
코드의 개방성과 운영의 집중은 Supabase에서 모순이 아니라 하나의 사업 구조다.

그렇다고 공개된 코드가 장식은 아니다.
GeekNews 공개 베타 토픽에서 misolab은 예전에 parse.com도 있었지만 조용히 사라진
것 같다고 썼고,[^misolab]
xguru는 Parse가 페이스북에 인수된 뒤 서비스를 닫으면서 오픈소스로 떨어져
나왔다고 정리했다.[^xguru-parse]
BaaS 회사가 사라질 때 사용자에게 남는 것은 코드뿐이다.
자체 호스팅의 운영 비용이 평소에는 사람들을 플랫폼으로 이끌지만,
회사가 방향을 바꾸거나 사라지는 날에는 공개된 코드가 유일한 출구가 된다.

---

[^RNCTX]: <https://news.ycombinator.com/item?id=23321805>

[^kiwicopple-db]: <https://news.ycombinator.com/item?id=23321890>

[^pm90]: <https://news.ycombinator.com/item?id=23322272>

[^kiwicopple-realtime]: <https://news.ycombinator.com/item?id=23325509>

[^kiwicopple-notify]: <https://news.ycombinator.com/item?id=23321167>

[^kiwicopple-ux]: <https://news.ycombinator.com/item?id=23325709>

[^habosa]: <https://news.ycombinator.com/item?id=23322108>

[^kiwicopple-medical]: <https://news.ycombinator.com/item?id=23323083>

[^kiwicopple-lockin]: <https://news.ycombinator.com/item?id=23320443>

[^x_stealth]: <https://news.ycombinator.com/item?id=23324663>

[^kiwicopple-selfhost]: <https://news.ycombinator.com/item?id=23325951>

[^idoby]: <https://news.ycombinator.com/item?id=23320941>

[^kiwicopple-coupling]: <https://news.ycombinator.com/item?id=23321088>

[^InvOfSmallC]: <https://news.ycombinator.com/item?id=23320840>

[^bradyo]: <https://news.ycombinator.com/item?id=23324061>

[^zihado]: <https://news.hada.io/topic?id=3347#cid3819>

[^xguru]: <https://news.hada.io/topic?id=3347#cid3823>

[^awalias]: <https://news.hada.io/topic?id=3347#cid3825>

[^misolab]: <https://news.hada.io/topic?id=3347#cid3803>

[^xguru-parse]: <https://news.hada.io/topic?id=3347#cid3805>
