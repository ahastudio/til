# Windows 11에서 돌아가는 가장 오래된 GUI 프로그램은 1992년의 CD 플레이어다

원문: [Oldest GUI application that still runs on Windows 11](https://blog.enlyth.com/posts/oldest-windows-gui-app-win-11/)

HN 토론: <https://news.ycombinator.com/item?id=50248055> (461점, 273개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/rwubks/oldest_gui_application_still_runs_on> (46점, 5개 댓글)

GN 토론: <https://news.hada.io/topic?id=36065>

## 요약

저자는 수정도 에뮬레이션도 없이 Windows 11에서 실행되는 GUI 프로그램 가운데 가장 오래된 것이 무엇인지 찾았다.
64비트 Windows에는 NTVDM이 없어 16비트 Windows 프로그램은 실행할 수 없으므로, 후보는 초기 NT 시대의 32비트 프로그램으로 좁혀진다.

첫 번째 답은 Win32s 초기 배포판에 들어 있던 FREECELL.EXE다.
수정 날짜가 1993년 2월 22일인 이 파일이 최신 Windows 11에서 아무 변경 없이 끝까지 플레이된다.
글이 쓰인 시점 기준으로 33년 8개월 된 프로그램이다.

저자는 여기서 멈추지 않고 Internet Archive의 NT 3.1 사전 배포 빌드를 뒤졌다.
1991년 빌드는 초안 단계의 PE 포맷을 쓰고, 1992년 중반까지의 빌드는 Windows API 호출에 stdcall이 아니라 cdecl을 가정한다.
cdecl 호출자는 인자를 직접 치우는데 현재의 ShowWindow는 `ret 4`로 스스로 치우므로, 스택이 두 번 정리되어 프로그램이 죽는다.

이 장벽을 넘은 것이 Build 347의 CDPLAYER.EXE다.
1992년 11월 16일에 링크된 이 파일은 같은 빌드의 다른 프로그램이 죽는 번들 C 런타임 대신 시스템의 `crtdll.dll`을 쓰고, Windows 11은 SysWOW64에 이 DLL을 지금도 싣고 있다.
CD-ROM 드라이브가 없으면 오류가 나므로, 저자는 가짜 오디오를 내는 작은 DLL(`cdemu.dll`)로 드라이브를 흉내 내어 재생까지 확인했다.
마지막으로 otvdm을 쓰면 Windows 1.01의 1985년 11월 15일자 REVERSI.EXE도 돌아가지만, 저자는 이를 반칙으로 여겨 기록에서 뺐다.

## 분석

### 후보는 세 개이고, 각각 다른 조건을 만족한다

글이 내놓은 세 후보를 같은 잣대로 놓으면 다음과 같다.

| 프로그램     | 날짜            | 추가로 필요한 것          | Windows 11에서의 상태         |
| ------------ | --------------- | ------------------------- | ----------------------------- |
| FREECELL.EXE | 1993-02-22      | 없음                      | 끝까지 플레이할 수 있음       |
| CDPLAYER.EXE | 1992-11-16 링크 | 가짜 CD 드라이브 DLL      | 실행되고 가짜 오디오가 재생됨 |
| REVERSI.EXE  | 1985-11-15      | otvdm (16비트 에뮬레이터) | 끝까지 플레이할 수 있음       |

표를 보면 날짜가 오래될수록 조건이 하나씩 더 붙는다는 점이 드러난다.
FREECELL은 조건 없이 돌아가고, CDPLAYER는 장치를 가짜로 채워야 하고, REVERSI는 실행 환경 자체를 얹어야 한다.
저자의 기준은 “더블클릭으로 바로 돌아가는 것”이고, 저자는 HN 댓글에서 이 기준을 직접 밝혔다.
Windows 11에는 32비트 판이 없고 NTVDM을 실은 마지막 Windows가 Windows 10 32비트였기 때문에, 서드파티 도구는 반칙으로 정했다고 한다.[^enlyth]

### 1992년 중반이 호환성의 단층선이다

글에서 가장 기술적인 대목은 어째서 1992년 중반 이전의 NT 빌드가 전멸하는가이다.
글이 보인 어셈블리는 호출자가 인자를 밀어 넣고 API를 부른 뒤, 자기도 스택을 한 번 더 치우는 모양이다.

```asm
push hwnd          ; 4 bytes of args
call [ShowWindow]  ; Win11 ShowWindow is stdcall, ends with "ret 4" and removes them
add  esp, 4        ; the 1992 caller removes them again
```

stdcall에서는 피호출자가 인자를 치우고 cdecl에서는 호출자가 치운다.
호출 규약이 개발 도중에 바뀌었으므로, 그 전에 링크된 바이너리는 호출 한 번마다 스택 포인터를 4바이트씩 어긋나게 만든다.
저자의 설명대로라면 1991년 빌드는 포맷부터 맞지 않고, 1992년 중반까지의 빌드는 포맷은 맞아도 호출 규약이 맞지 않는다.
그래서 “얼마나 오래된 파일인가”가 아니라 “개발 중 어느 시점에 링크되었는가”가 호환 여부를 정한다.

### 같은 빌드에서도 하나만 살아남은 이유는 런타임이다

Build 347에는 호출 규약이 이미 고정되어 있었다.
그런데도 그 빌드의 다른 프로그램은 번들된 C 런타임 안에서 죽고, CDPLAYER.EXE만 시스템 `crtdll.dll`을 써서 산다.
호환성의 경계가 운영체제 커널이나 API 표면에만 있는 것이 아니라, 각 프로그램이 어떤 런타임을 링크했는지에도 걸려 있다는 뜻이다.
이 대목은 글이 직접 한 주장이고, `crtdll.dll`이 SysWOW64에 남아 있다는 사실도 저자의 서술이다.

## 비평

### 작동한다는 기준이 후보마다 다르게 쓰였다

FREECELL은 끝까지 플레이된다고 했으니 작동의 기준이 높다.
CDPLAYER는 창이 뜨고 가짜 DLL을 통해 가짜 오디오가 재생되는 수준이다.
이 둘을 한 줄로 세워 “더 오래된 쪽이 CDPLAYER”라고 읽으면, 실행된다는 말과 쓸 수 있다는 말이 섞인다.

HN에서 unleaded는 실제 광학 드라이브로 직접 시험했다.
디스크를 넣고 실행하면 CD-ROM 장치를 찾을 수 없다는 메시지가 뜨고, 디스크 없이 실행한 뒤 디스크를 넣으면 탐색기 쪽에서 이상한 오류가 났다.
RTM 판은 조금 더 나아가지만 역시 재생하지 못했고 재생 목록을 열면 죽었으며, 사전 배포 판은 트랙 목록까지 보였다고 한다.
unleaded는 플레이어가 드라이브를 독점하려다 Windows와 다투는 것 같다고 추정했다.[^unleaded]
이 시험이 맞다면 CDPLAYER의 “실행됨”은 가짜 드라이브를 끼운 조건에서만 성립하고, 실물 드라이브에서는 성립하지 않는다.
글이 이 한계를 숨긴 것은 아니지만, 제목의 “still runs”가 약속하는 범위보다 실제 근거가 좁다.

### 반칙의 경계선이 한쪽으로만 그어졌다

저자는 otvdm을 반칙으로 정하면서도 `cdemu.dll`은 같은 잣대로 따지지 않는다.
둘 다 프로그램 밖에서 환경을 채워 주는 외부 도구인데, 하나는 기록을 무효로 만들고 다른 하나는 기록을 세운다.
MisterTea는 NTVDM이 Windows의 일부였다면 서드파티 복제품도 공정하다고 보았다.[^MisterTea]
저자의 구분(운영체제와 함께 오는가)에는 일관된 근거가 있지만, 가짜 CD 드라이브가 그 구분 안에 어떻게 들어오는지는 글에 설명이 없다.

NTVDM이 사라진 이유에 대한 댓글도 이 경계를 흐리게 한다.
mattbee는 NTVDM이 CPU가 16비트 코드를 직접 실행하는 모드에 기댔기 때문에 64비트 Windows에서는 자연히 끝났고, winvdm은 CPU 에뮬레이션으로 이를 되살린다고 요약했다.[^mattbee]
그렇다면 otvdm은 옛 기능을 복원한 것이 아니라 다른 방식으로 다시 만든 것이어서, “공식 지원이 끊긴 것을 되살렸다”는 반칙의 의미가 더 복잡해진다.

### Win32s라는 맥락이 글에서 거의 지워졌다

글은 Win32s를 “익명 포럼에서 들은 힌트” 정도로만 다룬다.
HN 댓글에서 lproven은 FREECELL이 Win32s에 든 시연용 프로그램이었고 Win32s가 NT보다 앞서 나왔다는 점이 이미 알려진 사실이라고 했다.[^lproven]
fredoralive는 Win32s가 NT 3.1(1993)과 같은 시기에 나왔고 PE 실행 파일을 읽지 못하는 Windows 3.0이 아니라 3.1(1992) 이상을 필요로 하지만, 1991년 Microsoft Entertainment Pack 2에는 Windows 3.0에서 도는 16비트 판이 이미 있었다고 보탰다.[^fredoralive]
lproven은 이어서 Win32s 베타가 1992년 10월, NT 3.1이 1993년 7월이라고 적었다.[^lproven-oct]

이 날짜들이 맞다면 FREECELL의 1993-02-22라는 수정 날짜는 Win32s 계열의 “초기 배포판”이라는 표현이 가리키는 시점을 정확히 알려 주지 못한다.
저자가 말한 “초기 릴리스”가 어느 버전이고 그 안의 파일 날짜가 왜 1993년 2월인지는 글에서 확인되지 않는다.
그래서 FREECELL과 CDPLAYER 사이의 선후, 곧 이 글의 핵심 순위가 어느 날짜를 기준으로 하느냐에 따라 흔들릴 여지가 있다.

## 인사이트

### 호환성은 커널이 아니라 함께 출하되는 낡은 파일들에 산다

CDPLAYER가 산 이유는 호출 규약이 고정된 시점 이후에 링크되었고, 시스템 런타임을 빌려 썼기 때문이다.
이는 Windows가 오래된 프로그램을 지원하는 방식이 “옛 API를 계속 구현한다”에만 있지 않고, “옛 DLL을 계속 설치한다”에도 있음을 보여 준다.
kevin_thibedeau가 든 예가 이를 뒷받침한다.
ODBC 관리자는 Windows 11에도 그대로 들어 있고, Windows 3.0과 NT 3.5 시절의 대화상자와 16색 아이콘을 아직 쓴다고 한다.[^kevin_thibedeau]

여기서 파생되는 결과는 호환성이 한 번의 설계 결정이 아니라 누적된 파일 목록의 유지 관리라는 점이다.
파일 하나를 빼면 그 파일에 기대던 프로그램 한 종류가 조용히 죽는다.
이 비용이 누구에게 얼마나 쌓이는지는 글도 댓글도 다루지 않았고, 따라서 이 문단의 일반화는 이 노트의 추정이다.

### '가장 오래된'은 기준 축을 바꾸면 순위가 뒤집힌다

이 글의 순위는 세 축에 동시에 걸려 있다.
파일의 날짜, 추가 도구의 유무, 기능의 완전성이다.
날짜만 보면 REVERSI(1985)가 이기고, 추가 도구 없이 완전히 돌아가는 것만 보면 FREECELL(1993)이 이기고, 둘 사이의 타협이 CDPLAYER(1992)다.

이런 순위는 소프트웨어 호환성 이야기에서 흔한 구조다.
“몇 년 된 코드가 아직 돈다”는 문장은 무엇을 돈다고 칠지를 먼저 정하지 않으면 반증도 확증도 되지 않는다.
이 글은 그 정의를 “더블클릭해서 실행”으로 밝혀 둔 덕에 읽을 만하지만, 기준을 하나 더 늘려 “실물 장치와 상호작용한다”를 넣으면 CDPLAYER는 unleaded의 시험 때문에 탈락한다.

### 다른 운영체제와의 비교는 같은 질문의 다른 답을 낸다

HN 댓글은 곧바로 Linux와 BSD로 질문을 옮겼다.
ndiddy는 11월 16일을 넘어야 하는 기준일로 삼고, FreeBSD와 NetBSD가 4.3BSD ABI의 a.out 실행 파일을 지원한다고 문서에 적혀 있으며, SCO OpenServer는 XENIX x.out 바이너리를 지원한다고 적혀 있다고 짚었다.[^ndiddy]
LeFantome는 1984년의 xwm과 1989년의 twm이 지금도 Xorg에서 실행된다고 했다.[^LeFantome]

반면 Linux의 일반적인 불편은 커널이 아니라 사용자 공간에서 나온다.
Rohansi는 커널은 사용자 공간을 깨지 않는 데 엄격하고, 호환성을 깨는 쪽은 사용자 공간이라고 지적했다.[^Rohansi]
kragen은 Ubuntu 24.04 컨테이너에서 만든 바이너리가 glibc 2.36의 Debian Bookworm에서 `GLIBC_2.38`이 없다며 실패했고, 반대 방향은 되며 정적 링크가 해법이라고 적었다.[^kragen]

두 증언을 합치면 이 글의 결과와 같은 이야기가 된다.
오래 사는 바이너리는 커널 쪽의 약속이 아니라, 바이너리가 기대는 런타임이 제자리에 있는지에 따라 결정된다.
다만 이 비교는 댓글의 보고일 뿐이고, 실제로 Windows와 같은 조건에서 두 계열의 가장 오래된 GUI 프로그램을 시험한 사람은 없었다.

Lobste.rs에서도 FreeCell을 두고 비슷한 방향의 질문이 나왔다.
jkoppel은 DirectX 이전 시대의 게임은 WinG를 쓰는데 이것이 Windows 11에서는 기본 지원되지 않는다며, FreeCell은 다른 방식일 것이라고 추측했다.[^jkoppel]
artem은 폼을 그리는 데 순수 Win32 API를, 그림을 옮기는 데 BitBlt 호출을 썼을 가능성이 높다고 답했다.[^artem]
둘 다 확인된 사실이 아니라 추측이어서 이 노트는 근거로 쓰지 않고 참고만 한다.

### 오래된 소프트웨어가 돌아간다는 사실은 놀라움의 기준선이 얼마나 내려갔는지도 보여 준다

kidel001은 34년 전의 책이 에뮬레이터 없이 열리고 1896년의 책도 그렇다며, 소프트웨어에서 하위 호환이 없다는 것에 우리가 너무 익숙해졌다고 꼬집었다.[^kidel001]
이 반응은 글의 감탄과 같은 방향이지만, 놀라움이 향하는 곳이 다르다.
글은 “이렇게 오래된 것도 돈다”에 놀라고, 댓글은 “그것이 놀라울 만큼 드물다”에 놀란다.

zod000은 Lobste.rs에서 Windows 3.1용으로 Win32s를 쓰는 프로그램을 여러 개 작성했는데 아직 갖고 있다면 아마 돌아갈 것이라고 적었다.[^zod000]
이는 개별 증언이고 시험된 결과는 아니다.
이 두 증언이 나란히 놓이면, Windows의 이 성질은 우연한 생존이 아니라 일정한 기간 동안의 설계 방침이었다는 읽기가 가능해진다.
이 해석은 이 노트의 추론이고, 글이나 댓글이 그렇게 주장한 것은 아니다.

---

[^enlyth]: <https://news.ycombinator.com/item?id=50250556>

[^unleaded]: <https://news.ycombinator.com/item?id=50253655>

[^MisterTea]: <https://news.ycombinator.com/item?id=50250195>

[^mattbee]: <https://news.ycombinator.com/item?id=50253547>

[^lproven]: <https://news.ycombinator.com/item?id=50255996>

[^fredoralive]: <https://news.ycombinator.com/item?id=50256999>

[^lproven-oct]: <https://news.ycombinator.com/item?id=50258023>

[^kevin_thibedeau]: <https://news.ycombinator.com/item?id=50253243>

[^ndiddy]: <https://news.ycombinator.com/item?id=50249857>

[^LeFantome]: <https://news.ycombinator.com/item?id=50252473>

[^Rohansi]: <https://news.ycombinator.com/item?id=50254901>

[^kragen]: <https://news.ycombinator.com/item?id=50253265>

[^kidel001]: <https://news.ycombinator.com/item?id=50250737>

[^jkoppel]: <https://lobste.rs/s/rwubks/oldest_gui_application_still_runs_on#c_o4mdzl>

[^artem]: <https://lobste.rs/s/rwubks/oldest_gui_application_still_runs_on#c_yixuvr>

[^zod000]: <https://lobste.rs/s/rwubks/oldest_gui_application_still_runs_on#c_3wfbft>
