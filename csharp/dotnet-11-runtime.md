# .NET 11 런타임: 최소 하드웨어 상향과 Runtime Async 프리뷰, JIT 개선 정리

원문: [What's new in the .NET runtime for .NET 11](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-11/runtime)

HN 토론: <https://news.ycombinator.com/item?id=50439284> (254점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=36957>

## 소개

Microsoft Learn의 이 문서는 .NET 11 런타임에 들어온 변화를 항목별로 나열한
릴리스 노트다.
문서 하단의 갱신일은 2026년 11월 10일이다.
주장을 펼치는 글이 아니라 무엇이 바뀌었고 어떻게 켜거나 끄는지를 적은 참고
자료이므로, 이 노트는 영향이 큰 변경을 골라 판단 기준을 붙이는 방식으로
정리한다.
문서의 성능 수치(“최대 20배”, “최대 200배” 등)는 모두 Microsoft가 문서에서 밝힌
값이며, 이 노트가 직접 측정한 것이 아니다.

## 최소 하드웨어가 올라갔다

.NET 11은 x86/x64와 Arm64 모두에서 최소 명령어 집합을 올렸다.
오래된 하드웨어에서는 실행 자체가 실패하고, “The current CPU is missing one or
more of the baseline instruction sets.”와 비슷한 메시지가 출력될 수 있다고
문서는 적는다.
이유로는 오래된 하드웨어 지원이 코드베이스를 복잡하게 하고, AOT 대상이 따라야
하는 “최저 공통 분모”가 성능을 깎을 수 있다는 점을 든다.

### x86/x64

세 운영체제(Apple, Linux, Windows) 모두 기준선이 x86-64-v1에서 x86-64-v2로
올라간다.
v1이 보장하던 CMOV, CX8, SSE, SSE2에 CX16, POPCNT, SSE3, SSSE3, SSE4.1, SSE4.2가
더해진다.
문서는 이 보장이 Windows 11과 Windows 10이 공식 지원하는 모든 x86/x64 CPU에서
이미 요구되며, 지원 종료되지 않은 Intel과 AMD 칩을 모두 포함한다고 설명한다.
마지막으로 빠진 옛 칩은 2013년 무렵 지원이 끝났다고 한다.

| 운영체제 | 이전 JIT/AOT 최소 | 새 JIT/AOT 최소 | 이전 R2R 대상 | 새 R2R 대상 |
| -------- | ----------------- | --------------- | ------------- | ----------- |
| Apple    | x86-64-v1         | x86-64-v2       | x86-64-v2     | 변경 없음   |
| Linux    | x86-64-v1         | x86-64-v2       | x86-64-v2     | x86-64-v3   |
| Windows  | x86-64-v1         | x86-64-v2       | x86-64-v2     | x86-64-v3   |

x86-64-v3은 AVX, AVX2, BMI1, BMI2, F16C, FMA, LZCNT, MOVBE를 더한다.

### Arm64

| 운영체제 | 이전 JIT/AOT 최소 | 새 JIT/AOT 최소 | 이전 R2R 대상 | 새 R2R 대상      |
| -------- | ----------------- | --------------- | ------------- | ---------------- |
| Apple    | Apple M1          | 변경 없음       | Apple M1      | 변경 없음        |
| Linux    | armv8.0-a         | 변경 없음       | armv8.0-a     | armv8.0-a + LSE  |
| Windows  | armv8.0-a         | armv8.0-a + LSE | armv8.0-a     | armv8.2-a + RCPC |

Linux는 Raspberry Pi처럼 AdvSimd만 지원하는 장치도 계속 지원한다.
다만 R2R 대상이 LSE를 포함하게 되어, 그런 장치에서는 앱을 시작할 때 JIT 비용이
더 들 수 있다.
Windows는 LSE를 요구하며, 이는 Windows 11과 Windows 10이 공식 지원하는 모든
Arm64 CPU, 그리고 Arm SBSA 요구 사항과 맞는다고 한다.

### 이 변경에서 구분할 것

최소 요구(JIT/AOT)와 R2R 대상은 다른 이야기다.
최소 요구를 못 채우면 실행이 막히고, R2R 대상을 못 채우면 실행은 되지만 미리
컴파일된 코드를 쓰지 못해 시작이 느려진다.
Linux x64 이미지가 v3, Windows Arm64가 armv8.2-a + RCPC를 R2R 대상으로 삼으므로,
구형 서버나 저가 가상 머신에서 같은 앱이 느려질 수 있다.

## Runtime Async는 아직 프리뷰다

.NET 11은 컴파일러가 만들던 async 상태 머신을 런타임이 직접 관리하는 Runtime
Async(V2)를 도입한다.
문서는 이를 프리뷰 기능이라고 분명히 적는다.

```xml
<PropertyGroup>
  <Features>runtime-async=on</Features>
</PropertyGroup>
```

net11.0 프로젝트는 이를 쓰려고
`<EnablePreviewFeatures>true</EnablePreviewFeatures>`를 넣지 않아도 된다.
.NET 런타임 라이브러리 자체는 `runtime-async=on`으로 컴파일되어, 상태 머신
클래스 없이 런타임 async에만 의존한다.
Microsoft는 처리량이나 라이브러리 크기 변화를 보면 긍정이든 부정이든 알려 달라고
요청한다.
이전에 동작을 제어하던 `DOTNET_RuntimeAsync`와 `UNSUPPORTED_RuntimeAsync` 환경
변수는 제거되었다.
프로젝트 단위로 끄려면 `<UseRuntimeAsync>false</UseRuntimeAsync>`를 쓴다.

### 눈에 보이는 변화는 실행 중 스택 트레이스다

문서의 예제에서 중첩된 async 메서드 3개를 호출하면, 켜지 않았을 때는 프레임이
13개이고 `AsyncMethodBuilderCore.Start` 같은 상태 머신 프레임이 섞인다.
켜면 `InnerAsync`, `MiddleAsync`, `OuterAsync`, `Main`의 실제 호출 사슬만 5개
프레임으로 보인다.
이 개선은 프로파일러, 진단 로그, 디버거의 호출 스택 창처럼 실행 중인 스택을
들여다보는 모든 도구에 적용된다.
반면 `catch (Exception ex)`로 얻는 예외 스택 트레이스는 기존 정리 로직 때문에
켜든 끄든 같다고 문서가 적는다.
따라서 예외 로그만 보는 팀은 이 변화를 체감하기 어렵다.
HN의 tikotus는 취소가 예외로 이루어지는데 깊은 스택의 트레이스 문자열 생성에서
끊김이 생긴다며 더 단순한 스택 트레이스에 기대를 걸었다.[^tikotus]
이에 electroly는 예외 스택 트레이스는 이미 async 기반 프레임을 숨기고 있어서
이 변화의 이득은 주로 디버거의 실행 중 호출 스택이라고 바로잡았다.[^electroly]
같은 스레드에서 gdwatson은 코루틴이 여전히 스택을 쓰지 않는 방식이되, 양보가
컴파일러가 지우는 동작이 아니라 런타임이 아는 동작이 된 것으로 이해했다.[^gdwatson]
bjoli는 켜 본 경험으로 성능이 꽤 좋아졌고 할당이 많이 줄었다고 썼다.[^bjoli]
이 증언은 한 사용자의 것이어서 어떤 코드에서 어느 정도인지는 알 수 없다.

### 성능 쪽 변경

- NativeAOT와 ReadyToRun에서도 동작하고, 연속(continuation) 객체를 더 적극적으로
  재사용하며 바뀌지 않은 지역 변수 저장을 피한다.
- 동기 경로(await 없는 async 호출)의 인라이닝이 crossgen2에서 확인되었다.
- JIT가 Task를 반환하는 동기 메서드의 전용 runtime-async 버전을 컴파일하고, 중단
  지점을 tail-merge하며, 연속을 캐시한다.
- 계층형 컴파일이 async 버전에도 적용되어 뜨거운 메서드는 tier 1 최적화를
  받는다.
- `Task.FromResult`, `Task.CompletedTask`, `ValueTask.FromResult`를 JIT가
  알아본다.
- 암시적 tail call이 다시 켜지고 `await Task.Yield()`의 할당이 줄었다.
- 연속이 복원할 `ExecutionContext` 상태가 없으면 캡처와 복원을 건너뛴다.
`ConfigureAwait(false)`를 쓰고 `AsyncLocal<T>`를 드물게 쓰는 앱에서 오버헤드가
  줄어든다고 한다.
이 마지막 항목은 Runtime Async를 켜지 않아도 Task와 ValueTask에 적용된다.
- `Task`에서 `Task<T>`로 공변 반환하는 오버라이드가 가상 호출에서 동작하도록
  런타임이 void 반환 thunk를 만든다.
- 디버거는 중단점이 runtime-async 메서드 안에서 제대로 걸리고, await 경계를 넘어
  컴파일러가 만든 코드로 들어가지 않고 단계 실행한다.

## JIT와 코드 생성

문서가 나열한 JIT 개선은 많지만, 앱 코드가 어떤 모양일 때 득을 보는지로 묶으면
다음과 같다.

| 묶음           | 변경                                                                                                               | 득을 보는 코드                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| 경계 검사      | `i + 상수 < 길이` 비교, `values[^1]`, `!span.IsEmpty && span[0]` 뒤의 검사 제거                                    | 배열과 span을 도는 반복문                          |
| 분기 접기      | 같은 상수를 내는 select 접기, 작은 상수 집합의 switch 식 접기, 이미 함의된 바깥 조건 제거                          | 인라이닝 뒤 여러 메서드의 가드가 한 본문에 모일 때 |
| 상수 접기      | 두 피연산자가 모두 컴파일 시점 상수인 `string.Equals`와 `SequenceEqual`, 불필요한 checked 문맥                     | `"Guest" == "Admin"`처럼 인라인된 리터럴 비교      |
| 가상 호출 제거 | 제네릭 가상 메서드, 제네릭 인터페이스의 기본 인터페이스 메서드, `Activator.CreateInstance<T>()` 결과의 정확한 타입 | 인터페이스 호출이 많은 코드                        |
| 하드웨어       | `Half` 연산의 FP16 명령, AVX 위의 `Vector128.Dot`, `Math.BigMul`의 단일 `MUL`, `uint`에서 float/double 변환        | 수치 연산, 이미지와 오디오 처리                    |

SIMD 쪽에서는 `CreateGeometricSequence`처럼 값을 만들거나 `Zip`, `Unzip`,
`Concat`, `Reverse`로 레인 배치를 바꾸는 API가 `Vector64`부터 `Vector512`와
`Vector<T>`까지 추가된다.
Arm에서는 SVE2 인트린식과 `CreateWhile`의 변형이 늘고, SVE_AES, SVE_SHA3,
SVE_SM4, SHA3, SM4가 별도 명령어 집합으로 보고된다.
`AvxVnni.V512`는 512비트 AVX-VNNI를 노출한다.

한 가지 동작 변경이 숨어 있다.
float와 double을 작은 정수형으로 바꾸는 unchecked 변환은 이제 중간 절단을 거쳐
값이 감겨 돌아가는 대신 형의 경계로 포화한다.
숫자 변환 결과에 기대는 코드는 이 항목을 점검해야 한다.

## 그 밖의 런타임 변경

- **ReadyToRun:** `Comparer<T>.Default`와 `EqualityComparer<T>.Default`가 R2R
  이미지 안에서 전용 도우미로 특수화된다.
이전에는 R2R이 볼 수 없는 리플렉션을 써서 호출자가 JIT로 돌아갔고, 기본 비교자에
  기대는 컬렉션 연산에서 최대 20배 개선을 문서는 보고한다.
- **VM:** JIT가 없는 플랫폼(iOS 등)의 캐시된 인터페이스 디스패치는 인터페이스
  호출이 많은 코드에서 최대 200배, 리눅스의 `Guid.NewGuid()`는 `getrandom()`과
  배치 캐시로 약 12% 처리량이 좋아진다.
- **NativeAOT:** 인터페이스 호출을 공유 도우미로 보내 호출 지점의 바이너리
  크기를 줄이고, `Assembly.GetCallingAssembly()`가 스택 트레이스 데이터가 있을
  때 동작한다.
- **WebAssembly:** WebCIL 로딩, 디버깅 심볼, `float[]` 계열 마샬링이 개선되고
  CoreCLR WASM 빌드는 WebCIL V1이 기본이 되며, 네이티브 재링크가 동작하고
  Release 빌드의 JavaScript가 압축된다.
NativeAOT WASM 게시가 패키지의 위성 어셈블리를 더 이상 떨어뜨리지 않는다.
- **1024개 초과 CPU:** `sched_getaffinity`가 `cpu_set_t` 기본 크기(1024)에 막혀
  초기화에 실패하던 문제가, CPU 집합을 동적으로 할당해 해결된다.
GC의 1024개 힙 제한은 그대로다.
- **크래시 보고:** 죽어가는 프로세스 안에서 관리 스택 트레이스, 모듈 목록, 주요
  런타임 상태를 남기는 프로세스 내 보고가 Linux와 macOS에 들어온다.
`DOTNET_DbgEnableMiniDump`가 꺼져 있을 때 `DOTNET_EnableCrashReport=1` 또는
  `DOTNET_EnableCrashReportOnly=1`로 고른다.
- **iOS와 tvOS 파일 잠금:** 시뮬레이터 포함 CoreCLR가 권고 파일 잠금을 기본으로
  끈다.
백그라운드로 들어갈 때 잠금을 쥔 앱이 운영체제에 종료될 수 있기 때문이다.
그 결과 같은 프로세스 안의 핸들 사이에서도 `FileShare` 제한이 강제되지 않는다.
되살리려면 `DOTNET_SYSTEM_IO_DISABLEFILELOCKING=0` 또는 런타임 설정
  `System.IO.DisableFileLocking`을 `false`로 둔다.
- **신뢰성 수정:** RHEL 8 Arm64에서 SDK 충돌, cgroup v2 메모리 한도 탐색,
  `AssemblyLoadContext`를 반복 언로드한 뒤의 제네릭 가상 호출 정지,
  `TryDequeue`와 `TryPeek`의 빈 큐 오보, Windows 다중 CPU 그룹의 GC가 고쳐졌다.
- **진단:** async 프로파일러가 runtime-async 메서드와 컴파일러 생성 상태 머신
  메서드를 한 가지 이벤트 모델로 계측한다.

## 비평

### 문서는 변경 목록이지 측정 자료가 아니다

문서가 제시하는 성능 수치는 “최대 20배”, “최대 200배”, “5–50%”, “약 12%”처럼
조건이 적히지 않은 값이다.
어떤 하드웨어, 어떤 벤치마크인지가 본문에 없어서 독자가 자기 앱에서 얼마나
개선될지는 알 수 없다.
Runtime Async도 처리량이 어떻게 달라지는지는 숫자 없이 “오버헤드가 낮다”고만
적고, 도움이 되는지 직접 보고해 달라고 요청한다.
이는 프리뷰 기능에 대한 정직한 서술이지만, 켜기 전에 읽는 사람에게는 판단 근거가
없다는 뜻이다.

### 하드웨어 상향의 비용은 “공식 지원” 바깥에서 생긴다

문서의 근거는 새 기준선이 Windows 11과 Windows 10이 공식 지원하는 CPU와 같다는
것이다.
그러나 .NET은 Linux 서버, 컨테이너, Raspberry Pi, 에뮬레이터, 구형 가상 머신 CPU
모델에서도 돈다.
가상 머신이 노출하는 CPU 모델은 하드웨어보다 낮은 명령어 집합만 보이게 설정된
경우가 있고, 그런 환경은 Windows의 공식 지원 목록으로 판단되지 않는다.
문서는 이 경우를 다루지 않으며, 이 지적은 문서에 없는 점을 짚은 것이라 환경마다
확인이 필요하다.

### 프리뷰 기능을 라이브러리가 먼저 쓰는 위험은 설명되지 않았다

런타임 라이브러리는 이미 `runtime-async=on`으로 컴파일된다고 문서는 적는다.
이는 기능을 폭넓게 검증하는 방법이지만, 프리뷰라고 하는 기능 위에 기본
라이브러리가 올라간다는 뜻이기도 하다.
앱이 이 경로를 켜지 않더라도 라이브러리 쪽 동작은 바뀔 수 있는데, 문서는
사용자가 느낄 차이(예: 스택 트레이스 모양, 디버거 동작)를 라이브러리 쪽에서는
따로 구분해 적지 않는다.

## 확인할 것

- 배포 대상 CPU가 x86-64-v2(x64) 또는 Windows의 LSE(Arm64)를 만족하는지
  확인한다.
특히 가상 머신 CPU 모델과 구형 서버를 본다.
- 실행 실패 메시지(“missing one or more of the baseline instruction sets”)를
  장애 목록에 넣어 둔다.
- Runtime Async는 앱 하나에서 `<Features>runtime-async=on</Features>`로 켜 보고,
  처리량과 크기를 켜기 전후로 측정한다.
이상이 있으면 `<UseRuntimeAsync>false</UseRuntimeAsync>`로 끈다.
- `DOTNET_RuntimeAsync`로 제어하던 스크립트가 있다면 제거된 변수이므로 바꾼다.
- iOS나 tvOS 앱이 `FileShare`에 기대고 있다면 잠금 기본값 변경을 점검한다.
- float나 double을 작은 정수형으로 바꾸는 unchecked 변환의 결과가 달라지는지
  테스트한다.
- 크래시 진단이 필요하면 `DOTNET_EnableCrashReport=1`을 시험한다.

## 기억할 원칙

런타임 릴리스 노트는 “무엇이 빨라졌는가”보다 “무엇을 더 이상 지원하지 않는가”를
먼저 읽는다.
.NET 11에서 그 답은 최소 CPU 기준선이고, 실패할 때는 느려지는 것이 아니라 시작을
못 한다.

---

[^tikotus]: <https://news.ycombinator.com/item?id=50446399>

[^electroly]: <https://news.ycombinator.com/item?id=50447541>

[^gdwatson]: <https://news.ycombinator.com/item?id=50441059>

[^bjoli]: <https://news.ycombinator.com/item?id=50454102>
