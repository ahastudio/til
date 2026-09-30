# MicroLLM Lab: 브라우저 탭에서 1억 파라미터급 LLM을 돌리고 재 보는 실험실

<https://stateofutopia.com/experiments/microllmlab/>

<https://github.com/robss2020/microllm-lab>

HN 토론: <https://news.ycombinator.com/item?id=49882781> (276점, 113개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/1gy0zx/microllm_lab_tiny_llms_q4_your_browser> (1점, 3개 댓글)

GN 토론: <https://news.hada.io/topic?id=34468>

## 소개

MicroLLM Lab은 2,600만에서 3억 6,000만 파라미터 사이의 작은 언어 모델을 4비트로 양자화해 브라우저의 WebGPU로 돌리는 웹 페이지다.
API 키도, Python도, CUDA 설치도 필요 없고, 가중치는 그 사이트 출처의 IndexedDB에 저장된다.
State of Utopia 사이트의 실험 페이지로 공개되었고, 저장소는 2026년 9월 20일에 만들어졌다.
HN에는 제작자 logicallee가 브라우저에서 작은 LLM 7개를 써 보라는 제목으로 올렸다.

README는 첫머리에서 클라우드 모델이 더 낫다고 인정하고, 그게 요점이 아니라고 말한다.
프롬프트가 기기를 떠나지 않고, 첫 토큰까지 네트워크 왕복이 없고, 다운로드 뒤에는 비용이 0이며, 작은 모델이 틀리는 모습을 채팅 화면 뒤에 숨기지 않고 측정한다는 것이 존재 이유다.
온디바이스 기능을 출시하려는 사람이 사용자와 같은 브라우저에서 품질과 속도의 교환을 직접 느껴 보라는 것이다.

페이지는 채팅, 벤치마크, 비교와 인증서, 사용자 정의 평가의 네 탭으로 되어 있다.
벤치마크는 정규식과 정확한 토큰으로 판정하는 객관식 검사이고, 페이지는 135M 모델이 실패해도 되며 그 실패가 곧 측정값이라고 적어 둔다.
사용자 정의 평가 탭에서는 JavaScript로 검사를 쓰면 그 출처에서 `eval()`한 뒤 모델 출력에 적용한다.

## 모델

README 표에는 여덟 개의 체크포인트가 있다.

| 모델                  | 파라미터 | Q4 크기 | 라이선스   | 만든 곳                           |
| --------------------- | -------- | ------- | ---------- | --------------------------------- |
| PetitGPT research-v1  | 124.6M   | 74 MB   | Apache-2.0 | yangqi0                           |
| SmolLM2 135M Instruct | 134.5M   | 80 MB   | Apache-2.0 | Hugging Face Smol Models Research |
| SmolLM 135M Instruct  | 134.5M   | 80 MB   | Apache-2.0 | Hugging Face Smol Models Research |
| L20-Edu 135M          | 134.5M   | 80 MB   | Apache-2.0 | AliceYin                          |
| SmolLM2 360M Instruct | 362M     | 216 MB  | Apache-2.0 | Hugging Face Smol Models Research |
| MiniMind2 104M        | 104M     | 62 MB   | Apache-2.0 | jingyaogong                       |
| MiniMind2 Small 26M   | 26M      | 15 MB   | Apache-2.0 | jingyaogong                       |
| GPT-2 124M            | 124M     | 77 MB   | MIT        | OpenAI                            |

이 실험실의 출발점은 PetitGPT다.
yangqi0이 RTX 4090 한 장으로 약 130억 토큰을 사전 학습한 124.6M Llama 스타일 디코더이고, RMSNorm, 9/3 GQA, RoPE, SwiGLU, 묶인 임베딩을 쓴다.
README는 이 저장소가 그 아키텍처와 체크포인트의 WebGPU 이식이자 Q4 패커이자 다중 모델 하네스일 뿐, 원작을 대체하지 않는다고 거듭 밝힌다.

나머지 모델은 비교를 위해 골랐다.
SmolLM2 135M은 PetitGPT와 같은 30×576 GQA 형태라 공정한 속도 대 정확도 비교가 되고, 약 2조 토큰으로 사전 학습했다.
2024년의 1세대 SmolLM은 약 6,000억 토큰이라 1년 사이 데이터와 레시피가 무엇을 바꿨는지 보여 준다.
L20-Edu는 NVIDIA L20 한 장과 약 130억 토큰으로 만든, 같은 형태의 적은 예산 버전이다.
MiniMind2는 중국어 학습자를 위한 교육용 프로젝트라 영어보다 중국어에 강하다.
GPT-2 124M은 채팅 튜닝이 없는 완성 모델이라 탐욕 디코딩에서 자주 반복하는데, README는 그것이 디코더 버그가 아니라 체크포인트의 성질이라고 적는다.

