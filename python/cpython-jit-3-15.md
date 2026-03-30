# CPython 3.15 JIT, 다시 궤도에 오르다

- 원문: <https://blog.python.org/2026/03/jit-on-track/>

## 요약

Python 공식 블로그에 게재된 CPython JIT 컴파일러 개발 현황 업데이트다.
3.13에서 실험적으로 도입된 JIT 컴파일러가 3.15를 목표로 본격적인 성능
개선 단계에 접어들었음을 알린다.

## 배경

CPython은 오랫동안 인터프리터 방식으로만 동작했다.
3.11의 Specializing Adaptive Interpreter로 첫 번째 최적화 레이어를 도입했고,
3.13에서 Copy-and-Patch JIT를 실험적 플래그로 추가했다.

## 현재 상태

- 기본 활성화를 위한 성능 임계값 접근 중
- Copy-and-Patch 방식으로 JIT 코드 생성 오버헤드 최소화
- 특정 벤치마크에서 의미 있는 개선 확인

## 인사이트

### 1) Python JIT는 "빠른 Python"이 아니라 "더 이상 느리다는 말을 듣지 않는 Python"이다

Python의 성능 문제는 실제 병목보다 인식의 문제가 더 크다.
대부분의 애플리케이션에서 성능 병목은 I/O나 외부 서비스이지 Python 자체가 아니다.

그러나 JIT로 벤치마크 수치가 개선되면 "Python은 느리다"는 선입견이 줄어들고,
성능이 중요한 영역에서의 도입 저항도 낮아진다.

### 2) Copy-and-Patch JIT는 구현 복잡도와 성능 사이의 현실적 타협이다

LLVM 기반 JIT는 강력하지만 빌드 의존성이 무겁고 포팅이 복잡하다.
Copy-and-Patch는 미리 컴파일된 템플릿을 복사하고 주소만 패치하는 방식으로
JIT 코드 생성 비용을 크게 줄인다.

CPython 개발팀이 이상적인 JIT보다 배포 가능한 JIT를 선택한 것이다.

### 3) Python 성능 개선의 복리 효과

3.11 Adaptive Interpreter → 3.13 JIT 실험 → 3.15 JIT 안정화로 이어지는
흐름은 매 버전마다 성능이 누적된다는 신호다.

PyPy나 다른 대안 없이도 CPython 자체가 성능 플랫폼으로 진화하고 있다.
Python을 선택하는 이유에 "충분히 빠르다"가 더 강하게 추가되는 추세다.
