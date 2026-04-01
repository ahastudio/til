# Pretext — DOM 없이 텍스트 높이를 측정하는 순수 JS 레이아웃 라이브러리

> 원문: <https://github.com/chenglou/pretext>

## 요약

브라우저에서 텍스트 높이 측정 시 발생하는 레이아웃 리플로우(layout reflow)를
완전히 회피하는 JavaScript/TypeScript 라이브러리다. Canvas의 `measureText()`
API로 글자 너비를 직접 측정한 뒤, 캐싱된 너비값으로 순수 산술 연산만 수행하여
DOM 접근 없이 텍스트 레이아웃을 계산한다.

React/Relay 창시자인 chenglou의 프로젝트이며, GitHub 7.1k 스타를 기록했다.

## 해결하는 문제

`getBoundingClientRect()`나 `offsetHeight`로 텍스트 높이를 측정하면 브라우저가
레이아웃을 재계산하도록 강제된다. 이 "강제 리플로우"는 렌더링 파이프라인에서
가장 비싼 연산 중 하나이며, 특히 가상화된 리스트나 에디터처럼 수백 개의 텍스트
블록을 다루는 경우 심각한 성능 병목이 된다.

## 동작 원리

```text
prepare('text', '16px Inter')  →  글자별 너비 측정 + 캐싱
                                   (~19ms / 500텍스트)

layout(prepared, width, lineHeight)  →  순수 산술로 높이·줄 수 반환
                                        (~0.09ms / 500텍스트)
```

핵심은 **측정(prepare)과 계산(layout)의 분리**다. 측정은 Canvas API를 한 번만
호출하고, 이후의 모든 레이아웃 계산은 캐싱된 값에 대한 사칙연산이다.

## API

### 기본 사용

```javascript
import { prepare, layout } from 'pretext';

const prepared = prepare('Hello, world!', '16px Inter');
const { height, lineCount } = layout(prepared, 300, 24);
```

### 줄 단위 제어

- `layoutWithLines()` — 개별 줄 정보 접근
- `walkLineRanges()` — 텍스트 문자열 없이 줄 범위만 순회
- `layoutNextLine()` — 가변 너비 줄 처리

### 설정

`{ whiteSpace: 'pre-wrap' }` 옵션으로 공백, 탭, 하드 브레이크를 보존한다.
textarea 스타일의 텍스트 처리에 사용한다.

## 분석

Pretext의 설계 철학은 **DOM과 레이아웃 엔진의 결합을 끊는 것**이다. 브라우저의
텍스트 렌더링 파이프라인은 "측정 → 레이아웃 → 페인트"가 강하게 결합되어 있다.
Pretext는 측정 단계만 Canvas API로 추출하고, 레이아웃 단계를 순수 함수로
재구현한다. 이 분리가 가능한 이유는 텍스트 레이아웃의 핵심 로직이 결국
"글자 너비의 누적합이 컨테이너 너비를 초과하면 줄바꿈"이라는 단순한 산술이기
때문이다.

성능 수치가 인상적이다. prepare가 19ms, layout이 0.09ms라는 것은 **한 번
측정하면 이후 200배 이상 빠른 계산**이 가능하다는 뜻이다. 가상화된 리스트에서
스크롤할 때마다 수백 개 아이템의 높이를 재계산해야 하는 경우, 이 차이는
프레임 드롭 여부를 결정한다.

## 비평

### Canvas measureText의 신뢰 경계

GeekNews 댓글에서 지적된 것처럼, Canvas `measureText()`와 실제 DOM 렌더링이
완벽히 일치하려면 폰트 명세, line-height, word-break 규칙 등이 정확히 동기화
되어야 한다. Pretext가 `white-space: normal`, `word-break: normal`,
`overflow-wrap: break-word`, `line-break: auto`로 지원 범위를 한정한 것은
이 불일치 위험을 관리하기 위한 의도적 설계다.

