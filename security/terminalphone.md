# TerminalPhone

Tor 히든 서비스 위에서 동작하는 익명 암호화 음성 통신 도구.
단일 Bash 스크립트 하나로 설치, 실행, 통화까지 모두 처리한다.

<https://gitlab.com/here_forawhile/terminalphone>

## 핵심 설계 철학

### 단일 파일, 제로 서버

3050줄의 Bash 스크립트 하나가 전체 시스템이다.
별도 서버 인프라가 없다. 계정도, 전화번호도 없다.
`.onion` 주소가 곧 신원이다.

이 선택은 배포 단순성과 공격 표면 최소화를 동시에 얻는다.
"서버를 공격하면 사용자 데이터를 얻는다"는 공격 경로가
존재하지 않는다.

### 반이중(Half-Duplex) 통신의 의도적 선택

v1.0.0에는 전이중(Full-duplex) 스트리밍이 포함되어 있었다.
v1.0.3에서 제거되었다.

> Tor 지연으로 인해 실용성 없음

Tor 회로의 레이턴시는 경로에 따라 1~3초다. 실시간 양방향
스트리밍은 이 레이턴시 하에서 대화를 불가능하게 만든다.
PTT(Push-to-Talk) 방식으로 전환하면 레이턴시가 허용 범위 안에
들어온다. 기술적 한계를 우회하는 대신 UX 모델 자체를 바꾼
결정이다.

워키토키는 Tor와 궁합이 맞다.

## 암호화 파이프라인

### 계층 구조

```text
평문 오디오(Opus 16kbps, 8kHz)
    │
    ▼
공유 비밀 → PBKDF2(10,000회) → 파생 키  ← 파일 암호화용
    │
    ▼
AES-256-CBC 암호화
    │
    ▼
base64 인코딩
    │
    ▼
AUDIO:<b64> 프로토콜 메시지
    │
    ▼
HMAC-SHA256 서명 (선택): nonce:AUDIO:<b64>|signature
    │
    ▼
fd:4 → socat → Tor SOCKS → 수신측 히든 서비스
```

오디오가 이진 데이터로 TCP 스트림에 직렬화되는 대신
base64로 인코딩 후 텍스트 라인으로 전송된다.
제어 채널(PTT, HANGUP 신호)과 데이터 채널(AUDIO)을
동일한 텍스트 스트림에서 프로토콜 메시지로 통합할 수 있다.

### PBKDF2 이터레이션 수의 의도적 차별화

파일 암호화와 비밀 저장에 다른 이터레이션 수를 사용한다.

```bash
# 파일 암호화: 10,000회
openssl enc -"${c}" -pbkdf2 -iter 10000 -pass "fd:3" ...

# 비밀 저장: 100,000회
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -pass "fd:3" ...
```

파일 암호화는 실시간 통화 중 매초 실행된다. 10,000회도
브루트포스를 충분히 어렵게 만들면서 레이턴시를 허용 범위
안에 유지한다.

비밀 저장은 한 번만 실행된다. 100,000회로 오프라인 크래킹
비용을 10배 더 높인다. 공유 비밀이 디스크에 저장될 때의
보호가 더 강해야 하기 때문이다.

### Encrypt-then-MAC 순서

암호화 후 HMAC을 계산하는 순서다. 이 순서가 중요하다.

- MAC-then-Encrypt: 복호화 전에 검증 불가 → Padding Oracle 노출
- Encrypt-then-MAC: 변조된 암호문을 복호화 시도 전에 거부

HMAC-SHA256이 비활성화 상태여도 AES-256-CBC로 기밀성은
유지된다. HMAC은 메시지 인증과 재생 공격 방지를 추가로 제공한다.

### HMAC 프로토콜: nonce 기반 재생 방지

