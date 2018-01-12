# Let's Encrypt - Free SSL/TLS Certificates

https://letsencrypt.org/

## Certbot을 Docker로 실행해 인증서 만들기

Docker를 이용하면 불필요한 프로그램 설치를 피할 수 있다.

```
docker run -it --rm -p 443:443 -p 80:80 --name certbot \
    -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    -v "/var/log/letsencrypt/:/var/log/letsencrypt/" \
    certbot/certbot certonly --standalone -d 도메인
```
