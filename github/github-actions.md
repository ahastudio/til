# GitHub Actions

간략한 소개: <https://github.com/features/actions>

공식 문서: <https://help.github.com/actions>

저장소: <https://github.com/actions>

Quickstart for GitHub Actions:
<https://docs.github.com/en/actions/quickstart>

Github Actions 오픈소스 목록:
<https://github-actions.netlify.app/>

Awesome Actions:
<https://github.com/sdras/awesome-actions>

## Articles

- [GitHub Actions now supports CI/CD, free for public repositories](https://github.blog/2019-08-08-github-actions-now-supports-ci-cd/)
- [GitHub Actions: First impressions — Martian Chronicles, Evil Martians’ team blog](https://evilmartians.com/chronicles/github-actions-first-impressions)
- [Guide to a custom CI/CD with GitHub Actions - ITNEXT](https://itnext.io/https-medium-com-marekermk-guide-to-a-custom-ci-cd-with-github-actions-5aa0ff07a656)
- [Trying GitHub Actions | Better world by better software](https://glebbahmutov.com/blog/trying-github-actions/)
- [How to use GitHub Actions in GitKraken](https://support.gitkraken.com/git-workflows-and-extensions/github-actions/)
- [An Unintentionally Comprehensive Introduction to GitHub Actions CI - DEV Community 👩‍💻👨‍💻](https://dev.to/bnb/an-unintentionally-comprehensive-introduction-to-github-actions-ci-blm)
- [GitHub Actions 워크플로우의 승인 기능 사용하기](https://blog.outsider.ne.kr/1556)

## Simple Example

<https://github.com/ahastudio/github-actions-example>

## CI/CD

### Docker

- [Introducing GitHub Container Registry](https://github.blog/2020-09-01-introducing-github-container-registry/)
- [Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Publishing and installing a package with GitHub Actions - GitHub Docs](https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions)
- [Publishing Docker images](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)

GitHub Marketplace:

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)

```yaml
name: CI

on: [push, pull_request]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Log in to the Container registry
        uses: docker/login-action@v1
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push Docker image
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-to: type=inline
```

### GitHub Pages

GitHub Marketplace:

- [GitHub Pages action](https://github.com/marketplace/actions/github-pages-action)
- [Deploy to GitHub Pages](https://github.com/marketplace/actions/deploy-to-github-pages) (아래 예제에서 사용)
- [GH Pages deploy](https://github.com/marketplace/actions/gh-pages-deploy)

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-18.04
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'
      - name: Install dependencies
        run: npm ci
      - name: Lint
        run: npx eslint .
      - name: Run tests
        run: npx jest
      - name: Build
        run: npm run build
      - name: Archive production artifacts
        uses: actions/upload-artifact@v2
        with:
          name: dist
          path: dist/
  deploy:
    needs: build
    runs-on: ubuntu-18.04
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Download production artifacts
        uses: actions/download-artifact@v2
        with:
          name: dist
          path: dist/
      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@4.1.5
        with:
          branch: gh-pages
          folder: dist
          clean: false
```

### 코드숨 CI/CD 예제 (by [한윤석](https://github.com/hannut91))

[코드숨 CI/CD 세미나](https://j.mp/3j3qe4d)

- [https://github.com/CodeSoom/cicd-example](https://j.mp/3zYw90K)
- [https://github.com/CodeSoom/cicd-example2](https://j.mp/3GHa1Mh)

사용된 Actions:

- [Checkout](https://github.com/actions/checkout)
- [setup-node](https://github.com/actions/setup-node)
- [SSH Remote Commands](https://github.com/marketplace/actions/ssh-remote-commands)
