# Command & Conquer Generals: Zero Hour — Apple 플랫폼 포트

<https://github.com/ammaarreshi/Generals-Mac-iOS-iPad>

HN 토론: <https://news.ycombinator.com/item?id=48788283> (417점, 159개 댓글)

## 소개

Ammaar Reshi가 Claude Code(Anthropic Fable 모델)와 협업해 2003년 Windows
RTS 게임 Command & Conquer Generals: Zero Hour를 macOS, iPhone, iPad에서
네이티브로 실행되도록 이식한 프로젝트다.
GitHub 저장소 설명에 “built as a human+AI collaboration: engineering by
Claude Code, directed and playtested on real devices by Ammaar Reshi”라고
명시되어 있다.
이식 작업은 “one long working session” — 하루 안에 완료됐다.

게임 코드는 EA가 GPL v3로 공개한 1.6M LOC C++ 원본에 기반하며,
macOS/Linux 포트를 이미 완성한 fbraz3/GeneralsX 포크 위에서 진행되었다.
이 저장소는 iOS/iPadOS 이식과 엔진 수정을 추가하는 데 집중했다.
게임 에셋은 포함되지 않으며 Steam에서 자신의 사본이 필요하다(~$5).

주요 기능은 iPhone 17 Pro Max, iPad mini에서 캠페인·스커미시·Generals
Challenge를 실행하는 것이다.
터치 컨트롤은 RTS를 위해 설계됐다: tap-select, drag-box, long-press deselect,
two-finger scroll, pinch zoom.
에뮬레이션 없이 진짜 ARM64 컴파일 바이너리다.
단, 크로스 플랫폼 float 결정론 문제로 멀티플레이어는 모든 네이티브 포트에서
작동하지 않는다.

## 기술 구조

렌더링 파이프라인은 번역 체인 구조다:

```text
게임 코드 (DirectX 8 호출)
  → DXVK 2.6 (d3d8/d3d9 dylib)
  → Vulkan
  → MoltenVK 1.4.1 (dynamic framework)
  → Metal → Apple GPU
```

주요 의존성:

| 구성 요소   | 선택                                  | 원본 대체         |
| ----------- | ------------------------------------- | ----------------- |
| 윈도우/입력 | SDL3 3.4.2                            | Win32             |
| 렌더링      | DXVK 2.6 + MoltenVK 1.4.1            | DirectX 8         |
| 오디오      | openal-soft 1.24.2                    | Miles Sound       |
| 비디오      | FFmpeg 8.1                            | Bink              |
| 텍스트      | FreeType + Liberation 폰트(번들)      | GDI               |
| 앱 셸       | XcodeGen 생성 서명 번들               | Win32 exe         |

iOS 이식에서 핵심 난관은 세 가지였다.
첫째, `dlopen`은 앱 번들 내 경로만 허용한다.
DXVK가 `@executable_path/Frameworks/libdxvk_d3d8.0.dylib`로 로드하고,
MoltenVK도 같은 방식으로 처리해야 했다.
둘째, `pkg_check_modules`의 `-framework X` 플래그가 CMake 중복 제거 로직과
충돌해 링커가 bare name을 파일명으로 읽는 버그가 있었다.
셋째, fontconfig가 iOS 크로스 컴파일에서 실패해 번들 폰트 폴백으로
대체해야 했다.

RTS 터치 컨트롤 구현의 핵심은 “지연 탭 상태 기계(deferred-tap state machine)”다.
`IDLE → PENDING → {tap | DRAGGING | LONGPRESSED | PAN}` 흐름으로,
손가락을 올렸을 때 즉시 LMB-down을 보내지 않는다.
제스처가 확인된 후에야 이벤트를 주입하는 방식이다.
이를 통해 “two-finger pan의 첫 번째 손가락이 집결 명령을 발행하는” 버그를
방지했다.

## 분석

### 포크 고고학이 작업 기간을 수개월에서 하루로 줄였다

이 프로젝트의 가장 중요한 기술적 결정은 코드를 한 줄도 작성하기 전에
이루어졌다. 원본 EA 소스 코드를 직접 포팅하면 수개월이 걸리는 작업이다.
그러나 fbraz3/GeneralsX가 이미 macOS ARM64에서 SDL3+DXVK+MoltenVK 스택을
완성했다는 사실을 발견함으로써, 작업 범위가 “게임을 이식”에서
“iOS 샌드박스 + 라이프사이클 + 서명 + 터치”로 축소됐다.

