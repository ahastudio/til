# bloomery: 카드보다 큰 MoE 모델을 서버로 돌리는 Rust 추론 엔진

<https://github.com/midagedev/bloomery>

## 소개

bloomery는 mixture-of-experts(MoE) 모델을 위한 추론 엔진이다.
HTTP 서버부터 CUDA 커널까지 모두 Rust로 썼고,
llama-server를 그대로 대체하도록 만들었다.
라이선스는 MIT이고, 저장소는 2026년 9월 19일에 만들어졌으며 별은 41개다.

핵심 전제는 모델이 GPU 메모리보다 크다는 것이다.
라우팅되는 expert는 GPU와 호스트 RAM에 나눠 두고,
엔진이 스스로 라우팅 횟수를 세어 자주 호출되는 expert를 카드로 옮긴다.
호스트 RAM에도 다 들어가지 않으면 나머지를 NVMe의 모델 파일에서 읽어 온다.
README는 RTX 3090 24GB와 RAM 256GB 호스트에서
DeepSeek-V4.1-Flash `Q3_K_M`(347GB)이 요청 두 개를 합쳐 초당 34.4토큰,
GLM-5.3-Flash가 26.9토큰을 낸다고 적는다.

llama-server와 같은 HTTP API(OpenAI와 Anthropic 형식),
GGUF 파일, 플래그 철자를 쓴다.
그래서 클라이언트를 바꾸지 않고 붙일 수 있고,
Claude Code는 `ANTHROPIC_BASE_URL=http://localhost:8080`으로 연결한다.

이 문서는 README와 docs를 읽고 정리한 것이다.
수치는 전부 제작자가 자기 장비에서 잰 값이며, 이 문서가 다시 재현한 것은 없다.

## 무엇이 되고 무엇이 안 되는가

지원 범위가 좁다.
사용 전에 이 표부터 확인해야 한다.

| 항목        | 상태                                                               |
| ----------- | ------------------------------------------------------------------ |
| OS와 CPU    | Linux x86-64, AVX2 필요. Windows는 WSL2로만                        |
| GPU         | NVIDIA sm_86 이상(Ampere), 드라이버 R580 이상(CUDA 13)             |
| 검증된 카드 | RTX 3090, RTX A6000, RTX 3060                                      |
| Blackwell   | 사용자의 RTX 5090(WSL2)에서 동작 보고. Ada(sm_89)는 미실행         |
| DGX Spark   | 소스 빌드로 동작. 릴리스 바이너리는 x86-64뿐                       |
| 미지원      | macOS와 Apple silicon, AMD GPU, WSL2 없는 Windows                  |
| 호스트      | 수치는 모두 8채널 메모리 호스트에서 잰 것. 2채널 데스크톱은 미측정 |

가장 큰 제약은 마지막 줄이다.
CPU에 올린 expert의 속도는 메모리 대역폭이 정한다.
저장소 문서도 V4.1의 decode가 호스트 메모리 대역폭에 묶인다고 적는다.[^serving]
채널이 2개뿐인 일반 데스크톱에서는 README의 수치가 나온다고 기대하면 안 된다.

## 지원 모델

바이너리 하나가 일곱 개의 seat를 갖고, 파일의 아키텍처를 보고 seat를 고른다.
seat는 모델 계열별 실행 경로를 뜻하는 이 프로젝트의 용어다.

| seat       | 모델                                                     |
| ---------- | -------------------------------------------------------- |
| `ds41`     | DeepSeek-V4.1-Flash                                      |
| `glm`      | GLM-5.3-Flash                                            |
| `qwen38`   | Qwen3.8-Flash-Next                                       |
| `qwen3`    | Qwen3.6-35B-A3B, Qwen3-30B-A3B, MiniCPM-V 4.7 35B-A3B    |
| `mimo2`    | MiMo-V2.6-Flash                                          |
| `decide`   | Clef-Flash, lev(결정용 모델)                             |
| `nemotron` | Nemotron 3 Nano 4B, Nemotron 3.5 Bolt 74B-A9B(로컬 파일) |

메모리 요구는 모델마다 크게 다르다.
README는 Qwen3-30B와 Qwen3.6이 24GB 카드에서 돌고,
Qwen3.8은 RAM 128GB, GLM-5.3과 V4.1은 256GB를 원하며,
RAM이 모자라면 NVMe에서 읽어 오는 방식으로 돌아간다고 적는다.

