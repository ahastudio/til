# Tiptap - Dev Toolkit Editor Suite

> Build AI-native editors faster 🚀 with production-ready tools

<https://tiptap.dev/>

<https://github.com/ueberdosis/tiptap>

HN 토론: <https://news.ycombinator.com/item?id=36957204> (246점, 103개 댓글)

GN 토론: <https://news.hada.io/topic?id=13585>

## 소개

Tiptap은 “웹 장인들을 위한 헤드리스 리치 텍스트 에디터 프레임워크”를
표방하는 오픈소스 프로젝트로, 신뢰성이 검증된 ProseMirror 라이브러리
위에 구축되어 있다. 헤드리스(headless)하다는 것은 정해진 UI를
제공하지 않는다는 뜻으로, 개발자가 클래스를 오버라이드하거나
코드를 억지로 수정할 필요 없이 완전한 디자인 자유도를 갖는다는
것을 의미한다. Vue, React, 순수 JavaScript 등 프레임워크에
구애받지 않고 통합할 수 있도록 설계됐다.

핵심 설계는 확장(extension) 기반 아키텍처다. 단순한 텍스트 서식
지정부터 드래그 앤 드롭 블록 편집 같은 고급 기능까지, 문서화된
100개 이상의 확장 기능과 커뮤니티가 만든 확장을 조합해 원하는
편집 경험을 구성할 수 있다. 개발자는 직접 커스텀 확장과 노드
타입을 정의할 수도 있다.

무료 오픈소스 코어에 더해, 협업 편집·댓글·버전 관리·문서 변환·AI
관련 기능을 제공하는 유료 구독형 “Pro Extensions”가 있다.
협업 편집을 위한 백엔드는 Yjs의 CRDT(Conflict-free Replicated
Data Type) 기술을 기반으로 한 오픈소스 프로젝트 Hocuspocus가
담당하며, 에디터와 Hocuspocus가 함께 “Tiptap Suite”의 기반을
이룬다. 코어는 MIT 라이선스로 배포되며, GitHub 기준 3만 7,800개의
스타와 3,100개의 포크를 보유하고 있다.

## 사용법

React 기준 최소 설치는 코어 패키지와 스타터 확장 묶음을 설치하는
것으로 시작한다.

```bash
npm install @tiptap/react @tiptap/pm @tiptap/starter-kit
```

`useEditor` 훅으로 에디터 인스턴스를 만들고 `EditorContent`로
렌더링한다. `extensions` 배열에 필요한 기능을 조합해 넣는 것이
Tiptap의 확장 기반 설계를 가장 직접적으로 드러내는 지점이다.

```tsx
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";

function Editor() {
  const editor = useEditor({
    extensions: [StarterKit],
    content: "<p>Hello, world!</p>",
  });

  return <EditorContent editor={editor} />;
}
```

`StarterKit`은 굵게·기울임 같은 기본 서식, 문단·제목·목록 같은
기본 노드, 실행 취소(undo/redo) 히스토리를 한 번에 묶어 제공하는
편의 패키지다. 특정 기능만 필요하다면 `StarterKit.configure()`로
불필요한 항목을 끄거나, `@tiptap/extension-link`처럼 개별 확장
패키지를 따로 설치해 조합할 수 있다.

```tsx
import Link from "@tiptap/extension-link";

const editor = useEditor({
  extensions: [
    StarterKit.configure({ heading: { levels: [1, 2] } }),
    Link.configure({ openOnClick: false }),
  ],
});
```

UI가 전혀 포함되어 있지 않으므로, 서식 버튼이나 툴바는 `editor`
인스턴스가 제공하는 커맨드 체이닝 API로 직접 구현한다.

```tsx
<button onClick={() => editor.chain().focus().toggleBold().run()}>
  Bold
</button>
```

Vue 3에서는 `@tiptap/vue-3` 패키지의 `useEditor` 컴포저블과
`EditorContent` 컴포넌트를 같은 방식으로 사용하며, 순수
JavaScript 환경에서는 `@tiptap/core`의 `Editor` 클래스를 직접
인스턴스화해 DOM 요소에 마운트한다.

## 분석

### “헤드리스”라는 설계 선택이 프레임워크 중립성과 사업 모델을 동시에 뒷받침한다

Tiptap이 UI를 제공하지 않기로 한 결정은 단순한 기술적 선택이
아니라, 이 프로젝트의 프레임워크 중립성과 수익 모델 모두를
가능하게 하는 전략적 토대다. UI를 갖지 않으면 Vue든 React든
프레임워크에 종속되지 않고 문서 편집 로직만을 순수하게 제공할
수 있으며, 이는 채택 장벽을 크게 낮춘다. 동시에 UI를 제공하지
않기 때문에 “완성된 편집 경험”이라는 더 상위의 가치는 여전히
개발자가 직접 조립하거나 유료 템플릿·Pro Extensions를 통해
얻어야 하는 것으로 남는다. 즉 헤드리스 설계는 무료로 제공할
부분과 유료로 남겨둘 부분의 경계를 자연스럽게 긋는 역할을
겸한다.

