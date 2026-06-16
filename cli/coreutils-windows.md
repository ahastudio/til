# Coreutils for Windows

<https://github.com/microsoft/coreutils>

GeekNews: <https://news.hada.io/topic?id=30522>

HN 토론: <https://news.ycombinator.com/item?id=48372853> (227점, 247개 댓글)

## 소개

마이크로소프트가 공개한 Windows용 UNIX 스타일 핵심 유틸리티 모음이다.
Linux, macOS, WSL에서 사용하는 것과 동일한 명령어와 파이프라인을 Windows 네이티브 환경에서 그대로 실행할 수 있도록 한다.
uutils/coreutils, findutils, grep을 하나의 멀티콜 바이너리로 패키징했다.

현재 프리뷰(preview) 상태이며 MIT 라이선스로 공개됐다.
Rust, PowerShell, Inno Setup으로 구현됐다.

## 설치 및 요구 사항

```bash
# WinGet으로 설치
winget install Microsoft.Coreutils
```

또는 릴리스 페이지에서 바이너리를 직접 다운로드할 수 있다.

**요구 사항:**

- PowerShell 7.4 이상 (7.6 이상 권장, 틸드 지원을 위해)
- 심볼릭 링크 생성 시 개발자 모드 또는 관리자 권한 필요

## 주요 기능

- **플랫폼 간 명령어 일관성**: 동일한 명령어, 플래그, 파이프라인이 수정 없이 동작한다.
- **단일 바이너리**: `ls`, `grep`, `find`, `cat`, `awk`, `sed` 등이 하나의 실행 파일에 포함된다.
- **PSReadLine 통합**: PowerShell과의 개선된 파싱 통합을 제공한다.

## 제한 사항

Windows의 운영 체제 차이로 인한 제약이 있다.

**사용 불가 명령어**: 이름 충돌(`dir`, `kill`, `more`, `whoami`) 또는 Windows 비호환성으로 일부 명령어를 제공하지 않는다.

**환경 차이:**

