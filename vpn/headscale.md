# Headscale

<https://github.com/juanfont/headscale>

Tailscale 컨트롤 서버의 오픈소스 구현체.
공식 Tailscale 클라이언트를 그대로 사용할 수 있습니다.

## 주요 특징

- WireGuard 기반 mesh 네트워크
- 기기 간 P2P 직접 연결 (서버 경유 없음)
- NAT/방화벽 자동 통과
- ACL 기반 접근 제어
- 기기 수 제한 없음 (Tailscale 무료는 100대)

## 설치 (Docker)

```bash
docker run -d \
  --name headscale \
  -v ./config:/etc/headscale \
  -v ./data:/var/lib/headscale \
  -p 8080:8080 \
  -p 9090:9090 \
  --restart unless-stopped \
  headscale/headscale:latest \
  serve
```

## 설정

`config.yaml`에서 주요 항목을 설정합니다.

```yaml
server_url: https://headscale.example.com
listen_addr: 0.0.0.0:8080
ip_prefixes:
  - 100.64.0.0/10
```

## 사용자 생성

```bash
headscale users create my-user
```

## 노드 등록

### 인증키 방식

```bash
# 서버에서 키 생성
headscale preauthkeys create \
  --reusable --expiration 24h --user my-user

# 클라이언트에서 연결
tailscale up \
  --login-server https://headscale.example.com \
  --authkey YOUR_AUTH_KEY
```

### 수동 방식

```bash
# 클라이언트에서 요청
tailscale up --login-server https://headscale.example.com

# 서버에서 승인
headscale nodes register \
  --user my-user --key nodekey:XXXX
```

## 웹 UI

Headscale 자체에는 웹 UI가 없습니다.
별도 프로젝트를 사용합니다.

- [Headscale-UI](https://github.com/gurucomputing/headscale-ui)
- [Headplane](https://github.com/tale/headplane)

## 참고

- [Headscale Docs](https://headscale.net/stable/usage/getting-started/)
- [Headscale & Tailscale 셀프 호스팅 가이드](https://www.lucasjanin.com/2025/01/03/headscale-tailscale-in-a-self-hosted-environment/)
