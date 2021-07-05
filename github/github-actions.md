# GitHub Actions

간략한 소개: <https://github.com/features/actions>

공식 문서: <https://help.github.com/actions>

저장소: <https://github.com/actions>

Github Actions 오픈소스 목록: <https://github-actions.netlify.app/>

## Articles

- [GitHub Actions now supports CI/CD, free for public repositories](https://github.blog/2019-08-08-github-actions-now-supports-ci-cd/)
- [GitHub Actions: First impressions — Martian Chronicles, Evil Martians’ team blog](https://evilmartians.com/chronicles/github-actions-first-impressions)
- [Guide to a custom CI/CD with GitHub Actions - ITNEXT](https://itnext.io/https-medium-com-marekermk-guide-to-a-custom-ci-cd-with-github-actions-5aa0ff07a656)
- [Trying GitHub Actions | Better world by better software](https://glebbahmutov.com/blog/trying-github-actions/)
- [How to use GitHub Actions in GitKraken](https://support.gitkraken.com/git-workflows-and-extensions/github-actions/)
- [An Unintentionally Comprehensive Introduction to GitHub Actions CI - DEV Community 👩‍💻👨‍💻](https://dev.to/bnb/an-unintentionally-comprehensive-introduction-to-github-actions-ci-blm)

## CI/CD

### Docker

Introducing GitHub Container Registry
<https://github.blog/2020-09-01-introducing-github-container-registry/>

Working with the Container registry
<https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry>

Build and push Docker images
<https://github.com/marketplace/actions/build-and-push-docker-images>

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v1

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v1
        with:
          registry: ghcr.io
          username: ${{ secrets.CONTAINER_REGISTRY_USERNAME }}
          password: ${{ secrets.CONTAINER_REGISTRY_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: ghcr.io/ahastudio/demo:latest
          cache-from: type=registry,ref=ghcr.io/ahastudio/demo:latest
          cache-to: type=inline
```

### Deploy to GitHub Pages

GitHub Pages Deploy Action
<https://github.com/marketplace/actions/deploy-to-github-pages>

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-18.04

    strategy:
      matrix:
        node-version: [12.x]

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npx eslint .

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy
        if: github.ref == 'refs/heads/main'
        uses: JamesIves/github-pages-deploy-action@4.1.4
        with:
          branch: gh-pages
          folder: dist
          clean: false
```

### 예제

<https://github.com/CodeSoom/cicd-example>
