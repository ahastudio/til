# Supabase에서 비즈니스 로직을 어디에 둘 것인가

## 소개

Supabase 앱에는 보통 직접 만든 API 서버가 없다.
브라우저와 모바일 앱이 Data API(PostgREST)를 거쳐 Postgres에 바로 붙고,
요청은 로그인 여부에 따라 `anon` 또는 `authenticated` 역할로 실행된다.
그래서 “이 규칙을 어디서 강제하느냐”는 질문이 서버 프레임워크에서보다 훨씬
일찍, 그리고 훨씬 날카롭게 나온다.
클라이언트 코드에 둔 규칙은 사용자가 개발자 도구에서 그대로 우회할 수 있기
때문이다.

Supabase가 제공하는 자리는 다섯 가지다.
누가 어떤 행에 접근하는지는 Row Level Security(RLS) 정책이 맡고,
여러 테이블을 한 트랜잭션으로 바꾸는 규칙은 데이터베이스 함수가 맡는다.
테이블 이벤트에 반응하는 규칙은 트리거가 맡고,
외부 API 호출이나 TypeScript가 필요한 일은 Edge Functions가 맡는다.
오래 걸리거나 반복되는 일은 Queues와 Cron이 맡는다.

공식 문서의 기준은 짧다.
데이터를 많이 다루는 작업은 데이터베이스 안에서 도는 데이터베이스 함수로,
지연 시간이 중요한 작업은 전 세계에 배포되는 Edge Functions로 하라는 것이다.
이 글은 그 한 줄을 실제로 쓸 수 있는 판단 기준으로 풀고,
주문 하나가 들어와서 확인 메일이 나가기까지의 흐름을 따라 각 자리에 무엇을
두는지 보인다.

## 동작 방식

### 요청은 권한과 정책을 차례로 통과한다

클라이언트 요청이 테이블에 닿기 전에 Postgres는 두 가지를 검사한다.
먼저 권한(grant)이 그 역할이 해당 연산을 아예 할 수 있는지 정하고,
그다음 RLS 정책이 그 연산이 어느 행에 적용되는지 정한다.
권한이 없으면 정책을 보기도 전에 `42501` 오류가 난다.

| 역할            | 요청의 주체                     | RLS    |
| --------------- | ------------------------------- | ------ |
| `anon`          | 로그인하지 않은 방문자          | 적용됨 |
| `authenticated` | 로그인한 사용자                 | 적용됨 |
| `service_role`  | 서버 쪽 코드(Edge Function 등)  | 우회함 |
| `postgres`      | 대시보드, 마이그레이션의 소유자 | 우회함 |

기존 프로젝트에서는 `public`에 새로 만든 테이블에 세 API 역할 모두의
`select`, `insert`, `update`, `delete` 권한이 자동으로 붙고,
함수에는 `execute` 권한이 붙는다.
정책을 추가해도 이 권한은 회수되지 않는다.
Supabase는 이 자동 부여를 없애 노출을 명시적 선택으로 바꾸는 중이라고
밝히고 있으므로, 프로젝트마다 실제 기본값을 확인해야 한다.

### 로직을 둘 수 있는 다섯 자리

| 자리              | 실행 위치        | 맞는 일                       | 호출자의 트랜잭션 |
| ----------------- | ---------------- | ----------------------------- | ----------------- |
| RLS 정책          | Postgres         | 누가 어떤 행을 읽고 쓰는가    | 안에서 평가       |
| 데이터베이스 함수 | Postgres         | 여러 테이블을 묶는 규칙, 집계 | 함께 커밋         |
| 트리거            | Postgres         | 같은 쓰기에 딸린 후속 쓰기    | 함께 커밋         |
| Edge Functions    | Deno 기반 런타임 | 외부 API, 웹훅 수신, LLM 호출 | 밖                |
| Queues, Cron      | Postgres + 워커  | 재시도가 필요한 일, 주기 작업 | 메시지만 함께     |

