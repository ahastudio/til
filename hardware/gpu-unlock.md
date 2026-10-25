# GPU unlock: RTX 30 시리즈의 FP/BF16 명령 발행 속도 제한을 푸는 리눅스 커널 모듈

<https://github.com/Zagitta/gpu-unlock>

HN 토론: <https://news.ycombinator.com/item?id=50219700> (212점, 67개 댓글)

GN 토론: <https://news.hada.io/topic?id=35938>

## 소개

GPU unlock은 NVIDIA RTX 30 시리즈 카드의 FP/BF16 명령 발행 속도를 전문가용
카드와 같은 수준으로 풀어 주는 리눅스 커널 모듈이다.
README는 이 모듈이 GA102, GA103, GA104, GA106 카드에서 FP/BF16 FMA를 FP32로
누적하는 연산의 명령 발행 속도를 두 배로 만든다고 설명한다.
CMP 언락 도구의 V67/PLM 기법을 UEFI 방식의 드라이버 이전 타이밍과 합쳤다고 하며,
언락을 실행하고 속도 선택값을 쓰고 FLR을 수행한 뒤 수정하지 않은 NVIDIA
드라이버가 카드를 붙잡게 한다.
UEFI 애플리케이션도 패치한 NVIDIA 드라이버도 아니다.
README가 강조하는 이점은 NVIDIA가 새 드라이버를 낼 때마다 수동으로 패치할 필요가
없다는 점이다.

저장소는 2026년 10월 18일에 만들어졌고 마지막 푸시는 10월 24일이며, GitHub API
기준 언어는 C, 별은 3,469개다.
README는 커널 모듈과 로컬 패키징이 GPL-2.0-only이고, 생성되는 페이로드는 고정된
CMP 참조에서 파생됐으며 NVIDIA 펌웨어는 자체 약관을 따른다고 적는다.
GitHub의 라이선스 메타데이터는 비어 있다.
이 문서는 저장소의 코드와 문서를 직접 실행하거나 검증하지 않았고, README와 HN
스레드에 쓰인 내용을 정리했다.

README의 측정은 3090 Ti, 450W, 8192³ 밀집 GEMM, FP32 누적, 다섯 번의 중앙값이다.
FP16은 87.46에서 118.39 TFLOPS로, BF16은 87.50에서 157.41 TFLOPS로, TF32는
42.58에서 82.61 TFLOPS로 오른다.
다른 카드의 수치는 사용자 보고로 모은 표에 있다.
3090 Ti는 BF16 GEMM이 68~80%, 3090은 25~67%, 3080 10GB는 70~73%, 3070은 73~81%,
3060 12GB는 약 80% 올랐다고 하며, 가장 낮은 25%는 전력 제한이 225W인 카드에서
나왔다.
3080 Ti 20GB OEM 카드는 언락이 끝났지만 BF16이 절반 속도에 머물렀다고 한다.
3070 Ti는 이 모듈로는 시험되지 않았고 Windows용 UEFI 포트로는 됐다는 보고가
있다.
GA103은 보고가 아직 없다.

## 동작 방식

### 속도 제한을 푸는 위치가 드라이버보다 앞이다

모듈은 initramfs에 들어가 `nvidia`가 카드를 붙잡기 전에 실행된다.
그래서 드라이버를 패치하지 않아도 되고, 드라이버 버전에 묶이지 않는다.
언락은 커널 명령행에서 선택해야 동작한다.
`gpu_unlock.targets=all`은 아직 드라이버가 붙지 않은 모든 GA102, GA103, GA104,
GA106 카드를, PCI 주소를 쓰면 그 카드만 대상으로 한다.
부팅 뒤에 모듈을 손으로 올리면 이미 `nvidia`가 붙잡은 카드에는 아무 일도 하지
않는다.
여러 카드는 동시에 언락하며 전부 합쳐 1초쯤 걸린다.

### 화면 출력과 절전에서의 동작

화면을 내는 카드에도 적용된다.
펌웨어 프레임버퍼(부팅 콘솔과 Plymouth)는 언락 단계가 도는 동안 유지되다 카드
리셋 직전에 제거되고, 리셋부터 `nvidia-drm`이 인수할 때까지 화면이 비어 있다.
메모리로의 절전은 카드 전원을 끄므로 속도 선택값이 초기화된다.
복귀할 때 모듈은 부팅 때 언락했던 카드를 `nvidia`가 깨우기 전에 다시 언락하며,
복귀가 1초쯤 늘어난다.
최대 절전은 다루지 않는다.
펌웨어가 멈추지 않는 카드에서는 모듈이 이를 기록하고, 펌웨어가 쓸 수 있는 DMA
버퍼를 다음 전원 차단까지 유지한다.
이 경우 다시 시도하기 전에 전원을 끄라고 한다.

## 설치하기

