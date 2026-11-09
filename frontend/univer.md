# Univer: 웹앱에 스프레드시트와 문서 편집기를 넣는 오픈소스 코어와 상용 Office SDK

<https://github.com/dream-num/univer>

HN 토론: <https://news.ycombinator.com/item?id=40171216> (178점, 53개 댓글)

GN 토론: <https://news.hada.io/topic?id=36853>

## 소개

Univer는 자신의 제품 안에 Office 편집을 넣는 Office SDK다.
README는 편집, 계산, 협업, 파일 처리를 사람과 기존 에이전트에게 제공하며
사용자의 데이터와 권한을 쓴다고 소개한다.
제품군은 스프레드시트, 문서, 프레젠테이션, 관계형 표, 캔버스, PDF에 걸친다고
한다.
2026년 11월 9일 기준 GitHub API가 보고한 저장소는 2022년 9월 29일에 만들어졌고
별 22,925개, 포크 1,926개, 열린 이슈 158개이며 Apache-2.0 라이선스, 주 언어는
TypeScript, 마지막 푸시는 같은 날이다.
이 문서는 README와 저장소 정보, 2024년 HN 스레드를 읽고 정리한 것이며 직접
설치하거나 시험하지 않았다.
기능과 성능에 대한 서술은 모두 개발사의 주장이다.

SDK는 세 부분이다.
웹 SDK는 콘텐츠 모델, 편집, 렌더링, 수식 계산, 응용 프로그램용 Facade API를
담은 토대이고, 편집기 없이 Node.js에서 쓰는 헤드리스 처리도 같은 모델과 명령,
계산을 쓴다.
서버 SDK는 실시간 협업, 편집 이력, Office 파일 가져오기와 내보내기 서비스를
더한다.
AI SDK는 Office 기능을 기존 에이전트와 워크플로에 연결해 콘텐츠 도구, 실행,
검토 통합을 제공한다.
이 저장소가 Apache-2.0으로 주는 것은 웹 SDK의 코어 아키텍처와 엔진 구현이고,
상용 웹 SDK 플러그인, 서버 SDK, 상용 AI SDK 확장은 따로 배포되고 따로 라이선스된다고
README가 구분한다.

## 구조와 기능

오픈소스 쪽의 기능은 README의 표에 이렇게 나온다.
스프레드시트의 편집과 레이아웃(셀 서식, 병합, 셀 안 서식 있는 텍스트, 창 고정, 떠
있는 이미지, 실행 취소와 다시 실행), 데이터와 계산(수식, 이름 정의, 필터, 정렬,
데이터 검증, 조건부 서식, 하이퍼링크, 댓글, 찾아 바꾸기), 문서의 서식 있는 텍스트
편집(단락 서식, 목록, 하이퍼링크, 댓글, 그림 통합)이다.
기능은 플러그인과 프리셋(preset)으로 조합하고 빠른 시작은 Sheets Core 프리셋만
쓴다.

README의 빠른 시작은 번들러를 쓰는 브라우저 앱에서 다음처럼 한다.

```bash
pnpm add @univerjs/presets @univerjs/preset-sheets-core
```

```ts
import { UniverSheetsCorePreset } from '@univerjs/preset-sheets-core'
import UniverPresetSheetsCoreEnUS from '@univerjs/preset-sheets-core/locales/en-US'
import { createUniver, LocaleType, mergeLocales } from '@univerjs/presets'
import '@univerjs/preset-sheets-core/lib/index.css'

const { univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  locales: {
    [LocaleType.EN_US]: mergeLocales(UniverPresetSheetsCoreEnUS),
  },
  presets: [UniverSheetsCorePreset({ container: 'app' })],
})
univerAPI.createWorkbook({})
```

이 예제는 오픈소스 패키지만 쓰며 상용 라이선스나 서버 SDK가 필요 없다고 한다.
컴포넌트 프레임워크에서는 `createUniver`가 돌려준 인스턴스를 기억했다가 컴포넌트가
사라질 때 `univer.dispose()`를 호출하라고 안내한다.
조정된 `@univerjs/*` 패키지는 같은 버전으로 맞추라는 주의도 있다.

내부 설계에서 README가 강조하는 것은 세 가지다.
기능마다 자기 변경과 실행 취소 데이터를 제공하고 명령이 그 실행과 이력을 합쳐서,
필터 범위 안에 행을 넣을 때 기본 콘텐츠와 필터 범위가 함께 바뀌고 한 번의
취소로 둘이 같이 되돌려지게 한다.
명령(Command)이 편집을 조율하고 변이(Mutation)가 콘텐츠 변화를 기술하며, 협업은
변이를 변경 집합(changeset)으로 묶어 동시 편집에 운영 변환(OT)을 적용한다.
Facade API는 `FWorkbook`, `FWorksheet`, `FRange` 같은 응용 객체로 하위 기능을
감싸고, 플러그인이 자기 Facade 확장과 타입이 있는 이벤트를 `univerAPI.Event`와
`univerAPI.Enum`으로 내놓는다.

## 오픈소스와 상용의 경계

