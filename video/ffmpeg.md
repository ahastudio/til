# FFmpeg: 인터넷의 영상을 떠받치는 자원봉사 멀티미디어 프레임워크

<https://ffmpeg.org/>

<https://github.com/FFmpeg/FFmpeg>

HN 토론: <https://news.ycombinator.com/item?id=49166202> (466점, 97개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=44886997> (364점, 353개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=44886647> (1033점, 325개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/jvgi1u/ffmpeg_9_0> (35점, 5개 댓글)

GN 토론: <https://news.hada.io/topic?id=22671>

## 소개

FFmpeg는 사람과 기계가 만든 거의 모든 오디오·영상을 디코드, 인코드,
트랜스코드, 먹스·디먹스, 스트리밍, 필터링, 재생할 수 있다고 스스로를 소개하는
멀티미디어 프레임워크다.
공식 소개 페이지는 표준 위원회가 만든 포맷이든, 커뮤니티나 기업이 만든
포맷이든 가장 오래된 것부터 최신 것까지 지원한다고 적는다.
Linux, macOS, Windows, BSD, Solaris 등에서 컴파일되고,
FATE라는 자체 테스트 인프라를 통과한다.

### 라이브러리와 도구

FFmpeg는 하나의 명령이 아니라 라이브러리 묶음이다.

| 구성          | 역할                             |
| ------------- | -------------------------------- |
| libavcodec    | 코덱(인코더·디코더)              |
| libavformat   | 컨테이너(먹서·디먹서)와 프로토콜 |
| libavfilter   | 필터 그래프                      |
| libavutil     | 공통 유틸리티                    |
| libavdevice   | 캡처·재생 장치                   |
| libswscale    | 이미지 크기·색 공간 변환         |
| libswresample | 오디오 리샘플링                  |
| `ffmpeg`      | 변환용 명령줄 도구               |
| `ffplay`      | 간단한 재생기                    |
| `ffprobe`     | 미디어 정보 분석                 |

소개 페이지는 의존성을 줄이고 코드를 공유하기 위해 자체 코드를 “약간 선호”하며,
무엇이 최선인지 답할 수 없는 경우에는 두 선택지를 모두 지원해 사용자가 고르게
한다고 밝힌다.
같은 H.264 인코딩이라도 외부 라이브러리 `libx264`와 Apple의 하드웨어 인코더
`h264_videotoolbox`를 함께 쓸 수 있는 것이 그 결과다.

### 저장소는 자체 git이 원본이고 GitHub는 미러다

다운로드 페이지가 밝히는 주 저장소는 `https://git.ffmpeg.org/ffmpeg.git`이다.
`github.com/FFmpeg/FFmpeg`은 “주 저장소의 미러”로 명시되어 있고,
GitHub 저장소 설명도 “Mirror of https://git.ffmpeg.org/ffmpeg.git”이며
이슈 기능은 꺼져 있다.
그럼에도 2026년 10월 기준 스타 약 65,000개, 포크 약 14,300개를 모았다.
FFmpeg 8.0 발표문은 메일링 리스트 서버를 전면 교체했고,
`code.ffmpeg.org`의 Forgejo 인스턴스로 기여를 받기 시작했다고 알렸다.
오래 이어진 메일링 리스트 패치 방식에서 웹 기반 포지로 옮겨 가는 중이다.

### 라이선스: LGPL이 기본이지만 GPL 부품을 켜면 전체가 GPL

법률 페이지에 따르면 FFmpeg는 LGPL 2.1 이상이지만,
선택적인 부품과 최적화 일부는 GPL 2 이상이다.
그런 부품을 쓰면 FFmpeg 전체에 GPL이 적용된다.
그리고 어떤 상용·독점 라이선스로도, 돈을 내더라도 제공하지 않는다고
분명히 적는다.

