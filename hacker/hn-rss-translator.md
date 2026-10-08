# HN RSS Translator: Hacker News를 요약하고 번역해 언어별 RSS로 내보내는 무료 서비스

> HN RSS Translator - Multilingual Hacker News Feeds (Korean, English, Japanese, and 1 more)

<https://hevinxx.github.io/hn-summary-and-translate/>

<https://github.com/hevinxx/hn-summary-and-translate>

Show GN: [HN RSS Translator - Hacker News를 AI로 요약하고 번역하는 무료 오픈소스](https://news.hada.io/topic?id=23750)

## 소개

HN RSS Translator는 Hacker News 첫 페이지 RSS를 받아 각 글을 요약하고,
여러 언어로 번역한 뒤 언어별 RSS 피드로 다시 내보내는 서비스다.
hevinxx가 만들었고, 서버 없이 GitHub Actions에서 돌며
결과물은 GitHub Pages에 올라간다.
서비스 페이지는 한국어, 영어, 일본어, 중국어(간체) 피드 네 개의 주소와
복사 버튼만 보여 주는 단순한 화면이다.
페이지가 내세우는 장점은 자동 번역, BART 모델 요약, 3시간마다 갱신,
API 키 없이 GitHub 인프라에서 도는 무료 오픈소스, 이렇게 네 가지다.

| 언어         | 피드 주소                                                       |
| ------------ | --------------------------------------------------------------- |
| 한국어       | <https://hevinxx.github.io/hn-summary-and-translate/rss-ko.xml> |
| 영어         | <https://hevinxx.github.io/hn-summary-and-translate/rss-en.xml> |
| 일본어       | <https://hevinxx.github.io/hn-summary-and-translate/rss-ja.xml> |
| 중국어(간체) | <https://hevinxx.github.io/hn-summary-and-translate/rss-zh.xml> |

저장소는 2025년 10월 12일에 만들어졌고 MIT 라이선스다.
코드 커밋은 10월 16일이 마지막이며, 그 뒤로는 배포 커밋만 쌓였다.
`gh-pages` 브랜치의 배포 커밋은 2026년 10월 7일 기준 2,585개다.
저자는 2025년 10월 19일 GeekNews에 Show GN 글을 올려,
긴 영문 글을 매번 읽기 버거워서 만들었다고 소개했다.
이 글은 25점을 받았고 댓글은 4개다.
글은 RSS 리더로 구독하는 방법과 함께,
Slack에서 `/feed subscribe` 명령에 한국어 피드 주소를 넘겨
받아 보는 방법을 적었다.
jiwonio는 Slack으로 받아 보겠다고 답했고,[^jiwonio]
yangeok은 이것을 Slack 봇으로 배포할 생각이 있는지 물었지만
답글은 없다.[^yangeok]

같은 저장소에는 한국어로 쓴 기획서 `PRD.md`와 구현 계획 `WORKFLOW.md`,
Claude Code용 `CLAUDE.md`가 함께 있다.
기획서는 목표를 무료 AI 라이브러리와 GitHub 인프라만으로
완전 무료로 운영하는 것이라고 적는다.

## 동작 방식

### 파이프라인

Show GN 글이 요약한 흐름은 다음과 같고, `main.py`의 순서도 같다.

```text
HN RSS → 웹 크롤링 → BART 요약 → Google 번역 → RSS 생성 → GitHub Pages 배포
```

| 단계 | 모듈                | 하는 일                                                        |
| ---- | ------------------- | -------------------------------------------------------------- |
| 수집 | `src/fetcher.py`    | `feedparser`로 HN RSS를 읽고 24시간 이내 항목을 최대 30개 고름 |
| 중복 | `src/utils.py`      | 캐시에 있는 링크와 같은 URL을 빼고 새 항목만 남김              |
| 추출 | `src/scraper.py`    | 링크된 페이지를 5개씩 병렬로 받아 본문을 최대 5,000자 추출     |
| 요약 | `src/summarizer.py` | `facebook/bart-large-cnn`으로 50~150 토큰 요약                 |
| 번역 | `src/translator.py` | `deep-translator`의 `GoogleTranslator`로 제목과 요약을 번역    |
| 생성 | `src/generator.py`  | 언어별 RSS 2.0 XML, 색인 페이지, `sitemap.xml`, `robots.txt`   |

HN RSS의 `description`은 댓글 링크 하나뿐이므로,
요약할 본문은 반드시 원문 페이지를 직접 긁어 와야 한다.
스크레이퍼는 `article`이나 `main` 태그를 먼저 찾고,
`content`, `article`, `post` 같은 클래스 이름을 가진 `div`,
50자가 넘는 문단 묶음, GitHub·Medium·arXiv 전용 규칙 순으로 내려간다.
마지막에는 페이지 전체 텍스트를 쓰며, 200자가 안 되면 실패로 본다.

요약 모델은 BART를 Hugging Face `transformers` 파이프라인으로 CPU에서 돌린다.
입력은 약 4,096자에서 자르고, 모델을 불러오지 못하면
`sshleifer/distilbart-cnn-12-6`을 시도한다.
그것마저 실패하면 단어 빈도로 문장 세 개를 고르는 추출 요약으로 내려간다.
번역 제공자는 설정에서 `google`, `libre`, `mymemory` 중 하나를 고를 수 있고,
기본값은 `google`이다.
영어 피드는 `skip_translation`으로 번역을 건너뛰고
원문 제목과 요약을 그대로 쓴다.

### 갱신 주기와 캐시

워크플로 `update-rss.yml`은 cron `0 */3 * * *`로 3시간마다 돌고,
수동 실행과 `main` 브랜치의 코드 변경에도 반응한다.
Hugging Face 모델 디렉터리와 처리 결과 `cache/`를 Actions 캐시에 보관해
다음 실행이 이어받는다.
처리한 항목은 `processed_items.json`에 7일 동안 남고,
요약과 번역은 원문의 MD5 해시를 키로 `summaries.pkl`,
`translations.pkl`에 쌓인다.
결과물은 `peaceiris/actions-gh-pages`로 `gh-pages` 브랜치에 통째로 덮어쓴다.

README는 실행 한 번에 10~20분, 한 달에 약 480분이 든다고 계산했다.
최근 실행 기록을 보면 RSS 갱신 작업은 3~4분 만에 끝났다.
다만 실제 실행 간격은 3시간이 아니었다.
10월 5일부터 7일 사이 예약 실행은 UTC 21:49, 05:00, 12:47, 19:58, 00:21에
시작해 간격이 4~8시간이었다.

### 피드에 담기는 것

피드 하나는 RSS 2.0 채널이고 제목은 `Hacker News - Korean` 같은 형식이다.
항목마다 번역된 제목, 원문 링크, HN 댓글 링크, 발행 시각이 들어가며,
설명에는 다음 순서로 내용이 붙는다.

```text
📝 <번역된 요약>

🔤 Original: <원문 제목>   (번역된 제목이 원문과 다를 때만)
📊 Score: <점수> points     (점수가 있을 때만)
🔗 Read more: <원문 링크>
```

XML 맨 앞에 XSLT 스타일시트 지시문을 넣어,
브라우저로 피드 주소를 열면 사람이 읽을 수 있는 화면으로 보인다.
점수 줄은 HN RSS 설명에서 `points`를 찾아 만드는데,
HN RSS에는 점수가 없으므로 지금 피드에서는 나타나지 않는다.
요약을 만들지 못한 항목은 설명 없이 제목과 링크만 실린다.

새 항목이 있으면 그 실행에서 새로 처리한 항목만 피드에 들어가고,
새 항목이 없을 때만 캐시에서 최근 항목을 꺼내 피드를 다시 만든다.
그래서 피드는 누적 목록이 아니라 직전 실행의 결과물이다.
과거 배포본을 표본으로 보면 한국어 피드의 항목 수는 2개에서 12개 사이였고,
2026년 10월 7일 배포본은 21개였다.

## 지금의 상태

### 번역이 멈췄다

2026년 10월 7일 00:25 UTC 배포본을 받아 보면,
한국어, 일본어, 중국어 피드 모두 21개 항목의 제목과 요약이 영어 그대로다.
네 피드의 내용이 영어 피드와 사실상 같고, `🔤 Original` 줄도 하나도 없다.
`gh-pages` 브랜치의 과거 배포본을 표본으로 확인하면,
2025년 10월부터 2026년 8월 23일 09:26 UTC 배포본까지는
한국어 피드 항목이 모두 한국어로 번역되어 있었다.
2026년 8월 24일 15:38 UTC 배포본부터는 표본으로 본 모든 배포본에서 번역이 없다.
그 사이 코드는 바뀌지 않았으므로 원인은 번역 경로 바깥에 있다고 보는 것이
자연스럽지만, 실행 로그는 확인하지 못했으므로 정확한 원인은 알 수 없다.

### 실패가 성공으로 보이는 구조

번역이 멈춰도 워크플로는 계속 성공으로 끝난다.
`translator.py`는 번역 중 예외가 나거나 결과가 원문과 같으면
경고 로그만 남기고 원문을 돌려준다.
`main.py`는 그 결과를 번역문으로 여겨
`translations.pkl`과 처리 항목 캐시에 저장한다.
피드 검증 단계는 XML이 올바른지만 보므로,
한국어 피드가 영어로 채워져도 검사를 통과한다.

이 구조 때문에 번역 경로가 되살아나도 이미 처리한 항목은 다시 번역되지 않는다.
처리 항목은 URL로 중복을 거르므로 7일 캐시가 만료될 때까지는 영어로 남고,
요약문 단위의 번역 캐시에도 영어 문장이 번역 결과로 남는다.
이 부분은 코드를 읽고 내린 해석이며, 직접 실행해 확인하지는 않았다.

### 요약의 품질

BART 요약은 추출된 본문이 깨끗할 때만 쓸 만하다.
10월 7일 피드에서 OpenAI의 Decisions API 문서는
표의 머리글과 가격 문구가 섞인 요약이 되었다.
요약은 `How decisions work A request has three parts: Field Purpose model`로
시작해 `Design services$1,200.`으로 끝난다.
GitHub 저장소를 가리키는 항목은 BibTeX 인용 블록이 그대로 요약으로 들어갔다.
21개 항목 중 3개는 요약 없이 실렸다.
`bart-large-cnn`은 뉴스 기사 요약 데이터로 학습한 모델이라,
문서 페이지, 저장소, 랜딩 페이지처럼 HN에 자주 올라오는 형식과는 잘 맞지 않는다.
이 마지막 문장은 모델 이름에서 끌어낸 해석이다.

## 직접 운영하기

README와 Show GN 글이 안내하는 방법은
저장소를 포크해 자기 계정에서 돌리는 것이다.

1. 저장소를 포크한다.
2. Settings › Actions › General에서 모든 액션 실행을 허용한다.
3. `config.yaml`의 `target_languages`에 원하는 언어를 넣는다.
4. Settings › Pages에서 `gh-pages` 브랜치를 배포 원본으로 고른다.
5. Actions 탭의 Update RSS Feeds에서 Run workflow를 누른다.

워크플로는 실행할 때 `config.yaml`의 `base_url`을 저장소 주인과 이름으로 고쳐
쓰므로, 포크한 저장소에서는 이 값을 손댈 필요가 없다.
기본 설정은 다음과 같다.

```yaml
summarization:
  model: "facebook/bart-large-cnn"   # 느리면 "sshleifer/distilbart-cnn-12-6"
  max_length: 150
  min_length: 50

translation:
  provider: "google"                 # google, libre, mymemory
  target_languages:
    - code: "ko"
      name: "Korean"
      feed_name: "rss-ko.xml"

filtering:
  max_items: 30                      # Actions 실행 시간을 줄이려면 낮춘다
  max_age_hours: 24
  skip_jobs: false                   # Ask HN, Show HN 중 채용 글 제외

output:
  keep_days: 7                       # 처리 항목 캐시의 보관 기간
  generate_index: true
```

로컬에서는 `python main.py`로 전체를 돌리고,
`python main.py --test`는 항목을 3개로 줄여 실행한다.
테스트는 `pytest tests/ -v`이며 수집기, 생성기, 스크레이퍼 테스트가 있다.
이 문서를 쓰며 로컬 실행이나 포크 배포는 해 보지 않았다.

## 트레이드오프

### 무료 인프라는 가격 대신 신뢰성을 내준다

이 서비스의 설계 목표는 돈을 한 푼도 쓰지 않는 것이다.
요약은 공개 모델을 Actions 러너의 CPU에서 돌리고,
번역은 README 표현대로 API 키가 필요 없는 Google 번역을
`deep-translator`로 부른다.
그 대가로 번역 경로는 서비스 제공자와 아무 계약이 없는 상태가 된다.
계약된 유료 API라면 장애를 알리는 통로라도 있겠지만,
지금 구조에서는 번역이 멈춰도 알려 주는 쪽이 없다.
2026년 8월 말 이후의 피드가 그 결과를 보여 준다.
계약과 알림에 관한 이 문단의 판단은 구조에서 끌어낸 해석이다.

예약 실행도 같은 성격이다.
GitHub Actions의 cron은 정해진 시각을 보장하지 않으며,
이 저장소에서도 3시간 간격이 4~8시간으로 늘어났다.
HN 첫 페이지는 몇 시간이면 크게 바뀌므로,
간격이 벌어진 사이에 올라왔다 내려간 글은 피드에 한 번도 실리지 않을 수 있다.
수집 단계가 실행 시점의 RSS만 보기 때문이다.

### 로컬 요약 모델은 비용이 없지만 품질의 상한이 낮다

BART는 API 키도 호출 비용도 없고, 1.6GB 정도의 모델을 캐시해 두면
실행도 몇 분이면 끝난다.
그러나 요약 모델은 받은 텍스트가 본문인지 잡음인지 가리지 못하므로,
본문 추출이 잘못되면 메뉴, 표, 인용 블록이 그대로 요약문에 들어간다.
LLM API를 쓰면 이런 잡음을 걸러 낼 여지가 커지지만,
그 순간 API 키와 비용이 생겨 포크해서 바로 쓰는 구조가 무너진다.
무료와 품질 사이에서 이 프로젝트는 무료를 골랐고,
그 선택은 README와 기획서에 분명히 적혀 있다.

### 요약 다음에 번역하는 순서

이 파이프라인은 영어로 요약한 뒤 그 요약만 번역한다.
번역할 글자 수가 150토큰 안팎으로 줄어 번역 호출이 가볍고,
영어 피드는 번역 없이 같은 요약을 쓸 수 있다.
대신 요약에서 생긴 오류가 번역에 그대로 전달되고,
깨진 영어 요약은 번역을 거치면 원래 무엇이 깨졌는지 알아보기가 더 어려워진다.
원문 제목은 `🔤 Original` 줄로 남지만 원문 요약은 남지 않으므로,
번역 피드 독자는 번역 품질을 영어 원문과 대조할 방법이 링크를 여는 것밖에 없다.

## 함정

- 한국어, 일본어, 중국어 피드를 구독해도 2026년 8월 24일 무렵부터는 영어 제목과 영어 요약이 온다. 피드 주소만 보고 번역이 된다고 기대하면 안 된다.
- 워크플로의 초록 체크는 번역 성공을 뜻하지 않는다. 번역 실패는 경고 로그로만 남고, 피드 검증은 XML 형식만 본다.
- 번역 실패 결과가 캐시에 저장되므로, 번역 경로가 고쳐져도 이미 처리한 항목은 최대 7일 동안 영어로 남는다.
- 피드는 직전 실행에서 새로 처리한 항목만 담는다. RSS 리더가 갱신을 오래 놓치면 그 사이 항목은 이미 피드에서 빠져 있을 수 있다.
- 요약이 없는 항목은 설명 없이 제목만 온다. 스크레이퍼가 본문을 200자 이상 얻지 못한 경우다.
- 피드 설명의 점수 줄은 코드에만 있고, HN RSS에 점수가 없어 실제로는 나오지 않는다.
- 포크해서 운영하면 이 모든 문제를 그대로 물려받는다. 특히 번역 제공자를 `libre`로 바꾸면 코드에 하드코딩된 공개 인스턴스 주소를 쓰므로, 그 인스턴스가 살아 있는지 먼저 확인해야 한다.

## 기억할 원칙

### 조용히 원문을 돌려주는 폴백은 장애를 숨긴다

번역에 실패하면 원문을 돌려준다는 선택은
한 항목의 실패가 전체 실행을 멈추지 않게 하려는 합리적인 방어다.
문제는 그 폴백의 결과가
성공한 번역과 같은 자리에 같은 형식으로 저장된다는 점이다.
그 순간 실패는 데이터가 되어 캐시에 남고,
워크플로, 피드 검증, 피드 독자 누구도 차이를 구별하지 못한다.
이 저장소에서는 그 상태가 6주 넘게 이어졌다.

폴백을 두려면 폴백이 일어났다는 사실도 함께 남겨야 한다.
번역 결과가 원문과 같은 항목이 일정 비율을 넘으면 실행을 실패로 표시하거나,
실패한 결과는 캐시에 넣지 않는 것만으로도 이 사고는 드러났을 것이다.
무료 외부 서비스에 기대는 자동화일수록,
그 서비스가 말없이 멈출 때 무엇이 보이는지를 먼저 설계해야 한다.

Hacker News 데이터를 다루는 다른 도구로는 `hacker/hn-trends-18years.md`가 있다.

---

[^jiwonio]: <https://news.hada.io/topic?id=23750#cid45667>

[^yangeok]: <https://news.hada.io/topic?id=23750#cid45580>