마지막 열이 이 글의 핵심이다.
Postgres 안에 있는 세 자리는 원래 쓰기와 같은 트랜잭션에서 성공하거나 함께
되돌려진다.
Edge Function은 그 바깥에서 돌기 때문에,
Edge Function 안에서 두 번 쓰면 첫 번째만 남는 상황이 언제든 생길 수 있다.

### 주문 하나의 흐름

이 글의 예제는 다음 순서로 움직인다.

```text
클라이언트 ── rpc('place_order') ──▶ place_order()        [트랜잭션 시작]
                                      ├ products 재고 차감
                                      ├ orders 행 추가
                                      └ 트리거 → pgmq.send()  [같은 트랜잭션]
                                                              [커밋]
pg_cron (매분) ── net.http_post ──▶ process-orders Edge Function
                                      ├ 큐에서 메시지 읽기
                                      ├ 확인 메일 발송 (외부 API)
                                      └ 메시지 삭제
```

재고 차감, 주문 기록, 후속 작업 예약은 하나의 커밋으로 묶인다.
메일 발송은 커밋 뒤에 따로 일어나고, 실패하면 메시지가 큐에 남아 다시
처리된다.

## 구현하기

아래 SQL은 마이그레이션 파일 하나에 순서대로 넣어 실행할 수 있다.
권한과 RLS는 같은 마이그레이션에 두라는 것이 공식 문서의 권고다.

### 테이블과 권한, RLS

```sql
create table public.products (
  id bigint generated always as identity primary key,
  name text not null,
  price integer not null check (price >= 0),
  stock integer not null check (stock >= 0)
);

create table public.orders (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users,
  product_id bigint not null references public.products,
  quantity integer not null check (quantity > 0),
  total integer not null,
  created_at timestamptz not null default now()
);

alter table public.products enable row level security;
alter table public.orders enable row level security;

-- 자동으로 붙었을 수 있는 권한을 먼저 모두 회수한다.
revoke all on table public.products, public.orders from anon, authenticated;

-- 상품은 누구나 읽기만 한다.
grant select on table public.products to anon, authenticated;
create policy "Anyone can read products"
on public.products for select
to anon, authenticated
using ( true );

-- 주문은 본인 것만 읽는다. insert 권한은 주지 않는다.
-- 주문은 오직 place_order()를 거쳐서만 생긴다.
grant select on table public.orders to authenticated;
create policy "Users can read their own orders"
on public.orders for select
to authenticated
using ( (select auth.uid()) = user_id );
```

`orders`에 `insert` 권한을 주지 않은 것이 설계의 핵심이다.
권한을 주고 RLS로 `user_id`만 검사하면,
사용자는 `total`을 0으로 적은 주문을 직접 넣을 수 있다.
행 단위 접근 제어는 RLS로 충분하지만, 값 사이의 규칙은 RLS로 표현하기
어렵다.

### 트랜잭션이 필요한 규칙은 데이터베이스 함수로

```sql
create or replace function public.place_order(product_id bigint, quantity integer)
returns bigint
language plpgsql
security definer      -- 사용자가 직접 쓸 수 없는 products, orders를 바꿔야 한다.
set search_path = ''  -- definer 함수에서는 필수. 모든 이름에 스키마를 붙인다.
as $$
declare
  caller uuid := auth.uid();
  unit_price integer;
  new_order bigint;
begin
  -- definer 함수는 RLS를 우회하므로 호출자 확인을 본문에서 직접 한다.
  if caller is null then
    raise exception 'sign-in required' using errcode = '42501';
  end if;
  if place_order.quantity <= 0 then
    raise exception 'quantity must be positive' using errcode = '22023';
  end if;

  -- 재고 확인과 차감을 조건부 update 한 문장으로 한다.
  -- select 후 update로 나누면 동시 주문 두 건이 같은 재고를 본다.
  update public.products p
  set stock = p.stock - place_order.quantity
  where p.id = place_order.product_id
    and p.stock >= place_order.quantity
  returning p.price into unit_price;

  if not found then
    raise exception 'out of stock' using errcode = 'P0001';
  end if;

  -- 가격은 클라이언트가 보낸 값이 아니라 DB에 있는 값으로 계산한다.
  insert into public.orders (user_id, product_id, quantity, total)
  values (caller, place_order.product_id, place_order.quantity,
          unit_price * place_order.quantity)
  returning id into new_order;

  return new_order;
end;
$$;

-- 함수의 기본 execute 권한은 public(모든 역할)에 있다. anon까지 막는다.
revoke execute on function public.place_order(bigint, integer) from public, anon;
grant execute on function public.place_order(bigint, integer) to authenticated;
```

