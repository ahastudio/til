# Remotion

<https://github.com/remotion-dev/remotion>

## 소개

Remotion은 React로 비디오를 프로그래밍 방식으로 제작하는 프레임워크다.
슬로건은 “Make videos programmatically with React”이며,
전통적인 비디오 편집 소프트웨어 대신 코드로 비디오를 생성한다.

2021년 출시 이후 GitHub 스타 44,000개 이상을 기록하며 코드 기반 비디오 제작 분야의
사실상 표준(de facto standard)으로 자리잡았다.
GitHub Unwrapped(GitHub 연간 리뷰 개인화 비디오), Fireship의 유튜브 콘텐츠 등
프로덕션 레벨의 사용 사례로 검증됐다.

## 아키텍처

Remotion의 핵심은 React 컴포넌트를 비디오 프레임으로 변환하는 파이프라인이다.
각 프레임은 `useCurrentFrame()` 훅으로 현재 프레임 번호를 받아
결정론적으로 렌더링된다.

```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const MyComp = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  return <div style={{ opacity }}>Hello World</div>;
};
```

렌더링 파이프라인은 다음 단계로 구성된다:

```text
React 컴포넌트 → Webpack 번들링 → 헤드리스 Chrome
→ 프레임 캡처 → Rust 컴포지터 → FFmpeg → MP4
```

특히 Rust로 작성된 네이티브 컴포지터(`@remotion/compositor`)를 통해
프레임 인코딩을 가속한다.
이 컴포지터는 플랫폼별 바이너리로 배포된다(darwin-arm64, linux-x64 등).

## 주요 패키지

| 패키지                     | 역할                                       |
| -------------------------- | ------------------------------------------ |
| `remotion`                 | 핵심 훅, 시퀀스, 보간 유틸리티             |
| `@remotion/player`         | 브라우저 임베드 플레이어 컴포넌트          |
| `@remotion/lambda`         | AWS Lambda 분산 렌더링                     |
| `@remotion/serverless`     | 클라우드 서버리스 렌더링 추상화 레이어     |
| `@remotion/cloudrun`       | Google Cloud Run 렌더링                    |
| `@remotion/media-parser`   | 브라우저/Node.js 미디어 파일 파서          |
| `@remotion/captions`       | 자막 렌더링                                |
| `@remotion/skia`           | React Native Skia 통합                     |
| `@remotion/three`          | React Three Fiber (3D) 통합                |
| `@remotion/lottie`         | Lottie 애니메이션 통합                     |
| `@remotion/studio`         | 개발용 브라우저 스튜디오 환경              |
| `@remotion/mcp`            | MCP 서버 통합                              |

## 렌더링 방식

### 로컬 렌더링

```bash
npx remotion render MyComp out.mp4
```

헤드리스 Chrome이 각 프레임을 순차적으로 렌더링하고,
Rust 컴포지터와 FFmpeg가 이를 MP4로 인코딩한다.

### Lambda 분산 렌더링

`@remotion/lambda`는 AWS Lambda 함수 여러 개에 프레임 작업을 분산한다.
1,000개의 Lambda 함수가 병렬로 실행되어 렌더링 시간을 대폭 단축한다.
프로덕션 레디 수준의 분산 렌더링을 지원하는 것이 경쟁 도구 대비 최대 강점이다.

## 라이선스

Remotion은 소스 공개(source-available) 모델을 사용한다.
OSI 인증 오픈소스가 아니며, 규모에 따라 유료 라이선스가 필요하다:

| 대상                            | 라이선스                  | 비용           |
| ------------------------------- | ------------------------- | -------------- |
| 개인 / 직원 3인 이하 조직       | Free License              | 무료           |
| 비영리 / 교육 기관              | Free License              | 무료           |
| 직원 4인 이상 영리 조직         | Company License           | 좌석당 $25/월  |
| 자동화 렌더링 파이프라인 구축   | Remotion for Automators   | $0.01/렌더, 최소 $100/월 |
| 엔터프라이즈                    | Enterprise License        | $500+/월       |

## 분석

### React를 비디오 타임라인 모델로 재해석하다

Remotion의 핵심 통찰은 “시간을 함수의 입력 인자로 다루는 것”이다.
전통적인 NLE(Non-Linear Editor)는 타임라인 위에 클립을 배치하는 시각적 모델이다.
Remotion은 이것을 `frame → React 트리`라는 순수 함수 매핑으로 대체한다.

이 모델의 결과로 얻는 것은 결정론적 렌더링이다.
같은 프레임 번호에는 항상 같은 출력이 나온다.
이것은 재현성(reproducibility)과 테스트 가능성(testability)을 보장한다.

### React 생태계 전체를 비디오 도구로 전환하다

CSS, Canvas, SVG, WebGL, Three.js, Lottie, React Native Skia 등
웹 프론트엔드 생태계의 모든 렌더링 기술이 Remotion에서 그대로 사용된다.
새로운 비디오 효과 DSL을 배울 필요 없이,
이미 알고 있는 웹 기술로 비디오를 만들 수 있다.

패키지 수만 보더라도 `@remotion/skia`, `@remotion/three`, `@remotion/lottie`,
`@remotion/rive` 등 주요 애니메이션 런타임이 모두 래퍼로 지원된다.
이것은 기술 선택의 폭이 아니라, 기존 자산 재사용의 폭이다.

### Rust 컴포지터의 역할

성능이 중요한 프레임 인코딩 계층에 Rust 네이티브 컴포지터를 도입한 것이 주목할 만하다.
렌더링의 병목은 Chrome이 각 프레임을 그리는 것과,
그려진 프레임을 비디오로 인코딩하는 두 단계에서 발생한다.
Rust 컴포지터는 후자를 처리하며, 순수 JavaScript 대비 인코딩 속도를 끌어올린다.

