# CallMe — Claude Code가 전화를 건다

<https://github.com/ZeframLou/call-me>

Claude Code 플러그인.
작업이 완료되거나 막혔을 때 AI가 사용자에게 직접 전화를 걸어
음성으로 대화할 수 있게 해준다.
스마트폰, 스마트워치, 유선전화 어디든 연결된다.

## 왜 주목해야 하는가

텍스트 기반 인터랙션을 넘어 **음성(Voice)**이라는 채널을
AI 에이전트에 부여한 실험적 프로젝트.
"AI가 나에게 전화한다"는 발상의 전환이 핵심이다.

기존 AI 코딩 도구들은 터미널 안에 갇혀 있다.
사용자가 화면 앞에 있어야만 소통이 가능하다.
CallMe는 이 한계를 부수고,
**개발자가 자리를 비운 사이에도 AI가 능동적으로 연락**할 수
있는 구조를 만들었다.

## 아키텍처

```
Claude Code
    ↓ stdio (MCP Protocol)
MCP Server (Bun + TypeScript)
    ├── Phone Provider (Telnyx / Twilio)
    │     ↕ HTTP Webhook + WebSocket
    ├── TTS Provider (OpenAI tts-1)
    │     → PCM 24kHz → mu-law 8kHz 변환
    ├── STT Provider (OpenAI Realtime API)
    │     ← mu-law 8kHz 직접 수신
    └── ngrok Tunnel
          ↕ 외부 Webhook 수신용 터널
```

세 겹의 프로바이더(Phone, TTS, STT)를
`ProviderRegistry`로 묶어 의존성 주입(DI) 패턴 적용.
전화 사업자를 Telnyx↔Twilio로 교체해도
나머지 코드를 건드릴 필요가 없다.

## 4가지 Tool

| Tool            | 역할                           |
|-----------------|--------------------------------|
| initiate_call   | 전화 걸기 + 첫 메시지 전달     |
| continue_call   | 대화 중 후속 질문              |
| speak_to_user   | 일방적 안내 (응답 불필요)      |
| end_call        | 통화 종료 + 마무리 메시지      |

Claude는 이 4가지 도구만으로
**멀티턴 음성 대화**를 수행한다.

## 코드 분석 — 핵심 포인트

### 오디오 파이프라인이 날것 그대로

TTS에서 받은 PCM 24kHz 오디오를 전화망이 요구하는
mu-law 8kHz로 직접 변환한다.
FFmpeg 같은 외부 도구 없이
**순수 TypeScript로 리샘플링과 mu-law 인코딩**을 구현했다.

```
PCM 16-bit 24kHz mono
  → resample24kTo8k() : 3샘플 평균으로 다운샘플링
  → pcmToMuLaw() : ITU-T G.711 mu-law 압축
  → 160바이트 청크로 분할 → WebSocket 전송
```

이 과정을 스트리밍으로도 처리한다.
`synthesizeStream()`이 AsyncGenerator로 청크를 넘기면
지터 버퍼(100ms)를 채운 뒤 실시간으로 전송한다.
**첫 음절까지의 지연(TTFB)을 최소화**하는 설계.

### Webhook 보안이 프로바이더별로 다르다

Twilio는 HMAC-SHA1, Telnyx는 Ed25519.
전혀 다른 서명 체계를 하나의 엔드포인트(`/twiml`)에서
Content-Type으로 분기 처리한다.

- `application/x-www-form-urlencoded` → Twilio
- `application/json` → Telnyx

Telnyx는 타임스탬프 기반 리플레이 공격 방어(5분 윈도우)도
포함한다.
WebSocket 연결에는 crypto 난수 토큰 +
timing-safe 비교를 적용했다.

### STT가 OpenAI Realtime API 직접 연결

`gpt-4o-transcribe` 모델에 WebSocket으로 직접 연결.
mu-law 오디오를 변환 없이 바로 전송한다.
서버 사이드 VAD(Voice Activity Detection)로
사용자 발화의 시작과 끝을 자동 감지한다.

연결이 끊어지면 지수 백오프(1s → 2s → 4s...)로
최대 5회 자동 재연결을 시도한다.

### 이중 트랜스포트 설계

MCP 서버는 Claude Code와 stdio로 통신하면서,
동시에 HTTP 서버를 별도로 띄워
전화 사업자의 webhook을 수신한다.
하나의 프로세스가 **두 가지 통신 채널**을 동시에 운영.

또한 `initiateCall()` 내부에서
TTS 오디오 생성(`ttsPromise`)을
전화 연결 대기(`waitForConnection`) **이전에** 시작한다.
전화벨이 울리는 동안 음성을 미리 합성해두어
사용자가 받자마자 바로 AI 목소리를 듣게 된다.

### Stop Hook의 절제된 설계