README가 공개한 Apple M4 Safari 측정값은 다음과 같다.

| 항목           | PetitGPT             | SmolLM2 135M Instruct |
| -------------- | -------------------- | --------------------- |
| 짧은 인사 응답 | 87 ms, 115 tok/s     | 227 ms, 66 tok/s      |
| 객관식 검사    | 원래 짧은 세트 10/14 | 확장 세트 14/20       |
| 20개 검사 소요 | 약 1.5초             | 약 6초                |

SmolLM2는 어휘가 크고 ChatML 접두사가 붙어 느리지만, 작은 모델도 통과할 만한 쉬운 검사에서 눈에 띄게 정확하다.
README는 이 비교를 보여 주는 것이 이 실험실의 존재 이유라고 말한다.

## 실행하기

`file://`로 `index.html`을 열면 모듈과 워커와 `fetch`가 동작하지 않으므로 로컬 서버가 필요하다.

```bash
git clone https://github.com/robss2020/microllm-lab
cd microllm-lab
python3 -m http.server
# 브라우저에서 http://127.0.0.1:8000/ 을 연다
```

모델은 카드의 다운로드 버튼을 누르거나 생성을 시작할 때 받아지고, IndexedDB 사본은 Discard로 지운다.
다른 Llama 스타일 Hugging Face 체크포인트는 변환 스크립트로 Q4로 바꾼 뒤 `models/catalog.json`에 한 줄을 더한다.

```bash
python3 -m venv .venv && .venv/bin/pip install torch transformers safetensors
.venv/bin/python tools/convert_hf_to_pgw.py HuggingFaceTB/SmolLM2-135M-Instruct models/my-model
```

GPT-2 형태는 `tools/convert_gpt2_to_pgw.py`를 쓴다.
컨텍스트는 노트북 GPU에 KV 캐시가 들어가도록 2048 토큰으로 제한되고, 디코딩은 탐욕 방식만 지원한다.
WebGPU가 없으면 WASM으로, 그다음 순수 JS로 내려간다.

## 분석

### 이 실험실의 제품은 모델이 아니라 실패의 측정이다

MicroLLM Lab은 어떤 모델도 새로 학습하지 않았다.
기여는 세 가지, 즉 WebGPU 디코더, Q4 패커, 같은 조건에서 여러 모델을 재는 하네스다.
그리고 그 하네스의 목적은 작은 모델이 잘한다는 것을 보여 주는 게 아니라 얼마나 못하는지를 같은 잣대로 보여 주는 것이다.

HN 반응은 이 의도를 정확히 확인해 주었다.
PetitGPT는 2+2를 묻자 양변에 2를 더해야 한다며 2+2=4+2라고 답했고[^tolugenius], 고양이가 동물이냐는 질문에 고양이는 동물이 아니며 온혈 동물이라고 했다[^touchme].
SmolLM2 360M은 캘리포니아 인구를 1억 5,300만 명이라고 했다가 3억 2,500만 명이라고 했다[^not2b].
Anthropic 모델과 능력을 비교해 달라는 질문에는 둘 다 교활한 광대에 관한 이야기라고 답했다[^mgaunard].
이런 답들은 조롱거리로 돌았지만, README가 약속한 바로 그 측정 결과이기도 하다.

### 같은 형태, 다른 예산이라는 비교 설계

모델 선택에는 실험 설계가 들어 있다.
PetitGPT, SmolLM2 135M, SmolLM 135M, L20-Edu는 모두 비슷한 135M급 Llama 형태다.
차이는 사전 학습 토큰 수, 즉 약 130억, 6,000억, 2조라는 예산이다.

아키텍처를 고정하고 예산만 바꾸면, 같은 크기에서 데이터가 무엇을 사 주는지 브라우저에서 직접 볼 수 있다.
README의 측정표가 그 결과를 요약한다.
PetitGPT가 더 빠르지만, 2조 토큰의 SmolLM2가 쉬운 검사에서 더 정확하다.
beschizza가 JavaScript 키 입력 질문에 제대로 답한 모델은 Smol뿐이었다고 한 것도 같은 방향이다[^beschizza].

### 교육용 체크포인트가 설명의 무게를 진다

PetitGPT, L20-Edu, MiniMind2는 모두 소비자용 GPU 한 장으로 누군가 직접 학습한 모델이다.
README는 L20-Edu를 한 GPU로 무엇을 할 수 있는지 감사 가능한 체크포인트라고 소개한다.
이 실험실은 대형 연구소의 모델과 개인이 만든 모델을 같은 표에 두고, 둘 다 Apache-2.0이라는 사실을 강조한다.

이 구성은 작은 모델의 가치를 성능이 아니라 투명성에서 찾는 흐름과 맞닿아 있다.
Karpathy의 nanoGPT가 GPT-2 124M을 재현 가능한 교재로 만든 것처럼, 이 실험실은 그 교재들을 브라우저에서 비교 가능한 표본으로 만든다.

