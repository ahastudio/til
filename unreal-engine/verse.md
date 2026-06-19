# Verse

## 소개

Verse는 Epic Games가 개발한 멀티패러다임 프로그래밍 언어다.
함수형, 논리형, 명령형 전통을 조합하며, 게임과 메타버스 환경을 위해 설계됐다.
현재는 UEFN(Unreal Editor for Fortnite) 안에서만 사용할 수 있으며, 포트나이트 크리에이티브 2.0의 핵심 스크립팅 언어로 실제 서비스에서 운용 중이다.

Simon Peyton Jones(Haskell 설계자), Jan Vitek, Tim Sweeney(Epic Games CEO)가 함께 설계했다.
Tim Sweeney는 2000년대 초부터 차세대 프로그래밍 언어에 관한 글을 써왔으며,
Verse는 그 수십 년간의 사유가 응축된 결과물이다.

세 가지 설계 원칙이 언어를 관통한다.

- **It's Just Code** — 특수한 문법 없이 일반 코드로 모든 것을 표현한다.
- **Just One Language** — 컴파일 타임과 런타임이 동일한 구성체를 사용한다.
- **Metaverse First** — 지속적이고 전역적인 시뮬레이션 환경을 기본 대상으로 설계됐다.

[UE6로 가는 길](road-to-ue6.md)에서 Verse가 UE6의 핵심 언어로 채택되어 C++와 Blueprints를 대체하는 맥락을 다룬다.

## 기본 문법

### 표현식 중심 언어

Verse에는 구문(statement)이 없다.
`if`, `for`, `loop` 등 모든 제어 흐름은 값을 생성하는 표현식이다.

```verse
# if 표현식 — 값을 반환한다
Result := if (X > 0) { "양수" } else { "음수 또는 0" }
```

### 변수 선언과 불변성

Verse는 기본적으로 불변(immutable)이다.
가변 변수는 `var`로 선언하고, 재대입은 `set` 키워드를 사용한다.

```verse
# 불변 바인딩
Name := "Aldric"

# 가변 변수
var Count : int = 0
set Count = Count + 1
```

`set` 표현식은 대입한 값을 반환하므로 연쇄 대입이 가능하다.

```verse
set Y = set X = 5   # X와 Y 모두 5가 됨
```

### 블록 문법

Verse는 세 가지 블록 표기를 지원한다.

```verse
# 들여쓰기 스타일 (콜론 + 4칸 들여쓰기)
if (Condition):
    DoSomething()

# 중괄호 스타일
if (Condition) { DoSomething() }

# 닷 스타일 (한 줄)
if (Condition) . DoSomething()
```

### 주석

```verse
# 한 줄 주석

<# 인라인 블록 주석 #>

<#>
    들여쓰기 블록 주석
    여러 줄 가능
    중첩 지원: <# 내부 #>
```

## 타입 시스템

### 기본 타입

| 타입         | 설명                                 |
| ------------ | ------------------------------------ |
| `int`        | 임의 정밀도 정수 (리터럴은 64비트)   |
| `rational`   | 정수 나눗셈으로 생성되는 정확한 분수 |
| `float`      | IEEE 64비트 부동소수점               |
| `logic`      | `true` / `false`                     |
| `char`       | UTF-8 코드 단위                      |
| `char32`     | 전체 유니코드 포인트                 |
| `string`     | `char` 배열                          |
| `type`       | 타입 자체를 값으로 취급하는 메타타입 |
| `any`        | 모든 타입의 수퍼타입                 |
| `void`       | 의미 있는 결과가 없음을 나타냄       |

`rational`은 표현이 달라도 값이 같으면 동등하다.
`5/2`와 `10/4`는 같은 값이다.

### 타입 추론

타입 어노테이션은 대부분 생략할 수 있다.
필요한 경우 `:` 뒤에 타입을 명시한다.

```verse
Score : int = 100
Name : string = "Aldric"
```

