# RubyGems와 Bundler 저장소 소유권을 Ruby 코어 팀이 맡는다

원문: [The Transition of RubyGems Repository Ownership | Ruby](https://www.ruby-lang.org/en/news/2025/10/17/rubygems-repository-transition/)

HN 토론: <https://news.ycombinator.com/item?id=45615863> (667점, 378개 댓글). 지지와 반발이 모두 상위에 올랐고 취재 근거를 둘러싼 공방도 벌어졌다.

## 요약

2025년 10월 17일 ruby-lang.org에 matz 명의로 올라온 공식 발표문이다.
약 300단어이며 Ruby 커뮤니티에게 보내는 편지 형식으로 시작하고 Yukihiro Matsumoto의 서명으로 끝난다.

전제를 두 문장으로 세운다.
RubyGems와 Bundler는 rubygems.org와 Ruby 생태계의 필수적인 공식 클라이언트이며 오랫동안 Ruby 언어에 번들되어 표준 라이브러리의 일부로 기능해 왔다는 것이다.
그런데도 RubyGems와 Bundler는 Ruby 생태계의 다른 주요 구성 요소와 달리 역사적으로 GitHub의 Ruby 조직 밖에서 개발되어 왔다고 적는다.

그리고 결정을 알린다.
커뮤니티에 장기적 안정성과 연속성을 제공하기 위해 Matz가 이끄는 Ruby 코어 팀이 Ruby Central로부터 이 프로젝트들의 관리 책임을 맡기로 결정했으며, Ruby Central 및 더 넓은 커뮤니티와 긴밀히 협력해 개발을 이어 가겠다는 것이다.

이어 강조하고 싶은 중요한 점 네 가지를 항목으로 제시한다.

| 항목       | 내용                                                                                                                    |
| ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| 소유권     | 장기적 안정성과 넓은 Ruby 생태계와의 정렬을 위해 저장소 소유권이 Ruby 코어 팀으로 이전되며, 관리는 이제 Ruby 코어 팀과 공동으로 Ruby Central이 계속 담당한다 |
| 라이선스   | RubyGems와 Bundler는 현재 라이선스로 오픈 소스를 유지하며 라이선스 조건에 변경이 없다                                   |
| 저작권     | 기존 기여자 전원이 자기 코드 기여에 대한 저작권과 저작자 지위를 온전히 보유하며 이 이전은 어떤 기여자의 지적 재산권에도 영향을 주지 않는다 |
| 개발 방식  | 협력적이고 커뮤니티 주도적인 개발 과정이 이전과 같이 이어지며 모든 커뮤니티 구성원의 기여를 환영한다                     |

마지막 문단에서 이 이전이 앞으로도 Ruby 생태계의 지속적인 건강과 안정과 성장을 보장하겠다는 약속을 나타낸다고 적는다.
여러 해에 걸친 헌신적인 관리에 대해 Ruby Central에 감사하며, Ruby의 더 밝은 미래를 만들기 위해 커뮤니티 모든 구성원과 함께 일하기를 기대한다는 것이다.
계속된 지원과 기여에 감사한다는 인사로 맺는다.

## 분석

### 분쟁이 아니라 조직 정합성의 문제로 서술한다

이 발표문에서 가장 결정적인 선택은 이전의 이유를 어디에 두는지다.
근거로 제시되는 것은 하나뿐이다.
RubyGems와 Bundler가 Ruby 생태계의 다른 주요 구성 요소와 달리 GitHub의 Ruby 조직 밖에서 개발되어 왔다는 사실이다.

이 서술은 참이면서 동시에 오래된 사실이다.
두 프로젝트가 Ruby 조직 밖에 있었던 것은 10년 넘게 그러했고 그동안 아무 문제로 취급되지 않았다.
그렇다면 왜 2025년 10월에 갑자기 정합성 문제가 되었는지는 발표문이 답하지 않으며, 그 공백에 놓여 있어야 할 것이 [그해 9월의 분쟁](rubygems-takeover.md)이다.
발표문에는 접근 권한 회수도, 잠긴 유지관리자도, 후원 철회도, 소송 위협도 나오지 않는다.

그래서 이 문서는 배경 없이 읽으면 정리 작업의 공지로 읽힌다.
Ruby Central에 대한 언급은 여러 해에 걸친 헌신적인 관리에 감사한다는 한 문장뿐이며, 그것이 전임 관리자에 대한 유일한 평가다.
곧 이 발표문의 장르는 사건 보고가 아니라 승계 공지이고, 그 선택이 뒤의 모든 특성을 결정한다.

### 다투어지지 않은 항목을 안심시키고 다투어진 항목은 다루지 않는다

네 항목 중 두 개는 애초에 쟁점이 아니었다.
라이선스가 그대로라는 것과 기여자가 저작권을 보유한다는 것이다.
MIT 계열 라이선스로 배포된 코드의 라이선스를 소유권 이전으로 바꿀 수 없고, CLA로 권리를 양도한 적이 없는 기여자는 언제나 자기 저작권을 갖는다.
곧 두 항목은 법적으로 자동인 사실을 약속의 형태로 다시 적은 것이다.

정작 쟁점이었던 것은 목록에 없다.
누가 커밋 권한과 관리자 권한을 갖는지, gem 소유자 레코드를 누가 관리하는지, 그리고 rubygems.org라는 서비스를 누가 운영하는지다.
발표문의 대상은 저장소이며 서비스는 한 번도 언급되지 않는다.
[이 사태의 핵심이 코드 소유권과 서비스 운영권의 구분이었다는 점](rubygems-takeover.md)을 생각하면, 이 발표문은 문제가 아니었던 계층을 다루고 문제였던 계층을 비워 둔다.

HN에서 그 질문이 곧바로 나왔다.
그러면 Ruby Central이 여전히 rubygems.org를 운영하는 것이냐는 물음[^hn-ands]이고, rubygems.org는 계속 Ruby Central이 운영하므로 여전히 그들을 신뢰해야 하며 상황을 감안하면 이상적이지 않지만 아무것도 바뀌지 않는 것보다는 나은 결과일 것이라는 정리[^hn-winter]다.
발표문이 답하지 않은 것을 독자가 첫 시간 안에 채워 넣었다는 뜻이다.

### 공동 관리라는 형식에 절차가 없다

첫 항목의 문장 구조가 특이하다.
소유권은 Ruby 코어 팀으로 이전되지만 관리는 이제 Ruby 코어 팀과 공동으로 Ruby Central이 계속 담당한다는 것이다.
곧 소유와 관리를 분리하고 관리는 두 주체가 함께 한다.

그런데 함께 한다는 것이 무엇인지가 정의되지 않는다.
누가 어떤 결정을 내리는지, 두 주체의 판단이 갈리면 무엇이 우선하는지, 각자에게 어떤 권한이 배정되는지, 이 배치를 나중에 바꾸려면 누구의 동의가 필요한지가 없다.
이름과 역할과 결정 규칙 없이 협력을 선언하는 형식이며, 이것이 이 문서의 구조적 약점이다.

이 약점이 특히 눈에 띄는 이유는 이 사태의 원인이 같은 종류의 공백이었기 때문이다.
[Ruby Together와 Ruby Central의 합병 시점에 자산 명세가 없었기 때문에 10년 뒤 누가 무엇을 소유하는지가 다투어졌다](ruby-central-legacy.md).
그리고 이 발표문은 거버넌스 명세 없이 새 공동 관리 체제를 세운다.
문서화되지 않은 관리 관계를 문서화되지 않은 다른 관리 관계로 교체한 것이며, 같은 실패 조건을 남긴다.

### 이전받는 주체의 정당성 근거가 인물이다

Ruby 코어 팀이 왜 적합한 관리자인지에 대한 발표문의 근거는 두 가지다.
장기적 안정성과 넓은 Ruby 생태계와의 정렬이며, 그리고 Matz가 이끈다는 사실이다.

Ruby 코어 팀은 선거로 구성되지 않는다.
이사회도 회원도 임기도 없고 커미터가 커미터를 받아들이는 구조이며 최종 판단은 Matz에게 있다.
그래서 이 이전은 자산을 더 안정적인 곳으로 옮기지만 더 책임을 묻기 쉬운 곳으로 옮기지는 않는다.
비영리 법인에는 이사회와 정관과 회계 공개가 있고 그것이 부실했다는 것이 이 사태의 비판점이었는데, 이전받는 쪽에는 그 부실한 장치조차 없다.

발표문 자체가 이 구조를 드러낸다.
Matz가 이끄는 Ruby 코어 팀이 결정했다고 3인칭으로 적고 마지막에 Matz가 서명한다.
집단이 결정했다는 서술과 한 사람이 서명하는 형식이 함께 놓이며, 실질적 정당성이 인물에서 온다는 것을 문서가 그대로 보여 준다.
HN에서 그 인물성이 지지의 근거로 반복됐다.
Matz의 행동과 어조가 완벽하며 위대함이 어떤 것인지 겸허하게 상기시킨다는 반응[^hn-james]이나, 일본 개발자로서 상황의 방향을 걱정했는데 안심된다는 반응[^hn-moss]이 그렇다.

## 비평

### 감사 인사 한 줄로 전임자를 평가한 것이 사실 관계를 확정한다

여러 해에 걸친 헌신적인 관리에 감사한다는 문장은 의례로 보이지만 실은 판단이다.
같은 시점에 커뮤니티의 상당 부분은 그 관리가 헌신이 아니라 탈취였다고 보고 있었고, 발표문은 그 견해가 존재한다는 사실조차 기록하지 않는다.

HN에서 그 반발이 최상위 댓글로 올라왔다.
이 프로젝트들은 애초에 Ruby Central의 것이 아니었으며 Ruby 코어 내부자 HSBT가 Ruby Central을 위해 훔친 것이므로 이것은 끔찍한 소식이라는 것[^hn-joel]이고, 빼앗긴 사람으로 André Arko, Colby Swandale, David Rodríguez, Ellen, Josef Šimánek, Martin Emde, Samuel Giddins 일곱 명을 이름으로 열거했다.
같은 사람이 논점을 좁히기도 했다.
누가 코드를 썼는지가 아니라 누가 유지관리권을 가졌고 그 유지관리자들이 프로젝트를 어떻게 통치하기로 합의했는지가 문제라는 것[^hn-joel-maint]이다.

이 반발이 옳은지는 별개 문제이고 실제로 다투어진다.
다만 발표문이 감사 인사를 택한 순간 그 논쟁에서 한쪽을 골랐다는 점은 피할 수 없다.
중립을 원했다면 전임 관리에 대한 평가를 생략하는 선택도 있었고, 사실 관계가 확정되지 않았음을 인정하는 선택도 있었다.
공식 채널이 감사를 적으면 그것이 기록이 되며, 접근 권한을 잃은 일곱 명은 그 기록 안에 존재하지 않는다.

### 이전받는 쪽이 원래 사건의 당사자라는 지적에 답하지 않는다

이 발표문은 Ruby 코어 팀을 분쟁 외부의 안정적 수탁자로 제시한다.
그런데 발표문이 나온 뒤 독자들이 시간 순서를 되짚으며 다른 독법을 제시했다.

HN에서 나온 정리가 그것이다.
Hiroshi Shibata가 승인 없이 단독으로 행동하지 않았다는 것을 며칠 전에 지적했는데 이제 그것이 Matz의 지시였음이 확인됐다며, 그렇다면 처음부터 이것을 공개적으로 밝힐 수는 없었는지 그러면 혼란이 줄었을 것이라고 적은 반응[^hn-shevy]이다.
같은 사람이 gem과 bundler를 가져오겠다는 결정이 언제 내려졌는지를 물으며 몇 달 전에 이미 정해졌을 수 있다는 의심을 덧붙였다[^hn-shevy-when].

이 추론은 확정된 사실이 아니라 발표문을 근거로 한 해석이다.
그러나 해석이 나올 수 있게 만든 것이 발표문 자신이라는 점이 문제다.
9월의 권한 회수를 실행한 인물이 Ruby 코어의 커미터이고, 10월에 그 자산의 소유권이 Ruby 코어로 이전된다면, 두 사건의 관계를 명시하지 않는 문서는 관계가 있었다는 추측을 초대한다.
그리고 이 추측이 성립하는 만큼 중립적 제3 수탁자라는 이 발표문의 전제도 약해진다.

발표문이 이 문제를 다루는 비용은 크지 않았다.
9월의 조치가 이 결정과 어떤 관계였는지 한 문단만 적으면 됐고, 관계가 없었다면 없었다고 적는 것으로 충분했다.
아무것도 적지 않은 선택이 가장 비싼 선택이 됐다.

### 최선의 실현 가능한 결과라는 방어는 가능한 대안이 검토됐음을 전제한다

이 발표를 지지하는 가장 정교한 논거가 HN에서 제시됐다.
Homebrew를 16년간 작업하고 상당 기간 이끌어 온 사람이 현직과 전직 RubyGems 유지관리자, Ruby Central 직원, gem.coop 유지관리자, Ruby 코어 인사들과 이야기해 본 뒤 이것이 실제로 도달 가능했던 최선의 결과로 보인다고 적었다[^hn-mike].
지난 1년간 본 어떤 것보다 장기적으로 지속 가능해 보이며 일부 제안은 더 좋게 들렸지만 어느 한쪽 이상에게 수용될 수 없었다는 것이다.
그리고 결정적으로 이 이전이 보장된 호스팅 비용과 온콜이 필요한 웹 서비스 운영을 보장된 비용이 없는 오픈 소스 CLI와 라이브러리 운영으로부터 분리한다고 짚었다.

이 논거는 강하고 이 문서의 구조를 정확히 설명한다.
코드와 서비스를 분리해 각각 다른 주체가 맡게 한 것이 합리적 설계라는 것이며, 그렇게 보면 서비스를 언급하지 않은 것이 누락이 아니라 범위 설정이 된다.

문제는 그 논거가 발표문 안에 없다는 것이다.
분리가 설계였다면 발표문이 그렇게 적어야 했고, 서비스는 계속 Ruby Central이 운영하며 그 이유는 비용과 온콜 구조가 다르기 때문이라고 한 문장으로 밝히면 됐다.
그것을 적지 않았기 때문에 같은 사실이 어떤 독자에게는 합리적 분리로, 다른 독자에게는 절반만 해결된 이전으로 읽혔다.
공식 문서의 해설을 외부 인사가 대신 제공해야 했다는 것이 이 발표문의 실패 형태다.

그리고 이 방어는 다른 대안이 실제로 검토되고 거부됐음을 전제하는데 발표문에는 그 기록이 없다.
gem.coop 같은 대안이 논의됐고 수용되지 않았다는 것은 그 논거를 제시한 사람의 개인적 관측이며, 어떤 안이 왜 배제됐는지에 대한 공적 기록은 존재하지 않는다.

### 사실 관계를 공백으로 남긴 대가가 이후 10개월의 서술 다툼이다

발표문이 왜를 적지 않은 결과가 이 스레드에 이미 나타난다.
무슨 일이 있었는지 여전히 궁금하며 생태계 전반에 대해 다소 마음이 식었다는 반응[^hn-pebble]이나, 상대적 외부인에게 간단히 설명해 줄 수 있느냐는 요청[^hn-gardnr]이 그렇다.
667점을 받은 발표문의 스레드에서 사람들이 여전히 사건 경위를 서로에게 묻고 있었다.

그리고 그 공백이 남긴 것은 중립이 아니었다.
같은 스레드에서 취재 근거를 둘러싼 공방이 벌어졌다.
Ruby Central이 비판자들에게 법적 위협을 하고 있어 사람들이 실명으로 나서기를 꺼린다며, 직접 아는 두 사람이 Shopify가 Ruby Central에 RubyGems GitHub 조직과 패키지의 완전한 통제를 요구했다고 말해 줬고 자기가 거짓말한다고 믿어도 되지만 이 경우에는 출처를 직접 인용할 수 없다고 적은 대목[^hn-joel-source]이다.
익명 출처 두 명에 근거한 주장이 공식 기록의 부재를 메우게 된 것이며, [나중에 그 취재 자체가 다른 기여자에게 반박된 것](minaswan.md)도 같은 공백의 결과다.

곧 이 발표문의 안심시키는 네 항목이 지불한 값은 이후 서술의 통제권이었다.
자기 위기를 스스로 서술하지 않는 기관은 중립을 얻지 못하고 가장 동기가 강한 서술자를 얻는다.
이 사안의 기록이 Joel Drapper의 취재와 David Celis의 정리와 André Arko의 상실 목록과 Ruby Central의 사고 보고서와 Paul Battley의 글로 이루어져 있고 그중 어느 것도 제3자 기록이 아니라는 사실이 그 결과다.

## 인사이트

### 패키지 생태계 분쟁에서 저장소는 다섯 자산 중 가장 덜 중요한 것이다

이 발표문의 대상은 GitHub 저장소 소유권이다.
그런데 이 분쟁에서 실제로 다투어진 자산을 열거하면 저장소는 그중 하나이고 나머지 넷이 더 무겁다.
gem 소유자 레코드, 프로덕션 인증 정보, 상표, 릴리스 서명 키다.

각 자산의 성질이 다르다.
저장소는 포크가 가능하므로 소유권을 잃어도 코드를 잃지 않는다.
반면 gem 소유자 레코드는 복제할 수 없고, 프로덕션 접근은 서비스 그 자체이며, 상표는 이름을 쓸 권리를 정하고, 서명 키는 사용자가 무엇을 믿을지를 정한다.
곧 저장소만 옮기는 것은 다섯 자산 중 유일하게 대체 가능한 것을 옮기는 일이다.

그래서 이런 사안을 판단할 때 쓸 수 있는 절차가 나온다.
다섯 자산을 먼저 나열하고 제안된 해법이 각각을 건드리는지 표로 채우는 것이며, 발표문 한 편이 다섯 칸 중 몇 칸을 채우는지가 그 해법의 실질을 말해 준다.
이 발표문은 한 칸을 채우고 네 칸을 비운다.
[코드는 라이선스로 자유롭지만 서비스는 운영자가 통제한다는 구분](rubygems-takeover.md)이 이 표의 두 번째와 세 번째 칸에 해당하고, [상표가 코드를 다 넘긴 뒤에도 쟁점으로 남았다는 사실](ruby-central-legacy.md)이 네 번째 칸을 설명한다.
같은 시점에 Ruby Central도 별도 성명을 냈고 HN 스레드에서 링크됐지만, 두 성명을 나란히 놓고 다섯 칸을 함께 채우려는 시도는 어느 쪽에도 없었다.

한 가지 덧붙일 것은 다섯 칸 중 마지막 두 개가 기술로 완화될 수 있다는 점이다.
HN에서 그 방향이 제시됐다.
서명이 이미 지원되는 OCI 아티팩트 레지스트리에서 gem을 제공할 수 있느냐고 물으며 `gem cert`와 `gem install -P HighSecurity`, sigstore-ruby, Trusted Publishing을 열거한 반응[^hn-west]이다.
서명과 배포가 단일 운영자에게 묶여 있지 않다면 그 운영자를 누가 통제하는지가 덜 중요해진다.

### Matz의 정치적 비가시성은 거버넌스 공백이 아니라 이 국면에서 자산으로 기능했다

Ruby 커뮤니티의 표어를 비판한 글은 Matz가 기술 영역 밖에서 선언을 하지 않고 온라인 활동 대부분을 일본어로 한다는 점을 문제로 다룬다.
[그것이 무엇이든 투사할 수 있는 공간을 제공했다는 지적](minaswan.md)이며, 성품이 제도를 대신해 온 것이 이 커뮤니티의 결함이라는 진단이다.

그런데 이 발표문은 같은 특성이 반대로 작동한 사례다.
분쟁의 어느 진영에도 공개적으로 서지 않았고 어느 후원사와도 논쟁하지 않았기 때문에, 자산을 옮겨받을 때 양쪽 모두에게 수용 가능한 인물이 됐다.
수탁자의 자격 요건이 정확히 그것이다.
분쟁에 대해 아무 말도 하지 않았을 것, 그리고 이해관계가 관측되지 않을 것이다.

이것은 양육권이나 재산 분쟁이 실제로 해소되는 표준 경로와 같다.
당사자 중 누구도 상대에게 자산을 넘기지 않으려 할 때 해법은 제3 수탁자이고, 그 수탁자의 자격은 능력이 아니라 무관함이다.
법원이 임명하는 관리인이 그 분야 최고 전문가일 필요는 없고 이해관계가 없어야 한다.
발표문이 근거로 든 장기적 안정성이라는 표현은 실은 그 무관함을 다르게 적은 것이다.

여기서 나오는 결론이 앞선 비판과 충돌하지는 않는다.
같은 특성이 평시에는 제도의 부재를 은폐하고 위기에는 교착을 푸는 데 쓰인다는 뜻이며, 그래서 그것은 대체 가능한 자산이 아니다.
한 번 쓰면 줄어드는 종류의 자원이기도 하다.
이번에 수탁자가 되면서 Matz는 더 이상 분쟁 외부에 있지 않게 됐고, 다음 분쟁에서 같은 역할을 할 수 있는 사람이 남아 있는지는 별개 문제다.

### 안정성을 위해 한 사람에게 의존을 늘렸고 승계 계획은 이전보다 얇아졌다

발표문이 반복하는 단어가 장기적 안정성이다.
그러나 이전 전후의 구조를 비교하면 장기 위험은 오히려 커졌다.

이전 전에는 언어의 핵심 패키지 인프라가 비영리 법인에 있었다.
그 법인의 거버넌스가 부실했다는 것이 이 사태의 비판점이지만, 법인에는 교체할 수 있는 이사회와 개정할 수 있는 정관과 문제가 생기면 상대할 수 있는 법적 주체가 있다.
이전 후에는 선거도 정관도 없는 커미터 집단에 있으며 실질적 결정권은 60대의 한 사람에게 있고 승계 절차는 문서화되어 있지 않다.
곧 대체 가능성이라는 축에서 인프라가 더 취약한 쪽으로 이동했다.

이 위험이 즉시 보이지 않는 이유는 안정성이라는 단어가 두 가지를 뜻하기 때문이다.
지금 갈등이 없다는 뜻의 안정성과 담당자가 바뀌어도 유지된다는 뜻의 안정성이다.
발표문이 제공하는 것은 앞의 것이고 주장하는 것은 뒤의 것이며, 두 의미의 차이가 승계 문서의 부재로 나타난다.
[André Arko가 커뮤니티가 이사를 선출하는 조직을 바란다고 적은 것](ruby-central-legacy.md)과 [Ruby Central이 정관을 전면 개정하고도 선거를 도입하지 않은 것](ruby-central-legacy.md)이 이 사안의 다른 두 면이며, 이 발표문은 그 논의를 다시 인물 신뢰로 되돌린다.
[Rails 쪽 포크론이 결국 소유권과 거버넌스 문제로 수렴한 것](../rails/rails-without-dhh.md)도 같은 결핍, 곧 승계 절차가 문서화되지 않은 채 인물에게 걸려 있는 구조를 겨냥한다.

실무적으로 남는 요구는 그래서 명확하다.
소유권을 옮긴 뒤에 필요한 문서는 감사 인사가 아니라 권한자 명단과 승계 절차다.
누가 관리자 권한을 갖는지, 그 목록을 누가 갱신하는지, Matz가 결정할 수 없는 상황이 오면 무엇이 발동하는지를 적는 것이며, 그 문서는 평시에 쓰기 쉽고 다음 분쟁에서는 쓸 수 없다.

### 레지스트리 포획이 이만큼 큰 사건이 된 것은 미러가 없기 때문이다

이 사태가 언어 생태계 전체를 흔든 이유를 기술 구조에서 찾은 관점이 HN에서 나왔다.
Linux 배포판 공동체에 이런 소동의 대응물이 있었는지 물으며, APT와 dpkg 모델에는 이런 종류의 혼란을 막는 무언가가 있는지 궁금하다는 반응[^hn-shadow]이다.
Ruby 커뮤니티가 너무 오래 신뢰할 만한 인터넷과 함께 살아서 자동 패키지 미러를 구축하는 문제를 풀 필요가 없었던 저주를 겪는 것 아니냐며, 패키지와 체크섬만 있으면 되는 문제에 많은 말과 에너지가 쓰인 것처럼 느껴진다고 덧붙였다.

이 관점이 사건의 규모를 설명한다.
Debian 계열에서 미러 하나가 신뢰를 잃으면 설정 한 줄을 바꾸고 잊으면 된다.
단일 도메인이 유일한 배포 경로인 생태계에서는 그 도메인의 운영자가 누구인지가 생태계의 운명이 되며, 그래서 조직 분쟁이 인프라 위기로 증폭된다.
같은 스레드에서 지적된 대로 여러 패키지 관리자가 미러를 불필요한 복잡성으로 보고 생략했으며 그 결정의 비용이 이런 국면에 청구된다.

다만 이 진단에는 곧바로 단서가 붙는다.
배포판 공동체가 조직 분쟁을 겪지 않은 것은 아니며, 하나의 공동체로 묶을 수도 없다는 반론[^hn-zahl]이 나왔다.
Debian 계열이 아닌 배포판은 패키지 형식조차 다르고 문제가 완화된 이유의 상당 부분은 경쟁하는 대안들 사이에서 선택할 수 있게 한 것이라는 지적이다.
곧 미러가 해법이라기보다 복수의 대안이 해법이며, 미러는 그 복수성을 구현하는 한 방식이다.

그래서 이 발표문 이후에 실제로 남은 과제는 소유권이 아니라 복수성이다.
같은 스레드에서 gem.coop 같은 여러 출처를 갖는 것이 장기적으로 더 안전하고 견고한 해법일 것이라는 정리[^hn-dluan]가 나온 이유이며, 탈중앙 패키지 호스팅이 유일한 길이라는 짧은 단언[^hn-binary]도 같은 방향이다.
누가 레지스트리를 소유하느냐는 질문은 레지스트리가 하나일 때만 중요하다.


---

[^hn-ands]: HN 사용자 `andsmedeiros`: “So Ruby Central will still be running rubygems.org?”
[^hn-winter]: HN 사용자 `winterqt`: “rubygems.org will still be operated by Ruby Central, though, so you still have to trust them. Given the state of affairs, this is less than ideal, but it's probably a better outcome than nothing changing.”
[^hn-james]: HN 사용자 `james_marks`: “Matz' action and tone in the announcement is impeccable. Humbling reminder of what greatness looks like.”
[^hn-moss]: HN 사용자 `white-moss`: “As a Japanese developer, I've been worried about the direction things were going, so it's reassuring to see this.”
[^hn-joel]: HN 사용자 `joeldrapper`: “These projects were not Ruby Central's in the first place. They were stolen for Ruby Central by a Ruby Core insider, HSBT. This is horrible news.” 이후 André Arko, Colby Swandale, David Rodríguez, Ellen, Josef Šimánek, Martin Emde, Samuel Giddins를 열거했다.
[^hn-joel-maint]: HN 사용자 `joeldrapper`의 답글: “I'm not talking about who wrote the code. Hundreds of people wrote the code, that's not particularly relevant. I'm talking about who had maintainership of the code and how those maintainers had agreed to govern the project.”
[^hn-shevy]: HN 사용자 `shevy-java`: “For instance, I pointed out days ago that Hiroshi Shibata did not act solo. Now this is confirmed - it was a matz directive. The main question to ask here is: could he not have made this open AND public from the get go? It would have lessened the confusion for some people.” 발표문을 근거로 한 해석이며 확정된 사실은 아니다.
[^hn-shevy-when]: HN 사용자 `shevy-java`의 답글: “It was always clear that Hiroshi Shibata didn't act solo without approval. I am not saying he knew the outcome before that, but WHEN was the decision made to take over gems + bundler? I have a slight suspicion that this may have been decided upon months ago already.”
[^hn-mike]: HN 사용자 `mikemcquaid`: “As someone who spent a bunch of time talking before and after this all went down with current and past RubyGems maintainers, RubyCentral employees, Gem.coop maintainers and Ruby Core folks: this seems like the best outcome that was actually attainable... It also separates the 'running a web service' which has guaranteed hosting costs, requires on-call, etc. from 'running an open source CLI/library' which has no guaranteed costs.”
[^hn-pebble]: HN 사용자 `pebble`: “Better Ruby core than Ruby Central but still leaves me wondering what the hell happened and slightly sours me on the whole ecosystem.”
[^hn-gardnr]: HN 사용자 `gardnr`: “Can anyone please explain this in simple terms for a relative outsider?”
[^hn-joel-source]: HN 사용자 `joeldrapper`의 답글: “Ruby Central is making legal threats to its critics, so I hope you can see why people don't feel safe to come forward on the record. I can tell you that two people with direct knowledge of the situation told me that Shopify demanded that Ruby Central take full control of the RubyGems GitHub organisation and packages. You can believe that I am lying if you want. But I can't directly cite my sources in this case.”
[^hn-west]: HN 사용자 `westurner`: “Can Gems be served from OCI Container/Artifact registries, which (also) already support signatures?” 이후 `gem cert --build`, `gem install gemname -P HighSecurity`, sigstore-ruby, Trusted Publishing을 열거했다.
[^hn-shadow]: HN 사용자 `shadowgovt`: “Was there ever a mirror of this dustup in the Linux distro community? I'm unaware of one ever happening, and I'm wondering whether it's because of mere fortune or because there's something about the APT / dpkg model that precludes this kind of messiness... This just feels like a lot of words and energy burned on a problem that ought to be as simple as 'Here's the package, here's its checksum, go to town.'”
[^hn-zahl]: HN 사용자 `zahlman`: “The fact that you speak of 'the Linux distro community' but also 'the APT / dpkg model' is already telling. Most distros — i.e., everything not derived from Debian — don't even use the same package format. A lot of the problem has been mitigated simply by letting people choose among competitive suites of alternatives.”
[^hn-dluan]: HN 사용자 `dluan`: “In the long run, having multiple sources like gem.coop is probably a safer and more robust solution. But for RubyGems specifically, the trust was fully lost, through several layers - maintainers, community members, sponsors, etc.”
[^hn-binary]: HN 사용자 `binary132`: “Decentralized package hosting is the only way.”
