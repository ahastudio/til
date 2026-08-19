# Radicle: 중앙 주체 없이 Git 위에 세운 주권적 코드 포지

<https://radicle.dev/>

HN 토론: <https://news.ycombinator.com/item?id=48147603> (274점, 93개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/6tbq79/radicle_peer_peer_stack_for_code>

## 소개

Radicle은 자신을 “sovereign {code forge} built on Git”이라고 소개한다.
Git 위에 올린 오픈소스 P2P 코드 협업 스택이며, 네트워크를 통제하는 단일 주체가 없다는 것이
중앙집중식 호스팅 플랫폼과 갈라지는 지점이다.
저장소는 피어들 사이에 복제되고, 사용자는 자신의 데이터와 워크플로를 온전히 쥔다.

프로토콜은 코드와 사회적 산출물 모두에 암호학적 신원을 부여한다.
피어 사이의 데이터 전송에는 Git을 그대로 쓰고, 저장소 메타데이터 교환에는 자체 가십 프로토콜을
사용한다.
이슈, 논의, 코드 리뷰 같은 것들은 Collaborative Objects(COBs)라는 Git 오브젝트로 구현되며,
Radicle은 이것을 자신의 “사회적 원시 자료형(social primitive)”이라고 부른다.
모든 사회적 산출물은 Git에 저장되고 공개키 암호로 서명되므로, 진위와 저작자 확인이 프로토콜
차원에서 이루어진다.

Radicle은 local-first를 표방한다.
인터넷 연결이 없어도 기능이 계속 동작하고, 사용자가 데이터를 소유하므로 이전과 백업, 온·오프라인
접근이 모두 쉽다는 주장이다.
사용자가 직접 노드를 운영할 수 있다는 점을 검열 저항성의 근거로 든다.

## 아키텍처

스택은 CLI, 웹 인터페이스, TUI가 앞단에 있고 Radicle Node와 HTTP 데몬이 뒤를 받치는 형태다.
어느 부분이든 교체할 수 있고 다른 클라이언트를 새로 만들 수도 있다는 것이 모듈 설계의 취지다.

```text
┌─────────────────┐┌────────────────┐
│  Radicle CLI    ││ Radicle Web    │
└─────────────────┘└────────────────┘
┌───────────────────────────────────┐
│  Radicle Repository               │
│ ┌────────┐ ┌────────┐ ┌─────────┐ │
│ │  code  │ │ issues │ │ patches │ │
│ └────────┘ └────────┘ └─────────┘ │
├───────────────────────────────────┤
│  Radicle Storage (Git)            │
└───────────────────────────────────┘
┌────────────────┐┌─────────────────┐
│  Radicle Node  ││  Radicle HTTPD  │
├────────────────┤├─────────────────┤
│    NoiseXK     ││   HTTP + JSON   │
└────────────────┘└─────────────────┘
```

노드 간 전송은 NoiseXK 핸드셰이크를 쓰고, HTTPD는 HTTP + JSON을 노출한다.
저장 계층이 Git 그 자체라는 점이 핵심이다 — 코드도, 이슈도, 패치도 전부 Git 오브젝트로 저장된다.
Radicle에서 PR/MR에 해당하는 개념은 “Patch”다.

## 설치와 릴리스 현황

설치는 한 줄이다.

```bash
curl -sSLf https://radicle.dev/install | sh
```

Linux, macOS, BSD 계열과 Windows를 지원한다.
그래픽 클라이언트로 Radicle Desktop이 따로 있다.
라이선스는 MIT와 Apache 2.0 이중 라이선스다.

릴리스 흐름은 꾸준하다.

| 날짜       | 내용                                       |
| ---------- | ------------------------------------------ |
| 2026-08-12 | Radicle 1.10.1                             |
| 2026-08-05 | Radicle 1.10.0                             |
| 2026-05-22 | Radicle 1.9.1                              |
| 2026-05-19 | Radicle 1.9.0                              |
| 2026-04-23 | radicle.{dev,network}로 도메인 이전        |
| 2026-03-30 | Radicle 1.8.0                              |
| 2026-03-30 | 서명된 레퍼런스의 취약점 공개              |
| 2026-03-20 | Radicle 1.7.1                              |
| 2026-03-18 | Radicle 1.7.0                              |
| 2026-01-14 | Radicle 1.6.0                              |

