# Grafana 관측성 스택과 OpenTelemetry: 무엇이 있고 각각 왜 쓰는가

## 소개

관측성(observability)은 시스템이 밖으로 내보내는 데이터만으로
안에서 무슨 일이 일어나는지 묻고 답할 수 있는 상태를 말한다.
그 데이터를 흔히 시그널이라 부르고, 이 문서는 네 가지를 다룬다.

| 시그널   | 답하는 질문                           | 이 문서의 저장소  |
| -------- | ------------------------------------- | ----------------- |
| 메트릭   | 얼마나, 얼마나 자주, 얼마나 느린가    | Prometheus, Mimir |
| 로그     | 그때 정확히 무슨 일이 있었나          | Loki              |
| 트레이스 | 요청 하나가 어디를 거쳐 어디서 막혔나 | Tempo             |
| 프로파일 | 코드의 어느 함수가 CPU·메모리를 쓰나  | Pyroscope         |

Grafana Labs는 이 시그널마다 오픈소스 저장소를 하나씩 만들고 Grafana로 묶었다.
Loki(로그), Grafana(시각화), Tempo(트레이스), Mimir(메트릭)의 첫 글자를 따
“LGTM 스택”이라 부른다.[^mimir]
여기에 수집 표준인 OpenTelemetry와 메트릭의 사실상 표준인 Prometheus가 더해져
현재 오픈소스 관측성의 기본 조합이 된다.

이 문서는 각 구성 요소가 무엇이고 어떤 가치를 주는지,
서로 어떻게 연결되는지, 어디서부터 공부하면 되는지를 한 장에 정리한 시작점이다.
자세한 내용은 각 각주의 공식 문서에서 이어서 보면 된다.

## 한눈에 보기

| 구성 요소     | 역할                                 | 라이선스   | 상태 (2026-10 기준)                              |
| ------------- | ------------------------------------ | ---------- | ------------------------------------------------ |
| Grafana       | 대시보드·탐색·알림 UI                | AGPL-3.0   | 활성, v13.2.4[^gh-grafana]                       |
| Prometheus    | 메트릭 수집·저장·질의                | Apache-2.0 | 활성, v3.15.0, CNCF 졸업(2018)[^cncf-prom]       |
| Mimir         | Prometheus 호환 대규모 메트릭 저장소 | AGPL-3.0   | 활성, 3.2.2[^gh-grafana]                         |
| Loki          | 로그 저장소                          | AGPL-3.0   | 활성, v3.7.8[^gh-grafana]                        |
| Tempo         | 분산 트레이스 저장소                 | AGPL-3.0   | 활성, v3.1.0[^gh-grafana]                        |
| Pyroscope     | 지속적 프로파일링                    | AGPL-3.0   | 활성, v2.4.0[^gh-grafana]                        |
| Alloy         | 수집기 (OTel Collector 배포판)       | Apache-2.0 | 활성, v1.20.1, Grafana Agent 대체[^alloy]        |
| Beyla / OBI   | eBPF 자동 계측                       | Apache-2.0 | OpenTelemetry에 기증되어 OBI가 됨[^beyla]        |
| k6            | 부하 테스트                          | AGPL-3.0   | 활성, v2.3.0[^gh-grafana]                        |
| Faro          | 브라우저 실사용자 모니터링(RUM) SDK  | Apache-2.0 | 활성, v2.12.1[^gh-grafana]                       |
| OnCall OSS    | 온콜·인시던트 대응                   | AGPL-3.0   | 2026년 3월 아카이브, Cloud IRM으로 이전[^oncall] |
| OpenTelemetry | 계측 API·SDK·프로토콜·수집기 표준    | Apache-2.0 | 활성, CNCF 졸업(2026)[^otel-grad]                |

Grafana, Loki, Tempo는 2021년 Apache 2.0에서 AGPLv3로 라이선스를 바꿨다.[^agpl]
자체 호스팅해서 쓰는 것은 문제가 없지만,
수정한 코드를 네트워크 서비스로 제공하면 소스 공개 의무가 생긴다.
수집 쪽(Alloy, Beyla, Faro, OpenTelemetry)은 Apache 2.0이라
애플리케이션에 넣는 부분과 서버 쪽 저장소의 라이선스가
다르다는 점을 알아 두면 좋다.

## 데이터가 흐르는 길

