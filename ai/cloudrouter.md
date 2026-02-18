# CloudRouter

<https://cloudrouter.dev/>

AI 코딩 에이전트(Claude Code, Codex 등)에게
자체 머신을 제공하는 도구.
에이전트가 VM을 시작하고, 프로젝트 파일을 업로드하고,
명령을 실행하고, 작업이 끝나면 정리까지 수행한다.

> "에이전트에게 자신만의 머신을 주는
> 프리미티브(primitive)."

## 주요 기능

- **VM/GPU 프로비저닝**: 클라우드 VM과 GPU를 즉시 생성.
  T4부터 H100, B200까지 다양한 GPU를 지원하고,
  `--gpu H100:2`처럼 멀티 GPU도 가능하다.
- **다중 프로바이더**: E2B(Docker 샌드박스)와
  Modal(GPU 워크로드)을 하나의 CLI로 통합.
- **브라우저 자동화**: Chrome CDP 내장으로
  페이지 탐색, 클릭, 스크린샷 촬영 가능.
- **VS Code/VNC**: 브라우저에서 에디터와
  데스크톱 환경에 접근.
- **파일 동기화**: 로컬과 샌드박스 간
  자동 파일 동기화.

## 사용 방법

Claude Code Skill로 설치하여
`/cloudrouter` 또는 `/cr`로 호출한다.

```bash
cloudrouter start        # VM 시작
cloudrouter ssh <id>     # SSH 접속
cloudrouter code <id>    # VS Code 열기
cloudrouter vnc <id>     # VNC 데스크톱
cloudrouter browser      # 브라우저 자동화
cloudrouter stop <id>    # VM 중지
```

## 사이즈 프리셋

| 사이즈 | vCPU | RAM   | 디스크 |
|--------|------|-------|--------|
| small  | 2    | 8 GB  | 20 GB  |
| medium | 4    | 16 GB | 40 GB  |
| large  | 8    | 32 GB | 80 GB  |
| xlarge | 16   | 64 GB | 160 GB |

기본값은 `large`.

## 인사이트

### 로컬 CLI와 클라우드 에이전트의 간극

Claude Code는 로컬 터미널에서 실시간 협업하고,
Devin은 클라우드 샌드박스에서 자율적으로 동작한다.
CloudRouter는 로컬 CLI 에이전트에게
클라우드 환경을 제공하여 이 둘의 장점을 결합한다.
실시간 협업을 유지하면서도 무거운 빌드,
GPU 연산, 브라우저 테스트를
원격 환경으로 분리할 수 있다.

### 프로바이더 추상화

E2B와 Modal이라는 서로 다른 특성의 프로바이더를
하나의 CLI로 통합한 점이 실용적이다.
E2B는 빠른 Docker 샌드박스(150ms 이하 콜드 스타트),
Modal은 GPU 워크로드에 적합하다.
사용자는 프로바이더를 의식하지 않고
용도에 맞는 환경을 바로 띄울 수 있다.

### 병렬 에이전트 실행

에이전트가 자체 VM을 가지면
여러 에이전트를 병렬로 실행할 수 있다.
각 에이전트가 독립된 환경에서 작업하므로
충돌 없이 다수의 작업을 동시에 진행 가능하다.
로컬 머신의 자원 제약에서도 벗어난다.

## 기술 정보

- MIT 라이선스
- Go로 작성
- npm 패키지로 배포 (macOS, Linux, Windows)

## Show HN

[Skill that lets Claude Code/Codex spin up VMs and GPUs](https://news.ycombinator.com/item?id=47006393)