### 옵셔널 타입

`?T`는 값이 있거나 없는(empty) 옵셔널 타입이다.
`option{Value}`로 값을 감싸고, `?` 연산자로 언래핑한다.

```verse
MaybeScore : ?int = option{42}

if (Score := MaybeScore?):
    # Score는 여기서 int 타입
    Print(Score)
```

## 실패(Failure) 시스템

Verse의 가장 독창적인 설계 중 하나다.
예외(exception) 대신 "실패(failure)"를 제어 흐름의 핵심으로 사용한다.

### 실패 가능 표현식

표현식은 성공(값을 생성)하거나 실패(아무것도 생성하지 않음)할 수 있다.
실패 가능 함수는 `[]` 표기로 호출한다.

```verse
# 일반 호출 (항상 성공)
Result := Sqrt(9.0)

# 실패 가능 호출 (실패할 수 있음)
Value := Map[Key]     # 키가 없으면 실패
Item := Array[Index]  # 인덱스 범위 초과 시 실패
```

### 실패 문맥

실패 가능 표현식은 실패 문맥(failure context) 안에서만 실행할 수 있다.
`if` 조건부, `for` 루프, `<decides>` 효과가 붙은 함수가 실패 문맥을 형성한다.

```verse
if (Value := Map[Key]):
    # 키가 있을 때만 실행됨
    Print(Value)
```

### 논리 연산자

```verse
# and: 모두 성공해야 진행
if (A > 0 and B > 0):
    Print("둘 다 양수")

# or: 하나라도 성공하면 진행 (왼쪽부터 시도)
if (Value := Map1[Key] or Map2[Key]):
    Print(Value)

# not: 성공/실패를 반전
if (not Map[Key]):
    Print("키가 없음")
```

### 쿼리 연산자 `?`

어떤 값이든 실패 가능 표현식으로 변환한다.
`false?`는 항상 실패, 그 외 값은 항상 성공한다.

```verse
if (IsAlive?):
    Print("살아있음")
```

### 트랜잭셔널 실패

`<transacts><decides>` 효과를 가진 함수는 실패 시 그 안의 모든 상태 변경이 자동으로 롤백된다.

```verse
AttemptPurchase()<transacts><decides> : void =
    # 잔액 차감
    set Balance = Balance - Price
    # 재고 확인 — 실패하면 잔액 차감도 취소됨
    Stock := Inventory[ItemId]
    set Inventory[ItemId] = Stock - 1
```

## 함수

### 기본 정의

```verse
Add(A:int, B:int) : int =
    A + B

Greet(Name:string) : string =
    "Hello, {Name}!"
```

### 네임드 파라미터와 기본값

`?` 접두사로 네임드 파라미터를 선언한다.

```verse
CreatePlayer(?Name:string = "Player", ?Health:int = 100) : player =
    player{Name := Name, Health := Health}

# 호출 시 이름으로 지정
P := CreatePlayer(?Name := "Aldric")
```

### 람다 (중첩 함수)

`=>` 람다 문법은 현재 미지원이다.
중첩 함수로 동일한 효과를 낸다.

```verse
Apply(Value:int, Operation:(int):int) : int =
    Operation(Value)

Double := (X:int):int => X * 2   # 미지원
# 대신:
Double(X:int):int = X * 2
Result := Apply(5, Double)
```

### 확장 메서드

기존 타입(내장 타입 포함)에 메서드를 추가할 수 있다.

```verse
(Value:int).IsEven() : logic =
    Mod[Value, 2] = 0

if (42.IsEven()):
    Print("짝수")
```

### 오버로딩

동일한 이름으로 파라미터 타입이 다른 함수를 여러 개 정의할 수 있다.
타입이 완전히 구분되어야 하며, 옵셔널 타입이나 배열끼리는 오버로드할 수 없다.

