# Mutagen

> Cloud-based development using your local tools

> Fast file synchronization and network forwarding for remote development

<https://mutagen.io/>

<https://github.com/mutagen-io/mutagen>

## 세팅

용어 정리:
- **로컬 Mac**: 내 개발 머신 (코드 작성)
- **원격 Mac**: 빌드/실행 머신 (성능 좋은 Mac)

1번만 원격 컴퓨터에서 세팅하고 나머지는 로컬 컴퓨터에서 처리합니다.

### 1. 원격 컴퓨터에 원격 로그인 활성화

시스템 설정 > 일반 > 공유 > 원격 로그인 활성화

### 2. Mutagen 설치

Homebrew로 설치:

```bash
brew install mutagen-io/mutagen/mutagen
```

### 3. SSH 공개키 복사

원격 Mac에 공개키 복사:

```bash
ssh-copy-id your-username@192.168.1.100
```

### 4. 프로젝트 폴더로 이동

작업할 프로젝트 폴더로 이동:

```bash
cd ~/my-project
```

### 5. 동기화 제외 파일 설정

프로젝트 루트에 `.mutagen-ignore` 파일 생성:

```
node_modules/
.git/
*.log
.DS_Store
dist/
build/
```

### 6. 프로젝트 동기화 시작

동기화 시작:

```bash
mutagen sync create . your-username@192.168.1.100:~/my-project
```

파일 변경사항이 자동으로 양방향 동기화됩니다. 로컬에서 코드를 수정하면 원격에 즉시 반영되고, 원격에서 빌드 결과물이 생성되면 로컬에도 동기화됩니다.

### 7. 동기화 상태 확인

동기화 상태 확인:

```bash
# 동기화 상태 확인
mutagen sync list

# 실시간 모니터링
mutagen sync monitor
```

## 세션 관리

세션 관리:

```bash
# 세션 일시정지 (배터리 절약)
mutagen sync pause --all

# 세션 재개
mutagen sync resume --all

# 모든 세션 종료
mutagen sync terminate --all
```
