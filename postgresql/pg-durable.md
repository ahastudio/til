# pg_durable — PostgreSQL을 위한 내구성 SQL 함수

<https://github.com/microsoft/pg_durable>

HN 토론: <https://news.ycombinator.com/item?id=48414367> (380점, 87개 댓글)

## 소개

Microsoft가 오픈소스로 공개한 `pg_durable`은 PostgreSQL 안에서 장기 실행되는
내결함성(fault-tolerant) SQL 함수를 가능하게 하는 확장이다. “SQL로 워크플로를
정의하고, pg_durable이 각 단계를 체크포인트한 뒤, 크래시나 재시작, 실패한
단계 이후에도 재개한다”는 것이 핵심 약속이다.

Temporal 같은 외부 오케스트레이션 서비스나 Redis, 외부 큐 없이 PostgreSQL 내부에서
내구성 있는 실행(durable execution) 패턴을 구현한다. 모든 실행 상태가 PostgreSQL에
저장되므로 기존 백업 및 관찰 가능성(observability) 인프라를 그대로 활용할 수 있다.

## 주요 기능

- **내구성 있는 상태 지속**: 함수 실행 상태가 PostgreSQL에 저장되어 크래시와 재시작을
  견딘다
- **SQL 네이티브 설계**: `~>`, `|=>` 연산자를 사용하는 조합 가능한 SQL DSL로 워크플로를
  정의한다
- **데이터베이스 통합 프리미티브**: 스케줄링, 조건부 실행, 병렬 실행을 네이티브 지원한다
- **제로 외부 인프라**: PostgreSQL 확장으로만 동작하며 별도 서버가 필요 없다

## 사용법

```sql
SELECT df.start(
    'SELECT id FROM documents WHERE processed = false LIMIT 100' |=> 'batch'
    ~> 'UPDATE documents SET processed = true WHERE id = ANY($batch)'
);
```

내장 DSL의 `~>` 연산자는 단계 순차 실행을, `|=>` 연산자는 이전 단계 출력을
다음 단계 입력으로 바인딩한다.

대상 워크로드는 다음과 같다.

- 벡터 임베딩과 AI 파이프라인 (API 호출 및 배치 업서트 포함)
- 스테이징, 중복 제거, 변환 단계가 있는 데이터 수집
- 승인 워크플로가 있는 스케줄링된 유지보수 작업
- 독립적인 쿼리 결과를 합치는 병렬 집계

## 아키텍처

`pg_durable`은 PostgreSQL 백그라운드 워커로 실행되며 pgrx 프레임워크로 구축된다.
두 개의 내부 라이브러리에 의존한다.

- **duroxide**: 결정론적 재실행(replay)과 체크포인팅을 제공하는 오케스트레이션
  런타임
- **duroxide-pg**: 전용 스키마에 런타임 데이터를 저장하는 PostgreSQL 상태 제공자

PostgreSQL 17 이상, Rust nightly, cargo-pgrx 0.16.1이 필요하다. 현재 프리뷰
단계이며 736개의 GitHub 스타를 받았다.

## 분석

### 내구성 있는 실행의 데이터베이스 통합

Temporal, Apache Airflow 같은 외부 오케스트레이션 도구들은 워크플로 상태를
별도 저장소에 유지한다. `pg_durable`은 이 상태를 PostgreSQL 자체에 통합함으로써
운영 복잡성을 줄인다. 단일 백업으로 애플리케이션 데이터와 워크플로 상태가 함께
보존되고, 기존 PostgreSQL 모니터링 도구가 그대로 적용된다.

