# Laya-CoreML: Apple Silicon의 Neural Engine에서 오프라인으로 판단하는 Laya

<https://gist.github.com/fordnox/e592d0f68b543fd044be8e6d040863a0>

<https://github.com/mizorewww/laya-coreml>

HN 토론: <https://news.ycombinator.com/item?id=49777106> (178점, 34개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49805823> (2점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=34033>

## 소개

Laya-CoreML은 Laya 모델을 Apple의 Core ML로 옮긴 오픈소스 이식판이다.
Laya는 문장을 한 토큰씩 생성하는 대신 선택지별 확률, 순서형 점수,
참일 확률을 돌려주는 판단용 모델이다.
이 저장소는 Apache-2.0 라이선스이며 Apple Silicon의 Core ML과 Neural
Engine(ANE)에서 생성 토큰 없이 실행하는 것을 목표로 한다.
모델은 한 번 내려받으면 이후에는 네트워크 없이 판단한다.
Laya 자체는 이 저장소의 `jev/laya.md`에, Jev 같은 판단 모델의 개념은
`jev/jev.md`에 정리되어 있다.

이 문서가 다루는 대상은 두 가지다.
하나는 fordnox가 올린 Gist이고,
다른 하나는 그 Gist가 실행하는 `laya-coreml` 저장소다.
Gist는 여섯 줄의 셸 명령이 전부이며 성능 수치는 들어 있지 않다.
성능과 한계에 관한 내용은 모두 저장소 README에서 가져왔다.
나는 이 도구를 직접 실행하지 않았고, 아래 수치는 README가 주장하는 값이다.

## 실행하기

요구 사항은 Apple Silicon, macOS 15 이상, Python 3.11에서 3.13이다.
Gist의 여섯 명령은 다음과 같고, `uv`로 프로젝트를 만들어 데모를 설치한다.

```bash
mkdir test-laya
cd test-laya
uv init
uv add 'laya-coreml[demo]'
hf download aac6fef/laya-multilingual-coreml-ane --local-dir models/snake
uv run laya-coreml-snake --model models/snake
```

데모는 로컬 Laya 모델이 뱀 게임을 하는 화면이다.
화면에 선택 확률, 점수, 길이, 지연 시간,
안전장치 개입이 보이고 터미널은 104열에 35행이 필요하다.
스페이스는 일시 정지, 위아래 화살표는 속도, `R`은 재시작, `Q`는 종료다.
처음 Core ML을 초기화할 때는 수십 초가 걸릴 수 있다고 README가 안내한다.

### 파이썬에서 판단 요청하기

README의 API 예시는 이렇다.
`noul`은 참과 거짓을 묻는 불리언 질문 유형이다.

```python
import laya_coreml as laya

agent = laya.load("aac6fef/laya-multilingual-coreml-ane")
result = agent.predict(
    "The customer requests a refund of a duplicate payment.",
    {
        "refund": {
            "type": "noul",
            "instructions": "Does the customer request a refund?",
        }
    },
)
print(result["answers"]["refund"])
```

질문 유형은 선택(choice), 순서형 점수(score), 불리언(noul)의 세 가지다.
자기회귀 디코딩이나 파싱할 JSON이 없고,
허브에서 내려받은 모델은 이후 예측을 로컬에서 처리한다.
`local_files_only=True`를 주면 이미 있는 캐시만 쓰도록 강제할 수 있다.

## 값 정하기

저장소가 제공하는 체크포인트는 용도에 따라 나뉜다.

| 번들                 | 기본 엔진 | 용량      | 용도                                    |
| -------------------- | --------- | --------- | --------------------------------------- |
| Laya 421M            | CPU+GPU   | 512 토큰  | 원본 영어 모델                          |
| Multilingual 322M    | CPU+GPU   | 1024 토큰 | 범용 다국어 판단                        |
| Typed Decisions 421M | CPU+GPU   | 1024 토큰 | 원본 특화 체크포인트                    |
| Snake GPU            | CPU+GPU   | B3 / L64  | 게임의 간결한 질문 세 개를 한 번에 처리 |
| Multilingual ANE     | CPU+ANE   | B1 / L96  | 짧은 판단, FP16                         |
| Multilingual ANE W8  | CPU+ANE   | B1 / L96  | 선택 사항인 근사 팔레트 압축            |

선택 기준은 질문의 길이다.
ANE 번들은 질문, 선택지, 상태를 합쳐 96토큰까지만 받고, 넘으면 용량 오류가 난다.
그보다 긴 요청에는 1024토큰의 범용 다국어
모델(`aac6fef/laya-multilingual-coreml`)을 쓰라고 README가 안내한다.

