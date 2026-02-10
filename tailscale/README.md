# Tailscale

<https://tailscale.com/>

WireGuard 기반의 VPN 서비스.
별도의 서버 설정 없이 기기 간 사설 네트워크를 구성한다.
로그인만 하면 연결되므로 설정이 거의 필요 없다.

## 주요 특징

- 별도의 VPN 서버 불필요 (mesh 방식)
- NAT 환경에서도 P2P 연결
- SSO 기반 인증 (Google, GitHub 등)
- ACL로 접근 제어 가능

## 설치

### macOS

```bash
brew install --cask tailscale
```

### Linux

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### 그 외

<https://tailscale.com/download>

## 시작

```bash
sudo tailscale up
```

로그인 URL이 표시되면 브라우저에서 인증한다.

## 상태 확인

```bash
tailscale status
```

## 참고

- [How Tailscale works](https://tailscale.com/blog/how-tailscale-works)
- [Tailscale Docs](https://tailscale.com/kb)