README의 절차는 두 단계다.
먼저 저장소를 받아 `make install`을 실행한다.
이 명령은 `/etc/os-release`로 Arch, Debian/Ubuntu, Fedora/RHEL 계열을 감지해
맞는 설치기를 고르고 sudo 암호를 묻는다.
그다음 커널 명령행에 `gpu_unlock.targets=all`을 기존 옵션을 유지한 채 덧붙인다.
GRUB, systemd-boot, UKI 등 배포판별 방법이 README에 나와 있다.
결과는 `journalctl -k -b | grep gpu_unlock`과 `lspci -nnk -s <주소>`로 확인하고,
되돌리려면 명령행에서 `gpu_unlock.targets=`를 지운다.
빌드는 고정된 NVIDIA와 CachyOS 입력을 HTTPS로 내려받아 SHA-256을 확인한다.
`make dist` 보관본, Debian 소스 패키지, `.nosrc.rpm`에는 NVIDIA 보관본과 생성된
펌웨어가 들어 있지 않다고 한다.

## 함정

### 이득은 전력 제한과 작업의 종류에 크게 좌우된다

README 스스로 이득이 각 보고자의 벤치마크이므로 서로 직접 비교할 수 없고 전력
제한이 크게 중요하다고 적는다.
행렬 연산이 많은 작업(LLM prefill, 확산 모델, FlashAttention)은 빨라지지만,
메모리 대역폭이 한계인 LLM 디코딩과 INT8은 거의 같다.
LLM prefill은 14~36%로 보고됐다.
비교한 보고에서는 출력이 언락 전후로 비트 단위로 같았다고 한다.
HN에서 jacquesm은 카드를 더 뜨겁게 돌려야 하고 이득이 크려면 최대 전력을 450W로
올려야 하며 순정 쿨러가 견디게 설계된 수준을 넘는다고 주의했다.[^jacquesm]
Zagitta는 언락이 특정 명령을 풀 속도로 낼 수 있게 바꿀 뿐이고, 더 많은 연산은
전력을 더 쓰니 전력 한도 안에서는 주파수 곡선이 내려간다고
설명했다.[^Zagitta-power]
따라서 순정 전력 제한에서는 풀 속도에 이르지 못하며 남는 이득은 작업에 따라
다르다.

### 광고된 수치와 사용자 보고가 크게 다를 수 있다

blagui는 TFLOPS 시험은 200W 제한에서 25%였고 prefill만 이득을 보고 디코딩이
그렇지 않아 실제 이득이 7~8%라고 했다.[^blagui]
chromaton은 3060에서 nanochat 학습이 6% 빨라졌고 170W에 막혀 있으며, 저장소가
커널 6.x용이라 5.15에서는 Claude Code의 도움으로 코드를 고쳐야 했다고
했다.[^chromaton]
Sharlin은 xrd에게 25~80%이며 AI 작업에 한정되고 실제 개선은 다른 병목 때문에
훨씬 적다고 정리했다.[^Sharlin]
반대로 aunty_helen은 27B 모델을 개발자가 벤치마크해 133 tks, 약 3.2배가 나왔다고
했다.[^aunty_helen]
이 수치는 README의 어느 표와도 맞지 않으며 이 문서는 확인하지 못했다.

### 지원하는 카드는 사용자 보고가 정한다

README는 모듈이 `kernel/gpu_unlock/main.c`의 모든 GeForce ID를 받아들이지만 표의
카드는 누군가 보고한 것이라고 밝힌다.
superkuh은 헤드라인이 틀렸고 풀린 것은 16비트가 아니라 FP32 쪽이며, 일주일 동안
3090과 3090 Ti 이외에 적용된 보고를 보지 못했다고 했다.[^superkuh]
Tiberium은 저장소의 이슈에 3080 Ti, 3070 Ti, 3070, 3060의 보고가 있다고
답했고,[^Tiberium-cards] Zagitta는 대부분의 30 시리즈가 같은 GA102 부트 단계를
쓰기 때문에 작동하며 VBIOS 구성이 특이한 카드에 문제가 있다는 보고가 있다고
했다.[^Zagitta-cards]
README의 표도 이 답과 같은 모양이다.
다만 3080 Ti OEM 카드는 BF16이 절반 속도에 남았다.

## 비평

### 이 도구가 의존하는 것은 보장이 아니라 제조사가 막지 않는다는 사실이다

Tiberium은 직접 시험했고 결과가 진짜지만 펌웨어를 악용하는 방식이라 조금
위험하다고 했다.[^Tiberium-risk]
chromaton도 카드를 망가뜨리거나 불을 내고 싶지 않아 전력 제한 안에서 쓴다고
했다.[^chromaton]
README는 보증이나 고장 위험을 다루지 않는다.
londons_explore는 다음 버전은 이런 설정을 막는 서명된 펌웨어를 내놓을 것이
틀림없다고 했다.[^londons_explore]
Zagitta는 Hopper와 Blackwell은 부팅 과정이 새롭고 보안 단계가 더 많아 이 방식의
범위 밖이라고 했다.[^Zagitta-security]
따라서 이 도구는 이미 판 카드에 한해서만 작동하는 방법이고, 새 세대에서
이어진다는 근거는 없다.

### 라이선스 서술은 부분마다 다르다

