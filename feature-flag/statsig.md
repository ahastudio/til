# Statsig — 실험·피처 플래그·분석을 합친 제품 개발 플랫폼

<https://www.statsig.com/>

Show HN: [Show HN: Statsig – feature gates, dynamic config, experiments and more for devs](https://news.ycombinator.com/item?id=26629429) (13점, 1개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=48028790> (10점, 2개 댓글)

## 목차

- [소개](#소개)
- [소유 구조는 두 번 바뀌었다](#소유-구조는-두-번-바뀌었다)
- [주요 기능](#주요-기능)
- [가격과 사용](#가격과-사용)
- [고객 성과 지표](#고객-성과-지표)
- [Feature Gate는 이렇게 동작한다](#feature-gate는-이렇게-동작한다)
  - [평가는 결정론적이고 네트워크를 타지 않는다](#평가는-결정론적이고-네트워크를-타지-않는다)
  - [클라이언트 SDK와 서버 SDK는 평가 위치가 다르다](#클라이언트-sdk와-서버-sdk는-평가-위치가-다르다)
  - [클라이언트 초기화 전략이 첫 화면을 좌우한다](#클라이언트-초기화-전략이-첫-화면을-좌우한다)
- [시작하기: 게이트 하나를 코드까지 연결하기](#시작하기-게이트-하나를-코드까지-연결하기)
  - [콘솔에서 게이트를 만든다](#콘솔에서-게이트를-만든다)
  - [클라이언트 코드 (JavaScript와 React)](#클라이언트-코드-javascript와-react)
  - [서버 코드 (Node와 Python)](#서버-코드-node와-python)
  - [테스트에서는 값을 고정한다](#테스트에서는-값을-고정한다)
- [게이트 운영하기](#게이트-운영하기)
  - [점진적 출시와 킬 스위치](#점진적-출시와-킬-스위치)
  - [환경과 정리](#환경과-정리)
- [다음 단계: 설정, 실험, 레이어](#다음-단계-설정-실험-레이어)
- [다른 제품은 언제 쓰나](#다른-제품은-언제-쓰나)
- [트레이드오프와 함정](#트레이드오프와-함정)
- [도입 체크리스트](#도입-체크리스트)
- [분석](#분석)
  - [이 홈페이지의 핵심 메시지는 “도구 통합이 곧 속도다”라는 등식이다](#이-홈페이지의-핵심-메시지는-도구-통합이-곧-속도다라는-등식이다)
  - [인프라 수치는 신뢰가 아니라 규모의 증거로 배치되어 있다](#인프라-수치는-신뢰가-아니라-규모의-증거로-배치되어-있다)
  - [피처 플래그를 독립 제품이 아니라 진입점으로 배치한 전략](#피처-플래그를-독립-제품이-아니라-진입점으로-배치한-전략)
- [비평](#비평)
  - [성과 배수는 출처와 기준선을 숨긴 채 제시된다](#성과-배수는-출처와-기준선을-숨긴-채-제시된다)
  - [8개 기능의 통합은 강점이자 잠금(lock-in)의 다른 이름이다](#8개-기능의-통합은-강점이자-잠금lock-in의-다른-이름이다)
  - [홈페이지는 “왜 통합이어야 하는가”를 끝내 논증하지 않는다](#홈페이지는-왜-통합이어야-하는가를-끝내-논증하지-않는다)
  - [홈페이지는 소유 구조가 두 번 바뀐 사실을 한 줄로만 말한다](#홈페이지는-소유-구조가-두-번-바뀐-사실을-한-줄로만-말한다)
- [인사이트](#인사이트)
  - [실험 플랫폼의 통합은 “데이터 중력”이 만드는 필연적 수렴이다](#실험-플랫폼의-통합은-데이터-중력이-만드는-필연적-수렴이다)
  - [“실험 속도”라는 지표는 측정 가능성이 만든 대리 목표다](#실험-속도라는-지표는-측정-가능성이-만든-대리-목표다)
  - [피처 플래그를 “공짜 입구”로 두는 전략은 메트칼프의 법칙을 노린다](#피처-플래그를-공짜-입구로-두는-전략은-메트칼프의-법칙을-노린다)
  - [제품과 팀이 갈라지면 남는 것은 계약과 이식성이다](#제품과-팀이-갈라지면-남는-것은-계약과-이식성이다)

## 소개

Statsig는 스스로를 “modern product development platform”으로 소개하는 SaaS다.
피처부터 AI 기반 경험까지, 각 릴리스가 고객에게 어떻게 도달하는지를
테스트하는 것을 핵심 가치로 내세운다.
전통적으로 서로 다른 도구로 나뉘어 있던 실험(experimentation),
피처 관리(feature management), 제품 분석(product analytics)을
하나의 플랫폼으로 통합한 점이 특징이다.

홈페이지는 제품의 규모를 수치로 강조한다.
하루 1조(1+ trillion) 건 이상의 이벤트를 처리하고,
월간 고유 실험 대상자(unique monthly experiment subjects)는
25억(2.5 billion) 명,
API와 콘솔의 가동률은 99.99%, 초기화 이후 평가 지연은 1ms 미만이라고 밝힌다.
고객 사례로 Brex, Ancestry, Notion, Lime 네 곳의 수치를 내걸고,
후기에는 OpenAI의 ChatGPT 엔지니어링 관리자 등 마흔 건 가까운 말을 싣는다.
이 문서가 읽은 홈페이지 텍스트에는 Microsoft,
Atlassian, SoundCloud가 나오지 않는다.
로고 이미지로만 들어 있을 수 있어서 이 문서는 확인하지 못했다.

가격은 “업계에서
가장 관대한 무료 티어 또는 확장 가능한 엔터프라이즈 가격”이라고만
표현하며, 홈페이지에 구체적인 금액은 드러내지 않는다.
금액은 가격 페이지에 있다(아래 절).

## 소유 구조는 두 번 바뀌었다

홈페이지 맨 위 띠는 Statsig가 Amplitude 가족의 일부라고 알린다.
이 한 줄 뒤에 인수가 두 번 있었다.

Statsig는 2021년 2월에 시작했다고 스스로 밝힌다.[^openai-blog]
같은 해 3월 29일 HN에 올린 첫 Show HN에서 공동 창업자 vijayer는
Facebook 출신의 작은 팀이라며 기능 게이트, 동적 설정, 이벤트 로깅을
JS, Node, Swift SDK로 내놓는 첫 미리보기를 소개했고,
곧 기능 출시 기반 인사이트와 지표 디버깅을 낼 계획이라고 적었다.[^vijayer]
지금 홈페이지의 SDK 목록은 React부터 Rust까지 스무 개 남짓이고
가격 페이지는 30개 넘는 SDK라고 말한다.[^pricing]

2025년 9월 2일 Statsig는 OpenAI에 합류한다고 밝혔다.[^openai-blog]
HN의 dantihanyi는 OpenAI가 지난 9월에 11억 달러에 인수했다고 전했다.
가격은 Statsig의 글이 아니라 이 댓글이 링크한 보도에서 나온 것이다.[^dantihanyi]
2026년 5월 5일에는 Amplitude가 Statsig의 브랜드와 고객을 넘겨받고
클라우드와 데이터 웨어하우스에 걸친 현재 플랫폼을 유지하고 발전시키며
OpenAI에 있는 Statsig 팀과 전환기에 협력한다고 발표했다.[^amplitude-blog]
Statsig의 OpenAI 합류 글에는 이 사실이 머리말로 덧붙었다.
원래 팀은 OpenAI에 남았고
제품과 브랜드와 고객은 Amplitude 가족이 되었다는 내용이다.[^openai-blog]

Amplitude의 제품 담당 부사장 Chris Yu는 6월 17일 글에서
Amplitude 소속 약 50명이 Statsig 플랫폼을 유지하고
고객을 지원하고 앞날을 계획한다고 썼다.
처음 여섯 주(Phase 0)는 인계에 썼고
원래 팀이 코드베이스와 운영과 로드맵을 설명해 주었다고 한다.
1단계의 우선순위로는 제어와 거버넌스,
AI 중심 워크플로, 플랫폼 규모와 성능을 꼽았다.
Amplitude의 이벤트와 코호트가 Statsig 안에서 쓰이고
Statsig 실험 결과가 Amplitude 안에 나타나게
하는 연결은 3분기 말까지로 약속했다.[^phase1]
이 문서는 그 약속의 이행 여부를 확인하지 못했다.
Statsig 블로그에는 이후에도 10월 7일 MCP v3
같은 글이 계속 올라온다.[^blog-index]

## 주요 기능

| 기능                  | 설명                             |
| --------------------- | -------------------------------- |
| Experimentation       | 고급 통계 분석 기반 A/B 테스트   |
| Feature Management    | 통제된 릴리스를 위한 피처 플래그 |
| Product Analytics     | 사용자 행동 추적 및 인사이트     |
| Session Replay        | 사용자 상호작용 시각화           |
| Web Analytics         | 웹사이트 성능 지표               |
| Infra Analytics       | 인프라 모니터링                  |
| Marketing Experiments | 전환(conversion) 테스트 도구     |
| Warehouse Native      | 데이터 웨어하우스 통합           |

피처 플래그는 이 묶음의 한 축이다.
Statsig에서 피처 플래그는 단순한 온/오프 토글이 아니라,
같은 시스템 안에서 곧바로 실험과 분석으로 이어지는 진입점으로 설계되어 있다.
플래그로 기능을 일부 사용자에게만 노출하고,
그 노출을 곧 실험 그룹으로 삼아 통계 분석을 돌리고,
제품 분석으로 영향을 측정하는 흐름이 하나의 플랫폼 안에서 닫힌다.

Warehouse Native 모드는 고객의 데이터 웨어하우스 위에서
직접 동작하는 배포 형태로,
이벤트 데이터를 Statsig로 복제하지 않고 고객 인프라 안에 두려는 조직을 겨냥한다.

## 가격과 사용

가격 페이지는 세 단계를 보여 준다.
Developer는 무료이고 신용카드가 필요 없다.
월 200만 이벤트, 무제한 플래그와 설정 확인,
월 5만 개 세션 리플레이, 무제한 좌석, 1년 분석 보존이 들어 있다.
Pro는 월 150달러이고 이벤트 500만 개를 포함하며 그 뒤에는 1,000개당 0.05달러다.
세션 리플레이 월 10만 개, 고급 실험과 고급 제품 분석, 무제한 분석 보존,
변경 검토와 승인, API 제어가 더해진다.
Enterprise는 맞춤 계약이고 웨어하우스 네이티브 배포,
외부 전송 통합, 웨어하우스 가져오기,
SSO와 역할 기반 접근 제어, 우선 지원, HIPAA 적격(BAA 필요)이 더해진다.
페이지는 고객의 90%가 무료로 쓴다고 밝힌다.[^pricing]

가격 페이지는 실험에서 쓰는 통계 기법도 목록으로 보여 준다.
베이지안과 빈도주의 분석, CUPED, 본페로니 보정, 윈저화, 벤자미니-호크버그 절차,
이질적 효과의 자동 탐지, 실험 간 상호작용 탐지,
층화 표집, 순차 검정, 스위치백 검정,
비열등성 검정이다.
홈페이지의 고급 통계 엔진이라는 말은 이 목록이 뒷받침한다.
단계별로 어느 기법이 어느 요금제에 들어 있는지는
이 문서가 텍스트로는 가려내지 못했다.[^pricing]
비용이 붙는 단위는 플래그 확인 횟수가 아니라 이벤트다.
자세한 계산은 아래 함정 절에 있다.[^pricing]
한 가지 눈에 띄는 점은 웨어하우스 네이티브가
모든 플랫폼에 포함된 항목으로 소개되면서
요금 비교에서는 Enterprise에만 들어 있는 것처럼 적혀 있다는 점이다.[^pricing]

## 고객 성과 지표

홈페이지는 고객 사례를 구체적 배수로 제시하고,
각 사례 페이지가 그 수치의 출처다.
사례 페이지를 열어 보면 기준선이 홈페이지가 보여 주는 것보다 구체적이다.

| 고객     | 홈페이지의 수치                            | 사례 페이지가 덧붙이는 기준선                                                   |
| -------- | ------------------------------------------ | ------------------------------------------------------------------------------- |
| Notion   | 실험 속도 30배, 기능 600개 이상            | 분기당 한 자릿수에서 수백 건으로, 활성화율 6% 증가. 이전에는 자체 도구[^notion] |
| Ancestry | 연 70건에서 600건 이상                     | 이전에는 수동 실험. 성장팀이 4명에서 25명으로 6배[^ancestry]                    |
| Brex     | 데이터 과학자 시간 50% 감소, 비용 20% 절감 | 이전에는 다른 플랫폼 사용. 실험 100건 이상[^brex]                               |
| Lime     | 환불 20% 감소, 취소 여행 5% 감소           | 이전에는 데이터 과학팀이 실험을 일일이 감독[^lime]                              |

## Feature Gate는 이렇게 동작한다

### 평가는 결정론적이고 네트워크를 타지 않는다

Feature Gate는 사용자 한 명에게 켜짐(true)이나
꺼짐(false)을 돌려주는 규칙 묶음이다.
같은 사용자와 같은 규칙이면 몇 번을 물어도 같은 답이 나온다.
판정은 사용자 ID와 규칙마다 다른 salt를 이어 붙인 문자열의 SHA256 해시를
10,000으로 나눈 나머지로 이뤄지고,
그 값이 규칙의 통과 비율보다 작으면 통과한다.[^ev]
오픈소스 Node 서버 SDK의 평가 코드도 같은 구조다.
통과 비율이 0%나 100%면 해시를 계산하지 않고 바로 답하고,
그 사이면 salt와 ID를 이어 붙인 해시를 10,000으로 나눈 나머지를
통과 비율의 100배와 비교한다.[^evaluator]
이 코드 저장소는 2026년 9월에도 갱신되었고
보관(archive) 상태가 아니다.[^evaluator]

게이트 하나 안에서 평가 순서는 정해져 있다.
먼저 ID 단위 오버라이드를 보고,
그다음 세그먼트나 다른 게이트를 조건으로 쓰는 오버라이드,
그다음 홀드아웃을 본다.
그 뒤에 규칙을 위에서 아래로 훑어 처음 조건이 맞는 규칙을 적용한다.[^ev]
규칙에 조건이 맞았는데 통과 비율에서 떨어진 사용자는
아래 규칙으로 넘어가지 않고 그 자리에서 거짓을 받는다.[^cond]
규칙이 하나도 없는 게이트는 기본이 거짓이다.[^create]

salt가 규칙마다 따로 있다는 점이 운영에서 중요하다.
통과 비율을 올리면 먼저 통과했던 사용자가 그대로 남고 새 사용자가 더해진다.
비율을 내리면 가장 늦게 들어온 구간부터 빠진다.
같은 규칙을 다시 쓰면 같은 사용자가 다시 노출되고,
재솔팅(resalt)을 하면 구간이 새로 섞인다.[^ev][^cond]

### 클라이언트 SDK와 서버 SDK는 평가 위치가 다르다

클라이언트 SDK는 초기화할 때 사용자 한 명의 모든 게이트 결과를
Statsig 서버에서 한꺼번에 받아 온다.
서버 SDK는 반대로 규칙 전체를 내려받아 메모리에 두고 요청마다 직접 계산한다.
초기화가 끝난 뒤에는 확인마다 네트워크 호출이 없고
1ms 미만이라고 문서는 말한다.[^ev]
서버 SDK는 사용자 속성을 기억하지 않으므로
호출마다 사용자 전체를 넘겨야 한다.[^ev]
노출(exposure) 이벤트는 코드가 `checkGate`나
`getExperiment`를 부를 때만 기록된다.[^ev]

| 구분             | 클라이언트 SDK                    | 서버 SDK                      |
| ---------------- | --------------------------------- | ----------------------------- |
| 키               | 공개되어도 되는 클라이언트 키     | 비밀 서버 키                  |
| 규칙 위치        | Statsig 서버가 평가해 결과만 전달 | 규칙 전체를 메모리에 내려받음 |
| 동기화           | 사용자를 바꿀 때 다시 요청        | 기본 10초 간격으로 폴링       |
| 이벤트 전송 주기 | 기본 10초                         | 기본 60초                     |

위 표의 키, 폴링, 전송 주기 항목은 문서 기준이다.[^init][^servercore][^cvs]

### 클라이언트 초기화 전략이 첫 화면을 좌우한다

클라이언트 초기화는 캐시 확인, 안정 ID(STATSIG_STABLE_ID) 생성,
캐시나 기본값으로 초기화 표시, 네트워크 요청, 응답 반영 순서로 진행된다.[^init]
문서는 네 가지 전략을 비교한다.

| 전략                | 속도 | 일관성 | 비고                                 |
| ------------------- | ---- | ------ | ------------------------------------ |
| 비동기, await       | 느림 | 높음   | 최신 값, 가장 단순                   |
| 부트스트랩          | 빠름 | 높음   | 서버가 값을 내려 주는 추가 작업 필요 |
| 비동기, await 안 함 | 빠름 | 낮음   | 화면이 깜빡일 수 있음                |
| 동기(캐시만)        | 빠름 | 낮음   | 첫 방문 사용자는 배정되지 않음       |

표의 평가는 문서의 비교를 줄인 것이다.[^init]
처음 쓴다면 await 방식으로 시작하고,
로딩 지연이나 깜빡임이 문제가 될 때
부트스트랩으로 옮기는 것이 문서의 흐름과 맞다.
이 순서는 이 문서의 제안이다.

## 시작하기: 게이트 하나를 코드까지 연결하기

### 콘솔에서 게이트를 만든다

1. 콘솔의 Feature Gates에서 새 게이트를 만들고 이름을 정한다.
   이름은 표시용이고 ID는 만든 뒤에 바꿀 수 없다.[^create]
2. 규칙을 추가한다. 규칙은 조건과 통과 비율로 이뤄진다.
   조건에는 사용자 ID, 이메일, 국가, 앱 버전, 브라우저, 운영체제,
   세그먼트, 다른 게이트 통과 여부, 환경 단계(tier), 사용자 정의 필드,
   시각 같은 항목이 있다.[^cond]
3. 처음에는 규칙을 Everyone 100%로 두는 대신
   내부 직원 이메일 같은 조건과 100%로 시작하는 편이 안전하다.
   이 순서는 이 문서의 제안이다.
4. 필요하면 특정 ID를 항상 통과나 항상 실패로 고정하는 오버라이드를 넣는다.
   오버라이드된 사용자는 분석에서 빠진다.[^overrides]
5. 콘솔의 Test Gate 도구에 사용자 속성을 넣어 결과를 미리 확인한다.[^testgate]

Statsig 튜토리얼의 게이트 이름은 문서 안에서도 엇갈린다.
본문은 `example_gate`를 만들라 하고 코드는 `check_user`를 확인하며
화면의 이름은 “Example Gate”다.[^tutorial]
아래 예제는 실제 게이트 ID와 코드의 문자열이 같은지부터 확인하라는 뜻에서
`new_checkout`이라는 이름 하나로 통일했다.

### 클라이언트 코드 (JavaScript와 React)

React에서는 `@statsig/react-bindings` 3.33.5를 쓴다.[^npm-react]
튜토리얼은 `npm install @statsig/react`를 안내하지만
이 문서가 npm에서 조회했을 때 그 이름의 패키지는 없었다.[^tutorial]

```tsx
import * as React from 'react';
import {
  StatsigProvider,
  useClientAsyncInit,
  useStatsigClient,
} from '@statsig/react-bindings';

function Checkout() {
  const { client, checkGate, getExperiment, logEvent } = useStatsigClient();
  const label = getExperiment('checkout_button').get('label', 'Buy now');
  return (
    <button
      onClick={() => {
        logEvent('checkout_click', 1, { surface: 'cart' });
        void client.flush();
      }}
    >
      {checkGate('new_checkout') ? 'New: ' : ''}
      {label}
    </button>
  );
}

export function App({ userID }: { userID: string }) {
  const { client, isLoading } = useClientAsyncInit('client-key', { userID });
  if (isLoading) return <div>Loading...</div>;
  return (
    <StatsigProvider client={client}>
      <Checkout />
    </StatsigProvider>
  );
}
```

React 바깥에서는 `@statsig/js-client` 3.33.5를 직접 쓴다.[^jssdk]
아래 코드는 개발 환경 단계를 지정하고,
`@statsig/js-local-overrides`로 로컬에서 게이트 값을 고정한다.[^testing]

```ts
import { StatsigClient } from '@statsig/js-client';
import { LocalOverrideAdapter } from '@statsig/js-local-overrides';

const overrideAdapter = new LocalOverrideAdapter();
overrideAdapter.overrideGate('new_checkout', true);

const client = new StatsigClient(
  'client-key',
  { userID: 'u_123', email: 'dev@example.com' },
  { environment: { tier: 'development' }, overrideAdapter },
);
await client.initializeAsync();

if (client.checkGate('new_checkout')) {
  // 새 결제 화면
}
const exp = client.getExperiment('checkout_button');
const label = exp.get('label', 'Buy now');
client.logEvent('add_to_cart', 19.99, { sku: 'A1' });

await client.updateUserAsync({ userID: 'u_456' });
await client.flush();
await client.shutdown();
```

위 세 코드(JavaScript, React, 아래 Node)는 이 문서가 패키지의 타입 정의를 받아
TypeScript 5.9.3 strict 모드로 검사해 통과시켰다.
메서드 이름을 일부러 틀리면 같은 검사가 오류를 내는 것도 확인했다.
검사는 컴파일 수준이므로 실제 키로 서버에 붙어 돌려 본 것은 아니다.

React 훅 `useGateValue`와 `useFeatureGate`는 렌더링할 때 노출을 기록한다고
문서가 경고한다.[^react]
같은 컴포넌트가 여러 번 렌더링되는 구조라면 노출이 부풀 수 있다.

### 서버 코드 (Node와 Python)

Node는 `@statsig/statsig-node-core` 0.23.2다.[^npm-nodecore]
Next.js에서는 `next.config`의 `serverExternalPackages`에
이 패키지를 넣어야 한다.[^nodecore]

```ts
import { Statsig, StatsigUser } from '@statsig/statsig-node-core';

const statsig = new Statsig(process.env.STATSIG_SERVER_KEY!, {
  environment: 'staging',
});
await statsig.initialize();

const user = new StatsigUser({
  userID: 'u_123',
  email: 'dev@example.com',
  custom: { plan: 'pro' },
  privateAttributes: { age: '20-29' },
});

if (statsig.checkGate(user, 'new_checkout')) {
  // 새 결제 흐름
}
const label = statsig
  .getExperiment(user, 'checkout_button')
  .getValue('label', 'Buy now');
statsig.logEvent(user, 'add_to_cart', 19.99, { sku: 'A1' });

await statsig.flushEvents();
await statsig.shutdown();
```

Python은 `statsig-python-core` 0.23.2다.[^pypi-pycore]
아래 코드는 이 문서가 패키지의 `.pyi` 타입 정의와 대조하고
문법 검사만 거쳤다. 실행하지는 않았다.

```python
import os
from statsig_python_core import Statsig, StatsigOptions, StatsigUser

options = StatsigOptions()
options.environment = "staging"
statsig = Statsig(os.environ["STATSIG_SERVER_KEY"], options)
statsig.initialize().wait()

user = StatsigUser("u_123", email="dev@example.com", custom={"plan": "pro"})
if statsig.check_gate(user, "new_checkout"):
    pass  # 새 결제 흐름

label = statsig.get_experiment(user, "checkout_button").get_string(
    "label", "Buy now"
)
statsig.log_event(
    user=user, event_name="add_to_cart", value=19.99, metadata={"sku": "A1"}
)
statsig.shutdown().wait()
```

서버 SDK는 프로세스가 끝나기 전에 `shutdown`을 불러야 쌓인 이벤트가 나간다.
이 문서는 종료 시 `shutdown`이 이벤트를 비우는 것으로 보고
예제를 만들었다.[^servercore]
Node 문서 일부는 `Statsig.overrideGate`를 대문자 정적 호출로 적지만,
0.23.2의 타입 정의에서 `overrideGate`는 인스턴스 메서드다.[^nodecore]
FAQ에는 `statsig.flush()`라는 이전 이름이 남아 있고
0.23.2의 Node 코어에는 `flushEvents()`가 있다.[^faq]

### 테스트에서는 값을 고정한다

문서는 테스트에서 네트워크를 막는 `localMode`와
`overrideGate`, `overrideConfig`로 값을 고정하라고 안내한다.[^testing]
앞의 클라이언트 예제처럼 `LocalOverrideAdapter`를 쓰면
게이트 결과를 테스트마다 정할 수 있다.

## 게이트 운영하기

### 점진적 출시와 킬 스위치

출시 순서로 문서는 2%, 10%, 50%, 100%를 권한다.[^cond]
모범 사례 문서는 0%에서 시작하는 변형도 보여 준다.[^bestp]
규칙 하나를 Everyone 100%로 두면 모두에게 켜지고 0%로 내리면 모두에게 꺼진다.
이 0% 규칙이 곧 킬 스위치다.[^create]
코드를 다시 배포하지 않아도 되는 것이 게이트의 핵심 이점이다.

운영에서 쓰는 보조 기능은 다음과 같다.

- 예약 롤아웃은 15분 단위로 비율을 단계적으로 올리도록 미리 정한다.[^sched]
- 출시를 단계별로 나눠 순서대로 진행하는 일은 Release Pipelines로 짠다.
  이 기능은 Server Core에서만 되고
실험이나 예약 롤아웃과 같이 쓸 수 없다.[^relpipe]
- Safeguards는 지표가 나빠지면 알림을 보내는 장치이고
Pro 이상에서 쓴다.[^safeguards]
- 노출 로그는 Diagnostics의 Exposure Stream에서 바로 확인한다.[^exposures]

### 환경과 정리

환경은 Development, Staging, Production 세 단계가 기본이다.
SDK에 단계를 지정하지 않으면 production으로 간주한다.[^envs]
같은 게이트라도 단계마다 규칙을 달리 둘 수 있다.
개발 환경에서는 켜고 운영 환경에서는 끄는 식이다.[^envs]

게이트는 쌓이면 부채가 된다.
문서는 100%나 0%로 30일을 넘기면 Launched나 Disabled 상태로 바꾸고,
코드 참조는 60일이 지나면 지우고,
7일 동안 확인이 0건이면 보관(Archive)하라고 권한다.[^lifecycle]
보관되거나 삭제되거나 알 수 없는 게이트는 거짓을 돌려준다.[^ev]
그래서 코드에서 먼저 지우지 않고 콘솔에서 게이트를 지우면
그 기능이 갑자기 꺼진다.
수명이 긴 게이트는 Permanent로 표시해 정리 알림에서 빼고,
Stale 게이트는 월간 이메일이나 Slack으로 알려 준다.[^stale]

## 다음 단계: 설정, 실험, 레이어

게이트가 켜짐과 꺼짐이라면 Dynamic Config는 JSON 값을 돌려준다.
크기 한도는 100KB다.[^dynconfig]
Statsig의 마이그레이션 안내는 LaunchDarkly의 불리언 플래그를 Feature Gate로,
문자열과 숫자와 JSON 플래그를 Dynamic Config로 옮기라고 한다.[^migrate-ld]
즉 값의 모양으로 둘을 가른다.

실험은 게이트를 타기팅 조건으로 쓰고 그룹별 값을 돌려준다.
무작위 단위로는 사용자 ID, 안정 ID, 세션이 있다.[^gatevsexp]
한 가지 헷갈리는 점이 있다.
게이트의 통과 비율(pass %)과 실험의 할당
비율(allocation %)은 다른 개념이다.[^gatevsexp]
레이어는 1,000개 구간에 실험을 겹치지 않게 배정하고,
실험이 시작되면 그 레이어의 구조는 잠긴다.[^layers]
홀드아웃은 전체 사용자의 1~50%를 새 기능에서
빼 두고 누적 효과를 본다.[^holdouts]
Parameter Store는 코드가 게이트인지 실험인지 몰라도
되도록 이름만 바라보게 한다.[^paramstores]

## 다른 제품은 언제 쓰나

| 필요                      | 제품              | 문서가 말하는 쓰임                       |
| ------------------------- | ----------------- | ---------------------------------------- |
| 배포 위험 줄이기          | Feature Gates     | 점진 출시, 킬 스위치                     |
| 효과 측정                 | Experiments       | 통계 분석, 레이어, 홀드아웃              |
| 변형을 자동으로 몰아주기  | Autotune          | 밴딧 방식(맥락 기반 포함)[^autotune]     |
| 사용자 행동 분석          | Product Analytics | 퍼널, 리텐션, 분포, 여정[^prodanalytics] |
| 화면에서 무슨 일이 있었나 | Session Replay    | rrweb 기반 녹화[^sessionreplay]          |
| 사이트 방문 지표          | Web Analytics     | 스크립트 태그와 자동 수집[^webanalytics] |
| 데이터를 웨어하우스에 둠  | Warehouse Native  | 분석을 고객 웨어하우스에서 실행[^whn]    |

이 표는 앞서 본 8개 기능 목록의 쓰임을 문서의 설명으로 풀어 쓴 것이다.
자동화에는 Console API(`https://statsigapi.net`, 헤더 `STATSIG-API-KEY`)와
CLI `@statsig/siggy`가 있다.[^consoleapi][^cli]
Console API의 변경 요청은 15분에 약 1,800회까지다.[^consoleapi]

## 트레이드오프와 함정

- 초기화 지연. 클라이언트에서 await 방식은 첫 화면이 늦고,
  await하지 않는 방식은 깜빡임을 만든다.[^init]
- 안정 ID 불일치. 로그인 전에는 안정 ID로, 후에는 사용자 ID로 배정하면
  같은 사람이 다른 그룹을 받을 수 있다.[^gatevsexp]
- 노출 잡음. 렌더링마다 노출이 기록되는 훅이 있다.[^react]
  또 0%와 100% 규칙은 기본으로 노출을 기록하지 않아서
  완전 출시 후에는 분석 데이터가 끊긴다.[^exposures]
- 오래된 게이트. 보관되거나 삭제된 게이트는 조용히 거짓이 된다.[^ev]
- 비용 구조. 가격 페이지 FAQ는 플래그와 설정 확인은 무제한이고,
  측정되는 이벤트는 지표 증가(Metric Lifts)를 켠 게이트의 부분 출시 노출과
  로그 이벤트와 지표라고 설명한다.
  노출은 클라이언트 60분, 서버 1분 단위로 중복을 제거한다.[^pricing]
  그런데 문서 FAQ는 게이트나 실험 확인과 이벤트가 모두 과금 대상이라고 적어
  두 설명이 어긋난다.[^faq]
  어느 쪽이 맞는지 이 문서는 가리지 못했다.
- 문서 오류. 앞서 본 패키지 이름, 게이트 이름, 메서드 이름의 불일치가 있어
  예제는 복사하기 전에 타입 정의와 맞춰 봐야 한다.[^tutorial][^faq]

경쟁 제품과의 비교는 Statsig 자신의 마이그레이션 안내에서 확인한 만큼만 쓴다.
LaunchDarkly에서 옮길 때 플래그 소유자와 태그와 팀과 변경 이력은 옮겨지지 않고,
큰 ID 목록 세그먼트도 자동으로 옮겨지지 않는다.[^migrate-ld]
OpenFeature와 Unleash와의 비교는 이 문서가 확인하지 못해 싣지 않는다.

## 도입 체크리스트

- 클라이언트 키와 서버 키를 구분해 저장했는가.
- 초기화 전략과 로딩 중 화면을 정했는가.
- 코드의 게이트 문자열이 콘솔의 ID와 같은가.
- 환경 단계를 개발과 운영에서 다르게 지정했는가.
- 게이트마다 담당자와 정리 시한을 정했는가.
- 완전 출시 뒤 코드의 분기를 제거하는 작업을 일정에 넣었는가.
- 테스트에서 오버라이드로 값을 고정했는가.
- 노출 이벤트 양을 한 달 뒤 청구와 대조할 계획이 있는가.

## 분석

### 이 홈페이지의 핵심 메시지는 “도구 통합이 곧 속도다”라는 등식이다

홈페이지가 나열한 8개 기능은 표면적으로는 서로 다른 제품 카테고리다.
실험 플랫폼, 피처 플래그 서비스, 제품 분석, 세션 리플레이는
각각 독립된 SaaS 시장을 이루고 있고, 카테고리마다 강력한 단독 경쟁자가 있다.
Statsig의 포지셔닝은 이들을 한 플랫폼에 모으는 것 자체를 가치로 제시한다.
Notion의 “30배”, Ancestry의 “9배” 같은 지표는 기능의 우수성이 아니라
통합이 만들어낸 속도를 증거로 내세운다.

이 등식에는 숨은 전제가 있다.
실험이 느린 이유가 도구의 성능이 아니라 도구 사이의 마찰이라는 가정이다.
피처 플래그, 실험 설정, 분석 대시보드가 서로 다른 시스템에 흩어져 있으면
한 번의 실험을 돌리는 데 여러 팀과 여러 도구를 거쳐야 한다.
Statsig는 그 왕복을 없애는 것을 팔고 있다.
“데이터 과학자 시간 50% 감소”라는 Brex 지표가 정확히 이 지점을 겨냥한다.

### 인프라 수치는 신뢰가 아니라 규모의 증거로 배치되어 있다

하루 1조 이벤트, 월 25억 실험 대상자, 99.99% 가동률, 1ms 미만 지연이라는
네 숫자는 단순한 자랑이 아니다.
실험 플랫폼을 도입하려는 조직이 가장 먼저 걱정하는 것은
“우리 트래픽 규모를 감당하는가”와 “평가 지연이 사용자 경험을 해치지 않는가”다.
1ms 미만 지연은 피처 플래그 평가가 요청 경로(request path)에 들어가도
체감되지 않는다는 약속이고, 99.99%는 플래그 시스템 장애가 곧 서비스 장애가 되는
공포에 대한 답이다.

이 수치 배치는 의도적이다.
홈페이지는 기능 설명보다 먼저 규모와 안정성을 제시함으로써,
“이미 검증된 인프라”라는 인상을 만든다.
후기에 OpenAI의 ChatGPT 엔지니어링 관리자의 말을 싣는 것도 같은 맥락이다.
가장 까다롭고 빠르게 움직이는 조직이 쓴다는 사실 자체가 기술 검증을 대신한다.
다만 OpenAI는 2025년 9월 이후 고객이 아니라 Statsig의 원래 팀이 합류한 회사이고,
제품은 다시 Amplitude로 넘어갔다.[^openai-blog][^amplitude-blog]
후기가 그 사이의 시간을 말해 주지 않는다는 점은 비평에서 다룬다.

### 피처 플래그를 독립 제품이 아니라 진입점으로 배치한 전략

Statsig는 피처 플래그를 8개 기능 중 하나로 나열하지만,
플랫폼 구조상 피처 플래그는 다른 모든 기능으로 들어가는 문이다.
플래그로 노출을 제어하는 순간, 그 노출 데이터가 곧 실험의 처리/대조군이 되고,
같은 데이터가 제품 분석과 세션 리플레이의 분석 단위가 된다.
즉 피처 플래그는 데이터를 플랫폼 안으로 끌어들이는 입구 역할을 한다.

이 설계는 경쟁 구도에서 중요하다.
LaunchDarkly도 플래그에 지표를 묶는 Experimentation 기능을 문서에 두고 있어서,
플래그 제품은 측정을 다른 도구로 넘긴다는 구분은 더 이상 맞지 않는다.[^ld-exp]
Statsig는 플래그를 입구로 삼아 실험과 분석까지 한 플랫폼에 묶는다.
홈페이지가 피처 플래그를 전면에 내세우지 않는 것은,
그것이 목적이 아니라 더 큰 통합으로 가는 경로이기 때문이다.

## 비평

### 성과 배수는 출처와 기준선을 숨긴 채 제시된다

“30배”, “9배”, “50% 감소” 같은 숫자는 강력해 보이지만,
홈페이지 본문은 이 숫자가 무엇 대비 무엇인지를 밝히지 않는다.
사례 페이지를 열어 보면 기준선이 일부 나온다.
Notion의 “실험 속도 30배”는 분기당 한 자릿수에서 수백 건으로 늘어난 것이고,
이전에는 자체 도구가 있었는데 플래그를 일일이 붙이는 데 시간이 걸리고
겹치지 않게 실험을 돌리기 어려웠다고 한다.[^notion]
Notion은 도구가 아예 없던 팀이 아니었다.
비교 대상은 도구의 부재가 아니라 한계가 분명한 자체 도구다.
그래도 분기당 한 자릿수라는 기준선이 낮다는 사실은 남고,
기준선이 낮을수록 배수가 커진다는 점은 그대로다.

이런 배수는 마케팅 지표의 전형적 함정을 안고 있다.
기준선이 낮을수록 배수는 극적으로 커진다.
연 70건에서 600건으로 늘었다는 Ancestry 사례도,
실험 건수의 증가가 곧 제품 성과의 증가를 의미하지는 않는다.
같은 사례 페이지는 성장팀이 4명의 소규모 팀에서
25명으로 6배 커졌다고 적는다.[^ancestry]
실험이 9배 늘 때 실험을 설계하고 분석하는 사람도 6배 늘었다면,
증가의 얼마가 도구 덕분이고 얼마가 인력 덕분인지는 분리되지 않는다.
Brex의 “데이터 과학자 시간 50% 감소”도 이전에 쓰던 다른 플랫폼과의 비교이고,
도구 교체 효과와 통합 효과를 가르는 설명은 없다.[^brex]
의미 없는 실험을 600건 돌리는 것은 70건의 좋은 실험보다 나쁠 수 있다.
홈페이지는 “속도”를 미덕으로 전제하지만, 속도가 곧 가치라는 등식 자체가
검증되지 않은 채 제시된다.

### 8개 기능의 통합은 강점이자 잠금(lock-in)의 다른 이름이다

모든 기능을 한 플랫폼에 모으는 것은 마찰을 줄이지만,
동시에 그 플랫폼에서 빠져나오기를 극도로 어렵게 만든다.
피처 플래그, 실험 데이터, 분석 대시보드, 세션 리플레이가 한 시스템에 얽히면,
이 중 하나만 다른 도구로 옮기는 것이 거의 불가능해진다.
홈페이지가 자랑하는 “통합”은 고객 입장에서는 “전환 비용”이다.

이 잠금은 인프라 수치와 결합될 때 더 강해진다.
하루 1조 이벤트가 이미 Statsig를 통과하고 있다면,
그 데이터 파이프라인을 재구축하는 비용은 천문학적이다.
Warehouse Native 모드가 “데이터는 당신 것”이라는 인상으로 이 우려를 누그러뜨리려
하지만, 분석 로직과 실험 설계가 Statsig 플랫폼에 묶여 있는 한
데이터의 물리적 위치는 잠금의 본질을 바꾸지 못한다.

### 홈페이지는 “왜 통합이어야 하는가”를 끝내 논증하지 않는다

홈페이지의 모든 메시지는 통합이 좋다는 결론을 전제한다.
그러나 통합이 항상 옳은 선택은 아니다.
각 카테고리의 단독 강자(LaunchDarkly, FullStory 등)를 조합해 쓰는 것이
특정 조직에는 더 나을 수 있다.
각 영역에서 가장 깊은 기능을 쓰고, 필요한 부분만 연결하는 전략 말이다.

홈페이지는 이 대안을 전혀 언급하지 않는다.
통합 플랫폼의 약점은 각 기능이 단독 제품만큼 깊지 못할 수 있다는 점이다.
Statsig의 세션 리플레이가 FullStory만큼 정교한가?
제품 분석이 Amplitude만큼 풍부한가?
이 질문은 이제 같은 회사 안의 질문이 되었다. Amplitude가
Statsig를 넘겨받았기 때문이다.[^amplitude-blog]
홈페이지는 “다 된다”고 말할 뿐, 각 기능의 깊이를 단독 경쟁자와 비교하지 않는다.
“하나로 충분하다”는 주장은 매력적이지만, 그 충분함의 기준은 제시되지 않는다.

### 홈페이지는 소유 구조가 두 번 바뀐 사실을 한 줄로만 말한다

맨 위 띠의 Amplitude 가족이라는 말과, 후기 목록에 남은 OpenAI의 목소리와,
Statsig 블로그의 OpenAI 합류 글 머리말이 이 이력을 보여 주는 전부다.
홈페이지의 본문은 누가 제품을 만들고 있는지를 말하지 않는다.
정작 도입 판단에 영향을 주는 정보다.

Amplitude의 발표는 원래 팀을 OpenAI에 남기고
Amplitude가 브랜드와 고객을 가져온다고 밝힌다.[^amplitude-blog]
Optimizely의 CEO는 이를 코드는 받고
사람은 못 받은 경주용 자동차라고 비유했다고 한다.
이는 경쟁사 CEO의 말이고,
그 전달도 MarTech 기사를 옮긴 ORM News 글을 거쳤다.[^orm]
Amplitude 쪽 서술은 다르다.
원래 팀이 코드베이스와 운영을 설명해 주었고
Amplitude 소속 약 50명이 유지한다는 것이다.[^phase1]
어느 쪽이 맞는지 이 문서는 판단할 자료가 없다.
다만 두 서술이 다르다는 점,
그리고 홈페이지가 그 차이를 다루지 않는다는 점은 분명하다.

후기도 시점이 다르다.
OpenAI 엔지니어링 관리자의 후기는 OpenAI를 고객으로 둔 시기의 말일 수 있다.
고객 후기에 날짜가 없어서
지금 읽는 사람은 어느 소유 구조 아래의 말인지 알 수 없다.

## 인사이트

### 실험 플랫폼의 통합은 “데이터 중력”이 만드는 필연적 수렴이다

Statsig가 8개 기능을 한 곳에 모은 것은 마케팅 선택처럼 보이지만,
더 깊은 차원에서는 데이터 중력(data gravity)의 결과다.
실험, 피처 플래그, 분석은 모두 같은 이벤트 스트림을 소비한다.
사용자가 무엇을 보고 무엇을 클릭했는가라는 동일한 데이터를,
서로 다른 도구가 각자 수집하면 정의가 어긋나고 중복이 쌓인다.
한 번 수집한 데이터를 여러 용도로 재사용하려는 압력이
자연스럽게 통합 플랫폼을 끌어당긴다.

이것이 가져올 2차 효과는 시장의 재편이다.
단독 카테고리 강자들도 인접 기능으로 확장할 수밖에 없다.
LaunchDarkly가 플래그에서 실험으로 넓어진 흐름과,
제품 분석 회사인 Amplitude가 2026년 5월
Statsig의 브랜드와 고객과 플랫폼을 가져간 일은
경쟁 대응이 아니라 데이터 중력에 대한 같은 반응이다.[^ld-exp][^amplitude-blog]
결국 이 시장은 여러 단독 제품의 공존이 아니라,
같은 데이터를 두고 통합 플랫폼들이 부딪히는 구도로 수렴한다.
Statsig의 포지셔닝은 그 수렴을 먼저 선언한 것이다.

### “실험 속도”라는 지표는 측정 가능성이 만든 대리 목표다

홈페이지가 자랑하는 “9배”, “30배”의 공통 단위는 실험 건수다.
왜 하필 건수인가?
제품 성과의 진짜 지표는 매출, 리텐션, 사용자 만족이지만,
이것들은 실험 도구 하나의 기여로 분리해 측정하기 어렵다.
반면 실험 건수는 깔끔하게 셀 수 있다.
측정 가능한 것이 목표가 되는 전형적인 굿하트의 법칙(Goodhart's law) 패턴이다.

이 대리 목표는 위험한 인센티브를 만든다.
“실험 속도”가 성공 지표가 되면, 조직은 실험을 많이 돌리는 것 자체를 추구한다.
질 낮은 실험, 통계적으로 무의미한 결과, 잘못 설계된 가설이 양산된다.
도구가 마찰을 없앨수록 나쁜 실험의 비용도 낮아지기 때문이다.
Statsig가 파는 “속도”는 좋은 실험 문화가 이미 있는 조직에서는 가속이지만,
실험 규율이 없는 조직에서는 쓰레기를 더 빨리 만드는 장치가 된다.
홈페이지는 도구가 문화를 대체할 수 없다는 이 한계를 말하지 않는다.

### 피처 플래그를 “공짜 입구”로 두는 전략은 메트칼프의 법칙을 노린다

Statsig의 “가장 관대한 무료 티어”는 단순한 가격 정책이 아니라
플랫폼 채택을 위한 침투 전략이다.
피처 플래그는 도입 장벽이 가장 낮은 기능이다.
개발자가 부담 없이 플래그 하나를 넣는 순간,
그 노출 데이터가 플랫폼으로 흘러들고,
한 번 데이터가 들어오면 실험과 분석으로 확장하는 것은 추가 설정만 남는다.

이 전략의 본질은 네트워크 효과를 조직 내부에 만드는 것이다.
한 팀이 플래그를 쓰기 시작하면, 그 데이터를 공유하는 인접 팀도 같은 플랫폼을
쓰는 것이 유리해진다.
실험 정의, 메트릭, 세그먼트가 한 곳에 모일수록 플랫폼의 가치가 제곱으로 커진다.
무료 티어로 입구를 넓게 열어두는 것은,
조직 안에서 임계 질량(critical mass)을 넘기면 잠금이 자동으로 완성되기 때문이다.
즉 Statsig의 가격 정책은 관대함이 아니라,
초기 마찰을 없애 데이터 중력과 네트워크
효과를 동시에 작동시키려는 정교한 설계다.

### 제품과 팀이 갈라지면 남는 것은 계약과 이식성이다

이번 사례는 소프트웨어 공급자의 인수에서 흔치 않은 모양이다.
브랜드와 고객과 코드는 한 회사로, 코드를 만든 사람들은 다른 회사로 갔다.
고객이 계약한 것은 제품이지만
고객이 의지해 온 것은 그 제품을 계속 고치던 팀이었다.
Amplitude가 6월 글에서 인계에 여섯 주를 쓰고
원래 팀에게서 문서를 받았다고 적은 것은
이 간극을 인정한 것으로 읽을 수 있다.[^phase1]

그러므로 도입 판단은 기능 비교에서 한 걸음 더 나아가야 한다.
누가 이 제품의 로드맵을 쥐는가,
공급자가 바뀌면 가격과 데이터 구조가 바뀔 수 있는가,
빠져나올 때 무엇을 가지고 나갈 수 있는가를 묻는 일이다.
이 문서는
ORM News 글이 짚은 가격과 로드맵의 불확실성을 사실로 확인하지는 않았지만,
그 질문들은 이번 사례가 아니어도 공급자 의존의 일반 점검 항목이다.[^orm]

이 점에서 앞서 본 잠금 논의가 구체적인 질문으로 바뀐다.
웨어하우스 네이티브 배포는 이벤트 데이터가 고객의 웨어하우스에 남는다는 점에서
이식성을 높인다.
오픈소스를 내세우는 SDK도 클라이언트 쪽의 이탈 비용을 낮춘다.
그러나 실험 정의와 메트릭과 세그먼트가 플랫폼에 있다면 그것은 가져갈 수 없다.
가져갈 수 있는 형식으로 내보내는 경로가 있는지를 도입 전에 시험해 보는 것이
소유 구조가 두 번 바뀐 제품을 쓰는 가장 현실적인 보험이다.
이는 이 문서의 제안이다.

---

[^openai-blog]: Statsig, [Statsig is joining OpenAI](https://www.statsig.com/blog/openai-acquisition), 2025-09-02

[^amplitude-blog]: Amplitude, [Amplitude and Statsig partnership](https://amplitude.com/blog/amplitude-and-statsig-partnership), 2026-05-05

[^phase1]: Statsig, [Statsig + Amplitude: The drop on Phase 1](https://www.statsig.com/blog/statsig-amplitude-phase-1), 2026-06-17

[^blog-index]: Statsig, [Statsig Blog | The authoritative source for data-driven insights](https://www.statsig.com/blog)

[^orm]: ORM News, [Amplitude Partners with Statsig, Raising Customer Concerns](https://orm-tech.com/news/20260508-amplitude-acquires-statsig-assets-in-2026-partnership/), 2026-05-08

[^pricing]: Statsig, [Statsig | The modern product development platform](https://www.statsig.com/pricing)

[^notion]: Statsig, [Statsig customer story - Notion went from single-digit to hundreds of experiments per quarter](https://www.statsig.com/customers/notion)

[^ancestry]: Statsig, [Statsig customer story - Ancestry goes from 70 to 600 annual experiments](https://www.statsig.com/customers/ancestry)

[^brex]: Statsig, [Statsig customer story - How Brex’s data teams achieved a +50% time efficiency gain](https://www.statsig.com/customers/brex)

[^lime]: Statsig, [Statsig customer story - Lime decreased refunds by 20% and started measuring the impact of every rollout](https://www.statsig.com/customers/lime)

[^vijayer]: <https://news.ycombinator.com/item?id=26629439>

[^dantihanyi]: <https://news.ycombinator.com/item?id=48029407>

[^ev]: Statsig Docs, [How Evaluation Works](https://docs.statsig.com/sdks/how-evaluation-works)

[^cvs]: Statsig Docs, [Client vs Server SDKs](https://docs.statsig.com/sdks/client-vs-server)

[^init]: Statsig Docs, [Initialization](https://docs.statsig.com/client/concepts/initialize)

[^create]: Statsig Docs, [Create a Feature Gate](https://docs.statsig.com/feature-flags/create)

[^cond]: Statsig Docs, [Conditions](https://docs.statsig.com/feature-flags/conditions)

[^overrides]: Statsig Docs, [Overrides](https://docs.statsig.com/feature-flags/overrides)

[^testgate]: Statsig Docs, [Test Gate](https://docs.statsig.com/feature-flags/test-gate)

[^exposures]: Statsig Docs, [View Exposures](https://docs.statsig.com/feature-flags/view-exposures)

[^sched]: Statsig Docs, [Scheduled Rollouts](https://docs.statsig.com/feature-flags/scheduled-rollouts)

[^lifecycle]: Statsig Docs, [Feature Flags Lifecycle](https://docs.statsig.com/feature-flags/feature-flags-lifecycle)

[^stale]: Statsig Docs, [Permanent and Stale Gates](https://docs.statsig.com/feature-flags/permanent-and-stale-gates)

[^bestp]: Statsig Docs, [Best Practices](https://docs.statsig.com/feature-flags/best-practices)

[^gatevsexp]: Statsig Docs, [Feature Flags or Experiments](https://docs.statsig.com/guides/featureflags-or-experiments)

[^envs]: Statsig Docs, [Using Environments](https://docs.statsig.com/guides/using-environments)

[^testing]: Statsig Docs, [Testing](https://docs.statsig.com/guides/testing)

[^tutorial]: Statsig Docs, [Check a Gate](https://docs.statsig.com/guides/check-gate)

[^dynconfig]: Statsig Docs, [Dynamic Config](https://docs.statsig.com/dynamic-config/overview)

[^layers]: Statsig Docs, [Layers](https://docs.statsig.com/experiments/layers-overview)

[^holdouts]: Statsig Docs, [Holdouts](https://docs.statsig.com/experiments/holdouts-introduction)

[^paramstores]: Statsig Docs, [Parameter Stores](https://docs.statsig.com/client/concepts/parameter-stores)

[^servercore]: Statsig Docs, [Server Core](https://docs.statsig.com/server-core)

[^nodecore]: Statsig Docs, [Node Core](https://docs.statsig.com/server-core/node-core)

[^react]: Statsig Docs, [React](https://docs.statsig.com/client/React)

[^jssdk]: Statsig Docs, [JavaScript SDK](https://docs.statsig.com/client/javascript-sdk)

[^faq]: Statsig Docs, [FAQ](https://docs.statsig.com/faq)

[^safeguards]: Statsig Docs, [Safeguards](https://docs.statsig.com/feature-flags/safeguards-overview)

[^relpipe]: Statsig Docs, [Release Pipelines](https://docs.statsig.com/release-pipeline/overview)

[^consoleapi]: Statsig Docs, [Console API](https://docs.statsig.com/console-api/introduction)

[^cli]: Statsig Docs, [Statsig CLI](https://docs.statsig.com/statsigcli/introduction)

[^whn]: Statsig Docs, [Warehouse Native](https://docs.statsig.com/statsig-warehouse-native/introduction)

[^sessionreplay]: Statsig Docs, [Session Replay](https://docs.statsig.com/session-replay/overview)

[^prodanalytics]: Statsig Docs, [Product Analytics](https://docs.statsig.com/product-analytics/overview)

[^webanalytics]: Statsig Docs, [Web Analytics](https://docs.statsig.com/webanalytics/overview)

[^autotune]: Statsig Docs, [Autotune](https://docs.statsig.com/autotune/overview)

[^migrate-ld]: Statsig Docs, [Migrate from LaunchDarkly](https://docs.statsig.com/guides/migrate-from-launchdarkly)

[^evaluator]: GitHub, [statsig-io/node-js-server-sdk](https://github.com/statsig-io/node-js-server-sdk/blob/main/src/Evaluator.ts)

[^ld-exp]: LaunchDarkly Docs, [Experimentation](https://launchdarkly.com/docs/home/experimentation)

[^npm-react]: npm, [@statsig/react-bindings](https://www.npmjs.com/package/@statsig/react-bindings)

[^npm-nodecore]: npm, [@statsig/statsig-node-core](https://www.npmjs.com/package/@statsig/statsig-node-core)

[^pypi-pycore]: PyPI, [statsig-python-core](https://pypi.org/project/statsig-python-core/)
