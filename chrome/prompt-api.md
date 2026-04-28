# Chrome Prompt API — 브라우저 내장 온디바이스 AI

<https://developer.chrome.com/docs/ai/prompt-api>

## 개요

Chrome Prompt API는 브라우저 안에서 직접 Gemini Nano에 자연어 요청을 보낼 수 있는
웹 API다. 서버 없이 온디바이스(on-device)로 추론이 이루어지므로, 네트워크 레이턴시와
클라우드 API 비용 없이 생성형 AI 기능을 웹 앱에 내장할 수 있다. Chrome 138부터
사용 가능하며, 샘플링 파라미터 관련 오리진 트라이얼(origin trial)은 Chrome 148에서
시작된다.

텍스트·오디오·이미지를 입력으로 받고 텍스트를 출력한다. 현재 지원 언어는 영어(`en`),
일본어(`ja`), 스페인어(`es`)다. 데스크톱 전용으로, 모바일 Chrome과 iOS는 현재
지원하지 않는다.

## 하드웨어 요구사항

| 항목       | 요구사항                                          |
| ---------- | ------------------------------------------------- |
| OS         | Windows 10/11, macOS 13+, Linux, ChromeOS        |
| 스토리지   | 22 GB 이상 여유 공간                              |
| GPU        | VRAM 4 GB 초과 (오디오 입력 시 필수)              |
| CPU        | RAM 16 GB 이상, 코어 4개 이상 (GPU 대체 가능)     |
| 네트워크   | 최초 모델 다운로드 시 무제한/무과금 연결 필요     |

## API 명세

### 가용성 확인 및 세션 생성

```javascript
const availability = await LanguageModel.availability({
  expectedInputs: [{ type: 'text', languages: ['en'] }],
  expectedOutputs: [{ type: 'text', languages: ['en'] }]
});

const session = await LanguageModel.create();
```

`LanguageModel.availability()`는 현재 지원 여부를 반환한다.
`LanguageModel.create()`로 세션을 생성하며, 다음 옵션을 받는다.

| 옵션              | 설명                                            |
| ----------------- | ----------------------------------------------- |
| `temperature`     | 응답 무작위성 조정 (Extensions 전용)            |
| `topK`            | 토큰 샘플링 파라미터 (Extensions 전용)          |
| `signal`          | 세션 중단용 `AbortSignal`                       |
| `initialPrompts`  | 이전 대화 복원용 메시지 배열                    |
| `expectedInputs`  | 입력 모달리티/언어 명세                         |
| `expectedOutputs` | 출력 모달리티/언어 명세                         |

### 프롬프트 메서드

```javascript
// 단순 응답
const result = await session.prompt('Write me a poem!');

// 스트리밍 응답
const stream = session.promptStreaming('Write an extra-long poem!');
for await (const chunk of stream) {
  console.log(chunk);
}

// 중단 가능한 요청
const result = await session.prompt('...', { signal: controller.signal });
```

### JSON Schema 구조화 출력

```javascript
const schema = { type: 'boolean' };
const result = await session.prompt(prompt, {
  responseConstraint: schema,
  omitResponseConstraintInput: true
});
```

`responseConstraint`에 JSON Schema를 전달하면 모델 출력이 해당 스키마를 준수하도록
강제된다. `omitResponseConstraintInput`은 스키마 정의 자체를 컨텍스트에서 제외해
토큰을 절약하는 옵션이다.

### 멀티모달 입력

```javascript
const session = await LanguageModel.create({
  expectedInputs: [
    { type: 'text', languages: ['en'] },
    { type: 'audio' },
    { type: 'image' }
  ]
});
```

- **오디오**: `AudioBuffer`, `ArrayBufferView`, `ArrayBuffer`, `Blob`
- **이미지**: `HTMLImageElement`, `HTMLVideoElement`, `HTMLCanvasElement`,
  `ImageBitmap`, `OffscreenCanvas`, `VideoFrame`, `Blob`, `ImageData` 등

### 컨텍스트 관리

```javascript
console.log(`${session.contextUsage}/${session.contextWindow}`);

session.addEventListener('contextoverflow', () => {
  console.log('Context window exceeded; earliest messages removed');
});

const cloned = await session.clone({ signal: controller.signal });
session.destroy();
```

세션은 토큰 윈도우 안에서 대화 맥락을 유지한다. 한계에 도달하면 가장 오래된 메시지가
자동으로 제거된다. `clone()`으로 세션을 복제하고, `destroy()`로 리소스를 해제한다.

### 기타 메서드

- `session.append()`: 세션 생성 이후 컨텍스트 프롬프트 추가
- `session.measureContextUsage()`: 토큰 소비량 사전 측정
- `LanguageModel.params()`: `defaultTopK`, `maxTopK`, `defaultTemperature`,
  `maxTemperature` 반환

