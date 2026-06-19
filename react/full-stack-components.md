# 풀스택 컴포넌트

<https://www.epicweb.dev/full-stack-components>

## 소개

Kent C. Dodds는 2024년 7월에 "풀스택 컴포넌트(Full Stack Components)"라는 패턴을 소개한다.
이 패턴의 핵심은 UI 컴포넌트 코드와 그 컴포넌트가 필요로 하는 백엔드 코드를 하나의 파일에 함께 배치하는 것이다.
저자는 Remix 프레임워크의 Resource Routes를 활용해 서버 측 로직(`loader`, `action`)과 클라이언트 측 React 컴포넌트를 같은 파일에 정의할 수 있음을 보여준다.

전통적으로 Twitter의 좋아요 버튼 같은 인터랙티브 컴포넌트를 만들려면 수 개의 파일이 필요했다.
프런트엔드와 백엔드가 별도 저장소에 있는 경우도 있고, 언어 자체가 다른 경우도 있다.
클릭 이벤트 핸들러, 비동기 요청, 에러 상태, 낙관적 UI, 경쟁 조건(race condition) 처리까지 각각 별도 코드가 필요하다.

## 배경: Remix의 풀스택 라우트

Remix는 이미 페이지 단위에서 서버와 클라이언트 코드를 한 파일에 배치할 수 있다.
`loader`는 페이지 진입 시 서버에서 데이터를 가져오고, `action`은 폼 제출을 처리하며, `default export`가 UI를 렌더링한다.

```tsx
export async function loader({ request }: LoaderFunctionArgs) {
  const projects = await getProjects()
  return json({ projects })
}

export async function action({ request }: ActionFunctionArgs) {
  const form = await request.formData()
  const newProject = await createProject({ title: form.get('title') })
  return redirect(`/projects/${newProject.id}`)
}

export default function Projects() {
  const { projects } = useLoaderData<typeof loader>()
  const { state } = useTransition()
  const busy = state === 'submitting'
  return (
    <div>
      {projects.map(project => (
        <Link to={project.slug}>{project.title}</Link>
      ))}
      <Form method="post">
        <input name="title" />
        <button type="submit" disabled={busy}>
          {busy ? 'Creating...' : 'Create New Project'}
        </button>
      </Form>
    </div>
  )
}
```

풀스택 컴포넌트는 이 개념을 페이지 전체가 아닌 개별 컴포넌트 단위로 내려온 것이다.
"Remix allows me to colocate my UI and backend code for more than just full page routes, but also individual components."

## 구현: CustomerCombobox

저자는 고객 검색 콤보박스(`CustomerCombobox`)를 실제 예제로 제시한다.
입력창에 텍스트를 타이핑하면 서버에서 고객 목록을 검색해 드롭다운으로 보여주는 컴포넌트다.

### 1단계: Resource Route 생성

`app/routes/resources/customers.tsx`에 서버 전용 엔드포인트를 만든다.

```tsx
// app/routes/resources/customers.tsx
import { json } from '@remix-run/node'

export async function loader() {
  return json({ hello: 'world' })
}
```

이 파일에는 `default export`가 없다.
Remix는 `default export`가 없는 라우트를 Resource Route로 인식하고, 페이지 없이 API 엔드포인트처럼 동작시킨다.

### 2단계: 서버 로직 완성

```tsx
import type { LoaderFunctionArgs } from '@remix-run/node'
import { json } from '@remix-run/node'
import invariant from 'tiny-invariant'
import { searchCustomers } from '~/models/customer.server'
import { requireUser } from '~/session.server'

export async function loader({ request }: LoaderFunctionArgs) {
  await requireUser(request)
  const url = new URL(request.url)
  const query = url.searchParams.get('query')
  invariant(typeof query === 'string', 'query is required')
  return json({
    customers: await searchCustomers(query),
  })
}
```

`requireUser`로 인증을 확인하고, 쿼리 파라미터를 검증한 뒤, 데이터베이스에서 고객을 검색한다.
서버에서만 실행되는 코드이므로 데이터베이스 접근, 세션 검증 등을 자유롭게 쓸 수 있다.

### 3단계: UI 컴포넌트 추가

