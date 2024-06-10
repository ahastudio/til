# Grafana

<https://grafana.com/>

<https://github.com/grafana/grafana>

## Installation (Container)

- https://hub.docker.com/r/grafana/grafana
- https://hub.docker.com/r/grafana/grafana-oss

https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/

```bash
mkdir ~/data/grafana

docker run -d --name=grafana \
    -p 3000:3000 \
    -v ~/data/grafana:/var/lib/grafana \
    grafana/grafana

docker logs -f grafana
```
