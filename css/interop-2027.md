# CSS의 다음 1년: Interop 2027에 바라는 기능 10가지와 지금 써 보는 법

원문: [The Future of CSS ✨ • Josh W. Comeau](https://www.joshwcomeau.com/css/interop-2027/)

HN 토론: <https://news.ycombinator.com/item?id=50175070> (563점, 235개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/vidyh0/future_css> (44점, 6개 댓글)

GN 토론: <https://news.hada.io/topic?id=35743>

## 요약

Josh W. Comeau가 2026년 10월 20일에 올린 글이다.
Google, Apple, Microsoft, Mozilla에 Igalia와 Bocoup이 더해져
브라우저 지원을 맞추려고 해 온 프로젝트 Interop의 2027년 후보 가운데,
자신이 투표한 상위 10개 기능을 소개한다.
Mozilla 팀이 후보에 순위를 매기는 투표 시스템을 열어 두었고,
그 결과가 내년 Interop에 무엇을 넣을지 정하는 데 쓰인다고 한다.

저자가 Interop를 성공작으로 보는 근거는 서브그리드(subgrid)다.
서브그리드는 2019년에 Firefox가 구현했지만 다른 브라우저는 몇 년 동안 움직이지 않았다.
2023년에 Interop에 들어간 뒤 그해가 가기 전에 모든 최신 브라우저에서 쓸 수 있게 되었다.
저자는 Interop의 주제로 들어간 기능이 대개 1년 안에 모든 주요 브라우저에서 거의 100% 지원에 이른다고 말한다.

10개 기능은 다음과 같다.
글을 쓴 2026년 10월 기준으로, 5번을 제외한 모든 기능이 Chrome 155와 Edge 154에서만 지원되고
Firefox 157과 Safari 27에서는 지원되지 않는다.
5번 `inherit()` 함수는 어떤 브라우저에도 구현되지 않았고 caniuse에도 없다.

| 순번 | 기능                              | 하는 일                                                                    |
| ---- | --------------------------------- | -------------------------------------------------------------------------- |
| 1    | CSS 함수 `@function`              | CSS 안에서 값을 돌려주는 함수를 정의하고 호출한다                          |
| 2    | `corner-shape`                    | 모서리를 `squircle`, `bevel`, `notch`, `scoop`으로 바꾼다                  |
| 3    | `border-shape`                    | 직선, 호, 베지어 곡선으로 테두리 모양을 직접 그린다                        |
| 4    | 앵커드 컨테이너 쿼리              | 앵커 위치 지정 요소가 대체 위치로 뒤집혔는지 CSS에서 확인한다              |
| 5    | `inherit()` 함수                  | 상속받은 값을 `calc()`로 가공한다                                          |
| 6    | 스크롤 트리거 애니메이션          | 스크롤이 특정 지점에 닿으면 키프레임 애니메이션을 재생한다                 |
| 7    | `reading-flow`, `reading-order`   | 탭 이동 순서를 화면에 보이는 순서에 맞춘다                                 |
| 8    | `interpolate-size`, `calc-size()` | `auto` 같은 키워드 값 사이를 애니메이션한다                                |
| 9    | 갭 장식(gap decorations)          | 그리드 칸 사이에 `rule` 속성으로 선을 긋는다                               |
| 10   | 스크롤 상태 컨테이너 쿼리         | `position: sticky`가 붙었는지, 스크롤할 수 있는지를 컨테이너 쿼리로 묻는다 |

앵커 위치 지정(Anchor Positioning)은 Interop 2026에서 우선 과제였고 지금은 널리 쓸 수 있다.
스크롤 기반 애니메이션(scroll-driven animations)도 Interop 2026에 들어가 모든 브라우저에 구현되었다.
글의 결론에서 저자는 LLM에게 일을 맡기는 시대일수록 최신 CSS 기능을 알아야 한다고 주장한다.

## 동작 방식

### 새 값을 만드는 기능과 상태를 묻는 기능

10개를 두 부류로 나누면 쓰임새가 정리된다.
하나는 새 값을 만드는 기능이다.
`@function`, `inherit()`, `calc-size()`, `corner-shape`, `border-shape`가 여기에 든다.
다른 하나는 요소의 상태를 CSS가 알게 하는 기능이다.
앵커드 컨테이너 쿼리, 스크롤 상태 컨테이너 쿼리, 스크롤 트리거 애니메이션, `reading-flow`가 여기에 든다.

상태를 묻는 기능은 지금까지 JavaScript가 맡아 온 일을 CSS로 옮긴다.
스크롤 트리거 애니메이션은 지금도 `IntersectionObserver`로 구현할 수 있지만 번거롭다는 것이 저자의 설명이다.
스티키 헤더가 붙었는지 알려면 이제까지 스크립트가 필요했는데,
`container-type: scroll-state`와 `@container scroll-state(stuck: top)`이 이를 대신한다.

### 모양을 바꾸는 기능은 박스 자체를 바꾼다

저자는 `clip-path`나 마스크로도 비슷한 모양을 낼 수 있다고 인정한다.
다만 `corner-shape`와 `border-shape`는 요소의 border-box 자체를 바꾼다고 설명한다.
그래서 테두리, 아웃라인, `box-shadow`가 바뀐 모양을 따라간다.

### 함수는 값을 반환한다

`@function`은 JavaScript의 함수와 비슷하게 정의하고, `result`로 값을 반환한다.
저자가 꼽은 용도는 극좌표를 직교좌표로 바꾸는 것이다.

```css
@function --translate-polar(--angle, --distance) {
  result: translate(
    calc(cos(var(--angle)) * var(--distance)),
    calc(sin(var(--angle)) * var(--distance))
  );
}

/* 이 요소를 45도 방향으로 100px 옮긴다. */
.particle {
  transform: --translate-polar(45deg, 100px);
}
```

HN에서는 CSS에 함수가 정말 필요한지를 두고 말이 갈렸다.
lioeters는 CSS가 이미 튜링 완전해졌으니 배는 떠났다고 하면서, 이런 곡예 대신 JavaScript와의 통합을 개선하면 되지 않느냐고 물었다.[^lioeters]
afavour는 JavaScript는 가상 머신과 스크립트 파싱이 필요해서, 콘텐츠를 보여 주기 전에 그것을 요구하는 것은 퇴보라고 답했다.[^afavour]
bradley13은 지금은 JavaScript를 꺼서 웹 페이지가 계산하지 못하게 하면서 기본 콘텐츠만 볼 수 있지만, CSS에 명시적인 함수가 생기면 그 방법이 불가능해진다고 우려했다.[^bradley13]
longor1996은 이 함수가 명세와 문서를 보면 함수라기보다 템플릿이나 위생적 매크로에 가깝다고 이해한다고 적었다.[^longor1996]
함수가 계산 능력을 CSS에 더하는 것인지, 값 치환을 정리하는 것인지에 따라 우려의 크기가 달라진다.
Lobste.rs의 Pomax는 후자 쪽에 가깝다고 보았다.
이 함수는 TeX의 매크로처럼 더 확장할 것이 없을 때까지 펼쳐질 뿐 무언가를 실행하는 것이 아니며, 그래서 본문 자체가 결과인데도 `result` 키워드가 따로 필요한 점이 어색하다는 것이다.[^Pomax]

## 지금 적용하기

저자는 Interop 후보인 기능 대부분을 점진적 개선(progressive enhancement)으로 지금 써도 된다고 말한다.
미지원 브라우저에서 무시되어도 화면이 깨지지 않는 방식으로 쓰는 것이 조건이다.
아래 코드는 글에 실린 예시를 용도별로 모은 것이다.

### 모서리 모양

```css
.panel {
  /* 미지원 브라우저에서는 이 값만 적용되어 둥근 모서리로 남는다. */
  border-radius: 16px;
  corner-shape: bevel;
}
```

### 높이가 0에서 auto로 바뀌는 아코디언

```css
html {
  interpolate-size: allow-keywords;
}

/* 미지원 브라우저에서 전환이 걸리면 짧은 지연이 생기므로 @supports로 감싼다. */
@supports (interpolate-size: allow-keywords) {
  details {
    overflow: hidden;

    &::details-content {
      height: 0;
      transition:
        height 300ms,
        content-visibility 300ms;
      transition-behavior: allow-discrete;
    }

    &:open::details-content {
      height: auto;
    }
  }
}
```

### 스티키 헤더가 붙었을 때의 스타일

```css
header {
  position: sticky;
  top: 0;
  container-type: scroll-state;
}

@container scroll-state(stuck: top) {
  .header-content {
    background: var(--gray-300);
    border-bottom: 1px solid var(--gray-500);
  }
}
```

### 그리드 칸 사이의 선

지원되는 곳에서는 `rule` 속성 하나로 끝난다.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  border: 1px solid red;
  rule: 1px solid red;
}
```

저자가 오래 써 온 우회 방법은 그리드 배경색을 선 색으로 칠하고 `1px` 갭 사이로 비치게 하는 것이다.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  padding: 1px;
  background-color: red;
}

/* 빈 칸에도 요소를 넣고 배경을 흰색으로 덮어야 선이 보인다. */
.empty.child {
  background-color: white;
}
```

