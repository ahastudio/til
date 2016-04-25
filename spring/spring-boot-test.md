# Spring Boot 1.4 Testing

- [Testing improvements in Spring Boot 1.4](https://spring.io/blog/2016/04/15/testing-improvements-in-spring-boot-1-4)
- [Spring Boot Reference Guide - 40. Testing](http://docs.spring.io/spring-boot/docs/1.4.0.M2/reference/html/boot-features-testing.html)

기존 코드:
```java
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(MyApp.class)
@WebIntegrationTest
```

새 코드:
```java
@RunWith(SpringRunner.class)
@SpringBootTest
```