클라이언트에서는 함수 이름과 인자 이름으로 부른다.

```ts
const { data: orderId, error } = await supabase.rpc('place_order', {
  product_id: 1,
  quantity: 2,
})
if (error) {
  // error.code에 함수가 던진 '42501', 'P0001' 같은 SQLSTATE가 들어온다.
  console.error(error.code, error.message)
}
```

공식 문서는 `security invoker`를 기본으로 쓰라고 권한다.
여기서 `definer`를 고른 이유는 사용자에게 `orders`의 `insert` 권한을 주지 않기
위해서다.
`invoker` 함수는 호출자 권한으로 돌기 때문에,
함수 안의 `insert`가 성공하려면 사용자가 테이블에 직접 `insert`할 수 있어야
하고, 그러면 함수를 거치지 않는 경로가 다시 열린다.
`definer`를 쓰는 대가는 두 가지를 반드시 함께 해야 한다는 것이다.
본문에서 호출자를 직접 확인하고, `execute` 권한을 `public`과 `anon`에서
회수해야 한다.

### 같은 쓰기에 딸린 후속 작업은 트리거로

```sql
-- Queues 확장(pgmq)이 켜져 있어야 한다.
select pgmq.create('order_events');

-- 트리거 함수는 Data API로 노출되지 않는 스키마에 둔다.
create schema if not exists private;

create or replace function private.enqueue_order_event()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  perform pgmq.send(
    'order_events',
    jsonb_build_object('order_id', new.id, 'user_id', new.user_id)
  );
  return new;
end;
$$;

create trigger orders_enqueue_event
after insert on public.orders
for each row
execute function private.enqueue_order_event();
```

트리거는 주문을 넣은 트랜잭션 안에서 실행된다.
`place_order()`가 중간에 실패해 롤백되면 큐에 넣은 메시지도 함께 사라진다.
주문은 생겼는데 후속 작업 예약이 빠지는 경우도,
주문은 없는데 메일이 나가는 경우도 이 구조에서는 생기지 않는다.
흔히 트랜잭셔널 아웃박스(transactional outbox)라고 부르는 패턴을 별도
인프라 없이 Postgres 안에서 얻는 셈이다.

### 외부 호출은 Edge Function에서, 트랜잭션 밖에서

워커 함수는 사용자가 아니라 Cron이 부르므로 비밀 키로 인증한다.
`auth: 'secret'`을 쓰려면 플랫폼의 JWT 검사를 꺼야 한다.

```toml
# supabase/config.toml
[functions.process-orders]
verify_jwt = false
```

