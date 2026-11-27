# UniRig: 3D 모델 자동 리깅

<https://zjp-shadow.github.io/works/UniRig/>

<https://github.com/VAST-AI-Research/UniRig>

## 소개

UniRig는 3D 메시를 받아 뼈대(skeleton)를 예측하고
각 정점이 뼈대에 영향받는 정도인 스키닝 가중치(skinning weight)까지 예측하는
자동 리깅(rigging) 모델이다.
SIGGRAPH 2025(ACM Transactions on Graphics)에 실린 논문의 공식 구현으로,
칭화대학교와 Tripo(VAST)가 만들었다고 README는 밝힌다.
라이선스는 MIT이고 언어는 Python이다.

프로젝트 사이트는 저장소의 `homepage` 필드가 가리키는 주소다.
읽은 시점(2026년 11월 27일)에 본문을 끝까지 읽었다.
논문 초록, 파이프라인 그림 설명, 검증 데이터 결과 영상으로 구성되어 있고,
저자는 Jia-Peng Zhang 외 4명이다.
사이트의 수치는 논문 저자들의 주장이다.

GitHub API가 보고한 저장소의 현황은 다음과 같다.

| 항목        | 값                          |
| ----------- | --------------------------- |
| 생성        | 2025년 4월 8일              |
| 마지막 푸시 | 2026년 6월 4일(README 수정) |
| 스타        | 2,393                       |
| 포크        | 230                         |
| 열린 이슈   | 27(풀 리퀘스트 포함 집계)   |
| 커밋        | 35                          |
| 기여자      | 5명                         |

README 맨 위에는 후속 연구 SkinTokens로 안내하는 공지가 있다.
이 문서는 UniRig 저장소만 다룬다.

## 구조

UniRig는 두 단계로 나뉜다.

첫 단계는 뼈대 예측이다.
메시에서 뽑은 점군을 Shape Encoder에 넣고,
GPT와 비슷한 트랜스포머가 뼈대 트리를 토큰열로 한 토큰씩 생성한다.
이때 쓰는 표현이 논문이 제안한 Skeleton Tree Tokenization이고,
토큰열은 계층 구조가 있는 뼈대로 되돌려진다.

둘째 단계는 스키닝 예측이다.
Point-wise Encoder가 점군의 특징을, Bone Encoder가 뼈대 트리의 특징을
뽑고, Bone-Point Cross Attention으로 이 둘을 합쳐 정점별 가중치와
뼈 속성을 예측한다.

README가 밝히는 공개 범위는 다음과 같다.
뼈대 예측과 스키닝 예측 코드, 학습 코드, 체크포인트, Rig-XL과 VRoid 데이터는
공개되었다.
뼈 속성(예: 물리 보조 움직임을 위한 강성) 예측은 “곧 공개”로 적혀 있다.
논문의 주요 결과를 재현하는 체크포인트는 “공개 예정”이다.

## 사용법

필요한 환경은 Python 3.11, PyTorch 2.3.1 이상, `spconv`,
`torch_scatter`, `torch_cluster`이고 `numpy`는 1.26.4로 고정하라고 한다.
`flash_attn` 설치에서 오류가 날 가능성이 높다고 README가 미리 알린다.
추론에는 VRAM 8GB 이상의 CUDA GPU가 필요하다.

```bash
# 1. 뼈대 예측
bash launch/inference/generate_skeleton.sh \
  --input examples/giraffe.glb --output results/giraffe_skeleton.fbx

# 2. 스키닝 예측(뼈대를 다듬은 파일을 입력으로 권장)
bash launch/inference/generate_skin.sh \
  --input examples/skeleton/giraffe.fbx --output results/giraffe_skin.fbx

# 3. 원본 메시와 합치기
bash launch/inference/merge.sh \
  --source results/giraffe_skin.fbx --target examples/giraffe.glb \
  --output results/giraffe_rigged.glb
```

입력 형식은 `.obj`, `.fbx`, `.glb`, `.vrm`이다.
`--seed`를 바꾸면 다른 뼈대 변형을 얻는다.
뼈대 파일을 합치면 스키닝이 없는 결과가 나오므로
최종 결합에는 스키닝 결과 파일을 써야 한다.
`.vrm` 입출력에는 Blender 애드온을 따로 설치한다.

학습은 RigNet 설정으로 재현할 수 있다.
README에 따르면 뼈대 모델은 RTX 4090 4장으로 약 18시간 뒤 120 에포크 근처에서
가장 좋은 결과가 나오고, 스키닝 모델은 GPU 한 장에서 60GB 이상의 메모리를
쓴다.
README는 학습 코드가 “조금 지저분할 수 있다”고 스스로 적는다.

## 분석

### 뼈대와 스키닝을 분리한 두 단계 구조

뼈대는 이산적인 트리이고 가중치는 정점마다 이어지는 값이다.
UniRig는 앞의 것을 토큰 생성 문제로, 뒤의 것을 뼈와 점 사이의 어텐션 문제로
따로 푼다.
분리의 대가는 오류가 전파된다는 점이다.
README도 꼬리나 날개 뼈가 빠진 뼈대를 쓰면 스키닝 결과가 크게 나빠질 수 있어
뼈대를 먼저 다듬으라고 권한다.
사람이 개입하는 지점을 설계에 넣은 셈이다.

### 후속작이 같은 분리를 없앤다

