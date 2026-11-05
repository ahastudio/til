# C++26 국제표준안 투표 부결: Contracts를 두고 위원회와 국가 기관이 갈라섰다

원문: [C++26 DIS failed, how does C++ survive?](https://andreasfertig.com/blog/2026/11/cpp26-dis-failed-how-does-cpp-survive/)

HN 토론: <https://news.ycombinator.com/item?id=50360164> (405점, 340개 댓글)

GN 토론: <https://news.hada.io/topic?id=36576>

## 요약

C++ 표준화 위원회 위원이자 독일의 투표를 대표하는 Andreas Fertig가 2026-11-03에
올린 글이다.
글은 2026-10-23에 C++26 국제표준안(Draft International Standard,
DIS)이 부결되었다고 알린다.
12주 동안 진행된 ISO 국가 기관(National Body, NB) 투표의 선택지는 찬성,
반대, 기권이고 의견도 낼 수 있다.
저자가 아는 한 C++에서 DIS 투표가 부결된 것은 처음이다.
ISO 시스템에서 찾은 다른 부결 사례는 2006-08-11의 C++/CLI 언어 명세(ISO/IEC DIS
26926) 하나뿐이고, 그 프로젝트는 중단되었다고 한다.
저자는 자신의 검색 권한이 모든 것을 보기에 충분하지 않을 수 있다고 단서를 단다.
글은 ISO 규칙상 일부 투표는 ISO 내부용이어서 결과나 내역을 공개할 수 없다며,
이 글이 개인 견해라고 밝힌다.

부결의 이유는 NB가 낸 의견으로 볼 때 분명하다고 한다.
Contracts, 곧 함수의 사전 조건과 사후 조건을 언어 기능으로 쓰는 기능이 아직
출시할 준비가 되지 않았다고 보는 NB가 여럿이라는 것이다.
저자는 이번 일이 절차의 관행을 바꾸었다고 본다.
이전에는 새 정보가 나오거나 절차의 오류가 확인될 때만 NB가 표준에 반대표를
던졌는데, 이번에는 그렇지 않다는 것이다.
Contracts 없는 C++26을 원하는 NB는 새 정보가 있다고 주장하지만,
저자는 옛 논거를 담은 새 문서를 새 정보로 보기 어렵다고 말한다.

글은 Contracts의 역사를 짚는다.
2019년 쾰른 회의에서 C++20을 위해 다른 형태의 Contracts가 들어갔다가 같은
회의에서 빠졌고, 2020년부터 약 2024년까지 연구 그룹이 이 주제를 맡았다.
이후 언어 확장을 다루는 Evolution Working Group(EWG)에서 여러 회의에 걸쳐 논의한
뒤 다수결로 C++26에 포함되었다.
2026년 3월에 WG21이 Contracts가 들어간 C++26 초안을 표결했을 때도 반대표는
있었지만 큰 다수가 찬성했다.
그다음 단계인 DIS에서 반대표가 충분히 나와 3분의 2 찬성에 이르지 못했다.

다음 단계에 대해 글은 ISO가 선택지를 넷 준다고 적는다.
수정한 초안을 새 DIS 투표에 올리거나, 위원회에 돌려보내거나(CD 단계),
기술 사양서(Technical Specification)로 내거나, 프로젝트를 취소하는 것이다.
넷 모두 WG21의 과반 지지가 필요한데,
WG21은 Contracts가 들어간 C++26을 3분의 2가 넘는 다수로 다음 투표 단계에 올렸다.
Contracts에 불만인 쪽도 대안 구현에 노력을 들였으므로,
Contracts를 빼지 않고는 결과가 바뀌기 어렵다고 저자는 본다.
C++26 자체를 없애면 C++23으로 돌아가 변경 없이 C++29로 가는 것이고,
C++26에 이미 들어간 기능을 C++29에 다시 넣으려면 각 기능마다 지지하는 사람이
문서를 써야 한다.
다음 회의는 11월 16일이고, 교착을 푸는 것이 최우선이라고 한다.

저자는 이 결과를 큰 재앙으로 여긴다고 쓴다.
Contracts를 좋아하든 싫어하든 이 기능은 몇 년 동안 다듬어졌고 현재 형태로 여러
번 다수결을 얻었으며, 반대표로 신뢰와 존중하는 협업에 기댄 제도가 흔들렸다는
것이다.
저자는 모든 ISO 표준이 타협의 집합이라고 말하고,
투표에서 진 쪽이 패배를 받아들이지 않았다고 쓴다.
앞으로의 방향을 가르는 질문은 이 그룹이 신뢰를 다시 쌓을 수 있느냐다.

## 분석

### 글이 말하지 않는 수치는 다른 곳에서 공개되었다

글은 ISO 규칙을 들어 투표 결과의 내역을 적지 않는다.
같은 시기에 LinkedIn 사용자 Robert Seacord는 P-회원 20곳 중 12곳이 찬성해 60%로,
필요한 66.66% 이상에 미달했다고 적었다.[^seacord]
기권한 P-회원은 이 집계에서 빠진다고도 적었다.[^seacord]
같은 게시물은 회원 기관 22곳 중 반대가 9곳으로 41%이고,
허용 기준은 25% 이하라고 적었다.[^seacord]
이 수치는 한 사람의 게시물이고, 이 문서는 ISO의 공식 문서와 맞춰 보지 못했다.

수치가 맞다면 두 기준 모두 미달이다.
20곳의 3분의 2는 13.3이므로 찬성이 14곳은 되어야 하는데 12곳이어서 2곳이
모자란다.
22곳의 25%는 5.5이므로 반대는 5곳까지 허용되는데 9곳이어서 4곳이 넘는다.
Mateusz Pusz의 글도 승인 조건을 투표하는 P-회원의 3분의 2 이상 찬성과 전체 표의
4분의 1 이하 반대의 둘로 적고, 하나라도 못 채우면 부결이라고 쓴다.[^trainit]
a4z의 글도 같은 두 조건을 적는다.[^a4z]
Fertig의 글은 3분의 2 찬성이 미달했다는 점만 말하고 반대 상한은 언급하지 않는다.

### 두 번의 투표가 서로 다른 유권자를 가진다

글이 대비시키는 것은 WG21의 표결과 NB의 표결이다.
WG21에서는 Contracts가 들어간 C++26이 3분의 2가 넘는 다수로 통과했고,
이 저장소의 `cpp/cpp26.md`는 2026년 3월 회의에서 Contracts가 찬성 114,
반대 12, 기권 3으로 채택되었다고 전한다.
기권을 빼면 찬성 비율이 약 90%다.
반면 NB 단계의 찬성은 앞의 수치로 60%다.
두 비율은 단위가 다르다.
앞의 것은 회의장에 있는 개인들의 표이고, 뒤의 것은 국가 기관 단위의 표다.
HN에서 kllrnohj는 두 번째 단계가 사실상 형식이었다고
적었다.[^kllrnohj-formality]
kllrnohj는 이어 WG21의 3분의 2 찬성을 낸 하위 그룹이 이미 C++에 관심 있는 사람을
모두 포함하므로, 이번 결과는 평소 C++에 관여하지 않던 더 넓은 ISO 구성원이
WG21의 소수 의견 쪽으로 움직였다는 뜻이라고 추정한다.[^kllrnohj-formality]
이는 추정이고 이 문서는 확인하지 못했다.

### 합의와 다수결이 구분되지 않은 채 쓰이고 있다

글의 용어인 “합의(consensus)”에는 두 가지 쓰임이 있다.
HN에서 crote는 WG21이 주로 합의로 운영되며 이는 다수결이 아니라고 적고,
Contracts의 최종 표결 114-12-3을 일부가 이례적인 반대 수준으로 본다고
전했다.[^crote]
lewdwig는 기술 위원회가 합의가 있을 때 초안을 DIS에 보내야 하는데 본회의 표결로
보냈고, 합의는 지속적인 반대가 없는 상태라서 Contracts에는 합의가 없었다고
주장했다.[^lewdwig]
이에 맞서 zugi는 Contracts가 C++26 초안에 들어간 뒤 고쳐야 한다는 합의는
있었지만 어떤 수정에도 합의하지 못해 거의 그대로 갔고,
그 결과 어정쩡한 Contracts를 막는 유일한 방법이 언어 명세 전체를 부결시키는
것이었다고 설명했다.[^zugi]
글은 합의의 신뢰가 흔들렸다고 말하지만,
어떤 의미의 합의가 먼저 깨졌는지에 대해서는 이 댓글들이 서로 다르게 답한다.

### 선택지마다 치르는 값이 다르다

글이 든 ISO의 네 선택지는 Mateusz Pusz의 글에서 조금 더 구체적이다.
Pusz의 글은 수정한 질의 단계 초안에 8주의 투표가 따르고,
SC22 의장이 앞의 세 선택지 중에서 고르며,
취소는 SC22의 결정이 필요하다고 적는다.[^trainit]
또 의견을 포함한 전체 보고서가 투표 종료 후 12주 안에,
곧 늦어도 2027년 1월 중순에 나오고,
WG21이 2026-11-16부터 21일까지 브라질 부지우스에서 모여 방침을 논의한다고
적는다.[^trainit]

| 선택지                   | 의미                                      | 글과 댓글에서 나온 비용                                                                         |
| ------------------------ | ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 새 DIS 투표              | 수정한 초안으로 다시 표결한다             | Contracts를 두고 양쪽이 모두 투자했으므로 바뀌려면 Contracts를 빼야 한다는 것이 저자의 전망이다 |
| 위원회로 되돌림(CD 단계) | 위원회가 초안을 다시 다듬고 의견을 받는다 | 일정이 가장 길어진다                                                                            |
| 기술 사양서로 발행       | 표준이 아닌 문서로 낸다                   | 글은 이 방법의 구체적인 영향을 설명하지 않는다                                                  |
| 취소                     | C++23으로 돌아간다                        | C++26의 기능을 C++29에 다시 넣으려면 기능마다 지지자가 문서를 써야 한다                         |

## 비평

### 새 정보라는 기준은 글에서만 관행으로 나온다

저자는 NB가 새 정보가 있거나 절차에 오류가 있을 때만 반대표를 던지는 것이 이전
관행이었다고 쓰고, 이번에 그 관행이 깨졌다고 본다.
HN의 lowatt는 ISO가 승인을 두 단계로 요구하는 것은 일부러 한 설계인데 두 번째
단계의 표결권 행사가 왜 신뢰의 배신으로 여겨지느냐고 물었다.[^lowatt]
dannyw는 진짜로 서로 다른 견해가 충분히 있는 것이고 제도가 설계대로 작동한
것처럼 보인다고 답했다.[^dannyw]
bigstrat2003는 거부권이 있는 제도에서 그것이 행사되었다고 충격이나 배신으로 여길
이유가 없다고 적었다.[^bigstrat2003]
Pannoniae는 법률에 대한 왕의 재가에 비유해,
실제 논의는 WG21에서 일어나고 ISO 표결은 형식으로 취급되어 왔는데 이번에 그
관행이 바뀐 것이라고 글의 입장을 선의로 읽었다.[^pannoniae]
crote는 글이 이전 관행이라고만 쓰고 규정으로 밝히지 않았으며,
글 스스로 절차의 오류도 반대의 사유로 든다고 지적했다.[^crote]
이 문서가 보기에, 관행이 있었더라도 그것이 NB의 표결권을 제한하는 근거가
되는지는 글에서 규정이나 문서로 제시되지 않았다.

### 새 정보가 없다는 판단은 저자의 입장이고 반대 쪽 문서는 소개되지 않는다

저자는 Contracts 없는 C++26을 원하는 NB가 새 정보가 있다고 주장한다는 점을
소개하면서, 자신은 옛 논거의 새 문서를 새 정보로 보기 어렵다고 판단한다.
그 판단은 저자 개인의 것이고, 반대 쪽이 낸 문서의 내용을 글은 소개하지 않는다.
Lobste.rs의 refi64는 Contracts를 비판하는 P4334r0과 DIS 부결을 촉구하는 청원과
이를 반박하는 P4433r0이 있다고 정리했다.[^refi64]
olliej는 P4334의 모든 비판이 Contracts를 C++26에 넣기로 표결하기 전에 이미
위원회에 전달되어 검토되었다고 주장했다.[^olliej]
이에 seb는 P4334가 인용하는 문서에 이미 WG21이 각 우려를 신중히 검토하고 각각
현재 명세 쪽으로 결정했다고 적혀 있다며,
합의가 위원회 안에서는 있었어도 Contracts가 여전히 매우 논쟁적이라고
답했다.[^seb]
이 스레드는 글의 원문이 아니라 Robert Seacord의 LinkedIn 게시물을 올린 것이어서,
이 문서는 별도의 헤더 줄로 달지 않고 같은 사건을 다룬 의견으로 인용한다.
두 쪽의 논쟁이 이처럼 갈리는 상황에서,
저자의 판단은 새 정보 여부에 대한 하나의 입장이다.

### 저자의 위치가 글에 어떻게 작용하는지 알 수 없다

저자는 자신이 독일의 투표를 대표하는 위원이라고 밝히지만,
독일이 어떻게 투표했는지는 쓰지 않는다.
ISO 규칙 때문이라고 설명하지만,
같은 시기에 투표 집계가 공개되었으므로 이 설명이 어디까지 필요한 것인지 이
문서는 가리지 못했다.
글의 결론인 큰 재앙이라는 평가와 투표에서 진 쪽이 패배를 받아들이지 않았다는
문장은 부결표를 던진 쪽의 입장을 평가한 것이다.
독일의 표가 어느 쪽이었는지 알 수 없으므로 독자는 이 평가를 당사자의 것으로
읽을지 관찰자의 것으로 읽을지 정할 수 없다.

### Contracts의 기술적 쟁점은 글에 없다

글은 Contracts가 무엇인지 설명하지 않는다.
HN의 hankbond는 글에서 Contracts가 무엇을 가리키는지 찾지 못했다고
적었다.[^hankbond]
쟁점은 댓글에서 드러났다.
jandrewrogers는 고신뢰성 C++를 쓰는 입장에서 C++20 Concepts 이후에 Contracts가
해결하는 문제가 불분명하고, 대부분이 constexpr와 Concepts로 이미 되는 것의
조합이라고 적었다.[^jandrewrogers]
rerdavies는 Bjarne Stroustrup이 공저한 문서를 읽고 동의한다며,
가상 함수에 대한 Contracts의 동작을 C++29로 미룬 결정이 이 기능을 쓸모없게
만든다고 적었다.[^rerdavies]
kllrnohj는 같은 문서에서 가장 큰 불만이 마케팅이 잘못되었다는 것으로 보여
진지하게 받아들이기 어렵고, Bjarne Stroustrup이 Profiles를 미래로 보기 때문에
Contracts가 그 길을 덜 매력적으로 만든다고 해석했다.[^kllrnohj-flaws]
nanolith는 정적 분석기와 모델 검사기로 검증할 수 있는 계약 주석이 매우 유용하며,
현재 형태는 부적합하지만 더 단순하게 다시 제안될 자격이 있다고
적었다.[^nanolith]
이 문서는 이 쟁점이 되는 문서(P2900 등)를 열어 읽지 못했으므로 위 해석 중 어느
쪽이 맞는지는 가리지 못한다.

## 인사이트

### 연기되는 것은 Contracts 하나가 아니라 같은 초안의 모든 기능이다

HN의 Zepto8537은 리플렉션, std::execution,
라이브러리 강화 같은 C++26의 주요 기능이 같은 초안에 있었기 때문에 함께
늦어진다고 적었다.[^zepto]
dzogchen은 표준이 늦어질 뿐 컴파일러는 이 기능들을 이미 내놓고 있다고
반박했고,[^dzogchen]
bluGill은 컴파일러의 구현이 실험적 수준이어서 대부분의 사람이 쓰지 않을 것이라고
다시 반박했다.[^bluGill]
이 저장소의 `cpp/cpp26.md`는 GCC와 Clang이 리플렉션과 계약을 trunk에 병합했다고
전한다.
세 의견을 합치면, 표준 문서가 늦어지는 것과 실제 사용이 늦어지는 것은 별개의
일이다.
표준의 연도 대신 사용하는 컴파일러의 문서와 기능 확인 방법으로 채택을 판단하는
편이 이번 부결의 영향을 덜 받는다.
이 문서가 확인하지 못한 점은 컴파일러가 Contracts 없이 나머지만 먼저
안정화하는지 여부다.

### 두 기준 중 반대 상한이 길을 더 좁힌다

앞의 수치가 맞다면, 찬성 2곳을 더 얻어 3분의 2를 넘겨도 반대 상한은 풀리지
않는다.
반대 9곳을 5곳 이하로 줄이려면 최소 4곳이 반대에서 돌아서야 한다.
Contracts를 빼서 이 4곳을 설득하는 방법과,
Contracts를 유지한 채 기권이나 찬성으로 바꾸게 하는 방법은 서로 다른 협상이다.
Lobste.rs의 david_chisnall은 개별 회원 기관이 비준해서 발행할 수 있어 ANSI가
비준하고 ISO가 하지 않는 경우 ISO 표준이 아닌 C++26이 생길 수 있다고
적었는데,[^david-chisnall]
이는 이 문서가 확인하지 못한 추정이다.
이 수치는 한 게시물에 의존하므로,
판단 전에 12주 안에 나올 전체 보고서와 대조해야 한다.

### 부결은 표준화 제도 전체의 선택지로 일반화되어 읽히고 있다

HN에는 이번 일을 C++ 밖으로 확장한 반응이 많다.
swiftcoder는 몇 년 전 Rust가 ISO 인증을 받아야 하는지를 놓고 큰 논쟁이 있었고,
번거로움에 비해 이점이 적다는 쪽으로 결론이 났다고 상기하며 이번 일이 그 견해에
힘을 싣는다고 적었다.[^swiftcoder]
fithisux는 새 기능이 아니라 옛 표준의 수정이나 백포트를 내는 유지보수 릴리스를
제안했다.[^fithisux]
이 의견들은 이번 부결이 한 기능의 문제가 아니라 3년 주기의 표준 제도를 다시 묻게
한다는 읽기다.
다만 이 문서가 읽은 근거는 댓글뿐이어서,
부결이 실제로 이런 제도 논의를 일으킬지는 11월의 WG21 회의와 이후 결정을 봐야
한다.

---

[^seacord]: LinkedIn, [Balloting has completed for C++26. Unfortunately it was Disapproved](https://www.linkedin.com/posts/robertseacord_balloting-has-completed-for-c26-unfortunately-activity-7519795140887035918-5PWL)

[^trainit]: Train IT, [The result of the C++26 DIS ballot](https://train-it.eu/blog/cpp26-contracts-the-ballot-result/), 2026-10-25

[^a4z]: a4z, [C++26, WG21, and ISO's national bodies](https://a4z.noexcept.dev/blog/2026/10/29/cpp26-wg21-and-isos-national-bodies.html), 2026-10-29

[^kllrnohj-formality]: <https://news.ycombinator.com/item?id=50366300>

[^crote]: <https://news.ycombinator.com/item?id=50363280>

[^lewdwig]: <https://news.ycombinator.com/item?id=50364825>

[^zugi]: <https://news.ycombinator.com/item?id=50361561>

[^lowatt]: <https://news.ycombinator.com/item?id=50361674>

[^dannyw]: <https://news.ycombinator.com/item?id=50361727>

[^bigstrat2003]: <https://news.ycombinator.com/item?id=50362273>

[^pannoniae]: <https://news.ycombinator.com/item?id=50362050>

[^refi64]: <https://lobste.rs/s/rlrfew/balloting_has_completed_for_c_26#c_ojm0ur>

[^olliej]: <https://lobste.rs/s/rlrfew/balloting_has_completed_for_c_26#c_98sfpe>

[^seb]: <https://lobste.rs/s/rlrfew/balloting_has_completed_for_c_26#c_54264o>

[^hankbond]: <https://news.ycombinator.com/item?id=50361140>

[^jandrewrogers]: <https://news.ycombinator.com/item?id=50361334>

[^rerdavies]: <https://news.ycombinator.com/item?id=50370482>

[^kllrnohj-flaws]: <https://news.ycombinator.com/item?id=50365964>

[^nanolith]: <https://news.ycombinator.com/item?id=50361756>

[^zepto]: <https://news.ycombinator.com/item?id=50361735>

[^dzogchen]: <https://news.ycombinator.com/item?id=50362522>

[^bluGill]: <https://news.ycombinator.com/item?id=50366455>

[^david-chisnall]: <https://lobste.rs/s/rlrfew/balloting_has_completed_for_c_26#c_p6xvjl>

[^swiftcoder]: <https://news.ycombinator.com/item?id=50362903>

[^fithisux]: <https://news.ycombinator.com/item?id=50362252>
