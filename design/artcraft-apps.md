# ArtCraft Crafting Apps: Adobe 제품 일곱 개를 Rust로 다시 만들겠다는 오픈소스 프로젝트

<https://getartcraft.com/apps>

<https://github.com/storytold>

HN 토론: <https://news.ycombinator.com/item?id=49958850> (115점, 173개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49981449> (99점, 62개 댓글)

GN 토론: <https://news.hada.io/topic?id=34809>

## 소개

Crafting Apps는 AI 영상·이미지 도구 ArtCraft를 만드는 팀이 내놓은 오픈소스 창작
앱 모음이다.
페이지는 일곱 개의 앱, 하나의 기술(Seven apps. One craft)이라는 문구로 시작하며,
이미지 편집, 벡터 일러스트레이션, 영상, 사진, PDF, 모션 그래픽,
페이지 레이아웃을 다루는 네이티브 앱을 Rust로 만들어 무료로 제공한다고 소개한다.
웹사이트는 Adobe라는 이름을 직접 쓰지 않지만,
GitHub 저장소의 설명은 각 앱을 Adobe 제품의 클린룸(clean-room) 재구현이라고
밝힌다.

| 앱          | 분야                       | GitHub 설명이 밝힌 대상 | 상태      | 2026년 10월 7일 스타 |
| ----------- | -------------------------- | ----------------------- | --------- | -------------------- |
| PhotoCraft  | 이미지 편집                | Photoshop               | 초기 알파 | 6,644                |
| VectorCraft | 벡터 일러스트레이션        | Illustrator             | 개발 중   | 1,034                |
| FilmCraft   | 영상 편집                  | Premiere Pro            | 개발 중   | 1,617                |
| LightCraft  | 사진 라이브러리와 RAW 현상 | Lightroom               | 개발 중   | 1,238                |
| PrintCraft  | PDF 작업                   | Acrobat                 | 초기 알파 | 1,110                |
| EffectCraft | 모션 그래픽과 VFX          | 설명 없음               | 개발 중   | 824                  |
| DesignCraft | 페이지 레이아웃과 출판     | 설명 없음               | 개발 중   | 533                  |

일곱 저장소는 모두 2026년 9월 30일과 10월 1일 사이에 만들어졌고 라이선스는
Apache-2.0이다.
PhotoCraft 저장소에는 만들어진 지 일주일 만에 270개의 커밋이 쌓였다.
GitHub 조직 이름은 `storytold`이고, 웹사이트 바닥글의 연락처는 `storyteller.ai`
도메인이다.

## 공통 원칙

페이지는 모든 앱이 따르는 여섯 가지 원칙을 내세운다.

- 오픈소스: 모든 코드를 허용적인 라이선스로 GitHub에 공개한다.
- 네이티브: 순수 Rust로 macOS, Windows, Linux 데스크톱 앱을 만들고 Electron이나 웹뷰를 쓰지 않는다.
- 첫날부터 익숙함: 현업 전문가가 이미 아는 레이아웃, 도구, 단축키를 쓴다.
- 내 파일, 내 컴퓨터: 모든 작업을 로컬 파일에서 실행하고 클라우드를 오가지 않는다.
- 에이전트 대응: 모든 앱을 CLI, JSON 제어 채널, MCP 서버로 조작할 수 있다.
- 브라우저에서도: FilmCraft를 뺀 여섯 앱은 WebAssembly로 컴파일되어 브라우저 탭에서 돈다.

## PhotoCraft로 본 구현

가장 앞선 PhotoCraft의 README가 이 프로젝트의 설계를 가장 자세히 보여 준다.
레이어, 마스크, 조정 레이어, 레이어 스타일, 문자, 벡터,
브러시를 갖춘 이미지 편집기이며, 메뉴와 단축키가 Photoshop을 아는 사람의 손이
기대하는 자리에 있다고 소개한다.
도구 34개, 블렌드 모드 27개, 조정 레이어 16개,
미리보기가 되는 필터 70여 개를 갖췄고, RGB, Grayscale, CMYK, Lab 문서를 8, 16,
32비트로 다루며 ICC 색 관리와 소프트 프루핑을 지원한다고 적는다.
캔버스는 wgpu 위의 GPU 합성기로 Metal, Vulkan, DirectX 12, WebGPU에서 그려진다.

구조는 순수 데이터로 된 문서 모델과 명령 엔진 위에 얇은 egui UI를 얹은 형태이고,
24개 크레이트 사이의 계층을 빌드 단계에서 강제한다.
CPU 합성기를 기준(oracle)으로 두고 GPU 합성기를 그것과 비교해 시험하며,
테스트는 1,700개가 넘는다고 한다.
모든 메뉴, 도구, 대화상자는 500개가 넘는 명령이 담긴 하나의 레지스트리를 거치고,
UI, CLI, JSON 제어 채널, MCP 서버가 같은 명령을 부른다.

