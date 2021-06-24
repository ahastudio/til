# TypeScript + Express

- Express <https://github.com/expressjs/express>
- CORS <https://github.com/expressjs/cors>
- body-parser <https://github.com/expressjs/body-parser>

## 프로젝트 세팅

```bash
npm init

npm i -D typescript ts-node eslint

npx tsc --init

npx eslint --init

npm i express cors body-parser
npm i -D @types/express @types/cors @types/body-parser

npm i -D nodemon
```

## `package.json` 파일의 `scripts` 항목

```json
  "scripts": {
    "start": "nodemon --exec ts-node src/index.ts",
    "lint": "eslint --fix --ext .js,.ts .",
    "check": "tsc --noEmit"
  },
```

## `nodemon.json` 파일

```json
{
  "exec": "ts-node --files",
  "ext": "js,json,ts",
  "watch": ["src/"],
  "ignore": [".git", "node_modules/**/node_modules"],
  "verbose": true
}
```

## `src/index.ts` 파일

```typescript
import app from './app';

const { log: print } = console;

const port = 3000;

app.listen(port, () => {
  print(`app listening at http://localhost:${port}`);
});
```

## `src/app.ts` 파일

```typescript
import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';

const app = express();

app.use(cors());
app.use(bodyParser.json({ limit: '1mb' }));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send('Hello World!');
});

export default app;
```