```bash
proto_send() {
    local nonce sig signed_msg
    nonce=$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')
    signed_msg="${nonce}:${msg}"
    sig=$(printf '%s' "$signed_msg" | \
        openssl dgst -sha256 -hmac "$SHARED_SECRET" -r 2>/dev/null | \
        cut -d' ' -f1)
    echo "${signed_msg}|${sig}" >&4 2>/dev/null
}
```

전송 형식: `<nonce>:<message>|<hmac-sha256>`

수신측은 nonce를 로그 파일에 기록하고 중복을 거부한다.
동일한 암호화된 패킷을 재전송하는 재생 공격이 이 nonce
추적으로 차단된다.

HMAC이 활성화되지 않은 경우, 암호화 자체의 무결성에만
의존한다. CBC 모드는 암호문 변조를 감지하지 못하므로
HMAC 비활성화는 의미 있는 보안 약화다.

### 비밀 전달: 파일 디스크립터

v1.1.1에서 도입된 변경이다.

```bash
# fd:3 방식 - 프로세스 목록에서 비밀이 보이지 않음
openssl enc -"${c}" -pbkdf2 -iter 10000 -pass "fd:3" \
    -in "$infile" -out "$outfile" 3<<< "${SHARED_SECRET}"
```

`3<<<` 구문은 here-string을 파일 디스크립터 3으로 연다.
프로세스를 `ps aux`로 조회해도 비밀 값이 보이지 않는다.
로컬 시스템의 모니터링 도구나 다른 사용자에 의한
비밀 노출을 차단한다.

### 임시 파일 이름 불투명화

```bash
uid() {
    head -c6 /dev/urandom | od -An -tx1 | tr -d ' \n'
}

# 사용
local raw_file="$AUDIO_DIR/tx_$(uid).tmp"
local opus_file="$AUDIO_DIR/tx_o_$(uid).tmp"
local enc_file="$AUDIO_DIR/tx_e_$(uid).tmp"
```

각 파일마다 `/dev/urandom`에서 6바이트를 읽어 12자 hex 문자열로
변환한다. `/tmp/audio.opus` 같은 예측 가능한 이름 대신
`tx_a3f1e9c4b200.tmp` 형태가 된다.

TOCTOU(Time-Of-Check-To-Time-Of-Use) 경쟁 조건 공격과
심볼릭 링크 공격을 방지한다.

## Tor 통합 설계

### 히든 서비스가 신원

전통적인 통신 시스템은 서버가 중계한다. 서버가 알면 당국도
안다. TerminalPhone은 서버가 없다. 각 사용자가 Tor 히든
서비스를 직접 구동한다.

torrc를 런타임에 직접 생성한다:

```bash
cat > "$TOR_CONF" << EOF
SocksPort $TOR_SOCKS_PORT
DataDirectory $TOR_DIR/data
HiddenServiceDir $TOR_DIR/hidden_service
HiddenServicePort $LISTEN_PORT 127.0.0.1:$LISTEN_PORT
Log notice file $TOR_DIR/tor.log
EOF
```

`HiddenServicePort`가 외부 Tor 포트를 로컬 포트로 매핑한다.
socat이 로컬 포트를 리슨하면 Tor가 앞에서 익명 라우팅을
처리한다.

### 회로 경로 가시화

v1.1.2에서 추가된 기능이다.

```text
Guard Node → Middle Relay → Rendezvous Point
(입구)        (중계)          (만남 지점)
```

Tor 제어 포트로 실시간으로 회로 경로를 조회한다. 단순한
디버깅 도구가 아니다.

어떤 국가의 노드를 거치는지 사용자가 직접 확인할 수 있다.
이 가시성이 다음 기능의 전제가 된다.

### Five/Nine/Fourteen Eyes 국가 제외

v1.1.3에서 추가된 기능이다.

```text
Five Eyes:      미국, 영국, 캐나다, 호주, 뉴질랜드
Nine Eyes:      +덴마크, 프랑스, 네덜란드, 노르웨이
Fourteen Eyes:  +독일, 벨기에, 이탈리아, 스웨덴, 스페인
```

