# macOS 기본 도구만으로 Secure Enclave에 SSH 키를 두는 방법과 접어 둔 이유

원문: [Protecting SSH Keys with macOS Secure Enclave](https://gatezh.com/posts/macos-secure-enclave-ssh-keys/)

HN 토론: <https://news.ycombinator.com/item?id=50449748> (360점, 130개 댓글)

GN 토론: <https://news.hada.io/topic?id=36985>

## 요약

gatezh 블로그의 글쓴이는 `~/.ssh/`에 파일 권한만으로 놓인 SSH 키가 악성
스크립트에 복사될 수 있다는 걱정에서 이 글을 시작한다.
가짜 면접 과제로 저장소를 내려받아 실행하게 하는 사례를 들고, 이미 개발
컨테이너로 전환했지만 그것만으로는 부족했다고 말한다.
보호 방법으로 네 가지를 꼽는다.
macOS 기본 Secure Enclave, 서드파티 앱 Secretive, YubiKey, 1Password나 Bitwarden
같은 보관소의 SSH 에이전트다.
보관소 방식은 키가 메모리에서 복호화되는 소프트웨어 해법이라 제외하고, 키를 꺼낼
수 없는 하드웨어를 원해서 YubiKey와 Secure Enclave 중 추가 장비와 앱이 없는 기본
방식을 먼저 시험했다.

글쓴이가 설명하는 방식은 macOS Sequoia 이후 지원되는 Secure Enclave 기반 SSH
키다.
키가 칩 안에서 만들어져 밖으로 나오지 않고, SSH가 접속할 때 맥이 Secure
Enclave에 인증 요청의 서명을 맡긴다.
Touch ID를 켜면 서명마다 승인해야 한다.
디스크에는 개인 키 대신 이 맥에서만 쓸 수 있는 참조 파일이 남는다.

설정 절차는 다음과 같다.
1. `sc_auth create-ctk-identity -l "ssh-MacBook" -k p-256-ne -t bio`로 내보낼 수
   없는 P-256 키를 만들고 Touch ID를 매번 요구하게 한다.
2. `ssh-keygen -w /usr/lib/ssh-keychain.dylib -K -N ""`로 키 핸들 파일을
   내보낸다.
3. 셸 설정에 `SSH_SK_PROVIDER=/usr/lib/ssh-keychain.dylib`를 추가한다.
4. 공개 키를 서버의 `authorized_keys`에 넣는다.
5. `~/.ssh/config`에 이 핸들 파일을 `IdentityFile`로 직접 적는다.

글쓴이는 세 가지 문제를 겪었다.
- Touch ID 등록이 초기화되어 키 생성이 `Failed to get bio catacomb UUID` 오류로
  실패했고, 지문을 다시 등록해서 해결했다.
- 온라인 안내가 말하는 `ssh-add -K`는 폐기되었고, 새 옵션도 CryptoTokenKit
  키에는 통하지 않아 `SSH_SK_PROVIDER` 환경 변수가 맞는 방법이었다.
- SSH가 `id_ecdsa_sk_rk`라는 이름의 파일은 자동으로 찾지 않아서 설정에 명시해야
  했다.
1Password의 `IdentityAgent`와도 충돌했다.

결론은 반전된다.
이 방식은 완전히 동작하고, 그것 자체로는 쓸 만한 해법이라고 인정하지만, Touch ID
창이 “ctccardtoken needs to authenticate to continue”라고 떠서 너무 못생겼다는
이유로 쓰지 않기로 했다.
이 창은 Apple이 마감하지 않은 저수준 프레임워크 CryptoTokenKit에서 나온다.
권장 사항은 Touch ID를 모든 키에 쓰는 것이다.
키를 쓰는 일을 항상 알 수 있고, 하루에 몇 번 더 누르는 것은 작은 대가라는
이유다.
한계는 백업이 없다는 점이다.
키가 그 맥에 묶여 있으므로 맥이 죽으면 키도 죽고, 그래서 YubiKey나 다른 맥의
백업 키를 `authorized_keys`에 함께 넣으라고 한다.

글 맨 위의 11월 11일 갱신에서 글쓴이는 Secretive로 옮겼고, 훨씬 나은 확인 창을
쓴다고 밝힌다.
2부도 예고한다.
또 공개 키 줄 끝의 `ssh:`를 FIDO2 응용 프로그램 ID라고 쓴 부분은 실제로는
주석이었고, Hacker News 사용자의 지적으로 고쳤다고 적는다.

## 분석

### 이 방식의 이점은 “키를 훔칠 수 없다”가 아니라 “쓸 때마다 알게 된다”에 가깝다

키가 하드웨어를 떠나지 않으므로 악성 코드가 파일을 복사해 다른 곳에서 쓰는 것은
막힌다.
HN에서 Gigachad는 패스프레이즈를 건 키도 키보드 입력을 읽거나 암호를 입력하게
속이는 악성 코드, macOS 취약점으로 메모리를 읽는 공격에는 약하지만 Secure
Enclave는 개인 키에 접근하는 것이 불가능해야 한다고 짚었다.[^Gigachad]
mjg59는 매번 패스프레이즈를 입력하지 않는다면 키가 RAM에 있어 악성 코드가 꺼낼
수 있고, 매번 입력하는 것은 Touch ID 같은 물리적 확인보다 훨씬 성가시다고
썼다.[^mjg59]
Vegenoid는 SSH 인증이 서명으로 키 소유를 증명하는 것이고, Secure Enclave는 서명
인터페이스만 노출하므로 키를 얻으려면 물리적 접근이 필요하다고
설명했다.[^Vegenoid]
글쓴이도 같은 방향으로 결론 낸다.
Touch ID를 끄면 악성 코드가 조용히 키를 쓸 수 있으므로 모든 키에 켜 두라는
것이다.

### 글의 가치는 막힌 지점을 그대로 적은 데 있다

오류 메시지, 폐기된 명령, 이름 때문에 키를 찾지 못한 증상을 순서대로 적어서 같은
길을 가는 사람의 시간을 줄여 준다.
이런 기록은 기본 도구로 가능한지를 판단하는 근거가 된다.
가능하지만 설정이 많고 알아 두어야 하는 함정이 있다는 것이 이 글의 결론이다.

## 비평

### 글의 출발 전제가 패스프레이즈를 건너뛴다는 반박이 많았다

LeBit는 글이 키를 파일 시스템에 두기 싫다는 틀린 전제에서 출발한다고 지적했다.
키는 패스프레이즈로 보호하고 ssh-agent가 메모리에 올려 두며, macOS의 OpenSSH에는
`UseKeychain` 설정이 있다는 것이다.[^LeBit]
글이 패스프레이즈 보호를 비교 대상으로 두지 않은 것은 사실이다.
다만 앞서 인용한 mjg59와 tiberious726의 반박도 있다.
tiberious726은 디스크의 키와 패스프레이즈는 1요소 인증이고, Secure Enclave의
키와 해제 PIN은 2요소 인증이라고 정리했다.[^tiberious726]
LeBit의 반박은 위협 모델이 다르다는 지적이지 이 방식이 틀렸다는 증명은 아니다.

### 기본 기능이 문서화되지 않았다는 위험

Gigachad는 이 기능이 문서화된 것이 아니라 누군가 우연히 발견한 것처럼 보여서,
Apple이 나중에 바꾸거나 없애면 키가 잠길까 걱정된다고 했다.[^Gigachad-2]
cavoirom은 이는 기기를 잃는 것과 같으니 반드시 두 번째 백업 키를 두고 Secure
Enclave 키는 버려도 되는 키로 취급하라고 답했다.[^cavoirom]
database64128은 시스템 업그레이드 뒤 WireGuard 앱이 키체인에서 구성을 열지
못하고 프로필을 모두 “고아”로 지웠던 경험을 들며, 이런 보안 기능은 어느 날
갑자기 문제가 된다고 썼다.[^database64128]
이 사례는 다른 앱의 키체인 문제이고 SSH 키와 직접 관련은 없지만, 키가 장치에
묶인 방식이 같은 종류의 위험을 지닌다는 근거다.

### 사람이 있어야 하는 방식은 자동화와 부딪친다

computerfriend는 터치를 캐시할 방법이 없어서 리베이스가 잦은 작업에서 커밋
서명용으로 거의 쓸 수 없다고 했다.[^computerfriend]
mavam은 에이전트 개발에서는 Secure Enclave 키 접근에 사람이 있어야 해서,
로그인하지 않은 헤드리스 환경에서는 Secretive도 접근하지 못한다고 하며 이 방식이
안정적으로 확장될지 회의적이라고 썼다.[^mavam]
글은 Touch ID가 귀찮으면 두 번째 키를 만들면 된다고 하지만, 이런 자동화 사례는
다루지 않는다.

### 글쓴이가 결론을 접은 이유는 미관이다

글쓴이는 실용성이 아니라 못생긴 UI가 이유라고 스스로 밝힌다.
이는 솔직한 서술이지만, 독자가 판단해야 할 기준은 기능이 아니라 취향이 되어
버린다.
기본 방식의 실제 단점(백업 불가, 문서화 부재, 자동화 곤란)은 그가 갈아탄
Secretive에도 그대로 적용된다.
petesergeant는 Secretive도 시작이 Secure Enclave인 키는 백업할 수 없다고
썼다.[^petesergeant]
결국 글쓴이가 바꾼 것은 확인 창뿐이고 보안 모델은 같다.

## 인사이트

### 하드웨어 키 도입의 비용은 설정이 아니라 운영 시나리오에서 나온다

설정은 한 번이지만 백업, 헤드리스 접근, 서명 작업은 매일 부딪친다.
HN 댓글에서 드러난 사용 사례는 세 가지로 갈린다.
개인 작업용(Touch ID를 감수), 저장소 접근용(dsenkus는 VM에 에이전트만 전달해 깃
동작마다 지문을 요구한다고 했다[^dsenkus]), 자동화용(사람이 없으면 안 된다)이다.
용도별로 키를 나누는 것이 현실적인 설계로 보이며, 이 문서의 제안이다.

### 보안 확인의 빈도가 방어력을 낮춘다

jen729w는 하루 스무 번의 지문 요청을 받으면 근육 기억이 그냥 승인해 버릴까
걱정되어, 위험이 없는 개발 환경 키는 확인을 면제하고 1Password의 `op`를 쓴다고
썼다.[^jen729w]
글쓴이의 “매번 Touch ID”라는 권고는 확인이 드물 때만 안전하다는 한계가 있다.
이 한계는 한 사용자의 증언이며 얼마나 일반적인지는 알 수 없다.

### 결론을 바꿀 관찰

- Apple이 Secure Enclave SSH 키 흐름을 문서화하고 확인 창을 정리한다면,
  “못생겨서 접는다”는 이유가 사라지고 기본 방식이 첫 선택이 된다.
- 키를 잃은 사례를 모았을 때 백업 키가 있던 경우와 없던 경우의 복구 비용이 크게
  다르다면, 백업 키를 필수로 보는 권고가 강해진다.
- 헤드리스 자동화에서도 사람이 없이 서명할 수 있는 안전한 방식이 나온다면,
  에이전트 개발에서의 확장성 우려가 줄어든다.

---

[^Gigachad]: <https://news.ycombinator.com/item?id=50450366>

[^mjg59]: <https://news.ycombinator.com/item?id=50450718>

[^Vegenoid]: <https://news.ycombinator.com/item?id=50450583>

[^LeBit]: <https://news.ycombinator.com/item?id=50450330>

[^tiberious726]: <https://news.ycombinator.com/item?id=50451863>

[^Gigachad-2]: <https://news.ycombinator.com/item?id=50449914>

[^cavoirom]: <https://news.ycombinator.com/item?id=50449960>

[^database64128]: <https://news.ycombinator.com/item?id=50450079>

[^computerfriend]: <https://news.ycombinator.com/item?id=50450786>

[^mavam]: <https://news.ycombinator.com/item?id=50450945>

[^petesergeant]: <https://news.ycombinator.com/item?id=50449954>

[^dsenkus]: <https://news.ycombinator.com/item?id=50450027>

[^jen729w]: <https://news.ycombinator.com/item?id=50450593>