같은 파일에 React 컴포넌트를 `export function`으로 추가한다.
이 함수는 `default export`가 아니므로 Remix는 여전히 이 파일을 Resource Route로 취급한다.

```tsx
export function CustomerCombobox({ error }: { error?: string | null }) {
  const customerFetcher = useFetcher<typeof loader>()
  const id = useId()
  const customers = customerFetcher.data?.customers ?? []
  type Customer = typeof customers[number]
  const [selectedCustomer, setSelectedCustomer] = useState<
    null | undefined | Customer
  >(null)
  const cb = useCombobox<Customer>({
    id,
    onSelectedItemChange: ({ selectedItem }) => {
      setSelectedCustomer(selectedItem)
    },
    items: customers,
    itemToString: item => (item ? item.name : ''),
    onInputValueChange: changes => {
      customerFetcher.submit(
        { query: changes.inputValue ?? '' },
        { method: 'get', action: '/resources/customers' },
      )
    },
  })
  // ...
}
```

`useFetcher<typeof loader>()`로 선언하면 TypeScript 타입이 서버의 `loader` 함수 반환값에서 자동으로 추론된다.
`customerFetcher.data?.customers`의 타입이 `searchCustomers`의 반환 타입과 일치한다.
별도의 타입 정의나 타입 단언(type assertion)이 필요 없다.

### 4단계: 로딩 스피너

```tsx
const busy = customerFetcher.state !== 'idle'
const showSpinner = useSpinDelay(busy, {
  delay: 150,
  minDuration: 500,
})
```

`spin-delay`는 네트워크 응답이 150ms 이내로 빠른 경우 스피너를 아예 표시하지 않는다.
스피너가 나타났다면 최소 500ms는 유지한다.
"깜빡임(flicker)"을 방지해 시스템이 불안정하다는 인상을 주지 않는다.

```tsx
function Spinner({ showSpinner }: { showSpinner: boolean }) {
  return (
    <div
      className={`absolute right-0 top-[6px] transition-opacity ${
        showSpinner ? 'opacity-100' : 'opacity-0'
      }`}
    >
      <svg
        className="-ml-1 mr-3 h-5 w-5 animate-spin"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        width="1em"
        height="1em"
      >
        <circle
          className="opacity-25"
          cx={12}
          cy={12}
          r={10}
          stroke="currentColor"
          strokeWidth={4}
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>
  )
}
```

### 완성된 컴포넌트 전체 코드

