# Marp — AI 에이전트를 위한 프레젠테이션 파이프라인

<https://github.com/marp-team/marp>

Markdown을 슬라이드로 변환하는 CLI 도구.
AI 에이전트가 **마크다운을 생성하고 CLI를 호출**하면 프레젠테이션이 완성된다.
사람이 GUI를 만질 필요가 없다.

## 왜 Marp인가 — AI 에이전트 관점

프레젠테이션 도구는 대부분 GUI 기반이다. Keynote, PowerPoint, Google Slides.
AI 에이전트가 이것들을 직접 조작하려면 화면 인식, 클릭 좌표 계산,
API 래핑 같은 간접 경로가 필요하다.

Marp는 다르다. **입력이 텍스트, 출력이 파일, 인터페이스가 CLI**.
AI 에이전트가 가장 잘하는 세 가지와 정확히 일치한다.

```
[AI 에이전트] → 마크다운 생성 → marp CLI 호출 → PDF/PPTX/HTML
```

중간에 사람이 개입할 지점이 없다.

## 에이전트가 알아야 할 Marp 문법

### 슬라이드 구조

`---`로 나눈다. YAML front matter로 전체 설정을 잡는다.

```markdown
---
marp: true
theme: default
paginate: true
header: "프로젝트 보고서"
footer: "2026-03-15"
---

# 제목 슬라이드

발표자: AI Agent

---

# 두 번째 슬라이드

- 항목 1
- 항목 2

---

<!-- _backgroundColor: #264653 -->
<!-- _color: white -->

# 강조 슬라이드
```

### 디렉티브 체계

| 디렉티브          | 범위   | 용도                         |
| ----------------- | ------ | ---------------------------- |
| `theme`           | 글로벌 | 테마 지정                    |
| `paginate`        | 글로벌 | 페이지 번호                  |
| `header`/`footer` | 글로벌 | 머리글/바닥글                |
| `_backgroundColor`| 로컬   | 해당 슬라이드 배경색         |
| `_color`          | 로컬   | 해당 슬라이드 글자색         |
| `_class`          | 로컬   | 해당 슬라이드 CSS 클래스     |
| `_paginate`       | 로컬   | 해당 슬라이드 페이지 번호    |

글로벌은 front matter에, 로컬은 `<!-- _key: value -->` HTML 주석으로 넣는다.
`_` 접두사가 로컬의 표식. 에이전트가 슬라이드별 스타일을 제어할 때 쓴다.

### 내장 테마

`default`, `gaia`, `uncover` 세 가지.
에이전트는 용도에 따라 선택하면 된다.

- `default`: 무난한 기본. 대부분의 상황에 적합.
- `gaia`: 컬러풀. 키노트 스타일에 가까움.
- `uncover`: 미니멀. 텍스트 중심 발표에 적합.

## Marp CLI — 에이전트의 실행 인터페이스

<https://github.com/marp-team/marp-cli>

### 설치 (환경 세팅 자동화)

```bash
# npm (프로젝트 로컬 — CI/CD에 적합)
npm install --save-dev @marp-team/marp-cli

# npx (설치 없이 즉시 실행)
npx @marp-team/marp-cli@latest slide.md

# Docker (환경 격리 — 브라우저 포함)
docker run --rm -v $PWD:/home/marp marpteam/marp-cli slide.md

# 독립 바이너리 (Node.js 불필요)
# GitHub Releases에서 다운로드
```

Docker 이미지에는 헤드리스 브라우저가 포함되어 있다.
CI/CD에서 브라우저 설치를 신경 쓸 필요가 없어진다.

### 변환 명령 — 에이전트가 호출할 패턴들

```bash
# 마크다운 → HTML
marp slide.md -o slide.html

# 마크다운 → PDF
marp slide.md -o slide.pdf

# 마크다운 → PowerPoint
marp slide.md -o slide.pptx

# 마크다운 → 이미지 (슬라이드별)
marp --images png slide.md

# 타이틀 슬라이드만 이미지로 (썸네일 생성)
marp --image png slide.md

# 발표자 노트만 텍스트로 추출
marp slide.md -o notes.txt

# 디렉토리 일괄 변환 (구조 유지)
marp -I ./slides -o ./output

# 병렬 처리 (대량 변환 시)
marp -I ./slides -o ./output -P 10
```

출력 형식은 `-o` 확장자로 자동 감지된다. `slide.pdf`면 PDF, `slide.pptx`면 PPTX.
에이전트는 파일명만 바꾸면 형식이 바뀐다.

### PDF 옵션

```bash
# 발표자 노트를 PDF 주석으로 포함
marp --pdf --pdf-notes slide.md

# 슬라이드 제목을 PDF 북마크로 생성
marp --pdf --pdf-outlines slide.md

# 둘 다
marp --pdf --pdf-notes --pdf-outlines slide.md
```

### 브라우저 제어

PDF/PPTX/이미지 변환은 브라우저 엔진이 렌더링한다.

