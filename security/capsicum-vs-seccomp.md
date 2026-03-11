# Capsicum vs seccomp: 프로세스 샌드박싱

<https://vivianvoss.net/blog/capsicum-vs-seccomp>

## 한 줄 요약

FreeBSD Capsicum은 권한을 "제거"하고,
Linux seccomp-bpf는 시스템 콜을 "필터링"한다.
같은 목표, 정반대의 인식론.

## 문제: Ambient Authority

1969년 이래 Unix의 보안 모델은 변하지 않았다.
프로세스는 자신을 실행한 사용자의 **모든 권한**을 상속받는다.
tcpdump는 캡처 디바이스 1개와 출력 파일 1개만 필요하지만,
root로 실행되므로 root가 접근할 수 있는 **모든 것**을 얻는다.
"필요한 것"과 "얻는 것" 사이의 간극이 곧 공격 표면이다.

두 운영체제가 이 문제를 풀기로 했다.
하나는 방에서 문을 없앴고, 다른 하나는 경비원을 세웠다.

## FreeBSD Capsicum: 빼기의 모델

2010년 Cambridge 대학의 Robert Watson과 Jonathan Anderson이
USENIX Security에서 Best Student Paper를 수상한 논문에서
제안했다. 핵심 통찰은 단순하다.
프로세스가 하지 **못할** 것을 나열하는 대신,
모든 것을 제거하고 필요한 것만 돌려준다.

2014년 FreeBSD 10.0에 기본 탑재됐다.
API의 핵심은 단 하나의 시스템 콜이다.

```c
#include <sys/capsicum.h>

int main(void)
{
    int fd = open("/var/log/capture.pcap", O_WRONLY);

    /* FD 권한 제한: 쓰기와 탐색만 허용 */
    cap_rights_t rights;
    cap_rights_init(&rights, CAP_WRITE, CAP_SEEK);
    cap_rights_limit(fd, &rights);

    /* 캡빌리티 모드 진입. 돌아올 수 없다. */
    cap_enter();

    /*
     * 글로벌 네임스페이스 접근 완전 상실.
     * 파일시스템 없음. 새 소켓 없음. 새 프로세스 없음.
     * 남는 것: 이미 열린 FD들, 명시적으로 부여한 권한만.
     */
    write_packets(fd);
    return 0;
}
```

`cap_exit()`는 존재하지 않는다.
커널이 플래그를 설정하고, 그 플래그는 해제되지 않는다.
파일시스템, 네트워크, 프로세스 테이블은 접근 불가가 아니라
**존재하지 않게** 된다.

## Linux seccomp-bpf: 필터링의 모델

2005년 Andrea Arcangeli가 seccomp strict 모드를 추가했다.
4개 시스템 콜(read, write, exit, sigreturn)만 허용.
우아하지만 실용성이 거의 없었다.

2012년 Will Drewry가 Linux 3.5에 seccomp-bpf를 도입했다.
BPF 프로그램이 매 시스템 콜을 런타임에 검사하여
허용, 거부, 종료를 결정한다.

```c
#include <seccomp.h>

int main(void)
{
    /* 기본: 허용되지 않은 시스템 콜은 프로세스 종료 */
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);

    /* 허용 목록: 이 시스템 콜만 통과 */
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

    seccomp_load(ctx);

    /*
     * 이후:
     *   - 목록의 시스템 콜만 작동
     *   - 단, 모든 기존 FD는 전체 권한 유지
     *   - read()가 허용되면 어떤 FD든 읽을 수 있다
     *   - 필터는 "콜"을 검사하지 "대상"을 검사하지 않는다
     */
    write_packets(fd);
    return 0;
}
```

Docker 기본 seccomp 프로필은 300개 이상의 시스템 콜 중
약 44개만 차단한다. 나머지 256개는 통과한다.
"3번과 7번 방에만 들어갈 수 있다"와
"12번과 15번 방을 **제외하고** 아무 데나 들어갈 수 있다"의
차이다. 건물에 층이 늘어날수록 후자가 더 위험해진다.

## tcpdump: 같은 도구, 정반대의 샌드박싱

가장 명확한 비교는 이론이 아니라 tcpdump다.

