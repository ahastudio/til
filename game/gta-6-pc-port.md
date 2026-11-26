# GTA 6 비공식 PC 구동

트윗: [TA ACONTECENDO RAPAZIADAAAA, isso é no computaaadorr!!! repito COMPUTADOR!!](https://twitter.com/raul_bs3/status/2125213756238291075)

HN 토론: <https://news.ycombinator.com/item?id=50627783> (435점, 507개 댓글)

GN 토론: <https://news.hada.io/topic?id=37795>

## 요약

브라질 포르투갈어로 쓴 트윗 묶음이다.
`rust1co`(`@raul_bs3`)가 2026년 11월 24일에 올렸고,
읽은 시점의 조회수는 약 17만 2천이다.
GTA 6가 PC에서, 셰이더(shader)가 거의 다 갖춰진 상태로 돈다는 영상을 올리고
컴퓨터에서 도는 것이라고 거듭 강조한다.

묶음의 다른 글은 다음 다섯 가지다.

- VIctory라는 프로젝트(개발자 marvy)가 다른 개발자들에게도 길을 열었다는 글
- Cyberleek이 무언가를 공개한 지 24시간이 안 되어 이 결과가 나왔다는 글
- 작성자 자신도 충격을 받았다는 말과 함께 24시간이 안 걸렸다는 영상
- Vulkan과 Claude의 마법이라는 짧은 글과,
  Vulkan을 고른 이유로 오류에 더 관대한 그래픽 API여서
  DX12보다 까다롭지 않기 때문이라는 설명
- 다른 계정(`@OnlyWashington_`)의 답글로,
  가장 큰 게임이 인공지능 덕분에 일주일도 안 되어 다시 만들어지고 있다며
  혁명적이라는 평

트윗은 성능 수치, 해상도, 프레임, 구동 환경을 말하지 않고,
이 문서는 영상 속 화면을 확인하지 못했다.
GeekNews의 요약도 운영체제 이름이나 구체적인 환경, 성능 수치가 본문에
없다고 짚는다.

### 배경

HN 스레드에서 Tiberium이 정리한 맥락은 다음과 같다.
Cyberleek이라는 이름으로 GTA 6의 Xbox 빌드가 유출되었고,
처음에는 리소스, 이어서 게임 실행 파일이 나왔다.
현재의 프로젝트(`xcl`과 VIctory)는 Wine과 비슷한 방식으로
Xbox용 실행 파일을 Windows에서 돌리려는 것이다.[^Tiberium]
이 문서는 유출물의 입수 방법이나 위치를 다루지 않는다.

## 분석

### 왜 이렇게 빨리 돌았는가

HN의 Tiberium는 현재 Xbox가 Windows PC와 매우 가까우므로
실행 코드를 돌리는 것 자체가 어렵지 않고, 대부분은 호환성과 그래픽
문제라고 했다.
실행 파일에는 특별한 DRM이나 난독화가 없었다는 것이다.[^Tiberium]
해결해야 할 문제로 꼽은 것은 세 가지다.

첫째는 셰이더 번역이다.
게임이 RDNA 2용 원시 셰이더를 담고 있어서 다른 형식으로 번역하고 다시
컴파일해야 하며, DX12용 DXIL이 예로 나온다.
번역 파이프라인이 나쁘면 셰이더가 부풀고 성능이 떨어진다.

둘째는 메모리 구조다.
Xbox는 통합 메모리를 쓰지만 대부분의 PC는 그렇지 않아서 우회와 관리 코드가
많이 필요하다.

셋째는 Xbox 전용 API와 형식이다.
Xbox의 DirectX 12는 일반 Windows와 다르고,
게임이 Xbox 전용 텍스처 형식과 DirectStorage를 쓴다.

Tiberium는 이것이 흔히 말하는 재컴파일(recomp)이 아니라고 짚었다.
약 100MB의 실제 기계어를 전부 디컴파일하는 일은 실행시키는 것보다 훨씬 큰
일이라는 이유다.[^Tiberium]
게임 그래픽 성능을 다루는 Agentlien도 같은 취지로,
Xbox와 PC 사이에서 90%는 그냥 돌고 나머지 10%가 플랫폼 특유의 세부 사항으로
가득하다고 적었다.[^Agentlien]
vrmiguel은 Xbox용 호환 작업은 재컴파일이 필요 없고 그래픽 API가 Windows
DirectX와
거의 일대일로 대응할 것이므로, 앞서 있었던 Switch 2용 작업보다 일이 적을
것이라고 보았다.[^vrmiguel]

### 트윗이 말하는 Vulkan

트윗은 Vulkan을 쓴다고 하고 DX12보다 오류에 관대하다는 점을 이유로 든다.
Tiberium는 번역 대상의 예로 DX12용 형식을 들었다.
두 설명이 같은 프로젝트를 가리키는지는 이 문서가 확인하지 못했다.
`xcl`과 VIctory가 서로 다른 방식일 수도 있고, 트윗의 설명은 작성자의 해석일
수도 있다.

### 유출이 필요했던 이유

pipes는 왜 Xbox 빌드의 유출이 있어야 가능했는지,
디스크에서 바이너리와 에셋을 뽑으면 되지 않느냐고 물었다.[^pipes]
chocochunks는 요즘 콘솔이 디스크를 암호화하고 키가 필요하다고 답했다.
Switch 2와 PS5는 탈옥으로 키를 얻을 수 있었지만 Xbox Series에는 탈옥이 없고,
이번 유출은 암호화되지 않은 빌드여서 키가 필요 없었다는 설명이다.[^chocochunks]
이 점이 이번 사례가 콘솔 보안의 약점이라기보다 유출에 기댄 것이라는 해석의
근거가 된다.

## 비평

### 트윗은 증거가 아니라 선언이다

트윗은 영상과 환호로 이루어져 있고 구동의 범위를 말하지 않는다.
그래서 일부 반응이 갈렸다.
ozgrakkurt는 실제로는 돌지 않으며 전체가 조악한 결과물이라고 했고,
vrmiguel은 인공지능 물결을 싫어하는 입장이지만 이 프로젝트들로 게임이 도는 것은
사실이라고 답했다.[^ozgrakkurt][^vrmiguel]
RomanKornev는 며칠이면 반복 개선되어 원본 빌드보다 빠르게 돌 것이라고 했는데,
근거는 다수가 자신의 여유 에이전트 사용량을 기여하는 군집이 자율 개선이 가능한
지점을 넘었다는 점이다.[^RomanKornev]
이는 예측이고 확인된 사실이 아니다.
CMay는 이 방식이 PC에서 GTA 6를 돌리는 주된 방법이 될 만큼 장벽이 낮지 않으며,
Xbox Series X를 살 수 있는 사람이면 프레임이 더 잘 나올 것이라고 보았다.[^CMay]

### 인공지능의 역할 서술

트윗과 답글은 Claude와 인공지능 덕분이라고 말하지만
어떤 작업을 모델이 맡았고 사람이 무엇을 했는지는 밝히지 않는다.
HN의 의견도 갈렸다.
vrmiguel은 대형 언어 모델이 이런 이식 작업에 놀랍도록 능하다고
보았고,[^vrmiguel]
Tiberium는 문제를 풀려면 좋은 번역 파이프라인과 호환성 작업이 필요하다고
설명했다.[^Tiberium]
이 문서는 이 프로젝트에서 모델이 하는 일의 크기를 확인할 수단이 없다.

### 법적 쟁점은 이 글 밖에 있다

d--b는 불법으로 얻은 코드를 이식하는 것이 얼마나 합법인지 물었다.[^d--b]
origini는 독일에서는 해킹 도구가 별도 조항의 대상이 될 수 있고,
합법적으로 가진 게임을 PC에서 돌도록 바꾸는 것은 다르게 볼 여지가 있다고 보았다.
이 논의는 정식으로 산 사본을 전제로 한 것으로 읽힌다.[^origini]
이 문서는 법적 판단을 하지 않는다.
다만 이 문서가 다루는 대상은 유출된 빌드를 돌리려는 비공식 작업이며,
공식 PC판이나 정식으로 산 사본을 위한 이식이 아니다.

## 인사이트

### 배포 구조를 향한 반응

HN 반응의 상당수는 기술보다 배포 구조를 향한다.
FLeXMurphy는 이런 일이 막대한 비용을 쓴 스튜디오에 좋지 않다고
보았고,[^FLeXMurphy]
micromacrofoot는 AI가 디컴파일하지 못하게 소스를 잠그려면 게임 스트리밍이 유일한
길이 될 것이라고 했다.[^micromacrofoot]
반론도 있다.
coldstreamflowi는 게임 스트리밍이 20년 동안 시장의 극히 일부에 머물렀고
기술적 한계로 경험이 나빠진다고 보았고,[^coldstreamflowi]
wpm은 지연 시간을 낮게 유지하기 전까지 사람들이 따라오지 않을 것이라고
했다.[^wpm]

### 구매자의 관점

ivraatiems는 이것이 치명적이라고 보지 않는다며 PC판이 나오면 사겠다고
했고,[^ivraatiems]
jmyeet는 이 이식이 Rockstar에 PC판 출시를 앞당기라는 압력이 될 것이라고 보았다.
jmyeet가 든 2027년 1분기 출시 소문은 확인되지 않았다고 본인이 적는다.[^jmyeet]
이 소문은 이 문서도 확인하지 못했다.

### 확인할 것

영상의 구동이 얼마나 지속되고 어떤 성능인지,
프로젝트들이 공개된 형태로 유지되는지,
Rockstar가 공식 PC판 일정을 바꾸는지를 확인해야 한다.

---

[^Tiberium]: <https://news.ycombinator.com/item?id=50629877>

[^Agentlien]: <https://news.ycombinator.com/item?id=50630800>

[^vrmiguel]: <https://news.ycombinator.com/item?id=50634760>

[^pipes]: <https://news.ycombinator.com/item?id=50633428>

[^chocochunks]: <https://news.ycombinator.com/item?id=50633561>

[^ozgrakkurt]: <https://news.ycombinator.com/item?id=50634495>

[^RomanKornev]: <https://news.ycombinator.com/item?id=50635062>

[^CMay]: <https://news.ycombinator.com/item?id=50630201>

[^d--b]: <https://news.ycombinator.com/item?id=50629470>

[^origini]: <https://news.ycombinator.com/item?id=50629602>

[^FLeXMurphy]: <https://news.ycombinator.com/item?id=50629284>

[^micromacrofoot]: <https://news.ycombinator.com/item?id=50629333>

[^coldstreamflowi]: <https://news.ycombinator.com/item?id=50634032>

[^wpm]: <https://news.ycombinator.com/item?id=50633500>

[^ivraatiems]: <https://news.ycombinator.com/item?id=50634934>

[^jmyeet]: <https://news.ycombinator.com/item?id=50635454>
