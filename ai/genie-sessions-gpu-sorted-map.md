# Genie Sessions: GPU Sorted Map

Kent Beck의 Genie Sessions 라이브 코딩에서 배운 인사이트.

영상: <https://www.youtube.com/watch?v=58n6ludV-iw>

## 프로젝트 개요

GPU를 활용하여 B+ 트리보다 빠른 정렬된 맵(Sorted Map)을 구현하는 프로젝트.
Rust와 WGPU를 사용하여 크로스 플랫폼 GPU 가속을 구현한다.

### 핵심 API

- `put(key, value)` / `get(key)` / `delete(key)`
- `iterate(key1, key2)` - 특정 키 범위 내 반복
- **Bulk Insert** - 여러 키를 한 번에 삽입
- **Bulk Retrieval** - 여러 키를 한 번에 조회

GPU의 병렬 처리 능력을 활용하려면 대량 연산(Bulk Operations)이 필수다.

## 기술 스택

| 기술       | 용도                                              |
|------------|---------------------------------------------------|
| Rust       | 시스템 프로그래밍 언어                            |
| WGPU       | 크로스 플랫폼 GPU API (Vulkan, Metal, DirectX)    |
| Byte Muck  | 제로 카피 캐스팅으로 GPU 버퍼에 직접 쓰기         |

## WGPU 핵심 개념

| 구성 요소          | 역할                                       |
|--------------------|--------------------------------------------|
| Adapter            | 시스템에서 사용 가능한 GPU 검색 및 선택    |
| Device             | GPU 리소스 생성 및 관리                    |
| Queue              | GPU로 작업 제출, 버퍼에 데이터 쓰기        |
| Buffer             | GPU 메모리 블록                            |
| Shader Module      | WGSL 코드를 컴파일한 GPU 실행 코드         |
| Bind Group         | 실제 버퍼를 셰이더의 바인딩에 연결         |
| Compute Pipeline   | 셰이더 진입점과 파이프라인 레이아웃 연결   |
| Command Encoder    | GPU 명령 기록 및 실행                      |

## 성능 결과

초기에는 GPU put이 느렸으나,
GPU merge 커널을 **Merge Path Style 병렬 커널**로 변경한 결과:

- **GPU put**: 중간~대규모 배치에서 **38% 성능 향상**
- **GPU get**: 대규모 데이터에서 B-tree map보다 훨씬 빠름

각 스레드가 출력 범위의 특정 청크를 병합하도록 설계하여
GPU의 병렬 처리 능력을 극대화했다.

## AI 협업 인사이트

### Augmented Coding

Kent Beck은 AI와의 협업을 "Augmented Coding"(증강 코딩)이라고 부른다.
AI를 단순한 코드 생성기가 아닌 **학습 촉매제**로 활용한다.

### 학습 중심 접근

> AI가 코딩하는 방식처럼 코딩하도록 만드는 것은 잘못된 접근 방식이다.

AI에게 적극적으로 질문하여 복잡한 개념을 이해한다:
- "바인드 그룹이란 무엇인가요?"
- "WGPU의 각 부분에 대해 가르쳐 주세요"
- "동화처럼 이야기해 달라"

### 컨텍스트 관리

AI 에이전트의 컨텍스트 창을 효율적으로 관리하는 것이 중요하다.
AI가 "이상해지기" 시작하면 작업을 더 작은 조각으로 분할한다.

컨텍스트 창의 30~40%를 초과할 때 경고를 주는 도구가 필요하다.

### TDD와 AI

복잡한 GPU 프로그래밍 환경에서도 TDD 방식을 유지한다.
작은 단위의 테스트로 코드의 정확성을 빠르게 확인하고
점진적으로 기능을 추가한다.

## 핵심 교훈

1. **GPU 가속은 대량 연산에서 효과적**
   - 단일 연산보다 Bulk Operations 설계가 중요

2. **병렬화가 성능의 핵심**
   - 단일 스레드 → 병렬 커널로 38% 성능 향상

3. **AI는 학습 도구**
   - 코드 생성뿐 아니라 복잡한 기술을 배우는 리소스로 활용

4. **점진적 접근**
   - CPU 구현 → GPU 구현 순서로 진행
   - 어려우면 CPU로 롤백할 수 있는 유연성 유지

## 관련 문서

- [Vibe Coding](./vibe-coding.md) - Kent Beck의 Augmented Coding
- [Codex](./codex.md) - OpenAI Codex