## 실행하기

```sh
# Homebrew (Linux x86-64)
brew install midagedev/tap/bloomery

# 모델을 내려받아 서버를 띄운다
bloomery-serve --hf unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M --port 8080

# llama-server와 같은 형식으로 요청한다
curl -s http://127.0.0.1:8080/v1/chat/completions \
  -d '{"messages": [{"role": "user", "content": "Hello"}], "max_tokens": 64}'
```

Docker, 설치 스크립트, 릴리스 tarball도 있다.
처음 시작할 때 카드에 맞춰 GPU 코드를 한 번 컴파일하는 데 수십 초가 걸리고,
이후에는 몇 초면 뜬다.[^perf]
소스 빌드는 고정된 nightly Rust와 저장소 제작자의 cuda-oxide 포크가 필요해서
릴리스 바이너리를 쓰는 편이 쉽다.[^evaluating]

## 속도의 근거

저장소는 속도의 이유를 항목마다 같은 엔진에서
그 선택만 끄고 켠 측정과 함께 적는다.[^perf]
Rust로 썼다는 사실은 이유가 아니라고 스스로 밝힌다.[^perf]

| 선택                                   | 문서가 제시한 측정                                     |
| -------------------------------------- | ------------------------------------------------------ |
| 자주 쓰는 expert를 카드로 이동         | V4.1 decode 29.48 → 43.86 tok/s                        |
| prompt 처리에서 카드와 CPU 동시 작업   | V4.1, P = 4096에서 1.20배                              |
| prompt가 많이 쓰는 CPU expert를 카드로 | Qwen3.8 P = 4096에서 772.9 → 1,350.5 tok/s(A6000)      |
| Qwen prompt를 int8 텐서코어 GEMM으로   | P = 4096에서 357 → 2,615 tok/s                         |
| 디스크 행을 미리 읽기(V4.1)            | 토큰당 4.69ms → 0.31ms                                 |
| 한 decode step을 CUDA graph 하나로     | 현재 모델에서는 측정으로 분리하지 못했다고 문서가 인정 |

마지막 줄이 눈에 띈다.
측정 근거가 없는 항목에는 수치를 달지 않는다는 원칙을 문서가 지킨다.[^perf]

출력 정확도는 ik_llama.cpp의 중간 텐서와 층마다 비교해 확인한다고 한다.
공개 V4.1 파일에서 perplexity가 2.2401 대 2.2378,
같은 top token 비율이 97.46%다.[^perf]

## 벤치마크 읽는 법

README의 표는 bloomery만의 수치이고 다른 엔진과 나란히 놓은 비교가 아니다.
같은 카드와 시간대에서 llama.cpp,
mistral.rs와 함께 잰 행은 별도 저장소의 bench 페이지에 있다.[^bench]
거기서 비율은 같은 창에서 함께 잰 행끼리만 내고,
행마다 라운드 수와 provisional 여부를 단다.[^bench]

그 페이지의 Qwen3-30B 행을 보면 decode는 llama.cpp보다 약 1.01~1.08배,
prompt 처리는 약 1.4~2.2배 빠르다고 적혀 있다.[^bench]
decode는 거의 비기고 prefill에서 크게 앞서는 모양이다.

저장소 문서는 이 비교에 단서를 단다.
상대 엔진은 제작자가 찾은 가장 빠른 플래그로
돌렸을 뿐 그 엔진의 최선이라는 증명은 아니고,
일부 행은 두 엔진을 같은 조건에 두지 못했다.[^perf]
예로 V4.1 행에서 llama.cpp는 engram 테이블을 캐시 없이 읽었고
bloomery의 prompt는 같은 id를 반복했다.[^perf]
더 빠른 플래그를 아는 사람은 issue로 알려 달라고 적었다.[^perf]

## 함정

