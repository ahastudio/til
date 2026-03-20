---
name: quotes-curly
description:
  마크다운 파일의 ASCII 큰따옴표(")를 유니코드 큰따옴표("\u201c", "\u201d")로
  변환합니다. 큰따옴표 변환, 유니코드 따옴표, 전각 따옴표 요청 시 사용하세요.
argument-hint: <file-path>
disable-model-invocation: true
allowed-tools: Bash
---

마크다운 파일의 ASCII 큰따옴표(`"`, U+0022)를 유니코드 큰따옴표(`\u201c` /
`\u201d`)로 변환합니다.

## 사용법

```
/quotes-curly path/to/file.md
```

## 실행 방법

1. 인수로 받은 파일 경로에 대해 아래 파이썬 스크립트를 실행합니다:

```bash
python3 ${CLAUDE_SKILL_DIR}/convert_quotes.py $ARGUMENTS
```

2. 실행 결과를 사용자에게 보여줍니다.
3. 변환 전후를 `git diff`로 확인하여 결과가 올바른지 검증합니다.
