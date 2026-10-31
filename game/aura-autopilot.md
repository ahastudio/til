# Aura Autopilot: 게임을 직접 플레이하며 배우는 실시간 플레이테스트 에이전트

<https://github.com/ramenvr/autopilot>

## 소개

Aura Autopilot은 Unreal Engine 5, Unity 6,
Godot 4를 지원하는 오픈소스 플레이테스트(playtest) 시스템이다.
Windows와 macOS에서 쓸 수 있고, 프로젝트에 설치하면 게임을 학습하고 레벨을
탐색하며 실행을 거듭할수록 플레이가 나아진다는 것이 만든 쪽의 설명이다.
Aura라는 Unreal과 Unity 개발자용 AI 에이전트를 만든 개발진이 낸 도구이고,
Autopilot은 Aura 구독에도 포함되며 오픈소스 버전은 사용자 자신의 API 키도
받는다고 한다.[^homepage]
저장소는 2026-10-30에 만들어져 별 263개, 포크 14개,
열린 이슈 2개이고 라이선스는 Apache-2.0이며 언어는 Python이다.

### 어떻게 쓰는가

가장 기본적인 사용법은 편집기 안의 플러그인이다.
Unreal은 `Autopilot/`을 프로젝트의 `Plugins/` 폴더에 옮기고,
Unity는 `com.ramenvr.autopilot-<version>.tgz`를 Package Manager에서 tarball로
설치하며, Godot은 `autopilot/`을 `addons/`에 옮긴 뒤 플러그인을 켠다.
지원 버전은 Unreal 5.4~5.8, Unity 6 이상, Godot 4.7 이상이다.
소스에서 설치하는 방법은 Unreal에만 지원되고,
PowerShell 스크립트로 Unreal 소스 빌드에 맞춰 플러그인을 만들어 프로젝트의
`Plugins/`에 넣어 준다.

설치 뒤 첫 실행의 설정 흐름은 Aura 계정 만들기나 로그인, 설정 실행, 인증 완료,
실행 기록 공유 여부 선택, 선택 사항인 10분짜리 탐색 실행,
그리고 프롬프트 입력이다.
README는 Aura 계정을 쓰길 권하고, 실행 기록 공유는 켜 주면 고맙겠다고 쓴다.
Claude Code나 Codex에서 쓰려면 터미널에서 `autopilot connect claude` 또는
`autopilot connect codex`를 실행하고 스킬과 MCP 서버를 통해 쓴다.
이 경로는 사용자의 Claude나 ChatGPT 구독을 쓴다.

### 프롬프트의 네 가지 종류

프롬프트는 네 종류 중 하나이다.

| 종류               | 예                                                      |
| ------------------ | ------------------------------------------------------- |
| 탐색(Exploration)  | Lvl_Main의 제작 시스템을 탐색하라                       |
| 테스트(Testing)    | 열려 있는 레벨을 돌며 이상해 보이는 것을 모두 알려 달라 |
| 검증(Verification) | 도끼로 치면 나무가 흔들리는지 검증하라                  |
| 목표(Goal)         | 체력을 최대치의 20% 위로 유지하면서 보스를 처치하라     |

프롬프트마다 PIE 창을 띄우고 프로젝트의 소스 코드를 읽고, PIE를 탐색하고,
프롬프트에 따라 플레이한다.
끝나면 PIE 창이 닫히고 보고서가 생성된다.

## 동작 방식

README의 설명은 이렇다.
Autopilot은 LLM 코딩 에이전트가 게임에 대해 아는 것을 바탕으로 결정
모델(decision model)을 위한 하니스(harness)를 만들고,
플레이 중에는 결정 모델에게 행동 선택을 요청한다.
처음 몇 번은 게임에 대한 기억(memory)을 채우는 동안 서툴 수 있고,
실행을 거듭할수록 같은 일을 더 빠르게 하고 더 똑똑하게 움직인다고 한다.

저장소의 설정 파일이 이 두 층의 정체를 보여 준다.
결정 모델은 `TYPESAFE_API_KEY`로 쓰는 Jev라는 이름의 외부 서비스이고,
게임을 조사하고 하니스를 쓰는 언어 모델은 기본 에이전트인 OpenCode, Claude Code,
Codex 중에서 고르며 기본 모델은 Anthropic의 모델이다.[^env]
Autopilot 서버는 `autopilot serve`로 띄우면 플러그인을
`ws://127.0.0.1:8765/v1/bridge`에서 기다린다.[^contributing]

