# HairDeck: 이미지 한 장에서 움직이는 스타일화 헤어 카드를 만드는 모델

<https://github.com/hyz317/HairDeck>

<https://huggingface.co/spaces/hyz317/HairDeck>

## 소개

HairDeck은 캐릭터 이미지 한 장에서 스타일화된 헤어 카드(hair card)와 그 카드를
흔드는 스프링 본(spring bone) 체인을 만드는 연구 코드다.
헤어 카드는 게임과 아바타에서 머리카락 한 다발을 리본 모양의 판 하나로
표현하는 방식이다.
README는 카드 하나를 토큰 하나로 다루고,
집합 확산 트랜스포머(set diffusion transformer)가 카드 전체를 한꺼번에
만든다고 설명한다.
결과는 GLB 메시로 내보내거나, 아바타에 붙여 VRM으로 내보낼 수 있다.

README가 꼽는 구성 요소는 세 가지다.
첫째, 카드 VAE가 카드 하나하나를 인코딩하고,
조건부 집합 확산이 헤어스타일 전체를 만든다.
둘째, 출력이 카드를 개별로 보존하고 카드마다 UV 좌표를 준다.
셋째, 체인 확산 모델이 카드를 움직이는 본을 만들고,
스키닝과 VRM 내보내기까지 이어진다.

저장소는 2026년 10월 29일에 만들어졌고 마지막 푸시는 2026년 10월 31일이다.
기록 시점에 스타는 517개, 포크는 31개였다.[^api]
코드와 체크포인트의 라이선스는 Apache-2.0이고,
서드파티 모델과 데이터는 각자의 라이선스를 따른다고 README는 적는다.

## 논문이 말하는 위치

arXiv 초록에 따르면 이전에 스타일화 헤어 카드를 만든 방법은 CHARM 하나였고,
CHARM은 헤어스타일을 제어점의 긴 순서열로 한 단계씩 쌓아 만든다.
저자들은 카드 헤어스타일이 순서 없는 집합이라는 점에서 출발해 카드를 한꺼번에
만든다고 밝힌다.
CHARM의 테스트 세트에서 Chamfer 거리를 44% 줄이고,
카드 방향 오차를 절반 넘게 줄이며, 33배 빠르다는 것이 저자들의 주장이다.[^arxiv]
이 수치는 저자들이 자기 방법을 자기가 고른 테스트 세트에서 잰 값이다.
이 문서는 논문 본문의 표를 열어 보지 않았고, 수치를 독립적으로 재현하지 않았다.

## 설치하기

README의 요구 조건은 Linux x86-64, Python 3.12, NVIDIA CUDA GPU 한 장이다.
PyTorch 2.8과 CUDA 12.8에서 시험했다고 하며,
비디오 미리보기에는 `ffmpeg`가 `PATH`에 있어야 한다.

```bash
git clone https://github.com/hyz317/HairDeck.git
cd HairDeck

python -m pip install -r requirements.txt
python -m pip install --no-deps pyrender==0.1.45  # without its old PyOpenGL pin
```

가중치는 Hugging Face의 `hyz317/HairDeck`에 있다.
SAM 3과 DINOv3는 접근 제한(gated) 모델이어서,
각 모델 페이지에서 라이선스에 동의하고 로그인해야 내려받을 수 있다.

```bash
hf auth login
export HAIRDECK_ROOT=/path/to/workspace
python scripts/setup/download_weights.py
```

내려받기 스크립트는 체크포인트, 전처리와 이미지 인코더 가중치, 보조 데이터,
VRM 애드온이 들어 있는 Blender 4.2 LTS를 설치한다.
기본 Blender 내려받기는 Linux x86-64용이고,
이미 있는 Blender 4.2 LTS를 쓰려면 `HAIRDECK_BLENDER`에 그 명령을 지정한다.
이 문서를 쓴 환경에는 CUDA GPU가 없어서 위 설치와 아래 실행 명령은 직접 돌려
보지 않았다.

## 실행하기

README의 빠른 시작은 이미지 한 장에서 변형 네 개를 만들고,
그중 0번을 VRM 아바타와 고개 돌리기 영상으로 내보내는 두 줄이다.

```bash
python scripts/image_to_hair.py character.png --out results/my_character --n 4
python -m hairdeck.vrm.export results/my_character/character 0
```

`--n`은 1에서 4까지의 변형 수이고, `--seed`는 첫 시드를 정한다.
`--no-chains`를 주면 카드만 만들고 스프링 본 체인은 만들지 않는다.
직접 학습한 모델을 쓰려면 `--ckpt`와 함께,
같은 카드 VAE로 학습한 `--chain_ckpt`를 넘겨야 한다.

결과는 `OUT/<이미지 이름>/`에 쓰인다.
시드 0의 주요 파일은 다음과 같다.

| 파일                    | 내용                              |
| ----------------------- | --------------------------------- |
| `cards_seed0.json`      | 헤어 카드 형상                    |
| `chains_seed0.json`     | 생성된 스프링 본 체인             |
| `hair_seed0.glb`        | 머리 대용물과 카드별 UV, 머리색   |
| `hair_seed0_nohead.glb` | 머리 대용물이 없는 헤어           |
| `info.json`             | 생성 설정과 결과 메타데이터       |
| `avatar_seed0.vrm`      | VRM 내보내기 명령이 만드는 아바타 |
| `turn_seed0.mp4`        | 고개 돌리기 미리보기 영상         |

`--no-chains`를 쓰면 체인 파일은 만들어지지 않는다.

