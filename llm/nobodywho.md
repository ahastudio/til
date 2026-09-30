# NobodyWho: 앱 안에 LLM을 넣는 온디바이스 추론 엔진

<https://www.nobodywho.ai/>

<https://github.com/nobodywho-ooo/nobodywho>

HN 토론: <https://news.ycombinator.com/item?id=44487281> (2점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=34463>

## 소개

NobodyWho는 오픈 웨이트 LLM을 서버 없이 앱 안에서 돌리게 해 주는 추론 엔진이다.
README는 스스로를 “어떤 기기에서든 돌아가는 온디바이스 AI”라고 소개한다.
핵심은 Rust로 작성되어 있고, 실제 연산은 텍스트 쪽은 llama.cpp, 음성 쪽은 ONNX Runtime에 맡긴다.
라이선스는 EUPL-1.2이며, 2026년 9월 기준 GitHub 별은 약 1,460개다.

기능은 다음과 같다.

- 오프라인 로컬 실행, API 키나 사용료 없음
- Gemma, Qwen, Mistral 등 GGUF 형식의 채팅 모델 실행
- 함수 시그니처에서 문법(grammar)을 자동 생성하는 타입 안전한 도구 호출
- 이미지와 오디오를 직접 받는 멀티모달 입력
- Kokoro, Pocket TTS, Supertonic 백엔드의 음성 합성
- Whisper 기반 음성 인식과 Silero 기반 음성 구간 감지(VAD)
- Hugging Face나 임의 URL에서 모델 내려받기

바인딩은 여섯 가지다.

| 바인딩              | 설치 경로     | 실행 환경                     |
| ------------------- | ------------- | ----------------------------- |
| Kotlin              | Maven Central | 데스크톱, Android             |
| Swift               | SPM           | macOS, iOS, visionOS, watchOS |
| React Native / Expo | npm           | 데스크톱, Android, iOS        |
| Flutter             | pub.dev       | 데스크톱, Android, iOS        |
| Python              | PyPI          | 데스크톱                      |
| Godot               | AssetLib      | 데스크톱, Android             |

README가 먼저 알려 두는 공백이 세 가지 있다.
Godot 바인딩은 iOS로 내보낼 수 없고, Windows ARM64는 아직 지원하지 않으며, 웹 내보내기가 없다.
웹 지원은 이슈 #111에서 추적 중이다.

회사 쪽 홈페이지는 이 엔진 위에 온프레미스 서버 배포와 Assurance Layer라는 관리 계층을 얹어 판다.
토큰당 비용 0유로, 인프라 밖으로 나가는 데이터 0바이트, 유럽에서 만들고 유지한다는 점을 내세운다.
오픈소스 엔진은 그 사업의 하부 구조인 셈이다.

## 동작 방식

### 계층 구조

호출 경로는 네 층으로 나뉜다.

```text
Flutter · Python · Godot · Kotlin · Swift · React Native
        │            │        │        └─────┴──────┘
flutter_rust_bridge  PyO3    gdext        UniFFI
        └────────────┴────────┴──────────────┘
                         │
      NobodyWho 코어 (Rust): 채팅 · 템플릿 · 문법 · 샘플링 · 컨텍스트 이동
                ┌────────┴─────────┐
           llama.cpp          ONNX Runtime
   (텍스트·비전·임베딩·리랭킹)   (STT·TTS·VAD)
                └────────┬─────────┘
              Vulkan · Metal · CUDA · CPU
```

각 언어 바인딩은 얇은 연결층이고, 대화 기록 관리와 채팅 템플릿 적용, 도구 호출 문법 생성, 샘플링, 컨텍스트 정리는 모두 Rust 코어에서 한다.
그래서 홈페이지는 일곱 개 언어(Rust 포함) SDK가 같은 기능을 가진다고 말할 수 있다.
반대로 코어에 없는 기능은 어느 바인딩에서도 쓸 수 없다.

### 도구 호출이 문법으로 강제되는 방식

