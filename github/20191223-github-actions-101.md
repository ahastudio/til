# GitHub Actions 맛보기

- [아듀 2019!](https://adieu2019.ahastudio.com/)
- 이전 글:
- 다음 글:

---

GitHub Actions를 이용하면 Travis CI나 CircleCI 등을 사용하지 않아도
GitHub만 이용해서 CI 환경을 구축할 수 있습니다.

## 설정 파일 준비

GitHub은 `.github/worflows` 디렉터리에 있는 Action을 실행합니다.

이를 위해 먼저 해당 디렉터리를 준비합니다.

```bash
mkdir -p .github/workflows
```

Action을 정의한 YAML 파일을 만들어 줍니다.
여기선 간단한 CI를 만들기 위해 `ci.yml` 파일을 만들겠습니다.

```bash
touch .github/workflows/ci.yml
```

## Checkout

일단 소스 코드를 가져와서 확인해 봅시다.

`.github/workflows/ci.yml` 파일을 다음과 같이 작성합니다.

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-18.04]
        node-version: [12.x]
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: File list
        run: ls -al
```

## NPM

NPM으로 의존성을 설치하고, 테스트를 실행합시다.

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-18.04]
        node-version: [12.x]
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
```

## Pull Request

해당 저장소를 Fork 하고, PR을 날렸을 때 작동하도록 액션 초반부에 `pull_request`를 추가합니다.

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-18.04]
        node-version: [12.x]
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
```

## Deploy

`master` 브랜치에 Merge 됐을 때 자동으로 deploy 할 수 있도록 준비합시다.

`if`와 `github.ref`를 이용해 브랜치 이름을 확인하면 됩니다.

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-18.04]
        node-version: [12.x]
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Deploy
        if: github.ref == 'refs/heads/master'
        run: echo "Hello, world!"
```

---

- [아듀 2019!](https://adieu2019.ahastudio.com/)
- 이전 글:
- 다음 글:
