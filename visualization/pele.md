# Pele: Mermaid 문법을 CSS로 꾸미는 SVG로 그리는 라이브러리

<https://pele.run/>

<https://github.com/obsidianmd/pele>

HN 토론: <https://news.ycombinator.com/item?id=50132193> (436점, 39개 댓글)

GN 토론: <https://news.hada.io/topic?id=35549>

## 소개

Pele는 Mermaid 문법으로 쓴 다이어그램을 SVG로 렌더링하는 오픈소스 라이브러리다.
Obsidian 팀이 Obsidian에서 쓰려고 만들었고,
홈페이지에는 kepano(Steph Ango)가 만든 것으로 적혀 있다.
이름은 하와이 신화의 화산 여신 펠레에서 따왔다.
저장소는 2026년 10월 초에 공개되었고 TypeScript로 작성되었다.
홈페이지는 MIT 라이선스라고 소개하지만,
GitHub API는 라이선스를 `NOASSERTION`으로 표시하므로
도입 전에 저장소의 라이선스 파일을 직접 확인하는 편이 안전하다.

홈페이지가 내세우는 숫자는 다음과 같다.

| 항목             | 값                               |
| ---------------- | -------------------------------- |
| 번들 크기 (gzip) | 230 KB                           |
| 렌더링 시간      | 0.05–0.3 ms                      |
| 직접 의존성      | 0개                              |
| 지원 범위        | Mermaid 12.1.0의 모든 다이어그램 |
| Mermaid.js 대비  | 6배 작고 최대 500배 빠름         |

이 숫자는 모두 프로젝트가 직접 잰 값이다.
측정 환경과 비교 대상 다이어그램은 홈페이지에서 확인되지 않았다.

## 동작 방식

### 문법만 따르고 배치는 따로 한다

Pele는 Mermaid의 문법을 입력으로 받지만, 노드 위치와 간격, 간선 경로는 자체
레이아웃으로 계산한다.
그래서 같은 소스라도 Mermaid와 결과 모양이 다르다.
Hacker News에서 lukeify가 Mermaid는 장난감 수준을 넘는 다이어그램만 그려도
배치가 엉망이라 스타일 문제는 사소하게 느껴진다고 불평하자,
kepano는 바로 그래서 문법만 따르고 레이아웃은 따르지 않도록 설계했다고
답했다.[^kepano]
플레이그라운드의 Compare 모드로 두 결과를 나란히 볼 수 있다.

Mermaid와 다른 동작 가운데 하나는 서브그래프의 방향이다.
Pele에서는 서브그래프가 바깥 노드와 연결되어도 자기 `direction`을 유지한다.
Ancapistani는 이 한 가지만으로도 Mermaid.js보다 느리더라도 갈아탈 이유가
충분하다고 적었다.[^ancapistani]

### 색과 글꼴은 CSS 변수가 정한다

색상은 `--pele-bg`, `--pele-fg`, `--pele-accent` 같은 CSS 변수로,
차트와 범주 색은 `--pele-series-1`부터 `--pele-series-8`까지로 정한다.
글꼴은 `--pele-font`, `--pele-font-mono`가 맡는다.
색이 변수로 연결되어 있으므로 다크 모드로 바꿀 때 다시 렌더링할 필요가 없고,
`@media (prefers-color-scheme: dark)` 안에서 변수만 바꾸면 된다.
개별 요소는 `.pele-node`, `.pele-edge` 같은 클래스와 `[data-id]` 속성 선택자로
꾸밀 수 있다.
Mermaid 테마는 적용되지 않는다.

haburka는 Mermaid를 서버에서 돌리고 CSS 변수로 다크 모드를 맞추는 일이
악몽이었다며 반겼다.[^haburka]
9dev도 Mermaid와 panzoom, 몇 가지 우회책을 조합하던 문서 사이트를 Pele로
옮겼더니 스타일과 다크 테마가 해결되었고 배치도 더 나아졌다고 전했다.[^9dev]

### 글꼴은 측정에 쓰이므로 먼저 준비되어야 한다

