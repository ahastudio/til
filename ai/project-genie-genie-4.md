# Project Genie 업데이트와 Genie 4 제공

원문: [Genie 4 is now available](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)

HN 토론: <https://news.ycombinator.com/item?id=50550415> (198점, 143개 댓글)

GN 토론: <https://news.hada.io/topic?id=37431>

## 요약

2026년 11월 18일 Google DeepMind의 Diego Rivas(그룹 프로덕트 매니저)와 Google Labs의 Pavan Kumar(그룹 프로덕트 매니저)가 쓴 Project Genie 업데이트 글이다.
올해 초 실험용 연구 프로토타입으로 나온 Project Genie에 새 경험이 추가되며, 자격이 되는 Google AI Ultra 구독자에게 오늘부터 열린다고 한다.
새 경험은 Genie 4 첫 접근, Genie 3 개선, Project Genie 에이전트, 커뮤니티 갤러리의 네 가지이다.
이 문서는 글 전문을 읽었다. Genie 4의 기술 설명은 별도 연구 글에 있으며 이 글은 제품 쪽 소개이다(그 글은 이 저장소의 `ai/genie-4.md`에 정리되어 있다).

| 항목                   | 글의 내용                                                                                                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Genie 4                | 가장 사실적이고 상호작용성이 높은 월드 모델이라고 한다. 세션 도중 글로 날씨, 캐릭터, 행동을 바꾸고, 처음으로 장면에 맞춰 바뀌는 실시간 네이티브 오디오(환경음, 캐릭터 대화)를 함께 낸다 |
| Genie 3 개선           | 모델 선택기에 남는다. 한 번 생성에 최대 3분 탐험(기존 60초), 여러 세계 연결, 360도 파노라마 이미지로 세계 시작, 탐험 중 자연어로 환경 변화                                              |
| Project Genie 에이전트 | 대화로 세계를 만든다. 초기 화면과 배경 음악을 Google의 멀티모달 모델로 만들고, Gemini가 세션에 함께해 화면을 보고 다음 이동 제안 칩이나 세계 속 사건을 낸다                             |
| 갤러리                 | 큐레이션된 세계와 커뮤니티 세계를 둘러보고 리믹스해 게시한다. 예로 Living Memory, Dino Field Guide, Rock Paper Scissors, Villa Giallo, The Life of Ants가 있다                          |
| 안전                   | 모든 영상과 오디오에 SynthID 워터마크, 모든 입력과 출력에 안전 검사                                                                                                                     |
| 제공                   | 자격이 되는 Google AI Ultra 구독자는 labs.google/projectgenie에서 오늘부터, Google AI Pro는 같은 페이지의 대기자 명단                                                                   |

글이 한계로 꼽는 것은 카메라 지연, 복잡한 물리적 상호작용, 실시간 오디오 정밀도, 장기 장면 지속성이며 수치는 없다.
가격, 지역, Genie 4의 세션 길이, 해상도, 프레임 수는 글에 없다. 「자격이 되는」의 기준도 정의하지 않는다.
글에는 AI가 만든 요약 블록이 따로 붙어 있는데 이 문서는 본문만 근거로 삼았다.

## 분석

### 중심 주장은 연구 모델을 만들고 나누는 제품으로 감싼다는 것이다

앞선 연구 글이 모델의 능력을 설명했다면 이 글은 그 모델을 쓰는 방식을 설명한다.
새 요소 넷 가운데 모델 자체의 변화는 Genie 4와 Genie 3 개선이고, 에이전트와 갤러리는 만들고 공유하는 층이다.
글의 첫머리가 초기 이용자의 요구(더 많은 통제, 쉬운 제작과 공유)를 이유로 드는 점이 이 구성을 뒷받침한다.
이는 글의 서술을 이 문서가 정리한 것이다.

### Genie 3가 계속 남는 이유가 용도 분담이다

Genie 3는 더 긴 탐험과 파노라마 기반 공간에 쓰도록 선택기에 남는다.
Genie 4는 오디오와 사실감을, Genie 3는 길이와 이미지 기반 시작을 맡는 구도이다.
Genie 4의 세션 길이가 글에 없어 어느 쪽이 얼마나 긴지는 비교할 수 없다.

### 발표와 접근 사이의 간격이 있다

앞선 발표는 10월 27일이고 이 글은 11월 18일이다.
HN 사용자 bsboxe는 발표와 제한적 제공 사이의 22일이 매우 길다고 짚었다.[^bsboxe]

## 비평

### 접근 조건이 가장 큰 불만이다

