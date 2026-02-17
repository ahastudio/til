# `useEffectEvent`

<https://react.dev/reference/react/useEffectEvent>

React 19.2에서 정식으로 추가된 Hook. Effect 안에서 "이벤트적인" 로직을 분리할 수
있게 해준다.

## 문제

Effect 안에서 최신 props나 state를 읽어야 하지만, 그 값이 바뀔 때마다 Effect가
다시 실행되는 건 원치 않는 경우가 있다.

```javascript
function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on("connected", () => {
      // theme이 바뀔 때마다 재연결하고 싶지 않다
      showNotification("연결됨!", theme);
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, theme]); // theme 때문에 재연결됨
}
```

`theme`은 Effect의 의존성이지만 `theme`이 바뀐다고 재연결할 필요는 없다.

### 기존 우회 방법: `useRef`

```javascript
function ChatRoom({ roomId, theme }) {
  const themeRef = useRef(theme);
  useEffect(() => {
    themeRef.current = theme;
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on("connected", () => {
      showNotification("연결됨!", themeRef.current);
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);
}
```

동작은 하지만 번거롭고, 실수하기 쉬운 패턴이다.

## 해결: `useEffectEvent`

```javascript
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification("연결됨!", theme);
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on("connected", () => {
      onConnected();
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // theme이 의존성에서 빠진다
}
```

`useEffectEvent`로 감싼 함수는 항상 최신 props와 state를 참조하면서도 Effect의
의존성에 포함되지 않는다.

## 규칙

- Effect 또는 다른 Effect Event 안에서만 호출할 수 있다.
- 렌더링 중에 호출하거나 다른 컴포넌트에 전달하면 안 된다.
- 컴포넌트 또는 커스텀 Hook의 최상위에서만 선언할 수 있다 (조건문, 반복문 안에서
  불가).
- 의존성 배열을 우회하기 위한 용도로 사용하면 안 된다. 진짜 이벤트적인 로직에만
  사용해야 한다.

## 참고

Separating Events from Effects
<https://react.dev/learn/separating-events-from-effects>

[React has finally solved its biggest problem: The joys of useEffectEvent](https://blog.logrocket.com/react-has-finally-solved-its-biggest-problem-useeffectevent/)
