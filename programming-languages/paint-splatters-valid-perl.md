# 페인트 얼룩의 93%가 유효한 Perl 프로그램이라는 풍자 논문은 합격 기준이 넓으면 합격률이 정보가 아님을 보여 준다

원문: [93% of Paint Splatters are Valid Perl Programs](https://www.mcmillen.dev/sigbovik/)

HN 토론: <https://news.ycombinator.com/item?id=50459745> (497점, 64개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ivhdd6/93_paint_splatters_are_valid_perl>

GN 토론: <https://news.hada.io/topic?id=37029>

GN 토론: <https://news.hada.io/topic?id=14571>

## 요약

Colin McMillen이 쓴 풍자 논문으로, 2019년 4월 1일 피츠버그에서 열린 SIGBOVIK 2019에
채택되었다.
논문은 페인트 얼룩 사진 100장 가운데 93장이 광학 문자 인식(OCR)을 거치면 유효한 Perl
프로그램이 된다고 보고한다.
블로그 글은 논문 PDF와 얼룩마다 OCR이 읽은 코드를 모은 갤러리, 100장의 데이터셋 압축 파일을
안내한다.
SIGBOVIK은 장난스러운 학술 행사이고, 블로그는 이 논문이 진짜 결과물을 담았다고
판정된 논문에 붙는 Unwitting Participation Ribbon을 받았다고 적는다.

배경은 2019년 2월의 트위터 대화이다.
Adrienne Porter Felt가 자기 아이가 컴퓨터 프로그래밍 같은 직업 기술 대신 벽에 페인트를
칠했으면 좋겠다고 하자,
Jake Archibald가 유효한 Perl을 만들지 않고 벽에 페인트를 바르는 것이 가능하냐고
물었다.
논문은 이 질문에 가능하다고 답한다는 것이 초록의 주장이다.[^paper]

방법은 이렇다.
첫 번째 저자(논문은 이 사람을 실업자라고 부른다)가 Pinterest에서 paint splatter
wallpaper를 검색해 이미지 100장을 내려받았다.
워터마크나 합성된 글자가 겹친 이미지는 손으로 걸러 냈다.
OCR은 Tesseract 4.0.0-beta.1을 썼다.
엔진은 전통 방식(legacy), LSTM 기반, 둘을 합친 방식 세 가지이고,
쪽 분할 모드는 14가지 중 #4, #7, #8, #9 네 가지를 골라 모든 조합을 시도했다.
legacy 엔진에만 가능한 설정으로 허용 문자를 ASCII 32~126으로 제한했다.
OCR이 읽은 문자열을 Perl 5.26.1 실행 파일에 넣어 유효한 프로그램인지 확인했고,
비어 있지 않은 프로그램만 성공으로 셌다.
Perl이 유효한지는 이론적으로 결정 불가능하다는 Jeffrey Kegler의 증명을 인용해
perl 자체로 확인한다.[^paper]

결과는 100장 중 93장이 열두 조합(엔진 3개 곱하기 모드 4개) 가운데 적어도 하나에서
유효한 Perl이 되었다는 것이다.
가장 성공적인 단일 조합은 LSTM 엔진과 모드 9로 55%였다.
LSTM 엔진은 네 모드 중 하나라도 되는 경우가 74%,
legacy 엔진은 62%, 두 엔진을 합친 방식은 40%였다.
저자들은 합친 방식이 각각보다 훨씬 나쁜 이유를 모르겠다고 쓴다.[^paper]

유효한 프로그램들은 모두 시시하다.
실행해도 아무 일도 하지 않거나 값을 만들어 버린다.
논문은 `eval()`로 결과를 출력해 보았다.
숫자 리터럴이 20장이고, 가장 작은 값은 −3, 가장 큰 값은 225252이다.
나머지는 대부분 Perl의 따옴표 없는 문자열(unquoted string, 베어워드) 덕분에 유효하다.
OCR이 `ME`라고 읽으면 따옴표 없이도 문자열 `ME`가 된다.
`;` 하나만 읽힌 경우도 있고, 이것은 비어 있지 않지만 아무 값도 만들지 않는다.
어떤 OCR 해석으로도 유효하지 않은 이미지는 일곱 장이다.
Nintendo의 Splatoon 공식 이미지는 유효했지만 OCR 결과가 부적절해 싣지 않았다고 한다.[^paper]
블로그의 정오표는 `lerzfijglpFiji-j`가 Perl에서 숫자 0이 되는 것 같은, 마감 뒤에야
알아본 흥미로운 사례를 덧붙인다.

저자들이 스스로 적은 한계도 있다.
100장은 작은 데이터셋이고, 질문은 paint smear(문지른 자국)였는데 splatter(튄 자국)로
검색했고, Pinterest에서 고른 것은 누군가 저장할 만하다고 한 이미지라는 선별이 있다.
어린아이가 그린 서투른 얼룩에서 결과가 다른지도 시험하지 않았다.[^paper]

## 분석

### 중심 주장은 농담이지만 구조는 느슨한 합격 기준과 열두 번의 시도이다

가장 강하게 말하면 이 논문이 실제로 보여 주는 것은 페인트의 성질이 아니라 합격 기준의
성질이다.
유효한 Perl이라는 기준은 넓다.
숫자 하나, 따옴표 없는 단어 하나, 세미콜론 하나도 통과한다.
저자들은 여기에 열두 가지 OCR 설정을 이미지마다 모두 돌려 하나라도 통과하면 성공으로
치는 선택을 얹는다.
논문은 이 방식이 훈련, 시험, 검증 세트가 따로 없어서 매우 비윤리적이라고 스스로 쓰면서도
정직하게 밝히고 있다고 말한다.[^paper]
이 문장은 농담이지만 다중 비교의 문제를 정확히 짚는다.
기준이 넓고 시도가 많으면 합격률은 대상(페인트)이 아니라 기준과 시도 횟수를 반영한다.

### Perl이어서 93%가 나온 것이 아니라 기준이 넓어서 나왔다

논문 자신이 짚듯 숫자 리터럴로 읽히는 20장은 Perl 특유가 아니다.
−3은 Python에서도 −3이다.[^paper]
Perl 특유의 부분은 따옴표 없는 문자열이다.
HN에서 larsonian은 따옴표 없는 문자열이 셸 언어의 기본이고 Perl의 설계 목표가 셸
스크립트의 더 강력한 대체였으므로 놀라운 기능이 아니며,
`use strict`를 쓰면 이 기능이 꺼진다고 썼다.[^larsonian]
같은 현상은 다른 형식에도 있다.
layer8은 Java 속성(properties) 파일이 잘못된 유니코드 이스케이프만 아니면 어떤 문자
시퀀스도 유효하다고 했고,
hyperman1은 R 코드가 서버 응답을 CSV로 읽는데 CSV가 거의 무엇이든 유효해서 XML 오류
응답이 레코드로 해석되어 데이터베이스에 쓰레기가 들어간 일을 말했다.[^layer8][^hyperman1]
합격 기준이 구문의 유효성에 머물면 오류와 정상을 구분하지 못한다는 점에서 같은 문제이다.

같은 글이 다른 주소로 올라온 Lobste.rs 스레드(2019년과 2022년의 다른 제출 주소, 같은 논문)에서도
같은 쟁점이 나왔다.
inactive-user는 논문이 무슨 일이 일어나는지 설명하지 않는다며,
`strict`를 켜지 않으면 서브루틴으로 해석되지 않는 베어워드가 문자열이 되기 때문이라고
짚었다.[^lobsters-bareword]
`use strict`를 기본값으로 해야 하느냐는 토론도 이어졌다.
한쪽은 하위 호환 때문에 기본값이 안 된다고 했고,
다른 쪽은 `strict`가 변수를 먼저 선언하게 해서 10줄짜리 일회용 스크립트마다 한 줄을
영원히 더해야 하는 큰 변화라고 했다.[^lobsters-strict-compat][^lobsters-strict-oneliner]
gerikson은 1999년부터 Perl을 쓰면서 항상 `strict`와 `warnings`를 썼고 여러 번 도움이
되었다고 했다.[^gerikson]

### 풍자는 선별과 시도 횟수를 정직하게 적는 방식을 보여 준다

이 논문은 어떤 설정이 가장 잘 되었는지, 가장 잘 된 설정이 몇 퍼센트였는지, 시도 방식이
무엇이었는지를 숨기지 않는다.
93%라는 제목의 수치 바로 옆에 단일 설정의 55%와 엔진별 40~74%가 있다.
빈 프로그램을 성공으로 세지 않았다는 조건도 적는다.[^paper]
제목의 수치만 읽으면 놀랍지만 본문을 읽으면 그 수치가 어떻게 만들어졌는지가 다 보인다.
무엇을 숨기고 무엇을 보여 주는가의 차이를 드러내는 사례로 읽힌다.

### 무작위 문자열 기준선을 직접 재 보았다

HN의 SoraTakai는 OCR이 무엇을 쓰느냐에 달린 무의미한 결과이고
무작위 입력에서 얼마나 통과하는지의 기준선이 없다고 지적했다.[^sorataka]
논문에도 기준선은 없다.
이 문서는 그 기준선을 흉내 내 보았다.
ASCII 32~126에서 균일하게 뽑은 길이 L의 무작위 문자열을 파일로 쓰고,
`perl -c`로 구문 검사를 통과하는 비율을 쟀다.
빈 문자열(공백뿐인 것)은 제외했고 길이마다 2,000개를 뽑았다.
Perl은 이 머신의 5.34.1이다.
`strict`는 같은 문자열 앞에 `use strict; use warnings;`를 붙인 경우이다.

| 문자열 길이 | 기본 `perl -c` 통과 | `use strict` 통과 |
| ----------- | ------------------- | ----------------- |
| 1           | 66.2%               | 12.4%             |
| 2           | 53.1%               | 8.6%              |
| 3           | 42.6%               | 6.3%              |
| 5           | 30.4%               | 3.9%              |
| 8           | 18.1%               | 2.9%              |
| 13          | 9.2%                | 2.1%              |
| 21          | 6.7%                | 2.1%              |

OCR이 얼룩에서 뽑는 문자열은 대개 짧다.
논문의 예시는 `35`, `-3`, `ME`, `;`, 여섯 자리 숫자이다.
짧은 무작위 문자열은 기본 설정에서 절반 안팎이 유효한 Perl이므로,
이미지마다 열두 번씩 시도하면 93%가 크게 놀랍지 않다.
`use strict`를 붙이면 통과가 한 자릿수 퍼센트로 떨어지는 것은 larsonian이 말한
`use strict`의 효과와 맞는다.[^larsonian]
이 실험의 한계는 분명하다.
`perl -c`는 구문만 검사하고 논문은 실행 결과를 보았으며,
무작위 균일 문자열은 OCR이 뽑는 문자열의 분포와 다르고,
시도 횟수(열두 번)와 문자열 길이의 분포까지 흉내 내지는 않았다.
따라서 이 표는 논문의 93%를 재현한 것이 아니라 기준이 얼마나 넓은지의 감을 주는
기준선이다.

```python
import random, subprocess, tempfile, os
ALPHA = [chr(c) for c in range(32, 127)]

def passes(src, strict):
    prefix = "use strict; use warnings;\n" if strict else ""
    with tempfile.NamedTemporaryFile("w", suffix=".pl", delete=False) as f:
        f.write(prefix + src + "\n")
    try:
        return subprocess.run(["perl", "-c", f.name],
                              capture_output=True, timeout=10).returncode == 0
    finally:
        os.unlink(f.name)

random.seed(20261112)
strings = ["".join(random.choice(ALPHA) for _ in range(3)) for _ in range(2000)]
strings = [s for s in strings if s.strip()]
print(sum(passes(s, False) for s in strings) / len(strings))
```

## 비평

### 기준선이 없고 OCR 선택이 결과를 좌우한다

논문에는 무작위 입력에서의 통과율이 없다.
SoraTakai의 지적처럼 어느 OCR을 쓰느냐에 결과가 달려 있고,
charcircuit는 이것이 페인트가 아니라 나쁜 OCR에 관한 결과이며 더 정확한 OCR이면 전혀 다를
것이라고 썼다.[^sorataka][^charcircuit]
michaelt는 이를 거꾸로 뒤집었다.
더 정확한 OCR은 이미지에 글자가 없다고 인식할 것이고, 빈 파일(`touch temp.pl`)도
종료 코드 0으로 유효한 Perl이며,
워터마크 글자인 `stitch & shutter`도 유효한 Perl이라고 직접 실행해 보였다.[^michaelt]
논문이 빈 프로그램을 세지 않은 이유가 여기에 있다.
다만 기준선이 없다는 점은 논문의 약점으로 남는다.
ashton314는 SoraTakai의 지적에 농담의 핵심을 놓쳤다고 답했는데,
농담이라는 해석과 방법론 비판은 양립한다.[^ashton314]

### 입력 선별과 데이터셋이 작다는 한계가 결과를 좁힌다

이미지는 Pinterest에서 사람이 저장한 것이고 100장이며 워터마크가 있는 것은 손으로
뺐다.[^paper]
ideasphere는 세 번째 이미지에 있는 Stitch & Shutter 워터마크를 OCR이 놓친 것이
궁금하다고 했다.[^ideasphere]
이 문서는 그 이미지를 확인하지 않았고, 논문의 필터링 기준이 어디까지 적용되었는지도
확인하지 못했다.
michaelt는 Tesseract가 흰 배경의 검은 글자 같은 고대비 문서용이라 옅은 금색 글자가 있는
얼룩에서는 힘들 것이라고 했다.[^michaelt-tesseract]
논문은 입력 이미지의 종류를 바꿔도 결과가 같은지를 미래 연구로 남긴다.[^paper]

### 현대판으로 옮기면 합격률이 더 쓸모없어진다

silvandeboer는 현대판이 이미지를 맥락 없이 LLM에 넣고 출력을 유효한 Rust로
제한하는 것이라고 했고, spwa4는 AI를 쓰면 작은 프롬프트로 그것이 100%가 되었다고
농담했다.[^silvandeboer][^spwa4]
농담이지만 이 구조는 오늘의 평가에 그대로 있다.
코드 생성 평가에서 컴파일되는가나 유효한가는 합격 기준이 넓고, 시도를 여러 번 허용하는
방식(여러 번 뽑아 하나라도 통과하면 성공)은 이 논문이 한 선택과 같다.
이 대응은 이 문서의 해석이다.
HN의 한 댓글은 2021년 스레드 상단의 Master Foo 공안이 바이브 코딩 시대에는 다르게
읽힌다고 했는데, 이 문서는 그 공안을 열어 보지 않았다.[^adamrezich]

## 인사이트

### 어떤 X%가 통과했다는 주장을 읽을 때 다섯 가지를 묻는다

이 논문은 숫자를 읽는 연습 문제로 쓸 수 있다.
이 문서의 제안은 합격률을 읽을 때 다섯 가지를 확인하는 것이다.
합격 기준이 어디까지 넓은지, 한 대상에 몇 번 시도했는지, 빈 입력이나 무작위 입력의
기준선이 있는지, 입력이 어떻게 골라졌는지, 합격이 구문의 유효성인지 의미의 정확성인지이다.
이 다섯 질문은 이 문서의 제안이다.

### 구문의 유효성을 정상의 증거로 삼지 않는다

hyperman1의 사례처럼 구문 검증만 통과하는 파서는 오류 응답을 정상 데이터로 받아들인다.
이 문서의 제안은 외부 입력을 받는 코드에서 구문 파싱 뒤에 의미 검사(필수 열이 있는지,
값의 범위가 맞는지, 기대한 열 이름이 있는지)를 따로 두는 것이다.
Perl의 `use strict`가 베어워드를 막듯이 더 엄격한 모드가 있는 도구라면 그것을 켜는
것이 값이 싼 방법이다.
이 실험에서도 `use strict`는 통과율을 한 자릿수로 낮췄다.
이 제안은 이 문서의 적용 제안이다.

### 시도를 여러 번 허용하는 평가는 시도 횟수를 함께 적는다

이미지마다 열두 설정을 돌려 하나라도 되면 성공으로 센 이 논문은 극단적인 예이지만,
여러 번 시도해 하나라도 통과하면 성공으로 세는 방식은 실제 평가에도 흔하다.
이 문서의 제안은 그런 평가를 읽거나 쓸 때 한 번에 통과한 비율과 여러 번 허용한 비율을
나란히 적는 것이다.
이 논문은 한 문단 안에 두 비율(단일 설정 55%, 열두 설정 93%)을 모두 적어서 이 점을
지킨다.

### 이 논문의 결과를 확인할 관찰

논문의 93%가 의미 있는지는 같은 방법을 무작위 입력에 돌려 비교하면 알 수 있다.
이 문서의 실험은 균일한 무작위 문자열로 한 가장 거친 기준선이다.
OCR이 실제로 뽑는 문자열의 분포와 열두 번의 시도를 흉내 내면 더 가까운 기준선을 얻을
수 있고, 그 기준선이 93%에 가까우면 논문의 결과는 얼룩이 아니라 기준의 결과라는 뜻이다.
이 확인은 이 문서가 하지 않았고, 제안이다.

---

[^paper]: Colin McMillen and Tim Toady, [93% of Paint Splatters are Valid Perl Programs](https://www.mcmillen.dev/sigbovik/2019.pdf), 2019-04-01

[^lobsters-bareword]: <https://lobste.rs/s/odi5eu/93_paint_splatters_are_valid_perl#c_u6mn7z>

[^lobsters-strict-compat]: <https://lobste.rs/s/odi5eu/93_paint_splatters_are_valid_perl#c_tremnv>

[^lobsters-strict-oneliner]: <https://lobste.rs/s/odi5eu/93_paint_splatters_are_valid_perl#c_o5suaf>

[^gerikson]: <https://lobste.rs/s/odi5eu/93_paint_splatters_are_valid_perl#c_tgf9qe>

[^larsonian]: <https://news.ycombinator.com/item?id=50466777>

[^layer8]: <https://news.ycombinator.com/item?id=50460402>

[^hyperman1]: <https://news.ycombinator.com/item?id=50463563>

[^sorataka]: <https://news.ycombinator.com/item?id=50462724>

[^charcircuit]: <https://news.ycombinator.com/item?id=50463822>

[^michaelt]: <https://news.ycombinator.com/item?id=50464422>

[^ashton314]: <https://news.ycombinator.com/item?id=50462760>

[^ideasphere]: <https://news.ycombinator.com/item?id=50462839>

[^michaelt-tesseract]: <https://news.ycombinator.com/item?id=50464367>

[^silvandeboer]: <https://news.ycombinator.com/item?id=50463937>

[^spwa4]: <https://news.ycombinator.com/item?id=50465236>

[^adamrezich]: <https://news.ycombinator.com/item?id=50460341>
