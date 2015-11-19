## Git ignores your indent changes

들여쓰기만 했을 때도 Git은 해당 라인을 전부 변경으로 표시합니다. 이걸 무시해 봅시다.

### Git
`git diff -w`

또는

`git diff --ignore-space-change`

참고: http://git-scm.com/docs/git-diff

### GitHub
URL 뒤에 `?w=1` 추가

참고: https://github.com/blog/967-github-secrets

### Example: Rails 코드로 살펴봅시다.
`abstract_adapter.rb`

[Original](https://github.com/rails/rails/commit/064877cab83d84fcf7be26e17639c5c2544ffc3d)
: if 구문이 case-when으로 바뀌면서 많은 코드에 들여쓰기가 적용되었습니다. 내용 변경 없이 들여쓰기만 했는지, 변경과 동시에 들여쓰기를 한건지 알기 어렵습니다.

[with w option](https://github.com/rails/rails/commit/064877cab83d84fcf7be26e17639c5c2544ffc3d?w=1)
: 단순히 들여쓰기만 한 부분은 나오지 않습니다. 들여쓰면서 수정된 부분이 명확히 보입니다.

### HTML
가장 유용히 쓸 수 있는 곳은 HTML입니다. Division이나 조건문 등을 추가하면서 막대한 양의 코드를 들여쓰는 경우에 이 옵션을 유용히 쓸 수 있습니다.

#### Discourse 사례 ####

1. `app/views/layouts/application.html.erb` [Original](https://github.com/discourse/discourse/commit/5171a23a9cb3b6742100d3e6907035c80e5c3ccc), [with w option](https://github.com/discourse/discourse/commit/5171a23a9cb3b6742100d3e6907035c80e5c3ccc?w=1)

2. `site_content_edit.js.handlebars` [Original](https://github.com/discourse/discourse/commit/abf910d210ffa722ca4c4f69daa95aaedd8b396f), [with w option](https://github.com/discourse/discourse/commit/abf910d210ffa722ca4c4f69daa95aaedd8b396f?w=1)

### 주의
Python이나 CoffeeScript 등에선 들여쓰기가 중요한 역할을 하기 때문에, 이 옵션에만 의존하면 문제가 생길 수 있습니다.