작은 모델은 도구 호출 형식을 자주 틀린다.
JSON 괄호를 빠뜨리거나, 없는 인자를 만들거나, 타입을 잘못 넣는다.
NobodyWho는 도구로 등록한 함수의 이름, 매개변수 이름, 타입을 읽어 구조화된 문법을 만들고,
샘플러가 그 문법에 맞지 않는 토큰을 아예 고르지 못하게 한다.
문서 표현으로는 올바른 도구 호출 형식을 알아내고, 매개변수의 이름과 타입을 살펴 샘플러를 설정한다.

이 방식의 의미는 형식 오류가 확률의 문제에서 불가능의 문제로 바뀐다는 것이다.
다만 문법이 보장하는 것은 형식뿐이다.
언제 어떤 도구를 부를지는 여전히 모델이 판단하며, 문서도 모든 모델이 도구 호출을 지원하는 것은 아니고 안정적인 호출에는 Qwen 계열을 권한다고 적는다.

### 컨텍스트가 차면 일어나는 일

기본 컨텍스트 크기(`n_ctx`)는 4096 토큰이다.
대화가 이 크기를 넘으면 NobodyWho는 시스템 프롬프트와 첫 사용자 메시지를 뺀 오래된 메시지를 지워,
사용량이 `n_ctx / 2`가 될 때까지 줄이고 KV 캐시도 함께 갱신한다.
요약이 아니라 삭제다.
`n_ctx`는 `Chat` 객체를 만들 때 고정되며 나중에 바꿀 수 없다.

### 스레드와 GPU 배분

CPU에서 돌 때는 논리 CPU 수가 아니라 성능 코어(P-core) 수만큼 스레드를 쓴다.
모든 연산이 가장 느린 스레드를 기다리는 장벽에서 끝나므로,
하이퍼스레드나 효율 코어가 섞이면 전체가 그 속도로 끌려 내려가기 때문이다.
문서가 싣는 측정값은 P-core 8개, E-core 4개인 12코어 Mac에서 다음과 같다.

| 스레드 수          | 프롬프트 처리 | 생성     |
| ------------------ | ------------- | -------- |
| 8 (성능 코어만)    | 435 tok/s     | 90 tok/s |
| 12 (모든 논리 CPU) | 327 tok/s     | 48 tok/s |

생성 속도가 거의 두 배 차이다.
GPU는 여유 VRAM에 들어가는 만큼 레이어를 올리고 나머지는 CPU에서 돌린다.
거의 들어가지 않으면 GPU를 건너뛰고, 여러 장이 있으면 여유 메모리가 가장 큰 한 장만 쓴다.

## 사용하기

### 가장 작은 예제

Python 바인딩으로 시작하면 설치와 확인이 가장 빠르다.

```bash
pip install nobodywho
```

```python
from nobodywho import Chat

# 약 330MB짜리 Qwen3 0.6B. 통합이 되는지 확인하는 용도로 README가 권하는 모델이다.
chat = Chat("hf:NobodyWho/Qwen_Qwen3-0.6B-GGUF:Q4_K_M")

# ask()는 토큰 스트림을 돌려준다. 바로 출력하려면 순회한다.
for token in chat.ask("What is the capital of Denmark?"):
    print(token, end="", flush=True)
print()

# Chat 객체가 대화 기록을 들고 있으므로 다음 질문은 앞 대화를 기억한다.
print(chat.ask("And what is its population, roughly?").completed())
```

모델 경로 자리에는 `hf:owner/repo:QUANT` 참조, HTTPS URL, 로컬 경로 중 하나를 넣는다.
원격 모델은 처음 쓸 때 내려받아 캐시하며, 이후에는 인터넷 없이 돈다.
`"auto"`를 넣으면 가용 메모리에 맞는 모델을 고른다.

### 도구 붙이기

