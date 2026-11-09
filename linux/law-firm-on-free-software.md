# 영국 소규모 로펌 decoded.legal이 5년째 자유 소프트웨어로 사무소를 운영하는 2026년판 구성

원문: [Running a law firm on Free software (2026 edition) | decoded.legal's blog](https://decoded.legal/blog/2026/11/running-a-law-firm-on-free-software-2026-edition/)

HN 토론: <https://news.ycombinator.com/item?id=50403066> (294점, 139개 댓글)

GN 토론: <https://news.hada.io/topic?id=36769>

## 소개

영국 소규모 로펌 decoded.legal의 Neil Brown이 2026년 11월 6일에 쓴 글이다.
인터넷, 통신, 기술 법을 다루는 이 로펌을 클라이언트와 서버 모두 자유 소프트웨어로
운영한 지 약 5년이고, 첫 1년 뒤의 글(2022년)과 2024년 갱신에 이은 2026년판이다.
누군가 지금 무엇을 쓰는지 물어서 바뀐 부분을 정리했다고 한다.
이 문서는 글에 적힌 구성을 정리한 것이며 직접 시험하지 않았다.

글쓴이는 터미널 기반 도구를 많이 쓰는 이유를 터미널이 편해서이고
방해가 적으며 키보드에서 손을 떼지 않아도 되기 때문이라고 밝힌다.
mutt, vim, ikhal, ncmpcpp, newsboat, toot, links를 자주 쓴다고 한다.

## 클라이언트 쪽

주 컴퓨터는 Debian과 GNOME을 올린 ThinkPad X1 Yoga Gen 6이다.
화면을 접어 문서에 필기할 수 있어서 마음에 들지만
썬더볼트와 USB-C 포트의 데이터가 불안정해 교체를 고려한다고 한다.

| 용도        | 도구                                                   |
| ----------- | ------------------------------------------------------ |
| 이메일      | Thunderbird, mutt                                      |
| 문서 작성   | LibreOffice Writer(다른 변호사와 교환), pandoc과 typst |
| 발표        | reveal.js(Markdown으로 작성)                           |
| PDF         | evince, Xournal++, PDFarranger, pdftk                  |
| 텍스트 확장 | espanso                                                |
| 브라우저    | Firefox, links                                         |
| 노트와 지식 | vimwiki                                                |
| 암호화      | LUKS, Syncthing 전에 파일을 Cryptomator로 암호화       |
| 비밀번호    | Bitwarden(vaultwarden 서버), 민감한 곳은 YubiKey       |
| 문서 스캔   | paperless-ngx                                          |
| 모바일      | GrapheneOS를 올린 Pixel, F-Droid                       |

글쓴이는 다른 변호사와 문서를 주고받을 때만 Word 형식이 필요하다고 하고,
고객 다수가 Microsoft나 Apple 소프트웨어를 쓰지만 협업에는 문제가 전혀 없다고
적는다.
AI 도구는 쓰지 않는다고 하며 이유는 이 글에서 밝히지 않는다.

## 서버 쪽

Signal을 제외한 모든 것이 자체 호스팅이고 대부분 Intel NUC에서 돌며
Raspberry Pi는 줄었다고 한다.
주요 구성은 다음과 같다.

- 메일: postfix와 dovecot, 언젠가 Stalwart로 옮기는 것을 검토한다.
- 파일과 일정: Syncthing과 radicale(CalDAV와 CardDAV).
- 화상 회의: 예전에는 jitsi를 돌렸지만 대부분 다른 사람의 Teams나 Zoom에 참여해 중단하고 Signal을 제공한다.
- 업무 관리: 송장은 InvoicePlane(PDF 생성만), 시간 추적은 Kimai v2, 사건 관리는 EspoCRM.
- 보안: WireGuard(trailofbit의 algo 스크립트와 PiVPN), greenbone/OpenVAS 취약점 검사, Wazuh SIEM, Uptime Kuma 모니터링.
- 개발: Forgejo(웹사이트 버전 관리용이며 중요한 것은 인터넷에 열리지 않은 다른 기기의 git).
- 웹사이트와 블로그: mkdocs 정적 사이트를 apache2에 올리고 Tor의 .onion 버전도 운영한다. 블로그는 Hugo에서 bash 정적 사이트 생성기 BSSG로 옮겼다.
- Fediverse: glitch-soc Mastodon 포크를 쓰고 로펌 자체의 fedi 인스턴스는 껐다.
- 지식과 정책: Markdown 플러그인을 단 dokuwiki.
- DNS: Pi-Hole을 앞에 둔 unbound. 예전의 DoH 서버는 껐다.
- 백업: restic과 rsync.
- 양식: LiberaForms로 고객 사전 확인(KYC) 설문 등을 받고, 응답이 서버에 암호화되어 저장된다.

바뀐 것은 몇 가지다.
Nextcloud가 문제를 해결하기보다 만들어서 Syncthing과 radicale로 옮겼다.
거의 쓰이지 않은 jitsi와 CryptPad(공동 문서 편집)는 껐다.
공동 편집은 지금 하지 않는다고 적는다.

## 비평

### 한 사람의 구성이 조직의 지속성에 대한 질문을 남긴다

HN에서 skeeter2020은 변호사가 법에 집중하길 바라며,
글쓴이에게 무슨 일이 생기면 다른 변호사나 법률 보조원이 어떻게 이어받느냐고
물었다.[^skeeter2020]
99harry는 DevOps 담당이 한 사람이라는 점이 가장 큰 걱정이며
고객이 기업이나 은행이면 보안 인증이 필요할 수 있다고 했다.[^99harry]
글은 직원 수, 고객 유형, 인증, 승계 계획을 다루지 않는다.
이 글이 고객을 위한 것은 아닐 것이라고 NoboruWataya는 짚었다.[^noboruwataya]
그러므로 이 구성이 큰 조직에도 옮겨지는지는 이 글로 알 수 없다.

### 유지 비용이 글에 나오지 않는다

pclowes는 읽으면 갖고 싶어지지만 합치면 유지하기가 힘들어 보이며,
이 구성이 변호사로서 더 효과적으로 만드는지,
취미에 가까운 것이 아니냐고 물었다.[^pclowes]
글은 도구를 열거하고 바뀐 이유를 짧게 적지만 운영에 쓰는 시간은 말하지 않는다.
Nextcloud를 버린 이유가 문제를 만들었기 때문이라는 한 줄에서 유지 비용의 일부가
드러날 뿐이다.

### 메일 전달 신뢰도는 자체 호스팅의 가장 약한 고리다

raegis는 25년 넘게 postfix로 메일 서버를 돌렸지만
몇 년 전 Gmail이 서버 암호화 규칙을 강화해 수신이 반송된 적이 있었고,
업무용으로 쓰려면 대형 제공자들이 만든 불문율을 계속 점검해야 한다고
했다.[^raegis]
글쓴이는 메일 인프라를 언젠가 옮기고 싶다고 쓸 뿐 현재의 전달 문제는 밝히지 않는다.
메일은 법률 업무에서 놓치면 안 되는 매체이므로 이 부분은 글이 다루지 않은 위험이다.

### 도구 선택과 직업상의 호환 규범이 부딪힐 수 있다

HN에서 Tomte는 법률 워크숍에서 Word를 쓰지 않는 것이 과실에 해당한다는 이야기를
들었다고 전했다.
이에 미국 변호사라고 밝힌 droidjj는 Word를 쓰지 않는 것이 일률적으로 과실은
아니며 법원이 docx를 요구하는데 rtf로 제출하는 것처럼 상황에 달렸다고
답했다.[^tomte][^droidjj]
글쓴이는 다른 변호사와 문서를 교환할 때만 LibreOffice로 Word 형식을 쓴다고 하고
문제가 없었다고 말한다.
이것은 영국 소규모 로펌의 한 경험이다.

## 도입 전에 따져볼 것

- 협업 도구를 처음부터 쓸 것인지 정한다. 글쓴이는 공동 문서 편집을 포기했고 Nextcloud도 접었다.
- 메일은 전달 문제를 감당할 수 있는지 먼저 따진다. 자체 서버를 계속 운영한다면 대형 제공자로 보내는 시험을 주기적으로 한다.
- 한 사람이 모든 것을 아는 상태를 피하는 방법을 마련한다. 정책은 dokuwiki에 기록한다는 글쓴이의 선택이 그 일부다.
- 고객 대면 접점(화상 회의, 양식)은 상대가 쓰는 도구를 따라간다. 글쓴이는 jitsi를 접고 Signal과 상대의 Teams와 Zoom 참여로 바꿨다.
- 법원, 상대 변호사, 고객이 요구하는 파일 형식이 있는지 먼저 확인한다.
- 백업과 암호화(LUKS, Cryptomator, restic)는 도구를 늘리기 전에 정한다.

---

[^skeeter2020]: <https://news.ycombinator.com/item?id=50405010>

[^99harry]: <https://news.ycombinator.com/item?id=50404437>

[^pclowes]: <https://news.ycombinator.com/item?id=50406396>

[^raegis]: <https://news.ycombinator.com/item?id=50408309>

[^tomte]: <https://news.ycombinator.com/item?id=50404694>

[^droidjj]: <https://news.ycombinator.com/item?id=50405035>

[^noboruwataya]: <https://news.ycombinator.com/item?id=50406353>
