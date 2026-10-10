# vgpu: 브라우저와 Node에서 같은 셰이더를 돌리는 에이전트용 WebGPU 라이브러리

<https://vgpu.sh/>

<https://github.com/vercel-labs/vgpu>

HN 토론: <https://news.ycombinator.com/item?id=49470841> (2점, 0개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49475848> (1점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35088>

## 소개

vgpu는 Vercel Labs가 만든 TypeScript용 WebGPU 라이브러리다.
README는 스스로를 타입이 붙는 셰이더 import, 작은 GPU 우선 API,
그리고 브라우저와 헤드리스 Node, 테스트에서 똑같이 도는 코드로 소개한다.
홈페이지 vgpu.sh의 첫 문구는 에이전트를 위해 설계한 WebGPU 라이브러리이고,
그 아래에 프롬프트, CLI, 스킬, MCP 네 가지 설치 경로를 나란히 놓는다.
사람보다 코딩 에이전트를 먼저 독자로 상정한 라이브러리라는 점이
다른 WebGPU 래퍼와 가장 크게 다른 부분이다.

GitHub 저장소는 2026년 5월 5일에 만들어졌고,
10월 10일 기준으로 별 2,472개, 포크 122개, 열린 이슈 44개다.
기본 브랜치는 `canary`이며 라이선스는 MIT(저작권 2025 Vercel, Inc.)다.
기여자 목록에서는 matiasngf 계정이 1,750개 커밋으로 거의 전부를 차지하고,
`claude` 계정이 63개로 뒤를 잇는다.

저장소 설명은 셰이더, 3D 장면, GPU 텐서, 신경망, 수학 시각화를 위한
모듈식 교차 런타임 WebGPU 라이브러리라고 적는다.
그러나 README와 문서를 읽어 보면 텐서와 신경망은 vgpu가 직접 구현한 기능이
아니라 다른 ML 런타임과 GPU 기기를 나눠 쓰는 연결 기능이다.
이 차이는 아래 ML 런타임 절에서 다룬다.

### 릴리스와 다운로드

CHANGELOG의 첫 항목은 2026년 5월 7일의 0.0.1 공개 프리뷰이고,
npm 레지스트리에는 5월 26일 0.0.5부터 올라와 있다.
7월 21일 하루에 0.1.0부터 0.1.3까지 나왔고,
이후 0.2.0(7월 31일), 0.3.0(8월 5일), 0.4.0(9월 3일),
0.5.0(9월 14일)으로 이어졌다.
현재 npm `latest` 태그는 0.5.0이고 `next` 태그는 10월 7일의 0.6.0-rc.2다.
npm 다운로드는 10월 2일부터 8일까지 한 주에 168,823회,
9월 9일부터 10월 8일까지 한 달에 680,740회였다.
다섯 달 된 그래픽스 라이브러리로는 큰 수치인데,
CI와 의존성 설치가 반복 집계된 몫이 클 것으로 보인다(해석).

0.x 동안에는 호환성을 깨는 변경이 잦았다.
0.2.0은 `Gpu` 파사드를 없애고 모든 팩토리를 첫 인자로 `gpu`를 받는 자유 함수로
바꿨고, 0.5.0은 텍스처 생성을 명시적인 `kind`, `size`, `usage`로 통일하며
`Texture.resize()`를 없앴다.
0.6.0-rc.1부터는 셰이더를 미리 준비한 `ShaderSource`만 받는다.
릴리스마다 마이그레이션 가이드를 패키지 안 문서에 넣어 두고
`vgpu docs cat /migrations/0.5.0.docs.md`처럼 읽게 한다.

## 패키지 구성

저장소는 pnpm 모노레포다.
공개 진입점은 `vgpu` 하나이고 나머지는 그 뒤를 받치거나 따로 배포된다.