포팅 플레이북(§0)이 제시하는 기준은 명확하다.
“macOS Apple Silicon에서 이미 실행된다면, iOS 포트는
cross-compile + sandbox + lifecycle + touch”라는 것이다.
이 판단을 위해 수행한 작업은 fork ecosystem 매핑이었다.
`gh api repos/<owner>/<repo>/forks?sort=stargazers`로 포크를 정렬하고,
각 포크가 실제로 무엇을 달성했는지 README 주장이 아닌 릴리스와 CI
설정으로 검증했다.

### 번역 체인 패턴은 레거시 소프트웨어 이식의 구조적 해법이다

DX8 → DXVK → Vulkan → MoltenVK → Metal의 체인은 특이하게 보이지만,
각 레이어는 독립적인 오픈소스 프로젝트다.
이 체인이 가능한 이유는 DXVK가 Direct3D를 Vulkan으로 변환하는 이미
성숙한 레이어이기 때문이다. Wine 생태계에서 발전한 DXVK는 수천 개의
Windows 게임에서 검증됐다.
MoltenVK는 Vulkan을 Metal로 변환하는 Khronos 공식 레이어다.

게임 코드는 단 한 줄도 수정하지 않고 렌더링 API를 교체한 셈이다.
이 패턴의 장점은 게임 로직과 렌더링 구현의 완전한 분리다.
단점은 번역 레이어가 추가될수록 디버깅이 어려워진다는 것이다.
DXVK의 SDL2/SDL3 fallback 버그처럼, 각 레이어는 자신만의 “silent failure”
패턴을 갖는다.

Reubend는 이 체인을 보고 “5개 레이어를 통과한 뒤 렌더링하는 건가?
미친 것 같다”고 반응했다.[^Reubend]
하지만 그 자신도 인정했듯 각 레이어가 충분히 성숙한 라이브러리이기
때문에 이것이 작동하는 것이 의외가 아니다.
이 반응은 렌더링 체인의 구조가 직관에 반한다는 것을 보여주는 동시에,
충분한 추상화 레이어가 있으면 복잡한 체인도 운용 가능하다는 점을 확인한다.

### AI 에이전트의 “user must do” vs “agent can do” 분리는 협업 설계의 새 원칙이다

플레이북 §8.8은 “Distinguish 'user must do' from 'agent can do' early:
Steam login, device unlock/pair/trust, Developer Mode — front-load the ask
so it overlaps with agent work”라고 명시한다.
이는 단순한 팁이 아니라 AI 에이전트와의 협업 구조 설계 원칙이다.

에이전트가 처리할 수 있는 작업(빌드 스크립트 작성, 의존성 해결, 패키징)과
인간이 반드시 개입해야 하는 작업(Steam Guard 인증, 기기 페어링, Developer
Mode 활성화)의 경계를 앞단에 명확히 하면, 에이전트가 블로킹 없이 작업을
진행하는 동안 인간이 병렬로 준비 작업을 완료할 수 있다.
이 분리가 “하루 세션” 완료를 가능하게 한 구조적 요인이다.

## 비평

### “하루 세션” 주장은 선행 작업을 숨긴다

이 프로젝트의 성공 조건에서 가장 중요한 것은 fbraz3/GeneralsX의 존재다.
GeneralsX는 macOS ARM64 네이티브 실행, SDL3, DXVK, MoltenVK, OpenAL,
FFmpeg를 이미 통합한 상태였다.
그 프로젝트 자체가 상당한 선행 작업의 산물이다.

“하루 작업”이라는 인상은 이 누적 투자를 시야에서 지운다.
플레이북도 이를 인정하며 “fbraz3/GeneralsX did the heavy lifting of
the macOS/Linux port”라고 명시한다.
AI 협업으로 하루에 이식이 가능하다는 명제가 성립하려면,
이미 동일 플랫폼 계열에서 실행되는 커뮤니티 포크가 존재해야 한다는
전제가 함께 명시되어야 한다.
이 전제가 충족되지 않는 게임이라면 “하루 작업”은 성립하지 않는다.

HN에서 dools는 “Fable로 만들었다는데 첫 커밋이 작년 2월이다”라고
의문을 제기했고,[^dools] debugnik은 “GeneralsX를 포크해서 마지막 몇 커밋만
추가한 것”이라고 설명했다.[^debugnik]
HN 제목이 “using Fable”을 강조한 탓에, 이 저장소가 실질적으로
커뮤니티 포트 위에 iOS 레이어를 얹은 것임이 희석됐다.
이 크레딧 문제는 단순한 의전이 아니다.
“AI가 레거시 게임을 하루에 이식했다”는 내러티브의 조건을 정확히 이해하려면
GeneralsX 기여자들의 작업이 명시적으로 보여야 한다.

### 실제 사용 장벽은 문서가 제시하는 것보다 훨씬 높다