### 화면 순서와 탭 순서 맞추기

```css
.grid {
  display: grid;
  reading-flow: grid-rows;
}
```

`reading-order`는 `tabIndex`처럼 순서를 직접 정할 때 쓴다.
`reading-flow`는 Grid와 Flexbox에 쓸 수 있는 값이 따로 있다.

## 트레이드오프

### 점진적 개선은 브라우저마다 다른 화면을 받아들이는 일이다

`corner-shape: bevel`은 Chrome 사용자에게 사선 모서리를 주고 Firefox와 Safari 사용자에게는 둥근 모서리를 준다.
디자인이 어느 쪽으로 보아도 성립해야 점진적 개선이 된다.
저자는 게임이나 공상과학 풍의 화면에 `bevel`을 자주 쓴다고 하는데,
그런 화면에서 사선이 정체성의 일부라면 둥근 모서리는 의도와 다른 결과다.
기능이 장식인지 요구 사항인지에 따라 같은 코드가 점진적 개선이기도 하고 깨짐이기도 하다.

HN의 PennRobotics는 모서리 모양이 열 개 중 세 개를 차지한다는 점을 지적했다.
눈요깃거리가 모든 웹사이트와 프레임워크 템플릿에서 과하게 쓰여 어느 사이트도 서로 달라 보이지 않게 된다는 것이 이유다.[^PennRobotics]
모서리 모양을 지원 범위와 상관없이 쓸 수 있게 되는 순간이 오면, 쓸 수 있다는 사실과 써야 한다는 판단은 별개의 문제가 된다.

