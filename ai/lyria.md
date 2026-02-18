# Lyria - Google DeepMind의 AI 음악 생성 모델

<https://deepmind.google/models/lyria/>

Google DeepMind가 개발한 AI 음악 생성 모델 시리즈.
텍스트, 이미지, 영상으로부터 보컬과 다중 악기 트랙을
포함한 고품질 음악을 생성한다.

## Lyria 3

2026년 2월 18일, Google이 Gemini 앱에 Lyria 3를
베타로 출시했다. DeepMind의 가장 진보된 음악 생성
모델이다.

<https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/>

### 주요 기능

- **텍스트 → 음악**: 프롬프트로 30초 트랙 생성.
  가사, 보컬, 커버 아트까지 자동 생성한다.
  예: "양말이 짝을 찾는 내용의 코믹 R&B 슬로우 잼"
- **이미지/영상 → 음악**: 사진이나 영상을 업로드하면
  분위기에 맞는 곡을 생성한다.
- **자동 가사 생성**: 이전 버전과 달리 사용자가 가사를
  직접 입력할 필요 없이 프롬프트 기반으로 자동 생성.
- **세밀한 제어**: 스타일, 보컬, 템포 등 음악 요소를
  사용자가 조정할 수 있다.

### 기술 구조

Latent Diffusion 아키텍처를 사용한다.
Stable Diffusion과 유사하지만 오디오에 최적화했다.
기존 "주크박스" 방식과 달리 루프를 조합하지 않고
풀 편곡을 처음부터 생성한다.

- **Chunk 기반 자기회귀(Autoregression)**: 2초 단위
  청크로 오디오를 생성하며, 이전 컨텍스트를 참조해
  흐름을 유지한다.
- **양방향 WebSocket**: 실시간 스트리밍을 위한
  라이브 연결을 유지한다.
- **오디오 품질**: 최대 48kHz 스테레오.
- **장르 지원**: 일렉트로닉, 오케스트라, 재즈,
  앰비언트, 팝, 록, 영화 음악 등.

### 이용 및 제한

| 항목         | 내용                                    |
| ------------ | --------------------------------------- |
| 대상         | 18세 이상 Gemini 사용자                 |
| 지원 언어    | 영어, 독일어, 스페인어, 프랑스어,       |
|              | 힌디어, 일본어, 한국어, 포르투갈어      |
| 트랙 길이    | 30초                                    |
| 구독자 혜택  | AI Plus, Pro, Ultra 구독자 한도 상향    |

<https://gemini.google/overview/music-generation/>

### SynthID 워터마크

생성된 모든 트랙에 SynthID가 삽입된다.
사람이 인지할 수 없는 워터마크로 AI 생성 콘텐츠를
식별한다. Gemini 앱에서 파일을 업로드하면 Google AI로
생성된 것인지 확인할 수 있다.

### 아티스트 모방 방지

특정 아티스트 이름을 프롬프트에 넣으면 직접 모방이
아닌 넓은 의미의 스타일 영감으로 해석한다.
원본 표현(original expression)을 위한 도구로
설계했다는 것이 Google의 입장이다.

## Lyria의 역사

### Lyria (v1) - 2023년 11월

Google DeepMind가 YouTube와 협력하여 공개했다.
YouTube Shorts용 음악 생성 엔진으로 출발했다.
악기와 보컬 포함 고품질 음악 생성, 스타일 변환,
이어 만들기(continuation) 기능을 지원했다.

### Dream Track

Lyria 기반의 YouTube 실험 기능이다.
Alec Benjamin, Charlie Puth, Charli XCX, Demi Lovato,
John Legend, Sia, T-Pain 등 아티스트의 음악 스타일로
30초 사운드트랙을 생성할 수 있었다.
가사, 반주, AI 보컬을 동시에 생성하는 방식이다.
Lyria 3 출시와 함께 Dream Track이 미국 외 글로벌로
확대되었다.

### Music AI Incubator

YouTube의 Music AI Incubator에서 아티스트, 작곡가,
프로듀서가 참여해 피드백을 제공하며 도구를
발전시켰다. 처음부터 새 음악 생성, 스타일 변환,
반주 생성 등의 도구를 개발했다.

## 다른 AI 음악 생성 서비스와 비교

| 항목       | Lyria 3              | Suno             | Udio             |
| ---------- | -------------------- | ---------------- | ---------------- |
| 출시       | 2026.02              | 2023 말          | 2024.04          |
| 강점       | 플랫폼 규모          | 속도, 편의성     | 음질, 제어력     |
| 최신 모델  | Lyria 3              | V5               | Allegro v1.5     |
| 무료 제공  | Gemini 내장          | 50크레딧/일      | 10크레딧/일      |
| 플랫폼     | Gemini 앱            | 독립 웹앱        | 독립 웹앱        |
| 저작권     | 자체 학습, SynthID   | WMG 합의         | UMG 합의         |

- [Suno](https://suno.com/): 텍스트 프롬프트로
  가사와 보컬 포함 완성곡을 생성한다.
  무료 ~$30/월. 2024년 RIAA 소송 후 WMG와 합의.
- [Udio](https://www.udio.com/): 전 DeepMind
  엔지니어 창업. 스템 추출, 인페인팅, 리믹스 등
  세밀한 제어 제공. UMG와 라이선스 계약 체결.

## 인사이트

**플랫폼 통합의 위력**.
독립 AI 음악 서비스들이 수천만 사용자를 확보한
반면, Google은 7.5억 MAU의 Gemini 앱과
YouTube Dream Track이라는 배포 채널을 보유한다.
AI 음악 생성이 별도 앱이 아닌 범용 AI 어시스턴트의
기능으로 자리잡는 전환점이 될 수 있다.

**저작권 선제 대응**.
경쟁 서비스들이 기존 음원 학습으로 소송에 직면한
반면, Google은 자체 학습 데이터, SynthID 워터마크,
아티스트 모방 방지 정책으로 저작권 리스크를
구조적으로 회피하고 있다.

## 참고 자료

- [Use Lyria 3 to create music tracks in the Gemini app - Google Blog](https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/)
- [Gemini - Music Generation](https://gemini.google/overview/music-generation/)
- [Lyria 3 - Google DeepMind](https://deepmind.google/models/lyria/)
- [Google adds Lyria 3 AI-music model to its Gemini app - Music Ally](https://musically.com/2026/02/18/google-adds-lyria-3-ai-music-model-to-its-gemini-app/)
- [Transforming the future of music creation - Google DeepMind](https://deepmind.google/blog/transforming-the-future-of-music-creation/)
