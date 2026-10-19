# Coucou: 맥 노치에서 AI 코딩 에이전트를 지켜보는 오픈소스 동반자

<https://louis-cfm.github.io/coucou/>

<https://github.com/Louis-CFM/coucou>

## 소개

Coucou는 맥북 노치에 사는 작은 캐릭터 Mochi를 통해
AI 코딩 에이전트 세션을 보여 주는 앱이다.
Claude Code, Cursor, Codex, Gemini CLI, Antigravity, Copilot CLI,
OpenCode, Amp, Hermes 등의 세션이 무엇을 읽고 고치고 실행하는지
노치에서 단계별로 보여 준다.
Claude Code의 권한 요청에는 노치에서 Allow, Deny, Always로 답할 수 있고,
`AskUserQuestion` 질문도 노치에서 고를 수 있다.
노치가 없는 Windows와 Linux에서는 화면 위쪽 가장자리에서
섬(island)이 내려오는 방식으로 같은 기능을 제공한다.

Louis Raillé가 만들었고,
README는 Claude Code로 만들었다고 밝힌다.
저장소는 2026년 9월 27일에 만들어졌고,
2026년 10월 18일 기준으로 별 5,475개, 포크 956개를 받았다.
기여자 목록에서 커밋이 가장 많은 계정은 `claude`(271개)이고
저자 계정 `Louis-CFM`(251개)이 그 뒤를 잇는다.

README는 만든 동기를 이렇게 설명한다.
어떤 디자인 스튜디오들이 멋진 노치 동반자 콘셉트를 자랑했지만
아무도 쓸 수 없게 했으니, Coucou는 그 열린 버전이라는 것이다.

### 기능 범위

처음에는 에이전트 감시 도구였지만 기능이 빠르게 늘었다.

| 영역           | 내용                                                                          |
| -------------- | ----------------------------------------------------------------------------- |
| 에이전트 감시  | 세션별 단계, 파일 수정마다 `+N −M` 표시와 전체 diff, 터미널 창으로 이동       |
| 승인과 응답    | 권한 요청 Allow/Deny/Always, 최대 4개 질문의 선택지 응답, Codex Allow/Deny    |
| 채팅           | Claude, Gemini, OpenAI, DeepSeek, Qwen, Moonshot, Ollama, LM Studio           |
| 요금제 사용량  | Claude 5시간·주간 한도, Codex 한도와 남은 무료 리셋 횟수                      |
| 서비스 연동    | Stripe, n8n, GitHub, Vercel, Resend, Notion, Cal.com                          |
| 음성(0.4)      | 키를 누른 채 말하면 입력 위치에 붙여 넣는 Flow 받아쓰기, 오프라인 Parakeet    |
| 회의 기록(0.4) | 봇 없이 통화를 녹음해 화자별 전사, 요약, 할 일 생성                           |
| 기타           | 암호화폐 포트폴리오, Apple Music과 Spotify, 옷 갈아입기, 주간 리캡, 10개 언어 |

iPhone 앱은 맥이 잠긴 동안 Mochi를 잠금 화면과 Dynamic Island로 옮기고,
Face ID를 거쳐 권한 요청을 허용하게 한다.
Android 앱은 기여자 Rhytam Biswas가 만들었고,
같은 Wi-Fi에 있는 Windows나 Linux 앱과 연결된다.

## 저장소 구조

GitHub 언어 통계는 Swift 약 2.9MB, Rust 약 1.4MB, Kotlin 약 1.2MB,
TypeScript 약 0.9MB다.
플랫폼마다 네이티브에 가까운 별도 구현을 둔 결과다.

| 경로                            | 역할                                                    |
| ------------------------------- | ------------------------------------------------------- |
| `NotchBuddy/Sources/App/`       | macOS 앱(Swift 6, SwiftUI, AppKit)                      |
| `NotchBuddy/Sources/CoucouKit/` | Mac과 iPhone이 공유하는 Mochi 엔진, 필(pill), diff 엔진 |
| `NotchBuddy/Sources/Phone/`     | iPhone 앱과 위젯, 알림 확장                             |
| `windows/`                      | Windows와 Linux용 Tauri 2 앱(Rust + TypeScript)         |
| `windows/hook/`                 | 에이전트가 훅마다 실행하는 `coucou-hook` 중계기(Rust)   |
| `android/`                      | Kotlin과 Jetpack Compose로 만든 Android 앱              |
| `relay/`                        | Live Activity 푸시를 전달하는 무상태 Cloudflare Worker  |
| `design/`                       | 원본 HTML 프로토타입과 목표 화면 캡처                   |

