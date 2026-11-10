# Tiny Little Office: 링크 자체가 문서인 작은 오피스 도구 모음

<https://tinylittleoffice.com/>

<https://github.com/aboard-io/tinylittleoffice>

HN 토론: <https://news.ycombinator.com/item?id=50096142> (705점, 202개 댓글)

GN 토론: <https://news.hada.io/topic?id=35390>

## 소개

Tiny Little Office는 문서가 링크 안에만 존재하는 웹 오피스 도구 모음이다.
URL을 쓰면 문서가 만들어진다.
계정이 필요 없고,
사용자가 이 기기에 보관하겠다고 고르지 않는 한 문서는 아무 데도 저장되지 않는다.
Aboard가 만들었고 MIT 라이선스로 무료로 제공된다.
소스는 GitHub의 `aboard-io/tinylittleoffice`에 있으며,
저장소는 2026년 10월 5일에 만들어졌다.[^gh-api]
2026년 11월 10일에 확인한 저장소는 별 612개, 포크 41개, 열린 이슈 30개다.
앱은 스물한 개 언어로 나왔고, 사이트는 스스로 이를 대부분 뉴욕에서 쓰는
언어라고 설명한다.

공개 직후의 반응은 만든 Paul Ford의 글에 적혀 있다.
Ford는 공개 첫 주에 방문자가 몰려 Cloudflare 무료 요금제의 한도를 넘겨
신용카드를 등록해야 했고, 약 20만 명이 다녀갔으며,
The Register가 기사를 썼고 Product Hunt 상위 열 곳에도 한동안 올랐다고
한다.[^ford]
이 수치는 글쓴이 본인의 서술이며 이 문서가 따로 확인한 것은 아니다.

열 개의 앱이 있다.[^llms]

| 앱 ID     | 앱            |
| --------- | ------------- |
| `write`   | 워드 프로세서 |
| `outline` | 아웃라이너    |
| `deck`    | 프레젠테이션  |
| `sheet`   | 스프레드시트  |
| `calc`    | 계산기        |
| `draw`    | 그림 도구     |
| `diagram` | 다이어그램    |
| `anim`    | 애니메이터    |
| `cal`     | 캘린더        |
| `trip`    | 여행 계획     |

## 동작 방식

### 문서는 `#` 뒤에 들어 있다

문서는 Markdown에 몇 가지를 더한 TLO 형식으로 쓰이고,
퍼센트 인코딩되어 URL의 `#doc=` 뒤에 들어간다.[^llms]

```text
https://tinylittleoffice.com/<app>/#doc=<퍼센트 인코딩한 TLO>
```

`#` 뒤의 부분은 브라우저가 서버에 보내지 않는다.
링크를 열면 편집기에 문서가 보이고, 연 사람은 누구나 고칠 수 있으며,
타이핑이 멈추면 주소가 편집을 따라 바뀌어 새 링크가 곧 새 문서가 된다.
“브라우저에 저장”은 기본으로 꺼져 있고, 켜면 문서를 자기 브라우저에만 보관한다.
짧은 링크를 만들면 서버가 그 문서를 서버가 모르는 키로 암호화해 만료될 때까지
보관한다.[^llms-full]
이것 말고 서버가 문서의 일부를 읽을 수 있게 되는 경우가 하나 더 있는데,
아래의 미리보기 카드다.

예를 들어 다음 링크는 이름 붙은 줄로 저녁 비용을 나누는 계산기 문서다.

```text
https://tinylittleoffice.com/calc/#doc=---%0Atitle%3A+Dinner+for+six%0A---%0Afood+%3D+164.50%0Adrinks+%3D+58%0Atip+%3D+%28food+%2B+drinks%29+%2A+18%25%0Atotal+%3D+food+%2B+drinks+%2B+tip%0Atotal+%2F+6
```

### 비밀번호와 미리보기 카드

저장소의 위협 모델 문서(`docs/threat-model.md`)는 두 가지를 더 말한다.
하나는 비밀번호로 문서를 봉인하는 기능이다.
2026년 10월 11일부터 비밀번호는 사용자가 입력하지 않고 앱이 만든다.
56자 알파벳에서 20자를 무작위로 뽑으며 엔트로피는 약 116비트이고,
키 유도는 HKDF(SHA-256) 한 번, 암호는 AES-256-GCM이다.
봉인된 문서는 변조되면 열리지 않으므로 전달 중의 변경도 막는다.
비밀번호가 없는 문서는 링크를 넘겨받은 사람이 내용을 바꿀 수 있다.

다른 하나는 미리보기 카드다.
Bluesky, Mastodon, X, LinkedIn이나 공유 시트로 공유할 때
“첫 쪽의 미리보기 보이기”가 켜져 있으면(기본값이다)
첫 쪽의 그림, 제목, 첫 200자가 사이트의 `/card`로 올라가 암호화되지 않은 채
한 달 동안 읽을 수 있게 보관된다.
공유 네트워크가 읽어 가야 하기 때문이다.
문서 자체와 링크는 올라가지 않고, 편집 링크, 발표 링크, 이메일 공유와
비밀번호가 있는 문서는 카드를 만들지 않는다.
그래서 “서버에는 아무것도 가지 않는다”는 말은 이 스위치를 끈 경우에만
정확하다.

