# Grafana

<https://grafana.com/>

<https://github.com/grafana/grafana>

## Installation (Container)

[Run Grafana Docker image | Grafana documentation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/)

```bash
mkdir ~/data/grafana

docker run -d --name=grafana \
    --user "$(id -u)" \
    -v ~/data/grafana:/var/lib/grafana \
    -p 3000:3000 \
    grafana/grafana

docker logs -f grafana
```

다음 두 컨테이너 이미지는 같다:
- https://hub.docker.com/r/grafana/grafana
- https://hub.docker.com/r/grafana/grafana-oss
