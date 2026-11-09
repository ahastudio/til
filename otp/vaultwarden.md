# Vaultwarden: Rust로 다시 만든 Bitwarden 호환 서버, 개인과 소규모 조직의 셀프호스팅용

<https://github.com/dani-garcia/vaultwarden>

## 소개

Vaultwarden은 Bitwarden 서버 API를 다시 구현한 비공식 서버다.
Rust로 쓰였고 공식 Bitwarden 클라이언트(브라우저 확장, 모바일, 데스크톱)와
호환되며, 공식 서버처럼 무거운 서비스를 돌리고 싶지 않은 셀프호스팅에 알맞다고
README가 소개한다.
예전 이름은 bitwarden_rs다.
README는 개인, 가족, 소규모 조직을 대상으로 한다고 밝히고,
위키는 대규모 조직에 주로 필요한 기능(단일 로그인, 디렉터리 동기화 등)의 개발은
우선순위가 아니지만 품질 높은 기여는 환영한다고 적는다.[^wiki-home]
이 문서는 README와 위키, 소스 코드의 한 줄을 읽고 정리한 것이며 직접 설치하거나
시험하지 않았다.

2026년 11월 9일 기준 GitHub API가 보고한 저장소는 2018년 2월 17일에 만들어졌고
별 70,448개, 포크 3,439개, 열린 이슈 92개이며 AGPL-3.0 라이선스다.
최근 릴리스는 2026년 11월 1일의 1.37.5이고 마지막 푸시는 11월 4일이다.
컨테이너 이미지는 ghcr.io, docker.io, quay.io에 올라온다.

README의 면책 문구는 이 프로젝트가 Bitwarden 및 Bitwarden, Inc.와 무관하다고
밝힌다.
다만 유지 관리자 중 한 명이 Bitwarden에 고용되어 개인 시간에 기여하며 그 기여는
다른 유지 관리자가 검토한다고 한다.
버그나 제안은 사용 중인 클라이언트와 상관없이 Vaultwarden 쪽에 보고하고, Bitwarden
공식 지원 창구를 쓰지 말라고 안내한다.

## 기능

위키가 정리한 지원 기능은 Bitwarden 보관함의 주요 기능 대부분이다.[^wiki-home]

- 웹 보관함, 개인 보관함, 조직 보관함, 컬렉션, 그룹, 비밀번호 공유, 이벤트 로그
- 파일 첨부, 폴더, 즐겨찾기, 웹사이트 아이콘, 휴지통, 마스터 비밀번호 재입력
- Bitwarden 인증 앱 기능(TOTP), Send, 비상 접근, 개인 API 키
- 이메일, Duo, YubiKey, FIDO2 WebAuthn을 쓰는 2단계 로그인
- 데스크톱과 브라우저 확장의 실시간 동기화(WebSocket), 모바일 푸시 알림 동기화
- OpenID Connect를 쓰는 단일 로그인(SSO), 일부 엔터프라이즈 정책
- 계정 복구(메일 설정 필요), SimpleLogin, AnonAddy, Firefox Relay 사용자명 생성기

위키는 아직 없는 기능도 적는다.
공식 서버에 있지만 Vaultwarden에 없는 것으로 Bitwarden 공개 API와 조직 API 키는
디렉터리 커넥터용으로만 일부 추가되었고, 패스키로 로그인과 새 기기 로그인 보호는
시간이 나면 추가될 수 있는 기능이다.
사용자 지정 역할과 일부 엔터프라이즈 정책(SSO 강제, 보관함 시간 제한, 개인 보관함
내보내기 제한)은 누가 기여하지 않으면 추가되지 않을 가능성이 크다고 한다.[^wiki-home]

## TOTP를 쓰는 방법

Vaultwarden은 인증 앱처럼 6자리 TOTP 코드를 만든다.
Bitwarden 공식 서비스에서는 TOTP 키를 저장하는 것은 모든 계정이 쓸 수 있지만 코드를
생성하는 것은 Premium이나 유료 조직이 필요하다.[^bw-auth]
Vaultwarden의 소스 코드(`src/db/models/user.rs`)는 사용자 프로필 응답에서 `premium`을
항상 `true`로, `premiumFromOrganization`을 `false`로 돌려준다.
클라이언트가 이 값을 보고 코드 생성 기능을 여는 것으로 보이지만 이 문서는 클라이언트
코드를 읽지 않았으므로 그 연결은 추론이다.
사용법은 Bitwarden 문서를 따른다.
로그인 항목을 고쳐 QR 코드를 스캔하거나 인증 키 칸에 비밀 키를 붙여 넣으면 30초마다
바뀌는 6자리 코드(SHA-1)가 생긴다.[^bw-auth]

TOTP 자체는 RFC 6238이 정의한, HOTP에서 카운터를 시간으로 바꾼 알고리즘이고 기본
시간 간격은 30초다.[^rfc6238]
Google Authenticator의 QR 코드도 `otpauth://totp/` 형식이다.[^keyuri]

