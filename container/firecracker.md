# Firecracker: AWS Lambda와 Fargate를 위해 만든 최소 구성의 KVM microVM 모니터

<https://github.com/firecracker-microvm/firecracker>

HN 토론: <https://news.ycombinator.com/item?id=18539532> (24점, 10개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=45060837> (45점, 5개 댓글)

## 소개

Firecracker는 서버리스 컴퓨팅을 위한 안전하고 빠른 microVM을 만드는 오픈소스
가상화 기술이다.
README는 사명을 컨테이너와 함수 워크로드를 안전한 다중 테넌트로 최소한의 오버헤드로
실행하는 것이라고 밝힌다.
하드웨어 가상화가 주는 보안과 격리에 컨테이너의 속도와 유연성을 합친 가벼운
가상 머신을 microVM이라 부른다고 설명한다.

AWS에서 AWS Lambda와 AWS Fargate의 속도와 효율을 높이려고 개발되었고,
Apache 2.0 라이선스로 공개되어 있다.
Kata Containers와 Flintlock 같은 컨테이너 런타임에 통합되었다고 한다.
저장소는 2017년 10월에 만들어졌고 Rust로 쓰였으며,
2026년 11월 9일 기준 GitHub API가 보고한 별은 37,903개, 포크는 2,729개,
열린 이슈는 141개이고 마지막 푸시는 11월 6일이다.
이 문서는 직접 설치하거나 시험하지 않았고 README와 GitHub API,
HN 댓글에서 읽은 내용만 정리했다.

## 구조와 기능

핵심 구성 요소는 리눅스 KVM을 써서 microVM을 만들고 실행하는 가상 머신
모니터(VMM)다.
README는 이 VMM이 불필요한 장치와 게스트 대상 기능을 뺀 최소 설계라서
microVM마다 메모리 사용량과 공격 표면을 줄이고, 시작 시간을 줄이고,
하드웨어 활용도를 높인다고 설명한다.

프로세스 하나가 시작되면 호스트에 API 엔드포인트를 연다.
API는 OpenAPI 형식으로 정의되어 있고 다음을 할 수 있다고 README가 적는다.

- vCPU 수(기본 1)와 메모리 크기(기본 128MiB), CPU 템플릿 설정
- 네트워크 인터페이스와 읽기 쓰기 또는 읽기 전용 디스크(파일 기반 블록 장치) 추가
- virtio 장치의 대역폭이나 초당 연산 수 제한(rate limiter), 로그와 지표 설정
- vsock 소켓, 엔트로피 장치, pmem 장치 추가, 메모리 핫플러그 관리
- 개발자 미리 보기 단계의 virtio PCI 장치 핫플러그
- 주어진 커널 이미지, 루트 파일 시스템, 부팅 인자로 microVM 시작

기본 제공 기능으로는 요구 시 페이지 폴트와 CPU 오버섭스크립션, 스레드별 seccomp
필터, 운영 환경에서 cgroup과 네임스페이스 격리를 걸고 권한을 내려놓는 Jailer
프로세스가 있다.
소스에서 빌드하려면 Docker가 도는 유닉스 계열 시스템에서 다음처럼 한다.

```bash
git clone https://github.com/firecracker-microvm/firecracker
cd firecracker
tools/devtool build
toolchain="$(uname -m)-unknown-linux-musl"
```

결과 바이너리는 `build/cargo_target/${toolchain}/debug/firecracker`에 생긴다.
릴리스는 보통 두세 달마다 GitHub 릴리스로 나온다고 한다.

## 보안에 대한 README의 단서

README는 Firecracker microVM의 전체 보안, 곧 안전한 다중 테넌트 컴퓨팅의 기준을
맞출 수 있는지는 잘 구성된 리눅스 호스트 운영체제에 달려 있다고 밝힌다.
이 기준을 만족한다고 믿는 구성을 운영 호스트 설정 문서로 제공한다.
취약점을 발견했다고 의심되면 비공개로 연락하도록 보안 정책 문서를 안내하고,
보안을 최우선으로 둔다고 쓴다.
이 문서는 취약점 사례를 다루지 않으며, 기존 취약점 보고는 이 저장소의
`security/` 아래 문서에서 다룬다.

