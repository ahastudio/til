# Fork: Mac과 Windows용 Git 클라이언트

<https://git-fork.com/>

HN 토론: <https://news.ycombinator.com/item?id=31567702> (74점, 65개 댓글)

GN 토론: <https://news.hada.io/topic?id=147>

## 소개

Fork는 Dan Pristupov와 Tanya Pristupova가 만드는 Mac과 Windows용 Git 클라이언트이다.
홈페이지는 이를 빠르고 친근한 Git 클라이언트라고 소개한다.
직접 설치해 써 보지 않았고 릴리스 노트와 블로그는 열지 않았다.
설명은 모두 개발자의 주장이다.

홈페이지가 소개하는 내용은 다음과 같다.

- 개발자: 홈페이지는 소프트웨어 개발자 가족이 여가 시간에 전업으로 Fork를 만든다고 적는다. 푸터의 저작권자는 Danil Pristupov이다.
- 버전과 요구 환경: Mac은 2.66.7(OS X 10.11 이상), Windows는 2.21.1(Windows 7 이상)이다. 릴리스 날짜는 홈페이지에 없다.
- 가격: 플랫폼마다 59.99달러이고 무료 평가판이 있다.
- 기본 기능: 가져오기, 풀, 푸시, 커밋, 수정(amend), 브랜치와 태그, 원격 저장소 만들기와 삭제, 체크아웃, 체리픽, 되돌리기, 병합, 리베이스, 스태시, 서브모듈이다.
- 커밋 화면: 줄 단위로 스테이징하고 최근 커밋 메시지에 접근한다.
- 추가 기능: 대화형 리베이스, blame, 임의 커밋에서의 파일 트리 열람, 병합 충돌 해결, Reflog로 잃은 커밋 복원, 커밋 목록 안의 스태시, Git-flow, Git LFS, GPG이다.
- 화면 소개: GitHub 알림, 이미지 diff, 고급 diff 뷰어, 파일이나 디렉터리를 바꾼 커밋을 찾는 이력이 있다.

라이선스 페이지에 따르면 한 사용자가 한 라이선스 키로 Mac과 Windows에서 동시에 최대 3대에서 쓸 수 있고 장기 사용에는 라이선스를 구입해야 한다.
임대, 판매, 역공학은 금지되고 준거법은 체코 공화국 법이다.

## 분석

### 중심 주장은 빠르고 다듬어진 유료 GUI라는 것이다

홈페이지의 이름 지음과 기능 목록은 속도와 사용성이 핵심이라고 말하지만 수치는 없다.
성능 주장은 HN의 사용자 증언으로만 뒷받침된다.
이는 홈페이지의 서술을 이 문서가 정리한 것이다.

### 소규모 개발자가 유료 단일 제품을 직접 운영한다

두 사람이 개발하고 개발자가 이슈에 직접 답하는 운영이 사용자 평가의 중심이다.
HN에서 한 사용자는 이슈를 올리자 Dan이 한 시간 안에 답했다고 했다.[^zubspace]
이는 큰 회사의 지원 체계와 다른 장단점이 있다. 이는 이 문서의 관찰이다.

### 기능이 Git의 실제 구조에 가깝다는 평가를 받는다

HN에서 한 사용자는 Fork가 Git이 실제로 동작하는 방식을 다른 GUI보다 잘 담았다고 평했다.[^oerpli]
한 사용자는 Fork가 자기 회사의 모노레포를 감당하는 유일한 Mac GUI라고 말했다.[^zacwest]
둘 다 개인 후기이다.

## 비평

### 성능 우위의 근거가 후기뿐이다

HN의 다른 사용자는 왜 Fork가 다른 GUI보다 빠른지 알고 싶다고 물었고 답은 달리지 않았다.[^sdflhasjd]
다른 사용자는 가장 빠른 GUI가 GitUp이라고 반문했다.[^frogperson]
홈페이지와 HN 어느 쪽에도 비교 측정이 없다.

### 안정성에 대한 상반된 증언이 있다

한 사용자는 Fork가 주니어의 로컬 저장소를 망가뜨리는 데 시간을 쓰게 한다고 했고, Dan은 이런 피드백은 처음 듣는다며 상세 내용을 요청했다.[^vanit-fork][^danpristupov]
같은 글의 여러 사용자는 반대로 몇 년간 안정적이었다고 했다. 어느 쪽이 일반적인지는 읽은 범위에서 알 수 없다.

### 플랫폼과 소스 공개의 제약

Linux 버전이 없다. HN에서 Linux로 옮기는 유료 사용자는 그래서 Fork를 쓰지 않은 지 오래되었다고 했다.[^lioeters]
소스가 닫혀 있다는 점은 사용자도 인정하면서 문제가 되지 않는다고 본다.[^anaganisk]
HN의 한 사용자는 오픈소스 대안이 충분히 성숙했다고 말했고 다른 사용자는 도구에 돈을 내지 않는 것이 문제라고 반박했다.[^skrowl][^gittower-reply]

### 외부 반응

HN 글은 2022년의 것이고 수년 전 인상을 포함한다.
GeekNews 토픽은 2019년 7월의 것으로 옛 주소(`fork.dev`)로 올라와 있다. 한 이용자는 Tower를 버리고 잘 쓰고 있다고 했고, 운영자는 맥용은 대체 도구가 여럿이나 Windows용에서는 가장 깔끔한 UI일 것이라고 썼다.[^xguru]
Lobste.rs에는 `git-fork.com` 도메인의 글이 없었다.

## 인사이트

### 가져갈 것은 유료 GUI를 고를 때의 기준이다

사용자들이 꼽은 이유는 모노레포 성능, 대화형 리베이스와 충돌 처리의 편의, 개발자의 응답 속도였다.
무료 대안과 비교할 때 가격 대비 이 세 가지를 자기 저장소로 시험할 수 있다. 이는 이 문서의 적용이다.

### 라이선스 조건을 구매 전에 읽는다

한 키로 3대까지 쓸 수 있고 Mac과 Windows 키가 플랫폼마다 따로 있다. 둘 다 쓰는 사용자는 두 번 사는지 확인한다.

### 확인할 관찰

이 제품의 주장을 가를 관찰은 세 가지이다.
같은 저장소에서 다른 GUI와 비교한 속도와 메모리,
안정성 이슈의 빈도와 수정 속도,
Linux 지원이나 소스 공개 같은 플랫폼 정책의 변화이다.

---

[^zubspace]: <https://news.ycombinator.com/item?id=31567749>

[^oerpli]: <https://news.ycombinator.com/item?id=31573262>

[^zacwest]: <https://news.ycombinator.com/item?id=31570469>

[^sdflhasjd]: <https://news.ycombinator.com/item?id=31575803>

[^frogperson]: <https://news.ycombinator.com/item?id=31576172>

[^vanit-fork]: <https://news.ycombinator.com/item?id=31571486>

[^danpristupov]: <https://news.ycombinator.com/item?id=31571754>

[^lioeters]: <https://news.ycombinator.com/item?id=31575475>

[^anaganisk]: <https://news.ycombinator.com/item?id=31570143>

[^skrowl]: <https://news.ycombinator.com/item?id=31569738>

[^gittower-reply]: <https://news.ycombinator.com/item?id=31570078>

[^xguru]: <https://news.hada.io/topic?id=147#cid169>
