# Gemini 3.8 TTS: 음성 합성을 고정된 목소리 목록에서 연출 스튜디오로 바꾸려는 시도

원문: [Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/)

HN 토론: <https://news.ycombinator.com/item?id=49817615> (329점, 148개 댓글)

GN 토론: <https://news.hada.io/topic?id=34194>

## 요약

Google이 2026년 9월 23일 텍스트 음성 변환(TTS) 모델 두 개, Gemini 3.8 Flash TTS와 Gemini 3.8 Flash-Lite TTS를 발표했다.
글은 Group Product Manager Leland Rechis와 Gemini Audio 팀을 대표한 연구 과학 디렉터 Alan Cowen의 이름으로 나왔다.
발표의 표어는 음성 생성을 고정된 프리셋에서 역동적인 창작 스튜디오로 바꾼다는 것이다.
두 모델은 앞서 나온 3.5 Live Translate, 3.5 Transcribe, 3.8 Live, 3.8 Live Extended Thinking에 이은 Gemini Audio 제품군의 일부다.

두 모델의 역할은 나뉜다.
Flash TTS는 깊은 창작 연출과 캐릭터 설계용으로, 자연어 프롬프트로 새 목소리를 만들고 연기 지시, 속도, 방언 전환, 맞장구를 대사 단위로 조절한다.
Flash-Lite TTS는 대량 처리와 비용 효율용으로, 대량 더빙, 오디오 콘텐츠 제작, 표현력 있는 음성 에이전트에 맞춰졌다.

목소리를 만드는 방법은 네 가지다.
첫째는 생성형 음성 설계로, 100개가 넘는 언어와 방언에서 역할, 억양, 음색을 자연어로 지정해 목소리를 처음부터 만든다.
둘째는 2,000개가 넘는 기성 목소리 라이브러리로, 멕시코 스페인어, 퀘벡 프랑스어, 스코틀랜드 영어 같은 지역 변형을 포함한다.
기존의 목소리는 30개였다.
셋째는 음성 복제로, 자기 목소리나 사용 권리가 있는 목소리를 30초 샘플로 재현하며, 동의 확인, SynthID 워터마크, C2PA 자격 증명이 함께 붙는다.
넷째는 곧 나올 음성 리믹스로, 라이브러리의 목소리를 골라 음색, 음높이, 속도, 억양을 프롬프트로 다듬는다.
만든 목소리는 저장해 프로젝트 사이에서 일관되게 쓸 수 있다.

연출 기능도 있다.
대본에 무대 지시를 직접 쓰거나 Gemini가 자연스러운 대본 신호로 전달 방식을 정하게 할 수 있고, 몇 시간 길이의 오디오에서도 화자 드리프트를 최소로 유지하며, 한 대본으로 두 화자의 대화 장면을 만들고, `<laughs>`, `<sigh>`, `<gasp>` 같은 비언어 신호와 “음”, “네” 같은 맞장구를 넣을 수 있다.

성능 근거로는 세 가지를 든다.
Flash TTS가 Hume AI의 Voice Design Benchmark에서 71.4로 종합 1위, 억양 모델링에서 60.8로 1위를 했고, Hume AI의 Overall Quality Index에서는 Flash TTS와 Flash-Lite TTS가 1위와 2위를 했다.
Voice Arena의 블라인드 인간 선호 평가에서는 일본어, 브라질 포르투갈어, 베트남어, 현대 표준 아랍어, 멕시코 스페인어, 힌디어에서 상위권에 올랐다.
안전 장치로는 음성 복제 전에 목소리 주인의 음성 동의 녹음을 받아 참조 화자와 일치하는지 확인하고, Gemini Audio 모델이 만드는 모든 오디오에 SynthID 워터마크를 넣는다.
AI Studio의 음성 복제는 일리노이, 텍사스, EEA, 영국, 스위스, 인도에서는 쓸 수 없다.
Flash TTS는 Gemini API, Google AI Studio, Gemini Notebook에, Flash-Lite TTS는 Gemini API, Google AI Studio, Google Vids에 풀리고, 두 모델 모두 Gemini Enterprise API에는 곧 들어간다.

## 분석

### 경쟁의 축이 “자연스러운 목소리”에서 “연출할 수 있는 목소리”로 옮겨 갔다

몇 년 전까지 TTS의 경쟁은 목소리가 얼마나 사람 같으냐였다.
그 경쟁은 사실상 끝났다.
Hacker News에서 ttul은 내부 앱의 읽어 주기 기능에서 Eleven v3를 이 모델로 바꿔 봤는데, 표현력이 극도로 풍부하고 자기 귀에는 이미 놀라웠던 Eleven v3와 동급이라고 적었다.[^ttul]
LarsDu88은 수년간 Google Cloud의 WaveNet에서 Azure, ElevenLabs, Fish.audio로 최고 수준을 따라 옮겨 다녔는데 이번 것이 정말 좋다고 했다.[^LarsDu88]

