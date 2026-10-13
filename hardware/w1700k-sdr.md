# W1700K SDR: Wi-Fi 7 공유기를 320Msps 광대역 수신기로

<https://github.com/h0m3us3r/w1700k-sdr>

HN 토론: <https://news.ycombinator.com/item?id=50055593> (295점, 81개 댓글)

GN 토론: <https://news.hada.io/topic?id=35258>

## 소개

W1700K SDR은 Gemtek W1700K Wi-Fi 7 공유기를
광대역 소프트웨어 정의 수신기(SDR)로 바꾸는 프로젝트다.
공유기 안의 MediaTek MT7996 무선 칩이 14비트 원시 IQ를 최대 320Msps로 받고,
Airoha AN7581 SoC가 그 데이터를 10GbE로 내보내며,
Linux 호스트가 브라우저에서 실시간 스펙트럼과 워터폴,
수신기 조작 화면을 보여 준다.
README 맨 위의 화면은 2.4GHz 대역 전체를 320Msps로 받아
모든 샘플에 262,144점 FFT를 초당 100번 돌린 결과다.

핵심은 MT7996이 이 프로젝트의 펌웨어만 돌린다는 점이다.
ROM 패치, WM, WA 펌웨어를
모두 저장소에서 빌드하며 MediaTek 코드는 들어 있지 않다.
MediaTek 펌웨어의 레지스터 접근을 하나하나 기록한 추적을 해독해
초기화와 보정 절차를 다시 써서, 전원을 처음 넣은 무선 칩을 스스로 깨운다.
호스트는 LO, 샘플링 속도, 캡처, 스트림, 이득, 필터를 명령으로 보낸다.

저장소는 2026년 10월 11일 만들어졌고, 10월 13일 기준 스타 421개,
커밋 9개가 모두 h0m3us3r 한 사람에게서 나왔다.
라이선스는 기본 MIT이고,
Linux 드라이버와 커널 패치는 GPL-2.0-only, U-Boot 패치는 GPL-2.0+,
MediaTek mt76 드라이버에서 파생한 파일은 BSD-3-Clause-Clear다.

## 주요 사양

| 항목       | 내용                                                                                                        |
| ---------- | ----------------------------------------------------------------------------------------------------------- |
| 샘플링     | 모든 대역에서 40·80·160·320Msps, 14비트 복소 IQ. 2번 대역은 640Msps의 짝수 샘플만 받는 640/2도 지원         |
| 대역       | 2.4GHz(MT7976), 5GHz·6GHz(MT7977 두 개). 스트림 중 레지스터 하나로 대역 전환                                |
| 튜닝       | 채널 개념 없이 합성기가 잠기는 임의 주파수. 2.98Hz(2.4GHz) 또는 11.9~14.3Hz 격자, 스트림 중 약 1ms에 재튜닝 |
| 프런트엔드 | AGC 또는 수동 LNA·기저대역 이득, 아날로그 필터 20~320MHz                                                    |
| 전송       | SoC DRAM의 1GiB 링 버퍼, 8KiB 조각마다 UDP 데이터그램 하나를 무복사로 10GbE 전송                            |
| 호스트     | `w1700k-stream`이 공유 메모리로 IQ 배포, `w1700k-spectrum`이 FFT와 웹 UI, `sdr-recv`가 기록                 |

## 동작 방식

### 데이터 경로

A-die(LNA, 믹서, LO, 아날로그 필터)가 만든 아날로그 IQ를
MT7996 PHY의 캡처 엔진이 받아 SYSRAM 풀 1MiB를 링으로 쓴다.
WM 펌웨어의 생산자 루틴이 캡처 포인터를 따라가며 8KiB 조각을 내놓고,
MCU DMA가 PCIe를 거쳐 AN7581 DRAM의 1GiB 링(8KiB 조각 131,072개)에 쓴다.
이 링은 사용자 공간에 읽기 전용으로 매핑되고 복사되지 않으며,
커널이 조각마다 UDP 데이터그램 하나를 페이지를 붙인 채로 10GbE로 보낸다.
호스트의 `w1700k-stream`은 수신 스레드 8개로 받아 순서를 맞추고 압축을 풀어
복소 int16 공유 링으로 여러 소비자에게 나눠 준다.

