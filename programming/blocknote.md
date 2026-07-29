# BlockNote - Javascript Block-Based React rich text editor

> Build a Notion-style editor in minutes.

<https://www.blocknotejs.org/>

<https://github.com/TypeCellOS/BlockNote>

## 소개

BlockNote는 ProseMirror와 Tiptap 위에 구축된 오픈소스 React 리치
텍스트 에디터로, Notion 스타일의 블록 기반 편집 경험을 제공하는 데
초점을 맞춘다. 블록을 드래그해 순서를 바꾸고, Tab/Shift+Tab으로
들여쓰기 수준을 조절하며, 슬래시(`/`) 메뉴로 새 블록을 빠르게
삽입하는 등 Notion 사용자에게 익숙한 상호작용을 그대로 재현한다.
실시간 협업 편집, 서식 지정 메뉴, 부드러운 애니메이션, 도움말
플레이스홀더까지 갖춘 완성된 UI 컴포넌트를 제공해 별도의 스타일링
작업 없이 곧바로 프로덕션에 투입할 수 있는 것을 목표로 한다.

프로젝트는 pnpm 워크스페이스 기반 모노레포로 구성되어 있으며,
편집기 핵심 로직을 담은 `@blocknote/core`, React 전용 컴포넌트를
제공하는 `@blocknote/react`, Mantine UI 기반 스타일을 입힌
`@blocknote/mantine`, 그리고 추가 기능을 담은 XL 패키지들로
나뉜다. 핵심 패키지는 MPL-2.0 라이선스로 배포되어 상업적·클로즈드
소스 애플리케이션에서도 사용할 수 있지만 수정한 소스 파일은
공개해야 하며, XL 패키지는 GPL-3.0이면서 상업 라이선스를 별도로
구매할 수 있는 이중 라이선스 구조를 취한다. 네덜란드의 인터넷
인프라 지원 재단 NLNet의 후원을 받고 있다.

## 사용법

React 프로젝트에서는 코어·React 바인딩·UI 패키지(Mantine 기준)
세 가지를 함께 설치한다.

```bash
npm install @blocknote/core @blocknote/react @blocknote/mantine
```

`useCreateBlockNote` 훅으로 에디터 인스턴스를 만들고
`BlockNoteView`로 렌더링하면, 별도의 스타일링 없이 바로 완성된
편집기가 나타난다.

```typescript
import { useCreateBlockNote } from "@blocknote/react";
import { BlockNoteView } from "@blocknote/mantine";
import "@blocknote/core/fonts/inter.css";
import "@blocknote/mantine/style.css";

function App() {
  const editor = useCreateBlockNote();

  return <BlockNoteView editor={editor} />;
}
```

`@blocknote/react` 패키지를 쓰면 완전히 스타일링된 UI가 기본
제공되므로, 위 예제만으로도 즉시 사용 가능한 편집기가 완성된다.
초기 콘텐츠를 지정하려면 `useCreateBlockNote`에 블록 배열을
`initialContent`로 전달한다.

```typescript
const editor = useCreateBlockNote({
  initialContent: [
    {
      type: "paragraph",
      content: "Hello, world!",
    },
  ],
});
```

편집기 상태 변화를 감지하려면 `onChange` 콜백을 등록하고,
`editor.document`로 현재 블록 트리 전체를 가져올 수 있다.

```typescript
const editor = useCreateBlockNote({
  onChange: () => {
    console.log(editor.document);
  },
});
```

Mantine 대신 shadcn/ui나 Ariakit 기반 UI 패키지로 교체할 수도
있으며, 이 경우 `@blocknote/mantine` 자리에 해당 패키지를 설치하고
`BlockNoteView`만 그 패키지에서 가져오면 나머지 코드는 그대로
유지된다. 커스텀 블록 타입이 필요하면 `@blocknote/core`의
`createReactBlockSpec`으로 새 블록을 정의하고 스키마에 등록한다.

## 분석

### Notion 스타일 UX를 재현하는 대신 ProseMirror 생태계의 검증된 기반을 재사용한다

BlockNote가 스스로를 “ProseMirror와 Tiptap 위에 구축됐다”고 명시하는
것은 이 프로젝트의 전략을 압축적으로 보여준다. 문서 편집의 핵심
난제 — 트랜잭션 기반 상태 관리, 커서와 선택 영역 추적, 스키마
검증 — 를 처음부터 다시 푸는 대신, 이미 검증된 ProseMirror의
문서 모델과 Tiptap의 확장 시스템을 그대로 가져오고, 그 위에
Notion 특유의 블록 인터랙션 계층만을 새로 얹는 방식을 택했다.
이는 리치 텍스트 에디터 생태계가 이미 충분히 성숙해, 새로운
프로젝트가 밑바닥부터 에디터 엔진을 재발명하기보다 기존 엔진
위에서 차별화된 사용자 경험을 조립하는 방향으로 수렴하고 있다는
것을 보여주는 사례다.

### 이중 라이선스 구조는 오픈소스 편집기가 수익화 압박에 대응하는 방식을 보여준다

