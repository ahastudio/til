# Qualcomm Cloud AI 100 Ultra: 128GB 메모리를 150W 카드에 담았다는 추론 가속기

<https://www.qualcomm.com/data-center/products/cloud-ai-100-ultra>

HN 토론: <https://news.ycombinator.com/item?id=50370654> (164점, 60개 댓글)

GN 토론: <https://news.hada.io/topic?id=36652>

## 소개

Cloud AI 100 Ultra는 Qualcomm이 데이터센터용으로 내놓은 AI
추론(inference) 카드다.
Qualcomm은 이 카드를 Cloud AI 100 제품군에서 가장 새로운 제품이라고 소개하며,
생성형 AI와 대규모 언어 모델(LLM)을 겨냥해 성능과 비용을 함께 최적화한 추론
솔루션이라고 주장한다.
회사는 카드당 최대 576MB의 온다이 SRAM과 64개의 AI 코어를 갖추었고,
컴퓨터 비전과 자연어 처리부터 트랜스포머 기반 LLM까지 폭넓은 작업에 맞게
프로그래밍할 수 있다고 말한다.
이 문서에서 제품 수치는 모두 Qualcomm이 제시한 값이며,
독립적으로 측정된 결과는 아니다.

회사가 공개한 사양표에서 AI 100 Ultra 행은 다음과 같다.

| 항목                         | 값                              |
| ---------------------------- | ------------------------------- |
| 폼 팩터                      | PCIe FH3/4L (111.2mm x 237.9mm) |
| 전력(TDP)                    | 150W                            |
| 정수 연산 최대치(INT8)       | 최대 870 TOPS                   |
| 부동소수점 연산 최대치(FP16) | 최대 288 TFLOPS                 |
| SRAM                         | 576 MB                          |
| DRAM(ECC 포함)               | 128 GB LPR4x                    |
| DRAM 대역폭                  | 548 GB/s                        |
| 호스트 인터페이스            | PCIe Gen4, 16 레인              |

같은 표에는 AI 80 Ultra(150W, 128GB, 548GB/s, INT8 최대 618 TOPS),
AI 100 Pro(75W, 32GB, 137GB/s, 400 TOPS), AI 100 Standard(75W, 16GB, 137GB/s,
350 TOPS), AI 80 Standard(75W, 16GB, 137GB/s, 190 TOPS)가 함께 실려 있다.
메모리 종류는 회사 표에 `LPR4x`로 적혀 있으며, 이 문서는 표기를 그대로 옮긴다.

Qualcomm은 카드와 함께 쓰는 소프트웨어로 AI Inference Suite를 안내한다.
회사는 이것을 온프레미스와 클라우드 배포를 아우르는 소프트웨어와 서비스
묶음이라고 설명하며, OpenAI 호환 API, 사용자 관리 기능,
채팅과 이미지 생성과 멀티모달 AI와 검색 증강 생성(RAG)을 지원하고 Kubernetes나
bare-metal 컨테이너로 배포한다고 말한다.
Qualcomm의 제품 소개에는 구매(Buy Now) 버튼이 있으나 가격은 적혀 있지 않다.
출시 시기와 가격은 아래 HN 댓글에서 다룬다.

## 분석

### 용량을 대역폭보다 앞세운 설계라는 해석

사양표에서 눈에 띄는 것은 128GB 용량 대비 548GB/s라는 대역폭이다.
HN에서 zrm은 이 카드가 소비자용 GPU와 비슷한 모양이면서 GDDR나 HBM 대신 채널을
늘린 일반 DRAM을 쓰는 설계로 보인다고 했고,
같은 방식을 Apple이 쓴다고 짚었다.[^zrm]
zamadatix는 Intel D270, Nvidia DGX Spark,
AMD Strix Halo도 같은 방식이어서 흔해지고 있다고 덧붙였다.[^zamadatix]