### 네트워크로 나가는 것

저장소의 `docs/network.md`는 사이트가 할 수 있는 모든 요청을 표로 나열한다.
문서를 여는 데는 사이트 자신의 파일만 요청하고,
그 밖의 요청은 짧은 링크, 미리보기 카드, 여행 계획의 지도(OpenFreeMap과
OpenStreetMap의 타일, 장소 검색에는 Nominatim)가 전부다.
원격 측정(telemetry)이 없고 분석 스크립트나 외부 글꼴도 없으며,
콘텐츠 보안 정책(Content-Security-Policy)이 허용하는 곳만 브라우저가
열어 준다고 문서가 설명한다.

### 문서 안의 문서

어떤 앱의 문서든 워드 프로세서 페이지, 슬라이드, 아웃라인 항목 안에
앱 ID로 이름 붙인 펜스(`sheet`, `calc`, `anim` 등)로 넣을 수 있다.
그 앱이 그 자리에서 화면에 그려지고 편집된다.
슬라이드에 넣은 애니메이션은 발표할 때 재생되고,
페이지나 덱의 PDF와 덱의 PowerPoint에도 그려진 채로 들어간다.[^llms]

### 내보내기와 에이전트

모든 문서는 PDF, PNG, HTML, Markdown,
그리고 자체 형식 `.tlo`로 내려받을 수 있다.[^llms-full]
사이트는 `llms.txt`로 에이전트에게 링크로 문서를 만드는 법을 설명하고,
브라우저, Deno, Bun에서는
`https://tinylittleoffice.com/api.js`의 `link`, `read`, `lint`를,
Node에서는 `npx tinylittleoffice`를 쓸 수 있다.
`skill --into` 명령으로 이 안내를 Claude Code 스킬로 설치할 수도 있다.[^llms]
HN의 simonw는 Claude 같은 도구에 `llms.txt`를 읽히기만 하면
문서를 그리는 URL을 만들 수 있다며,
그렇게 만든 URL 형식 설명 덱을 공유했다.[^simonw]

## 길이 한도

| 값            | 한도         | 이유                                         |
| ------------- | ------------ | -------------------------------------------- |
| 권장 URL 길이 | 2,000자 미만 | 일부 채팅 앱이 약 2,000자 넘는 링크를 자른다 |
| QR 코드       | 2,953자      | QR 코드 하나가 담을 수 있는 최대치           |
| 짧은 링크     | 12,272자     | 서버에 암호화해 보관하는 경우                |

출처는 모두 사이트의 전체 설명서다.[^llms-full]

## 트레이드오프

### 서버가 없는 대신 링크가 곧 비밀이다

문서가 `#` 뒤에 있어 서버에 가지 않는다는 것은 개인정보 보호 면에서 큰 장점이다.
그러나 같은 이유로 링크를 가진 사람은 누구나 문서 전체를 읽고 고칠 수 있다.
링크를 메신저에 붙이면 그 메신저의 기록과 미리보기에 문서가 남고,
브라우저 기록에도 남는다.
접근 제어는 링크를 누구에게 주느냐뿐이다.

### 편집하면 새 문서가 된다

편집하면 주소가 바뀌어 새 링크가 새 문서가 된다.[^llms-full]
버전 충돌이 없다는 장점이 있지만,
여러 사람이 같은 문서를 함께 고치는 협업은 성립하지 않는다.
누가 가진 링크가 최신인지 정하는 일은 사람에게 남는다.
HN의 datas도 실시간 협업을 제안했다가,
데이터가 URL에 담긴다는 것을 알고 생각보다 거리가 멀다고 고쳐 말했다.[^datas]

### 크기가 문서의 한계를 정한다

URL 길이 한도 때문에 이 도구는 짧은 문서에 맞다.
2,000자 안에 들어가는 계산, 일정, 작은 표나 그림이 대상이고,
긴 보고서는 짧은 링크로 넘어가야 하며 그 순간 서버에 보관된다.
HN의 ninju는 텍스트 문서가 2,000자 안팎에서 막힌다며
“tiny”라는 이름이 큰 제약이라고 짚었고,[^ninju]
eviks는 메가바이트 단위 문서를 링크에 담아 공유하는 것이
어떻게 쉽냐고 물었다.[^eviks]

### 코드를 내려주는 쪽이 문서를 읽을 수 있다

위협 모델 문서가 스스로 적는 한계가 있다.
링크의 `#` 뒤를 읽는 페이지는 사이트가 보내는 코드이므로,
다른 코드를 보내는 호스트(침해당했거나 강요받았거나 단순히 바뀐 경우)는
조각을 어디로든 보낼 수 있다.
문서는 이에 대한 답을 사용자가 직접 확인할 수 있는 것으로 제시한다.
빌드가 재현 가능하고, 사이트가 `/version.json`에 빌드한 커밋을 밝히며,
`npm run verify-deploy`가 그 커밋을 빌드해 모든 파일을 비교한다.
그러나 누군가 그렇게 확인하기 전까지는 운영자를 믿는 구조라고 문서가
인정한다.

