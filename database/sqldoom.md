# SQLDoom: 원작 Doom을 통째로 SQL 안으로 옮기다

원문: [We ported the original Doom to SQL | CedarDB](https://cedardb.com/blog/sqldoom/)

HN 토론: <https://news.ycombinator.com/item?id=49948300> (336점, 56개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/qf2mtz/we_ported_original_doom_sql> (1점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34815>

## 요약

CedarDB의 Lukas Vogel이 1993년 Doom의 게임 로직과 렌더러를 SQL로 옮겨
데이터베이스 안에서 실행한 과정을 정리한 글이다.
게임 루프는 원작과 같은 35 FPS로 돌고, 렌더러는 320x200 프레임 버퍼 전체를
저자의 노트북에서 최대 60 Hz로 만들어 낸다.
Python은 타이밍을 맞추고, 키보드를 읽고,
돌려받은 비트맵을 화면에 띄우는 일만 한다.
멀티플레이어도 동작하며, EU와 US에 4인 데스매치 공개 서버를 열어 두었다.
자리가 차면 대기열에 들어가고, 대기열마저 차면 진행 중인 게임 상태를
SQL로 조회할 수 있다.
코드는 GitHub의 `cedardb/sqldoom` 저장소에 GPL v2(이후 버전 포함)로
공개되어 있고, 저장소는 2026년 9월 22일에 만들어졌다.

전작은 작년에 공개한 DOOMQL이다.
DOOMQL은 Doom과 비슷해 보이는 ASCII 아트를 30 FPS로 그렸지만,
레이캐스팅 방식이라 Doom보다는 Wolfenstein 3D에 가깝다는 지적을 받았다.
Doom은 BSP 트리를 써서 깊이 순서를 싸게 정하고,
그 덕분에 텍스처와 임의 각도의 벽, 다양한 바닥 높이를 감당할 수 있었다.
저자는 이 지적을 그냥 넘기지 못했고, 육아휴직 기간에
다시 손을 대 진짜 Doom을 SQL로 옮겼다고 말한다.

### 다섯 가지 규칙과 구조

저자는 먼저 규칙을 정한다.
첫째, 진짜 Doom처럼 보여야 한다.
둘째, 더 중요하게는 진짜 Doom처럼 느껴져야 한다.
셋째, 렌더링은 순수하게 SQL로 하며,
출력은 모든 픽셀의 정확한 RGB 값을 담은 테이블이나 비트맵이어야 한다.
넷째, 게임 루프도 순수하게 SQL로 하되
데이터베이스 안의 사용자 정의 함수는 허용한다.
다섯째, 다른 언어로 클라이언트를 써도 되지만 입력 파싱, 게임 틱 구동,
출력 비트맵 표시만 맡아야 한다.

Python 스크립트 하나가 pygame으로 입력과 화면을 처리하고
1초에 35번 게임 틱을 호출한다.
게임 로직, 게임 상태, 렌더러는 모두 데이터베이스 안에 있다.
게임 로직은 고정된 35 Hz 루프로 돌고, 렌더러는 게임 상태 테이블의 순수 함수라서
클라이언트가 원할 때마다 새 프레임을 요청할 수 있다.
두 경로는 의도적으로 분리되어 있다.

### WAD를 관계형 테이블로

Doom의 `.wad` 파일은 이미 관계형에 가깝다.
VERTEXES 두 개를 LINEDEF가 잇고, LINEDEF에는 SIDEDEF가 두 개 있고,
SIDEDEF가 SECTOR의 경계를 이루고, SECTOR 안에 THINGS가 있는 식이다.
저자는 WAD 전체를 데이터베이스로 옮기는 일이 의외로 간단했다며
Python 약 1,000줄이 들었고,
Doom 1 전체를 가져오는 데 노트북에서 약 18초가 걸린다고 적었다.
다만 README는 같은 임포터(`wad_loader.py`)를 약 1,300줄이라고 적는다.

가져온 데이터는 보통의 SQL로 다룰 수 있다.
다음은 E1M1을 위에서 내려다본 지도로 그리는 쿼리다.

```sql
WITH wall AS (
  SELECT round((v1.x + (v2.x - v1.x) * t / 32.0) / 48) AS col, -- 48 units per column
         round((v1.y + (v2.y - v1.y) * t / 32.0) / 96) AS row, -- chars are 2:1
         l.left_sd_id < 0 AS solid -- one-sided lines are pass-through
  FROM linedefs l, generate_series(0, 32) AS t        -- walk each line in 32 steps
  JOIN vertexes v1 ON (v1.map_id, v1.id) = (l.map_id, l.v1_id)
  JOIN vertexes v2 ON (v2.map_id, v2.id) = (l.map_id, l.v2_id)
  WHERE l.map_id = 1
)
SELECT string_agg(CASE WHEN (col, row) IN (SELECT col, row FROM wall WHERE solid) THEN '#'
                       WHEN (col, row) IN (SELECT col, row FROM wall)             THEN '.'
                       ELSE ' ' END, '' ORDER BY col)
FROM generate_series(-16, 79) AS col, generate_series(-51, -21) AS row
GROUP BY row ORDER BY row DESC;
```

각 LINEDEF를 `generate_series(0, 32)`로 33개 점으로 나누고,
두 꼭짓점 사이를 선형 보간한 좌표를 문자 격자의 칸으로 내린다.
글자가 세로로 길어서 y축은 x축의 두 배인 96 단위로 나눈다.
왼쪽 SIDEDEF가 없는 한쪽 면 선은 막힌 벽이라 `#`으로,
나머지 선은 `.`으로 찍는다.
마지막으로 격자 전체를 `generate_series`로 만들고
행마다 `string_agg`로 한 줄 문자열을 만든다.

### 게임 루프와 틱 예산

원작 Doom은 고정된 35 Hz 시계로 돌았으므로 틱 하나의 예산은 28.6 ms이고,
틱마다 정확히 한 프레임을 그려서 35 FPS가 상한이었다.
SQLDoom은 원작의 상수가 그대로 통하도록 게임 로직을 35 Hz로 유지하되
그리기를 분리했다.
클라이언트는 언제든 프레임을 요청할 수 있고, 틱 사이의 카메라 위치는 보간한다.
따라서 지켜야 할 예산은 두 개다.
28.6 ms마다 틱을 돌려야 하고, 초당 최소 35프레임을 그려야 한다.

게임 틱은 본질적으로 절차적이다.
CedarDB에는 PL/pgSQL과 비슷한 cedarscript라는 스크립트 언어가 있어서
틱마다 할 일의 순서를 적을 수 있다.
다음은 틱 함수의 일부다.

```sql
doom_cs_clock(map, p);
let mut plan = doom_cs_plan(map, p);    -- returns a bitmask of functions to trigger

let use_queued = doom_tic_use(map, p, plan);
if (plan & 2) <> 0 OR use_queued { active = doom_cs_activate_specials(map); }
if (plan & 4) <> 0 OR active <> 0 { doom_cs_doors(map, p); }

doom_tic_move(map, p);                  -- full movement, or just turning
doom_cs_death(map, p);                  -- process deaths

plan = doom_cs_plan(map, p);            -- the world moved; re-plan
plan = doom_tic_secrets(map, p, plan);  -- secrets, walkover lines, pickups
plan = doom_tic_weapon(map, p, plan);   -- weapon state, hitscan, damage
...
if sound_due { doom_cs_sound(map, p); } -- yes, we also play sounds
doom_cs_monsters(map, p);               -- always
doom_cs_sector_fx(map, p);              -- always
doom_cs_thing_physics(map);             -- always
```

`doom_cs_plan`이 이번 틱에 실행할 함수를 비트마스크로 돌려주고,
이 값에 따라 특수 효과 활성화나 문 처리 같은 단계를 건너뛴다.
세계가 움직인 뒤에는 계획을 다시 세운다.
Python 드라이버는 1/35초마다 `SELECT doom_run_game_tic(...)`을 호출하고,
각 함수는 SQL 문 묶음을 실행한다.

몬스터 AI의 상태 기계는 다음처럼 생겼다.

```sql
-- Abridged from sql/runtime/functions/26_cs_monsters.sql.
WITH RECURSIVE
  monsters AS ( [...] ),   -- who is alive, what kind, where
  los      AS ( [...] ),   -- visible, in_view_cone, dist: recursive, walks walls
  decision AS ( [...] ),   -- one row per actor: its state and what it can see
  transitions AS (
    SELECT d.*,
      CASE
        WHEN NOT d.alive AND d.state NOT IN ('die', 'dead', 'xdeath') THEN
          CASE WHEN d.health < -d.max_health AND d.xdeath_frame IS NOT NULL
               THEN 'xdeath'::actor_state ELSE 'die'::actor_state END -- GORY EXPLOSION!
        WHEN d.state = 'stand' THEN
          CASE WHEN d.visible AND d.in_view_cone AND d.dist <= sight_range
               THEN 'see'::actor_state ELSE 'stand'::actor_state END
        WHEN d.state_tics > 1 THEN d.state          -- animation still running
        WHEN d.state = 'see' THEN
          CASE WHEN d.visible AND d.dist <= d.attack_range
                    AND d.attack_cooldown <= 0
               THEN 'missile'::actor_state ELSE 'see'::actor_state END
        [...]                -- die, xdeath, missile, pain, barrel: 5 more
        ELSE d.state
      END AS next_state
    FROM decision d
  )
UPDATE monster_ai ai
SET state = n.next_state, state_tics = n.next_tics, seq_index = n.next_seq,
    fired_this_tick = n.advances AND n.lands_on_attack_frame
FROM next_values n
WHERE ai.map_id = n.map_id AND ai.thing_id = n.thing_id;
```

몬스터마다 루프를 도는 대신, 시야 판정까지 끝낸 행 집합에 `CASE` 하나로
다음 상태를 계산하고 `UPDATE ... FROM` 한 번으로 모든 몬스터에 반영한다.
체력이 최대 체력의 음수보다 낮아지고 폭사 프레임이 있으면 `xdeath`로,
서 있다가 시야 원뿔 안에서 플레이어를 보면 `see`로,
사거리 안에서 쿨다운이 끝났으면 `missile`로 넘어간다.

가장 느린 틱은 E4M1에서 몬스터 46마리가 열리는 문으로 한꺼번에 몰려드는
장면이었고 10.45 ms, 즉 예산의 약 37%였다.
몬스터 6마리가 깨어 있는 보통의 틱은 평균 2.15 ms로 예산의 약 8%다.
게임 로직은 SQL 약 5,900줄이고, 같은 일을 하는 원작 C 코드는
약 9,000줄이라고 저자는 비교한다.
저자는 이 작업 덕분에 ECS(Entity Component System) 패턴이
비로소 이해되었다고 말한다.
컴포넌트는 테이블이 되고, 시스템은 관심 있는 테이블을 엔티티 키로 조인하는
`UPDATE`나 `INSERT`가 된다는 것이다.

### 렌더링 파이프라인

프레임 하나는 레벨 지형, 게임 상태, 플레이어 위치를 입력으로 받아
완성된 프레임 버퍼를 돌려주는 거대한 뷰다.
전체 파이프라인의 윤곽은 다음과 같다.

```sql
WITH RECURSIVE
  render_context AS (SELECT $1 AS map_id, $2 AS player_thing_id, $3 AS difficulty),
  pos            AS (SELECT $4 AS x, $5 AS y, $6 AS z, $7 AS angle),
  visible_children AS ( ... ),    -- walk the BSP, culling invisible segments
  clipped, projected, on_screen,  -- project segments to screen space
  wall_parts, columns, fragments, -- one row per wall pixel
  panel_clips, plane_spans, ...,  -- ceiling/floorclip as window functions, visplanes
  thing_pixels, sprite_fragments, -- sprites
  fragment_union, resolved,       -- every candidate pixel, resolve for the nearest
  view_colored, ui_colored,       -- COLORMAP, status bar
  framebuffer AS ( ... )          -- 64,000 rows of (x, y, rgb)
SELECT string_agg(rgb, ''::bytea ORDER BY y, x) AS frame_rgb
FROM framebuffer;                  -- 192,000 bytes, one row
```

구현은 주석을 빼고 SQL 약 1,300줄이며 CTE 89개에 나뉘어 있다.
`linux_doom`의 렌더링 엔진은 주석을 빼고 약 3,300줄이라
SQLDoom의 약 2.5배라고 저자는 적었다.
마지막 `framebuffer`는 `(x, y, rgb)` 64,000행이고,
이를 `string_agg`로 이어 192,000바이트짜리 한 행으로 돌려준다.

### BSP 순회를 정렬 하나로

1993년에는 하드웨어 Z 버퍼가 없었으므로 Doom은 그리는 순서로 가림을 해결했다.
앞에서 뒤로 그리면서 이미 칠한 픽셀을 기록하고,
앞의 벽이 덮은 자리 뒤에 있는 것은 건너뛴다.
이 순서는 WAD에 미리 계산되어 들어 있는 BSP 트리가 준다.
트리의 노드마다 맵을 둘로 가르는 선이 있고, 잎은 볼록한 서브섹터이며,
각 노드에서 카메라 쪽 서브트리 전체가 반대쪽 서브트리보다
앞에 있다는 성질이 보장된다.
따라서 트리를 재귀로 내려가면 서브섹터의 앞뒤 순서를 얻는다.

SQLDoom은 로드 시점에 루트에서 각 서브섹터까지의 경로를 모두 미리 계산해 둔다.
현재 위치에서 경로의 각 단계는 앞(0) 아니면 뒤(1)이고,
이 결정을 bigint 하나에 비트로 담아 정렬하면 앞뒤 순서가 나온다.

```sql
SELECT ssector_id, ROW_NUMBER() OVER (ORDER BY sort_key) AS bsp_seq
FROM (
  SELECT st.ssector_id,
         -- back = 1 at bit (40 - depth), front = 0.
         SUM(CASE WHEN st.side = fs.front_side THEN 0::bigint
                  ELSE (1::bigint << (40 - st.depth)) END) AS sort_key,
         BOOL_AND(vc.keep) AS visible   -- was any parent bbox culled?
  FROM node_path_steps st -- materialized view, every root-to-ssector path
  JOIN nodes n ON ...
  CROSS JOIN LATERAL (SELECT ... AS front_side) fs -- on which side are we?
  JOIN visible_children vc ON ...
  GROUP BY st.ssector_id
) s WHERE s.visible;
```

깊이가 얕은 결정일수록 높은 비트에 놓이므로,
비트를 합한 값의 크기 순서가 곧 트리를 앞쪽 우선으로 내려간 순서다.
`SUM() ... ORDER BY` 하나가 재귀 하강 전체를 대신한다.
가장 깊은 BSP 트리는 E4M8의 32단계라서 40비트면 넉넉하다고 저자는 말한다.
WAD의 노드마다 자식 전체의 경계 상자가 있어서,
시야 절두체가 경계 상자 밖에 있음을 보이면 그 서브트리를 버릴 수 있다.
`BOOL_AND(vc.keep)`은 조상 중 하나라도 버려진 서브섹터를 걸러 낸다.
이후 파이프라인은 모두 `bsp_seq`에 조인하므로
보이는 서브섹터만 올바른 순서로 다룬다.

### 벽과 visplane

Doom은 3D처럼 보이지만 실제로는 수직 벽과 바닥에 평행한 천장만 있는 2.5D다.
그래서 벽을 앞에서 뒤로 칠하고, 남은 곳을 바닥이나 천장으로 칠하고,
항상 정면을 보는 납작한 스프라이트를 그리면 된다.
벽 하나는 연속된 화면 열을 차지하고 열 안에서는 연속된 픽셀 구간이므로,
`generate_series()`로 열과 행을 펼치면 픽셀 단위 행이 나온다.
원작은 `R_RenderSegLoop`와 `R_DrawColumn` 두 루프로 같은 일을 한다.
벽 렌더링은 평균 1.7 ms가 든다.

바닥과 천장, 즉 visplane은 SQL로 옮기기가 훨씬 까다롭다.
원작은 화면 열마다 한 칸씩 있는 `ceilingclip`, `floorclip` 두 배열을 두고,
벽을 칠할 때마다 아직 비어 있는 구간을 정확한 순서로 고쳐 나간다.
SQL에는 루프도 가변 상태도 없으므로, 저자는 정렬과 정렬된 구간 위의 집계를 쓴다.
열마다 앞에서 뒤로 정렬한 패널(한 열에 나타나는 벽의 한 부분) 목록이 있으면,
어떤 패널 직전의 클립 상태는 그 앞 행들만으로 정해지기 때문이다.

```sql
panel_clips AS (
  -- 1. the band as the NEARER panels left it
  SELECT p.*,
    COALESCE(MAX(CASE WHEN part IN ('solid','upper','upper_flush')
                      THEN y_bot::int + 1 END) OVER w, 0)            AS cc_before,
    COALESCE(MIN(CASE WHEN part IN ('solid','lower','lower_down')
                      THEN y_top::int - 1 END) OVER w, screen_h - 1) AS fc_before
  FROM panel_seq p
  WINDOW w AS (PARTITION BY col_x ORDER BY depth_x, bsp_seq, part, seg_id
               ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)
),
plane_spans_raw AS (
  -- 2. whatever the band leaves uncovered is a ceiling above the wall...
  SELECT col_x, fsec AS sector_id, f_ceil AS plane_z, 'ceil' AS plane,
         cc_before         AS y0,   -- from where nearer walls stopped
         f_ceil_y::int - 1 AS y1    -- down to this panel's own ceiling
  FROM panel_clips
  WHERE part IN ('solid','upper','upper_open','upper_flush')
    AND f_ceil_y::int - 1 >= cc_before          -- nothing left open: skip
  UNION ALL
  -- ...and a floor below it
  SELECT col_x, fsec, f_floor, 'floor',
         f_floor_y::int AS y0,      -- from this panel's own floor
         fc_before      AS y1       -- down to where nearer walls stopped
  FROM panel_clips
  WHERE ...
)
```

창 정의 `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`은 같은 열에서
자기보다 가까운 패널만 본다.
위쪽을 막는 패널의 아래 끝 중 최댓값이 `ceilingclip`,
아래쪽을 막는 패널의 위 끝 중 최솟값이 `floorclip` 역할을 한다.
그다음 이전 패널이 멈춘 곳부터 이번 패널의 천장까지를 천장으로,
이번 패널의 바닥부터 이전 패널이 멈춘 곳까지를 바닥으로 칠한다.
저자는 이것을 가난한 사람의 루프라고 부르며,
명령형 알고리즘을 집합 기반으로 위장한 꽤 꼼수 같은 방법이라고 인정한다.
바닥, 천장, 하늘 렌더링은 보통 약 3 ms가 든다.

### 깊이 해소, 가장 비싼 단계

벽, visplane, 스프라이트 단계는 실제로 아무것도 그리지 않고
`(x, y, depth, colour)` 형태의 후보만 낸다.
SQLDoom은 원작의 고정소수점 연산을 구현하지 않았으므로 벽, 바닥,
하늘 후보가 겹칠 수 있고, 스프라이트는 벽에 일부 가려질 수 있다.
원작은 이런 일이 생기지 않도록 정교하게 순서를 맞춰 Z 버퍼링을 피했는데,
저자는 그 안무를 SQL로 재현하려다 실패하고
모든 후보를 만든 뒤 승자를 고르는 무차별 방식을 택했다.

```sql
((LEAST(depth, 131071.0) * 4096)::bigint << 34) -- depth, clamped to 17.12 fixed-point
| ((2 - surface_priority) << 32)                -- wall > sprite > plane
| (LEAST(source_priority, 3) << 30)
| ((stable_id + 32768) << 14)                   -- stable tiebreak
| (light_index << 8) | palette_index            -- the payload
AS winner_key
...
SELECT pix, MIN(winner_key) FROM ranked_fragments GROUP BY pix
```

BSP 순서와 같은 기법이다.
깊이를 17.12 고정소수점으로 바꿔 가장 높은 비트에 두고,
그 아래에 표면 우선순위(벽, 스프라이트, 평면 순), 출처 우선순위,
안정적인 동점 처리용 id를 둔다.
맨 아래 14비트에는 조명 인덱스와 팔레트 인덱스라는 실제 색 정보가 들어간다.
픽셀마다 `MIN(winner_key)` 하나만 구하면 가장 가까운 후보가 정해지고,
색이 키 안에 함께 들어 있으므로 다시 조인할 필요도 없다.
그래도 이 단계가 가장 비싸서 평균 8.2 ms, 프레임 전체 시간의 3분의 1이 넘는다.
저자는 바로 이것이 John Carmack이 피한 일이며,
이제는 SQL로도 35 FPS를 낼 만큼 기계가 빨라졌다고 말한다.

저자의 노트북(Ryzen 7 PRO 7840U)에서는 보통 약 60 FPS가 나오고,
아주 붐비는 장면에서는 35 FPS까지 떨어진다.
가장 비싼 부분은 반복 알고리즘을 흉내 내는 visplane, 원작은 아예 피한 깊이 해소,
그리고 컬러맵 조회와 프레임 버퍼 묶기처럼 픽셀마다 해야 하는 일이다.

### 데이터베이스가 정말 잘 맞는 곳

저자는 Doom을 데이터베이스에서 렌더링하는 것은
분명 나쁜 생각이라고 인정하면서도,
데이터베이스가 실제로 잘 맞는 영역이 있다고 주장한다.

첫째는 모든 것이 데이터라는 점이다.
플레이어의 샷건은 `weapon_defs` 테이블의 한 행이고,
펠릿 7개가 각각 3d5 피해를 준다.
발사 애니메이션도 `weapon_frames` 테이블의 12행짜리 상태 기계다.
그래서 모드를 만들기가 아주 쉽고, 저자는 화면을 보며
샷건이 펠릿 500개를 더 넓게 쏘도록 바꾸는 영상을 보여 준다.
JSON 같은 파일에 두었다면 수정 시점에 제약 조건이 검증되지 않고,
바뀐 값을 반영하려면 다시 불러와야 한다고 덧붙인다.

둘째는 멀티플레이어가 거의 공짜라는 점이다.
인증, 동시성 제어, 접근 제어, 일관된 게임 상태 스냅샷,
바이너리 와이어 프로토콜을 데이터베이스가 이미 준다.
별도의 Python 심판(referee) 스크립트가 공유 35 Hz 시계를 돌리고 맵을 순환시키며,
플레이어 클라이언트는 입력만 넣는다.
저자가 가장 좋아하는 부분은 원자성이다.
틱마다 트랜잭션을 시작하고 끝에 커밋하므로,
모든 플레이어는 틱 이전이나 이후의 세계만 보고 반쯤 적용된 갱신은 보지 않는다.

접근 제어도 깔끔하다.
SQLDoom에는 테이블 약 110개와 함수 100여 개가 있지만,
네 플레이어 역할은 몇 개의 API 함수로만 게임에 접근하고
나머지 권한은 모두 회수된다.

```sql
CREATE OR REPLACE FUNCTION api_input(
  p_fwd real, p_strafe real, p_run boolean, p_turn real,
  p_fire boolean, p_weapon integer, p_use boolean) RETURNS integer
LANGUAGE cedarscript SECURITY DEFINER AS $doom$
INSERT INTO mp_inputs
SELECT mp.map_id, mp.player_thing_id,
       LEAST(1.0, GREATEST(-1.0, COALESCE(p_fwd, 0)))::real,
       LEAST(1.0, GREATEST(-1.0, COALESCE(p_strafe, 0)))::real,
       [...]
FROM mp_players mp WHERE mp.role_name = session_user::text;
return 1;
$doom$;
```

`SECURITY DEFINER` 함수는 테이블을 바꿀 수 있지만
플레이어는 함수를 호출할 수만 있다.
플레이어가 줄 수 있는 값은 전진, 옆걸음, 달리기, 회전, 발사, 무기 선택,
사용(스페이스바) 일곱 가지뿐이고, 함수가 입력을 허용 범위로 잘라 내므로
입력값을 믿을 필요도 없다.
어느 플레이어인지는 `session_user`로 정한다.
클라이언트당 3코어면 안정적인 35 FPS가 나오고,
틱 드라이버용 코어 하나를 더하면 16코어 기계로
원작의 `-altdeath` 데스매치를 돌릴 수 있다고 한다.

### 컴파일된 SQL과 원작 C

CedarDB는 복잡한 쿼리를 여러 단계를 거쳐 LLVM IR로 내리고 기계어로 컴파일한다.
저자는 오브젝트 이동과 운동량 처리를 두고
원작 C의 컴파일 결과와 SQLDoom의 생성 코드를 비교했다.
일대일 비교는 아니지만 C는 명령어 48개, SQLDoom은 117개였고,
늘어난 명령어 중 42개는 결과를 다시 테이블에 저장하는 코드였다.
저자는 SQL과 CPU 사이에 보통 있는 추상화 계층을 생각하면
차이가 놀랍도록 작다고 평가한다.

마지막으로 저자는 DOOMQL과 SQLDoom을 나란히 놓는다.
같은 엔진, 같은 제약(SQL을 넣고 비트맵을 받는다) 아래에서
레이캐스팅은 SQL로 표현하기 쉽고 단계 사이 의존성이 적어
집합 기반 처리에 더 잘 맞는다.
그런데도 BSP 방식의 SQLDoom이 훨씬 빠르고 화질도 훨씬 좋다.
가장 잘 맞아 보이는 방식이 늘 최선의 결과를 내지는 않으며,
그 차이는 John Carmack이 486에서 얼마나 많은 것을 끌어낼지
깊이 고민한 덕분이라는 것이 글의 결론이다.
저자는 DOOMQL 시절보다 CedarDB 자체도 빨라졌고 그때는
역할 기반 접근 제어도 없었다고 덧붙인다.

직접 돌리려면 CedarDB Community Edition, psycopg2와 pygame이 있는 Python,
그리고 Doom IWAD가 필요하다.
셰어웨어 `doom1.wad`는 자유롭게 재배포할 수 있어 에피소드 1을 하기에 충분하다.
README에 따르면 SQLDoom은 Postgres 와이어 프로토콜로 데이터베이스와 통신하고,
일부 함수가 cedarscript를 쓰기 때문에 현재는 CedarDB가 필요하지만
PL/pgSQL로 쉽게 옮길 수 있다고 한다.
이 문서를 쓰면서 SQLDoom을 직접 실행하거나 공개 서버에 접속해 보지는 않았다.

## 분석

### 루프를 값으로 바꾸는 세 가지 기법

이 글에서 가장 옮겨 쓸 만한 것은 Doom 자체보다
명령형 알고리즘을 집합 연산으로 바꾸는 방법이다.
SQLDoom의 렌더러는 서로 다른 세 문제를 사실상 하나의 기법으로 푼다.
순서가 중요한 계산을 만나면, 그 순서를 값 하나에 담고 그
값 위에서 정렬하거나 집계한다.

BSP 순회에서는 경로의 앞뒤 결정을 비트로 담아 `SUM`한 값이 순서가 된다.
visplane에서는 가까운 순서로 정렬한 창 위의
`MAX`, `MIN`이 원작에서 배열을 고쳐 가던 상태를 대신한다.
깊이 해소에서는 깊이와 우선순위와 색을 한 bigint에 담아
`MIN`이 승자 선택과 결과 조회를 한꺼번에 한다.
세 경우 모두 재귀나 루프의 상태가 정렬 키로 바뀌고,
상태 변경은 집계 함수로 바뀐다.

이 기법이 통하는 조건도 분명하다.
다음 단계의 상태가 앞선 원소들의 결합적인 집계로 표현될 때만
창 함수나 집계로 바꿀 수 있다.
visplane이 통한 것은 `ceilingclip`이 지금까지 본 패널 아래 끝의
최댓값이기 때문이다.
원작이 깊이 해소를 피하려고 쓴 정교한 순서 제어는 앞선 결과에 따라
다음에 무엇을 할지가 달라지는 계산이라 이 틀에 들어가지 않았고,
저자는 결국 무차별 방식으로 돌아갔다.
글 전체가 어떤 명령형 알고리즘이 집합 연산으로 옮겨지고 어떤 것은
옮겨지지 않는지의 경계를 보여 주는 셈이다.

### 틱과 프레임의 분리는 데이터베이스의 쓰기와 읽기 분리와 겹친다

SQLDoom의 구조는 게임 엔진으로 보면
고정 시간 간격 갱신과 가변 렌더링의 분리이고,
데이터베이스로 보면 트랜잭션 쓰기와 스냅샷 읽기의 분리다.
게임 로직은 35 Hz로 상태 테이블을 고치는 쓰기 트랜잭션이고,
렌더러는 그 상태를 읽기만 하는 순수 함수다.
이 둘이 정확히 겹치기 때문에 원자성과 일관된 스냅샷이라는
데이터베이스의 기본 성질이 그대로 게임의 성질이 된다.

원작 Doom은 틱마다 한 프레임만 그렸으니 이런 분리가 필요 없었다.
SQLDoom이 그리기를 분리한 이유는 표면적으로는 부드러운 화면이지만,
구조적으로는 읽기 쿼리가 쓰기 트랜잭션을 기다리지 않게 하려는 선택으로 읽힌다
(이 부분은 해석이다).
글에서 렌더러를 게임 상태 테이블의 순수 함수라고 부르는 것도 같은 맥락이다.

멀티플레이어에서도 같은 구조가 쓰인다.
플레이어는 `mp_inputs`에 입력 행을 추가할 뿐이고,
세계를 고치는 쓰기는 심판 하나가 틱 트랜잭션으로만 한다.
쓰기 주체가 하나이므로 여러 클라이언트가 같은 행을 동시에 갱신하며
생기는 충돌이 구조적으로 줄어든다.
noduerme는 2010년에 만든 카지노 게임에서 모든 원격 호출이
SQL 테이블의 게임 상태를 직접 갱신하게 했더니
초반의 교착 상태가 끔찍했고 확장이 악몽이었지만,
모든 것이 원자적이라 상태를 잃지는 않았다고 회고했다.[^noduerme]
SQLDoom은 그 경험의 반대편에 있는 설계로 보인다.
입력은 추가만 하는 큐로, 상태 변경은 단일 작성자의 트랜잭션으로 나누면
원자성은 유지하면서 교착 상태의 원인을 줄일 수 있다.
vovavili는 같은 댓글에 Designing Data-Intensive Applications의
트랜잭션 동시성 장을 권했다.[^vovavili]

### 데이터 주도 설계가 SQL에서 자연스러워지는 이유

저자가 ECS 패턴이 SQL에서 비로소 이해되었다고 말한 대목은
가볍게 넘길 일이 아니다.
ECS의 핵심은 엔티티를 객체가 아니라 컴포넌트 배열의 인덱스로 보고,
시스템이 필요한 컴포넌트를 가진 엔티티만 골라 일괄 처리하는 것이다.
이것은 관계형 모델에서 테이블과 조인으로 거의 그대로 표현된다.
몬스터 AI 쿼리가 몬스터 하나씩이 아니라 행 집합 전체에
`CASE` 하나로 다음 상태를 정하는 모습이 그 예다.

샷건의 정의와 애니메이션이 테이블 행이라는 점도 같은 흐름이다.
원작 Doom도 무기와 몬스터의 상태를 C 배열로 된 상태 테이블(`info.c`)에 두었으니,
저자가 한 일은 원작이 이미 데이터로 다루던 것을
진짜 데이터베이스로 옮긴 것에 가깝다
(원작 구조에 대한 이 설명은 글에 없는 배경이다).
그 결과 모드는 `UPDATE` 한 줄이 되고, 수정은 제약 조건 검사를 거치고,
실행 중에 바로 반영된다.

`game/bevy.md`에서 다룬 Bevy처럼
데이터 주도 게임 엔진들이 ECS를 앞세우는 흐름과 비교하면,
SQLDoom은 그 아이디어를 끝까지 밀어
저장소와 실행 엔진까지 데이터베이스로 바꾼 실험으로 볼 수 있다.

### 이 글은 CedarDB의 성능 시연이기도 하다

글의 표면은 재미있는 해킹이지만, 거의 모든 장이 CedarDB의 특성으로 돌아온다.
쿼리를 LLVM으로 컴파일하는 엔진이라는 점, C와 명령어 수를 비교한 장,
DOOMQL 이후 엔진이 빨라지고 역할 기반 접근 제어가 생겼다는 언급이 그렇다.
d--b는 HN에서 이를 잘 만든 광고라고 부르며,
SQL 데이터베이스 시장에서 눈에 띄기 어려운데 확실히 주목을 끌었다고
평했다.[^d--b]
vovavili는 Postgres 호환 HTAP 시스템을 찾던 중이었는데 LLM들이 아직 CedarDB를
모르더라며, 이 사람들은 게임을 안다고 화답했다.[^vovavili-cedardb]

저장소의 `MULTIPLAYER.md`는 이 시연이 실제로 엔진을 시험하는
부하였다는 사실을 보여 준다.
96코어 EPYC 9654P에서 측정할 때, 렌더러가 열과 프레그먼트마다
텍스처 메타데이터를 조인하던 시절에는
프레임당 B-트리 점 조회가 58,000번 일어났다.
조회마다 공유 래치를 잡다 보니 여러 세션에서 래치가 코어 사이를 오가며
서버 전체가 초당 약 220프레임에서 막혔다.
같은 문서는 이 과정에서 CedarDB의 문제 두 가지를 찾았다고 적는다.
유휴 스케줄러 작업자가 파이프라인이 시작될 때마다 깨어나
각각 1.5%의 CPU를 쓰던 문제는 2026년 9월 7일 업스트림에서 고쳐졌고,
같은 작은 페이지를 읽는 세션이 많을 때는 점 조회마다 잡는
공유 래치가 한계가 된다는 것이다.
글은 이런 엔진 쪽 발견을 다루지 않지만, 장난처럼 보이는 작업이
데이터베이스 회사에게는 실제 부하 시험이었다는 점이
프로젝트의 진짜 무게일 수 있다.

## 비평

### 줄 수 비교는 같은 것을 세지 않는다

글은 두 번 줄 수를 근거로 든다.
게임 로직은 SQL 약 5,900줄로 원작 C 약 9,000줄보다 적고,
렌더러는 약 1,300줄로 `linux_doom`의 약 3,300줄보다 2.5배 적다는 것이다.
paul-vernon이 이 대목을 인용하며 감탄했고[^paul-vernon],
soltanov는 쿼리 플래너를 상태 기계로 남용하면서 원작 C보다 줄 수가 적다는 것이
최고의 공학적 직무 태만이라며 반어적으로 반겼다.[^soltanov]

그러나 두 숫자는 같은 일을 세지 않는다.
SQLDoom의 렌더러는 원작의 고정소수점 연산을 구현하지 않았고,
원작이 Z 버퍼 없이 해내려고 들인 정교한 순서 제어를 포기하고
무차별 깊이 해소로 대신했다.
원작 렌더러 코드 중 상당 부분은 바로 그 순서 제어와
1993년 하드웨어에서 빨리 돌기 위한 최적화에 쓰였을 것이다.
그 일을 빼고 같은 그림을 얻는 코드가 더 짧은 것은 놀랍지 않다.

또 SQL 쪽 줄 수에는 해시 조인, 정렬, 창 함수, 병렬 실행,
쿼리 컴파일러가 하나도 들어 있지 않다.
C 코드가 직접 하던 반복과 메모리 관리를 데이터베이스 엔진이 대신하므로,
공정한 비교라면 엔진의 복잡도도 어느 정도 셈에 넣어야 한다.
게다가 텍스트 안에서도 숫자가 흔들린다.
WAD 임포터는 본문에서 Python 약 1,000줄, README에서 약 1,300줄이고,
틱 예산 계산은 본문에서 `1000 ms × 35 Hz = 28.6 ms`라고 적혀 있지만
README처럼 나눗셈이어야 맞다.
줄 수는 표현력의 대략적인 인상으로만 읽어야 하며,
SQL이 C보다 간결한 범용 언어라는 근거로 쓰기는 어렵다.

### “원작처럼 느껴져야 한다”는 규칙은 검증되지 않았다

저자는 다섯 규칙 중 두 번째, 즉 진짜 Doom처럼 느껴져야 한다는 것을
가장 중요하다고 했다.
그런데 글이 이 규칙을 뒷받침하는 방법은 플레이 영상과
원작과 나란히 놓은 스크린샷 퀴즈뿐이다.
이동, 충돌, 무기 피해, 몬스터 AI가 원작과 같은 결과를 내는지는 보여 주지 않는다.

원작 Doom은 결정론적 엔진이라
입력 기록(데모)을 재생하면 같은 게임이 다시 펼쳐지고,
소스 포트들은 이 데모 호환성을 원작 재현의 기준으로 삼아 왔다
(이 배경은 글에 없는 내용이다).
SQLDoom의 README에도 결정론 검사가 있지만,
같은 입력을 두 번 넣으면 같은 세계 해시가 나오는지 보는 자기 일관성 검사이지
원작과의 일치 검사가 아니다.
README는 피해 계산에 고정소수점을 쓰고
게임 상태에서 시드를 얻는 결정론적 난수를 쓴다고 설명하지만,
원작의 난수 테이블과 같은 순서로 난수를 소비하는지는
글과 README 어디에도 나오지 않는다.

렌더러가 원작의 고정소수점 연산을 구현하지 않았다는 사실도 이 규칙과 긴장한다.
그 때문에 원작에서는 생기지 않는 후보 겹침이 생기고,
이를 무차별 깊이 해소로 덮는다.
결과 그림이 비슷하다는 것과 원작의 동작을 옮겼다는 것은 다른 주장이며,
글은 앞의 것을 보여 주고 뒤의 것을 제목으로 내건다.

### 이식성은 말만 있고 근거가 없다

island_dev는 README상 CedarDB Community Edition이 필요하다는데
다른 데이터베이스에서도 동작하는지,
CedarDB 고유 기능을 쓰는지 물었다.[^island_dev]
스레드에서 이 질문에 대한 답은 달리지 않았고,
README는 cedarscript 때문에 지금은 CedarDB가 필요하지만
PL/pgSQL로 쉽게 옮길 수 있다고만 말한다.

그런데 글이 보여 준 틱 함수는 `let mut`, 중괄호 블록,
문장 단위 함수 호출을 쓰며 PL/pgSQL과 문법이 상당히 다르다.
더 큰 문제는 성능이다.
SQLDoom이 게임이 되는 이유는
89개 CTE짜리 쿼리가 프레임 예산 안에 끝나기 때문이고,
글의 마지막 장은 그것이
CedarDB가 쿼리를 기계어로 컴파일하기 때문이라고 설명한다.
같은 쿼리가 해석형 실행기를 쓰는 다른 데이터베이스에서
몇 FPS가 나오는지는 아무도 측정하지 않았다.
문법을 옮기는 일은 쉬울 수 있지만, 게임으로서 성립하는지는 엔진에 달려 있으므로
쉽게 옮길 수 있다는 말은 반쪽짜리 주장이다.

### 자동 병렬화라는 말과 저장소의 측정값 사이의 거리

저자는 몬스터를 하나씩 순회하는 대신 `UPDATE ... WHERE`를 쓰면
데이터베이스가 가장 좋은 적용 방법을 병렬로 자동으로 찾아 준다고 말한다.
하지만 같은 저장소의 `MULTIPLAYER.md`는 결이 다른 이야기를 한다.
프레임 하나는 단일 스레드 CPU로 약 28 ms이고 병렬화로 줄어들지 않으며,
세션마다 `max_parallel_workers`를 4~8로 제한하는 것이 가장 좋고
기본값인 전체 코어 사용은
혼자 하는 클라이언트에게 3분의 1을 손해 본다고 적혀 있다.

글이 말하는 클라이언트당 3코어, 16코어 기계로 4인 데스매치라는 수치도
이 맥락에서 읽어야 한다.
작은 행 집합을 짧은 시간 안에 처리하는 게임 틱과 프레임에서는
병렬 실행의 조정 비용이 이득을 쉽게 넘어선다.
선언적으로 쓰면 병렬화는 공짜라는 인상은 분석용 대용량 쿼리에서 나온 직관이며,
지연 시간이 중요한 작은 쿼리에서는 오히려 조정해야 할 비용이 된다.
글은 이 미묘함을 저장소 문서에만 남기고 본문에서는 장점으로만 말한다.

## 인사이트

### 정렬 키에 결과를 함께 담는 기법은 업무 쿼리에서도 그대로 쓸 수 있다

깊이 해소의 `winner_key`는 SQL에서 흔히 부딪히는 문제의 일반적인 해법이다.
그룹마다 어떤 기준으로 최소인 행을 고르고 그 행의 다른 열을 가져와야 할 때,
보통은 창 함수로 순위를 매긴 뒤 다시 거르거나,
집계 후 원래 테이블에 다시 조인한다.
SQLDoom은 기준과 결과를 한 정수에 비트로 담아 `MIN` 하나로 끝내고,
다시 조인하지 않는다.

이 기법은 그룹별 최신 행, 여러 규칙 중 우선순위가 가장 높은 규칙 선택,
동점일 때 안정적인 순서 같은 업무 쿼리에 그대로 쓸 수 있다.
조건은 기준과 결과를 정해진 비트 폭 안에 넣을 수 있어야 하고,
기준이 단조로운 정수로 바뀌어야 한다는 것이다.
SQLDoom이 깊이를 17.12 고정소수점으로 바꾸고 131071.0에서 자른 것이
바로 그 비용이다.

대가는 가독성과 경계 조건이다.
비트 폭을 넘는 값은 조용히 다른 필드를 침범하고,
음수나 부호 있는 시프트는 엔진마다 다르게 동작할 수 있다.
그래서 이 기법은 SQLDoom처럼 픽셀 수만큼 반복되는 경로처럼
성능이 정말 중요한 곳에만 쓰고,
비트 배치를 주석으로 남겨 두는 편이 낫다.
SQLDoom의 코드가 각 시프트 옆에 무엇을 담았는지 적어 둔 것은 그 최소한의 예의다.

### 데이터베이스 게임 서버의 진짜 이점은 권한 모델에 있다

저자는 멀티플레이어의 장점으로 원자성을 가장 좋아한다고 했지만,
더 오래 남을 설계는 접근 제어 쪽이다.
`api_input`은 플레이어 슬롯을 인자로 받지 않고 `session_user`로 정한다.
`MULTIPLAYER.md`도 클라이언트가 다른 플레이어의 슬롯을 지정할 수 없는 이유를
인자 자체가 없기 때문이라고 설명한다.
보통의 게임 서버라면 패킷의 플레이어 id를 검증하는 코드를 짜야 하고,
그 검증이 빠지는 순간이 곧 취약점이 된다.

이 방식은 공격 표면을 함수 몇 개의 시그니처로 줄인다.
플레이어가 할 수 있는 일은 허용된 함수 호출과 몇 개의 `api_*` 뷰 조회뿐이고,
입력값은 함수 안에서 범위가 잘린다.
치트 방지가 별도 시스템이 아니라 권한 부여의 결과가 되는 것이다.

두 번째 효과는 관전과 분석이 공짜로 따라온다는 점이다.
공개 서버에서 자리가 없으면 SQL 콘솔로 진행 중인 경기를 조회할 수 있다는 기능은,
읽기 전용 역할 하나만 더 주면 되는 일이다.
일반 게임 서버라면 관전 모드, 통계 API, 리플레이 저장을 따로 만들어야 하는데,
상태가 이미 테이블에 있으니 질의 권한만 나누면 된다.
이 구조가 액션 게임에는 과하더라도, 턴제 게임이나 상태가 작은
실시간 협업 도구에는 진지하게 검토할 만한 패턴이다.

### 저장 프로시저 논쟁은 언어보다 도구의 문제로 옮겨 가고 있다

HN에서 가장 길게 이어진 토론은 Doom이 아니라
업무 로직을 데이터베이스에 둘 것인가였다.
bob1029는 반도체 공장에서
운영 의사결정 로직 대부분을 저장 프로시저와 SQL로 돌렸고,
수백 명이 같은 프로시저를 검토하고 변경을 제안했으며,
매일 아침 운영 DB를 복제해 실제 데이터로 실험했기에
테스트가 간단했다고 적었다.[^bob1029]
pak9rabid는 데이터 분석 플랫폼 로직의 약 95%를
데이터베이스 함수와 저장 프로시저로 구현했다고 했다.[^pak9rabid]
반대로 viraptor는 문자열 중심 타입과 빈약한 표준 라이브러리 환경에서
복잡한 로직을 짜는 것만큼 하기 싫은 일도 드물다고 했고[^viraptor],
jcmontx는 2010년대에 2000년대 레거시 앱의 저장 프로시저를 고치던 기억을 떠올리며
그 코드가 일반 코드처럼 다뤄지지 않았고
버전 관리도 되지 않았다고 썼다.[^jcmontx]
_heimdall은 데이터베이스 계층의 복잡한 업무 로직을 편하게 다룰 만큼
SQL을 잘 아는 사람을 한 손으로 꼽을 정도라고 했다.[^_heimdall]

반대 의견을 자세히 보면 대부분 SQL이라는 언어보다 주변 도구에 대한 불만이다.
버전 관리가 안 되고, 테스트가 어렵고, 편집기 지원이 약하고,
다룰 줄 아는 사람이 적다는 것이다.
SQLDoom 저장소는 이 불만 중 상당수에 대한 반례처럼 생겼다.
`sql/runtime/functions/26_cs_monsters.sql`,
`42_api.sql`처럼 번호 붙은 파일로 git에서 관리되고,
모든 맵을 도는 스모크 테스트와 결정론 검사와 권한 검사 스크립트가 있다.

beachy는 저장 프로시저를 오래 다룬 경험을 말하면서,
AI 덕분에 데이터베이스를 건드리는 코드가 폭발적으로 늘어나는 지금은
우회할 수 없는 데이터베이스 안에 로직과 제약을 두는 편이
더 말이 될 수 있다고 했다.[^beachy]
이것이 이 논쟁의 2차 효과다.
애플리케이션 코드를 쓰는 주체가 늘고 검증이 느슨해질수록,
마지막 방어선인 데이터베이스 제약과 권한의 가치는 올라간다.
SQLDoom의 `SECURITY DEFINER` 함수와 권한 회수는
게임이 아닌 곳에서도 같은 역할을 할 수 있다.

### “Doom이 돌아가는가”는 이제 엔진 부하 시험이다

“Doom이 돌아가는가”는 오랫동안 새 하드웨어나 플랫폼의
이식성을 증명하는 농담이었다.
SQLDoom은 이 농담을 데이터베이스의 실행 엔진에 적용하면서 성격을 바꾼다.
여기서 Doom은 이식성 시험이 아니라
짧은 지연 시간, 많은 세션, 작은 페이지에 집중된 조회라는
분석 벤치마크가 잘 다루지 않는 부하 모양을 만들어 낸다.
`MULTIPLAYER.md`에 남은 래치 경합과 유휴 작업자 문제가 그 증거다.

CedarDB 블로그에 “Introducing DoomBench - Can Your Data Stack Run DOOM?”이라는
제목의 글이 따로 있다는 점도 이 방향을 보여 준다(이 글의 내용은 읽지 않았다).
`sqlite/neural-network-in-sql.md`에서 다룬 SQL 신경망처럼,
데이터베이스를 범용 계산 엔진으로 밀어붙이는 데모는
엔진의 약점을 드러내는 시험대 역할을 한다.
Sharlin은 행렬 곱셈이 결국 교차 조인 위의 합계 집계라며
SQL을 CUDA 커널로 컴파일하는 플래너를 농담처럼 제안했고[^Sharlin],
thesz는 선형대수 식을 관계대수로 바꿔 최적화한 뒤 되돌려
실제로 속도를 높인 VLDB 논문을 소개했다.[^thesz]

여기서 얻을 수 있는 판단 기준은 데모를 볼 때 결과물보다
그 과정에서 엔진이 무엇을 고쳤는지를 보라는 것이다.
SQLDoom의 진짜 산출물은 플레이 가능한 Doom보다,
지연 시간이 중요한 작은 쿼리를 많이 돌릴 때
데이터베이스가 어디서 막히는지에 대한 측정 기록이다.
pavlov는 학습 데이터에 흔한 것을 학습 데이터에 흔한 언어로 만든 글이
AI 시대 화제성의 정점이라고 냉소했지만[^pavlov],
저장소의 측정 기록은 그런 재현으로는 얻을 수 없는 종류의 지식이다.

---

[^noduerme]: <https://news.ycombinator.com/item?id=49962015>

[^vovavili]: <https://news.ycombinator.com/item?id=49962637>

[^d--b]: <https://news.ycombinator.com/item?id=49961983>

[^vovavili-cedardb]: <https://news.ycombinator.com/item?id=49962758>

[^paul-vernon]: <https://news.ycombinator.com/item?id=49819304>

[^soltanov]: <https://news.ycombinator.com/item?id=49961500>

[^island_dev]: <https://news.ycombinator.com/item?id=49967714>

[^bob1029]: <https://news.ycombinator.com/item?id=49963076>

[^pak9rabid]: <https://news.ycombinator.com/item?id=49965359>

[^viraptor]: <https://news.ycombinator.com/item?id=49964160>

[^jcmontx]: <https://news.ycombinator.com/item?id=49964732>

[^_heimdall]: <https://news.ycombinator.com/item?id=49964425>

[^beachy]: <https://news.ycombinator.com/item?id=49968533>

[^Sharlin]: <https://news.ycombinator.com/item?id=49963944>

[^thesz]: <https://news.ycombinator.com/item?id=49974711>

[^pavlov]: <https://news.ycombinator.com/item?id=49970237>
