# StreamFusion: Flink SQL 연산자를 Rust와 Arrow로 대신 실행하는 오픈소스 가속기

<https://streamfusion.tech>

<https://github.com/datafusion-contrib/StreamFusion>

HN 토론: <https://news.ycombinator.com/item?id=49327209> (1점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=36136>

## 소개

StreamFusion은 Apache Flink SQL의 지원되는 연산자를 Rust와 Apache
Arrow/DataFusion으로 실행하는 가속기다.
Flink와 Flink 쪽 JVM 사이는 JNI(Java Native Interface)로 이어진다.
계획 수립과 조율, 아직 지원하지 않는 모든 것은 Flink가 계속 맡는다.
README의 설명으로는 쿼리를 Flink가 계획하면,
결과를 정확히 재현할 수 있는 잡만 네이티브 잡으로 바꾸고 나머지는 같은 결과로
Flink에 되돌린다.
README 맨 위의 안내문은 이 프로젝트가 Apache Flink나 Apache DataFusion의 일부가
아니라고 밝힌다.

저장소는 2026년 7월 3일에 만들어졌고, 마지막 푸시는 2026년 11월 1일이다.
기록 시점에 스타는 157개, 포크는 13개, 열린 이슈는 72개였고, 주 언어는 Java,
라이선스는 Apache-2.0이다.[^api]
설치 예시의 버전은 `0.1.0-rc4`로, 릴리스 후보(release candidate)다.

## 동작 방식

가속은 쿼리 전체가 조건을 만족할 때만 일어난다.
행(row) 단위 소스와 싱크를 뺀 모든 연산자가 네이티브로 실행되어야 하고,
연산자 사이에서는 Arrow 배치를 주고받는다.
행과 Arrow 사이의 변환은 호스트 가장자리에서 한 번만 치른다.
내부의 연산자 하나라도 지원되지 않으면 쿼리 전체가 Flink로 돌아간다고
README는 적는다.

README가 꼽는 네이티브 범위는 넓다.
무상태 연산(projection, filter, `UNION ALL`, `GROUPING SETS`, `UNNEST`),
윈도 집계(`TUMBLE`, `HOP`, `SESSION`, `CUMULATE`, `OVER`), 조인(정규 조인,
구간 조인, 윈도 조인, 시간 테이블 조인, 룩업 조인),
변경 로그(non-windowed `GROUP BY`, Top-N, 중복 제거)가 들어간다.
커넥터는 Parquet와 ORC 싱크, Delta Lake 싱크, Apache Paimon 소스와 싱크,
Kafka 소스와 싱크다.
Kafka는 Flink의 클라이언트가 소비와 생산, 오프셋, 트랜잭션을 맡고,
Rust는 포맷 직렬화와 역직렬화만 맡는다.

Flink에 남는 것은 lateral 테이블 함수, `MATCH_RECOGNIZE`, PyFlink UDF,
3단계 distinct 집계, 원격 파일 경로(`hdfs:`, `s3:`)의 일부,
JVM과 결과가 갈릴 수 있는 표현식과 타입의 가장자리(`allowIncompatible`로 선택),
비트 단위로 재현하지 못하는 커넥터 옵션(Maxwell/Canal CDC,
일부 protobuf 필드)이다.
README는 연산자와 커넥터별 상태(네이티브, 부분,
미지원)가 문서 사이트에 한 페이지씩 있다고 안내한다.

README는 설계의 뼈대를 기존 엔진을 포팅하는 데서 가져왔다고 말한다.
DataFusion Comet이 전체 구조(변경하지 않은 SQL 플래너 뒤의 네이티브 컬럼형
가속기)와 JNI와 Arrow C Data Interface 다리의 기준이고,
Arroyo가 스트리밍 연산자 구현, DataFusion이 실행 엔진,
RisingWave가 변경 로그 의미와 상태 인코딩의 기준이다.
Apache Flink는 모든 연산자가 같은 출력을 내는지 확인하는 정합성(parity)
기준이라고 한다.

## 설치하기

릴리스 JAR은 Maven Central에서 받으며, 리눅스 x86_64와 macOS Apple Silicon용
네이티브 라이브러리가 이미 들어 있다고 README는 말한다.
사용자가 Rust나 Java를 직접 빌드할 필요는 없다.

