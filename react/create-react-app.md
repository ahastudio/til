# Create React App

> Create React apps with no build configuration.

<https://github.com/facebookincubator/create-react-app>

## 웹 브라우저 띄우지 않기

환경 변수 `BROWSER`는 사용할 웹 브라우저를 지정하는데 쓰인다.
이걸 `none`으로 설정하면 웹 브라우저가 뜨지 않는다.

`.env` 파일에 다음을 추가한다:

```txt
BROWSER=none
```

참고:
[Disabling opening of the browser in server start](https://github.com/facebookincubator/create-react-app/issues/873)

## Heroku로 배포

<https://github.com/ahastudio/til/tree/main/heroku#create-react-app>