2026년 4월 `radicle.xyz`에서 `radicle.dev`로 도메인을 옮겼다.
HN에서 그 이유를 두고 `.xyz` 같은 TLD가 스팸 비율이 높아 ISP 차단 대상이 되곤 한다는 추정이
나왔다[^satvikpendem].
소스 코드는 자기 네트워크 위에 있고, 웹으로는 `radicle.network`의 시드 노드를 통해 열람한다.

## 분석

### 저장 포맷을 Git으로 고정한 것이 이 설계의 전부다

탈중앙 포지를 만들 때 가장 큰 선택은 “이슈와 리뷰를 어디에 둘 것인가”다.
GitHub의 락인이 코드가 아니라 코드 주변의 사회적 데이터에 있다는 것은 이미 널리 합의된 진단이고,
`git clone`으로 가져올 수 없는 것들 — 이슈, 리뷰 코멘트, CI 설정, 권한 모델 — 이 정확히 이동
비용을 만든다.

Radicle의 답은 그것들을 전부 Git 오브젝트로 만드는 것이다.
COBs는 별도 데이터베이스도, 별도 동기화 프로토콜도 요구하지 않는다.
Git이 이미 잘하는 것 — 콘텐츠 주소 지정, 머클 구조, 효율적 델타 전송 — 을 사회적 데이터에도
그대로 적용한다.
그래서 “저장소를 복제한다”는 말이 코드뿐 아니라 협업 이력 전체의 복제를 뜻하게 된다.

이 선택의 대가는 Git에 묶인다는 것이다.
Zopieux는 홈페이지 하단의 jujutsu 관련 글을 보고 Radicle이 jj 저장소를 탈중앙화하는 네이티브
프로토콜을 준비하는 줄 알았는데 아니었다며 아쉬워했다[^Zopieux].
메인테이너 vinnyhaps는 현재로서는 Git 위에 쌓는 데 집중하고 있고 그것이 프로토콜 설계에 깊이
들어가 있다고 답했다[^vinnyhaps].
당분간은 jj의 Git 호환성에 기대겠다는 것인데, 저장 포맷을 프로토콜의 기반으로 삼은 설계에서
이는 피할 수 없는 결과다.

### 신원을 암호학으로 옮기면 계정이라는 개념이 사라진다

중앙 포지에서 “누가 이 커밋을 올렸는가”는 플랫폼 계정이 보증한다.
GitHub이 계정을 정지하면 그 사람의 기여 이력은 사실상 무효가 되고, 플랫폼이 사라지면 보증 자체가
사라진다.

Radicle은 이 보증을 키로 옮긴다.
모든 사회적 산출물이 공개키로 서명되므로, 진위 판정에 서버가 필요 없다.
h1watt는 여기서 에이전트 시대의 함의를 읽었다 — 순수하게 에이전트를 위한 포지가 나온다면 그것은
분산형일 가능성이 높고, 암호학적 신원과 서명된 아티팩트가 기본값일 것이라고 봤다[^h1watt].
theptip도 같은 방향에서, GitHub에서 PAT와 저장소 권한을 다루는 일이 지겨울 정도로 번거롭다며
에이전트 모델에는 이쪽이 더 맞는다고 했다[^theptip].

계정 대신 키를 쓴다는 것은 권한 모델이 플랫폼 정책이 아니라 프로토콜 규칙이 된다는 뜻이다.
비공개 저장소는 identity document에 그 사실이 기록되고, 공개로 바꾸려면 문서를 갱신해야 하며,
delegate(Radicle 용어로 저장소 메인테이너)가 여럿이면 그들의 승인이 필요하다는 것이 기여자
2color의 설명이다[^2color-private].
설정 화면의 토글이 아니라 서명된 문서의 변경으로 공개 여부가 결정되는 구조다.

### 검열 저항성보다 존속성이 실제 동기다

Radicle의 홈페이지는 검열 저항(censorship-resistant)을 앞세우지만, HN에서 “이게 무슨 문제를
푸는 거냐”는 솔직한 질문[^incompleteCode]에 돌아온 답은 결이 조금 달랐다.

gsaslis는 오픈소스를 공공재로 규정하는 데서 출발했다.
공공재라면 사유 플랫폼에 속해서는 안 되고, 어떤 조직도 게이트키퍼 자리에 있어서는 안 되며,
누구나 접근 가능한 공개 P2P 네트워크에 있어야 한다는 논리다[^gsaslis-public].

