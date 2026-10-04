# MoneyPrinterTurbo: 주제 한 줄로 숏폼 영상을 만드는 자동화 도구

<https://github.com/harry0703/MoneyPrinterTurbo>

HN 토론: <https://news.ycombinator.com/item?id=42150493> (2점, 0개 댓글)

## 소개

MoneyPrinterTurbo는 영상 주제나 키워드 하나를 받아 대본, 영상 소재, 음성, 자막,
배경 음악을 차례로 만들고 하나의 HD 숏폼 영상으로 합성하는 파이썬 프로젝트다.
README는 스스로를 올인원 AI 숏폼 영상 생성기라고 소개한다.
2026년 10월 4일 기준으로 GitHub 스타 128,326개,
포크 20,080개를 기록했고, 라이선스는 MIT다.
저장소는 2024년 3월 11일에 만들어졌고 `pyproject.toml`의 버전은 1.3.8이다.
같은 날까지도 커밋이 올라오고 있어 방치된 프로젝트는 아니다.

쓰는 길은 네 가지다.
Streamlit으로 만든 WebUI, FastAPI로 만든 HTTP API, 브라우저 없이 돌리는 CLI,
그리고 AI 에이전트에게 맡기는 방식이다.
마지막 방식은 저장소의 `docs/skill/SKILL.md`를 에이전트에게 읽히고 주제를 주면,
에이전트가 설치와 설정을 마친 뒤 영상 파일 경로를 돌려주는 흐름이다.
README는 이 에이전트 경로를 설치를 직접 하고 싶지 않은
사람에게 가장 먼저 권한다.

결과물은 세로 `9:16`(1080×1920), 가로 `16:9`(1920×1080),
정사각 `1:1`(1080×1080) 세 가지 비율로 나온다.
완성된 영상을 TikTok, Instagram, YouTube Shorts에 바로 올리는 기능도 들어 있다.
README의 갤러리에는 이 도구로 만든 중국어와 영어 예시 영상 16편이 14초에서
59초 길이로 올라와 있다.

## 동작 방식

### 다섯 단계 파이프라인

한 편의 영상은 다음 순서로 만들어진다.

1. LLM이 주제로 대본을 쓰고, 영상 소재를 찾을 검색 키워드를 뽑는다.
2. 키워드로 스톡 영상을 받아 오거나, 영상 생성 모델로 클립을 만들거나, 사용자가 올린 이미지와 영상을 쓴다.
3. TTS가 대본을 읽어 음성을 만든다.
4. 음성의 타임스탬프나 Whisper 전사로 자막 타이밍을 잡는다.
5. 배경 음악을 깔고 MoviePy로 클립, 음성, 자막을 하나의 영상으로 합성한다.

README의 후원 문구는 두 번째 단계의 품질이 첫 번째 단계에 달려 있다고 설명한다.
LLM이 내용을 잘 이해할수록 검색 키워드가 정확해지고,
키워드가 정확할수록 최종 화면이 대본과 맞아떨어진다는 것이다.
이 설명은 이 도구에서 가장 약한 고리가 어디인지도 함께 알려 준다.
대본과 화면을 잇는 연결은 키워드 검색 한 번뿐이다.

### 각 단계에 꽂을 수 있는 공급자

단계마다 공급자를 고를 수 있고, 그 목록이 이 프로젝트의 가장 큰 부분이다.

| 단계      | 선택지                                                                                    |
| --------- | ----------------------------------------------------------------------------------------- |
| 대본      | OpenAI, Claude, Gemini, DeepSeek, Qwen, Kimi, Grok, MiniMax, Ollama, OpenRouter, LiteLLM  |
| 영상 소재 | Pexels, Pixabay, Coverr, 로컬 파일, MiniMax H3, Seedance, Wan, MuAPI, 이미지 생성 후 변환 |
| 음성      | Edge TTS(무료), Azure, Gemini, ElevenLabs, Fish Audio, Kokoro, Chatterbox, VoxCPM         |
| 자막      | `edge`(TTS 타임스탬프, 기본값), `whisper`(`faster-whisper` 전사)                          |
| 음악      | `resource/songs`의 기본 곡, 로컬 파일, AI 생성 음악                                       |

