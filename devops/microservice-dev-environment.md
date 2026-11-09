# 컨테이너 기반 마이크로서비스 개발 환경 만들기: Vultr 인스턴스와 Mac mini·Mac Studio 구매 비교

<https://www.apple.com/kr/shop/buy-mac/mac-mini>

<https://www.apple.com/kr/shop/buy-mac/mac-studio>

<https://api.vultr.com/v2/plans?type=all&per_page=500>

## 소개

이 문서는 Docker 컨테이너로 마이크로서비스(microservice) 여러 개를 띄우고
같은 기계에서 Claude Code 세션을 동시에 돌리는 개발 환경을 만드는 방법을 다룬다.
기계를 어디서 구하느냐에 두 갈래가 있다.
Vultr에서 Linux 인스턴스를 월 단위나 시간 단위로 빌리는 방법과,
Apple의 Mac mini나 Mac Studio를 사서 책상이나 서버 자리에 두는 방법이다.
전제는 RAM 64GB, 컨테이너(container) 메모리 사용량 32GB 이상,
Claude Code 세션 12개이고, 목표는 여유 있는 사양이 아니라
빠듯해도 돌아가는 가장 낮은 비용이다.

두 방법은 결국 같은 질문으로 모인다.
기계 값을 한 번에 내고 오래 쓸지, 쓰는 만큼 달마다 낼지다.
그래서 문서는 비용을 먼저 비교한 뒤, 사양과 개발 환경의 구조,
각 방법의 구성 절차를 차례로 다룬다.

가격은 두 곳에서 읽었다.
Vultr 플랜은 2026년 11월 9일에 공개 Plans API에서 읽은 값이고,
Mac mini와 Mac Studio는 같은 날 Apple 한국 온라인 스토어의 구성별 페이지에서
읽은 값이다.
달러 금액에는 같은 날 환율 1달러당 1,361.4원을 곱한 원화를 함께 적었다.[^fx]
이 환율은 환율 조회 서비스의 값이어서
카드 결제나 환전에 적용되는 환율과 다를 수 있다.
이 문서의 명령과 설정은 어느 것도 실제 기계에서 실행해 보지 않았고,
메모리와 CPU 배분은 직접 재지 않은 추정이다.

## 요구 사항을 만족하는 구성

64GB 메모리를 채우면서 컨테이너 32GB 이상과 세션 12개가 함께 도는 구성을 고른다.

### Vultr

RAM이 64GB인 일반 플랜 가운데 월 요금이 낮은 순서는 아래와 같다.[^plans]

| 플랜 ID             | vCPU | RAM  | 디스크  | 월 요금                | 시간당 요금       |
| ------------------- | ---- | ---- | ------- | ---------------------- | ----------------- |
| `vx1-m-8c-64gb`     | 8    | 64GB | 없음    | $233.6 (약 318,000원)  | $0.32 (약 436원)  |
| `vx1-m-8c-64g-480s` | 8    | 64GB | 480GB   | $281.78 (약 383,600원) | $0.386 (약 526원) |
| `vc2-16c-64gb`      | 16   | 64GB | 1,280GB | $320 (약 435,600원)    | $0.438 (약 596원) |

`vx1-m-8c-64gb`는 API가 `storage_type`을 `block_storage`로 돌려주고
`disk`를 `1`로만 표기한다.[^plans]
Vultr 문서는 블록 스토리지(Block Storage) 볼륨이 NVMe 또는 HDD이고,
VX1 인스턴스는 스냅샷에서 부팅 가능한 볼륨을 복제할 수 있다고 설명한다.[^block]
이 두 사실을 합치면 이 플랜은 디스크가 요금에 들어 있지 않고 볼륨을 따로 사서
붙이는 구성으로 보인다.
볼륨의 GB당 요금은 가격 페이지가 JavaScript로 그려져서 읽지 못했다.
그래서 $233.6(약 318,000원)에 볼륨 요금을 더한 총액은 이 문서에서
계산하지 않았다.

`vx1-m-8c-64g-480s`는 `storage_type`이 `local_and_block_storage`이고
디스크 480GB가 요금에 들어 있다.[^plans]
두 플랜의 월 요금 차이는 $48.18(약 65,600원)이다.
요금이 확인된 가장 낮은 총액은 480GB가 포함된 $281.78(약 383,600원)이다.
CPU를 16개로 늘리는 다음 단계는 `vc2-16c-64gb`(월 $320,
약 435,600원)이다.[^plans]