같은 페이지의 LGPL 준수 체크리스트는 `--enable-gpl`과 `--enable-nonfree` 없이
빌드할 것, 동적 링크할 것,
배포하는 바이너리와 정확히 일치하는 소스를 함께 둘 것을
요구한다.
그리고 GPL 라이브러리를 쓰지 말라며 예로 `libx264`를 든다.
Homebrew로 설치한 ffmpeg 9.0.2의 빌드 설정(`ffmpeg -buildconf`)을 보면
`--enable-gpl`, `--enable-version3`, `--enable-libx264`, `--enable-libx265`가
켜져 있다.
즉 개인이 흔히 쓰는 배포판 ffmpeg는 이미 GPL 빌드다.

법률 페이지는 특허에 대해서도 솔직하다.
FFmpeg가 특허 알고리즘을 쓰는지 모르고, 구현할 때 특허를 읽은 적도 없다고 한다.
개인적 용도라면 걱정할 이유가 거의 없지만,
상용 제품에 FFmpeg 코어 전체를 넣는 것은 문제가 될 수 있다고 경고한다.
상표 FFmpeg는 프로젝트를 시작한 Fabrice Bellard의 것이다.

### 릴리스 주기

다운로드 페이지에 따르면 FFmpeg는 약 6개월마다 메이저 릴리스를 내고,
그 사이에는 새 기능 없이 중요한 버그 수정만 담은 포인트 릴리스를 낸다.
릴리스는 배포판과 시스템 통합자를 위한 것이고,
직접 빌드하는 사용자에게는 개발자들이 실제로 일하는 유일한 버전인 개발 브랜치를
쓰라고 강하게 권한다.
릴리스 브랜치는 개발 브랜치의 일부 변경만 골라 가져오기 때문이다.

| 릴리스 | 이름      | 최신 포인트 릴리스 | 브랜치 분기일 |
| ------ | --------- | ------------------ | ------------- |
| 9.0    | Lei       | 9.0.2 (2026-09-18) | 2026-06-26    |
| 8.1    | Hoare     | 8.1.3 (2026-09-21) | 2026-03-08    |
| 8.0    | Huffman   | 8.0.3 (2026-06-18) | 2025-08-09    |
| 7.1    | Péter     | 7.1.5 (2026-06-20) | 2024-09-24    |
| 6.1    | Heaviside | 6.1.6 (2026-06-20) | 2023-10-29    |

Lobste.rs에서 mdaniel은 9.0의 릴리스 노트가 “변경 로그를 보라”는 한 문단뿐이라며
변경 로그 링크를 공유했고,[^mdaniel]
timschumi는 큰 줄기의 변경 로그는 릴리스 브랜치가 갈라질 때 확정되고
그 뒤로는 버그 수정만 들어가기 때문에 날짜가 오래돼 보인다고
설명했다.[^timschumi]
sri는 깨지는 변경이 없어서 스크립트를 고칠 필요가 없었다고 했다.[^sri]

모든 릴리스는 PGP 키로 서명되고,
최근 릴리스는 양자 내성 서명(`.pq.asc`)도 함께 제공한다.

### 최근의 큰 변화

8.0 “Huffman”(2025년 8월)은 지연과 인프라 현대화 때문에 역대 가장 큰 릴리스
중 하나가 됐다고 발표문은 적는다.
APV, ProRes RAW 같은 네이티브 디코더와 함께,
Vulkan 1.3 구현이면 어디서든 도는 순수 Vulkan 컴퓨트 기반 코덱(FFv1 인코드·
디코드, ProRes RAW 디코드)이 들어왔다.
필터 목록에는 Whisper도 있다.
8.1 “Hoare”(2026년 3월)는 xHE-AAC, MPEG-H 디코딩, D3D12 인코딩 등을 더했고,
swscale 재작성 준비가 진행 중이라고 밝혔다.
2026년 6월에는 Ampere가 192코어 Arm 서버를 기증했다는 소식을 올리면서,
이를 기념하는 그림을 “AI가 아닌 작품”으로 공모했다고 적었다.

## 분석

### 표준이 아니라 현실의 파일을 구현하는 것이 FFmpeg의 일이다

