# Liquibase

Source control for your database

<https://www.liquibase.com/>

<https://github.com/liquibase/liquibase>

## 소개

Liquibase는 데이터베이스 스키마 변경을 추적, 관리, 적용하는 오픈소스 데이터베이스 마이그레이션 도구입니다.

- SQL, XML, YAML, JSON 등 다양한 형식으로 변경사항 작성 가능
- 여러 데이터베이스 벤더 지원 (MySQL, PostgreSQL, Oracle, SQL Server 등)
- 롤백 기능 제공
- CI/CD 파이프라인 통합 가능

## 주요 개념

### ChangeLog

데이터베이스 변경 내역을 기록하는 파일. 모든 변경사항(changeset)을 순서대로 포함합니다.

### ChangeSet

데이터베이스에 적용할 하나의 변경 단위. 각 changeset은 고유한 ID와 작성자를 가집니다.

### Preconditions

변경사항을 적용하기 전에 확인할 조건을 정의합니다.

### Rollback

변경사항을 되돌리는 방법을 정의합니다.

## 기본 사용법

### SQL 형식 예제

```sql
--liquibase formatted sql

--changeset developer:1
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL
);
```

## Gradle 명령어

Liquibase Gradle 플러그인을 사용하는 경우:

```gradle
plugins {
    id 'org.liquibase.gradle' version '2.2.0'
}

liquibase {
    activities {
        main {
            changeLogFile 'src/main/resources/db/changelog/db.changelog-master.sql'
            url 'jdbc:postgresql://localhost:5432/mydb'
            username 'myuser'
            password 'mypassword'
        }
    }
}
```

```bash
# 변경사항 적용
./gradlew update

# 롤백
./gradlew rollbackCount -PliquibaseCommandValue=1

# 현재 상태 확인
./gradlew status

# SQL 생성 (실행하지 않고 확인)
./gradlew updateSQL
```

Spring Boot를 사용하는 경우, 애플리케이션 실행 시 자동으로 적용됩니다.

```bash
# Spring Boot 애플리케이션 실행 시 자동 적용
./gradlew bootRun
```

## Spring Boot 통합

### Gradle 설정

```gradle
dependencies {
    implementation 'org.liquibase:liquibase-core'
    runtimeOnly 'org.postgresql:postgresql'  // 또는 사용하는 DB 드라이버
}
```

### application.yml 설정

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: myuser
    password: mypassword
    driver-class-name: org.postgresql.Driver

  liquibase:
    change-log: classpath:db/changelog/db.changelog-master.sql
    enabled: true
```

Spring Boot는 `spring.datasource` 설정을 자동으로 Liquibase에 전달하므로, 별도의 환경변수 설정 없이 application.yml만으로 데이터베이스 연결이 가능합니다.

## 베스트 프랙티스

1. **하나의 ChangeSet에 하나의 변경사항만 포함**
   - 롤백과 디버깅이 쉬워짐

2. **절대 이미 적용된 ChangeSet을 수정하지 않기**
   - 체크섬 오류 발생
   - 새로운 ChangeSet으로 수정사항 추가

3. **의미있는 ID와 설명 사용**
   - 변경 이력 추적이 용이

4. **롤백 전략 명시**
   - 자동 롤백이 불가능한 경우 명시적으로 정의

5. **환경별 설정 관리**
   - Context와 Label을 활용하여 환경별로 다른 변경사항 적용

## 참고 자료

[Liquibase Documentation](https://docs.liquibase.com/)

[Liquibase Best Practices](https://www.liquibase.com/blog/liquibase-best-practices)

[Spring Boot with Liquibase](https://docs.spring.io/spring-boot/docs/current/reference/html/howto.html#howto.data-initialization.migration-tool.liquibase)