- 첫 요청은 느리다. 적응형 residency가 자주 쓰는 expert를 카드로 옮기는
중이기 때문이다. 시간을 잴 때는 한 번 버리고 재야 한다.[^evaluating]
- prompt cache가 켜져 있으면
반복한 prompt가 빨라진다. prefill 속도를 잴 때는 요청마다
다른 prompt를 쓰거나 `--cache-ram 0`을 줘야 한다.[^evaluating]
- 응답의 `timings`(`predicted_per_second`,
`prompt_per_second`)를 읽어야 한다. 다운로드와
로드가 섞인 wall time은 속도가 아니다.[^evaluating]
- 적응형 residency가 켜지면
같은 요청도 이전 요청의 이력에 따라 토큰이 달라질 수 있다. expert가 카드에
있느냐 호스트에 있느냐에 따라 활성값 반올림이 달라서 근접 동점에서
답이 바뀐다. 반복 가능한 출력이 필요하면
`BLOOMERY_RESIDENCY=off`로 속도를 내준다.[^serving]
- `--parallel 2`는 카드에 올라가는 expert 수를 줄인다.
두 서버의 답이 근접 동점에서 달라질 수 있다.[^serving]
- 구조화 출력은 `json_schema`와 강제 tool 호출만 되고, `$ref`,
`anyOf`, `pattern` 같은 키워드는 이름을 대며 거절한다.[^serving]
- GLM-5.3은 slot당 최대 16,384 위치까지만 담는다.[^serving]
- 한 서버에 모델 하나, expert 계층 카드는 최대 하나다.[^serving]
- 알려진 문제도 README가 적는다. V4.1을 카드 두
장(`--place bp`)에 올려도 한 장(`a`)보다 빠르지 않다.

## 공정하게 평가하기

저장소의 평가 문서는
사람이나 코딩 agent가 직접 돌려 볼 수 있게 열한 단계를 준다.[^evaluating]
핵심만 추리면 이렇다.

1. `nvidia-smi`, `ldd --version`,
`free -g`로 기계를 확인하고 모델이 요구하는 카드와 RAM에 맞는지 본다.
2. 릴리스 바이너리를 쓰고
`--hf`로 시작한다. 로그의 plan 줄이 expert를 어떻게 나눴는지 알려 준다.
3. 한 번 워밍업하고 버린다.
4. llama-server와 비교할 때는 같은 GGUF, 같은 `--ctx-size`,
같은 `--parallel`, 같은 요청 본문을 쓴다.
5. 모델 카드가 권하는 sampling을 쓴다.
6. 실패하면 `bloomery-serve --version`,
`nvidia-smi`, 명령, 로그를 붙여 issue를 연다.

Ada나 Blackwell 카드, Intel 호스트,
다중 카드 기계에서 돌려 본 보고를 환영한다고 하며,
성공 보고도 실패 보고만큼 도움이 된다고 적었다.[^evaluating]

## 판단

이 프로젝트의 가치는 속도 숫자 하나보다 정직한 측정 문서화에 있다.
측정이 없는 항목에 수치를 달지 않고,
다른 엔진 비교의 약점을 스스로 적고, 알려진 실패를 README 표에 둔다.
다만 이 문서가 확인한 것은 저장소 문서의 서술이지 그 수치의 재현이 아니다.

쓸 사람의 조건은 분명하다.
Ampere 이상 NVIDIA 카드가 있고, 호스트 메모리 채널이 넉넉하며,
RAM이 128GB 이상이고, Linux에서 돌린다.
이 조건에서 카드보다 큰 MoE 모델을 서버 형태로 쓰고 싶을 때 후보가 된다.
조건이 하나라도 빠지면 README의 수치는 기대치로 쓸 수 없다.

이 판단을 뒤집을 관찰은 두 가지다.
2채널 데스크톱 호스트에서 같은 모델이 쓸 만한 속도로 돌지 알려 주는 제3자 측정,
그리고 llama.cpp를 그 엔진의 최선 설정으로 같은 조건에 둔 독립 비교다.
어느 쪽도 이 문서를 쓴 시점에 찾지 못했다.

---

[^serving]: GitHub, [Serving: Limits](https://github.com/midagedev/bloomery/blob/main/docs/serving.md#limits)

[^perf]: GitHub, [Performance and verification](https://github.com/midagedev/bloomery/blob/main/docs/performance.md)

[^evaluating]: GitHub, [Evaluating bloomery](https://github.com/midagedev/bloomery/blob/main/docs/evaluating.md)

[^bench]: GitHub, [bloomery 벤치마크](https://github.com/midagedev/rig-log/blob/main/docs/bloomery-bench.md)