| 패키지               | 역할                                                                |
| -------------------- | ------------------------------------------------------------------- |
| `vgpu`               | 공개 API: `init`, `draw`, `compute`, `effect`, `frame`, `bundle` 등 |
| `@vgpu/cli`          | `vgpu` 실행 파일: 문서, 셰이더 `check`, `doctor`, Dawn 설치(비공개) |
| `@vgpu/core`         | `Device`, `Buffer`, `Texture`, 바인드 그룹 같은 저수준 WebGPU 래퍼  |
| `@vgpu/wgsl`         | `.wgsl` 파일을 JS 모듈로 바꾸고 WGSL 사이 import를 해석하는 로더    |
| `@vgpu/wgsl-std`     | 해시, 노이즈, 색, 샘플링, 수학, 조명 등 WGSL 표준 모듈              |
| `@vgpu/adapter-node` | `vgpu/node`가 쓰는 Dawn 기반 어댑터                                 |
| `@vgpu/adapter-mock` | `vgpu/mock`이 쓰는 결정론적 가짜 어댑터                             |
| `@vgpu/render`       | 편집, 검사, 성능 측정 보조 도구                                     |
| `@vgpu/native`       | WGSL을 Metal로 컴파일해 Swift 패키지를 만드는 베타 빌드 도구        |

`vgpu` 패키지의 하위 경로는 `.`, `./node`, `./mock`, `./scene`, `./scene/gpu`,
`./client`, `./core`, `./three`다.
`src` 아래 TypeScript 줄 수를 세어 보면 `vgpu` 공개 API가 약 16,600줄,
`@vgpu/wgsl`이 약 7,000줄, `@vgpu/native`가 약 7,300줄이고,
`@vgpu/core`는 약 1,900줄로 작다.
라이브러리의 무게가 저수준 래퍼보다 셰이더 해석과 공개 API의 검증 쪽에
실려 있다는 뜻이다.
각 API 파일 옆에는 `draw.docs.md`, `effect.docs.md` 같은 문서가 함께 있고,
이 문서가 패키지에 들어가 CLI와 MCP로 제공된다.

## 동작 방식

### 하나의 `Gpu` 컨텍스트와 명시적 프레임

`init()`은 어댑터와 기기를 얻어 `Gpu` 컨텍스트 하나를 돌려준다.
`draw`, `effect`, `compute`, `frame`, `surface`, `target` 같은 모든 진입점은
이 컨텍스트를 첫 인자로 받으며, 숨은 전역 상태가 없다.
시간은 `clock(gpu)`에서, 해상도는 타깃의 `size`와 `texelSize`에서 얻는다.
패스, 지우기, 그리기는 `frame(gpu, (f) => f.pass(target, effect))`처럼
명시적으로 호출하고, 장면 그래프가 암묵적으로 그리는 일은 없다.
유니폼은 WGSL 이름으로 `set()`에 넘기며, 값은 호출 즉시 기록된다.

### WGSL 모듈

셰이더 언어는 WGSL이다.
vgpu는 WGSL에 `import`와 `export`를 더해 `.wgsl` 파일을 TypeScript 모듈처럼
다루게 한다.

```wgsl
// grain.wgsl
import { hash2 } from "@vgpu/wgsl-std/hash";

export fn grain(uv: vec2f, time: f32) -> f32 {
  return hash2(uv * time).x;
}
```

빌드 시점에 `@vgpu/wgsl` 로더(Vite, webpack, Turbopack)가 모듈 그래프를
해석하고, 바인딩을 반영(reflection)해 이름과 타입, 메모리 배치를 뽑아내고,
쓰지 않는 선언을 지운 다음 압축한다.
홈페이지 예시에서는 세 파일로 나뉜 셰이더가 397바이트 한 줄짜리 WGSL이 된다.

0.6.0-rc.1부터 `draw`, `effect`, `compute`는 문자열 WGSL을 받지 않는다.
최종 WGSL과 반영 정보, 체크섬, 생성자를 담은 `ShaderSource`(`version: 2`)만
받고, 날 문자열을 넘기면 `VGPU-SHADER-SOURCE-UNPREPARED`를 던진다.
번들러가 있으면 로더가 이를 만들어 주고,
번들러가 없으면 `@vgpu/wgsl/prepare`의 `prepareShader()`로 한 번 감싼다.
그 대가로 브라우저 번들에는 WGSL 파서가 들어가지 않는다.

vgpu에는 TypeScript로 셰이더를 쓰는 자체 DSL이 없다.
다만 예제 갤러리의 TypeGPU Liquid Glass는 TypeGPU의 `"use gpu"` 함수를
`tgpu.resolve()`로 WGSL로 바꾼 뒤 `prepareShader()`로 감싸 vgpu로 그린다.
TypeScript DSL이 필요하면 TypeGPU 같은 도구가 WGSL을 만들고
vgpu는 그 WGSL을 실행하는 분업이 가능하다는 것을 저장소가 직접 보여 준다.

### 런타임별로 WebGPU를 얻는 방법

