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

ChangeSet ID를 타임스탬프로 사용하면 여러 개발자가 동시에 작업할 때 충돌을 방지할 수 있습니다.

```sql
--liquibase formatted sql

--changeset developer:20240115-001
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL
);
--rollback DROP TABLE users;

--changeset developer:20240115-002
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
--rollback ALTER TABLE users DROP COLUMN created_at;

--changeset developer:20240115-003
CREATE INDEX idx_users_username ON users(username);
--rollback DROP INDEX idx_users_username;

--changeset developer:20240116-001
INSERT INTO users (username, email) VALUES ('admin', 'admin@example.com');
INSERT INTO users (username, email) VALUES ('user1', 'user1@example.com');
--rollback DELETE FROM users WHERE username IN ('admin', 'user1');
```

각 ChangeSet에는 롤백 구문을 명시할 수 있으며, 필요한 경우 여러 개의 SQL 쿼리를 실행할 수 있습니다.

## Spring Boot 실행

Spring Boot 애플리케이션 실행 시 자동으로 Liquibase가 적용됩니다.

```bash
# 애플리케이션 실행 시 자동 적용
./gradlew bootRun
```

### 롤백

롤백이 필요한 경우 Liquibase CLI를 사용하거나 Gradle 플러그인을 사용할 수 있습니다.

```bash
# Liquibase CLI 설치
brew install liquibase  # macOS
# 또는 https://www.liquibase.com/download 에서 다운로드

# 특정 개수만큼 롤백
liquibase --defaults-file=liquibase.properties rollback-count 1

# 특정 날짜로 롤백
liquibase --defaults-file=liquibase.properties rollback-to-date 2024-01-15

# 특정 태그로 롤백
liquibase --defaults-file=liquibase.properties rollback version-1.0
```

`liquibase.properties` 파일 예시:

```properties
changeLogFile=src/main/resources/db/changelog/db.changelog-master.sql
url=${DB_URL}
username=${DB_USERNAME}
password=${DB_PASSWORD}
driver=org.postgresql.Driver
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
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    driver-class-name: org.postgresql.Driver

  liquibase:
    change-log: classpath:db/changelog/db.changelog-master.sql
    enabled: true
```

환경 변수를 통해 데이터베이스 접속 정보를 주입합니다. Spring Boot는 `spring.datasource` 설정을 자동으로 Liquibase에 전달합니다.

```bash
# 환경 변수 설정 예시
export DB_URL=jdbc:postgresql://localhost:5432/mydb
export DB_USERNAME=myuser
export DB_PASSWORD=mypassword

# 애플리케이션 실행
./gradlew bootRun
```

## 베스트 프랙티스

1. **타임스탬프 기반 ID 사용**
   - 형식: `YYYYMMDD-001`, `YYYYMMDD-002` 등
   - 여러 개발자가 동시 작업 시 충돌 방지
   - 시간 순서대로 자동 정렬

2. **하나의 ChangeSet에 하나의 변경사항만 포함**
   - 롤백과 디버깅이 쉬워짐
   - 단, 관련된 여러 쿼리는 하나의 ChangeSet에 포함 가능

3. **절대 이미 적용된 ChangeSet을 수정하지 않기**
   - 체크섬 오류 발생
   - 새로운 ChangeSet으로 수정사항 추가

4. **항상 롤백 구문 작성**
   - `--rollback` 주석으로 롤백 SQL 명시
   - DROP, DELETE 등은 데이터 손실 주의

5. **환경별 설정 관리**
   - Context와 Label을 활용하여 환경별로 다른 변경사항 적용

## 참고 자료

[Liquibase Documentation](https://docs.liquibase.com/)

[Liquibase Best Practices](https://www.liquibase.com/blog/liquibase-best-practices)

[Spring Boot with Liquibase](https://docs.spring.io/spring-boot/docs/current/reference/html/howto.html#howto.data-initialization.migration-tool.liquibase)
