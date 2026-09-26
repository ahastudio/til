# Python 25줄로 만든 Jev: 로짓 몇 개를 확률로 바꾸면 Jev인가라는 패러디

원문: [Jev in 25 lines of Python - NobodyWho](https://www.nobodywho.ai/posts/jev-in-25-lines/)

HN 토론: <https://news.ycombinator.com/item?id=49812769> (674점, 210개 댓글)

GN 토론: <https://news.hada.io/topic?id=34167>

## 요약

로컬 추론 라이브러리를 만드는 NobodyWho의 Duarte O. Carmo가 2026년 9월 22일 “Python 25줄로 만든 Jev”를 올렸다.
글은 모두가 Jev 이야기를 하고 트위터가 Jev를 대형 언어 모델의 다음 전선이자 AI의 새 패러다임이라고 떠들지만 자신들은 그렇게 생각하지 않는다며, 그래서 25줄짜리 Jev를 보여 주겠다고 시작한다.

코드는 세 단계다.
먼저 `llama-cpp-python`으로 Hugging Face의 GGUF 모델 `Qwen3-0.6B-Q8_0.gguf`를 불러오고, 모든 위치의 로짓을 남기도록 `logits_all=True`를 켠다.
다음으로 “Legitimate”, “Spam”, “Phishing” 세 선택지에 A, B, C 라벨을 붙이고, 회사 밖 로그인 페이지에서 급여 담당자가 비밀번호를 묻는 이메일을 넣은 프롬프트를 만든 뒤, 추론 블록을 빈 채로 닫아 모델이 곧바로 답을 내게 한다.
마지막으로 마지막 위치의 로짓에서 A, B, C 토큰의 값만 꺼내 log-sum-exp로 정규화해 확률로 바꾼다.

```python
logits = model.scores[model.n_tokens - 1]
token_ids = [model.tokenize(text=label.encode(), add_bos=False)[0] for label in labels]
choice_logits = numpy.asarray([logits[token_id] for token_id in token_ids])
# 세 라벨 토큰의 로짓만 남기고 그 안에서 정규화한다
logprobs = choice_logits - numpy.logaddexp.reduce(choice_logits)
probabilities = numpy.exp(logprobs)
```

예시 이메일에 대한 결과는 Legitimate 0.031, Spam 0.084, Phishing 0.885다.
글은 “그게 Jev다”라고 선언한 뒤, 이것을 System One 의사결정 모델이라 부르지 않았고, API를 부르지 않았고, 합성 데이터를 만들지 않았고, 결정과 확률을 보정하려고 RLCD(Reinforcement Learning for Calibrated Decisions)로 모델을 학습시키지도 않았지만, 선택지가 있는 프롬프트를 받아 확률을 내놓으니 분류기이고, 빠르고, 로컬에서 돌며, 데이터를 어디에도 보내지 않는다고 말한다.
끝에는 이것이 패러디 글이라는 단서와 함께 더 완전한 공개 구현으로 OpenJev, openjev-sglang, DiffusionGemma 위의 OpenJev를 소개한다.

## 분석

### 패러디의 표적은 기술이 아니라 이름 붙이기다

글이 웃음을 노리는 지점은 Jev의 핵심 동작, 곧 선택지를 받아 확률을 돌려준다는 것이 오래된 기법으로도 흉내 낼 수 있다는 데 있다.
언어 모델의 다음 토큰 로짓에서 선택지 토큰만 골라 정규화하는 방법은 객관식 벤치마크를 평가할 때 오래 써 온 방식이다.
글은 거기에 “System One”, “RLCD”, “의사결정 모델” 같은 이름을 붙이지 않았을 뿐이라고 말한다.

[[jev]]가 정리한 TypeSafe의 주장, 곧 채팅이 아니라 결정을 위한 모델이라는 틀은 새 범주를 만드는 마케팅이기도 하다.
Hacker News에서 alun은 Jev가 왜 “System One” 서사를 만드는지 이해할 수 없다며, 사람은 분류 과제를 System One이 아니라 System Two로 하고, 오히려 생각 없이 논리대로 자동 실행되는 평범한 프로그램이 System One에 가깝다고 적었다.[^alun]
패러디는 이름이 기술보다 앞서 나가는 순간을 겨냥한다.

### 25줄이 보여 주는 것은 인터페이스이고, 빼먹은 것은 보정이다

이 코드는 Jev의 입출력 모양을 정확히 재현한다.
선택지 목록과 입력을 받아, 선택지마다 확률을 돌려준다.
[[structured-output]]이 짚었듯, Jev가 되살린 것이 새 모델이라기보다 구조화된 출력이라는 인터페이스라면, 그 인터페이스는 확실히 25줄로 흉내 낼 수 있다.

그러나 Jev가 스스로 내세우는 차별점은 인터페이스가 아니라 그 확률이 믿을 만하다는 것, 곧 보정이다.
[[architecture-unmasked]]가 정리했듯 보정은 0.8 확률이 붙은 사례 묶음의 약 80%가 실제로 그러한지를 묻는 성질이고, 한 예측이 맞았는지로는 판정할 수 없다.
글은 RLCD를 하지 않았다고 스스로 말하면서도, 그 결과 나온 확률이 보정됐는지는 재지 않는다.
Hacker News에서 sidclaw는 다음으로 보고 싶은 것은 가장 높은 선택지가 맞았는지가 아니라 돌려준 확률이 보정됐는지라며, 자신은 기본 모델과 지시 모델의 선택지 로짓 보정을 비교하고 Brier 손실과 교차 엔트로피로 미세 조정해 보는 실험을 했다고 적었다.[^sidclaw]

xg15는 이 이중 잣대를 꼬집었다.[^xg15]
Jev에 대해서는 결정과 확률이 “늘 옳지는 않다”고 흠잡으면서, 자기 모델에 대해서는 “숫자를 원하면 숫자를 준다”고만 말한다는 것이다.
패러디가 Jev의 약점으로 든 바로 그 지점에서, 25줄짜리 구현은 아무것도 보여 주지 않는다.

### 로짓을 직접 읽는 방법에는 잘 알려진 함정이 있다

Hacker News의 기술적 반응은 이 방법 자체의 약점에 모였다.
sigmoid10은 채팅 모델은 산문을 쓰도록 학습됐기 때문에, 선택지 토큰의 확률이 모델이 원래 하고 싶던 다른 말에 희석될 수 있어 로짓을 직접 읽는 것은 늘 찜찜하다고 적었다.[^sigmoid10]
그는 이 방식을 쓰려면 적어도 분명한 시스템 지시와 조심스럽게 쓴 답변의 시작 부분을 넣어 모델이 곧바로 딴 길로 새지 않게 하라고 권했다.
글이 추론 블록을 비운 채 닫은 것도 같은 의도로 읽힌다.

antirez는 LLM의 어텐션이 마스크되어 있기 때문에, 분석할 이메일 앞에 선택지를 두면 트랜스포머가 무엇을 찾아야 할지 미리 알고 그 과제에 맞는 상태를 더 많은 토큰에 걸쳐 만들 수 있다고 적었다.[^antirez]
뒤의 토큰까지 보는 BERT와 달리 앞만 보는 모델에서는 선택지의 위치가 성능을 바꾼다는 것이다.
그는 시스템 프롬프트에 예시를 몇 개 넣어 보정을 돕거나, 과제와 라벨을 한 번 더 반복하는 요령도 덧붙였다.
fzysingularity는 더 근본적인 차이를 짚었다.[^fzysingularity]
LLM이 학습한 것은 질문 뒤에 생각과 결정이 이어질 확률이고, Jev가 학습했을 것은 질문 바로 뒤 결정 토큰의 확률이라, 둘은 같은 분포가 아니라는 것이다.

## 비평

### 속도와 정확도를 비교하지 않고 “빠르다”고 말한다

글은 이 구현이 빠르다고 말하지만 무엇과 비교해 빠른지는 말하지 않는다.
Hacker News에서 onion2k는 무언가와 비교한다면 “빠르다”를 상대적으로 말해야 한다며, 이 Python이 Jev와 같은 시간에 결정을 낸다면 빠른 것이지만 Jev보다 100배 느리다면 빠르다고 부르면 안 된다고 적었다.[^onion2k]
no-name-here도 지연 시간과 연산량 비교가 없을 뿐 아니라, Jev와 비교한 오류율도, 앱이 늘 해석할 수 있는 형식으로 답하는지도 나오지 않는다고 지적했다.[^no-name-here]

패러디라는 형식이 이 빈자리를 덮는다.
글은 끝에서 패러디라고 밝히며 진지한 비교의 책임에서 빠져나가지만, 그 전까지는 “이것이 Jev”라는 진지한 주장을 한다.
jorisw는 진지한 주장을 하는 척하다가 마지막에 제품을 소개하고 패러디라고 말하는 구성이 콘텐츠 마케팅처럼 의심스럽다고 적었다.[^jorisw]
Qwen3-0.6B의 한 예시 하나로 “Jev다”라고 말하려면, 적어도 같은 과제 묶음에서 두 방식의 정확도와 지연 시간과 보정을 나란히 놓았어야 한다.

### “그걸로도 된다”는 논증은 제품이 해결한 나머지를 지운다

xigoi는 이 논증을 탱크에서 대포를 떼면 같은 일을 할 수 있으니 자동차는 쓸모없다고 말하는 것에 빗댔다.[^xigoi]
dhsysusbsjsi는 기술적 요령을 읽는 것은 좋지만, 이제 Jev를 만든 사람은 이것보다 더 잘한 작은 일 100가지가 모여 훨씬 나은 제품이 된다는 것을 설명하는 데 열 배의 노력을 들여야 할 것이라고 적었다.[^dhsysusbsjsi]
yipinwong도 이 데모가 80%까지는 데려다주지만 가장자리 사례, 인프라, API, 소통까지 갖춘 Jev 수준의 99%나 100%에 이르기는 어렵다고 봤다.[^yipinwong]

이 반론은 패러디가 무엇을 과소평가하는지 보여 준다.
0.6B 모델의 로짓을 읽는 코드는 한 번의 분류를 보여 주지만, 수천 개의 선택지 목록, 선택지 순서에 따른 흔들림, 선택지 경계를 위조하려는 입력, 대규모 동시 요청을 다루는 일은 보여 주지 않는다.
[[architecture-unmasked]]가 보고한 선택지 순서 민감도나 선택지 주입에 대한 저항 같은 성질은, 바로 이 25줄에서 빠진 부분이다.

### 이 방법은 가장 강한 모델에는 쓸 수 없다

로짓을 직접 읽으려면 모델의 내부 점수에 접근할 수 있어야 한다.
Hacker News에서 armcat은 로그 확률을 보는 방식이 로컬 모델에서는 되지만 프런티어 모델에서는 안 되며, GPT-4o 이후로 사실상 망가졌다고 적었다.[^armcat]
그는 신뢰도 추정과 루브릭 평가에서 같은 방법을 써 봤는데, 오히려 LLM에게 확신을 말하게 하는 편이 “실제 확신”과 더 잘 맞았다고 덧붙였다.
K0IN도 큰 제공사가 아직 로그 확률을 주던 시절 불확실한 토큰을 강조하는 VS Code 도구를 만들었지만, 채팅 모델은 사람이 읽을 답을 쓰려 하기 때문에 그 로그 확률이 그리 의미 있지 않았다고 전했다.[^K0IN]

그렇다면 25줄 Jev는 선택의 폭이 좁다.
로짓에 접근할 수 있는 작은 로컬 모델로는 쓸 수 있지만, 판단이 어려운 과제에 필요한 큰 모델로는 쓸 수 없다.
Jev가 파는 것이 “큰 모델의 지식으로 한 번에 보정된 결정”이라면, 이 구현은 그 조건 가운데 하나를 처음부터 포기한다.

## 인사이트

### 새 범주가 뜨면 “그건 원래 있던 것”이라는 반박이 곧 따라오고, 둘 다 반쯤 맞다

Hacker News에서 0123456789ABCDE는 DSPy라면 너무 사소해서 아무도 이름을 붙이지 않았을 일이라며, 이메일을 받아 세 선택지 가운데 하나를 고르는 예측기를 7줄로 보여 줬다.[^0123456789ABCDE]
bruhhhhhh는 Jev를 처음 듣는다며, 타입 안전성은 구조화된 출력으로 이미 풀 수 있고 분류는 고전적인 BERT 모델로도 더 빠르게 할 수 있으니, 결국 과제별 작은 모델을 파는 것이냐고 물었다.[^bruhhhhhh]
chpatrick도 아무 모델에 “내 선택은 a/b/c”로 출력을 제한하는 것과 무엇이 다르냐고 물었다.[^chpatrick]

이런 반응은 새 범주가 뜰 때마다 반복되는 패턴이다.
NoSQL이 떴을 때 “그건 원래 있던 키-값 저장소”라는 반박이, 서버리스가 떴을 때 “그건 원래 있던 CGI”라는 반박이 나왔다.
반박은 기술적 핵심에 대해서는 맞지만, 그 핵심을 쓰기 쉽게 포장하고 기본값을 정하고 운영을 떠맡는 일이 만드는 차이에 대해서는 틀린다.
Jev와 25줄 Jev의 차이도 그 사이 어딘가에 있고, 어느 쪽이 더 큰지는 보정과 운영의 실측이 정할 일이다.

### 복제판의 홍수는 원본의 평가 기준을 흐린다

iamflimflam1은 “작년에 Jev를 만들었다”거나 “어젯밤에 바이브 코딩한 Jev”라는 글이 우스울 만큼 많아졌고, Hacker News가 그것들을 액면 그대로 받아들이는 것이 특히 우습다고 적었다.[^iamflimflam1]
그는 며칠 전 그럴듯한 데모가 있었지만 자세히 보니 고를 선택지에 “best”라는 단어를 붙여 넣고, 그 단어를 알아보도록 미세 조정한 모델에 먹이고 있었다고 전했다.
이 저장소만 해도 [[laya]], [[kev]], [[jevlike]], [[semif]]가 모두 Jev를 재현하거나 앞섰다고 말한다.

복제판이 많아질수록 무엇이 같은 기능인지에 대한 기준이 흐려진다.
25줄 Jev와 원본은 같은 입출력 모양을 가지지만, 보정, 속도, 견고성에서 얼마나 다른지는 각자의 데모로는 드러나지 않는다.
모든 복제판에 같은 과제 묶음, 같은 보정 곡선, 같은 지연 측정을 요구하는 공개 평가가 없으면, 이 범주는 이름과 데모의 경쟁으로 남는다.

### 데이터를 밖으로 보내지 않는다는 장점은 정확도와 따로 팔린다

글이 끝에서 강조하는 가치는 속도나 정확도가 아니라 로컬이라는 것, 곧 데이터를 어디에도 보내지 않는다는 것이다.
이것은 NobodyWho라는 회사의 존재 이유이기도 하다.
피싱 판별처럼 민감한 이메일을 다루는 분류는, 조금 덜 정확하더라도 밖으로 보내지 않는 쪽이 나은 경우가 많다.

이 관점에서 보면 패러디의 진짜 메시지는 “Jev는 별것 아니다”가 아니라 “분류 정도는 작은 로컬 모델로도 할 수 있다”다.
cupofjoakim이 이것을 로컬 프롬프트 라우터, 곧 조회는 Haiku로, 추론은 Opus로, 구현은 Sonnet으로 보내는 장치의 출발점으로 쓸 수 있겠다고 적은 것[^cupofjoakim]도 같은 방향이다.
클라우드의 결정 모델과 로컬의 작은 분류기는 같은 시장에서 겨루는 것이 아니라, 정확도와 비용과 사생활 사이에서 서로 다른 점을 차지한다.

---

[^alun]: <https://news.ycombinator.com/item?id=49814660>

[^sidclaw]: <https://news.ycombinator.com/item?id=49836250>

[^xg15]: <https://news.ycombinator.com/item?id=49814572>

[^sigmoid10]: <https://news.ycombinator.com/item?id=49813052>

[^antirez]: <https://news.ycombinator.com/item?id=49813417>

[^fzysingularity]: <https://news.ycombinator.com/item?id=49818119>

[^onion2k]: <https://news.ycombinator.com/item?id=49813117>

[^no-name-here]: <https://news.ycombinator.com/item?id=49813031>

[^jorisw]: <https://news.ycombinator.com/item?id=49813768>

[^xigoi]: <https://news.ycombinator.com/item?id=49822610>

[^dhsysusbsjsi]: <https://news.ycombinator.com/item?id=49813007>

[^yipinwong]: <https://news.ycombinator.com/item?id=49821318>

[^armcat]: <https://news.ycombinator.com/item?id=49814490>

[^K0IN]: <https://news.ycombinator.com/item?id=49814200>

[^0123456789ABCDE]: <https://news.ycombinator.com/item?id=49818501>

[^bruhhhhhh]: <https://news.ycombinator.com/item?id=49815019>

[^chpatrick]: <https://news.ycombinator.com/item?id=49818896>

[^iamflimflam1]: <https://news.ycombinator.com/item?id=49822726>

[^cupofjoakim]: <https://news.ycombinator.com/item?id=49813257>
