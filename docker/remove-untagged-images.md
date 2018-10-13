# Remove untagges image

```bash
docker rmi $(docker images -f "dangling=true" -q)
```
