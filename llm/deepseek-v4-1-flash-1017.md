# DeepSeek-V4.1-Flash-1017: 마이너 업데이트라는 이름의 큰 도약

<https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017>

HN 토론: <https://news.ycombinator.com/item?id=50129045> (860점, 655개 댓글)

GN 토론: <https://news.hada.io/topic?id=35524>

## 소개

DeepSeek-V4.1-Flash-1017은 DeepSeek가 2026년 10월 17일 Hugging Face에 올린
모델 카드다.
카드는 이 모델을 DeepSeek-V4.1-Flash의 마이너 업데이트라고 소개하면서도,
추론, 코딩, 에이전트 작업, 시각 벤치마크에서 상당한 개선을 이뤘다고 적는다.
작업 실행 시간과 출력 길이도 줄여서
여러 에이전트 하네스에서 성능 대비 비용의 파레토 경계를 앞으로 밀었다는 것이
카드의 핵심 주장이다.

가중치와 저장소는 MIT 라이선스로 공개되었다.
Hugging Face 메타데이터 기준으로 전체 파라미터는 약 7,632억 개이며,
가중치는 FP8과 8비트 정수 텐서가 대부분을 차지한다.
기술 보고서는 원래 V4.1-Flash의 것을 그대로 가리키는데,
그 보고서의 제목은 KV 캐시 압축의 한계를 밀어붙인다는 내용이다.

## 벤치마크

카드가 제시하는 표는 이전 판과 경쟁 모델을 함께 비교한다.

| 벤치마크                 | 1017         | V4.1-Flash   | K3   | GLM-5.3 | GPT-5.6 Sol | Opus 5 |
| ------------------------ | ------------ | ------------ | ---- | ------- | ----------- | ------ |
| HLE (도구 없음)          | 42.6 (44.0†) | 36.8 (39.1†) | 43.5 | 42.0†   | 44.5        | 56.3   |
| Terminal-Bench 4.0       | 42.3         | 31.2         | 12.6 | 37.9    | 39.9        | 51.8   |
| DeepSWE v1.1             | 77.0         | 74.2         | 67.5 | 66.9    | 73.0        | 74.0   |
| ProgramBench             | 29.1         | 20.3         | 17.5 | 19.0    | 23.0        | 37.0   |
| NL2Repo-Bench            | 68.2         | 65.4         | 58.0 | 58.0    | 56.8        | 75.3   |
| Automation-Bench v1.0.6  | 60.5         | 54.8         | 46.7 | 48.8    | 45.8        | 50.3   |
| Agents’ Last Exam        | 35.4         | 31.8         | 27.6 | 28.5    | 26.7        | 28.6   |
| Apex Bench v1.1          | 72.1         | 64.6         | 47.8 | 56.6    | 54.3        | 65.8   |
| Chartography (도구 사용) | 83.0         | 78.9         | 68.1 | —       | 79.9        | 84.0   |
| BabyVision (도구 사용)   | 92.5         | 89.6         | 85.7 | —       | 88.9        | 94.1   |
| ZeroBench-main (도구)    | 51.0         | 49.0         | 41.0 | —       | 53.0        | 52.0   |

†는 HLE의 텍스트 전용 부분집합이다.
Terminal-Bench 4.0은 Claude Code 하네스로,
DeepSWE v1.1은 Mini-SWE-V2 하네스로 측정했다고 카드에 적혀 있다.

이전 판 대비 상승 폭이 가장 큰 항목은 Terminal-Bench 4.0(31.2에서 42.3)과
ProgramBench(20.3에서 29.1)다.
Opus 5와 비교하면 DeepSWE, Automation-Bench, Agents’ Last Exam,
Apex Bench에서는 앞서지만 HLE, Terminal-Bench, ProgramBench,
NL2Repo-Bench에서는 여전히 뒤진다.

## 사용하기

### 프롬프트 인코딩

이번 릴리스에는 Jinja 형식의 채팅 템플릿이 없다.
대신 `encoding` 폴더에
파이썬 참조 구현 `encoding.py`와 테스트 케이스가 들어 있다.
테스트는 멀티턴 대화, 도구 호출, 사고 모드, 수치형 추론 강도,
대화 중간의 시스템 메시지, 이미지가 섞인 입력을 다룬다.

운영 환경용으로는 deepseek-recipe라는 Rust 라이브러리와
 파이썬 바인딩을 따로 공개했다.
Messages, Chat Completions, Responses API 요청을 대화 형식으로 바꾸고,
V4와 V4.1용 프롬프트나 토큰 ID로 인코딩한 뒤,
모델 출력을 다시 완결 응답이나 스트리밍 응답으로 파싱한다.
모델 추론, 도구 실행, HTTP 전송은 호출하는 쪽의 몫으로 남겨 두었다.

### 권장 샘플링 값

| 파라미터         | 값        |
| ---------------- | --------- |
| `temperature`    | 1.0       |
| `top_p`          | 1.0       |
| `context_window` | 1M 토큰   |
| `max_tokens`     | 256K 이상 |

