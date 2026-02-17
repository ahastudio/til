# JavaScript 프로젝트 시작하기

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글:
- 다음 글: [C++에서 어셈블리 공부하기](http://j.mp/2Q7SPUw)

## 목표

Node.js를 설치하고, 프로젝트를 진행할 수 있는 Node.js 패키지를 만들고, 코드
퀄리티를 일정 수준 이상으로 유지할 수 있도록 `lint`와 `test`를 실행할 수 있는
상태를 만든다.

## fnm (Fast Node Manager) 설치

계속 업그레이드되는 Node.js로 프로젝트를 진행하다 보면 프로젝트마다 서로 다른
버전을 사용하는 경우가 있다. 그래서 여러 버전의 Node.js를 설치해서 사용하고 싶을
때가 있는데, [`fnm`](https://github.com/Schniz/fnm)을 사용하면 이게 가능하다.

### Mac, Linux 사용자

[Homebrew](https://brew.sh/)를 이용해 `fnm`을 설치할 수 있다.

```bash
brew install fnm
```

`~/.bashrc` 또는 `~/.zshrc`에 다음을 추가한다.

```bash
eval "$(fnm env)"
```

현재 터미널에서 바로 사용하고 싶다면 위 명령을 그대로 입력한다.

### Windows 사용자

Windows 사용자는 [Scoop](https://scoop.sh/) 또는
[Chocolatey](https://chocolatey.org/)를 사용해 `fnm`을 설치할 수 있다.

```bash
scoop install fnm

# 또는

choco install fnm
```

## Node.js 설치

설치 가능한 버전 확인.

```bash
fnm ls-remote
```

LTS(Long Term Support) 버전을 설치하고 기본으로 사용하게 한다.

```bash
fnm install --lts
fnm use lts-latest
fnm default $(fnm current)
```

설치된 상태 확인.

```bash
fnm list

fnm current
```

## NPM 업그레이드

```bash
npm install -g npm
```

## 프로젝트 폴더 생성

프로젝트 이름을 `my-project`라고 했을 때 다음과 같이 폴더를 만들고 사용할
Node.js 버전을 잡아준다.

```bash
mkdir my-project
cd my-project
fnm use default
echo "$(fnm current)" > .nvmrc
```

나중에 시스템에 설치된 Node.js 버전과 프로젝트에서 사용하는 Node.js 버전이 다른
상황이 오더라도 `fnm use` 명령을 통해 프로젝트에서 사용하고 있는 버전을 쉽게
사용할 수 있다.

또는 `.nvmrc` 파일을 확인함으로써 어떤 버전으로 개발했는지 알 수 있다.

```bash
cat .nvmrc
```

## 프로젝트 초기화

다음 명령을 실행하고 질문에 답함으로써 `package.json` 파일을 자동으로 생성한다.

```bash
npm init
```

귀찮으면 질문에 대해 그냥 엔터만 계속 눌러도 되는데, `-y` 플래그를 사용하면 질문
자체를 안 하게 할 수도 있다.

```bash
npm init -y
```

## ESLint 설치

좋은 코딩 스타일을 위해 [ESLint](https://eslint.org/)를 설치해 사용한다.

```bash
npm install --save-dev eslint
```

다음 명령을 통해 ESLint 설정 파일(`.eslintrc.js`)을 자동으로 생성한다.

```bash
npx eslint --init
```

몇 가지 질문이 나오는데 프로젝트에 따라 다르게 선택한다. 내가 사용하는 건 주로
다음과 같다.

```text
? How would you like to configure ESLint?  (Use arrow keys)
❯ Answer questions about your style

? Which version of ECMAScript do you use?  (Use arrow keys)
❯ ES2017

? Are you using ES6 modules? (y/N)
N

? Where will your code run? (Press <space> to select, <a> to toggle all, <i> to invert selection)
 ◯ Browser
❯◉ Node

? Do you use JSX? (y/N)
N

? What style of indentation do you use? (Use arrow keys)
❯ Spaces

? What quotes do you use for strings? (Use arrow keys)
❯ Single

? What line endings do you use? (Use arrow keys)
❯ Unix

? Do you require semicolons? (Y/n)
Y

? What format do you want your config file to be in? (Use arrow keys)
❯ JavaScript
```

`.eslintrc.js` 파일을 열어 `rules`를 수정, 추가한다.
[Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) 같은 널리
알려진 스타일 가이드를 사용하고 싶다면 간단히
[eslint-config-airbnb](https://www.npmjs.com/package/eslint-config-airbnb)
확장을 설치해서 사용하면 된다.

```javascript
    // 공백 4칸에서 공백 2칸으로 변경.
    // https://eslint.org/docs/rules/indent
    'indent': ['error', 2],

    // 줄 끝 공백 항상 제거.
    // https://eslint.org/docs/rules/no-trailing-spaces
    'no-trailing-spaces': 'error',

    // 블록 중괄호 항상 사용.
    // https://eslint.org/docs/rules/curly
    'curly': 'error',

    // 중괄호 스타일 맞춤.
    // https://eslint.org/docs/rules/brace-style
    'brace-style': 'error',

    // 공백이 필요하면 하나만 들어게 한다.
    // https://eslint.org/docs/rules/no-multi-spaces
    'no-multi-spaces': 'error',

    // 연산자 앞뒤에 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/space-infix-ops
    'space-infix-ops': 'error',

    // 단항 연산자가 단어면 사이에 공백이 들어가게 하고, 기호면 공백을 제거.
    // https://eslint.org/docs/rules/space-unary-ops
    'space-unary-ops': 'error',

    // 속성 앞 공백 제거.
    // https://eslint.org/docs/rules/no-whitespace-before-property
    'no-whitespace-before-property': 'error',

    // 함수 호출을 위한 소괄호는 반드시 붙여서 쓰게 한다.
    // https://eslint.org/docs/rules/func-call-spacing
    'func-call-spacing': 'error',

    // 블록 앞에 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/space-before-blocks
    'space-before-blocks': 'error',

    // if, else 등 키워드 앞뒤에 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/keyword-spacing
    'keyword-spacing': ['error', { 'before': true, 'after': true }],

    // 쉼표 뒤에만 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/comma-spacing
    'comma-spacing': ['error', { 'before': false, 'after': true }],

    // 여러 줄로 여러 요소를 표현할 때 줄 마지막에 쉼표가 들어가게 한다.
    // https://eslint.org/docs/rules/comma-style
    'comma-style': ['error', 'last'],

    // 여러 줄로 여러 요소를 표현할 때 마지막 줄 끝에도 쉼표가 들어가게 한다.
    // https://eslint.org/docs/rules/comma-dangle
    'comma-dangle': ['error', 'always-multiline'],

    // 소괄호 안에 공백이 들어가지 않게 한다.
    // https://eslint.org/docs/rules/space-in-parens
    'space-in-parens': ['error', 'never'],

    // 블록 중괄호 안에 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/block-spacing
    'block-spacing': 'error',

    // Array 리터럴 대괄호 안에 공백이 들어가지 않게 한다.
    // https://eslint.org/docs/rules/array-bracket-spacing
    'array-bracket-spacing': ['error', 'never'],

    // Object 리터럴 중괄호 안에 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/object-curly-spacing
    'object-curly-spacing': ['error', 'always'],

    // Key-Value 구분을 위한 콜론 뒤에만 공백을 넣는다.
    // https://eslint.org/docs/rules/key-spacing
    'key-spacing': ['error', { 'mode': 'strict' }],

    // Arrow Function 기호 앞 뒤에 공백이 들어가게 한다.
    // https://eslint.org/docs/rules/arrow-spacing
    'arrow-spacing': ['error', { 'before': true, 'after': true }],
```

`.eslintrc.js` 파일 자체를 ESLint 설정에 맞추고 싶다면 다음을 실행한다.

```bash
npx eslint --fix --no-ignore .eslintrc.js
```

이 설정 파일은 [Visual Studio Code](https://code.visualstudio.com/)나
[WebStorm](https://www.jetbrains.com/webstorm/) 등에서 사용할 수 있다.

간단하게 테스트를 하기 위해 `index.js` 파일을 작성한다.

```javascript
var a = 1;
b = [1, 2];
console.log(b.map((i) => i + a));
```

고쳐야 할 부분을 찾는다.

```bash
npx eslint .
```

다음 명령을 실행하면 코드를 검사하고 자동으로 고칠 수 있는 부분을 고쳐주고,
그래도 남아있는 문제는 화면에 보여준다.

```bash
npx eslint --fix .
```

`package.json`의 `scripts` 항목에 `lint`를 추가하면 이 작업을 편하게 할 수 있다.

```json
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "lint": "eslint --fix .  # <- 여기에 lint 명령을 추가"
  },
```

`npm run`으로 ESLint를 실행할 수 있다.

```bash
npm run lint
```

아까 테스트하기 위해 만든 `index.js` 파일의 문제가 모두 해결되지 않아서
`npm ERR! code ELIFECYCLE` 에러 메시지가 나오는 걸 볼 수 있다. 간단히 고쳐보자.

```javascript
const { log: print } = console;

var a = 1;
const b = [1, 2];

print(b.map((i) => i + a));
```

## Jest 설치

자동화된 테스트 코드를 작성하고 활용하기 위해 Jest를 설치해서 쓸 수 있다.

```bash
npm install --save-dev jest
```

`sum.test.js` 파일을 만들어서 확인해 보자.

```javascript
test("sum", () => {
  expect(sum(1, 2)).toBe(3);
});
```

`jest`를 실행하면 `*.test.js` 파일을 모두 실행한다.

```bash
npx jest
```

테스트를 간단히 통과시키자.

```javascript
const sum = (a, b) => a + b;

test("sum", () => {
  expect(sum(1, 2)).toBe(3);
});
```

만약 파일을 계속 감시하고 있다가 수정될 때마다 자동으로 테스트가 실행되게 하려면
`watchAll` 플래그를 사용하면 된다. 그 상태에서 테스트 전체를 다시 실행하려면
`a`나 `Enter` 키를 누르면 되고, 중단하려면 `q`를 누르면 된다.

```bash
npx jest --watchAll
```

추가적인 설정이 필요하면 `jest.config.js` 파일을 작성하면 된다.
<https://jestjs.io/docs/en/configuration> 문서 참고.

```javascript
module.exports = {
  verbose: true,
};
```

ESLint를 실행하면 `test`나 `expect` 같은 게 정의되지 않았다는 에러가 뜨는데,
`.eslintrc.js` 파일의 `env`에 `jest`를 추가하면 된다.

```javascript
  'env': {
    'es6': true,
    'node': true,
    // Jest 사용
    'jest': true,
  },
```

마찬가지로 `package.json`을 수정해서 `npm`으로 테스트를 실행할 수 있다.

```json
  "scripts": {
    "test": "jest  # <- 기존의 에러 종료를 Jest 실행으로 변경",
    "lint": "eslint --fix ."
  },
```

`test`는 기본 명령이라 `run` 없이 실행 가능하다.

```bash
npm test
```

## Sample Code

[https://github.com/ahastudio/javascript-sample-project](http://j.mp/2AkJkfA)

---

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글:
- 다음 글: [C++에서 어셈블리 공부하기](http://j.mp/2Q7SPUw)
