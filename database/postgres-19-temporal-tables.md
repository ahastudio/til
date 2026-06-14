# PostgreSQL 19 — 템포럴 테이블, 드디어 네이티브 지원

원문: <https://www.pgedge.com/blog/looking-forward-to-postgres-19-its-about-time>

HN 토론: <https://news.ycombinator.com/item?id=48506372> (149점, 42개 댓글)

## 요약

pgEdge의 Shaun Thomas가 2026년 6월 12일에 작성한 글이다.
SQL:2011 표준이 템포럴(temporal) 기능을 도입한 지 10년이 훌쩍 넘었지만,
PostgreSQL은 줄곧 네이티브 지원을 미뤄왔다.
PostgreSQL 19에서 드디어 애플리케이션 타임(application-time) 기반 템포럴 테이블이 기본 기능으로 탑재된다.
범위 타입 컬럼, `WITHOUT OVERLAPS` 제약, `FOR PORTION OF` DML 절이 핵심이다.
다만 트랜잭션 타임(system-time) 지원은 이번 릴리스에 포함되지 않는다.

## 분석

### 템포럴 테이블이란

템포럴 테이블(temporal table)은 데이터가 “언제 유효했는가”를 행 단위로 추적하는 테이블이다.
일반 테이블은 현재 상태만 저장하지만,
템포럴 테이블은 각 행에 유효 기간을 붙여서 시간 축 위의 변화를 모두 보존한다.

SQL:2011 표준은 두 가지 시간 차원을 정의한다.

- **애플리케이션 타임(application-time, valid time)**: 비즈니스 현실에서 데이터가 유효한 기간.
  “이 계약은 2025-01-01부터 2025-12-31까지 유효하다”처럼 도메인 의미를 갖는다.
- **시스템 타임(system-time, transaction time)**: 데이터베이스가 그 사실을 알게 된 시점.
  “이 행이 2025-03-15 14:32에 삽입됐다”처럼 DB 내부 이력을 뜻한다.

두 차원을 모두 갖추면 바이템포럴(bitemporal) 테이블이 된다.
PostgreSQL 19는 애플리케이션 타임만 지원하므로 단일 템포럴(uni-temporal)이다.

### 범위 기반 저장

기존 접근 방식은 `valid_from`과 `valid_to`를 별도 컬럼으로 두는 것이었다.
두 컬럼의 조합으로 겹침을 막으려면 `btree_gist` 익스텐션의 GiST 배제 제약(exclusion constraint)을 써야 했다.

```sql
-- 기존 방식 (btree_gist 필요)
CREATE TABLE products (
    id          integer,
    valid_from  date,
    valid_to    date,
    price       numeric,
    EXCLUDE USING GIST (
        id WITH =,
        daterange(valid_from, valid_to) WITH &&
    )
);
```

PostgreSQL 19는 범위 타입 컬럼 하나로 유효 기간을 표현하고,
기본 키에 `WITHOUT OVERLAPS` 제약을 선언한다.

```sql
-- PostgreSQL 19 방식
CREATE TABLE products (
    id       integer,
    valid_at daterange,
    price    numeric,
    PRIMARY KEY (id, valid_at WITHOUT OVERLAPS)
);
```

`WITHOUT OVERLAPS`는 같은 `id`에 대해 `valid_at` 범위가 겹치는 행을 엔진 수준에서 차단한다.
GiST 익스텐션 없이도 인덱스 구조 안에서 오버랩 검사가 이뤄지는 것이 핵심이다.

### FOR PORTION OF 절

템포럴 DML의 가장 중요한 기능은 `FOR PORTION OF` 절이다.
특정 기간에 대해서만 행을 수정할 수 있고,
엔진이 범위를 자동으로 분할·병합한다.

```sql
UPDATE products
    FOR PORTION OF valid_at FROM '2025-03-01' TO '2025-09-01'
    SET price = 10.99
    WHERE id = 42;
```