모듈과 패키징은 GPL-2.0-only이고, 생성되는 페이로드는 고정된 CMP 참조에서
파생됐으며, NVIDIA 펌웨어는 자체 약관을 따른다고 README가 적는다.
GitHub의 라이선스 메타데이터는 비어 있다.
저장소를 내려받는 쪽에서는 어느 부분이 어느 조건인지 `firmware/NOTICE.md`와
`licenses/`를 직접 읽어야 한다.
이 문서는 두 파일을 열어 보지 못했다.

### 주제가 하드웨어 제한 해제여서 이득과 위험이 모두 개인의 책임이다

pixl97은 NVIDIA가 몇 년 동안 카드가 부족할 것이니 이 제한을 둘 이유가 없다고
했다.[^pixl97]
wewewedxfgdf는 NVENC 세션 제한을 푸는 별도 패치를 들며, 카드를 사고 나서 제
성능을 내려면 소프트웨어를 따로 돌려야 하는 상황을 비꼬았다.[^wewewedxfgdf]
이 반응들은 이 모듈이 하드웨어의 성능 제한이 기술이 아니라 판매 정책이라는
인식을 보여 준다.
다만 그 인식과 별개로 이 도구는 소유자가 자기 카드에 쓰는 선택이고, 그로 인한
열, 전력, 보증 문제는 사용자가 진다.

## 인사이트

### 제품 등급을 가르는 것이 칩이 아니라 설정값일 수 있다

README가 말하는 것은 같은 칩에서 소프트웨어가 정한 발행 속도가 카드 등급을
나눈다는 점이다.
같은 GA102를 쓰는 소비자용 카드와 전문가용 카드의 차이가 일부는 이 설정이라는
뜻이다.
이런 구조에서는 사용자가 설정을 풀 수 있는지 여부가 제조사의 가격 정책을
시험한다.
CPU의 배수 잠금처럼 칩의 일부 기능을 등급에 묶는 방식은 오래전부터 있었고
사용자가 푸는 시도도 늘 있었지만, 이것은 이 문서의 비유이고 이 글이 다루지는
않는다.
제조사의 대응은 보통 다음 세대에서 해당 설정을 하드웨어나 서명된 펌웨어로 옮기는
것이며, londons_explore의 예상과 Zagitta가 말한 새 세대의 보안 단계가 그
방향이다.

### 검증 자료를 사용자가 만들고 저장소가 표로 묶는다

README의 표는 사용자가 이슈로 올린 보고를 모은 것이다.
카드, PCI ID, 결과, 이득, 보고 번호가 한 줄에 있고, 효과가 없었던 카드도 같은
표에 들어 있다.
이는 제조사 사양서가 아닌 커뮤니티가 만든 호환성 목록이며, 약점은 보고의
조건(전력 제한, 벤치마크)이 제각각이라는 점이다.
README도 이를 인정한다.
따라서 자기 카드에 적용하려는 사람은 표의 숫자가 아니라 같은 모델에 대한 이슈를
읽고 보고자의 전력 제한과 작업을 확인해야 한다.

### 이 글을 읽는 방법

이 저장소는 사용자 보고로 지원 범위를 넓혀 가는 초기 프로젝트이고, 판단에 필요한
것은 자기 카드와 자기 작업에서의 측정이다.
오늘 할 일은 저장소에서 같은 모델 카드의 이슈를 찾아 보고자의 전력 제한과 작업이
자기와 같은지 보고, 순정 전력 제한에서 자기 작업(학습인지 prefill인지
디코딩인지)이 행렬 연산 중심인지 확인하는 것이다.
이 도구의 주장을 가를 관찰은 두 가지다.
같은 카드를 순정 전력 제한에서 같은 작업으로 언락 전후 측정했을 때 이득이
README의 최대 수치가 아니라 사용자 보고의 중앙값에 가까운지, 그리고 NVIDIA의
드라이버나 펌웨어 갱신 뒤에도 언락이 계속 작동하는지다.
둘 다 이 문서는 직접 확인하지 못했다.

---

[^jacquesm]: <https://news.ycombinator.com/item?id=50221626>

[^Zagitta-power]: <https://news.ycombinator.com/item?id=50222247>

[^blagui]: <https://news.ycombinator.com/item?id=50224176>

[^chromaton]: <https://news.ycombinator.com/item?id=50224546>

[^Sharlin]: <https://news.ycombinator.com/item?id=50226671>

[^aunty_helen]: <https://news.ycombinator.com/item?id=50222269>

[^superkuh]: <https://news.ycombinator.com/item?id=50221729>

[^Tiberium-cards]: <https://news.ycombinator.com/item?id=50221825>

[^Zagitta-cards]: <https://news.ycombinator.com/item?id=50222051>

[^Tiberium-risk]: <https://news.ycombinator.com/item?id=50219868>

[^londons_explore]: <https://news.ycombinator.com/item?id=50223892>

[^Zagitta-security]: <https://news.ycombinator.com/item?id=50222921>

[^pixl97]: <https://news.ycombinator.com/item?id=50224142>

[^wewewedxfgdf]: <https://news.ycombinator.com/item?id=50228023>
