# mimalloc — Microsoft의 고성능 범용 메모리 할당자

<https://github.com/microsoft/mimalloc>

HN 토론: <https://news.ycombinator.com/item?id=20249743> (356점, 66개 댓글)

## 소개

mimalloc은 Microsoft Research의 Daan Leijen이 Koka와 Lean 프로그래밍 언어를 위해 개발한 범용 메모리 할당자(memory allocator)다.
현재는 Bing, Microsoft Azure, Cosmos DB, Unreal Engine 등 대규모 프로덕션 시스템에서 사용되는 산업급 구현체로 성장했다.
MIT 라이선스로 공개되어 있으며, 약 10,000줄 수준의 작고 일관된 코드베이스를 유지한다.

기존의 대표 할당자인 jemalloc, tcmalloc, Hoard와 비교해 다양한 워크로드에서 일관되게 우수한 성능을 보인다.
Lean 정리 증명기(theorem prover) 워크로드에서 tcmalloc 대비 13% 빠른 속도를 기록했으며, 메모리 사용량도 유사하거나 낮은 수준을 유지한다.
13,000개 이상의 GitHub 스타와 1,100개 이상의 포크를 보유한 활발한 오픈소스 프로젝트다.

## 아키텍처

mimalloc의 핵심 설계 원칙은 “작고 일관된(small and consistent)” 구조다.
복잡한 잠금 메커니즘 대신 단일 CAS(Compare-And-Swap) 원자적 연산만을 사용해 멀티스레드 환경에서도 경쟁(contention)을 최소화한다.

**Free list sharding** 기법이 핵심이다.
할당을 메모리 페이지당 여러 개의 작은 리스트에 분산시켜 단편화(fragmentation)를 줄인다.
**Free list multi-sharding**은 여기서 한 단계 더 나아가 페이지당 복수의 free list를 유지한다.
하나는 스레드 로컬 연산용, 다른 하나는 동시 접근용이다.

버전별 아키텍처 차이도 있다.

- v2: 스레드 로컬 세그먼트(thread-local segments) 기반
- v3: 아레나(arena) 기반으로 단순화된 lock-free 설계, 모든 스레드에서 할당 가능한 1등급 힙(first-class heap) 지원

페이지가 비어지면 즉시 OS에 반환 신호를 보내는 eager page purging으로 메모리 반환을 최적화한다.
보안 모드(`-DMI_SECURE=ON`)에서는 가드 페이지(guard page)와 암호화된 free list를 제공한다.

## 사용법

가장 간단한 통합 방법은 `LD_PRELOAD`를 통한 동적 오버라이드다.
코드 수정 없이 기존 프로그램의 malloc을 mimalloc으로 교체할 수 있다.

```bash
LD_PRELOAD=/usr/local/lib/libmimalloc.so my-program
```

macOS에서는 `DYLD_INSERT_LIBRARIES`를 사용한다.
Windows에서는 리다이렉션 DLL(`mimalloc.dll`)로 오버라이드한다.

CMake를 통한 빌드는 다음과 같다.

```bash
cmake ../.. && make
```

`src/static.c` 단일 파일을 직접 컴파일해 CMake 없이 통합할 수도 있다.
통계 확인은 환경변수 `MIMALLOC_SHOW_STATS=1`로 활성화한다.

## 주요 기능

| 기능          | 설명                                            |
| ------------- | ----------------------------------------------- |
| Drop-in 교체  | 코드 수정 없이 malloc 교체 가능                 |
| NUMA 지원     | 대규모 서버 환경의 NUMA 토폴로지 인식           |
| 보안 모드     | 가드 페이지, 암호화 포인터로 버퍼 오버플로 탐지 |
| 가이드 모드   | `-DMI_GUARDED=ON`으로 오버플로 탐지 강화        |
| 크로스플랫폼  | Linux, macOS, Windows, WASM, BSD 등 지원        |

## 라이선스 및 상태

MIT 라이선스로 상업적 사용이 자유롭다.
2026년 4월 기준 최신 버전은 v3.3.2이며, v2.x와 v1.x 브랜치도 병행 유지 중이다.

## 분석

### 설계 철학: 단순성이 성능을 만든다

mimalloc의 약 10,000줄 코드베이스는 경쟁 할당자들에 비해 작은 편이다.
이 단순성은 유지보수성뿐 아니라 CPU 캐시 적중률에도 긍정적 영향을 준다.
코드가 작으면 할당자 자체의 코드가 더 자주 캐시에 머물고, 결과적으로 실행 속도가 향상된다.

Free list sharding은 멀티코어 환경에서 특히 효과적이다.
기존 할당자들이 중앙화된 free list를 가드하기 위해 복잡한 잠금을 사용하는 반면, mimalloc은 분산 구조로 잠금 경쟁 자체를 원천 차단한다.

### v3의 아레나 기반 전환

v3에서 스레드 로컬 세그먼트 대신 아레나 기반 관리로 전환한 것은 주목할 만한 변화다.
스레드 로컬 방식은 스레드 이동(thread migration)이 잦은 워크로드에서 메모리를 비효율적으로 사용할 수 있다.
아레나 방식은 모든 스레드가 동일한 메모리 풀을 공유해 이 문제를 해결한다.
특히 서버 환경에서 스레드 풀(thread pool)을 사용하는 워크로드에서 이점이 두드러진다.

