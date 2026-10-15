# Rebalancer: Meta가 공개한 범용 할당 문제 솔버

<https://facebook.github.io/rebalancer/>

<https://github.com/facebook/rebalancer>

GN 토론: <https://news.hada.io/topic?id=35320>

## 소개

Rebalancer는 Meta가 공개한 할당 문제(assignment problem) 솔버 라이브러리다.
README는 할당 문제를 “객체를 컨테이너에 배정하는 결정”으로 정의한다.
각 객체는 정확히 하나의 컨테이너에 들어가야 하고,
그 배정은 제약(constraint)을 만족하면서 목표(goal)를 최적화해야 한다.
샤드를 호스트에 두는 일, 작업을 서버에 올리는 일,
공을 상자에 나누는 일이 모두 이 틀에 들어간다.

핵심 솔버는 C++로 작성되었고 단일 프로세스 안에서 멀티스레드로 계산한다.
README는 객체와 컨테이너가 약 100만 개 규모인 문제까지
무리 없이 다룬다고 적는다.
사용자 인터페이스는 C++와 Python 두 가지이고, 라이선스는 Apache 2.0이다.

Meta 내부에서는 하드웨어와 서버 할당, ML 학습과 추론 배치, 트래픽 라우팅,
부하 분산 마이그레이션 등 수십 개의 대규모 자원 할당 문제에 쓰였다고 한다.
설계와 알고리즘, 운영 경험은 OSDI 2024 논문
“Optimizing Resource Allocation in Hyperscale Datacenters: Scalability, Usability, and Experiences”에 정리되어 있다.

저장소는 2026년 6월 10일에 만들어졌고,
첫 릴리스 v1.0.1은 6월 14일, v1.0.4는 7월 7일에 나왔다.
2026년 10월 15일 기준 스타는 457개, 포크는 43개다.

## 동작 방식

### 문제 정의와 풀이 알고리즘의 분리

Rebalancer의 중심 설계는 문제를 어떻게
정의하는가와 어떻게 푸는가를 떼어 놓는 것이다.
사용자는 객체, 컨테이너, 차원(dimension), 제약, 목표를 선언하고,
같은 정의에 대해 풀이 알고리즘을 따로 고른다.
README가 대표로 드는 알고리즘은 두 가지다.

| 알고리즘                  | 방식                                                              | 강점                      | 약점                             |
| ------------------------- | ----------------------------------------------------------------- | ------------------------- | -------------------------------- |
| 지역 탐색(local search)   | 임의 배정에서 시작해 이동·교환을 반복하며 목표가 나아질 때만 적용 | 큰 문제로 잘 확장됨       | 전역 최적해를 보장하지 않음      |
| 최적 솔버(혼합 정수 계획) | 문제를 MIP 식으로 바꿔 외부 솔버에 맡김                           | 시간만 주면 최적해를 찾음 | 거대한 문제로는 잘 확장되지 않음 |

지역 탐색은 더 나아지는 이동을 찾지 못하거나,
사용자가 정한 이동 횟수나 시간 한도에 닿으면 멈춘다.
MIP 쪽은 오픈소스 HiGHS와 상용 솔버인 FICO Xpress, Gurobi를 지원한다.

### 미리 정의된 표현식

제약과 목표는 수식을 직접 쓰는 대신 미리 정의된 표현식을 조합해 만든다.
표현식 집합은 유한하지만 확장할 수 있다고 README는 설명한다.
대표 예시는 두 가지다.

- Balance: 어떤 차원을 컨테이너 사이에 고르게 맞춘다.
  샤드마다 CPU 사용량이 있을 때
  호스트 전체의 CPU 사용률을 최대한 비슷하게 만드는 식이다.
- Capacity: 컨테이너 안의 차원 합을 제한한다.
  호스트에 올라간 샤드들의 메모리 요구량 합이
  그 호스트의 메모리 용량을 넘지 않게 한다.

## 사용하기

### Python 예제

README의 빠른 예제는 작업 4개와 호스트 2개, 메모리 용량 제약 하나로 이루어진다.
`host0`에 작업 3개가 몰려 있고 `host1`에는 1개뿐인 상태에서 시작한다.
작업마다 메모리 10, 호스트마다 용량 20이므로 2대2 분배만 제약을 만족한다.

```bash
pip install rebalancer
```

```python
from rebalancer import ProblemSolver
from rebalancer.specs import (
    CapacitySpec, ConstraintSpec, LocalSearchSolverSpec,
    MoveTypeSpec, SingleMoveTypeSpec, SwapMoveTypeSpec, SolverSpec,
)

solver = ProblemSolver(service_name="rebalancer", service_scope="example")
(solver
    .set_object_name("task")
    .set_container_name("host")
    # 시작 배정: host0이 과부하 상태
    .set_assignment({"host0": ["task0", "task1", "task2"], "host1": ["task3"]})
    .add_object_dimension("memory", {"task0": 10, "task1": 10, "task2": 10, "task3": 10})
    # 명시하지 않은 호스트는 기본 용량 20
    .add_container_dimension("memory", {}, default_value=20.0)
    .add_constraint(ConstraintSpec(capacitySpec=CapacitySpec(
        name="memory_capacity", scope="host", dimension="memory")))
    # 지역 탐색이 쓸 이동 종류: 단일 이동과 교환
    .add_solver(SolverSpec(localSearchSolverSpec=LocalSearchSolverSpec(
        moveTypeList=[MoveTypeSpec(singleMoveTypeSpec=SingleMoveTypeSpec()),
                      MoveTypeSpec(swapMoveTypeSpec=SwapMoveTypeSpec())])))
)
solution = solver.solve()
print(solution["assignment"])
```