## 성능 주장과 그 조건

README가 보고하는 측정은 M3 Max에서 나왔다.
질문 한 개는 91토큰이고 96으로 채워 넣었으며, 프롬프트 준비부터 토크나이징,
추론, 보정, 포맷까지 포함하고 로딩과 워밍업은 제외했다.
구현마다 20초 블록 여섯 개를 번갈아 돌려 안정적인 호출 65,598건을 얻었다고 한다.

| 지표                  | 컴파일된 MLX FP16 | Core ML ANE FP16 | Core ML ANE W8 |
| --------------------- | ----------------- | ---------------- | -------------- |
| P50 / P95             | 6.94 / 7.39 ms    | 4.98 / 5.31 ms   | 4.88 / 5.23 ms |
| 시스템 전력 평균 추정 | 61.39 W           | 30.75 W          | 27.39 W        |
| 판단당 시스템 에너지  | 0.4288 J          | 0.1540 J         | 0.1344 J       |
| 속도 향상             | 1배               | 1.39배           | 1.42배         |
| 에너지 향상           | 1배               | 2.78배           | 3.19배         |

전체 게임 루프는 세 번의 600단계 에피소드에서 초당 49.1에서 50.0회 판단을
유지했고 사망은 없었으며 안전장치가 두 번 개입했다.
이 수치는 렌더링 직렬화를 포함하고 터미널 그리기는 제외한 값이다.
GN 요약은 Hacker News 제목의 초당 45회 판단과 Gist 본문이 서로 맞지 않고,
Gist에는 측정 코드가 없다고 지적한다.

README 스스로 한계도 적는다.
- 이 수치는 질문 하나의 결과이고 게임 한 프레임의 시간이 아니다.
- 에너지는 SMC 센서 값에서 추정한 것이어서 센서와 배경 부하의 불확실성이 있다.
- 요청했던 10배 향상은 달성하지 못했다.
- 1024토큰짜리 ANE 그래프는 실제 요청에 약 91.7ms가 걸려서 짧은 질문의 우위가 긴 문맥으로 이어지지 않는다.
- 변환 충실도 검사는 189개 검증 질문에서 선택된 답이 원본과 일치하는 것을 확인한 것이며 일반 과업 정확도의 증거가 아니다.

## 함정

### 보정 온도의 제한

README는 업스트림 v0.3.5를 따라 보정 온도를 0.5에서 5.0 사이로
제한한다고 설명한다.
기본 체크포인트의 `choice:11+` 구간 값이 0.1006이어서 그대로 쓰면 로짓이 약 10배
뾰족해져서 동전 던지기 수준의 불확실성이 거의 확실한 것처럼 보고된다는 이유다.
제한된 구간은 로드할 때 `RuntimeWarning`으로 알려 준다.
확률이 확신처럼 보일 수 있다는 점은 `jev/laya-confidence.md`가
다루는 문제와도 이어진다.
`answer_confidence`와 `confidence` 필드가 보정 정확도를 보증하지 않는다는
문장도 README에 있다.

### 데모의 성능은 모델만의 결과가 아니다

GN 요약에 따르면 데모는 경로 계획 정보와 충돌 방지 안전장치를 함께 쓴다.
README도 게임이 명시적인 플래너 특징과 눈에 보이는 순환 안전층을 쓴다고 적는다.
뱀 게임 점수는 모델과 이 보조 장치를 합한 결과이고,
모델이 게임을 풀었다는 뜻이 아니다.
HN에서 putna는 이 데모가 로컬에서 돌리는 방법을 보여 주는 예제일 뿐이고 뱀
게임용으로 따로 미세 조정한 것이 아니라고 답했다.[^putna-demo]

### 초기화 시간과 메모리

처음 실행하면 Core ML 초기화에 수십 초가 걸릴 수 있다.
HN의 putna는 M3 Max에서 물리 메모리 사용량이 560.4MB,
최대 778.0MB였다고 알렸다.[^putna-memory]
모델이 약 3억 매개변수 규모라서 128GB 통합 메모리에 비해 매우 작다.

## 확인하기

내 기기에서 직접 확인하려면 아래 순서로 한다.

