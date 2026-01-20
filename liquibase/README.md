# Liquibase

Source control for your database

<https://www.liquibase.com/>

<https://github.com/liquibase/liquibase>

## 소개

Liquibase는 데이터베이스 스키마 변경을 추적, 관리, 적용하는
오픈소스 도구입니다. SQL 형식으로 변경사항을 작성하고,
여러 데이터베이스 벤더(PostgreSQL, MySQL, Oracle 등)를 지원합니다.

## Gradle 설정

`build.gradle.kts`에 Liquibase 의존성과 플러그인을 추가합니다.

```kotlin
plugins {
    id("org.liquibase.gradle") version "2.2.2"
}

dependencies {
    implementation("org.liquibase:liquibase-core")
    runtimeOnly("org.postgresql:postgresql")

    liquibaseRuntime("org.liquibase:liquibase-core:4.25.1")
    liquibaseRuntime("org.postgresql:postgresql:42.7.1")
    liquibaseRuntime("info.picocli:picocli:4.7.5")
}

liquibase {
    activities.register("main") {
        this.arguments = mapOf(
            "changelogFile" to "src/main/resources/db/changelog/db.changelog-master.sql",
            "url" to System.getenv("DB_URL"),
            "username" to System.getenv("DB_USERNAME"),
            "password" to System.getenv("DB_PASSWORD"),
            "driver" to "org.postgresql.Driver"
        )
    }
}
```

## application.yml 설정

Spring Boot 설정 파일을 작성합니다.

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    driver-class-name: org.postgresql.Driver

  liquibase:
    change-log: classpath:db/changelog/db.changelog-master.sql
    enabled: false  # 자동 적용 비활성화
```

`enabled: false`로 설정하여 애플리케이션 시작 시
자동 마이그레이션을 비활성화하고, Gradle 명령으로 명시적으로 실행합니다.

## 환경 변수 설정

데이터베이스 접속 정보를 환경 변수로 설정합니다.

```bash
export DB_URL=jdbc:postgresql://localhost:5432/mydb
export DB_USERNAME=myuser
export DB_PASSWORD=mypassword
```

## 마이그레이션 파일 작성

`src/main/resources/db/changelog/db.changelog-master.sql` 파일을
생성하고 ChangeSet을 작성합니다.

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

### ChangeSet 작성 규칙

- **ID는 타임스탬프 기반**: `YYYYMMDD-001` 형식으로 작성하면
  여러 개발자가 동시 작업할 때 충돌을 방지할 수 있습니다.
- **한 번 적용된 ChangeSet은 수정 금지**: 수정이 필요하면
  새로운 ChangeSet을 추가합니다.
- **롤백 구문 필수**: 각 ChangeSet에 `--rollback` 주석으로
  롤백 SQL을 명시합니다.
- **하나의 변경사항 단위**: 하나의 ChangeSet에는 하나의 변경사항을
  포함하되, 관련된 여러 쿼리는 함께 묶을 수 있습니다.

## 변경사항 적용

```bash
# SQL 미리보기 (실행하지 않고 확인)
./gradlew updateSQL

# 변경사항 적용
./gradlew update

# 현재 상태 확인
./gradlew status

# 변경사항 검증
./gradlew validate
```

## 롤백

롤백은 항상 최근 적용된 ChangeSet부터 역순으로 진행됩니다.
특정 ChangeSet 하나만 선택적으로 롤백할 수 없습니다.

```bash
# 롤백 SQL 미리보기
./gradlew rollbackCountSQL -PliquibaseCommandValue=1

# 최근 N개 롤백 (예: 최근 1개)
./gradlew rollbackCount -PliquibaseCommandValue=1

# 특정 날짜까지 롤백
./gradlew rollbackToDate -PliquibaseCommandValue=2024-01-15

# 특정 태그까지 롤백
./gradlew rollback -PliquibaseCommandValue=version-1.0
```
