# crashcat

> crashcat is physics engine for javascript,
> built for games, simulations, and creative websites.

<https://crashcat.dev/>

<https://github.com/isaac-mason/crashcat>

문서: <https://crashcat.dev/docs/>

## 설치

```bash
npm install crashcat
```

## 특징

- 강체(Rigid Body) 시뮬레이션
- 다양한 형상 지원:
  볼록 형상(Convex), 삼각형 메시(Triangle Mesh),
  사용자 정의 형상(Custom Shape)
- 8가지 제약 조건(Constraint):
  Hinge, Slider, Distance, Point, Fixed,
  Cone, Swing-Twist, Six-DOF
- 모터(Motor)와 스프링(Spring) 지원
- 빠른 물체를 위한
  연속 충돌 감지(Continuous Collision Detection)
- 동적 BVH 기반 브로드페이즈(Broadphase)
  공간 가속
- 강체 슬리핑(Sleeping)으로 성능 최적화
- 센서 바디(Sensor Body)로 트리거 영역 구현
- 순수 JavaScript로 작성되어 트리 쉐이킹 가능
- babylon.js, playcanvas, three.js 등과 호환

## 핵심 개념

SI 단위계 사용(미터, 킬로그램, 초).
기본 중력은 -9.81 m/s²이고 Y축이 위 방향.

### 모션 타입(Motion Type)

| 타입         | 설명                         |
|--------------|------------------------------|
| Static       | 움직이지 않는 물체           |
| Dynamic      | 물리 시뮬레이션되는 물체     |
| Kinematic    | 스크립트로 제어하는 물체     |

### 레이어 시스템

2단계 레이어 구조:

- **Broadphase Layer**:
  동적 BVH 트리로 공간을 분할
- **Object Layer**:
  어떤 물체끼리 충돌할지 필터링

## 기본 사용법

```javascript
import {
  registerAll,
  createWorldSettings,
  createWorld,
  updateWorld,
  addBroadphaseLayer,
  addObjectLayer,
  enableCollision,
  rigidBody,
  box,
} from "crashcat";

// 모든 형상과 제약 조건 등록
registerAll();

// 월드 설정
const settings = createWorldSettings();

addBroadphaseLayer(settings, { id: 0 });
addBroadphaseLayer(settings, { id: 1 });

addObjectLayer(settings, {
  id: 0,
  broadphaseLayer: 0,
});
addObjectLayer(settings, {
  id: 1,
  broadphaseLayer: 1,
});

enableCollision(settings, 0, 1);

// 월드 생성
const world = createWorld(settings);

// 바닥 (Static)
rigidBody.create(world, {
  objectLayer: 0,
  motionType: "static",
  shape: box.create({ x: 10, y: 0.5, z: 10 }),
  position: { x: 0, y: -0.5, z: 0 },
});

// 떨어지는 상자 (Dynamic)
rigidBody.create(world, {
  objectLayer: 1,
  motionType: "dynamic",
  shape: box.create({ x: 0.5, y: 0.5, z: 0.5 }),
  position: { x: 0, y: 5, z: 0 },
});

// 시뮬레이션 업데이트
const listener = {};
updateWorld(world, listener, 1 / 60);
```

## 쿼리(Query)

시뮬레이션 없이 물리 세계를 조회할 수 있다:

- 레이캐스트(Raycast)
- 형상 스윕(Shape Sweep)
- 포인트 오버랩 테스트
- 형상 오버랩 테스트
- 브로드페이즈 AABB 쿼리

## 캐릭터 컨트롤러

키네마틱(Kinematic) 캐릭터 컨트롤러 제공:

- 벽과 장애물 슬라이딩
- 계단 오르기
- 경사면 처리
- 지면 감지

## 성능 팁

- 단순한 형상 사용 (Sphere > Box > Capsule)
- 여러 물체에 형상 인스턴스 재사용
- 생성 시 슬리핑 활성화
- 무거운 시뮬레이션은 Web Worker 활용
- 삼각형 메시 등 복잡한 형상은 오프라인 생성

## Matter.js와 비교

[Matter.js](./matter-js.md)가 2D 물리 엔진인 반면,
crashcat은 3D 물리 엔진이다.
crashcat은 순수 JavaScript로 작성되어
WASM 기반 엔진 대비 번들 크기가 작고
트리 쉐이킹이 가능하다는 장점이 있다.
