# ResponseStatusException

<https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html>

<https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/server/ResponseStatusException.html>

Spring 5.0(2017년 9월)에서 도입된 `ResponseStatusException`은 HTTP 상태 코드와
함께 예외를 프로그래밍 방식으로 던질 수 있는 클래스다.
`@ResponseStatus` 애노테이션 기반 방식의 한계를 보완하기 위해 설계됐다.

Spring 6.0에서 클래스 계층이 바뀌었다. 기존에는 `NestedRuntimeException`을
직접 상속했지만, RFC 9457(Problem Details for HTTP APIs) 지원을 위해
`ErrorResponseException`의 하위 클래스로 재배치됐다. 덕분에 `ProblemDetail`
기반의 표준화된 에러 응답 형식과 자동으로 연동된다.

```text
NestedRuntimeException
  └─ ErrorResponseException        ← Spring 6.0에서 중간 계층 추가
      └─ ResponseStatusException
```

## 등장 배경

Spring MVC에서 HTTP 에러 응답을 만드는 전통적인 방법은 두 가지였다.

**방법 1: 커스텀 예외 클래스에 `@ResponseStatus` 애노테이션 붙이기**

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("User not found: " + id);
    }
}
```

**방법 2: `@ExceptionHandler`로 전역 처리**

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public void handleNotFound() {}
}
```

두 방법 모두 문제가 있다. 상태 코드가 하나 필요할 때마다 새 예외 클래스를
만들어야 하고, 상태 코드가 런타임 조건에 따라 달라지는 경우를 다루기 어렵다.

## ResponseStatusException 사용법

`ResponseStatusException`은 예외 클래스를 따로 만들지 않고 즉석에서 던진다.

```java
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new ResponseStatusException(
            HttpStatus.NOT_FOUND, "User not found: " + id
        ));
}
```

생성자는 세 가지 형태를 제공한다.

```java
// 상태 코드만
new ResponseStatusException(HttpStatus.NOT_FOUND);

// 상태 코드 + 메시지
new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found");

// 상태 코드 + 메시지 + 원인 예외
new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found", cause);
```

## 상태 코드를 동적으로 결정하는 경우

`@ResponseStatus`로는 다룰 수 없는 시나리오를 깔끔하게 처리한다.

```java
@PostMapping("/items/{id}/reserve")
public void reserveItem(@PathVariable Long id, @RequestBody ReserveRequest req) {
    Item item = itemRepository.findById(id)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

    if (!item.isAvailable()) {
        throw new ResponseStatusException(HttpStatus.CONFLICT, "Item already reserved");
    }
    if (!currentUser.hasPermission("RESERVE")) {
        throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Permission denied");
    }

    item.reserve(req.getUserId());
}
```

## 응답 형태

Spring Boot의 기본 에러 처리(`BasicErrorController`)와 함께 사용하면
아래와 같은 JSON 응답이 자동으로 생성된다.

```json
{
  "timestamp": "2024-01-15T10:30:00.000+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "User not found: 42",
  "path": "/users/42"
}
```

`message` 필드 노출은 Spring Boot 2.3부터 기본적으로 비활성화됐다.
활성화하려면 `application.properties`에 아래를 추가한다.

```properties
server.error.include-message=always
```

## @ResponseStatus와 비교

| 항목             | `@ResponseStatus`      | `ResponseStatusException`  |
| ---------------- | ---------------------- | -------------------------- |
| 예외 클래스 생성 | 필요                   | 불필요                     |
| 상태 코드        | 컴파일 타임 고정       | 런타임 동적 결정 가능      |
| 재사용성         | 높음 (타입으로 구분)   | 낮음 (인라인 사용)         |
| 전역 처리        | `@ExceptionHandler`    | `@ExceptionHandler`        |
| 메시지 전달      | `reason` 속성으로 고정 | 생성자 인자로 유연하게     |

## @ExceptionHandler와 함께 쓰기

`ResponseStatusException`도 `@ExceptionHandler`로 잡아서 응답 형식을
커스터마이즈할 수 있다.

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResponseStatusException.class)
    public ResponseEntity<ErrorResponse> handleResponseStatus(
            ResponseStatusException ex) {
        ErrorResponse body = new ErrorResponse(
            ex.getStatusCode().value(),
            ex.getReason()
        );
        return ResponseEntity.status(ex.getStatusCode()).body(body);
    }
}
```

## 주의사항

`ResponseStatusException`을 남발하면 도메인 예외의 의미가 사라진다.
`UserNotFoundException` 같은 명시적 타입은 코드 전체에서 해당 상황을
검색·추적하기 쉽게 만든다. `ResponseStatusException`은 컨트롤러 레이어에서
즉각적인 HTTP 응답이 필요한 간단한 케이스에만 쓰고, 도메인 로직의 에러는
의미 있는 예외 타입으로 모델링하는 것이 낫다.
