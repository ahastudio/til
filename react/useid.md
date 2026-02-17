# `useId` Hook

<https://ko.react.dev/reference/react/useId>

> **useId를 사용하는 것이 카운터를 증가하는 것보다 나은 이유는 무엇일까요?**
>
> `useId`의 주요 이점은 React가
> [서버 렌더링](https://ko.react.dev/reference/react-dom/server)과 함께
> 작동하도록 보장한다는 것입니다. 서버 렌더링을 하는 동안 컴포넌트는 HTML
> 결과물을 생성합니다. 이후, 클라이언트에서
> [hydration](https://ko.react.dev/reference/react-dom/client/hydrateRoot)이
> HTML 결과물에 이벤트 핸들러를 연결합니다. hydration이 동작하려면 클라이언트의
> 출력이 서버 HTML과 일치해야 합니다.
