# Bifrost

<https://github.com/maximhq/bifrost>

## 소개

Go로 작성된 초고속 엔터프라이즈 AI 게이트웨이다.
OpenAI, Anthropic, AWS Bedrock, Google Vertex AI 등 15개 이상의 AI 제공자를 단일 OpenAI 호환 API로 통합한다.
추가 지연시간 11µs, 5,000 RPS에서 100% 성공률을 성능 지표로 제시한다.
Apache 2.0 라이선스.

## 주요 기능

### 라우팅 및 안정성

- 여러 API 키와 제공자 간 지능형 부하 분산
- 자동 장애 조치로 다운타임 없는 페일오버
- 시맨틱 유사도 기반 응답 캐싱으로 비용·지연시간 절감

### 멀티모달 지원

텍스트, 이미지, 오디오, 스트리밍을 모두 지원한다.
MCP(Model Context Protocol)를 통해 AI가 외부 도구를 사용할 수 있다.

### 엔터프라이즈 기능

- 계층적 예산 관리 및 비용 제어
- Google·GitHub SSO 통합 인증
- Prometheus 메트릭, 분산 추적, 포괄적 로깅
- HashiCorp Vault 통합

## 아키텍처

```text
core/            핵심 기능 (providers/, schemas/)
framework/       데이터 지속성 (configstore/, logstore/, vectorstore/)
transports/      HTTP 게이트웨이
plugins/         확장 시스템
```

언어 구성: Go 74.6%, TypeScript 16.9%, Python 4.8%.

## 시작하기

```bash
npx -y @maximhq/bifrost
```

또는 Docker로 배포 후 `http://localhost:8080` 웹 UI에서 구성한다.
기존 OpenAI SDK 코드에서 엔드포인트만 변경하는 드롭인 교체 방식을 지원한다.

## 분석

LiteLLM 대비 50배 빠르다는 주장은 Go 기반 구현의 이점에서 온다.
LiteLLM이 Python으로 작성되어 있어 단순 프록시 레이어에서도 인터프리터 오버헤드가 있는 반면, Bifrost는 컴파일 언어로 레이턴시를 최소화한다.
시맨틱 캐싱은 단순 키-값 캐시와 달리 의미론적으로 유사한 요청을 같은 캐시 항목으로 처리해 캐시 히트율을 높인다.

## 비평

50배 성능 주장은 구체적인 벤치마크 조건이 명시되지 않으면 마케팅 수치로 봐야 한다.
시맨틱 캐싱은 벡터 유사도 계산 자체에 비용이 들기 때문에 짧은 요청이 많은 워크로드에서는 오히려 역효과가 날 수 있다.
AI 게이트웨이 시장은 LiteLLM, Portkey, OpenRouter, AWS API Gateway 등 경쟁자가 많고, 오픈소스 프로젝트로서 장기 유지보수 지속성은 미지수다.

## 인사이트

AI 게이트웨이는 다중 모델 전략을 운영하는 조직에서 필수 인프라로 자리잡고 있다.
특정 제공자 장애 시 자동 전환, 비용 최적화를 위한 모델 라우팅, 사용량 추적이 단일 레이어에서 처리되면 애플리케이션 코드 복잡도를 크게 낮출 수 있다.
Bifrost가 MCP를 네이티브로 지원한다는 점은 에이전트 워크로드가 늘어나는 환경에서 차별화 요소가 될 수 있다.
