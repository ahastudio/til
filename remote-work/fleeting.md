# Fleeting: 시간을 뺏기지 않으려고 가짜 회의를 틀어 두는 서비스

<https://iminafleeting.com/>

HN 토론: <https://news.ycombinator.com/item?id=50018088> (883점, 249개 댓글)

GN 토론: <https://news.hada.io/topic?id=35070>

## 소개

Fleeting은 지어낸 회의의 음성과 화상회의 화면을
브라우저에서 재생해 주는 웹 서비스다.
첫 화면의 제목은 “Sorry, I'm in a meeting.”이고,
부제는 자기 시간을 훔쳐 가는 사람들에 맞서는 직장 내 자기방어라고 소개한다.
회의를 하나 고르고 재생을 누른 뒤 스피커로 틀어 두면,
주변 사람은 회의 중이라고 여기고 말을 걸지 않는다는 발상이다.
부제에서 “Realistic”에 취소선을 긋고 “Plausible”로 고쳐 쓴 것처럼,
진짜 같다기보다 그럴듯한 정도를 목표로 한다고 스스로 밝힌다.

만든 사람은 John Carroll이고, 푸터에는 그의 LinkedIn과 정보보안·조사 업체
Splinters가 함께 걸려 있다.
개인정보 처리방침의 운영자 표기는 Fleeting(iminafleeting.com)이며,
연락처는 LinkedIn뿐이다.
처리방침의 마지막 수정일은 2026년 10월 8일이고,
다음 날인 10월 9일 Hacker News에 `splintersio` 계정으로 올라와 883점을 받았다.
이 계정은 토론에서 광고와 다국어 지원에 관한 질문에 운영자로서 답했다.

계정과 가입 절차가 없고 요금도 받지 않는다.
수익원은 회의 안에 들어가는 후원 언급과 회의 종료 화면의 후원 카드다.

## 주요 기능

### 회의 목록

회의는 14종이다.
각 회의에는 시간대 슬롯이 정해져 있어서,
지금 시각에 어울리는 회의가 목록 앞쪽에 온다.

| 회의                             | 홈페이지 설명                                         | 시간대             |
| -------------------------------- | ----------------------------------------------------- | ------------------ |
| Engineering Standup              | 짧은 업데이트, 블로커 없음, 누군가의 개가 짖음        | 평일 8:30~11:30    |
| Client Sales Call                | “can you see my screen?”                              | 평일 9:00~17:30    |
| API Design Review                | 버전 관리, 페이지네이션, “should that be a 409?”      | 평일 9:00~17:30    |
| AppSec Review                    | 위협 모델링, 인증 흐름, “what's the blast radius?”    | 평일 9:00~17:30    |
| Scoping Call                     | 고객과 컨설턴트가 범위 안팎을 합의                    | 평일 9:00~17:30    |
| Project Status Meeting           | RAG 상태, 밀린 일정, “let's take that offline.”       | 평일 9:00~17:30    |
| Vendor Security Review           | SOC 2 보고서, 데이터 상주 위치, 침투 테스트 요약 요청 | 평일 9:00~17:30    |
| Quarterly All-Hands              | 열정적인 발표자 한 명과 예의 바른 박수                | 평일 9:00~17:30    |
| IT Incident War Room             | 긴장된 타자 소리, “Who deployed last?”                | 언제나             |
| Before the Host Joins            | 10분이 지나도 주최자가 없어 시작된 뒷담화             | 평일 9:00~17:30    |
| Healthy Workplace Working Group  | 친절 헌장, 번아웃 설문, “per my last email.”          | 평일 9:00~17:30    |
| Offsite Planning Sync            | 온수 욕조, 방 배정, “happy to go deep on that.”       | 평일 9:00~17:30    |
| Ops Weekly (Flight Deck Edition) | 기장 안내 방송 말투의 프로젝트 관리자                 | 평일 9:00~17:30    |
| Ransomware Crisis Bridge         | 모든 것이 암호화된 상황                               | 언제나, 목록 맨 끝 |

광고 안내 페이지는 Bad-Connection Zoom을 포함한 11종을 후원 대상으로 나열하지만,
메인 화면 목록에는 Bad-Connection Zoom이 없다.
반대로 Healthy Workplace Working Group 이하 네 회의는 메인 목록에만 있다.

### 억양과 언어

억양은 British, American, International(mixed accents) 세 가지 영어가 기본이다.
스페인어, 프랑스어, 독일어, 이탈리아어는 베타로 표시되며, Engineering Standup,
IT Incident War Room, Healthy Workplace Working Group, Offsite Planning Sync,
Ops Weekly 다섯 회의에만 있다.
고른 억양이 없는 회의는 British로 대체되고, 카드에 실제로 나올 억양이 표시된다.

