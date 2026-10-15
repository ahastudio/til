# Lore: Epic Games의 차세대 오픈소스 버전 관리 시스템

<https://lore.org/>

<https://github.com/EpicGames/lore>

HN 토론: <https://news.ycombinator.com/item?id=48571081> (1276점, 680개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version> (75점, 65개 댓글)

GN 토론: <https://news.hada.io/topic?id=30586>

## 소개

Lore는 Epic Games가 개발하고 MIT 라이선스로 공개한 버전 관리 시스템이다.
2026년 5월 GitHub에 공개되었고,
Epic은 6월 17일 이를 정식으로 발표했다.[^asawicki]
2026년 10월 14일 기준 최신 릴리스는 10월 6일에 나온 v0.10.1이며,
저장소의 스타는 8,914개, 포크는 459개다.[^lore-gh]
아직 1.0 이전이라 인터페이스, 디스크 형식,
API가 릴리스 사이에 바뀔 수 있다.[^lore-readme]
“차세대”라는 수식어는 게임·엔터테인먼트 산업의 구체적 문제를 겨냥한다.
코드와 수십 기가바이트 규모의 바이너리 에셋이
같은 레포지토리에 공존하는 환경에서
기존 도구들의 한계를 해결하는 것이 목표다.

Lore는 Git처럼 분산형이 아니라 **중앙 집중형** 시스템이다.
단일 서버가 내구성·접근 제어·충돌 해결의 정본(source of truth)으로 기능한다.
그러나 커밋, 브랜치 전환, diff,
스테이징 같은 일상 작업은 서버 접촉 없이 로컬에서 실행된다.
이 설계는 Perforce의 “모든 작업에 서버 왕복” 방식과
Git의 “완전 분산” 방식 사이의 중간지점이다.

Lore는 원래 “Unreal Revision Control”이라는
이름으로 UEFN(Unreal Editor for Fortnite)에 내장되어
Epic 내부에서 수년간 사용되었다.
오픈소스로 공개된 버전과 UEFN 내장 버전 사이에는 아직 압축 포맷 차이가 존재하며,
Epic은 이 간극을 없애기 위해 UEFN을 오픈소스 포맷으로 이전 중이다.
로드맵에 따르면 오픈소스판은 Zstandard를,
UEFN은 Oodle을 써서 서로 호환되지 않으며,
Epic은 UEFN을 Zstandard로 옮기고 있다.[^lore-roadmap]
데스크탑 클라이언트는 바이너리로 제공되지만 아직 오픈소스가 아니다.

## 설치

### 스크립트 설치 (권장)

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/EpicGames/lore/main/scripts/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/EpicGames/lore/main/scripts/install.ps1 | iex
```

### 소스 빌드

```bash
# CLI 클라이언트
cargo build --release -p lore-client --bin lore

# 서버
cargo build --release -p lore-server --bin loreserver
```

Rust stable 툴체인이 필요하다.
포맷팅에는 nightly가 사용된다.

## 사용법

### 서버 시작

```bash
# 로컬 데모 서버 (인증서·스토어 자동 생성)
LORE_DEMO=1 loreserver

# 설정 파일 지정
LORE_CONFIG_PATH=/etc/lore LORE_ENV=prod loreserver
```

기본 포트는 `41337`(QUIC/gRPC), `41339`(HTTP 헬스체크), `41340`(내부 복제)이다.

### 기본 워크플로

```bash
# 레포지토리 생성
lore repository create lore://127.0.0.1:41337/my-project

# 파일 스테이징
lore stage hello.txt sample.bin

# 커밋
lore commit "Initial revision"

# 원격에 반영
lore push

# 다른 워크스페이스로 클론
lore clone lore://127.0.0.1:41337/my-project ./workspace2

# 브랜치 생성 및 전환
lore branch create feature
lore branch switch feature

# 브랜치 병합
lore branch merge feature into main
```

### CLI 명령 구조

`lore <그룹> <명령> [옵션]` 형태로 구성된다.
자주 쓰는 명령은 최상위 단축어로도 제공된다.

| 그룹           | 주요 명령                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------- |
| `repository`   | `create`, `clone`, `verify`, `gc`, `info`, `config`, `metadata`                                    |
| `branch`       | `list`, `create`, `switch`, `push`, `merge`, `diff`, `archive`, `reset`, `protect`                 |
| `revision`     | `history`, `info`, `commit`, `amend`, `sync`, `bisect`, `diff`, `restore`, `cherry-pick`, `revert` |
| `file`         | `info`, `stage`, `unstage`, `reset`, `dirty`, `obliterate`, `history`, `diff`, `hash`              |
| `auth`         | `login`, `logout`, `list`, `clear`, `info`                                                         |
| `lock`         | `acquire`, `release`, `query`, `status`                                                            |
| `layer`        | `add`, `remove`, `list`                                                                            |
| `link`         | `add`, `remove`, `update`, `list`                                                                  |
| `service`      | `run`, `start`, `stop`                                                                             |
| `shared-store` | `create`, `info`, `set-use-automatically`                                                          |

#### 자주 쓰는 단축어

`clone`, `status`, `stage`, `unstage`, `reset`, `diff`,
`history`, `commit`, `sync`, `push`, `dirty`, `login`

### 전역 플래그

```text
--repository <path>      레포지토리 경로 지정
--log-level <level>      로그 레벨 (TRACE|DEBUG|INFO|WARN|ERROR)
--debug / --silent       출력 제어
--json                   JSON 형식 출력
--no-pager               페이저 비활성화
--force / --dry-run      강제 실행 / 시뮬레이션
--offline / --remote / --local   데이터 소스 선택
--identity <id>          커밋 아이덴티티 지정
--max-connections <n>    최대 연결 수
--file-size-limit <n>    파일 크기 제한
--compress-limit <n>     압축 임계값
--non-interactive        대화형 입력 비활성화
```

## 설정

### 레포지토리 설정 (`.lore/config.toml`)

```toml
remote_url = "lore://127.0.0.1:41337/my-project"
identity = "user@example.com"

