# Temporal: 코드로 쓰는 워크플로가 실패해도 이어서 실행되게 하는 오픈소스 Durable Execution 플랫폼

<https://temporal.io/>

<https://github.com/temporalio/temporal>

HN 토론: <https://news.ycombinator.com/item?id=24815640> (123점, 52개 댓글)

## 소개

Temporal은 애플리케이션의 실행 상태를 서비스가 기록해 두었다가, 서버나 워커가 죽어도 끊긴 지점부터 이어서 실행하게 해 주는 플랫폼이다.
홈페이지는 이를 Durable Execution이라 부르고, 실패가 없는 것처럼 코드를 쓰게 해 준다고 소개한다.
워크플로는 각 단계의 상태를 자동으로 저장하며, 실패하면 정확히 중단된 곳에서 이어서 실행된다는 설명이다.
홈페이지는 고객사를 대표 사례(OpenAI, NVIDIA, Salesforce, Twilio, Descript 등)로 내세우며, 첫 문구는 세계 최고의 AI가 Temporal 위에서 돈다는 것이다.

핵심 저장소 `temporalio/temporal`은 Go로 쓰였고 MIT 라이선스이며, 2019년 10월에 만들어졌다.
이 글을 쓸 때 별은 약 23,900개(홈페이지 표기 23,920개, GitHub API 23,921개)였고 마지막 푸시는 2026년 10월 22일이었다.
홈페이지는 이 프로젝트가 완전한 오픈소스이고, 9년 동안 운영 환경에서 쓰였으며, AWS SQS, AWS SWF, Azure Durable Functions, Uber를 움직이는 Cadence 프로젝트를 만든 사람들의 20년 개발 경험 위에 있다고 말한다.
이 문장들은 홈페이지의 서술이며 여기서 검증한 것은 저장소 메타데이터뿐이다.

### 다른 도구와의 차이

HN의 이 홈페이지 스레드는 2020년 10월의 것이어서 당시 제품 이야기이지만, 개념의 차이는 지금도 같다.
Temporal CEO라고 밝힌 mfateev가 직접 질문에 답했다.[^mfateev-ceo]
acjohnson55는 비즈니스 소프트웨어의 큰 문제가 핵심 로직이 요청과 응답에 담기지 않는 순간 큐, 예약 작업, ETL, 마이크로서비스에 쪼개져 이해하고 관측하기 어려운 과정이 된다는 점이라고 적고 Temporal에 기대를 표했다.[^acjohnson55]

BPMN 엔진과 무엇이 다르냐는 질문에 mfateev는 워크플로 코드를 범용 프로그래밍 언어로 쓰는 것이 핵심이라고 답했다.
타입 검사, 표준 오류 처리, IDE와 디버거와 단위 테스트 같은 기존 도구, 같은 언어로 쓰는 Activity와 워크플로, 표준 라이브러리 재사용을 장점으로 들었다.[^mfateev-bpmn]
그는 시각적 정의가 순서 정의는 돕지만 상태 관리, 표현식, 데이터 가공, 재시도 정책 같은 복잡성의 대부분은 다이어그램에 보이지 않는다고 보았다.[^mfateev-visual]
워크플로를 DAG나 상태 기계 같은 중간 표현 없이 코드 그대로 동기 프로그램처럼 실행하므로, 승인을 기다린 뒤 30일 동안 잠들었다가 메일을 보내는 코드도 유효한 워크플로라는 설명이다.[^mfateev-code]

Cadence와의 관계는 Temporal이 Cadence 원 창업자들이 만든 포크라는 것이다.
mfateev는 가장 큰 기술적 차이로 Temporal이 gRPC와 Protobuf를 쓰고 Cadence는 TChannel과 Thrift를 쓴다는 점을 들었고, 그 결과로 TChannel이 지원하지 않던 mTLS를 Temporal이 지원한다고 했다.[^mfateev-fork]
이는 2020년 시점의 설명이다.

## 핵심 개념

홈페이지와 문서가 설명하는 용어는 다음과 같다.

| 개념                | 의미                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------- |
| Workflow Definition | 워크플로의 단계를 적은 코드. Go, Java, TypeScript, Python 같은 범용 언어로 쓴다                                |
| Workflow Execution  | Workflow Definition을 실행 요청과 결합해 만든 실제 실행 인스턴스                                               |
| Activity            | 서비스 호출, 파일 변환, 메일 발송처럼 한 가지 동작을 하는 일반 함수. 실패하면 재시도 정책에 따라 다시 실행된다 |
| Worker와 Task Queue | Activity 함수를 이름으로 등록한 워커가 Task Queue를 폴링해 작업을 가져와 실행한다                              |
| Event History       | 워크플로 실행에서 이미 일어난 일의 순서 있는 전체 로그. 실행을 같은 상태로 되돌리는 데 쓴다                    |
| Schedule            | 정해진 시각에 워크플로를 시작하게 하는 기능                                                                    |

