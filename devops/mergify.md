# Mergify: merge queue로 main을 초록색으로 지키는 도구

<https://mergify.com/>

## 소개

Mergify는 GitHub 위에서 동작하는 CI 보조 서비스다.
홈페이지는 제품을 세 단으로 나눈다.
CI Insights는 느리거나 실패하거나 비용을 쓰는 CI 작업을 보여 주고,
Test Engine은 flaky test를 찾아 격리하며,
Merge Queue는 실제 main 위에서 테스트한 뒤에만 병합한다.

홈페이지의 약속은 한 문장이다.
PR을 묶어 함께 테스트하므로 queue가 적은 CI 실행으로 비워지고,
깨진 코드는 main에 닿지 않는다는 것이다.
이 문서는 그 약속을 설정 파일 수준까지 내려가 확인하고,
GitHub 기본 merge queue와 언제 갈라서는지 정리한다.

홈페이지는 사용 규모를 조직 2천 곳 이상, 사용자 2만 5천 명 이상,
저장소 30만 곳 이상, 월 7만 5천 건 이상의 자동 병합으로 적는다.
이 숫자는 운영사가 스스로 밝힌 것이고 외부에서 확인되지 않았다.

## 목차

- [동작 방식](#동작-방식)
  - [merge queue가 막는 문제](#merge-queue가-막는-문제)
  - [batch와 bisection](#batch와-bisection)
  - [나머지 두 제품](#나머지-두-제품)
- [설정하기](#설정하기)
  - [설치와 첫 PR](#설치와-첫-pr)
  - [검증한 .mergify.yml](#검증한-mergifyyml)
- [값 정하기](#값-정하기)
- [GitHub 기본 merge queue와 비교](#github-기본-merge-queue와-비교)
- [가격과 보안](#가격과-보안)
- [함정](#함정)
- [비평](#비평)
- [체크리스트](#체크리스트)
- [인사이트](#인사이트)

## 동작 방식

### merge queue가 막는 문제

홈페이지가 그리는 사고 경로는 이렇다.
PR이 열리고 초록색으로 보이며, CI가 flake로 한 번 흔들리고,
엔지니어가 초록이 될 때까지 다시 돌린다.
그러다 낡은 base 위에서 병합되어 main이 빨개지고,
조직 전체에서 빌드가 줄줄이 실패하며 배포가 막힌다.

핵심은 두 PR이 각자는 통과하지만 합치면 깨지는 경우다.
Mergify 문서는 설정이 하나도 없어도 queue가 PR을 최신 main에 맞춰 갱신하고,
갱신된 코드로 CI를 돌린 뒤 통과하면 자동 병합한다고 설명한다.
GitHub의 branch protection과 ruleset도 그대로 따른다.[^mq-setup]

### batch와 bisection

`batch_size`는 queue가 한 번에 묶어 테스트할 PR 수다.
3으로 두면 다음 PR 세 개의 변경을 담은 batch PR을 만들어 CI로 검증하고,
통과하면 세 PR을 함께 병합한다.
실패하면 문제의 PR을 찾아 queue에서 빼고
나머지를 계속 처리한다고 한다.[^batches]

`batch_max_wait_time`은 batch가 찰 때까지 기다리는 시간이다.
문서는 이것을 지연 시간과 CI 사용량 사이의 선택이라고 설명한다.
`batch_size`에 `min`과 `max`를 주면 동적 크기가 된다.
queue가 한가하면 min에 머물러 실패 격리가 싸고,
깊어지면 max로 커져 처리량을 낸다.[^batches]

batch를 만들 때 PR을 앞에서부터 순서대로 집지는 않는다.
우선순위가 먼저이고, 스택(서로 의존하는 PR)은 한 batch에 같이 들어가며,
남는 자리는 scope, 변경된 디렉터리, 대기 시간 순으로 비슷한 PR이 채운다.
batch가 실패해 쪼개질 때 무관한 PR이 남의
실패에 끌려가지 않게 하려는 설계다.[^batches]

### 나머지 두 제품

CI Insights는 작업별 실행 수, 소요 시간, 실패율, flakiness를 보여 주고
PR 코멘트로 CI 문제 요약을 올린다.
제품 페이지는 이를 쓰는 팀이 수동 재실행을 엔지니어당 주 15회에서
총 3회 미만으로 줄인다고 주장한다.
출처가 밝혀지지 않은 마케팅 수치다.[^ci-insights]

Test Engine은 test framework 안의 plugin(pytest-mergify,
rspec-mergify 등)으로 돌아간다.
PR이 추가하거나 바꾼 테스트를 같은 commit에서
다시 돌려 통과와 실패를 오가는 테스트를 잡고,
기본 브랜치의 불안정한 테스트에는 영향도 순위를 매겨 quarantine한다.
quarantine된 테스트가 실패해도 종료 코드에는 반영되지 않는다고
한다.[^test-engine]

## 설정하기

### 설치와 첫 PR

문서가 말하는 최소 절차는 세 단계다.
저장소에 Mergify GitHub App을 설치하고,
열린 PR에 `@mergifyio queue`라고 코멘트를 달고,
대시보드에서 PR이 queue를 지나가는 것을 본다.[^mq-setup]
설정 파일 없이도 이 상태가 queue로 동작한다.

설정 파일은 저장소의 `.mergify.yml`이다.
공식 문서는
파일 맨 위에 `yaml-language-server` 주석으로 JSON schema를 걸라고 안내하고,
pre-commit hook(`validate-mergify-config`)도 제공한다.[^file-format]

### 검증한 .mergify.yml

아래 설정은 batch, 동적 크기, 자동 queue,
병합 방식, 긴급 PR 우선순위를 한 번에 쓴다.
문서의 예시 조각을 이어 붙여 만들었고,
`docs.mergify.com/mergify-configuration-schema.json`에 대해 검증했다.
유효한 파일은 통과했고, 없는 키를 하나 넣은 같은 파일은 거부되었다.
단 이는 schema 검증이다.
실제 저장소에서 queue를 돌려 본 것은 아니다.

```yaml
# yaml-language-server: $schema=https://docs.mergify.com/mergify-configuration-schema.json
merge_queue:
  max_parallel_checks: 3

queue_rules:
  - name: default
    autoqueue: true
    merge_method: squash
    batch_size:
      min: 1
      max: 5
    batch_max_wait_time: 5 min
    queue_conditions:
      - base = main
      - "#approved-reviews-by >= 1"
      - check-success = ci
    merge_conditions:
      - check-success = ci

priority_rules:
  - name: hotfix
    conditions:
      - label = hotfix
    priority: high
```

각 키의 의미는 문서가 이렇게 정리한다.

| 키                    | 역할                                            |
| --------------------- | ----------------------------------------------- |
| `max_parallel_checks` | 동시에 검사하는 batch 수                        |
| `queue_conditions`    | PR이 queue에 들어갈 조건                        |
| `merge_conditions`    | queue 안에서 병합 전에 통과해야 할 조건         |
| `autoqueue`           | 조건을 만족하면 코멘트 없이 자동으로 queue 진입 |
| `merge_method`        | 병합 방식                                       |
| `priority_rules`      | 라벨이나 파일 경로로 우선순위 부여              |

`autoqueue`와 `queue_conditions`, `merge_conditions`의 조합은
문서의 Auto-Merge 예시에서 가져왔다.[^auto-merge]
우선순위 규칙은 `label = urgent` 같은 조건에 `priority: high`를 붙이는 형태이고,
`allow_checks_interruption: true`를 켜면
이미 돌고 있는 검사를 끊고 먼저 간다.[^priority]

## 값 정하기

병합 방식은 history 모양을 결정한다.
`merge`는 비선형이고 원래 commit이 보존되며,
`squash`와 `rebase`는 선형이지만 SHA가 새로 생기고,
`fast-forward`는 SHA를 보존하는 선형이지만 queue가 직렬로만 돈다.[^strategies]
batch나 병렬 검사를 쓸 계획이라면 `fast-forward`는 맞지 않는다.

`batch_size`는 지연 시간과 CI 비용의 교환이다.
작은 batch는 빠르고 실패 격리가 싸지만 CI를 더 쓰고,
큰 batch는 CI를 아끼고 밀린 queue를 빨리 비우지만
실패 한 번에 더 많은 PR을 쪼개 다시 돌려야 한다.[^batches]
처음에는 `min: 1`,
`max: 5` 같은 범위로 시작해 queue 통계를 보며 조정하는 쪽이 안전하다.

semi-linear history(리베이스 후 merge commit)가 필요하면 제약이 있다.
Mergify 대표가 HN에서
밝힌 바로는 batch와 병렬 검사를 쓰지 않을 때만 지원한다.[^hn-semilinear]

## GitHub 기본 merge queue와 비교

GitHub 기본 queue는 PR이 필수 검사를 통과한 뒤 쓰기 권한자가 넣으면,
최신 대상 브랜치와 앞선 PR들 위에서 필수 검사를 다시 통과시키는 방식이다.
CI는 `merge_group` 이벤트로 트리거해야 하고,
이를 빼먹으면 필수 검사가 보고되지 않아 병합이 실패한다.
빌드 동시성은 1에서 100 사이로 정하고,
병합 방식은 merge, rebase, squash 중 고른다.[^gh-mq]

Mergify는 비교 페이지에서 차이를 표로 보인다.
큐 8개에 대해 GitHub는 PR당 한 번씩 8번, Mergify는 batch로 최소 1번의 CI를 돌고,
실패 시 GitHub은 해당 PR을 빼고 나머지를 다시 만들지만
Mergify는 batch를 쪼개 원인을 찾는다고 한다.
monorepo scope, 일시적 실패 자동 재시도, flaky test 격리, queue 일시 정지는
GitHub 쪽 칸이 비어 있다.[^cmp-gh]
같은 페이지가 인정하는 대로
10명 미만, 15분 미만의 단일 workflow,
하루 PR 20개 미만이면 기본 queue로 충분하다.[^cmp-gh]

이 표는 판매자가 그린 것이다.
GitHub 문서에는 queue가 PR을 묶어 병합 그룹으로 만드는 설정도 있어서,
“PR당 한 번”이 모든 설정에서 성립하는지는 이 표만으로 알 수 없다.[^gh-mq]

## 가격과 보안

가격 페이지에는 세 등급이 있다.
Free는 오픈 소스 프로젝트와 비공개 저장소 5명까지 무료이고,
Max는 사용자 100명까지이며
좌석당 월 21달러로 표시된다(연간 전환 시 15% 할인 표기).
Enterprise는 맞춤 가격에 무제한 사용자, 온프레미스 배포를 제공한다.
세 제품은 모든 등급에 들어 있다.
활성 기여자는 최근 30일 안에 PR을 열거나 push한 사람으로 센다.[^pricing]
Merge Queue의 batch, scope, 스택 PR 같은 기능 열도 등급표에 있으므로
계약 전에 해당 열이 본인 등급에 포함되는지 직접 확인해야 한다.

보안 문서는 SOC 2 Type II 인증, 전송 구간 TLS 1.2 이상,
저장 데이터 AES-256 암호화를 적는다.
저장소 내용은 보관하지 않고, rebase나 병합 같은 git 작업을 할 때만
임시 디렉터리에 clone했다가 끝나면 지운다고 한다.
로그인은 GitHub OAuth뿐이며 역할은 GitHub에서 상속한다.[^security]

## 함정

- 필수 검사 이름이 `queue_conditions`나 `merge_conditions`와 어긋나면
queue가 영원히 기다린다.
  예시의 `check-success = ci`는 자기 저장소의 검사 이름으로 바꿔야 한다.
- batch는 flaky test와 잘 맞지 않는다.
  flake로 batch가 실패하면 쪼개 다시 도는 비용이 커지므로,
  Test Engine이나 Auto-Retry로 flake를 먼저 줄이는 것이 순서다.
- `fast-forward`는 직렬 전용이다.
  병렬 검사나 batch로 처리량을 얻으려는 계획과 충돌한다.
- 홈페이지의 `3-5×`, `60-90%` 같은 수치는 조건이 붙지 않은 문구다.
  자기 CI 시간과 PR 빈도로 계산기를 돌리기 전에는 기대치로 쓰지 않는다.
- GitHub 로그인 외에 별도 계정이 없다.
  GitHub 장애 때 queue도 같이 멈추는 구조임을 전제로 운영해야 한다.[^security]

## 비평

가장 강한 주장은 PR이 많고 CI가 길수록 merge queue가 필수라는 것이다.
이 점은 외부 증언도 받쳐 준다.
Mergify 블로그의 merge queue 연혁 글이 HN에 올랐을 때,
GitHub 직원이 쓴 경험담이 올라왔다.
2017년 무렵 GitHub 내부 queue는 PR 하나를 병합하는
데 하루를 붙들게 했다는 것이다.[^hn-jes]
queue가 필요하다는 사실과 Mergify가 그
일을 가장 잘한다는 사실은 별개의 주장이다.

반론은 queue 자체가 과하다는 쪽에서 나왔다.
한 사용자는 merge skew는 드물어서
main을 깨진 뒤 자동 revert하는 쪽이 낫다고 썼고,[^hn-kccqzy]
다른 사용자는 queue는 임시 브랜치에서 먼저 검증하므로 main이 깨지지 않아
개발자가 깨진 commit을 받는 혼란이 없다고 반박했다.[^hn-kevincox]
어느 쪽이 맞는지는 팀의 PR 빈도와 CI 길이에 달렸다.
Mergify 자신의 비교 페이지가 작은 팀에는
기본 queue를 권한다는 점이 이를 인정한다.

운영사 신뢰도에 대한 문제도 있었다.
위 HN 글에서 한 사용자는 글과 답변에서
AI 느낌이 나서 인상이 나빴다고 적었고,[^hn-qlm]
다른 사용자는 경쟁사 Graphite 창업자가 자기 글과 비슷하다고
지적했다.[^hn-foster]
Lobste.rs에서는 DVCS 시절의 bot이 빠졌다는 지적이 달렸다.[^lobsters-robey]
이는 블로그 글에 대한 반응이지 제품에 대한 평가가 아니다.
다만 홈페이지의 수치와 비교표를 읽을 때
판매자 자료라는 점을 잊지 말라는 이유는 된다.

Lobste.rs의 한 댓글은 queue가 monorepo의 산물이며 직렬 queue는 느리고
이를 풀려는 투기적 스케줄링이 CI 자원을 더 쓴다고 지적했다.[^lobsters-sluongng]
batch와 병렬 검사는 이 문제에 대한 Mergify의 답이다.
그래서
이 도구의 가치는 queue 자체가 아니라 batch
실패 시 원인을 얼마나 잘 찾느냐에 있다.
이 부분을 외부에서 측정한 자료는 이번에 찾지 못했다.

이 판단을 바꿀 관찰은 하나다.
같은 저장소에서 기본 queue와 Mergify를 같은 기간 돌려
PR당 CI 실행 수와 병합까지 걸린 시간을 비교한 결과다.
Cerebras 사례(350명 monorepo, 3시간 테스트 주기에서 처리량 2배)는
고객 사례 페이지에 있을 뿐 독립 측정이 아니다.

HN과 Lobste.rs에는 이 홈페이지 URL을 직접 다룬 글이 없었고,
GeekNews 검색은 mergify에 결과가 없었다.
(GeekNews는 검색어 `merge queue`로 대조해 검색 자체가 동작함을 확인했다.)

## 체크리스트

1. 지난 한 달의 PR 수, CI 소요 시간, main이 깨진 횟수를 센다.
   하루 20개 미만에 CI가 15분 미만이면 기본 queue부터 쓴다.
2. 저장소에 Mergify App을 설치하고 PR 하나에 `@mergifyio queue`를 달아 본다.
3. 위 `.mergify.yml`에서 검사 이름(`ci`)과 브랜치(`main`)를 바꾸고,
   schema 주석을 건 채 편집기와 pre-commit hook으로 검증한다.
4. 처음에는 `batch_size`를 1로 두고 일주일을 돌려 기준선을 잡는다.
5. 기준선 위에서 `min: 1, max: 5`를 켜고 CI 실행 수와 대기 시간을 비교한다.
6. flaky test가 batch를 자꾸 깨면 Test Engine이나 Auto-Retry를 먼저 붙인다.
7. 가격 페이지의 기능 열이 쓰려는 등급에 포함되는지 확인한다.

실패 조건은 명확하다.
기준선 대비 CI 실행 수가 줄지 않거나 병합 대기 시간이 늘면
batch를 끄고 기본 queue로 돌아간다.

## 인사이트

Mergify의 상품은 queue가 아니라 queue가 흔들릴 때의 복구 비용이다.
GitHub 기본 queue가 있는 상황에서 별도 도구를 쓸 이유는
batch로 실행 수를 줄이는 것과 flake가 병합을 막지 않게 하는 것,
이 두 가지로 좁혀진다.
둘 다 팀의 PR 빈도와 CI 길이가 어느 선을 넘어야 값이 나온다.
그 선을 넘기 전에는 설정 파일 한 줄 늘리는 것도 운영 부담이다.

따라서
도입 결정은 홈페이지가 아니라 자기 저장소의 기준선 일주일로 내리는 것이 맞다.

[^mq-setup]: Mergify Docs, [Setting Up a Merge Queue](https://docs.mergify.com/merge-queue/setup/)

[^batches]: Mergify Docs, [Merge Queue Batches](https://docs.mergify.com/merge-queue/batches/)

[^ci-insights]: Mergify, [CI Insights](https://mergify.com/product/ci-insights)

[^test-engine]: Mergify, [Test Engine](https://mergify.com/product/test-engine)

[^file-format]: Mergify Docs, [Configuration File Format](https://docs.mergify.com/configuration/file-format/)

[^auto-merge]: Mergify Docs, [Auto-Merge](https://docs.mergify.com/merge-protections/auto-merge/)

[^priority]: Mergify Docs, [Merge Queue Priority](https://docs.mergify.com/merge-queue/priority/)

[^strategies]: Mergify Docs, [Merge Strategies](https://docs.mergify.com/merge-queue/merge-strategies/)

[^gh-mq]: GitHub Docs, [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)

[^cmp-gh]: Mergify, [Mergify vs GitHub merge queue](https://mergify.com/compare/github-merge-queue)

[^pricing]: Mergify, [Pricing](https://mergify.com/pricing)

[^security]: Mergify Docs, [Security](https://docs.mergify.com/security/)

[^hn-semilinear]: <https://news.ycombinator.com/item?id=45208911>

[^hn-jes]: <https://news.ycombinator.com/item?id=45200945>

[^hn-kccqzy]: <https://news.ycombinator.com/item?id=45202149>

[^hn-kevincox]: <https://news.ycombinator.com/item?id=45202994>

[^hn-qlm]: <https://news.ycombinator.com/item?id=45201590>

[^hn-foster]: <https://news.ycombinator.com/item?id=45205248>

[^lobsters-robey]: <https://lobste.rs/s/h6peie/origin_story_merge_queues#c_0mzcju>

[^lobsters-sluongng]: <https://lobste.rs/s/h6peie/origin_story_merge_queues#c_ycnfsw>
