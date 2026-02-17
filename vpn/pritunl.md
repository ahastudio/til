# Pritunl - Open Source Enterprise Distributed OpenVPN, IPsec and WireGuard Server

<https://pritunl.com/>

<https://github.com/pritunl/pritunl>

OpenVPN/IPsec/WireGuard를 하나의 웹 UI에서 관리하는 오픈소스 VPN 서버.

## 주요 특징

- OpenVPN, IPsec, WireGuard 멀티 프로토콜
- 웹 관리 UI 기본 제공
- 멀티 서버 클러스터링 (고가용성, 자동 페일오버)
- Google Authenticator 2단계 인증
- SSO 연동 (Okta, OneLogin, RADIUS 등)
- REST API 제공
- 멀티 클라우드 site-to-site (AWS, GCP, Azure)
- MongoDB 기반

## 설치 (Docker)

```bash
docker run -d \
  --name pritunl \
  --privileged \
  -p 443:443 \
  -p 1194:1194/udp \
  ghcr.io/jippi/docker-pritunl
```

MongoDB가 내장되어 바로 시작할 수 있습니다. 외부 MongoDB를 쓰려면
`PRITUNL_MONGODB_URI`를 설정합니다.

## 초기 설정

웹 콘솔(`https://<서버IP>`)에 접속합니다. 기본 계정은 `pritunl`/`pritunl`입니다.

1. Organization 생성 (VPN 클라이언트 그룹)
2. User 추가 (기기당 1개)
3. Server 생성 후 Organization 연결
4. 사용자별 `.ovpn` 프로필 다운로드

## WireGuard 사용 시 주의

Docker에서 WireGuard를 쓰려면:

- 호스트에 WireGuard 커널 모듈 설치 필요
- 웹 서비스가 포트 443 + SSL 활성화 필수
- 미설정 시 클라이언트 연결 15초 후 타임아웃

## 클라이언트

<https://client.pritunl.com/>

<https://formulae.brew.sh/cask/pritunl>

## 참고

- [Pritunl Docs](https://docs.pritunl.com/)
- [Docker 이미지 (jippi)](https://github.com/jippi/docker-pritunl)
- [Pritunl VPN 설치 가이드 (Ubuntu)](https://cloudspinx.com/install-and-configure-pritunl-vpn-on-ubuntu/)
