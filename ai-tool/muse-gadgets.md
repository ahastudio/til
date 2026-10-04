# Muse Gadgets: ESP32 보드와 Raspberry Pi를 Meta의 Muse 에이전트에 연결하는 오픈소스 SDK

<https://gadgets.muse.ai/>

<https://github.com/facebookincubator/muse-gadget-sdk>

HN 토론: <https://news.ycombinator.com/item?id=49937504> (241점, 108개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49938066> (2점, 3개 댓글)

GN 토론: <https://news.hada.io/topic?id=34702>

## 소개

Muse Gadgets는 Meta의 개인 AI 에이전트 Muse에 직접 만든 기기를 연결하게 해 주는
사이트이자 오픈소스 SDK다.
Muse 자체는 이 저장소의 `ai-tool/meta-muse.md`에 정리되어 있다.
사이트의 표제는 “Open source hardware for your Muse”이고,
기성품 ESP32 보드를 프로그래밍하거나 Raspberry Pi를 설정해 Muse를 디스플레이,
버튼, 센서, 액추에이터, 작업대에 굴러다니는 무엇이든에 연결하라고 소개한다.
코드는 GitHub의 `facebookincubator/muse-gadget-sdk` 저장소에 있으며 Apache 2.0
라이선스로 공개되었다.
GitHub API 기준으로 저장소는 2026년 10월 2일에 만들어졌고,
확인한 시점에 별이 929개였다.

사이트와 README는 이것이 해커가 해커를 위해 재미로 만든 것이라고 강조한다.
보드가 벽돌이 되거나, 보증이 무효가 되거나,
전압 강하나 파산이 생길 수 있으니 각자 책임지고 진행하라는 문장도 있다.
SDK는 두 갈래다.
ESP32 Device SDK는 ESP32 보드에 올리는 펌웨어이고,
Linux Device SDK는 Raspberry Pi 같은 Linux 컴퓨터를 Muse 기기로 만든다.

나는 이 SDK를 직접 설치하거나 보드에 올려 보지 않았다.
아래 내용은 사이트, 하위 페이지, 저장소 README에서 확인한 것이다.

## 구성

### ESP32 Device SDK

ESP32 호환 보드에 이 펌웨어를 올리면 Muse가 집의 Wi-Fi에 연결된다.
홈 네트워크 터널을 지원하는 보드에서는 Muse가 이미 가진 기기와 로컬 HTTP API로
만든 기기에 닿을 수 있다.
가장 빠른 시작점은 상태 표시등과 BOOT 버튼이 달린 ESP32-C5 DevKitC-1이다.
README는 이 보드를 포함해 열일곱 종의 보드를 표로 정리하며,
그중 일부는 움직이는 아바타, 푸시투토크, 설정 화면을 갖춘 전체 화면 UI를 돌린다.
나머지는 표시등, LED 링, 간단한 상태 화면으로 상태를 보여 준다.

Muse의 응답은 텍스트다.
푸시투토크로 음성 메모를 보내면 Muse가 받아 적고 글로 답하며,
화면이 있는 보드는 그 답을 자막으로 보여 준다.
말로 듣고 싶으면 응답 텍스트를 원하는 TTS API로 보내 재생하면 되고,
README는 PSRAM이 있는 보드에서 `components/muse/muse_chat_session.cpp`의
`start_tts`가 그 자리라고 짚는다.
PSRAM이 없는 클래식 ESP32와 ESP32-C6는 메모리가 모자라 홈 네트워크 터널 없이
돌지만 Muse가 기기를 제어할 수는 있다.

### Linux Device SDK

Linux SDK를 설치하고 페어링하면 Muse가 그 컴퓨터에서 명령을 실행하고
파일을 옮길 수 있다.
Bluetooth가 있는 Raspberry Pi 3B+, 4, 5, Zero 2 W가 대상이고,
Bluetooth LE가 있는 다른 Linux 컴퓨터도 된다.
Raspberry Pi OS Bullseye 이상, Debian 11 이상,
Ubuntu 22.04 이상과 sudo 권한이 있는 계정이 필요하다.
Muse가 쓸 수 있는 명령은 네 가지다.