```verse
Describe(X:int) : string = "정수: {X}"
Describe(X:float) : string = "실수: {X}"
Describe(X:string) : string = "문자열: {X}"
```

### 제네릭 함수

`where` 절로 타입 파라미터 제약을 표현한다.

```verse
Max(A:t, B:t) : t where t:subtype(comparable) =
    if (A >= B) { A } else { B }
```

## 제어 흐름

### if 표현식

```verse
Grade := if (Score >= 90) { "A" }
         else if (Score >= 80) { "B" }
         else { "C" }
```

조건부에서 바인딩된 변수는 `then` 분기에서만 사용할 수 있다.

### case 표현식

```verse
case (Direction):
    "North" => MoveNorth()
    "South" => MoveSouth()
    _ => Print("알 수 없는 방향")
```

닫힌 열거형에 대해 컴파일러가 완전성(exhaustiveness)을 검사한다.

### loop / break

```verse
loop:
    Input := ReadInput()
    if (Input = "quit"):
        break
    Process(Input)
```

`break`는 바텀 타입(bottom type)을 가지므로 어떤 타입 문맥에도 호환된다.

### for 표현식

```verse
# 컬렉션 순회
for (Item : Items):
    Process(Item)

# 인덱스와 값
for (Index -> Item : Items):
    Print("{Index}: {Item}")

# 필터링 (실패 가능 표현식 포함 가능)
for (Player : Players, Player.IsAlive()):
    Player.GivePoints(10)

# 범위 (for 안에서만 유효)
for (I : 1..10):
    Print(I)
```

### defer

스코프를 벗어날 때(정상 종료, 실패, 취소 모두) 실행할 코드를 예약한다.
정의 역순(LIFO)으로 실행된다.
투기적 실행(speculative execution)이 롤백될 때는 실행되지 않는다.

```verse
OpenFile(Path:string) : void =
    Handle := FileOpen(Path)
    defer { FileClose(Handle) }
    # 이후 코드 — 어떤 경로로 나가든 파일이 닫힘
    ProcessFile(Handle)
```

## 클래스와 인터페이스

### 클래스 정의

```verse
character := class:
    Name : string
    Health : int = 100

    TakeDamage(Amount:int) : void =
        set Health = Health - Amount

    IsAlive() : logic = Health > 0
```

### 인스턴스 생성 (아키타입 표현식)

```verse
Hero := character{Name := "Aldric", Health := 100}
```

### 상속

단일 상속만 지원한다.
메서드 오버라이딩에는 `<override>` 지정자를 사용한다.

```verse
hero := class(character):
    Level : int = 1

    LevelUp()<override> : void =
        set Level = Level + 1
        set Health = Health + 10

# 부모 메서드 호출
(super:character).TakeDamage(Amount)
```

### 주요 클래스 지정자

| 지정자           | 설명                                         |
| ---------------- | -------------------------------------------- |
| `<unique>`       | 동등성을 아이덴티티로 판단, 맵 키로 사용 가능 |
| `<abstract>`     | 직접 인스턴스화 불가, 서브클래스용 템플릿    |
| `<castable>`     | 런타임 타입 검사 및 다운캐스팅 허용          |
| `<final>`        | 상속 및 메서드 오버라이딩 금지               |
| `<persistable>`  | 세션 간 상태 저장·복원 가능                  |

### 인터페이스

인터페이스는 계약(contract)을 정의한다.
다중 인터페이스 구현이 가능하며 다이아몬드 상속도 지원한다.

```verse
damageable := interface:
    TakeDamage(Amount:int) : void
    IsAlive() : logic

character := class(damageable):
    Health : int = 100
    TakeDamage(Amount:int) : void = set Health = Health - Amount
    IsAlive() : logic = Health > 0
```

## 효과(Effects) 시스템

함수는 자신의 부수 효과(side effect)를 타입 서명에 명시한다.
"모든 함수는 두 가지 이야기를 한다. 타입은 데이터가 어떻게 흐르는지를, 효과는 그 과정에서 무슨 일이 일어나는지를 서술한다."

