# pdfcn: React 컴포넌트로 PDF를 조립하는 shadcn 레지스트리

<https://pdfcn.dev/>

<https://github.com/shadcn-labs/pdfcn>

HN 토론: <https://news.ycombinator.com/item?id=49771732> (6점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=34090>

## 소개

PDF 문서를 React 컴포넌트로 조립하도록 만든 shadcn 레지스트리다.
같은 조직의 `termcn`과 마찬가지로 npm 패키지를 설치해 의존하는 방식이 아니라,
`shadcn` CLI로 소스를 프로젝트에 복사해 넣고 그 코드를 직접 소유하는 방식을 따른다.
2026년 8월 11일에 만들어졌고 MIT 라이선스이며 TypeScript로 쓰여 있다.

이 프로젝트가 약속하는 것과 약속하지 않는 것을 먼저 구분해 두는 편이 낫다.
약속하는 것은 렌더러 위에 올라가는 컴포넌트 계층이다.
표, 폼, 그래프, 페이지 머리말과 꼬리말, 서명란, 워터마크 같은 문서 부품과
청구서와 보고서 같은 완성된 문서 골격을 복사해 갈 수 있는 형태로 제공한다.
약속하지 않는 것은 렌더링 자체다.
PDF를 실제로 만들어 내는 일은 Takumi 또는 Forme가 하고, `pdfcn`은 그 위에서 같은 모양의 API를 제공한다.

그래서 이것은 라이브러리가 아니라 레지스트리다.
버전을 올려 받을 상류가 없고, 설치한 시점의 코드가 프로젝트의 코드가 된다.
이 성질이 장점과 단점을 동시에 만드는데, 그 값은 아래 트레이드오프 절에서 따로 다룬다.

## 레지스트리 구성

`registry.json`에 79개 항목이 들어 있고 네 종류로 나뉜다.

| 종류    | 개수 | 내용                                       |
| ------- | ---- | ------------------------------------------ |
| `ui`    | 48   | 문서 부품 24종을 두 렌더러용으로 각각 제공 |
| `block` | 20   | 완성 문서 10종을 두 렌더러용으로 각각 제공 |
| `theme` | 9    | 테마 토큰 프리셋                           |
| `lib`   | 2    | 각 렌더러의 테마 컨텍스트와 프리미티브     |

`ui` 24종은 역할별로 이렇게 나뉜다.

| 역할        | 컴포넌트                                                              |
| ----------- | --------------------------------------------------------------------- |
| 텍스트      | `Text`, `Heading`, `Link`, `List`                                     |
| 데이터      | `Table`, `DataTable`, `KeyValue`, `Graph`, `Form`                     |
| 구획        | `Section`, `Stack`, `Card`, `Divider`, `Alert`, `Badge`               |
| 페이지 제어 | `PageBreak`, `PageHeader`, `PageFooter`, `PageNumber`, `KeepTogether` |
| 삽입물      | `PdfImage`, `Qrcode`, `Signature`, `Watermark`                        |

`block` 10종은 청구서 6종(`classic`, `consultant`, `corporate`, `creative`, `minimal`, `modern`)과
보고서 4종(`financial`, `marketing`, `operations`, `security`)이다.

`ui`와 `block`은 `takumi/`와 `forme/`로 이름 공간이 갈리지만, 테마 9종은 갈리지 않는다.
`theme-professional`부터 `theme-blueprint`까지 이름에 베이스 접두어가 없다.
테마가 순수한 토큰 묶음이고 렌더러에 의존하지 않기 때문인데, 이 비대칭이 설치 명령에서 문제를 만든다.
함정 절에서 다시 다룬다.

## 설치하기

레지스트리 이름 공간을 `components.json`에 한 번 등록한다.

```json
{
  "registries": {
    "@pdfcn": "https://pdfcn.dev/r/{name}.json"
  }
}
```

그다음 이름으로 받아 온다.
베이스에 따라 이름 공간이 갈린다.

```bash
# Takumi 베이스
npx shadcn@latest add @pdfcn/takumi/text
npx shadcn@latest add @pdfcn/takumi/invoice-minimal

# Forme 베이스
npx shadcn@latest add @pdfcn/forme/text
npx shadcn@latest add @pdfcn/forme/invoice-minimal
```

이름 공간을 등록하지 않았다면 전체 URL을 그대로 쓸 수 있다.