| 런타임         | 가져오는 경로 | WebGPU 출처                                                  |
| -------------- | ------------- | ------------------------------------------------------------ |
| 브라우저       | `vgpu`        | 브라우저의 네이티브 WebGPU                                   |
| Node.js 22+    | `vgpu/node`   | `webgpu` npm 패키지의 Dawn 프리빌드, 또는 vgpu가 배포한 Dawn |
| 테스트와 CI    | `vgpu/mock`   | GPU 없이 도는 결정론적 소프트웨어 어댑터                     |
| Apple 네이티브 | `vgpu native` | 빌드 시점에 Tint로 WGSL을 Metal로 옮긴 Swift 패키지(베타)    |

Node에는 전역 WebGPU가 없으므로 `@vgpu/adapter-node`가 `webgpu` 패키지의
Dawn 네이티브 프리빌드를 연결한다.
지원 엔진은 Node 22 이상이다.
Linux에서는 디스플레이 서버가 있든 없든 Vulkan이 기본이고,
GPU가 없으면 Mesa lavapipe 같은 CPU 렌더러를 쓴다.
`webgpu@0.4.0`의 Linux ARM64 프리빌드는 glibc 2.38을 요구하므로,
오래된 호스트에서는 `npx vgpu install-dawn`이 glibc 2.31까지 내려가는
vgpu 자체 Dawn 빌드를 받는다.
`npx vgpu install-software-renderer`는 GitHub Release에 올린
lavapipe(`lavapipe-v25.0.7-vgpu.1`)를 받는데,
npm 설치나 `init()`이 몰래 받지 않고 이 명령을 실행해야만 받는다.
`init({ adapter: "auto" | "hardware" | "software" })`나
`VGPU_ADAPTER` 환경 변수로 어댑터를 고른다.

Deno와 Bun은 저장소 문서와 소스 어디에서도 지원 대상으로 언급되지 않는다.
두 런타임에서 `vgpu/node`가 동작하는지는 확인할 수 없었고,
공식으로 검증된 런타임은 브라우저, Node 22, 가짜 어댑터 세 가지로 보는 것이
안전하다(해석).

## 시작하기

아래 코드는 README의 예제다.
직접 실행해 보지는 않았다.

```bash
pnpm add vgpu
pnpm add -D @webgpu/types
```

```ts
// 브라우저: 캔버스에 전체 화면 효과를 그린다
import { clock, init, effect, frameLoop, surface } from "vgpu";
import waveShader from "./wave.wgsl"; // 로더가 준비된 ShaderSource로 바꾼다

const gpu = await init(); // 어댑터와 기기를 얻는 유일한 컨텍스트
const canvasSurface = surface(gpu, canvas, { dpr: [1, 2] }); // DPR을 1~2로 제한
const wave = effect(gpu, waveShader, { set: { speed: 2 } });

const time = clock(gpu);
frameLoop(gpu, (frame) => {
  wave.set({ time: time.time }); // 프레임마다 바뀌는 값만 쓴다
  frame.pass(canvasSurface, wave);
});
```

같은 API가 Node에서는 화면 없이 돈다.

```ts
import { draw, frame, init, target } from "vgpu/node";
import triangleShader from "./triangle.wgsl";

const gpu = await init(); // Dawn 기반 기기
const colorTarget = target(gpu, { size: [256, 256], format: "rgba8unorm" });
const triangle = draw(gpu, { shader: triangleShader });

frame(gpu, (f) => f.pass(colorTarget, triangle));
const pixels = await colorTarget.read(); // RGBA 바이트를 읽어 검증한다
gpu.dispose(); // Node 프로세스를 깨끗하게 끝내려면 필요하다
```

README의 Node 예제는 `colorTarget.read()`를 쓰지만,
0.5.0 CHANGELOG는 `Target`의 `read` 위임을 없앴다고 적고,
`@vgpu/adapter-node` README와 시작하기 문서는
`colorTarget.color.read({ mipLevel: 0, region: "all" })`를 쓴다.
README의 짧은 예제가 최신 API를 따라가지 못한 것으로 보이므로
설치한 버전의 `npx vgpu docs`로 확인하는 편이 낫다(해석).

## 에이전트를 위한 장치

### CLI가 문서이자 진단 도구다

`npx vgpu` 하나로 문서, 예제, 검증, 진단에 들어간다.