```python
from pathlib import Path
from nobodywho import Chat, tool

@tool(description="Lists files in the given directory with their sizes in bytes",
      params={"path": "a relative or absolute path to a directory"})
def list_files(path: str) -> str:
    # 도구는 문자열을 반환해야 한다. 모델이 읽을 결과이기 때문이다.
    entries = [f"{p.name}: {p.stat().st_size}" for p in Path(path).iterdir() if p.is_file()]
    return "\n".join(entries) or "no files"

# 도구 호출은 Qwen 계열이 안정적이라고 문서가 권한다. 4B는 약 2GB다.
chat = Chat("hf:NobodyWho/Qwen_Qwen3-4B-GGUF:Q4_K_M",
            tools=[list_files],
            n_ctx=8192)  # 도구 결과가 컨텍스트를 빨리 채우므로 기본값 4096보다 넉넉히 둔다.

print(chat.ask("Which file in the current directory is the largest?").completed())
print(chat.stats())  # 컨텍스트 사용량을 확인한다.
```

`@tool`에는 설명이 반드시 있어야 하고, 매개변수 이름과 타입이 모델에 그대로 전달된다.
이름만으로 뜻이 불분명하면 `params`로 설명을 덧붙인다.
Python 해석기(`python_tool`)와 Bash 해석기(`bash_tool`)가 내장 도구로 들어 있으며,
무한 루프를 막으려면 `max_duration`, `max_memory`, `max_commands` 같은 제한을 걸어야 한다.

### 사용자마다 대화를 나누고 모델은 하나만 올리기

```python
from nobodywho import Chat, Model

# 모델 가중치는 한 번만 메모리에 올린다.
model = Model("hf:NobodyWho/Qwen_Qwen3-4B-GGUF:Q4_K_M")

# 대화 기록은 Chat마다 분리된다.
alice = Chat(model, system_prompt="You are a concise assistant.")
bob = Chat(model, system_prompt="You answer like a pirate.")

print(alice.ask("Say hello.").completed())
print(bob.ask("Say hello.").completed())
```

경로 대신 `Model` 객체를 넘기면 여러 `Chat`이 가중치를 공유한다.
경로를 그대로 넘기면 `Chat`마다 모델을 따로 올리므로 메모리가 배로 든다.

### OpenAI 호환 서버로 띄우기

```bash
uvx --from 'git+https://github.com/nobodywho-ooo/nobodywho.git#subdirectory=nobodywho/server' \
  nobodywho-server --model hf:NobodyWho/Qwen_Qwen3-0.6B-GGUF:Q4_K_M --name qwen

curl http://127.0.0.1:8888/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model": "qwen", "messages": [{"role": "user", "content": "Say hello."}]}'
```

`/health`, `/v1/models`, `/v1/chat/completions`만 제공하는 실험 기능이다.
모델은 하나, 생성은 순차 처리, 인증은 전혀 없고, 도구 선택에서 `required`를 지원하지 않는다.
문서가 직접 운영이나 민감한 작업에 쓰지 말라고 적는다.

## 값 정하기

| 항목              | 시작값                                 | 근거                                                                                             |
| ----------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 모델 크기         | Qwen3 0.6B로 통합 확인, 4B로 기능 확인 | 0.6B는 약 330MB로 어느 폰에서나 돈다. 4B는 약 2GB로 문서의 기본 추천이다                         |
| 양자화            | Q4_K_M                                 | Q4~Q5까지는 정확도 손실이 거의 없다. 작은 모델의 높은 비트보다 큰 모델의 낮은 비트가 대체로 낫다 |
| 메모리 추정       | 매개변수 수 × 비트 수 ÷ 8              | 14B Q4는 약 7GB, 2B Q8은 약 2GB                                                                  |
| 데스크톱 여유 RAM | 모델 파일의 1.5배, 바쁜 기기는 2배     | README 기준. 모델 2GB까지는 8GB 기기, 그 이상은 16GB 이상                                        |
| 모바일 여유 RAM   | 모델 파일의 2배                        | iOS는 약 2GB, Android는 제조사에 따라 2~4GB를 시스템이 먼저 가져간다                             |
| `n_ctx`           | 대화형 4096, 도구 사용 8192 이상       | 기본 4096은 짧은 대화용이다. 모델의 `max_ctx()`를 넘기면 이득이 없다                             |
| `n_threads`       | 비워 둔다                              | 자동으로 P-core 수를 쓴다. 게임 렌더링과 같이 돌릴 때만 낮춘다                                   |
| MTP 추측 디코딩   | 끈 상태로 시작                         | 코드나 JSON에서 크게 빨라지지만 통합 메모리 기기에서는 오히려 느릴 수 있고 VRAM을 약 5% 더 쓴다  |