## 비평

### 페이지가 README의 정직함을 지키지 못한다

README는 작은 모델이 산수에 실패하고 사실을 지어낸다고 솔직하게 말한다.
그런데 페이지의 선택 읽을거리는 Q4가 거의 손실 없는 생성 품질을 준다고 하고, 10ms 미만의 첫 토큰 지연으로 즉각적인 자동 완성과 실시간 에이전트를 약속하고, 질의를 분류하고 스팸을 걸러 비싼 클라우드 LLM이 필요한지 판단하는 계층이라고 소개한다.
README의 측정값에서 짧은 인사 하나에 87ms에서 227ms가 걸렸으니, 10ms라는 수치는 실험실 자신의 측정과도 맞지 않는다.

HN에서 demibabs는 이 설명을 대부분 쓸모없고 AI가 만든 정보라고 부르며, 인터페이스에 닿기까지 한 페이지 넘게 스크롤해야 한다고 지적했다[^demibabs].
amelius는 이 모델로 무엇을 할 수 있고 한계가 무엇인지 예시를 보여 달라고 했다[^amelius].
제작자는 12시간 동안 첫 화면 3~4위에 머물며 고유 IP 3만 6,000개에서 30만 건 넘는 요청과 600GB 모델 다운로드가 있었다며 형식이 통했다고 보고, 설명은 선택 읽을거리로 표시하고 맨 위에 요약을 더하는 선에서 고쳤다[^logicallee-traffic].
트래픽은 호기심의 증거일 수는 있어도 설명이 정확하다는 증거는 아니다.
실제로 바뀌어야 했던 것은 설명의 분량보다, README의 측정과 맞지 않는 주장이었다.

### 쓸모의 질문에 답할 도구가 채팅 화면 뒤에 있다

botanrice는 아침 식사 레시피를 물었다가 파르메산 치즈 8컵 같은 조합을 받고, 이 모델들이 포함된 검사조차 꾸준히 통과하지 못하는데 무엇에 쓰느냐고 물었다[^botanrice].
Lobste.rs에서도 WilhelmVonWeiner가 작은 언어 모델이 지금 쓸모가 있느냐고 물었고, 제출자 dimonomid는 실용 목적이 아니라 재미로 보는 것이라고 답했다[^WilhelmVonWeiner][^dimonomid].
HN의 smokel은 SLM의 쓸모는 지식이 아니라 감정 분석, 텍스트 분류, 개체 추출이라고 답했다[^smokel].

문제는 실험실의 첫 화면이 채팅이라는 점이다.
채팅은 작은 모델이 가장 못하는 일, 즉 지식과 추론을 요구하는 자유 질문으로 사용자를 이끈다.
작은 모델이 잘하는 분류나 추출을 보여 줄 수 있는 도구는 사용자 정의 평가 탭에 JavaScript로 검사를 짜야 하는 형태로 숨어 있다.
측정이 목적이라면, 분류나 추출 같은 과제의 예제 세트가 기본으로 있어야 사용자가 모델의 쓸모를 판단할 수 있다.

### 영어 전용 검사가 다국어 모델을 제대로 재지 못한다

README는 MiniMind2가 중국어에 강하다고 소개하면서도, 공개한 객관식 검사는 영어 질문이다.
Surac은 독일어 질문은 그대로 되풀이될 뿐이라고 보고했다[^Surac].
중국어에 강한 모델을 영어 검사로 재면, 이 실험실이 보여 주는 것은 모델의 약점이 아니라 검사 설계의 약점이다.
언어별 검사 세트가 없으면 비교표는 영어 사용자의 기대를 기준으로 한 순위표가 된다.

## 인사이트

### 브라우저 WebGPU의 파편화가 온디바이스 AI의 실제 배포 장벽이다

HN에서 여러 사람이 Linux의 Firefox에서 `GPUShaderStage is not defined` 오류로 페이지가 뜨지 않는다고 보고했고[^langurmonkey], 다른 사용자는 Linux Firefox가 WebGPU를 기본으로 켜지 않기 때문이라고 설명했다[^Doohickey-d].
제작자는 WASM 대체 경로로 돌도록 고쳤지만 더 느리다고 답했다[^logicallee-firefox].
macOS 자체가 멈췄다는 보고도 있었다[^gslepak].

이 반응들은 온디바이스 AI의 약속과 현실 사이의 간격을 보여 준다.
프라이버시와 비용 0은 모델이 모든 사용자의 기기에서 같은 속도로 돈다는 전제 위에 있지만, 실제로는 브라우저와 OS와 GPU 조합마다 다른 경로가 선택된다.
서버 추론에서는 한 번 해결하면 끝나는 호환성 문제가, 클라이언트 추론에서는 사용자 수만큼의 테스트 매트릭스가 된다.
온디바이스 기능을 출시하려는 팀에게 이 실험실의 진짜 교훈은 모델 품질보다 이 매트릭스의 크기일 수 있다.

