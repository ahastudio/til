# GitUp: macOS용 Git 클라이언트

<https://gitup.co/>

<https://github.com/git-up/GitUp>

HN 토론: <https://news.ycombinator.com/item?id=9653978> (267점, 256개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ko7hdk/gitup> (19점, 17개 댓글)

## 소개

GitUp은 Pierre-Olivier Latour가 만든 macOS용 무료 오픈소스 Git GUI 클라이언트이다.
사이트는 평생 기다려 온 Git 인터페이스가 마침내 왔다고 소개한다.
직접 설치해 써 보지 않았고 위키와 기여 안내, GitUpKit 소스는 열지 못했다.
설명은 모두 프로젝트의 주장이다.

GitHub API로 읽은 시점(2026년 11월 19일)의 수치는 별 12,167개, 포크 1,514개, 열린 이슈와 풀 리퀘스트 370개, 라이선스 GPL-3.0, 언어 Objective-C, 생성일 2015년 8월 13일, 마지막 푸시 2026년 10월 8일이다. 저장소의 홈페이지 필드는 `gitup.co`이다.
최신 릴리스는 v1.5.0 「Tahoe Release」(2026년 7월 15일)이다. 내용은 새 Tahoe 디자인과 Sparkle 업데이트 API, libgit2 1.4.4에서 1.9.0으로의 갱신(OpenSSH 키 지원과 shallow clone), 모두 스테이징 수정, 색인이 잠긴 상태에서 줄을 스테이징할 때의 충돌 수정, 하위 디렉터리에서 상위 저장소 열기, 최소 macOS 12.4이다. 내려받기 파일은 GitUp.zip이다.

사이트와 README가 소개하는 기능은 다음과 같다.

- 라이브 맵: 저장소 그래프를 직접 편집한다. 커밋 순서 바꾸기, fixup, 병합이 되고 GitUp 밖에서 바뀐 것은 새로 고침 없이 반영된다.
- 퀵 뷰: 커밋을 고르고 스페이스를 누르면 메시지와 diff가 보인다.
- 무제한 실행 취소와 다시 실행: 리베이스와 병합을 포함해 거의 모든 작업에 되며 사이트는 `cmd-z`만큼 쉽다고 한다.
- 스냅숏: 저장소 상태의 타임머신 같은 이력으로 한 번 클릭 되돌리기를 한다.
- 이력 다시 쓰기: 커밋 분할, 삭제, 순서 변경, fixup과 squash, 체리픽, 병합, 리베이스가 된다. README는 시각적 커밋 분할기와 통합 reflog 브라우저가 Git에 원래 없는 기능이라고 한다.
- 검색: 메시지, 작성자, diff 내용으로 브랜치와 태그와 모든 커밋을 즉시 검색한다.
- 성능 주장: Git 저장소 자체의 약 4만 커밋 그래프를 1초 안에 불러와 그린다고 한다.
- 동작 방식: 사이트는 Git 실행 파일을 거치지 않고 저장소 데이터베이스와 직접 상호작용해 다른 클라이언트보다 더 믿을 만하고 명령줄보다 빠른 경우가 많다고 한다. README에 따르면 UI는 재사용 가능한 Git 도구 키트 GitUpKit 위의 얇은 층이고, GitUpKit은 libgit2의 최소 부분집합만 쓰고 리베이스 엔진을 포함한 나머지를 직접 구현하며 libgit2의 맞춤 포크를 쓴다.
- 업데이트 채널: `v` 태그는 Stable, `b` 태그는 Continuous이다.
- 요구와 설치: macOS 12.4 이상. 내려받기, 또는 `brew install gitup-app`(개발자가 관리하지 않는 Homebrew 항목)이다. 소스 빌드는 서명 설정이 필요하다.
- 관련 앱: GitUpKit으로 만든 Retcon(커밋 이력 다시 쓰기 앱)이 있으나 GitUp과 무관하다고 사이트가 밝힌다.

## 분석

### 중심 주장은 Git CLI를 거치지 않는 빠르고 되돌릴 수 있는 GUI라는 것이다

다른 GUI가 Git CLI를 감싸 대화상자를 얹는 것과 달리 자체 도구 키트로 저장소를 직접 다루고, 그 위에 무제한 되돌리기를 쌓은 구성이다.
HN에서 제작자는 다른 Git GUI가 대개 CLI를 감싸 대화상자를 더하는 것이고 GitUp은 이를 피하도록 설계했다고 설명했다.[^swisspol-cli]
이는 사이트와 제작자의 서술을 이 문서가 정리한 것이다.

