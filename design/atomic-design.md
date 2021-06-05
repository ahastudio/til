# Atomic Design

<https://atomicdesign.bradfrost.com/>

이건 디자인 방법론. 부주의하게 쓰지 않도록 주의하자.

거칠게 요약하면 이렇게 볼 수 있다:

- Atom: 가장 작은 단위. Text 같은 기본 요소에 시각적 꾸밈이 더해진 상태.
- Molecule: 의미를 갖는 단위. 기존에 만든 걸 예로 든다면, TextField 같은 식으로 Label Text와 Input Control이란 두 Atom이 결합된 상태.
- Organism: 우리가 명백히 인지하는 단위. 하나의 기능을 온전히 전달한다. 흔히 보는 Widget 같은 거라 생각해도 좋다. Form, Menu 같은 게 여기에 속한다.
- Template: 이걸 이해하려면 Page를 먼저 파악해야 한다. Page의 공통된 부분을 추출한 것이라고 보면 된다. 여기부터는 사실상 Atomic 철학과는 무관하다.
- Page: 전체 화면. Organism이 적절히 배치된다.

다시 강조하면, 이건 layered architecture가 아니다. 우리가 디자인 요소를 만들 때 사용할 사고의 프레임워크다.
사실 (일 잘하는) 대부분의 사람들은 이를 의식하지 않고 써왔다.
의식하면 유용한 순간들이 있고, 그래서 추출한 디자인 방법론이다.
