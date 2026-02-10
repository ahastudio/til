# 오픈소스 설치형 VPN 솔루션

셀프 호스팅이 가능한 무료 오픈소스 VPN 솔루션 정리.

## WireGuard

<https://www.wireguard.com/>

약 4,000줄의 간결한 코드로 구현된 현대적인 VPN 프로토콜.
리눅스 커널에 내장되어 성능이 뛰어나고 CPU 부하가 적습니다.
Raspberry Pi 같은 저사양 기기에서도 잘 동작합니다.

- 가장 빠른 VPN 프로토콜
- 설정이 비교적 단순 (텍스트 기반 설정 파일)
- 기기 수가 늘어나면 설정 관리가 복잡해짐

### 설치

```bash
# Ubuntu/Debian
sudo apt install wireguard

# macOS
brew install wireguard-tools
```

## WG-Easy

<https://github.com/wg-easy/wg-easy>

WireGuard 서버를 웹 UI로 쉽게 관리할 수 있는 도구.
Docker로 간단히 배포할 수 있습니다.

```bash
docker run -d \
  --name=wg-easy \
  -e LANG=en \
  -e WG_HOST=your-server-ip \
  -e PASSWORD_HASH='your-password-hash' \
  -v ~/.wg-easy:/etc/wireguard \
  -p 51820:51820/udp \
  -p 51821:51821/tcp \
  --cap-add=NET_ADMIN \
  --cap-add=SYS_MODULE \
  --sysctl="net.ipv4.conf.all.src_valid_mark=1" \
  --sysctl="net.ipv4.ip_forward=1" \
  --restart unless-stopped \
  ghcr.io/wg-easy/wg-easy
```

웹 UI에서 클라이언트 추가/삭제, QR 코드 생성,
트래픽 모니터링이 가능합니다.

## Headscale

<https://github.com/juanfont/headscale>

Tailscale 컨트롤 서버의 오픈소스 구현체.
Tailscale의 편리함을 자체 서버에서 누릴 수 있습니다.
공식 Tailscale 클라이언트를 그대로 사용할 수 있는 게 장점.

- WireGuard 기반 mesh 네트워크
- NAT 환경에서도 자동 P2P 연결
- ACL 기반 접근 제어
- Tailscale 클라이언트 호환

## NetBird

<https://netbird.io/>

<https://github.com/netbirdio/netbird>

제로 트러스트 네트워킹 솔루션 (BSD-3 라이선스).
기기 간 직접 P2P 연결로 성능이 좋고,
완전한 셀프 호스팅이 가능합니다.

- 피어 투 피어 방식으로 중앙 서버 병목 없음
- SSO 연동 지원
- 웹 기반 관리 UI 제공
- Docker로 셀프 호스팅 가능

## OpenVPN

<https://openvpn.net/>

가장 오랜 역사를 가진 오픈소스 VPN.
높은 커스터마이징 자유도와 강력한 암호화(AES-256)를
제공하지만 설정이 복잡하고 WireGuard보다 느립니다.

- 가장 높은 커스터마이징 자유도
- 검증된 보안 (다수의 독립 감사 통과)
- 크로스 플랫폼 지원
- 설정 복잡도가 높음

## AmneziaVPN

<https://amnezia.org/>

<https://github.com/amnezia-vpn/amnezia-client>

검열 우회에 특화된 VPN 클라이언트.
앱에서 VPS의 SSH 정보만 입력하면
서버 설치까지 자동으로 처리합니다.

- AmneziaWG: DPI를 우회하는 WireGuard 포크
- OpenVPN + Cloak, Shadowsocks, XRay 지원
- 서버 설정 자동화 (SSH 접속 → 자동 설치)
- 검열이 심한 환경에서 유용

## Algo VPN

<https://github.com/trailofbits/algo>

클라우드에 WireGuard/IPsec VPN을 자동 배포하는 도구.
DigitalOcean, AWS, GCP 등에서 사용할 수 있습니다.
"배포하고 잊어버리기" 방식으로 관리 부담이 적습니다.

## 비교

| 솔루션     | 프로토콜       | 난이도 | 특징            |
|------------|----------------|--------|-----------------|
| WireGuard  | WireGuard      | 중     | 최고 성능       |
| WG-Easy    | WireGuard      | 하     | 웹 UI 관리      |
| Headscale  | WireGuard      | 중     | Tailscale 호환  |
| NetBird    | WireGuard      | 중     | 제로 트러스트   |
| OpenVPN    | OpenVPN        | 상     | 최고 커스터마이징 |
| AmneziaVPN | WireGuard 외   | 하     | 검열 우회       |
| Algo VPN   | WireGuard      | 하     | 클라우드 자동화 |

## 추천

- **간단하게 시작**: WG-Easy (웹 UI로 WireGuard 관리)
- **Tailscale 대체**: Headscale (같은 클라이언트 사용)
- **검열 우회**: AmneziaVPN (DPI 우회 기능)
- **기업 환경**: NetBird (제로 트러스트 + SSO)
- **클라우드 VPN**: Algo VPN (자동 배포)

## 참고

- [WireGuard](https://www.wireguard.com/)
- [WG-Easy](https://github.com/wg-easy/wg-easy)
- [Headscale](https://github.com/juanfont/headscale)
- [NetBird](https://github.com/netbirdio/netbird)
- [AmneziaVPN](https://github.com/amnezia-vpn/amnezia-client)
- [Algo VPN](https://github.com/trailofbits/algo)