FFmpeg의 존재 이유는 사양서를 구현하는 데 있지 않다.
소개 페이지가 “표준 위원회, 커뮤니티, 기업이 만든 것 무엇이든”이라고 굳이
나열하는 것처럼,
실제 세상에 존재하는 파일을 읽을 수 있게 만드는 데 있다.
HN의 dylan604는 TV 제조사가 준 칩 사양대로 최대 비트레이트까지 밀어붙였다가,
실제로는 사양의 85% 수준에서야 제대로 재생되어 값을 다시 낮춰야 했던 경험을
전했다.[^dylan604]
사양과 실제 하드웨어·소프트웨어의 동작이 다르다는 것을 아는 프로젝트만이
“거의 모든 것”을 읽을 수 있다.

이 태도는 9.0의 변경 목록에도 그대로 보인다.
Playdate 휴대용 게임기용 영상 인코더가 들어가고 애니메이션 WebP 디코더가
들어오는 동시에,
더는 쓰이지 않는 CELT 디코딩은 빠졌다.[^gyan]
HN의 kergonath는 Playdate 코덱을 LucasArts 코덱 다음가는 극한의 틈새라고
감탄했다.[^kergonath]
틈새 포맷을 넣고 빼는 판단이 프로젝트의 일상 업무다.

### 라이브러리 묶음이라는 구조가 FFmpeg를 보이지 않는 인프라로 만든다

대부분의 사용자는 `ffmpeg` 명령을 FFmpeg라고 생각하지만,
실제 영향력은 libavcodec과 libavformat 같은 라이브러리에서 나온다.
브라우저, 미디어 플레이어, 영상 플랫폼, 편집기가 이 라이브러리를 링크해 쓰므로,
FFmpeg는 사용자가 모르는 사이에 인터넷 영상 처리의 바닥에 깔린다.
HN의 hparadiz는 FFmpeg가 웹 백엔드의 틈새 도구에서 지금의 위치로 오는 과정이
놀라웠다고 했다.[^hparadiz]

이 구조는 FFmpeg에 독특한 협상력을 준다.
HN 스레드의 원 기사가 전한 바에 따르면, 오픈소스 정책 전문가 Mark Atwood는
Amazon 재직 시절 상사들에게 FFmpeg는 공급업체가 아니고, NDA도 없고,
우리에게 지렛대도 없으며,
이메일 한 통으로 주요 제품 라인 세 개를 죽일 수 있다고 계속 설명해야
했다고 회고했다.
phkahler가 이 대목을 인용하며 버그를 찾는 데 돈을 쓸 수 있다면 고치는 데도
쓸 수 있다고 덧붙였다.[^phkahler]

### 자원봉사자 프로젝트가 기업 보안 프로세스를 받아 내는 비대칭

2025년 11월 FFmpeg가 Google에 “자금을 대든지 버그 보고를 멈추라”고 요구한
논쟁은 이 비대칭이 터진 사건이다.
Google의 AI 기반 도구가 찾은 use-after-free 취약점이 공개 기한과 함께 보고되자,
FFmpeg 측은 자원봉사자에게 기업의 보안 일정을 강요한다고 반발했다.

HN에서는 양쪽 논리가 팽팽했다.
theoldgreybeard는 AI로 찾은 버그라면 고치는 데도 몇 초면 됐을 텐데,
돈을 태워 자원봉사 프로젝트에 스팸 같은 보고를 쏟는 것은
씁쓸하다고 했다.[^theoldgreybeard]
반면 woodruffw는 자신도 메인테이너라 공감하지만,
보안 이슈는 누가 보고하든 메인테이너가 고쳐야 하거나 평판 손실을 감수해야 하는
일이고,
보안을 우선순위로 두지 않는 선택도 괜찮지만 양쪽을 다 가질 수는 없다고
반박했다.[^woodruffw]
iscoelho는 이 취약점이 대부분의 데스크톱·서버 배포판에 기본 포함된 코덱에 있는
재현 가능한 use-after-free라고 짚었다.[^iscoelho]

