# boring — SSH 터널 관리 CLI

<https://alebeck.github.io/boring/>

<https://github.com/alebeck/boring>

HN 토론: <https://news.ycombinator.com/item?id=41785511> (213점, 67개 댓글)

## 소개

`boring`은 SSH 터널을 관리하기 위한 경량 CLI 도구다.
Go(95.5%)로 작성되었으며 macOS, Windows, Linux를 지원한다.
기존 SSH 설정 파일(`~/.ssh/config`)과 통합되어 별도의 호스트 설정 없이 사용할 수 있고,
백그라운드 데몬 방식으로 동작하여 터널을 열어 둔 채 터미널을 닫아도 유지된다.

자동 재연결과 keep-alive가 핵심 기능이다.
네트워크가 끊기거나 SSH 세션이 종료되면 자동으로 재연결을 시도하며,
`keep_alive` 옵션으로 주기를 설정할 수 있다(기본 120초).
설정은 TOML 파일로 관리한다(`~/.boring.toml`, Linux에서는 `$XDG_CONFIG_HOME/boring/.boring.toml`).

지원하는 포워딩 모드는 네 가지다.

- `local`: 로컬 포트 → 원격 포트 포워딩 (기본값)
- `remote`: 원격 포트 → 로컬 포트 포워딩
- `socks`: 로컬 SOCKS5 동적 포워딩
- `socks-remote`: 원격 SOCKS5 동적 포워딩

## CLI

```text
boring list, l [-g <group>]                          터널 목록 표시
boring open, o (-a | -g <group> | <patterns>...)     터널 열기
boring close, c (-a | -g <group> | <patterns>...)    터널 닫기
boring edit, e                                       설정 파일 편집
boring version, v                                    버전 표시
boring help, h                                       도움말
```

`open`과 `close`에 공통으로 사용하는 플래그:

- `-a`, `--all`: 모든 터널에 적용
- `-g`, `--group <group>`: 특정 그룹의 터널에 적용
- `<patterns>...`: glob 패턴으로 터널 선택

셸 자동완성은 다음과 같이 설정한다.

```bash
# bash
eval "$(boring --shell bash)"

# zsh
source <(boring --shell zsh)

# fish
boring --shell fish | source
```

## 설정

| 옵션          | 설명                                   | 필수 여부                          |
| ------------- | -------------------------------------- | ---------------------------------- |
| `name`        | 터널 별칭                              | 필수                               |
| `local`       | 로컬 주소 (포트 또는 Unix 소켓 경로)   | local/remote/socks 모드에서 필수   |
| `remote`      | 원격 주소                              | local/remote/socks-remote에서 필수 |
| `host`        | SSH 호스트 (설정 별칭 또는 호스트명)   | 필수                               |
| `mode`        | 포워딩 모드                            | 선택 (기본: `local`)               |
| `user`        | SSH 사용자명                           | 선택 (SSH 설정에서 읽음)           |
| `identity`    | SSH 키 경로                            | 선택 (기본값 시도)                 |
| `port`        | SSH 포트                               | 선택 (기본: 22)                    |
| `group`       | 그룹 레이블                            | 선택                               |
| `keep_alive`  | Keep-alive 주기 (초)                   | 선택 (기본: 120)                   |

예시 설정:

```toml
[[tunnels]]
name = "dev"
local = "9000"
remote = "localhost:9000"
host = "dev-server"

[[tunnels]]
name = "prod"
local = "5001"
remote = "localhost:5001"
host = "prod.example.com"
user = "root"
identity = "~/.ssh/id_prod"
group = "production"
```

환경 변수:

| 변수               | 용도                       | 기본값                   |
| ------------------ | -------------------------- | ------------------------ |
| `$BORING_CONFIG`   | 설정 파일 경로             | 플랫폼별 기본 경로       |
| `$BORING_LOG_FILE` | 로그 파일 경로             | `/tmp/boringd.log`       |
| `$BORING_SOCK`     | 데몬 소켓 경로             | `/tmp/boringd.sock`      |
| `$DEBUG`           | 상세 로그 활성화           | 비활성화                 |