```bash
# torrc에 추가
echo "ExcludeNodes $EXCLUDE_NODES" >> "$TOR_CONF"
echo "StrictNodes 1" >> "$TOR_CONF"
```

`StrictNodes 1`이 핵심이다. 이게 없으면 Tor가 제외 조건을
"권고"로만 처리한다. `StrictNodes 1`은 제외 국가 노드를
절대 사용하지 않도록 강제한다.

단, 노드의 보고 위치가 실제 위치와 다를 수 있다.
완벽한 보장이 아니라 알려진 위험을 줄이는 조치다.

### Snowflake 브릿지

```bash
ClientTransportPlugin snowflake exec $sf_bin
Bridge snowflake 192.0.2.3:80 \
    2B280B23E1107BB62ABFC40DDCC8824814F80A72 ...
    url=https://snowflake-broker.torproject.net/ \
    ice=stun:stun.l.google.com:19302,...
```

WebRTC 기반 Tor 브릿지다. Tor 트래픽을 WebRTC 데이터
채널로 위장해 심층 패킷 검사(DPI)를 우회한다.
일반 Tor가 차단된 환경에서 TerminalPhone을 사용 가능하게
한다.

## 오디오 파이프라인

### 녹음 → 전송 경로

```text
마이크
  │ Linux: arecord -f S16_LE -r 8000 -c 1 -t raw
  │ Termux: termux-microphone-record → ffmpeg 변환
  ▼
raw PCM (16-bit, 8kHz, 모노)
  │ sox DSP 필터 (음성 변조가 설정된 경우)
  ▼
변조된 raw PCM
  │ opusenc --raw --raw-rate 8000 --bitrate 16 --speech --framesize 60
  ▼
.opus 파일
  │ openssl enc -aes-256-cbc -pbkdf2 -iter 10000 -pass fd:3
  ▼
암호화된 바이너리
  │ base64 -w 0
  ▼
"AUDIO:<base64>" 텍스트
  │ >&4 (fd 4: socat 연결)
  ▼
수신측 Tor 히든 서비스
```

8kHz 샘플링 레이트와 16kbps Opus 설정을 눈여겨봐야 한다.
전화 음질(8kHz)로 낮추고 비트레이트도 최소화했다.
Tor 회로의 제한된 대역폭과 레이턴시 환경에서 최적화된
선택이다.

### 수신 → 재생 경로

```text
socat (히든 서비스 포트 리슨)
  │ "AUDIO:<base64>" 텍스트 수신
  ▼
base64 디코딩
  │ openssl dec
  ▼
.opus 파일
  │ opusdec --quiet --rate 48000
  ▼
raw PCM (48kHz, 디코딩 후 업샘플링)
  │ Linux: aplay -f S16_LE -r 48000
  │ Termux: sox play (MediaPlayer 아님)
  ▼
스피커
```

인코딩은 8kHz지만 재생은 48kHz다. opusdec이 자동으로
업샘플링한다. Opus의 내부 처리는 48kHz 기반이므로 자연스럽다.

Termux에서 MediaPlayer 대신 sox play를 쓰는 이유가 있다.
MediaPlayer는 재생 파일을 MediaStore 데이터베이스에 등록한다.
다른 앱이 이 데이터베이스를 조회하면 통화 오디오 파일이
노출된다. sox는 파일 시스템에서 직접 읽어 이 노출 경로가
없다. v1.0.9에서 이를 수정했다.

### 음성 변조: sox DSP 파이프라인