GN에서는 GN 사용자들의 직접 반응이 이어졌다.
secret3056은 버그 보고 자체는 훌륭하지만,
아주 오래된 비디오 포맷의 취약점을 기한 안에 못 고쳤다고 소문내는 것은
“먹어야만 하는 걸 주고 왜 기한 안에 못 먹느냐”고 하는 셈이라고
했다.[^secret3056]
bungker는 자발적으로 동네를 청소하는 사람에게 동네 땅을 가장 많이 가진 사람이
구석에 담배꽁초가 있다고 알려 주는 느낌이라고 비유했고,[^bungker]
nullptr은 curl이 겪은 버그 바운티용 엉터리 AI 보고서 문제의 연장선이지만,
이번에는 대기업이 보낸 유효하지만 사소한 보고라는 점이 다르다고
정리했다.[^nullptr]

## 비평

### “사소한 코덱”이라는 판단은 공격면의 논리와 맞지 않는다

FFmpeg 측과 지지자들은 문제가 된 코덱이 아주 오래된 게임의 초반 몇 프레임에만
쓰이는 포맷이라는 점을 강조했다.
GN의 ifmkl도 고전 게임의 첫 10~20프레임에서만 유효한 중간 등급 취약점이
FFmpeg에 정말 중요한 기여냐고 물었다.[^ifmkl]
하지만 보안의 관점에서 코덱의 인기는 위험도의 척도가 아니다.

HN의 cm2187은 FFmpeg 개발자 인터뷰에서 들은 이 논리를 이해할 수 없다고 했다.
위험도는 그 코드 경로가 얼마나 인기 있는지가 아니라 공격자가 닿을 수 있는지에
달려 있고,
누군가 잘 쓰이지 않는 코덱으로 만든 `.mkv`를 영상 플랫폼에 올려 FFmpeg로
처리하게 만들면 코덱의 인기와 무관하게 큰 사고라는 것이다.[^cm2187]
iscoelho도 드물게 쓰이는 DNG 이미지 포맷을 겨냥한 iOS 제로데이를 예로
들었다.[^iscoelho]

FFmpeg가 “거의 모든 것”을 읽는다는 것은 곧 거의 모든 포맷이 공격면이라는
뜻이다.
틈새 포맷을 지원한다는 자부심과 틈새 포맷의 취약점은 사소하다는 주장은
양립하기 어렵다.
위험을 줄이는 현실적 방법은 기본 빌드에서 오래된 디코더를 빼는 것이고,
lamontcg도 오래되고 버그 많은 코덱을 기본 빌드 플래그에서 빼자고
제안했다.[^lamontcg]

### LGPL이라는 간판은 실제 배포 현실을 가린다

법률 페이지는 FFmpeg를 LGPL로 소개하지만,
사용자가 실제로 받는 대부분의 ffmpeg는 GPL 빌드다.
Homebrew 빌드가 `--enable-gpl`로 `libx264`와 `libx265`를 켠 것처럼,
쓸 만한 H.264·H.265 소프트웨어 인코더를 원하면 GPL을 피하기 어렵다.
LGPL 체크리스트가 “`libx264`를 쓰지 말라”고 경고하는 것 자체가 그 긴장을
보여 준다.

이 문서의 [YouTube 영상 받기 매뉴얼](youtube-download.md)에서 최종 선택한
`libx264` CRF 23 인코딩도 GPL 부품이다.
개인이 자기 영상을 변환하는 데는 아무 문제가 없지만,
같은 명령을 회사 서비스의 백엔드에 넣는 순간 라이선스 판단이 달라진다.
FFmpeg의 문서는 이 경계를 정확히 설명하지만,
“FFmpeg는 LGPL”이라는 한 줄만 기억하는 사용자에게는 함정이 된다.

### 개발 브랜치를 쓰라는 권고는 배포 현실과 어긋난다

다운로드 페이지는 직접 빌드하는 사용자에게 릴리스가 아니라 개발 브랜치를
권한다.
보안 패치와 버그 수정이 개발 브랜치에 훨씬 빨리 들어가기 때문이다.
그런데 앞의 Google 논쟁에서 보듯,
FFmpeg의 보안 수정 속도는 자원봉사자의 시간에 묶여 있다.