HN Launch 스레드에서는 이 추상화 계층이 실제로 얼마나 두꺼운지에
대한 실무자들의 다양한 경험이 공유됐다. Notion의 에디터를 재구축할
프레임워크를 평가했던 한 참여자는 “추상화 계층은 도움이 되지만
동시에 방해가 될 수 있다”며, Android Gboard 입력 버그를 고치는
것처럼 프레임워크 없이 DOM 구조를 직접 제어해야 하는 상황에서
Tiptap의 개념들이 ProseMirror의 개념을 정확히 어떻게 확장하거나
대체하는지 궁금하다고 물었다[^jitl]. 반면 실제로 Tiptap을
ProseMirror 위의 얇은 추상화 계층으로 활용해온 개발자는 React
노드 뷰 지원이 특히 잘 작동한다고 평가하며, 다른 대부분의 기능은
순수 ProseMirror 플러그인으로 직접 구현하는 방식을 택하고
있다고 밝혔다[^TheProTip]. 이는 Tiptap의 추상화가 모든 사용
사례에 균일하게 도움이 되는 것이 아니라, 어떤 기능을 프레임워크에
맡기고 어떤 기능을 직접 제어할지 개발자가 선택적으로 결정해야
하는 계층이라는 것을 보여준다.

GeekNews에서도 비슷한 결의 실사용담이 나왔다. 실제로 Slate로
에디터를 만들다가 Tiptap으로 옮긴 사용자는 문서가 더 거칠고,
모바일 한글 입력 문제나 선택 영역 속성 처리, 플러그인 개발 난도가
더 높게 느껴졌다고 회고했다[^gn-bbulbum-slate]. 다른 사용자는
React처럼 자체 DOM 추상화가 있는 환경에서 외부 컴포넌트를
붙이거나 모듈화하는 작업이 Tiptap 쪽이 더 편했다고 덧붙였다[^gn-firea32-react].
이는 “헤드리스 추상화”가 단순한 취향 문제가 아니라, 프레임워크의
렌더링 모델과 편집기 확장 모델이 만나는 지점에서 실질적인 개발 비용
차이로 이어질 수 있음을 보여준다.

### 확장 생태계의 규모가 진입장벽이자 동시에 해자로 작동한다

100개 이상의 공식 확장과 그보다 많은 커뮤니티 확장이 존재한다는
것은 신규 개발자에게는 학습해야 할 대상이 많다는 뜻이지만,
동시에 이미 이 생태계에 진입한 개발자에게는 대체하기 어려운
전환 비용을 만든다. 특정 프로젝트가 이미 수십 개의 Tiptap
확장을 조합해 편집기를 구성했다면, 다른 에디터 프레임워크로
옮기는 것은 단순히 API를 바꾸는 문제가 아니라 그 모든 확장
기능을 다시 구현하거나 대체재를 찾아야 하는 문제가 된다. 이는
오픈소스 프레임워크가 규모의 경제를 통해 자연스럽게 락인
효과를 만들어내는 전형적인 방식이다.

## 비평

### 무료 코어와 유료 Pro Extensions의 경계가 README만으로는 불분명하다

README는 Pro Extensions가 “유효한 구독”을 필요로 한다고만 밝힐
뿐, 협업 편집이나 AI 기능처럼 실무에서 빈번하게 필요한 기능들
중 정확히 어디까지가 무료이고 어디부터 유료인지 명확한 경계를
제시하지 않는다. Hocuspocus는 오픈소스로 명시되어 있지만
“Content AI”나 문서 버전 관리 같은 기능은 Pro Extensions에
속한다는 것만 알 수 있을 뿐, 실제 가격 정책이나 무료 티어의
한도는 별도로 확인해야 한다. 이는 프로젝트를 채택하려는 팀이
초기 견적을 세우기 어렵게 만드는 정보 공백이다. 실제로 HN
Launch 스레드에서 여러 참여자가 이 경계의 불투명성과 급격한
가격 정책 변화를 직접 지적했다. 한 참여자는 Tiptap이 홈페이지와
가격 페이지의 문구를 “MIT 라이선스이니 원하는 것을 자유롭게 할
수 있다(프리미엄 유료 플러그인 지원)”에서 “신용카드 없이
무료”라는 문구로 바꾸면서 MIT 라이선스에 대한 언급 자체가
사라졌다는 점을 우려했다[^eggbrain]. 또 다른 사용자는 투자
유치 이후 요금제가 오히려 5~7배 인상됐다며, 펀딩을 받으면
가격이 낮아질 것이라 기대했는데 정반대였다고 밝혔다[^NayamAmarshe].
무료 티어에서 월 150달러 요금제로 곧바로 건너뛰는 가격 구조에
대한 불만도 제기됐으며, 한 참여자는 OpenAI나 Firebase처럼
사용량 기반 과금으로 비용을 세밀하게 제어할 수 있게 해달라고
요청했다[^egonschiele].