macOS 빌드 요구사항 목록을 보면: Xcode command line tools, Homebrew,
cmake/ninja/meson/pkgconf, steamcmd, vcpkg 풀 클론, LunarG Vulkan SDK,
환경 변수 설정. iOS 추가 요구사항: 전체 Xcode(Apple ID 로그인),
xcodegen, Apple Developer 계정(유료 또는 무료).

여기에 Steam 계정, 실제 게임 구매, Steam Guard 인증, 기기 케이블 페어링,
Developer Mode 활성화가 추가된다.
이 과정은 일반 사용자가 아닌 iOS 앱 개발 경험이 있는 개발자를 위한 것이다.
저장소 설명이 “web developer”나 “game player”가 아닌 “engineer or agent”를
반복 대상으로 명시하는 것은 이 현실을 반영한다.
그러나 GitHub 스타와 소셜 미디어 반응에서 이 프로젝트는 “iPhone에서
C&C 실행하기”로 소비되는데, 이 이미지와 실제 사용 요구사항 사이에는
상당한 간극이 있다.

### AI 생성 문서의 문체는 인간 독자에게 인지 부하를 만든다

xg15는 README의 “tap-select, drag-box, long-press deselect, two-finger scroll,
pinch zoom” 같은 표현을 “AI-ism”으로 지적한다.[^xg15]
AI 코딩 에이전트가 복잡한 개념을 복합 명사 구절로 압축하는 경향이 있는데,
이것이 토큰 절약 때문인지 개념의 내부 식별자 역할을 하는 것인지 모르겠다고
한다. 결과 문장이 읽기 어렵다는 지적이다.

Eufrat도 유사한 관찰을 했다.[^Eufrat]
포팅 문서가 “AI가 생성한 텍스트 스타일”이라 불쾌하다고 하면서도,
이것이 블로그 포스트나 에세이가 아닌 코딩 에이전트의 중간 산출물에
가깝기 때문에 괜찮다고 판단했다.
이 관용적 태도는 AI 생성 기술 문서에 대한 커뮤니티 기준이 아직
정착하지 않았음을 보여준다.

### 멀티플레이어 불가 문제는 “알려진 이슈”가 아니라 게임의 핵심 기능 결여다

플레이북은 멀티플레이어가 “broken in ALL native ports of this engine”이라고
설명하며, 원인은 크로스 플랫폼 float 결정론 문제라고 밝힌다.
이는 이 프로젝트만의 한계가 아니라 모든 커뮤니티 포트의 공통 미해결 과제다.

그러나 C&C Generals는 2003년에 멀티플레이어가 핵심 기능인 게임이다.
캠페인과 AI 스커미시만 가능한 포트는 게임의 상당 부분을 복원하지 못한다.
이것이 기술적으로 어려운 문제임은 사실이지만,
“fully playable = campaigns + skirmish vs AI”라는 정의를 요약본에서 명확히
하지 않고 “fully playable”만 제목 설명에 사용하는 것은
독자에게 과장된 기대를 줄 수 있다.

## 인사이트

### 포크 고고학은 AI 에이전트 시대의 소프트웨어 이식 핵심 역량이 된다

이 프로젝트의 진짜 레버리지 포인트는 코딩 능력이 아니라 정보 수집 능력이었다.
어느 포크가 어느 플랫폼 요건을 이미 만족했는지 체계적으로 파악하는 것이
수개월 작업을 하루로 줄였다.
AI 에이전트는 API 호출로 대규모 포크 생태계를 순회하고, 각 포크의
실제 CI 상태와 릴리스를 검증하는 작업에 인간보다 훨씬 빠르다.

이 패턴은 레거시 소프트웨어 이식에 일반화된다.
어떤 목표 플랫폼에 가장 가깝게 도달한 커뮤니티 포크를 찾는 것이 항상
첫 번째 단계가 되어야 한다.
AI 에이전트가 이 “포크 고고학”을 자동화하면 레거시 이식 비용이
구조적으로 낮아진다. 단, 대상이 오픈소스 게임이거나 GPL 소스가 공개된
경우에 한정된다. 상용 소프트웨어 이식은 이 접근이 성립하지 않는다.

OsrsNeedsf2P는 같은 SAGE 엔진 기반의 Battle for Middle Earth(반지의 제왕
RTS)를 AI로 “오픈소스화”하는 작업을 진행 중이라고 밝혔다.[^OsrsNeedsf2P]
동일 엔진 계열에서 이 패턴이 즉시 반복 적용된다는 것은,
포크 고고학 + AI 이식 접근이 특수한 사례가 아니라 일반화 가능한
방법론임을 실증한다.

