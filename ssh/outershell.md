# Outer Shell: 서버와 엣지 장치에 원격용 그래픽 셸을 씌우는 서비스

<https://outershell.org/>

<https://github.com/outergroup/outershell>

GN 토론: <https://news.hada.io/topic?id=36076>

## 소개

Outer Shell은 서버와 엣지 장치가 원격 우선 운영체제처럼 바깥쪽(outer) 그래픽
셸을 가져야 한다는 생각을 구현한 프로젝트다.
웹과 네이티브 앱을 섞은 형태로 브라우저 안에서 셸을 만든다.
그러려면 브라우저 자체가 SSH, Unix 도메인 소켓, sudo, 네이티브 앱 모델을
지원해야 하므로
짝이 되는 브라우저 Outer Loop이 따로 있다.
Outer Shell은 Linux나 macOS 어느 기기에서든 도는 서비스이고,
앱을 등록하고 조회하는 API와 셸 UI를 호스팅하는 로컬 HTTP 서버를 제공한다.
공식 사이트는 이 개념을 설명한 블로그 글과 화면 녹화로 「A native graphical
shell for SSH」를 안내한다.
이 저장소의 [SSH를 위한 네이티브 그래픽 셸](native-graphical-shell-for-ssh.md)
문서가 그 글을 다룬다.

저장소는 MIT 라이선스이고 Swift로 작성되었다.
2026년 6월 27일에 만들어졌고 10월 27일에 확인한 시점에 별 66개, 포크 2개였으며
마지막 푸시는 10월 26일이었다.
기본 앱으로 Files, Plaintext, Top, Profile, Firehose가 있고 UI에서 설치한다.
이 앱들은 소켓이나 포트에서 HTTP 서버를 여는 서비스일 뿐이며, 같은 방식으로 직접
앱을 만들어 공유할 수 있다.
사용하려면 macOS용 Outer Loop을 내려받아 기기에 연결한다.

## 동작 방식

Outer Shell의 핵심은 앱 레지스트리다.
앱은 백엔드가 소유하고, 백엔드 하나가 여러 앱을 가질 수 있으며, 흔한 경우
프런트엔드와 백엔드는 일대일이고 표시 이름도 같다.
백엔드는 대개 macOS의 launchd plist나 Linux의 systemd 유닛과 연결되고, 필수는
아니다.
앱은 TCP 엔드포인트, Unix 소켓 엔드포인트, 또는 아직 엔드포인트가 없는 상태 중
하나를 가진다.
사용자가 앱을 열면 Outer Shell이 서비스를 시작하고 등록된 엔드포인트에 연결한다.

파일 연결도 셸의 중심이다.
미리보기는 현재 몇몇 형식에 고정되어 있고, 열기와 편집은 완전히 확장할 수 있다.
앱은 설치할 때 API 호출로 자기가 소유한 파일 형식과 열 수 있는 파일 형식을
등록하고, 앱이 제거되면 Outer Shell이 등록을 지운다.
내장 형식은 `public.text`, `public.pdf` 같은 이름이고, 앱은
`com.yourwebsite.yourtype` 같은 형식에 확장자와 MIME 정보를 붙여 등록한다.
형식을 등록할 때 어느 형식을 따르는지(conformance)를 알려 주면 기존 뷰어를
재사용할 수 있고,
예를 들어 자기 텍스트 형식이 텍스트 편집기에서 열리게 할 수 있다.
내장 `public.*` 형식에는 `public.data`, `public.text`, `public.markdown`,
`public.json`, `public.xml`, `public.shell-script`, `public.python-script`,
`public.javascript`, `public.html`, `public.css` 등이 있고 소유 백엔드가 없다.