### 주요 효과 지정자

| 지정자          | 의미                                                   |
| --------------- | ------------------------------------------------------ |
| `<computes>`    | 순수 계산. 부수 효과 없음                              |
| `<transacts>`   | 기본값. 읽기·쓰기·할당 가능                            |
| `<reads>`       | 가변 상태를 관찰만 함                                  |
| `<writes>`      | 가변 상태를 변경함                                     |
| `<decides>`     | 실패할 수 있음                                         |
| `<suspends>`    | 실행이 여러 프레임에 걸쳐 일시 정지될 수 있음          |

### 서브타이핑 원칙

효과가 적은 함수를 효과가 많은 함수가 요구되는 자리에 쓸 수 있다.
순수 함수(`<computes>`)는 `<transacts>` 함수가 기대되는 모든 곳에 전달할 수 있다.

### 효과 전파

함수는 자신이 호출하는 함수의 효과를 선언해야 한다.
다만 특정 구조가 효과를 숨긴다.

- `if` — 조건부 안의 실패를 숨김
- `spawn` — 서스펜션을 숨김
- `option{}` — 실패를 옵셔널 값으로 변환

## 동시성(Concurrency)

### 구조적 동시성

Verse는 4가지 구조적 동시성 기본 요소를 제공한다.
모두 둘러싼 스코프의 생명주기에 묶인다.

```verse
# sync: 모두 완료될 때까지 대기
sync:
    LoadMap()
    LoadAssets()
    LoadPlayers()

# race: 가장 먼저 완료된 것이 승리, 나머지 취소
race:
    WaitForButton()
    Sleep(10.0)   # 타임아웃

# rush: 가장 먼저 완료된 후 계속 진행, 나머지는 백그라운드 지속
rush:
    FetchData()
    ShowLoadingScreen()

# branch: 파이어-앤드-포겟, 스코프 종료 시 자동 취소
branch:
    PlayBackgroundMusic()
```

### 비구조적 동시성

`spawn`은 독립적인 태스크를 만든다.
즉시(immediate) 함수에서도 사용 가능하다.

```verse
T := spawn { LongRunningTask() }

# 취소
T.Cancel()

# 완료 대기 (결과 캐시됨)
Result := T.Await()
```

### 타이밍

```verse
Sleep(2.0)       # 2초 일시 정지
Sleep(0.0)       # 취소 포인트만 생성 (1프레임 양보)
NextTick()       # 다음 시뮬레이션 업데이트까지 대기
```

### 이벤트

```verse
ScoreChanged : event(int) = event(int){}

# 이벤트 발신
ScoreChanged.Signal(NewScore)

# 이벤트 수신 (suspends)
Value := ScoreChanged.Await()
```

## UEFN 활용

### 게임 디바이스 연동

Verse는 UEFN의 디바이스 시스템과 통합된다.
포트나이트의 기존 크리에이티브 디바이스를 Verse 코드로 제어할 수 있다.

```verse
using { /Fortnite.com/Devices }

my_game_manager := class(creative_device):
    @editable
    TriggerDevice : trigger_device = trigger_device{}

    OnBegin<override>()<suspends> : void =
        loop:
            TriggerDevice.TriggeredEvent.Await()
            HandleTrigger()
```

### 퍼시스턴스(Persistable)

`<persistable>` 클래스는 세션 간에 상태를 저장하고 복원할 수 있다.
`weak_map` 스토리지를 통해 플레이어별 데이터를 유지한다.

```verse
player_data := class<persistable><final>:
    Score : int = 0
    Level : int = 1
```

## 분석

### 실패 시스템은 언어 전반을 통합하는 핵심 추상화다

