# Shimmy: 단일 바이너리 로컬 LLM 서버

<https://github.com/Michael-A-Kuykendall/shimmy>

## 소개

Shimmy는 Rust로 작성된 단일 바이너리 로컬 LLM 추론 서버다. GGUF 모델을 위한
OpenAI 호환 API 엔드포인트를 제공하며, 기존 OpenAI SDK나 툴을 코드 변경 없이
그대로 연결할 수 있다. MIT 라이선스로 공개되어 있으며, “영원히 무료”를 명시적으로
약속하고 있다.

기술 스택은 Rust + Tokio 비동기 런타임, llama.cpp 백엔드로 구성된다.
v1.9.0부터 플랫폼별로 GPU 백엔드가 모두 포함된 단일 바이너리를 제공한다.
Windows/Linux x64는 CUDA + Vulkan + OpenCL을, macOS ARM64는 MLX를 포함한다.

## 주요 기능

### 제로 설정 자동 인식

서버 시작 시 `~/.cache/huggingface/hub/`, `~/.ollama/models/`, `./models/`,
`SHIMMY_BASE_GGUF` 환경 변수 경로에서 GGUF 모델을 자동으로 탐색한다. 설정 파일도,
별도 초기화도 필요 없다. 포트 역시 자동 할당되어 충돌을 방지한다.

```bash
# 바이너리 다운로드 후 즉시 실행 (macOS Apple Silicon 예시)
curl -L https://github.com/Michael-A-Kuykendall/shimmy/releases/latest/download/shimmy-macos-arm64 -o shimmy
chmod +x shimmy
./shimmy serve
```

### GPU 백엔드 자동 감지

`--gpu-backend auto`(기본값)로 실행하면 CUDA → Vulkan → OpenCL → MLX → CPU 순으로
감지해 사용 가능한 최적 백엔드를 선택한다. 강제로 지정한 백엔드가 없으면 다음
우선순위로 자동 폴백하므로 운영 환경에서 크래시 없이 동작한다.

```bash
shimmy serve --gpu-backend auto      # 기본값, 자동 감지
shimmy serve --gpu-backend cuda      # NVIDIA 강제
shimmy serve --gpu-backend vulkan    # AMD/Intel 크로스플랫폼
shimmy serve --gpu-backend cpu       # 테스트/호환성용
```

### MOE CPU 오프로딩

70B 이상의 대형 모델을 소비자용 하드웨어에서 실행하기 위한 혼합 GPU/CPU 처리를
지원한다. `--cpu-moe` 플래그와 `--n-cpu-moe` 플래그로 CPU에 오프로드할 레이어 수를
제어한다. 한정된 VRAM을 가진 환경에서 시스템 RAM을 전략적으로 활용하는 구조다.

```bash
cargo install shimmy --features moe
shimmy serve --cpu-moe --n-cpu-moe 8
```

### OpenAI 호환 엔드포인트

기본 포트 `11435`에서 다음 엔드포인트를 제공한다.

```text
GET  /health
GET  /v1/models
POST /v1/chat/completions
POST /api/generate
GET  /ws/generate  (WebSocket 스트리밍)
```