| 명령                        | 하는 일                                                |
| --------------------------- | ------------------------------------------------------ |
| `docs`                      | 패키지에 들어 있는 문서를 오프라인으로 찾고 읽는다     |
| `examples`                  | 예제 갤러리를 검색하고 소스를 내려받는다(실행은 안 함) |
| `check`                     | WGSL 파일을 검증하고 반영 정보를 JSON으로 출력한다     |
| `doctor`                    | 이 기계가 헤드리스로 렌더링할 수 있는지 판정한다       |
| `mcp`                       | 문서와 예제를 stdio MCP 도구로 제공한다                |
| `install-dawn`              | 이식용 Dawn 프리빌드를 받아 검증한다                   |
| `install-software-renderer` | 이식용 CPU 렌더러를 받아 검증한다                      |
| `native`                    | Metal 도구 체인으로 넘긴다                             |

`doctor`는 저장소의 첫 ADR이 다루는 주제다.
외부 에이전트 두 개가 어댑터를 얻지 못한 상황을 샌드박스의 한계로 잘못 진단한
일이 있었고, 정적 점검은 통과해도 Dawn이 거부하는 경우가 있었다.
그래서 판정은 실제로 초기화, 그리기, 읽기, 해제를 해 본 결과로 내리고,
정적 검사는 실패를 설명하는 데만 쓴다.
결과는 기본이 JSON이고, 실패마다 Debian/Ubuntu, Fedora/RHEL 등에서 그대로
실행할 수 있는 설치 명령이나 환경 변수를 처방으로 붙인다.

### 스킬, llms.txt, MCP

`npx skills add vercel-labs/vgpu`로 설치하는 스킬은 API 문서를 담지 않는다.
0.4.1에서 스킬을 버전 중립적인 라우터로 바꿔,
프로젝트에 설치된 `vgpu` 버전에 들어 있는 문서를 읽게 했다.
에이전트가 기억하는 옛 API로 코드를 쓰는 문제를 설치된 버전의 문서로
대신 답하게 해서 줄이려는 설계다.
vgpu.sh는 `agents.md`, `llms.txt`, `llms-full.txt`, OpenAPI 3.1로 설명한
읽기 전용 예제 API, 그리고 `https://vgpu.sh/api/mcp` MCP 엔드포인트를 공개한다.

저장소 자체도 에이전트가 개발한다.
`AGENTS.md`는 연구자, API 설계자, 계획자, 구현자, 작성자, 리뷰어 같은
전문 에이전트를 `.subharness/agents/`에 정의하고 `subharness` CLI로 돌린다고
적고, `apps/agent-evals`에는 에이전트가 장면 수학 문서를 얼마나 잘 찾는지 같은
평가 결과가 남아 있다.

## ML 런타임과 기기 나눠 쓰기

vgpu에는 텐서 타입도, 신경망 연산자도 없다.
패키지 소스에서 텐서라는 말은 CHANGELOG에만 나온다.
저장소 설명의 GPU 텐서와 신경망은 0.2.0에서 더한 `initFromDevice(device)`와
`Device.wrapBuffer(buffer)`를 가리킨다.

ONNX Runtime Web 같은 런타임이 이미 WebGPU 기기를 가지고 있을 때,
vgpu가 그 기기를 빌려 써서 모델 출력이 CPU를 거치지 않고 셰이더로 바로 가게
한다.
문서는 이 API가 모델 종류와 무관하며, 비전이든 확산이든 임베딩이든 LLM이든
출력은 vgpu에게 그저 `GPUBuffer`라고 설명한다.
빌려 온 기기는 `gpu.dispose()`가 파괴하지 않는다.

```ts
import * as ort from "onnxruntime-web/webgpu";
import { initFromDevice } from "vgpu";

declare const session: ort.InferenceSession;
declare const input: ort.Tensor;

const gpu = await initFromDevice(await ort.env.webgpu.device); // GPUDevice 하나를 공유
const output = (await session.run({ input })).output; // 모델 출력은 GPU에 남는다
const source = gpu.device.wrapBuffer(output.gpuBuffer); // 복사 없이 감싼다
```