| 명령            | 하는 일                                             |
| --------------- | --------------------------------------------------- |
| `system.run`    | 셸 명령을 실행하고 출력과 종료 코드를 돌려준다      |
| `file.read`     | 파일을 64KB씩 읽는다                                |
| `file.write`    | 파일을 64KB씩 쓰고, 다 쓴 뒤에만 기존 파일을 바꾼다 |
| `device.health` | 가동 시간, 부하, 메모리, 디스크, 온도를 보고한다    |

명령은 설치한 계정의 권한 그대로 실행된다.
README는 그 계정이 sudo를 쓸 수 있으면 Muse도 쓸 수 있다고 분명히 적는다.

### Muse Home Link

Home Link는 Meta가 직접 만든 USB-C 기기다.
ESP32-C5 칩(240MHz 32비트 RISC-V)에 PSRAM 8MB, 플래시 8MB,
Wi-Fi 6(2.4GHz와 5GHz)을 갖췄고 크기는 35 × 42 × 10mm다.
펌웨어는 오픈소스 ESP32 Device SDK를 바탕으로
하지만 Home Link 자체는 공식 펌웨어만 돌고 다시 굽을 수 없다.
미국의 유효한 Muse 구독자에게 한 명당 하나씩 무료로 주며 10월에
선착순으로 배송한다고 한다.
Home Link 페이지에 대한 HN 글에서 big_toast는 Nat Friedman이 Home Link를 5,000개
만들었다고 Twitter에 쓴 문장을 옮겼다.[^big_toast]
이 수치는 사이트에는 없고 댓글이 인용한 것이다.

### 커뮤니티 스킬

저장소의 `skills/` 디렉터리에는 Philips Hue, Sonos, Apple TV, Google Nest,
Samsung TV, Roborock 같은 기기를 Muse로 다루는 커뮤니티 스킬이 기기마다
`gadget-<기기 이름>/SKILL.md` 형태로 들어 있다.
README는 이것이 공식 통합이 아니라고 밝힌다.
쓰려면 Muse 채팅에 저장소 링크를 주고 필요한 스킬을 찾게 하거나,
카탈로그에서 기기를 찾아 `SKILL.md`를 붙여 넣는다.
기여는 마크다운만으로 하라고 한다.
Home Link 페이지는 스킬이 커뮤니티가 만든 것이라 바뀌거나 깨질 수 있으니 집
보안, 응급, 의료처럼 안전이 중요한 일에 기대지 말라고 경고한다.

## 시작하기

### 토큰부터 받는다

모든 기기는 페어링하려면 SDK 토큰이 필요하고,
자기가 쓰려고 만든 기기도 마찬가지다.
토큰은 `gadgets.muse.ai`의 Account > SDK tokens에서 받는다.
페어링은 iOS나 Android의 Muse 앱에서 Settings > Devices에 들어가 Developer
mode를 켠 뒤 `MuseGadget`으로 시작하는 기기를 추가하는 방식이다.

### ESP32 보드에 직접 올리기

README는 Muse Code 같은 코딩 에이전트에게 맡기는 길을 먼저 안내한다.
각 디렉터리의 `AGENTS.md`에 툴체인 설정, 보드별 빌드, 플래시,
로그 읽기가 정리되어 있어 에이전트가 이를 읽고 진행한다.
이때 `muse --disable-sandbox`로 실행해야 USB 시리얼 포트에 닿고 ESP-IDF 툴체인을
내려받을 수 있으며, 명령마다 사용자가 승인한다.
직접 하려면 ESP-IDF v6.0.1이 필요하고 다른 버전은 지원하지 않는다.

```bash
git clone -b v6.0.1 --recursive https://github.com/espressif/esp-idf.git ~/esp/esp-idf-v6
~/esp/esp-idf-v6/install.sh esp32c5,esp32s3,esp32c6,esp32
. ~/esp/esp-idf-v6/export.sh   # 빌드할 새 터미널마다 다시 실행한다

git clone https://github.com/facebookincubator/muse-gadget-sdk
cd muse-gadget-sdk/esp32
idf.py menuconfig              # ESP32 Device SDK > Muse Gadgets SDK token 에 토큰을 넣는다
idf.py build                   # 기본 대상은 ESP32-C5 DevKitC-1
idf.py -p /dev/cu.usbmodem1101 flash monitor   # 포트는 ls /dev/cu.usb* 로 확인한다
```

