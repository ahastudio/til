# KoELECTRA-small 텍스트 이진 분류

KoELECTRA는 34GB 한국어 텍스트로 사전학습한 ELECTRA 모델이다. Hugging Face
Transformers 라이브러리로 바로 사용할 수 있다.

<https://github.com/monologg/KoELECTRA>

## ELECTRA

ELECTRA(Efficiently Learning an Encoder that Classifies Token Replacements
Accurately)는 "Replaced Token Detection"이라는 방식으로 사전학습한다.
Generator가 토큰을 생성하고, Discriminator가 각 토큰이 원본인지 대체된 것인지
판별한다. Fine-tuning 시에는 Discriminator를 사용한다.

## KoELECTRA-Small-v3 모델 구조

| 항목                | 값    |
| ------------------- | ----- |
| Hidden Size         | 256   |
| Embedding Size      | 128   |
| Hidden Layers       | 12    |
| Attention Heads     | 4     |
| Intermediate Size   | 1,024 |
| Max Sequence Length | 512   |
| 파라미터 수         | ~14M  |

v3은 모두의 말뭉치(신문, 구어, 문어, 메신저, 웹 등)를 추가로 활용했고, Mecab +
Wordpiece로 어휘를 새로 구축했다.

## 이진 분류(Binary Classification)

`ElectraForSequenceClassification`은 마지막 레이어의 `[CLS]` 토큰을 가져와 분류
헤드(Classification Head)를 거친다.

```
(dense): Linear(256, 256)
(dropout): Dropout(p=0.1)
(out_proj): Linear(256, 2)
```

## 코드 예제

NSMC(Naver Sentiment Movie Corpus, 영화 리뷰)로 fine-tuning된 모델이지만, 감정
표현 패턴은 도메인을 넘어 공유되므로 식당, 병원, 쇼핑 등 일반적인 리뷰에도 추가
학습 없이 적용할 수 있다.

```python
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="daekeun-ml/koelectra-small-v3-nsmc",
)

texts = [
    # 식당
    "음식이 신선하고 직원도 친절해요",
    "위생 상태가 엉망이고 너무 짜요",
    # 병원
    "의사 선생님이 자세히 설명해주셔서 좋았어요",
    "대기 시간이 너무 길고 불친절해요",
    # 쇼핑
    "가격 대비 품질이 정말 좋습니다",
    "배송도 느리고 포장이 엉망이네요",
]

for text in texts:
    result = classifier(text)
    label = result[0]["label"]
    score = result[0]["score"]
    sentiment = "긍정" if label == "1" else "부정"
    print(f"{sentiment} ({score:.2f}): {text}")
```

출력:

```
긍정 (0.95): 음식이 신선하고 직원도 친절해요
부정 (0.93): 위생 상태가 엉망이고 너무 짜요
긍정 (0.94): 의사 선생님이 자세히 설명해주셔서 좋았어요
부정 (0.91): 대기 시간이 너무 길고 불친절해요
긍정 (0.96): 가격 대비 품질이 정말 좋습니다
부정 (0.94): 배송도 느리고 포장이 엉망이네요
```

## 다른 도메인에서의 정확도

NSMC 학습 데이터는 영화 리뷰지만, "좋다", "별로", "엉망" 같은 감정 표현은
도메인에 관계없이 통용된다.

**잘 되는 경우:**

- 감정이 명확한 텍스트 ("정말 좋아요", "최악이에요")
- 일반적인 리뷰 형태의 글 (식당, 쇼핑, 숙소 등)

**잘 안 되는 경우:**

- 도메인 전문 용어에 의존하는 텍스트 ("가성비" → 긍정이지만 맥락에 따라 다름)
- 중립적이거나 모호한 표현 ("그냥 그래요", "보통이에요")
- 반어법이나 풍자 ("와 진짜 대단하시네요^^")

일반 리뷰 감성 분류 용도로는 80~85% 정도 정확도를 기대할 수 있다. 정밀도가
중요하다면 해당 도메인 데이터로 추가 fine-tuning하는 것을 권장한다.

## NSMC 벤치마크

NSMC는 15만 개 학습 데이터와 5만 개 테스트 데이터로 구성된 이진 분류
데이터셋이다. 레이블이 0이면 부정, 1이면 긍정이다.

<https://github.com/e9t/nsmc>

## 참고 자료

[HuggingFace KoElectra로 NSMC 감성분석 Fine-tuning해보기](https://heegyukim.medium.com/huggingface-koelectra%EB%A1%9C-nsmc-%EA%B0%90%EC%84%B1%EB%B6%84%EB%A5%98%EB%AA%A8%EB%8D%B8%ED%95%99%EC%8A%B5%ED%95%98%EA%B8%B0-1a23a0c704af)

[2주 간의 KoELECTRA 개발기](https://monologg.kr/2020/05/02/koelectra-part1/)

[KoELECTRA Fine-tuning](https://github.com/monologg/KoELECTRA/blob/master/finetune/README.md)

[daekeun-ml/koelectra-small-v3-nsmc](https://huggingface.co/daekeun-ml/koelectra-small-v3-nsmc)
