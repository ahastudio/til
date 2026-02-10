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

## 설정

```bash
mkdir -p ~/data/headscale/{config,lib}

curl https://raw.githubusercontent.com/juanfont/headscale/refs/heads/main/config-example.yaml \
  -o ~/data/headscale/config/config.yaml
```

`config.yaml` 파일의 주요 항목을 설정합니다.

```yaml
server_url: https://my-domain

listen_addr: 0.0.0.0:8080
```

## Docker로 실행

```bash
docker run -d --name headscale \
  --read-only \
  --tmpfs /var/run/headscale \
  -v ~/data/headscale/config:/etc/headscale:ro \
  -v ~/data/headscale/lib:/var/lib/headscale \
  -p 8080:8080 \
  -p 9090:9090 \
  --health-cmd "CMD headscale health" \
  headscale/headscale:latest \
  serve

docker logs -f headscale
```

잘 실행됐는지 확인합니다.

```bash
curl https://my-domain/health
```

## 사용자 생성

```bash
docker exec -it headscale \
  headscale users create my-user

docker exec -it headscale \
  headscale users list
```

## 노드 등록

**클라이언트에서 요청**:

```bash
tailscale up --login-server https://my-domain --accept-routes
```

**서버에서 승인**:

```bash
docker exec -it headscale \
  headscale nodes register --user my-user --key <REGISTRATION_KEY>
```

## 웹 UI

Headscale 자체에는 웹 UI가 없습니다.
별도 프로젝트를 사용합니다.

- [Headscale-UI](https://github.com/gurucomputing/headscale-ui)
- [Headplane](https://github.com/tale/headplane)

### Headplane

> A full-featured admin interface for Headscale

<https://headplane.net/>

가장 기능이 풍부한 Headscale 웹 UI.
Tailscale 공식 대시보드에 가까운 경험을 제공합니다.

- 노드 관리 (만료, 라우팅, 이름, 소유자)
- ACL/태그 설정
- DNS 설정
- OIDC 로그인 지원

```bash
docker run -d --name headplane \
  -p 3000:3000 \
  ghcr.io/tale/headplane:latest
```

## 참고

- [Headscale Docs](https://headscale.net/stable/usage/getting-started/)
- [Headscale & Tailscale 셀프 호스팅 가이드](https://www.lucasjanin.com/2025/01/03/headscale-tailscale-in-a-self-hosted-environment/)
