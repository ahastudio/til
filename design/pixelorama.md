# Pixelorama: Godot로 만든 MIT 라이선스 픽셀 아트 에디터, 스프라이트와 타일과 애니메이션을 한 곳에서

<https://www.pixelorama.org/>

<https://orama-interactive.itch.io/pixelorama>

<https://github.com/orama-interactive/pixelorama>

## 소개

Pixelorama는 Orama Interactive가 만드는 오픈소스 픽셀 아트 편집기다.
스프라이트, 타일, 애니메이션을 만드는 도구를 한 프로그램에 모았고,
만드는 쪽은 이를 pixel art multitool이라고 부른다.
Godot 엔진으로 작성되어 있고 코드의 대부분은 GDScript다.
블로그에는 글쓴이가 Emmanouil Papadeas이고
직함이 Lead developer of Pixelorama라고 적혀 있다.[^v12]
GitHub 기여자 목록에서는 OverloadedOrama가 커밋 3,562개로 1위이고,
itch.io 페이지의 제작자 표기에도 OverloadedOrama가 올라 있다.
2위 Variable-ind의 커밋은 292개이니
프로젝트의 무게가 한 계정에 크게 기울어 있다.

이 도구가 약속하는 것은 세 가지다.
라이선스는 MIT이고, README는 이를 두고 무료 업데이트가 영원히 보장된다고 쓴다.
데스크톱 세 운영체제와 웹에서 돌아가고, 안드로이드 빌드는 실험 단계다.
Steam 판은 유료이지만 기능은 다른 판과 같고
Pro 버전이 아니라는 것이 FAQ의 설명이다.[^faq]

약속하지 않는 것도 있다.
안드로이드 빌드는 태블릿을 전제로 하며 휴대전화에서는
경험이 좋지 않다고 itch.io 페이지가 밝힌다.
Windows와 macOS 설치 파일은 서명되어 있지 않아서
운영체제가 경고를 띄운다.[^docs-trouble]
이 문서의 숫자는 2026-10-22에 읽은 값이다.

## 목차

