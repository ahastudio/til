# SpacetimeDB

> 데이터베이스 속도로 개발하라 (Develop at the speed of light)

<https://spacetimedb.com/>

<https://github.com/clockworklabs/SpacetimeDB>

SpacetimeDB는 데이터베이스와 게임 서버(애플리케이션 서버)를
하나로 통합한 실시간 관계형 데이터베이스 시스템이다.
Clockwork Labs가 MMORPG BitCraft Online의 백엔드로 구축하며
탄생했으며, 2025년 3월 버전 1.0, 2025년 2월에 2.0을
릴리스했다.

## 핵심 개념: "Inside-Out" 아키텍처

### 전통적인 아키텍처의 문제

```
[클라이언트] → [게임 서버] → [데이터베이스]
```

기존 멀티플레이어 게임의 백엔드는 클라이언트와 DB 사이에
게임 서버(혹은 웹 서버)가 존재한다.
이 구조는 필연적으로 3개 계층 간의 네트워크 오버헤드와
복잡한 동기화 로직을 낳는다.

### SpacetimeDB의 역전

```
[클라이언트] ↔ [SpacetimeDB = DB + 로직]
```

SpacetimeDB는 이 구조를 뒤집는다.
서버 로직을 DB 안에 직접 업로드하고,
클라이언트는 DB에 직접 연결한다.
중간에 어떤 서버도 필요 없다.

> "No more microservices, no more containers, no more
> Kubernetes, no more Docker, no more VMs, no more DevOps,
> no more infrastructure, no more ops, no more servers."
> — Clockwork Labs

## 핵심 컴포넌트

### 1. 모듈(Module) — WASM으로 컴파일된 서버 로직

모듈은 서버 로직 전체를 담은 WebAssembly(WASM) 바이너리다.
테이블 스키마, 리듀서, 뷰, 프로시저를 모두 정의하고
`spacetime publish` 한 번으로 DB에 배포된다.

```rust
// Rust 모듈 예시
#[spacetimedb::table(name = player, public)]
pub struct Player {
    #[primary_key]
    #[auto_inc]
    pub id: u64,
    pub identity: Identity,
    pub name: String,
    pub position: Vec2,
}
```

지원 언어:

- Rust (WASM 컴파일)
- C# (WASM 컴파일)
- TypeScript (V8 런타임)

내부적으로 WASM 모듈은 **Wasmtime** 런타임,
TypeScript 모듈은 **V8 런타임**에서 실행된다
(`crates/core/src/host/`).

### 2. 리듀서(Reducer) — 트랜잭셔널 RPC 엔드포인트

리듀서는 DB 상태를 변경하는 함수다.
모든 리듀서는 DB 트랜잭션 안에서 실행되므로
변경사항은 전부 커밋되거나 전부 롤백된다.

```rust
#[spacetimedb::reducer]
pub fn move_player(
    ctx: &ReducerContext,
    new_pos: Vec2,
) {
    // ctx.sender()로 호출자 신원 확인 (2.0에서 메서드로 변경)
    let identity = ctx.sender();
    if let Some(mut player) = ctx.db.player()
        .identity()
        .find(identity)
    {
        player.position = new_pos;
        ctx.db.player().identity().update(player);
    }
}
```

리듀서는 다른 리듀서를 **특정 시간이나 반복 주기**로
스케줄링할 수 있어 게임 루프, 타이머, 배치 작업에 활용된다.

### 3. 구독(Subscription) — 실시간 증분 델타 푸시

클라이언트는 SQL 쿼리를 구독하고, 해당 테이블이
변경될 때마다 자동으로 델타(변경분)를 수신한다.

SpacetimeDB 구독 시스템의 핵심 혁신:

- **트랜잭션마다 전체 쿼리를 재실행하지 않는다**
- 삽입/삭제된 행에 WHERE 절만 적용해 최소 델타 계산
- `crates/subscription/` — 증분 쿼리 평가(Incremental
  Query Evaluation) 구현
- 모듈 업데이트(핫스왑) 중에도 기존 연결/구독 유지

```csharp
// 클라이언트 (C# SDK)
conn.SubscriptionBuilder()
    .OnApplied(OnSubscriptionApplied)
    .Subscribe("SELECT * FROM player WHERE active = true");
```

### 4. 뷰(View) — Row-Level Security의 기반

2.0에서 도입된 뷰는 클라이언트 신원(Identity)으로
자동 파라미터화되는 가상 테이블이다.
행 수준 보안(RLS)의 핵심 패턴이다.

```rust
#[spacetimedb::view(name = my_player, public)]
pub fn my_player(ctx: &ViewContext) -> Option<Player> {
    ctx.db.player().identity().find(ctx.sender())
}
```