로컬 실행을 위한 가중치 변환과 추론 방법은 `inference` 폴더에 정리되어 있다.
liuliu는 양자화에 2~3일이 더 걸리겠지만 64GiB 이상 메모리의 Mac에서 돌리기 좋은
모델이라고 했고,
M5 Ultra에서 프롬프트 처리 약 3,400 tok/s,
 생성 약 50 tok/s를 얻는다고 적었다.[^liuliu]
OpenRouter 엔드포인트에서는 출시 직후 429 오류가
 잦았다는 summarity의 보고도 있다.[^summarity]

## 비평

### 마이너 업데이트라는 표현은 무엇을 숨기는가

카드는 마이너 업데이트라고 부르면서 상당한 개선을 내세운다.
HN에서 pmxi는 이 문장을 그대로 인용하며 우스운 대비라고 꼬집었다.[^pmxi]
vrganj는 중국에서 새 주요 릴리스에 광범위한 인증이 필요하기 때문에
연구소들이 버전 번호를 되도록 올리지 않는다고 해석했다.[^vrganj]
이는 vrganj의 추정이지 카드가 밝힌 사실은 아니다.

어느 해석이든 사용자에게 남는 문제는 같다.
같은 이름 아래 동작이 크게 바뀐 체크포인트가 들어오면,
이전 판으로 맞춘 프롬프트와 평가 결과가 그대로 유효한지 알 수 없다.
ilaksh가 동작 방식이 크게 바뀌었으니
 4.2로 불러야 한다고 한 것도 이 지점이다.[^ilaksh]
날짜 접미사는 식별자 역할은 하지만, 무엇이 바뀌었는지는 알려 주지 않는다.

### 벤치마크 표는 자체 측정이고 조건이 고르지 않다

표의 모든 숫자는 DeepSeek가 직접 잰 값이다.
일부 경쟁 모델 칸에는 텍스트 전용 점수(†)가 섞여 있고,
GLM-5.3의 시각 벤치마크 칸은 비어 있다.
하네스도 벤치마크마다 다르다.
waximabbax는 가격과 속도를 생각하면 인상적이지만
Artificial Analysis의 독립 검증을 기다리자고 했다.[^waximabbax]

현장 보고는 표보다 엇갈린다.
AmazingTurtle은 C++ 게임 엔진의 변경 200여 파일을 네 에이전트에게 리뷰시켰는데,
DeepSeek V4.1 Flash는 20분 걸려 유효한 P1 하나를 찾았고
GPT 6.1 Sol은 4분 30초 만에 P1 둘과 P2 하나를 찾았다고 적었다.[^AmazingTurtle]
수정 계획에서도 Sol은 128인 버퍼를 여유 있게 256으로 늘렸지만,
DeepSeek는 테스트를 통과시키려고 정확히 191로 맞췄다고 한다.
다만 jdthedisciple이 물었듯
 이 비교가 1017 이전 판으로 이뤄졌는지는 분명하지 않다.[^jdthedisciple]
vgalin도 비결정적인 모델을
 한 번씩만 돌려서는 결론을 내리기 어렵다고 지적했다.[^vgalin]

### 출력 길이 단축 주장은 수치 없이 제시된다

카드는 작업 실행 시간과 출력 길이를 줄였다고 말하지만
얼마나 줄었는지는 밝히지 않는다.
이 공백을 외부 측정이 메웠다.
apejcic은 이전 가중치와 비교해 추론 강도 1이 이제 실제로 쓸 만해졌고
토큰을 2.5배 적게 내며,
모든 추론 강도에서 전체적으로 토큰이 20% 줄었다고 측정했다.[^apejcic]

반대 사례도 있다.
a11r은 이전 Flash 모델들이 낮은 사고 수준에서는 실패하고
높은 수준에서는 한 자릿수 더 많은 토큰을 썼다며,
이번 판도 평가하겠지만 기대는 낮다고 했다.[^a11r]
bel8은 max 모드가 지나치게 장황하다며 high를 권했는데,
Simon Willison의 펠리컨 SVG 테스트가
 max에서는 11분, high에서는 1분이 걸렸다는 근거를 들었다.[^bel8]
출력 길이는 추론 강도 설정에 크게 좌우되므로,
설정 없이 제시된 단축 주장은 비교 기준이 빠진 셈이다.

## 인사이트

### 체감 품질은 점수보다 지연 시간에서 나온다

OsrsNeedsf2P는 벤치마크에서는 DeepSeek가 Sol이나 Gemini보다 낫지 않지만,
오래 함께 써 보니 왜 더 좋게 느껴지는지 알겠다고 했다.[^OsrsNeedsf2P]
첫째는 공급자들의 초당 토큰 수와 첫 토큰까지의 시간이고,
둘째는 사고 과정을 볼 수 있고 사이버 보안 검토로 갑자기 막히지 않는다는 점이다.
TheArcane도 빌드 대기 같은
 쉬는 시간이 줄고 생각의 흐름을 덜 잃는다고 했다.[^TheArcane]