이 구문은 내부적으로 다음을 자동 처리한다.

1. 기존 행의 유효 범위를 잘라내어 갱신 대상 구간을 분리한다.
2. 갱신된 구간에 새 가격을 적용한 행을 삽입한다.
3. 나머지 구간은 원래 값을 유지한 행으로 남겨둔다.

애플리케이션 코드에서 범위 분할 로직을 직접 구현할 필요가 없어진다.

munk-a는 "복잡한 비즈니스 로직이 얽혀 있을 때 날짜 범위 조작을 직접 관리하는 것이 얼마나 골치 아픈지"를 강조하며,
기간 제약이 서브 범위 조정 중 갭이 생기지 않도록 보장하는 데 탁월하다고 평했다.[^munk-a]
ris는 다른 각도에서 우려를 제기했다: `UPDATE`가 내부적으로 새 행을 추가한다는 점이 DBA의 통상적인 가정을 뒤흔든다는 것이다.[^ris]
이 동작은 명시적으로 이해하지 않으면 예상치 못한 테이블 크기 증가나 인덱스 동작으로 이어질 수 있다.

### 템포럴 외래 키

`PERIOD` 키워드로 외래 키에 시간 제약을 걸 수 있다.

```sql
CREATE TABLE order_items (
    order_id   integer,
    product_id integer,
    valid_at   daterange,
    FOREIGN KEY (product_id, PERIOD valid_at)
        REFERENCES products (id, PERIOD valid_at)
);
```

참조되는 테이블(`products`)의 유효 기간이 참조하는 테이블(`order_items`)의 기간을 완전히 포함해야 한다.
“주문 항목이 존재하는 동안 상품도 존재해야 한다”는 시간적 참조 무결성을 DB가 직접 보장한다.

## 비평

### 왜 이렇게 오래 걸렸나

SQL:2011 표준이 나온 건 15년 전이다.
다른 주요 RDBMS들은 훨씬 빨리 움직였다.
SQL Server는 2016년부터 `SYSTEM_TIME` 기반 시스템 버전 테이블을 제공했고,
Oracle은 Workspace Manager로 복잡한 버전 관리를 지원해왔다.
MariaDB도 SQL Server 스타일의 시스템 버전 테이블을 일찌감치 도입했다.

HN에서 bhaak는 "2000년대에 Oracle 문서에서 이 기능을 처음 읽었고 실제 운영 환경에서 써보고 싶었는데,
Oracle을 쓰던 시절엔 결국 못 써봤다"고 회고했다.[^bhaak]
이 기능의 역사가 길다는 것, 그리고 실무 적용 기회가 얼마나 드물었는지를 잘 보여주는 증언이다.

PostgreSQL 커뮤니티가 늦어진 데는 몇 가지 이유가 있다.
범위 타입 지원, GiST 인덱스 구조, 기존 익스텐션 생태계(`btree_gist`, `pg_bitemporal`) 등
우회 수단이 이미 존재했기 때문에 네이티브 구현의 우선순위가 낮았다.
`pg_bitemporal`(Henrietta Dombrovskaya, Chad Slaughter)이 2015년부터 논의를 이어온 것이
표준화 작업에 기반 자료 역할을 했다는 점은 긍정적이다.

이번 기능을 직접 구현한 pjungwir는 HN에 등장해 "이 기능을 원하는 사람이 없다는 말을 자주 들었는데,
그래서 벤더들이 이렇게 느렸던 것 같다"고 밝혔다.[^pjungwir]
시스템 타임은 아직 없지만 직접 작업할 의향이 있다고 덧붙였으며,
SQL:2011을 넘어서는 확장 로드맵도 공유했다.
MBCook은 "GiST 인덱스와 날짜 범위로 10년 넘게 이 패턴을 써왔는데,
외래 키가 없어서 저장 프로시저로 입력·수정을 강제해야 했다"며 네이티브 지원을 반겼다.[^MBCook]