## 분석

### 데몬-클라이언트 분리가 터널 영속성 문제를 해결한다

`$BORING_SOCK`과 `$BORING_LOG_FILE` 환경 변수의 존재는 boring이 백그라운드 데몬(`boringd`)과
프론트엔드 CLI 두 개로 구성된다는 것을 드러낸다.
CLI 명령은 Unix 소켓을 통해 데몬에 지시를 보내고, 데몬이 실제 SSH 연결을 유지한다.
이 분리 덕분에 터미널 세션을 닫아도 터널이 끊기지 않는다.

이 구조는 Docker(dockerd + docker CLI)와 동일한 아키텍처 패턴이다.
클라이언트-서버 분리는 단순한 백그라운드 프로세스(`nohup ssh -L ...`)보다 낫다 —
상태 조회(`boring list`), 개별 터널 제어, 로그 수집이 모두 가능해지기 때문이다.
Go가 이 아키텍처를 단일 바이너리로 구현하기에 적합한 이유는 고루틴을 통한 동시 터널 관리와
정적 바이너리 배포가 모두 언어 수준에서 지원되기 때문이다.

perbu는 Go 생태계에서 SSH 구현의 품질이 이 도구를 가능하게 한 핵심 요소라고 지적한다.[^perbu]
`golang.org/x/crypto/ssh`는 Go 표준 라이브러리 확장팩에서 제공하는 SSH 구현으로,
성숙도와 API 설계 면에서 Go의 킬러 피처 중 하나라는 평가다.
`github.com/gliderlabs/ssh`처럼 SSH 서버를 애플리케이션에 내장하는 고수준 추상화도 존재하여,
Go 생태계가 SSH 관련 도구 제작에 특히 적합한 환경임을 보여 준다.

collinvandyck76은 1년간 Rust를 사용하다 boring 코드베이스를 읽으면서 신선한 공기를 느꼈다고 표현한다.[^collinvandyck76]
간결하고 직관적인 레포지토리라는 묘사는 Go와 Rust의 코드 표현력 차이를 드러낸다.
Rust의 소유권 모델과 생명주기 어노테이션은 메모리 안전성을 보장하지만
코드 가독성을 높이는 방향과 항상 일치하지는 않는다.
동시성과 네트워크 I/O가 중심인 도구에서 Go의 고루틴 모델이 코드를 더 직선적으로 만든다는 것을 이 비교가 시사한다.

### SSH 설정 파일 통합이 사용자의 지식 중복을 제거한다

`host` 필드가 SSH 설정 파일의 Host 별칭을 그대로 사용한다는 점은 중요한 설계 결정이다.
사용자는 이미 `~/.ssh/config`에 정의한 호스트 정보를 boring에서 다시 입력할 필요가 없다.
`user`, `identity`, `port` 옵션이 모두 “선택 사항 — SSH 설정에서 읽음”인 것도 같은 원칙에서 온다.

이것은 “기존 도구와 설정을 대체하지 않고 통합한다”는 Unix 철학과 일치한다.
반면 SSH 설정 파일을 전혀 모르는 사용자에게는 이 통합이 불투명하게 느껴질 수도 있다.
boring의 동작을 이해하려면 SSH 설정 파일의 우선순위 규칙까지 알아야 하기 때문이다.

madeforhnyo는 GitHub Issues에서 `$XDG_CONFIG_HOME` 지원을 제안했고, 이 기능이 실제로 구현됐다고 보고한다.[^madeforhnyo]
Linux 사용자가 `~/.boring.toml` 대신 `$XDG_CONFIG_HOME/boring/.boring.toml`을 사용할 수 있게 된 것이다.
이 기여는 boring이 Linux 데스크탑 생태계의 설정 파일 관례를 존중하는 방향으로 진화하고 있음을 보여 준다.
XDG Base Directory 스펙은 홈 디렉토리에 점 파일이 쌓이는 문제를 해결하기 위한 표준인데,
오픈소스 도구가 이 스펙을 채택하는 흐름이 저변에 깔려 있다.

### glob 패턴과 그룹 태깅이 다중 환경 운영을 지원한다

