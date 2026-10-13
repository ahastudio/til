# YouTube 영상을 받아 압축하고 자막 달기

## 소개

5시간짜리 YouTube 강의 영상(라이브 방송 다시보기)을 받아 MKV와 MP4로 저장하고,
YouTube에 자막이 없어서 음성 인식으로 한국어 자막을 만든 뒤,
자막을 정리한 과정을 정리한다.
명령과 숫자는 모두 2026년 10월, Apple M4 Pro(메모리 24GB) macOS에서 실제로
돌린 결과다.

쓴 도구는 넷이다.

| 도구                                              | 버전       | 역할                                     |
| ------------------------------------------------- | ---------- | ---------------------------------------- |
| [yt-dlp](../cli/yt-dlp.md)                        | 2026.10.10 | 영상·음성 스트림 다운로드                |
| [ffmpeg](ffmpeg.md)                               | 9.0.2      | 병합, 재인코딩, 음성 추출                |
| [mlx-whisper](../machine-learning/mlx-whisper.md) | 0.4.3      | Apple Silicon GPU로 음성 인식, 자막 생성 |
| [deno](../deno/README.md)                         | 2.9.7      | yt-dlp의 YouTube JS 챌린지 풀이          |

받는 영상은 본인이 볼 권한이 있는 것이어야 하고,
만든 파일과 자막은 개인 시청용으로만 쓴다는 전제다.
재배포는 별개의 문제다.

## 동작 방식

### YouTube는 영상과 음성을 따로 준다

YouTube의 고화질 스트림은 DASH 방식이라 영상만 있는 포맷과 음성만 있는
포맷이 따로 있다.
`yt-dlp -F`로 보면 1080p는 모두 `video only`이고 음성은 `audio only`다.
그래서 1080p를 받으려면 영상 하나, 음성 하나를 받아 ffmpeg로 합쳐야 한다.
ffmpeg가 없으면 yt-dlp는 합치지 못하고, 영상과 음성이 함께 든 낮은 화질의
단일 포맷만 쓸 수 있다.

이번 영상의 1080p 포맷은 두 가지였다.

| ID  | 컨테이너 | 코덱  | 비트레이트 | yt-dlp 예상 크기 | 실제 크기 |
| --- | -------- | ----- | ---------- | ---------------- | --------- |
| 137 | mp4      | H.264 | 4200k      | 약 8.88GiB       | 받지 않음 |
| 248 | webm     | VP9   | 1402k      | 약 2.96GiB       | 1.20GiB   |
| 140 | m4a      | AAC   | 144k       | 약 311MiB        | -         |

VP9 포맷이 같은 해상도에서 H.264보다 훨씬 작다.
`bv*[height<=1080]+ba` 같은 포맷 선택식을 쓰면 yt-dlp가 기본 정렬에 따라
VP9을 고른다.
라이브 다시보기는 예상 크기가 실제와 크게 다를 수 있다.

### JS 런타임이 없으면 포맷이 빠진다

최근 yt-dlp는 YouTube의 JavaScript 챌린지를 풀기 위해 외부 JS 런타임을
쓴다.
런타임이 없으면 “No supported JavaScript runtime could be found”라는 경고와
함께 일부 포맷이 빠진다.
기본으로 켜진 런타임은 deno이므로 deno를 설치하면 된다.
설치 후에는 로그에 `Solving JS challenges using deno`가 찍힌다.

### 왜 MKV에서 MP4로 다시 인코딩하는가

VP9 영상과 AAC 음성은 MKV에 손실 없이 그대로 담을 수 있다(`-c copy`).
MP4에도 VP9을 넣을 수는 있지만,
QuickTime Player 같은 기본 플레이어에서 재생이 안 될 수 있다.
어디서나 재생되는 MP4를 원하면 영상을 H.264나 H.265로 다시 인코딩해야 한다.
이 단계에서 용량과 시간이 크게 갈린다.

## 설치하기

```bash
# yt-dlp는 오래되면 YouTube 변경을 따라가지 못한다. 최신으로 유지한다
pip install -U --pre "yt-dlp[default]"

# 병합·변환용 ffmpeg, JS 챌린지용 deno
brew install ffmpeg deno

# 음성 인식은 별도 가상환경에 둔다
python3 -m venv ~/venvs/whisper
~/venvs/whisper/bin/pip install mlx-whisper
```

## 다운로드하기

### 포맷과 메타데이터 확인

```bash
URL="https://www.youtube.com/watch?v=VIDEO_ID"
yt-dlp -F "$URL"
yt-dlp --print "%(title)s | %(duration_string)s | %(uploader)s" "$URL"
```

