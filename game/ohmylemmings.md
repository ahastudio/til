# ohmylemmings: DOS 레밍즈를 원본 대조로 검증하며 Rust로 옮기는 포팅

<https://github.com/edwardkim/ohmylemmings>

## 소개

ohmylemmings는 1991년 DOS 게임 레밍즈(Lemmings)의
데이터와 동작을 Rust로 재현하는 프로젝트다.
README의 제목은 Rusty Lemmings이고,
렌더링과 입출력에서 분리된 코어 엔진을 만들어
SDL2 기반 데스크톱과 WebAssembly 기반 웹에서 돌리는 것이 목표다.
저장소는 2026년 10월 18일에 만들어졌고,
이 문서를 쓴 시점에 별은 9개, 커밋은 117개,
pull request는 24개다.
저장소에는 LICENSE 파일이 없고 GitHub도 라이선스를 인식하지 못한다.

README는 진행 상황을 G00부터 번호를 붙인 목표 단위로 적는다.
G00~G09를 완료했고 G10(사운드)을 진행 중이라고 한다.
레벨 120개, 직업 8개, 음악 21곡, 효과음 18개가 검증 범위다.
다만 전체 DOS 호환성 판정은 후속 목표로 미뤄 두었다고 README가 밝힌다.

이 프로젝트에서 눈에 띄는 것은 포팅 결과보다 만드는 방식이다.
저장소는 스스로를 문서 기반 개발 방법론인 Hyper-Waterfall의 사례로 소개하고,
AI 코딩 어시스턴트가 맥락을 잃지 않게 하는 참고 프로젝트가 되기를 바란다고
기획서에 적었다.[^plan]

## 구성

코어는 `no_std` Rust 크레이트 두 개다.
`lemmings-core`는 레벨 식별 자료형, 0/1 지형 읽기와 변형, 17호출 게임 시계,
시작과 생성 스케줄, 개체 이동을 맡는다.
`lemmings-resources`는 원본 DAT 파일의 압축 해제, 레벨 레코드, 120개 카탈로그,
그래픽과 팔레트 해석을 맡는다.
두 크레이트는 외부 패키지에 의존하지 않는다.
AGENTS.md는 파싱, 시뮬레이션, 플랫폼 어댑터를 서로 분리하고
시뮬레이션이 렌더링과 입출력에 의존하지 않게 하라고 규칙으로 정한다.[^agents]

그 위에 `lemmings-session`(결정적 게임 세션)과 `lemmings-game`(자산 조립,
CPU 화면,
패널, 장면 전환)이 있고, 사운드용 `lemmings-opl`이 따로 있다.
앱은 두 개다.
`apps/desktop`은 Linux SDL2 창과 입력과 캡처·재생을 담당하고,
`apps/web`은 JS와 WASM으로 만든 브라우저 연습장이다.
Rust 버전은 `rust-toolchain.toml`이 1.93.1로 고정한다.

## 실행하기

원본 게임 파일은 저장소에 없다.
`tools/reference_assets.py fetch`가 고정된 커밋의 외부 저장소에서
파일 50개를 받아
크기와 SHA-256을 확인한 뒤 `assets/local/dos-original/`에 둔다.
이 폴더는 Git 추적에서 제외된다.
받는 곳은 Lemmix 저장소의 `orig.zip`과
VorticonCmdr/lemmings 저장소의 게임 데이터다.[^manifest]
50개는 엔진 리소스 27개와 원작 실행·참고용 23개로 나뉜다.[^assets]

```sh
# 의존 준비와 전체 검사
rustup target add wasm32-unknown-unknown
cargo fetch --locked
python3 tools/web_build.py fetch
make check

# 원본을 받아 해시로 검증한 뒤 데스크톱 화면 실행
python3 tools/reference_assets.py fetch
python3 tools/reference_assets.py verify
cargo run --release --locked --offline -p lemmings-desktop -- \
  --assets assets/local/dos-original
```

조작은 F, C, E, K, U, M, B, D 키로 직업(Floater, Climber, Bomber, Blocker,
Builder, Miner, Basher, Digger)을 고르고 레밍을 클릭하는 방식이다.
`--level 6`은 Bomber를 배우는 원본 6번 레벨을 연다.
스페이스는 일시정지, 위아래 화살표는 생성 속도, 좌우 화살표는 카메라이고,
Esc로 끝낸다.
README가 말한 데스크톱 지원은 Linux뿐이며, 나머지 플랫폼은 적혀 있지 않다.

## 검증 방식