### 선을 긋는 기능은 폴백이 없으면 그냥 사라진다

`rule` 속성만 쓰고 폴백을 두지 않으면 미지원 브라우저에서는 칸 사이의 선이 없어진다.
이는 글의 설명에서 추론한 것이다.
`corner-shape`는 폴백인 `border-radius`가 자연스럽게 남지만, `rule`에는 그런 기본값이 없다.
그래서 선이 정보를 전달하는 표라면 우회 방법을 함께 두거나, 지원 범위가 넓어질 때까지 기다려야 한다.
우회 방법도 빈 DOM 노드를 추가해야 하고 페이지 배경이 단색이어야 하며,
그리드 바깥 테두리와 안쪽 선 사이에 간격을 두지 못하는 한계가 있다.

### 폴리필은 초안의 문법이 바뀌지 않는다는 가정에 기댄다

Lobste.rs의 bramh는 PostCSS 플러그인으로 이 기능들 일부를 폴리필하면, 초안의 문법이 바뀌지 않는 한 브라우저가 지원을 추가했을 때도 그대로 쓸 수 있다고 적었다.[^bramh]
단서가 그 조건 하나에 걸려 있다.
아직 제안 단계인 기능일수록 문법이 바뀔 가능성이 크므로, 폴리필로 쌓아 둔 코드는 바뀐 문법에 맞춰 다시 쓸 비용을 안고 있다.

### 접근성 기능은 지원 여부에 따라 사용자가 겪는 순서가 달라진다

`reading-flow`가 없는 브라우저는 DOM 순서대로 포커스를 옮긴다.
같은 페이지에서 키보드 사용자가 Chrome에서는 화면 순서로, 다른 브라우저에서는 DOM 순서로 이동하게 된다.
이 차이가 문제가 되지 않으려면 DOM 순서 자체가 어느 정도 말이 되도록 짜 두어야 한다.
`reading-flow`가 있다고 해서 DOM 순서를 방치해도 되는 것은 아니다.

## 함정

### 미지원 속성을 쓰는 곳마다 @supports를 두는 것은 아니다

`@supports`가 필요한 경우는 미지원 브라우저에서 부작용이 생기는 경우다.
글이 `interpolate-size`에서 `@supports`를 요구하는 이유는,
전환을 감싸지 않으면 미지원 브라우저에 짧은 지연이 생기기 때문이다.
반대로 `corner-shape`처럼 모르는 속성이 그냥 무시되는 경우에는 감쌀 필요가 없다.
무엇이 부작용을 만드는지 따져 보지 않고 모두 `@supports`로 감싸면 코드만 길어진다.

