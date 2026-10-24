# HackiOS: Android 폰에서 iOS 16.5 사용자 영역을 돌리는 XNU 이식 프로젝트

<https://github.com/oosexgang/hackios-xnu-kernel>

HN 토론: <https://news.ycombinator.com/item?id=50196718> (489점, 179개 댓글)

GN 토론: <https://news.hada.io/topic?id=35830>

## 소개

HackiOS는 Apple의 오픈소스 XNU 커널(`xnu-8796.121.2`, iOS 16.5의 커널)을 Android
폰 하드웨어에서 부팅하고, 그 위에서 수정하지 않은 iOS 16.5 사용자 영역을
실행하는 연구 프로젝트다.
`launchd`에서 `backboardd`, SpringBoard, 앱으로 이어지는 흐름이 그대로 돈다.
이를 위해 자체 EFI 로더, Apple의 비공개 드라이버를 대체하는 자체 드라이버, UEFI
이식, 호환 계층 위의 Linux Wi-Fi 드라이버를 만들었다고 한다.

실행 환경은 두 곳이다.
POCO X5 Pro 5G(Snapdragon 778G)에서는 아무것도 기기에 쓰지 않고 시스템 전체를
RAM에 올리며, 재부팅하면 폰이 Android로 돌아온다.
다른 하나는 QEMU(`virt`, aarch64)로, 폰 없이 Linux 컴퓨터에서 같은 일을 한다.
README는 이 프로젝트가 ROM이 아니라 연구 벤치이며, 세션이 정해진 시간 동안
이어진 뒤 커널이 로더로 돌아가 로그를 넘긴다고 설명한다.

저장소는 프로젝트의 절반이다.
이 저장소에는 XNU 패치, EFI 로더, UEFI 이식, Wi-Fi, QEMU 스크립트가 있고, 다른
절반은 `hackios-xnu-userland`(자체 init, 주입 라이브러리, APFS 이미지 빌더,
IPSW에서 iOS를 꺼내는 스크립트, Metal/Mesa 작업)다.
저장소 상태는 2026년 10월 22일에 생성됐고 10월 23일에도 푸시가 있으며, 스타 968,
포크 165, 언어는 C이다(2026년 10월 23일 확인).

## 동작 방식

### Apple의 파일은 저장소에 없고 사용자 기계에서 내려받는다

README는 두 저장소 모두에 Apple 파일이 없다고 밝힌다.
`ios165/fetch.sh`가 Apple의 CDN에서 iOS 16.5 IPSW를 사용자 컴퓨터로 내려받아
필요한 것만 꺼낸다.
프로젝트는 Apple과 관계가 없고 인가나 보증을 받지 않았다고도 적는다.
기기 고유 펌웨어(GPU, Wi-Fi, 오디오, 햅틱)도 저장소에 없고 그 폰의 Android에서
가져와야 한다.

### 커널이 Apple 하드웨어의 빈자리를 메운다

README의 구조도에 따르면 XNU는 BCM2837 설정을 기반으로 하고 여기에 자체 플랫폼
코드를 얹는다.
GICv3와 타이머, 비디오 콘솔, APFS(RAM의 이미지와 플래시의 iOS 볼륨), corecrypto
대신 minicrypto, AMFI와 Sandbox의 대체 구현, IOSurface와 IOMobileFramebuffer와
AppleKeyStore와 네트워크 스택의 드라이버 대체, 터치 입력, Adreno 642L GPU,
Wi-Fi(WCN6750, `ath11k`), 오디오가 포함된다.
iOS 프로그램과 프레임워크, dyld 공유 캐시는 한 바이트도 바꾸지 않고, 빠진 부분은
커널(드라이버 대체) 또는 커널이 `DYLD_INSERT_LIBRARIES`로 주입하는 라이브러리가
메운다고 한다.

### 되는 것과 아직 안 되는 것

README의 표를 요약하면 다음과 같다.

