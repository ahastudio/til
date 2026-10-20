# Java sealed 타입을 공개 API에 두면 새 하위 타입이 런타임 예외가 된다

원문: [Java sealed classes and exhaustive pattern matching – Neil Madden](https://neilmadden.blog/2026/04/24/java-sealed-classes-and-exhaustive-pattern-matching/)

HN 토론: <https://news.ycombinator.com/item?id=50141579> (184점, 147개 댓글)

GN 토론: <https://news.hada.io/topic?id=35598>

## 소개

Neil Madden의 이 글은 Java 17에서
도입된 sealed 클래스와 이를 이용한 exhaustive 패턴 매칭이 공개 API에서
어떤 호환성 문제를 만드는지 보여 준다. sealed 타입은 허용되는 하위 타입을
명시적으로 나열하고
컴파일러는 그 목록을 알기 때문에 `switch`가 모든 경우를 다뤘는지 검사한다.
모든 경우를 다뤘다면 `default` 절이 필요 없고
하나를 빠뜨리면 컴파일 오류가 난다.

글의 결론은 두 문장으로 줄일 수 있다. sealed 타입은 컴포넌트의 구현 안쪽에서
가장 쓸모 있고 컴포넌트가 다른 컴포넌트에 내놓는 공개 API에서는 쓸모가 줄어든다.
모듈 경계를 넘어 쓰면 코드를 깨뜨리는 새 방법을 만들 수 있고
그 깨짐은 런타임에야 발견되는 경우가 많다.
저자는 JDK의 PEM 인코딩 API 미리보기(JEP 524)를 검토하다가
이 미묘함을 발견했다고 밝힌다.
그 API가 sealed 인터페이스를 공개 API에 넣고
클라이언트에게 그 타입으로 패턴 매칭을 권하는 실수를 한다는 것이다.

## 동작 방식

### 컴파일 시점의 검사는 소비자를 컴파일할 때만 일어난다

글의 예제는 `SealedType` 인터페이스에 `TypeA`와 `TypeB` 두 레코드가 있고
소비자 `Main`이 `default` 없이 두 경우를 모두 다루는 `switch` 식을 쓰는 구조다.
여기에 `TypeC`를 더하고 `Main`을 다시 컴파일하면
`switch` 식이 모든 값을 다루지 않는다는 오류가 난다.
라이브러리 작성자 입장에서는
하위 타입 하나를 더하는 일이 소비자 코드를 깨뜨리는 변경이므로,
SemVer를 따른다면 주 버전을 올려야 한다는 것이 글의 첫 번째 지적이다.

두 번째 지적은 더 까다롭다.
`SealedType.java`만 다시 컴파일하고
`Main`은 다시 컴파일하지 않으면 컴파일러가 검사할 기회가 없다.
그 상태에서 새 경우가 들어오면 `MatchException`이 런타임에 던져진다.
글은 이 예외의 Javadoc도 별도 컴파일의 이런 문제와 패턴
안의 `null`에 관한 몇몇 예외 상황을 언급한다고 적는다.
따라서 sealed 클래스를 쓰면
새 경우를 추가할 때 모든 소비자의 갱신을 정적으로 보장받는다고
기대했더라도, 전부 다시 컴파일하지 않으면 그렇지 않다.

### 같은 조건을 한 번에 재현하기

글의 예제를 그대로 확인하는 명령은 아래와 같다.
Java 25에서 인스턴스 `main` 메서드가 정식 기능이므로
`void main`을 그대로 쓸 수 있다.

```bash
mkdir -p v1 v2 out1 out2

cat > v1/SealedType.java <<'EOF'
public sealed interface SealedType {
    record TypeA() implements SealedType {}
    record TypeB() implements SealedType {}
    static SealedType of(String type) {
        return switch (type) {
            case "A" -> new TypeA();
            case "B" -> new TypeB();
            default -> throw new IllegalArgumentException();
        };
    }
}
EOF

cat > v1/Main.java <<'EOF'
void main(String[] args) {
    var val = SealedType.of(args[0]);
    System.out.println(switch (val) {
        case SealedType.TypeA() -> "A";
        case SealedType.TypeB() -> "B";
    });
}
EOF

# v2는 TypeC를 더한 라이브러리 버전이다
sed -e 's/record TypeB() implements SealedType {}/&\n    record TypeC() implements SealedType {}/' \
    -e 's/case "B" -> new TypeB();/&\n            case "C" -> new TypeC();/' \
    v1/SealedType.java > v2/SealedType.java
cp v1/Main.java v2/Main.java

# 1) v1 전체를 컴파일하고 실행한다
javac -d out1 v1/SealedType.java v1/Main.java
java -cp out1 Main A

# 2) 라이브러리만 v2로 다시 컴파일하고 소비자는 그대로 둔 채 새 경우를 실행한다
javac -d out1 v2/SealedType.java
java -cp out1 Main C

# 3) 소비자도 v2에 대해 컴파일하면 컴파일 오류가 난다
javac -d out2 v2/SealedType.java v2/Main.java
```

이 문서가 Temurin 25.0.3에서 실행한 결과는 이렇다.
첫 실행은 `A`를 출력한다.
두 번째 실행은 `java.lang.MatchException`이 `Main.main(Main.java:3)`에서
던져진다.
세 번째 컴파일은
`the switch expression does not cover all possible input values`
오류로 실패한다.

## 설계하기

### 공개 API의 sealed 타입을 고르는 기준

글의 결론을 그대로 규칙으로 옮기면 이렇다.

| 상황                                                  | 권장                                             | 이유                                             |
| ----------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| 컴포넌트 안에서만 쓰고 항상 함께 컴파일한다           | sealed와 `default` 없는 `switch`를 쓴다          | 컴파일 시점의 완전성 검사를 얻는다               |
| 라이브러리가 공개 API로 내놓고 하위 타입이 늘 수 있다 | sealed를 피하거나 소비자가 `default`를 갖게 한다 | 새 하위 타입이 소비자를 런타임에 깨뜨린다        |
| 라이브러리가 집합이 닫혀 있다고 약속할 수 있다        | sealed를 쓰고 문서에 닫혀 있다고 적는다          | 새 하위 타입이 곧 주 버전 변경임을 소비자가 안다 |

OpenJDK의 Amber 팀이 쓴 안내문 「Preparing for Change:
Safe Switching over Sealed APIs」는 같은 문제를 라이브러리
작성자와 소비자의 책임으로 나눠 다룬다.[^amber-guide]
작성자는 타입을 왜 sealed로 두었는지와 앞으로 어떻게
바뀔 것으로 예상하는지를 문서에 적으라고 한다.
소비자에게는 `default`를 거의 쓰지 말고
허용된 하위 타입마다 `case`를 두라고 권한다.
`default`가 완전성 검사의 의도를 숨기고 미래의 변경을 덮을 수 있다는 이유다.
다만 모든 하위 타입을 나열하기 어려운 경우에는
가장 좁은 타입의 일치 패턴을 쓰라고 한다.

### 하위 타입 하나를 공개하지 않는 우회

이 글이 나온 뒤 HN에서
JDK 개발자 smarks는 JDK 26의 PEM 인코딩 API가 이 위험을 갖고 있었음을 확인했다.
JDK 27 버전인 JEP 538에서는
허용된 하위 타입에 공개되지 않은 것을 하나 포함시켰다고 한다.[^smarks]
이렇게 하면
애플리케이션이 하위 타입을 전부 나열한 exhaustive `switch`를 쓸 수 없고
JDK는 나중에 허용 하위 타입을 늘려도 예상하지 못한 예외를 일으키지 않는다.

이 우회가 실제로 그렇게 동작하는지는 아래 예제로 확인할 수 있다.
`lib` 패키지의 `Shape`가 공개된 두 하위 타입과
패키지 안에서만 보이는 `Hidden`을 허용한다.

```bash
mkdir -p v3/lib v3/app out3

cat > v3/lib/Shape.java <<'EOF'
package lib;

public sealed interface Shape permits Shape.Circle, Shape.Square, Hidden {
    record Circle(double r) implements Shape {}
    record Square(double s) implements Shape {}
}
EOF

cat > v3/lib/Hidden.java <<'EOF'
package lib;

// 패키지 안에서만 보이는 허용 하위 타입이라 소비자가 이름을 쓸 수 없다
record Hidden() implements Shape {}
EOF

cat > v3/app/Main.java <<'EOF'
import lib.Shape;

public class Main {
    public static void main(String[] args) {
        Shape s = new Shape.Circle(1);
        System.out.println(switch (s) {
            case Shape.Circle c -> "circle";
            case Shape.Square q -> "square";
        });
    }
}
EOF

javac -d out3 v3/lib/Shape.java v3/lib/Hidden.java v3/app/Main.java
```

이 문서가 같은 JDK에서
실행했을 때 `default` 없는 `switch`는 모든
값을 다루지 않는다는 오류로 컴파일에 실패했다.
소비자가 `default -> "other"`를 더하면 컴파일되고 `circle`을 출력했다.
이 우회는 소비자가 새 경우를 컴파일 시점에 놓치지
않게 하는 대신 처음부터 `default`를 쓰게 강제한다.
같은 위험이 있는 `switch`를 아예 쓸 수 없게 만들어 런타임 예외를 막는 방식이다.

## 트레이드오프

### 컴파일 오류가 드러내는 깨짐을 받아들이는 쪽과 숨기는 쪽

Amber 안내문은 소비자가 다시 컴파일할 때
컴파일러가 거부하는 것을 바람직한 피드백으로 본다.
가정이 깨진 코드를 알려 주기 때문이다.
반대편에서
라이브러리 작성자는 하위 타입을 더하는 일이
모든 소비자에게 깨짐이 된다는 비용을 진다.
HN에서 misja111은 소비자와 생산자의 API 사이에서
이 변경이 바이너리 호환성을 깨는 것으로 취급되어야 한다고
했다.[^misja111] looperhacks는 JVM에서
바이너리 호환성 문제는 어차피 런타임에 나타나며
`MatchException`이 링크 오류(`LinkageError`)의 하위 클래스였다면
실수로 잡히는 일을 피했을 것이라고 적었다.[^looperhacks] tpxl은 sealed가 없어도
인터페이스 A의 구현체 B와 C를 가정한 코드는 라이브러리가
D를 내놓는 순간 오류를 만난다고 반박했다.[^tpxl]
세 댓글은 글의 새 위험이 sealed가 만든 것이 아니라 기존의 위험을 더 눈에 띄게
만든 것임을 보여 준다. sealed가 새로 주는 것은 컴파일이
되던 코드가 라이브러리를 바꾸기만 해도 깨진다는 확실성이다.

### JDK 팀은 이 문제를 패턴 매칭보다 하위 클래스 통제의 문제로 본다

smarks는 라이브러리 설계자로서
자신이 sealed를 쓰는 주된 이유가 하위 클래스 통제라고 했다.
예전에는 생성자의 접근 범위를 패키지 수준으로 줄여 외부의 하위 클래스를 막았고
인터페이스는 통제할 방법이 없었다고 한다.
JDK는 이런 옛 관용구를 모두 sealed로 바꿨고
수십 개의 사례 가운데 패턴 매칭의 후보로 보이는 것은
하나도 없다는 것이 그의 판단이다.[^smarks-control]
이 판단이 맞다면
글의 우려는 패턴 매칭을 목적으로 sealed를 공개 API에 내놓는 경우에 해당하고
하위 클래스 통제만이 목적인 경우에는 해당하지 않는다.

저자 nmadden은 이 답에서 문제가 고쳐진 것을 반기면서
자신이 당시에 보고한 보안 약점을 포함한 다른 설계 문제도 고쳐지기를 바란다고
적었다.
그때 받은 응답이 다소 무시하는 듯하고
도움이 되지 않았다는 평가도 덧붙였다.[^nmadden]
이 부분은 이 글의 기술적 논증과는 별개의 이야기이고
이 문서는 보안 약점의 내용을 확인하지 못했다.

## 함정

`default`를 넣으면 컴파일은 되지만
새 하위 타입이 `default`로 흘러가므로 완전성 검사를 잃는다.
Amber 안내문도 이 점을 이유로 `default`를 거의 쓰지 말라고 한다.

`MatchException`은 소비자 쪽에서
쉽게 잡아 버릴 수 있다. looperhacks가 지적했듯 이 예외가 링크
오류 계열이 아니어서 광범위한 `catch (Exception e)`에 걸린다.

sealed라는 표시만으로는 하위 타입 집합이 영원히 닫힌다는 약속이 되지 않는다.
라이브러리가 그런 약속을 문서에 적지 않았다면
소비자는 집합이 늘 수 있다고 가정해야 한다.

공개 API의 sealed 타입은 하위 타입이 늘면
주 버전을 올린다는 약속과 함께 내놓아야 한다는 것이 글의 요지다.
그 약속이 없는 라이브러리가 sealed를 내놓으면
소비자는 완전성 검사를 믿고 `default`를 뺄 수 있다.
그것이 위험이다.

## 확인하기

위 두 예제를 `v1`, `v2`, `v3` 디렉터리로 나눠 실행해 세 가지를 눈으로 본다.
소비자를 다시 컴파일하지 않고 라이브러리만 바꾸면 `MatchException`이 나는지,
다시 컴파일하면 컴파일 오류가 나는지,
공개되지 않은 허용 하위 타입이 있을 때
`default` 없이는 컴파일되지 않는지를 확인한다.
자신의 프로젝트에서는
공개 API에 노출된 sealed 타입을 찾아 각 타입이 닫힌 집합을 약속하는지 문서에서
확인한다.

## 체크리스트

- 공개 API에 노출된 sealed 타입마다 왜 sealed로 두었는지 문서에 적혀 있는가.
- 하위 타입을 더할 때 SemVer의 주 버전을 올리는 정책이 있는가.
- 소비자가 `default`를 쓰도록 안내했는가,
아니면 모든 하위 타입을 나열하도록 안내했는가.
- 패턴 매칭이 목적이 아니라면 sealed 대신 접근 범위나 패키지로 통제할 수 있는가.
- 소비자를 함께 다시 컴파일하지 않는 배포 구조에서
`MatchException`이 어떻게 처리되는지 확인했는가.

## 기억할 원칙

### sealed는 닫힌 집합에 대한 약속이고 약속의 상대는 소비자다

sealed 타입은 컴파일러에게 하는 선언이기 이전에 소비자에게 하는 약속이다.
집합이 닫혀 있다는 약속이 있으면
소비자는 완전성 검사에 기대어 `default` 없이 코드를 쓸 수 있고
라이브러리는 그 약속을 깨는 변경에 주 버전을 올려야 한다.
약속을 할 수 없다면
공개되지 않은 허용 하위 타입을 두어 소비자가 약속을
기대하지 못하게 하는 것이 JDK 팀이 택한 방법이다.

---

[^amber-guide]: OpenJDK Amber, [Preparing for Change: Safe Switching over Sealed APIs](https://openjdk.org/projects/amber/guides/exhaustiveness-guide), 2026-08-11

[^smarks]: <https://news.ycombinator.com/item?id=50148756>

[^misja111]: <https://news.ycombinator.com/item?id=50149325>

[^looperhacks]: <https://news.ycombinator.com/item?id=50149820>

[^tpxl]: <https://news.ycombinator.com/item?id=50149836>

[^smarks-control]: <https://news.ycombinator.com/item?id=50159310>

[^nmadden]: <https://news.ycombinator.com/item?id=50150459>