## 비평

### 지원 범위가 AWS 인스턴스 조합에 묶여 있다

README의 시험 플랫폼 표는 m5n, m6i, m7i, m8i, m6a, m7a, m6g, m7g, m8g, m9g 같은
AWS EC2 베어메탈 인스턴스와 호스트 커널 5.10, 6.1, 6.18의 조합이다.
8세대 Intel(`*8i`)은 6.1이나 6.18 호스트 커널에서만 지원한다고 하고,
이유로 5.10에서 Granite Rapids CPU에 대한 커널 지원이 나쁜 점을 든다.
자기 하드웨어에서 돌리려는 사람에게 이 표는 지원되는 환경이 매우 구체적이라는
뜻이다.
README가 알려진 한계로 적는 것은 aarch64의 `pl031` RTC 장치가 인터럽트를 지원하지
않아 RTC 알람을 쓰는 게스트 프로그램이 동작하지 않는다는 하나뿐이다.

### 장치 수가 적다는 것은 성능 한계로도 읽힌다

HN에서 bradhe가 쓰면서 겪을 함정이 있는지 묻자 scoodah는 구현된 가상 장치의 수가
제한적이어서 입출력 처리량이 높은 애플리케이션에서 병목이 생길 수 있고,
동적 메모리 관리는 메모리 벌루닝을 쓰기 때문에 이를 관리할 맞춤 구현이 필요하다고
답했다.[^bradhe][^scoodah]
이는 한 사용자의 경험이다.
README의 최소 설계가 공격 표면을 줄이는 장점은 같은 이유로 기능과 성능의
한계가 된다는 구조다.

### 쿠버네티스와의 관계는 처음부터 오해가 있었다

HN의 2018년 공개 스레드에서 cheeseburgerj는 쿠버네티스가 하지 못하는 일이 무엇이냐며
AWS가 잃은 종속성을 되찾으려는 것 같다고 썼다.
mcrute는 Firecracker가 전혀 다른 목적을 가진다고 답했다.
쿠버네티스는 클러스터 스케줄러이고 스케줄되는 컨테이너는 여전히 런타임이
필요하다는 설명이었다.[^cheeseburgerj][^mcrute]
2025년 스레드에서 jiggawatts가 오픈소스가 되었으니 쿠버네티스에 통합할 수 있을지
궁금해하자 scoodah는 2018년부터 오픈소스였으며 컨테이너를 microVM으로 돌리는
firecracker-containerd가 오래전부터 있다고 바로잡았다.[^jiggawatts][^scoodah-containerd]
README가 AWS의 두 서비스에서 출발했다고 밝히는 점과 별개로,
범용 컨테이너 대체가 아니라 격리 경계를 하나 더 두는 도구라는 이해가 반복해서
필요하다.

## 도입 전에 따져볼 것

- 호스트 구성을 먼저 따른다. 운영 호스트 설정 문서를 따르지 않으면 README가 말하는 안전한 다중 테넌트 기준을 만족한다고 볼 수 없다.
- Jailer로 시작하고 seccomp와 격리를 켠 상태를 기본으로 삼는다.
- 자기 하드웨어와 커널 조합이 시험 플랫폼 표에 있는지 확인한다.
- 입출력이 많은 워크로드와 동적 메모리가 필요한 워크로드는 장치 수와 벌루닝 때문에 별도로 시험한다.
- 컨테이너 생태계에 쓰려면 직접 쓰기보다 Kata Containers나 firecracker-containerd 같은 통합이 이미 있는지 먼저 확인한다.
- 취약점 신고는 공개 이슈가 아니라 보안 정책 문서의 비공개 경로로 한다.

---

[^bradhe]: <https://news.ycombinator.com/item?id=45069228>

[^scoodah]: <https://news.ycombinator.com/item?id=45077671>

[^cheeseburgerj]: <https://news.ycombinator.com/item?id=18539589>

[^mcrute]: <https://news.ycombinator.com/item?id=18539621>

[^jiggawatts]: <https://news.ycombinator.com/item?id=45072266>

[^scoodah-containerd]: <https://news.ycombinator.com/item?id=45077968>