자연스러움이 기본이 되자, 차별화는 통제로 옮겨 간다.
Google이 발표의 대부분을 연기 지시, 대사 단위 연출, 두 화자 장면, 비언어 신호에 쓴 것은 이 이동을 보여 준다.
Hume AI의 벤치마크 가운데 강조한 것도 음성 설계와 억양 모델링, 곧 원하는 목소리를 만들어 내는 능력이다.
목소리를 고르는 시대에서 목소리를 만들고 연기를 시키는 시대로 넘어가고 있다.

Hacker News에서 Multicomp는 자신이 쓰는 긴 Star Trek 팬픽의 장면 파일을 라디오 드라마처럼 읽히게 하려 했지만, GPT-Live로는 인물마다 충분히 다른 목소리를 내고 머릿속에 떠올린 표현을 연출하기 어려웠다며, 이번 모델의 큰 목소리 라이브러리와 연출 기능이 반갑다고 적었다.[^Multicomp]
연출 가능성이 실제 사용자의 막힌 지점이었다는 증언이다.

### 음성 복제를 내놓은 것은 기술보다 시장의 판단이다

Hacker News에서 simonw는 음성 복제가 이제 다른 곳에서도 충분히 널리 쓰이게 되어 Google이 더는 망설이지 않고 내놓은 것 같다고 적었다.[^simonw]
sharktheone은 몇 년 전 Google이 악용이 두려워 한 TTS 모델을 공개하지 않았던 일을 떠올리며, 이제는 별 고민 없이 내놓는다고 꼬집었다.[^sharktheone]
kingstnap은 전날 밤 Qwen TTS 1.7B로 깨끗한 녹음 데이터셋을 만들고 미세 조정 방법을 실험해, 몇 시간 만에 가족이 놀랄 만큼 자기와 똑같은 목소리를 만들었다고 전했다.[^kingstnap]

이 증언들은 Google의 판단 근거를 보여 준다.
누구나 공개 모델로 몇 시간 만에 목소리를 복제할 수 있다면, Google이 복제 기능을 내놓지 않아도 악용은 줄지 않는다.
그렇다면 동의 확인과 워터마크를 붙인 복제 기능을 내놓아 적어도 Google 플랫폼 위의 복제를 추적 가능하게 만드는 편이 낫다.
음성 복제를 막을 수 없는 기술로 받아들이고, 막는 대신 표시하는 쪽으로 방향을 바꾼 것이다.

### 두 모델의 분업은 음성 시장이 둘로 갈라졌다는 인식이다

Flash TTS와 Flash-Lite TTS의 분업은 기능보다 시장을 나눈다.
Flash TTS가 겨냥하는 게임, 오디오북, 팟캐스트, 인터랙티브 미디어는 한 편의 품질이 중요한 창작 시장이다.
Flash-Lite TTS가 겨냥하는 대량 더빙, 오디오 콘텐츠 제작, 음성 에이전트는 초당 비용이 중요한 산업 시장이다.

이 분업은 배포처에서도 드러난다.
Flash TTS는 연구와 창작 도구인 Gemini Notebook에, Flash-Lite TTS는 업무용 영상 도구인 Google Vids에 들어간다.
Agora, LiveKit, Pipecat, Vercel 같은 음성 에이전트 플랫폼과 HeyGen, Wondercraft 같은 더빙과 콘텐츠 회사를 협력사로 든 것도 두 시장을 함께 잡겠다는 뜻이다.

## 비평

### 벤치마크 1위와 데모의 실제 품질 사이에 간극이 있다

Google은 Hume AI의 두 지표에서 1위를 했다고 내세운다.
그러나 Hacker News에서 burkaman은 기술적으로는 놀랍지만 결과가 그다지 좋지 않고 대개 프롬프트와 가깝지 않으며, 거의 모든 예시에서 프롬프트의 핵심 일부가 완전히 무시된다고 평가했다.[^burkaman]
112233은 발표의 “아주 쇳소리 나는 단조로운 로봇 목소리” 예시가 쇳소리도 단조롭지도 않다며, 90년대 TTS나 영화 속 로봇 연기와 비교해 보라고 꼬집었다.[^112233]
dangoodmanUT도 독백 데모에서 대본의 음성 신호가 무시되는 것이 분명히 들린다고 지적했다.[^dangoodmanUT]

