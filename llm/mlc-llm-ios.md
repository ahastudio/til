# MLC-LLM으로 iOS에서 Gemma 3를 직접 컴파일해 돌리기

원문: [MLC-LLM으로 iOS에서 로컬 LLM 실행하기](https://blog.devstory.co.kr/post/mlc-llm-ios/)

GN 토론: <https://news.hada.io/topic?id=27437>

## 소개

서울의 개발자가 2026년 3월 12일에 쓴 실습 기록이다.
[MLC-LLM](mlc-llm.md)으로 iOS 기기에서 로컬 LLM을 돌리는 전 과정을 명령어 단위로 따라갈 수 있게 정리했다.

MLC-LLM은 기계 학습 모델을 모바일과 브라우저와 데스크톱을 포함한 모든 하드웨어에 범용으로 배포하고 고성능으로 실행하게 돕는 솔루션이다.
iOS에서는 **Metal API로 하드웨어 가속을 지원하므로** 사양이 낮은 모바일 기기에서도 LLM을 효율적으로 돌릴 수 있다는 것이 전제다.

글은 두 갈래로 진행된다.
먼저 MLCChat 프로젝트를 빌드해 **기본 제공 모델**을 돌리고, 다음으로 Hugging Face에서 받은 **임의의 모델을 직접 변환·컴파일**해 앱에 넣는다.

시연 결과로 두 가지 수치가 나온다.
Gemma 2 2B를 `q4f16_1`로 돌렸을 때 **약 2.4GB**, Gemma 3 1B를 같은 방식으로 돌렸을 때 **약 1.14GB**를 점유한다.

## 동작 방식

이 글의 절차를 이해하려면 MLC-LLM이 다른 온디바이스 추론 도구와 무엇이 다른지를 먼저 봐야 한다.

llama.cpp 계열은 GGUF 파일을 런타임이 읽어 해석한다. 모델을 바꾸면 파일만 바꾸면 된다.
MLC-LLM은 그렇지 않다. **모델마다 그 기기를 위한 실행 라이브러리를 미리 만들어야 한다.**

그래서 커스텀 모델을 올리는 과정이 네 단계로 갈라진다.

| 단계        | 명령                     | 산출물                            |
| ----------- | ------------------------ | --------------------------------- |
| 가중치 변환 | `mlc_llm convert_weight` | 양자화된 가중치 폴더              |
| 설정 생성   | `mlc_llm gen_config`     | `mlc-chat-config.json` 등         |
| 컴파일      | `mlc_llm compile`        | `*-iphone.tar` (Metal 커널)       |
| 패키징      | `mlc_llm package`        | Xcode 프로젝트에 묶인 최종 결과물 |

컴파일 단계가 이 도구의 정체성이다.
글의 설명대로 **모델의 연산 구조를 iPhone GPU가 가장 효율적으로 처리할 수 있는 형태의 라이브러리로 변환**하는 과정이며, `--device iphone`이 그 대상을 지정한다.

`git clone`에 `--recursive`가 필요한 이유도 여기에 있다.
핵심 컴파일 엔진인 **TVM Unity가 서브모듈**로 들어 있기 때문이다.

## 설정하기

### 초기 세팅

```bash
git clone https://github.com/mlc-ai/mlc-llm.git
cd mlc-llm
git submodule update --init --recursive
```

파이썬 가상 환경을 만들고 나이틀리 휠을 설치한다.
글이 가상 환경을 권하는 이유는 시스템 환경과의 충돌을 막기 위해서이고, 나이틀리를 권하는 이유는 `mlc-llm-nightly` 패키지가 **자주 갱신되기 때문**이다.

```bash
python3 -m venv .venv
source .venv/bin/activate
# 미리 빌드된 나이틀리 휠을 쓰는 것이 가장 효율적이다
python3 -m pip install --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cpu mlc-ai-nightly-cpu
```

가중치 파일이 수 GB에 이르므로 `git-lfs`가 필수이고, Metal GPU 가속을 위해 Metal 툴체인이 필요하다.

```bash
brew install git-lfs
git lfs install
xcodebuild -downloadComponent MetalToolchain
```

### 빌드와 실행

빌드 스크립트가 소스 위치를 알아야 하므로 환경 변수를 잡는다. 글은 셸 설정 파일에 넣어 두기를 권한다.

```bash
# ~/.zshrc 등에 추가. 경로는 자신의 클론 위치로
export MLC_LLM_SOURCE_DIR="/Users/yourname/projects/mlc-llm"
source ~/.zshrc
```

```bash
cd ios/MLCChat
python3 -m mlc_llm package
xed .                      # Xcode를 연다
```

Xcode에서 두 가지를 설정한다.

대상 기기는 실제 iPhone도 되지만 **My Mac (Designed for iPad)**을 고르면 Mac의 실리콘 가속으로 시험할 수 있다.
서명은 자기 Apple ID 팀을 고르고 **Bundle Identifier를 겹치지 않는 값으로** 바꾼다.

실행하면 모델 목록이 비어 있으므로 앱 안의 모델 관리자에서 기본 지원 모델을 내려받는다.

| 모델         | 특징                                       |
| ------------ | ------------------------------------------ |
| Llama-3.2-3B | Meta, 4비트 양자화, 2K 컨텍스트            |
| Gemma-2-2B   | Google, 효율적인 아키텍처, 4비트 양자화    |
| Phi-3.5-mini | Microsoft, 강한 추론 성능, 4비트 양자화    |
| Qwen3-0.6B   | Alibaba, 초경량, FP16 정밀도               |
| Qwen3-1.7B   | Alibaba, 균형형, 4비트 양자화, 2K 컨텍스트 |

### 커스텀 모델 올리기

Hugging Face에서 받으려면 로그인이 필요하다.

```bash
pip3 install huggingface_hub --upgrade
python3 -c "from huggingface_hub import login; login()"
```

토큰은 읽기(Read) 권한이면 충분하다.

```bash
python3 -c "from huggingface_hub import snapshot_download; \
  snapshot_download(repo_id='google/gemma-3-1b-it', \
  local_dir='./dist/models/gemma-3-1b-it', local_dir_use_symlinks=False)"
```

Gemma는 **게이트 저장소**라 라이선스 동의 전에는 `GatedRepoError: 403`이 난다.
Kaggle의 Gemma 라이선스 동의 페이지에서 Hugging Face 계정을 선택해 동의한 뒤, Gated Repos 화면에서 상태가 `Accepted`로 바뀐 것을 확인하고 다시 받으면 된다.

그다음이 앞에서 본 네 단계다.

```bash
# 1. 서버 GPU용 FP16/BF16 가중치를 4비트로 압축한다
python3 -m mlc_llm convert_weight ./dist/models/gemma-3-1b-it \
  --quantization q4f16_1 \
  -o ./dist/models/gemma-3-1b-it-q4f16_1-MLC/

# 2. 대화 템플릿을 포함한 설정을 만든다. 모델마다 템플릿이 다르다
python3 -m mlc_llm gen_config ./dist/models/gemma-3-1b-it \
  --quantization q4f16_1 \
  --conv-template gemma3_instruction \
  -o ./dist/models/gemma-3-1b-it-q4f16_1-MLC/

# 3. iPhone GPU용 Metal 커널을 생성한다
python3 -m mlc_llm compile ./dist/models/gemma-3-1b-it-q4f16_1-MLC \
  --device iphone \
  --output ./dist/models/gemma-3-1b-it-q4f16_1-iphone.tar
```

마지막으로 `mlc-package-config.json`에 항목을 더하고 다시 패키징한다.

```json
{
  "device": "iphone",
  "model_list": [
    {
      "model": "./dist/models/gemma-3-1b-it-q4f16_1-MLC",
      "model_id": "gemma-3-1b-it-q4f16_1",
      "model_lib": "gemma3_text_q4f16_1",
      "estimated_vram_bytes": 1500000000,
      "bundle_weight": true
    }
  ],
  "model_lib_path-for-prepare-libs": {
    "gemma3_text_q4f16_1": "./dist/models/gemma-3-1b-it-q4f16_1-iphone.tar"
  }
}
```

```bash
python3 -m mlc_llm package
```

## 값 정하기

이 절차에서 실제로 고르는 값은 많지 않다. 그런데 고르는 값마다 결과가 크게 갈린다.

| 값                     | 글의 선택            | 무엇에 달렸는가                                |
| ---------------------- | -------------------- | ---------------------------------------------- |
| 양자화 방식            | `q4f16_1`            | 기기 RAM과 허용 가능한 품질 저하               |
| 대화 템플릿            | `gemma3_instruction` | **모델이 정한다.** 틀리면 지시를 따르지 않는다 |
| 모델 크기              | 1B 또는 2B           | 점유 메모리와 과제 난이도                      |
| `--device`             | `iphone`             | 대상 하드웨어. 컴파일 산출물이 여기에 묶인다   |
| `estimated_vram_bytes` | 1,500,000,000        | 실측 점유량보다 여유 있게                      |

`q4f16_1`은 가중치를 4비트로 압축하되 연산 정밀도는 16비트로 유지해 품질 저하를 줄이는 방식이다.
글이 측정한 결과가 이 선택의 근거가 된다.

| 모델       | 파라미터 | 점유 메모리 |
| ---------- | -------- | ----------- |
| Gemma 2 2B | 20억     | 약 2.4GB    |
| Gemma 3 1B | 10억     | 약 1.14GB   |

글이 1B의 의미를 정확히 짚는다.
점유율이 절반 이하로 떨어지므로 **구형 기기나 여러 앱을 동시에 쓰는 환경에서도 강제 종료되지 않고 훨씬 안정적으로 돌아간다**는 것이다.

이것이 iOS에서 실제로 중요한 기준이다. 속도보다 **OS가 앱을 죽이지 않는가**가 먼저다.

대화 템플릿은 고르는 값처럼 보이지만 사실상 정해진 값이다.
글이 `--conv-template gemma3_instruction`을 지정해야 한다고 명시한 것이 그래서다. 각 LLM마다 어떻게 묻고 답할지에 대한 약속이 다르기 때문이다.

## 함정

### 컴파일 결과물은 모델과 기기에 동시에 묶인다

이 방식의 가장 큰 제약이 여기 있고, 글은 절차만 보여 주므로 명시되지 않는다.

`--device iphone`으로 만든 `.tar`는 **그 모델의 그 양자화 설정을 위한 iPhone 전용 라이브러리**다.
모델을 바꾸면 다시 컴파일해야 하고, 양자화 방식을 바꿔도 다시 컴파일해야 하고, 다른 플랫폼에 올리려면 또 다시 컴파일해야 한다.

GGUF 파일 하나를 여러 런타임이 읽는 것과 성질이 다르다.

그래서 이 방식은 **앱에 넣을 모델이 정해져 있을 때** 잘 맞는다.
사용자가 임의의 모델을 받아 쓰게 하려는 앱이라면 모든 후보를 미리 컴파일해 두거나 다른 도구를 골라야 한다.

### 나이틀리 의존이 재현성을 깎는다

글이 `mlc-llm-nightly`를 권하는 이유는 타당하다. 패키지가 자주 갱신되기 때문이다.

그런데 나이틀리는 버전이 고정되지 않는다.
오늘 되는 절차가 다음 주에 안 될 수 있고, 그때 원인이 자기 설정인지 패키지 변경인지 구분하기 어렵다.

[MLC LLM 프로젝트 노트](mlc-llm.md)에서도 사전 컴파일된 바이너리 의존이 재현성을 흐린다는 점을 짚었는데, 이 실습 절차가 그 문제를 그대로 물려받는다.

실무에서는 설치 시점의 휠 버전을 기록해 두는 편이 낫다.

```bash
pip freeze | grep -E 'mlc-(llm|ai)'
```

### 게이트 저장소는 스크립트를 조용히 멈춘다

Gemma 계열은 라이선스 동의가 필요하고, 동의 없이 받으면 `GatedRepoError: 403`이 난다.

글이 이 함정을 직접 겪고 해결 경로까지 적어 둔 것은 좋다.
다만 CI에서 이 절차를 자동화하려 할 때 문제가 커진다. **토큰에 권한이 있어도 계정이 동의하지 않았으면 실패하기 때문**이다.

그리고 동의는 사람이 브라우저에서 해야 한다. 자동화할 수 없는 단계가 파이프라인 한가운데 있는 셈이다.

### 소형 모델은 구조화된 출력에서 무너진다

글의 마무리에 가장 중요한 관찰이 있다.

시연한 소형 모델들이 온디바이스 환경에서 **JSON 같은 구조화된 응답을 생성하는 것을 다소 어려워했다**는 것이다.
그래서 복잡한 시스템 프롬프트가 필요한 기능이나 데이터 추출 업무에 쓰려면 프롬프트 엔지니어링이나 추가 파인튜닝 같은 보완이 필요하다고 적는다.

이 한 문단이 이 글에서 가장 값진 부분인데, 분량은 가장 적다.

온디바이스 LLM을 앱에 넣으려는 이유가 대개 **자연어를 앱의 동작으로 바꾸는 것**이기 때문이다. 그러려면 구조화된 출력이 필요하다.
그런데 정확히 그 부분이 안 된다는 것이 실측 결과다.

[Needle 같은 모델이 문법 제약 디코딩을 쓰는 이유](needle.md)가 여기에 있다.
모델에게 올바른 JSON을 생성하라고 요구하는 대신, **디코딩 단계에서 스키마 밖의 토큰을 아예 못 내게 막는 것**이다.

MLC-LLM 자체는 문법 제약 디코딩을 지원하지만 이 글의 절차에는 등장하지 않는다.
구조화된 출력이 목적이라면 그 기능을 켜는 것이 프롬프트 엔지니어링보다 먼저다.

### Metal 가속의 이점이 안드로이드로 옮겨 가지 않는다

GN 스레드에서 이 지점이 실측으로 드러났다.

kji96이 정확히 짚었다.
갤럭시 노트20에는 더 낮은 사양의 CPU에서 잘 동작하도록 최적화된 모델이 나오기 전까지 원활한 사용이 어렵지 않겠느냐면서, **글의 내용이 Mac 전용 Metal 커널용으로 만들어진 것**임을 상기시켰다.[^kji96]
그리고 MLX를 쓰면 일반 GGUF보다 빠른 로딩과 실행이 가능한 것으로 안다고 덧붙였다.

이 글의 제목이 iOS이고 모든 수치가 Apple 기기에서 나왔다는 점을 생각하면 당연한 지적이지만, 독자는 “온디바이스 LLM이 잘 돌아간다”는 인상만 가져가기 쉽다.

## 다른 기기에서는 어땠는가

GN 댓글 여덟 개가 전부 실사용 보고라서, 이 글이 보여 주지 않는 쪽을 채워 준다.

wedding은 갤럭시 폴드 4에서 Qwen 3 0.6B를 q5로 돌리고 있는데 **아직까진 좀 아쉽다**고 적었다.[^wedding]
dolsangodkimchi가 무엇이 아쉬운지 되물었다. 모델이 너무 작아 LLM 성능이 아쉬운 것인지, 로컬 실행 시 퍼포먼스가 아쉬운 것인지를 구분해 물은 것이다.[^dolsangodkimchi]

답이 명확했다. **퍼포먼스가 아쉬우며 GPU나 특정 NPU 지원이 아직 안 되어서 느리다**는 것이다.[^wedding-perf]

이 교환이 이 글의 수치를 해석하는 틀을 준다.

글이 보고한 “지연 시간이 거의 느껴지지 않는” 응답 속도는 **Metal 가속이 켜진 상태의 숫자**다.
가속이 없으면 같은 크기의 모델도 체감이 전혀 달라진다.
즉 온디바이스 LLM의 실용성을 가르는 것은 모델 크기가 아니라 **그 기기의 가속 경로가 지원되는가**다.

newbie1004는 갤럭시 노트 20 울트라에서 Gemma 3 1B int4를 연구 중이며 **구형 모델에서 돌아가는 수준**이라고 전했다.[^newbie1004]
그리고 **4B까지는 애매하다**고 덧붙였다.[^newbie1004-4b]

kaboom45가 Vulkan 가속이 되느냐고 물었고,[^kaboom45] wedding은 **된다고는 하는데 자기는 안 된다**고 답했다.[^wedding-vulkan]

이 짧은 교환이 안드로이드 쪽의 현실을 요약한다.
지원 목록에 있는 것과 자기 기기에서 켜지는 것이 다르다.

## 체크리스트

- `--recursive`로 클론했거나 서브모듈을 갱신했는가? TVM Unity가 없으면 컴파일이 되지 않는다
- `MLC_LLM_SOURCE_DIR`가 셸 설정에 들어가 있는가?
- `xcodebuild -downloadComponent MetalToolchain`을 실행했는가?
- Bundle Identifier를 고유한 값으로 바꿨는가?
- 게이트 모델이라면 브라우저에서 라이선스 동의를 마치고 상태가 `Accepted`인가?
- `--conv-template`가 그 모델이 요구하는 값인가? 기본값으로 두지 않았는가?
- `estimated_vram_bytes`가 실측 점유량보다 여유 있는가?
- 대상 기기의 실제 RAM에서 이 점유량이 버티는가? 다른 앱과 함께 떠 있을 때도 확인했는가?
- 구조화된 출력이 필요하다면 문법 제약 디코딩을 검토했는가?
- 설치한 나이틀리 휠 버전을 기록해 두었는가?

## 기억할 원칙

### 온디바이스 LLM에서 먼저 재야 할 것은 속도가 아니라 상주 메모리다

이 글이 두 모델에 대해 보고하는 핵심 수치가 응답 속도가 아니라 점유 메모리다.
2.4GB와 1.14GB이고, 글이 1B의 장점으로 든 것도 속도가 아니라 **강제 종료되지 않고 안정적으로 돈다**는 점이다.

이 우선순위가 맞다.

모바일 OS는 메모리가 부족하면 백그라운드 앱부터 죽인다.
2.4GB를 잡고 있는 앱은 사용자가 카메라를 켜거나 지도를 여는 순간 후보가 된다.
그리고 사용자 입장에서 **느린 앱과 돌아와 보니 처음부터 다시 시작하는 앱은 전혀 다른 경험**이다.

그러므로 온디바이스 LLM을 앱에 넣을 때 던져야 할 첫 질문은 “얼마나 빠른가”가 아니다.
**“이 앱이 포그라운드에서 벗어났다가 돌아왔을 때 모델이 살아 있는가”**다.

그 답이 아니오라면 모델을 다시 올리는 시간이 실제 지연이 되고, 벤치마크의 토큰 속도는 그 지연을 설명하지 못한다.

일반화하면 이렇다.
제약된 환경에서 성능을 논할 때, 자원 사용량은 성능과 맞바꾸는 대상이 아니라 **성능이 존재할 수 있는 조건**이다.

### 컴파일 방식은 유연성을 성능과 맞바꾼 것이고 그 대가는 나중에 온다

MLC-LLM이 모델마다 기기별 커널을 만들어 두는 방식을 택한 이유는 분명하다.
런타임 해석 계층이 없으므로 빠르다.

그런데 이 글의 절차를 끝까지 따라가면 그 대가가 보인다.
모델 하나를 더 넣으려면 다운로드, 변환, 설정 생성, 컴파일, 패키징을 다시 거쳐야 한다.

그리고 이 대가는 **개발할 때가 아니라 운영할 때** 온다.

새 모델이 나와서 갈아 끼우고 싶을 때, 양자화 방식을 바꿔 메모리를 줄이고 싶을 때, 안드로이드도 지원하기로 했을 때마다 파이프라인 전체를 다시 돌려야 한다.
GN에서 나온 안드로이드 쪽 보고들이 그 지점을 보여 준다. 같은 모델도 가속 경로가 다르면 다른 작업이 된다.

선택의 시점과 비용의 시점이 어긋나는 것이 **이런 구조의 특징**이다.
컴파일 방식을 고를 때는 성능만 보이고, 비용은 몇 달 뒤 모델을 갈아 끼울 때 나타난다.

그래서 이 도구를 고를 때 물어야 할 것은 “얼마나 빠른가”가 아니라 **“이 모델을 몇 번이나 바꿀 것인가”**다.
한 번 정해 두고 오래 갈 제품이면 컴파일 방식이 맞고, 모델을 자주 갈아 끼우거나 사용자가 고르게 할 제품이면 해석 방식이 맞다.

---

[^wedding]: <https://news.hada.io/topic?id=27437#cid53221>

[^dolsangodkimchi]: <https://news.hada.io/topic?id=27437#cid53289>

[^wedding-perf]: <https://news.hada.io/topic?id=27437#cid53468>

[^newbie1004]: <https://news.hada.io/topic?id=27437#cid52936>

[^newbie1004-4b]: <https://news.hada.io/topic?id=27437#cid52937>

[^kaboom45]: <https://news.hada.io/topic?id=27437#cid52984>

[^wedding-vulkan]: <https://news.hada.io/topic?id=27437#cid53695>

[^kji96]: <https://news.hada.io/topic?id=27437#cid52949>
