# APSW: SQLite를 숨기지 않고 전부 꺼내 주는 Python 래퍼

<https://rogerbinns.github.io/apsw/>

<https://github.com/rogerbinns/apsw>

HN 토론: <https://news.ycombinator.com/item?id=50045273> (84점, 25개 댓글)

## 소개

APSW는 Another Python SQLite Wrapper의 약자로,
Roger Binns가 2004년부터 관리해 온 Python용 SQLite 바인딩이다.
SQLite C API 전체와 Python C API를 이어 붙이고,
두 쪽의 새 버전을 계속 따라간다.
최신 릴리스는 3.53.4.0이며, 버전 번호 앞부분이 함께 묶인 SQLite 버전이다.
CPython 3.10부터 3.15까지 지원한다.

표준 라이브러리의 `sqlite3`와 APSW는 출발점이 다르다.
`sqlite3`는 DBAPI(PEP 249)를 지키려고
SQLite를 다른 데이터베이스처럼 보이게 만들고,
그 과정에서 SQLite의 특성 일부를 감춘다.
APSW는 SQLite가 다른 데이터베이스와 다르다는 사실을 감추지 않고,
SQLite에서 하던 방식 그대로 쓰게 한다.
문서는 다른 데이터베이스로 쉽게 갈아탈 수 있어야 하고
요구가 단순하다면 `sqlite3`를,
SQLite의 기능을 직접 쓰고 싶다면 APSW를 쓰라고 권한다.

HN에서 Retr0id는 APSW를 한 문장으로
“SQLite를 사랑하는 사람의 SQLite 라이브러리”라고 정리했다.[^Retr0id]

### 담고 있는 것

| 영역        | 내용                                                                          |
| ----------- | ----------------------------------------------------------------------------- |
| SQLite 기능 | 전문 검색(FTS5), Session 확장, 가상 테이블, VFS, BLOB I/O, 백업, JSON, CArray |
| 개발자 도구 | 셸, 실행·행 추적, 쿼리 정보, 결과 표 출력, SQLite 로그를 Python 로거로 전달   |
| 설정 도우미 | `apsw.bestpractice`로 권장 설정을 한 번에 적용                                |
| 비동기      | asyncio, trio, anyio 지원, 콜백도 async 함수로 작성 가능                      |
| 배포        | PyPI 빌드에 SQLite와 확장, 명령줄 도구까지 정적으로 포함, 타입 스텁 포함      |

라이선스는 zlib 계열의 자체 문구이며,
그 문구 대신 OSI가 승인한 아무 오픈소스 라이선스로 써도 된다고 명시한다.

## 동작 방식

### SQLite를 정적으로 품고 들어온다

PyPI에서 받는 APSW는 SQLite를 내부에 정적으로 포함한다.
시스템에 깔린 SQLite와 섞이지 않으므로
운영체제 배포판이 오래된 SQLite를 갖고 있어도
최신 SQLite를 쓸 수 있다.
PyPI 빌드에는 따로 컴파일해야 하는 SQLite의
추가 확장과 프로그램도 함께 들어 있다.
PyPI를 쓰지 않으면 빌드 옵션으로 SQLite를 세밀하게 조정할 수 있다.

배포판 패키지로도 받을 수 있다.
HN에서 a96이 Debian에도 패키지가 있다고 하자,
관리자 rogerbinns는 Linux와 BSD 계열 대부분에 패키지가 있고
Repology가 150여 개 배포판의 패키지 이름과 버전을
추적한다고 답했다.[^rogerbinns-repology]

### 뒤에서 아무 일도 하지 않는다

`sqlite3`는 DBAPI를 맞추려고
기본적으로 사용자의 SQL을 들여다보며 트랜잭션을 관리한다.
문서는 이 동작이 예상하지 못한 결과를 낳을 수 있다고 지적한다.
APSW는 SQL을 고치지 않고 SQLite에 그대로 넘긴다.

이 원칙이 드러나는 차이는 다음과 같다.

- 한 번의 `execute`에 세미콜론으로 이어진 여러 문장을 넣을 수 있고,
  `select`가 섞여 있어도 결과 행이 차례로 나온다.
  `sqlite3`의 `executescript`는 반환 데이터를 조용히 버린다.
- `Connection`을 컨텍스트 매니저로 쓰면 SQLite의 중첩 트랜잭션(savepoint)을 쓴다.
  `sqlite3`의 컨텍스트 매니저는 중첩을 지원하지 않는다.
- SQLite 오류 코드마다 대응하는 예외가 있고 확장 오류 코드도 준다.
  `sqlite3`는 여러 코드를 DBAPI 예외 몇 개로 묶는다.
- 사용자 정의 함수 안에서 난 Python 예외가 그대로 올라온다.
  `sqlite3`는 콜백의 예외를 삼키고
  “user-defined function raised exception”이라는 메시지만 남긴다.