```bash
deep)
    sox $fmt "$infile" $fmt "$outfile" pitch -400
    ;;
robot)
    sox $fmt "$infile" $fmt "$outfile" overdrive 10 flanger
    ;;
custom)
    local effects=""
    [ "$VOICE_PITCH" -ne 0 ] && effects="$effects pitch $VOICE_PITCH"
    [ "$VOICE_OVERDRIVE" -gt 0 ] && \
        effects="$effects overdrive $VOICE_OVERDRIVE"
    [ "$VOICE_FLANGER" -eq 1 ] && effects="$effects flanger"
    [ "$VOICE_ECHO_DELAY" -gt 0 ] && \
        effects="$effects echo 0.8 0.88 $VOICE_ECHO_DELAY 0.${VOICE_ECHO_DECAY}"
    sox $fmt "$infile" $fmt "$outfile" $effects
    ;;
```

sox의 effect chain을 연결해 DSP를 구현한다. 별도 음성
처리 라이브러리 없이 시스템에 이미 있는 sox만 사용한다.
모든 변조는 Opus 인코딩 전에 raw PCM 단계에서 적용된다.
수신측에 도달하는 오디오가 이미 변조된 상태다.

## PTT 메커니즘

### 키 입력 감지: stty raw 모드

```bash
ORIGINAL_STTY=$(stty -g)
stty raw -echo -icanon min 0 time 1
# ...
key=$(dd bs=1 count=1 2>/dev/null) || true
```

터미널을 raw 모드로 전환해 한 바이트씩 즉시 읽는다.
일반 모드에서는 Enter를 눌러야 입력이 전달된다.
raw 모드에서는 공백 키 하나가 즉시 캡처된다.

`time 1`은 1/10초 타임아웃이다. 키 입력이 없으면 빈
문자열이 반환된다. 이 타임아웃이 Linux hold-to-talk
메커니즘의 핵심이다.

### Linux vs Termux PTT 전략 차이

Linux는 hold-to-talk:

```bash
# 키 누름: 녹음 시작 + stty time을 5로 늘림 (5/10초 타임아웃)
stty time 5
start_recording

# 키 떼면: dd 타임아웃 → 빈 key → 녹음 중지 + 전송
if [ -z "$key" ] && [ $ptt_active -eq 1 ]; then
    stty time 1  # 복원
    stop_and_send
fi
```

Termux는 toggle 모드:

```bash
# 첫 번째 탭: 녹음 시작
if [ $ptt_active -eq 0 ]; then
    ptt_active=1
    start_recording
# 두 번째 탭: 중지 + 전송
else
    ptt_active=0
    stop_and_send
fi
```

Termux에서는 터치스크린 키보드가 hold 이벤트를 안정적으로
전달하지 못한다. toggle 모드가 더 실용적이다. 물리 키보드가
있는 Linux에서는 hold-to-talk이 자연스러운 PTT 경험을 준다.

`stty time 5`로 타임아웃을 늘리는 것이 Linux 디바운스
구현이기도 하다. 녹음 중에는 키 떼는 시점을 500ms 단위로
감지한다.

### Termux 볼륨 버튼 PTT

볼륨 다운 더블탭을 파일 시스템으로 감지한다.

```bash
if [ -f "$vol_trigger_file" ]; then
    rm -f "$vol_trigger_file"
    key="$PTT_KEY"  # PTT 키 입력처럼 처리
fi
```

볼륨 버튼 이벤트를 백그라운드 프로세스가 감지하면 트리거
파일을 생성한다. 메인 루프가 이 파일의 존재를 체크하는
방식이다. 복잡한 IPC 대신 파일 시스템을 신호 채널로
사용하는 유닉스 전통 기법이다.

## 보안 모델의 한계

README가 직접 명시한 한계들이다. 정직한 문서다.

### 전방향 비밀성(Forward Secrecy) 없음

공유 비밀이 노출되면 과거 모든 녹음된 통화를 복호화할 수
있다. Signal Protocol의 Double Ratchet이 제공하는 세션 키
교환이 없다.

설계 선택이지 버그가 아니다. DH 키 교환을 Tor 위에서
구현하면 핸드셰이크 레이턴시가 추가된다. 단순성과 레이턴시를
위해 포기한 기능이다.