같은 목적의 다른 선택은 다음과 같다.
Bitwarden 공식 서버를 직접 운영해도 일부 기능은 라이선스 파일로 풀어야 한다.[^bw-license]
KeePassXC는 서버 없이 파일로 TOTP를 저장하고 생성하며 GPL-2 또는 GPL-3
라이선스다.[^keepassxc]
Aegis는 서버 없이 기기에서 AES-256-GCM으로 암호화한 볼트에 TOTP를 보관하는 Android
앱이다.[^aegis]
Ente Auth는 TOTP만 다루며 종단간 암호화로 동기화한다.[^ente-faq]

## 설치하기

README가 권하는 방법은 컨테이너 이미지다.
Docker 대신 Podman도 쓸 수 있고, 직접 빌드할 수도 있다.
웹 보관함은 Web Crypto API가 안전한 컨텍스트를 요구하므로 HTTPS가 있어야 동작한다.
Rocket 프레임워크의 TLS 기능이 있지만 리버스 프록시를 세우라고 권한다.

```shell
docker pull vaultwarden/server:latest
docker run --detach --name vaultwarden \
  --env DOMAIN="https://vw.domain.tld" \
  --volume /vw-data/:/data/ \
  --restart unless-stopped \
  --publish 127.0.0.1:8000:80 \
  vaultwarden/server:latest
```

README의 Docker Compose 예제도 같은 설정이다.

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    environment:
      DOMAIN: "https://vw.domain.tld"
    volumes:
      - ./vw-data/:/data/
    ports:
      - 127.0.0.1:8000:80