이 문서의 계산으로, 가중치가 메모리 128GB를 가득 채우는 밀집(dense) 모델이면
토큰 하나를 만들 때마다 가중치 전체를 한 번 읽어야 하므로 548을 128로 나눈 약
4.3회가 한 스트림의 초당 읽기 횟수 상한이다.
이는 단일 요청을 가정한 이론적 상한이고 실제 속도는 아니다.
한편 INT8 870 TOPS를 548 GB/s로 나누면 바이트당 약 1,590회의 연산이 된다.
연산 능력에 비해 대역폭이 좁은 구성이므로,
같은 가중치를 여러 요청에 재사용하는 일괄 처리나 토큰을 한꺼번에 처리하는
프리필(prefill) 단계에 유리하다는 해석과 맞는다.

zozbot234는 이 점을 설명했다.
높은 연산 능력과 낮은 대역폭 구성은 산술 강도(arithmetic intensity)를 높여
주므로 프리필에 좋고, 디코딩(decode)은 병렬도를 높이거나 추측 디코딩(speculative
decoding)으로 보완할 수 있어 플랫폼이 못 쓰게 되지는 않는다고 했다.[^zozbot234]
dist-epoch는 최신 추론 스택이 디코딩과 프리필에 서로 다른 GPU를 쓰며,
이 카드는 프리필에 적합하다고 했다.[^dist-epoch]
이 두 해석은 사양표에서 이 문서가 얻은 계산과 방향이 같지만,
실제 소프트웨어 스택에서 그 이점이 나오는지는 확인되지 않았다.

### 카드 하나가 여러 칩이라는 점이 메모리 해석을 바꾼다

AI 80 Ultra 행에는 INT8 618 TOPS 옆에 칩(SoC)당 155 TOPS가 병기되어 있고,
618을 155로 나누면 약 4다.
따라서 Ultra 카드는 SoC 네 개로 구성된다는 것이 이 문서의 추론이다.
Qualcomm은 이를 명시하지 않았다.

이 추론이 맞다면 128GB와 548GB/s가 카드 전체에서 하나의 공유 풀인지,
SoC마다 나뉜 메모리인지가 성능을 좌우한다.
mciancia는 카드 8장이면 1TB와 4.4TB/s가 된다고 했고,
PhunkyPhil은 대역폭이 그렇게 합쳐지지는 않으며 카드 사이에 데이터가 오간다고
반문했다.[^mciancia][^PhunkyPhil]
throwawayffffas는 가중치를 층 단위로 나누면 앞 GPU가 끝나기를 기다려야 하고,
텐서 단위로 나누면 유효 대역폭이 장치 수에 가까워지지만 동기화와 리듀스 비용이
생긴다고 설명했다.[^throwawayffffas]
회사 사양표만으로는 어느 쪽 설계인지 판단할 수 없다.

### 출시 시기는 오래되었고 지금도 구매할 수 있는 제품이다

varispeed는 사양이 이미 낡았고 새로운 것을 보여 주어야 한다고
비판했다.[^varispeed]
tokepi는 이 칩이 2024년에 출시되어 사양이 낡아 보이는 것이라고 답했고 Cirrascale
같은 클라우드 업체에서 쓸 수 있다고 했다.[^tokepi]
simoncion은 Qualcomm 블로그에 2023년 11월 13일자 소개 글이 있다고
인용했다.[^simoncion]
Qualcomm의 제품 소개에는 출시일이 적혀 있지 않다.
새 제품으로 소개된 카드가 2년 이상 된 사양이라는 점은 댓글이 제시한 정보이며,
이 문서는 해당 블로그를 직접 열어 보지 않았다.

## 비평

### 사양표에는 비교 대상과 실측 값이 없다