다른 보드는 `tools/board.sh <보드> build`처럼 보드별 설정으로 빌드한다.
플래시가 끝나면 상태 표시등의 색으로 단계를 확인한다.

| 표시등       | 뜻                              |
| ------------ | ------------------------------- |
| 주황, 숨쉬기 | 설정 준비 완료                  |
| 파랑, 숨쉬기 | 버튼을 눌러 페어링 확인         |
| 파랑         | Wi-Fi에 접속하고 Muse에 연결 중 |
| 초록         | 연결됨                          |
| 노랑, 깜빡임 | 다시 연결 중                    |
| 보라         | 페어링되지 않음                 |
| 빨강, 깜빡임 | 문제 발생, 로그 확인            |

버튼을 5초 누르면 기기를 초기화한다.
보드 없이 UI를 고치려면 `simulator/`의 데스크톱 미리보기를 쓴다.

### Raspberry Pi에 설치하기

설치 스크립트는 먼저 내려받아 읽은 뒤 실행하라고 README가 권한다.

```bash
curl -fsSL https://raw.githubusercontent.com/facebookincubator/muse-gadget-sdk/main/linux/install.sh -o install.sh
less install.sh                       # 먼저 읽는다
bash install.sh --sdk-token mgst_…    # Muse가 쓸 계정으로 실행한다
```

설치기는 `/opt/musegadget`에 필요한 것을 넣고 `musegadget` 서비스를 시작하며,
계정을 Muse에 넘기기 전에 묻고 그 계정이 sudo를 쓸 수 있는지 알려 준다.
페어링 창은 10분 동안 열리고,
나중에 다시 페어링하려면 `sudo musegadget pair`를 실행한다.
기기의 다른 프로그램은 자격 증명 없이 `musegadget send-user-msg`로 Muse에
메시지를 보낼 수 있고, `--session-id`를 주면 별도 대화로 보낸다.

```bash
musegadget send-user-msg "The garage door has been open for an hour."
bash install.sh --run-as someone      # sudo 없는 다른 계정에 Muse를 넘긴다
bash install.sh --uninstall           # 제거한다(--purge를 더하면 페어링도 잊는다)
```

## 함정

### Linux 기기에서는 설치한 계정이 곧 Muse의 권한이다

`system.run`은 임의의 셸 명령이고, 계정이 sudo를 쓸 수 있으면 Muse도 그렇다.
Muse가 클라우드에서 도는 에이전트라는 점을 생각하면, 이 기기는 원격
에이전트에게 내 네트워크 안의 셸을 주는 것과 같다.
README가 `--run-as`로 sudo 없는 계정을 쓸 수 있다고 안내하지만 기본 흐름은
설치한 계정을 그대로 넘긴다.
Muse가 허락 없이 메시지를 읽었다는
보고는 이 저장소의 `ai-tool/muse-read-my-messages.md`와
`ai-tool/muse-ignores-permissions.md`에 있다.
그 보고를 읽은 뒤라면 sudo 없는 전용 계정으로 시작하는 것이 기본값이어야 한다.

### 페어링은 중간자 공격을 막지 못한다

두 README 모두 커뮤니티 기기는 제조사 검증이 없어서 능동적인 중간자 공격을
막을 수 없다고 적는다.
페어링은 기기의 버튼을 누르거나 기기에서 직접 명령을
실행해야 열리고 설정할 때마다 새 암호화 세션을 만들지만,
믿을 수 있는 네트워크에서 설정하라는 것이 README의 조언이다.

### 토큰은 비밀번호가 아니라 식별자로 다룬다

