# Jest · 🃏 Delightful JavaScript Testing

- <https://jestjs.io/>
- <https://github.com/facebook/jest>

## Awesome Jest

<https://github.com/jest-community/awesome-jest>

## Jest Plugins

<https://github.com/negativetwelve/jest-plugins>

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

## 테스트를 멈추게 만드는 범인 찾기 (Ruby 스크립트)

```
Dir.glob('src/*.test.*').each do |name|
  puts "\n\n*** Run test: #{name}"
  system("npx jest --runInBand --detectOpenHandles #{name}")
end
```
