# ktransformers

<https://github.com/kvcache-ai/ktransformers>

## 소개

CPU-GPU 이종 컴퓨팅을 통해 대형 언어 모델의 추론과 파인튜닝을 효율적으로 실행하는 프레임워크다.
소비자 하드웨어에서 대형 모델을 실행하는 것이 핵심 목적이다.

두 가지 기능을 제공한다.
첫째, kt-kernel 기반의 고성능 추론 서빙이다.
둘째, LLaMA-Factory를 활용한 SFT(Supervised Fine-Tuning) 파인튜닝이다.

MiniMax-M3, GLM-5.2, DeepSeek-V4-Flash, Kimi-K2.5 같은 모델의 Day0 지원을 목표로 한다.

## 주요 기능

- CPU-GPU Expert 스케줄링 지원
- Native BF16 및 FP8 per-channel 정밀도 지원
- AVX2 전용 CPU 백엔드 지원
- AutoDL 통합 파인튜닝 + 추론 파이프라인
- RL-DPO 파인튜닝 지원 (LLaMA-Factory 연동)

## 분석

### CPU-GPU 이종 컴퓨팅으로 소비자 하드웨어 활용

대형 모델을 GPU VRAM에 완전히 올리려면 고가 서버급 GPU가 필요하다.
ktransformers는 Expert 레이어를 CPU에서 처리하고 나머지를 GPU에서 실행하는 이종 스케줄링으로
소비자급 GPU와 일반 RAM 조합으로 대형 MoE 모델을 실행할 수 있게 한다.

MiniMax-M3, Kimi-K2.5 같은 상업 모델의 Day0 지원은
모델 출시 즉시 로컬 실행이 가능하다는 의미로, 연구자와 개발자에게 중요한 가치다.

## 비평

### 소비자 하드웨어 지원의 실용성

이론적 지원과 실제 사용 가능한 성능은 다르다.
소비자 하드웨어에서 대형 모델을 실행하면 추론 속도가 느려질 수 있다.
실용적인 속도인지, 또는 연구·실험 목적에 한정되는지는
실제 하드웨어 구성에 따라 크게 다르다.

## 인사이트

### 로컬 LLM 실행의 범위가 확장되고 있다

llama.cpp가 소비자 하드웨어에서 7B~13B 모델 실행을 가능하게 한 것처럼,
ktransformers는 수십B~수백B 파라미터 모델의 로컬 실행 범위를 넓히려는 시도다.
CPU-GPU 이종 컴퓨팅이 주류 접근법으로 자리 잡으면
클라우드 API 없이 대형 모델을 연구하는 것이 현실적인 선택이 된다.