```ts
// supabase/functions/process-orders/index.ts
import { withSupabase } from 'npm:@supabase/server@1'

const QUEUE = 'order_events'

export default {
  // 'secret'은 apikey 헤더의 default 비밀 키만 받는다.
  fetch: withSupabase({ auth: 'secret' }, async (_req, ctx) => {
    const queue = ctx.supabaseAdmin.schema('pgmq_public')

    // 읽은 메시지는 60초 동안 다른 워커에게 보이지 않는다.
    // 그 안에 delete하지 못하면 다시 보이고, 다음 실행에서 재처리된다.
    const { data: messages, error } = await queue.rpc('read', {
      queue_name: QUEUE,
      sleep_seconds: 60,
      n: 10,
    })
    if (error) return Response.json({ error: error.message }, { status: 500 })

    let done = 0
    for (const msg of messages ?? []) {
      const { order_id, user_id } = msg.message
      try {
        await sendConfirmationEmail(order_id, user_id)
        // 외부 호출이 성공한 뒤에만 지운다.
        await queue.rpc('delete', { queue_name: QUEUE, message_id: msg.msg_id })
        done++
      } catch (err) {
        // 지우지 않으면 가시성 시간이 지난 뒤 다시 처리된다.
        console.error('order', order_id, 'failed:', err)
      }
    }
    return Response.json({ read: messages?.length ?? 0, done })
  }),
}

async function sendConfirmationEmail(orderId: number, userId: string) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${Deno.env.get('RESEND_API_KEY')}`,
      'Content-Type': 'application/json',
      // 같은 주문에 대해 두 번 보내지 않도록 공급자 쪽 멱등성 키를 쓴다.
      'Idempotency-Key': `order-confirmation-${orderId}`,
    },
    body: JSON.stringify({
      from: 'shop@example.com',
      to: await lookupEmail(userId),
      subject: `주문 #${orderId} 확인`,
      text: '주문이 접수되었습니다.',
    }),
  })
  if (!res.ok) throw new Error(`email API ${res.status}`)
}

async function lookupEmail(_userId: string): Promise<string> {
  // 실제로는 ctx.supabaseAdmin.auth.admin.getUserById()로 조회한다.
  return 'customer@example.com'
}
```

`ctx.supabaseAdmin`이 `pgmq_public` 함수를 부르려면 대시보드의 Queues 설정에서
“Expose Queues via PostgREST”를 켜고, `service_role`에 해당 함수 권한을 줘야
한다.
`ctx.supabaseAdmin`은 RLS를 우회하므로, 사용자가 부르는 함수에서 이 클라이언트로
공유 테이블을 조회하면 모든 사용자의 행이 나온다.
사용자 요청을 처리하는 함수에서는 `auth: 'user'`와 `ctx.supabase`를 쓴다.

### 주기 실행은 Cron으로

```sql
-- URL과 키는 Vault에 넣고 SQL에는 이름만 남긴다.
select vault.create_secret('https://<project-ref>.supabase.co', 'project_url');
select vault.create_secret('<default secret key>', 'worker_secret_key');

