# Spring Boot 2.2로 업그레이드하기

[아듀 2019!](https://adieu2019.ahastudio.com/)

- 이전 글: [Kotlin + Spring Boot 맛보기](http://j.mp/2RvIA0H)
- 다음 글:

---

참고: [패캠 강의 프로젝트 업그레이드 Pull Request](http://j.mp/2Yfc6ZW)

## Gradle 파일 수정

### Spring Boot 플러그인 버전 변경

```diff
- id 'org.springframework.boot' version '2.1.5.RELEASE'
+ id 'org.springframework.boot' version '2.2.1.RELEASE'
```

### Spring 의존성 관리자 플러그인 버전 명시

```diff
+ id 'io.spring.dependency-management' version '1.0.8.RELEASE'
```

```diff
- apply plugin: 'io.spring.dependency-management'
```

### `test` 작업에 JUnit Platform 적용

```diff
+ test {
+     useJUnitPlatform()
+ }
```

## JUnit 5에 맞춰서 테스트 코드 수정

### `@Test` Annotation 패키지 변경

```diff
- import org.junit.Test;
+ import org.junit.jupiter.api.Test;
```

### `@BeforeEach` Annotation 사용

```diff
- import org.junit.Before;
+ import org.junit.jupiter.api.BeforeEach;
```

```diff
- @Before
+ @BeforeEach
```

### JUnit 4 `SpringRunner` 제거

```diff
- import org.junit.runner.RunWith;
- import org.springframework.test.context.junit4.SpringRunner;
```

```diff
- @RunWith(SpringRunner.class)
```

---

[아듀 2019!](https://adieu2019.ahastudio.com/)

- 이전 글: [Kotlin + Spring Boot 맛보기](http://j.mp/2RvIA0H)
- 다음 글:
