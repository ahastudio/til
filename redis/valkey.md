# Valkey

> A new project to resume development on the formerly open-source Redis project.
> We're calling it Valkey, since it's a twist on the key-value datastore.

<https://valkey.io/>

<https://github.com/valkey-io/valkey>

[Linux Foundation Launches Open Source Valkey Community](https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community)
\
→ 한국어 요약:
[Valkey - 리눅스 재단(Linux Foundation)이 발표한 Redis의 오픈소스 | GeekNews](https://news.hada.io/topic?id=14057)

[Valkey is Rapidly Overtaking Redis - DevOps.com](https://devops.com/valkey-is-rapidly-overtaking-redis/)
\
→ 한국어 요약:
[GN⁺: Valkey가 빠르게 Redis를 대체하고 있음 | GeekNews](https://news.hada.io/topic?id=14436)

## Container

<https://hub.docker.com/r/valkey/valkey>

<https://github.com/valkey-io/valkey-container>

```bash
docker pull valkey/valkey:7.2-alpine

docker run -d --name valkey \
    -p 6379:6379 \
    valkey/valkey:7.2-alpine

docker logs -f valkey
```

```bash
docker exec -it valkey valkey-cli monitor
```

```bash
docker exec -it valkey valkey-cli
```

```bash
docker stop valkey
docker rm valkey
```
