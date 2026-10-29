# 두 번째 뇌를 시험하는 법: 위키는 모델이 쓰고 검사는 코드가 한다

트윗: [The Second Brain Guide: How to Stop Re-Explaining Yourself to Claude (Full Build)](https://twitter.com/danikkk_wqs/status/2113001913662734619)

## 소개

Brucky(`@danikkk_wqs`)가 2026년 10월 22일에 올린 Twitter Article이며,
읽는 데 7분이 걸린다고 표시되고 조회수는 18만 5천 회다.
글의 문제의식은 Claude 세션이 매번 빈 상태로 시작해서 프로젝트, 결정, 사람,
지난주에 시도한 것을 다시 설명해야 한다는 것이다.
해법은 두 번째 뇌(second brain)이며, Claude가 읽고 스스로 쓰고 유지하는 일반
텍스트 파일 폴더다.
저자는 이 방식을 Andrej Karpathy가 2026년 4월에 설명한 패턴이라고 소개하면서,
그의 gist가 별 5천 개 이상과 포크 5천 개 이상을 받았다고 적는다.
이 문서는 그 수치를 직접 확인하지 않았고, 저자의 서술로만 옮긴다.

글이 남들의 복제본과 다르다고 내세우는 점은 시험이다.
저자는 위키에 거짓 문장 하나, 곧 Bush가 1941년에 하이퍼텍스트를 발명했다는
문장을 심었다.
원본 파일에는 그런 내용이 없다.
“위키의 오류를 확인해 줘”라고 모델에게 시키면 그럴듯한 문장은 통과시킬 것이므로,
저자는 AI가 들어 있지 않은 95줄 스크립트로 그 문장을 잡았다고 한다.
스크립트의 출력은 해당 페이지에서 인용이 원본에 없다고 보고한다.

이 문서는 글을 실무 노트로 재구성한다.
글의 프롬프트와 설정은 그대로 옮기지 않고 구조와 판단 기준만 정리하며,
린트 스크립트는 글의 부록 코드가 아니라 같은 규칙을 이 문서가 새로 짜서
시험한 것이다.
글의 주장과 이 문서의 해석은 구분해서 적는다.
claude-obsidian 같은 완성된 도구를 다룬 `agent-skill/claude-obsidian.md`와 같은
계열의 주제이며, 이 글의 고유한 부분은 도구가 아니라 검사를 코드로 옮긴 점이다.

## 동작 방식

일반적인 AI 파일 검색은 RAG처럼 질문마다 조각을 찾아 지식을 처음부터 다시
발견한다는 것이 글의 설명이다.
Karpathy의 패턴은 이를 뒤집어서 모델이 출처와 사람 사이에 링크된 마크다운
페이지로 이루어진 위키를 짓고 유지하게 한다.
글이 인용하는 역할 분담은 Obsidian이 IDE, LLM이 프로그래머, 위키가 코드베이스다.
모델에게 맡기는 이유는 사람이 위키를 버리는 까닭이 유지 비용이 가치보다 빨리
커지기 때문이고, LLM은 지루해하지 않고 상호 참조를 잊지 않으며 한 번에 파일
열다섯 개를 만질 수 있기 때문이라고 한다.

구성은 세 층과 세 동작이다.

| 층          | 내용                        | 모델의 권한   |
| ----------- | --------------------------- | ------------- |
| `raw/`      | 사용자가 넣은 원본 자료     | 읽기만        |
| `wiki/`     | 모델이 쓰고 유지하는 페이지 | 읽기와 쓰기   |
| `CLAUDE.md` | 규칙: 관례와 작업 흐름      | 사용자가 정함 |

세 동작은 ingest(자료를 넣으면 모델이 페이지 10~15개에 통합),
query(질문하고 좋은 답은 위키에 되돌려 저장), lint(모순, 낡은 주장,
고아 페이지 찾기)다.
글은 Karpathy가 코드가 아니라 아이디어 파일로 공개했다고 하며,
에이전트가 각자의 필요에 맞게 짓게 하려는 의도라고 전한다.

이 문서의 해석으로는 이 구조의 핵심은 쓰는 쪽과 검사하는 쪽의 분리다.
`raw/`는 모델이 고치지 못하는 사실의 층이고,
`wiki/`는 모델이 고치는 해석의 층이다.
검사의 기준이 되는 것은 항상 사실의 층이어야 하며,
이것이 뒤의 린트가 성립하는 전제다.

## 구현하기

### 폴더와 규칙 만들기

글의 첫 단계는 폴더 네 개와 저장소 하나를 만드는 일이다.

```bash
mkdir -p brain/{raw,wiki,output,.brain}
cd brain && git init
claude
```

Obsidian은 그래프 보기를 원할 때만 이 폴더를 볼트로 열면 된다.
글은 Local REST API 플러그인과 MCP 서버를 거치라는 안내가 많지만,
실행 중인 Obsidian과 대화할 때만 필요하다고 한다.
`CLAUDE.md`는 Claude가 사용자를 한 번에 한 질문씩 인터뷰해서 쓰게 하라는 것이
글의 제안이며, 물을 항목은 사용자가 누구인지, 올해 목표, 소통 방식, 강점과 약점,
현재 프로젝트다.
파일 이름은 담긴 내용을 따라 짓고(`tax-policy.md`처럼, `note-12.md`는 금지),
소문자와 하이픈을 쓰며, 한 파일은 한 주제만 다룬다.

### 모든 주장에 인용 줄을 붙이기

글이 린트를 가능하게 만드는 ingest 규칙으로 꼽는 것은 각 구체적 주장이 아래
형식의 줄을 달고 나오는 것이다.

```text
> "원본에 있는 문장 그대로" - raw/파일이름.md
```

인용 줄이 있어야 스크립트가 원본 파일에서 그 문장을 단어 그대로 찾을 수 있다.
페이지 맨 위에는 `title`, `sources`, `updated` 세 항목을 가진 프론트매터를 둔다.

### 결정론적 린트 스크립트

글의 부록 코드는 붙여넣기 과정에서 들여쓰기가 사라진 형태로 읽혔다.
그래서 이 문서는 글이 말한 검사 규칙을 같은 목록으로 새로 구현하고 직접
돌려 보았다.
글이 열거한 규칙은 모든 페이지의 프론트매터, 나열된 출처의 존재,
`[[링크]]`의 해석 가능성, 고아 페이지와 남은 TODO 없음,
수집 뒤 바뀐 원본 파일의 표시, 인용한 주장이 원본에 글자 그대로 존재함이다.
`status`는 수집 이후 새로 생기거나 바뀌거나 지워진 원본만 보여 주고,
`done`은 수집을 마친 원본의 해시를 기록하며, `lint`는 위 규칙을 검사한다.

```python
#!/usr/bin/env python3
"""brain.py: LLM 없이 위키를 검사하는 결정론적 도구. status | done | lint"""
import hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
RAW, WIKI = ROOT / "raw", ROOT / "wiki"
MANIFEST = ROOT / ".brain" / "manifest.json"
SPECIAL = {"index", "hot", "log"}
LINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
# 인용 줄 형식: > "원문 그대로" - raw/파일
QUOTE = re.compile(r'^>\s*"(.+?)"\s*[-–—]+\s*(raw/\S+)\s*$', re.M)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def rel(path):
    return str(path.relative_to(ROOT))


def norm(text):
    return " ".join(text.split())


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def status():
    manifest, pending = load(), []
    for path in sorted(p for p in RAW.rglob("*") if p.is_file()):
        key = rel(path)
        if key not in manifest:
            pending.append(("NEW", key))
        elif manifest[key]["sha"] != digest(path):
            pending.append(("CHANGED", key))
    pending += [("DELETED", k) for k in manifest if not (ROOT / k).exists()]
    for kind, key in pending:
        print(kind, key)
    return 0


def done(raw, pages):
    manifest = load()
    manifest[raw] = {"sha": digest(ROOT / raw), "pages": pages}
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


def lint():
    errors, texts = [], {p.stem: (p, p.read_text()) for p in sorted(WIKI.rglob("*.md"))}
    inbound = {name: 0 for name in texts}
    for name, (path, text) in texts.items():
        if name in SPECIAL:
            continue
        fields = frontmatter(text)
        if fields is None:
            errors.append(f"{rel(path)}: 프론트매터 없음")
            continue
        for need in ("title", "sources", "updated"):
            if need not in fields:
                errors.append(f"{rel(path)}: 프론트매터에 '{need}' 없음")
        for src in re.findall(r"raw/[^\s,\]\[]+", fields.get("sources", "")):
            if not (ROOT / src).exists():
                errors.append(f"{rel(path)}: 출처 {src} 없음")
        for target in LINK.findall(text):
            if target not in texts:
                errors.append(f"{rel(path)}: 끊어진 링크 [[{target}]]")
            elif target != name:
                inbound[target] += 1
        for quote, src in QUOTE.findall(text):
            source = ROOT / src
            if not source.exists():
                errors.append(f"{rel(path)}: 인용이 없는 파일 {src}를 가리킴")
            elif norm(quote) not in norm(source.read_text()):
                errors.append(f"{rel(path)}: QUOTE NOT IN SOURCE -> {quote[:50]!r} ({src})")
        if "TODO" in text:
            errors.append(f"{rel(path)}: 남은 TODO")
    for name, count in inbound.items():
        if count == 0 and name not in SPECIAL:
            errors.append(f"{rel(texts[name][0])}: 고아 페이지(들어오는 링크 없음)")
    for key, entry in load().items():
        if (ROOT / key).exists() and digest(ROOT / key) != entry["sha"]:
            errors.append(f"{key}: 수집 뒤 바뀜, 낡은 페이지: {', '.join(entry['pages'])}")
    for line in errors:
        print(line, file=sys.stderr)
    print(f"lint: 페이지 {len(texts)}개에서 문제 {len(errors)}건", file=sys.stderr)
    return 2 if errors else 0


if __name__ == "__main__":
    command, args = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    actions = {"status": lambda: status(), "lint": lambda: lint(),
               "done": lambda: done(args[0], args[1:])}
    sys.exit(actions.get(command, lambda: print(__doc__) or 1)())
```

### Claude Code에 걸기

글은 설정 파일로 `raw/`를 읽기 전용으로 만들고, 위키 편집 직후 린트를 돌리고,
세션 시작 때 상태를 주입하는 구성을 제시한다.
글의 설정 요지는 다음과 같다.
`permissions.deny`에 `Edit(/raw/**)`를 넣으면 `raw/`가 읽기 전용이 되고,
글은 `Write(raw/**)` 규칙은 받아들여지지만 쓰이지 않는다고 주장한다.
`PostToolUse` 훅은 `Edit|Write` 뒤에 린트를 돌려 종료 코드 2를 돌려주며,
글에 따르면 도구가 이미 실행된 뒤라서 편집을 되돌리지는 못하지만 오류 문장이
Claude에게 전달되어 같은 턴에 고친다.
`SessionStart` 훅은 `hot.md`와 대기 중인 수집 목록을 컨텍스트에 넣고,
매처 값은 `startup`, `resume`, `clear`,
`compact`라서 `/clear` 뒤에도 브리핑이 남는다.
이 문서는 이 동작을 Claude Code 문서와 대조하지 않았으므로,
적용 전에 사용하는 버전에서 직접 확인해야 한다.

글이 권하는 수집 명령은 `.claude/skills/ingest/SKILL.md`에 두고
`disable-model-invocation: true`로 사람이 직접 부르게 하는 것이다.
파일을 다시 쓰는 작업이므로 사람의 호출로 한정하는 것이 맞다는 이유다.
수집이 끝날 때마다 커밋하면 diff가 모델이 지식에 한 변경을 정확히 보여 주고,
잘못된 수집은 되돌리기 한 번이면 취소된다고 한다.

### 여러 프로젝트가 한 볼트를 보게 하기

글이 가장 좋은 아이디어로 꼽는 것은 프로젝트마다 두 번째 뇌를 짓지 말고 모든
Claude Code 프로젝트를 같은 볼트에 연결하는 것이다.
각 프로젝트의 `CLAUDE.md`에 볼트 경로를 적고, 읽는 순서를 `hot.md`, `index.md`,
도메인 하위 색인, 개별 페이지로 정한다.
범용 코딩 질문에는 위키를 읽지 말라는 줄이 비용 통제라고 글은 말한다.
`hot.md`는 열두 줄 정도로 지금 하는 일, 마지막 변경, 열린 질문만 적고,
큰 색인을 `@index.md`로 가져오지 말라고 한다. 가져오기는 시작할 때 읽혀 파일을
붙여넣은 것과 같은 컨텍스트를 쓰기 때문이다.

## 값 정하기

글은 숫자를 몇 개 주지만 대부분 경고용이다.
아래는 글의 수치에 이 문서가 시작값과 근거를 붙인 표다.
수치의 출처는 글이며 이 문서가 확인하지 않았다.

| 값                    | 글이 주는 수치              | 시작값과 근거                                                            |
| --------------------- | --------------------------- | ------------------------------------------------------------------------ |
| 위키를 도입할 자료 수 | 약 50~100개 아래는 사각지대 | 그 아래에서는 검색 엔진과 비슷하므로 설정 비용만 든다는 것이 글의 경고다 |
| `hot.md` 길이         | 열두 줄 안팎                | 매 세션 컨텍스트에 들어가므로 짧게 유지한다                              |
| 자동 메모리 한도      | 첫 200줄 또는 25KB          | 글의 주장이며, 넘는 부분은 읽히지 않는다고 하므로 요약을 짧게 둔다       |
| 수집당 갱신 페이지 수 | 10~15개                     | 한 번에 건드리는 범위이며, 잘못된 자료가 퍼지는 폭이기도 하다            |
| 린트 실행 시점        | 위키 편집 직후              | 같은 턴에 모델이 고치게 하려면 편집 직후가 가장 빠르다                   |

측정할 것은 린트가 잡은 건수의 추이, 수집당 변경된 페이지 수,
세션 시작 때 주입한 문서의 토큰 수다.
글이 인용하는 R&D World의 한 달 후기는 약 760페이지에 이르렀고 좁은 용도에서는
보통 수준의 도움이며 한 달 시점에는 유지 시간과 절약 시간이 비슷했다고 한다. 이
문서는 그 후기를 열어 보지 않았다.

## 트레이드오프

### 모델이 쓰고 같은 모델이 검사하면 검사가 되지 않는다

위키를 쓴 모델에게 오류를 찾게 하면 자기 작업에 동의하는 경향이 있다는 것이
글의 출발점이다.
결정론적 스크립트로 검사를 옮기면 비용이 0 토큰이고 걸리는 시간은 밀리초이며
결과가 매번 같다.
대신 잡는 것은 구조와 인용 일치뿐이다.
글도 린트는 진실이 아니라 구조와 인용을 검사하며,
틀린 원본은 충실하게 틀린 위키를 만든다고 인정한다.
이 문서의 해석으로는 이 한계가 설계의 경계선이다.
스크립트는 위키가 원본을 정확히 옮겼는지만 보증하고,
원본이 맞는지는 사람이나 독립된 출처가 판정해야 한다.

### 인용 줄을 강제하면 위키가 짧아지고 믿을 만해진다

모든 구체적 주장에 인용 줄을 요구하면 모델이 원본에 없는 일반론을
쓰기 어려워진다.
얻는 것은 환각의 차단이고, 잃는 것은 여러 원본을 종합한 문장을 쓰기
어렵다는 점이다.
종합은 한 줄 인용으로 뒷받침되지 않기 때문이다.
남는 어려움은 종합과 해석 페이지를 어떻게 다루느냐이며, 글은 이를 다루지 않는다.
이 문서가 권하는 한 가지 방식은 종합 페이지에 `sources`로 여러 원본을 적되 인용
줄은 개별 원본 페이지에만 두는 것이다.

### 읽기 전용 규칙은 파일 도구만 막는다

글은 deny 규칙이 Claude의 파일 도구와 `cat`, `sed` 같은 인식된 명령을 덮고,
파일을 직접 여는 파이썬 스크립트는 덮지 못한다고 한다.
단단한 벽이 필요하면 샌드박스를 켜라는 것이 글의 처방이다.
권한 규칙을 얻으면 편하지만, 규칙이 막는 범위와 사용자가 막는다고 믿는 범위가
어긋날 수 있다는 점이 숨은 비용이다.

## 함정

### 사각지대에서 포기한다

글이 경고하는 첫 함정은 자료가 50~100개 아래인 구간이다.
이 구간에서 위키는 좋은 검색 엔진처럼 동작하고,
설정 비용을 낸 사용자는 검색을 돌려받을 뿐이다.
대부분 이 구간에서 그만둔다고 글은 말한다.
자료가 적을 때는 위키 대신 파일 몇 개와 `CLAUDE.md`로 충분한지 먼저
따져 봐야 한다.

### 나쁜 원본이 퍼진다

노트 앱에서는 틀린 메모가 하나일 뿐이지만,
컴파일된 위키에서는 틀린 원본 하나가 이미 10~15개 페이지에 닿아 있다.
글이 매니페스트, 인용 검사, diff를 모두 두라고 하는 이유다.
원본이 바뀌면 `lint`가 낡은 페이지 목록을 내므로,
원본 수정 뒤에는 해당 페이지를 다시 수집해야 한다.

### 낯선 사람의 글을 읽는 에이전트가 파일을 고친다

웹 클리핑은 낯선 사람이 쓴 텍스트이고, 에이전트가 이를 읽으면서 파일을
편집할 수 있다.
글이 드는 방어는 `raw/`의 deny 규칙, 인용 검사, git diff 세 가지다.
이 문서의 해석으로는 클리핑에 적힌 지시문이 위키 페이지에 그대로 옮겨져 다음
세션의 지침처럼 읽힐 위험도 있으므로, 수집한 문장을 인용 줄 밖에 옮기는 일을
검토 대상으로 삼아야 한다.

### 생명주기 신호가 없다

글은 한 달 전 페이지가 아직 최신인지 알려 주는 신호가 패턴에 없다고 지적하며,
린트를 일부러 돌려야 한다고 한다.
`updated` 값만으로는 낡았는지 알 수 없으므로, 원본 해시 비교가 유일한 신호다.

## 확인하기

글의 시험을 그대로 재현할 수 있다.
빈 볼트에 원본 한 개와 페이지 한 개를 만들고,
페이지에 원본에 없는 문장을 인용 줄로 넣은 뒤 린트를 돌리면 그 문장이 `QUOTE NOT
IN SOURCE`로 보고되어야 한다.
이 문서가 위 스크립트로 같은 구성을 시험한 결과는 다음과 같았다.
없는 출처, 끊어진 링크, 남은 TODO, 프론트매터 누락, 원본에 없는 인용,
고아 페이지, 수집 뒤 바뀐 원본이 모두 보고되었고, 종료 코드는 2였다.

```bash
python3 brain.py status        # NEW, CHANGED, DELETED 원본만 나열
python3 brain.py done raw/memex.md wiki/memex.md
python3 brain.py lint; echo "exit=$?"   # 문제가 있으면 2
```

이어서 원본을 한 글자 고치고 린트를 돌려 낡은 페이지 목록이 나오는지,
페이지에서 인용을 지우면 오류가 사라지는지 확인한다.
그다음 훅으로 걸었을 때 린트의 오류가 Claude에게 전달되어 같은 턴에 고쳐지는지
실제 세션에서 본다.

## 비평

### 효과의 증거는 모두 장난감 볼트에서 나온다

글의 시험은 작은 샘플 볼트이고 파일이 천 개는 아니라고 저자 스스로 밝힌다.
거짓 문장, 끊어진 링크, 빠진 출처, TODO,
수집 뒤 바뀐 원본은 모두 저자가 일부러 심은 오류다.
스크립트가 심은 오류를 잡는 것은 구현이 의도대로 동작한다는 증거일 뿐이고,
실제 운영에서 어떤 오류가 얼마나 나오는지에 대해서는 말해 주지 않는다.
두 번째 뇌가 세션 시작 비용을 줄였는지,
같은 설명을 몇 번 덜 했는지에 대한 측정도 글에는 없다.
3개월째 모습과 6개월째의 “구조적 격차” 서술은 저자의 예상이다.

### 근거로 든 조회수와 별 수가 효과의 증거로 쓰인다

글은 Karpathy의 글이 며칠 만에 1천 6백만 회 조회로 보도되었고 R&D World는
6월까지 2천 1백만 회를 넘었다고 적는다.
이 수치들은 패턴이 유명하다는 사실을 보여 줄 뿐 잘 작동한다는 증거가 아니다.
글 자신도 인기 있는 가이드들이 낡은 별 수와 존재하지 않는 설치 스크립트를
인용한다고 지적하는데, 같은 문제가 인기 지표에 기대는 글의 논거에도 해당한다.
이 문서는 그 수치도 확인하지 않았다.

### 경쟁자 비판을 제품 판매 때문이라며 깎아내린다

글은 색인이 한 컨텍스트 창에 들어가는 동안만 동작한다는 비판을 소개하며,
그 비평가가 경쟁 제품을 판다는 이유로 가려 들으라고 한다.
이해관계를 밝히는 것은 정당하지만, 그것이 비판의 내용에 대한 반박은 아니다.
글은 이 비판을 검증하는 실험도 하지 않았다.
규모의 한계는 이 문서의 해석으로도 실제 위험이므로,
색인이 컨텍스트에 들어가는지 토큰 수로 직접 재 보는 것이 맞다.

### 글의 마무리는 저장과 팔로우 요청이다

글은 결론에서 오늘 밤 폴더를 만들고 인터뷰 프롬프트를 돌리라고 권하고,
저자의 프로필은 내일의 AI를 오늘 써 본다고 적는다.
글을 근거로 팀의 지식 체계를 바꾸려는 사람은 위 확인 절차로 자기 자료에서 린트가
의미 있는 오류를 잡는지부터 보아야 한다.

## 체크리스트

- `raw/`에 모델의 쓰기 권한이 없고, 설정 후 실제로 막히는지 확인했는가.
- 모든 위키 페이지에 `title`, `sources`, `updated`가 있는가.
- 구체적 주장마다 `> "원문 그대로" - raw/파일` 형식의 인용 줄이 있는가.
- 린트가 LLM 없이 돌고, 문제가 있을 때 종료 코드가 0이 아닌가.
- 일부러 심은 거짓 인용을 린트가 잡는 것을 한 번 확인했는가.
- 원본을 고친 뒤 낡은 페이지 목록이 나오는가.
- 수집이 끝날 때마다 커밋해서 diff로 모델의 변경을 볼 수 있는가.
- 여러 프로젝트가 한 볼트를 쓴다면 범용 코딩 질문에는 위키를 읽지 않도록 적었는가.
- `hot.md`가 한 화면 안으로 짧게 유지되는가.
- 자료가 50개를 넘기 전에 린트를 먼저 붙였는가.
- 웹 클리핑에 든 지시문이 위키 본문에 옮겨지지 않았는지 diff에서 보는가.

## 기억할 원칙

### 쓰는 쪽과 검사하는 쪽을 분리한다

모델이 쓴 결과를 같은 모델이 검사하게 하면 서로 동의하기 쉽다.
검사를 결정론적 코드로 옮기면 비용이 거의 없고 결과가 재현되며,
잡을 수 있는 것과 없는 것의 경계가 분명해진다.
위키뿐 아니라 모델이 만든 모든 산출물에 적용할 수 있고,
검사 기준은 모델이 건드리지 못하는 사실의 층에 두어야 한다.

### 이 문서가 확인하지 못한 것을 구분해서 쓴다

이 문서는 글의 수치(별, 조회수, 줄 수)와 Claude Code 동작에 대한 주장을 외부
페이지에서 확인하지 않았다.
스크립트는 이 문서가 직접 짜서 샘플 볼트에서 시험한 것이고,
글의 부록 코드와 같지 않다.
그래서 글이 주장한 설정의 동작은 사용하는 환경에서 한 번 시험한 뒤에
믿어야 한다.
