# Ollaya: Ollama처럼 결정 모델을 내려받아 로컬에서 돌리는 도구

<https://ollaya.dev/>

<https://github.com/ollaya-dev/ollaya>

HN 토론: <https://news.ycombinator.com/item?id=49848269> (404점, 111개 댓글)

GN 토론: <https://news.hada.io/topic?id=34288>

## 소개

Ollaya는 열린 결정 모델(decision model)을 내 컴퓨터에 내려받아 서빙하는 도구다.
홈페이지는 “결정 모델을 로컬에서 돌려라”라며, 텍스트나 JSON에 타입이 있는 질문을 던지면 보정된(calibrated) 답을 밀리초 안에 돌려받을 수 있고, 사적이며 오픈소스이고 내 하드웨어에서 돈다고 소개한다.
README의 한 줄 요약은 “Ollama가 LLM을 돌리는 방식으로 결정 모델을 돌린다”이다.
저장소는 2026년 9월 23일에 만들어졌고, Rust로 작성됐으며, Apache-2.0 라이선스다.

결정 모델은 메시지, 이메일, 티켓 같은 상태(state)와 `choice`, `score`, `noul` 같은 타입이 있는 질문을 읽고, 한 번의 순전파로 보정된 확률을 돌려준다.
텍스트는 생성하지 않는다.
Ollaya는 이 모델들을 이름으로 내려받아 로컬 데몬에서 서빙하고, TypeSafe의 `/v1/systemone` 형식을 그대로 말하므로 기존 Jev 클라이언트는 환경 변수 하나만 바꾸면 동작한다.

## 사용법

```bash
curl -fsSL https://ollaya.dev/install.sh | sh
ollaya run laya --preset triage "I was charged twice for my subscription this month and want a refund."
```

명령 체계는 Ollama를 그대로 따른다.
`ollaya serve`가 데몬을 띄우고, `run`, `pull`, `list`, `ps`, `show`, `rm`, `cp`, `stop`, `create`가 Ollama에서처럼 동작하며, 데몬이 없으면 CLI가 띄운다.
TypeSafe SDK를 로컬 서버로 돌리려면 다음처럼 가리키면 된다.

```bash
export TYPESAFE_BASE_URL=http://localhost:11435
export TYPESAFE_API_KEY=local        # 아무 값이나 된다
export TYPESAFE_DEFAULT_MODEL=laya
```

질문 묶음을 모델에 구워 넣는 Modelfile도 있다.

```text
FROM laya
QUESTIONS ./triage.json
PARAMETER precision fp32
```

`ollaya create triage -f Modelfile`로 만들고 `ollaya run triage "…"`로 쓴다.
`ollaya mcp`는 Claude Code, Claude Desktop, Cursor 같은 MCP 클라이언트에 모델을 제공하고, 에이전트에게 언제 어떻게 쓸지 가르치는 `ollaya-decisions` 스킬도 함께 배포한다.

## 모델

| 모델         | 설명                                                                                |
| ------------ | ----------------------------------------------------------------------------------- |
| `laya`       | Convai Innovations의 결정 모델, 영어와 100개 이상 언어, 322M·421M, 언어별로 라우팅  |
| `decider`    | Mapika의 Qwen3.5 기반 디코더, 0.75B·1.9B, 선택지 글자 로짓으로 답을 읽음, 가장 정확 |
| `nli`        | Moritz Laurer의 제로샷 분류기, 선택지를 가설로 바꿔 함의 점수를 매김                |
| `gliclass`   | Knowledgator의 지시 따르기 제로샷 분류기, 한 번에 모든 선택지를 점수화              |
| `qwen3guard` | Qwen 팀의 안전 가드, 안전·논쟁적·위험 판정과 위험 범주, 119개 언어                  |
| `kev`        | Jared Palmer의 결정 모델, Qwen3.5 위 LoRA와 포인터 헤드                             |
| `von`        | Victor Hugo Panisa의 ModernBERT-large 기반 결정 모델, 8,192 토큰 문맥               |

가중치는 원저자의 Hugging Face 저장소에서 커밋을 고정하고 sha256으로 검증해 가져오며, Ollaya는 가중치를 다시 호스팅하지 않고 약 3MB짜리 ONNX 그래프만 배포한다.
fp32 내보내기는 체크포인트마다 2,383개 질문에서 PyTorch 기준과 100% 같은 결정을 낸다고 한다.
실행은 ONNX Runtime으로 CPU나 NVIDIA GPU에서 하고, 서버는 기본적으로 `127.0.0.1`에서만 듣는다.
NVIDIA GPU는 드라이버 R580 이상과 CUDA 13이 필요하고, Apple, AMD, Intel GPU에서는 CPU로 돈다.

