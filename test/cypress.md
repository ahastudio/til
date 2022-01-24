# Cypress - JavaScript End to End Testing Framework

<https://www.cypress.io/>

<https://github.com/cypress-io/cypress>

## 튜토리얼

[Cypress 시작하기](https://github.com/ahastudio/til/blob/main/test/20201208-cypress.md)

## `scrollBehavior`

Cypress에서 `click` 등 몇 가지 동작을 테스트하려고 하면,
이벤트 발생 전에 대상 DOM 객체를 찾아서 스크롤하는 작업을 먼저 수행한다.
화면 좌표 등을 활용하는 테스트를 작성하면 이 부분에서 문제가 발생할 수 있고,
`scrollBehavior` 옵션을 이용해 스크롤 여부를 제어할 수 있다.

<https://docs.cypress.io/guides/references/configuration#Actionability>

<https://docs.cypress.io/guides/core-concepts/interacting-with-elements#Actionability>

## `type()`

마우스를 조작하던 도중에 `type()`을 쓰면
클릭 이벤트가 개입해서 문제가 될 수 있음.

<https://docs.cypress.io/api/commands/type#When-element-is-not-in-focus>

> **When element is not in focus**
>
> If the element is currently not in focus, before issuing any keystrokes
> Cypress will first issue a .click() to the element to bring it into focus.
