# CodeceptJS 3 시작하기

- [아듀 2020!](https://adieu2020.ahastudio.com/)
- 이전 글: [Docker 컨테이너로 간단히 Python 개발 시작하기](https://j.mp/3mUGowl)
- 다음 글: [Cypress 시작하기](https://j.mp/3gBwqOd)

---

테스트 코드 작성은 이제 올바르게 개발을 하는 조직에선
상식으로 자리 잡았다고 생각합니다.
어떤 걸 만들지 미리 정의하고, 올바르게 만들었는지 확인하고,
유지보수 과정에서 혹시 잘못된 부분이 있는지 확인하는데
매우 적은 비용으로 큰 효용을 거둘 수 있기 때문이죠.

하지만 단위 테스트만으로는 시스템이 올바르게 작동하는지 알 수 없고,
사용자가 유용하게 사용할 수 있는지 미리 정의하는 것도 쉽지 않습니다.
결정적으로, 사용자(또는 고객)와 소통하기 위한 교차점이 마련되지 않습니다.
따라서 우리에겐 인수 테스트가 필요합니다.

인수 테스트는 여러 방식으로 작성할 수 있습니다.
최근에 가장 인기 있는 E2E 테스트를,
[CodeceptJS](https://j.mp/3gMqkuJ)로 시작해 봅시다.

## CodeceptJS 설치

일단 프로젝트를 만들어 봅시다.

```bash
mkdir <프로젝트 이름>
cd <프로젝트 이름>

npm init -y
```

여기선 [CodeceptJS all-in-one Installer](https://j.mp/37Um4VI)를 이용해
CodeceptJS를 간단히 설치해 보죠.

```bash
npx create-codeceptjs .
```

이제 우리는 3가지 방식으로 테스트를 실행할 수 있습니다.

```bash
# 웹 브라우저를 화면에 띄워 테스트를 실행합니다.
npm run codeceptjs

# 웹 브라우저를 화면에 띄우지 않고 테스트를 실행합니다.
npm run codeceptjs:headless

# 웹 브라우저에 CodeceptUI를 띄워 훨씬 편학게 테스트를 실행합니다.
npm run codeceptjs:ui
```

각각 어떤 형태인지 궁금하다면 예제를 먼저 감상하세요.

```bash
npm run codeceptjs:demo

npm run codeceptjs:demo:headless

npm run codeceptjs:demo:ui
```

## CodeceptJS 프로젝트 세팅

테스트 코드를 작성하기 전에 CodeceptJS를 쓸 수 있도록 준비해야 합니다.

```bash
npx codeceptjs init
```

저는 다음과 같이 질문에 답했습니다.

```bash
? Where are your tests located? (./*_test.js)
# => ./tests/**/*_test.js

? What helpers do you want to use?
(Use arrow keys)
# => ❯ Playwright

? Where should logs, screenshots, and reports to be stored? (./output)
# => ./output

? Do you want localization for tests? (See https://codecept.io/translation/)
(Use arrow keys)
# => ❯ English (no localization)

? [Playwright] Base url of site to be tested (http://localhost)
# => http://localhost:8080

? [Playwright] Show browser window (Y/n)
# => Y

? [Playwright] Browser in which testing will be performed.
Possible options: chromium, firefox or webkit (chromium)
# => chromium

Creating a new test...
----------------------

? Feature which is being tested (ex: account, login, etc)
# => google

? Filename of a test (google_test.js)
# => google_test.js
```

몇 개의 파일이 만들어진 걸 확인할 수 있습니다.

```txt
jsconfig.json
codecept.conf.js
steps.d.ts
steps_file.js
tests/google_test.js
```

나중에라도 설정을 바꾸고 싶다면 `codecept.conf.js` 파일을 고치면 됩니다.

## 테스트 코드 작성

`google_test.js` 파일을 열어 구글 검색 기능을 간단히 테스트해 봅시다.

```javascript
Feature('Google');

Scenario('Search “CodeceptJS”', ({ I }) => {
  I.amOnPage('https://www.google.com/ncr');
  I.fillField('[name="q"]', 'CodeceptJS');
  I.click('Google Search');
  I.see('codecept.io');
});
```

테스트를 실행해 봅시다.

```bash
npm run codeceptjs
```

## 결론

CodeceptJS의 가장 큰 장점은 JavaScript를 DSL처럼 활용하고 있기 때문에
프로그래머가 아니라도 작성 또는 검토가 가능하다는 점입니다.
누군가에게 완전히 떠넘기지 말고, 협력적으로 인수 테스트를 작성하면
우리가 함께 만들고 있는 게 어떤 건지 명확히 공유할 수 있을 겁니다.

---

- [아듀 2020!](https://adieu2020.ahastudio.com/)
- 이전 글: [Docker 컨테이너로 간단히 Python 개발 시작하기](https://j.mp/3mUGowl)
- 다음 글: [Cypress 시작하기](https://j.mp/3gBwqOd)
