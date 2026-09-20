# cherry-pick과 revert는 패치를 적용하지 않고 3방향 병합을 한다

원문: [How git cherry-pick and revert use 3-way merge](https://jvns.ca/blog/2023/11/10/how-cherry-pick-and-revert-work/)

HN 토론: <https://news.ycombinator.com/item?id=38222596> (211점, 123개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/j4ljoz/how_git_cherry_pick_revert_use_3_way_merge> (19점, 1개 댓글)

## 요약

Julia Evans가 2023년 11월 10일에 쓴 글이다.

시작이 솔직하다. 며칠 전 누군가에게 `git cherry-pick`이 어떻게 동작하는지 설명하려다 **자기가 헷갈리고 있다는 것을 발견했다**는 것이다.

무엇이 잘못되었는가 하면, cherry-pick이 기본적으로 패치를 적용하는 것이라고 생각했는데 **실제로 그렇게 해 보니 되지 않았다**는 것이다.

글은 자기가 틀린 지점을 먼저 보여 준다.

원래 갖고 있던 모델은 이렇다. `COMMIT_ID`의 diff를 계산하고(`git show COMMIT_ID --patch > out.patch`), 그 패치를 현재 브랜치에 적용한다(`git apply out.patch`).

저자가 여기서 선을 하나 긋는다. **이 모델이 대체로 맞으며 이것이 당신의 심상 모델이라면 괜찮다**는 것이다. 다만 미묘하게 틀린 데가 있고 그게 흥미로우니 보자는 것이다.

충돌이 나는 경우에 두 방식이 갈린다.

```text
$ git show 10e96e46 --patch > out.patch
$ git apply out.patch
error: patch failed: content/post/2023-07-28-why-is-dns-still-hard-to-learn-.markdown:17
error: content/post/...markdown: patch does not apply
```

`git apply`는 그냥 **실패한다**. 충돌을 해결하거나 문제를 파악할 방법을 주지 않는다.

반면 `git cherry-pick`은 병합 충돌을 준다.

```text
$ git cherry-pick 10e96e46
error: could not apply 10e96e46... wip
hint: After resolving the conflicts, mark them with
hint: "git add/rm <pathspec>", then run
hint: "git cherry-pick --continue".
```

그래서 “git이 패치를 적용한다”는 모델이 정확하지 않아 보이는데, 오류 메시지가 문자 그대로 “could not **apply**”라고 하니 **완전히 틀린 것도 아니다**.

git 소스를 뒤져 도달한 한 줄이 답이다.

```c
res = do_recursive_merge(r, base, next, base_label, next_label, &head, &msgbuf, opts);
```

**cherry-pick이 병합이라는 것**이다.

## 3방향 병합

### 원본이 있으면 답이 보인다

저자가 든 예가 명료하다. 두 파일을 병합해야 한다.

```python
# v1.py
def greet():
    greeting = "hello"
    name = "julia"
    return greeting + " " + name
```

```python
# v2.py
def say_hello():
    greeting = "hello"
    name = "aanya"
    return greeting + " " + name
```

두 줄이 다르다. `def greet()` 대 `def say_hello()`, 그리고 `name = "julia"` 대 `name = "aanya"`다.
무엇을 골라야 하는지 **알 방법이 없어 보인다**.

그런데 원래 함수가 이랬다면 어떨까.

```python
# base.py
def say_hello():
    greeting = "hello"
    name = "julia"
    return greeting + " " + name
```

갑자기 훨씬 분명해진다.
**v1은 함수 이름을 `greet`으로 바꿨고 v2는 `name`을 `aanya`로 바꿨다.** 그러니 둘 다 적용하면 된다.

git에게 직접 시킬 수 있다.

```bash
git merge-file v1.py base.py v2.py -p
```

```python
def greet():
    greeting = "hello"
    name = "aanya"
    return greeting + " " + name
```

두 파일과 그 원본을 함께 병합하는 이 방식을 **3방향 병합**이라고 부른다.

### git은 파일이 아니라 변경을 병합한다

저자가 3방향 병합을 이해하는 방식이 이 한 문장이다.

git은 파일이 아니라 **변경을 병합한다**.

원본 파일 하나와 그에 대한 가능한 변경 두 개가 있고, git이 그 둘을 합리적으로 결합하려 시도한다.
못 할 때도 있고(둘 다 같은 줄을 바꾼 경우), 그때 병합 충돌이 난다.

두 개보다 많은 변경도 병합할 수 있다. 원본 하나에 가능한 변경 여덟 개를 놓고 전부 조정하려 시도할 수 있으며, 그것을 **옥토퍼스 병합**이라고 부른다.
저자는 그 이상은 모르고 해 본 적도 없다고 덧붙인다.

## 세 명령이 같은 뼈대를 쓴다

git이 “패치를 적용한다”고 말할 때 — rebase든 revert든 cherry-pick이든 — **실제로 패치 파일을 만들어 적용하는 것이 아니다**. 3방향 병합을 한다.

커밋 `X`를 현재 커밋에 패치로 적용하는 것이 앞의 v1/v2/base 구도에 이렇게 대응된다.

| 3방향 병합의 역할 | 무엇인가                    |
| ----------------- | --------------------------- |
| `v1`              | 현재 커밋의 파일 버전       |
| `base`            | 커밋 X **직전**의 파일 버전 |
| `v2`              | 커밋 X의 파일 버전          |

즉 **`base`와 `v2`를 합쳐서 “패치”로 생각하면 된다.** 둘의 차이가 `v1`에 적용하려는 변경이다.

### cherry-pick

이런 그래프에서 `Y`를 `main`에 cherry-pick 한다고 하자.

```text
A - B (main)
 \
  X - Y - Z
```

| 역할 | 커밋 |
| ---- | ---- |
| v1   | `B`  |
| base | `X`  |
| v2   | `Y`  |

`X`와 `Y`가 함께 “패치”다.

그리고 **`git rebase`는 `git cherry-pick`을 여러 번 반복하는 것**일 뿐이다.

### revert

`X - Y - Z - A - B` 그래프에서 `git revert Y`를 한다고 하자.

| 역할 | 커밋 |
| ---- | ---- |
| v1   | `B`  |
| base | `Y`  |
| v2   | `X`  |

cherry-pick과 **정확히 같은데 `X`와 `Y`가 뒤집혔다**. “역방향 패치”를 적용하고 싶기 때문이다.

revert와 cherry-pick이 워낙 가까워서 git 안에서 **같은 파일(`revert.c`)에 구현되어 있다**.

### 3방향 패치라는 발상

저자는 이 기법에 이름이 없는 것 같다며 **“3방향 패치”**라고 부르고 싶다고 적는다.

3방향 패치는 패치를 파일 **두 개**로 명시한다. 패치 이전 파일과 이후 파일이다.
그래서 관련 파일이 셋이 된다. 원본 하나와 패치를 이루는 둘이다.

왜 더 나은가. **두 전체 파일을 다 가지고 있으므로 병합할 때 문맥이 훨씬 많기 때문**이다.

일반 패치는 이렇게 생겼다.

```diff
@@ -1,1 +1,1 @@:
- def greet():
+ def say_hello():
  greeting = "hello"
```

3방향 패치는 이렇다. 실제 파일 형식이 아니라 저자가 지어낸 것이다.

```text
BEFORE: (전체 파일)
def greet():
    greeting = "hello"
    name = "julia"
    return greeting + " " + name

AFTER: (전체 파일)
def say_hello():
    greeting = "hello"
    name = "julia"
    return greeting + " " + name
```

## 확인하기

### 충돌 표시에 base를 켜 둔다

이 글을 읽고 바로 바꿀 만한 설정 하나가 HN에서 나왔다.

juped가 `merge.conflictStyle`을 `diff3`으로 두면 **병합 충돌의 세 입력을 전부** — 왼쪽과 오른쪽만이 아니라 base까지 — 볼 수 있다고 적었다.[^juped]
그래야 왼쪽이 base에 무슨 변경을 했고 오른쪽이 무슨 변경을 했는지 보이므로 **추측하지 않고 실제로 해결할 수 있다**는 것이다.

그리고 이것이 기본값이면 좋겠다고 덧붙였다. 기본이 아닌 이유는 특정 재귀 병합을 아주 기이하게 표시하기 때문이라고 한다.

Amorymeltzer는 몇 년 전에 바꾸고 다시 돌아가지 않았다고 답했다.[^Amorymeltzer]
처음에는 무엇을 보고 있는지 명확하지 않아 적응이 좀 필요하지만, **단순한 경우에는 손해가 없고 험한 충돌에서는 전체 문맥이 있다는 것이 엄청난 도움**이라는 것이다.
그리고 git 2.35 이상에서는 “열성적인 diff3”인 `zdiff3`을 쓴다고 덧붙였다.

```bash
git config --global merge.conflictStyle zdiff3
```

이 설정 하나가 이 글의 내용을 매일 눈으로 보게 만든다. base가 보이면 3방향 병합이 무엇인지 설명할 필요가 없어진다.

### `git apply --3way`로 같은 일을 해 본다

저자가 직접 확인한 경로다.

`git apply`에도 3방향 병합을 하는 `--3way` 플래그가 있어서, cherry-pick과 비슷한 것을 이렇게 구현할 수 있다.

```bash
git show 10e96e46 --patch > out.patch
git apply out.patch --3way
```

그런데 `--3way`는 **패치 파일의 내용만 쓰는 것이 아니다**.

패치 파일이 이렇게 시작한다.

```text
index d63ade04..65778fc0 100644
```

`d63ade04`와 `65778fc0`이 그 파일의 이전·이후 버전이 **git 객체 데이터베이스에서 갖는 ID**다. git이 그것을 꺼내 3방향 패치 적용을 한다.

그래서 누가 패치를 메일로 보내 주었고 내게 그 파일 버전들이 없으면 되지 않는다.

```text
$ git apply out.patch
error: repository lacks the necessary blob to perform 3-way merge.
```

juped가 이 점을 정리했다. `git apply`가 `--3way`를 알지만 **적용되는 패치가 생성될 때 블롭 해시를 기록해 두어야 한다**는 것이고, git이 생성한 패치라면 그렇게 된다.
`git am`도 전이적으로 `--3way`를 안다고 덧붙였다.[^juped-apply]

### 문맥을 키우면 같아지는가

chx가 좋은 질문을 던졌다.[^chx]
10억 줄보다 짧은 파일에 대해 `git show -U1000000000 $hash > x.patch; git apply x.patch`와 `git cherry-pick $hash`의 차이가 무엇이냐는 것이다.

문맥 줄을 무한히 키우면 전체 파일이 담기니 3방향 패치와 같아지지 않느냐는 발상이다.

coryrc의 답이 핵심을 짚는다.[^coryrc]
**3방향 병합에는 패치로는 수동 해결해야 할 충돌 일부를 피할 수 있는 정보가 더 있다**는 것이고, 그 점만 빼면 발상 자체는 맞다는 것이다.

차이는 이렇다. 문맥을 키운 패치도 결국 “이 줄들을 찾아 바꿔라”이고, 찾지 못하면 실패한다.
3방향 병합은 **base 대비 양쪽이 각각 무엇을 바꿨는지를 계산**하므로, 겹치지 않는 변경이면 자동으로 합친다.

## 함정

### merge-base와 cherry-pick의 base는 다르다

이 글에서 가장 많은 혼란을 부른 지점이다.

crdrost가 반론을 폈다.[^crdrost]
`B -- X1 -- X2 -- X3 -- Head` 와 `B -- Y1 -- Y2 -- Cherry` 상황이라면, **`Y2`가 Head와 Cherry 사이의 merge-base일 수 없고 merge-base는 `B`**라는 것이다. 그것은 그래프 속성이지 입력이 아니며 `git merge-base`로 계산할 수도 있다는 지적이다.
그리고 “`Y2`와 Cherry가 패치다”라는 표현이 이해에 도움이 되지 않는다고 덧붙였다.

oasisaimlessly의 답이 이 혼란을 정확히 해소한다.[^oasisaimlessly]

`git merge-base`의 출력은 **일반 병합을 할 때** 쓰이는 3방향 diff의 base다. 그게 전부다.
cherry-pick과 revert 같은 다른 연산은 **다른 base 커밋을 쓴다**.
눈을 가늘게 뜨고 보면 이 연산들을 **비정상적으로 선택된 base를 가진 병합**으로 볼 수 있고, 그것이 이 글의 요점 전체다.

그러면서 문제가 용어일 뿐이라고 정리한다.
**`3way_merge(v1, base, v2)` 알고리즘이 쓰인다는 것이 `base = merge_base(v1, v2)`인 병합이 수행된다는 뜻은 아니다**는 것이다.

andrewla도 같은 이해를 다르게 설명했다.[^andrewla]
cherry-pick의 목적에서 git이 **`Y2`의 부모가 병합의 base인 척한다**는 것이며, git은 패치나 diff가 아니라 **내용만 신경 쓴다**는 것이다.
이 연산의 효과는 `Y1 → X3`에 필요한 것과 `Y1 → Y2`에 필요한 것을 비교하는 것이고 경로는 상관하지 않는다.
예를 들어 `Y1`이 새 함수를 추가했다면, 3방향 diff를 계산할 때 **“X3 쪽에서는 그 함수가 제거되었군”이라고 말하게 된다**는 것이다.

그가 이것을 **“놀랍도록 영리하다”**고 평했는데, 동시에 이 문장이 cherry-pick이 가끔 이상하게 구는 이유이기도 하다.

이 함정을 한 줄로 정리하면 이렇다.
cherry-pick의 base는 그래프에서 계산되지 않는다. **대상 커밋의 부모로 지정된다**.

### 반복되는 충돌의 정체

xg15이 이 글에서 얻은 것을 짧게 적었다.[^xg15]

rebase를 이해하는 데도 정말 유용하며, **rebase가 3방향 병합의 연속이라는 통찰이 그 오류들과 악명 높은 “반복되는 병합 충돌” 문제를 드디어 이해할 수 있게 해 주었다**는 것이다.

이것이 실무에서 가장 값진 귀결이다.

rebase가 커밋마다 독립적인 3방향 병합을 하므로, 각 병합이 **자기 base만 본다**.
첫 커밋에서 해결한 충돌을 두 번째 커밋이 알지 못하고, 그래서 같은 충돌을 다시 만난다.

그러므로 반복 충돌은 버그가 아니라 구조의 결과다. 그리고 대응책이 따로 있다.

```bash
# 같은 충돌 해결을 기록해 두었다가 재사용한다
git config --global rerere.enabled true
```

### 3방향 병합은 결합법칙을 만족하지 않는다

crdrost가 이 스레드에서 가장 깊은 지적을 남겼다.[^crdrost-assoc]

**3방향 병합이 결합법칙을 만족하는 연산이 아니며, 그래서 가끔 놀라운 동작으로 이어질 수 있다**는 것이다. Pijul 문서를 근거로 들었다.

무슨 뜻인가 하면, 세 변경 A와 B와 C를 병합할 때 `(A∘B)∘C`와 `A∘(B∘C)`의 결과가 다를 수 있다는 것이다.

이것이 추상적인 이야기가 아니다.
rebase 중에 커밋 순서를 바꾸면 충돌 양상이 달라지는 이유, 같은 변경 집합을 다른 순서로 통합하면 결과가 갈리는 이유가 여기에 있다.

Pijul이나 Darcs 같은 패치 이론 기반 시스템이 존재하는 이유가 정확히 이 성질을 없애려는 것이다.

## 비평

### 알고리즘의 나이를 늦게 밝힌다

이 글이 3방향 병합을 새로 발견한 것처럼 서술하다가, 맨 끝에 가서야 “몇몇 사람이 3방향 병합이 git보다 훨씬 오래되었고 70년대 후반의 것이라고 짚어 주었다”고 덧붙인다.

not2b가 그 지적을 구체적으로 했다.[^not2b]
3방향 병합이 git보다 훨씬 오래되었고 **1979년부터 Version 7 Unix의 일부였던 `diff3` 프로그램에 구현되어 있으며**, 같은 알고리즘을 CVS와 Perforce와 사실상 다른 모든 버전 관리 시스템이 쓴다는 것이다.
GNU 버전이 diffutils의 일부이고 BSD 버전도 있다고 덧붙였다.

loeg는 BSD 버전이 사실 꽤 최근이라며, FreeBSD가 2017년에 완전히 동작하지는 않는 버전을 들여왔고 2022년에 더 작업했지만 **기본 제공은 여전히 2007년경의 GNU diff3**이라고 정정했다.[^loeg]

이 순서가 글의 인상을 바꾼다.

“이 기법이 정말 영리하고 멋지며 전에 들어 본 적이 없어 놀랍다”는 문장이 본문 한가운데 있는데, 사실은 **40년 넘은 표준 알고리즘**이다.
발견의 서사로 쓰인 글이라 개인적 놀라움이 그대로 남은 것인데, 독자 입장에서는 앞쪽에 한 줄 있었으면 좋았을 자리다.

다만 이 순서가 글을 나쁘게 만들지는 않는다. 오히려 다음 절의 이야기와 이어진다.

### 이 내용이 왜 어디에도 없는가

Lobste.rs의 유일한 댓글이 이 글의 진짜 값어치를 말한다.

arxanas가 적었다.[^arxanas]
최근에 이 주제를 조사했는데 **거의 모든 git 학습 자료가 3방향 병합에 관한 결정적인 정보를 빠뜨리고 있다**는 것이다.
대부분의 설명이 **DAG 수준에서만 다루는데, 그래프 구조만으로는 자기 워크플로에서 git이 실제로 어떻게 행동할지 예측할 수 없다**는 것이다.

그리고 이 글이 지금까지 본 것 중 이 주제에 대해 가장 나은 글일 것이라며, 다른 자료를 아는 사람이 있으면 알려 달라고 청했다.

저자 본인도 같은 공백을 확인했다.
James Coglan의 **Building Git**이 git 소스 코드 말고 `git cherry-pick`이 3방향 병합을 쓴다고 설명하는 **유일한 자료**였다는 것이다. Pro Git에 있을 줄 알았는데 없어 보였다고 적는다.

이 두 증언이 겹치는 것이 시사적이다.

git 교육 자료가 거의 전부 **커밋 그래프**를 그린다. 브랜치가 갈라지고 합쳐지는 그림이다.
그런데 실무에서 사람을 막히게 하는 것은 그래프가 아니라 **충돌**이고, 충돌은 그래프가 아니라 3방향 병합에서 나온다.

즉 가르치기 쉬운 것과 필요한 것이 어긋나 있다.
그래프는 그림으로 그릴 수 있고 3방향 병합은 그렇지 않다는 점이 그 어긋남의 원인일 것이다.

### git의 복잡도 논쟁으로 번졌지만 답이 없다

vvpan이 솔직한 질문을 던졌다.[^vvpan]
git이 대부분의 용도에 대해 지금처럼 복잡해야만 하느냐, 자기와 남의 git 문제를 고치느라 막힌 횟수가 필요 이상으로 많았다는 것이다.
rebase가 훨씬 말이 되므로 직장에서 merge를 너무 오래 안 써서 어떻게 동작하는지 잊었다고 적고, git이 수천 가지 기능을 주는데 자기는 셋만 쓴다고 덧붙였다.
그리고 **더 매끄러운 UX였던 것으로 기억하는 Mercurial이 사라졌다**는 점을 아쉬워했다.

AlotOfReading이 답했다.[^AlotOfReading]
git이 더 단순한 인터페이스를 가질 수는 있지만, 정신적 부담을 대폭 줄이는 것은 결국 **도구로서의 힘을 줄이는 일**이 된다는 것이다.
매력의 큰 부분이 파워 유저와 초보자가 같은 도구에 동의하고 각자의 필요에 맞게 쓸 수 있다는 점이며, 원하는 방식으로 경험을 단순화하는 프런트엔드와 스크립트의 거대한 애프터마켓이 있다고 적었다.
jujutsu 같은 일부는 사실상 git 위에 지어진 새로운 VCS라는 것이다.

그리고 Mercurial에 대해 한마디 덧붙였다. 자기는 Mercurial이 싫지 않았지만, **Google과 Facebook처럼 그것을 밀던 거대 기업들조차 각자의 도구(fig/sapling)로 갈라져 나간 것이 시사적**이라는 것이다.

b212은 반대편의 실용적 입장을 대변했다.[^b212]
자기는 99% 시간 동안 `git pull`, `add`, `commit`, `merge`, `push`, `status`, `log`, `checkout -- filename`만 쓰는데 자기만 그러냐는 것이다.
기본 merge 흐름이 아주 단순하고 **강제 푸시를 동반한 rebase는 종종 지옥**이며, 충돌이 있는 revert도 지옥이라 가끔은 revert보다 커밋 취소를 택한다고 적었다.
기본만 지키면 git이 오히려 단순하며 rebase는 역병처럼 피하고 merge 커밋은 전혀 신경 쓰지 않는다는 것이다.

이 논쟁 자체는 결론이 나지 않는다. 다만 이 글의 맥락에서 의미가 있다.

b212의 전략 — rebase를 피하고 merge만 쓰기 — 이 **이 글이 설명한 내용과 정확히 대응한다**.
merge는 base가 그래프에서 계산되고, rebase와 cherry-pick은 base가 지정된다.
전자는 예측 가능하고 후자는 이 글을 읽어야 예측 가능해진다.

즉 “기본만 쓰면 git은 단순하다”는 주장은 **3방향 병합의 base를 직접 다루지 않는 부분집합으로 자신을 제한한다**는 뜻이다.

## 체크리스트

- `merge.conflictStyle`이 `zdiff3`(또는 `diff3`)으로 설정되어 있는가? base 없이 충돌을 해결하고 있지 않은가
- `rerere.enabled`가 켜져 있는가? rebase에서 같은 충돌을 반복해 풀고 있지 않은가
- cherry-pick이 이상하게 동작할 때, **대상 커밋의 부모**가 base라는 점을 떠올렸는가? `git merge-base`의 결과와 혼동하지 않았는가
- 메일로 받은 패치에 `--3way`를 쓰려 한다면, 저장소에 해당 블롭이 있는가
- 같은 커밋 집합을 다른 순서로 통합하는 중이라면, 결과가 순서에 따라 달라질 수 있음을 알고 있는가
- 자기 팀의 git 교육 자료가 그래프만 그리고 있지 않은가

## 기억할 원칙

### 그래프를 안다고 동작을 예측할 수 있는 것은 아니다

arxanas의 지적이 이 글에서 가장 일반화할 만한 통찰이다.
거의 모든 git 자료가 DAG 수준에서 다루는데 **그래프 구조만으로는 git이 실제로 어떻게 행동할지 예측할 수 없다**는 것이다.

왜 그런가.

그래프는 **어떤 커밋이 어떤 커밋의 조상인가**를 말해 준다. 그것으로 알 수 있는 것은 도달 가능성이다.
그런데 충돌은 도달 가능성에서 나오지 않는다. **파일 내용의 어느 줄이 겹치는가**에서 나온다.

그래서 같은 그래프 모양에서도 충돌이 날 수도 안 날 수도 있고, 그것은 그림에 나타나지 않는다.

이 어긋남이 git 학습의 구조적 문제를 만든다.
배우기 쉬운 표상(그래프)과 필요한 표상(3방향 병합) 사이에 다리가 없으므로, 그래프를 완벽히 이해한 사람도 충돌 앞에서 막힌다.

일반화하면, 어떤 시스템을 그림으로 설명할 수 있다는 것과 **그 그림으로 동작을 예측할 수 있다는 것은 다르다**.
그림은 대체로 구조를 담고 동작은 내용에서 나오기 때문이다.

그리고 교육 자료는 그릴 수 있는 것 쪽으로 쏠린다. 그것이 만들기 쉽고 이해되었다는 느낌을 잘 주기 때문이다.
그래서 어떤 주제에 대한 자료가 많다는 사실이 **그 주제가 잘 가르쳐지고 있다는 뜻은 아니다**.

### 하나의 기법이 여러 명령을 설명하면 그 기법을 배우는 것이 남는 장사다

이 글의 구조가 그 자체로 논증이다.

cherry-pick, revert, rebase, merge, `git apply --3way`, `git am --3way`가 전부 같은 것 — 3방향 병합 — 의 변주다.
다른 점은 **v1과 base와 v2에 무엇을 넣는가**뿐이고, revert는 cherry-pick에서 둘을 뒤집은 것이며 그래서 같은 파일에 구현되어 있다.

저자가 마지막에 git UI에 불만이 많지만 **이것만큼은 불만이 아니라**고 적은 이유가 그것이다.
3방향 병합이 여러 다른 문제를 푸는 **하나의 통일된 방법**으로 보인다는 것이다.

여기서 배움의 전략이 나온다.

명령을 여섯 개 외우는 것과 기법을 하나 이해하는 것 중에서, 후자가 **새로운 상황에 전이된다**.
`git rebase --onto`가 처음 보는 형태여도 “v1, base, v2에 무엇이 들어가는가”를 물으면 답할 수 있다.

일반화하면, 도구를 배울 때 물어야 할 것은 “이 명령이 무엇을 하는가”가 아니라 **“몇 개의 기법이 이 명령들을 전부 설명하는가”**다.
그 수가 작을수록 그 도구는 배울 값어치가 있고, 그 기법을 찾아내는 데 쓴 시간이 명령을 외우는 시간보다 훨씬 오래 남는다.

이 글이 하는 일이 정확히 그 기법 하나를 찾아 이름 붙인 것이고, 저자가 붙인 이름이 **3방향 패치**다.

---

[^juped]: <https://news.ycombinator.com/item?id=38223096>

[^Amorymeltzer]: <https://news.ycombinator.com/item?id=38224147>

[^juped-apply]: <https://news.ycombinator.com/item?id=38223015>

[^chx]: <https://news.ycombinator.com/item?id=38223406>

[^coryrc]: <https://news.ycombinator.com/item?id=38223967>

[^crdrost]: <https://news.ycombinator.com/item?id=38223276>

[^oasisaimlessly]: <https://news.ycombinator.com/item?id=38224206>

[^andrewla]: <https://news.ycombinator.com/item?id=38225834>

[^xg15]: <https://news.ycombinator.com/item?id=38228863>

[^crdrost-assoc]: <https://news.ycombinator.com/item?id=38223405>

[^not2b]: <https://news.ycombinator.com/item?id=38223334>

[^loeg]: <https://news.ycombinator.com/item?id=38224255>

[^vvpan]: <https://news.ycombinator.com/item?id=38222996>

[^AlotOfReading]: <https://news.ycombinator.com/item?id=38223317>

[^b212]: <https://news.ycombinator.com/item?id=38230186>

[^arxanas]: <https://lobste.rs/s/j4ljoz/how_git_cherry_pick_revert_use_3_way_merge#c_gfkjmj>
