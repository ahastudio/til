# 디스크에 SSH 키를 두지 않기: YubiKey, TPM, Secure Enclave로 옮긴 기록

원문: [I deleted all my SSH keys](https://blog.infected.systems/posts/2026-11-03-i-deleted-all-my-ssh-keys/)

HN 토론: <https://news.ycombinator.com/item?id=50382401> (277점, 151개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys>

GN 토론: <https://news.hada.io/topic?id=36960>

## 요약

infected.systems 블로그의 글쓴이는 ed25519-sk 키를 YubiKey와 함께 오래 써
왔지만, 일부 용도 때문에 디스크에 저장하는 전통적인 키가 남아 있었다.
이 글은 YubiKey, TPM, Apple Secure Enclave 세 가지 하드웨어로 키 재료를
보관하거나 암호화해서 디스크에 보호되지 않은 키가 하나도 없도록 만든 과정을
정리한다.

글쓴이는 먼저 패스프레이즈로 충분하냐고 묻고, 대부분의 위협 모델에서는 아마
충분하다고 인정한다.
패스프레이즈는 bcrypt와 AES로 키를 보호하고, ssh-agent를 쓰면 한 세션에 한 번만
입력하면 된다.
그래도 하드웨어 키로 옮기려는 이유는 만족감이 주된 것이라고 밝힌다.
이점은 키를 만든 하드웨어가 있어야만 키를 쓸 수 있다는 것이다.
글은 2026년 11월 4일에 올라왔고, 목표는 세 가지다.
하드웨어에 상주하는 키로 완전히 옮기고, 가능한 한 추가 소프트웨어 없이 기본
기능으로 하며, LXC 안에서 실행하거나 SSHFS 서버를 사람 없이 마운트하는 실제
상황에서 시험하는 것이다.

### 방법 1: YubiKey

YubiKey 5 이상에서는 `ssh-keygen -t ed25519-sk -O resident` 명령으로
OpenSSH만으로 키를 장치에 등록할 수 있다.
`-O application="ssh:이름"`의 응용 프로그램 태그는 임의의 문자열이며, 한 장치에
키를 여러 개 만들 때 구별하는 용도다.
`ykman fido credentials list`로 장치에 등록된 자격 증명을 볼 수 있지만 `ykman`은
필수가 아니고 관리 편의를 위한 것이다.
공개 키는 일반 SSH 공개 키처럼 `authorized_keys`나 Git 호스팅 서비스에 넣는다.
디스크에 남는 `id_ed25519-sk` 파일은 개인 키처럼 보이지만 키 재료가 아니라
하드웨어에서 키를 찾는 핸들일 뿐이다.
기본 설정에서는 키를 쓸 때마다 YubiKey를 만져야 한다.
무인 사용이 필요하면 `no-touch-required` 키를 만들고 서버의 `authorized_keys`
항목 앞에도 같은 옵션을 붙여야 하지만, 이 경우 호스트에 접근한 공격자가 키를
훔치지는 못해도 사람 없이 쓸 수는 있다고 경고한다.

### 방법 2: TPM

YubiKey는 비싸므로 이미 있는 TPM을 쓰는 방법으로 Go 패키지 ssh-tpm-agent를
소개한다.
`ssh-tpm-keygen`으로 키를 만들고, TPM을 인식하는 에이전트를 systemd 소켓으로
켠다.
사람 없이 쓰거나 셸이 없는 systemd 마운트 단위에서 쓰려면 `-N ""`로 PIN 없는
키를 만들고 `SSH_AUTH_SOCK` 대신 `~/.ssh/config`에 소켓 경로를 적는다.
이 경로는 사용자 ID가 바뀌지 않아야 예측할 수 있다는 조건이 붙는다.
글쓴이는 여기에 중요한 단서를 단다.
TPM은 SSH 키를 직접 등록하는 기능이 없어서 개인 키 재료가 암호화된 형태로
디스크에 저장되고 TPM이 이를 풀어 준다.
TPM 없이는 쓸 수 없으니 장치에 묶인 자격 증명이지만, `-sk` 키처럼 장치 안에
상주하는 자격 증명과는 다르다.
또 ssh-tpm-agent는 부팅 상태를 기록하는 PCR 값을 보지 않으므로 펌웨어나 OS가
바뀌어도 키를 푸는 것을 거부하지 않는다.

### 방법 3: Apple Secure Enclave

macOS Sequoia부터 스마트 카드 인증 기능이 SSH 키를 신원으로 다룬다.
`sc_auth create-ctk-identity -k p-256-ne -t bio`로 내보낼 수 없는 키를 만들고
Touch ID를 요구하도록 한다.
이어 `ssh-keygen -w /usr/lib/ssh-keychain.dylib -K`로 핸들 파일을 내보내고
`SSH_SK_PROVIDER` 환경 변수를 설정한다.
이 명령은 등록된 모든 키의 핸들을 한꺼번에 내보내고, 글쓴이는 Apple 문서가 된다고
하는 `KEYCHAIN_CERTIFICATES`로도 키 하나만 내보내는 방법을 찾지 못했다.
그래서 `-l` 라벨을 알아보기 쉽게 붙여 두라고 권하며, 핸들 파일 이름에 이 라벨이
들어간다.
macOS의 SSH 에이전트가 이 핸들을 자동으로 찾지 못해서 글쓴이는
`~/.ssh/config`의 `IdentityFile`에 직접 적었다.
덮개를 닫고 쓰는 clamshell 모드에서는 키 생성이 “Touch ID is not available in
closed clamshell mode” 오류로 실패한다.
글쓴이는 Safari 키체인이나 Apple Pay와 달리 `-t bio` 키가 생성과 사용 모두에서
비밀번호로 대체되지 않는다고 설명한다.
대안은 `-t none`으로 존재 확인을 끄거나(YubiKey 무인 사용과 같은 위험),
Touch ID가 달린 Apple 블루투스 키보드를 사거나, 닫힌 맥북 옆면에 거의 붙는 작은
YubiKey 5C Nano를 방법 1로 쓰는 것이다.

글쓴이는 마지막으로 이 방식의 약점을 짚는다.
키가 하드웨어에 상주하므로 장치가 고장나거나 분실되면 키를 쓸 수 없고, 그러니
키를 여러 개 두고 `authorized_keys`에 모두 등록해 두는 것이 최선이라고 한다.

## 분석

### 이 글의 핵심은 “키를 가진 것”과 “키를 쓸 수 있는 것”을 떼어 놓는 데 있다

글의 세 방법은 같은 목표의 다른 수준이다.
YubiKey는 키 재료가 장치 밖으로 나오지 않고, TPM은 암호화된 키가 디스크에 있지만
TPM 없이는 쓸 수 없고, Secure Enclave는 내보낼 수 없는 키를 장치 안에 둔다.
Lobste.rs 사용자 tuxes는 이 차이를 분명히 했다.
KeePassXC 보관소를 열면 키가 메모리에 올라가므로 암호화된 키 파일을 쓰는 일반
ssh-agent와 크게 다르지 않고, 이 글은 하드웨어에 상주하는 키를 다룬다는
것이다.[^f6wjua]
HN의 anyfoo도 키가 하드웨어 밖에서 접근되지 않고 서명 같은 연산만 요청할 수
있어서 파일 시스템에 접근한 사람이 키를 복사할 수 없다는 점을 이 접근의 요점으로
짚었다.[^anyfoo]
palata는 컴퓨터가 침해되면 SSH 키와 패스프레이즈를 모두 복사당해도 알 수 없지만,
YubiKey는 패스프레이즈가 유출되어도 장치를 훔쳐야만 쓸 수 있고 훔치면 알게
된다고 설명했다.[^palata]
이 때문에 “패스프레이즈로 충분한가”라는 글쓴이의 첫 질문은 위협 모델에 달려
있다.

### TPM 방식의 단서가 실제로는 가장 큰 구별선이다

글쓴이는 TPM 방식이 키를 디스크에 암호화해 두므로 YubiKey 방식과 다르다고 직접
밝혔다.
HN 사용자 Foxboron은 이 대목을 인용하며 사실이라고 인정하되, 정적 계층 키(static
hierarchy key)를 쓰면 키 파일 없이 TPM에서 키를 다시 만들 수 있다고 보충했다.
그 경우 TPM에 접근할 수 있는 사람은 누구나 키를 재생성할 수 있어서 소유자
비밀번호를 설정해야 한다는 조건도 달았다.[^Foxboron]
Lobste.rs의 eny5dv도 ssh-tpm-agent가 계층 키로 같은 것을 지원한다고
적었다.[^eny5dv]
이는 글의 단서가 정확하다는 확인이면서, 키 파일을 남기지 않는 선택지가 하나 더
있다는 보충이다.

## 비평

### 가장 큰 쟁점은 가용성이고 글은 한 문단으로만 다룬다

글은 하드웨어가 고장나면 키를 쓸 수 없다고 인정하고 복수의 키를 권하는 것으로
끝낸다.
그러나 독자들이 가장 많이 묻은 질문이 이것이다.
data-ottawa는 YubiKey의 수명과 교체 절차를 물었고,[^data-ottawa] traceroute66은
YubiKey를 쓰는 사람은 최소 두 개를 가져야 하며 이는 IT 장비의 이중화 기본이라고
답했다.[^traceroute66]
Lobste.rs의 vbernat은 TPM이 좋은 절충안이지만 서버에 기기마다 키를 밀어 넣어야
하고 예비 YubiKey와 예비의 예비까지 필요하냐고 물었다.[^vbernat]
이에 Foxboron은 키마다 서버에 등록하지 말고 SSH CA로 각 키를 인증하고 서버에는
CA만 배포하라고 권했다.[^Foxboron-lob]
글이 “여러 키를 `authorized_keys`에 넣으라”는 해법으로 마무리하는 것은
소규모에서만 맞고, 키가 늘면 서명 기반 운영으로 넘어가야 한다는 점이 빠져 있다.

### 하드웨어 키는 모든 환경에서 받아들여지지 않는다

Lobste.rs의 varesa는 ed25519-sk 키를 쓰려 했지만 LTS 배포판의 OpenSSH가 너무
오래되어 이해하지 못하고, 사용자 지정 CLI의 네트워크 장비는 ed25519가 아닌 키를
거부하며, 클라우드 인스턴스 프로비저닝도 받아들이지 않는다고 썼다.[^varesa]
글쓴이는 LXC와 SSHFS 마운트를 시험 목표로 적었지만 본문에는 두 시험의 결과가
따로 없고, 이런 호환성 한계도 다루지 않는다.
무인 사용 항목이 그 시험에 가장 가까운 내용이다.
이 한계는 사용자의 경험이고 환경마다 다를 수 있다.
그래도 도입 비용을 판단하려면 대상 서버의 OpenSSH 버전을 먼저 확인해야 한다는
신호다.

### 사용 편의의 대안이 같은 목표를 달성하는지는 입장이 갈린다

비밀번호 관리자를 SSH 에이전트로 쓰는 방식이 대안으로 많이 나왔다.
Lobste.rs의 benoliver999는 KeePassXC에 키를 넣는 간이 방식을 쓴다고
했고,[^benoliver999] patryk는 YubiKey로 키를 쓰는 방식은 코드를 푸시할 때
번거로워 비밀번호 관리자의 에이전트가 적당한 절충이라고 썼다.[^patryk]
juri는 1Password가 누가 키를 요청하는지 창으로 알려 주는 것이 YubiKey가 구석에서
약하게 깜빡이는 것보다 낫다고 했다.[^juri]
이것은 사용성 비교이고 위협 모델이 다르다는 뜻이다.
patryk 스스로 PC가 해킹될 가능성이 비밀번호 관리자 해킹보다 높다는 가정이라고
밝혔다.[^patryk-2]
글의 목표가 “디스크에 보호되지 않은 키 없음”이므로 이 대안들은 목표를 달성하지
못한 채 더 편한 것을 택한 경우다.

### 존재 확인을 끄는 선택의 비용이 과소 서술된다

글은 `no-touch-required`와 PIN 없는 TPM 키를 무인 사용 때문에 소개하고 위험을
언급한다.
그러나 이 선택은 하드웨어 키의 핵심 이점인 “사람이 있어야 쓴다”를 없앤다.
tuxes는 자신이 LLM 에이전트에 SSH 접근을 주면서, 키가 새지 않도록 에이전트 전용
ssh-tpm-agent와 TPM 키를 따로 만들었다고 썼다.[^tuxes]
이 사례는 무인 사용에서도 키를 용도별로 분리하면 위험을 줄일 수 있다는 구체적인
방법이다.

## 인사이트

### 하드웨어에 상주하는 키는 키 관리를 “분실”의 문제로 바꾼다

키를 유출하는 위험은 줄지만 키를 잃는 위험이 커진다.
이 거래가 맞는지는 키를 누가 어디에 얼마나 등록해 두었는지에 달려 있다.
carlomonte는 보안의 CIA 가운데 가용성(A)을 들어, 백업은 내가 내용을 소유하지만
YubiKey나 TPM의 내용은 소유하지 못한다고 지적했다.[^carlomonte]
그러므로 도입 순서는 키를 만든 뒤가 아니라, 복구 경로(예비 키, SSH CA, 비상용
접근)를 먼저 정하는 것이다.
이는 이 문서의 제안이다.

### 서버 쪽 인증 구조가 클라이언트 쪽 보호의 한계를 정한다

클라이언트 키가 아무리 안전해도 서버가 키마다 한 줄씩 등록하는 구조면 키가 늘
때마다 등록과 폐기 작업이 늘어난다.
SSH CA는 이 부담을 서버에서 CA 하나로 줄여 주고, 키의 유효 기간과 허용 주체를
제한할 수 있다.
binarin도 YubiKey를 CA로 써서 만료와 허용 주체가 제한된 인증서를 발급하는 방식을
언급했다.[^binarin]
이 글의 방법은 클라이언트 쪽에 한정되므로, 팀이나 다수 서버 환경에서는 인증서
쪽을 함께 봐야 한다.

### 결론을 바꿀 관찰

- 대상 서버와 장비의 OpenSSH가 모두 `-sk` 키를 받아들인다면, 호환성 우려는
  사라지고 YubiKey 방식의 비용은 하드웨어 가격과 복구 절차만 남는다.
- 패스프레이즈를 건 키와 하드웨어 키를 쓴 환경의 침해 사례를 비교한 자료가 나와
  큰 차이가 없다면, 글쓴이가 말한 “대부분의 위협 모델에서는 충분하다”가 더
  강하게 읽힌다.
- 무인 사용이 필요한 작업에서 용도별 TPM 키가 실제로 유출 사고를 막았다는 사례가
  쌓이면, 존재 확인을 끄는 선택의 위험이 줄어든다.

---

[^f6wjua]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_f6wjua>

[^anyfoo]: <https://news.ycombinator.com/item?id=50445441>

[^palata]: <https://news.ycombinator.com/item?id=50446367>

[^Foxboron]: <https://news.ycombinator.com/item?id=50443632>

[^eny5dv]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_eny5dv>

[^data-ottawa]: <https://news.ycombinator.com/item?id=50445221>

[^traceroute66]: <https://news.ycombinator.com/item?id=50446730>

[^vbernat]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_o1wmse>

[^Foxboron-lob]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_2jvibq>

[^varesa]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_syawgh>

[^benoliver999]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_hx2mzn>

[^patryk]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_ivpfpf>

[^juri]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_vpmib7>

[^patryk-2]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_dmknts>

[^tuxes]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_eselk1>

[^carlomonte]: <https://lobste.rs/s/sdtcvv/i_deleted_all_my_ssh_keys#c_styrdq>

[^binarin]: <https://news.ycombinator.com/item?id=50445361>
