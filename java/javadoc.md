# Javadoc

<https://www.oracle.com/java/technologies/javase/javadoc-tool.html>

<https://docs.oracle.com/en/java/javase/16/javadoc/javadoc.html>

## 주석을 쓰면 안 좋다고 하던데?

<https://codesoom-group.slack.com/archives/C015Y4HM1J8/p1629638188092500?thread_ts=1629622504.081000&channel=C015Y4HM1J8&message_ts=1629638188.092500>

> Javadoc은 엄밀히 말하면 주석보다는 문서화에 대한 겁니다. 코드를 보는 사람이
> 어려운 코드를 이해할 수 있도록 주석을 다는 경우가 많은데, 이런 걸 지양하자는
> 게 주석 최소론자(?)들의 주장인 거죠. Javadoc은 코드를 읽는 걸 돕는 게 아니라,
> 그냥 사용자가 해당 API를 사용할 수 있도록 돕는 거죠. 목적이 다릅니다. 특히,
> 사용자 입장에서 작성하는 걸 통해 더 나은 설계를 이끌어낼 수 있습니다. 테스트
> 코드도 동일한 관점을 통해 살아있는 문서로 기능하는데, Go 같은 경우엔 아예
> 테스트 코드가 문서에 예제로 바로 들어가게 함으로써 정점을 찍어버렸죠.