색과 달리 글꼴은 다시 렌더링 없이 바뀌지 않는다.
Pele는 라벨 텍스트를 측정해서 노드 크기를 정하기 때문에,
렌더링 전에 글꼴이 준비되어 있어야 한다.
브라우저에서는 canvas로, 그 밖의 환경에서는 내장된 글자 폭 표로 측정한다.
`mount()`는 CSS의 글꼴 변수를 읽어 들이고,
글꼴을 바꾼 뒤에는 `refresh()`로 라벨을 다시 측정해야 한다.

브라우저 밖에서도 측정할 수단이 있다는 점은 서버 렌더링과 이어진다.
nickmain은 공식 Mermaid 라이브러리가 여전히 레이아웃에 브라우저나 헤드리스
브라우저를 요구한다면 Pele는 다른 곳에 Mermaid 렌더링을 넣을 때 반가운
소식이라고 했다.[^nickmain]

## 사용하기

기본 사용법은 `render()`로 SVG 문자열을 받아 페이지에 넣는 것이다.
오류 메시지에는 다이어그램 소스가 들어 있으므로 `textContent`로 표시한다.

```javascript
import { PeleError, render } from 'pele';

try {
  container.innerHTML = render(source).svg;
} catch (error) {
  if (!(error instanceof PeleError)) throw error;
  // 메시지에 소스가 포함되므로 innerHTML이 아닌 textContent로 표시한다
  container.textContent = error.message;
}
```

번들 크기를 줄이려면 필요한 다이어그램 종류만 등록하거나 처음 쓸 때 불러온다.

```javascript
import { register, render } from 'pele/core';
import flowchart from 'pele/diagrams/flowchart';
import sequence from 'pele/diagrams/sequence';

// pele/core에는 다이어그램 종류가 없으므로 쓸 것만 등록한다
register(flowchart, sequence);
const { svg } = render(source);
```

```javascript
import { renderAsync } from 'pele/lazy';

// 다이어그램 종류를 처음 쓰는 시점에 비동기로 불러온다
const { svg } = await renderAsync(source);
```

컨테이너에 붙여 두고 소스를 갱신할 때는 `mount()`를 쓴다.

```javascript
import { mount } from 'pele';

const diagram = mount(container, source);
diagram.update('flowchart LR\n  A[Draft] --> B[Published]');
```

번들러 없이 쓸 때는 CDN의 브라우저 스크립트가 전역 `pele`를 정의한다.
`@1`은 최신 1.x를 가리키므로, 사이트를 특정 릴리스에 고정하려면
`@1.6.0`처럼 정확한 버전을 쓴다.

```html
<script src="https://cdn.jsdelivr.net/npm/pele@1/dist/pele.global.js"></script>
```

## 신뢰할 수 없는 다이어그램 다루기

Pele는 다른 사람이 쓴 다이어그램을 렌더링하는 상황을 전제로 설계되었다.
다이어그램 텍스트를 이스케이프하고, 링크와 스타일을 걸러 내며,
결과는 SVG 도형과 텍스트, 링크, 이미지뿐이고 스크립트나 이벤트 핸들러는
만들지 않는다.
`click` 문의 JavaScript 콜백은 무시하고 링크만 지원한다.

기본 허용 범위와 한도는 다음과 같다.

| 항목        | 기본값                                     |
| ----------- | ------------------------------------------ |
| 링크 스킴   | `http`, `https`, `mailto`, `tel`, 상대 URL |
| 이미지 스킴 | `http`, `https`, 상대 URL                  |
| 항상 차단   | `javascript:`, `data:`, `vbscript:`        |
| 소스 길이   | 50,000자                                   |
| SVG 출력    | 4,000,000자                                |
| 순서도 간선 | 5,000개                                    |

라이브러리가 막아 주지 않는 부분은 애플리케이션 몫이다.
오류는 `textContent`로 표시하고, 아이콘 마크업은 신뢰할 수 있는 출처에서만
공급하며, 다이어그램 작성자가 렌더링 옵션을 직접 정하지 못하게 해야 한다.

