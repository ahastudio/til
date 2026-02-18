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

## AI 음악 생성 시장

Lyria 3의 출시는 AI 음악 생성 시장이 본격적으로
확대되는 시점에 이루어졌다. Gemini 앱의 월간 활성
사용자 7억 5천만 명이라는 규모는 기존 AI 음악
스타트업과 차원이 다른 배포 채널이다.

### Suno

<https://suno.com/>

2023년 말 출시된 AI 음악 생성 플랫폼.
Cambridge, MA 기반으로 Mikey Shulman과
Keenan Freyberg가 공동 창업했다.
텍스트 프롬프트로 가사와 보컬을 포함한 완성곡을
생성한다.

#### 모델 버전

- **V4.5** (2025년 5월): 1,200개 이상 장르 지원,
  자연스러운 보컬 표현, 44.1kHz 스튜디오급 오디오,
  최대 8분 트랙 생성. 보컬 교체(vocal replacement)와
  반주 자동 생성 기능 추가.
- **V5** (최신): ELO 벤치마크 1,293으로 역대 최고.
  오디오 충실도, 음악 구조, 보컬 사실감에서
  이전 버전을 상회한다.

#### 가격

| 플랜       | 가격      | 크레딧           |
| ---------- | --------- | ---------------- |
| Basic      | 무료      | 50/일            |
| Pro        | $10/월    | 2,500/월         |
| Premier    | $30/월    | 10,000/월        |

무료 크레딧으로 하루 약 10곡 생성 가능.
Pro 이상에서 상업적 사용 허가.

#### 저작권 소송과 라이선스

2024년 6월, RIAA를 대표해 Sony Music, UMG,
Warner Records가 Suno를 저작권 침해로 제소했다.
허가 없이 저작권 보호 음원으로 AI 모델을
학습시켰다는 혐의다.

2025년 11월, Warner Music Group이 Suno와 합의하고
라이선스 파트너십을 체결했다. 2026년 라이선스
기반의 새 모델 출시 예정이며, 아티스트가 자신의
이름, 이미지, 목소리 사용 여부를 직접 통제한다.
합의의 일환으로 Suno는 WMG의 콘서트 플랫폼
Songkick을 인수했다. Suno는 2025년 11월
$24.5억 기업가치로 $2.5억을 조달했다.

Sony Music과 UMG의 소송은 2026년 현재 계속
진행 중이며, 공정 이용(fair use)이 핵심 쟁점이다.

### Udio

<https://www.udio.com/>

전 Google DeepMind 엔지니어들이 2023년 12월
창업하고 2024년 4월에 출시한 AI 음악 생성 플랫폼.
Suno보다 세밀한 제어를 제공한다.

- **스템(Stem) 다운로드**: 베이스, 드럼, 보컬 등
  개별 요소 추출
- **인페인팅(Inpainting)**: 특정 구간만 재생성
- **리믹스**: 멜로디를 유지하면서 장르 변경
- **현재 모델**: Allegro v1.5

Udio는 UMG와 2025년 10월 라이선스 계약을
체결했다. 라이선스 플랫폼 전환 중 다운로드/내보내기
기능을 일시 중단한 상태다.

### 비교

| 항목         | Suno           | Udio           | Lyria 3       |
| ------------ | -------------- | -------------- | ------------- |
| 강점         | 속도, 편의성   | 음질, 제어력   | 플랫폼 규모   |
| 생성 시간    | 60초 이내      | 90초 이상      | -             |
| 무료 제공    | 50크레딧/일    | 10크레딧/일    | Gemini 내장   |
| 보컬 품질    | 좋음           | 매우 좋음      | 좋음          |
| 플랫폼       | 독립 웹앱      | 독립 웹앱      | Gemini 앱     |
| 라이선스     | WMG 합의       | UMG 합의       | 자체 학습     |

## 인사이트

**플랫폼 통합의 위력**.
Suno와 Udio가 독립 웹앱으로 수천만 사용자를
확보한 반면, Google은 7.5억 MAU의 Gemini 앱과
YouTube Dream Track이라는 배포 채널을 보유한다.
AI 음악 생성이 별도 앱이 아닌 범용 AI 어시스턴트의
기능으로 자리잡는 전환점이 될 수 있다.

**저작권 문제의 분기**.
Suno와 Udio는 기존 음원으로 학습하여 소송에
직면했고 레이블과 라이선스 합의를 진행 중이다.
Google은 자체 학습 데이터로 이 문제를 회피하면서
SynthID 워터마크와 아티스트 모방 방지 정책으로
선제적 대응을 하고 있다.

**생성 음악의 품질 도약**.
2024년 합성 느낌이 강했던 AI 음악이 2026년에는
전문 프로덕션과 구분하기 어려운 수준에 도달했다.
Suno V5, Udio Allegro v1.5, Lyria 3 모두
스튜디오급 품질을 주장하고 있으며, 음악 산업의
구조적 변화가 가속화될 전망이다.

## 참고 자료

- [Use Lyria 3 to create music tracks in the Gemini app - Google Blog](https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/)
- [Gemini - Music Generation](https://gemini.google/overview/music-generation/)
- [Lyria 3 - Google DeepMind](https://deepmind.google/models/lyria/)
- [Google adds Lyria 3 AI-music model to its Gemini app - Music Ally](https://musically.com/2026/02/18/google-adds-lyria-3-ai-music-model-to-its-gemini-app/)
- [Transforming the future of music creation - Google DeepMind](https://deepmind.google/blog/transforming-the-future-of-music-creation/)
- [Suno](https://suno.com/)
- [Udio](https://www.udio.com/)
- [AI-Music Heavyweight Suno Partners With Warner Music Group After Lawsuit Settlement - Rolling Stone](https://www.rollingstone.com/music/music-features/suno-warner-music-group-ai-music-settlement-lawsuit-1235472868/)
- [Record Companies Bring Landmark Cases for Responsible AI Against Suno and Udio - RIAA](https://www.riaa.com/record-companies-bring-landmark-cases-for-responsible-ai-againstsuno-and-udio-in-boston-and-new-york-federal-courts-respectively/)
