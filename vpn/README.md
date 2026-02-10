# VPN

## 오픈소스 설치형 VPN 솔루션

- [WireGuard](./wireguard.md) -
  리눅스 커널 내장. 최고 성능. ~4,000줄 코드라 감사 용이.
  기기가 많아지면 설정 관리가 복잡해지는 게 단점.
- [WG-Easy](https://github.com/wg-easy/wg-easy) -
  WireGuard에 웹 UI를 씌운 것.
  Docker 한 줄이면 시작. 가장 쉽게 WireGuard를 쓰는 법.
- [Headscale](https://github.com/juanfont/headscale) -
  Tailscale 컨트롤 서버의 오픈소스 구현체.
  공식 Tailscale 클라이언트를 그대로 사용 가능.
  mesh 네트워크, NAT 자동 통과, ACL 지원.
- [NetBird](https://github.com/netbirdio/netbird) -
  제로 트러스트 + P2P. SSO 연동, 웹 관리 UI 제공.
  완전한 셀프 호스팅 가능. 기업 환경에 적합.
- [OpenVPN](https://openvpn.net/) -
  가장 오래되고 검증된 VPN. 커스터마이징 자유도 최고.
  다만 설정이 복잡하고 WireGuard보다 느림.
- [AmneziaVPN](https://github.com/amnezia-vpn/amnezia-client) -
  검열/DPI 우회 특화. VPS SSH 정보만 넣으면 서버 자동 설치.
  WireGuard 포크(AmneziaWG)로 트래픽 탐지 회피.
- [Algo VPN](https://github.com/trailofbits/algo) -
  클라우드(AWS, GCP, DO 등)에 WireGuard를 자동 배포.
  "배포하고 잊기" 방식. 관리 부담 최소.
- [Tailscale](./tailscale.md) -
  WireGuard 기반 SaaS. 설정 거의 불필요. 개인 무료.
  컨트롤 서버가 비공개라 셀프 호스팅 불가(→ Headscale).
- [Pritunl](./pritunl.md) -
  OpenVPN/IPsec/WireGuard 통합 서버.
  웹 UI 제공. 여러 프로토콜을 한곳에서 관리.

## Headscale vs Pritunl

| 항목           | Headscale              | Pritunl                |
|----------------|------------------------|------------------------|
| 방식           | mesh (P2P 직접 연결)   | 허브-스포크 (서버 경유) |
| 프로토콜       | WireGuard              | OpenVPN/IPsec/WireGuard |
| 트래픽 경로    | 기기 간 직접           | 중앙 서버 경유         |
| NAT 통과       | 자동                   | 수동 (포트포워딩)      |
| 웹 UI          | 없음 (별도 설치 필요)  | 기본 제공              |
| 클라이언트     | Tailscale 공식 앱      | 전용 클라이언트        |
| 외부 의존성    | 없음                   | MongoDB                |
| 적합한 경우    | P2P 성능, Tailscale 전환 | 웹 관리, 멀티 프로토콜 |
