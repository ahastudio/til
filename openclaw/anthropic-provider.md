# OpenClaw - Anthropic 프로바이더 (CLI 사용 재허용)

원문: <https://docs.openclaw.ai/providers/anthropic>

## 소개

Anthropic이 OpenClaw에서의 Claude CLI 방식 사용을 다시 허용했다. OpenClaw는
이를 공식 문서에 반영하여 두 가지 인증 방식을 모두 지원한다.

- **Anthropic API 키**: Anthropic 콘솔에서 발급, 사용량 기반 과금
- **Claude CLI 재사용**: 기존 Claude CLI 로그인을 `claude -p` 방식으로 직접 재사용

## 설정

### 온보딩

```sh
openclaw onboard --anthropic-api-key <KEY>
```

비대화형(non-interactive) 설정 시 `--anthropic-api-key` 플래그를 사용한다.
기존 토큰 프로파일(token profile)은 실행 중에도 계속 유효하다.

### 모델 기본값

Claude 4.6 모델은 명시적 thinking 수준을 지정하지 않으면 `adaptive` 모드가
자동 적용된다. 메시지별로 `/think:<level>`로 재정의하거나 설정 파일에서
`agents.defaults.models[“anthropic/<model>”].params.thinking`으로 조정한다.

### Fast Mode

`/fast` 토글은 Anthropic의 서비스 티어(service tier)와 연동된다.

- `/fast on` → `service_tier: “auto”`
- `/fast off` → `service_tier: “standard_only”`

단, 이 설정은 `api.anthropic.com` 직접 요청에만 적용된다. 프록시를 경유하는
트래픽에는 반영되지 않는다.

### 프롬프트 캐싱

API 키 인증에서만 사용 가능하다. `cacheRetention` 파라미터로 제어한다.

- `“none”`: 캐싱 비활성화
- `“short”`: 5분 캐시 (API 키 인증 기본값)
- `“long”`: 1시간 캐시

### 1M 컨텍스트 창 (베타)

`params.context1m: true`로 활성화한다. 내부적으로
`anthropic-beta: context-1m-2025-08-07` 헤더가 추가된다. Anthropic의 사전 승인이
필요하다.

### 설정 예시

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": {
          params: {
            fastMode: true,
            cacheRetention: "long",
            context1m: true
          }
        }
      }
    }
  }
}
```

## 분석

### CLI 재허용의 배경

Anthropic이 Claude CLI를 통한 OpenClaw 연동을 한동안 허용하지 않았다가 다시
허용했다. 정책 변경의 명시적 이유는 공개되지 않았으나, OpenClaw 측 개발자는
“반복적인 정책 변경이 신뢰를 훼손했다”고 밝혔다
([GeekNews 댓글](https://news.hada.io/topic?id=28761)).

### 두 인증 방식의 기능 차이

API 키와 CLI 인증 방식은 기능 범위가 다르다.

| 기능              | API 키 | CLI 재사용 |
| ----------------- | ------ | ---------- |
| 프롬프트 캐싱     | ✓      | ✗          |
| Fast Mode         | ✓      | ✓          |
| 1M 컨텍스트 창    | ✓      | 미확인     |
| 토큰 만료 위험    | 낮음   | 높음       |

프로덕션 환경에서는 API 키 인증이 권장된다.

### Agent별 독립 인증

인증은 에이전트(agent) 단위로 관리된다. 새 에이전트를 추가할 때마다 별도의
자격증명이 필요하다. 레이트 리밋(rate limit) 쿨다운도 모델 범위에서 적용되므로,
한 모델이 제한되어도 다른 모델은 계속 사용 가능하다.

## 비평

### 정책 불안정성이 생태계 신뢰를 무너뜨린다

GeekNews 커뮤니티의 반응은 냉소적이었다. CLI 재허용 자체보다 “언제 또 막힐지
모른다”는 불확실성에 대한 우려가 컸다
([GeekNews 댓글](https://news.hada.io/topic?id=28761)).
Anthropic의 트위터 소통과 공식 정책 사이의 불일치, 반복적인 방향 전환은 써드파티
개발자들이 Anthropic 생태계에 의존하는 데 구조적 리스크가 된다.

### 문서화의 한계

CLI 재사용 방식의 1M 컨텍스트 창 지원 여부가 명시되지 않은 점이 아쉽다. “API 키만
지원”이라고 명시된 기능과 “미확인” 상태인 기능의 구분이 문서 내에서 명확하지 않다.

### Fast Mode의 프록시 제한

프록시를 경유하는 트래픽에서 Fast Mode가 무효화된다는 점은 기업 환경에서 문제가
된다. 많은 조직이 API 호출을 프록시를 통해 라우팅하므로 이 기능의 실효성이
제한될 수 있다.

## 인사이트

### 플랫폼 정책 리스크가 에이전트 인프라의 새 변수가 된다

에이전트 시스템을 프로덕션에 배포할 때 기술적 안정성만큼 중요한 것이 플랫폼 정책
안정성이다. OpenClaw가 경험한 것처럼, LLM 제공자가 정책을 바꾸면 제3자 제품 전체가
중단될 수 있다. API 키 방식이 CLI 방식보다 “프로덕션 권장”인 이유는 성능 차이가
아니라 정책 의존성의 차이다. 에이전트 인프라를 설계할 때 특정 인증 방식의 정책적
지속 가능성을 평가하는 것이 필수 요소가 됐다.

### 인증 방식 이중화는 에이전트 생태계의 현실적 타협이다

OpenClaw가 API 키와 CLI 인증 두 가지를 병행 지원하는 것은 기술적 선택이 아니라
생존 전략이다. 하나의 인증 경로만 지원하면 제공자의 정책 변경 한 번으로 서비스
전체가 중단된다. 복수 인증 방식은 resilience(복원력) 설계의 일부다. LLM 생태계가
성숙할수록 이런 방어적 설계가 제3자 툴의 기본 요구사항이 될 것이다.

### 모델별 레이트 리밋 관리는 새로운 운영 기술이 된다

“레이트 리밋 쿨다운이 모델 범위로 적용되므로 sibling 모델은 계속 사용 가능하다”는
설명은, 에이전트 운영자가 여러 모델을 전략적으로 분산 사용해야 한다는 것을 의미한다.
이는 기존 소프트웨어의 데이터베이스 커넥션 풀(connection pool) 관리와 유사한 운영
지식이다. 에이전트 시스템 운영에는 모델 레이트 리밋을 고려한 로드 밸런싱이 새로운
전문 역량으로 자리잡고 있다.
