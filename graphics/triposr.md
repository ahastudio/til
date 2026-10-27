# TripoSR: 사진 한 장에서 3D 모델을 만드는 MIT 라이선스 오픈 모델

<https://github.com/VAST-AI-Research/TripoSR>

## 소개

TripoSR은 사진 한 장에서 3D 형상을 빠르게 복원하는 최신 오픈소스 모델의 공식
코드 저장소다.
Tripo AI와 Stability AI가 함께 개발했고, 큰 복원 모델(LRM)의 원리를 바탕으로
입력을 빠르게 처리해 고품질 3D 메시를 낸다고 README는 설명한다.
소스 코드와 사전 훈련된 모델과 온라인 데모가 모두 MIT 라이선스로 공개되어
연구자, 개발자, 창작자가 3D 생성 AI와 3D 콘텐츠 제작의 경계를 넓힐 수 있게 하는
것이 목표라고 한다.
저장소는 2024년 2월 7일에 만들어졌고, 2026년 10월 27일에 확인한 시점에 스타
7,233개, 포크 935개, 열린 이슈 109개였으며 마지막 푸시는 2026년 6월 4일이다.
저장소는 `run.py`, `gradio_app.py`, `requirements.txt`, `tsr` 패키지, 예제
이미지로 이루어져 있다.

이 모델은 상용 서비스 [Tripo](tripo.md)의 한 부분이 아니라 별도의 공개 모델이고,
크레딧 없이 로컬에서 돌릴 수 있다는 점이 가장 큰 쓰임이다.

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

## 실행하기

한 장의 이미지에서 3D 모델을 만드는 기본 명령이다.

```bash
python run.py examples/chair.png --output-dir output/
```

복원된 3D 모델이 `output/`에 저장되고, 이미지 경로를 공백으로 여러 개 줄 수
있다.
기본 설정은 이미지 한 장에 약 6GB의 VRAM이 든다고 한다.
정점 색 대신 텍스처를 출력하려면 `--bake-texture`를 쓰고
`--texture-resolution`으로 텍스처 해상도(픽셀)를 정한다.
자세한 옵션은 `python run.py --help`에 있고, 브라우저에서 쓰려면 로컬 Gradio
앱을 띄운다.

```bash
python gradio_app.py
```

## 값 정하기

| 항목           | 시작값                        | 근거                                                                             |
| -------------- | ----------------------------- | -------------------------------------------------------------------------------- |
| 입력           | 배경이 단순한 정면 사진 한 장 | 단일 이미지 복원이어서 가려진 면은 추정이다. 이는 이 문서의 해석이다             |
| VRAM           | 6GB 이상                      | README가 이미지 한 장의 기본 설정이 약 6GB라고 밝힌다                            |
| 출력 색        | 정점 색                       | 텍스처는 `--bake-texture`를 켜야 하며 해상도는 `--texture-resolution`으로 정한다 |
| CUDA와 PyTorch | 주 버전을 일치                | 불일치가 가장 흔한 설치 오류의 원인이라고 README가 안내한다                      |

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

## 트레이드오프

### 공짜의 대가는 설치와 하드웨어이고 기능은 서비스에 못 미친다

크레딧도 구독도 필요 없지만 CUDA 지원 GPU와 PyTorch와 컴파일 의존성을 직접
맞춰야 한다.
이 저장소는 단일 이미지 복원 하나를 제공하고, 상용 서비스가 주는 리깅, 스마트
분할, 8K 텍스처 같은 기능은 들어 있지 않다.
이는 이 문서가 두 곳의 설명을 비교한 해석이며 품질을 직접 비교해 보지는 않았다.

### 단일 이미지 입력은 보이지 않는 면을 추정한다

한 장에서 3D를 복원하는 방식은 뒷면 같은 보이지 않는 부분을 모델이 채운다.
정확한 형상이 필요한 제품이라면 다중 시점이나 실측이 필요하고, README는 이
한계를 따로 설명하지 않는다.

## 체크리스트

- Python 3.8 이상과 PyTorch를 설치했고 CUDA 주 버전이 일치하는가.
- `pip install -r requirements.txt`가 오류 없이 끝났는가.
- `python run.py examples/chair.png --output-dir output/`가 6GB 안팎의 VRAM에서
돌아가는가.
- 텍스처가 필요하면 `--bake-texture`와 `--texture-resolution`을 줬는가.
- `torchmcubes` CUDA 오류가 나면 지우고 다시 설치했는가.
- 결과물을 상업적으로 쓰기 전에 MIT 라이선스 고지를 지켰는가.

## 기억할 원칙

### 서비스가 막는 곳에서 오픈 모델이 길을 연다

크레딧과 상업 이용 제한이 있는 서비스의 무료 플랜이 아쉬울 때 같은 회사가 낸
공개 모델은 한도 없는 시험대가 된다.
다만 설치와 하드웨어라는 다른 비용을 치르고, 기능은 서비스가 앞선다는 점을
감안해 선택해야 한다.

### 이 글을 읽는 방법

이 문서는 저장소의 README와 파일 목록, GitHub의 저장소 정보를 읽고 정리했으며,
직접 설치해 실행하지는 못했다.
HN에서 이 저장소의 스레드는 찾지 못했고 Lobste.rs와 GeekNews에서도 찾지 못했다.
판단을 가를 관찰은 둘이다.
하나는 같은 이미지를 TripoSR과 유료 서비스로 만들었을 때의 품질 차이다.
다른 하나는 6GB VRAM에서의 실제 생성 시간이다.
둘 다 이 문서가 확인하지 못했다.
