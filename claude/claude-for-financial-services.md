# Claude for Financial Services

<https://github.com/anthropics/financial-services>

HN 토론: <https://news.ycombinator.com/item?id=44576312> (213점, 114개 댓글)

## 소개

Anthropic이 오픈소스로 공개한 금융 서비스 특화 AI 레퍼런스 저장소다.
투자은행, 주식 리서치, 사모펀드, 자산관리, 펀드 운용 등 주요 금융 워크플로우를 위한 에이전트, 스킬, MCP 커넥터를 제공한다.
Apache 2.0 라이선스로 공개 직후 19k 스타, 2.5k 포크를 기록했다.

## 에이전트

11개의 명명된 에이전트가 포함된다.

| 에이전트             | 역할                                          |
| -------------------- | --------------------------------------------- |
| Pitch Agent          | Comps, 선례거래, LBO → 브랜드 피치덱 작성    |
| Meeting Prep Agent   | 클라이언트 미팅 전 브리핑 팩 작성            |
| Market Researcher    | 섹터·테마 → 산업 개요, 경쟁 환경, 아이디어  |
| Earnings Reviewer    | 어닝콜 + 공시 → 모델 업데이트 → 노트 초안   |
| Model Builder        | DCF, LBO, 3-statement, comps를 Excel에 구현  |
| Valuation Reviewer   | GP 패키지 수집, 평가 템플릿 실행, LP 보고서  |
| GL Reconciler        | 계정 잔액 차이 발견 및 근본 원인 추적        |
| Month-End Closer     | 충당금, 이월, 편차 설명                      |
| Statement Auditor    | LP 배포 전 재무제표 감사                     |
| KYC Screener         | 온보딩 문서 파싱, 규칙 엔진 실행             |

## MCP 커넥터

11개 금융 데이터 제공자와 MCP로 통합된다: Daloopa, Morningstar, S&P Global(Kensho), FactSet, Moody's, MT Newswires, Aiera, LSEG, PitchBook, Chronograph, Egnyte.

## 아키텍처

```text
plugins/
  agent-plugins/         에이전트 11개 (자체 포함)
  vertical-plugins/      버티컬 7개 (financial-analysis, investment-banking, ...)
  partner-built/         LSEG, S&P Global 제공
managed-agent-cookbooks/ Claude Managed Agents API 배포용
claude-for-msft-365-install/  Microsoft 365 추가 기능
scripts/                 배포·검증·오케스트레이션
```

핵심 플러그인은 `financial-analysis`로, 모든 데이터 커넥터를 중앙 집중식으로 관리하고 DCF·LBO·3-statement·comps 등 핵심 금융 분석 스킬을 포함한다.

## 설치

Claude Code CLI:

```bash
claude plugin marketplace add anthropics/claude-for-financial-services
claude plugin install financial-analysis@claude-for-financial-services
claude plugin install pitch-agent@claude-for-financial-services
```

Managed Agents API 배포:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

## 분석

이 저장소는 단순 프롬프트 모음이 아니라 MCP 커넥터, 스킬, 에이전트, 오케스트레이션 스크립트까지 갖춘 프로덕션 레퍼런스 아키텍처다.
금융 데이터 제공자 11곳이 MCP로 통합된 것은 Anthropic이 금융 업계와 맺은 파트너십 관계를 드러낸다.
70개 이상의 스킬과 50개 이상의 명령어는 실제 IB·리서치 워크플로우를 상당히 구체적으로 모델링하고 있다.

[GeekNews 댓글](https://news.hada.io/topic?id=29372)에서는 "금융주가 폭락할 때인가"라는 반응이 나왔다.
자동화 범위가 어닝 리뷰, 피치덱 작성, KYC 심사까지 포괄하기 때문에 금융 분야 화이트칼라 업무 대체 가능성에 대한 반응이다.

## 비평

저장소는 "투자 권고, 거래 체결, 위험 인수를 하지 않는다"며 모든 출력물은 전문가의 검토가 필요한 초안이라고 명시한다.
그러나 GL Reconciler, Statement Auditor처럼 수치 정확성이 중요한 워크플로우에서 LLM 환각이 발생할 경우 후속 검토자가 이를 잡아낼 수 있을지는 별개 문제다.
레퍼런스 구현이므로 실제 배포 전 조직별 규정 준수 검토와 데이터 거버넌스 설계가 선행돼야 한다.

jasonthorsness[^jasonthorsness]는 코드 생성 분야에서는 린팅·컴파일·테스트라는 검증 체계가 AI 오류를 잡아내지만, 금융 분야에는 이에 상응하는 자동화된 검증 메커니즘이 없다는 점을 지적했다.
작은 세부 사항에 결과가 크게 달라지는 두 영역이지만, 오류를 탐지하는 방식은 근본적으로 다르다.

injidup[^injidup]은 아버지에게 들은 말을 인용했다.
"카지노·경마장·주식거래에서 이기는 시스템을 파는 사람은 사기꾼이다. 시스템이 실제로 작동한다면 그것을 팔지 않았을 것이다."
금융 AI 도구에 대한 가장 고전적이면서도 날카로운 반론이다.

gyosko[^gyosko]는 한 문장으로 핵심을 찔렀다: "바이브 투자가 온다, 그리고 그것은 많은 사람들을 가난하게 만들 것이다."
바이브 코딩이 검증되지 않은 코드를 프로덕션에 올린다면, 바이브 투자는 검증되지 않은 분석을 금융 결정에 적용한다.

osn9363739[^osn9363739]는 금융 업계의 현실을 더 냉소적으로 그렸다.
금융 서비스에서 "숫자로 원하는 이야기를 어떻게 만드는가"가 핵심인 경우가 많다는 것이다.
AI가 분석의 질을 높이는 것이 아니라 원하는 내러티브를 더 빠르게 생산하는 도구로 쓰일 가능성을 지적한다.

## 인사이트

Anthropic이 직접 수직 산업 특화 레퍼런스를 오픈소스로 공개한 것은 API 판매 전략을 넘어 생태계 구축 전략으로의 전환을 보여준다.
MCP가 AI 에이전트와 데이터 소스를 연결하는 표준 레이어로 자리잡으면, 이런 레퍼런스 아키텍처가 각 산업의 AI 도입 템플릿이 될 수 있다.
금융 서비스는 규제·데이터·워크플로우 복잡도가 높아 AI 도입 장벽이 크지만, 그만큼 자동화 효과도 크다는 점에서 가장 먼저 공략할 만한 수직 시장이다.

mildlyhostileux[^mildlyhostileux]는 이것이 코딩 분야의 Claude Code와 같은 패턴이라고 짚었다.
향상된 모델에 좋은 통합을 더하는 전략이지만, 금융 업무는 여전히 Excel과 PowerPoint 중심이라는 현실적 제약을 함께 지적했다.
초기 파일럿에 참여한 Bridgewater, NBIM, AIG, CBA 같은 기관들이 분석가 생산성 향상을 보고했다는 점은 실제 검증이 진행 중임을 보여준다.

---

[^jasonthorsness]: <https://news.ycombinator.com/item?id=44576713>
[^injidup]: <https://news.ycombinator.com/item?id=44579256>
[^gyosko]: <https://news.ycombinator.com/item?id=44576606>
[^osn9363739]: <https://news.ycombinator.com/item?id=44577713>
[^mildlyhostileux]: <https://news.ycombinator.com/item?id=44579188>