```text
[애플리케이션]  OTel SDK·자동 계측, Beyla/OBI(eBPF), Faro(브라우저)
      │  OTLP (gRPC 4317 / HTTP 4318)
      ▼
[수집기]  OpenTelemetry Collector 또는 Alloy
      │  처리: 배치, 샘플링, 속성 정리, 라우팅
      ├─▶ 메트릭  ─▶ Prometheus / Mimir
      ├─▶ 로그    ─▶ Loki
      ├─▶ 트레이스 ─▶ Tempo
      └─▶ 프로파일 ─▶ Pyroscope
                        │
                        ▼
                  [Grafana]  대시보드, Explore, 알림, 시그널 간 이동
```

핵심은 계측과 저장을 분리하는 것이다.
애플리케이션은 OpenTelemetry로 한 번만 계측하고,
어디에 저장할지는 수집기 설정으로 정한다.
저장소를 Grafana 스택에서 다른 벤더로 바꿔도 애플리케이션 코드는 그대로다.

## 구성 요소

### Grafana: 모든 시그널을 한 화면에서

Grafana는 데이터를 저장하지 않는다.
Prometheus, Loki,
Tempo뿐 아니라 여러 데이터 소스에 질의해 대시보드로 보여 주는 UI다.
가치는 시그널 사이를 오갈 수 있다는 데 있다.
메트릭 그래프에서 튀는 지점을 누르면 그 시점의 트레이스로,
트레이스의 스팬에서 같은 요청의 로그로 넘어간다.
이 연결의 대표적인 장치가 exemplar다.
exemplar는 특정 시간 구간의 측정값을 대표하는 트레이스 하나로,
집계된 메트릭과 개별 요청을 보여 주는 트레이스를 잇는다.[^exemplars]

공부 포인트: 데이터 소스 추가, 대시보드와 변수,
Explore, 알림 규칙, 시그널 간 상관 설정.

### Prometheus: 메트릭의 기준점

Prometheus는 2012년에 시작된 오픈소스 모니터링·알림 도구다.[^prom-overview]
메트릭 이름과 키-값 레이블로 식별되는 다차원 시계열을 저장하고,
PromQL로 질의하며,
HTTP로 대상에서 값을 가져오는 pull 방식으로 수집한다.[^prom-overview]
짧게 끝나는 작업은 Pushgateway를 거쳐 보내고,
알림은 Alertmanager가 처리한다.[^prom-overview]
단일 서버로 독립적으로 동작한다는 점이 신뢰성의 근거다.[^prom-overview]

2024년 11월의 3.0은 OpenTelemetry와 가까워진 버전이다.
OTLP 메트릭을 직접 받는 엔드포인트가 생겼고,
메트릭과 레이블 이름에 UTF-8을 기본으로 허용하며,
Remote Write 2.0을 지원한다.[^prom3]

한계도 공식 문서에 적혀 있다.
요청 단위 과금처럼 100% 정확도가 필요하면
Prometheus는 맞지 않는다.[^prom-overview]

공부 포인트: 메트릭 타입(counter, gauge, histogram),
레이블 설계와 카디널리티, PromQL의 `rate`와 집계, 기록 규칙과 알림 규칙.

### Mimir: Prometheus를 크게 키울 때

Prometheus 서버 하나는 저장 기간과 규모에 한계가 있다.
Mimir는 Prometheus 메트릭을
수평 확장·고가용성·멀티테넌트로 오래 저장하는 저장소다.
Cortex에서 만든 것과 Grafana Enterprise Metrics,
Grafana Cloud를 운영하며 쌓은 기능을 합친 포크이고,
10억 개 이상의 시계열까지 확장할 수 있다고 소개한다.[^mimir]
Prometheus는 수집기 역할을 하고 Remote Write로 Mimir에 보내는 구성이 일반적이다.

공부 포인트: Remote Write, 테넌트, 마이크로서비스 모드와 단일 바이너리 모드.

### Loki: 로그를 싸게 저장한다

Loki는 로그 내용을 색인하지 않고,
로그 스트림마다 붙은 레이블이라는 메타데이터만 색인한다.[^loki]
로그 본문은 압축해 S3나 GCS 같은 객체 저장소에 청크로 저장한다.[^loki]
전체 내용을 색인하는 기존 로그 시스템보다 운영비가
크게 낮다는 것이 가치다.[^loki]
질의 언어 LogQL은 PromQL에서 영감을 받았다.[^loki]
대신 레이블이 아닌 내용으로 찾으려면 해당 기간의 청크를 훑어야 하므로,
레이블 설계가 성능을 좌우한다.

공부 포인트: 레이블과 스트림, 카디널리티를 피하는 레이블 설계,
LogQL의 필터와 로그에서 메트릭 만들기.

### Tempo: 트레이스를 객체 저장소에