| 되는 것                                                                | 아직 안 되는 것                                         |
| ---------------------------------------------------------------------- | ------------------------------------------------------- |
| 잠금 화면, 홈 화면, 시스템 제스처, 제어 센터, 설정·시계·사진·Safari 등 | 셀룰러, Bluetooth                                       |
| 터치스크린, 멀티터치, 전원·볼륨 키, 최대 CPU 8코어                     | 이 커널에서의 충전(폰이 방전만 된다)                    |
| Adreno GPU(Mesa/freedreno), Wi-Fi 55~90 Mbit/s                         | 앱용 Metal(시스템 셰이더 456개 중 293개 동작)           |
| 소리, 카메라 앱의 전후면 촬영, 재부팅 뒤에도 남는 데이터               | App Store 콘텐츠와 Apple ID 로그인(Secure Enclave 없음) |
| 잠금 화면까지 약 20초                                                  | 동영상과 Live Photo 녹화                                |

라이선스는 저장소가 Apple Public Source License 2.0이다.
XNU 변경분이 XNU의 파생물이라 같은 라이선스여야 하고,
`ath11k`(BSD-3-Clause-Clear)와 FreeBSD LinuxKPI 코드(BSD-2-Clause) 등 제3자
코드는 각자의 라이선스를 유지한다고 적혀 있다.

## 비평

### 되는 목록은 보여 주지만 속도와 안정성은 보여 주지 않는다

README는 기능 표와 세션이 정해진 시간 동안만 이어진다는 문장을 준다.
세션이 얼마나 자주 죽는지, 앱이 얼마나 오래 쓸 만한지, 전력 소모가 얼마인지는
없다.
QEMU 실행의 기본 세션이 20분이고 폰 세션이 15분으로 안내돼 있어서, 상시 사용이
아니라 시연 단위라는 짐작은 가능하지만 이는 이 문서의 추정이다.
Wi-Fi 55~90 Mbit/s 같은 수치만 구체적이다.

### 실용 가치는 질문으로 남았다

HN에서 drnick1은 iOS를 Android에서 돌리는 이유보다 Apple 하드웨어에서 Graphene
같은 자유 배포판을 돌리는 편이 바람직하다고 물었다.[^drnick1]
Wowfunhappy는 이 프로젝트가 완전히 탈옥된 iOS를 얻는 방법이 되고, 커널을
마음대로 고칠 수 있다고 답했다.[^wowfunhappy]
gruez는 App Store 콘텐츠와 Apple ID 로그인이 안 되는 것(Secure Enclave 없음,
FairPlay 데몬 종료)이 드라이버 문제를 다 풀어도 큰 걸림돌이라고 짚었다.[^gruez]
README는 용도를 연구 벤치라고만 밝힌다.

### 보안 모델이 약해진다는 지적

iPhone 보안을 대체하려는 시도가 아니라는 점은 분명하다.
hollowonepl이 이를 바탕으로 iOS판 Graphene OS를 만들 기회가 있느냐고 묻자,
gruez는 iPhone의 부트로더는 잠겨 있고 Android 폰 위의 이 조합은 Graphene보다
보안이 나쁠 것이라고 답했다.[^gruez-graphene]
lunar_rover는 Graphene은 업스트림 지원을 받거나 스스로 업스트림이어야 하는데
비공식 iOS 이식에서는 둘 다 없어, 위협 모델에서 Apple만 공격자일 때가 아니면
기회가 없다고 했다.[^lunar_rover]
README도 AMFI와 Sandbox를 대체 구현으로 바꿨다고 적는데, 이 대체가 보안 경계로서
무엇을 지키는지는 설명하지 않는다.

### 프로젝트 주변의 신뢰 신호가 불안하다

jrmg는 프로젝트 웹사이트에 BNB 체인의 커뮤니티 토큰이 있고 거래마다 1% 수수료가
팀을 지원한다는 문구가 있다고 전했다.[^jrmg]
katzenq는 이것이 도박이 붙은 암호화폐 기부 아니냐고 물었다.[^katzenq]
croes는 이런 AI 프로젝트 중 악성코드가 든 것이 얼마나 되는지 궁금해했고,
dmcrespo는 빠르게 퍼지지만 바이러스나 정보 탈취 여부를 검증할 방법이 없다고
했다.[^croes][^dmcrespo]
이 문서는 웹사이트와 토큰을 직접 열어 보지 않았고, 코드를 감사하지도 않았다.
README의 설치 흐름은 Apple의 CDN에서 7.4 GB를 내려받고 기기 펌웨어를 꺼내는
것이므로, 실행하기 전에 격리된 환경에서 소스를 읽어야 한다는 점만 말해 둘 수
있다.