같은 뷰를 구독해도 클라이언트마다 자기 데이터만 본다.
행 필터링뿐 아니라 컬럼 필터링(커스텀 타입 반환)도 가능하다.

## 내부 아키텍처 (Rust Workspace)

```
crates/
├── core/               # 핵심 DB 엔진 (RelationalDB)
│   ├── src/db/         # 스토리지 계층
│   ├── src/host/       # WASM/V8 런타임
│   └── src/subscription/ # 구독 시스템
├── commitlog/          # WAL (커밋 로그)
├── vm/                 # 쿼리 VM (QueryExpr)
├── subscription/       # 증분 쿼리 평가
└── bindings-*/         # 언어별 SDK 바인딩
sdks/
├── rust/               # Rust 클라이언트 SDK
├── csharp/             # C# 클라이언트 SDK
└── typescript/         # TypeScript 클라이언트 SDK
```

### 스토리지 엔진

| 계층                  | 세부 내용                              |
|-----------------------|----------------------------------------|
| 실행 모델             | 모든 상태를 인메모리(In-Memory) 유지   |
| 내구성(Durability)    | WAL — 커밋 로그 (`crates/commitlog/`) |
| 복구(Recovery)        | 스냅샷 (기본값: 1,000,000 트랜잭션마다)|
| 격리(Isolation)       | MVCC (잠금 기반 데이터스토어)          |
| 트랜잭션              | ACID 보장                              |
| 클라이언트 프로토콜   | HTTP (단발성) + WebSocket (구독)       |

**인메모리 + WAL 조합**은 SpacetimeDB 성능의 핵심이다.
네트워크를 거치지 않고 메모리에서 직접 읽고 쓴 뒤,
WAL로 영속성을 보장한다.

## 신원(Identity) 시스템

SpacetimeDB의 Identity는 **장기적·전역적으로 유효한
공개 식별자**다. 연결이 끊겼다가 다시 연결해도
동일한 Identity를 유지한다.

- 클라이언트: Identity로 로그인 → Connection ID 수령
- 리듀서 내: `ctx.sender()` (2.0, 메서드 호출)로 호출자 확인
  - 1.0에서는 `ctx.sender` (필드 접근) — 호환성 주의
- 권한 검증: 리듀서 시작 시 assert로 검사, 실패 시 롤백

```rust
// 권한 패턴: 간단한 assert
#[spacetimedb::reducer]
pub fn delete_post(ctx: &ReducerContext, post_id: u64) {
    let post = ctx.db.post().id().find(post_id)
        .expect("Post not found");
    assert_eq!(
        post.author_identity,
        ctx.sender(),
        "Permission denied"
    ); // 실패 시 트랜잭션 자동 롤백
    ctx.db.post().id().delete(post_id);
}
```

## 성능 수치 (측정값)

| 지표                        | 수치                              |
|-----------------------------|-----------------------------------|
| Rust 모듈 처리량            | ~170,000 TPS                      |
| TypeScript 모듈 처리량      | ~100,000 TPS                      |
| 트랜잭션 레이턴시           | ~10μs (WebSocket 기준)            |
| 구독 평가 속도 향상 (v0.9)  | 최대 100배                        |
| 인메모리 PK 조회            | 서브 마이크로초 (서브 1μs)        |
| 기존 DB 대비 주장 성능      | 100x ~ 1,000x                     |

Convex(클라우드 함수 기반) 대비 SpacetimeDB는
HTTP 오버헤드 없이 WebSocket으로 직접 통신해
레이턴시가 ~10μs vs ~2–20ms 수준이다.

## 프로덕션 사례: BitCraft Online

BitCraft Online은 SpacetimeDB 위에서 돌아가는
대규모 오픈월드 MMORPG다.

- 백엔드 전체 = SpacetimeDB 모듈 1개
- 별도 서버, 마이크로서비스, 메시지 큐 없음
- 채팅, 아이템, 지형, 플레이어 위치 모두 DB가 처리
- 클로즈드 알파(v0.9): **700명 동시 접속** 단일 DB 인스턴스
- 배포: `spacetime publish bitcraft` 단 한 줄
- 2026년 1월: 서버 코드 오픈소스 공개

GDC에서 "Database-Oriented Design" 세션을 통해
DB + WASM이 대규모 멀티플레이어 게임을 어떻게
단순화하는지 발표했다.

## 기존 솔루션과 비교

### vs 전통적 게임 서버 스택

