# 2026년은 Rust 컴파일러에 특별한 해다: 오래 투자한 일들이 한꺼번에 결실을 맺는다

원문: [2026 is an exciting year for the Rust compiler (and me)](https://yoyo-code.com/2026-is-exciting-year-for-rust-compiler-and-me/)

HN 토론: <https://news.ycombinator.com/item?id=50166502> (195점, 108개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/c2ouz0/2026_is_exciting_year_for_rust_compiler_me> (64점, 7개 댓글)

GN 토론: <https://news.hada.io/topic?id=35739>

## 요약

2026년 10월 19일에 올라온 글이다.
Rust 컴파일러의 성능 분류(perf triage)에 참여해 온 글쓴이가, 올해 Rust 컴파일러에서 일어나는 일을 개인적으로 흥미로운 것만 골라 소개한다.
글쓴이는 올해 작업량이 특별히 많은 것이 아니라, 여러 장기 투자가 동시에 마무리 단계에 들어서서 결실이 한꺼번에 보이는 해라고 정리한다.

가장 큰 것으로 두 가지를 꼽는다.
하나는 차세대 trait 솔버다.
타입 시스템의 큰 부분을 다시 구현하는 일로, 여러 형태로 거의 10년 동안 진행됐다.
건전성(soundness) 버그를 고치고, 오래된 문제의 해결을 막던 기술 부채를 해소하며, async Rust와 `impl Trait`의 한계에 대한 해법을 연다고 한다.
다른 하나는 새 빌림 검사기 Polonius다.
더 많은 코드가 컴파일되게 하고 관련 기능을 열어 준다.
글쓴이는 언젠가 내부 참조를 가능하게 할 수도 있다고 하지만, 컴파일러 전체에 미치는 영향은 새 솔버보다 작다고 본다.

글쓴이의 주된 관심사인 컴파일러 성능에서는 한꺼번에 많은 일이 일어난다.
병렬 프런트엔드는 안정화(stabilization)가 가까워졌다.
LLVM 23은 rustc 성능에 분명하고 예상 밖으로 큰 긍정적 변화를 가져왔다.
미세 최적화가 계속 들어오고 있고, 병합을 관리하는 사람들이 성능 영향을 직접 분류하게 되어 회귀에 대한 대응이 빨라졌다.
Amanieu가 제안한 MIR 최적화 패스인 move elimination은 LLVM이 최적화하기 어려운 복사를 제거해 컴파일 시간과 실행 시간을 모두 줄인다.
polymorphization(다형화)은 이번이 세 번째 실험으로, Swift에서 영감을 받아 제네릭 인자의 레이아웃을 인자로 넘기는 방식이다.
`cargo check`와 `cargo build`가 산출물을 공유하는 프로젝트 목표, `no-embed-metadata` 기본 활성화(target 디렉터리 크기를 작업에 따라 5~30% 줄임), 새 `cargo build-dir` 배치, `no-link`와 `link-only` 지원 수정도 있다.

아키텍처 쪽에서는 컴파일러 속성(attribute) 표현을 통합하는 작업의 마지막 속성이 며칠 전에 옮겨졌다.
rustc의 쿼리 시스템 구현이 정리됐고, const generics를 진전시키는 작업이 있다.
조직 쪽으로는 “프로젝트 목표(project goals)”라는 운영 틀이 안정된 상태에 이르렀고, Fast Builds 로드맵과 “Maintainers in Residence” 프로그램, 새 펀딩 팀이 생겼다.
글의 마지막은 글쓴이 자신의 이야기다.
웹 기반 일에 지쳐 더 기술적인 일로 돌아가고 싶던 차에 Rust All Hands에 초대받았고, 그 경험으로 Rust 프로젝트에서 일하기로 정했다고 한다.
다만 프로젝트에서 일자리를 얻는 길은 분명하지 않아서, target 디렉터리 크기를 줄이는 프로젝트 목표를 펀딩이 있을 때 맡기로 했고 GitHub Sponsors를 열었다.

## 분석

### 글의 중심 주장: 큰 일은 큰 폭발이 아니라 건강한 체계에 대한 지속 투자의 결과다

글은 마지막까지 같은 논지를 반복한다.
눈에 띄는 변화는 하나의 큰 프로젝트에서 나오지 않고, 내부 문제의 긴 목록을 하나씩 해결하다가 갑자기 큰 것이 열리는 방식으로 나온다는 것이다.
`no-link`와 `link-only` 항목이 이 문장을 그대로 쓴다.
병렬 프런트엔드도 설계에 만족하는 사람이 거의 없는데 대안이 없어서, 까다롭고 성가신 문제를 하나씩 해결해 남은 게 없을 때까지 밀어붙인 결과로 안정화에 다가갔다고 한다.

이 틀에서 올해가 특별한 이유는 새 아이디어가 아니라 시점의 일치다.
글쓴이는 올해가 일의 양이 특별해서가 아니라, 여러 장기 투자가 동시에 성과를 내기 시작하는 해여서 특별하다고 분명히 한다.
이것은 검증이 어려운 주장이다.
이전 해와 비교한 작업량 통계는 글에 없다.

### 성능이 좋아진 이유는 도구보다 사람과 절차에 있다

글쓴이가 설명하는 성능 개선의 원인은 하나의 기술이 아니다.
새 기여자, 성능 작업을 더 많이 하게 된 기존 기여자, 도구 개선, 아키텍처 정리가 겹쳤다고 한다.
특히 눈에 띄는 대목은 병합을 관리하는 사람들이 성능 영향을 직접 분류하게 된 점이다.
응답 시간이 짧아지고, 성능 영향이 롤업(rollup)으로 PR을 묶는 방식까지 바꾼다는 것이다.
글쓴이는 이를 콘웨이의 법칙이 여전히 법칙이라는 말로 정리한다.

LLVM의 변화도 같은 구조다.
LLVM 10 업그레이드가 10%의 성능 후퇴를 가져왔고, LLVM의 현재 책임 개발자가 이를 블로그 글로 지적한 뒤 성능을 시간에 따라 추적하는 체계가 생겼다.
그 이후 업그레이드의 성과는 덜 나쁨, 엇갈림, 대체로 긍정적으로 바뀌었고, LLVM 23은 거의 전적으로 긍정적이었다고 한다.
성능이 좋아진 원인을 글쓴이는 LLVM에서 기능 작업과 함께 최적화 작업이 늘었기 때문으로 이해한다고 밝히며, LLVM 개발은 자세히 따라가지 않는다고 단서를 단다.

### polymorphization은 두 가지 서로 다른 일을 가리킨다

글에서 가장 정확한 구분 중 하나다.
원래의 polymorphization은 중복되거나 불필요한 monomorphization을 피하는 것이어서 순수하게 컴파일 시간 최적화이고 실행 시간에는 영향이 없다.
Swift 방식은 모든 것을 다형화하고 제네릭 인자의 레이아웃을 인자로 넘기므로 실행 시간 비용이 생기며, 컴파일러 플래그로 조절하게 된다.
글쓴이가 아는 한 차세대 solver가 원래의 방식을 가능하게 한다.
두 방식이 같은 문제에 부딪히므로 작업이 양쪽에 쓸모가 있고, 한 노력에서 둘 다 나올 수도 있다고 한다.

## 비평

### 글은 성과 목록이지 검증이 아니다

글쓴이는 스스로 개인적으로 흥미로운 것을 고른 불완전한 개요라고 밝힌다.
그래서 이 글을 올해 Rust 컴파일러의 객관적 결산으로 읽을 수는 없다.
각 항목의 상태도 구분된다.
이미 발표된 것(`no-embed-metadata`, 새 build-dir 배치), 안정화가 가까운 것(병렬 프런트엔드), 실험인 것(polymorphization), 진행 중인 프로젝트 목표(`cargo check`와 `cargo build`의 캐시 공유)가 한 목록에 섞여 있다.
독자가 실제로 쓰게 될 시점은 글에서 알 수 없고, 수치가 있는 것은 target 디렉터리 크기 5~30%뿐이다.
성능 개선에 대한 서술도 대부분 질적이다.

### 가장 큰 변화의 출시 시점은 글 밖에서 나왔다

글은 새 solver가 언제 안정화되는지 말하지 않는다.
Lobste.rs에서 jana는 차세대 solver가 1.101에 들어갈 가능성이 높다고 했고,[^jana]
davidcornu는 1.100에 never type과 Allocator가 들어간다고 알렸다.[^davidcornu]
goldstein은 1.100이라는 숫자가 우연이 아니라 두 기능 모두 그 시기에 안정화되면 좋겠다는 이야기가 있었다고 설명했다.[^goldstein]
이 정보는 댓글의 전언이며, 글이 아니라 이 문서가 확인한 것도 아니다.
따라서 독자가 새 solver가 언제 쓸 수 있는지 알려면 글이 아닌 출처를 확인해야 한다.

### 조직의 어두운 면은 한 문단에 모인다

글은 이번 해가 모두 긍정적인 것은 아니라고 인정한다.
연초에 사람들이 펀딩을 잃은 일과 AI 정책을 둘러싼 격한 논쟁이 있었고, All Hands 며칠 전에 정책 초안이 소셜 미디어에 올라와 중재 팀이 스트레스 속에서 피해를 줄이려 애썼다는 것이다.
그러나 이는 결론의 한 문단이고, 어떤 정책이었는지, 어떤 결과가 있었는지는 글에 없다.
HN에서 hmokiguess가 최근 한 Ruby 젬 관리자의 깊은 실망과 이 글의 기쁨을 대비했을 때, anonymous908213은 리더십의 차이를 이유로 들었다.[^anonymous908213]
그 댓글은 Rust 프로젝트의 AI 정책에 대한 정보를 주지 않으며, 글의 서술을 보강하는 근거도 아니다.

## 인사이트

### 소비자에게 가장 먼저 체감되는 것은 디스크 크기일 수 있다

글에서 비중이 작은 target 디렉터리 크기가 HN 스레드에서는 가장 큰 호응을 얻었다.
thomashabets2는 컴파일 옵션별로 target 안에 하위 디렉터리를 만드는 자신의 프로젝트가 190GB라고 적었다.[^thomashabets2]
stymaar는 Rust가 컴파일이 느리다는 밈이 있지만 실제로 써 본 사람에게는 컴파일러 속도보다 target 디렉터리가 더 성가신 문제라고 했다.[^stymaar]
Lobste.rs에서 valpackett는 요즘 SSD 가격 때문에 기초 작업과 성능보다 target 디렉터리를 줄이는 일이 더 기대된다고 했다.[^valpackett]

이유는 estebank가 설명했다.
Rust 도구 체인이 크레이트마다 디버그 정보를 많이 만들고, 언어가 monomorphization에 크게 의존해 이름만 다른 중복 코드가 생기며, 큰 의존성 트리와 feature 때문에 같은 크레이트가 작업 공간마다 다른 것으로 취급돼 재사용되지 않기 때문이라고 했다.[^estebank]
이 설명대로라면 target 크기는 한 가지 원인이 아니라 디버그 정보, 단형화, 작업 공간 사이의 캐시 부재가 곱해진 결과다.
글이 소개한 `no-embed-metadata`, 새 build-dir 배치, `cargo check`와 `cargo build`의 캐시 공유가 각각 그 곱셈의 한 항을 겨냥한다.

### 컴파일러의 기술 부채 상환은 언어의 여지를 늘린다

HN에서 throwup238은 새 solver를 수년째 기다려 왔다고 하며, solver와 Polonius가 몇 년째 정체된 specialization을 풀어 주기를 바란다고 했다.[^throwup238]
panstromek는 specialization에도 움직임이 있고, solver에 직접 막혀 있는 것은 아니지만 타입 시스템이 나아지면 건전성 문제를 따지기가 수월해진다고 답했다.[^panstromek]
simplesocieties가 async에서 새 solver가 고칠 문제를 묻자, yoshuaw는 async 함수가 돌려주는 future에 경계를 거는 Return Type Notation(RTN)이 막혀 있다고 했고, 이것이 trait 안의 async 함수를 실용적으로 만드는 두 남은 기능 중 하나이며 다른 하나인 dyn 지원은 solver와 무관하다고 했다.[^yoshuaw]
이런 서술은 솔버가 단일 기능이 아니라 기능 대기열의 병목이라는 글의 주장을 구체적으로 뒷받침한다.

### 이 글을 읽는 방법

Rust로 일하는 사람이라면 글에서 얻을 수 있는 실무적 판단은 넓지 않다.
당장 할 수 있는 것은 새 안정화 릴리스 노트를 보며 위 항목들이 들어왔는지 확인하는 것이다.
이 글의 서술을 가를 관찰은 두 가지다.
새 solver와 병렬 프런트엔드가 안정 채널에 들어온 뒤 실제 컴파일 시간과 target 크기가 줄어드는지가 하나다.
글쓴이가 맡기로 한 target 디렉터리 프로젝트 목표가 펀딩을 받아 진행되는지가 다른 하나다.
둘 다 이뤄지면 글의 올해 특별한 해라는 평가는 사후에 확인된 것이 되고, 지연되면 그것은 장기 투자의 결실이 한꺼번에 온다는 구조가 예상만큼 동시에 오지 않았다는 뜻이다.

---

[^jana]: <https://lobste.rs/s/c2ouz0/2026_is_exciting_year_for_rust_compiler_me#c_7sgyof>

[^davidcornu]: <https://lobste.rs/s/c2ouz0/2026_is_exciting_year_for_rust_compiler_me#c_m5c4oo>

[^goldstein]: <https://lobste.rs/s/c2ouz0/2026_is_exciting_year_for_rust_compiler_me#c_pzbode>

[^anonymous908213]: <https://news.ycombinator.com/item?id=50170331>

[^thomashabets2]: <https://news.ycombinator.com/item?id=50167575>

[^stymaar]: <https://news.ycombinator.com/item?id=50169328>

[^valpackett]: <https://lobste.rs/s/c2ouz0/2026_is_exciting_year_for_rust_compiler_me#c_1vi6u2>

[^estebank]: <https://news.ycombinator.com/item?id=50170472>

[^throwup238]: <https://news.ycombinator.com/item?id=50168852>

[^panstromek]: <https://news.ycombinator.com/item?id=50170093>

[^yoshuaw]: <https://news.ycombinator.com/item?id=50175087>
