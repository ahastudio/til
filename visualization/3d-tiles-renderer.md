# 3d-tiles-renderer: 이미 쓰는 three.js, Babylon.js, r3f 장면 안에서 3D Tiles를 스트리밍하는 NASA JPL의 렌더러

<https://github.com/NASA-AMMOS/3DTilesRendererJS>

데모: <https://nasa-ammos.github.io/3DTilesRendererJS/three/mars.html>

## 소개

3d-tiles-renderer는 3D Tiles를 이미 가진 three.js, Babylon.js,
react-three-fiber(r3f) 장면 안에서 스트리밍해 그리는 JavaScript 라이브러리다.
저장소 설명은 “Renderer for 3D Tiles in Javascript using three.js,
Babylon.js, and r3f”다.
카메라, 조명, 후처리, 렌더 루프는 사용자가 쥐고,
라이브러리는 타일셋을 순회하며 어떤 타일을 받아서 보여 줄지만 맡는다.
CesiumJS처럼 지구본, 카메라, 장면을 통째로 가져오는 엔진이 아니라
기존 3D 앱에 끼우는 부품이라는 점이 이 라이브러리의 자리다.

2026년 10월 22일 GitHub 기준으로 별 2,503개, 포크 428개, 열린 이슈 115개다.
라이선스는 Apache-2.0이고 저장소는 2020년 1월 30일에 만들어졌다.
마지막 푸시는 2026년 10월 21일이고, 최신 릴리스는 2026년 9월 18일의 v0.5.3이다.
npm 주간 다운로드는 2026년 10월 12일부터 18일까지 106,214회였다.[^npm-downloads]

저장소의 README는 이 렌더러가 3D Tiles 명세의 대부분을 지원하지만
몇 가지 예외가 있다고 밝힌다.
어떤 기능이 아직 없는지는 “Feature Complete” 마일스톤에서 확인하라고 안내한다.
이 문서는 그 말이 오늘 무엇을 뜻하는지,
어떻게 붙이고 어디서 막히는지를 코드와 릴리스 기록으로 확인해 정리한다.

이 문서가 직접 실행한 것은 npm 설치와 짧은 Node 스크립트뿐이다.
브라우저에서 타일셋을 그려 보지는 않았고,
성능 수치는 하나도 측정하지 않았다.
“확인하기” 절에 무엇을 실행했고 무엇을 하지 않았는지 적었다.

## 목차