LLM 쪽은 `litellm`을 의존성으로 두고 OpenAI 호환 게이트웨이를 폭넓게 받는다.
Claude Code 구독을 대본 생성기로 연결하는 항목도 목록에 있다.
AI 영상 소재는 대체로 4초에서 15초 길이의 클립으로 생성되고,
프로젝트가 이를 대본 구간에 맞춰 이어 붙인다.

### 의존성으로 본 구조

`pyproject.toml`을 보면 구조가 그대로 드러난다.
합성은 `moviepy` 2.2.1, WebUI는 `streamlit`, API는 `fastapi`와 `uvicorn`,
음성은 `edge-tts`와 `azure-cognitiveservices-speech`,
자막은 `faster-whisper`가 맡는다.
작업 상태 저장에 `redis`를 쓸 수 있고,
영상 이해와 임베딩을 위한 TwelveLabs 연동은 선택 의존성으로 빠져 있다.
의존성 버전은 모두 고정되어 있고 `uv.lock`이 해석 결과를 묶는다.

## 설치와 실행

### 경로 고르기

README가 권하는 경로는 운영체제에 따라 갈린다.

| 상황                     | 권장 경로                              |
| ------------------------ | -------------------------------------- |
| 설치를 직접 하기 싫다    | AI 에이전트에 `SKILL.md`를 읽혀 맡긴다 |
| Windows에서 빨리 써 본다 | Releases의 `.7z` 원클릭 패키지         |
| macOS, Linux             | `uv`로 로컬 설치                       |
| 격리된 환경이 필요하다   | Docker Compose                         |
| 로컬 환경 없이 써 본다   | Google Colab 노트북                    |

Windows 원클릭 패키지는 Releases 페이지의 Assets에 있는 `.7z` 파일이어야 한다.
GitHub가 자동으로 붙이는 `Source code (zip)`에는 `webui.bat`만 있고
`start.bat`과 `update.bat`이 없다.
패키지를 풀면 `update.bat`으로 최신 코드를 받은 뒤 `start.bat`으로
실행하라고 README는 안내한다.

### 로컬 설치

```bash
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
uv python install 3.11
uv sync --frozen          # uv.lock에 고정된 버전 그대로 설치
sh webui.sh               # WebUI, 빈 포트를 골라 브라우저를 연다
uv run python main.py     # API 서버, 문서는 :8080/docs
```

Python은 3.11 이상이 필요하다.
처음 실행할 때 `config.example.toml`에서 `config.toml`이 만들어지므로 설정
파일을 직접 복사할 필요는 없다.
클라우드 LLM이나 영상 생성 서비스의 API 키는 WebUI의 기본 설정 화면에서 넣는다.
같은 네트워크의 다른 기기에서 WebUI를 열려면
`MPT_WEBUI_HOST=0.0.0.0`을 지정한다.

### Docker

```bash
cp config.example.toml config.toml   # 컨테이너에 마운트할 설정 파일
docker compose -f docker-compose.release.yml up
```

`docker-compose.release.yml`은 `ghcr.io/harry0703/moneyprinterturbo:latest`
이미지를 받아 쓴다.
WebUI는 `127.0.0.1:8501`, API 문서는 `127.0.0.1:8080/docs`에 뜬다.
API는 기본적으로 같은 출처의 브라우저 요청만 허용하고,
다른 출처의 프런트엔드가 직접 부를 때만 `CORS_ALLOWED_ORIGINS`를 설정한다.
curl이나 n8n 같은 서버 쪽 클라이언트에는 CORS가 상관없다.

### CLI와 배치

```bash
uv run python cli.py --video-subject "How AI is changing everyday life"
uv run python cli.py --batch-file ./tasks.json --stop-at video
```

배치 파일은 UTF-8 JSON 배열이나 JSONL이며, 각 객체가
`VideoParams`의 필드를 덮어쓴다.

```json
[
  { "video_subject": "How solar panels work" },
  { "video_subject": "How wind turbines work", "video_aspect": "16:9" }
]
```

배치에는 작업 100개, 파일 1MiB라는 상한이 있다.
모든 항목을 먼저 검증한 뒤 실행하고, 한 작업이 실패해도 나머지를 계속 돌린다.
끝나면 `total`, `succeeded`, `failed`, `tasks`를 담은 JSON 요약 하나를 출력하며,
작업마다 실패한 단계(`failed_stage`)와 오류가 남는다.

