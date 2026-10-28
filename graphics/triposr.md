# TripoSR: 사진 한 장에서 3D 메시를 만드는 MIT 라이선스 오픈 모델

<https://github.com/VAST-AI-Research/TripoSR>

<https://arxiv.org/abs/2403.02151>

<https://www.triposrai.com/>

## 목차

- [소개](#소개)
- [동작 방식](#동작-방식)
- [성능](#성능)
- [결과가 아쉬운 이유](#결과가-아쉬운-이유)
  - [단일 이미지 복원은 초안을 만드는 도구로 설계되었다](#단일-이미지-복원은-초안을-만드는-도구로-설계되었다)
  - [triplane이 64×64라서 마칭 큐브 격자를 높여도 세부는 늘지 않는다](#triplane이-6464라서-마칭-큐브-격자를-높여도-세부는-늘지-않는다)
  - [색은 같은 triplane에서 읽고 조명이 섞여 있다](#색은-같은-triplane에서-읽고-조명이-섞여-있다)
  - [보이지 않는 면은 모델이 추정한다](#보이지-않는-면은-모델이-추정한다)
- [비평](#비평)
  - [개선 항목별 기여를 보여 주는 실험이 논문에 없다](#개선-항목별-기여를-보여-주는-실험이-논문에-없다)
  - [비교는 저자가 고른 물체와 지표에서 이뤄졌다](#비교는-저자가-고른-물체와-지표에서-이뤄졌다)
  - [한계와 실패 사례, 그리고 일반 GPU의 속도가 빠져 있다](#한계와-실패-사례-그리고-일반-gpu의-속도가-빠져-있다)
  - [공식 데모와 같은 결과를 못 얻는 이유는 대개 입력 준비에 있다](#공식-데모와-같은-결과를-못-얻는-이유는-대개-입력-준비에-있다)
  - [정량 표는 형태만 재고 사용자가 보는 것은 색과 표면이다](#정량-표는-형태만-재고-사용자가-보는-것은-색과-표면이다)
- [설치하기](#설치하기)
- [실행하기](#실행하기)
- [값 정하기](#값-정하기)
- [제대로 쓰는 법](#제대로-쓰는-법)
  - [입력 이미지를 모델이 본 모양에 가깝게 만든다](#입력-이미지를-모델이-본-모양에-가깝게-만든다)
  - [마칭 큐브: 해상도와 임계값](#마칭-큐브-해상도와-임계값)
  - [텍스처: 구워 넣기와 바깥에서 입히기](#텍스처-구워-넣기와-바깥에서-입히기)
  - [메시 정리: 용접, 조각 제거, 구멍 메우기, 평활, 면 줄이기](#메시-정리-용접-조각-제거-구멍-메우기-평활-면-줄이기)
  - [작업 순서](#작업-순서)
- [CPU와 Apple Silicon과 Intel GPU에서 돌리기](#cpu와-apple-silicon과-intel-gpu에서-돌리기)
- [다른 모델로 갈아탈 때](#다른-모델로-갈아탈-때)
  - [증상별로 무엇을 바꿀지](#증상별로-무엇을-바꿀지)
  - [다중 시점을 먼저 만들고 재구성하는 흐름](#다중-시점을-먼저-만들고-재구성하는-흐름)
- [파생 프로젝트와 도구](#파생-프로젝트와-도구)
- [함정](#함정)
  - [로컬 결과가 공식 데모와 다르다](#로컬-결과가-공식-데모와-다르다)
  - [Gradio 미리보기의 방향과 밝기](#gradio-미리보기의-방향과-밝기)
  - [처음 실행할 때 내려받는 것들](#처음-실행할-때-내려받는-것들)
  - [마칭 큐브와 텍스처 굽기의 장치 문제](#마칭-큐브와-텍스처-굽기의-장치-문제)
- [비공식 사이트](#비공식-사이트)
  - [triposrai.com이 무엇인가](#triposraicom이-무엇인가)
  - [공식 저장소와 어떻게 다른가](#공식-저장소와-어떻게-다른가)
  - [받을 파일은 어디서 받는가](#받을-파일은-어디서-받는가)
- [트레이드오프](#트레이드오프)
  - [공짜의 대가는 설치와 하드웨어이고 기능은 서비스에 못 미친다](#공짜의-대가는-설치와-하드웨어이고-기능은-서비스에-못-미친다)
  - [단일 이미지 입력은 보이지 않는 면을 추정한다](#단일-이미지-입력은-보이지-않는-면을-추정한다)
  - [가볍게 쓰는 대신 품질의 천장이 낮다](#가볍게-쓰는-대신-품질의-천장이-낮다)
  - [전처리와 후처리에 쓰는 시간이 결과를 좌우한다](#전처리와-후처리에-쓰는-시간이-결과를-좌우한다)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)
  - [서비스가 막는 곳에서 오픈 모델이 길을 연다](#서비스가-막는-곳에서-오픈-모델이-길을-연다)
  - [인기 있는 오픈 모델은 이름을 쓰는 사이트가 먼저 보인다](#인기-있는-오픈-모델은-이름을-쓰는-사이트가-먼저-보인다)
  - [결과가 아쉬울 때는 모델 능력과 입력 준비를 따로 시험한다](#결과가-아쉬울-때는-모델-능력과-입력-준비를-따로-시험한다)
  - [해상도 숫자를 올리기 전에 원본 해상도를 본다](#해상도-숫자를-올리기-전에-원본-해상도를-본다)
  - [이 글을 읽는 방법](#이-글을-읽는-방법)

## 소개

TripoSR은 사진 한 장에서 3D 형상을 빠르게 복원하는 오픈소스 모델이다.
Tripo AI와 Stability AI가 함께 개발했고, 2024년 3월 4일에 열 명이 쓴 기술
보고서가 arXiv에 올라왔다.
소스 코드와 사전 훈련된 모델과 온라인 데모가 모두 MIT 라이선스로 공개되어 있고,
연구자와 개발자와 창작자가 3D 생성 AI를 쓰게 하는 것이 공개의 목표라고 논문과
README가 똑같이 밝힌다.
공식 코드는 GitHub의 `VAST-AI-Research/TripoSR` 저장소다.
2026년 10월 27일에 확인한 저장소는 2024년 2월 7일에 만들어졌고, 스타 7,233개,
포크 935개, 열린 이슈 109개이며 마지막 푸시는 2026년 6월 4일이다.

이 모델은 상용 서비스 [Tripo](tripo.md)의 한 부분이 아니라 별도로 풀린 공개
모델이다.
크레딧이나 구독 없이 내 GPU에서 돌릴 수 있다는 점이 가장 큰 쓰임이고, 대신
설치와 하드웨어를 직접 맞춰야 한다.
이름이 같은 비공식 안내 사이트(`triposrai.com`)도 검색 결과에 나오므로, 아래
비공식 사이트 절에서 따로 다룬다.

Stability AI의 공개 글은 이 모델을 초안 품질(draft-quality)의 텍스처 메시를
A100에서 약 0.5초에 만드는 모델로 소개하고, GPU 없이도 쓸 수 있다고
적는다.[^stability-blog]
Hugging Face 모델 카드는 맨 위에서 더 새로운 모델인 SF3D를 써 보라고 안내하고,
학습에 A100 40GB 여덟 장짜리 노드 22개로 5일이 들었다고 밝힌다.[^hf-card]
체크포인트 `model.ckpt`는 약 1.68GB이다.[^hf-card]
2026년 10월 27일에 읽은 모델 페이지의 `downloads` 값은 248,938이며 집계 기간은
확인하지 못했다.[^hf-card]

이 문서는 TripoSR로 얻은 결과가 아쉬웠다는 경험에서 출발한다.
아쉬운 이유를 공식 코드와 이슈에서 찾고, 같은 모델로 끌어올릴 수 있는 만큼을
정리한 다음, 그 한계를 넘으려면 어떤 모델로 가야 하는지 적는다.
코드 쪽의 마지막 기능 병합은 2024년 5월 14일의 텍스처 구현이고, 2026년 6월 4일의
마지막 푸시는 README 수정 하나였다.[^pr-94][^commits]
모델이 개선되기를 기다리기보다 사용법과 전후 처리를 손보거나 후속 모델로 옮겨야
한다는 뜻이다.
이는 이 문서의 해석이다.

## 동작 방식

논문이 설명하는 모델은 LRM이라는 큰 복원 모델의 구조를 바탕으로 한 트랜스포머다.
입력은 RGB 이미지 한 장이고 세 부분을 거친다.
이미지 인코더는 사전 훈련된 비전 트랜스포머 DINOv1로 초기화하며, 이미지를 전역과
지역 특징을 담은 잠재 벡터로 바꾼다.
디코더는 자기 어텐션 층과 교차 어텐션 층을 가진 트랜스포머 층을 쌓은 구조이고,
이 잠재 벡터를 triplane 기반 NeRF 표현으로 옮긴다.
마지막 NeRF는 다층 퍼셉트론으로 3D 공간의 한 점의 색과 밀도를 예측하고, 저장소의
`run.py`는 여기서 Marching Cubes로 메시를 뽑아 낸다.

가장 눈에 띄는 설계 선택은 카메라 정보를 모델에 주지 않는다는 점이다.
저자들은 카메라의 외부 파라미터와 내부 파라미터를 학습과 추론에서 모델이 스스로
짐작하게 해, 카메라 정보 없이 찍힌 실제 사진에 더 견고하게 만들려 했다고 쓴다.
이 선택은 편의를 주는 대신 부담을 모델에 옮긴다.
시점이 모호한 이미지에서는 카메라와 형태를 함께 추정해야 하므로 어긋남이 두 겹이
될 수 있다.
이는 이 문서의 해석이다.

논문이 LRM에 더한 개선은 다섯 가지다.
학습 데이터는 CC-BY 라이선스의 Objaverse에서 골라낸 부분집합이고, 실제 이미지
분포를 더 닮게 한 여러 렌더링 기법으로 만든다.
저자들은 이 방식으로 Objaverse만 써도 일반화가 좋아진다고 한다.
triplane 채널 수는 40으로 정했고, 그 덕에 학습에서 더 큰 배치와 해상도를 쓰면서
추론 메모리를 줄인다고 한다.
마스크 손실은 “floater”라는 떠다니는 조각 같은 아티팩트를 줄이며, 전체 손실은
평균제곱오차와 LPIPS(가중치 2.0)와 마스크 손실(가중치 0.05)의 합이다.
국소 렌더링 감독은 512×512 이미지에서 128×128 무작위 패치만 렌더링해 메모리를
아끼고, 전경을 덮는 패치를 더 자주 뽑아 물체 표면의 세부에 비중을 둔다.

학습 데이터를 CC-BY 부분집합으로 한정한 점은 MIT 라이선스 공개와 맞물려 읽힌다.
학습 데이터의 이용 조건이 분명해야 모델을 자유롭게 풀 수 있기 때문이다.
저자들이 이 연결을 직접 말하지는 않으므로 이는 이 문서의 해석이다.

## 성능

논문은 A100 GPU 한 장에서 메시 하나를 약 0.5초에 만든다고 주장한다.
품질은 GSO와 OmniObject3D 두 공개 데이터셋에서 잰다.
저자들은 두 데이터셋에 상자와 구와 원기둥 같은 단순한 형태가 많아 점수가
한쪽으로 쏠린다고 보고, 사람이 직접 걸러 각각 약 300개 물체만 썼다.
메시는 Marching Cubes로 추출해 표면에서 1만 개 점을 뽑고 Chamfer Distance(CD)와
F-score(FS)로 비교한다.
방법마다 예측이 시점에 묶여 있지 않을 수 있어서 회전 각도를 직접 탐색하고 ICP로
정렬을 다듬어 정답과 맞춘다.
비교 대상은 One-2-3-45, ZeroShape, TGS, OpenLRM(`openlrm-large-obj-1.0`
모델)이다.

| 데이터셋     | 방법       | CD↓   | FS@0.1↑ | FS@0.2↑ | FS@0.5↑ |
| ------------ | ---------- | ----- | ------- | ------- | ------- |
| GSO          | One-2-3-45 | 0.227 | 0.382   | 0.630   | 0.878   |
| GSO          | ZeroShape  | 0.160 | 0.489   | 0.757   | 0.952   |
| GSO          | TGS        | 0.122 | 0.637   | 0.846   | 0.968   |
| GSO          | OpenLRM    | 0.180 | 0.430   | 0.698   | 0.938   |
| GSO          | TripoSR    | 0.111 | 0.651   | 0.871   | 0.980   |
| OmniObject3D | One-2-3-45 | 0.197 | 0.445   | 0.698   | 0.907   |
| OmniObject3D | ZeroShape  | 0.144 | 0.507   | 0.786   | 0.968   |
| OmniObject3D | TGS        | 0.142 | 0.602   | 0.818   | 0.949   |
| OmniObject3D | OpenLRM    | 0.155 | 0.486   | 0.759   | 0.959   |
| OmniObject3D | TripoSR    | 0.102 | 0.677   | 0.890   | 0.986   |

정성 비교에서 저자들은 ZeroShape가 지나치게 매끈한 형태를 내고, TGS는 표면
세부를 더 살리지만 입력과 어긋나는 때가 있다고 쓴다.
ZeroShape와 TGS는 텍스처가 있는 메시를 바로 내지 못하고, One-2-3-45와 OpenLRM은
텍스처 메시를 내지만 형태가 부정확한 경우가 많다고 한다.
이 표를 읽을 때는 이 숫자가 저자가 고른 물체와 지표에서 나온 값임을 염두에
두어야 한다.
이 숫자가 말해 주는 것과 말해 주지 않는 것은 바로 다음 절에서 따진다.

## 결과가 아쉬운 이유

### 단일 이미지 복원은 초안을 만드는 도구로 설계되었다

Stability AI의 공개 글은 결과물을 draft-quality라고 부른다.[^stability-blog]
0.5초라는 숫자가 가리키는 것은 완성된 에셋이 아니라 빠르게 얻는 초안이다.
이는 이 문서의 해석이다.

예제처럼 나오지 않는다는 질문이 GitHub에 있다.
2026년 1월의 이슈는 `examples` 폴더의 이미지를 그대로 넣어도 메시가 늘
울퉁불퉁하고 정밀도가 낮다고 적는다.
작성자는 `--mc-resolution`과 `--chunk-size`를 바꿔 봤지만 쓸 만한 결과를 얻지
못했다며, README의 소개 GIF에 나온 메시를 만든 과정과 값을 묻는다.[^issue-149]
같은 증상이라는 댓글이 달렸을 뿐 이 문서가 읽은 범위에서 개발자의 답은
없었다.[^issue-149]

커뮤니티의 평도 비슷하다.
TRELLIS 스레드에서 horsawlarway는 ComfyUI의 TripoSR 노드와 마칭 큐브로 만든
모델이 '녹은 밀랍' 같은 모습이었다고 썼다.[^horsawlarway]
3D 변환 서비스 Meshcraft를 소개한 Show HN에서 vunderba는 두 해 된 TripoSR이
TRELLIS.2와 어떻게 비교되느냐고 물었고, 작성자 otmardev는 TRELLIS.2를 보니 PBR
재질과 깔끔한 쿼드 위상이 TripoSR의 구워 넣은 조명과 어지러운 메시보다 분명한
진전이라며 백엔드를 바꿀 계획이라고 답했다.[^vunderba][^otmardev]
두 사람의 평가는 개인의 인상이며 같은 입력으로 비교한 측정은 아니다.

### triplane이 64×64라서 마칭 큐브 격자를 높여도 세부는 늘지 않는다

논문 표 1은 triplane 업샘플러의 출력 모양을 64×64×40으로 적는다.
공개 설정 파일은 triplane 토큰의 평면 크기를 32, 출력 채널을 40, 렌더러 반지름을
0.87로 두고, 이미지 입력 크기는 512이다.[^hf-card]
마칭 큐브 격자는 이 triplane에서 밀도를 질의하는 3D 점들의 해상도이고
`--mc-resolution`의 기본값은 256이다.

triplane이 반지름 0.87의 정육면체(한 변 1.74)를 덮는다고 가정하면 triplane 한
칸은 약 0.027이고 256 격자 한 칸은 약 0.0068이어서, 격자 네 칸이 triplane 한
칸에 해당한다.
아래 표는 이 가정으로 계산한 값이다.
계산에 쓴 스크립트와 출력은 뒤의 마칭 큐브 소절에 있다.

| mc-resolution | 질의 점 수  | 밀도 격자(float32) | 격자 한 칸 | triplane 한 칸당 격자 칸 |
| ------------- | ----------- | ------------------ | ---------- | ------------------------ |
| 64            | 262,144     | 1.0MB              | 0.0272     | 1.0                      |
| 128           | 2,097,152   | 8.4MB              | 0.0136     | 2.0                      |
| 256           | 16,777,216  | 67.1MB             | 0.0068     | 4.0                      |
| 320           | 32,768,000  | 131.1MB            | 0.0054     | 5.0                      |
| 512           | 134,217,728 | 536.9MB            | 0.0034     | 8.0                      |

그래서 격자를 높이면 면이 더 촘촘하고 날카로워질 뿐 triplane이 담지 않은 세부가
새로 생기지는 않는다고 읽힌다.
이는 이 문서의 해석이다.
같은 취지의 말이 풀 리퀘스트 #68에 있다.
마칭 큐브를 최대 1024³까지 키우는 변경을 낸 thatname은 해상도가 크면 면이
날카로워지지만 본질은 보간이고 원래 triplane 해상도가 낮다고 적었다.[^pr-68]
이슈 #60은 해상도를 최대인 320으로 올리면 톱니 모양의 모서리가 눈에 띈다고
보고한다.[^issue-60]

### 색은 같은 triplane에서 읽고 조명이 섞여 있다

기본 출력은 정점 색이다.
`extract_mesh`가 마칭 큐브로 뽑은 정점마다 triplane에서 색을 질의한다.
정점 수는 입력에 따라 달라져서, 한 이슈의 작성자는 같은 설정에서 3만 삼각형부터
13만 삼각형까지 나왔다고 보고한다.[^issue-22]

`--bake-texture`는 `xatlas`로 UV를 펼치고, 텍스처의 각 칸에 해당하는 3D 위치에서
같은 triplane의 색을 질의해 채운다.
그러므로 `--texture-resolution`을 올려도 색의 근원은 같은 triplane이다.
칸이 늘면 색의 경계가 매끄러워질 수는 있어도 사진에 있던 잔 무늬가 되살아나지는
않는다고 읽힌다.
코드를 읽고 내린 이 문서의 해석이다.
이슈 #22의 첫 글도 텍스처 해상도가 낮고 자주 틀린다고 적고, 개발자가 아닌
사용자들이 블렌더에서 UV를 펼쳐 원본 사진을 입히거나 앞면에 원본 이미지를
투영하는 우회를 제안한다.[^issue-22]

조명이 색에 섞인다는 지적은 후속 모델의 설명에서도 보인다.
SF3D의 README는 색에서 조명을 걷어내고(delight) 재질 변수를 예측해 게임에 바로
쓸 수 있게 했다고 적는다.[^sf3d]
TripoSR이 그 일을 하지 않는다는 말을 이 README가 직접 하지는 않으므로, 이는
대비에서 읽어 낸 해석이다.

### 보이지 않는 면은 모델이 추정한다

단일 이미지에서 뒷면과 옆면을 채우는 것은 학습으로 얻은 사전 지식이다.
이슈 #89는 앞, 뒤, 옆 사진을 함께 넣을 수 있느냐고 묻는다.
이 문서가 읽은 범위에서는 같은 요청이 이어졌을 뿐 구현이나 답은
없었다.[^issue-89]
TRELLIS 스레드에서 hi_hi는 F-117 사진을 넣었더니 윤곽이 전혀 맞지 않았고 여러
각도의 이미지를 넣을 수 있기를 바랐다고 썼다.[^hi_hi]
한 장의 입력으로는 알 수 없는 면이 있고, 그 면의 모양은 모델의 취향이 된다.

## 비평

### 개선 항목별 기여를 보여 주는 실험이 논문에 없다

논문은 데이터 큐레이션, 렌더링, 채널 수 40, 마스크 손실, 국소 렌더링 감독을
개선으로 나열한다.
그러나 이 문서가 읽은 본문에는 각 항목을 빼고 학습한 비교가 없고, 결과 절은
완성된 모델과 다른 방법의 비교만 싣는다.
채널 수 40은 실험 평가에 따라 정했다고 하지만 그 수치는 나오지 않는다.
그래서 TGS나 OpenLRM과의 차이가 데이터 때문인지, 구조 때문인지, 학습 설정
때문인지 가를 수 없다.
기술 보고서라는 형식이 이를 허용하지만 개선이라는 말이 근거 없이 읽힌다는 비용이
있다.

### 비교는 저자가 고른 물체와 지표에서 이뤄졌다

평가 물체는 두 데이터셋에서 사람이 걸러 각각 약 300개로 줄인 것이다.
걸러 낸 이유는 단순한 형태가 점수를 부풀리는 편향 때문이라고 설명되어 합리적으로
들리지만, 걸러 낸 기준과 목록이 본문에 없어 다른 연구자가 같은 집합을 재현하기
어렵다.
TripoSR이 모든 표에서 가장 높거나 가장 낮은 값을 보이는 것은 사실이다.
다만 GSO의 FS@0.1에서 TGS는 0.637이고 TripoSR은 0.651이어서 차이가 작고, 이
차이가 측정의 잡음 범위 안인지는 논문이 다루지 않는다.
평가에서 정답과의 정렬을 사후에 회전 탐색과 ICP로 맞추므로 카메라 추정의 실패가
점수에 그대로 드러나지 않을 수 있다.
이는 이 문서의 해석이다.

### 한계와 실패 사례, 그리고 일반 GPU의 속도가 빠져 있다

논문에는 한계 절이나 실패 사례가 없고, 정성 비교 그림은 저자가 고른 성공 사례로
읽힌다.
속도도 A100 기준이어서 일반 사용자의 GPU에서의 시간은 알 수 없다.
README가 말하는 약 6GB VRAM이 현실적인 하한이라는 점만 확인된다.
또한 비교 대상에 원본 LRM이 없고, OpenLRM은 LRM 계열의 한 공개 구현이므로 개선을
LRM 대비라고 쓴 주장과는 간극이 있다.

### 공식 데모와 같은 결과를 못 얻는 이유는 대개 입력 준비에 있다

저장소의 예제 이미지는 전경을 오려 회색 배경에 놓은 전처리본이다.
로컬 실행 결과가 허깅페이스 데모와 다르다는 한 이슈에서 개발자는 전처리 차이일
수 있으니 `--no-remove-bg`로 돌려 보라고 답했고, rembg는 가벼운 전경 추출
도구이며 Clipdrop 같은 다른 도구가 더 나을 수 있다고 덧붙였다.[^issue-16]
보고자는 그 옵션을 줘도 다르다고 했고, 개발자가 같은 명령의 출력을 올려 데모와
일치한다고 했으며, 보고자가 마칭 큐브를 CPU로 바꾸는 수정을 했었다는 것까지 나온
뒤 이 문서가 읽은 범위에서 원인은 가려지지 않았다.[^issue-16]

이 비평의 요점은 모델 능력과 입력 준비를 함께 뭉뚱그려 평가하기 쉽다는 것이다.
배경 제거 결과, 전경 비율, 물체의 시점이 달라지면 같은 모델에서 다른 메시가
나온다.
입력을 통제하지 않은 채 결과가 별로라고 판단하면 원인이 모델인지 전처리인지
가려지지 않는다.

### 정량 표는 형태만 재고 사용자가 보는 것은 색과 표면이다

논문의 정량 비교는 메시 표면에서 뽑은 점 1만 개의 거리 지표(Chamfer Distance와
F-score)이다.
그래서 표면의 울퉁불퉁함, 구워 넣은 조명, 뭉개진 색은 표가 재지 않는 영역에
있다.
논문 스스로도 정성 비교에서 TripoSR의 재구성을 정점 색이 있는 것과 없는 것으로
나누어 렌더링했다고 적는다.
사용자가 아쉬워하는 부분과 저자들이 숫자로 증명한 부분이 겹치지 않을 수 있다.
이는 이 문서의 해석이다.

## 설치하기

요구 사항은 Python 3.8 이상이고 CUDA가 있으면 설치하며, 플랫폼에 맞는 PyTorch를
설치한다.
README는 로컬에 설치된 CUDA 주 버전이 PyTorch가 함께 가져오는 CUDA 주 버전과
같아야 한다고 강조한다(예: CUDA 11.x면 CUDA 11.x용 PyTorch).
이어 setuptools를 올리고 나머지 의존성을 설치한다.

```bash
pip install --upgrade setuptools
pip install -r requirements.txt
```

`run.py`와 Gradio 앱은 CUDA가 없으면 장치를 스스로 `cpu`로 바꾼다.
다만 `requirements.txt`가 `torchmcubes`를 소스에서 빌드하게 해서
설치가 걸리는 환경이 있고, 이 문제는 CPU, Intel GPU, Apple Silicon을 다루는
절에서 따로 다룬다.
같은 파일은 `transformers==4.35.0`, `Pillow==10.1.0`, `trimesh==4.0.5`,
`moderngl==5.10.0`, `xatlas==0.0.9`처럼 오래된 버전을 고정한다.
새 Python 환경에서 다른 패키지와 충돌할 수 있다는 점은 이 문서의 짐작이며 직접
설치해 보지는 않았다.

## 실행하기

한 장의 이미지에서 3D 모델을 만드는 기본 명령이다.

```bash
python run.py examples/chair.png --output-dir output/
```

복원된 모델이 `output/`에 저장되고, 이미지 경로를 공백으로 여러 개 줄 수 있다.
정점 색 대신 텍스처를 출력하려면 `--bake-texture`를 쓰고
`--texture-resolution`으로 텍스처 해상도(픽셀)를 정한다.
자세한 옵션은 `python run.py --help`에 있고, 브라우저에서 쓰려면 로컬 Gradio
앱을 띄운다.

```bash
python gradio_app.py
```

저장소는 `run.py`, `gradio_app.py`, `requirements.txt`, `tsr` 패키지, 예제
이미지로 이루어져 있다.

`run.py`가 받는 옵션을 코드에서 읽어 정리하면 다음과 같다.

| 옵션                              | 기본값                | 하는 일                                                            |
| --------------------------------- | --------------------- | ------------------------------------------------------------------ |
| `image`                           | 필수(여러 개 가능)    | 입력 이미지 경로                                                   |
| `--device`                        | `cuda:0`              | CUDA가 없으면 코드가 `cpu`로 바꾼다                                |
| `--pretrained-model-name-or-path` | `stabilityai/TripoSR` | 허깅페이스 모델 ID나 로컬 폴더                                     |
| `--chunk-size`                    | 8192                  | 렌더링과 표면 추출의 평가 묶음 크기. 작을수록 VRAM이 줄고 느려진다 |
| `--mc-resolution`                 | 256                   | 마칭 큐브 격자 해상도                                              |
| `--no-remove-bg`                  | 꺼짐                  | 배경 제거를 건너뛴다. 회색 배경에 크기가 맞은 RGB 입력이 필요하다  |
| `--foreground-ratio`              | 0.85                  | 이미지 대비 전경의 크기. 배경 제거를 쓸 때만 적용된다              |
| `--output-dir`                    | `output/`             | 결과 폴더                                                          |
| `--model-save-format`             | `obj`                 | `obj` 또는 `glb`                                                   |
| `--bake-texture`                  | 꺼짐                  | 정점 색 대신 텍스처 아틀라스를 굽는다                              |
| `--texture-resolution`            | 2048                  | 아틀라스 해상도. `--bake-texture`와 함께만 쓴다                    |
| `--render`                        | 꺼짐                  | NeRF로 30개 시점을 렌더링해 동영상으로 저장한다                    |

마칭 큐브의 임계값(`threshold`, 기본 25.0)은 `extract_mesh`의 인자이지만
`run.py`는 이 값을 옵션으로 내놓지 않는다.

## 값 정하기

| 항목           | 시작값                              | 근거                                                                                             |
| -------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------ |
| 입력           | 배경이 단순한 정면 사진 한 장       | 단일 이미지 복원이어서 가려진 면은 추정이다. 이는 이 문서의 해석이다                             |
| VRAM           | 6GB 이상                            | README가 이미지 한 장의 기본 설정이 약 6GB라고 밝힌다                                            |
| 생성 시간      | 환경마다 직접 잰다                  | 논문의 0.5초는 A100 기준이어서 다른 GPU의 시간은 어디에도 나와 있지 않다                         |
| 출력 색        | 정점 색                             | 텍스처는 `--bake-texture`를 켜야 하며 해상도는 `--texture-resolution`으로 정한다                 |
| CUDA와 PyTorch | 주 버전을 일치                      | 불일치가 가장 흔한 설치 오류의 원인이라고 README가 안내한다                                      |
| 전경 비율      | 0.85에서 시작해 0.7~0.95를 비교     | 공식 기본값이 0.85이고 Gradio 슬라이더는 0.5~1.0이다. Gradio 안내문이 이 값을 바꿔 보라고 권한다 |
| mc-resolution  | 128로 먼저 보고 256                 | triplane이 64×64라서 격자를 올려도 세부가 늘지 않는다는 해석이다. 비용은 해상도의 세제곱이다     |
| 임계값         | 25.0(코드 기본값)에서 5~10까지 비교 | 이슈 #12의 사용자 보고가 근거이며 개발자가 확인한 값은 아니다                                    |
| 텍스처 해상도  | 2048(기본값)                        | 색의 근원이 같은 triplane이라 올려도 세부는 늘지 않는다는 해석이다                               |
| chunk-size     | 8192(기본값)                        | 줄이면 VRAM이 줄고 느려진다고 `--help`가 밝힌다                                                  |

## 제대로 쓰는 법

공식 도구는 입력 준비와 마칭 큐브 설정과 색 처리를 사용자에게 맡긴다.
아래는 코드와 이슈에서 확인한 사실과 이 문서의 제안을 가려 적은 작업 흐름이다.
TripoSR 자체는 이 문서가 실행하지 못했고, 보조 스크립트만 합성 데이터로 돌렸다.

### 입력 이미지를 모델이 본 모양에 가깝게 만든다

공식 코드는 입력을 다음 순서로 다룬다.
이미지가 알파 채널을 갖고 투명한 픽셀이 하나라도 있으면 배경 제거를 건너뛴다.
그렇지 않으면 rembg로 배경을 지운다.
그다음 전경을 잘라 정사각형으로 채우고 `--foreground-ratio`(기본 0.85)가 되도록
가장자리를 넓힌 뒤 배경을 0.5 회색으로 채운다.
모델의 입력 해상도는 512이다.[^hf-card]

Gradio 앱의 안내문은 결과가 마음에 들지 않으면 전경 비율을 바꿔 보라고 한다.
배경 제거를 끄는 것은 입력이 투명 배경의 RGBA이고 내용이 가운데에 있으며 너비나
높이의 70%를 넘게 차지할 때만 하라고 한다.
그래서 직접 준비한 이미지에 `--no-remove-bg`를 쓸 때는 회색 배경과 정사각형
구도와 약 0.85의 전경 비율을 스스로 맞춰야 한다.
개발자는 rembg보다 나은 전경 추출 도구가 있을 수 있다고도 말한다.[^issue-16]

사진을 고를 때는 물체가 한 개이고 정면이나 정면에서 약간 비스듬한 시점이며,
조명이 고르고 강한 그림자와 원근 왜곡이 없는 쪽이 낫다고 본다.
이 조건은 이 문서의 제안이며 공식 문서나 논문이 요구한 것이 아니다.
학습 이미지의 분포가 어떤지는 논문 본문에서 구체적으로 확인하지 못했다.

아래 스크립트는 rembg 없이 numpy와 Pillow만으로 배경 색 추정, 전경 마스크,
정사각형 채움, 회색 합성, 512 리사이즈를 한다.
배경이 거의 균일한 사진에만 맞고, 공식 코드의 `resize_foreground`와 같은
방식으로 전경 비율을 맞춘다.
흰 배경 1600×1200 이미지의 오른쪽 아래에 작은 물체를 그린 합성 입력으로 돌렸다.

```python
"""TripoSR 입력 준비: 배경 추정 → 전경 마스크 → 정사각 패딩 → 회색 합성 → 512 리사이즈.

rembg 없이 numpy와 Pillow만 쓴다. 배경이 거의 균일한 사진에만 맞는다.
공식 tsr/utils.py의 resize_foreground와 같은 방식으로 전경 비율을 맞춘다.
"""
import sys
import numpy as np
from PIL import Image

GRAY = 0.5          # 공식 코드가 배경을 채우는 값 (0.5)
RATIO = 0.85        # 공식 기본 전경 비율
OUT = 512           # 모델 입력 해상도 (config.yaml의 cond_image_size)


def foreground_mask(rgb: np.ndarray, tol: float = 24.0) -> np.ndarray:
    """네 모서리 20x20 픽셀의 중앙값을 배경색으로 보고 색 거리로 마스크를 만든다."""
    h, w, _ = rgb.shape
    k = 20
    corners = np.concatenate([
        rgb[:k, :k].reshape(-1, 3), rgb[:k, -k:].reshape(-1, 3),
        rgb[-k:, :k].reshape(-1, 3), rgb[-k:, -k:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)
    return dist > tol


def prepare(img: Image.Image, ratio: float = RATIO, out: int = OUT):
    rgba = np.array(img.convert("RGBA"))
    if rgba[..., 3].min() < 255:                 # 이미 투명 배경이면 알파를 쓴다
        mask = rgba[..., 3] > 0
        source = "alpha"
    else:
        mask = foreground_mask(rgba[..., :3])
        source = "background-color"
    ys, xs = np.where(mask)
    y1, y2, x1, x2 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    fg = rgba[y1:y2, x1:x2].astype(np.float32) / 255.0
    m = mask[y1:y2, x1:x2][..., None].astype(np.float32)
    size = max(fg.shape[:2])
    canvas_side = int(round(size / ratio))
    canvas = np.full((canvas_side, canvas_side, 3), GRAY, dtype=np.float32)
    oy = (canvas_side - fg.shape[0]) // 2
    ox = (canvas_side - fg.shape[1]) // 2
    region = canvas[oy:oy + fg.shape[0], ox:ox + fg.shape[1]]
    region[:] = fg[..., :3] * m + region * (1 - m)
    result = Image.fromarray((canvas * 255).astype(np.uint8)).resize(
        (out, out), Image.LANCZOS)
    info = {
        "mask_source": source,
        "input_size": img.size,
        "bbox_xyxy": (int(x1), int(y1), int(x2), int(y2)),
        "fg_ratio_before": round(size / max(img.size), 3),
        "fg_ratio_after": round(size / canvas_side, 3),
        "output_size": result.size,
    }
    return result, info


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    image, info = prepare(Image.open(src))
    image.save(dst)
    for k, v in info.items():
        print(f"{k}: {v}")
    arr = np.array(image)
    print("corner pixel (should be gray 127/128):", tuple(arr[0, 0]))
```

```text
mask_source: background-color
input_size: (1600, 1200)
bbox_xyxy: (1000, 560, 1401, 1101)
fg_ratio_before: 0.338
fg_ratio_after: 0.851
output_size: (512, 512)
corner pixel (should be gray 127/128): (np.uint8(127), np.uint8(127), np.uint8(127))
```

전경이 이미지의 33.8%였던 입력이 85.1%로 맞춰지고 모서리 픽셀이 회색 127이
되었다.
마스크가 틀리면 이 비율도 틀어지므로 실제 사진에서는 `mask_source`와
`bbox_xyxy`를 눈으로 확인해야 한다.

### 마칭 큐브: 해상도와 임계값

`extract_mesh`는 `resolution=256`과 `threshold=25.0`을 기본값으로 받는다.
`run.py`는 해상도만 옵션으로 내놓으므로 임계값을 바꾸려면 파이썬 API를 직접
부른다.
아래는 코드에서 읽은 호출이며 이 문서가 실행하지는 않았다.

```python
import torch
from tsr.system import TSR

model = TSR.from_pretrained(
    "stabilityai/TripoSR", config_name="config.yaml", weight_name="model.ckpt"
)
model.renderer.set_chunk_size(8192)
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)

with torch.no_grad():
    # image는 위 스크립트가 만든 512x512 PIL 이미지
    scene_codes = model([image], device=device)

# 임계값을 바꿔 가며 같은 scene_codes에서 메시만 다시 뽑는다
for t in (25.0, 10.0, 5.0):
    mesh = model.extract_mesh(scene_codes, True, resolution=256, threshold=t)[0]
    mesh.export(f"mesh_t{int(t)}.glb")
```

`scene_codes`를 한 번 만들어 두면 메시 추출만 되풀이하므로 임계값과 해상도를
비교하는 비용이 낮다.
마칭 큐브는 `-(density - threshold)`의 0 등치면을 표면으로 삼는다.
이슈 #12에서 mr-lab은 코드의 임계값을 25에서 5로 낮췄더니 사과 같은 단단한
물체가 나아졌고, 나무처럼 복잡한 물체는 10 아래로 내리면 커다란 덩어리가 된다고
적었다.[^issue-12]
한 사용자의 보고이며 개발자가 확인하지는 않았다.
같은 글에서 그는 해상도를 올려도 효과가 없고 512에서 약 21GB, 1024에서 약 44GB의
VRAM이 든다고 했다.[^issue-12]

해상도를 크게 올리는 비용을 줄이는 변경도 있다.
풀 리퀘스트 #68은 삼각 평면 샘플링을 128³ 블록 단위로 나눠 1024³ 메시를 RTX
3090에서 33초, VRAM 13GB로 만든다고 적지만 병합되지 않았다.[^pr-68]
아래는 격자 해상도별 비용과 triplane 해상도와의 비율을 계산한 스크립트와
출력이다.

```python
"""마칭 큐브 격자 해상도별 질의 점 수와 밀도 격자 메모리, 그리고 triplane 해상도와의 비율.
radius=0.87(config.yaml)이고 triplane이 같은 정육면체를 덮는다고 가정한 계산이다."""
radius, plane = 0.87, 64                 # 논문 Table 1: 업샘플 후 triplane 64x64x40
side = 2 * radius
print(f"cube side = {side:.2f}  triplane texel = {side/plane:.4f}")
for res in (64, 128, 256, 320, 512):
    pts = res ** 3
    mb = pts * 4 / 1e6                   # float32 밀도 한 채널
    print(f"mc_res={res:4d}  points={pts:>12,d}  density grid={mb:8.1f} MB  "
          f"voxel={side/res:.4f}  voxels per triplane texel={plane and (res/plane):.1f}")
```

```text
cube side = 1.74  triplane texel = 0.0272
mc_res=  64  points=     262,144  density grid=     1.0 MB  voxel=0.0272  voxels per triplane texel=1.0
mc_res= 128  points=   2,097,152  density grid=     8.4 MB  voxel=0.0136  voxels per triplane texel=2.0
mc_res= 256  points=  16,777,216  density grid=    67.1 MB  voxel=0.0068  voxels per triplane texel=4.0
mc_res= 320  points=  32,768,000  density grid=   131.1 MB  voxel=0.0054  voxels per triplane texel=5.0
mc_res= 512  points= 134,217,728  density grid=   536.9 MB  voxel=0.0034  voxels per triplane texel=8.0
```

### 텍스처: 구워 넣기와 바깥에서 입히기

`--bake-texture`는 `xatlas`로 UV를 만들고 텍스처 각 칸의 3D 위치에서 triplane
색을 질의한다.
코드를 읽어 보면 `positions_to_colors`가 위치 텐서를 장치 지정 없이 CPU에 만들고
결과를 곧바로 `.numpy()`로 바꾼다.
이슈 #100은 이 옵션이 GPU에서 실패하고 `--device cpu`로 바꾸면 텍스처 파일이
생긴다고 보고하며, 이슈 안의 댓글이 `positions_to_colors`를 고치는 코드를
제안한다.[^issue-100]
작성자는 이어서 `--device cuda:0`에 `--model-save-format glb`를 함께 주면
된다고도 적어, 어떤 조건에서 실패하는지는 이 문서가 가리지 못했다.
코드 읽기와 보고가 맞아 보이지만 이 문서는 실행하지 못했다.

색의 근원이 같은 triplane이므로, 텍스처를 구운 결과가 여전히 흐릿하면 해상도를
더 올리기보다 바깥에서 입히는 쪽을 고려한다.
이슈 #22는 블렌더에서 UV를 펼치고 원본 사진을 텍스처로 쓰는 방법과, 앞면에 원본
이미지를 투영하는 함수를 제안한다.[^issue-22]
제3자의 `triposr-texture-gen`은 TripoSR이 만든 모델의 텍스처를 생성한다고
소개하는 저장소이다.[^texgen]
`TripoSR-Bake`는 마칭 큐브 결과와 NeRF 예측을 따로 저장해 구워 넣는 접근이었으나
폐기(deprecated)되었고, README가 Meshfinity나 공식 저장소를 쓰라고
안내한다.[^tripo-bake]

### 메시 정리: 용접, 조각 제거, 구멍 메우기, 평활, 면 줄이기

마칭 큐브가 뽑은 메시는 떠다니는 조각과 구멍과 울퉁불퉁한 표면을 가질 수 있다.
아래 스크립트는 합성 메시로 정리 순서를 보인다.
입력은 노이즈를 더한 구에 구멍 3곳과 떠다니는 작은 구를 붙이고 정점을 용접하지
않은 합성 메시이다.
TripoSR의 출력이 아니다.

```python
"""TripoSR 계열 출력 메시 정리: 용접, 퇴화 면 제거, 떠다니는 조각 제거, 구멍 메우기,
라플라시안 평활, 쿼드릭 간소화. 입력은 합성 메시(합성 데이터)로 대체해 돌린다."""
import numpy as np
import trimesh
from trimesh import smoothing, repair

rng = np.random.default_rng(7)


def make_bad_mesh() -> trimesh.Trimesh:
    """노이즈가 낀 구 + 구멍 + 떠다니는 조각 + 용접되지 않은 중복 정점."""
    sphere = trimesh.creation.icosphere(subdivisions=5, radius=1.0)
    v = sphere.vertices + rng.normal(0, 0.012, sphere.vertices.shape)  # 표면 노이즈
    f = sphere.faces
    keep = np.ones(len(f), bool)
    for c in rng.choice(len(f), 3, replace=False):                       # 구멍 3곳
        near = np.where(np.linalg.norm(sphere.triangles_center - sphere.triangles_center[c], axis=1) < 0.12)[0]
        keep[near] = False
    f = f[keep]
    floater = trimesh.creation.icosphere(subdivisions=2, radius=0.06)
    floater.apply_translation([1.4, 0.3, 0.2])                           # 떠다니는 조각
    # 용접 해제: 면마다 정점을 따로 둔다 (process=False)
    tri = v[f].reshape(-1, 3)
    mesh = trimesh.Trimesh(tri, np.arange(len(tri)).reshape(-1, 3), process=False)
    return trimesh.util.concatenate([mesh, floater])


def report(tag: str, m: trimesh.Trimesh) -> None:
    comps = len(m.split(only_watertight=False))
    r = np.linalg.norm(m.vertices - m.vertices.mean(axis=0), axis=1)
    print(f"{tag:10s} verts={len(m.vertices):6d} faces={len(m.faces):6d} "
          f"watertight={str(m.is_watertight):5s} components={comps:2d} "
          f"radius_std={r[r < 1.3].std():.4f}")


def fill_boundary_loops(m: trimesh.Trimesh) -> int:
    """trimesh.repair.fill_holes는 삼각형 한 개나 사각형 한 개짜리 구멍만 메운다.
    그보다 큰 구멍은 경계 모서리를 고리로 이어 중심점 부채꼴로 직접 메운다."""
    edges = m.edges_sorted
    uniq, counts = np.unique(edges, axis=0, return_counts=True)
    boundary = uniq[counts == 1]
    if len(boundary) == 0:
        return 0
    adj = {}
    for a, b in boundary:
        adj.setdefault(int(a), []).append(int(b))
        adj.setdefault(int(b), []).append(int(a))
    seen, loops = set(), []
    for start in list(adj):
        if start in seen:
            continue
        loop, cur, prev = [start], start, None
        seen.add(start)
        while True:
            nxt = [n for n in adj[cur] if n != prev and n not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            loop.append(cur)
            seen.add(cur)
        if len(loop) >= 3:
            loops.append(loop)
    verts = m.vertices.tolist()
    faces = m.faces.tolist()
    for loop in loops:
        center = m.vertices[loop].mean(axis=0)
        verts.append(center.tolist())
        c = len(verts) - 1
        for i in range(len(loop)):
            faces.append([loop[i], loop[(i + 1) % len(loop)], c])
    m.vertices = np.array(verts)
    m.faces = np.array(faces)
    return len(loops)


def clean(m: trimesh.Trimesh, target_faces: int = 20000) -> trimesh.Trimesh:
    m = m.copy()
    m.merge_vertices()                       # 1. 위치가 같은 정점 용접
    m.update_faces(m.nondegenerate_faces())  # 2. 면적 0인 면 제거
    parts = m.split(only_watertight=False)   # 3. 가장 큰 덩어리만 남김
    m = max(parts, key=lambda p: len(p.faces))
    repair.fill_holes(m)                     # 4. 작은 구멍은 trimesh가, 큰 구멍은 직접
    n_loops = fill_boundary_loops(m)
    print(f"filled {n_loops} boundary loops by fan")
    m.merge_vertices()
    repair.fix_normals(m)
    smoothing.filter_laplacian(m, iterations=6)   # 5. 평활 (부피가 조금 줄어든다)
    if len(m.faces) > target_faces:          # 6. 면 수 줄이기
        m = m.simplify_quadric_decimation(face_count=target_faces)
    return m


if __name__ == "__main__":
    bad = make_bad_mesh()
    report("before", bad)
    good = clean(bad)
    report("after", good)
    print(f"volume after = {good.volume:.3f} (unit sphere = {4/3*np.pi:.3f})")
    good.export("cleaned_synthetic.glb")
    print("exported cleaned_synthetic.glb")
```

```text
before     verts= 60960 faces= 20586 watertight=False components=20267 radius_std=0.0120
filled 3 boundary loops by fan
after      verts= 10002 faces= 20000 watertight=True  components= 1 radius_std=0.0093
volume after = 4.187 (unit sphere = 4.189)
exported cleaned_synthetic.glb
```

정리 전 `components=20267`은 정점을 용접하지 않아 면마다 조각으로 센 값이다.
용접하면 본체 하나와 떠다니는 조각 하나가 남고, 가장 큰 쪽만 남겼다.
정리 뒤 메시는 닫혔고(watertight) 구의 부피 4.189에 가까운 4.187이 되었다.
평활은 표면 노이즈를 0.0120에서 0.0093으로 줄였고, 반복할수록 부피가 줄어드는
대가가 있다.

이 실행에서 확인한 함정이 하나 있다.
`trimesh.repair.fill_holes`는 삼각형 한 개나 사각형 한 개로 막히는 구멍만
메운다.
반지름 0.12쯤의 구멍 3곳(경계 모서리 72개)은 이 함수로 메워지지 않았고, 경계
고리를 찾아 중심점으로 잇는 부채꼴을 직접 만들어서야 닫혔다.
실제 TripoSR 메시에서도 같은 일이 생기는지는 확인하지 못했다.

블렌더에서는 거리로 정점 병합, 평활, 면 줄이기(Decimate)의 순서가 흔한
시작점이라고 본다.
이 순서는 이 문서의 제안이다.
TRELLIS 스레드에서 RugnirViking은 거리로 정점을 병합하는 일이 모델을 블렌더에
가져올 때마다 첫 단계라고 썼다.[^RugnirViking]

### 작업 순서

1. 한 물체가 가운데에 오고 그림자가 적은 사진을 고른다.
2. 위 스크립트나 외부 도구로 배경을 지우고 회색 512 정사각형으로 맞춘다.
3. 같은 입력을 공식 데모(허깅페이스 Space)에도 넣어 로컬 결과와 비교한다.
4. 기본값으로 만들고, 같은 `scene_codes`에서 해상도 128과 256,
임계값 25와 10을 비교한다.
5. 메시를 정리한다.
용접, 떠다니는 조각 제거, 구멍 메우기, 평활, 면 줄이기 순이다.
6. 색이 필요하면 정점 색이나 `--bake-texture`를 쓰고,
부족하면 바깥에서 입힌다.
7. 앞의 단계로 해결되지 않는 증상은 뒤의 증상별 표를 보고 모델을 바꾼다.

## CPU와 Apple Silicon과 Intel GPU에서 돌리기

Stability AI의 공개 글은 이 모델이 낮은 추론 예산에서, 심지어 GPU 없이도
돌아간다고 소개한다.[^stability-blog]
공식 코드도 CUDA가 없으면 `cpu`로 돌아간다.
걸림돌은 모델이 아니라 마칭 큐브 구현이라고
풀 리퀘스트 #153의 작성자는 설명한다.
`torchmcubes`가 네이티브 CUDA 확장을 컴파일해야 해서
TripoSR이 사실상 CUDA 전용이었다는 것이다.[^pr-153]
README의 문제 해결 절이 다루는 오류 메시지는 CUDA 없이 컴파일된 경우이므로,
CPU만으로 빌드가 가능한지는 이 문서가 확인하지 못했다.

공개된 측정과 변경은 다음과 같다.
모두 작성자 한 사람의 환경에서 잰 값이며 이 문서는 어느 것도 재현하지 못했다.

| 출처                     | 환경                                       | 내용                                                                                                                                                                                            |
| ------------------------ | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 풀 리퀘스트 #153(미병합) | Intel Arc Pro B70, `torch+xpu`, 해상도 256 | 같은 입력에서 CPU는 모델 추론 3,899ms와 메시 추출 9,871ms, XPU는 1,541ms와 1,685ms이고 정점과 면의 수가 같다. CPU 기종은 PR 본문 발췌에 보이지 않았다.[^pr-153]                                 |
| 풀 리퀘스트 #153(미병합) | 위와 같음                                  | `torchmcubes`를 못 쓸 때 `PyMCubes`로 대체하는 코드를 더한다.[^pr-153]                                                                                                                          |
| 풀 리퀘스트 #155(미병합) | Apple M4 Pro, MPS                          | CUDA, MPS, CPU 순으로 장치를 고르고 마칭 큐브는 CPU 구현을 쓴다. 해상도 128에서 정점 13,030개와 면 25,976개의 OBJ가 나왔다고 적는다.[^pr-155]                                                   |
| `tripo-mlx`              | Apple Silicon M3 16GB                      | 신경망 추론을 MLX로 돌리고 배경 제거와 표면 추출과 텍스처 굽기는 CPU로 한다. 체크포인트를 변환하면 약 1.68GB의 float32 가중치가 하나 더 생기고 `--resolution`은 32에서 256까지이다.[^tripo-mlx] |

두 풀 리퀘스트 모두 병합되지 않았으므로, 지금 공식 저장소를 그대로 받으면 CUDA가
없는 환경에서는 `torchmcubes`를 직접 해결해야 한다.
`PyMCubes`로 바꾸는 방법은 풀 리퀘스트의 코드를 참고할 수 있다.
이는 이 문서가 풀 리퀘스트 설명을 읽고 정리한 것이다.

같은 계열의 후속 모델은 CPU 경로를 공식 문서로 안내한다.
SF3D의 README는 GPU가 없으면 CPU 백엔드를 자동으로 쓰고 `SF3D_USE_CPU=1`로
강제할 수 있다고 적으며, MPS는 CUDA보다 메모리를 많이 쓰므로 통합 메모리가
32GB보다 작으면 CPU를 권한다고 적는다.[^sf3d]
SPAR3D의 README는 CPU는 아주 느리다고 밝히고 `--device=cpu`와
`SPAR3D_USE_CPU=1`을 안내한다.[^spar3d]

## 다른 모델로 갈아탈 때

TripoSR이 가볍고 라이선스가 단순한 대신 품질에 천장이 있다는 점은 위에서 따졌다.
아래 표는 갈아탈 후보를 각 저장소와 모델 카드에서 읽은 사실로만 비교한다.
품질은 직접 비교하지 않았으므로 칸에 적지 않았다.
하드웨어 칸은 공식 문서가 밝힌 숫자이고 기준이 다르다.

| 모델           | 라이선스                       | 공식 문서의 하드웨어       | 소개 문구가 말하는 개선점                                          |
| -------------- | ------------------------------ | -------------------------- | ------------------------------------------------------------------ |
| TripoSR        | MIT                            | 약 6GB VRAM(기본 설정)     | 단일 이미지, 빠른 초안                                             |
| SF3D           | Stability AI Community License | 약 6GB VRAM, CPU 자동 전환 | TripoSR 기반으로 UV 펼친 텍스처, 조명 제거, 재질 변수 예측[^sf3d]  |
| SPAR3D         | 위와 같음                      | 10.5GB, 저VRAM 모드 약 7GB | 포인트 클라우드로 뒷면을 개선하고 편집할 수 있음[^spar3d]          |
| TripoSG        | MIT                            | 8GB 이상                   | 정류 흐름(rectified flow) 기반의 고충실도 형태 생성[^triposg]      |
| InstantMesh    | Apache-2.0                     | 문서가 숫자를 밝히지 않음  | 다중 시점 생성 뒤 희소 시점 재구성[^instantmesh]                   |
| TRELLIS        | MIT                            | 16GB 이상                  | 여러 이미지를 조건으로 주는 기능[^trellis]                         |
| TRELLIS.2      | MIT                            | 24GB 이상                  | 4B 매개변수, 열린 표면과 PBR 재질, H100에서 512³ 약 3초[^trellis2] |
| Step1X-3D      | Apache-2.0                     | 27~29GB(50단계 152초)      | 형태와 텍스처를 함께 생성[^step1x]                                 |
| SAM 3D Objects | SAM License                    | 문서에서 확인하지 못함     | 가림과 어수선한 장면에 강한 형태, 질감, 배치 복원[^sam3d]          |

Hunyuan3D 계열은 라이선스에 지역 제한이 있어 따로 다룬
문서(graphics/hunyuan3d.md)를 본다.
SF3D와 SPAR3D의 라이선스는 모델 카드에서 `other`로 표기되고 접근 승인이
필요하며, LICENSE의 서두는 연구, 비상업, 제한적인 상업 이용을 무료로 허락한다고
밝힌다.[^sf3d][^hf-sf3d]
SAM 3D Objects의 모델 카드는 수동 승인(gated)이다.[^hf-sam3d]
라이선스 본문은 끝까지 읽지 않았으므로 상업 이용 전에 직접 확인해야 한다.

### 증상별로 무엇을 바꿀지

| 증상                          | 먼저 바꿀 것                                     | 그래도 안 되면                                                   |
| ----------------------------- | ------------------------------------------------ | ---------------------------------------------------------------- |
| 표면이 울퉁불퉁하고 뭉툭하다  | 전경 비율, 배경 제거 품질, 해상도 128과 256 비교 | 메시 평활과 면 줄이기. 모양 자체가 문제면 TripoSG나 TRELLIS 계열 |
| 뒷면이 납작하거나 엉뚱하다    | 시점이 분명한 입력으로 교체                      | 포인트 클라우드를 쓰는 SPAR3D나 다중 시점 파이프라인             |
| 색이 흐리고 조명이 섞여 있다  | `--bake-texture` 또는 바깥에서 재텍스처          | 조명을 걷어내는 SF3D나 PBR을 내는 TRELLIS.2                      |
| 구멍이나 떠다니는 조각이 있다 | 임계값 조정                                      | 위의 정리 스크립트                                               |
| 설치에서 막힌다               | `torchmcubes` 재설치, CUDA 주 버전 일치          | CUDA가 필요 없는 후속 모델의 CPU 경로나 `tripo-mlx`              |

### 다중 시점을 먼저 만들고 재구성하는 흐름

TripoSR의 한계 중 하나가 한 장에서 보이지 않는 면을 추정하는 것이라면, 그 면을
먼저 이미지로 만들고 재구성하는 접근이 있다.
InstantMesh의 README는 맞춤 Zero123++ UNet으로 흰 배경 다중 시점 이미지를 만들고
희소 시점 재구성 모델 네 가지 중 하나로 메시를 뽑는 구조를 설명한다.
기본값은 `instant-mesh-large`이고, 이미 알파 마스크가 있으면 `--no_rembg`를,
텍스처 맵을 내려면 `--export_texmap`(시간이 더 걸린다)을 준다.[^instantmesh]

이 흐름의 앞 단계인 Zero123++는 v1.2에서 출력 시야각을 30°로 통일하고 고정
고도를 20°와 -10°로 바꿨으며, 보이는 면의 노멀 이미지를 만드는 컨트롤넷도
제공한다.
코드는 Apache 2.0이고 모델 가중치는 CC-BY-NC 4.0이라 상업 제품 파이프라인에는 쓸
수 없고 출력은 자유롭게 쓸 수 있다고 README가 밝힌다.[^zero123plus]
InstantMesh의 모델 카드 라이선스는 Apache-2.0으로 표기되어 있으나 이 문서는 맞춤
UNet의 조건을 따로 확인하지 못했다.[^hf-instantmesh]
같은 목적의 다중 시점 생성기로는 MV-Adapter(Apache-2.0)와 Wonder3D(MIT)도
있다.[^mvadapter][^wonder3d]

정리하면 이미지 한 장에서 시작해 깔끔한 컷아웃, 다중 시점 확산, 재구성, 메시
정리의 순서로 간다.
실제로 이 순서가 TripoSR보다 나은 결과를 내는지는 이 문서가 같은 입력으로
비교하지 못했다.

## 파생 프로젝트와 도구

아래는 2026년 10월 27일에 GitHub에서 검색해 본 TripoSR 관련 저장소이다.
별 수와 마지막 푸시는 그날 GitHub API가 알려 준 값이다.

| 저장소                           | 별  | 마지막 푸시 | 라이선스  | 설명                                                                               |
| -------------------------------- | --- | ----------- | --------- | ---------------------------------------------------------------------------------- |
| flowtyone/ComfyUI-Flowty-TripoSR | 545 | 2024-06-16  | GPL-3.0   | ComfyUI 사용자 지정 노드. `model.ckpt`를 `models/checkpoints`에 두고 쓴다[^flowty] |
| ejones/triposr-texture-gen       | 113 | 2024-03-21  | MIT       | TripoSR이 만든 3D 모델의 텍스처를 생성한다[^texgen]                                |
| mapluisch/TripoSR-for-Unity      | 66  | 2024-03-23  | MIT       | 유니티에서 메시를 만들고 다시 텍스처를 입힌다[^unity]                              |
| iffyloop/TripoSR-Bake            | 57  | 2024-10-17  | Unlicense | 폐기됨. Meshfinity나 공식 저장소를 쓰라고 안내한다[^tripo-bake]                    |
| sachaarbonel/tripo-mlx           | 1   | 2026-10-14  | MIT       | Apple Silicon용 MLX 추론과 MV-Adapter 텍스처 도구[^tripo-mlx]                      |

ComfyUI 노드의 마지막 푸시가 2024년 6월이고 라이선스가 GPL-3.0이라, 최신
ComfyUI와의 호환과 라이선스 파급을 따로 확인해야 한다.

## 함정

README의 문제 해결 절은 하나다.
`torchmcubes_module`에 `mcubes_cuda` 속성이 없다거나 `torchmcubes`가 CUDA 지원
없이 컴파일되었다는 오류는 `torchmcubes`가 CUDA 없이 빌드되었기 때문이다.
CUDA 주 버전이 PyTorch의 것과 같은지, `setuptools`가 49.6.0 이상인지 확인한 뒤
`torchmcubes`를 지우고 다시 설치한다.

```bash
pip uninstall torchmcubes
pip install git+https://github.com/tatsy/torchmcubes.git
```

### 로컬 결과가 공식 데모와 다르다

예제 이미지는 이미 전처리되어 있어서 `--no-remove-bg`를 주지 않으면 배경 제거가
한 번 더 걸리고 결과가 달라질 수 있다.
개발자도 이 점을 먼저 짚는다.[^issue-16]
같은 입력으로 로컬과 데모를 비교한 뒤에야 자기 입력의 문제인지 환경의 문제인지
가려진다.

### Gradio 미리보기의 방향과 밝기

Gradio 앱의 화면은 OBJ가 뒤집혀 보이고 GLB가 더 어둡게 보이므로 내려받은 파일이
올바른 결과라고 앱 코드가 안내한다.
미리보기만 보고 방향이나 색을 판단하면 틀린다.

### 처음 실행할 때 내려받는 것들

`run.py`는 처음 실행할 때 허깅페이스에서 약 1.68GB의 체크포인트와 설정 파일을
받고, 이미지 인코더 구성을 위해 `facebook/dino-vitb16`의 `config.json`도 받는다.
배경 제거에 쓰는 rembg도 처음 쓸 때 자기 모델 가중치를 내려받는다고
`tripo-mlx`의 README가 밝힌다.[^tripo-mlx]
오프라인 환경이나 용량 제한이 있는 환경에서는 미리 받아 두거나
`--pretrained-model-name-or-path`에 로컬 폴더를 줘야 한다.

### 마칭 큐브와 텍스처 굽기의 장치 문제

`--bake-texture`는 GPU에서 실패한다는 보고가 있고 CPU에서는 된다고
한다.[^issue-100]
`torchmcubes`는 CUDA 없이 컴파일되면 위의 오류가 난다.
둘 다 CUDA를 쓰는 환경에서 오히려 문제가 생기는 곳이라는 점에서, 장치 선택을
코드가 알아서 해 준다고 믿으면 안 된다.

## 비공식 사이트

### triposrai.com이 무엇인가

TripoSR AI라는 이름의 웹사이트다.
2026년 10월 27일에 읽은 페이지의 제목은 단일 이미지에서의 오픈소스 3D 복원을
내세우고, 첫 화면 문구는 2D 이미지 한 장에서 고품질 3D 에셋을 빠르게 만든다는
것이다.
페이지에는 글, 도구, 태그, 소개, 개인정보 처리방침과 쿠키 정책 메뉴가 있고,
광고가 곳곳에 붙어 있다.
화면에는 Tripo 3D의 스폰서 광고(텍스트로 3D 모델 만들기, `studio.tripo3d.ai`)도
있다.

FAQ는 TripoSR을 Tripo AI와 Stability AI가 함께 개발한 최신 오픈소스 단일 이미지
3D 복원 모델이라고 설명한다.
ComfyUI 통합 노력과 텍스처 해상도를 높이는 스크립트가 커뮤니티에 있다고
안내하고, 시작하려면 TripoSR GitHub 설치 도우미를 쓰라고 한다.
사이트가 제공하는 도구와 안내는 GitHub 설치 도우미, ComfyUI 워크플로 생성기와
노드 안내, Blender 애드온 워크플로, API 튜토리얼, TripoSR과 SF3D 비교, 오픈소스
3D 복원 도구 비교다.
설치 도우미 설명에는 안전한 다운로드와 로컬 설치 명령, PyTorch와 CUDA 설정, APK
위험 안내가 들어 있다.
글 목록은 2025년과 2026년의 TripoSR 활용 글(전자상거래, 건축 시각화, 기업 배포,
마켓플레이스 사례)을 담는다.

### 공식 저장소와 어떻게 다른가

사이트는 공식 저장소로 가라는 안내를 여러 번 하고, 다운로드와 APK의 위험을
경고한다.
광고와 스폰서 배너가 붙은 구조, 설치와 다운로드와 GitHub 같은 검색어 중심의 글
제목은 이 사이트가 공식 저장소가 아니라 검색을 겨냥한 안내 사이트로 읽히는
근거다.
이 사이트가 TripoSR을 개발한 조직과 관련 있다는 표시는 이 문서가 읽은 페이지에서
확인되지 않았다.
이는 이 문서의 해석이다.

사이트의 설명은 공식 문서와 어긋나는 곳이 있다.
FAQ의 기술 설명(이미지를 NumPy 배열로 처리해 전처리된 이미지와 메시 파일 이름의
튜플을 돌려준다는 식)은 모델의 동작이 아니라 함수 호출의 일부를 말한다.
사이트의 글 일부는 TripoSR v2.0과 다중 시점 복원을 말하지만, 이 문서가 읽은 공식
README는 단일 이미지 복원 모델이라고만 설명한다.
이 불일치는 사이트의 모든 글을 읽지 못해 확정하지 못했고, 공식 README를 기준으로
삼는 것이 안전하다.

### 받을 파일은 어디서 받는가

TripoSR 다운로드나 APK를 찾는 사람이 공식 경로가 아닌 파일을 받을 위험이 있다고
사이트가 직접 경고한다.
공식 코드는 GitHub의 `VAST-AI-Research/TripoSR` 저장소이고 설치는 위 설치하기
절을 따른다.
사이트가 도구로 제공하는 다운로드(ComfyUI 워크플로 JSON 등)는 이 문서가 열어
보지 않았으므로, 출처가 불분명한 파일은 공식 저장소의 파일과 대조해야 한다.

## 트레이드오프

### 공짜의 대가는 설치와 하드웨어이고 기능은 서비스에 못 미친다

크레딧도 구독도 필요 없지만 CUDA 지원 GPU와 PyTorch와 컴파일 의존성을 직접
맞춰야 한다.
이 저장소는 단일 이미지 복원 하나를 제공하고, 상용 서비스가 주는 리깅, 스마트
분할, 8K 텍스처 같은 기능은 들어 있지 않다.
이는 이 문서가 두 곳의 설명을 비교한 해석이며 품질을 직접 비교해 보지는 않았다.

### 단일 이미지 입력은 보이지 않는 면을 추정한다

한 장에서 3D를 복원하는 방식은 뒷면 같은 보이지 않는 부분을 모델이 채운다.
정확한 형상이 필요한 제품이라면 다중 시점이나 실측이 필요하다.
README도 논문도 이 한계를 따로 설명하지 않는다.

### 가볍게 쓰는 대신 품질의 천장이 낮다

TripoSR은 약 6GB VRAM이나 CPU에서 돌고 MIT 라이선스라 제약이 없다.
후속 모델은 개선점을 내세우는 대신 하드웨어를 더 쓴다.
공식 문서 기준으로 TRELLIS는 16GB 이상, TRELLIS.2는 24GB 이상, Step1X-3D는 27GB
이상이다.[^trellis][^trellis2][^step1x]
가벼움과 품질을 함께 얻을 수는 없다.
다만 SF3D는 같은 약 6GB 안에서 UV와 재질을 더한다고 소개하므로 중간 선택지가
된다.[^sf3d]
이는 이 문서가 공식 문서의 숫자만 비교한 해석이며 품질은 직접 비교하지 못했다.

### 전처리와 후처리에 쓰는 시간이 결과를 좌우한다

입력을 통제하고 메시를 정리하는 일은 모델 밖에서 사람이 하는 작업이다.
이 작업이 익숙해지면 같은 모델에서 더 나은 결과를 얻지만, 그 시간은 서비스의 한
번 클릭과 맞바꾸는 비용이다.
후속 모델이나 유료 서비스로 옮기면 이 시간 일부를 돈이나 하드웨어로 바꾸게 된다.

## 체크리스트

- Python 3.8 이상과 PyTorch를 설치했고 CUDA 주 버전이 일치하는가.
- `pip install -r requirements.txt`가 오류 없이 끝났는가.
- `python run.py examples/chair.png --output-dir output/`가 6GB 안팎의 VRAM에서
돌아가는가.
- 같은 입력을 공식 데모에 넣어 로컬 결과와 비교했는가.
- 직접 준비한 입력은 회색 배경, 정사각형, 전경 비율 약 0.85인가.
- 해상도를 128과 256으로, 임계값을 25와 10으로 비교했는가.
- 텍스처가 필요하면 `--bake-texture`를 줬고, GPU에서 실패하면 CPU로 돌려 봤는가.
- 메시의 떠다니는 조각과 구멍을 정리했고 면 수를 목적에 맞게 줄였는가.
- `torchmcubes` CUDA 오류가 나면 지우고 다시 설치했는가.
- 결과가 요구에 못 미치면 증상별 표를 보고 모델 교체를 검토했는가.
- 파일을 공식 저장소나 Hugging Face에서만 받았는가.
- 결과물을 상업적으로 쓰기 전에 MIT 라이선스 고지를 지켰는가.

## 기억할 원칙

### 서비스가 막는 곳에서 오픈 모델이 길을 연다

크레딧과 상업 이용 제한이 있는 서비스의 무료 플랜이 아쉬울 때 같은 회사가 낸
공개 모델은 한도 없는 시험대가 된다.
이 모델은 상용 서비스의 하한선이기도 해서, 서비스가 파는 것은 재구성 자체가
아니라 그 위의 리깅과 분할과 텍스처 같은 후처리와 편의가 된다.
다만 설치와 하드웨어라는 다른 비용을 치르고, 기능은 서비스가 앞선다는 점을
감안해 선택해야 한다.

### 인기 있는 오픈 모델은 이름을 쓰는 사이트가 먼저 보인다

오픈소스 프로젝트가 인기를 얻으면 이름을 딴 비공식 사이트가 검색 결과와 광고
수익을 가져간다.
사용자는 이름이 같아서 공식으로 오해하기 쉽다.
이 문서는 사이트의 의도를 판단하지 않고 구조만 짚는다.

### 결과가 아쉬울 때는 모델 능력과 입력 준비를 따로 시험한다

TripoSR의 결과가 별로라고 느껴질 때 원인은 셋으로 갈린다.
모델이 한 장에서 추정한 초안이라는 천장, 입력 준비의 문제, 마칭 큐브와 색 처리의
설정이다.
앞의 둘은 입력을 바꾸고 공식 데모와 비교해 가를 수 있고, 마지막은 같은
`scene_codes`에서 메시만 다시 뽑아 가를 수 있다.
그 셋을 모두 시험한 뒤에도 못 미치면 그제야 모델을 바꾼다.
이 순서가 모델을 바꾸는 비용을 가장 늦게 치르게 한다.

### 해상도 숫자를 올리기 전에 원본 해상도를 본다

마칭 큐브 해상도를 올리는 일은 쉬워서 먼저 하게 되지만, 모델 안쪽의 triplane이
64×64라면 격자를 높여도 더 담길 정보가 없다고 읽힌다.
한 단계 앞에 있는 해상도를 보지 않고 나중 단계의 숫자를 올리는 일은 다른
도구에서도 되풀이된다.
이는 이 문서의 해석이다.

### 이 글을 읽는 방법

이 문서는 저장소의 README와 `run.py`와 `tsr` 패키지와 `bake_texture.py` 코드,
논문 PDF, 모델 카드와 설정 파일, GitHub 이슈와 풀 리퀘스트, 후속 모델 저장소의
README, 비공식 사이트의 첫 화면과 FAQ와 글 목록을 읽고 정리했다.
TripoSR을 직접 설치하거나 실행하지는 못했고, 보조 스크립트 세 개만 합성 데이터로
돌렸다(Python 3.15.0, numpy 2.5.4, Pillow 13.0.0, trimesh 5.2.0).
논문의 표는 저자들이 고른 물체와 지표에서 나온 값이므로 모델 선택의 근거라기보다
같은 계열 모델을 비교할 때의 출발점으로 읽어야 한다.
판단을 가를 관찰은 넷이다.
하나는 같은 모델을 개선 항목별로 빼고 학습해 성능이 어디서 오는지 보이는
실험이다.
다른 하나는 저자가 걸러 낸 집합이 아닌 다른 물체 집합에서 같은 비교를 되풀이했을
때 순위가 유지되는지다.
셋째는 같은 이미지를 TripoSR과 유료 서비스로 만들었을 때의 품질 차이와 6GB
VRAM에서의 실제 생성 시간이다.
넷째는 비공식 사이트가 배포하는 파일이 공식 저장소의 파일과 같은지, 그리고
사이트 운영 주체가 누구인지다.
이 문서는 넷 모두 확인하지 못했다.

---

[^stability-blog]: Stability AI, [Introducing TripoSR: Fast 3D Object Generation from Single Images](https://stability.ai/news/triposr-3d-generation)

[^hf-card]: Hugging Face, [stabilityai/TripoSR](https://huggingface.co/stabilityai/TripoSR)

[^pr-94]: GitHub, [Implement texturing](https://github.com/VAST-AI-Research/TripoSR/pull/94), 2024-05-07

[^commits]: GitHub, [Commits · VAST-AI-Research/TripoSR](https://github.com/VAST-AI-Research/TripoSR/commits/main)

[^issue-149]: GitHub, [Matching Output Quality using Example Images](https://github.com/VAST-AI-Research/TripoSR/issues/149), 2026-01-21

[^issue-12]: GitHub, [Marching cubes meshing is done incorrectly(?)](https://github.com/VAST-AI-Research/TripoSR/issues/12), 2024-03-05

[^issue-16]: GitHub, [The result is different from the huggingface?](https://github.com/VAST-AI-Research/TripoSR/issues/16), 2024-03-05

[^issue-22]: GitHub, [Increase texture resolution](https://github.com/VAST-AI-Research/TripoSR/issues/22), 2024-03-05

[^issue-60]: GitHub, [Jagged edges when using high resolution marching cubes.](https://github.com/VAST-AI-Research/TripoSR/issues/60), 2024-03-18

[^issue-89]: GitHub, [Would it be feasible to provide more than one view angle as input to better the quality of the outputs](https://github.com/VAST-AI-Research/TripoSR/issues/89), 2024-04-15

[^issue-100]: GitHub, [--bake-texture option doesn't work with gpu, here is the error message:](https://github.com/VAST-AI-Research/TripoSR/issues/100), 2024-05-23

[^pr-68]: GitHub, [Add fast high resolution marching cubes up to 1024^3.](https://github.com/VAST-AI-Research/TripoSR/pull/68), 2024-03-20

[^pr-153]: GitHub, [Add Intel Arc (XPU) support and PyMCubes marching-cubes fallback](https://github.com/VAST-AI-Research/TripoSR/pull/153), 2026-07-16

[^pr-155]: GitHub, [Add Apple MPS support with CPU marching cubes fallback](https://github.com/VAST-AI-Research/TripoSR/pull/155), 2026-08-23

[^sf3d]: GitHub, [Stability-AI/stable-fast-3d](https://github.com/Stability-AI/stable-fast-3d)

[^hf-sf3d]: Hugging Face, [stabilityai/stable-fast-3d](https://huggingface.co/stabilityai/stable-fast-3d)

[^spar3d]: GitHub, [Stability-AI/stable-point-aware-3d](https://github.com/Stability-AI/stable-point-aware-3d)

[^triposg]: GitHub, [VAST-AI-Research/TripoSG](https://github.com/VAST-AI-Research/TripoSG)

[^instantmesh]: GitHub, [TencentARC/InstantMesh](https://github.com/TencentARC/InstantMesh)

[^hf-instantmesh]: Hugging Face, [TencentARC/InstantMesh](https://huggingface.co/TencentARC/InstantMesh)

[^trellis]: GitHub, [microsoft/TRELLIS](https://github.com/microsoft/TRELLIS)

[^trellis2]: GitHub, [microsoft/TRELLIS.2](https://github.com/microsoft/TRELLIS.2)

[^step1x]: GitHub, [stepfun-ai/Step1X-3D](https://github.com/stepfun-ai/Step1X-3D)

[^sam3d]: GitHub, [facebookresearch/sam-3d-objects](https://github.com/facebookresearch/sam-3d-objects)

[^hf-sam3d]: Hugging Face, [facebook/sam-3d-objects](https://huggingface.co/facebook/sam-3d-objects)

[^zero123plus]: GitHub, [SUDO-AI-3D/zero123plus](https://github.com/SUDO-AI-3D/zero123plus)

[^mvadapter]: GitHub, [huanngzh/MV-Adapter](https://github.com/huanngzh/MV-Adapter)

[^wonder3d]: GitHub, [xxlong0/Wonder3D](https://github.com/xxlong0/Wonder3D)

[^flowty]: GitHub, [flowtyone/ComfyUI-Flowty-TripoSR](https://github.com/flowtyone/ComfyUI-Flowty-TripoSR)

[^texgen]: GitHub, [ejones/triposr-texture-gen](https://github.com/ejones/triposr-texture-gen)

[^unity]: GitHub, [mapluisch/TripoSR-for-Unity](https://github.com/mapluisch/TripoSR-for-Unity)

[^tripo-bake]: GitHub, [iffyloop/TripoSR-Bake](https://github.com/iffyloop/TripoSR-Bake)

[^tripo-mlx]: GitHub, [sachaarbonel/tripo-mlx](https://github.com/sachaarbonel/tripo-mlx)

[^horsawlarway]: <https://news.ycombinator.com/item?id=42376484>

[^vunderba]: <https://news.ycombinator.com/item?id=47039045>

[^otmardev]: <https://news.ycombinator.com/item?id=47050674>

[^hi_hi]: <https://news.ycombinator.com/item?id=42371940>

[^RugnirViking]: <https://news.ycombinator.com/item?id=42382712>
