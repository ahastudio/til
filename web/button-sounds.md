# Button Sounds

<https://buttons.joshwcomeau.com/>

<https://github.com/joshwcomeau/button-sounds>

HN 토론: <https://news.ycombinator.com/item?id=50638032> (491점, 73개 댓글)

GN 토론: <https://news.hada.io/topic?id=37822>

## 소개

Josh W. Comeau가 2026년 가을에 만든 UI 효과음 모음이다.
버튼 클릭과 토글 소리 50여 종을 직접 녹음해 무료로 공개하고,
웹 프로젝트에 붙이는 NPM 패키지와 React 바인딩을 함께 낸다.
저장소는 2026년 9월 21일에 만들어졌고, NPM의 최신 버전은 1.0.0(11월 22일)이다.
라이선스는 MIT다.

저자는 오디오 엔지니어링 배경이 있고
몇 해 전부터 프로젝트에 작은 UI 효과음을 넣어 왔다고 README에서 밝힌다.
이 프로젝트는 집 안에서 눌러 볼 만한 것을 모두 찾아 몇 주 동안 녹음한
결과물이다.

### 소리 구성

소리 이름은 녹음한 대상을 가리킨다.
아래 분류는 이름과 놀이터의 필터(키보드, 마우스, 게임 패드, 토글, 기타)에서 읽은
것이어서 일부는 추정이다.
- 키보드: `hi75-*`, `halo-*`, `uhk-*`, `asus-kbd-*` 등
- 마우스: `asus-mouse`, `rival-3`, `mx-master-3` 등
- 게임 패드: `ps5-dull`, `ps5-paddle`, `ps5-snappy` 등
- 토글: `guitar-toggle-on`, `guitar-toggle-off`, `tonal-on`, `synth-on` 등
- 기타: `kvm-switch`, `treadmill-*`, `camera-latch`, `lock-closed`,
  `lock-open` 등

각 소리는 누름 4개와 뗌 4개 이상, 많게는 16개의 샘플을 갖는다.
저자는 훨씬 많이 녹음하고 흥미로운 것만 남겼다고 한다.
녹음은 방음 처리를 한 같은 방에서 Zoom H4 레코더로 했고,
잡음은 Adobe Audition으로 줄였다.
`synth-on`과 `synth-off`만 Current VST 신시사이저로 디지털로 만들었다.
모든 소리는 스테레오이며 192kbps MP3와 48kHz 무손실 WAV로 받는다.

## 동작 원리

### 다중 샘플링

기존 효과음 대부분은 한 번 녹음한 단발음이라
같은 버튼을 계속 누르면 기계적이고 인공적으로 들린다.
이 프로젝트는 같은 소리를 여러 번 녹음해 두고
소리를 낼 때마다 무작위로 하나를 고른다.
실제 버튼도 누를 때마다 소리가 똑같지 않다는 점을 따른 것이다.
저자는 효과가 미묘해서 노트북이나 휴대폰 스피커로는 알아차리기 어려울 수 있다고
인정한다.

사이트의 놀이터(Sound Playground)에서는 큰 빨간 버튼으로 현재 선택한
소리를 내고,
오른쪽 패널에서 어느 샘플이 재생 중인지 보며 번호를 눌러 샘플을 고정할 수 있다.
위아래 화살표 키로 소리를 빠르게 넘길 수 있다.

### 패키지가 하는 일

`wireUp` 함수 하나가 다음을 맡는다.
- 지정한 소리 파일을 미리 불러온다.
- 버튼에 포인터 이벤트 핸들러를 달아 누름과 뗌 소리를 알맞은 때에 재생한다.
- 누를 때마다 샘플을 무작위로 고르고, 원하면 음높이에 약간의 변화를 더한다.
- 원하면 비트 수와 샘플링 속도를 낮춰 8비트 게임 같은 소리를 만든다.

오디오 파일은 기본으로 JSDelivr CDN에서 받으며, `wireUp`을 부를 때 선택한 소리만
내려받는다.
패키지 자체는 gzip으로 약 3kB이고,
소리를 재생하는 Howler 라이브러리(약 10kB)를 비동기로 불러온다.

## 사용하기

설치와 가장 단순한 사용은 다음과 같다.

