# pixelfx: 코드로 그린 픽셀 아트 이펙트 244개와 Claude Code 스킬

<https://github.com/patch-gg/pixelfx>

## 소개

pixelfx는 Patch(patch.gg)가 MIT 라이선스로 공개한 픽셀 아트 이펙트 라이브러리다.
이펙트 244개가 모두 이미지 파일이 아니라 작은 JavaScript 코드이고,
저장소의 `src/fx/<category>/<name>.js`에 하나씩 들어 있다.
README는 이 코드를 세 가지로 쓸 수 있다고 소개한다.
브라우저 게임(canvas, Phaser, PixiJS, Kaplay,
three.js)에서 코드를 그대로 쓰는 방법, 어느 엔진에서든 스프라이트 시트(sprite
sheet)를 내보내 쓰는 방법, 갤러리에서 색을 바꾸고 좌우를 뒤집어 보는 방법이다.
여기에 이펙트를 새로 만드는 Claude Code 스킬이 함께 들어 있다.

README는 방법론의 출처를 Hugo Duprez의 글 «How to make (good) pixel art effects
with Claude»로 밝힌다.
코드는 하나의 글이 아니라 라이브러리 규모로 같은 생각을 옮긴 결과이고,
`src/core/sim.js`와 파일 맨 위에 그렇게 적힌 이펙트는 Duprez의 코드를 가져다
고친 것이라고 한다.
이 문서는 README만 읽고 쓴 것이며 갤러리나 코드를 직접 실행해 보지는 않았다.

## 구성

README의 분류표에 적힌 개수를 모두 더하면 244개가 된다.
`moves` 12개도 이 합계에 들어 있고, 분류표는 `moves`를 포함해 모두 21개 범주로
이루어져 있다.

| 범주          | 개수 | README가 든 예                                       |
| ------------- | ---- | ---------------------------------------------------- |
| moves         | 12   | arrow shot, dash strike, earth stomp, fireball throw |
| fire          | 12   | brazier, campfire, candle, fire breath               |
| explosions    | 12   | barrel explosion, big explosion, cartoon pow         |
| water         | 12   | bubbles, drip, fountain, geyser                      |
| ice           | 10   | blizzard vortex, freeze, frost breath, frost nova    |
| lightning     | 11   | ball lightning, chain lightning, charge up           |
| sci-fi        | 12   | emp blast, energy core, force field, glitch          |
| melee         | 12   | claw swipe, dagger flurry, double slash              |
| impacts       | 11   | blunt hit, bullet impact, critical hit               |
| projectiles   | 13   | arrow, bullet tracer, cannon shot                    |
| spawn & death | 10   | coin drop, disintegrate, dissolve burn               |
| arcane        | 12   | arcane beam, arcane missiles, blink in               |
| holy          | 10   | blessing, divine shield, feather burst               |
| shadow        | 12   | black hole, curse, dark explosion                    |
| status        | 13   | bleeding, burning, charmed, confused                 |
| nature        | 13   | acid splash, boulder, earth spike                    |
| weather       | 12   | aurora, blizzard, cherry blossoms                    |
| ui            | 12   | achievement, coin collect, combo counter             |
| pickups       | 11   | chest open, coin spin, gem spin                      |
| transitions   | 10   | blinds, burn away, crt off, iris                     |
| critters      | 12   | bat, bird, butterfly, fish school                    |

## 사용하기

### 브라우저 게임에서는 코드를 그대로 쓴다

의존성이 없고, `npm i github:patch-gg/pixelfx`로 설치하거나 `src/core`와 필요한
이펙트만 복사한다.
프레임 버퍼를 만들고 `createFx`로 이펙트를 만든 뒤 매 틱마다 `update`와 `draw`를
부르는 구조다.
`draw`는 `"back"`과 `"front"`를 구분해 캐릭터 뒤와 앞에 따로 그리고,
마지막에 `composite`가 색을 먼저 합친 다음 빛을 위에 더한다.
`createFx`는 `flip`, `angle`, `seed`, `palette`,
`light` 같은 옵션도 받는다고 README는 적는다.

### 다른 엔진에서는 스프라이트 시트를 쓴다

Godot, Unity, GameMaker, Defold, LÖVE, Bevy에서는 `node tools/render.mjs
ice/frost-nova --sheet`로 시트를 만든다.
투명 PNG에 모든 프레임이 격자로 들어가고,
Aseprite 형식의 JSON이 프레임 사각형과 지속 시간, 그리고 `meta.pixelfx`(fps,
반복 여부, 열 수, 피벗)를 함께 담는다고 한다.
`node tools/sheets.mjs`는 라이브러리 전체를 `sheets/`로 내보낸다.