vCPU 하나가 무엇인지도 봐야 한다.
API는 이 플랜들의 `vcpu_type`을 `thread`로 돌려준다.[^plans]
vCPU 8개는 하드웨어 스레드 8개를 뜻하므로 물리 코어 수는 그보다 적을 수 있다.

### Mac mini와 Mac Studio

Apple 한국 온라인 스토어에 올라온 구성 가운데
메모리 64GB를 채우는 것은 둘뿐이다.

| 구성                                                                      | 가격        |
| ------------------------------------------------------------------------- | ----------- |
| Mac mini, M5 Pro 칩, 18코어 CPU, 20코어 GPU, 64GB 메모리, 1TB 저장 장치   | 5,540,000원 |
| Mac Studio, M5 Max 칩, 18코어 CPU, 40코어 GPU, 64GB 메모리, 1TB 저장 장치 | 6,500,000원 |

가격은 각 구성의 구입 페이지에 적힌 값이다.[^mini-64][^studio-64]
같은 스토어의 다른 구성은 이 요구 사항에 모자란다.
Mac mini의 M6 칩 구성은 가장 큰 메모리가 32GB이고,
Mac Studio의 M5 Max 36GB 구성은 4,290,000원이지만 36GB여서
컨테이너 32GB에 세션 12개를 더하기에 모자란다.[^mini-spec][^studio-36]
Mac mini의 M5 Pro 칩은 통합 메모리가 최대 64GB이므로 64GB가 이 모델의
상한이다.[^mini-spec]
Mac Studio의 M5 Max 칩은 최대 128GB까지 선택할 수 있어서
더 큰 메모리가 필요해지면 이쪽이 열려 있다.[^studio-spec]

두 모델의 차이는 이렇다.

| 항목             | Mac mini (M5 Pro)              | Mac Studio (M5 Max)  |
| ---------------- | ------------------------------ | -------------------- |
| CPU              | 최대 18코어                    | 18코어               |
| GPU              | 최대 20코어                    | 최대 40코어          |
| 통합 메모리 상한 | 64GB                           | 128GB                |
| 메모리 대역폭    | 307GB/s                        | 최대 614GB/s         |
| 이더넷           | 2.5Gb                          | 10Gb                 |
| 확장 포트        | Thunderbolt 3개와 USB-C 2개 등 | Thunderbolt 5 4개 등 |
| 64GB 1TB 가격    | 5,540,000원                    | 6,500,000원          |

표의 값은 Apple 한국 제품 페이지의 서술을 옮긴 것이다.[^mini-spec][^studio-spec]
두 기계의 CPU 코어 수는 같다.
컨테이너 빌드와 서비스 실행은 CPU와 메모리가 일을 하므로,
GPU와 10Gb 이더넷과 128GB 메모리 상한이 필요하지 않다면
차액 960,000원은 개발 환경에 쓰이지 않는 부분을 사는 셈이다.
GPU 코어는 로컬 LLM이나 영상 작업에서 값을 하는 항목이다.

## 비용 비교: 몇 달이면 본전인가

Mac은 일시불이고 Vultr는 달마다 낸다.
그래서 Mac 가격을 Vultr 월 요금으로 나눈 개월 수가 기준이 된다.

| Vultr 월 요금 기준               | Mac mini 5,540,000원 | Mac Studio 6,500,000원 |
| -------------------------------- | -------------------- | ---------------------- |
| `vx1-m-8c-64gb` 약 318,000원     | 17.4개월             | 20.4개월               |
| `vx1-m-8c-64g-480s` 약 383,600원 | 14.4개월             | 16.9개월               |
| `vc2-16c-64gb` 약 435,600원      | 12.7개월             | 14.9개월               |

월 31만 원대의 클라우드를 계속 켜 두는 쓰임이라면
Mac mini는 1년 반 안쪽에서 본전이고 그 뒤로는 기계 값이 남는다.
Apple은 18개월 무이자 할부를 조건부로 제공한다.
Mac mini 64GB 구성을 18개월로 나누면 월 약 307,800원이고
이 금액은 Vultr의 가장 낮은 플랜 월 요금 약 318,000원과 거의 같다.
Mac Studio는 월 약 361,100원이다.
Apple 제품 페이지는 최소 결제 금액 조건을 채우고
제휴 신용카드를 쓸 때 최대 18개월 무이자 할부가 된다고 적는다.[^mini-spec]
카드사별 조건은 읽지 않았다.

