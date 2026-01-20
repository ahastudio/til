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
            "changelogFile" to "src/main/resources/db/changelog/db.changelog-main.yaml",
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
    change-log: classpath:db/changelog/db.changelog-main.yaml
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

진입점 파일 `src/main/resources/db/changelog/db.changelog-main.yaml`을
생성하고, changes 디렉토리의 모든 SQL 파일을 포함시킵니다.

```yaml
databaseChangeLog:
  - includeAll:
      path: db/changelog/changes/
```

개별 마이그레이션 파일을 타임스탬프 기반 이름으로 생성합니다.
파일은 알파벳 순서로 실행되므로 `YYYYMMDDHHMMSS-description.sql` 형식을
사용합니다. 초 단위까지 포함하면 여러 개발자가 동시에 작업해도 충돌하지
않습니다.

```bash
# 타임스탬프 생성
date +%Y%m%d%H%M%S

# 파일 바로 생성
touch src/main/resources/db/changelog/changes/$(date +%Y%m%d%H%M%S)-create-users.sql
```

`src/main/resources/db/changelog/changes/20250115143022-create-users.sql`:

```sql
--liquibase formatted sql

--changeset developer:20250115143022
-- 사용자 기본 정보를 저장하는 테이블
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '사용자 ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '사용자명 (로그인 ID)',
    email VARCHAR(100) NOT NULL COMMENT '이메일 주소',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시각'
) COMMENT='사용자';
--rollback DROP TABLE users;
```

`src/main/resources/db/changelog/changes/20250115144531-add-created-at-index.sql`:

```sql
--liquibase formatted sql

--changeset developer:20250115144531
-- 생성 시각 기준 조회 성능 향상을 위한 인덱스
CREATE INDEX idx_users_created_at ON users(created_at);
--rollback DROP INDEX idx_users_created_at ON users;
```

### 작성 규칙

- **파일명**: `YYYYMMDDHHMMSS-description.sql` 형식으로 작성합니다.
  생성 시각을 초 단위까지 포함하여 충돌을 방지합니다.
  알파벳 순서로 정렬되어 올바른 순서로 실행됩니다.
- **ChangeSet ID**: `author:YYYYMMDDHHMMSS` 형식을 사용합니다.
  파일명의 타임스탬프 부분과 일치시키면 관리가 편합니다.
- **수정 금지**: 한 번 적용된 파일은 절대 수정하지 않습니다.
  수정이 필요하면 새로운 파일을 추가합니다.
- **롤백 필수**: 각 ChangeSet에 `--rollback` 주석으로
  롤백 SQL을 반드시 명시합니다.
- **하나의 변경**: 하나의 파일에는 하나의 ChangeSet만 포함합니다.

## 기존 데이터베이스에 적용하기

이미 운영 중인 데이터베이스가 있다면, 현재 상태를 기준점으로
설정합니다.

```bash
# Liquibase 메타데이터 테이블 초기화
./gradlew update
```

처음 실행하면 `DATABASECHANGELOG`, `DATABASECHANGELOGLOCK` 테이블이
생성됩니다. 이 테이블들이 변경 이력을 추적합니다.

기존 테이블이나 데이터는 전혀 건드리지 않습니다.
이후 추가하는 마이그레이션 파일만 실행됩니다.

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
./gradlew rollbackToDate -PliquibaseCommandValue=2025-01-15

# 특정 태그까지 롤백
./gradlew rollback -PliquibaseCommandValue=version-1.0
```