```bash
STREAMFUSION_VERSION=0.1.0-rc4
curl --fail --location \
  "https://repo1.maven.org/maven2/tech/streamfusion/streamfusion-loader/$STREAMFUSION_VERSION/streamfusion-loader-$STREAMFUSION_VERSION.jar" \
  --output "$FLINK_HOME/lib/00-streamfusion-loader.jar"
curl --fail --location \
  "https://repo1.maven.org/maven2/tech/streamfusion/streamfusion-core/$STREAMFUSION_VERSION/streamfusion-core-$STREAMFUSION_VERSION-runtime.jar" \
  --output "$FLINK_HOME/lib/streamfusion-core.jar"
```

지원 버전은 Flink 2.2.0과 2.2.1 두 개뿐이다.
JAR은 Flink의 `lib` 디렉터리에 넣고 잡 JAR에는 넣지 않으며,
일반 스트리밍 SQL 잡에 애플리케이션 쪽 호출은 필요 없다.
기본 설치는 커넥터와 포맷에 중립이어서,
잡이 쓰는 커넥터와 포맷의 `streamfusion-*` JAR을 따로 얹는다.

배포 문서(streamfusion.tech의 Deployment 페이지)는 몇 가지를 더 말한다.
JAR은 TaskManager뿐 아니라 제출 클라이언트와 JobManager에도 있어야 한다.
클라이언트와 JobManager와 TaskManager의 JDK는 같아야 하고,
Iceberg 어댑터는 JDK 17이 전부 필요하다.
리눅스 ARM64 바이너리는 아직 배포하지 않으며,
다른 Flink 라인 사이의 세이브포인트 업그레이드와 다운그레이드는 검증되지 않았다.
이 문서를 쓴 환경에는 Flink 클러스터가 없어서 설치와 실행은 직접 해 보지 않았다.

## 쿼리가 가속되었는지 확인하기

가속은 쿼리 모양에 달려 있으므로, 설치한 뒤 첫 일은 내 쿼리가 실제로 네이티브로
가는지 보는 것이다.
README는 쿼리가 Flink로 되돌아간 이유를
`-Dstreamfusion.logFallbackReasons=true`로 볼 수 있다고 안내한다.
가속 켜기와 끄기 스위치, `allowIncompatible` 표현식 선택,
네이티브 Kafka 버퍼용 오프힙 메모리 크기도 설정 문서에 있다고 한다.
같은 쿼리를 가속을 켠 채와 끈 채로 돌려 결과와 처리량을 비교하는 것이 가장
확실한 확인이다.

## 벤치마크 읽기

헤드라인 벤치마크는 Nexmark 쿼리를 Kafka에서 읽어 Kafka로 내보내는 끝에서
끝(end-to-end) 파이프라인이다.
병렬도 4에서 같은 200만 이벤트 JSON 코퍼스를 읽고, 체크포인트 간격은 1초이며,
소비와 직렬화와 Kafka 쓰기와 마지막 트랜잭션 커밋까지 시간에 들어간다고
README는 적는다.
측정은 Apple M1 Max에서 했다.

| 열          | 기하평균 배율 | 비교 대상                                            |
| ----------- | ------------- | ---------------------------------------------------- |
| Memory, off | 1.31×         | Flink 기본 힙 상태 대 StreamFusion 메모리 상태       |
| Memory, on  | 1.44×         | 같음, 미니 배치 켬                                   |
| Disk, off   | 2.75×         | stock Flink RocksDB 대 StreamFusion 네이티브 RocksDB |
| Disk, on    | 3.41×         | 같음, 미니 배치 켬                                   |

README의 표는 쿼리별 값도 싣는다.
Disk 열의 가장 큰 값은 q20의 68.20×와 q9의 67.95×(미니 배치 켬)이고, Memory,
off 열에서 q19만 0.99×로 느려졌다.
Memory 열은 셀마다 한 번 측정(2026-08-25)했고,
Disk 열은 워밍업 한 번에 두 번 측정한 값 중 가장 좋은 것(2026-09-05)이다.
README는 이 숫자가 한 기계 안에서만 비교할 수 있다고 적는다.

Fluss 커넥터는 별도로 측정했다.
Linux의 Intel Core i7-12650H에서 Fluss 1.0.0을 양쪽 끝에 두고 같은 22개 쿼리의
중앙값 배율 기하평균을 낸 값이 4.66×, 5.07×, 4.83×,
5.71×(Memory/Disk, off/on)다.
README는 Memory/off q4와 Memory/on q16이 중앙값에서 느려졌고,
이 짧은 전체 잡 시간은 지속 처리량을 보여 주지 않는다고 적는다.

## 비평

### Disk 열은 엔진 비교가 아니라 상태 저장소 비교를 섞는다

