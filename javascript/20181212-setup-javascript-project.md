# JavaScript 프로젝트 시작하기

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글:
- 다음 글: [C++에서 어셈블리 공부하기](http://j.mp/2Q7SPUw)

## NVM(Node Version Manager) 설치

### Mac, Linux 사용자

맥이나 리눅스에선
[NVM(Node Version Manager)](https://github.com/creationix/nvm)을 먼저 설치하고,
이걸 통해서 여러 버전의 Node.js를 관리한다.

설치 스크립트는 <https://github.com/creationix/nvm#installation> 참고.
2018년 말 현재 기준으로 NVM 최신 버전은 `0.33.11`이다.

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
```

NVM이 설치되면 `~/.bash_profile`에 다음이 추가된다.

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

맥 사용자는 Homebrew를 통해 설치하지 않도록 주의한다.

### Windows 사용자

윈도에선 [NVM for Windows](https://github.com/coreybutler/nvm-windows)를
먼저 설치하고, 이걸 통해서 여러 버전의 Node.js를 관리한다.

인스톨러를 <https://github.com/coreybutler/nvm-windows/releases>에서 받아서
실행해 설치한다.

## Node.js 설치

설치 가능한 버전 확인.

```bash
nvm ls-remote
```

LTS(Long Term Support) 버전을 설치하고 기본으로 사용하게 한다.

```bash
nvm install --lts
nvm use --lts
nvm alias default $(nvm current)
```

설치된 상태 확인.

```bash
nvm ls
```

## NPM 업그레이드

```bash
npm install -g npm
```

## 프로젝트 폴더 생성

프로젝트 이름을 `my-project`라고 했을 때 다음과 같이 폴더를 만들고
사용할 Node.js 버전을 잡아준다.

```bash
mkdir my-project
cd my-project
nvm use default
echo "$(nvm current)" > .nvmrc
```

나중에 시스템에 설치된 Node.js 버전과 프로젝트에서 사용하는 Node.js 버전이
다른 상황이 오더라도 `nvm use` 명령을 통해 프로젝트에서 사용하고 있는 버전을
쉽게 사용할 수 있다.

또는 `.nvmrc` 파일을 확인함으로써 어떤 버전으로 개발했는지 알 수 있다.

```bash
cat .nvmrc
```

매번 `nvm use`를 입력하는 게 귀찮은 Mac, Linux 사용자는
`AVN(Automatic Version Switching for Node.js)`을 설치하면 편하다.

```bash
npm install -g avn avn-nvm
avn setup
```

`avn setup`은 `~/.bash_profile`에 다음을 추가한다.

```bash
[[ -s "$HOME/.avn/bin/avn.sh" ]] && source "$HOME/.avn/bin/avn.sh" # load avn
```

앞으로 해당 프로젝트 폴더로 이동하면 다음과 같은 메시지가 출력되고
자동으로 해당 버전을 사용하게 된다(생각보다는 느리다).

```text
avn activated v10.15.0 via ../my-project/.nvmrc (avn-nvm v10.15.0)
```

## 프로젝트 초기화

다음 명령을 실행하고 질문에 답함으로써 `package.json` 파일을 자동으로 생성한다.
귀찮으면 질문에 대해 그냥 엔터만 계속 눌러도 된다.

```bash
npm init
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

몇 가지 질문이 나오는데 프로젝트에 따라 다르게 선택한다.
내가 사용하는 건 주로 다음과 같다.

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
[Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) 같은
널리 알려진 스타일 가이드를 사용하고 싶다면 간단히
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
var a=1
b  =  [
 1
  ,2
]
console . log( b.map(i=>i+a) )
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
`npm ERR! code ELIFECYCLE` 에러 메시지가 나오는 걸 볼 수 있다.
간단히 고쳐보자.

```javascript
const { log: print } = console;

var a = 1;
const b = [
  1,
  2,
];

print(b.map(i => i + a)) ;
```

## Jest 설치

자동화된 테스트 코드를 작성하고 활용하기 위해 Jest를 설치해서 쓸 수 있다.

```bash
npm install --save-dev jest
```

`sum.test.js` 파일을 만들어서 확인해 보자.

```javascript
test('sum', () => {
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

test('sum', () => {
  expect(sum(1, 2)).toBe(3);
});
```

만약 파일을 계속 감시하고 있다가 수정될 때마다 자동으로 테스트가 실행되게
하려면 `watchAll` 플래그를 사용하면 된다.
그 상태에서 테스트 전체를 다시 실행하려면 `a`나 `Enter` 키를 누르면 되고,
중단하려면 `q`를 누르면 된다.

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

---

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글:
- 다음 글: [C++에서 어셈블리 공부하기](http://j.mp/2Q7SPUw)