`boring open -g production`으로 production 그룹의 터널을 한 번에 열거나
`boring open “prod*”`로 패턴에 일치하는 터널을 선택하는 기능은
단순한 편의 기능이 아니라 멀티 환경 운영 패턴을 지원한다.
개발, 스테이징, 프로덕션 환경 각각에 그룹을 부여하면
환경 전환이 단일 명령으로 이루어진다.

이 설계는 도구를 단순 SSH 래퍼에서 환경 관리 도구로 격상시킨다.
다만 그룹은 단순 레이블이고 계층 구조나 상속이 없다.
하나의 터널이 여러 그룹에 속하거나, 그룹 간 의존성을 표현하는 방법은 없다.

## 비평

### 재연결 실패 시 동작이 문서화되지 않았다

자동 재연결은 boring의 핵심 차별점인데, 정작 재연결 로직의 상세가 공개되지 않는다.
네트워크가 계속 끊겨 있을 때 얼마나 오래 재시도하는가?
지수 백오프(exponential backoff)를 사용하는가, 아니면 고정 주기인가?
최대 재시도 횟수가 있는가?

이 질문들에 대한 답이 없으면 프로덕션 환경에서 boring을 의존하기 어렵다.
모니터링 도구나 알림이 없는 경우, 터널이 조용히 끊겨 있을 때 사용자가 이를 발견하는 방법은 무엇인가?
`$BORING_LOG_FILE`이 있지만, 실패 상태를 외부 시스템에 노출하는 메커니즘은 보이지 않는다.

jaimehrubiks는 HN 댓글에서 이 질문을 정확히 제기한다.[^jaimehrubiks]
서버가 다운된 상태에서 즉시 재시도를 반복하면 CPU 스파이크가 발생할 수 있다는 것이다.
지수 백오프 없이 재시도하는 도구는 네트워크 장애 상황에서 오히려 시스템 부하를 증가시킨다.
boring이 내부적으로 어떤 재시도 전략을 구현하는지 소스코드를 직접 확인해야 알 수 있는 상황이다.

### socks-remote 모드의 실제 용도가 문서에서 불명확하다

네 가지 포워딩 모드 중 `socks-remote`는 가장 설명이 부족하다.
`socks` 모드(로컬 SOCKS5)는 일반적으로 로컬 브라우저 등이 SSH 서버를 통해 나가는 트래픽을 프록시할 때 쓴다.
`socks-remote`가 이와 어떻게 다르고 어떤 시나리오에서 필요한지 README는 설명하지 않는다.

기능이 있다는 것만 알고 어떤 상황에서 써야 하는지 모르는 사용자는 이 모드를 발견하지 못할 것이다.
문서에 각 모드의 전형적 사용 사례가 한 문장씩이라도 있었다면 실용성이 크게 올라갈 것이다.

### Go 관용구를 따르지 않는 코드 패턴이 유지보수성을 낮춘다

coumbaya는 boring의 코드베이스에서 Go 관용구(idiom)를 벗어난 패턴을 여러 가지 지적한다.[^coumbaya]
전역 가변 변수(mutable global variables) 사용, 그레이스풀 셧다운을 위한 `signal.NotifyContext` 미사용,
컨텍스트를 전달하지 않는 `Dial` 대신 `DialContext` 미사용,
고루틴 에러 처리를 위한 `errGroup` 미사용이 구체적인 지적 사항이다.

이 비판은 코드가 “작동한다”는 것과 “Go스럽다”는 것이 다름을 드러낸다.
collinvandyck76이 “신선한 공기”라고 표현한 간결함은 언어 레벨의 관용구 준수와 별개의 차원이다.
코드가 짧고 읽기 쉽더라도, 언어가 제공하는 에러 처리 및 동시성 패턴을 우회하면
나중에 이를 수정하는 기여자가 예상치 못한 곳에서 막히게 된다.
“학습용 Go 프로젝트”라는 출발점이 이 패턴들을 설명하지만, 정당화하지는 않는다.

### Unix 소켓 기반 데몬은 Windows에서 다르게 동작해야 한다