재야 할 것은 세 가지다.
`chat.stats()`로 대화가 컨텍스트의 몇 퍼센트를 쓰는지 보고, 목표 기기에서 초당 생성 토큰 수를 재고,
앱이 평소에 쓰는 메모리 위에 모델을 올렸을 때 운영체제가 앱을 죽이는지 확인한다.
특히 모바일에서는 세 번째가 가장 먼저 무너진다.

## 트레이드오프

### 로컬 실행은 비용을 없애지 않고 사용자 기기로 옮긴다

토큰당 비용이 0이라는 말은 개발사 청구서 기준으로만 참이다.
전력, 발열, 배터리, 저장 공간, 첫 실행의 모델 내려받기 시간은 모두 사용자에게 넘어간다.
2GB 모델을 앱 설치 뒤에 내려받게 하면 모바일 데이터 사용자에게는 첫 경험부터 비용이 생긴다.

그렇다고 모델을 앱 번들에 넣으면 앱 크기가 커지고, 모델을 바꿀 때마다 앱을 다시 배포해야 한다.
내려받기 방식은 첫 실행 흐름을 복잡하게 만들고, 번들 방식은 배포 주기를 모델에 묶는다.
어느 쪽을 골라도 클라우드 API처럼 서버에서 모델을 몰래 바꾸는 유연성은 없다.
홈페이지의 Assurance Layer가 기기들의 모델을 관리하고 갱신하는 상품이라는 점은, 이 문제가 오픈소스 엔진만으로는 풀리지 않는다는 회사 스스로의 인정이다.

### 작은 모델의 능력 한계는 문법으로 메울 수 없다

문법 기반 도구 호출은 형식 오류를 없앤다.
하지만 사용자가 도구가 필요한 질문을 했을 때 도구를 부를지,
어떤 인자를 넣을지, 결과를 제대로 해석할지는 모델의 크기에 달려 있다.
형식은 완벽한데 판단이 틀린 호출은 형식이 깨진 호출보다 오히려 찾기 어렵다.
오류로 드러나지 않고 그럴듯한 오답으로 끝나기 때문이다.

그래서 모델을 키우고 싶어지지만, 모델을 키우면 지원 가능한 기기 목록이 줄어든다.
iPhone 11, 6GB RAM Android라는 최소 사양은 1GB 안팎의 모델을 전제로 한다.
기기 범위, 응답 품질, 응답 속도 세 가지를 동시에 최대로 가질 수 없고,
온디바이스 제품의 설계는 결국 셋 중 무엇을 양보할지 정하는 일이다.

### 컨텍스트 정리가 조용히 기억을 지운다

컨텍스트가 차면 오래된 메시지를 지우는 방식은 구현이 단순하고 예측 가능하다.
대신 사용자가 대화 중간에 알려 준 중요한 사실, 예컨대 알레르기나 선호 설정이 경고 없이 사라진다.
시스템 프롬프트와 첫 사용자 메시지만 남기 때문에, 중요한 정보가 두 번째 메시지 이후에 있으면 보장이 없다.

요약 방식으로 바꾸면 기억은 남지만 요약 자체에 추론 시간이 들고, 작은 모델의 요약은 정보를 왜곡한다.
`n_ctx`를 키우면 모든 응답이 느려지고 메모리를 더 쓴다.
현실적인 대응은 앱이 기억해야 할 사실을 대화 기록이 아니라 앱의 상태로 관리하고,
필요할 때 시스템 프롬프트나 `set_chat_history()`로 다시 넣는 것이다.

### 여섯 바인딩이 같은 코어를 쓰는 대가

