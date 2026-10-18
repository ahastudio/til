# PS5LM: 탈옥한 PS5를 집 안의 LLM 서버로 쓰다

<https://ps5lm.cobanov.dev/>

<https://github.com/cobanov/PS5LM>

HN 토론: <https://news.ycombinator.com/item?id=50122431> (227점, 62개 댓글)

GN 토론: <https://news.hada.io/topic?id=35496>

## 소개

PS5LM은 탈옥한 PS5의 GPU에서 llama.cpp를 돌려,
집 안의 노트북, 휴대폰, 코딩 도구에 언어 모델을 제공하는 앱이다.
GGUF 모델을 콘솔 GPU에 올리고 OpenAI와 Anthropic 호환 API로 내놓으며,
실행 중에는 PC도 클라우드도 계정도 필요 없다.[^readme]
라이선스는 GPL-3.0 이상이고, 저장소에는 Sony SDK 파일, 키, 펌웨어,
모델 가중치가 들어 있지 않다.
저장소는 2026년 10월 1일에 만들어졌고,
10월 17일 확인 기준 스타 384개, 포크 68개다.[^gh-api]
abhi245y가 만든 네이티브 GPU 앱(PS5LM Plus)에서 출발했다.[^readme]

## 주요 기능

- llama.cpp의 Vulkan 백엔드로 콘솔의 RDNA 2 GPU에서 실행되고,
  공유 메모리 가운데 11.4GB를 모델과 컨텍스트에 쓴다.
- OpenAI의 `/v1/chat/completions`와 Anthropic의 `/v1/messages`를 제공해
  Claude Code도 붙일 수 있고, 브라우저용 채팅 페이지도 있다.
  `http://<콘솔>:8081`을 가리키면 어떤 모델 이름을 보내든 올라온 모델이 답한다.
- 판단 모델을 올리면 Ollaya가 PC에서 제공하는 `/v1/systemone` API로
  선택, 점수, 예/아니오 질문에 답한다.
- 들어오는 요청이 어느 기기에서 왔는지, 무엇을 물었는지,
  답이 쓰이는 과정을 TV 화면에 채팅처럼 보여 준다.
- 온도, 전력, GPU와 CPU 부하를 최근 2분 또는 1시간 동안 그래프로 보여 준다.
- 각 GGUF를 읽어 남은 메모리에 맞는 가장 긴 컨텍스트와 캐시를 고르고,
  Hugging Face에서 내부 저장소, M.2, USB 드라이브로 직접 내려받는다.
- 이미지 프로젝터가 있는 모델(Gemma 4, MiniCPM-V, d1)은 이미지를 읽는다.[^readme]

PS5 Slim에서 잰 속도는 다음과 같다.[^readme]

| 모델                     | 크기  | 속도                                         |
| ------------------------ | ----- | -------------------------------------------- |
| Qwen 3.5 0.8B, Q4_K_M    | 0.5GB | 초당 207토큰                                 |
| Qwen 3.5 9B, Q4_K_M      | 5.3GB | 초당 55토큰                                  |
| Qwen 3.8 27B, UD-Q2_K_XL | 9.2GB | 초당 약 20토큰, 64k 컨텍스트                 |
| d1 Omni 600M(판단 모델)  | 1.1GB | 질문 3개 0.3초, 720p 이미지와 질문 7개 2.9초 |

## 설치

펌웨어 7.00~13.60의 탈옥한 PS5에 kstuff-lite, etaHEN,
ShadowMountPlus 페이로드가 필요하고,
온도와 전력을 보려면 elfldr, 앱 설치와 모델 복사에는 ftpsrv가 권장된다.[^readme]

1. 최신 릴리스에서 `ps5lm-app-vX.Y.Z.zip`을 받아 푼다.
2. `PPSA99575` 폴더를 FTP로 `/data/homebrew`에 복사하면
   ShadowMountPlus가 홈 화면에 PS5LM을 추가한다.