CLI의 자막 스타일과 음성 설정은 명시한 옵션, `config.toml`의 `[ui]` 값,
내장 기본값 순서로 정해진다.
배경 음악, 영상 개수, 문단 수 같은 나머지 설정은 WebUI에서 물려받지 않는다.
WebUI에서 업로드한 음성을 쓰도록 해 두었더라도 CLI에서는
`--custom-audio-file`을 따로 넘겨야 한다.

### 사양

| 항목 | 최소      | 권장     | 최적       |
| ---- | --------- | -------- | ---------- |
| CPU  | 4코어     | 6~8코어  | 8코어 이상 |
| RAM  | 4GB       | 8GB      | 16GB 이상  |
| GPU  | 필요 없음 | VRAM 4GB | VRAM 8GB   |

클라우드 LLM, 클라우드 TTS,
온라인 소재만 쓴다면 GPU보다 CPU와 메모리가 중요하다.
GPU가 의미 있어지는 경우는 `faster-whisper`로 자막을 만들거나
배치를 크게 돌릴 때다.

## 값 정하기

### 자막 모드

자막의 기본값은 `edge` 모드로, TTS가 돌려준 타임스탬프를 그대로 쓴다.
GPU 없이 빠르게 끝나지만, 타이밍이 TTS 엔진의 출력에 묶인다.
더 정확한 타임라인이 필요하면 `whisper` 모드로 바꾼다.

```toml
[app]
subtitle_provider = "whisper"

[whisper]
model_size = "large-v3-turbo"   # 기본 large-v3는 약 3GB, turbo는 약 1.6GB
```

Whisper 모델은 처음 쓸 때 Hugging Face에서 받는다.
자동 다운로드가 막히면 `faster-whisper-large-v3`를 직접 받아
`models/whisper-large-v3`에 두어야 한다.

### 음성

WebUI의 Azure TTS V1은 실제로는 Edge TTS이고, API 키 없이 무료로 쓸 수 있다.
비용 없이 첫 영상을 만들어 보는 조합은 Ollama 같은 로컬 LLM,
Pexels나 Pixabay의 무료 API, Edge TTS, `edge` 자막이다.
ModelBest VoxCPM을 고르면 참고 음성으로 화자를 복제할 수 있다.
참고 음성은 20MiB까지 올릴 수 있고, 현재 브라우저 세션과 작업 안에서만 쓰이며
설정이나 로그에 남지 않는다고 README는 밝힌다.

## 트레이드오프

### 스톡 영상은 싸지만 대본과 어긋난다

Pexels와 Pixabay는 무료이고 화질도 HD다.
대신 화면은 대본이 아니라 LLM이 뽑은 키워드에 맞춰 고른다.
키워드가 추상적일수록 화면은 주제와 상관없는 일반적인 장면으로 흐른다.

이 문제는 이름이 같은 선행 프로젝트인 FujiwaraChoki의 MoneyPrinter가 2024년 2월
HN에 올라왔을 때 이미 지적되었다.
직접 설치해 본 사용자는 프롬프트에 맞는 영상이 다섯 개 중 하나
정도라고 적었다[^jcpham2].
같은 사용자는 LLM 응답에 콜론이 들어가면 자막 생성이 실패해서 코드를 직접 고쳐야
했다고 덧붙였다[^jcpham2-reply].
다른 사용자는 데모 영상의 소재가 흐릿한 식물 클로즈업과 반쯤 잘린
앵무새였다고 지적했다[^mashimo].
MoneyPrinterTurbo가 AI 영상 생성 공급자를 계속 늘리는 이유도 여기서 읽힌다.
대본 구간마다 클립을 새로 생성하면 화면을 대본에 맞출 수 있지만,
그만큼 클립마다 비용이 붙는다.

### 공급자 선택지는 넓지만 비용 구조가 흩어진다

LLM, 영상, 음성 공급자를 단계마다 따로 고를 수 있다는 것은 유연하다는 뜻이다.
동시에 키와 과금 계정이 단계 수만큼 늘어난다는 뜻이기도 하다.
AI 영상 클립을 쓰는 순간 영상 한 편의 비용은 대본 생성이 아니라
클립 생성이 지배한다.
배치로 수십 편을 돌리기 전에 한 편의 단계별 비용을 먼저 재야 하는 이유다.

### 편집 통제와 자동화는 반대 방향이다

