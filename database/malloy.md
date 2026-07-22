# Malloy — SQL 위에 쌓은 데이터 모델링 언어

> A modern open source language for analyzing, transforming, and modeling data.

<https://www.malloydata.dev/>

<https://github.com/malloydata/malloy>

HN 토론: <https://news.ycombinator.com/item?id=39735569> (3점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=31679>

## 소개

Malloy는 데이터 관계, 변환, 모델링을 위한 오픈소스 언어다.
SQL 엔진 위에서 동작하며, Malloy 쿼리는 실행 시점에 최적화된 SQL로 컴파일된다.
원래 Looker 산하의 실험 프로젝트로 시작했으나,
현재는 독립적인 malloydata 프로젝트로 성장해 GitHub 스타 약 2,500개를 기록한다.
BigQuery, DuckDB, PostgreSQL을 포함한 여러 데이터베이스를 지원한다.

## 핵심 개념

**시맨틱 데이터 모델** — Malloy는 쿼리와 데이터 모델을 분리한다.
`source`를 정의하면 테이블 구조, 관계, 계산 규칙을 한 곳에 선언하고
여러 쿼리에서 재사용할 수 있다.

**중첩 쿼리(Nested Queries)** — 단일 쿼리 안에 집계 결과를 중첩시킬 수 있다.
SQL에서 여러 단계의 서브쿼리로 해결해야 할 것을 Malloy는 자연스러운 구문으로 표현한다.

**대칭 집계(Symmetric Aggregates)** — 여러 테이블을 조인할 때 발생하는
중복 계산 오류를 방지하는 집계 방식이다.
합계, 평균, 개수를 계산할 때 조인 구조와 관계없이 올바른 결과를 보장한다.

**뷰(Views) 재사용** — 정의된 집계와 필터를 `view`로 선언하면
다른 쿼리에서 쉽게 참조할 수 있다.
이 구조는 반복적인 쿼리 작성을 줄이고 분석 로직의 일관성을 높인다.

## 사용법

VSCode 확장 프로그램이 공식 지원된다.
`.malloy` 파일을 만들고 소스를 정의한 뒤 쿼리를 작성하면
바로 결과를 확인할 수 있다.

```malloy
source: flights is duckdb.table('flights.parquet') extend {
  measure: flight_count is count()
  measure: total_distance is sum(distance)
}

run: flights -> {
  group_by: carrier
  aggregate: flight_count, total_distance
  nest: by_origin is {
    group_by: origin
    aggregate: flight_count
  }
}
```

이 쿼리는 항공사별 집계에 출발지별 중첩 집계를 한 번에 표현한다.
SQL로 같은 결과를 얻으려면 여러 단계의 CTE 또는 서브쿼리가 필요하다.

## 분석

### SQL의 어디를 보완하려 하는가

SQL은 집합 연산에 최적화된 언어지만, 현대 분석 작업에서 반복되는 패턴에 약점이 있다.
조인된 테이블 간의 집계 오류, 반복되는 계산 정의, 재사용하기 어려운 쿼리 구조가 대표적이다.
Malloy는 이 세 가지를 시맨틱 모델, 대칭 집계, 뷰 재사용으로 해결하려 한다.

접근 방식은 dbt가 데이터 변환 계층에서 했던 것과 유사하다.
dbt가 “SQL을 더 잘 관리하자”는 방향이라면,
Malloy는 “SQL을 다른 언어로 대체하자”는 방향이다.
후자는 더 급진적인 접근이며, 학습 비용이 따른다.

### Looker와의 관계가 양날의 검이다

Malloy가 Looker에서 시작했다는 사실은 프로덕션 환경에서의 검증을 의미하지만,
동시에 특정 벤더의 비전이 언어 설계에 반영됐을 가능성을 의미한다.
Looker의 LookML이 해결하려 했던 문제와 Malloy가 해결하려는 문제가
얼마나 겹치는지, 어떻게 다른지를 이해하면 Malloy의 포지셔닝이 더 명확해진다.

독립 프로젝트로 전환된 것은 언어의 범용성을 높이는 방향이지만,
Looker 생태계 밖에서 커뮤니티를 어떻게 구성하느냐가 과제다.

GeekNews 사용자 click의 댓글처럼[^click] SQL에 익숙한 사람에게
Malloy의 문법이 반드시 더 간결하게 느껴지지 않을 수 있다.
C# LINQ 같은 다른 패러다임이 더 친숙한 경우도 있다.
언어 설계에서 “더 간결하다”는 주장은 항상 “누구에게, 어떤 작업에서”라는 조건이 붙는다.

## 비평

