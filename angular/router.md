# Router

- https://angular.io/docs/ts/latest/guide/router.html
- https://angular.io/docs/ts/latest/tutorial/toh-pt5.html

```html
<head>
  <!--
    “We must add a <base href> element tag to the index.html to make pushState routing work.”
    https://angular.io/docs/ts/latest/guide/router.html#!#base-href
  -->
  <base href="/">
</head>
```

```typescript
import {Component} from 'angular2/core';
import {RouteConfig, ROUTER_DIRECTIVES} from 'angular2/router';
import {HomeComponent} from './home.component';
import {BoardComponent} from './board.component';

@Component({
  selector: 'my-app',
  template: `
    <nav>
      <a [routerLink]="['Home']">Home</a>
      <a [routerLink]="['Board', {name: 'free'}]">Free Board</a>
    </nav>
    <router-outlet></router-outlet>
    `,
  directives: [ROUTER_DIRECTIVES]
})
@RouteConfig([
  {
    path: '/',
    name: 'Home',
    component: HomeComponent,
    useAsDefault: true
  },
  {
    path: '/board/:name',
    name: 'Board',
    component: BoardComponent
  }
])
class AppComponent {
}
```

```typescript
import {bootstrap} from 'angular2/platform/browser';
import {ROUTER_PROVIDERS} from 'angular2/router';
import {AppComponent} from './app.component';

bootstrap(AppComponent, [ROUTER_PROVIDERS]);
```
