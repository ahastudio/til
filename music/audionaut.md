# Audionaut: AI 에이전트가 MCP로 편집하는 오픈소스 멀티트랙 오디오 편집기

<https://audionaut.app/>

<https://github.com/kvoltmer/Audionaut>

HN 토론: <https://news.ycombinator.com/item?id=49931031> (147점, 47개 댓글)

GN 토론: <https://news.hada.io/topic?id=34682>

## 소개

Audionaut는 녹음, 자르기, 배치,
내보내기를 하는 무료 오픈소스 멀티트랙 오디오 편집기다.
README의 한 줄 소개는 AI 에이전트가 MCP로 조작할 수 있는
멀티트랙 오디오 편집기다.
음악, 팟캐스트, 멀티트랙 녹음을 대상으로 하며,
완전한 DAW의 무게와 복잡함 없이 정밀한 자르기, 트랙별 플레이리스트, 다채널 지원,
깔끔한 내보내기를 주겠다고 한다.
JUCE 프레임워크 위에 현대 C++로 작성했고 Windows, macOS,
Linux에서 네이티브로 돈다.

저장소는 2023년 1월에 만들어졌고,
홈페이지에 따르면 코드는 2026년 8월 15일에 공개됐다.
라이선스는 GPL-3.0 이상과 상용 라이선스의 이중 라이선스다.
다만 `LICENSE.md`는 Essentia와 Ableton Link 같은 GPL·AGPL 라이브러리를 링크하고
있어 지금은 상용 라이선스를 발급할 수 없다고 밝힌다.
최신 릴리스는 10월 1일의 v1.6.4이고, 2026년 10월 4일 기준 스타는 190개다.
홈페이지는 GPLv3 소스 공개와 함께 GitHub Sponsors로 개발을
후원해 달라고 요청한다.
홈페이지의 소개 문구는 녹음, 편집, 편곡 세 단어와 함께, 이 앱이 MCP를
말하므로 AI 어시스턴트가 사용자 곁에서 같이 편집할 수 있다는 문장으로 끝난다.

작성자 vltmrkls는 HN의 Show HN 글에서
3~4년을 들여 만들었다고 소개했다.[^vltmrkls]
처음 동기는 자신의 다채널 녹음을 옛 Sound Designer II
방식으로 편집하는 것이었다.
리전을 만들고, 플레이리스트에 놓고, 플레이리스트를 내보내면 끝나는 흐름이다.
그는 가장 최근 기능인 에이전트 편집이 UI가 항상 투명성을 주기
때문에 유용하다고 적었다.

나는 Audionaut를 설치하거나 실행하지 않았다.
아래 내용은 홈페이지, README, `docs/features.md`, 사용자 매뉴얼 11장,
`audionaut-mcp` README, 릴리스 노트, HN 토론에서 확인한 것이다.

## 주요 기능

### 편집 모델

편집은 리전 기반이고 비파괴적이다.
이름 붙은 리전은 원본 오디오의 조각이고, 클립이 그 리전을 타임라인에 놓는다.
한 리전을 오디오 복사 없이 여러 번 쓸 수 있고,
트랙마다 자기 클립 플레이리스트를 갖는다.
플레이리스트와 타임라인은 양방향으로 동기화된다.
Intro, Theme A, Theme B, End처럼 구간에 한 번 이름을 붙이면, 그 리전을
플레이리스트나 타임라인에 끌어다 놓아 원하는 순서로 몇 번이든 배치할 수 있다.
한 트랙은 함께 움직이는 채널을 몇 개든 담을 수 있어서,
8채널 라이브 녹음이나 믹스의 스템을 하나의 트랙으로 다룬다.

클립 단위로는 채널별 게인, 곡선을 조절할 수 있는 페이드 인·아웃(기본은 등전력),
0.25배에서 4배까지의 속도 변경이 있다.
속도 변경은 음높이가 같이 바뀌는 varispeed와 음높이를 유지하는 Rubber Band R3
기반 타임 스트레치 중에서 고른다.
조작은 Cmd+Alt를 누른 채 클립 가장자리를 끄는 테이프 방식이고,
페이드와 마커와 파형이 함께 따라온다.
분할, 복제, 내보내기를 거쳐도 속도와 방식이 유지되며,
늘리기 한 번은 되돌리기 한 번으로 취소된다.
녹음 테이크, 스템 분리, 에이전트 편집까지 모두 되돌리기 대상이다.