### 공유 비밀 교환 문제

처음 한 번은 어떻게든 안전하게 비밀을 교환해야 한다.
이 도구는 그 첫 교환을 해결하지 않는다. 대역 외(out-of-band)
교환이 필요하다. 직접 만나서, Signal로, 또는 다른 암호화
채널로.

### HMAC이 양측 모두 활성화되어야 의미 있다

HMAC은 선택 기능이며 기본값이 비활성화다. 한쪽만 활성화하면
동작하지 않는다. 양측의 설정이 일치해야 한다.

기능 자체는 훌륭하지만, 기본값 비활성화 + 수동 활성화 요구
조합은 많은 사용자가 이 보호를 받지 못함을 의미한다.

## 통화 세션 아키텍처

### Named Pipe 기반 IPC

통화 세션에서 수신 루프와 PTT 루프가 병렬로 실행된다.
두 루프는 파일 시스템으로 통신한다.

```bash
# 세션 시작 시 named pipe 생성
mkfifo "$RECV_PIPE" "$SEND_PIPE"

# socat이 Tor와 named pipe를 연결
socat "SOCKS4A:127.0.0.1:${onion}:${PORT},socksport=9050" \
  "SYSTEM:cat $SEND_PIPE & cat > $RECV_PIPE"

# 파일 디스크립터로 연결
exec 3< "$RECV_PIPE"   # fd 3 = 원격에서 읽기
exec 4> "$SEND_PIPE"   # fd 4 = 원격으로 쓰기
```

`socat`의 `SYSTEM:` 액션이 핵심이다.
`cat $SEND_PIPE &`(송신)과 `cat > $RECV_PIPE`(수신)를
동시에 실행해 하나의 socat 프로세스로 양방향 스트리밍을
구성한다.

### 수신 루프와 PTT 루프의 병렬 분리

```
in_call_session()
├── 수신 루프 (백그라운드 subshell &)
│   └── fd 3에서 readline → proto_verify → switch
│       ├── AUDIO:<b64> → 복호화 → play_chunk
│       ├── HANGUP → CONNECTED_FLAG 삭제
│       └── CIPHER:<algo> → cipher 불일치 경고
└── PTT 메인 루프 (포그라운드)
    └── stty raw → dd bs=1 → start/stop_and_send
```

연결 상태는 `CONNECTED_FLAG` 파일의 존재 여부로 제어한다.
한쪽이 파일을 삭제하면 양쪽 루프가 모두 종료된다.

### 런타임 설정 동기화

통화 중 암호화 알고리즘 변경은 두 가지 문제를 해결해야 한다.
서로 다른 subshell과 백그라운드 프로세스에 변경을 전파하는
문제, 그리고 원격 피어에 알리는 문제다.

```bash
# 설정 변경 시
echo "$CIPHER" > "$CIPHER_RUNTIME_FILE"
proto_send "CIPHER:${CIPHER}"    # 원격에 알림

# 암호화 함수는 항상 파일에서 읽음
local c="$CIPHER"
[ -f "$CIPHER_RUNTIME_FILE" ] && c=$(cat "$CIPHER_RUNTIME_FILE")
```

환경 변수로는 subshell 간 전파가 불가능하다.
파일 시스템이 공유 메모리 역할을 한다.

### ANSI 커서 기반 깜빡임 없는 UI

```bash
# 특정 행만 갱신
printf '\033[s'                             # 커서 위치 저장
printf '\033[%d;1H\033[K' "$RECV_INFO_ROW" # 해당 행으로 이동 + 지우기
printf '  Last recv: %s' "$info"
printf '\033[u'                             # 커서 위치 복원
```

수신 루프 subshell과 메인 PTT 루프가 동시에 화면을 갱신한다.
전체 화면을 다시 그리지 않고 각자 담당 행만 덮어쓰는 방식으로
경쟁 조건(race condition)에서도 UI가 깔끔하게 유지된다.

