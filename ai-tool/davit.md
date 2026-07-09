# Davit: Apple Containers를 위한 네이티브 macOS UI

<https://davit.app/>

HN 토론: <https://news.ycombinator.com/item?id=48821848>

## 소개

Davit는 Apple의 컨테이너 플랫폼을 위한 무료 오픈소스 macOS
애플리케이션으로, Docker Desktop 없이도 Apple 실리콘 Mac에서
Linux 컨테이너를 네이티브 그래픽 인터페이스로 관리할 수 있게
해준다.

컨테이너 시작·중지·재시작·삭제와 실시간 CPU·메모리·IP 모니터링을
지원하며, 실행 중인 컨테이너에 터미널이나 iTerm으로 바로 인터랙티브
셸을 열 수 있다. 컨테이너 파일시스템을 탐색하고 파일을 업로드·
다운로드·삭제할 수 있는 파일 관리 기능도 있다. Docker Compose
파일을 가져와 전체 스택을 실행하기 전에 미리 볼 수 있고, Apple의
BuildKit을 이용해 Dockerfile로 이미지를 빌드할 수 있다. Docker
Hub, ghcr.io, quay.io 및 커스텀 OCI 레지스트리 로그인도
지원한다.

아키텍처 면에서 Davit는 Apple의 컨테이너 데몬과 XPC 프로토콜로
직접 통신하며, 이는 CLI가 사용하는 것과 동일한 경로다. 별도의
백그라운드 서비스나 Electron 프레임워크 없이 SwiftUI만으로
작성됐고, 앱 번들 용량은 17MB, 유휴 상태의 플랫폼 서비스는 약
25MB에 불과하다. macOS 15 이상, Apple 실리콘이 요구 사항이며,
`brew install wouterdebie/tap/davit`로 설치하고 필요 시 플랫폼도
자동으로 설치된다. 관리자 권한은 필요 없다.

라이선스는 MIT이며, Wouter de Bie가 개발했다. Apple의 디지털
서명과 공증을 받았고 소스는 GitHub에 공개되어 있다. Docker
Desktop이 항상 켜져 있는 하나의 큰 VM을 운영하는 방식이나,
Docker CLI 호환성을 앞세운 상용 도구 OrbStack과 달리, Davit는
컨테이너마다 가벼운 개별 VM을 띄워 더 강한 격리를 유지하면서도
유휴 시에는 백그라운드 리소스를 전혀 쓰지 않는다.

## 분석

### Apple 네이티브 컨테이너 인프라가 서드파티 UI 생태계를 열었다

Apple이 자체 컨테이너 런타임을 macOS에 내장하면서, Docker
Desktop이 독점하던 "컨테이너 관리 UI" 영역에 서드파티가 진입할
여지가 생겼다. Davit는 Apple의 XPC 프로토콜을 CLI와 동일하게
직접 사용함으로써, 중간 계층 없이 얇고 반응성 높은 네이티브 앱을
구현했다. 이는 플랫폼 제공자가 저수준 API를 공개하면 그 위에
다양한 사용자 경험이 빠르게 생겨나는 전형적인 패턴이다.

## 비평

### OrbStack과의 실질적 차별점이 사용자 경험으로 검증되지 않았다

컨테이너별 개별 VM으로 더 강한 격리를 얻는다는 주장은 이론적으로는
타당하지만, 이것이 실제 개발 워크플로에서 체감할 만한 이점인지,
아니면 오버헤드로 이어지는지는 벤치마크 없이는 판단하기 어렵다.
격리 수준과 성능은 종종 트레이드오프 관계에 있으므로, 개별 VM
방식이 이미지 빌드나 컨테이너 시작 속도에 미치는 영향을 구체적으로
비교한 자료가 필요하다.
HN에서도 같은 의문이 반복적으로 제기됐다.
oulipo2는 OrbStack과 비교했을 때 어떤 차이가 있는지 직접
질문했고, 이에 대한 후속 논의에서 OrbStack은 커스텀 가상화로
모든 컨테이너를 하나의 VM에서 돌리는 반면 이 앱은 컨테이너마다
매우 얇은 VM을 개별로 띄운다는 구조적 차이가 확인됐다[^oulipo2].
reassess_blind는 Apple Containers가 이미 빠른 OrbStack 대비
체감할 만한 개발 경험 개선을 주는지 의문을 제기했고[^reassess_blind],
dllrr 역시 Docker나 OrbStack 대신 Apple Containers를 선택해야
하는 이유를 요약해 달라고 요청했다[^dllrr]. 이런 반응들은 격리
수준의 이론적 우위가 실제 채택 결정에서는 충분한 설득력을 갖지
못하고 있음을 보여준다.

## 인사이트

### AI 코딩 도구가 소규모 오픈소스 유틸리티의 개발 속도를 끌어올리고 있다

HN 댓글에서는 Davit와 유사한 Swift 기반 컨테이너 UI가 여러 개
동시에 등장하고 있다는 관찰이 나왔다.[^davit-hn] 이는 AI 코딩
도구의 보급으로 한 명의 개발자가 짧은 기간에 네이티브 macOS
앱을 완성도 있게 만들어낼 수 있게 되면서, 플랫폼 API가 공개되면
그 위의 도구 생태계가 훨씬 빠른 속도로 다양화되는 흐름을 보여준다.
Docker Desktop 대체재를 둘러싼 경쟁이 이런 가속화된 개발 주기
안에서 벌어지고 있다는 점이 특히 흥미롭다.
joohwan은 contained-app, iContainer, dory, berth, ContainerUtility,
orchard 등 동일한 아이디어를 구현한 여러 프로젝트를 나열하며,
"이제는 누구나 같은 아이디어의 버전을 그 어느 때보다 빠르게
만들 수 있다"고 짚었고, 이런 흐름이 "초개인화된 소프트웨어
(hyper-personal software)" 시대로 이어질 것이라 내다봤다[^joohwan].
xinit은 이 저장소가 3일 만에 28개의 커밋과 5,015줄의 Swift
코드로 만들어졌고, 모든 커밋이 "Co-Authored-By: Claude Fable 5"로
표시되어 있다는 점을 지적하며 AI 도구가 가져온 개발 속도의 변화를
구체적으로 보여줬다[^xinit]. internet2000은 여기서 한 걸음 더
나아가, Claude가 기여자로 표시된 것 자체가 "네이티브한 느낌에
Electron이 없는 좋은 앱일 것"이라는 품질 신호로 읽히기도 한다고
언급했다[^internet2000].

---

[^davit-hn]: <https://news.ycombinator.com/item?id=48821848>
[^oulipo2]: <https://news.ycombinator.com/item?id=48823110>
[^reassess_blind]: <https://news.ycombinator.com/item?id=48827856>
[^dllrr]: <https://news.ycombinator.com/item?id=48825567>
[^joohwan]: <https://news.ycombinator.com/item?id=48831617>
[^xinit]: <https://news.ycombinator.com/item?id=48823028>
[^internet2000]: <https://news.ycombinator.com/item?id=48824366>