그러나 이 계산은 쓰는 방식에 가장 크게 달라진다.
Vultr는 시간 단위로 과금되므로 쓸 때만 켜면 요금이 준다.
`vx1-m-8c-64gb`의 시간당 요금 $0.32(약 436원)로 하루 10시간,
한 달 22일(220시간) 쓰면
인스턴스 요금이 $70.4(약 95,800원)다.[^plans]
이 쓰임에서는 Mac mini 본전이 57.8개월, 곧 4년 10개월이고
Mac Studio는 67.8개월이다.
상시로 켜 두는 사람은 사는 쪽이, 일하는 시간에만 쓰는 사람은 빌리는 쪽이 앞선다.

두 방법의 비용에서 빠진 것이 서로 다르다.

| 항목                          | Vultr                               | Mac mini와 Mac Studio                                                                     |
| ----------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------- |
| 이 문서가 계산에 넣지 않은 것 | 블록 스토리지, 스냅샷, 트래픽, 세금 | 전기, 모니터와 입력 장치, AppleCare+, 정전 대비                                           |
| 되팔 수 있는가                | 없음                                | Apple Trade In이 있으나 견적은 예상 금액이고 실제는 낮을 수 있다고 스토어 페이지가 적는다 |
| 가격이 바뀔 위험              | 요금표가 바뀔 수 있음               | 이 저장소의 다른 문서가 메모리 가격 상승과 Apple의 가격 인상을 다룬다                     |

Mac Studio 스토어 페이지는 디스플레이와 액세서리가 별도 판매라고 적는다.
AppleCare+의 우발적 손상 본인 부담금은 화면이나 외장 손상이 건당 120,000원,
그 밖의 손상이 건당 370,000원이라고 스토어 페이지가 밝힌다.
가격이 올랐다는 사실은 이 저장소의 `hardware/apple-price-hike-ramagedon.md`와
`hardware/memory-prices-2026.md`에 정리되어 있다.
다만 앞 문서는 MacBook과 iPad의 인상을 다루고
Mac mini나 Mac Studio가 포함되는지는 확인되지 않았다.

## 사양을 요구 사항에 대 보기

| 요구 사항                         | Vultr `vx1-m-8c-64gb`     | Mac mini M5 Pro 64GB           |
| --------------------------------- | ------------------------- | ------------------------------ |
| 컨테이너를 돌리는 곳              | Linux에서 직접            | macOS 위의 Linux 가상 머신(VM) |
| Claude Code 세션 12개를 돌리는 곳 | 같은 Linux에서 SSH로 접속 | macOS에서 직접                 |
| CPU                               | vCPU 8개(스레드 단위)     | 코어 18개                      |
| 메모리를 나눠 쓰는 상대           | Linux 커널과 Docker       | macOS와 Docker용 VM            |
| 디스크                            | 볼륨을 따로 구매          | SSD 1TB 포함                   |
| 아키텍처                          | x86(AMD)                  | arm64(Apple silicon)           |
| 켜 두는 방식                      | 항상 켜져 있음            | 잠자기 방지와 정전 대비가 필요 |

CPU 비교에는 단서가 필요하다.
Vultr의 vCPU 8개는 스레드 8개이고 Mac mini M5 Pro의 18코어는 코어 수이므로
숫자를 그대로 견줄 수 없다.
다만 두 숫자의 차이가 이만큼 크면 CPU가 부족해서 12개 세션이 빌드와 겹칠 때
버티는 정도는 Mac mini 쪽이 넉넉할 가능성이 크다고 읽을 수 있다.
이것은 이 문서가 읽은 값으로부터의 추정이다.

## 개발 환경의 구조

### Vultr에서는 모든 것이 한 Linux 안에 있다

Docker 엔진이 Linux 커널 위에서 직접 돌고, Claude Code 세션도 같은 Linux에서
돌아간다.
사용자는 SSH로 접속해 세션을 열고, 서비스의 포트는 SSH 터널로 로컬에서 본다.
메모리 계획은 단순하다.
64GB를 운영체제, 컨테이너, 세션이 나눠 쓴다.

### Mac에서는 컨테이너가 VM 안에서 돈다

