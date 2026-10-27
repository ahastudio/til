# Hunyuan3D: 오픈 가중치로 쓰는 Tencent의 3D 생성 모델 계열과 한국에서의 라이선스 제약

<https://github.com/Tencent-Hunyuan/Hunyuan3D-2>

<https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1>

<https://hy3d.tencent.ai/>

HN 토론: <https://news.ycombinator.com/item?id=42786040> (323점, 142개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=43419237> (180점, 77개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49265051> (277점, 82개 댓글)

GN 토론: <https://news.hada.io/topic?id=18861>

## 목차

- [소개](#소개)
- [버전 계보](#버전-계보)
- [동작 방식](#동작-방식)
- [파이프라인을 코드로 따라가기](#파이프라인을-코드로-따라가기)
- [모델 목록과 사양](#모델-목록과-사양)
- [성능](#성능)
- [라이선스](#라이선스)
- [설치하기](#설치하기)
- [실행하기](#실행하기)
- [실행하는 다른 길](#실행하는-다른-길)
- [GPU 없이 CPU로 돌리기](#gpu-없이-cpu로-돌리기)
- [값 정하기](#값-정하기)
- [후처리와 내보내기](#후처리와-내보내기)
- [다른 모델과 견주기](#다른-모델과-견주기)
- [호스티드 서비스와 요금](#호스티드-서비스와-요금)
- [파생 프로젝트](#파생-프로젝트)
- [함정](#함정)
- [트레이드오프](#트레이드오프)
- [비평](#비평)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)

## 소개

Hunyuan3D는 Tencent의 Hunyuan 팀이 만든 3D 에셋 생성 모델 계열이다.
이미지 한 장(또는 여러 시점의 이미지)에서 형태(mesh)를 만들고, 그 위에 텍스처를
입혀 질감이 있는 3D 에셋을 내놓는 것이 기본 흐름이다.
2025년 1월 21일에 공개된 2.0이 이 계열의 전환점이다.
2.0의 README는 형태 생성과 텍스처 생성을 두 단계로 나누고, 추론 코드와 사전
훈련된 가중치와 기술 보고서를 모두 공개했다.
이어 2025년 6월 13일에 2.1이 나왔고, README는 이를 PBR 텍스처 모델과 새 VAE
인코더와 모든 학습 코드를 갖춘 완전한 오픈소스 공개로 소개한다.

2026년 10월 27일에 GitHub에서 확인한 저장소 현황은 다음과 같다.
`Hunyuan3D-2`는 스타 15,209개와 포크 1,582개로 계열에서 가장 크고,
`Hunyuan3D-2.1`은 스타 4,290개와 포크 638개와 열린 이슈 157개다.
두 저장소의 마지막 푸시는 각각 2025년 10월 28일과 2025년 10월 17일이어서, 오픈
가중치 쪽의 갱신은 2025년 가을 이후 조용하다.
반면 이 문서가 읽은 Tencent 쪽 자료는 호스티드 서비스에서 3.0과 3.1을 고를 수
있다고 말한다.[^billing]
오픈 가중치는 2.1까지이고 최신 모델은 서비스로만 제공된다는 구도는 이 문서의
해석이며, 3.x의 가중치가 따로 공개되었는지는 Tencent-Hunyuan 조직의 3D 관련
저장소 목록에서 찾지 못했다는 뜻이다.

이 문서를 쓰는 이유가 하나 더 있다.
2.0과 2.1의 라이선스 본문은 유럽 연합, 영국, 대한민국을 허용 지역에서 제외한다.
한국에서 이 모델의 가중치를 쓰려는 독자는 설치법보다 먼저 아래 라이선스 절을
읽어야 한다.

이 문서를 쓰는 사람의 사용 경험도 여기에 적어 둔다.
Hunyuan3D는 결과가 꽤 괜찮았고, GPU 없이 CPU만으로 돌려도 만족스러웠다.
이 경험담에는 측정값이 없어서 숫자로 바꾸지 않았다.
아래 「GPU 없이 CPU로 돌리기」 절은 이 경험이 어떤 조건에서 성립하는지를 공식
코드와 공개된 측정 기록으로 따져 본다.

계열의 저장소를 2026년 10월 27일 GitHub 조직 목록에서 읽은 값으로 정리하면
다음과 같다.[^org-api]

| 저장소               | 스타   | 마지막 푸시 | 내용                                |
| -------------------- | ------ | ----------- | ----------------------------------- |
| Hunyuan3D-1          | 3,500  | 2025-11-19  | 1.0, 텍스트와 이미지에서 3D         |
| Hunyuan3D-2          | 15,209 | 2025-10-28  | 2.0과 변형(Fast, Turbo, mini, mv)   |
| Hunyuan3D-2.1        | 4,290  | 2025-10-17  | PBR 텍스처와 학습 코드              |
| Hunyuan3D-Omni       | 651    | 2025-10-17  | 점 구름과 골격 같은 추가 제어 신호  |
| Hunyuan3D-Part       | 553    | 2025-12-05  | 부품 분할과 생성                    |
| HY3D-Bench           | 363    | 2026-02-27  | 학습용 데이터셋                     |
| Hunyuan3D-Buffalo1.0 | 260    | 2026-08-10  | 이해, 생성, 편집을 한 구조에서 처리 |
| Hunyuan3D-WorldClaw  | 1,418  | 2026-08-13  | 에이전트로 만드는 3D 세계           |

스타가 가장 많은 저장소는 2.0이고, 가중치를 받는 허깅페이스 쪽의 내려받기 수도 같은 순서다.
허깅페이스 API가 돌려준 `downloads` 값은 2.0이 172,834, 2.1이 82,316, mini가
51,728, mv가 18,259였다.[^hf-2][^hf-21][^hf-2mini][^hf-2mv]
이 값의 집계 기간은 확인하지 못했으므로 서로 견주는 용도로만 읽어야 한다.

## 버전 계보

| 버전     | 시기               | 제공 형태               | 핵심                                                                                               |
| -------- | ------------------ | ----------------------- | -------------------------------------------------------------------------------------------------- |
| 1.0      | 2024년 11월        | 저장소 공개             | 다중 시점 이미지를 만든 뒤 피드포워드 재구성으로 3D를 만드는 2단계. 텍스트와 이미지 입력[^arxiv-1] |
| 2.0      | 2025년 1월 21일    | 오픈 가중치             | 형태 모델 DiT와 텍스처 모델 Paint의 2단계[^arxiv-2]                                                |
| 2.0 변형 | 2025년 2월~4월     | 오픈 가중치             | Fast, Turbo, mini, mv(다중 시점), Paint Turbo                                                      |
| 2.1      | 2025년 6월 13일    | 오픈 가중치와 학습 코드 | PBR 텍스처, 학습 파이프라인 전체 공개[^arxiv-21]                                                   |
| 2.5      | 2025년 6월(보고서) | 호스티드로 읽힘         | 최대 100억 매개변수의 형태 모델 LATTICE와 PBR 텍스처[^arxiv-25]                                    |
| 3.0, 3.1 | 2025년 하반기 이후 | 호스티드 서비스와 API   | 서비스에서 모델 버전으로 고른다[^billing]                                                          |

1.0의 논문은 첫 단계의 다중 시점 확산이 약 4초, 둘째 단계의 재구성이 약 7초
걸린다고 한다.[^arxiv-1]
형태 생성과 텍스처 생성을 분리한 2.0의 설계는 그 뒤 계열 전체의 뼈대가 되었다.
2.0 README의 공개 일지는 변형 모델이 짧은 간격으로 이어졌음을 보여 준다.
2025년 1월 27일에 Blender 애드온, 2월 3일에 추론 시간을 절반으로 줄이는 지침
증류 모델(Fast), 2월 14일에 텍스처 향상 모듈, 3월 18일에 다중 시점 형태
모델(mv)과 0.6B 소형 모델(mini), 3월 19일에 단계 증류 모델(Turbo)과 FlashVDM,
4월 1일에 Paint Turbo가 나왔다.

2.5의 보고서는 형태 모델 LATTICE가 데이터와 모델 크기와 계산량을 키워 학습되었고
가장 큰 모델이 100억 매개변수라고 밝힌다.[^arxiv-25]
이 문서가 읽은 2.0 README의 모델 목록에는 2.5가 없다.
Part 저장소의 안내는 입력 메시로 Hunyuan3D V2.5나 V3.0이 만든 결과를 권하므로,
두 버전이 서비스로 존재한다는 점은 확인된다.[^part]

## 동작 방식

2.0 이후의 구조는 형태와 텍스처를 분리한 2단계다.
첫 단계의 Hunyuan3D-DiT는 확장 가능한 흐름 기반(flow-based) 확산 트랜스포머로,
조건 이미지와 맞는 기하를 만든다.
둘째 단계의 Hunyuan3D-Paint는 기하와 확산 모델의 사전 지식을 이용해 고해상도
텍스처 맵을 만들고, 모델이 만든 메시뿐 아니라 손으로 만든 메시에도 쓸 수
있다.[^arxiv-2]
2.0 README는 이 분리가 형태와 텍스처의 난이도를 따로 다루게 해 주고, 이미 있는
메시에 텍스처만 입히는 유연성도 준다고 설명한다.

이 구조에서 실무적으로 중요한 점은 두 모델이 따로 돈다는 것이다.
형태만 필요하면 DiT만 돌려 적은 VRAM으로 메시를 얻고, 텍스처는 필요할 때 얹는다.
2.0 README의 사양도 형태 생성에는 6GB, 형태와 텍스처를 합치면 16GB가 든다고 둘을
나눠 적는다.

2.1은 텍스처 쪽을 RGB 기반에서 PBR(물리 기반 렌더링)로 바꿨다.
README는 이를 금속 반사와 표면 아래 산란 같은 빛의 상호작용을 물리 기반 재질
모사로 만든다고 설명한다.
2.1의 기술 문서(arXiv)는 스스로를 튜토리얼이라고 부르며 3D 데이터 처리, 생성
모델 학습, 평가, 배포의 전 과정을 단계별로 안내한다고 밝힌다.[^arxiv-21]
이 공개의 요점은 가중치뿐 아니라 학습 코드까지 풀려 직접 미세 조정할 수 있다는
점이다.

출력 메시가 어떻게 만들어지는지는 HN에서 작은 논쟁이 되었다.
sebzim4500은 구조도 하나가 마칭 큐브(Marching Cubes)로 메시를 만드는 것처럼
보이는데 결과물의 기하는 그렇게 보이지 않는다고 했다.[^sebzim4500]
GrantMoyer는 데모의 새 메시에 정사각형에 가까운 삼각형 쌍이 많다는 점을 들어
마칭
큐브의 산물로 보인다고 반박했고,[^GrantMoyer] wumeow도 허깅페이스 데모의 메시가
마칭 큐브 결과처럼 보인다고 했다.[^wumeow]
그렇다면 모델이 부호 거리장(SDF)을 만든다는 뜻이어서, TinkersW는 삼각형 메시
대신 SDF 자체를 내보낼 수 있으면 좋겠다고 적었다.[^TinkersW]

## 파이프라인을 코드로 따라가기

2.0 저장소의 코드를 따라가면 이미지 한 장이 메시가 되기까지 다섯 단계를 지난다.
아래는 `hy3dgen/shapegen/pipelines.py`와 `postprocessors.py`, `gradio_app.py`를
읽고 정리한 것이다.[^code-pipelines][^code-post][^code-gradio]
이 문서가 코드를 실행해 확인한 것은 아니며, 읽은 코드가 말하는 바를 적었다.

### 1단계: 이미지 준비

입력은 파일 경로나 PIL 이미지다.
Gradio 앱에는 배경 제거 체크박스가 있고 기본값이 켜짐이다.
켜 두면 `BackgroundRemover`가 배경을 지운 RGBA 이미지로 바꿔 모델에
넘긴다.[^code-gradio]
README가 안내하는 `minimal_demo.py`는 이미지를 먼저 RGBA로 바꾼 뒤 모드가 RGB일
때만 배경을 지우도록 쓰여 있어서, 이 분기는 실행되지 않는다.[^code-minimal]
2.1의 형태 전용 `minimal_demo.py`는 이미지 변수를 경로 문자열로 다시
덮어쓴다.[^code-21-minimal]
그래서 데모 스크립트를 그대로 돌리면 배경 제거 없이 원본이 들어간다고 읽힌다.
이는 이 문서의 코드 읽기다.
배경이 복잡한 사진을 쓸 때는 직접 배경을 지우거나 Gradio 앱의 체크박스를 쓰는
편이 안전하다.

### 2단계: 조건 인코딩

`prepare_image`가 입력을 정리하고 `encode_cond`가 조건 인코더로 조건 벡터를
만든다.[^code-pipelines]
체크포인트 하나에 `model`, `vae`, `conditioner`가 함께 들어 있고 로딩 코드가 세
묶음을 나눠 읽는다.[^code-pipelines]
그래서 같은 변형을 받으면 형태 모델과 디코더와 조건 인코더가 한 파일로 온다.
커뮤니티의 CPU 측정 기록은 이 단계를 DINO 인코더의 로딩과 실행으로
적는다.[^gc-cpu]

### 3단계: 흐름 매칭 샘플링

`Hunyuan3DDiTFlowMatchingPipeline`은 `np.linspace(0, 1, num_inference_steps)`로
시점 값을 만들고 단계마다 DiT를 부른다.
classifier-free guidance를 쓰면 조건부 예측과 무조건부 예측을 함께 얻으려고
배치를 둘로 늘려 DiT가 한 단계에 두 배의 일을 한다.
모델에 guidance 임베딩이 들어 있으면 이 배치 확장을 하지 않고 한 번만
계산한다.[^code-pipelines]
README가 Fast를 지침 증류 모델이고 추론 시간을 절반으로 줄인다고 설명하는 것은
이 구조와 맞아 보인다.
다만 Fast가 절반인 이유가 배치 확장 생략이라는 연결은 이 문서의 해석이다.
Turbo는 단계 증류여서 Gradio 앱의 단계 수 기본값이 Turbo는 5, 그 밖의 모델은
30이다.[^code-gradio]

### 4단계: 격자 디코딩과 표면 추출

샘플링이 끝나면 VAE가 잠재 변수를 격자 위의 값으로 풀어낸다.
격자는 한 변에 `octree_resolution + 1`개의 점을 두고, 범위는 `box_v`(기본
1.01)가 정한 정육면체 안이다.
`num_chunks`는 이 점들을 몇 개씩 나누어 디코더에 넣을지 정한다.[^code-pipelines]
격자 값에서 표면을 뽑는 방법은 코드에 두 가지가 있다.
`mc`는 scikit-image의 마칭 큐브(`method="lewiner"`)이고, 모델이 GPU에 있어도
`grid_logit.cpu().numpy()`로 값을 CPU로 옮겨 CPU에서 돈다.
`dmc`는 `diso` 패키지의 DiffDMC로 GPU 쪽 구현이다.[^code-surface]
Gradio 앱은 장치가 `cpu`나 `mps`이면 `mc`를 강제한다.[^code-gradio]
FlashVDM을 켜면 Turbo용 VAE로 바꿔 끼우고 적응형 KV 선택을 쓰는 디코더가
켜진다.[^code-pipelines]
한 CPU 측정 기록에서는 요청한 해상도 256이 63, 126, 252의 단계별 격자로
조정되었다.[^gc-cpu]

해상도 숫자는 점 수를 세제곱으로 바꾼다.
해상도 256이면 격자점이 257의 세제곱인 16,974,593개이고, 384이면 385의 세제곱인
57,066,625개다.
출력 면 수는 이보다 완만하게 늘며, 아래 후처리 절의 합성 도형에서는 해상도 128,
256, 384에서 각각 57,288개, 228,192개, 511,616개였다.

### 5단계: 후처리

같은 저장소의 `postprocessors.py`에는 세 도구가 있다.
`FloaterRemover`는 전체 면의 0.5% 미만인 떨어진 조각을 골라 지운다.
`FaceReducer`는 쿼드릭 엣지 콜랩스로 면 수를 줄이며 경계와 법선과 위상을
보존하는 옵션을 켠다.
기본 목표는 40,000면이고 목표가 현재 면 수보다 크면 메시를 건드리지
않는다.[^code-post]
`DegenerateFaceRemover`도 같은 모듈에 있다.
Gradio 앱은 텍스처를 입히기 전에 `FaceReducer`를 기본값으로 호출하고, 같은
자리의 플로터 제거와 퇴화 면 제거 호출은 주석 처리되어 있다.[^code-gradio]
그래서 텍스처 모델은 40,000면 이하로 줄인 메시를 받는다고 읽힌다.
내보내기 탭의 면 수 목표 슬라이더는 기본값이 10,000이다.[^code-gradio]

### 기본값 정리

| 항목              | 파이프라인 API 기본값 | Gradio 앱 기본값                      |
| ----------------- | --------------------- | ------------------------------------- |
| 추론 단계         | 50                    | Turbo 5, 그 밖의 모델 30              |
| guidance          | 5.0                   | 5.0                                   |
| octree_resolution | 384                   | 256 (Low 196, Standard 256, High 384) |
| num_chunks        | 8000                  | 8000                                  |
| mc_level          | 0.0                   | 앱 슬라이더에 없음                    |
| 장치와 자료형     | `cuda`, `float16`     | `--device` 기본값 `cuda`              |

API 기본값과 앱 기본값이 다르다는 점이 중요하다.
앱에서 만든 결과와 같은 설정을 파이썬에서 재현하려면 해상도를 256으로, Turbo의
단계 수를 5로 직접 맞춰야 한다.

## 모델 목록과 사양

2.0과 2.1 README의 모델 목록을 정리한 표다.
README끼리 숫자가 어긋나는 곳이 있어 2.1 README를 기준으로 삼았다.

| 계열  | 모델                                 | 역할                      | 크기 | VRAM(README)                      |
| ----- | ------------------------------------ | ------------------------- | ---- | --------------------------------- |
| 2.1   | Hunyuan3D-Shape-v2-1                 | 이미지에서 형태           | 3.3B | 형태 10GB, 텍스처 21GB, 합계 29GB |
| 2.1   | Hunyuan3D-Paint-v2-1                 | PBR 텍스처                | 2B   | 위와 같음                         |
| 2.0   | Hunyuan3D-DiT-v2-0                   | 이미지에서 형태           | 1.1B | 형태 6GB, 합계 16GB               |
| 2.0   | Hunyuan3D-DiT-v2-0-Fast              | 지침 증류(추론 시간 절반) | 1.1B | 위와 같음                         |
| 2.0   | Hunyuan3D-DiT-v2-0-Turbo             | 단계 증류                 | 1.1B | 위와 같음                         |
| 2.0   | Hunyuan3D-Paint-v2-0                 | 텍스처(RGB)               | 1.3B | 위와 같음                         |
| 2.0   | Hunyuan3D-Paint-v2-0-Turbo           | 텍스처 증류               | 1.3B | 위와 같음                         |
| 2.0   | Hunyuan3D-Delight-v2-0               | 이미지 조명 제거          | 1.3B | 위와 같음                         |
| 2mv   | Hunyuan3D-DiT-v2-mv(-Fast, -Turbo)   | 다중 시점 이미지에서 형태 | 1.1B | 위와 같음                         |
| 2mini | Hunyuan3D-DiT-v2-mini(-Fast, -Turbo) | 소형 형태 모델            | 0.6B | 위와 같음                         |

2.0 README의 표는 2.1 모델의 크기를 3.0B와 1.3B로 적지만 2.1 README는 3.3B와
2B로 적는다.
앞쪽은 개정되지 않은 흔적으로 보이고, 이는 이 문서의 해석이다.
VRAM 숫자도 시점에 따라 달랐다.
2025년 3월 HN 스레드의 댓글은 당시 README를 인용해 형태 6GB와 합계 24.5GB라고
적었는데,[^fancyfredbot] 지금 README는 합계 16GB다.
다만 이 숫자는 모두 README의 서술이고, 이 문서가 직접 재지는 못했다.

### 내려받는 파일의 크기

허깅페이스 API가 알려 준 파일 크기로 보면 형태 모델 하나의 가중치 파일은 2.0과
Fast, Turbo, mv가 4.93GB, mini가 3.82GB, 2.1이
7.37GB다.[^hf-2][^hf-2mini][^hf-2mv][^hf-21]
mini는 매개변수가 0.6B인데 파일이 3.82GB인 것은 체크포인트에 형태 모델뿐 아니라
VAE와 조건 인코더도 함께 들어 있기 때문으로 읽힌다.[^code-pipelines]
이는 이 문서의 해석이며, 파일 안의 항목별 크기는 확인하지 못했다.

| 구성 요소                          | 파일 크기(GB) | 저장소                  |
| ---------------------------------- | ------------- | ----------------------- |
| 2.0 형태 모델(DiT, Fast, Turbo)    | 4.93          | tencent/Hunyuan3D-2     |
| 2.0 VAE (일반, Turbo)              | 0.43, 0.41    | tencent/Hunyuan3D-2     |
| 2.0 텍스처 모델 UNet               | 3.66          | tencent/Hunyuan3D-2     |
| 2.0 조명 제거 모델 UNet            | 3.46          | tencent/Hunyuan3D-2     |
| 2mini 형태 모델(일반, Fast, Turbo) | 3.82          | tencent/Hunyuan3D-2mini |
| 2mv 형태 모델(일반, Fast, Turbo)   | 4.93          | tencent/Hunyuan3D-2mv   |
| 2.1 형태 모델                      | 7.37          | tencent/Hunyuan3D-2.1   |
| 2.1 VAE                            | 0.66          | tencent/Hunyuan3D-2.1   |
| 2.1 PBR 텍스처 UNet                | 3.93          | tencent/Hunyuan3D-2.1   |

저장소 전체의 크기는 2.0이 74.9GB, mini가 25.3GB, mv가 29.6GB, 2.1이 14.9GB로
표시되었다.[^hf-2][^hf-2mini][^hf-2mv][^hf-21]
2.0 쪽이 큰 것은 같은 가중치를 `.ckpt`와 `.safetensors`로 중복해 올려 둔 데다
변형이 많기 때문이다.

필요한 조합만 받는 것이 가능하다.
형태 파이프라인의 로딩 코드는 먼저 로컬 경로(`HY3DGEN_MODELS` 환경 변수, 기본값
`~/.cache/hy3dgen`)를 찾고, 없을 때만 `snapshot_download`에 `allow_patterns`로
지정한 하위 폴더만 받는다.[^code-utils]
그래서 `subfolder`를 `hunyuan3d-dit-v2-mini-turbo`로 주면 그 폴더만 내려온다.
FlashVDM을 켜면 Turbo용 VAE 폴더가 따로 필요하므로 두 폴더가 함께 내려온다고
읽힌다.[^code-pipelines]
이 문서는 가중치를 내려받지 않았고, 크기 표는 API가 알려 준 값이다.

## 성능

2.0 README의 비교는 기준 모델을 이름 없이 적는다.

| 모델                 | CMMD↓ | FID_CLIP↓ | FID↓    | CLIP-score↑ |
| -------------------- | ----- | --------- | ------- | ----------- |
| 최고 오픈소스 모델 1 | 3.591 | 54.639    | 289.287 | 0.787       |
| 최고 비공개 모델 1   | 3.600 | 55.866    | 305.922 | 0.779       |
| 최고 비공개 모델 2   | 3.368 | 49.744    | 294.628 | 0.806       |
| 최고 비공개 모델 3   | 3.218 | 51.574    | 295.691 | 0.799       |
| Hunyuan3D 2.0        | 3.193 | 49.165    | 282.429 | 0.809       |

2.1 README는 이름 있는 기준 모델과 비교한다.

| 형태 모델           | ULIP-T↑ | ULIP-I↑ | Uni3D-T↑ | Uni3D-I↑ |
| ------------------- | ------- | ------- | -------- | -------- |
| Michelangelo        | 0.0752  | 0.1152  | 0.2133   | 0.2611   |
| Craftsman           | 0.0745  | 0.1296  | 0.2375   | 0.2987   |
| TripoSG             | 0.0767  | 0.1225  | 0.2506   | 0.3129   |
| Step1X-3D           | 0.0735  | 0.1183  | 0.2554   | 0.3195   |
| Trellis             | 0.0769  | 0.1267  | 0.2496   | 0.3116   |
| Direct3D-S2         | 0.0706  | 0.1134  | 0.2346   | 0.2930   |
| Hunyuan3D-Shape-2.1 | 0.0774  | 0.1395  | 0.2556   | 0.3213   |

텍스처 비교에서는 Hunyuan3D-Paint-2.1이 CLIP-FID 24.78, CMMD 2.191, CLIP-I
0.9207, LPIPS 0.1211로 Hunyuan3D-2.0의 26.44, 2.318, 0.8893, 0.1261보다 낫다고
README는 보인다.
이 표들은 Tencent의 자체 평가이고 기준 모델의 구성과 평가 물체 선정이 공개된
범위에서는 재현하기 어렵다.
Step1X-3D와의 Uni3D-T 차이는 0.2554 대 0.2556이다.
이 정도 차이가 측정의 잡음 안인지는 README가 다루지 않는다.

사용자 쪽 평가는 더 엇갈렸다.
HN의 godelski는 연구자로서 논문과 프로젝트 페이지의 사례를 믿지 말고 직접 해
보라고 말하며 프로젝트 페이지의 물체를 재현해 보았다.
그는 처음의 비판을 일부 거두며, 흔한 에셋에서는 꽤 괜찮지만 샘플이 적을 법한
물체에서는 성능이 좋지 않다고 정리했다.[^godelski]
Kelvin506은 프로젝트 페이지의 기타가 현이 다섯 개인데 조율 나사는 여섯 개이고
지판 아래에 픽업이 있는 등 구조 오류가 있다고 짚었다.[^Kelvin506]
BigJono는 이것이 생산에 쓰기에는 아직 한참 멀었다고 평했다.[^BigJono]

## 라이선스

2.0과 2.1의 라이선스는 Tencent Hunyuan 3D Community License다.
2.1 본문의 첫 문장은 이 계약이 유럽 연합, 영국, 대한민국에서는 적용되지 않으며
허용 지역(Territory)으로 명시적으로 제한된다고 분명히 적는다.[^license-21]
허용 지역은 유럽 연합, 영국, 대한민국을 제외한 전 세계로 정의된다.[^license-21]
2.0 라이선스도 같은 문장으로 시작하고 같은 정의를 쓴다.[^license-2]

한국 독자에게 중요한 조항은 세 개다.
첫째, 허용 지역 안에서만 사용과 복제와 배포와 수정이 허락되고, 허용 지역 밖에서
가중치나 Output(생성 결과)을 쓰고 보여 주는 것은 무허가라고 5조 c항이
정한다.[^license-21]
둘째, 허용 사용 정책(Acceptable Use Policy)의 첫 항목이 허용 지역 밖에서의 사용
금지다.[^license-21]
셋째, 이 계약은 홍콩 법을 준거법으로 하고 홍콩 법원을 전속 관할로
삼는다.[^license-21]
이 문서가 읽은 범위에서는 한국을 위한 별도 신청 절차가 보이지 않는다.
이는 법률 자문이 아니며, 한국에서 쓸 계획이 있다면 가중치를 받기 전에 전문가에게
확인해야 한다.

그 밖의 조건도 알아 둘 만하다.
출시일 기준으로 모든 제품과 서비스의 월간 활성 사용자가 100만을 넘으면
Tencent에서 별도 라이선스를 받아야 하고 승인은 Tencent의 재량이다.[^license-21]
생성 결과물에 대해서는 Tencent가 어떤 권리도 주장하지 않으며 결과물과 그 이용의
책임은 사용자와 이용자에게 있다고 6조 d항이 적는다.[^license-21]
가중치나 결과물로 다른 AI 모델을 개선하는 것은 금지된다.[^license-21]
이 모델을 써서 제3자에게 서비스를 제공하면 실제 제공자의 법적 이름을 최종
사용자에게 드러내고 Tencent가 제휴하거나 보증하지 않는다고 밝혀야
한다.[^license-21]

HN에서는 2.0 공개 직후 pella가 이 문구를 올렸고,[^pella] gruez가 유럽 연합의 AI
규제와 관련이 있는지 물었다.[^gruez]
EMIRELADERO는 모델 가중치는 저작권이 없을 테니 무시해도 안전하리라고
추정했다.[^EMIRELADERO]
이 추정은 댓글의 의견이며, 이 문서는 법적 판단을 하지 않는다.
다만 라이선스 본문이 결과물의 사용까지 명시적으로 지역 제한 아래 둔다는 점은
가중치의 저작권 여부와 별개의 문제로 남는다.

최신 파생 저장소의 상황도 다르다.
2026년 10월 27일 GitHub 조회에서 `Hunyuan3D-WorldClaw`와 `Hunyuan3D-Buffalo1.0`
저장소는 라이선스가 표시되지 않았고, 이 문서는 두 저장소의 본문에서 라이선스
조건을 찾지 못했다.

라이선스 본문을 다시 읽으면 앞의 설명에 보탤 조항이 더 있다.

서두는 이 계약을 호스티드 서비스를 통한 사용을 포함해 Works의 어떤 부분이든
사용하거나 복제하거나 수정하거나 배포하거나 수행하거나 표시하는 순간 동의한
것으로 본다고 적는다.[^license-21]
그래서 허깅페이스 스페이스나 제3자 호스팅으로 쓰는 경우에도 계약 밖에 있다고
단정할 수 없다.
이는 이 문서의 해석이며 법률 자문이 아니다.

월간 활성 사용자 100만 명의 기준은 출시일 직전 달력월의 값이다.
기준을 넘어 허락을 구하려면 회사 이름과 사업 분야, 사용 목적, 모델을 수정하거나
파생 모델을 만들 계획을 `hunyuan3d@tencent.com`으로 보내야 한다고 2.1 본문이
적는다.
2.0 본문에는 앞의 두 항목만 있어, 마지막 항목이 2.1에서 더해진 것으로
읽힌다.[^license-21][^license-2]

배포하는 경우의 조건도 있다.
받는 쪽에 계약서 사본을 주고, 수정한 파일에는 수정했다는 고지를 붙이고, 호스티드
서비스가 아닌 배포에는 정해진 문구의 Notice 텍스트 파일을 함께 줘야 한다.
제품에 「Powered by Tencent Hunyuan」을 표시하고 사용 경험을 알리는 글을 쓰는
것은 의무가 아니라 권장이다.[^license-21]
파생 저작물과 수정본과 파생 모델은 Tencent 소유분을 뺀 부분을 만든 사람이
소유한다고 6조 a항이 적고, 6조 c항은 Tencent나 다른 이에게 이 자료나 결과물이
지식재산권을 침해한다는 소송을 걸면 모든 허락이 그날 끝난다고
정한다.[^license-21]
허용 사용 정책에는 지역 밖 사용 금지 말고도, 공개된 자리에 올리는 정보가 기계가
만든 것임을 분명히 밝히지 않는 것을 금지하는 항목이 있다.[^license-21]
2.1 저장소의 Notice 파일은 Stable Diffusion을 MIT와 CreativeML Open RAIL++-M
아래의 제3자 구성 요소로 적는다.[^notice-21]

이 지역 제한이 왜 생겼는지에 대해서는 GeekNews의 Hunyuan-A13B 글에 달린 댓글이
한 가지 설명을 내놓았다.
fortune은 한국 인공지능 기본법으로 해외 모델에도 위험 평가와 표시와 국내 대표
지정 의무가 생겨 한국이 막혔다고 적었고, 이 설명을 GPT가 작성했다고 스스로
밝혔다.[^fortune]
이 글이 다루는 모델은 Hunyuan3D가 아닌 Tencent의 다른 모델이며, 글 제목이 EU와
영국과 한국에서 쓸 수 없다고 같은 지역 제한을 밝힌다.[^gn-a13b]
이 문서는 이 설명을 확인하지 못했으므로 지역 제한의 이유로 읽지 않고 한 댓글의
추측으로만 소개한다.
HN의 2025년 3월 스레드에서도 sruc가 같은 지역 제한을 지적했고,[^sruc] johaugum은
Meta의 Llama 3.2 라이선스가 멀티모달 모델에 대해 EU에 사는 개인이나 EU에 주된
사업장을 둔 회사에게 권리를 주지 않는 비슷한 제한을 둔다고 짚었고, 그 이유를
EU의 AI 규제를 완전히 따르지 못하기 때문으로 설명했다.[^johaugum]

## 설치하기

2.0은 PyTorch를 공식 안내대로 설치한 뒤 요구 사항과 텍스처용 확장을 빌드한다.

```bash
pip install -r requirements.txt
pip install -e .
# for texture
cd hy3dgen/texgen/custom_rasterizer
python3 setup.py install
cd ../../..
cd hy3dgen/texgen/differentiable_renderer
python3 setup.py install
```

2.1은 Python 3.10과 PyTorch 2.5.1(CUDA 12.4)에서 시험했다고 README가 밝힌다.
텍스처 쪽 빌드와 업스케일러 가중치 내려받기가 설치 절차에 들어 있다.

```bash
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

cd hy3dpaint/custom_rasterizer
pip install -e .
cd ../..
cd hy3dpaint/DifferentiableRenderer
bash compile_mesh_painter.sh
cd ../..

wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P hy3dpaint/ckpt
```

README는 macOS, Windows, Linux를 지원한다고 쓴다.
HN의 swframe2는 4090에서 윈도우 설치가 빌드 오류로 막혔고 WSL 우분투에서는 잘
되었으며, CUDA 11.3에서는 빌드가 실패하고 12.4로 바꾸니 되었다고
보고했다.[^swframe2]
Windows 사용자를 위해 커뮤니티가 만든 설치 묶음과 ComfyUI 래퍼가 2.0 README의
커뮤니티 자원 목록에 올라 있다.

## 실행하기

2.0은 diffusers와 비슷한 API를 제공한다.
형태만 만들 때는 다음과 같이 쓰고 결과는 trimesh 객체여서 glb나 obj로 저장할 수
있다.

```python
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
mesh = pipeline(image='assets/demo.png')[0]
```

텍스처까지 입히려면 메시를 먼저 만든 뒤 Paint 파이프라인을 이어 쓴다.

```python
from hy3dgen.texgen import Hunyuan3DPaintPipeline
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

# let's generate a mesh first
pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
mesh = pipeline(image='assets/demo.png')[0]

pipeline = Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')
mesh = pipeline(mesh, image='assets/demo.png')
```

2.1의 README 예제는 형태 파이프라인과 텍스처 파이프라인의 임포트 경로를 나누고
시점 수와 해상도를 설정으로 준다.

```python
import sys
sys.path.insert(0, './hy3dshape')
sys.path.insert(0, './hy3dpaint')
from textureGenPipeline import Hunyuan3DPaintPipeline, Hunyuan3DPaintConfig
from hy3dshape.pipelines import Hunyuan3DDiTFlowMatchingPipeline

shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2.1')
mesh_untextured = shape_pipeline(image='assets/demo.png')[0]

paint_pipeline = Hunyuan3DPaintPipeline(Hunyuan3DPaintConfig(max_num_view=6, resolution=512))
mesh_textured = paint_pipeline(mesh_path, image_path='assets/demo.png')
```

이 예제는 앞 줄에서 `mesh_untextured`를 만들고 마지막 줄에서 정의되지 않은
`mesh_path`를 쓴다.
저장소의 예제 폴더를 확인해 두 변수를 이어야 하며, 이 문서는 이 코드를 직접
실행해 보지 못했다.

브라우저에서 쓰려면 로컬 Gradio 앱을 띄운다.
2.1의 명령은 다음과 같다.

```bash
python3 gradio_app.py \
  --model_path tencent/Hunyuan3D-2.1 \
  --subfolder hunyuan3d-dit-v2-1 \
  --texgen_model_path tencent/Hunyuan3D-2.1 \
  --low_vram_mode
```

2.0 README는 mini, mv, 본 모델 각각의 명령을 주고, Turbo 버전에는
`--enable_flashvdm`을 더한다.
2.0은 또 로컬 API 서버와 Blender 애드온을 제공한다.
API 서버는 `python api_server.py --host 0.0.0.0 --port 8080`으로 띄우고,
애드온은 이 서버에 연결해 Blender 안에서 모델을 부른다.

## 실행하는 다른 길

코드와 Gradio 말고도 저장소가 제공하거나 커뮤니티가 만든 실행 경로가 여럿 있다.
아래 명령과 예제는 모두 문서와 코드를 읽고 옮긴 것이며, 이 문서가 직접 실행하지
못했다.

### 2.0 API 서버

2.0은 `python api_server.py --host 0.0.0.0 --port 8080`으로 서버를 띄우고
`/generate`에 이미지를 base64로 보내면 GLB를 돌려준다.
README의 예제 JSON은 마지막 값 뒤에 쉼표가 남아 있어 엄격한 JSON 파서는
거부한다.
쉼표를 지운 명령은 다음과 같다.[^repo-2-readme]

```bash
# macOS: base64 -i, Linux: base64 -w0
img_b64_str=$(base64 -i assets/demo.png)
curl -X POST "http://localhost:8080/generate" \
     -H "Content-Type: application/json" \
     -d '{"image": "'"$img_b64_str"'"}' \
     -o test2.glb
```

README의 서버 명령은 `0.0.0.0`에 열도록 되어 있어서 같은 망의 다른 기기에도
서버가 보인다.
로컬에서만 쓸 때는 `--host 127.0.0.1`로 바꾸는 편이 안전하다.
이는 이 문서의 제안이다.

### 2.1 API 서버와 Docker

2.1 저장소에는 FastAPI 서버가 있고 문서가 엔드포인트와 기본값을 적는다.
`/generate`는 GLB를 바로 돌려주고, `/send`는 비동기 작업을 시작해 작업 번호를
주며, `/status/{uid}`로 결과를 받는다.
`/health`는 상태 확인이다.
요청 항목의 기본값은 다음과 같다.[^doc-21-api]

| 항목                | 기본값 | 의미                   |
| ------------------- | ------ | ---------------------- |
| remove_background   | true   | 배경 자동 제거         |
| texture             | false  | 텍스처 생성 여부       |
| seed                | 1234   | 무작위 시드            |
| octree_resolution   | 256    | 메시 해상도            |
| num_inference_steps | 5      | 생성 단계              |
| guidance_scale      | 5.0    | 가이던스               |
| num_chunks          | 8000   | 한 번에 처리하는 점 수 |
| face_count          | 40000  | 텍스처용 최대 면 수    |
| type                | glb    | 출력 형식              |

문서는 서버를 띄우면 `http://localhost:8081/docs`에서 Swagger UI를 쓸 수 있다고
적는다.[^doc-21-api]
기본 단계 수 5는 Turbo류의 값이어서, 일반 형태 모델을 이 서버에 물릴 때는 단계
수를 올려야 하는지 확인해야 한다.
이 문서가 이를 확인하지는 못했다.

2.1의 Docker 안내는 Windows 10에서 시험했다고 하며, 빌드에 한 시간 넘게 걸리고
이미지가 70GB를 넘는다고 경고한다.
실행은 `docker run -it --name hy3d21 -p 7860:7860 --gpus all hunyuan3d21 python
gradio_app.py --port 7860`이다.[^doc-21-docker]
`--gpus all`이 들어 있어서 이 안내는 NVIDIA GPU가 있는 환경을 전제한다.

### 텍스트에서 3D, 다중 시점

Gradio 앱에 `--enable_t23d`를 주면 텍스트에서 3D가 켜진다.
이때는 `HunyuanDiTPipeline`으로
`Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled`를 불러 이미지를 먼저
만들고 그 이미지를 형태 모델에 넣는다.[^code-gradio]
그래서 텍스트에서 3D는 모델이 둘 필요하고 추가 가중치를 내려받아야 한다.
2mv는 앞, 뒤, 왼쪽, 오른쪽 네 시점 이미지를 받는 입력 칸이 Gradio 앱에 있고,
README는 `hunyuan3d-dit-v2-mv-turbo` 하위 폴더와 `--enable_flashvdm`을 쓰는
명령을 준다.[^code-gradio][^repo-2-readme]

### Blender, ComfyUI, 커뮤니티 묶음

Blender 애드온은 2025년 1월 27일에 나왔고 API 서버에 연결해 Blender 안에서
모델을 부른다.[^repo-2-readme]
HN의 sinzin91은 Claude Desktop이나 Cursor 같은 도구를 Blender에 연결하는 Blender
MCP를 소개하며 앞으로의 방향을 보여 준다고 했다.[^sinzin91]
2.0 README의 커뮤니티 자원 목록과 2.1 README의 기여 목록에 오른 프로젝트를
2026년 10월 27일 GitHub에서 읽은 값으로 정리한다.

| 프로젝트                                  | 스타  | 라이선스(GitHub 표시) | 마지막 푸시 | 비고                              |
| ----------------------------------------- | ----- | --------------------- | ----------- | --------------------------------- |
| ComfyUI-3D-Pack[^c-3dpack]                | 3,890 | MIT                   | 2025-12-29  | ComfyUI 3D 노드 묶음              |
| ComfyUI-Hunyuan3DWrapper[^c-kijai]        | 1,048 | 표시 없음             | 2026-03-16  | 2.0용 ComfyUI 래퍼                |
| ComfyUI-Hunyuan3d-2-1[^c-visualbruno]     | 391   | 표시 없음             | 2026-09-08  | 2.1용 ComfyUI 노드                |
| Hunyuan3D-2-WinPortable[^c-winport]       | 1,363 | GPL-3.0               | 2025-11-19  | Windows 설치 묶음                 |
| Hunyuan3D-2-for-windows[^c-sdbds]         | 218   | 표시 없음             | 2025-04-22  | Windows용 포크                    |
| Hunyuan3D-2GP[^c-2gp]                     | 462   | 표시 없음             | 2025-03-29  | 6GB VRAM 미만을 노리는 오프로딩판 |
| Hunyuan3D-2.1-Unity-XR-PC-Phone[^c-unity] | 28    | 표시 없음             | 2025-07-03  | 2.1 Unity 지원                    |

스타와 푸시일은 저장소 현황이며 품질이나 안정성을 말하지 않는다.
Windows 묶음의 GPL-3.0은 묶음 자체의 코드에 대한 표시이고, 안에 든 가중치는
여전히 Hunyuan 라이선스를 따른다.
이는 이 문서의 해석이다.
GitHub 라이선스란이 비어 있는 저장소는 라이선스가 없다는 뜻일 수도 있고 본문에
다른 형식으로 적혀 있다는 뜻일 수도 있어서, 쓰기 전에 직접 확인해야 한다.

## GPU 없이 CPU로 돌리기

이 절은 「CPU만으로도 꽤 만족스러웠다」는 사용 경험이 어떤 조건에서 성립하는지를
따진다.
읽은 자료가 보여 주는 CPU 경로는 형태(shape) 단계까지다.
텍스처 단계는 공식 경로에서 CUDA를 전제하고, 커뮤니티 포크 하나는 CUDA 없이
돈다고 주장하지만 이 문서가 확인하지 못했다.
형태만으로 충분한 용도라면 GPU 없이도 길이 있다는 것이 이 절의 요지다.

### 공식 코드가 허락하는 것

형태 파이프라인의 `from_pretrained`와 생성자는 `device`의 기본값이 `'cuda'`이고
`dtype`의 기본값이 `torch.float16`이다.
`device='cpu'`를 주면 모델이 CPU에 올라간다.[^code-pipelines]
Gradio 앱에는 `--device` 옵션(기본값 `cuda`)과 `--disable_tex` 옵션이 있고,
장치가 `cpu`나 `mps`이면 FlashVDM의 표면 추출을 `mc`로 강제한다.[^code-gradio]
이 분기는 공식 코드가 형태 단계에서 CPU와 MPS를 염두에 두었다는 흔적이다.

`--low_vram_mode`는 CPU 모드가 아니다.
이 옵션은 텍스처 모델의 CPU 오프로드를 켜고 `torch.cuda.empty_cache()`를 부르는
CUDA 전제의 절약책이다.[^code-gradio]
텍스처 파이프라인(2.0)은 장치를 `'cuda'`로 고정하고 있고, 설치 안내도
텍스처용으로 CUDA 확장 `custom_rasterizer`를 빌드하라고
한다.[^code-tex][^repo-2-readme]
그래서 CUDA가 없는 장비에서는 텍스처용 빌드를 건너뛰고 형태만 돌리는 쪽이 공식
경로가 가리키는 방향이다.

공식 이슈 게시판에도 같은 내용이 보인다.
AMD 카드 사용자가 형태 생성만 하려면 설치 안내의 어느 단계를 건너뛸지 묻자, 한
사용자는 텍스처용 빌드(`# for texture`)를 건너뛰고 Gradio 앱을 띄우라고
답했다.[^issue53-yan]
다른 사용자는 `device="cpu"`로 고쳐 Ryzen 5 5500에서 돌렸는데 “아주 오래
걸렸다”고 적었고, MPS는 시도하지 않았다고 했다.[^issue53-cpu]
같은 이슈에서 ROCm을 쓰는 한 사용자는 24GiB VRAM으로 형태는 충분하지만(약 16GiB)
텍스처는 모자랐다고 적었다.[^issue53-rocm]
macOS를 묻는 이슈에는 개발진의 한 사람이 형태 생성이 macOS에서 도는 버전을 곧
내겠다고 답했다(2025년 3월 12일).[^issue123]
그 약속이 지켜진 시점이나 형태는 확인하지 못했다.

HN에서는 manjunaths가 Radeon 7900 GRE 16GB와 WSL 우분투, ROCm 6.3.4로 Turbo를
돌려 보고 비Turbo보다 훨씬 빠르다고 평하면서, 시간의 대부분이 형태가 아니라
텍스처 생성에 쓰인다고 적었다.[^manjunaths]
Turbo가 줄이는 것은 형태 생성이고 텍스처 단계가 느리다는 관찰은, 앞의 구조
설명과 일치한다.

### 공개된 측정 기록

CPU나 CUDA 이외 장치에서 시간을 잰 공개 기록은 적다.
읽은 기록은 모두 개인이나 작은 프로젝트가 잰 값이며 공식 벤치마크가 아니다.

| 출처                            | 장치                         | 설정                                            | 결과                                | 범위          |
| ------------------------------- | ---------------------------- | ----------------------------------------------- | ----------------------------------- | ------------- |
| GCaggianese 검증[^gc-cpu]       | Intel i7-11800H CPU          | 2mv Turbo, 5단계, FlashVDM, 해상도 256, FP32    | 1시점 169.92초, 최대 메모리 6.81GiB | 형태만        |
| 위와 같음                       | 위와 같음                    | 3시점                                           | 330.74초, 6.80GiB                   | 형태만        |
| 위와 같음(비교용 TripoSR)       | 위와 같음                    | TripoSR 1시점                                   | 36.41초, 3.61GiB                    | 형태만        |
| VladimirTalyzin 포크[^mac-rocm] | Apple M4 Pro 24GB, MPS       | 2.1, 형태 30단계 해상도 192, 텍스처 6시점 256px | 형태 344초, PBR 텍스처 512초        | 형태와 텍스처 |
| 위와 같음                       | AMD Radeon 8060S(iGPU), ROCm | 같은 설정                                       | 형태 약 6.4분, 텍스처 약 2.5분      | 형태와 텍스처 |
| m3dium[^m3dium]                 | Apple M1, M4                 | 자체 앱(MLX 기반으로 읽힘)                      | M1 약 4분, M4 약 2분                | 범위 불명     |
| hy3dgen-8g-laptop[^wth]         | RTX 5060 노트북 8GB          | 2mini Turbo, 낮은 해상도                        | 총 52.5초, 78,146면                 | 형태만        |

GCaggianese 기록의 세부를 더 읽으면 CPU 시간이 어디에 가는지 보인다.
3시점 330.74초 중 샘플링이 256.37초이고, DINO 로딩이 34.10초, VAE 로딩과
디코딩이 34.59초다.
1시점은 샘플링이 123.28초이고 DINO 로딩이 10.28초, VAE 로딩과 디코딩이
30.32초다.[^gc-cpu]
시점을 셋으로 늘리면 총 시간이 1.95배가 되고, 세 시점 윤곽 겹침(IoU) 평균은
0.7292에서 0.7966으로 올랐다.
이 값은 윤곽의 일치도이지 보정된 품질 점수가 아니라고 기록 자체가
밝힌다.[^gc-cpu]
이 측정은 DINO와 확산 모델과 VAE를 번갈아 올리고 쓴 모듈을 내려 메모리 최고점을
낮추었다.
공식 PyTorch 2.5.1 CPU 빌드를 쓰고 FP16으로 배포된 가중치를 FP32로 올려
돌렸으며, 코드와 가중치의 커밋 해시를 기록에 남겼다.[^gc-cpu]

이 기록에서 얻을 수 있는 신중한 결론은 세 가지다.
첫째, 노트북급 CPU에서도 2mv Turbo의 1시점 형태 생성이 3분 안쪽에 끝난
사례가 있다.
둘째, 그때의 최대 메모리가 약 6.8GiB여서 RAM이 넉넉하지 않은 장비도 가능성이
있다고 읽히지만, 8GB 이하 RAM에서 되는지는 확인하지 못했다.
셋째, 같은 실험의 TripoSR는 36.41초로 훨씬 빨랐다.
형태 품질이 비슷한 구간에서 빠른 대안이 있다는 뜻이지만, 품질 비교는 이 문서가
하지 않았다.

Apple Silicon의 기록은 형태보다 텍스처가 훨씬 비싸다는 점을 보여 준다.
M4 Pro에서 형태는 344초(약 5.7분)이고 PBR 텍스처는 512초(약 8.5분)였으며, 텍스처
단계에서 약 8GB의 스왑이 쓰였다고 포크의 README가 적는다.[^mac-rocm]
같은 README의 표는 CPU만 쓰는 경우를 형태는 되지만 매우 느리고 텍스처도 매우
느리다고 적는다.[^mac-rocm]
그 포크는 `custom_rasterizer`에 완전한 CPU 구현이 들어 있어 CUDA 커널이 필수가
아니라고도 주장한다.[^mac-rocm]
이 문서는 이 주장을 코드로 확인하지 못했으므로, 공식 2.0 경로의 텍스처가 CUDA를
요구한다는 앞의 서술과 별개의 포크 주장으로 두었다.

### CPU에서 먼저 줄일 항목

| 조절 항목         | 낮추거나 바꾸면                                         | 근거                                              |
| ----------------- | ------------------------------------------------------- | ------------------------------------------------- |
| 추론 단계         | DiT 호출 횟수가 단계 수에 비례해 준다                   | 샘플링 반복문. Turbo의 기록 설정은 5단계[^gc-cpu] |
| 모델 변형         | mini Turbo는 파일이 3.82GB로 가장 작다                  | 파일 크기 표                                      |
| 시점 수           | 1시점이 3시점의 약 절반 시간                            | GCaggianese 기록[^gc-cpu]                         |
| octree_resolution | 격자점이 해상도의 세제곱으로 줄고 마칭 큐브 부담도 준다 | 아래 합성 실험                                    |
| num_chunks        | 디코더 한 번에 넣는 점 수를 줄이면 최고 메모리가 준다   | 기본 8000, 기록은 2048[^gc-cpu]                   |
| mc_algo           | CPU에서는 `mc`만 쓴다                                   | `dmc`는 `diso`의 GPU 구현[^code-surface]          |
| 텍스처 단계       | `--disable_tex`로 끄면 CUDA 확장이 필요 없다            | Gradio 앱 옵션[^code-gradio]                      |

num_chunks를 줄이면 메모리가 준다는 서술은 이 문서의 해석이다.
기록은 청크 2048을 썼다고만 밝히고 이 값이 메모리에 미친 영향을 따로 재지
않았다.
스레드 수는 기록이 8로 두었다고만 알려 줄 뿐 다른 값과 견주지 않았다.

### 합성 도형으로 보는 해상도 비용

Hunyuan3D 가중치 없이 같은 종류의 격자에서 표면을 뽑을 때 비용이 해상도에 따라
어떻게 변하는지 합성 부호 거리장으로 쟀다.
스크립트와 전체 출력은 아래 「후처리와 내보내기」 절에 있다.
이 실행은 Apple M4 Max(14코어, 36GB) 한 대에서 한 번 돌린 값이고 CPU 전용 장비가
아니며, 초는 잡음이 크다.
격자점 수와 메모리는 산술로 정해지는 값이다.

| 해상도 | 격자점 수  | 32비트 값 격자 메모리 | 합성 도형의 마칭 큐브 출력 면 수 |
| ------ | ---------- | --------------------- | -------------------------------- |
| 128    | 2,146,689  | 8.6MB                 | 57,288                           |
| 256    | 16,974,593 | 67.9MB                | 228,192                          |
| 384    | 57,066,625 | 228.3MB               | 511,616                          |

해상도를 256에서 384로 올리면 점 수가 3.4배, 값 격자 메모리도 3.4배가 된다.
이 표는 값 격자만 센 것이고 모델 가중치와 디코더 중간값의 메모리는 포함하지
않는다.
실제 모델에서 해상도가 총 시간에 미치는 영향은 이 문서가 재지 못했다.
형태 모델의 디코더가 격자점마다 값을 내는 방식이어서 시간이 점 수에 비례해 늘
것이라는 추측은 가능하지만, 확인된 사실이 아니다.

### 형태만 CPU에서 돌리는 코드

아래는 앞에서 읽은 코드의 인자만 조합한 스크립트다.
이 조합을 문서가 약속하는 것은 아니며, 이 문서가 실행해 보지 못했다.
CPU 측정 기록이 쓴 설정(Turbo 5단계, FlashVDM, 해상도 256, 청크 2048, FP32)을
따랐다.[^gc-cpu]

```python
import torch
from PIL import Image

from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

torch.set_num_threads(8)  # 기록은 8스레드. 물리 코어 수에 맞춘다

# 데모 스크립트의 배경 제거 분기가 실행되지 않으므로 직접 지운다
image = BackgroundRemover()(Image.open('assets/demo.png').convert('RGB'))

pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    'tencent/Hunyuan3D-2mini',
    subfolder='hunyuan3d-dit-v2-mini-turbo',
    use_safetensors=True,
    device='cpu',               # 기본값은 'cuda'
    dtype=torch.float32,        # 기본값은 float16
)
pipe.enable_flashvdm(mc_algo='mc')   # Turbo VAE로 바꿔 끼운다
pipe.to('cpu', torch.float32)        # 바뀐 VAE의 자료형도 맞춘다

mesh = pipe(
    image=image,
    num_inference_steps=5,      # Turbo
    octree_resolution=256,
    num_chunks=2048,
    generator=torch.manual_seed(12345),
)[0]
mesh.export('out.glb')
```

`pipe.to('cpu', torch.float32)` 줄이 들어간 이유는 코드에 있다.
`enable_flashvdm`이 VAE를 새로 불러올 때 `dtype`을 넘기지 않아 VAE 로더의 기본값
`float16`이 되고, 형태 모델만 FP32이면 자료형이 어긋날 수 있다고 읽히기
때문이다.[^code-pipelines][^code-vae]
`to` 메서드가 VAE와 모델과 조건 인코더의 자료형과 장치를 한꺼번에
바꾼다.[^code-pipelines]
이 해석도 실행으로 확인하지 못했다.
첫 실행에는 가중치를 허깅페이스에서 내려받는 시간이 포함된다.

### 한계

- 읽은 측정은 개인이나 작은 프로젝트가 장비 한두 대에서 얻은 것이고, 가장 자세한
CPU 기록은 각 설정을 한 번씩만 실행했다고 밝힌다.
- 텍스처 단계를 CPU에서 돌렸다는 확인된 기록은 찾지 못했다.
- 공식 문서는 CPU 요구 사양을 따로 적지 않는다.
README의 VRAM 수치는 GPU 기준이다.
- 이 문서는 Hunyuan3D 가중치를 내려받지 않았고 CPU에서 모델을 돌려 보지 못했다.
- 「꽤 만족스러웠다」는 평가는 사용자의 주관이며 입력과 결과를 함께 남긴 비교가
아니다.

## 값 정하기

| 상황                         | 시작값                            | 근거                                                                           |
| ---------------------------- | --------------------------------- | ------------------------------------------------------------------------------ |
| 형태만 필요하다              | 2.0 DiT 또는 mini Turbo           | README가 형태 생성은 6GB라고 하고 mini는 0.6B다                                |
| 텍스처까지 한 GPU에서 돌린다 | 2.0이면 16GB, 2.1이면 29GB 이상   | 2.1의 PBR 텍스처는 21GB, 합계 29GB를 요구한다고 README가 적는다                |
| GPU가 작다                   | `--low_vram_mode`, 단계 분리 실행 | llm_nerd는 3060(12GB)에서 단계별로 나눠 돌렸다고 했다[^llm_nerd-3060]          |
| PBR 재질이 필요하다          | 2.1 Paint                         | 2.0 Paint는 RGB 기반이다                                                       |
| 다중 시점 입력               | 2mv                               | 시점이 여럿이면 형태 정확도가 오른다고 기대할 수 있다. 이는 이 문서의 해석이다 |
| 가벼운 단일 이미지 복원      | [TripoSR](triposr.md)             | MIT 라이선스이고 VRAM 약 6GB지만 텍스처와 PBR 기능은 약하다                    |

HN의 sorenjan은 2.0의 `hunyuan3d-dit-v2-0` 가중치 파일이 4.93GB라고 알려 모델의
크기를 가늠하는 방법을 보여 주었다.[^sorenjan]
Turbo에 대해서는 스레드 제목이 4090에서 형태 생성이 약 1초라고 주장한다.
thot_experiment는 2.0과 Fast를 많이 써 보았고 추론이 가벼워서 잠재 변수를
디코딩하는 데 더 많은 시간이 든다고 적었다.[^thot_experiment]

## 후처리와 내보내기

Hunyuan3D의 형태 출력은 격자 값에서 마칭 큐브로 뽑은 삼각형 메시다.
HN의 MITSardine는 저장소를 잠깐 훑어 본 결과 모델이 점 구름 같은 중간 표현을
만들고 그 위에 마칭 큐브 같은 비ML 방식으로 표면을 뽑는다고 읽었다.
처음에는 어떻게 유효한 메시를 안정적으로 내는지 궁금했는데, 답은 메시를 직접
만들지 않는 것이라 현명하다고 했다.[^MITSardine]
앞의 코드 읽기가 이 관찰과 맞는다.
모델은 격자 값을 내고 표면은 마칭 큐브가 뽑는다.
이 구조 때문에 결과 메시에는 다음 성질이 따라온다.

- 삼각형이 균일하고 매우 많다.
CPU 실측 기록의 해상도 256 출력은 약 41만~44만 면이었다.[^gc-cpu]
- 면적이 0인 면이 섞인다.
같은 기록은 원본 GLB 둘에서 면적이 정확히 0인 면이 각각 182,424개와
216,800개라고 보고했고, 이 면만 지우고 정점은 건드리지 않은 사본은 trimesh
기준으로 닫혀 있었다.
닫혀 있다는 것이 시각적 결함이 없다는 뜻은 아니라고 기록 자체가
덧붙인다.[^gc-cpu]
- 떨어진 작은 조각이 생길 수 있다.
저장소의 `FloaterRemover`가 전체 면의 0.5% 미만인 조각을 지우는
이유다.[^code-post]

HN에서는 자동 재위상(리토폴로지)이 잘 통하지 않는다는 보고가 이어졌다.
kilpikaarna는 Quad Remesher가 AI 없이 영리한 알고리즘만으로 사각형 메시를 만드는
상용 도구이고 영구 상용 라이선스가 109달러(월 구독은 15달러)라고
소개했다.[^kilpikaarna]
llm_nerd는 이 도구를 Hunyuan3D v2의 출력에 써 보니 인간이 만든 위상에서는 잘
되지만 이 출력에서는 모델을 크게 해치고 아주 명백한 단순화도 놓치며 낮은 감축
설정에서도 충실도를 무너뜨린다고 답했다.[^llm_nerd-remesher]
같은 사용자는 앞서 Hunyuan3D가 만든 메시가 어떤 도구로도 잘 줄지
않는다고도 썼다.
이는 개인의 시험 보고이므로 도구를 가리지 않는 결론으로 읽으면 안 되고, 합성
도형으로 해 본 아래 실행에서도 사각형 재위상은 시험하지 않았다.

### 용도별로 무엇을 고칠까

| 용도               | 먼저 할 일                                         | 형식과 확인                                      |
| ------------------ | -------------------------------------------------- | ------------------------------------------------ |
| 게임 엔진          | 면 수를 목표치로 줄이고 떨어진 조각을 정리한다     | GLB. 엔진에서 스케일과 방향을 확인한다           |
| 3D 프린트          | 닫힌 메시인지 확인하고 크기를 밀리미터로 맞춘다    | STL이나 OBJ. 슬라이서에서 닫힘과 두께를 확인한다 |
| 웹 뷰어            | 면 수와 파일 크기를 줄인다                         | GLB                                              |
| 다시 텍스처 입히기 | 40,000면 안팎으로 줄인 메시를 텍스처 모델에 넣는다 | 앱이 기본으로 하는 순서와 같다[^code-gradio]     |

Gradio 앱이 내보낼 수 있는 형식은 `glb`, `obj`, `ply`, `stl`이다.[^code-gradio]
이 표는 이 문서의 제안이며, 면 수의 구체적 목표치는 엔진과 기기에 따라 달라서
적지 않았다.
리깅이 필요하면 오픈 가중치에는 그 기능이 없고 호스티드 서비스가 후처리
기능으로 판다.

### 합성 도형으로 해 본 정리 스크립트

아래 스크립트는 Hunyuan3D 없이 같은 종류의 격자에서 표면을 뽑는 합성 도형(구와
기둥과 떨어진 고리)을 만들고, 사용자가 흔히 할 정리를 순서대로 적용한다.
면적 0인 면 제거, 가장 큰 조각만 남기기, 닫힘 확인, 쿼드릭 단순화, 100mm 높이로
스케일, GLB와 OBJ와 STL 내보내기다.
저장소 밖 임시 가상환경에 `numpy`, `scipy`, `scikit-image`, `trimesh`,
`fast-simplification`을 설치해 실행했다.

```python
"""Synthetic stand-in for a Hunyuan3D shape output.

Hunyuan3D's shape stage predicts an implicit field on a regular grid of
(octree_resolution + 1)^3 points and turns it into triangles with marching
cubes.  This script builds a synthetic signed-distance field on the same kind
of grid, extracts a surface the same way, and then does the clean-up a user
would do before using the mesh: drop zero-area faces, keep the largest
component, check watertightness, decimate, and export GLB / OBJ / STL.

No Hunyuan3D weights are involved; the numbers below describe this synthetic
shape only.
"""
import os
import sys
import time

import numpy as np
import trimesh
from skimage import measure
import fast_simplification

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
BOX = 1.01  # same default as the pipeline's box_v


def sdf(p):
    """Blob made of a sphere, a capsule-like pillar and a thin torus."""
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    sphere = np.sqrt(x**2 + (y - 0.25) ** 2 + z**2) - 0.45
    # vertical pillar (rounded cylinder) below the sphere
    r = np.sqrt(x**2 + z**2)
    pillar = np.maximum(r - 0.18, np.abs(y + 0.35) - 0.45)
    # thin torus around the middle
    q = np.sqrt((np.sqrt(x**2 + z**2) - 0.6) ** 2 + (y + 0.05) ** 2) - 0.07
    return np.minimum(np.minimum(sphere, pillar), q)


def run(res):
    t0 = time.perf_counter()
    axis = np.linspace(-BOX, BOX, res + 1, dtype=np.float32)
    grid = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1)
    field = sdf(grid).astype(np.float32)
    t_field = time.perf_counter() - t0

    t0 = time.perf_counter()
    spacing = (2 * BOX / res,) * 3
    v, f, _, _ = measure.marching_cubes(field, level=0.0, spacing=spacing)
    v = v - BOX
    t_mc = time.perf_counter() - t0

    mesh = trimesh.Trimesh(vertices=v, faces=f, process=False)
    zero_area = int((mesh.area_faces == 0).sum())
    tiny = int((mesh.area_faces < 1e-12).sum())
    mesh.update_faces(mesh.area_faces > 1e-12)
    mesh.remove_unreferenced_vertices()
    parts = mesh.split(only_watertight=False)
    biggest = max(parts, key=lambda m: len(m.faces))
    return dict(
        res=res,
        grid_points=(res + 1) ** 3,
        field_mb=field.nbytes / 1e6,
        t_field=t_field,
        t_mc=t_mc,
        faces=len(f),
        zero_area=zero_area,
        tiny=tiny,
        components=len(parts),
        watertight=biggest.is_watertight,
        mesh=biggest,
    )


print("res | grid pts | field MB | field s | MC s | faces | zero-area | comps | watertight")
results = {}
for res in (128, 256, 384):
    r = run(res)
    results[res] = r
    print(
        f"{r['res']:>3} | {r['grid_points']:>9,} | {r['field_mb']:>7.1f} | {r['t_field']:>6.2f} |"
        f" {r['t_mc']:>5.2f} | {r['faces']:>7,} | {r['zero_area']:>4} | {r['components']:>3} | {r['watertight']}"
    )

mesh = results[256]["mesh"]
print("\nresolution 256 mesh: verts", len(mesh.vertices), "faces", len(mesh.faces))
print("watertight:", mesh.is_watertight, "| volume:", round(mesh.volume, 4))
print("bounds:", np.round(mesh.bounds, 3).tolist())

# decimate with quadric edge collapse
for target in (50000, 20000, 5000):
    ratio = 1 - target / len(mesh.faces)
    t0 = time.perf_counter()
    v2, f2 = fast_simplification.simplify(
        mesh.vertices.astype(np.float32), mesh.faces.astype(np.int32), target_reduction=ratio
    )
    dt = time.perf_counter() - t0
    m2 = trimesh.Trimesh(v2, f2, process=False)
    print(
        f"decimate to ~{target:>6,}: faces {len(f2):>6,} | {dt:5.2f} s | "
        f"watertight {m2.is_watertight} | volume {m2.volume:.4f} "
        f"({(m2.volume / mesh.volume - 1) * 100:+.2f}%)"
    )
    if target == 20000:
        keep = m2

# scale to 100 mm tall for 3D printing and export three formats
keep = keep.copy()
height = keep.bounds[1][1] - keep.bounds[0][1]
keep.apply_scale(100.0 / height)
keep.apply_translation(-keep.bounds[0])
print("\nscaled for printing: extents (mm)", np.round(keep.extents, 1).tolist())
for ext in ("glb", "obj", "stl"):
    path = os.path.join(OUT, f"blob.{ext}")
    keep.export(path)
    print(f"{ext}: {os.path.getsize(path) / 1e3:8.1f} kB")

# round trip to confirm the STL is still a closed solid
back = trimesh.load(os.path.join(OUT, "blob.stl"))
print("reloaded STL: watertight", back.is_watertight, "| faces", len(back.faces))
```

실행 출력은 다음과 같다.

```text
res | grid pts | field MB | field s | MC s | faces | zero-area | comps | watertight
128 | 2,146,689 |     8.6 |   0.02 |  0.38 |  57,288 |    0 |   2 | True
256 | 16,974,593 |    67.9 |   0.27 |  0.09 | 228,192 |    0 |   2 | True
384 | 57,066,625 |   228.3 |   0.99 |  0.29 | 511,616 |    0 |   2 | True

resolution 256 mesh: verts 75266 faces 150528
watertight: True | volume: 0.4446
bounds: [[-0.45, -0.8, -0.45], [0.45, 0.7, 0.45]]
decimate to ~50,000: faces 49,998 |  0.05 s | watertight True | volume 0.4445 (-0.02%)
decimate to ~20,000: faces 20,000 |  0.06 s | watertight True | volume 0.4443 (-0.07%)
decimate to ~ 5,000: faces  5,000 |  0.08 s | watertight True | volume 0.4228 (-4.90%)

scaled for printing: extents (mm) [60.0, 100.0, 60.0]
glb:    360.7 kB
obj:    710.5 kB
stl:   1000.1 kB
reloaded STL: watertight True | faces 20000
```

이 출력에서 읽을 것은 다음과 같다.
이 도형은 합성이며 Hunyuan3D 출력이 아니고, 시간은 M4 Max 한 대에서 한 번 잰
값이다.

- 마칭 큐브 출력에는 면적 0인 면이 0개였다.
이 합성 도형은 scikit-image의 구현을 썼기 때문이며, CPU 기록이 본 면적 0 면의
문제를 재현하지 않는다.
그래서 스크립트의 면적 검사는 실제 출력에 쓸 때 의미가 있다.
- 조각이 둘이었다.
고리가 구와 기둥에서 떨어져 있어서다.
가장 큰 조각만 남기는 방식은 이 고리를 지웠다.
의도한 분리 부품이 있는 모델에는 이 방식을 쓰면 안 된다.
- 단순화는 면 수를 150,528개에서 20,000개로 줄이는 데 약 0.06초가 걸렸고 부피가
0.07% 달라졌으며, 5,000개에서는 4.90% 달라졌다.
닫힘은 세 경우 모두 유지되었다.
- 20,000면에서 파일은 GLB 약 361kB, OBJ 약 711kB, STL 약 1,000kB였다.
같은 메시도 형식에 따라 크기가 세 배 가까이 다르다.
- STL을 다시 읽어도 닫힌 메시로 확인되었다.

실제 Hunyuan3D 출력에서는 면적 0인 면, 많은 조각, 비다양체 가장자리를 먼저
검사하고, 그 결과에 따라 같은 순서의 정리를 적용하는 것이 현실적이다.
이 순서는 이 문서의 제안이며 실제 출력으로 검증하지 못했다.

## 다른 모델과 견주기

Hunyuan3D 2.1의 README는 TripoSG, Step1X-3D, Trellis 같은 모델을 이름을 밝혀
비교하지만, 앞의 성능 절에서 보았듯 자체 평가다.
여기서는 점수 대신 독자가 고를 때 걸리는 사실만 모았다.
라이선스와 하드웨어 요구와 CPU 언급이다.
모두 각 저장소의 README와 라이선스 표시, 허깅페이스 카드에서 2026년 10월 27일에
읽은 값이다.

| 모델                       | 라이선스(표시)                                     | 스타   | README의 GPU 요구                 | CPU 언급                                       | 마지막 푸시 |
| -------------------------- | -------------------------------------------------- | ------ | --------------------------------- | ---------------------------------------------- | ----------- |
| Hunyuan3D 2.1              | Tencent 커뮤니티(EU, 영국, 한국 제외)              | 4,290  | 형태 10GB, 텍스처 21GB, 합계 29GB | 언급 없음                                      | 2025-10-17  |
| Hunyuan3D 2.0              | 위와 같은 계열                                     | 15,209 | 형태 6GB, 합계 16GB               | 언급 없음(코드에 `device` 인자)                | 2025-10-28  |
| TRELLIS[^cmp-trellis]      | MIT                                                | 14,120 | NVIDIA 16GB 이상                  | 언급 없음                                      | 2026-10-27  |
| TRELLIS.2[^cmp-trellis2]   | MIT                                                | 12,492 | NVIDIA 24GB 이상, 매개변수 4B     | 언급 없음                                      | 2026-07-10  |
| TripoSG[^cmp-triposg]      | MIT                                                | 1,864  | CUDA GPU 8GB 이상                 | 언급 없음                                      | 2025-04-18  |
| TripoSR[^cmp-triposr]      | MIT                                                | 7,234  | 단일 이미지 기본 약 6GB           | 마칭 큐브 CPU 대체 문구만 있음                 | 2026-06-04  |
| SF3D[^cmp-sf3d]            | Stability AI 커뮤니티(허깅페이스 카드)[^hf-sf3d]   | 1,907  | 단일 이미지 기본 약 6GB           | GPU가 없으면 CPU 자동, `SF3D_USE_CPU=1`로 강제 | 2025-01-22  |
| SPAR3D[^cmp-spar3d]        | Stability AI 커뮤니티(허깅페이스 카드)[^hf-spar3d] | 1,084  | 기본 10.5GB, 저VRAM 모드 약 7GB   | CPU 지원, README는 아주 느리다고 적음          | 2025-05-05  |
| Step1X-3D[^cmp-step1x]     | Apache-2.0                                         | 898    | 27~29GB, 50단계에 152초           | 언급 없음                                      | 2025-09-08  |
| InstantMesh[^cmp-instant]  | Apache-2.0                                         | 4,579  | README에서 VRAM 수치를 찾지 못함  | 언급 없음                                      | 2025-01-03  |
| SAM 3D Objects[^cmp-sam3d] | SAM License(허깅페이스 수동 승인)[^hf-sam3d]       | 7,581  | README에서 VRAM 수치를 찾지 못함  | 언급 없음                                      | 2026-06-02  |

표에서 읽을 수 있는 것은 세 가지다.
첫째, 한국에서 쓰려는 독자에게 지역 제한이 없는 선택지로 읽히는 것은 MIT인
TRELLIS 계열과 TripoSG와 TripoSR, Apache-2.0인 Step1X-3D와 InstantMesh다.
이 문서는 각 라이선스의 본문을 끝까지 읽지 않았고 저장소와 허깅페이스 카드의
표시만 확인했으므로, 실제로 쓰기 전에 본문을 읽어야 한다.
둘째, CPU를 문서로 지원하는 쪽은 Stability AI의 두 모델이다.
SF3D는 GPU가 없으면 CPU를 자동으로 쓰고, 통합 메모리가 32GB보다 작은 Apple
장비에서는 MPS보다 CPU를 권한다고 적는다.[^cmp-sf3d]
SPAR3D는 CPU 지원을 적지만 아주 느리다고 밝힌다.[^cmp-spar3d]
Hunyuan3D에는 이런 문장이 없고 CPU 경로는 코드와 커뮤니티 기록에서 읽어야 한다.
셋째, 허깅페이스 API가 돌려준 `downloads` 값에서 TRELLIS 계열의 TRELLIS.2-4B는
2,582,870, TRELLIS-image-large는 2,484,768로 Hunyuan3D 2.0의 172,834보다 훨씬
크다.[^hf-trellis2][^hf-trellis][^hf-2]
집계 기간과 방식이 서로 같은지 확인하지 못했으므로 대략적인 규모 차이로만
읽어야 한다.

SAM 3D Objects는 마스크로 지정한 물체에서 포즈와 형태와 텍스처와 배치를 만드는
Meta의 모델이고, 2025년 11월 19일에 체크포인트가 공개되었으며 2026년 6월 1일에
인코더 가중치가 나왔다고 README가 적는다.[^cmp-sam3d]
Hunyuan3D와 입력 방식이 달라서(이미지 전체가 아니라 마스크된 물체와 장면) 같은
기준으로 비교하지 않았다.

## 호스티드 서비스와 요금

공식 호스티드 서비스는 두 갈래다.
중국 본토 사이트(`3d.hunyuan.tencent.com`)는 중국어 로그인 화면으로 열리고,
글로벌 사이트(`hy3d.tencent.ai`)도 로그인이 필요하다.
이 문서는 로그인하지 않았으므로 두 사이트의 화면 안쪽 기능과 일일 무료 한도는
확인하지 못했다.
글로벌 사이트는 접속하면 먼저 알림을 보여 준다.
실험실의 3D Smart Topology와 Sketch to 3D 기능을 내리고 3D Studio의 형태 생성,
리토폴로지, 텍스처 칠하기 모듈로 합친다는 내용이다.

Tencent는 2025년 11월 26일에 3D 엔진을 전 세계로 연다고 발표하면서 신규
창작자에게 하루 20회 무료 생성을, Tencent Cloud의 API를 쓰는 기업 사용자에게 200
크레딧을 주겠다고 했다.[^tencent-press]
발표문은 3.0이 고품질 객체 에셋에 집중한다고 설명하고, 텍스트와 이미지(최대
4장의 다중 시점)와 스케치 입력, 삼각형이나 사각형 면으로의 자동 위상 최적화,
OBJ와 GLB 내보내기, Unity와 Unreal Engine과 Blender 연동을
소개한다.[^tencent-press]
중국 본토에서는 150곳이 넘는 기업이 Tencent Cloud를 통해 연동했고 Unity China와
Bambu Lab과 Liblib이 포함된다고도 한다.[^tencent-press]

API의 요금은 Tencent Cloud의 청구 문서에 정리되어 있다.
문서는 2026년 5월 8일에 갱신되었고, 첫 활성화 때 200 크레딧의 무료 한도를 주며
1년 안에 쓰지 않으면 소멸한다고 한다.[^billing]
선불 패키지는 1,000 크레딧에 15달러, 10,000 크레딧에 145달러, 50,000 크레딧에
700달러, 100,000 크레딧에 1,350달러이고 1년 유효하다.[^billing]
후불은 크레딧당 0.02달러이고 하루 단위로 정산한다.[^billing]

호출당 크레딧은 작업 종류에 따라 다르다.

| 구분         | 작업                             | 크레딧 |
| ------------ | -------------------------------- | ------ |
| Professional | Normal(텍스처가 있는 모델, 기본) | 25     |
| Professional | LowPoly                          | 30     |
| Professional | Geometry(텍스처 없음)            | 15     |
| Professional | Sketch                           | 25     |
| Express      | 텍스트에서 3D                    | 15     |
| Express      | 이미지에서 3D                    | 15     |
| 후처리       | 3D 파트 생성                     | 30     |
| 후처리       | Smart Topology                   | 50     |
| 후처리       | 3D 텍스처 편집                   | 30     |
| 후처리       | UV 펼치기, 자동 리깅             | 각 10  |
| 후처리       | 3D 형식 변환                     | 5      |

Professional의 추가 옵션(다중 시점 이미지, PBR, 면 수 지정)은 각각 10 크레딧이
더 들고 Express의 PBR은 10 크레딧이 더 든다.[^billing]
문서는 모델 버전으로 3.0이나 3.1을 고르는 데 추가 비용이 없다고 한다.[^billing]
실패한 작업은 콘텐츠 위험 관리에 걸린 경우를 포함해 과금되지 않는다.[^billing]
동시 작업은 기본 Professional 3개, Express 1개이고 주 계정과 하위 계정이
공유한다.[^billing]
같은 문서는 동시 작업 증설 패키지를 동시 작업 하나당 월 5,000달러로 적는데, 이
금액은 이 문서가 구매 화면에서 확인하지 못했으므로 예산에 넣기 전에 확인해야
한다.
이 표로 계산하면 PBR을 켠 LowPoly는 호출당 40 크레딧이고, 선불 1,000 크레딧으로
Normal 생성 약 40번을 한다.
이는 이 문서의 계산이다.

Tencent Cloud의 해설 글 일부는 신규 사용자에게 1,000 크레딧을 0달러에 준다고
쓰지만 그 행사는 2026년 6월 30일까지로 적혀 있어 이미 지났고, 이 문서는 현재
같은 혜택이 있는지 확인하지 못했다.
무료 한도에 대해서는 신규 200 크레딧(청구 문서)과 하루 20회(2025년 11월
발표문)가 따로 나오며, 지금 둘 다 적용되는지는 로그인 후에야 알 수 있다.

청구 문서의 단가 열을 보태면 선불 패키지의 크레딧당 단가는 1,000 크레딧이
0.015달러, 10,000 크레딧이 0.0145달러, 50,000 크레딧이 0.014달러, 100,000
크레딧이 0.0135달러다.[^billing]
이 단가로 계산하면 텍스처가 있는 Normal 생성(25 크레딧)은 1,000 크레딧
패키지에서 호출당 0.375달러이고 후불에서는 0.50달러다.
PBR을 켜면 10 크레딧이 더해져 35 크레딧이 된다.
이는 이 문서의 계산이다.
문서는 2026년 5월 8일에 갱신된 것이어서 지금의 화면 가격과 다를 수 있다.

Tencent 밖의 호스티드 경로도 있다.
Replicate의 `tencent/hunyuan3d-2` 페이지는 한 번 실행에 약 0.15달러(1달러에 약
6번)이고, 예측이 보통 3분 안에 끝나며 NVIDIA L40S에서 돈다고 적는다.
같은 페이지는 이 모델을 2025년 1월 21일의 Hunyuan3D 2.0으로 소개하고 라이선스를
적지 않는다.[^replicate]
fal의 `hunyuan3d-v21` 페이지는 생성 한 번에 0.3달러라고 적지만 이 엔드포인트가
지원 종료로 표시되어 있었다.[^fal21]
두 값 모두 2026년 10월 27일에 읽은 페이지의 표시이고, 입력에 따라 달라진다고
페이지가 밝히거나 지원이 끝난 상태이므로 예산에 쓰기 전에 현재 화면에서
확인해야 한다.
이들 서비스가 Hunyuan 라이선스의 지역 제한을 사용자에게 어떻게 적용하는지는 이
문서가 읽지 못했다.

## 파생 프로젝트

2.1 위에서 갈라진 프로젝트들이 이 계열의 활용 범위를 넓힌다.

Hunyuan3D-Omni는 2.1의 구조를 물려받고 점 구름, 복셀, 골격, 경계 상자를 추가
제어 신호로 받는 통합 프레임워크다.[^arxiv-omni]
저장소는 크기 3.3B의 모델과 `--control_type` 옵션(`point`, `voxel`, `bbox`,
`pose`)을 가진 `inference.py`를 제공하며 생성에 10GB VRAM이 든다고
한다.[^repo-omni]

Hunyuan3D-Part는 부품 단위 처리를 다룬다.
P3-SAM은 3D 메시를 의미 단위 부품으로 분할하고 X-Part는 분할된 부품을 완성된
부품으로 생성한다.[^part]
저장소 공지에 따르면 공개된 것은 X-Part의 가벼운 버전이고 전체 버전은
Hunyuan3D-Studio에서 쓸 수 있으며, P3-SAM은 어떤 입력 메시든 처리하지만 X-Part는
스캔한 메시나 AI가 만든 메시를 입력으로 권한다.[^part]

HY3D-Bench는 학습용 데이터셋 모음이다.
2026년 2월 4일에 공개되었고, 252,000개가 넘는 방수(watertight) 메시의 전체
데이터셋, 240,000개가 넘는 부품 분해 데이터셋, 1,252개 하위 범주에 걸친
125,000개가 넘는 합성 데이터셋으로 이루어지며 기준 모델로 0.8B 규모의
Hunyuan3D-Shape-v2-1 Small을 제공한다.[^repo-bench]

2026년 8월에는 두 갈래가 더 나왔다.
Hunyuan3D-Buffalo 1.0은 3D 이해, 텍스트에서 3D 생성, 지시 기반 3D 편집, 텍스트에
근거한 부품 생성을 한 구조에서 처리하는 모델이다.
저자들은 8,700만 규모의 3D 멀티모달 말뭉치(이해 샘플 2,500만, 텍스트에서 3D 쌍
5,000만, 편집 쌍 1,200만)로 학습했다고 쓴다.[^arxiv-buffalo]
WorldClaw는 텍스트에서 탐험 가능한 대규모 3D 세계를 만드는 에이전트
프레임워크로, 계획 에이전트가 지역과 지형과 에셋과 재질의 구조화된 명세를 만든
뒤 지형과 에셋과 배치를 단계적으로 쌓고 렌더링 기반 에이전트가
다듬는다.[^arxiv-worldclaw]
HN의 avaer는 이것이 모델이 아니라 모델들을 부르는 파이썬 스크립트이고 코드가
공개되지 않았다고 짚었으며,[^avaer] tjohns도 스레드 시점에 GitHub 저장소가 비어
있었다고 알렸다.[^tjohns]
이 문서가 확인한 시점의 저장소 현황과 위 상태가 같은지는 확인하지 못했다.

## 함정

### 라이선스를 모르고 시작한다

가장 큰 함정은 코드를 받아 돌려 본 뒤에야 한국이 허용 지역이 아니라는 점을 아는
것이다.
위 라이선스 절의 조항은 학습이나 연구 목적의 개인 시험을 따로 구분하지 않는다.
이 문서가 읽은 범위의 본문에서는 그런 예외를 찾지 못했다.

### 설치 환경의 취약성

텍스처 모델은 CUDA 확장을 직접 빌드해야 하고 CUDA 주 버전과 컴파일러 조합에
민감하다.
swframe2는 데모를 로컬에서 돌릴 때 가중치를 안전하지 않게 불러온다는 경고가 두
곳에서 나왔다고 알렸는데, 이는 가중치가 pickle 데이터로 배포되기 때문이라는
설명이 이어졌다.[^swframe2]
신뢰하지 않는 곳에서 받은 가중치를 불러오는 일의 위험은 일반적인 주의 사항이고,
이 문서는 공식 가중치에 문제가 있다고 주장하지 않는다.
또한 같은 사용자는 데모 이미지에서 메시가 너무 크다는 검사에 걸려 그 검사를
지우고 돌렸다고 했다.

### 결과 메시의 위상

llm_nerd는 생성된 메시가 면이 매우 많고 어떤 도구로도 잘 줄어들지 않으며, 숙련된
Blender 사용자는 훨씬 적은 정점으로 더 좋은 메시를 금방 만들 수 있다고
썼다.[^llm_nerd]
같은 사용자는 사각형 면으로 다시 만드는 도구를 2.0의 결과에 써 보니 형태를
심하게 해쳤다고도 했다.
deterministic은 정적 3D 모델은 잘 만들지만 삼각형이 지나치게 많고 사람이 아니면
골격이 없다고 적었다.[^deterministic]
결과를 게임이나 애니메이션에 넣으려면 리토폴로지와 리깅이라는 후처리가 따로
필요하고, 호스티드 서비스는 이를 후처리 기능으로 파는 반면 오픈 가중치에는 들어
있지 않다.

### 글자와 구조의 오류

steinhafen은 제품 이미지를 시험했을 때 모양은 잘 잡았지만 생성된 3D 모델의
글자가 읽히지 않는다고 했다.[^steinhafen]
이는 godelski와 Kelvin506이 보고한 구조 오류와 같은 종류의 한계로 읽히며, 문자와
악기처럼 세부 구조가 중요한 물체에서 특히 드러난다.
이는 이 문서의 해석이다.

### CPU로 돌릴 때의 함정

첫째, 기본 장치가 `cuda`다.
`device`를 `'cpu'`로 바꾸지 않으면 CUDA가 없는 환경에서 모델을 올리는 단계에서
실패한다고 읽힌다.[^code-pipelines]
둘째, `--low_vram_mode`를 CPU 대용으로 착각하기 쉽다.
이 옵션은 CUDA 전제의 절약책이어서 GPU가 없는 장비의 해법이
아니다.[^code-gradio]
공식 이슈 중에는 이 옵션을 켠 Gradio 앱에서 장치 오류가 났다는 제목의 것이
있다.[^issue244]
셋째, 텍스처용 빌드는 NVIDIA 컴파일러가 필요하다고 한 사용자가 설명했고, 그래서
CUDA가 없는 장비에서는 설치 절차의 텍스처용 단계를 건너뛰어야
한다.[^issue53-yan]
`custom_rasterizer` 빌드가 실패했다는 제목의 공식 이슈도 여러 건 있다.[^issue49]
넷째, 기본 자료형이 `float16`이다.
CPU에서 FP16이 느리거나 일부 연산이 지원되지 않을 수 있어서, 읽은 CPU 측정
기록은 FP16 가중치를 FP32로 올려 돌렸다.[^gc-cpu]
FP32는 같은 모델이 차지하는 메모리를 늘리므로, RAM이 모자란 장비에서는 FP16을
시도해 볼 이유가 생긴다.
CPU에서 FP16이 실제로 어떻게 동작하는지는 이 문서가 확인하지 못했다.
다섯째, FlashVDM을 켜면 바뀌어 들어오는 VAE의 자료형이 기본 `float16`이 될
수 있다.
형태 모델을 FP32로 올렸다면 `pipe.to()`로 자료형을 다시 맞추라고 위 코드에서
권했고, 이 점은 코드 읽기일 뿐 실행으로 확인하지 못했다.[^code-vae]
여섯째, 데모 스크립트가 배경 제거를 건너뛴다.
CPU에서 한 번 돌리는 데 몇 분이 걸리므로 입력이 나빠 다시 돌리는 비용이 크다.
배경을 미리 지우고 입력 이미지를 한 번 확인한 뒤 돌리는 편이 낫다.

## 트레이드오프

### 오픈 가중치의 자유와 최신 모델의 거리

오픈 가중치는 2.1에서 멈췄고 최신 개선은 호스티드 서비스에 있다.
오픈 쪽에서는 미세 조정과 로컬 실행과 비용 통제가 가능한 대신 최신 품질과 후처리
기능(자동 리깅, Smart Topology)을 얻지 못한다.
서비스 쪽은 반대다.
서비스는 최신 모델을 쓰고 후처리를 한 번에 받지만 크레딧 비용과 로그인과
데이터가 외부로 나간다는 부담이 있다.
그리고 한국의 사용자에게는 오픈 가중치의 길이 라이선스로 막혀 있으므로 실제
선택지는 서비스나 다른 오픈 모델로 좁아진다.
이는 이 문서의 해석이며, 서비스 약관의 지역 제한은 이 문서가 읽지 못했다.

### 품질과 VRAM

2.1의 PBR 텍스처는 합계 29GB를 요구해 소비자용 GPU 한 장에서 돌리기 어렵다.
2.0이나 mini는 가볍지만 PBR이 없다.
형태만 로컬에서 만들고 텍스처는 별도로 다루는 분리 실행이 현실적인 타협이고,
이는 두 모델이 따로 도는 구조 덕에 가능한 선택이다.

## 비평

### 평가가 자체 평가이고 기준이 가려져 있다

2.0 README의 표는 최고 오픈소스 모델과 최고 비공개 모델 세 개를 이름 없이
비교한다.
이름이 없으면 독자는 어떤 모델과 비교했는지 모르므로 재현도 반박도 할 수 없다.
2.1 표는 이름 있는 모델을 쓰지만 평가 물체와 설정이 README만으로는 재현되지
않는다.
수치 차이도 작은 곳이 많아 순위가 실사용 품질을 대변한다고 말하기 어렵다.

### 공개의 문서화가 개정을 따라가지 못한다

README에서 숫자가 어긋나는 곳이 여럿 보였다.
2.0 README는 2.1 모델의 크기를 3.0B와 1.3B로 적고 2.1 README는 3.3B와 2B로
적는다.
VRAM도 시점에 따라 달랐고 2.1의 예제 코드는 변수가 이어지지 않는다.
이는 빠르게 모델을 내놓는 팀의 문서가 뒤따르지 못했다는 신호로 읽히며, 세부
숫자는 하드웨어에서 직접 재야 한다.
이는 이 문서의 해석이다.

### 오픈이라는 이름과 허용 지역 사이의 간극

README는 오픈소스라고 쓰고, 발표문은 오픈소스 3D 모델이 Hugging Face 내려받기가
300만 건을 넘었다고 홍보한다.[^tencent-press]
그러나 라이선스는 지역과 사용자 규모와 결과물의 용도를 제한하는 커뮤니티
라이선스다.
지역 제한은 가중치를 받을 수 있다는 사실과 쓸 수 있다는 사실 사이에 간극을
만든다.
오픈이라는 이름만 보고 시작한 한국 사용자는 이 간극을 뒤늦게 발견할 위험이 있다.

### CPU로 충분하다는 경험은 한 사람의 한 번에서 일반화되지 않는다

이 문서를 쓰는 사람은 CPU만으로 꽤 만족스러웠다고 말하고, 가장 자세한 공개
기록은 노트북 CPU에서 2mv Turbo가 1시점에 169.92초, 3시점에 330.74초 걸렸다고
보여 준다.[^gc-cpu]
두 경험은 서로 받쳐 주지만 둘 다 한 사람이 한 장비에서 얻은 것이다.
그 기록은 각 설정을 한 번씩만 실행했고, 입력은 같은 대상의 생성 이미지 세
장이며, 결과는 텍스처가 없는 형태뿐이다.[^gc-cpu]
Ryzen 5 5500에서 `device='cpu'`로 돌린 다른 사용자는 아주 오래 걸렸다고만
적었는데, 그는 Turbo가 아닌 기본 모델을 쓴 것으로 읽히고 시간도 재지 않아 두
기록은 직접 견줄 수 없다.[^issue53-cpu]
따라서 「CPU로도 된다」는 말이 성립하는 조건은 노트북용 i7-11800H급 CPU, 형태만,
Turbo 단계 수, 중간 해상도로 읽는 것이 안전하다.
「만족스럽다」는 평가는 이 조건에서 기다릴 만하다는 뜻이지, 다른 용도에서도 같은
판단이 나온다는 뜻이 아니다.

### 공식 문서가 CPU를 다루지 않아 이 경로가 눈에 띄지 않는다

공식 README는 VRAM 수치만 적고 CPU 요구나 CPU에서의 속도를 적지 않는다.
CPU 경로는 코드의 `device` 인자와 Gradio 앱의 분기, 이슈 게시판의 댓글, 커뮤니티
포크의 README에 흩어져 있다.
그래서 GPU가 없다는 이유로 이 모델을 아예 후보에서 빼는 사용자가 생긴다.
같은 기능을 문서로 안내하는 Stability AI의 SF3D와 대비되는 점이다.[^cmp-sf3d]
이 비대칭은 모델의 능력과 무관하게 정보가 어디에 있는지가 선택을 좌우한다는
뜻이고, 이 절의 정리가 쓸모 있는 이유이기도 하다.
반대로 공식이 CPU를 보증하지 않으므로, 버전이 바뀌어도 CPU 경로가 유지된다는
약속은 없다.
이 점은 2.1 저장소의 설치 안내가 `+cu124` PyTorch만 적는 것에서도
읽힌다.[^repo-21-readme]

## 체크리스트

- 사용하는 지역과 법인이 라이선스의 허용 지역에 들어가는지 확인했는가.
- 월간 활성 사용자가 100만을 넘는 서비스에 통합하려는가, 그렇다면 Tencent의 별도
허락을 받았는가.
- 필요한 것이 형태인지 텍스처인지, PBR이 필요한지 정했는가.
- 사용할 GPU의 VRAM이 선택한 버전의 요구량(2.0은 16GB, 2.1은 29GB)을 넘는가.
- CUDA 주 버전과 PyTorch 버전을 README의 시험 환경과 맞췄는가.
- 결과물을 게임이나 애니메이션에 쓴다면 리토폴로지와 리깅 후처리를 계획했는가.
- 결과물로 다른 AI 모델을 학습하지 않는가.
- 호스티드 서비스를 쓴다면 현재 무료 한도와 단가를 로그인 후 화면에서
확인했는가.
- 형태만 필요하다면 GPU 없이 CPU로 돌릴 수 있는지 `device='cpu'`, FP32, Turbo
단계 수, 해상도 256으로 먼저 시험했는가.
- CPU 시험에서 시간과 최대 메모리를 기록하고 입력 이미지의 배경을 미리 지웠는가.
- 결과 메시에서 면적 0인 면과 떨어진 조각, 닫힘 여부를 검사했는가.
- 한국에서 쓸 계획이라면 지역 제한이 없는 모델(MIT나 Apache-2.0)과 견주어
보았는가.

## 기억할 원칙

### 모델을 고르기 전에 허용 범위를 먼저 읽는다

성능표와 설치 안내가 눈에 먼저 들어오지만 사용할 수 있는지를 정하는 것은
라이선스다.
같은 계열의 모델이라도 버전마다, 저장소마다 조건이 다르고 어떤 저장소는
라이선스가 표시되어 있지 않다.
받기 전에 허용 지역과 사용자 규모 조건과 결과물 조항을 읽는 습관이 가장 싸게
사고를 막는다.

### 형태와 텍스처를 분리하는 설계는 실무의 선택지를 늘린다

두 단계가 따로 돌기 때문에 형태만 가볍게 만들고, 텍스처는 이미 있는 메시에 얹고,
후처리를 끼워 넣을 수 있다.
같은 이유로 큰 GPU가 없는 사용자도 형태 단계만으로 쓸 만한 시작점을 얻는다.
이 구조를 이해하면 한 번에 모든 것을 해결하려 하지 않고 단계별 도구를 조합하는
쪽이 현실적이라는 점이 보인다.

### 형태까지만 필요한지 먼저 정하면 GPU 없이도 길이 있다

텍스처와 PBR이 필요하면 CUDA 장비를 전제하는 공식 경로를 따라야 한다.
형태만 필요하면 CPU에서도 노트북급 장비로 몇 분 안에 결과가 나온 기록이 있고,
사용자의 경험도 그렇다.
무엇이 필요한지를 먼저 정하면 장비 걱정의 상당 부분이 줄어든다.
이 구분은 형태와 텍스처를 분리한 설계에서 나온다.

### 이 글을 읽는 방법

이 문서는 두 저장소의 README와 라이선스 본문, 논문 초록, Tencent의 발표문과
Tencent Cloud 청구 문서, 파생 저장소의 README를 읽고 정리했다.
2026년 10월 27일에 보강하면서 2.0과 2.1 저장소의 코드(`pipelines.py`,
`postprocessors.py`, `gradio_app.py`, `utils.py`, 표면 추출기)와 2.1의 API
문서와 Docker 안내, 라이선스 본문과 Notice, 허깅페이스 파일 목록, 공식 이슈,
CPU와 비CUDA 장치를 다룬 커뮤니티 저장소 다섯 곳의 README, 비교 대상 모델 아홉
곳의 README를 더 읽었다.
직접 실행한 것은 합성 도형으로 만든 후처리 스크립트 하나이고, Hunyuan3D의
가중치는 내려받지 않았으며 모델을 CPU든 GPU든 돌려 보지 못했다.
호스티드 서비스는 로그인이 필요해 화면 안쪽을 보지 못했다.
논문 본문(2.0, 2.1, 2.5)은 초록만 읽었다.
판단을 가를 관찰은 넷이다.
하나는 같은 이미지를 2.0, 2.1, 호스티드 3.1로 만들어 형태와 텍스처 품질과 위상을
견주는 것이다.
다른 하나는 호스티드 서비스 약관이 한국 사용자에게 지역 제한을 어떻게
적용하는지다.
셋째는 3.x의 가중치가 공개되는지, 공개된다면 어떤 라이선스인지다.
넷째는 이 문서를 쓰는 사람의 CPU 경험을 같은 입력으로 시간과 메모리를 재서
남기는 것이다.
이 문서는 넷 모두 확인하지 못했다.

---

[^billing]: Tencent Cloud, [Tencent HY 3D Global Billing Overview](https://www.tencentcloud.com/document/product/1284/75281), 2026-05-08

[^tencent-press]: Tencent, [Tencent Announces Global Launch of Hunyuan 3D Engine to Empower Creators with Advanced Creation Tools](https://www.tencent.com/en-us/articles/2202235.html), 2025-11-26

[^arxiv-1]: arXiv, [Hunyuan3D 1.0: A Unified Framework for Text-to-3D and Image-to-3D Generation](https://arxiv.org/abs/2411.02293), 2024-11-04

[^arxiv-2]: arXiv, [Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation](https://arxiv.org/abs/2501.12202), 2025-01-21

[^arxiv-21]: arXiv, [Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material](https://arxiv.org/abs/2506.15442), 2025-06-18

[^arxiv-25]: arXiv, [Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details](https://arxiv.org/abs/2506.16504), 2025-06-19

[^arxiv-omni]: arXiv, [Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets](https://arxiv.org/abs/2509.21245), 2025-09-25

[^arxiv-buffalo]: arXiv, [Hunyuan3D-Buffalo 1.0: A Unified Multimodal Model for Scalable 3D Generation, Understanding, and Editing](https://arxiv.org/abs/2608.02711), 2026-08-03

[^arxiv-worldclaw]: arXiv, [WorldClaw: Agentic 3D Open-World Generation at Scale](https://arxiv.org/abs/2608.05248), 2026-08-05

[^part]: GitHub, [Hunyuan3D Part](https://github.com/Tencent-Hunyuan/Hunyuan3D-Part)

[^repo-omni]: GitHub, [Hunyuan3D-Omni](https://github.com/Tencent-Hunyuan/Hunyuan3D-Omni)

[^repo-bench]: GitHub, [HY3D-Bench](https://github.com/Tencent-Hunyuan/HY3D-Bench)

[^license-21]: GitHub, [Tencent Hunyuan 3D 2.1 Community License Agreement](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE), 2025-06-13

[^license-2]: GitHub, [Tencent Hunyuan 3D 2.0 Community License Agreement](https://github.com/Tencent/Hunyuan3D-2/blob/main/LICENSE), 2025-01-21

[^pella]: <https://news.ycombinator.com/item?id=42786403>

[^EMIRELADERO]: <https://news.ycombinator.com/item?id=42786487>

[^swframe2]: <https://news.ycombinator.com/item?id=42789352>

[^godelski]: <https://news.ycombinator.com/item?id=42786749>

[^Kelvin506]: <https://news.ycombinator.com/item?id=42787039>

[^BigJono]: <https://news.ycombinator.com/item?id=42788216>

[^sorenjan]: <https://news.ycombinator.com/item?id=42786791>

[^fancyfredbot]: <https://news.ycombinator.com/item?id=43420827>

[^llm_nerd]: <https://news.ycombinator.com/item?id=43422513>

[^llm_nerd-3060]: <https://news.ycombinator.com/item?id=43422912>

[^deterministic]: <https://news.ycombinator.com/item?id=49295078>

[^steinhafen]: <https://news.ycombinator.com/item?id=42791031>

[^avaer]: <https://news.ycombinator.com/item?id=49265585>

[^tjohns]: <https://news.ycombinator.com/item?id=49265632>

[^sebzim4500]: <https://news.ycombinator.com/item?id=42786451>

[^GrantMoyer]: <https://news.ycombinator.com/item?id=42786723>

[^wumeow]: <https://news.ycombinator.com/item?id=42786748>

[^TinkersW]: <https://news.ycombinator.com/item?id=42791057>

[^gruez]: <https://news.ycombinator.com/item?id=42786434>

[^thot_experiment]: <https://news.ycombinator.com/item?id=43420250>

[^org-api]: GitHub, [Tencent-Hunyuan](https://github.com/Tencent-Hunyuan)

[^hf-2]: Hugging Face, [tencent/Hunyuan3D-2](https://huggingface.co/tencent/Hunyuan3D-2)

[^hf-21]: Hugging Face, [tencent/Hunyuan3D-2.1](https://huggingface.co/tencent/Hunyuan3D-2.1)

[^hf-2mini]: Hugging Face, [tencent/Hunyuan3D-2mini](https://huggingface.co/tencent/Hunyuan3D-2mini)

[^hf-2mv]: Hugging Face, [tencent/Hunyuan3D-2mv](https://huggingface.co/tencent/Hunyuan3D-2mv)

[^hf-trellis]: Hugging Face, [microsoft/TRELLIS-image-large](https://huggingface.co/microsoft/TRELLIS-image-large)

[^hf-trellis2]: Hugging Face, [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B)

[^hf-sf3d]: Hugging Face, [stabilityai/stable-fast-3d](https://huggingface.co/stabilityai/stable-fast-3d)

[^hf-spar3d]: Hugging Face, [stabilityai/stable-point-aware-3d](https://huggingface.co/stabilityai/stable-point-aware-3d)

[^hf-sam3d]: Hugging Face, [facebook/sam-3d-objects](https://huggingface.co/facebook/sam-3d-objects)

[^code-pipelines]: GitHub, [Hunyuan3D-2/hy3dgen/shapegen/pipelines.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/shapegen/pipelines.py)

[^code-post]: GitHub, [Hunyuan3D-2/hy3dgen/shapegen/postprocessors.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/shapegen/postprocessors.py)

[^code-gradio]: GitHub, [Hunyuan3D-2/gradio_app.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/gradio_app.py)

[^code-tex]: GitHub, [Hunyuan3D-2/hy3dgen/texgen/pipelines.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/texgen/pipelines.py)

[^code-surface]: GitHub, [Hunyuan3D-2/hy3dgen/shapegen/models/autoencoders/surface_extractors.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/shapegen/models/autoencoders/surface_extractors.py)

[^code-vae]: GitHub, [Hunyuan3D-2/hy3dgen/shapegen/models/autoencoders/model.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/shapegen/models/autoencoders/model.py)

[^code-utils]: GitHub, [Hunyuan3D-2/hy3dgen/shapegen/utils.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/shapegen/utils.py)

[^code-minimal]: GitHub, [Hunyuan3D-2/minimal_demo.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/minimal_demo.py)

[^code-21-minimal]: GitHub, [Hunyuan3D-2.1/hy3dshape/minimal_demo.py](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/hy3dshape/minimal_demo.py)

[^repo-2-readme]: GitHub, [Hunyuan3D-2 README](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/README.md)

[^repo-21-readme]: GitHub, [Hunyuan3D-2.1 README](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/README.md)

[^doc-21-api]: GitHub, [Hunyuan3D-2.1/API_DOCUMENTATION.md](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/API_DOCUMENTATION.md)

[^doc-21-docker]: GitHub, [Hunyuan3D-2.1/docker/README.md](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/docker/README.md)

[^notice-21]: GitHub, [Hunyuan3D-2.1/Notice.txt](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/Notice.txt)

[^issue53-yan]: GitHub, [Which steps to ignore for shape generation only? · Issue #53](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/53#issuecomment-2621745309), 2025-01-29

[^issue53-cpu]: GitHub, [Which steps to ignore for shape generation only? · Issue #53](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/53#issuecomment-2629503788), 2025-02-02

[^issue53-rocm]: GitHub, [Which steps to ignore for shape generation only? · Issue #53](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/53#issuecomment-2661008929), 2025-02-15

[^issue123]: GitHub, [Mac osx support · Issue #123](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/123#issuecomment-2716882414), 2025-03-12

[^issue244]: GitHub, [Device error using low_vram_mode on gradio app · Issue #244](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/244), 2025-05-15

[^issue49]: GitHub, [custom_rasterizer python setup.py install fail · Issue #49](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/49), 2025-01-27

[^gc-cpu]: GitHub, [Hunyuan3D-2mv Turbo: prueba real en CPU](https://github.com/GCaggianese/local-multipart-3d/blob/main/HUNYUAN_VALIDATION.md), 2026-10-03

[^mac-rocm]: GitHub, [Hunyuan3D 2.1 without CUDA — Apple Silicon (MPS) and AMD (ROCm)](https://github.com/VladimirTalyzin/hunyuan3d-2.1-mac-rocm)

[^m3dium]: GitHub, [m3dium (Apple Silicon)](https://github.com/anton-vsh/m3dium)

[^wth]: GitHub, [AI 文创手办 3D 生成与打印系统](https://github.com/WTHTech/hy3dgen-8g-laptop)

[^c-3dpack]: GitHub, [ComfyUI-3D-Pack](https://github.com/MrForExample/ComfyUI-3D-Pack)

[^c-kijai]: GitHub, [ComfyUI-Hunyuan3DWrapper](https://github.com/kijai/ComfyUI-Hunyuan3DWrapper)

[^c-visualbruno]: GitHub, [ComfyUI-Hunyuan3d-2-1](https://github.com/visualbruno/ComfyUI-Hunyuan3d-2-1)

[^c-winport]: GitHub, [Hunyuan3D-2-WinPortable](https://github.com/YanWenKun/Hunyuan3D-2-WinPortable)

[^c-sdbds]: GitHub, [Hunyuan3D-2-for-windows](https://github.com/sdbds/Hunyuan3D-2-for-windows)

[^c-2gp]: GitHub, [Hunyuan3D-2GP: 3D Generation for the GPU Poor](https://github.com/deepbeepmeep/Hunyuan3D-2GP)

[^c-unity]: GitHub, [Hunyuan3D-2.1-Unity-XR-PC-Phone](https://github.com/VR-Jobs/Hunyuan3D-2.1-Unity-XR-PC-Phone)

[^cmp-trellis]: GitHub, [microsoft/TRELLIS](https://github.com/microsoft/TRELLIS)

[^cmp-trellis2]: GitHub, [microsoft/TRELLIS.2](https://github.com/microsoft/TRELLIS.2)

[^cmp-triposg]: GitHub, [VAST-AI-Research/TripoSG](https://github.com/VAST-AI-Research/TripoSG)

[^cmp-triposr]: GitHub, [VAST-AI-Research/TripoSR](https://github.com/VAST-AI-Research/TripoSR)

[^cmp-sf3d]: GitHub, [Stability-AI/stable-fast-3d](https://github.com/Stability-AI/stable-fast-3d)

[^cmp-spar3d]: GitHub, [Stability-AI/stable-point-aware-3d](https://github.com/Stability-AI/stable-point-aware-3d)

[^cmp-step1x]: GitHub, [stepfun-ai/Step1X-3D](https://github.com/stepfun-ai/Step1X-3D)

[^cmp-instant]: GitHub, [TencentARC/InstantMesh](https://github.com/TencentARC/InstantMesh)

[^cmp-sam3d]: GitHub, [facebookresearch/sam-3d-objects](https://github.com/facebookresearch/sam-3d-objects)

[^replicate]: Replicate, [tencent/hunyuan3d-2](https://replicate.com/tencent/hunyuan3d-2)

[^fal21]: fal.ai, [fal-ai/hunyuan3d-v21](https://fal.ai/models/fal-ai/hunyuan3d-v21)

[^gn-a13b]: GeekNews, [텐센트 훈위안, 첫 하이브리드 AI 모델 오픈소스화. 유럽 연합(EU), 영국(UK), 그리고 대한민국에서는 사용할 수 없습니다.](https://news.hada.io/topic?id=21685), 2025-06-28

[^fortune]: <https://news.hada.io/topic?id=21685#cid40705>

[^manjunaths]: <https://news.ycombinator.com/item?id=43432463>

[^MITSardine]: <https://news.ycombinator.com/item?id=43422177>

[^kilpikaarna]: <https://news.ycombinator.com/item?id=43446581>

[^llm_nerd-remesher]: <https://news.ycombinator.com/item?id=43453511>

[^sinzin91]: <https://news.ycombinator.com/item?id=43426707>

[^sruc]: <https://news.ycombinator.com/item?id=43420870>

[^johaugum]: <https://news.ycombinator.com/item?id=43421191>