## 비평

### 강점: Lambda 분산 렌더링이 프로덕션 도입의 결정적 이유다

개인이나 소규모 팀이 로컬 렌더링으로 시작해,
트래픽이 늘어나면 Lambda로 수평 확장할 수 있는 경로가 명확하다.
1,000개 Lambda 병렬 실행이라는 구체적인 수치는 단순한 마케팅이 아니라
GitHub Unwrapped 같은 실제 사례로 검증된 수치다.

경쟁 도구들이 단일 머신 렌더링에 머물러 있을 때,
Remotion은 이미 서버리스 분산 렌더링을 프로덕션 레디 수준으로 제공한다.
이 차이가 엔터프라이즈 도입에서 Remotion이 선택받는 핵심 이유다.

### 강점: 생태계 깊이가 신뢰를 만든다

44,000개 GitHub 스타, MCP 서버, ElevenLabs TTS 통합, Whisper 캡션,
Google Fonts, Bun 런타임 지원까지—패키지 목록만 봐도
수년간 커뮤니티 피드백을 반영해온 생태계의 깊이가 드러난다.
신생 경쟁 도구와 달리 실제 프로덕션 사용 사례에서 검증된 트레이드오프를 갖고 있다.

### 약점: 라이선스 모델이 오픈소스 생태계 편입을 막는다

“Source available” 모델은 소스 코드를 읽고 수정할 수 있지만,
OSI 오픈소스 정의를 충족하지 않는다.
직원 4인 이상 조직에서 유료 라이선스가 필요하다는 조건은
스타트업이나 SaaS 제품에 내재화할 때 법무 검토가 필요하다는 것을 의미한다.
Apache 2.0 하에 출시된 HyperFrames 같은 대안이 이 지점을 공략하고 있다.

### 약점: React 의존성이 진입 장벽이다

React를 모르거나 TypeScript 빌드 도구 체인에 익숙하지 않은 팀에게
번들러(Webpack) 설정과 TSX 컴포넌트 모델은 즉각적인 진입 장벽이다.
“HTML만 알면 된다”는 HyperFrames의 포지셔닝은
바로 이 약점을 직접적으로 겨냥한다.

## 인사이트

### “코드로 비디오를 만든다”는 것은 소프트웨어 엔지니어링의 영역 확장이다

Remotion이 대답하는 질문은 “어떻게 비디오를 더 쉽게 만들까”가 아니라
“소프트웨어 엔지니어가 비디오를 어떻게 만들어야 하는가”다.
이 질문의 전환이 중요하다.

전통적 비디오 편집은 GUI 중심 도구의 영역이었다.
타임라인을 마우스로 조작하고, 효과를 드래그하며, 렌더링 버튼을 누르는 워크플로우는
소프트웨어 엔지니어의 도구가 아니었다.
Remotion은 이 워크플로우를 코드, 버전 관리, CI/CD 파이프라인으로 끌어들인다.

깃헙 리포에 비디오 소스가 들어가고, PR로 리뷰되며,
배포 파이프라인에서 자동으로 렌더링된다.
“비디오도 코드다(Video as Code)”라는 패러다임은 이미 Fireship, GitHub Unwrapped 같은
사례에서 실현됐다. 앞으로 이 패러다임이 더 많은 데이터 시각화,
마케팅 자동화, 개인화 콘텐츠 생성 영역으로 확산될 것이다.

### 라이선스 모델이 오픈소스의 새로운 전선이 됐다

Remotion의 소스 공개 모델은 현재 소프트웨어 생태계에서
반복적으로 등장하는 긴장 관계의 한 사례다.
MongoDB의 SSPL, HashiCorp의 BSL, Elastic의 라이선스 변경과 같은
“코드는 공개하되 상업적 이익은 통제하는” 전략이 확산되고 있다.

Remotion의 선택은 일관된 논리 위에 있다.
개인과 소규모 팀은 무료로 쓰게 하고, 그 도구로 비즈니스를 운영하는
대규모 조직에서만 비용을 받는 것이다.
이것은 “오픈소스로 성장하고 엔터프라이즈에서 수익화”하는
전통적 오픈코어 모델의 변형이다.

HyperFrames가 Apache 2.0을 선택한 것은 이 긴장 관계에서
반대편 전략을 택한 것이다.
완전한 오픈소스로 신뢰를 확보하고, 다른 방식(클라우드 서비스, 지원 계약)으로
수익화를 모색하겠다는 베팅이다.
두 전략 중 어느 쪽이 옳은지는 지금 당장 판단하기 어렵지만,
이 경쟁 자체가 “지속 가능한 오픈소스”라는 미해결 문제를 드러낸다.

### 분산 렌더링은 비디오 생성 SaaS의 핵심 인프라다

Remotion Lambda가 해결하는 문제는 단순한 속도 향상이 아니다.
개인화된 대규모 비디오 생성이라는 새로운 비즈니스 모델을 가능하게 하는 인프라다.

GitHub Unwrapped는 한 시즌에 수십만 명의 개인화된 비디오를
자동으로 생성한다. 이것은 로컬 렌더링으로는 불가능하다.
Lambda 분산 렌더링이 있기 때문에 가능한 비즈니스 모델이다.

앞으로 “당신만을 위한 개인화 비디오”라는 형식의 마케팅,
사용자별 맞춤 리포트, 실시간 데이터 기반 뉴스 영상 등의
비즈니스 모델이 확산될 때, 그 인프라 계층이 Lambda 분산 렌더링이다.
Remotion은 이 인프라를 npm 패키지로 추상화해 제공한다는 점에서,
단순한 도구가 아니라 비디오 생성 SaaS 스택의 핵심 레이어를 노리고 있다.
