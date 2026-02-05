# Mutagen

> Cloud-based development using your local tools

> Fast file synchronization and network forwarding for remote development

<https://mutagen.io/>

<https://github.com/mutagen-io/mutagen>

## 설치(Installation)

### macOS

```bash
brew install mutagen-io/mutagen/mutagen
```

### Linux/Windows

<https://github.com/mutagen-io/mutagen/releases>에서 바이너리 다운로드

## 기본 사용법(Basic Usage)

### 파일 동기화(File Sync)

로컬과 원격 서버 간 파일 동기화:

```bash
# 동기화 세션 생성
mutagen sync create <로컬경로> <사용자>@<호스트>:<원격경로>

# 예시
mutagen sync create ~/project user@example.com:~/project
```

### 포트 포워딩(Port Forwarding)

원격 서버의 포트를 로컬에서 접근:

```bash
# 포워딩 세션 생성
mutagen forward create <로컬포트> <사용자>@<호스트>:<원격포트>

# 예시 (원격 3000번 포트를 로컬 3000번으로)
mutagen forward create tcp:localhost:3000 user@example.com:tcp:localhost:3000
```

## 주요 명령어(Key Commands)

```bash
# 모든 세션 목록 확인
mutagen sync list
mutagen forward list

# 세션 상태 모니터링
mutagen sync monitor

# 세션 일시정지/재개
mutagen sync pause <세션명>
mutagen sync resume <세션명>

# 세션 종료
mutagen sync terminate <세션명>
mutagen forward terminate <세션명>

# 모든 세션 종료
mutagen sync terminate --all
mutagen forward terminate --all
```

## 설정 파일(Configuration)

프로젝트 루트에 `mutagen.yml` 파일로 설정 관리:

```yaml
sync:
  defaults:
    ignore:
      vcs: true
      paths:
        - "node_modules/"
        - ".git/"
        - "*.log"
  project:
    alpha: "."
    beta: "user@example.com:~/project"
    mode: "two-way-resolved"
```

설정 파일을 사용한 세션 생성:

```bash
mutagen project start
```

## 유용한 팁(Tips)

- **성능**: `.mutagen-ignore` 파일로 불필요한 파일 제외
- **충돌 해결**: `two-way-resolved` 모드는 최신 파일 우선
- **SSH 설정**: `~/.ssh/config`에 호스트 별칭 설정하면 편리