### 무료 추론은 대역폭 비용으로 옮겨 갈 뿐이다

README는 다운로드 뒤에는 비용이 0이라고 말한다.
하지만 제작자의 보고를 보면 12시간 동안 600GB의 가중치가 나갔고, 첫 모델 다운로드 8,500건 중 5,500건은 동시 접속으로 느려져 끝까지 기다리지 않았다[^logicallee-traffic].
제작자는 서버가 1기가비트 무제한 회선에 있다고 밝혔다[^logicallee-bandwidth].

클라이언트 추론은 GPU 비용을 사용자에게 넘기지만, 그 대신 모델 배포라는 새 비용을 만든다.
80MB짜리 모델도 수만 명이 받으면 CDN 비용이 되고, 모델을 바꿀 때마다 다시 나간다.
kenzic이 제안한 Web Models API처럼 브라우저가 모델을 공유 캐시로 관리하는 표준이 나오면 이 비용이 사이트마다 반복되지 않는다[^kenzic].
제작자가 그 제안에 대해 모델을 어디서 받아 오느냐고 되물은 것은 정확히 이 지점이다[^logicallee-webmodels].
온디바이스 AI의 경제성은 추론이 아니라 배포에서 결정된다.

### 작은 모델의 실패가 큰 모델의 실패를 이해하는 교재가 된다

HN에서 dotancohen은 LLM이 만드는 것은 사실적으로 옳은 진술이 아니라 의미적으로 옳은 문장이라는 점을 벌써 잊었느냐고 했다[^dotancohen].
작은 모델의 답은 이 명제를 극단적으로 보여 준다.
문법은 맞고 어조는 자신 있지만 내용은 무작위에 가깝다.

대형 모델에서는 같은 현상이 훨씬 드물고 그럴듯해서 알아채기 어렵다.
그래서 작은 모델의 실패를 직접 보는 경험은, 큰 모델의 환각이 어떤 모양으로 나타나는지 감각을 기르는 교재가 된다.
tcgv가 이 경험을 옛날 프롬프트 엔지니어링 시절 같다고 한 것도 이 때문이다[^tcgv].
Lobste.rs의 k749gtnc9l3w는 이 크기에서도 Mozilla의 온디바이스 번역 모델은 쓸모가 있다며, 그것은 완성 모델이 아니라 seq2seq 모델이라고 구분했다[^k749gtnc9l3w].
같은 파라미터 수라도 과제를 좁히고 구조를 맞추면 쓸모가 생긴다는 것, 그 대조가 이 실험실이 보여 주지 않은 절반이다.

---

[^tolugenius]: <https://news.ycombinator.com/item?id=49883564>

[^touchme]: <https://news.ycombinator.com/item?id=49889582>

[^not2b]: <https://news.ycombinator.com/item?id=49887067>

[^mgaunard]: <https://news.ycombinator.com/item?id=49885051>

[^beschizza]: <https://news.ycombinator.com/item?id=49891699>

[^demibabs]: <https://news.ycombinator.com/item?id=49883842>

[^amelius]: <https://news.ycombinator.com/item?id=49890245>

[^logicallee-traffic]: <https://news.ycombinator.com/item?id=49897068>

[^botanrice]: <https://news.ycombinator.com/item?id=49897203>

[^WilhelmVonWeiner]: <https://lobste.rs/s/1gy0zx/microllm_lab_tiny_llms_q4_your_browser#c_gimbhh>

[^dimonomid]: <https://lobste.rs/s/1gy0zx/microllm_lab_tiny_llms_q4_your_browser#c_n7ivcg>

[^smokel]: <https://news.ycombinator.com/item?id=49883612>

[^Surac]: <https://news.ycombinator.com/item?id=49895903>

[^langurmonkey]: <https://news.ycombinator.com/item?id=49888934>

[^Doohickey-d]: <https://news.ycombinator.com/item?id=49889609>

[^logicallee-firefox]: <https://news.ycombinator.com/item?id=49897147>

[^gslepak]: <https://news.ycombinator.com/item?id=49888119>

[^logicallee-bandwidth]: <https://news.ycombinator.com/item?id=49884892>

[^kenzic]: <https://news.ycombinator.com/item?id=49884085>

[^logicallee-webmodels]: <https://news.ycombinator.com/item?id=49884195>

[^dotancohen]: <https://news.ycombinator.com/item?id=49884506>

[^tcgv]: <https://news.ycombinator.com/item?id=49892421>

[^k749gtnc9l3w]: <https://lobste.rs/s/1gy0zx/microllm_lab_tiny_llms_q4_your_browser#c_ewnhxg>