첫 방문 때의 억양은 브라우저 언어 설정으로 정한다.
`en-US`와 `en-CA`는 American, 인도·나이지리아·싱가포르·필리핀 등 아홉 개 지역의
영어는 International, 나머지 영어는 British가 되고,
영어가 아니면서 베타 언어에도 없으면 International이 된다.

HN 공개 당일에는 British 외의 억양이 재생되지 않는다는 제보가 이어졌다.
roryirvine은 American과 International을 고르면 소리가 나지 않고,
“Join Audio” 버튼도 듣지 않는다고 했다[^roryirvine].
AIorNot은 인도, 러시아, 남미 억양이 하나도 없어 금방 의심받겠다고 했다가,
억양 선택기를 뒤늦게 찾았다[^AIorNot].
다른 언어를 넣어 달라는 요청에 `splintersio`는
번역과 방언이 오히려 덜 그럴듯하게 만들 것 같지만
베타로는 넣을 수 있다고 답했다[^splintersio-beta].
지금 사이트에는 네 언어가 베타로 들어가 있다.

### 통화 화면

회의에 들어가면 화면이 전체 화면으로 바뀌고, `F` 키로 전환할 수 있다.
위쪽에는 “Recording” 표시와 회의 제목, 경과 시간이 있고, 아래에는 마이크,
카메라, “I have to drop”, 통화 종료 버튼이 있다.
참가자 타일에는 이니셜 아바타가 뜨고,
일부 회의의 참관자 타일에서는 영상이 재생된다.
FAQ는 목소리가 모두 합성이고,
얼굴은 AI로 만들었거나 사용권을 산 스톡 영상이라고 밝힌다.
이름도 모두 지어낸 것인데,
만든 사람인 John Carroll만 예외로 몇몇 회의에 카메라를 끈 참관자로 앉아 있다.

입력한 이름은 내 타일에 표시된다.
마이크와 카메라 버튼은 모양만 바뀌며, 사이트의 `Permissions-Policy` 헤더가
`camera=()`, `microphone=()`으로 두 장치를 아예 막는다.
통화 중에는 브라우저 탭 제목이 `<회의 제목> | Meeting`으로,
파비콘이 통화 아이콘으로 바뀐다.

### 재생과 퇴장

FAQ에 따르면 회의 하나는 약 12분이고,
매번 임의의 지점에서 재생을 시작해 같은 첫 대사가 연달아 나오지 않는다.
Engineering Standup의 British 녹음 타임라인은 751.4초다.
“Leave”나 “I have to drop”을 누르면 다른 참가자들이 작별 인사를 한 뒤
통화가 끝나고, 회의에 머문 시간이 표시된다.

Back-to-back meetings 옵션은 기본으로 켜져 있다.
회의를 거의 다 들으면 대화가 잠시 끊기는 지점에서 모두 인사하고,
2.5~5초 뒤 지금 시간대에 맞는 다른 회의로 넘어간다.
이번 세션에서 아직 듣지 않은 회의를 먼저 고른다.
옵션을 끄면 같은 회의가 반복된다.

### 캘린더 차단

회의를 고르고 제목, 날짜, 시작 시각, 길이, 반복 여부를 정하면
캘린더 일정을 만들어 준다.
길이는 15분에서 1시간 30분까지이고, 반복은 없음, 평일마다, 매주 중에서 고른다.
기본 길이는 Engineering Standup이 15분,
Quarterly All-Hands와 IT Incident War Room이 1시간, 나머지가 30분이며,
Engineering Standup은 기본으로 평일마다 반복한다.
기본 시작 시각은 10분 이상 뒤의 15분 단위 시각이고,
그 시각이 회의 시간대를 벗어나면 다음 평일 아침으로 잡힌다.

홈페이지는 내려받는 `.ics` 파일이 브라우저에서 만들어지고,
서버로 전송되지 않는다고 밝힌다.
일정에는 시간대 정의, 시작 5분 전 알림, 바쁨 상태가 들어가고,
참가 링크를 넣으면 `?m=<회의>&v=<억양>` 주소가 위치와 설명에 들어간다.
알림이 떴을 때 이 링크를 열면,
이름을 확인하는 대기실을 거쳐 바로 그 회의에 들어간다.
비공개로 표시하면 동료에게는 바쁨만 보인다.
Google Calendar 버튼은 반복 일정까지 넘기지만,
Outlook 버튼은 단일 일정만 추가한다.