### 분석과 자동 편집

분석은 Essentia로 한다.
구간 경계(SBic), 온셋, 비트 추적을 계산해 프로젝트에 캐시하고 트랙
위에 겹쳐 보여 준다.
Auto Edit는 분석된 경계에서 클립을 자르는 Create Segments와, 트랙의 리전들로
원하는 길이의 새 편곡을 순서대로 또는 섞어서 만드는 Assemble 두 가지다.
Create Segments는 자를 지점을 클립 위에 미리 보여 주고,
조각 수를 줄이거나 늘리고 크로스페이드를 켜고 끈 뒤 한 번에 적용하는 방식이다.
홈페이지는 긴 테이크, 즉흥 연주,
스템을 구조가 있는 트랙으로 바꾸는 용도로 이 기능을 소개한다.

### 스템 분리

Meta의 Demucs를 C++로 옮긴 demucs.cpp로 클립을 드럼, 베이스,
그 밖의 소리(Other), 보컬의 네 트랙으로 나눈다.
Edit 메뉴에서 바로 실행하며, 모노 클립에서는 모노 스템이 나온다.
로컬에서 돌고 아무것도 올리지 않으며, 약 80MB인 모델은 처음 쓸 때 내려받는다.
`docs/features.md`와 `LICENSE.md`는 이 htdemucs 가중치가 연구용으로만 허가되어
있다고 분명히 적는다.

### 녹음과 라우팅

녹음은 처음부터 끝까지 한 번에 하거나, 재생 중에 펀치 인으로 끼어들거나,
구간을 반복하며 할 수 있다.
녹음 대기 상태인 채널마다 파일이 하나씩 생기고, 모든 테이크는 되돌리기 대상이다.
트랙의 각 채널은 하드웨어 입출력 어느 포트로든, 또는 메인 버스로 보낼 수 있다.
채널 스트립은 기본값이 아닌 라우팅을 한눈에 보여 주고,
포트를 쓸 수 없으면 경고한다.

### 입출력과 플랫폼

WAV, AIFF, FLAC, Ogg Vorbis, MP3를 가져오고,
같은 형식으로 실시간보다 빠르게 오프라인 렌더링해 내보낸다.
MP3와 Ogg Vorbis는 비트레이트를 고를 수 있고, 내보내기는 모노, 스테레오, 다채널,
그리고 채널마다 파일을 따로 만드는 멀티 모노 중에서 고른다.
채널별 입출력 라우팅과 Ableton Link 동기화를 지원한다.
`.audium` 프로젝트는 평범한 JSON 프로젝트 파일과 오디오를 담은 폴더다.

macOS는 Apple silicon과 macOS 13 이상이 필요하고,
공증된 DMG와 Mac App Store 판이 있다.
Windows는 x64 설치 파일인데 아직 코드 서명이 없어 첫 실행 때
SmartScreen 경고가 뜬다.
Linux는 x86_64용 AppImage와 `.deb`다.

## 에이전트 편집의 동작 방식

### 모든 도구 호출은 명령 하나다

`audionaut-mcp`는 얇은 래퍼다.
도구 하나가 Audionaut 명령 하나를 `--json`으로 실행하고 결과를 그대로 넘기며,
엔진 로직은 이 서버에 없다.
명령을 실행하는 주체는 설치된 Audionaut 앱 자체다.
앱 바이너리에 동사(verb)를 붙여 실행하면 GUI 없이 실행한 뒤 그 명령의 종료
코드로 끝나고, GUI 인스턴스가 열려 있어도 마찬가지다.