이 반응은 벤치마크가 무엇을 재는지에 대한 질문으로 이어진다.
음성 설계 벤치마크의 점수는 생성된 목소리의 전반적인 질을 반영할 수 있지만, 프롬프트에 적힌 조건을 얼마나 따랐는지는 별개의 문제다.
연출 가능성을 핵심 가치로 내세운 발표에서, 정작 연출 지시가 무시되는 예시가 데모에 들어 있다면 벤치마크 1위라는 주장의 무게가 줄어든다.
burkaman의 표현대로, 컴퓨터가 이것을 만들었다는 놀라움이 가시면 결과가 원하던 것이 아니라는 것이 보인다.[^burkaman-image]

### “표현력”을 최고의 가치로 놓는 것은 모든 사용자에게 맞지 않는다

발표는 두 모델을 가장 표현력 있는 오디오 생성 모델이라고 소개한다.
그러나 Hacker News에서 m3kw9은 여전히 AI 같은 소리가 나며, 점수를 잘 받는 표현을 과장해 모든 어조와 끝맺음을 부풀린다고 적었다.[^m3kw9]
qlte는 최신 음성 모델 거의 모두가 가짜로 과장된 표현과 감정 때문에 듣기 힘들다며, 무작위로 강조를 넣어 주의를 흐트러뜨리고, ChatGPT 음성 모델과는 45초 넘게 대화하기 어렵다고 했다.[^qlte]
그가 원하는 것은 오디오북 같은 특수한 경우를 빼면 거의 모든 용도에서 명료하고 기술적으로 흠 없는, 절제된 컴퓨터 목소리다.

이 반응은 발표가 겨냥한 창작 시장과 일상의 TTS 사용 사이의 차이를 보여 준다.
글을 들으며 이동하거나, 음성 비서와 짧게 대화하거나, 화면 낭독기를 쓰는 사람에게 필요한 것은 연기가 아니라 명료함이다.
Hacker News에서 loremm은 TTS 오디오북을 수백 시간 들었지만 머리가 텍스트만으로 인물의 목소리를 채우며, 책에서 인물마다 글꼴이 다르지 않듯 인물마다 목소리가 달라야 하는 것은 아니라고 적었다.[^loremm]
표현력은 한 시장의 가치이지 음성 합성 전체의 가치가 아니다.

### 동의 확인과 워터마크의 한계를 글은 말하지 않는다

글은 음성 복제의 안전 장치로 목소리 주인의 음성 동의 녹음을 받아 참조 화자와 일치하는지 확인한다고 설명한다.
Hacker News에서 accountrequired는 그 동의 녹음을 얼마나 오래 저장하느냐고 물었고,[^accountrequired] kmoser는 합성된 동의 녹음을 잡아낼 수 있느냐고 물었다.[^kmoser]
두 질문 모두 글에 답이 없다.

두 번째 질문은 특히 날카롭다.
공개 모델로 몇 시간 만에 목소리를 복제할 수 있다면, 다른 사람의 목소리로 “나는 동의한다”는 녹음을 만드는 것도 같은 방법으로 할 수 있다.
동의 확인이 복제 기술 자체를 상대로 버틸 수 있는지, 곧 합성 음성을 판별하는지를 글은 설명하지 않는다.
SynthID 워터마크도 Google 모델이 만든 오디오에만 들어가므로, 공개 모델로 만든 복제 음성을 가려내는 데는 쓸 수 없다.

### 가격을 밝히지 않은 발표는 대량 처리 모델의 핵심 정보를 빠뜨렸다

Flash-Lite TTS는 대량 처리와 비용 효율을 위한 모델이라고 소개되지만, 발표문에는 가격이 없다.
Hacker News에서 OutOfHere[^OutOfHere]와 nater5000[^nater5000]은 가격이 어디에도 없다고 지적했다.
thevinter가 댓글로 정리한 가격은 시간당 Flash TTS 표준 0.81달러, 배치 0.41달러, Flash-Lite TTS 표준 0.54달러, 배치 0.27달러였다.[^thevinter]
비용 효율을 모델의 존재 이유로 내세우면서 그 숫자를 발표에 넣지 않은 것은, 가장 중요한 비교 정보를 독자가 따로 찾게 만든다.

## 인사이트

### 음성 복제가 흔해지면 목소리는 신원 확인 수단의 자격을 잃는다

Hacker News에서 talon8635는 이제 AI 이메일 답장에 더해 전화로 지인을 사칭하는 AI까지 받게 되겠다고 적었다.[^talon8635]
이 짧은 반응이 가리키는 결과는 기술 발표의 범위를 넘어선다.
목소리는 오랫동안 사람을 알아보는 가장 자연스러운 방법이었고, 은행 콜센터와 가족 사이의 전화는 목소리를 신원의 근거로 삼아 왔다.

30초 샘플로 목소리를 복제하는 기능이 대형 플랫폼의 기본 기능이 되면, 목소리는 “이 사람이다”라는 증거로 쓸 수 없게 된다.
그 빈자리는 다른 확인 수단, 예컨대 가족끼리 정한 암호나 별도 채널 확인으로 채워야 한다.
Google의 동의 확인은 자기 플랫폼에서의 복제를 통제하지만, 사회 전체가 목소리를 믿는 방식을 바꾸는 비용은 플랫폼 밖에서 치러진다.

