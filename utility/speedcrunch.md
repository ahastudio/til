# SpeedCrunch 1.1: 50자리 정밀도의 키보드 중심 과학 계산기

<https://www.speedcrunch.org/>

HN 토론: <https://news.ycombinator.com/item?id=50224210> (203점, 42개 댓글)

GN 토론: <https://news.hada.io/topic?id=35966>

## 소개

SpeedCrunch는 무료 오픈소스 고정밀 과학 계산기다.
STEM 전문가와 학생, 교사를 대상으로 하며 Windows, macOS, Linux에서 쓸 수 있다.
최대 50자리 정밀도와 복소수를 지원하고, 함수 140개 이상과 단위, 상수를 갖췄다.
변수와 함수, 단위를 직접 정의할 수 있고, 벡터와 행렬도 다룬다.
이전 수식을 고쳐 다시 계산하는 히스토리 재작성과 결과별 설정이 있다.
키패드 프리셋과 탭, 패널, 창으로 나누는 여러 세션, 40개 이상의 번역과 색
구성표도 있다.

매뉴얼 소개 페이지는 이 계산기가 문법이 강조되는 스크롤 화면을 가졌고
키보드만으로 쓰도록 설계됐다고 설명한다.[^manual]
함수와 변수의 자동 완성, 공식집, 여러 분야의 상수를 빠르게 넣는 기능이
두드러진다고 한다.[^manual]

## 1.1에서 바뀐 것

다운로드 페이지의 변경 내역은 1.1을 기능 추가보다 다듬기와 되살리기에 가깝게
보여 준다.[^download]
항목이 많아서 쓰는 방식에 영향이 큰 것만 추린다.

수식 입력 쪽에서는 `root(n; x)`가 추가됐다.
음수와 단위가 붙은 양도 n제곱근을 구할 수 있고, 예로 `root(5; -32)`는 `-2`를
돌려준다.[^download]
`Ctrl+Space`로 이름이나 단위를 검색해 상수를 넣을 수 있고, 사용자 정의 함수 안의
계승이 고쳐졌다.[^download]
입력 중 연산자 교체나 닫는 괄호 같은 자동 보정을 끄는 옵션도 생겼다.[^download]

세션 쪽에서는 닫을 때 내용이 사라지고 다음 실행에서 복원되지 않는 비공개 탭이
들어왔다.
`Ctrl+Shift+N`(macOS는 `Cmd+Shift+N`)으로 연다.[^download]
설정을 모두 초기화하되 세션과 히스토리, 사용자 정의는 남기는 메뉴도
있다.[^download]

화면 쪽에서는 입력과 결과의 간결한 Classic 배치가 추가됐고, Modern이 기본으로
남는다.[^download]
메뉴와 패널, 상태 표시줄에 시스템 테마와 SpeedCrunch 테마를 따로 고를 수
있다.[^download]
macOS에서는 설정과 세션을 앱 옆의 `SpeedCrunch-data` 폴더에 두는 포터블 ZIP이
생겼다.[^download]

1.0은 그 앞에서 탭과 분할 패널, 히스토리 저장, 리스트와 행렬, 새 함수 수십 개를
넣은 큰 개편이었다.[^download]
기여자 목록은 2016년 11월 30일 이후의 기여를 기준으로 한다고 적혀
있다.[^download]

## 비평

### 변경 내역에 없는 수정을 댓글이 먼저 알렸다

HN에서 unanimous는 이번 릴리스에서 연산 순서 버그가 고쳐져 `1/2(-9.8)`이
`-4.9`로 계산된다고 적었다.[^unanimous]
이전에는 `-0.05102040816326530612`가 나왔고, 지금은 식이 `1 / 2 × (−9.8)`로 다시
표시돼 곱셈이 눈에 보인다고 했다.[^unanimous]
1.1 변경 내역에는 이 수정이 적혀 있지 않았다.
1.0 내역의 해석된 식을 곱셈 기호까지 보여 준다는 항목이 표시 쪽의 근거로는
보이지만, 계산 순서가 바뀐 사실은 확인할 수 없다.