Rust 코어 하나에 여섯 바인딩을 붙이는 구조는 기능의 일관성을 준다.
대신 네 가지 연결 도구(flutter_rust_bridge, PyO3, gdext, UniFFI)의 빌드 문제와 플랫폼별 네이티브 라이브러리 배포가 모두 이 프로젝트의 몫이 된다.
2026년 9월 14일에 다섯 바인딩이 한꺼번에 새 주 버전(Python 3.0.0, 나머지 4.0.0)으로 올라간 것도 코어 변경이 모든 바인딩의 호환성 단절로 이어지는 구조를 보여준다.
업그레이드 한 번이 여러 언어의 API 변경으로 퍼진다.
같은 Show HN 글은 Godot과 함께 Unity 플러그인을 내세웠지만, 지금 README의 바인딩 목록에는 Unity가 없다.
지원 대상이 늘어나는 만큼 줄어들기도 한다는 점은 특정 엔진에 묶어 도입할 때 따져 볼 일이다.

## 함정

모델 경로 문자열의 형식을 잘못 쓰면 원격 모델이 아니라 로컬 경로로 해석된다.
`owner/repo:QUANT` 형식은 저장소 이름이 `-GGUF`로 끝나고 양자화 표기가 있어야 원격 참조로 인식된다.
llama.cpp는 양자화가 정확히 맞지 않으면 저장소의 첫 모델을 쓰지만, NobodyWho는 오류를 낸다.

`complete()`에 넘긴 `tools`, `sampler`, `template_variables`는 그 호출에만 쓰이지 않고 채팅의 설정으로 남는다.
다음 호출에서 생략해도 앞의 값이 유지된다.
그리고 `tools`를 바꾸면 채팅 템플릿을 다시 고르고 시스템 프롬프트 영역을 다시 쓰므로, 그 턴은 거의 처음부터 프리필을 다시 한다.
매 호출마다 도구 목록을 새로 넘기면 매번 이 비용을 치른다.

멀티모달 모델은 LLM과 투영 모델(`mmproj`)이 한 쌍으로 학습된 것이어야 한다.
마음에 드는 LLM에 아무 투영 모델이나 붙이면 동작하지 않는다.
GGUF 한 파일에 모든 것을 담는다는 원칙이 여기서는 두 파일로 깨진다.

LFM처럼 채팅 템플릿 형식에 문제가 있는 모델은 원본 GGUF로는 실패할 수 있다.
NobodyWho는 이런 모델을 고친 버전을 자체 Hugging Face 계정에 올려 두므로, 처음에는 그 계정의 모델로 시작하는 편이 안전하다.

사고(thinking) 모델의 사고 구간 태그는 모델마다 다르다.
Qwen3는 `<think>`, Gemma 4는 `<|channel>thought`, Ministral은 `[THINK]`를 쓴다.
사고 내용을 직접 잘라내 파싱하려면 모델의 채팅 템플릿을 확인해야 한다.

라이선스를 오해하기 쉽다.
EUPL-1.2는 상호주의(copyleft) 라이선스지만, README는 유럽 법에서 링크만으로는 파생물이 되지 않는다는 해석을 인용하며 상용 앱에 자유롭게 쓸 수 있다고 명시한다.
의무가 생기는 것은 이 저장소의 코드를 수정해 배포할 때이며, 그 수정은 공개해야 한다.
독점 앱은 괜찮고 독점 포크는 안 된다는 것이 프로젝트의 요약이다.
다만 이 해석이 모두에게 편한 것은 아니다.
2025년 7월 NobodyWho 팀이 올린 Show HN 글에 iFire는 자기들은 EUPL의 동일 조건 공유(share-alike) 성격이 Godot 엔진과 맞지 않아
iree-gd를 쓰고 llama.cpp, PyTorch, ONNX를 직접 붙이는 방법을 검토했다고 답했다.[^iFire]
엔진 자체에 기여하거나 엔진 모듈로 합치려는 쪽에게는, 링크만 하는 앱 개발자와 다른 계산이 나온다는 뜻이다.

## 확인하기

목표 기기에서 통합이 되는지 먼저 가장 작은 모델로 확인하고, 그다음 실제 모델로 속도와 메모리를 잰다.

