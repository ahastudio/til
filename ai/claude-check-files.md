# Claude 파일 확인 도구: 파일에 붙은 C2PA 콘텐츠 자격 증명만 읽는다

<https://claude.com/check-files>

HN 토론: <https://news.ycombinator.com/item?id=49535201> (188점, 132개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ayatfy/check_if_file_was_made_with_claude> (5점, 2개 댓글)

## 소개

Anthropic이 공개한 웹 도구로, 파일이 Claude로 만들어졌는지 확인한다.
처음에는 `claude.com/check-content`라는 주소였고, 지금은 `claude.com/check-files`로 영구 리디렉션된다.
파일을 끌어다 놓으면 브라우저 안에서 검사하고, 파일은 기기를 떠나지 않는다고 페이지는 밝힌다.

지원 형식은 JPG, PNG, GIF, WEBP, TIFF, HEIC, AVIF, SVG, DNG, JXL 이미지, MP4, MOV, AVI 영상, WAV, MP3, M4A, FLAC 오디오이고, 크기는 100MB까지다.
텍스트는 검사하지 않는다.
Claude는 텍스트에 글 자체에 들어가는 워터마크를 넣고, 그것은 EU 법에 따라 대상 조직에 비공개 프리뷰로 제공되는 탐지 API로 확인한다고 페이지는 설명한다.
표시 체계 전반과 그 한계는 도움말 문서를 다룬 `ai/claude-content-marking.md`에 정리했다.

이 도구가 약속하는 것은 좁다.
파일에서 Claude의 콘텐츠 자격 증명(Content Credential)을 찾으면, Claude가 그 파일을 만들었거나 처리했을 수 있다고 알려 준다.
그 밑의 내용을 누가 썼는지는 알려 주지 않고, 사용자를 식별하는 정보도 담고 있지 않다.

## 동작 방식

### 자격 증명이 붙는 곳

Claude가 PNG, JPG, SVG 같은 지원 형식의 파일을 만들면, 파일 메타데이터에 이 파일이 Claude로 만들어졌거나 처리되었을 수 있다는 작고 암호학적으로 서명된 메모를 붙인다.
이것은 카메라 제조사와 사진 편집 소프트웨어가 이미지의 출처를 기록하는 데 쓰는 개방형 산업 표준 C2PA이고, C2PA를 아는 도구라면 무엇이든 읽을 수 있다.

HN에서 declawclaw는 직접 보는 방법을 알려 줬다.[^declawclaw]
claude.ai에서 고양이 이미지를 만들어 달라고 하면 내려받을 때 SVG와 PNG 두 판을 주는데, 둘 다 메타데이터가 있다.
SVG에서는 여는 태그 바로 뒤에 서명이 그대로 들어 있고, PNG에서는 `caBX` 청크에 들어 있다.

### 검사가 도는 곳

페이지는 검사기가 파일 자체가 아니라 붙은 자격 증명만 읽으며, 파일은 저장되거나 다른 용도로 쓰이지 않는다고 적는다.
simonw는 이 도구가 WebAssembly로 돌고, 그 WASM이 콘텐츠 진위성 이니셔티브의 Rust 라이브러리 `c2pa-rs`를 컴파일한 것이라고 확인했다.[^simonw]
브라우저 밖으로 파일을 보내지 않는다는 설명이 구현으로 뒷받침되는 셈이다.

### 해시 조회가 아니라 서명 검증이다

ramon156은 Anthropic이 자기 쪽에 파일 해시가 있는지 확인하는 줄 알았다고 적었다.[^ramon156]
그렇지 않다.
검사기는 파일에 들어 있는 서명을 Anthropic의 공개 키로 검증할 뿐, Anthropic이 만든 모든 출력의 기록을 조회하지 않는다.
mohamedkoubaa가 모든 출력의 체크섬을 저장하면 되지 않느냐고 묻자 xigoi는 그것은 아마 개인정보 법을 어길 것이라고 답했다.[^xigoi]
lxgr는 C2PA와 텍스트 워터마크 모두 상태 없이 검증할 수 있어서, 특정 파일이 존재하는지 알아내는 식의 공격 경로가 되지 않는다고 설명했다.[^lxgr]

## 확인하기

### 자격 증명을 직접 읽어 보기

```bash
# C2PA 자격 증명을 읽는 공식 CLI(c2pa-rs 기반)
cargo install c2patool

# claude.ai에서 받은 이미지의 매니페스트를 JSON으로 본다
c2patool cat.png

# 다시 저장하면 자격 증명이 어떻게 되는지 확인한다(ImageMagick)
magick cat.png -strip cat-resaved.png
c2patool cat-resaved.png   # 매니페스트가 사라졌는지 확인한다
```