출력을 쓰는 방법은 둘이다.
스냅숏은 GPU 안에서 한 번 복사해 vgpu 소유 버퍼로 옮기므로,
그 뒤에는 런타임의 텐서를 언제 해제해도 된다.
참조는 복사 없이 런타임 버퍼를 감싸므로 수명 규칙을 지켜야 한다.
텐서 유지, 감싸기, 제출, `await gpu.device.queue.flush()`, 래퍼 해제, 텐서 해제
순서이고, flush를 건너뛰는 것은 지원하는 계약이 아니라 실험적 지름길이라고
문서가 분명히 한다.
Node에서는 `onnxruntime-web@1.27.0`, `webgpu@0.4.0`, Node 22 조합으로 검증했다.
예제 갤러리의 `mnist-classifier`, `depth-estimation`, `air-painting`
(MediaPipe Hands)이 이 경로를 쓴다.

수학 시각화도 같은 방식이다.
`vgpu/scene`은 계층, 인스턴스, 카메라, 기하 레시피를 다루지만
완전한 CPU 수학 API나 ECS, 물리, 재질 시스템은 목표가 아니라고 문서가 밝히고,
벡터와 쿼터니언 연산은 선택 의존성인 pmndrs의 `math`에 맡기라고 권한다.
셰이더 쪽 수학은 `@vgpu/wgsl-std`의 `math`, `scene` 모듈이 맡는다.

## 주변 라이브러리와의 관계

저장소에 근거가 있는 관계는 두 가지다.
첫째, three.js와는 경쟁보다 연결을 택했다.
0.4.0에서 더한 `vgpu/three`의 `tslExports()`는 vgpu가 해석한 WGSL 모듈의
`export` 함수를 three.js TSL 노드로 부를 수 있게 한다.
렌더러, 장면, 재질, 렌더 루프는 three.js가 계속 소유하고,
vgpu는 이식 가능한 WGSL 모듈을 공급하는 역할만 한다.
`three`는 선택적 피어 의존성이고, 문서는 `three@^0.180.0`으로 설치하라고 한다.
둘째, 앞에서 본 것처럼 TypeGPU가 만든 WGSL을 vgpu가 실행하는 예제가 있다.

Use.GPU나 WebGPU 기반 텐서 라이브러리와의 비교는 저장소에 없다.
여기서부터는 해석이다.
Use.GPU처럼 선언적 컴포넌트로 GPU 그래프를 짜는 접근과 달리,
vgpu는 명시적 프레임과 자유 함수로 WebGPU에 가깝게 머문다.
텐서 라이브러리와는 겹치지 않고, 그런 라이브러리의 출력 버퍼를 받아
그리는 쪽에 선다.
three.js TSL 컴퓨트 셰이더로 LLM 추론을 돌린 사례는 `llm/llm-in-threejs.md`에,
브라우저 WebGPU를 대상으로 하는 LLM 배포 엔진은 `llm/mlc-llm.md`에 정리돼 있다.
결국 vgpu의 자리는 렌더링 엔진도 ML 프레임워크도 아닌,
WGSL 모듈 시스템과 교차 런타임 실행기, 그리고 에이전트용 도구 상자의 조합이다.

## 트레이드오프

### 준비된 셰이더만 받는 대가

0.6에서 문자열 WGSL을 거부한 덕분에 브라우저 번들에서 파서가 빠지고,
같은 산출물을 여러 그리기가 공유하면 검증을 한 번만 한다.
대신 빌드 단계 없이 셰이더를 즉석에서 만드는 코드,
예를 들어 사용자가 입력한 WGSL을 바로 보여 주는 플레이그라운드는
매번 `prepareShader()`를 거쳐야 하고, 그 순간 파서가 번들에 다시 들어온다.
런타임 생성과 작은 번들을 동시에 가질 수는 없다.

### 25KB라는 숫자는 고정값이 아니다

README는 전체 화면 효과가 gzip 25KB로 나가며 CI가 이 예산을 지킨다고 쓴다.
`packages/vgpu-api/package.json`의 `effect-only` 예산은 v0.2.0에서 25,600바이트,
v0.5.0에서 28,160바이트, 0.6.0-rc.0에서 32,256바이트,
0.6.0-rc.1에서 43,008바이트, rc.2에서 43,520바이트다.
예산은 측정값보다 큰 다음 512바이트 배수로 정하므로 실제 크기도 비슷하게 늘었다.
CI가 1바이트라도 넘으면 실패시키는 것은 맞지만, 승인을 거쳐 예산을 올리는
커밋(`chore(vgpu): account for approved encode cache bundle cost`)이 정상
절차로 존재한다.
CI 게이트는 크기를 고정하지 않고, 크기가 늘 때마다 사람이 승인하게 만들 뿐이다.
0.6으로 올라갈 때는 README의 25KB가 아니라 자기 번들을 직접 재야 한다.