### 팔레트를 바꾸면 코드를 건드리지 않고 색이 바뀐다

어느 이펙트든 어두운 색에서 밝은 색으로 이어지는 16진수 색 배열인
팔레트를 받는다.
README는 불을 파란색으로 태우거나 치유 효과를 분홍색으로 빛나게 하는 예를 든다.

## 연기하는 이펙트

README는 이펙트만 있으면 스티커처럼 보인다고 말한다.
공격이 세게 느껴지는 것은 이펙트 주변의 몸이라는 것이다. 공격 전의 준비 동작,
맞는 순간의 정지, 맞은 쪽이 밀려나는 모습, 마무리 동작이 그렇다.
그래서 캐릭터가 나오는 이펙트 61개와 이펙트를 이어 붙인 동작(moves) 12개는 몸이
언제 무엇을 하는지를 데이터로 적어 둔다.

그 데이터가 `act` 객체다.
`poses`는 시간(이펙트의 첫 프레임이 0)과 자세의 쌍이고,
`hits`는 맞는 순간의 시각, 정지 시간(`stop`), 화면 흔들림(`shake`),
밀려나는 거리(`push`)를 담는다.
`createFx` 대신 `createAct`를 쓰면 캐릭터와 맞는 대상까지 함께 재생되고,
정지 구간에서는 `update`가 스스로 멈춘다.
이 타이밍은 평범한 데이터라서 스프라이트 시트의 `meta.pixelfx.act`에도 들어가고,
자기 캐릭터를 쓰는 사용자는 이 시간만큼 먼저 준비 동작을 시작하고 맞는 순간마다
정지 시간 동안 모든 갱신을 멈추면 된다.

몸에 그려지는 이펙트(서리, 독, 스캔 선)는 서 있는 캐릭터를 기준으로 쓰여 있고,
자세의 각 픽셀이 서 있는 몸의 어느 픽셀에서 왔는지를 알고 있어서
캐릭터를 따라다닌다.
기본 캐릭터는 24×38 크기의 회색 더미이고,
README는 이 더미가 3D 뼈대를 평평한 몇 가지 색과 한 줄의 윤곽선으로 그린
것이라고 설명한다.
`skeleton(pose)`와 `posedParts(pose)`로 관절과 부위별 그림도 꺼내 쓸 수 있다.

## 스킬과 직접 만들기

스킬은 Claude Code가 이펙트를 찾고, 쓰고, 내보내고, 만들게 가르친다.
`/plugin marketplace add patch-gg/pixelfx`와 `/plugin install pixelfx@pixelfx`로
설치하거나, `skills/pixelfx` 폴더를 스킬 디렉터리에 복사한다.

새 이펙트는 세 명령으로 돈다.

```bash
node tools/new.mjs arcane/my-spell     # 동작하는 출발점 (반복형은 --loop)
node tools/render.mjs arcane/my-spell  # records/arcane/my-spell/contact.png를 눈으로 본다
node tools/check.mjs arcane/my-spell   # 경계 밖으로 새는 픽셀, 이음매, 시드 없는 난수, 느린 프레임을 검사한다
```

그다음 접촉 시트(contact sheet)를 보고 가장 나쁜 점을 고치고 다시 렌더링하는
일을 되풀이한다.
`--gif`와 `--mp4`는 움직임을, `--all`은 모든 프레임을 보여 주고,
`node tools/act.mjs`는 동작 전체를 12fps 단계로 보여 준다. 움직임의 결함은 몇
장의 샘플로는 드러나지 않기 때문이라고 README는 설명한다.

## 동작 원리

이펙트는 두 종류이고 이미지는 쓰지 않는다.
순수 이펙트(pure effect)는 `draw(p, t, o)`를 내보내서 시간 `t`만으로 프레임이
정해지고, 그래서 반복형은 이음매 없이 이어진다.
시뮬레이션 이펙트는 `create(o)`를 내보내고 입자, 파편,
빛을 120Hz로 진행시켜서 프레임 속도와 상관없이 불꽃이 튀고 연기가 퍼지는
모양이 같다.