macOS에는 Linux 커널이 없으므로 Linux 컨테이너는 VM 안에서 돌아간다.
이 VM을 만드는 도구가 여럿 있다.
이 저장소의 `container/colima.md`에 정리된 Colima는 Lima 위에서 Docker,
containerd, Incus 런타임을 띄우고,
`colima start --cpu --memory --disk` 플래그로 VM의 자원을 정한다.
기본 사양은 CPU 2개, 메모리 2GB, 디스크 100GB다.
`mac/apple-container-machine.md`에 정리된 Apple의 `container`는 Apple silicon과
macOS 26 이상에서
컨테이너마다 가벼운 VM을 만든다.

이 구조가 메모리 계획에 영향을 준다.
VM은 시작할 때 정한 만큼의 메모리를 상한으로 받으므로,
컨테이너 32GB가 들어가려면 VM에 그보다 큰 값을 줘야 한다.
그 위에 macOS 자신이 쓰는 메모리와 Claude Code 세션이 같은 64GB를 나눠 쓴다.
Claude Code는 macOS에서 VM 밖의 네이티브 프로세스로 돌기 때문에
VM 메모리와는 따로 계산한다.

| 용도                    | Vultr 64GB | Mac 64GB |
| ----------------------- | ---------- | -------- |
| 운영체제                | 3GB        | 약 8GB   |
| 마이크로서비스 컨테이너 | 32GB       | 32GB     |
| Docker VM 자체          | 없음       | 약 2GB   |
| Claude Code 세션 12개   | 12GB       | 12GB     |
| 남는 공간               | 약 17GB    | 약 10GB  |

표의 값은 모두 추정이다.
Mac의 운영체제 몫은 Vultr의 서버용 Linux보다 크게 잡았고,
세션당 1GB는 Claude Code가 띄우는 Node.js 프로세스와 개발 도구를 합친 값으로
잡았다.
Mac은 남는 공간이 Vultr보다 작으므로 64GB가 더 빠듯하다.
메모리를 키워야 한다면 Mac mini는 64GB가 상한이어서
Mac Studio로 올라가야 한다.[^mini-spec][^studio-spec]

### 아키텍처가 다르다

Apple silicon에서 도는 컨테이너는 기본적으로 arm64 Linux 이미지다.
운영 환경이 x86 서버라면 이미지를 두 아키텍처로 빌드하거나 에뮬레이션을 쓰게
된다.
이 문서는 사용하는 이미지들이 arm64를 지원하는지 확인하지 않았다.
개발 환경에서 이 차이가 작은 문제인지는 서비스마다 다르다.

### 켜 두는 방식

Vultr 인스턴스는 항상 켜져 있다.
Mac은 잠자기에 들어가면 세션과 컨테이너가 멈추므로 막아야 한다.
이 저장소의 `mac/caffeinate.md`는 macOS 내장 명령 `caffeinate`가 유휴 잠자기를
막는 전원 assertion을
만든다고 정리한다.
`-s` 옵션은 AC 전원일 때만 유효하다고 한다.
상시 서버로 쓰려면 정전 대비와 자동 재시작이 문제가 되는데,
이 문서는 그 설정을 확인하지 않았다.

## 선택 기준

| 상황                                                          | 선택                                                                             |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 하루 대부분 켜 두고 1년 반 넘게 쓸 것이다                     | Mac mini M5 Pro 64GB. 18개월 무이자 할부 월 납입이 Vultr 최저 월 요금과 비슷하다 |
| 일하는 시간에만 쓰고 안 쓸 때는 끄고 싶다                     | Vultr 시간 과금. 본전이 5년에 가깝다                                             |
| 메모리가 64GB보다 필요해질 수 있다                            | Mac Studio. 상한이 128GB다                                                       |
| 서비스가 x86 이미지에 묶여 있다                               | Vultr. Mac은 arm64 호환을 먼저 확인해야 한다                                     |
| 어디서든 접속해야 하고 집이나 사무실의 전원과 회선이 불안하다 | Vultr                                                                            |
| ego lite처럼 macOS나 Windows 앱이 필요한 도구를 함께 쓴다     | Mac. Linux 서버에서는 설치할 수 없다                                             |

마지막 줄은 같은 저장소의 `ai-tool/ego-lite.md`를 근거로 한다.
ego lite는 macOS와 Windows에서 돌고 Linux는 로드맵에 있다.

## 구성 절차: 공통 부분

두 방법 모두 서비스를 하나의 Compose 파일로 정의해 두면
기계를 바꿀 때 옮기기 쉽다.
서비스마다 메모리 상한을 걸어 한 컨테이너가 다른 것을 밀어내지 못하게 한다.
Compose 파일은 서비스 단위로 `mem_limit`, `mem_reservation`, `memswap_limit`,
`cpus`를 지원한다.[^compose]