```bash
# 브라우저 지정
marp --browser chrome slide.md -o slide.pdf
marp --browser firefox slide.md -o slide.pdf

# 브라우저 경로 직접 지정 (비표준 설치 경로)
marp --browser-path /usr/bin/chromium slide.md -o slide.pdf

# 타임아웃 설정 (초 단위, 무거운 슬라이드)
marp --browser-timeout 60 slide.md -o slide.pdf
```

### 종료 코드

| 코드 | 의미               |
| ---- | ------------------ |
| 0    | 성공               |
| 1    | 실패               |

에이전트는 종료 코드로 성공/실패를 판단하고 다음 단계를 결정한다.

## 에이전트 워크플로우 패턴

### 패턴 1: 단순 생성

가장 기본적인 흐름. 에이전트가 마크다운을 쓰고 CLI로 변환한다.

```bash
# 1. 에이전트가 마크다운 파일 생성
cat > slide.md << 'EOF'
---
marp: true
theme: default
paginate: true
---

# 프로젝트 현황 보고

...
EOF

# 2. 변환
marp slide.md -o slide.pdf
```

### 패턴 2: 다중 형식 동시 출력

하나의 소스에서 여러 형식을 뽑는다.
회의실에는 PDF, 웹 공유에는 HTML, 임원에게는 PPTX.

```bash
marp slide.md -o slide.pdf &
marp slide.md -o slide.html &
marp slide.md -o slide.pptx &
wait
```

에이전트가 병렬로 실행하면 된다.

### 패턴 3: 디렉토리 기반 대량 변환

여러 발표 자료를 한 번에 처리한다.

```bash
marp -I ./slides -o ./output --pdf -P 10
```

`-I`로 입력 디렉토리, `-P`로 병렬 수를 지정.
에이전트가 여러 마크다운 파일을 생성한 뒤 한 번의 명령으로 전부 변환한다.

### 패턴 4: CI/CD 파이프라인

Git push → 자동 빌드 → 산출물 배포.

```yaml
# GitHub Actions 예시
- name: Convert slides
  run: npx @marp-team/marp-cli@latest -I ./slides -o ./output --pdf
```

Docker를 쓰면 브라우저 설치 문제가 사라진다.

```yaml
- name: Convert slides
  uses: docker://marpteam/marp-cli:latest
  with:
    args: -I ./slides -o ./output --pdf
```

### 패턴 5: 이미지 추출 → 다른 도구 입력

슬라이드를 이미지로 뽑아서 다른 AI 도구의 입력으로 쓴다.

```bash
# 슬라이드를 PNG로 추출
marp --images png slide.md

# → slide.001.png, slide.002.png, ...
# → 이미지 분석 AI에 전달하여 리뷰 자동화
```

## 분석

### 텍스트 입력 + CLI 실행 = AI 에이전트 최적 인터페이스

Marp가 AI 에이전트에게 이상적인 이유는 **인터페이스의 본질** 때문이다.

GUI 기반 도구를 자동화하려면 **화면을 보는 눈**이 필요하다.
API 기반 도구를 자동화하려면 **인증과 네트워크**가 필요하다.
CLI 기반 도구를 자동화하려면 **셸 명령 한 줄**이면 된다.

AI 에이전트는 텍스트를 생성하고, 명령을 실행하고, 종료 코드를 읽는다.
Marp CLI의 인터페이스는 이 능력 범위와 완벽히 겹친다.

### 마크다운의 생성 용이성

프레젠테이션 포맷 중 AI가 생성하기 가장 쉬운 것이 마크다운이다.
JSON 스키마를 지킬 필요도 없고, XML 네임스페이스를 맞출 필요도 없다.
**자연어에 가장 가까운 구조화된 포맷**이 마크다운이다.

AI 에이전트가 "3장짜리 프로젝트 보고서 슬라이드를 만들어"라는 요청을 받으면,
마크다운을 생성하는 것은 자연어 생성의 연장선에 불과하다.
별도의 포맷 변환 레이어가 필요 없다.

### 브라우저 의존성의 양면

PDF/PPTX 변환이 헤드리스 브라우저에 의존한다.
CSS 렌더링을 브라우저에 위임하므로 **출력 품질은 브라우저 수준**으로 보장된다.

대신 에이전트 실행 환경에 브라우저가 설치되어 있어야 한다.
Docker 이미지를 쓰면 해결되지만, 환경 제약이 있는 경우 걸림돌이 된다.

### 레이어드 아키텍처의 확장 가능성

Marpit → Marp Core → Marp CLI 3계층 구조.
에이전트가 CLI를 쓰는 한 내부 구조를 알 필요는 없지만,
**커스텀 테마나 플러그인**을 만들어야 할 때 이 분리가 의미를 갖는다.
Marpit 기반으로 자체 변환 파이프라인을 구축하는 것도 가능하다.

## 비평

### AI 에이전트 도구로서의 강점

**제로 인터랙션 변환**. 입력(마크다운 파일)과 출력(PDF/PPTX/HTML)이 명확하다.
중간에 "확인" 버튼을 누르거나 대화 상자에 응답할 필요가 없다.
에이전트는 파일을 쓰고, 명령을 실행하고, 결과 파일을 확인하면 된다.

