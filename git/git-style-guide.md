# Git Style Guide

<https://github.com/agis/git-style-guide> \
→ 한국어 번역:
<https://github.com/ikaruce/git-style-guide>

## Git Commit Message

[How to Write a Git Commit Message](https://cbea.ms/git-commit/) \
→ 한국어 번역:
[좋은 git 커밋 메시지를 작성하기 위한 7가지 약속 : NHN Cloud Meetup](https://meetup.nhncloud.com/posts/106)

“Use the imperative mood in the subject line”를
“제목은 `명령조`로”라고 옮겼는데,
번역 자체가 틀린 건 아니지만 한국어로 커밋 메시지를 쓰면 오용하기 쉬운 부분.

이 부분의 핵심은 “명령”이 아니라,
`과거형`이나 `명사형`으로 바꾸지 않고 `동사 원형`을 그대로 쓰라는 것.
다른 가이드를 보면 `현재형`을 쓰라고 표현하기도 함.

이 부분은 예시를 보면 자명하다.

- Fixed 어쩌고 (X)
- Fixing 어쩌고 (X)
- Fix 어쩌고 (O)

이를 한국어로 그냥 무작정 옮기면 어색할 수 있다는 점에 주의!

- 고쳤다
- 고침
- 고쳐라

해당 글에서 Git의 built-in convention과 통일성을 언급했기 때문에,
한국어로 커밋 메시지를 남기면 이 부분이 무의미하다.
따라서 한국어로 커밋 메시지를 남기는 팀이라면
해당 부분을 적절히 변경해서 적용하는 걸 강력히 추천한다.
