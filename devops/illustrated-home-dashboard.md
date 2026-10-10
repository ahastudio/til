# 일러스트레이터가 그린 집 그림을 Home Assistant 대시보드로 만들기

원문: [I hired an illustrator to draw my house. Now it's my Home Assistant dashboard.](https://antonfrolov.substack.com/p/i-hired-an-illustrator-to-draw-my)

HN 토론: <https://news.ycombinator.com/item?id=49986882> (891점, 199개 댓글)

GN 토론: <https://news.hada.io/topic?id=35031>

## 요약

Anton Frolov가 2026년 10월 5일 Substack에 올린 글이다.
그는 1년 동안 오픈소스 스마트홈 플랫폼 Home Assistant로 집을 자동화했다.
모두 외출하면 에어컨이 전부 꺼지고, 정원 스프링클러는 날씨를 보고
더운 날은 오래 돌고 비 오는 날은 건너뛴다.

그래도 사람이 손대야 하는 기기가 남았다.
대표적인 것이 정원 조명이다.
조명은 제조사 앱이나 Home Assistant 앱으로만 켤 수 있는데,
저자 말로는 스스로 상황을 더 어렵게 만들었다.
직접 만든 타이머가 일정 시간 뒤 조명을 끄고,
끝나기 직전에 조명을 깜빡여 앱에서 연장할 시간을 준다.
문제는 가족 누구도 Home Assistant 앱이나
기존 대시보드를 쓰려 하지 않았다는 점이다.
물리 스위치는 타이머 문제를 풀지 못하고,
스프링클러처럼 본체 버튼을 누르고 젖기 전에 뛰어나와야 하는 기기도 있다.
그래서 저자는 모두가 쓰고 싶어 할 만큼 멋진 대시보드를 만들기로 했다.

여러 대시보드를 살펴보다가 실제 집을 그대로 옮긴 상호작용 평면도에 끌렸다.
찾은 사례는 대부분 Home Assistant 커스텀 카드나 외부 모델링 소프트웨어로 만든
3D였는데, 모델 자체는 정지 그림이고 상호작용은 그 위에 얹은 아이콘 층뿐이었다.
저자는 각주에서 이것이 2026년 5월에 조사할 때의 사정이며,
지금은 대부분의 작업을 AI 도구에 맡기는 방법을 포함해
3D 대시보드를 만드는 글이 훨씬 많아졌다고 덧붙였다.
픽셀 아트 평면도를 다룬
[글](https://strawberrysec.net/homelab/Home-Assistant-Pixel-Floorplan/)도 있었지만,
직접 다 그리거나 라이브러리 스프라이트를 편집기에서 하나씩 배치해야 했다.
원문에 실린 3D와 픽셀 아트 예시 그림은 저자가 이 글을 위해 생성한 것이라고
캡션에 밝혀 두었다.
저자는 작가를 찾아 나섰고, 이미 실내 공간을 많이 그려 온 환경 아티스트
Owen Yeconiel을 소개받았다.
작가 이름과 [링크](https://linktr.ee/owenyeconiel)는 글 맨 끝에 적혀 있다.
픽셀 아트 구상은 그 작가의 화풍이 더 마음에 들면서 자연스럽게 사라졌다.

결과물은 벽난로가 깜빡이고 정원 조명이 빛나고 침실 에어컨이 바람을 내보내는
손 그림 대시보드다.
구현은 Home Assistant 기본 카드인 `picture-elements` 하나와 몇 가지 요령이며,
저자는 작가 섭외와 요구 사항 정리, 문서 준비가 프로젝트의 대부분이었다고 말한다.
그림이 곧 프로젝트이고, 상태를 애니메이션으로 보여 주면 UI는 아이콘 몇 개와
센서 값만 남아 설계하거나 코딩할 것이 별로 없다는 것이다.
완성된 대시보드는 TV의 HDMI 입력 하나로 띄워 두고,
저자는 TV로 집 전체를 한눈에 보고 무언가를 바꿀 때는 앱을 쓰는
지금의 방식에 만족한다며 글을 맺는다.
Home Assistant 자체는 `hardware/home-assistant-core.md`에서,
홈랩 안에서 Home Assistant 설정을 GitOps로 다루는 사례는
`devops/homelab-ai-dev-platform.md`에서 다룬다.

## 동작 방식

### 그림 한 장 위에 겹치는 층

`picture-elements` 카드는 배경 그림(`image:`) 위에 요소(`elements:`)를
각자의 위치에 얹는 카드다.
저자가 쓴 요소 종류는 네 가지다.

| 요소          | 쓰임                                       |
| ------------- | ------------------------------------------ |
| `image`       | 기기 그림. 상태에 따라 그림을 바꾼다       |
| `icon`        | 상태 표시 아이콘                           |
| `state-label` | 온도, CO2 같은 센서 값 표시                |
| `conditional` | 상태 조건에 따라 하위 요소를 보이거나 숨김 |

기기가 살아 움직이는 원리는 `image` 요소의 `state_image`다.
에어컨이 꺼져 있으면 정지 그림을, 켜져 있으면 애니메이션 WebP를 보여 준다.
애니메이션 재생은 브라우저가 알아서 하므로 별도의 코드가 없다.

### 낮과 밤

낮밤 전환은 헬퍼 하나(`input_boolean.dashboard_night`)와
해 질 녘과 해 뜰 녘에 이 값을 뒤집는 자동화로 처리한다.
손으로 뒤집을 수도 있어 테스트할 때 쓸모가 있다.
밤 그림은 `conditional` 요소로 낮 그림 위에 얹고,
기기마다 낮 버전과 밤 버전을 같은 방식으로 나눈다.
정원은 낮, 밤, 조명을 켠 밤 세 가지 버전으로 마무리되었다.

### 기기를 누르면

에어컨처럼 조작할 수 있는 기기를 누르면 `tap_action: more-info`로
Home Assistant 기본 제어 창이 열린다.
창을 따로 디자인할 필요가 없어 가장 간단하다.
예외는 정원 관수다.
대시보드에서는 아이콘 하나지만, 그 뒤에 독립된 밸브와 타이머 여러 개가 묶여 있어
열어 줄 기본 창이 없다.
저자는 HACS로 설치하는 커스텀 통합
[Browser Mod](https://github.com/thomasloven/hass-browser_mod)로
직접 만든 팝업 창을 띄운다.
Browser Mod는 브라우저를 Home Assistant에서 제어할 수 있는
엔티티로 만드는 통합이며,
`browser_mod.popup` 서비스로 팝업을 열거나 기본 more-info 창을 대체할 수 있다.

## 작가에게 줄 작업 지침서

저자는 작가에게 다음 묶음을 보냈다.

- 가구 위치를 직접 표시한 단순한 건축 평면도
- 실제 방 사진
- 화풍과 색감 참고용 일러스트
- 다른 사람들의 대시보드 예시. 결과물이 어디에 쓰이는지 보여 주기 위해서다
- 요구 사항, 받아야 할 파일과 형식, 위 자료 각각의 용도를 적은 짧은 기술 명세
- 지난번 리모델링 때의 페인트 색상 코드. 사진에서도 색을 맞출 수 있어 필수는 아니다

글의 나머지가 모두 기대는 것은 기술 명세다.
저자가 정리한 요구 사항은 다음과 같다.

| 항목      | 요구 사항                                                         |
| --------- | ----------------------------------------------------------------- |
| 파일 형식 | 투명 배경 PNG, 애니메이션은 WebP                                  |
| 층 그림   | 층마다 낮 버전과 밤 버전                                          |
| 기기      | 기기마다 별도 레이어                                              |
| 꺼진 상태 | 정지 그림 한 장                                                   |
| 켜진 상태 | 짧은 반복 프레임. 8장이면 충분했다                                |
| 조명      | 꺼짐, 켜짐 모두 낮과 밤 버전                                      |
| 캔버스    | 모든 파일을 같은 크기의 공용 캔버스에, 집 안 제자리 위치로 내보냄 |

가장 중요한 규칙은 마지막 줄이다.
각 조각을 자기 크기로 잘라 내지 말고,
공용 캔버스 위 원래 자리에 둔 채 내보내야 한다.
저자는 이 규칙 하나가 나중에 위치를 맞추는 며칠을 아껴 준다고 했고,
그것을 어렵게 배웠다고 적었다.
또 처음에는 애니메이션을 PNG 스프라이트 시트로 요청했다가 프레임을 직접
애니메이션 WebP로 변환했으므로, 처음부터 WebP로 요청하라고 권한다.

작가 찾기에 대한 조언도 있다.
작가마다 전문 분야와 화풍이 다르고, 인기 작가는 몇 달씩 예약이 차 있으며,
작업 자체도 몇 주에서 몇 달이 걸린다.
대시보드 의뢰는 예쁜 그림 한 장이 아니라 기술 요구를 이해해야 하는 특이한 일이라
몇 차례 메시지를 주고받으며 최종 목표를 맞추는 과정이 필요했다.

## 구현하기

### 원문의 카드 설정

원문이 보여 준 아래층(`ground`) 카드 설정이다.
밤 헬퍼가 켜져 있으면 밤 그림을 얹고,
꺼져 있으면 거실 에어컨 레이어를 상태에 따라 바꾼다.

```yaml
type: picture-elements
image: /local/floorplan/ground/ground_day.webp
elements:
  - type: conditional
    conditions:
      - entity: input_boolean.dashboard_night
        state: 'on'
    elements:
      - type: image
        image: /local/floorplan/ground/ground_night.webp
  - type: conditional
    conditions:
      - entity: input_boolean.dashboard_night
        state: 'off'
    elements:
      - type: image
        entity: climate.main_room_ac
        image: /local/floorplan/ground/ac_living_off.webp
        # climate 엔티티는 냉방, 난방 등 모드가 상태값이므로
        # 켜진 상태로 볼 모드를 모두 같은 애니메이션에 연결한다
        state_image:
          cool: /local/floorplan/ground/ac_living_on.webp
          heat: /local/floorplan/ground/ac_living_on.webp
          heat_cool: /local/floorplan/ground/ac_living_on.webp
          auto: /local/floorplan/ground/ac_living_on.webp
          dry: /local/floorplan/ground/ac_living_on.webp
          fan_only: /local/floorplan/ground/ac_living_on.webp
        tap_action:
          action: more-info
```

원문 코드는 `elements:` 아래 들여쓰기가 4칸이지만, 여기서는 2칸으로 맞추었다.
YAML 의미는 같다.
주석은 원문에 없고 설명을 위해 더했다.

### 그림 파일 호스팅

`image` 속성은 URL이나 로컬 경로를 받으므로 그림을 어딘가에 올려야 한다.
저자는 Home Assistant 장비 자체에서 서빙했다.
`/config/www` 폴더가 없으면 만들고 Home Assistant를 재시작한 뒤 파일을 넣는다.
경로는 다음처럼 대응한다.

| 대시보드에서 쓰는 경로                       | 실제 파일 위치                                    |
| -------------------------------------------- | ------------------------------------------------- |
| `/local/floorplan/ground/ac_living_off.webp` | `/config/www/floorplan/ground/ac_living_off.webp` |

### 층별 보기와 전체 보기

저자는 층마다, 그리고 정원에 따로 보기를 만들고,
이 모두를 한 화면에 모은 Full 보기를 더했다.
공용 캔버스 규칙이 여기서 효과를 냈다.
모든 조각이 같은 캔버스에서 잘려 나왔으므로 원래 위치로 되돌리면
이미지 편집기의 레이어처럼 저절로 맞물린다.
정원은 집 위가 아니라 아래에 깔고, 1층은 아래층보다 조금 들어 올려
분해도처럼 두 층 안을 모두 들여다볼 수 있게 했다.

어려운 것은 층 설정을 재사용하는 일이었다.
Home Assistant의 UI 편집기는 카드 사이에 요소를 공유할 방법이 없어서,
같은 기기를 층 보기와 전체 보기에 두 번 설정해야 한다.
저자는 대시보드를 YAML 모드로 바꾸고, 층마다 요소를 별도 파일에 두어
두 보기가 함께 포함하게 했다.
방 하나를 한 번 고치면 모든 곳에 반영된다.
대시보드를 등록하는 재시작 한 번 뒤로는 파일만 고치면 된다.
대가는 시각 편집기를 잃는 것인데, 이미 층별 작업이 대부분 끝난 뒤라
저자에게는 큰 문제가 아니었다.

`picture-elements` 카드는 다른 카드를 품을 수 없다는 제약도 있다.
그래서 전체 보기는 층 카드들을 `vertical-stack`으로 쌓고,
CSS로 카드를 꾸미는 HACS 플러그인 card-mod로 위치를 잡는다.

원문은 YAML 모드 파일이나 card-mod 설정을 공개하지 않았다.
아래는 Home Assistant 문서와 card-mod README를 바탕으로 구조만 보인 예시이며,
직접 실행해 보지 않았다.
파일 이름, 경로, 그리고 `margin-top` 값은 임의로 정한 것이고,
실제 겹침 정도는 캔버스 비율에 맞춰 조정해야 한다.

```yaml
# configuration.yaml
lovelace:
  dashboards:
    home-floorplan:            # 대시보드 키에는 하이픈이 있어야 한다
      mode: yaml
      filename: dashboards/floorplan.yaml
      title: Floorplan
      show_in_sidebar: true
```

```yaml
# dashboards/floorplan.yaml
views:
  - title: Ground
    path: ground
    panel: true
    cards:
      - type: picture-elements
        image: /local/floorplan/ground/ground_day.webp
        # 층 요소는 한 파일에만 두고 두 보기가 함께 포함한다
        elements: !include floorplan/ground_elements.yaml
  - title: Full
    path: full
    panel: true
    cards:
      - type: vertical-stack
        cards:
          # 정원을 먼저 두어 집 아래에 깔리게 한다
          - type: picture-elements
            image: /local/floorplan/garden/garden_day.webp
            elements: !include floorplan/garden_elements.yaml
          - type: picture-elements
            image: /local/floorplan/ground/ground_day.webp
            elements: !include floorplan/ground_elements.yaml
            card_mod:
              style: |
                ha-card {
                  margin-top: -40%;
                  background: none;
                }
```

## TV에 띄우기

저자는 처음부터 TV에 대시보드를 띄우려 했다.
LG webOS 브라우저가 WebP를 지원하지 않는다는 글을 읽었지만 사실이 아니었다.
그 주장은 브라우저가 아니라 TV 내장 사진 뷰어 이야기였을 가능성이 크고,
테스트 이미지 하나로 확인할 수 있었다.
같은 이야기를 들으면 믿기 전에 직접 시험해 보라는 것이 저자의 조언이다.

진짜 문제는 다른 데 있었다.
webOS는 웹 페이지를 화면 보호기로 쓰거나
브라우저 시작 페이지를 지정하게 해 주지 않아,
대시보드를 보려면 매번 리모컨을 몇 번 눌러야 했다.
저자는 TV 소프트웨어를 아예 우회했다.
Home Assistant 장비가 어차피 TV 옆에 있어서
[HAOS Kiosk Display](https://github.com/puterboy/HAOS-kiosk/) 애드온을 설치하고
장비를 TV의 HDMI 입력 하나에 연결했다.
이 애드온은 HAOS 서버에서 X 윈도와 OpenBox, Luakit 브라우저를 띄워
지정한 대시보드를 여는 방식이다.
설정 탭에 HA 사용자 이름과 비밀번호를 넣어야 시작되고,
연결된 디스플레이가 있어야 하며,
기본값으로 600초마다 브라우저를 새로 고친다.
대시보드는 이제 TV의 입력 하나가 되었고, 늘 올바른 페이지에 열려 있다.

TV 화면에는 Home Assistant 메뉴를 숨기는
[Kiosk Mode](https://github.com/NemesisRE/kiosk-mode)를 HACS로 더했다.
저자의 TV는 Home Assistant로 제어할 수 있어서,
아무도 TV를 보지 않을 때 아침과 저녁 몇 시간 동안
대시보드 입력으로 바꾸는 일정을 걸어 두었다.
아쉬운 점은 TV 리모컨으로 HDMI 너머의 대시보드를 조작할 수 없다는 것이다.
TV에서는 보기만 하고 만질 수는 없다.

그런데 이것이 오히려 도움이 되었다.
TV에서 대시보드를 본 가족들이 직접 조작하려고 휴대폰에 앱을 깔거나
컴퓨터에 대시보드를 북마크했다.
층별 보기는 휴대폰에서 잘 맞고, 전체 보기는 최소 노트북 크기 화면이 필요하다.
처음 TV에 띄웠을 때 가족들은 그림과 실제 방을 비교하고,
기기를 켰다 끄며 그림이 어디에 반응하는지 찾아보았다고 한다.

## 트레이드오프

### 그림을 고정하면 집의 변화가 비용이 된다

모든 상태를 그림으로 표현하면 UI 설계와 코드는 거의 사라지지만,
그 대신 모든 변화가 작가의 작업이 된다.
기기 하나를 더하려면 낮과 밤, 꺼짐과 켜짐에 해당하는 그림이 최소 네 벌 필요하고,
같은 화풍으로 그려야 하므로 원래 작가에게 다시 맡겨야 한다.
swiftcoder는 자기 집이 이 작업을 할 만큼
느리게 바뀌면 좋겠다고 적었다.[^swiftcoder]
가구 배치나 기기 구성이 자주 바뀌는 집이라면 이 방식은 유지비가 크다.

표현할 수 있는 정보의 양도 그림이 정한다.
zimpenfish는 자기의 단순한 2D SVG 평면도가 초라해 보인다면서도,
센서가 20개 넘게 달린 화면을
이런 그림에 다 담기는 어려울 것이라고 했다.[^zimpenfish]
원문 대시보드가 보여 주는 것은 기기 상태와 온도, CO2 정도이며,
저자는 그림 위 UI가 아이콘 몇 개와 센서 값으로 줄어든 것을 장점으로 꼽는다.
센서가 많은 집이라면 그 장점은 곧 한계가 된다.

### YAML 모드는 재사용을 얻고 편집기를 잃는다

층 요소를 파일로 나누면 한 번 고친 방이 모든 보기에 반영된다.
대신 Home Assistant의 시각 편집기는 쓸 수 없고, 모든 변경이 파일 편집이 된다.
저자는 층별 작업이 끝난 뒤에 전환했기 때문에 손해가 작았다.
순서를 바꿔, 처음에는 UI 편집기로 한 층의 위치를 맞추고
그 결과를 YAML로 옮기는 편이 덜 고통스럽다.
이 순서는 원문의 경험에서 끌어낸 해석이다.

### 사람 작가 대 생성 이미지

HN 토론의 상당 부분은 사람 작가를 고용한 선택 자체를 다루었다.
_virtu는 LiDAR 휴대폰의 PolyCam으로 집을 스캔해 Blender와 Claude로 넘기면
일러스트레이터가 필요 없다고 했고,[^_virtu]
hatthew는 대부분 LiDAR 휴대폰이 없고 이 그림 의뢰 비용이
LiDAR 휴대폰 값과 비슷하다고 반박했다.[^hatthew]
dolebirchwood는 Reddit 댓글을 근거로 900달러를 들며 싸지는 않지만
연봉 75만 달러가 있어야 할 금액도 아니라고 했다.[^dolebirchwood]
이 금액은 원문에 없고, 링크된 Reddit 댓글은 확인하지 못했다.
ChickeNES는 평범한 사람은 맞춤 그림에 900달러를 쓸 수 없거나 쓸 생각이 없고
AI 그림이 폭발한 것이 그 선호를 드러낸다고 했다.[^ChickeNES]
반대편에서 sho_hn은 Krita 포럼의 구인 게시판으로 그림을 의뢰해 본 경험을 들며,
포트폴리오를 채우려는 학생 작가가 많아
상위 1%가 아니어도 그림을 의뢰할 수 있다고 했다.[^sho_hn]
KZerda도 젊은 작가나 생활비가 싼 지역의 작가에게 맡기면
기껏해야 몇백 달러라고 거들었다.[^KZerda]
mrmlz는 이 그림을 예술품이 아니라 집 제어용 키오스크의 일부로 보면,
사람들이 e-ink 화면, Control4, Hue 조명에 쓰는 돈과
비교할 만하다고 정리했다.[^mrmlz]

생성 이미지로 같은 일을 해 본 사람들의 경험은 엇갈린다.
dzhiurgis는 가진 평면도에 갈색 식탁, 냉장고 같은 이름표를 붙여 주면
AI가 그럭저럭 그렸지만,
사진 묶음을 주고 알아서 그리라고 하면 실수가 너무 많았다고 했다.[^dzhiurgis]
Leherenn은 짓고 있는 집의 차고 문 색을 고르려고 평면도, 렌더,
공사 사진을 모두 주었는데
두 채짜리 주택을 한 채로 그리고 층수와 창문 위치를 틀렸으며,
평지에 없는 계단까지 지어냈다고 적었다.[^Leherenn]
두 경험 모두 원문의 지침서가 왜 평면도, 사진, 공용 캔버스 규칙을
함께 담았는지 보여 준다.
다만 작가가 AI를 쓰지 않았는지 어떻게 아느냐는 maxdo의 질문에,[^maxdo]
OJFord는 의뢰인이 결과에 만족하면 문제 될 것이 없다고 답했다.[^OJFord]
vntok은 저자가 평면도, 사진, 지시 사항을 모두 넘겼으니
위에서 내려온 구현이 많고 작가 고유의 창작은 적어
지금 세대의 AI로도 쉽게 재현할 수 있다고 주장했다.[^vntok]
AI 없이 가는 길로는 c22가 LiDAR 대신
일반 사진 측량(photogrammetry)으로도 충분할 것이라고 했다.[^c22]

의심은 그림 바깥으로도 번졌다.
palmotea는 사람 작가를 고용한 것에 박수를 보내면서도,
그림을 보자마자 AI 특유의 어색한 부분부터 찾았다며
AI가 이 화풍을 망쳐 놓았다고 아쉬워했다.[^palmotea]
qwerty2020은 원문의 문장이 AI가 쓴 글 같다고 했지만,[^qwerty2020]
MostlyStable은 AI 글 판별 도구 Pangram이 90% 사람 글로 판정했고
자기 눈에도 AI 글 같지 않았다고 반박했다.[^MostlyStable]
작가 표기를 두고도 말이 있었다.
ideasphere는 작가 링크를 공유하며
그렇게 만족했다면 훨씬 눈에 띄게 밝혔을 것이라고 했고,[^ideasphere]
elicash는 Wayback Machine으로 보면 며칠 전부터 글 끝에
작가 표기가 있었다고 확인했다.[^elicash]

## 함정

### 원문 코드에는 위치 지정이 없다

Home Assistant 문서는 `image` 요소의 `style`을 필수로 두고,
기본값 `transform: translate(-50%, -50%)` 때문에 `top`, `left` 좌표가
요소의 중심을 가리킨다고 설명한다.
원문 예시에는 `style`이 없다.
공용 캔버스로 내보낸 레이어를 배경과 정확히 겹치려면
레이어의 중심을 카드 중심에 두고 폭을 카드에 맞추는 식의 지정이 필요할 것이다.
예를 들어 `top: 50%`, `left: 50%`, `width: 100%`를 주는 방식이다.
이 값은 문서의 규칙에서 끌어낸 것이며, 저자가 실제로 쓴 값은 원문에 없다.

### 꺼진 기기 그림이 회색으로 바뀔 수 있다

문서에 따르면 `image` 요소의 `filter` 기본값은 엔티티 상태가 `off`일 때
`grayscale(100%)`다.
에어컨 같은 `climate` 엔티티가 꺼지면 상태가 `off`이므로,
작가가 공들여 그린 꺼짐 그림이 흑백으로 표시될 수 있다.
의도와 다르면 `filter: none`을 지정한다.
원문은 이 문제를 언급하지 않는다.

### 파일만 고쳐도 반영되지 않을 때가 있다

저자는 YAML 대시보드 파일을 고친 뒤 브라우저 새로 고침만 하면 된다고 적었다.
Home Assistant 문서는 대시보드 오른쪽 위 메뉴의 Refresh로
설정을 다시 읽으라고 하며,
브라우저 새로 고침이 늘 변경을 반영하지는 않는다고 경고한다.
TV 키오스크처럼 오래 켜 두는 화면이라면
HAOS Kiosk의 주기적 새로 고침에 기대기보다
변경 뒤 직접 다시 읽게 하는 편이 확실하다.

### 그림 속 숫자도 사람들이 읽는다

mbnielsen은 예시 화면의 CO2 수치가 꽤 높다며,
실제 화면이라면 환기를 더 자주 하라고 했다.[^mbnielsen]
phs318u는 실내 24도, 사무실 26도가 덥다고 지적했다.[^phs318u]
그림이 멋질수록 사람들은 그 위의 숫자를 더 오래 들여다본다.
글이나 공개 스크린숏에 실제 센서 값이 그대로 드러난다는 점도 기억할 만하다.

### 대시보드가 필요 없는 집도 있다

BorisMelnik은 10년 가까이 Home Assistant를 쓰면서 모든 것을 자동화했다며
왜 아직 대시보드를 쓰느냐고 물었다.[^BorisMelnik]
lawn은 가족이 외출 전에 대시보드로 기온과 날씨를 보고,
음악이나 조명처럼 기분에 따라 손으로 조작할 일이 남는다고 답했다.[^lawn]
원문의 출발점도 자동화로 풀 수 없는 정원 조명 타이머였다.
자동화를 늘리는 것과 사람이 직접 만질 곳을 남기는 것은
서로 대체하는 관계가 아니다.
londons_explore는 모두가 쓰고 싶어 할 대시보드라는 저자의 목표를 인용하며,
자기 할머니라면 그런 것은 불가능하다고 여길 것이고,
새벽 2시에 욕실 조명을 켜려고 맞는 앱을 찾아야 할 때는
더욱 그렇다고 꼬집었다.[^londons_explore]

### 외출 시 에어컨을 끄는 자동화에도 반론이 있다

topham은 모두 외출하면 에어컨을 끈다는 원문의 첫 예시를 두고,
설정 온도를 유지하거나 조금 조정하는 편보다
비효율적인 경우가 많다고 지적했다.[^topham]
overtone1000은 압축기 재가동 손실은 몇 분짜리 짧은 공백에서만 의미가 있고,
더워지게 두었다가 다시 식히는 것보다 온도를 유지하는 편이
효율적이라는 말은
열역학적으로 오해이며 전기 요금이 시간대별로 다를 때만
비용상 이점이 생길 수 있다고 반박했다.[^overtone1000]
topham은 다시 공기 온도만이 아니라 벽과 바닥의 표면 온도도 쾌적함을 좌우하므로,
집이 많이 달아오르는 지역이라면 일정에 맞춰 미리 낮추는 편이
나을 수 있다고 답했다.[^topham2]
어느 쪽이 맞는지는 기후와 집 구조, 요금제에 따라 달라지며,
원문은 이 자동화의 효과를 측정하지 않았다.

### Home Assistant가 멈춰도 손으로 켤 수 있어야 한다

대시보드를 멋지게 만들수록 모든 조작이 그 화면을 거치게 되기 쉽다.
wallst07은 숙련된 Home Assistant 사용자가 아는 원칙으로
Home Assistant가 꺼져도 기기를 손으로 조작할 방법을 남겨 둘 것과
클라우드 없이 로컬로만 운영할 것을 꼽았다.[^wallst07]
sgarland는 같은 이유로 Hue 조명과 Inovelli 스위치를
Zigbee 그룹으로 직접 묶어 두어,
Home Assistant가 멈춰도 조명이 켜지게 했다고 적었다.[^sgarland]
원문의 스프링클러 문제에 대해서도 sandworm101은 문 가까이에 밸브를 달거나
전동 밸브를 실내 스위치에 연결하면 된다고 했다.[^sandworm101]
저자는 물리 스위치로는 타이머 문제가 풀리지 않는다고 했으므로,
이런 수동 경로는 대시보드를 대체하기보다 그 옆에 함께 두는 장치다.
이 마지막 판단은 해석이다.

## 체크리스트

- 작가에게 평면도, 방 사진, 화풍 참고 자료, 대시보드 예시, 기술 명세를 함께 보냈는가
- 모든 레이어를 같은 크기의 공용 캔버스, 제자리 위치로 받기로 했는가
- 애니메이션을 처음부터 WebP로 요청했는가
- 기기마다 꺼짐, 켜짐과 낮, 밤 조합을 모두 받기로 했는가
- `climate` 엔티티처럼 상태값이 여러 개인 기기의 `state_image`에 켜짐으로 볼 상태를 모두 연결했는가
- 꺼짐 그림이 흑백으로 바뀌지 않도록 `filter`를 확인했는가
- 그림 파일을 `/config/www` 아래에 두고 `/local/` 경로로 참조했는가
- 대상 TV 브라우저에서 애니메이션 WebP를 직접 시험했는가
- 층 요소를 한 파일에 두고 여러 보기가 포함하게 했는가

## 기억할 원칙

### 산출물의 좌표계를 의뢰 단계에서 고정한다

원문에서 가장 옮겨 쓸 만한 규칙은 공용 캔버스다.
작가가 조각을 자기 크기로 잘라 보내면 개발자가 위치를 하나하나 맞춰야 하고,
같은 캔버스에 제자리로 두면 층별 보기와 전체 보기 모두 좌표 계산 없이 맞물린다.
turnwrighthere는 저자가 작가에게 아주 상세한 지침서를 준 것을 칭찬하며
좋은 것을 넣어야 좋은 것이 나온다고 적었다.[^turnwrighthere]
일러스트레이터의 배우자라는 ckozlowski도 상세한 지침서를 높이 사며,
구도와 색 같은 규칙과 절충을 아는 전문가가 그 지침 위에
자기 화풍과 훈련을 더할 때 결과물이 크게 좋아진다고 했다.[^ckozlowski]

이 원칙은 그림에만 해당하지 않는다.
디자이너에게 아이콘을 받든 외주로 에셋을 받든,
나중에 코드가 조립할 산출물이라면 조립 방식이 요구하는 형식을
의뢰서에 먼저 적어야 한다.
저자가 이 프로젝트의 대부분이 작가 찾기와 문서 준비였다고 말한 것도
같은 이야기다.

### 사용자가 원하는 것은 조작이 아니라 보는 즐거움일 수 있다

저자의 목표는 가족이 앱을 쓰게 만드는 것이었고,
결과적으로 그 목표는 조작할 수 없는 TV 화면을 통해 이루어졌다.
보기만 하는 화면이 관심을 만들고, 관심이 생기자 가족이 스스로 앱을 설치했다.
기능을 더 편하게 만드는 것보다 보고 싶은 화면을 만드는 것이
채택을 끌어낸 셈이며, 이것은 원문의 경과를 정리한 해석이다.

---

[^swiftcoder]: <https://news.ycombinator.com/item?id=50017826>

[^zimpenfish]: <https://news.ycombinator.com/item?id=50018820>

[^_virtu]: <https://news.ycombinator.com/item?id=50011600>

[^hatthew]: <https://news.ycombinator.com/item?id=50012640>

[^dolebirchwood]: <https://news.ycombinator.com/item?id=50013875>

[^dzhiurgis]: <https://news.ycombinator.com/item?id=49990076>

[^Leherenn]: <https://news.ycombinator.com/item?id=50016567>

[^maxdo]: <https://news.ycombinator.com/item?id=50014047>

[^OJFord]: <https://news.ycombinator.com/item?id=50017444>

[^mbnielsen]: <https://news.ycombinator.com/item?id=50017431>

[^phs318u]: <https://news.ycombinator.com/item?id=50011672>

[^BorisMelnik]: <https://news.ycombinator.com/item?id=50023039>

[^lawn]: <https://news.ycombinator.com/item?id=50023819>

[^londons_explore]: <https://news.ycombinator.com/item?id=50026702>

[^turnwrighthere]: <https://news.ycombinator.com/item?id=50015207>

[^ChickeNES]: <https://news.ycombinator.com/item?id=50014295>

[^sho_hn]: <https://news.ycombinator.com/item?id=50012273>

[^KZerda]: <https://news.ycombinator.com/item?id=50013070>

[^mrmlz]: <https://news.ycombinator.com/item?id=50017635>

[^vntok]: <https://news.ycombinator.com/item?id=50016505>

[^c22]: <https://news.ycombinator.com/item?id=50015003>

[^palmotea]: <https://news.ycombinator.com/item?id=50012723>

[^qwerty2020]: <https://news.ycombinator.com/item?id=50021532>

[^MostlyStable]: <https://news.ycombinator.com/item?id=50021977>

[^ideasphere]: <https://news.ycombinator.com/item?id=50012378>

[^elicash]: <https://news.ycombinator.com/item?id=50019978>

[^ckozlowski]: <https://news.ycombinator.com/item?id=50015210>

[^topham]: <https://news.ycombinator.com/item?id=50014372>

[^overtone1000]: <https://news.ycombinator.com/item?id=50015626>

[^topham2]: <https://news.ycombinator.com/item?id=50025480>

[^wallst07]: <https://news.ycombinator.com/item?id=50018564>

[^sgarland]: <https://news.ycombinator.com/item?id=50019268>

[^sandworm101]: <https://news.ycombinator.com/item?id=50019948>