핵심 API는 소켓 메시지로 돌고, 편의용 명령줄 래퍼 `outerctl`이 있다.
소켓은 처음에 사용자 소유 디렉터리에 놓이고, 루트로 무엇을 설치하면 루트 소유
디렉터리에 두 번째 소켓과 두 번째 `outerctl`이 생긴다.
macOS의 사용자 소켓은 `DARWIN_USER_TEMP_DIR/outershelld-api`, Linux는
`$XDG_RUNTIME_DIR/outershelld-api`에 있고,
`outerctl` 실행 파일은 macOS에서
`$HOME/Library/Application Support/outershell/bin/outerctl`, Linux에서
`$XDG_STATE_HOME/outershell/bin/outerctl`에 있다.
메시지 프레임은 4바이트 리틀 엔디언 길이 접두사로 시작하고, 첫 2바이트가 메시지
종류다.
문자열은 같은 메시지 안의 오프셋과 길이로 가리키며, 변경 명령은 종료 상태와
stdout, stderr를 돌려주고 목록 요청은 전용 이진 응답을 돌려준다.
`outerctl`은 목록 응답을 TSV로 바꿔 출력한다.
단순한 getter와 setter가 대부분이고, 논리가 복잡한 것은 열기 도구(opener) 조회
하나다.
조회는 파일의 내용 형식을 추정하거나 주어진 형식을 쓰고, 따르는 관계를 펼쳐서
맞는 열기 도구를 순서대로 돌려준다.

## 설치하기

보통은 Outer Loop을 통해 설치하고, 직접 설치는 릴리스를 시험하거나 부분 설치를
복구하거나 UI 없이 설치할 때 쓴다.
공식 문서는 이 설치 페이지가 대부분 AI로 쓰였고 나머지 사이트는 사람이 썼다고
밝힌다.

```bash
# 설치 또는 갱신
curl -fsSL https://outershell.org/outer-shell/latest/install.sh -o /tmp/outershell-install.sh
sh /tmp/outershell-install.sh install

# 기존 설치 갱신
sh /tmp/outershell-install.sh update

# 제거
sh /tmp/outershell-install.sh uninstall

# 모든 앱을 제거한 뒤 사용자 상태까지 지우기
OUTERSHELL_UNINSTALL_REMOVE_USER_STATE=1 sh /tmp/outershell-install.sh uninstall
```

Linux에서 루트 설치는 같은 명령을 루트로 실행한다.
설치 프로그램이나 UI가 동작하지 않을 때를 위한 강제 제거 절차도 있어서,
서비스 파일과 설치된 바이너리를 지우되 사용자 지정 앱 등록은 보존하려 하지
않는다.
Linux 사용자 범위는 `systemctl --user`로 소켓과 서비스를 끄고
`~/.config/systemd/user`의 유닛 파일과 `$XDG_STATE_HOME/outershell` 아래를
지운다.

## 앱 만들기

Outer Shell은 Linux의 systemd와 macOS의 launchd와 맞물린다.
앱을 추가하는 일은 세 단계다.
로컬 포트나 소켓에서 웹 서버를 시작하는 명령을 만들고,
그 명령을 시스템의 서비스 관리자에 등록하고,
`outerctl`이나 소켓 API로 Outer Shell에 알린다.
일반 HTML과 JavaScript를 쓸 수도 있고 outerframe 앱을 만들 수도 있다고 안내한다.

가장 단순한 예는 `python -m http.server`로 홈 디렉터리를 `localhost:8000`에
서빙하는 것이다.
Linux에서는 `~/.config/systemd/user/com.example.HttpServer.service`를 만든다.

```ini
[Unit]
Description=Example Python HTTP server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m http.server 8000 --directory %h
Restart=on-failure

[Install]
WantedBy=default.target
```

유닛을 켜고 Outer Shell에 백엔드와 앱을 등록한다.

```bash
systemctl --user daemon-reload
systemctl --user enable com.example.HttpServer.service

outerctl backend upsert \
  --backend com.example.HttpServer \
  --name "HTTP Server" \
  --systemd-unit com.example.HttpServer.service
outerctl app upsert \
  --backend com.example.HttpServer \
  --name "HTTP Server" \
  --scheme http \
  --host 127.0.0.1 \
  --port 8000 \
  --path /
```

`--frontend-id`를 생략하면 `outershelld`가 프런트엔드 ID를 `<백엔드>:main`으로
정한다.
사용자가 앱을 열면 Outer Shell이 서비스를 시작한 뒤 `127.0.0.1:8000`에 연결한다.
macOS에서는 같은 일을 `~/Library/LaunchAgents`의 plist와
`launchctl bootstrap "gui/$(id -u)"`로 하고,
`backend upsert`에 `--systemd-unit` 대신 `--launchd-plist`를 준다.