Verse의 실패 시스템은 표면적으로 에러 처리처럼 보이지만, 실제로는 언어 전반을 관통하는 단일 추상화다.
`if` 조건부의 분기, `for` 루프의 필터링, 타입 캐스팅의 성공/실패, 트랜잭션의 롤백이
모두 같은 메커니즘 위에 성립한다.

Lobste.rs에서 steinuil은 이를 정확히 파악했다.
"표현식이 하나의 값이 아닌 0개 이상의 (순서 있는) 값을 나타낸다"는 것이 핵심이다.
`x := (0|1|2)`는 x가 0, 1, 2가 되는 분기를 만들며, 이 분기들은 병렬로 실행될 수 있다.
그리고 타입도 이 개념의 연장선이다.
타입은 "해당 타입에 속하지 않는 값에 대해 실패하는 함수"이므로, 의존 타입(dependent typing)이 자연스럽게 성립한다.

justinpombrio는 이 개념이 새로운 것이 아니라고 지적했다.[^justinpombrio-ndt83j]
SICP의 `amb`(ambiguous operator)가 같은 아이디어이며, 오래전부터 알려져 있었지만 어떤 주류 언어에도 채택된 적이 없었다는 것이다.
Verse는 수십 년간 학술 연구에 머물던 이 개념을 실제 운영 환경에 올린 첫 사례에 해당한다.

### 효과 시스템은 트랜잭셔널 의미론의 토대다

Verse의 효과 시스템은 단순한 어노테이션이 아니다.
`<transacts>` 효과는 소프트웨어 트랜잭셔널 메모리(STM) 위에서 동작하며,
이것이 "실패 시 자동 롤백"을 가능하게 하는 기반이다.

david_chisnall은 게임 엔진과의 적합성을 정확하게 분석했다.
게임 엔진의 프레임 루프는 "이전 세계 상태를 받아 새 세계 상태와 프레임을 반환하는 순수 함수"로 볼 수 있다.
프레임이 화면에 출력되면 그 상태는 커밋되고, 그 이전에는 모든 것이 롤백 가능하다.
Verse의 효과 + STM 모델은 이 구조에 자연스럽게 맞아 들어간다.

### 자동 스케일링이 메타버스 설계의 근본 목표다

puffnfresh는 Verse의 핵심 동기를 명확히 제시했다.
"모든 변수가 STM이고, 효과가 롤백 가능 여부로 분류되므로, Epic Games는 Verse 코드를 마음 놓고 실행하고 접속하는 플레이어 수에 맞게 자동으로 스케일링할 수 있다."

이것은 단순한 스크립팅 언어 설계가 아니다.
언어 자체가 인프라 확장성을 보장하는 수단이 된다.

## 비평

### UEFN에 갇혀 있다는 점이 언어 발전을 가로막는다

mjn이 지적했듯, Verse는 현재 UEFN 안에서만 사용할 수 있고, 일반 Unreal Engine에서도 쓸 수 없다.
게임 회사가 저명한 PL 연구자들을 채용해 새 언어를 만든다는 것 자체가 이례적인 일이고,
포트나이트의 사용자 기반이 그 재정적 근거를 제공한다는 점을 이해할 수 있다.

그러나 이 제약은 언어 연구 공동체의 접근을 차단한다.
dmytrish가 언급했듯 Mercury, Curry 같은 논리형 언어와의 비교 연구조차 어렵다.
fanf는 단, Verse Calculus 논문 자체에 이미 Curry와의 비교가 여러 곳에 담겨 있다고 보충했다.[^fanf]
오픈소스 레퍼런스 구현이 공개 로드맵에 있다가 사라졌고(puffnfresh), 채용 공고만 있었다는 사실은 상황이 불투명함을 보여준다.

