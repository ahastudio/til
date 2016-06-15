# git log에서 보이지 않는 이전 commit 모두 확인하기

```
$ git reflog
```

이전 커밋으로 돌아가 복구하고 싶다면 다음과 같이 새로운 브랜치(master2)를 만든다.

```
$ git checkout -b master2 <커밋번호>
```

reflog는 로컬 저장소만 활용하기 때문에, GitHub 저장소에서 쓰고 싶다면 API를 호출해야 한다.
https://github.com/ahastudio/til/blob/master/github/reflog.md