### 휴대전화에서 쓰기

휴대전화에서는 브라우저의 홈 화면에 추가 기능으로 설치하면,
주소창 없이 전체 화면으로 열린다.
웹 앱 매니페스트의 짧은 이름과 iOS 홈 화면 제목은 Fleeting이 아니라 Meeting이다.

## 광고와 후원

### 두 가지 상품

광고 안내 페이지는 두 가지 상품을 판다.
하나는 회의 출연진이 대화 중에 20~45초 동안 제품을 자연스럽게 언급하는 방식이다.
문구는 Fleeting이 쓰고 후원사가 한 단어까지 승인하며,
회의의 원래 출연진과 억양으로 녹음되고,
재생되는 동안 화면에 “Sponsored by” 표시가 뜬다.
다른 하나는 회의를 떠날 때 보이는 종료 화면의 후원 카드로,
회의 하나에 후원사 하나만 받는다.

후원은 월 단위로 회의 하나 또는 열한 개 전체에 걸 수 있다.
예산 선택지는 250파운드 미만부터 1,000파운드 이상까지이고,
초기 후원사에게는 창립 요율을 준다고 한다.
신청서는 브라우저에서 짧은 메모와 전체 브리프로 만들어지며,
짧은 메모는 LinkedIn 연결 요청에 들어가도록 300자 이내로 맞춘다.
페이지 하단의 연락처 칸은 아직 “Contact details coming soon.”이다.

### 재생 규칙

후원 언급은 회의 시작 후 45초가 지나기 전에는 나오지 않는다.
그 뒤 대화가 1초 이상 끊기는 지점에서 본 녹음을 줄이고 언급 클립을 재생한 다음,
원래 회의로 돌아간다.
한 바퀴 재생에 한 번만 나온다.

현재 후원 목록에는 두 곳이 있다.
Acme Audio는 광고 안내 페이지의 예시용 가상 브랜드로,
실제 재생 대상에서는 빠진다.
남은 하나는 만든 사람의 회사인 Splinters이며, IT Incident War Room,
Vendor Security Review, AppSec Review의 British 판에 언급이 들어 있다.
후원 카드가 없는 회의의 종료 화면에는
이 자리에 로고를 올리라는 자체 광고가 뜬다.

광고 안내 페이지의 원칙은 네 가지다.
모든 후원은 영국 광고 규정에 따라 화면에 Sponsored로 표시하고,
언급 속 주장은 사실이고 근거가 있어야 하며,
추적 쿠키나 제3자 스크립트를 쓰지 않고,
회의나 청취자에게 맞지 않는 광고는 거절한다.
후원사 링크에는 클릭을 셀 수 있도록 `utm_source=fleeting` 태그가 붙는다.

## 개인정보

처리방침은 개인 정보를 수집하지 않는다고 말한다.
브라우저 로컬 스토리지에 타일에 표시할 이름, 억양 선택,
보내지 않은 후원 브리프가 남고, 연속 회의 옵션의 켜짐 여부도 함께 저장된다.
사이트와 오디오는 Cloudflare가 제공하고 글꼴은 Google Fonts에서 받으므로,
두 곳은 IP 주소 같은 요청 정보를 받는다.

사이트의 콘텐츠 보안 정책은
스크립트와 네트워크 연결을 자기 도메인으로만 제한한다.
제3자 광고 스크립트가 없다는 처리방침의 설명과 맞는다.
HN 공개 직후 `splintersio`는
사용자 경험을 위해 AdSense를 껐다고 적었다[^splintersio].

## 트레이드오프

### 사실감은 어디까지 필요한가

HN에서 가장 많이 나온 지적은 사실감이었다.
0xR1CK는 말이 겹치는 순간이 없고 한 음성이 끝나면 바로 다음 음성이 나오며,
합성 음성 특유의 지나치게 또렷한 발음이라 자연스럽지 않다고 했다[^0xR1CK].
kazinator는 전문 방송인이 회의를 연기하는 것 같다며, 실제 회의에는 말버릇,
헛기침, 마이크 잡음, 음성 감지로 잘리는 말이 있다고 덧붙였다[^kazinator].
jonwinstanley는 사람이 가짜를 알아보는 데 아주 능하다며 실제 사람의 녹음 조각을
쓰는 편이 낫겠다고 했다[^jonwinstanley].