**FreeBSD**: tcpdump는 BPF 캡처 디바이스와 출력 파일을 열고,
`cap_rights_limit()`로 권한을 제한한 뒤 `cap_enter()`를
호출한다. 그 순간부터 파일시스템도, 네트워크도, 새 소켓도
존재하지 않는다. 침해된 tcpdump가 할 수 있는 것:
디바이스 1개 읽기, 파일 1개 쓰기. 그뿐이다.

**Linux**: tcpdump는 seccomp-bpf 필터로 시스템 콜을
걸러낸다. 허용된 콜은 모든 열린 FD에 대해 전체 권한을
유지한다. `read()`가 허용되면 **어떤** 열린 FD든 읽는다.
필터는 콜을 검사하지, 대상을 검사하지 않는다.

**구조적 차이가 중요한 이유**: 커널이 성장할 때 드러난다.
Capsicum은 커널에 시스템 콜이 1,000개 추가돼도 상관없다.
`cap_enter()` 이후 파일을 여는 새 시스템 콜은 캡빌리티
모드라서 작동하지 않는다. 제한이 열거적(enumerative)이
아니라 구조적(structural)이기 때문이다.

## CVE-2022-30594: 증거

2022년, Linux 커널 5.17.2 이전에서 `PTRACE_SEIZE`를 이용해
`PT_SUSPEND_SECCOMP`를 설정하면 seccomp 필터를 **완전히
우회**할 수 있었다. 필터 규칙은 정확했다.
규칙을 **강제하는 메커니즘**이 정확하지 않았다.

Capsicum은 이 종류의 공격에 구조적으로 면역이다.
중단할 필터가 없다. 우회할 강제 계층이 없다.
존재하지 않는 문은 열 수 없다.

## 비교표

| 차원               | Capsicum           | seccomp-bpf          |
|--------------------|--------------------|-----------------------|
| 철학               | 캡빌리티(빼기)     | 필터(열거)            |
| 기본 자세          | 전부 거부          | 전부 허용             |
| 세분도             | FD별 + 연산별      | 시스템 콜별           |
| 되돌림 가능        | 불가               | 필터 단위로 불가      |
| 새 커널 시스템 콜  | 설계상 차단        | 누락 가능             |
| FD 수준 제한       | `cap_rights_limit` | 없음                  |
| 샌드박스 진입      | 시스템 콜 1개      | BPF 프로그램          |
| 런타임 오버헤드    | 무시할 수준(1 플래그) | 매 콜마다 필터 평가 |
| 실사용             | tcpdump, dhclient, hastd, gzip, OpenSSH | Docker, Firefox, OpenSSH, systemd, Android |

## 숫자로 보기

- Capsicum: 캡빌리티 모드에서 ~567개 중 ~190개 시스템 콜
  허용
- Docker 기본 seccomp: 300개 이상 중 ~44개만 차단
- Capsicum 오버헤드: 프로세스당 커널 플래그 1개
- seccomp-bpf 오버헤드: 매 시스템 콜마다 필터 평가
- Linux 시스템 콜: 2012년 335개 → 현재 450개 이상

## 인사이트

### 인식론의 차이가 보안 아키텍처를 결정한다

seccomp은 "이 프로세스가 **호출하면 안 되는** 것은
무엇인가?"를 묻는다. 모든 위험한 행위를 사전에 알아야 한다.
커널 버전마다, 새 시스템 콜마다, 새 공격 벡터마다
필터를 갱신해야 한다.

Capsicum은 "이 프로세스가 **실제로 필요한** 것은
무엇인가?"를 묻는다. 위협을 열거하는 것이 아니라
요구사항을 열거한다. 프로세스가 필요로 하는 집합은
작고, 알 수 있고, 안정적이다. 프로세스가 남용할 수 있는
집합은 커널 릴리스마다 커진다.

이 차이는 보안 설계를 넘어 소프트웨어 엔지니어링 전반에
적용된다. 차단 목록(blocklist)은 알려진 위협에 반응하고,
허용 목록(allowlist)은 알려진 요구사항에 기반한다.
**알려진 요구사항은 알려진 위협보다 항상 관리하기 쉽다.**

### 비가역성이 보안의 강도를 결정한다

`cap_enter()`의 비가역성은 제약이 아니라 강점이다.
보안 메커니즘에서 "되돌릴 수 있다"는 것은 곧
"공격자도 되돌릴 수 있다"는 뜻이다.
CVE-2022-30594가 정확히 이것을 증명했다.
seccomp 필터 자체는 완벽했으나 필터를 **중단하는** 경로가
존재했고, 공격자가 그것을 찾았다.

