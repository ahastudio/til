# Kafka 이벤트 스키마 관리 옵션 비교

## 문제: 프로듀서와 컨슈머의 메시지 형식을 어떻게 맞출 것인가

Kafka로 이벤트를 주고받는 시스템이 커지면 프로듀서와 컨슈머 사이의 메시지 형식을 어떻게 맞출지가 문제가 된다.
스키마를 코드에 하드코딩하면 한쪽만 필드를 바꿔도 다른 쪽이 조용히 깨지고, 어떤 필드가 언제 추가되고 삭제됐는지 추적할 방법이 없다.

## 해법: 스키마 레지스트리

스키마 레지스트리는 이 문제를 중앙 저장소로 푼다.
프로듀서는 메시지를 보내기 전에 스키마를 레지스트리에 등록하고, 컨슈머는 메시지에 담긴 스키마 ID로 레지스트리에서 정의를 가져와 역직렬화한다.
스키마가 바뀔 때는 호환성 규칙을 검사해 기존 컨슈머를 깨뜨리는 변경을 미리 막는다.

```text
프로듀서 → 스키마 등록/조회 → 스키마 레지스트리
   │                              ▲
   ▼                              │ 스키마 ID로 조회
 Kafka 토픽 (스키마 ID + 페이로드) → 컨슈머
```

이 생태계에는 여러 구현체가 있고 각각 라이선스, 저장소 아키텍처, 배포 방식이 다르다.

## 비교 대상

- Confluent Schema Registry
- Apicurio Registry (Red Hat)
- AWS Glue Schema Registry
- Karapace (Aiven)
- Buf Schema Registry

## Confluent Schema Registry

- **라이선스**: Confluent Community License.[^ccl] 소스는 공개되어 있지만 OSI 승인 오픈소스는 아니고, 경쟁 SaaS로 재판매하는 것을 금지한다. 클라이언트/직렬화 모듈만 Apache 2.0이고, RBAC·Schema Linking 같은 고급 기능은 유료 Enterprise 구독이 필요하다.
- **지원 포맷**: Avro, Protobuf, JSON Schema
- **호환성 모드**: BACKWARD, FORWARD, FULL(각각 transitive 변형 포함), NONE.[^evolution] 사실상 업계 표준이 되어 다른 레지스트리들이 그대로 따라 구현한다.
- **배포**: 자체 호스팅(Confluent Platform) 또는 완전관리형(Confluent Cloud)
- **저장소**: 전용 Kafka 토픽(`_schemas`, 단일 파티션)에 append-only 로그로 저장. 해당 토픽이 손상되면 스키마 쓰기가 막히는 구조적 병목이 될 수 있다.[^hidden-arch]
- **생태계 통합**: Kafka Connect 컨버터, ksqlDB, REST Proxy, Control Center까지 가장 깊게 통합되어 있다
- **가격**: Confluent Cloud 기준 Essentials는 시간당 $0(스키마 약 1,000개 포함), Advanced는 시간당 $1부터(2만 개 포함), 초과분은 스키마당 시간당 $0.002

## Apicurio Registry

- **라이선스**: Apache 2.0. 2026년 6월 CNCF Sandbox 프로젝트로 채택됐다.[^cncf]
- **지원 포맷**: Avro, Protobuf, JSON Schema에 더해 OpenAPI, AsyncAPI, GraphQL, WSDL, XML Schema까지. Kafka 전용이 아니라 범용 API/스키마 레지스트리다.
- **저장소**: 인메모리(개발용), PostgreSQL, KafkaSQL(Kafka 토픽) 중 선택 가능. Kafka 토픽을 저장소로 쓰는 구조를 피하고 싶다면 PostgreSQL을 고르면 된다.
- **생태계 통합**: Confluent Schema Registry와 호환되는 REST API를 제공해[^apicurio-compat] 기존 Confluent 직렬화기, Kafka Connect 컨버터, ksqlDB, AKHQ와 드롭인으로 연동된다
- **배포**: 자체 호스팅만 가능(Docker, Kubernetes Operator, 또는 Red Hat 상업 지원 빌드). 관리형 클라우드 오퍼링은 없다
- **가격**: 무료(커뮤니티), Red Hat 상업 지원 구독 옵션

## AWS Glue Schema Registry

- **라이선스**: 프로프라이어터리 AWS 서비스. 클라이언트 라이브러리는 GitHub에서 Apache 2.0으로 공개되어 있다[^glue-github]
- **지원 포맷**: Avro(1.11.4), JSON Schema(Draft-04/06/07), Protobuf(proto2/proto3)
- **호환성 모드**: BACKWARD_ALL·FORWARD_ALL·FULL_ALL·DISABLED를 포함해 8가지로 가장 세분화되어 있다.[^glue-docs] 다만 문서에 서술된 검사 동작과 실제 동작이 다르다는 보고도 있다
- **배포**: 완전관리형·서버리스. 인프라 운영이 필요 없는 대신 AWS 종속성이 강하다
- **생태계 통합**: Kafka 클라이언트/Streams/Connect 직렬화기, Amazon MSK, Kinesis, Lambda와 연동. ksqlDB는 지원하지 않는 등 AWS 바깥 생태계와의 통합은 약하다
- **가격**: AWS Glue의 서버리스 기능으로 포함되어 추가 요금 없음

## Karapace