대역폭 계산이 이 설계를 정한다.
320Msps × 32비트는 무선 칩에서 초당 1.28GB이고,
10GbE 링크 하나는 약 1.24GB/s의 페이로드를 나른다.
그래서 조각의 절반을 MT7996 안에서 IQ 쌍당 28비트로 압축(8KiB → 7KiB)해
링크를 약 97%로 쓴다.
1GiB 링은 최대 속도에서 약 0.8초의 짧은 정체를 흡수한다.

### 초기화와 제어

호스트가 ROM 패치, WM, WA를 내려보내고 공유기의 보정 EEPROM을 WM에 쓰면,
WM이 차가운 무선 칩을 약 2초 만에 깨운다.
BRINGUP 단계는 MediaTek ROM 패치가 하던 일,
즉 수정 발진기, 핀 다중화, 대역별 보정 펄스,
A-die 초기화, eFuse 트림을 다시 한다.
FILTER와 SETUP은 대역의 LO와 대역폭 등급만으로 필요한 표와 설정을 계산하고,
그 LO에서 DC 오프셋 보정을 한다.
CAPTURE는 캡처 경로와 MAC 수신을 켠다.
송신 보정과 송신 전력 제어는 빼서 MAC의 송신 경로는 꺼진 채로 남는다.

스트림 중에도 RF 명령을 처리한다.
WM은 각 명령의 레지스터 프로그램을 만들어 스트림 조각 사이에 조금씩 실행하므로
재튜닝이 320Msps 스트림을 멈추지 않는다.
각 프로그램에는 시작과 끝의 조각 번호가 찍혀서
설정 변경 이후의 샘플을 정확히 골라낼 수 있다.

### 펌웨어를 직접 쓰기까지

로드맵 문서는 펌웨어를 자기 것으로 만든 과정을 여섯 단계로 정리한다.
먼저 자체 WM과 WA를 MT7996에 올렸고,
MediaTek 초기화에서 캡처한 레지스터 상태를 재생해 무엇이 필요한지 찾았다.
그다음 전원을 끈 장치에서
MediaTek 펌웨어의 모든 레지스터 접근과 A-die SPI 접근을
69번의 콜드 로드에 걸쳐 보정 항목 하나씩 기록하고,
각 절차를 기록 단위로 재생성했다.
수신에 필요한 것만 남기도록 벤치에서 MediaTek 펌웨어와 비교해 줄이고,
각 절차를 헤더 파일에서 C로 다시 쓴 뒤
하드웨어에 올리기 전에 호스트에서 추적과 접근 단위로 대조했다.
결과는 전원을 껐다 켠 장치에서 측정된 보정 코드를 빼면
MediaTek 로드와 레지스터 단위로 같은 상태를 만들고,
모든 대역에서 똑같이 수신한다고 한다.

## 시작하기

필요한 것은 W1700K(HW 1.x)나 W1700K2(HW 2.1),
콘솔 헤더에 연결할 3.3V USB 시리얼 어댑터,
설치용으로 `lan3` 포트에 연결할 이더넷 케이블,
그리고 `wan` 포트에 연결할 10GbE NIC(10GBASE-T)다.

```sh
make                                   # 공개 소스에서 전부 빌드 (약 10분과 다운로드 시간)
make check                             # 테스트

sudo init/host/link up IFACE           # lan3에 연결한 NIC에 192.168.1.10/24
sudo init/host/tftp-forward enable IFACE
init/install                           # NAND 백업, 설치, 무선 보정값 저장

sudo init/host/link up IFACE10G 10.77.0.10/24 9216    # 10GbE 스트림 링크
host/stream/build/w1700k-stream &
host/spectrum/build/w1700k-spectrum --controller "host/bin/w1700k serve" --listen 0.0.0.0:8073
```

브라우저에서 `http://HOST:8073/`을 열고 ▶을 누르면 된다.
브라우저 없이도 `host/bin/w1700k load|start|band|tune|gain|filter|stop|status`로
같은 일을 할 수 있다.
빌드에는 C/C++ 컴파일러, Python 3.10 이상, Buildroot 필수 패키지,
RISC-V 펌웨어용 clang·ld.lld·llvm-objcopy, 펌웨어 컨테이너 암호화용 openssl,
`libfftw3-dev`와 `zlib`이 필요하고 벤더 펌웨어는 받지 않는다.

