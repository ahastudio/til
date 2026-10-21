# 던전 구간 사이 길을 막힌 통로로 만든 리팩터링: 테스트 안의 코드를 메서드로 옮기는 과정

원문: [Refactoring = Learning](https://ronjeffries.com/articles/-v026/o/y/)

## 요약

Ron Jeffries가 2026년 9월 17일에 올린 글로,
Python으로 던전 지도를 만드는 연재의 한 편이다.
구간(suite)과 구간 사이에 길을 놓는 일을 테스트 안에서 먼저 풀고,
그 코드를 `DungeonLayout`의 메서드로 옮기는 과정을 보여 준다.

바뀐 것은 세 가지다.
첫째, 두 구간을 잇는 테스트가 `make_passages`를 부르던 것을
확장된 경로(`find_extended_path`)의 첫 두 칸과
마지막 두 칸에 통로를 직접 놓는 방식으로 바꿨다.
둘째, 그 길을 통과할 수 없게 만드는 `Passages.isolate`를 새로 만들고,
`create_passage`가 두 방 중 하나라도 격리되어 있으면
통로를 만들지 않고 `False`를 돌려주게 했다.
셋째, 테스트에서 하던 일이 `DungeonLayout` 쪽 코드 같아 보여
`add_isolated_path(s1, s2)`로 추출하고,
같은 시드로 두 테스트를 돌려 결과를 비교하게 했다.
마지막으로 실제 던전 생성 함수에서 이 메서드를 써서
구간 네 개와 보스 구간을 격리된 길로 이었고,
저자는 지도가 보기 좋다고 평가한다.

글 끝에서 저자는 이전 방들을 저장해 두었다가
새 방들만 모아 구간을 만드는 반복 패턴을
함수로 묶을 만하다고 말한다.
던전 레이아웃이 많아지면 구성을 정리할 방법도 필요하다고 덧붙인다.
이 글은 연재의 한 토막이라 앞의 글을 읽지 않으면 일부 이름(`Suite`,
`Room`, `YieldStepper`)의 뜻을 알 수 없다.
앞선 글 Paths Between Suites?에서
길을 통과할 수 없게 표시한다는 계획을 먼저 적었다.[^prev]

## 무엇이 어떻게 바뀌었나

### 테스트의 두 단계

이전 테스트는 확장된 경로의 가운데 칸들로 새 방 `path_room_1_2`를 만들고
`make_passages`를 불렀다.
저자의 설명으로 `make_passages`는 마법이 많이 들어 있는 큰 호출이다.
이 경우에는 필요한 것이 더 정확히 알려져 있으므로 그 일만 하기로 했다.
새 방과 양 끝 방 사이 통로 두 개를 `add_passage_unconditionally`로 직접 놓고,
`isolate`로 새 방을 격리한다.

```python
layout.clear_subregions()
path_cells = suite_1.find_extended_path(suite_2)
path_room_1_2 = Room(path_cells[1:-1])
layout.add_room(path_room_1_2)
layout.passages.add_passage_unconditionally((path_cells[0], path_cells[1]))
layout.passages.add_passage_unconditionally((path_cells[-1], path_cells[-2]))
layout.passages.isolate(path_room_1_2)
```

### 격리의 구현

`Passages`에 `isolated: set[Room]`이 생기고,
`create_passage`의 앞 두 줄이 추가됐다.
격리된 방이 끼면 `False`, 이미 연결된 방이면 `False`,
아니면 함수를 불러 통로를 만든다.
무조건 추가하는 메서드는 격리를 검사하지 않으므로,
격리된 길의 양 끝 통로를 놓을 때도 그대로 쓸 수 있다.

### 추출과 새 테스트

테스트에서
하던 여섯 줄이 레이아웃 소관이라는 판단으로
`DungeonLayout.add_isolated_path`가 생겼다.
같은 일을 하는 새 테스트는 이 메서드를 부르고,
확인에 필요한 만큼만 `find_extended_path`를 따로 불러 양 끝을 검사한다.
저자는 둘이 같은 경로를 쓰도록 두 테스트에서 같은 시드(14159)를 쓴다.

## 직접 돌려 보기

글의 `Passages` 전체 코드는 나오지 않는다.
`rooms_are_connected`와 `add_passage_unconditionally`의 본문이 빠져 있어서,
아래 코드는 이 문서가 최소한으로 다시 만든 것이고 글의 원본이 아니다.
격리된 방이 새 연결을 거절하고,
무조건 추가는 이를 우회한다는 두 가지만 확인한다.

```python
import random


class Room:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Passages:
    def __init__(self):
        self.room_connections = set()
        self.isolated = set()

    def rooms_are_connected(self, r1, r2):
        return (r1, r2) in self.room_connections or (r2, r1) in self.room_connections

    def add_passage_unconditionally(self, r1, r2):
        self.room_connections.add((r1, r2))

    def isolate(self, room):
        self.isolated.add(room)

    def create_passage(self, r1, r2, func):
        if r1 in self.isolated or r2 in self.isolated:
            return False
        elif self.rooms_are_connected(r1, r2):
            return False
        else:
            func()
            self.add_passage_unconditionally(r1, r2)
            return True


a, b, path = Room("A"), Room("B"), Room("path")
p = Passages()
p.isolate(path)
p.add_passage_unconditionally(a, path)       # 무조건 추가는 격리를 우회한다
p.add_passage_unconditionally(path, b)
print("격리된 방에 연결 시도:", p.create_passage(a, path, lambda: None))
q = Passages()
print("첫 연결:", q.create_passage(a, b, lambda: None),
      "/ 두 번째:", q.create_passage(a, b, lambda: None))
```

실행하면 `격리된 방에 연결 시도: False`,
`첫 연결: True / 두 번째: False`가 나온다.
이 출력은 이 문서가 직접 실행해 확인했다.

## 비평

### 반환값 하나가 두 가지 이유를 섞는다

`create_passage`는 격리된 방이어서 거절될 때와 이미 연결되어 있어서
거절될 때 똑같이 `False`를 돌려준다.
호출하는 쪽은 왜 안 됐는지 알 수 없다.
글의 용도에서는 둘 다 연결하지 않는다는 점이 같아 문제가 없지만,
나중에 격리된 방에 연결을 시도하는 것이 버그인 경우를 잡으려면
이유를 구분해야 한다.
이는 이 문서의 지적이고 저자가 다룬 문제는 아니다.

### 같은 시드로 두 번 부르면 같은 경로가 나온다는 보장이 약하다

글은 가장 가까운 칸 쌍이 여럿이면 경로의 시작과 끝이 무작위라고 설명한다.
새 테스트는 시드를 한 번만 주고 `find_extended_path`를 한 번 부른 뒤
`add_isolated_path`가 같은 함수를 다시 부른다.
테스트 주석은 지금 `find_closest_pair`가 결정적이라서 통한다고 적는다.
그 말이 맞다면 시드는 필요하지 않고, 무작위가 실제로 들어 있다면
시드만으로는 두 번의 호출이 같은 결과를 내지 않는다.
이 문서가 `random.choice` 하나로 만든 장난감으로 확인해 보니,
시드를 한 번 주고 두 번 부르면 4와 0이 나왔고
호출마다 시드를 주면 4와 4가 나왔다.
따라서 시드는 결정성이 깨지는 날을 위한 보험처럼 보이지만
그 보험은 두 번째 호출에는 듣지 않는다.
글의 실제 코드를 열어 보지는 못해서 실제 함수의 동작은 확인하지 못했다.

### 추출한 메서드의 위치 판단이 한 문장에 기댄다

여섯 줄이 `DungeonLayout`에 속한다는 판단은 코드가 그렇게 보인다는 한 문장이다.
메서드는 두 구간을 받아 방과 통로와 격리를 모두 레이아웃에 쓰는데,
이 구성은 `Suite` 쪽에 경로 찾기가,
`Passages` 쪽에 격리가 나뉘어 있는 구조를 `DungeonLayout`이 이어 붙이는 것이다.
그래서 이 메서드는 세 객체를 모두 아는 조율자가 된다.
작은 프로젝트에서는 문제가 아니지만
던전 유형이 늘면 이 조율자가 비대해질 수 있다.
이는 이 문서의 우려이고 저자가 한 말은 아니다.

## 인사이트

### 테스트 안에서 풀고 나서 옮기는 순서가 특성 테스트를 남긴다

저자는 먼저 테스트 안에서 방법을 풀고, 그 줄들이 굳으면 메서드로 추출하고,
추출한 뒤에도 원래 테스트가 확인하던 세부를 새 테스트에서 일부러 남겼다.
추출하면서 사라지기 쉬운 것은 중간 값을 들여다보던 단언이다.
`path_cells[0].has_passage(path_cells[1])` 같은 단언이 남았기 때문에
메서드 안의 구현이 바뀌어도 양 끝에 통로가 있다는 사실은 계속 확인된다.
이는 추출 리팩터링에서 보통 놓치는 부분이고 이 글이 실제로 보여 주는 가치다.

### 불변식을 플래그 하나로 두면 쓰는 쪽 모두가 그 규칙을 알아야 한다

`isolated`는 `Passages` 안의 집합이고
규칙은 `create_passage`의 앞 두 줄에만 있다.
무조건 추가하는 메서드는 이 규칙을 지나친다.
격리된 길의 양 끝 통로를 놓으려면 이 우회가 필요하므로 설계의 의도이기도 하다.
그러나 이는 같은 객체에 규칙을 지키는 경로와 어기는 경로가 함께 있다는 뜻이고,
어느 경로를 쓸지 호출하는 쪽이 정해야 한다.
격리가 구조(별도 타입)가 아니라 이름 붙은 상태에 있으므로
새 호출자가 규칙을 잊으면 컴파일러도 테스트도 막아 주지 않을 수 있다.
이는 이 문서의 해석이다.

### 반복되는 방 모으기 패턴은 문맥 관리자로 묶을 수 있다

저자가 글 끝에서 언급한,
이전 방들을 저장하고 새 방들만 모아 구간으로 만드는 패턴은
시작 시점의 방 집합과 끝 시점의 방 집합의 차이를 구간으로 삼는 것이다.
이는 파이썬의 `with` 블록으로 자연스럽게 감쌀 수 있는 모양이다.
다만 이 문서는 글의 코드를 갖고 있지 않아 실제로 어떻게 묶일지는 말할 수 없다.
저자는 다음 글에서 이를 다루겠다고만 한다.
연재의 다음 편을 읽어야 이 패턴이 어떻게 정리되는지 알 수 있다.

---

[^prev]: ronjeffries.com, [Paths Between Suites?](https://ronjeffries.com/articles/-v026/o/z/)