README의 Disk 열은 stock Flink의 RocksDB 경로와 StreamFusion의 네이티브 RocksDB
백엔드를 견준다.
두 쪽은 쿼리 엔진뿐 아니라 상태를 읽고 쓰는 구현도 다르다.
README가 스스로 말하듯 Flink의 RocksDB 경로는 레코드마다 비용을 치르고
StreamFusion은 네이티브 상태 작업을 배치로 묶는다.
q9와 q20의 60배 넘는 배율은 이 차이가 크게 반영된 값일 가능성이 높다.
엔진만의 효과를 보려면 같은 상태 백엔드에서 연산자만 바꾼 측정이 있어야 하고,
그것에 가까운 것은 Memory 열의 1.31×와 1.44×다.

### 맨 위의 바이트 단위 동일성 약속과 헤드라인 셀은 같은 조건이 아니다

README는 승인된 모든 것에서 결과가 stock Flink와 바이트 단위로 같다고 말한다.
그런데 표에서 † 표시가 붙은 q1, q10, q14에서 q17,
q21의 셀은 근사 소수 연산이나 날짜와 정규식 동작의 가장자리에서 Flink와 다를 수
있는 선택 변형(opt-in)으로 측정했다고 README가 직접 적는다.
그러므로 이 쿼리들의 헤드라인 배율은 기본 설정에서 같은 결과를 내는 쿼리의
배율이 아니다.
Fluss 비교는 이 변형을 끄고 정확한 SQL로 돌렸다고 밝히고 있어서,
같은 문서 안에서도 조건이 갈린다.

### 한 대의 노트북, 한 번의 측정은 서버 운영의 증거가 되기 어렵다

헤드라인은 노트북급 칩에서 병렬도 4로 잰 값이고,
Memory 열은 셀마다 한 번 측정한 값이다.
README 스스로 짧은 전체 잡 시간에는 클라이언트 종료 시간이 들어간다고 적는다.
운영에서 쓸 코어 수, 상태 크기, 체크포인트 간격에서 같은 배율이 나오는지는 이
문서의 어떤 자료로도 알 수 없다.

### 다른 가속기와의 비교는 같은 척도가 아니다

README는 Flash(Alibaba Cloud)와 Vera X(Ververica)가 Nexmark에서 5에서 10배를
주장하고, Iron Vector(Irontools)는 무상태 파이프라인에서 약 97% 높은 처리량을
주장한다고 쓴다.
이 문서는 그 세 페이지를 열어 보지 않았고, README가 전하는 주장으로만 적는다.
세 주장은 각자의 하드웨어와 벤치마크에서 나왔고,
StreamFusion의 1.3에서 3.4배와 나란히 놓을 수 있는 숫자가 아니다.
README도 StreamFusion이 Flash와 Vera X보다 초기 단계이고 연산자 폭과 공개
벤치마크에서 못 미친다고 인정한다.

### 도입의 문턱이 높고 실패는 조용하다

지원 버전이 Flink 2.2.0과 2.2.1로 고정되어 있고, 예시 버전은 릴리스 후보다.
연산자 하나가 지원되지 않으면 쿼리 전체가 되돌아가므로,
가속을 기대한 쿼리가 아무 오류 없이 평소 속도로 도는 일이 생길 수 있다.
되돌아간 이유는 로그로 확인해야 하고, 기본 설정에서 확인하지 않으면 가속
여부를 알 수 없다.

## 체크리스트

- [ ] Flink가 2.2.0 또는 2.2.1인가
- [ ] 클라이언트와 JobManager와 TaskManager의 JDK가 같은가
- [ ] 로더와 코어 JAR이 `lib`에 있고 같은 빌드에서 나온 것인가
- [ ] 잡이 쓰는 커넥터와 포맷의 `streamfusion-*` JAR을 얹었는가
- [ ] `-Dstreamfusion.logFallbackReasons=true`로 내 쿼리가 네이티브로 가는지 확인했는가
- [ ] 쿼리에 `MATCH_RECOGNIZE`, lateral 테이블 함수, PyFlink UDF 같은 되돌아가는 모양이 없는가
- [ ] 가속을 켠 채와 끈 채의 결과가 같은가
- [ ] 비교할 때 상태 백엔드를 같게 두었는가
- [ ] `allowIncompatible`로 켠 표현식이 내 데이터에서 결과를 바꾸지 않는가

---

[^api]: GitHub, [REST API: datafusion-contrib/StreamFusion](https://api.github.com/repos/datafusion-contrib/StreamFusion)
