# Rayfish - Iroh 위에 지은 인프라 없는 P2P 메시 VPN

<https://rayfish.xyz/blog/01-introducing-rayfish>

HN 토론: <https://news.ycombinator.com/item?id=48746038> (117점, 107개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh>

## 소개

Rayfish는 서버, 계정, 포트 포워딩, 고정 IP 없이 개인 네트워크를 구성하는
피어-투-피어(P2P) 메시 VPN이다.
공식 소개 문구는 "당신만의 개인 네트워크.
서버도, 설정도 필요 없다"이다.
저장소 설명은 이를 한 문장으로 압축한다.
"인프라가 전혀 없는 P2P 메시 VPN(A peer-to-peer mesh VPN with zero
infrastructure)."

핵심 아이디어는 두 가지다.
첫째, 모든 머신이 암호화 신원(cryptographic identity)을 가지며, 그 신원에서
안정적이고 충돌 없는 가상 IP(IPv4는 `100.64.0.0/10`, IPv6는 `200::/7`)가
파생된다.
둘째, 네트워크를 유지하는 데 상시 가동 서버가 필요 없다.
DHT를 통해 피어끼리 서로를 자동으로 찾고, 네트워크를 처음 만든 코디네이터는
한 번만 온라인이었다가 그 뒤로는 오프라인이어도 나머지 피어들의 연결이
유지된다.

라이선스는 Mozilla Public License 2.0이며, 아직 "실험적인 pre-1.0
소프트웨어"로 표시돼 있다.
제작진 스스로 프로덕션 사용은 권장하지 않고, 홈랩이나 친구들끼리의 네트워크
같은 용도를 우선 대상으로 삼는다.

## 아키텍처

동작 흐름은 단순하다.
각 머신에서 데몬이 실행되며 TUN 디바이스를 만들어 IP 패킷을 붙잡은 뒤, 그
패킷을 iroh의 QUIC 연결을 통해 터널링한다.

네트워크 생성부터 사용까지는 네 단계로 나뉜다.

- Create: 한 피어가 네트워크를 시작하며 코디네이터 역할을 맡는다.
- Join: 나머지 피어가 일회용 초대 코드나 실시간 승인을 거쳐 입장한다.
- Mesh: 입장한 모든 피어가 서로 직접 연결을 맺는다.
- Use: 이후로는 평범한 TCP/UDP 애플리케이션처럼 사용한다.

기능 구성은 다음과 같다.

| 기능 | 설명 |
| --- | --- |
| 폐쇄형 네트워크 | 기본값이 폐쇄형이며 일회용 초대 코드, 재사용 가능한 키, 실시간 승인 세 방식을 지원 |
| 직접 P2P 연결 | `ray connect <id>` 로 접촉 ID만으로 둘만의 네트워크 즉시 생성 |
| Magic DNS | `name.network.ray` 형식으로 가상 IP 대신 이름으로 피어 접근 |
| 디바이스별 방화벽 | 상태 기반 TCP/UDP 규칙과 방향성 제어 |
| Mesh SSH | 키를 따로 배포하지 않고 신원 기반 인증으로 SSH 접속 |
| 선언형 프로비저닝 | YAML 스펙으로 네트워크·방화벽 구성을 자동화 |
| 다중 디바이스 ID | 암호화 키를 백업하고 1Password 같은 도구와 연동 |
| 파일 공유 | `ray send file.zip bob` 형태로 피어 간 파일 전송 |

CLI 사용 흐름의 예시는 다음과 같다.

```bash
ray create --hostname alice          # 네트워크 생성
ray invite gentle-amber-fox          # 일회용 초대 코드 발급
ray join <코드> --hostname bob       # 가입
ping alice.gaming.ray                # 이름으로 접근
ray ping alice                       # 메시 프로브(RTT, 직접/릴레이 경로 확인)
ray firewall add in allow -p tcp --port 22
```

권한 모델도 명확히 나뉜다.
`status`처럼 읽기만 하는 명령은 로컬 사용자 누구나 실행할 수 있지만, 설정을
바꾸는 명령은 root이거나 별도로 지정된 operator 권한이 있어야 한다.
설치를 수행한 사용자는 자동으로 operator가 된다.

## Iroh와의 관계