Tempo는 객체 저장소만 있으면 동작하는 대규모 분산 트레이스 저장소다.[^tempo]
Jaeger, Zipkin, OpenTelemetry 프로토콜을 받고,
TraceQL로 조건에 맞는 트레이스와 스팬을 찾는다.[^tempo]
스팬에서 메트릭을 만들어 낼 수 있어 트레이스와 메트릭을 잇고,
Grafana, Prometheus, Loki와 연결해 시그널 간 상관 분석을 한다.[^tempo]

공부 포인트: 트레이스·스팬·컨텍스트 전파의 개념, 샘플링, TraceQL, 스팬 메트릭.

### Pyroscope: 네 번째 시그널, 프로파일

Pyroscope는 운영 환경에서 상시로 프로파일을 모으는 지속적 프로파일링 도구다.
2023년 Grafana Phlare와 합쳐졌고,
Grafana Labs는 이를 관측성의 다음 기둥으로 소개했다.[^pyroscope]
트레이스가 “어느 서비스가 느린가”를 알려 준다면
프로파일은 “그 서비스의 어느 함수가 느린가”를 알려 준다.

### Alloy: 수집기

Alloy는 프로그래밍 가능한 파이프라인을 갖춘 OpenTelemetry Collector 배포판이고,
Prometheus 파이프라인이 내장되어 있다.[^alloy]
이전 제품인 Grafana Agent는 2025년 11월 1일 지원이 끝났다.[^agent-eol]
Grafana 스택만 쓴다면 Alloy가,
벤더 중립이 더 중요하다면 OpenTelemetry Collector가 자연스러운 선택이다.

### Beyla와 OBI: 코드를 고치지 않는 계측

Beyla는 eBPF 기반 자동 계측 도구로,
애플리케이션 코드를 고치지 않고 텔레메트리를 만든다.[^beyla]
Grafana Labs는 2025년 Beyla를 OpenTelemetry에 기증했고,
그 프로젝트가 OpenTelemetry eBPF Instrumentation(OBI)이다.[^beyla]
계측 코드를 넣기 어려운 레거시 서비스에서 출발점이 된다.

### k6와 Faro: 시험하고, 사용자 쪽에서 보기

k6는 Go와 JavaScript로 만든 부하 테스트 도구다.[^gh-grafana]
부하를 주는 동안 같은 Grafana에서 메트릭과 트레이스를 함께 보면
병목을 찾는 실험이 된다.
Faro는 브라우저에서 실사용자 모니터링 데이터를 모으는 SDK다.[^gh-grafana]
서버 쪽 트레이스와 이어 사용자가 실제로 겪는 지연을 볼 수 있다.

### 온콜

Grafana OnCall OSS는 2025년 3월 유지 보수 모드에 들어갔고
2026년 3월 아카이브되었으며,
Grafana Cloud IRM 앱으로 옮기라고 안내한다.[^oncall]
자체 호스팅으로 온콜까지 하려면 다른 도구를 찾아야 한다.

## OpenTelemetry

OpenTelemetry(OTel)는 트레이스, 메트릭, 로그 같은 텔레메트리를
생성하고 내보내고 수집하기 위한 벤더 중립 프레임워크다.[^otel-what]
OpenTelemetry 자체는 관측성 백엔드가 아니다.[^otel-what]
저장과 시각화는 Prometheus, Tempo, Loki 같은 다른 도구에 맡긴다.

구성 요소는 다음과 같다.[^otel-what]

| 구성 요소       | 하는 일                                       |
| --------------- | --------------------------------------------- |
| 명세와 OTLP     | 텔레메트리 데이터 구조와 전송 프로토콜의 표준 |
| SDK             | 언어별로 텔레메트리를 만드는 구현             |
| 시맨틱 컨벤션   | `http.request.method` 같은 속성 이름의 표준   |
| Collector       | 받고, 처리하고, 내보내는 프록시               |
| 계측 라이브러리 | 주요 프레임워크용 미리 만든 계측              |
| 자동 계측       | 코드 수정 없이 텔레메트리 생성                |

가치는 두 가지로 정리된다.
생성한 데이터를 자기가 소유해 벤더 종속을 피할 수 있고,
조직 전체가 하나의 API로 계측할 수 있다.[^otel-what]
2026년 5월 CNCF 졸업 프로젝트가 되었다.[^otel-grad]

시그널별 성숙도는 다르다.[^otel-status]

| 시그널   | API            | SDK    | 프로토콜    |
| -------- | -------------- | ------ | ----------- |
| 트레이스 | Stable         | Stable | Stable      |
| 메트릭   | Stable         | Mixed  | Stable      |
| 로그     | Stable(브리지) | Stable | Stable      |
| 배기지   | Stable         | Stable | 해당 없음   |
| 프로파일 | —              | —      | Development |

