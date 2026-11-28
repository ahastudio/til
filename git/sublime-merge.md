# Sublime Merge: Git 클라이언트

<https://www.sublimemerge.com/>

HN 토론: <https://news.ycombinator.com/item?id=40862144> (88점, 93개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/gmxeyq/sublime_merge_git_client_from_makers> (27점, 14개 댓글)

## 소개

Sublime Merge는 Sublime Text를 만든 Sublime HQ Pty Ltd(시드니)의 Git 클라이언트이다.
홈페이지는 Git 클라이언트를 Sublime답게 만들었다고 소개한다.
직접 설치해 써 보지 않았고 문서와 가격 페이지는 열지 않았다.
설명은 모두 회사의 주장이다.

홈페이지와 내려받기 페이지가 소개하는 내용은 다음과 같다.

- 슬로건: 줄 단위 스테이징, 커밋 편집, 비교할 수 없는 성능이다.
- 구성 요소: 홈페이지는 크로스 플랫폼 자체 GUI 툴킷, 구문 강조 엔진, 자체 Git 읽기 라이브러리를 빠름의 이유로 든다.
- 커밋: 파일, 헝크, 줄 단위 스테이징을 기다림 없이 한다.
- 검토: 나란히 보는 diff, 구문 강조, 글자 단위 diff, 끌어서 조정하는 헝크 문맥 줄이다.
- 검색: 커밋 메시지, 작성자, 경로, 내용으로 저장소 전체를 즉시 검색한다.
- 충돌 해결: 병합 도구가 내장되어 있다.
- 그 밖에: 명령 팔레트, 커밋 편집, blame과 파일 이력, 서브모듈 관리, 명령줄 연동, Git Flow 연동이다. 40개가 넘는 언어의 구문 강조를 기본 제공한다. 실제 Git 명령을 그대로 보여 준다고 적는다.
- 플랫폼: Windows(포터블 포함), Mac, Linux(저장소, deb, rpm, pkg.tar.xz, tar.xz, ARM64 deb와 tar.xz)이며 64비트만 지원한다.
- 라이선스: 평가용으로 무료로 내려받을 수 있으나 계속 쓰려면 라이선스를 사야 한다. 현재는 평가 기간이 강제되지 않는다고 적는다. 읽은 두 페이지에 가격은 없다.

내려받기 페이지의 최신 빌드는 2136(2026년 11월 9일)이다.
이 빌드는 diff 성능을 개선하고 원격 브랜치를 묻는 푸시 프롬프트를 넣었으며 Windows와 Mac에 포함된 Git을 2.56.0으로 올렸다.
앞선 빌드에는 Git reftables 지원, 워크트리 관리(2130, 2026년 9월 14일), LFS 잠금(2125, 2026년 4월 14일), SHA-256 저장소 지원과 저장소 로딩 속도 개선(2121, 2025년 12월 18일)이 있다.

## 분석

### 중심 주장은 Sublime Text의 방식을 Git에 옮긴 빠른 도구라는 것이다

홈페이지는 텍스트 편집기와 같은 제작사가 같은 방식(명령 팔레트, 빠른 반응)으로 Git 클라이언트를 만들었다고 말한다.
HN의 사용자들도 이 키보드 중심 방식과 CLI와의 근접함을 강점으로 꼽았다.[^tehnub]
이는 홈페이지의 서술과 사용자 후기를 이 문서가 정리한 것이다.

### 병합과 커밋 구성에 강점이 있다는 평가가 반복된다

HN에서 한 사용자는 3자 병합에서 이보다 나은 것을 본 적이 없다고 했고,[^pilif] 다른 사용자는 서로 다른 파일의 헝크를 한 커밋으로 묶는 데 매우 좋지만 이력 개요와 blame은 약하다고 했다.[^wodenokoto]
한 사용자는 이 도구가 새 Git GUI라기보다 잘 설계된 GUI로 보는 CLI라고 평했다.[^apocalyptic0n3]
2018년 Lobste.rs에서도 한 사용자가 버튼에 마우스를 올리면 실제 Git 명령이 보여 숨기지 않는다는 점을 좋게 평했다.[^ac]

