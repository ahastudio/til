# GoScrapy — Go 기반 초고속 웹 스크래핑 프레임워크

<https://github.com/tech-engine/goscrapy>

## 소개

GoScrapy는 Python의 Scrapy 아키텍처를 Go로 재구현한 고성능 웹 스크래핑
프레임워크다. Go의 동시성 모델을 활용하여 병렬 스크래핑을 지원하며,
구조화된 워크플로우로 요청, 미들웨어, 데이터 파이프라인을 처리한다.

## 아키텍처

```text
Spider → Engine → Scheduler → Worker → Middleware → HTTP Client → Response
                                                                      ↓
                                                               Spider Callback
                                                                      ↓
                                                               Pipelines → CSV/JSON/MongoDB/...
```

- **Spider**: 요청 생성 및 응답 파싱 로직 작성
- **Engine**: 스케줄링 및 워크 분배 조율
- **Worker Pool**: Go 고루틴 기반 병렬 실행
- **Middleware**: 요청/응답 처리 레이어 (재시도, 헤더, 쿠키 등)
- **Pipeline**: 데이터 내보내기 (CSV, JSON, MongoDB, Google Sheets, Firebase)

## 설치 및 시작

Go 1.22 이상 필요:

```bash
go install github.com/tech-engine/goscrapy/cmd/...@latest
goscrapy startproject my_project
```

`startproject` 명령으로 프로젝트 스캐폴딩을 자동 생성한다.

## 프로젝트 구조

생성된 프로젝트는 관심사를 명확히 분리한다:

- **`settings.go`**: 미들웨어와 파이프라인 설정
- **`spider.go`**: 파싱 로직 (데이터 추출에 집중)
- **`base.go`**: 엔진 초기화 보일러플레이트

## 주요 기능

- Go 고루틴 기반 병렬 스크래핑
- 지수 백오프(exponential backoff) 자동 재시도
- 타깃별 독립 쿠키 세션
- CSS 셀렉터 및 XPath 체이닝
- CLI 프로젝트 스캐폴딩 (`goscrapy startproject`)
- 복수 데이터 내보내기 파이프라인

## 라이선스 및 상태

v0.x 활성 개발 단계. BSL(Business Source License) 사용 — 상업적 제품에서
자유롭게 사용 가능하지만 프레임워크를 경쟁 서비스로 재판매하는 것은
제한된다.

## 분석

### Scrapy를 Go로 옮긴 이유

Python Scrapy는 성숙한 생태계를 가진 사실상의 표준 스크래핑 프레임워크다.
GoScrapy가 같은 아키텍처를 선택한 것은 두 가지를 노린다. 첫째, Python
Scrapy 사용자에게 친숙한 진입점을 제공한다. 둘째, Go의 네이티브 동시성
(고루틴, 채널)을 활용하여 Python GIL(Global Interpreter Lock) 한계를
극복한다.

Python Scrapy에서 고성능 스크래핑은 Twisted 비동기 프레임워크에 의존한다.
Go에서는 언어 자체가 경량 스레드(고루틴)를 네이티브로 지원하므로,
동일한 목적을 더 단순한 코드로 달성할 수 있다.

### 파이프라인의 다양성

CSV, JSON 외에 MongoDB, Google Sheets, Firebase 파이프라인을 기본 제공하는
것은 실용적이다. 데이터 웨어하우스, 스프레드시트 기반 분석, 실시간 데이터베이스
모두 별도 통합 없이 바로 연결할 수 있다.

## 비평

### v0.x의 위험

v0.x 단계는 API 안정성을 보장하지 않는다. 프로덕션 파이프라인에서
GoScrapy를 사용하면 버전 업그레이드 시 브레이킹 체인지를 직접 처리해야
한다. BSL 라이선스와 맞물려 대규모 채택 전에 v1.0 안정화를 기다리는 것이
합리적일 수 있다.

### BSL 라이선스의 모호성

“경쟁 서비스로 재판매 제한”이 명확하게 정의되지 않으면 기업 사용자에게
법적 불확실성을 만든다. Elasticsearch, HashiCorp Terraform도 BSL로
전환하면서 커뮤니티 포크(OpenSearch, OpenTofu)가 발생했다. GoScrapy가
같은 경로를 걸을지 주시할 필요가 있다.

### Scrapy와의 기능 격차

Python Scrapy의 성숙한 생태계 — splash(JavaScript 렌더링), scrapy-splash,
scrapy-playwright 등 — 에 비해 GoScrapy는 아직 JavaScript 렌더링 통합이
없는 것으로 보인다. SPA(Single Page Application) 스크래핑이 필요한
경우 별도 해결이 필요하다.

## 인사이트

### Go는 스크래핑에서 Python을 대체할 수 있는가

Python은 스크래핑 생태계에서 압도적 우위를 가지고 있다. Beautiful Soup,
Scrapy, Playwright, httpx — 도구 다양성과 커뮤니티 크기에서 Go가 따라가기
어렵다.

그러나 특정 시나리오에서 Go는 명확한 우위가 있다. 대규모 크롤링 인프라,
고처리량이 요구되는 데이터 수집 파이프라인, 서버 리소스를 최소화해야
하는 환경. 이런 경우 Python의 메모리 오버헤드와 GIL 제약이 병목이 된다.

GoScrapy는 Python에서 Go로의 전환을 고려하는 팀에게 완만한 학습 곡선을
제공한다. 아키텍처가 익숙하면 언어만 바꾸는 것이 훨씬 쉽다.
이것이 GoScrapy의 진짜 포지셔닝이다 — Python 스크래핑 생태계 전체와
경쟁하는 것이 아니라 **마이그레이션 경로**를 제공하는 것.

### 스크래핑의 규제 환경이 빠르게 변한다

기술적 특성과 별개로, 웹 스크래핑의 법적, 윤리적 환경이 복잡해지고 있다.
X(구 Twitter), LinkedIn 등이 스크래핑을 적극적으로 차단하고 소송을 제기하고
있다. `robots.txt`를 준수하는 것이 기본이지만, 이것만으로 법적 보호가
충분하지 않은 경우도 생기고 있다.

GoScrapy 같은 프레임워크를 사용할 때는 **무엇을 스크래핑하느냐**가
**어떻게 스크래핑하느냐**만큼 중요해졌다. 미들웨어로 속도 제한과
정중한 크롤링(polite crawling)을 구현하는 것이 기술적 선택이 아니라
법적 필수 요건이 되고 있다.

### 오픈소스 스크래핑 생태계의 BSL 전환 트렌드

HashiCorp, Elastic 등 주요 오픈소스 프로젝트의 BSL 전환은 오픈소스 비즈니스
모델의 지속 가능성에 대한 질문을 다시 제기했다. GoScrapy도 처음부터 BSL을
선택했다.

이것은 오픈소스 프리라이더 문제에 대한 현실적인 대응이다. 누군가 GoScrapy를
클라우드 스크래핑 서비스로 포장해서 팔면 원 개발자는 아무 이익이 없다.
BSL은 이를 방지한다. 그러나 이 선택은 커뮤니티 생태계 형성을 느리게 할
수 있다. 기여자 유치가 어려워지고, 포크 가능성이 항상 열려 있다.

**도구의 장기적 건강은 기술 품질만큼이나 라이선스 전략에 달려 있다.**
GoScrapy가 커뮤니티를 키울 것인지 상업 제품으로 수렴할 것인지는 두고 봐야 한다.