### 시스템 타임 부재의 의미

이번 릴리스에서 트랜잭션 타임이 빠진 것은 실질적 한계다.
시스템 타임 없이는 “DB가 언제 이 사실을 기록했는가”를 쿼리할 수 없다.
감사 추적(audit trail), 규제 컴플라이언스, 실수 복구 시나리오에서는
트랜잭션 타임이 종종 더 중요하다.

IgorPartola는 주(州) 판매세율 관리 시스템을 예로 들며 이 한계를 구체화했다.[^IgorPartola]
2026년 세율을 7.25%로 미리 입력해뒀는데 6월이 되어서야 1월 1일부터 7.35%였어야 한다는 것을 알게 된 경우,
“오늘 변경됐다”고 기록하는 것은 틀리고 “1월 1일부터 7.35%였다”고 소급해야 한다.
그러면서도 기존에 잘못된 세율로 발행된 인보이스들이 어떤 버전의 데이터를 참조했는지는 보존해야 한다.
이런 “버전 있는 애플리케이션 타임” 시나리오는 PostgreSQL 19의 단일 템포럴 지원만으로는 완전히 해결되지 않으며,
바이템포럴 접근이 필요하다.

현재로서는 트리거 기반 이력 테이블이나 `pg_audit`를 병행해야 한다.
완전한 바이템포럴 지원은 이후 릴리스를 기다려야 한다.

### 설계상 의문: 종료일이 꼭 필요한가

larsnystrom은 "시작일만 저장하면 범위 겹침이나 타임 트래블 문제가 제약 없이도 사라지는데 왜 기간을 저장하는가"라고 물었다.[^larsnystrom]
이에 throwaway7783는 "시작일만 있으면 현재 유효한 가격이 항상 존재한다고 가정해야 한다"고 답했다.[^throwaway7783]
종료일이 있으면 계절 상품처럼 특정 기간 이후 자동으로 비활성화되는 행을 자연스럽게 표현할 수 있다.
이 논쟁은 "범위 vs. 시작점" 모델링의 근본적 차이를 드러낸다.
명시적 종료일은 유연성을 높이는 대신 겹침 방지 제약이 필요하고, PostgreSQL 19의 `WITHOUT OVERLAPS`가 그 비용을 낮춘다.

### 성능: GiST 인덱스의 부담

fabian2k는 현재 행만 조회하는 일반적인 경우에 대한 성능 영향을 물었다.[^fabian2k]
수동 버전 관리에서는 현재 행 테이블과 아카이브 테이블을 분리해 성능을 보호하는 전략이 흔하다.
구현자 pjungwir의 답변에 따르면 애플리케이션 타임은 단일 테이블(파티셔닝은 가능)에 저장되며,
가장 큰 성능 부담은 B-Tree 대신 GiST 인덱스를 사용하는 데서 온다.[^pjungwir-perf]
그는 GiST 전반의 성능 개선을 TODO에 두고 있으며, PGConf.dev에서 다른 기여자들도 관련 패치를 준비 중임을 확인했다고 전했다.
시스템 타임 구현 시에는 별도 히스토리 테이블과 파티셔닝을 조합하는 벤더 방식이 참고 기준이 될 것이다.

### 다른 DB와의 비교

SQL Server의 `FOR SYSTEM_TIME AS OF` 구문은 특정 시점의 스냅숏 쿼리를 한 줄로 쓸 수 있다.
PostgreSQL 19는 애플리케이션 타임 쿼리에 범위 연산자(`@>`, `&&`)를 직접 써야 해서
SQL Server보다 표현력이 다소 낮다.
Oracle Workspace Manager는 버전 분기·병합까지 지원하는 훨씬 복잡한 모델인데,
PostgreSQL은 그런 수준을 목표로 삼고 있지 않다.
단순하고 표준 친화적인 구현에 집중한 선택은 합리적이다.

## 인사이트

### 애플리케이션 아키텍처의 변화