| 항목               | 전통 스택                        | SpacetimeDB       |
|--------------------|----------------------------------|-------------------|
| 구성 요소          | DB + 서버 + WebSocket 레이어     | 단일 시스템       |
| 배포               | Docker, K8s, CI/CD 파이프라인    | spacetime publish |
| 실시간 동기화      | 직접 구현                        | 자동 구독 푸시    |
| 트랜잭션 보장      | 별도 처리 필요                   | 기본 제공 (ACID)  |
| 스키마 접근        | ORM / 쿼리 레이어                | 직접 테이블 접근  |

### vs Firebase / Supabase

Firebase와 Supabase는 DB 위에 API 레이어를 얹은 구조로,
복잡한 비즈니스 로직은 Cloud Functions / Edge Functions에서
따로 실행해야 한다.

SpacetimeDB는 **완전한 프로그래밍 언어**(Rust, C#, TypeScript)로
모듈을 작성하고 DB 내부에서 실행한다. Cold Start 없음,
실행 시간 제한 없음, 서버리스 함수의 어색한 추상화 없음.

### vs 서버리스(Serverless)

서버리스 함수는 상태를 직접 보유하지 않아 매번 DB 왕복이
필요하다. SpacetimeDB는 상태를 인메모리에 보유하고
로직도 그 안에서 실행하므로 왕복 비용이 없다.

## 핵심 인사이트

### 1. "패러다임 역전"으로 복잡도 제거

네트워크 경계를 제거하는 것만으로 애플리케이션에서
가장 복잡한 문제들(동기화, 일관성, 레이턴시)이
자연스럽게 해결된다. 아키텍처 레벨의 결정이
코드 레벨의 복잡도를 어떻게 제거하는지 보여주는 사례다.

### 2. WASM이 안전한 서버 로직 확장 메커니즘

WASM 샌드박스는 사용자 코드와 DB 엔진을 격리한다.
덕분에 임의의 사용자 코드를 DB 내부에서 실행해도
안전하다. WASM이 단순 클라이언트 실행 환경을 넘어
서버 측 확장성의 핵심이 될 수 있음을 보여준다.

### 3. 증분 구독이 실시간 시스템의 핵심

매 트랜잭션마다 전체 쿼리를 재실행하지 않고
삽입/삭제 행에만 WHERE 절을 적용해 델타를 계산하는 방식은
실시간 시스템에서 "어떻게 O(N)을 O(변경분)으로 줄이느냐"의
실용적 답이다.

### 4. 신원 기반 Row-Level Security의 우아함

뷰가 클라이언트 신원으로 자동 파라미터화되는 패턴은
복잡한 ACL 없이도 Row-Level Security를 구현한다.
"다른 클라이언트는 다른 데이터를 본다"를
DB 설계 수준에서 해결한다.

### 5. 인메모리 + WAL: 성능과 내구성의 균형

모든 상태를 인메모리에 유지하고 WAL로 내구성을 보장하는
패턴은 Redis의 성능과 관계형 DB의 신뢰성을 동시에 취한다.
스냅샷으로 WAL 재생 시간을 제한해 복구 속도도 관리한다.

### 6. 게임에서 배운 교훈이 범용으로 확장

게임 서버의 특수 요구사항(극저지연, 대용량 동시성,
실시간 상태 동기화)을 해결한 기술이 협업 편집, IoT,
실시간 대시보드 등 범용 분야로 자연스럽게 확장된다.

## 한계와 주의사항

- **서버 사이드 쿼리 제한**: 인덱스가 정의된 컬럼으로만
  조회 가능. 서버 모듈에서 JOIN 쿼리 미지원
  (JOIN 로직을 직접 구현해야 함)
- **스케일링 모델**: 전통적인 수평 분산보다 DB 스타일
  스케일링에 가까움. 단일 인스턴스 한계가 존재함
- **스키마 마이그레이션**: WAL 기반 접근에서의
  스키마 진화 전략이 아직 성숙 중
- **인메모리 의존**: 데이터 크기가 메모리를 초과하는
  대용량 데이터셋에는 부적합

## 링크

- [공식 문서](https://spacetimedb.com/docs/)
- [GitHub — clockworklabs/SpacetimeDB](https://github.com/clockworklabs/SpacetimeDB)
- [BitCraft Public — 오픈소스 서버 코드](https://github.com/clockworklabs/BitCraftPublic)
- [GDC Vault — Database-Oriented Design](https://gdcvault.com/play/1035359/)
- [SpacetimeDB 1.0 블로그](https://spacetimedb.com/blog/introducing-spacetimedb-1-0)
- [Databases and Data-Oriented Design](https://spacetimedb.com/blog/databases-and-data-oriented-design)
- [Rust SDK Docs](https://docs.rs/spacetimedb/latest/spacetimedb/)
