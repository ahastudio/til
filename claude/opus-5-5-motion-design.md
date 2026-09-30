# Opus 5.5로 모션 디자인 스튜디오 만들기: 프롬프트는 10%, 하네스가 90%

트윗: [How to build motion design studio with Opus 5.5 ( Full-course )](https://twitter.com/0xmovez/status/2104216919033192746)

## 소개

Movez(@0xMovez)가 2026년 9월 27일 Twitter 아티클로 올린 12단계 강좌다.
Claude Opus 5.5가 9월 22일 나온 뒤 타임라인은 쇼릴, 출시 영상, 뮤직비디오, 5분짜리 역사 영화로 가득 찼는데, 모두 코드로 렌더링한 것이었다.
캡션은 “프롬프트 하나”라고 했고, 답글은 모션 디자이너는 끝났다고 했다.
저자는 둘 다 반만 맞다고 본다.
어떤 영상은 정말 30단어 프롬프트에서 나왔지만, 어떤 영상은 9,500자짜리 감독 지시서와 스킬 폴더, API 키 두 개, 12시간의 자율 실행에서 나왔다.
Claude Code 팀의 Thariq가 이 간극을 한 줄로 요약했다고 인용한다.
게시물은 원샷이라고 하지만 프롬프트는 스킬, 예제, 키까지 딸린 1만 자라는 것이다.

글의 약속은 제목 그대로다.
대부분의 사람이 Opus 5.5로 모션 디자인을 시도하면 그라디언트 위의 가운데 정렬 텍스트, 전부 페이드인, 마지막에 로고라는 똑같은 영상을 얻는다.
참조도 렌더 엔진도 주지 않고, 자기 프레임을 보라고 하지도 않기 때문이다.
저자는 이것을 반복 가능한 스튜디오 파이프라인으로 바꾸는 12단계를 제시하며, 프롬프트는 영상의 10%이고 나머지 90%는 하네스라고 말한다.

강좌는 네 부분이다.
1부는 실제로 무슨 일이 일어나는지와 설치, 2부는 감독처럼 프롬프트를 쓰는 법(한 줄 프롬프트, 브랜드, 참조, 명세), 3부는 엔진 구현(`seek(t)` 렌더러, 스프링, 사운드), 4부는 한 클립에서 스튜디오로 가는 법(감독 지시서, 비평 루프, 출시)이다.
트렌드를 만든 게시물 9개를 인용하며 각각의 프롬프트 패턴을 보여 준다.
이 노트는 그 가운데 재현 가능한 부분, 곧 렌더링 원리와 하네스 구성, 비평 루프를 중심으로 정리한다.

## 동작 방식

### 모델은 영상이 아니라 프로그램을 쓴다

Opus 5.5는 텍스트와 이미지를 받아 텍스트를 내놓는다.
MP4를 만들 수 없다.
이 트렌드의 모든 영상은 Opus가 쓴 프로그램이고, 그 프로그램을 프레임으로 바꾼 것은 다른 도구다.

핵심은 결정론이다.
Opus는 임의의 시각에 해당하는 정확한 프레임을 그리는 함수 하나, `draw(t)`나 `seek(t)`를 쓴다.
헤드리스 브라우저가 60fps 15초 영상이면 이 함수를 900번 부르고, 매번 스크린숏을 찍고, ffmpeg가 이어 붙인다.
타이머에 의존하는 것이 없으므로 렌더링은 매번 같고, 수정은 한 줄 편집과 재렌더링이다.

저자가 인용한 Tommy D. Rossi의 분석에 따르면 Opus는 기본적으로 의존성이 없는 경로를 고른다.
`index.html` 하나에 `seek` 함수를 두고, Playwright로 프레임마다 캡처하고, ffmpeg로 인코딩하는 방식이다.
Remotion이나 HyperFrames가 설치되어 있어도 쓰지 않았으므로, 프레임워크를 원하면 명시해야 한다.
저자는 이 기본 경로를 A, 프레임워크를 쓰는 경로를 B로 부른다.

### 피드백 루프가 결과를 가른다

채팅 앱도 애니메이션 코드는 쓸 수 있다.
하지만 렌더링하고, 소리를 듣고, 자기가 만든 프레임을 볼 수 있는 것은 셸을 가진 에이전트, 곧 Claude Code 같은 도구뿐이다.
저자는 이 피드백 루프가 사람들이 불평하는 밋밋한 첫 시도와 입소문 난 영상의 차이 전부라고 말한다.

루프는 이렇게 돈다.
에이전트가 코드를 쓰고, 렌더링하고, 비트마다 한 프레임씩 모은 밀착 인화(contact sheet)를 만들고, 그 이미지를 직접 본다.
정해진 기준으로 점수를 매기고, 가장 나쁜 문제 세 개를 고치고, 모든 점수가 8점 이상이 될 때까지 반복한다.
Opus 5.5가 이미지를 읽을 수 있다는 사실이 이 루프를 가능하게 한다.

### 한 줄 프롬프트에서 감독 지시서까지

글은 입력의 수준을 사다리처럼 제시한다.
가장 아래는 네 개의 게시물이 공통으로 쓴 한 문장, 곧 이력서용 쇼릴처럼 모션 디자이너로서 실력을 보여 주는 15초 영상을 만들라는 프롬프트다.
장르가 정해져 있고, 모델 자신이 주인공이라 틀릴 내용이 없으며, 한 번에 끝낼 만큼 짧다는 것이 이 프롬프트가 통하는 이유라고 분석한다.
하지만 수백 개의 똑같은 프롬프트가 서로 닮은 릴을 낳는 “지시 전염(brief contagion)”이 생겼고, 저자는 한 줄 프롬프트가 엔진은 시험하지만 아이디어는 시험하지 못한다고 말한다.

그 위로 제품 URL과 실제 자산을 주는 브랜드 프롬프트, 참조 프레임이나 영상을 주는 참조 프롬프트, 상태 목록을 XML로 적는 명세 프롬프트, 그리고 수천 자짜리 감독 지시서가 이어진다.
사다리를 올라갈수록 프롬프트가 영상을 묘사하기보다 제작진을 고용하는 문서에 가까워진다는 것이 저자의 관찰이다.

## 설정하기

### 도구 설치

저자가 제시하는 최소 구성은 Node, ffmpeg, 오디오 분석용 Python, 그리고 Playwright의 헤드리스 Chromium이다.

```bash
# 런타임
brew install node ffmpeg python          # Linux라면 apt
pip install numpy librosa soundfile      # 비트 분석용

# 프로젝트와 헤드리스 브라우저
mkdir motion-studio && cd motion-studio && npm init -y
npm i -D playwright && npx playwright install chromium

# Claude Code를 Opus 5.5로 시작
claude --model claude-opus-5-5
```

경로 B를 쓰려면 Remotion이나 HyperFrames의 스킬을 추가한다.
저자는 새 영상에는 `xhigh`, 출시 영상처럼 첫 3초가 중요한 작품에는 `max`, 작은 수정과 재렌더링에는 기본값 `medium`을 권하며,
목록에 오른 입소문 원샷은 모두 `xhigh`나 `max`에서 돌았다고 적는다.

### 프로젝트 규칙 파일

Claude Code는 매번 프로젝트 루트의 `CLAUDE.md`를 읽으므로, 모든 영상에 적용할 규칙은 거기에 한 번만 적는다.
저자의 규칙 파일은 네 부분으로 되어 있고, 요지는 다음과 같다.

```markdown
# Motion studio rules

## Render contract
- 모든 영상은 시간의 순수 함수다. `window.seek(t)`가 t 시점의 프레임을 그린다.
- 렌더 모드에서는 CSS transition, setTimeout, requestAnimationFrame, 프레임 간 상태 금지.
- 난수는 시드 고정(mulberry32)만. Math.random 금지.

## Look
- 금지 기본값: 그라디언트 위 가운데 제목, 전부 페이드인, 모서리 라벨과 프레임 테두리, UI 크롬의 글로.
- 디스플레이 서체 하나, UI 서체 하나, 강조색 하나.
- 2~4초마다 화면에 새로운 일이 일어나야 한다.

## Sound
- 트랙이 주어지지 않으면 음악과 효과음은 코드로 합성한다.
- 효과음은 측정한 비트 그리드(beats.json)에 맞춘다. 음량 -14 LUFS.

## Loop before you show me anything
1. 비트마다 한 프레임씩 밀착 인화를 만들어 직접 본다.
2. 1~10점으로 채점: 첫 2초 훅, 휴대폰 크기 가독성, 움직임 품질, 다양성, 브랜드 정확도, 소리 동기화.
3. 가장 나쁜 문제 세 개를 고친다. 모든 점수가 8 이상이 될 때까지 반복.
4. 그다음에만 전체 렌더링.
```

규칙의 첫 절이 가장 중요하다.
나머지는 취향이지만, 렌더 계약은 루프 전체가 성립하는 조건이다.
프레임이 시간의 순수 함수가 아니면 같은 코드로 두 번 렌더링한 결과가 달라지고, 그러면 비평 루프가 무엇을 고쳤는지 확인할 수 없다.

## 엔진 구현하기

### 결정론적 렌더러

원리를 확인할 수 있는 최소 구성이다.
페이지는 요청한 시각의 프레임을 그리고, 렌더러는 시간을 걸으며 프레임을 ffmpeg로 넘긴다.
저자의 코드를 바탕으로 핵심만 남겨 다시 썼다.

```html
<!-- index.html -->
<style>html,body{margin:0;background:#141413}canvas{display:block}</style>
<canvas id="c" width="1080" height="1920"></canvas>
<script>
const W = 1080, H = 1920, DUR = 6;
const g = document.getElementById('c').getContext('2d');
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));

// 닫힌 형태의 감쇠 스프링. 시간의 순수 함수라 어떤 프레임이든 바로 계산된다.
function spring(t, k = 170, d = 26) {
  if (t <= 0) return 0;
  const w0 = Math.sqrt(k), z = d / (2 * w0);
  if (z < 1) {
    const wd = w0 * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t));
  }
  return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
}

// 시드 고정 난수. Math.random을 쓰면 렌더링마다 결과가 달라진다.
function rng(seed) {
  return () => {
    seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const SCENES = [
  { from: 0, to: 3, draw(t) {               // 튀어나오는 제목
    const s = spring(t - 0.1, 220, 22);
    g.save(); g.translate(W / 2, H / 2); g.scale(0.6 + 0.4 * s, 0.6 + 0.4 * s);
    g.globalAlpha = clamp(t * 4);
    g.fillStyle = '#F0EEE6'; g.font = '700 190px serif'; g.textAlign = 'center';
    g.fillText('MOTION', 0, 0);
    g.fillStyle = '#D97757'; g.fillRect(-320 * s, 50, 640 * s, 18);
    g.restore();
  }},
  { from: 3, to: 6, draw(t) {               // 시차를 두고 나타나는 격자
    const r = rng(7);                       // 매 프레임 같은 시드 → 같은 난수열
    for (let i = 0; i < 48; i++) {
      const x = (i % 6) * 170 + 115, y = Math.floor(i / 6) * 170 + 360;
      const s = spring(t - i * 0.03 - r() * 0.1, 260, 20);
      g.fillStyle = i % 7 ? '#F0EEE6' : '#D97757';
      g.fillRect(x - 60 * s, y - 60 * s, 120 * s, 120 * s);
    }
  }},
];

function draw(t) {
  g.fillStyle = '#141413'; g.fillRect(0, 0, W, H);
  for (const s of SCENES) if (t >= s.from && t < s.to) s.draw(t - s.from);
}
window.seek = (t) => { draw(t); return true; };

// 일반 브라우저에서 열면 미리보기, 헤드리스 렌더링 중에는 꺼진다.
if (!navigator.webdriver) {
  const t0 = performance.now();
  (function loop() { draw(((performance.now() - t0) / 1000) % DUR); requestAnimationFrame(loop); })();
}
</script>
```

```javascript
// render.mjs — node render.mjs --fps 30 --dur 6
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? Number(process.argv[i + 1]) : d; };
const FPS = arg('fps', 30), DUR = arg('dur', 6);
mkdirSync('out', { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto('file://' + process.cwd() + '/index.html');
await page.evaluate(() => document.fonts.ready);   // 캔버스 글자는 폰트가 로드된 뒤에 그려야 한다

const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/silent.mp4'],
  { stdio: ['pipe', 'inherit', 'inherit'] });

for (let i = 0; i < DUR * FPS; i++) {
  await page.evaluate((t) => window.seek(t), i / FPS);   // 시계가 아니라 프레임 번호로 시간을 정한다
  const png = await page.locator('#c').screenshot({ type: 'png' });
  if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
```

저자의 원본은 프레임당 서브프레임 4장을 찍어 ffmpeg의 `tmix`로 섞는 모션 블러까지 넣는다.
위 코드는 그 부분을 빼 결정론 원리만 남긴 것이다.
모션 블러가 필요하면 서브프레임 수만큼 `framerate`를 올려 캡처하고 섞으면 된다.

### 목표가 여러 번 바뀌는 값

저자가 사람들이 가장 많이 놓친다고 강조하는 요령이다.
커서 위치나 컨테이너 너비처럼 목표가 여러 번 바뀌는 값은 스프링을 다시 시작하지 않는다.
목표가 바뀔 때마다 그 시점에서 시작하는 스프링을 하나씩 더한다.

```javascript
// keys: [[시각, 값], ...] 시간순. t 시점의 값을 돌려준다.
function track(t, keys, k = 170, d = 26) {
  let v = keys[0][1];
  for (let i = 1; i < keys.length; i++)
    v += (keys[i][1] - keys[i - 1][1]) * spring(t - keys[i][0], k, d);
  return v;
}

// 앞쪽 가장자리를 더 단단한 스프링으로 두면 탭 표시가 늘어났다 줄어든다.
function indicator(t, stops) {
  const lead = track(t, stops, 320, 30);
  const trail = track(t, stops, 140, 22);
  return { left: Math.min(lead, trail), right: Math.max(lead, trail) + 120 };
}
```

이렇게 하면 움직임은 끊기지 않으면서도 812번째 프레임을 그리려고 0번부터 811번까지 시뮬레이션할 필요가 없다.
물리 시뮬레이션처럼 상태를 적분하는 방식은 자연스럽지만 `seek(t)`의 결정론을 깨고, 이 합산 방식은 둘 다 지킨다.

### 소리

두 경로가 있다.
트랙을 주면 측정하고, 주지 않으면 그림과 같은 타임라인에서 합성한다.
측정은 librosa로 비트와 다운비트와 강한 온셋을 뽑아 JSON으로 남기고, 애니메이션이 그 파일을 읽는다.

```python
# python beats.py song.wav > beats.json
import sys, json
import numpy as np
import librosa

y, sr = librosa.load(sys.argv[1], sr=None, mono=True)
tempo, frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
beats = librosa.frames_to_time(frames, sr=sr).round(3).tolist()

onset = librosa.onset.onset_strength(y=y, sr=sr)
peaks = librosa.util.peak_pick(onset, pre_max=3, post_max=3, pre_avg=3,
                               post_avg=5, delta=0.5, wait=10)
json.dump({
    "bpm": float(np.atleast_1d(tempo)[0]),
    "beats": beats,              # 상태 변화를 놓을 자리
    "downbeats": beats[::4],     # 큰 전환을 놓을 자리 (4/4 가정)
    "hits": librosa.frames_to_time(peaks, sr=sr).round(3).tolist(),  # 효과음 자리
}, sys.stdout, indent=1)
```

합성 경로에서 저자는 클릭, 팝, 쿵, 휙 같은 효과음을 Node에서 사인파와 잡음으로 만들어 16비트 WAV로 쓰는 코드를 제시한다.
인용한 사례로, onur ozcan의 Steve Jobs 영상은 Node에서 사운드트랙을 합성하고 모든 컷을 120 BPM에 맞췄으며, Vox의 “small print”는 Python으로 음악을 합성한 뒤 초 단위로 렌더링을 다듬었다.

## 확인하기

### 에이전트에게 자기 프레임을 보게 하기

저자는 이 습관 하나가 입소문 난 영상과 밋밋하다며 올린 영상을 가른다고 말한다.
ffmpeg로 세 가지 이미지를 만든다.

```bash
# 밀착 인화: 초당 2프레임, 가로 6장
ffmpeg -i out/final.mp4 -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 out/contact.png

# 빠른 동작 주변 연속 12프레임: 튀는 곳과 겹치는 곳을 잡는다
ffmpeg -ss 4.1 -i out/final.mp4 -vf "scale=320:-1,tile=12x1" -frames:v 1 out/strip.png

# 휴대폰 테스트: 가로 360px에서 읽히는가
ffmpeg -i out/final.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 out/phone.png

# 루프 이음새 확인: 두 번 이어 붙여 본다
ffmpeg -stream_loop 1 -i out/final.mp4 -c copy out/loop_check.mp4
```

그리고 에이전트에게 자랑스러운 작가가 아니라 가혹한 모션 디렉터로서 세 이미지를 보라고 지시한다.
채점 항목은 첫 2초 훅, 휴대폰 크기 가독성, 움직임 품질, 다양성, 구도, 브랜드 정확도, 소리 동기화다.
찾아야 할 결함도 구체적으로 적는다.
전환 중 겹치는 텍스트, 부드럽게 멈추지 않고 미끄러지는 요소, 모서리 라벨과 프레임 테두리, 그라디언트 위 가운데 정렬 컷, 흐려진 확대 텍스트, 아무 일도 없는 비트, 루프 이음새의 끊김이다.

### 결정론 확인

같은 코드로 두 번 렌더링한 결과가 같아야 비평 루프가 의미를 가진다.

```bash
node render.mjs --dur 5 --fps 30 && md5 out/silent.mp4
node render.mjs --dur 5 --fps 30 && md5 out/silent.mp4   # 두 해시가 같아야 한다
```

저자가 원본에 넣은 확인 절차다.
다만 H.264 인코더가 멀티스레드로 돌면 같은 입력에도 바이트 단위 결과가 달라질 수 있으므로, 해시가 다르면 먼저 PNG 프레임을 저장해 프레임 단위로 비교하는 편이 정확하다.

## 트레이드오프

### 경로 A와 경로 B

경로 A, 곧 HTML 파일 하나와 캔버스와 `seek(t)`는 의존성이 없고 Opus가 기본으로 고르는 방식이다.
에이전트가 모든 것을 한 파일에서 보고 고칠 수 있어 루프가 빠르다.
대신 영상이 길어지거나 시리즈가 되면 한 파일이 수천 줄로 불어난다.
저자가 인용한 Steve Jobs 영상은 Remotion과 React와 SVG로 약 8,700줄이었다.

경로 B, 곧 Remotion이나 HyperFrames는 컴포넌트와 타임라인 미리보기를 준다.
저자는 Remotion을 시리즈와 템플릿과 데이터 기반 영상에, HyperFrames를 웹 페이지처럼 생각하는 사람에게 권한다.
대신 프레임워크의 규칙과 버전을 에이전트가 알아야 하므로 스킬을 따로 설치해야 하고, 에이전트가 프레임워크의 추상화를 우회하려다 오히려 복잡해질 수 있다.
한 편짜리 실험은 A, 반복해서 만들 형식은 B가 맞다.

### 한 번에 끝내기와 게이트를 두기

`xhigh`나 `max`에서 한 줄 프롬프트로 한 번에 끝내는 방식은 빠르고 인상적이다.
하지만 저자가 짚듯 결과가 서로 닮아 가고, 아이디어가 없는 영상이 된다.

감독 지시서는 계획, 리그, 스틸, 애니매틱, 전체 패스, 다듬기, 오디오, 렌더링이라는 게이트를 둔다.
결과는 좋아지지만 비용이 크다.
저자가 인용한 수채화 단편은 모델 호출 163번에 약 6시간 45분이 걸렸고, Donald의 뮤직비디오는 12시간 자율 실행이었다.
게이트마다 사람이 확인하면 시간이 더 들고, 확인하지 않으면 잘못된 방향으로 12시간을 쓸 수 있다.
저자의 지시서 템플릿이 샷 목록을 보여 주되 10분 안에 답이 없으면 계속하라고 적은 것은 이 사이의 절충이다.

### 비평 루프의 비용과 한계

모델이 자기 프레임을 채점하는 루프는 품질을 올리지만, 채점자와 작가가 같은 모델이다.
모델이 좋다고 보는 것과 사람이 좋다고 보는 것이 다를 때, 루프는 모델의 취향으로 수렴한다.
금지 목록에 모서리 라벨과 그라디언트 위 제목을 명시하는 이유가 여기 있다.
모델이 스스로 알아채지 못하는 기본값은 사람이 이름을 붙여 줘야 루프가 잡는다.

또 루프 한 번마다 렌더링과 이미지 읽기가 들어가므로 토큰과 시간이 늘어난다.
모든 점수 8점 이상이라는 종료 조건은 모델의 채점이 관대해지면 빨리 끝나고, 엄격해지면 끝나지 않는다.
사람이 최종 판단을 하는 지점은 루프가 대신할 수 없다.

## 함정

`Math.random`, `setTimeout`, CSS 트랜지션, `requestAnimationFrame`이 렌더 모드에 하나라도 남아 있으면 렌더링마다 결과가 달라진다.
모델은 습관적으로 이것들을 쓰므로 규칙 파일에 금지를 적어야 하고, 두 번 렌더링해 비교해야 확인된다.

캔버스 글자는 폰트가 로드되기 전에 그리면 대체 폰트로 찍힌다.
렌더러에서 `document.fonts.ready`를 기다리지 않으면 첫 몇 프레임만 서체가 다른 영상이 나온다.

카메라가 확대하는 요소에 `will-change`를 걸면 텍스트가 흐려진다고 저자의 명세 템플릿이 경고한다.
브라우저가 그 요소를 비트맵 레이어로 올린 뒤 확대하기 때문이다.

루프 영상은 마지막 프레임이 첫 프레임과 같아야 하며, 커서의 위치뿐 아니라 속도까지 같아야 이음새가 보이지 않는다.
위치만 맞추면 반복될 때 커서가 순간적으로 방향을 바꾸는 것처럼 보인다.

API 키를 프롬프트에 붙여 넣지 않는다.
저자는 키를 `.env`에 두고 프롬프트에는 변수 이름만 적으라고 하며, achxvi가 공개한 프롬프트가 농담 같은 가짜 키를 쓴 것도 그 때문이라고 적는다.
프롬프트를 스크린숏으로 공유하는 순간 키가 새어 나간다.

브랜드 영상에서 제품 UI를 모델이 상상으로 다시 그리게 두면 없는 화면이 생긴다.
저자는 Playwright로 실제 사이트의 스크린숏을 받아 자르고 움직이라고 하며, 스킬의 절대 규칙에도 실제 제품 UI만 쓰라고 넣는다.

## 체크리스트

- 모든 장면이 `window.seek(t)` 하나로 그려지며 프레임 간 상태가 없는가?
- 렌더 모드에서 `Math.random`, 타이머, CSS 트랜지션을 쓰지 않는가?
- 같은 설정으로 두 번 렌더링한 프레임이 같은가?
- 렌더러가 폰트 로드를 기다린 뒤 캡처하는가?
- 목표가 여러 번 바뀌는 값을 스프링 합산으로 처리했는가?
- 효과음과 상태 변화가 측정하거나 합성한 비트 그리드 위에 있는가?
- 밀착 인화, 연속 프레임, 휴대폰 크기 이미지를 만들어 에이전트가 직접 보게 했는가?
- 금지할 기본 스타일을 규칙 파일에 이름으로 적었는가?
- 루프 영상의 마지막 프레임이 첫 프레임과 위치와 속도까지 같은가?
- API 키가 프롬프트가 아니라 `.env`에만 있는가?
- 제품 화면을 실제 스크린숏에서 가져왔는가?

## 기억할 원칙

### 생성물이 아니라 생성기를 결정론적으로 만든다

이 강좌의 모든 기법은 한 가지 결정에서 나온다.
모델이 영상을 직접 만들게 하는 대신, 영상을 만드는 프로그램을 쓰게 한다는 것이다.
모델의 출력은 확률적이지만, 그 출력이 프로그램이라면 프로그램의 실행은 결정적일 수 있다.

결정론은 비평 루프의 전제 조건이다.
같은 코드가 같은 프레임을 내야 “이 수정이 이 문제를 고쳤다”고 말할 수 있다.
그래서 `Math.random` 금지와 닫힌 형태의 스프링은 취향이 아니라 루프를 성립시키는 계약이다.
이 원칙은 영상에만 해당하지 않는다.
에이전트에게 무언가를 만들게 할 때, 결과물을 직접 만들게 하기보다 결과물을 재현 가능하게 만드는 생성기를 쓰게 하면 검증과 수정이 쉬워진다.

### 한 번 잘된 과정은 스킬로 굳혀야 반복된다

강좌의 마지막 단계는 파이프라인을 스킬로 묶는 것이다.
입력 수집, 자산 수집, 스타일 가이드, 비트 그리드, 샷 목록, 렌더링, 비평, 출력이라는 과정을 문서로 남기면, 다음 영상은 스킬 이름과 URL 한 줄로 시작된다.
저자는 결론에서 한 줄 프롬프트는 클립을 주고 하네스는 스튜디오를 준다고 요약한다.

여기서 교훈은 긴 프롬프트를 매번 다시 쓰지 말라는 것만이 아니다.
입소문 난 원샷의 뒤에 있던 1만 자짜리 지시서와 스킬 폴더는, 누군가 여러 번 실패하며 알아낸 규칙의 모음이다.
그 규칙을 스킬과 규칙 파일로 남기지 않으면 매번 같은 실패에서 다시 시작하고, 남기면 그 실패가 다음 작업의 출발점이 된다.
