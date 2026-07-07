# Typeshare — Rust 타입을 여러 언어로 자동 변환하는 도구

<https://github.com/1Password/typeshare>

## 소개

Typeshare는 1Password가 사내 도구로 개발해 오픈소스로 공개한 Rust FFI(Foreign Function Interface) 타입 동기화 도구다.
Rust 코드에 `#[typeshare]` 어트리뷰트를 붙이면 CLI가 해당 타입을 파싱해
Kotlin, Swift, TypeScript, Scala, Go, Python 형식의 타입 정의 파일을 생성한다.
serde 라이브러리 위에서 동작하기 때문에 직렬화·역직렬화 구현까지 자동으로 포함된다.

저장소는 4개의 크레이트로 구성된다.
`typeshare` 크레이트는 프로시저럴 매크로(`#[typeshare]`)를 제공하고,
`typeshare-core`는 Rust 파싱과 코드 생성 로직을 담당한다.
`typeshare-annotation`은 어트리뷰트 파싱, `typeshare-cli`는 CLI 진입점이다.
2022년 9월 공개 이후 약 3,000개의 스타를 얻었으며, 89개의 오픈 이슈가 있다.

## 사용법

### 설치 및 기본 사용

CLI 설치와 기본 실행은 한 쌍이다.

```bash
cargo install typeshare-cli
```

```bash
typeshare ./my_rust_project --lang=kotlin --output-file=my_kotlin_definitions.kt
typeshare ./my_rust_project --lang=swift --output-file=my_swift_definitions.swift
typeshare ./my_rust_project --lang=typescript --output-file=my_typescript_definitions.ts
typeshare ./my_rust_project --lang=scala --output-file=my_scala_definitions.scala
```

Go와 Python은 실험적 기능이며 `--features go` 또는 `--features python`으로 명시적으로 활성화해야 한다.

### 타입 어노테이션

Rust 타입에 `#[typeshare]`를 붙이면 변환 대상이 된다.

```rust
#[typeshare]
struct MyStruct {
    my_name: String,
    my_age: u32,
}

#[typeshare]
#[serde(tag = "type", content = "content")]
enum MyEnum {
    MyVariant(bool),
    MyOtherVariant,
    MyNumber(u32),
}
```

위 Rust 코드는 다음 TypeScript로 변환된다.

```typescript
export interface MyStruct {
    my_name: string;
    my_age: number;
}

export type MyEnum =
    | { type: "MyVariant", content: boolean }
    | { type: "MyOtherVariant", content: undefined }
    | { type: "MyNumber", content: number };
```

### 어드밴스드 어노테이션

`#[typeshare]`는 인자를 통해 세부 동작을 제어한다.

- **언어별 데코레이터**: `#[typeshare(swift = “Equatable, Codable”)]`로 Swift 프로토콜을 추가한다.
- **타입 별칭**: `#[typeshare(serialized_as = “String”)]`으로 다른 타입으로 직렬화되도록 지시한다.
- **필드별 타입 지정**: `#[typeshare(typescript(type = “Record<string, any>”))]`로 특정 언어에서의 타입을 명시한다.
- **필드 제외**: `#[typeshare(skip)]` 또는 `#[serde(skip)]`으로 특정 필드를 변환에서 제외한다.

serde의 `rename_all`, `rename`, `tag`, `content` 등 어트리뷰트도 그대로 반영된다.

## 분석

### 문제의 구조: FFI 타입 불일치는 런타임에야 드러난다

크로스 플랫폼 앱에서 Rust 백엔드와 Swift·Kotlin 프론트엔드 사이의 타입 불일치는
컴파일 타임이 아닌 런타임에야 표면화된다.
필드 이름이 바뀌거나 enum 변형이 추가될 때, 양쪽 코드를 수동으로 동기화하는 것은
리뷰어의 주의력에 의존한 취약한 프로세스다.
Typeshare는 이 문제를 “Rust를 단일 정보 원천(source of truth)으로 삼는다”는 원칙으로 해결한다.
어노테이션이 붙은 타입은 CI 파이프라인에서 자동 생성되므로, 타입 정의 불일치는 구조적으로 방지된다.

