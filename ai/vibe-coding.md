# Vibe Coding

> There's a new kind of coding I call "vibe coding", where you fully give in to
> the vibes, embrace exponentials, and forget that the code even exists.

Andrej Karpathy의 트윗:
<https://twitter.com/karpathy/status/1886192184808149383>

[Replit — What is Vibe Coding? How To Vibe Your App to Life](https://blog.replit.com/what-is-vibe-coding)

[Coding Agents 101: The Art of Actually Getting Things Done](https://devin.ai/agents101)

## Coding Agents

- [GitHub Copilot](https://github.com/features/copilot)
- [Cursor](./cursor.md)
- [Claude Code](../claude/claude-code.md)
- [Codex](../codex)
- [Windsurf Cascade](https://windsurf.com/cascade)
- [Replit Agent](https://replit.com/products/agent)
- [Zencoder](https://zencoder.ai/)
- [Cline](https://cline.bot/) ·
  [README (Korean)](https://github.com/cline/cline/blob/main/locales/ko/README.md)
- [Roo Code](https://roocode.com/) ·
  [README (Korean)](https://github.com/RooCodeInc/Roo-Code/blob/main/locales/ko/README.md)
- [Devin](./devin.md)
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) ·
  [README (Korean)](https://www.readme-i18n.com/ko/All-Hands-AI/OpenHands)

## Spec-Driven Development

[Spec-Driven Development](./spec-driven-development.md)

## Articles

[Most People Can't Vibe Code. Here's How We Fix That. - a16z](https://a16z.com/most-people-cant-vibe-code-heres-how-we-fix-that/)
· [요약](./vibe-coding-for-consumers.md)

[Agentic Coding: How I 10x'd My Development Workflow | by nicolas | Medium](https://medium.com/@dataenthusiast.io/e6f4fd65b7f0)

[What I learned trying seven coding agents](https://www.understandingai.org/p/what-i-learned-trying-seven-coding)

## 비판

### Vibe Coding Is The WORST IDEA Of 2025

[Vibe Coding Is The WORST IDEA Of 2025 - YouTube](https://www.youtube.com/watch?v=1A6uPztchXk)

[Vibe Coding Is The WORST IDEA Of 2025 - SecondB Summary](https://secondb.ai/summary/4541/)

[Dave Farley on X: "Vibe coding might sound trendy, but I think vibe coding might be one of the worst ideas in software engineering and software development in 2025... Listen to my thoughts on #VibeCoding in my latest video on the @ModernSoftwareX channel. (Link in my bio 📽️) https://t.co/Kxa2OI4NR3" / X](https://twitter.com/davefarley77/status/1955690818028683415)

[Toby Lee - 모든 개발자의 필독서인 "모던 소프트웨어 엔지니어링"의 저자인 데이비드 팔리의 바이브 코딩에 대한 비판적인 영상을 봤다. | Facebook](https://www.facebook.com/tobyilee/posts/pfbid032q2pLke5Hxf9bb7nxPFxtMy5dSecSrbNsyvfDU8sYuAQMcV1aX5KUQhzhWCxJiYol)

[박성철 - 코드를 작성과 관련해 컴퓨터 업계는 늘 둘로 나뉘어 있었다. | Facebook](https://www.facebook.com/fupfin.geek/posts/pfbid02cxgfujcuHJjumpGBM1BHopGKfe491D6DsMr33M1KMZimKmxo6vRLMWZCmJhJ4bJ6l)

## Groundhog AI Coding Assistant

<https://github.com/ghuntley/groundhog>

[You are using Cursor AI incorrectly...](https://ghuntley.com/stdlib/)

[From Design doc to code: the Groundhog AI coding assistant (and new Cursor vibecoding meta)](https://ghuntley.com/specs/)

## Beyond Vibe Coding: From Coder to AI-Era Developer

<https://beyond.addy.ie/>

<https://www.oreilly.com/library/view/beyond-vibe-coding/9798341634749/>

## Kent Beck의 Augmented Coding

Kent Beck은 AI 코딩 도구와 협업하는 방식을 **Augmented Coding**(증강 코딩)이라고
부른다. Vibe Coding이 코드 자체를 신경 쓰지 않는 반면, Augmented Coding은 코드
품질, 테스트 커버리지, 복잡성 관리에 집중한다.

> Augmented coding means never having to say no to an idea.

[Augmented Coding: Beyond the Vibes - by Kent Beck](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)

### Taming the Genie 시리즈

Kent Beck은 AI를 "예측 불가능한 지니(Genie)"에 비유한다. 소원을 들어주지만 종종
예상치 못한 방식으로 동작하기 때문이다.

[Taming the Genie: "Like Kent Beck"](https://tidyfirst.substack.com/p/taming-the-genie-like-kent-beck)

#### 지니의 문제점

- **복잡한 상황에서 오작동**: 무한 루프, 테스트 삭제, 구현 위조 등
- **과신(Overconfidence)**: 시스템이 크고 복잡할수록 복잡성의 늪에 빠짐
- **취향(Taste) 부재**: 합리적인 다음 단계라도 요청하지 않은 기능 구현

#### "Like Kent Beck" 프롬프트

AI에게 역할을 부여하는 시스템 프롬프트:

> Act as a senior software engineer who follows Kent Beck's Test-Driven
> Development (TDD) and Tidy First principles.

이렇게 지시하면 AI가 TDD 방식으로 작업하도록 유도할 수 있다.

#### 프롬프트 전략

| 전략                 | 설명                                       |
| -------------------- | ------------------------------------------ |
| 변경 분리            | 구조적 변경과 행동적 변경을 절대 섞지 않음 |
| 컨텍스트 제한        | 다음 단계에 필요한 정보만 제공             |
| Persistent Prompting | 반복되는 지시를 시스템 프롬프트로 고정     |
| 중간 결과 감시       | 비생산적인 개발을 조기에 중단              |

#### 소프트웨어 디자인은 인간 관계의 연습

> Software design is an exercise in human relationships. So are all the other
> techniques we use to develop software.

기술에 능숙해지는 것은 관계에 능숙해지는 한 가지 방법이다.

### 참고 자료

- [Genie Wants to Leap](https://tidyfirst.substack.com/p/genie-wants-to-leap)
- [Persistent Prompting](https://tidyfirst.substack.com/p/persistent-prompting)
- [TDD, AI agents and coding with Kent Beck | The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent)
