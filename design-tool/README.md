# 디자인 도구: 캔버스 위에서 에이전트와 함께 쓰는 도구들

## 소개

이 폴더는 캔버스에서 화면을 그리고, 에이전트가 MCP와 CLI로 그 캔버스를 읽고 쓰는
디자인 도구를 모은다.
Figma 자체를 다룬 문서는 `figma/`에 있고,
이 폴더는 Figma의 대안이나 경쟁자로 나온 도구를 다룬다.
각 도구의 사용법과 분석은 해당 문서에 있으며,
이 문서는 도구를 나란히 놓고 보는 짧은 비교만 담는다.

## 문서 목록

| 도구                | 문서                                         | 한 줄 요약                                                           |
| ------------------- | -------------------------------------------- | -------------------------------------------------------------------- |
| Penpot              | [penpot.md](penpot.md)                       | 서버가 있는 팀용 오픈소스 디자인·코드 협업 플랫폼                    |
| open-pencil         | [open-pencil.md](open-pencil.md)             | Figma `.fig` 파일을 그대로 여는 로컬 우선 오픈소스 편집기            |
| ZSeven-W/openpencil | [openpencil-zseven.md](openpencil-zseven.md) | 에이전트가 쓰는 JSON 디자인 형식과 Rust 코어를 가진 벡터 디자인 도구 |
| pen.dev             | [pen-dev.md](pen-dev.md)                     | IDE 안에서 시작해 독립 캔버스가 된 에이전트용 상용 디자인 도구       |
| Paper               | [paper.md](paper.md)                         | HTML과 CSS 위에 만든 에이전트용 디자인 캔버스                        |

open-pencil과 ZSeven-W/openpencil은 이름이 같지만 서로 다른 프로젝트다.

## 간단 비교

| 항목        | Penpot                           | open-pencil                        | ZSeven-W/openpencil              | pen.dev                                     | Paper                                                                                                                                                        |
| ----------- | -------------------------------- | ---------------------------------- | -------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 핵심 방향   | 서버가 있는 팀용 오픈소스 플랫폼 | Figma 파일을 여는 로컬 우선 편집기 | 에이전트용 JSON 형식과 Rust 코어 | 에이전트가 캔버스에서 직접 그리는 상용 도구 | HTML과 CSS 캔버스                                                                                                                                            |
| 파일        | `.penpot`(ZIP 안의 JSON)         | `.fig`를 읽고 쓰며 `.pen`을 연다   | `.op`(JSON), `.fig` 가져오기     | `.pen`(JSON), `.fig` 가져오기               | HTML과 CSS 기반                                                                                                                                              |
| 데이터 위치 | 서버(셀프 호스팅 지원)           | 사용자의 기기                      | 사용자의 기기                    | 로컬 편집기와 웹 버전                       | 데스크톱 앱(macOS, Windows, Linux)과 브라우저. 파일 저장 위치는 Paper의 홈페이지, 문서, 다운로드, 약관 페이지에 적혀 있지 않음[^paper-tos][^paper-downloads] |
| 라이선스    | MPL-2.0                          | MIT, Cloud만 Apache-2.0            | MIT                              | 오픈소스 주장이 없음                        | 비공개 소프트웨어. 소스를 주지 않고 약관이 리버스 엔지니어링을 금지함[^paper-tos]                                                                            |
| 에이전트 면 | 공식 MCP 서버                    | CLI, MCP, 내장 채팅                | MCP, CLI `op`, 에이전트 팀       | MCP, WebMCP, CLI                            | MCP                                                                                                                                                          |

Penpot, open-pencil, ZSeven-W/openpencil,
pen.dev 열의 값은 `open-pencil.md`의 비교표를 줄여 옮긴 것이고,
Paper 열은 `paper.md`에서 가져왔다.
각 칸은 프로젝트가 자기 문서에서 한 주장이며,
이 폴더의 문서가 모두 직접 써 보고 확인한 것은 아니다.

