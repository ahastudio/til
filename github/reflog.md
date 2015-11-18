= 특정 Commit으로 master 브랜치 복구

```
$ curl -u ahastudio -X POST \
  -d '{"ref":"refs/heads/new-master", "sha":"SHA123456789"}' \
  https://api.github.com/repos/ahastudio/test-repo/git/refs
```