- [소개](#소개)
- [이 렌더러는 어디서 왔고 어디까지 왔나](#이-렌더러는-어디서-왔고-어디까지-왔나)
  - [화성 탐사 도구에서 시작했다](#화성-탐사-도구에서-시작했다)
  - [포럼 글로 따라가 보는 6년](#포럼-글로-따라가-보는-6년)
  - [포럼 글이 오래된 곳](#포럼-글이-오래된-곳)
- [구성: 하나의 패키지, 여러 개의 엔트리](#구성-하나의-패키지-여러-개의-엔트리)
- [동작 방식](#동작-방식)
  - [타일셋은 오류 예산으로 순회된다](#타일셋은-오류-예산으로-순회된다)
  - [캐시는 하드 캡이다](#캐시는-하드-캡이다)
  - [v0.5.0부터 캐시와 큐는 기본으로 공유된다](#v050부터-캐시와-큐는-기본으로-공유된다)
- [사용하기](#사용하기)
  - [three.js](#threejs)
  - [react-three-fiber](#react-three-fiber)
  - [Babylon.js](#babylonjs)
  - [인증과 데이터 제공자](#인증과-데이터-제공자)
  - [플러그인 지도](#플러그인-지도)
- [값 정하기](#값-정하기)
- [다른 선택지와 견주기](#다른-선택지와-견주기)
  - [CesiumJS](#cesiumjs)
  - [iTowns, Giro3D, deck.gl, Potree](#itowns-giro3d-deckgl-potree)
- [함정](#함정)
  - [루트 엔트리에서 플러그인을 찾으면 없다](#루트-엔트리에서-플러그인을-찾으면-없다)
  - [인스턴스 캐시를 따로 두는 코드가 오래됐을 수 있다](#인스턴스-캐시를-따로-두는-코드가-오래됐을-수-있다)
  - [0.x 버전의 폐기 주기](#0x-버전의-폐기-주기)
  - [3D Tiles 명세를 다 구현한 것은 아니다](#3d-tiles-명세를-다-구현한-것은-아니다)
  - [열린 문제는 작지 않다](#열린-문제는-작지-않다)
  - [데이터 제공자 쪽의 제약이 따라온다](#데이터-제공자-쪽의-제약이-따라온다)
- [확인하기](#확인하기)
- [비평](#비평)
  - [이 도구의 약속은 코드가 아니라 사용자의 장면에 있다](#이-도구의-약속은-코드가-아니라-사용자의-장면에-있다)
  - [사용량이 늘어도 유지의 구조는 좁다](#사용량이-늘어도-유지의-구조는-좁다)
  - [제3자 요약은 저장소보다 느리다](#제3자-요약은-저장소보다-느리다)
- [인사이트](#인사이트)
  - [이 라이브러리가 푸는 것은 렌더링보다 데이터의 길이다](#이-라이브러리가-푸는-것은-렌더링보다-데이터의-길이다)
  - [엔진 중립 코어는 이 프로젝트의 가장 큰 자산이자 가장 큰 비용이다](#엔진-중립-코어는-이-프로젝트의-가장-큰-자산이자-가장-큰-비용이다)
  - [기본값 공유는 편해졌지만 디버깅 책임을 옮겼다](#기본값-공유는-편해졌지만-디버깅-책임을-옮겼다)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)
  - [이 라이브러리는 엔진의 한 부품으로 쓴다](#이-라이브러리는-엔진의-한-부품으로-쓴다)
  - [먼저 데이터를 확인하고 나서 렌더러를 고른다](#먼저-데이터를-확인하고-나서-렌더러를-고른다)

## 이 렌더러는 어디서 왔고 어디까지 왔나

### 화성 탐사 도구에서 시작했다

이 프로젝트는 NASA JPL에서 화성 탐사 데이터를 보여 주려고 만든 렌더러다.
저장소 관리자 gkjohnson은 2022년 10월 29일 three.js 포럼에 쓴 소개글에서
JPL의 화성 임무가 궤도선과 탐사 로버의 데이터로 3D Tiles 데이터셋을 만들고,
이 렌더러가 Perseverance와 Curiosity 임무의 도구에 쓰여 왔다고
적었다.[^forum-announce]
같은 글은 Curiosity의 Dingo Gap 데이터셋 데모와
“Explore with Perseverance” 웹 체험에도 쓰였다고 밝힌다.
저장소 README의 첫 예제가 지금도 Dingo Gap 화성 타일셋인 이유가 여기에 있다.

JPL이 내부에서 쓰는 타일 생성 파이프라인은 공개되어 있지 않다.
한 사용자가 화성 데이터셋을 어떤 변환기로 만들었느냐고 묻자
gkjohnson은 그 파이프라인이 JPL 내부용이고
화성이 아닌 데이터에는 쉽게 쓸 수 없다고 답했다.[^tjb-24][^gkjohnson-25]
그 대신 README가 링크하는 3D Tiles 생성 도구 목록을 보라고 안내했다.
그러니 이 라이브러리를 쓰려는 사람은 타일셋을 만드는 쪽을 따로 해결해야 한다.

### 포럼 글로 따라가 보는 6년

포럼 소개글 아래에는 gkjohnson이 새 릴리스를 알린 글이 이어진다.
아래 표는 그 글과 저장소 릴리스 기록을 맞춰 본 것이다.
포럼 글의 날짜와 버전은 글에 적힌 대로 옮겼고,
2026년 릴리스 내용은 저장소의 릴리스 노트에서 읽었다.

| 시점       | 버전    | 무엇이 붙었나                                                                    |
| ---------- | ------- | -------------------------------------------------------------------------------- |
| 2022-10-29 | 소개글  | three.js 렌더러로 공개, 화성 임무에 사용[^forum-announce]                        |
| 2023-06-20 | v0.3.19 | Google Photorealistic 3D Tiles 지원과 지구본 로딩 클래스[^gkjohnson-6]           |
| 2023-06-29 | v0.3.20 | 절두체 컬링 최적화, 일부 장면에서 그려지는 타일 45% 감소[^gkjohnson-7]           |
| 2024-01-17 | 예제    | GlobeControls와 타일 페이드 전환 예제[^gkjohnson-8]                              |
| 2024-07-29 | v0.3.36 | 플러그인 구조, 직교 카메라 GlobeControls, Cesium 생태계 지원금[^gkjohnson-9]     |
| 2024-10-15 | v0.3.39 | react-three-fiber 공식 지원[^gkjohnson-11]                                       |
| 2025-02-14 | v0.4.5  | Deep Zoom, XYZ, TMS 타일[^gkjohnson-23]                                          |
| 2025-07-28 | v0.4.13 | 등고선 재질, Quantized Mesh, 텍스처 오버레이[^gkjohnson-28]                      |
| 2025-09-26 | v0.4.17 | WMTS, WMS, GeoJSON 오버레이, 주간 다운로드 7,000회 이상[^gkjohnson-29]           |
| 2026-05-22 | v0.4.25 | Babylon.js 지원, loadAncestors, 가우시안 스플랫 커뮤니티 플러그인[^gkjohnson-33] |
| 2026-07-15 | v0.5.0  | 폐기된 API 제거, 캐시와 큐 기본 공유                                             |
| 2026-09-18 | v0.5.3  | Potree 플러그인, 점군 효과, 표면(surface) 개념, stats.refused                    |

표의 포럼 글은 모두 gkjohnson 본인이 쓴 것이다.
지구본 컨트롤과 페이드 전환 같은 기능은 처음에 예제 코드로 나왔다.
2024년 1월 글은 두 예제가 나중에 코어에 합쳐질 수 있다고 적었다.[^gkjohnson-8]
지금 패키지의 `three` 엔트리에는 `GlobeControls`가,
`plugins` 엔트리에는 `TilesFadePlugin`이 들어 있다.

사용량은 글마다 숫자가 적혀 있다.
2025년 9월 글은 주간 다운로드가 7,000회를 넘었다고 하고,[^gkjohnson-29]
2026년 5월 글은 21,000회를 넘어 1년 전의 약 4,500회에서 5배 가까이 늘었다고
한다.[^gkjohnson-33]
npm의 공개 집계로는 2026년 10월 둘째 주가 106,214회였다.[^npm-downloads]
이 세 숫자는 다른 때에 다른 방식으로 읽은 것이어서
한 줄의 성장 곡선으로 잇지는 않는다.
다만 5개월 사이에 5배 정도 늘었다는 점만큼은 npm의 집계가 뒷받침한다.

### 포럼 글이 오래된 곳

포럼 글은 시점이 고정된 기록이어서 오늘과 다른 부분이 있다.
2022년 소개글의 데모 주소는
`example/bundle/mars.html` 경로이고,[^forum-announce]
오늘 README의 Dingo Gap 데모는 `three/mars.html` 경로다.
렌더러가 three.js 전용이던 시절의 설명도 지금과 다르다.
소개글은 three.js용 구현으로 소개되었고,
Babylon.js 지원은 2026년 5월에야 릴리스 글에 등장한다.[^gkjohnson-33]
2025년 1월 글은 iTowns와 Giro3D 프로젝트의 지원에 감사하고,
Cesium ion이 데모용 키를 제공했다고 적었다.[^gkjohnson-17]
2026년 현재 README의 “Community Resources”에는 iTowns, Giro3D, MapLibre 연동,
three-geospatial, threepipe 플러그인, 3DBAG 뷰어가 올라 있다.

## 구성: 하나의 패키지, 여러 개의 엔트리

패키지 이름은 `3d-tiles-renderer` 하나이고 서브패스로 나뉜다.
`package.json`의 `exports`는 `.`, `./core`, `./three`, `./r3f`, `./babylonjs`,
`./plugins`, `./core/plugins`, `./three/plugins`,
`./babylonjs/plugins`를 정의한다.
README의 표는 `core`, `three`, `babylonjs`, `r3f`를 렌더러 엔트리로,
`three/plugins`, `babylonjs/plugins`,
`core/plugins`를 플러그인 엔트리로 안내한다.
엔진에 무관한 순회와 캐시는 `core`에 있고,
`three`와 `babylonjs`가 그것을 각 엔진의 장면 그래프에 맞춘다.

피어 의존성은 `three >= 0.167.0`이고,
`@react-three/fiber`는 `^8.17.9 || ^9.0.0`, `react`는 18.3.1 또는 19,
`@babylonjs/core`와 `@babylonjs/loaders`는 `>= 8.0.0`이다.
r3f와 Babylon.js 쪽은 `peerDependenciesMeta`에서 선택 의존성으로 표시되어 있다.
`@mapbox/vector-tile`, `pbf`, `pmtiles`는 일반 의존성이다.
v0.4.28 릴리스 노트는 이 세 패키지를 필수 의존성으로 넣었다고 적었다.
번들러에서 설치되지 않아 실패하는 일을 막으려는 조치였다.

이 문서가 설치해 본 환경에서는 `three`가 0.186.1로 풀렸다.
`3d-tiles-renderer`는 0.5.3이었고, 설치된 최상위 패키지는 아홉 개였다.
루트 엔트리 `3d-tiles-renderer`가 내보내는 이름은 48개이고
`TilesRenderer`, `GlobeControls`, `EnvironmentControls`, `LRUCache`,
`PriorityQueue`, `B3DMLoader` 같은 것이 들어 있다.
플러그인은 루트가 아니라 `3d-tiles-renderer/plugins`에서 따로 가져온다.
이 구분은 아래 “함정”에서 다시 다룬다.

## 동작 방식

### 타일셋은 오류 예산으로 순회된다

3D Tiles는 타일의 트리다.
각 타일은 경계 부피와 기하 오차(geometric error)를 갖고,
카메라에서 본 화면상 오차가 목표보다 크면 더 자세한 자식 타일로 내려간다.
`errorTarget`의 기본값은 16픽셀이다.
이 값이 작을수록 더 세밀한 타일을 요구하고,
커질수록 더 거친 타일에서 멈춘다.

`TilesRenderer.update()`를 매 프레임 부르면
그 프레임에서 보일 타일과 불러야 할 타일을 결정하고
다운로드, 파싱, 노드 처리를 각각의 큐에 넣는다.
`maxTilesProcessed`는 한 번의 순회에서 즉시 처리할 타일 수이고 기본값은 250이다.
이 값을 낮추면 프레임 끊김이 줄지만 새 타일셋이 뜨는 속도가 느려진다고
API 문서는 설명한다.

### 캐시는 하드 캡이다

`LRUCache`는 `maxSize`(기본 8000개)와 `maxBytesSize`(기본 약 430MB),
회수 후 남길 `minBytesSize`(기본 약 322MB)로 제한된다.
바이트 한도는 three.js r166 이상에서만 동작한다고 API 문서에 적혀 있다.
README의 “Gotchas”는 이 한도가 차면
새 타일을 더 불러오지 않는다고 분명히 밝힌다.
현재 시점에 필요한 타일이 한도 안에 다 들어오지 않으면
더 거친 타일이 표시되고 세분화가 멈춘다.
화질이 낮아지는 원인이 네트워크가 아니라 캐시 한도일 수 있다는 뜻이다.

v0.5.3은 이 상황을 보려는 `stats.refused`를 더했다.
마지막 업데이트에서 캐시가 가득 차서 큐에 넣지 못한 타일의 수다.
설치한 패키지에서 `stats` 객체의 키를 읽어 보니
`inCacheSinceLoad`, `inCache`, `queued`, `downloading`, `parsing`, `loaded`,
`failed`, `inFrustum`, `used`, `active`, `visible`, `refused`,
`tilesProcessed`가 있었다.

### v0.5.0부터 캐시와 큐는 기본으로 공유된다

v0.5.0 릴리스 노트에는 이렇게 적혀 있다.
`TilesRenderer`의 모든 인스턴스는 `processNodeQueue`, `lruCache`,
`downloadQueue`, `priorityQueue`를 따로 지정하지 않으면 공유한다.
이 문서가 실제로 확인한 결과도 같았다.
같은 프로세스에서
인스턴스 두 개를 만들어 `lruCache`와 `downloadQueue`를 비교하니
둘 다 같은 객체였다.
`USAGE.md`에는 아직 인스턴스마다 캐시를 직접 공유시키는 예제가 남아 있다.
v0.5.0 이전에 필요했던 코드이고, 지금은 공유가 기본이라 중복이다.

## 사용하기

### three.js

아래는 `USAGE.md`의 기본 예제를 줄여 옮긴 것이다.
이 문서에서 브라우저로 실행해 보지는 않았다.

```js
import { Sphere } from 'three';
import { TilesRenderer } from '3d-tiles-renderer';

const tilesRenderer = new TilesRenderer( './path/to/tileset.json' );
tilesRenderer.setCamera( camera );
tilesRenderer.setResolutionFromRenderer( camera, renderer );

// 타일셋이 원점에서 멀리 떨어져 있으면 중심을 원점으로 옮긴다
tilesRenderer.addEventListener( 'load-root-tileset', () => {

	const sphere = new Sphere();
	tilesRenderer.getBoundingSphere( sphere );
	tilesRenderer.group.position.copy( sphere.center ).multiplyScalar( - 1 );

} );

scene.add( tilesRenderer.group );

function renderLoop() {

	requestAnimationFrame( renderLoop );

	// update 전에 카메라 행렬이 최신이어야 한다
	camera.updateMatrixWorld();
	tilesRenderer.update();
	renderer.render( scene, camera );

}
renderLoop();
```

화면상 오차를 계산하려면 카메라와 화면 해상도가 필요하므로
`setCamera`와 `setResolutionFromRenderer` 호출을 빠뜨리지 않아야 한다.
호출을 빠뜨렸을 때 실제로 무슨 일이 생기는지는 이 문서가 확인하지 않았다.

### react-three-fiber

r3f 엔트리는 컴포넌트로 같은 일을 한다.
README가 안내하는 사용법의 뼈대는 아래와 같다.

```jsx
import { TilesRenderer, TilesPlugin, GlobeControls, TilesAttributionOverlay }
	from '3d-tiles-renderer/r3f';
import { DebugTilesPlugin, GoogleCloudAuthPlugin }
	from '3d-tiles-renderer/plugins';

export default function App() {

	return (
		<Canvas camera={ { position: [ 0, 0, 1e8 ] } }>
			<TilesRenderer>
				<TilesPlugin plugin={ GoogleCloudAuthPlugin }
					args={ { apiToken: /* 발급받은 키 */ } } />
				<GlobeControls />
				<TilesAttributionOverlay />
			</TilesRenderer>
		</Canvas>
	);

}
```

`TilesAttributionOverlay`는 데이터 제공자의 저작자 표시를 화면에 띄운다.
r3f 문서는 Google과 Cesium ion 같은 데이터를 쓸 때 이 표시를 쓰라고 안내한다.

### Babylon.js

Babylon.js 엔트리는 `scene.useRightHandedSystem = true`를 요구한다.
설명서가 밝힌 한계는 다음과 같다.
오른손 좌표계의 장면만 지원한다.
경계 상자와 절두체 검사에 축 정렬 경계 상자(AABB)를 써서 오탐이 생긴다.
3D Tiles의 `boundingRegion`은 아직 지원하지 않는다.
타일 캐싱이 제한적이고, I3DM과 PNTS는 지원하지 않는다.
Babylon.js 엔트리를 고르는 이유가 있다면 이 목록을 먼저 읽어야 한다.

### 인증과 데이터 제공자

Google Photorealistic Tiles와 Cesium ion 예제는 각각 API 키가 필요하다고
README가 각주로 밝힌다.
키는 `GoogleCloudAuthPlugin`과 `CesiumIonAuthPlugin`에 넘긴다.
Cesium ion의 지형 자산에서는 `assetTypeHandler` 콜백으로
`QuantizedMeshPlugin`을 등록하라고 플러그인 안내가 설명한다.

### 플러그인 지도

플러그인은 렌더러의 기능이 아니라 그 위에 얹는 선택 부품이다.
`3d-tiles-renderer/plugins`가 실제로 내보내는 이름을 설치본에서 읽어
역할별로 묶으면 다음과 같다.

| 역할            | 설치본에서 확인한 이름                                                                                                                 |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 인증과 제공자   | `CesiumIonAuthPlugin`, `GoogleCloudAuthPlugin`, `GoogleMapsOverlay`                                                                    |
| 이미지 오버레이 | `ImageOverlayPlugin`, `XYZTilesOverlay`, `TMSTilesOverlay`, `WMSTilesOverlay`, `WMTSTilesOverlay`, `DeepZoomOverlay`, `GeoJSONOverlay` |
| 벡터 타일       | `MVTOverlay`, `PMTilesOverlay`, `MVTAnnotationsPlugin`                                                                                 |
| 지형            | `QuantizedMeshPlugin`, `TerrainRGBMeshPlugin`, `TerrariumMeshPlugin`, `GeneratedSurfacePlugin`                                         |
| 점군            | `PotreePlugin`, `PointCloudEffectsPlugin`                                                                                              |
| 표현과 성능     | `TilesFadePlugin`, `TileCompressionPlugin`, `UnloadTilesPlugin`, `BatchedTilesPlugin`, `UpdateOnChangePlugin`                          |
| 영역과 변형     | `LoadRegionPlugin`, `TileFlatteningPlugin`, `ReorientationPlugin`                                                                      |
| 명세 구현       | `ImplicitTilingPlugin`, `GLTFMeshFeaturesExtension`, `GLTFExtensionsPlugin`                                                            |
| 개발 보조       | `DebugTilesPlugin`, `EnforceNonZeroErrorPlugin`                                                                                        |

`TextureOverlayPlugin`과 `TopoLinesPlugin`은 패키지에 들어 있지 않다.
플러그인 안내는 둘을 “예제 디렉터리에 있고
메인 패키지의 일부가 아니다”라고 분류한다.
설치본의 `plugins` 엔트리에서 `TextureOverlayPlugin`을 찾아도 없었다.

가우시안 스플랫과 3D Tiles 스타일 언어, glTF 외곽선 확장은
저장소 밖의 커뮤니티 플러그인이다.
플러그인 안내의 “Community Plugins & Integrations” 목록이 그 출처이고,
이 문서는 그 플러그인을 직접 실행해 보지 않았다.
2026년 5월 포럼 글은 가우시안 스플랫 타일셋이
SparkJS 기반의 커뮤니티 플러그인 덕에
렌더링된다고 소개했다.[^gkjohnson-33]

## 값 정하기

기본값이 맞지 않을 때 어떤 값을 어느 쪽으로 움직일지를 정리한다.
아래 표의 기본값은 설치한 0.5.3에서 읽은 값이다.
“근거” 열은 API 문서와 README가 밝힌 효과이고,
“측정” 열은 값을 고칠 때 볼 지표다.
이 문서는 어떤 값도 실측으로 정하지 않았으므로 시작점으로만 읽는다.

| 값                  | 기본값   | 올리거나 켜면                    | 내리거나 끄면                    | 측정                         |
| ------------------- | -------- | -------------------------------- | -------------------------------- | ---------------------------- |
| `errorTarget`       | 16       | 더 거친 타일, 적은 다운로드      | 더 세밀한 타일, 캐시 압박        | `stats.refused`, 프레임 시간 |
| `maxBytesSize`      | 약 430MB | 세밀한 장면이 한 번에 들어간다   | 메모리 절약, 거친 타일에 머문다  | `lruCache.cachedBytes`       |
| `maxSize`           | 8000     | 타일 수가 많은 장면을 담는다     | 개수 기준으로 먼저 회수된다      | `lruCache.isFull()`          |
| `maxTilesProcessed` | 250      | 새 타일셋이 빨리 뜬다            | 프레임 끊김이 줄어든다           | 첫 로드의 프레임 시간        |
| `errorFalloff`      | 0 (꺼짐) | 먼 타일이 더 거칠어진다          | 효과 없음                        | 먼 장면의 타일 수            |
| `loadAncestors`     | `true`   | 첫 로드가 부드럽지만 메모리 증가 | 바로 고해상도로 가지만 틈이 생김 | 메모리, 첫 화면까지의 시간   |

`errorFalloff`는 Cesium의 `dynamicScreenSpaceError`에
견줄 수 있는 실험 기능이라고
API 문서가 경고한다.
`loadSiblings`와 `loadAncestors`도 같은 문서에서 실험 기능으로 분류되어 있다.
`loadAncestors`를 켜면 `loadSiblings`도 암묵적으로 켜진다.

가장 먼저 볼 것은 `maxBytesSize`다.
화질이 기대보다 낮을 때 `stats.refused`가 0보다 크다면
캐시가 가득 차서 세분화가 멈춘 것이다.
그 경우 `errorTarget`을 올려 덜 세밀하게 받거나 `maxBytesSize`를 올려야 한다.

## 다른 선택지와 견주기

### CesiumJS

CesiumJS는 3D Tiles의 참조 구현이고 자체 장면, 카메라, 지구본을 가진다.
Cesium 블로그는 이 렌더러가 JPL에서
시작해 지금은 Garrett Johnson이 관리한다고 소개한다.
같은 글은 그가 2024년 4월 Cesium 생태계 지원금을 받아
3D Tiles 1.1의 glTF 메타데이터 확장과 텍스처 오버레이를 추가했다고
적었다.[^cesium-blog]
Cesium은 CesiumJS를 만들고
Cesium ion 서비스를 운영하는 회사라는 점을 감안해 읽어야 한다.
그 글은 자기 생태계의 지원금이 만든 성과를 설명하는 글이다.

이 문서가 뽑은 판단 기준은 다음 한 가지다.
지구본이 앱의 중심이고 카메라와 장면을 엔진에 맡겨도 되면 CesiumJS가 단순하다.
이미 쓰는 three.js 앱이나 Babylon.js 앱 안의 한 구역으로 타일셋을 넣으려면
이 렌더러가 맞다.
HysenLabs의 편집 글도 같은 결론을 낸다.
CesiumJS는 장면, 카메라, 지구본, 타일 스케줄링을 소유하고
이 렌더러는 소유하지 않는다는 것이다.[^hysen]
이 문서는 그 글이 README를 다시 정리한 글이라고 읽고,
독립된 검증으로 쓰지 않았다.

### iTowns, Giro3D, deck.gl, Potree

README의 “Community Resources”는 iTowns와 Giro3D를
이 렌더러를 쓰는 지리공간 프레임워크로 소개한다.
둘은 렌더러가 아니라 프레임워크여서 이 라이브러리와 층이 다르다.
포럼에서도 iTowns 쪽의 지원이 언급됐다.[^gkjohnson-17]
deck.gl과 Potree는 README가 비교 대상으로 다루지 않아서
이 문서는 그 둘과의 우열을 판단하지 않는다.
다만 v0.5.3의 `PotreePlugin`은 Potree 데이터셋을 이 렌더러 안에서
읽는 길을 연다.

## 함정

### 루트 엔트리에서 플러그인을 찾으면 없다

Cesium 블로그의 2024년 예제는 `GLTFMeshFeaturesExtension`과
`GLTFStructuralMetadataExtension`을 `3d-tiles-renderer` 루트에서
가져온다.[^cesium-blog]
설치한 0.5.3의 루트 엔트리에는 이 이름들이 없고
`3d-tiles-renderer/plugins`에서 내보낸다.
블로그 예제를 그대로 옮겨 쓰면 가져오기가 실패한다.
같은 블로그 글의 `TextureOverlayPlugin` 콜백
시그니처는 `(scene, tile, plugin)`이지만
플러그인 안내의 현재 시그니처는 `(tile, model, plugin)`이다.
블로그는 이 시점의 기록으로만 읽는 것이 안전하다.

### 인스턴스 캐시를 따로 두는 코드가 오래됐을 수 있다

v0.5.0 이후에는 공유가 기본이다.
`USAGE.md`의 “공유 캐시” 절 코드는 필요 없고,
반대로 인스턴스마다 캐시를 분리하고 싶다면 새 객체를 직접 할당해야 한다.
이 동작은 릴리스 노트와 설치본에서 확인했지만
분리를 실제로 시도해 보지는 않았다.

### 0.x 버전의 폐기 주기

v0.5.0은 “폐기된 API와 필드를 제거했다”고 릴리스 노트에 적었다.
v0.5.3도 `GeneratedSurfacePlugin`의 `shape` 옵션을 폐기 예정으로 돌렸다.
`package.json`의 `exports`에는 `./src/*` 통과 경로도 있다.
문서화되지 않은 경로까지 가져다 쓸 수 있으므로 업그레이드할 때 깨질 여지가 크다.
서브패스 엔트리를 통해서만 가져오는 편이 안전하다.

### 3D Tiles 명세를 다 구현한 것은 아니다

“Feature Complete” 마일스톤의 열린 이슈는 두 개다.
하나는 Viewer Request Volume 지원을 요청하는 이슈 74번이고,
다른 하나는 “3D Tiles Next(3D Tiles 1.1) 기능” 체크리스트인 이슈 235번이다.
이슈 #235의 체크리스트는 `3DTILES_content_gltf`와 `EXT_mesh_features`에만
표시가 있고, `3DTILES_multiple_contents`, `3DTILES_implicit_tiling`,
`3DTILES_bounding_volume_S2`, `3DTILES_metadata`는 표시가 없다.
그런데 설치본의 코어 플러그인 엔트리에는 `ImplicitTilingPlugin`이 들어 있다.
체크리스트가 갱신되지 않았을 수도 있고, 구현이 일부만 되었을 수도 있다.
이 문서는 어느 쪽인지 판단하지 못했다.
3D Tiles 1.1은 glTF 직접 콘텐츠, 구조화 메타데이터, 다중 콘텐츠,
암시적 타일링을 더한 버전이고 b3dm, i3dm, pnts,
cmpt는 폐기 예정으로 돌렸다.[^spec-readme]
쓰려는 타일셋이 1.1의 어느 기능에 기대는지 먼저 확인해야 한다.

### 열린 문제는 작지 않다

최근 열린 이슈 가운데는 `BatchTable.getDataFromId`가
이진 VEC2, VEC3, VEC4 속성에서 숫자 하나만 돌려준다는 이슈(#1772),
`ImageOverlayPlugin`에서
오버레이를 바꾸는 동안 오류와 검은 타일이 생긴다는 이슈(#1769),
`UnloadTilesPlugin`으로 다시 방문한 타일이 GPU 캐시에서
계속 회수 대상이라는 이슈(#1767),
진행 중인 요청 취소를 고려하자는 이슈(#1609)가 있다.
또 PlayCanvas 엔진 지원을 `3d-tiles-renderer/playcanvas`로
추가하자는 제안(#1763)이 열려 있다.
이슈 본문은 PlayCanvas 엔진 팀이 그 부분을 맡겠다는 내용을 담는다.
이 이슈들은 모두 사용자나 기여자의 보고이며 이 문서가 재현한 것은 아니다.

### 데이터 제공자 쪽의 제약이 따라온다

Google Photorealistic Tiles나 Cesium ion을
쓰는 예제는 각자의 키와 약관이 필요하다.
라이선스가 Apache-2.0이어도 그 데이터까지 자유로운 것은 아니다.
한 포럼 사용자는 2023년에 Google Map Tiles API의 타일마다 키가 필요하다는 점에서
막혔다고 적었고,[^lawrence3dpk-2]
gkjohnson은 `fetchOptions`와 URL 전처리
훅으로 Cesium ion과 같은 방식으로 풀 수 있다고
답했다.[^gkjohnson-3]
같은 시기의 한 사용자는 파일은 받아졌는데 장면에 아무것도 보이지 않는다고
도움을 청했다.[^aiden-4]
지금은 공식 Google 플러그인이 있어 이 문제 자체는 달라졌지만,
키가 요청마다 붙는다는 구조는 같다.

## 확인하기

이 문서가 설치와 실행으로 확인한 범위와 그 방법이다.
작업 디렉터리는 저장소 밖의 임시 폴더였고, 브라우저는 열지 않았다.

```bash
mkdir probe && cd probe && npm init -y
npm install 3d-tiles-renderer three
```

```js
// probe.mjs: 설치본의 버전, 엔트리별 내보내기, 기본값을 읽는다
import { readFileSync } from 'node:fs';

const pkg = JSON.parse( readFileSync( 'node_modules/3d-tiles-renderer/package.json', 'utf8' ) );
const three = JSON.parse( readFileSync( 'node_modules/three/package.json', 'utf8' ) );
console.log( '3d-tiles-renderer', pkg.version, '| three', three.version );

const entries = [
	'3d-tiles-renderer/core',
	'3d-tiles-renderer/three',
	'3d-tiles-renderer/plugins',
	'3d-tiles-renderer/three/plugins',
	'3d-tiles-renderer/core/plugins',
];
for ( const e of entries ) {

	const m = await import( e );
	console.log( e, Object.keys( m ).length );

}

// 인스턴스 두 개로 기본값과 공유 여부를 본다
const { TilesRenderer } = await import( '3d-tiles-renderer' );
const a = new TilesRenderer( 'https://example.invalid/tileset.json' );
const b = new TilesRenderer( 'https://example.invalid/other.json' );
console.log( 'errorTarget', a.errorTarget, 'maxTilesProcessed', a.maxTilesProcessed );
console.log( 'lru', a.lruCache.maxSize, a.lruCache.maxBytesSize, a.lruCache.minBytesSize );
console.log( 'shared cache', a.lruCache === b.lruCache, 'shared queue', a.downloadQueue === b.downloadQueue );
a.dispose();
b.dispose();
```

2026년 10월 22일에 실행한 출력의 핵심은 다음과 같았다.

```text
3d-tiles-renderer 0.5.3 | three 0.186.1
3d-tiles-renderer/core 31
3d-tiles-renderer/three 17
3d-tiles-renderer/plugins 58
3d-tiles-renderer/three/plugins 52
3d-tiles-renderer/core/plugins 7
errorTarget 16 maxTilesProcessed 250
lru 8000 429496729.6 322122547.2
shared cache true shared queue true
```

인스턴스를 만들 때 존재하지 않는 도메인을 썼고
`update()`를 호출하지 않았으므로 네트워크 요청은 나가지 않았다.
이 실험이 보여 주는 것은 노출된 이름과 기본값이지
렌더링의 정확성이나 성능이 아니다.

직접 해 보지 않은 것은 다음과 같다.
브라우저에서 타일셋 그리기, Google이나 Cesium ion 연동,
r3f와 Babylon.js 엔트리의 실행, 플러그인 동작,
캐시 한도에서 세분화가 멈추는 현상의 재현이다.

## 비평

### 이 도구의 약속은 코드가 아니라 사용자의 장면에 있다

README는 이 라이브러리가 3D Tiles를 “렌더링한다”고 하지만
화면에 무엇이 어떻게 보일지는 사용자의 장면, 재질, 카메라, 후처리에 달려 있다.
순회와 로딩만 가져다 쓴다는 설계의 대가는
이 모든 부분이 사용자의 몫이 된다는 것이다.
타일셋이 안 보일 때 원인이 타일 선택인지 재질인지
카메라인지 좌표계인지 가르는 일이 남는다.
`DebugTilesPlugin`이 그 일을 돕지만,
처음 쓰는 사람에게 진입 장벽이 낮다고 말하기는 어렵다.
포럼의 질문 가운데 파일은 받아지는데 장면이 비어 있다는 것이 있었던 것도
이 구조 때문이다.[^aiden-4]

### 사용량이 늘어도 유지의 구조는 좁다

공개 기록을 보면 이 프로젝트의 주요 기능은 gkjohnson의 릴리스 글로 소개된다.
2024년과 2025년에는 Cesium 생태계 지원금이 큰 기능을 뒷받침했다고
글이 적는다.[^gkjohnson-28]
PlayCanvas 지원 제안이 “엔진 팀이 그 쪽을 유지하겠다”는 조건으로 올라온 것은
새 엔진을 추가할 때의 유지 부담이 컸다는 사실을 보여 준다.
README의 Babylon.js 한계 목록도 한 엔진이 늘어날
때마다 기능 격차가 생긴다는 점을 드러낸다.
주간 다운로드가 100,000회를 넘은 시점에도
핵심 기능이 소수의 손에 달려 있다는 것은 도입을 결정할 때 위험으로 따져야 한다.
이 판단은 공개된 글에서 추론한 것이고 기여자 통계를 확인한 것은 아니다.

### 제3자 요약은 저장소보다 느리다

HysenLabs의 글은 마지막 푸시를 2026년 9월 28일이라고 적었지만
GitHub는 2026년 10월 21일의 푸시를 보여 준다.[^hysen]
같은 글은 릴리스 노트가 각 릴리스의 변경을 설명하지 않는다고 했으나
저장소 릴리스에는 변경 목록이 자세히 있다.[^hysen]
한국어 라이브러리 카탈로그는 별 2.3k와 “활동 6주 전”을 적었는데,
2026년 5월 25일 등록 시점의 값으로 읽힌다.[^seongmin]
이 카탈로그는 한국의 디지털 트윈 사내 뷰어에 가장 적합하다는 주장도 하지만,
근거가 제시되지 않았고 이 문서는 확인하지 못했다.[^seongmin]
두 글 모두 저장소의 설명을 요약한 글로 읽히므로
저장소의 현재 상태를 보려면 저장소를 직접 봐야 한다.

## 인사이트

### 이 라이브러리가 푸는 것은 렌더링보다 데이터의 길이다

3D Tiles를 쓰는 사람의 현실적인 병목은 타일을 그리는 일보다
타일셋을 어디서 얻고 어떤 형식을 맞추느냐다.
포럼의 질문 가운데 변환기와 지형 데이터 생성에 관한 것이 있었고,
저장소 관리자의 답은 JPL의 파이프라인이 공개되어
있지 않다는 것이었다.[^tjb-24][^gkjohnson-25]
최근 릴리스들이 Quantized Mesh, Terrain RGB, XYZ, WMTS, WMS, GeoJSON,
Mapbox Vector Tiles, Potree 같은 다른 데이터 형식으로 확장해 온 것도
같은 방향을 가리킨다.
이름은 “3D Tiles 렌더러”지만 실제 제품은 타일 형식의 허브에 가까워지고 있다.
이 해석은 이 문서의 추론이며, 저장소가 그렇게 선언한 것은 아니다.

### 엔진 중립 코어는 이 프로젝트의 가장 큰 자산이자 가장 큰 비용이다

코어를 엔진에 무관하게 두면 three.js, Babylon.js, 그리고 제안된 PlayCanvas로
같은 순회 로직을 재사용할 수 있다.
2026년 5월 글은 같은 기본 클래스를 공유해 두 커뮤니티의 개선이
서로에게 도움이 된다고 설명한다.[^gkjohnson-33]
반면 엔진마다 재질, 좌표계, 컬링의 제약이 다르고
Babylon.js 엔트리의 한계 목록이 그 비용을 보여 준다.
세 번째 엔진이 붙을수록 기능 격차를 관리하는 일이 핵심 과제가 된다.
이는 여러 엔진을 지원하는 라이브러리에서 흔히 나타나는 구조이고,
이 저장소에 대해서는 앞의 두 증거에서만 추론했다.

### 기본값 공유는 편해졌지만 디버깅 책임을 옮겼다

v0.5.0에서 캐시와 큐가 기본으로 공유되었다.
여러 타일셋을 한 장면에 올릴 때 메모리 중복과 다운로드 경쟁을 줄이는 선택이다.
그 대가로 캐시 한도가 인스턴스 하나의 설정이 아니라
장면 전체의 설정이 되었다.
한 타일셋의 캐시 압박이 다른 타일셋의 화질을 낮출 수 있다.
`stats.refused`가 인스턴스별로 노출되는 것이 이 변화에 맞는 진단 수단이다.
이 시나리오는 설계에서 이끌어낸 추정이고 직접 재현하지 않았다.

## 체크리스트

- 쓰려는 타일셋이 3D Tiles 1.0인지 1.1인지, 어떤 확장에 기대는지 확인했는가
- 그 확장이 “Feature Complete” 마일스톤의 열린 이슈에 걸리지 않는가
- 앱이 이미 three.js, Babylon.js, r3f 중 하나를 쓰는가
- three.js 버전이 0.167.0 이상이고, 바이트 한도를 쓰려면 r166 이상인가
- 플러그인을 `3d-tiles-renderer/plugins`에서 가져오고 있는가
- `maxBytesSize`와 `stats.refused`를 모니터링하는가
- Google 또는 Cesium ion을 쓴다면 키, 약관, 저작자 표시를 갖췄는가
- Babylon.js를 쓴다면 오른손 좌표계와 지원 한계 목록을 확인했는가
- 서브패스 엔트리만 가져와 0.x의 폐기 주기를 견딜 수 있는가
- 업그레이드 전에 릴리스 노트의 폐기와 변경 항목을 읽었는가

## 기억할 원칙

### 이 라이브러리는 엔진의 한 부품으로 쓴다

장면과 카메라를 이미 쓰는 앱에 타일 순회를 더하는 부품으로 보면 기대가 맞는다.
엔진 전체의 기능을 기대하면 직접 만들어야 할 것이 늘어난다.

### 먼저 데이터를 확인하고 나서 렌더러를 고른다

어떤 타일셋을 어디서 얻을지, 어떤 명세 기능에 기대는지를 정하는 일이
렌더러를 고르는 일보다 앞선다.
저장소의 마일스톤과 릴리스 노트는 그 판단의 가장 정확한 근거다.

---

[^npm-downloads]: npm, [3d-tiles-renderer weekly downloads](https://api.npmjs.org/downloads/point/last-week/3d-tiles-renderer), 2026-10-18

[^forum-announce]: three.js Forum, [3d-Tiles-Renderer: A 3D Tiles implementation for three.js from NASA JPL](https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136), 2022-10-29

[^cesium-blog]: Cesium, [Enhancements to the Three.js 3D Tiles Renderer](https://cesium.com/blog/2024/09/11/enhancements-to-the-threejs-3d-tiles-renderer/), 2024-09-11

[^spec-readme]: GitHub, [CesiumGS/3d-tiles: Version History](https://github.com/CesiumGS/3d-tiles)

[^hysen]: HysenLabs, [3DTilesRendererJS: 3D Tiles for three.js and Babylon.js](https://hysenlabs.com/projects/nasa-ammos-3dtilesrendererjs), 2026-09-29

[^seongmin]: CIVIL AI Korea, [3DTilesRendererJS](https://www.tryseongmin.com/library/three-tiles-renderer), 2026-05-25

[^gkjohnson-3]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/3>

[^lawrence3dpk-2]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/2>

[^aiden-4]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/4>

[^gkjohnson-6]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/6>

[^gkjohnson-7]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/7>

[^gkjohnson-8]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/8>

[^gkjohnson-9]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/9>

[^gkjohnson-11]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/11>

[^gkjohnson-17]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/17>

[^gkjohnson-23]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/23>

[^tjb-24]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/24>

[^gkjohnson-25]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/25>

[^gkjohnson-28]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/28>

[^gkjohnson-29]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/29>

[^gkjohnson-33]: <https://discourse.threejs.org/t/3d-tiles-renderer-a-3d-tiles-implementation-for-three-js-from-nasa-jpl/44136/33>
