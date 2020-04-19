# Jest · 🃏 Delightful JavaScript Testing

- <https://jestjs.io/>
- <https://github.com/facebook/jest>

## Awesome Jest

<https://github.com/jest-community/awesome-jest>

## Jest Plugins

<https://github.com/negativetwelve/jest-plugins>

### `set` (RSpec의 `let`)

<https://github.com/negativetwelve/jest-plugins/tree/master/packages/jest-plugin-set>

```bash
npm install --save-dev jest-plugin-set
```

`jest.config.js`

```javascript
module.exports = {
  // ...(중략...)
  setupFiles: [
    'jest-plugin-set/setup',
  ],
  // ...(중략...)
};
```

### `context`

<https://github.com/negativetwelve/jest-plugins/tree/master/packages/jest-plugin-context>

```bash
npm install --save-dev jest-plugin-context
```

`jest.config.js`

```javascript
module.exports = {
  // ...(중략...)
  setupFiles: [
    'jest-plugin-context/setup',
  ],
  // ...(중략...)
};
```
