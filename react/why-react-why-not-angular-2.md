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

# Angular 특화 문법

자주 인용되는 Angular의 장점 중 하나는 프로그래머가 아닌 사람도 쓰기 좋다는 겁니다. “디자이너가 JavaScript에 대해 아무 것도 몰라도 HTML만 바꾸면 됩니다”는 식이죠. 저는 이런 식으로 일해본 적이 없고, 이게 잘 된다고 말할 수 없습니다(경험이 있는 분은 아래에 댓글을 남겨주세요).

그래서 Angular 2는 “HTML을 JavaScript에 안에 넣기” 대신 “HTML에 JavaScript 넣기”란 철학을 유지함으로써 이 장점을 계속 가져갑니다.

Angular가 이해하는 걸 제외하고 HTML은 진짜 JavaScript가 아닙니다. 그건 (JavaScript의) 서브셋입니다(Anagular에서 뭔가 추가한 JavaScript입니다). 그리고 추상화가 빈약합니다. 이상하게 되기 전까진 훌륭하게 작동합니다. 거기에 써넣는 코드를 예측해야 하는 상황에 처하게 됩니다.

JavaScript 같은 문법 위에 JavaScript가 아닌 게 있습니다. Angular 1은 `ng-repeat="item in items"`와 `ng-click="doStuff()"` 같은 게 있습니다. Angular 2는 Angular directive 혼란이 있다는 이유로 `*ngFor="let item of items"`로 변경했습니다. [이걸 작성하는 두 가지 다른 방식이 있고, 주입할 수 있는 변수도 더 있습니다.](https://angular.io/docs/ts/latest/api/common/NgFor-directive.html)

![Angular Dev Cycle](https://daveceddia.com/images/angular_dev_cycle@2x.png)

하지만 React에선 이렇게 씁니다:

```javascript
let List = function({ items }) {
  return (
    <ul>
      {items.map(item =>
        <li key={item.id}>{item.name}</li>
      )}
    </ul>
  );
}
```

괄호 안에 있는 코드는 진짜 실제 JavaScript(와 JSX li)입니다. 당신이 기대하는 현재 scope에 있는 모든 걸 접근할 수 있고, 아마 당신이 생각하는대로 작동할 겁니다. :)

## TypeScript


(...작성 중...)