### Interop에 들어간다고 일정이 보장되는 것은 아니다

저자는 `inherit()` 함수를 두고 Interop 2027에 들어가면 놀랄 것이라고 쓴다.
제안이 아직 초기 단계라서다.
Chromium에만 구현된 기능은 Interop에 들어가면 지원이 빨라질 가능성이 크다는 것이 저자의 기대이지만,
기대일 뿐이며 어떤 기능이 선정될지는 투표 결과를 본 뒤에야 알 수 있다.

### 데모의 지원 현황은 글을 쓴 시점의 값이다

각 기능 아래에 붙은 브라우저 지원 표기는 2026년 10월 기준이다.
이 글을 읽는 시점에는 이미 바뀌었을 수 있으므로 caniuse로 다시 확인해야 한다.

## 확인하기

사용하려는 기능이 지금 브라우저에서 동작하는지 CSS 안에서 확인할 수 있다.

```css
/* 브라우저가 이 속성 값을 알 때만 안쪽 규칙이 적용된다. */
@supports (corner-shape: bevel) {
  .panel {
    corner-shape: bevel;
  }
}
```

미지원 브라우저의 화면은 직접 열어서 눈으로 확인해야 한다.
Chrome에서는 보이고 다른 브라우저에서는 어떻게 보이는지 나란히 비교하는 것이 가장 빠르다.

## 체크리스트

- 사용하려는 기능이 미지원 브라우저에서 속성만 무시되는가, 부작용이 생기는가?
- 부작용이 생기는 기능이라면 `@supports`로 감쌌는가?
- 미지원 브라우저의 화면이 디자인 의도를 벗어나지 않는가?
- 선이나 순서처럼 정보를 전달하는 기능은 폴백을 두었는가?
- `reading-flow`를 쓰더라도 DOM 순서가 최소한 말이 되도록 짰는가?
- 지원 현황을 caniuse로 최근에 다시 확인했는가?

## 비평

### 저자의 순위는 저자의 작업을 반영한다

10개 선정 이유는 대부분 저자가 직접 쓰는 장면에서 나온다.
극좌표 변환은 저자의 Whimsical Animations 강의에서 반복해 쓰는 개념이고,
`corner-shape: bevel`은 만들고 있는 사이드 프로젝트에 쓰며,
`reading-flow`는 진행 중인 비공개 프로젝트에서 필요하다고 한다.
글에는 저자의 CSS 강의를 소개하는 문장도 두 번 나온다.
이는 순위가 틀렸다는 뜻이 아니라, 이 목록이 웹 전체의 필요가 아니라 한 개발자의 작업을 기준으로 정렬되었다는 뜻이다.
독자의 프로젝트에서 더 급한 기능은 다를 수 있다.

HN의 fodkodrasz는 이 점을 거칠게 짚었다.
장갑을 낀 채 쓰는 산업 현장용 터치 화면을 만들 때 날짜 선택기, 시간 선택기, 숫자 증감 입력을 모두 커스텀 컴포넌트와 JavaScript로 만들어야 했는데, 표준 쪽은 모서리 장식 같은 눈요깃거리만 만든다는 것이다.[^fodkodrasz]
alberth도 제안들이 CSS를 불필요하게 복잡하게 만들거나 JavaScript에 가깝게 만든다고 보았다.[^alberth]
두 사람의 불만은 서로 다르지만, 이 목록이 새로 만들 수 있는 모양에 쏠려 있다는 점은 같다.

### 서브그리드 하나로 일반화하기에는 근거가 약하다

Interop에 들어간 기능이 대개 1년 안에 거의 100% 지원에 이른다는 주장은 서브그리드 사례 하나로 뒷받침된다.
서브그리드는 이미 Firefox에 구현되어 있었고 다른 브라우저의 구현이 따라붙는 데 Interop가 속도를 더한 경우로 보인다.
이 글의 대부분 기능은 Chromium에만 있는데, 다른 엔진이 구현하지 않은 기능이 같은 속도를 보일지는 이 사례만으로 알 수 없다.
저자도 Interop 2027에 들어가면 가능성이 높다고만 쓴다.