결국 대부분의 사용자는 배포판이나 Homebrew가 주는 릴리스 바이너리를 쓰고,
릴리스 브랜치에는 개발 브랜치의 일부만 골라 들어간다.
9.0 HN 스레드에서는 FFmpeg 개발자 일부가 Anthropic의 오픈소스 프로그램으로
Claude를 지원받아 9.0에서 빠진 백포트를 찾는 데 썼다는 이야기가
나왔다.[^world2vec]
백포트 누락을 찾는 일에 도구가 필요할 만큼 릴리스 브랜치 관리가 사람 손에
버겁다는 뜻이기도 하다.

### 필터 그래프는 강력하지만 진입 장벽이 문서에 반영되지 않는다

FFmpeg의 필터 시스템은 Whisper 음성 인식, Vulkan 변환, 색 검출까지 담는 거대한
도구가 됐다.
HN의 shevy-java는 필터가 매우 강력하지만 쓰기 혼란스럽고 우아하지 않다며,
AviSynth처럼 미디어를 다루는 더 단순한 메타 언어를 바랐다.[^shevy-java]
account42는 FFmpeg의 필터 시스템이 바로 그런 메타 언어를 설계한 결과이고,
각 노드가 속성을 가진 필터인 그래프의 텍스트 표현일 뿐이라 익히면 나쁘지
않다고 답했다.[^account42]

두 의견은 모두 맞다.
문제는 공식 문서가 옵션을 나열하는 레퍼런스 중심이라,
그래프를 머릿속에 그리는 법을 가르치지 않는다는 점이다.
HN에서 꾸준히 큰 반응을 얻는 것이 FFmpeg 자체 발표보다 “FFmpeg by Example” 같은
외부 예제 모음이라는 사실이 그 공백을 보여 준다.

## 인사이트

### Whisper 필터는 FFmpeg가 미디어 “변환기”에서 “이해기”로 넘어가는 신호다

8.0에 Whisper 필터가 들어간 것은 기능 하나 이상의 의미가 있다.
지금까지 FFmpeg는 미디어의 형식을 바꾸는 도구였지,
내용을 해석하는 도구는 아니었다.
9.0의 변경 목록에는 GPU 실행을 지원하는 ONNX Runtime DNN 백엔드도 들어갔고,
HN의 alex7o는 ONNX가 하드웨어 가속 합성곱을 돌릴 몇 안 되는 방법이라고
했다.[^alex7o]

그 결과는 의존성의 성격 변화다.
HN에서 zoobab은 어떻게 만들어졌는지 모르는 외부 바이너리 모델이 필요한 기능을
Debian이 패키징할지 의문이라고 했고,[^zoobab]
dncornholio는 완벽하게 동작하지도 않는 기능을 라이브러리에 넣는 것은 비대화라고
비판했다.[^dncornholio]
실제로 Homebrew ffmpeg 9.0.2의 필터 목록에는 whisper가 없다.
배포판은 이미 이 기능을 선택적으로 다루고 있다.

이 흐름은 FFmpeg의 라이선스와 보안 문제를 다시 쓰게 한다.
코덱 코드는 사람이 읽을 수 있지만 모델 가중치는 그렇지 않고,
디코더의 버그는 재현할 수 있지만 모델의 환각은 확률적이다.
HN의 re는 Whisper가 15초 넘는 무음 구간에서 환각 루프에 빠진다고
지적했는데,[^re]
매뉴얼에서 실제로 겪은 “다음 영상에서 만나요” 26번 반복이 바로 그 현상이다.
FFmpeg가 이런 비결정적 구성 요소를 품을수록,
“거의 모든 것을 정확히 읽는다”는 정체성과 긴장이 커진다.

### 인프라 오픈소스의 자금 문제는 결국 포크가 아니라 협상으로 풀린다

HN에서 ranger_danger는 Google이 그냥 포크해서 자기 버그만 고치고 기여를 멈추면
어떻게 되느냐고 물었다.[^ranger_danger]
이론상 가능하지만, 현실에서 FFmpeg 규모의 프로젝트를 포크해 유지하는 비용은
버그를 고치거나 후원하는 비용보다 훨씬 크다.
수천 개 포맷, 아키텍처별 손으로 쓴 어셈블리, 30년 가까운 지식이 함께 따라오기
때문이다.

