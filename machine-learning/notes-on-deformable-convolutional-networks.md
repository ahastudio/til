원문: [https://medium.com/@phelixlau/notes-on-deformable-convolutional-networks-baaabbc11cf3](https://j.mp/2pCV496)

날림 번역입니다. 피드백은 Issue Tracker에 부탁드립니다:
<https://github.com/ahastudio/til/issues>

# Notes on “Deformable Convolutional Networks”

Dai, Jifeng, Haozhi Qi, Yuwen Xiong, Yi Li, Guodong Zhang,
Han Hu, and Yichen Wei. 2017.
“Deformable Convolutional Networks.” arXiv [cs.CV]. arXiv.
<http://arxiv.org/abs/1703.06211>

- 이 논문은 **변형가능한 컨볼루션**과 **변형가능한 RoI 풀링**이란 새로운 형태를 소개합니다.
논문의 저자들은 기존의 신경망의 일부를 이 모듈로 교체하는 게 쉽다고 주장합니다.
이 모듈은 **역동적이고 학습 가능한 수용 영역**을 효과적으로 갖추고 있습니다.

- **동기**: 논문의 저자는 기존의 CNN 방식들은 크고 알려지지 않은 변형에 본질적으로 불변하고,
기하학적 변형을 학습하려면 더 많은 데이터가 필요하다고 주장합니다.
완전한 컨볼루션 네트웍(FCN)에선 수용 영역을 동적으로 조정할 수 있는 건 특히 중요합니다.

## Deformable Convolution

![Figure 2](https://cdn-images-1.medium.com/max/1600/1*6lBZ5rM1fExa_N_VTtNfXw.png)

오프셋 영역의 화살표는 입력 쪽 특징맵(input feature map)에서
파란 사각형이 어떻게 이동하는지 표현합니다.

- 변형가능한 컨볼루션(Deformable convolution)은 정규 컨볼루션 레이어와
각 입력에 대한 2차원 오프셋을 학습하는 컨볼루션 레이어,
이렇게 2개 부분으로 이뤄져있습니다.
이 그림에서 정규 컨볼루션 레이어는 초록 사각형 대신 파란 사각형에서 가져옵니다.
(역주: 입력 쪽 특징맵을 보면 기존의 CNN에서 볼 수 있는 9개의 초록 사각형과,
어긋나게 그려진 9개의 파란 사각형을 볼 수 있음.)

- 내가 그랬던 것처럼 혼란스럽다면, 변형가능한 컨볼루션을 늘어날 비율을 학습할 수 있고
각 입력에 대해 다를 수 있는 **“학습가능한” 늘어나는(dilated) (atrous) 컨볼루션**이라고
생각하면 됩니다.
변형가능한 컨볼루션과 다른 기법의 관계에 대해 더 알고 있다면 3절을 읽어보세요.

- 오프셋은 정수가 아니기 때문에 입력쪽 특징맵에서 가져올 때
**이중선형보간법(bilinear interpolation)**이 사용됩니다.
논문의 저자는 이게 효율적으로 계산될 수 있다고 주장합니다.
(순방향으로 걸리는 시간은 Table 4 참조.)

- 2차원 오프셋은 채널 차원에 맞춰 인코딩됩니다.
(예를 들어, `n` 채널의 컨볼루션 레이어는 `2n` 채널의 오프셋 컨볼루션 레이어와 짝을 이룹니다.)

- 오프셋은 `0`으로 초기화되고, 오프셋 레이어의 위한 학습률은
정규 컨볼루션 레이어와 같을 필요는 없습니다.
(하지만 논문에서는 기본값으로 주어집니다)

- 논문의 저자들은 변형가능한 컨볼루션이 **커다란 사물의 수용 영역을 “확장”**할 수 있음을
경험적으로 보여줍니다.
그들은 각 오프셋 사이의 평균 거리인 “효과적인 늘어남(effective dilation)”을 측정합니다.
그들은 커다란 사물을 중심으로 하는 변형가능한 필터가 더 큰 “수용 영역”을 갖고 있음을 발견했습니다.
아래를 보세요.

![Figure 5](https://cdn-images-1.medium.com/max/1600/1*umayO8-FFmxcVOHO7uy5iA.png)

Figure 5의 일부.
빨간 점은 변형가능한 컨볼루션 필터가 학습된 오프셋을 통해 추출하는 위치입니다.
녹색 사각형은 그에 대한 출력입니다.
커다란 사물에 적용된 필터는 더 커다란 수용 영역을 갖습니다.

## Deformable ROI Pooling

![Figure 3](https://cdn-images-1.medium.com/max/1600/1*uENf2eOPwtY4BYiuOo4gPg.png)

- 변형가능한 RoI 풀링(Deformable RoI pooling)도
정규 RoI 풀링 레이어와 오프셋을 학습하는 완전연결 레이어, 이렇게 2개 부분으로 이뤄져 있습니다.

- 픽셀 단위의 오프셋 대신, RoI 영역의 가로, 세로 크기 같은 RoI 크기에 대해
불변하는 값으로 정규화된(=나누기한) 오프셋을 사용합니다.

- 정규화된 오프셋을 더 조정하는 묘한 상수값 `gamma`가 있습니다. (?)

## Open Questions / Comments / Thoughts

- 오프셋이 특별히 정규화(regularized)될 필요가 없다는 게 굉장히 인상적이고 놀라웠습니다.
(<http://nyus.joshuawise.com/batchnorm.pdf>와 다르게,
배치 정규화(normalization)는 진짜로 모든 걸 해결할 수 있을 겁니다.)

- 정규 그리드의 오프셋이 [아핀 변환](http://j.mp/2oPCsjw)에 의해
간단히 결정되는 게 흥미롭습니다.
이건 “변형가능성”의 모양은 유지한채 파라미터 수는 현저하게 줄여줘야 합니다.
아마 이전 작업이 있지 않을까요?

- 구현이 매우 효율적으로 보여서 인상적입니다!

- 데이터가 늘어나는 걸 (특히 크기) 변형가능한 컨볼루션을 이용해 줄여주는 연구가 없습니다.
그 연구가 있으면 훨씬 설득력이 있을 겁니다.

- 논문의 저자들이 언급하지 않은 정규 맥스풀링에 변형가능한 오프셋을 적용한 결과가 궁금합니다.

- 딥러닝의 기본 블럭인 컨볼루션에 대한 더 기본적인 연구를 보는 건 놀랍습니다.
최근 사례는 그룹 컨볼루션과 분리가능한 컨볼루션 등이 있습니다.

- 이게 모델 해석가능성이란 면에서 무얼 의미하는지 궁금합니다.

- 실험은 굉장히 잘 됐지만 그림의 일부는 그다지 설명이 되지 않습니다. (예를 들어 Figure 5)

[아래](https://j.mp/2pCV496)에 댓글로 당신의 생각을 알려주세요!
이 논문에 대한 더 많은 기록을 보고 싶으면
[트위터](https://twitter.com/phelixlau)를 팔로우하세요.