프로젝트의 주된 특징은 구현마다 독립된 기준
구현과 원본 데이터에 대조한다는 점이다.
AGENTS.md는 시뮬레이션 상수와 동작마다 참고한 출처를 기록하라고 요구하고,
오프라인 테스트는 원본 바이너리 없이 합성 데이터로 돌아야 한다고
정한다.[^agents]

README가 기록한 대조의 예를 몇 가지 들면 이렇다.

| 대상               | 대조 내용                                                         |
| ------------------ | ----------------------------------------------------------------- |
| DAT 압축 해제      | 원본 21개 파일, 102개 구간을 해시로 대조                          |
| 초기 레벨 지형     | 120개 진입점, 30,412,800픽셀과 팔레트를 독립 Python 구현과 대조   |
| 레밍 스프라이트    | 337프레임, 63,488픽셀을 Rust, Python, TS 구현끼리 대조            |
| MAIN.DAT UI와 폰트 | 19개 묶음, 200개 이미지와 글리프의 전체 픽셀을 대조               |
| 화면               | 일곱 기준 장면의 320×160 전체 영역이 DOS 원본 세 번의 실행과 같음 |
| OPL 사운드 합성    | 독립 C 구현과 전체 샘플을 비교                                    |

기준 구현은 Lemmix(Delphi)와 Lemmings.ts(TypeScript)이고,
게임 시계는 화면 주사율과 분리한 고정 틱이다.
그래서 입력을 정수 ID로 기록하면 같은 결과를 되풀이해 재생할 수 있다.
README의 재생 예는 `54 0 AssignFloater 0`(틱 54에 0번 레밍에게 Floater 부여)과
`120 0 Nuke`다.

한계도 README가 직접 적는다.
호환성 비교 목록은 바이트와 정적 구조를 검증한 결과이고
실행 호환성의 통과 표가 아니다.
앞에서 인용한 대조는 지형, 스프라이트, 한 레벨 완주 같은 한정된 범위이며,
120개 레벨 전체를 DOS와 같은 결과로 완주한다는 주장은 아직 없다.

## 개발 방법론

Hyper-Waterfall은 모든 작업을 GitHub 이슈로 먼저 등록하고 번호와 URL을 확인한 뒤
시작하는 방식이다.
관련 문서를 읽어 맥락을 맞추고, 작은 모듈부터 TDD로 구현하고,
검증 결과와 피드백과 기술 지식을 문서에 반영한 뒤 이슈를 닫는다.
문서는 `mydocs/` 아래 `plans`, `orders`, `working`, `reports`, `feedbacks`,
`tech_insights`, `troubleshootings`로 나뉘고,
파일 이름은 `issue-<번호>_<주제>.md`다.[^agents]
`orders/`에는 서울 시간 기준의 날짜별 작업일지가 들어간다.

README는 이 방법론을 관리자가 정립한 것이라고
소개할 뿐 설명하는 문서를 따로 걸어 두지 않는다.
이 문서가 확인한 정의는 README와 AGENTS.md에 적힌 위 내용이 전부다.

## 비평

### 진행 상황 보고가 한 곳에 쌓여 읽을 수 없다

README의 현재 상태 절은 완료한 작업마다 이슈 번호와 보고서
링크를 붙인 문장을 이어 붙이는 형태다.
G07 직업 구현과 G08 승패 판정을 설명하는
같은 문장들이 다른 절에서도 한 번 더 나온다.
처음 방문한 사람은 이 프로젝트를 어떻게 실행하고
지금 무엇이 되는지 한눈에 찾기 어렵다.
문서가 많은 프로젝트가 가장 먼저 겪는 문제를 README 자체가 보여 준다.

### 완료의 기준이 자기 선언이다

README의 완료 표현은 병합, 실제 CI 통과, 종료 확인 같은 절차 이력이다.
절차를 지켰다는 사실은 해당 기능이 원작과 같다는 증거가 되지 못한다.
위의 원본 대조가 그 간격을 메우는 부분이고, 대조가 없는 직업 간 상호작용이나
레벨별 특수 규칙은 이 문서가 확인하지 못했다.

### 저장소에 라이선스가 없고 원본 데이터를 외부 미러에 기댄다

코드의 라이선스 파일이 없으면 다른 사람이 쓰고
고치고 재배포할 권리가 명시되지 않는다.
오픈소스 포팅으로 소개하는 프로젝트에서는 의외의 빈칸이다.
한편 원본 데이터는 저장소에 넣지 않고 고정된 커밋의 외부 두 저장소에서 받는다.
이렇게 하면 저작권이 있는 게임 파일을 직접 배포하지 않는 구조가 되지만,
그 두 저장소가 계속 남아 있어야 한다는 의존이 생긴다.
이 문서는 원작 게임 데이터의 권리 관계를 판단하지 않았다.

