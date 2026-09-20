# localias: /etc/hosts와 Caddy로 로컬 개발 서버에 이름과 TLS를 붙이기

<https://github.com/peterldowns/localias>

HN 토론: <https://news.ycombinator.com/item?id=36006628> (11점, 4개 댓글)

## 소개

localias는 개발 서버용 로컬 별칭을 안전하게 관리하는 도구다.

하는 일이 한 줄로 설명된다. **`https://server.test` → `http://localhost:3000`** 리다이렉트를 브라우저에서도 명령줄에서도 동작하게 만드는 것이다.

README가 내세우는 기능은 이렇다.

- URL에 포트 없이 편한 이름을 쓴다
- 개발 웹사이트를 TLS 뒤에서 서빙해 개발과 프로덕션의 차이를 줄인다 — **CORS 문제 없음, 보안 쿠키 설정 가능**
- macOS와 Linux, 그리고 WSL2에서도 동작한다
- 기본적으로 모든 별칭의 TLS 인증서를 자동 발급하고 설치한다
- 별칭을 추가하고 제거할 때마다 **`/etc/hosts`를 자동 갱신**해 모든 도구에서 동작하게 한다
- 포그라운드로 돌리거나 백그라운드 데몬으로 돌린다
- 공유 설정 파일을 지원해 팀 전체가 같은 별칭을 쓴다
- 요청 프록시와 TLS 인증서 생성을 [Caddy](https://caddyserver.com/)로 처리해 빠르고 기본적으로 안전하다
- `.local` 도메인을 mDNS로 서빙해 휴대폰이나 같은 네트워크의 다른 기기에서 개발 서버를 방문할 수 있다

[lcl.host 노트](lcl-host.md)와 같은 문제를 다루는데 접근이 다르다.
lcl.host가 **관리형 사설 CA**를 쓰는 반면 localias는 Caddy가 로컬에서 만든 루트 인증서를 쓴다.

실제로 저자 peter_l_downs가 lcl.host 발표 스레드에 직접 댓글을 남겼다.
lcl.host가 `lcl.host`와 `localhost` 서브도메인으로만 인증서를 발급할 수 있다는 제약을 인용하며, localias는 **원하는 커스텀 도메인 무엇이든** 쓸 수 있다는 것이다.

## 설치

```bash
# Homebrew
brew install peterldowns/tap/localias

# Go
go install github.com/peterldowns/localias/cmd/localias@latest

# Nix (flakes)
nix profile install --refresh github:peterldowns/localias
```

바이너리 직접 내려받기도 지원한다. `darwin-amd64`, `darwin-arm64`, `linux-amd64`, `linux-arm64`다.

HN Show HN 스레드에서 zallarak이 크로스 플랫폼으로 배포한 점을 높이 샀고,[^zallarak] 저자가 Homebrew와 nix와 go와 실행 파일 내려받기 어느 쪽으로든 쉽게 설치되도록 애썼다고 답했다.[^peterldowns]

## 설정 파일

localias는 두 부분이다. **설정 파일**과 **프록시 서버**다.

### 탐색 순서

`localias`를 실행할 때마다 다음 순서로 설정 파일을 찾고 처음 발견한 것을 쓴다.

1. `--configfile <path>`를 명시하면 그 경로
2. 환경 변수 `LOCALIAS_CONFIGFILE=<path>`
3. 현재 디렉터리의 `.localias.yaml`
4. **Git 저장소 안이라면 저장소 루트의 `.localias.yaml`**
5. 그 외에는 `$XDG_CONFIG_HOME/localias.yaml`(없으면 생성)
   - macOS 기본값: `~/Library/Application Support/localias.yaml`
   - Linux·WSL 기본값: `~/.config/localias.yaml`

네 번째 항목이 이 도구의 팀 공유 기능을 만든다. **저장소 루트에 `.localias.yaml`을 커밋하면 팀 전체가 같은 별칭을 쓴다.**

현재 쓰이는 설정 파일을 확인하는 방법이 따로 있다.

```bash
# 현재 설정 파일 경로 출력
localias debug config

# 현재 설정 파일 내용 출력
localias debug config --print
```

### 형식

설정은 `<별칭>: <포트>` YAML 맵이다.

```yaml
bareTLD: 9003                     # https와 http 둘 다 서빙
implicitly_secure.test: 9002      # https와 http 둘 다 서빙
https://explicit_secure.test: 9000  # https와 http 둘 다 서빙
http://explicit_insecure.test: 9001 # http만 서빙
```

스킴을 붙이지 않거나 `https://`를 붙이면 둘 다 서빙하고, `http://`를 명시하면 HTTP만 서빙한다.

### 설정 명령

```bash
localias set <alias> <port>   # 별칭 추가·수정
localias list                 # 별칭 목록
localias rm <alias>           # 별칭 제거
localias clear                # 전체 삭제
localias import path/to/another/config/localias.yaml  # 다른 설정 가져오기
```

## 프록시 서버 동작

`localias run`이나 `localias start`를 실행하면 순서대로 이 일들이 일어난다.

1. 현재 설정 파일을 읽어 별칭과 대상 포트를 파악한다
2. `/etc/hosts`를 확인해 모든 별칭이 있는지 본다
   - 없는 별칭을 추가한다
   - 설정에서 사라진 오래된 별칭을 제거한다
   - **변경이 있을 때만 파일을 쓴다.** `sudo` 권한이 필요하기 때문이다
3. Caddy 프록시 서버를 실행한다
   - 로컬 루트 인증서가 없으면 생성하고, **시스템 트러스트 스토어와 (접근 가능하다면) Firefox 인증서 저장소에 설치**한다
   - 각 별칭을 올바른 로컬 포트로 넘기는 Caddy 설정을 생성한다
   - 현재 쓰이는 각 별칭의 TLS 인증서를 생성하고 서명한다
   - 요청을 프록시하기 위해 **80·443 포트에 바인딩**한다

### 권한

세 가지에 상승된 권한이 필요하다고 명시한다.

- `/etc/hosts` 편집
- 로컬 생성 루트 인증서를 시스템 스토어에 설치
- 프록시 서버 실행을 위한 80·443 포트 바인딩

필요할 때마다 `sudo`로 서브셸을 열어 수행하며 비밀번호를 묻는데, **localias가 비밀번호를 읽거나 다루지는 않는다**고 밝힌다.

그리고 한 줄이 덧붙는다. **localias는 전적으로 로컬이며 어떤 텔레메트리도 수행하지 않는다.**

이 문장이 [lcl.host](lcl-host.md)와의 가장 큰 차이다. 계정도 네트워크 호출도 없다.

### 첫 실행

```console
$ localias set frontend.test 3000
[added] frontend.test -> 3000

$ localias list
frontend.test -> 3000

$ localias run
# root 인증 프롬프트가 한 번 이상 뜬다
2023/05/02 23:12:58.218 INFO  tls.obtain  acquiring lock  {"identifier": "frontend.test"}
2023/05/02 23:12:58.230 INFO  tls.obtain  certificate obtained successfully  {"identifier": "frontend.test"}
# 이제 요청을 기다린다
```

중요한 동작이 하나 있다. `Ctrl-C`로 멈추고 다시 실행하면 **sudo 프롬프트가 다시 뜨지 않는다**.
`/etc/hosts`와 인증서가 이미 갖춰져 있으면 변경할 것이 없기 때문이다.

### 데몬 모드

```bash
localias start    # 데몬으로 프록시 서버 시작
localias status   # 데몬 상태 확인
localias reload   # 최신 설정을 프록시 서버에 적용
localias stop     # 데몬 중지
```

데몬으로 돌 때는 설정을 바꿔도 자동으로 반영되지 않는다. **명시적으로 `reload`해야 한다.**

```bash
localias set frontend.test 3000
localias start
localias set frontend.test 4004
# 데몬은 아직 3000을 보고 있다
localias reload   # 이제 4004가 적용된다
```

## 기존 도구와의 차이

README가 hotel과 chalet를 대체 대상으로 명시하고 비교를 제시한다.
hotel은 더 이상 유지보수되지 않고 chalet는 사실상 같은 기능의 포크라는 것이다.

| 항목      | localias                                 | hotel                         |
| --------- | ---------------------------------------- | ----------------------------- |
| 배포 형태 | 단일 바이너리                            | NodeJS 런타임 필요            |
| 동작 방식 | `/etc/hosts` 수정 — 관찰과 디버그가 쉬움 | 브라우저나 OS에 프록시로 설정 |
| 적용 범위 | **`curl`과 스크립트에서도 동작**         | 브라우저에서만 동작           |
| TLD       | 여러 TLD에 원하는 만큼 별칭              | TLD 하나만                    |
| TLS       | 루트 인증서 생성·설치, 경고 없음         | TLS 서명 없음                 |
| 팀 공유   | Git 저장소의 설정 파일 자동 탐색         | 공유 설정 없음                |
| 프로세스  | 관리하지 않음(전적으로 사용자 몫)        | 프로세스 실행·관리 시도       |

세 번째 줄이 실무에서 가장 크게 갈린다.
브라우저 프록시 설정으로 동작하는 방식은 `curl`이나 스크립트나 다른 프로그램의 요청에는 적용되지 않는다.

마지막 줄도 설계 철학의 차이다. **localias는 프로세스 관리를 하지 않는다.**

### 왜 만들었는가

저자가 오랫동안 `localhost:8080`을 방문하다가 해법을 찾아보고 hotel과 chalet를 발견했으며, 훌륭한 프로젝트이고 영감이 되었지만 더 낫고 유용한 방식으로 구현했다고 생각한다는 것이다.

그리고 친구 Justin의 트윗을 인용한다.
`localhost:8000 → application.local`, `localhost:3000 → marketing.local`, `localhost:3002 → docs.local` 같은 걸 해 주는 도구가 분명히 있는데 이름이 도무지 기억나지 않는다는 내용이다.

HN 스레드에서 그 Justin(jmduke)이 직접 나타나 사용 사례를 적었다.[^jmduke]
Overmind로 관리하는 Procfile에 `app-web`, `app-vite`, `app-storybook`, `api`, `docs`, `marketing` 여섯 프로세스를 돌리는데, 나이를 먹어서인지 **어느 프로세스가 3003이고 3002이고 3001인지 기억하는 것이 미치도록 짜증스러웠다**는 것이다.
매일 몇 초의 좌절을 아끼게 해 줘서 고맙다고 적었다.

저자가 답했다. 애초에 이걸 만들도록 영감을 준 것에 감사한다는 것이다.[^peter_l_downs]

## 트레이드오프

### `/etc/hosts`를 고치는 방식이 관찰 가능성과 권한 요구를 맞바꾼다

이 도구의 핵심 설계 결정이 `/etc/hosts` 수정이다.

얻는 것이 크다. **브라우저만이 아니라 시스템의 모든 클라이언트에 적용된다.**
`curl`도, 언어 런타임의 HTTP 클라이언트도, 백그라운드 스크립트도 같은 이름을 해석한다.

그리고 상태가 투명하다. `cat /etc/hosts`로 지금 무엇이 걸려 있는지 즉시 볼 수 있고, 문제가 생기면 그 파일을 직접 고치면 된다.
README가 이것을 hotel 대비 장점으로 명시한다. 관찰과 디버그가 쉽다는 것이다.

대가는 `sudo`다.

그리고 이 대가가 생각보다 넓다. `/etc/hosts` 편집과 루트 인증서 설치와 80·443 바인딩 셋 모두 권한을 요구한다.

localias가 이 부담을 줄이는 방식이 영리하다. **변경이 있을 때만 파일을 쓴다.**
그래서 재시작할 때 프롬프트가 다시 뜨지 않는다.

다만 근본적인 긴장은 남는다.
개발 도구가 시스템 전역 파일을 고치고 시스템 트러스트 스토어에 인증서를 넣는다는 것은, 그 도구를 시스템 수준으로 신뢰한다는 뜻이다.

“전적으로 로컬이며 텔레메트리가 없다”는 README의 문장이 그 신뢰를 요청하는 근거다.
오픈소스이므로 검증 가능하다는 점이 그것을 뒷받침한다.

### 루트 인증서에 이름 제약이 없다는 것이 유연성의 대가다

localias의 장점으로 저자가 내세운 것이 **어떤 커스텀 도메인이든 쓸 수 있다**는 점이다.

그런데 그 유연성이 구조적으로 요구하는 것이 있다. **이름 제약이 없는 루트 CA**다.

[lcl.host](lcl-host.md)는 CA 인증서에 이름 제약을 걸어 `lcl.host`와 `localhost` 서브도메인만 유효하게 한다.
그래서 그 CA의 개인키가 새더라도 다른 도메인을 사칭할 수 없다.

localias는 임의 도메인의 인증서를 발급해야 하므로 그 제약을 걸 수 없다.
Caddy가 만든 로컬 루트 인증서가 시스템 트러스트 스토어에 들어가면, **그 키로 서명한 어떤 도메인의 인증서든 시스템이 신뢰한다.**

이것이 localias만의 문제는 아니다. mkcert도 같고, 로컬에서 임의 도메인 인증서를 만드는 모든 도구가 같다.

실무적 의미는 이렇다.
그 루트 개인키가 있는 파일이 곧 **시스템 전체의 TLS 신뢰를 좌우한다**.

경로는 확인할 수 있다.

```bash
# 루트 인증서 경로 확인
localias debug cert
# 예: ~/Library/Application Support/localias/caddy/pki/authorities/local/root.crt
```

개인키가 같은 디렉터리에 있으므로, 그 디렉터리를 백업 대상에서 제외하고 공유 드라이브에 두지 않는 것이 맞다.

### 팀 공유가 편의이면서 신뢰 확장이다

저장소 루트의 `.localias.yaml`을 자동으로 찾는 기능이 팀 공유의 핵심이다.

새 팀원이 저장소를 클론하고 `localias start`만 하면 모두가 같은 URL로 개발할 수 있다.
문서에 “`localhost:3001`로 접속하세요”라고 적는 대신 `https://api.test`를 공유하면 된다.

그런데 이 파일이 **시스템 전역 파일을 고치는 명령의 입력**이라는 점을 봐야 한다.

`.localias.yaml`에 적힌 이름들이 `/etc/hosts`에 들어간다.
저장소에 쓰기 권한이 있는 사람이 그 파일을 바꾸면, 그것을 실행한 팀원의 시스템 hosts 파일이 바뀐다.

악의적 시나리오가 성립한다. 자주 쓰는 도메인을 별칭으로 넣으면 그 팀원의 요청이 로컬 프록시로 향한다.

README가 이 위험을 직접 다루지는 않지만, 바로 다음에 나오는 도메인 충돌 경고가 같은 메커니즘을 설명한다.

실무 규칙이 나온다. **`.localias.yaml`을 코드 리뷰 대상으로 다루고, 실제 도메인처럼 보이는 항목이 들어오면 막는다.**

## 함정

### 실제 도메인을 별칭으로 쓰면 안 된다

README의 “Domain conflicts and HSTS” 절이 이 도구를 쓸 때 가장 중요한 경고다.

**기존 웹사이트와 같은 이름의 별칭을 만들면 안 된다**는 것이다.
프로덕션에서 `https://example.com`으로 서비스하는 웹사이트를 작업하고 있다면, `example.com`을 개발 서버로 가리키는 로컬 별칭을 정말로 만들고 싶지 않을 것이라고 적는다.

그러면 브라우저가 예상 밖의 일을 한다며 둘을 든다.

**쿠키 오염**: 개발 쿠키가 프로덕션 요청에 포함되고 그 반대도 마찬가지다.
localias를 껐다 켜며 개발과 프로덕션을 오가면 이 쿠키들이 서로 충돌해 사용자와 웹사이트를 극도로 혼란스럽게 만든다는 것이다.

**HSTS 충돌**: 프로덕션 웹사이트가 HSTS나 인증서 피닝을 쓰면 그것을 로컬 별칭으로 쓸 때 매우 무서운 오류를 보게 된다.
localias가 다른 개인키로 콘텐츠를 서빙하는데 **HSTS가 브라우저에 그것을 명시적으로 금지하라고 알려 주기 때문**이다.

그래서 권고가 명확하다. 이 문제를 아예 피하고 `.test`나 `.example`이나 `.localhost`처럼 **쓰이지 않는 TLD**로 끝나는 별칭을 쓰라는 것이다.

이 경고가 중요한 이유가 하나 더 있다.
HSTS 오류는 해당 도메인에 대한 브라우저 상태로 **남는다**. 별칭을 지운 뒤에도 그 도메인 접속이 한동안 이상하게 동작할 수 있다.

### WSL2에서 mDNS가 깨진다

`.local` 별칭을 mDNS로 브로드캐스트하는 기능이 이 도구의 매력 중 하나다. 휴대폰에서 개발 서버를 볼 수 있기 때문이다.

그런데 WSL2에서는 이것이 부분적으로만 동작한다.

README가 정확히 적는다. WSL2 환경이 기본적으로 NAT 계층 뒤에 있어 mDNS 지원이 깨진다는 것이다.
`frontend.local` 별칭을 설정했을 때 이렇게 갈린다.

| 접근 주체                         | 동작 여부 |
| --------------------------------- | --------- |
| WSL2 컨테이너 안의 프로그램       | 가능      |
| Windows 환경의 프로그램(브라우저) | 가능      |
| 네트워크의 다른 기기(휴대폰)      | **불가**  |

저자가 이것이 답답하며 기본적으로 더 잘 동작하지 않아 미안하다고 적는다.
Windows 11의 미러 모드 네트워킹 옵션이 “멀티캐스트 지원”을 주장하지만 이것으로 문제가 풀릴지는 모르겠다며, [열린 이슈 #36](https://github.com/peterldowns/localias/issues/36)에 성공한 사람이 있으면 댓글을 달아 달라고 요청한다.

### 트러스트 스토어가 플랫폼과 브라우저마다 다르다

Caddy가 루트 서명 인증서를 macOS와 Linux의 시스템 스토어에 설치한다.
브라우저가 시스템 스토어를 읽는다면 그대로 동작한다. macOS·Linux의 Safari·Edge·Chrome이 그렇다.

문제가 두 곳에서 생긴다.

**WSL**: Caddy가 인증서를 Linux VM의 트러스트 스토어에 설치하지만 부모 Windows 호스트에는 넣지 않는다.
그래서 Windows에서 도는 브라우저로 보안 별칭을 방문하면 인증서 경고가 뜬다.

```bash
# Windows 인증서 저장소에 localias 루트 인증서를 명시적으로 설치
localias debug cert --install
```

**Firefox**: Firefox는 기본적으로 시스템 인증서 저장소를 신뢰하지 않는다.

macOS·Linux에서는 설정으로 해결된다.

```text
about:config → security.enterprise_roots.enabled = true → Firefox 재시작
```

Windows의 Firefox로 WSL의 서버를 보려면 이 방법이 통하지 않으므로 수동으로 가져와야 한다.

```console
# macOS/Linux에서 인증서 경로 확인
$ localias debug cert
/Users/pd/Library/Application Support/localias/caddy/pki/authorities/local/root.crt

# WSL에서는 Windows 경로로 변환
$ wslpath -w $(localias debug cert)
\\wsl$\Ubuntu-20.04\home\pd\.local\state\localias\caddy\pki\authorities\local\root.crt
```

그다음 Firefox 설정에서 *Privacy & Security > Certificates > View Certificates > Authorities > Import*로 가져오고 **“Trust this CA to identify websites”**를 체크한다.

### Linux에서 80·443 바인딩이 막힌다

Linux에서는 기본적으로 특권 포트에 바인딩할 수 없다.

```console
$ localias run
error: loading new config: http app module: start: listening on :443: listen tcp :443: bind: permission denied
```

데몬으로 시작하면 조용히 실패하는 형태로 나타난다.

```console
$ localias start
$ localias status
daemon is not running
```

해결은 capability를 부여하는 것이다.

```bash
sudo setcap CAP_NET_BIND_SERVICE=+eip $(which localias)
```

**설치하거나 업그레이드할 때마다 다시 실행해야 한다.** 바이너리가 교체되면 capability가 사라지기 때문이다.

### 80·443을 다른 프로세스가 점유하면 시작하지 않는다

localias가 80·443을 차지해야 하므로, 다른 프록시나 웹 서버가 이미 그 포트를 쓰고 있으면 시작하지 못한다.

오류 메시지가 그 원인을 안내한다. 다른 localias 인스턴스나 다른 종류의 프록시·서버가 443·80을 듣고 있어 새 인스턴스가 시작되지 못한다는 것이다.

로컬에 nginx나 Apache나 Docker의 포트 매핑이 있으면 부딪힌다.

## 체크리스트

- 별칭 TLD가 `.test`·`.example`·`.localhost` 같은 미사용 TLD인가? 실제 도메인 이름을 쓰고 있지 않은가?
- 데몬으로 돌리고 있다면 설정을 바꾼 뒤 `localias reload`를 실행했는가?
- Linux라면 설치·업그레이드 후 `setcap`을 다시 실행했는가?
- 80·443을 점유하는 다른 프로세스가 없는가?
- 저장소의 `.localias.yaml` 변경을 코드 리뷰에서 확인하고 있는가?
- Caddy 루트 개인키가 있는 디렉터리를 공유 드라이브나 백업 대상에 두고 있지 않은가?
- Firefox를 쓴다면 `security.enterprise_roots.enabled`를 켰는가?
- WSL이라면 `localias debug cert --install`로 Windows 쪽에도 인증서를 넣었는가?

## 기억할 원칙

### 개발 도구가 시스템 전역 상태를 바꿀 때는 그 변경이 보여야 한다

localias가 hotel 대비 장점으로 내세운 것 중 가장 이전 가능한 것이 이 설계 태도다.

브라우저 프록시 설정으로 동작하면 사용자가 그 상태를 보기 어렵다.
설정 화면 어딘가에 프록시가 걸려 있고, 그것이 어떤 요청에 적용되는지 추론해야 한다.

`/etc/hosts`를 고치는 방식은 반대다. 파일 하나를 열면 현재 상태가 전부 보이고, 문제가 생기면 그 파일을 직접 고칠 수 있다.

일반화하면, 시스템 전역 상태를 바꾸는 도구는 그 상태를 **표준적이고 검사 가능한 형태**로 두어야 한다.
도구가 죽거나 사라져도 사용자가 스스로 원복할 수 있어야 하기 때문이다.

같은 기준이 인증서에도 적용된다. `localias debug cert`가 루트 인증서 경로를 출력하는 것이 그 역할을 한다.
설치된 CA가 어디서 왔는지 추적할 수 없다면 트러스트 스토어를 정리할 방법도 없다.

그리고 이 원칙에 따르는 비용이 `sudo` 프롬프트다.
표준적인 위치를 쓰면 그 위치를 보호하는 표준적인 권한 체계를 마주하게 된다.

### 로컬 개발용 이름은 실제로 존재하지 않는 이름이어야 한다

README의 HSTS 경고가 이 도구를 넘어서는 원칙이다.

로컬에서 이름을 재정의하는 모든 방법 — `/etc/hosts`, 로컬 DNS, 프록시 — 이 같은 함정을 공유한다.
실제로 존재하는 이름을 가로채면 **그 이름에 붙은 브라우저 상태가 함께 따라온다**.

쿠키가 그렇고, HSTS 정책이 그렇고, 서비스 워커 등록이 그렇고, 저장된 자격증명이 그렇다.

이것들이 도메인 단위로 저장되므로 로컬 별칭과 프로덕션이 같은 도메인을 쓰면 섞인다.
그리고 일부는 **별칭을 지운 뒤에도 남는다.** HSTS가 대표적이다.

그래서 IETF가 예약해 둔 TLD를 쓰는 것이 정답이다. `.test`와 `.example`과 `.invalid`와 `.localhost`다.
이 이름들은 공개 DNS에 등록될 수 없으므로 충돌이 원리적으로 불가능하다.

`.local`은 다른 범주다. mDNS용으로 예약되어 있어 같은 네트워크의 다른 기기에서 보이는 이점이 있지만, 그만큼 네트워크의 다른 mDNS 장치와 충돌할 수 있다.

실무 기준은 이렇다. 기기 안에서만 쓸 이름은 `.test`, 같은 네트워크의 다른 기기에서도 볼 이름은 `.local`을 쓰고, **프로덕션에서 쓰는 이름은 어떤 경우에도 쓰지 않는다**.

---

[^zallarak]: <https://news.ycombinator.com/item?id=36006895>

[^peterldowns]: <https://news.ycombinator.com/item?id=36006919>

[^jmduke]: <https://news.ycombinator.com/item?id=36007023>

[^peter_l_downs]: <https://news.ycombinator.com/item?id=36007063>