toyg는 더 실용적인 쪽을 짚었다.
검열보다 심각한 GitHub의 문제는 장기 존속성과 신뢰성이라는 것이다 — 내일 서비스를 접어도 대부분의
사용자는 원시 코드만 남고 나머지를 전부 잃는다[^toyg].
이 지적은 앞 절의 COBs 설계와 정확히 맞물린다.
검열은 드물게 일어나지만 플랫폼의 정책 변경과 폐업은 흔하고, 후자에 대한 방어책이 곧 전자에 대한
방어책이기도 하다.

## 비평

### 삭제할 수 없다는 문제를 프로젝트가 정면으로 다루지 않는다

figbert는 2020년에 Radicle을 발견했다가 저장소를 제대로 삭제할 수 없다는 이유로 떠났다고 했다.
당시에는 그에 관한 FAQ 항목이 있었는데 지금은 사라졌고, 대신 공개/비공개 저장소 영역이 훨씬
두터워졌다고 짚었다 — 비공개로 전환하면 새 업데이트가 더 퍼지지 않을 뿐 히스토리는 그대로
남는다[^figbert].
문서에서 문제가 사라진 것이지 문제가 해결된 것은 아니다.

방어 논리는 두 갈래로 나왔다.
nine_k는 한번 공개된 것을 되돌리기 어려운 것은 P2P에서 특히 심할 뿐 GitHub도, 웹 전체도
마찬가지라며, 되돌릴 수 있어야 한다면 애초에 공개하지 말라고 정리했다[^nine_k].
lukeck도 중앙 시스템에서 데이터를 지운다는 것이 실제로는 무엇을 보장하는지 되물었다[^lukeck].
zfourhrms는 분산 시스템에서 삭제와 롤백에 대한 기대치가 중앙 플랫폼과 다르다는 점을 일반화해
지적했다[^zfourhrms].

이 반박들은 기술적으로 맞지만 논점을 옮긴다.
GitHub에서 저장소를 지우면 최소한 정본이 사라지고 검색에서 빠지며, 법적 요청의 수신처가 명확하다.
그 정도의 실효적 삭제조차 구조적으로 불가능하다는 것은 GDPR의 삭제권이나 실수로 올린 자격 증명,
법원 명령 같은 상황에서 실무적 부담이 된다.
“우리도 GitHub만큼 못 지운다”가 아니라 “우리는 지울 수 있는 척조차 하지 않는다”가 정확한
설명인데, 홈페이지에는 그 말이 없다.

### 비공개 저장소는 암호화가 아니라 복제 정책에 기대고 있다

philsnow가 가장 날카롭다.
Radicle의 비공개 저장소는 신뢰하는 피어 집합에만 공유되고 네트워크 전체에는 보이지 않지만,
저장 시 암호화되지 않고 선택적 복제(selective replication)에 의존한다.
즉 공개 저장소와 비공개 저장소 사이에 구조적 분리가 없고, 버그 하나 또는 손가락 실수 하나면
유출이라는 것이다[^philsnow].

2color의 답변은 identity document 기반의 승인 절차를 설명했지만[^2color-private], 이는 실수로
공개 전환하는 것을 어렵게 만드는 장치이지 유출 자체를 막는 장치가 아니다.
복제 정책은 소프트웨어가 올바르게 동작할 때만 성립하는 경계이고, 암호화는 소프트웨어가 잘못
동작해도 성립하는 경계다.
그 차이가 기업 채택 여부를 가른다.

josh-sematic이 tangled.org와 비교하며 Radicle이 local-first이고 비공개 저장소 이야기가 탄탄하다고
평가한 것[^josh-sematic]도 이 맥락에서 상대적인 평가로 읽어야 한다.
경쟁 구현보다 낫다는 것과 사내 코드를 맡길 수 있다는 것은 다른 기준이다.

### 자체 호스팅이 어렵다는 것은 탈중앙 프로젝트에서 치명적이다

xvilka는 로컬 전용 배포를 더 쉽게 만들어 달라고 요청했다.
머신 세 대를 두고 공용 Radicle 네트워크에 합류하지 않은 채 그들끼리만 동작시키고 싶은데 —
온프레미스 GitLab 같지만 서버 없이 탈중앙으로 — 그러려면 상당한 스크립팅이 필요하고 문서에도
그 사용 사례가 없다고 했다[^xvilka].
기여자 endiangroup은 그에 관한 RIP가 열려 있고 곧 피드백을 낼 예정이라고 답했다[^endiangroup-rip].
survirtual은 직접 로컬 Radicle에 패치를 넣어 기본 시드를 제거하고 자기 시드를 기본값으로 바꾼 뒤
네트워크 규칙으로 LAN 외 접근을 차단해 쓰고 있다고 했다[^survirtual].

