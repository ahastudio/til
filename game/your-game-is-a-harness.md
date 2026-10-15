# 게임 자체가 AI 에이전트의 하네스다

원문: [Your Game Is A Harness - kyle kukshtel's website](https://kylekukshtel.com/ai-harness-engineering-game-development-claude-code)

HN 토론: <https://news.ycombinator.com/item?id=50072120> (171점, 88개 댓글)

GN 토론: <https://news.hada.io/topic?id=35355>

## 요약

Kyle Kukshtel은 15년 가까이 게임 프로그래밍을 해 온 개발자로,
2026년 9월 12일 캘거리의 Indie Rodeo에서
한 45분짜리 발표 “Your Game Is A Harness”를 2026년 10월 10일 글로 옮겼다.
저자는 이 글이 녹취가 아니라 발표 슬라이드만 참고해 100% 직접 썼다고 밝힌다.
출발점은 웹 스택에서는 LLM이 못 하는 일이 거의 없다고 느끼면서도,
게임 작업에 쓰기만 하면 번번이 무너졌다는 경험,
즉 “LLMs are Bad At Games”라는 인상이다.

저자의 진단은 게임에 코드가 아닌 것이 많다는 데 있다.
Three.js 원샷 데모가 잘 되는 이유는 모든 것이 코드이기 때문이고,
전통적인 게임은 에셋, 씬,
런타임 상태처럼 LLM이 들여다볼 수 없는 불투명한 부분에 기대고 있다.
그래서 LLM이 게임을 잘 다루게 하는 문제는
게임이나 LLM의 본성 문제가 아니라 컨텍스트 문제이며,
해법은 게임이라는 블랙박스를 열어 LLM이
직접 다룰 수 있는 형태로 바꾸는 것이라고 주장한다.

구체적인 처방은 다음과 같다.
시드 하나로 모든 난수를 고정하고,
스크린샷을 찍되 UI·게임플레이 레이어를 끌 수 있게 하고,
두 장을 그대로 넘기는 대신 `odiff`로 이미지 차이와
유사도 수치를 뽑아 평가 기준으로 삼는다.
객체 모델은 모든 것을 하나의 `Thing` 타입(fat struct)으로 통일해
저장·불러오기를 단순하게 만들고,
상태 변경은 직렬화 가능한 커맨드 패턴으로 표현해 재생할 수 있게 한다.
정적 데이터는 코드 밖으로 빼 재컴파일 없이 바꾸게 한다.
저자는 Cantata 개발 때 자체 데이터 편집기 Depot으로
비프로그래머 약 7명이 이렇게 작업했다.
시뮬레이션은 엔진과 분리된 별도 DLL로 두어 엔진은 커맨드를 보내고
결과 상태만 받아 그리는 “Blackbox Game Architecture”를 따른다.
성능은 사람이 보는 GUI 프로파일러 대신 텍스트로
결과를 내보내는 `samply`를 쓰게 한다.

이 조각들을 합치면 에이전트 한 턴이 결정적 입력, 컴파일 없는 수정, 격리된 검증,
영향 평가를 몇 초 안에 도는 루프가 되고,
그 루프가 곧 게임 전용 하네스이며 그 하네스가 바로 게임 자체라는 것이 결론이다.
다만 후기에서 저자는 지금 출시하는 작은 프로젝트에는 이 중 아무것도 쓰지 않았고,
이 방법이 겨냥하는 규모는 더 큰 프로젝트라고 덧붙인다.

## 동작 방식

저자가 그리는 루프는 네 단계다.
먼저 시드와 저장 파일로 정확히 같은 상태를 언제든 다시 만든다.
다음으로 커맨드나 외부 데이터로 그 상태를 컴파일 없이 바꾼다.
그 결과를 엔진 없이 시뮬레이션 단독으로, 또는 스크린샷 차이로 검증한다.
마지막으로 성능 같은 영향을 텍스트 프로파일로 확인한다.

```text
고정 시드 + 저장 상태 로드
        ↓
커맨드 재생 / 외부 데이터 수정 (컴파일 없음)
        ↓
시뮬레이션 단독 테스트 ──→ 스크린샷 → odiff 유사도
        ↓
samply 텍스트 프로파일 → 다음 턴
```

핵심은 각 단계가 에이전트에게 “읽을 수 있는 출력”을 돌려준다는 점이다.
스크린샷 두 장은 바뀌지 않은 영역까지 모두 컨텍스트로 들어가 오히려 진행 감각을
흐리지만,
`odiff`의 “85% 유사” 같은 숫자는 턴마다 비교할 수 있는 안정된 기준선이 된다.
GUI 프로파일러의 호출 그래프는 사람용이지만
`samply`의 텍스트 덤프는 에이전트가 직접 읽는다.

결정성이 모든 단계의 바탕이다.
같은 상태로 반복해서 돌아갈 수 없으면 에이전트는 수정이
효과가 있었는지 판단하기 전에 상태 재현 실패부터 헤매게 된다.
저자가 저장·불러오기를 “기능”이
아니라 개발 첫날부터 설계할 기반으로 보라고 하는 이유도 여기에 있다.

## 구현하기

### 단일 난수원

게임 시작 시 시드를 받은 난수 생성기 하나를 만들고,
비결정적인 호출은 모두 이것만 쓰게 한다.
`Random.Float` 같은 호출이 30군데 있어도 30번째 호출 값은 매번 같아진다.

### Thing 하나로 통일한 객체 모델

나무는 메시와 충돌체를 가진 객체이고,
개는 거기에 이동이 더해진 객체일 뿐이라는
것이 저자의 “A Tree is a Dog” 관찰이다.
그래서 클래스 계층 대신 모든 객체를
한 타입으로 두고 종류는 열거형 값으로 구분한다.
원문의 `Thing` 정의는 이미지로만 실려 있어 정확한 필드를 옮길 수 없지만, 본문 설명(스탯 값, `isAlive` 플래그, 종류 열거형, `attackDamage`·`walkSpeed`·`boatSpeed` 같은 데이터)에 맞춰 C#으로 쓰면 다음과 같은 모양이 된다.

```csharp
using System.Collections.Generic;
using System.Text.Json;

public enum ThingType { Tree, Dog, Boat, GameManager }

// 모든 객체가 같은 구조체다. 종류별 동작은 Type으로 분기한다.
public struct Thing
{
    public int Id { get; set; }
    public ThingType Type { get; set; }
    public bool IsAlive { get; set; }
    public float X { get; set; }
    public float Y { get; set; }
    public int AttackDamage { get; set; }
    public float WalkSpeed { get; set; }
    public float BoatSpeed { get; set; }
    public int TurnNumber { get; set; }
}

public static class Save
{
    // 타입이 하나뿐이라 다형성 역직렬화가 필요 없다. 들어가는 길도 나오는 길도 하나다.
    public static string Write(List<Thing> world) => JsonSerializer.Serialize(world);
    public static List<Thing> Read(string json) => JsonSerializer.Deserialize<List<Thing>>(json)!;
}
```

### 커맨드로만 상태를 바꾸기

상태 변경을 느슨한 함수 호출이 아니라 직렬화 가능한 객체로 표현하고,
처리기 하나가 그것을 적용한다.
그러면 시작 상태와 커맨드 목록만으로 플레이어가 겪은 버그를 그대로
재생할 수 있고,
에이전트가 텍스트 편집기로 커맨드를 엮어 실행 중인 게임에 흘려 넣을 수도 있다.

```csharp
using System.Collections.Generic;

public record MoveCommand(int ThingId, float ToX, float ToY);

public static class Simulation
{
    // 시뮬레이션이 진실의 원천이다. 엔진은 결과 상태를 받아 그리기만 한다.
    public static List<Thing> Apply(List<Thing> world, MoveCommand cmd)
    {
        var next = new List<Thing>(world);
        int i = next.FindIndex(t => t.Id == cmd.ThingId);
        if (i < 0 || !next[i].IsAlive || next[i].WalkSpeed <= 0) return next; // 유효하지 않은 이동은 무시
        var t = next[i];
        t.X = cmd.ToX;
        t.Y = cmd.ToY;
        next[i] = t;
        return next;
    }

    public static List<Thing> Replay(List<Thing> start, IEnumerable<MoveCommand> log)
    {
        var world = start;
        foreach (var c in log) world = Apply(world, c);
        return world;
    }
}
```

이 `Simulation`을 엔진과 별도 라이브러리로 두면
엔진 없이 순수 C# 테스트 프로젝트로 돌릴 수 있다.
저자는 Monster Train의 Brian Cronin 발표와
Solium Infernum 팀 인터뷰를 같은 기법의 사례로 든다.

### 이미지 차이와 텍스트 프로파일

```bash
# 변경 전후 스크린샷의 차이 이미지를 만든다. 유사도 수치를 에이전트의 평가 기준으로 쓴다.
odiff before.png after.png diff.png

# GUI가 아닌 텍스트로 읽을 수 있는 프로파일을 남긴다.
samply record ./my-game
```

헤드리스 실행은 원문에 없는 내용이지만 HN 토론에서 같은 방향의 경험이 나왔다.
TeMPOraL은 가장 값진 프롬프트가
“게임을 헤드리스로 돌리는 방법을 찾아 달라”였다고 적었는데,
그 덕에 에이전트가 여러 인스턴스를 병렬로
띄워 스스로 가정을 확인하게 되었다고 한다.[^TeMPOraL]

## 트레이드오프

### 결정성은 공짜가 아니다

HN에서 가장 큰 논쟁은 결정성이었다.
bob1029는 여러 플랫폼에서 결정성을 유지하는 일이 가장 고약한 부분이고
게임을 매우 옹색하게 만드는 방식이라고 반박했다.[^bob1029]
rrradical은 고정소수점 수학 라이브러리를 쓰면 되며 결정성은 롤백 넷코드,
리플레이,
쉬운 디버깅을 주는 해방이라고 맞섰고,[^rrradical] 시작 상태에 입력을
흘린 뒤 결과 상태의 체크섬을 플랫폼마다 비교하는
CI는 쉽게 만들 수 있다고 덧붙였다.[^rrradical-ci]
avaer는 에이전트가 라이브러리 대신 플랫폼 기본 삼각함수를 코드 깊숙이 넣는
실수는 쉽게 일어나고 큰 게임에서는 찾기 어려우며,
셰이더와 그래픽 차이는 라이브러리로 막을 수 없다고 짚었다.[^avaer]
simonw의 경험이 이를 그대로 보여 준다.
리플레이 기능이 있는 작은 RTS를 만들었는데 Safari에서 리플레이가 깨졌고,
에이전트가 `Math.sin()`,
`Math.cos()`를 자체 결정적 함수로 바꿔 고쳤다고 한다.[^simonw]

결국 결정성은 시뮬레이션 상태에 한정해야 얻을 수 있는 성질이다.
mypalmike의 말처럼 GPU 출력이 게임 루프로 되먹임되지 않는 한 렌더링 차이는
문제가 아니고,
플레이테스터가 넘긴 입력 기록으로 버그를 100% 재현하는 이득은 크다.[^mypalmike]
그러나 meheleventyone가 지적하듯 결정성은 고정소수점 라이브러리 하나로 끝나는
일이 아니며,[^meheleventyone] 저자 말대로
프로젝트 막바지에 넣으려 하면 근본적인 변경이 필요해진다.
처음부터 넣을지 말지를 정하는 것이 이 트레이드오프의 실체다.

### Thing 하나는 규모가 커지면 비싸다

avaer는 `Thing` 접근이 작은 게임에는 합리적이지만,
수천 개의 Thing이 걸린 서브시스템 30개를 프레임 시간 안에 순회하고
복사하는 일은 불가능하며 그래서 ECS와 SoA가 있다고 비판했다.[^avaer-thing]
저자 kkukshtel은 이런 시스템이 AAA에서도 흔하고 Dreams 팀 인터뷰에서도
비슷한 구조를 설명했으며 ECS와 배타적이지 않다고 답했다.[^kkukshtel-thing]
nsagent는 Dreams가 표준 ECS를 썼고 팀 규모와 예산으로
보아 AAA로 보기 어렵다고 다시 반박했다.[^nsagent]

정리하면 단일 타입은 에이전트에게 “어디를 고쳐야 하는지” 모호함을
없애 주는 대가로, 메모리 배치와 순회 비용을 설계자가 따로 관리하게 만든다.
저자는 메모리가 생각만큼 비싸지 않다고 하지만 그 근거를 수치로 보이지는 않는다.

### 컴파일 없는 루프는 경계를 늘린다

데이터를 밖으로 빼고 시뮬레이션을 DLL로 분리하면 에이전트의 반복은 빨라지지만,
직렬화 형식, 커맨드 스키마,
엔진과 시뮬레이션 사이의 상태 차이 계산이라는 새 경계가 생긴다.
경계마다 버전 불일치와 변환 버그가 생길 수 있고,
이는 원문이 다루지 않는 비용이다.

## 비평

### 기법은 옳지만 하네스라는 이름이 과하다

글의 처방은 결정성, 데이터 주도 설계, 시뮬레이션 분리,
재현 가능한 버그 리포트처럼 게임 업계가 오래 권해 온 관행이다.
저자도 이 팁들이 AI가 없어도 좋다고 인정한다.
HN의 hatthew는 AI가 나오고서야 사람들이 디버깅 가능성, 반복 속도 같은 좋은 엔지니어링 관행에 신경 쓰게 된 것이 우습다고 했고,[^hatthew] Viliam1234는 같은 관행이 사람의 번아웃을 막는다는 이유로는 외면받다가 토큰을 아낀다는 이유로 되살아났다고 꼬집었다.[^Viliam1234]
marcus_holmes는 슬라이드가 “엔티티 디커플링 입문”을
도는 것 같았다고 적었다.[^marcus_holmes]

그렇다면 “게임이 곧 하네스”라는 주장의 새 부분은 기법이 아니라 동기의 재배치다.
사람에게는 미루던 투자가 에이전트에게는 즉시 회수된다는 것이 진짜 논지이고,
hatthew가 든 셈법,
즉 구현이 거의 공짜가 되면 설계 투자의 지렛대가 커진다는
설명이 그 논지를 더 정확히 말해 준다.[^hatthew-math]

### 후기가 본문의 적용 범위를 스스로 줄인다

저자는 후기에서 지금 출시하는 작은 프로젝트에는
이 중 아무것도 쓰지 않았다고 밝힌다.
본문은 “어떤 게임이든 자기 하네스가 될 수 있다”고 끝맺지만,
정작 저자의 실제 출하 경험은 이 방법 없이 이루어졌다.
nylonstrung은 저자의 강한 의견이 실제 플레이어층을 가진 게임을
출시한 경험의 부족을 반영하는 것 같다고까지 말했다.[^nylonstrung]
반대로 avaer는 이 조언이 주로 작은 인디 타이틀에 맞는다고
보았으니,[^avaer-thing] 큰 프로젝트용이라는 저자와 작은 프로젝트용이라는
비판자가 서로 반대 방향에서 적용 범위를 의심하는 셈이다.
어느 규모에서 효과가 있었는지 보여 주는
사례가 글에 없다는 점이 이 혼란의 원인이다.

### 아트와 감각은 여전히 하네스 밖에 있다

글은 게임의 비코드 요소를 문제로 제기하지만
해법은 대부분 시뮬레이션과 데이터 쪽에 머문다.
avaer는 현대 게임 제작 주기를 지배하는 것은 아트이고 그것은 별도의 하네스가
필요하며, `samply`로는 오버드로를 진단할 수 없다고 지적했다.[^avaer-thing]
psadauskas는 길쭉한 사탕과 둥근 사탕이 드래그될 때 똑같이 3px 커지면 어딘가
어색해 보이는데,
“드래그할 때 느낌이 이상하다”를 LLM에게
어떻게 전할지 모르겠다고 적었다.[^psadauskas]
`odiff`의 유사도는 목표 이미지가 있을 때만 쓸모 있고,
그 목표를 정하는 감각은 여전히 사람 몫이다.

이 지점에서 drusepth의 제안이 글을 보완한다.
LLM에게 미세 조정을 시키지 말고,
사람이 손으로 미세 조정을 더 빨리 할 수 있는
도구를 LLM에게 만들게 하라는 것이다.[^drusepth]
하네스가 에이전트용 관측 장치일 뿐 아니라 사람용 조율 장치이기도
해야 한다는 뜻이다.

### 에이전트가 결정성 쪽으로 기울이는 힘을 다루지 않는다

MMO와 인디 개발 경력을 가진 dudeinhawaii는 AI 모델이 모든 것을 결정적으로 만들고
싶어 하지만 게임은 시뮬레이터 장르를 빼면 검증 가능한 프로그램이 아니며,
검증기에 맞추려는 코드 변경이 오히려 버그와
경직성을 낳는다고 경험을 적었다.[^dudeinhawaii]
글은 결정성을 무조건 좋은 것으로 다루지만,
검증 가능한 축으로 게임을 끌어당기는 압력이 재미라는
검증 불가능한 축을 희생시킬 수 있다는 위험은 언급하지 않는다.

## 함정

- 시드를 하나로 묶어도 플랫폼 기본 수학 함수나 부동소수점 차이로 결정성이 깨진다. 리플레이가 브라우저마다 달라지는 사례가 실제로 있다.[^simonw]
- 스크린샷 두 장을 그대로 넘기면 바뀌지 않은 영역이 컨텍스트를 오염시킨다. 레이어를 끄고 잘라 낸 뒤 차이를 수치로 넘겨야 한다.
- 한 번에 잘 만든 게임도 이후 작은 수정마다 품질이 떨어질 수 있다. sarchertech는 원샷으로 만든 수학 게임을 조금이라도 고치면 테스트와 스펙으로 묶어도 매번 결과가 더 나빠졌다고 했다.[^sarchertech]
- 시뮬레이션을 분리해도 아트, 셰이더, GPU 타이밍은 그 밖에 남는다. 이 영역의 회귀는 별도 수단으로 잡아야 한다.

## 체크리스트

- 같은 시드와 저장 파일로 같은 프레임의 같은 상태를 다시 만들 수 있는가?
- 모든 상태 변경이 직렬화 가능한 커맨드를 거치는가?
- 정적 데이터를 바꿀 때 재컴파일이 필요 없는가?
- 시뮬레이션이 엔진 없이 테스트 프로젝트에서 돌아가는가?
- 게임을 헤드리스로 여러 인스턴스 띄울 수 있는가?
- 플랫폼마다 같은 입력에 같은 상태 체크섬이 나오는지 CI가 확인하는가?
- 스크린샷 비교가 유사도 수치로 나오는가?
- 프로파일 결과가 텍스트로 나오는가?

## 기억할 원칙

### 에이전트에게 읽히는 출력이 곧 하네스다

이 글에서 일반화할 수 있는 원칙은 게임에 한정되지 않는다.
에이전트의 성능은 모델보다 작업 대상이 돌려주는 신호의 형태에 더 크게 좌우된다.
재현 가능한 상태, 텍스트로 된 결과,
숫자로 된 차이가 있으면 에이전트는 스스로 반복할 수 있고,
그렇지 않으면 사람이 매 턴 눈으로 확인해야 한다.
TeMPOraL이 1997년 PC 게임을 Claude Code로 디컴파일하고 헤드리스로 돌리게
한 뒤 레벨 공략까지 쓰게 한 사례는,
소스가 없는 게임에서도 에이전트에게 계측을 맡기면
같은 효과가 난다는 것을 보여 준다.[^TeMPOraL-case]

### 투자 시점이 결과를 정한다

결정성, 저장·불러오기,
시뮬레이션 분리는 모두 처음에 하면 싸고 나중에 하면 비싸다.
에이전트는 이 비용 차이를 키운다.
초기에 구조를 잡아 두면 에이전트의 반복은 몇 초짜리 루프가 되고,
그렇지 않으면 에이전트는 dudeinhawaii의 말처럼 스스로를 구석에
몰아넣었다가 많은 코드 변경을 치르며 빠져나오기를 반복한다.[^dudeinhawaii]
작은 프로젝트라면 저자처럼 아무것도 안 해도 되지만,
규모가 커질 프로젝트라면 첫 줄을 쓰기 전에 정해야 한다.

---

[^TeMPOraL]: <https://news.ycombinator.com/item?id=50080720>

[^bob1029]: <https://news.ycombinator.com/item?id=50074374>

[^rrradical]: <https://news.ycombinator.com/item?id=50075430>

[^rrradical-ci]: <https://news.ycombinator.com/item?id=50078764>

[^avaer]: <https://news.ycombinator.com/item?id=50075919>

[^simonw]: <https://news.ycombinator.com/item?id=50074610>

[^mypalmike]: <https://news.ycombinator.com/item?id=50076161>

[^meheleventyone]: <https://news.ycombinator.com/item?id=50084083>

[^avaer-thing]: <https://news.ycombinator.com/item?id=50075724>

[^kkukshtel-thing]: <https://news.ycombinator.com/item?id=50076887>

[^nsagent]: <https://news.ycombinator.com/item?id=50077738>

[^hatthew]: <https://news.ycombinator.com/item?id=50080514>

[^Viliam1234]: <https://news.ycombinator.com/item?id=50094756>

[^marcus_holmes]: <https://news.ycombinator.com/item?id=50083254>

[^hatthew-math]: <https://news.ycombinator.com/item?id=50095798>

[^nylonstrung]: <https://news.ycombinator.com/item?id=50079470>

[^psadauskas]: <https://news.ycombinator.com/item?id=50079834>

[^drusepth]: <https://news.ycombinator.com/item?id=50078259>

[^dudeinhawaii]: <https://news.ycombinator.com/item?id=50078115>

[^sarchertech]: <https://news.ycombinator.com/item?id=50080799>

[^TeMPOraL-case]: <https://news.ycombinator.com/item?id=50080674>