```bash
npx shadcn@latest add https://pdfcn.dev/r/takumi/text.json
```

받아 온 컴포넌트는 렌더러의 문서 프리미티브 안에서 쓴다.
테마는 `PdfcnThemeProvider`로 주입한다.

```tsx
import { Document, Page } from "@/components/pdf/pdf-primitives";
import { PdfcnThemeProvider } from "@/components/pdf/theme-provider";
import { Text } from "@/components/pdf/text";

export function Invoice() {
  return (
    <Document>
      <Page size="A4">
        <PdfcnThemeProvider>
          <Text variant="xl">Invoice</Text>
        </PdfcnThemeProvider>
      </Page>
    </Document>
  );
}
```

Forme를 쓸 때는 `Document`와 `Page`를 `@formepdf/react`에서 가져오며,
설치된 `pdfcn` 컴포넌트의 API는 그대로다.
이것이 이 프로젝트의 핵심 주장이고, 어떻게 성립하는지가 다음 절이다.

렌더러 의존성은 레지스트리가 알아서 넣는다.
Takumi 항목은 `takumi-pdf`와 `@takumi-rs/helpers`를,
Forme 항목은 `@formepdf/react`와 `@formepdf/core`를 선언한다.
컴포넌트끼리의 의존도 선언되어 있어서,
예컨대 `takumi/data-table`을 받으면 `takumi/utils`와 `takumi/table`이 함께 따라온다.

## 두 렌더러가 같은 API를 갖는 방식

이 프로젝트에서 실제로 배울 것이 있는 부분이다.
공개 API를 같게 유지하면서 구현을 두 벌 두는데, 그 경계를 어디에 두었는지가 명확하다.

`KeepTogether`를 두 베이스에서 나란히 놓으면 구조가 바로 보인다.
Takumi 쪽은 이렇다.

```tsx
export const KeepTogether = ({ children, style }: KeepTogetherProps) => (
  <View style={[{ breakInside: "avoid" }, style].filter(Boolean) as never}>
    {children}
  </View>
);
```

Forme 쪽은 이렇다.

```tsx
export const KeepTogether = ({ children, style }: KeepTogetherProps) => (
  <View wrap={false} style={style as never}>
    {children}
  </View>
);
```

공개 props는 글자 하나까지 같고, 달라지는 것은 한 줄이다.
Takumi는 브라우저 CSS 의미론을 따르므로 `breakInside: "avoid"`라는 스타일 속성으로 표현하고,
Forme는 `react-pdf` 계열의 관례를 따르므로 `wrap={false}`라는 props로 표현한다.
같은 의도를 두 렌더러의 모국어로 각각 옮겨 놓은 것이며, 컴포넌트 이름과 props가 그 사이의 공용어가 된다.

더 흥미로운 것은 단위 처리다.
Takumi 베이스의 `pdf-primitives.tsx`에 이런 주석과 상수가 있다.

```ts
/**
 * pdfcn's shared component tokens follow the PDF convention of using points.
 * Takumi follows browser CSS instead, where numeric lengths are pixels at
 * 96 DPI. Converting at the primitive boundary keeps the public component API
 * and the generated document's physical measurements aligned with Forme.
 */
export const PDF_POINT_TO_CSS_PIXEL = 96 / 72;

export const pointToCssPixel = (value: number): number =>
  value * PDF_POINT_TO_CSS_PIXEL;
```

`pdfcn`의 공유 토큰은 PDF의 관례대로 포인트를 쓰는데, Takumi는 96 DPI 픽셀로 숫자를 읽는다.
그래서 프리미티브 경계에서 한 번 변환한다.
변환 대상이 되는 속성 이름 목록을 집합으로 따로 두고 그 속성에만 적용하는 방식이다.
`fontSize`나 `margin`처럼 길이인 속성은 변환하고, `opacity`나 `flexGrow`처럼 무차원인 속성은 건드리지 않는다.

이 선택이 중요한 이유는 변환 지점이 하나라는 것이다.
컴포넌트마다 단위를 맞추면 스물네 곳에서 실수할 수 있고, 테마 토큰 쪽에서 맞추면 테마가 렌더러에 묶인다.
프리미티브 경계에 두면 위쪽 전부가 포인트 세계에 살고 아래쪽 하나만 픽셀 세계를 안다.
두 렌더러를 지원하는 코드를 쓸 때 어디를 접경으로 삼을지에 대한 좋은 예다.