```bash
npm install button-sounds
```

```javascript
import { wireUp } from 'button-sounds';

const button = document.querySelector('.my-button');

// 누름과 뗌 소리를 버튼에 연결한다.
wireUp(button, 'hi75-soft');
```

옵션으로 음높이 변화와 로파이 효과를 줄 수 있다.

```javascript
import { wireUp } from 'button-sounds';

const button = document.querySelector('.my-button');

wireUp(button, 'hi75-soft', {
  pitchVariation: 0.1,
  lofi: true,
  lofiOptions: { bits: 4, downsample: 0.25 },
});
```

재생 시점을 직접 정하려면 낮은 수준의 API를 쓴다.

```javascript
import { load, press } from 'button-sounds';

load('hi75-soft'); // 첫 클릭 전에 파일을 미리 받아 둔다.

const btn = document.querySelector('.my-button');
btn.addEventListener('pointerdown', () => {
  if (someCondition) press('hi75-soft');
});
```

저자는 단순한 경우에는 높은 수준의 `wireUp`을 권한다.
커서가 버튼 밖으로 나가도 뗌 소리가 항상 재생되도록 처리해 주기 때문이다.

React에서는 `button-sounds/react`의 `useButtonSounds(ref, '소리 이름')`
훅이 있고,
재생 시점을 직접 정하는 `useImperativeButtonSounds`도 있다.
소리 파일을 직접 쓰는 방법, 자체 호스팅, 오디오 스프라이트는 저장소 문서에
따로 있다.

## 주의할 점

README가 알리는 사용 지침은 다음과 같다.
- 소리를 작게 재생한다. 저자는 최대 음량의 25~50%를 쓴다.
  소리가 켜져 있다는 것을 잊은 사람을 놀라게 하지 않기 위해서다.
- 사용자가 끌 수 있게 한다. 모션에는 `prefers-reduced-motion`이 있지만
  소리에는 그런 명시적 설정이 없다고 저자는 알고 있다.
  저자의 블로그는 다크 모드 토글 옆에 음소거 버튼을 둔다.
- 소리가 항상 재생된다고 보장할 수 없다.
  브라우저가 사이트에 쌓인 신뢰를 계산해 자동 재생을 막기 때문이고,
  기준은 브라우저마다 다르고 계속 바뀐다.

## 비평

### 모바일 오디오 정책

HN의 masenf가 인용한 사이트 안내문은 iOS Safari에서 브라우저가 소리를 막을 수 있다고 말한다.
이 문서가 읽은 페이지 본문에서는 그 문구를 찾지 못했다.
masenf는 하드웨어 스위치로 무음 모드를 해제하면 소리가 난다는 것을
5분 헤맨 끝에 알았다고 적었다.[^masenf]
al_borland는 브라우저 오디오가 무음 모드를 따르는 것이 합리적이라고
보았다.[^al_borland]
hn-aarvin은 `navigator.audioSession.type`을 `"playback"`으로 설정하면
무음 모드에서도 소리가 난다고 알렸고, 기본값은 `"ambient"`라고 한다.
iOS 16.4 미만에서는 이 방법이 덜 안정적이어서 `AudioContext`를 쓰는 우회 방법이
있다고 덧붙였다.[^hn-aarvin]
이 문서는 이 방법을 직접 시험하지 않았다.
README의 지침과 같이 소리는 있으면 좋은 것이지 필수가 아니라는 입장이다.

### 사이트 성능

ShadowOfThePit는 사이트가 CPU의 절반을 쓰고 브라우저를 느리게 한다고 했다.
자바스크립트 파일 하나가 700kb라는 점을 이유로 들었다.[^ShadowOfThePit]
같은 스레드에서 nickserv는 모바일에서 거의 쓸 수 없다고 했고,[^nickserv]
patatero는 맥 미니의 온도가 55도에서 80도로 올랐다고 했으며,[^patatero]
cyocum은 Firefox가 멈췄다고 했다.[^cyocum]
반면 bovermyer는 다른 Firefox 버전에서 문제없이 돈다고 반례를 냈다.[^bovermyer]
isomorphic은 맥 미니의 팬이 도는 원인이 페이지의 광고 배너 같다고
추측했다.[^isomorphic]
이 문서는 이를 직접 재 보지 않았다.
패키지가 가볍다는 저자의 설명과 사이트의 놀이터가 무겁다는 보고는 서로 다른
대상이다.