그러나 실제 프로덕션 환경에서는 CSS 속성의 조합이 훨씬 다양하다.
`letter-spacing`, `word-spacing`, `text-transform`, `font-feature-settings`
등이 글자 너비에 영향을 미친다. Pretext가 이 모든 변수를 정확히 반영하지
못한다면, "거의 맞지만 가끔 틀리는" 측정 결과가 나올 수 있다. 이 "가끔"이
레이아웃 깨짐으로 이어지면 사용자 경험에 직접적으로 영향을 준다.

### 적용 범위의 현실

Pretext가 가장 빛나는 곳은 텍스트 에디터, 가상 스크롤 리스트, 터미널
에뮬레이터처럼 대량의 텍스트 블록을 다루는 특화된 UI 컴포넌트다. 일반적인
웹 애플리케이션에서 텍스트 높이를 몇 번 측정하는 정도라면 DOM 리플로우의
비용은 무시할 수 있는 수준이다.

도구의 가치는 문제의 크기에 비례한다. Pretext는 특정 문제를 극한까지
최적화하는 도구이지, 범용 솔루션이 아니다.

## 인사이트

### "브라우저의 일을 대신 한다"는 전략의 의미

Pretext의 접근법은 본질적으로 **브라우저 레이아웃 엔진의 일부를
JavaScript로 재구현**하는 것이다. 이것은 브라우저 API의 성능 특성에 만족하지
못할 때 개발자가 취하는 극단적 전략이다.

같은 패턴이 다른 영역에서도 반복된다. 가상 DOM은 실제 DOM 조작의 비효율을
JavaScript 레이어에서 해결했다. Web Workers는 메인 스레드의 블로킹 문제를
별도 스레드로 우회했다. `OffscreenCanvas`는 Canvas 렌더링을 메인 스레드에서
분리했다.

공통 패턴은 이렇다: **브라우저가 제공하는 추상화가 성능 요구사항을 충족하지
못하면, 개발자가 추상화의 일부를 뜯어내서 직접 제어한다.** Pretext는 이
패턴의 가장 최근 사례이며, 텍스트 레이아웃이라는 매우 기초적인 영역에서
이것이 필요하다는 사실이 브라우저 렌더링 파이프라인의 설계적 한계를 드러낸다.

### 측정과 계산의 분리가 주는 아키텍처 교훈

prepare/layout의 2단계 API 설계는 **부수 효과가 있는 연산과 순수 연산의
분리**라는 함수형 프로그래밍의 핵심 원칙을 실무적으로 구현한 사례다.

prepare는 Canvas API를 호출하므로 부수 효과가 있다. layout은 캐시된 데이터로
순수 계산만 수행한다. 이 분리 덕분에 layout은 반복 호출해도 비용이 거의
없고, 테스트하기 쉽고, 병렬화가 가능하다.

같은 원칙이 더 넓은 시스템 설계에 적용된다. 데이터 수집(IO-bound)과 데이터
처리(CPU-bound)를 분리하면, 각각을 독립적으로 최적화할 수 있다. Pretext는
"측정은 비싸지만 한 번이면 되고, 계산은 싸니까 무한히 반복해도 된다"는
비대칭을 아키텍처로 포착한 것이다.

### chenglou의 일관된 철학

React, Relay, ReasonML, 그리고 이제 Pretext. chenglou의 프로젝트를 관통하는
주제는 "복잡한 런타임 동작을 예측 가능한 정적 구조로 변환한다"는 것이다.
React는 명령형 DOM 조작을 선언적 트리로, ReasonML은 JavaScript의 동적
타이핑을 정적 타입으로, Pretext는 DOM 리플로우를 순수 산술로 변환한다.

이 일관성은 도구 자체보다 더 가치 있는 통찰이다. **런타임의 예측 불가능성을
컴파일 타임 또는 초기화 타임의 확정적 계산으로 옮기는 것**이 성능과 신뢰성을
동시에 개선하는 보편적 전략이라는 것. Pretext는 이 전략의 텍스트 레이아웃
버전이다.