Rayfish의 P2P 직결과 NAT 통과는 Iroh가 제공하는 홀 펀칭과 종단간 암호화
위에서 이뤄진다.
직접 경로가 불가능한 약 10%의 경우에는 암호화된 릴레이로 자동 전환된다.
이는 이 저장소의 Iroh 관련 TIL(`iroh.md`, `iroh-v1-release.md`)에서 다룬
"NAT 홀 펀칭 우선 시도, 실패 시 공개 릴레이로 우회"라는 iroh의 하이브리드
라우팅 구조를 그대로 물려받은 것이다.
Rayfish는 여기에 UPnP·NAT-PMP·PCP 지원을 더해 라우터 차원의 포트 개방도
함께 시도한다.

Lobste.rs 토론에서 tuxes는 Iroh의 이 NAT 통과 능력을 Yggdrasil 대비 Rayfish의
실질적 우위로 꼽았다.[^tuxes]
ecksdee는 Iroh가 QUIC을 기반으로 삼는다는 점에서 향후 양자내성(post-quantum)
암호화로 확장할 여지가 있다는 점을 짚었고, 이를 Tailscale이 갖지 못한 또
다른 격차로 언급했다.[^ecksdee-quic]
즉 Rayfish 입장에서 Iroh는 "공개키로 다이얼한다"는 저수준 정체성·전송
문제를 대신 풀어주는 기반 계층이며, Rayfish는 그 위에 VPN 특유의 기능
(가상 IP 대역, Magic DNS, 방화벽, 초대·승인 흐름)을 쌓은 애플리케이션에
해당한다.

## 분석

### 기존 VPN 스택이 상시 서버를 요구했던 이유를 되짚는다

Tailscale, ZeroTier, Nebula 같은 메시 VPN은 모두 "메시"를 표방하지만, 어느
지점에는 예외 없이 조정 서버(coordination server)가 남아 있다.
Tailscale은 자체 컨트롤 플레인을, ZeroTier는 루트 서버를, Nebula는 인증서를
발급하는 CA를 각각 요구한다.
이 조정 지점은 피어 발견과 신뢰의 시작점을 해결해 주지만, 동시에 "그
서버가 없으면 네트워크도 없다"는 단일 의존을 만든다.

Rayfish의 설계는 이 의존을 코디네이터의 "일회성 온라인"으로 축소한다.
네트워크를 처음 만든 피어가 한 번은 온라인이어야 하지만, 그 뒤로는 DHT를
통한 발견으로 나머지 피어들이 서로를 계속 찾을 수 있다.
이는 상시 서버 자체를 없앤 것이 아니라, "부트스트랩의 순간"과 "지속적
가동"을 분리한 것에 가깝다.
후자를 없앴다는 점이 Rayfish가 스스로를 "인프라 없음"이라 부르는 근거다.

### VPN을 "네트워크 하나"가 아니라 "여러 네트워크 동시 소속"으로 재정의한다

Lobste.rs에서 valpackett이 짚은 대목은 Rayfish 설계의 핵심을 건드린다.[^valpackett]
"한 번에 둘 이상의 네트워크를 다루는 것"을 예외가 아니라 기본 전제로
삼았다는 점이다.
Tailscale류 도구는 한 기기가 하나의 tailnet에 속하는 모델을 기본으로
하고, 여러 네트워크 동시 소속은 부차적으로 지원된다.

Rayfish의 `ray connect <id>` 로 즉석에서 둘만의 네트워크를 만드는 기능이나
다중 디바이스 ID 지원은 이 전제를 코드 차원에서 구현한 결과로 읽힌다.
한 사람이 회사 네트워크, 홈랩 네트워크, 친구들과의 게임 네트워크에 동시에
속하는 상황이 예외가 아니라 기본 시나리오라는 관점의 전환이다.

## 비평

### "인프라 없음"의 실제 범위는 DHT 부트스트랩과 릴레이에 걸려 있다