접근 제약은 언어 자체의 완성도에도 영향을 미친다.
steinuil은 Book of Verse에서 "choices"—표현식이 0개 이상의 값을 나타낸다는 언어의 핵심 개념—가 빠져 있다는 점을 발견했다.[^steinuil-gnnnni]
rpjohnst는 그 이유를 설명했다. choices는 아직 Unreal Engine 구현에 포함되지 않았으며, 문서는 구현이 완료된 기능만을 반영하기 때문이다.[^rpjohnst-4hyk8u]
언어의 설계 철학에서 가장 근본적인 개념이 구현 대기 상태라는 사실은, Book of Verse를 읽을 때 문서가 언어의 현재 능력이 아닌 방향을 기술한 것임을 염두에 둬야 함을 의미한다.

독립적인 도구 체인의 부재도 진입 장벽을 높인다.
epolanski는 "REPL도 인터프리터도 독립 컴파일러도 없고, UEFN 외부에서는 언어를 전혀 테스트할 수 없다는 말인가?"라고 물었다.[^epolanski-35272648]
MattRix는 "현재는 그렇지만 REPL과 오픈소스 릴리스 계획이 있고, 초기 단계에서는 단일 사용 사례에 집중하고 있다"고 답했다.[^mattrix-35273227]

### "자동 롤백"은 I/O 경계에서 한계를 가진다

steinuil은 트랜잭셔널 의미론의 실제 제약을 명확히 짚었다.
투기적 실행은 롤백을 지원하는 I/O 백엔드에 의존한다.
포트나이트 서버는 이를 위해 설계됐지만, 파일시스템 쓰기나 네트워크 호출에는 적용되지 않는다.
Verse는 트랜잭셔널 연산을 위한 인체공학적 프레임워크를 제공하지만, 그 연산이 실제로 롤백 가능하려면 하부 시스템이 이를 지원해야 한다.

rpjohnst는 포트나이트 서버 측 구현의 구체적 내용을 담은 Unreal Engine 기술 블로그를 제시했다.[^rpjohnst]
Epic이 C++ 런타임에 STM 의미론을 어떻게 이식했는지를 다루며, "자동 롤백"이 언어 추상화만의 산물이 아니라 서버 인프라와 긴밀히 결합된 결과임을 보여준다.

Microsoft Research의 STM.NET이 트랜잭셔널 NTFS까지 시도하다 결국 실용성 한계에 부딪혔다는 선례도 있다.

### 학습 진입 장벽과 실전 투입 가능성 사이의 간극

Verse는 프로그래밍 경험이 없는 사람도 UEFN에서 시작할 수 있도록 설계됐다.
그러나 언어의 진짜 힘인 효과 시스템, 트랜잭셔널 의미론, 실패 기반 제어 흐름은
함수형 프로그래밍과 타입 이론에 익숙하지 않은 개발자에게는 낯선 개념이다.
입문 자료와 실제 언어의 깊이 사이에 큰 간극이 존재한다.

### `logic` 타입 명명은 관례와의 단절을 초래한다

mdaniel은 Verse가 불리언 타입을 `boolean` 대신 `logic`으로 명명한 결정을 비판했다.[^mdaniel-35277144]
`boolean`은 수십 년에 걸쳐 정착된 용어이며, 이를 교체하면 기존 언어 사용자에게 불필요한 인지 부담을 준다는 것이다.
블록 문법에서 들여쓰기 스타일과 중괄호 스타일을 모두 허용하는 것과 함께, 친숙한 용어를 의도적으로 피하는 설계 결정들이 학습 곡선을 가파르게 만든다.

## 인사이트

### Verse는 게임 개발에서 검증된 PL 이론의 실용화 실험이다

puffnfresh는 Tim Sweeney가 2000년부터 프로그래밍 언어를 연구해왔음을 상기시켰다.
Verse는 Simon Peyton Jones(Haskell), Jan Vitek(JVM 성능 연구)이 참여한 프로젝트이며,
학술적으로 엄밀한 Verse 미적분학(Verse Calculus) 논문이 선행했다.

