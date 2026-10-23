# AWS WAF로 PHP2Shell 노출을 줄이는 법: 규칙은 패치까지의 완충일 뿐이다

원문: [Using AWS WAF to apply mitigations for PHP2Shell RCE vulnerabilities (CVE-2026-109618 and CVE-2026-109619) | AWS Security Blog](https://aws.amazon.com/blogs/security/using-aws-waf-to-apply-mitigations-for-php2shell-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619/)

## 읽기 전에

### 이 글이 다루는 것

PHP2Shell은 `CVE-2026-109618`과 `CVE-2026-109619`를 묶어 부르는 이름이다.
AWS의 이 글은 취약점 설명이 아니라, PHP를 업데이트하는 동안 AWS WAF로 노출을 줄이는 방법을 정리한 안내다.
취약점 자체는 `php/php-cve-2026-109618-109619.md`와 `php/php-8-2-35.md`에 정리했다.
글은 PHP 업데이트가 유일한 완전한 해결책이고 WAF는 보조 통제라고 거듭 밝히므로, 이 문서도 같은 위치에서 읽으면 된다.

### AWS WAF를 쓴다면 확인할 것

해당하는 항목만 보면 된다.

- PHP 업데이트: 해당 브랜치의 수정 버전은 8.5.12, 8.4.27, 8.3.36, 8.2.35다. 8.1 이하는 업스트림 지원이 끝났으므로 배포판이나 장기 지원 업체의 백포트를 확인하거나 지원되는 브랜치로 옮긴다.
- 관리형 규칙 그룹: PHP 워크로드 앞의 web ACL이 PHP application 관리형 규칙 그룹(`AWSManagedRulesPHPRuleSet`)을 쓰는지 본다. 기본 버전을 쓰면 `PHP2Shell_BODY` 규칙이 이미 평가 중이고, 버전을 고정했다면 `Version_2.3`으로 바꿔야 한다.
- 본문 크기: `CVE-2026-109618`에는 Core rule set(`AWSManagedRulesCommonRuleSet`)의 `SizeRestrictions_BODY` 규칙이 8KB를 넘는 본문을 막는다. 업로드 경로 때문에 Count로 바꿨다면 레이블 기반 예외로 그 경로만 풀면 된다.
- 멀티파트 차단: 파일 업로드가 없는 애플리케이션이라면 `multipart/form-data` 요청을 막는 규칙을 둘 수 있다.
- 속도 제한: POST 요청에 속도 제한 규칙을 둘 수 있다.
- 서버 설정: `session.upload_progress.enabled=0`, PHP 8.5의 `fatal_error_backtraces=0` 등을 적용하고 워커를 재시작한다.
- 도입 방식: 직접 만든 규칙은 WAF 로깅을 켠 뒤 Count 모드로 시작하고, 정상 트래픽이 걸리지 않는지 확인한 다음 Block으로 바꾼다.

## 요약

AWS Security Blog의 글이다.
2026년 10월 21일 PHP 프로젝트가 PHP 코어의 원격 코드 실행 취약점 둘(CVSS v4.0 9.2)에 대한 수정을 공개했고, 수정 버전은 PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35다.
글은 패치가 유일한 완전한 해결책이라고 말하되, 플릿을 패치하려면 PHP가 어디서 실행되는지 조사하고 유지보수 창을 잡고 새 빌드로 애플리케이션을 시험해야 하므로 시간이 걸린다고 짚는다.
그 기간의 노출을 줄이는 방법으로 AWS WAF 규칙을 안내한다.

글은 공격 요소마다 AWS WAF가 도울 수 있는지를 표로 정리하고, 규칙 네 가지의 AWS WAFv2 JSON을 싣는다.
세션 업로드 진행 필드를 막는 규칙, 파일 업로드가 없을 때 멀티파트 요청을 막는 규칙, 요청 본문 크기를 제한하는 규칙, POST 요청의 속도를 제한하는 규칙이다.
그리고 WAF가 닿지 않는 부분을 서버 설정으로 막는 방법과, Count 모드로 시작해 Block으로 전환하는 도입 절차를 알린다.

## 동작 방식

### WAF가 볼 수 있는 것과 없는 것

AWS WAF는 엣지에서 HTTP 요청을 검사한다.
멀티파트 본문의 내부 구조를 파싱하지 못하고, PHP 워커의 메모리나 서버 설정을 볼 수 없다.
글은 공격 요소를 이렇게 나눈다.

| 공격 요소                                            | AWS WAF의 대응 범위                                                        |
| ---------------------------------------------------- | -------------------------------------------------------------------------- |
| 멀티파트 POST의 세션 업로드 진행 필드                | 가능. 해당 필드가 있는 요청을 막는 규칙을 둔다                             |
| 멀티파트 업로드 경로 자체                            | 업로드가 없는 애플리케이션이라면 가능. `multipart/form-data`를 막는다      |
| 과도한 본문으로 인한 메모리 부족                     | 부분적. 본문 크기를 제한한다. 헤더 증폭은 크기 제한 아래에 머물 수 있다    |
| 같은 워커에 대한 반복 시도                           | 부분적. 속도 제한은 필요한 요청량을 줄이지만 단 한 번의 성공을 막지 못한다 |
| `fatal_error_backtraces`를 만드는 쪽 (PHP 8.5)       | 불가능. 서버 설정으로 막는다                                               |
| 잘못되었거나 사용이 중단된 INI 설정이 내는 진단 경고 | 불가능. 클라이언트 HTTP가 아니라 서버 안에서 실행되는 경로다               |

헤더 증폭은 작은 멀티파트 부분 헤더 몇 킬로바이트가 PHP 안에서 훨씬 큰 메모리로 확장되는 것이다.
WAF가 본문 속 개별 부분의 헤더를 파싱할 수 없으므로, 애플리케이션이 멀티파트 업로드를 받는다면 WAF는 위험을 줄일 뿐 막지 못한다.
그 경우 글은 PHP 업그레이드를 우선하고 서버 쪽 완화를 적용하라고 한다.

### 본문 검사 한도

AWS WAF는 요청 본문의 일부만 검사한다.
Application Load Balancer와 AWS AppSync에서는 한도가 8KB로 고정이고, CloudFront와 API Gateway 같은 서비스에서는 기본 16KB이며 web ACL의 `AssociationConfig`로 32, 48, 64KB까지 올릴 수 있다.
한도를 넘는 부분은 초과(oversize)로 취급되고, 본문 크기 규칙은 검사하는 크기까지만 제한할 수 있다.
따라서 쓰려는 규칙에 맞는 한도를 먼저 정해야 한다.

### 규칙 네 가지가 막는 것

사용자 정의 규칙 `PHP2Shell`은 세 조건이 모두 참일 때만 요청을 막는다.
HTTP 메서드가 정확히 `POST`이고, `PHPSESSID`가 쿠키 키나 요청 본문 어디에든 있고, 본문에 `PHP_SESSION_UPLOAD_PROGRESS`가 있어야 한다.
이 규칙은 `session.upload_progress.enabled=0` 서버 설정과 함께 쓰라고 안내한다.
글은 이 규칙을 관리형 규칙 그룹을 쓸 수 없을 때의 대안으로 소개한다.

멀티파트 차단 규칙은 `Content-Type` 헤더에 `multipart/form-data`가 들어 있는지 본다.
헤더 하나를 이름으로 지정해 전체를 검사하므로 8KB 헤더 검사 한도의 영향을 받지 않아 믿을 만하다고 글은 설명한다.
본문 크기 규칙은 `OversizeHandling: MATCH`로 검사 한도를 넘는 본문까지 잡는다.
`Content-Length` 헤더 자체는 크기 제약으로 제한할 수 없다.
크기 제약이 숫자가 아니라 헤더 값 문자열의 길이를 재기 때문이다.
속도 제한 규칙은 POST 요청에 한정해 IP당 요청 수를 제한하며, 생산자 요청과 소비자 요청이 같은 워커에 닿아야 하는 `CVE-2026-109619` 경로를 어렵게 만든다.

## 설정하기

### 기준 상태 확인

규칙을 바꾸기 전에 WAFv2 로깅을 켜서 각 규칙이 무엇과 일치하는지 볼 수 있어야 한다.
관리형 규칙 그룹의 현재 기본 버전과 web ACL이 쓰는 버전은 읽기 전용 명령으로 확인한다.

```bash
aws wafv2 list-available-managed-rule-group-versions \
  --vendor-name AWS --name AWSManagedRulesPHPRuleSet --scope REGIONAL

aws wafv2 get-web-acl --name <web-acl-name> --id <web-acl-id> --scope REGIONAL \
  --query "WebACL.Rules[?Statement.ManagedRuleGroupStatement.Name=='AWSManagedRulesPHPRuleSet']"
```

CloudFront에 연결된 web ACL은 `--scope CLOUDFRONT`와 미국 동부(버지니아 북부) 리전을 쓴다.

### 본문 검사 한도 올리기

CloudFront의 한도를 64KB로 올리는 예다.
규칙이 필요로 하는 크기에 맞춰 값을 고른다.

```bash
aws wafv2 update-web-acl ... --association-config \
  'RequestBody={CLOUDFRONT={DefaultSizeInspectionLimit=KB_64}}'
```

### 관리형 규칙 그룹 추가

다음은 PHP application 관리형 규칙 그룹을 추가하되 `PHP2Shell_BODY`를 Count로 두는 규칙이다.
이 규칙 정의는 글의 구조를 따라 간추려 다시 쓴 것이다.

```json
{
  "Name": "AWS-AWSManagedRulesPHPRuleSet",
  "Priority": 0,
  "Statement": {
    "ManagedRuleGroupStatement": {
      "VendorName": "AWS",
      "Name": "AWSManagedRulesPHPRuleSet",
      "RuleActionOverrides": [
        { "Name": "PHP2Shell_BODY", "ActionToUse": { "Count": {} } }
      ]
    }
  },
  "OverrideAction": { "None": {} },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "AWS-AWSManagedRulesPHPRuleSet"
  }
}
```

Count로 둔 것은 일치 내역을 먼저 보기 위한 것이다.
글은 악용이 공개 직후 빠르게 이어졌으므로 이 검토 기간을 일 단위가 아니라 시간 단위로 잡으라고 한다.
확인이 끝나면 `RuleActionOverrides`를 지워 규칙이 기본 동작인 Block으로 돌아가게 한다.

### 사용자 정의 규칙

멀티파트 차단, 본문 크기 제한, 속도 제한 규칙은 관리형 규칙 그룹이 대신하지 않는다.
글도 어떤 관리형 규칙 그룹이 모든 멀티파트 요청을 막거나 POST를 속도 제한하지 않으므로 이 두 규칙은 사용자 정의로 남는다고 밝힌다.
아래 규칙은 글의 구조를 따라 간추려 쓴 것이며, 처음에는 모두 Count다.

```json
[
  {
    "Name": "Block-Multipart-FormData",
    "Priority": 10,
    "Action": { "Count": {} },
    "Statement": {
      "ByteMatchStatement": {
        "FieldToMatch": { "SingleHeader": { "Name": "content-type" } },
        "PositionalConstraint": "CONTAINS",
        "SearchString": "multipart/form-data",
        "TextTransformations": [ { "Priority": 0, "Type": "LOWERCASE" } ]
      }
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "PHP2ShellBlockMultipart"
    }
  },
  {
    "Name": "Block-Oversize-Body",
    "Priority": 11,
    "Action": { "Count": {} },
    "Statement": {
      "SizeConstraintStatement": {
        "FieldToMatch": { "Body": { "OversizeHandling": "MATCH" } },
        "ComparisonOperator": "GT",
        "Size": 8192,
        "TextTransformations": [ { "Priority": 0, "Type": "NONE" } ]
      }
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "PHP2ShellBlockOversizeBody"
    }
  },
  {
    "Name": "RateLimit-Posts",
    "Priority": 12,
    "Action": { "Count": {} },
    "Statement": {
      "RateBasedStatement": {
        "Limit": 100,
        "EvaluationWindowSec": 60,
        "AggregateKeyType": "IP",
        "ScopeDownStatement": {
          "ByteMatchStatement": {
            "FieldToMatch": { "Method": {} },
            "PositionalConstraint": "EXACTLY",
            "SearchString": "POST",
            "TextTransformations": [ { "Priority": 0, "Type": "NONE" } ]
          }
        }
      }
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "PHP2ShellRateLimitPosts"
    }
  }
]
```

우선순위는 자기 web ACL의 다른 규칙과 겹치지 않게 조정한다.
글은 관리형 규칙 그룹을 이 규칙들보다 먼저, 그 그룹의 레이블에 의존하는 예외 규칙은 그룹 뒤에 두라고 안내한다.

### 서버 쪽 완화

WAF가 닿지 않는 부분은 서버 설정으로 막는다.
FPM 풀에서 애플리케이션이 되돌릴 수 없게 적용하는 예다.
글이 권하는 설정 가운데 `.ini`로 표현되는 것만 옮겼다.

```ini
; FPM 풀 설정. php_admin_*은 애플리케이션의 ini_set()으로 바꿀 수 없다.

; CVE-2026-109618: 통제 가능한 메모리 제한 실패를 없앤다.
; 메모리 상한은 RLIMIT_AS나 RLIMIT_DATA가 아니라 컨테이너나 cgroup으로 건다.
php_admin_value[memory_limit] = -1

; 업로드를 받지 않으면 8M, 받으면 32M.
php_admin_value[post_max_size] = 8M

; CVE-2026-109619: 확인된 세션 업로드 진행 경로를 막는다.
php_admin_flag[session.upload_progress.enabled] = off

; PHP 8.5에서만: 요청 사이에 크래시 추적 상태를 저장하는 기능을 끈다.
php_admin_value[fatal_error_backtraces] = 0

; 성능이 허락하면 요청마다 워커를 재활용한다.
pm.max_requests = 1
```

글은 이 밖에 오류 로깅을 켜고(`log_errors=On`, `error_log`, `error_reporting=E_ALL`) 공격자가 닿을 수 있는 경로의 경고와 치명적 오류와 시간 초과를 없애라고 한다.
오류가 없다는 것이 안전하다는 증거는 아니라는 단서도 붙인다.

## 값 정하기

| 항목                    | 시작 값               | 근거                                                                                             |
| ----------------------- | --------------------- | ------------------------------------------------------------------------------------------------ |
| 본문 크기 규칙의 `Size` | 8192바이트            | Core rule set의 `SizeRestrictions_BODY`가 기본으로 막는 크기다. 정상 요청의 크기에 맞춰 조정한다 |
| 본문 검사 한도          | 16KB(기본), 최대 64KB | 한도보다 큰 값을 크기 규칙에 쓸 수 없다. 규칙이 필요로 하는 크기에 맞춘다                        |
| 속도 제한               | 60초에 100건          | 글이 출발점으로 든 값이다. 평소 IP당 POST 요청률에서 정한다                                      |
| `post_max_size`         | 8M 또는 32M           | 업로드가 없으면 8M, 있으면 32M이다                                                               |
| Count 모드 검토 기간    | 시간 단위             | 악용이 공개 직후 빠르게 이어졌으므로 일 단위로 잡지 않는다                                       |

속도 제한 값은 평소 IP당 POST 수를 측정해서 고쳐야 한다.
측정할 것은 정상 사용자의 60초당 최대 POST 수와, 같은 IP를 공유하는 사용자 수다.

## 트레이드오프

### 멀티파트 차단은 업로드를 끊는다

`multipart/form-data`를 막으면 두 취약점의 진입 경로를 엣지에서 없애지만, 파일 업로드가 필요한 애플리케이션은 동작하지 않는다.
브라우저의 파일 업로드뿐 아니라 일부 폼과 API 클라이언트도 멀티파트를 쓰므로, 막기 전에 Count 모드의 일치 내역으로 어떤 경로가 이 형식을 쓰는지 봐야 한다.
업로드가 있는 애플리케이션이라면 이 규칙을 쓸 수 없고, 남는 방어는 PHP 업그레이드와 서버 설정뿐이다.

### 본문 크기 제한은 큰 정상 요청도 막는다

8KB를 넘는 본문을 막으면 큰 JSON POST와 정상 업로드도 걸린다.
글은 큰 업로드가 있는 애플리케이션이라면 이 규칙을 업로드가 아닌 경로에만 적용하라고 안내한다.
그러나 경로로 좁히면 업로드 경로는 크기 제한 없이 남고, 그 경로가 바로 공격자가 노릴 수 있는 곳이다.
막지 않은 경로를 어떻게 보호할지는 이 규칙으로 해결되지 않는다.

### 속도 제한은 한 번의 성공을 막지 못한다

속도 제한은 공격에 필요한 요청량을 줄일 뿐이다.
글이 인정하듯 단 한 번의 성공적인 요청은 막지 못한다.
같은 IP를 많은 사용자가 공유하는 환경에서는 정상 사용자가 걸릴 수 있다는 점도 고려해야 하며, 이는 글이 다루지 않은 추론이다.

### 워커를 요청마다 재활용하는 비용

`pm.max_requests=1`은 오래된 상태를 남기는 요청과 그것을 쓰는 요청이 같은 워커에 닿는 연결을 끊는다.
그러나 요청마다 프로세스를 새로 만드는 비용이 들고, 글도 성능이 허락하면이라는 조건을 붙인다.
부하가 큰 서비스에서는 쓸 수 없는 완화이고, 속도 제한 규칙은 이 설정의 대체가 아니라 보완이다.

## 함정

### 규칙 그룹 전체를 Count로 돌리지 않는다

일치하는 정상 요청이 있다고 규칙 그룹 전체를 Count로 바꾸면 그 그룹의 다른 규칙도 함께 꺼진다.
글은 문제가 되는 규칙만 Count로 덮어쓰고 레이블 기반 예외로 필요한 경로만 풀라고 한다.
예외가 풀어 주는 경로는 이 규칙으로 보호되지 않으므로 가능한 한 좁게 두고 그 애플리케이션을 먼저 패치해야 한다.

### 버전을 고정하면 규칙이 없다

관리형 규칙 그룹의 버전을 고정한 web ACL에는 `Version_2.3`으로 올리기 전까지 `PHP2Shell_BODY`가 없다.
`Version_2.2`로 되돌리면 그 보호가 사라진다는 점을 글도 경고한다.
튜닝 중에는 되돌리기보다 Count 덮어쓰기와 예외를 쓰는 편이 낫다.

### Count에서 끝나는 규칙

모든 규칙이 Count로 시작하므로, 확인이 끝나고 Block으로 바꾸는 일을 하지 않으면 규칙은 아무것도 막지 않는다.
Count 모드의 규칙 일치 수는 지표에 남아 보호되고 있다는 착각을 줄 수 있다.
Block으로 바꾼 날짜를 기록하고, 관리형 규칙 그룹의 `RuleActionOverrides`를 지웠는지 확인해야 한다.

### 한도를 넘는 본문은 일부만 검사된다

`PHP2Shell_BODY`는 web ACL의 본문 검사 한도까지만 본문을 검사하고, 한도를 넘는 부분에는 Continue 옵션을 쓴다.
그래서 글은 이 규칙을 본문 크기 규칙과 함께 쓰라고 한다.
크기 규칙을 빼면 한도를 넘는 큰 본문의 뒷부분은 이 규칙이 보지 못한다.

### 이름이 다른 규칙 그룹

PHP application 규칙 그룹은 `CVE-2026-109618`을 대상으로 하지 않는다.
그 CVE에는 Core rule set의 `SizeRestrictions_BODY`를 쓰라고 글은 안내한다.
PHP 규칙 그룹만 켜 놓고 둘 다 막힌다고 여기면 안 된다.

## 확인하기

규칙을 Block으로 바꾼 뒤에는 자기 테스트 환경에서 요청 세 가지로 동작을 확인한다.
글도 정상 멀티파트 POST, 큰 본문, `PHP_SESSION_UPLOAD_PROGRESS`가 든 요청으로 시험하고 일치한 규칙의 지표를 보라고 안내한다.
아래 명령은 이 글을 쓰면서 로컬 에코 서버로 실행해, 의도한 모양의 요청이 만들어지는지만 확인했다.
WAF에 대해서는 실행하지 않았다.

```bash
URL=https://<자기-테스트-엔드포인트>/

# 1. 멀티파트 POST: 멀티파트 차단 규칙을 Block으로 바꿨다면 403이 기대된다.
curl -s -o /dev/null -w '%{http_code}\n' -X POST -F 'a=b' "$URL"

# 2. 8KB를 넘는 본문: 본문 크기 규칙을 Block으로 바꿨다면 403이 기대된다.
head -c 20000 /dev/zero | curl -s -o /dev/null -w '%{http_code}\n' \
  -X POST -H 'Content-Type: application/octet-stream' --data-binary @- "$URL"

# 3. 세션 업로드 진행 필드와 PHPSESSID가 함께 있는 요청: 403이 기대된다.
curl -s -o /dev/null -w '%{http_code}\n' -X POST \
  -b 'PHPSESSID=test' -F 'PHP_SESSION_UPLOAD_PROGRESS=x' -F 'file=@/etc/hosts' "$URL"
```

각 요청 뒤에는 CloudWatch 지표와 샘플 요청에서 어느 규칙이 일치했는지 확인한다.
정상 업로드와 큰 JSON POST가 일치하지 않는지도 같은 방법으로 본다.

## 체크리스트

- 모든 PHP 호스트의 버전과 서버 API(`mod_php`, FPM, FrankenPHP, LSAPI)를 목록으로 만들었는가?
- PHP를 해당 브랜치의 수정 버전으로 올렸고 워커를 재시작했는가?
- web ACL이 `AWSManagedRulesPHPRuleSet`을 쓰는가? 쓴다면 `Version_2.3` 이상인가?
- 관리형 규칙의 `PHP2Shell_BODY`를 Count로 덮어썼다면 덮어쓰기를 지웠는가?
- `CVE-2026-109618`에 대응하는 본문 크기 규칙이 Block 상태이고 업로드 경로는 예외로 처리했는가?
- 업로드가 없는 애플리케이션에 멀티파트 차단 규칙을 두었는가?
- 속도 제한 값은 평소 IP당 POST 수를 측정해서 정했는가?
- WAF 로깅을 켰고 각 규칙의 일치 내역을 확인했는가?
- 서버 쪽 설정(`session.upload_progress.enabled=0` 등)을 적용했는가?

## 비평

### 규칙의 효과에 대한 수치가 없다

글은 규칙마다 무엇을 막는지는 설명하지만 얼마나 막는지는 보이지 않는다.
오탐률이나 우회 사례를 시험한 결과가 없고, 속도 제한 값 100도 출발점이라고만 적는다.
이는 취약점이 공개된 지 하루도 지나지 않아 나온 완화 글이라는 사정을 감안해야 한다.
그래도 글이 말하는 보호 범위는 설계상 추론이지 관찰된 결과가 아니다.

### 세션 이름을 바꾼 애플리케이션은 이 규칙에 걸리지 않을 수 있다

사용자 정의 규칙은 `PHPSESSID`가 쿠키 키나 본문에 있어야 일치한다.
PHP의 세션 이름은 설정으로 바꿀 수 있으므로, 이름을 바꿔 쓰는 애플리케이션의 요청은 이 조건을 만족하지 못한다.
이는 글이 다루지 않은 추론이고, 그런 경우에도 업로드 진행 필드로 취약 경로에 닿을 수 있는지는 확인하지 못했다.
그래서 이 규칙에만 기대지 말고 `session.upload_progress.enabled=0`을 함께 적용하라는 글의 안내가 중요하다.

## 기억할 원칙

### WAF 규칙은 패치까지의 시간을 버는 수단이다

글의 모든 문장이 같은 말로 돌아온다.
패치가 유일한 완전한 해결책이고, WAF는 패치하는 동안 노출을 줄이는 통제이며, 패치한 뒤에는 지우거나 보조로 남긴다.
규칙을 만들었다는 사실로 일정이 늦춰지면 규칙은 해결책이 아니라 지연의 근거가 된다.

### 새 규칙은 Count로 시작하고 Block으로 바꾸는 날을 정한다

모든 규칙을 Count로 시작하면 정상 트래픽을 막는 사고는 피하지만, Block으로 바꾸는 일이 별개의 작업으로 남는다.
규칙을 넣을 때 확인 기간과 전환 날짜를 함께 정하고, 전환했는지 나중에 한 번 더 확인해야 한다.