더 완성된 예는 텍스트 편집기 Plaintext다.
TCP 포트 대신 Unix 소켓을 쓰고, 서비스 관리자가 소켓을 소유해 첫 입력에서
백엔드를 시작하며, `public.text`의 열기 도구로 등록한다.
Linux에서는 `.service` 파일과 함께 `.socket` 유닛을 만들고(`ListenStream`,
`SocketMode=0600`) 소켓을 켠 뒤 등록한다.

```bash
SOCKET_PATH="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/org.outershell.Plaintext"
outerctl backend upsert \
  --backend org.outershell.Plaintext \
  --name Plaintext \
  --systemd-unit org.outershell.Plaintext.service
outerctl app upsert \
  --backend org.outershell.Plaintext \
  --name Plaintext \
  --socket-path "$SOCKET_PATH" \
  --path /
outerctl opener upsert \
  --backend org.outershell.Plaintext \
  --content-type public.text \
  --url-template "?file={file}" \
  --rank 0 \
  --capabilities view,edit
```

`public.text`는 내장 형식이라 `outerctl content-type add`로 만들 필요가 없다.
URL 템플릿의 `{file}`은 열려는 파일 경로를 퍼센트 인코딩해 채우고,
`--capabilities`를 생략하면 `view`와 `edit`를 모두 보낸다.
macOS에서는 launchd가 plist의 `Sockets` 사전으로 소켓을 소유하고 백엔드가
`launch_activate_socket`으로 리스너를 받는다.

## API 한눈에 보기

| 대상           | 명령                                          | 하는 일                                          |
| -------------- | --------------------------------------------- | ------------------------------------------------ |
| 백엔드         | `outerctl backend upsert`, `remove`, `list`   | 앱, 로그, 열기 도구, 형식이 가리키는 루트 레코드 |
| 앱             | `outerctl app upsert`, `remove`, `list`       | 백엔드의 사용자용 진입점과 엔드포인트            |
| 로그           | `outerctl log add`, `remove`, `list`          | 백엔드의 로그 경로 등록                          |
| 내용 형식      | `outerctl content-type add`, `remove`, `list` | 앱이 소유하는 형식과 확장자, MIME, 따르는 형식   |
| 열기 도구      | `outerctl opener upsert`, `remove`            | 프런트엔드가 열 수 있는 형식과 순위, 보기/편집   |
| 열기 도구 조회 | 소켓 메시지만 있음                            | 파일에 맞는 열기 도구를 순서대로 반환            |

`backend upsert`는 `--outershell-owns true`로 플랫폼의 launchd나 systemd 항목을
Outer Shell이 소유하게 할 수 있다.
`app upsert`는 `--scheme http|https`, `--host`, `--path`, `--icon-path`,
`--list`(제안되는 목록), `--port` 또는 `--socket-path`를 받는다.
컨테이너 안에 앱을 설치하는 방법은 문서의 별도 항목인 컨테이너 앱에 있다.

## 분석

### 셸의 단위를 데스크톱 창이 아니라 서비스로 잡았다

앱이 소켓이나 포트에서 HTTP 서버를 여는 서비스이고 셸은 그 서비스를 시작하고
연결할 뿐이라는 설계는,
앱 개발의 문턱을 웹 서버를 만들 수 있느냐로 낮춘다.
시작과 종료를 systemd와 launchd에 맡기므로 Outer Shell이 프로세스 관리자를 새로
만들지 않는다.
이는 기존 운영체제의 기능을 그대로 쓰면서 그 위에 그래픽 층만 얹는 선택이다.
이는 이 문서의 해석이다.

### 파일 연결을 레지스트리로 만든 것이 앱 사이의 결합을 푼다

앱이 설치할 때 자기 형식과 열 수 있는 형식을 등록하고, 형식이 서로 따르는 관계를
선언하면 뷰어가 재사용된다.
Files 앱이 파일 형식을 몰라도 등록된 열기 도구에게 넘기면 되므로 앱끼리 서로를
알 필요가 없다.
이 구조는 데스크톱 운영체제의 파일 형식 레지스트리와 같은 모양이고, 원격
장치에서 그것을 다시 만든 셈이다.

## 비평

### 브라우저를 고쳐야 한다는 전제가 도입 장벽이다