3. PS5LM에서 Models > Suggested로 모델을 받거나,
   `.gguf`를 `/data/PS5LM/models`나 USB의 `PS5LM/models`에 복사한다.
4. 모델을 올리고 Home에 Ready가 뜨면 브라우저나 OpenAI, Anthropic 클라이언트로 접속한다.

## 콘솔이라는 플랫폼의 제약

프로젝트 문서는 테스트 콘솔에서 직접 잰 제약을 꼼꼼히 남겼다.[^console]

### 페이로드로는 큰 모델을 못 돌린다

처음에는 페이로드로 돌렸다.
페이로드 프로세스는 유연 메모리 8GiB 가운데
malloc으로 6.25GiB까지 할당할 수 있었지만,
약 6GiB를 할당하자 홈 화면이 멈췄다.
직접 메모리는 0이었다.
elfldr가 모든 페이로드를 예산 0으로 시작하기 때문이며,
6GiB 넘게 쓰는 홈브루 프로젝트는 모두 네이티브 앱이다.

CPU는 AVX2와 FMA까지 있고 AVX-512는 없으며,
페이로드에 허용된 CPU는 9, 11, 13, 14,
15번 다섯 개뿐이고 시스템 서비스와 공유한다.
llama.cpp 기본값대로 다섯 개 모두에서 바쁜 대기를 하자
시스템 서비스가 응답을 멈추고 콘솔이 두 번 꺼졌다.
그래서 기본 스레드 수를 허용 CPU 수에서 2를 뺀 값으로 하고
폴링을 끄는 패치를 넣었다.

1GB가 넘는 모델은 크기로 예상한 것보다 10~65배 느렸다.
PS5 브라우저가 포그라운드에 있으면
시스템이 백그라운드 페이로드의 메모리를 디스크로 내보냈기 때문이다.
가중치를 `mlock`으로 잠그자 Qwen3.5 2B가 초당 0.9토큰에서
8.5~9.2토큰으로 올랐지만,
2.7GB를 잠그자 콘솔이 멈춰서 페이로드는 1.6GB 넘는 파일을 거부한다.

### 네이티브 앱이 되어서야 GPU를 쓴다

지금의 PS5LM 앱은 페이로드가 아니라 타이틀이다.
직접 메모리 12GiB를 받고, PS5_Vulkan의 RADV 위에서 ggml-vulkan으로 GPU를 쓴다.
RADV는 통합 힙 옵션을 켜면 11.44GiB의 장치 힙 하나를 보고한다.
타이틀이 되면서 새 제약이 생겼다.
`exit()`를 호출하면 SIGSYS로 종료되어서 셸이 닫을 때까지 기다려야 하고,
SDK 스텁에서 다른 라이브러리만 정의한 `isatty` 같은 함수는 null이 되어
llama.cpp의 로그 설정이 주소 0으로 점프했다.

모델을 내려도 GPU 메모리 일부가 해제되지 않아서,
Qwen3.8-27B를 64k로 올렸다 내리면 여유 메모리가 11.01GiB에서 5.77GiB로 줄었다.
그래서 앱은 모델을 바꿀 때 선택을 파일에 적고 자기 자신을 다시 실행한다.

### 내려받기도 쉽지 않다

Sony의 HTTP 라이브러리는 페이로드에서 요청을 보내지 못해
cpp-httplib와 mbedTLS로 대신했다.
커널이 수신 버퍼를 64KB로 제한해서
Hugging Face CDN과 연결 하나로는 초당 0.9MB가 한계였고,
연결 16개로 8MiB 조각을 병렬로 받아 초당 약 12.5MB를 얻었다.[^console]

## 분석

### 게임 콘솔은 가장 싼 통합 메모리 GPU 상자다

