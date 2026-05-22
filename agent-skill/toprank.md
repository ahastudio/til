# Toprank

<https://github.com/nowork-studio/toprank>

## 소개

Toprank는 [NotFair](https://notfair.co)에서 만든 Claude Code 공식 플러그인으로,
AI 에이전트가 Google Search Console, Google Ads, Meta Ads(Facebook + Instagram)에
직접 접근할 수 있도록 한다.
“대시보드가 아니라 데이터 기반 결정(Data-driven decisions, not dashboards)”을 표방하며,
광고 낭비 발견, 랭킹 저하 원인 분석, 크리에이티브 피로도 진단 등을 자연어 명령 한 줄로 처리한다.

Claude Code에서 두 줄로 설치할 수 있다.

```text
/plugin marketplace add nowork-studio/toprank
/plugin install toprank@nowork-studio
```

Google Ads와 Meta Ads 연결은 별도 API 키 없이 OAuth 2.1로 진행된다.
첫 연결 시 브라우저가 열려 notfair.co에 로그인하면 토큰이 OS 키체인에 저장된다.

## 주요 스킬

### Google Ads

| 스킬                     | 설명                                                         |
| ------------------------ | ------------------------------------------------------------ |
| `google-ads-audit`       | 계정 감사 + 비즈니스 컨텍스트 구성. 7개 상태 차원 점수화.   |
| `google-ads`             | 캠페인 관리. 성과 조회, 키워드 최적화, 입찰/예산 조정.      |
| `google-ads-copy`        | RSA 카피 생성 + A/B 테스트. 글자 수 및 핀 위치 포함.        |
| `google-ads-landing`     | 랜딩 페이지 감사. 키워드·광고·페이지 간 연관성 분석.        |

### Meta Ads

| 스킬             | 설명                                                              |
| ---------------- | ----------------------------------------------------------------- |
| `meta-ads-audit` | 계정 감사. Pixel/CAPI 상태, Creative Health, Scaling Readiness 등 7개 차원. |
| `meta-ads`       | ROAS 분석, 빈도 분석, Learning Phase 트리아지, 오디언스 중첩 진단. |

### SEO

| 스킬                       | 설명                                                         |
| -------------------------- | ------------------------------------------------------------ |
| `seo-analysis`             | GSC 데이터 기반 전체 SEO 감사. 30일 액션 플랜 생성.         |
| `content-writer`           | E-E-A-T 가이드라인 기반 SEO 콘텐츠 작성.                    |
| `keyword-research`         | 키워드 발굴, 의도 분류, 토픽 클러스터, 콘텐츠 캘린더.       |
| `meta-tags-optimizer`      | 타이틀 태그, 메타 디스크립션, OG/Twitter 카드 + A/B 변형.   |
| `schema-markup-generator`  | JSON-LD 구조화 데이터(FAQ, HowTo, Article 등).               |
| `geo-optimizer`            | AI 검색엔진용 GEO 최적화. ChatGPT, Claude, Perplexity 등 대상. |

### Cross-Model

| 스킬     | 설명                                                         |
| -------- | ------------------------------------------------------------ |
| `gemini` | Google Gemini 2차 검토. 검토/도전/상담 세 가지 모드 지원.   |

## 아키텍처

```text
toprank/
├── .claude-plugin/
│   ├── plugin.json          <- 플러그인 메타데이터 (스킬 경로 명시)
│   └── marketplace.json     <- 레지스트리 항목
├── .mcp.json                <- NotFair MCP 서버 설정 (자동 구성)
├── google-ads/
├── meta-ads/
├── seo/
├── gemini/
├── openclaw/                <- 다중 사이트 자동화 에이전트 레이어
├── toprank-upgrade-skill/   <- 자가 업데이터
└── test/
```

각 스킬은 `SKILL.md` 파일과 선택적 `scripts/`, `references/` 디렉터리로 구성된다.
스킬은 `~~google-ads`, `~~search-console` 같은 플레이스홀더(placeholder) 패턴으로
외부 도구를 참조해, 특정 MCP 서버에 종속되지 않는 도구 불가지론적(tool-agnostic) 구조를 갖는다.

## MCP 서버

Google Ads와 Meta Ads는 독립적인 원격 MCP 서버로도 제공된다.

- **NotFair-GoogleAds:** `https://notfair.co/api/mcp/google_ads`
  - GAQL 쿼리를 최대 20개 병렬 실행하는 `runScript` 도구 포함
- **NotFair-MetaAds:** `https://notfair.co/api/mcp/meta_ads`
  - 뮤테이션 표면이 의도적으로 좁음(캠페인 생성·오디언스 편집·크리에이티브 업로드 제외)

## 분석

Toprank는 Claude Code의 플러그인 생태계가 어떻게 전문화된 도메인 도구로 확장되는지를
보여주는 좋은 사례다.
핵심 설계 결정은 다음 세 가지로 요약된다.

첫째, **스킬을 실행 단위로 삼는다.**
각 스킬은 `SKILL.md`라는 텍스트 파일로 정의된 지시문이다.
스크립트나 바이너리가 아니라, 에이전트가 읽고 따르는 명세서(specification)다.
이 구조 덕분에 기여 장벽이 낮고, 도구 업그레이드 없이 행동을 수정할 수 있다.

둘째, **커넥터를 플레이스홀더로 추상화한다.**
`~~google-ads`, `~~search-console` 같은 패턴은 실제 MCP 서버 이름을 숨긴다.
동일한 스킬이 NotFair 서버와 Google 공식 MCP 서버 모두에서 작동할 수 있다.
이는 스킬을 특정 벤더에 종속시키지 않는 유연한 설계다.

셋째, **돌연변이 표면을 의도적으로 제한한다.**
Meta Ads 서버는 캠페인 생성, 오디언스 편집, 크리에이티브 업로드를 프로그래밍 방식으로
지원하지 않는다. 이를 요청하면 Meta Ads Manager로 유도한다.
AI 에이전트의 무분별한 자동 변경을 막는 안전 설계다.

## 비평

Toprank의 접근법은 흥미롭지만 몇 가지 긴장이 있다.

**도구 불가지론과 실제 경험의 간극.** `~~google-ads` 플레이스홀더가 우아하게 보이지만,
실제로 NotFair가 아닌 다른 MCP 서버로 잘 작동하는지는 확인하기 어렵다.
오픈소스 생태계에서 “이론상 호환”과 “실제 작동”은 다른 문제다.

**SKILL.md 방식의 취약성.** 에이전트가 텍스트 지시문을 “읽고 따른다”는 전제는
모델마다 다르게 해석될 수 있다.
같은 `SKILL.md`가 Claude Opus와 Haiku에서 다른 결과를 낼 수 있다.
이를 보완하기 위한 `test/` 디렉터리가 있지만, LLM 판단 기반 평가(LLM-judge eval)가
얼마나 신뢰할 수 있는지는 열린 문제다.

**OpenClaw 레이어의 복잡성.** README는 “완전 자동화 SEO 에이전트”를 미래로 제시하지만,
cron 작업을 설정하고 다중 사이트 상태를 관리하는 것은 상당한 운영 부담을 수반한다.
“30초 설치”라는 입구와 “완전 자동화 에이전트”라는 출구 사이의 복잡성 점프가 크다.

## 인사이트

### 스킬 파일이 곧 코드다

Toprank의 가장 중요한 설계 철학은 `SKILL.md`를 실행 가능한 명세서로 취급한다는 점이다.
전통적인 소프트웨어에서 기능을 추가하려면 코드를 작성하고, 컴파일하고, 배포해야 한다.
반면 Toprank의 스킬은 텍스트 파일 하나다.
이 파일을 에이전트가 읽고 그 지시에 따라 행동한다.

이 패러다임이 성립하려면 에이전트가 자연어 지시를 충분히 신뢰할 수 있게 따라야 한다.
현재 수준의 LLM은 이 역할을 상당 부분 수행할 수 있다.
하지만 지시의 명확성, 모호성 처리, 엣지 케이스 대응은 여전히 스킬 작성자의 책임이다.
결국 “스킬을 잘 쓰는 것”이 새로운 형태의 프로그래밍이 된다.

이는 코드베이스의 단위가 함수나 클래스에서 지시문(instruction)으로 이동하는 흐름과 맞닿아 있다.
프롬프트 엔지니어링이 단순 기교가 아니라 소프트웨어 개발의 핵심 역량이 되는 세계의 모습이다.

### MCP 플러그인 생태계의 성숙

Toprank는 Claude Code가 단순한 코딩 보조 도구를 넘어 플러그인 생태계를 가진 플랫폼으로
발전하고 있음을 보여준다.
`/plugin marketplace add nowork-studio/toprank` 명령은 마치 `npm install`처럼 작동한다.
서드파티 개발자가 Claude Code 위에서 전문화된 도메인 도구를 만들고 배포할 수 있는 구조다.

이 생태계에서 MCP 서버는 도구의 실행 백엔드를 담당하고,
`SKILL.md`는 에이전트의 행동 지침을 담당한다.
둘의 분리는 깔끔하다.
스킬 개발자는 API 서버를 운영할 필요 없이 텍스트 파일만 작성하면 되고,
MCP 서버 제공자는 스킬 로직을 신경 쓰지 않아도 된다.

향후 이 생태계가 성숙하면, 특정 도메인(법률, 의료, 금융, 광고)에 특화된
수십 개의 플러그인이 공존하는 마켓플레이스가 형성될 것이다.
Toprank는 그 초기 형태를 보여주는 선례다.

### AI 에이전트의 안전한 뮤테이션 설계

Toprank의 Meta Ads 서버가 뮤테이션 표면을 의도적으로 좁게 유지한다는 점은
AI 에이전트 설계에서 중요한 원칙을 시사한다.
AI가 자동으로 캠페인을 만들고 오디언스를 편집할 수 있다면, 잘못된 판단 하나가
수백만 원의 광고비 손실로 이어질 수 있다.

이를 방지하기 위해 Toprank는 읽기(read)와 안전한 쓰기(safe write)는 허용하되,
위험한 쓰기(risky write)는 인간에게 돌려보낸다.
이는 “에이전트가 할 수 있는 것”과 “해야 하는 것”을 구분하는 신중한 접근이다.
기술적으로 가능한 기능을 의도적으로 구현하지 않는 결정이다.

AI 에이전트가 실제 비즈니스 시스템에 통합될수록, 이런 “의도적 제한”의 설계가
제품 신뢰성의 핵심이 된다.
“모든 것을 자동화”하는 에이전트보다, “안전한 것만 자동화하고 위험한 것은 사람에게 묻는”
에이전트가 실제 업무 환경에서 더 오래 살아남는다.

### GEO: SEO의 다음 단계

Toprank에 포함된 `geo-optimizer` 스킬은 생성형 AI 검색엔진 최적화(Generative Engine
Optimization, GEO)를 다룬다.
ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews 각각의 인용 방식에 맞춰
콘텐츠를 최적화하는 도구다.
이는 검색 패러다임의 전환을 반영한다.

전통적인 SEO는 Google 알고리즘이 페이지를 어떻게 크롤링하고 순위를 매기는지에
초점을 뒀다.
GEO는 AI가 질문에 답할 때 어떤 출처를 인용하는지에 초점을 둔다.
이 두 목표는 겹치는 부분도 있지만, 최적화 방향이 다를 수 있다.

예를 들어, AI 검색엔진은 구조화되고 사실 확인이 가능한 문장을 선호하는 경향이 있다.
반면 전통적인 SEO는 길고 포괄적인 롱폼 콘텐츠를 선호했다.
GEO를 위한 콘텐츠는 더 짧고 명확하며 인용 가능한 형태를 지향할 수 있다.
Toprank가 이 영역을 스킬로 포함한 것은, 이 전환이 이미 실용적인 도구가 필요한 수준에
도달했음을 의미한다.
