# Barman

<https://github.com/EnterpriseDB/barman>

<https://pgbarman.org/>

HN 토론: <https://news.ycombinator.com/item?id=47948526> (183점, 24개 댓글)

## 소개

Barman(Backup and Recovery Manager)은 PostgreSQL 서버의 재해 복구(disaster recovery)를 위한 오픈소스 관리 도구다.
Python으로 작성됐으며, EnterpriseDB가 관리한다.
여러 PostgreSQL 서버의 백업과 복구를 원격에서 중앙집중식으로 관리할 수 있다.
pgBackRest의 유지보수가 중단된 이후, [GeekNews 댓글](https://news.hada.io/topic?id=29139)에서 언급됐듯 그 대체제로 주목받고 있다.

2026년 3월 현재 버전 3.18.0이 출시됐으며, GitHub에서 3,100개 이상의 스타와 251개의 포크를 기록 중이다.
라이선스는 GNU GPL 3이다.

## 주요 기능

**온라인 핫 백업(Online Hot Backup)**
PostgreSQL 서버가 실행 중인 상태에서 백업을 수행한다. 서비스 중단 없이 정기 백업이 가능하다.

**특정 시점 복구(Point-In-Time Recovery, PITR)**
PostgreSQL 기본 PITR 기술을 활용해 특정 시점의 상태로 데이터베이스를 복원한다.
전체 백업 시점뿐 아니라 WAL(Write-Ahead Log) 아카이브를 활용해 임의의 시점으로 복구할 수 있다.

**동기 WAL 스트리밍(Synchronous WAL Streaming)**
실시간으로 WAL을 스트리밍 받아 데이터 손실 가능성을 최소화한다.
Zero Data Loss(ZDL) 구성을 지원한다.

**중앙집중식 다중 서버 관리**
단일 Barman 서버에서 여러 PostgreSQL 인스턴스의 백업과 복구를 관리할 수 있다.
엔터프라이즈 환경에서 수십 개의 데이터베이스 서버를 일관된 방식으로 운영하는 데 적합하다.

**백업 카탈로그와 보존 정책**
백업 목록 조회, 보존 기간 설정, 오래된 백업 자동 삭제, 아카이브 관리를 통합 인터페이스에서 처리한다.

## CLI

주요 명령어:

```bash
barman backup <server>          # 즉시 백업 수행
barman list-backups <server>    # 백업 목록 조회
barman recover <server> <id> /target/path  # 특정 백업으로 복구
barman check <server>           # 서버 상태 및 백업 설정 검사
barman show-backup <server> <id>  # 특정 백업 상세 정보
barman delete <server> <id>     # 특정 백업 삭제
barman switch-wal <server>      # WAL 세그먼트 강제 전환
```

`barman check`는 SSH 접속, PostgreSQL 연결, WAL 아카이빙, 디스크 공간 등 운영 요구사항을 종합 점검하여
백업 설정이 올바른지 사전에 검증할 수 있다.

## 분석

### PostgreSQL 재해 복구 생태계에서의 위치

PostgreSQL 백업 도구는 크게 세 가지 접근 방식으로 나뉜다.
`pg_dump`/`pg_dumpall`은 논리적 백업으로 간단하지만 대규모 데이터베이스에서 복구 시간이 길다.
`pg_basebackup`은 물리적 백업이지만 단독으로는 관리 기능이 제한적이다.
Barman과 pgBackRest 같은 백업 관리 도구는 물리적 백업에 PITR, 중앙 관리, 보존 정책을 더한다.

pgBackRest가 유지보수를 중단하면서 Barman은 물리적 백업 관리 카테고리에서 사실상 유일한 활발히 유지되는 오픈소스 대안이 됐다.
EnterpriseDB라는 상업 주체가 관리한다는 점은 장기 지원 안정성 측면에서 긍정적 신호다.
HN에서 subhobroto는 pgBackRest가 2026년 4월 27일 공식 아카이브됐다는 사실을 확인하며, 과거 pgBackRest로 이전했던 팀들이 이 결정을 재검토하고 있는지 묻는다.[^subhobroto]

### Python 기반 구현의 의미

Python으로 작성된 도구는 PostgreSQL의 C 기반 에코시스템에서 이례적이다.
성능 크리티컬한 경로(실제 백업 I/O)는 rsync, pg_basebackup 같은 외부 도구에 위임하고,
오케스트레이션과 관리 레이어만 Python으로 구현하는 설계다.
이는 코드 가독성과 확장성을 높이지만, 대용량 환경에서 오케스트레이션 자체의 성능 병목 가능성이 있다.

## 비평

### 강점: 엔터프라이즈 운영 요구사항에 맞춘 설계

단순 백업 도구가 아니라 DBA가 다수 서버를 운영하는 환경을 상정한 설계가 돋보인다.
중앙집중식 관리, 보존 정책 자동화, 상태 점검(`barman check`) 기능은
개별 서버에 cron + pg_basebackup을 구성하는 방식과 차별화된다.
`barman check`를 통해 백업 설정의 정합성을 사전 검증하는 접근은 장애 발생 전 문제를 발견하는 운영 모범 사례다.

### 약점: 초기 설정 복잡성

SSH 연결 설정, PostgreSQL 인증, WAL 아카이빙 구성, Barman 서버 자체 구성까지
초기 설정 단계가 복잡하다. 공식 문서가 상세하지만, 소규모 팀이나 PostgreSQL 운영 경험이 적은 환경에서는
진입 장벽이 높다. 클라우드 관리형 PostgreSQL(RDS, Cloud SQL 등)을 사용하는 경우
WAL 아카이빙 설정에 제약이 있어 Barman의 기능을 완전히 활용하기 어렵다.

### 약점: 클라우드 네이티브 환경과의 통합

Barman은 기본적으로 온프레미스나 IaaS 수준의 서버 환경을 전제한다.
Kubernetes 환경에서의 운용, 클라우드 오브젝트 스토리지(S3, GCS) 연동은 가능하지만
기본 구성이 아니라 추가 설정이 필요하다.
CloudNativePG 같은 Kubernetes-native PostgreSQL 오퍼레이터가 내장 백업 기능을 제공하면서
컨테이너 환경에서는 Barman의 포지셔닝이 복잡해졌다.

S3 지원 여부는 HN에서 상반된 경험담이 나왔다. levkk는 "Barman이 S3 백업을 지원하지 않아 pgBackRest를 선택했다. Barman은 다른 Linux 머신에만 백업할 수 있었던 것으로 기억한다"며 pgBackRest의 부재를 아쉬워했다.[^levkk] 그러나 bakies는 정반대의 경험을 공유한다. "barman-cloud를 통한 S3 백업이 내가 Barman을 사용해본 유일한 방식이었다. 파일 시스템에도 쓸 수 있다는 걸 몰랐다"는 것이다.[^bakies] 이 상반된 경험은 Barman의 S3 지원이 알려진 것보다 폭넓지만 문서화와 기본 설정 경험이 균일하지 않음을 시사한다.

실제 프로덕션 사례에서 philippemnoel은 CloudNativePG를 통해 Barman을 사용하며 두 가지 제약을 보고한다. S3 스토리지 클래스 지정 불가와 대용량 데이터베이스에서의 느린 업로드 속도다.[^philippemnoel] ninjaoxygen 역시 CloudNativePG 플러그인으로 사용하면서 "WAL 한도를 신중하게 설정하지 않으면 WAL 볼륨이 꽉 차 데이터베이스가 사용 불가 상태가 된다"고 경고한다.[^ninjaoxygen] WAL 모니터링과 임계값 알림을 백업 설정과 함께 구성하는 것이 실운영에서 필수적이다.

## 인사이트

### 재해 복구 계획 없는 데이터베이스 운영의 현실

pgbarman.org가 인용하듯, 조직의 절반만이 데이터베이스 재해 복구 계획을 갖추고 있다.
그리고 많은 조직이 실제 데이터 손실이나 서비스 중단을 경험한 후에야 DR 플랜을 도입한다.
이것은 기술 문제라기보다 위험 인식의 문제다.

PITR이 가능한 백업 시스템은 랜섬웨어, 실수로 인한 데이터 삭제, 애플리케이션 버그로 인한 데이터 오염 등
광범위한 장애 시나리오에 대응할 수 있다.
`DROP TABLE` 같은 실수가 발생했을 때, 트랜잭션 로그를 통해 해당 명령 직전으로 복구하는 능력은
서비스의 생존을 결정할 수 있다.

### 백업은 복구 테스트를 포함해야 완성된다

Barman 같은 도구가 백업을 자동화하더라도, 복구 테스트 없이는 절반짜리 DR 플랜이다.
“백업이 있다”와 “복구할 수 있다”는 다른 명제다.
백업 파일이 손상됐거나, PITR 설정이 잘못됐거나, 복구 절차가 문서화되지 않았다면
장애 발생 시 패닉 상태에서 수동으로 복구를 시도하게 된다.

`barman check`와 정기적인 복구 드릴(recovery drill)을 조합하는 운영 관행이 필요하다.
이상적으로는 실제 프로덕션 데이터의 일부를 스테이징 환경으로 복구하는 테스트를
분기마다 자동화하는 것이 목표가 되어야 한다.
복구에 걸리는 시간(RTO), 허용 가능한 데이터 손실 범위(RPO)를 사전에 정의하고,
Barman 설정이 그 요구사항을 충족하는지 실증적으로 검증해야 한다.

---

[^subhobroto]: <https://news.ycombinator.com/item?id=47987187>
[^levkk]: <https://news.ycombinator.com/item?id=47987771>
[^bakies]: <https://news.ycombinator.com/item?id=47989075>
[^philippemnoel]: <https://news.ycombinator.com/item?id=47989160>
[^ninjaoxygen]: <https://news.ycombinator.com/item?id=47987464>
