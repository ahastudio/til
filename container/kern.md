# kern: 데몬 없이 밀리초 단위로 컨테이너를 띄우는 rootless 런타임이자 에이전트 샌드박스

<https://getkern.dev>

<https://github.com/getkern/kern>

Show HN: [Kern – container and resource runtime in a 1.5 MB binary, no daemon](https://news.ycombinator.com/item?id=49423927)

GN 토론: <https://news.hada.io/topic?id=36200>

## 소개

kern은 데몬이 없고 root 권한이 필요 없는 컨테이너 런타임이다.
정적 바이너리 하나로 배포되며, README는 같은 바이너리가 에이전트가 쓴 코드를
돌리는 샌드박스이기도 하다고 설명한다.
kern은 컨테이너를 box라고 부른다.
Hacker News에서 jeffbee는 제목의 container runtime이 CRI 구현으로 읽힐 수 있다고
짚었다.[^jeffbee]
realexweb은 CRI가 아니라고 인정하며, README의 한계 절에 쿠버네티스 런타임이
아니고 containerd나 CRI-O를 쓰라고 적혀 있다고 답했다.[^realexweb-cri]
그가 말한 runtime은 pull, build, 수명 주기를 한 바이너리에 담은 docker나 podman
의미다.[^realexweb-cri]
저장소의 한 줄 설명은 에이전트의 도구 호출과 LLM이 생성한 코드를 커널이 강제하는
컨테이너에서 실행한다는 것이다.

README가 내세우는 특징은 다음과 같다.
OCI 이미지를 `pull`, `build`, `commit`, `push`, `save`와 `load`로 다루고,
box는 한 자릿수 밀리초에 시작한다.
`docker-compose.yml`을 고치지 않고 쓰거나 kern 고유의 `stack.toml`을 쓴다.
`kern run`은 샌드박스 없이 호스트의 일반 프로세스에 같은 자원 한도를 건다.
Python과 Node용 SDK(`kern-sandbox`)와 MCP 서버를 제공하고,
README는 MCP 서버가 Claude Code, Cursor, Claude Desktop,
LM Studio에서 쓸 수 있다고 적는다.

저장소는 2026년 7월 18일에 만들어졌고, 마지막 푸시는 2026년 11월 1일이다.
기록 시점에 스타는 460개, 포크는 12개, 열린 이슈는 0개였고, 주 언어는 Rust,
라이선스는 Apache-2.0이다.[^api]
홈페이지는 Linux(x86_64와 ARM), WSL2를 통한 Windows,
Linux VM을 통한 macOS에서 돈다고 소개한다.
홈페이지에는 직접 써 볼 수 있는 데모나 플레이그라운드로 가는 링크가 없고,
README의 시연은 터미널 녹화 GIF다.

## 설치하기

Linux는 설치 스크립트 한 줄이다.

```bash
curl -fsSL https://raw.githubusercontent.com/getkern/kern/main/install.sh | sh
```

Windows는 WSL2를 거치는 PowerShell 스크립트(`install.ps1`)다.
macOS에는 네이티브 `kern`이 없고, `colima`로 Linux VM을 띄우고 그 안에서 같은
스크립트를 실행한다.
Kern Sandbox도 VM 안에서 쓰고, 그것을 호출하는 코드도 VM 안에서 돌려야 한다.
설치한 뒤 `kern doctor`가 호스트를 점검하고 고칠 것을 알려 준다.
README는 Ubuntu 23.10 이상에서 먼저 root 권한의 설정 단계가 하나
필요하다고 안내한다.
이 문서를 쓴 환경은 macOS여서 설치와 실행은 직접 해 보지 않았고,
`install.sh`의 내용도 읽지 않았다.
소스에서 빌드하려면 패키지 이름을 줘야 한다고 프로젝트를 소개한 realexweb이
Hacker News에서 안내했다.
저장소에는 바이너리가 있는 패키지가 CLI, fuzz 하네스,
Windows 셈(shim) 세 개라서 이름 없이 `cargo install`을 하면 어느 것인지 가릴 수
없다는 것이다.[^realexweb-cri]

```bash
cargo install --git https://github.com/getkern/kern getkern --locked
```

같은 댓글은 소스 빌드가 1.91 MB이고 제목의 1.5 MB는 CI가 고정된 nightly 도구
체인과 `build-std`, `optimize_for_size`,
`opt-level="z"` 프로필로 만든 릴리스 바이너리의 크기라고 밝힌다.[^realexweb-cri]

## 빠른 시작

README의 빠른 시작 표는 네 가지 명령을 보여 준다.

| 하는 일                        | 명령                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------ |
| 실제 OCI 이미지의 셸           | `kern box dev --image alpine -it -- sh`                                                          |
| 호스트에 포트를 연 서비스      | `kern box svc --image nginx:alpine -d -p 8080:80`                                                |
| 엄격한 프로필의 신뢰 못할 코드 | `kern box job --image python:3.12-slim --security-profile untrusted -- python3 -c "print('hi')"` |
| 실행 중인 것(`--json`도 가능)  | `kern ps`                                                                                        |

`--security-profile untrusted`는 seccomp allowlist, `--cap-drop ALL`,
`--read-only`를 한 번에 켜는 플래그다.
여러 서비스는 `stack.toml`에 서비스마다 표(table) 하나를 적고 `kern compose
stack.toml up`으로 올린다.
서비스마다 자기 네트워크 네임스페이스를 갖고 서로 이름으로 닿는다.

## Kern Sandbox로 에이전트의 코드 돌리기

Python에서는 호출 한 번이 컨테이너 하나다.

```python
import kern_sandbox as kern

r = kern.run_code("print(sum(range(100)))")
print(r.stdout, r.fault)   # 4950  None
```

코드는 호출 한 번 동안, 또는 세션 내내 자기 컨테이너 안에서 돌고,
타임아웃이나 메모리 부족은 형식이 있는 `fault`로 돌아온다고 README는 적는다.
Linux에서는 `pip install kern-sandbox`가 kern을 함께 가져오고,
Node는 `npm install kern-sandbox`다.

MCP 서버는 같은 블록을 `claude_desktop_config.json`,
Cursor와 LM Studio의 `mcp.json`, Claude Code의 프로젝트 루트
`.mcp.json`에 넣는다.

```json
{
  "mcpServers": {
    "kern": { "command": "uvx", "args": ["--from", "kern-sandbox", "kern-mcp"] }
  }
}
```

## 격리가 하는 일

SECURITY.md는 지금 강제되는 것을 이렇게 나열한다.
user, PID, network(loopback만), UTS, IPC, mount 네임스페이스를 쓰고,
이미지 캐시를 읽기 전용 하위 레이어로 둔 overlay 루트에 `pivot_root`한다.
위험한 capability 16개를 exec 직전에 effective, permitted, inheritable, ambient,
bounding 집합에서 모두 뺀다.
seccomp는 항상 켜져 있고 기본이 allowlist이며,
moby의 기본 필터에서 35개 탈출 syscall을 뺀 것이다.
35개 중 24개는 호출자를 `SIGSYS`로 즉시 죽이고 11개는 `ENOSYS`를 돌려준다.
`/dev`는 새 tmpfs에 `null`, `zero`, `full`, `random`,
`urandom`만 연결한 deny-by-default이고, cgroup v2 한도가 걸린다.

Landlock 쓰기 허용 목록과 `--egress-allow` 필터링 프록시는 선택 기능이다.
SDK의 네트워크 설정은 세 가지이고 기본값은 없다. `egress_allow=[...]`는 이름
붙인 호스트만 열고, `network=True`는 호스트 loopback과 그 위의 서비스까지 호스트
네트워크를 공유한다.
SDK는 호스트의 `.ssh`, `.aws`, `.kube` 등 이름이 정해진 자격 증명 디렉터리
17개와 kern 자신의 상태를 마운트하는 것을 옵트아웃 없이 거부하고,
호출자의 환경 변수를 상속하지 않는다고 SECURITY.md는 적는다.

## 속도 읽기

BENCHMARKS.md의 기준은 Intel i7-14700KF, Linux 7.0.0에서 2026년 9월 20일에 잰,
이미지가 이미 로컬에 있는 `/bin/true` 하나다.

| 런타임              | 컨테이너 하나 | 200개 동시 | 시작마다 하는 일                                                          |
| ------------------- | ------------- | ---------- | ------------------------------------------------------------------------- |
| kern `box --rootfs` | 2.7 ms        | 0.10 s     | 네임스페이스, overlay, `pivot_root`, seccomp allowlist, 메모리와 PID 한도 |
| kern `box --image`  | 3.6 ms        | 0.12 s     | 같음, 더해서 OCI 이미지를 overlay로 풂                                    |
| bubblewrap          | 2.7 ms        | 0.15 s     | 네임스페이스와 bind mount, seccomp와 cgroup 한도 없음                     |
| runc(rootless)      | 13.2 ms       | 0.32 s     | OCI 런타임, 보통 위의 엔진이 구동                                         |
| podman `run --rm`   | 288 ms        | 43.6 s     | 매번 `conmon`과 전체 OCI 스택을 fork                                      |
| docker `run --rm`   | 294 ms        | 16.6 s     | 클라이언트, 데몬 왕복, containerd, runc                                   |

README는 이 표에서 `docker run --rm`보다 80배, 동시 200개에서는 130배,
rootless `runc`보다 3.6배 빠르다고 요약한다.
BENCHMARKS.md는 스스로 한계를 길게 적는다.
3.6 ms는 그날 34번 잰 것 중 가장 빠른 값이고 중앙값은 4.05 ms이며, 바쁜 기계에서는 4 ms에 가깝게 읽어야 한다.
표의 모든 줄은 이미지가 로컬에 있는 상태이고,
처음 실행에서는 레지스트리 pull이 거의 전부다. `alpine:3.19`를 가져와 푸는 데
kern으로 11.06초에서 12.14초, docker로 9.98초에서 10.77초가 걸렸다.
pod 안의 box는 2.59 ms지만 user와 network 네임스페이스를 공유하는 다른
작업이어서 같은 줄에 놓을 수 없다고 한다.
`python:3.12-slim`에서 표준 라이브러리 모듈 두 개를 가져오는 `run_code`는 46.82
ms이고, 바이트코드를 미리 컴파일하면 17.66 ms가 된다.
가장 큰 비용은 box가 아니라 이미지의 파이썬이라는 것이 문서의 결론이다.
GeekNews의 florian13은 80배라는 차이가 이미지가 이미 로컬에 있을 때에만 성립하는 비교로 보이고, 이미지를 처음 풀어야 하는 첫 도구 호출은 이 수치에 잡히지 않은 비용을 따로 치른다고 적었다.[^florian13]
BENCHMARKS.md는 같은 한계를 스스로 적고 있어서 이 지적은 문서가 숨긴 것이 아니라
표 바깥의 비용을 짚은 것이다.
Hacker News에서 sdageltc가 캐시 없는 단일 파이썬 명령의 콜드 스타트를 묻자,
realexweb은 이미지를 이미 받은 경우와 받지 않은 경우를 나눠 답했다.[^sdageltc]
받은 경우 alpine에서 `/bin/sh -c 'echo hi'`는 100번 평균 3.73 ms로 명령을 얹어도
시간이 늘지 않고, `python:3.12-slim`에서 `python3 -c 'print(1)'`은 15.6 ms이며
그중 약 12 ms가 CPython 기동이라고 한다.[^realexweb-cold]
받지 않은 경우 pull이 지배해서 자신의 연결에서 alpine이 2.7초,
`python:3.12-slim`이 41 MB에 9.0초였다고 한다.[^realexweb-cold]
BENCHMARKS.md의 alpine pull 11초대와 달리 이 값은 다른 시점과 연결에서 잰
것이어서, pull 시간은 네트워크가 정한다는 점만 공통이다.

## 비평

### 경계의 안쪽은 호스트 커널이다

README의 한 줄 설명은 커널이 강제하는 컨테이너를 내세운다.
SECURITY.md는 그 경계의 공격 면이 호스트 커널이라서 커널 권한 상승 버그가 곧
탈출이라고 인정하고, 권한 없는(unprivileged) user 네임스페이스 자체가 커널 공격
면이며 과거 권한 상승 CVE의 주요 출처였다고 적는다.
그래서 문서는 코드가 내 것이거나 반쯤 믿을 만할 때는 kern을,
낯선 사람의 적대적 다중 테넌트 코드에는 microVM(Firecracker,
Kata)이나 gVisor를 권한다.
kern의 microVM 계층은 로드맵의 “개발 중”에 있고 아직 없다.
LLM이 생성한 코드를 돌리는 용도가 이 두 경우 중 어디인지는 사용자가 정해야 한다.
Hacker News에서 chrisweekly가 microVM인 smolvm과의 차이를 묻자 realexweb은
smolvm은 microVM이고 kern은 평범한 OS 수준 격리라고
답했다.[^chrisweekly][^realexweb-smolvm]

### 프롬프트 인젝션을 당한 에이전트는 격리로 막히지 않는다

SECURITY.md는 위협을 둘로 나눈다.
오염된 의존성은 파일시스템과 네트워크 제한으로 가두지만,
프롬프트 인젝션을 당한 에이전트는 시킨 코드를 정확히 그대로 실행하므로 격리가
도움이 되지 않는다고 문서가 직접 말한다.
방어는 자격 증명이 box 안에 아예 없게 하는 것이고,
`network=True`는 호스트 loopback의 서비스까지 열어 버린다.
그래서 이 도구의 안전은 기본값을 쓰는지, `env=`로 무엇을 넘기는지,
네트워크를 어떻게 여는지에 달려 있다.

### 속도의 비교 대상이 서로 같은 일을 하지 않는다

80배는 `docker run --rm`을 기준으로 한 값이고,
이 줄은 클라이언트와 데몬 왕복과 containerd와 runc를 모두 거친다.
같은 표에서 bubblewrap은 2.7 ms로 kern의 `--rootfs`와 같고,
차이는 kern이 seccomp와 cgroup 한도를 더 한다는 데 있다.
빠르다는 말이 의미를 가지려면 비교 대상이 같은 일을 하는지 보아야 하고,
문서도 표에 “시작마다 하는 일” 열을 두어 그것을 드러낸다.
측정은 한 대의 데스크톱에서 하루 동안 한 것이어서 다른 하드웨어의
값은 알 수 없다.

### 프로젝트는 아직 어리다

저장소를 만든 지 석 달 남짓이고, 이름이 적힌 관리자는 한 사람이다.[^api]
열린 이슈가 0개인 것이 모두 해결되었다는 뜻인지 쓰는 사람이 적다는 뜻인지는
저장소 정보만으로 가릴 수 없다.
GPU는 box에 카드 전체를 넘길 뿐 나누거나 제한하지 않고,
SECURITY.md는 그래서 GPU를 보안 범위 밖으로 둔다.

## 체크리스트

- [ ] 돌릴 코드가 내가 쓴 것인가, 반쯤 믿을 만한가, 낯선 사람의 것인가
- [ ] 낯선 사람의 적대적 코드라면 microVM이나 gVisor가 필요하지는 않은가
- [ ] 호스트가 Linux이거나 WSL2나 Linux VM을 쓸 수 있는가(macOS는 VM 안에서만)
- [ ] `install.sh`를 파이프로 바로 실행하기 전에 내용을 읽었는가
- [ ] 설치 뒤 `kern doctor`가 고치라는 것이 없는가
- [ ] cgroup 위임이 없는 호스트에서 한도가 실제로 걸리는지 `--require-limits`로 확인했는가
- [ ] SDK에서 `network=True`를 쓰지 않았는가, `env=`로 넘기는 값에 비밀이 없는가
- [ ] 속도는 내 하드웨어에서 BENCHMARKS.md의 재현 명령으로 다시 쟀는가

---

[^jeffbee]: <https://news.ycombinator.com/item?id=49425236>

[^realexweb-cri]: <https://news.ycombinator.com/item?id=49425378>

[^chrisweekly]: <https://news.ycombinator.com/item?id=49426104>

[^realexweb-smolvm]: <https://news.ycombinator.com/item?id=49426199>

[^sdageltc]: <https://news.ycombinator.com/item?id=49432491>

[^realexweb-cold]: <https://news.ycombinator.com/item?id=49432664>

[^florian13]: <https://news.hada.io/topic?id=36200#cid68770>

[^api]: GitHub, [REST API: getkern/kern](https://api.github.com/repos/getkern/kern)