- 같은 `Connection`을 추가 잠금 없이 여러 스레드에서 쓸 수 있다.
  `sqlite3`는 연결과 커서를 만든 스레드에서만 쓰게 한다.

### 동시성은 연결 단위의 뮤텍스로 정해진다

SQLite는 연결마다 뮤텍스가 하나 있다.
연결을 호출할 때 잡고 돌아올 때 놓으므로,
한 연결에 스레드를 더 붙여도 동시성은 늘지 않고 연결을 여러 개 열어야 한다.
APSW는 SQLite를 호출하는 동안 GIL을 풀어 다른 Python 코드가 돌 수 있게 한다.

비동기 모드에서는 연결마다 전용 작업 스레드가 하나 붙는다.
이벤트 루프에서 한 호출이 그 스레드로 넘어가고, 결과를 `await`로 받는다.
사용자 정의 함수, 가상 테이블, VFS, 각종 훅 같은 콜백이 async 함수라면,
작업 스레드가 그 코루틴을 이벤트 루프로 되돌려 보내고 결과가 올 때까지 기다린다.
`AsyncConnection` 같은 별도 클래스는 없고,
`Connection.as_async()`로 만든 연결과 그로부터 나온 커서,
BLOB, 백업 객체가 모두 비동기 모드가 된다.

## 사용하기

### 설치와 권장 설정

```bash
pip install apsw
```

```python
import apsw
import apsw.bestpractice

# 외래 키 활성화, 짧은 busy timeout, WAL, 큰따옴표 문자열 금지,
# 쿼리 플래너 통계 기록 등을 이후 열리는 모든 연결에 적용한다.
apsw.bestpractice.apply(apsw.bestpractice.recommended)

con = apsw.Connection("app.db")
print(apsw.sqlite_lib_version(), apsw.apsw_version())
```

`bestpractice`는 SQLite가 하위 호환 때문에
기본으로 켜 두지 못하는 설정을 대신 켠다.
개별 함수만 골라 적용할 수도 있다.

### 여러 문장, 중첩 트랜잭션, 예외

```python
import apsw

con = apsw.Connection(":memory:")

# 세미콜론으로 이은 여러 문장과 바인딩을 한 번에 실행하고, select 결과를 순서대로 받는다.
for row in con.execute(
    "create table foo(x, y, z);"
    "insert into foo values (?, ?, ?);"
    "insert into foo values (?, ?, ?);"
    "select * from foo;",
    (1, 2, 3, 4, 5, 6),
):
    print(row)  # (1, 2, 3) 다음 (4, 5, 6)

# with 블록이 중첩되면 바깥은 트랜잭션, 안쪽은 savepoint가 된다.
with con:
    con.execute("insert into foo values (7, 8, 9)")
    try:
        with con:
            con.execute("insert into foo values (10, 11, 12)")
            raise RuntimeError("안쪽만 되돌린다")
    except RuntimeError:
        pass
print(con.execute("select count(*) from foo").get)  # 3

# 사용자 정의 함수의 예외가 원래 타입과 스택 그대로 올라온다.
def badfunc(t):
    return 1 / 0

con.create_scalar_function("badfunc", badfunc, 1)
try:
    con.execute("select badfunc(3)").get
except ZeroDivisionError as e:
    print("원인 그대로:", e)
```

### 비동기 연결

```python
import asyncio
import apsw

async def main():
    db = await apsw.Connection.as_async(":memory:")
    await db.execute("create table item(name, price)")
    await db.execute("insert into item values ('a', 1), ('b', 2)")
    # execute를 await해서 커서를 받고, async for로 행을 순회한다.
    async for name, price in await db.execute("select name, price from item"):
        print(name, price)
    await db.aclose()

asyncio.run(main())
```

비동기 모드에서는 `Connection.authorizer` 같은 속성도 `await`해야 하고,
값을 바꿀 때는 `await db.async_run(setattr, db, "authorizer", fn)`처럼
작업 스레드에서 실행한다.
포함된 타입 스텁이 어느 API를 기다려야 하는지 IDE에 알려 준다.

## 값 정하기

| 항목                       | 값                                  | 근거와 조정 방법                                        |
| -------------------------- | ----------------------------------- | ------------------------------------------------------- |
| 지원 Python                | 3.10~3.15                           | APSW는 개발 중인 Python 버전도 따라간다                 |
| busy timeout(bestpractice) | 100ms                               | 다른 연결이 잠그고 있을 때 바로 `BusyError` 대신 재시도 |
| 연결 수                    | 동시에 일할 단위마다 하나           | 한 연결 안의 동시성은 뮤텍스 하나로 묶인다              |
| 비동기 작업 스레드         | 연결마다 하나                       | 연결을 많이 열면 스레드도 그만큼 늘어난다               |
| 테스트 커버리지(문서 기준) | APSW 99.6%, `sqlite3` C 코드 약 81% | 메모리 부족 같은 실패 경로까지 시험한다                 |

