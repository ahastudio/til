# Cloudflare Cache Rules의 Vary 지원: 원본이 “무엇이 달라질 수 있는지”를 말하면 캐시가 “무엇이 중요한지”를 정한다

원문: [We just shipped support for the ugliest part of HTTP: Vary | Cloudflare Blog](https://blog.cloudflare.com/vary-support/)

HN 토론: <https://news.ycombinator.com/item?id=49823195> (147점, 40개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/iulfsj/we_just_shipped_support_for_ugliest_part> (4점, 2개 댓글)

GN 토론: <https://news.hada.io/topic?id=34282>

## 소개

Cloudflare의 Alex Krivit와 Zaidoon Abd Al Hadi가 2026년 9월 22일 발표한 기능이다.
응답 헤더 `Vary`를 이제 모든 요금제의 Cache Rules에서 쓸 수 있다.
원본은 여전히 응답에 영향을 줄 수 있는 요청 헤더를 이름으로 알려 주고, 사용자는 Cloudflare가 각 헤더의 값을 어떻게 다룰지 정한다.
알려진 협상 헤더는 정규화하고, 작은 차이가 중요할 때는 정확한 값을 그대로 쓰고, 변동이 너무 예측 불가능하면 캐시를 우회한다.

글은 `Vary`가 “아직 개선하지 못한 HTTP의 가장 못생긴 부분”, 중간 캐시 사이의 상호 운용성이 “꽤 처참한 끔찍하고 엉성한 장치”라고 불렸다는 인용으로 시작한다.
그러면서 못생겼다고 쓸모없는 것은 아니라고 말한다.

## 동작 방식

### Vary가 푸는 문제

한 URL에 올바른 응답이 둘 이상일 수 있다.
브라우저가 `Accept: text/html`로 `/catalog`를 요청하면 원본은 HTML을 주고, API 클라이언트가 같은 URL을 `Accept: application/json`으로 요청하면 JSON을 준다.
원본은 응답에 `Vary: Accept`를 붙여, URL만으로는 응답을 고를 수 없고 요청의 `Accept` 값도 봐야 한다고 캐시에 알린다.
`Vary`가 없으면 먼저 캐시에 들어간 응답이 두 클라이언트 모두에게 나가서, HTML이 먼저 들어가면 API 클라이언트의 JSON 파서가 실패하고 JSON이 먼저 들어가면 브라우저가 API 응답을 받는다.

### Vary가 만드는 문제

`Vary`는 어떤 요청 필드가 응답에 영향을 줄 수 있는지는 알려 주지만, 두 요청의 값이 다를 때 정말 다른 응답이 필요한지는 알려 주지 않는다.
영어, 프랑스어, 독일어만 서비스하는 원본에 `Accept-Language: en-US, fr;q=0.8`과 `Accept-Language: fr;q=0.8, en-GB`가 오면, 둘 다 영어를 원하지만 날것의 값을 비교하는 캐시는 같다고 가정할 수 없다.
원본은 수천 가지 언어 선호가 세 언어로 모인다는 것을 알지만 캐시는 모른다.

여러 필드로 달라지면 문제는 곱해진다.
한 필드에 값이 10개면 변형이 10개, 세 필드에 10개씩이면 1,000개다.
`User-Agent`는 값이 무수히 많고, 쿠키는 방문자마다 다르며, 선호 헤더는 순서와 공백과 품질 값이 제각각이다.
결과는 완벽하게 정확하지만 거의 영원히 차가운 캐시다.
글에 따르면 인기 사이트 약 5만 곳의 응답 1억 2천만 개 이상을 분석한 결과, 거의 3,000개 사이트가 네 개 이상의 필드로 달라졌고, 10개, 23개, 심지어 47개 필드로 달라지는 곳도 있었다.

### 요청이 캐시를 지나는 순서

1. 첫 요청에는 그 자원에 대해 저장된 Vary 정보가 없으므로 캐시를 놓친다. 일치하는 Cache Rule은 원본에 요청을 보내기 전에 설정된 필드를 정규화할 수 있다.
2. 원본이 `Vary: Accept, Accept-Language`로 답하면, Cloudflare는 그 헤더 이름을 기록하고 응답을 하나의 변형으로 저장한다.
3. 다음 요청이 오면 기본 캐시 키, 곧 URL과 설정된 키 필드로 시작해, 저장된 Vary 필드를 새 요청에 규칙대로 적용해 해당 변형을 곧바로 찾는다. 저장된 변형을 하나씩 비교하지 않는다.
4. 맞는 변형이 신선하면 적중이고, 아니면 원본에 보내 새 변형으로 저장할 수 있다.

정규화가 원본으로 보내기 전에 일어나는 이유가 있다.
Cloudflare가 여러 날것의 값을 하나의 정규화된 캐시 키로 묶는데 원본은 날것의 값을 받는다면, 원본이 서로 다른 응답을 만들어도 캐시는 그것들을 바꿔 써도 되는 것으로 여길 수 있다.
정규화된 값을 원본에 보내야 원본의 선택과 캐시의 일치가 어긋나지 않는다.
그래서 `Accept`와 `Accept-Language`는 정규화된 값이 원본으로 가고, `Accept-Encoding`은 Respect Strong ETags가 켜져 있을 때만 정규화된 값이 간다.
다른 헤더는 캐시 일치에만 정규화된다.

## 설정하기

### 세 가지 동작

| 동작          | Cloudflare가 하는 일                                               | 쓰기 좋은 곳                                 |
| ------------- | ------------------------------------------------------------------ | -------------------------------------------- |
| `normalize`   | 협상 헤더를 규칙대로 정리해 같은 뜻의 요청이 한 변형을 공유하게 함 | 많은 값이 적은 응답으로 모이는 협상 헤더     |
| `passthrough` | 대소문자, 공백, 순서, 중복까지 날것의 바이트로 캐시를 일치시킴     | 값의 집합이 통제되고 정확한 값이 응답을 바꿈 |
| `bypass`      | 원본이 그 헤더를 `Vary`에 넣으면 응답을 저장하지 않음              | `Cookie`, `User-Agent` 같은 개인화 헤더      |

`normalize`는 `Accept`, `Accept-Language`, `Accept-Encoding`의 값을 소문자로 바꾸고, 품질 값이 높은 순으로, 같으면 알파벳순으로 정렬한다.
그래서 클라이언트가 보낸 순서는 캐시 키에 영향을 주지 않는다.
정렬 뒤에는 품질 값이 0이 아닌 항목의 매개변수를 떼어 낸다.
그 밖의 헤더는 선택적 공백을 다듬고 반복된 헤더 줄을 원래 순서대로 합칠 뿐, 대소문자와 내부 공백은 그대로 둔다.
`Accept`와 `Accept-Language`에서는 원하는 미디어 유형과 언어만 남기게 할 수 있고, `en-US` 같은 지역 태그는 전체 태그를 설정하지 않으면 기본 언어 `en`으로 줄어든다.

`passthrough`는 `X-View: compact,full`, `X-View: Compact,full`, `X-View: compact, full` 세 값을 서로 다른 캐시 키로 만든다.
Cloudflare는 기본값으로 `normalize`를 권하고, 개인적이거나 값이 끝없는 헤더에는 `bypass`를, 정확한 값이 응답을 바꿀 때만 `passthrough`를 쓰라고 한다.
설정과 무관하게 `Vary: *`는 늘 캐시를 우회한다.

### Rulesets API 예시

대시보드에서는 Caching > Cache Rules에서 규칙을 만들고 응답을 캐시 가능하게 한 뒤 Vary 설정을 더한다.
API로는 `http_request_cache_settings` 단계에 다음처럼 넣는다.

```json
{
  "rules": [
    {
      "ref": "vary_negotiated_content",
      "description": "Cache bounded negotiated representations",
      "expression": "(http.host eq \"example.com\" and http.request.uri.path eq \"/catalog\")",
      "action": "set_cache_settings",
      "action_parameters": {
        "cache": true,
        "vary": {
          "default": { "action": "normalize" },
          "headers": {
            "accept": {
              "action": "normalize",
              "media_types": ["text/html", "application/json"]
            },
            "accept-language": {
              "action": "normalize",
              "languages": ["en", "fr", "de"]
            }
          }
        }
      }
    }
  ]
}
```

이것은 진입점에 대한 `PUT`의 전체 요청 본문이고, `PUT`은 그 진입점의 모든 규칙을 바꾼다.
이미 Cache Rules가 있다면 `rules` 배열에 함께 넣거나 규칙 하나를 만들고 고치는 작업을 써야 한다.
Terraform으로도 설정할 수 있다.

### 사용자 지정 캐시 키와 무엇이 다른가

`Accept`와 `Accept-Language`를 사용자 지정 캐시 키에 넣는 방법도 있다.
그러나 사용자 지정 키는 원본이 그 헤더를 썼든 안 썼든 규칙이 덮는 모든 응답에 그 차원을 더한다.
`Vary`는 응답이 정하지만, 같은 기본 키 아래 캐시 가능한 응답들은 일관된 Vary 필드 집합을 가져야 한다.
요청의 속성이 늘 자원을 정의하면 사용자 지정 키를, 원본이 캐시 가능한 응답 전반에서 같은 요청 필드 집합을 선언하면 `Vary`를 쓰라는 것이 글의 기준이다.

## 함정

### Vary를 빠뜨린 응답 하나가 나머지를 덮을 수 있다

글은 원본이 무거운 책임을 진다고 적는다.
요청 필드에 따라 달라질 수 있는 모든 캐시 가능한 응답은 오류와 대체 응답까지 포함해 적절한 `Vary`를 일관되게 돌려줘야 한다.
하나라도 빠뜨리면, Cloudflare는 그 응답을 변동 없이 캐시할 수 있다.

Hacker News에서 rob-olmos는 이 두 문장을 나란히 인용하며, `Vary`가 없는 캐시 객체가 `Vary`로 나뉜 객체들을 앞질러 버리는지 묻고, 그렇다면 모든 응답에 `Vary`가 붙게 하는 Snippet 규칙을 두는 것이 좋겠다고 적었다.[^rob-olmos]
원본의 404나 500 응답, 기본값으로 떨어지는 경로가 `Vary`를 빼먹기 쉬운 곳이다.

### 설정을 바꿔도 기존 캐시는 지워지지 않는다

Vary 설정을 바꾸면 캐시 키가 달라질 수 있지만, 기존 콘텐츠는 자동으로 지워지지 않는다.
새 요청은 새 키로 놓치고 다시 채워지며, 옛 항목은 만료되거나 지워질 때까지 남는다.
`bypass`도 기존 캐시 항목을 지우지 않으므로 필요하면 직접 퍼지해야 한다.
자원을 대상으로 한 퍼지는 그 자원의 모든 Vary 변형을 덮는다.

### 정규화는 “허용하지 않음”을 잃을 수 있다

`normalize`는 언어 태그를 줄이거나 설정한 형식과 언어로 걸러 낼 때 `q=0`, 곧 “받아들일 수 없음”을 잃을 수 있다.
글의 예로 `en-US;q=0`이 `en`이 될 수 있다.
원본이 이런 제외를 봐야 한다면 `Accept`나 `Accept-Language`에 `passthrough`를 써야 한다.

Hacker News에서 charcircuit은 `en-US`와 `en-GB`를 왜 같게 다뤄야 하느냐며, 미국 방문자가 `colour` 같은 철자를 보게 되지 않느냐고 물었다.[^charcircuit]
tancop은 대부분의 사이트는 영어 변형을 따로 두지 않고, 두 나라에 물건을 판다면 보통 HTTP 언어 체계가 아니라 지역 선택기를 쓴다고 답했다.[^tancop]
지역 변형을 실제로 서비스한다면, 전체 태그를 설정해 기본 언어로 줄어들지 않게 해야 한다.

### 여섯 가지 조합이 캐시 키 여섯 개를 뜻하지 않는다

예시처럼 미디어 유형 둘과 언어 셋이면 콘텐츠 조합은 여섯이지만, 선호 순서, 빠진 헤더, 정규화 뒤 빈 값 때문에 캐시 키는 더 많아질 수 있다.
지원하는 집합을 작게 유지하고 규칙의 경계를 분명히 해야 한다.

## 확인하기

글이 권하는 확인 방법은 이렇다.

1. 같은 변형으로 정규화돼야 할 서로 다른 헤더 값으로 같은 URL을 요청한다.
2. 같은 클라이언트에서 보내고, 기대한 형식과 언어가 오는지 확인한다.
3. `CF-Cache-Status`를 보고, 캐시가 채워진 뒤 적중이 나오는지 본다.
4. 계속 놓치거나 예상치 못하게 우회되는 응답을 조사한다.

```bash
# 순서와 지역 태그만 다른 두 요청이 같은 변형을 공유하는지 확인한다
for lang in "en-US, fr;q=0.8" "fr;q=0.8, en-GB"; do
  curl -s -o /dev/null -D - -H "Accept: text/html" -H "Accept-Language: $lang" \
    https://example.com/catalog | grep -i -E "cf-cache-status|content-language"
done
```

## 체크리스트

- 달라질 수 있는 모든 캐시 가능한 응답, 곧 오류와 대체 응답까지 같은 `Vary`를 돌려주는가?
- `Cookie`, `User-Agent`처럼 값이 끝없는 헤더에 `bypass`를 설정했는가?
- `normalize`에 원본이 실제로 서비스하는 미디어 유형과 언어만 설정했는가?
- 원본이 `q=0` 제외를 봐야 하는 헤더에 `passthrough`를 썼는가?
- 설정을 바꾼 뒤 필요한 자원을 퍼지했는가?
- 같은 헤더를 사용자 지정 캐시 키와 `Vary`에 함께 넣지 않았는가, 넣었다면 의도하고 시험했는가?

## 인사이트

### 20년 된 헤더를 제대로 지원하기까지의 시간이 CDN의 우선순위를 보여 준다

Hacker News의 첫 반응은 대부분 안도였다.
simonw는 이 기능을 수년 동안 원했다며, `Accept: text/html`을 보내는 클라이언트에는 HTML을, 그렇지 않은 클라이언트에는 JSON을 주는 방식이 Cloudflare가 이미지 외에는 `Vary`를 무시했기 때문에 캐시 뒤에서 배포할 수 없었다고 적었다.[^simonw]
bhouston은 예전에 CloudFront에서 `Vary`를 잘 썼고 Cloudflare도 당연히 지원할 줄 알았다가 자기 SaaS 앱에 심각한 버그가 났다고 했고,[^bhouston] xyzzy_plugh는 절대 출시하지 않을 줄 알았다며 2026년에 진짜 콘텐츠 협상을 보게 될 줄 몰랐다고 적었다.[^xyzzy_plugh]

colmmacc는 20여 년 전 Apache 2.0의 여러 mod_cache 하위 모듈에 Vary 지원을 넣었던 경험을 떠올리며, 고통 대비 보상이 너무 낮았고 사용자 에이전트의 버그와 이상한 백엔드를 끝없이 드러냈다고 적었다.[^colmmacc]
지리 위치 같은 가상 헤더로 달라지게 하자는 논쟁과, 말이 안 되는 `Date:`로 달라지게 해 달라는 요청까지 있었다는 것이다.
Cloudflare가 이 기능을 늦게 낸 것은 기술이 어려워서라기보다, 잘못 쓰면 캐시를 망가뜨리는 기능을 모든 고객에게 안전하게 주는 방법을 찾아야 했기 때문이다.
세 가지 동작과 `normalize` 기본값은 그 답이다.

### Vary의 진짜 문제는 HTTP가 제공하지 않는 기능을 Vary에 얹어 온 역사다

Lobste.rs에서 craigstuntz는 Cloudflare가 `Vary`를 “엉성하다”고 부른 글을 정확히 인용하지 않았다고 지적했다.[^craigstuntz]
원래 글은 `Vary`가 지리 위치로 캐시를 나누는 데 끔찍하고 엉성한 장치라고 한 것이며, 문제는 `Vary` 자체보다 사용자가 원하는데 HTTP가 제공하지 않는 기능을 `Vary` 위에 억지로 얹는 데 있다는 것이다.
Hacker News에서 jiehong도 `Accept-Language`는 RFC 4647의 세 가지 방식 중 하나로 파싱하고 일치시켜야 하는데 그 복잡함은 `Vary`의 잘못이 아니라고 적었다.[^jiehong]

이 관점에서 Cloudflare의 해법은 `Vary`를 고친 것이 아니라, `Vary`가 전하지 못하는 정보, 곧 원본이 실제로 어떤 표현을 서비스하는지를 Cache Rules로 따로 알려 주게 한 것이다.
글이 마지막에 만료된 Availability Hints 초안의 아이디어를 검토하고 있다고 밝힌 것도, 결국 원본이 자기가 서비스하는 표현을 직접 서술하게 하는 방향이다.
kevincox가 지적한 캐시 병합의 어려움, 곧 응답을 받기 전에는 두 요청이 같은 응답을 공유할지 알 수 없어 뒤따르는 요청을 막을지 그냥 보낼지 정해야 한다는 문제도,[^kevincox] 원본이 표현의 목록을 미리 알려 주면 풀 여지가 생긴다.

---

[^rob-olmos]: <https://news.ycombinator.com/item?id=49824234>

[^charcircuit]: <https://news.ycombinator.com/item?id=49826351>

[^tancop]: <https://news.ycombinator.com/item?id=49826697>

[^simonw]: <https://news.ycombinator.com/item?id=49823961>

[^bhouston]: <https://news.ycombinator.com/item?id=49823965>

[^xyzzy_plugh]: <https://news.ycombinator.com/item?id=49824063>

[^colmmacc]: <https://news.ycombinator.com/item?id=49825920>

[^craigstuntz]: <https://lobste.rs/s/iulfsj/we_just_shipped_support_for_ugliest_part#c_3ymuze>

[^jiehong]: <https://news.ycombinator.com/item?id=49827557>

[^kevincox]: <https://news.ycombinator.com/item?id=49830677>
