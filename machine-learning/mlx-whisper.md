# mlx-whisper: Apple Silicon GPU로 돌리는 Whisper

<https://github.com/ml-explore/mlx-examples/tree/main/whisper>

HN 토론: <https://news.ycombinator.com/item?id=40225839> (4점, 0개 댓글)

## 소개

mlx-whisper는 OpenAI의 음성 인식 모델 Whisper를 Apple의 머신러닝 프레임워크
MLX로 옮긴 구현이다.
Apple의 `ml-explore/mlx-examples` 저장소 안 `whisper/` 폴더에 있고,
PyPI에는 `mlx-whisper` 패키지로 올라가 있다.
저장소 라이선스는 MIT이고, 2026년 10월 기준 패키지 버전은 0.4.3이다.

README는 Whisper를 3,900만에서 15억 파라미터에 이르는 오픈소스 음성 인식 모델
모음이라고 소개하고,
설치부터 CLI, Python API, 모델 변환까지 짧게 다룬다.
음성 파일을 읽는 데 ffmpeg가 필요하다는 점을 첫 단계로 둔다.

이 저장소의 [YouTube 영상 매뉴얼](../video/youtube-download.md)에서는
mlx-whisper 0.4.3과 `mlx-community/whisper-large-v3-turbo` 모델로
5시간짜리 한국어 강의를 M4 Pro에서 약 10분 만에 자막으로 만들었다.
아래의 함정 일부는 그때 직접 겪은 것이다.

## 동작 방식

### 30초 창으로 잘라 이어 붙인다

소스 코드의 상수를 보면 동작이 분명하다.
음성은 ffmpeg로 16kHz 모노로 변환해 읽고(`SAMPLE_RATE = 16000`),
30초(`CHUNK_LENGTH = 30`) 단위 창으로 로그 멜 스펙트로그램을 만들어 디코딩한다.
입력 끝에는 30초 분량의 무음을 덧붙여 자르기 쉽게 하고,
언어를 지정하지 않으면 처음 30초로 언어를 감지한다.

긴 파일은 창을 하나씩 밀면서 처리한다.
`condition_on_previous_text`가 켜져 있으면 앞 창의 결과를 다음 창의 프롬프트로
넣어 문맥을 이어 가는데,
이것이 반복 환각을 퍼뜨리는 통로도 된다.

### 실패한 디코딩은 온도를 올려 다시 시도한다

Whisper는 디코딩 결과가 이상하면 다시 시도하는 장치를 갖고 있다.
gzip 압축률이 `compression_ratio_threshold`(기본 2.4)보다 높으면
같은 말이 반복된 것으로 보고,
평균 로그 확률이 `logprob_threshold`(기본 -1.0)보다 낮으면 실패로 본다.
이때 더 높은 온도로 다시 샘플링한다.
`no_speech_threshold`(기본 0.6)는 무음 확률이 높은 구간을 건너뛰는 데 쓴다.

### 모델은 Hugging Face에서 바로 받거나 직접 변환한다

`path_or_hf_repo`(CLI에서는 `--model`)에 로컬 경로나 Hugging Face 저장소를
주면 된다.
MLX Community 조직에 미리 변환된 Whisper 모델 모음이 있고,
지정하면 자동으로 내려받는다.
직접 변환하려면 저장소를 클론해 `convert.py`를 돌리며,
`-q`로 4비트 양자화 모델을 만들 수 있다.
변환 결과는 `weights.npz`와 `config.json`으로 저장된다.

## 사용법

### CLI

```bash
pip install mlx-whisper
brew install ffmpeg

# 가장 단순한 형태: audio_file.txt가 생긴다
mlx_whisper audio_file.mp3

# 모델, 언어, 출력 형식을 지정한다
mlx_whisper lecture.wav \
  --model mlx-community/whisper-large-v3-turbo \
  --language ko \
  --output-format all \
  --output-dir subs \
  --condition-on-previous-text False

# 다른 프로그램의 출력을 stdin으로 받을 수도 있다. 기본 출력 이름은 content.*
ffmpeg -i video.mkv -f wav - | mlx_whisper - --output-name lecture
```

`--output-format`은 `txt`, `vtt`, `srt`, `tsv`, `json`, `all` 중 하나다.

### Python API

```python
import mlx_whisper

result = mlx_whisper.transcribe(
    "lecture.wav",
    path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
    language="ko",
    # 단어 단위 타임스탬프. 무음 환각 억제 옵션도 이것이 켜져 있어야 동작한다
    word_timestamps=True,
    hallucination_silence_threshold=2.0,
)
print(result["text"][:200])
print(result["segments"][0]["words"][:5])
```

### 모델 변환