### Legacy 비밀 감지 및 마이그레이션

```bash
magic=$(head -c 8 "$SECRET_FILE" | cat -v)
if [[ "$magic" == "Salted__"* ]]; then
    # OpenSSL 암호화 형식
else
    # 평문 저장 → 암호화로 마이그레이션 제안
fi
```

OpenSSL 암호화 파일은 항상 `Salted__` 8바이트 헤더로 시작한다.
이를 감지해 구버전 평문 저장 방식을 자동으로 감지하고
마이그레이션한다.

## 기술적 흥미 포인트

### 파일 디스크립터를 프로세스 간 채널로

```bash
# 연결 수립 후 fd 4를 socat 연결에 연결
exec 4<> /dev/tcp/...

# 모든 프로토콜 메시지를 fd 4로
echo "$msg" >&4

# 제어 메시지와 데이터 메시지가 동일 스트림
proto_send "PTT_START"
proto_send "AUDIO:${b64}"
proto_send "HANGUP"
```

별도 제어 채널 없이 하나의 TCP 연결에서 모든 통신이
이루어진다. 텍스트 프로토콜로 제어 메시지와 오디오 데이터를
구분한다.

### 오디오의 base64 직렬화 트레이드오프

이진 오디오를 base64로 인코딩하면 크기가 약 33% 증가한다.
Tor 대역폭에 부담이 된다.

그러나 텍스트 라인 기반 프로토콜의 단순성이 이 비용을
정당화한다. 이진 프레이밍 프로토콜을 Bash에서 안전하게
구현하는 것보다 텍스트 라인이 훨씬 간단하다.

### 진화 속도가 말하는 것

v1.0.0(2026-02-16)에서 v1.1.3(2026-02-24)까지 8일. 13개 버전.

주목할 만한 패턴:

- 기능 추가 후 즉시 버그 수정 (v1.0.4 → v1.0.5)
- 실험 후 폐기 (전이중 → 반이중, v1.0.3)
- 보안 강화가 후기에 집중

```text
v1.0.x: 기능 완성 (Snowflake, 음성 변조, 자동 수신)
v1.1.x: 보안 강화 (PBKDF2, fd 전달, HMAC, 국가 제외)
```

초기에 기능을 만들고 나중에 보안을 강화하는 패턴은
현실적이지만 위험하다. 초기 버전을 실제 사용한 사람이 있다면
상대적으로 약한 보안으로 통신한 셈이다. 보안 도구는 기능
우선/보안 후순위 개발 순서가 특히 위험하다.

## 사용 시나리오와 실제 위협 모델

이 도구가 실제로 보호하는 것:

1. **통신 내용**: AES-256-CBC로 암호화
2. **통신 당사자의 IP 주소**: Tor 히든 서비스로 익명화
3. **신원**: 계정, 전화번호 없음. onion 주소만
4. **메타데이터(부분적)**: Tor가 통신 사실 자체를 숨기지만,
   타이밍 분석은 여전히 가능

이 도구가 보호하지 않는 것:

1. **목소리 자체**: 음성 변조 없이는 신원 노출 가능
2. **HMAC 비활성화 시 재생 공격**: 기본값이 비활성화
3. **공유 비밀 교환 과정**: 첫 교환은 사용자 책임
4. **컴프로미즈된 디바이스**: 엔드포인트 보안 전제
5. **과거 통화**: 전방향 비밀성 없음

### 실제 적합한 사용 사례

- 저널리스트-제보자 통신
- 검열 국가에서의 안전한 통신
- 계정 생성 없는 익명 음성 채널

### 부적합한 사용 사례

- 일상적인 편의 통신(Signal로 충분)
- 전방향 비밀성이 필요한 장기 통신
- 음성 신원 노출이 위험한 상황(음성 변조 필수)