```bash
# README에 실린 예: 헤드리스로 열고, 고치고, 저장한다
photocraft-cli run wave.psd \
  --cmd filter.sharpen.smartSharpen     --params '{"amount":80}' \
  --cmd layer.newAdjustmentLayer.curves --params '{"points":[[0,0],[64,48],[192,212],[255,255]]}' \
  --out wave-final.png

# 에이전트가 MCP로 조작하게 한다
photocraft-cli mcp
```

PSD 지원은 Adobe의 공개 명세로 작성한 독립 크레이트다.
README는 psd-tools 테스트 세트 309개 중 307개가 다시 저장해도 같은 화면으로
그려지고, 다만 다시 저장한 파일은 원본과 바이트 단위로 같지 않으며 독립
크레이트로 파싱하고 쓸 때만 바이트 단위로 같다고 설명한다.
클린룸이란 공개 명세와 관찰한 동작만으로 구현했고 독점 코드, 셰이더,
자산을 쓰지 않았다는 뜻이라고 밝힌다.
버전은 0.2.0이고 macOS, Windows, Linux용 설치 파일과 웹 빌드가 함께 배포된다.

## 분석

### AI로 일주일 만에 만든 제품군이라는 점이 핵심이다

일곱 저장소가 이틀 사이에 생겼고, 가장 큰 저장소에 일주일 동안 270개의 커밋이
쌓였다는 사실은 이 프로젝트가 사람 손만으로 만든 것이 아님을 보여 준다.
HN 첫 스레드에서 자신이 만든 사람이라고 밝힌 echelon은 아직 전혀 준비되지 않았고 HN에 올릴 생각이 없었다며, 베타를 넘기면 다시 올리겠다고 적었다[^echelon].
그는 모두 MIT나 Apache 라이선스이고 원격 수집이 없으며,
완전한 동등성을 목표로 하되 시간이 걸릴 것이라고 했다.
또 Microsoft Office, AutoCAD, Solidworks도 만들 것이며,
이제 모든 것이 오픈소스 멀티플랫폼 Rust가 될 수 있다고 덧붙였다.
두 번째 스레드에서 slopinthebag은 만든 사람이 사흘 전 Photoshop 전체를 한 번에
만들어 냈다고 썼다고 인용했다[^slopinthebag].

이 프로젝트가 흥미로운 이유는 결과물의 품질보다,
거대한 상용 제품군을 복제하는 시도의 비용이 얼마나 낮아졌는지를 보여 준다는 데
있다.
slopinthebag은 이 정도 범위면 바이브 코딩에 관한 주장 대부분을 시험할 수 있다고
평가했다[^slopinthebag-scope].

### 에이전트 인터페이스가 처음부터 설계에 들어 있다

모든 기능을 하나의 명령 레지스트리로 묶고 UI, CLI,
MCP가 같은 명령을 부르게 한 구조는 이 프로젝트에서 가장 설계다운 부분이다.
Photoshop 같은 기존 제품은 GUI를 먼저 만들고 스크립팅을 나중에 붙였지만,
여기서는 명령이 먼저이고 GUI는 그 위의 얇은 층이다.
README의 스크린숏까지 제어 채널로 오프스크린 렌더링해서 찍었다는 설명은,
이 앱을 만든 에이전트가 같은 인터페이스로 앱을 시험했다는 뜻으로 읽힌다.
에이전트가 만든 소프트웨어가 에이전트가 다루기 쉬운 형태를 띠는 것은 자연스러운
결과다.

### 사용자 쪽 수요는 실재한다

HN 반응은 냉소와 기대가 섞여 있다.
queenkjuul은 평생 오픈소스 InDesign 경쟁자를 기다렸고 Scribus는 경쟁 상대가
아니라며 희망을 걸었다[^queenkjuul].
hypfer는 Linux에서 늘 아쉬웠던 PDF 도구를 가장 흥미로운 부분으로 꼽고,
예술가가 아닌 거대한 사용자층이 혜택을 볼 수 있다고 봤다[^hypfer].
dinkleberg는 GIMP와 Inkscape의 불편함을 견디며 살던 Linux 사용자에게 유망한
대안이라고 했다[^dinkleberg].
Adobe 구독 모델에 대한 피로가 이런 시도를 기다리는 수요를 만든다.

## 비평

### 웹사이트의 약속과 실제 상태가 크게 다르다