```tsx
import type { LoaderFunctionArgs } from '@remix-run/node'
import { json } from '@remix-run/node'
import { useFetcher } from '@remix-run/react'
import clsx from 'clsx'
import { useCombobox } from 'downshift'
import { useId, useState } from 'react'
import { useSpinDelay } from 'spin-delay'
import invariant from 'tiny-invariant'
import { LabelText } from '~/components'
import { searchCustomers } from '~/models/customer.server'
import { requireUser } from '~/session.server'

export async function loader({ request }: LoaderFunctionArgs) {
  await requireUser(request)
  const url = new URL(request.url)
  const query = url.searchParams.get('query')
  invariant(typeof query === 'string', 'query is required')
  return json({
    customers: await searchCustomers(query),
  })
}

export function CustomerCombobox({ error }: { error?: string | null }) {
  const customerFetcher = useFetcher<typeof loader>()
  const id = useId()
  const customers = customerFetcher.data?.customers ?? []
  type Customer = typeof customers[number]
  const [selectedCustomer, setSelectedCustomer] = useState<
    null | undefined | Customer
  >(null)
  const cb = useCombobox<Customer>({
    id,
    onSelectedItemChange: ({ selectedItem }) => {
      setSelectedCustomer(selectedItem)
    },
    items: customers,
    itemToString: item => (item ? item.name : ''),
    onInputValueChange: changes => {
      customerFetcher.submit(
        { query: changes.inputValue ?? '' },
        { method: 'get', action: '/resources/customers' },
      )
    },
  })
  const busy = customerFetcher.state !== 'idle'
  const showSpinner = useSpinDelay(busy, {
    delay: 150,
    minDuration: 500,
  })
  const displayMenu = cb.isOpen && customers.length > 0
  return (
    <div className="relative">
      <input
        name="customerId"
        type="hidden"
        value={selectedCustomer?.id ?? ''}
      />
      <div className="flex flex-wrap items-center gap-1">
        <label {...cb.getLabelProps()}>
          <LabelText>Customer</LabelText>
        </label>
        {error ? (
          <em id="customer-error" className="text-d-p-xs text-red-600">
            {error}
          </em>
        ) : null}
      </div>
      <div {...cb.getComboboxProps({ className: 'relative' })}>
        <input
          {...cb.getInputProps({
            className: clsx('text-lg w-full border border-gray-500 px-2 py-1', {
              'rounded-t rounded-b-0': displayMenu,
              rounded: !displayMenu,
            }),
            'aria-invalid': Boolean(error) || undefined,
            'aria-errormessage': error ? 'customer-error' : undefined,
          })}
        />
        <Spinner showSpinner={showSpinner} />
      </div>
      <ul
        {...cb.getMenuProps({
          className: clsx(
            'absolute z-10 bg-white shadow-lg rounded-b w-full border border-t-0 border-gray-500 max-h-[180px] overflow-scroll',
            { hidden: !displayMenu },
          ),
        })}
      >
        {displayMenu
          ? customers.map((customer, index) => (
              <li
                className={clsx('cursor-pointer py-1 px-2', {
                  'bg-green-200': cb.highlightedIndex === index,
                })}
                key={customer.id}
                {...cb.getItemProps({ item: customer, index })}
              >
                {customer.name} ({customer.email})
              </li>
            ))
          : null}
      </ul>
    </div>
  )
}

function Spinner({ showSpinner }: { showSpinner: boolean }) {
  return (
    <div
      className={`absolute right-0 top-[6px] transition-opacity ${
        showSpinner ? 'opacity-100' : 'opacity-0'
      }`}
    >
      <svg
        className="-ml-1 mr-3 h-5 w-5 animate-spin"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        width="1em"
        height="1em"
      >
        <circle
          className="opacity-25"
          cx={12}
          cy={12}
          r={10}
          stroke="currentColor"
          strokeWidth={4}
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>
  )
}
```

하나의 파일 안에 인증, 데이터베이스 쿼리, 접근성(downshift), 스타일(Tailwind), UX(spin-delay)가 모두 담겼다.

## 뮤테이션과 자동 재검증

뮤테이션(mutation) 기반 컴포넌트에서는 추가적인 이점이 있다.
Remix는 `action`이 완료되면 페이지의 데이터를 자동으로 재검증(revalidate)한다.
수동으로 캐시를 무효화하거나 상태를 갱신하는 코드가 필요 없다.
알림 개수를 표시하는 벨 아이콘 같은 컴포넌트가 action 완료 후 자동으로 최신 상태를 반영한다.

## 분석

### 풀스택 컴포넌트는 "관심사 분리"의 단위를 레이어에서 기능으로 바꾼다

소프트웨어 아키텍처에서 관심사 분리(separation of concerns)의 기준은 시대마다 달랐다.
MVC 패턴은 모델(데이터), 뷰(표현), 컨트롤러(로직)를 분리했다.
전통적인 웹 개발에서는 서버(Python, Ruby, PHP)와 클라이언트(JavaScript)가 분리됐고, 이 분리는 언어의 차이로 강제됐다.

Node.js의 등장 이후 서버와 클라이언트가 같은 언어를 쓰게 됐지만, 파일 구조상 분리는 계속됐다.
Next.js의 API Routes, Remix의 Resource Routes는 같은 저장소에서 서버와 클라이언트 코드를 쓸 수 있게 했다.
풀스택 컴포넌트는 그 다음 단계다.
같은 저장소를 넘어 같은 파일에서 서버와 클라이언트를 통합한다.

이 전환의 핵심 주장은 "레이어로 분리하는 것보다 기능으로 묶는 것이 인지 부담을 줄인다"는 것이다.
검색 콤보박스를 수정할 때, 관련 코드가 `routes/resources/customers.ts`, `components/CustomerCombobox.tsx`, `api/customers.ts`에 흩어져 있는 대신 하나의 파일에 있으면 맥락 전환 비용이 줄어든다.
이것은 React의 JSX가 HTML/JS 분리를 거부했을 때와 같은 논리적 구조다.

