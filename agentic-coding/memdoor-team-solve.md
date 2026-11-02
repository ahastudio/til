# Memdoor team-solve: 작은 모델 다섯 역할을 YAML 파일로 엮은 코딩 문제 풀이 워크플로

<https://github.com/guregodevo/memdoor/tree/main/examples/workflows/team-solve>

HN 토론: <https://news.ycombinator.com/item?id=50320995> (418점, 203개 댓글)

GN 토론: <https://news.hada.io/topic?id=36373>

## 소개

team-solve는 Memdoor 저장소의 예제 워크플로다.
README는 이것을 하나의 프로그래밍 문제에 작은 모델 다섯 개를 쓰는
방법이라고 소개한다.
계획자(planner), 아이디어를 내는 두 명, 풀이자(solver), 관리자(manager),
수리 담당(repair worker)이 각자 새 컨텍스트에서 시작하고,
서로 디스크의 파일로만 소통한다.
성공 여부는 샘플을 돌리는 스크립트가 정한다.
방법은 Lee(2026)의 GVS5H를 Memdoor 워크플로로 옮긴 것이며,
코드 없이 YAML 파일 여덟 개로 되어 있고 모델 이름은 적혀 있지 않다.

Memdoor 자체는 저장소 설명에서 단일 CLI 바이너리로 된 가벼운 코딩 및 자동화
에이전트이자 멀티 에이전트 하네스(harness)로, 로컬이나 SSH로 돌린다고 한다.
라이선스는 Apache-2.0이고 저장소는 2026년 10월 5일에 만들어졌으며,
이 글을 쓸 때 별은 221개였다.[^api]

## 결과

README는 같은 모델인 Qwen3.8-27B를 쓰는 원저자들의 하네스와 비교한다.
원저자들의 프롬프트, 반복 구조, 128K 응답 상한을 그대로 쓰고,
그들의 LiveCodeBench Hard 목록 첫 열 문제를 다섯 번씩 돌려 숨겨진 테스트
전체로 채점했다.
평균은 이 워크플로가 9.8/10, 원저자 하네스가 9.6,
Fable 5의 한 번 호출이 8.0이다.
50번의 실행은 중앙값 40분, 한 번에 0.39달러였고, 50번의 합계는 35.79달러다.

README는 이 결과가 보여 주지 않는 것도 적는다.
표본은 열 문제와 다섯 번이고 원저자는 100문제를 돌렸으므로,
9.8과 9.6은 오차 범위 안이며 주장은 원저자 하네스와 같은 수준이라는 데 그친다.
대회가 2025년 봄이어서 모델이 문제를 본 적이 있을 수 있고 어느 열에서도
배제하지 못한다.
Fable 5는 원저자 파일에서 가져온 한 번 호출 결과이고 이 하네스에서
돌리지 않았다.
반복 구조는 공개 샘플을 보고, 점수는 숨겨진 테스트로 매기며,
호스트는 로컬 머신이 아니라 OpenRouter다.

## 실행하기

README의 순서는 설치, 공급자 연결, 저장소 복제, 워크플로 복사, 실행이다.

```bash
curl -fsSL https://memdoor.ai/install.sh | bash
memdoor connect openrouter
git clone --depth 1 https://github.com/guregodevo/memdoor
mkdir -p ~/.memdoor/workflows
cp -r memdoor/examples/workflows/team-solve ~/.memdoor/workflows/
mkdir my-problem && cd my-problem
cp -r ../memdoor/examples/workflows/team-solve/sample/* .
memdoor workflow run team-solve --wait
```

자기 문제를 쓰려면 `task.md`와 짝이 되는 `tests/N.in`, `tests/N.out`을 두고,
프로그램은 `solution.py`로 표준 입력을 받아 샘플과 `diff`로 비교한다.
Python 3와 bash가 필요하다.
키가 없으면 `memdoor connect local`로 Ollama, llama.cpp, vLLM,
LM Studio를 쓸 수 있고, Ollama는 기본 4K가 아니라 32K 창이 필요하다고 한다.

## 동작 방식

흐름은 `plan`에서 두 아이디어 단계(`ideate-a`, `ideate-b`)가 병렬로 나가고,
`solve`, `test`, `review`, `repair`, `verify` 순으로 이어진다.
`plan`은 `task.md`를 읽어 `plan.md`와 `notes.md`를 쓴다.
두 아이디어 단계는 하나는 가장 직접적이고 증명 가능한 알고리즘,
다른 하나는 다른 계열의 알고리즘을 제안한다.
`test`와 `verify`는 모델이 아닌 명령이고,
`test`는 실행을 실패시키지 않으며 `verify`의 0이 아닌 종료 코드가
실행을 실패시킨다.