메트릭 SDK는 언어별 구현마다 상태가 다르고,
로그 API는 애플리케이션이 직접 쓰는 API가 아니라
기존 로깅 라이브러리를 OTel로 잇는 브리지 API다.[^otel-status]

공부 포인트: 컨텍스트 전파와 `traceparent`, 리소스 속성(`service.name`),
시맨틱 컨벤션, Collector의 receiver·processor·exporter 파이프라인,
샘플링(head와 tail).

## 바로 해 보기

Grafana가 배포하는 `grafana/otel-lgtm` 이미지 하나에
OpenTelemetry Collector, Grafana, Loki, Mimir, Tempo가 들어 있다.[^otel-lgtm]
개발, 데모, 테스트용이고 운영용은 아니다.[^otel-lgtm]

```bash
docker run --rm -ti \
  -p 3000:3000 \
  -p 4317:4317 \
  -p 4318:4318 \
  grafana/otel-lgtm
```

3000번은 Grafana(초기 계정 `admin`/`admin`),
4317과 4318은 각각 OTLP gRPC와 HTTP다.[^otel-lgtm]
애플리케이션에 OpenTelemetry SDK를 붙이고
`OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`로 보내면
Grafana에서 세 시그널을 바로 볼 수 있다.

직접 운영하고 싶지 않다면 Grafana Cloud의 무료 플랜이 있다.
신용카드 없이 쓸 수 있고, 사용량 한도 안에서 모든 서비스를 쓰며,
데이터는 14일 보관한다.[^pricing]

## 함정

- **카디널리티 폭발**: 사용자 ID나 요청 ID를 메트릭 레이블이나 Loki 레이블에 넣으면 시계열과 스트림 수가 폭증한다. 그런 값은 로그 본문이나 트레이스 속성에 둔다.
- **세 개의 저장소를 각각 운영해야 한다**: LGTM 스택은 시그널마다 저장소가 다르다. 단일 저장소로 묶은 SigNoz 같은 대안과의 비교는 [SigNoz vs Grafana Stack](../devops/signoz-vs-grafana.md)에 있다.
- **샘플링 없이 트레이스 전부 저장**: 트래픽이 크면 저장 비용이 빠르게 커진다. 수집기에서 샘플링 정책을 먼저 정한다.
- **로그 내용 검색을 기대하기**: Loki는 레이블만 색인하므로 전문 검색 위주라면 설계를 다시 봐야 한다.[^loki]
- **라이선스 확인 누락**: 저장소 쪽은 AGPLv3다. 수정해서 서비스로 제공할 계획이 있다면 미리 확인한다.[^agpl]
- **수집기 마이그레이션**: Grafana Agent를 아직 쓰고 있다면 지원이 끝났으므로 Alloy나 OTel Collector로 옮겨야 한다.[^agent-eol]

## 공부 순서

1. 관측성의 세 시그널과 차이를 이해한다(이 문서의 소개 표).
2. Prometheus 하나로 메트릭, PromQL, 알림을 익힌다.
3. Grafana에 Prometheus를 붙여 대시보드와 알림을 만든다.
4. `grafana/otel-lgtm`을 띄우고 애플리케이션 하나를 OpenTelemetry로 계측한다.
5. Tempo에서 트레이스를 보고, Loki 로그와 exemplar로 시그널 사이를 오가 본다.
6. 수집기(OTel Collector 또는 Alloy) 파이프라인과 샘플링을 직접 설정한다.
7. 규모가 커지면 Mimir, 성능 분석이 필요하면 Pyroscope, 부하 실험은 k6로 넓힌다.

## 필요한 시그널부터 고르기

모든 조직이 처음부터 LGTM 전체를 운영할 필요는 없다.
먼저 해결할 질문을 하나 정한다.
오류율과 지연 시간의 추세가 문제라면 메트릭부터,
특정 요청이 실패한 이유가 문제라면 구조화된 로그부터,
여러 서비스 사이의 지연 경로가 문제라면 트레이스부터 시작한다.
CPU와 메모리 사용이 어디서 생기는지 모를 때 프로파일을 더한다.

각 시그널을 추가할 때는 보관 기간,
샘플링 비율, 레이블과 속성의 민감도,
담당자가 실제로 확인할 알림을 함께 정한다.
수집량을 늘리고 나중에 줄이려 하면
저장 비용과 개인정보 노출 범위가 먼저 커진다.

