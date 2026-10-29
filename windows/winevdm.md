# winevdm: 64비트 Windows에서 16비트 Windows 프로그램을 돌리는 에뮬레이터

<https://github.com/otya128/winevdm>

HN 토론: <https://news.ycombinator.com/item?id=50253529> (147점, 34개 댓글)

GN 토론: <https://news.hada.io/topic?id=36187>

## 소개

winevdm은 16비트 Windows(Windows 1.x, 2.x, 3.0, 3.1 등)를 64비트 Windows에서
실행하는 에뮬레이터이다.
README는 Wine의 winevdm(16비트 Windows 에뮬레이터)을 64비트 Windows로 옮기며
고친 판이라고 소개한다.
실행 파일 이름은 `otvdm.exe`와 `otvdmw.exe`이다.

GitHub API로 읽은 시점의 값은 별 3,620개, 포크 209개, 열린 이슈 352개(열린 풀
리퀘스트 포함), 주 언어 C, 라이선스 GPL-2.0이다.
저장소는 2015년 9월 22일에 만들어졌고 마지막 푸시는 2026년 10월 24일이다.
최근 안정 릴리스는 2023년 9월 15일의 v0.9.0이고,
최신 개발 버전(불안정)은 AppVeyor
빌드로 받는다고 README가 안내한다.

이 문서는 README와 저장소 파일 목록, 릴리스 정보를 읽고 썼다.
프로그램을 직접 실행해 보지는 않았다.
아래 명령은 README에 적힌 대로 옮겼고 이 문서가 실행해 본 것이 아니다.

## 동작 방식

### 64비트 Windows가 16비트 프로그램을 거부하는 이유

README는 CPU 에뮬레이터가 필요한 이유를 한 줄로 적는다.
64비트 Windows에서는 LDT(Local Descriptor Table)를 바꿀 수 없다는 것이다.
`NtSetInformationProcess`의 `ProcessLdtInformation`을 호출하면 항상 오류가
돌아온다고 한다.
이 문서의 이해로는 16비트 프로그램이 세그먼트 주소 방식을 쓰기 때문에
LDT를 바꾸지 못하면 CPU가 직접 실행할 수 없고,
그래서 이 프로젝트가 명령어를 소프트웨어로 해석하는 것으로 읽힌다.
README는 이 연결을 한 줄로만 적는다.

HN에서 my123은 Microsoft의 문서를 인용해 다른 이유를 보탰다.
64비트 Windows의 핸들은 유효한 비트가 32비트라서 16비트 프로그램에 넘길
때 정보 손실
없이 줄일 수 없고, 그래서 16비트 프로그램을 실행하려 하면 `ERROR_BAD_EXE_FORMAT`
오류가 난다는 내용이다.[^my123]
이 문서는 Microsoft 문서 원문을 열어 보지 못했다.

### 16비트 호출을 32비트 호출로 바꾸는 계층

프로젝트의 구성은 README가 네 가지로 적는다.

| 구성 요소                     | 하는 일                                                   |
| ----------------------------- | --------------------------------------------------------- |
| CPU 에뮬레이터                | LDT를 바꿀 수 없는 환경에서 16비트 코드를 해석해 실행한다 |
| Wine 기반 Win16→Win32 변환    | 16비트 API 호출을 같은 일을 하는 32비트 호출로 바꾼다     |
| Win16용 DOS 에뮬레이션        | DOS 호출을 처리한다                                       |
| 16비트와 네이티브 HANDLE 변환 | 16비트 핸들과 64비트 Windows의 핸들 값을 서로 대응시킨다  |

변환 코드는 README가 보인 예에서 단순하다.
`DestroyWindow16`은 16비트 핸들을 32비트 핸들로 바꿔 `DestroyWindow`를
부르고 결과를
돌려준다.
16비트에서 32비트로 건너가는 중계 루틴은 `convspec` 도구가 spec
파일에서 자동으로
만든다.
vintagedave는 HN에서 핸들을 매핑 표로 바꾸면 되지 않느냐고 물었고,
README의 `WIN_Handle32`가 바로 그런 일을 하는 것으로 읽힌다고
했다.[^vintagedave]
my123은 그런 매핑을 시도했지만 잘 되지 않았다는 글을 가리켰다.[^my123-mapping]
이 문서는 그 글을 열어 보지 못했다.

### 설치 프로그램과 설정 파일 처리