이 설계는 Obsidian의 사정에서 나왔다.
blazarquasar가 옮긴 kepano의 트윗에 따르면, Mermaid 12.1은 세 번째 레이아웃
엔진을 들여왔고 CVE 이력도 걱정스러워서
Obsidian 1.13에는 안전하지 않은 Mermaid 다이어그램에 대한 토글과 경고를
새로 넣어야 했다.[^blazarquasar]
같은 인용에서 kepano는 Mermaid.js가 mermaid.ai로 넘어가며 원래 비전을 잃고
있다고 평가했다.
이는 Mermaid 쪽이 아닌 경쟁 프로젝트 저자의 판단이라는 점을
감안해서 읽어야 한다.

## 트레이드오프

### 같은 문법, 다른 그림

Mermaid 문법을 유지한다는 것은 기존 소스를 그대로 가져올 수 있다는 뜻이지만,
결과 그림까지 같다는 뜻은 아니다.
Mermaid로 그린 그림을 기준으로 문서를 쓰고 캡처까지 해 둔 팀이라면,
Pele로 바꾸는 순간 배치가 달라진다.
레이아웃이 더 낫다는 평이 많더라도
“더 낫다”는 것과 “예전과 같다”는 것은 다른 요구다.
배치를 손으로 맞춘 다이어그램이 많을수록 전환 비용이 커진다.

같은 이유로 두 렌더러를 섞어 쓰면 혼란스럽다.
GitHub처럼 Mermaid로 렌더링하는 곳에 같은 소스를 올리면 다른 그림이 나온다.
소스의 이식성은 지켜지지만 그림의 이식성은 사라진다.

### 지원하지 않는 것

ZenUML과 외부 Mermaid 플러그인은 지원하지 않는다.
임의의 HTML 라벨 대신 줄바꿈과 굵게, 기울임만 되는 SVG 텍스트를 쓴다.
`fa:fa-car` 같은 아이콘은 `icons` 매개변수로 직접 공급해야 한다.
HTML 라벨에 표나 이미지를 넣어 쓰던 다이어그램은 이 경계에서 깨진다.
보안 모델을 지키려고 일부러 포기한 기능이므로, 앞으로도 돌아올 가능성은
낮다고 보는 편이 맞다.

### 상류에 합치지 않은 이유

CrimsonRain은 Pele를 Mermaid의 일부로 기여할 수는 없었느냐고
물었다.[^crimsonrain]
문법은 공유하되 레이아웃 엔진과 보안 모델이 통째로 다르므로,
이것은 기여라기보다 대체 구현에 가깝다.
대가는 문법의 진화를 계속 따라가야 한다는 점이다.
지원 범위가 “Mermaid 12.1.0”이라는 특정 버전으로 표시된 것도 그 때문이고,
Mermaid가 새 다이어그램 종류나 문법을 추가할 때마다 Pele가 뒤따라야 한다.

## 기억할 원칙

### 문법과 렌더러는 분리할 수 있다

Mermaid의 가치가 텍스트로 다이어그램을 적는 문법에 있었다면,
그 문법은 하나의 구현에 묶일 이유가 없다.
Pele는 문법을 사실상의 표준으로 삼고 렌더러를 교체했다.
dbg31415가 짚었듯 텍스트 다이어그램은 버전 관리에 잘 맞고
LLM이 마크다운 파일 하나 안에서 편집하기도 쉽다.[^dbg31415]
그렇다면 문법은 더 널리 퍼지고, 렌더러는 용도에 따라 갈라지는 흐름이 이어질
것이다.
도입을 판단할 때는 문법 호환성과 그림의 동일성을 별개의 질문으로 다뤄야 한다.

---

[^kepano]: <https://news.ycombinator.com/item?id=50134925>

[^ancapistani]: <https://news.ycombinator.com/item?id=50137419>

[^haburka]: <https://news.ycombinator.com/item?id=50138796>

[^9dev]: <https://news.ycombinator.com/item?id=50139527>

[^nickmain]: <https://news.ycombinator.com/item?id=50133359>

[^blazarquasar]: <https://news.ycombinator.com/item?id=50138731>

[^crimsonrain]: <https://news.ycombinator.com/item?id=50136362>

[^dbg31415]: <https://news.ycombinator.com/item?id=50135861>