[GeekNews 댓글](https://news.hada.io/topic?id=30225)에서 공유된 해커뉴스 논의는
핵심 트레이드오프를 잘 보여준다. levkk[^levkk]는 “2026년은 Postgres 큐의 해”라고
선언하며 DBOS, pgQue 같은 유사 프로젝트들과의 비교를 이끌었다. 동시에 그는 솔직하게
인정한다. “앱 엔지니어 출신으로서 큐 로직은 코드에, Git에 있는 것을 선호한다.” 이것은
도구의 기술적 우수성과 팀의 실제 선호가 다를 수 있다는 현실적 관찰이다.

faxmeyourcode[^faxmeyourcode]는 더 직접적인 회의론을 표명한다. Apache Airflow 같은
DAG 스케줄러가 오래전에 해결한 문제를 왜 다시 데이터베이스 안에서 해결하려 하는가.
제어 흐름을 데이터베이스에 넣는 것이 낯설다는 반응이다. joelthelion[^joelthelion]은
스케일링 관점에서 같은 우려를 제기한다. “이미 가장 스케일하기 어려운 인프라에 장기
실행 작업까지 추가하려 한다.” Temporal과의 비교를 묻는 kilobaud[^kilobaud]의 질문은
이 프로젝트의 실질적 포지셔닝을 파악하려는 많은 개발자들의 관심을 대표한다.

### 비즈니스 로직의 위치 결정

저장 프로시저(stored procedure)에 대한 회의론은 오래되었다. 관찰 가능성, 테스트
가능성, 버전 관리의 어려움이 주요 비판이었다. `pg_durable`은 이 비판에 맞서
“올바르게 구현된 저장 프로시저는 탁월하다”는 입장을 취한다. 테스트와 버전 관리
문제는 도구의 문제가 아니라 실천의 문제라는 것이다.

## 비평

데이터베이스 스케일링의 어려움에 장기 실행 작업을 추가하는 것에 대한 우려는
타당하다. PostgreSQL은 OLTP 워크로드에 최적화되어 있으며, 장기 실행 트랜잭션은
잠금(lock)과 vacuum에 영향을 미칠 수 있다. `pg_durable`이 이런 경우를 어떻게
처리하는지는 프로덕션 채택 전에 면밀히 검토해야 할 사항이다.

프리뷰 단계라는 상태도 중요한 고려 사항이다. Microsoft의 오픈소스 프로젝트가
Azure PostgreSQL 환경에서 최우선적으로 지원될 가능성이 높지만, 온프레미스와
다른 클라우드 환경에서의 지원 수준은 불확실하다. TuringNYC[^TuringNYC]는 Azure에
묶인 기업 사용자 관점에서 이 우려를 현실적으로 표현한다. Azure PostgreSQL이
ParadeDB, 고차원 벡터 지원 등 최신 확장에서 경쟁자보다 뒤처진다는 구체적 불만이며,
pg_durable을 오픈소스로 공개하면서도 자사 서비스에서 먼저 지원하지 않는 것에 대한
아이러니를 지적한다. Azure 팀이 직접 응답한 것은 이 우려가 현실임을 시사한다.

## 인사이트

### PostgreSQL은 데이터베이스에서 플랫폼으로 진화하고 있다

pg_durable, pgvector, pg_cron, pg_partman 등 확장의 확산은 PostgreSQL이 단순한
관계형 데이터베이스를 넘어 범용 데이터 플랫폼으로 진화하고 있음을 보여준다.
오케스트레이션, 벡터 검색, 작업 스케줄링까지 PostgreSQL 안에서 처리 가능해지면,
애플리케이션 스택에서 필요한 외부 서비스의 수가 줄어든다. 이것은 운영 단순화의
기회이면서, 동시에 PostgreSQL에 대한 의존도 심화라는 위험이기도 하다.

### 코드와 데이터베이스 사이의 경계는 항상 협상 중이다

“비즈니스 로직은 애플리케이션 코드에 있어야 한다”는 원칙은 불변의 진리가 아니라
특정 시대의 합의다. 마이크로서비스가 서비스 경계를 재정의했듯, 데이터베이스 확장의
성숙은 로직의 위치 결정에 새로운 선택지를 추가한다. 중요한 것은 원칙을 교조적으로
따르는 것이 아니라 관찰 가능성, 테스트 가능성, 유지보수성이라는 실질적 기준으로
각 경우를 평가하는 것이다.

---

[^levkk]: <https://news.ycombinator.com/item?id=48414608>
[^faxmeyourcode]: <https://news.ycombinator.com/item?id=48414641>
[^joelthelion]: <https://news.ycombinator.com/item?id=48415637>
[^kilobaud]: <https://news.ycombinator.com/item?id=48414662>
[^TuringNYC]: <https://news.ycombinator.com/item?id=48415580>
