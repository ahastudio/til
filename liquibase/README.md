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

### XML 형식 예제

```xml
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd">

    <changeSet id="1" author="developer">
        <createTable tableName="users">
            <column name="id" type="bigint" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="username" type="varchar(50)">
                <constraints nullable="false" unique="true"/>
            </column>
            <column name="email" type="varchar(100)">
                <constraints nullable="false"/>
            </column>
        </createTable>
    </changeSet>

</databaseChangeLog>
```

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

### YAML 형식 예제

```yaml
databaseChangeLog:
  - changeSet:
      id: 1
      author: developer
      changes:
        - createTable:
            tableName: users
            columns:
              - column:
                  name: id
                  type: bigint
                  autoIncrement: true
                  constraints:
                    primaryKey: true
                    nullable: false
              - column:
                  name: username
                  type: varchar(50)
                  constraints:
                    nullable: false
                    unique: true
              - column:
                  name: email
                  type: varchar(100)
                  constraints:
                    nullable: false
```

## CLI 명령어

```bash
# 변경사항 적용
liquibase update

# 특정 개수만큼 적용
liquibase update-count 3

# 특정 태그까지 적용
liquibase update-to-tag version-1.0

# 롤백
liquibase rollback-count 1
liquibase rollback-to-date 2024-01-01
liquibase rollback <tag>

# 현재 상태 확인
liquibase status

# 변경사항 검증
liquibase validate

# SQL 생성 (실행하지 않고 확인)
liquibase update-sql
```

## Spring Boot 통합

### Gradle 설정

```gradle
dependencies {
    implementation 'org.liquibase:liquibase-core'
}
```

### Maven 설정

```xml
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
```

### application.yml 설정

```yaml
spring:
  liquibase:
    change-log: classpath:db/changelog/db.changelog-master.yaml
    enabled: true
```

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