이 조합은 드물다.
게임 회사가 유명 PL 연구자를 채용하고, 수억 명 사용자의 플랫폼에서 새 언어를 운용하는 것은
언어 설계 이론을 실제 규모에서 검증하는 거의 유일한 사례다.
Haskell이 산업 현장에서 영향력을 확장한 것처럼, Verse의 아이디어들이 미래 언어들에 흡수될 수 있다.

justinpombrio는 Verse가 UEFN 밖에서 사용 불가능하더라도 언어 설계 자체를 읽을 가치가 있다고 주장했다.[^justinpombrio-8gxskn]
fallibility, structured concurrency, live variables, effect markers는 각각 독립적으로 다른 언어 설계에 영향을 줄 수 있는 아이디어들이며, Verse를 직접 쓰지 않더라도 이 개념들을 공부하는 것이 의미 있다는 것이다.

calvin은 Sweeney의 선견지명이 Verse 이전에도 드러난 적이 있다고 지적했다.[^calvin]
1995년 Unreal 개발 당시 그가 남긴 내부 노트에는 DirectX 콘솔, 온라인 게임 유통, 소프트웨어 배포 방식의 변화 등이 예측되어 있었다.
Unreal 1이 동시대 경쟁 제품 대비 낮은 하드웨어 요구 사양에서도 더 좋은 비주얼을 구현한 것처럼, Sweeney의 공학적 판단은 일관되게 시대를 앞섰다는 것이다.

### 프로그래밍 언어가 인프라 확장성을 보장할 수 있다

REST API, 마이크로서비스, 데이터베이스 샤딩은 모두 확장성을 위한 아키텍처적 선택이다.
Verse는 다른 접근을 시도한다.
언어 설계 자체에 STM과 효과 추적을 내장함으로써, 런타임이 코드의 분산 실행과 롤백을 자동으로 처리하게 한다.

amw-zero와 andyferris의 토론에서 이 함의가 드러났다.
"왜 기본 CRUD 앱에 두 개 이상의 언어가 필요한가?"
Verse의 방향은 "언어가 트랜잭셔널 의미론을 이해하면 별도의 데이터베이스 계층이 필요 없을 수 있다"는 가능성을 탐구한다.
이것이 현실화될 경우, 웹 백엔드 개발의 구조 자체가 바뀔 수 있다.

### 동시성은 컬러드 함수 문제를 효과 추적으로 우회한다

4ad는 Verse가 "컬러드 함수(colored functions) 없이 동시성 모델을 갖는다"고 평가했다.[^4ad-35272329]
이는 Bob Nystrom의 에세이 "What Color is Your Function?"에서 비판된 async/await의 전염성 문제를 지칭한다.
async/await 방식에서는 비동기 함수를 호출하는 모든 함수 역시 비동기가 되어야 하는 색 전파(color propagation) 문제가 발생한다.
Verse에서는 `<suspends>` 효과와 구조적 동시성 기본 요소(`sync`, `race`, `rush`, `branch`)가 비동기성을 효과 수준에서 추적하기 때문에, 호출자가 반드시 같은 효과를 전파받을 필요가 없다.

4ad는 또한 Verse의 효과 지정자가 일반적인 효과 시스템과 반대 방향으로 작동한다고 분석했다.[^4ad-35273332]
일반적인 효과 타입은 "이 함수는 X를 할 수 있다"고 선언하지만, Verse의 지정자는 "이 함수는 X를 하지 않는다"는 부정(negation)을 표현한다.
`<computes>`는 부수 효과가 없음을, `<reads>`는 쓰기 효과가 없음을 나타내는 식이다.
이 관점에서 Verse의 효과 시스템은 가능성이 아닌 제약을 명시하는 부정 타입(negative type)에 가깝다고 볼 수 있다.

### 실패 시스템은 타입 시스템, 에러 처리, 동시성을 단일 추상화로 통합한다

