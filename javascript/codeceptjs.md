# CodeceptJS

Effective End 2 End Testing for NodeJS

- <https://codecept.io/>
- <https://github.com/Codeception/CodeceptJS>

## Puppeteer Chrome Window Size

`codecept.conf.js`

- `windowSize`는 웹 브라우저 안의 뷰포트 크기에 영향.
- `--window-size` 플래그는 웹 브라우저 자체의 크기에 영향.

```javascript
exports.config = {
  // ...(중략)...
  helpers: {
    Puppeteer: {
      url: 'http://localhost',
      show: true,
      windowSize: '1024x768',
      chrome: {
        args: ['--window-size=1024,768'],
      },
    },
  },
  // ...(중략)...
};
```

## Example

- <https://github.com/ahastudio/CodingLife/tree/master/20190910/codeceptjs>
- <https://github.com/wholemann/atdd-practice-codeceptjs>