같은 문제를 C++ API로도 거의 같은 모양으로 쓸 수 있다.

### 설치 경로

| 경로            | 방법                                              | 비고                                 |
| --------------- | ------------------------------------------------- | ------------------------------------ |
| PyPI            | `pip install rebalancer`                          | Python에서 쓰려면 이 경로가 유일하다 |
| Debian / Ubuntu | 릴리스의 `.deb`를 `dpkg -i`로 설치                | postinstall이 `ldconfig`를 실행한다  |
| Fedora / RHEL   | 릴리스의 `.rpm`을 `rpm -i`로 설치                 |                                      |
| macOS           | 저장소의 `Formula/rebalancer.rb`를 `brew install` | Homebrew tap은 아직 준비 중이다      |
| 소스 빌드       | fbthrift와 Folly를 먼저 빌드한 뒤 CMake + Ninja   | Python 패키지는 만들어지지 않는다    |

패키지 설치 후에는 README가 제공하는 `test_solve.cpp`를 컴파일해
`PASS: 2-2 split achieved`가 나오는지로 확인할 수 있다.

### Rebalancer Explorer

Rebalancer Explorer는 솔버 실행 결과를 들여다보는 웹 UI다.
문제의 객체, 컨테이너, 제약,
목표를 탐색하고 해가 각 항목에서 몇 점을 받는지 볼 수 있다.
백엔드는 C++ Thrift 서비스이고,
앞단의 JSON 프록시가 `POST /v2/<method>` 형태의 HTTP로 바꿔 준다.
그래서 Next.js 프런트엔드는 Thrift 도구 체인 없이 동작한다.

```bash
docker compose up --build
```

저장소 루트에서 이 명령을 실행하고 `http://localhost:3000`에 접속하면 된다.
Compose는 스도쿠,
8퀸 같은 예제 번들도 공유 볼륨에 넣어 주므로 바로 둘러볼 수 있다.

## 트레이드오프

### 선형 계획법 솔버를 그냥 쓰면 되지 않는가

GN에서 heal9179는 이것이 그냥 선형 계획법 문제가 아니냐고 물었다.[^heal9179]
수학적으로는 맞는 지적이다.
배정 변수가 0 또는 1인 정수 변수이므로 엄밀히는 정수 계획 문제이고,
Rebalancer 스스로도 최적 솔버 경로에서는
문제를 MIP 식으로 바꿔 HiGHS나 Gurobi에 넘긴다.

차이는 문제를 푸는 엔진이 아니라 문제를 적는 층과 규모에 있다.
MIP 솔버를 직접 쓰면 Balance 같은 목표를
보조 변수와 선형화 기법으로 손수 풀어 써야 하고,
README가 인정하듯 그렇게 만든 식은 거대한 문제에서 잘 확장되지 않는다.
Rebalancer는 같은 선언을 지역 탐색으로도 풀 수 있게 해서,
최적성 보장을 내주고 100만 개 규모까지 가는 길을 열어 둔다.
즉 질문에 대한 답은 “그렇다, 그런데 그 식을 매번 손으로 쓰지 않게 하고,
식이 너무 커지면 다른 엔진으로 바꿀 수 있게 하는 것이 이 도구의 몫”에 가깝다.

### 지역 탐색과 최적 솔버 사이의 선택

지역 탐색은 빠르고 크게 확장되지만 결과가 국소 최적에 머물 수 있다.
README의 예제처럼 이동 종류에 교환(swap)을 함께 넣는 이유도 여기 있다.
단일 이동만으로는 용량이 꽉 찬 두 호스트 사이에서
아무것도 옮길 수 없는 상태에 갇히기 쉽다.

최적 솔버는 해의 품질을 보장하지만 시간과 문제 크기에서 대가를 치른다.
또 실무에서 쓸 만한 속도를 내는 Gurobi, FICO Xpress는 상용 라이선스가 필요하다.
같은 문제 정의로 두 엔진을 돌려 품질과 속도를
비교할 수 있다는 점이 이 선택을 실험으로 바꿔 준다.

## 함정

- Python 사용자가 소스 빌드를 하면 Python 패키지가 나오지 않는다.
  PyPI 패키지를 써야 한다.
- 소스 빌드는 fbthrift와 Folly를 먼저 빌드해야 해서 진입 비용이 크다.
- 기여할 때 새 파일을 추가하면 CMake를 다시 실행해야 한다.
  Meta 내부 빌드와 오픈소스 빌드를 동시에 맞추느라
  CMake가 디렉터리 전체를 훑어 파일을 분류하기 때문이다.
- 단일 프로세스 설계이므로 한 머신의 메모리와 코어를 넘는 문제는 쪼개서 다뤄야 한다.
- 지역 탐색 결과가 좋아 보여도 최적이라는 보장은 없다.
  작은 표본에서 MIP 결과와 비교해 격차를 재 두는 편이 안전하다.

## 기억할 원칙

### 모델링 층과 풀이 엔진을 분리하라

할당 문제는 대부분 수학적으로 이미 잘 알려진 형태다.
실무에서 어려운 부분은 풀이가 아니라 요구사항을
정확한 제약과 목표로 옮기는 일이고,
문제 크기가 바뀔 때 그 정의를 버리지 않고 엔진만 바꿀 수 있는가다.
Rebalancer의 가치는 새 알고리즘보다 이 분리를
Meta의 여러 운영 문제에서 검증했다는 데 있다.

---

[^heal9179]: <https://news.hada.io/topic?id=35320#cid67651>
