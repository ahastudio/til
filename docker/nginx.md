# nginx

<https://hub.docker.com/_/nginx/>

## Nginx 실행 테스트

```bash
docker run -it --rm --name nginx -p 8080:80 nginx
```

<http://localhost:8080/>

## 간단한 HTML 띄우기

```bash
mkdir -p ~/nginx/html

echo "Welcome" > ~/nginx/html/index.html
```

```bash
docker run -d --name nginx \
    -p 8080:80 \
    -v ~/nginx/html:/usr/share/nginx/html \
    nginx
docker logs -f nginx
```

<http://localhost:8080/>
