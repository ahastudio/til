# Jest · 🃏 Delightful JavaScript Testing

<https://jestjs.io/>

<https://github.com/facebook/jest>

## Awesome Jest

<https://github.com/jest-community/awesome-jest>

## `jest-extended` - Additional Jest matchers

<https://github.com/jest-community/jest-extended>

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

```ruby
Dir.glob('src/*.test.*').each do |name|
  puts "\n\n*** Run test: #{name}"
  system("npx jest --runInBand --detectOpenHandles #{name}")
end
```

## Articles

[Why Is My Jest Test Suite So Slow? | by Steven Lemon](https://blog.bitsrc.io/why-is-my-jest-suite-so-slow-2a4859bb9ac0)
→ 한국어 번역:
[내가 작성한 Jest 테스트는 왜 이렇게 느릴까?](https://velog.io/@sehyunny/why-is-my-jest-test-suit-so-slow)