### 재시도까지 포함한 다운로드

```bash
cd ~/Downloads/yt
for i in $(seq 1 30); do
  # 병합된 결과물이 생겼으면 끝
  ls *"[VIDEO_ID]".mkv >/dev/null 2>&1 && break
  # --fragment-retries를 무한으로 두지 않는다.
  # 만료된 URL로 같은 조각을 영원히 다시 받는 대신
  # yt-dlp가 종료되어 다음 반복에서 새 URL을 뽑게 한다.
  yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mkv \
    --retries 10 --fragment-retries 10 --continue \
    --concurrent-fragments 4 \
    --write-subs --write-auto-subs --sub-langs "ko.*" \
    --newline -o "%(title)s [%(id)s].%(ext)s" "$URL" > dl.log 2>&1
  sleep 15
done
```

`--continue`가 있으면 이미 받은 조각과 다 받은 스트림은 건너뛴다.
`--write-subs --write-auto-subs`는 업로더 자막과 자동 생성 자막을 함께
요청하는데,
이번 영상은 둘 다 없어서 “There are no subtitles for the requested
languages”가 나왔다.
`--write-info-json`을 붙이면 메타데이터가 저장되는데,
5시간 라이브 다시보기에서는 이 파일만 약 156MB였다.

### 음성 스트림이 401로 막힐 때

이번 다운로드에서 영상(1.2GiB)은 약 5분 만에 끝났지만,
음성 스트림은 받는 도중 `HTTP Error 401: Unauthorized`가 수십만 번 반복됐다.
`--fragment-retries infinite`로 걸어 두었더니 yt-dlp가 끝나지 않고 같은
조각을 계속 다시 시도했다.
`--extractor-args "youtube:player_client=tv,web_safari"`로
다른 플레이어 클라이언트를 쓰면 “This live event has ended” 오류가 났다.

통한 방법은 음성만 따로, 연결 하나로 받는 것이었다.

```bash
# 꼬인 조각 파일을 지우고 음성 포맷만 단일 연결로 다시 받는다
rm -f *"[VIDEO_ID]".f140.m4a.part *"[VIDEO_ID]".f140.m4a.ytdl
for i in $(seq 1 10); do
  yt-dlp -f 140 --concurrent-fragments 1 --fragment-retries 5 --continue \
    --newline -o "%(title)s [%(id)s].f140.%(ext)s" "$URL" > audio-dl.log 2>&1 \
    && break
  sleep 20
done
```

### 직접 병합하기

영상과 음성을 따로 받았으면 ffmpeg로 합친다.
다시 인코딩하지 않으므로 몇 초면 끝난다.

```bash
B="제목 [VIDEO_ID]"
ffmpeg -i "$B.f248.webm" -i "$B.f140.m4a" \
  -map 0:v:0 -map 1:a:0 -c copy "$B.mkv"
```

결과는 VP9 1080p + AAC, 5:02:13(18,133초), 1.58GB였다.

## 변환하고 압축하기

### 첫 시도는 왜 9.4GB가 됐나

처음에는 Mac의 하드웨어 인코더로 비트레이트를 4Mbps로 고정해 변환했다.

```bash
ffmpeg -i "$B.mkv" -c:v h264_videotoolbox -b:v 4M -profile:v high \
  -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$B.mp4"
```

속도는 약 7.9배속이라 5시간 영상이 40분 안에 끝났지만,
결과는 9.4GB였다.
원본 VP9가 0.5~0.7Mbps 수준인데 그보다 6배 넘는 비트레이트를 강제했기
때문이다.
화면 공유 위주의 강의는 화면이 거의 움직이지 않아서 적은 비트로도 충분하다.
고정 비트레이트는 이런 영상에 낭비다.

### 5분 구간으로 설정을 비교한다

전체를 여러 번 인코딩하기 전에 5분 구간을 잘라 설정별로 비교했다.

```bash
ffmpeg -ss 01:30:00 -t 300 -i "$B.mkv" -c copy clip.mkv

# H.264, 품질 고정(CRF)
ffmpeg -i clip.mkv -c:v libx264 -preset slow -crf 23 \
  -c:a aac -b:a 96k x264.mp4

# H.265, 품질 고정. hvc1 태그가 있어야 Apple 기기에서 재생된다
ffmpeg -i clip.mkv -c:v libx265 -preset medium -crf 26 -tag:v hvc1 \
  -c:a aac -b:a 96k x265.mp4

# H.265 하드웨어 인코더, 품질 모드
ffmpeg -i clip.mkv -c:v hevc_videotoolbox -q:v 50 -tag:v hvc1 \
  -c:a aac -b:a 96k vt.mp4

# 해상도 720p, 프레임 15fps로 낮춘 H.264
ffmpeg -i clip.mkv -vf scale=-2:720,fps=15 -c:v libx264 -preset slow -crf 23 \
  -c:a aac -b:a 96k x264-720p15.mp4
```