select cron.schedule(
  'process-orders-every-minute',
  '* * * * *',
  $$
  select net.http_post(
    url := (select decrypted_secret from vault.decrypted_secrets
            where name = 'project_url') || '/functions/v1/process-orders',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'apikey', (select decrypted_secret from vault.decrypted_secrets
                 where name = 'worker_secret_key')
    ),
    body := '{}'::jsonb
  );
  $$
);
```

## 값 정하기

| 값                         | 시작값 | 근거                                                       |
| -------------------------- | ------ | ---------------------------------------------------------- |
| 큐 가시성 시간             | 60초   | 메시지 10개 × 외부 호출 시간보다 넉넉해야 중복 처리가 없다 |
| 한 번에 읽는 메시지 수 `n` | 10     | Edge Function CPU 시간 한도(요청당 2초) 안에 끝나야 한다   |
| Cron 주기                  | 1분    | 메일 지연 허용치. 공식 권고는 동시 실행 작업 8개 이하      |
| `pg_net` 타임아웃          | 2000ms | 기본값. 워커가 응답을 늦게 줘도 Cron은 기다리지 않는다     |

가시성 시간은 “한 번 읽은 메시지를 처리할 수 있는 최대 시간”이다.
너무 짧으면 처리 중인 메시지가 다른 실행에 다시 보이고,
너무 길면 실패한 메시지가 그만큼 늦게 재시도된다.
`net._http_response`에서 워커의 응답 시간을, 큐 테이블에서 `read_ct`가 2 이상인
메시지 비율을 보고 조정한다.

## 트레이드오프

### 데이터베이스 함수는 정합성을 주고 개발 경험을 가져간다

데이터베이스 함수의 이점은 분명하다.
여러 테이블을 바꾸는 규칙이 하나의 트랜잭션 안에서 실행되고,
네트워크 왕복 없이 데이터 옆에서 돈다.
Data API, Realtime, 다른 도구 등 어느 경로로 들어오든 같은 규칙이 적용된다.

대가는 코드가 PL/pgSQL로 쓰이고 마이그레이션으로 배포된다는 점이다.
함수를 고치려면 `create or replace`가 담긴 새 마이그레이션을 만들어야 하고,
diff는 함수 전체가 바뀐 것처럼 보이기 쉽다.
TypeScript 타입 검사, 익숙한 단위 테스트 도구,
라이브러리 생태계를 모두 내려놓아야 한다.
Supabase는 같은 이름에 인자만 다른 오버로드 함수를 지원하지 않으므로,
인자를 바꿀 때는 기존 함수를 지우는 마이그레이션도 함께 써야 한다.

그래서 함수에는 “같이 커밋되어야 하는 것”만 넣는 것이 좋다.
금액 계산 규칙이 복잡해서 테스트가 많이 필요하다면,
계산은 Edge Function에서 하고 결과를 함수에 넘겨 검증과 기록만 시키는 분할도
가능하다.
다만 그 순간 클라이언트가 계산 결과를 위조할 수 있는지를 다시 따져야 한다.

### `security definer`는 RLS를 끄는 스위치다

`definer` 함수는 소유자 권한으로 돈다.
대시보드나 마이그레이션으로 만든 함수의 소유자는 `postgres`이고,
`postgres`는 RLS를 우회한다.
즉 `definer` 함수 안에서는 지금까지 RLS로 쌓은 행 단위 보호가 전부 사라진다.

`execute` 권한을 `authenticated`에만 줘도 이 문제는 풀리지 않는다.
권한은 누가 함수를 부를 수 있는지만 정하고,
그 사람이 어떤 행을 돌려받는지는 정하지 않는다.
본문에서 `auth.uid()`로 소유권을 직접 확인하지 않으면,
로그인한 모든 사용자가 남의 행을 받는다.

반대로 `invoker`만 쓰면 이 위험은 없지만,
테이블에 직접 쓰는 권한을 사용자에게 줘야 해서 함수가 강제하려던 규칙을 우회할
길이 열린다.
둘 다 가질 수는 없다.
`definer`를 쓰고 그 함수를 작게 유지하며 반드시 테스트하는 것이 현실적인
절충이다.

### 비동기로 미루면 정확히 한 번은 얻기 어렵다

Queues 문서는 가시성 시간 안에서 메시지가 정확히 한 번 전달된다고 설명한다.
하지만 그것은 큐에서 꺼내는 쪽의 보장이지, 외부 부수 효과의 보장이 아니다.
메일 API 호출은 성공했는데 `delete` 직전에 함수가 시간 제한에 걸리면,
메시지는 가시성 시간 뒤 다시 보이고 메일은 두 번 나간다.

이 간극은 Supabase 설정으로 메울 수 없다.
외부 호출은 공급자의 멱등성 키를 쓰거나,
“이미 처리함” 표시를 DB에 먼저 남기고 확인하는 식으로 멱등하게 만들어야 한다.
반대로 동기 처리(주문 요청 안에서 메일 발송)를 택하면 중복은 줄지만,
메일 API 장애가 곧 주문 실패가 되고 트랜잭션과 외부 호출이 다시 어긋난다.

### Database Webhooks는 간편하지만 재시도가 없다

Database Webhooks는 `pg_net`으로 HTTP 요청을 보내는 트리거를 감싼 기능이다.
대시보드에서 테이블과 이벤트만 고르면 되므로 위의 큐와 Cron 구성보다 훨씬
간단하다.
`pg_net`은 비동기이므로 느린 외부 요청이 쓰기를 붙잡지도 않는다.

대신 `pg_net`의 요청은 트랜잭션이 커밋된 뒤에야 시작되고,
결과는 `net._http_response`에 6시간만 남는다.
요청이 실패해도 다시 보내는 주체가 없다.
알림처럼 한 번 놓쳐도 되는 일에는 웹훅이,
결제 후속 처리처럼 놓치면 안 되는 일에는 큐가 맞다.

## 함정

- `public`에 테이블을 만들고 정책만 추가하면 `anon`의 `insert` 권한이 그대로
  남는다. 정책은 권한을 회수하지 않는다.
- 뷰는 기본적으로 `postgres` 권한으로 만들어져 RLS를 우회한다.
  보호된 테이블 위에 뷰를 만들면 정책이 숨기려던 행이 뷰로 새어 나간다.
- `update` 정책만 있고 `select` 정책이 없으면 `update`가 기대대로 동작하지
  않는다.
- `definer` 함수에 `search_path`를 비우지 않으면,
  호출자가 만든 같은 이름의 객체가 함수 안에서 대신 쓰일 수 있다.
- 로컬 개발에서 웹훅 URL에 `localhost`를 쓰면 Docker 컨테이너 자신을 가리킨다.
  호스트의 함수는 `host.docker.internal`로 부른다.
- 로컬 CLI는 요청이 끝나면 Edge Function 인스턴스를 바로 종료한다.
  `EdgeRuntime.waitUntil()`로 미룬 작업을 로컬에서 시험하려면 `config.toml`의
  `[edge_runtime]`에 `policy = "per_worker"`를 둔다.
- Edge Function의 요청당 CPU 시간은 2초, 실행 시간은 무료 플랜 150초,
  유료 플랜 400초다. 한 번에 큐를 많이 비우려 하면 이 한도에 먼저 걸린다.
- Cron 작업은 동시에 8개 이하, 한 번에 10분 이하로 돌리라는 것이 공식 권고다.

## 확인하기

`place_order()`가 의도대로 막고 허용하는지는 pgTAP 테스트로 확인한다.
`supabase test new place_order.test`로 파일을 만들고 다음 내용을 넣는다.

```sql
-- supabase/tests/place_order.test.sql
begin;
select plan(5);