모든 에이전트 프롬프트는 “새 컨텍스트에서 파일을 읽고 대화에 기대지
말라”고 지시한다.
README는 논문이 이 장부 규율(ledger discipline)에 성능 향상을 돌린다고 적는다.
각 단계는 `steps/`의 YAML 파일 하나이고 `requires:`가 의존 관계를 정한다.

## 분석

### 이 저장소가 내세우는 것은 새 알고리즘이 아니라 재현이다

README는 반복해서 “원저자의 하네스와 같다”고 말한다.
NOTES.md는 요청 하나하나가 바이트 단위로 같음을 보였다고 적는다. 원저자의
`multiagent_solve`와 이 워크플로를 같은 스크립트 모델에 돌려 요청을 비교하는
테스트이며, 네 가지 경우가 모두 같았고 한 글자를 바꾸면 달라졌다고 한다.
온도(계획 0.3, 아이디어 0.4, 관리자와 작업자 0.2), `top_p` 0.95, `top_k` 20,
128K 상한, 최대 10라운드까지 같다.[^notes]

따라서 이 프로젝트의 기여는 방법 자체가 아니라,
방법을 코드 없이 YAML로 옮겼을 때 결과가 유지된다는 확인이다.
같은 NOTES.md는 그 과정에서 Memdoor 쪽을 네 가지 바꿔야 했다고 한다.
모델이 글을 쓰지 않았을 때 추론 내용으로 응답하는 것,
모델 줄의 `top_p`와 `top_k`, 상한에서 잘린 응답을 표시하는 `mark_cutoff`,
네 시간짜리 호출 시계다.[^notes]

### 실패 사례를 숨기지 않았다

NOTES.md는 잃은 문제 한 건을 설명한다.
5번째 실행의 abc399_e에서 1라운드의 프로그램은 맞았는데,
관리자가 기대 답이 틀린 반례를 지어냈고 팀이 그것에 맞춰 프로그램을 다시 썼다.
새 프로그램은 샘플을 통과했지만 샘플에는 그 경우가 없었다.[^notes]
다른 두 건에서는 숨겨진 테스트를 모두 통과하던 프로그램이 관리자가 끝났다고
말하지 않아 이후 라운드에서 덮어써졌다가 되돌아왔고,
이 둘이 가장 비싼 실행(3.44달러, 4.24달러)이었다.[^notes]
저자들은 둘 다 방법을 바꾸지 않고 고칠 수 있다고 쓰면서 고친 결과를 공개 수치에
넣지 않았다.

## 비평

### 제목의 비교는 자원이 다른 두 대상을 맞세운다

HN 제목은 Qwen3.8-27B 다섯 개 팀이 Fable 5를 이긴다고 말한다.
README의 표에서 Fable 5는 한 번 호출이고,
이 워크플로는 최대 10라운드를 도는 반복 구조다.
실행당 중앙값 40분과 0.39달러, 가장 긴 것은 4시간이다.
작은 모델이 큰 모델을 이긴 것이 아니라,
큰 모델 한 번 호출이 작은 모델의 긴 반복 구조에 졌다는 것이고,
같은 반복 구조를 큰 모델에 쓴 결과는 없다.
README는 같은 반복 구조를 Fable에 적용한 결과를 싣지 않는다.

IsTom은 같은 취지로, Astra, Fable, Opus가 쓰는 컴퓨팅이 실행 시간 1시간 대
24시간의 비율처럼 Qwen 27B의 24배쯤 되는지 물었다.[^IsTom]
이 질문에 답하려면 정답당 토큰이나 비용이 필요한데,
README는 이 워크플로의 비용만 제시하고 Fable 5 한 번 호출의 비용은
제시하지 않는다.

### 벤치마크가 오염되고 포화되었다는 반론이 남는다

vikramkr는 같은 방식의 글이 지난주에도 있었다며,
실제 에이전트 작업을 반영하지 않는 포화된 오염 벤치마크에서 오픈 모델이
프런티어와 맞먹는다고 보이게 하는 것은 인터넷의 관심을 얻기 쉬운 방법일 뿐이라고
비판했다.[^vikramkr]
README는 오염을 인정하되 배제하지 못했다고만 적고,
이 구조가 더 최근의 문제에서도 유지되는지는 시험하지 않았다.
저자 guregodevo는 같은 스레드에서 GVS5H를 Memdoor로 재현하는 것이 의도였다고
답했다.[^guregodevo-intent]
의도가 재현이라면 위 반론은 재현의 가치를 부정하는 것이 아니라 결과의 일반화를
문제 삼는 것이다.

### 표본이 작아 격차의 방향을 말하기 어렵다

