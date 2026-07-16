# Noisia — PostgreSQL 유해 워크로드 생성기

<https://github.com/lesovsky/noisia>

HN 토론: <https://news.ycombinator.com/item?id=23731360> (135점, 7개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/y0thmw/noisia_harmful_workload_generator_for>

## 소개

Noisia는 PostgreSQL에서 발생할 수 있는 다양한 성능 문제 상황을
의도적으로 재현하는 부하 생성 도구다.
Go로 작성됐고 BSD-3-Clause 라이선스를 따르며, 2020년 6월에 시작해
2026년 현재까지 꾸준히 업데이트되고 있다.
저장소 설명은 스스로를 “harmful workload generator”라 부르며,
“테스트 목적으로만 사용하라”는 경고를 README 최상단에 굵은 글씨로
배치한다.

## 지원 워크로드

Noisia는 열 가지가 넘는 서로 다른 장애 시나리오를 각각 독립된
워크로드로 제공한다.

- **idle transactions** — 활성 상태의 트랜잭션이 아무 작업도 하지
  않은 채 핫라이트 테이블 위에 오래 머무르게 만든다.
- **rollbacks** — 일부러 잘못된 쿼리를 실행해 오류를 유발하고
  롤백 카운터를 증가시킨다.
- **waiting transactions** — 하나의 세션이 `ACCESS EXCLUSIVE` 잠금을
  쥔 채 순환하는 동안, 속도 제한이 걸린 매니저가 `--wait-xacts.waiters`
  옵션만큼 별도 연결을 열어 각각 그 잠금에 걸리게 만든다.
  대기 세션 수를 무제한(`--wait-xacts.waiters=0`)으로 두면 `max_connections`가
  소진될 때까지 계속 쌓여, 새 클라이언트는 `FATAL: sorry, too many
  clients already` 오류를 받게 된다.
- **deadlocks** — 여러 트랜잭션이 서로 상대방이 원하는 잠금을 쥐고
  있는 교착 상태를 동시에 만들어낸다.
- **temporary files** — 기본 설정 서버에서 `work_mem`보다 큰 시드
  데이터셋을 정렬하는 쿼리를 실행해 디스크 임시 파일 스필을
  유발한다. `work_mem`을 역할·데이터베이스 단위로 올리면 같은
  쿼리가 메모리 안에서 끝나 스필이 사라지는 것을 그대로 시연할
  수 있다.
- **terminate backends** — `pg_terminate_backend()`와
  `pg_cancel_backend()`로 무작위 백엔드나 쿼리를 강제 종료한다.
- **failed connections** — 사용 가능한 연결을 모두 소진시켜 다른
  클라이언트가 PostgreSQL에 접속하지 못하게 만든다.
- **fork connections** — 짧은 쿼리 하나를 위해 매번 전용 연결을
  새로 만들어, PostgreSQL 백엔드 프로세스가 과도하게 포크되게
  한다.
- **backend-killer** — 단일 세션이 prepared statement를 계속
  누적시켜 플랜 캐시를 불려 백엔드 메모리를 OOM-kill이 인스턴스
  전체를 재시작할 때까지 부풀린다. `--backend-killer.plan-size`를
  아주 크게 잡으면 각 `PREPARE` 자체가 무겁고 느려진다.
- **slot-bloat** — 소비되지 않는 물리 복제 슬롯 하나가 WAL을 붙들어
  `pg_wal`이 무한정 커지다가 디스크가 가득 차 인스턴스가 PANIC
  상태에 빠지게 만든다. 데이터 자체는 늘지 않고 체크포인트도
  계속 도는데 디스크만 채워진다.
- **wal-flood** — 여러 병렬 `UPDATE`-처리 워커(`--jobs`)가 원시
  쓰기 속도로 프라이머리의 WAL을 범람시켜 복제 지연을 만들고,
  재활용·아카이빙이 따라가지 못하면 `pg_wal`이 디스크 가득 참
  쪽으로 자란다. slot-bloat와 짝을 이루는, 눈에 보이는 활동을
  동반하는 버전이다.