GeekNews에서도 가격표 자체보다 먼저 문서 읽기 경험에서 유료 기능의
존재감이 강하게 드러난다는 지적이 나왔다. 한 사용자는 설치 문서의
완성도는 괜찮게 봤지만, 문서 중간중간에 유료 구독이 필요한 요소가
섞여 있어 필요하지도 않은 기능에 계속 눈길이 가는 점이 미묘하게
거슬린다고 평가했다[^gn-nemorize-premium]. 이는 가격 페이지를 보기
전에도 이미 제품 경험 차원에서 “무료 코어와 유료 확장”의 경계가
사용자에게 지속적으로 의식된다는 뜻이다.

### “100개 이상의 확장”이라는 수치가 품질이나 유지보수 상태를 보장하지 않는다

확장 생태계의 규모를 강조하는 것은 매력적인 마케팅 포인트지만,
공식 확장과 커뮤니티 확장이 같은 문서 페이지에 섞여 언급되는
방식은 각 확장의 유지보수 활성도나 안정성 수준에 대한 정보를
가려버린다. npm 생태계에서 흔히 나타나듯, 초기에 활발히
관리되다가 방치된 확장이 여전히 “사용 가능한 확장 목록”에
남아 있을 위험이 있으며, 이런 확장을 프로덕션에 채택했다가
유지보수 부담을 떠안게 되는 사례는 확장 기반 프레임워크에서
반복적으로 나타나는 패턴이다.

### 커스텀 확장 개발 문서화 부족이 결국 ProseMirror 학습을 강제한다

Tiptap의 핵심 매력 중 하나는 ProseMirror의 가파른 학습 곡선을
우회할 수 있다는 기대지만, HN 스레드에서 나온 실사용 경험은
이 기대가 항상 충족되지는 않는다는 것을 보여준다. Remirror와
Tiptap을 모두 React와 함께 써본 한 참여자는 커스텀 편집 동작을
구현해야 하는 순간 두 프레임워크 모두 한계를 드러냈다고
지적했다. 커스텀 확장을 만드는 방법에 대한 문서화가 부실해서,
결국 “프레임워크 없이도 필요 없었을 ProseMirror까지 배워야
하는” 상황에 놓이게 됐고, 이 문제로 프로젝트 자체를 중단했다고
밝혔다[^raarts]. 이는 헤드리스 프레임워크가 표준적인 사용
사례에서는 확실히 진입 장벽을 낮추지만, 표준을 벗어나는 순간
그 추상화가 오히려 우회해야 할 장애물로 바뀔 수 있다는 것을
보여준다.

이 문제는 GeekNews에서도 더 구체적인 형태로 반복된다. 한 React 팀은
시작하기 문서와 API 문서 사이의 간극이 커서 실제 POC를 만들면서
`StarterKit`에 무엇이 포함되는지, 왜 `editor.chain().focus()` 같은
호출이 필요한지, 표 관련 확장을 어디까지 추가해야 하는지 같은 기본
판단조차 문서만으로는 매끄럽게 연결되지 않았다고 적었다[^gn-savvykang-docs].
이에 대해 다른 사용자는 `StarterKit`은 말 그대로 출발점일 뿐이고,
`chain().run()` 패턴은 모바일에서 포커스를 유지한 채 액션을 이어갈 때
유용하며, 표 포커스 여부는 `editor.isActive('table')`처럼 판단할 수
있다고 반박했다[^gn-nemorize-rebuttal]. 이 왕복은 Tiptap의 학습 곡선이
절대적으로 높다기보다, 문서가 상정하는 사용자 모델과 실제 도입 팀의
기대치가 어긋날 때 체감 난도가 급격히 올라간다는 점을 잘 보여준다.

## 인사이트

### ProseMirror 위의 두 계층(Tiptap과 BlockNote)이 서로 다른 사업화 전략을 실험하고 있다

