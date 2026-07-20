# MobX

<https://mobx.js.org/>

<https://github.com/mobxjs/mobx>

## 소개

MobX는 신호(signal) 기반의 상태 관리 라이브러리로,
투명한 함수형 반응형 프로그래밍(TFRP)을 통해 상태 관리를 단순하고 확장 가능하게 만든다.
핵심 철학은 "애플리케이션 상태에서 파생될 수 있는 것은 모두 자동으로 파생되어야 한다"는 것이다.

세 가지 설계 원칙이 있다.

- **간결함**: 보일러플레이트 없이 의도를 명확히 표현한다.
  일반 JavaScript 할당으로 필드를 수정하면 반응성 시스템이 변화를 자동으로 감지하고 전파한다.
- **최적 렌더링**: 런타임에 모든 데이터 변경과 사용을 추적해 의존성 트리를 구성한다.
  React 컴포넌트는 실제로 의존하는 상태가 바뀔 때만 재렌더링된다.
- **아키텍처 자유도**: UI 프레임워크 외부에서 상태를 관리할 수 있어 코드 결합도가 낮다.

## 설치

```bash
npm install mobx
```

React와 함께 쓸 때는 바인딩 패키지를 추가로 설치한다.

```bash
# 함수형 컴포넌트 전용 (권장)
npm install mobx-react-lite

# 클래스 컴포넌트도 지원
npm install mobx-react
```

## 핵심 개념

MobX는 애플리케이션을 세 가지로 구분한다.

### State (상태)

관찰 가능한 상태를 정의한다.
평문 객체, 배열, 클래스 등 어떤 데이터 구조든 사용할 수 있다.

### Actions (액션)

상태를 변경하는 코드다.
사용자 이벤트, 서버 응답, 예약된 작업 등이 해당한다.

### Derivations (파생값)

상태로부터 자동으로 계산되는 값과 부수 효과다.
계산된 값(`computed`)과 반응(`reaction`)으로 나뉜다.

## Observable 상태 정의

### makeObservable

각 멤버에 주석을 명시적으로 지정한다.
클래스에서 주로 사용한다.

```javascript
import { makeObservable, observable, computed, action } from "mobx"

class TodoStore {
    todos = []

    constructor() {
        makeObservable(this, {
            todos: observable,
            unfinishedCount: computed,
            addTodo: action,
        })
    }

    get unfinishedCount() {
        return this.todos.filter(todo => !todo.finished).length
    }

    addTodo(title) {
        this.todos.push({ title, finished: false })
    }
}
```

### makeAutoObservable

모든 속성을 자동으로 추론한다.
상속이 없는 클래스나 팩토리 함수에 적합하다.

```javascript
import { makeAutoObservable } from "mobx"

function createTimer() {
    return makeAutoObservable({
        secondsPassed: 0,
        increase() {
            this.secondsPassed += 1
        },
        reset() {
            this.secondsPassed = 0
        },
    })
}
```

### observable()

객체를 복제해 모든 멤버를 observable로 변환한다.
Proxy를 생성하므로 동적 속성 추가가 가능하다.

```javascript
import { observable } from "mobx"

const todos = observable([
    { title: "Make coffee", finished: false },
])
```

## React 연동

`observer`로 컴포넌트를 감싸면 반응형 컴포넌트가 된다.
의존하는 observable이 변경될 때만 자동으로 재렌더링한다.

```javascript
import React from "react"
import { makeAutoObservable } from "mobx"
import { observer } from "mobx-react-lite"

const timer = makeAutoObservable({
    secondsPassed: 0,
    increase() {
        this.secondsPassed += 1
    },
    reset() {
        this.secondsPassed = 0
    },
})

const TimerView = observer(({ timer }) => (
    <button onClick={() => timer.reset()}>
        Seconds passed: {timer.secondsPassed}
    </button>
))

setInterval(() => timer.increase(), 1000)
```

## 주요 주석(Annotations)

| 주석         | 설명                                    |
| ------------ | --------------------------------------- |
| `observable` | 상태를 저장하는 추적 가능한 필드        |
| `action`     | 상태를 수정하는 메서드                  |
| `computed`   | 상태에서 파생된 값 (결과를 캐싱)        |
| `autorun`    | 의존 observable 변경 시 자동 실행       |
| `reaction`   | 특정 데이터 변경에만 반응하는 부수 효과 |
| `when`       | 조건이 참이 되면 한 번만 실행           |

## 데코레이터

MobX 6 이상에서는 Stage 3 데코레이터 문법을 지원한다.
`makeObservable` / `makeAutoObservable` 호출이 불필요해진다.

### Babel 설정

```json
{
    "plugins": [
        ["@babel/plugin-proposal-decorators", { "version": "2023-05" }]
    ]
}
```

### TypeScript 설정

`tsconfig.json`에서 레거시 플래그를 비활성화한다.

```json
{
    "compilerOptions": {
        "experimentalDecorators": false
    }
}
```

레거시 데코레이터(`experimentalDecorators: true`)는 MobX 7에서 제거될 예정이다.

## 데이터 흐름

MobX의 단방향 데이터 흐름은 다음과 같다.

```text
Action → Observable State → Computed Values → Reactions (UI 렌더링 등)
```

이벤트가 액션을 호출하고, 액션이 observable 상태를 변경하면,
해당 상태에 의존하는 computed 값과 reaction이 자동으로 업데이트된다.