**결정론적 출력**. 같은 마크다운 + 같은 CLI 옵션이면 같은 결과가 나온다.
에이전트가 결과를 예측할 수 있고, 실패 시 원인을 추적할 수 있다.

**파이프라인 조합성**. 에이전트가 데이터를 수집 → 마크다운 생성 → Marp 변환 →
결과 파일 배포까지 **하나의 셸 스크립트**로 엮을 수 있다.
다른 CLI 도구들과 자연스럽게 조합된다.

### AI 에이전트 도구로서의 약점

**시각적 피드백 부재**. 에이전트가 슬라이드를 생성해도 **결과를 볼 수 없다**.
마크다운 문법은 맞는데 시각적으로 깨지는 경우를 감지하지 못한다.
"텍스트가 슬라이드 밖으로 넘침", "이미지가 잘림" 같은 문제는
이미지로 변환 후 비전 모델에 넘겨야 검증할 수 있다.

**레이아웃 제어의 거칠기**. CSS로 레이아웃을 잡아야 하는데,
AI 에이전트가 생성하는 CSS의 품질이 균일하지 않다.
내장 테마를 쓰고 커스텀 CSS를 최소화하는 것이 안전한 전략이다.

**편집 가능 PPTX의 미완성**. `--pptx-editable`은 실험적 상태다.
"AI가 초안을 만들고 사람이 PPTX로 편집"이라는 워크플로우는 아직 불안정하다.
현실적으로는 PDF 출력에 집중하는 것이 낫다.

### 생태계 상태

Marp Web, Marp React, Marp Vue가 모두 비활성 상태다.
핵심인 CLI와 VS Code 확장만 유지되고 있다.
에이전트 관점에서는 **CLI만 살아있으면 충분**하므로 큰 문제는 아니다.

## 인사이트

### 프레젠테이션은 "AI가 자동화하기 가장 쉬운 문서 유형"이 된다

문서 유형별 AI 자동화 난이도를 생각해보면:

- **코드**: 구문 검사, 테스트로 검증 가능. 자동화 성숙도 높음.
- **이메일/보고서**: 텍스트 생성이 핵심. AI가 잘하는 영역.
- **프레젠테이션**: GUI 조작이 필요했으므로 자동화가 어려웠다.
- **디자인 산출물**: 시각적 판단이 필수. 자동화 난이도 높음.

Marp가 프레젠테이션을 **텍스트 생성 문제**로 환원시킨다.
프레젠테이션이 "AI가 손대기 어려운 영역"에서
"이메일만큼 쉬운 영역"으로 이동한다.

### "생성 → 변환 → 검증" 파이프라인의 가능성

에이전트가 Marp CLI를 활용하는 최적의 흐름:

1. **생성**: 마크다운으로 슬라이드 내용 작성.
2. **변환**: `marp slide.md -o slide.pdf`로 산출물 생성.
3. **검증**: `marp --images png slide.md`로 이미지 추출 → 비전 모델로
   레이아웃 깨짐, 텍스트 오버플로우 등을 검사.
4. **수정**: 검증 결과를 바탕으로 마크다운 수정 → 2번으로 돌아감.

이 루프가 성립하면 **사람 개입 없이 품질 관리까지 자동화**된다.

### CLI 도구 선택의 기준이 바뀐다

전통적으로 도구를 선택할 때 "UX가 좋은가", "학습 곡선이 낮은가"를 봤다.
AI 에이전트 시대에는 기준이 달라진다:

- **입력이 텍스트인가?** — AI가 생성할 수 있는가.
- **인터페이스가 CLI인가?** — AI가 실행할 수 있는가.
- **출력이 파일인가?** — AI가 결과를 확인할 수 있는가.
- **결정론적인가?** — 같은 입력에 같은 출력이 나오는가.

Marp는 네 가지를 모두 만족한다.
이 기준으로 보면 Marp는 "프레젠테이션 도구" 중에서
AI 에이전트 친화도가 가장 높은 도구다.

### 프레젠테이션의 탈-디자인화

Marp + AI 에이전트 조합이 시사하는 것은
**프레젠테이션에서 디자인의 비중이 줄어든다**는 것이다.
내장 테마를 쓰고, 내용만 잘 정리하면 "충분히 괜찮은" 슬라이드가 나온다.

이것은 열화가 아니라 **관심사의 분리**다.
내용은 AI가 생성하고, 디자인은 테마가 담당한다.
"디자인을 잘 못해서 슬라이드를 못 만든다"는 병목이 사라진다.

## 참고 자료

- [Marp 공식 저장소](https://github.com/marp-team/marp)
- [Marp CLI](https://github.com/marp-team/marp-cli)
- [Marpit 프레임워크](https://github.com/marp-team/marpit)
- [Marp Core](https://github.com/marp-team/marp-core)
- [Marp for VS Code](https://github.com/marp-team/marp-vscode)
