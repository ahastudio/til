# Kotlin + Spring Boot 맛보기

[아듀 2019!](https://adieu2019.ahastudio.com/)

- 이전 글:
- 다음 글: [Spring Boot 2.2로 업그레이드하기](http://j.mp/36eeIdt)

---

## Gradle 프로젝트 만들기

```bash
gradle init

# 몇 가지 질문이 나오면 답변.
# 불필요한 설정을 제하기 위해 프로젝트 타입을 “library”로 선택.

Select type of project to generate:
  1: basic
  2: application
  3: library
  4: Gradle plugin
Enter selection (default: basic) [1..4] 3

Select implementation language:
  1: C++
  2: Groovy
  3: Java
  4: Kotlin
Enter selection (default: Java) [1..4] 4

Select build script DSL:
  1: Groovy
  2: Kotlin
Enter selection (default: Kotlin) [1..2] 1

Project name (default: kotlin-spring-sample): sample
Source package (default: sample): sample

BUILD SUCCESSFUL in 20s
2 actionable tasks: 1 executed, 1 up-to-date
```

## IntelliJ IDEA로 프로젝트 열기

```bash
idea .
```

## `build.gradle`에 Spring Boot 설정 추가

참고: [Kotlin 공식 홈페이지의 “Using Gradle” 문서](http://j.mp/354nf2q)

플러그인 설정.

- [Kotlin Compiler Plugins](http://j.mp/2Psk25R)
- [Spring Boot Gradle Plugin](http://j.mp/2YsHYKA)
- [Dependency Management Plugin](http://j.mp/2P0dTyO)

```gradle
plugins {
    // Apply the Kotlin JVM plugin to add support for Kotlin on the JVM.
    id 'org.jetbrains.kotlin.jvm' version '1.3.61'

    // Kotlin-Spring compiler plugin
    id "org.jetbrains.kotlin.plugin.spring" version "1.3.61"

    // Spring Boot plugin
    id 'org.springframework.boot' version '2.2.2.RELEASE'

    // Spring Dependency Management plugin
    id 'io.spring.dependency-management' version '1.0.6.RELEASE'
}
```

의존성 설정.

```gradle
dependencies {
    // Use the Kotlin JDK 8 standard library.
    implementation 'org.jetbrains.kotlin:kotlin-stdlib-jdk8'

    // Kotlin Reflection
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    // Spring Boot Web
    implementation("org.springframework.boot:spring-boot-starter-web")

    // Spring Boot Test
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

JUnit 5 설정.

```gradle
test {
    useJUnitPlatform()
}
```

Kotlin 컴파일 타겟 지정.

```gradle
compileKotlin {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}
```

## Application 코드 작성

`src/main/kotlin/myapp/SampleApplication.kt`

```kotlin
package myapp

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class SampleApplication

fun main(args: Array<String>) {
    runApplication<SampleApplication>(*args)
}
```

`src/test/kotlin/myapp/SampleApplicationTest.kt`

```kotlin
package myapp

import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
class SampleApplicationTests {
    @Test
    fun contextLoads() {
    }
}
```

## 빌드

```bash
./gradlew build
```

## 웹 서버 실행

```bash
./gradlew bootRun
```

브라우저에서 <http://localhost:8080/> 주소를 열어 잘 되고 있는지 확인합니다.
“Whitelabel Error Page”가 나오면 정상입니다.

## 테스트 실행

```bash
./gradlew test
```

## `HelloController` 추가

`src/main/kotlin/myapp/controller/HelloController.kt`

```kotlin
package myapp.controller

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class HelloController {
    @GetMapping("/hello")
    fun hello() = "Hello, world!"
}
```

웹 서버를 다시 실행하고, 브라우저에서 <http://localhost:8080/hello> 주소를 열어
잘 되고 있는지 확인합니다.

## `HelloController`에 대한 테스트 코드 작성

`src/test/kotlin/myapp/controller/HelloControllerTest.kt`

```kotlin
package myapp.controller

import org.hamcrest.CoreMatchers.containsString
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.content
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.status

@WebMvcTest(HelloController::class)
internal class HelloControllerTest(@Autowired val mockMvc: MockMvc) {
    @Test
    fun `GET hello`() {
        mockMvc.perform(get("/hello"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("Hello")))
    }
}
```

테스트를 실행해서 결과를 확인할 수 있습니다.

```bash
./gradlew test
```

## 소스 코드

[https://github.com/ahastudio/kotlin-spring-sample](http://j.mp/2Ruz79S)

## 참고

- [Building web applications with Spring Boot and Kotlin](http://j.mp/342KhFi)

---

[아듀 2019!](https://adieu2019.ahastudio.com/)

- 이전 글:
- 다음 글: [Spring Boot 2.2로 업그레이드하기](http://j.mp/36eeIdt)