README는 모든 단계를 자동으로 넘기면서도 단계마다 통제권을 남긴다고 말한다.
실제로 대본을 직접 넣거나, 소재를 직접 올리거나, 음성을 업로드할 수 있다.
그러나 사람이 손을 대는 단계가 늘수록 주제 한 줄로 끝난다는 장점은 줄어든다.
`docs/video-projects.md`가 설명하는 리비전 기반 로컬 프로젝트는 이
간극을 메우려는 장치다.
준비된 장면 소재를 바꾸면 영향을 받는 단계만 다시 빌드하고,
마지막으로 성공한 결과물을 보존하며, 공급자 호출이나 자동 게시는 하지 않는다.

## 함정

### ffmpeg를 찾지 못한다

보통은 ffmpeg가 자동으로 내려받아지지만,
네트워크가 막힌 환경에서는 `No ffmpeg exe could be found` 오류가 난다.
이때는 ffmpeg를 직접 받아 `config.toml`의 `[app]`에 `ffmpeg_path`를 적는다.
Windows 경로는 역슬래시를 두 번 써야 한다.

### 열린 파일 수 한도에 걸린다

클립을 많이 이어 붙이면 `OSError: [Errno 24] Too many open files`가 날 수 있다.
`ulimit -n`으로 한도를 확인하고 `ulimit -n 10240`처럼 올린다.

### Windows 경로와 원클릭 패키지

Windows에서는 프로젝트 경로에 한글 같은 비ASCII 문자, 특수문자,
공백이 들어가지 않게 해야 한다.
Source code zip을 받으면 실행 스크립트가 빠져 있다는 점도 처음 쓰는 사람이
자주 걸리는 부분이다.

### 기본 배경 음악의 저작권

`resource/songs`에 들어 있는 기본 곡은 YouTube 영상에서 가져온 것이다.
README는 저작권 문제가 있으면 지우라고만 적는다.
영상을 플랫폼에 자동 게시하는 기능과 이 기본 곡을 함께 쓰면 저작권 신고를 받을
위험을 그대로 떠안는다.
게시까지 자동화한다면 기본 곡을 지우고 라이선스가 확인된 음악만
남겨 두는 편이 안전하다.

### MoviePy 유지보수

합성의 핵심인 MoviePy는 2024년 초에 메인테이너를 찾고 있었고, v2 재작성이
진행되던 중이었다[^drekipus].
MoneyPrinterTurbo는 현재 `moviepy==2.2.1`로 v2 이후 버전에 고정되어 있다.
버전을 고정한 덕에 당장은 안정적이지만,
합성 단계의 버그는 결국 상위 라이브러리의 속도에 묶인다.

## 비평

### README의 절반은 후원 광고다

영문 README는 약 38KB인데, 기능 설명보다 앞에 Kimi, BytePlus,
APIMart, Metaso, Infistar, OfoxAI, Shengsuan Cloud, AstraFlow, Fluxion AI,
RecCloud 같은 후원사 블록이 길게 이어진다.
대부분은 추적 파라미터가 붙은 가입 링크와 할인 문구,
무료 크레딧 안내를 담고 있다.
기능 목록 안의 공급자 링크에도 같은 추천 코드가 붙어 있다.
공식 가격의 1%라거나 40~98% 저렴하다는 수치는 후원사가 내세운 주장이며,
README가 검증한 것이 아니다.

이 구조가 문제인 이유는 독자가 기능과 광고를 구별하기 어렵기 때문이다.
어떤 공급자가 기능 목록 위쪽에 놓인 것이 품질 때문인지 후원 때문인지
README만으로는 알 수 없다.
스타 12만 개를 넘긴 저장소의 첫 화면이 광고판 역할을 한다는
것은 오픈소스 프로젝트가 돈을 버는 방식 하나를 보여 주지만,
도구를 평가하려는 사람에게는 소음이다.

### 이름이 목적을 말한다

프로젝트 이름의 Money Printer는 돈을 찍어 내는 기계라는 뜻이다.
선행 프로젝트가 HN에 올라왔을 때 한 사용자는 이 이름 자체가 오늘날 영상 수익화의
모습을 말해 준다고 꼬집었다[^kaladin-jasnah].
다른 사용자는 데모 채널의 조회수가 대부분 수백 회 수준이라 YouTube
수익화 조건인 구독자 1,000명과 시청 시간 4,000시간에 미치지 못했을 것이라고
짚었다[^plasticbugs].
README의 갤러리는 기술 시연 영상이지만,
이름은 이 도구의 쓰임새가 콘텐츠 농장임을 숨기지 않는다.

