# Nintendo가 GitHub에 DMCA 통지 네 건을 보내 Switch 에뮬레이터 둘과 모드칩 펌웨어 저장소 144개를 내렸고, IGN은 이를 AI 시대의 에뮬레이션 단속으로 읽는다

원문: [Nintendo Takes Down Switch Emulators and Mod Chip Firmware in Massive GitHub DMCA Sweep](https://www.ign.com/articles/nintendo-takes-down-switch-emulators-and-mod-chip-firmware-in-massive-github-dmca-sweep)

HN 토론: <https://news.ycombinator.com/item?id=50469994> (322점, 261개 댓글)

GN 토론: <https://news.hada.io/topic?id=37072>

## 요약

IGN의 Jacqueline Thomas 기자가 쓴 이 기사는 Nintendo가 GitHub에 DMCA 삭제 통지 네 건을 보냈다고 전한다.
대상은 Switch 에뮬레이터 두 개(Yuzu와 Citron Neo)와 모드칩 펌웨어이다.
이 펌웨어는 저장소 144개로 퍼져 있었고 모두 GitHub가 내리고 삭제 통지문으로 바꿨다.
Picofly 같은 모드칩은 Switch 본체 기판에 납땜해 이 펌웨어를 올리면 Nintendo의 복제 방지를 우회한다고 기사는 설명한다.

기사가 인용한 11월 6일자 통지는, Switch 본체와 게임이 정당한 게임 파일하고만 상호작용하게 하는 기술적 보호 조치(TPM)를 담고 있고, 이 조치가 불법 복제본 실행과 무단 기기에서의 불법 복제를 막는다고 적는다.
TorrentFreak를 인용해, 이 펌웨어가 사이트의 다른 곳에는 여전히 올라와 있는 듯하다고도 전한다.
기사는 2024년에 Nintendo가 Yuzu 미러 12곳을 겨냥한 통지로 사본 8,500개를 내렸던 일을 상기시킨다.

기사는 시점을 두 가지 맥락과 묶는다.
며칠 전 에뮬레이터가 PC에서 The Legend of Zelda: Ocarina of Time 리메이크를 돌렸다는 것이고, 그래서 Nintendo가 에뮬레이션 단속을 다시 시작하는 신호일 수 있다고 한다.
또 2026년의 에뮬레이션은 AI 때문에 2024년과 다르다고 쓴다. AI로 만든 게임 혼합 모드가 한동안 Twitter를 채웠고, Anthropic은 Claude가 게임을 그대로 베끼지 못하도록 막는 장치를 넣었으며, Rockstar가 GTA 5 브라우저 판을, Bethesda가 AI로 만든 Fallout New York 게임을 내렸다고 한다.
기사는 이 연결이 기자의 해석이고 Nintendo가 그렇게 밝힌 것은 아니다.

## 분석

### 이번 통지의 새로운 초점은 에뮬레이터보다 우회 도구이다

기사는 이번 초점이 모드칩 펌웨어라는 점을 짚는다.
에뮬레이터와 펌웨어는 법적 성격이 다르다.
HN의 한 댓글은 에뮬레이션 자체는 내부 문서나 내부 소프트웨어, 부정한 수단으로 얻은 정보를 쓰지 않는 한 거의 어디서나 합법이라고 했고, 답글은 배포는 합법이 아닌 경우가 많다고 덧붙였다.[^dormento][^flanz_10]
한 사용자는 자기가 가진 게임을 자기 기기에서 추출한 펌웨어로 에뮬레이터에서 돌리면 어떤 법을 어기느냐고 물었다.
답글은 DMCA 1201조가 두 부분으로 되어 있어, 하나는 보호 조치를 깨는 행위를 금지하고 다른 하나는 우회를 위한 기기와 소프트웨어를 유통하는 행위를 금지한다고 설명했다.[^glimshe][^ndiddy]
이 문서는 이 법률 해석을 직접 확인하지 못했고, 댓글의 설명으로만 소개한다.

### 삭제 통지의 효과는 법원 판결 없이도 생긴다

한 댓글은 Nintendo가 소송에서 이기지 못한다고 단언했고, 답글은 정식 재판 없이 억누르고 싶은 것을 억눌렀다면 이긴 것이라고 맞받았다.[^eur0pa][^mrmorden]
호스팅 쪽에서 보면 이번 삭제의 실제 효과는 GitHub에서 저장소가 사라지는 것이고, 코드가 세상에서 없어지는 것은 아니다.
스레드에서 한 사용자는 Switch 2 에뮬레이터가 아직 GitHub와 GitLab에 있고, Switch 1 에뮬레이터 대부분도 자체 도메인의 저장소에 있어서 지금도 구할 수 있다고 했다.[^haunter]
기사도 펌웨어가 다른 곳에서 호스팅되는 듯하다고 전한다.

## 비평

### 기사는 AI와의 연결을 근거 없이 단정한다

기사의 마지막 부분은 AI 때문에 에뮬레이션이 달라졌다고 쓰지만, 이번 통지가 AI와 관련 있다는 근거는 Nintendo의 통지문에 없다.
통지문은 TPM과 불법 복제 방지를 말할 뿐이다.
스레드에서는 이 연결이 다른 방향으로 확장되었다.
한 댓글은 NDA로 묶인 SDK는 문서와 예제가 풍부해서, 충분한 토큰을 주면 AI가 이를 에뮬레이터로 바꿀 수 있고, 새 에뮬레이터가 금지된 정보 없이 만들어졌음을 누가 판별하느냐고 물었다.[^mattbee]
이것은 가능성에 대한 추정이고, 기사와 스레드 어디에도 실제 사례가 확인되지 않았다.
다른 댓글은 재컴파일 프로젝트는 아무것도 재배포하지 않으니 어떻게 막을 수 있겠느냐고 물었고,[^christkv]
이에 대한 답은 무서워서 물러서는 쪽 외에는 막을 방법이 없다는 것이었다.[^majorchord]
이 문서는 재컴파일 프로젝트의 법적 지위를 확인하지 못했다.

### 보존과 신작 즉시 실행이 같은 도구에서 섞인다

한 사용자는 게임 보존은 인류에 주는 선물이지만 Ocarina of Time을 출시 이틀 만에 공짜로 하는 것은 문제라고 물었다.[^sergiotapia]
답글은 그런 사람 대부분은 원래 사지 않을 사람이고 Switch 2가 없는 경우도 많아 잃어버린 매출이 아니라고 반박했고,[^haunter2]
다른 답글은 Nintendo만큼 큰 기업에 미안함을 느끼지 않는다고 했다.[^ohentis]
ROM 해킹 계의 한 참여자는 최신 에뮬레이터가 보존 운동에 해를 끼친다고 했다. 출시 한 달도 안 된 리메이크를 PC에서 돌리게 하는 것과 보존을 구분하지 않으면 정당한 프로젝트가 같이 공격받는다는 것이다.[^andrewclunn]
답글은 Nintendo가 가장 소송을 많이 거는 저작권 독점 기업이라는 이유로 그 입장을 이해하면서도 동의하지 않았다.[^matheusmoreira]
기사는 이 구분을 다루지 않는다.

### 저작권의 근거를 묻는 댓글은 오해를 일으킬 수 있다

한 댓글은 통지문이 “저작권으로 보호되는 게임”이라고 하는데 Nintendo가 LLM으로 게임을 만드느냐고 물었고 LLM 출력은 저작권이 없는 것으로 안다고 했다.[^softtalker]
답글은 저작권에는 최소한의 인간 창작성이 필요하고, Nintendo의 게임은 사람이 디자인하고 그렸으니 해당된다고 반박했으며 단순화가 지나치다고 했다.[^kube-system]
다른 답글은 Switch가 2017년에 나왔으니 그 주장이 설령 맞아도 관련이 없다고 했다.[^zamadatix]

## 인사이트

### 호스팅 위치는 법적 위험과 별개의 선택이다

스레드의 실무적 반응은 호스팅에 모였다.
한 사용자는 Nintendo 에뮬레이터를 GitHub에 올리는 것을 언제 그만두겠느냐고 했고, 답글은 주목을 받고 나서 다른 곳으로 옮기면 되니 잃은 것이 없다고 했다.[^lloydatkinson][^micromacrofoot]
또 다른 답글은 사람들이 이미 아는 무료 플랫폼에서 몇 달의 호스팅을 얻는다는 계산을 한다고 했다.[^zamadatix2]
대안으로는 GitHub 말고 자체 호스팅이나 분산 저장소(Radicle 같은)가 거론되었지만, 한 사용자는 Radicle이 암호화폐 요소와 보안 허점 때문에 진지하지 않다고 반박했다.[^skeledrew][^this_user]
이것은 이 문서가 평가하지 못한 프로젝트들이다.

### 소비자 반응은 불매 쪽으로 기운다

스레드에는 Nintendo를 더는 사지 않겠다는 댓글이 여럿 있었다. Bowser를 상대한 일을 이유로 든 사람과, Yuzu 삭제 뒤 영구 불매를 결정한 사람이 있었다.[^lilbigdoot][^cadamsdotcom]
한 답글은 불매는 아주 큰 규모가 아니면 작동하지 않고 혼자 하면 자신만 손해라고 했다.[^cowlevel]
이는 댓글 작성자들의 자기 보고이고 실제 매출 영향의 증거가 아니다.

### 확인할 관찰

이 사안의 방향을 가를 관찰은 세 가지이다.
펌웨어가 GitHub의 다른 곳에 남아 있다는 보도가 이어서 삭제로 이어지는지,
Nintendo가 Ocarina of Time 리메이크를 돌린 에뮬레이터 쪽으로 통지를 확대하는지,
AI로 만든 재컴파일 프로젝트에 대한 첫 법적 대응이 나오는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^dormento]: <https://news.ycombinator.com/item?id=50472709>

