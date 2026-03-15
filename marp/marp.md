# Marp — Markdown Presentation Ecosystem

<https://github.com/marp-team/marp>

Markdown으로 프레젠테이션을 만드는 생태계.
슬라이드 덱을 **일반 마크다운 문서**로 작성하고,
HTML, PDF, PPTX, 이미지로 변환한다.

## 생태계 구성

| 구성 요소          | 역할                                        |
| ------------------ | ------------------------------------------- |
| Marpit             | 마크다운 → 슬라이드 변환 프레임워크 (최소 코어) |
| Marp Core          | 실전용 변환기. 내장 테마와 확장 문법 제공       |
| Marp CLI           | CLI 도구. HTML/PDF/PPTX/이미지 변환            |
| Marp for VS Code   | VS Code 확장. 실시간 미리보기                   |

Marpit이 markdown-it 파서를 확장해서 슬라이드 분할과 디렉티브를 처리하고,
Marp Core가 그 위에 테마·수식·코드 하이라이팅 등 실용 기능을 얹는 구조다.

## 핵심 개념

### 슬라이드 분할

수평선(`---`)으로 슬라이드를 나눈다. 이게 전부다.

```markdown
# 첫 번째 슬라이드

내용

---

# 두 번째 슬라이드

내용
```

### 디렉티브

YAML front matter 또는 HTML 주석으로 슬라이드 속성을 제어한다.

```markdown
---
marp: true
theme: default
paginate: true
---

# 제목 슬라이드

---

<!-- _backgroundColor: #264653 -->
<!-- _color: white -->

# 다크 슬라이드
```

- **글로벌 디렉티브**: `theme`, `paginate`, `header`, `footer` 등. 전체 덱에 적용.
- **로컬 디렉티브**: `_`(언더스코어) 접두사. 해당 슬라이드에만 적용.

### 테마

CSS로 테마를 만든다. 프레임워크 전용 클래스 없이 **순수 HTML 요소**에
스타일을 입히는 방식. 내장 테마는 `default`, `gaia`, `uncover` 세 가지.

### Inline SVG 슬라이드

슬라이드를 `<svg>` + `<foreignObject>`로 감싸서 **픽셀 퍼펙트 스케일링**을
CSS만으로 구현한다. 해상도 독립적인 렌더링이 가능해지는 핵심 기법.

## Marp CLI

<https://github.com/marp-team/marp-cli>

### 설치

```bash
# npx로 즉시 실행 (설치 불필요)
npx @marp-team/marp-cli@latest slide-deck.md

# Homebrew (macOS/Linux)
brew install marp-cli

# npm 글로벌
npm install -g @marp-team/marp-cli

# Docker
docker run --rm -v $PWD:/home/marp marpteam/marp-cli slide-deck.md
```

독립 실행 바이너리도 제공한다. Node.js 없이도 사용 가능.

### 변환

```bash
# HTML (기본)
marp slide.md -o slide.html

# PDF
marp --pdf slide.md

# PowerPoint
marp --pptx slide.md

# 편집 가능한 PPTX (실험적, LibreOffice Impress 필요)
marp --pptx --pptx-editable slide.md

# 이미지 (각 슬라이드별)
marp --images png slide.md

# 발표자 노트만 텍스트로 추출
marp slide.md -o notes.txt
```

PDF/PPTX/이미지 변환에는 Chrome, Edge, Firefox 중 하나가 필요하다.
브라우저 엔진을 사용해서 렌더링하기 때문이다.

### 워치 모드와 서버 모드

```bash
# 파일 변경 감지 → 자동 재변환
marp -w slide.md

# HTTP 서버로 실행
marp -s ./slides

# 포트 지정
PORT=3000 marp -s ./slides
```

서버 모드에서는 쿼리 파라미터로 형식을 지정할 수 있다.
`http://localhost:8080/slide.md?pdf` 식으로 접근하면 PDF로 변환해준다.

### 주요 옵션

| 옵션                    | 설명                              |
| ----------------------- | --------------------------------- |
| `-o, --output`          | 출력 경로 지정                    |
| `-I, --input-dir`       | 입력 디렉토리 (구조 유지 변환)    |
| `-P, --parallel`        | 병렬 처리 수 (기본 5)             |
| `--pdf-notes`           | PDF에 발표자 노트 포함            |
| `--pdf-outlines`        | PDF에 북마크 생성                 |
| `--image-scale`         | 이미지 해상도 배율                |
| `--browser`             | 사용할 브라우저 지정              |
| `--allow-local-files`   | 로컬 파일 접근 허용 (보안 주의)   |

## 분석

### 설계 철학

Marp의 핵심 설계 결정은 **"마크다운 문서 그 자체가 프레젠테이션"**이라는 전제다.
별도의 DSL을 만들지 않고, 표준 마크다운에 최소한의 확장만 얹었다.
`---`로 슬라이드를 나누고, YAML front matter로 설정하는 것이 문법의 거의 전부다.