Python과 Node.js에서 `base_url`/`baseURL`만 바꾸면 기존 코드가 그대로 동작한다.

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11435/v1", api_key="sk-local")
resp = client.chat.completions.create(
    model="<모델명>",
    messages=[{"role": "user", "content": "Say hi in 5 words."}],
)
print(resp.choices[0].message.content)
```

### CLI 명령 일람

```bash
shimmy serve                          # 서버 시작 (포트 자동 할당)
shimmy serve --bind 127.0.0.1:11435   # 포트 수동 지정
shimmy list                           # 사용 가능한 모델 목록
shimmy discover                       # 모델 재탐색
shimmy generate --name X --prompt "Hi" # 생성 테스트
shimmy probe <모델명>                  # 모델 로드 검증
shimmy gpu-info                       # GPU 백엔드 상태 확인
```

## 분석

Shimmy의 핵심 가치 제안은 “Ollama 수준의 간편함 + llama.cpp 수준의 성능”이다.
README의 성능 비교표에서 4.8MB 바이너리, 100ms 미만 시작 시간, 50MB 메모리 사용량을
Ollama(680MB, 5~10초, 200MB+)와 대비시킨다. 이는 `local-llm-without-ollama.md`에서
다뤘던 Ollama 비판과 맥락이 닿아 있다. Ollama가 독자 백엔드로 분기하면서 성능 격차가
생긴 자리를 Shimmy가 직접 llama.cpp 백엔드를 유지하며 채우겠다는 구도다.

기술적으로 Shimmy는 llama.cpp를 래핑하되 추상화 레이어를 최소화했다. 응답 캐싱은
LRU + TTL 방식을 사용하며 반복 쿼리에서 20~40% 성능 향상을 주장한다. 스마트 모델
프리로딩은 백그라운드에서 모델을 미리 로드하고 사용 이력을 추적해 모델 전환 시 지연을
줄인다.

Hacker News 프런트 페이지에 두 번 올랐다는 점, crates.io 다운로드 수치, GitHub 스타
상승 추세를 마케팅 포인트로 강조한다. 스폰서십 단계를 $5부터 $500까지 체계적으로
구성하고, “영원히 무료” 서약을 반복적으로 강조하는 것은 Ollama와의 차별화가
기술적 측면뿐 아니라 철학적 신뢰 면에서도 이루어지고 있음을 보여준다.

## 비평

Shimmy의 강점은 실용성의 밀도에 있다. 30초 안에 서버를 띄우는 경험을 단계별로
명확하게 제시하고, 코드 예제가 복사해 바로 실행 가능한 수준으로 완성도가 높다.
GPU 폴백 논리의 5단계 에러 처리 설명은 프로덕션 환경을 고려한 설계 감각을 보여준다.

그러나 성능 비교표에 신중함이 부족하다. “Binary Size 4.8MB”는 llama.cpp 백엔드를
포함한 실제 GPU 지원 빌드 기준으로는 “~40~50MB”라고 다른 섹션에서 스스로 인정한다.
4.8MB는 CPU 전용 최소 빌드 수치로 보이며, 이를 표에서 대표값으로 쓰는 것은
오해를 유발한다. 성능 수치를 인용할 때 측정 조건(모델, 컨텍스트 길이, 하드웨어)을
명시하지 않은 것도 검증 가능성을 낮춘다.

MOE 오프로딩을 `cargo install shimmy --features moe`로 별도 빌드해야 하는데,
프리빌드 바이너리에 이 기능이 포함되어 있는지 명확하지 않다. 대형 모델 사용자에게
중요한 기능이 배포 방식에 따라 다를 수 있다는 점은 사용자 혼란을 일으킬 수 있다.

`shimmy-vision-private`이라는 디렉토리 이름이 파일 목록에 포함되어 있다. 비전
기능의 일부가 비공개 저장소로 관리되는 것으로 보이는데, “영원히 무료 + MIT 라이선스”
서약과 조화를 이루는지 향후 확인이 필요하다.

## 인사이트

### 단일 바이너리 철학이 AI 인프라에서 갖는 의미

소프트웨어 배포에서 “단일 바이너리”는 단순한 편의성 이상의 가치를 지닌다.
의존성 지옥(dependency hell)의 부재, 버전 충돌 불가능, 에어갭 환경 배포 가능성,
컨테이너 없이도 재현 가능한 실행 환경을 의미한다. Shimmy가 이 철학을 AI
추론 서버에 적용한 것은 Go 언어의 단일 바이너리 철학이 서버 배포를 단순화한 것과
같은 궤적을 따른다.

Rust는 이 목표에 이상적인 언어다. C 런타임 의존 없이 정적 링킹이 가능하고,
메모리 안전성을 런타임 오버헤드 없이 보장한다. 하지만 GPU 백엔드를 단일 바이너리에
포함시키면 크기가 40~50MB로 증가한다. “142x smaller than Ollama”라는 주장은 CPU 전용
빌드 기준으로만 성립한다. 진정한 제로 의존성과 GPU 지원은 서로 트레이드오프 관계에
있으며, Shimmy는 이를 “플랫폼별 바이너리, 각 바이너리에 모든 백엔드 내장”으로
해결하려 한다.

이 접근의 장기적 함의는 흥미롭다. CUDA, Vulkan, OpenCL, MLX를 모두 정적으로
링크하면 바이너리 크기가 커지지만, 사용자는 GPU 드라이버만 설치하면 된다. 이는
“설치 크기 vs 사용자 마찰” 트레이드오프에서 마찰 감소를 선택한 것이다. 클라우드
네이티브 환경과 달리 엣지/로컬 환경에서는 이 선택이 합리적이다.

### OpenAI API 표준화가 만드는 로컬 AI 생태계의 전환 비용 구조

Shimmy가 OpenAI 호환 API를 제공하는 전략은 로컬 AI 생태계 전체의 수렴 현상을
반영한다. Ollama, LM Studio, llama.cpp 서버, Lemonade, vLLM이 모두 같은 API를
구현하고 있다. 이 수렴은 사용자에게 “클라우드에서 로컬로의 전환 비용 제로”를
의미하며, 동시에 공급자 간 교체 비용도 제로로 만든다.

이 구조에서 경쟁 우위는 API 설계가 아니라 성능, 안정성, 설치 경험, 모델 지원
범위, 커뮤니티 신뢰에서 결정된다. Shimmy는 이 중 설치 경험과 커뮤니티 신뢰에
집중한다. “영원히 무료” 서약, MIT 라이선스 강조, Ollama와의 암묵적 대비는
모두 신뢰 자본을 쌓는 시도다.

아이러니한 점은 이 모든 로컬 AI 도구들이 클라우드 API의 경쟁자를 자처하면서,
그 경쟁자의 API 설계를 표준으로 채택한다는 것이다. OpenAI의 API 설계가
인터넷의 HTTP처럼 사실상의 표준이 되어 가고 있다. 이 표준이 로컬 AI 생태계
전체를 묶는 인프라가 된 순간, OpenAI는 직접적인 수익을 얻지 않으면서도
에코시스템의 설계 권력을 유지하는 위치에 있다.

### 오픈소스 지속가능성 모델로서의 “철학적 차별화”

Shimmy의 비즈니스 모델은 스폰서십이다. $5부터 $500/월까지의 스폰서 계층과
“100%의 지원금이 영원히 무료로 유지하는 데 사용된다”는 약속은 사용자가
후원 의사 결정을 할 때 가이드를 제공한다. Patreon, GitHub Sponsors가
오픈소스 개인 개발자의 주요 수익 모델로 자리잡은 시대에 이 접근은 일관성이
있다.

“영원히 무료, 별표 없음”이라는 약속의 신뢰도는 현재 단계에서는 설립자의
의도에 의존한다. 법적 구속력이 없는 약속이며, 조직이나 자본 구조가
바뀌면 유지되지 않을 수 있다. Ollama가 VC 투자 후 전략을 바꾼 사례를 직접
반면교사로 삼고 있다는 점에서 의도는 진지해 보이지만, 사용자는 이를 신뢰
판단 시 할인율을 적용해 평가해야 한다.

더 근본적인 질문은 개인 개발자가 멀티플랫폼 GPU 지원, 여러 모달리티, 기업
수준 안정성을 요구받는 프로젝트를 스폰서십만으로 장기 유지할 수 있는가다.
현재 README의 기능 목록 - MOE 오프로딩, Prometheus 통합, Kubernetes 배포,
WebSocket 스트리밍, LRU 캐시 - 은 상당한 엔지니어링 깊이를 요구한다.
스폰서 수익이 이 유지 비용을 감당하지 못하는 순간, “영원히 무료”가 “영원히
방치”로 바뀔 위험이 있다. 이는 Shimmy만의 문제가 아니라 오픈소스 지속가능성
모델 전체가 직면한 구조적 긴장이다.
