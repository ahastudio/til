# posthog-js의 `/sessionRecording` 버그: 맵의 키를 URL로 착각한 한 줄

원문: [Debugging Interesting Bugs at PostHog | Neil Kakkar](https://neilkakkar.com/debugging-open-source.html)

## 소개

Neil Kakkar가 2021년 5월 29일, PostHog에서 고친 버그 하나를 처음부터 끝까지 따라간 글이다.
세션 녹화 데이터가 PostHog 서버가 아니라 고객 사이트의 `/sessionRecording` 경로로 전송되고 있었다.
데이터를 잃고, 고객의 로그를 더럽히고, 자주 일어나는데 재현이 안 되는 버그였다.

PostHog는 Django 백엔드와 React 프런트엔드로 된 본 앱과, 고객 웹사이트에 넣는 통합 라이브러리로 나뉜다.
문제의 라이브러리는 `posthog-js`이고, 그 안의 세션 녹화 확장이 녹화를 캡처해 본 앱의 `/s/` 엔드포인트로 보내야 했다.
PostHog가 오픈소스라서 글은 가상의 예가 아니라 실제 코드와 실제 수정 PR로 설명한다.

글은 이 과정에서 원칙 네 가지를 뽑는다.
버그를 재현하라, 가설을 세우고 시험하라, 더 나은 도구가 일을 쉽게 한다, 실패하는 테스트를 써라.

## 동작 방식

### 버그가 생기던 경로

`posthog-js`의 `RequestQueue`는 보낼 이벤트를 모아 두었다가 주기적으로, 그리고 페이지를 떠날 때 한꺼번에 보낸다.
큐는 요청을 묶는 기준으로 URL을 쓰지만, 세션 녹화처럼 따로 묶어야 하는 요청은 `_batchKey` 옵션으로 다른 키를 준다.
`formatQueue()`는 이 키를 기준으로 요청을 모은 객체를 돌려주는데, 저자가 로그로 재구성한 모양은 이렇다.

```javascript
// formatQueue()가 돌려주는 객체의 모양.
// 키는 URL이거나, _batchKey가 있으면 그 값이다.
const requests = {
  sessionRecording: { url: '/s/', data: binaryData, options: { transport: 'sendbeacon' } },
  '/e/': { url: '/e/', data: binaryData, options: { transport: 'sendbeacon' } },
}
```

평소의 주기적 전송은 각 항목의 `url`을 제대로 썼다.
그런데 페이지를 떠날 때 부르는 `unload()`는 객체의 키를 URL로 썼다.

```javascript
// 수정 전 src/request-queue.js의 unload()
for (let url in requests) {
  const { data, options } = requests[url]
  this.handlePollRequest(url, data, { ...options, transport: 'sendbeacon' })
}
```

키가 URL과 같은 `/e/`는 문제없이 갔지만, 키가 `sessionRecording`인 녹화 데이터는 `sessionRecording`이라는 상대 경로로 보내졌다.
상대 경로는 고객 사이트를 기준으로 풀리므로, 요청은 고객 서버의 `/sessionRecording`에 도착했다.

### 수정

수정 PR(`posthog-js` #234, 2021년 5월 25일 병합)은 두 줄을 바꿨다.

```javascript
// 수정 후
for (let key in requests) {
  const { url, data, options } = requests[key]
  this.handlePollRequest(url, data, { ...options, transport: 'sendbeacon' })
}
```

변수 이름을 `url`에서 `key`로 바꾸고, 실제 URL은 항목 안에서 꺼낸다.
같은 PR에 `_batchKey`가 있는 이벤트를 넣고 `unload()`를 부른 뒤 세 요청이 각각 올바른 URL로 가는지 확인하는 테스트가 더해졌다.

### 왜 재현이 어려웠나

`unload()`는 페이지를 떠나는 순간에만 불린다.
저자는 로컬에 샘플 웹사이트와 PostHog를 띄우고, 들어오는 요청을 보여 주는 `http-server`를 붙인 뒤, 양쪽에서 세션 녹화를 켜고 새로 고침을 반복했다.
새로 고침의 약 50%에서 `/sessionRecording` 요청이 생겼고, 그는 파고들기에 충분한 비율로 봤다.

요청은 서버 로그에는 보이는데 DevTools 네트워크 탭에는 보이지 않았다.
새로 고친 직후에 생긴다고 생각했는데, 실은 새로 고치기 직전에 생긴 요청이라 로그 보존을 켜지 않은 네트워크 탭에서 사라진 것이었다.
로그 보존을 켜자 요청이 `ping` 유형으로 보였고, 그 정체는 `{transport: 'sendbeacon'}`이 쓰는 Beacon API였다.

## 트레이드오프

### `console.log`는 느리지만 어디서나 통한다

저자는 수백 개의 `console.log`로 범인을 찾았고, 스스로 초보 수준의 디버깅이었다고 평한다.
더 나은 방법으로 두 가지를 꼽는다.
압축된 코드 대신 소스 맵이나 압축하지 않은 코드를 쓰도록 개발 설정을 바꾸고, Chrome DevTools의 중단점을 쓰는 것이다.
중단점은 `console.log`가 보여 줄 것을 직접 로그를 찍지 않고도 보여 준다.

그런데 이 버그에서는 중단점이 도움이 안 되었다.
`unload` 이벤트는 신뢰하기 어렵고, Chrome은 페이지를 떠나는 순간에 멈추는 것을 잘 못한다.
그래서 그의 결론은 둘 다다.
디버거는 레이더처럼 전체를 보여 주고 무엇이 흥미로운지 고르게 하지만, 레이더가 안 통하는 곳에서는 원시적이지만 끈질긴 `console.log`가 남는다.

### 가설은 빠르게 세우는 것만큼 틀린 추론을 걸러 내는 것이 중요하다

빠른 디버거를 가르는 것은 좋은 가설로 탐색 공간을 얼마나 빨리 줄이느냐라고 저자는 쓴다.
3만 줄의 코드가 탐색 공간이고, `grep`은 맞으면 몇 줄로 줄여 준다.
실제로 그는 재현하기 전에 먼저 `sessionRecording`을 `grep`했고, 문자열이 나오는 곳은 말이 안 되는 한 군데뿐이었다.

더 비싼 실수는 시험 결과를 잘못 읽은 것이었다.
새로 고침을 누르고 서버 로그 화면으로 옮겨 가는 사이 요청이 보였으니, 새로 고침 뒤에 일어난 것처럼 느껴졌다.
컴퓨터는 사람보다 훨씬 빠르므로, 사람의 시간 감각으로 순서를 판단하면 틀린다.
그는 반증하는 증거를 찾아야 했다고 반성한다.

## 함정

### 객체의 키를 값처럼 쓰는 코드

`for...in`으로 객체를 돌 때 키 이름을 `url`이라고 붙이면, 키가 늘 URL이라는 가정이 코드에 새겨진다.
`_batchKey`처럼 키가 다른 의미를 갖게 되는 기능이 나중에 더해지면, 그 가정은 조용히 깨진다.
평소 경로가 올바른 `url` 필드를 썼기 때문에, 드물게 불리는 `unload()`만 틀린 채로 남았다.
같은 일을 하는 두 경로가 서로 다른 방식으로 데이터를 꺼내는 것 자체가 이 버그의 온상이다.

### 상대 경로는 실행되는 페이지를 기준으로 풀린다

`handlePollRequest`에 `sessionRecording`이 전달되자 요청은 오류 없이 나갔다.
상대 경로는 유효한 URL이고, 브라우저는 현재 페이지의 출처를 기준으로 그것을 풀었다.
라이브러리가 고객 사이트 안에서 도는 한, 잘못된 상대 경로는 실패 대신 엉뚱한 서버로 가는 요청이 된다.
외부 서버로 보내는 라이브러리라면 전송 직전에 URL이 절대 경로인지, 기대한 호스트인지 확인하는 편이 안전하다.

### 떠나는 순간의 요청은 보이지 않는다

페이지를 떠날 때 보내는 Beacon 요청은 네트워크 탭의 로그 보존을 켜지 않으면 사라진다.
그리고 중단점도 잘 걸리지 않는다.
언로드 경로에서만 생기는 버그는, 서버 쪽에서 요청을 받아 보는 것이 가장 확실한 관찰 방법이다.

## 확인하기

### 수정 전 코드에서 테스트가 실패하는지 본다

저자의 네 번째 원칙은 테스트가 수정 전에는 실패하고 수정 후에는 통과하는지 확인하라는 것이다.
TDD처럼 테스트를 먼저 쓰라는 뜻은 아니다.
그의 순서는 이렇다.

```bash
# 1. 수정과 테스트를 브랜치에 커밋한다.
git switch -c fix-session-recording
# ... 수정, 테스트 작성, 커밋 ...
npx jest src/__tests__/request-queue.js      # 통과해야 한다

# 2. 테스트 파일만 남기고 코드를 수정 전으로 되돌려 다시 돌린다.
git checkout master -- src/request-queue.js
npx jest src/__tests__/request-queue.js      # 이번에는 실패해야 한다

# 3. 원래대로 돌려놓는다.
git checkout fix-session-recording -- src/request-queue.js
```

수정 전 코드에서도 테스트가 통과한다면, 엉뚱한 것을 시험하고 있거나, 테스트가 동작하지 않거나, 수정이 실제로 문제를 고치지 못한 것이다.

### 로컬에서 언로드 요청을 관찰한다

```bash
# 들어오는 모든 요청을 로그로 보여 주는 정적 서버
npx http-server ./playground -p 8080
```

1. 샘플 페이지에 스니펫을 넣고 세션 녹화를 켠다.
2. 브라우저 DevTools의 네트워크 탭에서 로그 보존(Preserve log)을 켠다.
3. 새로 고침을 여러 번 하며 서버 로그에 `/sessionRecording` 같은 예상 밖의 경로가 오는지 본다.
4. 네트워크 탭에서 유형이 `ping`인 요청을 찾아 요청 본문과 대상 URL을 확인한다.

## 기억할 원칙

### 실패를 본 테스트만 믿는다

이 글에서 가장 오래 남을 습관은 네 번째 원칙이다.
테스트가 통과하는 것만 보면, 그 테스트가 무엇을 증명하는지 알 수 없다.
수정 전 코드에서 실패하는 것을 보고 나서야, 그 테스트가 이 버그를 잡는다는 것을 안다.

같은 원리가 가설에도 적용된다.
새로 고침 뒤에 요청이 생긴다는 가설은, 그것을 반증할 증거를 찾지 않았기 때문에 오래 살아남았다.
디버깅에서도 테스트에서도, 틀릴 수 있는 방식으로 시험해 본 주장만 믿을 수 있다.