반론은 위장이 얇아도 된다는 것이었다.
saulpw는 1980년대 게임의 상사 화면처럼, 잠깐 말을 걸어도 되는지 살피러 온 사람을
돌려보낼 정도면 충분하다고 했다[^saulpw].
tacostakohashi도 MS-DOS 시절 게임에서 화면을 가짜 스프레드시트로 바꾸던 상사
키를 이번 세기에 맞게 고친 것 같다고 했다[^tacostakohashi].
cantrevealname은 수십 년 전,
공중전화로 상사나 배우자에게 전화하며 정비소 소음 같은 배경음을 트는
카세트테이프가 실제 상품으로 팔렸다고 적었다[^cantrevealname].

이 서비스가 주는 것은 회의 내용이 아니라,
지나가던 사람이 다가오기를 망설이게 만드는 신호다.
그 신호에는 귀 기울여 들었을 때의 사실감보다
멀리서 들었을 때의 분위기가 더 중요하다.
그래서 사실감을 높이는 일은 생각만큼 이득이 크지 않고 비용은 분명하다.
kazinator가 원한 말버릇, 끊김, 잡음은 틀어 둔 본인도 피곤하게 만드는 요소다.
FAQ가 Realistic을 지우고 Plausible로 고친 것은
이 둘 사이에서 앞쪽을 포기했다는 뜻으로 읽힌다.
이것은 해석이다.

### 위장이 강할수록 본인의 집중도 깨진다

신호가 강하려면 사람 목소리가 또렷하게 들려야 하는데,
사람 목소리는 틀어 둔 본인의 집중도 깬다.
bartread는 API Design Review를 옆에서 틀어 두면
다른 일에 집중할 수 없을 만큼 신경 쓰인다며,
사람 목소리는 여럿이 섞여 웅성거림이 되기 전까지는
주의를 빼앗는다고 했다[^bartread].
voidUpdate는 애초에 사무실에서
회의를 스피커로 크게 트는 사람이 있느냐고 물었다[^voidUpdate].
스피커로 틀면 본인도 듣게 되고, 볼륨을 줄이면 위장이 약해진다.
이 둘을 함께 얻는 방법은 없고,
고를 수 있는 것은 어느 쪽을 얼마나 양보하느냐뿐이다.

### 캘린더 차단은 소리보다 오래 남는다

소리는 틀어 둔 순간에만 효과가 있지만,
캘린더 일정은 다른 사람이 회의를 잡으려고 내 일정을 볼 때마다 작동한다.
HN의 경험담도 대부분 소리가 아니라 일정으로 시간을 지킨 이야기였다.
alexpotato는 SRE 팀원들이 회의 요청에 시달리자,
매주 금요일 오전 8~11시에 팀 회의를 잡아
집중 시간을 만들어 줬다고 했다[^alexpotato].
glenngillen은 같은 목적으로 “[IMPORTANT] CUSTOMER OUTAGE” 같은 제목의
일정을 잡았는데,
다른 부서가 그 위에 회의를 덮어 잡는 일을 겪었다고 했다[^glenngillen].
Fleeting은 일정에 참가 링크를 넣어 두 기능을 잇는다.

대가는 노출이다.
일정을 볼 수 있는 사람은 링크도 보므로,
링크를 누르면 가짜 회의라는 것이 바로 드러난다.
홈페이지도 이 점을 경고하며 링크를 빼거나 비공개로 표시하라고 권한다.
비공개로 하면 동료에게는 바쁨만 보여 안전하지만,
조직에 따라 비공개 일정이 잦은 것 자체가 눈에 띈다.

### 광고가 위장을 깰 수 있다

후원 언급은 출연진의 목소리로 회의 흐름 속에 들어가도록 설계되었다.
대화가 끊긴 지점에서만 나오고 한 바퀴에 한 번뿐이라 위장을 크게 해치지 않지만,
화면에는 Sponsored 표시가 뜬다.
옆에서 화면을 흘끗 본 사람에게 이 표시는 회의가 진짜가 아니라는 단서가 된다.
broken-kebab은 YouTube 회의 영상을 틀어 두면
언젠가 시끄러운 광고가 나와 들통날 것이라고 했다[^broken-kebab].
같은 종류의 위험이 형태만 바꿔 남는다.

광고 모델 자체에 대한 반응도 갈렸다.
franga2000은 장난 사이트의 수익화 전략으로는 최고라고 했고[^franga2000],
fyltr는 광고가 농담인지 묻고 은밀한 광고는 싫다고 했다[^fyltr].
출연진의 목소리로 제품을 언급하는 방식은
화면 표시가 없으면 곧 은밀한 광고가 된다.
소리만 듣는 사람에게는 Sponsored 표시가 보이지 않는다는 점에서,
표시 의무와 위장이라는 목적은 서로 부딪친다.