```bash
git clone https://github.com/ml-explore/mlx-examples.git
cd mlx-examples/whisper

# convert.py는 같은 경로의 모델을 덮어쓴다. 변형마다 경로를 따로 준다
python convert.py --torch-name-or-path tiny --mlx-path mlx_models/tiny_fp16
python convert.py --torch-name-or-path tiny -q --q_bits 4 \
  --mlx-path mlx_models/tiny_q4
```

## 값 정하기

| 값                                  | 시작값                    | 근거                                                                       |
| ----------------------------------- | ------------------------- | -------------------------------------------------------------------------- |
| 모델                                | `whisper-large-v3-turbo`  | 대형 모델 수준의 정확도에 속도가 빠르다. 5시간 음성이 약 10분              |
| `--language`                        | 언어를 명시               | 자동 감지는 처음 30초만 본다. 인트로가 무음이거나 음악이면 틀린다          |
| `--condition-on-previous-text`      | `False`(긴 녹음)          | 한 번 틀린 문장이 다음 창으로 번지는 것을 막는다                           |
| `--word-timestamps`                 | 무음이 긴 녹음이면 `True` | `--hallucination-silence-threshold`가 이것을 요구한다                      |
| `--hallucination-silence-threshold` | 2초 안팎에서 시작         | 이보다 긴 무음에서 환각 의심 구간을 건너뛴다                               |
| `--fp16`                            | 기본 `True`               | 반복이 심하면 `False`로 비교한다. 관리자는 fp16이 약간 나쁠 수 있다고 했다 |

`--hallucination-silence-threshold`의 2초는 저장소가 권하는 값이 아니라
출발점이다.
결과 자막에서 무음 구간의 환각이 남는지,
실제 짧은 발화가 잘려 나가는지를 보며 조정한다.

## 함정

### CLI와 Python API의 기본값이 다르다

코드를 읽으면 같은 이름의 옵션도 진입점마다 기본값이 다르다.

| 항목      | CLI(`cli.py`)                     | Python API(`transcribe.py`)           |
| --------- | --------------------------------- | ------------------------------------- |
| 기본 모델 | `mlx-community/whisper-tiny`      | `mlx-community/whisper-turbo`         |
| 온도      | `--temperature` 기본 `0`(값 하나) | `(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)` 튜플 |

README는 기본 모델을 `whisper-tiny`라고 적지만 그것은 CLI 기준이고,
Python API를 모델 인자 없이 부르면 turbo 모델을 받는다.
더 중요한 차이는 온도다.
API는 디코딩이 실패하면 온도를 단계적으로 올려 다시 시도하지만,
CLI의 `--temperature`는 값 하나만 받으므로 기본 상태에서는 다시 시도할 높은
온도가 없다.
압축률 검사로 반복을 감지해도 대안을 샘플링할 여지가 줄어든다는 뜻이다.
CLI에서 반복이 심하면 API로 옮겨 튜플 온도를 쓰는 것을 비교해 볼 만하다.

### 무음에서 같은 문장을 지어낸다