### 속도 주장은 대형 저장소의 Git 연산 예측으로 설명된다

HN에서 홈페이지의 기다림 없는 스테이징이 무엇에 대한 비교냐는 질문에, 답한 사용자는 큰 파일과 큰 저장소와 느린 플랫폼에서 `git add`가 느릴 수 있다고 하며 Sublime Merge가 결과를 예측한다고 설명했다.[^ben-schaaf]

## 비평

### 가격이 부담이라는 반응이 있다

HN에서 한 사용자는 쓰고 있지만 100달러가 무료 대안이 많은 상황에서 정당화하기 어려워 구입하지 못했다고 했다.[^have-faith]
평가판이 사실상 무기한이라는 점은 홈페이지가 직접 적는다.

### 비교와 차별점이 제시되지 않는다

HN에서 한 사용자는 Fork 같은 독립 도구와 VS Code의 Git 기능에 대한 비교 페이지가 있으면 좋겠다고 했다.[^sam-goody]
다른 사용자는 VS Code의 내장 Git과 터미널로 충분한데 왜 따로 GUI를 쓰는지 묻기도 했다.[^thiht]
홈페이지는 다른 클라이언트와의 비교를 싣지 않는다.

### 기능의 빈 곳을 사용자가 지적한다

앞선 한 사용자는 이력 개요와 blame이 약하다고 했다.[^wodenokoto]
2018년 Lobste.rs에서는 Linux에서 설정 메뉴가 열리지 않는 버그를 만났지만 보고하려면 포럼 가입이 필요했다는 불만이 있었다.[^fkumro]
이는 당시 버전의 인상이고 지금의 상태가 아니다.

### 외부 반응

HN 헤더의 글은 2024년 것이다. 2018년 9월 HN에는 935점 351개 댓글의 글이 있고 Lobste.rs 글도 같은 시기의 것이어서 출시 때의 반응이다.
GeekNews에서는 `Sublime Merge`로 검색해 이 제품을 원문으로 삼은 토픽이 없었다(대조 쿼리는 정상이었다).

## 인사이트

### 가져갈 것은 CLI와 대응하는 GUI의 설계이다

사용자들이 좋게 본 점은 키보드와 명령 팔레트, 명령 이름이 Git과 같다는 점, 툴팁으로 명령을 보여 주는 점이다.
GUI가 CLI를 숨기지 않고 대응시키면 숙련자도 쓰기 쉽다는 사례로 쓸 수 있다. 이는 이 문서의 적용이다.

### 병합 도구와 커밋 도구를 나눠 고른다

HN의 평가는 병합과 커밋 구성에서 강하고 이력 개요에서 약하다는 쪽이었다.
IDE의 이력 도구와 함께 쓰는 사용자도 있었다.[^outcoldman]
도구 한 개로 모든 작업을 해결하기보다 작업별로 쓰는 도구를 나누는 선택지가 있다.

### 확인할 관찰

이 제품의 주장을 가를 관찰은 세 가지이다.
같은 저장소에서 다른 클라이언트와 비교한 속도,
홈페이지가 적지 않은 현재 가격과 갱신 조건,
이력 개요와 blame 같은 약점의 개선이다.

---

[^tehnub]: <https://news.ycombinator.com/item?id=40863900>

[^pilif]: <https://news.ycombinator.com/item?id=40863935>

[^wodenokoto]: <https://news.ycombinator.com/item?id=40863962>

[^apocalyptic0n3]: <https://news.ycombinator.com/item?id=40866305>

[^ac]: <https://lobste.rs/s/gmxeyq/sublime_merge_git_client_from_makers#c_axxunp>

[^ben-schaaf]: <https://news.ycombinator.com/item?id=40864515>

[^have-faith]: <https://news.ycombinator.com/item?id=40863804>

[^sam-goody]: <https://news.ycombinator.com/item?id=40863633>

[^thiht]: <https://news.ycombinator.com/item?id=40864879>

[^fkumro]: <https://lobste.rs/s/gmxeyq/sublime_merge_git_client_from_makers#c_wtb44d>

[^outcoldman]: <https://news.ycombinator.com/item?id=40864997>
