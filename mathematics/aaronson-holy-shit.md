# 복잡도 이론의 연이은 AI 증명

원문: [HOLY SHIT HOLY SHIT HOLY SHIT HOLY SHIT](https://scottaaronson.blog/?p=10379)

HN 토론: <https://news.ycombinator.com/item?id=50646108> (2033점, 1877개 댓글)

GN 토론: <https://news.hada.io/topic?id=37850>

## 요약

이론 컴퓨터과학자 Scott Aaronson이 2026년 11월 25일 블로그에 올린 글이다.
제목은 같은 감탄사를 네 번 반복하며,
저자는 이전의 글과 팟캐스트가 지금 벌어지는 일의 크기를 충분히 전하지 못했다고
느껴 다시 쓴다고 한다.
이 문서는 글이 전하는 내용을 정리한 것이고, 각 성과는 저자가 전하는 대로 옮겼다.

저자는 전날 저녁 손님을 초대한 자리에서 연이어 들어온 소식을 적는다.

| 소식                                               | 저자의 설명                                                            |
| -------------------------------------------------- | ---------------------------------------------------------------------- |
| OpenAI와 Anthropic의 VP ≠ VNP 증명                 | Alpöge와 Anthropic의 리만 가설 증명 직후라 이미 지난주 일처럼 느껴진다 |
| 행렬 곱셈 지수 ω가 정확히 9/4라는 OpenAI의 주장    | 10월 6일 발표한 상계와 맞는 하계이고 답이 유리수라는 점이 충격이다     |
| 푸리에 변환의 선형 게이트 수가 N(log N)^(1/2+o(1)) | 1960년대의 FFT보다 상계가 좋아지고 하계도 일치한다                     |
| Yupan Liu의 QIP(2) = PSPACE                        | 2025년이면 그해 최고 성과였을 결과인데 AI 사용이 눈에 띄지도 않았다    |

저자는 두 가지 충격을 구분한다.
하나는 수십 년 된 핵심 질문의 답이 드디어 나왔다는 것이고,
더 큰 충격은 AI가 ω > 2 같은 하계를 증명할 수 있었다는 것이다.
그는 이 과제가 P ≠ NP보다 훨씬 쉬울 것이라고는 기대하지 않았다고 쓴다.
한 개의 풀이가 아니라 “복잡도 이론의 우주”라는 새 대륙이 한꺼번에 드러나고
있다는 비유도 든다.
회사들이 보도자료 없이 GitHub 저장소에 논문을 올리는 것이 지금의 방식이라고도
쓴다.
그는 처음으로 P ≠ NP의 증명이 멀지 않다는 확신이 든다고 말한다.

글의 마지막은 세 가지 요청과 경고다.
AI 회사를 미워하든 반기든 일어나는 일을 부정하지 말라는 것,
Lean 인증이 나온 뒤에는 Lean과 비형식 증명의 사소한 불일치나 쓰이지 않은 구간을
들어
문제가 풀리지 않았다고 주장하지 말라는 것,
암호에 관해서는 연구소들이 “하나 이상의 폭탄”을 쥐고 있다고 믿지만 세부는
확인하지 못했고 소문을 퍼뜨리지 않겠다는 것이다.
“지금은 내가 상상해 온 AI 특이점의 시작과 같은 느낌”이라고 쓰되,
지구 전체가 아니라 어려운 수학 문제에 관한 특이점으로 그치기를 바란다고 한다.
11월 26일 추가 글에서는 쓰이지 않은 증명 구간을 이유로 증명이 무효라는 주장이
퍼졌다고 적고,
Lean 검증기에 실제 오류가 있다는 증거를 내놓든지 그만두라고 쓴다.
일상에 미치는 직접 영향은 없을 것이지만 AI 자체의 존재가 경제 전반에 큰 의미를
가진다고도 덧붙인다.

## 분석

### 기준의 이동

글의 가장 구체적인 주장은 연구 수준에 대한 기준이 바뀌었다는 것이다.
저자는 Yupan Liu의 결과를 예로 들어
2025년에는 한 해의 대표 성과였을 것이 이제는 기억해야 할 정도의 사건이 되었다고
말한다.
이 비교는 저자의 기억에 기대고 있어서 다른 해와 비교한 자료는 글에 없다.
다만 사건이 하루 안에 연달아 보도된다는 상황 설명은 글의 분위기를 이해하는
열쇠다.

### 검증이 근거가 되는 구조

저자가 “회사에서 직접 나온 증명은 반대 정보가 없는 한 옳다”를 작업 가정으로 삼는
근거는 Lean 인증이다.
인증이 있으면 비전문가의 이의 제기가 증명을 무너뜨리기 어렵다는 논리다.
HN에서 yewenjie가 인용한 암호 관련 문단에 xoa가 답한 것도 같은 맥락으로,
“암호가 깨진다”는 말은 구체적이지 않으면 의미가 없다는
지적이다.[^yewenjie][^xoa]
저자 자신도 암호 소문은 확인된 바가 없다고 거리를 둔다.

## 비평

### 자기 이해관계의 위치

HN에서 utopiah는 Lean과 MathLib, 계산 자원만 있고 생성형 AI가 없었다면 얼마나
가능했을지,
대기업이 마케팅 목적으로 계산 비용을 대는 지금과 시점이 우연히 겹친 것은 아닌지
물었다.[^utopiah]
reasonableklout은 “무차별 대입보다 조금 빠른 정도”라는 폄하가 과소평가이고
Claude Code가 프로그램을 쓰는 일을 무차별 대입이라 하지는 않을 것이라고
답했다.[^reasonableklout]
다만 글이 성과를 낸 회사들과 저자의 관계를 따로 밝히지 않으므로
그 거리가 평가에 영향을 주는지는 독자가 가려야 한다.

### 수학에서 세상으로의 비약

jsLavaGoat는 AI가 공리적이고 선험적인 수학에서 뛰어나다는 것이
다른 분야를 “풀” 것이나 SF의 역할을 한다는 것으로 이어지지 않는다고
썼다.[^jsLavaGoat]
alkonaut는 리만 가설 증명과 P ≠ NP가 AI와 수학에서는 큰 성과여도
보통 사람에게는 당장 의미가 없지 않느냐고 물었다.[^alkonaut]
dreambuffer는 6개월 뒤 세상의 대부분이 거의 그대로일 것이라는 데 전 재산을
걸겠다고 했고,
이에 dude250711은 편한 반대 예측의 기간이 이제 6개월이냐고
되받았다.[^dreambuffer][^dude250711]
저자도 글에서 일상에 대한 직접 영향은 없다고 인정하고 있어서,
이 비판은 글과 충돌하기보다 글이 약하게 다룬 부분을 가리킨다.

### 암호에 대한 반론

nickysielicki는 연구소들이 지금 암호를 깨는 기법을 가졌다는 증거가 없고,
커진 조직에서 그런 비밀을 지키기도 어렵다고 반론했다.[^nickysielicki]
저자는 이를 “복수의 신뢰할 만한 출처”에서 들었다고 하고 구체적 근거는 밝히지
않는다.
이 대립은 어느 쪽도 공개된 증거가 없다.

## 인사이트

### 어느 정도의 놀람이 적절한가

Nevermark는 인간은 이 정도의 놀람을 느끼도록 진화하지 않았다고 썼고,[^Nevermark]
olalonde는 디지털 “생명”을 만드는 것이 아니라서 걱정이 덜하다고
답했다.[^olalonde]
pixl97은 저자의 “우리 구석의 특이점이기를”이라는 문장을 인용하며
이것이 검증 가능한 과제에 머물기를 바랄 수밖에 없다고 썼고,
hn_throwaway_99는 Yann LeCun이 이것이 특이점이라면 아주 이상한 특이점이라고
답했다고 전했다.[^pixl97][^hn_throwaway_99]
이 논쟁은 사건의 크기에 대한 합의가 아니라 크기를 재는 단위가 없다는 것을 보여
준다.

### 인간 수학의 끝인가, 새 영역의 시작인가

rufuspollock은 이것이 인간 수학의 끝이며 화학에서 새 원소를 합성하는 일보다
인간 화학이 끝나는 것에 가깝다고 썼다.[^rufuspollock]
jameshart는 새 원소 발견이 광석을 뒤지는 일에서 합성으로 바뀐 비유를 들었고,
codethief는 수학에서는 새 원소를 만드는 것이 곧 게임 전체라는 점이 다르다고
했다.[^jameshart][^codethief]
이 대조는 “AI가 해 준다”의 결과가 연구자의 역할을 없애는지 바꾸는지에 대한 입장
차이다.
이 저장소의 `mathematics/mathocalypse.md`와
`mathematics/future-of-mathematics.md`가 같은 질문을 다룬다.

---

[^yewenjie]: <https://news.ycombinator.com/item?id=50646311>

[^xoa]: <https://news.ycombinator.com/item?id=50646626>

[^utopiah]: <https://news.ycombinator.com/item?id=50647274>

[^reasonableklout]: <https://news.ycombinator.com/item?id=50647488>

[^jsLavaGoat]: <https://news.ycombinator.com/item?id=50650600>

[^alkonaut]: <https://news.ycombinator.com/item?id=50653301>

[^dreambuffer]: <https://news.ycombinator.com/item?id=50648459>

[^dude250711]: <https://news.ycombinator.com/item?id=50648689>

[^nickysielicki]: <https://news.ycombinator.com/item?id=50651547>

[^Nevermark]: <https://news.ycombinator.com/item?id=50650666>

[^olalonde]: <https://news.ycombinator.com/item?id=50651422>

[^pixl97]: <https://news.ycombinator.com/item?id=50647096>

[^hn_throwaway_99]: <https://news.ycombinator.com/item?id=50647329>

[^rufuspollock]: <https://news.ycombinator.com/item?id=50647109>

[^jameshart]: <https://news.ycombinator.com/item?id=50646685>

[^codethief]: <https://news.ycombinator.com/item?id=50646832>