insert into auth.users (id, email)
values ('11111111-1111-1111-1111-111111111111', 'buyer@example.com');
insert into public.products (name, price, stock)
values ('keyboard', 50000, 1);

-- 로그인하지 않은 호출자는 execute 권한이 없다.
set local role anon;
select throws_ok(
  $$select public.place_order(1, 1)$$,
  '42501',
  null,
  'anon cannot place an order'
);

-- 로그인한 사용자는 직접 insert할 수 없다.
set local role authenticated;
set local request.jwt.claim.sub = '11111111-1111-1111-1111-111111111111';
select throws_ok(
  $$insert into public.orders (user_id, product_id, quantity, total)
    values ('11111111-1111-1111-1111-111111111111', 1, 1, 0)$$,
  '42501',
  null,
  'users cannot insert orders directly'
);

-- 함수를 거치면 주문이 생기고 가격은 DB 값으로 계산된다.
select lives_ok(
  $$select public.place_order(1, 1)$$,
  'a signed-in user places an order'
);
select results_eq(
  $$select total from public.orders$$,
  array[50000],
  'total comes from the product price'
);

-- 재고가 0이 되었으므로 두 번째 주문은 실패한다.
select throws_ok(
  $$select public.place_order(1, 1)$$,
  'P0001',
  'out of stock',
  'the second order fails when stock runs out'
);

select * from finish();
rollback;
```

```bash
supabase start
supabase db reset   # 마이그레이션을 처음부터 적용한다
supabase test db
```

기대 출력은 다섯 항목이 모두 `ok`로 표시되는 것이다.
테스트가 `begin`과 `rollback` 사이에서 돌기 때문에,
트리거가 큐에 넣은 메시지도 함께 사라진다.

큐와 워커는 로컬에서 다음 순서로 확인한다.

```bash
supabase functions serve process-orders
```

```sql
-- 주문 뒤 큐에 메시지가 쌓였는지 본다.
select msg_id, read_ct, message from pgmq.q_order_events;

