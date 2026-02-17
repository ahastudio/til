# Spring Boot에 Sentry 도입하기

Spring Boot 애플리케이션에 Sentry를 도입하면 로그를 중앙화하고, 에러가 발생했을
때 상세한 트레이스로 빠르게 문제를 파악할 수 있습니다.

## Sentry 프로젝트 생성

Sentry에서 프로젝트를 생성하고 DSN(Data Source Name)을 발급받으세요. DSN은
`https://examplePublicKey@o0.ingest.sentry.io/0`와 같은 형식입니다. 발급받은
DSN은 애플리케이션 설정에 사용됩니다.

## 의존성 추가

Sentry Gradle Plugin을 사용하면 자동으로 적절한 의존성을 추가할 수 있습니다.

`build.gradle.kts` 파일에 Sentry Gradle Plugin을 추가합니다.

```kotlin
plugins {
    id("io.sentry.jvm.gradle") version "5.12.2"
}
```

Sentry Gradle Plugin은 Spring Boot 버전에 맞는 Starter를 자동으로 선택합니다.

- Spring Boot 2: `sentry-spring-boot-starter`
- Spring Boot 3: `sentry-spring-boot-starter-jakarta`
- Spring Boot 4: `sentry-spring-boot-4`

## 설정

`application.yml` 파일에 Sentry 설정을 추가합니다.

```yaml
sentry:
  dsn: ${SENTRY_DSN:https://examplePublicKey@o0.ingest.sentry.io/0}
  environment: ${SENTRY_ENV:development}
  send-default-pii: ${SENTRY_SEND_PII:false}
  traces-sample-rate: 1.0
  logs:
    enabled: true
```

### 주요 설정 항목

- `dsn`: Sentry 프로젝트 DSN (환경 변수 `SENTRY_DSN` 사용 권장)
- `environment`: 배포 환경 (`development`, `staging`, `production` 등)
- `send-default-pii`: 개인 식별 정보 전송 여부 (요청 헤더, IP 주소 등)
- `traces-sample-rate`: 성능 트레이스 수집 비율 (0.0~1.0, Production은 0.1~0.3
  권장)
- `logs.enabled`: 로그 자동 전송 활성화

## 로그 중앙화

여러 서버에 분산된 로그를 Sentry 대시보드에서 한꺼번에 모아 볼 수 있습니다.

`logs.enabled: true` 설정을 추가하면 [SLF4J](https://www.slf4j.org/) 로그가
자동으로 Sentry에 전송됩니다. 기본적으로 WARN 레벨 이상의 로그만 Sentry 이벤트로
기록되며, 모든 레벨의 로그는 Breadcrumb으로 수집됩니다.

### 로그 사용 예시

일반적인 로깅을 하면 Sentry SDK가 로그를 캡처합니다.

```java
@Slf4j
@RestController
public class UserController {
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        log.info("Fetching user: {}", id);

        User user = userService.findById(id);
        if (user == null) {
            log.error("User not found: {}", id);
            throw new UserNotFoundException(id);
        }

        return user;
    }
}
```

- `log.info`는 Breadcrumb으로만 기록됩니다.
- `log.error`는 Sentry 이벤트로 기록되며, 알림도 발송됩니다.

예외가 발생하면 스택 트레이스가 자동으로 Sentry에 전송됩니다.

## Trace로 문제 파악하기

Sentry의 가장 강력한 기능은 상세한 트레이스 정보입니다. 에러가 발생하면 다음과
같은 정보를 제공합니다.

### 1. 스택 트레이스

예외가 발생한 정확한 위치와 호출 스택을 확인할 수 있습니다. 소스 코드 링크가
함께 제공되어 빠르게 문제 지점으로 이동할 수 있습니다.

### 2. Breadcrumbs

에러가 발생할 때까지의 로그, HTTP 요청, 데이터베이스 쿼리 등을 시간순으로
보여줍니다. 이를 통해 에러 발생 전후의 상황을 쉽게 파악할 수 있습니다.

```java
@Service
public class PaymentService {
    public void processPayment(Long orderId, BigDecimal amount) {
        log.info("Starting payment process for order: {}", orderId);

        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        log.info("Order found: {}, amount: {}", order.getId(), amount);

        // 결제가 실패하면 PaymentException 예외를 던진다고 가정합니다.
        paymentGateway.charge(order, amount);

        log.info("Payment successful for order: {}", orderId);
    }
}
```

`paymentGateway.charge`에서 예외가 발생하면 Sentry에 다음과 같은 Breadcrumbs가
기록됩니다.

- “Starting payment process for order: 123”
- “Order found: 123, amount: 49.99”
- 예외 스택 트레이스

결제 실패 원인을 Breadcrumbs를 통해 단계별로 추적할 수 있습니다.

### 3. 컨텍스트 정보

에러 발생 시점의 다양한 컨텍스트를 자동으로 수집합니다.

- **HTTP 요청 정보**: URL, Method, Headers, Query Params
- **사용자 정보**: IP, User-Agent, 인증된 사용자 ID
- **서버 정보**: 환경 변수, JVM 정보, 서버 이름

### 4. 커스텀 컨텍스트 추가

추가 정보를 직접 기록할 수 있습니다.

```java
import io.sentry.Sentry;

@Service
public class OrderService {
    public void createOrder(OrderRequest request) {
        Sentry.configureScope(scope -> {
            scope.setTag("order-type", request.getType());
            scope.setExtra("item-count", request.getItems().size());
            scope.setUser(User.builder()
                .id(request.getUserId().toString())
                .email(request.getUserEmail())
                .build());
        });

        // 주문 처리 로직
        processOrder(request);
    }
}
```

추가한 정보는 Sentry 대시보드에서 에러와 함께 표시되어 문제 진단에 도움을
줍니다.

## 결론

Spring Boot에 Sentry를 도입하면 분산된 로그를 중앙에서 관리하고 상세한
트레이스로 문제를 빠르게 파악할 수 있습니다. Stack Trace, Breadcrumbs, Context
정보를 통해 에러의 원인을 정확히 진단하고, 실시간 알림으로 신속하게 대응할 수
있습니다.

Slack 등 다양한 알림 채널과도 연동할 수 있어, 팀 전체가 에러 상황을 즉시
공유하고 협력을 촉진할 수 있다는 점도 Sentry의 큰 장점입니다.

## 참고 링크

- Sentry Gradle Plugin: <https://docs.sentry.io/platforms/java/gradle/>
- Sentry for Spring Boot:
  <https://docs.sentry.io/platforms/java/guides/spring-boot/>