같은 경계에서 스타일 병합 방식의 차이도 흡수된다.
Takumi 쪽은 스타일 배열을 그대로 넘길 수 있고, Forme 쪽은 단일 객체만 받으므로
`mergeFormeStyles`가 중첩 배열을 재귀로 평탄화해 하나의 객체로 합친다.
공개 API에서는 양쪽 모두 배열을 받는 것처럼 보이고, 차이는 프리미티브 아래에 남는다.

## 테마 토큰 정하기

테마는 원시 토큰과 의미 토큰의 두 층으로 나뉜다.
`primitives.ts`가 모든 프리셋이 공유하는 척도를 정의하고, 각 테마가 그 척도에서 골라 의미 토큰에 배정한다.

| 척도         | 값                                    |
| ------------ | ------------------------------------- |
| 타이포그래피 | Major Third 비율 1.25, 기준 12pt      |
| 간격         | 4pt 그리드                            |
| 글꼴 두께    | 400, 500, 600, 700                    |
| 행간         | 1.2, 1.4, 1.6                         |
| 모서리       | 0, 2, 4, 8pt, 그리고 알약 모양용 9999 |
| 자간         | -0.025, 0, 0.025, 0.05                |

의미 토큰은 shadcn 계열과 같은 이름을 쓴다.
`minimal` 테마를 예로 보면 색은 `foreground`, `background`, `muted`, `mutedForeground`,
`primary`, `primaryForeground`, `accent`, `border`와 상태색 넷(`destructive`, `success`, `warning`, `info`)이다.
웹 쪽 shadcn 테마를 써 본 사람이 그대로 옮겨 올 수 있는 이름이며, 이것이 이 프로젝트가 노리는 친숙함의 실체다.

테마에는 색뿐 아니라 문서 수준의 값도 들어 있다.
`page`가 크기와 방향을 정하고(`A4`, `portrait`), `spacing`이 페이지 여백과 컴포넌트 사이 간격을 정한다.
따라서 A4가 아닌 문서를 만들려면 컴포넌트가 아니라 테마를 고쳐야 한다.

값을 고를 때의 기준은 이렇다.

| 결정할 것      | 무엇에 따라 정하는가                                                         |
| -------------- | ---------------------------------------------------------------------------- |
| 기준 글자 크기 | 인쇄 대상이면 10~12pt, 화면 열람 위주면 12pt 이상                            |
| 간격 그리드    | 4pt를 유지하되 표가 많은 문서는 세로 밀도를 위해 컴포넌트 간격만 줄인다      |
| 페이지 여백    | 제본 여부. 제본하면 안쪽 여백을 별도로 키워야 하는데 토큰에는 그 개념이 없다 |
| 상태색         | 흑백 인쇄 가능성. 색으로만 구분하면 인쇄본에서 정보가 사라진다               |

## 함정

문서만 읽어서는 드러나지 않는 것들이다.

`minPresenceAhead`는 선언되어 있지만 아무 일도 하지 않는다.
`KeepTogether`의 props 인터페이스에 `minPresenceAhead?: number`가 있고
문서의 API 표에도 올라가 있는데, Takumi 구현과 Forme 구현 어느 쪽도 이 값을 쓰지 않는다.
두 구현 모두 `children`과 `style`만 꺼내 쓰고 나머지는 버린다.
페이지 하단에 최소 얼마의 공간이 남아 있어야 블록을 시작하게 하는 값이므로
긴 표를 다룰 때 가장 먼저 손이 가는 props인데, 넘겨도 조용히 무시된다.
타입 검사도 통과하고 경고도 없으므로 출력물을 눈으로 보기 전까지 알 수 없다.

설치 경로에 대한 문서 설명이 실제 설정과 어긋난다.
레지스트리 문서는 컴포넌트가 `components/ui/`로 들어간다고 적고 있지만,
`registry.json`의 각 파일에 지정된 대상 경로는 `components/pdf/...`이고
설치 문서의 사용 예제도 `@/components/pdf/text`에서 가져온다.
문서 한 줄만 보고 경로를 가정하면 가져오기 경로가 맞지 않는다.