5시간 강의 자막에서는 방송 시작 전과 끝난 뒤의 무음 구간에
“다음 영상에서 만나요.”가 26번 반복되어 들어갔다.
같은 현상은 저장소 이슈에도 반복해서 올라온다.
[#774 「Whisper stutters」](https://github.com/ml-explore/mlx-examples/issues/774)에서는
대화 녹음 중간에 “Yes.”가 수십 번 이어졌고,
관리자 awni는 인코더-디코더 모델에 흔한 반복 문제이며 고품질 모델에서는
드물어지고 경계 사례 입력에서 잘 일어난다고 답했다.
[#1402](https://github.com/ml-explore/mlx-examples/issues/1402)에서는 진폭이
계속 0인 구간에서 “you”가 여러 번 전사됐다.

[#1427](https://github.com/ml-explore/mlx-examples/issues/1427)은
원인 하나를 코드 수준에서 짚는다.
upstream `openai/whisper`는 무음 확률이 높고 평균 로그 확률도 낮을 때만
재시도를 끄는데,
mlx-whisper는 조건이 더 넓어 무음 확률만으로 재시도를 꺼 버린다는 것이다.
2026년 10월 기준 이 이슈와 관련 PR은 열려 있다.

### `--output-name`의 마지막 점 뒤는 확장자로 취급된다

`--output-name "제목.ko"`로 주면 `.ko`가 사라지고 `제목.srt`가 만들어진다.
`writers.py`가 경로를 `(output_dir / output_name).with_suffix(".srt")`로 만들기
때문이다.
`pathlib`의 `with_suffix`는 마지막 확장자를 바꾸므로 `.ko`가 `.srt`로
대체된다.
언어 코드가 필요하면 인식이 끝난 뒤 이름을 바꾼다.

### 여러 파일을 한 번에 주면 첫 파일 이름으로 덮어쓴다

[#1441](https://github.com/ml-explore/mlx-examples/issues/1441)에 따르면
`mlx_whisper a.mp3 b.mp3`처럼 여러 파일을 넘기면 모든 결과가 `a.txt`에
차례로 덮어써진다.
`cli.py`가 첫 반복에서 `output_name`을 정한 뒤 다음 파일에서도 그 값을 그대로
쓰기 때문이다.
파일마다 따로 실행한다.

### 아주 긴 파일은 메모리가 부족할 수 있다

[#1366](https://github.com/ml-explore/mlx-examples/issues/1366)에서는 21시간짜리
오디오북(1.2GB m4a)이 GPU 메모리 부족으로 실패했다.
awni는 긴 오디오의 로그 멜 스펙트로그램 계산이 메모리를 많이 쓴다고 설명했고,
파일을 나누면 동작했다.
5시간 강의(16kHz 모노 WAV 약 580MB)는 24GB 메모리에서 문제없었다.

## 확인하기

```bash
# 자막 개수와 첫·끝 자막을 본다. 앞뒤 무음 구간에 같은 문장이 반복되면 환각이다
grep -c -- "-->" subs/lecture.srt
head -20 subs/lecture.srt
tail -20 subs/lecture.srt

# 같은 문장이 몇 번 나오는지 센다
grep -v -- "-->" subs/lecture.srt | grep -v "^[0-9]*$" | sort | uniq -c | sort -rn | head
```

## 비평

### “Apple Silicon에서 빠르다”는 비교 대상에 따라 뜻이 달라진다

MLX Whisper가 처음 화제가 된 것은 2023년 12월 RTX 4090과 M1 Pro를 비교한
블로그 글이었다.
HN에서 modeless는 같은 10분 파일을 4090에서 insanely-fast-whisper로 돌리면
8초 안에 끝나 Apple 쪽보다 6~12배 빠르다고 반박했고,[^modeless]
글쓴이 owehrens도 직접 돌려 본 뒤 “Nvidia가 왕”이라며 글을 고쳤다.[^owehrens]
woadwarrior01은 whisper.cpp가 가장 빠른 구현도 아니니 PyTorch 대 MLX처럼
비교해야 공정하다고 지적했다.[^woadwarrior01]

반대로 jdminhbg는 MLX 구현이 손으로 최적화한 CUDA 구현이 아니라,
PyTorch로 CUDA를 쓰듯 MLX API를 쓴 것뿐이라고 짚었다.[^jdminhbg]
stefan_은 Whisper에는 같은 품질에서 한두 자릿수 빠른 구현이 여럿 있으니,
같은 소프트웨어와 모델이 아니면 성능 직관을 믿지 말라고 했다.[^stefan_]
mlx-whisper의 가치는 최고 속도가 아니라,
Mac 한 대에서 별도 GPU 없이 대형 모델을 실용적인 속도로 돌린다는 데 있다.

### 예제 저장소라는 위치가 품질 기대치를 정한다

mlx-whisper는 독립 프로젝트가 아니라 `mlx-examples` 안의 예제다.
README가 짧고, CLI와 API 기본값이 어긋나고,
출력 이름 버그와 무음 재시도 조건 차이가 열린 이슈로 남아 있는 것도
그 위치와 맞닿아 있다.
Lightning Whisper MLX처럼 이를 바탕으로 속도를 더 끌어올린 파생 구현도 나왔지만,
HN에서 asdlkj178은 빔 서치를 끄면 Whisper 논문이 말한 긴 음성의 전사 품질이
떨어지지 않느냐고 물었다.[^asdlkj178]
mlx-whisper의 빔 서치 디코딩 역시 2026년 10월 기준 열린 PR(#1439)로만 있다.

## 기억할 원칙

### 음성 인식 결과는 앞뒤 무음 구간부터 의심한다

Whisper 계열은 소리가 없을 때 학습 데이터에 흔한 문장을 만들어 낸다.
방송 시작 전 대기 화면, 끝난 뒤의 엔딩, 녹음 중간의 긴 침묵이 모두 위험하다.
결과를 받으면 가장 먼저 자막의 앞과 끝, 그리고 가장 많이 반복된 문장을 본다.
이 검사는 1분이면 끝나고, 가장 눈에 띄는 오류를 대부분 잡아낸다.

---

[^modeless]: <https://news.ycombinator.com/item?id=38629951>

[^owehrens]: <https://news.ycombinator.com/item?id=38633250>

[^woadwarrior01]: <https://news.ycombinator.com/item?id=38632305>

[^jdminhbg]: <https://news.ycombinator.com/item?id=38631326>

[^stefan_]: <https://news.ycombinator.com/item?id=38631691>

[^asdlkj178]: <https://news.ycombinator.com/item?id=39913386>