Tiptap이 헤드리스 프레임워크로서 프레임워크 중립성과 최대
커스터마이징 자유도를 무기로 삼는 반면, Tiptap 위에 다시
구축된 BlockNote는 정반대로 “완성된 UI 즉시 사용”을 무기로
삼는다. 이는 같은 기반 기술 위에서 서로 다른 고객 세그먼트를
겨냥하는 두 가지 사업 전략이 공존할 수 있다는 것을 보여준다.
Tiptap은 자체 디자인 시스템을 가진 팀이나 세밀한 제어가
필요한 팀을 겨냥하고, BlockNote는 빠른 프로토타이핑이나
Notion류 경험을 즉시 원하는 팀을 겨냥한다. 이런 계층적 분화는
앞으로도 ProseMirror 생태계 안에서 계속 늘어날 가능성이 높으며,
각 계층 사이의 상호 의존 관계(BlockNote의 성공이 Tiptap의
채택을 늘리는 식)는 생태계 전체의 성장을 서로 강화하는 구조를
만든다. 실제로 BlockNote 개발자 본인이 이 Launch HN 스레드에
직접 등장해 이 계층 관계를 확인해주기도 했다. 그는 Tiptap과
ProseMirror 위에 BlockNote를 구축했다고 밝히며, BlockNote는
“UI와 블록 기반 편집이 기본 포함된, 조금 더 배터리가 채워진”
방향을 지향한다고 설명했다. 이는 헤드리스 라이브러리를 직접
다루는 학습 곡선이 부담스러운 개발자를 위한 선택지라는 것이다[^YousefED].
이 코멘트는 이론적 추론이 아니라 생태계 계층 관계를 실제
당사자가 공개적으로 확인해준 사례라는 점에서 의미가 있다.

### Pro Extensions 모델은 오픈소스 프로젝트의 “핵심 기능 유료화” 시점을 미리 설계하는 방식이다

많은 오픈소스 프로젝트가 성장한 뒤에야 수익화 압박에 못 이겨
갑작스럽게 라이선스를 변경하거나 핵심 기능을 유료화해 커뮤니티의
반발을 사는 것과 달리, Tiptap은 처음부터 “코어는 무료, 협업·AI
같은 고급 기능은 유료 구독”이라는 경계를 설계에 내장했다. 이는
오픈소스 프로젝트가 나중에 겪을 수 있는 라이선스 변경 리스크
(예: 특정 데이터베이스나 검색 엔진 프로젝트들이 겪었던 논란)를
사전에 피하는 방법이자, 사용자에게 미리 예측 가능한 사업 모델을
제시하는 방식이다. 다만 이런 사전 설계형 이중 구조가 장기적으로
코어 기능 자체의 발전 속도를 늦추는 유인으로 작동하지는 않는지,
즉 매력적인 신규 기능들이 코어보다 Pro 쪽에 우선 배치되는
경향이 나타나지는 않는지는 시간이 지나야 검증될 문제다.

### 헤드리스 아키텍처의 확산은 UI 레이어의 상품화 속도가 로직 레이어보다 훨씬 빠르다는 것을 방증한다

Tiptap이 의도적으로 UI를 배제한 것은, 편집기 로직(트랜잭션
관리, 스키마 검증, 확장 시스템)은 안정적으로 재사용 가능한
자산인 반면 UI 디자인 트렌드는 몇 년 단위로 바뀌는 훨씬 휘발성
높은 자산이라는 판단을 반영한다. 이는 리치 텍스트 에디터에
국한되지 않는 더 넓은 소프트웨어 아키텍처 트렌드 — 헤드리스
CMS, 헤드리스 이커머스 플랫폼 등 — 와 같은 궤를 그린다.
UI 트렌드의 변화 속도가 로직의 변화 속도를 크게 앞지르는
영역일수록, 헤드리스 아키텍처가 장기적으로 더 지속 가능한
설계 선택이 된다는 것을 여러 산업 영역에서 반복적으로
확인할 수 있다.

---

[^jitl]: <https://news.ycombinator.com/item?id=36957754>
[^TheProTip]: <https://news.ycombinator.com/item?id=36959889>
[^eggbrain]: <https://news.ycombinator.com/item?id=36960818>
[^NayamAmarshe]: <https://news.ycombinator.com/item?id=36966734>
[^egonschiele]: <https://news.ycombinator.com/item?id=36958534>
[^raarts]: <https://news.ycombinator.com/item?id=36970343>
[^YousefED]: <https://news.ycombinator.com/item?id=36959463>
[^gn-bbulbum-slate]: <https://news.hada.io/topic?id=13585#cid23462>
[^gn-firea32-react]: <https://news.hada.io/topic?id=13585#cid23479>
[^gn-nemorize-premium]: <https://news.hada.io/topic?id=13585#cid23396>
[^gn-savvykang-docs]: <https://news.hada.io/topic?id=13585#cid23429>
[^gn-nemorize-rebuttal]: <https://news.hada.io/topic?id=13585#cid23431>