1Password가 이 도구를 사내에서 먼저 개발했다는 사실은 문제의 성격을 증명한다.
이미 수백만 사용자를 보유한 제품에서 타입 불일치 버그는 보안 취약점으로 직결될 수 있다.
비밀번호 데이터를 주고받는 FFI 경계에서의 역직렬화 실패는 단순 오류가 아니다.
도구가 실용적 동기에서 출발했다는 점은 문서화된 스펙이 아니라 실제 사용 사례를 반영함을 의미한다.

### serde에 대한 의존 구조: 지렛대이자 족쇄

Typeshare의 핵심 전제는 “serde가 이미 정확한 직렬화 형태를 서술하고 있다”는 것이다.
`#[serde(rename_all = “camelCase”)]`나 `#[serde(tag = “type”, content = “content”)]` 같은 어트리뷰트를
Typeshare가 그대로 해석해 타깃 언어 코드에 반영하는 구조다.
이는 기존 serde 코드베이스에서 추가 작업 없이 도입할 수 있다는 장점을 준다.

그러나 동시에 Typeshare의 지원 범위는 serde가 표현할 수 있는 것으로 제한된다.
serde가 직접 지원하지 않는 복잡한 직렬화 로직은 Typeshare로 표현할 수 없다.
`#[typeshare(serialized_as = “String”)]` 같은 탈출구가 있지만,
이는 타입 안전성을 포기하는 대가를 치른다.
serde에 대한 의존이 Typeshare의 확장성을 구조적으로 제한하고 있다.

### 지원 언어의 불균형: 실험적 기능의 의미

Kotlin, Swift, TypeScript, Scala는 안정적으로 지원하지만
Go와 Python은 “실험적” 상태다.
이 구분은 단순히 기능 성숙도의 차이가 아니다.
Go의 타입 시스템은 Rust enum의 tagged union 패턴을 자연스럽게 표현할 방법이 없고,
Python은 타입 힌트가 선택적이다.
두 언어에서 Rust enum을 “올바르게” 변환한다는 것의 의미 자체가 애매하다.
실험적 지원은 “가능은 하나 프로덕션에서 의존하기 어렵다”는 신호다.

## 비평

### Rust 타입 시스템의 표현력이 변환 경계를 결정한다

Typeshare는 Rust enum의 강력함을 타깃 언어에 전달하는 것을 핵심 가치로 내세우지만,
이 전달이 가능한 것은 타깃 언어가 tagged union을 표현할 수 있을 때뿐이다.
TypeScript는 discriminated union으로, Swift는 associated value가 있는 enum으로 변환이 자연스럽다.
그러나 Kotlin에서 sealed class로의 변환이나 Go에서의 변환은 이미 구조적 불일치를 내포한다.
“Rust를 정보 원천으로 삼는다”는 원칙은 실제로는 “Rust가 표현한 것 중 타깃 언어가 수용할 수 있는 부분만”으로 제한된다.
이 경계가 어디인지 문서는 충분히 명시하지 않는다.

Go 지원이 실험적인 이유는 바로 이 지점이다.
Rust의 `Option<T>`는 Go에서 포인터 타입이나 래퍼 타입으로 표현되어야 하는데,
어느 쪽도 Rust의 의미와 완전히 일치하지 않는다.
Typeshare가 내리는 변환 결정은 암묵적이고, 사용자는 그 결과를 검증할 수단이 CLI 출력 파일밖에 없다.
변환 시맨틱을 문서화하는 공식 규격이 없다는 점은 숨겨진 부채다.

### 단방향 변환은 협업 모델의 절반만 해결한다

Typeshare는 Rust → 타깃 언어 방향의 코드 생성만 지원한다.
반대 방향 — 이미 존재하는 Swift 또는 Kotlin 타입 정의를 Rust로 가져오는 것 — 은 지원하지 않는다.
1Password 같은 조직에서 Rust가 진정한 정보 원천이 될 수 있는 것은
Rust 팀이 타입 설계를 주도하는 구조이기 때문이다.
그러나 Rust 도입 이전부터 타입 정의가 Swift나 Kotlin에 먼저 존재하는 팀에게는
이 도구를 도입하는 것이 구조적 권력 이동을 요구한다.
Rust 팀이 타입 소유권을 가져야 Typeshare가 의미 있다.
이 전제는 문서 어디에도 명시되어 있지 않다.

