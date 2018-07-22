# MobX

```
$ yarn add mobx
$ yarn add mobx-react
$ yarn add --dev babel-plugin-transform-decorators-legacy
```

`.babelrc`의 `"plugins"`에 `"transform-decorators-legacy"` 추가.

```json
{
  "presets": ["babel-preset-expo"],
  "env": {
    "development": {
      "plugins": [
        "transform-react-jsx-source",
        "transform-decorators-legacy"
      ]
    }
  }
}
```

VS Code를 위해 `tsconfig.js` 작성.

```json
{
    "compilerOptions": {
        "experimentalDecorators": true,
        "allowJs": true
    }
}
```