## 호스티드 데모를 직접 써 본 기록

GPU가 없는 환경에서는 Hugging Face Space의 데모가 가장 빠른 확인
수단이다.
화면은 세 단계다.
01은 이미지 올리기와 예시 12장 고르기, 변형 수 1에서 4 고르기, 고급 설정,
`Generate hair` 버튼이다.
02는 3D 미리보기로, `Reference head`와 `Spring bones` 체크 상자가 있다.
03은 변형(시드)을 고르고 `Preview motion`이나 `Export VRM`을 누르는 단계이며,
오른쪽 `Downloads` 탭에서 GLB와 지오메트리 데이터를 내려받는다.
페이지는 선명한 인물 사진에 머리 모양이 전부 보여야 결과가 좋다고 안내한다.

이 문서를 쓰며 예시 이미지 하나를 골라 변형 1개로 생성해 봤다.
미리보기에 긴 머리 카드가 떴고, 상태줄은 `1 variation ready`와 `3.0
s`를 표시했다.
내려받기 목록에는 `hair_seed0.glb` 978.2 KB와 머리 대용물이 없는 `.glb` 857.2
KB가 보였다.
Space의 상단 표시는 `Running on ZERO`였다.
이 3.0초는 한 번의 실행에서 화면이 보여 준 값이며,
대기열 시간이 포함되었는지는 확인하지 못했다.
`Spring bones` 보기, `Preview motion`, `Export VRM`, 사진 입력,
변형 2개 이상은 시험하지 않았다.

## 평가와 학습

평가는 `scripts/test.py`로 한다.
점 구름 조건 테스트와 체인 테스트가 있고, 각 테스트가 시드 0, 1,
2를 뽑아 논문 지표를 출력하며 샘플별 결과와 평균을 `eval.json`에 저장한다고
README는 말한다.
학습은 CHARM 데이터셋과 캐릭터 VRM 파일에서 시작해 VAE, 점 구름 DiT, 이미지 DiT,
체인 DiT 순으로 `scripts/train/` 아래 런처를 돌린다.

README는 한계를 하나 밝힌다.
현재의 이미지 학습 레시피는 합성 외형 증강을 포함하는데,
공개된 이미지 모델에 쓰인 재스타일 렌더 풀(restyled-render pool)은 이 릴리스에
들어 있지 않다.

## 비평

### 공개된 학습 코드로는 공개된 이미지 모델이 재현되지 않는다

README 스스로 이미지 모델의 학습 데이터 일부가 빠져 있다고 적는다.
따라서 학습 런처를 그대로 돌려도 내려받은 이미지 체크포인트와 같은 모델이
나온다고 기대할 수 없다.
점 구름 조건 모델은 CHARM 데이터로 학습하므로 이 문제가 덜하지만,
논문의 핵심 주장인 한 장의 이미지에서 시작하는 경로는 체크포인트를 쓰는
사용으로 한정된다.

### 숫자는 한 팀의 첫 보고다

저장소는 만든 지 사흘이 안 되었고, 기록 시점의 커밋은 두 개였다.[^api]
44%, 절반, 33배라는 수치는 저자들이 초록에서 주장한 값이고,
이 문서가 확인한 독립 재현은 없다.
스타 517개는 관심의 크기이지 품질의 증거가 아니다.

### 하드웨어와 접근 조건이 사용자를 좁힌다

로컬 실행은 Linux x86-64와 NVIDIA GPU로 한정되고,
기본 Blender 내려받기도 Linux x86-64용이다.
SAM 3과 DINOv3는 계정 로그인과 라이선스 동의가 있어야 받을 수 있어서,
설치 스크립트가 무인으로 끝나지 않는다.
Mac이나 GPU가 없는 환경에서는 호스티드 데모가 유일한 길이지만,
데모가 올린 이미지를 어떻게 다루는지는 이 문서가 확인하지 못했다.

### 입력 범위는 데모 한 번으로 말할 수 없다

예시 이미지 12장 가운데 일러스트 외에 사진처럼 보이는 것도 있었지만,
이 문서는 사진 입력을 시험하지 않았다.
README가 대상으로 삼는 것은 스타일화된 캐릭터이고,
현실의 인물 사진에서 결과가 어떤지는 데모 안내문의 한 줄 외에 근거가 없다.

## 체크리스트

- [ ] GPU가 있다면 Linux x86-64, Python 3.12, CUDA 12.8에서 설치가 끝나는가
- [ ] SAM 3과 DINOv3의 라이선스에 동의하고 `hf auth login`을 마쳤는가
- [ ] `python scripts/setup/download_weights.py`가 오류 없이 끝나는가
- [ ] 대표 이미지 한 장으로 `scripts/image_to_hair.py`가 `hair_seed0.glb`를 만드는가
- [ ] 같은 이미지로 `--no-chains`를 줬을 때 체인 파일이 빠지는가
- [ ] VRM을 내보낸 뒤 쓰려는 엔진이나 뷰어에서 스프링 본이 실제로 움직이는가
- [ ] 직접 학습한다면 이미지 모델에 빠진 재스타일 렌더 풀의 영향을 알고 있는가
- [ ] 서드파티 모델과 CHARM 데이터의 라이선스가 쓰려는 용도에 맞는가

---

[^api]: GitHub, [REST API: hyz317/HairDeck](https://api.github.com/repos/hyz317/HairDeck)

[^arxiv]: arXiv, [HairDeck: Animation-Ready Stylized Hair Cards from a Single Image](https://arxiv.org/abs/2610.40599), 2026-10-29
