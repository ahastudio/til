# Remove untagges image

Prune unused Docker objects
<https://docs.docker.com/config/pruning/>

```bash
docker image prune
```

## 옛날 방식

직접 dangling image를 찾아서 삭제.

```bash
docker rmi $(docker images -f "dangling=true" -q)
```
