# Guard Clause와 Extract Method로 리팩터링한 세션 기록

[_agent/skills/quotes-curly/scripts/convert_quotes.py](../_agent/skills/quotes-curly/scripts/convert_quotes.py)를
if-else 대신 guard clause를 쓰고, 좋은 이름의 extract
method를 반복 적용해 리팩터링한 실습 기록이다.
사용자가 원칙을 하나씩 더 깐깐하게 요구할 때마다 Claude Code가
같은 코드를 다시 들여다보며 무엇을 놓쳤는지 알아낸 과정이 핵심이라,
결과 코드보다 그 과정에서 걸린 판단들이 더 남는 배움이었다.

## if-else를 걷어내면 상태가 드러난다

원래 스크립트는 문자 하나하나를 순회하며 `if ch == '"' and not
in_fenced_code_block: ...` 형태로 조건을 검사했다.
guard clause로 바꾸는 과정에서 자연히 함수를 쪼개게 됐고,
그 결과 코드에 숨어 있던 상태가 눈에 보이는 값으로 드러났다.

- 펜스 블록 안인지 여부(`in_fenced_code_block`)
- 다음에 나올 따옴표가 여는 따옴표인지(`open_quote`)

이 두 상태는 원래도 존재했지만 반복문 안의 지역 변수로 숨어 있었다.
`toggle_fence_state`, `next_open_quote`처럼 상태 전이 하나만 하는
함수로 뽑아내자, 상태가 코드의 일급 개념이 됐다.

## list comprehension은 상태가 없을 때만 자연스럽다

`result.append(...)` 루프를 list comprehension으로 바꾸라는 요청을
받았을 때, Claude Code는 처음에 그대로 반복문 안에서 `open_quote`를
갱신하며 append하는 형태로 접근했다.
이 상태는 문자마다 이전 결과에 의존하므로 comprehension 하나로는
표현할 수 없었다.

해결한 방법은 상태 갱신과 값 변환을 분리하는 것이었다.

1. `itertools.accumulate`로 상태의 시퀀스를 먼저 만든다
   (`quote_states`, `line_states`).
2. 그 상태 시퀀스와 원본 시퀀스를 `zip`으로 묶어
   순수한 변환 함수(`convert_char`, `convert_line`)에 넘긴다.
3. 이 값 변환 부분만 list comprehension으로 표현한다.

“상태를 누적하는 부분”과 “값을 변환하는 부분”을 분리하면,
값 변환 부분은 언제나 comprehension으로 표현할 수 있다.
반대로 이 둘을 분리하지 않은 채 comprehension을 억지로 쓰려고 하면
안에 부작용이 섞인, 읽기 어려운 코드가 된다.

## 상태 계산과 값 변환을 나누다 생긴 중복

상태 시퀀스(`line_states`)와 최종 문자열(`convert_content`)을
각각 만드는 함수로 나누면서, Claude Code는 같은 줄에 대해
`convert_line`이 두 번 호출되는 실수를 저질렀다.
한 번은 `next_line_state`가 “이 줄을 지난 뒤의 따옴표 상태”를
알아내기 위해, 한 번은 `convert_content`가 실제 변환 결과를 만들기
위해서였다.

책임을 나누는 리팩터링은 같은 계산을 두 곳에서 반복하게 만들
위험이 있다.
해결은 `convert_line`을 “문자열만 반환”하도록 유지하고,
`next_line_state`는 `convert_line`을 호출하지 않은 채
`quote_states`(더 하위의 순수 상태 계산 함수)만 다시 사용하도록
정리하는 것이었다.
즉 상태 계산 로직 자체를 한 단계 더 낮은 함수로 뽑아,
그 함수를 상태 전이 쪽과 값 변환 쪽이 각각 필요한 만큼만
가져다 쓰게 했다.

## 긴 docstring 테스트는 SRP 위반의 신호다

Claude Code는 `convert_content`의 docstring에 빈 문자열, 일반 텍스트,
홀수 따옴표, 펜스 블록, 다중 따옴표 등 7개의 예제를 몰아넣었다.
동작은 맞았지만, 사용자로부터 “이 함수 하나가 이렇게 많은 경우의
수를 책임져야 하는가?”라는 질문을 받고 나서야 문제가 보였다.

각 예제를 실제로 검증하고 싶은 대상별로 분류해보니,
`convert_content`가 검증해야 할 것은 딱 하나,
“줄로 쪼개고 상태를 전파하며 다시 합치는 조립이 맞는가”였다.
빈 문자열이나 일반 텍스트, 홀수/다중 따옴표 같은 문자 단위 변환의
세부 사례는 그 일을 실제로 하는 `convert_line`과 `quote_states`의
책임이었다. 예제를 원래 책임을 가진 함수로 옮기자
`convert_content`의 테스트는 2개로 줄었고, 각 함수의 테스트도
그 함수가 실제로 하는 일만 검증하게 됐다.

**함수 하나의 테스트 목록이 길어지는 것은 테스트를 더 촘촘히
써야 한다는 신호가 아니라, 그 함수가 여러 책임을 떠안고 있다는
신호로 먼저 의심해야 한다.**

## 헬퍼 함수는 호출부의 모양을 지켜야 한다

파일 읽기에 예외 처리를 추가하면서, Claude Code는 처음에
`convert_file` 안에 `try: content = read_file(filepath) except
FileNotFoundError: ...`처럼 호출부에서 직접 예외를 잡는 형태로
작성했다.
사용자는 이 형태가 “이상하다”고 지적했다.
헬퍼를 만드는 이유는 호출부를 단순하게 유지하기 위해서인데,
호출부가 여전히 내부 구현(어떤 예외가 날 수 있는지)을 알아야
한다면 추상화가 새고 있는 것이다.

예외 처리를 `read_file`/`write_file` 내부로 옮기고 나니
호출부는 다시 `content = read_file(filepath)` 한 줄로 돌아왔다.
**헬퍼 함수를 뽑았는데 호출부가 여전히 그 헬퍼의 실패 방식을
알아야 한다면, 책임이 잘못된 곳에 남아 있다는 뜻이다.**

## 인사이트

이번 세션에서 반복된 패턴은 하나였다.
사용자가 “겉보기엔 끝난 것 같은 리팩터링”에 한 가지 원칙(guard
clause, comprehension, docstring 테스트, 헬퍼 추출)을 더 깐깐하게
들이댈 때마다, Claude Code는 매번 그 밑에 숨어 있던 책임의 경계를
다시 찾아내야 했다.
좋은 이름의 extract method가 핵심이라는 말은, 이름을 잘 짓는
기술이 아니라 “이 코드 조각이 실제로 무엇을 책임지는가”를
정확히 알아내는 일이라는 뜻에 더 가까웠다.
리팩터링 도구(guard clause, comprehension 등)는 목적이 아니라,
숨은 책임을 찾아내기 위해 코드를 흔들어보는 수단이었다.