## 비용 비교: Figma 기준

기준선은 Figma이고, 정가는 모두 각 도구의 가격 페이지에 적힌 값이다.
이 폴더의 문서가 결제를 시험한 것은 아니며,
모델 비용과 세금과 연간 할인은 뺀 정가다.

### 요금제와 돈이 매겨지는 단위

| 도구                | 무료로 쓸 수 있는 것                                              | 유료 정가                                                                                                      | 돈이 매겨지는 단위              |
| ------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Figma               | Starter, MCP 도구 호출 월 20회[^figma-pricing]                    | 좌석 월 $3~$90, AI 크레딧[^figma-pricing]                                                                      | 좌석 종류, MCP 호출 한도        |
| Penpot              | Professional(구성원 8명, 저장 10GB), 셀프 호스팅[^penpot-pricing] | Unlimited 편집자당 월 $7(월 $175 상한), Enterprise 구성원당 월 $25, Private Server 연 $50,000[^penpot-pricing] | 편집자 수, 저장 용량, 운영 항목 |
| open-pencil         | 편집기, CLI, MCP 전부                                             | 자기 AI 공급자의 토큰, Cloud 가격은 미공개[^os-roadmap]                                                        | 모델 사용량                     |
| ZSeven-W/openpencil | 편집기, CLI, MCP 전부                                             | 자기 AI 공급자의 토큰                                                                                          | 모델 사용량                     |
| pen.dev             | 편집기, CLI, MCP 무제한, 에이전트 월 5일[^pen-pricing]            | Pro 월 $16, Ultra 월 $48[^pen-pricing]                                                                         | 에이전트 일수와 병렬도          |
| Paper               | 팀 전체 초대, MCP 도구 호출 주 100회[^paper-pricing]              | Pro 편집자당 월 $20(연 결제 시 $16)[^paper-pricing]                                                            | 편집자 수, MCP 호출 한도        |

오픈소스 두 도구의 모델 비용은 공급자와 모델에 따라 다르며,
호환성 표에서 가장 싼 권장 모델은 입출력 100만 토큰당 0.15~0.35유로
수준이다.[^os-byok]

### 열 명짜리 팀의 한 달 정가

이 계산은 `pen-dev.md`의 가정을 그대로 쓴다.
설계자 다섯과 개발자 다섯 모두 편집 권한이 필요하고, 정가만 더한 값이다.
Paper 행은 이 폴더에서 같은 가정으로 새로 더한 것이다.

| 도구 / 요금제                 | 계산                        | 한 달 합계(USD) |
| ----------------------------- | --------------------------- | --------------- |
| Figma Professional            | Full 5명 $16 + Dev 5명 $12  | $140            |
| Figma Organization(연간 청구) | Full 5명 $55 + Dev 5명 $25  | $400            |
| Figma Enterprise(연간 청구)   | Full 5명 $90 + Dev 5명 $35  | $625            |
| pen.dev Pro                   | 10명 $16                    | $160            |
| pen.dev Ultra                 | 10명 $48                    | $480            |
| Paper Pro                     | 편집자 10명 $20             | $200            |
| Penpot Unlimited              | 편집자 5명 $7(월 $175 상한) | $35             |
| Penpot Enterprise             | 구성원 10명 $25             | $250            |
| Penpot Private Server         | 연 $50,000                  | 약 $4,167       |
| open-pencil, ZSeven           | 라이선스 비용 없음          | $0              |

Penpot Unlimited는 가격 페이지가 편집자의 단위를 정의하지 않아,
개발자를 편집자로 세면 값이 달라진다.[^penpot-pricing]
Figma는 좌석 종류로 값을 나누고 pen.dev와 Paper는 모든 편집자에게 같은
값을 받는다.
이 문서의 해석으로는 라이선스 비용만 보면 오픈소스 쪽이 가장 싸고,
그 차이를 메우는 것은 운영 부담과 성숙도다.