### useFetcher가 가능하게 하는 것은 경쟁 조건 추상화다

풀스택 컴포넌트 패턴에서 가장 중요한 기술적 기여는 `useFetcher`의 자동 경쟁 조건 처리다.
사용자가 검색 입력을 빠르게 바꾸면 여러 HTTP 요청이 거의 동시에 발생한다.
나중에 보낸 요청보다 먼저 보낸 요청의 응답이 늦게 도착하면, 과거 데이터가 최신 결과를 덮어쓰는 경쟁 조건이 발생한다.

전통적인 `fetch` 기반 구현에서는 `AbortController`를 써서 이전 요청을 취소하거나, 요청 시퀀스 번호를 추적하는 코드가 필요하다.
`useFetcher`는 이 로직을 내부에서 처리하며 개발자에게 노출하지 않는다.
저자가 "경쟁 조건과 재제출을 자동으로 처리한다"고 말할 때, 이것은 비자명한 비동기 처리 코드 수십 줄을 없애준다는 의미다.

`spin-delay` 사용은 이와 다른 차원의 문제를 해결한다.
네트워크 요청이 150ms 이내에 완료되면 스피너 자체가 보이지 않는다.
스피너가 나타났다가 즉시 사라지는 "깜빡임"은 사용자에게 시스템이 불안정하다는 인상을 준다.
이 패턴이 코드 파일 하나에서 인증, 데이터베이스 쿼리, UI, UX를 통합 관리하는 방식은
컴포넌트를 "기술 스택의 조각"이 아니라 "완성된 사용자 경험의 단위"로 정의하는 것이다.

### 이 패턴은 Remix의 아키텍처 특성에 의존한다

풀스택 컴포넌트가 성립하는 이유는 Remix의 컴파일러가 같은 파일 안에서 서버 코드와 클라이언트 코드를 분리해 번들링하기 때문이다.
`loader`와 `action` 함수는 서버 번들에만 포함되고, React 컴포넌트는 클라이언트 번들에 포함된다.
개발자가 파일을 하나로 쓰더라도 배포 결과는 여전히 분리된 서버/클라이언트 코드다.

이 컴파일러 동작은 Remix의 특수한 기능이다.
일반적인 번들러(Vite, webpack)는 모듈 내보내기에 특수한 의미를 부여하지 않는다.
`export async function loader`가 "서버에서만 실행되어야 한다"는 것을 이해하는 것은 Remix의 규약이다.
이 규약을 위반하면(예: `loader` 안에서 클라이언트 전용 코드를 `import`하거나, 컴포넌트 안에서 서버 전용 모듈을 직접 `import`하면) 런타임 오류가 발생한다.

## 비평

### 패턴의 이식성을 프레임워크 의존성이 제한한다

저자는 풀스택 컴포넌트를 일반적인 설계 원칙으로 제시하지만, 구현의 모든 세부 사항은 Remix에 종속적이다.
`useFetcher`, Resource Routes, `loader`/`action` 규약은 Remix의 고유한 API다.
Next.js는 React Server Components와 Server Actions를 통해 유사한 코로케이션을 지원하지만, API 형태가 완전히 다르다.
SvelteKit은 `+page.server.ts`와 `+page.svelte`의 파일 쌍으로 같은 문제를 다른 방식으로 해결한다.

이것은 "풀스택 컴포넌트"가 특정 프레임워크의 기능 설명에 더 가깝고, 이식 가능한 설계 패턴이라기 어렵다는 뜻이다.
`useFetcher` 대신 `fetch`로 교체하면, 저자가 강조하는 핵심 이점(경쟁 조건 자동 처리, 자동 재검증)이 모두 사라진다.
패턴의 가치는 Remix의 추상화 위에 성립하며, 그 추상화 밖에서는 개발자가 직접 해결해야 할 문제들이 다시 드러난다.