기존 언어들은 이 세 가지를 별도로 처리한다.
Null 안전성은 타입 시스템에서, 에러는 예외나 Result 타입으로, 동시성은 async/await나 채널로 다룬다.
Verse의 "0개 이상의 값" 추상화는 이 세 가지를 하나의 메커니즘으로 통합한다.

표현식이 실패하면 — 배열 인덱스 범위 초과든, 타입 캐스팅 실패든, 조건 불충족이든 — 모두 같은 방식으로 처리된다.
이 단일성은 코드의 합성 가능성(composability)을 높이고, 언어 전체의 인지 부담을 줄인다.
steinuil이 말했듯, 이 개념을 익히면 "하나의 값을 다루는 것과 값의 시퀀스를 다루는 것이 완전히 동일하게 보인다."

## 참고 자료

### 공식 문서

| 자료 | 설명 |
| --- | --- |
| [Verse 시작하기 (한국어)](https://dev.epicgames.com/documentation/fortnite/verse-language-get-started-in-unreal-editor-for-fortnite?lang=ko) | UEFN에서 Verse를 처음 시작하는 온보딩 가이드 (한국어) |
| [Verse 시작하기 (영어)](https://dev.epicgames.com/documentation/fortnite/verse-language-get-started-in-unreal-editor-for-fortnite) | 동일 가이드 영어 원문. 학습 경로와 자료 링크 포함 |
| [Book of Verse Reference](https://dev.epicgames.com/documentation/fortnite/verse-language-book-of-verse-reference) | Epic 공식 레퍼런스 랜딩 페이지. Book of Verse GitHub 저장소로 연결 |
| [Book of Verse](https://verselang.github.io/book/) | 언어 철학·타입 시스템·효과·동시성 등을 다루는 심화 명세서. `main` 브랜치 최신 내용을 반영하며 미출시 기능도 포함될 수 있음 |

### 토론

- [Lobste.rs: Verse language](https://lobste.rs/s/jiii0u/verse_language) — Simon Peyton Jones·Jan Vitek의 발표를 본 PL 연구자들의 기술적 토론. STM, 투기적 실행, Curry·Mercury와의 비교 등 언어 설계 관점의 깊은 논의가 담겨 있다.
- [Lobste.rs: Book of Verse](https://lobste.rs/s/ffpbht/book_of_verse) — Book of Verse 문서가 공개된 시점의 토론. choices 개념 미구현 현황, SICP `amb`와의 관계, "메타버스"라는 단어의 용법 등을 다룬다.
- [HN: Epic's Verse Programming Language](https://news.ycombinator.com/item?id=35270720) (117점, 59개 댓글) — 효과의 부정 타입 해석, REPL 부재 비판, `logic` 타입 명명 논란 등 언어 설계 관련 토론을 담고 있다.

---

[^rpjohnst]: <https://lobste.rs/s/jiii0u/verse_language#efytxd>
[^fanf]: <https://lobste.rs/s/jiii0u/verse_language#9p0tos>
[^calvin]: <https://lobste.rs/s/jiii0u/verse_language#vgjlbi>
[^justinpombrio-ndt83j]: <https://lobste.rs/s/ffpbht/book_of_verse#ndt83j>
[^steinuil-gnnnni]: <https://lobste.rs/s/ffpbht/book_of_verse#gnnnni>
[^rpjohnst-4hyk8u]: <https://lobste.rs/s/ffpbht/book_of_verse#4hyk8u>
[^justinpombrio-8gxskn]: <https://lobste.rs/s/ffpbht/book_of_verse#8gxskn>
[^4ad-35272329]: <https://news.ycombinator.com/item?id=35272329>
[^4ad-35273332]: <https://news.ycombinator.com/item?id=35273332>
[^epolanski-35272648]: <https://news.ycombinator.com/item?id=35272648>
[^mattrix-35273227]: <https://news.ycombinator.com/item?id=35273227>
[^mdaniel-35277144]: <https://news.ycombinator.com/item?id=35277144>
