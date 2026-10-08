# C++ 게임 엔진 100선, 목록이 오래 살아남을 때 생기는 일

원문: [Best C++ Game Engines and Games Made in C++ (100+ Engines, 2026)](https://www.mycplus.com/game-development/game-engines/top-100-game-engines-c-cpp/)

## 요약

MYCPLUS는 Muhammad Saqib이 2004년부터 운영해 온 C/C++ 학습 사이트이고,
이 글은 그가 C와 C++로 작성된 게임 엔진을 한 페이지에 모은 디렉터리다.
페이지 메타데이터 기준으로 처음 게시된 날은 2019년 12월 29일이고,
마지막 수정일은 2026년 8월 25일이다.
제목에는 “100+ Engines, 2026”이 붙어 있다.

글은 게임 엔진이 무엇인지부터 설명한다.
엔진은 그래픽 렌더링, 물리, AI, 오디오, 애니메이션, 네트워킹, 에셋 관리를
맡는 소프트웨어 프레임워크이고,
C나 C++로 작성된 엔진은 성능과 하드웨어 제어, 확장성 덕분에 콘솔 게임,
대형 오픈 월드, 경쟁 멀티플레이 게임에서 선호된다고 말한다.
Unreal Engine 5, CryEngine, id Tech를 예로 들며,
Unreal 공식 C++ 프로그래밍 문서를 근거로 게임플레이와 엔진 시스템이 C++로
직접 작성된다고 덧붙인다.

본론은 세 개의 표와 하나의 큰 디렉터리로 이루어진다.
첫 표는 C++로 만든 유명 게임 10개와 그 엔진, 스튜디오다.
Fortnite(Unreal Engine), The Witcher 3(REDengine), Crysis(CryEngine 2),
Half-Life 2(Source), Doom Eternal(id Tech 7) 같은 조합이다.
둘째 표는 “Top 10 C++ Game Engines Comparison”으로,
엔진마다 용도, 난이도(별 다섯 개 척도), 라이선스, 학습 기간을 적었다.

| 엔진            | 용도              | 라이선스(원문 표기)    | 학습 기간(원문 표기) |
| --------------- | ----------------- | ---------------------- | -------------------- |
| Unreal Engine 5 | AAA Games         | Free (5% royalty $1M+) | 4-6 months           |
| Unity           | Cross-Platform    | Free (Pro available)   | 2-4 months           |
| Godot           | Indie/Learning    | Free Forever           | 1-3 months           |
| CryEngine       | Visual Quality    | Subscription           | 4-5 months           |
| Cocos2d-X       | 2D Mobile         | Free Forever           | 2-3 months           |
| Blender         | 3D Assets         | Free Forever           | 3-5 months           |
| Lumberyard      | Cloud/Multiplayer | Free (AWS)             | 4-6 months           |
| Source 2        | Multiplayer       | Free (Valve)           | 3-5 months           |
| Frostbite       | AAA Action        | Proprietary            | 5-7 months           |
| id Tech 7       | High Performance  | Proprietary            | 6-8 months           |

디렉터리는 “100 game engines written in C and C++”를 아홉 범주로 나눈다고
소개한다.
각 행은 엔진 이름, 대표 게임, 지원 플랫폼 세 칸이고,
대부분의 이름은 같은 사이트의 엔진별 개별 페이지로 연결된다.
범주별 행 수를 직접 세면 다음과 같다.

| 범주(원문)                 | 행 수 | 대표 항목                                        |
| -------------------------- | ----- | ------------------------------------------------ |
| AAA & Industry-Standard    | 26    | Unreal 1~5, CryEngine 1~V, Anvil 계열, Frostbite |
| Open-Source                | 11    | Godot, OGRE, Panda3D, Pyrogenesis, Urho3D        |
| 2D & Casual                | 9     | Adventure Game Studio, Cocos2d-X, StepMania      |
| Mobile-Optimized           | 4     | GamePlay3D, Marmalade, Moai SDK, Felgo           |
| Web-Based & HTML5          | 1     | Blend4Web                                        |
| Indie & Mid-Scale          | 14    | C4, Chrome Engine, Irrlicht, Torque3D            |
| Retro & Classic            | 19    | id Tech 1~8, GoldSrc, Dark Engine, Shark 3D      |
| Specialized & Niche        | 10    | Gamebryo, HPL 1~3, Source, Stockfish             |
| Educational & Experimental | 13    | Blender, Unity, Unigine, UDK, Banshee 3D         |
| 합계                       | 107   |                                                  |

글은 C++가 고수준 추상화와 저수준 제어 사이의 균형을 잡을 수 있고,
C++17, C++20, C++26으로 진화하면서 레이 트레이싱, VR, 실시간 전역 조명 같은
차세대 기술의 요구에 맞춰 간다고 정리한다.
맺음말은 C++를 배우면 성능 최적화, 메모리 관리, 엔진 구조, 실시간 시스템 설계,
멀티스레딩을 익힐 수 있고 엔진을 쓰는 데서 그치지 않고 직접 만들 수 있게 된다는
권유다.
마지막 FAQ 다섯 개는 초보자용으로 Godot, 모바일용으로 Unity와 Cocos2d-X를
추천하고, Godot(MIT), Cocos2d-X(Apache 2.0), Blender(GPL) 등은 상업적
사용에 제한이 없다고 답한다.

## 분석

### 이 글은 디렉터리이자 사이트의 허브 페이지다

표의 엔진 이름 대부분은 외부 공식 사이트가 아니라 MYCPLUS 안의 개별 엔진
페이지로 연결된다.
디렉터리 구간에서 서로 다른 내부 링크를 추려 보니 76개였고,
링크가 없는 행은 Urho3D, V-Play(Felgo), LumixEngine, Wintermute Engine,
Visual Pinball, Antara Gaming SDK, Unigine, WorldForge 여덟 개였다.
외부 링크는 Unreal 공식 C++ 문서 하나뿐이다.
따라서 이 글의 일차 역할은 독자에게 엔진을 고르게 하는 것보다
사이트 안의 엔진 페이지 수십 개를 하나로 묶는 허브에 가깝다.
같은 사이트의 개별 페이지 가운데 Shark 3D와 OGRE는 이 저장소에서
`game/shark-3d.md`, `game/ogre.md`가 따로 다룬다.

허브 페이지라는 성격은 글의 구성에도 드러난다.
도입부와 맺음말은 “게임을 만들고 싶다면 C++를 배우라”는 학습 동기 부여이고,
FAQ는 검색에 자주 걸리는 질문 형태다.
2019년에 만든 목록 위에 2026년의 도입부, 비교표, 원형 그래프와 연표 이미지,
FAQ를 덧붙여 제목의 연도만 갱신해 온 구조로 읽힌다.
이것은 해석이지만, 대표 게임 칸이 2025년 작품(id Tech 8의 Doom: The Dark Ages,
Anvil의 Assassin's Creed Shadows)까지 갱신된 행과 2010년대 초반에서 멈춘
행이 섞여 있다는 점이 그 근거다.

### 분류 축이 하나가 아니다

아홉 범주는 같은 기준으로 나눈 것이 아니다.
“AAA”는 시장 위치, “Open-Source”는 라이선스, “2D”는 차원, “Mobile”과
“Web”은 배포 대상, “Retro & Classic”은 시기, “Educational & Experimental”은
성숙도에 따른 분류다.
한 엔진이 여러 범주에 동시에 속할 수 있는데 표에서는 한 곳에만 놓이므로,
범주 배치가 사실상 임의가 된다.
그 결과 상용 엔진 Unity와 Unigine이 교육·실험용 칸에, 2025년 신작을 낸
id Tech 8이 레트로 칸에 놓인다.

이 축의 혼재는 목록형 글에서 흔한 실패다.
독자가 실제로 묻는 질문은 “내 프로젝트에 무엇을 쓸까”인데,
그 답에 필요한 축은 라이선스 조건, 유지 상태, 스크립팅 언어, 대상 플랫폼이다.
글은 이 중 플랫폼만 행마다 적고, 라이선스와 유지 상태는 Top 10 표와 FAQ에만
일부 적는다.

### 100이라는 숫자는 버전과 계열을 세는 방식에서 나온다

디렉터리의 실제 행은 107개다.
그런데 같은 엔진의 세대를 별도 행으로 센 경우가 많다.
Unreal Engine 1~5(그리고 UDK), CryEngine 다섯 행, id Tech 1~8,
Anvil 계열 네 행, HPL 1~3, Cube 두 행, Source 두 행, Cocos2d 두 행이다.
이 세대 행을 계열 하나로 묶으면 107행은 84개 계열로 줄어든다.

세대를 따로 세는 데는 나름의 이유가 있다.
같은 이름 아래에서도 세대가 바뀌면 지원 플랫폼과 대표 게임이 크게 달라지기
때문이다.
그러나 같은 표에서 Anvil, Anvil Next, Anvil Next 2.0을 셋으로 세면서
Unity나 Godot의 큰 세대 변화는 한 행으로 두는 것은 일관성이 없다.
숫자 100은 분류의 결과가 아니라 제목을 위해 맞춘 목표값에 가깝다.

### C++ 엔진이라는 범위가 흐려져 있다

글의 주장은 “고성능 게임은 C++ 엔진으로 만든다”이고 이것 자체는 업계 상식에
가깝다.
문제는 이 주장을 뒷받침하려고 목록에 들인 항목들이다.
Unity의 경우 글의 FAQ 스스로 Unity가 pure C++가 아니라 C#을 쓴다고 인정한다.
Godot 역시 FAQ에서 “가장 좋은 초보자용 C++ 엔진”으로 추천되는데,
추천 이유는 Python 비슷한 GDScript다.
즉 “C++로 작성된 엔진”과 “C++로 게임을 만드는 엔진”이 한 목록에 섞여 있다.

## 비평

### 표본 확인 방법

목록의 사실을 1차 자료와 대조하기 위해 2026년 10월 8일에 다음 방법으로
표본을 확인했다.
디렉터리의 내부 링크 76개는 `curl`로 모두 요청했고 전부 HTTP 200을 돌려주었다.
즉 링크가 깨진 곳은 없다.
엔진 상태는 GitHub API로 저장소의 보관(archived) 여부, 라이선스, 주 언어,
마지막 푸시 날짜를 확인했다.
대상은 Godot, Cocos2d-x, Urho3D와 후속 포크 U3D, Lumberyard와 O3DE,
Torque3D, OpenClonk, Aleph One, Panda3D, Horde3D, Exult, Stratagus,
StepMania, Delta Engine, LumixEngine, Toy, Stockfish, Moai, GamePlay3D,
Orx, Adventure Game Studio, Anura, Qfusion, Visual Pinball, WorldForge,
Spring과 후속 RecoilEngine, Frictional Games의 HPL1 저장소다.
그 밖에 Blender 2.80 릴리스 노트의 제거 기능 문서와 CRYENGINE 라이선스 안내
페이지를 읽었다.
Unreal Engine 라이선스 페이지는 자동 요청에 403을 돌려주어 확인하지 못했다.

### 링크는 살아 있지만 엔진은 죽어 있다

링크 상태만 보면 이 목록은 잘 관리된 것처럼 보인다.
그러나 링크가 가리키는 대상의 생존 여부는 표에 드러나지 않는다.
Amazon Lumberyard의 GitHub 저장소는 보관 상태이고, README 맨 위 안내문은
“Amazon Lumberyard is no longer offered”이며 후속작으로 Apache 라이선스의
Open 3D Engine(O3DE)을 권한다.
그런데 Top 10 표는 Lumberyard를 “Cloud/Multiplayer”용, “Free (AWS)”로 적고
학습 기간 4~6개월을 제시한다.
더 이상 제공되지 않는 엔진을 배우는 데 몇 달을 쓰라는 안내가 된다.

Urho3D도 비슷하다.
`urho3d/urho3d` 저장소는 보관 상태(마지막 푸시 2023년 1월)이고,
README 맨 위에는 러시아어로 된 안내가 있다.
하위 호환을 깨는 개발은 Dviglo 포크에서 진행된다는 내용이고,
그 아래에는 창시자 Lasse Öörni가 Turso3D를 만들고 있다는 안내가 있다.
활발한 후속 포크인 U3D(`u3d-community/U3D`)는 2026년 9월에도 푸시가 있었지만
목록에는 Urho3D라는 이름만 링크 없이 남아 있다.
Delta Engine의 저장소는 2017년, Toy는 2021년, Moai SDK는 2023년이
마지막 푸시였고, WorldForge의 서버 저장소 cyphesis는 보관 상태다.
Delta Engine 저장소는 GitHub가 집계한 주 언어가 C#이어서,
C/C++ 엔진 목록에 들어간 근거부터 의심스럽다.
반대로 Aleph One, Exult, Stratagus, Adventure Game Studio, Anura, Orx,
OpenClonk, Panda3D, Torque3D, LumixEngine, Visual Pinball은 2026년에도 커밋이
이어지고 있다.
“오래된 엔진”과 “버려진 엔진”이 같은 칸에 같은 형식으로 나열되어 있으니,
표만 보고서는 둘을 구별할 수 없다.

Blender는 더 직접적인 오류다.
Blender 2.80 릴리스 노트의 제거 기능 문서는
“The Blender Game Engine was removed”라고 적고 대안으로 Godot을 권한다.
Blender 저장소의 `v2.80` 태그 날짜는 2019년 7월 30일이므로,
이 목록이 처음 게시된 2019년 12월에 이미 Blender에는 게임 엔진이 없었다.
그런데 목록은 Blender를 Top 10에 넣고, 디렉터리에서는 Yo Frankie!와
Sintel The Game을 대표 게임으로 든다.
Top 10의 용도 칸이 “3D Assets”로 바뀐 것은 이 사실을 일부 반영한 흔적으로
보이지만, 그렇다면 Blender는 게임 엔진 목록에서 빠져야 한다.
GitHub 설명에서 스스로 “the best integrated game engine in Blender”라고 소개하는
UPBGE가 있으나 목록에는 없다.

### 라이선스 정보가 같은 사이트 안에서도 서로 어긋난다

FAQ는 Cocos2d-X가 Apache 2.0이라고 쓴다.
그러나 `cocos2d/cocos2d-x` 저장소의 `licenses/LICENSE_cocos2d-x.txt`는
“Permission is hereby granted, free of charge”로 시작하는 MIT 문구다.
더 흥미로운 점은 같은 MYCPLUS의 Cocos2d 개별 페이지가
Cocos2d-x를 “MIT-licensed”라고 적고,
2019년 4.0 이후 개발이 멈추어 Cocos Creator가 후속작이 되었다는 내용을
“Cocos2d-x Is Deprecated — Here's What Replaced It”이라는 절로 따로 다룬다는
것이다.
이 허브 페이지의 Cocos2d-X 행도 바로 그 절로 링크한다.
허브 페이지는 자기가 링크한 페이지가 폐기되었다고 말하는 엔진을
FAQ에서 2D 모바일 게임의 “optimal choice”로 추천한다.

CryEngine의 라이선스 칸은 “Subscription”이다.
그러나 CRYENGINE 공식 라이선스 안내는 5% 로열티 모델이며
프로젝트마다 연 매출 첫 5,000달러는 로열티가 없다고 적는다.
적어도 현재 공식 안내와는 맞지 않는 표기다.

### 대표 게임과 플랫폼 칸에는 확인 가능한 오류가 있다

HPL 엔진의 세 행은 서로 뒤섞여 있다.
HPL Engine 3 행은 Penumbra: Black Plague와 Penumbra: Requiem을 대표 게임으로
든다.
그러나 Frictional Games가 공개한 `HPL1Engine` 저장소의 README는
이것이 “the Engine that made the Penumbra Series”라고 밝히고,
`PenumbraOverture` 저장소 설명도 HPL1 엔진을 쓴다고 적는다.
첫 행(HPL Engine)에는 Penumbra: Requiem과 Soma가 함께 들어 있어
세대 구분 자체가 무너져 있다.

id Tech 8 행의 플랫폼에는 PlayStation 4가 들어 있다.
Doom: The Dark Ages는 2025년 5월 15일 PC, PlayStation 5, Xbox Series X|S로
나왔다고 출시 보도들은 적는다(웹 검색으로 확인).
이 보도들에 PS4판은 없다.
가장 최근에 갱신된 행에서도 이런 오류가 나온다는 것은,
갱신이 사실 확인보다 항목 추가 위주로 이루어졌음을 시사한다.

Stockfish 행은 분류 오류의 극단이다.
Stockfish 저장소의 설명은 “A free and strong UCI chess engine”이다.
체스 엔진은 수를 계산하는 탐색 프로그램이지 게임을 만드는 도구가 아니다.
“engine”이라는 낱말이 같다는 이유로 들어온 항목으로 보이며,
대표 게임 칸에 “Stockfish Chess, DroidFish, SmallFish”가 적힌 것도
그 엔진을 쓰는 체스 앱일 뿐이다.

### Top 10의 학습 기간과 난이도에는 근거가 없다

Top 10 표의 “4-6 months”, “6-8 months” 같은 학습 기간과 별점 난이도는
출처나 측정 방법 없이 제시된다.
FAQ도 “Godot 1-3개월, Unity 2-4개월, Unreal 4-6개월”을 반복할 뿐이다.
게다가 id Tech 7과 Frostbite는 FAQ 스스로 각각 Bethesda와 EA 내부 전용이라고
인정하는 엔진이다.
외부 개발자가 접근할 수 없는 엔진에 학습 기간을 매긴 것은
비교표의 칸을 채우기 위한 숫자로 읽힌다.

## 인사이트

### 목록형 글의 수명은 링크가 아니라 대상의 상태로 재야 한다

이 글의 링크 76개는 전부 살아 있었다.
일반적인 링크 검사기라면 이 페이지를 건강하다고 판정할 것이다.
그러나 실제로 낡은 것은 링크가 아니라 링크가 가리키는 세계, 즉
보관된 저장소, 제거된 기능, 바뀐 라이선스다.
내부 링크로 묶인 허브 페이지는 외부 링크 부패라는 가장 눈에 띄는 노후화
신호를 구조적으로 피하기 때문에 오히려 낡음이 더 오래 감춰진다.

목록을 관리하는 쪽에서 쓸 만한 대책은 행마다 “마지막 확인일”과
“상태(활발, 유지 보수, 보관, 단종)” 칸을 두는 것이다.
GitHub에 있는 엔진이라면 `archived`와 `pushed_at` 두 필드만으로도
상태 칸의 초안을 자동으로 채울 수 있다.
이번 표본 확인도 그 두 필드만으로 대부분의 판정을 내렸다.

### 엔진은 죽어도 이름은 포크와 후속작으로 옮겨 간다

Lumberyard는 O3DE로, Urho3D는 U3D와 Dviglo로, Cocos2d-x는 Cocos Creator로
이어졌다.
Beyond All Reason 팀이 유지하던 Spring 저장소(`beyond-all-reason/spring`)는
지금 RecoilEngine이라는 이름으로 넘어가 있다.
Blender Game Engine의 빈자리는 Blender에 통합된 게임 엔진을 표방하는 UPBGE가
잇고 있다.
오픈소스 게임 엔진의 일반적인 생애는 “단종”보다 “분기와 개명”에 가깝다.

이 점이 목록을 읽는 사람에게 주는 교훈은 단순하다.
목록에서 흥미로운 이름을 찾았다면, 그 이름을 그대로 검색하기보다
저장소에 들어가 README 첫 몇 줄과 보관 여부를 먼저 확인해야 한다.
Lumberyard와 Urho3D 모두 README 맨 위에서 후속작을 안내하고 있었다.
목록이 낡아도 원 저장소가 남긴 이정표는 대개 정확하다.

### “C++ 엔진”이라는 범주는 런타임 언어보다 확장 언어가 더 중요해졌다

이 목록이 Unity와 Godot을 C++ 엔진으로 묶는 데서 드러나는 긴장은
글이 놓친 더 큰 변화를 가리킨다.
오늘날 주요 엔진의 런타임은 거의 모두 C나 C++이므로,
“C++로 작성되었다”는 기준은 엔진을 구별하는 힘을 잃었다.
개발자가 실제로 마주하는 언어는 Unity의 C#, Godot의 GDScript,
Unreal의 C++와 Blueprint처럼 확장 계층의 언어다.

비유하자면 “C로 작성된 운영체제 100선”과 비슷하다.
거의 모든 운영체제가 C로 작성되었으니 그 목록은 운영체제를 고르는 데
도움이 되지 않는다.
엔진을 고르는 사람에게 필요한 범주는 “어느 언어로 게임 로직을 쓰는가”와
“엔진 소스를 고칠 수 있는가”이다.
C++를 배우라는 이 글의 권유가 설득력을 얻으려면, 게임 로직까지 C++로 쓰는
엔진(Unreal, O3DE, 그리고 이 저장소의 `game/raylib.md`가 다루는 raylib 같은
라이브러리)과 런타임만 C++인 엔진을 갈라 보여 주어야 했다.

### 연도만 갱신되는 목록은 검색 순위와 정확성 사이의 긴장을 드러낸다

제목의 “2026”과 2019년 게시일 사이에는 7년이 있다.
그동안 대표 게임 칸은 일부 갱신되었지만 엔진의 상태 칸은 생기지 않았다.
이것은 이 사이트만의 문제가 아니라 검색 유입에 의존하는 목록형 글의
일반적인 경제 구조로 보인다(해석).
제목의 연도를 바꾸고 FAQ를 붙이는 비용은 낮고 검색 노출 효과는 크지만,
107개 행을 하나씩 재검증하는 비용은 크고 그 효과는 독자 눈에 잘 띄지 않는다.

결과적으로 이런 목록은 시간이 지날수록 “역사 자료”로서의 가치는 커지고
“선택 안내서”로서의 가치는 줄어든다.
GoldSrc, Dark Engine, Jade, Shark 3D 같은 항목은 어떤 게임이 어떤 엔진으로
만들어졌는지 보여 주는 계보 자료로 여전히 유용하다.
이 글을 읽을 때는 대표 게임 칸을 계보 자료로 쓰고,
라이선스와 생존 여부는 반드시 원 저장소와 공식 페이지에서 다시 확인하는 것이
맞는 사용법이다.