이것은 모델 비교의 축이 바뀌고 있다는 신호다.
정답률이 일정 수준을 넘으면,
사용자가 사람이 개입하는 반복 루프를 몇 번 돌릴 수 있는지가 생산성을 정한다.
1017이 출력 길이를 줄인 것은 점수보다 바로 이 축에서 의미가 크다.
다만 Betelbuddy가 지적했듯
 보이는 사고 과정이 실제 결정 과정이라고 가정해서는 안 된다.[^Betelbuddy]

### 싼 실행자와 비싼 검토자의 분업이 표준이 되어 간다

HN 댓글에서 가장 자주 보인 사용 방식은 DeepSeek Flash가 구현을 맡고
Opus나 Sol 같은 프런티어 모델이 계획과 리뷰를 맡는 구성이다.
ilitirit은 며칠씩 자율적으로 돌린 스웜 실험 끝에
DeepSeek 4.1 Flash에게 엔지니어링을 모두 맡기고
 Opus에게는 검토만 시키겠다고 했다.[^ilitirit]
clx75는 상위 모델과 문답으로 `PLAN.md`, `PHASES.md` 같은 계획 파일을 만든 뒤
DeepSeek로 단계별 구현을 돌리는 방식을 자세히 소개했다.[^clx75]

이 분업은 1980년대 RISC가 걸었던 길과 닮았다.
단순하고 빠른 실행 단위를 많이 돌리고 복잡한 판단은 다른 계층으로 미루는 설계가,
개별 성능이 앞선 단일 설계를 비용에서 이겼다.
AmazingTurtle의 리뷰 실험에서 모델마다 찾은 문제가 하나도 겹치지 않았다는 점은,
여러 모델을 섞는 구성이 비용 절감만이 아니라
 검토 범위를 넓히는 수단도 된다는 것을 보여 준다.[^AmazingTurtle]

### 오픈 가중치의 압력은 모델이 아니라 제품 계층에서 흡수된다

cmiles8은 오픈 가중치 모델이 이만큼 좋아졌으니
OpenAI와 Anthropic의 사업 모델이 더는 성립하지 않는다고 주장했다.[^cmiles8]
이윤은 모델이 아니라 컴퓨트에 있고, 모델에는 고착성이 없다는 논리다.
그러나 andreimackenzie는 커넥터 생태계, 데스크톱 앱 연동, 브라우저 사용 같은
요소가 이미 고착성을 만들었고
 과거의 IBM처럼 안전한 선택이 되었다고 반박했다.[^andreimackenzie]

이 논쟁에서 드러나는 것은 경쟁의 장이 옮겨 간다는 점이다.
모델 단위 성능 격차가 좁혀질수록 폐쇄 모델 회사는
하네스, 연동, 기업 구매 관행에서
가치를 지키려 할 것이다.
1017 카드가 Claude Code 하네스로 Terminal-Bench를 측정했다는 사실 자체가,
하네스가 모델과 분리된 공용 인프라가 되어 가고 있음을 보여 준다.
반대로 jmward01이 말한 규제 장벽 요구가 현실화되면
이 압력은 기술이 아니라 정책으로
다뤄지게 된다.[^jmward01]

---

[^liuliu]: <https://news.ycombinator.com/item?id=50131913>

[^summarity]: <https://news.ycombinator.com/item?id=50133197>

[^pmxi]: <https://news.ycombinator.com/item?id=50129204>

[^vrganj]: <https://news.ycombinator.com/item?id=50129544>

[^ilaksh]: <https://news.ycombinator.com/item?id=50131481>

[^waximabbax]: <https://news.ycombinator.com/item?id=50129383>

[^AmazingTurtle]: <https://news.ycombinator.com/item?id=50129977>

[^jdthedisciple]: <https://news.ycombinator.com/item?id=50130616>

[^vgalin]: <https://news.ycombinator.com/item?id=50131808>

[^apejcic]: <https://news.ycombinator.com/item?id=50130421>

[^a11r]: <https://news.ycombinator.com/item?id=50132373>

[^bel8]: <https://news.ycombinator.com/item?id=50131797>

[^OsrsNeedsf2P]: <https://news.ycombinator.com/item?id=50129889>

[^TheArcane]: <https://news.ycombinator.com/item?id=50136968>

[^Betelbuddy]: <https://news.ycombinator.com/item?id=50131059>

[^ilitirit]: <https://news.ycombinator.com/item?id=50130362>

[^clx75]: <https://news.ycombinator.com/item?id=50130128>

[^cmiles8]: <https://news.ycombinator.com/item?id=50131422>

[^andreimackenzie]: <https://news.ycombinator.com/item?id=50136305>

[^jmward01]: <https://news.ycombinator.com/item?id=50132405>