[store]
max_capacity = 10485760     # 로컬 캐시 용량 (기본 10 MiB)
eviction_delay = 10         # 캐시 퇴거 지연 (초)
max_size = 10737418240      # 최대 캐시 크기 (10 GiB)
compaction_delay = 30       # 압축 지연 (초)
verify_write = false

[file]
direct_write = false
direct_io = false
flush_write = false
```

### 희소 워크스페이스 (`.lore/view`)

레포지토리 전체가 아닌 필요한 경로 부분집합만
로컬에 구체화(materialize)할 수 있다.

```text
/Assets/Characters/**
/Source/Game/Core/**
```

### 스테이징 제외 (`.loreignore`)

```text
*.log
build/
.DS_Store
```

### CLI 사용자 설정

```toml
# ~/.config/lore/cli.toml (Linux 기준)
pager = "less -R"
```

### 환경 변수

| 변수                       | 설명                                     |
| -------------------------- | ---------------------------------------- |
| `LORE_DEMO=1`              | 데모 모드 (임시 인증서·스토어 자동 생성) |
| `LORE_CONFIG_PATH`         | 서버 설정 디렉터리                       |
| `LORE_ENV`                 | 설정 파일 환경 이름 (`dev`, `prod` 등)   |
| `LORE__TOPOLOGY__PROVIDER` | 스토리지 백엔드 지정 (예: `aws`)         |
| `LORE_MAX_THREADS`         | 스레드 풀 크기                           |

## 아키텍처

### 코드베이스 구조

Lore는 Rust로 작성된 워크스페이스로 구성된다.

| 크레이트            | 역할                                |
| ------------------- | ----------------------------------- |
| `lore`              | 핵심 라이브러리 (C ABI 포함)        |
| `lore-client`       | CLI 바이너리                        |
| `lore-server`       | 서버 데몬                           |
| `lore-storage`      | 콘텐츠 주소 저장소 엔진             |
| `lore-revision`     | 리비전 그래프·Merkle 트리           |
| `lore-capi`         | C FFI 바인딩 (`lore.h`, ~10,000 줄) |
| `lore-proto`        | Protocol Buffers / gRPC 명세        |
| `lore-transport`    | 네트워크 전송 계층 (QUIC)           |
| `lore-credential`   | 자격증명 저장·해석                  |
| `lore-aws`          | AWS S3 / DynamoDB 백엔드            |
| `lore-hashicorp`    | HashiCorp Vault 통합                |
| `lore-chaos-client` | 카오스 테스트 클라이언트            |

### 콘텐츠 주소 저장소와 Merkle 트리

모든 데이터는 BLAKE3 해시로 식별되는 콘텐츠 주소 저장소에 저장된다.
텍스트와 바이너리를 구분하지 않고 불투명한 바이트 스트림으로 취급한다.
레포지토리 상태는 Merkle 트리로 표현된다.
파일 노드는 콘텐츠 해시에서, 디렉터리 노드는 정렬된 자식 해시에서 도출되며,
루트 해시 하나로 전체 상태를 유일하게 식별한다.

각 리비전은 부모 리비전의 해시를 포함하므로,
리비전 체인 자체가 암호화된 불변 연결을 형성한다.
구조적 중복 제거가 자연스럽게 발생한다.
파일 하나만 바뀐 두 리비전은 변경되지 않은 모든 노드와 디렉터리를 공유한다.
저장 비용은 레포지토리 크기가 아닌 변경량에 비례한다.

### 청킹과 대용량 파일 처리

대용량 파일은 두 전략으로 청크화된다.
**FastCDC**(콘텐츠 정의 청킹)는 롤링 해시로
경계를 탐지하며 평균 64KiB 청크를 목표로 한다.
같은 바이트 영역이 버전 간에 이동해도 중복 제거가 유지된다.
**고정 크기 청킹**은 동일 내용에 항상 동일 해시를 보장하는 정규 주소를 제공한다.

멀티 테라바이트 파일은 프래그먼트 참조 리스트가
재귀적으로 청크화되어 트리 구조를 형성한다.
각 레벨이 독립적으로 주소화·중복 제거·지연 페치된다.
프래그먼트 참조에 바이트 오프셋이
포함되어 임의 범위 읽기 시 해당 범위를 커버하는 프래그먼트만 가져온다.
압축(기본값 Zstd)은 주소 지정과 직교하므로
압축 방식이 달라도 중복 제거가 보존된다.

### 스토리지 레이어

```text
Immutable Store (콘텐츠 주소, 추가 전용)
├── 파일·디렉터리·트리 페이로드
└── 프래그먼트 참조 목록

Mutable Store (가변 키-값)
├── 브랜치 포인터
├── 스테이지드 앵커 (인스턴스별 로컬 상태)
└── 메타데이터 (사용자 정의 키-값)

Local Cache
├── 인스턴스 캐시 (워크스페이스별)
└── Shared Store (여러 인스턴스가 공유, 중복 제거)
```

#### 압축 알고리즘

| 알고리즘     | 비율   | 압축 속도 | 비고               |
| ------------ | ------ | --------- | ------------------ |
| Zstd level 6 | 28.9%  | 136 MiB/s | 기본값             |
| LZ4          | 47.6%  | 719 MiB/s | 빠른 압축·해제     |
| Oodle Kraken | (낮음) | ~2 MiB/s  | 하위 호환용 레거시 |

### 희소 워크스페이스와 온디맨드 하이드레이션

`.lore/view` 파일이 레포지토리의 어느 부분집합을 로컬에 구체화할지 선언한다.
필요할 때만 파일 데이터를 가져오므로 수백만 파일 레포지토리에서도
워크스페이스가 가볍게 유지된다.

브랜치는 경량 가변 참조로 구현된다.
브랜치 생성과 전환이 데이터 복제 없이 저오버헤드로 처리된다.
브랜치 ID는 UUIDv7로 이름과 분리되어,
이름을 변경하거나 아카이브해도 브랜치 히스토리가 보존된다.

### 합성 프리미티브: 링크와 레이어

**링크**는 다른 레포지토리의 특정 리비전을 경로에 마운트하는 버전화된 참조다.
링크는 리비전과 함께 이동하므로 모든 클론이 동일한 링크를 본다.
각 링크 레포지토리는 독립된 파티션으로 접근 제어·버전 관리·중복 제거가 분리된다.

**레이어**는 리비전에 저장되지 않는 인스턴스 로컬 오버레이다.
같은 팀에서 사람마다 다른 레이어 구성을 가질 수 있다.
버전화가 부적합한 로컬 조합 문제를 해결한다.

### 인프라

팀 배포는 AWS S3(내구성 불변 저장소)와
DynamoDB(가변 키-값 저장소)를 기본 백엔드로 사용한다.
백엔드 인터페이스는 교체 가능하도록 명세화되어 있다.
브랜치 포인터 전진은 compare-and-swap으로 원자적으로 처리된다.
Push는 원격의 현재 상태가 클라이언트의 예상과
일치할 때만 성공하는 조건부 연산이다.

### API-first 설계: C 헤더

Lore는 C 헤더(`lore.h`, ~10,000 줄)를 정식 인터페이스로 선언한다.
CLI, IDE 플러그인,
원격 서비스가 모두 동일한 API를 사용하는 피어 애플리케이션이다.

핵심 타입:

| 타입                | 설명                                                                      |
| ------------------- | ------------------------------------------------------------------------- |
| `lore_hash_t`       | 32바이트 BLAKE3 해시                                                      |
| `lore_context_t`    | 16바이트 중복 제거 컨텍스트                                               |
| `lore_address_t`    | (hash, context) 쌍, 프래그먼트 식별자                                     |
| `lore_string_t`     | UTF-8 바이트 슬라이스 + 길이                                              |
| `lore_metadata_t`   | 태그드 메타데이터 (주소·불리언·해시·숫자·문자열)                          |
| `lore_error_code_t` | `NONE`, `INVALID_ARGUMENTS`, `ADDRESS_NOT_FOUND`, `INTERNAL`, `SLOW_DOWN` |

모든 연산은 이벤트 콜백으로 결과를 반환한다.
이벤트 타입: `LOG`, `PROGRESS`, `MAINTENANCE`,
`AUTH_URL`, `ERROR`, `COMPLETE`, `END`

C API 사용 순서:

```c
lore_set_allocator(...);   // 선택
lore_set_thread_limit(n);  // 선택
lore_log_configure(...);   // 선택
// 연산 실행 (이벤트 콜백 수신)
lore_shutdown();
```

### 와이어 프로토콜

네트워크 레이어는 `lore-proto/proto/` 하위 10개 `.proto` 파일로 명세화된다.

| 전송 프로토콜 | 포트  | 용도                       |
| ------------- | ----- | -------------------------- |
| QUIC (UDP)    | 41337 | 클라이언트 공개 엔드포인트 |
| gRPC / HTTP2  | 41337 | 공개 gRPC API              |
| HTTP          | 41339 | 헬스체크, 프리사인드 URL   |
| QUIC (mTLS)   | 41340 | 서버 간 복제               |

## 로드맵

공식 로드맵은 1.0 안정판까지의 큰 줄기를 시기별로 나눈다.[^lore-roadmap]
지금 저장하는 콘텐츠는 이후 모든 릴리스에서 읽을 수 있도록 형식을 설계했지만,
API와 프로토콜은 1.0 전까지 바뀔 수 있다고 밝힌다.

| 주제                               | 시기 | 상태    |
| ---------------------------------- | ---- | ------- |
| 오픈소스판과 UEFN 호환             | 2026 | 진행 중 |
| VS Code 플러그인                   | 2026 | 진행 중 |
| 확장 가능한 파일 잠금              | 2026 | 진행 중 |
| 가상 파일 시스템(VFS)              | 2026 | 진행 중 |
| 링크와 레이어                      | 2026 | 진행 중 |
| 데스크톱 클라이언트 오픈소스화     | 2027 | 진행 중 |
| Unreal Editor 플러그인             | 2027 | 진행 중 |
| 웹 클라이언트                      | 2027 | 확정    |
| 엣지 인스턴스와 고급 서버 토폴로지 | 2027 | 검토 중 |
| 포크와 격리된 파티션               | 이후 | 검토 중 |

가상 파일 시스템은 지금의 희소 클론이 가진 한계를 겨냥한다.
지금은 받을 범위를 미리 정해야 하고,
로컬에 두는 브랜치마다 디스크에 사본이 하나씩 생긴다.
VFS가 들어오면 파일을 열 때 공유 저장소에서 가져오므로
콘텐츠가 디스크에 한 번만 존재하게 된다.[^lore-roadmap]
로드맵은 방향일 뿐 보장이 아니며 시기는 목표라고 단서를 단다.

## 분석

### 게임 산업의 VCS 문제는 일반적 VCS 문제와 다르다

Git의 LFS는 대용량 파일을 포인터로 대체하는 추가 계층이다.
이 방식은 텍스트 중심 워크플로에서 이식성을
유지하면서 바이너리를 수용하는 타협안이다.
그러나 게임 개발에서는 바이너리가 예외가 아닌 기본이다.
100GB 텍스처 팩, 수십 GB 사운드 에셋,
대형 바이너리 DLL이 코드와 동등한 지위를 갖는다.
LFS는 이 규모에서 중앙화된 락킹, 희소 체크아웃,
아티스트 친화 UI 요구를 충족하지 못한다.

Perforce는 게임 산업에서 사실상 표준으로 자리잡은 이유가 있다.
중앙 집중형 설계는 락킹과 접근 제어가 자연스럽고,
대용량 파일 처리가 기본 기능이다.
그러나 소유권이 단일 회사에 있고, 프로토콜이 비공개이며,
모든 일상 작업에 서버 왕복이 필요하다.
Lore는 Perforce의 비즈니스 모델 의존성을
제거하면서 기술적 능력을 재현하려는 시도다.

HN 댓글에서 throw2ih020은 현장 경험을 공유했다.[^throw2ih020]
Perforce가 잘 작동할 때는 훌륭하지만, 충분히 자주 문제가 발생하여
전담 tools engineer가 수동으로 문제를 해결해야 한다는 것이다.
tlahtinen은 약 20년간의 게임 개발 경험을
바탕으로 더 핵심적인 관찰을 덧붙였다.[^tlahtinen]
Epic의 Unreal Engine에 Perforce 통합이 깊게 내장되어 있고,
반대로 Git 플러그인은
“Epic이 내부적으로 사용하지 않기 때문에 고통스럽게 미완성 상태”라는 점이다.
이는 Lore가 첫 번째 클래스 엔진 지원을 받을 것이라는 합리적 기대의 근거가 된다.

Git과 LFS로도 충분하지 않느냐는 반론도 있었다.
rootlocus는 LFS에도 파일 잠금이 있고
어떤 VCS도 바이너리 diff 도구를 주지 못하니,
Perforce, Diversion,
Lore와 Git+LFS 사이에 의미 있는 차이를 모르겠다고 했다.[^rootlocus]
이에 대해 가장 많은 답글을 받은 LugosFergus의 답은 권한이었다.
P4에서는 NDA에 서명한 사람만 특정 디렉터리를 볼 수 있게 할 수 있지만
Git은 전부 아니면 전무라는 것이다.[^LugosFergus]
Lore가 링크된 저장소마다 파티션과 접근 제어를
두는 설계가 바로 이 요구를 겨냥한다.
zipy124는 LFS를 오래 써 본 사람이라면 GitHub 같은 포지와 함께 쓸 때
얼마나 자주 깨지는지 안다고 했고,[^zipy124]
raincole은 LFS가 오래된 이력을 지울 수 없어서
초기에 자주 바뀐 에셋의 저장 비용을 저장소가
사는 내내 낸다고 지적했다.[^raincole]
tikotus는 이 차이를 한 문장으로 정리했다.
VCS는 중앙형과 분산형, 파일 단위와 커밋 단위로 나뉘는데,
게임에는 Perforce 같은 중앙형 파일 단위가 맞고
Git은 분산형 커밋 단위라는 것이다.[^tikotus]

현장의 Perforce 경험은 엇갈린다.
akurilin은 Perforce가 게임 업계의 사실상 표준이고
창작 인력 대부분이 이미 익숙하며 UE5의 안전한 기본값이라고 했고,[^akurilin]
dijit은 Git을 쓰던 팀을 넘겨받아 Perforce로 옮기자
아트 리뷰 시간이 몇 시간에서 몇 초로 줄었다고 했다.[^dijit]
반면 retroflexzy는 자기 업무의 상당 부분이
Perforce가 망가뜨린 작업 공간을 고치고 그러지 못하게
막는 래퍼를 만드는 일이라고 털어놓았다.[^retroflexzy]
Lobste.rs에서 가장 많은 표를 받은 icefox의 반응은
누군가 마침내 Perforce의 수십 년 독점에 질려 뭔가를 했다는 것이었다.[^icefox]

### BLAKE3 + FastCDC의 조합이 선택된 이유

BLAKE3는 병렬화 가능한 해시 함수로, 단일 코어에서도 SHA-256 대비 수 배 빠르다.
대규모 레포지토리에서 해시 계산 비용이
병목이 될 수 있는 환경에서 유의미한 선택이다.
Perforce가 MD5를 사용하는 것과 대조적으로, 충돌 저항성과 성능을 동시에 확보한다.

FastCDC는 Netflix, Restic, Borg 같은 백업 도구들이 검증한 접근이다.
파일 내부 동일 영역이 오프셋 이동 없이 중복 제거되므로
게임 에셋의 패치·업데이트 시나리오에서 전송량이 크게 줄어든다.
30GB 텍스처 파일에서 1MB 영역만 수정된 경우 해당 청크만 전송된다.
실측 벤치마크에서 238GB UE5 레포지토리 기준 약 20% 중복 제거율이 확인되었다.

### “API-first” 명세는 생태계 전략이다

Lore는 C 헤더를 정식 인터페이스로 선언한다.
CLI, IDE 플러그인,
원격 서비스가 모두 동일한 API를 사용하는 피어 애플리케이션이다.
온디스크·온와이어 포맷, 와이어 프로토콜,
스토리지 백엔드 인터페이스, 인가 계약이 모두 명세화된다.

이 설계는 서드파티 구현을 기술적으로 가능하게 만든다.
바이너리를 리버스 엔지니어링하지 않고도 명세에 맞는 호환 구현을 만들 수 있다.
Epic이 관리하는 단일 구현에 생태계가 종속되지 않는 구조다.
Git이 명세보다 구현 중심으로 발전한 것과 대조적인 접근이다.

## 비평

### “중앙 집중형이지만 오프라인 가능”이라는 주장은 실제 사용 조건을 숨긴다

Lore는 일상 작업이 서버 없이 로컬에서 실행된다고 강조한다.
그러나 희소 워크스페이스 모델에서 파일 데이터는 온디맨드로 가져온다.
오프라인 환경에서 워크스페이스에 없는 파일에 접근하면 페치가 실패한다.
“오프라인 작업 가능”은 이미 로컬에 하이드레이션된 파일 범위 내에서만 성립한다.

게임 개발자가 비행기에서 씬 에셋을 수정하려는 상황을 생각하면,
희소 워크스페이스 모델은 사전에 어떤 파일이
필요할지 예측해 미리 가져와야 한다는 부담을 전가한다.
이 조건은 README에서 명시되지 않는다.
“온디맨드”와 “오프라인 가능”을 동시에 주장하는
것은 실제 사용 시나리오에서 긴장 관계에 있다.

### 락킹 확장성 문제는 게임 산업의 핵심 요구사항을 충족하지 못한다

FAQ에 따르면 지금의 잠금은 다른 사람에게
알리기만 할 뿐 편집을 막지는 않는다.[^lore-faq]
FAQ는
“락 상태가 레포지토리 전체에서 전역으로 쿼리되어 대규모 프로젝트로 확장되지 않는다”고 솔직하게 인정한다.
게임 개발에서 락킹은 단순한 부가 기능이 아니다.
아티스트가 같은 바이너리 에셋을 동시에 수정하면 병합이 불가능하므로,
락킹은 작업 흐름의 핵심 조율 메커니즘이다.

[Perforce](perforce.md)가 게임 산업에서
지배적인 이유 중 하나가 성숙한 락킹 시스템이다.
Perforce는 `+l` 파일 형식으로 다른 사용자가 아예 파일을 열지 못하게 하는
배타적 체크아웃을 제공한다.[^p4-edit]
“확장 가능한 락킹”이 로드맵에 있다는 것은
현재 이 문제가 해결되지 않았음을 의미한다.
pre-1.0 상태에서 대규모 게임 프로젝트로의 전환을 권고하기 어려운 핵심 이유다.

swiftcoder는 락킹 부재와 함께 GUI 클라이언트 문제를 함께 지적했다.[^swiftcoder]
메시, 애니메이션, 사운드 같은 에셋에 대한 락킹 워크플로가 보이지 않는다는 점,
그리고 CLI만 존재한다면 아트 팀 전체가 커맨드라인에 익숙해져야 한다는 점이다.
데스크탑 클라이언트가 제공되지만 오픈소스가 아닌 현재 상황에서,
이 두 문제는 연결되어 있다.
아티스트 친화적 UI와 확장 가능한 락킹은 같은 사용자 그룹의 요구사항이며,
둘 다 현재 Lore가 완전히 해결하지 못한 영역이다.

### 데스크탑 클라이언트의 비공개 컴포넌트는 “완전 오픈소스” 주장과 충돌한다

Epic은 “완전 오픈소스”를 강조하지만,
데스크탑 클라이언트는 “아직 오픈소스가 아니다”고 명시한다.
독점 컴포넌트에 의존하기 때문이라고 설명하지만,
이 의존성의 성격은 공개되지 않는다.
아티스트와 비개발자 팀원은 CLI보다 데스크탑 클라이언트를 주로 사용한다.
“개발자를 위한” 오픈소스 핵심과
“아티스트를 위한” 비공개 클라이언트가 분리된 구조다.

HN의 iceweaselfan44는 이 모순을 한 줄로 압축했다.[^iceweaselfan44]
“완전 오픈소스”라고 선언한 페이지에서 데스크탑 클라이언트 링크를 클릭하면
“바이너리만 제공됩니다”라는 메시지를 마주친다는 것이다.
Epic이 “기여자는 Epic 엔지니어와 동등한 기능 접근권을 가져야 한다”고
원칙을 선언했지만,
데스크탑 클라이언트 접근에서 이 원칙이
실현되려면 클라이언트도 오픈소스가 되어야 한다.

### 커밋 이력이 vibe-coding의 흔적을 드러낸다면 핵심 신뢰 기반이 흔들린다

pkasting은 아이디어는 좋지만 커밋 메시지들이
vibe-coding의 산물임이 명확히 보이며,
버전 관리는 “97% 동작으로 충분한” 영역이 아니라고 지적했다.[^pkasting]
이 비판은 표면적인 스타일 문제가 아니다.

버전 관리 시스템에서 커밋 이력은 변경의 의도와 맥락을 담는 감사 추적이다.
vibe-coding으로 생성된 커밋 메시지는
코드의 왜(why)를 설명하지 않고 무엇(what)을 나열한다.
이는 향후 기여자가 설계 결정을 이해하거나 회귀를 추적할 때 직접적인 비용이 된다.
수천 명의 UEFN 사용자 데이터를 책임지는 시스템의 이력이 그 방식으로 관리된다면,
“불변 리비전 체인”이라는 기술적 보증이
“왜 이 변경이 이루어졌는가”를 설명하지 못하는 이력 위에 서게 된다.

Lobste.rs에서도 같은 비판이 나왔다.
sunshowers는 설계 문서에 LLM의 흔적이 많다며,
Mercurial과 Sapling을 “텍스트 우선”이라고 단정하는 대목처럼
대안을 제대로 검토하지 않고 세부를 틀리게 적은 부분을 짚었다.[^sunshowers]
JordiGH는 설계 문서의 영어조차 틀리는 LLM에게
소스 코드를 맡길 수 있느냐며,
97%만 맞는 소프트웨어라면 3%의 확률로 데이터가 깨져도 괜찮냐고 물었다.[^JordiGH]
Lobste.rs 관리 기록에는 사용자 제안으로
이 글에 `vibecoding` 태그가 자동으로 붙었다는 내용이 남아 있다.[^gerikson]

fg137는 더 구조적인 문제를 제기했다.[^fg137]
Epic은 내일 이 프로젝트를 포기해도 비즈니스에
아무 일도 일어나지 않는다는 것이다.
반면 Helix/Perforce는 버전 관리가 핵심 사업이라 그럴 수 없다.
MIT 라이선스와 명세 공개가 포크 가능성을 이론적으로 보장하지만,
활성 관리자 없는 포크는 보안 패치와 플랫폼 지원 업데이트가
필요한 인프라 도구에서 현실적 대안이 되기 어렵다.

## 인사이트

### 게임 산업이 버전 관리의 다음 아키텍처를 정의할 수 있다

Git의 설계는 Linux 커널 개발 패턴에서 나왔다.
텍스트 파일, 분산 개발자, 패치 단위 협업이 전제였다.
이 전제가 지난 20년간 소프트웨어 개발 전반에 적용되면서 Git이 기본값이 되었다.

그러나 AI 개발, 멀티미디어 콘텐츠,
대규모 바이너리 모델이 소프트웨어 개발의 구성 요소가 되면서,
“텍스트가 기본, 바이너리는 예외”라는 전제가 흔들리고 있다.
게임 산업은 이 미래의 선행 사례다.
Lore가 게임 산업의 문제를 해결하는 방식이
다른 산업의 버전 관리 미래를 미리 보여줄 수 있다.
머신러닝 팀이 수백 GB 모델 체크포인트를 버전 관리하는 문제는
게임 팀이 수백 GB 텍스처를 버전 관리하는 문제와 구조적으로 동일하다.

penciltwirler는 이 구조적 동일성이 이미 부분적으로
해결되었지만 서로 고립되어 있음을 지적했다.[^penciltwirler]
Pachyderm, XetHub(현 HuggingFace 일부), LakeFS,
Oxen 같은 AI/ML 데이터 버전 관리 도구들이
이미 유사한 문제를 해결했는데,
“서로 다른 도메인/산업이 비슷한 문제를 가지고 있지만
크로스 폴리네이션이 일어나지 않는 것처럼 보인다”는 것이다.
Lore가 게임 산업의 경험에서 출발하여 AI/ML 도구 생태계의 교훈을 흡수하거나
그 역방향의 영향을 줄 수 있다면, 버전 관리 문제의 두 번째 해결 시도가
첫 번째 시도의 검증된 설계를 재발명하는 낭비를 피할 수 있다.

Lobste.rs의 rs545837은 잠금이야말로 실제 제품이라고 봤다.
레벨 파일이나 PSD는 병합할 수 없으니 조율이
병합 시점이 아니라 편집 전에 일어나야 하고,
그것이 Perforce가 맞게 한 일이자 Git이 진지하게
다루지 않은 일이라는 것이다.[^rs545837]
반대로 HN의 toobulkeh는 두 아티스트가 조율 없이 같은 에셋을 고친다면
그것은 VCS가 아니라 관리의 문제라고 반박했다.[^toobulkeh]

### 같은 결론에 다른 길로 도착한 Scion

2026년 10월 Anthropic은 사내 모노레포를 Git에서
자체 시스템 [Scion](scion.md)으로 옮겼다고 밝혔다.[^scion]
Lore와 Scion은 출발점이 정반대다.
Lore는 사람(아티스트)이 다루는 대형 바이너리 에셋 때문에,
Scion은 에이전트가 만드는 엄청난 양의 변경 때문에 Git의 한계에 부딪혔다.

그런데도 두 시스템이 고른 설계는 거의 같다.
둘 다 중앙 서버를 정본으로 두고, 저장소를 콘텐츠 주소와 Merkle 트리로 표현하며,
필요한 파일만 가져오는 희소·가상 작업 사본을 기본으로 삼는다.
차이는 클라이언트의 무게다.
Lore는 스테이징, 커밋, 브랜치,
diff를 네트워크 없이 처리하겠다고 하지만,[^lore-faq]
Scion은 커밋, 병합,
리베이스를 모두 서버에서 하고 클라이언트를 얇게 만들었다.[^scion]
사람이 오프라인에서도 일해야 하는 게임 스튜디오와
클라이언트가 정의상 온라인인 에이전트 조직의 차이가 그대로 드러난다.

### 오픈소스 버전 관리는 표준 전쟁이 아직 끝나지 않았다

Git이 모든 경쟁자를 제압했다는 인식이 있지만,
이는 소프트웨어 개발 영역의 이야기다.
게임, 영상, 하드웨어, 바이오인포매틱스는 여전히 Perforce,
Plastic SCM, 독자 시스템에 의존한다.
Lore, Jujutsu, Sapling이 동시에 등장한 것은 우연이 아니다.
Git의 설계 결정들이 새로운 규모와 패턴에서 마찰을 만들기 시작했다는 신호다.

Lore가 흥미로운 이유는 배후에 실제 사용 조직이 있다는 점이다.
UEFN의 수천 명 사용자와 Epic 내부 프로젝트가 검증 대상이다.
학술 프로젝트나 개인 실험이 아닌, 실제 운영 부하 아래 진화하는 시스템이다.
이 검증 기반은 Lore가 단순한 아이디어 수준에서 생존할 가능성을 높인다.

bentt은 이 맥락에서 PlasticSCM의 반면교사를 제시했다.[^bentt]
PlasticSCM은 게임 개발용 VCS로서 좋은 경쟁자였지만, Unity가 인수한 후
오픈소스화 대신 P&L 책임을 부여했다.
그 결과 도구는 생태계 확장 대신 수익화 압력 아래 방치에 가까운 상태가 되었다.
Epic이 오픈소스를 선택한 것은 Unity가 하지 않은 결정이며,
그 대조가 게임 산업 VCS 생태계에서 Lore의 포지셔닝을 더 뚜렷하게 만든다.

### 콘텐츠 주소 저장소와 Merkle 트리는 버전 관리의 표준 기본 요소가 되어가고 있다

Git이 이 조합을 버전 관리에 도입했을 때 혁신적이었다.
이제 Lore, Nix, IPFS, OCI 컨테이너,
Merkle DAG 기반 파일 시스템이 같은 추상화를 공유한다.
이 패턴이 수렴하는 이유가 있다.
콘텐츠 주소화는 중복 제거, 무결성 검증,
캐시 가능성을 단일 메커니즘으로 해결한다.
Merkle 트리는 부분 검증과 구조적 공유를 동시에 제공한다.

Lore가 이 표준 기본 요소 위에 “바이너리 우선”이라는
레이어를 추가한다는 점이 중요하다.
청킹 전략(FastCDC vs 고정 크기), 파티션 기반 접근 제어, 희소 하이드레이션은
기본 요소를 특정 문제 도메인에 맞게 확장하는 방식이다.
다른 도메인이 같은 기본 요소를 다른 방식으로 확장하는 사례들이 나올 것이다.

### 사양 우선 설계는 구현 독점을 방지하는 유일한 방법이다

VCS 도구의 역사는 구현이 사양보다 앞서는 경우가 많았다.
Git은 공식 와이어 프로토콜 사양이 없다가 gitprotocol-v2가 늦게 공식화되었다.
Perforce의 프로토콜은 비공개다.
이 패턴은 도구 주변에 생태계가 형성될수록 구현 독점력이 커지는 구조를 만든다.

Lore가 C 헤더를 정식 인터페이스로 선언하고
온디스크·온와이어 포맷을 명세화하는 것은
초기부터 구현 독점을 차단하려는 설계 결정이다.
이것이 MIT 라이선스만큼 중요하다.
라이선스는 소스를 복사할 권리를 주지만, 명세는 호환 구현을 만들 능력을 준다.
Epic이 방향을 바꾸거나 개발을 중단하더라도
명세 기반 커뮤니티 포크가 가능한 구조다.
오픈소스 지속 가능성의 실질적 보증은 라이선스가 아닌 명세 공개에 있다.

## 도입 결정을 내리는 순서

Lore를 평가할 때는 저장소 크기보다 작업 종류부터 분류한다.
텍스트 코드, 병합 가능한 데이터,
잠금이 필요한 바이너리 에셋의 비중을 따로 센다.
팀이 실제로 가장 자주 겪는 문제가 동기화 시간인지,
충돌인지, 접근 권한인지도 같은 기준으로 기록한다.

그다음 대표 프로젝트의 일부를 복제해
초기 클론, 브랜치 전환, 오프라인 수정,
대용량 파일 복구와 잠금 경쟁을 시험한다.
특히 잠금은 현재 알림 중심이고 확장 가능한 강제 잠금은
로드맵 항목이므로,[^lore-faq][^lore-roadmap]
필요한 작업 흐름을 실제로 막아 주는지 확인하기 전에는
바이너리 제작 파이프라인 전체를 옮기지 않는다.

마지막 관문은 사용자 경험과 되돌릴 수 있는 이전이다.
아티스트가 매일 쓰는 클라이언트,
엔진 플러그인, 권한 모델,
백업에서 복원하는 절차까지 통과해야 한다.
현재 데스크톱 클라이언트는 오픈소스가 아니고
프로젝트는 1.0 이전이므로,[^lore-readme][^lore-roadmap]
도입은 팀 단위 시험과 명확한 복귀 계획을 전제로 해야 한다.

---

[^throw2ih020]: <https://news.ycombinator.com/item?id=48571302>

[^tlahtinen]: <https://news.ycombinator.com/item?id=48572497>

[^swiftcoder]: <https://news.ycombinator.com/item?id=48573464>

[^iceweaselfan44]: <https://news.ycombinator.com/item?id=48571674>

[^pkasting]: <https://news.ycombinator.com/item?id=48572878>

[^fg137]: <https://news.ycombinator.com/item?id=48578289>

[^bentt]: <https://news.ycombinator.com/item?id=48573783>

[^penciltwirler]: <https://news.ycombinator.com/item?id=48571859>

[^asawicki]: Adam Sawicki, [First Look at Epic Games Lore VCS](https://asawicki.info/news_1803_first_look_at_epic_games_lore_vcs), 2026-06-18

[^lore-gh]: GitHub, [EpicGames/lore](https://github.com/EpicGames/lore), 2026-10-14 기준 (저장소 정보, 게시일 없음)

[^lore-readme]: Epic Games, [Lore README](https://github.com/EpicGames/lore/blob/main/README.md), 게시일 표시 없음

[^lore-roadmap]: Epic Games, [Roadmap - Lore Developer Documentation](https://epicgames.github.io/lore/roadmap/), 게시일 표시 없음

[^lore-faq]: Epic Games, [FAQ - Lore Developer Documentation](https://epicgames.github.io/lore/faq/), 게시일 표시 없음

[^p4-edit]: Perforce Software, [p4 edit](https://perforce.com/manuals/cmdref/Content/CmdRef/p4_edit.html), 게시일 표시 없음

[^scion]: Anthropic, [Redesigning source control at Anthropic](https://www.anthropic.com/engineering/redesigning-source-control), 2026-10-13

[^rootlocus]: <https://news.ycombinator.com/item?id=48571375>

[^LugosFergus]: <https://news.ycombinator.com/item?id=48571625>

[^zipy124]: <https://news.ycombinator.com/item?id=48571716>

[^raincole]: <https://news.ycombinator.com/item?id=48574148>

[^tikotus]: <https://news.ycombinator.com/item?id=48581537>

[^akurilin]: <https://news.ycombinator.com/item?id=48573700>

[^dijit]: <https://news.ycombinator.com/item?id=48575595>

[^retroflexzy]: <https://news.ycombinator.com/item?id=48572947>

[^icefox]: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version#c_zbpqf9>

[^sunshowers]: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version#c_qtbmrs>

[^JordiGH]: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version#c_lqafjs>

[^gerikson]: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version#c_zybnwy>

[^rs545837]: <https://lobste.rs/s/r9fmgk/epic_games_announces_lore_version#c_shgnpy>

[^toobulkeh]: <https://news.ycombinator.com/item?id=48580288>