### 측정 결과

5분 구간 크기를 5시간(18,133초)으로 비례 환산한 값이다.

| 설정                           | 5분 크기 | 5시간 환산  | 5분 인코딩 시간 | 비고                           |
| ------------------------------ | -------- | ----------- | --------------- | ------------------------------ |
| 원본 MKV(VP9, 복사)            | 25.1MB   | 약 1.52GB   | -               | 기준                           |
| `h264_videotoolbox` 4Mbps 고정 | -        | 9.4GB(실측) | 약 7.9배속      | 첫 시도, 낭비가 큼             |
| `hevc_videotoolbox` `-q:v 50`  | 42.8MB   | 약 2.59GB   | 40초            | 하드웨어 인코더는 품질 대비 큼 |
| `libx264` `slow` CRF 23        | 19.1MB   | 약 1.15GB   | 23초            | 최종 선택, 전체 실측 1.46GB    |
| `libx265` `medium` CRF 26      | 13.3MB   | 약 0.80GB   | 99초            | 가장 작지만 4배 느림           |
| `libx264` CRF 23, 720p, 15fps  | 10.2MB   | 약 0.62GB   | 9초             | 작은 글씨가 흐려질 수 있음     |

최종 선택은 1080p·30fps를 유지한 `libx264 -preset slow -crf 23`이다.

```bash
ffmpeg -i "$B.mkv" -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart "$B.mp4"
```

전체 인코딩 결과는 1.46GB였다.
5분 구간으로 환산한 1.15GB보다 약 27% 큰데,
표본으로 고른 구간보다 화면 변화가 많은 구간이 다른 곳에 있었기 때문이다.
속도는 구간에 따라 약 5.8배속에서 13배속까지 오갔다.
표본 하나로 낸 환산값은 방향을 정하는 데 쓰고, 정확한 크기로 믿지는 않는다.

## 값 정하기

| 값                     | 시작값           | 근거                                                            |
| ---------------------- | ---------------- | --------------------------------------------------------------- |
| 코덱                   | H.264(`libx264`) | 거의 모든 기기와 브라우저에서 재생된다                          |
| 품질                   | CRF 23           | x264 기본값. 화면 속 코드 글씨가 읽힌다. 낮을수록 고화질·대용량 |
| preset                 | `slow`           | 같은 CRF에서 `medium`보다 작다. 5시간 영상도 1시간 안쪽         |
| 해상도·프레임          | 원본 유지        | 화면 공유 강의는 글씨 가독성이 중요하다                         |
| 음성                   | AAC 128k         | 말소리 위주라 충분하다                                          |
| `-movflags +faststart` | 항상             | 메타데이터를 앞에 두어 다 받기 전에도 재생이 시작된다           |

CRF를 바꿀 때는 5분 구간에서 결과물을 직접 열어 화면 속 가장 작은 글씨를
확인한다.
글씨가 뭉개지면 CRF를 2씩 낮추고, 충분히 선명하면 2씩 올린다.

## 자막 만들기

### 음성 추출과 인식

```bash
# Whisper는 16kHz 모노를 쓴다. 5시간이면 약 580MB WAV가 된다
ffmpeg -i "$B.mkv" -vn -ac 1 -ar 16000 audio.wav

~/venvs/whisper/bin/mlx_whisper audio.wav \
  --model mlx-community/whisper-large-v3-turbo \
  --language ko \
  --output-format all \
  --output-dir subs \
  --output-name "$B" \
  --condition-on-previous-text False
```

M4 Pro에서 5시간 음성이 약 10분 만에 끝났고, 자막 5,268개가 나왔다.
`--output-format all`은 `srt`, `vtt`, `txt`, `tsv`, `json`을 모두 만든다.
`--condition-on-previous-text False`는 앞 문장을 다음 인식의 힌트로 쓰지 않게
해서,
한 번 틀린 문장이 같은 패턴으로 계속 반복되는 현상을 줄인다.

### 결과를 영상 옆에 두기

플레이어가 자막을 자동으로 찾게 하려면 영상과 같은 이름에 언어 코드를 붙인다.

```bash
cp "subs/$B.srt" "$B.ko.srt"
cp "subs/$B.vtt" "$B.ko.vtt"
```

## 자막 정리하기

### 1단계: 무음 구간의 환각 줄 지우기

