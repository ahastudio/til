# PHP2Shell: 패치 공개 직후 시작된 공격과 4%의 적용률

원문: [\[PHP 파장\] 세계 웹사이트 70% 쓰는 PHP, 치명적 보안 결함 발견... 정부·기업 '비상' < 국제 < 사건·사고 < 기사본문 - 보안뉴스](https://www.boannews.com/news/articleView.html?idxno=146621)

원문: [\[단독\] PHP 패치 공개 36시간, 국내 기업 적용률 4%... “96% 아직 무방비” \[PHP 파장\] < 인사이트 < 사건·사고 < 기사본문 - 보안뉴스](https://www.boannews.com/news/articleView.html?idxno=146702)

HN 토론: <https://news.ycombinator.com/item?id=50180836> (455점, 185개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release> (198점, 148개 댓글)

GN 토론: <https://news.hada.io/topic?id=35759>

## 요약

보안뉴스 국제면 기사에 따르면, PHP 개발·관리팀은 21일(현지시각) 보안 권고문을
내고 'PHP2Shell'로 명명된 취약점 2건(CVE-2026-109618, CVE-2026-109619)을 치명적
수준으로 분류했다.
두 결함은 로그인 같은 인증(authentication) 절차 없이 서버에서 악성 코드를
실행하게 하는 원격 코드 실행(remote code execution, RCE) 취약점이다.
기사는 전체 웹사이트의 70% 이상이 PHP를 쓴다는 일부 추산을 전하고,
유럽연합(EU)과 독일·일본·호주·영국·네덜란드가 보안 경보를 발령했으며 닌텐도를
포함한 기업과 단체가 일부 서비스를 일시적으로 닫았다고 보도했다.

PHP 프로젝트의 공식 권고문은 두 결함의 원인을 각각 적어 두었다.
CVE-2026-109618은 메모리 부족(out-of-memory, OOM) 오류가 났을 때 PHP가
`longjmp()`로 요청을 중단하는데, 요청 메모리가 아직 완전히 초기화되지 않았다면
요청 종료 단계가 잘못된 상태를 읽는 문제다.[^advisory-oom]
CVE-2026-109619는 워커(worker)가 유지하는 전역 상태가 한 요청이 쓰던 메모리를
가리킨 채 남고, 다음 요청의 초기화 이전 단계가 그 상태를 읽어 use-after-free가
되는 문제다.[^advisory-state]
두 권고문은 모두 CVSS 4.0 기본 점수를 9.2로
매겼다.[^advisory-oom][^advisory-state]
수정 버전은 8.5.12, 8.4.27, 8.3.36, 8.2.35다.[^phpnet]

영향 범위는 웹 요청을 처리하는 PHP 설치 전반이다.
기사는 PHP-FPM, php-cgi, 프랭큰PHP(FrankenPHP), 라이트스피드(LiteSpeed)를
열거하고, 아파치에 PHP를 직접 연결하는 mod_php 방식이 가장 위험하다고 전한다.
PHP 보안팀도 같은 판단을 밝히며, mod_php에서 인증 없는 요청 한 번이 애플리케이션
코드가 실행되기 전에 공격을 일으키는 익스플로잇(exploit)을 시연했다고
설명했다.[^bleeping]

인사이트면 단독 기사는 보안뉴스가 국내 보안 기업 에스케어와 함께
쇼단(Shodan)으로 조회한 결과를 전한다.
패치가 공개되고 약 36시간이 지난 23일 오전 11시에 PHP 8.2~8.5를 쓰는 국내 서버는
5500여 대였고, 그중 210여 대(약 3.8%)만 수정판을 쓰고 있었다.
버전별 적용률은 8.5가 6.2%, 8.3과 8.4가 각각 4.2%, 8.2가 2.8%이며, 22일 오후
6시의 0.6%에서 약 15시간 만에 3.2%p 올랐다.
기사는 미국 사이버보안·인프라보안국(CISA)이 위험도에 따라 3~14일 안의 적용을
권고하지만 기업의 평균 적용 시간은 30일 이상이었다고 대비하며, 에스케어 강기호
상무의 말을 빌려 공격 코드를 짜는 시간이 AI 때문에 더 급격히 줄었다고 전한다.

당장 업데이트하기 어려운 환경을 위한 임시 조치도 나왔다.
CVE-2026-109618에는 `memory_limit`을 -1로 두고 `post_max_size`를 낮게 유지하는
방법이, CVE-2026-109619에는 `session.upload_progress.enabled`를 0으로 바꾸고
모든 워커를 다시 시작하는 방법이 권고됐다.[^advisory-oom][^advisory-state]
PHP 프로젝트는 완전한 완화책(mitigation)은 없으며 업데이트만이 안전한 선택이라고
밝혔다.[^phpnet]
8.1 이하는 프로젝트의 지원이 끝났지만, 보안팀은 7.4, 8.0, 8.1용 최소 소스 패치를
따로 공개했다.[^helpnet]

## 분석

### 애플리케이션 코드가 실행되기 전에 작동하는 결함

이번 결함이 평소의 웹 취약점과 다른 점은 공격이 일어나는 위치다.
SQL 인젝션이나 파일 업로드 취약점은 애플리케이션 코드의 허점이어서, 해당
플러그인을 고치거나 입력 검증을 덧붙이면 막을 수 있다.
PHP2Shell은 PHP 엔진이 요청을 받아 메모리를 준비하고 정리하는 과정에서 일어난다.
mod_php에서는 요청 초기화 단계에서 공격이 성립한다고 PHP 보안팀이
설명했으므로,[^bleeping] 애플리케이션 계층의 점검은 이 경로에 닿지 못한다.

그래서 사이트 앞단의 웹 애플리케이션 방화벽(web application firewall, WAF)
규칙이 거의 유일한 외부 방어가 되었다.
Cloudflare는 무료 요금제 고객을 포함한 모든 고객에게 방화벽 규칙을 켰고, 공개 약
9시간 전부터 적용했다고 한다.[^tnw]
Cloudflare 스스로 이 규칙이 임시 보호일 뿐이라고 경고했다는 점도 함께
전해졌다.[^tnw]
방화벽이 알려진 공격 형태를 걸러 주는 동안 엔진을 고치는 일이 끝나야 한다는
구조다.

영향 범위를 세는 단위도 달라진다.
애플리케이션 취약점은 그 애플리케이션을 쓰는 사이트가 대상이지만, 이번에는 PHP로
웹 요청을 처리하는 모든 프로세스가 대상이다.
국제면 기사가 위험 요인으로 꼽은 것이 조직이 존재조차 파악하지 못한 오래된
홍보용 웹사이트, 호스팅 관리 도구, PHP가 탑재된 기기라는 점은 이 구조에서
나온다.
코드 저장소를 기준으로 한 점검으로는 찾을 수 없는 자산이 방어에서 빠지게 된다.

Lobste.rs 사용자 fanf는 이 결함에 메모리 안전성(memory safety)과 직접 관계없는
측면이 있다고 짚었다.[^fanf]
하나는 PHP의 핵심 자료구조가 요청마다 새로 만들어지지 않고 이어지는 요청에서
재사용되어, 한 요청이 일으킨 손상을 다음 요청이 이용할 수 있다는 점이다.[^fanf]
다른 하나는 OOM 상황의 `longjmp`가 자료구조의 불변 조건을 깨뜨릴 수 있다는 예외
안전성(exception safety) 문제다.[^fanf]
앞의 두 권고문이 적은 원인과 같은 방향의 설명이다.

### 패치가 공개되는 순간 공격 준비가 시작된다

인사이트면 기사는 패치 디핑(patch diffing)을 공격 준비의 핵심 수단으로 소개한다.
패치가 적용된 새 소스 코드와 이전 버전을 비교하면 어느 코드가 바뀌었는지
드러나고, 그 변경이 곧 취약점의 위치를 알려 준다는 것이다.
국제면 기사에 인용된 디텍티파이(Detectify)의 조비안 자르딤도 같은 지적을 했으며,
산섹(Sansec)은 패치 공개 15분 만에 대량 공격이 이뤄질 것으로 예상했다고
인사이트면 기사는 전한다.
Lobste.rs 사용자 pushcx는 지난달 한 프로젝트가 조용히 패치를 담은 변경 요청을
열었을 뿐인데, 공개되고 10분이 지나기 전에 공격 시도가 있었다고 적었다.[^pushcx]

이번 사안에서는 공식 권고문이 비교 작업을 더 쉽게 만든다고 볼 여지가 있다.
권고문은 수정 방식을 구체적으로 적어 두었다.
`longjmp()` 대신 다음 VM 안전 지점(VM safe point)에서 처리하는 지연된 소프트
OOM(soft OOM)으로 바꾸고, 더 높은 두 번째 한도에서는 `_exit()`로 끝내는 하드
OOM(hard OOM)을 둔다는 내용이다.[^advisory-oom]
이는 필자의 추론이며, 권고문이 공격 코드 제작을 실제로 앞당겼는지는 이 자료들로
확인되지 않는다.

더구나 공개 이전의 시간도 안전하지 않았다.
TNW에 따르면 기술 세부 정보가 온라인에 유출되어 PHP가 예정보다 하루 일찍 패치를
냈다.[^tnw]
아마존 위협 인텔리전스는 공개 4일 전인 10월 17일에 자사 허니팟(honeypot)
네트워크에서 공격 시도를 관측했다고 밝혔다.[^helpnet]
패치 공개일을 공격의 출발점으로 보는 가정이 이번에는 맞지 않았다는 뜻이다.

### 두 기사는 서로 다른 단위로 사건을 잰다

국제면 기사는 위협의 크기를, 인사이트면 기사는 방어의 속도를 잰다.
앞의 기사가 쓰는 단위는 전체 웹사이트의 70%, 대응에 나선 국가의 수 같은 세계
규모의 숫자다.
뒤의 기사가 쓰는 단위는 쇼단에서 조회된 국내 서버 5500여 대 가운데 수정판을 쓰는
비율이다.

두 숫자는 분모가 달라서 곱하거나 이어 붙일 수 없다.
PHP를 쓰는 웹사이트의 비율조차 기사마다 다르다.
국제면 기사는 70% 이상이라고 쓰지만, BleepingComputer는 75%에서 80%라고
전한다.[^bleeping]
한쪽은 사이트, 다른 쪽은 인터넷에 노출된 호스트를 세는 방식의 차이일 수 있다.
BleepingComputer는 VirusTotal 추정으로 노출된 PHP 호스트가 510만 곳을 넘는다고
인용했다.[^bleeping]

## 비평

### “성공 사례 없음”이라는 문장은 날짜를 붙여야 읽힌다

국제면 기사는 와치타워의 제이크 노트가 한 말, 곧 지금까지 성공한 곳은 없지만 그
상태가 오래가지는 않을 것이라는 경고를 싣는다.
인사이트면 기사는 위협 인텔리전스 기업 켈라(KELA)가 22일 기준으로 성공 사례를
확인하지 못했다고 평가했고, CISA도 두 취약점을 알려진 악용 취약점(Known
Exploited Vulnerabilities, KEV) 목록에 올리지 않았다고 전한다.
두 기사 모두 22일 안팎의 상태를 말한다.

그 뒤의 보도는 다른 상황을 보여 준다.
ISMG의 보도에 따르면 네덜란드 국가사이버보안센터는 성공적인 악용의 초기 징후를
조사 중이라고 밝혔고, VulnCheck는 다른 치명적 결함과 연결하지 않아도 되는
동작하는 익스플로잇을 만들었다고 말했다.[^ismg]
같은 보도에서 Sophos 연구진은 아직 동작하는 익스플로잇을 만들지 못했고, 상용
봇넷 운영자의 시도도 지금까지 실패했다고 했다.[^ismg]
성공 사례가 없다는 말과 동작하는 익스플로잇이 없다는 말은 다른 주장이며, 앞의
것은 탐지된 침해가 없다는 뜻일 뿐 침해가 없다는 뜻이 아니다.

이 판단을 바꿀 관찰은 분명하다.
CISA의 KEV 등재, 침해 사고를 공개한 조직의 등장, 또는 독립 연구자가 기본 설정의
서버에서 익스플로잇을 재현했다는 보고가 나오면 “성공 없음”이라는 서술은 유지될
수 없다.
기사를 읽는 시점이 22일이 아니라면 이 문장은 그 시점에 다시 확인해야 한다.

### 4%와 96%는 같은 것을 가리키지 않는다

인사이트면 기사의 제목은 96%가 아직 무방비라고 말한다.
그러나 패치를 적용하지 않은 서버가 곧 방어되지 않은 서버는 아니다.
방화벽 규칙이나 설정 변경 같은 임시 조치를 이미 적용한 서버가 있을 수 있고, 같은
기사의 본문이 패치 이외의 대응을 따로 다루지 않으므로 이 구분은 제목에서
사라진다.

더 큰 문제는 분모다.
조사 대상은 PHP 8.2~8.5를 쓰는 서버뿐이어서, 지원이 끝난 8.1 이하는 집계에
들어가지 않는다.
ISMG가 전한 Censys 집계에서 가장 흔한 버전은 지원이 끝난 7.4.33이고 호스트의
16%를 차지했다.[^ismg]
가장 위험하고 가장 오래 방치될 집단이 4%라는 숫자의 바깥에 있다.

측정 방식에도 한계가 있다.
기사는 PHP 버전 정보가 삭제된 채 조회된 서버를 집계에서 제외했고 그래서
조치율에는 영향이 거의 없을 것이라고 적었다.
그런데 배포판이 업스트림 버전 번호는 그대로 둔 채 수정만 가져오는
백포트(backport) 방식을 쓰는 경우가 있다.
이 경우 수정을 마친 서버도 쇼단에는 옛 버전으로 보이므로 적용률이 낮게 잡힐
수 있다.
이는 필자의 추론이며 이번 조사에서 그 영향이 얼마인지는 확인되지 않는다.

Hacker News 사용자 bananamogul은 PHP가 두 취약점을 9.2로 매긴 데 비해 Red Hat은
8.1로 매겼다는 점을 짚고, 배포판의 기본 구성이 달라서인지 물었다.[^bananamogul]
같은 스레드에서 jacobalcock은 SELinux가 있어도 mod_php와 php-fpm이 `httpd_t`로
실행되고 이 영역은 `/bin/sh`를 실행할 수 있어 셸 실행을 막지 못한다고
답했다.[^jacobalcock]
워커 안에서 실행되는 코드는 애플리케이션이 다루는 인증 정보를 그대로 본다는
설명도 덧붙었다.[^jacobalcock]
패치하지 않은 서버를 얼마나 방어할 수 있는지는 배포판과 구성에 따라 달라서,
제목의 96%라는 숫자는 하나의 위험 수준을 뜻하지 않는다.

같은 ISMG 보도에서 Censys는 패치된 호스트가 약 810만 곳으로, 버전을 보고하는
서비스 4150만 개의 약 20%라고 집계했다.[^ismg]
국내 3.8%와 이 20%는 시점, 대상, 방법이 모두 달라 직접 비교할 수 없다.
다만 36시간 시점의 한 숫자만으로 국내 대응이 느리다고 단정하기도, 빠르다고
단정하기도 어렵다는 점은 분명하다.

### 속도 단축의 원인을 AI로 돌리는 근거는 부분적이다

인사이트면 기사는 AI의 발전으로 취약점 발견에서 공격 준비까지의 시간이 급속히
줄었다고 쓰고, 국제면 기사는 공개된 PoC(proof of concept, 개념증명) 도구 가운데
AI로 작성된 프로그램이 있다고 전한다.
뒷받침하는 보도는 있다.
Wiz 연구진은 최첨단 AI 모델이 진입 장벽을 크게 낮추어 오래된 결함을
익스플로잇으로 바꾸었다고 말했다.[^helpnet]
BleepingComputer는 이 취약점의 발견이 Calif, OpenAI, Wiz의 보안 연구자에게
돌아갔다고 전한다.[^bleeping]

반대 방향의 증거도 같은 보도 안에 있다.
ISMG에 따르면 떠도는 PoC 수백 개 가운데 상당수는 주소 공간 배치 무작위화(address
space layout randomization, ASLR)를 우회하지 못해 실패하고 있다.[^ismg]
Trail of Bits의 Dan Guido는 한 연구자가 OpenAI Codex로 MediaWiki에서 셸을
얻었지만 깊은 전문성이 핵심이었다고 말했다.[^ismg]
AI가 발견과 초안 작성의 비용을 낮춘 것은 사실로 보이나, 성공하는 익스플로잇까지
낮춘다는 근거는 이 자료에 없다.
Hacker News 사용자 asbv-1qq는 이번 결함이 최소 20년 된 코드에 있었는데도 발견과
익스플로잇 작성에 든 컴퓨팅 비용이 공개되지 않았다고 지적했다.[^asbv-1qq]
AI가 사람보다 빠르다는 주장을 따지려면 바로 그 비용이 필요하다.

패치 디핑은 AI 이전부터 있던 방법이어서 속도 단축의 몫을 AI와 나누려면 비교
기준이 필요하다.
과거 사례에서 패치 공개부터 첫 동작하는 익스플로잇까지 걸린 시간을 모아 이번
건과 비교하면 답이 나온다.
그런 비교가 없는 지금은 AI가 원인이라는 문장을 전문가 의견으로 읽어야 하고,
측정된 사실로 읽어서는 안 된다.

## 인사이트

### 사전 통지는 방어자와 공격자에게 같은 시간을 준다

국제면 기사에 따르면 PHP 관리팀은 권고문을 내기 전날 저녁 두 결함을 치명적으로
분류하고 긴급 업데이트를 준비하라고 알렸다.
BleepingComputer는 이 경고가 세부 정보가 공개되거나 실제 공격이 나타나면 더 일찍
낼 수 있다는 말과 함께 나갔다고 전한다.[^bleeping]
리눅스 배포판과 장기 지원 업체에는 공개 전에 패치가 전달됐다.[^helpnet]
방어가 가장 많이 필요한 쪽에 먼저 시간을 주려는 설계다.

그런데 이번에는 세부 정보가 유출됐고, 패치는 하루 앞당겨졌으며,[^tnw] 공격
시도는 공개 4일 전부터 관측됐다.[^helpnet]
알고 있는 사람이 늘수록 새어 나갈 가능성도 커진다는 것이 이 구조의 약점이다.
Hacker News 사용자 edh649는 Calif가 8월 11일에, Wiz가 8월 24일에 각각 공개
절차를 시작한 것으로 보인다고 적었고,[^edh649] Topfi는 보고에서 공개까지 두 달이
걸린 이유와 확인 응답까지 한 달이 걸린 이유를 이해하기 어렵다고 적었다.[^Topfi]
같은 결함을 여러 팀이 따로 찾았다면 비공개 기간이 길수록 유출될 경로도
늘어난다는 것이 필자의 추론이다.

Lobste.rs 사용자 hoistbypetard는 PHP의 갱신 안내를 인용했다.[^hoistbypetard]
그 글에 따르면 10월 21일 07:41 UTC, 조율된 공개보다 6시간 넘게 앞서 Chainguard가
수정이 담긴 빌드 이미지를 먼저 공개했고, 다른 배포 업체와 마찬가지로 패치를 미리
받았기 때문에 가능한 일이었다.[^hoistbypetard]
공격자가 수정 내용을 바이너리 형태로 살펴볼 수 있게 됐다는 것이 안내의
설명이다.[^hoistbypetard]
kingmob은 PHP 재단 글을 따라 경과를 정리했다.[^kingmob]
부정확한 세부 정보가 새어 나가 PHP가 발표를 하루 앞당겼고, 이어 발견자 중 하나인
Calif가 PoC 영상을 잘못 올렸다가 지웠으며, 마지막으로 Chainguard의 이미지가
나왔다는 순서다.[^kingmob]
kingmob은 전 세계 웹사이트의 70%가 갱신되기 전에 LLM을 쓰는 공격자 한 명이
익스플로잇을 만드는 상황밖에 상상하기 어렵다고 보았고,[^kingmob] hoistbypetard는
이해관계자가 이렇게 많을 때 조율된 공개(coordinated disclosure)의 가치를 다시
따져 봐야 한다고 답했다.[^hoistbypetard-2]
이는 필자의 추론이지만, 사전 통지가 방어자에게 준 시간과 공격자가 얻은 시간이
같은 크기였을 수 있다는 점은 이번 경과가 보여 준다.

여기서 나오는 판단은, 사전 통지를 받은 조직은 공개일을 기다리지 말고 통지를 받은
시점부터 이미 공격이 진행 중이라고 가정해야 한다는 것이다.
인사이트면 기사가 전한 대로 숙련된 보안팀은 패치 공개 몇 시간 만에 야근으로
적용을 마쳤고, 인력과 야근 보상 체계가 부족한 기업은 다음 날 출근 시간에야
작업을 시작했다.
통지에서 적용까지의 시간은 기술이 아니라 당직과 보상의 제도가 결정한다.

### 패치 적용률은 자산 목록(asset inventory)의 크기를 알 때만 의미가 있다

적용률은 분자를 분모로 나눈 값이고, 분모는 조직이 알고 있는 서버의 수다.
국제면 기사가 지목한 가장 큰 위험은 조직이 존재조차 파악하지 못한 서버였다.
알지 못하는 서버는 분모에 들어가지 않으므로, 적용률이 100%에 가까워도 방치된
서버가 남는다.

이 점은 쇼단 조사의 구조와도 닮았다.
인터넷에서 보이는 서버만 세는 조사는 바깥에서 볼 수 있는 자산의 비율을 잴
뿐이며, 내부망이나 장비 안에 든 PHP는 잴 수 없다.
Palo Alto Networks가 PAN-OS 전 버전이 영향을 받는다고 확인하고 아직 수정
릴리스를 내지 못했다는 보도가 이를 보여 준다.[^helpnet]
PHP를 직접 설치하지 않았는데도 장비 안에 PHP가 들어 있는 경우다.

그래서 이번 사안에서 조직이 할 일은 순서가 정해져 있다.
먼저 PHP가 요청을 처리하는 모든 자산을 목록으로 만들고, 그 목록에서 버전과 지원
상태를 확인한다.
수정 버전이 없는 8.1 이하는 업그레이드나 공급업체의 백포트 확인으로 보내고, 그
외에는 적용 시각을 기록해 적용률이 분모와 함께 보이게 한다.
목록에 없던 서버가 외부 스캔에서 먼저 발견된다면 그것이 이 절차가 실패한
지점이다.
Lobste.rs 사용자 Two9A는 이번이 어떤 사이트가 PHP로 돌아가는지 알게 되는
기회라고 적으며, 자신이 일하는 DeviantArt가 아침 내내 점검 중 페이지를 띄웠다고
전했다.[^Two9A]
GeekNews 사용자 rtyu1120은 국내에서 제로보드와 그누보드를 아직 쓰는 곳이 얼마나
될지 물었다.[^rtyu1120]
두 프로그램은 PHP로 만든 게시판 소프트웨어이며, 인사이트면 기사가 센 5500여 대
안에 이런 설치가 얼마나 들어 있는지는 기사에서 알 수 없다.

### 완화(mitigation) 설정은 위험을 다른 곳으로 옮긴다

CVE-2026-109618의 첫 번째 임시 조치가 `memory_limit=-1`이라는 점은 눈여겨볼
만하다.
OOM 오류가 공격의 시작점이므로 메모리 한도를 없애 오류 자체를 일으키지 못하게
하는 방식인데, 이는 PHP가 요청 하나에 쓸 수 있는 메모리의 상한을 없애는
일이기도 하다.
공식 권고문은 이 설정을 완전한 완화책이 아니라고 하면서, 대신 컨테이너나
cgroup의 `memory.max`를 가용성의 경계로 두고 문제가 된 워커만 종료하도록 하라고
안내한다.[^advisory-oom]
`RLIMIT_AS`나 `RLIMIT_DATA`는 쓰지 말라고도 덧붙인다.[^advisory-oom]

국제면 기사는 이 조치를 소개하면서 메모리 한도를 없애는 대가를 적지 않았다.
공격을 막는 설정이 서비스 거부(denial of service)의 위험을 키울 수 있다는 점은
운영자가 따로 판단해야 한다.
보안 위험 하나를 줄이면 가용성 위험이 생기는 이런 교환은 임시 조치가 대개 안고
있는 성질이다.

임시 조치가 얼마나 오래 남는지도 문제다.
`session.upload_progress.enabled=0`은 CVE-2026-109619의 임시 조치였는데, PHP는
10월 23일 별도 CVE(CVE-2026-115560)에 대한 참고용 권고에서도 다음 버그 수정
릴리스 전까지 같은 설정을 꺼 두라고 안내했다.[^phpnet-session]
긴급 패치로 끝나지 않고 후속 권고가 이어졌다는 것은, 임시 조치를 적용한 서버의
설정을 기록해 두고 이후 릴리스에서 되돌릴 시점을 정해야 한다는 뜻이다.

Hacker News 사용자 azyc는 낮은 `pm.max_requests`가 워커 재사용에 기댄 부분은
줄일 수 있어도, 워커들이 공유하는 메모리인 OPcache의 타입 혼동(type
confusion)에는 소용이 없다고 짚었다.[^azyc]
그래서 `session.upload_progress.enabled=0`이 더 값싼 임시 수단으로 보인다는 것이
azyc의 판단이다.[^azyc]
airtnp는 구버전용 백포트가 새 버전처럼 원인을 고치지 않고 세션 업로드 진행률
기능 자체를 끄는 방식으로 읽힌다고 적었다.[^airtnp]
이는 airtnp의 해석이며 이 문서가 코드를 직접 확인한 것은 아니지만, 사실이라면
8.1 이하에 제공되는 수정은 새 버전과 같은 수준의 보호가 아닐 수 있다.

mort는 설정 변경 하나로 악용을 막을 수 있다는 정보가 떠돌지만, PHP 핵심 개발자
Gina Banyard의 말로는 사실이 아니며 유일한 완화책은 패치라고 적었다.[^mort]
dsr는 PHP가 도는 머신에 저장된 모든 것이 접근 가능하다고 가정하라고
덧붙였다.[^dsr]
임시 조치만 적용한 서버는 패치 전까지 침해됐을 수 있다고 보고, 그 서버가 다룬
자격 증명(credential)의 교체 범위를 미리 정해 두어야 한다는 것이 필자의
판단이다.

---

[^advisory-oom]: GitHub, [RCE via OOM corruption · Advisory · php/php-src · GitHub](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), 2026-10-21

[^advisory-state]: GitHub, [RCE via stale global state · Advisory · php/php-src · GitHub](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp), 2026-10-21

[^phpnet]: PHP, [Security advisory: Critical remote code execution vulnerabilities, update now](https://www.php.net/archive/2026.php#2026-10-21-5), 2026-10-21

[^phpnet-session]: PHP, [Informational advisory: Session upload progress](https://www.php.net/archive/2026.php), 2026-10-23

[^bleeping]: BleepingComputer, [PHP ships emergency patches for critical PHP2Shell flaws](https://bleepingcomputer.com/news/security/php-ships-emergency-patches-for-critical-php2shell-flaws), 2026-10-21

[^helpnet]: Help Net Security, [PHP2Shell: Critical PHP vulnerabilities patched, update now!](https://www.helpnetsecurity.com/2026/10/21/php2shell-php-vulnerabilities-patched-cve-2026-109618-cve-2026-109619/), 2026-10-21

[^tnw]: TNW, [Cloudflare sees millions of attempts to exploit critical PHP flaws](https://thenextweb.com/news/cloudflare-php2shell-millions-exploit-attempts), 2026-10-23

[^ismg]: ISMG, [Waiting for the PHP2Shell Onslaught as PoCs Proliferate](https://www.govinfosecurity.com/waiting-for-php2shell-onslaught-as-pocs-proliferate-a-33190)

[^bananamogul]: <https://news.ycombinator.com/item?id=50184082>

[^jacobalcock]: <https://news.ycombinator.com/item?id=50187799>

[^asbv-1qq]: <https://news.ycombinator.com/item?id=50181413>

[^edh649]: <https://news.ycombinator.com/item?id=50181632>

[^Topfi]: <https://news.ycombinator.com/item?id=50181515>

[^azyc]: <https://news.ycombinator.com/item?id=50185593>

[^airtnp]: <https://news.ycombinator.com/item?id=50182077>

[^pushcx]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_mpnkx1>

[^fanf]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_drpzov>

[^hoistbypetard]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_vhy7rg>

[^kingmob]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_bmgjok>

[^hoistbypetard-2]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_byx3sm>

[^Two9A]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_fegwh3>

[^mort]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_sbgc5z>

[^dsr]: <https://lobste.rs/s/ekxoyt/upcoming_critical_php_security_release#c_msttox>

[^rtyu1120]: <https://news.hada.io/topic?id=35759#cid68292>
