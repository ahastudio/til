# RTX Spark 노트북에 Arch Linux를 올리면 CPU와 GPU가 116GiB를 하나의 풀로 보지만 비교는 같은 조건이 아니다

원문: [putting linux on my rtx spark laptop because i don't have a microsoft account - josie.lol](https://josie.lol/blog/linux-rtx-spark)

HN 토론: <https://news.ycombinator.com/item?id=50158100> (195점, 90개 댓글)

GN 토론: <https://news.hada.io/topic?id=35665>

## 요약

josie.lol의 저자는 2026년 10월 19일 글에서
ASUS ProArt P16 H7607BA-SE033W에 Arch Linux를 올린 이야기를 쓴다.
이 모델은 RAM 128GB, CUDA 코어 6,144개, SSD 2TB 구성이다.
요약은 이렇다.
Arch Linux가 동작하고 7-Zip에서 Windows와 비슷한 성능을 내며
OS와 CUDA에 같은 116.0GiB의 메모리 풀을 보고한다.
부팅 가능한 초기 설정과 패치는 저자의 저장소에 공개되어 있다.

저자는 GPU가 접근할 수 있는 RAM이 100GiB 이상인 노트북에 대한 소문이 돌 때부터
오픈 웨이트 모델을 로컬에서 돌리고
RL과 양자화와 미세 조정을 만지는 일을 생각했다고 한다.
이미 Hugging Face에 직접 만든 GGUF 양자화를 올리고
있고 지난달 다운로드가 16만 건을 넘었다고 한다.
공식 지원이 Windows뿐이라는 점이 실망스러웠고
Windows를 싫어하는 이유로 설정 중의 개인정보 양보와
오래 걸린 작업 표시줄 위치 문제와 광고를 든다.

저자는 Arch의 패키지 관리자 스태프이고
IBM 메인프레임에도 Arch를 올린 적이 있으며
이 빌드는 Arch Linux ARM에 하드웨어 지원을 덧붙인 것이다.
NVIDIA가 Ubuntu용으로 하던 커널 작업을 출발점으로 삼고 콘솔을 얻으려고
ACPI 오버라이드 할당과 프레임버퍼 매핑을 고쳤으며
노트북 자신의 테이블에서 ACPI 오버라이드를 도출했다.
키보드는 패치한 `hid-asus`가 필요했고 오디오는 별도의 머신 드라이버가 필요했다.
이것을 부팅 USB로 만들고
업스트림 Archinstall 4.5를 확장해 하드웨어 지원을 설치하게 했으며
빌드 입력은 해시로 고정하고
주말에 만든 하드웨어 패키지는 저자의 Arch 패키지 관리자 키로 서명했다.

성능은 세 가지 측정으로 보여 준다.
CPU는 네이티브 ARM64 7-Zip 26.04에서 32MiB 사전으로,
스레드 수마다 워밍업 한 번과 측정 세 번의 중앙값을 냈다. 1스레드는 압축
6.18MiB/s와 압축 해제 118.26MiB/s, 20스레드는
압축 141.77MiB/s와 압축 해제 1,629.60MiB/s였다.
StorageReview가 같은 20코어 N1X를 단 HP OmniBook Ultra 16 128GB에서
Windows ARM64 네이티브로 잰 값과 GIPS로 맞춰 비교하면,
1스레드는 거의 같고 20스레드 압축은 5.0%, 압축 해제는 2.7% 앞선다.
ComputerBase의 ProArt P16 Windows 점수 155.774GIPS는
저자의 세 번 측정 범위 155.759~157.193GIPS 안에 든다.

메모리 분할이 더 큰 자랑거리라고 저자는 쓴다.
Linux에서는 시스템 RAM과 CUDA 총량 모두 같은 물리 풀에서 116.0GiB로 보고된다.
Windows는 RAM을 전용 GPU 영역과 공유 영역과 CPU 전용 영역으로 나누어,
CPU 작업이 전용 GPU 영역을 쓸 수 없고 GPU 할당이 CPU 전용 영역을 쓸 수 없다.
Frandroid의 128GB ProArt P16은 전용 예약을 96GiB까지 올렸고, 91GiB 예약에서
CUDA 총량 109.7GiB를 보고했는데 저자의 Linux는 116.0GiB여서 약 6.3GiB 많다.
저자는 예약 슬라이더를 움직이고 재부팅하지 않아도
CPU 작업에 큰 풀을 쓸 수 있다는 점에 가치를 둔다.

로컬 LLM은 NVIDIA의 Qwen3.8-Flash-Next-FP4-Local을
vLLM과 B12X CUDA 커널로 ARM64 컨테이너에서 돌렸다.
적재 전에 Linux가 보고한 가용 RAM은 110.9GiB였고
vLLM은 모델 적재에 68.2GiB, KV 캐시에 21.1GiB를 할당했다.
적재와 컴파일에 첫 요청까지 약 16분이 걸렸다고 한다.
세 과제의 중앙값은 이렇다.

| 과제                             | 입력 토큰 | 첫 토큰 중앙값(초) | 전체 응답 중앙값(초) | 검사 통과 |
| -------------------------------- | --------- | ------------------ | -------------------- | --------- |
| 파이썬 코드 리뷰                 | 208       | 0.316              | 4.008                | 3/3       |
| 128개 기록 사건 로그의 실패 찾기 | 9,775     | 4.532              | 5.768                | 3/3       |
| 결제 메모 추출                   | 87        | 0.256              | 2.035                | 3/3       |

코드 리뷰의 생성 속도는 중앙값 30.9토큰/초로,
Frandroid가 Windows ProArt에서 llama.cpp로 잰 29.4와 31.4와 비슷하다.
네 건의 코드 리뷰를 동시에 보내면
중앙 묶음이 5.314초에 끝나 합계 86.6토큰/초가 나왔다. 10분 동안 세 과제를 한
요청씩 돌려 150건을 모두 통과했고,
처음 10회와 마지막 10회의 응답 시간 증가는 1.6% 미만이었다.
측정한 171개 응답이 모두 검사를 통과했다.

## 분석

### 글의 가치는 성능 수치보다 하드웨어 지원 패치와 재현 가능성에 있다

글의 제목은 Microsoft 계정이 없어서라는 동기를 내세우지만,
독자가 얻는 것은 두 가지다.
하나는 공식 지원이 없는 하드웨어를 Linux로 띄운 작업의 공개된 결과물이다.
저장소에는 빌드 스크립트와 패치가 있고 자신의 ACPI 테이블을 덤프하고
ASUS 드라이버 패키지에서 스피커 펌웨어를 로컬로 추출하는 절차가 들어 있다.
다른 하나는 이 하드웨어에서 Linux가 Windows와 비슷한 수준이라는 첫 측정이다.

HN의 hypfer는 이 글에서 배울 것이 무엇이고 어떤 도전을 넘었느냐고 물었고
swiftcoder는 저자가 Linux를 부팅시키려고 쓴 패치 링크를 올렸고
그것이 대수롭지 않은 일이 아니라고
답했다.[^hypfer][^swiftcoder] petercooper는 Windows를 쓰고
싶지 않은 사람으로서 동작한다는 것을 알게 되어 기쁘다고 했다.[^petercooper]
이 교환에서 글의 두 층이 드러난다.
소비로 읽으면 하드웨어 후기이고, 패치와 설치기를 보면 이식 작업이다.

### 메모리 풀의 통합이 이 글이 내세우는 구조적 이점이다

글이 가장 강조하는 것은 Linux가 CPU와 GPU에 같은 116.0GiB를 보여 준다는 점이다.
Windows에서는
전용 GPU 영역과 공유 영역과 CPU 전용 영역으로
나뉘어 한쪽이 다른 쪽의 영역을 쓰지 못한다.
로컬 LLM에는 이 차이가 의미 있다.
모델이 CPU 오프로드와 디스크 지원 임베딩 테이블을 함께 쓰므로
CPU와 GPU가 같은 풀을 보는 편이 편하다.

다만 글이 비교하는 상대는 다른 사람의 Windows 설정이다.
Frandroid의 Windows 환경이 91GiB 전용 예약에서
CUDA 총량 109.7GiB를 보고한 것과 저자의 Linux 116.0GiB를 견주는데,
예약 값을 다르게 잡으면 Windows의 수치도 달라진다.
따라서
통합이 6.3GiB를 더 준다는 비교보다 CPU 작업과 GPU 작업이
풀을 나눠 쓰지 않는다는 구조적 사실이 더 정확한 주장이다.

## 비평

### 모든 비교가 같은 기계의 같은 조건 비교가 아니다

글은 비교의 한계를 스스로 적는다.
HP OmniBook의 7-Zip 결과는 버전과 사전 크기를 밝히지 않으므로
비율은 두 노트북 구성의 비교이고,
ComputerBase의 기계는 64GB 구성에 7-Zip 26.00이며
차트가 사전 크기를 주지 않는다.
Frandroid의 추론은 85GiB 전용 예약에 컨텍스트 한도 262,144토큰이었고
저자는 32,768토큰이었으며
프롬프트와 양자화와 런타임과 시간 측정 방법이 모두 다르다고 직접 쓴다.
저자는 이것이 작동하는 두 구성의 비교이지 운영체제의 효과를 분리한 것이 아니라고
결론짓는다.

이 점은 글의 정직한 부분이지만 제목이 주는 인상과는 거리가 있다.
Linux가 Windows와 비슷하다는 요약은 서로
다른 기계와 설정의 숫자를 나란히 놓은 결과다.
같은 노트북에 Windows와 Linux를 번갈아
올려 같은 벤치마크를 돌린 비교는 글에 없다.

### 추론 실험이 작고 결정적이다

모델 실험은 세 개의 프롬프트를 결정적 디코딩으로 반복한 것이다.
코드 리뷰의 검사는 회귀 출력을 확인하고,
171개 응답이 모두 통과했다는 결과는 세 프롬프트의 반복 통과다.
글도 이것을 세 프롬프트의 반복이라고 밝힌다.
사고 모드를 끈 실행이고 컨텍스트는 32,768토큰이며
적재와 컴파일에 약 16분이 걸린다.

이 실험은 이 하드웨어에서 이 모델이 안정적으로 돌고
시간이 지나도 성능이 거의 유지된다는 점을 보여 준다.
다양한 입력에서 품질이 어떤지나 긴 컨텍스트에서
성능이 어떤지는 보여 주지 않는다.
사건 로그 과제는 9,775 입력 토큰에 답이 39토큰이어서
토큰/초가 아니라 응답 시간이 의미 있다고 저자도 설명한다.

### 글이 다루지 않는 일상 사용의 항목이 남는다

글은 디스플레이가 3840×2400과 120Hz로 동작하고
NetworkManager와 PipeWire와 NVIDIA CDI를 쓰는 rootless Podman을 쓴다고 적는다.
배터리 시간이나 절전과 재개, 무선 랜,
온도와 팬 같은 노트북 일상에 필요한 항목은 글에서 확인되지 않는다.
이 문서는 이 항목들이 동작하는지 알지 못한다.
설치기가 커널과 NVIDIA와 전력 관리와 펌웨어 패키지를 `IgnorePkg`로
고정하는 것은 이 구성이 업스트림 업데이트에 취약하다는 신호이기도 하다.

## 인사이트

### 비공식 지원이 만든 열린 이식은 하드웨어의 쓸모를 넓힌다

글의 동기는 Microsoft 계정이었지만
결과물은 같은 하드웨어를 가진 다른 사람들이 쓸 수 있는 이식이다.
HN의 petercooper는 DGX OS가 먼저 나올 줄 알았다고
했고[^petercooper] jasoneckert는 DGX Spark(Ubuntu)가 있는데
RTX Spark를 왜 사겠느냐며 개발자에게는 OS가 큰 차이이고
DGX Spark의 스택이 성숙하다고 했다.[^jasoneckert] wmf는 RTX Spark가 NIC가 없어서
1,000달러 싸고 노트북 형태도 있다고 답했다.[^wmf]

이 대화를 보면 이 이식이 어디서 필요해지는지 알 수 있다.
노트북이라는 폼팩터를 원하면서
Windows를 원하지 않는 사람에게는 공식 경로가 없고 이식이 그 공백을 채운다.
이 문서의 읽기로는 이 글의 영향은 성능 수치가 아니라 설치기와 패치를 공개해서
같은 기계의 다른 사용자가 같은 일을 반복하지 않게 한다는 데 있다.

### 대역폭이 토큰 속도를 정한다는 질문은 이 하드웨어의 한계를 겨냥한다

HN의 pshc는 Qwen 3.8 Flash Next에서 30토큰/초는 낮다며
24GB 비디오 카드에 RAM 오프로드를 쓰는 전문 엔진이면 약 두 배가 나온다고 했고
wmedrano는 Strix Halo에서
전문 엔진으로 UD-IQ4_XS를 MTP와 함께 돌려 약 60토큰/초를 얻는다고
했다.[^pshc][^wmedrano]
Grimblewald는 보통 한계는 계산이 아니라 메모리 대역폭이며,
pshc의 카드는 두 배 이상의 대역폭을 가졌을 가능성이 높다고
답했다.[^Grimblewald] chem83는 6,000달러짜리 노트북의 강한 용도를 아직
모르겠다며 비슷한 돈으로 96, 128, 192GB 메모리의 AMD 미니 PC를 사서 더 작고
전력 효율이 좋은 노트북으로 원격 접속할 수 있다고
했다.[^chem83] giancarlostoro는 NVIDIA 쪽은 시스템과 GPU의 VRAM을 공유해 GPU에서
AI 모델을 돌리게 하지만 그 시스템은 그렇지 않다고 답했다.[^giancarlostoro]

이 교환에서는 이 노트북의 가치가 메모리 용량에 있고
속도에는 없다는 점이 확인된다.
저자의 30.9토큰/초와 비교된 수치들은 통합된 큰 메모리 덕분에 큰
모델을 올릴 수 있지만 대역폭이 속도를 제한한다는 설명과 맞는다.
이 설명을 이 문서가 측정으로 확인하지는 못했다.

### 로컬 계정이라는 동기는 선택을 정당화하는 이유일 뿐이다

HN의 internet2000은 Microsoft 계정은 무료로 만들 수 있다고
했고[^internet2000] SimianSci는 Windows Pro에서
직장 또는 학교 계정으로 도메인에 가입하는 길로 로컬 계정을 만들 수 있다고
했으며[^SimianSci] delecti는 저자가 Arch 스태프의 패키지 관리자라서
기술적 장애가 아니었을 것이라고
짚었다.[^delecti] colechristensen은 새 Windows 노트북에서
클라우드 계정 없이 설정하는 것이 점점 어려워진다고 했다.[^colechristensen]

글의 제목이 내세운 이유가 이 교환에서 부차적으로 보인다.
글에서 저자의 동기는 오픈 웨이트 모델을 로컬에서 만지는 것이고
이 문서의 읽기로는 Linux를 고른 이유도 공식
지원 밖의 하드웨어를 직접 다루는 데 있었다.
제목은 이 선택의 가벼운 설명이다.

---

[^hypfer]: <https://news.ycombinator.com/item?id=50158387>

[^swiftcoder]: <https://news.ycombinator.com/item?id=50158552>

[^petercooper]: <https://news.ycombinator.com/item?id=50158443>

[^jasoneckert]: <https://news.ycombinator.com/item?id=50158645>

[^wmf]: <https://news.ycombinator.com/item?id=50159273>

[^pshc]: <https://news.ycombinator.com/item?id=50158956>

[^wmedrano]: <https://news.ycombinator.com/item?id=50159147>

[^Grimblewald]: <https://news.ycombinator.com/item?id=50159000>

[^chem83]: <https://news.ycombinator.com/item?id=50158409>

[^giancarlostoro]: <https://news.ycombinator.com/item?id=50158497>

[^internet2000]: <https://news.ycombinator.com/item?id=50158418>

[^SimianSci]: <https://news.ycombinator.com/item?id=50158393>

[^delecti]: <https://news.ycombinator.com/item?id=50159003>

[^colechristensen]: <https://news.ycombinator.com/item?id=50158355>