하니스가 쓰는 도구 모음(kit)은 게임 상태에 넓게 접근한다.
어느 객체의 어느 속성이든 읽을 수 있고 보호된 변수와 Blueprint 변수도 포함하며,
함수를 호출하고, 플레이어의 시점에서 보이는 것과 화면의 텍스트와 상호작용 가능한
UI 요소를 얻는다.[^kit]
모델이 쓴 코드가 실행되는 곳은 `AUTOPILOT_SANDBOX` 설정으로 정한다.[^env]

### 데이터와 신뢰

버그 신고에 첨부하는 실행 기록에는 에이전트의 로그, 하니스 버전,
보고서가 들어 있고 게임의 코드를 인용할 수 있다.[^contributing]
공유되는 실행 데이터는 `redact.py`가 비밀 값(API 키와 토큰 같은 모양,
비밀스러운 이름에 지정된 값), 프로젝트와 홈 폴더의 경로,
사용자 이름과 컴퓨터 이름, 이메일 주소를 지운다.[^redact]
보안 취약점은 공개 이슈 대신 GitHub의 비공개 취약점 보고로 신고하라고
한다.[^security]

## 분석

### 사람처럼 보고 누르는 것이 아니라 엔진 안에서 읽고 호출한다

Autopilot이 게임을 한다는 말은 화면을 보고 입력을 흉내 내는 것과 다르다.
도구 모음은 엔진 내부의 상태를 읽고 함수를 호출하는 특권 접근을 주며,
시점과 시야의 정보도 함께 준다.[^kit]
이 구조의 이점은 속도이다.
화면을 해석할 필요 없이 필요한 값을 바로 얻는다.
대가는 사람이 경험하는 것과 에이전트가 경험하는 것이 어긋날 수 있다는 점이다.
이는 필자의 해석이며, 이 저장소만으로는 어느 종류의 결함이 이 방식에서 놓치기
쉬운지 확인할 수 없다.

### 느린 모델과 빠른 모델의 역할을 나누었다

실시간 게임은 모델의 응답 지연이 큰 장애물이다.
Autopilot은 언어 모델이 한 번 하니스를 쓰고,
플레이 중의 순간순간의 선택은 결정 모델이 맡는 구조로 이를 비켜 간다.
하니스는 코드이므로 저장되고 버전이 붙으며 실행마다 다시 쓸 수
있다.[^contributing]
README가 실행할수록 더 빠르고 똑똑해진다고 말하는 근거는 이 저장된 기억과
하니스의 개선이다.

### 프롬프트 종류가 곧 테스트의 정의이다

프롬프트의 네 종류는 탐색, 이상 탐지, 가설 확인, 목표 달성이다.
저장소의 예제 벤치마크는 검증 프롬프트에 CONFIRMED나 DENIED를,
목표 프롬프트에 achieved를 기대 답으로 적는다.[^bench]
테스트의 결과가 사람이 정한 기대와 맞는지로 판정되는 구조이다.
탐색과 이상 탐지 프롬프트는 기대 답이 없고,
그 결과는 보고서에서 사람이 읽어야 한다.

## 비평

### 속도 비교는 제작사의 일곱 과제에 대한 주장이다

Aura의 홈페이지는 Unreal Engine 5.8 게임 하나에서 일곱 과제를 Autopilot과 Claude
Code와 다른 게임 에이전트에게 맡긴 결과를 보여 준다.
Autopilot은 과제당 평균 262초이고 Claude Code는 437초이며,
통과는 각각 7개와 5개이고 다른 에이전트는 4개라고 한다.[^homepage]
한 게임, 한 엔진 버전, 일곱 과제이고, 비교 대상 하나는 이름이 없으며,
백서는 이 글이 열어 보지 못했다.
속도 1.7배라는 표현은 평균 시간의 비율이고, 과제 수가 적어 분산을 말할 수 없다.
치팅한 실행은 실패로 센다고 하지만, 특권 접근이 가능한 구조에서 치팅이
무엇인지는 홈페이지에 정의되어 있지 않다.