공식 소개는 이 접근이 브라우저 자체의 수정, 곧 SSH, Unix 소켓, sudo, 네이티브 앱
모델을 지원하는 브라우저를 요구한다고 밝힌다.
그래서 사용하려면 Outer Loop이라는 별도 브라우저를 내려받아야 하고,
공식 안내에서 확인되는 다운로드는 macOS용이다.
Linux나 Windows 사용자는 Outer Shell 서비스를 서버에 둘 수는 있어도 접속하는 쪽
클라이언트가 이 문서가 읽은 범위에서는 보이지 않는다.
따라서 이 프로젝트는 서버 쪽이 이식 가능한 것에 비해 사용하는 쪽이 한 환경에
묶여 있다.

### 보안 모델이 문서에 보이지 않는다

API 문서는 소켓 위치와 메시지 형식을 자세히 다루지만 누가 앱을 등록할 수 있는지,
앱이 서로를 어떻게 격리하는지, sudo 권한 앱이 무엇을 할 수 있는지는 이 문서가
읽은 페이지에서 확인되지 않았다.
앱이 소켓이나 포트의 HTTP 서버이므로 같은 기기의 다른 프로세스가 그 포트에
접근할 수 있는지가 문제다.
Plaintext 예가 소켓 모드를 0600으로 두는 것은 이 위험을 의식한 설정으로
보이지만, 일반 앱 작성자에게 강제되는지는 알 수 없다.
이는 이 문서의 해석이다.

### 설치 방식이 신뢰를 요구한다

설치는 `curl`로 받은 스크립트를 실행하는 방식이고, 서명이나 체크섬 검증 절차는
이 문서가 읽은 설치 페이지에 없었다.
설치 페이지는 대부분 AI로 쓰였다고 스스로 밝히는데, 강제 제거 절차처럼 파일을
지우는 명령이 많은 문서이므로 실행 전에 읽어 보는 것이 맞다.
프로젝트가 만들어진 지 넉 달이고 저장소의 별이 66개라서 외부 검토가 아직 적을
가능성이 있다.

## 인사이트

### 원격 장치의 UI를 브라우저로 푸는 방식은 앱 생태계의 시작 비용을 낮춘다

이 프로젝트에서 앱은 웹 서버 하나와 등록 명령 몇 줄이다.
`python -m http.server`가 첫 예제라는 점이 보여 주듯, 앱을 만드는 능력이 웹 개발
지식과 같아진다.
이 비용 구조는 앱 생태계가 모이는 속도를 정하므로, 기능이 많은 셸보다 앱이 쉽게
생기는 셸이 이긴다는 방향의 베팅이다.
다만 앱이 쉽게 생길수록 앞의 보안 모델이 중요해진다.
이는 이 문서의 해석이다.

### 소켓 기반 활성화는 서버에서 켜 두는 비용을 없앤다

Plaintext 예는 서비스 관리자가 소켓을 소유하고 첫 입력이 올 때 백엔드를 시작하게
한다.
쓰지 않는 앱이 메모리를 차지하지 않으므로 앱이 많아도 서버가 가볍다.
엣지 장치처럼 자원이 작은 환경에서 이 방식이 앱 수를 늘릴 수 있게 하는 조건이다.
한편 첫 입력의 시작 지연이 사용자 경험에 들어가므로, 앱마다 자원 절약과 응답
속도 중에서 고르게 된다.

### 이 글을 읽는 방법

이 문서는 공식 사이트의 소개, API, 내용 형식, 설치, 앱 만들기 페이지와 저장소
정보를 읽고 정리한 것이며, 직접 설치해 실행하지는 못했다.
Outer Loop 브라우저와 outerframe, 컨테이너 앱 문서는 열어 보지 못했다.
판단을 가를 관찰은 둘이다.
하나는 Linux 서버에 Outer Shell을 설치하고 `python -m http.server` 예제를 등록해
Outer Loop에서 열렸을 때 걸리는 시간과 필요한 단계 수다.
설치부터 첫 앱까지가 문서의 설명처럼 몇 분 안에 끝나면 낮은 시작 비용이라는
주장이 맞다.
다른 하나는 같은 기기에서 다른 사용자나 다른 프로세스가 등록된 앱의 포트에
접근할 수 있는지다.
접근이 막히지 않는다면 보안 모델이 약한 고리다.
두 관찰 모두 이 문서가 확인하지 못했다.