64비트 Windows는 16비트 설치 프로그램을 발견하면 16비트가 아닌 대체
설치 프로그램을
시작하는 메커니즘을 갖고 있고, 이 프로그램은 그 장치를 쓴다고 README가 설명한다.
이 장치 덕분에 `install.inf`를 설치해 두면 Win16 바이너리를 바로 실행할 수 있다.

일부 Win16 프로그램은 설정을 `%WINDIR%\<파일 이름>.ini`에 저장하려 하는데,
최근 Windows는 `%WINDIR%`에 쓰기를 허용하지 않으므로 이 프로그램이 경로를 대신
돌려 준다.

## 설치하고 실행하기

README의 순서는 다음과 같다.

1. 안정 버전을 릴리스 페이지에서 받는다(최신 개발 버전은 AppVeyor).
2. `VCRUNTIME140.dll`이 없다는 오류가 나면 Visual Studio 2017용 Microsoft Visual C++
   재배포 가능 패키지(32비트)를 설치한다.
3. Win16 실행 파일을 `otvdm.exe`에 끌어다 놓거나 `otvdmw.exe`를 실행한다.
4. 직접 실행하고 싶으면 내려받은 폴더에서 `install` 바로가기를 실행하거나
   `install.inf`를 오른쪽 버튼으로 눌러 설치한다.
5. Windows Update가 레지스트리를 초기화했다면 4번을 다시 한다.
6. 지우려면 `uninstall.reg`를 실행한다.
7. 설정은 `otvdm.ini`에서 바꾼다.

소스에서 빌드하는 방법은 두 가지이고, Visual Studio 2017에서는
`PropertySheet.props`를 고치고 컴파일하며, cmake는 아래 명령이다.

```sh
git clone https://github.com/otya128/winevdm.git
cd winevdm
mkdir build
cd build
cmake ..
make
```

DOS 실행 파일도 `winevdm.exe`로 돌릴 수 있다.
`winevdm.exe [--app-name app.exe] 명령줄` 형식이고
`VDMDOSVER` 환경 변수로 DOS 버전을 정한다.
README는 DOS 에뮬레이션이 불완전하므로 DOSBox나 MS-DOS Player를 권한다.

## 함정

### 어느 압축 파일을 쓸지가 README에 없다

릴리스에는 `otvdm-v0.9.0.zip` 하나가 있고,
v0.8.1에는 `otvdm-for-old-windows-v0.8.1.zip`이 따로 있었다.
어떤 Windows 버전에 어느 압축 파일을 쓰는지는 README에 적혀 있지 않다.
이 문서는 이 구분을 확인하지 못했다.
설치 전에 릴리스 페이지의 설명을 읽어야 한다.

### 호환성의 범위는 README가 보장하지 않는다

README는 프로그램이 지원하는 Windows 버전(1.x부터 3.1까지)을 적지만
어떤 프로그램이 되는지의 목록은 없다.
HN에서 haunter는 몇 달 전 이것으로 MS Office 2.0을 설치해 일주일 쓴
경험에서 사전
파일을 인식하지 못하는 문제를 빼면 꽤 잘 돌았다고 했고,
현대 워드 프로세서가 그 파일을 열 수 있었다고 했다.[^haunter]
NetMageSCW는 Fluke의 16비트 프로그램으로 전압 이벤트 기록기와
통신하는 데 몇 년째
otvdm을 쓴다고 했다.[^NetMageSCW]
이 두 사례는 성공의 증언이지 보장이 아니다.
README의 호환성 수정이 어떤 범위를 다루는지는 이 문서가 확인하지 못했다.

### 16비트 파일 형식의 보안 위험을 에뮬레이터가 줄이지 않는다

haunter는 오래된 16비트 파일 형식이 어느 정도 공격에 취약할 것 같다고
추측했다.[^haunter-security]
pjmlp는 문서를 종이로 보낼 용도로 혼자 쓰는 경우라면 걱정이 적지만 파일을 남과
공유하면 별개의 문제라고 답했다.[^pjmlp]
이 에뮬레이터가 프로그램을 샌드박스에 넣는지는 README에 없다.
ale42는 이것이 가상 머신이 아니라고 짚었다.[^ale42]
따라서 신뢰할 수 없는 16비트 파일은 이 도구로 열기 전에 격리된 환경에서 먼저
다루는 것이 안전하다.
이 판단은 이 문서의 것이고 도구의 보안 모델을 확인한 결과가 아니다.

## 확인하기

아래 순서로 작은 프로그램 하나로 직접 시험할 수 있다.
이 문서가 실행하지 못한 절차이므로 환경에 따라 결과가 다를 수 있다.