-- Cron이 보낸 요청 중 실패한 것을 본다.
select id, status_code, error_msg, created
from net._http_response
where status_code >= 400 or error_msg is not null
order by created desc;

-- Cron 실행 기록을 본다.
select jobid, status, return_message, start_time
from cron.job_run_details
order by start_time desc
limit 10;
```

## 체크리스트

- 노출된 스키마의 모든 테이블에 RLS가 켜져 있는가?
- 정책과 별도로 `anon`, `authenticated`의 권한을 회수하고 필요한 것만 다시
  부여했는가?
- 클라이언트가 직접 쓰면 안 되는 테이블에서 `insert`, `update` 권한을 뺐는가?
- 모든 `security definer` 함수에 `set search_path = ''`가 있는가?
- 모든 `security definer` 함수가 본문에서 `auth.uid()`로 호출자를 확인하는가?
- 그 함수의 `execute` 권한을 `public`과 `anon`에서 회수했는가?
- 가격처럼 클라이언트가 위조할 수 있는 값을 DB에서 다시 계산하는가?
- 트리거 함수를 Data API로 노출되지 않는 스키마에 두었는가?
- 사용자 요청을 받는 Edge Function이 `ctx.supabaseAdmin` 대신 `ctx.supabase`를
  쓰는가?
- 큐 소비자의 외부 호출이 두 번 실행되어도 결과가 같은가?
- 테이블마다 허용과 거부를 모두 검사하는 `supabase test db` 테스트가 있는가?

## 기억할 원칙

### 규칙은 우회할 수 없는 가장 바깥 자리에 둔다

Supabase에서 클라이언트는 데이터베이스와 직접 이야기한다.
그러므로 클라이언트 코드에 둔 검사는 검사가 아니라 안내문에 가깝다.
어떤 규칙이 깨지면 안 된다면,
그 규칙은 클라이언트가 거치지 않고는 데이터에 닿을 수 없는 자리에 있어야 한다.
행 단위 접근은 RLS, 값 사이의 규칙은 권한을 막아 둔 테이블 앞의 함수가 그
자리다.

### 같이 커밋되어야 하는 것과 나중에 해도 되는 것을 먼저 나눈다

로직을 어디에 둘지 고민될 때는 언어나 성능보다 이 질문을 먼저 던진다.
“이 일이 실패하면 원래 쓰기도 취소되어야 하는가?”
그렇다면 Postgres 안의 함수나 트리거에 둔다.
아니라면 큐에 메시지만 남기고, 실제 작업은 재시도할 수 있는 워커로 보낸다.
이 구분만 지키면 Edge Function과 데이터베이스 함수 사이의 선택은 대부분 저절로
정해진다.

## 참고 자료

- [Database functions](https://supabase.com/docs/guides/database/functions)
- [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Securing your API](https://supabase.com/docs/guides/api/securing-your-api)
- [Postgres Triggers](https://supabase.com/docs/guides/database/postgres/triggers)
- [Database Webhooks](https://supabase.com/docs/guides/database/webhooks)
- [pg_net: Async Networking](https://supabase.com/docs/guides/database/extensions/pg_net)
- [Edge Functions](https://supabase.com/docs/guides/functions)
- [Securing Edge Functions](https://supabase.com/docs/guides/functions/auth)
- [Background Tasks](https://supabase.com/docs/guides/functions/background-tasks)
- [Edge Functions Limits](https://supabase.com/docs/guides/functions/limits)
- [Supabase Queues](https://supabase.com/docs/guides/queues)
- [Queues API](https://supabase.com/docs/guides/queues/api)
- [Cron](https://supabase.com/docs/guides/cron)
- [Scheduling Edge Functions](https://supabase.com/docs/guides/functions/schedule-functions)