이 식을 어떻게 읽어야 하는지는 댓글에서도 갈렸다.
dataflow는 이런 식은 계산하지 않고 오류를 내야 한다고 했고,[^dataflow] Jaxkr는
연산 순서를 두고 논쟁을 벌이는 소셜 미디어 글처럼 모호한 식이라고 했다.[^Jaxkr]
계산기가 모호한 식에 답을 내는 것이 서비스인지 위험인지에 대한 합의가 없고, 변경
내역은 어느 쪽인지도 밝히지 않는다.

girvo는 과학 계산기가 올바르게 만들기 어렵다고 하면서 SpeedCrunch도 최근 계산
오류를 고쳤다고 했다.[^girvo]
단위 변환 수정 목록(뮤온, 양성자, 중성자의 에너지 환산, `J/m²`와 `J/m³`)이 변경
내역에 길게 실려 있는 것도 같은 방향을 가리킨다.[^download]
정밀도를 내세우는 도구에서 결과가 틀렸다는 보고는 쉽게 넘길 수 있는 것이 아니다.

### 새 화면에 대한 호불호는 선택 가능한 설정으로 풀렸는가

Gormo는 오랫동안 0.12를 써 왔고, 새 버전에서 입력 상자가 불필요하게 두 배로
커지고 테두리와 여백이 생겼으며 입력 지연이 생겼다고 적었다.[^Gormo]
버그도 빠진 기능도 없던 소프트웨어가 개선하려다 나빠졌다는 불만이다.
academicfish는 마음에 들고, 예전 보기로 돌아가는 옵션도 있다고
답했다.[^academicfish]
변경 내역의 Classic 배치가 이 옵션으로 보인다.[^download]

그러나 입력 지연은 배치 옵션으로 풀리는 문제가 아니다.
Gormo가 말한 지연이 어떤 환경에서 생기는지는 댓글에서 확인되지 않았다.
1.1이 시작과 세션 복원 지연을 줄였다는 항목이 있지만, 입력 지연과 같은
문제인지는 알 수 없다.[^download]

eviks는 필요 없으면 옛 버전을 쓰면 되고 이 앱에도 일부 플랫폼의 흐릿한 글자 같은
버그가 있다고 답했다.[^eviks]
옛 버전을 쓰라는 조언은 맞지만, 새 설치 파일이 기본으로 Modern을 내미는 이상
불만이 나올 수밖에 없다.

### 숫자 표시와 기능 범위는 쓰는 사람마다 다르다

terlisimo는 SpeedCrunch가 지수 표기로 넘어가기 전의 자릿수가 5자리로 고정돼 있어
셸 스크립트와 프로그래밍에 쓰기 어려웠다고 적었다.[^terlisimo]
이슈를 열었을 때 의도한 동작이라는 답을 받았고, 직접 `expd > 5`를 `expd > 25`로
바꿔 빌드해 썼다고 한다.[^terlisimo]
지금은 14자리로 늘었다고 봤지만, 이 문서는 그 변경을 변경 내역에서 확인하지
못했다.[^terlisimo]

Surac은 소수 판별, 다음 소수, 소인수분해 함수가 없는 것을 아쉬워했다.[^Surac]
1.0 내역의 정수 함수는 `powmod`, `emod`, `lcm`, `popcount`이고 소수 관련 함수는
없다.[^download]
홈페이지의 함수 140개 이상이라는 숫자는 그 범위를 말해 주지 않는다.

## 인사이트

### 오래 쓰던 도구가 갱신될 때 지켜야 하는 것