macOS 앱은 서드파티 의존성이 전혀 없다고 README는 강조한다.
Mochi는 이미지나 Rive, Lottie 없이 SwiftUI `Canvas`와 `TimelineView`로
60fps로 그린다.
저장소의 `CLAUDE.md`는 에이전트에게 주는 규칙으로
Claude Code를 절대 막지 말 것, `~/.claude/settings.json`을 덮어쓰지 말 것,
명시적 클릭 없이 권한을 승인하지 말 것, 숨겨진 상태에서 CPU 0%를 유지할 것
등을 적어 둔다.

## 동작 방식

### 훅으로 이벤트를 받는다

Coucou는 에이전트의 훅 기능에 올라탄다.
macOS에서는 작은 `nb-hook` 스크립트가 Claude Code 훅 이벤트를 받아
Unix 소켓으로 앱에 넘긴다.
Windows에서는 `coucou-hook.exe`가 이름 있는 파이프(named pipe)를,
Linux에서는 `$XDG_RUNTIME_DIR` 아래 Unix 소켓을 쓴다.
OpenCode, Amp, Hermes는 훅 명령 대신 플러그인 파일을 설치하고,
그 밖의 에이전트는 `--agent <name>` 플래그로 연결한다.

`coucou-hook`의 `main.rs`는 에이전트마다 다른 이벤트 이름과 필드 이름을
Claude Code 형식으로 정규화한 뒤 앱에 전달한다.
예를 들어 Gemini CLI의 `BeforeTool` 이벤트는 `PreToolUse`로 바뀐다.

### 에이전트를 막지 않는 시간 예산

중계기의 핵심 규칙은 에이전트를 절대 막지 않는 것이다.
앱이 꺼져 있어 파이프가 없으면 아무 의견 없이 즉시 종료하고,
세션은 Coucou가 없는 것처럼 진행된다.
모든 단계는 메인 스레드가 강제하는 기한 아래에서 돌기 때문에,
연결만 받고 읽지 않는 파이프도 세션을 멈추지 못한다.

| 상수                     | 값    | 의미                                            |
| ------------------------ | ----- | ----------------------------------------------- |
| `CONNECT_TIMEOUT`        | 300ms | 파이프 연결을 기다리는 한도                     |
| `FIRE_AND_FORGET_BUDGET` | 2초   | 응답을 기다리지 않는 이벤트의 전체 실행 한도    |
| `DECISION_BUDGET`        | 110초 | 권한 요청이 화면에 머무는 한도, 넘으면 터미널로 |

응답을 기다리는 이벤트는 `PermissionRequest` 하나뿐이다.
110초 안에 결정이 오지 않으면 결정 없음으로 끝나고,
에이전트는 Coucou가 설치되지 않은 것처럼 터미널에서 다시 묻는다.

### 설정 파일은 병합하고 보여 준 뒤 쓴다

Claude Code 훅을 설치할 때 Coucou는 `~/.claude/settings.json`을 백업하고
자신의 훅을 병합한 뒤, 쓰기 전에 diff를 보여 준다.
Gemini CLI와 Antigravity도 각각의 설정 파일을 백업한다.

### 휴대폰으로 넘기는 경로

iPhone 연동은 사용자의 개인 CloudKit 데이터베이스를 거친다.
프로젝트 이름, 명령, 질문은 iCloud 키로 암호화되고,
iPhone이 써 넣은 결정은 맥이 기다리는 바로 그 요청과 일치할 때만 적용된다.
Live Activity 갱신에 필요한 APNs 키는 앱에 넣을 수 없으므로
`relay/`의 Cloudflare Worker가 들고 있으며,
이 Worker는 에이전트 이름과 상태만 본다.

Android 연동은 Windows와 Linux 앱 안의 선택형 서버로,
기본으로 꺼져 있고 로컬 네트워크에서만 동작한다.
페어링할 때 고정한 인증서로 TLS를 쓰고,
Allow에는 지문이나 화면 잠금이 필요하지만 Deny에는 필요 없다.
너무 길어 전부 보여 줄 수 없는 명령은 컴퓨터에서만 허용할 수 있다.

## 설치