```

데이터는 `/vw-data/`에 남고 포트는 호스트의 127.0.0.1에만 열린다.
바깥에서 쓰려면 리버스 프록시가 HTTPS를 맡아야 한다.
공식 Bitwarden 클라이언트에서는 서버 주소를 `DOMAIN`의 주소로 바꿔 로그인한다.

## 운영

### 가입 제한

기본값은 서버에 접근할 수 있는 누구나 계정을 만들 수 있다는 것이다.
위키는 환경 변수 `SIGNUPS_ALLOWED`를 `false`로 두면 막을 수 있다고 안내한다.[^wiki-signups]
그래도 조직의 소유자나 관리자는 새 사용자를 초대할 수 있고, 초대까지 막는 방법은
별도 문서에 있다.[^wiki-signups]
`SIGNUPS_DOMAINS_WHITELIST`를 설정하면 특정 이메일 도메인만 가입할 수 있고, 이때
`SIGNUPS_ALLOWED` 값은 무시된다.[^wiki-signups]
관리자 페이지에서는 어떤 제한에도 상관없이 누구든 초대할 수 있다.[^wiki-signups]

### 관리자 페이지

관리자 페이지는 `ADMIN_TOKEN`을 설정해야 켜진다.
사용자와 조직을 보고 지울 수 있고, 가입이 막혀 있어도 사용자를 초대할 수 있으며,
지원 자료를 만드는 진단 페이지가 있다.[^wiki-admin]
위키는 HTTPS를 먼저 켜라고 강하게 권하고, 토큰은 긴 무작위 문자열로 정하라고 한다.
설정이 평문으로 저장되므로 `vaultwarden hash` 명령으로 argon2id 해시(PHC 문자열)를
만들어 쓰는 방법도 안내한다.[^wiki-admin]
관리자 세션은 기본 20분이며, 유효한 세션 토큰은 토큰을 바꿔도 즉시 무효가 되지
않으므로 모두 무효로 하려면 데이터 폴더의 `rsa_key.pem`을 지우고 재시작해야 한다.[^wiki-admin]

### 백업

위키는 데이터를 자동화된 방식(예: cron)으로 정기적으로 백업하고 적어도 한 부는
원격에 두라고 권한다.[^wiki-backup]
파일시스템이나 VM 스냅숏에 의존하는 것은 피하라고 한다.[^wiki-backup]
기본 SQLite 구성에서 `data` 디렉터리에는 데이터베이스(`db.sqlite3`),
첨부 파일(`attachments`), Send 파일(`sends`), 아이콘 캐시, 토큰 서명용 `rsa_key.*`
파일, 관리자 설정 `config.json`이 있다.[^wiki-backup]
데이터베이스는 SQLite의 온라인 백업 API를 쓰는 `.backup` 명령으로 받으라고 하며,
1.32.1부터는 내장 명령 `/vaultwarden backup`도 있다.[^wiki-backup]
MySQL이나 PostgreSQL 백엔드에서는 `data` 디렉터리와 함께 테이블 덤프도 필요하다.[^wiki-backup]

```shell
sqlite3 data/db.sqlite3 ".backup '/path/to/backups/db-$(date '+%Y%m%d-%H%M').sqlite3'"
```

## 비평

### 비공식 서버라서 공식 쪽의 변경에 영향을 받는다

Vaultwarden은 Bitwarden 클라이언트 API를 따라가는 서버여서 클라이언트나 API가
바뀌면 호환이 깨질 수 있다.
Bitwarden이 클라이언트 라이선스와 배포 방식을 바꾼 일과 그 호환성 우려는 기존 문서
`security/bitwarden-app-store-license.md`에 정리되어 있다.
이 문서는 현재 호환성의 상태를 직접 확인하지 못했다.

### 무료로 열리는 기능은 공식 서비스의 유료 기능을 비공식 서버가 열어 주는 구조다

코드가 `premium` 값을 항상 `true`로 돌려주는 것은 Premium 기능을 무료로 쓰게 한다.
이 구조의 법적, 정책적 위치는 이 문서가 판단하지 못했다.
셀프호스팅이 이 기능을 쓰는 것이 Bitwarden의 약관과 어떻게 만나는지는 이 문서가
읽은 자료에 없다.
사용자는 공식 서비스의 Premium을 대신하는 것이 아니라 다른 서버를 운영한다고
받아들여야 한다.

### 대규모 조직의 요구를 목표로 하지 않는다

프로젝트가 개인, 가족, 소규모 조직을 대상으로 한다고 밝히는 만큼 SSO 강제,
보관함 시간 제한, 사용자 지정 역할 같은 기능은 없거나 우선순위가 낮다.
회사 전체 도입이라면 이 목록을 먼저 대조해야 한다.

### 보안 감사 문서를 확인하지 못했다

위키는 Vaultwarden에 대한 감사가 여러 건 있었고 일부는 공개되어 있다고 소개하지만,
이 문서는 그 감사 페이지를 읽지 못했다.
감사의 범위와 시점은 확인되지 않았다.

### 직접 운영하는 비용은 사용자에게 돌아온다

README는 데이터 손실에 책임지지 않는다고 밝히고 파일과 데이터베이스를 정기적으로
백업하라고 권한다.
서버가 꺼졌을 때 클라이언트가 보관함 사본으로 얼마나 동작하는지는 이 문서가
확인하지 못했다.
TOTP를 이 보관함에만 두면 서버와 기기를 모두 잃을 때 계정 복구가 어려워진다.
비밀번호와 TOTP 비밀 키가 한 보관함에 있으면 보관함이 열릴 때 두 요소가 함께 열리므로
핵심 계정은 TOTP를 따로 두는 선택도 있다.
이 두 문장은 이 문서의 설명이다.

## 도입 전에 따져볼 것

- 리버스 프록시로 HTTPS를 설정한다. 없으면 웹 보관함이 동작하지 않는다.
- `DOMAIN`을 실제 접속 주소로 정하고 새 사용자 가입을 막을지 정한다(`SIGNUPS_ALLOWED`).
- 관리자 페이지를 켠다면 `ADMIN_TOKEN`은 해시로 저장한다.
- `data` 디렉터리를 정기적으로 백업하고 복원을 시험한다. 데이터베이스는 `.backup`이나 `/vaultwarden backup`으로 받는다.
- 중요한 서비스의 복구 코드를 보관함 밖에 따로 보관한다.
- 필요한 기능이 위키의 지원 목록에 있는지, 없는 기능 목록에 없는지 확인한다.
- Bitwarden 클라이언트를 업데이트하기 전에 호환성 소식을 확인한다.

---

[^wiki-home]: Vaultwarden Wiki, [Vaultwarden](https://github.com/dani-garcia/vaultwarden/wiki)

[^wiki-signups]: Vaultwarden Wiki, [Disable registration of new users](https://github.com/dani-garcia/vaultwarden/wiki/Disable-registration-of-new-users)

[^wiki-admin]: Vaultwarden Wiki, [Enabling admin page](https://github.com/dani-garcia/vaultwarden/wiki/Enabling-admin-page)

[^wiki-backup]: Vaultwarden Wiki, [Backing up your vault](https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault)

[^bw-auth]: Bitwarden, [Integrated Authenticator | Bitwarden](https://bitwarden.com/help/authenticator-keys/)

[^bw-license]: Bitwarden, [License Organizations or Premium | Bitwarden](https://bitwarden.com/help/licensing-on-premise/)

[^rfc6238]: IETF, [TOTP: Time-Based One-Time Password Algorithm](https://www.rfc-editor.org/rfc/rfc6238), 2011-05

[^keyuri]: Google, [Key Uri Format](https://github.com/google/google-authenticator/wiki/Key-Uri-Format)

[^keepassxc]: KeePassXC, [KeePassXC README](https://github.com/keepassxreboot/keepassxc/blob/develop/README.md)

[^aegis]: beemdevelopment, [Aegis Authenticator](https://github.com/beemdevelopment/Aegis)

[^ente-faq]: Ente, [FAQ - Auth | Ente Help](https://ente.io/help/auth/faq/)