Rayfish가 "제로 인프라"를 표방하지만, 이는 문자 그대로 아무 인프라도 없다는
뜻이 아니다.
DHT를 통한 발견도, 직접 경로가 실패했을 때의 암호화 릴레이도 결국 어딘가의
네트워크 인프라에 의존한다.
HN 이용자 keepupnow는 더 직설적으로, WAN을 넘어 두 피어를 연결하려면
어떤 형태로든 조정 서버가 필요하다는 점에서 이런 P2P 제품들을
"서버 없음"이라고 부르는 것 자체가 부정확하며, Rayfish도 Iroh의
디스커버리·릴레이 인프라에 의존하고 있다는 사실을 더 명확히 밝혀야
한다고 주장했다.[^keepupnow]
Iroh 자체의 TIL에서 이미 짚었듯, 홀 펀칭 실패 시의 릴레이 폴백은 "순수
P2P"에서 한 발 물러선 타협이며, 그 릴레이를 누가 운영하고 어떤 가용성을
보장하는지는 Rayfish의 문서만으로는 드러나지 않는다.
Rayfish가 이 릴레이 인프라를 Iroh의 공개 릴레이에 그대로 얹었는지, 자체
운영으로 대체했는지에 따라 "인프라 없음"의 실질적 의미가 크게 달라진다.

### 비교 대상 서술의 정확도에 대한 커뮤니티의 이의 제기

Lobste.rs에서 Corbin은 Rayfish가 Yggdrasil과 자신을 비교한 대목이
불완전하고 부정확하다고 지적했다.
Yggdrasil도 비공개 네트워크 구성이 가능하며, 소규모 그룹에는 tinc가 더
적합할 수 있다는 것이다.[^corbin]
tuxes는 이에 대해 Yggdrasil에는 "분리된 프라이빗 네트워크"라는 개념 자체가
없고 승인 절차나 친숙한 DNS 이름도 없다는 점을 들어 Rayfish의 실질적
개선을 옹호했다.[^tuxes-defense]
이 논쟁은 신생 프로젝트의 소개 글이 흔히 겪는 문제를 보여준다.
경쟁 도구를 단순화해 서술하면 자신의 우위가 선명해 보이지만, 그 단순화가
과녁을 벗어나면 오히려 신뢰도를 깎는다.

mempko가 제기한 "ZeroTier One과 무엇이 다른가"라는 질문도 같은 결의
지적이다.
ZeroTier는 10년 넘게 존재해 온 P2P 소프트웨어이며, Rayfish가 내세우는
가치 제안 다수(피어 발견, NAT 통과, 폐쇄 네트워크)를 이미 구현해 왔다.
Rayfish의 소개 자료가 이 오래된 경쟁자와의 구체적 차별점을 충분히
설명하지 않는다면, 독자는 "왜 지금 새로 나온 것을 써야 하는가"라는 질문에
스스로 답을 채워야 한다.[^mempko]

### AI 저작에 대한 의구심이 신뢰도 문제로 번졌다

Lobste.rs의 여러 댓글이 별도로 짚은 지점은 기술이 아니라 글쓰기 방식이다.
baetylboy는 소개 글의 일부가 AI로 작성된 것처럼 읽혀서 거슬렸다고
밝혔고, valpackett은 저장소에 있는 `CLAUDE.md` 파일(AI 보조 작업 기록)을
근거로 실제 기여도에 비해 AI 사용 흔적이 두드러진다는 의견을 냈다.[^valpackett-ai]
HN에서도 같은 우려가 나왔다.
rsyring은 코드베이스가 생긴 지 몇 주밖에 안 됐는데 커밋 속도가 매우
빠르다는 점에서 LLM 개입이 상당했을 것으로 추정했고, 저장소에 있는
큰 `CLAUDE.md` 파일이 일반적인 에이전트 지침 관행과도 어긋난다고
지적하며 저자의 LLM 활용 경험 자체에 의문을 제기했다.
개인 Tailscale 네트워크를 관리할 도구로 흥미를 느끼면서도, 아직
신뢰할 만한 신호가 충분하지 않다는 것이 결론이었다.[^rsyring]
소프트웨어 자체의 완성도와 무관하게, 소개 자료의 문체가 신뢰를 깎을 수
있다는 점은 오픈소스 프로젝트 공개 시점에 흔히 간과되는 리스크다.

### 플랫폼 커버리지의 공백

baetylboy는 Rayfish가 실제로 흥미롭다고 인정하면서도 Android 지원이
없다는 점을 이주(migration)의 걸림돌로 꼽았다.[^baetylboy]
mdaniel은 저장소에 Android 구현 코드가 이미 존재하고 nightly 태그로 디버그
APK가 배포되고 있다고 정정했지만, 이는 정식 지원과 실험적 빌드 사이의
간극을 보여준다.[^mdaniel]
모바일이 개인 네트워크의 실사용에서 큰 비중을 차지한다는 점을 고려하면,
이 공백은 초기 채택의 실질적 장벽으로 남는다.