andix는 1.0과 1.1이 10년 만의 첫 업데이트들이 아니냐고 물었고,[^andix] 기여자
목록은 2016년 11월 30일 이후를 기준으로 하니 대략 맞는 이야기다.[^download]
Gormo의 댓글이 보여 주듯 10년 동안 같은 모습으로 쓰던 도구가 바뀌면 사용자는
개선보다 달라진 점을 먼저 본다.[^Gormo]
이런 도구를 갱신하는 쪽의 결정 규칙은 단순하다.
기본값을 새 배치로 바꾸더라도 예전 배치로 돌아가는 방법을 같은 릴리스에 넣고,
계산 결과가 달라지는 수정은 변경 내역에 적는다.
1.1은 앞의 것은 했지만, 뒤의 것은 변경 내역에서 확인되지 않는다.

### 계산기 선택은 입력 방식과 단위 처리가 가른다

jiehong은 예전에 SpeedCrunch를 많이 썼지만 지금은 numbat을 쓴다고
했고,[^jiehong] faldor20도 numbat으로 옮겼다고 했다.[^faldor20]
faldor20이 든 이유는 단위를 즉석에서 정의하기 쉽고, 단위를 쓰면 단순 계산 실수가
많이 줄어든다는 것이다.[^faldor20]
wiz21c는 qalculate를 많이 쓴다고 했고 화면은 평범하지만 아주 강력하다고
했다.[^wiz21c]
SpeedCrunch의 강점은 borner791이 말한 비트 이동과 진법 변환처럼 빠른 키보드
입력과 계산 과정의 가시성이다.[^borner791]
smusamashah도 비트와 비트 이동 연산을 눈으로 보려고 거의 매일 쓴다고
했다.[^smusamashah]
선택 기준은 정밀도가 아니라, 단위를 중심으로 계산하는지 수식 입력의 속도를
중심으로 하는지에 가깝다.

### 이 글을 읽는 방법

이 페이지는 프로젝트가 자기 릴리스를 소개하는 글이므로, 변경 내역은 확인된
사실이고 사용 경험에 대한 평가는 아직 확인되지 않았다.
댓글의 사용 보고는 소수의 사람이 쓴 것이고, 입력 지연과 5자리 한계 같은 주장은
이 문서에서 재현하지 못했다.

이 판단을 가를 관찰은 두 가지다.
첫째, `1/2(-9.8)` 같은 식을 1.0과 1.1에서 각각 입력해 결과를 비교하고, 같은 식이
변경 내역에 적혀 있는지 보는 것이다.
둘째, Gormo가 말한 입력 지연을 Modern과 Classic 배치에서 같은 환경으로 측정하는
것이다.
첫째는 계산 결과가 바뀐 사실이 공지됐는지를, 둘째는 불만이 배치의 문제인지
구현의 문제인지를 가른다.

---

[^manual]: SpeedCrunch, [Introduction — SpeedCrunch Manual](https://www.speedcrunch.org/introduction.html)

[^download]: SpeedCrunch, [Download SpeedCrunch for Windows, macOS and Linux](https://www.speedcrunch.org/download.html)

[^unanimous]: <https://news.ycombinator.com/item?id=50226148>

[^dataflow]: <https://news.ycombinator.com/item?id=50226195>

[^Jaxkr]: <https://news.ycombinator.com/item?id=50226875>

[^girvo]: <https://news.ycombinator.com/item?id=50226287>

[^Gormo]: <https://news.ycombinator.com/item?id=50227880>

[^academicfish]: <https://news.ycombinator.com/item?id=50228414>

[^eviks]: <https://news.ycombinator.com/item?id=50228541>

[^terlisimo]: <https://news.ycombinator.com/item?id=50230774>

[^Surac]: <https://news.ycombinator.com/item?id=50233221>

[^andix]: <https://news.ycombinator.com/item?id=50227712>

[^jiehong]: <https://news.ycombinator.com/item?id=50225240>

[^faldor20]: <https://news.ycombinator.com/item?id=50231532>

[^wiz21c]: <https://news.ycombinator.com/item?id=50230934>

[^borner791]: <https://news.ycombinator.com/item?id=50225787>

[^smusamashah]: <https://news.ycombinator.com/item?id=50226084>