- `/dev/null` 대신 `NUL` 사용
- POSIX 시그널 없음 (Ctrl+C 제외)
- POSIX 비트 대신 ACL 기반 권한
- `/`와 `\` 경로 구분자 모두 지원

## 분석

### uutils/coreutils 기반의 선택

마이크로소프트가 GNU coreutils를 직접 포팅하지 않고 Rust로 작성된 uutils/coreutils를 기반으로 선택한 것은 의미 있다.
Rust는 메모리 안전성과 크로스 컴파일 지원이 강점이다.
GPL 라이선스인 GNU coreutils보다 MIT 라이선스인 uutils/coreutils를 사용하면 라이선스 호환성 문제를 피할 수 있다.

이 선택은 마이크로소프트가 Rust를 Windows 핵심 도구의 구현 언어로 진지하게 채택하고 있음을 보여주는 또 다른 사례다.
Windows 커널 구성 요소 일부가 Rust로 재작성되는 프로젝트와 같은 방향이다.

다만 HN에서는 더 근본적인 의문이 제기됐다.
upstream인 uutils/coreutils는 이미 Linux, macOS, wasm과 함께 Windows를 지원하는데, 왜 별도 포크가 필요하냐는 것이다.[^testdelacc1]
실제 차이는 몇 가지 Windows 전용 수정에 불과해 upstream으로 병합될 수 있어 보인다는 지적이다.
마이크로소프트라는 주체가 직접 유지보수한다는 점은 신뢰를 주지만, 기술적 신규성은 크지 않다는 평가다.

흥미로운 재해석도 있었다.
한 사용자는 이 도구의 진짜 동기가 AI 에이전트를 Windows에서 더 잘 동작시키려는 데 있을 수 있다고 추측했다.[^fabiensanglard]
에이전트가 Linux/macOS에서 학습한 셸 명령을 Windows에서도 그대로 실행하려면 네이티브 coreutils가 유용하다는 관점이다.

### WSL이 아닌 네이티브 접근

WSL(Windows Subsystem for Linux)이 이미 존재함에도 불구하고 네이티브 Windows 바이너리를 만든 것은 중요한 차이를 만든다.
WSL은 Linux 파일 시스템 경계, 성능 오버헤드, 상호 운용성 제약이 있다.
네이티브 바이너리는 Windows 파일 시스템, 프로세스 모델, 환경 변수와 완전히 통합된다.

크로스 플랫폼 CI/CD 파이프라인이나 Windows 서버에서 실행되는 배포 스크립트에서 이 차이가 가장 크게 느껴진다.

## 비평

### 절반의 해결책

“동일한 명령어와 파이프라인을 수정 없이 실행”이라는 약속은 제한 사항 목록과 충돌한다.
`kill`, `whoami`, `dir`, `more`가 빠져 있고, POSIX 시그널을 지원하지 않으며, `/dev/null`이 다르게 동작한다.

실제 크로스 플랫폼 스크립트에서 이 차이들은 예상치 못한 곳에서 문제를 일으킨다.
POSIX 환경을 기대하는 스크립트를 “수정 없이” Windows에서 실행한다는 약속은 과장일 수 있다.

HN 사용자들은 이름 충돌 처리 규칙 자체가 일관성이 없다고 비판했다.
어떤 coreutils 명령이 실제로 실행될지가 셸 종류, PATH 순서, PowerShell 별칭 테이블에 따라 달라져 사용자가 매번 추측해야 한다는 것이다.[^pjmlp]
또 `dir`는 충돌로 빠졌는데 `echo`와 `rmdir`는 충돌에도 포함됐고 `sort`는 충돌이 아니라고 판단된 기준이 무엇이냐는 지적도 나왔다.[^dataflow]
`find` 역시 모든 Windows NT 계열 OS에 `System32\find.exe`가 존재하는데도 충돌로 표기되지 않았고,
findutils의 `find`는 텍스트 검색용 DOS `find`와 기능적으로 전혀 다르다는 점이 함께 지적됐다.[^EvanAnderson]
이런 사례들은 "절반의 해결책"이라는 비판을 구체적으로 뒷받침한다.

성능 측면의 우려도 있었다.
한 사용자는 Windows에서 가장 느린 단계가 프로세스 생성이라며,
프로세스를 재사용해 여러 명령을 이어 실행하지 않는 한 Unix 도구 특유의 잦은 프로세스 생성이 병목이 될 수 있다고 짚었다.[^Dwedit]

### 프리뷰 상태의 프로덕션 사용 위험

마이크로소프트가 공개적으로 “프리뷰”라고 명시한 것은 API 안정성이 보장되지 않음을 의미한다.
크로스 플랫폼 빌드 파이프라인에서 이 도구에 의존하기 시작하면, 향후 동작 변경이 빌드 시스템을 예상치 않게 중단시킬 수 있다.

### 이미 존재하는 대안들

HN에서는 같은 문제를 푸는 기존 도구들이 여럿 거론됐다.
한 사용자는 Busybox-w32가 가장 완성도 높은 Windows용 coreutils 구현이며,
유지보수자가 적극적으로 커뮤니티 PR을 병합하는 반면 마이크로소프트는 그러지 않을 것이라고 비판했다.[^doctorpangloss]
또 Git for Windows가 이미 bash를 포함한 GNU 호환 명령들을 함께 설치한다는 점,[^ilotoki0804]
그리고 cygwin, msys2도 오래전부터 같은 역할을 해왔다는 지적이 이어졌다.
마이크로소프트가 직접 제공한다는 정통성 외에 기능적 차별점이 무엇이냐는 물음은 이 발표에 대한 가장 흔한 회의론이었다.

## 인사이트

### Windows에서의 Unix 철학 채택

수십 년간 Windows는 Unix 철학 — 작고, 단일 목적을 가지며, 파이프라인으로 조합되는 도구들 — 과 대립하는 방향으로 발전했다.
PowerShell은 객체 기반 파이프라인으로 이 철학을 Windows식으로 재해석했다.
이제 마이크로소프트가 직접 Unix 도구를 Windows에 가져오는 것은 개발자 도구 생태계에서 Unix 철학의 승리를 시사한다.

이것은 개발자 경험(developer experience)이 플랫폼 차별화보다 더 중요한 전략 목표가 됐다는 마이크로소프트의 판단을 반영한다.
개발자를 Windows에 붙잡아두려면 Linux/Mac에서 익숙한 도구 경험을 제공해야 한다는 것이다.

### 크로스 플랫폼 스크립팅의 미래

이 도구가 성숙해지면, “Linux/Mac에서 작성하고 Windows에서 테스트”하는 대신 모든 플랫폼에서 동일한 스크립트가 동작하는 진정한 크로스 플랫폼 쉘 스크립팅이 가능해질 수 있다.
현재의 POSIX 호환 제한이 해결된다면, CI 파이프라인에서의 OS별 분기 처리가 대폭 줄어들 것이다.

---

[^testdelacc1]: <https://news.ycombinator.com/item?id=48373320>
[^fabiensanglard]: <https://news.ycombinator.com/item?id=48373327>
[^pjmlp]: <https://news.ycombinator.com/item?id=48373260>
[^dataflow]: <https://news.ycombinator.com/item?id=48373174>
[^EvanAnderson]: <https://news.ycombinator.com/item?id=48373627>
[^Dwedit]: <https://news.ycombinator.com/item?id=48374353>
[^doctorpangloss]: <https://news.ycombinator.com/item?id=48373796>
[^ilotoki0804]: <https://news.ycombinator.com/item?id=48373899>