그래서 이 갈등은 xz 사태와 같은 구조로 흐르지 않는다.
immibis는 xz에 백도어를 넣은 Jia Tan이 먼저 기여로 신뢰를 쌓았다는 점을
상기시키며 대기업의 대량 기여에 경계심을 보였지만,[^immibis]
FFmpeg에서 실제로 일어나는 일은 장악이 아니라 자원의 제공이다.
2026년의 Ampere 서버 기증, Anthropic의 Claude 지원처럼,
기업은 현금 대신 장비와 도구로 기여하는 길을 찾고 있다.

이는 Linux 재단이나 curl의 후원 모델과 비교할 만하다.
코드 소유권을 중앙화하지 않으면서도 운영 비용은 외부에 분산하는 방식이다.
FFmpeg가 공식 페이지에 “Funding through SPI”와 “Hire Developers”를 메뉴로
둔 것도 같은 방향이다.
자원봉사 프로젝트가 인프라가 되면, 남는 질문은 기술이 아니라 거버넌스다.

### FFmpeg를 쓰는 쪽의 책임은 빌드 플래그에서 시작한다

사용자 입장에서 이 모든 논쟁의 실무적 결론은 단순하다.
어떤 ffmpeg를 쓰는지가 라이선스, 공격면, 기능을 동시에 결정한다.
`ffmpeg -buildconf` 한 줄로 GPL 여부와 켜진 외부 라이브러리를 확인할 수 있고,
`ffmpeg -decoders`와 `ffmpeg -filters`로 실제 공격면과 기능을 볼 수 있다.

개인이 영상을 변환하는 데는 배포판 빌드로 충분하다.
하지만 사용자가 올린 파일을 서버에서 처리하는 서비스라면,
필요한 디코더만 켠 최소 빌드가 가장 효과적인 보안 조치다.
FFmpeg가 “거의 모든 것”을 지원한다는 것은 장점이지만,
그 장점을 전부 켜 두는 것은 사용자의 선택이고 책임이다.

---

[^dylan604]: <https://news.ycombinator.com/item?id=49170759>

[^gyan]: <https://news.ycombinator.com/item?id=49166203>

[^kergonath]: <https://news.ycombinator.com/item?id=49170103>

[^hparadiz]: <https://news.ycombinator.com/item?id=49166480>

[^phkahler]: <https://news.ycombinator.com/item?id=45891830>

[^theoldgreybeard]: <https://news.ycombinator.com/item?id=45891941>

[^woodruffw]: <https://news.ycombinator.com/item?id=45891521>

[^iscoelho]: <https://news.ycombinator.com/item?id=45892331>

[^secret3056]: <https://news.hada.io/topic?id=24307#cid46278>

[^bungker]: <https://news.hada.io/topic?id=24307#cid46276>

[^nullptr]: <https://news.hada.io/topic?id=24307#cid46315>

[^ifmkl]: <https://news.hada.io/topic?id=24307#cid46282>

[^cm2187]: <https://news.ycombinator.com/item?id=49167654>

[^lamontcg]: <https://news.ycombinator.com/item?id=45892915>

[^world2vec]: <https://news.ycombinator.com/item?id=49166708>

[^shevy-java]: <https://news.ycombinator.com/item?id=49166922>

[^account42]: <https://news.ycombinator.com/item?id=49180430>

[^alex7o]: <https://news.ycombinator.com/item?id=49167615>

[^zoobab]: <https://news.ycombinator.com/item?id=44887044>

[^dncornholio]: <https://news.ycombinator.com/item?id=44887542>

[^re]: <https://news.ycombinator.com/item?id=44886854>

[^ranger_danger]: <https://news.ycombinator.com/item?id=45891460>

[^immibis]: <https://news.ycombinator.com/item?id=45891512>

[^mdaniel]: <https://lobste.rs/s/jvgi1u/ffmpeg_9_0#c_uwjoh6>

[^timschumi]: <https://lobste.rs/s/jvgi1u/ffmpeg_9_0#c_iitbst>

[^sri]: <https://lobste.rs/s/jvgi1u/ffmpeg_9_0#c_uactzb>