### 에이전트 호출 한도

에이전트 시대에 새로 생긴 가격 축은 MCP 호출 한도다.

| 도구                | MCP 호출 한도                                                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Figma               | Starter 월 20회, Professional 일 200회와 분당 10회, Organization 일 200회와 분당 15회, Enterprise 일 600회와 분당 20회[^figma-pricing] |
| Paper               | 무료 주 100회, Pro 주 100만 회[^paper-pricing]                                                                                         |
| pen.dev             | 모든 요금제에서 디자인하는 동안 무제한[^pen-pricing]                                                                                   |
| Penpot              | 서버는 무료이고 오픈소스라고 하지만 호출 한도나 가격은 소개 페이지에 없음[^penpot-mcp]                                                 |
| open-pencil, ZSeven | 로컬 도구라서 호출 한도 자체가 없음                                                                                                    |

에이전트가 하루에 수백 번 도구를 부르는 작업 방식에서는 Figma의 호출 한도에 가장 먼저 걸린다.
Paper의 무료 요금제 주당 100회도 실제 화면 하나를 만드는 데 들어가는 호출 수가
요금제 페이지에 없어서, 체험용 한도로 읽힌다.
이 두 문장은 이 문서의 해석이다.

### 무료라는 말의 네 가지 뜻

무료는 도구마다 다른 뜻으로 쓰이고, 네 뜻은 서로 겹치지 않는다.
라이선스가 자유롭다는 뜻(Penpot, open-pencil, ZSeven),
무료 요금제가 있다는 뜻(Figma Starter, Penpot Professional, pen.dev Free,
Paper 무료), 로컬에서 서버 없이 돈다는 뜻(open-pencil, ZSeven),
자기 모델 비용만 낸다는 뜻이다.
pen.dev는 편집기와 CLI와 MCP를 무료 단계에서 제한 없이 주지만 에이전트와
디자인하는 날을 월 5일로 막고, 자기 키를 연결해도 이 한도는 풀리지
않는다.[^pen-pricing]
무료의 범위가 편집기에 있는지 에이전트에 있는지가 도구마다 다르다.

## 고르는 기준

- 기존 Figma 파일을 그대로 열어야 하면 open-pencil, 가져오기로 충분하면 ZSeven이나 pen.dev를 먼저 본다.
- 서버와 팀 협업이 필요하고 소스가 열려 있어야 하면 Penpot이다.
- 에이전트가 하루에 수백 번 도구를 부른다면 Figma와 Paper는 호출 한도를, pen.dev는 월 에이전트 일수를 먼저 본다.
- 라이선스 비용 0과 운영 부담의 교환을 받아들일 수 있으면 open-pencil과 ZSeven이다.

이 기준은 각 문서의 결론을 줄인 것이고,
결과는 자기 파일과 작업으로 시험해야 확정된다.

---

[^figma-pricing]: Figma, [Pricing](https://www.figma.com/pricing/)

[^penpot-pricing]: Penpot, [Penpot Pricing | From Professional to Enterprise Plans](https://penpot.app/pricing)

[^pen-pricing]: pen.dev, [Pricing](https://www.pen.dev/pricing)

[^paper-pricing]: Paper, [Pricing • Paper](https://paper.design/pricing)

[^paper-tos]: Paper, [Terms of Service](https://paper.design/legal/tos), 2026-10-11

[^paper-downloads]: Paper, [Downloads](https://paper.design/downloads)

[^penpot-mcp]: Penpot, [Penpot MCP Server](https://penpot.app/penpot-mcp-server)

[^os-roadmap]: OpenPencil, [Roadmap](https://openpencil.dev/development/roadmap)

[^os-byok]: OpenPencil, [BYOK provider and model compatibility](https://openpencil.dev/programmable/byok-provider-compatibility)