첫 스레드에서 직접 써 본 사람들의 평가는 혹독했다.
rf15는 AI가 만든 매우 망가진 소프트웨어이며 제목과 설명이 실제와 너무 달라
기만적이라고 해도 될 정도라고 적었다[^rf15].
luckydata는 Photoshop에 해당하는 앱을 써 봤지만 거의 아무것도 작동하지 않는다고
했다[^luckydata].
tiborsaas는 PhotoCraft에서 클립보드 이미지를 붙여 넣지 못했고 복제 도장 도구는
실시간으로 갱신되지 않는다고 구체적인 문제를 들었다[^tiborsaas].
Wheen은 README의 Flatpak 설치 안내를 따랐지만 안내에 나온 Flatpak 파일이
배포되지 않았다고 지적했다[^Wheen].

웹사이트는 첫날부터 익숙하다, 전문가가 아는 도구를 쓴다고 말하지만,
상태 표시는 초기 알파와 개발 중이다.
만든 사람 스스로도 아직 준비되지 않았다고 말하는 제품을,
페이지는 완성된 대안처럼 소개한다.
이 간극이 반응의 상당 부분을 냉소로 만들었다.

### 수치가 문서마다 다르다

PhotoCraft 소개 페이지는 실제 테스트 파일 135개 중 134개가 바이트 단위로
왕복(round-trip)한다고 적는다.
그런데 README는 다시 저장한 파일이 원본과 바이트 단위로 같지 않다고 분명히
밝히고, 바이트 단위 재현은 독립 PSD 크레이트에서만 성립한다고 설명한다.
같은 제품의 두 문서가 핵심 품질 지표를 다르게 말하는 것은,
문서도 코드처럼 빠르게 생성되었고 서로 맞춰 보지 않았다는 신호로 읽힌다.
freeone3000은 두 테스트 사례에서 저장 후 내보낸 렌더가 달라질 만큼 PSD가
바뀐다며, 만든 사람이 결과물을 실제로 써 보지 않은 것 같다고
비판했다[^freeone3000].

### 클린룸이라는 말이 무엇을 뜻하는지 흐리다

클린룸 재구현은 원래 한 팀이 기존 제품을 분석해 명세를 쓰고,
그 명세만 본 다른 팀이 구현하는 절차를 가리킨다.
forgotpwd16은 역공학이 없으니 클린룸이라는 말은 맞지 않고,
Adobe 제품군 복제(clone)라고 부르는 편이 정확하다고 지적했다[^forgotpwd16].
README는 공개 명세와 관찰한 동작만으로 구현했다고 말하지만,
그 구현을 쓴 모델이 무엇을 학습했는지는 아무도 확인할 수 없다.
같은 시기 GeekNews에는 Photopea 개발자가 Photosuite라는 다른 데스크톱 편집기를
두고 자신의 코드를 가져와 AI로 변수명만 바꿨다고 문제를 제기한 소식이 올라왔다.
그 사건은 이 프로젝트와 무관하지만, AI로 만든 복제품의 출처를 둘러싼 의심이
어떻게 생기는지 보여 준다.

라이선스도 단순하지 않다.
일곱 앱은 Apache-2.0이지만, kmeisthax는 본체인 ArtCraft 저장소가 스스로를 일종의
페어 소스(fair source)라고 소개하며 몇 가지 사용 제한을 둔다고
지적했다[^kmeisthax].
같은 회사의 제품이 서로 다른 라이선스 철학을 따르는 셈이다.

### 소프트웨어의 가치는 기능 목록에 있지 않다

dofm은 Excel 같은 프로그램은 철저한 테스트로 동작을 증명할 수 있지만,
Photoshop은 그런 방식으로 정의되는 앱이 아니라며 이 시도가 Photoshop의 본질을
오해하고 있다고 봤다[^dofm].
bergen은 Adobe의 해자는 업계 표준이라는 지위와 수많은 문서, 튜토리얼,
프린터와 카메라 같은 산업 표준과의 통합이라며,
회사가 사람을 뽑을 때마다 n번째 Adobe 대체품을 다시 가르치려 하지 않을 것이라고
했다[^bergen].
Youden은 사진 작업에서는 RAW 지원이 거대한 구멍이라며,
같은 RAW 파일을 Lightroom과 LightCraft에 나란히 열면 결과가 완전히 다르다고
지적했다[^Youden].
fschuett는 자신이 관리하는 `printpdf` 크레이트 경험을 들어,
PDF 내보내기에서 텍스트를 경로로 내보내는 문제를 지적하고 올바른 PDF 인코딩과
글꼴 서브셋팅에 몇 달의 시행착오가 들었다며 QA에 드는 노력을 과소평가하지 말라고
했다[^fschuett].

일곱 앱의 기능 목록은 길지만, 그 목록 하나하나가 전문가가 기대하는 수준으로
동작하게 만드는 일은 코드 생성과 다른 종류의 작업이다.