1. 위 여섯 명령으로 데모를 돌리고 화면의 지연 시간 표시를 읽는다.
2. 파이썬 예시를 짧은 문장과 긴 문장으로 각각 호출해 지연 시간을 재고, ANE 번들이 96토큰을 넘을 때 오류가 나는지 확인한다.
3. 자기 작업의 질문 열 개쯤을 정답이 있는 예제로 만들어 확률이 얼마나 맞는지 본다.
4. 활동 모니터나 전력 측정 도구로 Neural Engine 사용을 확인한다. HN의 speedping은 에너지 모니터 도구 pumas를 켜 보니 GPU가 아니라 거의 전부 Neural Engine에서 돈다고 밝혔다.[^speedping]

## 쓰임새와 한계에 대한 논의

HN의 imranq는 제한적으로 살펴본 결과 Laya를 훈련 데이터가 있는 더 결정적인
작업에 쓰는 편이 맞고 제로샷에서는 Jev만큼 잘하지 못할 것이라고 썼다.[^imranq]
jwpapi는 Jev로 데이터셋을 만든 뒤 Laya를 학습시켜 나머지를 Laya로 처리하면
비용을 아끼는 데 유용할 것이라고 덧붙였다.[^jwpapi]
frag는 이것이 로컬 LLM이 아니고 시스템 1 AI, 곧 상태와 질문을 받아 확률을 내놓는
분류기 같은 것이라서 로컬 실행 여부가 핵심이 아니라고 짚었다.[^frag]
bigyabai는 Laya가 거의 10년 된 Google BERT의 미세 조정
모델이라서 BERT가 데이터센터 증설을 흔들 잠재력이 있었다면 이미 그랬을 것이라고
반박했다.[^bigyabai]
EgregiousCube는 0.3B 모델이 Jev의
오픈소스 대체재라고 주장하기는 어렵지 않으냐고 물었고,
게시자 putna는 대체재라는 표현이 과했을 수 있다고 인정했다.[^EgregiousCube]
ImJasonH는 같은 가중치로 같은 데모를 iPhone 15 Pro에서 돌려 약 40ms에
판단했다고 했다.[^ImJasonH]
이 마지막 수치는 댓글 작성자의 주장이며 README의 것이 아니다.

## 비평

### 속도 수치가 비교 대상에 따라 달라 보인다

헤드라인의 4.98ms는 컴파일된 MLX FP16 대비 1.39배 빠른 값이다.
이는 의미 있는 향상이지만 큰 도약은 아니고,
README도 10배 목표를 달성하지 못했다고 밝힌다.
더 큰 차이는 에너지 쪽의 2.78배이며 이 값은 센서 추정이다.
실제 제품 결정에서는 속도보다 같은 일을 배터리로 얼마나 오래 돌리는가가 의미
있을 수 있고, 그 근거가 추정치라는 점을 감안해야 한다.

### 정확도가 아니라 충실도를 검증했다

저장소가 내세우는 검증은 원본 모델과 선택된 답이 같은지,
보정 확률의 차이가 기준 이내인지에 관한 것이다.
이는 이식이 원본을 훼손하지 않았다는 증거이고 이 모델이 내 과업에서
정확하다는 증거가 아니다.
README가 이를 변환 충실도 확인이라고 분명히 쓰므로 오해는 독자의 몫이다.
판단 모델을 도입하려는 팀은 자기 데이터로 정확도를 따로 재야 한다.

## 기억할 원칙

### 판단 모델은 말을 하지 않는 대신 확률로 책임을 진다

Laya류 모델이 주는 것은 답변 문장이 아니라 선택지별 확률이다.
호출하는 쪽은 그 확률을 문턱값으로 받아 처리하므로,
모델이 틀렸을 때 책임이 확률의 보정 품질로 옮겨 간다.
그래서 이 이식판 README가 보정 온도 제한과 신뢰도 필드의 한계를 길게
적은 것이 눈에 띈다.
빠르고 싼 판단을 쓰려면 먼저 그 판단이 자기 확신을 얼마나 정직하게
말하는지를 측정해야 한다.

---

[^putna-demo]: <https://news.ycombinator.com/item?id=49779758>

[^putna-memory]: <https://news.ycombinator.com/item?id=49779534>

[^speedping]: <https://news.ycombinator.com/item?id=49780354>

[^imranq]: <https://news.ycombinator.com/item?id=49779462>

[^jwpapi]: <https://news.ycombinator.com/item?id=49779588>

[^frag]: <https://news.ycombinator.com/item?id=49777853>

[^bigyabai]: <https://news.ycombinator.com/item?id=49778084>

[^EgregiousCube]: <https://news.ycombinator.com/item?id=49780292>

[^ImJasonH]: <https://news.ycombinator.com/item?id=49781744>