ESP32 펌웨어에는 SDK 토큰이 그대로 들어간다.
README는 그래서 토큰을 비밀번호가 아닌 식별자로 취급하고,
유출되면 사이트에서 폐기하고 새로 받아 다시 빌드하라고 한다.
보드의 NVS 플래시에는 Wi-Fi 자격 증명과 기기 토큰이 저장되므로, 지원하는
보드라면 `CONFIG_HOMEHUB_NVS_ENCRYPTION`으로 NVS 암호화를 켜라고 강하게 권한다.
암호화하지 않으면 보드를 손에 쥔 사람은 누구나 이를 읽을 수 있다.
빌드는 포함된 개발용 키로 서명되고 Secure Boot는 켜지지 않는다.

### 오픈소스 라이선스와 토큰 약관은 따로 간다

Gadget SDK Terms는 코드가 Apache 2.0이어도 그 라이선스가 토큰에 대한 권리를
주지 않는다고 명시한다.
토큰은 개인적이고 비상업적인 용도로만 쓸 수 있고,
남에게 주는 기기에는 최대 50대까지만 넣을 수 있으며,
판매하거나 공개적으로 내놓는 기기에는 넣을 수 없다.
남에게 기기를 줄 때는 페어링 전에 그 기기가 상대의 정보로
무엇을 하는지 알려야 한다.
SDK와 토큰은 지원되는 제품도 개발자 플랫폼도 아니며 언제든 바뀌거나 멈추거나
회수될 수 있다고 약관이 말한다.
HN의 karmakaze는 사이트가 나만의 것을 만들라고 하면서 토큰과 기기 수 제한,
언제든 깨질 수 있다는 문구를 붙인 것을 들어 나의 것처럼 느껴지지
않는다고 적었다.[^karmakaze]
cheriot은 남의 API를 부르는 데 토큰이 필요한 것은 합리적이라고 답했다.[^cheriot]

## 비평

### 오픈소스 하드웨어라는 표제와 실제 구조가 어긋난다

사이트의 표제는 오픈소스 하드웨어지만 공개된 것은 Meta의 독점 서비스에 붙는
클라이언트 펌웨어와 에이전트다.
Meta가 직접 만든 유일한 하드웨어인 Home Link는 구독이 있어야 받을 수
있고 다시 굽을 수 없다.
HN의 TomGarden은 코드가 오픈소스인 것은 맞지만 Meta의 독점 서비스를
위한 오픈소스 클라이언트일 뿐이고, Meta 인큐베이터 저장소에서 해커가 해커를 위해
만들었다는 말투를 쓰는 것이 풀뿌리 흉내라고 비판했다.[^TomGarden]
Home Link에 대해 big_toast는 펌웨어를 공개한 것은 좋은 출발이지만 Home Link가
공식 펌웨어만 돈다는 점에서 보안상의 함의가 궁금하다고 적었다.[^big_toast]
코드를 읽을 수 있다는 것과 내 기기에서 무엇이 도는지 확인할 수
있다는 것은 다른 문제다.

### 실재하는 대안을 언급하지 않는다

이 SDK가 하는 일, 곧 ESP32 기기를 집의 자동화 허브에 붙이고 언어 모델에게 기기를
다루게 하는 일에는 이미 오픈소스 생태계가 있다.
HN의 usagisushi는 Home Assistant, ESPHome,
HA-MCP나 CLI의 조합이 이미 그 대안이라고 답했다.[^usagisushi]
지원 보드 목록에 Home Assistant Voice Preview Edition이 들어 있다는
점이 그 사실을 보여 준다.
rumblefrog는 몇 주 전 산 Seeed reTerminal E1001에 ESPHome을
올려 아침 브리핑을 띄우고 있었는데 Meta가 이 틈새 해커 제품의 지원을 홍보한다고
신기해했다.[^rumblefrog]
사이트는 이 기존 경로와 비교해 Muse 쪽이 무엇이 나은지 말하지 않는다.
답이 있다면 로컬 장치 대신 클라우드 에이전트가 판단한다는 점일 텐데,
그것은 장점이자 이 SDK의 가장 큰 위험이다.

### 에이전트의 사고 이력과 물리 세계 접근이 같은 발표에 놓인다