- **라이선스**: Apache 2.0. Aiven이 유지관리하며, Confluent의 Kafka REST Proxy와 Schema Registry를 대체하는 드롭인 구현으로 설계됐다[^karapace]
- **지원 포맷**: Avro, JSON Schema, Protobuf
- **저장소**: Confluent와 마찬가지로 Kafka 토픽
- **생태계 통합**: Confluent와 동일한 REST API를 구현해 기존 Confluent 포맷 클라이언트가 그대로 동작한다
- **배포**: 자체 호스팅 또는 Aiven 관리형 Kafka(Instaclustr도 애드온으로 지원)
- **가격**: 무료. Confluent 호환 API를 원하지만 라이선스 제약은 피하고 싶은 경우의 대안이다

## Buf Schema Registry

Kafka 전용 도구가 아니라 Protobuf를 위한 범용 스키마 레지스트리다.
Confluent와 동일한 API 표면을 구현해 Kafka 프로듀서/컨슈머, ksqlDB, Kafka Connect, AKHQ와 연동할 수 있다.

- **강점**: Google 자체 툴링보다 앞선다고 평가받는 breaking-change 탐지와[^buf-blog] `.proto` 네이티브 린팅·코드 생성. Confluent의 Protobuf 지원이 "동작은 하지만 Avro 우선"이라는 평이 있는 지점을 메운다[^buf-vs-confluent]
- **한계**: Avro나 JSON Schema는 다루지 않는다. 조직이 Protobuf 중심으로 Kafka를 쓰는 경우에만 고려 대상이 된다

## 비교

| 항목 | Confluent SR | Apicurio Registry | AWS Glue SR | Karapace |
| --- | --- | --- | --- | --- |
| 라이선스 | Confluent Community License(소스 공개, OSI 아님) | Apache 2.0(CNCF Sandbox) | 프로프라이어터리 AWS 서비스 | Apache 2.0 |
| 지원 포맷 | Avro, Protobuf, JSON Schema | 위 3종 + OpenAPI/AsyncAPI/GraphQL 등 | Avro, Protobuf, JSON Schema | Avro, Protobuf, JSON Schema |
| 배포 | 자체 호스팅 + 관리형 클라우드 | 자체 호스팅만 | 완전관리형(AWS 전용) | 자체 호스팅 또는 Aiven 관리형 |
| 벤더 종속성 | 낮음~중간 | 없음 | 높음(AWS) | 낮음 |
| 저장 백엔드 | Kafka 토픽(단일 파티션) | 인메모리/PostgreSQL/KafkaSQL 중 선택 | AWS 관리형(비공개) | Kafka 토픽 |
| Kafka 생태계 통합 | 가장 깊음(네이티브) | 높음(Confluent API 호환) | 중간(AWS 중심) | 높음(Confluent API 드롭인) |
| 가격 | 코어 무료, Enterprise 기능·클라우드 초과분은 유료 | 무료(Red Hat 상업 지원 옵션) | 무료(AWS 추가 요금 없음) | 무료 |
| 주요 약점 | 소스 공개 라이선스, 단일 파티션 토픽의 구조적 병목, 고급 기능 유료화 | 관리형 오퍼링 부재 | UI 부재, 비-AWS 생태계 통합 약함 | 커뮤니티 규모 작음, 거버넌스 기능 미흡 |

## 선택 기준

- 이미 Confluent Platform/Cloud를 쓰거나 표준적인 선택을 원한다 → **Confluent Schema Registry**
- 오픈소스·벤더 중립성·PostgreSQL 같은 유연한 저장소를 원한다 → **Apicurio Registry**
- AWS 네이티브 환경이고 추가 인프라 없이 쓰고 싶다 → **AWS Glue Schema Registry**
- Confluent 호환 API를 무료 오픈소스로 원한다 → **Karapace**
- Protobuf 중심이고 breaking-change 탐지가 중요하다 → **Buf Schema Registry**

---

[^ccl]: [confluentinc/schema-registry LICENSE-ConfluentCommunity](https://github.com/confluentinc/schema-registry/blob/master/LICENSE-ConfluentCommunity)

[^evolution]: [Confluent Docs: Schema Evolution and Compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)

[^hidden-arch]: [Medium: The Hidden Architecture of Confluent Schema Registry](https://medium.com/@aywengo/the-hidden-architecture-of-confluent-schema-registry-how-leader-election-really-works-b10069d760bd)

[^cncf]: [Apicurio Registry Joins CNCF](https://www.apicur.io/blog/2026/06/18/apicurio-registry-joins-cncf)

[^apicurio-compat]: [Apicurio: Confluent Schema Registry Compatibility API](https://www.apicur.io/registry/docs/apicurio-registry/3.3.x/getting-started/assembly-confluent-schema-registry-compatibility.html)

[^glue-github]: [awslabs/aws-glue-schema-registry](https://github.com/awslabs/aws-glue-schema-registry)

[^glue-docs]: [AWS Glue: How the Schema Registry Works](https://docs.aws.amazon.com/glue/latest/dg/schema-registry-works.html)

[^karapace]: [Aiven-Open/karapace](https://github.com/Aiven-Open/karapace)

[^buf-blog]: [Buf: Why a Protobuf Schema Registry?](https://buf.build/blog/why-a-protobuf-schema-registry)

[^buf-vs-confluent]: [LinkedIn: Confluent vs Buf — What's the Difference?](https://www.linkedin.com/posts/zoranmilosevic_confluent-vs-buf-whats-the-difference-activity-7363940413101039616-1uk9)
