# Spring Boot 2.2로 업그레이드하기

참고: [패캠 강의 프로젝트 업그레이드 Pull Request](http://j.mp/2Yfc6ZW)

## Gradle

### Spring Boot 플러그인 버전 변경

```
- id 'org.springframework.boot' version '2.1.5.RELEASE'
+ id 'org.springframework.boot' version '2.2.1.RELEASE'
```

### Spring 의존성 관리자 플러그인 버전 명시

```
+ id 'io.spring.dependency-management' version '1.0.8.RELEASE'
```

```
- apply plugin: 'io.spring.dependency-management'
```

### `test` 작업에 JUnit Platform 적용

```
+ test {
+     useJUnitPlatform()
+ }
```

## 테스트 코드

### `@Test` Annotation 패키지 변경

```
- import org.junit.Test;
+ import org.junit.jupiter.api.Test;
```

### `@BeforeEach` Annotation 사용

```
- import org.junit.Before;
+ import org.junit.jupiter.api.BeforeEach;
```

```
- @Before
+ @BeforeEach
```

### JUnit 4 `SpringRunner` 제거

```
- import org.junit.runner.RunWith;
- import org.springframework.test.context.junit4.SpringRunner;
```

```
- @RunWith(SpringRunner.class)
```
