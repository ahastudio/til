# React 프로젝트 시작하기

## 참고

- <https://github.com/ahastudio/til/blob/main/javascript/20181212-setup-javascript-project.md>
- <https://github.com/ahastudio/til/blob/main/jest>
- <https://jestjs.io/docs/configuration#testenvironment-string>
- <https://npmjs.com/jest-environment-jsdom>
- <https://github.com/testing-library/dom-testing-library>
- <https://github.com/testing-library/react-testing-library>

## 패키지 생성

```bash
npm init -y
```

## TypeScript 세팅

개발할 때만 사용하는 TypeScript 의존성 설치.

```bash
npm i -D typescript
```

`tsconfig.json` 파일 생성.

```bash
npx tsc --init
```

`tsconfig.json` 파일에서 `jsx` 관련 항목 주석을 제거하고 수정.

```json
    "jsx": "react-jsx",
```

## ESLint 세팅

개발할 때만 사용하는 ESLint 설치.

```bash
npm i -D eslint
```

```bash
npx eslint --init
```

XO 관련 의존성 제거하고, 에어비앤비 관련 의존성 설치.

```bash
npm uninstall eslint-config-xo \
    eslint-config-xo-typescript

npm i -D eslint-config-airbnb \
    eslint-plugin-import \
    eslint-plugin-react \
    eslint-plugin-react-hooks \
    eslint-plugin-jsx-a11y
```

`.eslintrc.js` 파일을 섬세하게 수정.

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    jest: true,
  },
  extends: [
    "airbnb",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react", "react-hooks", "@typescript-eslint"],
  settings: {
    "import/resolver": {
      node: {
        extensions: [".js", ".jsx", ".ts", ".tsx"],
      },
    },
  },
  rules: {
    indent: ["error", 2],
    "no-trailing-spaces": "error",
    curly: "error",
    "brace-style": "error",
    "no-multi-spaces": "error",
    "space-infix-ops": "error",
    "space-unary-ops": "error",
    "no-whitespace-before-property": "error",
    "func-call-spacing": "error",
    "space-before-blocks": "error",
    "keyword-spacing": ["error", { before: true, after: true }],
    "comma-spacing": ["error", { before: false, after: true }],
    "comma-style": ["error", "last"],
    "comma-dangle": ["error", "always-multiline"],
    "space-in-parens": ["error", "never"],
    "block-spacing": "error",
    "array-bracket-spacing": ["error", "never"],
    "object-curly-spacing": ["error", "always"],
    "key-spacing": ["error", { mode: "strict" }],
    "arrow-spacing": ["error", { before: true, after: true }],
    "import/no-extraneous-dependencies": [
      "error",
      {
        devDependencies: [
          "**/*.test.js",
          "**/*.test.jsx",
          "**/*.test.ts",
          "**/*.test.tsx",
        ],
      },
    ],
    "import/extensions": [
      "error",
      "ignorePackages",
      {
        js: "never",
        jsx: "never",
        ts: "never",
        tsx: "never",
      },
    ],
    "react/jsx-filename-extension": [
      2,
      {
        extensions: [".js", ".jsx", ".ts", ".tsx"],
      },
    ],
    "jsx-a11y/label-has-associated-control": ["error", { assert: "either" }],
  },
};
```

## VS Code 설정 파일 생성

`.vscode` 디렉터리 및 `settings.json` 파일 생성.

```bash
mkdir .vscode

touch .vscode/settings.json
```

`.vscode/settings.json` 파일은 다음과 같이 작성한다.

```json
{
  "editor.rulers": [80],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "trailing-spaces.trimOnSave": true
}
```

## Jest 세팅

Jest 및 SWC 지원 패키지 설치.

```bash
npm i -D jest @types/jest @swc/core @swc/jest
```

`jest.config.js` 파일 생성.

```javascript
module.exports = {
  // testEnvironment: 'jsdom',
  // setupFilesAfterEnv: [
  //   '<rootDir>/src/setupTests.ts',
  // ],
  transform: {
    "^.+\\.(t|j)sx?$": [
      "@swc/jest",
      {
        jsc: {
          parser: {
            syntax: "typescript",
            // jsx: true,
            // decorators: true,
          },
          transform: {
            // react: {
            //   runtime: 'automatic',
            // },
            // legacyDecorator: true,
            // decoratorMetadata: true,
          },
        },
      },
    ],
  },
};
```

## React, Parcel 세팅

React 의존성 설치.

```bash
npm i react react-dom

npm i -D @types/react @types/react-dom
```

Parcel 설치.

```bash
npm i -D parcel
```

`package.json` 파일에 `source` 항목 추가.

```json
  "source": "index.html",
```

`index.html` 파일 작성.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>React Demo App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./src/main.tsx"></script>
  </body>
</html>
```

`src/main.tsx` 파일 작성.

```tsx
import ReactDOM from "react-dom/client";

import App from "./App";

function main() {
  const container = document.getElementById("root");
  if (!container) {
    return;
  }

  const root = ReactDOM.createRoot(container);
  root.render(<App />);
}

main();
```

`src/App.tsx` 파일 작성.

```tsx
export default function App() {
  return <p>Hello, world!</p>;
}
```

## React Testing Library 세팅

관련 의존성 설치

```bash
npm i -D @testing-library/react jest-environment-jsdom
```

`jest.config.js` 파일에서 관련 항목의 주석을 풀어준다.

```javascript
module.exports = {
  testEnvironment: "jsdom",
  // setupFilesAfterEnv: [
  //   '<rootDir>/src/setupTests.ts',
  // ],
  transform: {
    "^.+\\.(t|j)sx?$": [
      "@swc/jest",
      {
        jsc: {
          parser: {
            syntax: "typescript",
            jsx: true,
            // decorators: true,
          },
          transform: {
            react: {
              runtime: "automatic",
            },
            // legacyDecorator: true,
            // decoratorMetadata: true,
          },
        },
      },
    ],
  },
};
```

`src/App.test.tsx` 파일 작성.

```tsx
import { render, screen } from "@testing-library/react";

import App from "./App";

test("App", () => {
  render(<App />);

  screen.getByText(/Hello, world/);
});
```