README는 경계를 표로 보인다.
이 저장소는 Apache-2.0로 상용 애플리케이션에도 쓸 수 있는 웹 SDK 코어(콘텐츠
모델, 엔진, 플러그인, UI 토대, 시트와 문서 기능, 헤드리스 콘텐츠 작업)다.
상용 웹 SDK 플러그인은 차트, 도형, 피벗 테이블, SmartArt 같은 기능을 더한다.
서버 SDK는 실시간 협업과 개정 이력, Office 파일 변환을 더하며 응용 프로그램의
신원과 권한과 저장소에 연결된다.
AI SDK 확장은 에이전트가 콘텐츠를 검사하고 고치고 확인하도록 Node.js API와 CLI
부품을 주며 협업과 Worktree 검토 통합을 포함한다.
무료 평가판에는 워터마크와 기능 제한이 있다고 한다.
XLSX, DOCX, PPTX 같은 OOXML 파일의 가져오기와 내보내기는 서버 SDK의 변환 기능이며,
슬라이드와 캔버스(Boards)도 현재는 따로 배포되는 상용 제품이라고 README가 밝힌다.
README의 데모는 기본 오픈소스 설정보다 많은 것을 보이며 상용 기능을 포함한다고
스스로 알린다.

## 비평

### 오픈소스 코어와 상용 기능의 경계가 사용 가능성을 좌우한다

README가 오픈소스에 두는 것은 시트와 문서의 편집 코어이고, 협업, 파일 변환,
차트, 피벗 테이블, 슬라이드는 상용이다.
HN의 2024년 스레드에서 사람들이 가장 먼저 짚은 것이 이 경계였다.
zipping1549는 시트 협업이 Pro 기능이라는 사실을 짧게 꼬집었고,[^zipping1549]
m4thfr34k는 시트의 가져오기와 내보내기가 Pro 기능이면 Pro 기능 없이 누가 쓰겠느냐고
물었다.[^m4thfr34k]
williamstein은 실시간 협업이 상용 엔터프라이즈 판의 기능이라고 문서를 인용해
확인했다.[^williamstein]
지금 README는 이 경계를 먼저 표로 밝히고 오픈소스 전용 필터가 있는 비교표로
안내하므로 투명성은 높아졌다.
그러나 파일 형식 호환과 협업이 상용이라는 구조는 그대로여서, 이 저장소만으로
Google Sheets나 Microsoft Excel의 대안이 된다고 보기는 어렵다.

### 데모가 오픈소스 기능의 증거가 아니다

README는 데모가 오픈소스 기본 설정보다 많은 것을 보이며 상용 기능을 포함한다고
스스로 적는다.
따라서 첫 화면의 이미지와 데모 링크는 오픈소스 코어가 무엇을 하는지가 아니라 전체
SDK가 무엇을 하는지를 보여 준다.
오픈소스만으로 가능한 범위는 기능 표와 빠른 시작이 정하고, 그것을 넘는 기능이
필요한 사람은 상용 계약을 알아봐야 한다.

### 품질의 증거가 개발사의 서술에 머문다

2024년 스레드에서 StarlaAtNight는 iPhone Firefox에서 대용량 예제의 셀을 100만 행
근처까지 끌면 충돌한다고 보고했고,[^StarlaAtNight]
js4ever는 첫 예제의 데이터 검증에서 날짜 칸에 글자를 입력하면 페이지 전체가
멈추며 유료 제품인데 이렇다고 썼다.[^js4ever]
이는 2년 반 전 시점의 개별 보고이고 지금도 재현되는지는 이 문서가 확인하지
못했다.
README에도 성능 수치나 호환성 시험 결과가 없고, 열린 이슈 158개가 어떤 상태인지는
이 문서가 읽지 않았다.

### AI 기능의 주장이 구체적 시험으로 뒷받침되지 않는다

README는 이 SDK로 AI 에이전트가 콘텐츠를 검사하고 편집하고 렌더링 결과를 확인하며
Worktree에서 초안을 고쳐 사람이 검토하게 한다고 설명한다.
설계는 구체적이지만 에이전트가 실제 문서 작업에서 얼마나 잘하는지에 대한 평가는
없다.
이는 이 분야의 제품 설명 대부분에 공통되는 한계이고 이 문서는 AI SDK를 시험하지
못했다.

## 도입 전에 따져볼 것

- 필요한 기능이 오픈소스 표에 있는지 먼저 확인한다. XLSX 가져오기와 내보내기, 실시간 협업, 차트, 피벗 테이블은 상용이다.
- 비교표의 오픈소스 전용 필터로 기능을 확인하고, 데모에서 본 기능이 오픈소스에 있는지 따로 확인한다.
- 상용 범위가 필요하면 무료 평가판의 워터마크와 제한을 먼저 시험하고 요금과 라이선스를 문의한다.
- Office 문서와의 호환이 업무 요건이면 실제 파일로 가져오기와 내보내기를 시험한다. HN 스레드에서 Dalewyn은 오픈소스 여부보다 업계 표준 파일과의 호환이 우선이라고 했다.[^Dalewyn]
- 브라우저에서 큰 시트를 다룬다면 모바일을 포함해 대용량 데이터의 동작을 직접 시험한다.
- `@univerjs/*` 패키지 버전을 맞추고 API 안정성 정책을 확인한 뒤 확장 지점에 의존한다.
- 소스를 읽고 싶다면 필터 구현 해설이 README가 추천하는 시작점이다.

---

[^zipping1549]: <https://news.ycombinator.com/item?id=40175384>

[^m4thfr34k]: <https://news.ycombinator.com/item?id=40175538>

[^williamstein]: <https://news.ycombinator.com/item?id=40175618>

[^StarlaAtNight]: <https://news.ycombinator.com/item?id=40176475>

[^js4ever]: <https://news.ycombinator.com/item?id=40177724>

[^Dalewyn]: <https://news.ycombinator.com/item?id=40177345>