### 소리 자체에 대한 의견

hunter2_는 같은 소리 안의 샘플에 음높이를 바꾸는 가공이 섞여 있다고 지적했다.
예를 들어 `DOWN4`는 다른 `DOWN`보다 반음 가까이 낮게 들린다는 것이다.
버튼의 기본 음높이는 진동하는 물체의 크기로 정해지므로
EQ, 왜곡, 리버브로 음색만 바꾸고 음높이는 고정하라고 제안했다.[^hunter2_]
이 패키지의 `pitchVariation` 옵션은 반대로 음높이 변화를 켜는 기능이다.
저자가 이 의견에 답한 기록은 스레드에서 찾지 못했다.

pembrook은 많은 샘플에 좌우 균형이 한쪽으로 치우친 채 들어 있다고
했다.[^pembrook]
HelloUsername는 방음된 방에서 마이크를 가까이 두고 녹음했다면
왜 모노가 아닌 스테레오로 내보냈느냐고 물었다.[^HelloUsername]
osener는 소리 선택 항목을 클릭할 때 그 소리가 재생되면 훑기가 쉬울 것이라고
제안했다.[^osener]
MiroslavPokorny는 CRT 슬라이더가 주사선이 아니라 건 글로우만 조절한다고
짚었다.[^MiroslavPokorny]

### 라이선스가 만든 파생물

DimitriBouriez는 MIT 라이선스를 근거로
이 소리로 Mechvibes(타자 소리를 재생하는 앱)용 팩을 만들었다고 알렸다.
키보드 4종과 마우스 4종이며, 누름과 뗌 샘플을 키마다 나눠 같은 소리가 반복되지
않게 했다.
저자의 이름과 라이선스를 각 팩에 포함했다고 한다.[^DimitriBouriez]

## 기억할 원칙

- 반복되는 UI 소리는 단발음 하나보다 여러 샘플의 무작위 선택이 낫다.
  이 프로젝트의 핵심이며 같은 원리는 효과음 전반에 쓸 수 있다.
- 소리는 작게, 끌 수 있게, 안 나와도 문제없게 만든다.
  브라우저의 오디오 정책을 이길 방법은 없다.
- 효과음 설계는 오래된 산업의 관심사이기도 하다.
KellyCriterion은 지인이 자동차 회사에서 문 소리와 손잡이 소리를 측정하는 일을
  했다고 전했고,[^KellyCriterion]
이 분야에서 일한다는 nippoo는 자동차 사운드 디자인 또는 오디오 엔지니어링이라고
  부른다고 답했다.[^nippoo]
- 확인할 것은 자기 사이트의 사용자가 소리를 원하는지,
  그리고 모바일 Safari에서 실제로 소리가 나는지다.

---

[^masenf]: <https://news.ycombinator.com/item?id=50638438>

[^al_borland]: <https://news.ycombinator.com/item?id=50638622>

[^hn-aarvin]: <https://news.ycombinator.com/item?id=50638749>

[^ShadowOfThePit]: <https://news.ycombinator.com/item?id=50640220>

[^isomorphic]: <https://news.ycombinator.com/item?id=50638921>

[^hunter2_]: <https://news.ycombinator.com/item?id=50639450>

[^pembrook]: <https://news.ycombinator.com/item?id=50641602>

[^HelloUsername]: <https://news.ycombinator.com/item?id=50640961>

[^osener]: <https://news.ycombinator.com/item?id=50640812>

[^MiroslavPokorny]: <https://news.ycombinator.com/item?id=50640240>

[^DimitriBouriez]: <https://news.ycombinator.com/item?id=50641271>

[^KellyCriterion]: <https://news.ycombinator.com/item?id=50639394>

[^nippoo]: <https://news.ycombinator.com/item?id=50640509>

[^nickserv]: <https://news.ycombinator.com/item?id=50640363>

[^patatero]: <https://news.ycombinator.com/item?id=50640565>

[^cyocum]: <https://news.ycombinator.com/item?id=50641376>

[^bovermyer]: <https://news.ycombinator.com/item?id=50641427>