### 이 도구로 음성 결과가 나오는 경우를 알아 두기

- Claude Code가 ImageMagick이나 ffmpeg 같은 명령으로 만든 파일은 그 도구가 만든 것이므로 자격 증명이 없다.
- 채팅에서도 모델이 SVG를 쓴 뒤 다른 경로로 렌더링했다면, 어느 단계의 파일인지에 따라 결과가 달라진다.
- 스크린샷, 다시 저장, 메신저 전송, 메타데이터 제거는 모두 자격 증명을 지운다.

## 트레이드오프

### 떼기는 쉽고 위조는 어렵다

coffeecoders는 C2PA 데이터를 떼는 것은 쉽지만 위조하는 것은 어렵다는 점이 흥미롭다고 적었다.[^coffeecoders]
파일을 다시 저장하면 Claude가 만들었다는 신호가 사라지지만, Anthropic의 서명 키 없이는 아무 파일이나 Claude가 만든 것처럼 보이게 할 수 없다.
그래서 이 보증은 한 방향이다.
서명이 있으면 강한 신호이고, 서명이 없으면 거의 아무것도 말해 주지 않는다.

Tiberium은 이것이 Claude가 처리한 파일의 C2PA일 뿐 텍스트 워터마크와는 관계가 없고, SynthID처럼 숨겨진 워터마크와 달리 파일 메타데이터라 쉽게 떼어 낼 수 있다고 정리했다.[^Tiberium]
mhitza는 그것이 EU AI Act에서 회사의 책임이 끝나는 지점이고, 비밀 워터마크가 없는 것이 옳다고 답했다.[^mhitza]

### 위조는 어렵지만 서명을 받아 내기는 쉽다

Retr0id는 서명 키가 필요 없다고 반박했다.[^Retr0id-2]
자기 파일을 올리고 이 파일을 그대로 다시 달라고 하면 Anthropic이 원하는 것에 서명해 준다는 것이다.
페이지가 만들었거나 처리했을 수 있다고 조심스럽게 쓴 이유가 여기에 있다.
자격 증명은 Claude가 이 파일을 거쳤다는 것을 증명할 뿐, Claude가 이 내용을 만들었다는 것을 증명하지 않는다.

이 구분은 실제 쓰임에서 중요하다.
사람이 찍은 사진이나 직접 그린 그림을 Claude에게 보여 주고 조금 다듬어 달라고 하면, 결과물에는 Claude의 자격 증명이 붙을 수 있다.
그 파일을 AI가 만든 것으로 판정하면, 사람의 작업이 AI 생성물로 분류된다.

### 서명이 없는 것을 의심하는 날은 카메라가 서명할 때 온다

advisedwang은 C2PA의 목표가 카메라도 자격 증명을 내보내는 것이라며, 그러면 세 가지 상황이 생긴다고 적었다.[^advisedwang]
C2PA가 사진이 진짜라고 확인하는 경우, AI가 만들었다고 확인하는 경우, 그리고 C2PA가 없어 알 수 없는 경우다.
그는 서명이 없다는 것을 의심스럽게 보는 것은 일부 상황에서만 일어날 것이라고 봤다.

지금은 대부분의 파일에 서명이 없으므로, 없다는 것은 정보가 아니다.
이 도구의 가치는 서명이 있는 파일이 늘어날수록, 그리고 사람이 만든 콘텐츠에도 출처를 증명하는 서명이 붙을수록 커진다.
그 전까지 이 도구는 Claude를 거친 파일을 찾을 수는 있어도, Claude를 거치지 않은 파일을 가려낼 수는 없다.

## 함정

### 도구가 음성이라고 해서 Claude가 만들지 않은 것은 아니다

cmiles8은 Claude로 그림을 만들어 넣었더니 Claude가 만들었다는 증거가 없다고 나왔다며, 이 도구는 쓸모없어 보인다고 적었다.[^cmiles8]
vb-8448도 Simon Willison의 펠리컨 그림 하나를 넣었더니 Claude가 처리한 흔적을 찾지 못했다는 결과를 받았다.[^vb-8448]
Retr0id는 언제 메타데이터가 붙느냐고 물으며, Claude Code CLI는 미디어 파일이 필요할 때 대개 ImageMagick이나 ffmpeg 명령을 실행하는데 그러면 C2PA 메타데이터가 붙지 않는다고 지적했다.[^Retr0id]
자격 증명은 Claude의 특정 생성 경로에서만 붙는다.
모델이 코드를 써서 다른 프로그램으로 파일을 만들면, 그 파일은 그 프로그램의 것이다.