## 함정

- 펌웨어는 수신 전용이고 송신 경로를 꺼 두지만,
README는 안테나 포트를 감쇠기 없이 민감한 계측기에 바로 연결하지 말라고 경고한다.
- 이 프로젝트의 ROM 패치는 eFuse를 쓰지 않는다.
README에 따르면 2025년 이후 MediaTek ROM 패치는 처음 실행될 때 eFuse 게이트 비트 하나를 영구히 설정한다.
- 설치는 공장 운영체제를 대체한다.
`init/install`이 먼저 NAND 데이터를 호스트에 복사하니 그 사본을 보관해야 하고,
`init/restore`로 되돌릴 수 있다.
- 일부 W1700K2에 들어간 W25N04LV NAND는 지원하지만 실제 장치에서 돌려 본 적이 없어서,
설치 스크립트가 별도 플래그 없이는 멈추고 원시 덤프를 요청한다.
- 문서화되지 않은 MT7996이나 AN7581 주소에 접근하면 SoC가 멈추거나
전원을 껐다 켤 때까지 무선 칩이 굳을 수 있다.
`include/hw/`가 알려진 위험을 모두 표시해 둔다.
- 각 대역폭 등급의 데시메이션은 나이퀴스트의 약 60%부터 감쇠해(94%에서 −19dB)
가장자리 레벨이 떨어진다.
스트림의 “flatten” 보정이 이를 샘플 자체에서 바로잡는다.

## 비평

### 문서는 재현 가능성을 강조하지만 검증한 사람은 아직 한 명이다

저장소는 공개된 지 이틀이 안 되었고 커밋 9개가 모두 한 사람의 것이다.
문서는 레지스터 단위의 대조와 69번의 콜드 로드를 말하지만,
다른 사람이 다른 장치에서 같은 결과를 얻었다는 보고는 아직 없다.
W25N04LV NAND를 실제로 돌려 본 적이 없다는 고백처럼
README 스스로 시험 범위의 한계를 밝히고 있다.
HN에서 tverbeure가 장치를 주문해 다음 날 받는다고 적은 것처럼,[^tverbeure]
이 프로젝트의 진짜 검증은 이제부터 시작된다.

### AI로 만든 역공학이라는 의심과 그 답

HN의 asdff는 짧게 Claude에게 감사한다고 비꼬았다.[^asdff]
ChuckMcM은 BRINGUP 절차를 설명한 문장들을 인용하며
문체를 문제 삼았다.[^ChuckMcM]
Aurornis는 누군가 하드웨어를 하네스에 걸어 놓고
자기 토큰으로 역공학해 공개했다면 고마운 일이라며,
1년 전에는 이런 “바이브 역공학” 프로젝트들이 주장한 일조차
하지 못하는 경우가 많았지만 이제는 다르다고 답했다.[^Aurornis]
ctmlr은 문제 영역을 잘 모르면 GPT로 이런 소프트웨어를 쓸 수 없다며,
이해는 아직 AI가 대체할 수 없다고 덧붙였다.[^ctmlr]

저자의 방법론은 이 논쟁에 답을 준다.
모든 절차를 MediaTek 펌웨어의 실제 레지스터 접근 기록과 대조하고,
하드웨어에 올리기 전에 호스트에서 접근 단위로 비교했다는 것이다.
누가 코드를 썼든 그 검증 장치가 신뢰의 근거가 된다.
다만 그 대조 결과와 추적 기록 자체가 저장소에 공개되어 있지 않다면,
독자는 그 검증을 확인할 방법이 없다.

### “공유기를 SDR로”라는 표현은 정확하지만 오해를 부른다

