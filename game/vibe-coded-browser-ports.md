# AI로 디컴파일한 게임 브라우저 이식판은 잘 돌아가고, 그래서 문제다

원문: [Vibe-Coded Browser Ports Of Games Work Perfectly, Unfortunately](https://kotaku.com/we-might-be-cooked-as-these-vibe-coded-web-browser-ports-of-halo-the-simpsons-hit-and-run-and-gta-vice-city-seem-to-work-perfectly-2000743300)

HN 토론: <https://news.ycombinator.com/item?id=50035561> (105점, 80개 댓글)

GN 토론: <https://news.hada.io/topic?id=35192>

## 요약

Kotaku의 Lewis Parker가 2026년 10월 9일에 쓴 짧은 칼럼이다.
글은 지난 몇 주 사이 바이브 코딩과 AI 디컴파일로 만든 에뮬레이터와 게임이
수백 개 쏟아졌다는 관찰로 시작한다.
저자는 그 원인을 Claude Opus 5.5의 뛰어난 디컴파일 능력으로 본다.
예전에는 몇 달 걸리던 게임 코드 재구성이 이제 기록적인 시간에 끝나고,
최근 화제가 된 Fallout과 Call of Duty: Modern Warfare의 “네이티브” 이식판,
Elden Ring 안에 Super Mario 64를 넣은 AI 생성 모드도 그 결과라는 것이다.

저자가 가장 우려스럽다고 꼽는 사례는 브라우저 이식판이다.
Twitter 계정 @RadiantOpti가 10월 8일 올린 트윗은 Black Ops 좀비 모드,
Skate 3, Halo, MW2 등을 게임 설치 없이 브라우저 탭에서 할 수 있다고 소개했다.
저자는 Call of Duty: Black Ops, Halo: CE, Grand Theft Auto: Vice City,
Skate 3, The Simpsons: Hit and Run의 브라우저 이식판을 직접 해 봤고,
몇몇은 거의 흠이 없었다고 적는다.
The Simpsons: Hit and Run은 어릴 적 기억에 없던 240fps까지 노렸고,
서로 다른 Halo: CE 이식판 네 개 가운데 하나는 온라인 서버가 동작했으며
핑도 낮았다.

기술적 설명은 메모리에 기댄다.
이식된 게임 대부분이 PS2나 PS3 시대 작품인데,
PS3의 RAM은 약 512MB이고 저자의 브라우저는 지금 약 1,200MB를 쓰고 있다.
브라우저 이식은 오래전부터 RAM의 제약을 받지 않았고,
달라진 점은 코드를 한 줄씩 손으로 뜯어보는 대신
밤새 돌려 둘 수 있는 AI가 생겼다는 것이라고 말한다.

결론은 법적 대응의 한계다.
Take-Two나 Microsoft의 변호사가 중지 요청서를 보내 내리게 할 수는 있지만,
이렇게 쉽고 빠르게 만든 이식판이라면 누군가 또 만들 것이다.
저자는 이를 해적판 DVD 이후 처음 보는 규모의 지식재산권 두더지 잡기라고
부르고,
앞으로 게임 퍼블리셔 법무팀이 한동안 야근하게 될 것이라는 말로 글을 맺는다.

## 분석

### 글의 주장은 “만들기 쉬워졌다”와 “잘 돌아간다”라는 두 다리에 서 있다

저자의 우려는 두 사실이 겹치는 데서 나온다.
하나는 제작 비용의 붕괴다.
몇 달 걸리던 작업이 밤새 끝난다면 내려도 다시 올라온다.
다른 하나는 품질이다.
조악한 결과물이었다면 퍼블리셔가 걱정할 이유가 적었겠지만,
240fps로 돌고 온라인까지 되는 이식판은 정품의 대체재가 된다.
제목의 “불행하게도”는 이 두 번째 사실을 인정해야 하는 불편함을 가리킨다.

HN에서 sublinear는 LLM이 이 일을 잘하는 것이 놀랍지 않다고 했다.
바이너리는 원래 진정한 해자가 아니었고,
옮기는 데 드는 고된 노동이 해자였다는 것이다.[^sublinear]
teaearlgraycold은 기존 소스를 컴파일해 순서를 뒤집기만 하면
디컴파일 학습 데이터를 얼마든지 만들 수 있다고 설명했고,[^teaearlgraycold]
j2kun이 30년간 쓰인 컴파일러의 다양성을 반론으로 들자
Pannoniae는 현대 게임은 MSVC나 GCC로 수렴하고 버전도 몇 함수를 대조하면
찾을 수 있으며,
1990년대 이전 게임은 컴파일러가 다양해도
프로그램 자체가 작다고 답했다.[^Pannoniae]
수작업 역공학이 불가능할 만큼 프로그램이 커진 시점에는
컴파일러 지형이 이미 정리되어 있었다는 지적이다.

### 메모리 설명은 엉뚱한 축을 짚는다

저자는 PS3의 512MB와 브라우저의 1,200MB를 대비하지만,
PS2·PS3 게임을 브라우저로 옮기는 데 걸림돌은 메모리 용량이 아니었다.
PS2의 MIPS 계열 CPU와 벡터 유닛,
PS3의 Cell 프로세서는 PC와 구조가 전혀 달라서,
에뮬레이터는 이를 실시간으로 흉내 내느라 큰 비용을 치렀다.
AI가 바꾼 것은 이 명령어 집합을 미리 고수준 코드로 옮기고
입출력 계층을 갈아 끼우는 노동의 비용이다.

genxy는 이 차이를 용어로 정리했다.
디컴파일은 같은 툴체인으로 비트 단위까지 같은 바이너리를 다시 만들 수 있는
소스를 복원하는 일이고,
리컴파일은 PPC 인터프리터 같은 것을 고수준 코드로 풀어 현대 툴체인에서
다루게 한 뒤 그래픽·컨트롤러·네트워크 계층을 교체하는 일이다.
지금 사람들이 하는 일은 대부분 리컴파일이며,
AI 이전에도 이를 위한 SDK가 있었다고 덧붙였다.[^genxy]
이 저장소의 [PS2 Web Recomp](ps2-web-recomp.md) 문서가 다루는 정적
재컴파일이 바로 그 방식이다.

성능 쪽 질문에도 답이 나왔다.
YuechenLi가 WebAssembly와 WebGPU의 오버헤드를 묻자,[^YuechenLi]
Jcampuzano2는 대상 게임이 지금보다 한 자릿수 이상 약한 하드웨어용으로
만들어졌으니 오버헤드가 커도 충분히 돈다고 답했다.[^Jcampuzano2]
jeroenhd는 CPU가 약하기로 유명한 Pixel 9 Pro에서 Skate 3가 45fps로
돌았다고 전했다.[^jeroenhd]
저자가 메모리로 설명하려던 현상의 실제 배경은
20년 사이 벌어진 연산 성능 격차다.

### 저작권 프레임은 기존 해적판과의 차이를 설명하지 못한다

글은 이 현상을 지식재산권 보호의 위기로 읽는다.
그러나 sobiolite는 이런 브라우저 이식판이 에뮬레이터용 롬 파일을
호스팅하는 것보다 더 불법적이지도 덜 불법적이지도 않고,
사이트를 내리는 난이도도 기존 해적판 사이트와 같다고 반박했다.[^sobiolite]
더 흥미로운 것은 원본 데이터 파일을 가져와 고해상도, 프레임 제한 해제,
버그 수정이 들어간 엔진에서 합법적으로 옛 게임을 즐길 수 있게 됐다는 점이고,
최근 몇 달 사이 소스가 유실된 DOS 게임의 이식판을 여럿 봤다고 했다.

이 구분은 실제 사례에서도 갈린다.
theturtletalks는 Halo CE와 God of War 이식판이 롬을 직접 가져오게 하므로,
정품 디스크에서 직접 뽑은 롬으로 하는 것은
불법이 아니라고 했다.[^theturtletalks]
cwnyth는 The Simpsons 이식판은 롬을 요구하지 않는다고 짚었다.[^cwnyth]
즉 저자가 한데 묶은 사례들 안에 합법과 불법이 섞여 있고,
글은 그 경계를 긋지 않는다.

## 비평

### “완벽하게 돌아간다”는 판정에는 기준이 없다

저자의 품질 판정은 몇 개 이식판을 잠깐 해 본 인상에 기댄다.
240fps와 낮은 핑은 인상적이지만,
원작과 같은 동작을 하는지는 다른 질문이다.
물리 계산이 프레임률에 묶여 있던 게임을 240fps로 돌리면 동작이 바뀔 수 있고,
AI가 재구성한 코드는 처음 몇 분이 멀쩡해도 후반부 특정 분기에서
원작과 다르게 갈 수 있다.
저자는 끝까지 해 보지 않았고,
원작과 비교하는 방법도 제시하지 않는다.

mschuster91은 이것이 게임 그 자체인지,
아니면 게임이 어때야 한다는 기계의 추정인지 물었다.
기존 디컴파일·리컴파일 커뮤니티는 자기 한계를 알았지만,
챗봇은 “다 됐다”고 말하며 쓰레기 더미를 내놓을 수 있다는 것이다.[^mschuster91]
VCFundedGenYer는 이런 프로젝트가 디컴프·리컴프의 이름을 더럽힌다고
비판했지만,[^VCFundedGenYer]
sigmar는 LLM 이전에는 완전히 플레이할 수 있는 리컴프가 거의 없었다고
반박했다.[^sigmar]
두 주장은 모두 맞을 수 있다.
그래서 필요한 것은 인상이 아니라 검증 기준인데,
글은 “거의 흠 없다”는 감상으로 그 자리를 메운다.

### 해적판 DVD 이후 최대라는 비교는 에뮬레이션의 역사를 건너뛴다

저자는 이것을 해적판 DVD 이후 처음 보는 규모의 두더지 잡기라고 부른다.
하지만 게임 업계는 이미 25년 넘게 에뮬레이터, 롬 사이트, 브라우저 에뮬레이터와
씨름해 왔다.
PS2 에뮬레이터 PCSX2만 해도 오래전부터 원작보다 높은 해상도와 프레임률을
제공했고,
퍼블리셔는 에뮬레이터 자체가 아니라 롬 배포를 주로 겨냥해 왔다.
미국 법원은 2000년 Sony 대 Connectix 판결에서 에뮬레이터를 만들기 위한
역공학을 공정 이용으로 봤다.

이 역사를 놓으면 질문이 달라진다.
새로운 것은 게임을 브라우저에서 돌릴 수 있다는 사실이 아니라,
에뮬레이터라는 중간층 없이 게임별 이식판이 대량으로 생긴다는 점이다.
이식판에는 원작 코드를 재구성한 결과물이 들어가므로,
원작 데이터만 요구하는 에뮬레이터보다 저작권 논리상 더 취약하다.
kevinmchugh는 디컴파일해 명세를 쓰는 단계와 명세로 구현하는 단계를 나누면
미국에서 합법인 클린룸 역공학처럼 보인다고 했지만,[^kevinmchugh]
두 단계를 같은 모델이 연달아 수행한다면 “깨끗한 방”이라는 전제가 성립하는지가
새로운 쟁점이 된다.
글은 이 지점을 다루지 않고 DVD라는 엉뚱한 비교로 넘어간다.

### 모델의 안전장치라는 변수가 빠져 있다

저자는 AI가 이 일을 해 주는 것을 주어진 조건으로 둔다.
그러나 swingboy가 물었듯 모델이 “당신 코드가 아니다”라며 거부할 수도
있다.[^swingboy]
serf는 권한이 있다고 주장하면 대부분 쉽게 우회된다고 했고,[^serf]
게임 제작 수업을 하는 ModernMech는 스펀지밥 이미지를 거부당한 학생이
교육 목적이라고 말하자 Gemini가 바로 만들어 줬다고 전했다.[^ModernMech]
반대로 barbacoa는 자기 회사 기기의 펌웨어 작업을 할 때마다
권한이 있다고 상기시켜야 할 만큼 자주 막힌다고 했다.[^barbacoa]

이 비대칭은 글의 결론을 흔든다.
저자는 법무팀이 야근할 것이라고 예측하지만,
실제 압력은 퍼블리셔가 이식판 사이트보다 모델 제공자에게 거는 쪽으로
갈 수 있다.
tiborsaas는 프런티어 모델이 역공학을 거부하도록 바뀌어 시간을 벌겠지만,
오픈 웨이트 모델을 미세 조정하면 그것도 소용없을 것이라고 내다봤다.[^tiborsaas]
글이 그린 두더지 잡기의 진짜 상대는 개별 사이트가 아니라 모델 정책일 수 있다.

## 인사이트

### 리마스터 사업 모델이 먼저 흔들리고, 퍼블리셔는 스트리밍으로 물러난다

mjr00은 왜 이것을 굳이 저작권 침해로 몰아가는지 분명하다고 했다.
퍼블리셔는 PS2 시절 게임을 다시 컴파일하고 와이드스크린과 컨트롤러 지원,
약간의 그래픽 개선을 더해 20년 된 게임을 60달러에 되팔아 왔다.
신작보다 일이 적고 팬층이 있어 위험도 적은 사업이다.[^mjr00]
AI 이식판이 정확히 그 작업을 공짜로 해 버리면,
타격을 먼저 받는 것은 신작이 아니라 옛 카탈로그의 재판매다.

그다음 반응은 배포 방식의 이동일 가능성이 크다.
rvz는 업계가 클라우드 게이밍을 다시 꺼내 들 것이라고 했고,[^rvz]
urbnspacecowboy는 Amazon Luna, GeForce Now, Xbox Cloud Gaming이
이미 그 길에 있다고 짚었다.[^urbnspacecowboy]
바이너리를 내려받지 못하게 하면 디컴파일할 대상도 없다.
그러나 그 대가는 소유의 소멸이고,
robotnikman의 말처럼 언제든 서비스를 내릴 수 있는 클라우드 전용 게임은
오히려 이식판의 명분을 키운다.[^robotnikman]

즉 AI 디컴파일의 2차 효과는 해적판의 증가보다
퍼블리셔가 바이너리를 손에서 놓지 않으려는 쪽으로 배포 구조를 바꾸는 데서
더 크게 나타날 수 있다.
DRM이 강해질수록 정품 이용자의 불편이 커졌던 역사가
스트리밍이라는 형태로 반복될 수 있다.

### 이번 일은 Napster보다 Phoenix BIOS에 가깝다

jarjoura는 소프트웨어가 Napster의 순간을 맞았다고 했다.
다만 Napster 때는 음반 업계가 한목소리로 소송을 걸었지만,
이번에는 이해관계가 다른 수백 곳의 권리자가 있다는 점이
다르다고 봤다.[^jarjoura]
하지만 기술적으로 더 가까운 선례는 1980년대 IBM PC BIOS의 클린룸 재구현이다.
Phoenix Technologies는 BIOS 동작을 명세로 쓰는 팀과
그 명세만 보고 구현하는 팀을 분리해 저작권 소송을 피했고,
그 결과 PC 호환기 시장이 열렸다.

AI 디컴파일은 이 두 팀을 한 모델 안에 넣는다.
명세 작성자와 구현자가 분리되어야 한다는 클린룸의 핵심 조건을
기계가 어떻게 만족할 수 있는지에 대한 법적 답은 아직 없다.
Napster의 비유는 배포의 문제를 보지만,
Phoenix의 비유는 재구성 행위 자체가 합법인지를 묻는다.
퍼블리셔가 이길 수 있는 싸움은 앞쪽이고,
판례가 새로 쓰여야 하는 싸움은 뒤쪽이다.

spwa4는 AI 학습에 남의 저작물을 쓰는 것은 허용되면서
개인의 복제는 엄벌하는 이중 기준을 비판하며,
결국 의회가 저작권을 포기하든 AI 학습과 출력까지 범위를 넓히든
선택하게 될 것이라고 내다봤다.[^spwa4]
게임 이식판은 그 선택을 앞당기는 사례가 될 수 있다.

### 디컴프 커뮤니티의 가치는 결과물에서 검증 능력으로 옮겨 간다

jeroenhd는 이런 프로젝트를 실용적 도구보다 예술로 봤다고 했다.
과정을 자동화하면 유일하게 흥미로운 부분이 사라지고,
모나리자는 보러 갈 가치가 있지만 모나리자 사진은 일주일짜리 배경화면이라는
것이다.[^jeroenhd-art]
Jcampuzano2는 반대로 디컴프의 목적은 처음부터 사람들이 게임을 하게 하는
것이었다고 반박했다.[^Jcampuzano2-point]

두 입장의 긴장은 결과물의 희소성이 사라질 때 무엇이 남느냐로 정리된다.
이식판을 만드는 일이 싸지면,
값비싼 것은 그 이식판이 원작과 같은지를 판정하는 일이다.
genxy는 게임을 에뮬레이터 아래에서 돌리며 실시간 차분 디버깅과 화면 비교를
하는 에이전트 하네스가 나올 것이라고 내다봤다.[^genxy]
비트 단위로 같은 바이너리를 다시 만든다는 기존 디컴프 커뮤니티의 기준이
바로 그 판정 도구 역할을 할 수 있다.

그러면 커뮤니티의 역할은 손으로 코드를 옮기는 장인에서
AI가 만든 이식판을 검증하고 원작과의 차이를 문서화하는 감수자로 바뀐다.
awongh가 물은 것처럼 모델이 어떤 실수를 할 수 있고 결과물이 실제로
어떤 모양인지 아는 사람은 여전히 드물다.[^awongh]
“잘 돌아간다”는 감상을 “원작과 같다”는 판정으로 바꾸는 능력이
다음 몇 년 동안 이 분야에서 가장 희소한 기술이 될 것이다.

### 2000년대 게임이 가장 먼저, 가장 많이 풀린다

이식판이 PS2·PS3 시대 작품에 몰리는 데에는 이유가 있다.
그 시대 게임은 현대 기기에서 오버헤드를 감당할 만큼 가볍고,
프로그램 규모는 수작업 역공학이 버거울 만큼 커서 그동안 손대기 어려웠으며,
Pannoniae의 말대로 컴파일러는 이미 MSVC와 GCC로 정리되어 있었다.[^Pannoniae]
AI가 비용을 낮추자 이 구간이 한꺼번에 열린 것이다.

반면 최신 게임은 사정이 다르다.
서버 측 로직과 온라인 서비스에 핵심이 있고,
안티치트와 DRM이 바이너리를 감싸며,
요구 성능이 브라우저의 오버헤드를 감당할 만큼 낮지 않다.
user43928은 Rockstar가 GTA VI의 PC판을 너무 늦게 내면
커뮤니티가 더 나은 이식판을 먼저 만들지도 모른다고 했지만,[^user43928]
그러려면 먼저 PC 바이너리가 있어야 한다.

결국 AI 디컴파일의 영향은 게임 역사 전체에 고르게 퍼지지 않는다.
한 세대 전의 카탈로그가 가장 먼저 사실상 공공재처럼 풀리고,
퍼블리셔는 그 세대를 리마스터로 되파는 대신
스트리밍과 서비스형 게임으로 방어선을 옮길 것이다.
게임 보존의 관점에서는 득이고,
옛 카탈로그를 수익원으로 삼던 사업에는 실이다.

---

[^sublinear]: <https://news.ycombinator.com/item?id=50035999>

[^teaearlgraycold]: <https://news.ycombinator.com/item?id=50036797>

[^Pannoniae]: <https://news.ycombinator.com/item?id=50038811>

[^genxy]: <https://news.ycombinator.com/item?id=50036500>

[^YuechenLi]: <https://news.ycombinator.com/item?id=50036586>

[^Jcampuzano2]: <https://news.ycombinator.com/item?id=50036628>

[^jeroenhd]: <https://news.ycombinator.com/item?id=50036832>

[^sobiolite]: <https://news.ycombinator.com/item?id=50036130>

[^theturtletalks]: <https://news.ycombinator.com/item?id=50036732>

[^cwnyth]: <https://news.ycombinator.com/item?id=50036912>

[^mschuster91]: <https://news.ycombinator.com/item?id=50036849>

[^VCFundedGenYer]: <https://news.ycombinator.com/item?id=50036250>

[^sigmar]: <https://news.ycombinator.com/item?id=50036558>

[^kevinmchugh]: <https://news.ycombinator.com/item?id=50036837>

[^swingboy]: <https://news.ycombinator.com/item?id=50036097>

[^serf]: <https://news.ycombinator.com/item?id=50036132>

[^ModernMech]: <https://news.ycombinator.com/item?id=50036156>

[^barbacoa]: <https://news.ycombinator.com/item?id=50036316>

[^tiborsaas]: <https://news.ycombinator.com/item?id=50036137>

[^mjr00]: <https://news.ycombinator.com/item?id=50036182>

[^rvz]: <https://news.ycombinator.com/item?id=50036058>

[^urbnspacecowboy]: <https://news.ycombinator.com/item?id=50037065>

[^robotnikman]: <https://news.ycombinator.com/item?id=50036379>

[^jarjoura]: <https://news.ycombinator.com/item?id=50036855>

[^spwa4]: <https://news.ycombinator.com/item?id=50041516>

[^jeroenhd-art]: <https://news.ycombinator.com/item?id=50036884>

[^Jcampuzano2-point]: <https://news.ycombinator.com/item?id=50036465>

[^awongh]: <https://news.ycombinator.com/item?id=50044307>

[^user43928]: <https://news.ycombinator.com/item?id=50037940>
