# 나는 왜 Angular 2가 아니라 React를 선택했나?

> *원문:
> [Why React? Why not Angular 2?](https://daveceddia.com/why-react-why-not-angular2/)
> (April 26, 2016)*

Angular 1.x가 낡어가고 Angular 2가 분발하서,
많은 1.x 개발자들은 다음이 뭘까 궁금해 하고 있습니다.
Angular 2를 선택해야 할까? React는? 아니면 다른 거?

제가 최근에 독자들에게 받는 질문은
왜 Angular 2 대신 React에 대한 글을 쓰고 있냐는 겁니다.

왜 React가 Angular 2보다 나을까요?
음, 저는 Angular 1.x에서 논리적으로 연결되는 것처럼 보이는
Angular 2를 시작했습니다.

## Import와 Dependency Injection(의존성 주입)

일단 코드를 작성하는 게 매우 복잡해 보였습니다.
불필요한 게 너무 많습니다:
모듈 import, privider 목록 작성, 생성자를 통한 주입, 인스턴스 변수에 넣기.

뭐든지 사용하기 전에 같은 이름을 4번이나 타이핑합니다.

![YO DAWG](https://daveceddia.com/images/yo-dawg-imports.jpg)

오, 하나 더: 앱을 시작할 때(Angular 2에서 bootstrap 실행할 때),
나중에 주입할 provider 목록을 넘겨줘야 합니다.
이건 기억할 게 하나 더 생기는 거고, 에러가 날 수 있는 게 하나 더 생기는 겁니다.

이런 걸 하는 이유는 (Spring처럼) DI 시스템을 이용해서 wire하기 위해서다.

Angular 1에선 모듈 시스템으로 쓰기 위해 DI 시스템이 필요했습니다.
하지만 모듈이 생기고, 변환기(Babel이나 TypeScript 컴파일러 등)가
import나 require 등을 가능하게 한 지금은 DI의 혜택이 별로 없습니다.
그냥 import해서 쓰면 됩니다.

프레임워크 레벨의 DI 없이 테스트하는 건 좀 어렵지만, 해결할 방법은 이미 있습니다.

## Angular 특화 문법

자주 인용되는 Angular의 장점 중 하나는
프로그래머가 아닌 사람도 쓰기 좋다는 겁니다.
“디자이너가 JavaScript에 대해 아무 것도 몰라도 HTML만 바꾸면 됩니다”는 식이죠.
저는 이런 식으로 일해본 적이 없고,
이게 잘 된다고 말할 수 없습니다(경험이 있는 분은 아래에 댓글을 남겨주세요).

그래서 Angular 2는 “HTML을 JavaScript에 안에 넣기” 대신
“HTML에 JavaScript 넣기”란 철학을 유지함으로써 이 장점을 계속 가져갑니다.

Angular가 이해하는 걸 제외하고 HTML은 진짜 JavaScript가 아닙니다.
그건 (JavaScript의) 서브셋입니다(Anagular에서 뭔가 추가한 JavaScript입니다).
그리고 추상화가 빈약합니다.
이상하게 되기 전까진 훌륭하게 작동합니다.
거기에 써넣는 코드를 예측해야 하는 상황에 처하게 됩니다.

JavaScript 같은 문법 위에 JavaScript가 아닌 게 있습니다.
Angular 1은 `ng-repeat="item in items"`와
`ng-click="doStuff()"` 같은 게 있습니다.
Angular 2는 Angular directive 혼란이 있다는 이유로
`*ngFor="let item of items"`로 변경했습니다.
[이걸 작성하는 두 가지 다른 방식이 있고, 주입할 수 있는 변수도 더 있습니다.](https://angular.io/docs/ts/latest/api/common/NgFor-directive.html)

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

괄호 안에 있는 코드는 진짜 실제 JavaScript(와 JSX li)입니다.
당신이 (JavaScript 코드를 보며) 기대하는
현재 scope에 있는 모든 걸 접근할 수 있고,
아마 당신이 생각하는대로 작동할 겁니다. :)

## TypeScript

저는 TypeScript와 일반적인 정적 타이핑의 열성 팬이 아닙니다.
그건 확실히 몇 가지 장점이 있습니다: 더 나은 IDE 통합,
더 나은 자동완성, 오타를 내지 않았다는 더 나은 확신 등…

하지만 단위 테스트를 작성하기 위해 모의 객체를 인터페이스를 상속 받게 하고,
같은 인터페이스를 상속하는 식으로 모든 걸 클래스로 만들고 싶지는 않습니다.
저는 이게 더 나은 설계나 더 나은 유지보수를 가능케 한다고 생각하지 않습니다.
그냥 코드를 더 많이 작성하게 될 뿐이죠.

JavaScript의 힘의 일부는 느슨함이고, 저는 이걸 진짜로 즐기고 있어요. :)
저는 커뮤니티가 이 지점에서 나뉜다는 걸 알고 있습니다:
독자의 절반은 고개를 끄덕일 거고,
다른 절반은 제가 미쳤다고 생각할 겁니다(“JavaScript는 끔직합니다!
TypeScript는 제대로 된 언어로 만들어줍니다!”).

공식적으론,
[Angular 2를 JavaScript로](https://daveceddia.com/angular-2-in-plain-js)
코딩하는 게 가능하고, 작동하지만, 아직 지원이 좀 부족합니다.
제 생각에 대부분은 TypeScript를 쓸 거고,
Stack Overflow 질문이나 다른 커뮤니티 지원이 많지 않을 거라,
JavaScript로 Angular 2를 쓰는 건
뭔가 문제가 생길 때마다 사투를 벌이게 될 겁니다.

## React

만약 내 머리에 총을 들이대고 지금 당장 올바른 걸 선택하라고 한다면...
지금 당장 내 선호는 React 입니다.
(React만 쓴다면) 코드가 더 단순하고,
코드를 작성하는 동안 무슨 일이 벌어질지 이해하기 더 쉽습니다.
JSX를 배워야 하지만, 그 다음엔 그냥 JavaScript 입니다.

Redux는 확실히 좀 더 많은 복잡함과 학습과 결정을 더합니다.
하지만 아직까지는,
그 컨셉을 한번 이해하면 화면 뒤에서 무슨 일이 벌어지는지 이애하는 게 가능합니다.

Angular 1을 쓸 때, 저는 항상 토끼굴에 빠지는 것처럼 느꼈습니다.
배워도 배워도 끝이 없죠.
손으로 컴파일하고, 소화 주기를 막고, Angular 내부를 공부하고…
React 그렇게 느껴지지 않습니다: 더 깔끔하게 추상화되어 있습니다.

Angular 2는, 더 많은 (그리고 더 복잡한) 내부를 배워야 할까,
아니면 최소한 다시 배워야 할까 걱정입니다.

어쨌든, 이게 지금 당장 제 선택입니다.
어떻게 생각하세요?
새 프로젝트를 위한 당신의 선택은?

댓글을 남겨주세요!
[메일을 보내주세요](mailto:dave@daveceddia.com)!
이걸로 토론해 봅시다.

---

한국어로 옮긴 게 어색합니다.
많은 지적질 부탁합니다:
[@ahastudio](https://j.mp/1CAfmQ8)
