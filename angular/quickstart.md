# Angular 2 시작하기

## Node Version Manager

https://github.com/creationix/nvm

```
$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
```

## Node.js

https://nodejs.org/

```
$ nvm install v5.10.1
$ nvm alias default v5.10.1
```

## TypeScript

https://www.npmjs.com/package/typescript

```
$ npm install -g typescript
```

`tsconfig.json` 만들기:
```
$ tsc --init --module system --moduleResolution node
```

## NPM

`package.json` 만들기:
```
$ npm init --yes
$ npm install systemjs --save
$ npm install angular2@2.0.0-beta.14 --save
$ npm install rxjs@5.0.0-beta.2 --save
```

## SystemJS

https://github.com/systemjs/systemjs

`config.js` 만들기:
```javascript
System.config({
  packages: {
    app: {
      format: 'register',
      defaultExtension: 'js'
    }
  }
});
```

## Angular 2

`app/main.ts` 만들기:
```typescript
import {bootstrap} from 'angular2/platform/browser';
import {Component} from 'angular2/core';

@Component({
  selector: 'my-app',
  template: `
    <h1>Hello, {{name}}!</h1>
    <input [(ngModel)]="name">
    <ol *ngIf="items.length">
      <li *ngFor="#item of items">{{item}}</li>
    </ol>
    `
})
class App {
  name: string = 'world';

  get items(): string[] {
    return this.name.split('');
  }
}

bootstrap(App);
```

`index.html` 만들기:
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Angular2</title>
</head>
<body>
  <my-app></my-app>
  <script src="node_modules/angular2/bundles/angular2-polyfills.js"></script>
  <script src="node_modules/systemjs/dist/system.src.js"></script>
  <script src="node_modules/rxjs/bundles/Rx.js"></script>
  <script src="node_modules/angular2/bundles/angular2.dev.js"></script>
  <script src="config.js"></script>
  <script>
    System.import('app/main');
  </script>
</body>
</html>
```

```
$ tsc
$ php -S localhost:8000
```
