# PostgreSQL의 MVCC는 나쁘다, 그리고 다른 DB도 마찬가지다

원문: [PostgreSQL's MVCC is bad. So is everyone else's.](https://boringsql.com/posts/mvcc-bad-bad/)

HN 토론: <https://news.ycombinator.com/item?id=49098417> (34점, 22개 댓글)

Lobsters 토론: <https://lobste.rs/s/vjelns>

## 요약

PostgreSQL을 싫어하는 사람들이 가장 먼저 배우는 사실은 “MVCC가 나쁘다”는 것이다.
테이블이 두 배로 부풀고, 32-bit 트랜잭션 카운터가 한계에 부딪히며, VACUUM과의
끝없는 씨름과 dead tuple이 그 증거로 제시된다.
2016년 Uber는 쓰기 증폭을 측정한 뒤 MySQL로 떠났고, Andy Pavlo의 연구 그룹은
MVCC를 PostgreSQL에서 가장 싫어하는 부분이라고 불렀다.
저자는 이 비판이 과장이 아니라고 인정하면서도, 이것이 결함(defect)이 아니라
설계 선택(design choice)에서 비롯된다고 짚는다.
그리고 비판이 항상 한 가지 질문을 빼먹는다고 지적한다.
“무엇과 비교해서?”

저자는 reader가 writer를 막지 않으려면 어떤 DB든 과거 버전을 어딘가에
보관해야 하며, 그런 엔진은 모두 네 가지 질문에 답해야 한다고 정리한다.
과거 버전은 어디에 사는가(테이블 안인가 별도 구조인가), version chain은
어느 방향을 가리키는가(old에서 new인가 new에서 old인가), index는 무엇을
가리키는가(물리적 위치인가 논리적 키인가), 누가 언제 정리하는가(나중에
백그라운드 프로세스인가 트랜잭션 자신인가)이다.
PostgreSQL의 답은 테이블 안, old에서 new, 물리적 위치(ctid), 나중에
백그라운드 프로세스이다.
비판받는 모든 비용은 이 네 가지 답에서 파생된다.

글은 PostgreSQL 19 beta2에서 네 가지 혐의를 직접 재현한다.
쓰기 증폭에서는 100만 row 테이블에서 index가 없는 쪽은 row당 약 3.0개의
WAL record(36MB)를, secondary index가 4개인 쪽은 7.1개(69MB)를 만들었다.
바꾼 컬럼(`last_seen`)이 어떤 index에도 없는데도 row가 물리적으로 이동하면서
모든 index가 새로 쓰였기 때문이다.
HOT(Heap-Only Tuple) 업데이트는 이를 완화하지만 `fillfactor=70`에서도
첫 배치는 42% HOT에 그쳤고 재실행 후에야 66%까지 올라갔다.
테이블 팽창에서는 100만 row를 UPDATE한 뒤 ROLLBACK했는데도 테이블이 89MB에서
178MB로 커지고 100만 개의 dead tuple이 남았다.
정작 rollback 자체는 0.124ms에 끝났다.
새 버전을 버리기만 하면 되기 때문이다.
오래 열린 `REPEATABLE READ` 트랜잭션 하나는 database-wide `xmin` horizon을
붙잡아 VACUUM이 dead tuple을 제거하지 못하게 만들었고, 32-bit XID는 약 40억
트랜잭션마다 wraparound를 막기 위해 손대지 않은 페이지까지 freeze로 다시
쓰게 만든다.

이어서 저자는 다른 엔진들이 같은 네 질문에 어떻게 답하는지 비교한다.
Oracle과 InnoDB는 과거 버전을 테이블 밖 undo log에 두고 in-place로 업데이트해
heap bloat와 대부분의 쓰기 증폭을 피하지만, rollback을 실행 시간만큼(때로는 그
이상) 되감아야 하고, 과거 버전 read는 undo chain을 따라 재구성해야 하며, undo가
재사용된 뒤라면 Oracle은 `ORA-01555: snapshot too old`로 쿼리를 죽인다.
SQL Server는 버전을 `tempdb`의 version store에 두어 인스턴스 전체가 위험에
노출되며, 2019년 Accelerated Database Recovery(ADR)로 PostgreSQL이 처음부터
공짜로 가졌던 상수 시간 abort를 뒤늦게 엔지니어링으로 확보했다.
MongoDB의 WiredTiger는 버전을 캐시에 두어 오래된 snapshot이 history store를
부풀리고, CockroachDB 같은 LSM 계열은 timestamped key와 compaction으로 비용을
compactor에 옮기며, Kubernetes의 etcd조차 같은 패턴을 되풀이한다.
결론은 명확하다.
MVCC의 비용은 사라지지 않고 보존되며, 각 엔진은 누가, 언제, 어떻게 실패할지만
선택한다는 것이다.

## 분석

### 글의 핵심 주장은 “비용 보존 법칙”이다

이 글의 뼈대는 단일 명제로 압축된다.
멀티버전을 유지하는 비용, 즉 history를 만들고 읽고 버리는 비용은
보존(conserved)되며, 엔진은 그 비용을 없앨 수 없고 오직 청구서를 누구에게
보낼지만 고른다는 것이다.
저자는 이 명제를 물리학의 보존 법칙처럼 다룬다.
PostgreSQL은 미래에 청구하고 bloat로 실패하며, undo 진영은 writer와
history를 읽는 reader에게 청구하고 쿼리 취소나 undo 팽창으로 실패하고,
SQL Server는 tempdb에 청구하고 인스턴스 전체로 실패하며, WiredTiger는
캐시에 청구하고 모두를 동시에 느리게 만들어 실패한다.

이 구조가 영리한 이유는, 비판의 사실관계를 부정하지 않으면서도 그 비판의
프레임 자체를 뒤집기 때문이다.
저자는 네 가지 혐의가 모두 “실제로 성립한다(charges stick)”고 인정한다.
PostgreSQL의 MVCC는 네 가지 구체적이고 재현 가능한 방식으로 나쁘다.
그러나 곧바로 같은 잣대를 다른 엔진에 들이대면 어느 열(column)에도
실패 모드가 없는 곳은 없다.
비판이 암묵적으로 전제한 “더 나은 대안이 존재한다”는 가정이 무너지는 순간,
“PostgreSQL은 나쁘다”는 명제는 “모든 MVCC는 나쁘다”로 확장되고,
그러면 그 명제는 사실상 무해해진다.

### 재현 가능성이 논증의 무기다

저자가 PostgreSQL 19 beta2 인스턴스에서 각 혐의를 직접 재현한다는 점은
단순한 데모가 아니라 논증 전략이다.
쓰기 증폭에서 lean 테이블의 3.0 WAL record와 index가 많은 테이블의 7.1 WAL
record라는 대비, ROLLBACK만으로 89MB가 178MB가 되는 팽창, 1.59초짜리
UPDATE를 0.124ms에 되감는 abort 같은 숫자는 모두 독자가 직접 재현할 수 있게
SQL과 함께 제시된다.
숫자를 손에 쥐여 주는 순간 “MVCC가 나쁘다”는 정성적 담론이 정량적 무대로
옮겨지고, 그 무대에서는 다른 엔진의 비용도 같은 단위로 측정될 수밖에 없다.

특히 abort 비용의 대비는 글 전체에서 반복되는 수사적 축(axis)이다.
PostgreSQL의 0.124ms rollback은 “아무것도 되돌리지 않고 새 버전을 버리면
된다”는 heap 설계의 직접적 귀결이다.
반대로 undo 엔진에서 rollback은 변경을 하나씩 역적용해야 하므로 실행 시간에
비례하고, MySQL 운영자가 오래 걸린 UPDATE를 죽인 뒤 롤백이 더 오래 걸리는
것을 지켜보는 장면으로 이어진다.
이 상수 시간 abort는 SQL Server가 ADR로, WiredTiger가 처음부터 확보하려 한
바로 그 속성이며, 저자는 이를 PostgreSQL 설계가 “첫날부터 공짜로” 가진
장점으로 되풀이해 강조한다.

### 네 가지 질문이라는 분류 틀

글의 진짜 기여는 개별 벤치마크가 아니라 “네 가지 질문”이라는 분류 틀이다.
저자는 이 틀로 관계형 DB(PostgreSQL, Oracle, InnoDB, SQL Server)뿐 아니라
document store(MongoDB/WiredTiger), 분산 SQL의 LSM 엔진(CockroachDB,
YugabyteDB), 심지어 관계형 세계 밖의 etcd까지 같은 좌표계에 올려놓는다.
etcd가 revision을 `(key, revision)`으로 append하고 compaction으로 정리하며
`required revision has been compacted`로 실패하는 방식은 PostgreSQL의
append-now-clean-later와 정확히 같은 선택임을 보인다.

이 틀의 힘은 일반화 가능성에 있다.
저자는 마지막에 독자에게 실천적 도구를 건넨다.
누군가 “우리 DB는 멀티버전 문제를 해결했다”고 말하면 네 가지 질문을 던지고,
마지막으로 “트랜잭션 하나가 점심시간 내내 열려 있으면 무슨 일이 벌어지는가”를
물어보라는 것이다.
FoundationDB가 트랜잭션 수명을 5초로 강제해 이 문제를 클라이언트의 책임으로
떠넘긴 사례는 이 질문이 모든 설계를 관통함을 보여 주는 극단값이다.

## 비평

### “비용 보존”은 강력하지만 비용의 크기 차이를 지운다

이 글의 중심 은유인 “비용은 보존된다”는 수사적으로 강력하지만, 물리학의
보존 법칙과 달리 비용의 총량이 엔진 간에 동일하다는 보장이 전혀 없다.
보존되는 것은 “history를 유지하는 데 비용이 든다”는 정성적 사실뿐이고,
그 비용의 절대 크기와 발생 빈도는 엔진마다 크게 다르다.
Uber의 워크로드처럼 커밋이 대부분이고 index가 많은 row를 자주 갱신하며 hot
테이블에 대한 긴 read가 드문 경우, undo 방식은 저자 스스로 인정하듯 “진짜로
더 낫다.”
그렇다면 이것은 대칭적인 트레이드오프가 아니라 특정 워크로드에서 한쪽이
명백히 우월한 비대칭적 선택이다.

글은 각 엔진의 실패 모드를 나란히 배치해 “누구에게도 완벽한 답은 없다”는
인상을 준다.
그러나 실패 모드의 존재 여부가 아니라 그 실패의 발생 확률과 심각도가
실무에서 중요하다.
“오래 열린 snapshot”이라는 공통의 아킬레스건을 예로 들면, PostgreSQL은
`xmin` horizon이 뒤로 밀려 database-wide로 VACUUM이 멈추는 반면, Oracle의
기본 `READ COMMITTED`는 statement 단위 snapshot을 잡으므로 idle 트랜잭션이
undo를 붙잡지 않는다.
같은 “점심시간 트랜잭션”이라도 두 엔진이 노출되는 위험의 크기는 다르며,
글의 대칭적 서술은 이 차이를 평평하게 만든다.

### 완화 기법을 “기본값”으로 재단하는 이중 잣대

저자는 HOT 업데이트를 다루면서 “critics는 기본 동작(default)을 묘사하고
있다”며 7.1 WAL record라는 최악값을 PostgreSQL의 대표 비용으로 제시한다.
그러나 실무 OLTP 테이블이 적절한 `fillfactor`로 90% 이상의 HOT 비율을
얻는다는 사실도 같은 문단에서 인정한다.
기본값으로 PostgreSQL을 평가하겠다는 태도는 일관적이지 않다.
다른 엔진의 장점을 소개할 때는 Oracle의 안정적 `ROWID`, InnoDB의 논리적 PK
참조처럼 잘 튜닝된 특성을 전제하기 때문이다.

이 이중 잣대는 방향을 바꿔도 나타난다.
SQL Server의 version store가 tempdb를 채워 인스턴스 전체를 마비시키는
시나리오는 “잊혀진 장기 snapshot 트랜잭션”이라는 운영 실수를 전제로 한 최악
사례인데, 저자는 이를 SQL Server 설계의 대표적 실패 모드로 제시한다.
반면 PostgreSQL 쪽에서는 `idle_in_transaction_session_timeout`이나
`statement_timeout` 같은 외부 방어책을 곧바로 언급해 위험을 누그러뜨린다.
각 엔진에 “최악의 기본값”과 “현실적 완화책” 중 무엇을 대입하느냐가 논증의
결론을 상당 부분 좌우하는데, 글은 이 선택을 일관되게 적용하지 않는다.

### 운영 가시성을 미덕으로 포장하는 결론

글의 마무리는 PostgreSQL이 reader를 막지 않고, `snapshot too old`로 쿼리를
취소하지 않으며, rollback을 기다리게 하지 않고, garbage를 `pageinspect`로
열어 볼 수 있는 8KB 페이지에 눈에 보이게 남긴다는 점을 강조한다.
“garbage가 당신의 것”이라는 표현은 결점을 미덕으로 재프레이밍한다.
그러나 가시성은 그 자체로 가치가 아니라 운영자가 대응해야 할 노동의
존재를 뜻하기도 한다.
Oracle의 undo 재활용이나 WiredTiger의 eviction이 “보이지 않게” 돌아간다는
것은 그만큼 운영자의 개입이 덜 필요하다는 뜻일 수 있다.

저자는 “운영상 시끄러운(operationally loud) 실패 모드”를 PostgreSQL이
의식적으로 선택했다고 말하지만, 시끄러운 실패가 조용한 실패보다 낫다는 것은
검증되지 않은 가치 판단이다.
autovacuum 튜닝, 장기 트랜잭션 사냥, wraparound 감시라는 유지보수 달력이
“측정 가능하고 눈에 보인다”는 이유로 정당화되는지는 조직의 운영 성숙도에
달려 있다.
많은 팀에게는 보이지 않지만 알아서 돌아가는 시스템이 더 나은 선택이며,
글은 이 관점을 충분히 다루지 않는다.

## 인사이트

### 논쟁의 무게 중심이 기술에서 문체로 옮겨 갔다

이 글에 대한 HN 반응에서 가장 두드러진 것은 MVCC 기술 논쟁이 아니라
“이 글이 LLM으로 쓰였는가”라는 문체 논쟁이었다.
여러 사용자가 정보의 밀도와 유용성을 인정하면서도 LLM 특유의 어투 때문에
읽다가 탭을 닫고 싶어진다고 토로했다.[^gtowey]
한 사용자는 “load-bearing”, “It's a real thing”, “It's a real trade-off”
같은 표현을 구체적 징후로 지목했고[^jdnier], 다른 사용자는 각 문장과 문단,
목록 항목이 모두 같은 크기로 “이것! 그다음 이것! 이제 이것!” 하며 임팩트를
노리는 리듬 자체가 인간의 사고 방식이 아니라고 지적했다.[^lucianbr]
저자 radim은 자신이 오랜 시간 문체를 다듬어 왔고 LLM은 윤문에만 쓴다고
해명하다가 결국 “LLM이라 불리는 것을 포기한다”고 물러섰다.[^radimm]

이것은 기술 콘텐츠의 신뢰 메커니즘이 재편되고 있다는 신호다.
과거에는 내용의 정확성이 신뢰를 좌우했지만, 이제는 문체가 자동화된 생산의
징후로 읽히는 순간 내용 전체의 검증 여부가 의심받는다.
한 사용자의 표현대로, LLM 어투를 보면 “정보가 검증됐는지, 얼마나 많은
LLM 군더더기를 헤치고 나아가야 하는지” 자동으로 의심하게 된다.[^gtowey2]
저자가 진짜 전문성과 직접 재현한 벤치마크를 가지고 있음에도, 그것을 LLM으로
포장한 것이 “청중의 시간을 존중하지 않는 신호”로 읽힌다는 지적[^bostik]은
전문가에게 뼈아픈 딜레마를 남긴다.
콘텐츠의 질과 무관하게, 생산 방식의 흔적이 수용을 가로막는 시대가 온 것이다.

### 비용 보존 법칙은 아키텍처 선택을 조직 역량 문제로 되돌린다

글은 비용이 writer, reader, tempdb, 캐시, compactor 중 누구에게 청구되는가로
엔진을 분류하지만, 이 프레임의 진짜 함의는 “누가 그 청구서를 감당할 역량이
있는가”라는 조직 차원의 질문으로 이어진다.
PostgreSQL의 청구서는 운영자에게 온다.
autovacuum을 튜닝하고, 장기 트랜잭션을 사냥하고, wraparound를 감시할 수 있는
전담 DBA나 성숙한 SRE 문화가 있는 조직에게 이 “시끄러운” 비용은 통제 가능한
운영 항목이다.

그러나 그런 역량이 없는 조직에게는 같은 청구서가 재앙이 된다.
이것이 관리형 PostgreSQL 서비스(RDS, Aurora, Cloud SQL, Supabase 등)가
번성하는 구조적 이유다.
그들은 본질적으로 “PostgreSQL의 청구서를 대신 지불하는 사업”을 한다.
비용 보존 법칙은 데이터베이스 엔진의 선택이 순수한 기술 판단이 아니라,
그 비용을 어느 계층이 흡수할 것인가에 대한 조직적, 경제적 판단임을 드러낸다.
Uber가 MySQL로 옮긴 것은 undo 설계가 보편적으로 우월해서가 아니라, 그들의
워크로드와 운영 조직에 청구서가 맞아떨어졌기 때문이라는 저자의 관찰은
이 계층 이동의 한 사례일 뿐이다.

### zheap의 좌절은 “단순함이 하중을 견딘다”는 교훈을 남긴다

글에서 기술적으로 가장 깊은 통찰은 zheap의 실패에 대한 진단이다.
undo 설계가 명백히 우월하다면 PostgreSQL에 undo 스토리지 엔진을 붙이면
되지만, 2018년 발표된 zheap는 수년간의 작업 끝에 사실상 dormant 상태가
됐다.
저자의 진단은 “heap의 단순함이 하중을 견디는(load-bearing) 구조”라는
것이다.
버전이 undo에 살기 시작하는 순간 recovery, replication, index, hot standby
같은 모든 서브시스템이 새로운 invariant를 물려받고, 스토리지 계층 하나를
바꾸려다 엔진의 절반을 다시 짓게 된다.

이것은 데이터베이스를 넘어 모든 성숙한 시스템에 적용되는 아키텍처 패턴이다.
오래된 시스템의 “결함”처럼 보이는 특성이 실은 다른 여러 부분이 의존하는
암묵적 계약(implicit contract)인 경우가 많다.
Hyrum's Law가 API 표면에서 말하는 것을 zheap는 스토리지 엔진 내부에서
보여 준다.
관찰 가능한 모든 동작에는 그것에 의존하는 누군가가 있다는 것이다.
core PostgreSQL이 설계를 바꾸지 않고 15년에 걸쳐 상수(HOT, visibility map,
B-tree deduplication, bottom-up index deletion, 17의 VACUUM TID store,
19의 `REPACK`)만 줄여 온 역사는, 근본 재설계보다 점진적 개선이 지배적
전략이 되는 이유를 보여 준다.
“청구서를 없애는” 재설계보다 “청구서를 줄이는” 최적화가 훨씬 안전하고,
그것이 40년 된 설계가 여전히 현역인 비결이다.

### 빠진 조각: 무엇을 넣고 뺄지가 곧 논증이다

HN에서 한 사용자는 MVCC 접근을 개척한 Interbase/Firebird가 완전히 빠진 것에
놀랐다고 지적했고, 저자는 초안에는 있었지만 “어딘가에서 자연스럽게 잘라야
했다”며 오늘날 대부분이 아는 것에 집중했다고 답했다.[^jhgb]
이 짧은 교환은 이런 비교 논증의 구조적 취약점을 드러낸다.
어떤 엔진을 포함하고 배제하느냐가 곧 결론의 설득력을 좌우하기 때문이다.
MVCC를 처음 상용화한 Firebird가 PostgreSQL과 유사한 접근으로 유사한 비용을
낸다는 사실은 “테이블 안 버전 저장”이 PostgreSQL만의 별난 선택이 아님을
보강하는 강력한 증거였는데, 지면 사정으로 빠졌다.

한편 LSM 섹션에 대해서는 “해결된 것은 없고 비용이 compactor로 옮겨갔을
뿐”이라는 저자의 결론에 공감하며, 오래 이 주제를 다루고 싶었다는 반응도
있었다.[^shayonj]
“공짜 점심은 없다”를 “공짜 read도 write도 없다”로 바꾼 이 댓글은 글의 핵심
명제가 실무자들 사이에서 얼마나 직관적으로 받아들여지는지를 보여 준다.
결국 이런 글의 가치는 새로운 사실의 발견이 아니라, 흩어진 직관에 검증
가능한 분류 틀과 숫자를 부여하는 데 있다.
그리고 그 틀의 완결성은 무엇을 포함했는가만큼이나 무엇을 뺐는가에 의해
시험받는다.

[^gtowey]: <https://news.ycombinator.com/item?id=49099211>

[^jdnier]: <https://news.ycombinator.com/item?id=49099443>

[^lucianbr]: <https://news.ycombinator.com/item?id=49099780>

[^radimm]: <https://news.ycombinator.com/item?id=49099692>

[^gtowey2]: <https://news.ycombinator.com/item?id=49099910>

[^bostik]: <https://news.ycombinator.com/item?id=49110208>

[^jhgb]: <https://news.ycombinator.com/item?id=49098963>

[^shayonj]: <https://news.ycombinator.com/item?id=49099228>