저자가 Remix 팀의 멤버이자 epicweb.dev(Remix 에코시스템 교육 플랫폼)의 운영자라는 점은, 이 글이 교육 콘텐츠인 동시에 프레임워크 홍보 콘텐츠이기도 하다는 맥락을 제공한다.
이것이 글의 논지를 무효화하지는 않지만, "Remix가 아닌 환경에서도 이 원칙이 얼마나 적용 가능한가"라는 질문에 글이 충분히 답하지 않는 이유를 설명한다.

### 복잡성이 제거되는 게 아니라 프레임워크 안으로 이동한다

저자는 풀스택 컴포넌트가 복잡성을 줄인다고 주장한다.
경쟁 조건 처리, 재검증, 에러 상태가 "자동으로" 처리된다.
그러나 이 복잡성은 사라지는 것이 아니라 Remix 내부로 이동한다.

Remix가 어떻게 경쟁 조건을 처리하는지, 어떤 조건에서 재검증이 트리거되는지, 특정 상황에서 `useFetcher`가 예상과 다르게 동작할 때 어떻게 디버깅해야 하는지는 개발자가 알아야 한다.
단지 그 지식이 컴포넌트 코드에서 Remix 문서로 이동했을 뿐이다.
이것은 추상화의 일반적인 트레이드오프다.
추상화를 사용할 때는 쉽고 단순하지만, 추상화가 예상대로 동작하지 않을 때는 더 깊은 이해가 필요하다.

글은 `useFetcher`의 동작이 "자동"이라는 점을 여러 번 강조하지만, 그 자동화의 경계 조건에 대해서는 침묵한다.
예를 들어 같은 Resource Route에 여러 컴포넌트가 동시에 `useFetcher`를 사용할 때 재검증이 어떻게 동작하는지,
대규모 애플리케이션에서 재검증 범위가 성능에 어떤 영향을 미치는지는 다루지 않는다.
"자동으로 처리된다"는 설명은 입문자에게 유용하지만, 실제 프로덕션 사용을 결정하려는 독자에게는 불충분하다.

### 테스트 전략이 없는 패턴 소개는 완성되지 않았다

풀스택 컴포넌트는 서버와 클라이언트 로직이 같은 파일에 있다.
이것은 테스트 작성 방식에 직접적인 영향을 준다.
`loader` 함수만 단위 테스트하려면 Remix의 `Request` 객체를 모킹해야 한다.
`CustomerCombobox` 컴포넌트만 테스트하려면 `useFetcher`를 모킹해야 한다.
전체 컴포넌트를 통합 테스트하려면 Remix 서버 환경이 필요하다.

전통적인 분리 방식(API 엔드포인트 + 독립 컴포넌트)에서는 서버와 클라이언트를 완전히 독립적으로 테스트할 수 있다.
풀스택 컴포넌트는 이 독립성을 포기한다.
공동 배치(colocation)의 이점과 테스트 경계의 복잡화 사이에는 트레이드오프가 있으며, 저자는 이를 다루지 않는다.

이것이 실제 개발에서 어떻게 나타나는지 생각해보면, 이 글이 다루는 예제는 비교적 간단한 읽기 전용 콤보박스다.
프로덕션 환경에서 권한 검사, 감사 로그, 복잡한 에러 처리, 다국어 지원이 추가될 때, 하나의 파일이 계속 유지보수 가능한 크기를 유지할 수 있는지는 별개의 문제다.
"모든 복잡성이 한 곳에 있다"는 것은 양날의 검이다.

## 인사이트

### 네트워크 경계를 추상화하는 것이 다음 세대 프레임워크의 핵심 경쟁 영역이다

풀스택 컴포넌트가 등장하기까지의 역사는 네트워크 경계를 점진적으로 추상화하는 과정이다.
REST API는 서버와 클라이언트를 명시적 경계로 분리했다.
GraphQL은 그 경계에서 데이터 형태의 협상을 클라이언트 주도로 바꿨다.
tRPC는 타입 안전성으로 경계를 얇게 만들었다.
React Server Components와 Remix의 풀스택 컴포넌트는 경계 자체를 프레임워크 내부로 흡수한다.