README는 이 쓰임새가 플랫폼에 어떤 문제를 만드는지 다루지 않는다.
같은 HN 스레드에서는 YouTube 추천과 검색에 사실을 지어낸 역사,
과학 영상이 늘었다는 관찰이 나왔다[^haxiomic].
한 사용자는 이런 도구의 이상적인 고객이 소셜 미디어 콘텐츠 공장을 돌리는 마케팅
회사라고 보았다[^rchaud].
다른 사용자는 그런 영상을 만드는
사람이 한 달에 1만 5천 달러 넘게 번다는 인터뷰를 소개하며,
플랫폼이 개입하지 않는 한 사라지지 않을 것이라고 보았다[^sorenjan].
자동 게시 기능까지 갖춘 도구라면 생성물 검수와 AI 생성 표시를 어떻게 다룰지
안내할 책임도 생긴다.

### 품질 검증 장치가 없다

파이프라인은 대본이 사실인지,
화면이 대본과 맞는지를 확인하는 단계를 두지 않는다.
배치 요약은 작업이 성공했는지만 알려 주고,
결과물이 쓸 만한지는 알려 주지 않는다.
작업 100개를 한 번에 돌리고 플랫폼에 바로 올리는 흐름에서 이 공백은 커진다.
LLM이 지어낸 수치가 자막과 음성으로 그대로 나가는 일을 막는 것은
전적으로 사용자 몫이다.

## 인사이트

### 숏폼 자동화의 병목은 생성이 아니라 정렬이다

대본, 음성, 자막은 이미 거의 공짜로 만들 수 있다.
남은 어려움은 화면을 대본에 맞추는 일이다.
스톡 영상 검색은 키워드라는 좁은 통로를 거치므로 의미가 새어 나가고, AI 영상
생성은 의미를 지키지만 비용과 일관성 문제를 새로 만든다.
MoneyPrinterTurbo가 2년 넘게 공급자 목록을 늘려 온 과정은 이 정렬 문제를 공급자
교체로 풀려는 시도의 기록으로 읽힌다.

### 오픈소스 래퍼는 API 유통 채널이 된다

이 프로젝트는 스스로 모델을 만들지 않는다.
여러 회사의 LLM, TTS, 영상 생성 API를 하나의 흐름으로 묶을 뿐이다.
그런데 그 묶음이 스타 12만 개의 트래픽을 모으자, API 회사들이 후원 형태로 사용자
유입을 사는 구조가 생겼다.
오픈소스 래퍼가 API 공급자에게는 유통 채널이 되고,
메인테이너에게는 광고 수익원이 되는 셈이다.
이 구조에서는 기능 추가와 후원 유치가 같은 방향을 향하므로,
공급자 목록은 줄어들 이유가 없다.

### 에이전트가 설치 담당자가 된다

README가 가장 먼저 권하는 설치 방법이 AI 에이전트에게 `SKILL.md`를 읽히는
것이라는 점은 눈여겨볼 만하다.
Python 버전, ffmpeg, Whisper 모델, API 키 같은 설치 마찰을 사람이 아니라
에이전트가 흡수하게 하는 설계다.
비개발자 사용자가 많은 도구일수록 이 경로가 설치 문서를 대체할 가능성이 크다.
다만 에이전트가 API 키를 받아 설정 파일에 쓰는 과정은 사람이 보지 않는 곳에서
일어나므로, 키가 어디에 저장되는지 직접 확인해 두어야 한다.

---

[^jcpham2]: <https://news.ycombinator.com/item?id=39349343>

[^jcpham2-reply]: <https://news.ycombinator.com/item?id=39360246>

[^mashimo]: <https://news.ycombinator.com/item?id=39299884>

[^drekipus]: <https://news.ycombinator.com/item?id=39296107>

[^kaladin-jasnah]: <https://news.ycombinator.com/item?id=39296119>

[^plasticbugs]: <https://news.ycombinator.com/item?id=39296220>

[^haxiomic]: <https://news.ycombinator.com/item?id=39301142>

[^rchaud]: <https://news.ycombinator.com/item?id=39302685>

[^sorenjan]: <https://news.ycombinator.com/item?id=39301537>