## 비평

### 성능 수치의 맥락 의존성

“tcmalloc 대비 13% 빠르다”는 수치는 Lean 정리 증명기라는 특수한 워크로드에서의 결과다.
범용적 성능 우위를 주장하려면 다양한 워크로드 프로파일에 걸친 중간값(median) 비교가 필요하다.
실제로 특정 할당 패턴(예: 단기 소량 할당이 지배적인 경우)에서는 tcmalloc이나 jemalloc이 더 나을 수 있다.

이 우려는 실제 프로덕션 사례로 뒷받침된다.
ClickHouse 팀의 danlark는 mimalloc을 자체 워크로드에 적용했을 때
jemalloc 대비 약 2배 느린 결과를 얻었다고 보고했다.[^danlark]
Discourse가 Ruby 환경에서 테스트했을 때도 jemalloc보다 좋지 않은 결과가 나왔다.[^ksec]

벤치마크 방법론 자체에도 문제가 있다.
shereadsthenews는 tcmalloc과의 비교가 공정하지 않을 수 있다고 지적한다.[^shereadsthenews]
tcmalloc은 스레드 캐시 크기 등 수많은 파라미터를 가지는데 기본값이 충분하지 않은 경우가 많다.
16개 스레드 환경이라면 기본 3MiB 스레드 캐시를 훨씬 크게 설정하는 것이 권고된다.
결국 "자신의 워크로드로 직접 빌드하고 테스트"하는 것이 유일하게 신뢰할 수 있는 방법이다.

### 오버라이드 방식의 한계

`LD_PRELOAD` 방식은 편리하지만 동적 링크된 바이너리에만 적용된다.
정적으로 링크된 바이너리나 커스텀 malloc 구현을 내장한 런타임(예: Go, Java GC)에는 효과가 없다.
실제 성능 이득을 보려면 소스 수준 통합이 필요한 경우가 많다.

## 인사이트

### 메모리 할당자는 숨겨진 성능 레버다

대부분의 성능 최적화는 알고리즘 개선이나 I/O 최소화에 집중된다.
그러나 메모리 할당은 모든 프로그램의 기반 연산임에도 대개 기본 시스템 할당자에 맡겨진다.
mimalloc처럼 drop-in 교체 가능한 할당자는 코드 한 줄 변경 없이 전체 시스템 성능을 수 퍼센트 개선할 수 있는 드문 기회를 제공한다.
Death Stranding 같은 게임 엔진에서도 채택한 것은 할당자 최적화가 CPU 집약적 워크로드에서 실질적 차이를 만든다는 증거다.

### 보안과 성능의 동시 추구

mimalloc의 보안 모드는 가드 페이지와 암호화 포인터를 제공하면서도 성능을 크게 희생하지 않는다.
전통적으로 보안 강화는 성능 저하를 수반했지만, mimalloc은 옵트인(opt-in) 방식으로 이 트레이드오프를 사용자에게 위임한다.
이 설계 원칙은 현대 시스템 소프트웨어가 취해야 할 방향을 잘 보여준다.
보안 기능을 기본 비활성화하되 선택 가능하게 해, 프로덕션에서 성능을 얻고 디버그 빌드에서 안전성을 얻을 수 있다.

### 단순성이 경쟁 우위가 되는 역설

10,000줄의 코드베이스는 수십만 줄의 경쟁 프로젝트들 사이에서 오히려 강점이다.
단순한 코드는 CPU 명령어 캐시 효율을 높이고, 기여자 진입 장벽을 낮추며, 버그 발생 가능성을 줄인다.
mimalloc이 “빠른 이유”는 단지 알고리즘이 뛰어나서가 아니라, 불필요한 복잡성을 제거했기 때문이다.
소프트웨어 설계에서 단순성이 성능으로 직결되는 사례를 메모리 할당자라는 가장 기본적인 레이어에서 확인할 수 있다는 점이 흥미롭다.

huhtenberg는 다른 각도의 시각을 더한다.[^huhtenberg]
할당자 분야는 이미 성숙하여 표준적인 해법이 수렴하는 경향이 있다는 것이다.
멀티스레드 환경의 복잡한 문제들, 즉 크로스 스레드 할당·해제와 캐시 경쟁을 해결하다 보면
대부분의 고성능 할당자가 "중앙 슬랩/풀/free list + 스레드별 캐시" 구조로 수렴한다.
이 관점에서 보면 mimalloc의 단순성은 설계 혁신이라기보다 수렴하는 해법을
가장 간결하게 구현했다는 의미일 수 있다.
그러나 그 간결함 자체가 유지보수성과 캐시 효율에서 실용적 가치를 낳는다는 점은 여전히 유효하다.

---

[^danlark]: <https://news.ycombinator.com/item?id=20251614>
[^ksec]: <https://news.ycombinator.com/item?id=20263371>
[^shereadsthenews]: <https://news.ycombinator.com/item?id=20250967>
[^huhtenberg]: <https://news.ycombinator.com/item?id=20250099>
