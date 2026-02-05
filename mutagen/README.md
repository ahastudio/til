# Mutagen

> 로컬 개발 환경을 그대로 유지하면서 원격 서버에서 작업하기

<https://mutagen.io/>

<https://github.com/mutagen-io/mutagen>

## 세팅

```bash
brew install mutagen-io/mutagen/mutagen
```

### 1. SSH 연결 설정

원격 Mac에 SSH로 연결할 수 있도록 설정합니다.

**원격 Mac에서** (동기화 대상):

```bash
# 시스템 설정 > 일반 > 공유 > 원격 로그인 활성화
# 또는 터미널에서:
sudo systemsetup -setremotelogin on
```

**로컬 Mac에서**:

`~/.ssh/config` 파일을 만들어 연결을 간단하게 만듭니다:

```bash
Host remote-mac
    HostName 192.168.1.100
    User your-username
    IdentityFile ~/.ssh/id_rsa
```

이제 `ssh remote-mac`으로 간단하게 접속할 수 있습니다.

SSH 키가 없다면:

```bash
# 키 생성
ssh-keygen -t rsa -b 4096

# 원격 Mac에 공개키 복사
ssh-copy-id remote-mac
```

### 2. 프로젝트 동기화 시작

로컬 프로젝트 폴더를 원격 Mac과 동기화합니다:

```bash
cd ~/my-project
mutagen sync create . remote-mac:~/my-project
```

파일 변경사항이 자동으로 양방향 동기화됩니다. 로컬에서 코드를 수정하면 원격에 즉시 반영되고, 원격에서 빌드 결과물이 생성되면 로컬에도 동기화됩니다.

### 3. 원격 서버 포트 접근

원격에서 실행 중인 웹 서버(예: localhost:3000)를 로컬 브라우저에서 열 수 있습니다:

```bash
mutagen forward create tcp:localhost:3000 remote-mac:tcp:localhost:3000
```

이제 로컬 브라우저에서 `http://localhost:3000`으로 접속하면 원격 서버에 연결됩니다.

### 4. 작업 확인

```bash
# 동기화 상태 확인
mutagen sync list

# 포트 포워딩 상태 확인
mutagen forward list

# 실시간 모니터링
mutagen sync monitor
```

## 프로젝트 설정 파일

매번 명령어를 입력하기 번거롭다면, 프로젝트 루트에 `mutagen.yml` 파일을 만듭니다:

```yaml
sync:
  defaults:
    mode: "two-way-resolved"
    ignore:
      vcs: true
      paths:
        - "node_modules/"
        - ".git/"
        - "*.log"
        - ".DS_Store"
  my-project:
    alpha: "."
    beta: "remote-mac:~/my-project"

forward:
  web-server:
    source: "tcp:localhost:3000"
    destination: "remote-mac:tcp:localhost:3000"
```

이제 한 번에 시작:

```bash
mutagen project start
```

작업 종료:

```bash
mutagen project terminate
```

## 자주 사용하는 명령어

```bash
# 세션 일시정지 (배터리 절약)
mutagen sync pause --all

# 세션 재개
mutagen sync resume --all

# 모든 세션 종료
mutagen sync terminate --all
mutagen forward terminate --all
```

## 팁

### 동기화에서 제외할 파일

프로젝트 루트에 `.mutagen-ignore` 파일 생성:

```
node_modules/
.git/
*.log
.DS_Store
dist/
build/
```

### 충돌 해결

`two-way-resolved` 모드는 최신 파일을 자동으로 선택합니다. 같은 파일을 양쪽에서 동시에 수정하면 나중에 저장된 버전이 반영됩니다.

### 여러 원격 Mac 관리

`~/.ssh/config`에 여러 호스트를 추가:

```
Host work-mac
    HostName 192.168.1.100
    User work-user

Host home-mac
    HostName 192.168.1.200
    User home-user
```

각각 다른 동기화 세션으로 관리할 수 있습니다.