[^flanz_10]: <https://news.ycombinator.com/item?id=50472721>

[^mattbee]: <https://news.ycombinator.com/item?id=50475116>

[^glimshe]: <https://news.ycombinator.com/item?id=50470352>

[^ndiddy]: <https://news.ycombinator.com/item?id=50470491>

[^eur0pa]: <https://news.ycombinator.com/item?id=50472040>

[^mrmorden]: <https://news.ycombinator.com/item?id=50472229>

[^haunter]: <https://news.ycombinator.com/item?id=50470629>

[^christkv]: <https://news.ycombinator.com/item?id=50474291>

[^majorchord]: <https://news.ycombinator.com/item?id=50474470>

[^sergiotapia]: <https://news.ycombinator.com/item?id=50470987>

[^haunter2]: <https://news.ycombinator.com/item?id=50471063>

[^ohentis]: <https://news.ycombinator.com/item?id=50475268>

[^andrewclunn]: <https://news.ycombinator.com/item?id=50471891>

[^matheusmoreira]: <https://news.ycombinator.com/item?id=50472173>

[^softtalker]: <https://news.ycombinator.com/item?id=50471127>

[^kube-system]: <https://news.ycombinator.com/item?id=50472079>

[^zamadatix]: <https://news.ycombinator.com/item?id=50471504>

[^lloydatkinson]: <https://news.ycombinator.com/item?id=50471262>

[^micromacrofoot]: <https://news.ycombinator.com/item?id=50471471>

[^zamadatix2]: <https://news.ycombinator.com/item?id=50471622>

[^skeledrew]: <https://news.ycombinator.com/item?id=50471042>

[^this_user]: <https://news.ycombinator.com/item?id=50472967>

[^lilbigdoot]: <https://news.ycombinator.com/item?id=50472211>

[^cadamsdotcom]: <https://news.ycombinator.com/item?id=50472508>

[^cowlevel]: <https://news.ycombinator.com/item?id=50475193>
