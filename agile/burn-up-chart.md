# Burn-up chart: 범위와 완료를 두 선으로 나눠 그리는 법과 이 안내문이 틀린 곳

원문: [Burn Up Chart: The Complete 2026 Guide](https://instituteprojectmanagement.com/blog/burn-up-chart-the-complete-2026-guide/)

## 소개

교육 업체 Institute of Project Management(IPM)의
블로그가 2026년 9월 29일에 올린 안내문이다.
burn-up chart가 무엇인지, burndown chart와 어떻게 다른지, 언제 쓰는지를 설명하고
마지막에 작업 예 하나와 자주 묻는 질문 다섯 개를 붙였다.
글의 요지는 두 가지다.
burn-up chart는 완료한 양과 전체 scope를 서로 다른 선으로 그려서
팀이 느린 것인지 목표가 늘어난 것인지를 가려 주고,
그래서 scope가 바뀌는 릴리스와 프로그램 보고에는 burndown보다 낫다는 것이다.

이 문서는 그 요지를 실제로 쓸 수 있는 형태로 옮기는 데 무게를 둔다.
차트가 어떻게 동작하는지, 직접 만드는 코드, 값을 정하는 기준, 함정을 먼저 적고,
안내문의 주장을 Atlassian과 Microsoft의 문서로 대조한 결과를 비평으로 붙였다.
대조에서 안내문의 작업 예는 계산이 맞지 않았고,
burndown이 scope 변경을 전혀 보여 주지 못한다는 서술은 과장이었다.

## 동작 방식

### 두 선과 그 사이의 거리

burn-up chart는 시간에 따라 두 값을 그린다.
하나는 지금까지 약속된 전체 일의 양(scope)이고,
다른 하나는 완료로 옮긴 누적 양이다.
두 선 사이의 거리가 남은 일이고, 일이 끝나면 두 선이 만난다.
Jira의 burnup 보고서도 같은 구조다.
빨간 선이 계획한 work scope이고 초록 선이 Done으로 옮긴 completed work이며,
회색 guideline 선은 제때 끝내려면
팀이 어느 속도로 가야 하는지를 근사해서 보여 준다.[^atl-report]
세로축은 스토리 포인트나 작업 건수나 추정치이고
가로축은 일 단위 시간이다.[^atl-report]

### 읽는 법

- 완료 선이 scope 선을 향해 올라가 만나면 계획대로 끝난다는 뜻이다.
- scope 선이 중간에 올라가면 일이 더해졌다는 신호이고,
Jira 문서는 이 선이 계속 오르면 scope creep의 징후라고 설명한다.[^atl-report]
- 완료 선의 기울기가 속도이고,
이 기울기를 scope 선까지 연장하면 완료 시점의 추정이 나온다.

세 번째 읽기는 안내문에 없고 이 문서가 덧붙인 것이다.
Atlassian의 burn up chart 소개는 이 차트가 대략적인
완료 날짜를 정하는 예측에 쓰인다고 적는다.[^atl-page]

### 만들 때 기록해야 하는 것

차트는 매일 두 숫자만 있으면 그려진다.
그날까지의 누적 scope와 누적 완료다.
scope가 바뀌는 날에는 바뀐 양과 이유를 같이 기록해야 한다.
이 기록이 없으면
scope 선이 올라간 것이 새 요구인지 재추정인지 나중에 설명할 수 없다.

## 만드는 법

### 직접 계산하는 코드

아래는 일별 완료량과 scope 변경을 받아 누적 값을 만들고,
최근 며칠의 속도로 완료까지 걸릴 일수를 추정하고,
터미널에 간단한 그림을 그리는 코드다.
표준 라이브러리만 쓰고, 이 문서를 쓰면서 실제로 실행해 출력을 확인했다.

```python
"""Burn-up 차트 계산과 예측: 표준 라이브러리만 쓴다."""
from dataclasses import dataclass


@dataclass
class Day:
    label: str
    done: float = 0.0   # 그날 완료한 양(포인트)
    added: float = 0.0  # 그날 scope에 더해진 양(음수면 뺀 양)


def burnup(days, initial_scope):
    """날짜별 (누적 scope, 누적 완료)를 돌려준다."""
    scope, done, rows = initial_scope, 0.0, []
    for d in days:
        scope += d.added
        done += d.done
        rows.append((d.label, scope, done))
    return rows


def forecast_days(rows, window=5):
    """최근 window일의 평균 속도로 완료까지 남은 일수를 추정한다.

    속도가 0 이하이면 None. scope가 계속 움직이면 추정도 같이 움직인다.
    """
    if len(rows) < 2:
        return None
    recent = rows[-(window + 1):]
    velocity = (recent[-1][2] - recent[0][2]) / (len(recent) - 1)
    remaining = rows[-1][1] - rows[-1][2]
    if velocity <= 0:
        return None
    return remaining / velocity


def ascii_chart(rows, height=12):
    top = max(r[1] for r in rows)
    lines = []
    for level in range(height, -1, -1):
        y = top * level / height
        cells = []
        for _, scope, done in rows:
            mark = " "
            if abs(scope - y) <= top / height / 2:
                mark = "S"
            if abs(done - y) <= top / height / 2:
                mark = "D" if mark == " " else "*"
            cells.append(mark)
        lines.append(f"{y:6.1f} |" + " ".join(cells))
    lines.append("       +" + "-" * (2 * len(rows)))
    return "\n".join(lines)


if __name__ == "__main__":
    # 범위 100, 20일 릴리스, 하루 4포인트씩 완료, 10일째에 scope +20
    days = [Day(str(i + 1), done=4.0) for i in range(20)]
    days[9].added = 20.0
    rows = burnup(days, initial_scope=100.0)
    for label, scope, done in rows[8:12]:
        print(f"{label:>3}일  scope {scope:5.1f}  완료 {done:5.1f}  남음 {scope - done:5.1f}")
    print(ascii_chart(rows))
    print("20일째: 완료", rows[-1][2], "scope", rows[-1][1],
          "→ 미완료", rows[-1][1] - rows[-1][2])
    print("10일째 시점 예측 남은 일수:", round(forecast_days(rows[:10]), 1))
```

실행 결과의 핵심은 이렇다.

```text
  9일  scope 100.0  완료  36.0  남음  64.0
 10일  scope 120.0  완료  40.0  남음  80.0
 11일  scope 120.0  완료  44.0  남음  76.0
 12일  scope 120.0  완료  48.0  남음  72.0
 (이어서 터미널 그림이 출력된다)
20일째: 완료 80.0 scope 120.0 → 미완료 40.0
10일째 시점 예측 남은 일수: 20.0
```

10일째에 scope가 100에서 120으로 오르면서 남은 일이 64에서 80으로 뛴다.
하루 4포인트라는 속도는 전혀 변하지 않았다.
완료 선은 같은 기울기로 올라가고, 20일째에 80에 닿아 scope 120에 40이 모자란다.

### 스프레드시트로 만들기

도구가 없으면 다섯 개의 열이면 충분하다.
날짜, 그날 완료, 그날 scope 변경, 누적 scope, 누적 완료다.
누적 scope는 첫 값에 초기 scope를 두고
그다음 행부터 위 행의 값에 그날 변경을 더하고,
누적 완료도 같은 방식으로 더한다.
누적 scope와 누적 완료 두 열을 날짜에 대해 꺾은선으로 그리면 된다.
scope 변경 열에는 사유를 적는 열을 하나 더 두는 편이 좋다.

### 도구에서 쓸 때

- Jira의 burnup 보고서는 Scrum 보드에서만 쓸 수 있고,
하위 작업의 스토리 포인트는 포함하지 않으며
상위 작업의 포인트만 센다.[^atl-report]
- Azure DevOps에는 Burndown/Burnup widget이 있다. 한 팀이나 여러 팀을 대상으로
하고 기간을 설정할 수 있으며, 작업 항목 수나 Story Points,
Effort, Remaining Work 같은 필드의 합으로 집계한다.[^azure]
- 안내문이 함께 든 Monday.com은 지원 문서를 열지 못해 확인하지 못했다.

## 번업과 번다운의 차이

두 차트는 같은 데이터를 반대 방향으로 그린다.
burndown은 남은 일을 0으로 내리고, burn-up은 완료를 scope 선으로 올린다.
Azure DevOps 문서도 burndown이 보통 내려가는 추세이고
sprint 중에 일을 더하면 올라가는 추세가 되며,
burnup은 일이 완료되는 속도를 보여 주므로
언제나 올라가는 추세를 보인다고 설명한다.[^azure]

| 항목          | burndown                      | burn-up                            |
| ------------- | ----------------------------- | ---------------------------------- |
| 그리는 것     | 남은 일                       | 누적 완료와 scope                  |
| scope가 늘면  | 남은 일 선이 위로 뛴다        | scope 선이 위로 오른다             |
| 알 수 있는 것 | 남은 양과 이상 추세           | 속도와 scope 변화를 따로           |
| 헷갈리는 점   | 진행과 scope가 한 선에 섞인다 | 선이 두 개라 읽는 법을 알아야 한다 |

위 코드의 값으로 보면 10일째 burndown은 64에서 80으로 올라간다.
이 16은 scope가 20 늘고 그날 4가 완료된 순 효과다.
선만 보아서는 scope가 얼마나 늘었는지도, 속도가 어땠는지도 알 수 없고,
이 점이 burndown의 실제 약점이다.
scope 변경이 보이지 않는 것이 아니라 진행과 섞여서 분리되지 않는 것이다.

## 값 정하기

| 항목            | 시작값                                | 이유                                                                        |
| --------------- | ------------------------------------- | --------------------------------------------------------------------------- |
| 단위            | 팀이 이미 쓰는 것(포인트, 건수, 시간) | 도구가 지원하는 단위에 맞추면 자동으로 그려진다.[^atl-report][^azure]       |
| 갱신 주기       | sprint는 매일, 릴리스는 매주          | 안내문의 권고이며 근거 자료는 없다                                          |
| 예측 창         | 최근 3~5회분                          | 이 문서의 시작값이며 너무 짧으면 흔들리고 너무 길면 현재 속도를 못 따라간다 |
| scope 변경 기록 | 날짜, 양, 사유                        | 선이 움직인 이유를 설명하기 위한 최소 정보                                  |

측정해서 바꿀 것은 예측 창이다.
지난 릴리스의 같은 시점 예측과 실제 완료일을
비교해 어느 창이 덜 틀렸는지 보면 된다.

## 트레이드오프

### 한 선에 담지 않는 대가는 해석의 부담이다

burn-up은 진행과 scope를 나누어 설명할 수 있게 한다.
대신 선이 두 개이고 각도와 간격을 함께 읽어야 한다.
안내문은 이를 이해관계자에게 설명하기 쉽다고 하지만,
처음 보는 사람은 두 선이 만나는 지점을 확정된 일정으로 오해할 수 있다.
회의 자료에는 선이 무엇인지,
만나는 지점이 언제 예측되는지를 한 줄로 달아 두는 편이 좋다.
이는 이 문서의 권고다.

### scope 변경을 기록하는 일은 차트의 가치이자 비용이다

차트의 장점은 모두 변경 기록에서 나온다.
기록이 정확하면 대화가 어느 항목을 뺄 것인가로 옮겨 가지만,
기록이 빠지면 scope 선은 거짓말을 한다.
팀은 변경마다 날짜와 사유를 적는 부담을 지고,
그 대가로 목표가 움직인 책임을 누구에게 물을지 분명한 기록을 얻는다.

## 함정

- 재추정과 scope 추가를 구분하지 않으면 같은 일이 scope 선을 올리기도 하고
내리기도 한다. 어느 쪽으로 기록할지 팀이 먼저 정해야 한다. Azure DevOps 문서는
상승의 원인으로 나쁜 추정, 계획에 없던 새 일의 발견,
합의되지 않은 일의 유입을 구분해서 든다.[^azure]
- 완료의 기준이 흔들리면
완료 선이 거짓으로 오른다. Jira는 Done으로 옮긴 일만 완료로 센다.[^atl-report]
- 하위 작업에 포인트를 붙이면 Jira burnup에는 잡히지 않는다.[^atl-report]
- 완료 선이 매끈하게 오른다고 기대하면
안 된다. 안내문의 steadily 같은 표현과 달리 실제로는 계단형이 되기 쉽고,
마지막에 몰리는 팀도 많다. 이는 이 문서의 관찰이며 근거 자료는 없다.
- 속도가 변하는데 평균으로 연장하면
예측이 어긋난다. 위 코드는 최근 구간만 쓰도록 `window`를 두었다.

## 확인하기

위 코드를 파일로 저장해 `python3 burnup.py`로 실행하면 앞의 출력이 나온다.
직접 확인할 것은 세 가지다.

1. `days[9].added`를 0으로 바꾸면
20일째에 완료 80이 scope 100에 20 모자라는 것이 보인다.
안내문의 작업 예가 맞으려면 속도가 올라가야 한다는 뜻이다.
2. `added`에 음수를 넣으면 scope 선이 내려가고 두 선이 일찍 만난다.
3. `forecast_days`의 `window`를 1로 줄이고
완료량을 불규칙하게 바꾸면 예측이 얼마나 흔들리는지 볼 수 있다.

## 체크리스트

- scope의 단위와 추정 기준이 팀 안에서 같은가
- 갱신 시점이 정해져 있고 지켜지는가
- scope 변경마다 날짜, 양, 사유를 기록하는가
- 재추정과 새 일의 추가를 어느 쪽으로 기록할지 합의했는가
- 완료의 기준이 문서로 정해져 있는가
- 예측에 쓰는 속도 구간이 정해져 있고 지난 예측과 비교했는가
- 회의 자료에 선의 뜻과 예측 방법이 적혀 있는가

## 비평

### 작업 예의 계산이 맞지 않는다

안내문은 scope 100포인트로 릴리스를 시작해 중간쯤에 40포인트를 완료했고
완료 선이 마감까지 100에 닿도록 순조로운 상태라고 쓴다.
중간이 기간의 절반이라면 이 속도로는 마감에 80에 닿는다.
100에 닿으려면 남은 절반에 60을 해야 하는데, 앞의 절반에 한 40의 1.5배다.
이어서 scope가 120이 되면 남은 절반에 80, 곧 지금 속도의 두 배가 필요하다.
위 코드의 출력이 이를 확인한다.
글이 보여 주려는 요점, 곧 scope가 움직였고 속도는 변하지 않았다는 점은 맞다.
그러나 변하지 않은 속도가 애초에 마감에 모자랐다는 사실을 가린다.
예시는 두 선이 만나는 곳을 읽는 연습이어야 하는데,
읽어 보면 처음부터 만나지 않는 차트다.

### burndown이 scope 변경을 숨긴다는 서술은 과장이다

안내문은 burndown이 scope 변경을 완전히 가릴 수 있고,
scope가 늘면 팀이 갑자기 뒤처진 것처럼만 보인다고 말한다.
Microsoft의 Azure DevOps 문서는 sprint나 릴리스 중에 일을 더하면
burndown이 올라가는 추세를 보인다고 적고,
그 상승의 원인으로 scope creep을 든다.[^azure]
Atlassian의 burndown 튜토리얼도 위로 뛰는
선은 흔히 scope가 더해졌다는 뜻이라고 하면서
burndown이 개별 scope 변경을 명시하지 않으므로
scope가 자주 바뀌면 burnup을 고려하라고 한다.[^atl-burndown]
정확한 약점은 보이지 않는다가 아니라 섞여 보인다다.
올라간 만큼이 새 일인지 속도 저하인지 가르지 못하는 것이다.
같은 Atlassian의 burn up chart 소개 페이지는 burndown에서 변경을 추적할 수 없고
프로젝트가 정상으로 진행된다고 잘못 생각할 수 있다고 쓰는데,
이는 같은 회사의 burndown 튜토리얼과 어긋난다.[^atl-page]
안내문의 서술은 이 마케팅 문구와 닮았다.

### 74%라는 숫자는 두 단계를 거쳐 왔고 주장과 이어지지 않는다

안내문은 애자일 팀의 74%가 이제 혼합, 하이브리드, 자체 방식으로 일하므로
scope 안정성을 더는 가정할 수 없다고 쓴다.
출처로 단 것은 Breeze의 통계 모음 글이다.
그 글에는 같은 숫자가 있고, 하이브리드 48%와 자체 방식 26%를 합한 값이며
Digital.ai의 18번째 State of Agile 보고서(2025)에서 왔다고 적혀 있다.[^breeze]
이 문서는 원 보고서를 열지 못했다.
Digital.ai 사이트에서 열린 것은 17번째 보고서 소개 페이지이고,
이 보고서는 응답자 788명의 2023년 조사에서
하이브리드 모델을 쓴다는 답이 42%라고 적는다.[^digitalai]
집계 단위(팀인지 응답자인지 조직인지)와 시점이 글마다 다르다.

더 큰 문제는 논리의 연결이다.
방법이 섞였다는 사실에서 scope가 자주 바뀐다는 결론이 나오지 않는다.
이 숫자는 burn-up chart가 필요한 이유의 증거가
아니라 글을 시사성 있게 보이게 하는 장식에 가깝다.
섹션 제목에 UK가 들어갔지만 74%는 영국에 한정된 숫자가 아니며,
영국 팀에 대한 자료는 글에 없다.

### 완전한 안내라고 하기에는 함정이 빠졌다

제목은 완전한 2026 안내를 내세우지만 본문은 광고
문구를 포함해 영어로 약 1,700단어다.
하위 작업과 재추정의 처리, 속도 변동에 따른 예측 오차,
scope 변경의 기록 방식은 다루지 않는다.
독자가 연습할 수 있는 코드나 데이터도 없다.
반면 중간에 교육과정 안내와 브로셔 신청이 두 번 들어가고,
이해관계자 소통, 프로그램 보고, 도구 소개의 문단이 같은 주장을 되풀이한다.
검색에 걸리는 글의 형태이고, 글쓴이가 교육 업체라는 사실도 감안해 읽어야 한다.

작은 서술의 확인 결과도 정리해 둔다.

- Jira와 Azure DevOps가 burn-up을 지원한다는 말은 맞다.
다만 Jira는 Scrum 보드에 한정된다는 조건이 붙는다.[^atl-report][^azure]
- Monday.com의 지원은 확인하지 못했다.
- Kanban 팀에는 누적 흐름도가 burn-up의 가까운 친척이라는
FAQ의 서술은 내가 읽은 문서에서 근거를 찾지 못했다.
- 갱신을 매일 또는 매주 하라는 권고에는 근거 자료가 없다.

## 기억할 원칙

### 두 선은 변경 기록이 있을 때만 이야기가 된다

burn-up chart의 설득력은 그림의 모양이 아니라 scope가 바뀐 날짜와 양과 사유에서
나온다.
안내문이 가장 잘 짚은 부분은 scope 선이 올라가면 대화가 팀이 왜 느린가에서
새로 들어온 것 가운데 무엇을 미룰 것인가로 바뀐다는 점이다.
이 대화는 기록이 있을 때만 가능하다.
도구가 자동으로 그려 주더라도 변경의 사유는 사람이 남겨야 한다.

### 차트를 읽을 때는 모양보다 산수를 먼저 한다

안내문의 작업 예가 보여 주듯, 선이 순조롭게 올라가는 그림은 쉽게 믿어진다.
그러나 지금까지의 속도로 남은 기간을 곱하면
마감에 얼마가 되는지는 세 줄의 산수로 확인된다.
차트를 보고
결론을 내리기 전에 이 계산을 먼저 해 보는 습관이 차트를 읽는 가장 싼 안전장치다.

---

[^atl-report]: Atlassian, [View and understand the Burnup chart or report | Jira Cloud | Atlassian Support](https://support.atlassian.com/jira-software-cloud/docs/view-and-understand-the-burnup-chart/)

[^atl-page]: Atlassian, [Burn up chart | Atlassian](https://www.atlassian.com/agile/project-management/burn-up-chart), 2026-02-11

[^atl-burndown]: Atlassian, [Agile Burndown Chart Tutorial: How to Create & Use | Agile](https://www.atlassian.com/agile/tutorials/burndown-charts), 2026-02-24

[^azure]: Microsoft Learn, [Burndown and burnup guidance - Azure DevOps | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/report/dashboards/burndown-guidance)

[^breeze]: Breeze, [Agile and Scrum statistics you need to know (2026) • Breeze](https://www.breeze.pm/articles/agile-statistics), 2026-07-13

[^digitalai]: Digital.ai, [17th State of Agile Report | Analyst Reports | Digital.ai](https://digital.ai/resource-center/analyst-reports/state-of-agile-report/)