## 인사이트

### 왜 16.5인가가 이 계열 프로젝트의 한계를 보여 준다

torben-friis와 여러 사람이 왜 16.5냐고 물었다.[^torben-friis]
MBCook은 Apple이 해마다 보안을 높였을 것이라 짐작했고,[^mbcook] LoganDark는 iOS
17부터 Secure Page Table Monitor와 Trusted Execution Monitor가 들어왔다고
답했다.[^logandark]
README에는 버전을 고른 이유가 없으므로 이 설명은 댓글의 해석이다.
이 해석이 맞다면 이식할 수 있는 최신 버전은 Apple의 보안 설계가 하드웨어에
얼마나 묶여 있는가에 따라 정해지고, 그 선이 올라갈수록 비Apple 하드웨어에서 돌릴
수 있는 버전은 점점 뒤처진다.
runjake는 요즘 A·B급 iOS 앱 상당수가 이렇게 오래된 iOS에서는 돌지 않을 것이라
했고, busymom0는 Apple이 지금 앱 제출을 허용하는 가장 오래된 버전이 iOS 15라고
했다.[^runjake][^busymom0]
그래서 이 프로젝트의 가치는 앱 실행이 아니라 이식 가능성의 증명에 있다.

### AI가 만든 프로젝트라는 반발은 질문을 흐린다

LetsGetTechnicl은 Claude로 만든 프로젝트에 지쳤고 스스로 알아냈다면 더 멋졌을
것이라 했다.[^letsgettechnicl]
bigyabai는 iOS 16을 4년 동안 직접 역공학할 수 있었던 사람들이 할 기술적 동기가
없었다고 답했다.[^bigyabai]
README에는 AI 사용에 대한 언급이 없으므로 AI가 얼마나 관여했는지는 이 문서가
확인하지 못했다.
논쟁의 쓸모 있는 부분은 이식의 속도다.
esseph의 말처럼 여러 단계의 시연을 훨씬 짧은 시간에 내놓을 수 있게 되면,
정확성은 나중에 다듬는 것이 된다.[^esseph]
이 방식의 위험은 정확성을 보증하는 사람이 없는 채로 퍼진다는 점이다.

### 이 글을 읽는 방법

이 프로젝트는 구경하고 구조를 읽는 용도로 가장 안전하다.
직접 실행하려면 기기 제약(unlocked bootloader가 있는 특정 폰)과 내려받는 크기와
법적 위험(Apple의 CDN에서 받는 IPSW)을 먼저 따져야 한다.
이 프로젝트의 주장을 가를 관찰은 두 가지다.
세션이 몇 시간 단위로 이어지는지, Apple ID와 App Store 같은 서비스 의존 기능이
어떻게 해결되는지다.
둘 다 해결되지 않으면 이 프로젝트는 이식 기술의 시연으로 남는다.

---

[^drnick1]: <https://news.ycombinator.com/item?id=50198684>

[^wowfunhappy]: <https://news.ycombinator.com/item?id=50199742>

[^gruez]: <https://news.ycombinator.com/item?id=50197563>

[^gruez-graphene]: <https://news.ycombinator.com/item?id=50197550>

[^lunar_rover]: <https://news.ycombinator.com/item?id=50201443>

[^jrmg]: <https://news.ycombinator.com/item?id=50199094>

[^katzenq]: <https://news.ycombinator.com/item?id=50207083>

[^croes]: <https://news.ycombinator.com/item?id=50199103>

[^dmcrespo]: <https://news.ycombinator.com/item?id=50199415>

[^torben-friis]: <https://news.ycombinator.com/item?id=50197421>

[^mbcook]: <https://news.ycombinator.com/item?id=50197991>

[^logandark]: <https://news.ycombinator.com/item?id=50199130>

[^runjake]: <https://news.ycombinator.com/item?id=50199675>

[^busymom0]: <https://news.ycombinator.com/item?id=50204455>

[^letsgettechnicl]: <https://news.ycombinator.com/item?id=50199723>

[^bigyabai]: <https://news.ycombinator.com/item?id=50199852>

[^esseph]: <https://news.ycombinator.com/item?id=50199893>