HN 사용자 kingrolo는 영국의 자기 계정에서 Ultra 안내가 Genie 3까지만 보이는 점을 들어 어떻게 돈을 내고 쓸 수 있는지 불분명하다고 했다.[^kingrolo]
다른 사용자는 이 기능이 Ultra 20x 요금제에서만 열린다고 되물었고, 조직 계정의 한 사용자는 Workspace에서 Google AI 서비스 사용을 포기했다고 했다.[^nh23423fefe][^tosser811]
zeroq는 원래 약속한 것을 쓰려면 6배를 내라는 격이라고 평했다.[^zeroq]
글에는 가격과 지역이 없어 이 주장들을 이 문서가 확인하지 못했다. 6배라는 비교의 근거도 확인하지 못했다.

### 볼 수 없는 것에 돈을 내야 한다

dumbmrblah는 웹사이트에서 Genie가 무엇인지 볼 수 없고 20x 요금제를 보지 않고 가입하지 않겠다고 했다.[^dumbmrblah]
글에는 영상 예시가 있으나 공개 체험이 없다는 점은 글에서 확인된다. 체험 가능 여부의 다른 경로는 이 문서가 열어 보지 못했다.

### 이름과 버전이 헷갈린다

mlmonkey와 mchusma는 글 안에 Genie 3와 Genie 4가 함께 나오는 점이 의도는 이해되나 혼란스럽다고 했다.[^mlmonkey][^mchusma]
글은 Genie 3를 용도 분담으로 남긴다고 설명하므로 이는 설명 방식의 문제에 가깝다.

### 장면 지속성은 글이 인정하는 한계이다

int0x29는 홍보 영상이 카메라를 돌렸다 되돌리는 장면을 피하는 것 같아 물체 영속성 문제가 의심된다고 했다.[^int0x29]
글은 장기 장면 지속성을 해결 중인 과제로 적어 이 지적과 방향이 같다. 영상 편집 선택의 의도는 이 문서가 확인하지 못했다.
epsteingpt는 추수감사절 데모를 해 보니 불안하고 끔찍했다고 하며 Magic Leap 시연과 비슷하다고 했다.[^epsteingpt] 개인 평가이다.

### 쓸모와 비용에 대한 질문이 남는다

soared와 artdigital, m12k는 실제 용도를 물었다.[^soared][^artdigital][^m12k]
largbae는 이 모델의 이론적 용도가 로봇이 행동 전에 결과를 상상하는 선견지명이라고 설명했다.[^largbae] 이는 사용자의 설명이며 글은 이 용도를 말하지 않는다.
yodon은 FBX나 USD 같은 형식으로 내보내고 싶다고 했는데 글에 내보내기 기능은 언급되지 않는다.[^yodon]

### 외부 반응

Lobste.rs에는 이 글의 토론이 없었다(`blog.google` 도메인 검색은 이 글을 돌려주지 않았다).
GeekNews 토픽에는 이용자 댓글이 없다.

## 인사이트

### 가져갈 것은 모델 발표와 제공 사이를 따로 읽는 습관이다

연구 글의 능력 서술과, 누가 언제 어떤 조건으로 쓸 수 있는지는 다른 질문이다.
이 글에서 확인되는 것은 구독 등급, 대기자 명단, 가격과 지역 부재이다. 제품 글에서는 접근 조건을 먼저 찾는 것이 필요하다. 이는 이 문서의 적용이다.

### 용도 분담이 설명되면 구버전 유지가 혼란을 덜 만든다

Genie 3를 길이와 파노라마용으로 남긴 방식은 구버전 유지의 이유를 기능으로 말해 준다.
이 설명이 이용자 혼란을 줄이는지는 HN의 반응으로는 엇갈린다.

### 확인할 관찰

이 글의 주장을 가를 관찰은 세 가지이다.
Genie 4의 세션 길이와 지연, 장면 지속성의 실제 측정,
Ultra 외 등급과 지역의 접근 시점과 가격,
갤러리 세계의 품질과 리믹스 사용 규모이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^bsboxe]: <https://news.ycombinator.com/item?id=50550704>

[^kingrolo]: <https://news.ycombinator.com/item?id=50551015>

[^nh23423fefe]: <https://news.ycombinator.com/item?id=50551219>

[^tosser811]: <https://news.ycombinator.com/item?id=50551606>

[^zeroq]: <https://news.ycombinator.com/item?id=50550881>

[^dumbmrblah]: <https://news.ycombinator.com/item?id=50551625>

[^mlmonkey]: <https://news.ycombinator.com/item?id=50551756>

[^mchusma]: <https://news.ycombinator.com/item?id=50553049>

[^int0x29]: <https://news.ycombinator.com/item?id=50554157>

[^epsteingpt]: <https://news.ycombinator.com/item?id=50554568>

[^soared]: <https://news.ycombinator.com/item?id=50550893>

[^artdigital]: <https://news.ycombinator.com/item?id=50552712>

[^m12k]: <https://news.ycombinator.com/item?id=50552984>

[^largbae]: <https://news.ycombinator.com/item?id=50551126>

[^yodon]: <https://news.ycombinator.com/item?id=50552681>
