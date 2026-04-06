# pg_background - PostgreSQL 세션 밖에서 장기 쿼리 실행하기

> 원문: <https://vibhorkumar.wordpress.com/2026/02/16/pg_background-make-postgres-do-the-long-work-while-your-session-stays-light/>

## 요약

`pg_background`는 PostgreSQL 확장 모듈로, 클라이언트 세션과 독립된 서버 내부
백그라운드 워커 프로세스에서 SQL을 비동기로 실행한다. VACUUM, 대규모 데이터
수정, 집계 쿼리처럼 오래 걸리는 작업을 별도 큐 서비스 없이 DB 내부에서 분리할 수 있다.

v2 API는 PID 재사용으로 인한 핸들 보안 문제를 해결하기 위해 난수 쿠키를 도입했다.
결과는 `pg_background_result_v2`로 한 번만 소비 가능하며, 추적 해제(detach)와
작업 취소(cancel)는 의미가 다르다.

```sql
-- 백그라운드 작업 시작
SELECT * FROM pg_background_launch_v2(
  'SELECT pg_sleep(5); SELECT count(*) FROM large_table')
  AS handle;

-- 결과 조회
SELECT * FROM pg_background_result_v2(<pid>, <cookie>) AS (count BIGINT);
```

## 분석

기존 대안들과 비교하면 위치가 명확하다. `dblink`는 새 연결 오버헤드가 있고
인증·권한 설정이 복잡하다. 애플리케이션 레이어 비동기는 DB 외부에 상태 관리
복잡도가 생긴다. `pg_background`는 서버 내부에서 독립 트랜잭션으로 실행되어
리소스 격리가 보장된다.

실용적인 활용 사례:
- VACUUM/ANALYZE를 세션 블로킹 없이 실행
- 대규모 리포트 쿼리를 비동기로 돌리고 나중에 결과 수거
- 감사 로그 기록을 fire-and-forget으로 처리
- 인덱스 생성을 세션과 분리

운영상 주의점은 `max_worker_processes` 한도다. 백그라운드 작업이 이 값을 소비하므로
동시 백그라운드 작업 수를 설계 단계에서 고려해야 한다. v1.8+에서는 타임아웃,
워커 제한, 진행 상황 모니터링 기능이 추가됐다.

## 비평

`pg_background`는 "DB 내부에서 비동기"라는 매력적인 제안이지만, 결국 DB 서버가
작업 스케줄러 역할을 겸하게 된다. 장기 실행 작업이 많아지면 DB 서버의 워커 풀
경쟁이 생기고, 운영 관측성(어떤 작업이 실행 중인지)이 복잡해진다.

외부 큐(Sidekiq, Celery, Temporal 등)가 제공하는 재시도 정책, 우선순위 큐, 분산
실행 같은 기능은 `pg_background`에 없다. 단순한 "세션 분리" 수준의 요구에는
적합하지만, 복잡한 비동기 워크플로에는 여전히 전용 큐 시스템이 낫다.

## 인사이트

### PostgreSQL은 점점 애플리케이션 서버가 되고 있다

백그라운드 워커, 논리 복제,
pg_cron, pg_background 같은 확장들이 쌓이면서 Postgres는 단순 데이터 저장소를
넘어 스케줄링, 이벤트 처리, 비동기 작업까지 담당하게 됐다. 이 흐름은 아키텍처
단순화(외부 컴포넌트 축소)라는 장점과 DB 서버 복잡도 증가라는 트레이드오프를 동시에
가진다.

### "세션과 트랜잭션의 분리"는 DB 설계의 근본 패턴이다

클라이언트 연결 수명과
작업 수명을 일치시키는 전통적 모델은 장기 작업에서 항상 문제가 됐다. pg_background는
이 분리를 DB 내부에서 구현한 것이다. 클라우드 DB 서비스들이 서버리스 모델에서
연결과 컴퓨팅을 분리하는 방향과 맥이 닿는다.

### fire-and-forget 패턴의 숨은 비용은 관측성이다

감사 로그를 fire-and-forget으로
처리하면 세션 응답성은 좋아지지만, "작업이 실제로 실행됐는지"를 추적하기 어려워진다.
비동기 실행을 쓸 때마다 "이 작업이 실패하면 누가 감지하는가"라는 질문이 설계에
포함되어야 한다.
