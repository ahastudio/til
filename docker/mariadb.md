# MariaDB

<https://hub.docker.com/_/mariadb>

```bash
docker run -d --name mariadb \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=test \
  mariadb \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci

docker logs -f mariadb

docker stop mariadb
docker rm mariadb
```
