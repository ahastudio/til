# GNU, GitHub에 저장소를 두지 말라고 권하다

원문: [What's Wrong with GitHub - GNU Project - Free Software Foundation](https://www.gnu.org/philosophy/whats-wrong-with-github.html)

HN 토론: <https://news.ycombinator.com/item?id=50041739> (21점, 5개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github> (56점, 51개 댓글)

GN 토론: <https://news.hada.io/topic?id=35206>

## 요약

GNU 프로젝트 철학 문서에 Jacob Bachmeyer와 Richard Stallman이 함께 쓴 글이
올라왔다.
페이지 하단의 갱신 기록은 2026년 9월 14일이다.
첫 문단부터 결론을 밝힌다.
소프트웨어 개발자는 저장소를 GitHub에 두지 말라는 것이다.
해로운 관행의 피해자가 되지 않고,
다른 사람까지 피해자로 끌어들이지 않기 위해서다.
글은 네 가지 문제를 꼽는다.
모호한 라이선스 관행을 부추기는 것,
대부분의 작업에 비자유 JavaScript 실행을 요구하는 것,
일부 “서비스”가 사실상 SaaSS(Service as a Software Substitute)라는 것,
그리고 Git의 분산 구조를 무너뜨리려 한다는 것이다.

저자들은 “Git은 자유 소프트웨어지만 GitHub은 소프트웨어가 아니다”라고 정의한다.
GitHub은 웹사이트이며, 단순한 저장소 호스팅부터 SaaSS까지 기능이 너무 다양해서
공정한 비판 자체가 어렵다고 인정한다.
그래도 큰 그림은 분명하다고 본다.
GitHub은 Git과의 호환성을 깨지 않는 선에서 최대한 담장 친 정원처럼 움직인다.
원클릭 병합은 GitHub에 호스팅된 “포크”에서 만든 풀 리퀘스트에서만 되고,
웹 UI는 이메일 주소 대신 GitHub 계정 링크를 보여 주며,
CI는 기본으로 GitHub 서버에서 돈다.
글은 이것을 “쇠가 아니라 비단으로 된 수갑”이라고 부른다.
당장 옮길 수 없다면 README에 이메일 주소를 적고,
사용 안내 페이지는 비자유 소프트웨어 없이 읽히는 사이트에 두라고 권한다.

본론은 다섯 갈래다.
첫째, 라이선스 안내다.
GitHub은 2008년 서비스 초기에 라이선스에 대해 침묵했고,
그 결과 라이선스가 없는 공개 저장소가 넘쳐났다.
2013년에 “Choose a License” 사이트를 만들었지만,
2026년 현재도 GPL 전문을 파일 하나에 복사해 두면 충분하다고 안내한다.
FSF 변호사들은 실질적인 파일마다 라이선스 고지를 넣으라고 권하는데,
GitHub은 이를 “선택 단계”로만 다룬다.
표준 고지가 없으면 “GPL 버전 N만”인지 “N 이상”인지 알 수 없다.

둘째, JavaScript다.
GitHub은 JavaScript 없이 우아하게 동작하지 않아서,
JavaScript를 거부하는 사용자는 저장소 열람 이상의 상호작용을 할 수 없다.
Git 명령줄과 REST API가 우회로지만,
공식 CLI는 Expat 라이선스의 자유 소프트웨어임에도 “텔레메트리”라는 스파이웨어를
넣었기 때문에 추천할 수 없다고 한다.
웹 API를 쓰는 도구라면 서버 로그로 사용 정보를 얻으면 될 일이라는 것이다.

셋째, Copilot이다.
학습 데이터를 그대로 토해 내는 능력(GPL 전문, Zen of Python) 때문에
제안 코드의 법적 지위가 불분명하고,
상위 등급 구독자에게 주는 면책이 GPL 준수 요구에도 통할지는 알 수 없다.
Copilot으로 작성한 이슈는 생성 사실이 거의 표시되지 않은 채 메인테이너를
“슬롭”으로 뒤덮는데, 메인테이너는 이를 막을 수 없다.
무엇보다 Copilot은 원격 서버에서 도는 SaaSS다.
2026년 초 모든 구독을 토큰 기반 과금으로 강제 전환한 것이 그 증거로 제시된다.

넷째, Git의 중앙화다.
Git은 중앙 장애점이 없도록 설계됐고, 이는 CVS와의 차별화,
Linux 커널의 바자 방식, BitKeeper 사태의 교훈이 겹친 결과였다.
GitHub은 Torvalds가 거부한 중앙화를 다시 들여온다.
배지 시스템인 “Achievements”는 GitHub 안의 활동만 보상하는 게임화이고,
사용자와 조직이 한 네임스페이스를 공유하는 게시판 모델은
정본 저장소를 찾기 어렵게 만든다.
풀 리퀘스트는 GitHub 안의 저장소만 가리킬 수 있는데,
원격 Git 서버나 이메일을 참조하지 못할 기술적 이유는 없다.
포크 수는 인기 배지처럼 쓰이고,
포크에만 있는 내용을 부모 저장소 URL로 가져올 수 있어 악용 여지가 있다.
Actions의 표준 러너는 자유 소프트웨어지만 자동 업데이트라는
“보편적 백도어”를 품고 있고, 무엇을 실행할지는 GitHub의 SaaSS가 정한다.
탈출구로는 워크플로를 로컬에서 돌리는 `act`를 소개한다.

다섯째, 소통의 진공이다.
SourceForge와 GNU Savannah는 메일링 리스트를 제공했지만 GitHub은 그러지 않는다.
Git은 Linux 커널의 메일링 리스트 협업을 위해 이메일 주소를 신원으로 삼았는데,
GitHub은 웹 UI에서 이메일 주소를 아예 보여 주지 않는다.
글은 사용자가 개발자가 되는 데 기술 외의 장벽이 없어야 한다는
자유 소프트웨어의 원칙을 들어, 이메일을 가리고 계정 생성을 요구하는 것이
아직 스스로를 개발자로 여기지 않는 사용자에게 사회적 장벽이 된다고 결론짓는다.

## 분석

### 비판의 축은 기능이 아니라 통제권이다

이 글의 다섯 갈래는 서로 달라 보이지만 하나의 질문으로 묶인다.
누가 그 계산을 통제하는가.
라이선스 고지는 사용자가 자기 권리를 알 수 있느냐의 문제이고,
JavaScript는 사용자 컴퓨터에서 무엇이 실행되느냐의 문제이며,
Copilot과 Actions 디스패치는 원격 서버에서 무엇이 결정되느냐의 문제다.
FSF가 오래 써 온 SaaSS라는 개념이 이 글 전체의 뼈대다.

그래서 “GitHub은 소프트웨어가 아니다”라는 첫 정의가 중요하다.
GitHub을 소프트웨어로 보면 라이선스로 평가할 수 있지만,
웹사이트로 보면 그 사이트가 사용자에게 무엇을 강요하는지로 평가해야 한다.
Lobste.rs의 nedbat은 바로 이 문장을 걸고 넘어졌다.
서비스로 실행되는 소프트웨어를 다루려고 만든 것이
AGPL 아니냐는 것이다.[^nedbat-agpl]
HN에서도 같은 문장에 대한 실소가 나왔고,[^andsoitis]
다음 문장까지 읽으면 “당신 컴퓨터에서 실행할 수 있는 소프트웨어가 아니다”라는
뜻이 분명하다는 반론이 붙었다.[^zaik]
정의 하나가 독자 절반을 잃게 만든 셈이다.

### 비단 수갑이라는 비유가 말하는 것

이 글에서 가장 날카로운 부분은 비자유 JavaScript가 아니라
“쇠가 아니라 비단”이라는 문장이다.
GitHub은 Git을 강제로 묶을 수 없으니,
가장 저항이 적은 경로를 GitHub 안쪽으로만 깔아 둔다.
원클릭 병합, 포크 기반 풀 리퀘스트, 기본 CI, 계정 링크가 하나씩은 사소하지만
합치면 Git의 분산 구조 위에 사실상의 중앙 허브가 생긴다.

이 관찰은 기술적으로 정확하다.
Git 자체는 어느 원격에서든 pull할 수 있지만,
GitHub의 풀 리퀘스트는 GitHub 안의 브랜치만 가리킨다.
리눅스 커널의 “이 브랜치를 pull해 주세요”라는 이메일 요청은
GitHub UI에서 일급 시민이 아니다.
이것은 기술적 제약이 아니라 제품 결정이다.

### 이메일이라는 신원 모델을 둘러싼 충돌

마지막 절은 이 글에서 가장 GNU다운 논점이다.
Git의 신원은 이메일 주소이고, 이는 메일링 리스트 중심 협업을 전제한 설계다.
GitHub은 신원을 계정으로 바꿔 놓았고, 그 결과 저장소 바깥의 사람이
메인테이너에게 닿는 경로가 GitHub 계정으로 좁아졌다.

Lobste.rs의 toastal은 GitHub을 쓰지 않으려고 저장소를 얕게 클론해서
메인테이너 이메일을 꺼낸 적이 있다고 했다.[^toastal-clone]
hoistbypetard는 웹 UI에서도 커밋 URL 끝에 `.patch`를 붙이면
커미터 이메일이 그대로 보인다고 짚었다.[^hoistbypetard-patch]
이메일은 여전히 거기 있다.
다만 기본 화면에서 지워졌을 뿐이고, 저자들이 문제 삼는 것도 바로 그 기본값이다.

## 비평

### JavaScript 집착이 정당한 비판을 갉아먹는다

이 글의 Copilot 절과 중앙화 절은 GNU가 아니라도 많은 개발자가 동의할 내용이다.
그런데 글은 그 앞에 비자유 JavaScript를 세워 둔다.
Lobste.rs의 noirscape는 이 순서가 문제라고 지적했다.
현대 웹 기능은 거의 전부 JavaScript인데,
그걸 거부하는 사람을 기준으로 사이트를 평가하면
나머지 비판까지 함께 신뢰를 잃는다는 것이다.[^noirscape]
같은 댓글은 Copilot 비판은 정확하다고 인정했다.

반대편 논거도 있다.
tusharhero는 GNU가 JavaScript 사용 자체가 아니라
사용자가 모르는 채 실행되는 비자유 코드에 반대하는 것이라고
정리했다.[^tusharhero-js]
그러나 thombles의 반문이 더 무겁다.
GitHub의 클라이언트 JavaScript가 내일 전부 GPL로 공개돼도
사용자의 삶은 조금도 나아지지 않는다는 것이다.[^thombles]
서버에서 결정되는 것을 클라이언트 코드의 자유로 바꿀 수는 없다.
글 스스로 SaaSS라는 더 정확한 도구를 갖고 있으면서
JavaScript라는 덜 정확한 도구를 앞에 내세운 것은 설득의 실패다.

### 기준이 Codeberg까지 걸러 낸다면 기준이 틀린 것이다

글은 결론에서 “그런 문제가 없는 사이트로 옮기라”고 말하지만,
어디로 옮겨야 하는지는 본문에서 말하지 않는다.
GNU의 윤리적 저장소 기준으로 추천 등급을 받는 곳은
자체 Savannah를 빼면 Sourcehut뿐이다.
pyfisch에 따르면 Codeberg는 GitHub과 같은 F 등급인데,
이유 중 하나가 JavaScript가 자유 소프트웨어임에도
GNU가 승인한 방식으로 표기되지 않았다는 것이다.[^pyfisch]

hoistbypetard는 Codeberg가 비자유 비공개 저장소를 허용하지 않는다는 점에서
Sourcehut보다 GNU의 사명에 더 가깝다고 반박했다.
그런 곳을 추천하지 못한다면 기준을 고쳐야 한다는 것이다.[^hoistbypetard]
cadey는 Anubis의 JavaScript에 GNU가 요구하는 방식대로 라이선스 표기를
했는데도 악성 코드라는 비난을 받았다고 덧붙였다.[^cadey]

이것은 글의 실용 권고를 무력하게 만든다.
GitHub을 떠나라는 주장의 무게는 갈 곳이 있느냐에 달려 있다.
기준이 너무 좁아서 Codeberg처럼 가치가 거의 겹치는 곳까지 떨어뜨린다면,
독자에게 남는 선택지는 Savannah와 Sourcehut 둘뿐이다.
pyfisch가 다시 짚었듯 Savannah는 낡았고,
GUIX와 GIMP 같은 GNU 프로젝트조차
Codeberg와 GNOME GitLab을 쓴다.[^pyfisch-savannah]

### Actions 비판은 보안과 통제를 혼동한다

글은 Actions 러너의 자동 업데이트를 “보편적 백도어”라고 부르고,
오래된 러너에 작업을 배정하지 않는 것을 그 강제 수단으로 본다.
그러나 CI 러너는 외부 코드를 실행하는 장치이고,
오래된 러너를 거부하는 것은 대부분의 운영자가 보안 정책으로 요구하는 동작이다.
noirscape는 이것을 “비밀번호가 없어야 한다”는 옛 GNU 입장에 빗댔고,
다른 러너로 옮기는 일은 길어야 반나절이라고 했다.[^noirscape]

글이 Actions에 대해 정말 말해야 했던 것은 이식성이다.
YAML 워크플로가 GitHub의 이벤트 모델과 마켓플레이스 액션에 얽혀 있으면,
러너가 자유 소프트웨어여도 이전 비용은 크다.
Nixpkgs 이전을 원하는 toastal이 마지막 걸림돌로 꼽은 것도
“공짜인 YAML 스파게티 CI”였다.[^toastal]
pbsds는 Codeberg가 Nixpkgs 규모의 CI를 감당하지 못할 것이라고 했다.[^pbsds]
자동 업데이트 문제가 아니라 이 비용이 실제로 개발자를 붙잡는다.

### 이메일 비공개는 결함이 아니라 기능일 수 있다

글은 GitHub이 웹 UI에서 이메일 주소를 숨기는 것을
공동체를 고립시키는 행위로 본다.
하지만 많은 사용자에게 커밋 이메일 노출은 스팸 수집 경로다.
noirscape는 오히려 Git이 이메일을 필수로 요구하는 것이 문제라고 했다.
GitHub과 GitLab, Forgejo 모두 noreply 주소를 제공하는 것도
그 수요 때문이라는 것이다.[^noirscape-email]

이메일을 공개 신원으로 삼던 1990년대 메일링 리스트 문화와
2020년대의 개인정보 감각은 다르다.
저자들이 말하는 원칙,
곧 사용자가 개발자가 되는 데 기술 외의 장벽이 없어야 한다는 원칙은 타당하다.
다만 그 원칙을 지키는 수단이 반드시 이메일 노출이어야 하는지는 논증되지 않았다.
README에 연락처를 적으라는 글 자신의 권고가 오히려 더 나은 해법이다.

## 인사이트

### 비판의 효과는 대안의 문턱에 반비례한다

이 글의 결론이 실제 이전으로 이어지지 않는 이유는 논리가 틀려서가 아니라
대안의 문턱이 높아서다.
Lobste.rs의 ryan-duve는 지자체 퇴비함을 여는 유일한 방법이
독점 스마트폰 앱이라는 예를 들었다.[^ryan-duve]
“GitHub을 피하라”는 친구와 동료가 있는 곳을 떠나라는 말이고,
“그 앱을 피하라”는 지역의 환경 활동에서 빠지라는 말이다.
둘 다 옳은 선택처럼 느껴지지 않는다.

자유 소프트웨어 운동이 1990년대에 이긴 영역은 컴파일러와 운영체제처럼
대안을 직접 만들어 낼 수 있었던 곳이다.
GCC는 “독점 컴파일러를 쓰지 마라”가 아니라 “이걸 쓰라”였다.
반면 GitHub에 대해 GNU가 내놓은 것은 기준표와 Savannah다.
pyfisch가 바란 “GNU 밖에서도 널리 쓰일 만큼 좋은 GNU 포지 소프트웨어”가
없는 한, 이런 글은 이미 동의한 사람에게만 닿는다.[^pyfisch-savannah]

### 진짜 문제는 클라이언트 코드가 아니라 확장 지점이다

david_chisnall의 지적은 글의 프레임 자체를 겨눈다.
FSF는 자유 소프트웨어 세계를 상상하는 대신
독점 소프트웨어 세계의 자유 복제본을 상상한다는 것이다.[^david_chisnall]
GitHub 같은 것을 처음부터 자유 소프트웨어로 설계했다면,
클라이언트 JavaScript와 서버 API는 단지 수정 가능한 라이선스가 아니라
문서화된 확장 지점과 최종 사용자 프로그래밍을 갖췄을 것이다.
사용자는 자기 작업 흐름에 맞게 UI를 고치고,
그 변경을 다른 사용자와 나눌 수 있다.

이 관점에서 보면 GitHub의 잠금은 비자유 JavaScript보다
API의 비대칭에 있다.
풀 리퀘스트가 원격 서버를 가리킬 수 없다는 글의 지적이 정확히 그 예다.
라이선스를 바꿔도 풀 리퀘스트 모델은 바뀌지 않는다.
포지 대안을 평가할 때 물어야 할 것은 “JavaScript가 자유로운가”보다
“이 포지를 떠날 때 무엇을 들고 나갈 수 있는가”다.

### 독점의 무기가 편의에서 AI 과금으로 옮겨 가고 있다

글의 Copilot 절은 다른 절과 성격이 다르다.
나머지는 2008년부터 이어진 오래된 불만이지만,
Copilot은 GitHub과 사용자의 관계를 바꾸는 새 축이다.
GitHub이 2026년 초 구독을 토큰 과금으로 일방 전환할 수 있었던 것은
저자들 말대로 Copilot이 SaaSS이기 때문이다.

이 변화는 비단 수갑을 조인다.
과거 GitHub의 잠금은 무료 CI와 네트워크 효과라는 편의였다.
앞으로의 잠금은 저장소, 이슈, 리뷰, 에이전트가 한 회사의 과금 체계 안에서
엮이는 구조다.
코드 리뷰 에이전트가 저장소의 이력과 이슈를 맥락으로 쓸수록,
저장소를 옮기는 일은 에이전트의 기억을 버리는 일이 된다.
HN의 haburka는 GitHub은 다른 서비스로 옮기기 쉽다고 반박했지만,[^haburka]
그 말은 저장소가 Git 데이터로만 이뤄져 있을 때 맞는 말이다.

### 글에 날짜가 없다는 것도 메시지의 일부다

nedbat은 이 글에 분명한 날짜를 달아 달라고 요청했다.
날짜는 페이지 맨 아래 RCS 형식으로만 적혀 있다.[^nedbat]
사소해 보이지만 이 글의 성격을 드러낸다.
GNU 철학 문서는 시간과 무관한 원칙의 진술로 쓰이고,
그래서 계속 고쳐 쓰이며 날짜를 앞세우지 않는다.

그러나 이번 글의 내용은 시간에 강하게 묶여 있다.
2026년 Choose a License의 문구, `gh` 텔레메트리, Copilot 토큰 과금은
모두 특정 시점의 사실이다.
원칙은 시간을 타지 않지만 근거는 시간을 탄다.
GitHub이 내일 텔레메트리를 끄거나 풀 리퀘스트에 원격 저장소를 허용하면
글의 절반은 낡는다.
날짜 없는 원칙 문서에 날짜 있는 사실을 쌓는 방식은,
FSF가 점점 덜 중요해 보인다는 j3s 같은 반응을 스스로 키운다.[^j3s]

---

[^nedbat-agpl]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_l0ck08>

[^andsoitis]: <https://news.ycombinator.com/item?id=50041750>

[^zaik]: <https://news.ycombinator.com/item?id=50042824>

[^toastal-clone]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_9vhydq>

[^hoistbypetard-patch]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_k459qs>

[^noirscape]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_ojyfxb>

[^tusharhero-js]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_2s97td>

[^thombles]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_cmlbwc>

[^pyfisch]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_wgsxs9>

[^hoistbypetard]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_myjvau>

[^cadey]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_gipcxx>

[^pyfisch-savannah]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_eocbus>

[^toastal]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_5ezgrj>

[^pbsds]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_oh0vbw>

[^noirscape-email]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_up7x85>

[^ryan-duve]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_6au3bg>

[^david_chisnall]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_732pit>

[^haburka]: <https://news.ycombinator.com/item?id=50054747>

[^nedbat]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_ztmokw>

[^j3s]: <https://lobste.rs/s/u9ue6c/what_s_wrong_with_github#c_u95nqi>