Whisper는 소리가 없는 구간에서 학습 데이터에 흔한 문장을 지어낸다.
이번 자막에는 방송 시작 전과 끝난 뒤의 무음 구간에 “다음 영상에서 만나요.”가
26번 들어 있었다.
앞뒤 끝에서 이어지는 환각 문장만 지우고 번호를 다시 매기는 스크립트다.

```python
# clean_srt.py: 앞뒤 무음 구간의 환각 자막을 지우고 번호를 다시 매긴다
import sys

HALLUCINATIONS = {"다음 영상에서 만나요."}


def load(path):
    blocks = [b for b in open(path, encoding="utf-8").read().strip().split("\n\n") if b.strip()]
    cues = []
    for block in blocks:
        lines = block.split("\n")
        cues.append((lines[1], "\n".join(lines[2:])))
    return cues


def trim(cues):
    start, end = 0, len(cues)
    # 본문 중간의 같은 문장은 실제 발화일 수 있으므로 앞뒤 끝만 자른다
    while start < end and cues[start][1].strip() in HALLUCINATIONS:
        start += 1
    while end > start and cues[end - 1][1].strip() in HALLUCINATIONS:
        end -= 1
    return cues[start:end]


def save(cues, path):
    with open(path, "w", encoding="utf-8") as f:
        for n, (timing, text) in enumerate(cues, 1):
            f.write(f"{n}\n{timing}\n{text}\n\n")


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    cues = load(src)
    kept = trim(cues)
    save(kept, dst)
    print(f"{len(cues)} -> {len(kept)}")
```

```bash
python3 clean_srt.py "$B.ko.srt" "$B.ko.cleaned.srt"
```

이번 영상에서는 앞쪽의 마이크 테스트 줄(“1, 2, 3, 2, 3, 2, 1”)까지 손으로
목록에 더해 지웠고, 5,268개가 5,241개가 됐다.

### 2단계: 용어 바로잡기

음성 인식은 일반 문장보다 제품 이름과 영어 약어에서 많이 틀린다.
바이브 코딩 강의라면 Claude, Codex, Vercel, Supabase, PRD, MVP 같은 말이
특히 그렇다.
먼저 자주 나오는 영어 토큰과 한글로 적힌 제품명을 세어 의심 목록을 만든다.

```python
# terms.py: 자막에서 영어 토큰과 한글 제품명 후보의 빈도를 센다
import collections
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
lines = [l for l in text.split("\n") if l and "-->" not in l and not l.isdigit()]

english = collections.Counter(w for l in lines for w in re.findall(r"[A-Za-z]+", l))
print(english.most_common(80))

for word in ["클로드", "코덱스", "버셀", "수파베이스", "커서", "깃허브"]:
    print(word, sum(l.count(word) for l in lines))
```

틀린 표기와 바른 표기를 표로 정리한 뒤 일괄 치환한다.
치환은 자막 텍스트 줄에만 적용하고, 번호 줄과 타임코드 줄은 건드리지 않는다.

### 3단계: 문장 단위 교정은 형식을 고정한 채로 한다

문맥을 보고 문장을 고치는 일은 LLM에게 맡길 수 있지만,
5천 개가 넘는 자막을 한 번에 넘기면 번호나 타임코드가 바뀌거나 줄이 합쳐진다.
안전하게 하려면 세 가지를 지킨다.

1. 자막을 수백 개 단위로 나눠 넘기고, 번호와 타임코드는 그대로 두고 텍스트만
   고치라고 명시한다.
2. 뜻을 바꾸지 말고 오인식, 띄어쓰기, 용어만 고치라고 범위를 정한다.
3. 결과를 합친 뒤 아래 검사 스크립트로 원본과 구조를 비교한다.

```python
# verify_srt.py: 교정본이 원본과 같은 번호·타임코드 구조인지 확인한다
import sys


def cues(path):
    blocks = [b for b in open(path, encoding="utf-8").read().strip().split("\n\n") if b.strip()]
    return [(b.split("\n")[0], b.split("\n")[1]) for b in blocks]


a, b = cues(sys.argv[1]), cues(sys.argv[2])
assert len(a) == len(b), f"자막 개수가 다르다: {len(a)} != {len(b)}"
for i, (x, y) in enumerate(zip(a, b), 1):
    assert x == y, f"{i}번째 자막의 번호나 타임코드가 바뀌었다: {x} != {y}"
print("OK", len(a))
```

```bash
python3 verify_srt.py "$B.ko.cleaned.srt" "$B.ko.polished.srt"
```

## 함정

### 무한 재시도는 실패를 숨긴다