## 인사이트

### 복제의 비용이 무너지면 상용 소프트웨어의 방어선이 옮겨 간다

petterroea는 회사가 소송으로 지킬 만한 소프트웨어의 클린룸 포트가 나오기
시작했고, 아무도 다시 만들지 않을 것이라는 오래된 방어가 더는 통하지 않는다고
봤다[^petterroea].
기능을 복제하는 비용이 일주일과 토큰 값으로 떨어지면,
상용 제품의 방어선은 기능에서 다른 곳으로 옮겨 간다.
bergen이 말한 표준 지위와 교육 자료, Youden이 말한 RAW 처리 같은 깊은 품질,
fschuett이 말한 긴 QA처럼 시간이 쌓여야 만들어지는 것들이다.
tonyedgecombe은 Adobe의 진짜 문제는 사람들이 AI로 만든 도구로 Adobe 도구를
대체하는 것이 아니라, Adobe 도구를 쓰는 일 자체를 AI로 대체하는 것이라고
짚었다[^tonyedgecombe].
이 관점에서 Crafting Apps는 Adobe를 위협하는 경쟁자라기보다,
소프트웨어 기능이 더 이상 희소하지 않다는 것을 보여 주는 증상에 가깝다.

### 대량 복제의 시대에는 유지보수가 진짜 비용이 된다

VortexLain은 이 제품군이 한 달 만에 버려지지 않고 언젠가 실제로 쓸 수 있는
수준이 되기를 바란다고 적었다[^VortexLain].
여러 댓글이 같은 걱정을 했다.
일곱 개의 거대한 앱을 만드는 데 일주일이 걸렸다면,
그 앱들에 쌓일 이슈와 회귀를 처리하는 일은 훨씬 오래 걸린다.
4b11b4는 그 많은 토큰과 비용, 그리고 그 뒤의 유지보수가 동기와 추진력이 유지될
때만 가능할 것이라고 물었다[^4b11b4].
AI가 소프트웨어를 만드는 비용을 낮춘 만큼,
그 소프트웨어를 쓸 만한 상태로 유지하는 비용이 오히려 차별점이 된다.

### 이 프로젝트의 진짜 고객은 AI 서비스일 수 있다

Crafting Apps 페이지 바닥글은 ArtCraft를 제어할 수 있는 AI 이미지·영상을 위한
오픈소스 스튜디오라고 소개하고, 본체 ArtCraft는 Seedance나 Nano Banana 같은 생성
모델을 한 화면에서 쓰는 도구다.
CreepGin은 구독이 이미지 생성만을 위한 것인지,
앱에 내장된 것인지 물었다[^CreepGin].
무료 오픈소스 Adobe 대체품은 사람들을 ArtCraft 생태계로 끌어들이는 입구 역할을
할 수 있다.
이는 내 해석이지만, 무료 편집 도구와 유료 생성 서비스의 조합은 Adobe가 Creative
Cloud와 Firefly로 하고 있는 구조를 오픈소스로 뒤집어 놓은 모양이다.

---

[^echelon]: <https://news.ycombinator.com/item?id=49959605>

[^slopinthebag]: <https://news.ycombinator.com/item?id=49961583>

[^slopinthebag-scope]: <https://news.ycombinator.com/item?id=49959755>

[^queenkjuul]: <https://news.ycombinator.com/item?id=49965043>

[^hypfer]: <https://news.ycombinator.com/item?id=49961177>

[^dinkleberg]: <https://news.ycombinator.com/item?id=49982700>

[^rf15]: <https://news.ycombinator.com/item?id=49961301>

[^luckydata]: <https://news.ycombinator.com/item?id=49961271>

[^tiborsaas]: <https://news.ycombinator.com/item?id=49982228>

[^Wheen]: <https://news.ycombinator.com/item?id=49982126>

[^freeone3000]: <https://news.ycombinator.com/item?id=49982008>

[^forgotpwd16]: <https://news.ycombinator.com/item?id=49981947>

[^kmeisthax]: <https://news.ycombinator.com/item?id=49960110>

[^dofm]: <https://news.ycombinator.com/item?id=49966551>

[^bergen]: <https://news.ycombinator.com/item?id=49961389>

[^Youden]: <https://news.ycombinator.com/item?id=49981942>

[^fschuett]: <https://news.ycombinator.com/item?id=49959707>

[^petterroea]: <https://news.ycombinator.com/item?id=49982167>

[^tonyedgecombe]: <https://news.ycombinator.com/item?id=49961111>

[^VortexLain]: <https://news.ycombinator.com/item?id=49978319>

[^4b11b4]: <https://news.ycombinator.com/item?id=49959653>

[^CreepGin]: <https://news.ycombinator.com/item?id=49959701>
