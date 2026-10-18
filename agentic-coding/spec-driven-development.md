# Spec-Driven Development

## 개요

Spec-Driven Development(SDD)는 AI 코딩 에이전트에게 코드 작성을 맡기기 전에
무엇을 만들지를 문서로 먼저 쓰고,
그 문서를 에이전트가 계획, 작업 분해, 구현, 검증의 기준으로 삼게 하는
개발 방식이다.
GitHub 블로그에서 Spec Kit을 소개한 Den Delimarsky는
이를 코드가 기준이던 방식에서 의도가 기준인 방식으로 옮겨 가는 것이라고
설명했다.[^github-blog]

다만 이 용어는 아직 정의가 확립되지 않았다.
Thoughtworks 기술 레이더는 용어의 정의가 여전히 바뀌는 중이라고 적었고,
대체로 구조화된 기능 명세에서 시작해
여러 단계에 걸쳐 작은 단위로 나눠 가는 흐름을 가리킨다고만 정리했다.[^radar]
그래서 “SDD를 쓴다”는 말은 도구마다,
팀마다 서로 다른 것을 뜻할 수 있다.

[병목은 결코 코드가 아니었다](bottleneck-was-never-the-code.md)가 지적하듯,
코드 작성 비용이 0에 수렴하면 병목은 무엇을 만들지 정밀하게 정의하는
단계로 옮겨 간다.
SDD는 이 진단을 워크플로로 만든 시도다.
이 문서는 SDD의 수준 구분, 앞선 기법과의 관계, 주요 도구,
연구와 실무 보고, 그리고 그를 둘러싼 비판과 논쟁을 차례로 정리한다.

## 세 가지 수준

Birgitta Böckeler는 SDD 도구를 살펴보며
스펙을 언제까지 유지하고 코드보다 얼마나 우선하는지에 따라
세 수준으로 나눴다.[^bockeler]

| 수준           | 스펙의 역할                                         | 코드의 역할             |
| -------------- | --------------------------------------------------- | ----------------------- |
| spec-first     | 작업 전에 공들여 쓴 스펙을 그 작업에만 쓴다         | 작업 뒤에는 코드가 기준 |
| spec-anchored  | 작업이 끝난 뒤에도 남겨 이후 변경과 유지보수에 쓴다 | 스펙과 코드를 함께 관리 |
| spec-as-source | 사람은 스펙만 고치고 코드는 건드리지 않는다         | 코드는 생성물           |

이 구분이 중요한 이유는 비판이 대개 특정 수준을 겨누기 때문이다.
Kent Beck의 비판은 구현 전에 스펙 전체를 쓰는 spec-first 설명을 겨눴고,[^fowler]
Böckeler가 모델 기반 개발(MDD)과 비교하며 비판한 대상은
spec-as-source다.[^bockeler]
cc-sdd는 스펙을 계약으로 보면서도 코드가 계속 기준으로 남는다는
입장이어서 spec-anchored에 가깝다.[^cc-sdd]
반대로 Spec Kit의 철학 문서는 스펙이 코드를 섬기는 것이 아니라
코드가 스펙을 섬긴다고 적어 spec-as-source 쪽으로 기운다.[^spec-driven-md]

## 앞선 기법과의 관계

SDD 논쟁에는 오래된 기법의 이름이 자주 나온다.
아래는 출처가 직접 그 연결을 짚었거나,
SDD 도구가 그 기법을 그대로 가져다 쓰는 경우다.

### 워터폴과 Royce의 1970년 논문

SDD 비판에서 가장 자주 나오는 말은 “워터폴의 귀환”이다.
그런데 워터폴의 출처로 꼽히는 Winston Royce의 1970년 논문은
순차 모델을 권하지 않았다.
Royce는 그 개념을 믿지만 그대로 구현하면 위험하고 실패를 부른다고 썼고,
해법으로 전체를 두 번 만드는 단계를 제시했다.[^royce]
한편 그는 문서화를 매우 강조해,
문서가 곧 명세이자 설계라고까지 적었다.[^royce]
“명세가 곧 설계”라는 SDD의 주장과
“먼저 만들어 보고 배워야 한다”는 SDD 비판이
같은 논문 안에 함께 들어 있는 셈이다.

### EARS