- [소개](#소개)
- [숫자로 본 현황](#숫자로-본-현황)
- [어디서 어떻게 받나](#어디서-어떻게-받나)
- [기능 지도](#기능-지도)
  - [프로젝트와 레이어와 cel](#프로젝트와-레이어와-cel)
  - [애니메이션](#애니메이션)
  - [타일맵](#타일맵)
  - [3D 레이어](#3d-레이어)
  - [가져오기와 내보내기](#가져오기와-내보내기)
  - [자동화와 확장](#자동화와-확장)
- [사용하기](#사용하기)
  - [설치](#설치)
  - [첫 스프라이트를 내보내기까지](#첫-스프라이트를-내보내기까지)
  - [명령행으로 내보내기](#명령행으로-내보내기)
  - [확장 만들기](#확장-만들기)
- [값 정하기](#값-정하기)
- [Aseprite와 LibreSprite 곁에서](#aseprite와-libresprite-곁에서)
  - [사용자들은 무엇을 이유로 옮기나](#사용자들은-무엇을-이유로-옮기나)
- [트레이드오프](#트레이드오프)
  - [무료와 유료가 공존하는 후원 구조](#무료와-유료가-공존하는-후원-구조)
  - [Godot 위에 지은 편집기의 값](#godot-위에-지은-편집기의-값)
  - [새 기능과 파일 호환성의 교환](#새-기능과-파일-호환성의-교환)
  - [확장의 자유와 업데이트 뒤의 충돌](#확장의-자유와-업데이트-뒤의-충돌)
- [함정](#함정)
- [확인하기](#확인하기)
- [비평](#비평)
  - [비교의 근거가 모멘텀과 라이선스에 쏠려 있다](#비교의-근거가-모멘텀과-라이선스에-쏠려-있다)
  - [프로젝트가 한 사람의 시간에 걸려 있다](#프로젝트가-한-사람의-시간에-걸려-있다)
  - [문서와 코드가 서로 다른 시간을 가리킨다](#문서와-코드가-서로-다른-시간을-가리킨다)
  - [AI를 쓰지 않았다는 표시는 도구의 경계를 정하지 못한다](#ai를-쓰지-않았다는-표시는-도구의-경계를-정하지-못한다)
- [인사이트](#인사이트)
  - [편집기가 엔진을 재사용하는 구조가 기능의 속도와 취약점을 함께 정한다](#편집기가-엔진을-재사용하는-구조가-기능의-속도와-취약점을-함께-정한다)
  - [파일 형식은 곧 이탈 비용이고, Pixelorama는 이를 가져오기로 낮췄다](#파일-형식은-곧-이탈-비용이고-pixelorama는-이를-가져오기로-낮췄다)
  - [무료 도구에 돈을 내는 이유는 가격이 아니라 지속성이다](#무료-도구에-돈을-내는-이유는-가격이-아니라-지속성이다)
  - [오픈소스 에디터는 AI 서비스의 껍질이 될 수 있다](#오픈소스-에디터는-ai-서비스의-껍질이-될-수-있다)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)
  - [원본과 사본을 나누고 둘 다 남긴다](#원본과-사본을-나누고-둘-다-남긴다)
  - [라벨은 무엇을 재는지부터 정해야 한다](#라벨은-무엇을-재는지부터-정해야-한다)

## 숫자로 본 현황

아래 표는 2026-10-22에 GitHub API,
itch.io 페이지, Steam 상점 페이지에서 읽은 값이다.
저장소와 itch.io 페이지의 값에는 각주를 달지 않았고, Steam 값에만 달았다.

| 항목               | 값                                                                                                          |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| GitHub 별 / 포크   | 10,605 / 566                                                                                                |
| 열린 이슈와 PR     | 81개(PR 16개 포함), bug 라벨 이슈 55개                                                                      |
| 라이선스           | MIT                                                                                                         |
| 최신 안정판        | v1.2.3(2026-09-15), 소스의 버전 표기는 v1.2.4-rc1                                                           |
| 최근 릴리스 간격   | v1.1.8(2025-12-31), v1.1.9(04-12), v1.1.10(04-29), v1.2(07-29), v1.2.1(08-19), v1.2.2(09-09), v1.2.3(09-15) |
| 커밋 기여          | OverloadedOrama 3,562, Variable-ind 292, Calinou 29, Erevoid 27                                             |
| itch.io 평점       | 5점 만점에 4.9, 평가 789개, 댓글 648개                                                                      |
| Steam 가격과 평가  | 한국 스토어 11,000원, 평가 89개 중 85개 긍정[^steam]                                                        |
| 번역               | itch.io 언어 목록에 한국어를 포함해 29개 항목                                                               |
| Windows 64비트 zip | 38MB, 설치 프로그램 76MB, macOS dmg 67MB, 안드로이드 apk 90MB                                               |

릴리스 주기는 짧다.
1.2대로 들어선 뒤 7주 동안 안정판이 네 개 나왔다.
다만 v1.2.2와 v1.2.3의 변경 기록에는 기여자로 Variable-ind의 이름만 올라 있다.

## 어디서 어떻게 받나

README가 안내하는 안정판 경로는 여섯 가지다.
Steam(Windows와 Linux), itch.io(Windows, Linux, Mac, Web),
GitHub Releases(Windows, Linux, Mac), GitHub Pages의 웹 판, Flathub, WinGet이다.
docs의 설치 페이지는 여기에 Scoop과 Snap을 더하고,
안드로이드는 itch.io에서만 받을 수 있다고 적는다.[^docs-install]

두 안내는 어긋나는 곳이 있다.
README는 GitHub Releases가 Windows, Linux, Mac용이라고
하지만 실제 릴리스 자산에는 `Pixelorama.apk`가 들어 있다.
README는 안드로이드를 한 줄도 언급하지 않는다.
이 문서는 apk가 GitHub 릴리스에도 올라온다는 점까지만 확인했고,
설치해 보지는 않았다.

가격 모델은 세 가지가 공존한다.
itch.io에서는 Download Now를 누르면 가격을 직접 정하는 대화창이 뜨고,
docs는 기부가 선택이라고 적는다.[^docs-install]
Steam에서는 한국 스토어 기준 11,000원이며,
FAQ는 이를 프로젝트에 돈을 보태는 길로 설명한다.[^faq]
GitHub Releases와 Flathub와 Scoop은 무료다.

## 기능 지도

### 프로젝트와 레이어와 cel

작업 단위는 `.pxo` 프로젝트다.
프로젝트는 layer와 frame이 교차하는 cel 격자로 이루어지고, layer에는 pixel,
group, tilemap, 3D, audio 같은 종류가 있다.[^docs-tilemaps][^docs-import]
저장하면 `.pxo`가 만들어지고,
내보내기를 하면 PNG나 GIF 같은 이미지가 만들어진다.
이 둘을 혼동하는 질문은 Troubleshooting 페이지의 단골 항목이다.[^docs-trouble]

layer에는 클리핑 마스크와 비파괴 효과(outline,
gradient map, drop shadow 등)를 붙일 수 있다.
v1.2에서는 이 효과의 속성을 프레임에 따라 움직이는 keyframe 타임라인이 들어왔고,
레이어 불투명도도 같은 방식으로 움직인다.[^v12]
사용자가 만든 Godot 셰이더를 레이어 효과로 불러올 수도 있다.[^v12]
반면 Effects 메뉴의 이미지 효과는 파괴적이어서,
적용하면 픽셀이 바뀌고 되돌리는 길은 undo뿐이다.[^docs-effects]

### 애니메이션

타임라인은 layer와 frame으로 구성되고, onion skinning,
frame tag, 오디오 동기화, 재생 중에 그리기를 지원한다.
프로젝트의 기본 FPS는 소스에서 6으로 정해져 있다.
새 프로젝트의 기본 캔버스는 64×64이고 Preferences에서 바꿀 수 있다.
자동 백업은 기본으로 켜져 있고 간격은 1분이다.

### 타일맵

tilemap layer는 tileset의 타일 번호를 격자에 배치한다.
사각, 등각(isometric), 육각(hexagonal) 타일을 지원하고,
육각 타일은 pointy-top과 flat-top을 모두 다룬다.[^docs-tilemaps]
타일 크기와 모양은 만든 뒤에 바꿀 수 없다.[^docs-tilemaps]
v1.2에서 autotiling이 들어왔지만 지금은 terrain을 하나만 지원한다.[^v12]
tileset을 Godot TileSet 리소스로 내보내면
autotiling 정보와 타일별 확률이 같이 나간다.[^v12]

### 3D 레이어

3D layer는 3D 모델과 도형을 2D 캔버스에 올리는 기능이다.
v1.2에서 이 기능이 처음부터 다시 만들어졌다.
3D 객체가 layer의 모든 cel에서 공유되고,
객체의 위치와 회전과 크기와 재질까지 애니메이션할 수 있으며,
glTF 장면을 불러오고 3D 모델 위에 직접 그릴 수도 있다.[^v12]
다만 3D 위에 그리는 기능은 실험 단계라고 블로그가 밝힌다.[^v12]
그리고 이 개편은 호환성을 깼다.
v1.1.x에서 만든 `.pxo`를 v1.2에서 열면 3D layer가 비어 있고,
그 반대도 마찬가지다.[^v12]

### 가져오기와 내보내기

가져오기는 PNG, APNG, JPEG, WebP, BMP, SVG, TGA, HDR 이미지와 `.pxo`를 다루고,
다른 프로그램의 `.ora`, `.aseprite`, `.kra`,
`.psd`, `.piskel`도 제한적으로 읽는다.[^docs-import]
`.mp3`와 `.wav`는 오디오 layer가 되고,
비디오와 GIF는 FFmpeg를 연결해야 프레임으로 들어온다.[^docs-import]
내보내기 형식은 소스의 `FileFormat` 열거형에서 읽었다.
PNG, WebP, JPEG, SVG, EXR, GIF, Aseprite,
APNG와 FFmpeg를 거치는 MP4, AVI, OGV, MKV, WebM이다.
docs의 Save and Export 페이지는 PNG, APNG,
GIF와 FFmpeg를 거치는 비디오를 설명할 뿐 SVG와
Aseprite 내보내기는 다루지 않는다.[^docs-export]
Aseprite 내보내기는 v1.2.2에서, SVG 내보내기는 v1.2.1에서 들어왔고,
SVG는 투명하지 않은 픽셀마다 `<rect>` 하나를 만드는 단순한 방식이다.

### 자동화와 확장

CLI는 데스크톱에서만 쓸 수 있고, `--export`, `--spritesheet`, `--output`,
`--scale`, `--frames`, `--direction`, `--json`,
`--split-layers` 같은 옵션을 준다.[^docs-cli]
확장은 `.pck`나 `.zip`으로 배포되고
Edit > Preferences > Extensions에서 설치한다.[^docs-ext]
소스의 확장 API 버전은 10이다.
README는 커뮤니티 확장의 예로 2D 픽셀을 3D 복셀로 바꾸는 도구를 든다.
프로젝트, layer, frame,
cel에는 사용자 메타데이터를 붙일 수 있어서 게임 파이프라인과 이어 붙이기 쉽다.

## 사용하기

### 설치

가장 짧은 길은 웹 판이다.
GitHub Pages와 itch.io 페이지에서 설치 없이 브라우저로 열린다.
웹 판에서 저장하면 브라우저가 `.pxo` 파일을 내려받는다.[^docs-export]
데스크톱에서는 `winget install pixelorama`처럼 패키지 관리자로 설치할 수 있고,
docs는 Scoop과 Snap 명령도 안내한다.[^docs-install]
macOS에서 앱이 손상되었다는 경고가 뜨면
서명되지 않은 바이너리 때문이라고 docs가 설명한다.[^docs-trouble]

### 첫 스프라이트를 내보내기까지

아래 순서는 docs의 설명을 이어 붙인 것이며,
이 문서가 직접 따라 해 본 절차는 아니다.

1. New project에서 캔버스 크기를 정하고, 기본은 64×64이다.
2. 팔레트는 기본 제공 Default와 Pixelorama 중에서 고른다.[^docs-palettes]
3. layer에 그리고, 애니메이션이면 frame을 추가해 frame tag를 단다.
4. `Control + S`로 `.pxo` 원본을 저장한다.
5. `Control + E`로 내보낸다.
6. 작은 캔버스는 export 창에서 확대 배율을 주고 보간은 Nearest로 둔다.[^docs-export]

### 명령행으로 내보내기

docs는 CLI의 형식을 이렇게 보인다.[^docs-cli]

```bash
Pixelorama.x86_64 [SYSTEM OPTIONS] -- [USER OPTIONS] [FILES]...
```

시스템 옵션 중에는 `--headless`와 `--quit`가 유용하고,
사용자 옵션에는 위에서 나열한 것들이 있다.
이 문서는 CLI를 실행해 보지 않았다.
다만 변경 기록은 v1.2.4(미출시)에서
`-o/--output` 옵션이 조용히 실패하던 문제를 고쳤다고 적는다.
그러니 v1.2.3 이하에서
`--output`에 의존하는 스크립트는 결과 파일이 실제로 생겼는지를 검사해야 한다.

### 확장 만들기

확장은 `extension.json`, `Main.tscn`, `Main.gd` 세 파일로 시작한다.[^docs-ext]
docs의 예시 JSON은 아래 같은 모양이다.

```json
{
    "name": "Example",
    "display_name": "Anything you want",
    "description": "What the extension does",
    "author": "Your Name",
    "version": "0.1",
    "supported_api_versions": [4],
    "license": "MIT",
    "nodes": ["Main.tscn"]
}
```

여기서 눈여겨볼 곳은 `supported_api_versions`이다.
docs의 예시는 4이고, 이 숫자로 호환성을 판정한다고
설명하지만,[^docs-ext] 현재 소스의 `ExtensionsAPI_Version`은 10이다.
예시를 그대로 복사하면 오래된 API를 선언하게 되니,
대상 버전의 `project.godot`에서 값을 확인해야 한다.

## 값 정하기

아래 표에서 기본값은 소스나 docs에서 읽은 것이고,
권장값과 그 근거는 이 문서의 제안이다.

| 항목               | 기본값              | 이 문서의 제안과 근거                                                                                              |
| ------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 캔버스 크기        | 64×64               | 게임에 넣을 스프라이트는 엔진에서 쓸 해상도로 시작한다. 타일 크기는 만든 뒤 바꿀 수 없다                           |
| 애니메이션 FPS     | 6                   | 도트 애니메이션은 프레임 수가 적어서 6~12 사이에서 정한다. 엔진 쪽 재생 속도와 맞추려고 frame duration도 함께 본다 |
| 자동 백업          | 켜짐, 1분           | 충돌 시 복구 수단이므로 끄지 않는다. 그래도 저장은 직접 한다                                                       |
| 내보내기 확대 배율 | 100%(소스의 기본값) | 공유용은 정수 배율과 Nearest 보간이 번짐을 막는다                                                                  |
| GIF 대 APNG        | GIF                 | 큰 캔버스에서 GIF가 느리면 APNG로 내보내고 변환한다고 docs가 권한다                                                |
| 앱 FPS 제한        | 0(제한 없음)        | 느린 기기에서는 낮추면 CPU 사용이 준다. 너무 낮추면 반응이 끊긴다                                                  |
| 타일 크기와 모양   | 만들 때 정함        | 만든 뒤에는 못 바꾸므로 엔진의 tile size를 먼저 정한다                                                             |
| Steam Cloud        | 500개 또는 2GB      | `Pictures/Pixelorama/SteamCloud/`에 저장한 `.pxo`만 동기화된다                                                     |

Steam Cloud의 상한과 경로는 v1.2 블로그가 밝힌 값이다.[^v12]
GIF와 앱 FPS에 관한 조언은 각각 Save and Export와 Troubleshooting 페이지에서
가져왔다.[^docs-export][^docs-trouble]

## Aseprite와 LibreSprite 곁에서

Pixelorama와 가장 자주 나란히 놓이는 도구는 Aseprite와 LibreSprite다.
세 도구의 공개된 사실을 표로 맞추면 아래와 같다.
Krita, GraphicsGale, Piskel은 이 문서가 직접 확인하지 못해서 표에 넣지 않았다.

| 항목           | Pixelorama                    | Aseprite                           | LibreSprite                                              |
| -------------- | ----------------------------- | ---------------------------------- | -------------------------------------------------------- |
| 라이선스       | MIT                           | EULA, 일부 모듈은 MIT[^ase-readme] | GPL-2.0, Aseprite 마지막 GPLv2 커밋의 포크[^libresprite] |
| 가격           | 무료, Steam 판 11,000원       | Steam 21,000원(한국)[^steam-ase]   | 소스 공개, 가격은 이 문서가 확인하지 못함                |
| GitHub 별      | 10,605                        | 40,270                             | 8,623                                                    |
| 마지막 푸시    | 2026-10-21                    | 2026-10-14                         | 2026-10-21                                               |
| 스크립팅과 CLI | 확장 API, CLI                 | Lua 스크립팅, CLI[^ase-readme]     | 이 문서는 확인하지 못함                                  |
| 고유한 점      | 타일맵, 3D layer, 레이어 효과 | 애니메이션과 도트 전용 도구가 성숙 | 오래된 Aseprite의 계보                                   |

별과 푸시 날짜는 GitHub API에서 읽은 값이며
각 저장소 페이지에 대응한다.[^ase-readme][^libresprite]
표의 마지막 줄은 이 문서의 요약이어서 일부는 해석이다.
Aseprite가 도트 전용 도구에서 앞선다고 본 것은 이 문서의 추정이고,
Steam 평가 21,515개가 보여 주는 사용자 규모가 근거의 전부다.[^steam-ase]

### 사용자들은 무엇을 이유로 옮기나

Hacker News에서 이 저장소는 단독 토론이 없다.
저장소와 v1 릴리스 페이지를 올린 글이 2024년에 한 건씩 있었지만
점수가 2~3점이고 댓글이 없다.[^hn-sub1][^hn-sub2]
대신 다른 글의 댓글에서 이름이 오르내린다.
아래는 그런 댓글 중 이 도구를 직접 비교한 것들이다.

roflcopter69는 Octopath Traveler II에서
영감을 얻은 에디터의 소개 글에 달린 댓글에서
Aseprite에서 Pixelorama로 갈아탔다고 적었다.
이유는 Aseprite의 개발이 몇 해 동안 조금 정체된 반면
Pixelorama에는 모멘텀과 커뮤니티가 있어 보인다는 것이고,
Godot로 만든 점도 좋다고 했다.[^roflcopter69]
그 댓글에 Aseprite 사용자 charlie-83이 Pixelorama에는 있고
Aseprite에는 없는 것이 무엇이냐고 물었다.[^charlie-83]
내가 읽은 범위에서는 이 질문에 대한 답이 달리지 않았다.

LibreSprite 소개 글에서는 desdenova가 Pixelorama를 처음 알았다며,
Aseprite가 상용화된 뒤로 LibreSprite만 써 왔기에
대안이 생겨 반갑다고 썼다.[^desdenova]
bbkane은 상품을 판다는 이유로 악이라 부를 수는 없다고 맞받았다.[^bbkane]
이 짧은 말다툼은 MIT 라이선스라는 사실이
이 도구의 장점으로 읽히는 맥락을 보여 준다.

파이썬으로 만든 도트 에디터 소개 글에서는
3036e4가 Pixelorama를 “open source이고 좋은 속도로 개선되는 듯하다”고 적었다.
같은 댓글은 그가 자세히 살펴본 적은 없다고 밝히고,
Aseprite의 소스는 직접 컴파일하면 무료로 쓸 수 있다고도 적는다.[^3036e4]
Aseprite 저장소의 README도 소스와 공식 바이너리가 EULA 아래에 있다고
밝히고 있어, 이 서술은 EULA의 범위를 말한 것으로 읽힌다.[^ase-readme]

Lobste.rs에서는 bkhl이 도트 에디터를 묻는 글에서
Pixelorama를 로컬이나 웹 앱으로 돌릴 수 있는 오픈소스라고 소개하며,
엔진별 소스 가져오기와 내보내기는 확장으로 해결한다고 적었다.[^bkhl]
이 댓글이 짚은 것은 확장 생태계가 Pixelorama의
기능 격차를 메우는 통로라는 점이다.

## 트레이드오프

### 무료와 유료가 공존하는 후원 구조

Pixelorama는 같은 소프트웨어를 세 가지 값으로 판다.
GitHub는 무료이고, itch.io는 가격을 정하게 하며, Steam은 11,000원이다.
Steam 구매자에게 주는 혜택은 자동 업데이트와 Steam Cloud,
업적이고 기능은 같다고 FAQ가 밝힌다.[^faq]
Steam Cloud 지원은 v1.2에서 들어왔고 이를 Steam에서
산 이들에 대한 선물이라고 블로그가 설명한다.[^v12]

이 구조가 얻는 것은 지속성이다.
무료 판이 있으니 진입 장벽이 없고, 돈을 내려는 사람에게는 편한 경로가 있다.
잃는 것은 단순함이다.
같은 앱이 세 가지 경로로 배포되면서 업데이트 지연,
설치 방법, 지원 범위가 경로마다 다르다.
Steam 판은 macOS를 지원하지 않는다는 점도 그 예다.

여전히 어려운 것은 후원의 크기다.
Patreon과 Steam과 itch.io의 수입이 개발에
쓰이는 비중은 공개된 자료로 알 수 없다.
커밋의 분포는 이 수입이 한 사람의 시간을 사고 있음을 시사하지만, 이는 추정이다.

### Godot 위에 지은 편집기의 값

FAQ는 Godot를 고른 이유를 개발 속도와 커뮤니티로 든다.[^faq]
얻는 것은 분명하다.
셰이더 기반 효과, 3D layer, glTF 가져오기,
Godot TileSet 내보내기가 모두 엔진의 기능을 빌려 쓴 것이다.
잃는 것은 엔진 버전에 묶이는 안정성이다.

변경 기록이 그 예를 보여 준다.
v1.2.4는 Windows에서 앱이 Shift가 계속 눌린 것처럼 동작하는 문제를 고치려고
Godot를 4.7.1로 낮췄고, 4.7.3이나 4.8에서
다시 올릴 때 재발하지 않기를 바란다고 적었다.
v1.2.3은 Godot 4.7.2로 빌드되었으니,
같은 앱이 엔진의 패치 버전에 따라 입력 버그를 겪은 셈이다.
README는 클론하려면 Godot 4.7.1이 필요하다고 쓰고 FAQ는 4.7이라고 쓴다.[^faq]
두 서술이 모순은 아니지만
어느 패치 버전이 맞는지는 릴리스마다 변경 기록을 봐야 한다.

### 새 기능과 파일 호환성의 교환

v1.2는 큰 기능이 한꺼번에 들어온 릴리스다.
블로그는 호환성이 깨지는 변경을 세 가지로 밝혔다.
3D layer 데이터가 호환되지 않고, 참조 이미지가 `.pxo` 안에 저장되며
이전 판의 참조 이미지는 불러오지 못하고, 테마가 초기화된다.[^v12]
v1.2.4(미출시)도 비슷하다.
cel이 캔버스 밖의 내용을 가질 수 있게 하면서
이전 버전은 새 `.pxo`를 열 수 없게 되었다고 변경 기록이 적는다.

얻는 것은 메모리 사용의 감소와 더 자유로운 편집이다.
잃는 것은 여러 버전을 오가는 작업 흐름이다.
팀에서
쓰거나 Steam Cloud로 기기 사이를 오가는 사람이 버전이 다른 기기를 한 대라도
갖고 있다면 `.pxo`를 열지 못할 수 있다.
그래서 내보낸 PNG나 Aseprite 파일을 원본의 사본으로 같이 보관하는 편이 안전하다.

### 확장의 자유와 업데이트 뒤의 충돌

확장은 Pixelorama의 기능 격차를 메우는 통로이지만,
Troubleshooting 페이지는 업데이트 뒤에 도구나 효과가 멈추면
확장이 파일 충돌을 일으킨 것일 수 있다고 말한다.[^docs-trouble]
이때 확장을 끄는 것으로는 해결되지 않고 갱신하거나 지워야 한다고 적었다.
그러니 확장에 기대는 작업은 업데이트 전에 확장의 호환 여부를 확인해야 한다.

## 함정

모두 이 문서가 직접 재현한 것이 아니라 docs,
변경 기록, itch.io 페이지의 서술이다.

저장과 내보내기를 혼동하는 일이 가장 흔하다.
`.pxo`는 Pixelorama만 읽는 원본이고 PNG와 GIF는 내보내기의 결과다.[^docs-export]
공유하거나 엔진에 넣을 파일은 반드시 내보내야 한다.

3D layer를 쓰는 애니메이션은 내보내기 전에 한 번 재생해야 한다.
다른 cel에 영향을 주는 변경을 했거나 다른 cel에서 undo를 했다면
그 cel을 선택해 화면을 갱신해야 하고, 그러지 않으면
내보낸 프레임이 틀릴 수 있다고 블로그가 밝힌다.[^v12]

Steam Cloud는 `Pictures/Pixelorama/SteamCloud/`에 저장한 `.pxo`만 동기화한다.
다른 경로에 저장한 파일은 동기화되지 않고, 두 기기에서 동시에 열면
동기화 오류가 날 수 있으며,
블로그는 이 기능이 공개 사용은 처음이라 다른 곳에도 백업하라고 당부한다.[^v12]

태블릿 문제도 반복된다.
Windows에서는 Preferences의 Drivers에서
태블릿 드라이버를 바꾸라고 docs가 안내한다.[^docs-trouble]
itch.io 페이지에는 Huion 펜이 커서는 움직이는데
그려지지 않는다는 사용자 글이 있고,
제작자가 드라이버 변경을 권했지만 글쓴이는 이미 해 봤다고 답했다.
댓글 648개 중 첫 페이지만 읽었고, 그 범위에서 해결된 기록은 없었다.

큰 파일은 위험하다.
비디오를 가져올 때는 프레임 수가 너무 많으면
메모리가 모자라 멈출 수 있다고 docs가 경고한다.[^docs-import]
GIF 내보내기는 큰 캔버스에서 느리고,
색 양자화가 필요한 GIF를 내보낼 때 충돌하던 문제는 v1.2.4(미출시)에서 고쳐졌다.

팔레트는 전역과 프로젝트 두 종류다.
기본 설정에서는 전역 팔레트를 고치면 프로젝트 사본이 생기지만,
읽기 전용 옵션을 끄면 전역 팔레트가 직접 바뀌고 되돌릴 수 없다.[^docs-palettes]
tileset을 다른 것으로 바꿀 때 새 tileset의 타일이 더 적으면
내용이 망가질 수 있다.[^docs-tilemaps]

macOS의 손상 경고와 Windows Defender 경고는
서명되지 않은 빌드 때문이다.[^docs-trouble]
FAQ는 공식 경로에서 받은 것이면 안전하다고
말하지만,[^faq] 이는 서명을 대신하지 못하므로 릴리스 페이지에서
받은 파일이 공식 것인지 확인하는 일은 사용자의 몫이다.

## 확인하기

아래 스크립트는 이 문서가 쓴 값을 읽기 전용으로 다시 확인한다.
GitHub API만 부르고 바이너리는 받지 않는다.
이 문서를 쓰는 동안 실제로 돌려서 출력을 확인했다.

```bash
#!/usr/bin/env bash
# Pixelorama의 공개 메타데이터와 소스 기본값을 읽기 전용으로 확인한다.
set -euo pipefail
REPO=Orama-Interactive/Pixelorama
RAW=https://raw.githubusercontent.com/$REPO/master

# 1. 저장소 메타데이터: 라이선스, 별, 마지막 푸시
curl -fsS "https://api.github.com/repos/$REPO" | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("license:", d["license"]["spdx_id"], "| stars:", d["stargazers_count"], "| pushed:", d["pushed_at"])'

# 2. 최신 안정 릴리스와 Windows 64비트 zip의 크기(받지는 않는다)
curl -fsS "https://api.github.com/repos/$REPO/releases/latest" | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("latest:", d["tag_name"], d["published_at"][:10])
for a in d["assets"]:
    if "Windows-64bit" in a["name"]:
        print("asset:", a["name"], a["size"] // 1024 // 1024, "MB")'

# 3. 소스에 적힌 기본값과 내보내기 형식
curl -fsS "$RAW/project.godot" | grep -E 'config/version|ExtensionsAPI_Version|config/features'
curl -fsS "$RAW/src/Autoload/Global.gd" | grep -E '^var default_(width|height)'
curl -fsS "$RAW/src/Classes/Project.gd" | grep -E '^var fps'
curl -fsS "$RAW/src/Autoload/Export.gd" | grep -E '^enum FileFormat'
```

2026-10-22에 돌린 출력은 아래와 같았다.
별 수와 푸시 시각은 시간이 지나면 달라진다.

```text
license: MIT | stars: 10605 | pushed: 2026-10-21T13:49:15Z
latest: v1.2.3 2026-09-15
asset: Pixelorama-Windows-64bit.zip 38 MB
config/version="v1.2.4-rc1"
config/features=PackedStringArray("4.7")
config/ExtensionsAPI_Version=10
var default_width := 64  ## Found in Preferences. The default width of startup project.
var default_height := 64  ## Found in Preferences. The default height of startup project.
var fps := 6.0:
enum FileFormat { PNG, WEBP, JPEG, SVG, EXR, GIF, ASE, APNG, MP4, AVI, OGV, MKV, WEBM }
```

이 문서가 직접 하지 않은 것도 밝힌다.
Pixelorama를 내려받아 실행하지 않았고, 위의 CLI 명령, 확장 만들기,
가져오기와 내보내기 변환, 태블릿 동작,
안드로이드와 웹 판은 모두 문서와 소스를 읽은 것에 그친다.
`.pxo` 형식의 내부 구조와 확장 API의 함수 목록도 읽지 않았다.

## 비평

### 비교의 근거가 모멘텀과 라이선스에 쏠려 있다

사용자 반응에서 Aseprite에서
넘어가는 이유로 드러나는 것은 기능이 아니라 인상이다.
개발이 정체되어 보인다는 말, 모멘텀이 있어 보인다는 말,
상용화되었다는 말이다.[^roflcopter69][^desdenova]
기능 비교를 요구한 charlie-83의 질문에 답이
달리지 않았다는 점이 이를 뒷받침한다.[^charlie-83]
Aseprite의 마지막 푸시는 2026-10-14이어서
정체되었다는 인상은 이 문서가 읽은 날짜에서는 확인되지 않는다.[^ase-readme]
다만 푸시 날짜는 개발의 활발함을 재는 거친 척도이고,
사용자가 말한 것은 2025년 5월의 인상이다.

그래서 Pixelorama가 Aseprite를 대신할 수 있는지를 이 문서는 판단하지 못한다.
확인한 것은 라이선스와 가격의 차이,
그리고 Pixelorama가 타일맵과 3D layer와 레이어 효과에서
독자 기능을 갖고 있다는 점뿐이다.
Aseprite의 도트 전용 도구와 Lua 스크립팅에 견줄 수 있는지는 사용해 보지 않으면
알 수 없다.

### 프로젝트가 한 사람의 시간에 걸려 있다

커밋 기여가 OverloadedOrama 3,562, Variable-ind 292로 12배 가까이 차이 난다.
v1.2.1 이후 안정판 변경 기록에는 Variable-ind의
이름만 오르거나 몇 명이 추가될 뿐이다.
이 분포는 활발한 프로젝트와도, 한 사람의 프로젝트와도 양립한다.
커밋 수가 곧 노동의 크기는 아니기 때문이다.
이 문서가 확인하지 못한 것은 기여자 통계가 아닌 메인테이너의 시간 배분이며,
여기서 말하는 구조적 위험은 공개된 지표에서 추론한 것이다.

### 문서와 코드가 서로 다른 시간을 가리킨다

작은 어긋남이 여러 곳에서 보인다.
docs의 Save and Export 페이지는 내보내기 형식을 세 가지로 적지만
소스는 열세 가지를 가진다.
README는 GitHub Releases가 안드로이드를 포함하는지 말하지 않는데
릴리스에는 apk가 있다.
README의 클론 안내는 Godot 4.7.1이고 FAQ는 4.7이며 v1.2.3은 4.7.2로 빌드되었다.
docs의 확장 예시는 API 버전 4인데 현재 값은 10이다.

이는 대부분 문서가 코드를 뒤따르는 구조의 징후이고, 해로움은 크지 않다.
다만 작은 어긋남이 누적되면 처음 쓰는 사람이 어느 쪽이 맞는지 판단할 수 없다.
이 문서가 기능의 정확한 목록으로 소스를 우선한 이유가 여기에 있다.

### AI를 쓰지 않았다는 표시는 도구의 경계를 정하지 못한다

Pixelorama의 CONTRIBUTING은 AI를 이용한 기여를 허용하지 않으며,
의심되는 PR은 낮은 우선순위로 다루고 통지 없이 닫을 수도 있다고 밝힌다.
사람과 사람 사이의 소통에 AI가 쓴 글을 쓰지 말라고도 적는다.
itch.io 페이지의 Content 항목은 “No generative AI was used”라고 표시한다.
이 둘은 Pixelorama를 만드는 과정에 관한 방침이다.

그런데 PixelLab의 문서는
Pixelorama에 PixelLab을 직접 통합해 편집과 AI 생성을 브라우저 한 곳에서
하게 했다고 적고, 데스크톱 브라우저만 지원한다고 밝힌다.[^pixellab-doc]
PixelLab의 첫 화면 튜토리얼 카드도 인페인팅을 Aseprite와 PixelLab의 에디터에서
하는 방법으로 소개하며 그 에디터를 괄호 안에 Pixelorama라고
부른다.[^pixellab-home]
제3자 프로젝트의 GitHub 이슈는 PixelLab의 에디터가 Pixelorama를 iframe으로 열고
`postMessage`로 저장 결과를 돌려받는 구조라고 설명한다.[^pixelkiln]

세 서술이 서로 맞아떨어지지만 Pixelorama 쪽에서 확인되는 것은 없다.
내가 읽은 README, 변경 기록, CONTRIBUTING, docs 페이지,
블로그 피드 어디에도 PixelLab이라는 이름이 나오지 않았고,
저장소 이슈 검색에서도 0건이었다.
그래서 이 통합이 Orama Interactive와 합의한 공식 협력인지,
확장인지, MIT 라이선스에 따른 제3자의 임베드인지 판단할 수 없다.
PixelLab의 페이지는 상업 서비스의 안내이고
자신들의 이해가 걸려 있다는 점도 감안해야 한다.
MIT는 이런 임베드를 막지 않는 라이선스이고,
이를 둘러싼 조건은 저작권 고지의 유지 정도다.

여기서 드러나는 것은 “AI 없음” 표시의 범위다.
itch.io 페이지의 표시는 도구가 만들어진 방식에 관한 것이어서
도구를 타고 만들어지는 결과물에는 말하지 않는다.
이는 Steam의 AI 공개 설문이 게임에 실려 배포되는 내용물을 본다는 점과 맞닿아
있고, 그 논의는 이 노트의 다른 문서(Steam Next Fest의 No-AI 필터)에서 다뤘다.
그 문서가 짚었듯 라벨이 무엇을 재는지 정하지 않으면
도구의 라벨과 결과물의 라벨은 서로를 보증하지 못한다.

## 인사이트

### 편집기가 엔진을 재사용하는 구조가 기능의 속도와 취약점을 함께 정한다

Pixelorama의 기능 목록을 보면 눈에 띄는 것이 Godot에서 오는 것이 많다는 점이다.
커스텀 셰이더 효과, 3D layer와 glTF, Godot TileSet 내보내기가 그렇다.
편집기를 엔진으로 지으면 엔진이 이미 가진 렌더링,
3D, 입력, 리소스 형식을 거의 공짜로 쓸 수 있다.
그래서 소수의 개발자가 적은 비용으로 넓은 기능을 쌓는다.

이 구조는 비슷한 사례가 많다.
Electron 위에 지은 편집기가 크로미움의 기능을 빌려 빠르게 자라고
크로미움의 변경에 같이 흔들리는 것과 같은 모양이다.
Godot를 4.7.1로 낮춰야 했던 Shift 키 버그는
이 구조의 비용이 어떻게 오는지를 보여 준다.
편집기가 고칠 수 없는 곳에서 문제가 오고,
해법은 엔진 버전을 되돌리는 것뿐이었다.

이 구조는 규모가 커질수록 문제가 된다.
엔진의 업그레이드 주기가 편집기의 안정 주기와 어긋날 때마다 호환성이 흔들린다.
앞서 본 `.pxo` 호환 문제도 같은 뿌리에서 나올 가능성이 있다.
이는 추정이며,
변경 기록은 호환 깨짐의 이유로 엔진이 아니라 cel 구조와 3D 재작성을 들었다.

### 파일 형식은 곧 이탈 비용이고, Pixelorama는 이를 가져오기로 낮췄다

Pixelorama가 Aseprite와 Krita와 Photoshop과 Piskel 파일을 읽고
v1.2.2부터 Aseprite 파일로 내보내는 것은
기능이기 전에 전략이라는 것이 이 문서의 해석이다.
도구를 옮기는 사람이 제일 두려워하는 것은 과거 작업의 손실이고,
가져오기와 내보내기는 그 두려움을 줄인다.
Aseprite로의 내보내기는 이동의 반대 방향을 열어 두는 것이어서
오히려 사용자가 안심하고 와 보게 하는 장치다.

그런데 이 전략에는 비대칭이 있다.
Pixelorama 자신의 `.pxo`는 버전 사이에서 호환이 깨진 적이 여러 번 있다.
이동하기 쉬운 포맷을 지원하면서 자기 포맷은 불안정한 셈이다.
이 비대칭은 프로젝트가 성숙하면서 줄어들 것이고,
그렇지 않다면 사용자는 내보낸 사본을 습관적으로 남기게 된다.

### 무료 도구에 돈을 내는 이유는 가격이 아니라 지속성이다

세 가지 가격이 공존하는 모델에서, Steam에 돈을 내는 사람은 기능을 사지 않는다.
FAQ가 말하듯 기능은 같다.
그들이 사는 것은 자동 업데이트와 동기화라는
편의와 프로젝트가 계속된다는 확신이다.
Steam Cloud 지원이 Steam 구매자에 대한 선물로
소개된 것은 이 모델이 지속성을 팔고 있다는 증거다.

이 구조는 오픈소스 후원의 흔한 형태이지만 한계가 있다.
후원이 개발자 한 사람의 생계로 이어지는
한 프로젝트의 안정이 그 사람의 사정에 달린다.
앞서 본 커밋 분포가 그 위험을 시사한다.

### 오픈소스 에디터는 AI 서비스의 껍질이 될 수 있다

PixelLab의 사례는 MIT 라이선스의 도구가 상업적 AI
서비스의 사용자 화면으로 쓰일 수 있음을 보여 준다.
이때 도구의 정체성은 두 겹이 된다.
Orama Interactive가 만드는 Pixelorama는 AI를 쓰지 않았다고 표시하지만,
PixelLab 안의 Pixelorama는 AI 생성이 일어나는 화면이다.

앞으로 게임 업계의 AI 공개 논의가 도구 단위로 번질 때 이 이중성이 문제가 된다.
Steam의 공개 설문이 내용물에 초점을 둔다는 점은 이런 경우에 합리적이다.
도구가 AI를 연결할 수 있다는 것과 결과물이
AI로 만들어졌다는 것은 다르기 때문이다.
그러나 같은 이유로 개발자가 도구의 라벨에 기대
결과물의 공개를 갈음하는 것은 안전하지 않다.

## 체크리스트

- [ ] 설치 경로를 정했는가(Steam, itch.io, GitHub, 웹, 패키지 관리자).
- [ ] 프로젝트 원본을 `.pxo`로 저장하고 내보낸 사본도 따로 보관하는가.
- [ ] 업데이트 전에 `.pxo`를 백업했는가.
- [ ] 두 대 이상의 기기를 쓸 때 Pixelorama 버전을 맞췄는가.
- [ ] tileset 크기를 엔진의 타일 크기에 맞춰 만들었는가.
- [ ] 3D layer를 쓰는 애니메이션은 내보내기 전에 한 번 재생했는가.
- [ ] CLI 내보내기 스크립트가 결과 파일의 존재를 검사하는가.
- [ ] 확장을 쓴다면 대상 버전의 API와 맞는지 확인했는가.
- [ ] 공개할 때 AI 사용 여부를 도구가 아닌 결과물 기준으로 적었는가.

## 기억할 원칙

### 원본과 사본을 나누고 둘 다 남긴다

`.pxo`는 Pixelorama만 읽는 원본이고
PNG나 Aseprite 파일은 다른 곳으로 가는 사본이다.
도구가 빠르게 바뀌는 시기에는 원본만으로는
미래의 자신에게 작업을 돌려줄 수 없다.
저장과 내보내기를 같은 동작으로 습관화하면
호환성 변경이 와도 잃는 것이 줄어든다.

### 라벨은 무엇을 재는지부터 정해야 한다

“AI 없음”이라는 표시가 도구가 만들어진 방식을 말하는지,
도구가 연결할 수 있는 것을 말하는지,
결과물의 방식을 말하는지에 따라 같은 도구도 다르게 읽힌다.
무언가를 표시하거나 표시를 믿기 전에 그 표시가 재는 대상을 먼저 확인한다.

---

[^v12]: Pixelorama, [Pixelorama v1.2, new possibilities for pixel art | Pixelorama](https://www.pixelorama.org/blog/pixelorama-1.2), 2026-07-29

[^faq]: Pixelorama, [FAQ | Pixelorama](https://www.pixelorama.org/faq)

[^docs-trouble]: Pixelorama, [Troubleshooting | Pixelorama](https://www.pixelorama.org/troubleshooting)

[^docs-install]: Pixelorama, [Installation | Pixelorama](https://www.pixelorama.org/user_manual/installation)

[^docs-export]: Pixelorama, [Save and Export | Pixelorama](https://www.pixelorama.org/user_manual/save_and_export)

[^docs-import]: Pixelorama, [Import | Pixelorama](https://www.pixelorama.org/user_manual/Import)

[^docs-cli]: Pixelorama, [Command Line Interface | Pixelorama](https://www.pixelorama.org/user_manual/cli)

[^docs-ext]: Pixelorama, [Extension Basics | Pixelorama](https://www.pixelorama.org/extension_system/extension_basics)

[^docs-tilemaps]: Pixelorama, [Tilemaps | Pixelorama](https://www.pixelorama.org/user_manual/tilemaps)

[^docs-palettes]: Pixelorama, [Palettes | Pixelorama](https://www.pixelorama.org/user_manual/palettes)

[^docs-effects]: Pixelorama, [Image effects | Pixelorama](https://www.pixelorama.org/user_manual/image_effects)

[^steam]: Steam, [Pixelorama on Steam](https://store.steampowered.com/app/2779170/)

[^steam-ase]: Steam, [Aseprite on Steam](https://store.steampowered.com/app/431730/)

[^ase-readme]: GitHub, [GitHub - aseprite/aseprite: Animated sprite editor & pixel art tool (Windows, macOS, Linux) · GitHub](https://github.com/aseprite/aseprite)

[^libresprite]: GitHub, [GitHub - LibreSprite/LibreSprite: Animated sprite editor & pixel art tool -- Fork of the last GPLv2 commit of Aseprite · GitHub](https://github.com/LibreSprite/LibreSprite)

[^pixellab-doc]: PixelLab, [Introduction to Pixelorama](https://www.pixellab.ai/docs/introduction-pixelorama)

[^pixellab-home]: PixelLab, [PixelLab - AI Generator for Pixel Art Game Assets](https://www.pixellab.ai/)

[^pixelkiln]: GitHub, [Browser pixel editor inside the gallery: Pixelorama with a host bridge (manual editing, Phase C)](https://github.com/gfargo/pixelkiln/issues/94), 2026-09-12

[^hn-sub1]: Hacker News, [Pixelorama: A powerful open-source pixel art multitool made in Godot](https://news.ycombinator.com/item?id=41241666), 2024-08-14

[^hn-sub2]: Hacker News, [Pixelorama v1 Released – Open-source pixel art multitool built with Godot](https://news.ycombinator.com/item?id=41110596), 2024-07-30

[^roflcopter69]: <https://news.ycombinator.com/item?id=43885646>

[^charlie-83]: <https://news.ycombinator.com/item?id=43886911>

[^desdenova]: <https://news.ycombinator.com/item?id=47273971>

[^bbkane]: <https://news.ycombinator.com/item?id=47279547>

[^3036e4]: <https://news.ycombinator.com/item?id=44874054>

[^bkhl]: <https://lobste.rs/s/bl9apn/favorite_pixel_art_editors#c_1p0kwd>