APSW는 `sqlite3`보다 빠르다고 주장하며,
Python에서 C로, C에서 Python으로 가는 호출을
모두 fastcall로 구현한 것을 이유로 든다.
직접 확인하려면 포함된 speedtest 벤치마크를 돌려 본다.

## 트레이드오프

### DBAPI 이식성을 버리지만, 그 이식성은 원래 생각보다 얇다

`sqlite3`가 APSW보다 나은 점으로 문서가 드는 것은 하나다.
표준 라이브러리에 있고,
데이터베이스 계층을 추상화하는 라이브러리들이 널리 지원한다.
ORM이나 DBAPI를 전제로 한 도구를 쓴다면 APSW로 바꿀 수 없다.

그러나 DBAPI가 주는 이식성은 기대보다 작다.
somat은 PostgreSQL 위주로 쓰던 프로그램에 SQLite 선택지를 붙이면서
SQL 방언 차이는 차치하고도
파라미터 표기(`%(name)s`와 `:name`)를 바꾸는 변환기를 따로 짜야 했고,
커서 대신 연결에 컨텍스트 매니저를 걸어야 하는 차이,
행을 딕셔너리로 받는 방법의 차이를 하나씩 맞춰야 했다고 적었다.[^somat]
DBAPI를 따른다고 해서 데이터베이스를 바꾸는 일이 쉬워지지는 않는다면,
그 대가로 SQLite의 기능을 포기하는 계산은 다시 해 볼 만하다.

중간 길도 있다.
cleifer는 표준 라이브러리의 사용법에 익숙하면서 합리적인 트랜잭션 의미론과
암호화 같은 자체 SQLite 정적 링크가 필요하다면
자신이 만든 cysqlite를 쓸 수 있다고 소개했다.
성능은 표준 라이브러리보다 낫지만 APSW만큼은 아니라고 직접 밝혔다.[^cleifer]
반대쪽에서 jph00은 사용하기 편한 API를 원하는 사람을 위해
sqlite-utils를 APSW 위로 옮긴 apswutils를 만들어
1~2년째 쓰고 있다고 했다.[^jph00]

### SQLite를 품는 대가로 한 프로세스에 SQLite가 둘이 될 수 있다

정적으로 포함된 SQLite는 시스템 SQLite와 무관하게 최신 기능을 준다.
그런데 같은 프로세스에서
다른 모듈이 시스템 SQLite로 같은 데이터베이스 파일을 열면 문제가 생긴다.
문서는 Windows가 아닌 플랫폼에서 서로 다른 SQLite 라이브러리 두 개로
같은 데이터베이스를 여는 것이 안전하지 않다고 경고한다.
`sqlite3`와 APSW를 한 프로세스에서 섞어 쓰는 코드,
특히 같은 파일을 여는 코드는 피해야 한다.

### SQLite를 빠르게 따라가는 만큼 호환이 깨지는 변경도 따라온다

APSW는 SQLite의 변화를 거의 그대로 반영한다.
변경 이력에는 하위 호환이 깨지는 항목이 자주 나온다.
3.53.3.0에서는 SQLite가 일부 API에 데이터베이스 뮤텍스를 요구하게 되면서
비동기 모드의 `changes()`, `last_insert_rowid()`,
`in_transaction` 등을 `await`해야 하게 바뀌었다.
3.52.0.0은 권장 컴파일 옵션을 따르면서 BLOB에 대한 `LIKE` 매칭을 막았고,
`apsw.config()`를 다른 무엇보다 먼저 부르던 코드의 동작도 바꾸었다.
SQLite의 closure 확장이나 `sqlite3_scrub` 바이너리처럼
SQLite 쪽에서 빠진 것은 APSW에서도 빠진다.
최신을 얻는 대신 버전을 올릴 때마다 변경 이력을 읽는 비용을 치러야 한다.

### 비동기는 완전하지만 free-threaded Python은 아직이다

비동기 지원은 콜백까지 async로 쓸 수 있을 만큼 넓지만,
연결마다 작업 스레드를 하나 두는 방식이라 연결 수가 곧 스레드 수다.
Python 3.14의 free-threaded 빌드에는 아직 대응하지 않았다(APSW issue 568).
PyPI에 free-threaded 빌드가 있지만 모듈을 불러오면 GIL이 다시 켜지고,
`-X nogil`로 강제하면 같은 객체를 여러 스레드에서
동시에 바꿀 때 크래시가 날 수 있다.

## 함정