템포럴 테이블이 네이티브로 지원되면 “유효 기간 관리 코드”를 애플리케이션에서 DB로 내릴 수 있다.
지금까지 많은 팀이 `deleted_at`, `effective_from`, `effective_to` 컬럼을 손수 관리하며
범위 겹침 방지, 현재 행 조회 로직을 비즈니스 레이어에 직접 구현했다.
`FOR PORTION OF`와 `WITHOUT OVERLAPS`가 이 로직을 엔진으로 흡수하면
애플리케이션 코드가 단순해지고 버그 면적이 줄어든다.

### 감사 추적과의 관계

템포럴 테이블은 애플리케이션 타임 이력이고,
감사 추적(audit trail)은 트랜잭션 타임 이력이다.
두 개념은 다르다.

“계약이 언제부터 언제까지 유효했는가”는 템포럴 테이블이 다룬다.
“누가 언제 그 계약을 수정했는가”는 감사 로그가 다룬다.
PostgreSQL 19만으로는 후자를 충족할 수 없으므로,
규정 준수 요건이 있는 시스템은 여전히 별도 감사 메커니즘이 필요하다.

### 이벤트 소싱과의 비교

이벤트 소싱(event sourcing)은 상태 변화를 이벤트 스트림으로 저장하고
현재 상태를 재계산하는 패턴이다.
템포럴 테이블은 다른 관점을 취한다.
현재 상태를 직접 저장하되, 시간 축을 명시적으로 모델링한다.

이벤트 소싱은 감사 추적과 도메인 이벤트 발행에 강점이 있고,
템포럴 테이블은 시점 쿼리(point-in-time query)와 기간 기반 조인에 강점이 있다.
둘은 경쟁 관계가 아니라 보완 관계로 볼 수 있다.
복잡한 이력 요구사항을 가진 시스템이라면 두 패턴을 함께 쓰는 것도 유효한 선택이다.

### 실무 도입 사례

HN 댓글에서 다양한 실무 맥락이 제시됐다.
cherryteastain은 거래 시스템에서 체결 후 거래소가 정정 또는 취소 메시지를 보내오는 상황에 이 기능이 유용하다고 언급했다.[^cherryteastain]
mrinterweb은 1년 반 전에 의료 스케줄링 캘린더 애플리케이션을 만들면서 이 기능이 있었다면 훨씬 수월했을 것이라고 회고했다.[^mrinterweb]
반복적으로 등장하는 도메인은 요금·세율·가격 관리, 의료 일정, 금융 거래 정정 등이다.
이 모두는 "언제 유효했는가"를 정확히 모델링해야 하는 영역이다.

PostgreSQL 19의 네이티브 템포럴 지원은,
오랫동안 익스텐션과 우회 로직으로 버텨온 PostgreSQL 생태계에
드디어 표준 수준의 도구를 쥐여준다.
시스템 타임 부재라는 한계가 있지만,
애플리케이션 타임 관리만으로도 상당수 실무 요구사항을 커버할 수 있다.

---

[^pjungwir]: <https://news.ycombinator.com/item?id=48508750>
[^IgorPartola]: <https://news.ycombinator.com/item?id=48507599>
[^munk-a]: <https://news.ycombinator.com/item?id=48507218>
[^bhaak]: <https://news.ycombinator.com/item?id=48507311>
[^fabian2k]: <https://news.ycombinator.com/item?id=48508945>
[^pjungwir-perf]: <https://news.ycombinator.com/item?id=48509304>
[^ris]: <https://news.ycombinator.com/item?id=48508855>
[^MBCook]: <https://news.ycombinator.com/item?id=48508801>
[^larsnystrom]: <https://news.ycombinator.com/item?id=48507374>
[^throwaway7783]: <https://news.ycombinator.com/item?id=48507427>
[^cherryteastain]: <https://news.ycombinator.com/item?id=48507808>
[^mrinterweb]: <https://news.ycombinator.com/item?id=48509868>