각 단계는 개발자가 네트워크 경계를 의식하는 수준을 낮춘다.
REST에서는 모든 API 호출이 명시적이었다.
풀스택 컴포넌트에서는 `fetcher.submit()`이 HTTP 요청이라는 사실을 알더라도, 그 세부 동작을 직접 관리하지 않는다.
이 추상화가 더 진행되면, 개발자는 "서버에서 실행되는 코드"와 "클라이언트에서 실행되는 코드"의 구분 자체를 의식하지 않는 방향으로 수렴할 수 있다.

이 방향의 다음 단계는 이미 실험되고 있다.
React의 `"use server"`/`"use client"` 지시어는 코드 위치가 아니라 어노테이션으로 실행 환경을 선언한다.
Cloudflare의 edge-first 아키텍처는 서버/클라이언트 구분 대신 "어디서 실행되는가"를 위치 기반으로 추상화한다.
풀스택 컴포넌트는 이 흐름의 한 좌표를 차지하는 현재 시점의 해답이다.

### 컴포넌트 코로케이션 원칙은 팀 구조에 대한 암묵적 주장을 포함한다

저자는 풀스택 컴포넌트를 기술적 패턴으로 소개하지만, 이 패턴은 팀 조직 방식에 대한 암묵적 주장을 내포한다.
서버 코드와 클라이언트 코드가 같은 파일에 있다면, 이 파일을 유지보수하는 사람은 두 영역을 모두 이해해야 한다.
"프런트엔드 개발자"와 "백엔드 개발자"의 전통적 역할 분리가 이 파일 앞에서 흔들린다.

콘웨이의 법칙(Conway's Law)은 "시스템의 설계는 그것을 만든 조직의 커뮤니케이션 구조를 반영한다"고 말한다.
역으로, 파일 구조의 변화는 팀 구조를 변화시키는 압력이 된다.
풀스택 컴포넌트를 채택한 팀은 자연스럽게 "컴포넌트 오너십"이 풀스택 역량을 가진 사람에게 집중되는 방향으로 이동한다.

이 변화가 긍정적인지 부정적인지는 팀의 맥락에 따라 다르다.
소규모 팀이나 스타트업에서는 풀스택 개발자가 코드 파일 전체를 소유하는 것이 효율적이다.
대규모 조직에서 프런트엔드 팀과 백엔드 팀이 분리된 구조에서는, 풀스택 컴포넌트가 팀 간 의존성을 만들어 오히려 협업 마찰을 증가시킬 수 있다.
저자는 이 트레이드오프를 다루지 않는다.

### "자동" 추상화는 새로운 형태의 기술 부채를 만든다

`useFetcher`가 경쟁 조건을 "자동으로" 처리한다는 점은 단기적으로 개발 속도를 높인다.
그러나 이 자동화는 개발자가 경쟁 조건이 무엇인지, 왜 문제인지 이해하지 않고도 기능을 구현할 수 있게 한다.
이해 없이 동작하는 코드는 이해 부채(comprehension debt)를 만든다.

Remix가 업그레이드되거나 프레임워크를 교체할 필요가 생겼을 때, 팀이 `useFetcher`의 자동 동작에만 의존해왔다면
그 코드를 다른 환경으로 마이그레이션하는 것은 단순한 API 교체가 아니다.
경쟁 조건 처리 코드를 직접 작성한 팀은 그 로직이 무엇인지 알고 있다.
"자동으로 처리된다"는 것만 알고 있는 팀은 프레임워크 종속성이 가장 깊이 숨겨진 곳에서 가장 취약하다.

이 긴장은 모든 "생산성 우선" 추상화에 내재한다.
Rails의 `before_action`, Django ORM의 N+1 쿼리 자동 처리, Jest의 자동 모킹이 같은 패턴을 보인다.
사용하기 쉬울수록 내부를 이해하지 않고 사용하게 되고, 내부를 이해하지 않을수록 예외 상황에서의 디버깅 비용이 높아진다.
풀스택 컴포넌트 패턴을 도입하는 팀은 `useFetcher`의 동작 원리를 의도적으로 학습하는 시간을 투자해야 한다.
자동화가 그 학습을 불필요하게 만드는 것처럼 보이더라도.
