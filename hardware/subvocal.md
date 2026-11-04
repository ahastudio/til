# Subvocal은 입을 움직이되 소리 내지 않고 말한 문장을 RF로 읽어 텍스트로 바꾸는 스마트 안경이다

<https://subvocal.company/>

Show HN: [Subvocal – Talk to your computer without making noise](https://news.ycombinator.com/item?id=50340088)

## 소개

Subvocal은 The Subvocal Company(YC F26)가 만드는 스마트 안경이다.
회사의 설명은 컴퓨터에 소리 내어 말하지 않고 말할 수 있게 하는 안경이다.
사용자가 입 모양으로 조용히 말하면 안경이 그것을 말하는 속도로 텍스트로
해독한다고 한다.
사이트 메타 설명은 컴퓨터를 위한 무음 텍스트 입력이며 말하는 속도로
입력한다고 쓴다.
이 문서가 읽은 `subvocal.company`는 JavaScript로 그려지는 페이지여서,
화면의 문구 대신 사이트 번들에 들어 있는 문자열을 읽었다.

### 동작 원리

Show HN 글에서 공동 창업자 Aarush와 Arnav는 이렇게 설명한다.
Georgia Tech에서 CS를 공부하던 두 사람은 Wispr Flow 파워 유저였고
도서관, 사무실, 공공장소에서 이런 도구를 쓸 수 없다는 점이 불편했다.
Stanford TreeHacks에서 MIT Media Lab의 AlterEgo를 36시간 안에 재현하려 했고,
얼굴에 근전도(EMG) 전극을 붙인 조잡한 프로토타입이 글자 수준에서 겨우 동작했다.

EMG는 세 가지 이유로 접었다.
땀에 따라 신호가 변하고, 전기 간섭이 있고, 전극 위치가 달라지며,
무엇보다 얼굴에 전극을 붙이려는 사람이 없다는 것이다.
그래서 블루투스와 비슷한 전파(RF)를 얼굴에 통과시키는 안경으로 바꿨다.
전파가 혀, 입술, 연구개를 지나면서 소리 없는 발음에 따라 변조되고,
이 교란을 파운데이션 모델(foundation model)로 텍스트로 해독한다고 한다.

개발 과정은 이렇게 적혀 있다.
아주 낮은 잡음의 RF 감지 스택을 만들었고,
안테나의 전기장이 조음기관과 최대한 겹치게 배치해야 했다.
안경에 처음 붙인 시도는 완전히 실패해서 안테나를 얼굴에 테이프로 붙였고,
위치를 고정하려고 머리 장치(head rig)를 만들었다.
시뮬레이션으로 안테나를 프레임 안에 넣은 지금의 설계로 발전했다.
사용자마다 얼굴 구조가 달라 RF 신호 패턴이 크게 다른 문제는
알고리즘 우회가 아니라 사전 학습 데이터를 크게 늘리는 방법으로 풀었다고 한다.
사무실에 부스를 차리고 사람들에게 돈을 주고 안경을 쓴 채 문장을 읽게 했으며,
데이터가 늘수록 오류가 빠르게 줄어드는 곡선을 얻었고 YC의 Dave는 20문장 교정만
했다고 쓴다.

수정된 설명도 있다.
입술을 움직이거나 입을 벌릴 필요가 없고,
RF가 입 안을 보므로 시스템을 “내적 발화(internal speech)”에 맞춰 조정할 수
있다는 것이다.
이것은 생각할 때 일어나는 자동 혀 움직임이 아니라 입술을 다문 채 하는 발음에
가깝다고 한다.

### 출시와 사전 주문

회사는 몇 달간 연구개발을 이어 Q1 2027에 출시할 계획이라고 쓴다.
첫 500대 사전 주문을 열었고 최종 가격에서 $200를 깎아 준다.
사이트 번들의 문구는 유료 사전 주문이 현재 미국에서만 가능하고
배송비와 세금은 따로 붙는다고 적는다.
추천 프로그램은 세 명이 유료 예약을 유지하면 남은 금액에서 $100를 깎아
준다고 한다.
사이트의 FAQ 문구는 Subvocal이 임의의 생각이나 무의식적 생각을 읽지 않고
의도적으로 발음한 단어만 해독하며,
카메라나 영상 기반 입술 읽기를 쓰지 않는다고 설명한다.

## 분석

### 이 제품의 핵심 주장은 소리 없는 입력이 사람이 있는 곳에서 음성 입력을 쓰게 한다는 것이다

음성 입력은 말하는 속도가 빠르다는 장점이 있지만 공공장소에서 쓰기 어렵다.
이 제품의 가설은 같은 입력 속도를 소리 없이 얻는 것이다.
HN에서 avree가 말하기가 타자보다 빠르지 않다는 사람도 있다고 하자,
공동 창업자 aarushyadav는 대부분 사람이 분당 40~50단어를 타자하고 개발자는
70~100단어인 데 비해
말은 120~200단어이며, 말로 하면 텍스트를 머릿속에서 다듬지 않아 더 나은
프롬프트가 나오는 경우가 많다고 답한다.[^aarushyadav-wpm]
이것은 회사의 주장이며 이 문서가 확인한 것이 아니다.

### 하드웨어 선택은 센서 접근에서 정해졌다

HN에서 여러 사람이 안경 대신 책상 위 장치나 이어폰 형태를 물었다.
tomhow가 노트북 위 장치를 묻자 aarushyadav는 같은 종류의 RF는 먼 거리에서 크게
약해져 안 되고,
60GHz 밀리미터파 레이더는 얼굴을 통과하지 않고 반사한다고
답한다.[^aarushyadav-mmwave]
growt가 기존 안경에 붙이는 형태를 원하자 같은 사람은 전자 부품과 안테나 배치를
사람과 안경에 걸쳐 일정하게 유지하기 어렵다고 답하고,[^aarushyadav-attach]
atulvi의 이어폰 형태 질문에는 AR 디스플레이로 출력을 돌려줄 수 있고 전자 부품과
안테나를 넣을 공간이 크다고 답한다.[^aarushyadav-glasses]
이 답들은 설계 이유에 대한 만든이의 설명이다.

## 비평

### 정확도와 사용 가능한 범위가 공개되지 않았다

글은 오류가 데이터 규모에 따라 빠르게 줄었다고만 하고 오류율 수치를 쓰지 않는다.
HN의 collabs는 YouTube 영상에서 약 5% 오류율을 솔직하게 보여 준 점을 높이 평가하지만,[^collabs]
이 문서는 그 영상을 열어 보지 않았고 댓글의 서술로만 전한다.
rootusrootus는 이 제품이 프로토타입에서 분당 200단어 이상을 주장하며
그 절반만 되어도 상위권 타자라고 쓰지만,[^rootusrootus]
수치의 출처는 이 문서가 확인하지 못했다.
demo4567은 오프라인 동작과 다른 언어 지원이 없으면 쓰지 않겠다고 하고
RonanSoleste는 영어가 모국어가 아니라 같은 이유라고
답한다.[^demo4567][^RonanSoleste]
이에 대한 회사의 답은 스레드에서 찾지 못했다.

### 내적 발화는 사용자 수가 매우 적은 상태에서의 결과다

mrandish는 입술을 다문 채 발음해 보았는데 어색했고 신호가 덜 나올 것 같으며,
어느 정도 발음해야 충분한지 피드백 없이는 알 수 없다고 쓴다.[^mrandish]
aarushyadav는 아직 외부인에게는 시험하지 않았고 두 창업자와 직원 한 명에게서만
풀었으며,
이 행동을 편하게 익히는 데 걸리는 시간이 길어 초기 핵심 기능으로 삼기 어렵다고
답한다.[^aarushyadav-internal]
그래서 글이 앞세운 “입을 열지 않아도 된다”는 현재는 소수 사용자의 결과이다.

### 데이터가 클라우드로 간다는 점이 질문으로 남았다

vessenes의 질문에 aarushyadav는 해독이 노트북이나 휴대폰의 동반 앱을 통해
클라우드에서 이루어지고
엔드투엔드 지연이 보통 500ms 미만이라고 답한다.
호출어는 처음에는 없고 연결된 기기의 트리거 키를 쓴다고
한다.[^aarushyadav-cloud]
ethanpil은 데이터가 어디로 가는지, 맥과 리눅스, 윈도 지원, 구독 여부를 묻고
vfosnar는 사용자 서버에 연결할 수 있는지 묻는데,[^ethanpil][^vfosnar]
이 문서는 이에 대한 회사의 답을 스레드에서 찾지 못했다.
사이트 번들의 개인정보 문구는 개인 정보를 팔지 않고 교차 맥락 광고에 공유하지
않는다고 하지만,
입 움직임 신호와 해독된 텍스트를 어떻게 다루는지는 이 문서가 읽은 문자열에서
확인하지 못했다.

### 제품 사진과 사이트 설명에 대한 신뢰 논쟁이 있었다

ipsum2는 모든 이미지가 AI로 생성되었다며 사전 주문이 사기라고 주장한다.[^ipsum2]
dang은 사전 주문은 제품이 아직 없다는 것이고 기술은 진짜이며,
스레드에 기술 정보와 개발 중인 제품 영상이 많아서 사기라는 주장은 이상하다고
답한다.[^dang]
AStrangeMorrow는 사이트 전체가 눈에 띄게 AI가 만든 이미지로 채워진 것이 신뢰를
주지 않는다고 한다.[^AStrangeMorrow]
이 문서는 이미지가 AI로 만들어졌는지 확인하지 못했다.
OhMeadhbh와 d1sxeyes는 홈페이지가 제품이 무엇인지 한 문장으로 알려 주지 않는다고
지적하고,[^OhMeadhbh][^d1sxeyes]
aarushyadav는 곧 고치겠다고 답한다.[^aarushyadav-site]

## 인사이트

### 이 제품은 안경이라는 폼팩터가 입력만이 아니라 출력까지 염두에 둔 선택이다

aarushyadav는 안경에 오픈 이어 스피커를 넣고 자체 에이전트 하네스를 안경에 직접
연결하려 한다고 한다.[^aarushyadav-speaker]
atulvi에게는 AR 디스플레이로 출력할 수 있다는 점을 안경의 이유로
든다.[^aarushyadav-glasses]
그렇다면 이 제품의 장기 가설은 소리 없는 입력만 파는 것이 아니라,
소리 없는 입력과 에이전트 응답을 묶은 착용 기기이다.
이 해석은 회사의 답변에서 이 문서가 연결한 것이며 회사가 직접 로드맵으로 밝힌
것은 아니다.

### 사전 주문 전에 확인할 조건

스레드와 글에서 아직 닫히지 않은 조건은 다섯 가지다.
오프라인 동작, 영어 외 언어, 데이터 처리 위치, 구독 여부, 도수 렌즈 지원이다.
vessenes는 사전 주문을 했다며 코가 높은 사람을 위해 조절식 코 받침을 유지해
달라고 요청하고,
aarushyadav는 코 받침을 유지하겠다고 답한다.[^vessenes]
이 조건들이 답으로 나오기 전에는 사전 주문을 취소할 수 있는지(예약금 조건)를
먼저 확인하는 것이 안전하다.
이것은 이 문서의 제안이다.

### 이 제품의 주장을 확인할 관찰

출시 후 독립적인 사용자들이 교정 없이 또는 짧은 교정만으로 얻는 단어 오류율과,
내적 발화로 입력했을 때의 오류율을 공개하면 데이터 규모로 일반화를 풀었다는
주장을 판단할 수 있다.
소수 사용자만 가능했다면 현재의 주장은 입술 움직임 기반 입력으로 한정해
읽어야 한다.

---

[^aarushyadav-wpm]: <https://news.ycombinator.com/item?id=50340836>

[^aarushyadav-mmwave]: <https://news.ycombinator.com/item?id=50340599>

[^aarushyadav-attach]: <https://news.ycombinator.com/item?id=50346366>

[^aarushyadav-glasses]: <https://news.ycombinator.com/item?id=50346340>

[^collabs]: <https://news.ycombinator.com/item?id=50341091>

[^rootusrootus]: <https://news.ycombinator.com/item?id=50340756>

[^demo4567]: <https://news.ycombinator.com/item?id=50345419>

[^RonanSoleste]: <https://news.ycombinator.com/item?id=50345701>

[^mrandish]: <https://news.ycombinator.com/item?id=50342985>

[^aarushyadav-internal]: <https://news.ycombinator.com/item?id=50347081>

[^aarushyadav-cloud]: <https://news.ycombinator.com/item?id=50341849>

[^ethanpil]: <https://news.ycombinator.com/item?id=50344101>

[^vfosnar]: <https://news.ycombinator.com/item?id=50344103>

[^ipsum2]: <https://news.ycombinator.com/item?id=50342045>

[^dang]: <https://news.ycombinator.com/item?id=50342129>

[^AStrangeMorrow]: <https://news.ycombinator.com/item?id=50342118>

[^OhMeadhbh]: <https://news.ycombinator.com/item?id=50340459>

[^d1sxeyes]: <https://news.ycombinator.com/item?id=50342003>

[^aarushyadav-site]: <https://news.ycombinator.com/item?id=50340761>

[^aarushyadav-speaker]: <https://news.ycombinator.com/item?id=50341953>

[^vessenes]: <https://news.ycombinator.com/item?id=50341512>