Capsicum에는 중단할 대상 자체가 없다.
**우회할 메커니즘이 없으면 우회도 없다.**

### 필터의 숙명: 유지보수 부채

seccomp-bpf 프로필은 유지보수 부채를 내재한다.
커널이 새 시스템 콜을 추가할 때마다 모든 seccomp 프로필을
검토하고 업데이트해야 한다. 2012년 335개에서 현재
450개 이상으로 늘어난 시스템 콜 수가 이를 증명한다.
차단 목록 기반 프로필은 새 시스템 콜이 추가될 때마다
자동으로 허용 범위가 넓어진다. 즉, **아무것도 하지 않아도
보안이 약해진다.**

Capsicum은 이 문제가 구조적으로 존재하지 않는다.
캡빌리티 모드에서 새 시스템 콜이 추가돼도 글로벌
네임스페이스 접근은 불가하므로, 보안 수준이
유지보수 없이 일정하게 유지된다.

### 세분도의 격차: FD 수준 vs 시스템 콜 수준

seccomp-bpf에서 `read()`를 허용하면 **모든** 열린 FD를
읽을 수 있다. Capsicum에서는 각 FD에 `CAP_READ`,
`CAP_WRITE`, `CAP_SEEK` 등을 개별적으로 부여한다.
이 세분도 차이는 실제 공격 시나리오에서 결정적이다.

침해된 프로세스가 `read()`를 호출할 수 있을 때:
- seccomp: 열린 모든 FD 읽기 가능
- Capsicum: `CAP_READ`가 부여된 FD만 읽기 가능

**같은 시스템 콜이 허용돼도 도달할 수 있는 범위가 다르다.**

### Capsicum이 주류가 되지 못한 이유

이렇게 우월한 모델이 왜 FreeBSD 밖에서 확산되지
못했는가? 기사가 직접 언급하지 않지만 추론할 수 있다.

1. **기존 코드 호환성**: `cap_enter()` 이후 글로벌
   네임스페이스가 사라지므로, 기존 프로그램을 캡빌리티
   모드에 맞게 리팩터링해야 한다. 모든 자원을 사전에
   열어야 하고, 지연 초기화 패턴이 깨진다.
2. **프로그래밍 모델의 전환**: 프로그래머가 "필요한 자원을
   미리 열고, 그 다음 격리에 진입한다"는 2단계 사고를
   내재화해야 한다. 이는 습관의 변화를 요구한다.
3. **생태계 관성**: Docker, Android, Chrome이 이미 seccomp
   기반으로 구축됐다. Linux 생태계 전체가 seccomp에
   투자했고, 전환 비용이 막대하다.

### Landlock: Linux의 수렴 진화

기사 말미에 언급된 Landlock(Linux 5.13, 2021)은 의미
심장하다. 파일시스템 샌드박싱을 추가하며 Capsicum의
캡빌리티 모델에 **수렴 진화**하고 있다. Linux가 seccomp의
한계를 인식하고 구조적 접근으로 이동하고 있다는 신호다.

이는 기술 경쟁에서 반복되는 패턴이다. 초기에는 빠르고
실용적인 접근(seccomp)이 승리하지만, 시간이 지나면
구조적으로 건전한 접근(Capsicum)의 아이디어가 흡수된다.
**옳은 아키텍처는 즉시 승리하지 않지만, 결국 영향을
미친다.**

## 타임라인

- **2005**: seccomp strict (Arcangeli) - 4개 시스템 콜만 허용
- **2010**: Capsicum 논문 (Watson, Anderson) -
  USENIX Security Best Student Paper
- **2012**: seccomp-bpf (Drewry) - Linux 3.5
- **2014**: Capsicum 기본 탑재 - FreeBSD 10.0
- **2021**: Landlock - Linux 5.13, 파일시스템 샌드박싱
- **2022**: CVE-2022-30594 - seccomp 우회 취약점

## 참고 자료

- [Capsicum vs seccomp - Vivian Voss](https://vivianvoss.net/blog/capsicum-vs-seccomp)
- [Capsicum: practical capabilities for UNIX - USENIX Security 2010](https://www.usenix.org/conference/usenixsecurity10/capsicum-practical-capabilities-unix)
- [CVE-2022-30594](https://nvd.nist.gov/vuln/detail/CVE-2022-30594)