포크와 패치가 필요하다는 것은 기능이 없다는 뜻이다.
그리고 이 결함은 다른 기능 결함과 무게가 다르다.
“단일 주체의 통제 없이”를 표방하는 프로젝트에서 기본 경로가 공용 네트워크 참여이고 사설 배포가
비공식 경로라면, 결국 특정 시드 인프라에 대한 의존이 남는다.
GitHub 대신 Radicle 공용 네트워크에 의존하는 것은 의존처를 옮긴 것이지 없앤 것이 아니다.
같은 문제를 tsuraan은 스팸 쪽에서 짚었다 — 연합형 포지에서 아무 노드나 남의 공개 저장소에 이슈와
머지 요청을 열 수 있느냐는 질문이었고[^tsuraan], gsaslis의 답은 `rad follow`와 `rad block`이라는
기본 재료만 있고 정교한 것은 그 위에 만들어야 한다는 것이었다[^gsaslis-spam].

### 라이선스와 자금 구조에 대한 의심이 오래 따라다닌다

Meneth는 AGPL이 아닌 것을 아쉬워하며, 이 라이선스라면 SaaS 기업의 Embrace, Extend, Extinguish가
가능하다고 했다.
그리고 FAQ의 “Radworks intends to offer services built on top of Radicle”이라는 문장을 근거로
이미 그 방향이 계획되어 있는 것으로 읽었다[^Meneth].
기여자 endiangroup은 Radicle이 프로토콜 주도이며 인프라가 되기를 바란다고 답했다[^endiangroup-infra].

이 의심에는 뿌리가 있다.
2020년 Lobste.rs의 베타 발표 스레드에서 stchris는 Ethereum 통합이 큰 거부 요인이라고 했고, 팀의
xla가 현재 통합은 전혀 없으며 앞으로 추가되더라도 전적으로 선택적이고 협업 기능은 영향을 받지
않는다고 해명했다[^stchris][^xla].
그러나 stchris는 설명을 이해한 뒤에도 입장을 바꾸지 않았다 — 계획이 존재한다는 사실 자체가
프로젝트를 매력 없게 만든다고 했다[^stchris-reject].
mordae는 반대로 블록체인 자금이 소수 과두에게 봉사하지 않는 자유 소프트웨어 재원이 되어 준다면
그것으로 족하다고 봤고[^mordae], singpolyma는 낭비되는 것은 블록체인이 아니라 작업 증명이며
Git 저장소도 머클 체인 구조를 쓴다고 용어를 정정했다[^singpolyma].

6년이 지난 지금 홈페이지에서 암호화폐 관련 문구는 사라졌다.
그러나 자금과 거버넌스 구조에 대한 설명도 함께 사라졌고, 남은 것은 FAQ의 한 문장뿐이다.
탈중앙을 파는 프로젝트일수록 자기 조직의 중앙성을 설명할 의무가 큰데, 그 설명이 가장 얇다.

## 인사이트

### 락인은 저장 포맷이 아니라 네트워크 효과에 있고, Radicle은 전자만 풀었다

einpoklum은 아이디어가 아주 마음에 들지만 함께 시도해 볼 사람을 찾기가 어렵다고 했다 — GitHub가
워낙 널리 쓰이기 때문이다[^einpoklum].
이 한 문장이 프로젝트의 진짜 난제를 요약한다.

COBs 설계는 기술적 이동 비용을 거의 없앴다.
저장소 하나를 통째로 복제하면 이슈와 패치까지 따라온다.
그런데 이동 비용이 0이 되어도 이동할 이유가 생기지는 않는다.
포지의 가치는 저장 형식이 아니라 그 위에 있는 사람들에게서 나오고, 그것은 프로토콜 설계로 풀리는
문제가 아니다.