- **bloat-churn** — 여러 병렬 `UPDATE`-처리 워커가 여전히 켜져
  있는 autovacuum을 속도로 앞질러, 인덱스가 걸린
  `updated_at = now()` 갱신으로 HOT 최적화를 깨뜨려 힙과 인덱스를
  함께 부풀린다. 손대지 않은 테이블 꼬리 부분이 `VACUUM`의 파일
  절단을 막는다. noisia를 멈추면 `VACUUM FULL`, `pg_repack`,
  `REINDEX CONCURRENTLY`로 복구 가능한, 속도 기반 공격의
  “치유 가능한” 버전이다.

각 워크로드는 고유한 CLI 플래그를 지원하며, 전체 옵션은
`noisia --help`로 확인할 수 있다.

## 설치와 사용법

[릴리스 페이지](https://github.com/lesovsky/noisia/releases)에서
바이너리를 내려받거나 Docker 이미지를 쓸 수 있다.

```bash
docker pull lesovsky/noisia:latest
docker run --rm -ti lesovsky/noisia:latest noisia --help
```

Go 코드에 라이브러리로 직접 임포트해 특정 워크로드만 골라 쓸 수도
있다.
이 경우 무한 실행을 막기 위해 반드시 컨텍스트를 함께 사용하라고
안내한다.

```go
package main

import (
	"context"
	"fmt"
	"github.com/lesovsky/noisia/waitxacts"
	"github.com/rs/zerolog"
	"log"
	"os"
	"time"
)

func main() {
	config := waitxacts.Config{
		Conninfo:       "host=127.0.0.1",
		Waiters:        10,
		WaitersRate:    1,
		ReportInterval: 1 * time.Second,
		LocktimeMin:    5 * time.Second,
		LocktimeMax:    20 * time.Second,
	}

	logger := zerolog.New(zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}).Level(zerolog.InfoLevel).With().Timestamp().Logger()

	ctx, cancel := context.WithTimeout(context.Background(), 4*time.Second)
	defer cancel()

	w, err := waitxacts.NewWorkload(config, logger)
	if err != nil {
		log.Panicln(err)
	}

	err = w.Run(ctx)
	if err != nil {
		fmt.Println(err)
	}
}
```

## 워크로드별 영향도 표

README는 각 워크로드가 이미 실행 중인 다른 애플리케이션에 실제로
피해를 주는지를 별도 표로 명시한다.
`deadlocks`와 `rollbacks`는 영향 없음으로 표시되지만, 나머지
대부분은 연결 소진, 백엔드 강제 종료, 테이블·인덱스 블로트, 디스크
가득 참으로 인한 인스턴스 PANIC 등 실제 운영 환경에 재현 가능한
피해를 명시적으로 경고한다.

## 문서화된 데모와 튜닝 가이드

`backend-killer`, `slot-bloat`, `wal-flood`, `bloat-churn`,
`tempfiles`, `waitxacts` 여섯 워크로드는 각각 `docs/workloads/`
아래 전용 가이드를 갖추고 있다.
각 가이드는 재현 가능한 스탠드를 구성하는 방법, 부하 강도를
조절하는 방법, 자체 리포트를 읽는 방법, 사후 복구 방법을 함께
다룬다.

## 분석

### 이 도구는 “장애를 만드는 도구”가 아니라 “장애를 관찰 가능하게 만드는 도구”다

Noisia의 진짜 가치는 장애를 일으키는 능력 자체가 아니라, 그 장애를
재현 가능하고 관찰 가능한 형태로 패키징했다는 데 있다.
`temp files` 워크로드가 `work_mem`을 늘리면 스필이 사라지는
“해결 시연”까지 포함하는 것이나, `bloat-churn`이 noisia를 멈춘
뒤 `VACUUM FULL`로 복구되는 과정을 문서화한 것은, 단순히 문제를
일으키는 데서 그치지 않고 “문제 → 관찰 → 해결”이라는 학습
루프를 완성하려는 의도를 보여준다.

일반적인 카오스 엔지니어링 도구(예: Chaos Monkey류)가 “무작위로
무언가를 죽인다”는 데 초점을 맞춘다면, Noisia는 PostgreSQL이라는
단일 시스템의 내부 메커니즘(WAL, 복제 슬롯, autovacuum, 잠금
관리자, 플랜 캐시)을 정확히 겨냥한 시나리오를 설계했다.
이는 범용 카오스 도구보다 훨씬 좁지만 훨씬 깊은 전문성을
요구하며, 동시에 그만큼 특정 데이터베이스 엔진에 대한 깊은
이해에서만 나올 수 있는 도구라는 뜻이다.
HN에서도 anticristi가 이 도구를 정확히 “ACID 데이터베이스를 위한
Chaos Monkey”라 부르며, 프로덕션 잠금 사고를 유발하는 코드 배포나
수동 데이터 수정을 아예 방지하는 방향으로 대화를 이끌어줬으면
좋겠다는 기대를 남겼다.[^anticristi]

### 워크로드 목록 자체가 PostgreSQL 운영자의 공포 지도다

열거된 14가지 워크로드는 무작위로 고른 것이 아니라, PostgreSQL
운영 경험이 있는 사람이라면 실제로 겪어봤을 법한 장애 유형을
정확히 짚고 있다.
`slot-bloat`(잊혀진 복제 슬롯이 디스크를 채우는 사고), `bloat-churn`
(autovacuum이 못 따라가는 상황), `backend-killer`(prepared
statement 누적으로 인한 OOM)는 모두 PostgreSQL 운영자 커뮤니티에서
반복적으로 보고되는 실제 장애 패턴이다.

이 목록은 그 자체로 “PostgreSQL을 운영할 때 실제로 무엇이
잘못될 수 있는가”에 대한 암묵지를 코드로 정리한 카탈로그
역할을 한다.
저자가 각 워크로드마다 원인이 되는 정확한 내부 메커니즘(HOT
최적화 붕괴, WAL 재활용 실패, 플랜 캐시 팽창)을 README 한 줄
설명 안에 압축해 넣었다는 것은, 이 도구가 단순한 스트레스
테스터가 아니라 PostgreSQL 내부 구조에 대한 저자의 실전 지식을
담은 결과물이라는 것을 보여준다.

### “치유 가능한” 워크로드와 “치명적인” 워크로드를 구분하는 설계

`bloat-churn`을 “치유 가능한 속도 공격”이라 명명하며 같은 증상을
내는 다른 워크로드(`xmin-horizon-holder`류의 지평선 공격)와
대비시킨 것은, 이 도구가 장애의 종류를 단순히 나열하는 데서 한
걸음 더 나아가 장애의 **회복 가능성**이라는 축으로 워크로드를
분류하고 있다는 뜻이다.

영향도 표에서 `deadlocks`와 `rollbacks`만 “No”로 표시되고 나머지
대부분이 “Yes”로 표시된 것도 같은 맥락이다.
이는 사용자가 도구를 실행하기 전에 “이 워크로드가 실행 중인
다른 서비스에 실제로 위해를 가하는가”를 명시적으로 판단할 수
있게 하려는 설계다.
카오스 엔지니어링 도구 대부분이 “이 실험이 안전한가”를 사용자의
판단에 전적으로 맡기는 것과 비교하면, Noisia는 최소한 위험도를
사전에 분류해 제공한다는 점에서 한 단계 더 신중한 태도를 취하고
있다.

## 비평

### “완전한 이해 없이 실행하지 말라”는 경고는 도구 자체의 안전장치 부재를 인정하는 셈이다

README는 대문자로 “ATTENTION: USE ONLY FOR TESTING PURPOSES, DO
NOT EXECUTE NOISIA WITHOUT COMPLETE UNDERSTANDING WHAT YOU REALLY
DO”라고 경고한다.
이 경고 자체가 정직하다는 점은 인정할 만하지만, 동시에 이는 도구
설계 차원에서 실수를 막을 안전장치가 사실상 없다는 것을 인정하는
문구이기도 하다.

예를 들어 프로덕션 환경과 테스트 환경을 구분해 실행 전 확인을
요구하는 장치, 혹은 연결 대상 데이터베이스가 실제로 격리된
테스트 인스턴스인지 검증하는 최소한의 가드레일이 CLI 차원에
존재하지 않는다.
`--wait-xacts.waiters=0`처럼 무제한 옵션이 기본값과 나란히
제공되는 것도, 사용자가 플래그 하나를 잘못 이해하면 프로덕션
연결 풀 전체를 고갈시킬 수 있는 구조다.
경고 문구로 책임을 사용자에게 완전히 넘기는 방식은, 오픈소스
도구가 흔히 취하는 태도이긴 하지만 “위해를 가하는 도구”라는
특성상 더 적극적인 안전장치가 있었어도 좋았을 부분이다.

### 영향도 표의 “No” 판정은 맥락에 따라 뒤집힐 수 있다

영향도 표는 `deadlocks`와 `rollbacks`를 “영향 없음”으로 분류하지만,
이 판정은 암묵적으로 “정상적인 애플리케이션 로직이 재시도와
오류 처리를 갖추고 있다”는 전제에 기대고 있다.

실제로는 애플리케이션이 교착 상태나 롤백에 대한 재시도 로직을
제대로 구현하지 않은 경우가 드물지 않다.
이런 환경에서 noisia가 인위적으로 교착 상태와 롤백 비율을
높이면, 표에는 “영향 없음”이라 적혀 있어도 실제로는 사용자
요청 실패율 급증이나 애플리케이션 레벨 오류 전파로 이어질 수
있다.
표가 제공하는 이분법적 Yes/No 판정은 PostgreSQL 엔진 자체에
미치는 구조적 손상 여부만을 기준으로 삼고 있을 뿐, 그 위에서
동작하는 애플리케이션 계층에 미치는 영향까지는 포괄하지
못한다.
이 구분을 README에서 명확히 하지 않으면, 사용자가 “No”라는
표시만 보고 안전하다고 오판할 위험이 있다.

### 문서화된 여섯 워크로드와 나머지 여덟 워크로드 사이의 불균형

`backend-killer`, `slot-bloat`, `wal-flood`, `bloat-churn`,
`tempfiles`, `waitxacts` 여섯 워크로드는 전용 데모·튜닝 가이드
문서를 갖췄지만, `idle transactions`, `rollbacks`, `deadlocks`,
`terminate backends`, `failed connections`, `fork connections`
같은 나머지 워크로드는 README의 한 줄 설명 이상의 문서가 없다.

이 불균형은 프로젝트가 최근 들어 특정 워크로드(주로 WAL·블로트
관련 시나리오)에 집중적으로 투자하고 있다는 뜻으로 읽을 수
있지만, 동시에 나머지 워크로드는 상대적으로 덜 성숙했거나 유지
보수 우선순위에서 밀려나 있다는 뜻이기도 하다.
사용자 입장에서는 어떤 워크로드가 충분히 검증되고 문서화된
것이고, 어떤 워크로드가 상대적으로 덜 다듬어진 것인지를 README
목록만 봐서는 구분하기 어렵다.
장애 재현 도구라는 특성상 이런 성숙도 차이는 단순한 문서
공백이 아니라, 실제 사용 시 예측 가능성의 차이로 이어질 수
있는 문제다.

## 인사이트

### 관측 도구 검증과 인력 훈련이라는, README에 없는 두 번째 용도

Noisia의 원작자 samokhvalov는 HN 댓글에서 README에 명시되지 않은
두 가지 용도를 직접 언급했다.
하나는 모니터링·관측 도구가 “나쁜 상황”을 실제로 얼마나 잘
드러내는지 검증하는 용도이고, 다른 하나는 DBA·DBRE·SRE
엔지니어가 다양한 장애 상황을 연습하고 진단 역량을 기르는
훈련 도구로서의 용도다.[^samokhvalov]
그는 동시에 pgbench 같은 표준 벤치마크 도구에는 이런 유해
워크로드가 내장되어 있지 않다는 점을 지적하면서도, 최대 처리량이나
최저 지연시간을 측정하는 일반적인 벤치마크에는 “유해 워크로드”가
오히려 방해가 될 것이라는 균형 잡힌 평가도 함께 남겼다.

이는 본문의 분석에서 다룬 “장애 주입 도구와 관측 도구는 하나의
생태계를 이루는 두 반쪽”이라는 관찰을 원작자 스스로 확인해준
것이기도 하다.
다만 kevteev가 서비스 내부와 서비스 간 우아한 성능 저하(graceful
degradation) 구현을 테스트하는 데 유용하겠다고 언급하자,
samokhvalov는 이런 테스트를 CI에서 완전히 자동화할 수 있을지
되물었다.[^kevteev] 이 질문에 대한 답은 이 스레드에서도, 그리고
2026년 현재의 README에서도 아직 나오지 않았다 — 유해 워크로드를
사람이 수동으로 관찰하는 훈련 도구에서 CI 파이프라인에 안전하게
편입할 수 있는 자동화 도구로 진화시키는 것이, Noisia류 프로젝트
앞에 남은 다음 과제로 보인다.

### 유해 도구의 신뢰도는 “얼마나 정교하게 실패하는가”로 판단해야 한다

일반적인 소프트웨어 도구는 “의도한 대로 성공적으로 동작하는가”로
품질을 판단하지만, Noisia처럼 의도적으로 시스템을 망가뜨리는
도구는 반대로 “의도한 방식으로 정확하게, 그리고 예측 가능하게
실패하는가”로 품질을 판단해야 한다.

`bloat-churn`이 `xmin-horizon-holder`류의 다른 실패와 명확히
구분되는 이유를 설명하는 데 공을 들인 것이나, `wal-flood`가
“디스크 가득 참은 환경에 따라 다르며 보장되지 않는다”고 정직하게
명시한 것은, 이 도구가 “무조건 시스템을 죽인다”가 아니라
“정확히 이 메커니즘을 통해, 이런 조건 아래서만 이 결과가
나온다”는 인과 관계를 정밀하게 설계하려 한다는 증거다.
이런 정밀성은 장애 재현 도구의 진짜 가치가 파괴력이 아니라
재현성과 설명 가능성에 있다는 것을 보여준다.
어떤 카오스 도구든, 사용자가 실패 원인을 사후에 정확히 설명할
수 없다면 그 도구는 학습 도구로서 실패한 것이다.

### “테스트용 장애 생성기”는 관측 가능성 도구 생태계의 거울 이미지다

Noisia 같은 도구가 존재할 수 있다는 사실 자체가, PostgreSQL
관측 가능성(observability) 생태계가 이미 상당히 성숙했다는
방증이다.
`pg_wal` 크기, `temp_files`/`temp_bytes`, `wait_event_type='Lock'`
같은 지표를 관찰하는 방법이 표준화되어 있지 않았다면, Noisia가
만들어내는 장애를 “관찰”하고 “해결”하는 데모 자체가 성립할 수
없었을 것이다.

이는 장애 주입 도구와 관측 도구가 사실상 하나의 생태계를
이루는 두 반쪽이라는 것을 보여준다.
장애를 인위적으로 만들 수 있는 도구가 유용해지려면, 그 장애를
포착하고 해석할 수 있는 관측 인프라가 먼저 갖춰져 있어야 한다.
반대로, 관측 인프라를 검증하고 훈련하려면 실제 장애를 기다리는
대신 Noisia 같은 도구로 장애를 인위적으로 재현하는 편이 훨씬
효율적이다.
두 생태계는 서로를 전제로 성립하며, 하나가 성숙할수록 다른
하나의 존재 가치도 함께 커진다.

### 특정 데이터베이스 엔진에 특화된 카오스 도구가 앞으로 더 늘어날 이유

Chaos Monkey 이후 카오스 엔지니어링 도구 대부분은 인프라
레벨(서버 종료, 네트워크 지연, 디스크 장애)에 초점을 맞춰
범용성을 추구해왔다.
그러나 Noisia는 그 흐름과 반대로, PostgreSQL이라는 단일 엔진의
내부 메커니즘에 완전히 특화된 경로를 택했다.

이 선택이 성립하는 이유는 데이터베이스 엔진마다 실패하는
방식이 근본적으로 다르기 때문이다.
MySQL의 잠금 방식, WAL 재활용 정책, autovacuum 스케줄링은
PostgreSQL과 전혀 다르므로, 범용 카오스 도구는 이런 엔진
고유의 실패 모드를 재현할 수 없다.
앞으로 관측 가능성 요구 수준이 높아질수록, PostgreSQL의
Noisia처럼 특정 엔진(MySQL, Redis, Kafka, 각종 벡터
데이터베이스)에 특화된 정밀 장애 주입 도구가 계속 등장할
가능성이 크다.
이는 카오스 엔지니어링이 “무엇이든 무작위로 부수는 것”에서
“각 시스템이 실제로 어떻게 무너지는지를 정밀하게 재현하는
것”으로 진화하고 있다는 더 큰 흐름의 한 사례로 읽을 수 있다.

---

[^anticristi]: <https://news.ycombinator.com/item?id=23733120>
[^samokhvalov]: <https://news.ycombinator.com/item?id=23732489>
[^kevteev]: <https://news.ycombinator.com/item?id=23733234>
