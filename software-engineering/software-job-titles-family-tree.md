# 소프트웨어 직함의 계보도

원문: [A Family Tree of Software Job Titles](https://zwischenzugs.com/2026/11/03/a-family-tree-of-software-job-titles/)

HN 토론: <https://news.ycombinator.com/item?id=50499038> (278점, 137개 댓글)

GN 토론: <https://news.hada.io/topic?id=37182>

## 요약

zwischenzugs 블로그에 2026년 11월 3일 imiell이 올린 글이다.
필자는 몇 년 동안 “Head of DevOps”였고, 그 직함 전에는 같은 일을 다른 이름으로 했으며, 이후 같은 일이 SRE로, 다시 플랫폼 엔지니어링으로 불리는 것을 보았다고 쓴다.
이 직함들이 어디서 왔는지 궁금해서 Claude의 도움으로 1940년대부터 지금까지의 소프트웨어 직함 계보도를 만들었다고 한다.
계보도 사이트와 저장소의 데이터는 열지 않았다.

계보도는 이렇게 구성된다.
직함 104개가 위의 “Computer”(기계가 아니라 사람)에서 아래의 “AI Agent / Context Engineer”까지 있고, 시간은 5년 간격 행으로 위에서 아래로 흐른다.
직함은 일곱 계열(개발, 분석·아키텍처·리더십, 운영과 인프라, 네트워크와 보안, 데이터와 AI, 품질과 시험, 지원과 고객 대면)의 색 열에 놓인다.
실선 화살표는 직함이 부모에서 자랐다는 뜻이고, 점선은 영향이나 흔한 이직 경로이다.
계보도는 Graphviz 파일 하나와 설명 JSON 파일 하나이고, 직함 추가는 노드, 시기 행, 부모 화살표의 세 가지 작은 수정이다.
날짜는 직함이 흔해진 대략의 시기이지 첫 기록이 아니고 출처가 달린 인용이 아닌 가장 좋은 추정이라고 필자가 밝힌다. 일부는 잘 알려졌지만 “c.”와 어깨 으쓱인 것이 많다고 한다.

필자가 그리면서 눈에 띄었다는 패턴 여섯 개는 다음과 같다.

- 코딩은 원래 사무직이었다: 1947년 Goldstine과 von Neumann의 글이 컴퓨터 사용을 수학자가 문제를 계획하고 코더가 기계 명령으로 옮기는 둘로 나누었고, 코딩은 낮은 지위의 사무 일로 여겨졌으며 상당수를 여성이 했다. 코딩이 결국 어렵고 창의적인 부분이 되어 코더가 프로그래머로 합쳐졌다고 쓴다. ENIAC의 첫 프로그래머 일부는 손으로 계산하던 군의 인간 계산원에서 뽑혔다고 한다.
- 직함은 쪼개졌다가 다시 합쳐진다: 1993년 무렵의 웹마스터는 HTML을 쓰고 웹서버를 돌리고 이메일에 답하고 사이트를 살려 두는 한 사람이었다가 2000년대 중반에 거의 사라졌다. 코드는 웹 개발자에게, 서버는 시스템 관리자에게, 내용은 편집자와 디자이너에게 갔다. 웹 개발자는 2005년 무렵 프런트엔드와 백엔드로 갈라졌다가 2008년 무렵 풀스택으로 다시 합쳐졌다.
- 어떤 직함은 오래가지 못한다: 프롬프트 엔지니어는 2023년 몇몇 고액 채용 공고로 화제였지만 모델이 나아지면서 다른 직무의 기술이 되었고 계보도에서는 AI 엔지니어로 거의 곧바로 흡수된다. 스크럼 마스터는 2010년대에 수요가 정점이었고 많은 조직이 엔지니어링 관리나 전달 역할로 접었다. 가장 새로운 직함은 “AI Agent / Context Engineer”(c. 2025)이다.
- 이름이 재활용된다: “Systems Engineer”는 계보도에서 서로 다른 두 직무이다. 1960년대 IBM에서는 고객과 설치를 설계하는 판매 전 역할이었고, 1990년대에는 Microsoft의 MCSE 자격 덕에 더 높은 수준의 설계 지향 시스템 관리자를 뜻했다. “Configuration management”는 1960년대 미국 국방의 하드웨어 변경 추적 규율에서 1970년대 소프트웨어 버전 관리가 되었다가 수십 년 뒤 Puppet과 Chef 같은 도구의 이름으로 돌아왔다.
- 새것은 흔히 옛것이다: 2025년 가장 뜨거운 직함 중 하나인 forward deployed engineer(FDE)는 OpenAI와 Anthropic을 비롯한 AI 스타트업이 고객 조직 안에서 AI를 돌리려고 채용한다. Palantir는 2010년 무렵부터 이를 중심으로 사업을 세웠고, 이는 1960년대 IBM의 시스템 엔지니어와 비슷하게 들린다고 쓴다. 옛 컨설팅과도 비슷하다고 덧붙인다.
- DevOps 논쟁이 계보도에 있다: Ben Treynor Sloss가 SRE를 소프트웨어 엔지니어에게 운영팀 설계를 맡기면 생기는 일이라고 정의했다. DevOps는 개발과 운영이 함께 일하는 문화였지만 2011년 무렵 직함이 되어 보통 자동화를 하는 사람을 가리켰다. 계보도에서 SRE와 DevOps 사이 화살표는 양방향이고, 플랫폼 엔지니어링은 둘을 부모로 두며 2022년 무렵 “DevOps의 후계자”로 팔렸다고 한다.

결말에서 필자는 1947년에는 코딩이 사무 일이고 진짜 일은 계획에 있다고 여겨졌는데, 80년 뒤 AI 때문에 코딩에 대해 같은 말이 들린다고 하며 지난번에는 코더가 어려운 부분을 하고 있었다고 쓴다.
이 화살표는 독자가 그으라고 남긴다.

## 분석

### 중심 주장은 직함이 새 일이 아니라 같은 일의 이름 바꾸기와 분할·병합이라는 것이다

여섯 패턴의 공통 논지는 직함의 변화가 일의 변화보다 느리거나 다르다는 것이다.
DevOps에서 SRE, 플랫폼 엔지니어링으로 이어지는 이름은 같은 개발과 운영의 간극에 붙는 새 이름이라는 서술이 이를 가장 잘 보여 준다.
이 해석은 필자의 것이고, 계보도의 화살표 자체가 증거가 되지는 않는다. 화살표는 필자가 그렸기 때문이다.

### 마지막 문단은 이 글의 유일한 예측이다

글의 서술은 대부분 역사이고, 결론만 AI에 관한 유추이다.
코딩이 낮은 지위의 일로 여겨졌다가 어려운 일로 판명된 역사가 되풀이될 수 있다는 암시이다.
필자는 이를 단정하지 않고 독자에게 맡긴다.

## 비평

### 날짜와 계보는 출처가 없다

필자가 스스로 날짜가 추정이고 계보를 잘못 그렸을 수 있다고 인정한다.
그래서 계보도는 가설을 시각화한 것으로 읽는 것이 맞고, 인용 가능한 역사로 쓰기에는 이르다.

### 빠진 직함과 구분이 지적된다

한 댓글은 15년 동안 가진 “Operations Manager”가 없다고 했고,[^torh]
답글은 순수 운영과 운영 관리가 계보도에서 DevOps에 가려진 것 같다고 했다.[^nikolanovak]
다른 댓글은 Webmaster와 Web Developer 사이에 흔했던 Web Designer가 빠졌다고 했고,[^chadk]
또 다른 댓글은 “Member of Technical Staff”는 어디에 속하느냐고 물었다.[^ykl]
한 댓글은 글이 “Systems Engineer”의 두 의미를 짚었지만, 소프트웨어 직무가 아닌 독립 분야인 시스템 공학과 드라이버와 커널을 쓰는 “systems software engineer”는 빠졌다고 했다.[^verall]
다른 댓글은 데이터 과학자 이전에 데이터 마이너가 있었다고 했다.[^jensgk]
필자가 직함을 104개로 한정했으므로 이 지적은 범위의 문제이고, 계보도가 불완전하다는 필자의 단서와 맞는다.

### 직함의 의미는 회사마다 다르다

한 댓글은 직함이 회사마다 다른 뜻이며 “product manager”도 그렇다고 했다.[^aurornis]
Levels.fyi 공동 창업자는 같은 직함과 등급이 회사와 산업과 시기에 따라 크게 다르다는 점이 분류 체계를 만들 때 가장 어려운 부분이라고 했다. 급여 정보를 모을 때 같은 뜻의 직함은 합치고 다른 것은 구분하며, 어떤 회사에서는 직함이 더 구체적이라는 사례도 있다고 한다.[^zaheer]
한 댓글은 자기 경력의 직함들(DevOps Engineer, Systems Development Engineer, DevOps Team Manager, Site Reliability Engineer 등)이 한 가지를 빼고는 모두 무의미했고 불확실성을 다루는 제너럴리스트를 가리켰다고 했다.[^stroebs]
이 증언들은 계보도의 한 직함이 하나의 일에 대응한다는 가정을 약하게 만든다.

### 접근성 문제가 반응의 일부였다

여러 댓글이 계보도를 보기 어렵다고 했고, 이미 있는 SVG 링크와 Ctrl+스크롤 확대법이 답으로 나왔다.[^backend_dev82]
다른 댓글은 모바일에서 확대할 수 없다고 했다.[^bluerooibos]
이는 계보도의 내용이 아니라 표현 방식의 한계이다.

### “코딩은 사무직이었다”는 서사에는 반론이 있다

한 댓글은 1947년에 코딩이 사무 일이고 진짜 일은 계획이라는 이야기가 계획자를 치켜세운다고 했다.[^kristianc]
필자는 이 서사를 AI 시대의 유추로 쓰는데, 유추의 힘은 1947년의 분업이 실제로 코딩을 낮게 보았다는 서술에 달려 있다.

## 인사이트

### 직함 논의의 실제 질문은 정체성과 시장의 두 가지이다

HN의 가장 긴 가지는 AI 시대의 직함이었다.
한 댓글은 소프트웨어를 배운 적 없이 AI로 Python 프로젝트를 공개하는 사람에게 프로젝트 관리자라는 이름을 제안했더니 불쾌해했다는 경험을 전했다. 지원하고 싶은 직군 때문에 소프트웨어 엔지니어라는 답을 원한 것 같다고 한다.[^probably_wrong]
답글은 컴퓨터과학 학위와 10년 경력이 있는 자신도 자기를 프로젝트 관리자라고 소개하기는 꺼려진다고 했고,[^pcthrowaway]
다른 답글은 그 역할이 결과는 정해졌지만 모양은 예측할 수 없는 음악 프로듀서와 비슷하다고 했다.[^julianpye]
이는 직함이 일의 설명이면서 시장에 내놓는 신호이기도 하다는 것을 보여 주고, 이 지점에서 직함이 일보다 빨리 움직이거나 느리게 움직이는 이유가 나온다.
한 댓글은 SWE가 사라지는 것이 아니라 훨씬 적게 필요해질 것이 걱정이라고 했다.[^tortasaur]

### DevOps는 직함이 아니라 원칙이라는 반복되는 주장

한 댓글은 Scrum과 Agile이 죽어 가고 DevOps는 두 능력을 갖추게 하려던 좋은 접근이었지만 사람들이 새 기술 배우기를 말만큼 좋아하지 않는다고 했다.[^siva7]
답글들은 DevOps가 전담 역할이 아니라 조직의 지도 원칙이어야 하고 모든 팀이 운영 환경과 대화하고 배포하고 관찰할 수 있어야 한다고 했고,[^nkmnz]
다른 답글은 개발과 운영은 서로 다른 생활 방식이며 운영에는 대기 순번과 상황실이 따른다고 했다.[^makeitdouble]
한 댓글은 규모가 커지면 도구와 인프라를 최적화하는 전담 DevOps 엔지니어가 필요하다고 맞섰다.[^groestl]
필자가 말한 “Dev/Ops 간극은 이름만 바뀐다”는 서술이 이 논쟁이 되풀이되는 모습과 맞는다.

### 확인할 관찰

이 계보도의 가치를 가를 관찰은 세 가지이다.
날짜와 계보에 출처가 붙어 독자가 검증할 수 있는지,
빠졌다고 지적된 직함이 추가되는지,
“AI Agent / Context Engineer” 같은 새 직함이 몇 년 뒤에도 독립된 직함으로 남는지이다.

---

[^torh]: <https://news.ycombinator.com/item?id=50499562>

[^nikolanovak]: <https://news.ycombinator.com/item?id=50499622>

[^chadk]: <https://news.ycombinator.com/item?id=50500776>

[^ykl]: <https://news.ycombinator.com/item?id=50500949>

[^verall]: <https://news.ycombinator.com/item?id=50501062>

[^jensgk]: <https://news.ycombinator.com/item?id=50500759>

[^aurornis]: <https://news.ycombinator.com/item?id=50500482>

[^zaheer]: <https://news.ycombinator.com/item?id=50501000>

[^stroebs]: <https://news.ycombinator.com/item?id=50499468>

[^backend_dev82]: <https://news.ycombinator.com/item?id=50499322>

[^bluerooibos]: <https://news.ycombinator.com/item?id=50504350>

[^kristianc]: <https://news.ycombinator.com/item?id=50499710>

[^probably_wrong]: <https://news.ycombinator.com/item?id=50501463>

[^pcthrowaway]: <https://news.ycombinator.com/item?id=50501992>

[^julianpye]: <https://news.ycombinator.com/item?id=50504737>

[^tortasaur]: <https://news.ycombinator.com/item?id=50500644>

[^siva7]: <https://news.ycombinator.com/item?id=50499826>

[^nkmnz]: <https://news.ycombinator.com/item?id=50500973>

[^makeitdouble]: <https://news.ycombinator.com/item?id=50500554>

[^groestl]: <https://news.ycombinator.com/item?id=50499675>
