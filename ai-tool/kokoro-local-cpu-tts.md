# CPU만으로 돌리는 고품질 로컬 TTS, Kokoro

<https://ariya.io/2026/03/local-cpu-friendly-high-quality-tts-text-to-speech-with-kokoro/>

HN 토론: <https://news.ycombinator.com/item?id=48821576> (246점, 56개 댓글)

## 요약

Kokoro는 파라미터 8200만 개에 불과한 경량 TTS(Text-to-Speech)
모델로, 영어·중국어·힌디어 등 여러 언어에서 실감나는 음성을
합성한다. 약 50개의 목소리를 제공하며 영어에 가장 최적화되어
있다. 이 글은 별도의 GPU 없이 CPU만으로 Kokoro를 로컬에서
실용적으로 돌리는 방법을 다룬다.

가장 손쉬운 배포 방법은 컨테이너화된 서비스인 Kokoro-FastAPI를
쓰는 것이다.

```
podman run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu
```

이 명령 하나로 `localhost:8880/web`에 웹 UI가 뜨고, OpenAI의
음성 API와 호환되는 인터페이스를 제공해 기존 애플리케이션에
바로 연결할 수 있다. 목소리 선택은 환경 변수로 조정하며, JavaScript와
Python 스크립트로 커맨드라인 테스트도 가능하다. 생성된 오디오는
MP3로 출력되고, SoX가 설치되어 있으면 자동 재생도 된다. 컨테이너
이미지 용량은 약 5GB다.

성능은 프로세서에 따라 갈린다. 12년 된 Intel Core i7-4770K에서는
4.7초, Apple M2 Pro에서는 4.5초, AMD Ryzen 7 8745HS에서는 1.5초가
걸렸다. 오래된 하드웨어에서도 충분히 쓸 만한 속도라는 점을
저자는 강조한다. 대안으로는 더 작은 컨테이너 용량과 STT(음성
인식) 기능까지 갖춘 Speaches가 언급된다.

## 분석

### "GPU 없이도 충분하다"는 문턱이 로컬 AI 도구의 확산 조건을 바꾼다

TTS는 오랫동안 실시간성과 자연스러움을 확보하려면 GPU 가속이
사실상 필수라고 여겨져 온 영역이다. Kokoro가 8200만 파라미터라는
작은 크기로 CPU에서도 수 초 내 합성을 해낸다는 사실은, 로컬 AI
도구의 채택 문턱을 "GPU를 갖춘 개발 머신"에서 "일반 노트북"으로
낮춘다. 이는 접근성 도구, 홈서버, 저사양 임베디드 환경처럼 GPU를
가정할 수 없는 곳에서도 고품질 음성 합성을 내재화할 수 있다는
뜻이다.

## 비평

### 벤치마크 하드웨어 구성이 제한적이라 일반화하기 어렵다

세 종류의 CPU 벤치마크만 제시되어 있어, 더 저사양인 모바일
프로세서나 ARM 기반 SBC(싱글보드 컴퓨터)에서의 성능은 추정하기
어렵다. 특히 "12년 된 CPU에서도 4.7초"라는 결과가 인상적이긴
하지만, 실시간 대화형 응용에 쓰기엔 여전히 지연이 있는 수준인지,
아니면 문서 낭독처럼 지연에 관대한 용도에만 적합한지 구분해서
평가할 필요가 있다.

### 짧은 단어나 고유명사 발음의 편차

HN 댓글에서 지적된 것처럼, 짧은 단어 발음이나 고유명사 처리에서
모델별 편차가 크다는 한계가 있다.[^kokoro-hn] 이는 실제 제품에
적용하기 전에 대표적인 실사용 문장으로 회귀 테스트를 구성해야
한다는 뜻이며, 벤치마크 수치만으로는 드러나지 않는 실무적
리스크다.
sudobash1은 접근성 제품에 Kokoro를 적용한 경험에서, 단어를
단독으로 발음시키면 원치 않는 음소가 섞여 나오는 문제가 있어
목표 단어를 긴 문장 안에 넣어 합성한 뒤 타임스탬프 데이터로
오디오를 잘라내는 우회법을 쓰고 있다고 밝혔다[^sudobash1].
lucumo는 지원 언어 범위 자체가 제한적이라는 점을 지적했는데,
네덜란드어처럼 지원이 약한 언어는 결국 크기나 성능이 떨어지는
다른 모델을 대신 써야 했다고 밝혔다[^lucumo].
keyle은 Apple M2 Pro에서 약간만 긴 문단을 입력해도 곧바로
크래시가 발생한다고 보고해, 안정성 면에서 아직 다듬을 부분이
있음을 보여줬다[^keyle].

### 벤치마크 이상의 실사용 사례가 다양하게 보고됐다

kn100은 직접 만든 인터콤 도어 시스템에 이 엔진을 실제로 쓰고
있으며 음질이 매우 좋다고 평가했다[^kn100].
mowmiatlas는 Kokoro를 아이폰의 ANE(Apple Neural Engine)로
포팅해, 배터리 소모와 발열을 줄이면서 실시간 자연스러운 TTS를
구현했다고 밝혔다[^mowmiatlas].
bronco21016은 기사를 팟캐스트로 변환해 애플 팟캐스트로 아침에
청취하는 개인용 RSS 피드 시스템을 만들었고[^bronco21016],
cat_plus_plus는 로컬 LLM 기반 개인 일본어 튜터 애플리케이션에
Kokoro를 통합했다고 소개했다[^cat_plus_plus].
teravor는 대안으로 Pocket TTS를 언급하며, 좋은 목소리를 추출해
쓸 경우 Pocket TTS가 더 낫고 CPU 추론에는 ONNX 버전이 유리하다는
비교 의견을 남겼다[^teravor].

## 인사이트

### STT와 TTS 모두 "작은 로컬 모델 우선, 고품질은 클라우드로" 하이브리드 구조로 수렴하고 있다

Kokoro와 Speaches 같은 프로젝트들은 음성 합성·인식 모두에서 작은
로컬 모델이 기본 기능을 담당하고, 더 높은 품질이 필요할 때만
클라우드 모델로 전환하는 하이브리드 구조가 점차 표준이 되고
있음을 보여준다. 이는 비용과 지연시간, 프라이버시라는 세 가지
축에서 로컬 모델이 이미 "충분히 좋은" 수준에 도달했다는 신호이며,
문서 읽기·알림 음성화·홈서버 안내 방송 같은 저위험 기능부터
먼저 이 구조로 전환될 가능성이 높다. HN 댓글에서는 접근성 제품과
전자책 낭독 같은 실사용 사례, 그리고 Pocket TTS나 Piper 같은
대안과의 비교가 활발히 오갔다.[^kokoro-hn]

---

[^kokoro-hn]: <https://news.ycombinator.com/item?id=48821576>
[^sudobash1]: <https://news.ycombinator.com/item?id=48823393>
[^lucumo]: <https://news.ycombinator.com/item?id=48829204>
[^keyle]: <https://news.ycombinator.com/item?id=48826233>
[^kn100]: <https://news.ycombinator.com/item?id=48822415>
[^mowmiatlas]: <https://news.ycombinator.com/item?id=48823242>
[^bronco21016]: <https://news.ycombinator.com/item?id=48824438>
[^cat_plus_plus]: <https://news.ycombinator.com/item?id=48824873>
[^teravor]: <https://news.ycombinator.com/item?id=48822329>