### 복구하는 방식

문서는 워크플로가 중단되거나 오류를 만나면 Temporal의 목표가 워크플로를 중단 직전과 똑같은 상태로 되돌리는 것이라고 설명한다.[^wf]
이를 위해 Event History를 보관한다.[^wf]
애플리케이션이 죽어도 Temporal이 장애 전 상태를 다시 만들어 그 지점부터 계속한다.[^wf]
홈페이지는 이 덕분에 잃는 진행이나 고아 프로세스, 수동 복구가 없다고 말한다.

### 실패를 두는 위치

실패하기 쉬운 호출은 Activity로 감싼다.
Activity는 일반 함수이고, 문서는 Activity 코드가 무엇이든 할 수 있고 비결정적이어도 된다고 설명하면서 재시도가 중복된 부작용을 만들지 않도록 멱등(idempotent)하게 쓰기를 권한다.[^act]
Activity 시도가 실패하면 재시도 정책에 따라 자동으로 다시 실행되고, 각 시도는 초기 상태에서 시작하되 heartbeat 상세 정보를 체크포인트로 쓰면 마지막 기록을 다음 시도에서 받을 수 있다.[^act]
큰 기능은 여러 Activity로 쪼개라는 안내도 있는데, 장애 복구가 쉽고 타임아웃을 짧게 걸 수 있으며 멱등하게 만들기 쉬워지기 때문이다.[^act]

## 사용 사례

홈페이지가 소개하는 패턴은 다음과 같다.

- 에이전트, MCP, AI 파이프라인: 현실의 혼란을 견디는 에이전트와 학습 파이프라인 조율
- 사람이 끼는 워크플로
- 보상 패턴(Saga): Saga를 `try...catch`처럼 쓴다는 설명
- 며칠, 몇 주, 몇 달 동안 이어지는 긴 워크플로
- 주문 처리
- 내구성 있는 원장
- CI/CD
- 고객 확보와 온보딩
- DAG

고객 사례는 NVIDIA(클라우드에 걸친 GPU 플릿 관리), Salesforce(모놀리스 이전), Twilio(자체 시스템에서 Temporal Cloud로 이동), Descript(AI 가동률 개선)다.
홈페이지는 이 사례들을 강연 영상으로 연결한다.

## 호스팅

Temporal Service는 직접 호스팅하거나 Temporal Cloud를 쓸 수 있다.
홈페이지는 어느 쪽이든 Temporal이 사용자의 코드를 보지 않는다고 적는다.
Temporal Cloud 가입 시 150달러의 무료 크레딧을 준다.
홈페이지 하단에는 최근 30일 가동률 99.999%와 모든 시스템 정상 표시가 있다.
이 수치가 Temporal Cloud 전체의 값인지 어느 범위인지는 홈페이지에서 확인하지 못했다.

## 쓰기 전에 알아둘 점

### 서버를 직접 운영하면 서버가 하나 더 늘어난다

Temporal Service는 애플리케이션의 상태를 저장하는 서비스이므로, 직접 호스팅하면 그 서비스와 저장소를 운영해야 한다.
Cloud를 쓰면 이 부담을 줄이지만 비용이 생긴다.
국내 사례인 Inflab은 EKS에 서버를 직접 띄우고 기존 Aurora PostgreSQL에 DB를 추가했고, 이 선택과 이관 과정은 `devops/jenkins-to-temporal.md`에 정리했다.

### 워크플로 코드와 Activity 코드의 제약이 다르다

문서는 Activity는 비결정적이어도 된다고 명시한다.[^act]
이는 반대로 워크플로 코드가 Event History로 상태를 되살리는 구조에서는 같은 입력에 같은 결과를 내야 한다는 제약이 있음을 시사한다.
이 제약의 구체적인 내용은 이 글에서 확인하지 못했다.
실제로 쓰기 전에 문서의 워크플로 제약 설명을 읽어야 한다.

HN에서 mfateev는 워크플로를 외부에 저장된 스키마 있는 데이터가 아니라 계산의 전체 상태, 즉 API 호출에 막힌 스레드와 스택의 지역 변수까지 포함한 것이라고 설명했다.[^mfateev-state]
그래서 버전 사이의 상태 변환을 데이터 마이그레이션처럼 정의할 수 없다는 것이다.

### 오래 도는 워크플로의 버전 관리