Kiro가 요구사항 형식으로 쓰는 EARS(Easy Approach to Requirements Syntax)는
Alistair Mavin이 Rolls-Royce 동료들과 함께 제트엔진 제어 시스템의
감항 규정을 분석하다가 만들었고,
2009년 IEEE 요구공학 학회(RE'09)에서 처음 발표되었다.[^ears-wiki]
Mavin은 EARS를 자연어 요구사항을
부드럽게 제약하는 장치라고 설명한다.[^ears-mavin]
패턴은 키워드 없는 상시 요구사항, WHEN(이벤트), WHILE(상태),
WHERE(선택 기능), IF/THEN(원치 않는 상황)으로 나뉘고 서로 조합할 수 있다.
Airbus, Bosch, Honeywell, NASA, Siemens 등이 쓰고 있으며,
2025년부터 AI 기반 SDD 도구에 들어갔다.[^ears-wiki]

### 모델 기반 개발

OMG의 모델 기반 아키텍처(MDA)는 소프트웨어 명세를 모델로 표현하고,
플랫폼 독립 모델(PIM)을 여러 플랫폼에서 구현하는 구조를 제시했다.
목표는 핵심 애플리케이션을 끊임없이 바뀌는 기술에서 떼어 놓는 것이었다.[^mda]
Böckeler는 spec-as-source가 모델 기반 개발의 경직성과
LLM의 비결정성이라는 두 단점을 함께 가질 위험이 있다고 보았다.[^bockeler]
HN 사용자 twen_ty도 OpenSpec 스레드에서
90년대 UML 코드 생성과 무엇이 다르냐고 물었다.[^twen_ty]

### 계약에 의한 설계와 BDD

Bertrand Meyer의 계약에 의한 설계는 호출하는 쪽과 제공하는 쪽 사이의 계약을
사전조건, 사후조건, 불변식으로 정의한다.[^dbc]
Kiro의 버그 수정 방법론은 버그 조건과 사후조건을 먼저 정의하는데,[^kiro-bugfix]
이는 같은 개념을 버그 수정에 쓰는 것이다.
아래 실증 연구에서 다룰 Tufano 등의 실험도
사전조건과 사후조건을 테스트 생성의 근거로 썼다.[^tufano]

Dan North가 2006년에 소개한 BDD는 TDD에서 출발해
Given/When/Then 템플릿으로 동작을 기술한다.[^bdd]
Piskala의 개념 논문은 BDD 프레임워크부터 Spec Kit까지를
같은 범위에서 다룬다.[^piskala]

### 형식 명세

AWS 엔지니어들은 TLA+를 대형 실제 시스템 10개에 적용했고,
엔지니어들이 처음부터 배워 2~3주 안에 쓸 만한 결과를 냈다고 보고했다.[^tla]
TLA+ 같은 형식 명세는 스펙을 기계로 검사할 수 있다는 점에서
마크다운 스펙과 다르다.
뒤에서 다룰 Verified Spec-Driven Development는
이 형식 검증을 SDD 파이프라인 안에 넣으려는 시도다.[^vsdd]

## 주요 도구

### GitHub Spec Kit

GitHub는 2025년 9월 2일 Spec Kit을 오픈소스로 공개했다.[^github-blog]
처음 흐름은 `/specify`(사용자 경험 수준의 설명), `/plan`(기술 구현 전략),
`/tasks`(실행 가능한 작업 분해), 구현 순서였고,
각 단계는 다음으로 넘어가기 전의 확인 지점이었다.[^github-blog]
Microsoft 개발자 블로그의 Den Delimarsky 소개는 여기에
프로젝트가 타협하지 않을 원칙을 적는 `constitution.md`를 더하고,
이것이 워터폴식 계획이 아니라 생각을 버전 관리하는 것이라고 설명했다.[^ms-blog]

저장소의 `spec-driven.md`는 Spec Kit의 철학을 담은 문서다.
이 문서는 코드가 스펙을 섬긴다는 “권력의 역전”을 내세우고,
constitution에 라이브러리 우선, CLI 인터페이스 의무, 테스트 우선,
단순성(초기 구현은 프로젝트 3개 이하), 추상화 금지(프레임워크를 직접 사용),
통합 우선 테스트(목 대신 실제 데이터베이스) 같은 조항을 둔다.[^spec-driven-md]

Spec Kit 1.0.0은 2026년 8월 21일, 저장소 공개 1년 만에 나왔다.[^spec-kit-1]
지금의 README는 프로젝트마다 constitution을 한 번 만들고,
기능마다 specify, plan, tasks, implement, converge를 거치며,
converge가 수렴을 보고할 때까지 implement와 converge를 반복하라고 안내한다.
버그 수정과 아이디어 평가는
선택해서 붙이는 확장으로 분리되었다.[^spec-kit-readme]
1.1.0 릴리스에서는 핵심 명령이던 `taskstoissues`가 사용 중단 예정으로 바뀌고
GitHub 확장으로 옮겨졌다.[^spec-kit-releases]
저장소 `github/spec-kit`은 2025년 8월 21일에 만들어졌고,
2026년 10월 18일 확인 기준 스타 141,629개다.[^spec-kit-api]

### Kiro

AWS의 Kiro는 2025년 7월 14일 프리뷰로 공개되었다.[^kiro-intro]
한 줄짜리 요청에서 요구사항(사용자 스토리), 설계, 작업 목록을 차례로 만든다.
설계에는 데이터 흐름도, TypeScript 인터페이스, 데이터베이스 스키마,
API 엔드포인트가 들어간다.[^kiro-intro]
Kiro 개발자 NathanKP는 출시 HN 토론에서
이 방식이 Amazon 내부의 대형 프로젝트 프로세스에
바탕을 둔다고 설명했다.[^nathankp]
Kiro는 2025년 11월 17일 정식 출시되면서 스펙의 정확성을 확인하는
property-based testing과 Kiro CLI, 팀 요금제를 함께 내놓았다.[^kiro-ga]

Kiro의 스펙은 `requirements.md`(버그는 `bugfix.md`), `design.md`,
`tasks.md` 세 파일이고,
서로 독립적인 작업은 묶어서 병렬로 실행한다.[^kiro-specs]
요구사항은 EARS 형식으로 쓴다.[^kiro-feature]

```text
WHEN [조건 또는 이벤트] THE SYSTEM SHALL [기대 동작]
```

Kiro 문서는 Requirements-First와 Design-First 두 흐름을 두고,
버그 수정이나 탐색적 코딩에는 기능 스펙을 권하지 않는다.[^kiro-feature]
정확성 기능은 EARS 요구사항에서 속성을 뽑아
property-based testing을 돌리는데,
문서 스스로 이것이 증명이 아니라 정확성의 증거라고 밝힌다.[^kiro-correctness]
모든 작업에 공통으로 필요한 프로젝트 맥락은
`.kiro/steering/`의 `product.md`, `tech.md`,
`structure.md`가 맡고, `AGENTS.md`도 자동으로 읽는다.[^kiro-steering]
파일 저장, 도구 호출 전후 같은 이벤트에 셸 명령이나 에이전트 프롬프트를
자동으로 실행하는 훅도 있다.[^kiro-hooks]

버그 수정에는 별도 방법론이 있다.
Kiro 블로그는 에이전트가 사람보다 방어 코드를 거의 두 배 더 많이 넣는다고
지적하고,
버그 조건과 사후조건을 먼저 정의한 뒤
버그 조건에서는 사후조건을 만족하고(수정 속성)
나머지 입력에서는 동작이 그대로인지(보존 속성)를
property-based testing으로 확인하라고 권한다.
이 방식으로 Apache RocketMQ의 메모리 누수를 고쳤는데,
수정은 한 줄이었지만 코드 경로 다섯 개를 검증해야 했다.[^kiro-bugfix]

출시 1년 회고에 따르면 프리뷰 공개 5일 만에 10만 명 넘는 개발자가 써 봤고,
2025년 10월에 그 수가 두 배가 되었다.
고객 사례로는 LMU가 2개월 걸리던 Lambda 함수 500개 업데이트를 반나절에 끝냈고,
Siemens는 3~4개월 걸리던 서비스를 아키텍트 한 명이 2주 만에 만들었다고
소개한다.[^kiro-one-year]
모두 AWS가 직접 내놓은 사례다.

AWS는 2026년 4월 30일 Amazon Q Developer의 지원 종료를 발표했다.
신규 가입은 2026년 5월 15일에 막혔고,
IDE 플러그인과 유료 구독은 2027년 4월 30일에 지원이 끝난다.
AWS는 Kiro를 스펙 기반 개발을 위해 처음부터 만든 에이전트 개발 환경으로
소개하며 이전 대상으로 제시한다.[^q-eos]
Threads 사용자 cys_makin은 Kiro가 2026년 5월에 나왔다고 적었지만,[^cys-2]
2026년 5월은 Q Developer 신규 가입이 막힌 시점이고
Kiro의 프리뷰와 정식 출시는 2025년이다.

### Tessl

Tessl은 2025년 9월 23일 블로그에서 Spec Registry를 공개 베타로,
Tessl Framework를 비공개 베타로 내놓았다.
Registry에는 오픈소스 라이브러리 1만 개 이상의 스펙이 들어 있고,
스펙은 컴포넌트 스펙과 사용법 스펙으로 나뉜다.[^tessl]
CEO Guy Podjarny는 에이전트가 똑같이 믿을 수 없으면서 자신감은 넘친다며,
이 조합이 위험하다고 진단했다.[^tessl-podjarny]
Böckeler는 Tessl을 spec-as-source를 지향하는 도구로 보았고,
같은 스펙에서 코드를 여러 번 생성하자
결과가 매번 달라지는 것을 직접 확인했다고 적었다.[^bockeler]
2026년 10월 현재 Tessl 홈페이지는 스스로를 에이전트 맥락을 관리하는
플랫폼으로 소개하며, 스펙보다 스킬 레지스트리를 앞세운다.[^tessl-home]

### OpenSpec

Fission AI의 OpenSpec은 제안(propose), 적용(apply), 보관(archive)의
세 단계로 진행된다.
변경마다 `proposal.md`, `specs/`, `design.md`, `tasks.md`를 담은 폴더를 만들고,
스펙 변경은 ADDED, MODIFIED, REMOVED 요구사항으로 나눈 delta spec으로 쓴다.
README는 이것이 새 프로젝트만이 아니라 기존 코드베이스를 위해
만든 것이라고 내세운다.[^openspec]
보관하면 delta가 주 스펙에 반영되고
변경 폴더는 날짜를 붙여 보관 폴더로 옮겨지므로,
스펙은 변경이 쌓이면서 조금씩 자라난다.[^openspec-concepts]
기존 시스템 전체의 스펙을 처음부터 쓰지 않고 바뀌는 부분만 적는다는 점이
Spec Kit과 가장 큰 차이다.

Hashrocket의 Vinicius Negrisolo는 같은 과제(Team 탭 제거)로 두 도구를 비교했다.
생성되는 명령은 OpenSpec 3개, Spec Kit 8개였고,
같은 단계에서 OpenSpec은 파일 3개에 약 250줄,
Spec Kit은 약 800줄을 만들었다.
구현은 OpenSpec이 눈에 띄게 빨랐다.
그는 소규모 시니어 팀에는 OpenSpec을,
역할 분리가 필요하거나 주니어가 많은 팀에는 Spec Kit을 권했다.[^hashrocket]

### 그 밖의 도구

| 도구     | 특징                                                                                                        |
| -------- | ----------------------------------------------------------------------------------------------------------- |
| BMAD     | Breakthrough Method for Agile AI Driven Development의 약자, 명확화·계획·구현과 검증·학습과 조정 단계[^bmad] |
| cc-sdd   | Kiro 스타일 명령을 Claude Code, Codex 등 에이전트 8개에서 쓰게 하는 도구[^cc-sdd]                           |
| Agent OS | 코드베이스에서 표준을 찾아 에이전트 맥락에 넣는 도구[^agent-os]                                             |
| SDD Flow | <https://github.com/Ataden/SDD_Flow>                                                                        |

### 계획을 먼저 세우는 코딩 에이전트 기능

SDD 전용 도구가 아니어도,
주요 코딩 에이전트는 구현 전에 계획을 세우는 기능을 갖추고 있다.

- Claude Code의 plan 모드에서는 Claude가 파일을 읽고 계획을 제안하되,
  사용자가 승인하기 전까지 아무것도 수정하지 않는다.[^claude-plan]
- Cursor는 2025년 10월 7일 Plan Mode를 내놓으며,
  사내 새 기능 대부분이 이제 에이전트가 계획을 쓰는 것으로 시작한다고 밝혔다.
  계획은 편집 가능한 Markdown으로 저장된다.[^cursor-plan]
- JetBrains는 Junie에서 `docs/requirements.md`, `plan.md`, `tasks.md`,
  `.junie/guidelines.md` 네 파일로 스펙 기반 접근을 쓰는 법을 안내한다.[^junie]
- Google Antigravity는 작업 목록, 구현 계획, 결과 설명을
  Markdown 산출물로 만든다.[^antigravity]

Marmelab 비판의 저자 François Zaninotto가 HN에서
자신은 이미 plan 모드를 쓰기 때문에 SDD에서 얻는 것이 없다고 말한 것도
이 맥락이다.[^fzaninotto]
계획 우선은 이미 기본 기능이 되었고,
SDD 도구의 차별점은 계획을 얼마나 오래, 어떤 형식으로 남기느냐로 좁혀졌다.

## 실증 연구

SDD의 효과를 다룬 연구는 2026년 들어 나오기 시작했지만,
아직 통제된 비교 실험은 드물다.

### 실무에서 쓰이는 방식

Agarwal 등의 “Spec-Driven Development as Prescribed and as Practiced”는
공개 GitHub 저장소 73,030개에서 스펙 파일 470,795개를 모으고,
실무자 21명(그중 도구 제작자 8명)을 인터뷰하고 저장소 266개를 분석했다.
연구진은 SDD가 에이전트 동작을 더 믿을 만하게 만들지만
계획과 리뷰 비용을 늘린다고 보고했다.
SDD는 주로 새 기능에 선택적으로 쓰였고,
스펙과 코드가 맞는지는 개발 내내 확인되지 않고
주로 변경이 끝난 시점에만 확인되었다.[^specmine]

### 스펙이 있으면 리뷰가 달라지는가

InfoQ에 실린 Nitin Garg의 실험에서는
스펙 기준선이 있어도 버그 검출률은 52.5%와 51.8%로 차이가 없었다(p=0.69).
대신 발견한 문제를 요구사항과 연결한 비율은 81%와 0%로 크게 달랐고(p=0.043),
리뷰 시간은 48분과 27분으로 스펙이 있을 때 더 길었다.
그는 쉬운 과제에서 보이는 이득을 추론 효과가 다른 모습으로 드러난 것으로 보고,
금융, 보험, 의료 같은 규제 영역부터 단계적으로 도입하라고 권했다.[^garg]

### 계약을 먼저 쓰면 테스트가 나아진다

Tufano 등은 에이전트가 테스트를 만들기 전에 사전조건과 사후조건 같은
계약을 먼저 쓰게 했다.
버그 탐지율은 9.8%포인트(p=0.0352), 분기 커버리지는 2.5%포인트(p=0.0034)
올랐다.[^tufano]
SDD 전체가 아니라 계약이라는 작은 스펙의 효과를 잰 연구다.

### 에이전트에게 TDD를 시키면

Böckeler는 에이전트 루프 안의 TDD가 실제로 가치가 있는지 실험했다.
TDD는 토큰을 3~8.5배 더 썼지만 품질 점수는 TDD를 쓰지 않은 쪽이 조금 높았고,
뮤테이션 테스트 점수는 차이가 없었다.
에이전트는 구현을 계획하는 순간 테스트도 함께 쓸 수 있어서,
사람이 TDD에서 얻는 생각의 마찰이 생기지 않는다는 것이 그의 설명이다.
오히려 TDD 지시는
설계를 국소적인 최소 결정으로 쪼개는 쪽으로 작용했다.[^bockeler-tdd]
절차를 강제하는 것과 결과가 나아지는 것은 다르다는 점에서
SDD에도 그대로 적용되는 질문이다.

### 단일 사례와 개념 논문

Joel Abenhaim은 TypeScript 717,725줄 코드베이스에서 파일 189개를 바꾸며
스펙 수정 14회와 검증 17회로 결함 201개를 고쳤고,
3일이 걸리고 2,430달러가 들었다고 보고했다.[^abenhaim]
저자 한 사람의 자기 보고 사례다.
Piskala의 “Spec-Driven Development: From Code to Contract in the Age of AI
Coding Assistants”는 실험 없이 스펙의 엄밀성 단계와 적용 사례를 정리한
개념 논문이다.[^piskala]
Rosa 등의 연구는 실험 설계만 등록한 단계라 아직 결과가 없다.[^rosa]

## 실무 보고

### 잘 된 사례

- Den Delimarsky는 1년 동안 묵혀 둔 Mauna Kea 카메라 스냅샷 추적기를
  Spec Kit으로 2시간 안에 완성했다.
  그러면서도 스펙이 만병통치약은 아니며 사람의 감독이 계속 필요하다고 적었다.[^den]
- Erick Matsen은 Spec Kit으로 바이오인포매틱스 파이프라인을 하루 만에 만들었다.
  사용자 스토리 5개, 기능 요구사항 13개, 계획 단계의 주요 결정 9개,
  8단계에 걸친 작업 49개였고,
  파일럿에서는 서열 157K개에서 PCP 1,225개를 뽑았다.[^matsen]
- AWS 한국 블로그의 신정섭, 김진아, 권기훈은 Kent Beck의 Augmented Coding,
  TDD, Tidy First를 Kiro의 steering 파일로 적용해 앱을 만들었고,
  테스트 673개를 통과시켰다.[^aws-kr]
- HN 사용자 canterburry는 수용 기준 위주로 스펙을 2~3시간 쓰면
  하루 안에 테스트된 기능을 배포하므로 애자일이 줄어든 것이 없다고 했다.[^canterburry]
  jmathai는 471줄짜리 스펙으로 큰 기능을 문제없이 구현했다고 전했다.[^jmathai]

### 안 된 사례

- Scott Logic의 Colin Eberhardt는 Spec Kit으로 KartLog 앱의
  서킷 관리 기능을 다시 만들었다.
  에이전트 실행 33.5분 동안 마크다운 2,577줄과 코드 689줄이 나왔고,
  검토에 3.5시간이 들었다.
  평소의 반복 방식으로는 에이전트 실행 8분, 코드 리뷰 15분,
  테스트와 수정 9분이 들었다.
  그는 SDD를 쓰지 않을 때 열 배쯤 빠르다며,
  적어도 순수한 형태로는 쓸 만한 절차가 아니라고 결론 내렸다.[^scottlogic]
- Marmelab의 François Zaninotto는 날짜 표시 기능 하나에
  8개 파일, 1,300줄의 스펙이 생성되었다고 적었다.[^marmelab]
- HN 사용자 yoaviram은 Spec Kit을 Claude Code와 함께 열흘 동안 돌려
  “완료” 상태가 되었지만,
  테스트 대부분이 실패하고 빌드가 깨져 고치는 데 비슷한 시간이 더 들었다고
  했다.[^yoaviram]
- hatmanstack은 Kiro가 작업 12개 이상에 하위 작업을 4개 이상씩 만들고,
  코드를 예측할 수 없게 지운 뒤 되돌리지 않았다고 했다.[^hatmanstack]
  sandeepkd는 Spring Boot 업그레이드에 Kiro가 작업 40개 이상을 만들었는데,
  자신이 경험으로 정리한 목록은 5개였다고 했다.[^sandeepkd]
- thomascountz는 Spec Kit으로 CLI 도구를 만들며
  코드를 보기 전까지 수정과 질문에 몇 시간을 썼고,
  처음부터 끝까지 돌려 보는 피드백이 없어 답답했다고 했다.[^thomascountz]
- Böckeler도 Kiro가 작은 버그에는 지나치게 무거웠고,
  Spec Kit의 수많은 마크다운 파일보다
  차라리 코드를 리뷰하겠다고 적었다.[^bockeler]

잘 된 사례와 안 된 사례 모두 한 사람이 한두 기능으로 잰 것이다.
잘 된 쪽은 새 프로젝트나 독립된 기능이 많고,
안 된 쪽은 작은 변경이나 기존 코드베이스가 많다.

## 비판과 논쟁

### 구현 중에 배우는 것을 무시한다는 비판

Kent Beck은 LinkedIn에서 자신이 본 스펙 기반 개발 설명이 구현 전에 스펙
전체를 쓰는 것을 강조하며,
구현 중에 스펙을 바꿀 만한 것을 배우지 않으리라는
“(내게는 기이한) 가정”을 담고 있다고 했다.
Martin Fowler는 2026년 1월 8일 이 말을 인용하며,
실험하며 배우는 반복 과정이 쓸 만한 스펙의 핵심이고
AI는 코드를 빨리 만드는 데보다
피드백을 빨리 받는 데 써야 한다고 덧붙였다.[^fowler]

같은 비판은 여러 곳에서 되풀이된다.
deontologician은 코드에는 도메인 규칙을 다루는 일과
데이터 표현을 관리하는 일이 섞여 있으며,
도메인 규칙은 직접 구현해 보기 전까지는 제대로 이해하지 못한다고 썼다.
그래서 스펙을 쓸 수 없을 만큼 문제가 혼란스러울 때는 SDD가 통하지 않는다는
것이다.[^deontologician]
VSDD 스레드에서 _pdp_는 어떻게 만들지 모르는 것은 스펙으로 쓸 수 없고,
코드 비용이 0에 가깝다면 다섯 가지 버전을 만들어 고르면 된다고 했다.[^pdp]
이에 virgilp는 스펙이야말로 끝까지 읽고 통제할 수 있는 유일한 부분이라고
반박했고,[^virgilp]
petersumskas는 그렇게 하면
평범한 해법 다섯 개가 나올 뿐이라고 받았다.[^petersumskas]

### 워터폴 논쟁

Marmelab의 François Zaninotto는 2025년 11월 12일
“Spec-Driven Development: The Waterfall Strikes Back”에서
맥락을 보지 못하는 문제, 스펙과 코드를 모두 리뷰해야 하는 부담,
잘못된 안도감을 지적하고,
Lean Startup에서 따온 반복 방식을 대안으로 제안했다.[^marmelab]
이 글의 HN 토론에는 225점과 191개 댓글이 달렸다.[^hn-marmelab]

HN에서는 워터폴의 정의부터 부딪쳤다.
4ndrewl은 워터폴의 문제는 상세한 스펙이 아니라
수년에 걸친 리드타임과 반복할 수 없는 구조였고,
SDD에는 둘 다 해당하지 않는다고 했다.[^4ndrewl]
laserlight는 상세한 스펙 자체가 문제라며,
스펙은 자신이 해법이라고 전제하지만
애자일은 문제조차 모른다고 인정하는 데서 출발한다고 반박했다.[^laserlight]
constantcrying은 지연이 아니라 스펙이 문제이고,
프로젝트가 깊어지면 스펙이 엉망이 된다고 거들었다.[^constantcrying]
yoz-y는 대부분 실제 워터폴을 교과서로만 겪었다며,
몇 시간짜리 스펙을 워터폴이라 부르는 것은 우습다고 했다.[^yoz-y]
canterburry의 성공 사례에 대해서는
mattmanser가 스펙과 워터폴의 정의를 바꿔치기한다고 비판했고,[^mattmanser]
pipes는 SDD가 믿을 수 없는 컴파일러를 들여오는 것이라고 했다.[^pipes]
글쓴이 Zaninotto는 워터폴과 애자일 논쟁이 아직도 이렇게 뜨겁다는 데
놀랐다고 말했다.[^fzaninotto]

Spec Kit 쪽에서는 Delimarsky가 처음부터
이것이 워터폴식 계획이 아니라고 설명했다.[^ms-blog]
2026년 3월 12일 Allstacks CTO Jeremy Freeman은 Marmelab 글을 직접 반박하며,
워터폴의 결함은 스펙이 아니라 피드백 고리의 길이였고
애자일은 구현 비용이 비싸던 조건에 맞춘 적응이었다고 주장했다.[^allstacks]
자사 제품을 파는 회사의 글이라는 점은 감안해야 한다.

### 리뷰할 마크다운이 쏟아진다는 비판

가장 구체적인 불만은 리뷰 부담이다.
Thoughtworks 기술 레이더는 이런 도구가 정교하고 고집 센 워크플로를 만들며,
생성된 스펙 파일을 리뷰하기 어렵다고 지적했다.[^radar]
ctxc는 spec-kit의 계획이 볼트 하나 조이면 될 일을
토니 스타크가 동굴에서 로봇을 만드는 규모로 키웠다고 비꼬았다.[^ctxc]
OpenSpec 스레드에서 open-paren은 회사가 OpenSpec을 도입한 뒤
변경마다 리뷰할 마크다운이 쏟아지고 문서 품질이 늘 형편없다고 했다.[^open-paren]
이에 TabishB는 생각 없이 쓴 스펙이
쓸모없는 문서가 된다는 점은 인정했다.[^tabishb]
InfoQ의 Hari Krishnan은 기업 규모 도입의 위험으로
마크다운 문서가 끝없이 불어나는 현상을 꼽고,
SDD는 도구가 아니라 조직의 역량이라고 보았다.[^infoq-enterprise]

### 스펙이 코드와 어긋난다는 비판

spec-anchored와 spec-as-source가 성립하려면
스펙과 코드가 계속 맞아야 한다.
OpenSpec 스레드에서 mafro는 6~9개월짜리 개인 프로젝트 두 개에 OpenSpec을 쓰다가,
LLM으로 스펙과 코드를 양방향으로 대조해 보니 둘이 크게 어긋나 있어
스펙을 버렸다고 했다.
그는 코드가 곧 명세라며, 프로세스 흐름과 아키텍처 결정 기록만 남겼다.[^mafro]
mactavish88도 오래 남는 스펙은 쓸모없고 변경 절차만 가치가 있다고
동의했다.[^mactavish88]
trjordan은 진실의 원천은 하나여야 하고,
스펙에 모든 것을 걸려면 언제든 코드베이스를 처음부터 다시 만들 수 있어야 하는데
지금 도구로는 웃음거리 수준이라고 했다.[^trjordan]
앞의 실무 조사도 스펙과 코드의 일치가 주로 변경이 끝난 시점에만 확인된다고
보고했다.[^specmine]

### 스펙을 쓰는 비용이 코드를 만드는 비용을 넘는다는 비판

Spec Kit 저장소의 이슈 #1092에서 sholtomaud는
긴 스펙을 써도 구현 품질이 낮고,
문제가 스펙 탓인지 구현 탓인지 가를 디버깅 절차가 없으며,
스펙 작성 비용이 코드 생성 비용을 넘을 수 있다고 지적했다.
이 이슈는 2026년 2월 25일 토론 게시판으로 옮겨졌다.[^issue-1092]
HN에서 rsyring은 Spec Kit을 쓰기 전에 이 이슈를 읽어 보라고 권했다.[^rsyring]
OpenSpec 스레드의 sheepscreek은 최신 모델은 계획을 잘 세우므로
Codex나 Claude Code에서는 이런 도구가 필요 없다고 했고,[^sheepscreek]
Kiro 출시 스레드의 retinaros는
Claude Code에 규칙 파일 하나면 된다고 했다.[^retinaros]
sgt101은 커뮤니티가 증거 없이 효과가 있다는 방법을
사실처럼 밀어붙인다고 비판했다.[^sgt101]
shubhamjain은 SDD도 TDD 유행처럼 초반 성과로 부풀려졌다가
시들 것이라고 내다봤다.[^shubhamjain]

### 사람이 손으로 쓰는 규칙은 감당할 수 없다는 경고

Thoughtworks 기술 레이더는 2025년 11월 판(33호)에서
스펙 기반 개발을 Assess 단계에 두었다.
레이더는 AI에게 줄 세부 규칙을 사람이 손으로 쓰는 방식은
규모가 커지면 감당할 수 없다는 “쓴 교훈”을
다시 배우고 있을지도 모른다고 경고했다.
이 항목은 현재 판에는 실려 있지 않다.[^radar]
2026년 4월의 34호 레이더는
[Thoughtworks 기술 레이더 34호](thoughtworks-tech-radar-34.md)에 따로 정리했다.

### 충분히 상세한 스펙은 코드다

Gabriella Gonzalez는 2026년 3월 17일,
구현을 안정적으로 생성할 만큼 정밀한 스펙을 쓰려면
문서를 코드나 코드와 아주 닮은 형태로 바꿀 수밖에 없다고 썼다.[^gonzalez]
[충분히 상세한 명세는 코드다](sufficiently-detailed-spec-is-code.md)에
이 논지를 따로 정리했다.

HN의 alpaylan은 사람이 검증할 속성을 정하는 일은 피할 수 없고,
스펙이 구현보다 훨씬 단순할 때에만 이득이 생긴다고 짚었다.[^alpaylan]
Verified Spec-Driven Development(VSDD)는 이 방향을 끝까지 밀어붙인 제안이다.
스펙 확정, TDD, 맥락을 새로 연 별도 모델의 적대적 리뷰, 피드백 반영,
Kani, Dafny, TLA+를 이용한 형식 검증, 수렴의 6단계를 둔다.[^vsdd]
이 제안의 HN 토론에는 211점과 118개 댓글이 달렸다.[^hn-vsdd]

### 코드 없는 라이브러리

Drew Breunig은 2026년 1월 8일, 구현 코드 없이 약 500줄의 `SPEC.md`,
테스트 케이스 125개를 담은 `tests.yaml`, 설치 안내만으로 된 라이브러리
whenwords를 공개했다.
Ruby, Python, Rust, Elixir, Swift, PHP, Bash, Excel로 구현이 만들어졌지만,
그는 성능, 테스트 복잡도, 지원, 업데이트, 커뮤니티 때문에
코드 라이브러리가 여전히 필요하다고 적었다.[^breunig]
spec-as-source가 성립하는 데
스펙 문서보다 적합성 테스트가 더 큰 역할을 한다는 점을 보여 주는 사례다.

### Kiro 가격 논란

Kiro는 2025년 8월 15일 요금제를 발표하며
무료 요금제에서 일반 요청 50회만 주고 스펙 요청은 주지 않았다.[^kiro-pricing]
The Register에 따르면 처음 예고된 요금은 Pro가 19달러에 1,000회,
Pro+가 39달러에 3,000회였는데,
바뀐 요금에서는 스펙 요청이 회당 0.20달러로 일반 요청의 다섯 배가 되었다.
Antonio Ribeiro는 가볍게 써도 월 약 550달러,
하루 종일 쓰면 월 약 1,950달러가 든다고 추산했고,
Pro+ 한도를 15분 만에 다 썼다는 보고도 나왔다.
AWS는 8월 20일 일부 작업이 요청을 여러 번 잘못 차감하는 버그를 인정하고
8월 요금을 받지 않기로 했다.[^register-kiro]
HN에서 motbus3은 일반 에이전트가 작업이 너무 복잡하다며
계속 스펙 요청으로 바꾸라고 재촉했다고 했다.[^motbus3]
지금 Kiro 요금은 크레디트 기준으로 바뀌어
스펙 요청과 일반 요청의 구분이 없다.[^kiro-pricing-now]
스펙 단계가 과금 단위가 되면,
스펙을 더 쓰게 만드는 쪽으로 도구가 기울 수 있다는 점을 보여 준 사건이다.

### Lobste.rs의 반응

Lobste.rs의 Kiro 토론에서 manfred는
바이브 코딩 덕에 사람들이 쓸모 있는 산출물이 무엇인지 알게 되었고,
그 산출물을 만드는 일이 가장 큰 시간 소모라는 것을 깨달으면
LLM을 버리게 될지도 모른다고 냉소했다.[^manfred]
Student는 LLM이 직접 실행해 검증할 수 있는 실행 가능한 스펙이
빠져 있다고 했다.[^student]
mjb는 구조화된 마크다운은 모든 개발자가 이해하기 쉬워서
그 수준에서 시작했고,
더 실행 가능하고 형식적인 방향을 고민하고 있다고 답했다.[^mjb]
camshaft는 구현, 형식 모델, 사람이 읽는 스펙을
추적성 도구로 묶어야 한다고 했다.[^camshaft]

## 배경으로 인용되는 수치

Sonar가 전 세계 개발자 1,100명을 조사한 결과,
88%가 AI 코딩 도구를 쓰며 신뢰할 수 없는 코드(53%)나
중복 코드(40%) 같은 문제를 하나 이상 겪었다고 답했다.[^sonar]
DORA의 2025년 AI 보고서를 다룬 InfoQ 기사에 따르면
응답자의 약 90%가 AI를 쓰지만 AI를 신뢰한다는 응답은 33%였고,
처리량이 늘어난 만큼 불안정성도 계속 늘었다.
보고서는 AI를 조직의 강점과 약점을 모두 키우는 증폭기로 보았다.[^dora]
이 조사들은 AI 생성 코드의 문제를 보여 줄 뿐,
SDD가 그 문제를 줄인다는 근거는 아니다.

## 언제 쓰고 언제 피하나

자료를 모으면 SDD가 득이 되는 조건과 손해가 되는 조건이 비교적 분명하다.

- 새 기능처럼 범위가 크고 요구사항이 아직 흩어져 있을 때 쓰인다.
  실무 조사에서도 주로 새 기능에 쓰였다.[^specmine]
- 작은 버그 수정과 탐색적 코딩에는 맞지 않는다.
  Kiro 문서도 이 경우 기능 스펙을 권하지 않는다.[^kiro-feature]
  버그 수정에는 버그 조건과 사후조건만 적는 가벼운 형식이 낫다.[^kiro-bugfix]
- 기존 코드베이스에서는 전체 스펙보다 바뀌는 부분만 적는 방식이
  부담이 적다.[^openspec][^hashrocket]
- 스펙의 분량이 코드보다 커지면 리뷰 비용이 이득을 넘는다.[^scottlogic]
- 요구사항을 추적해야 하는 규제 영역에서는
  버그 검출률보다 문제를 요구사항과 연결하는 능력이 더 큰 이득이다.[^garg]
- 문제 자체가 아직 혼란스러우면 스펙보다 먼저 만들어 보는 편이 낫다.[^deontologician]
- 스펙과 코드의 일치는 변경이 끝날 때만 확인되기 쉬우므로,
  property-based testing이나 적합성 테스트처럼
  자동으로 확인하는 장치가 있어야 스펙이 낡지 않는다.[^specmine][^kiro-correctness]
- 오래 남길 스펙은 최소로 줄이고,
  변경 절차와 아키텍처 결정 기록처럼 시간이 지나도 맞는 것만 남긴다.[^mafro]

[카카오페이의 Spec-kit 실전기](kakaopay-spec-kit-practice.md)도
일관성은 나아지지만 간단한 작업에서는 오버엔지니어링이 되고
토큰 소모가 크다고 보고했다.
[AI 오케스트레이터라는 환상](ai-orchestrator-illusion.md)은
언어가 의도를 완전히 담지 못하고 AI가 그 빈틈을 확률적으로 채우므로,
스펙을 쓰는 일이 구현을 통한 맥락 축적을 대신할 수 없다고 본다.

## 국내 자료

- 요즘IT의 안영회는 2025년 12월 1일 Böckeler의 글을 옮기고 해설하며,
  SDD가 모델 기반 개발의 실패를 되풀이할 위험을 경고했다.[^yozm]
- AWS 한국 블로그의 Kiro 사례는 앞의 실무 보고에 정리했다.[^aws-kr]
- 카카오페이의 Spec Kit 적용기는
  [카카오페이의 Spec-kit 실전기](kakaopay-spec-kit-practice.md)에 있다.

## 정리

비판의 공통점은 스펙 자체가 아니라
피드백 없이 먼저 다 쓰는 스펙을 겨눈다는 것이다.
Fowler의 결론도 스펙을 버리라는 것이 아니라
코드와 함께 고치라는 쪽이다.[^fowler]
Threads 사용자 cys_makin은 이 논쟁을 미리 설계하자는 쪽과
일단 만들고 고치자는 쪽의 오래된 줄다리기가 반복되는 것으로 보았다.[^cys-5]
Royce의 원 논문이 이미 두 번 만들라고 권했다는 점을 보면,[^royce]
이 줄다리기는 반세기가 넘었다.

지금까지의 근거로 말할 수 있는 것은 세 가지다.
첫째, 계획을 먼저 세우는 것은 이미 모든 코딩 에이전트의 기본 기능이 되었다.
둘째, 스펙이 버그를 더 잘 잡는다는 정량 근거는 아직 없고,
요구사항과 문제를 연결하는 데서만 뚜렷한 차이가 나왔다.[^garg]
셋째, 오래 남는 스펙은 자동 검증 없이는 코드와 어긋난다.[^mafro][^specmine]
그래서 spec-anchored 수준의 짧은 스펙과 자동 검증을 함께 쓰는 방식에
반론이 가장 적다.
SDD 전체를 반복 개발과 비교한 대규모 통제 실험은 이번 조사에서 찾지 못했다.

---

[^github-blog]: The GitHub Blog, [Spec-driven development with AI: Get started with a new open source toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/), 2025-09-02

[^ms-blog]: Microsoft for Developers, [Diving Into Spec-Driven Development With GitHub Spec Kit](https://devblogs.microsoft.com/blog/spec-driven-development-spec-kit/), 2025-09-15

[^spec-driven-md]: GitHub, [spec-kit/spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md), 게시일 표기 없음

[^spec-kit-1]: GitHub, [Release v1.0.0 · github/spec-kit](https://github.com/github/spec-kit/releases/tag/v1.0.0), 2026-08-21

[^spec-kit-readme]: GitHub, [github/spec-kit](https://github.com/github/spec-kit), 2026-10-18 확인

[^spec-kit-api]: GitHub API, [github/spec-kit](https://api.github.com/repos/github/spec-kit), 2026-10-18 확인

[^spec-kit-releases]: GitHub, [Releases · github/spec-kit](https://github.com/github/spec-kit/releases), 2026-10-18 확인

[^bockeler]: martinfowler.com, [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), 2025-10-15

[^bockeler-tdd]: martinfowler.com, [TDD inside the agent loop - theater or actual value?](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html), 게시일 표기 없음

[^royce]: Winston W. Royce, [Managing the Development of Large Software Systems](https://faculty.washington.edu/hazeline/misc/reserve/royce_waterfall.pdf), 1970-08

[^ears-wiki]: Wikipedia, [Easy Approach to Requirements Syntax](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax), 게시일 표기 없음

[^ears-mavin]: Alistair Mavin, [EARS](https://alistairmavin.com/ears/), 게시일 표기 없음

[^mda]: OMG, [Model Driven Architecture](https://www.omg.org/mda/), 게시일 표기 없음

[^dbc]: Eiffel Software, [Design by Contract: Introduction](https://www.eiffel.com/values/design-by-contract/introduction/), 게시일 표기 없음

[^bdd]: Dan North, [Introducing BDD](https://dannorth.net/blog/introducing-bdd/), 2006-09-20

[^tla]: Newcombe 외, [How Amazon Web Services Uses Formal Methods](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf), 게시일 표기 없음

[^vsdd]: dollspace-gay(GitHub Gist), [Verified Spec-Driven Development (VSDD)](https://gist.github.com/dollspace-gay/d8d3bc3ecf4188df049d7a4726bb2a00), 게시일 표기 없음

[^kiro-intro]: Kiro, [Introducing Kiro](https://kiro.dev/blog/introducing-kiro/), 2025-07-14

[^kiro-ga]: Kiro, [Kiro is generally available: Build with your team in the IDE and terminal](https://kiro.dev/blog/general-availability/), 2025-11-17

[^kiro-specs]: Kiro, [Specs](https://kiro.dev/docs/specs/), 게시일 표기 없음

[^kiro-feature]: Kiro, [Feature Specs](https://kiro.dev/docs/specs/feature-specs/), 게시일 표기 없음

[^kiro-correctness]: Kiro, [Correctness](https://kiro.dev/docs/specs/correctness/), 2026-08-04

[^kiro-steering]: Kiro, [Steering](https://kiro.dev/docs/steering/), 2026-10-06

[^kiro-hooks]: Kiro, [Hooks](https://kiro.dev/docs/hooks/), 2026-10-10

[^kiro-bugfix]: Kiro, [The bug fix paradox: why AI agents keep breaking working code](https://kiro.dev/blog/bug-fix-paradox/), 2026-02-19

[^kiro-one-year]: Kiro, [One year of Kiro: a look back, and a look ahead](https://kiro.dev/blog/one-year/), 2026-07-14

[^kiro-pricing]: Kiro, [Kiro pricing plans are now live](https://kiro.dev/blog/pricing-plans-are-live/), 2025-08-15

[^kiro-pricing-now]: Kiro, [Pricing](https://kiro.dev/pricing/), 2026-10-18 확인

[^register-kiro]: The Register, [AWS pricing for Kiro dev tool dubbed 'a wallet-wrecking tragedy'](https://www.theregister.com/2025/08/18/aws_updated_kiro_pricing/), 2025-08-18

[^q-eos]: AWS DevOps Blog, [Amazon Q Developer end-of-support announcement](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/), 2026-04-30

[^tessl]: Tessl, [Tessl Launches Spec-Driven Development Tools for AI Coding Agents](https://tessl.io/blog/tessl-launches-spec-driven-framework-and-registry/), 2025-09-23

[^tessl-podjarny]: Tessl, [How Tessl's Products Pioneer Spec-Driven Development](https://tessl.io/blog/how-tessls-products-pioneer-spec-driven-development/), 2025-09-16

[^tessl-home]: Tessl, [tessl.io](https://tessl.io/), 2026-10-18 확인

[^openspec]: GitHub, [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), 게시일 표기 없음

[^openspec-concepts]: GitHub, [OpenSpec/docs/concepts.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md), 게시일 표기 없음

[^hashrocket]: Hashrocket, [OpenSpec vs Spec Kit: Choosing the Right AI-Driven Development Workflow for Your Team](https://hashrocket.com/blog/posts/openspec-vs-spec-kit-choosing-the-right-ai-driven-development-workflow-for-your-team), 2025-10-21

[^bmad]: GitHub, [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD), 게시일 표기 없음

[^cc-sdd]: GitHub, [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd), 게시일 표기 없음

[^agent-os]: Builder Methods, [Agent OS](https://buildermethods.com/agent-os), 게시일 표기 없음

[^claude-plan]: Anthropic, [Common workflows](https://code.claude.com/docs/en/common-workflows), 게시일 표기 없음

[^cursor-plan]: Cursor, [Introducing Plan Mode](https://cursor.com/blog/plan-mode), 2025-10-07

[^junie]: JetBrains Blog, [How to Use a Spec-Driven Approach for Coding with AI](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/), 2025-10-27

[^antigravity]: Simon Willison, [Google Antigravity](https://simonwillison.net/2025/Nov/18/google-antigravity/), 2025-11-18

[^specmine]: arXiv, [Spec-Driven Development as Prescribed and as Practiced](https://arxiv.org/abs/2608.25202), 2026-08-25

[^garg]: InfoQ, [When Spec-Driven Development Pays off](https://www.infoq.com/articles/when-spec-driven-development-pays-off/), 2026-09-10

[^tufano]: arXiv, [Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation](https://arxiv.org/abs/2608.17177), 2026-08-17

[^abenhaim]: arXiv, [Specification-first convergence with an AI coding agent: a case study of dismantling a core architectural invariant across 189 files in a 717k-line codebase with no test oracle and no human code review](https://arxiv.org/abs/2608.12440), 2026-08-12

[^piskala]: arXiv, [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180), 2026-01-30

[^rosa]: arXiv, [Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design](https://arxiv.org/abs/2601.03878), 2026-01-07

[^den]: den.dev, [What's The Deal With GitHub Spec Kit](https://den.dev/blog/github-spec-kit/), 2025-10-12

[^matsen]: Matsen group, [Spec-Driven Development with spec-kit](https://matsen.fhcrc.org/general/2026/02/10/spec-kit-walkthrough.html), 2026-02-10

[^aws-kr]: AWS 기술 블로그, [Kiro와 함께 Augmented Coding 기반 소프트웨어 개발하기](https://aws.amazon.com/ko/blogs/tech/augmented-coding-with-kiro), 2025-08-21

[^scottlogic]: Scott Logic, [Putting Spec Kit Through Its Paces: Radical Idea or Reinvented Waterfall?](https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html), 2025-11-26

[^marmelab]: Marmelab, [Spec-Driven Development: The Waterfall Strikes Back](https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html), 2025-11-12

[^allstacks]: Allstacks, [Spec-Driven Development Isn't Waterfall: Why the AI Coding Bottleneck Changed Everything](https://www.allstacks.com/blog/spec-driven-development-isnt-waterfall-why-the-ai-coding-bottleneck-changed-everything), 2026-03-12

[^deontologician]: deontologician, [Spec driven development doesn't work if you're too confused to write the spec](https://publish.obsidian.md/deontologician/Posts/Spec-driven+development+doesn%27t+work+if+you%27re+too+confused+to+write+the+spec), 게시일 표기 없음

[^infoq-enterprise]: InfoQ, [Spec-Driven Development – Adoption at Enterprise Scale](https://www.infoq.com/articles/enterprise-spec-driven-development/), 2026-02-19

[^issue-1092]: GitHub, [High Level Design Concerns · Issue #1092 · github/spec-kit](https://github.com/github/spec-kit/issues/1092), 2025-10-30

[^fowler]: martinfowler.com, [Fragments: January 8](https://martinfowler.com/fragments/2026-01-08.html), 2026-01-08

[^radar]: Thoughtworks, [Spec-driven development](https://www.thoughtworks.com/radar/techniques/spec-driven-development), 2025-11

[^gonzalez]: Haskell for all, [A sufficiently detailed spec is code](https://haskellforall.com/2026/03/a-sufficiently-detailed-spec-is-code), 2026-03-17

[^breunig]: Drew Breunig, [A Software Library with No Code](https://dbreunig.com/2026/01/08/a-software-library-with-no-code.html), 2026-01-08

[^sonar]: DevOps.com, [Survey Sees Wider Adoption of AI Coding Tools Creating More DevOps Challenges](https://devops.com/survey-sees-wider-adoption-of-ai-coding-tools-creating-more-devops-challenges/), 2026-01-08

[^dora]: InfoQ, [DORA Report Finds AI Is an Amplifier](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025), 2025-09-29

[^yozm]: 요즘IT, [스펙 주도 개발(SDD) 심층 탐구하기](https://yozm.wishket.com/magazine/detail/3477/), 2025-12-01

[^hn-marmelab]: <https://news.ycombinator.com/item?id=45935763>

[^hn-vsdd]: <https://news.ycombinator.com/item?id=47197595>

[^4ndrewl]: <https://news.ycombinator.com/item?id=45935850>

[^laserlight]: <https://news.ycombinator.com/item?id=45936308>

[^constantcrying]: <https://news.ycombinator.com/item?id=45936628>

[^yoz-y]: <https://news.ycombinator.com/item?id=45936231>

[^fzaninotto]: <https://news.ycombinator.com/item?id=45945971>

[^canterburry]: <https://news.ycombinator.com/item?id=45936358>

[^mattmanser]: <https://news.ycombinator.com/item?id=45936626>

[^pipes]: <https://news.ycombinator.com/item?id=45937007>

[^thomascountz]: <https://news.ycombinator.com/item?id=45935925>

[^sgt101]: <https://news.ycombinator.com/item?id=45936515>

[^yoaviram]: <https://news.ycombinator.com/item?id=45614365>

[^hatmanstack]: <https://news.ycombinator.com/item?id=45614020>

[^ctxc]: <https://news.ycombinator.com/item?id=45613826>

[^trjordan]: <https://news.ycombinator.com/item?id=45865096>

[^shubhamjain]: <https://news.ycombinator.com/item?id=45865308>

[^rsyring]: <https://news.ycombinator.com/item?id=45866013>

[^nathankp]: <https://news.ycombinator.com/item?id=44561071>

[^retinaros]: <https://news.ycombinator.com/item?id=44563666>

[^sandeepkd]: <https://news.ycombinator.com/item?id=44565669>

[^pdp]: <https://news.ycombinator.com/item?id=47198203>

[^virgilp]: <https://news.ycombinator.com/item?id=47198834>

[^petersumskas]: <https://news.ycombinator.com/item?id=47203293>

[^alpaylan]: <https://news.ycombinator.com/item?id=47199656>

[^mafro]: <https://news.ycombinator.com/item?id=49738937>

[^mactavish88]: <https://news.ycombinator.com/item?id=49739689>

[^open-paren]: <https://news.ycombinator.com/item?id=49736016>

[^tabishb]: <https://news.ycombinator.com/item?id=49736908>

[^twen_ty]: <https://news.ycombinator.com/item?id=49738104>

[^sheepscreek]: <https://news.ycombinator.com/item?id=49735141>

[^jmathai]: <https://news.ycombinator.com/item?id=49734869>

[^motbus3]: <https://news.ycombinator.com/item?id=44944236>

[^manfred]: <https://lobste.rs/s/gcgqvb/kiro_future_ai_spec_driven_software#c_wjuhsn>

[^student]: <https://lobste.rs/s/gcgqvb/kiro_future_ai_spec_driven_software#c_1lewhs>

[^mjb]: <https://lobste.rs/s/gcgqvb/kiro_future_ai_spec_driven_software#c_4otzrk>

[^camshaft]: <https://lobste.rs/s/gcgqvb/kiro_future_ai_spec_driven_software#c_dcd67u>

[^cys-2]: cys_makin(Threads), [그런데 문제가 터졌습니다.](https://www.threads.com/@cys_makin/post/DemDQ5MkzNK), 2026-10-17

[^cys-5]: cys_makin(Threads), [명세서에 보안계획을 싣는다면 비대해질 수밖에 없는데 이건 어떻게 해결할까요.](https://www.threads.com/@cys_makin/post/DemDSacE-6W), 2026-10-17
