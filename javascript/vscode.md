# Visual Studio Code

## 파일 저장할 때마다 ESLint로 검사하고 수정하기

`.vscode/settings.json`

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": ["javascript"]
}
```

참고: [Linting on Save with Visual Studio Code and ESLint](https://www.digitalocean.com/community/tutorials/workflow-auto-eslinting)