며칠에서 몇 주 걸리는 워크플로를 새 버전으로 배포하면 실행 중인 인스턴스는 어떻게 되느냐는 질문이 HN에 올라왔다.[^slotrans]
mfateev는 워크플로 전체에 버전을 붙이는 표준 방식은 새 기능에는 되지만 버그 수정에는 맞지 않는다고 답했다.
석 달 걸리는 워크플로의 끝부분에 버그가 있으면 수정본을 새 버전으로 배포해도, 그전에 시작한 워크플로는 석 달 동안 계속 실패하기 때문이다.
Temporal은 코드의 각 부분에 독립적으로 버전을 붙여 이를 해결하며, 여러 워크플로가 공유하는 라이브러리도 언제든 배포할 수 있고 여러 버전의 워커를 동시에 돌릴 필요가 없다고 했다.[^mfateev]

그는 사용자가 겪는 주된 문제가 바뀐 코드에 버전을 붙이는 것을 잊는 일이고, 이를 막는 보호 장치가 있다고 설명했다.
더 이상 필요 없는 옛 분기는 적극적으로 지우고, 버전별로 몇 개의 워크플로가 쓰이는지 세는 API를 제공한다는 것이다.[^mfateev-protections]
이 설명은 2020년 시점이므로 현재 방식은 문서에서 다시 확인해야 한다.

### 단순한 배치에는 과할 수 있다

홈페이지의 사례 대부분은 긴 실행, 보상, 사람 개입, AI 파이프라인처럼 상태를 오래 유지해야 하는 일이다.
컨테이너를 한 번 실행하고 끝나는 작업만 있다면 Temporal이 주는 내구성이 얼마나 쓰일지는 따져 봐야 한다.
Inflab의 이관 글에서도 Jenkins `docker run` 잡 대부분이 `containerOnly`라는 워크플로 하나로 옮겨졌다.

### 홈페이지의 수치는 서술이다

고객사 로고, 인용문, 가동률, 9년의 운영 기간은 모두 홈페이지가 보여 주는 것이다.
홈페이지는 많은 고객사를 로고로만 나열하고 각각이 Temporal을 어느 범위로 쓰는지는 말하지 않는다.
OpenAI 담당자의 인용문도 Temporal이 AI 시스템 구축에서 하는 역할에 대한 의견이지 사용 규모의 근거는 아니다.

## 체크리스트

- 해결하려는 문제가 장시간 실행, 재시도, 보상, 사람 개입처럼 상태를 오래 유지해야 하는 일인가?
- Temporal Service를 직접 호스팅할지 Cloud를 쓸지 정했는가?
- 실패하기 쉬운 호출을 Activity로 분리했고 그 Activity가 멱등한가?
- 워크플로 코드의 결정성 제약을 문서에서 확인했는가?
- 실행 이력의 보존 기간과 저장소 용량을 확인했는가?
- 워커가 내려갔을 때와 스케줄이 시작되지 않을 때를 감지하는 알림이 있는가?
- 팀이 Temporal의 개념(Workflow, Activity, Worker, Task Queue)을 익힐 시간이 있는가?

## 기억할 원칙

### 내구성은 서버가 아니라 실행 이력이 만든다

Temporal이 장애에서 돌아오는 방법은 서버가 죽지 않게 하는 것이 아니라 일어난 일을 기록해 두고 다시 만드는 것이다.
이 구조에서는 무엇을 기록하고 어디까지 되살릴지가 설계의 중심이므로, 도입할 때 가장 먼저 이해해야 하는 것은 Event History다.

### 실패를 기본으로 두면 재시도할 코드는 멱등해야 한다

Activity가 자동으로 재시도된다는 말은 같은 동작이 두 번 실행될 수 있다는 말이기도 하다.
재시도를 맡기는 대신 부작용이 겹치지 않게 만드는 책임이 코드에 남는다.

---

[^wf]: Temporal Documentation, [Temporal Workflow](https://docs.temporal.io/workflows)

[^act]: Temporal Documentation, [What is a Temporal Activity?](https://docs.temporal.io/activities)

[^mfateev-ceo]: <https://news.ycombinator.com/item?id=24818600>

[^acjohnson55]: <https://news.ycombinator.com/item?id=24815905>

[^mfateev-bpmn]: <https://news.ycombinator.com/item?id=24827734>

[^mfateev-visual]: <https://news.ycombinator.com/item?id=24818573>

[^mfateev-code]: <https://news.ycombinator.com/item?id=24819194>

[^mfateev-fork]: <https://news.ycombinator.com/item?id=24821869>

[^mfateev-state]: <https://news.ycombinator.com/item?id=24820929>

[^slotrans]: <https://news.ycombinator.com/item?id=24819317>

[^mfateev]: <https://news.ycombinator.com/item?id=24819558>

[^mfateev-protections]: <https://news.ycombinator.com/item?id=24820148>