```python
import time
from nobodywho import Chat

def bench(model_path: str, prompt: str) -> None:
    t0 = time.perf_counter()
    chat = Chat(model_path, n_ctx=4096)
    loaded = time.perf_counter()

    n_tokens = 0
    first = None
    for _ in chat.ask(prompt):
        if first is None:
            first = time.perf_counter()  # 첫 토큰까지의 시간이 체감 지연을 좌우한다.
        n_tokens += 1
    done = time.perf_counter()

    print(f"{model_path}")
    print(f"  load {loaded - t0:.1f}s, first token {first - loaded:.2f}s")
    print(f"  generation {n_tokens / (done - first):.1f} tok/s over {n_tokens} tokens")
    print(f"  {chat.stats()}")

for path in ["hf:NobodyWho/Qwen_Qwen3-0.6B-GGUF:Q4_K_M",
             "hf:NobodyWho/Qwen_Qwen3-4B-GGUF:Q4_K_M"]:
    bench(path, "Explain in three sentences why the sky is blue.")
```

첫 실행은 내려받기 시간이 섞이므로 두 번째 실행의 숫자를 본다.
토큰 스트림의 한 항목이 정확히 한 토큰이 아닐 수 있으므로 tok/s는 추정치로 읽는다.
같은 스크립트를 `n_threads` 값을 바꿔 돌리면 문서의 P-core 주장을 자기 기기에서 확인할 수 있다.

## 체크리스트

- 목표 최저 사양 기기에서 모델 파일 크기의 2배 이상 여유 RAM이 있는가?
- 모델을 앱에 번들할지 첫 실행에 내려받을지 정했고, 내려받기 실패 시 흐름이 있는가?
- 도구 호출을 쓴다면 도구 호출이 검증된 모델(Qwen 계열 등)로 시험했는가?
- 도구를 쓰는 대화에 맞게 `n_ctx`를 기본값 4096보다 키웠는가?
- 컨텍스트 정리로 사라지면 안 되는 정보를 앱 상태로 따로 관리하는가?
- 여러 대화를 동시에 다룰 때 `Model` 객체를 공유하고 있는가?
- 내장 `python_tool`, `bash_tool`에 시간과 메모리 제한을 걸었는가?
- 매 호출마다 `tools`를 다시 넘겨 프리필을 반복하고 있지 않은가?
- 실험용 서버를 인증 없는 상태로 외부에 열어 두지 않았는가?
- 이 저장소의 코드를 수정해 배포한다면 수정분을 공개할 준비가 되어 있는가?

## 기억할 원칙

### 온디바이스 LLM은 모델 선택이 아니라 기기 선택에서 시작한다

클라우드 API에서는 먼저 쓸 모델을 고르고 비용을 계산한다.
온디바이스에서는 순서가 반대다.
지원할 가장 약한 기기가 쓸 수 있는 메모리가 모델 크기의 상한을 정하고, 그 상한이 가능한 기능을 정한다.

NobodyWho 문서가 가장 작은 모델로 통합부터 확인하라고 권하는 것도 이 순서 때문이다.
통합이 된다는 것과 제품이 된다는 것 사이의 거리는 목표 기기의 메모리와 속도가 결정한다.
설계 문서의 첫 줄에는 모델 이름이 아니라 최저 사양 기기가 와야 한다.

### 형식을 강제하는 것과 판단을 믿는 것은 다른 문제다

문법으로 도구 호출 형식을 강제하는 것은 작은 모델을 쓸 수 있게 만드는 좋은 설계다.
하지만 그 성공이 판단의 신뢰로 번지면 안 된다.
형식이 맞다는 것은 파서가 깨지지 않는다는 뜻이지, 호출이 옳다는 뜻이 아니다.

그래서 도구 결과를 받는 쪽, 즉 앱 코드가 인자를 검증하고 위험한 동작에는 사용자 확인을 요구해야 한다.
작은 모델일수록 이 검증층이 더 두꺼워야 한다.
모델이 틀리지 않게 만드는 것보다 틀려도 피해가 작게 만드는 것이 온디바이스에서 더 현실적인 목표다.

---

[^iFire]: <https://news.ycombinator.com/item?id=44503939>
