# Decomp Academy

<https://decomp-academy.dev>

<https://github.com/JackPriceBurns/decomp-academy-fe>

[Show HN: Decomp Academy – Learn to decompile GameCube games into matching C | Hacker News](https://news.ycombinator.com/item?id=48703412) (188점, 71개 댓글)

## 소개

jackpriceburns가 만들어 Show HN으로 공개한 GameCube PowerPC 어셈블리 역컴파일 학습 플랫폼이다.
게임 바이너리의 PowerPC 어셈블리를 바이트 단위로 일치하는 C 코드로 복원하는 방법을 256개 레슨으로 가르친다.
실제 Metrowerks CodeWarrior(MWCC) GC/2.0 컴파일러로 제출물을 실시간 검증하며,
Star Fox Adventures, 피크민 2, 메트로이드 프라임, 마리오 파티 4의 실제 함수를 교재로 사용한다.
완전히 무료이며 가입이 필요 없고 오픈소스다.

## 커리큘럼

4단계로 구성된다.

1단계 워밍업은 8개 레슨으로 레지스터 기초와 PowerPC 어셈블리 읽기를 소개한다. 약 36분 분량이다.

2단계 핵심 관용구는 159개 레슨으로 정수 산술, 비트 연산, 제어 흐름, 루프, 타입, 포인터, 구조체, 부동소수점을 다룬다.

3단계 실전 ABI는 75개 레슨으로 함수 호출 규약, 스택 프레임, 전역 변수, 컴파일러 최적화, 64비트 정수 연산을 다룬다.

4단계 증명의 장은 14개 레슨으로 단순 세터부터 완전한 상태 기계까지 실제 Star Fox Adventures 함수를 복원한다.

백엔드는 Rust로 작성됐으며 AWS Lambda, DynamoDB, API Gateway로 구현됐다.[^jackpriceburns]
프론트엔드 레포는 공개됐지만 백엔드는 비공개다.
레슨 콘텐츠는 마크다운 파일로 저장돼 커뮤니티 기여가 용이하다.

## 분석

### 브라우저 우선 접근이 해결하는 진입 장벽 문제

nativeforks가 핵심을 정확히 짚었다.[^nativeforks]
역공학을 시도할 때마다 “이 오래된 컴파일러 설치”와 “이 SDK 패치” 사이 어딘가에서 막혔다고 한다.
탭을 열고 바로 실험할 수 있게 된 것이 도구 접근이 아닌 진입 장벽 제거다.

GameCube 역컴파일 프로젝트는 수년간 존재했지만
새로운 기여자가 유입되기 어려웠다.
StilesCrisis가 decomp.me 기여를 시도하다가
“순서가 약간 다른 명령어나 함수 논리적 끝 이후의 죽은 pop 문”을 고칠 방법을 몰라
포기했다고 밝힌 것이[^StilesCrisis] 이 문제를 보여준다.
Decomp Academy는 기여 전 단계인 “역컴파일 읽기”부터 가르침으로써
이 진입 장벽을 낮춘다.

### Show HN 프로젝트의 교육 설계 선택

이 프로젝트는 Show HN이라는 형식에 걸맞게 작성자가 직접 구축한 개인 프로젝트다.
256개 레슨과 4단계 커리큘럼을 혼자 설계하고
Rust 백엔드를 Lambda에서 돌리는 것까지 처리했다는 것이
댓글에서 인정받은 이유다.

Retr0id는 2단계에서 `void identity(void) { return; }` 함수로 통과했지만
“LLM 느낌의 텍스트 벽”에 막혔다고 보고했다.[^Retr0id]
이것은 레슨 품질의 불균일함을 드러낸다.
초기 레슨은 인터랙티브 검증으로 참여도를 높이지만
설명 텍스트의 완성도가 따라오지 못하는 구간이 있다.

## 비평

### 단일 아키텍처에 한정된 적용 가능성

PowerPC 어셈블리와 MWCC 컴파일러는 GameCube/Wii 역컴파일에 특화된 스택이다.
여기서 배운 것은 ARM, x86, RISC-V 같은 다른 아키텍처로 직접 전이되지 않는다.
OsrsNeedsf2P가 BFME(반지의 제왕 게임)를 점진적으로 역공학할 수 있는지 물었지만[^OsrsNeedsf2P]
그것은 완전히 다른 플랫폼이다.
Decomp Academy의 가치는 GameCube 생태계에 집중된 커뮤니티에서 가장 높고,
범용 어셈블리 학습 도구로 포지셔닝하기는 어렵다.

HiPhish의 피드백처럼[^HiPhish] 어셈블리 명령어 레퍼런스나
챕터 간 빠른 참조 기능이 없다는 실용적 부재도 있다.
레슨 진행 중에 이전 명령어를 확인하려면 탭을 벗어나야 한다.

### 백엔드 비공개와 교육 플랫폼의 장기 지속성

Decomp Academy는 무료이고 오픈소스를 지향하지만
컴파일러 실행을 담당하는 백엔드가 비공개다.
AWS Lambda 비용은 사용량에 따라 증가하고
개인 프로젝트가 HN에서 188점을 받으면 트래픽이 폭증한다.
jackpriceburns가 Lambda에 컴파일러를 올리는 것 자체가 “모험”이었다고 밝힌 것처럼
이 인프라는 장기 유지보수를 고려한 설계가 아닐 수 있다.
플랫폼이 지속되려면 커뮤니티 기여와 비용 지속 가능성 모두 해결해야 한다.

## 인사이트

### 역공학의 민주화와 게임 보존의 가속

saturn8601이 AI를 사용해 오래된 Windows/DOS 애플리케이션을 Mac 네이티브 버전으로 변환한 경험을 공유하며
“어떤 코드도 시간의 모래 속에서 사라지지 않을 것”이라는 전망을 언급했다.[^saturn8601]
Decomp Academy는 이 방향에서 중요한 위치를 차지한다.
더 많은 사람이 역컴파일 기술을 배우면 더 많은 게임이 보존되고,
보존된 코드는 다시 AI 학습 데이터가 되어 역공학 자체를 가속시키는 피드백 루프가 형성된다.

sciencejerk의 질문이 보여주듯[^sciencejerk] 이 분야는 여전히 외부에 잘 알려지지 않았다.
바이너리가 어떻게 구해지는지, 역컴파일과 어셈블리 문서화의 차이가 무엇인지조차 모르는 사람이 많다.
Decomp Academy의 가장 큰 기여는 어셈블리 역컴파일이 배울 수 있는 기술이라는 것을
브라우저 탭 하나로 증명한다는 점이다.

### GameCube 생태계가 실험장이 된 이유

GameCube가 역컴파일 커뮤니티의 활발한 실험장이 된 데는 여러 요인이 있다.
하드웨어가 충분히 단순해서 전체 아키텍처를 이해할 수 있고,
충분히 복잡해서 의미 있는 도전이 된다.
PowerPC는 상대적으로 정규적인 ISA여서 패턴 학습이 가능하다.
무엇보다 Star Fox Adventures, 피크민, 메트로이드 프라임 같은 타이틀이
이 작업에 강한 동기를 부여하는 팬 커뮤니티를 형성하고 있다.
Decomp Academy는 이 특수한 조건의 교차점에서 탄생한 프로젝트다.

---

[^jackpriceburns]: <https://news.ycombinator.com/item?id=48703426>
[^nativeforks]: <https://news.ycombinator.com/item?id=48707182>
[^StilesCrisis]: <https://news.ycombinator.com/item?id=48706283>
[^Retr0id]: <https://news.ycombinator.com/item?id=48703578>
[^OsrsNeedsf2P]: <https://news.ycombinator.com/item?id=48703964>
[^HiPhish]: <https://news.ycombinator.com/item?id=48705816>
[^saturn8601]: <https://news.ycombinator.com/item?id=48703647>
[^sciencejerk]: <https://news.ycombinator.com/item?id=48704257>