## 인사이트

### "제로 인프라"라는 표현은 인프라의 소멸이 아니라 이전을 가리킨다

Iroh의 1.0 릴리스를 다룬 이 저장소의 앞선 TIL은 "중앙 의존은 사라지는 게
아니라 계층을 옮겨 다닌다"는 결론에 도달했다.
Rayfish는 이 관찰을 한 겹 위에서 재현한다.
VPN 조정 서버라는 눈에 보이는 인프라를 없앴지만, 그 자리를 DHT 발견과
Iroh 릴레이라는 눈에 덜 띄는 인프라가 채운다.

이것이 나쁘다는 뜻은 아니다.
사용자가 직접 서버를 띄우고 관리할 필요가 없어졌다는 것만으로도 실질적인
운영 부담 감소다.
다만 "제로 인프라"라는 표현이 정확히 무엇을 없앴는지 — 사용자가 관리해야
할 인프라를 없앤 것이지, 인프라 자체가 사라진 것은 아니다 — 를 분명히
하지 않으면, 이는 Iroh 자체가 이미 겪은 "탈중앙 수사와 릴레이 의존의
간극"을 그대로 물려받게 된다.

### 애플리케이션 계층에서 P2P 인프라가 재조립되는 흐름의 한 사례

Iroh의 v1 릴리스 TIL은 Iroh를 "네트워크 계층이 아니라 애플리케이션 계층의
Tailscale"이라 부른 HN 댓글을 인용했다.
Rayfish는 그 관찰을 그대로 검증하는 사례다.
Iroh가 라이브러리로 제공한 "공개키로 다이얼하고, 홀 펀칭하고, 실패하면
릴레이로 우회한다"는 저수준 능력을, Rayfish는 VPN이라는 익숙한 사용자
경험(가상 IP, DNS 이름, 방화벽 규칙, 초대 코드)으로 감싸 재조립했다.

이 패턴은 앞으로도 반복될 가능성이 높다.
Iroh 같은 P2P 저수준 스택이 성숙해질수록, 그 위에 특정 사용 사례(VPN,
파일 공유, 메시징, 협업 도구)를 씌운 애플리케이션이 빠르게 늘어난다.
Rayfish는 "VPN"이라는 가장 직관적이고 검증된 사용 사례를 먼저 택했다는
점에서, Iroh 생태계가 실제 제품으로 옮겨가는 초기 단계를 보여주는
지표이기도 하다.

### 코디네이터의 "일회성 온라인"이라는 타협이 향후 신뢰 모델의 시험대가 된다

Rayfish의 설계에서 가장 흥미로운 지점은 코디네이터가 처음 한 번만
온라인이면 된다는 조건이다.
이는 상시 서버를 없앴다는 마케팅과, 그럼에도 최초 신뢰의 근원(root of
trust)이 특정 피어에게 남아 있다는 현실 사이의 타협이다.
코디네이터가 영구히 사라지면(기기 분실, 폐기) 그 네트워크의 관리 권한이나
신규 참여 승인은 어떻게 이어지는지가 문서에 명시돼 있지 않다.

이는 Iroh의 v1 TIL이 짚은 "키 관리가 새로운 DNS 문제가 된다"는 통찰과
같은 축에 있다.
개인키가 곧 정체성이자 권한인 시스템에서, 그 키를 쥔 최초 소유자가
사라졌을 때의 승계 경로는 P2P 계열 도구 대부분이 아직 충분히 답하지 못한
질문이다.
Rayfish가 pre-1.0 단계를 벗어나 실사용 규모로 커진다면, 이 승계와 신뢰
이전의 문제가 기능 목록보다 먼저 해결돼야 할 과제로 떠오를 것이다.

---

[^valpackett]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_vtjq6a>
[^valpackett-ai]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_vtjq6a>
[^ecksdee-quic]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_eeuk09>
[^tuxes]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_caawz7>
[^tuxes-defense]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_caawz7>
[^corbin]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_eeeqka>
[^mempko]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_svtulz>
[^baetylboy]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_j8d0w7>
[^mdaniel]: <https://lobste.rs/s/4behtu/rayfish_p2p_vpn_built_on_top_iroh#c_nl8mzl>
[^keepupnow]: <https://news.ycombinator.com/item?id=48796218>
[^rsyring]: <https://news.ycombinator.com/item?id=48796027>
