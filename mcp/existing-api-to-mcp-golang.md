# Go 언어로 기존 API를 MCP 서버로 연결하기

## 목차

- [소개](#소개)
- [구조](#구조)
- [흐름](#흐름)
- [Outside-in TDD로 두 서버를 함께 만들기](#outside-in-tdd로-두-서버를-함께-만들기)
- [기존 API 서버: Spring Boot](#기존-api-서버-spring-boot)
- [MCP 서버: Go 언어](#mcp-서버-go-언어)
- [설정](#설정)
- [트레이드오프](#트레이드오프)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)

## 소개

이 글은 access token과 refresh token으로 로그인하는 기존 API를
Go 언어로 만든 MCP 서버로 AI 클라이언트에 연결하는 방법을 다룬다.
MCP 서버는 도구, 리소스, 프롬프트를 제공할 수 있는데,
기존 API를 연결할 때 중심이 되는 것은 LLM이
호출하는 함수인 도구다.[^build-server]

방법은 하나로 정한다.
기존 API 서버가 MCP 연결마다 오래 사는 키 `APP_MCP_KEY`를 발급하고,
MCP 서버는 이 키로 수명 30초짜리 access token을 받아 기존 API를 부른다.
기존 API는 지금처럼 access token만 검증하면 되고,
refresh token 회전이나 분산 잠금 같은 문제는 MCP 서버에 생기지 않는다.

예제는 두 서버를 함께 만든다.
기존 API 서버는 Spring Boot 4.1.1과 Spring Data JPA로,
MCP 서버는 공식 MCP Go SDK v1.8.0으로 작성했다.[^go-sdk]
두 서버를 잇는 종단 간 테스트에서 출발하는 Outside-in TDD로 짰고,
Go 언어 테스트 11개와 Spring Boot 테스트 6개가 모두 통과한다.

## 구조

```text
[AI 클라이언트] ──MCP access token──▶ [MCP 서버] ──APP_MCP_KEY──▶ POST /mcp-keys/token
                (원격 모드만, OAuth)            │                      → 30초 access token
                                                └──30초 access token──▶ 기존 API (GET /me 등)
```

| 자격 증명         | 구간                     | 발급자        | 수명                           |
| ----------------- | ------------------------ | ------------- | ------------------------------ |
| MCP access token  | AI 클라이언트 → MCP 서버 | MCP 인가 서버 | MCP 명세를 따름                |
| `APP_MCP_KEY`     | MCP 서버 → 기존 서버     | 기존 서버     | 회전 없음, 폐기·90일 유휴 만료 |
| 짧은 access token | MCP 서버 → 기존 API      | 기존 서버     | 30초                           |

로컬 stdio 서버는 사용자 한 명의 키를 환경 변수로 받는다.
원격 Streamable HTTP 서버는 MCP 명세의 인가를 따라
MCP access token으로 사용자를 구분하고, 사용자별 키를 보관한다.[^authz]
MCP 서버는 자기 앞으로 발급된 MCP access token만 받아야 하고,
그 토큰을 기존 API에 그대로 넘기는 토큰 통과는 금지된다.[^authz][^security]
기존 API에 쓰는 것은 키로 따로 받은 짧은 access token이다.

키는 `appk_<키ID>_<비밀>` 형식이다.
접두사는 유출된 키를 비밀 스캐너가 찾기 쉽게 하고,
키 ID로 행을 바로 찾으며, 비밀은 해시로만 저장한다.

## 흐름

1. 사용자가 기존 웹에 로그인한 상태에서 `POST /mcp-keys`를 부른다.
   서버는 키를 만들어 평문을 한 번만 돌려주고 DB에는 해시만 남긴다.
2. 사용자가 키를 MCP 클라이언트 설정(로컬) 또는 연결 화면(원격)에 넣는다.
3. MCP 서버가 도구 호출을 받으면 `POST /mcp-keys/token`으로 30초 access token을 받는다.
   만료 5초 전까지는 같은 토큰을 재사용하고, 같은 사용자의 동시 호출은 교환 한 번을 나눠 쓴다.
4. 기존 API가 401을 주면 한 번만 새로 교환해 다시 시도한다.
5. 사용자가 `DELETE /mcp-keys/{id}`로 폐기하면 다음 교환부터 401이 나고,
   도구는 새 키를 만들라는 안내를 돌려준다.
   이미 받은 토큰은 최대 30초까지 살아 있다.

## Outside-in TDD로 두 서버를 함께 만들기

테스트는 바깥에서 안으로 쓴다.
가장 바깥은 MCP 클라이언트, Go 언어 MCP 서버,
실제 Spring Boot 서버를 모두 잇는 종단 간 테스트다.
그 시나리오가 두 서버 사이의 HTTP 계약을 정하고,
계약은 양쪽에서 따로 확인한다.
Spring Boot 쪽은 실제 서버를 띄운 인수 테스트로,
Go 언어 쪽은 같은 계약을 흉내 낸 가짜 API로 확인한다.
가장 안쪽은 키 저장과 토큰 재사용 규칙의 단위 테스트다.

| 층      | 테스트                                                                                                                                  | 확인하는 것                                                             |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 종단 간 | `TestE2EUserConnectsKeyAndAgentReadsProfile` (Go)                                                                                       | 로그인 → 키 발급 → 도구 호출 성공 → 폐기 → 새 키 안내                   |
| 계약    | `keyIssuedByLoggedInUserIsExchangedForShortTokenThatCallsExistingApi` (Spring)                                                          | 키를 30초 토큰으로 바꾸고 그 토큰으로 기존 API를 부른다                 |
| 계약    | `revokedKeyIsRejected`, `wrongSecretIsRejected` (Spring)                                                                                | 폐기된 키와 위조한 키는 401                                             |
| 계약    | `TestToolCallsExistingAPIWithMCPKey` (Go)                                                                                               | 키로 교환해 도구가 프로필을 돌려준다                                    |
| 계약    | `TestTokenIsReusedWithinItsLifetime` (Go)                                                                                               | 수명 안에서는 다시 교환하지 않는다                                      |
| 계약    | `TestConcurrentCallsShareOneExchange` (Go)                                                                                              | 동시 호출 20개가 교환 하나를 나눠 쓴다                                  |
| 계약    | `TestRevokedKeyAsksUserForNewKey`, `TestMissingKeyAsksUserForKey` (Go)                                                                  | 키가 없거나 거부되면 발급 안내를 도구 오류로 준다                       |
| 안쪽    | `storesOnlyHashOfSecret`, `idleKeyExpires`, `exchangeRecordsLastUse` (Spring)                                                           | 해시 저장, 90일 유휴 만료, 마지막 사용 시각                             |
| 안쪽    | `TestTokenIsReusedUntilFiveSecondsBeforeExpiry`, `TestUpstream401TriggersOneReexchange`, `TestCheckKeyRejectsUnknownKey` (Go, `appapi`) | 만료 5초 전까지 재사용한 뒤 재교환, 401 뒤 한 번 재교환, 모르는 키 거부 |
| 안쪽    | `TestLinkerSavesOnlyWorkingKey` (Go, `linking`)                                                                                         | 원격 연결 화면이 틀린 키는 거부하고 맞는 키만 저장한다                  |
| 안쪽    | `TestAudienceAcceptsStringOrArray` (Go, `mcpauth`)                                                                                      | `aud`가 문자열이든 배열이든 이 서버를 찾는다                            |

종단 간 테스트는 처음에 실패했다.
키를 폐기한 직후에도 도구 호출이 성공했기 때문이다.
이미 받은 30초 토큰이 아직 유효했고, 이것은 설계가 받아들인 폐기 지연이다.
테스트는 이 동작을 숨기지 않고 “다음 교환부터 막힌다”로 고쳐 적었다.

종단 간 테스트는 다음처럼 돌린다.

```bash
# 기존 API 서버
./gradlew bootRun --args='--server.port=18080'

# MCP 서버 (다른 터미널)
APP_E2E_URL=http://localhost:18080 go test -race ./...
```

```go
// e2e_test.go
package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
	"strings"
	"testing"
)

// 가장 바깥 테스트: MCP 클라이언트 → 이 MCP 서버 → 실제 Spring Boot 서버.
// Spring Boot 서버를 띄우고 APP_E2E_URL을 주면 돈다. 없으면 건너뛴다.
//
//	./gradlew bootRun --args='--server.port=18080'
//	APP_E2E_URL=http://localhost:18080 go test -run E2E ./...
func TestE2EUserConnectsKeyAndAgentReadsProfile(t *testing.T) {
	base := os.Getenv("APP_E2E_URL")
	if base == "" {
		t.Skip("APP_E2E_URL not set")
	}
	userToken := postJSON(t, base+"/login", "", `{"userId":"mark"}`)["accessToken"]
	key := postJSON(t, base+"/mcp-keys", userToken, `{"name":"Claude MCP"}`)["key"]

	assertText(t, callTool(t, connect(t, localServer(base, key))), `{"name":"mark"}`)

	// 폐기는 다음 교환부터 막힌다. 이미 받은 토큰은 최대 30초까지 산다.
	// 그래서 새로 교환하는 서버(재시작한 MCP 서버)로 확인한다.
	revoke(t, base, userToken, strings.Split(key, "_")[1])
	assertToolError(t, callTool(t, connect(t, localServer(base, key))), "APP_MCP_KEY")
}

func postJSON(t *testing.T, url, bearer, body string) map[string]string {
	t.Helper()
	req, _ := http.NewRequest(http.MethodPost, url, bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	if bearer != "" {
		req.Header.Set("Authorization", "Bearer "+bearer)
	}
	res, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer res.Body.Close()
	var out map[string]string
	if err := json.NewDecoder(res.Body).Decode(&out); err != nil {
		t.Fatalf("%s: %v", url, err)
	}
	return out
}

func revoke(t *testing.T, base, bearer, keyID string) {
	t.Helper()
	req, _ := http.NewRequest(http.MethodDelete, base+"/mcp-keys/"+keyID, nil)
	req.Header.Set("Authorization", "Bearer "+bearer)
	res, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	res.Body.Close()
}
```

## 기존 API 서버: Spring Boot

### 추가하는 것

| 엔드포인트              | 인증                  | 하는 일                                 |
| ----------------------- | --------------------- | --------------------------------------- |
| `POST /mcp-keys`        | 사용자의 access token | 키 발급. 평문은 응답으로 한 번만 나간다 |
| `GET /mcp-keys`         | 사용자의 access token | 내 키 목록                              |
| `DELETE /mcp-keys/{id}` | 사용자의 access token | 폐기                                    |
| `POST /mcp-keys/token`  | 키 자체               | 30초 access token 발급                  |

access token 발급은 `AccessTokenIssuer` 인터페이스와
`McpKeyService.issueAccessToken` 메서드 하나로 모았다.
이미 JWT 발급기가 있다면 인터페이스 구현만 그것으로 바꾸고,
토큰에 넣을 클레임(키 ID, 권한 등)을 바꿀 때는 `issueAccessToken`만 고친다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-webmvc'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    runtimeOnly 'com.h2database:h2'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.springframework.boot:spring-boot-resttestclient'
    testImplementation 'org.springframework.boot:spring-boot-restclient'
    testImplementation 'org.springframework.boot:spring-boot-starter-data-jpa-test'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}
```

```java
// auth/AccessTokenIssuer.java
package com.example.app.auth;

import java.time.Duration;
import java.util.Optional;

// 기존 서버의 access token 발급과 검증을 한곳으로 모은 경계.
// 이미 JWT 발급기가 있다면 이 인터페이스의 구현만 그것으로 바꾼다.
public interface AccessTokenIssuer {

    String issue(String userId, String scope, Duration ttl);

    Optional<TokenPrincipal> resolve(String token);

    record TokenPrincipal(String userId, String scope) {}
}
```

시간은 `Clock` 빈으로 주입해 테스트에서 유휴 만료를 앞당길 수 있게 한다.

```java
// ClockConfig.java
package com.example.app;

import java.time.Clock;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
class ClockConfig {
    @Bean
    Clock clock() {
        return Clock.systemUTC();
    }
}
```

```java
// mcpkey/McpKey.java
package com.example.app.mcpkey;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import java.time.Instant;

// MCP 연결 하나. 평문 키는 저장하지 않고 비밀의 해시만 둔다.
@Entity
public class McpKey {

    @Id
    private String id; // 키에 그대로 들어가는 키 ID

    private String userId;
    private String name;
    private String secretHash;
    private String scope;
    private Instant createdAt;
    private Instant lastUsedAt;
    private Instant revokedAt;

    protected McpKey() {}

    McpKey(String id, String userId, String name, String secretHash, String scope, Instant now) {
        this.id = id;
        this.userId = userId;
        this.name = name;
        this.secretHash = secretHash;
        this.scope = scope;
        this.createdAt = now;
        this.lastUsedAt = now;
    }

    boolean usableAt(Instant now, java.time.Duration idleExpiry) {
        return revokedAt == null && now.isBefore(lastUsedAt.plus(idleExpiry));
    }

    void markUsed(Instant now) { this.lastUsedAt = now; }

    void revoke(Instant now) { this.revokedAt = now; }

    public String getId() { return id; }
    public String getUserId() { return userId; }
    public String getName() { return name; }
    public String getSecretHash() { return secretHash; }
    public String getScope() { return scope; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getLastUsedAt() { return lastUsedAt; }
    public Instant getRevokedAt() { return revokedAt; }
}
```

```java
// mcpkey/McpKeyRepository.java
package com.example.app.mcpkey;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface McpKeyRepository extends JpaRepository<McpKey, String> {
    List<McpKey> findByUserIdAndRevokedAtIsNull(String userId);
}
```

```java
// mcpkey/McpKeyRejectedException.java
package com.example.app.mcpkey;

// 키가 없거나, 틀렸거나, 폐기되었거나, 오래 쓰지 않아 만료되었다. 응답은 모두 401로 같다.
public class McpKeyRejectedException extends RuntimeException {}
```

```java
// mcpkey/McpKeyService.java
package com.example.app.mcpkey;

import com.example.app.auth.AccessTokenIssuer;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.time.Clock;
import java.time.Duration;
import java.util.Base64;
import java.util.HexFormat;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class McpKeyService {

    static final String PREFIX = "appk";
    static final String SCOPE = "profile:read";           // MCP에 필요한 최소 권한
    static final Duration TOKEN_TTL = Duration.ofSeconds(30); // 아주 짧게
    static final Duration IDLE_EXPIRY = Duration.ofDays(90);

    private final McpKeyRepository repository;
    private final AccessTokenIssuer issuer;
    private final Clock clock;
    private final SecureRandom random = new SecureRandom();

    public McpKeyService(McpKeyRepository repository, AccessTokenIssuer issuer, Clock clock) {
        this.repository = repository;
        this.issuer = issuer;
        this.clock = clock;
    }

    /** 로그인한 사용자가 키를 만든다. 평문은 이 반환값으로 한 번만 나간다. */
    @Transactional
    public String issue(String userId, String name) {
        String id = randomHex(6);
        String secret = randomSecret();
        repository.save(new McpKey(id, userId, name, sha256(secret), SCOPE, clock.instant()));
        return PREFIX + "_" + id + "_" + secret;
    }

    /** 키를 아주 짧은 access token으로 바꾼다. 실패 이유는 밖으로 구분하지 않는다. */
    @Transactional
    public ShortToken exchange(String rawKey) {
        McpKey key = verify(rawKey);
        key.markUsed(clock.instant());
        return issueAccessToken(key);
    }

    /** access token 발급만 따로 둔다. 기존 발급 코드에 맞출 때 이 메서드만 고친다. */
    ShortToken issueAccessToken(McpKey key) {
        String token = issuer.issue(key.getUserId(), key.getScope(), TOKEN_TTL);
        return new ShortToken(token, TOKEN_TTL.toSeconds());
    }

    @Transactional
    public void revoke(String userId, String keyId) {
        repository.findById(keyId)
                .filter(k -> k.getUserId().equals(userId))
                .ifPresent(k -> k.revoke(clock.instant()));
    }

    public List<McpKey> list(String userId) {
        return repository.findByUserIdAndRevokedAtIsNull(userId);
    }

    private McpKey verify(String rawKey) {
        String[] parts = rawKey == null ? new String[0] : rawKey.split("_", 3);
        if (parts.length != 3 || !parts[0].equals(PREFIX)) {
            throw new McpKeyRejectedException();
        }
        McpKey key = repository.findById(parts[1]).orElseThrow(McpKeyRejectedException::new);
        boolean secretMatches = MessageDigest.isEqual(
                key.getSecretHash().getBytes(StandardCharsets.US_ASCII),
                sha256(parts[2]).getBytes(StandardCharsets.US_ASCII));
        if (!secretMatches || !key.usableAt(clock.instant(), IDLE_EXPIRY)) {
            throw new McpKeyRejectedException();
        }
        return key;
    }

    private String randomHex(int bytes) {
        byte[] b = new byte[bytes];
        random.nextBytes(b);
        return HexFormat.of().formatHex(b);
    }

    private String randomSecret() {
        byte[] b = new byte[32];
        random.nextBytes(b);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(b).replace('_', '-');
    }

    private static String sha256(String s) {
        try {
            byte[] d = MessageDigest.getInstance("SHA-256").digest(s.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(d);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }

    public record ShortToken(String accessToken, long expiresIn) {}
}
```

```java
// mcpkey/McpKeyController.java
package com.example.app.mcpkey;

import com.example.app.auth.BearerAuthFilter;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestAttribute;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
class McpKeyController {

    private final McpKeyService service;

    McpKeyController(McpKeyService service) {
        this.service = service;
    }

    // 로그인한 사용자만 부른다. 기존 인증이 요청 속성에 사용자 ID를 둔다.
    @PostMapping("/mcp-keys")
    ResponseEntity<Map<String, String>> issue(@RequestAttribute(BearerAuthFilter.USER_ID) String userId,
                                              @RequestBody Map<String, String> body) {
        String key = service.issue(userId, body.getOrDefault("name", "MCP"));
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("key", key));
    }

    @GetMapping("/mcp-keys")
    List<Map<String, Object>> list(@RequestAttribute(BearerAuthFilter.USER_ID) String userId) {
        return service.list(userId).stream()
                .map(k -> Map.<String, Object>of("id", k.getId(), "name", k.getName(), "lastUsedAt", k.getLastUsedAt()))
                .toList();
    }

    @DeleteMapping("/mcp-keys/{id}")
    ResponseEntity<Void> revoke(@RequestAttribute(BearerAuthFilter.USER_ID) String userId, @PathVariable String id) {
        service.revoke(userId, id);
        return ResponseEntity.noContent().build();
    }

    // MCP 서버가 부른다. 사용자 인증 없이 키 자체로 인증한다.
    @PostMapping("/mcp-keys/token")
    McpKeyService.ShortToken token(@RequestBody Map<String, String> body) {
        return service.exchange(body.get("key"));
    }

    @ExceptionHandler(McpKeyRejectedException.class)
    ResponseEntity<Void> rejected() {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
    }
}
```

### 예제용 대역

아래 세 파일은 기존 서버에 이미 있는 것을 흉내 낸 예제다.
실제 서버에서는 기존 JWT 발급기, 인증 필터, 로그인과 API가 이 자리에 있다.

```java
// auth/InMemoryAccessTokenIssuer.java
package com.example.app.auth;

import java.security.SecureRandom;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.HexFormat;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Component;

// 예제용 구현. 운영에서는 기존 JWT 발급기로 바꾼다.
@Component
public class InMemoryAccessTokenIssuer implements AccessTokenIssuer {

    private final Clock clock;
    private final SecureRandom random = new SecureRandom();
    private final Map<String, Entry> tokens = new ConcurrentHashMap<>();

    public InMemoryAccessTokenIssuer(Clock clock) {
        this.clock = clock;
    }

    @Override
    public String issue(String userId, String scope, Duration ttl) {
        byte[] b = new byte[24];
        random.nextBytes(b);
        String token = HexFormat.of().formatHex(b);
        tokens.put(token, new Entry(new TokenPrincipal(userId, scope), clock.instant().plus(ttl)));
        return token;
    }

    @Override
    public Optional<TokenPrincipal> resolve(String token) {
        Entry e = tokens.get(token);
        if (e == null || !clock.instant().isBefore(e.expiresAt())) {
            return Optional.empty();
        }
        return Optional.of(e.principal());
    }

    private record Entry(TokenPrincipal principal, Instant expiresAt) {}
}
```

```java
// auth/BearerAuthFilter.java
package com.example.app.auth;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

// 기존 인증 필터 자리. Bearer 토큰을 검증해 사용자 ID를 요청 속성에 둔다.
// Spring Security를 쓰고 있다면 그 필터 체인이 이 일을 한다.
@Component
public class BearerAuthFilter extends OncePerRequestFilter {

    public static final String USER_ID = "userId";

    private final AccessTokenIssuer issuer;

    public BearerAuthFilter(AccessTokenIssuer issuer) {
        this.issuer = issuer;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String header = req.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            issuer.resolve(header.substring(7)).ifPresent(p -> req.setAttribute(USER_ID, p.userId()));
        }
        chain.doFilter(req, res);
    }
}
```

```java
// auth/ExistingApiController.java
package com.example.app.auth;

import java.time.Duration;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestAttribute;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

// 이미 있는 로그인과 API를 흉내 낸 예제. 실제 서버에서는 기존 코드가 이 자리에 있다.
@RestController
class ExistingApiController {

    private final AccessTokenIssuer issuer;

    ExistingApiController(AccessTokenIssuer issuer) {
        this.issuer = issuer;
    }

    @PostMapping("/login")
    Map<String, String> login(@RequestBody Map<String, String> body) {
        return Map.of("accessToken", issuer.issue(body.get("userId"), "user", Duration.ofHours(1)));
    }

    @GetMapping("/me")
    ResponseEntity<Map<String, String>> me(@RequestAttribute(name = BearerAuthFilter.USER_ID, required = false) String userId) {
        if (userId == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(Map.of("name", userId));
    }
}
```

### 테스트

```java
// McpKeyApiTest.java
package com.example.app.mcpkey;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.TestRestTemplate;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureTestRestTemplate;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

// 바깥 테스트: MCP 서버가 기대하는 HTTP 계약을 실제 서버로 확인한다.
// Go 쪽 가짜 API(fake_api_test.go)가 흉내 내는 계약과 같아야 한다.
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class McpKeyApiTest {

    @Autowired TestRestTemplate http;

    @Test
    void keyIssuedByLoggedInUserIsExchangedForShortTokenThatCallsExistingApi() {
        String userToken = login("mark");
        String key = issueKey(userToken);

        Map<?, ?> token = exchange(key).getBody();

        assertThat(token.get("expiresIn")).isEqualTo(30);
        assertThat(me((String) token.get("accessToken")).getBody()).isEqualTo(Map.of("name", "mark"));
    }

    @Test
    void revokedKeyIsRejected() {
        String userToken = login("mark");
        String key = issueKey(userToken);
        String keyId = key.split("_")[1];

        http.exchange("/mcp-keys/" + keyId, HttpMethod.DELETE, new HttpEntity<>(bearer(userToken)), Void.class);

        assertThat(exchange(key).getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }

    @Test
    void wrongSecretIsRejected() {
        String key = issueKey(login("mark"));
        String forged = key.substring(0, key.lastIndexOf('_') + 1) + "forged";

        assertThat(exchange(forged).getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }

    // ---- 헬퍼 ----

    private String login(String userId) {
        return (String) http.postForObject("/login", Map.of("userId", userId), Map.class).get("accessToken");
    }

    private String issueKey(String userToken) {
        HttpEntity<Map<String, String>> req = new HttpEntity<>(Map.of("name", "Claude MCP"), bearer(userToken));
        return (String) http.postForObject("/mcp-keys", req, Map.class).get("key");
    }

    private ResponseEntity<Map> exchange(String key) {
        return http.postForEntity("/mcp-keys/token", Map.of("key", key), Map.class);
    }

    private ResponseEntity<Map> me(String accessToken) {
        return http.exchange("/me", HttpMethod.GET, new HttpEntity<>(bearer(accessToken)), Map.class);
    }

    private static HttpHeaders bearer(String token) {
        HttpHeaders h = new HttpHeaders();
        h.setBearerAuth(token);
        return h;
    }
}
```

```java
// McpKeyServiceTest.java
package com.example.app.mcpkey;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.example.app.auth.AccessTokenIssuer;
import com.example.app.auth.InMemoryAccessTokenIssuer;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;

// 안쪽 테스트: 키의 저장 방식과 만료 규칙.
@DataJpaTest
class McpKeyServiceTest {

    @Autowired McpKeyRepository repository;

    private final MutableClock clock = new MutableClock(Instant.parse("2026-10-15T00:00:00Z"));
    private final AccessTokenIssuer issuer = new InMemoryAccessTokenIssuer(clock);

    private McpKeyService service() {
        return new McpKeyService(repository, issuer, clock);
    }

    @Test
    void storesOnlyHashOfSecret() {
        String key = service().issue("mark", "Claude MCP");

        McpKey saved = repository.findAll().getFirst();
        assertThat(key).startsWith("appk_" + saved.getId() + "_");
        assertThat(saved.getSecretHash()).doesNotContain(key.substring(key.lastIndexOf('_') + 1));
    }

    @Test
    void idleKeyExpires() {
        String key = service().issue("mark", "Claude MCP");
        clock.advance(McpKeyService.IDLE_EXPIRY.plusSeconds(1));

        assertThatThrownBy(() -> service().exchange(key)).isInstanceOf(McpKeyRejectedException.class);
    }

    @Test
    void exchangeRecordsLastUse() {
        String key = service().issue("mark", "Claude MCP");
        clock.advance(Duration.ofHours(1));

        service().exchange(key);

        assertThat(repository.findAll().getFirst().getLastUsedAt()).isEqualTo(clock.instant());
    }

    static class MutableClock extends Clock {
        private Instant now;
        MutableClock(Instant now) { this.now = now; }
        void advance(Duration d) { now = now.plus(d); }
        @Override public Instant instant() { return now; }
        @Override public ZoneOffset getZone() { return ZoneOffset.UTC; }
        @Override public Clock withZone(java.time.ZoneId zone) { return this; }
    }
}
```

## MCP 서버: Go 언어

### 패키지 구조

```text
apibridge/
├── main.go, config.go          조립과 설정 (package main)
├── acceptance_test.go           바깥 테스트: MCP 클라이언트로 도구 호출
├── e2e_test.go                  가장 바깥 테스트: 실제 Spring Boot 서버
└── internal/
    ├── appapi/    기존 API 클라이언트: 키 교환, 사용자별 토큰 재사용, 401 재시도
    ├── keys/      키 출처: 환경 변수(로컬), 파일 저장소(원격)
    ├── tools/     MCP 도구 선언과 등록
    ├── linking/   키가 없을 때의 안내와 원격 연결 화면
    ├── mcpauth/   MCP access token 검증과 보호 리소스 메타데이터
    └── fakeapi/   테스트용 가짜 기존 API (Spring 쪽과 같은 계약)
```

| 패키지    | 밖으로 드러내는 것                                      | 숨기는 것                                            |
| --------- | ------------------------------------------------------- | ---------------------------------------------------- |
| `appapi`  | `Client.Get(ctx, userID, path)`, `CheckKey`, 에러 두 개 | 키 교환, 사용자별 토큰 캐시, 재사용 기준, 401 재시도 |
| `keys`    | `Env`, `FileStore`                                      | 파일 경로 처리, 권한 `0600`                          |
| `tools`   | `GetTool`, `Register`, `Profile`                        | 도구 응답 변환, 키 문제를 도구 오류로 바꾸기         |
| `linking` | `LocalHint`, `Linker`, `PendingLinks`                   | 연결 폼, 1회용 링크 만료                             |
| `mcpauth` | `Config`, `Protect`                                     | introspection 요청, audience 확인                    |

설계의 중심은 세 가지다.

첫째, 도구는 토큰을 모른다.
도구가 기대하는 것은 `tools.API`의 `Get(ctx, userID, path)` 하나뿐이고,
키를 꺼내 교환하고, 토큰을 25초 동안 재사용하고,
401이 오면 한 번 다시 교환하는 일은 모두 `appapi.Client` 안에 있다.
토큰 정책을 바꿔도 도구 코드는 그대로다.

둘째, 인터페이스는 쓰는 쪽이 정한다.
`appapi`는 `KeySource`,
`linking`은 `KeyChecker`와 `KeyStore`를 자기 필요만큼 선언하고,
`keys.FileStore`와 `appapi.Client`는 그 인터페이스를 모른 채 맞춘다.
그래서 패키지 사이의 의존은 `main`이 조립할 때만 생긴다.

셋째, 도구는 선언이다.
`GetTool{Name, Description, Path}` 하나가
기존 API의 GET 엔드포인트 하나를 도구 하나로 만든다.
기존 API의 다른 조회를 노출하려면 `tools.Register`에 한 줄을 더하면 된다.

함수는 한 가지 일만 하도록 나눴다.
`Client.Get`은 사용자 캐시를 찾고(`cacheFor`), 한 번 보내 보고(`getWith`),
401이면 무효화한 뒤 다시 보내는 흐름만 남는다.
교환은 요청 만들기(`newJSONRequest`), 보내기(`do`),
상태 해석(`tokenError`), 응답 읽기(`decodeToken`)로 나뉜다.
시계는 `appapi.WithClock` 옵션으로 주입해 테스트에서 시간을 앞당긴다.

### appapi: 기존 API 클라이언트

```go
// internal/appapi/errors.go
package appapi

import "errors"

// 사용자가 키를 새로 넣어야 풀리는 에러는 이 두 가지뿐이다.
var (
	// ErrNotLinked는 이 사용자의 APP_MCP_KEY가 아직 없다는 뜻이다.
	ErrNotLinked = errors.New("APP_MCP_KEY is not set for this user")
	// ErrKeyRejected는 기존 API 서버가 APP_MCP_KEY를 거부했다는 뜻이다(폐기, 만료, 오타).
	ErrKeyRejected = errors.New("APP_MCP_KEY was rejected")
)

// NeedsNewKey는 사용자가 키를 새로 넣어야 해결되는 에러인지 알려 준다.
func NeedsNewKey(err error) bool {
	return errors.Is(err, ErrNotLinked) || errors.Is(err, ErrKeyRejected)
}
```

```go
// internal/appapi/client.go
package appapi

import (
	"context"
	"net/http"
	"sync"
	"time"
)

// KeySource는 사용자의 APP_MCP_KEY를 돌려준다. 없으면 ErrNotLinked다.
type KeySource interface {
	Key(ctx context.Context, userID string) (string, error)
}

// Client는 MCP 서버가 기존 API를 부르는 유일한 통로다.
// 키 교환, 사용자별 토큰 재사용, 401 재시도를 모두 안에 숨긴다.
type Client struct {
	baseURL string
	http    *http.Client
	keys    KeySource
	now     func() time.Time

	mu     sync.Mutex
	caches map[string]*tokenCache
}

// Option은 테스트와 운영에서 바꿀 수 있는 부분을 연다.
type Option func(*Client)

func WithClock(now func() time.Time) Option { return func(c *Client) { c.now = now } }
func WithHTTPClient(h *http.Client) Option  { return func(c *Client) { c.http = h } }

func New(baseURL string, keys KeySource, opts ...Option) *Client {
	c := &Client{
		baseURL: baseURL,
		http:    &http.Client{Timeout: 10 * time.Second},
		keys:    keys,
		now:     time.Now,
		caches:  map[string]*tokenCache{},
	}
	for _, opt := range opts {
		opt(c)
	}
	return c
}

// Get은 사용자 대신 기존 API를 GET으로 부른다.
// 만료 전 토큰이라도 키가 폐기되면 401이 오므로, 한 번만 새로 교환해 다시 시도한다.
func (c *Client) Get(ctx context.Context, userID, path string) ([]byte, error) {
	cache := c.cacheFor(userID)
	res, err := c.getWith(ctx, cache, path)
	if err == nil && res.unauthorized() {
		cache.invalidate()
		res, err = c.getWith(ctx, cache, path)
	}
	if err != nil {
		return nil, err
	}
	return res.bodyIfOK(path)
}

// CheckKey는 키를 한 번 교환해 보아 쓸 수 있는 키인지 확인한다. 저장 전에 쓴다.
func (c *Client) CheckKey(ctx context.Context, key string) error {
	_, err := c.exchange(ctx, key)
	return err
}

func (c *Client) getWith(ctx context.Context, cache *tokenCache, path string) (response, error) {
	token, err := cache.token(ctx)
	if err != nil {
		return response{}, err
	}
	return c.send(ctx, path, token)
}

// cacheFor는 사용자마다 토큰 캐시를 하나만 만든다.
// 같은 사용자의 동시 호출이 교환 한 번을 나눠 쓰게 하는 장치다.
func (c *Client) cacheFor(userID string) *tokenCache {
	c.mu.Lock()
	defer c.mu.Unlock()
	if cache, ok := c.caches[userID]; ok {
		return cache
	}
	cache := c.newCache(userID)
	c.caches[userID] = cache
	return cache
}

func (c *Client) newCache(userID string) *tokenCache {
	return &tokenCache{now: c.now, fetch: func(ctx context.Context) (accessToken, error) {
		key, err := c.keys.Key(ctx, userID)
		if err != nil {
			return accessToken{}, err
		}
		return c.exchange(ctx, key)
	}}
}
```

```go
// internal/appapi/token.go
package appapi

import (
	"context"
	"sync"
	"time"
)

// reuseMargin보다 만료가 가까우면 새로 교환한다.
// 토큰 수명이 30초이므로 25초 동안 재사용하고, 호출 도중 만료되는 경계를 피한다.
const reuseMargin = 5 * time.Second

// accessToken은 키로 받은 아주 짧은 수명의 토큰이다.
type accessToken struct {
	value  string
	expiry time.Time
}

func (t accessToken) usableAt(now time.Time) bool {
	return t.value != "" && t.expiry.Sub(now) > reuseMargin
}

// tokenCache는 한 사용자의 토큰을 재사용하고, 쓸 수 없으면 fetch로 새로 받는다.
// 키는 회전하지 않으므로 갱신은 "키로 다시 교환"이 전부다.
type tokenCache struct {
	now   func() time.Time
	fetch func(context.Context) (accessToken, error)

	mu      sync.Mutex
	current accessToken
}

func (c *tokenCache) token(ctx context.Context) (string, error) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.current.usableAt(c.now()) {
		return c.current.value, nil
	}
	return c.refresh(ctx)
}

func (c *tokenCache) refresh(ctx context.Context) (string, error) {
	next, err := c.fetch(ctx)
	if err != nil {
		return "", err
	}
	c.current = next
	return next.value, nil
}

// invalidate는 기존 API가 401을 돌려줬을 때 부른다. 다음 호출이 새로 교환한다.
func (c *tokenCache) invalidate() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.current = accessToken{}
}
```

```go
// internal/appapi/http.go
package appapi

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const tokenPath = "/mcp-keys/token"

// exchange는 POST /mcp-keys/token으로 키를 30초 access token으로 바꾼다.
func (c *Client) exchange(ctx context.Context, key string) (accessToken, error) {
	req, err := newJSONRequest(ctx, c.baseURL+tokenPath, map[string]string{"key": key})
	if err != nil {
		return accessToken{}, err
	}
	res, err := c.do(req)
	if err != nil {
		return accessToken{}, err
	}
	if err := res.tokenError(); err != nil {
		return accessToken{}, err
	}
	return c.decodeToken(res.body)
}

func (c *Client) decodeToken(body []byte) (accessToken, error) {
	var out struct {
		AccessToken string `json:"accessToken"`
		ExpiresIn   int    `json:"expiresIn"` // 초. 서버는 30초를 준다
	}
	if err := json.Unmarshal(body, &out); err != nil {
		return accessToken{}, err
	}
	return accessToken{value: out.AccessToken, expiry: c.now().Add(time.Duration(out.ExpiresIn) * time.Second)}, nil
}

// send는 Bearer 토큰을 붙여 GET 요청을 보낸다.
func (c *Client) send(ctx context.Context, path, token string) (response, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, c.baseURL+path, nil)
	if err != nil {
		return response{}, err
	}
	req.Header.Set("Authorization", "Bearer "+token)
	return c.do(req)
}

func (c *Client) do(req *http.Request) (response, error) {
	res, err := c.http.Do(req)
	if err != nil {
		return response{}, err
	}
	defer res.Body.Close()
	body, err := io.ReadAll(res.Body)
	return response{status: res.StatusCode, body: body}, err
}

func newJSONRequest(ctx context.Context, url string, payload any) (*http.Request, error) {
	body, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	return req, nil
}

// response는 본문과 상태 코드만 남긴 응답이다. 재시도 판단과 결과 해석을 나눈다.
type response struct {
	status int
	body   []byte
}

func (r response) unauthorized() bool { return r.status == http.StatusUnauthorized }

func (r response) bodyIfOK(path string) ([]byte, error) {
	if r.status != http.StatusOK {
		return nil, fmt.Errorf("upstream %s: status %d", path, r.status)
	}
	return r.body, nil
}

// tokenError는 401과 403을 키 거부로, 그 밖의 실패를 일반 에러로 바꾼다.
func (r response) tokenError() error {
	switch {
	case r.status == http.StatusUnauthorized || r.status == http.StatusForbidden:
		return ErrKeyRejected
	case r.status != http.StatusOK:
		return fmt.Errorf("token exchange: status %d", r.status)
	default:
		return nil
	}
}
```

### keys: 키 출처

```go
// internal/keys/keys.go
package keys

import (
	"context"
	"errors"
	"os"
	"path/filepath"
	"strings"

	"apibridge/internal/appapi"
)

// Env는 로컬 모드의 키 출처다. 사용자는 한 명이고 키는 환경 변수에 있다.
type Env string

func (k Env) Key(context.Context, string) (string, error) {
	if k == "" {
		return "", appapi.ErrNotLinked
	}
	return string(k), nil
}

// FileStore는 원격 모드에서 사용자별 키를 파일로 보관한다.
// 운영에서는 KMS로 암호화한 DB 컬럼을 쓴다. 키는 회전하지 않으므로 쓰기 경합이 없다.
type FileStore struct{ Dir string }

func (s FileStore) Key(_ context.Context, userID string) (string, error) {
	b, err := os.ReadFile(s.path(userID))
	if errors.Is(err, os.ErrNotExist) {
		return "", appapi.ErrNotLinked
	}
	return strings.TrimSpace(string(b)), err
}

func (s FileStore) Save(_ context.Context, userID, key string) error {
	if err := os.MkdirAll(s.Dir, 0o700); err != nil {
		return err
	}
	return os.WriteFile(s.path(userID), []byte(key), 0o600)
}

// path는 사용자 ID에 경로 구분자가 섞여도 Dir 밖으로 나가지 못하게 한다.
func (s FileStore) path(userID string) string {
	return filepath.Join(s.Dir, filepath.Base(userID)+".key")
}
```

### tools: 선언형 도구

키가 없거나 거부되면 도구는 HTTP 401이 아니라 도구 오류로 알린다.
401을 돌려주면 클라이언트가 MCP 인가를 다시 시작하지만,
문제는 MCP access token이 아니라 `APP_MCP_KEY`이기 때문이다.

```go
// internal/tools/tools.go
package tools

import (
	"context"

	"github.com/modelcontextprotocol/go-sdk/mcp"

	"apibridge/internal/appapi"
)

// LocalUserID는 로컬 stdio 모드의 유일한 사용자다.
const LocalUserID = "local"

// API는 도구가 기존 API에 기대하는 전부다. 토큰은 신경 쓰지 않는다.
type API interface {
	Get(ctx context.Context, userID, path string) ([]byte, error)
}

// Hint는 키가 없거나 거부된 사용자에게 보여 줄 안내를 만든다.
type Hint interface {
	Hint(userID string) string
}

// GetTool은 기존 API의 GET 엔드포인트 하나를 MCP 도구 하나로 선언한다.
// 도구를 늘릴 때는 이 목록에 한 줄을 더한다.
type GetTool struct {
	Name        string
	Description string
	Path        string
}

var Profile = GetTool{
	Name:        "get_profile",
	Description: "Get the signed-in user's profile from the upstream API",
	Path:        "/me",
}

type noInput struct{}

// Register는 선언된 도구들을 서버에 붙인다.
func Register(s *mcp.Server, api API, hint Hint, defs ...GetTool) {
	for _, def := range defs {
		mcp.AddTool(s, &mcp.Tool{Name: def.Name, Description: def.Description}, handlerFor(def, api, hint))
	}
}

func handlerFor(def GetTool, api API, hint Hint) mcp.ToolHandlerFor[noInput, any] {
	return func(ctx context.Context, req *mcp.CallToolRequest, _ noInput) (*mcp.CallToolResult, any, error) {
		userID := userIDFrom(req)
		body, err := api.Get(ctx, userID, def.Path)
		return resultFor(body, err, func() string { return hint.Hint(userID) })
	}
}

// resultFor는 결과를 도구 응답으로 옮긴다.
// 키 문제는 HTTP 401이 아니라 도구 오류로 알린다.
// 401을 돌려주면 클라이언트가 MCP 인가를 다시 시작하지만, 문제는 MCP access token이 아니라 APP_MCP_KEY다.
func resultFor(body []byte, err error, hint func() string) (*mcp.CallToolResult, any, error) {
	switch {
	case appapi.NeedsNewKey(err):
		return toolError(hint()), nil, nil
	case err != nil:
		return nil, nil, err
	default:
		return toolText(string(body)), nil, nil
	}
}

// userIDFrom은 원격 모드에서 MCP access token의 사용자 ID를 꺼낸다.
func userIDFrom(req *mcp.CallToolRequest) string {
	if req.Extra != nil && req.Extra.TokenInfo != nil {
		return req.Extra.TokenInfo.UserID
	}
	return LocalUserID
}

func toolError(msg string) *mcp.CallToolResult {
	return &mcp.CallToolResult{IsError: true, Content: []mcp.Content{&mcp.TextContent{Text: msg}}}
}

func toolText(text string) *mcp.CallToolResult {
	return &mcp.CallToolResult{Content: []mcp.Content{&mcp.TextContent{Text: text}}}
}
```

### linking: 안내와 원격 연결 화면

```go
// internal/linking/linking.go
package linking

import (
	"context"
	"fmt"
	"html/template"
	"net/http"
	"net/url"
)

// LocalHint는 로컬 모드의 안내다. 사용자는 키를 만들어 MCP 클라이언트 설정에 넣는다.
type LocalHint struct{ IssuePage string }

func (h LocalHint) Hint(string) string {
	return "APP_MCP_KEY is missing or revoked. Create one at " + h.IssuePage +
		" and set it in the MCP client's env, then retry."
}

// KeyChecker는 저장하기 전에 키가 쓸 수 있는지 확인한다.
type KeyChecker interface {
	CheckKey(ctx context.Context, key string) error
}

// KeyStore는 사용자별 키를 저장한다.
type KeyStore interface {
	Save(ctx context.Context, userID, key string) error
}

// Linker는 원격 모드에서 MCP 사용자와 APP_MCP_KEY를 잇는다.
// 도구가 1회용 링크를 안내하고, 사용자는 그 화면에 새로 만든 키를 붙여 넣는다.
//
// 주의: 운영에서는 이 화면을 연 브라우저 사용자를 MCP 인가 서버로 다시 확인해야 한다.
type Linker struct {
	BaseURL   string
	IssuePage string
	Checker   KeyChecker
	Store     KeyStore
	Links     *PendingLinks
}

func (l *Linker) Hint(userID string) string {
	return "APP_MCP_KEY is not connected. Ask the user to open this link, then retry: " + l.linkFor(userID)
}

func (l *Linker) linkFor(userID string) string {
	return l.BaseURL + "/connect?nonce=" + url.QueryEscape(l.Links.Add(userID))
}

func (l *Linker) Routes(mux *http.ServeMux) {
	mux.HandleFunc("GET /connect", l.showForm)
	mux.HandleFunc("POST /connect", l.submitKey)
}

var connectForm = template.Must(template.New("connect").Parse(`<p>Create a key at <a href="{{.Issue}}">{{.Issue}}</a> and paste it here.</p>
<form method="post" action="/connect">
<input type="hidden" name="nonce" value="{{.Nonce}}">
<input name="key" type="password" autocomplete="off">
<button>Connect</button>
</form>`))

func (l *Linker) showForm(w http.ResponseWriter, r *http.Request) {
	nonce := r.URL.Query().Get("nonce")
	if _, ok := l.Links.Peek(nonce); !ok {
		http.Error(w, "link expired", http.StatusBadRequest)
		return
	}
	connectForm.Execute(w, map[string]string{"Issue": l.IssuePage, "Nonce": nonce})
}

func (l *Linker) submitKey(w http.ResponseWriter, r *http.Request) {
	nonce, key := r.PostFormValue("nonce"), r.PostFormValue("key")
	userID, ok := l.Links.Peek(nonce)
	if !ok {
		http.Error(w, "link expired", http.StatusBadRequest)
		return
	}
	if err := l.Checker.CheckKey(r.Context(), key); err != nil {
		http.Error(w, "this key was rejected", http.StatusUnauthorized) // 링크는 남겨 다시 시도하게 한다
		return
	}
	if err := l.save(r.Context(), nonce, userID, key); err != nil {
		http.Error(w, "save failed", http.StatusInternalServerError)
		return
	}
	fmt.Fprintln(w, "Connected. Return to your AI client and retry.")
}

func (l *Linker) save(ctx context.Context, nonce, userID, key string) error {
	l.Links.Remove(nonce)
	return l.Store.Save(ctx, userID, key)
}
```

```go
// internal/linking/pending.go
package linking

import (
	"crypto/rand"
	"encoding/hex"
	"sync"
	"time"
)

// PendingLinks는 아직 쓰이지 않은 1회용 링크를 사용자에 묶어 TTL 동안 보관한다.
type PendingLinks struct {
	ttl time.Duration
	now func() time.Time

	mu    sync.Mutex
	links map[string]pendingLink
}

type pendingLink struct {
	userID  string
	expires time.Time
}

func NewPendingLinks(ttl time.Duration) *PendingLinks {
	return &PendingLinks{ttl: ttl, now: time.Now, links: map[string]pendingLink{}}
}

func (p *PendingLinks) Add(userID string) string {
	p.mu.Lock()
	defer p.mu.Unlock()
	nonce := randomNonce()
	p.links[nonce] = pendingLink{userID: userID, expires: p.now().Add(p.ttl)}
	return nonce
}

func (p *PendingLinks) Peek(nonce string) (userID string, ok bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	link, found := p.links[nonce]
	return link.userID, found && p.now().Before(link.expires)
}

func (p *PendingLinks) Remove(nonce string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	delete(p.links, nonce)
}

func randomNonce() string {
	b := make([]byte, 16)
	rand.Read(b)
	return hex.EncodeToString(b)
}
```

### mcpauth: MCP access token 검증

```go
// internal/mcpauth/verifier.go
package mcpauth

import (
	"context"
	"encoding/json"
	"net/http"
	"net/url"
	"slices"
	"strings"
	"time"

	"github.com/modelcontextprotocol/go-sdk/auth"
)

// IntrospectionVerifier는 MCP 인가 서버에 토큰을 조회해(RFC 7662)
// 이 MCP 서버를 대상으로 발급된 토큰인지 확인한다.
type IntrospectionVerifier struct {
	endpoint     string
	clientID     string
	clientSecret string
	resource     string // 이 MCP 서버의 정식 URI
	http         *http.Client
}

// Config는 MCP access token을 검증하는 데 필요한 값이다.
type Config struct {
	AuthorizationServer string
	IntrospectionURL    string
	ClientID            string
	ClientSecret        string
	RequiredScopes      []string
}

func NewIntrospectionVerifier(cfg Config, resource string) *IntrospectionVerifier {
	return &IntrospectionVerifier{
		endpoint:     cfg.IntrospectionURL,
		clientID:     cfg.ClientID,
		clientSecret: cfg.ClientSecret,
		resource:     resource,
		http:         &http.Client{Timeout: 5 * time.Second},
	}
}

// Verify는 auth.TokenVerifier 시그니처를 따른다.
func (v *IntrospectionVerifier) Verify(ctx context.Context, token string, _ *http.Request) (*auth.TokenInfo, error) {
	res, err := v.introspect(ctx, token)
	if err != nil {
		return nil, err
	}
	if !res.acceptableFor(v.resource) {
		return nil, auth.ErrInvalidToken
	}
	return res.TokenInfo(), nil
}

// acceptableFor는 이 MCP 서버를 대상으로 발급된 유효한 토큰인지 확인한다.
// 다른 리소스용 토큰은 받지 않는다. 토큰 통과(passthrough) 방지의 핵심이다.
func (r *introspectionResponse) acceptableFor(resource string) bool {
	return r.Active && r.Audience.Contains(resource)
}

func (v *IntrospectionVerifier) introspect(ctx context.Context, token string) (*introspectionResponse, error) {
	req, err := v.newIntrospectionRequest(ctx, token)
	if err != nil {
		return nil, err
	}
	resp, err := v.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var res introspectionResponse
	if err := json.NewDecoder(resp.Body).Decode(&res); err != nil {
		return nil, err
	}
	return &res, nil
}

// newIntrospectionRequest는 RFC 7662 형식의 요청을 만든다. 리소스 서버 자격 증명으로 인증한다.
func (v *IntrospectionVerifier) newIntrospectionRequest(ctx context.Context, token string) (*http.Request, error) {
	form := url.Values{"token": {token}}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, v.endpoint, strings.NewReader(form.Encode()))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.SetBasicAuth(v.clientID, v.clientSecret)
	return req, nil
}

type introspectionResponse struct {
	Active   bool     `json:"active"`
	Scope    string   `json:"scope"`
	Exp      int64    `json:"exp"`
	Sub      string   `json:"sub"`
	Audience audience `json:"aud"`
}

func (r *introspectionResponse) TokenInfo() *auth.TokenInfo {
	return &auth.TokenInfo{
		UserID:     r.Sub,
		Scopes:     strings.Fields(r.Scope),
		Expiration: time.Unix(r.Exp, 0),
	}
}

// audience는 aud 클레임이 문자열 하나일 때와 배열일 때를 모두 받는다.
type audience []string

func (a *audience) UnmarshalJSON(b []byte) error {
	var one string
	if err := json.Unmarshal(b, &one); err == nil {
		*a = audience{one}
		return nil
	}
	var many []string
	if err := json.Unmarshal(b, &many); err != nil {
		return err
	}
	*a = many
	return nil
}

func (a audience) Contains(resource string) bool { return slices.Contains(a, resource) }
```

```go
// internal/mcpauth/mount.go
package mcpauth

import (
	"net/http"
	"time"

	"github.com/modelcontextprotocol/go-sdk/auth"
	"github.com/modelcontextprotocol/go-sdk/oauthex"
)

const metadataPath = "/.well-known/oauth-protected-resource"

// Protect는 보호 리소스 메타데이터(RFC 9728)를 붙이고,
// MCP access token을 검증한 뒤에만 next로 넘기는 핸들러를 돌려준다.
func Protect(mux *http.ServeMux, cfg Config, publicBaseURL, resource string, next http.Handler) http.Handler {
	mux.Handle(metadataPath, metadataHandler(cfg, resource))
	return requireToken(cfg, publicBaseURL+metadataPath, resource)(next)
}

func metadataHandler(cfg Config, resource string) http.Handler {
	return auth.ProtectedResourceMetadataHandler(&oauthex.ProtectedResourceMetadata{
		Resource:             resource,
		AuthorizationServers: []string{cfg.AuthorizationServer},
		ScopesSupported:      cfg.RequiredScopes,
	})
}

func requireToken(cfg Config, metadataURL, resource string) func(http.Handler) http.Handler {
	verifier := NewIntrospectionVerifier(cfg, resource)
	return auth.RequireBearerToken(verifier.Verify, &auth.RequireBearerTokenOptions{
		ResourceMetadataURL: metadataURL,
		Scopes:              cfg.RequiredScopes,
		ClockSkew:           30 * time.Second,
	})
}
```

### 조립과 설정

`main`은 객체를 만들어 잇기만 한다.
원격 모드는 시작할 때 필수 환경 변수가 비었는지 확인하고,
HTTP 서버에는 느린 클라이언트를 막는 타임아웃을 건다.

```go
// config.go
package main

import (
	"errors"
	"os"
	"strings"

	"apibridge/internal/mcpauth"
)

// Config는 환경 변수를 한 곳에서만 읽는다.
type Config struct {
	APIBase       string // 기존 API 서버 주소
	IssuePage     string // 사용자가 APP_MCP_KEY를 만드는 화면
	MCPKey        string // 로컬 모드의 APP_MCP_KEY
	KeyDir        string // 원격 모드에서 사용자별 키를 저장할 디렉터리
	PublicBaseURL string // 원격 모드의 이 서버 주소. 예: https://mcp.example.com
	MCPAuth       mcpauth.Config
}

func LoadConfig() Config {
	return Config{
		APIBase:       envOr("APP_HOST", "https://api.example.com"), // 서비스 주소가 하나면 기본값으로 둔다
		IssuePage:     envOr("APP_KEY_PAGE", "https://app.example.com/settings/mcp-keys/new"),
		MCPKey:        os.Getenv("APP_MCP_KEY"),
		KeyDir:        os.Getenv("KEY_DIR"),
		PublicBaseURL: strings.TrimSuffix(os.Getenv("PUBLIC_BASE_URL"), "/"),
		MCPAuth: mcpauth.Config{
			AuthorizationServer: os.Getenv("MCP_AUTH_SERVER"),
			IntrospectionURL:    os.Getenv("MCP_INTROSPECTION_URL"),
			ClientID:            os.Getenv("MCP_RS_CLIENT_ID"),
			ClientSecret:        os.Getenv("MCP_RS_CLIENT_SECRET"),
			RequiredScopes:      []string{"profile:read"},
		},
	}
}

// MCPResource는 이 MCP 서버의 정식 URI다. MCP access token의 audience와 비교한다.
func (c Config) MCPResource() string { return c.PublicBaseURL + "/mcp" }

// ValidateHTTP는 원격 모드에 꼭 필요한 값이 비었는지 시작할 때 확인한다.
func (c Config) ValidateHTTP() error {
	var missing []string
	for name, v := range map[string]string{
		"PUBLIC_BASE_URL":       c.PublicBaseURL,
		"KEY_DIR":               c.KeyDir,
		"MCP_AUTH_SERVER":       c.MCPAuth.AuthorizationServer,
		"MCP_INTROSPECTION_URL": c.MCPAuth.IntrospectionURL,
	} {
		if v == "" {
			missing = append(missing, name)
		}
	}
	if len(missing) > 0 {
		return errors.New("missing env: " + strings.Join(missing, ", "))
	}
	return nil
}

func envOr(name, fallback string) string {
	if v := os.Getenv(name); v != "" {
		return v
	}
	return fallback
}
```

```go
// main.go
package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"

	"apibridge/internal/appapi"
	"apibridge/internal/keys"
	"apibridge/internal/linking"
	"apibridge/internal/mcpauth"
	"apibridge/internal/tools"
)

// stdio 모드에서는 표준 출력이 JSON-RPC 통로다. 로그는 log 패키지(표준 에러)로만 쓴다.
func main() {
	if err := run(LoadConfig(), modeFromArgs()); err != nil {
		log.Fatal(err)
	}
}

func modeFromArgs() string {
	if len(os.Args) > 1 {
		return os.Args[1]
	}
	return "stdio"
}

func run(cfg Config, mode string) error {
	switch mode {
	case "stdio":
		return runStdio(cfg)
	case "http":
		return runHTTP(cfg)
	default:
		return errUnknownMode(mode)
	}
}

// newServer는 MCP 서버를 조립한다. 두 모드와 테스트가 모두 이것을 쓴다.
func newServer(api tools.API, hint tools.Hint) *mcp.Server {
	s := mcp.NewServer(&mcp.Implementation{Name: "apibridge", Version: "1.0.0"}, nil)
	tools.Register(s, api, hint, tools.Profile)
	return s
}

func runStdio(cfg Config) error {
	api := appapi.New(cfg.APIBase, keys.Env(cfg.MCPKey))
	server := newServer(api, linking.LocalHint{IssuePage: cfg.IssuePage})
	return server.Run(context.Background(), &mcp.StdioTransport{})
}

func runHTTP(cfg Config) error {
	if err := cfg.ValidateHTTP(); err != nil {
		return err
	}
	store := keys.FileStore{Dir: cfg.KeyDir}
	api := appapi.New(cfg.APIBase, store)
	linker := newLinker(cfg, api, store)

	server := newServer(api, linker)

	mux := http.NewServeMux()
	mcpHandler := mcp.NewStreamableHTTPHandler(func(*http.Request) *mcp.Server { return server }, nil)
	mux.Handle("/mcp", mcpauth.Protect(mux, cfg.MCPAuth, cfg.PublicBaseURL, cfg.MCPResource(), mcpHandler))
	linker.Routes(mux)
	return newHTTPServer(mux).ListenAndServe()
}

func newLinker(cfg Config, api *appapi.Client, store keys.FileStore) *linking.Linker {
	return &linking.Linker{
		BaseURL:   cfg.PublicBaseURL,
		IssuePage: cfg.IssuePage,
		Checker:   api,
		Store:     store,
		Links:     linking.NewPendingLinks(10 * time.Minute),
	}
}

// newHTTPServer는 느린 클라이언트가 연결을 붙잡지 못하게 타임아웃을 건다.
func newHTTPServer(h http.Handler) *http.Server {
	return &http.Server{Addr: ":8080", Handler: h, ReadHeaderTimeout: 10 * time.Second}
}

type errUnknownMode string

func (m errUnknownMode) Error() string { return "unknown mode " + string(m) + " (use stdio, http)" }
```

### 테스트

`fakeapi`는 테스트 전용이지만 여러 패키지의 테스트가
함께 쓰도록 일반 패키지로 둔다.

```go
// internal/fakeapi/fakeapi.go
// Package fakeapi는 테스트에서 기존 API 서버를 흉내 낸다.
// Spring Boot 쪽 인수 테스트가 확인하는 것과 같은 HTTP 계약을 따른다.
package fakeapi

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
)

const Key = "appk_7f3a9c_secret"

// Server는 POST /mcp-keys/token으로 유효한 키에 짧은 토큰을 주고,
// GET /me는 가장 최근에 발급한 토큰만 받는다.
type Server struct {
	*httptest.Server

	mu        sync.Mutex
	revoked   bool
	issued    int
	current   string
	exchanges int
}

func New(t *testing.T) *Server {
	t.Helper()
	f := &Server{}
	mux := http.NewServeMux()
	mux.HandleFunc("POST /mcp-keys/token", f.handleToken)
	mux.HandleFunc("GET /me", f.handleMe)
	f.Server = httptest.NewServer(mux)
	t.Cleanup(f.Close)
	return f
}

// Revoke는 키를 폐기한다. 이미 나간 토큰도 거부된다고 가정한다.
func (f *Server) Revoke() {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.revoked = true
	f.current = ""
}

// RejectCurrentToken은 서버가 만료 전 토큰을 거부하는 상황을 만든다.
func (f *Server) RejectCurrentToken() {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.current = "rejected-by-server"
}

func (f *Server) Exchanges() int {
	f.mu.Lock()
	defer f.mu.Unlock()
	return f.exchanges
}

func (f *Server) handleToken(w http.ResponseWriter, r *http.Request) {
	var in struct{ Key string }
	json.NewDecoder(r.Body).Decode(&in)
	f.mu.Lock()
	defer f.mu.Unlock()
	if in.Key != Key || f.revoked {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	f.exchanges++
	f.issued++
	f.current = fmt.Sprintf("at%d", f.issued)
	fmt.Fprintf(w, `{"accessToken":%q,"expiresIn":30}`, f.current)
}

func (f *Server) handleMe(w http.ResponseWriter, r *http.Request) {
	f.mu.Lock()
	ok := f.current != "" && r.Header.Get("Authorization") == "Bearer "+f.current
	f.mu.Unlock()
	if !ok {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	fmt.Fprint(w, `{"name":"mark"}`)
}
```

```go
// acceptance_test.go
package main

import (
	"context"
	"strings"
	"testing"

	"github.com/modelcontextprotocol/go-sdk/mcp"

	"apibridge/internal/appapi"
	"apibridge/internal/fakeapi"
	"apibridge/internal/keys"
	"apibridge/internal/linking"
)

// 바깥 테스트: MCP 클라이언트가 도구를 호출했을 때 사용자가 보는 결과를 검증한다.
// 진짜 MCP 클라이언트와 서버를 메모리 전송으로 잇고, 기존 API만 가짜로 둔다.

const issuePage = "https://app.example.com/settings/mcp-keys/new"

func TestToolCallsExistingAPIWithMCPKey(t *testing.T) {
	api := fakeapi.New(t)
	session := connect(t, localServer(api.URL, fakeapi.Key))

	assertText(t, callTool(t, session), `{"name":"mark"}`)
}

func TestTokenIsReusedWithinItsLifetime(t *testing.T) {
	api := fakeapi.New(t)
	session := connect(t, localServer(api.URL, fakeapi.Key))

	callTool(t, session)
	callTool(t, session)

	assertExchanges(t, api, 1)
}

func TestConcurrentCallsShareOneExchange(t *testing.T) {
	api := fakeapi.New(t)
	session := connect(t, localServer(api.URL, fakeapi.Key))

	for _, res := range callToolConcurrently(t, session, 20) {
		assertText(t, res, `{"name":"mark"}`)
	}
	assertExchanges(t, api, 1)
}

func TestRevokedKeyAsksUserForNewKey(t *testing.T) {
	api := fakeapi.New(t)
	session := connect(t, localServer(api.URL, fakeapi.Key))
	callTool(t, session)
	api.Revoke()

	assertToolError(t, callTool(t, session), "APP_MCP_KEY")
}

func TestMissingKeyAsksUserForKey(t *testing.T) {
	api := fakeapi.New(t)
	session := connect(t, localServer(api.URL, ""))

	assertToolError(t, callTool(t, session), issuePage)
}

// ---- 테스트 헬퍼 ----

func localServer(apiBase, key string) *mcp.Server {
	return newServer(appapi.New(apiBase, keys.Env(key)), linking.LocalHint{IssuePage: issuePage})
}

func connect(t *testing.T, server *mcp.Server) *mcp.ClientSession {
	t.Helper()
	ctx := context.Background()
	serverTransport, clientTransport := mcp.NewInMemoryTransports()
	if _, err := server.Connect(ctx, serverTransport, nil); err != nil {
		t.Fatal(err)
	}
	client := mcp.NewClient(&mcp.Implementation{Name: "test-client", Version: "1.0.0"}, nil)
	session, err := client.Connect(ctx, clientTransport, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { session.Close() })
	return session
}

func callTool(t *testing.T, session *mcp.ClientSession) *mcp.CallToolResult {
	t.Helper()
	res, err := session.CallTool(context.Background(), &mcp.CallToolParams{Name: "get_profile"})
	if err != nil {
		t.Fatal(err)
	}
	return res
}

func callToolConcurrently(t *testing.T, session *mcp.ClientSession, n int) []*mcp.CallToolResult {
	t.Helper()
	results := make([]*mcp.CallToolResult, n)
	errs := make(chan error, n)
	for i := range n {
		go func() {
			res, err := session.CallTool(context.Background(), &mcp.CallToolParams{Name: "get_profile"})
			results[i] = res
			errs <- err
		}()
	}
	for range n {
		if err := <-errs; err != nil {
			t.Fatal(err)
		}
	}
	return results
}

func textOf(res *mcp.CallToolResult) string {
	var b strings.Builder
	for _, c := range res.Content {
		if tc, ok := c.(*mcp.TextContent); ok {
			b.WriteString(tc.Text)
		}
	}
	return b.String()
}

func assertText(t *testing.T, res *mcp.CallToolResult, want string) {
	t.Helper()
	if res.IsError || textOf(res) != want {
		t.Fatalf("got isError=%v text=%q, want %q", res.IsError, textOf(res), want)
	}
}

func assertToolError(t *testing.T, res *mcp.CallToolResult, contains string) {
	t.Helper()
	if !res.IsError || !strings.Contains(textOf(res), contains) {
		t.Fatalf("got isError=%v text=%q, want tool error containing %q", res.IsError, textOf(res), contains)
	}
}

func assertExchanges(t *testing.T, api *fakeapi.Server, want int) {
	t.Helper()
	if got := api.Exchanges(); got != want {
		t.Fatalf("exchanges = %d, want %d", got, want)
	}
}
```

```go
// internal/appapi/client_test.go
package appapi_test

import (
	"context"
	"errors"
	"testing"
	"time"

	"apibridge/internal/appapi"
	"apibridge/internal/fakeapi"
	"apibridge/internal/keys"
)

// 안쪽 테스트: 토큰 재사용과 재교환 규칙. 시계를 바꿔 시간을 앞당긴다.

func TestTokenIsReusedUntilFiveSecondsBeforeExpiry(t *testing.T) {
	api := fakeapi.New(t)
	clock := newClock()
	client := appapi.New(api.URL, keys.Env(fakeapi.Key), appapi.WithClock(clock.now))

	mustGet(t, client)
	clock.advance(24 * time.Second) // 30초 수명에서 6초 남음: 재사용
	mustGet(t, client)
	clock.advance(2 * time.Second) // 4초 남음: 새로 교환
	mustGet(t, client)

	if got := api.Exchanges(); got != 2 {
		t.Fatalf("exchanges = %d, want 2", got)
	}
}

func TestUpstream401TriggersOneReexchange(t *testing.T) {
	api := fakeapi.New(t)
	client := appapi.New(api.URL, keys.Env(fakeapi.Key))
	mustGet(t, client)
	api.RejectCurrentToken()

	mustGet(t, client)

	if got := api.Exchanges(); got != 2 {
		t.Fatalf("exchanges = %d, want 2", got)
	}
}

func TestCheckKeyRejectsUnknownKey(t *testing.T) {
	api := fakeapi.New(t)
	client := appapi.New(api.URL, keys.Env(""))

	err := client.CheckKey(context.Background(), "appk_wrong_key")

	if !errors.Is(err, appapi.ErrKeyRejected) {
		t.Fatalf("err = %v, want ErrKeyRejected", err)
	}
}

type clock struct{ t time.Time }

func newClock() *clock                   { return &clock{t: time.Unix(1_800_000_000, 0)} }
func (c *clock) now() time.Time          { return c.t }
func (c *clock) advance(d time.Duration) { c.t = c.t.Add(d) }

func mustGet(t *testing.T, client *appapi.Client) {
	t.Helper()
	if _, err := client.Get(context.Background(), "local", "/me"); err != nil {
		t.Fatal(err)
	}
}
```

```go
// internal/linking/linking_test.go
package linking_test

import (
	"context"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"
	"time"

	"apibridge/internal/appapi"
	"apibridge/internal/fakeapi"
	"apibridge/internal/keys"
	"apibridge/internal/linking"
)

// 원격 연결 화면은 틀린 키를 거부하고, 맞는 키만 저장한다.
func TestLinkerSavesOnlyWorkingKey(t *testing.T) {
	api := fakeapi.New(t)
	store := keys.FileStore{Dir: t.TempDir()}
	linker := &linking.Linker{
		BaseURL:   "https://mcp.example.com",
		IssuePage: "https://app.example.com/settings/mcp-keys/new",
		Checker:   appapi.New(api.URL, store),
		Store:     store,
		Links:     linking.NewPendingLinks(10 * time.Minute),
	}
	mux := http.NewServeMux()
	linker.Routes(mux)
	nonce := nonceFrom(t, linker.Hint("u1"))

	if code := submit(mux, nonce, "appk_wrong_key"); code != http.StatusUnauthorized {
		t.Fatalf("wrong key: status %d, want 401", code)
	}
	if code := submit(mux, nonce, fakeapi.Key); code != http.StatusOK {
		t.Fatalf("valid key: status %d, want 200", code)
	}
	if body, err := appapi.New(api.URL, store).Get(context.Background(), "u1", "/me"); err != nil || string(body) != `{"name":"mark"}` {
		t.Fatalf("got %q, %v", body, err)
	}
}

func nonceFrom(t *testing.T, hint string) string {
	t.Helper()
	i := strings.Index(hint, "nonce=")
	if i < 0 {
		t.Fatalf("no link in %q", hint)
	}
	nonce, _ := url.QueryUnescape(hint[i+len("nonce="):])
	return nonce
}

func submit(h http.Handler, nonce, key string) int {
	form := url.Values{"nonce": {nonce}, "key": {key}}
	req := httptest.NewRequest(http.MethodPost, "/connect", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, req)
	return rec.Code
}
```

```go
// internal/mcpauth/verifier_test.go
package mcpauth

import (
	"encoding/json"
	"testing"
)

// aud 클레임은 문자열 하나일 수도 배열일 수도 있다. 둘 다 이 서버를 찾아야 한다.
func TestAudienceAcceptsStringOrArray(t *testing.T) {
	for _, raw := range []string{`"https://mcp.example.com/mcp"`, `["x","https://mcp.example.com/mcp"]`} {
		var a audience
		if err := json.Unmarshal([]byte(raw), &a); err != nil || !a.Contains("https://mcp.example.com/mcp") {
			t.Fatalf("%s: got %v, %v", raw, a, err)
		}
	}
}
```

## 설정

로컬 모드는 키 하나만 넣는다.
서비스 주소가 하나라면 바이너리의 기본값을 쓰고,
개발이나 스테이징에서만 `APP_HOST`로 덮어쓴다.

```json
{
  "mcpServers": {
    "app": {
      "command": "/ABSOLUTE/PATH/TO/apibridge",
      "args": ["stdio"],
      "env": {
        "APP_MCP_KEY": "appk_7f3a9c_..."
      }
    }
  }
}
```

원격 모드는 MCP 인가 서버 정보와 키 저장 위치를 준다.

```bash
export PUBLIC_BASE_URL=https://mcp.example.com
export MCP_AUTH_SERVER=https://auth.example.com
export MCP_INTROSPECTION_URL=https://auth.example.com/oauth/introspect
export MCP_RS_CLIENT_ID=...
export MCP_RS_CLIENT_SECRET=...
export KEY_DIR=/var/lib/apibridge/keys
export APP_KEY_PAGE=https://app.example.com/settings/mcp-keys/new   # 안내에 넣을 키 발급 화면
./apibridge http
```

## 트레이드오프

### 토큰 수명이 짧을수록 폐기는 빠르고 교환은 잦다

30초 토큰은 키를 폐기한 뒤 최대 30초까지 기존 API를 부를 수 있다.
더 줄이면 폐기는 빨라지지만 교환이 늘고,
MCP 서버와 기존 서버의 시계가 몇 초만 어긋나도 받은 토큰이 바로 만료로 보인다.
예제는 만료 5초 전까지만 재사용해 이 경계를 피한다.
즉시 폐기가 꼭 필요하다면 토큰에 키 ID를 넣고
기존 API가 폐기된 키 ID를 확인하게 해야 하는데, 그만큼 매 요청이 무거워진다.

### 회전하지 않는 키는 단순하지만 유출에 약하다

refresh token 회전은 이미 쓴 토큰이 다시 들어오는 것으로 도난을 감지한다.
회전하지 않는 키는 그 감지가 없다.
대신 해시 저장, 연결별 폐기, 90일 유휴 만료, 마지막 사용 시각 기록,
그리고 MCP에 필요한 최소 권한만 가진 토큰으로 피해 범위를 줄인다.
원격 모드라면 교환 엔드포인트가 MCP 서버의 출처(클라이언트 인증이나 고정 IP)까지
확인하게 해서, 키만 새어 나가서는 쓸 수 없게 만드는 편이 좋다.

### 원격 연결 화면은 사용자가 키를 붙여 넣는다

예제의 원격 연결 화면은 사용자가 기존 웹에서 만든 키를 붙여 넣는 방식이다.
가장 단순하지만 키가 클립보드를 지나간다.
연결 화면에서 기존 웹 로그인으로 돌아가
MCP 서버가 사용자를 대신해 `POST /mcp-keys`를
부르게 하면 붙여 넣기가 사라지지만,
기존 웹에 리디렉션과 1회용 코드가 필요해진다.

## 체크리스트

- [ ] DB에 키 평문이 아니라 비밀의 해시만 있는가
- [ ] 키 발급 응답 외에는 평문 키가 어디에도 남지 않는가
- [ ] 교환 실패 이유(없음, 위조, 폐기, 만료)를 밖으로 구분하지 않고 모두 401로 주는가
- [ ] 짧은 access token에 MCP에 필요한 권한만 들어가는가
- [ ] 키 목록에서 하나씩 폐기할 수 있고, 오래 쓰지 않은 키는 만료되는가
- [ ] MCP 서버가 같은 사용자의 동시 호출에서 교환을 한 번만 하는가
- [ ] 키가 없거나 거부되면 발급 페이지 링크를 담은 도구 오류를 돌려주는가
- [ ] stdio 모드에서 표준 출력에 로그를 쓰지 않는가
- [ ] 원격 모드의 MCP access token 검증이 audience를 확인하는가
- [ ] 종단 간 테스트가 실제 기존 서버를 상대로 통과하는가

## 기억할 원칙

### 오래 사는 것은 서버 사이에만, 요청에 실리는 것은 짧게

키는 오래 살지만 MCP 서버와 기존 서버의 교환 엔드포인트 사이에서만 오간다.
매 요청에 실리는 것은 30초짜리 토큰뿐이다.
오래 사는 비밀이 지나가는 길을 하나로 좁히면,
그 길만 단단히 지키면 된다.

### 두 서버의 계약은 바깥 테스트가 정한다

MCP 서버와 기존 서버는 언어도 저장소도 다르지만
그 사이의 HTTP 계약은 하나다.
종단 간 시나리오에서 출발해 계약을 정하고,
양쪽이 각자의 테스트로 그 계약을 지키게 하면
한쪽이 바뀌었을 때 어느 쪽이 깨졌는지 바로 드러난다.

---

[^build-server]: Model Context Protocol, [Build an MCP server](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server), 게시일 표시 없음 (2026-07-28 버전 문서)

[^authz]: Model Context Protocol, [Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), 2026-07-28 (명세 버전 날짜)

[^security]: Model Context Protocol, [Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices), 게시일 표시 없음 (2026-07-28 버전 문서)

[^go-sdk]: GitHub, [modelcontextprotocol/go-sdk v1.8.0](https://github.com/modelcontextprotocol/go-sdk/releases/tag/v1.8.0), 2026-09-14