PS5는 CPU와 GPU가 같은 메모리를 쓰는 APU 구조다.
PS5LM은 그 공유 메모리 중 11.4GB를 모델에 쓰며,
Qwen 3.8 27B를 2비트로 줄여 64k 컨텍스트로 초당 약 20토큰을 낸다.[^readme]
이미 거실에 있는 기계라 추가 하드웨어 비용이 없다는 점이
이 프로젝트의 가장 큰 매력이다.

다만 이 숫자는 매우 공격적인 양자화에서 나왔다.
UD-Q2_K_XL이나 UD-IQ2_XXS 같은 2비트대 양자화는
27B 모델을 콘솔에 넣는 유일한 방법이지만 품질 손실도 크다.
같은 메모리로 9B 모델을 4비트로 돌리면 초당 55토큰이 나온다는 점과 함께
어느 쪽이 실제로 더 쓸모 있는지는 용도에 따라 판단해야 한다.

HN의 hypfer는 VRAM이 제한되어 사실상 쓸모없고,
README가 실제로 쓸 만한 것처럼 과장한다고 했다.[^hypfer]
none_to_remain은 초당 20토큰의 2비트 Qwen3.8-27B가
제한적이지만 쓸모없지는 않다며,
오타가 덜 중요한 “이 코드베이스를 읽고 XYZ를 알아내라” 같은 일에
쓰고 있다고 답했다.[^none_to_remain]
jjcm은 서버 오류율 감시, 보안 영상 검토, 식물 물주기 제어처럼
평균보다 조금 못한 지능을 꾸준히 공급하면 되는 장기 작업에 적합하다고 했다.
하루 전기료 70센트로 출력 토큰 약 200만 개를 얻는다는 계산도 덧붙였다.[^jjcm]

### 문서가 프로젝트의 가장 큰 기여다

PS5LM의 `CONSOLE.md`는 페이로드와 타이틀의 메모리 예산,
허용 CPU 마스크, 페이징 동작, 수신 버퍼 상한, 타이틀에서 null이 되는 함수까지
측정값과 오류 코드로 기록한다.[^console]
이는 PS5 홈브루 생태계 전체에 쓸모 있는 지식이다.

특히 페이로드에 직접 메모리가 없는 이유를 elfldr의 소스와 오류 코드로 추적해,
요청이 거부된 것이 아니라 풀이 비어 있는 것이라고 밝힌 부분은
다른 프로젝트가 같은 벽에 부딪혔을 때 시간을 크게 아껴 준다.
“크래시로 하나씩 찾아낸” 제약을 목록으로 남긴 방식은
문서화되지 않은 플랫폼을 다룰 때 따를 만한 본보기다.

## 비평

### 탈옥이라는 전제가 사용자 범위를 크게 좁힌다

PS5LM은 펌웨어 7.00~13.60의 탈옥한 콘솔에서만 실행된다.[^readme]
업데이트를 미루고 익스플로잇 체인을 직접 올려야 하며,
테스트 콘솔의 문서에는
Relapse 커널 단계가 가끔 멈춰 콘솔이 꺼진다고 적혀 있다.[^console]
이는 PS5LM의 문제가 아니라 익스플로잇의 경쟁 상태지만,
사용자 입장에서는 서버가 예고 없이 꺼질 수 있다는 뜻이다.

집 안의 “모델 서버”로 쓰려면 안정성이 중요하다.
온라인 기능을 포기하고 펌웨어를 고정한 콘솔을 서버로 둔다는 것은
대부분의 사용자에게 현실적인 선택이 아니다.

HN의 Rabbit504030201은 Sony가 언제든 페이지를 내리게 할 수 있으니
이런 프로젝트는 GitHub가 아닌 곳에
기본 저장소를 두어야 한다고 했다.[^Rabbit504030201]
Retr0id는 Sony가 탈옥에는 의견이 있겠지만
llama.cpp를 돌리는 사람에게는 관심이 없을 것이라고 답했고,[^Retr0id-ps5]
anigbrowl은 이 저장소가
탈옥 방법을 호스팅하거나 안내하지 않는다고 짚었다.[^anigbrowl]

