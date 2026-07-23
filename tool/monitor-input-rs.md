# monitor-input-rs — DDC/CI로 모니터 입력 소스를 바꾸는 CLI

> Command line tool to change input sources of display monitors with DDC/CI.

<https://github.com/kojiishi/monitor-input-rs>

GN 토론: <https://news.hada.io/topic?id=31632>

## 소개

monitor-input-rs는 DDC/CI(Display Data Channel / Command Interface) 프로토콜로
모니터 입력 소스를 커맨드라인에서 전환하는 Rust 도구다.
Windows, macOS, Linux를 지원하며, Cargo로 설치할 수 있다.

```bash
cargo install monitor-input
```

연결된 모니터 목록을 확인하고 특정 입력으로 전환하거나, 여러 입력 소스를 순환할 수 있다.

```bash
monitor-input                  # 모니터 목록 확인
monitor-input U2723=dp1        # 특정 입력으로 전환
monitor-input P3223=hdmi1,usbc2  # 두 입력 사이 순환
```

모니터 이름 또는 인덱스로 대상을 지정하고, 다중 모니터를 동시에 제어할 수 있다.
라이브러리로도 사용 가능하며 docs.rs에 API 문서가 제공된다.
v1.2.8 기준 GitHub 스타는 43개다.

## 분석

### 물리 KVM 없이 다중 기기 워크스테이션을 구성할 수 있다

멀티 호스트 환경에서 모니터 입력 전환은 오랫동안 물리 KVM 스위치나 모니터 OSD 메뉴에 의존해 왔다.
monitor-input-rs는 이 작업을 셸 명령 하나로 줄인다.

xguru는 DELL U4025QW 모니터로 Windows(DisplayPort)와 Mac(USB-C) 사이를 셸 앨리어스로 전환한다고 보고했다.[^xguru]
이 패턴은 핫키나 스크립트와 결합하면 물리 KVM 없는 다중 호스트 워크스테이션을 구성할 수 있다는 것을 보여준다.

DDC/CI는 1998년에 VESA가 표준화한 프로토콜이다.
오래된 표준이지만 모니터 제조사마다 구현 차이가 있어 호환성이 일정하지 않다.

### Rust 선택이 크로스플랫폼 CLI에 자연스럽게 맞는다

Windows, macOS, Linux를 모두 지원하는 저수준 하드웨어 접근 도구에 Rust가 선택됐다.
플랫폼별로 DDC/CI 접근 방식이 다르다 — Windows는 MCCS API, macOS는 CoreDisplay, Linux는 i2c-dev.
Cargo를 통한 단일 설치 명령은 이 복잡성을 사용자에게 숨긴다.

라이브러리로도 배포된다는 점은 이 도구를 다른 자동화 스크립트나 스위처 앱에 임베드할 수 있다는 의미다.
daydreamblend은 세 기기를 전환하기 위해 Raspberry Pi/ESP32로 커스텀 솔루션을 구축했는데,
이 도구가 있었다면 훨씬 단순하게 해결됐을 것이라고 밝혔다.[^daydreamblend]

## 비평

### DDC/CI 구현 차이로 호환성이 보장되지 않는다

DDC/CI는 표준이지만 구현이 모니터마다 다르다.
loblue는 Ubuntu 24.04에서 의존성을 설치했음에도 동작하지 않는다고 보고했다.[^loblue]
Linux에서는 커널 i2c-dev 모듈 로드와 사용자 그룹 권한 설정이 추가로 필요한 경우가 있다.

도구가 의존하는 DDC/CI 지원은 모니터 펌웨어 구현에 달려 있다.
일부 모니터는 DDC/CI를 부분적으로만 구현하거나, 특정 명령에 응답하지 않는다.
README에 이 한계가 명시되어 있지 않아 사용자가 직접 시행착오를 겪어야 하는 경우가 생긴다.

### OSD 기반 대안과의 비교가 부재하다

yshrust는 Dell Display Manager(DDM)를 핫키와 함께 이미 사용하고 있으며,
이 도구를 써볼 의향이 있다고 했다.[^yshrust]
DDM 같은 공식 소프트웨어는 제조사 지원을 받고, 더 안정적인 DDC/CI 통신을 보장한다.

monitor-input-rs가 DDM을 대체하는 이점 — 범용성, 스크립트 통합, 비-Dell 모니터 지원 — 을
문서에서 명시적으로 다루지 않는다.
사용자가 트레이드오프를 스스로 평가해야 한다.

## 인사이트

### 셸 앨리어스 하나가 물리 장치를 대체한다

“모니터 입력 전환”은 물리 버튼을 눌러야 하는 일이라는 고정관념이 있다.
monitor-input-rs는 이 작업을 `alias mac='monitor-input U2723=usbc1'` 한 줄로 바꾼다.
물리 KVM 스위치가 50~200달러인 것을 감안하면, Rust CLI 하나가 하드웨어 구매를 대체할 수 있다.

이 패턴은 단순한 입력 전환에 그치지 않는다.
스크립트와 결합하면 “Mac 모드로 전환 시 조명, 오디오 기기, 모니터 입력을 동시에 바꾸는” 자동화가 가능하다.
홈 오피스 환경에서 다중 호스트를 쓰는 개발자에게 실질적인 도구다.

### 오래된 표준을 현대적 도구로 감싸는 패턴

DDC/CI는 1998년 표준이다.
이미 존재하는 표준에 현대적 CLI 인터페이스를 씌우는 것이 이 프로젝트의 본질이다.
ddcutil(Linux), MonitorControl(macOS) 같은 선행 도구들도 같은 접근을 취했다.

Rust로 크로스플랫폼 구현을 한 번에 제공한다는 점이 차별화된다.
오래된 표준을 현대 도구체인으로 감싸는 이 패턴은 오픈소스 생태계에서 반복적으로 가치를 만들어낸다.
하드웨어 인터페이스, 파일 포맷, 네트워크 프로토콜 — 어디서나 같은 기회가 있다.

---

[^xguru]: <https://news.hada.io/topic?id=31632#cid62061>
[^daydreamblend]: <https://news.hada.io/topic?id=31632#cid62082>
[^loblue]: <https://news.hada.io/topic?id=31632#cid62060>
[^yshrust]: <https://news.hada.io/topic?id=31632#cid62058>