도구는 22개다.
프로젝트 생성, 가져오기, 분석, Auto Edit, Assemble, 분할, 리전 생성·수정·정리,
클립 배치·이동·제거, 클립 게인·페이드·속도, 스템 분리, 트랙·채널 제거, 내보내기,
프로젝트 정보, 그리고 GitHub 이슈를 여는 `request_feature`와 `report_bug`다.

### 열린 프로젝트는 실행 중인 앱이 편집한다

이 도구의 핵심 설계는 사용자가 앱에서 열어 둔 프로젝트를 어떻게 다루는가에 있다.
앱이 프로젝트를 열고 있으면, 그 프로젝트를 향한 명령은 파일이 아니라 실행
중인 앱으로 넘어간다.
명령은 저장하지 않은 변경까지 포함해 사용자가 지금 보고 있는 문서에 적용되고,
결과는 동사 이름이 붙은 되돌리기 항목 하나로 들어온다.
창 제목에는 *Edited By Agent* 표시가 붙고,
`Project.json`에는 아무것도 쓰지 않으므로 저장은 사용자 몫으로 남는다.

충돌 규칙도 사용자 쪽에 서 있다.
명령이 도는 동안 사용자가 프로젝트를 바꾸면 명령 결과는 버려지고 에이전트에게
다시 실행하라고 알린다.
녹음 중에는 명령을 거부하고, 재생 중에는 내보내기를 거부한다.
앱이 프로젝트를 잡고 있는데 명령이 앱에 닿지 못하면 파일로 돌아가지 않고
실패한다(`host_unavailable`).
매뉴얼은 저장하지 않은 내용이 빠진 파일을 조용히 덮어쓰는 것이 거부할 가치가
있는 유일한 결과라고 설명한다.

앱이 프로젝트를 열고 있지 않으면 명령은 원래대로 프로젝트 파일을 직접 읽고 쓴다.
일부러 파일을 다루고 싶으면 `AUDIONAUT_AGENT_ROUTING=0`을 준다.
패키지 안의 `Autosave.json`(충돌 복구 스냅숏)과 `Host.json`(어느 프로세스가
프로젝트를 잡고 있는지 표시)은 앱 소유이므로 건드리지 않는다.

### 에이전트가 직접 이슈를 연다

`request_feature`와 `report_bug`는 에이전트가 도구의 한계나 버그에 부딪혔을 때
유지보수자에게 GitHub 이슈를 보내는 통로다.
기본 경로는 자체 GitHub 토큰으로 이슈를 여는 Cloudflare Worker 릴레이이고,
릴레이를 건너뛰면 로그인된 `gh`를, 그것도 없으면 미리 채운 이슈 URL을 돌려준다.
서버 지침은 에이전트에게 이슈를 보낼 때 사용자에게 알리고,
오디오는 첨부하지 말라고 한다.
보고자 이름이나 이메일은 사용자가 줄 때만 들어간다.
이슈를 원치 않으면 `AUDIONAUT_DISABLE_FEATURE_REQUESTS=1`을 준다.

## 사용법

### Claude Code에 연결하기

앱과 Node.js 18 이상이 있으면 MCP 서버를 등록한다.
버전은 1.6.3 이상을 권하고, 1.6.2는 macOS와 Linux에서는 되지만 Windows에서는
에이전트에 응답하지 않을 수 있다.

```bash
claude mcp add audionaut -- npx -y audionaut-mcp

# 서버가 어느 Audionaut를 찾았고 응답하는지 확인
npx -y audionaut-mcp --check
```

Claude Desktop은 `claude_desktop_config.json`에 다음을 넣고 다시 시작한다.

```json
{
  "mcpServers": {
    "audionaut": {
      "command": "npx",
      "args": ["-y", "audionaut-mcp"]
    }
  }
}
```

그다음 “`~/Music/Audionaut/Demo Project.audium`의 클립을 16마디마다 자르고
두 번째 조각마다 새 트랙에 놓아 줘” 같은 요청을 한다.
프로젝트를 앱에 열어 두면 편집이 들어오는 모습을 볼 수 있다.

### 명령줄로 스크립트 짜기