### “SQL보다 낫다”는 주장이 맥락에 따라 다르게 성립한다

Malloy 문서는 SQL보다 간결하고 오류가 적다고 주장하지만,
이 주장이 성립하는 조건은 “복잡한 중첩 집계와 재사용 가능한 모델이 필요한 상황”이다.
단순한 필터링, 집계, 조인 쿼리에서 Malloy가 SQL보다 낫다고 말하기 어렵다.

otteromkram은 한 줄로 이 회의론을 압축했다.[^otteromkram]
“존재하지 않는 문제의 해결책”이라는 지적은 과격하지만,
SQL로 이미 잘 해결되는 워크플로를 가진 팀에게 Malloy 도입 비용이 얼마나 정당화될 수 있는지에 대한 질문이기도 하다.
새 언어를 배우고, 기존 파이프라인을 전환하고, 팀 전체를 교육하는 비용은
Malloy가 제공하는 이점이 “충분히 크고 자주 발생하는 문제”일 때만 감당할 수 있다.

분석 도구의 선택은 팀의 SQL 역량, 기존 워크플로, 필요한 복잡도 수준에 따라 달라진다.
Malloy가 빛나는 시나리오는 분명히 있지만,
“SQL을 대체할 언어”로 자리잡으려면 더 광범위한 사용 사례를 커버해야 한다.

### 생태계 성숙도가 채택의 걸림돌이다

2,500개의 GitHub 스타는 관심을 받고 있다는 신호지만,
프로덕션 채택을 판단하는 기준은 다르다.
에러 메시지의 품질, 에디터 통합, 문서의 깊이, 커뮤니티 활성화가 중요하다.
VSCode 확장이 공식 지원되는 것은 긍정적이지만,
Slack 커뮤니티 규모와 질문에 대한 응답 속도가 실제 사용자 경험을 결정한다.

mdaniel은 구체적인 문법 불일치 사례를 들어 이 문제를 드러냈다.[^mdaniel]
`where: origin ? 'SFO'`와 `where: state != null`이 서로 다른 방식으로 SQL에 매핑된다면
문법이 일관되지 않다는 뜻이고, 이는 학습 비용을 높인다.
문서 링크가 깨져 있었다는 지적도 함께 나왔다.
언어 설계의 세밀함과 문서 품질은 커뮤니티 신뢰의 기반이다.
이 부분이 미흡하면 기술적 우위가 있어도 채택으로 이어지지 않는다.

SQL이 수십 년의 에코시스템을 가진 언어임을 고려하면,
새로운 언어가 그 자리를 차지하는 것은 기술적 우위만으로 이루어지지 않는다.

## 인사이트

### 시맨틱 레이어가 데이터 분석 스택의 핵심 논쟁이 됐다

Malloy, dbt Semantic Layer, LookML, Cube.js 같은 도구들이 경쟁하는 영역은
“시맨틱 레이어(semantic layer)”라는 개념이다.
이 레이어는 비즈니스 로직을 쿼리와 분리해 한 곳에 정의하는 계층이다.
같은 지표를 여러 도구에서 일관되게 사용할 수 있게 해주는 것이 목표다.

이 경쟁이 흥미로운 이유는 “진실의 원천(single source of truth)”이라는
데이터 팀의 오랜 목표를 언어 수준에서 다루기 때문이다.
SQL을 쓰는 한 지표 정의가 분산되는 문제를 완전히 해결하기 어렵다.
시맨틱 레이어 도구들은 이 문제를 언어 설계와 인프라 수준에서 접근한다.

### 데이터 분석 언어의 미래는 LLM과의 관계에 달려 있다

Malloy가 SQL 위에 추상 계층을 쌓는 방향은
LLM 기반 코드 생성과 흥미로운 긴장 관계를 만든다.
LLM은 SQL을 이미 잘 생성하지만 Malloy는 훈련 데이터가 훨씬 적다.
“LLM이 SQL을 잘 쓰는데 굳이 새 언어를 배워야 하는가”라는 질문은 현실적이다.

반대로 Malloy 같은 시맨틱 레이어 언어가 더 풍부한 컨텍스트를 제공한다면
LLM이 더 정확한 분석 쿼리를 생성하는 기반이 될 수 있다.
LLM을 적으로 보는 대신 협력 도구로 포지셔닝하는 것이
Malloy 생태계 성장의 유망한 경로 중 하나다.

---

[^click]: <https://news.hada.io/topic?id=31679#cid62209>
[^otteromkram]: <https://news.ycombinator.com/item?id=37774407>
[^mdaniel]: <https://news.ycombinator.com/item?id=39735774>