## 속도

홈페이지는 RTX 4090에서 질문 다섯 개짜리 요청을 HTTP API로 끝까지 처리하는 데 `laya`가 약 8~10ms 걸린다고 밝힌다.
중앙값 지연은 `laya:multilingual` 8.1ms, `laya:en` 9.6ms, `gliclass` 14.7ms, `nli` 20.4ms, `decider:0.8b` 155ms, `decider:2b` 190ms이고, 외부 벤치마크의 TypeSafe Jev 호스팅 API는 네트워크를 포함해 236~276ms다.
홈페이지 스스로 측정 조건이 다르니 자릿수 비교로 읽으라고 단서를 단다.

## 분석

### 이 도구의 핵심은 모델이 아니라 인터페이스의 복제다

Ollaya가 하는 일은 새 모델을 만드는 것이 아니다.
이미 있는 여러 열린 결정 모델을 한 가지 명령 체계와 한 가지 API 뒤에 모으고, 그 API를 TypeSafe의 형식과 똑같이 맞춘다.
사용자는 Jev를 부르던 코드를 그대로 두고 주소만 바꾸면 된다.

Hacker News에서 개발자 cobanov는 Ollama가 결정 모델을 지원해도 괜찮다며, Ollaya는 Jev와 같은 API를 쓰므로 코드가 어느 쪽에도 묶이지 않는다고 답했다.[^cobanov-api]
이 답은 도구의 전략을 요약한다.
Ollaya의 가치는 자기 자신에게 사용자를 묶는 것이 아니라, 사용자가 TypeSafe에서 벗어날 수 있게 하는 것이다.
이 저장소의 [[jev]]가 다룬 TypeSafe의 System One 모델이 한 회사의 API였다면, Ollaya는 그 API 형식을 누구나 구현할 수 있는 공용 규격으로 만든다.

### 속도는 분명하지만 품질에는 단서가 붙는다

홈페이지의 속도 비교는 인상적이다.
그러나 가장 빠른 `laya`와 가장 정확한 `decider` 사이에 스무 배 가까운 지연 차이가 있다는 것도 같은 표에 나온다.
Hacker News에서 george_max는 자기 경험으로는 Laya가 Jev보다 훨씬 못하며, 덜 확신하고 복잡한 질문에서 자주 틀린 결정을 내린다고 적었다.[^george_max]

cobanov는 그 지적이 맞다고 인정했다.[^cobanov-quality]
Laya는 작은 모델이라 빠르지만 그것이 대가이고, Jev에 가까운 열린 모델들은 훨씬 크며, 그것들을 돌리는 것이 다음 작업이라는 것이다.
cjonas는 자기 용도에서 Laya는 근처에도 못 갔지만 decider는 Jev만큼 좋았다고 적었다.[^cjonas]
결국 Ollaya의 속도 우위는 가장 작은 모델에서 나오고, Jev와 견줄 품질은 수백 밀리초가 드는 디코더 모델에서 나온다.

## 비평

### 홈페이지의 첫 예시가 “결정”이 아니라 분류다

Hacker News에서 ranyume은 결정 모델을 로컬에서 돌리라면서 예시는 텍스트 분류라고 짚었고,[^ranyume] cobanov는 그 예시가 사실상 분류라며 더 실제 결정처럼 보이는 것으로 바꾸겠다고 답했다.[^cobanov-example]
hbrn은 더 나아가, “결정 모델”은 분류기의 마케팅 용어이고 “System One 모델”은 추론하지 않는 작은 LLM, `noul`은 불리언, 확신도는 확률의 함수일 뿐이라고 적었다.[^hbrn]

이 비판은 Ollaya만이 아니라 Jev 계열 전체를 향한다.
그러나 Ollaya가 그 용어를 그대로 가져온 이상, 비판도 함께 가져온다.
홈페이지 첫 화면의 에이전트 예시, 곧 README 오타 수정 요청에 `git push --force`가 붙은 명령을 막을지 판단하는 장면은 그 비판에 대한 반박처럼 보이지만, 그 판단의 확률이 0.53이라는 점은 이런 모델을 안전장치로 쓸 때 어떤 문턱이 필요한지를 오히려 드러낸다.

### Ollama의 이름과 외형을 빌린 것은 기대와 혼동을 함께 만든다

Ollaya는 이름, 명령 체계, 문서 구조까지 Ollama를 따른다.
Hacker News에서 carimura는 Ollama 사람들이 만든 것인지, 아니면 일부러 모든 것을 흉내 낸 것인지 헷갈린다며 침해 소지가 있어 보인다고 적었고,[^carimura] thih9는 FAQ가 Ollama와 무관한 독립 프로젝트라고 밝힌다고 알렸다.[^thih9]

