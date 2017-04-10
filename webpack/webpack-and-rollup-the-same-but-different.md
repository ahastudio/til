원문: [https://medium.com/webpack/webpack-and-rollup-the-same-but-different-a41ad427058c](http://j.mp/2o8Z9jT)

날림 번역입니다. 피드백은 Issue Tracker에 부탁드립니다: https://github.com/ahastudio/til/issues

# Webpack and Rollup: the same but different

이번 주에 Facebook은 기존의 빌드 프로세스를 Rollup 기반으로 바꾼 [엄청난 PR(monster pull request)](https://github.com/facebook/react/pull/9327)을 머지했습니다. 이 일은 [몇몇](https://twitter.com/stanlemon/status/849366789825994752) [사람들](https://twitter.com/MrMohtas/status/849362334988595201)[에게](https://twitter.com/kyleholzinger/status/849683292760797184) “왜 webpack 대신 Rollup을 쓴다는 거지?”란 질문을 던졌습니다.

이건 완전 합리적인 질문입니다. [Webpack](https://webpack.js.org/)은 매달 백 만 다운로드와 만 개의 웹사이트와 앱에서 사용하는 Modern JavaScript 커뮤니티의 최고 성공 사례 중 하나니까요. 커다란 생태계, 많은 기여자, (커뮤니티 오픈 소스 프로젝트 중 흔치 않은) [의미 있는 재정 지원](https://opencollective.com/webpack)까지 갖추고 있습니다.

상대적으로, Rollup은 피라미입니다. 하지만 React뿐 아니라 Vue, Ember, Project, D3, Three.js, Moment 및 수많은 유명 라이브러리도 Rollup을 사용합니다. 어떻게 된 겁니까? 모두가 동의하는 하나의 JavaScript 모듈 번들러로 충분하지 않은 걸까요?

## A tale of two bundlers

webpack은 기존의 도구들이 고려하지 않은 “복잡한 단일 페이지 애플리케이션(SPA)을 빌드한다”는 어려운 문제를 해결하기 위해 2012년에 [Tobias Koppers](https://medium.com/@sokra)가 만들었습니다. 특히 두 기능이 모든 것을 바꿨습니다:

 1. 애플리케이션을 필요할 때 로딩할 수 있는 관리 가능한 작은 조각으로 쪼갤 수 있도록 **코드 분할**을 할 수 있습니다. 이건 사용자가 애플리케이션 전체를 다운로드 받고 파싱하는 걸 기다리는 것보다 훨씬 빠르게 인터랙티브 사이트를 쓸 수 있다는 걸 의미합니다. 직접 수작업으로 할 수도 있긴 하지만... 어... 행운을 빕니다.

 2. 이미지, CSS 같은 **정적 애셋(asset)** 을 마치 다른 모듈처럼(as just another node in the dependency graph) 임포트해서 쓸 수 있습니다. 파일을 올바른 폴더에 넣고, 파일을 합쳐주고, 파일 URL에 해시를 추가하는 번거로운 작업을 하지 않아도 됩니다. webpack이 대신 해주니까요.

Rollup은 ES2015 모듈의 독창적인 디자인을 통해 가능한 효율적으로 “플랫(flat)한 배포”(역주: 적절한 번역어를 찾지 못 했습니다. [의견 주세요](https://github.com/ahastudio/til/issues).)를 빌드하기 위해 만들어졌습니다. webpack을 비롯한 다른 모듈 번들러는 각 모듈을 하나의 함수에 넣고, 브라우저 친화적인 require 구현으로 하나의 번들에 넣은 뒤, 하나씩 평가(evaluate)합니다(역주: Lazy Evaluation을 설명하고 있습니다). 필요할 때마다 로딩할 땐 훌륭한 방법이지만, 그렇지 않은 경우엔 낭비고, [많은 모듈을 쓸 땐 정말 나쁩니다](https://nolanlawson.com/2016/08/15/the-cost-of-small-modules/).

Rollup은 ES2015 모듈이 제공하는 다른 접근법을 사용합니다. 한 곳에 있고, 한번에 평가(evaluate)되며, 차례로 결과를 얻는, 빠르게 시작되는 단순한 코드로 빌드합니다. [Rollup REPL로 직접 확인할 수 있습니다](https://rollupjs.org/repl).

하지만 트레이드오프가 있습니다. 코드 분할은 훨씬 흥미로운 문제고, 이 글을 쓰는 시점에는 Rollup은 코드 분할을 지원하지 않습니다. 마찬가지로, 실행 중 모듈 교체(HMR)도 지원하지 않습니다. Rollup을 도입할 때 가장 큰 문제는, 플러그인을 통해 CommonJS 파일을 사용할 때, webpack은 문제없이 잘 처리하는데 비해 Rollup은 ES2015로 변환하지 못하는 경우가 있다는 겁니다.

## So which should I use?

이제 왜 번들링 도구가 공존하고 서로를 지원하는지 명확해졌을 거라 믿습니다. 다른 목적을 갖고 있는 거죠. 요약하면 다음과 같습니다:

> 애플리케이션에는 webpack을 쓰고, 라이브러리에는 Rollup을 써라

이건 절대적인 규칙은 아닙니다. 많은 웹사이트와 앱이 Rollup으로 빌드되고, 많은 라이브러리가 webpack으로 빌드됩니다. 하지만 간단히 사용하긴 좋습니다([rule of thumb](https://en.wikipedia.org/wiki/Rule_of_thumb)).

코드 분할이 필요하거나 정적 애셋이 많거나 CommonJS 의존이 많다면 Webpack을 쓰는 게 좋습니다. 코드베이스가 ES2015 모듈이고 다른 사람이 쓰는 걸 만들고 있다면 Rollup이 좋을 겁니다.

# Package authors: use pkg.module!

여러분과 라이브러리 개발자가 하나의 모듈 시스템에 효과적으로 동의해야 하기 때문에, JavaScript 라이브러리를 쓰는 건 오랫동안 문제였습니다. Browserify를 쓰는데 AMD를 선호하는 사람이 있다면 빌드하기 전에 삽질(duct tape thing)을 해야 했습니다. 이 문제를 해결하려고 [UMD](https://github.com/umdjs/umd)가 있지만, 쓰는 곳이 없어서 전혀 알 수 없었습니다.

ES2015는 `import`와 `export`를 언어로 수용해 모든 걸 바꿨습니다. 앞으로는 모호함 없이 전부 매끄럽게 작동할 겁니다. 불행히도 대다수의 브라우저와 Node는 아직 `import`와 `export`를 지원하지 않기 때문에 UMD 파일(Node 전용이라면 CommonJS)로 만들어야 합니다.

라이브러리의 `package.js` 파일에 `"module": "dist/my-library.es.js"`를 추가하면(`pkg.module`이라고 알려진 방법입니다), 지금 당장 UMD와 ES2015를 동시에 지원할 수 있습니다. **Webpack과 Rollup 모두 `pkg.module`를 이용해 가능한 가장 효율적인 코드를 만들기 때문에 중요합니다**. 라이브러리에서 쓰지 않는 부분을 [털어버릴 수도 있습니다](https://webpack.js.org/guides/tree-shaking/).

[Rollup 위키](https://github.com/rollup/rollup/wiki/pkg.module)에서 `pkg.module`에 대해 더 배울 수 있습니다.

이 글이 두 프로젝트의 관계를 명확하게 해줬길 바랍니다. 더 궁금한 점이 있으면 트위터에서 [rich_harris](https://twitter.com/rich_harris), [rollupjs](https://twitter.com/rollupjs), [thelarkinn](https://twitter.com/thelarkinn)(역주: webpack 코어 개발자)을 찾아주세요. 해피 번들링!

---

이 글을 써준 Rich Harris에게 감사드립니다. We believe that collaboration in open source is incredibly vital to ensure we push technology and the web forward together.

No time to help contribute? Want to give back in other ways? Become a Backer or Sponsor to webpack by [donating to our open collective](https://opencollective.com/webpack). Open Collective not only helps support the Core Team, but also supports contributors who have spent significant time improving our organization on their free time! ❤