### 오픈소스라는 표현이 서비스 의존을 가린다

저장소는 Apache-2.0이다.
그러나 설정 파일은 게임을 플레이하는 결정 모델을 외부 서비스의 키로 쓴다고
적는다.[^env]
README는 설정 흐름에서 Aura 계정을 권장하고,
홈페이지는 Aura 구독에 포함된다고 쓴다.
이 저장소가 확인되는 범위에서, 결정 모델을 다른 것으로 바꿀 수 있는지는 이 글이
찾지 못했다.
코드를 바꿀 수 있다는 것과 서비스 없이 돌릴 수 있다는 것은 다른 이야기이다.

### 막 시작한 프로젝트이고, 지원 범위에는 단계가 있다

저장소는 만들어진 지 이틀이 안 되었고 기여자 목록에는 사람 한 명과 빌드
머신이 보인다.
지원한다고 말하는 세 엔진 가운데 소스 설치는 Unreal에만 지원된다는 점도
README에 있다.
Unity와 Godot에서 쓰는 방법은 미리 빌드된 패키지뿐이라는 뜻이다.
이는 흠이라기보다 시작 단계의 모습이지만,
도입을 검토하는 팀이 알아야 할 조건이다.

## 인사이트

### 하니스를 코드로 남기는 방식은 테스트를 자산으로 바꾼다

모델이 즉흥적으로 게임을 하는 것과 모델이 쓴 하니스가 코드로 남는 것은 다르다.
코드는 읽고, 고치고, 다시 실행할 수 있다.
실행 기록에 하니스 버전이 들어 있다는 것은 어떤 하니스가 어떤 결과를 냈는지
추적할 수 있다는 뜻이다.[^contributing]

그러나 긴장이 있다.
게임이 패치되면 저장된 기억과 하니스는 낡는다.
README는 기억을 쌓는 것을 장점으로 말하지만,
낡은 기억을 어떻게 걸러 내는지는 말하지 않는다.
필자의 추정으로는 패치 뒤 첫 실행에서 성능이 떨어지는지가 이 방식의 실제 비용을
가장 먼저 보여 줄 것이다.

### 게임의 테스트에서도 정답을 누가 정하는가가 남는다

검증 프롬프트의 기대 답은 사람이 손으로 확인한 값이라고 예제가 밝힌다.[^bench]
도구는 실행과 판정을 자동화하지만, 무엇이 맞는 동작인지는 사람이 정한다.
따라서 이 도구가 줄이는 것은 실행의 노동이고, 사양을 정하는 노동은 그대로이다.

### 실행 기록의 공유는 학습 자료와 코드 노출이 한 묶음이다

README는 실행 기록을 공유하면 Autopilot을 개선하는 데 쓰이니 켜 달라고 한다.
실행 기록은 게임의 코드를 인용할 수 있는 자료이다.[^contributing]
경로, 키, 이름, 이메일을 지우는 처리가 있지만 지우는 대상은 비밀 값과 개인 식별
정보이고 게임의 코드 자체는 아니다.[^redact]
저장소에는 `dataset.py`와 `tools/training_data.py`가 있는데 이 글은 열어 보지
않았으므로 공유된 기록이 어떻게 쓰이는지는 확인하지 못했다.
그래서 공유를 켜기 전에 확인할 것은, 어떤 파일이 나가고 그중 게임 코드가 어느
정도 포함되는지이다.

---

[^homepage]: Aura, [Aura Autopilot](https://tryaura.dev/autopilot)

[^env]: GitHub, [.env.example](https://github.com/ramenvr/autopilot/blob/main/.env.example)

[^contributing]: GitHub, [Contributing to Autopilot](https://github.com/ramenvr/autopilot/blob/main/CONTRIBUTING.md)

[^kit]: GitHub, [The harness kit (autopilot.kit)](https://github.com/ramenvr/autopilot/blob/main/autopilot/KIT.md)

[^redact]: GitHub, [autopilot/redact.py](https://github.com/ramenvr/autopilot/blob/main/autopilot/redact.py)

[^security]: GitHub, [Security policy](https://github.com/ramenvr/autopilot/blob/main/SECURITY.md)

[^bench]: GitHub, [bench/example.json](https://github.com/ramenvr/autopilot/blob/main/bench/example.json)
