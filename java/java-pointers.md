# Java에 포인터가 있나요: 농담 하나로 읽는 최신 Java의 저수준 메모리 API

트윗: [2016 년，应届生 Java 面试… 这十年，到底发生了些什么啊](https://twitter.com/__soragoto__/status/2099744219627995375)

## 원문 번역

空言(@__soragoto__)이 2026년 9월 15일에 올린 중국어 트윗이다.
확인 시점 조회수 48만 회, 좋아요 1,600회, 리포스트 140회, 답글 63개다.

> 2016년, 신입 Java 면접:
>
> 면접관: Java에 포인터가 있나요?
> 후보자: 없습니다.
> 면접관: 자네는 Java를 완전히 이해했군. 내일부터 출근하게.
>
> 2026년, 신입 Java 면접:
>
> 면접관: Java에 포인터가 있나요?
> 후보자: 원하시면 `Unsafe`로 하나 손수 만들어 드릴 수 있습니다.
> 면접관: 그런 뜻이 아니라…
> 후보자: 아, 스마트 포인터를 원하시는 거군요. 그건 시간을 좀 더 주셔야 합니다.
> 면접관: 그런 뜻이 아니라니까요.
> 후보자: 아아아 무슨 말씀인지 알겠습니다.
> `unsafe`의 그 연산들이 높은 버전 JDK에서 전부 폐기 표시가 돼서
> 너무 지저분하다고 여기시는 거죠?
> 그럼 JNI로 쓰겠습니다. 아니면 버전을 좀 올리시든가요. FFM도 됩니다.
> 면접관: ……
>
> 이 10년 동안, 대체 무슨 일이 있었던 걸까.

저자는 이어진 트윗에서 지인의 제보에서 영감을 받아
실제 사건을 각색한 것이라고 덧붙인다.
요즘 신입은 정말 이 정도 실력이 된다는 것이다.
한 답글은 2026년의 면접관이 곧 2016년의 후보자라고 적었다.

후보자가 던지는 용어는 모두 실재한다.
`Unsafe`, 스마트 포인터, JNI, FFM, 그리고 폐기 표시까지
하나하나가 지난 10년 Java의 실제 변화를 가리킨다.
아래에서 그 용어들을 순서대로 풀어 본다.

## 2016년의 답이 맞았던 이유

Java에 포인터가 없다는 말은 정확히는
포인터를 프로그래머가 직접 다루지 않는다는 뜻이다.
객체 변수는 힙의 객체를 가리키는 참조(reference)를 담지만,
그 참조의 수치값을 읽을 수도, 거기에 산술 연산을 할 수도,
임의의 주소를 만들어 역참조할 수도 없다.

이 제약이 Java의 정체성을 만들었다.
포인터 산술이 없으니 버퍼 오버런으로 남의 메모리를 덮어쓸 수 없고,
`free`가 없으니 해제 후 사용(use-after-free)이 없으며,
주소를 위조할 수 없으니 타입 시스템을 우회할 수 없다.
메모리 안전(memory-safe) 언어라는 분류가 여기서 나온다.

2016년의 면접관이 원한 답은 이것이었다.
그리고 그 답은 지금도 언어 명세 수준에서는 여전히 맞다.

## `sun.misc.Unsafe`: 존재했지만 없는 셈이던 뒷문

문제는 명세가 금지한 일을 JDK 내부 클래스 하나가 전부 할 수 있었다는 것이다.
`sun.misc.Unsafe`는 이름 그대로 안전하지 않은 연산을 모아 둔 클래스로,
공식 API가 아니면서도 사실상 모든 곳에서 쓰였다.

무엇을 할 수 있었는지 보면 왜 포인터라 불렸는지 알 수 있다.

| 연산 종류      | 대표 메서드                                 | 하는 일                             |
| -------------- | ------------------------------------------- | ----------------------------------- |
| 오프힙 할당    | `allocateMemory`, `freeMemory`              | GC 바깥의 메모리를 직접 잡고 푼다   |
| 주소 직접 접근 | `getLong(long)`, `putLong(long, long)`      | 임의 주소를 읽고 쓴다               |
| 필드 오프셋    | `objectFieldOffset`, `arrayBaseOffset`      | 객체 내부 필드 위치를 수치로 얻는다 |
| 원자 연산      | `compareAndSwapInt`, `compareAndSwapObject` | CAS를 직접 호출한다                 |

`allocateMemory`가 돌려주는 것은 `long` 타입의 주소값이고,
`getLong(address + offset)`으로 그 주소를 역참조한다.
이름만 `long`일 뿐 이것은 포인터이며, 포인터 산술도 그냥 덧셈으로 된다.
후보자가 손수 만들어 드리겠다고 한 것이 정확히 이 이야기다.

왜 다들 썼는가 하면 대안이 없었기 때문이다.
Netty는 오프힙 버퍼를, Cassandra와 Hazelcast는 GC를 피한 대용량 캐시를,
수많은 직렬화 라이브러리는 필드 오프셋 직접 접근을 이것으로 구현했다.
JDK 자신도 `java.util.concurrent`의 원자 클래스를 이 위에 올렸다.

대가는 안전망이 전혀 없다는 것이었다.
주소를 잘못 계산하면 JVM이 그 자리에서 죽는다.
예외가 아니라 프로세스 종료이며, 스택 트레이스도 남지 않는다.
해제한 메모리를 다시 읽어도 막아 주는 장치가 없다.
Java가 없앴다던 실패 양식이 이 클래스를 통해 전부 되돌아온다.

## `VarHandle`: 온힙 접근의 공식 대체재

`Unsafe`가 하던 일은 크게 둘로 나뉜다.
힙 안의 필드와 배열에 원자적으로 접근하는 일(온힙)과,
GC 바깥의 메모리를 다루는 일(오프힙)이다.
앞쪽의 공식 대체재가 `VarHandle`이며, 이것은 JDK 9에 이미 나왔다.

`VarHandle`은 변수 하나를 가리키는 타입 안전한 핸들이고,
접근할 때 메모리 순서(memory ordering)를 골라 쓴다.

```java
class Counter {
    private volatile long value;

    private static final VarHandle VALUE;
    static {
        try {
            VALUE = MethodHandles.lookup()
                .findVarHandle(Counter.class, "value", long.class);
        } catch (ReflectiveOperationException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    void increment() {
        long prev;
        do {
            prev = (long) VALUE.getVolatile(this);       // volatile 읽기
        } while (!VALUE.compareAndSet(this, prev, prev + 1));  // CAS
    }
}
```

접근 모드가 촘촘하게 나뉘어 있다는 점이 핵심이다.

| 모드            | 메서드                       | 보장                               |
| --------------- | ---------------------------- | ---------------------------------- |
| plain           | `get`, `set`                 | 일반 필드 접근과 같다              |
| opaque          | `getOpaque`, `setOpaque`     | 원자적이고 일관되나 순서 보장 없음 |
| acquire/release | `getAcquire`, `setRelease`   | 부분 순서 보장                     |
| volatile        | `getVolatile`, `setVolatile` | 전체 순서 보장                     |
| CAS             | `compareAndSet`, `getAndAdd` | 원자적 갱신                        |

`Unsafe`의 CAS는 오프셋을 직접 계산해 넘겨야 했고 타입 검사가 없었다.
`VarHandle`은 필드 이름과 타입으로 찾으므로 잘못된 타입이면 생성 시점에 막힌다.
배열은 `MethodHandles.arrayElementVarHandle(int[].class)`로 얻고,
`fullFence()` 같은 메모리 펜스도 여기에 정리돼 있다.

## FFM: 오프힙 접근의 공식 대체재

나머지 절반, 곧 오프힙 메모리와 네이티브 함수 호출을 맡는 것이
FFM(Foreign Function & Memory API)이다.
Project Panama의 결과물로 [JEP 454](https://openjdk.org/jeps/454)에서
JDK 22에 정식 기능이 되었다.

핵심 타입은 둘이다.
`MemorySegment`는 연속된 메모리 영역을 가리키고,
`Arena`는 그 영역의 수명을 관리한다.

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment seg = arena.allocate(ValueLayout.JAVA_LONG, 100);
    seg.setAtIndex(ValueLayout.JAVA_LONG, 0, 42L);
    long v = seg.getAtIndex(ValueLayout.JAVA_LONG, 0);
}   // 블록을 벗어나면 메모리가 해제된다
```

`Unsafe`와 비교하면 무엇이 달라졌는지가 분명하다.

| 항목         | `Unsafe`               | FFM                                 |
| ------------ | ---------------------- | ----------------------------------- |
| 주소 표현    | 벌거벗은 `long`        | `MemorySegment` (크기를 안다)       |
| 범위 검사    | 없음                   | 매 접근마다 공간 경계 검사          |
| 해제         | `freeMemory` 직접 호출 | `Arena` 닫힘에 연동                 |
| 해제 후 사용 | JVM 크래시             | `IllegalStateException`             |
| 스레드 경계  | 없음                   | confined arena는 소유 스레드만 접근 |

`Arena`는 네 종류가 있다.
`ofConfined`는 한 스레드만 접근하고 닫을 때 해제하며,
`ofShared`는 여러 스레드가 접근하되 동기화 비용을 치른다.
`ofAuto`는 GC가 도달 불가를 감지하면 해제하고,
`global`은 영원히 살아 있다.

네이티브 함수 호출도 같은 API에서 된다.
JNI처럼 C 헤더를 만들고 네이티브 메서드를 선언할 필요가 없다.

```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").get(),
    FunctionDescriptor.of(JAVA_LONG, ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello");
    long len = (long) strlen.invoke(str);   // 5
}
```

반대 방향, 곧 네이티브 코드가 Java 메서드를 부르는 업콜은
`linker.upcallStub()`으로 만든다.
`qsort`에 Java로 쓴 비교 함수를 넘기는 것이 JEP의 예제다.

## 폐기 표시는 어디까지 진행됐는가

후보자가 말한 폐기 표시는 진행 중인 5단계 계획의 일부다.
[JEP 471](https://openjdk.org/jeps/471)이 그 계획을 정했다.
`sun.misc.Unsafe`의 메서드 87개 중 79개가 메모리 접근용이며, 이들이 대상이다.

| 단계 | 릴리스 | 무슨 일이 일어나는가                          |
| ---- | ------ | --------------------------------------------- |
| 1    | JDK 23 | 컴파일 시점 폐기 경고 (terminally deprecated) |
| 2    | JDK 24 | 실행 시점 경고가 기본값 (`warn`)              |
| 3    | JDK 26 | 호출하면 예외 (`deny`)                        |
| 4~5  | 이후   | 온힙 메서드 먼저, 오프힙 메서드 나중에 제거   |

2단계를 실행한 [JEP 498](https://openjdk.org/jeps/498)부터
JDK 24에서는 별도 설정 없이 다음 경고가 뜬다.

```text
WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
WARNING: sun.misc.Unsafe::setMemory has been called by com.foo.bar.Server
WARNING: Please consider reporting this to the maintainers of com.foo.bar.Server
WARNING: sun.misc.Unsafe::setMemory will be removed in a future release
```

`--sun-misc-unsafe-memory-access` 옵션으로 단계를 앞당기거나 미룰 수 있다.
`allow`는 경고 없음, `warn`은 첫 호출에 한 번 경고,
`debug`는 매번 스택 트레이스까지, `deny`는 `UnsupportedOperationException`이다.
새 코드를 쓴다면 `deny`로 먼저 돌려 보는 것이 이후 마이그레이션 비용을 줄인다.

후보자가 높은 버전 JDK에서 폐기됐다고 말한 것은 이 상황을 정확히 짚은 것이다.
다만 온힙 대체재는 JDK 9부터, 오프힙 대체재는 JDK 22부터 있었으므로,
갑작스러운 통보가 아니라 15년에 걸친 예고된 정리다.

## 그래서 지금 Java에 포인터가 있는가

정확한 답은 이렇다.
언어의 기본 모델에는 여전히 포인터가 없다.
객체 참조는 여전히 수치로 읽을 수 없고 산술도 되지 않는다.

그러나 오프힙 메모리를 직접 다루는 일은 공식 API로 가능해졌고,
그 접근은 포인터가 아니라 경계와 수명을 아는 세그먼트를 통해 이뤄진다.
같은 능력을 얻으면서 실패 양식은 버린 셈이다.
`Unsafe`에서 잘못된 주소가 JVM을 죽였다면,
FFM에서 같은 실수는 `IndexOutOfBoundsException`이나 `IllegalStateException`이 된다.

그래서 2026년의 정답은 없습니다도 아니고 있습니다도 아니다.
직접 다루는 포인터는 없고, 경계가 관리되는 메모리 접근은 있다는 것이다.
면접에서 이 구분을 말할 수 있다면 농담의 후보자보다 나은 답이다.

## 같은 10년의 다른 변화들

농담은 메모리 API만 다루지만, 같은 기간 Java의 다른 축도 크게 움직였다.
2026년 면접 범위가 넓어졌다는 체감은 이쪽에서 더 크다.

| 기능             | 상태                  | 요지                                            |
| ---------------- | --------------------- | ----------------------------------------------- |
| 가상 스레드      | JDK 21 정식           | 블로킹 코드를 그대로 두고 동시성을 키운다       |
| 스코프 값        | JDK 25 정식           | `ThreadLocal`을 대체하는 불변 공유 값           |
| 구조적 동시성    | JDK 25 프리뷰 (5번째) | 관련 작업을 한 단위로 묶어 취소와 오류를 다룬다 |
| 패턴 매칭·레코드 | JDK 21 정식           | `switch` 패턴, 레코드 분해                      |
| Vector API       | 인큐베이터 지속       | SIMD 연산의 이식 가능한 표현                    |

가상 스레드가 특히 이 문서의 주제와 이어진다.
오프힙 메모리와 네이티브 호출이 안전해지고 경량 스레드가 값싸지면서,
그동안 C나 C++에 내주던 영역, 곧 고성능 직렬화와 네이티브 상호작용을
Java 안에서 처리할 여지가 넓어졌다.

## 마이그레이션이 필요하다면

`Unsafe`를 쓰는 코드가 있다면 대체 경로는 용도에 따라 갈린다.

| 기존 용도                | 대체재                    | 비고                             |
| ------------------------ | ------------------------- | -------------------------------- |
| 필드·배열 원자 접근, CAS | `VarHandle`               | JDK 9부터 가능                   |
| 오프힙 할당과 접근       | `Arena` + `MemorySegment` | JDK 22부터 정식                  |
| 네이티브 함수 호출       | `Linker` (FFM)            | JNI보다 간결                     |
| 객체 생성 우회 (직렬화)  | 대체재 없음               | `Unsafe`에 남아 있는 8개 중 일부 |

주의할 점이 둘 있다.
첫째, FFM의 `MemorySegment::reinterpret` 같은 일부 메서드는 여전히 제한적이라
`--enable-native-access` 없이 쓰면 경고가 나고,
앞으로의 릴리스에서는 이 옵션이 필수가 될 수 있다.
둘째, 메모리 접근이 아닌 `Unsafe` 메서드 8개는 이번 폐기 대상이 아니다.
역직렬화 프레임워크가 생성자를 건너뛰고 객체를 만드는 데 쓰는 기능이 여기 속하며,
이쪽은 아직 공식 대체재가 없다.

## 참고 자료

- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 471: Deprecate the Memory-Access Methods in sun.misc.Unsafe for Removal](https://openjdk.org/jeps/471)
- [JEP 498: Warn upon Use of Memory-Access Methods in sun.misc.Unsafe](https://openjdk.org/jeps/498)
- [VarHandle (Java SE 25 API)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/invoke/VarHandle.html)