### 네트워크에 인증 없는 API를 연다

README는 콘솔의 8081 포트로 OpenAI와 Anthropic 호환 API를 제공한다고 설명하지만,
인증이나 접근 제어에 대한 언급은 없다.[^readme]
집 안 네트워크라고 해도, 같은 네트워크의 어떤 기기든
GPU를 쓰고 대화 내용을 TV에 띄울 수 있다는 뜻이다.
요청 내용이 TV 화면에 그대로 표시되는 기능도
공용 공간에서는 사생활 문제가 될 수 있다.

## 인사이트

### 로컬 LLM의 하한선이 “이미 가진 기계”로 내려온다

Mac Studio 클러스터가 로컬 LLM의 상한을 보여 준다면,
PS5LM은 하한을 보여 준다.
이미 거실에 있는 게임기로 9B 모델을 초당 55토큰,
27B 모델을 초당 20토큰으로 돌릴 수 있다면,
로컬 LLM은 새 하드웨어를 사는 문제가 아니라
놀고 있는 하드웨어를 활용하는 문제가 된다.

이 흐름은 게임기에 그치지 않는다.
통합 메모리를 가진 APU라면 어떤 기기든 비슷한 실험의 대상이 될 수 있고,
llama.cpp의 Vulkan 백엔드처럼 이식성 높은 추론 엔진이 그 가능성을 넓힌다.

HN의 shiftpgdn은 PS5 칩을 줄인 AMD APU를 단 채굴용 BC250 보드에서도
이것을 실행할 수 있으며 eBay에서 150~200달러에 구할 수 있다고 했다.[^shiftpgdn]
haunter는 그 가격에 구하기도 어렵고,
조금 더 보태 RTX 3060을 사는 편이 수고를 덜 수 있다고 답했다.[^haunter]
randomblock1은 과거 PS3를 묶어 쓴 클러스터를 떠올렸다.[^randomblock1-ps3]

### API 호환성이 하드웨어를 교체 가능한 부품으로 만든다

PS5LM이 OpenAI와 Anthropic API를 모두 흉내 내는 덕에
Claude Code나 opencode 같은 도구가 아무 수정 없이 콘솔에 붙는다.[^readme]
추론 서버의 API가 사실상 표준이 되면서,
모델을 어디서 돌리는지는 클라이언트에게 보이지 않는 세부가 되었다.
게임기든 Mac이든 클라우드든, 같은 엔드포인트만 내놓으면
코딩 에이전트에게는 모두 같은 서버다.

---

[^readme]: cobanov/PS5LM, [README.md](https://github.com/cobanov/PS5LM/blob/main/README.md), 2026-10-17 확인

[^gh-api]: GitHub API, [cobanov/PS5LM](https://api.github.com/repos/cobanov/PS5LM), 2026-10-17 확인

[^console]: cobanov/PS5LM, [docs/CONSOLE.md](https://github.com/cobanov/PS5LM/blob/main/docs/CONSOLE.md), 2026-10-17 확인

[^hypfer]: <https://news.ycombinator.com/item?id=50125016>

[^none_to_remain]: <https://news.ycombinator.com/item?id=50125366>

[^jjcm]: <https://news.ycombinator.com/item?id=50125287>

[^Rabbit504030201]: <https://news.ycombinator.com/item?id=50123827>

[^Retr0id-ps5]: <https://news.ycombinator.com/item?id=50124070>

[^anigbrowl]: <https://news.ycombinator.com/item?id=50127567>

[^shiftpgdn]: <https://news.ycombinator.com/item?id=50123946>

[^haunter]: <https://news.ycombinator.com/item?id=50124114>

[^randomblock1-ps3]: <https://news.ycombinator.com/item?id=50123097>
