# 닌텐도의 GitHub DMCA 삭제 요청

원문: [Nintendo Takes Down Switch Emulators and Mod Chip Firmware in Massive GitHub DMCA Sweep](https://www.ign.com/articles/nintendo-takes-down-switch-emulators-and-mod-chip-firmware-in-massive-github-dmca-sweep)

HN 토론: <https://news.ycombinator.com/item?id=50469994> (327점, 262개 댓글)

GN 토론: <https://news.hada.io/topic?id=37072>

## 요약

IGN의 수석 기술 편집자 Jacqueline Thomas가 쓴 기사이다(2026년 11월 12일 갱신 표시). 기사 제목은 「Nintendo Takes Down Switch Mod Chip Firmware in GitHub DMCA Sweep」으로도 표시된다.
닌텐도가 GitHub에 DMCA 삭제 요청을 네 건 보냈고 대상은 Switch 에뮬레이터 두 개(Yuzu와 Citron Neo)와 모드칩 펌웨어이다. 기사는 이번 초점이 모드칩 펌웨어에 있는 듯하다고 하며, 그 펌웨어의 저장소 144개가 모두 GitHub에서 제거되어 DMCA 안내문으로 바뀌었다고 쓴다. Picofly 같은 모드칩은 Switch 메인보드에 납땜하고 이 펌웨어를 올려 닌텐도의 복제 방지를 우회한다.

기사의 나머지 내용은 다음과 같다.

- GitHub가 공개한 11월 6일자 닌텐도의 통지는 Switch 본체와 게임에 기술적 보호 조치(TPM)가 있어 정품 닌텐도 게임 파일만 동작하게 하고 불법 복제본의 실행과 무허가 기기에서의 복제를 막는다고 주장한다.
- 이번 삭제는 모드칩 펌웨어 저장소를 크게 지웠지만, TorrentFreak에 따르면 같은 사이트의 다른 곳에 여전히 올라와 있다. 닌텐도가 끝내지 않았을 수 있다고 기사는 덧붙인다. 2024년에는 Yuzu 사본 8,500개를 미러 12곳을 겨냥한 요청으로 내렸다.
- 며칠 전 에뮬레이터가 「젤다의 전설: 시간의 오카리나」 리메이크를 PC에서 돌렸고 이것이 닌텐도가 에뮬레이션을 다시 단속할 신호일 수 있다고 본다.
- 2026년의 에뮬레이션은 AI 때문에 2024년과 다르다고 한다. AI가 만든 혼합 모드가 한동안 소셜 미디어를 휩쓸었고 Anthropic이 Claude가 게임을 그대로 복제하지 못하도록 잠금을 넣었다고 쓴다. 게임 개발사도 AI 이식에 대응해, 지난달 Rockstar가 GTA 5의 브라우저 판을, Bethesda가 AI가 만든 「Fallout New York」 게임을 내렸다고 한다.

기사 끝에는 AI 모드와 디컴파일에 대한 독자 투표가 붙어 있다.

## 분석

### 기사는 소식 요약이고 법적 근거는 통지문에 있다

IGN 기사는 짧은 속보이며 법적 근거는 GitHub가 공개한 통지문에 있다. 통지문은 대표 저장소로 `Ansem-SoD/Picofly`를 들고 저장소 전체가 침해라고 주장하며, 닌텐도의 저작권 등록 네 건(마리오 카트 8 디럭스, 동물의 숲 뉴 호라이즌, 슈퍼 스매시 브라더스 얼티밋, 젤다의 전설 브레스 오브 더 와일드)을 든다.[^dmca]
통지문은 SX Core, SX Lite, Picofly, HWFLY를 포함한 모드칩 펌웨어가 부팅 순서를 우회해 TPM을 회피한다고 주장하고, 미국 저작권법 1201(a)(1)과 (2)항의 접근 통제 우회와 거래 금지 조항을 근거로 든다. 통지는 부모와 포크를 합해 저장소 네트워크 144개 전체에 적용되었고 포크 대부분이 같은 정도로 침해라고 주장했다. GitHub는 차단 전에 소유자에게 이의 제기 절차를 안내했다.
이는 통지문의 서술을 이 문서가 정리한 것이며 법적 판단이 아니다.

### 에뮬레이터와 모드칩 펌웨어를 구분해야 한다

기사 제목은 에뮬레이터와 펌웨어를 함께 말하지만 이번 삭제의 중심은 펌웨어이고, 통지문의 대표 대상도 Picofly 저장소이다.
HN에서 한 사용자는 내부 문서, 내부 소프트웨어와 펌웨어 구성 요소, 부정한 수단으로 얻은 정보를 쓰지 않는 한 에뮬레이션 자체는 대부분의 나라에서 합법이라고 썼다.[^dormento]
다른 사용자는 DMCA 1201조가 DRM을 깨는 행위와 우회 장치나 소프트웨어를 거래하는 행위를 나눠 금지하며 전자에는 예외가 많다고 설명했다.[^ndiddy]

### 호스팅 위치를 둘러싼 반응이 많다

HN 댓글의 다수는 GitHub에 둔 프로젝트의 운명이 반복된다는 것이다. 한 사용자는 Switch 2 에뮬레이터가 아직 GitHub와 GitLab에 있고 Switch 1 에뮬레이터 대부분도 자체 호스팅 저장소에 남아 있다고 했고,[^haunter] 다른 사용자는 GitHub에 두는 것이 이런 프로젝트에 나쁜 방식인데 왜 관례인지 모르겠다고 했다.[^whynothugo]
Radicle 같은 분산 호스팅을 권하는 댓글에는 보안 허점과 암호화폐 측면이 의심스럽다는 반박이 이어졌다.[^skeledrew][^this-user]

## 비평

### 기사가 한쪽 사실만 짧게 전한다

기사에는 닌텐도나 GitHub의 입장 취재가 없고 개발자 쪽 반응도 없다.
통지문 인용과 TorrentFreak 보도, 과거 사례 요약이 대부분이다.
IGN 기사 아래의 AI 모드에 대한 투표는 기사 본문과 별개의 상호작용이다.

### AI 이야기가 주제와 느슨하게 이어진다

기사 후반의 AI 모드, Claude 잠금, GTA 5 브라우저 판, Fallout 사례는 삭제 건과 직접 관계가 없는 배경이다. 이 연결이 인과인지 시기가 겹친 것인지 기사는 구분하지 않는다.
HN에서 한 사용자는 AI가 게임을 영상만으로 재현할 수 있다는 주장에 사례가 있느냐고 되물었다.[^mjr00]

### 법적 쟁점의 일반 독자 안내가 부족하다

사용자가 정품을 가지고 백업이나 에뮬레이션을 하는 경우가 어떻게 되는지 기사는 설명하지 않는다. HN에서 한 사용자가 이를 묻자 앞서 본 설명이 달렸다.[^glimshe]
재컴파일 프로젝트는 배포물이 없어 막기 어렵다는 지적도 있었는데 이 역시 기사 밖의 논의이다.[^christkv]

### 소비자 반응이 감정적이다

불매를 선언하는 댓글이 많았고[^cadamsdotcom] 게임 보존을 하는 사람이 최첨단 에뮬레이터가 오히려 해가 된다고 본 반대 입장도 있었다.[^andrewclunn]
한 사용자는 게임 산업을 보호해야 양질의 게임이 나온다는 입장에서 닌텐도의 조치를 옹호했다.[^junh0601]
이 반응들은 개인 의견이며 설문이 아니다.

### 외부 반응

HN 글 제목은 「Nintendo Takes Down Emulators and Firmware in Massive GitHub DMCA Sweep」이다.
Lobste.rs에서는 `picofly` 검색 결과가 0건이었다.
GeekNews 토픽은 GN⁺의 요약이고 이용자 댓글은 위의 한 건이다.

## 인사이트

### 가져갈 것은 DMCA 삭제 요청을 읽는 순서이다

속보 기사에서 한 걸음 더 나아가 GitHub의 `github/dmca` 저장소에 올라오는 통지문을 직접 보면 무엇이 대상이고 어떤 조항을 근거로 하는지 알 수 있다.[^dmca] 이는 이 문서의 적용이다.

### 한 플랫폼에 놓지 않는 설계를 점검한다

반복되는 삭제를 보며 사용자들이 말한 대로, 프로젝트의 저장소를 한 곳에만 두면 삭제에 취약하다. 오픈소스 프로젝트는 대체 호스팅과 포크의 위치를 미리 정해 둔다.

### 확인할 관찰

이 사안을 가를 관찰은 세 가지이다.
다른 호스트로 옮겨 간 프로젝트에 대한 추가 조치,
이의 제기(카운터 노티스)의 제출과 결과,
AI 재컴파일 프로젝트에 대한 법적 대응이다.

---

[^dmca]: [Nintendo of America DMCA notice, 2026-11-06 | github/dmca](https://github.com/github/dmca/blob/master/2026/11/2026-11-06-nintendo-2.md)

[^dormento]: <https://news.ycombinator.com/item?id=50472709>

[^ndiddy]: <https://news.ycombinator.com/item?id=50470491>

[^haunter]: <https://news.ycombinator.com/item?id=50470629>

[^whynothugo]: <https://news.ycombinator.com/item?id=50477612>

[^skeledrew]: <https://news.ycombinator.com/item?id=50471042>

[^this-user]: <https://news.ycombinator.com/item?id=50472967>

[^mjr00]: <https://news.ycombinator.com/item?id=50470974>

[^glimshe]: <https://news.ycombinator.com/item?id=50470352>

[^christkv]: <https://news.ycombinator.com/item?id=50474291>

[^cadamsdotcom]: <https://news.ycombinator.com/item?id=50472508>

[^andrewclunn]: <https://news.ycombinator.com/item?id=50471891>

[^junh0601]: <https://news.hada.io/topic?id=37072#cid69771>