`$BORING_SOCK`의 기본값이 `/tmp/boringd.sock`이고,
`$BORING_LOG_FILE`의 기본값이 `/tmp/boringd.log`다.
이 경로는 Unix 관례이며, Windows에서는 Named Pipe나 다른 IPC 메커니즘이 필요하다.
Windows 빌드가 별도의 `.bat` 파일로 분리된 것은 Windows 지원이 후순위임을 시사한다.

“Cross-Platform: Supports macOS, Windows, and Linux”라고 명시하지만,
데몬 아키텍처의 Windows 구현이 Unix와 동일한 방식으로 작동하는지는 불분명하다.
Windows 사용자가 boring을 도입하기 전에 실제 동작을 검증해야 할 여지가 있다.

## 인사이트

### SSH 터널 도구의 진짜 가치는 연결 끊김 회복에 있다

`ssh -L 9000:localhost:9000 dev-server`를 직접 실행하는 것 대비 boring이 추가하는 가치는
포트 포워딩 기능 자체가 아니라 연결 끊김 이후의 자동 회복이다.
장기 실행 터널의 가장 흔한 실패 지점은 네트워크 일시 단절, 노트북 절전 모드 복귀, SSH 서버 재시작이다.
이 모든 상황에서 수동으로 재연결하는 것이 SSH 터널 사용의 핵심 불편이었다.

boring은 이 불편을 인프라 수준에서 해결한다.
알림도 없고 사용자 개입도 없이 터널이 회복된다는 것은,
SSH 터널이 임시 수단이 아니라 신뢰할 수 있는 인프라 구성 요소가 될 수 있다는 뜻이다.
이 신뢰성이 확보되면 SSH 터널을 기반으로 한 아키텍처 결정의 폭이 넓어진다.

### SSH 터널 관리는 서비스 메시가 없는 환경의 현실적 대안이다

Kubernetes + Istio 또는 Consul 같은 서비스 메시는 마이크로서비스 간 보안 통신을 자동화하지만,
이 스택을 도입할 여건이 없는 팀은 SSH 터널로 같은 목표를 달성한다.
boring처럼 다중 터널을 그룹으로 관리하고 자동 재연결을 보장하는 도구는
이 중간 지대의 팀에게 서비스 메시의 운영 복잡도 없이 유사한 보안 통신을 가능하게 한다.

물론 SSH 터널은 서비스 메시가 제공하는 트래픽 관찰 가능성(observability), 세밀한 접근 제어,
로드 밸런싱을 제공하지 않는다.
boring의 적절한 사용 영역은 소규모 팀, 내부 개발 환경, 레거시 인프라와의 임시 연결이다.
서비스 메시로 가는 길목에서 “지금 당장 작동하는 무언가”로서의 위치다.

### TOML 설정 + CLI 패턴은 반복 수동 작업을 자동화하는 최소 추상화다

`boring open -a`로 모든 터널을 한 번에 여는 것은 작은 기능처럼 보이지만,
매일 아침 로그인하면서 개발 환경을 세팅하는 반복 작업을 하나의 명령으로 줄인다.
TOML 파일이 인프라를 코드로(infrastructure as code) 관리하는 방식과 통합되면,
버전 관리 저장소에 커밋된 `.boring.toml`이 팀의 공유 터널 설정이 된다.

이 패턴의 확장 방향은 시작 스크립트나 셸 설정 파일과의 통합이다.
`boring open -a`를 `.zshrc`나 `tmux` 세션 초기화 스크립트에 넣으면
개발 환경이 터미널을 열 때마다 자동으로 준비된다.
이 수준의 자동화는 boring 자체의 기능이 아니라 Unix 도구 조합에서 나오는 이차 효과다.

---

[^perbu]: <https://news.ycombinator.com/item?id=41787958>
[^collinvandyck76]: <https://news.ycombinator.com/item?id=41789097>
[^madeforhnyo]: <https://news.ycombinator.com/item?id=41786827>
[^jaimehrubiks]: <https://news.ycombinator.com/item?id=41788422>
[^coumbaya]: <https://news.ycombinator.com/item?id=41795969>