### 링크는 사이트가 살아 있는 동안만 문서다

문서가 링크에 있다고 해도 그 링크를 여는 것은 tinylittleoffice.com의 편집기다.
HN의 danhite는 공동 창업자의 소개 글을 인용하며,
팀이 6년 전에도 같은 아이디어로 사이트를 만들었지만
그 사이트들이 웹에서 사라지면서 옛 링크가 모두 깨졌다고 전했다.[^danhite]
출시 직후에는 요금제 한도에 걸려
사이트에 접속할 수 없다는 보고도 있었다.[^christophilus]
maelito는 그래서 이 도구가 다음 달에도 있으리라고
기대해서는 안 된다고 했다.[^maelito]
MIT 소스가 공개되어 있어 직접 호스팅할 수 있지만,[^beklein]
ktzar는 자체 호스팅 경로가 주로 Cloudflare 서비스에 기대고
Docker Compose와 로컬 저장소로 띄우는 문서가 없다고 아쉬워했다.[^ktzar]
이 불만이 나온 뒤의 상태는 다음과 같다.
2026년 11월 10일에 읽은 저장소의 `docs/self-host.md`는 Cloudflare 계정에 올리는
경로 외에
Node나 Docker로 SQLite 파일 하나를 쓰는 단일 프로세스 경로도 설명한다.
저장소에는 `compose.yaml`과 `Dockerfile`도 있다.
또 사이트가 내려가거나 요청 한도에 걸릴 때를 위한 미러가
GitHub Pages(`aboard-io.github.io/tinylittleoffice/`)에 있어,
링크 앞에 이 주소를 붙이면 거기서 열린다.
미러는 사이트와 같은 태그를 다시 빌드한 것이고
(2026년 10월 15일 이슈 13번 이후 추가되었다고 문서가 적는다),
미리보기 카드와 보안 헤더 일부가 없으며,
짧은 링크는 사이트와 같은 단축 서비스에 기대어 그 서비스가 멈추면 함께 멈춘다.
오래 보관할 문서라면
`.tlo`나 Markdown으로 내려받아 두는 편이 링크만 남기는 것보다 안전하다.

## 함정

`llms.txt`가 직접 꼽는, 에이전트가 가장 먼저 어기는 규칙이 있다.[^llms]

- 모든 공백과 줄바꿈이 보존된다.
  목록은 두 칸 들여쓰기로 중첩하므로
  링크에서 공백을 하나라도 빠뜨리면 계층 구조가 사라진다.
  문단 안의 줄바꿈도 그대로 줄바꿈이 되니 문단을 여러 줄로 나눠 쓰면 안 된다.
- 슬라이드 한 장에는 한 가지만 보여 준다.
  차트, 표, 다이어그램이 있는 슬라이드에서는 글머리표가 그려지지 않는다.
- 목록의 쉼표는 항목을 나눈다.
  벤 다이어그램이나 좌석 배치 목록에서 “2,000 cases”는 두 항목이 되므로
  2000으로 써야 한다.

손으로 쓴 링크는 아무것도 검사하지 않으므로,
`npx tinylittleoffice try <app> <file>`로 초안을 검사하는 편이 안전하다.[^llms]

## 기억할 원칙

### 저장소를 없애면 링크가 저장소가 된다

Tiny Little Office는 서버 저장을 없애는 대신 문서를 링크 안에 넣었다.
이 설계에서 링크는 단순한 주소가 아니라 문서 그 자체이자 접근 권한이다.
링크를 공유하는 것이 곧 문서를 복사해 주는 것이므로,
어디에 붙이느냐가 어디에 저장하느냐와 같은 결정이 된다.

---

[^llms]: Tiny Little Office, [llms.txt](https://tinylittleoffice.com/llms.txt), 2026-10-17 확인

[^llms-full]: Tiny Little Office, [llms-full.txt](https://tinylittleoffice.com/llms-full.txt), 2026-10-17 확인

[^ford]: Ftrain, [The Web Is More Than Enough, by Paul Ford (Ftrain)](https://ftrain.com/aboard-the-web-is-more-than-enough), 2026-10-21

[^gh-api]: GitHub API, [aboard-io/tinylittleoffice](https://api.github.com/repos/aboard-io/tinylittleoffice), 2026-10-17 확인

[^simonw]: <https://news.ycombinator.com/item?id=50096438>

[^datas]: <https://news.ycombinator.com/item?id=50096314>

[^ninju]: <https://news.ycombinator.com/item?id=50104564>

[^eviks]: <https://news.ycombinator.com/item?id=50098872>

[^danhite]: <https://news.ycombinator.com/item?id=50099619>

[^christophilus]: <https://news.ycombinator.com/item?id=50102111>

[^maelito]: <https://news.ycombinator.com/item?id=50101934>

[^beklein]: <https://news.ycombinator.com/item?id=50102331>

[^ktzar]: <https://news.ycombinator.com/item?id=50100965>
