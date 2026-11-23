# Unsloth Desktop 로컬 AI 입문 가이드

원문: [A beginner's guide to Local AI with Inkling, Qwen, and Unsloth](https://www.gpupartner.com/blog/beginners-guide-local-ai-inkling-qwen-unsloth)

HN 토론: <https://news.ycombinator.com/item?id=50603845> (469점, 196개 댓글)

GN 토론: <https://news.hada.io/topic?id=37670>

## 요약

GPU Partner 블로그에 Jerry James가 2026년 11월 22일에 올린 입문 가이드이다.
Windows PC에 Unsloth Desktop을 설치하고, 그래픽 메모리(VRAM)에 맞는 양자화 모델을 받아,
집 안 네트워크의 가족이 함께 쓰는 개인용 채팅 AI를 만드는 과정을 다룬다.
글은 하드웨어만 갖추면 다운로드 시간을 빼고 10~15분이 걸린다고 한다.

필자의 구성은 다음과 같다.

- 하드웨어는 VRAM 32GB인 RTX 5090이다.
- 모델은 Qwen3.8-27B의 4비트 양자화본(UD-Q4_K_XL)이다.
  전체 정밀도 모델은 약 56GB라 소비자용 그래픽 카드에 들어가지 않는다.
  더 큰 모델도 가능했지만 긴 문맥을 위해 한 단계 낮췄다고 한다.
- 문맥 크기는 양자화하지 않은 128K로 두었다.
- 설정은 세 단계이다. Unsloth Desktop 설치, 모델 내려받기, 문맥 크기 지정이다.
  터미널 명령, Python 환경, 구독은 필요 없다고 한다.
- 집 안 공유는 Unsloth Desktop 설정의 Remote & LAN 탭에서 원격 비밀번호를 정하고
  LAN 접근을 시작하는 것이다. 같은 네트워크의 사람은 알려 준 주소를 브라우저로 열어
  unsloth 계정과 그 비밀번호로 들어온다. 이 PC가 켜져 있어야 접속된다.
- 인터넷을 통한 접근, 성능, 로컬 에이전트는 다음 글로 미룬다.

VRAM별 시작점으로 글이 준 표는 다음과 같다.

| 구간   | VRAM      | 문맥 크기 | 글이 든 모델 예                           |
| ------ | --------- | --------- | ----------------------------------------- |
| 소형   | 8~12GB    | 8K~16K    | Qwen3.5-9B, Gemma 4 12B                   |
| 중형   | 16GB      | 16K~32K   | Qwen3-14B, gpt-oss-20b, Inkling 2 Mini 등 |
| 대형   | 24GB      | 16K~32K   | Gemma 4 31B, Qwen3.8-27B, Inkling 2 Mini  |
| 특대형 | 32GB 이상 | 64K~128K+ | Qwen3.8-27B, Inkling 2 Mini               |

글은 Inkling 2 Mini(Thinking Machines Lab, 2026년 11월 17일 공개,
26.4B 매개변수, Apache 2.0, 문맥 1M 토큰)가 RTX 5090에 들어간다고 하고,
Unsloth이 권하는 UD-Q4_K_XL 파일은 17.6GB라고 한다.
활성 매개변수가 5.4B인 전문가 혼합(MoE) 모델이라 16GB 카드에서도
나머지를 시스템 RAM에 두면 돌아간다고 한다.
Inkling 2 Small은 594B로, 가장 작은 파일도 171.7GB이므로
그래픽 카드가 아니라 통합 메모리 장비의 영역이라고 한다.
Mac은 통합 메모리 덕에 큰 모델을 돌릴 수 있고 Apple Silicon용 MLX 형식을 받으라고 한다.

## 분석

### 글이 내세우는 이유

글의 동기는 클라우드 LLM 제공자가 최신 버전에서 품질을 낮추고,
허용되는 사용 범위를 통제하며, 비용과 개인정보 문제가 커졌다는 판단이다.
이는 필자의 진술이며 글에 근거 자료는 붙어 있지 않다.
필자가 원한 것은 사용량 한도를 신경 쓰지 않고 토큰이 많이 드는 조사, 수집, 코딩을
맡기는 일이었다.

### 크기 선택의 논리

글의 선택 기준은 모델이 들어가는 가장 큰 크기가 아니라
긴 문맥에 여유를 남기는 크기이다.
양자화는 정확도를 조금 내주고 메모리를 얻는 거래이며,
작업에 따라 영향이 없을 수도 있고 거의 못 쓸 수도 있다고 글은 말한다.
이 영향이 어떤 작업에서 어느 정도인지는 글에 측정으로 나오지 않는다.

### 집 안 공유의 범위

글의 공유는 집 안 네트워크로 한정된다.
비밀번호 하나로 모두가 같은 계정으로 들어가는 구조이고,
인터넷 접근은 이 설정만으로 되지 않는다고 분명히 쓴다.

## 비평

### 가격 대비 이득

글은 RTX 5090이 터무니없이 비싸지만 여전히 나쁘지 않은 선택이라고 쓰되 가격은 적지 않는다.
dualvariable은 6500달러라는 가격을 기준으로 Claude Pro 구독 월 17달러의 16년치라며,
자신의 사용량은 한도에 걸리지 않고 모델도 더 나쁘다고 했다.[^dualvariable]
icedchai는 128GB RAM의 Strix Halo 장비로 둘 다 써 본 결과
특정 용도나 개인정보가 중요하지 않다면 월 20달러 구독이 낫다고 했다.[^icedchai]
poulpy123의 반응도 같은 방향으로 매우 비싼 카드가 필요하다는 것이다.[^poulpy123]
글은 비용 비교를 하지 않았고 이 문서도 어느 쪽이 맞는지 판단하지 못한다.

### 더 싼 구성

montroser는 5090이 필요 없고 12~16GB 카드에서 MoE 층을 시스템 RAM으로 내려
돌리면 된다며, 중고 Dell 워크스테이션과 Tesla P100을 합쳐 약 850달러 구성을 들었다.[^montroser]
tacoman은 Nvidia P40을 약 300달러에 구해 Qwen 3.8 27B Q4를 llama.cpp로
초당 14토큰으로 돌린다고 했다.[^tacoman]
denkmoon은 초당 14토큰이면 프롬프트를 넣고 하루 뒤에 돌아오는 수준이라며
자신이 40만 토큰짜리 작업을 한 예를 들었다.[^denkmoon]
calebkaiser는 먼저 시간당 0.3~1달러로 GPU를 빌려 시험하라고 권했지만
이는 완전한 로컬이 아니고 개인정보 측면을 따져야 한다고 덧붙였다.[^calebkaiser]
이들은 모두 댓글의 경험이며 이 문서가 확인한 것이 아니다.

### 보안

angry_octet는 집 안 PC 수천 대가 보호되지 않은 LAN 접근으로 모델을 돌리게 되면
가정용 회선에 거대한 에이전트 군집이 생길 것이라고 우려했다.[^angry_octet]
글은 LAN 공유를 원격 비밀번호로 보호한다고 하고 인터넷 노출은 다루지 않는다.
이 우려가 글의 설정에 그대로 해당하는지는 글만으로는 알 수 없다.

### 로컬이 따라잡는가

_pdp_는 지금이 플라스마 TV 단계의 로컬 AI이며
5년 안에 대부분의 실용적인 AI가 자기 기기에서 돌고 일부 초지능만 클라우드에 남으리라고 보았다.[^_pdp_]
oytis는 쓴 교훈(bitter lesson)을 들어 반대했다.
5년 뒤 지금의 최고 성능이 일반 하드웨어에서 돌면 데이터센터의 모델은 훨씬 강해질 것이라는 이유이다.[^oytis]
N8works는 64GB 맥북으로도 매우 쓸 만한 모델을 돌릴 수 있다고 했다.[^N8works]
이 논쟁은 글 밖의 예측이며 확인할 수 없다.

### 구체적인 모델 이야기의 불일치

IronWolve는 125B 규모의 Qwen flash next 양자화본이 낮은 VRAM에서 27B Qwen을 이긴다고 했고,[^IronWolve]
drillsteps5는 확인해 보니 그 파일이 약 40GB여서 8GB VRAM에 맞지 않고
특정 llama.cpp 개정과 패치가 필요하다고 반박했다.[^drillsteps5]
글의 표와 달리 댓글에서는 모델 이름과 크기가 엇갈린다.
이 문서는 둘 중 어느 쪽이 맞는지 확인하지 못했다.

## 인사이트

### 글에서 가져갈 것

이 글은 한 가지 구성(5090, 27B 4비트, 128K 문맥)의 절차 기록이다.
가이드로서 쓸모는 VRAM별 표와 세 단계 설정에 있고,
비용과 성능의 비교는 독자가 직접 해야 한다.
시작 전에 빌린 GPU로 시험해 보라는 댓글이 비용 위험을 줄이는 실용적인 순서이다.

### 확인할 관찰

1. 같은 설정에서 실제 속도와 응답 품질이 일상 작업에 충분한지.
2. 양자화 단계가 내려갈 때 작업별 품질 저하가 어떤지.
3. LAN 공유 설정이 비밀번호 하나로 충분히 안전한지.
4. 글이 예고한 후속편에서 성능과 에이전트 구성이 어떻게 나오는지.

위 넷 모두 이 문서가 확인하지 못했다.

---

[^dualvariable]: <https://news.ycombinator.com/item?id=50605683>

[^icedchai]: <https://news.ycombinator.com/item?id=50607082>

[^poulpy123]: <https://news.ycombinator.com/item?id=50604572>

[^montroser]: <https://news.ycombinator.com/item?id=50606773>

[^tacoman]: <https://news.ycombinator.com/item?id=50606063>

[^denkmoon]: <https://news.ycombinator.com/item?id=50607782>

[^calebkaiser]: <https://news.ycombinator.com/item?id=50606441>

[^angry_octet]: <https://news.ycombinator.com/item?id=50604606>

[^_pdp_]: <https://news.ycombinator.com/item?id=50604818>

[^oytis]: <https://news.ycombinator.com/item?id=50604934>

[^N8works]: <https://news.ycombinator.com/item?id=50606079>

[^IronWolve]: <https://news.ycombinator.com/item?id=50606487>

[^drillsteps5]: <https://news.ycombinator.com/item?id=50606601>