## 분석

### 온디바이스 AI의 기술적 포지셔닝

Prompt API는 클라우드 AI와 경쟁하는 것이 아니라 보완 관계를 형성한다. 네트워크가
없거나 불안정한 환경, 레이턴시가 극도로 중요한 인터랙션, 사용자 데이터를 서버에
보내고 싶지 않은 프라이버시 민감 상황에서 온디바이스 추론이 우위를 가진다. 반면
복잡한 추론, 대용량 출력, 최신 정보가 필요한 작업은 여전히 클라우드 AI의 영역이다.

멀티모달 입력 지원(텍스트 + 오디오 + 이미지)은 Gemini Nano의 역량을 웹 플랫폼에
직접 노출하는 설계다. 특히 오디오 입력이 GPU를 필수로 요구한다는 점은 추론 비용과
하드웨어 의존성이 여전히 높다는 현실을 반영한다.

### JSON Schema 구조화 출력의 의의

`responseConstraint`는 LLM 출력을 구조화된 데이터로 변환하는 표준 패턴을 API
수준에서 지원한다. 이는 자연어 응답을 파싱하던 기존 방식 대비 신뢰성을 크게 높인다.
JSON Schema 호환 구조화 출력은 이미 OpenAI, Anthropic 등 클라우드 AI 업체들이 제공하는
기능인데, 브라우저 내장 API가 이를 채용했다는 점은 구조화 출력이 AI API의 표준
인터페이스로 자리잡았음을 보여준다.

### 세션 모델과 컨텍스트 관리

세션(session) 추상화는 상태 없는 HTTP 요청 위에 상태 있는 대화 흐름을 구축하는
패턴이다. `contextoverflow` 이벤트와 자동 메시지 제거는 개발자가 명시적으로 관리해야
했던 토큰 윈도우 문제를 브라우저가 처리하는 방향을 보여준다. `clone()`으로 세션을
분기하면 다른 맥락으로 실험하면서 원본 대화를 유지할 수 있다.

### Extensions 전용 파라미터의 함의

`temperature`와 `topK` 조정이 Extensions 전용이라는 제약은 일반 웹 개발자에게
의도적 제한을 가한다. 이유는 명시되지 않았지만, 모델 오남용 방지와 일관된 사용자
경험 유지로 추측할 수 있다. Extensions는 더 엄격한 배포 검토를 거치므로 추가
권한을 신뢰할 수 있다는 Chrome의 신뢰 모델이 API 설계에 반영된 것이다.

## 비평

### 강점

멀티모달 입력과 스트리밍, 구조화 출력, 세션 복제를 포함한 기능 범위가 넓다. 특히
`responseConstraint`는 단순한 텍스트 생성을 넘어 데이터 추출, 분류, 검증 파이프라인에
실용적으로 쓸 수 있는 기능이다. AbortSignal 지원으로 사용자 인터랙션에서 흔히
필요한 요청 취소 패턴을 자연스럽게 처리한다.

공식 문서가 코드 예제를 충분히 제공하며, 준수해야 할 정책(금지 사용 정책, People +
AI Guidebook)을 명시적으로 안내한다. 이는 브라우저 레벨에서 책임 있는 AI 사용을
개발자에게 상기시키는 설계다.

### 약점 및 한계

하드웨어 요구사항이 상당히 높다. 22 GB 스토리지와 4 GB VRAM 조건은 보급형 기기에서
동작하지 않음을 의미한다. 온디바이스 AI의 핵심 가치인 “어디서나 작동”을 스스로
제한한다. 모바일 Chrome 미지원은 실사용 기반의 상당 부분을 배제한다.

언어 지원이 영어·일본어·스페인어 세 가지뿐이다. 전 세계 웹 사용자를 고려하면 매우
좁은 범위로, 한국어를 포함한 대다수 언어 사용자는 기능 자체를 활용하기 어렵다.

Web Workers 미지원은 무거운 AI 작업을 백그라운드 스레드로 옮기지 못한다는 의미다.
메인 스레드에서 긴 추론이 실행되면 UI 응답성이 저하될 수 있다. 온디바이스 추론의
현실적 제약을 API 설계가 아직 해결하지 못한 지점이다.

`temperature`와 `topK`를 Extensions 전용으로 제한하는 것은 일반 웹 개발자에게
지나치게 불투명한 제약이다. 모델 동작을 미세 조정할 수 없다면 특정 사용 사례에서
결과 품질을 개선하는 수단이 없다.

## 인사이트

### 브라우저가 AI 런타임이 되는 날의 의미