모든 동사는 `--json`을 받아 stdout에 결과 봉투 하나만 찍고,
로그는 stderr로 보낸다.
성공은 `{"ok": true, "result": ...}`,
실패는 `{"ok": false, "error": {"code": ..., "message": ...}}` 모양이다.
종료 코드는 0이 성공, 1이 실패, 2가 사용법 오류, 3이 이 빌드에 없는 기능(예:
Essentia 없이 `analyze`)이다.
위치와 길이는 기본이 음악 단위다.
`--unit bars|beats|seconds|clocks`로 단위를 바꾸며,
기본인 마디와 비트는 1부터 센다.
그래서 23마디에서 자르라는 요청은 그대로 `split song.audium --at 23`이 된다.

README가 제시하는 전형적인 에이전트 흐름은 `create` → `import` → `analyze` →
`auto-edit`나 `assemble` → `export`다.

```bash
audionaut-cli create    song.audium --channels 2
audionaut-cli import    song.audium take1.wav take2.wav --position 4.5
audionaut-cli analyze   song.audium --types sbic,beat_degara
audionaut-cli auto-edit song.audium --track 0 --measures 4
audionaut-cli split     song.audium --at 23            # 23마디에서 분할
audionaut-cli create-region song.audium --name chorus --start 17 --end 25
audionaut-cli place-clip    song.audium --region chorus --at 33
audionaut-cli clip-fades    song.audium --region chorus --fade-in 1 --unit beats
audionaut-cli export    song.audium -o mix.wav --sample-rate 48000 --bit-depth 24
```

`audionaut-cli`는 테스트용 CMake 프로젝트와 함께 빌드하는 독립 바이너리이고,
설치된 앱 바이너리도 같은 동사를 받는다.
CLI로 만든 프로젝트는 GUI에서 열리고 그 반대도 된다.

## 트레이드오프

### UI를 남겨 둔 에이전트 편집

작성자가 내세우는 장점은 UI가 투명성을 준다는 점이다.[^vltmrkls]
에이전트의 편집이 열린 문서에 되돌리기 한 단계로 들어오므로 사람은 결과를 듣고
보고, 마음에 안 들면 ⌘Z로 되돌린다.
에이전트에게 파일을 넘기고 결과 파일을 받는 방식과 달리,
사람의 작업 공간 안에서 에이전트가 같이 일하는 구조다.

HN에서 jhvkjhk가 완전히 자동으로 편집하는지,
AI는 언제 멈출지 어떻게 아는지 묻자, 작성자는 가져오기에서 분석, 자동 편집,
조립, 내보내기까지 자동으로 할 수 있지만 결과는 대개 작은 손질이 필요하고 그걸
돕는 것이 UI의 역할이라고 답했다.[^vltmrkls-auto]
즉 이 도구는 자동화의 끝을 사람의 귀에 둔다.

### 같은 일을 ffmpeg 스크립트로 할 수도 있다

thenoblesunfish는 잠들 때 듣는 팟캐스트에서 음악처럼 잠을 깨우는 부분을 예시
편집 몇 개로 가르쳐 다른 파일에서도 잘라 낼 수 있냐고 물었다.[^thenoblesunfish]
playfultones는 더 좋은 모델에 ffmpeg를 쥐여 주면 이미 할 수 있는 일이라며,
음량 분석과 Whisper로 말의 시작과 끝을 잡아 자르면 된다고 했다.[^playfultones]
tervem6istus는 Silero VAD나 YAMNet 같은 음성·음악 분류 모델이 있으니 LLM이 한
번에 스크립트를 써 줄 수 있을 것이라고 덧붙였다.[^tervem6istus]
질문자는 그런 방법이 더 효율적일 수 있다고 인정하면서도,
소프트웨어 공학이나 데이터 과학보다는 Audacity에서 손으로 하던 방식을 여러
파일에 자동으로 적용해 주는 도구를 원한다고 답했다.[^thenoblesunfish-reply]

이 대화가 Audionaut의 자리를 잘 보여 준다는 것이 내 해석이다.
일괄 처리만 필요하면 ffmpeg 스크립트가 더 가볍다.
Audionaut가 이기는 곳은 결과를 사람이 듣고 고쳐야 하는 편집, 그리고 리전과
플레이리스트 같은 편집 상태를 남겨 다시 손댈 수 있어야 하는 작업이다.