이 지점에서 [GitHub에는 대안이 있지만 대체재는 없다](../github/github-alternatives-no-replacement.md)의
논지가 그대로 적용된다.
Radicle은 훌륭한 대안이지만, 대체재가 되려면 사람들이 이미 거기 있어야 한다.
그리고 pessimizer가 crates.io를 Radicle로 옮기고 싶다고 한 것[^pessimizer]에 pie_flavor가 조목조목
반박한 것[^pie_flavor]도 같은 구조다 — 기술적으로 가능하다는 것과 생태계가 옮겨갈 이유가 있다는
것은 별개다.

돌파구가 있다면 신규 진입 지점일 것이다.
전체 이주가 아니라 새 프로젝트, 새 조직, 새 워크플로가 처음부터 여기서 시작하는 경로 말이다.
그런데 그 경로야말로 자체 호스팅이 쉬워야 열리는데, 앞서 본 대로 그쪽이 가장 약하다.

### 에이전트 워크플로가 탈중앙 포지의 첫 실용 명분이 될 수 있다

h1watt와 theptip이 각자 도달한 결론은 이 스레드에서 가장 흥미로운 대목이다.
둘 다 검열이나 이념이 아니라 에이전트 운영의 실무에서 출발했다[^h1watt][^theptip].

에이전트에게 코드 작업을 맡기면 신원과 권한 관리가 즉시 병목이 된다.
GitHub 모델에서는 에이전트마다 PAT를 발급하고 저장소 권한을 조정하고 만료를 관리해야 하는데,
이는 사람 사용자를 전제로 설계된 계정 체계에 비인간 행위자를 억지로 끼워 넣는 일이다.
키가 곧 신원이고 모든 산출물이 서명되는 모델에서는 에이전트에게 키를 하나 주는 것으로 끝난다.
그리고 어떤 커밋과 어떤 리뷰가 어느 키에서 나왔는지가 프로토콜 수준에서 검증 가능하다.

이것은 [Cursor Origin](../cursor/cursor-origin.md)이 에이전트 감사 추적을 자산으로 삼으려는
방향과 같은 문제를 정반대 방식으로 푸는 것이다.
Origin은 감사 추적을 플랫폼이 소유하는 데이터로 만들고, Radicle은 서명으로 저장소 안에 남긴다.
전자는 그 데이터를 근거로 락인을 만들 수 있고, 후자는 구조적으로 만들 수 없다.

다만 이 명분이 현실이 되려면 CI가 받쳐 줘야 하는데 아직 초기다.
esafak의 CI/PR 질문에 h1watt가 소개한 것은 실험적 단계의 구현이고[^esafak][^h1watt-ci],
2color가 설명한 `radicle-ci-broker`는 저장소 이벤트를 후킹해 사용하는 CI 도구별 어댑터를
띄우는 방식으로, 문서는 곧 나올 예정이라고 했다[^2color-ci].
에이전트가 만들어 낸 패치를 자동으로 검증하는 고리가 없으면 위 논리는 절반만 성립한다.

### 삭제 불가능성은 결함이 아니라 이 설계가 파는 상품의 뒷면이다

논쟁을 정리하면 이렇게 된다.
Radicle이 약속하는 것은 “당신의 데이터는 영원히, 안전하게”이고, 삭제 불가능성은 그 약속을 지킬 때
따라오는 필연이다.
어떤 주체도 데이터를 없앨 수 없다는 성질과, 당신이 데이터를 없앨 수 있다는 성질은 동시에 성립하지
않는다.

그러므로 이것을 로드맵으로 해결할 수 있는 결함으로 다루는 것은 양쪽 모두에게 정직하지 않다.
프로젝트는 그 사실을 명시하고 그 대가를 감수할 사용자를 고르는 편이 낫고, 사용자는 “언젠가 삭제
기능이 추가되겠지”라고 기대하지 않는 편이 낫다.
FAQ에서 관련 항목이 사라진 것은 그 반대 방향의 신호라 아쉽다.

실무적 함의는 경계 설정에 있다.
공개해도 되는 것과 실수로 공개되면 곤란한 것을 같은 시스템에 두지 않는 것이 유일한 방어다.
그런데 앞서 본 대로 Radicle은 비공개 저장소를 같은 시스템 안에 두면서 복제 정책으로만 구분한다.
설계 철학은 “지울 수 없음”을 받아들이라고 하고, 제품은 “비공개도 됩니다”라고 말한다.
이 둘이 화해하지 않은 채로 남아 있는 것이 지금 Radicle의 가장 큰 미해결 지점이다.

### 6년째 같은 자리에 있다는 것 자체가 하나의 데이터다