## 함정

- 첫 재생은 브라우저의 자동 재생 정책에 막힐 수 있다. 막히면 화면에 Join audio 버튼이 뜨고, 눌러야 소리가 난다.
- 억양이 없는 회의는 British로 바뀐다. 카드에 표시된 억양을 확인하지 않으면 고른 것과 다른 억양이 나온다.
- 연속 회의 옵션이 켜져 있으면 회의가 끝날 때 모두 작별 인사를 하고 몇 초 조용해진다. 그 사이에 누가 다가오면 회의가 끝났다고 보일 수 있다.
- 일정의 참가 링크에는 회의 종류와 억양이 주소에 그대로 들어간다. 일정 세부 정보가 공개된 캘린더라면 링크를 빼야 한다.
- Outlook 버튼은 반복을 넘기지 않는다. 평일마다 반복하려면 `.ics` 파일을 내려받아야 한다.
- 회사 관리 기기에서는 사이트가 막힐 수 있다. HN에서도 새로 등록된 도메인이라 회사 정책에 차단되었다는 보고가 있었다.
- 이름, 억양, 옵션은 로컬 스토리지에 남는다. 공용 기기에서 썼다면 사이트 데이터를 지워야 흔적이 사라진다.

## 기억할 원칙

### 경계를 지키는 도구는 경계를 말하지 못하는 조직을 드러낸다

Fleeting이 웃긴 이유는 실제로 쓸 사람이 있다는 것을 누구나 알기 때문이다.
“지금 집중하고 있다”는 말이 통하지 않고 “회의 중”이라는 말만 통하는 조직에서는,
회의가 시간을 지키는 유일한 공인된 이유가 된다.
그래서 가짜 회의는 회의가 너무 많다는 불만이 아니라,
회의가 아닌 일은 시간을 주장할 근거가 되지 못한다는 사실을 보여 준다.

수요가 실제로 있다는 증언도 이를 뒷받침한다.
frangonf는 GitLab의 보조 YouTube 채널에서
평범한 회의 영상의 조회수가 수백만이고,
가족이 혼자 두게 하려고, 또는 바쁜 척하려고 틀어 둔다는 댓글이
수천 개의 좋아요를 받았다고 전했다[^frangonf].
반면 ghusto는 일에 집중하고 싶다고 말하지 못한다면,
직장이나 본인에게 문제가 있다고 적었다[^ghusto].
두 말은 모순되지 않는다.
말하지 못하는 직장이 많다는 것이 바로 수백만 조회수의 이유다.

alexpotato의 팀원들은 집중 시간을 직접 잡아도 된다는 말에도,
팀장이 잡아야 무게가 있다고 답했다.
일정의 무게는 내용이 아니라 누가 잡았는지에서 나온다.
도구가 할 수 있는 일은 그 무게를 흉내 내는 데까지이고,
집중 시간을 일정으로 인정하는 규칙은 조직이 만들어야 한다.

---

[^splintersio]: <https://news.ycombinator.com/item?id=50020852>

[^roryirvine]: <https://news.ycombinator.com/item?id=50018424>

[^AIorNot]: <https://news.ycombinator.com/item?id=50026694>

[^splintersio-beta]: <https://news.ycombinator.com/item?id=50021284>

[^0xR1CK]: <https://news.ycombinator.com/item?id=50026386>

[^kazinator]: <https://news.ycombinator.com/item?id=50029230>

[^jonwinstanley]: <https://news.ycombinator.com/item?id=50019184>

[^saulpw]: <https://news.ycombinator.com/item?id=50028025>

[^tacostakohashi]: <https://news.ycombinator.com/item?id=50019334>

[^cantrevealname]: <https://news.ycombinator.com/item?id=50025034>

[^bartread]: <https://news.ycombinator.com/item?id=50022598>

[^voidUpdate]: <https://news.ycombinator.com/item?id=50019427>

[^alexpotato]: <https://news.ycombinator.com/item?id=50020900>

[^glenngillen]: <https://news.ycombinator.com/item?id=50022829>

[^broken-kebab]: <https://news.ycombinator.com/item?id=50019404>

[^franga2000]: <https://news.ycombinator.com/item?id=50023093>

[^fyltr]: <https://news.ycombinator.com/item?id=50021187>

[^frangonf]: <https://news.ycombinator.com/item?id=50019063>

[^ghusto]: <https://news.ycombinator.com/item?id=50020031>
