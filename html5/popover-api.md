# Popover API

<https://developer.mozilla.org/en-US/docs/Web/API/Popover_API>

[Getting Started With The Popover API](https://www.smashingmagazine.com/2026/03/getting-started-popover-api/)
— Godstime Aburu, Smashing Magazine, 2026-03-02

## 요약

브라우저 네이티브 Popover API를 사용해 툴팁을 다시 구현한 실전 마이그레이션 사례.
기존에는 라이브러리에 의존해 ~60줄의 JavaScript와 5개의 이벤트 리스너,
수동 ARIA 상태 관리가 필요했지만,
Popover API로 전환하면 약 10줄의 선언적 HTML만으로 동일한 결과를 얻을 수 있다.

핵심 구현:

```html
<button popovertarget="tip-1">?</button>

<div id="tip-1" popover="manual" role="tooltip">
  This button triggers a helpful tip.
</div>
```

JavaScript 이벤트 리스너 없이 열기/닫기가 동작하고,
`Esc` 키 처리와 `aria-expanded` 동기화가 브라우저 수준에서 자동으로 이뤄진다.

## 핵심 개념

### Invoker Commands

| 속성                      | 역할                                   |
| ------------------------- | -------------------------------------- |
| `popovertarget="id"`     | 버튼과 팝오버 요소를 연결              |
| `popovertargetaction`    | 동작 지정: `show`, `hide`, `toggle`   |

`toggle`이 기본값이며, 하나의 팝오버에 여러 트리거를 연결할 수 있다.

### popover 속성값

| 값         | 동작                                         |
| ---------- | -------------------------------------------- |
| `auto`    | light dismiss(바깥 클릭/Esc로 자동 닫힘)    |
| `manual`  | 명시적으로만 열고 닫음                        |

### 접근성 자동 처리

1. **키보드**: `Tab`/`Shift+Tab` 정상 동작, `Esc`로 닫기 보장
2. **스크린 리더**: `role="tooltip"`과 자동 `aria-expanded` 동기화
3. **포커스 관리**: 팝오버 닫힘 시 트리거로 포커스 자동 복귀(`auto` 모드)

## 아직 부족한 부분

1. **타이밍 제어**: 즉시 열림/닫힘만 지원. 호버 지연(hover delay)은 여전히 JS 필요
2. **호버 인텐트(hover intent)**: 의도적 호버와 스쳐 지나감을 구분 못 함
3. **`manual` 모드의 포커스 복귀**: `auto`와 달리 수동으로 `trigger.focus()` 호출 필요
4. **CSS Anchor Positioning**: 아직 초기 단계, 크로스 브라우저 지원 미완성

```javascript
// 타이밍 제어는 여전히 JS가 필요한 영역
let hideTimeout;

const show = () => {
  clearTimeout(hideTimeout);
  tooltip.showPopover();
};

const hide = () => {
  hideTimeout = setTimeout(() => {
    tooltip.hidePopover();
  }, 200);
};
```

## 라이브러리가 여전히 필요한 경우

- **대규모 디자인 시스템**: 조직 전체의 일관성과 가드레일 필요
- **복잡한 포지셔닝**: 중첩 스크롤 컨테이너, 커스텀 플립 로직 → Floating UI
- **접근성 경험이 부족한 팀**: 라이브러리가 안전망 역할

## 분석

### 플랫폼 시프트의 전형적 패턴

이 글은 웹 플랫폼이 반복적으로 보여주는 동일한 진화 패턴을 다시 한번 보여준다.
커뮤니티가 라이브러리로 문제를 해결하고,
그 패턴이 성숙하면 브라우저가 네이티브로 흡수하는 순환이다.
jQuery → `querySelector`, Modernizr → `@supports`,
AJAX 라이브러리 → `fetch`, 그리고 이제 툴팁 라이브러리 → Popover API.

이 패턴을 인식하는 것 자체가 중요하다.
"지금 라이브러리로 해결하는 문제 중 3년 후 브라우저가 흡수할 것은 무엇인가?"라는
질문을 항상 던져야 한다.

### 선언적 HTML의 승리

Popover API의 진짜 가치는 코드량 감소가 아니라 **책임의 이동**이다.
`popovertarget` 속성 하나로 트리거와 팝오버의 관계가 마크업에 명시되면,
브라우저는 그 관계를 포커스 모델, 접근성 트리, 닫기 규칙에 반영한다.
JavaScript가 "이것은 툴팁이다"라고 시뮬레이션하는 것과
브라우저가 "이것은 툴팁이다"라고 이해하는 것 사이의 차이는 질적으로 다르다.

### `<dialog>`와의 비교

같은 저장소에 정리해둔 `<dialog>`와 놀랍도록 유사한 궤적을 밟고 있다.
모달도 과거에는 라이브러리 없이 제대로 구현하기 어려웠지만,
`<dialog>` 요소가 등장하면서 `showModal()`, `::backdrop`, `Esc` 닫기,
포커스 트랩이 네이티브로 해결됐다.
Popover API는 **비모달(non-modal) 오버레이**에 대해 같은 일을 하고 있다.

| 비교 항목            | `<dialog>`            | Popover API                  |
| -------------------- | --------------------- | ---------------------------- |
| 용도                 | 모달/비모달 대화상자  | 툴팁, 팝오버, 알림           |
| 포커스 트랩          | 자동(모달 시)         | 없음(필요 시 수동)           |
| light dismiss        | 없음(수동 구현)       | `auto` 모드에서 기본 제공    |
| Top Layer 사용       | 예                    | 예                           |
| `Esc` 닫기          | 예                    | 예                           |

둘 다 Top Layer를 사용한다는 점이 핵심이다.
`z-index` 전쟁에서 벗어나 브라우저가 관리하는 최상위 레이어에 렌더링된다.

## 비평

### 글의 강점

글쓴이가 실제 마이그레이션 경험을 바탕으로 쓴 점이 설득력 있다.
"라이브러리가 나쁘다"는 이분법이 아니라,
"언제 네이티브를 쓰고 언제 라이브러리를 쓸지"라는 판단 기준을 제시한다.
특히 접근성 개선을 수치(Lighthouse 점수)와 구체적 행동(스크린 리더, 키보드)으로
보여주는 부분이 강하다.

### 글의 약점

**포지셔닝 문제를 너무 가볍게 다뤘다.**
실전에서 툴팁의 가장 큰 고통은 열기/닫기가 아니라 **어디에 표시할 것인가**다.
CSS Anchor Positioning을 언급은 하지만 깊이가 부족하다.
Popover API만으로는 "뷰포트 가장자리에서 방향 전환"이라는 핵심 문제를 해결하지 못한다.
이 부분이 빠져 있어서, 글만 읽으면 Popover API가 툴팁의 모든 문제를 해결한 것처럼
오해할 수 있다.

**`popover="hint"`를 빠뜨렸다.**
글에서 참고 자료로 Una Kravets의 "What is popover=hint?"를 링크하면서도
본문에서 `hint` 타입을 설명하지 않았다.
`hint`는 기존 `auto`/`manual` 이분법을 넘어
"호버 시 잠깐 보여주는 비대화형 힌트"라는 정확한 시맨틱을 부여하는 값으로,
툴팁 맥락에서 가장 관련성 높은 추가 스펙이다.

**성능 비교가 없다.**
라이브러리 대비 네이티브 API의 번들 사이즈 절감, 렌더링 성능 차이 등
정량적 비교가 전혀 없다. "코드가 줄었다"는 정성적 주장만으로는
마이그레이션의 비용 대비 효과를 판단하기 어렵다.

## 인사이트

### 1. "브라우저가 이해하는" 것과 "JavaScript가 시뮬레이션하는" 것의 근본적 차이

이 글에서 가장 날카로운 통찰은 이것이다:

> "The tooltip is no longer simply a box positioned near a button anymore,
> but participating in the browser's focus model, the accessibility tree,
> and native dismissal rules."

JavaScript로 `aria-expanded`를 수동 토글하면 접근성 트리에 반영은 되지만,
브라우저의 포커스 모델이나 닫기 규칙과는 무관하다.
Popover API를 쓰면 이 세 가지가 하나의 동작으로 연결된다.
이것은 단순한 편의가 아니라 **정합성(coherence)의 문제**다.

### 2. 의존성 결정의 새로운 기준선

"라이브러리를 쓸까 말까"의 기준이 바뀌었다.
과거에는 네이티브로 불가능하니 라이브러리가 기본값이었다.
이제는 **네이티브가 기본값이고, 라이브러리는 정당화가 필요하다.**
이 기준선의 이동은 툴팁뿐 아니라
모든 UI 프리미티브 선택에 적용되는 사고 전환이다.

### 3. CSS Anchor Positioning이 진짜 게임 체인저

글에서 살짝 언급하고 넘어간 CSS Anchor Positioning이야말로
Popover API의 마지막 퍼즐 조각이다.
`anchor-name`과 `position-area`로 팝오버의 위치를 CSS만으로 제어할 수 있으면,
Floating UI 같은 포지셔닝 라이브러리의 존재 이유가 사라진다.
2026년 현재 Interop에 포함되어 있으므로 크로스 브라우저 지원은 시간문제다.

```css
.trigger {
  anchor-name: --my-trigger;
}

[popover] {
  position-anchor: --my-trigger;
  position-area: top;
  position-try-fallbacks: bottom, right, left;
}
```

Popover API + CSS Anchor Positioning이 결합되면,
**선언적 HTML + 선언적 CSS만으로 완전한 툴팁**이 가능해진다.
이것이 이 글이 가리키는 최종 목적지다.

### 4. Top Layer의 의미를 과소평가하지 말 것

`<dialog>`와 Popover API가 공유하는 Top Layer는
`z-index` 스택 컨텍스트 밖에 존재한다.
이것은 "z-index: 99999" 같은 해킹이 필요 없다는 것 이상의 의미를 갖는다.
오버플로우 히든 컨테이너 안에서도 잘리지 않고,
트랜스폼이 적용된 부모 요소의 영향도 받지 않는다.
포지셔닝 라이브러리가 해결하려던 가장 고통스러운 문제의 상당 부분이
Top Layer 하나로 사라진다.

### 5. 점진적 마이그레이션 전략의 교훈

글쓴이가 제안한 "하나의 툴팁만 먼저 바꿔보라"는 조언은
모든 플랫폼 마이그레이션에 적용되는 황금률이다.
전체 시스템을 한꺼번에 바꾸려 하면 리스크가 커지고,
그 리스크 때문에 마이그레이션 자체를 시작하지 못한다.
하나만 바꾸면 무엇이 사라지는지(이벤트 리스너, ARIA 동기화 코드)를
직접 체감할 수 있고, 그 체감이 나머지를 바꾸는 동력이 된다.

### 6. "코드가 줄었다"가 아니라 "걱정이 줄었다"

> "fewer things you have to worry about at all"

네이티브 API 채택의 가치를 LOC(Lines of Code)로 측정하면 핵심을 놓친다.
진짜 가치는 **인지 부하(cognitive load)의 감소**다.
`Esc` 키가 동작할지, ARIA 상태가 동기화될지,
포커스가 올바른 곳으로 돌아올지를 더 이상 걱정하지 않아도 된다.
이것은 개발자 경험의 개선이 아니라 **사용자 경험의 보장**이다.
개발자가 잊어버려도 브라우저가 처리하기 때문이다.

## 참고 자료

- [MDN: Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)
- [Open UI Popover API Explainer](https://open-ui.org/components/popover.research.explainer/)
- [Poppin' In — Geoff Graham](https://frontendmasters.com/blog/poppin-in/)
- [What is popover=hint? — Una Kravets](https://developer.chrome.com/blog/popover-hint)
- [CSS Anchor Positioning — Juan Diego Rodríguez](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning)
- [Can I use: Popover API](https://caniuse.com/mdn-api_htmlelement_popover)
