# Mutagen

> Cloud-based development using your local tools

> Fast file synchronization and network forwarding for remote development

<https://mutagen.io/>

<https://github.com/mutagen-io/mutagen>

## 세팅

용어 정리:
- **Alpha**: 로컬 Mac (내 개발 머신, 코드 작성)
- **Beta**: 원격 Mac (빌드/실행 머신, 성능 좋은 Mac)

1번만 원격 컴퓨터에서 세팅하고 나머지는 로컬 컴퓨터에서 처리합니다.

### 1. 원격 컴퓨터에 원격 로그인 활성화

시스템 설정 > 일반 > 공유 > 원격 로그인 활성화

### 2. Mutagen 설치

```bash
brew install mutagen-io/mutagen/mutagen
```

### 3. SSH 공개키 복사

```bash
ssh-copy-id your-username@192.168.1.100
```

### 4. 프로젝트 폴더로 이동

```bash
cd ~/my-project
```

### 5. 프로젝트 동기화 시작

```bash
mutagen sync create . your-username@192.168.1.100:~/my-project
```

파일 변경사항이 자동으로 양방향 동기화됩니다. 로컬에서 코드를 수정하면 원격에 즉시 반영되고, 원격에서 빌드 결과물이 생성되면 로컬에도 동기화됩니다.

### 6. 동기화 상태 확인

```bash
# 동기화 상태 확인
mutagen sync list

# 상세 정보 확인
mutagen sync list --long

# 실시간 모니터링
mutagen sync monitor
```

## 세션 관리

```bash
# 세션 일시정지 (배터리 절약)
mutagen sync pause --all

# 세션 재개
mutagen sync resume --all

# 모든 세션 종료
mutagen sync terminate --all
```

## Cloud-based Development

Mutagen의 슬로건은
"Cloud-based development using your local tools"입니다.
코드 작성은 로컬 도구로 하되,
빌드와 실행은 원격 환경에서 수행하는 개발 방식을
의미합니다.

### 핵심 개념

전통적인 로컬 개발에서는 코드 작성, 빌드, 실행이
모두 한 머신에서 이루어집니다.
Cloud-based development는 이를 분리합니다:

- **코드 작성**: 로컬 머신의 기존 IDE/에디터 사용
- **빌드/실행**: 원격 서버, 컨테이너,
  클라우드 VM에서 수행
- **연결**: Mutagen이 파일 동기화와
  네트워크 포워딩으로 두 환경을 투명하게 연결

개발자 입장에서는 로컬에서 작업하는 것과
차이가 없습니다.
Mutagen이 동기화와 포워딩을 자동으로 처리하기
때문입니다.

### 왜 Cloud-based Development인가

**환경 일관성.**
"내 컴퓨터에서는 되는데" 문제를 해결합니다.
프로덕션과 동일한 원격 환경에서 실행하므로
환경 차이로 인한 버그를 줄입니다.

**하드웨어 제약 극복.**
빌드와 실행을 성능 좋은 원격 머신에 위임합니다.
로컬 머신의 CPU, 메모리 한계를 넘어설 수 있습니다.

**도구 변경 불필요.**
GitHub Codespaces나 Cloud IDE와 달리
기존에 쓰던 에디터와 터미널을 그대로 사용합니다.
Mutagen은 IDE 플러그인이 아니라
독립적인 인프라 도구입니다.

### 아키텍처: Daemon-Agent 모델

```txt
[로컬 머신]                    [원격 환경]
+----------------+             +----------------+
| IDE/에디터     |             | 서버/컨테이너  |
| 터미널         |             | 빌드/실행 환경 |
+----------------+             +----------------+
        |                              |
+----------------+  ssh/docker  +----------------+
| Mutagen Daemon | <==========> | Mutagen Agent  |
| (로컬 프로세스)|              | (경량 바이너리)|
+----------------+              +----------------+
```

- **Daemon**: 로컬에서 백그라운드로 실행되며
  모든 동기화/포워딩 세션을 관리합니다.
- **Agent**: 원격에 자동 주입되는 경량 바이너리로
  `scp`나 `docker cp`로 복사됩니다.
  별도 설치가 필요 없습니다.
- **통신**: `ssh`나 `docker exec` 같은 기존
  전송 수단을 사용합니다.
  별도 서버 설정이 불필요합니다.

### 파일 동기화 상세

Mutagen의 파일 동기화는 단순한 `rsync`가 아닙니다.

- **양방향 동기화**: 3-way merge로 양쪽
  변경사항을 안전하게 조정합니다.
- **실시간 감지**: 파일시스템 이벤트를 감시하여
  변경 즉시 동기화 사이클이 시작됩니다.
- **차등 전송**: 변경된 부분만 전송하므로
  큰 바이너리 파일도 효율적으로 처리합니다.
- **고성능 해싱**: xxHash(XXH128)를 사용하여
  SHA-1 대비 스캔 시간을 크게 단축합니다.

4가지 동기화 모드를 제공합니다:

- `two-way-safe` (기본값): 양방향 동기화,
  안전한 충돌만 자동 해결
- `two-way-resolved`: 충돌 시 alpha가 우선
- `one-way-safe`: alpha → beta 단방향
- `one-way-replica`: beta가 alpha의 완전 복제본

### 네트워크 포워딩

원격에서 실행 중인 애플리케이션에
로컬처럼 접근할 수 있습니다.

```bash
# 원격의 8080 포트를 로컬 8080으로 포워딩
mutagen forward create \
  tcp:localhost:8080 \
  your-username@192.168.1.100:tcp:localhost:8080
```

- TCP, Unix 도메인 소켓,
  Windows Named Pipe 지원
- 프로토콜 혼합 가능
  (예: 로컬 Unix 소켓 → 원격 TCP)
- 포트를 공개 노출하지 않고 안전하게 접근

### Docker 통합

컨테이너 기반 개발 환경과도 연동됩니다.

```bash
# Docker 컨테이너와 동기화
mutagen sync create . \
  docker://container-name/app/src
```

- **Mutagen Compose**: Docker Compose의
  `x-mutagen` 속성으로 동기화를 선언적 관리
- **Docker Desktop Extension**: macOS에서
  bind mount 성능 문제를 해결
- **직접 세션**: `docker cp`로 agent 주입,
  `docker exec`로 통신

### 다른 도구와의 비교

| 도구                      | 특징                  |
|---------------------------|-----------------------|
| SSHFS                     | 네트워크 지연에 민감  |
| IDE 원격 동기화 (PyCharm) | 브랜치 전환 시 불안정 |
| GitHub Codespaces         | 로컬 도구 사용 불가   |
| Mutagen                   | 로컬 도구 + 원격 실행 |

Mutagen은 기존 워크플로우를 유지하면서
원격 환경의 이점을 취하는 실용적인 선택입니다.
