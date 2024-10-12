# PostgreSQL

<https://hub.docker.com/_/postgres>

```bash
mkdir -p ~/data/my-postgres

docker run -d --name postgres \
  -e POSTGRES_PASSWORD=password \
  -v ~/data/my-postgres:/var/lib/postgresql/data \
  -p 65432:5432 \
  postgres:16.4

docker logs -f postgres

docker stop postgres
docker rm postgres
```
