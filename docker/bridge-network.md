# Bridge Network

예전에는 `--link` 옵션으로 컨테이너를 연결했는데,
지금은 bridge network으로 깔끔하게 쓸 수 있다.

- [Legacy container links](https://docs.docker.com/network/links/) - 없어질 예정이니 쓰지 말 것.
- [Use bridge networks](https://docs.docker.com/network/bridge/) - 여기서 다루는 것.

## 사용하기

네트워크 생성:

```bash
docker network create my-net
```

Nginx 띄우기:

```bash
docker run -d --name nginx \
    --network my-net \
    -p 8080:80 \
    nginx
```

Nginx 연결 테스트:

```bash
docker run -it --rm \
  --network my-net \
  ruby:2.5.3 ruby -e "
    require 'open-uri'
    puts open('http://nginx:80/').read
  "
```

외부로 publish된 포트(`8080`)가 아니라
원래 포트(`80`)를 그대로 쓴다는 점에 주의할 것.