```yaml
services:
  api:
    image: example/api:dev
    ports:
      - "127.0.0.1:8080:8080"
    mem_limit: 4g
    memswap_limit: 6g
    cpus: 1.0
  worker:
    image: example/worker:dev
    mem_limit: 2g
    cpus: 0.5
```

이미지 이름과 수치는 자리 표시용이다.
서비스별 상한의 합이 32GB 안쪽에 들어오게 정한다.
포트를 `127.0.0.1`에만 묶고 접속은 SSH 터널로 하는 방식은 두 방법에 모두 맞는다.

쓰지 않는 서비스는 `docker compose` 프로필(profile)로 빼 두고
필요할 때만 올린다.
무거운 빌드와 테스트는 한 번에 하나씩 돌리면 CPU와 메모리가 겹치지 않는다.

## 구성 절차: Vultr

### 인스턴스 만들기

Vultr 대시보드에서 위 표의 플랜으로 Linux 인스턴스를 만들고, SSH 키를 등록하고,
방화벽 그룹을 연결한다.
`vx1-m-8c-64gb`는 `ewr`, `ord`, `sea`, `atl`, `ams`, `lhr`, `syd`, `nrt`,
`mxp`에서 배포할 수 있다.[^plans]

### 방화벽과 포트 노출

Vultr 방화벽 그룹(Firewall Groups)은 인스턴스로 오가는 IPv4와 IPv6 트래픽을 걸러
준다.[^firewall]
Docker는 컨테이너 포트를 게시(publish)하면
그 트래픽을 ufw 규칙이 적용되기 전에 가로채므로, ufw 설정이 무시된다고
Docker 문서가 밝힌다.[^ufw]
그래서 접근 제어는 ufw가 아니라 Vultr 방화벽 그룹에서 한다.
인바운드는 SSH(22)만 열고 출발지를 내 IP로 제한한다.

### 스왑 파일

```bash
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swap.conf
```

스왑은 디스크에 있으므로 쓰는 순간 느려지고,
넘침을 받아 주는 완충이지 상시 사용량이 아니다.
이 플랜의 부팅 디스크가 볼륨이면 스왑 속도가 어떨지는 재 보지 않았다.

### Docker 설치

Docker 공식 문서의 apt 저장소 설치 방법을 따른다.
설치 뒤에는 `docker compose version`으로 Compose 플러그인이 붙었는지 확인한다.

### 쓸 때만 켜기

삭제한 인스턴스에서 같은 환경을 다시 만들려면
데이터를 인스턴스 디스크가 아니라 별도 볼륨이나 오브젝트 스토리지에 두고
Compose 파일과 설정 스크립트를 저장소에 두어야 한다.
Vultr가 중지(stop)한 인스턴스에도 요금을 매기는지,
삭제한 뒤 남는 볼륨에 얼마가 나오는지는 이 문서에서 확인하지 못했다.

## 구성 절차: Mac mini 또는 Mac Studio

### 구성 고르기

이 요구 사항의 최소는 Mac mini M5 Pro, 18코어 CPU, 64GB 메모리,
1TB 저장 장치다.[^mini-64]
메모리는 칩과 함께 구성하는 항목이고 구매 시점에 정해진다.
나중에 늘릴 수 있는지는 이 문서가 확인하지 못했으므로,
64GB가 모자랄 가능성이 있으면 처음부터 Mac Studio를 보는 편이
안전하다.[^studio-spec]

### macOS 설정

- 원격에서 접속할 수 있게 SSH를 켠다.
- 상시 서버로 쓸 때는 `caffeinate`나 에너지 설정으로 잠자기를 막는다.
- 정전 뒤 자동 재시작과 로그인 설정은 이 문서가 확인하지 못했다.

### 컨테이너 런타임

Colima를 쓴다면 VM에 컨테이너 몫을 넉넉히 준다.
예를 들어 메모리 40GB, CPU 12개, 디스크 200GB는 아래처럼 정한다.

```bash
colima start --cpu 12 --memory 40 --disk 200
```

이 수치는 자리 표시용이고, 컨테이너 32GB와 VM 자체의 몫을 더해 정한 것이다.
VM이 가진 메모리 상한을 넘기는 컨테이너는 VM 안에서 종료되므로,
`docker stats`로 실제 사용량을 잰 뒤에 값을 조정한다.
Apple의 `container`를 쓰면 컨테이너마다 VM이 따로 생기므로
컨테이너 수가 많을 때 VM 하나당 몫이 메모리에 쌓이는지 재 봐야 한다.

