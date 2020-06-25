# Given-When-Then

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글: [비트코인, 그 시작과 미래](http://j.mp/2ROLSJM)
- 다음 글: [강화학습 발 담그기 (by tura)](http://j.mp/2AnrwQW)

## 시작하며

테스트 코드를 작성한다고 하면 뭘 어떻게 시작해야 할지 모르겠다고 하는 경우를
많이 봤습니다.
망설임이 있을 때 가장 좋은 방법 중 하나는 템플릿을 사용하는 거죠.
정해진 틀을 보고 내가 가진 문제를 채워넣는 게
자유롭게 마음껏 쓰라고 하는 것보다 훨씬 쉽고,
더 나은 결과를 내는 경우가 많습니다.

이 글에서는 유명한 템플릿인 “Given-When-Then”을 소개하겠습니다.

## Specification By Example

테스트는 왜 하는 걸까요? 버그를 찾기 위해서 하는 거죠.

그렇다면 버그는 무엇일까요?

우리가 의도한 것과 다른 일이 벌어졌을 때, 우리는 버그가 발생했다고 합니다.
명세와 다른 프로그램 또는 명세가 불완전해서 알 수 없는 방식으로 작동하는
프로그램이 바로 버그가 발생하는 프로그램이죠.

올바른 명세가 있다면, 그걸 확인하는 테스트 코드를 작성하는 건 쉬울 겁니다.
바로 확인할 수 있는 명세가 있다면, 빠진 부분이 있는지 확인하는 것도
비교적 쉬울 겁니다.

명세는 코드가 아닙니다. 그래서 모호함이 숨어있을 수 있죠.
그걸 더 명료하게 만드는 방법은 예제를 활용하는 겁니다.

## 무슨 일이 벌어지나

아주 간단한 예를 들어보죠.

> 전자렌지에 3분만 돌리면 완성!

여기서 우리가 해야 하는 건 뭔가요?

> 전자렌지에 3분만 돌리면

그럼 무슨 일이 벌어지죠?

> 완성!

Ruby로 간단한 코드를 작성해 볼까요?

```ruby
# When
food = cook(3.minutes)

# Then
assert food.complete?
```

아주 간단합니다.

## 준비가 필요합니다

그러고 보니 전자렌지를 먼저 준비하는 게 빠진 것 같네요.

> 700W 전자렌지를 준비해서 3분만 돌리면 완성!

좋습니다. 이렇게 하니 모호함이 하나 줄어든 것 같아요.

간단히 코드로 옮겨보죠.

```ruby
# Given
stove = Stove.new(700.watts)

# When
food = stove.cook(3.minutes)

# Then
assert food.complete?
```

## 상황을 더 눈에 띄게

어떤 상황인지 약간 더 눈에 띄게 바꿔봅시다.

> Given - 700와트 전자렌지를 준비하고, 3분이란 시간이 주어졌을 때\
> When - 주어진 시간동안 전자렌지를 돌리면\
> Then - 요리가 완성된다.

코드로 옮겨보면 다음과 같습니다.

```ruby
# Given
power = 700.watts
time = 3.minutes
stove = Stove.new(power)

# When
food = stove.cook(time)

# Then
assert food.complete?
```

# 태세전환

상황을 좀 바꿔볼까요?

만약 1분만 돌리면 어떻게 될까요? 완성되지 않게 합시다.

여러 상황이 등장하니 여기선 RSpec으로 모양만 잡아보도록 하겠습니다.

```ruby
decribe 'Stove#cook' do
  context 'with enough time' do
    before(:each) do
      # Given
      @power = 700.watts
      @time = 3.minutes
      stove = Stove.new(@power)
    end

    it 'returns a complete food' do
      # When
      food = stove.cook(@time)

      # Then
      assert food.complete?
    end
  end

  context 'with not enough time' do
    before(:each) do
      # Given
      @power = 700.watts
      @time = 1.minute
      stove = Stove.new(@power)
    end

    it 'returns an incomplete food' do
      # When
      food = stove.cook(@time)

      # Then
      assert !food.complete?
    end
  end
end
```

이렇게 하니 만약 5분을 돌리면 어떻게 될까도 궁금하네요.
자꾸 떠오르는 생각이 있을 거고, 바로 실행해서 확인하면 됩니다.

## let

아까 작성한 코드엔 중복이 보이네요.
[예전에 다룬 RSpec의 `let`](http://j.mp/2gvIbWD)을 이용해서 정리해 봅시다.

```ruby
decribe 'Stove#cook' do
  let(:stove) { Stove.new(power) }

  subject { stove.cook(time) }

  context 'with enough time' do
    let(:power) { 700.watts }
    let(:time) { 3.minutes }
    it { is_expected.to be_complete }
  end

  context 'with not enough time' do
    let(:power) { 700.watts }
    let(:time) { 1.minute }
    it { is_expected.not_to be_complete }
  end
end
```

코드에 대한 부담이 줄어들고 의도가 좀더 명확하게 잘 보이니
전자렌지를 1000W로 바꾸거나 여러 시도를 해볼 수 있을 것 같죠?

## 정리하며

When - Then, 또는 거기서 확장된 Given - When - Then은
테스트 코드를 먼저 작성하는 작업을 명세를 명확히 하는 작업으로 바꿔줍니다.
사실 대부분은 테스트 코드를 어떻게 써야 할지 모르는 게 아니라,
우리가 하려는 작업을 내가 올바르게 이해하고 있지 못한 게 아닐까요?
약간만 시간을 내서 Given - When - Then 템플릿에 맞춰서
내가 하려는 게 뭔지 생각해 보면 좋을 것 같습니다.

## See also

- [Martin Fowler - Given When Then](http://j.mp/2RHlgdw)
- [Cucumber - Gherkin Reference](http://j.mp/2RSVUtv)
- [코딩을 하기 전에 해야 할 일](https://youtu.be/N4FV788fNiQ)
- [내가 한 일 증명하기](https://youtu.be/wd8OmjB_eUI)
- [Ginkgo - Go 언어 개발자를 위한 BDD 테스팅 프레임워크](https://youtu.be/gfTsSBRvdqI)
- [TDD on Spring ~ 봄에는 TDD ~](https://youtu.be/-hqiLswBiY8)
- [Test first!](http://j.mp/1Puv8O9)

---

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글: [비트코인, 그 시작과 미래](http://j.mp/2ROLSJM)
- 다음 글: [강화학습 발 담그기 (by tura)](http://j.mp/2AnrwQW)