테마 설치 명령도 문서와 레지스트리가 어긋난다.
설치 문서는 Takumi용으로 `@pdfcn/takumi/theme-minimal`을, Forme용으로 `@pdfcn/theme-minimal`을 제시한다.
그런데 `registry.json`의 테마 항목 이름에는 베이스 접두어가 없다.
`theme-professional`, `theme-modern`, `theme-minimal` 같은 형태다.
베이스 접두어를 붙인 쪽은 존재하지 않는 이름일 가능성이 높으므로, 접두어 없는 형태를 먼저 시도하는 편이 낫다.

직접 복사하는 경로의 비용이 생각보다 크다.
`KeepTogether`는 본체가 열다섯 줄 남짓인데, 문서의 수동 설치 절차는 아홉 개 파일을 옮기라고 안내한다.
컴포넌트 본체, 테마 제공자, 색 해석기, 프리미티브, SVG 처리, 테마 프리셋, 원시 토큰, 그리고 타입 정의 둘이다.
CLI를 쓰면 이 과정이 한 줄로 끝나지만, 수동으로 옮긴다면 가져오기 경로를 아홉 번 고쳐야 한다.

복사해 넣은 코드에는 상류 수정이 오지 않는다.
shadcn 방식의 일반적인 대가이지만 이 영역에서는 더 날카롭다.
PDF 컴포넌트에서 버그가 생기는 곳은 대체로 페이지 나눔과 표 분할이고,
그 코드는 렌더러의 판본이 올라갈 때 함께 손봐야 하는 부분이기 때문이다.
받아 온 시점을 기록해 두고 상류 커밋을 주기적으로 훑는 절차를 따로 만들어 두는 편이 낫다.

## 트레이드오프

### 두 렌더러를 지원하는 대가는 가장 약한 쪽에 맞춘 API다

같은 컴포넌트 이름과 같은 props로 두 렌더러를 쓸 수 있다는 것이 이 프로젝트의 중심 주장이다.
얻는 것은 분명하다.
렌더러를 바꿀 때 문서 코드를 다시 쓰지 않아도 되고, 팀이 배울 개념이 한 벌이면 된다.
Takumi와 Forme의 문서를 각각 읽는 대신 `pdfcn`의 컴포넌트 목록만 알면 된다.

내주는 것은 두 렌더러 중 한쪽에만 있는 기능이다.
`minPresenceAhead`가 그 증거다.
이 개념은 `react-pdf` 계열에 있는 것이고 CSS의 `break-inside`에는 대응물이 없다.
공통 API를 만들려다 보니 props에는 남았고 구현에서는 사라졌다.
이것이 명시적으로 처리되었다면, 즉 지원하지 않는 베이스에서 경고를 내거나 타입에서 제외했다면 문제가 아니다.
조용히 무시되는 형태가 문제인 이유는, 사용자가 그 기능이 동작한다고 믿은 채로 진행하기 때문이다.

이 비용은 컴포넌트가 늘어날수록 커진다.
지금은 24종이고 대부분 두 렌더러에 자연스럽게 대응하는 기본 부품이다.
글꼴 하위 집합 추출, 서식 있는 필드, 접근성 태그, 문서 암호화처럼 렌더러별 차이가 큰 영역으로 들어가면
공통 API는 최소 공배수가 아니라 최소 공약수 쪽으로 수렴한다.
두 베이스를 유지하는 선택은 그 지점에서 다시 검토되어야 한다.

### 복사 소유는 갱신을 포기하는 대신 수정 권한을 산다

레지스트리 방식은 의존성이 아니라 코드를 준다.
얻는 것은 완전한 수정 권한이다.
표의 열 폭 계산이 우리 문서에 맞지 않으면 그 파일을 열어 고치면 되고, 상류에 이슈를 올려 기다릴 필요가 없다.
PDF처럼 요구가 조직마다 제각각인 영역에서 이 자유는 실질적이다.

내주는 것은 상류의 수정이다.
그리고 여기서 흔히 놓치는 점은, 포기하는 것이 기능 추가가 아니라 버그 수정이라는 것이다.
새 컴포넌트는 받아 오면 되지만, 이미 복사한 `Table`의 페이지 나눔 버그가 상류에서 고쳐져도
내 프로젝트의 `Table`은 그대로다.
둘 다 가질 수는 없다.
차선은 복사한 파일을 별도 디렉터리에 모아 두고 상류와의 차이를 추적하는 것인데,
그러면 사실상 포크를 관리하는 것이 되어 복사 방식이 피하려던 부담이 되돌아온다.