`plugin.json`의 Stop Hook에 이런 프롬프트가 있다:

> SILENTLY evaluate if you should call the user.
> ONLY use initiate_call if you completed significant work
> and need to discuss next steps,
> or are genuinely blocked.

AI가 매번 전화를 걸지 않도록 **자기 억제** 메커니즘을
프롬프트 레벨에서 심어둔 것이다.
사소한 일에 전화가 울리면 사용자 경험이 파괴되기 때문에,
"정말 중요할 때만 걸어라"는 원칙을 코드가 아닌
**프롬프트로 강제**한다.
LLM의 판단력을 신뢰하면서도 가이드라인을 명확히 제시하는
프롬프트 엔지니어링의 좋은 사례다.

## 인사이트

### AI 에이전트의 출력 채널 확장

텍스트 → 코드 → 음성.
AI 에이전트가 세상과 소통하는 방식이 계속 확장되고 있다.
CallMe는 "전화"라는 가장 보편적이고 즉각적인 채널을
AI에게 부여한 사례다.
다음은 무엇일까? 문자 메시지, 슬랙 허들, 화상통화?

### MCP + Plugin = 무한 확장

Claude Code의 플러그인 시스템이
MCP(Model Context Protocol) 서버를 감싸는 구조로
설계되어 있음을 보여준다.
stdio로 통신하고, tool을 등록하고,
webhook을 받는 것까지 하나의 패키지 안에 담긴다.
**MCP가 AI 에이전트의 "운영체제" 역할**을
하기 시작했다는 신호.

### Provider Pattern의 교과서적 적용

`PhoneProvider`, `TTSProvider`, `RealtimeSTTProvider`를
인터페이스로 추상화하고 팩토리 함수로 생성.
Telnyx와 Twilio가 완전히 다른 API 체계를 갖지만
(하나는 REST + JSON, 다른 하나는 REST + TwiML)
상위 계층은 동일한 코드로 동작한다.
**실전에서 Strategy Pattern을 적용하는 깔끔한 예시.**

### 비용 최적화 사고

Telnyx가 Twilio의 절반 가격($0.007/min vs $0.014/min).
분당 $0.03~0.04 수준으로 AI 음성 통화를 구현할 수 있다.
OpenAI TTS는 ~$15/1M chars.
비용 구조를 코드 주석과 README에 명시해둔 점에서
**오픈소스 프로젝트가 사용자의 지갑까지 배려**하는
좋은 관행을 볼 수 있다.

### ngrok 무료 티어 호환성

ngrok 무료 티어에서는 URL이 재시작마다 바뀌고
WebSocket 토큰 검증이 깨질 수 있다.
이를 위해 "ngrok compatibility mode"라는
폴백(fallback) 로직을 별도로 구현했다.
보안을 타협하지 않으면서도
**진입 장벽을 낮추는 실용적 엔지니어링**.

### 오디오 처리를 외부 의존성 없이

FFmpeg, SoX 같은 네이티브 바이너리에 의존하지 않고
리샘플링과 mu-law 인코딩을 순수 TypeScript로 구현.
약 40줄의 코드로 ITU-T G.711 표준을 충실히 재현했다.
설치 과정의 마찰을 없애면서도
**전화 품질에 충분한 오디오 처리**를 달성한 점이 인상적.

### 빌드 없는 실행

Bun이 TypeScript를 직접 실행하므로
컴파일 단계가 존재하지 않는다.
`bun run src/index.ts`로 바로 서버가 뜬다.
빌드 설정, tsconfig, 번들러 모두 불필요.
**개발 피드백 루프를 극한까지 단축**한 선택.

### ZeframLou의 정체

저자명 ZeframLou는 DeFi 생태계에서
EIP-4626(토큰화된 볼트 표준),
Timeless Finance 등으로 알려진 개발자.
블록체인/스마트컨트랙트 전문가가 만든
전화 플러그인이라는 점이 의외다.
**도메인을 넘나드는 빌더 정신**이 프로젝트에 녹아 있다.

## 설정

```bash
# 필요한 서비스
# 1. 전화 사업자: Telnyx (권장) 또는 Twilio
# 2. OpenAI API 키: TTS + STT 용
# 3. ngrok: Webhook 터널링

# 주요 환경변수
CALLME_PHONE_PROVIDER=telnyx
CALLME_PHONE_ACCOUNT_SID=...
CALLME_PHONE_AUTH_TOKEN=...
CALLME_PHONE_NUMBER=+1234567890
CALLME_USER_PHONE_NUMBER=+1234567890
CALLME_OPENAI_API_KEY=sk-...
CALLME_NGROK_AUTHTOKEN=...
```

## 참고

- 2.5k+ GitHub 스타
- TypeScript 100%, Bun 런타임
- MIT 라이선스
