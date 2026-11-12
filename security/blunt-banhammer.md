# 숨은 링크 하나로 AI 봇을 영구 차단한다: 허니팟과 .htaccess로 만든 B6의 구현과 맹점

원문: [Blunt Banhammer Blocks Basic Bots Ballistically](https://shkspr.mobi/blog/2026/11/blunt-banhammer-blocks-basic-bots-ballistically/)

HN 토론: <https://news.ycombinator.com/item?id=50435925> (6점, 4개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots>

GN 토론: <https://news.hada.io/topic?id=36981>

## 소개

Terence Eden은 2026년 11월 9일 글에서 자신의 취미 사이트 OpenBenches.org가
지난달 2.5TB가 넘는 데이터를 방문자에게 전송했다고 밝힌다.
사이트가 그렇게 인기 있다고 보기는 어렵고, AI 봇이 데이터를 끝없이 긁고 이미지를
빨아들인 것으로 보인다는 것이다.
그래서 만든 것이 B6이라는 “가리지 않는” 차단 도구다.
Jeff Starr의 Blackhole에서 느슨하게 영감을 얻었지만 캐시가 강한 사이트에서도
동작한다고 한다.
글은 이를 직접 만드는 방법과 일으킬 수 있는 문제를 함께 설명하고, 코드는 AGPL
v3로 다뤄 달라고 요청한다.

글이 보고하는 결과는 다음과 같다.
이 도구를 돌린 지 일주일 동안 400개가 넘는 IP 주소를 차단했고 트래픽이 크게
줄었으며 불만은 아직 없었다.
정점에는 하루 216GB를 전송했는데 지금은 약 25GB 정도다.
글의 첫 문장은 “간단한 함정으로 봇 트래픽을 80% 넘게 줄였다”이다.
이 수치는 글쓴이가 한 사이트에서 일주일 동안 본 값이다.

## 동작 방식

B6은 크롤러의 행동 두 가지를 이용한다.
예의 바른 봇은 `robots.txt`를 읽고 금지된 곳에 가지 않는다.
크롤러는 페이지의 링크를 모두 찾아 방문한다.
그러므로 모든 페이지에 사람에게는 보이지 않는 링크를 걸고, 그 링크의 대상을
`robots.txt`에서 금지하면, 그 링크를 따라간 것은 `robots.txt`를 무시한 봇이다.

1. 사이트에 `/honeypot/` 같은 디렉터리를 만들고 `index.php`를 둔다.
2. `robots.txt`에서 이 경로를 `Disallow`로 명시한다.
3. 모든 페이지에 이 경로를 가리키는 숨은 링크를 넣는다.
4. 누가 이 페이지에 접근하면 그 IP를 `.htaccess`에 적는다.
5. `.htaccess`는 그 IP의 모든 접근을 영구 차단한다.

글쓴이는 이 방식이 거짓 양성이 없다고 말한다.
일반 사용자는 링크를 따라갈 수 없고 예의 바른 봇은 링크를 따라가지 않기
때문이다.
Anubis 같은 도구와 비교해 설치할 일이 많고 일반 사용자를 귀찮게 하는 반면, B6은
특정 호스팅 환경이 필요 없고 일반 사용자에게 보이지 않는다고 대비한다.

## 구현하기

### robots.txt

```text
User-agent: *
Disallow: /honeypot/
```

봇은 보통 24시간마다 갱신을 확인하므로 하루를 기다리거나 주요 크롤러에 직접
제출하라고 글쓴이는 적는다.

### .htaccess

차단 목록은 다른 재작성 규칙보다 앞에 있어야 한다.

```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
### BLOCKED IPs
    #   TEST-NET-1
    RewriteCond %{REMOTE_ADDR} "=192.0.2.1"
    RewriteRule ^ - [R=402,L]
### /BLOCKED IPs
    # ... 기존 규칙 ...
</IfModule>
ErrorDocument 402 "Payment Required - Access Denied."
```

차단된 IP에는 402 오류와 읽을 수 있는 메시지가 간다.
메시지는 원하는 평문으로 바꿀 수 있다.

### 함정 페이지(index.php)

글의 PHP 코드는 방문자의 IP와 User-Agent를 읽고, 상위 디렉터리의 `.htaccess`를
읽어 `### BLOCKED IPs` 줄 바로 아래에 날짜와 User-Agent를 주석으로, IP를
`RewriteCond` 조건 줄로 끼워 넣어 파일을 다시 저장한다.
블록이 없으면 아무것도 하지 않고 끝낸다.
IP는 `X-Forwarded-For`의 쉼표 목록, `REMOTE_ADDR`, `HTTP_CLIENT_IP`를 모아 사설
대역과 예약 대역을 걸러낸 첫 유효 값을 쓴다.

### 숨은 링크

```html
<a id="honey" aria-hidden="true" href="/honeypot/index.php">&zwj;</a>
```

```css
#honey {
    display: none !important;
    cursor:  none !important;
}
```

링크는 접근성 트리에서 빼고, 눌러 볼 글자 대신 너비가 없는 문자(ZWJ)를 넣으며,
CSS로 숨긴다.

## 트레이드오프

글쓴이가 직접 꼽는 문제는 다음과 같다.

| 문제                                       | 글의 대응                                                           |
| ------------------------------------------ | ------------------------------------------------------------------- |
| 사람이 링크를 눌러 차단됨                  | 차단 메시지에 풀어 달라는 방법을 적는다                             |
| robots.txt를 무시하는 유용한 봇            | 스스로 밝히는 봇이면 `.htaccess`에서 손으로 빼거나 허용 목록을 둔다 |
| robots.txt를 지키지만 문제인 봇            | 못 잡는다                                                           |
| 차단 IP가 수천 개로 늘면 느려질 수 있음    | 약한 일화적 근거만 있고 걱정할 정도는 아니라고 본다                 |
| 탈취된 IP를 쓰다 주인이 바뀜               | 항목마다 시각이 있으니 오래된 것을 주기적으로 푼다                  |
| 같은 봇이 IP를 돌려 가며 여러 번 걸림      | 해결책 없음                                                         |
| CSS로 숨겼다고 봇이 링크를 피함            | 보이지 않는 문자로 대체한다                                         |
| 똑똑한 봇이 `/honeypot/`이라는 이름을 피함 | 더 나은 이름과 여러 종류의 함정을 쓴다                              |

글쓴이는 이 도구가 경고도 User-Agent나 국가 판별도 없이 접근 즉시 영구 차단하는
“무딘 방망이”라고 스스로 부르고, 자동으로 이의를 제기할 방법이 없다고 인정한다.

## 비평

### “거짓 양성이 없다”는 주장은 글의 문제 목록이 이미 반박한다

글은 한편으로 B6에 거짓 양성이 없다고 하고, 다른 한편으로 탈취된 IP의 새 주인이
차단될 수 있다고 인정한다.
두 진술은 양립하지 않는다.
거짓 양성이 없다는 말은 “링크를 따라간 것은 모두 봇이다”라는 가정 아래서만 맞고,
그 가정이 깨지는 경로가 여럿이다.

HN의 joshblack1982는 통신사가 CGNAT 뒤에 두어 같은 IP를 여러 사람이 쓰는데,
함정에 접근하면 같은 통신사 이웃이 모두 차단될 수 있고 이를 일부러 반복해 많은
사람을 막을 수도 있다고 썼다.[^joshblack1982]
글쓴이 edent는 이를 작은 걱정으로 인정하면서, 이웃이 자기 블로그를 못 읽는다고
아쉬워하지는 않을 것이며 몇 주 뒤에 IP를 풀도록 만들겠다고 답했다.[^edent]
그는 부수 피해보다 자기 대역폭이 더 중요하다고 밝혔다.
이는 거짓 양성이 없다는 주장을 거짓 양성을 감수한다는 입장으로 바꾼 것이다.

mzajc는 두 가지를 더 짚었다.
메신저의 링크 미리 보기나 Internet Archive, archive.today, 구글 번역처럼 사람이
조작하지만 robots.txt를 무시하는 서비스에 함정 주소를 보내면 그 서비스 전체가
사이트에서 막히고, 악의적으로 다른 사이트에서 함정 주소를 가리키는 이미지를 걸어
방문자를 차단시킬 수도 있다는 것이다.[^mzajc]
이 두 시나리오가 얼마나 흔한지는 알 수 없다고 mzajc도 인정했다.
다만 둘 다 봇이 아닌 방문자가 함정에 닿는 경로이므로, 글의 “일반 사용자는 링크를
따라갈 수 없다”는 전제는 같은 사이트의 HTML 안에서만 성립한다.

### 이 글이 보여 주는 코드에는 글이 말하지 않은 위험이 있다

이 지적은 글의 코드를 읽고 추론한 것이며 실제로 시험한 것이 아니다.

- **IP를 헤더에서 읽는다.** `get_client_ip()`는 `X-Forwarded-For` 목록의 첫
  유효한 공인 IP를 `REMOTE_ADDR`보다 먼저 고른다.
앞단에 신뢰하는 프록시가 없으면 이 헤더는 요청자가 마음대로 적을 수 있으므로,
  함정에 닿으면서 다른 사람의 IP를 적어 그 사람을 차단시킬 수 있을 것이다.
글이 이 코드를 koko-analytics 프로젝트에서 가져왔다고 밝히지만 프록시를 신뢰하는
  배치인지는 설명하지 않는다.
Lobste.rs의 stephenr도 이 헤더를 맹목적으로 믿는 것이 나쁜 생각이라며, 접속
주소가 그
  프록시인지 먼저 확인해야 한다고 지적했다.[^stephenr]
- **웹 프로세스가 접근 제어 파일을 쓴다.** `index.php`는 `.htaccess`를 읽고 다시
  쓰므로 웹 서버 사용자에게 그 파일의 쓰기 권한이 있어야 한다.
이 페이지나 같은 사용자 권한으로 도는 다른 코드가 뚫리면 접근 제어 파일을 바꿀
  수 있다.
- **동시 요청이 규칙을 덮어쓸 수 있다.** 파일을 읽고 고쳐서 다시 쓰는 사이에
  잠금이 없고, 봇은 한꺼번에 여러 요청을 보낸다.
한 요청이 쓴 규칙을 다른 요청이 옛 내용 위에 덮어쓸 수 있다.
- **차단 목록이 선형으로 자란다.** 글쓴이는 수천 개까지는 걱정하지 않는다고
  하지만, 규칙은 요청마다 위에서부터 평가되므로 일주일에 400개라면 몇 달 뒤의
  모양은 글이 보여 주지 않는다.

### 같은 목적을 더 쉽게 달성하는 방법이 이미 있다는 반응이 이어졌다

글은 Anubis와 비교해 설치가 쉽다는 점을 내세우지만, 독자들은 함정 로그를 읽어
방화벽으로
넘기는 방법을 더 가볍다고 보았다.
Lobste.rs의 cornel은 복잡해 보인다며 접근 로그에서 함정 경로를 `grep`해 나온
IP를
방화벽으로 막으면 되지 않느냐고 물었다.[^cornel]
zimpenfish는 fail2ban과 보이지 않는 링크로 하고 있다고 답했고,[^zimpenfish]
wheybags는
fail2ban은 만료되는 차단을 지원해서 누군가 우연히 봇넷을 호스팅했다는 이유로
CGNAT
전체를 영구히 막지 않는다고 덧붙였다.[^wheybags]
Nerdeiro는 세 번 이상 접근한 경우에만 걸리게 하고 한 시간 동안 차단하는 규칙을
제안하며,
Cloudflare나 Akamai 같은 프록시 뒤라면 WAF 규칙에 넣으라고 했다.[^Nerdeiro]
freddyb는 함정 URL과 링크를 두지 않고 `wp-admin.php`처럼 사이트에 없는 흔한
주소를
요청하는 쪽을 차단하는 것만으로 비슷한 효과를 보았다고 했다.[^freddyb]
이들은 B6이 풀려는 문제(봇 식별)보다 차단 방식(영구, 즉시, 웹 프로세스가 파일
수정)에
대한 대안이다.
글의 문제 목록에서 가장 큰 항목인 거짓 양성과 IP 변동은 만료와 임계값이 있는
도구가
구조적으로 줄인다.
다만 이런 도구를 이미 운영하고 있다는 전제가 필요해서, `.htaccess`와 PHP만 쓸 수
있는
공유 호스팅 환경에서는 B6이 여전히 선택지가 된다.
이는 이 문서의 해석이다.

### 80% 감소의 근거가 짧고 한 곳이다

첫 문장의 80%는 정점의 하루 216GB와 현재 약 25GB를 비교한 것으로 보인다.
정점 하루와 일주일 뒤를 비교하면 절감폭이 부풀려지기 쉽고, 한 사이트의 한 주
자료이며, 차단된 것이 AI 봇인지 일반적인 봇인지는 확인된 바 없다.
글쓴이도 이 도구가 가장 정교한 봇 차단기라고 주장하지 않는다고 했고, 자기가
만드는 즐거움을 말했다.

## 확인할 것

- 이 방식은 `robots.txt`를 무시하는 봇만 잡는다.
규칙을 지키는 봇의 부하는 이 방법으로 줄지 않는다.
- 함정 링크가 있는 사이트가 앞단에 CDN이나 프록시를 둔다면 `REMOTE_ADDR`가 그
  프록시의 주소가 되어 프록시 전체가 차단될 수 있다.
신뢰하는 프록시의 헤더만 읽도록 바꿔야 한다.
- 차단 항목에 시각이 있으므로 만료 정책(몇 주 뒤 해제)을 먼저 정한다.
- 메신저 미리 보기, 웹 보관 서비스, 번역기가 함정 주소에 닿지 않도록 허용
  목록이나 사용자 에이전트 예외를 둘지 정한다.
- fail2ban 같은 만료와 임계값이 있는 도구를 쓸 수 있는 환경이면 먼저 그쪽을
  본다.
- 차단 후 로그에서 같은 User-Agent가 여러 IP로 반복되는지 본다.

## 기억할 원칙

자동 차단은 “누구를 막는가”보다 “잘못 막힌 사람이 어떻게 풀려나는가”를 먼저
설계해야 한다.
이 글의 방식은 앞의 질문에는 단순하게 답하지만, 뒤의 질문에는 만료 시각 하나가
전부다.

---

[^joshblack1982]: <https://news.ycombinator.com/item?id=50439760>

[^edent]: <https://news.ycombinator.com/item?id=50439890>

[^mzajc]: <https://news.ycombinator.com/item?id=50447938>

[^stephenr]: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots#c_w7lzdh>

[^cornel]: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots#c_wtlsbe>

[^zimpenfish]: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots#c_r2o6dv>

[^wheybags]: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots#c_rjbwuv>

[^Nerdeiro]: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots#c_xcu1i6>

[^freddyb]: <https://lobste.rs/s/bubqox/blunt_banhammer_blocks_basic_bots#c_xgglvr>
