# awesome 저장소는 낡았고 AI가 만든 PR로 쓸모가 줄고 있다

원문: [Awesome repositories are no longer awesome](https://erikgahner.github.io/posts/2026/awesome-repositories-are-no-longer-awesome/)

HN 토론: <https://news.ycombinator.com/item?id=50377821> (275점, 118개 댓글)

GN 토론: <https://news.hada.io/topic?id=36656>

## 요약

Erik Gahner Larsen이 2026년 11월 5일 쓴 블로그 글이다.
GitHub에는 이름 앞에 awesome이 붙은 저장소가 많다.
특정 분야의 지식과 자료를 골라 모아 둔 목록이며,
`awesome-python`이 그 예다.
글쓴이는 예전에 이런 저장소를 좋은 자료가 모여 있는 곳으로 보았지만
지금은 대부분 쓸모없다고 본다.
이유는 둘이고 둘 다 AI와 관련이 있다고 말한다.

첫째 이유는 목록이 오래되면 낡은 자료가 쌓인다는 것이다.
글쓴이는 필요한 자료나 영감을 얻으려면 괜찮은 AI 모델에게 묻는 편이 낫다고 쓴다.
목록이 계속 쓸모 있다면 자료를 찾고 확인하려는 에이전트에게 그렇다고 말한다.
예로 `awesome-R` 저장소를 훑어보았더니
마지막 갱신이 1년도 더 전이고 대부분의 자료가 낡았거나 R 사용자 일반의 관심사가
아니었다고 한다.
앞부분에 있는 링크 하나는 2016년 기준 다운로드 상위 패키지 50개의 개요였다고
지적한다.

둘째 이유는 이런 저장소에 AI가 만든 저질 결과물(AI slop)이 몰려든다는 것이다.
임의의 awesome 저장소에 가 보면 가장 흔한 도구와 자료를 추천하는
풀 리퀘스트(pull request, PR)가 많다고 한다.
예로 든 `awesome-free-online-tools`는 별이 13개인데 열린 PR이 91개이고,
글쓴이가 본 PR은 모두 AI로 만든 흔한 도구를 제안했다고 쓴다.
글쓴이는 자기 통계 자료 저장소에 들어온 PR을 계기로 이 현상을 알게 되었다.
그 PR을 올린 사용자는 AI로 만든 웹사이트를 최소 여섯 개 만들었고
여러 awesome 목록에 그 사이트들을 추가하자는 PR을 100건 넘게 냈다고 한다.

글쓴이는 이런 도구가 실제로 병합된 사례를 쉽게 찾았다고 말하며 PR 세 건을 든다.
반면 기본적인 확인을 한 사례도 찾았는데,
한 교육 자료 저장소는 교육자의 검토, 독립적인 검증,
학습 성과가 아직 충분히 입증되지 않았다는 이유로 PR을 닫았다.
글쓴이는 이 사례를 좋게 평가한다.
결론으로 awesome 저장소가 모두 나쁘다는 뜻은 아니며 여전히 훌륭할 수 있다고
한 걸음 물러선다.
다만 좋은 자료를 찾는 일반적인 방법으로서는 예전만 못하고,
AI가 자료와 PR을 더 잘 만들수록 더 쓸모가 줄 것이라고 예상한다.

## 분석

### 글의 주장은 서로 다른 두 가지 쇠퇴를 한 이야기로 묶는다

글은 두 가지를 말한다.
하나는 방치된 목록이 낡는다는 것이고,
다른 하나는 열려 있는 입구로 낮은 품질의 PR이 들어온다는 것이다.
앞의 것은 관리자의 시간 부족이 원인이고
뒤의 것은 누구나 PR을 낼 수 있는 구조와 PR을 거의 공짜로 만들어 주는 AI가
원인이다.
글쓴이는 둘 다 AI와 관련이 있다고 묶지만,
첫째 이유에서 AI는 낡은 목록을 대신할 선택지일 뿐이다.
낡음 자체를 만든 것은 AI가 아니다.

이 구분이 중요한 이유는 처방이 다르기 때문이다.
낡음에는 갱신이나 폐기가 처방이고,
낮은 품질의 PR이 몰려드는 문제에는 기여 조건을 높이는 것이 처방이다.
글은 처방을 말하지 않고 독자의 선택(AI에게 묻기)만 권한다.

### 낡음에 대한 증거는 확인된다

이 문서는 글이 든 사례의 일부를 GitHub API로 확인했다.
`awesome-R`의 마지막 푸시는 2025년 9월 18일이었다.[^awesome-r]
이 문서를 쓴 날(2026년 11월 5일)로부터 1년 이상 전이므로
글쓴이의 마지막 갱신이 1년도 더 전이라는 서술과 맞는다.
`awesome-free-online-tools`는 별 13개이고[^free-tools-repo]
열린 PR이 91개였다.[^free-tools-prs]
글쓴이가 제시한 수치와 일치한다.
다만 PR 내용이 모두 AI로 만든 흔한 도구라는 글쓴이의 판단은
이 문서가 PR을 읽지 않았으므로 확인하지 못했다.

### 이 글의 증거는 사례 두세 개에 의존한다

글은 `awesome-R` 하나와 `awesome-free-online-tools` 하나,
그리고 글쓴이 자신의 저장소에 들어온 PR 하나를 중심에 둔다.
글쓴이도 모든 PR을 보지는 않았다고 밝힌다.
이는 문제가 있다는 존재 증명으로는 충분하지만
대부분의 awesome 저장소가 그렇다는 일반화의 근거로는 부족하다.
글이 대부분이라고 쓰면서도 모두 나쁘지는 않다고 물러서는 이유가
거기에 있다고 읽을 수 있다.

## 비평

### 낡음은 AI 이전부터 있던 문제이고 글은 AI 시대의 변화와 섞는다

HN에서 Springtime은 기억하는 awesome 저장소 대부분이
들어 있는 도구를 직접 써 보지 않고 README만 읽은 사람이 만든 것 같다고 적었고,
이 문제가 LLM 열풍보다 몇 년 앞선다고 했다.[^Springtime]
embedding-shape는 목록이 엄선한 소프트웨어를 모으는 곳에서
관련된 모든 소프트웨어를 늘어놓는 곳으로 바뀐 때를 2015년 무렵으로 기억하며
그때 이미 스팸과 마케팅에 쓰이고 있었다고 했다.[^embedding-shape]
p-e-w는 awesome 목록을 예전의 웹 디렉터리가 현대에 되살아난 것으로 보고
디렉터리가 실패한 이유(스팸, 자기 홍보,
낡음)와 같은 이유로 실패했다고 적었다.[^p-e-w]
이 의견들은 글쓴이의 두 번째 이유(AI가 만든 PR)가 새로운 요인이 아니라
이미 있던 문제를 가속한 것일 수 있음을 보여 준다.
글은 이 구분을 하지 않으며, 어느 쪽이 맞는지는 글과 스레드가 가릴 수 없다.

### AI에게 묻는 편이 낫다는 말에는 근거가 없다

글쓴이는 괜찮은 AI 모델에게 묻는 편이 낫다고 쓰지만
AI의 답과 awesome 목록을 비교한 자료는 제시하지 않는다.
stridTastic은 시간이 흘러도 가치가 있는 자료가 있고,
이름을 아는 것만으로도 아무것도 모르는 것보다 낫다고 반박했다.[^stridTastic]
그는 AI가 같은 답을 주지 않고,
아무것도 모르는 사람을 한쪽으로 몰고 갈 수 있으며,
틀리거나 답을 거부할 수 있다고 덧붙였다.
이 반론도 비교 자료가 아니라 경험에서 나온 의견이다.

R의 경우 zaik가 더 쓸 만한 대안을 알려 주었다.
R에는 잘 관리되는 CRAN Views가 있다는 것이다.[^zaik]
글쓴이가 낡았다고 지적한 `awesome-R`은 이 분야에서 쓸 수 있는 도구의
하나였을 뿐이고
낡음이 곧 awesome 목록 전체의 쓸모 없음을 뜻하지는 않는다.
글의 논리는 이 분야 안의 다른 목록이 대신한다는 가능성을 지나간다.

xtracto는 `awesome-scalability` 같은 목록이 특정 도구를 추천하지 않고도
아직 모르는 것을 알게 해 주는 좋은 자료라고 했다.
AI는 검색 엔진과 같은 한계를 가져서,
모르는 것에 대해서는 물을 수 없다는 것이다.[^xtracto]
kevcampb는 AI 모델이 그 목록을 어디서 얻는지 궁금하다고 적었다.[^kevcampb]
두 의견은 AI에게 묻는 편이 낫다는 글의 전제를 서로 다른 쪽에서 건드린다.
앞의 것은 질문하는 사람이 대상을 모른다는 조건이고,
뒤의 것은 AI의 답이 목록 같은 자료에서 나온다는 조건이다.

### 글은 PR을 내는 쪽의 동기를 묻지 않는다

글은 한 사용자가 AI로 만든 사이트로 PR을 100건 넘게 냈다고 하지만
왜 그랬는지는 말하지 않는다.
glimshe는 AI가 인터넷에서 장난을 치는 것이 아니라
사람이 AI에게 PR을 만들게 시키는 것이라며 그 이유가 무엇인지
궁금해했다.[^glimshe]
광고인지, 이력서용 기여인지를 물었다.
Frieren은 AI 에이전트가 매우 적극적이어서
오래 돌거나 프롬프트가 일반적이면 달성할 수 없는 목표를 좇아
계속 무언가를 하려 한다고 답했다.[^Frieren]
이는 추측이다.
글쓴이가 본 사례에서 사람이 시켰는지 에이전트가 자율적으로 했는지는 알 수 없다.
이 구분이 처방에 영향을 주므로 글의 빈틈이다.

### 급증은 운영자의 증언으로 보강되지만 모두가 겪는 일은 아니다

글은 사례 두세 개에 기대지만 스레드에는 다른 목록을 관리하는 사람들의 보고가 있다.
hyperupcall은 `awesome-bash`를 수년째 돕고 있는데
최근 PR의 거의 전부가 AI로 만든 프로젝트로 가는 링크이고,
그런 프로젝트가 만들어진 지 며칠이나 몇 주 만에 별을 수백 개 얻는다고 적었다.[^hyperupcall]
vavkamil은 `awesome-bugbounty-tools`에 이렇게 많은 PR이 온 적이 없어서
별이 50개 미만인 저장소의 PR을 실패시키는 CI 검사를 넣었고,
최근 두 달 동안 닫은 PR이 지난 6년쯤 동안 병합한 PR보다 많다고 했다.[^vavkamil]
LeonB는 아주 좁은 주제의 목록인데도 몇 달째 하루에 여러 건의
엉터리 PR을 받는다고 적었다.[^LeonB]
이 증언은 글의 두 번째 이유를 뒷받침한다.

반대 사례도 있다.
dannyfritz07은 `awesome-ray-tracing`을 관리하는데
PR이 몰려드는 정도로 인기가 있지는 않은 것 같고,
최근 AI가 만든 것으로 의심되는 PR이 하나 왔지만
확인해 보니 맞는 수정이어서 병합했다고 했다.[^dannyfritz07]
well_ackshually는 `awesome-selfhosted` 관리자들이 저질 결과물과
알려지지 않은 소프트웨어를 거르려고 꽤 노력한다고 적었다.[^well_ackshually]
이 사례들은 급증이 인기와 주제에 따라 다르게 나타난다는 것을 보여 주며,
글의 일반화가 모든 목록에 해당하지는 않는다는 앞의 지적과 맞닿는다.

## 인사이트

### PR을 내는 비용과 검토하는 비용의 비대칭이 목록을 무너뜨린다

anushka_gandhi는 스패머가 AI가 만든 래퍼(wrapper)를 링크하는 PR 100개를
스크립트로 내는 데는 노력이 들지 않지만
관리자가 그것을 검토하고 거절하는 데는 사람의 노력이 든다고
적었다.[^anushka_gandhi]
이 비용의 비대칭은 awesome 목록에만 해당하지 않는다.
누구나 PR을 낼 수 있는 모든 공개 입구에 적용된다.
awesome 목록은 입구가 열려 있다는 것이 장점이었기 때문에 이 영향을 가장
먼저 받는다.

글쓴이의 사례 중 PR을 닫은 저장소는 검증 기준을 내세워 거절했다.
kdeldycke는 awesome 목록 네 개를 관리하는데 시간이 많이 들며
편집 과정을 기여 지침(contribution guidelines)으로 문서화했다고
적었다.[^kdeldycke]
kdeldycke의 방식은 기준을 미리 공개해 거절하는 비용을 줄인다.
기준이 있으면 거절하는 사람이 매번 이유를 설명하지 않아도 된다.
이는 이 문제에 대한 하나의 처방으로 생각할 수 있고,
글이 권하는 선택지(AI에게 묻기)와는 다른 방향이다.

### 거르는 일은 판단이 아니라 규칙으로 시작하는 편이 현실적이다

스레드에서 대응 방법을 두고 의견이 갈렸다.
bunderbunder는 AI에 돈을 쓰지 않아도 연결된 저장소가 하루 된 저질 결과물이
아닌지 확인하는 정도의 결정적인 스크립트로 자동 거절하고 규칙을 문서화하는
편이 낫다고 적었다.[^bunderbunder]
aftbit은 이를 이메일 스팸 필터에 비유했다.
AI가 이것이 훌륭하다고 판단해서는 안 되지만 이것은 명백한 쓰레기라고
판단하는 것은 괜찮고, PR 양식을 따르지 않으면 닫는 정도의 규칙이면 된다는
것이다.[^aftbit]
`awesome-javascript`를 2018년부터 관리해 온 gokaygurcan은
AI 문제의 해법이 더 많은 AI라고는 믿지 않으며,
목록을 훌륭하게 하는 것은 사람의 손길이라고 답했다.[^gokaygurcan]
xnx는 검증되지 않은 제출자에게는 PR을 낼 때 돈을 내게 하는 방식이
합리적으로 보인다고 적었다.[^xnx]
이 의견들은 낮은 비용의 규칙으로 명백한 잡음을 먼저 걸러 내고
남은 것에 사람의 판단을 쓰자는 쪽으로 모이지만,
규칙이 알려지면 우회될 수 있다는 반론도 스레드에 있다.
이 문서는 어느 방식이 실제로 통하는지 확인하지 못했다.

### 목록의 가치는 자료가 아니라 편집 판단에 있다

목록이 낡았다는 지적은 자료의 갱신 문제이지만
PR이 쏟아진다는 지적은 편집 판단의 문제다.
어떤 자료를 넣고 어떤 자료를 뺄지를 결정하는 것이 목록의 가치였다.
bemtevi는 일부 목록이 유용했지만 GitHub 별과 관심이 다른 일에도 쓸모가 있어서
목록이 점수 올리기의 대상이 된 것 같다고 적었다.[^bemtevi]
그는 개인적 열정 없이 형식을 따르는 후발 목록이 일반적이고 재미없어졌다고
덧붙였다.

별이나 관심이 보상이 되는 곳에서는 목록이 그 보상을 얻는 수단이 될 수 있다.
이 해석은 bemtevi의 의견을 이 문서가 확장한 것이며,
보상이 실제로 목록 품질을 해쳤다는 증거는 스레드에 없다.

### 낡은 목록이 에이전트의 입력이 된다면 오염이 AI 답변으로 옮겨 간다

글쓴이는 목록이 계속 쓸모 있다면 자료를 찾고 확인하려는 에이전트에게 쓸모 있을
것이라고 썼다.
이 문장을 그대로 따르면 에이전트가 참고하는 목록에
AI가 만든 도구가 병합될 때 그 오염이 에이전트의 추천에 들어갈 수 있다.
이는 글에 없는 이 문서의 추론이다.

글이 든 병합 사례가 사실이라면 이 경로는 열려 있다.
사람이 목록을 읽는 일은 줄어도 에이전트가 읽는 일은 늘 수 있으므로
목록의 신뢰도는 사람의 쓸모와 별개로 여전히 중요하다.
이 추론이 맞는지는 에이전트가 실제로 awesome 목록을 참고하는지,
참고한다면 얼마나 가중하는지를 봐야 확인된다.
이 문서는 그 자료를 확인하지 않았다.

---

[^awesome-r]: GitHub API, [qinwf/awesome-R](https://api.github.com/repos/qinwf/awesome-R)

[^free-tools-repo]: GitHub API, [abdessamadbettal/awesome-free-online-tools](https://api.github.com/repos/abdessamadbettal/awesome-free-online-tools)

[^free-tools-prs]: GitHub API, [Search issues: open pull requests in abdessamadbettal/awesome-free-online-tools](https://api.github.com/search/issues?q=repo:abdessamadbettal/awesome-free-online-tools+type:pr+state:open)

[^Springtime]: <https://news.ycombinator.com/item?id=50378242>

[^embedding-shape]: <https://news.ycombinator.com/item?id=50378470>

[^p-e-w]: <https://news.ycombinator.com/item?id=50378035>

[^stridTastic]: <https://news.ycombinator.com/item?id=50378022>

[^zaik]: <https://news.ycombinator.com/item?id=50378322>

[^glimshe]: <https://news.ycombinator.com/item?id=50378591>

[^Frieren]: <https://news.ycombinator.com/item?id=50378646>

[^anushka_gandhi]: <https://news.ycombinator.com/item?id=50378029>

[^kdeldycke]: <https://news.ycombinator.com/item?id=50377926>

[^bemtevi]: <https://news.ycombinator.com/item?id=50378032>

[^xtracto]: <https://news.ycombinator.com/item?id=50378955>

[^kevcampb]: <https://news.ycombinator.com/item?id=50380452>

[^hyperupcall]: <https://news.ycombinator.com/item?id=50380657>

[^vavkamil]: <https://news.ycombinator.com/item?id=50379462>

[^LeonB]: <https://news.ycombinator.com/item?id=50379834>

[^dannyfritz07]: <https://news.ycombinator.com/item?id=50384428>

[^well_ackshually]: <https://news.ycombinator.com/item?id=50380175>

[^bunderbunder]: <https://news.ycombinator.com/item?id=50379190>

[^aftbit]: <https://news.ycombinator.com/item?id=50379885>

[^gokaygurcan]: <https://news.ycombinator.com/item?id=50379487>

[^xnx]: <https://news.ycombinator.com/item?id=50385509>