Qualcomm이 제시한 것은 최대치(up to)로 적힌 이론 수치뿐이다.
처리량, 지연 시간, 모델별 토큰 속도, 소비 전력의 실제 값은 없고,
비교 대상(Nvidia, AMD의 같은 급 제품)도 없다.
pearl_panel5는 지속적인 추론 부하에서 메모리 대역폭이 사양표 수치만큼 유지되는지
궁금하다고 썼다.[^pearl_panel5]
이 질문에 답하려면 같은 모델과 배치 크기로 잰 독립 벤치마크가 있어야 하며,
이 스레드에서는 나오지 않았다.

비교는 댓글에서 사양만으로 이루어졌다.
throwawayffffas는 MI350P, H200 NVL, RTX PRO 6000이 600W 급이어도 연산 능력은 이
카드의 3~4배라고 했다.[^throwawayffffas-2]
entrope는 RTX PRO 6000이 보통 200~300W 카드이며 전력을 두 배 쓰면서 메모리는
4분의 3, 대역폭은 3배라고 하고, 중형 모델을 올려 두는 데 드는 전력과 사용자당
처리량의 균형이 다르게 보인다고 했다.[^entrope-2]
eyegor는 600W 설정은 곡선의 효율 구간을 크게 벗어나 있어서 조금만 조정하면 150W
근처에서 80~90% 성능을 얻는다고 했다.[^eyegor]
전력 대비 성능 비교는 설정에 따라 결론이 갈리며,
어느 한쪽 수치가 결정적이지 않다.

### 가격과 사용 비용이 가장 중요한 정보인데 페이지에 없다

thway15269037이 가격을 묻자 simlevesque는 회사 웹사이트에서 1센트로 표시된다고
했고, bigwheels는 자신의 조사로 1만~1만 7천 달러라고 했으며 1센트 재고가 8,750개
있다고도 했다.[^simlevesque][^bigwheels]
1센트 표시는 이 문서가 확인하지 못했고,
구매 버튼의 자리표시자일 가능성이 있으나 확인된 것은 아니다.
bigwheels의 범위도 출처가 제시되지 않은 개인 조사다.

임대 가격은 WarOnPrivacy가 인용한 값이 구체적이다.
Cirrascale의 8카드 Ultra 서버(카드당 128GB,
시스템 메모리 512GB)가 월 계약 기준 월 4,699달러,
연 계약 기준 월 3,759달러이고 GPU당 시간당 5.15달러부터라고 했다.[^WarOnPrivacy]
fancyfredbot은 시간당 5달러면 H200을 빌릴 수 있고 H200이 모든 면에서 낫다며 이
카드의 가치를 의문시했다.[^fancyfredbot]
teruakohatu는 외국 GPU에 의존하지 말라는 지시를 받은 고객이라면 H200을 빌릴 수
없다는 점을 들어 이유를 달리 보았다.[^teruakohatu]
이 비교는 임대료만으로는 수요가 어디서 나오는지 설명하지 못한다는 점을 보여
주지만, 가격이 확인되지 않은 상태에서 누가 이 카드를 사는지는 추측일 뿐이다.

### 메모리 용량이 있어도 소프트웨어 지원이 없으면 쓸 수 없다

Qualcomm은 AI Inference Suite를 소개하지만,
지원하는 모델과 프레임워크의 구체적 목록, 성능 최적화 수준,
오픈소스 추론 엔진 지원 여부는 제품 소개에 적지 않았다.
회사는 일반 모델과 독점 모델을 모두 쓸 수 있다고 하나,
어떤 모델이 얼마의 속도로 도는지는 말하지 않는다.
쓰려는 모델이 이 스택에서 돌아가지 않으면 용량이 커도 128GB를 활용할 수
없으므로, 경쟁 제품의 소프트웨어 지원 수준과 나란히 비교해야 한다.
이 스레드에서는 이 질문(실제로 돌려 본 사람의 경험)이 거의 없었다.

## 인사이트

### 이 카드의 쓰임새는 대형 모델을 한 장에 올리는 용량 쪽에서 찾아야 한다

