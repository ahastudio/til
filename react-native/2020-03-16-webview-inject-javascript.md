# WebView에서 JavaScript 실행하기

React Native(Expo)로 웹 페이지를 띄우고,
JavaScript를 실행하는 방법에 대해 간단히 알아보겠습니다.

## Instagram 간단 분석

Instagram에 있는 사진을 메뉴 등 없이 간단히 보고 싶습니다.
대단히 좋은 방법이 많이 있지만,
여기서는 JavaScript를 이용해 불필요한(?) 요소를 제거하는 방법을 취하겠습니다.

우리가 볼 사진은 이겁니다.

[![누구도 멈출 수 없다](https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/s640x640/88903499_195665645024364_1065843067895298031_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=100&_nc_ohc=akiS3rNkwbUAX_hqEM0&oh=6f4fa846e72be295971947bf9188db90&oe=5EA61A36)](https://j.mp/2TUStFU)

Instagram의 해당 페이지를 보면 사진 외의 요소가 많습니다.

Google Chrome의 개발자 도구를 열여서 우리가 제거할 요소를 찾아보면 다음과 같습니다:

1. 상단 메뉴: `nav`
1. 하단 메뉴: `footer`
1. 게시물 작성자: `article > header`
1. 게시물 설명 및 댓글: `article > div:nth-of-type(2)`
1. 게시물 메뉴: `article > div:nth-of-type(3)`

이들을 지워주는 코드를 JavaScript로 간단히 써봅시다.

```javascript
document.querySelector('nav').remove();
document.querySelector('footer').remove();
document.querySelector('article > header').remove();
document.querySelector('article > div:nth-of-type(3)').remove();
document.querySelector('article > div:nth-of-type(2)').remove();
```

완벽하진 않지만 일단 이 정도만 실행하도록 하죠.

## React Native 앱 만들기

Expo를 이용해 `instaview` 앱을 만들어 봅시다.

```bash
npx -p expo-cli expo init instaview
```

여기선 그냥 가장 간단한 blank template을 사용합니다.

프로젝트 폴더로 이동해서 `expo-cli` 의존성을 추가합니다.

```bash
cd instaview

npm install --save-dev expo-cli
```

`WebView`도 설치합니다.

```bash
npx expo install react-native-webview
```

Expo Developer Tools를 실행합니다.

```bash
npm start
```

## WebView 띄우기

`App.js` 파일을 다음과 같이 단순화합니다.

```javascript
import React from 'react';
import { WebView } from 'react-native-webview';

export default function App() {
  return (
    <WebView
      source={{ uri: 'https://www.instagram.com/p/B9PB--QjTDg/' }}
    />
  );
}
```

그냥 평범한 인스타그램 웹 페이지가 나왔습니다.

## JavaScript 코드 주입하기

[`WebView`](https://j.mp/2Wjeujs)엔
`injectJavaScript`와 `injectedJavaScript`가 있습니다.
JavaScript를 언제 실행하는지 차이가 있는데,
여기선 `injectedJavaScript`를 이용해 로딩된 후에 JavaScript 코드를 실행하도록 하겠습니다.

```javascript
import React from 'react';
import { WebView } from 'react-native-webview';

const script = `
  document.querySelector('nav').remove();
  document.querySelector('footer').remove();
  document.querySelector('article > header').remove();
  document.querySelector('article > div:nth-of-type(3)').remove();
  document.querySelector('article > div:nth-of-type(2)').remove();
`;

export default function App() {
  return (
    <WebView
      source={{ uri: 'https://www.instagram.com/p/B9PB--QjTDg/' }}
      injectedJavaScript={script}
    />
  );
}
```

이렇게 아주 간단히 우리가 원하는 결과를 만들 수 있습니다.