### 타입 안전성 보장의 범위가 CLI 경계에서 끊긴다

Typeshare는 빌드 타임에 타입 정의 파일을 생성하지만,
생성된 파일이 실제로 프로젝트에 반영되었는지는 보장하지 않는다.
Rust 코드를 수정하고 `typeshare` CLI를 실행했지만 출력 파일을 커밋하지 않은 상황,
혹은 출력 파일은 커밋했지만 네이티브 코드가 새 버전을 임포트하지 않은 상황은
Typeshare가 탐지하지 못한다.
CI에서 `typeshare` 실행 후 `git diff --exit-code`로 검사하는 패턴을 직접 구성해야 하는데,
이 패턴을 권장하는 내용이 공식 문서에 빠져 있다.
타입 안전성의 진짜 보장은 이 CI 훅에 있는데, 도구가 그것을 안내하지 않는다.

## 인사이트

### 언어 경계를 넘는 타입 안전성은 조직 구조 문제다

Typeshare가 해결하는 기술적 문제 — 타입 불일치 — 는 실은 조직 구조 문제의 증상이다.
모바일 클라이언트 팀과 Rust 백엔드 팀이 분리되어 있고, 양측이 독립적으로 배포할 때
타입 계약은 누군가의 책임 하에 관리되어야 한다.
Typeshare를 도입한다는 것은 Rust 코드베이스가 그 계약의 주인이 된다는 합의를 전제로 한다.
기술 선택이 아니라 팀 간 계약의 문제다.

Typeshare를 도입했지만 효과를 보지 못한 팀은 대부분
이 조직적 합의 없이 도구만 도입한 경우일 것이다.
Swift 팀이 독립적으로 타입을 변경하고, Rust 팀이 그것을 나중에 반영하는 구조에서는
Typeshare가 오히려 혼선을 심화시킨다.
정보 원천이 둘이 되기 때문이다.
도구가 조직 문제를 해결하지 않는다는 원칙이 여기서도 적용된다.

### 제너레이티브 타입 도구의 유지보수 함정: 타깃 언어가 변할 때

Typeshare의 지속적 사용 가치는 타깃 언어가 안정적이라는 가정 위에 있다.
TypeScript는 매년 새로운 기능을 추가하고, Kotlin의 타입 시스템도 진화한다.
Swift의 경우 엄격 동시성(strict concurrency) 모델이 도입되면서
Codable 관련 API가 변화했다.
타깃 언어의 변화가 Typeshare의 코드 생성 결과를 낡게 만들 수 있다.

이 문제는 89개의 오픈 이슈에 이미 반영되어 있다.
언어별 지원은 언어 자체의 생태계 속도를 따라가야 하는데,
오픈소스 유지보수 부담은 1Password 팀에게 집중된다.
커뮤니티 기여로 언어 지원이 추가될 수 있지만,
제너레이터 로직의 정확성을 검증하는 것은 고도로 전문적인 작업이다.
타깃 언어가 늘어날수록 조합적으로 복잡해지는 테스트 매트릭스가
장기 지속 가능성에 잠재적 위험이다.

### 프로시저럴 매크로 기반 어노테이션의 숨겨진 비용

`#[typeshare]` 어트리뷰트를 타입에 붙이는 것은 단순해 보이지만,
그 타입이 FFI 경계를 통과하도록 설계되어야 한다는 암묵적 제약을 수반한다.
직렬화 가능한 타입만 어노테이션을 붙일 수 있고,
Rust 타입 시스템의 풍부한 표현력 — 라이프타임, 트레잇 오브젝트, 소유권 패턴 — 은
FFI 경계에서 사라진다.
개발자는 `#[typeshare]` 타입과 내부용 타입을 분리해서 유지하거나,
내부 타입을 FFI에 맞게 설계해야 하는 선택에 직면한다.

전자를 선택하면 변환 레이어 코드가 생기고,
후자를 선택하면 Rust 타입의 표현력을 포기한다.
Typeshare는 이 트레이드오프를 문서에서 논의하지 않는다.
도구가 해결하는 문제만큼 새롭게 유발하는 설계 결정이 있다는 사실,
그리고 그 결정의 비용이 즉각적이지 않다는 점이 장기적으로 더 큰 문제가 될 수 있다.