1. 릴리스에서 `otvdm-v0.9.0.zip`을 받아 새 폴더에 푼다.
2. 64비트 Windows에서 16비트 실행 파일(예: 계산기 `CALC.EXE`)을 `otvdm.exe`에
   끌어다 놓는다.
3. 실행된다면 `winevdm.exe CALC.EXE`로도 같은 결과가 나오는지 본다.
4. 설정을 `%WINDIR%` 아래에 저장하는 프로그램이 있다면, 설정이 저장되는 위치를 확인한다.
5. `install.inf`를 설치한 뒤 같은 파일을 더블 클릭으로 실행해 본다.
6. 지울 때 `uninstall.reg`를 실행하고 더블 클릭 실행이 막히는지 확인한다.

## 체크리스트

- 열려는 16비트 파일을 신뢰할 수 있는가?
- 이 도구가 샌드박스가 아니라는 점을 알고 격리된 환경에서 쓰고 있는가?
- `VCRUNTIME140.dll` 오류 때 32비트 재배포 패키지를 설치했는가?
- Windows Update 뒤에 더블 클릭 실행이 안 되면 설치 절차를 다시 했는가?
- DOS 프로그램이라면 DOSBox나 MS-DOS Player를 먼저 고려했는가?
- 필요한 프로그램의 호환성을 설치 전에 작은 파일 하나로 시험했는가?

## 기억할 원칙

### 하위 호환성의 비용은 한쪽이 지지 않으면 다른 쪽이 진다

HN에서 londons_explore는 Microsoft가 64비트 Windows를 낼 때 이런
계층을 만들지 않은
것을 이해하기 어렵다고 썼다.
그는 16비트 Windows가 복잡하지 않았고 단순한 가상 머신과 API 변환
계층으로 30년 넘는
호환성을 유지할 수 있었을 것이라고 했다.[^londons_explore]
mike_hearn은 64비트 Windows가 나왔을 때 16비트로 돌아가는 것은 다시는
갱신되지 않을
기계뿐이라 만들 이유가 없었다고 반박했고,[^mike_hearn]
xacky는 30년 방치된 소프트웨어를 지원하는 데는 상업적 가치가 거의 없다고
했다.[^xacky]
이 논쟁의 결론은 이 문서가 내리지 못한다.
그러나 이 프로젝트가 존재한다는 사실 자체가 한 가지를 보여 준다.
공식 지원을 끊어도 필요한 사람은 개인이 만들고, 그 비용은 사용자가 설치 절차와
호환성 시험으로 치른다.

### 오래된 설치 프로그램이 오래된 프로그램보다 더 흔한 이유일 수 있다

da_chicken은 16비트 프로그램 중 가장 많이 쓰이는 것이 `setup.exe`나
`install.exe`였다고
썼다.
오랫동안 모든 소프트웨어가 16비트 설치 프로그램으로 배포되었으므로
2005년 소프트웨어도 설치 프로그램은 16비트인 경우가 있다는 것이다.[^da_chicken]
masfuerte는 Microsoft가 16비트 설치 프로그램을 권한 이유가 비 Intel 계열
Windows NT에서
에뮬레이션으로 돌릴 수 있었기 때문이라고 설명했다.[^masfuerte]
이 문서의 해석으로는 16비트 에뮬레이터가 필요한 순간이 16비트 프로그램을 쓰고
싶을 때가 아니라 32비트 프로그램을 설치하려 할 때일 수 있다.
`install.inf`가 16비트 설치 프로그램을 가로채는 기능을 갖춘 이유가 이것과 맞닿아
있는지는 README에 적혀 있지 않다.

---

[^my123]: <https://news.ycombinator.com/item?id=50256062>

[^vintagedave]: <https://news.ycombinator.com/item?id=50257847>

[^my123-mapping]: <https://news.ycombinator.com/item?id=50268307>

[^haunter]: <https://news.ycombinator.com/item?id=50255484>

[^NetMageSCW]: <https://news.ycombinator.com/item?id=50267668>

[^haunter-security]: <https://news.ycombinator.com/item?id=50255832>

[^pjmlp]: <https://news.ycombinator.com/item?id=50255882>

[^ale42]: <https://news.ycombinator.com/item?id=50257544>

[^londons_explore]: <https://news.ycombinator.com/item?id=50255937>

[^mike_hearn]: <https://news.ycombinator.com/item?id=50256161>

[^xacky]: <https://news.ycombinator.com/item?id=50257190>

[^da_chicken]: <https://news.ycombinator.com/item?id=50256470>

[^masfuerte]: <https://news.ycombinator.com/item?id=50267620>