Prompt API가 표준화된다면 브라우저는 단순한 문서 렌더러를 넘어 AI 추론 런타임이
된다. 이것은 JavaScript 엔진이 브라우저에 내장된 것, WebGL이 GPU 연산을 웹에 열어준
것과 같은 계보의 변화다. 각 전환점마다 웹 개발자가 할 수 있는 일의 범위가 근본적으로
달라졌다. AI 추론이 표준 브라우저 기능이 된다면, 설치가 필요한 네이티브 앱의 마지막
차별점 중 하나가 사라진다.

구체적으로 어떤 변화가 일어날 것인지 생각해보면, 오늘날 클라우드 API 호출로 구현하는
AI 기능들이 점진적으로 온디바이스로 내려올 것이다. 텍스트 분류, 감정 분석, 간단한
Q&A, 콘텐츠 요약처럼 추론 비용이 낮은 작업은 서버 없이 브라우저에서 처리된다.
프론트엔드 개발자가 백엔드 없이 AI 피처를 출시하는 패턴이 현실화된다.

하드웨어 요구사항이 낮아지는 속도와 함께 이 전환의 속도가 결정된다. 현재의 22 GB
스토리지, 4 GB VRAM 조건은 2026년 기준 보급형 기기의 한계를 넘는다. 그러나 모델
경량화와 양자화(quantization) 기술이 빠르게 발전하고 있어, 2~3년 내에 조건이 상당히
완화될 가능성이 높다. 이 임계점을 넘는 순간 온디바이스 AI의 실용 범위가 급격히 확대된다.

### `responseConstraint`가 열어주는 새로운 개발 패러다임

JSON Schema 구조화 출력은 LLM을 “대화 상대”가 아닌 “데이터 변환 파이프라인”으로
쓰는 패턴을 공식화한다. 지금까지 개발자들은 자연어 출력을 직접 파싱하거나,
프롬프트에 “JSON으로만 답하라”는 지시를 넣고, 파싱 실패에 대비한 재시도 로직을
작성해야 했다. `responseConstraint`는 이 번거로움을 API 수준에서 해결한다.

이 패러다임 전환의 실용적 함의는 크다. 사용자 입력에서 구조화된 데이터를 추출하는
작업(폼 자동 완성, 텍스트에서 캘린더 이벤트 파싱, 연락처 정보 추출)이 서버 왕복
없이 브라우저에서 처리될 수 있다. 기존에는 서버에서 LLM API를 호출하고 결과를
다시 클라이언트에 전달하는 구조였다면, Prompt API + responseConstraint 조합은 이
파이프라인 전체를 클라이언트에서 완결한다.

장기적으로 이는 서버리스 AI 파이프라인의 새로운 형태를 만든다. 민감한 사용자
데이터(의료 정보, 재무 데이터)를 서버에 보내지 않고 로컬에서 처리하는 프라이버시
우선 설계가 가능해진다. GDPR 같은 데이터 보호 규제가 강화될수록, 온디바이스 데이터
처리의 경쟁 우위가 커진다.

### 브라우저 AI 표준화 경쟁과 웹 플랫폼의 미래

Chrome Prompt API는 현재 Chromium 전용이다. Firefox와 Safari가 동일한 API를 구현하지
않는다면 이것은 표준이 아닌 벤더 락인(vendor lock-in)이다. 역사적으로 이런 상황은
두 방향으로 전개되었다. ActiveX처럼 결국 사장되거나, WebRTC처럼 표준화되어 모든
브라우저에 채택되거나.

현재 W3C와 WICG(Web Incubator Community Group)에서 AI API 표준화 논의가 진행 중이다.
Chrome Prompt API의 `LanguageModel` 인터페이스가 그 출발점이 될 가능성이 있다.
Google이 Chrome으로 AI 기능을 시범 도입하고, 채택이 충분히 이루어지면 표준화를
제안하는 패턴은 Web Bluetooth, Web USB 등에서 반복된 전략이다. Prompt API도 같은
궤적을 따를 가능성이 높다.

웹 개발자로서 지금 취해야 할 입장은 신중한 탐색이다. API가 아직 안정화되지 않았고
표준 여부가 불투명하다. 그러나 완전히 무시하면 표준화 이후 뒤처지는 리스크가 있다.
`LanguageModel.availability()` 패턴처럼 기능 감지(feature detection)를 전제로 한
점진적 향상(progressive enhancement) 방식으로 적용하는 것이 현재 최선이다. 온디바이스
AI가 가능하면 쓰고, 그렇지 않으면 클라우드 API로 폴백하는 구조가 앞으로 몇 년간의
표준 아키텍처 패턴이 될 것이다.