버퍼는 둘이다. `color`는 불투명, 디더링(dithered), 반투명 픽셀을 받고,
`light`는 위에 더해지는 빛을 받는다. 뜨거운 것이 뜨겁게 보이는 것은 빛 버퍼
덕분이라고 한다.
모든 난수는 이펙트의 시드에서 나오므로 40번째 프레임은 언제나 같다.
이펙트는 자기 원점 주변에 그려지고 배치, 뒤집기, 회전은 그리는 쪽이 맡으며,
방향이 있는 이펙트는 오른쪽을 향한다.
프레임 형식이 Sprite Fusion의 VFX와 같은 `{ w, h, ox, oy, color,
light }`여서 두 라이브러리가 한 프레임에 함께 그릴 수 있다고 README는 적는다.

## 라이선스

코드와 이펙트는 MIT이고 상업적 사용도 된다.
Duprez의 MIT 이펙트와 Hollow Crown의 MIT 소스에서 가져온 부분이 있고,
`gallery/fonts`의 Patch Pixel 글꼴은 Patch의 것이어서 MIT에 포함되지 않는다.
자세한 것은 `NOTICE.md`에 있다고 README는 안내한다.

## 분석

### 이미지 대신 코드를 자산으로 삼았다

pixelfx의 선택은 이펙트를 이미지가 아니라 시간과 시드를 받는 함수로 만든 것이다.
시드가 고정되면 같은 입력은 같은 프레임을 낳으므로,
40번째 프레임을 다시 렌더링해서 고치고 비교하는 일이 가능하다.
순수 이펙트가 시간만으로 프레임을 정하는 것도 같은 이유다. 반복형이 이음매 없이
이어지는 것은 구현의 편의가 아니라 설계의 결과다.

이 선택은 Claude Code가 만든 결과물을 사람이 판단하는 방식과 맞물린다.
Duprez의 글은 에이전트에게 처음 시안 5개에서 10개를 쓰게 하고 짧은 영상으로
렌더링해 `/records`에 두라고 권한다. 그 영상을 보고 방향을 고르는 것이 첫
단계라는 설명이다.[^spritefusion]
README의 `tools/render.mjs`가 `records/` 아래에 접촉 시트를 만드는 것은 이
흐름을 도구로 굳힌 것이다.

### 이펙트에 연기 데이터를 붙여 이식성을 만들었다

`act` 데이터가 스프라이트 시트의 JSON 메타데이터로 나간다는 점이 눈에 띈다.
이펙트의 프레임만 내보내면 준비 동작과 정지 구간이 사라지고,
받는 엔진은 이펙트를 스티커처럼 붙이게 된다.
pixelfx는 타이밍을 평범한 데이터로 두고,
쓰는 쪽에 그만큼 먼저 준비 동작을 시작하라고 요구한다.
이펙트와 몸의 시간 관계를 파일 형식의 일부로 만든 것이다.

### 방법론의 출처와 규모를 밝혔다

README는 Duprez의 방법과 코드를 쓴 부분을 명시한다.
Duprez의 글은 코드를 점토로 보고, 눈을 믿고,
참고 자료를 먹이라는 세 가지를 말하고, 게임 개발에서 AI로 한 번에 훌륭한 결과를
얻을 수 있다고 믿게 하려는 이들이 있지만 그렇지 않다고 적는다.[^spritefusion]
pixelfx는 그 생각을 244개로 확장하고 스킬을 붙인 것이어서,
독창적인 방법론이라기보다 한 사람의 작업 방식을 라이브러리 규모로 옮긴 사례로
읽는 것이 맞다.

## 비평

### 스킬은 반복 작업을 자동화하지만 눈은 대신하지 못한다

README의 스킬 설명은 Claude Code가 까다로운 픽셀 아티스트처럼 초안, 렌더링,
보기, 다듬기를 되풀이한다고 말한다.
그러나 Duprez의 글이 강조하는 것은 품질의 기준을 세우는 일이 사람의 몫이라는
점이다. 그 글은 이 일을 눈을 믿으라는 말로 요약하고,
같은 글에서 MIRV 로켓 발사기를 몇 시간 동안 다듬은 경험을 예로
든다.[^spritefusion]
스킬이 돌리는 루프에서 이펙트가 좋은지 판단하는 눈은 모델의 것이다.
`check.mjs`가 잡는 것은 경계 밖으로 새는 픽셀, 이음매, 시드 없는 난수,
느린 프레임이고, 느낌이 맞는지는 잡지 못한다.
README는 그 판단이 사람에게 남는다는 점을 말하지 않는다.

### 244개라는 숫자에 중복이 섞여 있을 수 있다

