# Spring Web MVC 프로젝트에서 Interceptor 간단히 써보기

- [아듀 2020!](https://adieu2020.ahastudio.com/)
- 이전 글: [TDD로 프론트엔드 개발하기]
- 다음 글: [Spring REST Docs 간단히 써보기](https://j.mp/3mRPUQe)

---

Spring Web MVC로 웹 애플리케이션을 만들다 보면 여러 핸들러에서 반복되는 코드를
발견할 때가 있습니다. Extract Method를 하는 방법도 있지만, 여러 파라미터가
필요한 경우 이것마저 반복되는 걸 막긴 어렵습니다.

흔히 Filter와 Interceptor 중 하나를 사용해서 이 문제를 해결할 수 있는데,
Filter는 `DispatcherServlet` 앞에 있고 Interceptor는 `DispatcherServlet` 뒤
`Handler` 앞에 있습니다.

여기서는 Spring의 도움을 크게 얻기 위해 Interceptor를 써보겠습니다.

## Spring Web MVC 프로젝트 생성

[Spring Initializr](https://start.spring.io/) 사이트에 가서 다음과 같이
입력/선택해 새 프로젝트를 만들어 봅시다.

- Project: `Gradle Project`
- Language: `Java`
- Spring Boot: `2.4.1`
- Project Metadata
  - Group: `com.example`
  - Artifact: `demo`
  - Name: `demo`
  - Description: `Demo project for Spring Boot`
  - Package name: `com.example.demo`
  - Packaging: `Jar`
  - Java: `11`
- Dependencies: `Spring Web` 추가.

Generate 버튼을 누르면 `demo.zip` 파일을 다운로드하게 됩니다.

## Controller와 Handler 만들기

자바 소스 파일을 하나 추가합니다:
`src/main/java/com/example/demo/HelloController.java`

```java
package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloController {
    @GetMapping
    public String say() {
        return "Hello, world!";
    }
}
```

스프링 웹 서버를 띄웁시다.

```bash
./gradlew bootRun
```

가볍게 확인해 봅시다.

```bash
curl http://localhost:8080/hello
```

## WebConfig 추가하기

Interceptor는 환경 설정에서 추가합니다. 여기서는 Java Config 방식을 사용하도록
하겠습니다.

`src/main/java/com/example/demo/WebConfig.java`

```java
package com.example.demo;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        System.out.println("\n\n*** WebConfig - addInterceptors\n\n");
        // TODO: add interceptor
    }
}
```

스프링 웹 서버를 중단하고 다시 실행하면 `addInterceptors` 메서드가 실행되는 걸
확인할 수 있습니다.

## 나만의 Interceptor 만들기

자, 이제 HTTP 요청에 끼어드는 Interceptor를 만들어 봅시다.

`src/main/java/com/example/demo/MyHandlerInterceptor.java`

```java
package com.example.demo;

import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class MyHandlerInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) {
        System.out.println("*** MyHandlerInterceptor - preHandle");

        return true;
    }
}
```

이렇게 만든 Interceptor를 설정에서 추가해 줍니다.

`src/main/java/com/example/demo/WebConfig.java`

```java
package com.example.demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        System.out.println("\n\n*** WebConfig - addInterceptors\n\n");

        registry.addInterceptor(myHandlerInterceptor());
    }

    @Bean
    public MyHandlerInterceptor myHandlerInterceptor() {
        return new MyHandlerInterceptor();
    }
}
```

서버를 다시 시작하고 확인해 봅니다.

```bash
curl http://localhost:8080/hello
```

## Controller로 객체 전달하기

Interceptor에서 HTTP 헤더를 참조해 객체를 만들어 Controller로 전달해 봅시다.

`src/main/java/com/example/demo/MyHandlerInterceptor.java`

```java
package com.example.demo;

import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MyHandlerInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) {
        System.out.println("*** MyHandlerInterceptor - preHandle");

        String authorization = request.getHeader("Authorization");
        if (authorization == null) {
            return true;
        }

        Pattern pattern = Pattern.compile("NAME (.+)");
        Matcher matcher = pattern.matcher(authorization);
        if (matcher.find()) {
            request.setAttribute("name", matcher.group(1));
        }

        return true;
    }
}
```

이제 Controller에서 `name`을 가져다 씁시다.

`src/main/java/com/example/demo/HelloController.java`

```java
package com.example.demo;

import org.springframework.util.ObjectUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloController {
    @GetMapping
    public String say(@RequestAttribute(required = false) String name) {
        return "Hello, " + (ObjectUtils.isEmpty(name) ? "world" : name) + "!";
    }
}
```

서버를 다시 실행하고 확인해 봅시다.

```bash
curl http://localhost:8080/hello
# => Hello, world!

curl -H "Authorization: NAME Ashal" http://localhost:8080/hello
# => Hello, Ashal!
```

---

- [아듀 2020!](https://adieu2020.ahastudio.com/)
- 이전 글: [TDD로 프론트엔드 개발하기]
- 다음 글: [Spring REST Docs 간단히 써보기](https://j.mp/3mRPUQe)
