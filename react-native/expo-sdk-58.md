# Expo SDK 58: iOS 27과 React Native 0.88 대응, 업그레이드 가이드

원문: [Expo SDK 58 — Expo changelog](https://expo.dev/changelog/sdk-58)

HN 토론: <https://news.ycombinator.com/item?id=50119636> (2점, 0개 댓글)

## 소개

Expo SDK 58은 2026년 10월 15일에 공개된 릴리스다.
iOS 27과 React Native 0.88을 기준으로 만들어졌고, 이전 SDK는 React Native
0.86이었다.
변경은 크게 네 갈래다.
플랫폼 대응(iOS 27의 UIScene과 크기 조절, iPhone Duo), 개발 속도(Android 사전
빌드 `expo-modules-core`, Rust 변환기), 새 모듈(`expo-hinge`,
`expo-app-intents`, `expo-observe`, `expo-widgets`), 개발 도구(에이전트용
CLI)다.
이 노트는 업그레이드를 하는 사람이 먼저 알아야 할 깨지는 변경과 절차를 중심으로
정리한다.

## 주요 변경

### 플랫폼

iOS 27에서는 UIScene 생명주기가 필수이고 iPhone 앱의 크기가 조절될 수 있다.
`requireFullScreen`은 더 이상 크기 조절을 막지 못한다.
iPhone Duo를 지원하며, 새 `expo-hinge`가 `useHinge`, `getHinge`,
`addHingeListener`를 제공하고 Expo UI의 `ArrangementView`가 배치를 맡는다.
Xcode 27의 Device Hub를 지원하고 `expo-device-hub` 개발 도구 플러그인이
추가됐다.

### 모듈과 UI

`expo-app-intents`는 알파 단계다.
Expo UI는 재활용 리스트(`List`, `LazyVStack`, `LazyHStack`, `LazyColumn`,
`LazyRow`)와 iOS `NavigationStack` 관련 컴포넌트를 더했다.
`expo-observe`가 추가되고 AppMetrics는 deprecated 됐다.
`expo-widgets`로 Android 위젯을 만들 수 있고, Swift Package Manager 지원의 기반
작업이 들어갔다.

### 빌드 속도

Android용 `expo-modules-core`를 미리 빌드해 제공한다.
M3 Pro에서 클린 디버그 빌드가 약 80초에서 39초로 줄었다.
Expo Modules 2.0은 베타다.
실험 기능인 Rust 변환기 Noxcturnal은 `experiments.noxcturnalTransformWorker`로
켜며, 약 5,500개 파일에서 콜드 번들링이 5.26초에서 2.46초로 약 2배 빨라졌다.
Fingerprint의 기본값은 balanced 프리셋이다.

### Expo Router

데이터 로더, SSR, 미들웨어, 네이티브 탭이 stable이 됐고 서버 출력이 기본값이다.

### 에이전트 도구

`npx expo command:ps`와 `command:events`(실험)가 실행 중인 명령을 보여 준다.
`@expo/agent-cli`(별칭 `expo-agent-cli`)는 `status`, `dev`, `smoke`,
`skills:sync` 명령을 제공한다.
새 터널 `@expo/ws-tunnel`, PostHog 통합, `__expo_` 접두 실행 URL 파라미터도
추가됐다.

## 깨지는 변경

| 변경                         | 영향                                            |
| ---------------------------- | ----------------------------------------------- |
| `NODE_ENV`를 명령이 강제     | 직접 설정한 값이 덮어써질 수 있다               |
| Android R8 기본 활성화       | 리플렉션 의존 코드에 keep 규칙이 필요하다       |
| `File.write()`가 비동기      | 호출부에 `await`가 없으면 쓰기 완료를 보장 못함 |
| libSQL 제거                  | 사용하던 앱은 대체 경로가 필요하다              |
| 포그라운드 알림 기본 표시    | 알림 UX가 바뀐다                                |
| Node.js 22.13+ / 24.3+ / 26+ | 오래된 Node에서는 CLI가 동작하지 않는다         |
| RN Strict TypeScript API     | 타입 오류가 새로 나올 수 있다                   |
| macOS 지원 중단              | macOS 타깃은 SDK 58로 올릴 수 없다              |

## 업그레이드 절차

```bash
# 1. 의존성을 SDK 58 호환 버전으로 올린다
npx expo install expo@^58.0.0 --fix

# 2. 설정과 의존성 문제를 점검한다
npx expo-doctor

# 3. CNG(Continuous Native Generation)를 쓰면 네이티브 폴더를 지우고 다시 만든다
rm -rf android ios
npx expo prebuild --clean
```

위 명령 형태는 이 문서가 정리한 것이며, 정확한 버전 지정은 원문 업그레이드
안내를 따른다.

## 함정

### UIScene과 크기 조절은 레이아웃 가정을 깬다

iPhone 앱이 크기 조절될 수 있으므로 고정 해상도를 가정한 레이아웃은 깨질 수
있다.
`requireFullScreen`으로 우회할 수 없다는 점이 이번 변경의 핵심이다.

### R8과 비동기 쓰기는 조용히 실패한다

R8이 기본으로 켜지면 릴리스 빌드에서만 클래스가 제거되어 개발 중에는 드러나지
않는다.
`File.write()`가 비동기가 되면 `await`를 빠뜨린 호출이 컴파일 오류 없이 경쟁
상태를 만든다.
이 두 가지는 이 문서의 해석이며, 실제 영향은 앱마다 다르다.

### 실험 기능은 기본값이 아니다

Noxcturnal과 `command:events`는 실험이다.
번들링 속도 수치는 약 5,500개 파일의 한 프로젝트 측정이므로 자신의 프로젝트에서
다시 재야 한다.

## 체크리스트

- Node.js 버전이 22.13 이상, 24.3 이상 또는 26 이상인가.
- `NODE_ENV`를 직접 설정하는 스크립트를 확인했는가.
- 릴리스 빌드에서 R8로 제거되는 클래스가 없는지 확인했는가.
- `File.write()` 호출에 모두 `await`가 있는가.
- libSQL을 쓰는 코드가 있는가.
- iPhone에서 창 크기 조절 시 레이아웃이 유지되는가.
- 포그라운드 알림이 기본 표시되어도 괜찮은가.
- `npx expo-doctor`가 통과하는가.

## 기억할 원칙

### 버전 점프는 깨지는 변경부터 읽는다

새 기능은 선택이지만 깨지는 변경은 선택이 아니다.
이번 릴리스에서는 R8 기본 활성화와 `File.write()`의 비동기화처럼 컴파일러가 잡아
주지 않는 변경이 가장 위험하다.
업그레이드 전에 표의 항목을 코드베이스에서 검색해 영향 범위를 먼저 센다.
