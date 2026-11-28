# ONNX Runtime의 GitHub 저장소 삭제

<https://onnxruntime.ai/>

<https://github.com/microsoft/onnxruntime>

HN 토론: <https://news.ycombinator.com/item?id=50539610> (350점, 74개 댓글)

GN 토론: <https://news.hada.io/topic?id=37390>

## 소개

ONNX Runtime은 Microsoft가 만든 오픈소스 머신러닝 추론과 학습 가속기이다.
저장소가 공개된 상태에서 사라졌다는 소식이 HN과 GeekNews에 올라왔다.
삭제 이유에 대한 Microsoft의 공식 설명은 읽은 범위에서 찾지 못했다.
이 문서의 대상은 글이 아니라 저장소와 그 사라짐이어서, 출처 줄에는 주소만 두었다.

읽은 시점에 확인한 상태는 다음과 같다.

- 프로젝트 사이트: `onnxruntime.ai`는 200으로 열리고 상단 메뉴의 GitHub 링크가 여전히 사라진 저장소를 가리킨다. 사이트는 이 엔진을 에지 머신러닝용 프로덕션급 AI 엔진이라고 소개하고 `pip install onnxruntime`을 안내한다.
- PyPI: `onnxruntime` 패키지는 열리고 버전 1.32.0이며, 다운로드 항목이 같은 GitHub 태그 주소를 가리킨다.[^pypi]
- 보존본: Wayback Machine에 2026년 11월 13일 캡처가 있다. 캡처의 README는 이 프로젝트를 크로스 플랫폼 추론과 학습 머신러닝 가속기로 소개하고, PyTorch, TensorFlow, scikit-learn 등을 지원하며, 훈련은 다중 노드 NVIDIA GPU에서 변환기 모델의 학습 시간을 줄일 수 있다고 한다. 라이선스는 MIT이고 데이터 및 텔레메트리 절에 이 프로젝트가 사용 데이터를 Microsoft에 보낼 수 있다고 적혀 있다.[^wayback]
- 포크: `intel/onnxruntime`은 열린다. HN에서 가장 앞선 포크로 지목되었고 OpenVINO 수정이 들어 있다고 했다.[^heliodex]

## 분석

### 중심 사건은 널리 쓰이는 의존성이 예고 없이 사라진 것이다

HN에서 한 사용자는 이날 아침 평가 파이프라인이 실패하면서 알았고, 22,000개의 별이 있는 저장소가 사전 경고 없이 어두워진 이유를 아는 사람이 있느냐고 물었다.[^nvader]
다른 사용자는 모든 것을 벤더링하는 이유가 이것이며 언제 사라질지 모른다고 했고,[^dangoodmanut] 이에 대해 이 상황에서는 벤더링한 버전도 신뢰하지 않는 편이 낫겠다는 반응이 나왔다.[^kirindave]
저장소의 별 수 22,000은 댓글 작성자의 서술이다.
이 정리는 스레드의 반응을 이 문서가 묶은 것이다.

### 추측이 갈리고 확인된 이유는 없다

원인에 대한 추측이 여러 개 나왔다.
공급망 공격으로 침해된 뒤의 정리라는 추측,[^fesbercluck][^hiddenvulkcan]
Microsoft GitHub 조직의 관리자 계정이 침해되었으리라는 추정,[^magnio]
반대로 Microsoft Ignite 기간 중 저장소를 통합하는 것일 수 있다는 의견,[^codecompost]
Phrack 최근호가 다룬 머신러닝 백도어 연구와 연결 짓는 질문,[^spdustin]
새 AI 모델 출시와 관련이 있느냐는 질문이 있었다.[^axodouble]

## 비평

### 이 문서는 사건의 원인과 범위를 단정하지 못한다

같은 시기의 다른 사건과 연결 짓는 댓글은 시간적 일치에 기댄 추측이다.

### 대체 경로의 신뢰 문제가 따른다

사라진 저장소를 대신하는 포크와 미러가 여럿 나왔다.
HN에서 한 사용자는 `syntax-syndicate`의 포크를, 다른 사용자는 Sourceforge 미러를 소개했고,[^tokyovigilante][^jcelerier] 또 다른 사용자는 Wayback 캡처의 커밋 해시를 대조해 남은 정당한 포크로 보인다고 했다.[^cookiengineer]
침해 가능성이 거론되는 상황에서 어떤 포크를 신뢰할지는 별도의 검증이 필요하다.