### 한 사람이 사흘 만에 쌓은 이력이라는 점을 고려해야 한다

저장소는 만든 지 사흘이 지났고 이슈는 80번대까지 갔다.
빠른 속도는 인상적이지만,
이 속도가 유지될지와 외부 기여를 받을지는 아직 알 수 없다.
AI 어시스턴트와 협업한다는 목표를 내걸었으므로,
어느 부분을 사람이 판단하고
어느 부분을 에이전트가 썼는지에 대한 기록을 README는 제공하지 않는다.

## 인사이트

### 문서가 에이전트의 장기 기억이 되려면 문서 자체를 관리해야 한다

Hyper-Waterfall의 발상은 에이전트가 대화마다 맥락을 잃으므로
맥락을 문서로 밖에 두자는 것이다.
이슈 번호로 문서 이름을 정하고,
짧은 AGENTS.md가 읽을 곳을 가리키는 구조는 합리적이다.
AGENTS.md는 3KB 남짓이고 세부는 `mydocs/`로 넘긴다.

그런데 문서가 쌓이면 문서끼리 어긋난다.
README에서 같은 문장이 두 군데 반복된 것이 그 징후다.
기억 장치로 쓰는 문서는 추가만 하면 오래된 서술과 새 서술이 충돌한다.
이 방식을 쓰려면 문서를 쓰는 규칙만큼이나 정리하고 합치는 규칙이 필요하다.
저장소에는 그런 규칙이 보이지 않는다.

### 기준 구현을 둘 이상 두면 대조 자체가 구현을 검증한다

이 프로젝트가 같은 데이터를 Rust, Python,
TypeScript로 각각 읽어 보고 결과를 비교하는 것은
에뮬레이터 개발에서 오래된 방식과 같은 구조다.
정답을 하나의 코드에 두지 않고,
서로 독립적으로 만든 구현이 같은 답을 내는지로 신뢰를 쌓는다.
결정적 틱과 입력 재생이 있어서
대조의 단위가 한 장면에서 한 판의 진행으로 넓어진다.

여기서 생기는 이차 효과가 있다.
기준 구현이 전부 같은 원본을 읽는 한,
원본 해석의 오류는 모두가 같이 틀려서 잡히지 않는다.
이를 막는 것이 DOS 실제 실행과의 화면 대조이고, 프로젝트가 그것을 한 이유다.
다만 지금은 일곱 장면뿐이어서
더 많은 레벨에서의 실행 대조가 이 방식의 가치를 가른다.

### 라이선스가 섞인 순간 배포 절차가 코드의 일부가 된다

사운드 엔진 `lemmings-opl`은 Nuked-OPL3 1.8에서
나온 LGPL-2.1 이상 코어를 정수로 옮긴 것이다.
third_party 고지는 이 엔진이 들어간 사본에 라이선스 전문,
소스, 수정과 재링크 방법을
함께 넣어야 한다고 적는다.[^third]
웹 빌드는 이를 푸터의 고지와 라이선스 텍스트,
소스와 재링크용 압축 파일, 해시 제공으로 해결했다.

이 설계가 알려 주는 것은 WebAssembly처럼 소스를 합쳐 배포하는 환경에서는
LGPL의 재링크 의무가 기능이 된다는 점이다.
그런데 저장소 전체에는 정작 라이선스가 선언되어 있지 않다.
의존하는 쪽의 의무는 정성껏 지키면서 자기 코드의 권리는 비워 두었으니,
선언하는 순간 LGPL 코어와 어떻게 조합할지도 함께 정해야 할 것이다.

---

[^agents]: GitHub, [Repository Guidelines](https://github.com/edwardkim/ohmylemmings/blob/main/AGENTS.md)

[^plan]: GitHub, [Rusty Lemmings 프로젝트 기획 및 설계서](https://github.com/edwardkim/ohmylemmings/blob/main/mydocs/plans/issue-1_rusty_lemmings.md)

[^assets]: GitHub, [원본 검증 리소스](https://github.com/edwardkim/ohmylemmings/blob/main/assets/README.md)

[^manifest]: GitHub, [dos_original.json](https://github.com/edwardkim/ohmylemmings/blob/main/assets/manifests/dos_original.json)

[^third]: GitHub, [Third-party notices](https://github.com/edwardkim/ohmylemmings/blob/main/third_party/README.md)
