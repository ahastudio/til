# git log에서 보이지 않는 이전 commit 모두 확인하기

```
$ git reflog
```

이전 커밋으로 돌아가 복구하고 싶다면 다음과 같이 새로운 브랜치(temp)를 만들어서
쓰면 편하다.

```
$ git checkout -b temp <커밋번호>
```

reflog는 로컬 저장소만 활용하기 때문에, GitHub 저장소에서 쓰고 싶다면 API를
호출해야 한다. https://github.com/ahastudio/til/blob/master/github/reflog.md

참고:

- [Git - git-reflog Documentation](https://git-scm.com/docs/git-reflog)
- [Git - 리비전 조회하기](https://git-scm.com/book/ko/v2/Git-%EB%8F%84%EA%B5%AC-%EB%A6%AC%EB%B9%84%EC%A0%84-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0)