- 결과 행이 없는 쿼리는 커서가 바로 소진되어 정리되므로 커서에서 열 이름을 얻기 어렵다.
  HN에서 dex0shubham이 이 문제를 묻자 rogerbinns는
  쿼리를 실행하지 않고 정보만 얻는 `apsw.ext.query_info`를 쓰라고 답했다.
  내부적으로 실행 추적기로 정보를 기록한 뒤 실행을 중단하는 방식이다.[^rogerbinns-query-info]
- `sqlite3`에서 넘어오면 트랜잭션이 자동으로 시작되지 않는다는 점을 잊기 쉽다.
  쓰기 묶음은 `with con:` 블록으로 명시한다.
- 비동기 연결에서 `Cursor.description`처럼 값으로 바뀐 속성을 `await`하거나,
  반대로 `await`가 필요해진 속성을 그냥 읽는 실수가 버전마다 생길 수 있다.
  타입 스텁과 변경 이력을 함께 확인한다.
- `bestpractice`는 큰따옴표로 감싼 문자열을 오류로 만든다.
  기존 SQL에 `"문자열"` 표기가 섞여 있으면 적용 직후 깨진다.
- 시스템 SQLite에 의존하는 다른 라이브러리와 같은 파일을 한 프로세스에서 열지 않는다.

## 확인하기

```bash
pip install apsw

# 포함된 SQLite 버전과 컴파일 옵션 확인
python3 -c "import apsw; print(apsw.sqlite_lib_version()); print(apsw.compile_options)"

# APSW 셸 실행(SQLite 셸과 비슷한 명령을 제공한다)
python3 -m apsw app.db

# sqlite3와의 속도 비교
python3 -m apsw.speedtest --help
```

예외 전달 차이는 위 `badfunc` 예제를 `sqlite3`로 바꿔 돌려 보면 바로 보인다.
`sqlite3`는 `OperationalError`만 내고,
APSW는 `ZeroDivisionError`와 원래 스택을 준다.

## 체크리스트

- [ ] ORM이나 DBAPI 전제 도구 없이 SQL을 직접 쓰는 프로젝트인가
- [ ] `apsw.bestpractice.recommended`를 앱 시작 시 적용하는가
- [ ] 쓰기 묶음을 `with con:` 블록으로 감쌌는가
- [ ] 같은 프로세스에서 `sqlite3`와 APSW가 같은 파일을 열지 않는가
- [ ] 동시 작업 수에 맞춰 연결을 나눴는가
- [ ] APSW를 올릴 때 변경 이력의 호환성 깨짐 항목을 확인했는가
- [ ] free-threaded Python에서 돌리지 않는가

## 기억할 원칙

### 감추는 추상화보다 드러내는 래퍼가 오래 간다

APSW가 20년 넘게 유지된 이유는 SQLite를
다른 무엇처럼 보이게 하지 않았기 때문이다.
감추는 추상화는 감춘 부분이 문제를 일으킬 때 디버깅을 어렵게 하고,
그 부분이 바뀔 때마다 추상화 쪽도 함께 흔들린다.
드러내는 래퍼는 SQLite의 문서가 곧 사용법이 되고,
SQLite가 새 기능을 내면 그대로 따라가면 된다.
HN에서 arc-in-space가 `sqlite3`의 특이한 동작을 파악하느라 애먹다가
APSW로 바꾸자 기대한 대로 동작했다고 한 경험도 같은 이야기다.[^arc-in-space]

### 데이터베이스가 필요해지는 순간은 기능에서 온다

rogerbinns는 처음에 Python 딕셔너리를 파일로 덤프해 쓰다가,
실행 취소와 특정 시점의 데이터 보기를 만들려다 데이터베이스로 옮겼다고 회고했다.
트리거로 이전 값을 자동 저장하고
뷰로 보기 좋게 꺼내야 했기 때문이다.[^rogerbinns-origin]
파일로 충분하다는 판단은 데이터가 아니라 기능이 바꾼다.
변경 이력, 동시 접근, 부분 갱신 같은 요구가 생기는 시점이
SQLite로, 그리고 SQLite를 제대로 쓰는 래퍼로 옮겨 갈 때다.

---

[^Retr0id]: <https://news.ycombinator.com/item?id=50046583>

[^rogerbinns-repology]: <https://news.ycombinator.com/item?id=50056178>

[^somat]: <https://news.ycombinator.com/item?id=50049871>

[^cleifer]: <https://news.ycombinator.com/item?id=50050190>

[^jph00]: <https://news.ycombinator.com/item?id=50048185>

[^rogerbinns-query-info]: <https://news.ycombinator.com/item?id=50056346>

[^arc-in-space]: <https://news.ycombinator.com/item?id=50046251>

[^rogerbinns-origin]: <https://news.ycombinator.com/item?id=50056474>