jeffbee는 정확한 설명은 “SDR을 SDR로 바꾸기”라고 꼬집었고,[^jeffbee]
yonatan8070은
“잠긴 단일 목적 SDR을 범용 SDR로”가 더 맞다고 답했다.[^yonatan8070]
BlackRabbit1은 모든 Wi-Fi 모뎀에 제조와 인증 시험을 위한 테스트 모드가 있고,
이를 통해 전체 스펙트럼을
읽어 낼 수 있는 것으로 보인다고 설명했다.[^BlackRabbit1]
즉 하드웨어는 원래 그 능력을 가지고 있었고,
이 프로젝트가 한 일은 그 능력을 벤더 펌웨어 바깥에서 쓸 수 있게 열어 준 것이다.

## 인사이트

### 가장 싼 고속 SDR은 이미 우리 집에 있다

HN의 aftbit은 직류부터 가시광까지는 아니지만
5GHz에서 320Msps 수신기를 이보다 싸게 얻는 방법을 모른다고 했다.[^aftbit]
zdw는 Amazon에서 80달러에 파는 제품을 찾았다.[^zdw]
tverbeure는 대부분의 기성 SDR 플랫폼이 사양이 훨씬 낮고
거의 모두 같은 Analog Devices 트랜시버 칩을 쓴다고 짚었다.[^tverbeure-spec]

이 가격 격차는 Wi-Fi 칩의 대량 생산이 만든 것이다.
수억 대씩 팔리는 공유기 칩은 전문 SDR보다 훨씬 높은 사양을 훨씬 싸게 담고 있다.
같은 저자가 ESP32 Wi-Fi 마이크로컨트롤러로
SDR을 만든 eSpDR도 있다고 yonatan8070은 소개했고,[^yonatan8070-esp]
thebeardisred는 같은 칩셋을 쓰는
Banana Pi R4에서도 동작할 것이라고 봤다.[^thebeardisred]
범용 Wi-Fi 하드웨어가 열리면 SDR의 가격 하한선이 한 번에 내려간다.

### 벤더 펌웨어를 다시 쓰는 일이 새로운 의미의 수리권이 된다

이 프로젝트가 결국 한 일은 벤더가 잠근 하드웨어에서
벤더 코드 없이 같은 기능을 재현한 것이다.
MediaTek ROM 패치가 eFuse 비트를 영구히 설정한다는 README의 경고는
벤더 펌웨어가 하드웨어 상태를 되돌릴 수 없게 바꾸고 있다는 뜻이기도 하다.
자기 펌웨어를 쓸 수 있다는 것은 하드웨어의 수명과 용도를
벤더가 아니라 소유자가 결정할 수 있다는 뜻이다.

### 송신 능력이 열리면 질문이 달라진다

crest는 샘플을 송신까지 할 수 있다면 여러 대를 묶어
재미있는 대역에서 DIY 위상 배열을 만들 수 있을 것이라고 했다.[^crest]
현재 펌웨어는 수신 전용이고 송신 경로를 꺼 두었다.
그 선택은 기술적 한계라기보다 책임 있는 공개 방식에 가깝다.
송신은 전파법과 다른 사용자에 대한 간섭 문제를 가져오고,
수신과 달리 그 영향이 장치 바깥에 미친다.
범용 Wi-Fi 하드웨어를 SDR로 여는 흐름이 계속된다면,
송신을 어떻게 다룰지가 이 생태계의 다음 쟁점이 될 것이다.

---

[^tverbeure]: <https://news.ycombinator.com/item?id=50062006>

[^asdff]: <https://news.ycombinator.com/item?id=50059315>

[^ChuckMcM]: <https://news.ycombinator.com/item?id=50059403>

[^Aurornis]: <https://news.ycombinator.com/item?id=50059737>

[^ctmlr]: <https://news.ycombinator.com/item?id=50062707>

[^jeffbee]: <https://news.ycombinator.com/item?id=50059440>

[^yonatan8070]: <https://news.ycombinator.com/item?id=50060681>

[^BlackRabbit1]: <https://news.ycombinator.com/item?id=50060849>

[^aftbit]: <https://news.ycombinator.com/item?id=50058986>

[^zdw]: <https://news.ycombinator.com/item?id=50061285>

[^tverbeure-spec]: <https://news.ycombinator.com/item?id=50060705>

[^yonatan8070-esp]: <https://news.ycombinator.com/item?id=50059772>

[^thebeardisred]: <https://news.ycombinator.com/item?id=50059739>

[^crest]: <https://news.ycombinator.com/item?id=50060651>
