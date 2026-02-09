# git push --force-with-lease

`git push --force`는 원격 저장소의 히스토리를 로컬 기준으로
강제로 덮어쓴다. 다른 사람이 그 사이에 push한 커밋이 있어도
무조건 덮어쓰기 때문에, 해당 커밋이 유실될 수 있다.

`--force-with-lease`는 이 문제를 해결하는 안전한 대안이다.

## 동작 방식

원격 브랜치의 현재 상태가 마지막으로 fetch한 시점과
동일한지 확인한 뒤, 일치할 때만 force push를 수행한다.
누군가 그 사이에 push한 커밋이 있으면 push가 거부된다.

```bash
# 안전한 force push
git push --force-with-lease

# 특정 브랜치 지정
git push --force-with-lease origin feature-branch
```

## 언제 쓰나

- `git rebase` 후 원격 브랜치를 업데이트할 때
- `git commit --amend` 후 push할 때
- 히스토리를 정리한 뒤 원격에 반영할 때

이런 상황에서 `--force`를 쓰면 동료의 작업을 날릴 수 있다.
`--force-with-lease`를 쓰면 그런 위험 없이 안전하게
force push할 수 있다.

## 주의

`git fetch`를 먼저 실행하면 원격 브랜치의 최신 상태를
로컬에 가져오기 때문에, `--force-with-lease`가 항상
성공하게 된다. fetch 직후에는 보호 효과가 없으므로
주의해야 한다.

## alias 설정

자주 쓴다면 alias를 설정하면 편하다.

```bash
git config --global alias.pushf \
  "push --force-with-lease"
```

```bash
# 사용 예
git pushf origin feature-branch
```

참고:
- [git-push - --force-with-lease](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt)
