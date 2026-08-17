# PgBouncer 없이 Postgres를 쓰는 사람이 있는가

원문: [Does anyone run Postgres without PgBouncer?](https://brandur.org/fragments/postgres-without-pgbouncer)

HN 토론: <https://news.ycombinator.com/item?id=49277952> (144점, 94개 댓글)

## 요약

brandur는 10년 전에 쓴 Postgres 커넥션 관리 글이 지금도 거의 그대로 유효하다는 사실에서 출발한다.
Postgres는 여전히 많은 수의 연결을 잘 다루지 못하고, 그래서 애플리케이션 로컬 풀, 짧은 체크아웃, 그리고 PgBouncer 같은 외부 풀러가 여전히 권장된다.

그는 이 권장이 얼마나 보편적인지를 확인하려고 이름 있는 관리형 Postgres 제공자를 표로 정리했다.
Aiven, Alibaba RDS, Azure PG, ClickHouse Managed Postgres, Crunchy Bridge, DigitalOcean, EDB, Fly.io MPG, Google Cloud SQL, Heroku, Neon, PlanetScale, Railway, Render, Supabase, Tiger Cloud가 모두 PgBouncer 또는 그에 준하는 것을 제공한다.
AWS는 RDS Proxy라는 별도 관리형 프록시로, Supabase는 PgBouncer 또는 Supavisor로 대응한다.
풀러가 없는 곳은 IBM Cloud와 OCI 둘뿐이다.

여기서 글의 논지가 나온다.
사실상 모든 제공자가 번들로 넣어야 하는 기능이라면, 그것을 과연 비핵심(non-core) 기능이라고 부를 수 있는가.
그는 앞유리 없는 차를 파는 자동차 대리점에 비유한다.
도로 위 모든 차에 앞유리가 있고 없으면 위험하다는 걸 아는 상태에서, 앞유리를 다는 건 구매자 책임이라고 말하는 것은 형식적으로는 맞지만 화가 나는 일이라는 것이다.

낭비도 지적한다.
제공자마다 Postgres와 그 앞의 바운서를 어떻게 배치하고 어디서 찾을지에 대한 규약을 각자 만들어야 했다.
사용자마다 LISTEN/NOTIFY를 쓰지 말라는 식의 제약 문서와 풀링 모드별 트레이드오프를 따로 읽어야 한다.

결론은 재통합(reintegration)이다.
데이터베이스 URL 하나, 포트 하나, 추가 설정이나 주의사항 없는 세계가 가능하다는 것은 MySQL과 Mongo가 이미 증명했다.
프로세스 대 스레드라는 오래된 논쟁을 다시 열어야 하기 때문에 진척이 없지만, 지금까지 이 결함을 우회하는 데 들어간 개발자-연수를 생각하면 가능한 운영 개선 중 가장 영향이 큰 축에 속한다는 주장이다.

## 분석

### 표가 증명하는 것과 증명하지 않는 것

brandur의 표는 제공자의 지원 여부를 세었지, 사용자의 실제 사용 여부를 세지 않았다.
이 차이는 생각보다 크다.
AWS 항목은 RDS Proxy로 채워져 있지만, 실제로 대다수 RDS 인스턴스는 RDS Proxy를 쓰지 않는다.
가격이 만만치 않기 때문이다.[^chuckadams]

Neon에서 Postgres 프록시 계층을 담당하는 개발자도 PgBouncer는 전적으로 선택 사항이며 언제나 옳은 선택은 아니라고 말한다.
서버리스가 아닌 전통적인 애플리케이션이고 앱에서 커넥션 풀을 유지할 수 있다면 PgBouncer를 피하라고 권한다.
PgBouncer의 이점은 대부분 불규칙한 클라이언트 연결, 즉 연결이 너무 많거나 생성과 종료가 너무 잦은 상황에서 나오기 때문이다.[^conradludgate]

즉 표는 제공자 관점에서 "빠지면 곤란한 기본 옵션"임을 보여줄 뿐, 워크로드 관점에서 "항상 필요한 것"임을 보여주지는 않는다.
글은 전자를 근거로 후자를 암시하는 방향으로 읽히고, 토론의 상당 부분이 이 간극을 지적하는 데 쓰였다.

### 애플리케이션 풀과 외부 풀러는 다른 목적을 최적화한다

토론에서 가장 유용한 정리는 두 종류의 풀이 서로 다른 목표 함수를 갖는다는 지적이다.
대부분의 애플리케이션 커넥션 풀은 FIFO로 동작하며, 앱이 항상 쓸 연결을 확보하는 것, 즉 낮은 지연을 최적화한다.
문제는 앱이 모든 연결을 계속 따뜻하게 유지하기 때문에 남는 연결을 걷어낼 수단이 거의 없다는 점이다.
반대로 PgBouncer를 비롯한 소수의 외부 풀러는 LIFO로 동작하며, Postgres에 도달하는 연결 수를 줄여 처리량을 올리는 것을 최적화한다.
마지막에 쓴 연결을 먼저 다시 쓰면 나머지는 자연히 식어서 닫힌다.[^giovannibonetti]

이 구분은 "앱에 풀이 있으니 PgBouncer는 중복"이라는 흔한 반론이 왜 절반만 맞는지를 설명한다.
앱 인스턴스가 하나이거나 몇 개라면 앱 풀만으로 충분하다.
그러나 인스턴스가 늘어나면 연결은 인스턴스 수만큼 곱해진다.
클라이언트 측 풀링은 좋은 아이디어이지만 서비스를 수평 확장하는 순간 연결 한도가 빠르게 올라가고, 그때 PgBouncer로 다중화하게 된다는 실무 증언이 이 경로를 그대로 보여준다.[^reezer]

쿠버네티스 환경의 사례는 더 구체적이다.
파드 20~30개가 하나의 Postgres 인스턴스에 붙고 각 파드가 수백 개의 동시 요청을 처리하는 구성에서, 파드가 풀 연결을 몇 초 이상 붙들고 있으면 Postgres 프로세스 수와 메모리 사용량, 프로세스 교체가 모두 불어난다.
풀 TTL을 짧게 잡아 유휴 연결을 빨리 회수하는 식으로 완화하지만, 어떤 파드가 쓰지 않는 유휴 연결을 다른 파드가 가져다 쓸 수는 없다.
공유 풀러는 바로 이 낭비를 없앤다.[^atombender]

### 언어와 런타임이 만드는 비대칭

같은 논점이 언어별 경험 차이로도 나타난다.
Python에서는 애플리케이션이 커지면 프로세스와 배포 단위가 늘어나기 때문에 외부 풀러가 사실상 필수가 되고, Java에서는 꽤 큰 앱에서도 필요를 느낀 적이 없다는 증언이 있다.
로컬에서 커넥션 풀을 공유하기가 훨씬 쉽기 때문에 전체 앱을 통틀어도 개별 연결 수가 많지 않다는 것이다.[^matsemann]

이 차이의 뿌리는 GIL이다.
Python 앱은 보통 여러 프로세스를 띄워서 확장하고, Java는 스레드를 늘려서 확장한다.
Python 프로세스들끼리는 스레드 풀을 공유할 수 없지만 Java는 할 수 있다.[^atomicnumber3]

다만 이 구분을 언어로 환원하는 건 지나치다는 반론도 나왔다.
언어가 아니라 사용 패턴이 제약을 만든다는 것이다.
어떤 언어로도 짧은 트랜잭션을 많이 돌리는 앱을 만들 수 있고, 크고 오래 잡는 트랜잭션을 만들 수도 있다.
전자는 PgBouncer가 트랜잭션을 인터리빙할 수 있어 잘 맞고, 후자는 3분짜리 BEGIN...COMMIT에 대해 PgBouncer가 할 수 있는 게 없다.[^tyre-lang]

### 프로세스 대 스레드라는 프레이밍이 정확한가

원문은 재통합을 가로막는 요인으로 프로세스 대 스레드 논쟁을 든다.
Lobsters 쪽에서는 이 프레이밍 자체가 초점을 벗어났다는 반박이 나왔다.
Linux에서 스레드와 프로세스는 스케줄링 관점에서 본질적으로 같으며, 진짜 문제는 PostgreSQL이 다중화(multiplexing)를 지원하지 않는다는 점이라는 것이다.
동시 요청을 여러 개 보내려고 연결을 여러 개 열어야 하는 구조 자체가 문제이지, 연결당 무엇을 만드느냐가 문제가 아니다.[^dprkh]

이 지적은 커널 수준의 설명으로 보강됐다.
Linux 스케줄러는 프로세스가 아니라 스레드를 스케줄링한다.
프로세스의 큰 오버헤드는 생성 시점에 있다.
프로세스는 자기 페이지 테이블, 자기 메모리, 자기 파일 디스크립터 집합을 갖고, 이것들을 모두 세팅해야 하며 RAM을 소모한다.
스케줄링 자체에는 영향이 없다.
다만 프로세스 간 전환은 페이지 테이블 교체를 수반하고 이는 TLB 교란을 일으키므로, 스레드 간 전환과 완전히 같지는 않다.[^chisnall]

문제를 이렇게 다시 세우면 처방이 달라진다.
스레드 모델로 갈아타는 것이 아니라 하나의 연결에서 동시 요청을 처리할 수 있게 하는 것이 목표가 된다.
libuv와 io_uring의 시대에 문제는 "무엇"-per-connection이 아니라 "per-connection" 부분이라는 요약이 이 관점을 압축한다.[^viraptor]

## 비평

### 표의 단위가 주장의 단위와 맞지 않는다

글의 핵심 논증은 "100퍼센트의 제공자가 번들한다 → 따라서 코어 기능이다"이다.
그런데 이 추론의 전제는 제공자 카탈로그이고 결론은 Postgres 코어 설계다.
관리형 제공자가 어떤 옵션을 제공하는지는 그 제공자가 어떤 고객군을 상대하는지의 함수이지, Postgres 사용자 전체 분포의 함수가 아니다.

토론에서도 이 점이 정확히 지적됐다.
관리형 클라우드 호스팅 바깥의 압도적 다수 PostgreSQL 사용자는 PgBouncer를 쓰지 않으며, 이 글은 사실상 상업용 클라우드 관리형 서비스에 대해 이야기하고 있다는 것이다.
그런 서비스가 커넥션 풀링을 지원해야 하고 당연히 PgBouncer를 쓰리라는 건 논쟁거리도 아니다.[^zzzeek]

제공자가 모든 옵션을 미리 켜두는 이유는 규모가 커진 사용자를 위한 준비를 처음부터 갖춰 지원 비용을 줄이기 위해서라는 해석이 더 자연스럽다.[^kronislv]
이 해석 아래에서 표는 "모두에게 필요하다"가 아니라 "누구에게 필요해질지 모른다"의 증거가 된다.
전자여야 앞유리 비유가 성립하는데, 표가 지지하는 것은 후자다.

### 앞유리 비유가 감추는 비용

앞유리는 달면 손해가 없다.
PgBouncer는 그렇지 않다.
트랜잭션 풀링 모드는 하나의 클라이언트 연결이 하나의 Postgres 백엔드 세션이라는 가정을 깨뜨리며, 이 때문에 여러 세션 범위 기능이 정상 동작하지 않는다.[^rootparent]

이 비용은 추상적인 게 아니다.
SET 문은 세션 범위인데 트랜잭션 모드에서는 트랜잭션 사이에 세션이 재배정되므로, 새벽 2시에 정체불명의 search_path 버그를 쫓기 전까지는 놓치기 쉽다.
psycopg3는 이제 기본으로 prepared statement를 준비하는데, 명시적으로 끄지 않으면 트랜잭션 모드에서 깨진다.[^saadyousfi]
SQLAlchemy 쪽에서도 트랜잭션 수준 풀링과 prepared statement 캐시의 상호작용은 오래 반복돼 온 악몽이라고 표현한다.[^zzzeek]

제공자 내부에서 본 통계는 더 결정적이다.
표에 오른 제공자 중 한 곳에서 일하는 사람에 따르면, 데이터베이스 티켓의 단일 최대 원인은 압도적으로 PgBouncer 연결에 적합하지 않은 워크로드를 PgBouncer 연결로 돌리는 고객이다.[^opboot]
구체적으로는 search_path를 설정하는 자동화 스크립트, 특정 상황에서 트랜잭션 모드를 읽기 전용으로 바꾸는 Prisma 같은 프레임워크, pg_dump, 같은 롤로 로그인하는 개별 사용자들에게 동일한 PgBouncer 연결 문자열을 나눠주는 경우, 그리고 SET을 쓰는 사실상 모든 것이다.[^opboot2]

앞유리를 달았더니 시야가 왜곡되고 정비 매뉴얼을 따로 읽어야 하는 상황이라면, 비유는 논증이 아니라 수사가 된다.
실제로 프로덕션 장애 때 PgBouncer가 짧아야 할 트랜잭션을 몇 시간씩 열어둔 채로 잡고 있어서 이를 걷어냈고, 그 뒤 몇 년간 맨 PostgreSQL로 문제없이 운영 중이라는 사례도 있다.[^duncan]

### 없어도 되는 경우를 배제하는 방식

원문 제목은 수사적 질문이지만, 토론은 이를 진지한 질문으로 되받았고 답은 대체로 긍정이었다.
연결이 30개 남짓이고 마이그레이션용 여유만 있으면 되는 규모에서 커넥션 매니저가 필요했던 적이 없다는 응답,[^manfred]
앱 서버 5대에 각 40연결로 약 200개의 백엔드를 클라이언트 측 풀링으로 잘 굴린다는 응답[^mandeep]이 대표적이다.

반대편에서는 질문 자체를 다시 써야 한다는 제안이 나왔다.
"비자명한 워크로드에서 PgBouncer 없이 Postgres를 운영하는 사람이 있는가"로 한정해야 흥미로운 답이 나온다는 것이다.
프로세스-per-connection 구조 때문에 작은 연결 폭주(connection storm)만으로도 서버가 망가지기 때문이다.[^petcat]
그런데 여기에 다시 반론이 붙는다.
모든 비자명한 워크로드가 웹 스케일인 것은 아니며, 동시 사용자가 수백에서 수천 명이고 연결이 스스로 풀링을 처리하는 몇 대의 두꺼운 Spring Boot 서버에서 오는 온프레미스 애플리케이션이 많다는 것이다.[^mrighele]

원문은 이 스펙트럼을 다루지 않는다.
필요 여부를 워크로드 축에서 논하지 않고 제공자 축에서만 논했기 때문에, 필요 없는 다수가 논증에서 통째로 빠진다.

### 사실관계와 자기모순

Supabase의 Supavisor를 독자 개발(proprietary) 풀러라고 적은 부분은 정확하지 않다.
proprietary가 비공개 소스를 뜻한다면 Supavisor는 공개 저장소가 있는 오픈소스다.[^edgurgel]

더 뼈아픈 건 IBM과 Oracle을 자기 존중이 있는 사람이라면 쓰지 않을 서비스라고 일축한 대목이다.
이 문장은 표에서 예외 두 개를 지우는 데 쓰였는데, 하필 그 예외 중 하나가 원문이 원하는 것을 이미 구현하고 있다.
Oracle 클라우드는 서버 측 커넥션 풀링, 클라이언트 측 로드 밸런싱, 수평 확장을 지원해서 저자가 원하는 "그냥 동작하는 URL 하나"를 제공한다는 반박이 나왔다.
Postgres가 10년간 나아지지 않았다고 말하면서, 그가 지적한 문제를 모두 해결한 데이터베이스는 자기 존중이 있는 사람이 쓰지 않는다고 동시에 말하는 셈이다.[^mikehearn]
IBM Cloud와 OCI를 고르는 정당한 엔지니어링 이유도 존재한다는 지적도 함께 나왔다.[^solatic]

수사적 처리로 지운 두 칸이 실은 논증의 반례였다는 점에서, 이 문장은 스타일 문제가 아니라 논증 결함이다.

## 인사이트

### 필요 판단의 축은 규모가 아니라 연결의 변동성이다

이 토론에서 반복적으로 확인되는 것은 절대 연결 수보다 연결의 성격이 판단 기준이라는 점이다.
연결이 너무 많거나, 생성과 종료가 너무 잦을 때 외부 풀러의 이점이 나온다.[^conradludgate]
서버리스는 이 두 조건을 동시에 만족한다.
지속 프로세스가 없으니 지속 풀도 없고, 그래서 전용 풀러가 제 몫을 하기 시작한다.
반대로 지속적인 서버 프로세스와 앱 내부 풀이 있는 앱에서 외부 바운서는 대체로 형식적 절차에 가깝다.[^saadyousfi]

이 기준을 쓰면 체크리스트가 단순해진다.
앱 인스턴스 수가 고정적이고 각자 풀을 유지하며 `max_workers * pool_size < max_connections`가 성립하면 외부 풀러는 필요 없다.[^frollogaston]
인스턴스 수가 오토스케일링으로 변동하거나, 배포마다 프로세스가 갈아엎히거나, 요청 단위로 프로세스가 생겼다 사라지면 필요해진다.

주의할 함정도 있다.
필요 없어야 할 사용 사례인데 다른 무언가가 잘못 설정돼 있어서 필요하다고 착각하는 경우다.
FastAPI가 HTTP 핸들러에 트랜잭션을 의존성 주입하도록 권장하는 패턴은 모든 연결을 묶어두고 idle in transaction을 양산한다.
PgBouncer를 쓸 정당한 이유는 있지만 이것은 그런 이유가 아니다.[^frollogaston]

### 풀러는 대기 지점을 옮길 뿐 용량을 만들지 않는다

PgBouncer를 은탄환으로 다루면 반드시 실망한다.
오래 도는 트랜잭션에는 할 수 있는 일이 거의 없다.
PgBouncer 풀을 1000으로, Postgres 풀을 100으로 잡을 수는 있지만, 그것은 "지금은 요청을 처리할 수 없습니다"라고 말할 주체를 옮기는 것일 뿐이다.[^tyre-limit]

이 관점을 위로 확장하면 더 불편한 결론이 나온다.
요청마다 스레드를 배정하는 시스템에서는 PgBouncer가 있어도 결국 연결을 기다리며 줄을 서게 된다.
IO 위주 애플리케이션 서버는 부하에 맞춰 인스턴스를 늘렸기 때문에 스레드들이 DB 연결을 기다리며 대기할 뿐이고, 그 대기는 웹 서버 레벨에서 처리할 수도 있었다.
그런 의미에서 PgBouncer는 상류 문제에 붙인 덕트 테이프인 경우가 많다.[^sandeepkd]

실무적 함의는 명확하다.
풀러를 넣기 전에 트랜잭션 길이 분포와 유휴 트랜잭션 비율을 먼저 봐야 한다.
그 분포가 나쁘면 풀러는 병목을 감출 뿐 없애지 못한다.

### 원문의 질문은 유효하지만 답은 코어 통합이 아닐 수도 있다

"모두가 필요로 하는데 왜 코어가 아닌가"라는 재구성은 토론에서도 가장 널리 동의를 얻었다.
사람들이 Postgres를 PgBouncer 없이 쓴다는 건 자명하니, 질문은 왜 커넥션 풀링이 Postgres 기본 제공이 아닌지가 되어야 한다는 것이다.[^mbreese]
거의 모두가 쓴다면 별도 컴포넌트가 아니라 내장 기능이어야 하고, 그런 긴밀한 통합은 전체 복잡도를 오히려 낮출 것이라는 논리다.[^kronislv]

실제로 상황은 그 방향으로 조금씩 움직이고 있다.
PgBouncer가 트랜잭션 모드에서의 prepared statement 지원이라는 역사적 최대 난점을 해소하면서, 어떤 관리형 제공자에서는 고객들이 대부분의 사용 사례에서 기본으로 PgBouncer 연결 문자열을 쓰고도 문제를 겪지 않는 상황이 늘고 있다.
몇 년 전만 해도 그렇지 않았다.
PgBouncer는 충분히 검증됐고 놀라울 정도로 설정 가능하며, 피어드 구성으로 멀티스레드처럼 굴릴 수도 있다.[^saisrirampur]

다만 코어 통합이 유일한 답은 아니다.
연결 수 자체를 줄이는 대신 하나의 연결에서 동시 요청을 처리하는 다중화가 더 근본적인 처방이라는 관점이 있고,[^dprkh]
드라이버 계층에서 풀링과 페일오버를 함께 처리해 세션 의미론을 깨지 않는 상용 접근도 존재한다.[^rootparent]
어느 쪽이든 공통점은 PgBouncer를 그대로 코어에 넣는 것이 아니라, PgBouncer가 트랜잭션 풀링으로 지불한 대가를 지불하지 않는 설계를 찾는 것이다.

### 사용자 입장에서 지금 할 일

PgBouncer를 쓴다면 모드별 함정을 문서가 아니라 코드 리뷰 항목으로 옮겨야 한다.
`SET`, `LISTEN`/`NOTIFY`, 세션 수준 어드바이저리 락, 임시 테이블, 드라이버의 자동 prepared statement가 트랜잭션 모드에서 어떻게 되는지를 팀 규약으로 명문화하는 것이 사고를 줄이는 가장 싼 방법이다.

```ini
[pgbouncer]
pool_mode = transaction
server_reset_query = DISCARD ALL
max_client_conn = 2000
default_pool_size = 20
```

풀러를 대규모로 운영하며 직접 기여하는 쪽에서는, 하지 말라는 식의 일괄 권고보다 워크로드별 판단이 낫다고 말한다.
배치 처리도 전용 풀을 워크로드에 맞게 튜닝하면 PgBouncer를 통과시켜 유용하게 쓸 수 있고, 세션 특화 기능도 `DISCARD ALL` 같은 리셋 쿼리를 활용하면 기능 단위로 트랜잭션 풀링 모드에서 다룰 여지가 있다는 것이다.[^brian]

반대로 PgBouncer를 쓰지 않기로 했다면, 그 선택은 지금의 연결 패턴에 대한 것이지 영구적인 것이 아니다.
연결 한도에 부딪히기 전까지는 필요 없다가, 벽에 부딪힌 뒤 트랜잭션 모드로 돌린 PgBouncer가 꽤 빠르게 해결해 줬다는 경험담이 이 전환의 전형이다.[^seabre]
전환 시점을 미리 정해두는 것, 즉 `max_connections` 대비 사용률과 백엔드 프로세스 메모리 합을 알람으로 걸어두는 것이 사후 대응보다 낫다.

관련 문서로 [커넥션 풀의 기본과 함정](../database/connection-pool-basics-and-pitfalls.md),
[PgBouncer 처리량 4배 확장](pgbouncer-fleet-4x-throughput.md),
[데이터베이스는 이런 용도로 설계되지 않았다](../database/defensive-databases.md)를 함께 보면 좋다.

[^chuckadams]: chuckadams, <https://news.ycombinator.com/item?id=49320226>
[^conradludgate]: conradludgate, <https://news.ycombinator.com/item?id=49320310>
[^giovannibonetti]: giovannibonetti, <https://news.ycombinator.com/item?id=49321051>
[^reezer]: reezer, <https://lobste.rs/c/33bw46>
[^atombender]: atombender, <https://news.ycombinator.com/item?id=49321473>
[^matsemann]: matsemann, <https://news.ycombinator.com/item?id=49320397>
[^atomicnumber3]: atomicnumber3, <https://news.ycombinator.com/item?id=49320909>
[^tyre-lang]: tyre, <https://news.ycombinator.com/item?id=49320818>
[^dprkh]: dprkh, <https://lobste.rs/c/5jnrnv>
[^chisnall]: david_chisnall, <https://lobste.rs/c/f240c2>
[^viraptor]: viraptor, <https://lobste.rs/c/f0fq5c>
[^zzzeek]: zzzeek, <https://news.ycombinator.com/item?id=49320295>
[^kronislv]: KronisLV, <https://news.ycombinator.com/item?id=49321975>
[^rootparent]: root-parent, <https://news.ycombinator.com/item?id=49320460>
[^saadyousfi]: saadyousfi, <https://news.ycombinator.com/item?id=49320979>
[^opboot]: OPBoot, <https://lobste.rs/c/6k51ap>
[^opboot2]: OPBoot, <https://lobste.rs/c/0ivckx>
[^duncan]: duncan_bayne, <https://lobste.rs/c/o26tnk>
[^manfred]: manfred, <https://lobste.rs/c/e85xnq>
[^mandeep]: mandeep, <https://lobste.rs/c/kx0x3j>
[^petcat]: petcat, <https://news.ycombinator.com/item?id=49320413>
[^mrighele]: mrighele, <https://news.ycombinator.com/item?id=49321945>
[^edgurgel]: edgurgel, <https://lobste.rs/c/nvcvbl>
[^mikehearn]: mike_hearn, <https://news.ycombinator.com/item?id=49321389>
[^solatic]: solatic, <https://news.ycombinator.com/item?id=49320956>
[^frollogaston]: frollogaston, <https://news.ycombinator.com/item?id=49321082>
[^tyre-limit]: tyre, <https://news.ycombinator.com/item?id=49320896>
[^sandeepkd]: sandeepkd, <https://news.ycombinator.com/item?id=49326331>
[^mbreese]: mbreese, <https://news.ycombinator.com/item?id=49320672>
[^saisrirampur]: saisrirampur, <https://news.ycombinator.com/item?id=49322111>
[^brian]: brian, <https://lobste.rs/c/txc9db>
[^seabre]: seabre, <https://lobste.rs/c/7dfejs>
