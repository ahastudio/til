# chrome-capture: Chrome 탭 녹화 도구

<https://paulirish.github.io/chrome-capture/>

<https://github.com/paulirish/chrome-capture>

HN 토론: <https://news.ycombinator.com/item?id=50427075> (3점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=37379>

## 소개

Chrome 탭의 화면과 소리를 AV1 `.mp4`로 직접 저장하는 Node.js 도구이다.
GitHub 사용자 paulirish의 저장소이다.
소스 코드, 벤치마크 문서(`benchmarks/README.md`), 예제는 열지 않았고 직접 설치해 써 보지도 않았다.
설명과 수치는 모두 저장소의 주장이다.

GitHub API로 읽은 시점(2026년 11월 18일)의 수치는 별 512개, 포크 9개, 열린 이슈 0개, 라이선스 Apache-2.0, 언어 TypeScript, 생성일 2026년 11월 8일, 마지막 푸시 2026년 11월 17일이다.
홈페이지는 이 도구의 스트레스 테스트 데모이고 읽은 시점의 문서 제목이나 설명 텍스트가 없었다. README는 이 페이지가 프레임마다 이진 프레임 카운터를 그린다고 설명한다.

핵심은 Chrome의 새 녹화 API를 쓴다는 점이다.

- 배경: 약 10년 동안 CDP에서 영상 프레임을 얻는 방법은 2013년경 만든 `Page.startScreencast` 하나였다고 한다. Chrome이 프레임을 JPEG로 인코딩해 base64로 JSON에 담아 CDP로 보내고 응답을 기다리면 라이브러리가 그 JPEG를 `ffmpeg`로 넘긴다. Playwright의 `recordVideo`와 Puppeteer의 `page.screencast()`가 이 위에 만들어졌다.
- 새 방식: 2026년 9월에 `Page.startScreenRecording`이 들어왔다고 한다(Chrome 153 이상). 프레임이 컴포지터에서 공유 메모리로 프로세스 밖 인코더에 바로 가고 Chrome이 진행하면서 AV1을 mp4에 쓴다. 탭 오디오도 선택할 수 있다. 종료가 거의 즉시이고 녹화를 원하는 구간에서만 시작하고 멈출 수 있다고 한다.
- 도구의 쓰임: `npx chrome-capture <주소> <파일> <길이>`로 URL을 녹화한다. 기본은 720p 60fps이고 탭 오디오도 녹음하며, 60fps 이하는 헤드리스로 돌고 `--fps`가 60을 넘으면 macOS에서 자동으로 헤드풀로 바꿔 ProMotion 120Hz에 맞춘다고 한다. 옵션으로 해상도, 프레임 속도, DevTools 동시 녹화(`--with-devtools`)가 있다.
- 라이브러리: `startRecording()`이 Playwright `Page`, Puppeteer `Page`, CDP 세션 중 무엇이든 받고 `await using`으로 블록이 끝날 때 mp4를 쓴다. `@playwright/test` 픽스처가 모든 테스트를 녹화해 리포트에 첨부하고, 원시 CDP용 클래스(`CdpScreenRecorder`)도 있다. Puppeteer v25.10 이상은 이 API를 실험적 `page.record()`로 감싸고 `page.screencast()`는 폐기 예정이라고 한다. Playwright는 같은 기능을 위한 PR이 열려 있다고 README가 적는다(11월 10일 갱신).
- 요구 사항: Chrome/Chromium 153 이상과 Node.js 24.11 이상이다(GeekNews 토픽 요약에서 읽었다).

README의 벤치마크는 M4 Max에서 같은 6.4초 UI 재생(1280x800)을 비교한다.

| 항목                      | `recordVideo` (`startScreencast`) | `chrome-capture` (`startScreenRecording`) |
| ------------------------- | --------------------------------- | ----------------------------------------- |
| 출력 fps                  | 25 (최대 60)                      | 60 (최대 120)                             |
| 전체 소요                 | 21초                              | 11초                                      |
| 종료와 마무리             | 3,800밀리초                       | 17밀리초                                  |
| WebSocket 트래픽          | 10.5MB                            | 450KB                                     |
| 최종 파일 크기            | 480KB                             | 330KB                                     |
| 무손실 스크린샷 대비 PSNR | 32dB                              | 34dB                                      |
| 오디오                    | 없음                              | 선택                                      |

README가 밝힌 한계와 조건은 다음과 같다.

