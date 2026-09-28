# Go의 플랫폼 독립 SIMD: 벡터 크기를 타입에서 지운 `simd` 패키지

원문: [Platform-independent SIMD in Go - The Go Programming Language](https://go.dev/blog/simd-experiment)

HN 토론: <https://news.ycombinator.com/item?id=49843269> (406점, 147개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/sfdf3h/platform_independent_simd_go> (18점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34271>

## 소개

Go 팀의 David Chase와 Junyang Shao가 2026년 9월 24일 Go 블로그에 쓴 글이다.
Go 1.26과 1.27에는 SIMD(Single Instruction Multiple Data) 연산을 위한 실험적 API가 들어 있다.
SIMD는 `float64` 값 8쌍을 한 명령으로 더하는 것처럼 데이터 벡터 전체에 같은 연산을 아주 빠르게 하는 현대 CPU의 기능이며, 암호화에서 데이터 처리와 AI까지 계산이 많은 작업을 크게 빠르게 할 수 있다.
Go의 Green Tea 가비지 컬렉터도 살아 있는 객체를 찾아 메모리를 훑는 데 SIMD를 쓴다.

이전에는 Go에서 SIMD를 쓰려면 Go 어셈블리를 써야 했고, 그만한 가치가 있는 것은 정말 성능이 중요한 계산 커널뿐이었다.
그래서 SIMD의 덕을 볼 수 있는 많은 소프트웨어가 CPU의 상당 부분을 놀려 왔다.
Go 1.26은 amd64용 SIMD API를, Go 1.27은 arm64의 NEON과 wasm용 API를 더했고, 이 API들은 아키텍처별 `archsimd` 패키지에 있다.

Go 1.27은 여기에 더해 C++의 Highway를 느슨하게 본뜬, 플랫폼과 벡터 크기에 무관한 실험적 `simd` 패키지를 넣었다.
목표는 SIMD를 지원하는 플랫폼에서는 어셈블리에 가까운 성능을 내는 코드를 한 번만 쓰고, 아직 SIMD를 지원하지 않는 플랫폼에서는 쓸 만한 에뮬레이션을 주는 것이다.
지금은 amd64의 AVX, AVX2, AVX512, arm64의 NEON, wasm의 SIMD 명령을 지원한다.
이 저장소의 [Go 1.27](./go-1-27.md) 문서가 릴리스 노트의 한 항목으로 다룬 기능을, 설계 의도와 사용법 중심으로 정리한다.

## 동작 방식

### 왜 아키텍처별 API만으로는 부족한가

SIMD 아키텍처는 세 방향으로 다르다.
첫째는 벡터 크기다.
wasm, PowerPC, s390x는 128비트 하나이고, amd64는 128, 256, 512비트, loong64는 128과 256비트다.
riscv64는 128비트에서 65536비트 사이의 2의 거듭제곱 크기를 지원하고, arm64는 고정 크기 NEON(128비트)과 가변 크기 SVE(128~2048비트)를 모두 갖는다.
같은 아키텍처라도 기능 검사가 필요해서, amd64라면 AVX인지 AVX2인지 AVX512인지, arm64라면 NEON인지 SVE인지, SVE라면 크기와 변형이 무엇인지 알아야 한다.

둘째는 마스킹이다.
벡터에서 조건 분기는 마스크로 구현하는데, wasm, AVX, AVX2, NEON에는 마스크 레지스터가 없어 벡터 비트마스크와 불리언 연산으로 흉내 낸다.
AVX512와 RVV는 원소마다 한 비트를 쓰는 별도 마스크 레지스터가 있고, SVE는 벡터 바이트마다 한 비트를 두되 각 원소의 최하위 비트가 연산을 정한다.
AVX2는 마스크를 쓰는 로드와 스토어를 지원하지만, 평범한 벡터를 마스크로 쓰고 최상위 비트가 연산을 정한다.

셋째는 연산 자체다.
원소를 재배열하는 기본 연산은 아키텍처마다 다르고, 어떤 것은 상수 입력만 받고 어떤 것은 변수 입력도 받는다.
암호 관련 연산도 다르며, 기본 산술조차 달라서 wasm에는 64비트 정수 벡터 비교가 없다.
`archsimd`는 가능한 한 통일되게 설계됐지만, 효율을 해치지 않고 아키텍처를 비슷하게 보이게 하는 데는 한계가 있다.

### 크기 없는 벡터 타입과 교집합 연산

새 `simd` 패키지는 고정 크기 벡터를 타입 시스템에서 없애고, 모든 플랫폼의 교집합에 있는 연산만 지원하며, 교집합의 빈틈은 다른 SIMD 명령을 이용한 효율적인 에뮬레이션으로 채운다.
글은 목표를 네 가지로 적는다.
벡터 크기에 묶이지 않는 많은 데이터 처리 알고리즘에 충분할 것, 소스 코드 연산이 하드웨어와 맞으면 어셈블리만큼 효율적일 것, 그렇지 않으면 가능한 한 잘 에뮬레이션할 것, 그리고 LLM이 코드를 쓰게 되더라도, 아니 특히 그럴 때 읽고 이해하기 쉬울 것.
SIMD 명령이 없거나 `archsimd`가 지원하지 않는 플랫폼에서는 모든 연산이 에뮬레이션되므로 `simd` 코드는 항상 돌아간다.

벡터 타입은 기본 타입 이름을 대문자로 쓰고 복수형으로 만든 것으로, `simd.Uint8s`나 `simd.Float32s` 같은 식이다.
비교 연산은 원소 너비에 맞는 마스크 값을 내서, `Int8s`의 비교는 `Mask8s`를 낸다.

### 컴파일러가 함수를 크기별로 복제한다

디버깅하거나 스택 트레이스를 보면 이상한 타입과 메서드가 보이는데, `simd`가 패키지이자 내부 구현 패키지이자 컴파일러 프런트엔드의 AST 재작성이기 때문이다.
AST 재작성은 `simd` 타입을 언급하는 함수, 변수, 타입의 특화된 복사본을 여러 개 만들고, `simd` 타입을 `simd/internal/bridge`의 크기별 타입으로 바꾼다.
각 bridge 타입은 메서드를 제한한 `archsimd` 타입이다.
특화된 복사본에는 `@simdNNN` 접미사가 붙는데, `NNN`은 벡터 길이 128, 256, 512이거나 에뮬레이션을 뜻하는 0이다.

시그니처에는 `simd`가 없고 내부에서만 쓰는 함수는 프로그램 시작 때 감지한 SIMD 수준에 따라 알맞은 특화 버전을 부르는 래퍼로 바뀐다.
특화된 함수끼리는 디스패치 비용 없이 직접, 경우에 따라 인라인으로 서로를 부른다.
이 전략은 코드 중복과 SIMD 성능 사이의 절충으로, 디스패치 비용을 SIMD 계산 안이 아니라 필요한 만큼 위로 끌어올리되 그 이상은 올리지 않는다.
HN의 vlovich123이 같은 바이너리가 알 수 없는 CPU에서 돌 수도 있는데 어떻게 타입 스위치를 최적화로 없앨 수 있느냐고 묻자,[^vlovich123] Scaevolus는 SIMD를 언급하는 함수의 여러 버전을 만들고 디스패치 비용을 호출자로 올린다고 정리한다.[^Scaevolus]

## 사용하기

### 활성화와 기본 루프

빌드할 때 `GOEXPERIMENT=simd`를 설정하면 된다.
벡터는 슬라이스에서 불러오고 슬라이스로 저장한다.
다음은 글에 실린 내적 예제로, 벡터 길이 `a.Len()`을 코드에 고정하지 않는다는 점이 핵심이다.

```go
// innerProduct는 x와 y의 내적을 돌려준다.
func innerProduct(x, y []float32) float32 {
    var a simd.Float32s
    var i int
    // 한 번에 벡터 길이만큼 처리한다. 길이는 실행 시 하드웨어가 정한다.
    for i = 0; i < len(x)-a.Len()+1; i += a.Len() {
        u := simd.LoadFloat32s(x[i : i+a.Len()])
        v := simd.LoadFloat32s(y[i : i+a.Len()])
        a = u.MulAdd(v, a)
    }
    // 벡터 길이로 나누어떨어지지 않는 꼬리는 Part 로드로 처리한다.
    if i < len(x) {
        u, _ := simd.LoadFloat32sPart(x[i:])
        v, _ := simd.LoadFloat32sPart(y[i:])
        a = u.MulAdd(v, a)
    }
    return sum(a)
}

// sum은 x 원소들의 스칼라 합을 돌려준다.
func sum(x simd.Float32s) float32 {
    s := make([]float32, x.Len())
    x.Store(s)
    var r float32
    for _, e := range s {
        r += e
    }
    return r
}
```

`sum`을 따로 쓴 것은 첫 실험 릴리스의 한계 때문이다.
벡터의 모든 원소를 더하는 공통 방법이 없어 Go 1.27의 `simd`는 이를 지원하지 않고, 다음 릴리스에 `ReduceSum`이 들어오면 `simd.ReduceSum`으로 바꿀 수 있다.

### 지원하는 연산의 범위

Go 1.27 기준으로 로드와 브로드캐스트(`LoadV`, `LoadVPart`, `BroadcastV`), 저장(`Store`, `StorePart`), 그리고 `Add`, `Sub`, `IfElse`, `Masked`, `Equal`, `NotEqual` 같은 연산은 열 가지 원소 타입 모두에서 쓸 수 있다.
나머지는 타입마다 다르다.
`MulAdd`, `Div`, `Sqrt`는 부동소수점 타입에만 있고, `And`, `Or`, `Xor`, `Not`은 정수 타입에만, 시프트와 회전은 그중 일부 정수 타입에만 있으며, `AddSaturated`와 `SubSaturated`는 8비트와 16비트 정수에만 있다.
`CarrylessMultiplyEven`과 `CarrylessMultiplyOdd`는 한 정수 타입에만 있고, 비트 수를 바꾸지 않는 `ReshapeToUint8s` 같은 재해석 연산은 비용이 없다.
어떤 연산이 어떤 타입에 있는지는 글의 표를 직접 확인해야 한다.

### 부족한 연산은 아키텍처별 코드로 내려가 채운다

`simd`가 애플리케이션의 모든 부분에 충분하지 않거나 필요한 기능의 에뮬레이션이 아직 없으면, 아키텍처별 SIMD로 넘어갔다 돌아올 수 있다.
각 벡터 타입의 `ToArch()`는 `any`를 돌려주고, 이것을 플랫폼별 타입으로 타입 단언한 뒤, `simd.<타입>FromArch` 함수로 되돌린다.
이식 가능한 코드에서는 이것이 각 플랫폼마다, 에뮬레이션까지 포함해 아키텍처별 코드를 써야 하는 의무가 된다.

글의 예는 Go 1.27에 없는 `Int8s.OnesCount()`다.
amd64에서는 AVX와 AVX2에 해당 명령이 없고 AVX512에는 있으므로, 128비트와 256비트에서는 4비트 단위 조회 테이블로 계산하고, 512비트에서는 하드웨어 명령을 쓴다.

```go
//go:build goexperiment.simd && amd64
package simd_test

import (
    "simd"
    "simd/archsimd"
)

var popcnt4x16 = [16]int8{0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4}

// OnesCount는 원소마다 1인 비트의 수를 돌려준다.
func OnesCount(v simd.Int8s) simd.Int8s {
    switch x := v.ToArch().(type) {
    case archsimd.Int8x16:
        // 하위 4비트와 상위 4비트를 각각 조회 테이블로 세어 더한다.
        lut := archsimd.LoadInt8x16Array(&popcnt4x16)
        mask0f := archsimd.BroadcastInt8x16(0x0f)
        lo := x.And(mask0f)
        hi := x.ToBits().ReshapeToUint16s().ShiftAllRight(4).
                ReshapeToUint8s().BitsToInt8().And(mask0f)
        return simd.Int8sFromArch(lut.PermuteOrZero(lo).
                Add(lut.PermuteOrZero(hi)))
    // Int8x32는 같은 방식을 PermuteOrZeroGrouped로 한다(생략).
    case archsimd.Int8x64:
        // AVX512에는 전용 명령이 있다.
        return simd.Int8sFromArch(x.OnesCount())
    default:
        // GODEBUG=simd=0일 때의 에뮬레이션
        return OnesCountEmulated(v)
    }
}
```

인터페이스 변환과 타입 스위치는 비효율적으로 보이지만, 컴파일러 쪽 `simd` 구현이 코드를 특화하면서 타입 스위치를 없앤다.
NEON과 wasm은 이 연산을 지원하므로 `case archsimd.Int8x16` 하나로 끝나고, SIMD가 없는 플랫폼용 파일은 에뮬레이션 함수만 부른다.
에뮬레이션 함수는 벡터를 `uint64` 두 개로 저장해 비트 트릭으로 세고 다시 불러온다.
글은 NEON과 wasm 파일에 SVE가 추가되면 이 코드가 동작하지 않을 것이라는 `TODO`를 남겨 두는데, 아키텍처별로 내려간 코드는 새 벡터 크기가 생길 때마다 다시 손봐야 한다는 뜻이다.

### `GODEBUG`로 하드웨어 구성을 바꿔 가며 시험한다

하드웨어 지원이 있는 플랫폼에서는 실행 전에 `GODEBUG` 환경 변수로 동작을 바꿔, 여러 하드웨어 구성에서 `simd` 코드를 시험할 수 있다.

| 설정              | 뜻                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| `simd=0`          | 하드웨어가 지원해도 에뮬레이션을 쓴다                                                                  |
| `simd=128`        | 128비트 벡터와 그 기능을 쓰고, 기능이 없으면 즉시 panic한다                                            |
| `simd=256`, `512` | 가능하면 256비트나 512비트 벡터와 그 기능을 쓴다                                                       |
| `simd=+128`       | 일부 기능이 없어도 128비트를 쓰고, 없는 명령을 실제로 쓸 때만 panic한다(예: PMULL이 없는 Raspberry Pi) |
| `simd=+256`       | 같은 방식의 256비트(예: AVX2는 있지만 VPCLMULQDQ가 없는 Apple Silicon의 amd64 에뮬레이션)              |
| `simd=+512`       | 일부 기능이 없어도 512비트를 쓴다                                                                      |

## 트레이드오프

### 교집합은 이식성을 얻는 대신 연산을 잃는다

모든 플랫폼에서 돌아야 한다는 제약은, 1년 안에 `archsimd`에 들어올 것으로 예상되는 riscv64, ppc64, s390x, loong64까지 포함해, `simd`에 어떤 메서드를 넣을지 보수적으로 만든다.
로드, 스토어, 산술, 비교(모든 비교는 아니다)처럼 어디에나 있는 연산은 쉽게 들어가지만, 단순 교집합에는 구멍이 많다.
그래서 `archsimd` 쪽에 에뮬레이션을 더해 구멍을 채운다.

에뮬레이션에는 가벼운 것과 무거운 것이 있다.
원소마다 다른 시프트 거리를 쓸 수 없는 아키텍처에서 같은 거리 시프트를 벡터 시프트로 흉내 내거나, 부호 없는 비교를 부호 있는 비교와 상수 XOR 두 번으로 만드는 것은 명령 2~3개면 된다.
반면 암호와 CRC에 중요한 캐리 없는 곱셈은 지원하지 않는 곳이 있어 제대로 에뮬레이션해야 하고, 암호에 쓰이므로 입력에 따라 실행 시간이 달라지지 않게 만들었다.
결국 교집합 설계의 비용은 코드를 쓸 때가 아니라 실행할 때 나타난다.
같은 코드가 어떤 플랫폼에서는 명령 하나로, 다른 플랫폼에서는 수십 개로 번역되며, 이 차이는 소스에서 보이지 않는다.

HN의 ghusbands는 교집합이라면 정의상 빈틈이 없어야 하니 글의 설명이 모순이라고 지적한다.[^ghusbands]
글의 표현은 느슨하지만 실제 설계는 “모든 곳에서 효율적으로 제공할 수 있는 연산의 집합”이며, 그 집합은 하드웨어 교집합보다 넓고 합집합보다 좁다.
cryptolobster가 SVE와 기능 변형이 들어오기 전까지 에뮬레이션이 핫 패스에 얼마나 들어갈지 궁금해한 것도 이 차이를 겨냥한다.[^cryptolobster]

### 이식 가능한 SIMD는 약간 느리다

ImJasonH는 이미지의 색을 바꾸는 wasm 예제를 브라우저에서 돌려 세 방식을 비교했다.[^ImJasonH]
이식 가능한 SIMD는 아키텍처 전용 SIMD보다 약 11% 느렸고, 둘 다 SIMD를 쓰지 않을 때보다 약 5배 빨랐다.
karolist도 이미지 잘라내기의 전경 추정에 써서 SIMD 없는 버전보다 약 30% 빨라졌다고 말한다.[^karolist]

11%는 작은 수치가 아니지만, 이 비교가 보여 주는 핵심은 두 번째 수치다.
지금까지 Go 개발자의 실제 선택지는 이식 가능한 SIMD와 전용 SIMD 사이가 아니라, 어셈블리를 쓰느냐 SIMD를 포기하느냐였다.
melodyogonna가 말하듯, 성능 손해가 조금 있더라도 이식 가능한 SIMD는 벡터 연산이 필요한 곳에서 스칼라 계산을 이기며, 언어들이 하드웨어별 API만 제공해 온 탓에 SIMD는 성능이 절대적으로 중요한 특수한 경우에만 쓰였다.[^melodyogonna-portable]

### 함수 복제는 디스패치를 없애는 대신 바이너리를 키운다

크기별로 함수를 복제하는 전략은 SIMD 계산 안의 디스패치 비용을 없앤다.
keel_dev는 그 대가를 묻는다.[^keel_dev]
SIMD 타입을 언급하는 모든 함수의 특화 복사본이 N개 만들어지면, 바이너리 크기가 SIMD를 건드리는 함수 수에 비례해 커지지 않느냐는 것이다.
많은 호출 지점에서 쓰이는 제네릭 도우미 함수라면 코드 크기가 눈에 띄게 늘 수 있고, 두 특화 복사본이 같을 때 중복을 없애는지, 실제 코드베이스에서 측정한 사람이 있는지 그는 묻는다.

글은 이 질문에 답하지 않는다.
글이 말하는 절충은 디스패치를 계산 안에서는 없애되 필요 이상으로 올리지 않는다는 것이며, 반대로 디스패치가 너무 아래에 있으면 `simd` 타입을 괜히 언급해 위로 올리라고 권한다.
그렇게 올릴수록 복제되는 함수는 늘어나므로, 성능과 바이너리 크기의 균형은 결국 사용자가 `simd` 타입을 어디서 언급하느냐로 정해진다.

### 가변 길이 벡터는 설계에서 이미 자리를 받았다

mshockwave는 최근 본 여러 이식 가능한 SIMD 구현 가운데, Fearless SIMD까지 포함해 SVE와 RISC-V 벡터처럼 크기가 고정되지 않은 벡터를 지원하기 쉽게 만든 것은 이것이 처음이라고 말한다.[^mshockwave]
Highway를 만든 janwas는 자신들이 Highway에서 이 방식을 먼저 개척했고 API에 대해 조언도 했다고 답한다.[^janwas]
melodyogonna가 가장 제약이 큰 플랫폼의 최대 벡터 크기에 맞춰야 하지 않느냐고 묻자,[^melodyogonna] mshockwave는 벡터 크기에 동적 인수를 넣고 모든 것을 그 인수를 중심으로 설계하면 된다며, LLVM IR이 SVE와 RVV에 쓰는 `vscale`이 바로 그 방식이라고 설명한다.[^mshockwave-vscale]

이것이 `simd`가 벡터 크기를 타입에서 지운 진짜 이유다.
타입에 128이나 256을 적은 코드는 SVE와 RVV가 오면 다시 써야 하지만, 크기를 모르는 코드는 새 크기가 와도 그대로 돈다.
Go 1.28에서 `archsimd`에 SVE를 넣고 `simd`에도 넣기를 바란다는 계획이 가능한 것도, 사용자 코드가 처음부터 `Len()`을 실행 시에 물어보도록 짜여 있기 때문이다.

## 함정

벡터 길이를 상수로 가정하지 않는다.
루프는 `a.Len()`만큼 나아가고, 나누어떨어지지 않는 꼬리는 `LoadFloat32sPart`처럼 `Part` 함수로 처리해야 한다.
128비트 기계에서 짠 코드가 512비트 기계에서 꼬리를 잘못 처리하는 식의 버그는, 개발 기계에서만 시험하면 드러나지 않는다.

`ToArch()`로 내려간 코드는 이식성을 스스로 책임진다.
타입 스위치에 없는 아키텍처나 벡터 크기가 오면 `default`로 떨어지므로, 모든 파일에 에뮬레이션 경로가 있어야 하고, 새 크기가 추가될 때마다 다시 확인해야 한다.
글의 예제에 남은 SVE 관련 `TODO`가 그 예다.

`simd` 타입을 시그니처에 넣지 않은 함수는 래퍼가 된다.
그런 함수를 뜨거운 루프 안에서 부르면 매번 디스패치가 일어날 수 있으므로, 글의 벤치마크 예처럼 바깥 함수에서 `var _ simd.Uint64s`로 `simd` 타입을 언급해 디스패치를 위로 올려야 한다.

마지막으로 API는 아직 실험 단계라 바뀔 수 있다.
`ReduceSum`, `OnesCount`, 마스크 연산, 셔플 연산은 다음 릴리스들에 들어올 예정이고, 지금 직접 구현한 우회 코드는 그때 표준 연산으로 바꿔야 한다.

## 확인하기

같은 기계에서 여러 하드웨어 구성을 흉내 내려면 `GODEBUG`를 바꿔 가며 테스트와 벤치마크를 돌리면 된다.

```bash
# 에뮬레이션 경로가 맞는 결과를 내는지 확인한다
GOEXPERIMENT=simd GODEBUG=simd=0 go test ./...

# 128비트와 256비트 경로를 각각 시험하고 성능을 비교한다
GOEXPERIMENT=simd GODEBUG=simd=128 go test -bench=. ./...
GOEXPERIMENT=simd GODEBUG=simd=256 go test -bench=. ./...
```

`simd=0`의 결과와 하드웨어 경로의 결과가 같은지 비교하면, 벡터 길이에 따른 꼬리 처리 버그와 아키텍처별 코드의 누락을 한 기계에서 잡을 수 있다.
`+128`이나 `+256`은 일부 명령이 없는 기계, 예를 들어 Raspberry Pi나 Apple Silicon의 amd64 에뮬레이션에서 코드가 그 명령을 실제로 쓰는지 확인하는 데 쓴다.

## 비평

### 자동 벡터화라는 더 넓은 빈틈은 여전히 남아 있다

physicsguy는 C나 C++ 코드를 링크해야 적절한 성능이 나오던 Go의 오랜 불만이 풀렸다고 반기면서도, 대개는 자동 벡터화로 충분한데 이 기능은 그 빈틈을 다루지 않는다고 말한다.[^physicsguy]
`simd` 패키지는 사람이, 또는 글이 말하듯 LLM이 벡터 코드를 직접 쓰는 것을 쉽게 만들지만, 평범한 루프를 컴파일러가 알아서 벡터화해 주지는 않는다.

typical182에 따르면 Go 컴파일러의 자동 벡터화 작업이 외부 기여자에 의해 진행 중이며, 복잡도나 컴파일 속도를 크게 해치지 않고 좋은 결과를 보이고 있다.[^typical182]
tgv는 첫 단계로 알맞은 숫자 루프를 SIMD로 바꿔 주는 린터 규칙을 만들 수도 있다고 제안한다.[^tgv]
대부분의 Go 코드는 벡터 코드를 직접 쓸 사람이 쓰지 않으므로, 생태계 전체의 성능에는 명시적 SIMD보다 자동 벡터화가 더 큰 영향을 줄 것이다.
글은 명시적 API의 설계를 자세히 설명하지만, 그것이 자동 벡터화와 어떻게 나뉘어 쓰일지는 말하지 않는다.

## 기억할 원칙

### 이식성은 타입에서 크기를 지울 때 생긴다

`simd` 패키지의 설계에서 옮겨 갈 만한 원칙은, 이식성을 추상화 계층이 아니라 타입의 모양으로 얻는다는 점이다.
벡터 크기를 타입에 적으면 코드는 그 크기에 묶이고, 새 하드웨어가 올 때마다 새 코드가 필요하다.
크기를 타입에서 지우고 실행 시에 묻게 하면, 코드는 아직 존재하지 않는 하드웨어에서도 돈다.

이 원칙은 SIMD 밖에서도 통한다.
어떤 값이 플랫폼마다 달라질 수 있다면, 그 값을 코드에 상수로 두기보다 실행 시에 물어보게 설계하는 편이 오래간다.
대가는 일부 최적화 기회를 잃는 것인데, `simd`는 그 대가를 컴파일러의 함수 복제로 되찾으려 한다.
사용자는 크기를 모르는 코드를 쓰고, 크기를 아는 코드는 컴파일러가 만든다는 역할 분담이 이 설계의 핵심이다.

---

[^vlovich123]: <https://news.ycombinator.com/item?id=49845045>

[^Scaevolus]: <https://news.ycombinator.com/item?id=49845159>

[^ghusbands]: <https://news.ycombinator.com/item?id=49847117>

[^cryptolobster]: <https://news.ycombinator.com/item?id=49849283>

[^ImJasonH]: <https://news.ycombinator.com/item?id=49845681>

[^karolist]: <https://news.ycombinator.com/item?id=49844358>

[^melodyogonna-portable]: <https://news.ycombinator.com/item?id=49848076>

[^keel_dev]: <https://news.ycombinator.com/item?id=49846660>

[^mshockwave]: <https://news.ycombinator.com/item?id=49847070>

[^janwas]: <https://news.ycombinator.com/item?id=49847715>

[^melodyogonna]: <https://news.ycombinator.com/item?id=49847917>

[^mshockwave-vscale]: <https://news.ycombinator.com/item?id=49849830>

[^physicsguy]: <https://news.ycombinator.com/item?id=49843775>

[^typical182]: <https://news.ycombinator.com/item?id=49844114>

[^tgv]: <https://news.ycombinator.com/item?id=49843868>