macOS는 Releases에서 `Coucou.zip`을 받아 `/Applications`로 옮긴다.
Windows 설치 파일은 아직 코드 서명이 없어 SmartScreen 경고가 뜨고,
Linux는 AppImage, `.deb`, `.rpm`을 제공한다.
iPhone 앱은 TestFlight 베타이고, Mac App Store 판은 준비 중이다.
App Store 판은 샌드박스 제약 때문에 Claude 요금제 사용량,
Apple Music 필, 앞쪽 창 첨부 기능이 빠진다.

소스에서 빌드할 때 macOS는 XcodeGen을 쓴다.

```bash
brew install xcodegen
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/NotchBuddy
xcodegen
open NotchBuddy.xcodeproj   # Xcode에서 ⌘R로 실행
```

API 키 없이 기능을 둘러보려면 Settings → General → Demo의 데모 모드를 쓴다.
데모 중에는 키체인 항목, 훅 파일, 리캡 기록을 디스크에 쓰지 않는다.

## 라이선스

코드는 MIT 라이선스다.
그러나 `LICENSE-ASSETS.md`는 Coucou와 Mochi라는 이름, 캐릭터 디자인,
아이콘, 효과음, `docs/media/`와 `design/`의 이미지와 영상을
Louis Raillé의 권리로 남겨 둔다.
포크를 배포하려면 자신만의 이름, 아이콘, 캐릭터, 소리를 써야 한다.

## 분석

### 승인 지점을 터미널 밖으로 꺼낸다

Coucou가 푸는 문제는 에이전트를 실행하는 일이 아니라
에이전트가 사람을 기다리는 순간을 알아차리는 일이다.
에이전트가 길게 작업하는 동안 개발자는 다른 창에 가 있고,
권한 요청은 보이지 않는 터미널에서 멈춰 있다.
Coucou는 이 대기 상태를 노치, 잠금 화면, 휴대폰 알림으로 옮긴다.

이 설계가 성립하는 이유는 Claude Code가 훅에서
권한 결정을 돌려받는 경로를 열어 두었기 때문이다.
Coucou는 이 경로를 기준 규격으로 삼고,
다른 에이전트의 이벤트를 Claude Code 형식으로 번역한다.
결과적으로 Claude Code의 훅 규격이 이 생태계의
사실상 공통 프로토콜 역할을 한다.

### 실패하면 없는 것처럼 행동한다

중계기 코드에서 가장 공들인 부분은 기능이 아니라 실패 처리다.
300ms 안에 연결하지 못하면 포기하고,
응답이 없으면 결정하지 않은 채 터미널로 넘긴다.
이는 Coucou가 승인 경로에 끼어들면서도
그 경로의 단일 장애점이 되지 않으려는 설계다.

실패 시 기본값이 허용이 아니라 결정 없음이라는 점도 중요하다.
앱이 죽거나 휴대폰이 응답하지 않아도
명령이 저절로 승인되지 않는다.
iPhone과 Android 쪽에서도 결정이 기다리는 그 요청과 일치할 때만 적용하는 규칙이
같은 원칙을 따른다.

### 에이전트로 만든 에이전트 도구

저장소는 3주 남짓 동안 약 600개의 커밋을 쌓았고,
macOS 기준으로 9월 27일 0.1.0부터 10월 14일 0.4.0까지
16개 버전을 냈다.
커밋 수 1위가 `claude` 계정이고 저장소에 에이전트용 `CLAUDE.md`가 있다는 점은
이 속도가 에이전트 작업에서 나왔음을 시사한다.
에이전트를 지켜보는 도구를 에이전트로 만든다는 순환이
이 프로젝트의 성격을 설명한다.

## 비평

### 기능 확장이 도구의 정체성을 흐린다

README 첫 문단은 에이전트 감시를 말하지만,
지금 기능 목록에는 암호화폐 포트폴리오, Spotify 제어, 음성 비서,
받아쓰기, 회의 녹음이 함께 있다.
0.4는 아예 Coucou를 Wispr Flow 같은 받아쓰기 앱이라고 소개한다.
각 기능은 그럴듯하지만, 권한 승인이라는 민감한 경로를 맡은 앱이
마이크, 화면 녹음, 거래소 API 키, 이메일 발송까지 다루게 되었다.

공격 표면은 기능 수에 비례해 넓어진다.
사용자가 에이전트 승인 때문에 설치한 앱이
통화 오디오와 거래소 키를 함께 다루는 앱이 되는 것은
설치할 때 동의한 범위와 다르다.
README의 프라이버시 원칙은 데이터 전송에 관한 약속이지
권한 집중에 관한 답은 아니다.

### 원클릭 승인은 검토를 줄이는 방향으로도 작동한다