entrope는 이 카드가 단일 높이(single-height) 형태이므로 네 장을 한
워크스테이션이나 서버에 넣으면 512GB와 2TB/s가 되어 현재 많은 LLM에 매력적이라고
했다.[^entrope]
varispeed는 1TB와 5TB/s 정도가 흥미롭다고 했고,
tempest_는 5년 된 GPU도 값이 터무니없어서 많은 기업이 로컬 추론을 포기하고
있다고 했다.[^tempest_]
이 두 반응 사이에 이 제품의 위치가 있다.
최고 성능이 아니라, 가격이 비싼 GPU의 대안으로 용량을 값싸게 확보하는 것이 이
카드의 명분이라는 해석이다.
이 해석이 성립하려면 가격과 소프트웨어 지원이 앞서 말한 조건을 채워야 한다.

### 구형 GPU 가격 급등이 2024년 제품을 새 제품처럼 보이게 만든다

rpcope1은 MI50과 V100 같은 구형 카드까지 다시 찾아 쓰는 상황에서는 2024년 제품이
아주 앞선 기술처럼 보인다고 했고, eyegor는 V100이 이베이에서 1천 달러쯤에
거래되는데 몇 년 전에는 100달러 이하였다고 덧붙였다.[^rpcope1][^eyegor-2]
GPU 공급이 부족하면 출시 후 시간이 지난 가속기도 수요가 생긴다.
이는 제품의 기술적 우위가 아니라 시장의 공급 부족이 제품 가치를 정하는 상황이며,
공급이 풀리면 그 수요는 사라질 수 있다.
따라서 도입 검토는 현재 가격이 아니라 공급이 정상화된 뒤의 비용 대비 성능으로도
해 봐야 한다.

### 구매 전에 확인할 것은 세 가지다

첫째, 판매 가격과 공급 방식이다.
둘째, 내가 쓸 모델이 이 카드의 소프트웨어 스택에서 어느 속도로 도는지를 실제
측정으로 확인해야 한다.
셋째, 메모리가 카드 전체의 공유 풀인지,
SoC별로 나뉘어 있는지를 Qualcomm에 물어야 한다.
세 질문 중 하나라도 답이 불리하면 임대 가격의 비교가 의미를 잃는다.

---

[^zrm]: <https://news.ycombinator.com/item?id=50371541>

[^zamadatix]: <https://news.ycombinator.com/item?id=50372031>

[^zozbot234]: <https://news.ycombinator.com/item?id=50372601>

[^dist-epoch]: <https://news.ycombinator.com/item?id=50371967>

[^mciancia]: <https://news.ycombinator.com/item?id=50371441>

[^PhunkyPhil]: <https://news.ycombinator.com/item?id=50371507>

[^throwawayffffas]: <https://news.ycombinator.com/item?id=50373101>

[^varispeed]: <https://news.ycombinator.com/item?id=50371100>

[^tokepi]: <https://news.ycombinator.com/item?id=50371301>

[^simoncion]: <https://news.ycombinator.com/item?id=50375946>

[^pearl_panel5]: <https://news.ycombinator.com/item?id=50371072>

[^throwawayffffas-2]: <https://news.ycombinator.com/item?id=50374368>

[^entrope]: <https://news.ycombinator.com/item?id=50371281>

[^entrope-2]: <https://news.ycombinator.com/item?id=50373458>

[^eyegor]: <https://news.ycombinator.com/item?id=50375227>

[^simlevesque]: <https://news.ycombinator.com/item?id=50371587>

[^bigwheels]: <https://news.ycombinator.com/item?id=50372339>

[^WarOnPrivacy]: <https://news.ycombinator.com/item?id=50375203>

[^fancyfredbot]: <https://news.ycombinator.com/item?id=50376793>

[^teruakohatu]: <https://news.ycombinator.com/item?id=50377413>

[^tempest_]: <https://news.ycombinator.com/item?id=50371224>

[^rpcope1]: <https://news.ycombinator.com/item?id=50374540>

[^eyegor-2]: <https://news.ycombinator.com/item?id=50375201>
