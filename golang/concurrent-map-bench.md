# Go Concurrent Map 벤치마크

<https://github.com/puzpuzpuz/go-concurrent-map-bench>

Go의 동시성 해시맵 구현체 5종을 비교한 벤치마크.
xsync 저자가 만들었지만 중립성을 지키려 노력했다고 밝혔다.

## 비교 대상

| 라이브러리             | 구조                                  |
| ---------------------- | ------------------------------------- |
| `sync.Map` (stdlib)    | HashTrieMap, 16-way 분기, lock-free 읽기 |
| `xsync.Map`            | 캐시 라인 크기 버킷, SWAR 기반 조회   |
| `cornelk/hashmap`      | lock-free 해시 + 정렬 연결 리스트     |
| `alphadose/haxmap`     | Harris의 lock-free 알고리즘, lazy 삭제 |
| `orcaman/concurrent-map` | 32개 고정 샤드, RWMutex              |

## 벤치마크 조건

**워크로드:** 100% 읽기, 99/0.5/0.5, 90/5/5, 75/12.5/12.5
(읽기/쓰기/삭제 비율)

**키 타입:** string(긴 접두사로 해싱 부하), int

**맵 크기와 메모리 계층:**

| 크기      | 메모리     | 대상       |
| --------- | ---------- | ---------- |
| 100       | ~15 KB     | L1 캐시    |
| 1,000     | ~150 KB    | L2 캐시    |
| 100,000   | ~15 MB     | L3 캐시    |
| 1,000,000 | ~150 MB    | RAM        |

**환경:** AMD Ryzen 9 7900, GOMAXPROCS 1/4/8/12

## 결과 요약

| 라이브러리             | 강점                            | 약점                             |
| ---------------------- | ------------------------------- | -------------------------------- |
| `sync.Map`             | stdlib, 읽기 스케일링 우수      | 쓰기 할당 비용 최고              |
| `xsync.Map`            | 거의 모든 시나리오에서 최고 성능 | 외부 의존성                      |
| `cornelk/hashmap`      | 소규모에서 경쟁력 있음          | 10만 이상 크기에서 성능 급락     |
| `alphadose/haxmap`     | 소규모 읽기 전용에서 양호       | 쓰기 경합 시 스케일링 부진       |
| `orcaman/concurrent-map` | 할당 0, 단순하고 예측 가능    | 32 샤드 한계, 읽기 처리량 최저   |

## 할당량 (B/op, WarmUp 기준)

**String 키:**

| 라이브러리             | 100% 읽기 | 99% 읽기 | 90% 읽기 | 75% 읽기 |
| ---------------------- | --------- | -------- | -------- | -------- |
| `sync.Map`             | 0         | 0        | 3        | 9        |
| `xsync.Map`            | 0         | 0        | 1        | 2        |
| `cornelk/hashmap`      | 0         | 0        | 1        | 4        |
| `alphadose/haxmap`     | 0         | 0        | 1        | 3        |
| `orcaman/concurrent-map` | 0       | 0        | 0        | 0        |

`orcaman/concurrent-map`는 일반 Go map을 사용하므로
기존 키 덮어쓰기 시 할당이 발생하지 않는다.
비샤드 구현체 중에서는 `xsync.Map`의 할당량이 가장 낮다.

## 분석

**`sync.Map` — Go 1.24 이후 재평가 필요.**
HashTrieMap으로 내부 구현이 바뀌면서 이전 버전 대비
크게 개선되었다. 그러나 쓰기 할당 비용이 여전히 가장 높고,
모든 워크로드에서 `xsync.Map`보다 느리다.

**`xsync.Map` — 사실상 최강.**
SWAR을 활용한 메타데이터 기반 조회가 핵심이다.
캐시 라인 크기로 맞춘 버킷 설계가 CPU 캐시 활용을
극대화한다. 리사이징도 협력적(cooperative)으로 처리해
전체 goroutine이 마이그레이션을 분담한다.

**`cornelk/hashmap` — 소규모 전용.**
10만 이상 크기에서 성능이 급격히 떨어져 벤치마크에서
제외되었다. CAS 기반 정렬 연결 리스트의 순회 비용이
데이터 크기에 비례해 증가하기 때문이다.

**`orcaman/concurrent-map` — 단순함의 대가.**
32개 고정 샤드는 구현이 가장 단순하지만,
코어 수가 늘어도 스케일링이 제한된다.
채널 기반 Range API로 인해 반복 성능도 최하위다.

## 인사이트

**1. lock-free가 항상 빠른 건 아니다.**
`cornelk/hashmap`과 `alphadose/haxmap`은 lock-free지만
`xsync.Map`(per-bucket mutex)보다 느리다.
캐시 친화적 데이터 배치가 동기화 방식보다 중요하다.

**2. 메모리 계층이 성능을 지배한다.**
맵 크기가 L1→RAM으로 넘어가면 구현체 간 격차가 벌어진다.
`xsync.Map`의 캐시 라인 정렬 설계가 대규모에서 빛나는
이유다.

**3. `sync.Map`은 이제 합리적 선택지다.**
Go 1.24의 HashTrieMap 전환 이후 성능이 대폭 개선되었다.
외부 의존성 없이 적당한 성능이 필요하면 충분하다.

**4. 샤드 수는 하드코딩하지 마라.**
`orcaman/concurrent-map`의 32개 고정 샤드는
GOMAXPROCS가 올라갈수록 병목이 된다.
동적 샤딩이나 다른 접근이 필요하다.

**5. 쓰기 비율이 선택을 결정한다.**
읽기 100%면 대부분의 구현체가 비슷하다.
쓰기가 5%만 섞여도 격차가 벌어지기 시작하고,
25%면 `xsync.Map`과 나머지의 차이가 확연하다.

## 참고

- [xsync](https://github.com/puzpuzpuz/xsync)
- [sync.Map (Go 1.24 HashTrieMap)](https://pkg.go.dev/sync#Map)
- [cornelk/hashmap](https://github.com/cornelk/hashmap)
- [alphadose/haxmap](https://github.com/alphadose/haxmap)
- [orcaman/concurrent-map](https://github.com/orcaman/concurrent-map)
