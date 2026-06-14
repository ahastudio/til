# TrueType 힌팅 인터프리터를 Swift로 이전하기 — 성능을 높이며 안전해진 C 코드

원문: <https://www.swift.org/blog/migrating-truetype-hinting-to-swift/>

HN 토론: <https://news.ycombinator.com/item?id=48508726> (237점, 125개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/o8i26c/swift_at_apple_migrating_truetype>

## 요약

Apple Security 팀이 2025년 가을 릴리스를 대상으로 TrueType 힌팅(hinting) 인터프리터를 C에서 Swift로 다시 작성했다.
목표는 메모리 안전성 확보와 성능 개선이었으며, 결과적으로 C 구현 대비 13% 성능 향상을 달성했다.

TrueType 힌팅 인터프리터는 인터넷에서 내려받은 신뢰할 수 없는 폰트 데이터를 처리한다.
Scott Perry는 이 코드를 다음과 같이 설명했다.
“이 인터프리터는 입력에 의한 제어 흐름, 복잡한 자료구조, 그리고 세심한 메모리 관리를 필요로 한다.
바로 완벽하게 만들기 어렵고, 메모리 오류가 악용되기 쉬운 종류의 코드다.”

배포 이후 보안 버그는 한 건도 보고되지 않았다.
소스 코드는 GitHub(<https://github.com/apple/truetype-hinting-interpreter-example>)에 공개되어 있다.

## 분석

### 왜 폰트 파싱에서 메모리 안전성이 중요한가

폰트 파일은 인터넷에서 자동으로 다운로드되어 렌더링 파이프라인에 즉시 투입된다.
사용자가 방문한 웹페이지에 임베드된 폰트, 문서에 포함된 폰트 모두 신뢰할 수 없는 데이터 소스다.
TrueType 힌팅 인터프리터는 폰트 파일 안에 담긴 바이트코드를 실행하는 가상 머신에 가깝다.
입력이 바이트코드이므로 조작된 폰트는 버퍼 오버플로우, 범위 밖 읽기/쓰기 같은 메모리 오류를 유발할 수 있다.
C 코드에서 이런 오류는 악의적인 공격자가 임의 코드를 실행하는 수단이 된다.
Swift는 경계 검사와 소유권 모델을 언어 수준에서 강제하므로, 이 공격 표면을 구조적으로 제거한다.

### `~Copyable`이 가능하게 하는 것

Swift 5.9에 도입된 `~Copyable`(noncopyable) 타입은 값이 복사되는 것을 컴파일 타임에 금지한다.
C의 참조 타입이나 포인터 없이도 “이 값의 사본은 존재하지 않는다”를 타입 시스템으로 보장한다.
인터프리터처럼 상태가 크고 복사 비용이 높은 자료구조에서는 두 가지 이점이 있다.
첫째, ARC(Automatic Reference Counting) 오버헤드가 줄어든다.
클래스 기반 참조 타입은 retain/release 호출을 발생시키지만, noncopyable 값 타입은 그 비용이 없다.
둘째, 배타성 검사(exclusivity checking) 비용도 최소화된다.
Swift는 값 타입에 대한 동시 접근을 컴파일 타임과 런타임에 검사하는데, noncopyable 타입은 이 검사를 더 효율적으로 만든다.
Swift 6.2에 도입된 `Span` 타입은 슬라이스에 대한 안전하고 효율적인 순차 연산을 제공하며, 인터프리터의 시퀀스 처리 경로를 단순화했다.

### Projection 타입으로 20% 런타임 감소가 가능한 이유

기존 접근은 C 자료구조에서 글리프(glyph) 데이터를 Swift 값 타입으로 복사해 다루는 것이었다.
복사는 메모리 할당과 초기화 비용을 수반하며, 글리프 하나당 수백 바이트에 달하는 데이터를 처리할 때 누적 비용이 크다.
Projection 타입은 복사 없이 원본 C 자료구조에 대한 안전한 뷰(view)를 제공한다.
Swift의 소유권 모델 덕분에 projection이 유효한 동안 원본 구조가 변경되지 않음을 컴파일러가 보장한다.
그 결과 할당과 복사를 생략하면서도 안전성을 유지할 수 있고, 인터프리터 런타임을 약 20% 줄였다.

### 이 이전이 보여주는 Swift의 시스템 언어로서의 성숙도

이 프로젝트가 흥미로운 이유는 Swift가 앱 레이어를 넘어 보안에 민감한 저수준 인프라 코드에 쓰였다는 점이다.
`~Copyable`, `Span`, projection 타입 같은 도구들은 C와 동등한 성능을 내면서 안전성을 추가하려는 설계 방향을 보여준다.
C++ 대체 언어로서 Rust가 주로 언급되는 분야에서, Apple은 Swift로 동일한 목표를 추구하고 있다.
99.7% 코드 커버리지의 유닛 테스트, 2,500만 개 글리프를 포함하는 퍼저 코퍼스, 프로덕션 코드 대비 4배에 달하는 테스트 코드는
단순한 이식이 아니라 검증 가능한 정확성을 전제로 한 재작성임을 보여준다.

HN에서 pjmlp[^pjmlp]는 이 TrueType 이전이 고립된 사례가 아님을 지적했다.
Apple 플랫폼 키노트에서 macOS 전반에 걸쳐 Swift 채택 사례가 다수 공개되었으며,
커널 수준을 포함한 OS 전 계층에서 메모리 안전 언어로의 전환이 진행 중임을 시사한다.

### Rust vs Swift: 시스템 언어 경쟁의 맥락

airstrike[^airstrike]는 "Swift를 즐겼지만, Apple이 Rust를 기본 언어로 선택했다면 세상이 어떻게 달라졌을지 궁금하다"고 썼다.
이 질문에 대해 AceJohnny2[^AceJohnny2]는 중요한 차이를 짚었다.
Rust는 안정적인 ABI가 없어 동적 라이브러리에서 유용한 Rust 시맨틱을 노출할 수 없는 반면,
Swift는 응용 프로그래밍 언어로 쓰이려면 ABI가 필수였기에 이를 설계 초기부터 포함했다는 것이다.
한편 Microsoft도 유사한 맥락에서 DirectWriteCore를 Rust로 재작성했다.
weinzierl[^weinzierl]이 언급하고 DASD[^DASD]가 확인한 바에 따르면,
엔지니어 2명이 6개월에 걸쳐 15만 4천 줄의 코드를 작성해 폰트 셰이핑 성능을 5~15% 향상시켰다.
Apple의 Swift 이전과 Microsoft의 Rust 이전은 거의 동시에 진행된 병렬 실험이라 할 수 있다.

Lobste.rs에서 kevinc[^kevinc-lobsters]는 이 구도를 더 단순하게 정리했다.
"Swift를 좋아하지만, Rust는 개발자와 친해졌다. Apple은 그러는 데 서툴다."
기술적 우열보다 생태계 형성 능력의 차이가 플랫폼 밖에서 Swift의 입지를 제한한다는 지적이다.
또한 snej[^snej-lobsters]는 비-Apple 플랫폼에서 Foundation이 OS에 내장되지 않아 바이너리 크기가 크게 늘어나는 문제를 언급했다.
Foundation이 ICU와 libcurl을 함께 포함하기 때문에 50MB 이상의 오버헤드가 발생할 수 있으며,
모바일 앱 크기에 민감한 Android 배포에서 특히 문제가 된다는 것이다.

## 비평

이 글은 결과 중심으로 잘 쓰여 있지만, 몇 가지 맥락이 빠져 있다.
13%라는 성능 수치가 어떤 조건에서 측정되었는지(CPU, OS 버전, 폰트 집합) 공개되지 않아 재현 가능성을 판단하기 어렵다.
또한 기존 C 코드가 얼마나 최적화된 상태였는지 모르므로, 개선의 기준선이 불명확하다.

AndriyKunitsyn[^AndriyKunitsyn]은 더 근본적인 질문을 던졌다.
2023년 이후 macOS는 1080p 디스플레이에서 UI를 힌팅 없이 렌더링하며, 결과적으로 비-Retina 해상도에서 텍스트가 뭉개진다는 것이다.
Windows와 Linux가 동일 해상도에서 힌팅을 적용해 선명한 텍스트를 보여주는 것과 대조적이다.
만약 이 관찰이 정확하다면, Apple이 힌팅 인터프리터를 정교하게 재작성한 실질적 수혜자는 PDF 렌더링에 국한될 수 있다.

C→Swift 변환에 LLM 코딩 어시스턴트용 교육 자료를 만들었다는 언급은 흥미롭지만 구체적이지 않다.
LLM이 이 마이그레이션에서 어떤 역할을 했는지, 어시스턴트 없이 수행한 부분과 어시스턴트를 활용한 부분이 어디서 갈렸는지 알 수 없다.
LoganDark[^LoganDark]는 공개된 GitHub 코드에서 LLM이 생성한 것으로 보이는 패턴을 발견했다고 지적하며,
보안에 민감한 저수준 코드에서 AI 생성 코드의 비중이 어느 정도인지 우려를 표했다.

comex[^comex]는 이 글이 소개하는 라이프타임 기능(lifetime features)에 대해 직접적인 반례를 제시했다.
몇 달 전 같은 기능을 사용해 보려 했을 때 매우 단순한 프로그램에서도 컴파일러 크래시가 반복 발생해 결국 포기했다는 것이다.
이에 대해 stephencanon[^stephencanon]은 이 글에서 다루는 작업이 이미 2025년 가을 OS에 탑재된 것이므로
가장 최근의 컴파일러 변경에 의존하지 않는다고 해명했다.
두 의견을 종합하면, 해당 기능들은 프로덕션에서는 안정적으로 쓰이고 있으나
일반 개발자가 최신 도구 체인에서 사용할 때는 아직 불안정한 경계가 존재할 수 있다.

Lobste.rs에서 olliej[^olliej-lobsters]는 이 글이 암묵적으로 드러내는 점에 주목했다.
Swift는 레퍼런스 카운팅(refcounting)을 기본 객체 수명 관리 방식으로 사용해 사실상 모든 객체가 `Arc`처럼 동작하며,
컴파일러가 필요하다고 판단하면 암묵적 힙 할당을 수행할 수 있다.
또한 불변 핵심 타입은 CoW(Copy-on-Write) 의미론으로 구현되는데, 값의 비탈출 여부를 컴파일러가 증명하지 못하면 원자적 단일 소유자 검사가 발생한다.
다중 스레드 경합 환경에서 이 비용은 상당할 수 있다.
ABI 안정성이라는 설계 목표 역시 비용을 수반한다.
제네릭 인터페이스가 기본적으로 안정적인 ABI를 갖추다 보니, 실제로는 Rust의 `dyn trait`에 가까운 코드가 생성된다.
ABI 제약이 없는 내부 라이브러리에서도 컴파일러가 불필요하게 보수적인 코드를 생성하는 경우가 있어 수작업 최적화가 필요하다.
olliej는 이 글이 성능 목표를 맞추기 위해 기본 Swift 스타일에서 벗어난 코드를 써야 했던 사례들을 보여준다고 지적했다.
13% 성능 향상은 언어가 자동으로 제공한 것이 아니라, 기본값을 우회하는 노력의 산물이기도 하다는 해석이다.

배포 후 보안 버그가 없다는 것은 고무적이지만, 배포 기간이 짧을 수 있고 버그가 단순히 아직 발견되지 않았을 가능성도 있다.
장기적 트랙 레코드가 쌓인 뒤에야 이 주장의 무게가 정해질 것이다.

## 인사이트

메모리 안전성과 성능이 반드시 상충하지 않는다는 것을 이 프로젝트가 실증했다.
언어와 런타임이 충분히 성숙하면, 안전성을 추가하면서 동시에 성능을 개선하는 경로가 열린다.

C 코드를 Swift로 이전할 때 가장 어려운 부분은 문법 변환이 아니라 정확성 보장이다.
4배에 달하는 테스트 코드와 대규모 퍼저 코퍼스는 이 프로젝트의 핵심 투자가 검증 인프라에 있었음을 말해준다.
“코드 이전”을 계획할 때는 테스트 전략을 먼저 설계해야 한다.

noncopyable 타입과 projection 타입은 Swift를 저수준 코드에 적용하는 핵심 도구로 부상하고 있다.
기존 Swift 코드에서도 복사 비용이 높은 자료구조가 있다면 `~Copyable`을 검토할 만하다.

---

[^pjmlp]: <https://news.ycombinator.com/item?id=48509276>
[^airstrike]: <https://news.ycombinator.com/item?id=48509652>
[^AceJohnny2]: <https://news.ycombinator.com/item?id=48510285>
[^weinzierl]: <https://news.ycombinator.com/item?id=48509508>
[^DASD]: <https://news.ycombinator.com/item?id=48509791>
[^AndriyKunitsyn]: <https://news.ycombinator.com/item?id=48510300>
[^LoganDark]: <https://news.ycombinator.com/item?id=48509564>
[^comex]: <https://news.ycombinator.com/item?id=48511793>
[^stephencanon]: <https://news.ycombinator.com/item?id=48511811>
[^kevinc-lobsters]: <https://lobste.rs/s/o8i26c/swift_at_apple_migrating_truetype#4csdpg>
[^snej-lobsters]: <https://lobste.rs/s/o8i26c/swift_at_apple_migrating_truetype#ipezpp>
[^olliej-lobsters]: <https://lobste.rs/s/o8i26c/swift_at_apple_migrating_truetype#teccgv>