### 음성 연출 도구는 이미지 생성 모델이 걸어온 길을 따른다

burkaman은 이 결과를 이미지 모델에 빗댔다.[^burkaman-image]
이미지 생성 모델도 처음에는 사람 같은 그림을 그린다는 것만으로 놀라웠고, 그다음에는 프롬프트를 얼마나 정확히 따르느냐가 경쟁의 축이 됐으며, 결국 참조 이미지, 인페인팅, 제어망 같은 세밀한 통제 도구가 핵심 기능이 됐다.
Gemini 3.8 TTS는 음성이 지금 그 두 번째 단계에 들어섰음을 보여 준다.

이 비유는 다음 단계도 예고한다.
이미지 모델에서 세밀한 통제 도구가 나오자 전문 창작자들이 그것을 작업 흐름에 넣었고, 동시에 저작권과 초상권 분쟁이 커졌다.
음성에서도 연출 도구가 성숙하면 성우와 오디오북 제작 시장이 바뀌고, 목소리의 권리를 둘러싼 분쟁이 늘 것이다.
Hacker News에서 UmYeahNo가 개발자의 일자리 상실은 한탄하면서 성우의 경력에는 무심한 반응을 꼬집은 것도 그 전조다.[^UmYeahNo]

### 로컬 모델이 따라오는 속도가 클라우드 TTS의 해자를 좁힌다

Hacker News 스레드의 상당 부분은 Google 모델이 아니라 로컬 모델 이야기였다.
thangalin은 클라우드도 토큰도 쓰지 않고 여러 인물의 목소리로 책을 읽어 주는 로컬 웹 앱을 소개했고,[^thangalin] freedomben은 Kokoro TTS로 가지고 있던 텍스트 파일을 오디오북으로 만들고 있다고 했으며,[^freedomben] VariousPrograms는 BreezeTTS, Higgs Audio v3, Fish Audio S2 Pro를 써 보라며 여러 모델을 한 번에 돌릴 수 있는 도구를 소개했다.[^VariousPrograms]

클라우드 TTS의 가치는 품질, 연출 도구, 대량 처리 인프라에 있다.
그러나 품질의 격차는 빠르게 줄고 있고, 개인 창작자에게는 시간당 몇 십 센트의 비용보다 로컬에서 무제한으로 돌리는 편이 매력적일 수 있다.
Google이 이 시장에서 지킬 수 있는 것은 모델 자체보다 음성 에이전트 플랫폼과의 통합, Workspace 제품 안의 배치, 그리고 대규모 더빙 같은 산업 수요일 것이다.
Flash-Lite TTS를 Vids에 넣고 에이전트 플랫폼을 협력사로 든 것은 그 방향을 이미 알고 있다는 신호로 읽힌다.

---

[^ttul]: <https://news.ycombinator.com/item?id=49826291>

[^LarsDu88]: <https://news.ycombinator.com/item?id=49819615>

[^Multicomp]: <https://news.ycombinator.com/item?id=49818488>

[^simonw]: <https://news.ycombinator.com/item?id=49818414>

[^sharktheone]: <https://news.ycombinator.com/item?id=49824831>

[^kingstnap]: <https://news.ycombinator.com/item?id=49819865>

[^burkaman]: <https://news.ycombinator.com/item?id=49818934>

[^112233]: <https://news.ycombinator.com/item?id=49818463>

[^dangoodmanUT]: <https://news.ycombinator.com/item?id=49822576>

[^burkaman-image]: <https://news.ycombinator.com/item?id=49819037>

[^m3kw9]: <https://news.ycombinator.com/item?id=49819079>

[^qlte]: <https://news.ycombinator.com/item?id=49822092>

[^loremm]: <https://news.ycombinator.com/item?id=49818502>

[^accountrequired]: <https://news.ycombinator.com/item?id=49819027>

[^kmoser]: <https://news.ycombinator.com/item?id=49819425>

[^OutOfHere]: <https://news.ycombinator.com/item?id=49819422>

[^nater5000]: <https://news.ycombinator.com/item?id=49819014>

[^thevinter]: <https://news.ycombinator.com/item?id=49818639>

[^talon8635]: <https://news.ycombinator.com/item?id=49818506>

[^UmYeahNo]: <https://news.ycombinator.com/item?id=49821238>

[^thangalin]: <https://news.ycombinator.com/item?id=49818395>

[^freedomben]: <https://news.ycombinator.com/item?id=49819974>

[^VariousPrograms]: <https://news.ycombinator.com/item?id=49820311>