현실적인 기준은 수정 여부다.
손대지 않은 컴포넌트는 상류와 주기적으로 맞춰 볼 가치가 있고, 손댄 컴포넌트는 그 순간부터 우리 코드다.
그 구분을 커밋으로 남겨 두면 나중에 무엇을 확인해야 하는지 알 수 있다.

## 비평

### 프리미티브 경계는 잘 잡혔는데 그 경계의 계약이 문서화되어 있지 않다

이 프로젝트에서 가장 잘 설계된 부분은 단위 변환과 스타일 병합을 프리미티브 경계 한 곳에 모은 것이다.
위쪽은 포인트와 배열 스타일이라는 하나의 세계에 살고, 아래쪽이 각 렌더러의 관례로 번역한다.
경계가 하나라는 사실이 이 구조의 값어치이고, 그것을 코드 주석이 정확히 설명하고 있다.

문제는 그 설명이 소스 주석에만 있다는 것이다.
공개 문서 어디에도 공유 토큰이 포인트 단위라는 말이 없다.
그래서 Takumi 베이스를 쓰는 사람이 `style={{ fontSize: 16 }}`을 직접 넘길 때
그것이 16pt로 해석되어 약 21px로 변환된다는 사실을 알 방법이 문서에 없다.
컴포넌트가 제공하는 `variant` 안에 머무는 동안에는 드러나지 않다가,
렌더러의 원시 API로 내려가 직접 제어할 때 어긋나기 시작한다.
그런데 필요하면 원시 API로 내려가라는 것이 이 프로젝트가 내세우는 설계 원칙 중 하나다.
내려가라고 권하면서 내려간 곳의 단위 규칙은 말하지 않는 셈이다.

같은 문제가 무차원 속성 목록에도 있다.
어떤 속성이 변환 대상이고 어떤 속성이 아닌지는 소스의 집합 정의를 읽어야 알 수 있다.
그 목록에 빠진 속성을 쓰면 변환 없이 통과하므로, 길이인데 목록에 없는 속성이 하나라도 있으면 조용히 어긋난다.
이런 종류의 경계는 목록이 아니라 문서화된 규칙으로 표현되어야 사용자가 검증할 수 있다.

`minPresenceAhead`도 결국 같은 결함의 다른 얼굴이다.
경계의 계약이 적혀 있지 않으면, 무엇이 지켜지고 무엇이 무시되는지를 사용자가 알 수 없다.
컴포넌트를 스물네 개 더 늘리는 것보다 이 계약을 한 쪽 분량으로 적는 편이 이 프로젝트를 더 쓸 만하게 만든다.

## 기억할 원칙

### 서로 다른 두 백엔드를 같은 API로 감쌀 때는 변환 지점을 하나로 만들고 그 계약을 적어 둔다

`pdfcn`이 잘한 것과 빠뜨린 것이 같은 자리에 있다.
단위와 스타일 표현의 차이를 프리미티브 한 층에 모은 것은 옳았다.
변환이 여러 곳에 흩어지면 어긋남을 재현하기 어렵고, 너무 위에서 변환하면 추상이 백엔드에 묶인다.

그런데 경계를 만드는 것만으로는 부족하다.
경계를 넘는 값이 어떤 단위이고 어떤 속성이 변환 대상이며 무엇이 지원되지 않는지를
사용자가 읽을 수 있는 곳에 적어야 추상이 완성된다.
적히지 않은 계약은 소스를 읽는 사람에게만 존재하고, 소스를 읽어야 한다면 추상의 값어치는 절반이다.

### 지원하지 않는 옵션은 조용히 무시하는 대신 눈에 보이게 실패시킨다

공통 API가 한쪽 백엔드에만 있는 기능을 담게 되는 것은 흔한 일이고 그 자체는 결함이 아니다.
결함은 그 옵션을 받아들이고 아무 일도 하지 않는 것이다.
타입이 통과하고 경고가 없으면 사용자는 그것이 동작한다고 믿으며,
틀렸다는 사실은 출력물을 눈으로 확인할 때에야 드러난다.

선택지는 셋이다.
지원하지 않는 베이스의 타입에서 그 props를 빼거나,
개발 모드에서 경고를 내거나, 최소한 문서의 API 표에 지원되지 않는다고 표시하는 것이다.
셋 중 어느 것도 하지 않으면, 공통 API가 주는 이식성이 그 이식성을 믿은 대가로 상쇄된다.