운영 형태도 선택의 일부다.
관리형 서비스를 쓰면 저장소 운영을 줄이는 대신
사용량과 데이터 이동 조건을 확인해야 한다.
직접 운영하면 AGPL 구성 요소의 배포 방식,
업그레이드와 장애 대응을 맡을 인력을 계산한다.
관측성 스택은 도구를 많이 붙이는 프로젝트가 아니라
장애 시 원인을 찾는 데 필요한 신호를 적정 비용으로 유지하는 일이다.

## 이 저장소의 관련 문서

- [Grafana 설치 메모](README.md)
- [OpenTelemetry](../opentelemetry/README.md)
- [OpenTelemetry Python](../opentelemetry/opentelemetry-python.md)
- [OpenTelemetry in 2023](../opentelemetry/opentelemetry-in-2023.md)
- [OTel isn't going well](../opentelemetry/otel-isnt-going-well.md)
- [SigNoz vs Grafana Stack](../devops/signoz-vs-grafana.md)
- [SigNoz](../devops/signoz.md)
- [ClickHouse is winning the observability wars](../clickhouse/clickhouse-is-winning-the-observability-wars.md)
- [Production Is Where the Rigor Goes](../devops/production-is-where-the-rigor-goes.md)

---

[^mimir]: Grafana Labs, [Announcing Grafana Mimir, the most scalable open source TSDB in the world](https://grafana.com/blog/2022/03/30/announcing-grafana-mimir/), 2022-03-30

[^gh-grafana]: GitHub, [Grafana Labs organization](https://github.com/grafana), 2026-10-14 조회 기준 각 저장소의 라이선스와 최신 릴리스

[^cncf-prom]: CNCF, [Cloud Native Computing Foundation announces Prometheus graduation](https://www.cncf.io/announcements/2018/08/09/prometheus-graduates/), 2018-08-09

[^alloy]: Grafana Labs, [Introducing an OpenTelemetry Collector distribution with built-in Prometheus pipelines: Grafana Alloy](https://grafana.com/blog/2024/04/09/grafana-alloy-opentelemetry-collector-with-prometheus-pipelines/), 2024-04-09

[^agent-eol]: Grafana Labs, [Grafana Agent | Grafana Agent documentation](https://grafana.com/docs/agent/latest/)

[^beyla]: Grafana Labs, [Introducing OpenTelemetry eBPF Instrumentation: Why we donated Grafana Beyla to OpenTelemetry](https://grafana.com/blog/2025/05/07/opentelemetry-ebpf-instrumentation-beyla-donation/), 2025-05-08

[^oncall]: Grafana Labs, [Grafana OnCall OSS in maintenance mode: your questions answered](https://grafana.com/blog/2025/03/11/grafana-oncall-maintenance-mode/), 2025-03-11

[^otel-grad]: CNCF, [Cloud Native Computing Foundation Announces OpenTelemetry's Graduation](https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation/), 2026-05-21

[^agpl]: Grafana Labs, [Grafana, Loki, and Tempo will be relicensed to AGPLv3](https://grafana.com/blog/2021/04/20/grafana-loki-tempo-relicensing-to-agplv3/), 2021-04-20

[^exemplars]: Grafana Labs, [Introduction to exemplars](https://grafana.com/docs/grafana/latest/fundamentals/exemplars/)

[^prom-overview]: Prometheus, [Overview](https://prometheus.io/docs/introduction/overview/)

[^prom3]: The Prometheus Team, [Announcing Prometheus 3.0](https://prometheus.io/blog/2024/11/14/prometheus-3-0/), 2024-11-14

[^loki]: Grafana Labs, [Grafana Loki overview](https://grafana.com/docs/loki/latest/get-started/overview/)

[^tempo]: Grafana Labs, [Grafana Tempo](https://grafana.com/docs/tempo/latest/)

[^pyroscope]: Grafana Labs, [Pyroscope and Grafana Phlare join together to accelerate adoption of continuous profiling, the next pillar of observability](https://grafana.com/blog/2023/03/15/pyroscope-grafana-phlare-join-for-oss-continuous-profiling/), 2023-03-15

[^otel-what]: OpenTelemetry, [What is OpenTelemetry?](https://opentelemetry.io/docs/what-is-opentelemetry/)

[^otel-status]: OpenTelemetry, [Specification Status Summary](https://opentelemetry.io/docs/specs/status/)

[^otel-lgtm]: Grafana Labs, [Docker OpenTelemetry LGTM](https://grafana.com/docs/opentelemetry/docker-lgtm/)

[^pricing]: Grafana Labs, [Pricing](https://grafana.com/pricing/)