### 오래된 학습 도구로 평가받는다

HN 2020년 글에서 한 사용자는 이 도구로 명령줄 지식의 틈(몇 단계 앞 커밋의 메시지 바꾸기 등)을 메우는 데 썼고 GUI가 기능의 발견을 돕는다고 했다.[^mettamage]
이 평가는 사용자의 경험이다.

## 비평

### macOS 전용이라는 한계가 반복해서 지적된다

2015년 HN에서도 Lobste.rs에서도 첫 반응의 상당수가 macOS 전용이고 당시에는 자유 소프트웨어가 아니라는 점이었다.[^greduan][^mempko]
지금은 GPL-3.0 오픈소스가 되었지만 macOS 전용이라는 점은 같다. 2020년 HN에서도 같은 질문이 나왔고 다른 사용자는 Fork를 권했다.[^solarkraft][^memco]

### 성능과 안정성의 서술이 자기 주장이다

4만 커밋을 1초 안에 그린다는 수치와 다른 클라이언트보다 더 믿을 만하다는 주장은 독립 측정이 없다.
HN에서 한 사용자는 SourceTree가 느리고 메모리를 많이 쓴다는 점이 GitUp으로 옮긴 이유라고 했다.[^dcre]
이는 2015년의 개인 경험이다.

### 용도에 대한 회의가 있었다

2015년 HN에서 한 사용자는 명령줄이 빠르다고 아는 사람에게는 생산성 이득이 없을 것이라고 했고, 제작자는 이를 다른 GUI에는 맞지만 GitUp은 CLI를 감싼 것이 아니라서 다르다고 답했다.[^chjohasbrouck][^swisspol-cli]
복잡한 저장소에서는 맵이 쓸모를 잃는다는 지적에 제작자는 그 그래프가 Git 저장소 자체의 것이라고 답했다.[^scotthew1]

### 외부 반응

HN 헤더의 글은 2015년 공개 직후의 것이고 지금의 평가가 아니다. 계정 등록이 필요한 고급 기능에 대한 우려도 그때의 것이다.[^zyxley]
GeekNews에서는 `GitUp`으로 검색해 이 프로젝트의 토픽이 없었다(대조 쿼리는 정상이었다).

## 인사이트

### 가져갈 것은 Git을 호출하지 않고 저장소 모델을 직접 다룬 설계이다

CLI를 감싸지 않고 저장소 데이터를 직접 다루면 스냅숏과 무제한 되돌리기 같은 기능을 쌓을 수 있다.
반대로 모든 로직을 다시 구현해야 하는 부담이 있다. 다른 Git 도구의 설계를 비교하는 축으로 쓸 수 있다. 이는 이 문서의 적용이다.

### 이력 다시 쓰기는 되돌리기와 함께 쓴다

HN에서 한 사용자는 초보자 대상 도구가 커밋 메시지 수정을 앞세우는 것을 걱정했다.[^dan00]
이력을 바꾸는 기능을 안전하게 쓰려면 이 도구의 스냅숏 같은 복구 수단이 짝이 되어야 한다.

### 확인할 관찰

이 프로젝트의 주장을 가를 관찰은 세 가지이다.
같은 저장소에서 다른 클라이언트와 비교한 속도,
최신 macOS에서의 안정성,
릴리스 이후 쌓이는 이슈 362개의 처리이다.

---

[^swisspol-cli]: <https://news.ycombinator.com/item?id=9655109>

[^mettamage]: <https://news.ycombinator.com/item?id=24645216>

[^greduan]: <https://lobste.rs/s/ko7hdk/gitup#c_jlqd7s>

[^mempko]: <https://lobste.rs/s/ko7hdk/gitup#c_f0pjbh>

[^solarkraft]: <https://news.ycombinator.com/item?id=24644355>

[^memco]: <https://news.ycombinator.com/item?id=24645932>

[^dcre]: <https://news.ycombinator.com/item?id=9654773>

[^chjohasbrouck]: <https://news.ycombinator.com/item?id=9654976>

[^scotthew1]: <https://news.ycombinator.com/item?id=9654888>

[^zyxley]: <https://news.ycombinator.com/item?id=9654430>

[^dan00]: <https://news.ycombinator.com/item?id=9654271>