이 접근은 **학습 비용을 사실상 제로**에 가깝게 만든다.
마크다운을 쓸 줄 아는 사람은 5분 안에 첫 슬라이드를 만들 수 있다.

### 아키텍처: 레이어드 분리

Marpit(프레임워크) → Marp Core(실전 기능) → Marp CLI/VS Code(인터페이스)
이 3계층 분리가 깔끔하다.

- Marpit은 **최소 자산 출력**에 집중. 슬라이드 분할과 디렉티브 처리만 한다.
- Marp Core는 Marpit 위에서 테마, 수식(KaTeX), 코드 하이라이팅을 추가한다.
- CLI와 VS Code는 순수한 프런트엔드 역할.

이 분리 덕분에 커스텀 변환기를 만들 수 있다.
Marpit 기반으로 자체 슬라이드 도구를 구축하는 것도 가능하다.

### 브라우저 의존성

PDF/PPTX 변환이 **브라우저 엔진에 의존**한다는 점이 독특하다.
HTML/CSS 렌더링을 브라우저에 위임하고, 그 결과를 캡처하는 방식이다.
장점은 CSS 호환성이 완벽하다는 것. 브라우저가 렌더링하니까.
단점은 **헤드리스 브라우저 설치가 필수**라는 것. CI/CD에서 귀찮아진다.

## 비평

### 강점

**마크다운 네이티브**. Git으로 버전 관리되고, 텍스트 에디터로 편집되고,
diff로 변경 이력을 추적할 수 있다. 프레젠테이션을 **코드처럼** 다룰 수 있다.

**VS Code 통합**이 실전에서 큰 차이를 만든다.
마크다운을 편집하면서 옆에서 실시간으로 슬라이드를 확인할 수 있다.
별도 앱을 오갈 필요가 없다.

**출력 형식의 유연성**. 같은 소스에서 HTML(웹 공유), PDF(인쇄),
PPTX(기업 환경) 모두 만들 수 있다.

### 약점

**레이아웃 제어의 한계**. CSS로 할 수 있는 것이 전부다.
PowerPoint나 Keynote의 자유로운 오브젝트 배치에 비하면 제약이 크다.
그리드 레이아웃이나 복잡한 다이어그램 배치는 CSS 숙련도를 요구한다.

**편집 가능 PPTX의 미완성**. `--pptx-editable`은 "실험적"이라고 명시되어 있고,
LibreOffice Impress를 요구하며 복잡한 테마에서 결과가 불완전하다.
"마크다운으로 만들고 파워포인트로 편집"이라는 워크플로우가 아직은 불안정하다.

**생태계 축소**. Marp Web(PWA), Marp React, Marp Vue가 모두 "inactive/outdated"
상태다. 핵심 도구(CLI, VS Code)에 집중하는 것은 현실적이지만,
웹 기반 편집이나 프레임워크 통합은 사실상 포기한 상태다.

## 인사이트

**"텍스트가 진실의 원천"이라는 원칙의 프레젠테이션 적용**.
코드에서 "소스 코드가 문서다"라는 철학이 있듯이,
Marp는 "마크다운이 프레젠테이션이다"를 실현한다.
바이너리 파일 포맷(`.pptx`, `.key`)이 아닌
**사람이 읽을 수 있는 텍스트**가 원본이 된다.

**개발자 워크플로우와의 자연스러운 통합**.
슬라이드를 Git으로 관리하면 PR 리뷰, CI/CD 자동 빌드,
브랜치별 버전 관리가 가능해진다.
발표 자료를 **코드 리뷰**할 수 있다는 것 자체가 팀 문화를 바꿀 수 있다.

**Marp CLI 서버 모드의 활용 가능성**.
`marp -s ./slides`로 로컬 서버를 띄우고 `?pdf` 쿼리로 실시간 변환하는 패턴은,
발표 직전에 최종 PDF를 뽑거나,
여러 형식을 즉석에서 제공하는 워크플로우에 적합하다.

**"충분히 좋은" 프레젠테이션 도구**.
Marp의 진짜 경쟁 상대는 Keynote나 PowerPoint가 아니다.
**"프레젠테이션을 안 만들기"**가 경쟁 상대다.
마크다운으로 내용을 정리하면 그것이 곧 슬라이드가 되니,
프레젠테이션 제작의 심리적 장벽이 낮아진다.
디자인에 시간을 쓰지 않고 **내용에 집중**할 수 있다.

## 참고 자료

- [Marp 공식 저장소](https://github.com/marp-team/marp)
- [Marp CLI](https://github.com/marp-team/marp-cli)
- [Marpit 프레임워크](https://github.com/marp-team/marpit)
- [Marp Core](https://github.com/marp-team/marp-core)
- [Marp for VS Code](https://github.com/marp-team/marp-vscode)
