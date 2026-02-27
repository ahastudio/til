# Zeitwerk

Rails의 코드 자동 로딩(autoloading)을 담당하는 gem이다.
파일 경로와 상수 이름이 일치하는 규칙을 강제하며,
이를 통해 `require` 없이도 클래스와 모듈을 사용할 수 있다.

## bin/rails zeitwerk:check

Zeitwerk 설정이 올바른지 확인하는 rake task다.
모든 파일을 eager load한 후 상수 충돌이나 경로 불일치가
없는지 검사한다.

```bash
bin/rails zeitwerk:check
```

성공 시:

```
Hold on, I am eager loading the application.
All is good!
```

## 주요 오류 유형

### 파일명과 상수 이름 불일치

파일 경로에서 유추한 상수 이름과 실제 정의된 상수가
다를 때 발생한다.

```
expected file app/models/user_profile.rb to define constant
UserProfile, but didn't
```

`app/models/user_profile.rb` 안에서 `UserProfile`이 아닌
다른 이름으로 클래스를 정의했을 때 나타난다.

### 네임스페이스 누락

```
expected app/models/admin/dashboard.rb to define constant
Admin::Dashboard
```

`app/models/admin/` 디렉토리에 `module Admin` 네임스페이스 없이
`Dashboard` 클래스만 정의했을 때 발생한다.

## 활용 시점

- CI 파이프라인에서 배포 전 자동화 검사
- 파일/클래스 이름 변경 후 확인
- 대규모 리팩토링 후 코드 구조 검증

---

- <https://github.com/fxn/zeitwerk>
- <https://guides.rubyonrails.org/autoloading_and_reloading_constants.html>