`--retries infinite --fragment-retries infinite`는 끊김에 강해 보이지만,
URL이 만료되어 401이 나는 경우에는 영원히 같은 조각을 다시 요청할 뿐이다.
yt-dlp가 종료되지 않으니 바깥의 재시도 루프도 돌지 않는다.
재시도 횟수를 유한하게 두어 yt-dlp가 실패로 끝나고,
바깥 루프가 새로 실행하면서 새 URL을 받게 해야 한다.

### 프로세스 존재로 완료를 판단하면 경쟁 상태가 생긴다

처음에는 `pgrep -f "yt-dlp.*VIDEO_ID"`가 사라지면 다운로드가 끝났다고 보고
변환을 시작하게 했다.
그런데 재시도 루프에는 반복 사이에 `sleep`이 있어서,
그 몇 초 동안 yt-dlp 프로세스가 없으면 변환 단계가 너무 일찍 시작된다.
완료 판단은 프로세스가 아니라 결과 파일(`.mkv`)이 있는지로 한다.

### zsh에서는 매치되지 않는 glob이 오류다

zsh는 `ls *"[ID]".mkv`가 아무것도 매치하지 않으면 명령을 실행하지 않고
“no matches found” 오류를 낸다.
파일 존재 검사에 glob을 쓸 때는 `2>/dev/null`로 오류를 숨기거나
`setopt nullglob`을 쓴다.

### macOS에는 `timeout`이 없다

`timeout 300 yt-dlp ...`는 macOS 기본 셸에서 “command not found”로 실패한다.
`brew install coreutils`의 `gtimeout`을 쓰거나,
백그라운드 실행과 재시도 루프로 대신한다.

### mlx-whisper는 출력 이름의 마지막 점 뒤를 지운다

`--output-name "제목.ko"`로 주면 `.ko`를 확장자로 보고 지워서 `제목.srt`가
만들어진다.
출력 경로를 `pathlib`의 `with_suffix()`로 만들기 때문이다.
무음 구간의 환각은 `--word-timestamps True`와 함께
`--hallucination-silence-threshold`를 주면 줄일 수 있다.
언어 코드는 인식이 끝난 뒤 복사하면서 붙인다.

### 하드웨어 인코더는 빠르지만 크다

`h264_videotoolbox`와 `hevc_videotoolbox`는 소프트웨어 인코더보다 빠르지만,
같은 화질에서 파일이 훨씬 크다.
이번 측정에서 `hevc_videotoolbox`(H.265)가 `libx264`(H.264) CRF 23보다
2배 넘게 컸다.
보관용이면 시간이 더 걸려도 소프트웨어 인코더를 쓴다.

## 확인하기

```bash
# 재생 길이, 코덱, 해상도, 크기를 원본과 비교한다
for f in "$B.mkv" "$B.mp4"; do
  ffprobe -v error \
    -show_entries format=duration,size \
    -show_entries stream=codec_name,width,height \
    -of compact "$f"
done

# 자막 개수를 확인한다
grep -c -- "-->" "$B.ko.srt"
```

이번 결과에서 MKV와 MP4는 둘 다 길이 18,133.02초, 1920×1080이었다.

## 체크리스트

- yt-dlp를 최신으로 올렸는가?
- deno 같은 JS 런타임이 설치되어 있는가?
- ffmpeg가 설치되어 있는가?
- `--fragment-retries`가 유한한 값인가?
- 완료 판단을 결과 파일 존재로 하는가?
- 재인코딩 설정을 5분 구간으로 먼저 비교했는가?
- MP4에 `-movflags +faststart`를 넣었는가?
- 자막 파일 이름이 영상 이름과 같고 언어 코드가 붙어 있는가?
- 자막 앞뒤 무음 구간의 환각 줄을 지웠는가?
- 교정한 자막의 번호와 타임코드가 원본과 같은지 검사했는가?

## 기억할 원칙

### 고정 비트레이트보다 고정 품질을 쓴다

강의 영상은 화면 변화가 적은 구간이 대부분이라,
같은 비트레이트를 모든 구간에 배분하면 정지 화면에 비트를 낭비한다.
CRF처럼 품질을 고정하면 인코더가 움직임이 많은 구간에만 비트를 쓴다.
이번 영상에서 그 차이는 9.4GB와 약 1.2GB였다.

### 긴 작업은 작은 표본으로 먼저 잰다

5시간 영상을 설정마다 전부 인코딩하면 몇 시간이 날아간다.
5분 구간 하나로 네 가지 설정을 비교하는 데는 3분이면 충분했고,
환산 결과가 최종 선택을 바로 결정했다.
다운로드, 인코딩, 음성 인식 모두 같은 원칙이 통한다.