익숙한 외형은 사용자를 빠르게 끌어들이지만, 동시에 Ollama 수준의 성숙도를 기대하게 만든다.
emmettbt와 george_max는 Ollama가 언제든 결정 모델을 지원할 수 있다는 점이 이 도구의 존재 이유를 약하게 만든다고 봤다.[^emmettbt][^george_max-ollama]
Ollama를 흉내 낸 도구가 가장 크게 기대는 것은 Ollama가 아직 그 일을 하지 않았다는 사실이다.

## 인사이트

### 결정 모델 시장은 모델보다 규격이 먼저 굳고 있다

TypeSafe가 Jev를 내놓은 뒤 짧은 기간에 Jevlike, Laya, Kev, CLM([[clm]]) 같은 열린 모델과 Ollaya 같은 서빙 도구가 나왔다.
이들 중 여럿이 TypeSafe의 `/v1/systemone` 형식을 그대로 따른다.
Hacker News에서 verdverm은 GoModel 게이트웨이가 이미 Jev 형식의 엔드포인트를 지원하고 다음 vLLM 릴리스에도 들어갈 것이라고 적었다.[^verdverm]

이 흐름은 OpenAI의 채팅 API 형식이 사실상 LLM 서빙의 공용 규격이 된 과정과 닮았다.
처음 시장을 연 회사의 API가 규격이 되고, 그 규격을 따르는 대안들이 늘면서 원래 회사는 규격의 주인이 아니라 여러 구현 중 하나가 된다.
TypeSafe가 차별화할 수 있는 곳은 API가 아니라, 그 API 뒤의 모델 품질과 학습 데이터다.

### 복제가 2주면 되는 시대에 혁신자의 몫은 어디에 남는가

Hacker News에서 pradn은 AI 스타트업의 혁신을 오픈소스가 2주 만에 복제할 수 있다면 무슨 의미냐며, 소비자 잉여는 모두에게 좋지만 그 일부는 혁신자에게 돌아가야 바람직하다고 적었다.[^pradn]
janalsncm은 학습 레시피와 학습 데이터셋은 1~2주 만에 쉽게 복제할 수 없을 것이라고 답했고,[^janalsncm] redox99는 이것이 사실 사소한 일이며 ChatGPT 이후 사람들이 머신러닝을 어떻게 하는지 잊은 것 같다고 반박했다.[^redox99]
fooker는 반대로 Jev의 혁신이 사소하지 않으며, 2019년의 MNIST 분류기와는 다르고, 이것이 제품이 될 수 있다는 것을 Jev가 증명한 것이 중요하다고 적었다.[^fooker]

이 논쟁은 결정 모델의 가치가 어디에 있는지에 대한 질문이다.
형식과 서빙 도구는 2주면 복제되고, 작은 모델도 금방 나오지만, cobanov 스스로 인정했듯 Jev 수준의 품질에는 아직 큰 모델이 필요하다.[^cobanov-quality]
Fordec이 적었듯 “기능 하나짜리 스타트업”은 끝났고,[^Fordec] 남는 해자는 복제하기 어려운 데이터와, 그 데이터로 쌓은 품질의 격차다.

---

[^cobanov-api]: <https://news.ycombinator.com/item?id=49848625>

[^george_max]: <https://news.ycombinator.com/item?id=49848537>

[^cobanov-quality]: <https://news.ycombinator.com/item?id=49848595>

[^cjonas]: <https://news.ycombinator.com/item?id=49853893>

[^ranyume]: <https://news.ycombinator.com/item?id=49848482>

[^cobanov-example]: <https://news.ycombinator.com/item?id=49848600>

[^hbrn]: <https://news.ycombinator.com/item?id=49848784>

[^carimura]: <https://news.ycombinator.com/item?id=49853294>

[^thih9]: <https://news.ycombinator.com/item?id=49849866>

[^emmettbt]: <https://news.ycombinator.com/item?id=49848421>

[^george_max-ollama]: <https://news.ycombinator.com/item?id=49848485>

[^verdverm]: <https://news.ycombinator.com/item?id=49850309>

[^pradn]: <https://news.ycombinator.com/item?id=49850052>

[^janalsncm]: <https://news.ycombinator.com/item?id=49850243>

[^redox99]: <https://news.ycombinator.com/item?id=49850617>

[^fooker]: <https://news.ycombinator.com/item?id=49851886>

[^Fordec]: <https://news.ycombinator.com/item?id=49851827>