README 스스로 열 문제와 다섯 번은 100문제 규모의 원저자 실험보다 작다고 적는다.
평균 9.8과 9.6의 차이는 한 문제의 한 번 실패로도 뒤집힌다.
저자는 HN에서 프롬프트와 온도를 조금 더 조정하면 10점을 얻을 수 있다고 믿는다고
답했다.[^guregodevo-reply]
그 조정이 다른 문제에서도 유지되는지는 이 저장소에 없다.

## 인사이트

### 하네스는 모델 크기와 호출 횟수를 서로 바꿔 쓰는 교환 관계다

이 결과를 읽는 가장 정직한 방식은 모델 하나의 능력과 모델이 쓰는 호출의 수가
서로 바꿀 수 있다는 것이다.
작은 모델에 계획, 아이디어, 풀이, 검토,
수리를 나누고 매 단계를 새 컨텍스트와 파일로 분리하면,
큰 모델 한 번의 호출이 하는 일을 시간과 호출로 대신한다.
guregodevo는 더 똑똑한 모델이 오면 개선은 토큰 사용량과 지연 시간에서 나올
것이라고 답했고, 이 구조가 가장 어려운 문제에서 100 token/s로 한 시간 넘게 걸릴
수 있다고도 덧붙였다.[^guregodevo-reply]

이 교환이 이득인지는 어느 쪽이 값싼가에 달려 있다.
HN에서 roenxi는 2비트 양자화(Bonsai 2)로 27B를 게이밍 머신에서 50 t/s로 돌리면
로컬에서도 Fable 5 수준의 코딩을 얻을 수 있다고 추정했다.[^roenxi]
SwellJoe는 2비트 양자화가 8비트나 4비트보다 눈에 띄게 못하고 다섯 개를 묶어도 이
수준은 어렵다고 반박했다.[^SwellJoe]
Aurornis도 직접 써 보니 실제 작업에는 쓸 수 없다고 했다.[^Aurornis]
호출 수를 늘려 품질을 사는 전략은 호출당 품질이 일정 수준 이상일 때만 성립한다.

### 컨텍스트를 매번 비우는 설계가 오류의 전파 경로를 파일로 바꾼다

모든 단계가 대화가 아니라 파일을 읽으므로,
한 단계의 오류는 파일에 남은 다음 단계의 입력이 된다.
NOTES.md의 실패 사례가 이를 보여 준다.
관리자가 틀린 반례를 `notes.md`에 쓰면 이후 단계는 그것을 사실로 받아들이고 맞는
프로그램을 고쳤다.
README가 말하는 장부 규율은 추적을 쉽게 하지만,
기록된 오류를 자동으로 걸러 주지는 않는다.

저자들이 제안한 수리(작은 입력에서 브루트포스로 관리자의 반례를 검증하고,
샘플을 통과한 마지막 프로그램을 보관하는 것)는 모두 이 경로를 끊는
장치다.[^notes]
공개 수치에는 들어 있지 않으므로 다음 버전이 같은 점수를 내는지가 이 설계의
실질적인 시험이다.

### 로컬 모델 경쟁력을 둘러싼 스레드 대부분은 이 글의 결과와 별개의 이야기다

이 스레드는 곧 로컬 모델의 미래, 공급자의 제한,
검열 제거 모델의 운명으로 흘렀다.
fedpost는 로컬 모델이 하이퍼스케일러와 경쟁력을 유지해야 한다고
적었다.[^fedpost]
metalspot은 모델이 더 클 필요 없이 도구 사용이 핵심이라고 주장했다.[^metalspot]
metalspot의 주장은 이 README의 구조와 맞닿아 있다.
모델은 고정되어 있고 파일, 테스트, 검증 같은 도구가 새 정보를 시스템에 넣어
준다는 주장이기 때문이다.
그러나 이것은 댓글의 주장이고, 이 저장소의 실험은 그 주장을 시험하지 않았다.

---

[^api]: GitHub, [guregodevo/memdoor repository](https://api.github.com/repos/guregodevo/memdoor)

[^notes]: GitHub, [team-solve: working notes](https://github.com/guregodevo/memdoor/blob/main/examples/workflows/team-solve/NOTES.md)

[^IsTom]: <https://news.ycombinator.com/item?id=50324392>

[^vikramkr]: <https://news.ycombinator.com/item?id=50322353>

[^guregodevo-intent]: <https://news.ycombinator.com/item?id=50321492>

[^guregodevo-reply]: <https://news.ycombinator.com/item?id=50321592>

[^fedpost]: <https://news.ycombinator.com/item?id=50321623>

[^roenxi]: <https://news.ycombinator.com/item?id=50321420>

[^SwellJoe]: <https://news.ycombinator.com/item?id=50321472>

[^Aurornis]: <https://news.ycombinator.com/item?id=50322593>

[^metalspot]: <https://news.ycombinator.com/item?id=50324539>
