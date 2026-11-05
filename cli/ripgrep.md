# ripgrep은 grep, ag, git grep보다 빠르다: 25개 벤치마크로 편 주장

원문: [ripgrep is faster than {grep, ag, git grep, ucg, pt, sift} - Andrew Gallant's Blog](https://blog.burntsushi.net/ripgrep/)

HN 토론: <https://news.ycombinator.com/item?id=12564442> (740점, 209개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg> (75점, 12개 댓글)

GN 토론: <https://news.hada.io/topic?id=12111>

## 요약

2016년 9월 23일, Andrew Gallant는 명령줄 검색 도구 ripgrep(`rg`)을 소개하는
글을 올렸다.
ripgrep은 The Silver Searcher(ack을 본뜬 도구)의 사용 편의와
GNU grep의 원시 성능을 합치려는 도구다.
Rust로 작성되었고 Linux, Mac, Windows용 바이너리를 제공한다.
글이 쓰인 시점의 버전은 0.1.2이며,
저자는 ripgrep과 그 밑의 정규식 엔진(regex engine)을 모두 만든 사람이라고
스스로 밝힌다.

글은 25개 벤치마크로 세 가지 주장을 뒷받침하겠다고 시작한다.
첫째, 파일 하나를 검색하든 거대한 디렉터리를 검색하든
성능과 정확성 양쪽에서 ripgrep보다 분명히 앞서는 도구는 없다.
둘째, ripgrep은 제대로 된 Unicode 지원을 하면서도
큰 대가를 치르게 하지 않는 유일한 도구다.
셋째, 많은 파일을 한꺼번에 검색하는 도구는
memory map(mmap)을 쓰면 대체로 더 느려진다.

소개 부분은 장점과 쓰지 말아야 할 이유를 함께 적는다.
ripgrep은 기본적으로 디렉터리를 재귀 검색하고,
`.gitignore`에 적힌 파일과 숨김 파일, 바이너리 파일을 건너뛴다.
`rg -tpy foo`처럼 파일 종류로 범위를 좁힐 수 있고,
`-P`를 주면 정규식 엔진을 PCRE2로 바꿔 look-around와 backreference를 쓸 수 있다.
UTF-16, latin-1, GBK, EUC-JP, Shift_JIS 같은 인코딩과
gzip, xz, lzma, bzip2, lz4로 압축된 파일도 검색한다.
쓰지 말아야 할 이유로는 POSIX 같은 표준을 따르지 않아서
어디에나 있는 도구가 아니라는 점,
다른 도구에만 있는 기능이나 버그에 기대고 있다는 점,
성능이 나쁜 예외 상황이 있다는 점,
설치할 수 없는 플랫폼이 있다는 점을 든다.

글의 중간은 grep 계열 도구의 구조 설명이다.
검색할 파일을 모으는 단계에서는 `stat` 호출을 최소로 하는 디렉터리 순회,
`.gitignore` 규칙을 한꺼번에 맞춰 보는 필터링,
작업을 스레드에 나눠 주는 Chase-Lev work-stealing queue가 나온다.
검색 단계에서는 정규식 엔진이
백트래킹(backtracking) 방식인지 유한 오토마타(finite automata)
방식인지가 갈린다.
GNU grep과 git grep은 직접 만든 오토마타 엔진,
ripgrep은 Rust의 regex 라이브러리,
The Silver Searcher와 Universal Code Grep은 PCRE,
The Platinum Searcher와 sift는 Go의 regexp 라이브러리를 쓴다.
리터럴 최적화(literal optimization)로는
`memchr`로 후보 위치를 빨리 찾는 방법,
여러 문자열을 SIMD로 한꺼번에 찾는 Teddy 알고리즘, Aho-Corasick이 설명된다.
저자는 파일을 줄 단위로 검색하지 말고 큰 바이트 버퍼를 통째로 검색하라고 하며,
출력은 스레드마다 메모리 버퍼에 결과를 모은 뒤 차례로 내보낸다고 설명한다.

벤치마크는 두 갈래다.
하나는 빌드까지 마친 Linux 커널 소스(커밋 d0acc7)를 검색하는 코드 검색이고,
다른 하나는 OpenSubtitles2016 자막 파일 하나를 검색하는 단일 파일 검색이다.
자막은 영어 약 1GB와 러시아어 약 1.6GB 표본을 쓴다.
각 명령은 세 번 예열한 뒤 열 번 측정해 평균과 표준편차를 낸다.
실행 환경은 EC2 c3.2xlarge(Xeon E5-2680 2.8 GHz, 메모리 16 GB, SSD 80 GB)이며,
저자의 로컬 머신(i7-6900K 3.2 GHz, 메모리 64 GB)에서도 따로 측정했다.
비교 대상은 ripgrep 0.1.2, GNU grep 2.25, git grep 2.7.4,
The Silver Searcher, Universal Code Grep, The Platinum Searcher, sift다.

| 벤치마크                       | ripgrep                        | 비교 도구                                                            |
| ------------------------------ | ------------------------------ | -------------------------------------------------------------------- |
| linux_literal_default          | 0.349                          | Universal Code Grep 0.218, git grep 0.342, The Silver Searcher 1.589 |
| linux_unicode_word(`\wAh`)     | 0.355 (Unicode)                | git grep 13.045 (Unicode), 2.991 (ASCII)                             |
| linux_alternates_casei         | 0.391                          | Universal Code Grep 0.522, git grep 2.018                            |
| linux_no_literal               | 0.577 (Unicode), 0.416 (ASCII) | git grep 26.382 (Unicode), 4.153 (ASCII)                             |
| subtitles_literal (영어)       | 0.268                          | GNU grep 0.516, sift 0.326                                           |
| subtitles_literal_casei (영어) | 0.366                          | GNU grep 4.084 (Unicode), 0.614 (ASCII)                              |
| subtitles_alternate (영어)     | 0.294                          | GNU grep 2.955                                                       |
| subtitles_no_literal (영어)    | 2.777 (Unicode), 2.541 (ASCII) | GNU grep 4.411 (ASCII)                                               |

원문 표에는 단위가 적혀 있지 않다.
같은 도구가 90초 넘게 걸린다는 본문 서술에 맞춰 초 단위로 읽었다.
위 표의 값은 EC2에서 잰 평균이다.
`linux_`로 시작하는 항목은 `.gitignore`를 따르는 `(ignore)` 설정의 값이다.

저자는 결론에서 세 주장을 다시 짚는다.
첫 주장에 대해서는 모든 항목에서 이기지는 않지만 어떤 도구도 우위를 주장할 수
없다고 정리한다.
둘째 주장에는 Unicode를 지원하는 도구가 ripgrep, GNU grep, git grep뿐이고
뒤의 둘은 Unicode를 켜면 많이 느려진다고 답한다.
셋째 주장에는 작은 파일 여러 개를 병렬로 검색할 때는 memory map이 더 느리고
큰 파일 하나를 검색할 때는 더 빠르다고 답한다.

## 분석

### 세 주장이 벤치마크의 구성을 정한다

벤치마크를 둘로 나눈 것은 사용자가 풀려는 문제가 둘이라는 판단에서 나왔다.
디렉터리 검색은 코드를 찾는 사용자에, 단일 파일 검색은 로그를 뒤지는 사용자에
대응한다.
저자는 두 경우의 성능 특성이 크게 다르며 한쪽에 강한 도구가 다른 쪽에도 강한
것은 아니라고 적는다.
ripgrep의 전제는 두 경우를 모두 잘할 수 있다는 것이다.

패턴의 선택에도 가정이 들어 있다.
저자는 대부분의 검색이 매치가 적고 단순한 리터럴, 리터럴의 나열,
가벼운 정규식을 쓴다고
자신의 경험에서 가설을 세운다.
그래서 매치가 적은 벤치마크를 우선하고 패턴도 그쪽으로 치우쳐 고른다.
이 가정은 세 번째 주장과도 이어진다.
매치가 적은 검색에서는 줄을 하나하나 파싱하는 일이 대부분 헛수고가 되므로,
버퍼 전체를 한 번에 검색하는 구조가 이긴다는 논리다.

### 속도는 ripgrep과 정규식 라이브러리의 분업에서 나온다

글이 반복해서 설명하는 속도의 원천은 크게 넷이다.
첫째, `memchr`를 쓸 때 리터럴의 마지막 바이트가 아니라
가장 드물 것 같은 바이트를 고른다.
`Sherlock Holmes`에서는 `s`보다 `S`나 `H`가 훨씬 드물어서 빠르게 건너뛸 수 있다.
러시아어 패턴에서는 첫 바이트가 `\xD0`이나 `\xD1`인 글자가 대부분이라
첫 바이트를 스캔하는 Go의 방식이 느려지고,
ripgrep은 미리 계산한 바이트 빈도표로 이를 피한다.

둘째, 대소문자를 무시하는 검색을 가능한 모든 대소문자 조합의 나열로 바꾼다.
`PM_RESUME`은 짧은 접두사 `PM_RE`, `PM_Re` 등 16개로 펼쳐지고,
이 나열을 Teddy 알고리즘에 넘긴다.
Unicode의 단순 대소문자 대응 규칙을 따르므로 `S`에는 `ſ`도 포함된다.
후보가 너무 많아지면 Teddy가 오히려 불리해서 Aho-Corasick으로 넘어간다.
저자가 든 사례에서는 리터럴이 48개로 늘어나는 `subtitles_alternate_casei`가
그런 경우다.

Teddy는 Intel의 Hyperscan 라이브러리에서 온 알고리즘이다.
Hacker News에서 Hyperscan 팀 소속이라고 밝힌 glangdale는
Hyperscan의 Teddy 구현에 있는 몇 가지 최적화가
Rust 구현에는 아직 반영되지 않은 것으로 안다고 적고,
이를 좋은 과제로 제안했다.[^glangdale]
저자는 가는 곳마다 Teddy를 자랑하고 다닌다고 답하며,
Hyperscan을 공개해 준 데 감사를 전했다.[^burntsushi-glangdale]

셋째, UTF-8 디코딩을 유한 상태 기계 안에 넣었다.
검색 텍스트를 코드 포인트로 먼저 바꾸는 단계가 없고 바이트열에 곧바로 맞춘다.
이 덕분에 ripgrep은 Unicode 인식 `\w`를 써도
ASCII 전용으로 돌릴 때와 시간 차이가 크지 않다.
반면 같은 `linux_no_literal`에서 git grep은 Unicode를 켜면 4.153에서 26.382로
느려진다.
GNU grep과 git grep은 Unicode를 다루는 별도 경로를 코어에 두고 있다고 저자는
설명한다.

Lobste.rs에서 LenFalken은 ag는 바이너리 검색이 되는데
ripgrep은 UTF-8 전용이 아니냐고 물었다.[^LenFalken]
저자는 ripgrep이 ASCII 호환 인코딩이면 무엇이든 처리하고
순수한 바이너리 데이터도 검색한다고 답했다.
이 점은 ag와 같고, 여기에 Unicode 지원이 더해져
`\w`가 모든 Unicode 단어 문자에 맞는다는 것이다.[^inactive-user-lenfalken]

넷째, `\w+\s+Holmes\s+\w+` 같은 패턴에서
패턴 안쪽의 리터럴(inner literal)을 뽑아 후보 줄을 찾은 뒤
그 줄에만 정규식을 돌린다.
이 최적화가 정규식 엔진이 아니라 검색 도구에 있어야 하는 이유도 저자는 설명한다.
리터럴을 찾아도 전체 매치가 어디서 시작하는지 엔진은 알 수 없기 때문이다.
줄 단위로 결과를 내는 도구만 줄의 경계로 범위를 한정할 수 있다.

### memory map의 결과는 작업의 모양에 따라 뒤집힌다

세 번째 주장의 근거는 같은 도구를 설정만 바꿔 비교한 측정이다.
`linux_literal`에서 `rg (ignore)`는 0.334인데 memory map을 강제하면 1.611로
느려지며,
이는 The Silver Searcher의 1.588과 거의 같다.
반대로 자막 파일 하나를 검색하는 `subtitles_literal`에서는
`rg`가 0.268, memory map을 쓰지 않는 `rg (no mmap)`이 0.336으로
memory map이 약 25% 빠르다.
저자는 파일마다 memory map을 새로 만드는 비용이 작은 파일 수천 개를 검색할
때는 크고,
큰 파일 하나에서는 한 번만 만들면 된다고 설명한다.
ripgrep은 검색할 파일이 적을 때만 memory map을 켜는 경험적 방식을 쓴다.

저자는 처음에 memory map 방식으로 ripgrep을 만들었고,
CPU 프로파일이나 `strace`에서 memory map이 원인이라는 증거가 나오지 않았는데도
중간 버퍼(intermediate buffer) 방식의 시제품을 만들어 보고서야 훨씬 빠르다는
것을 확인했다고 적는다.
이 서술은 직관과 실제가 어긋났을 때 프로파일이 아니라 대안 구현이 답을
줬다는 사례다.

Hacker News에서 bodyfour는 스레드가 여러 개가 되면
memory map이 숨은 동기화 비용을 만든다고 짚으면서,
스레드가 하나일 때도 memory map이 손해인지 재 보면 흥미롭겠다고
적었다.[^bodyfour]
저자는 같은 Linux 소스에서 `rg -j1`로 `PM_SUSPEND`를 검색해 답했다.
기본 설정에서는 0.406초, `--mmap`을 주면 0.482초가 걸렸다.
한 번의 측정이지만, 스레드가 하나여도 많은 파일을 검색할 때는
memory map이 느렸다는 결과다.
저자는 이 값이 Linux x64 환경의 것이며
다른 운영체제에서는 전혀 다른 결과가 나올 것이라고
덧붙였다.[^burntsushi-bodyfour]

### 공정한 비교를 만드는 방법

`linux_literal_default`는 일부러 불공정하게 설계한 항목이다.
각 도구의 기본 동작이 서로 다르기 때문이다.
ripgrep은 `.gitignore`를 따르고 줄 번호를 세지 않으며,
The Silver Searcher는 같은 동작에 줄 번호를 센다.
Universal Code Grep은 `.gitignore`를 읽지 않고 허용 목록(whitelist)의 확장자만
검색하며,
sift는 숨김 파일과 바이너리 파일까지 모두 검색한다.
이 항목은 성능 비교라기보다 기본값이 어떻게 다른지를 보여 주는 용도다.

이어지는 `linux_literal`부터는 통제 변수를 둔다.
`.gitignore`를 따르는 `(ignore)`와 허용 목록을 쓰는 `(whitelist)`로
ripgrep을 두 번 돌리고,
줄 번호를 끌 수 없는 도구가 있으면 모든 도구에서 줄 번호를 켠다.
Unicode 지원 여부는 `(ASCII)` 표시로 통제한다.
반대로 memory map을 쓰느냐 버퍼를 쓰느냐는 사용자가 보는 결과를 바꾸지 않는 구현
선택이라
비교에 넣어도 공정하다고 저자는 구분한다.

## 비평

### 저자가 만든 도구를 저자가 비교했다는 한계는 글이 먼저 밝힌다

저자는 벤치마크가 직접 고른 것이고 자신이 도구 중 하나의 저자이므로 편향되어
있다고 쓴다.
분석도 가장 잘 아는 자신의 구현을 설명하는 쪽으로 기울어 있다고 인정한다.
다만 모든 도구의 소스코드를 일부는 읽었다고 덧붙인다.
이 고백은 정직하지만 한계를 없애지는 않는다.

측정 조건은 EC2 인스턴스 한 종류와 저자의 로컬 머신 한 대,
열 번의 측정이 전부다.
저자도 열 번이 통계적으로 충분하지 않을 수 있다고 인정한다.
코퍼스는 Linux 커널과 영화 자막 두 가지다.
글머리에는 일부 사람이 자기 데이터에서는 주장만큼 빠르지 않다고 보고한다는
주의도 달려 있다.
재현할 수 있는 이슈를 올려 달라고 요청하는 이 문장은 결론이 모든 데이터에
성립하지는 않는다는 신호다.

독립적인 제3자가 다른 코퍼스, 다른 하드웨어에서 같은 `benchsuite`를 돌려
같은 순위가 나오는지 확인하기 전까지, 이 글의 결론은 저자의 조건에서 성립한
결과로 읽는 것이 맞다.

글이 올라온 날 Hacker News에서는 다른 도구를 만든 사람들이 이 비교를 직접
검토했다.
The Silver Searcher의 제작자라고 밝힌 ggreer는
비교가 좋았다고 평하면서 ripgrep이 ag보다 빠른 이유를 셋으로 정리했다.
DFA로 처리할 수 있는 Rust 정규식만 지원한다는 점,
줄 번호를 기본으로 세지 않는다는 점,
memory map을 쓰지 않는다는 점이다.[^ggreer]
ggreer는 줄 번호 없는 결과는 덜 유용하다고 보아 ag에서는 성능을 포기했고,
PCRE 전체를 지원해 온 ag가 가벼운 정규식 라이브러리로 바꾸면
사용자들의 항의 메일을 받게 될 것이라고도 적었다.[^ggreer]
그는 아주 큰 코드베이스가 아니면 속도 차이는 체감하기 어렵고
체감하게 되는 것은 기능 차이일 것이라며 기대치를 낮추라고 권했다.[^ggreer]

저자는 줄 번호는 `(lines)` 표시나 모든 도구의 줄 번호 계산으로
통제했다고 답했다.
memory map은 환경에 따라 결과가 크게 다를 수 있고
Windows에서는 memory map을 켰다고 설명했다.
ag에 있는데 ripgrep에는 없는 기능은 아마 `--ackmate`, `--depth`,
일부 색상 설정, `--passthrough`, `--smart-case`, `--stats`와
Mercurial 지원 정도일 것이라고 꼽았다.[^burntsushi-ggreer]

icgrep의 제작자라고 밝힌 rob_cameron은 icgrep과의 비교가 빠져 있다고 지적했다.
icgrep이 `\p{Greek}` 같은 Unicode 문자 클래스와 큰 파일, 대안 나열에서
훨씬 빠를 수 있고 Unicode 지원 범위도 넓다는 주장이다.
그는 ripgrep이 `&&`를 문자 그대로 해석해
UTS #18 레벨 1의 요구를 채우지 못한다고도 적었다.[^rob_cameron]
저자는 icgrep이 `\p{Greek}` 같은 항목에서 조금 낫고
Unicode 지원도 더 넓다는 점을 인정했다.
다만 리터럴 최적화가 없는데,
사람들이 실제로 검색하는 것은 대부분 단순한 리터럴이라서
그 경우를 잘 처리해야 경쟁력이 있다고 답했다.
또 자신의 글은 편향되었을 뿐 아니라 선별된 것이며
빠진 것은 icgrep만이 아니라고 말했다.[^burntsushi-rob_cameron]
rob_cameron이 자신의 테스트 머신에서 같은 패턴으로 자막 파일을 검색한 결과,
ripgrep은 1분 8초, icgrep은 11.9초였다.
그는 이 결과가 저자의 환경과 크게 다르다고 적었다.[^rob_cameron-reply]
저자는 이 결과를 자신도 설명하지 못한다고 답했다.[^burntsushi-rob_cameron-reply]

Lobste.rs에서는 저장소 규모가 작은 경우가 문제가 됐다.
hoodie는 Rust 코드 4천 줄짜리 저장소에서 `rg`와 `ag`를 비교해
ripgrep은 0.015에서 0.025, ag는 0.009에서 0.014의 총 CPU 시간이 나왔다고
적었다.[^hoodie]
저자는 그렇게 작은 저장소에서는 어떤 도구도 측정해 본 적이 없다고 인정했다.
시작 시간이 중요해지는 규모이며 ag만큼 빠르지 못할 기술적 이유는 없다며
이슈를 열었다.[^inactive-user-hoodie]
반대로 cgag는 파일 25,000개, 800만 줄의 DragonFlyBSD 코드베이스에서
ripgrep이 총 0.548초, ag가 1.676초로 앞섰다고 보고했다.[^cgag]
두 보고는 글의 코퍼스(Linux 커널과 자막)가
큰 규모에 치우쳐 있었다는 점을 다시 보여 준다.

### 제목은 글이 실제로 보인 것보다 단정적이다

제목은 ripgrep이 여섯 도구보다 빠르다고 말하지만 본문의 첫 주장은 훨씬
조심스럽다.
어떤 도구도 성능과 정확성에서 ripgrep보다 분명히 앞서지 않는다는 부정형이다.
측정 결과가 이 조심스러운 표현에 가깝다.
`linux_literal_default`에서 Universal Code Grep은 0.218로 ripgrep의
0.349보다 빠르고,
`linux_alternates`에서도 0.214와 0.216으로 사실상 같다.
git grep은 첫 항목에서 0.342로 ripgrep과 거의 같다.

단일 파일에서 저자는 모든 항목에서 ripgrep이 앞선다고 쓰지만 숫자만 보면
예외가 있다.
러시아어 `subtitles_alternate_casei`에서
ASCII 전용인 Universal Code Grep은 2.868로 ripgrep의 4.834보다 빠르다.
다만 이때 Universal Code Grep은 매치를 691줄 찾고 ripgrep은 735줄을 찾아서,
저자의 기준으로는 정확성에서 ripgrep이 앞선다.
이처럼 성능과 정확성을 묶은 기준에서야 첫 주장이 성립하며,
시간만 보면 단순한 코드 검색에서 Universal Code Grep과 git grep이
대등하다는 것이 글이 스스로 인정하는 내용이다.

Hacker News에서 lobster_johnson은 맥에서 3.5GB JSON 파일을 검색해
GNU grep이 이겼다고 보고했다.[^lobster_johnson]
atombender가 캐시를 고려해 다시 잰 결과도
GNU grep이 2.7초 안팎, ripgrep 기본 설정이 3.1초 안팎이었다.
ripgrep이 앞선 것은 `--no-mmap`을 줬을 때로, 1.7초 안팎이었다.[^atombender]
단일 파일에서 ripgrep이 모든 항목을 이긴다는 서술은
운영체제와 memory map 설정에 따라 성립하지 않을 수 있다.

Lobste.rs에서 cmm은 글이 정작 중요한 내용을 묻어 두었다고 적었다.
ag로 이미 충분히 빠르다고 느끼는 사용자에게 ripgrep을 볼 이유는 속도가 아니라
`.gitignore` 지원이라는 것이다.
ripgrep은 우선순위, 상위와 하위 디렉터리의 규칙,
예외 처리(whitelisting), 재귀 glob까지 지원하는데
ag는 이 부분에 버그가 많다고 했다.[^cmm]
제목은 속도를 내세우지만, 독자 중에는 정확성을 선택 이유로 읽은 사람이
있었다는 뜻이다.

### Unicode에 대가를 치르지 않는다는 주장에는 숫자가 약간 모자란다

두 번째 주장은 ripgrep이 Unicode를 지원하면서도 큰 대가를 치르지
않는다는 것이다.
`linux_unicode_word`에서 Unicode 인식 `rg (ignore)`는 0.355, ASCII는 0.329로
정말 차이가 작다.
그러나 패턴에 리터럴이 없는 항목에서는 대가가 보인다.
`linux_no_literal`에서 `rg (ignore)`는 0.577, ASCII는 0.416이다.
이 값으로 계산하면 Unicode 쪽이 약 39% 느리다.
저자는 이 차이를 about a 0.3x penalty라고 쓰는데,
같은 항목의 허용 목록 값(0.503과 0.343)으로 계산하면 약 47%다.
두 계산은 이 문서가 원문의 숫자로 직접 한 것이다.

러시아어 `subtitles_no_literal`에서는 `rg`가 4.905,
`rg (ASCII)`가 3.973으로 약 23% 차이가 난다.
저자는 그 원인을 Unicode 쪽 DFA를 만드는 비용으로 짚는다.
ASCII 패턴은 NFA 상태가 약 250개인 반면 Unicode 패턴은 약 77,000개이기 때문이다.
같은 항목에서 git grep이 4.153에서 26.382로 약 6배 느려지는 것과 견주면
확실히 작다.
그러므로 두 번째 주장은 상대적으로는 성립하지만 대가가 없다는 의미로 읽으면
과장이다.

여기에 한 가지가 더 있다.
25개 벤치마크는 모두 시간만 보고하고 메모리 사용량은 보고하지 않는다.
저자는 출력을 메모리 버퍼에 모으는 방식이 2GB 파일에서 모든 줄이 매치될 때
메모리를 많이 쓴다고
스스로 인정하고, 공간, 시간, 정확성 중 둘만 고를 수 있다고 쓴다.
속도 비교에서 ripgrep이 지불한 공간 비용은 이 글의 측정 범위 밖에 있다.

### 세부 사실은 독자의 지적으로 고쳐졌고 일부는 남아 있다

Hacker News에서 minimax는 GNU grep이 쓰는 libc의 `memchr`가
SIMD 명령을 직접 쓰지 않는 표준 C 코드라는 글의 설명이 틀렸다고 지적했다.
glibc에는 x86-64용으로 직접 작성한 어셈블리 `memchr`가 있다는 것이다.[^minimax]
저자는 지적이 맞다고 인정했다.
그 어셈블리에서 AVX2를 찾지 못했고 프로파일에서도 보지 못했으므로
분석은 대체로 그대로라고 답하며 글을 고쳤다고 적었다.[^burntsushi-minimax]

이 문서가 읽은 현재 글에서는 그 부분이 AVX2를 쓰지 않는다는 표현으로
바뀌어 있다.
그러나 바로 뒤 문장은 지금도 그 C 코드가 xmm 레지스터를 쓰도록
자동 벡터화된다고 적는다.
minimax가 틀렸다고 지적한 설명과 같은 취지의 문장이 남아 있는 셈이다.
이 차이가 결론을 바꾸지는 않지만,
원인 분석을 하나하나 따라가며 읽는 독자는 이 지점의 서술을 그대로 믿기 어렵다.

## 인사이트

### 결과가 없다는 말의 의미가 기본값에 따라 달라진다

ripgrep의 기본값은 검색하지 않을 파일을 정한다.
`.gitignore`, 숨김 파일, 바이너리 파일이 그 대상이다.
저자는 이런 스마트한 기본값이 도구를 불투명(opaque)하게 만든다고 직접 쓴다.
모든 것을 검색해야 할 때 어떤 주문을 외워야 하는지 알기 어렵다는 것이다.

이 불투명함은 검색 결과가 비었을 때 문제가 된다.
매치가 없어서 비었는지, 아예 검색 대상에서 빠져서 비었는지 결과만으로는 알
수 없다.
글의 사례로 Universal Code Grep은 알려진 확장자만 검색하므로
`fs/jffs2/README.Locking`을 검색하지 않는다.
저자는 이를 존재 자체를 모르는 파일은 놓칠 수밖에 없는 문제,
즉 unknown unknowns라고 부른다.

따라서 결과가 없다는 사실을 근거로 무언가를 지우거나 안전하다고 판단할 때는
검색 범위를 넓혀 다시 확인해야 한다.
글에 따르면 `rg -uuu`는 `grep -a -r`과 비슷하게 모든 파일을 검색하고,
무시 규칙이 기대한 대로 적용되지 않으면 `--debug`로 확인할 수 있다.
이 확인을 건너뛰어도 되는지는 검색의 목적이 관련 있는 결과를 찾는 것인지,
없음을 증명하는 것인지에 달려 있다.

이 기본값을 둘러싼 논쟁은 같은 스레드에서 바로 나왔다.
bpchaps는 모두가 git을 쓰는 직업 프로그래머는 아니라며
`.gitignore`를 따르는 기본값은 또 하나의 함정이니 빼는 것을 권한다고
적었다.[^bpchaps]
저자는 기본값을 바꾸지 않겠다고 답했다.
The Silver Searcher가 좋은 기본값임을 보여 줬다고 보며,
모든 파일을 검색하려면 `alias rg="rg -u"`를 쓰면 된다는 것이다.
다만 이 기본값이 절충(trade-off)이라는 점은 인정했고,
자신의 프로젝트가 목표로 하는 바에는 이 기본값이 가장 맞는다고
덧붙였다.[^burntsushi-bpchaps]
다른 답글에서는 ripgrep이 결과의 관련성을 높이려고
기본 동작에서 성능을 일부 포기한다고도 말했다.[^burntsushi-sidlls]

### 최적화가 놓이는 층이 어떤 최적화를 가능하게 하는지 결정한다

inner literal 최적화가 검색 도구에 있어야 한다는 저자의 설명은
최적화의 위치가 라이브러리 경계에 따라 정해진다는 사례다.
정규식 엔진은 입력의 구조를 모르므로 리터럴을 찾아도 매치의 시작점을 알 수 없다.
검색 도구는 결과의 단위가 줄이라는 것을 알아서 줄 경계로 문제를 줄인다.

이 구조의 이면은 엔진을 교체하는 순간 도구 쪽 최적화도 함께 바뀐다는 점이다.
저자는 PCRE를 쓰는 The Silver Searcher와 Universal Code Grep이 이 최적화를 하지
않는다고 쓴다.
엔진과 검색 도구가 한 덩어리인 GNU grep은 이 최적화를 하고,
ripgrep은 `regex-syntax`라는 파서 라이브러리 덕분에 비교적 쉽게 구현했다고 한다.
저자는 엔진 안에서 이를 일반적으로 해결하는 방법을 아직 찾지 못했고,
리터럴 앞뒤 부분을 거꾸로, 앞으로 따로 돌리면 최악의 경우 이차 시간이 든다고
설명한다.

여기서 읽을 수 있는 설계 교훈은 라이브러리를 나눌 때
어떤 최적화가 어느 쪽 정보를 필요로 하는지를 먼저 따져야 한다는 것이다.
엔진에 넣으려는 최적화가 사실은 호출자만 아는 정보에 의존한다면
엔진의 인터페이스에 그 정보를 전달할 방법이 있어야 한다.
`regex-syntax`처럼 파서를 노출하는 것은 그 방법의 하나다.

### 이 벤치마크의 결론을 가져다 쓰려면 자기 환경에서 다시 재야 한다

같은 비교가 EC2와 저자의 로컬 머신에서 다르게 나온 것이 이 글의 가장
실용적인 정보다.
`linux_literal`에서 `rg (ignore)`와 `rg (ignore) (mmap)`의 비율은
EC2에서 0.334 대 1.611로 약 4.8배, 로컬에서 0.156 대 0.397로 약 2.5배다.
`ag (ignore) (mmap)`과의 거리도 로컬에서 좁혀졌다.
저자는 가상 머신이 memory map의 성능을 떨어뜨렸을 수 있다고 추정한다.

따라서 memory map을 쓰지 말라는 결론을 자기 도구에 그대로 옮기면 안 된다.
ripgrep 자신도 파일 수에 따라 방식을 바꾸는 경험적 선택을 한다.
이 글이 남긴 방법은 직접 재 보는 것이다.
`benchsuite`는 `--allow-missing`으로 없는 도구를 건너뛰고,
`--raw`로 모든 측정값을 파일에 남길 수 있다.

같은 스레드에 이 결론을 뒷받침하는 사례가 있다.
atombender는 맥에서 큰 JSON 파일을 검색해
기본 설정의 `rg`가 3초 남짓 걸리는데 `--no-mmap`을 주면 1.7초 안팎으로 줄었다고
보고했다.[^atombender]
저자는 이 결과를 보고 맥에서는 `--no-mmap`을 기본값으로 바꾸겠다고 답하며
이슈를 열었다.[^burntsushi-atombender]
저자 자신의 맥에서도 1.2GB 파일 하나를 검색할 때
memory map을 쓰지 않는 쪽이 빨랐고,
같은 파일을 Linux에서 재면 반대로 memory map을 쓰는 쪽이
빨랐다.[^burntsushi-lobster_johnson]
글의 본문이 단일 파일에는 memory map이 낫다고 한 결론이
운영체제에 따라 뒤집힌 것이다.

Lobste.rs에서 mempko는 SSD와 HDD에서 알고리즘이 달라질지,
SSD의 기본 블록 크기에 맞춰 버퍼링하는 것이 맞을지 물었다.[^mempko]
저자는 디스크 I/O를 대체로 무시했다고 답했다.
명령마다 예열을 세 번 돌리고, 코퍼스가 메모리에 다 들어가는 머신에서 재서
디스크를 거치지 않게 했다는 것이다.
디스크에서 읽어야 한다면 도구 사이의 차이가 크지 않을 것이라는 직감이 있었는데,
그날 그 가정이 틀렸다는 말을 들었다고도 덧붙였다.[^inactive-user-mempko]
이 글의 모든 측정은 파일이 이미 페이지 캐시에 올라간 상태를 전제한다.
처음 읽는 파일이 많은 상황의 순위는 이 글만으로는 알 수 없다.

결정 규칙은 단순하다.
자기 코퍼스와 닮은 데이터에서 같은 패턴을 재고,
결과가 저자의 순위와 다르면 먼저 가상화와 파일 수, 파일 크기를 의심한다.
저자가 재현 가능한 이슈를 요청한 것도 같은 이유다.

## 관련 문서

- [tgrep](tgrep.md)
- [fzf](fzf.md)
- [Grep vs Vector Agentic Search](../llm/grep-vs-vector-agentic-search.md)

---

[^ggreer]: <https://news.ycombinator.com/item?id=12567328>

[^burntsushi-ggreer]: <https://news.ycombinator.com/item?id=12567484>

[^rob_cameron]: <https://news.ycombinator.com/item?id=12586928>

[^burntsushi-rob_cameron]: <https://news.ycombinator.com/item?id=12591086>

[^rob_cameron-reply]: <https://news.ycombinator.com/item?id=12599594>

[^burntsushi-rob_cameron-reply]: <https://news.ycombinator.com/item?id=12601158>

[^glangdale]: <https://news.ycombinator.com/item?id=12579686>

[^burntsushi-glangdale]: <https://news.ycombinator.com/item?id=12583859>

[^bodyfour]: <https://news.ycombinator.com/item?id=12566063>

[^burntsushi-bodyfour]: <https://news.ycombinator.com/item?id=12567573>

[^lobster_johnson]: <https://news.ycombinator.com/item?id=12567326>

[^atombender]: <https://news.ycombinator.com/item?id=12567944>

[^burntsushi-atombender]: <https://news.ycombinator.com/item?id=12568005>

[^burntsushi-lobster_johnson]: <https://news.ycombinator.com/item?id=12567901>

[^minimax]: <https://news.ycombinator.com/item?id=12566138>

[^burntsushi-minimax]: <https://news.ycombinator.com/item?id=12567516>

[^bpchaps]: <https://news.ycombinator.com/item?id=12569211>

[^burntsushi-bpchaps]: <https://news.ycombinator.com/item?id=12569277>

[^burntsushi-sidlls]: <https://news.ycombinator.com/item?id=12567770>

[^LenFalken]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_dtuvxx>

[^inactive-user-lenfalken]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_qzuazo>

[^hoodie]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_ypzsqm>

[^inactive-user-hoodie]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_nvkcva>

[^cgag]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_thokd5>

[^cmm]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_rnnmmc>

[^mempko]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_enfyf1>

[^inactive-user-mempko]: <https://lobste.rs/s/melmzg/ripgrep_is_faster_than_grep_ag_git_grep_ucg#c_dzabck>
