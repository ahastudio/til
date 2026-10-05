# NotionSSH: Notion 페이지에 적은 명령을 서버에서 실행하는 도구

<https://github.com/mirseo/notionSSH>

Show GN: [Show GN: NotionSSH - VPN 없이도 Notion으로 원격 서버를 제어하세요](https://news.hada.io/topic?id=23014)

## 소개

NotionSSH는 Notion 페이지에 명령을 적으면 그 페이지를 지켜보는 서버가 셸로
실행하고 결과를 같은 페이지에 붙여 주는 Rust 프로그램이다.
작성자 mirseo는 2025년 9월 11일 GeekNews에 Show GN으로 올리며,
HTTP와 HTTPS는 되지만 SSH와 RDP는 막아 둔 곳이 있어서 만들었다고 소개했다.
Notion에 `!(docker ps)`처럼 쓰면 해당 페이지를 모니터하는 머신이 실행하고 결과를
돌려준다는 설명이다.

저장소는 2025년 9월 10일에 만들어졌고 라이선스는 MIT다.
2026년 10월 5일 기준 스타는 11개이고 마지막 커밋은 2025년 9월 20일이다.
커밋 기록을 보면 9월 10일 첫 구현과 Linux 지원, 9월 11일 Windows 유니코드
처리, CA 인증서 검증, 사용자 권한 기능이 하루 사이에 들어갔다.
README의 한 줄 소개는 Notion 페이지와 연동되는 원격 명령 실행 도구이며,
실제로는 1초에 한 번 페이지를 확인한다고 덧붙인다.
나는 이 도구를 설치하거나 실행하지 않았고, 아래 내용은 README, `docs/access.md`,
`docs/ca.md`, GeekNews 토론에서 확인한 것이다.

## 동작 방식

### 페이지를 폴링하는 실행기

NotionSSH는 서버에서 계속 돌면서 지정한 Notion 페이지의 블록을 읽는다.
명령은 일반 단락이나 할 일 블록에 `!(명령)` 형식으로 쓴다.
README가 설명하는 처리 순서는 다음과 같다.

1. 페이지에서 `!(명령)` 패턴이 있는 새 블록을 찾는다.
2. 명령을 파싱하고 이미 실행했다는 표시가 있는지 확인한다.
3. 플랫폼에 맞는 셸로 명령을 실행한다.
4. 출력과 실행 메타데이터를 모은다.
5. 결과를 페이지에 코드 블록으로 붙인다.
6. 감사 기록을 남긴다.

결과 블록에는 명령 출력과 함께 실행한 사용자의 이메일, 머신 이름, 타임스탬프,
그리고 `# notionSSH-executed` 표시가 들어간다.
이 표시가 같은 명령을 다시 실행하지 않게 막는다.
Windows에서는 `cmd /C`로, Linux와 macOS에서는 `$SHELL`, `bash`,
`sh` 순서로 셸을 찾아 실행한다.

연결 방향이 이 도구의 핵심이다.
서버가 Notion API로 나가는 HTTPS 요청만 하므로 인바운드 포트를
하나도 열 필요가 없다.
사용자와 서버 사이에 Notion 서버가 끼어 있는 구조이고,
작성자는 SSH라는 이름을 붙인 이유를 서버, Notion 서버, 사용자로 이어지는
구조에서 셸 접근이 안전하다고 보았기 때문이라고 설명했다[^gn-mirseo-name].
처음 버전은 키 교환 방식의 Discord용이었는데 불편해서 쓰지 않게 되었고,
비밀번호를 Notion에 올리기도 곤란해 페이지를 읽는 방식으로 바꿨다고
한다[^gn-mirseo-history].

### 설정

필요한 것은 Rust 1.70 이상, Notion 통합(integration)의 API 키,
명령을 적을 페이지 URL이다.

```bash
git clone https://github.com/mirseo/notionSSH
cd notionSSH
cargo build --release

export NOTION_API_KEY="secret_xxxxxxxxxxxxx"
export NOTION_PAGE_URL="https://www.notion.so/your-page-id"
./target/release/notionSSH
```

환경 변수 없이 실행하면 대화형으로 값을 묻고
`.notionSSH/storage.json`에 저장한다.
Notion 통합은 Internal 유형으로 만들고,
통합이 접근할 페이지는 꼭 필요한 페이지만 고르라고 README는 권한다.
로그는 두 가지가 남는다.
`./logs/command.YYYYMMDD.log`에는 명령과 사용자 이메일이, `./log`에는 명령,
요청자, 시각, 노드, 상태를 담은 CSV 감사 기록이 쌓인다.

### 권한 제어와 인증서 검증

GeekNews에서 보안 지적을 받은 뒤 두 기능이 추가되었다.
첫째는 `.notionSSH/access.json`의 사용자별 권한이다.
이메일을 권한 그룹에 묶고, 그룹마다 `allow`와 `deny` 목록을 둔다.

```json
{
  "emails": { "intern@company.com": "readonly_user" },
  "perm_manager": ["admin@company.com"],
  "perms": {
    "default": { "allow": ["ls", "pwd", "whoami", "date", "ps"], "deny": [] },
    "readonly_user": { "allow": ["ls", "pwd", "whoami", "date"], "deny": ["*"] }
  }
}
```

판정 순서는 `perm_manager` 확인, 이메일로 그룹 결정(없으면 `default`),
`deny` 검사, `allow` 검사, 그리고 명시적으로 허용되지 않은 명령 거부다.
공백이 없는 규칙은 명령의 첫 토큰만 대소문자 구분 없이 비교하고,
공백이 있는 규칙은 명령 앞부분이 일치하는지 본다.

둘째는 Notion API 서버를 확인하는 세 단계 검증이다.
표준 CA 체인 검증, DNS over HTTPS로 받은 IP 확인,
미리 저장한 인증서 지문과 비교하는 인증서 핀(pinning)으로 이루어진다.
처음 실행할 때 사용 여부를 묻고,
지문은 `verify/notion-api.verify`와 `.notionSSH/ca.json`에 저장된다.

## 트레이드오프

### 포트를 열지 않는 대신 Notion 계정이 곧 루트 셸이 된다

README의 보안 항목은 이 도구가 자체 인증을 하지 않고 Notion의 사용자
관리를 믿는다고 밝힌다.
명령은 NotionSSH 프로세스와 같은 권한으로 실행된다.
즉 그 페이지의 편집 권한을 가진 사람,
또는 통합 API 키를 가진 사람은 서버에서 셸을 쓸 수 있다.
SSH의 키 인증과 달리 Notion 계정의 비밀번호, 세션,
공유 설정이 모두 서버 접근 경로가 된다.

GeekNews에서 ifmkl은 이것이 엄밀히 보면 원격 코드 실행(RCE)이며,
서버의 에이전트가 외부 페이지의 명령을 검증 없이 무조건 신뢰하는 구조라 매우
위험하다고 지적했다[^gn-ifmkl].
geekapple은 웹셸이 대표적인 보안 구멍인데 노션셸이라니 보안 담당자가
기절하겠다고 적었다[^gn-geekapple].
작성자는 유사 웹셸처럼 동작할 수 있다는 점을 인정하면서,
로그를 남기니 탐지할 수는 있을 것이라고 답했다[^gn-mirseo-webshell].
이후 추가된 권한 제어는 이메일 기준으로 명령을 제한하지만, 그 이메일 역시
Notion이 알려 주는 값이다.

### 명령 목록 필터는 셸 앞에서 약하다

권한 규칙은 명령 문자열의 첫 토큰이나 앞부분을 비교한다.
그러나 실행은 셸을 거치므로, 셸 문법으로 명령을 감싸거나 이어 붙이면 첫 토큰과
실제 실행 내용이 달라질 수 있다.
예를 들어 `ls`만 허용된 그룹이라도 `ls; 다른 명령`처럼 쓰면 첫 토큰은 `ls`다.
문서에서 이런 경우를 막는다는 설명을 찾지 못했으므로,
허용 목록을 보안 경계로 쓰려면 직접 확인해야 한다.
이것은 문서를 읽고 내린 추론이며 코드를 실행해 확인한 것은 아니다.

### 1초 폴링은 즉시성과 API 사용량을 맞바꾼다

페이지를 1초마다 읽으므로 명령은 길게는 1초 정도 늦게 실행되고,
결과도 Notion에 블록으로 쓰인 뒤에야 보인다.
대화형 셸처럼 쓸 수는 없고, 출력이 긴 명령은 페이지를 금방 무겁게 만든다.
Notion API에는 요청 속도 제한이 있으므로 여러 서버가 같은 통합 키로 폴링하면
제한에 걸릴 수 있다.
이 부분은 README가 다루지 않는다.

## 함정

### 조직의 보안 정책을 우회하는 도구가 된다

작성자는 학교 보안팀이 인바운드와 아웃바운드 모두 80, 443 포트의 HTTP와 HTTPS만
허용해서 Cloudflare Tunnel과 Tailscale도 규정 위반이 될 수 있다고 들었다고
설명했다[^gn-mirseo-policy].
그러면서 승인을 받을 수는 있지만 절차가 까다롭고 규정이 복잡해서 이런 방식을
만들었다고 덧붙였다[^gn-mirseo-approval].
regentag는 자신이 보안팀이라면 알게 된 순간 바로 차단할 것이며,
승인 절차가 있는데도 우회한다면 더욱 그렇다고 답했다[^gn-regentag].
kunggom은 이것을 섀도 IT(Shadow IT)라고 부른다고 짚었다[^gn-kunggom].
작성자는 실제로 쓰려는 것보다 이런 것이 있으면 어떨까 하는 사이드 프로젝트라고
답했다[^gn-mirseo-side].

포트를 막는 정책은 SSH라는 프로토콜이 아니라 외부에서 셸에 닿는
경로를 막으려는 것이다.
그 경로를 HTTPS 폴링으로 다시 만들면 정책의 의도는 그대로 깨진다.
회사나 학교 네트워크에서 이 도구를 쓰기 전에 보안 담당자의
승인을 받는 것이 먼저다.

### 망 분리 환경에서는 쓸 수 없다

beoks는 SSH 접속이 필요한 서버 일부는 인터넷이 막힌 폐쇄망에 있어 Notion을 쓸 수
없을 것이라고 지적했다[^gn-beoks].
작성자는 보안이 중요한 서버라면 이 방식보다 Tailscale 같은 것이 더 안전할
것이라고 인정했다[^gn-mirseo-tailscale].
반대로 이 도구가 동작한다는 것은 그 서버가 외부 SaaS에 계속 연결되어
있다는 뜻이기도 하다.

### `rm`은 기본으로 막히지 않았다

t7vonn이 `!(rm -rf /)`라는 한 줄을 댓글로 남기자[^gn-t7vonn],
작성자는 권한 제한이 필요하겠다고 답했다[^gn-mirseo-rm].
이후 최신 버전에서는 ACL이 추가되어 보안 설정 상황에서 `rm` 같은 명령이 기본
차단된다고 다시 답했다[^gn-mirseo-acl].
다만 `docs/access.md`의 `default` 그룹 예시는 여전히 `"allow": ["*"]`로
시작하므로, 설정을 바꾸지 않으면 모든 명령이 허용될 수 있다.
설치 직후 `access.json`을 열어 `default` 그룹을 좁히는 것이 첫 작업이어야 한다.

### 프로젝트의 지속성

토론 도중 저장소에 접근할 수 없다는 댓글이 달렸다[^gn-kaydash].
thinkpad는 작성자의 다른 페이지에 이 프로젝트가 미지원 및 삭제됨으로 표시되어
있다고 알렸다[^gn-thinkpad].
작성자는 개인 이메일과 여러 SNS로
보안 위험이 너무 크다는 지적을 계속 받으면서 무서웠고,
그래서 성급하게 3일 동안 저장소를 비공개로 돌렸다고 사과했다[^gn-mirseo-scared].
다른 답글에서는 추가 개발 일정을 잡고 다시 공개로 전환했다고
밝혔다[^gn-mirseo-private].
마지막 커밋이 2025년 9월이므로,
의존할 도구라기보다 구조를 참고할 실험으로 보는 편이 맞다.

## 대안

GeekNews 댓글에는 같은 문제를 다르게 푸는 도구가 여럿 나왔다.
cocofather는 22번 포트를 열 수 없는 것이 문제라면 SSH 포트를 바꾸거나 Cloudflare
Tunnel을 쓰는 방법이 있다고 했다[^gn-cocofather].
seokzoo는 원격 데스크톱 게이트웨이인 Apache Guacamole을 소개했고[^gn-seokzoo],
작성자는 써 봤지만 VNC 특성상 느려서 지연
때문에 영향을 많이 받았다고 답했다[^gn-mirseo-guacamole].
cgl00은 P2P로 SSH를 잇는 Rust 크레이트 `iroh-ssh`를 알려 주었다[^gn-cgl00].

| 방식              | 열어야 하는 것     | 인증 주체         | 비고                      |
| ----------------- | ------------------ | ----------------- | ------------------------- |
| SSH 포트 변경     | 인바운드 포트 하나 | SSH 키            | 포트 차단 정책이면 불가   |
| Cloudflare Tunnel | 아웃바운드 HTTPS   | Cloudflare Access | 조직 정책 확인 필요       |
| Tailscale         | 아웃바운드 연결    | Tailscale 계정    | 작성자 환경에서 규정 우려 |
| Guacamole         | 게이트웨이 서버    | Guacamole 계정    | 브라우저로 SSH, RDP, VNC  |
| NotionSSH         | 아웃바운드 HTTPS   | Notion 계정       | 자체 인증 없음            |

## 기억할 원칙

### 아웃바운드만 쓰는 원격 실행은 인증을 외부에 넘긴다

인바운드 포트를 열지 않는 원격 실행 도구는 모두 같은 구조를 가진다.
서버가 어딘가로 나가서 할 일을 가져오고, 그 어딘가를 믿는다.
NotionSSH에서는 그 어딘가가 Notion이고,
Cloudflare Tunnel이나 Tailscale에서는 각 회사의 인증 체계다.
차이는 그 중간 서비스가 셸 접근을 위한 인증과 감사 기능을 갖추었느냐에 있다.
문서 협업 도구를 셸 접근의 인증 경계로 쓰면,
문서를 공유하는 일이 곧 서버 권한을 나누는 일이 된다.

---

[^gn-mirseo-name]: <https://news.hada.io/topic?id=23014#cid43655>

[^gn-mirseo-history]: <https://news.hada.io/topic?id=23014#cid43653>

[^gn-ifmkl]: <https://news.hada.io/topic?id=23014#cid43656>

[^gn-geekapple]: <https://news.hada.io/topic?id=23014#cid43641>

[^gn-mirseo-webshell]: <https://news.hada.io/topic?id=23014#cid43645>

[^gn-mirseo-policy]: <https://news.hada.io/topic?id=23014#cid43667>

[^gn-mirseo-approval]: <https://news.hada.io/topic?id=23014#cid43668>

[^gn-regentag]: <https://news.hada.io/topic?id=23014#cid43686>

[^gn-kunggom]: <https://news.hada.io/topic?id=23014#cid43692>

[^gn-mirseo-side]: <https://news.hada.io/topic?id=23014#cid43688>

[^gn-beoks]: <https://news.hada.io/topic?id=23014#cid43659>

[^gn-mirseo-tailscale]: <https://news.hada.io/topic?id=23014#cid43660>

[^gn-t7vonn]: <https://news.hada.io/topic?id=23014#cid43633>

[^gn-mirseo-rm]: <https://news.hada.io/topic?id=23014#cid43644>

[^gn-mirseo-acl]: <https://news.hada.io/topic?id=23014#cid43663>

[^gn-kaydash]: <https://news.hada.io/topic?id=23014#cid43735>

[^gn-thinkpad]: <https://news.hada.io/topic?id=23014#cid43739>

[^gn-mirseo-scared]: <https://news.hada.io/topic?id=23014#cid44563>

[^gn-mirseo-private]: <https://news.hada.io/topic?id=23014#cid44559>

[^gn-cocofather]: <https://news.hada.io/topic?id=23014#cid43666>

[^gn-seokzoo]: <https://news.hada.io/topic?id=23014#cid43763>

[^gn-mirseo-guacamole]: <https://news.hada.io/topic?id=23014#cid44557>

[^gn-cgl00]: <https://news.hada.io/topic?id=23014#cid43631>