### 프로젝트에 대한 기존 불만이 섞여 있다

HN에서 한 사용자는 최근 개발이 느려서 몇 달 전에 떠났다고 했고,[^these] 다른 사용자는 투자가 정체된 듯하고 CPU 전용 모델의 성능이 손으로 최적화한 코드에 뒤처졌다고 했다.[^gluber]
이는 이번 사건의 설명이 아니라 프로젝트의 평가이며 개인의 인상이다.

### 텔레메트리 논쟁은 별개 주제이다

HN에서 한 사용자는 ONNX가 애플리케이션에 대한 데이터를 자동으로 보내고 소스에서 텔레메트리를 끄고 빌드하는 것 외에는 거부할 방법이 없다고 주장했다.[^eddythompson80]
이에 대해 `onnxruntime.disable_telemetry_events()`가 되지 않느냐는 반문이 있었다.[^henryteeare]
README의 데이터 절은 Microsoft에 데이터를 보낼 수 있다고만 쓴다.

### 외부 반응

HN 스레드는 350점 74개 댓글이다.
Lobste.rs에서는 `onnxruntime` 검색 결과 8건 가운데 이 사건의 글이 없었다.
GeekNews에는 같은 사건의 토픽이 있으나 댓글이 하나이고, 그것도 HN 댓글을 다시 모은 GN⁺ 계정의 요약이라 GeekNews 이용자의 반응은 없다.

## 인사이트

### 가져갈 것은 핵심 의존성의 사본과 대체 경로를 평소에 확보하는 일이다

이 사건의 실무적 교훈은 CI가 외부 저장소에서 직접 가져오는 의존성이 하나라도 사라지면 멈춘다는 점이다.
패키지 미러(사내 레지스트리), 벤더링, 고정된 해시와 보존본 확인이 대비가 된다.
HN에서 한 사용자는 새 버전을 2주 지나기 전에는 승격하지 않는 등 패키지 관리자 중개인을 바랐다.[^rtpg]
이는 한 사용자의 바람이며 이 문서의 적용은 사본과 대체 경로를 목록으로 만들어 두는 것이다.

### 포크로 갈아탈 때는 원본 해시와 대조한다

원본이 침해되었을 가능성이 거론되는 때에는 포크를 믿기 전에 Wayback 캡처 같은 사건 이전의 기록과 커밋 해시를 맞춰 본다.
HN에서 나온 방법이 같은 취지이다.[^cookiengineer]

### 확인할 관찰

이 사건의 해석을 가를 관찰은 세 가지이다.
Microsoft가 저장소 삭제의 이유와 복구 계획을 공식으로 밝히는지,
PyPI 패키지와 포크의 무결성에 문제가 있었는지,
같은 시기 내려간 다른 Microsoft 저장소(Agent Framework 등)와 같은 원인인지이다.

---

[^pypi]: [onnxruntime · PyPI](https://pypi.org/project/onnxruntime/)

[^wayback]: [microsoft/onnxruntime, Wayback Machine 2026-11-13 캡처](http://web.archive.org/web/20261113082932/https://github.com/microsoft/onnxruntime)

[^heliodex]: <https://news.ycombinator.com/item?id=50540243>

[^nvader]: <https://news.ycombinator.com/item?id=50539658>

[^dangoodmanut]: <https://news.ycombinator.com/item?id=50540449>

[^kirindave]: <https://news.ycombinator.com/item?id=50540499>

[^fesbercluck]: <https://news.ycombinator.com/item?id=50539668>

[^hiddenvulkcan]: <https://news.ycombinator.com/item?id=50540373>

[^magnio]: <https://news.ycombinator.com/item?id=50542350>

[^codecompost]: <https://news.ycombinator.com/item?id=50543836>

[^spdustin]: <https://news.ycombinator.com/item?id=50540135>

[^axodouble]: <https://news.ycombinator.com/item?id=50540126>

[^tokyovigilante]: <https://news.ycombinator.com/item?id=50540554>

[^jcelerier]: <https://news.ycombinator.com/item?id=50540735>

[^cookiengineer]: <https://news.ycombinator.com/item?id=50540709>

[^these]: <https://news.ycombinator.com/item?id=50541146>

[^gluber]: <https://news.ycombinator.com/item?id=50541981>

[^eddythompson80]: <https://news.ycombinator.com/item?id=50540608>

[^henryteeare]: <https://news.ycombinator.com/item?id=50541593>

[^rtpg]: <https://news.ycombinator.com/item?id=50540942>
