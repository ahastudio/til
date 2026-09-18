# CUDA Rust: NVIDIA가 내놓은 두 갈래의 Rust GPU 커널 경로

원문: [Introducing CUDA Rust: Two Tracks for Writing GPU Kernels | NVIDIA Technical Blog](https://developer.nvidia.com/blog/introducing-cuda-rust-two-tracks-for-writing-gpu-kernels/)

HN 토론: <https://news.ycombinator.com/item?id=49724881> (926점, 385개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/mlqqpn/introducing_cuda_rust_two_tracks_for> (25점, 2개 댓글)

GN 토론: <https://news.hada.io/topic?id=33815>

## 요약

NVIDIA의 Sri Koundinyan, Melih Elibol, Jonathan Bentz가 2026년 9월 8일에 쓴 글이다.
2026년 9월에 NVIDIA가 Rust 네이티브 GPU 프로그래밍에 힘을 싣는다고 발표했으며, CUDA C++와 CUDA Python은 성숙한 기업급 툴체인이고 CUDA Rust는 2027년과 그 이후까지 키우고 성숙시킬 것이라고 밝힌다.

동기가 명확하다. AI의 시스템 계층은 추론 엔진과 서빙 인프라, 드라이버, 에이전트 런타임에 걸쳐 있고 모델과 기법이 바뀔 때마다 계속 뒤집히는데, 그 부분이 점점 Rust로 쓰이고 있다는 것이다.
NVIDIA 자신도 같은 이유로 그 이동에 참여하고 있다. Nova Linux 드라이버가 Rust로 쓰였고, NVIDIA Dynamo가 Rust 코어 위에 있으며, NVTX에 Rust 바인딩이 있다.
남은 예외가 GPU 커널이었다. Rust에서 커널을 띄울 수는 있어도 커널 자체는 다른 언어로 써야 했다는 것이다.

CUDA 자체가 가진 두 경로에 맞춰 두 갈래를 제공한다.
SIMT는 CUDA C++나 `numba-cuda`에서 이미 쓰던 모델로, 한 스레드가 무엇을 하는지 적고 수천 개를 띄운다.
Tile은 더 새로운 모델이고 C++와 Python에도 있으며, 데이터 한 타일이 무엇을 하는지 적으면 Tile IR 컴파일러가 나머지를 한다.

둘 중 무엇을 고를지에 대한 권고가 명시적이다. 먼저 Tile을 집으라는 것이다.
컴파일러가 타일이 각 아키텍처에 어떻게 매핑되는지를 정하므로 소스가 아키텍처별 선택을 담지 않게 되고, 그 통제가 필요하거나 메모리와 스레드를 직접 관리하려 할 때 SIMT로 내려간다.
그리고 언어 선택은 모델 선택과 별개 문제라고 적으며, 언어 간 상호 운용을 지원할 계획이므로 프론트엔드 선택이 다른 생태계에서 사용자를 잠그지 않을 것이라고 밝힌다.

| 항목      | `cuda-oxide` (SIMT)                              | `cutile-rs` (Tile)                         |
| --------- | ------------------------------------------------ | ------------------------------------------ |
| 방식      | 커스텀 `rustc` 코드젠 백엔드가 PTX로 직접 컴파일 | AST를 호스트 바이너리에 담고 Tile IR로 JIT |
| 툴체인    | 고정된 nightly와 자체 LLVM 필요                  | 안정 채널 Rust 1.89 이상, LLVM 불필요      |
| CUDA      | 12.x 이상                                        | 13.3                                       |
| 안전 장치 | `DisjointSlice`와 실행 계약                      | 텐서 분할과 소유권                         |
| 배포 상태 | 초기 알파                                        | crates.io에 공개됨                         |
| 실사용    | —                                                | HuggingFace의 Grout 추론 엔진, mistral.rs  |

`cuda-oxide`는 컴파일을 가로채 `#[kernel]` 함수를 Rust MIR과 커뮤니티 Pliron IR 프레임워크와 LLVM IR을 거쳐 PTX까지 내려보내고, 나머지는 표준 백엔드에 넘긴다.
Pliron 위의 GPU 방언은 NVIDIA 것이며, 방언과 모든 변환이 표준 LLVM 백엔드가 인수할 때까지 Rust 안에 머문다.

글은 같은 커널, 즉 1,024개 float에 대한 원소별 덧셈을 두 경로로 각각 완전한 프로그램으로 제시한다. 둘 다 돌고 같은 줄을 출력한다.

## SIMT 경로: cuda-oxide

요구사항이 무겁다. Linux, 컴퓨트 능력 8.0 이상 GPU, CUDA 툴킷 12.x 이상, libclang 헤더가 딸린 clang, 그리고 고정된 nightly 툴체인이다.
`cargo oxide doctor`가 선택적인 시스템 LLVM까지 포함해 전부 점검한다.

```bash
cargo +nightly-2026-04-03 install --git https://github.com/NVlabs/cuda-oxide.git cargo-oxide

cargo oxide new vecadd_demo
cd vecadd_demo
cargo oxide doctor
cargo oxide run
```

첫 `cargo oxide run`은 코드젠 백엔드를 빌드하므로 오래 걸리고, 이후 실행은 캐시를 재사용한다.

```rust
use cuda_device::{kernel, launch_bounds, launch_contract, thread, DisjointSlice};
use cuda_host::cuda_module;
use cuda_core::{CudaContext, DeviceBuffer, LaunchConfig1D};

// 이 모듈 안의 모든 것이 PTX로 컴파일된다.
// 매크로가 호스트 쪽 API(load, prepare_vecadd, 안전한 vecadd)도 함께 만든다.
#[cuda_module]
mod kernels {
    use super::*;

    #[kernel]
    #[launch_bounds(256)]                                // 블록당 최대 스레드. 컴파일러가 레지스터를 배분한다
    #[launch_contract(domain = 1, block = (256, 1, 1))]  // 1차원 인덱싱, 256스레드 블록
    pub fn vecadd(a: &[f32], b: &[f32], mut c: DisjointSlice<f32>) {
        let idx = thread::index_1d();
        let idx_raw = idx.get();                         // 입력을 읽을 때 쓰는 평범한 usize
        if let Some(c_elem) = c.get_mut(idx) {
            *c_elem = a[idx_raw] + b[idx_raw];
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let ctx = CudaContext::new(0)?;
    let stream = ctx.default_stream();
    const N: usize = 1024;

    let a_host: Vec<f32> = (0..N).map(|i| i as f32).collect();
    let b_host: Vec<f32> = (0..N).map(|i| (i * 2) as f32).collect();
    let a_dev = DeviceBuffer::from_host(&stream, &a_host)?;
    let b_dev = DeviceBuffer::from_host(&stream, &b_host)?;
    let mut c_dev = DeviceBuffer::<f32>::zeroed(&stream, N)?;

    // SAFETY: 이 패키지가 위 kernels 모듈용으로 생성된 디바이스 번들을 소유한다
    let module = unsafe { kernels::load(&ctx)? };

    // prepare가 이 설정을 위 계약과 실제 디바이스 한계에 대조해 검사한다
    let prepared = module.prepare_vecadd(LaunchConfig1D::new((N as u32).div_ceil(256), 256, 0))?;
    module.vecadd(&stream, &prepared, &a_dev, &b_dev, &mut c_dev)?;

    let c_host = c_dev.to_host_vec(&stream)?;            // 복사 후 동기화까지 한다
    let errors = (0..N)
        .filter(|&i| (c_host[i] - (a_host[i] + b_host[i])).abs() > 1e-5)
        .count();
    if errors == 0 {
        println!("PASSED: all {} elements correct", N);
    } else {
        eprintln!("FAILED: {} errors", errors);
        std::process::exit(1);
    }
    Ok(())
}
```

호스트 코드와 디바이스 코드가 한 파일에 있고, 한 명령으로 빌드되며, 별도 커널 크레이트가 필요하지 않다.

세 가지 타입 장치가 안전을 만든다.

`DisjointSlice<f32>`는 각 스레드에 자기 원소에 대한 배타적 접근만 주는 타입이다. `&mut [f32]`는 이 일에 맞지 않는 모양이기 때문이며, 모든 스레드가 같은 `&mut`를 필요로 하게 되고 Rust가 그것을 정당하게 거부한다. 이 타입이 하나의 가변 대여를 스레드별 조각으로 쪼갠다.

`thread::index_1d()`는 정수가 아니라 인덱스 타입을 반환하고 `c.get_mut(idx)`는 그 타입만 받는다. 반환은 `Option`이므로 범위를 벗어난 경우가 나중에 발견되는 메모리 오류가 아니라 지금 처리하는 분기가 된다.

실행은 신뢰되지 않고 검사된다. `#[launch_contract]`가 이 커널이 1차원으로 인덱싱하고 256스레드 블록을 쓴다고 선언하고, `prepare_vecadd`가 `LaunchConfig1D`를 그 선언과 실제 디바이스 한계에 대조해 검증한 뒤 증명을 돌려준다. 안전한 `vecadd` 메서드가 그 증명을 요구한다.
계약이 없는 커널은 원시 unsafe 실행 메서드만 노출하는데, 맨 `LaunchConfig`는 자기가 무엇을 띄우는지에 대해 아무것도 말하지 않기 때문이다.

## Tile 경로: cutile-rs

요구사항이 가볍다. 컴퓨트 능력 8.0 이상 GPU, CUDA 13.3, 안정 채널 Rust 1.89 이상, Linux이며 nightly도 자체 LLVM도 필요 없다.

```bash
cargo new vecadd_demo
cd vecadd_demo
cargo add cutile
```

```rust
use cutile::prelude::*;

// 매크로가 이 모듈의 AST를 호스트 바이너리에 담는다.
// 커널은 처음 실제로 띄워질 때 CUDA Tile IR로 JIT 컴파일된다.
#[cutile::module]
mod kernel {
    use cutile::core::*;

    #[cutile::entry()]
    fn add<const B: i32>(
        // B는 타일 폭이고 정적 차원이다. B가 다르면 다른 특화가 생긴다
        z: &mut Tensor<f32, { [B] }>, // 배타적 출력. B개 원소짜리 부분 텐서 하나
        x: &Tensor<f32, { [-1] }>,    // 공유 입력. -1은 실행 시점에 결정되는 동적 차원
        y: &Tensor<f32, { [-1] }>,
    ) {
        // 이 본문은 가변 부분 텐서마다 한 번, 단일 논리 스레드로 실행된다
        let tx = load_tile_like(x, z);  // z의 이 부분 텐서에 맞춰 떼어 온 x의 조각
        let ty = load_tile_like(y, z);
        z.store(tx + ty);               // 타일 전체에 대한 원소별 연산
    }
}

fn main() -> Result<(), Error> {
    let device = Device::new(0)?;
    let stream = device.new_stream()?;

    // 지연 연산이다. 아직 GPU를 건드리지 않았다
    let x = api::ones::<f32>(&[1024]);
    let y = api::ones::<f32>(&[1024]);

    // partition이 세 가지를 동시에 한다:
    // 타일마다 자기 128개 조각의 배타적 소유권을 주고, 그리드를 1024/128 = 8로 고정하고, B를 공급한다
    let z = api::zeros::<f32>(&[1024]).partition([128]);

    let c: Vec<f32> = kernel::add(z, x, y) // 세 텐서의 소유권을 가져간다
        .first()                           // 그리고 되돌려 주므로 출력을 골라낸다
        .unpartition()                     // 호스트 쪽 분할 래퍼를 벗긴다. 데이터는 움직이지 않는다
        .to_host_vec()                     // 복사를 기록한다
        .sync_on(&stream)?;                // 이 줄에서야 전부 실행된다

    let errors = c.iter().filter(|&&v| (v - 2.0).abs() > 1e-5).count();
    if errors == 0 {
        println!("PASSED: all {} elements correct", c.len());
    } else {
        eprintln!("FAILED: {errors} errors");
    }
    Ok(())
}
```

여기에는 `DisjointSlice`가 없다. 호스트에서의 분할은 가변 텐서에만 필요하고, 그것이 각 타일 블록에 다른 타일 블록과 겹치지 않는 쓰기 가능한 부분 텐서 하나를 넘긴다. 그 배타성이 이미 `&mut`가 보장하는 것이다.

입력 모양의 `-1`은 크기가 아니라 표지다. 그 차원은 실행 시점에 텐서에서 읽으므로, 모양이 바뀌어도 다시 컴파일하지 않는다.

`.partition([128])`이 세 가지 일을 한꺼번에 한다.
배타성을 실제로 만들고, 실행 기하를 고정하고(1,024 나누기 128은 타일 8개 그리드), `B`를 공급한다.
그리드가 따로 계산되어 커널의 인덱싱과 대조되는 대신 분할에서 따라 나오며, `B`가 호출 지점에 적히지 않는 이유는 런처가 타일 폭을 분할에서 읽기 때문이다. 그래서 `&mut` 출력은 넘기기 전에 반드시 분할되어야 한다.

호스트에서 호출하는 `add`는 위의 디바이스 함수가 아니라 매크로가 만든 런처다. 세 텐서의 소유권을 가져가고 GPU가 끝나면 튜플로 되돌려 주며, `.first()`가 거기서 출력을 골라내는 일을 한다.

`.sync_on(&stream)` 전에는 아무것도 실행되지 않는다. 그 앞의 모든 것이 제출이 아니라 기록된 지연 서술이며, `ones`와 `zeros`, 커널 호출, 호스트로의 복사까지 포함한다. 프로그램 전체가 동기화 지점이 하나인 한 줄의 연쇄다.

## 컴파일러가 잡아 주는 것

두 커널이 메모리에 대해 같은 주장을 한다. 입력은 공유이고 출력은 한 쓰기 주체의 것이라는 것이다.
차이는 그 주장을 어느 수준에서 하는지와, 그것을 하기 위해 전용 타입이 필요한지뿐이다.

이것이 중요한 이유가 서술되어 있다. 수천 개의 스레드가 보장된 순서 없이 같은 버퍼에 닿고, 둘이 같은 주소를 건드리는데 하나가 쓰기라면 순서가 결과를 정한다.
그런 버그는 부르면 재현되는 일이 드물고, 테스트를 통과한 뒤 프로덕션에서 실패한다.

SIMT 커널의 출력 버퍼를 자기 입력 중 하나로 넘기면 실제로 경쟁이 일어나든 아니든 컴파일되지 않는다.

```text
module.vecadd(&stream, &prepared, &c_dev, &b_dev, &mut c_dev)?;

error[E0502]: cannot borrow `c_dev` as mutable because it is also borrowed as immutable
```

Tile 쪽의 같은 별칭도 컴파일되지 않는다.

```text
let z = api::zeros::<f32>(&[1024]);
kernel::add(z.partition([128]), z, y)

error[E0382]: use of moved value: `z`
```

둘 다 고전적인 별칭 실수를 컴파일 타임에 잡지만 선을 다른 곳에 긋는다.
`cuda-oxide`는 각 실행 호출을 검사하고, `cutile-rs`의 소유권은 실행 경계를 넘어 텐서를 따라가는데 글은 후자가 두 주장 중 더 강한 것이라고 적는다.

Tile에는 잘못 쓸 공유 메모리나 스레드 인덱싱이 없다. 컴파일러가 둘 다 소유하기 때문이다.
타일 블록이 단일 논리 스레드이므로 경쟁할 스레드 자체가 없으며, 그것이 구성상 안전하게 만드는 것이면서 동시에 포기하는 것이다.
SIMT는 그 통제를 유지하고, 오늘 그쪽의 공유 메모리는 `unsafe`를 요구한다. 공유 메모리가 빠른 SIMT 커널의 기반이므로 그 경로를 안전하게 만드는 것이 진행 중인 작업이라고 밝힌다.

## 값 정하기

| 결정            | 선택지                              | 기준                                                                                 |
| --------------- | ----------------------------------- | ------------------------------------------------------------------------------------ |
| 프로그래밍 모델 | Tile 우선, 필요할 때 SIMT           | 아키텍처별 선택을 소스에 담지 않으려면 Tile, 공유 메모리·스레드 통제가 필요하면 SIMT |
| 툴체인 안정성   | `cutile-rs` 안정 채널               | 고정된 nightly를 CI에 넣을 수 있는지가 갈림길                                        |
| 성숙도          | `cutile-rs` 배포, `cuda-oxide` 알파 | 지금 프로덕션 후보는 사실상 하나뿐                                                   |
| 타일 폭 `B`     | 예제 기준 128                       | 분할 크기가 그리드와 특화를 동시에 정하므로 벤치마크로 잡는다                        |

가장 결정적인 값은 툴체인이다. `cuda-oxide`가 요구하는 `nightly-2026-04-03`이라는 고정 날짜가 그 경로를 실험으로 묶는다.

## 트레이드오프

### 두 경로를 동시에 내놓은 것

한쪽만 내놓는 편이 단순했을 텐데 둘을 함께 냈다. 이유가 글에 명시되어 있다. CUDA 자체가 두 경로를 가졌기 때문이며, 언어 선택과 모델 선택을 분리하겠다는 것이다.

얻는 것은 기존 CUDA 사용자에게 대응이 명확하다는 점이다. C++에서 SIMT를 쓰던 사람은 `cuda-oxide`로, Tile을 쓰던 사람은 `cutile-rs`로 가면 된다.
그리고 언어 간 상호 운용 계획이 이 구도를 떠받친다. 프론트엔드 선택이 잠금이 되지 않는다는 약속이 없으면 두 경로가 두 생태계 분열이 된다.

대가는 두 경로의 성숙도가 전혀 다르다는 것이다.
`cutile-rs`는 crates.io에 있고 HuggingFace의 Grout과 mistral.rs에서 실제로 쓰이는데, `cuda-oxide`는 초기 알파다.
그래서 지금 이 발표를 읽고 고를 수 있는 것은 사실상 Tile 하나이며, Tile을 먼저 집으라는 권고가 설계 철학인 동시에 현재 상태의 반영이기도 하다.

### `DisjointSlice`라는 전용 타입을 만든 것

`&mut [f32]`가 이 일에 맞지 않는 모양이라는 진단이 정확하다. 모든 스레드가 같은 가변 대여를 필요로 하는 구조를 Rust가 허용할 수 없기 때문이다.

전용 타입으로 푼 것이 얻는 것은 빌림 검사기를 그대로 쓸 수 있다는 점이다.
`unsafe` 블록으로 빠져나가는 대신 하나의 가변 대여를 스레드별 조각으로 쪼개는 타입을 두면, 별칭 검사가 표준 규칙으로 돌아간다.
`thread::index_1d()`가 정수가 아니라 인덱스 타입을 반환하는 것도 같은 전략이다. 타입으로 출처를 고정해 아무 정수나 넣지 못하게 한다.

대가는 배울 것이 늘고 기존 커널을 옮길 때 다시 써야 한다는 것이다.
HN에서 the__alchemist가 이 지점을 정확히 정리했다.[^the__alchemist]
`cuda-oxide`가 `cudarc`의 호스트 컴포넌트와 비슷하지만 Rust 식 커널 방언을 쓴다는 것이고, 이점은 호스트와 디바이스가 구조체를 공유할 수 있다는 것이며 단점은 표준 CUDA 커널을 새로운 진행 중 방언과 바꾸는 것이라고 했다.
그는 마지막으로 확인했을 때 Linux 전용이고 async를 요구해서 아직 써 보지 않았다고 덧붙였다.

### Tile이 안전을 구성으로 얻는 대신 포기하는 것

글이 이 절충을 스스로 적어 둔 것이 이 발표에서 가장 정직한 대목이다.
Tile에는 잘못 쓸 공유 메모리와 스레드 인덱싱이 없고, 그것이 구성상 안전하게 만드는 것이면서 동시에 포기하는 것이라는 문장이다.

그리고 왜 그것이 큰 포기인지도 밝힌다. 공유 메모리가 빠른 SIMT 커널의 기반이기 때문이다.
즉 Tile은 안전하지만 최고 성능이 필요한 커널에는 부족할 수 있고, SIMT는 그 통제를 주지만 오늘 그쪽 공유 메모리는 `unsafe`다.

그렇다면 이 발표가 실제로 제시하는 선택은 안전한 Tile과 안전하지 않은 SIMT 사이다.
Rust를 고르는 동기가 컴파일 타임 안전이었다면, SIMT 경로에서 그 동기의 핵심 부분이 아직 충족되지 않는다.
글이 그것을 진행 중인 작업이라고 적은 것은 인정이며, 그 작업이 끝날 때까지 SIMT 경로의 값은 안전보다 언어 통일에 있다.

### 지연 실행과 소유권 이동을 결합한 API

`cutile-rs`의 호스트 코드가 특이하다. 런처가 텐서 소유권을 가져가고 튜플로 되돌려 주며, `.sync_on()` 전에는 아무것도 실행되지 않는다.

이 설계가 얻는 것이 두 가지다.
소유권 이동이 실행 경계를 넘어 별칭을 막고, 그것이 앞서 본 `use of moved value` 오류의 근거다.
그리고 지연 실행이 동기화 지점을 하나로 모아 준다. 전체 프로그램이 한 연쇄가 되므로 실수로 여러 번 동기화하는 일이 줄어든다.

대가는 코드 모양이 낯설어진다는 것이다.
`.first()`로 출력을 골라내고 `.unpartition()`으로 래퍼를 벗기는 단계가 데이터 이동 없이 타입만 바꾸는 작업인데, 읽는 사람에게는 무언가 일어나는 것처럼 보인다.
그리고 지연 실행은 오류가 어디서 났는지를 흐린다. 커널 호출 줄이 아니라 `.sync_on()` 줄에서 오류가 올라오기 때문이다.

## 함정

`cuda-oxide`는 고정된 nightly(`nightly-2026-04-03`)를 요구한다. 다른 nightly 의존성과 충돌하면 해결할 방법이 없다.

첫 `cargo oxide run`이 코드젠 백엔드를 빌드하므로 오래 걸린다. CI에서 캐시 없이 돌리면 그 비용이 매번 발생한다.

두 경로가 요구하는 CUDA 버전이 다르다. `cuda-oxide`는 12.x 이상이고 `cutile-rs`는 13.3이다. 한 머신에서 둘을 다 시험하려면 그 사정을 먼저 확인해야 한다.

둘 다 Linux이고 컴퓨트 능력 8.0 이상을 요구한다. 그보다 낮은 GPU는 대상이 아니다.

SIMT 경로에서 공유 메모리는 아직 `unsafe`다. 안전을 이유로 Rust를 고른 경우 이 사실이 결정을 바꿀 수 있다.

계약이 없는 커널은 원시 unsafe 실행 메서드만 노출한다. `#[launch_contract]`를 붙이지 않으면 안전한 실행 경로가 생기지 않는다.

`cutile-rs`에서 `&mut` 출력 텐서는 분할하지 않으면 넘길 수조차 없다. 타일 폭이 분할에서 읽히기 때문이다.

`-1`은 크기가 아니라 동적 차원 표지다. 실수로 크기로 읽으면 코드의 뜻이 통째로 달라진다.

## 확인하기

두 경로를 나란히 돌려 보는 것이 이 발표를 검증하는 가장 직접적인 방법이고, 글이 그 절차를 그대로 준다.

```bash
# Tile 경로: 요구사항이 가벼우므로 여기서 시작한다
cargo new vecadd_demo && cd vecadd_demo && cargo add cutile
# 위 예제를 src/main.rs에 붙이고
cargo run
```

`PASSED: all 1024 elements correct`가 나오면 안정 채널에서 GPU 커널이 돌았다는 뜻이며, 그것이 이 발표의 가장 큰 주장이다.

그다음 별칭 검사가 실제로 동작하는지 확인한다.

```rust
// 같은 텐서를 출력과 입력으로 동시에 넘긴다
let z = api::zeros::<f32>(&[1024]);
kernel::add(z.partition([128]), z, y)   // error[E0382]: use of moved value: `z`
```

이 오류가 나는지가 컴파일 타임 안전 주장의 시험이다. 런타임 경쟁이 아니라 컴파일 실패로 잡히는지를 눈으로 봐야 한다.

`cuda-oxide`를 시험하려면 환경 점검을 먼저 돌린다.

```bash
cargo oxide doctor
```

이 명령이 통과하지 못하면 커널 코드 문제가 아니라 툴체인 문제이며, 고정 nightly와 libclang 헤더가 가장 자주 걸리는 지점이다.

## 체크리스트

- Linux이고 컴퓨트 능력 8.0 이상 GPU인가
- 안정 채널만 쓸 수 있는 환경인가. 그렇다면 `cutile-rs`만 후보다
- 필요한 CUDA 버전(`cuda-oxide` 12.x 이상, `cutile-rs` 13.3)을 확인했는가
- 공유 메모리가 필요한 커널인가. 그렇다면 SIMT 경로의 `unsafe`를 감당할 수 있는가
- SIMT 커널에 `#[launch_contract]`를 붙여 안전한 실행 경로를 만들었는가
- `cutile-rs`에서 타일 폭을 벤치마크로 정했는가, 아니면 예제 값 128을 그대로 쓰고 있는가
- 지연 실행 때문에 오류가 `.sync_on()`에서 올라온다는 점을 오류 처리에 반영했는가

## 비평

### 벤더 종속 문제에 대한 답이 계획으로만 있다

HN에서 가장 많은 답글을 받은 댓글이 이 지점을 겨눴다. jacobgorm은 CUDA를 강하게 싫어한다고 적었다.[^jacobgorm]
그 독점적 물건을 C++ 코드베이스에 한번 들이면 빼내기가 매우 어렵고, 결국 단일 벤더에 묶인 코드나 `#ifdef` 지옥, 아마도 둘 다가 된다는 것이다.
GPU를 프로그래밍하는 최선의 방법은 GPU가 CPU와 같은 기계가 아니라는 현실을 인정하고, Metal이나 OpenCL, D3D12처럼 커널을 별도 파일에 쓰고 수동으로 띄우는 것이라고 봤다.
그리고 요즘은 Triton 같은 DSL이 있어서 Rust에서 바랄 수 있는 어떤 것보다 커널 작성이 훨씬 편하다고 덧붙였다.

Lobste.rs에서 FRIGN이 같은 것을 한 줄로 말했다. 가속기 소프트웨어 API에서 NVIDIA의 준독점을 더 영속시키고 싶다면 그렇게 하라는 것이다.[^FRIGN]
landon이 반론을 달았다. Tile IR이 언어 중립적 상호 운용에 대한 거의 선의의 시도로 보이며, GPU 코드를 만드는 유일한 방법이 독점 Linux 배포에서만 도는 독점 컴파일러의 독점 C++ 확장이던 것보다는 훨씬 낫다는 것이다.[^landon]
그러면서 이것이 옳은 방향으로 보이는데 일곱 걸음이 더 필요하기는 하지만 이 한 걸음을 격려하지 말아야 할 이유가 있는지 물었다.

글이 이 비판에 대비해 준비한 답이 언어 간 상호 운용 계획이다. 그런데 그것이 계획이다.
지금 확인할 수 있는 것은 두 프로젝트가 PTX와 Tile IR로 컴파일한다는 사실이고, 둘 다 NVIDIA 하드웨어 전용이다.
amelius가 정확히 그것을 물었다. 이것이 Rust를 CUDA에 용접하는 것이냐, 이 Rust 코드를 다른 아키텍처에서 돌릴 수 있느냐는 것이다.[^amelius]
글에 그 답이 없다.

다만 jauntywundrkind가 덧붙인 사실이 균형을 준다. NVIDIA가 약 8개월 전에 CUDA Tile IR을 오픈소스로 공개했고 코드도 오픈소스라는 것이다.[^jauntywundrkind]
그렇다면 Tile 경로의 잠금 정도는 SIMT보다 낮을 수 있으며, 이 구분이 글에서 강조되지 않은 것이 아쉽다.

### GPU 문서 공개라는 더 근본적인 요구가 비껴간다

loup-vaillant가 이 발표를 인정하면서 더 원하는 것을 적었다.[^loup-vaillant]
GPU가 범용 대규모 병렬 기계에 한 걸음 더 다가가는 것은 멋진데, 더 멋진 일은 GPU 벤더가 사용자 매뉴얼을 주기 시작하는 것이라는 것이다.
그가 말한 진짜 매뉴얼은 금속 조각 하나만 있을 때 그것을 어떻게 쓰는지를 설명하는 것이며, 와이어 프로토콜의 정밀한 서술과 GPU로 보내고 받는 버퍼의 데이터 형식, 접근 가능한 코어의 ISA, 관련 성능 특성을 뜻한다.
요약하면 어떤 OS에서든 최신 수준의 드라이버를 쓸 수 있을 만큼의 정보라는 것이다.

revengerwizard도 같은 방향에서, 지금은 GPU 벤더와 하드웨어 조합 수를 생각하면 비현실적이지만 그 밑의 GPU ISA 기계어를 직접 겨냥하는 편이 훨씬 좋을 것이라고 적었다.[^revengerwizard]
x64 기계어를 겨냥하는 간단한 컴파일러를 쓸 수 있으니 자기 GPU를 겨냥하는 것도 가능해야 한다면서, 벤더 잠금이 그들에게 더 수익성이 높을 것이라고 확신한다고 덧붙였다.

이 요구가 이 발표와 어긋나는 방향이라는 점이 중요하다.
CUDA Rust는 NVIDIA의 추상을 Rust로 쓰게 해 주는 것이고, 이들이 원하는 것은 추상을 걷어내는 것이다.
그리고 이 발표가 성공할수록 앞의 요구는 덜 시급해 보이게 된다. 불편이 줄면 개방 압력도 줄기 때문이다.

### 글의 문체가 내용에 대한 신뢰를 갉아먹었다

이 스레드에서 예상하지 못한 반응이 문체에 대한 것이었고, 두 사람이 같은 문장을 지목했다.
claiir는 실행이 신뢰되지 않고 검사된다는 문장을 인용하면서 NVIDIA조차 전적으로 Claude가 쓴 글을 내놓는다고 적었다.[^claiir]
winwang은 정말 흥미롭지만 과거 NVIDIA 글과 달리 Claude처럼 읽힌다며, 기술 블로그가 청소년 소설처럼 들리기를 바라지도 원하지도 않는다고 했다.[^winwang]

글 자체에 AI 생성 요약 절이 있고 NVIDIA Nemotron으로 만들었다고 표시되어 있다는 사실이 이 반응에 근거를 준다.
그리고 그 요약이 본문보다 앞에 놓여 있어 처음 읽는 사람이 먼저 만나는 것이 생성된 텍스트다.

이것이 사소한 불만처럼 보이지만 기술 문서에서는 실질적인 문제다.
이 글이 설득해야 하는 것은 초기 알파 상태의 툴체인을 시험해 볼 만하다는 것이고, 그 설득은 저자가 실제로 그것을 써 봤다는 신뢰에 기댄다.
문체가 생성된 것처럼 읽히면 그 신뢰가 깎이며, 실제로 두 댓글 모두 내용을 부정하지 않으면서 신뢰를 유보하는 형태였다.

LarsDu88이 반대편에서 흥미로운 반응을 남겼다. 모든 것이 LLM으로 쓰이는 시대가 Rust를 배울 동기를 다소 꺾어 놓았는데, LLM이 아직 이것으로 학습되지 않았다는 사실만으로 관심이 되살아났다는 것이다.[^LarsDu88]
새로운 API가 학습 데이터에 없다는 것이 사람에게 기회로 읽히는 상태가 지금 도구 채택의 한 동기가 되었다는 뜻이며, 이 발표가 의도하지 않은 유인이다.

## 기억할 원칙

### 타입으로 출처를 고정하면 검사를 잊을 수 없게 만들 수 있다

이 발표에서 배울 만한 설계 기법이 세 개 겹쳐 있고, 셋 다 같은 형태다.

`thread::index_1d()`가 정수 대신 인덱스 타입을 반환하고 `get_mut`이 그 타입만 받는다. 그래서 아무 정수나 인덱스로 쓸 수 없다.
`prepare_vecadd`가 실행 설정을 검증한 뒤 증명을 돌려주고, 안전한 실행 메서드가 그 증명을 요구한다. 그래서 검증을 건너뛸 수 없다.
`partition`이 배타적 소유권과 그리드와 타일 폭을 한꺼번에 정한다. 그래서 그리드를 따로 계산해 커널 인덱싱과 어긋나게 만들 수 없다.

공통 구조는 검사 결과를 값으로 만들고 그 값을 다음 단계의 입력으로 요구하는 것이다.
그러면 검사를 잊는 실수가 컴파일 오류가 된다. 문서에 적어 두고 사람이 기억하게 하는 방식과 대조된다.

이 기법이 GPU 프로그래밍에만 쓰이는 것이 아니다.
설정을 검증하는 함수가 불리언을 반환하는 대신 검증된 설정 타입을 반환하게 만들고, 그 타입만 받는 실행 함수를 두면 같은 성질을 얻는다.
API 요청에서 인증된 사용자, 파싱된 경로, 검사된 권한이 모두 같은 형태로 표현될 수 있다.

주의할 점은 이 기법이 타입을 늘린다는 것이다.
`DisjointSlice`와 인덱스 타입과 준비 증명 토큰은 모두 배워야 하는 개념이고, 예제를 그대로 따라 쓰는 사람에게는 그냥 장식처럼 보인다.
그래서 이 설계를 도입할 때는 각 타입이 어떤 실수를 막는지를 한 줄로 적어 두어야 하며, 이 발표가 세 장치마다 그 한 줄을 붙여 놓은 것이 문서로서 잘한 부분이다.

---

[^the__alchemist]: <https://news.ycombinator.com/item?id=49733856>

[^jacobgorm]: <https://news.ycombinator.com/item?id=49734146>

[^FRIGN]: <https://lobste.rs/s/mlqqpn/introducing_cuda_rust_two_tracks_for#9reeps>

[^landon]: <https://lobste.rs/s/mlqqpn/introducing_cuda_rust_two_tracks_for#viwzxg>

[^amelius]: <https://news.ycombinator.com/item?id=49738446>

[^jauntywundrkind]: <https://news.ycombinator.com/item?id=49735862>

[^loup-vaillant]: <https://news.ycombinator.com/item?id=49739057>

[^revengerwizard]: <https://news.ycombinator.com/item?id=49740396>

[^claiir]: <https://news.ycombinator.com/item?id=49733918>

[^winwang]: <https://news.ycombinator.com/item?id=49735409>

[^LarsDu88]: <https://news.ycombinator.com/item?id=49734075>