HN에서 herpdyderp는 글이 브라우저들의 협력을 내세우며 시작하는데 소개된 기능이 모두 Chrome에서만 된다는 점을 이상하게 여겼다.[^herpdyderp]
paulhebert는 이 글이 Interop라는 프로그램, 즉 브라우저들이 특정 표준을 모든 브라우저에 가져오려고 협력하는 과정에 관한 것이고 투표로 선정에 참여할 수 있다고 설명했다.[^paulhebert]
두 댓글은 글이 Interop의 현재 결과가 아니라 앞으로 들어갈 후보를 소개하는 글이라는 점을 구분해 준다.

### 에이전트가 최신 CSS를 못 쓴다는 전제는 시험하지 않았다

글의 결론은 LLM이 쓰는 학습 데이터가 오래되었으므로 최신 기능을 에이전트에게 쓰라고 시키려면 사람이 알아야 한다는 것이다.
그럴듯하지만 이 글은 이를 확인하지 않았다.
에이전트에 명세나 문서를 읽게 하면 같은 결과가 나올 수도 있고,
반대로 문서가 있어도 오래된 패턴을 쓰는지는 측정해 봐야 안다.
이 주장이 맞는지는 모델에게 같은 과제를 최신 기능을 알려 주었을 때와 알려 주지 않았을 때로 나눠 맡겨 보면 가려진다.

HN의 piro0919는 코드를 읽지 않고 Claude Code로 웹 앱을 만들었다고 적었다.
메뉴와 헤더에 바깥 여백을 주고 투명한 흐림 배경을 넣어 달라고 했더니 상상한 대로 나왔다는 것이다.[^piro0919]
louiskottmann은 그 결과도 Claude가 CSS를 써 준 것이므로 CSS라는 언어가 살아남아야 한다는 뜻이라며 반박했다.[^louiskottmann]
이 일화는 에이전트가 흔한 요청에 쓸 만한 CSS를 내놓는다는 것만 보여 준다.
새 기능을 쓰는지는 보여 주지 못한다.

## 기억할 원칙

### 기능이 장식인지 요구 사항인지에 따라 폴백의 무게가 다르다

모서리 모양처럼 없어도 기능이 같은 것은 점진적 개선으로 바로 써도 된다.
탭 순서나 칸 사이의 선처럼 정보와 접근성을 담는 것은 폴백이 없으면 일부 사용자가 잃는다.
새 CSS 기능을 쓰기 전에 지원하지 않는 브라우저에서 무엇이 사라지는지 먼저 적어 보는 것이 가장 빠른 판단 기준이다.
HN의 FDEUp은 같은 점을 한 문장으로 말했다.
새 CSS 기능의 폭넓은 지원은 좋지만, 기본적인 사이트 기능이 새 CSS 기능에 의존하게 만드는 것은 나쁘다는 것이다.[^FDEUp]

### 상태를 CSS가 알게 되면 스크립트가 줄어든다

스티키가 붙었는지, 스크롤할 수 있는지, 앵커가 뒤집혔는지를 CSS가 묻게 되면,
그동안 스크립트와 `IntersectionObserver`가 하던 상태 감지가 선언으로 바뀐다.
지금 이런 코드를 쓰고 있다면 어느 기능이 이를 대체할지 목록으로 만들어 두고,
지원이 넓어지는 시점에 교체할 후보로 관리하는 것이 좋다.

---

[^lioeters]: <https://news.ycombinator.com/item?id=50175657>

[^afavour]: <https://news.ycombinator.com/item?id=50175703>

[^bradley13]: <https://news.ycombinator.com/item?id=50177973>

[^longor1996]: <https://news.ycombinator.com/item?id=50178203>

[^PennRobotics]: <https://news.ycombinator.com/item?id=50178201>

[^fodkodrasz]: <https://news.ycombinator.com/item?id=50176887>

[^alberth]: <https://news.ycombinator.com/item?id=50175782>

[^herpdyderp]: <https://news.ycombinator.com/item?id=50175766>

[^paulhebert]: <https://news.ycombinator.com/item?id=50176056>

[^piro0919]: <https://news.ycombinator.com/item?id=50176890>

[^louiskottmann]: <https://news.ycombinator.com/item?id=50177054>

[^FDEUp]: <https://news.ycombinator.com/item?id=50175434>

[^Pomax]: <https://lobste.rs/s/vidyh0/future_css#c_pyhz6x>

[^bramh]: <https://lobste.rs/s/vidyh0/future_css#c_1phk82>
