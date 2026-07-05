# MemNixFS

<https://github.com/MemNixFS/MemNixFS>

## 소개

MemNixFS는 리눅스 메모리 덤프를 파일시스템으로 변환해 기존 도구로 탐색하고 분석할 수 있게 해주는
리눅스 메모리 포렌식 프레임워크다.
`grep`, `find`, `cat`, `diff` 같은 표준 유닉스 도구나 윈도우 탐색기로 메모리 이미지를 직접 탐색할 수 있다.
전용 쿼리 언어나 새로운 도구 학습 없이 기존 분석 스킬을 그대로 활용할 수 있다는 것이 핵심 가치다.

## 마운트 디렉토리 구조

메모리 이미지를 마운트하면 다음 디렉토리 구조로 노출된다.

| 디렉토리      | 내용                                                  |
| ------------- | ----------------------------------------------------- |
| `proc/<pid>/` | 프로세스별 데이터(맵, 파일 디스크립터, 스레드, 환경) |
| `sys/`        | 셸 히스토리, dmesg, 모듈, 네트워크 정보 등 시스템 전체 |
| `fs/`         | 페이지 캐시로 복원한 파일시스템                       |
| `forensic/`   | 타임라인 데이터 및 위협 탐지 결과                     |
| `search/`     | YARA 룰, IOC, 문자열 분석                             |
| `mem/`        | 물리 메모리 원시(raw) 접근                            |
| `plugins/`    | 확장 기능                                             |

## 지원 입력 포맷

- AVML(Azure Memory Loader)
- LiME(Linux Memory Extractor)
- 원시 물리 덤프
- kdump/vmcore(ELF64)

## 주요 기능

**심볼 의존성 최소화**

현대 커널의 BTF(BPF Type Format) 타입 정보를 활용해 디버그 심볼 없이도 동작한다.
커뮤니티 미러에서 심볼을 자동으로 가져오거나, 커스텀 커널을 위한 심볼 파일을 수동 지정할 수 있다.

**플랫폼 호환성**

윈도우에서는 WinFsp를 통해, 리눅스에서는 FUSE3를 통해 네이티브 마운트를 지원한다.
x86-64 리눅스 커널을 대상으로 한다.

**C ABI 노출**

C++17로 작성됐으며 `memnixfs.dll`을 통해 안정적인 C ABI를 제공한다.
FFI가 가능한 모든 언어에서 통합할 수 있다.

## 사용법

```bash
# 프로세스 목록 확인
memnixfs --dump memory.lime list

# 마운트 (윈도우: M: 드라이브)
memnixfs --dump memory.lime mount M:

# 특정 포렌식 파일 직접 읽기
memnixfs --dump memory.lime cat /sys/findevil/findevil.txt

# 심볼 자동 다운로드
memnixfs --auto-fetch --dump memory.lime mount /mnt/mem

# 오프라인 환경
memnixfs --no-http-cache --vmlinux /path/to/vmlinux --dump memory.lime list
```

## 분석

MemNixFS의 핵심 설계 결정은 "새로운 포렌식 쿼리 언어 대신 파일시스템 추상화"를 선택한 것이다.
Volatility 같은 기존 포렌식 도구는 플러그인 기반 명령어 체계를 가지며, 도구 자체를 배워야 한다.
반면 MemNixFS는 분석가가 이미 아는 `grep`, `find`, Python `os.walk`를 그대로 쓸 수 있게 한다.
진입 장벽이 낮아지고, 기존 스크립트와 도구를 재활용할 수 있다.

BTF를 통한 심볼 독립적 동작은 실무에서 중요하다.
커스텀 커널이나 디버그 심볼이 없는 환경, 클라우드 VM 메모리 덤프 같은 상황에서
Volatility의 심볼 의존성이 분석의 병목이 되곤 한다.
MemNixFS가 이 제약을 완화한다면 실무 포렌식 워크플로우에 실질적 기여를 할 수 있다.

## 비평

프로젝트가 아직 초기 단계이며 독립적 검증 사례가 부족하다.
BTF 기반 분석의 정확도와 완성도, 복잡한 메모리 레이아웃에서의 신뢰성은
실제 인시던트 대응 사례로 증명되어야 한다.
또한 Volatility 3의 방대한 플러그인 생태계와 비교했을 때 커버리지의 차이가 얼마나 큰지,
현재 문서만으로는 파악하기 어렵다.

## 인사이트

포렌식 분석 도구의 진화 방향 중 하나는 "학습 비용 최소화"다.
인시던트 대응은 시간이 생명인 작업이고, 분석가가 새로운 도구를 배우는 데 쓸 시간이 없다.
파일시스템 인터페이스를 통해 기존 도구와의 호환성을 제공하는 접근법은
도구 채택률 측면에서 의미 있는 차별화 전략이다.

## 라이선스

Apache-2.0 (작성자: Youssef Ayman, Tarek Salama)
