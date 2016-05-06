# [Why React? Why not Angular 2?](https://daveceddia.com/why-react-why-not-angular2/)

Angular 1.x가 낡어가고 Angular 2가 분발하서, 많은 1.x 개발자들은 다음이 뭘까 궁금해 하고 있습니다. Angular 2를 선택해야 할까? React는? 아니면 다른 거?

제가 최근에 독자들에게 받는 질문은 왜 Angular 2 대신 React에 대한 글을 쓰고 있냐는 겁니다.

왜 React가 Angular 2보다 나을까요? 음, 저는 Angular 1.x에서 논리적으로 연결되는 것처럼 보이는 Angular 2를 시작했습니다.

## Import와 Dependency Injection(의존성 주입)

일단 코드를 작성하는 게 매우 복잡해 보였습니다. 불필요한 게 너무 많습니다: 모듈 import, privider 목록 작성, 생성자를 통한 주입, 인스턴스 변수에 넣기.

뭐든지 사용하기 전에 같은 이름을 4번이나 타이핑합니다.

![YO DAWG](https://daveceddia.com/images/yo-dawg-imports.jpg)

오, 하나 더: 앱을 시작할 때(Angular 2에서 bootstrap 실행할 때), 나중에 주입할 provider 목록을 넘겨줘야 합니다. 이건 기억할 게 하나 더 생기는 거고, 에러가 날 수 있는 게 하나 더 생기는 겁니다.

이런 걸 하는 이유는 (Spring처럼) DI 시스템을 이용해서 wire하기 위해서다.

Angular 1에선 모듈 시스템으로 쓰기 위해 DI 시스템이 필요했습니다. 하지만 모듈이 생기고, 변환기(Babel이나 TypeScript 컴파일러 등)가 import나 require 등을 가능하게 한 지금은 DI의 혜택이 별로 없습니다. 그냥 import해서 쓰면 됩니다.

프레임웤 레벨의 DI 없이 테스트하는 건 좀 어렵지만, 해결할 방법은 이미 있습니다.

# Angular 특화 구문

(...작성 중...)

