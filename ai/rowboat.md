# Rowboat - 오픈소스 AI 코워커

<https://www.rowboatlabs.com/>

<https://github.com/rowboatlabs/rowboat>

업무 내용을 Knowledge Graph로 변환하고
이를 바탕으로 행동하는 오픈소스 AI 코워커.

이메일, 회의록 등을 연결해 지속적인
지식 베이스를 구축하고, 축적된 맥락을 활용해
업무를 처리한다.

Y Combinator S24 배치 출신.

## 핵심 특징

### 로컬 퍼스트(Local-First)

모든 데이터를 사용자의 로컬 머신에
플레인 마크다운 파일로 저장한다.
Obsidian 호환 Vault 형태로 관리되므로
기존 Obsidian 워크플로와 함께 사용 가능.

독점 포맷이나 호스팅 종속(Lock-in)이 없다.

### 투명한 메모리(Transparent Memory)

지식이 모델 파라미터 안에 숨겨지는 것이 아니라
편집 가능한 마크다운 파일로 명시적으로 저장된다.
사용자가 직접 확인하고 수정할 수 있다.

### 복리 맥락(Compounding Context)

세션마다 맥락을 새로 구성하는 것이 아니라
시간이 지날수록 정보가 축적되어
더 풍부한 맥락을 제공한다.

## 주요 기능

- Knowledge Graph 구축 및 시각화
- 회의 브리핑 자동 생성
- 프레젠테이션(PDF) 생성
- 이메일 초안 작성
- 음성 메모 녹음 및 핵심 요약 자동 추출
- 의사결정, 액션 아이템, 담당자 캡처

## Background Agents

반복적인 업무를 자동화하는 백그라운드 에이전트:

- 이메일 답장 초안 작성
- 일일 음성 브리핑 생성
- 프로젝트 업데이트 작성
- Knowledge Graph 유지보수

## 연동(Integrations)

- Gmail
- Granola (회의록)
- Fireflies (회의록)
- Google Calendar
- Google Drive

MCP(Model Context Protocol)를 통해
검색 엔진, 데이터베이스, CRM 등
외부 도구와 연결 가능.

## 모델 유연성

- 로컬 모델: Ollama, LM Studio
- 호스팅 모델: 사용자 API 키로 연결
- 모델 교체 시 로컬 데이터에 영향 없음

## 기술 스택

- TypeScript (96.8%)
- Electron (Mac/Windows/Linux)
- CSS, MDX, Python, JavaScript, Docker

## 설치

다운로드:
<https://www.rowboatlabs.com/downloads>

선택 사항:

- Gmail/Calendar/Drive 연동을 위한
  Google OAuth 설정
- 음성 메모 전사를 위한 Deepgram API 키