## 측정과 판단 기준

돌려 본 뒤에는 아래 명령으로 실제 사용량을 잰다.

```bash
free -h
docker stats --no-stream
vmstat 5
```

`free`와 `vmstat`는 Linux 명령이어서 Mac에서는 VM 안에서
실행하거나 활성 상태 보기(Activity Monitor)로 대신한다.
다음 중 하나가 반복되면 이 구성은 모자란 것이다.

- 스왑 사용량이 계속 늘어난다.
- OOM(out of memory) 종료 기록이 남는다.
- 부하 평균(load average)이 코어 수를 오래 넘는다.

모자랄 때의 다음 단계는 구성마다 다르다.
Vultr는 `vc2-16c-64gb`로 CPU를 늘리거나 RAM이 큰 플랜으로 올린다.
Mac mini는 64GB가 상한이므로 메모리가 문제라면 Mac Studio로 옮긴다.

## 확인하지 못한 것

- 블록 스토리지의 GB당 요금과 스냅샷 요금
- 중지한 인스턴스와 삭제한 뒤 남는 볼륨의 과금 방식
- Apple 가격에 세금이 포함되었는지와 18개월 무이자 할부의 카드사별 조건
- Mac mini 메모리를 구매 뒤에 늘릴 수 있는지
- 사용하는 컨테이너 이미지의 arm64 지원
- Claude Code 세션 하나와 macOS의 실제 메모리 사용량
- Mac을 상시 서버로 쓸 때의 정전 후 자동 재시작과 전기 요금
- 리전별 재고와 Vultr의 세금

---

[^fx]: ExchangeRate-API, [USD 기준 환율 조회](https://open.er-api.com/v6/latest/USD), 2026-11-09

[^plans]: Vultr, [Plans API](https://api.vultr.com/v2/plans?type=all&per_page=500), 2026-11-09

[^block]: Vultr Docs, [Vultr Block Storage Volumes for Cloud Compute Instances](https://docs.vultr.com/products/storage/block-storage)

[^firewall]: Vultr Docs, [Vultr Firewall Groups for Instance Traffic Filtering](https://docs.vultr.com/products/network/firewall)

[^ufw]: Docker Docs, [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/)

[^compose]: Docker Docs, [Services top-level elements](https://docs.docker.com/reference/compose-file/services/)

[^mini-64]: Apple, [Mac mini, M5 Pro 칩, 18코어 CPU, 20코어 GPU, 64GB 메모리, 1TB 저장 장치](https://www.apple.com/kr/shop/buy-mac/mac-mini/m5-pro-%EC%B9%A9-18%EC%BD%94%EC%96%B4-cpu-20%EC%BD%94%EC%96%B4-gpu-64gb-%EB%A9%94%EB%AA%A8%EB%A6%AC-1tb-%EC%A0%80%EC%9E%A5-%EC%9E%A5%EC%B9%98)

[^studio-64]: Apple, [Mac Studio, M5 Max 칩, 18코어 CPU, 40코어 GPU, 64GB 메모리, 1TB 저장 장치](https://www.apple.com/kr/shop/buy-mac/mac-studio/m5-max-%EC%B9%A9-18%EC%BD%94%EC%96%B4-cpu-40%EC%BD%94%EC%96%B4-gpu-64gb-%EB%A9%94%EB%AA%A8%EB%A6%AC-1tb-%EC%A0%80%EC%9E%A5-%EC%9E%A5%EC%B9%98)

[^studio-36]: Apple, [Mac Studio, M5 Max 칩, 18코어 CPU, 32코어 GPU, 36GB 메모리, 512GB 저장 장치](https://www.apple.com/kr/shop/buy-mac/mac-studio/m5-max-%EC%B9%A9-18%EC%BD%94%EC%96%B4-cpu-32%EC%BD%94%EC%96%B4-gpu-36gb-%EB%A9%94%EB%AA%A8%EB%A6%AC-512gb-%EC%A0%80%EC%9E%A5-%EC%9E%A5%EC%B9%98)

[^mini-spec]: Apple, [Mac mini](https://www.apple.com/kr/mac-mini/)

[^studio-spec]: Apple, [Mac Studio](https://www.apple.com/kr/mac-studio/)