- 비트레이트 조절이 아직 없다. Chrome이 `libaom` AV1 실시간 1패스 VBR로 인코딩하고 목표 비트레이트를 픽셀 속도에 선형으로 맞춘다(720p30에서 2Mbps, 1080p60에서 9Mbps, 1080p120에서 18Mbps, 2160p120에서 72Mbps). 무손실 1픽셀 글자 품질이 필요하고 초당 10프레임에서 15프레임이면 되는 경우 오프라인 PNG 스크린캐스트와 `ffmpeg` 경로가 여전히 쓸모 있다고 한다.
- 최고 성능 측정(프레임마다 이진 카운터를 그려 영상에서 고유 프레임을 세는 방식): 맥 헤드리스 2160p 60fps, 120Hz ProMotion 맥 헤드풀 1080p와 2160p 120fps(119.9fps), 헤드리스 리눅스(GPU 없음) 1080p 60fps이다. Windows와 개별 GPU 리눅스는 물음표로 남아 있다.
- 맥에서는 `--disable-frame-rate-limit --disable-gpu-vsync`를 쓰지 말라는 주의가 있다. rAF가 초당 수천 번 돌아 Metal 큐를 막아 2160p 60fps가 0.3fps로 떨어진다고 한다.

## 분석

### 중심 주장은 녹화가 브라우저 안에서 끝난다는 것이다

기존 방식은 프레임을 JPEG로 바꿔 CDP로 보내고 `ffmpeg`에 넘겨 영상을 만들었다.
새 API는 인코딩을 Chrome 안에서 하므로 전송량이 줄고(10.5MB에서 450KB) 종료 시 마무리 지연이 사라진다(3,800밀리초에서 17밀리초)는 것이 저장소의 핵심 서술이다.
`ffmpeg` 설치 없이 mp4가 나온다는 점이 CI와 에이전트 환경에서 간편하다는 장점으로 이어진다.
이는 README의 서술을 이 문서가 정리한 것이다.

### 이 도구는 얇은 래퍼이고 가치는 Chrome 쪽에 있다

README는 직접 npm으로 설치하거나 에이전트에게 `src/index.ts`를 가리켜 구현을 가져가라고 한다. 구현이 작다는 것이다.
성능의 대부분은 Chrome 153의 새 API에서 나오고, 도구는 CLI, Playwright 픽스처, 원시 CDP 사용법, 커서 표시를 얹는다.
따라서 이 도구의 수명은 새 API의 안정화와 Playwright, Puppeteer의 내장 지원에 달려 있다. 이는 이 문서의 해석이다.

## 비평

### 벤치마크가 한 기기, 한 시나리오이다

수치는 M4 Max에서 6.4초 UI 재생 하나의 결과이다.
PSNR 32dB 대 34dB, 파일 크기 480KB 대 330KB는 짧은 영상 하나의 값이어서 일반화하기 어렵다.
또한 25fps라는 기존 방식의 출력은 설정에 따라 달라질 수 있고(최대 60), 비교가 기본값끼리의 것인지 README는 밝히지 않는다.

### 새 API에 기댄 실험적 도구이다

Chrome 153 이상이 필요하고 Puppeteer의 래퍼도 실험적이며 Playwright는 PR 단계라고 README가 적는다.
저장소는 생성한 지 열흘 안팎이고 별 512개의 관심이 있지만 이는 사용 후기가 아니다.

### 플랫폼 범위가 불완전하다

최고 성능은 120Hz ProMotion 맥에서 측정되었고 Windows와 개별 GPU 리눅스는 미확인으로 남아 있다.
맥에서는 특정 플래그가 성능을 크게 해친다는 주의도 있다.
화질 조절 수단이 없다는 한계도 스스로 적었다.

### 외부 반응

Lobste.rs에서는 `chrome-capture`로 검색했을 때 이 도구의 글이 없었다(걸린 두 건은 무관한 글이었다).

## 인사이트

### 가져갈 것은 브라우저 테스트의 영상 첨부를 인코딩 비용 없이 하는 방법이다

테스트 실패 때 영상을 남기는 습관은 있어도 `ffmpeg` 파이프의 비용 때문에 꺼 두는 팀이 있다.
이 도구의 Playwright 픽스처는 모든 테스트를 녹화해 리포트에 붙이는 설정을 몇 줄로 하게 한다.
Chrome 153 이상을 쓰는 환경이라면 시도해 볼 수 있고, 실제 효과는 자기 테스트로 재야 한다. 이는 이 문서의 적용이다.

### 새 브라우저 API는 래퍼보다 원 API의 설명을 읽는다

도구가 작으므로 원 API(`Page.startScreenRecording`)의 변경 이력과 제약이 곧 도구의 제약이다.
도입하기 전에 원 API의 안정성과 지원 계획을 확인하는 것이 래퍼의 옵션을 비교하는 것보다 먼저이다.

### 확인할 관찰

이 도구의 주장을 가를 관찰은 세 가지이다.
다른 기기와 운영체제, 긴 영상에서의 성능과 화질,
Playwright와 Puppeteer가 같은 API를 공식 지원하게 된 뒤 이 도구가 어떤 역할로 남는지,
비트레이트 조절이 추가되는지이다.