### DAW가 아니라는 선택

작성자는 아직 DAW가 아니며, 자기 음악에 필요해서 플러그인 지원을 백로그에
올렸지만 지연 보상과 수많은 플러그인 형식이 골칫거리라고 했다.[^vltmrkls-daw]
PaulDavisThe1st는 이 말에 아마 올해 가장 절제된 표현일 것이라고
답했다.[^PaulDavisThe1st]
작성자는 다른 답글에서, 지금까지의 피드백을 보면 오디오
분석(MIR)에 집중하고 오디오 플러그인의 함정에 빠지지 않는 편이 나을지도 모른다고
적었다.[^vltmrkls-mir]
`docs/features.md`의 아직 없는 기능 목록에는 VST3·AU·LV2 플러그인 호스팅,
이펙트, 오토메이션, MIDI, 마커와 레이블, 메뉴에서 가져오기,
무음·군말 제거 같은 음성 전용 도구, Flatpak,
코드 서명된 Windows 설치 파일이 올라 있다.

## 함정

### macOS 샌드박스는 `~/Music`만 허락한다

macOS 앱은 샌드박스 안에서 돌고, 앱이 대신 실행하는 명령도 마찬가지다.
그래서 프로젝트, 가져올 오디오, 내보낼 경로가 모두 `~/Music` 안에 있어야 한다.
MCP 서버는 명령을 시작하기 전에 이를 검사해 다른 경로를
`sandbox_denied`로 거부한다.
소스에서 빌드한 `audionaut-cli`와 Windows, Linux에는 이 제약이 없다.

### 상대 경로는 MCP 클라이언트에 따라 달라진다

`audionaut-mcp` README는 도구 인자의 경로를 절대 경로로 주라고 권한다.
상대 경로는 서버 프로세스의 작업 디렉터리를 기준으로 풀리고, 그 디렉터리는 MCP
클라이언트마다 다르기 때문이다.

### 스템 분리 모델의 라이선스

demucs.cpp 자체는 MIT지만 htdemucs 가중치는 연구용으로만 허가되어 있다.
앱 코드가 GPL이어도 스템 분리 결과를 상업 작업에 쓸 때는 모델
라이선스를 따로 따져야 한다.

### 사용 통계

CLI 호출은 앱과 같은 옵트인 동의를 따르고,
동의하면 동사와 종료 코드를 담은 `cli_command` 이벤트 하나를 보낸다.
CI나 스크립트에서는 `AUDIONAUT_DISABLE_ANALYTICS=1`로 동의 여부와
상관없이 끌 수 있다.

## 체크리스트

- Audionaut 버전이 1.6.3 이상인가?
- `npx -y audionaut-mcp --check`가 설치된 앱을 찾았는가?
- macOS라면 프로젝트와 오디오와 내보내기 경로가 `~/Music` 안에 있는가?
- 도구 인자의 경로를 절대 경로로 주었는가?
- 에이전트가 자동으로 GitHub 이슈를 열어도 되는지 정했는가?
- 스템 분리 결과를 어디에 쓸지 모델 라이선스와 대조했는가?

---

[^vltmrkls]: <https://news.ycombinator.com/item?id=49931069>

[^vltmrkls-auto]: <https://news.ycombinator.com/item?id=49932817>

[^thenoblesunfish]: <https://news.ycombinator.com/item?id=49932136>

[^playfultones]: <https://news.ycombinator.com/item?id=49932259>

[^tervem6istus]: <https://news.ycombinator.com/item?id=49940790>

[^thenoblesunfish-reply]: <https://news.ycombinator.com/item?id=49945344>

[^vltmrkls-daw]: <https://news.ycombinator.com/item?id=49932724>

[^PaulDavisThe1st]: <https://news.ycombinator.com/item?id=49933805>

[^vltmrkls-mir]: <https://news.ycombinator.com/item?id=49936813>