핵심 기능은 MPL-2.0으로 공개하고, 더 고급 기능을 담은 XL
패키지는 GPL-3.0과 상업 라이선스를 병행하는 구조는, 오픈소스
리치 텍스트 에디터가 지속 가능한 사업 모델을 찾아가는 전형적인
패턴을 보여준다. MPL-2.0은 상업적 이용을 허용하면서도 수정된
파일의 공개 의무를 지워 코드 유출을 어느 정도 억제하고, XL
패키지의 GPL-3.0은 상업적으로 이 기능을 쓰려는 기업이 사실상
유료 라이선스를 구매하도록 유도하는 효과를 낸다. 이는 완전
무료 오픈소스와 완전 유료 SaaS 사이에서, 커뮤니티 기여를
유지하면서도 수익을 확보하려는 절충안이다.

## 비평

### “즉시 사용 가능한 UI”라는 강점이 동시에 커스터마이징의 한계로 작동할 수 있다

BlockNote의 핵심 세일즈 포인트는 Mantine 기반의 완성된 UI를
그대로 붙여 쓸 수 있다는 것이지만, 이는 동시에 특정 디자인
시스템에 대한 종속을 함의한다. 이미 자체 디자인 시스템을 갖춘
애플리케이션에 통합하려면 결국 Mantine 스타일을 오버라이드하거나
UI 레이어를 걷어내야 하는데, 이 작업의 난이도는 README만으로는
가늠하기 어렵다. Tiptap처럼 완전히 헤드리스(headless)한 접근과
비교하면, BlockNote의 “완성된 UI 우선” 전략은 빠른 프로토타이핑에는
유리하지만 이미 확립된 디자인 언어를 가진 프로덕트에는 오히려
마찰을 일으킬 수 있다.

### Notion 스타일 재현이 실제 문서 편집 요구사항과 항상 일치하지는 않는다

Notion의 블록 기반 UX는 개인 노트나 지식 관리 도구에는 잘
맞지만, 법률 문서나 학술 논문처럼 선형적이고 정교한 서식 제어가
필요한 텍스트 편집 요구사항과는 결이 다르다. README가 강조하는
기능들(드래그 앤 드롭, 슬래시 메뉴, 블록 들여쓰기)은 모두 Notion류
워크스페이스 도구에 최적화된 상호작용이며, 이런 상호작용 패턴이
모든 리치 텍스트 편집 시나리오에 적합한 것은 아니다. 즉 BlockNote는
범용 리치 텍스트 에디터가 아니라 특정 UX 패러다임에 특화된
도구이며, 이 특화가 강점이자 동시에 적용 범위의 한계로 작동한다.

## 인사이트

### Notion류 UX가 리치 텍스트 에디터 시장의 사실상 표준 참조 모델이 되고 있다

BlockNote가 Notion 스타일을 명시적으로 표방하는 것은 우연이
아니다. Notion이 대중화시킨 블록 기반 편집 패러다임은 이제 여러
에디터 라이브러리가 자신을 설명할 때 기준점으로 삼는 사실상의
업계 표준 어휘가 됐다. 이는 특정 제품의 UX가 경쟁 제품들의
설계 언어 자체를 재편할 만큼 지배적인 영향력을 갖게 되는 현상을
보여주는 사례이며, 향후 등장할 새로운 에디터 라이브러리들도
“Notion과 얼마나 유사한가, 혹은 어떻게 다른가”를 기준으로 스스로를
포지셔닝하게 될 가능성이 높다.

### ProseMirror 생태계의 계층화가 에디터 시장을 인프라와 경험 계층으로 분리하고 있다

ProseMirror(기반 엔진) 위에 Tiptap(프레임워크 중립적 확장
계층)이 있고, 그 위에 다시 BlockNote(특정 UX에 특화된 완성형
제품)가 쌓이는 구조는, 리치 텍스트 에디터 생태계가 통신 프로토콜
스택처럼 계층화되고 있다는 것을 보여준다. 각 계층은 서로 다른
종류의 회사에게 서로 다른 사업 기회를 제공한다. ProseMirror는
안정성과 정확성으로 신뢰를 쌓고, Tiptap은 범용 확장성으로
개발자 도구 시장을 공략하며, BlockNote는 특정 최종 사용자
경험으로 제품을 차별화한다. 이런 계층화는 앞으로 에디터 시장의
경쟁이 “누가 더 나은 엔진을 만드는가”에서 “누가 기존 엔진 위에
더 매력적인 경험을 조립하는가”로 이동하고 있다는 것을 시사한다.

### 재작성이 아니라 합성이 특정 생태계 성숙 단계의 지배적 전략이 될 수 있다

같은 시기에 등장한 Wordgard(ProseMirror를 처음부터 재작성한
프로젝트)와 BlockNote(ProseMirror와 Tiptap을 그대로 재사용해
그 위에 새 경험을 쌓은 프로젝트)는 정반대의 전략을 취하고
있다는 점에서 흥미로운 대조를 이룬다. 이는 성숙한 생태계에서
새로운 프로젝트가 취할 수 있는 두 가지 근본적으로 다른 경로 —
기반을 다시 놓거나, 기존 기반 위에 새로운 층을 쌓는 것 — 를
동시에 보여주는 자연 실험에 가깝다. 원저작자만이 가질 수 있는
깊은 이해와 브랜드 신뢰를 가진 경우(Wordgard의 Haverbeke처럼)
재작성이 합리적 선택이 될 수 있지만, 그런 위치에 있지 않은
대다수 프로젝트에게는 기존 기반 위에 합성하는 전략이 훨씬 낮은
리스크로 시장에 도달하는 길이라는 것을 BlockNote의 접근이
보여준다.