Muse는 출시 직후부터 허락 없는 메시지 접근, Amazon의 차단 같은 논란을 겪었다.
이 저장소의 `ai-tool/amazon-blocks-meta-muse.md`와
`security/muse-runtime-export.md`가 그 근접 사례다.
HN의 zmmmmm은 Meta가 이미 위험한 AI 에이전트에게 물리
세계를 제어하는 하드웨어 통합을 해킹할 수 있게 SDK를 배포한다며 무엇이 잘못될 수
있겠느냐고 꼬집었다.[^zmmmmm]
j45는 결정적이지 않은 소프트웨어가 개인 홈 네트워크에 머무는 것이 어떻게 될지
모르겠다고 썼다.[^j45]
frankest는 Home Link 소개 문장을 인용해 LAN 정보와 Wi-Fi 비밀번호,
미래 제품을 위한 무료 연구를 Meta에 넘기는 좋은 방법이라고 비꼬았다.[^frankest]
안전이 중요한 일에 쓰지 말라는 경고는 Home Link 페이지에 있지만,
차고 문과 스마트 플러그 스킬이 같은 저장소에 있다.

### 반대편의 평가도 있다

HN의 belval은 이것이 자기 제품에 들뜬 사내 팀이 에이전트에 기기를 붙일 펌웨어를
내놓은 것일 뿐이고 그 이상으로 볼 필요가 없다며 마음에 든다고 했다.[^belval]
harmoni-pet은 Codex로 저장소를 받아 M5Stack StickS3에 금방 올렸지만 음성
메시지에는 응답하게 하지 못했다고 적었다.[^harmoni-pet]
여기에 anant는 음성 문제가 최근 고쳐져 이제 음성을 넣고 텍스트를 받으며
원하는 TTS API를 쓸 수 있다고 답했다.[^anant]
wonderfuly는 이 하드웨어 SDK 안에 Muse와 통신하는 프로토콜이 들어 있어 이를
별도의 TypeScript SDK로 묶었다고 알렸다.[^wonderfuly]
SDK가 서비스 프로토콜을 사실상 공개한 셈이라는 점은 사이트가
말하지 않은 부수 효과다.

## 기억할 원칙

### 에이전트에게 기기를 줄 때는 권한의 상한을 기기 쪽에서 정한다

Linux SDK에서 Muse의 권한은 설치한 계정의 권한과 같고,
ESP32 SDK에서 Home Link 같은 터널은 Muse가 홈 네트워크의 기기에 닿게 한다.
에이전트가 무엇을 할지는 클라우드에서 정해지지만,
무엇을 할 수 있는지는 기기 쪽에서 정해진다.
sudo 없는 전용 계정, 터널이 없는 보드, 안전이 중요한 기기를 뺀 스킬 목록처럼
기기 쪽에서 상한을 낮추는 것이 사용자가 실제로 쥘 수 있는 유일한 손잡이다.

### 오픈소스 코드와 열린 플랫폼은 다른 질문이다

이 SDK는 코드를 Apache 2.0으로 열었지만 토큰 약관은 플랫폼이
아니라고 스스로 말한다.
코드 라이선스는 고치고 나눌 권리를 주고,
토큰 약관은 연결할 권리를 언제든 거둘 수 있게 한다.
Meta 서비스에 의존하는 기기를 만들 때는 앞의 것이 아니라 뒤의 것이
기기의 수명을 정한다.

---

[^big_toast]: <https://news.ycombinator.com/item?id=49938067>

[^karmakaze]: <https://news.ycombinator.com/item?id=49938304>

[^cheriot]: <https://news.ycombinator.com/item?id=49939790>

[^TomGarden]: <https://news.ycombinator.com/item?id=49939360>

[^usagisushi]: <https://news.ycombinator.com/item?id=49941421>

[^rumblefrog]: <https://news.ycombinator.com/item?id=49940450>

[^zmmmmm]: <https://news.ycombinator.com/item?id=49938809>

[^j45]: <https://news.ycombinator.com/item?id=49940075>

[^frankest]: <https://news.ycombinator.com/item?id=49943309>

[^belval]: <https://news.ycombinator.com/item?id=49938972>

[^harmoni-pet]: <https://news.ycombinator.com/item?id=49940545>

[^anant]: <https://news.ycombinator.com/item?id=49941176>

[^wonderfuly]: <https://news.ycombinator.com/item?id=49944941>