### PDF와 문서는 검사하지 않는다

nixlaz는 PDF를 확인할 수 없다며, 사람들의 주된 용도는 문서가 LLM으로 만들어지거나 편집되었는지 확인하는 것 아니냐고 물었다.[^nixlaz]
tom1337은 Excel과 PDF에 대한 수동 단서로 작성자 정보를 보라고 알려 줬다.[^tom1337]
Claude는 PDF를 wkhtmltopdf로 만들어 PDF 생성기가 Qt, 콘텐츠 작성자가 wkhtmltopdf로 찍히고, xlsx는 openpyxl로 만들어 메타데이터의 작성자가 그것이 된다는 것이다.
하지만 이것은 서명이 아니라 흔한 도구의 흔적일 뿐이라, 같은 도구를 쓴 사람의 파일과 구별되지 않는다.

### 텍스트를 넣어도 아무것도 알 수 없다

RIMR는 주된 기능이 LLM 텍스트의 워터마크인데 이 도구는 텍스트 형식을 받지 않는다고 지적했다.[^RIMR]
페이지 스스로 텍스트는 검사하지 않는다고 적는다.
텍스트 워터마크는 huhtenberg가 인용했듯 임의의 난수 생성기 대신 비밀 키와 앞의 몇 단어로 다음 단어를 정하는 방식이라,[^huhtenberg] 파일 메타데이터가 아니라 단어 선택의 통계에 들어 있다.
Lobste.rs에서 mdaniel은 제공자가 쥔 키로 씨를 뿌린 의사 난수 생성기 덕분에 그 단어 순서가 자기 모델에서 나왔다는 것을 통계적으로 유의하게 알 수 있다는 원리를 설명한 영상과 Nature 논문을 소개했다.[^mdaniel]

## 기억할 원칙

### 출처 증명과 탐지는 다른 문제다

HN에서 lxgr는 C2PA가 워터마킹과 다른 문제, 즉 진위성과 출처를 푼다고 정리했다.[^lxgr-2]
이 구분이 이 도구를 올바르게 쓰는 기준이다.
출처 증명은 서명이 있는 파일에 대해 누가 그것을 거쳤는지 말해 준다.
탐지는 서명이 없는 파일에 대해 AI가 만들었는지 추정한다.
이 도구는 앞의 것만 한다.

shujip의 말이 그다음 단계를 가리킨다.[^shujip]
워터마크는 이 모델이 파일을 건드렸는가에 답하지만, 사람이 그것을 읽고 책임지는가에는 답하지 않는다.
어떤 표시 체계도 그 질문을 대신하지 못하고, 결국 쓸모 있는 확인은 내보내기 전에 여기에 내 이름을 걸겠느냐는 사람의 판단이다.

---

[^declawclaw]: <https://news.ycombinator.com/item?id=49539817>

[^simonw]: <https://news.ycombinator.com/item?id=49540160>

[^ramon156]: <https://news.ycombinator.com/item?id=49537319>

[^xigoi]: <https://news.ycombinator.com/item?id=49539884>

[^lxgr]: <https://news.ycombinator.com/item?id=49538938>

[^coffeecoders]: <https://news.ycombinator.com/item?id=49538370>

[^Tiberium]: <https://news.ycombinator.com/item?id=49536575>

[^mhitza]: <https://news.ycombinator.com/item?id=49537712>

[^Retr0id-2]: <https://news.ycombinator.com/item?id=49538882>

[^advisedwang]: <https://news.ycombinator.com/item?id=49539105>

[^cmiles8]: <https://news.ycombinator.com/item?id=49540009>

[^vb-8448]: <https://news.ycombinator.com/item?id=49540696>

[^Retr0id]: <https://news.ycombinator.com/item?id=49537392>

[^nixlaz]: <https://news.ycombinator.com/item?id=49537680>

[^tom1337]: <https://news.ycombinator.com/item?id=49537808>

[^RIMR]: <https://news.ycombinator.com/item?id=49539643>

[^huhtenberg]: <https://news.ycombinator.com/item?id=49541637>

[^mdaniel]: <https://lobste.rs/s/ayatfy/check_if_file_was_made_with_claude#c_rb4zp8>

[^lxgr-2]: <https://news.ycombinator.com/item?id=49538901>

[^shujip]: <https://news.ycombinator.com/item?id=49536418>
