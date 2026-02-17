# git push --force-with-lease

`git push --force`는 원격 저장소를 강제로 덮어쓰기 때문에, 다른 사람의 커밋이
유실될 수 있습니다. `--force-with-lease`는 이를 방지하는 안전한 대안입니다.

## 동작 방식

마지막으로 fetch한 시점과 원격 브랜치 상태가 일치할 때만 force push를
수행합니다. 그 사이에 다른 커밋이 추가되었으면 push가 거부됩니다.

```bash
git push --force-with-lease
git push --force-with-lease origin feature-branch
```

## 언제 쓰나

- `git rebase` 후 원격 브랜치를 업데이트할 때
- `git commit --amend` 후 push할 때
- 히스토리를 정리한 뒤 원격에 반영할 때

## 주의

`git fetch` 직후에는 원격의 최신 상태를 이미 알고 있으므로
`--force-with-lease`의 보호 효과가 없습니다.

## alias 설정

```bash
git config --global alias.pushf \
  "push --force-with-lease"
```

참고:

- [git-push - --force-with-lease](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt)