2019년, 2020년, 2024년, 그리고 2026년 — Radicle은 HN 프론트 페이지에 네 번 이상 올라왔고 매번
수백 점을 받았다.
동시에 매번 비슷한 질문이 반복된다.
스팸은 어떻게 막나, 비공개는 되나, 지울 수 있나, CI는 있나, 같이 쓸 사람은 어디 있나.

이 반복은 두 가지로 읽힌다.
하나는 문제 의식이 계속 살아 있다는 것이다 — 중앙 포지에 대한 불만은 사그라들지 않았고 오히려
[소유권이 바뀔 때마다](../cursor/cursor-origin.md) 되살아난다.
다른 하나는 6년 동안 그 불만이 이주로 이어지지 않았다는 것이다.

한편 프로젝트 자체는 살아 있다.
1.6.0에서 1.10.1까지 2026년에만 여섯 번 릴리스했고, NixOS 패키징 같은 커뮤니티 기여도 붙어
있으며[^Zopieux-nix], 서명된 레퍼런스의 취약점을 공개적으로 처리했다.
기여자들이 HN 스레드에서 거의 모든 질문에 직접 답한 것도 건강한 신호다.
탈중앙 포지의 실패 원인은 소프트웨어 품질이 아니라는 뜻이고, 그렇다면 남은 원인은 사람들이 모여
있는 곳을 바꾸는 문제인데, 그것은 기술 프로젝트가 혼자 풀 수 있는 종류가 아니다.

---

[^satvikpendem]: <https://news.ycombinator.com/item?id=48149222>
[^Zopieux]: <https://news.ycombinator.com/item?id=48154753>
[^vinnyhaps]: <https://news.ycombinator.com/item?id=48177407>
[^h1watt]: <https://news.ycombinator.com/item?id=48148412>
[^theptip]: <https://news.ycombinator.com/item?id=48157049>
[^2color-private]: <https://news.ycombinator.com/item?id=48158131>
[^incompleteCode]: <https://news.ycombinator.com/item?id=48152000>
[^gsaslis-public]: <https://news.ycombinator.com/item?id=48153648>
[^toyg]: <https://news.ycombinator.com/item?id=48153809>
[^figbert]: <https://news.ycombinator.com/item?id=48152944>
[^nine_k]: <https://news.ycombinator.com/item?id=48155785>
[^lukeck]: <https://news.ycombinator.com/item?id=48155192>
[^zfourhrms]: <https://news.ycombinator.com/item?id=48157569>
[^philsnow]: <https://news.ycombinator.com/item?id=48155532>
[^josh-sematic]: <https://news.ycombinator.com/item?id=48147881>
[^xvilka]: <https://news.ycombinator.com/item?id=48150357>
[^endiangroup-rip]: <https://news.ycombinator.com/item?id=48150409>
[^survirtual]: <https://news.ycombinator.com/item?id=48172188>
[^tsuraan]: <https://news.ycombinator.com/item?id=48153495>
[^gsaslis-spam]: <https://news.ycombinator.com/item?id=48153593>
[^Meneth]: <https://news.ycombinator.com/item?id=48154430>
[^endiangroup-infra]: <https://news.ycombinator.com/item?id=48155301>
[^einpoklum]: <https://news.ycombinator.com/item?id=48148240>
[^pessimizer]: <https://news.ycombinator.com/item?id=48149916>
[^pie_flavor]: <https://news.ycombinator.com/item?id=48152598>
[^esafak]: <https://news.ycombinator.com/item?id=48148384>
[^h1watt-ci]: <https://news.ycombinator.com/item?id=48148447>
[^2color-ci]: <https://news.ycombinator.com/item?id=48157990>
[^Zopieux-nix]: <https://news.ycombinator.com/item?id=48154766>
[^stchris]: <https://lobste.rs/s/6tbq79/radicle_peer_peer_stack_for_code#c_zrrpr4>
[^xla]: <https://lobste.rs/s/6tbq79/radicle_peer_peer_stack_for_code#c_xsrevl>
[^stchris-reject]: <https://lobste.rs/s/6tbq79/radicle_peer_peer_stack_for_code#c_cvcc2u>
[^mordae]: <https://lobste.rs/s/6tbq79/radicle_peer_peer_stack_for_code#c_ajcvok>
[^singpolyma]: <https://lobste.rs/s/6tbq79/radicle_peer_peer_stack_for_code#c_usunxt>