### 에이전트 우선 설계와 사람의 비용

오프라인 문서, 구조화된 오류 코드(`VGPU-NODE-NO-ADAPTER` 등),
JSON 진단은 사람에게도 이롭다.
하지만 0.x 동안 거의 매 마이너마다 깨지는 변경이 있었고,
그 충격을 버전별 문서와 마이그레이션 가이드로 흡수하는 구조다.
에이전트는 설치된 버전의 문서를 매번 다시 읽으면 되지만,
사람 팀은 매 업그레이드마다 그 문서를 읽을 시간이 필요하다.
이 속도는 에이전트가 코드를 고치는 비용이 낮다는 전제 위에서만
감당할 수 있다(해석).

## 함정

- README의 짧은 예제가 최신 API와 어긋날 수 있다.
  Node 예제의 `colorTarget.read()`가 그런 예다.
- 0.1.4에서 `effect()`의 UV 원점이 왼쪽 위로 바뀌었다.
  이전 동작이 필요하면 `vec2f(uv.x, 1.0 - uv.y)`로 뒤집어야 한다.
- 참조 모드로 ML 출력을 감쌀 때 flush 전에 텐서를 해제하면 안 된다.
- `frame`과 `frameLoop` 콜백은 비동기 함수가 될 수 없다.
  0.6.0-rc.0부터 Promise를 돌려주는 콜백을 거부한다.
- Linux ARM64에서 `webgpu@0.4.0`은 glibc 2.38 미만이면 로드되지 않는다.
- Dawn의 OpenGL 백엔드는 명시적으로 고를 때만 쓰이며,
  제한된 밉 뷰와 스토리지 쓰기 버그(392121637)가 알려져 있다.
- `@vgpu/native`의 npm 0.0.1은 이름만 잡아 둔 빈 패키지다.
  실제 베타는 `next` 태그의 RC를 정확한 버전으로 고정해 받아야 한다.

## 체크리스트

- 설치한 `vgpu`가 `latest`(0.5.0)인지 `next`(0.6 RC)인지 확인했는가?
- 번들러에 `@vgpu/wgsl` 로더를 연결했거나 `prepareShader()`를 쓰는가?
- CI 기계에서 `npx vgpu doctor`가 `healthy`를 돌려주는가?
- 단위 테스트는 `vgpu/mock`으로, 픽셀 검증은 `vgpu/node`로 나눴는가?
- Node 프로세스 끝에서 `gpu.dispose()`를 부르는가?
- 자기 앱의 gzip 번들 크기를 업그레이드 전후로 직접 쟀는가?
- 공유 기기로 ML 출력을 쓸 때 스냅숏과 참조 중 무엇을 쓰는지 정했는가?
- Deno나 Bun에서 돌려야 한다면 직접 검증했는가?

## 기억할 원칙

### 에이전트용 라이브러리는 문서를 코드와 같은 버전으로 묶는다

vgpu가 가장 공들인 부분은 렌더링 API보다 문서가 도착하는 경로다.
문서를 패키지에 넣고, 스킬은 라우터로만 두고, 진단은 실제 렌더링으로 하고,
문서 예제는 `vgpu/mock`으로 실행해 API와 어긋나지 않게 검사한다.
에이전트가 틀리는 가장 흔한 이유가 학습 시점의 옛 API라는 점을 생각하면,
버전이 맞는 문서를 기계가 읽는 형태로 손 닿는 곳에 두는 것이
API를 아름답게 다듬는 것보다 효과가 크다(해석).
그래도 README 예제가 어긋난 것처럼, 검사 범위 밖의 문서는 여전히 낡는다.

### 경계가 좁을수록 연결이 쉽다

텐서도, 장면 그래프도, 재질 시스템도 갖지 않기로 한 결정 덕분에
vgpu는 ONNX Runtime, three.js, TypeGPU, pmndrs `math`와 겹치지 않고 붙는다.
기기를 빌려 쓰되 파괴하지 않고, 버퍼를 감싸되 소유하지 않는다는 규칙이
그 연결을 가능하게 한다.
저장소 설명이 내세우는 텐서와 신경망은 이 좁은 경계의 결과이지
vgpu가 그 일을 한다는 뜻이 아니라는 점을 기억해야 한다.