README 상단의 공지는 SkinTokens가 두 단계를 하나의 자기회귀 열로 합친다고
설명한다.[^st]
제작자는 스키닝 정확도가 98~133%, 뼈 예측이 17~22% 좋아졌다고 말한다.
이 수치는 제작자의 보고이고 이 문서는 SkinTokens를 실행하지 않았다.
UniRig 저장소의 최근 커밋 세 개는 인용 수정(2026년 1월 6일),
SkinTokens 공지(4월 22일), README 수정(6월 4일)이다.

### 규모의 근거는 데이터셋이다

논문은 Rig-XL이라는 14,000개 이상의 리깅된 모델 데이터셋을 함께 낸다.
Rig-XL 모델은 VRoid를 빼면 모두 Objaverse-XL에서 골랐다고 README가 밝힌다.
결과의 폭(동물, 인물, 가상 캐릭터)은 모델 구조만이 아니라 이 데이터의
범주 분포에서 온다.

## 비평

### 공개된 체크포인트는 논문의 학습 데이터와 다르다

논문 초록은 Rig-XL로 학습했다고 쓰지만,
README는 현재 공개된 체크포인트가 Articulation-XL2.0으로 학습한 것이라고 적는다.
Rig-XL과 VRoid로 학습한 체크포인트는 계속 “공개 예정”이다.
2025년 6월에 이 가중치가 언제 나오는지 묻는 이슈가 열렸고,[^i45]
2026년 2월에는 공개된 체크포인트가 Rig-XL이 아닌 데이터로 학습되었다는 점을
지적하는 이슈가 열렸다.[^i68]
따라서 논문의 215%, 194% 개선 수치가 공개 체크포인트에도 그대로 적용되는지는
이 문서가 확인하지 못했다.

### 수치의 기준이 초록에는 없다

초록은 “도전적인 데이터셋에서” 리깅 정확도 215%, 모션 정확도 194% 개선을
말한다.
어떤 기준 모델과 어떤 지표(개선의 분모)인지는 초록과 README에 없고,
이 문서는 논문 본문을 열어 보지 않았다.
상대 개선율은 기준값이 낮으면 크게 나오므로, 절대 오차를 본문에서 확인해야
한다.

### 실제 사용에서 막히는 지점이 이슈에 남아 있다

열린 이슈에는 예제 파일에 스키닝이 없어 뼈대 예제를 재현하지 못한다는 글,[^i66]
스키닝 결과가 이상하다는 글, CUDA 12.8 이후 버전에서 `spconv`를 쓸 수 없느냐는
글, RTX 5090(Blackwell) 지원 요청이 있다.
`spconv`, `torch_scatter`, `flash_attn` 같은 의존성은
GPU와 CUDA 조합에 민감하다.
설치에 시간이 들 수 있다는 점은 README도 인정한다.

### 유지 속도가 느리다

기여자가 5명이고 커밋이 35개이며, 최근 커밋 세 개에는 코드 변경이 보이지 않는다.
열린 이슈 27개 중 일부는 2025년 여름부터 열려 있다.
연구 코드 공개로서는 흔한 모습이지만, 제작 파이프라인에 넣을 때는
스스로 고쳐 쓸 각오가 필요하다.

## 인사이트

### 자동 리깅은 “초안 만들기”로 쓰는 편이 맞다

README가 뼈대를 먼저 손보고 스키닝을 돌리라고 권하는 것은
자동 결과를 최종물이 아니라 초안으로 보라는 뜻이다.
애니메이터가 처음부터 뼈대를 만드는 시간을 줄이는 용도로는 쓸 수 있다.
다만 초안의 품질이 모델 종류에 따라 얼마나 다른지는 모델을 직접 돌려 봐야
안다.
[Tripo](tripo.md)나 [TripoSR](triposr.md)처럼 생성한 모델에 뼈대를 붙이는
용도가 같은 조직이 노리는 흐름으로 보이지만, 저장소 문서가 그렇게 말하지는
않는다.

### 연구 코드의 공개 순서가 사용자 기대를 만든다

코드와 일부 체크포인트를 먼저 내고 논문 재현 체크포인트를 나중으로 미루는
방식은 연구실에서 흔하다.
그 사이 사용자는 논문의 수치를 공개 체크포인트의 성능으로 기대하게 된다.
이슈 두 건이 이 간극에서 나왔다.
공개 순서와 공개 범위를 README 첫머리에 적어 둔 점은 이 간극을 줄인다.

### 확인할 것

논문 본문의 비교 대상과 절대 지표, 공개 체크포인트의 실제 품질은
직접 돌려 봐야 알 수 있다.
이 문서는 설치, 추론 실행, 논문 본문 열람, SkinTokens 실행을 하지 않았다.
Rig-XL 계열 체크포인트가 공개되었는지는 저장소의 다음 업데이트로 확인한다.

---

[^st]: GitHub, [VAST-AI-Research/SkinTokens](https://github.com/VAST-AI-Research/SkinTokens), 2026-11-27

[^i45]: GitHub, [Great work! May I ask when the pretrained weights based on Rig-XL/VRoid will be released?](https://github.com/VAST-AI-Research/UniRig/issues/45), 2025-06-30

[^i68]: GitHub, [The released checkpoints only trained on Seed3D/Articulation-XL2.0 dataset, Not the Rig-XL](https://github.com/VAST-AI-Research/UniRig/issues/68), 2026-02-06

[^i66]: GitHub, [Example Files Lack Skinning, Cannot Replicate Skeletal Examples](https://github.com/VAST-AI-Research/UniRig/issues/66), 2026-01-11