tangenter는 이 추세가 역공학(reverse engineering) 영역으로도 확장될
것임을 전망한다.[^tangenter]
Ghidra + LLM 워크플로우를 사용해 소스 없는 게임도 C/C++ 코드로 복원하는
작업이 이미 진행 중이며, “LLM 없이도 유능한 팀은 LLM과 함께 무적”이
된다는 관찰이다.
소스가 공개되지 않은 게임에도 AI 지원 이식이 가능해진다면,
레거시 게임 보존의 범위가 GPL 공개 소스에서 훨씬 넓어진다.

### 1.6M LOC 레거시 코드 이식은 LLM의 이상적 작업 유형임이 증명됐다

새로운 기능을 설계하는 것과 기존 코드를 다른 환경에서 동작하게 만드는 것은
근본적으로 다른 작업이다.
이식 작업의 특성은 다음과 같다: 정답이 명확하다(게임이 실행되면 성공),
오류 메시지가 구체적이다(링커 에러, 런타임 크래시), 검증이 즉각적이다
(빌드하면 알 수 있다), 창의적 판단보다 체계적 문제 해결이 더 중요하다.

이 특성들은 LLM이 강점을 발휘하는 영역과 정확히 일치한다.
특히 플레이북에서 상세히 기록된 “silent failure” 패턴들 — DXVK가 SDL3
대신 SDL2를 조용히 사용하는 것, 빌드 스크립트가 실패를 숨기는 것 —
은 `strings`와 `otool` 출력으로 검증하는 체계적 접근으로 해결됐다.
LLM은 이런 검증 루프를 인간보다 빠르고 일관되게 수행할 수 있다.

### 렌더링 번역 체인 접근법은 오픈소스 생태계의 누적 투자를 재조합한다

DX8 → DXVK → Vulkan → MoltenVK → Metal 체인의 의미는 단순히
“오래된 게임을 새 플랫폼에서 실행한다”는 것이 아니다.
이 체인은 서로 다른 시기와 목적으로 만들어진 오픈소스 프로젝트들의
재조합이다. DXVK는 Wine/Proton 생태계에서 Linux 게이밍을 위해 만들어졌고,
MoltenVK는 Apple 플랫폼의 Vulkan 지원을 위해 Khronos가 공식 관리한다.

이 재조합이 가능한 이유는 각 레이어가 표준 인터페이스를 준수하기 때문이다.
Vulkan이 그 중간 공통 언어 역할을 한다.
이 패턴이 보여주는 것은 충분히 성숙한 오픈소스 번역 레이어들이 존재하면,
30년 된 레거시 코드도 최신 플랫폼에서 실행할 수 있다는 것이다.
이 패턴은 다른 고전 게임 이식에도 즉시 적용 가능하다.
EA가 GPL로 공개한 유사한 코드베이스나 다른 DirectX 기반 고전 게임들이
다음 대상이 될 수 있다.

### AI 협업 기록으로서의 포팅 플레이북은 새로운 소프트웨어 문서 형식이다

`docs/port/PORTING_PLAYBOOK.md`는 단순한 기술 문서가 아니다.
저자가 “the unedited record of how that worked”라고 설명하듯,
AI 에이전트가 수행한 작업의 완전한 감사 로그다.
모든 빌드 실패, 근본 원인, 수정 과정이 기록되어 있으며,
마지막 섹션(§8)은 “Process & agent-workflow lessons”로 이 협업 방식을
다른 프로젝트에 적용하는 방법론을 일반화한다.

이 형식은 AI 협업이 일상화될수록 중요해질 것이다.
“에이전트가 한 일”의 추적 가능성은 코드 품질 보증과 신뢰 구축의 핵심이다.
§8.9의 “write destructive-tool warnings into memory immediately”는
에이전트의 오작동 기록을 영구 저장해 반복을 방지하는 원칙인데,
이것은 인간 개발자의 포스트모템 문화를 AI 에이전트 협업에 이식한 것이다.
소프트웨어 이식 방법론 문서가 동시에 AI 협업 감사 로그가 되는 이 형식은,
앞으로의 AI 보조 개발이 어떤 문서를 남겨야 하는지에 대한 구체적 선례다.

---

[^Reubend]: <https://news.ycombinator.com/item?id=48789603>
[^dools]: <https://news.ycombinator.com/item?id=48789046>
[^debugnik]: <https://news.ycombinator.com/item?id=48789500>
[^xg15]: <https://news.ycombinator.com/item?id=48788648>
[^Eufrat]: <https://news.ycombinator.com/item?id=48788939>
[^OsrsNeedsf2P]: <https://news.ycombinator.com/item?id=48788503>
[^tangenter]: <https://news.ycombinator.com/item?id=48791171>