README는 효과 244개를 내세우지만 분류표의 `moves` 12개는 다른 이펙트를 이어
붙인 것이다.
README 스스로 열두 개의 동작이 이펙트를 이어 공격으로 만든다고 설명한다.
따라서 합계에는 이미 세어진 이펙트를 다시 쓴 항목이 섞여 있을 가능성이 있고,
독립된 이펙트가 몇 개인지는 README만으로 알 수 없다.
카탈로그(`docs/CATALOG.md`)를 열어 확인하지 않았으므로 이 점은
가능성으로만 적는다.

### 기본 캐릭터와 라이선스 경계가 쓰는 쪽의 부담이 된다

몸에 그리는 이펙트는 기본 캐릭터인 회색 더미를 기준으로 그려진다. README는 그
이펙트가 더미를 그리므로 자기 게임에 넣는다면 다시 생성하라고 안내한다.
자기 캐릭터를 쓰는 사람은 상태 이펙트, 오라(aura),
맞는 반응이 모두 24×38 더미 기준이라는 전제를 알고 시작해야 한다.
라이선스도 한 줄로 끝나지 않는다. 코드와 이펙트는 MIT이지만 글꼴은 별도이고,
가져온 코드는 원 저작자의 MIT 표기를 따라간다.
상업 게임에 넣을 때 확인해야 할 것은 MIT 한 줄이 아니라 `NOTICE.md`까지다.

## 인사이트

### 접촉 시트는 에이전트가 자기 결과를 보게 만드는 검증 장치다

코드로 그린 이펙트의 결과물은 PNG와 GIF로 떨어진다. 그래서 에이전트가 파일을
읽고 보는 단계를 루프 안에 넣을 수 있다.
README의 `new`, `render`, `check` 세 명령은 코드를 쓰고, 결과를 눈으로 보고,
결함을 자동으로 거르는 순서를 하나의 흐름으로 묶는다.
이 구조는 결과가 이미지나 영상으로 렌더링되는 다른 코드 생성에도 옮겨 쓸 수 있는
틀이다. 시드를 고정하고 접촉 시트를 만드는 두 가지가 핵심이다.

다만 이 루프의 마지막 판정이 눈에 있다는 점은 그대로 남는다.
`check.mjs`가 걸러내는 결함은 기계적으로 정의되는 것들이고,
어떤 움직임이 좋은지는 정의되지 않는다.
스킬의 가치는 사람의 눈을 대신하는 데 있지 않고,
사람이 보아야 할 시안의 수를 늘리고 보기 전에 명백한 결함을 치우는 데 있다.

### 타이밍을 데이터로 공개하면 엔진 사이의 경계가 사라진다

`meta.pixelfx.act`가 JSON에 들어간다는 것은 이펙트가 만들어진 곳과 쓰이는 곳이
다른 엔진이어도 시간 관계가 전해진다는 뜻이다.
README에 따르면 Phaser의 아틀라스 로더와 Godot,
Unity의 Aseprite 가져오기 도구가 이 JSON을 읽는다.
이 도구들이 모르는 필드를 무시한다면 기존 형식 위에 확장 필드를 얹어도 호환성은
깨지지 않는다. 이 문서는 그 동작을 직접 확인하지 않았다.

한편 이 방식의 한계는 필드를 읽고 쓰는 일이 사용자 몫이라는 점이다.
준비 동작을 먼저 시작하고 정지 시간 동안 모든 갱신을 멈추는 일은 엔진 쪽 코드가
해야 한다. 데이터는 공개되었지만 연기가 자동으로 재생되지는 않는다.

### 스킬 배포가 자산 배포를 대신하기 시작한다

pixelfx는 244개 이펙트를 담은 저장소이면서 그 이펙트를 쓰는 법을 에이전트에게
가르치는 플러그인이다.
`/plugin install` 한 줄이 라이브러리 설치와 사용법 교육을 함께 처리한다.
자산 라이브러리가 사람을 위한 갤러리 사이트와 에이전트를 위한 스킬을 동시에
내놓는 구성이다.

이 구성에서 갤러리 사이트의 역할은 달라진다. 사람이 이펙트를 골라 복사하던 일이
에이전트가 `“Make five takes on a coin pickup sparkle and show me the best
two.”` 같은 요청으로 대신하는 일이 된다.
고르는 눈은 여전히 사람에게 있으므로, 갤러리가 줄어드는 것이 아니라 시안을
비교하는 화면이 중심이 된다.

---

[^spritefusion]: Sprite Fusion, [How to make (good) pixel art effects with Claude - Sprite Fusion](https://www.spritefusion.com/blog/how-to-make-good-pixel-art-effects-with-claude), 2026-10-28