노치나 잠금 화면에서 Allow를 누르기 쉬워질수록
사람이 명령을 읽는 시간은 줄어든다.
Coucou는 파일 diff와 명령을 보여 주고,
Android에서는 너무 긴 명령을 휴대폰에서 허용하지 못하게 막는다.
이 장치들은 문제를 인식하고 있다는 증거다.

그러나 Always 버튼이 노치에 있고,
iPhone에서는 Face ID 한 번으로 허용된다.
Face ID는 누가 눌렀는지를 확인할 뿐
무엇을 허용하는지 읽었는지는 확인하지 않는다.
작은 화면에서 셸 명령을 읽는 일이 터미널보다 쉽지 않다는 점을
README는 다루지 않는다.

### 속도가 검증을 앞선다

17일 동안 16개 macOS 버전, 별도로 Windows·Linux·Android 릴리스가 나왔다.
`HookServer.swift` 한 파일이 약 181KB에 이를 만큼 코드가 빠르게 불었다.
권한 결정을 중계하는 코드가 이런 속도로 바뀔 때
각 릴리스가 어떤 검증을 거쳤는지는 README와 CHANGELOG만으로 알기 어렵다.

Windows 설치 파일에 코드 서명이 없다는 점도 같은 맥락이다.
README는 Microsoft Defender 검사에서 깨끗하다고 안내하지만,
서명 없는 설치 파일을 SmartScreen 경고를 넘겨 실행하라는 안내는
보안 관점에서 좋은 습관을 가르치지 않는다.

## 인사이트

### Claude Code 훅 규격이 사실상의 표준이 되고 있다

Coucou는 10개가 넘는 에이전트를 지원하지만,
내부에서는 모두를 Claude Code 이벤트 형식으로 바꾼다.
이런 도구가 늘수록 다른 에이전트는 Claude Code와 호환되는 훅을
제공하라는 압력을 받는다.
Cursor용 훅이 Claude Code 훅과 함께 자동으로 설치된다는 지원 표는
그 흐름이 이미 시작되었을 가능성을 보여 준다.

이는 한 제품의 확장 인터페이스가 생태계 표준으로 굳어진
과거 사례와 닮았다.
Language Server Protocol이 VS Code에서 출발해 편집기 전반의 규격이 된 것처럼,
훅 이벤트와 결정 응답 형식도 공식 표준 없이 수렴할 수 있다.
그렇게 되면 Claude Code가 훅 규격을 바꿀 때마다
주변 도구 전체가 따라가야 하는 의존이 생긴다.

### 사람의 승인 지점이 새로운 UI 경쟁 영역이 된다

에이전트가 더 오래 혼자 일할수록 사람이 개입하는 순간은 줄고,
남은 순간의 가치는 커진다.
Coucou는 그 순간을 노치, Dynamic Island, 휴대폰 알림, 위젯까지
끌어내는 데 기능 대부분을 쓴다.
에이전트 성능 경쟁 옆에서, 승인 순간을 어디에 띄울지를 두고
별도의 제품 경쟁이 생기고 있는 셈이다.

이 경쟁의 2차 효과는 승인의 의미가 바뀐다는 점이다.
승인이 터미널 앞에서 내리는 판단에서
주머니 속 알림에 대한 반사적 반응으로 옮겨 가면,
권한 시스템은 안전장치보다 알림 피로를 만드는 장치에 가까워진다.
승인 UI를 만드는 쪽은 편의보다
거절하기 쉬운 설계와 위험도에 따른 마찰을 경쟁 기준으로 삼아야 한다.

### 코드와 브랜드를 나눈 라이선스는 바이브 코딩 시대의 방어선이다

코드는 MIT로 열고 이름, 캐릭터, 소리는 묶어 둔 구조는
Coucou가 시작한 동기와 맞닿아 있다.
쓸 수 없는 콘셉트에 대한 반발로 모든 코드를 열었지만,
에이전트로 코드를 빠르게 복제할 수 있는 시대에
차별점으로 남는 것은 코드가 아니라 캐릭터와 경험이라는 판단이다.

포크가 956개에 이르는 상황에서
이 경계는 실제로 시험받게 된다.
에이전트에게 저장소를 주고 다른 이름으로 다시 만들라고 하면
코드는 몇 시간이면 갈라져 나온다.
그때 사용자가 원본을 고르는 이유는 Mochi라는 캐릭터와
승인 경로를 다루는 신뢰뿐이며,
후자는 라이선스가 아니라 검증 기록으로만 쌓인다.
