# F/OSS 코믹스 13화: 테이프 한 통씩 복사해 보내던 BSD가 3BSD와 DARPA의 관심으로 이어지기까지

원문: [13. BSD Unix, Part 3 - The Beginning of BSD Unix](https://fosscomics.com/posts/13.%20BSD%20Unix%20Part%203%20-%20The%20Beginning%20of%20BSD%20Unix/)

HN 토론: <https://news.ycombinator.com/item?id=50332163> (212점, 30개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/3nasb5/beginning_bsd_unix> (22점, 0개 댓글)

## 내용

F/OSS Comics는 자유 및 오픈 소스 소프트웨어의 역사를 그리는 웹 만화 시리즈이고,
이 13화는 2026-10-30에 올라온 BSD Unix 3부작의 마지막 편이다.
앞의 두 편은 Unix 코드가 UC Berkeley로 간 이야기와 vi 에디터의 탄생이다.
13화는 BSD의 시작과 초기 배포판 세 개(BSD, 2BSD, 3BSD)를 다루고, 끝에 참고 문헌
여섯 건을 단다.

### 첫 번째 BSD

1976년 Ken Thompson이 Bell Labs로 돌아간 뒤,
Bill Joy와 Chuck Haley가 Unix 커널을 직접 살펴보기 시작했다고 만화는 그린다.
다른 대학이 Pascal 컴파일러 사본을 원하자 Joy가 이를 em에서 발전한 줄 에디터
ex와 묶어 테이프로 보냈다.
1977년 초 Joy가 이렇게 엮은 것이 Berkeley Software Distribution, 곧 BSD이다.
이 초기 BSD는 독립한 운영체제가 아니라 기존 Unix 시스템에 설치하는 소프트웨어
모음이었고,
이듬해까지 약 서른 개가 나갔다고 한다.
BSD를 받으려면 AT&T의 Unix 소스 라이선스가 있어야 했고, Berkeley는 테이프와
배송비만 받았다.
만화는 Berkeley에 연구 소프트웨어를 나누는 전통이 있었고,
Free Speech Movement, 히피 문화, 반전 운동도 Joy가 아주 적은 돈만 받기로 한 데
영향을 주었다고 알려져 있다고 쓴다.
대학과 연구 기관은 소스 코드를 포함한 Unix를 낮은 라이선스 비용으로 얻을 수
있었고 이것이 Unix의 확산을 도왔다.
AT&T는 독점 금지 합의 때문에 컴퓨터 사업을 할 수 없어 Unix를 제품으로 팔 수도
없었다.

### 2BSD

사용자 의견으로 Pascal 시스템을 개선한 Joy는 이를 vi(ex의 비주얼 모드), C 셸
등과 묶어
Second Berkeley Software Distribution, 2BSD를 만들었다.
이듬해까지 약 75개의 테이프가 나갔다.
Joy는 버그 수정과 커널 조정만이 아니라 모든 배포 요청을 직접 받아 테이프에
복사해 우편으로 보냈다.

### 1978년 VAX가 Berkeley에 오다

Fateman 교수 연구실이 32비트에 메모리 1MB인 VAX를 받게 되었고, 거기에 Unix를
올리자는 이야기가 나온다.
Bell Labs가 이미 VAX용 Unix 32/V를 만들어 두었으나,
32/V는 VAX의 가상 메모리 기능을 쓰지 않아 프로그램의 주소 공간이 물리 메모리
크기에 묶였다.
Richard Fateman의 연구는 MIT가 1960년대 말부터 개발한 기호 계산 시스템 Macsyma를
쓰는 것이어서 더 큰 공간이 필요했다.
Berkeley 대학원생 Ozalp Babaoglu가 지도교수 Domenico Ferrari의 요청으로 가상
메모리 코드를 만들었고,
Joy가 이를 32/V에 통합하고 디버깅하는 것을 도왔다.
1978년 말 연휴에도 디버깅이 이어졌고, 1979년 1월에 대부분의 버그가 고쳐졌다.

Joy는 ex, vi, C 셸 등 2BSD 도구를 VAX로 옮겼고,
Peter Kessler와 Marshall Kirk McKusick이 Pascal 시스템을 옮겼다.
이것이 32/V의 표준 유틸리티와 가상 메모리 커널에 묶여 3BSD가 되었고 1979년
12월에 나가기 시작했다.
1969년부터 ARPANET이 DARPA가 지원하는 연구 기관들을 이었지만 기관마다 컴퓨터와
운영체제가 달라 소프트웨어를 나누기 어려웠다.
DARPA는 Unix의 이식성과 Berkeley가 3BSD를 연구 기관에 성공적으로 배포한 것에
관심을 보였다고 만화는 쓴다.

## 분석

### 이 화는 BSD를 배포 방식의 이야기로 읽게 한다

BSD의 시작을 운영체제의 설계가 아니라 테이프를 복사해 보내는 일로 그린다.
첫 BSD는 소프트웨어 모음이었고, 독립한 운영체제는 3BSD에 이르러서이다.
그래서 이 화에서 BSD의 정체성은 코드의 구조보다 누가 누구에게 어떤 조건으로
코드를 나눴느냐에 있다.
이것은 만화의 구성을 이 문서가 정리한 해석이다.

### 가상 메모리가 3BSD로 가는 전환점이다

32/V가 VAX의 가상 메모리를 쓰지 않았고 Macsyma가 큰 주소 공간을 필요로 했다는
만화의 서술은
BSD가 독자적인 커널 작업을 하게 된 계기를 한 가지 구체적 요구로 설명한다.
그 요구가 Babaoglu의 연구와 Joy의 통합 작업으로 이어지고, 결과가 3BSD라는 이름의
첫 독립 배포가 된다.

## 비평

### 인과의 설명이 만화의 대사와 짧은 글에 의존한다

각 장면의 설명은 한두 문장의 본문과 참고 문헌 번호로 이루어지고,
Joy의 동기(Free Speech Movement, 히피 문화, 반전 운동)는 “그렇다고 알려져
있다”는 형식으로만 적힌다.
HN의 getfacl은 자신이 BSD 이야기의 신화가 아닌 버전을 쓰겠다며 대중적 재해석의 일부를 바로잡고 싶다고 말한다.[^getfacl]
meekins가 구체적인 내용을 청하지만 이 문서가 읽은 범위에 답은 없다.[^meekins]
이 화의 동기 설명을 사실로 읽을 수 없다는 점은 본문의 표현이 이미 인정한다.

### 만화 형식이 서술에 더하는 것이 무엇인지 논쟁이 있었다

lproven은 이 시리즈가 트윗 길이의 텍스트 역사에 삽화를 붙인 것이고 만화라는
매체의 장점을 쓰지 않았다고 비판한다.[^lproven]
embedding-shape는 사이트가 만화 사이트이고 저자가 만화를 그리고 싶어서 그렸으며,
다큐멘터리 대부분도 10~15분짜리 블로그 글이 될 수 있어도 매체는 남는다고
답한다.[^embedding-shape]
이 문서는 만화 그림을 직접 평가하지 못했고 장면의 대사와 본문만 읽었다.

### 용어 하나가 질문으로 남는다

jolmg는 ex가 ed가 아니라 em에서 나왔다는 만화의 문장이 맞는지 묻고,
nagaiaida는 링크 하나로 답한다.[^jolmg][^nagaiaida]
이 문서는 그 링크를 열어 보지 않았으므로 어느 쪽이 맞는지 판정하지 못한다.
만화의 문장은 만화의 서술로만 전한다.

## 인사이트

### 소스 라이선스 위의 낮은 가격이 확산의 조건이었다

만화가 보여 주는 BSD의 초기 확산 조건은 세 가지다.
AT&T의 Unix 소스 라이선스가 있는 곳에서만 받을 수 있었고,
Berkeley는 테이프와 배송비만 받았으며,
AT&T는 독점 금지 합의 때문에 Unix를 제품으로 팔 수 없었다.
그래서 이 화에서 확산의 원동력은 공개된 자유 소프트웨어 라이선스가 아니라 소스
접근을 가진 조직 안에서의 낮은 비용이다.
이 구분은 만화의 서술에서 이 문서가 끌어낸 것이며, 만화가 직접 이렇게 정리하지는
않는다.

### 시리즈를 읽는 방법

HN의 lioeters는 시리즈 전체를 읽고 있다고 했고 wdr1은 앞의 두 편도 읽었다고 한다.[^lioeters][^wdr1]
이 화만으로는 BSD 1부(Berkeley로 간 Unix)와 2부(vi의 탄생)의 맥락이 빠지므로,
13화는 앞 두 편을 읽은 뒤 보면 DARPA 이야기의 뜻이 더 분명하다.
alexfortin은 RSS나 Atom 피드가 없어서 피드 리더에 넣을 수 없다고 아쉬워하는데,
이것은 이 시리즈를 꾸준히 읽으려는 독자에게 현실적인 장벽이다.[^alexfortin]

### 이 이야기를 확인하는 관찰

만화가 참고한 McKusick의 글과 TUHS의 2BSD 아카이브에서 배포 수와 날짜를 확인할
수 있다.
만화는 BSD 약 30개, 2BSD 약 75개, 3BSD 1979년 12월이라고 썼으므로,
이 숫자들이 원문과 같으면 이 화의 서술이 지지된다.
이 문서는 그 원문들을 열어 보지 않았다.

---

[^getfacl]: <https://news.ycombinator.com/item?id=50335828>

[^meekins]: <https://news.ycombinator.com/item?id=50340403>

[^lproven]: <https://news.ycombinator.com/item?id=50336130>

[^embedding-shape]: <https://news.ycombinator.com/item?id=50336255>

[^jolmg]: <https://news.ycombinator.com/item?id=50332706>

[^nagaiaida]: <https://news.ycombinator.com/item?id=50332729>

[^lioeters]: <https://news.ycombinator.com/item?id=50333911>

[^wdr1]: <https://news.ycombinator.com/item?id=50347341>

[^alexfortin]: <https://news.ycombinator.com/item?id=50334317>
