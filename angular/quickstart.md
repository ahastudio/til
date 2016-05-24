# Angular 2 시작하기

## Node Version Manager

https://github.com/creationix/nvm

```
$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.1/install.sh | bash
```

## Node.js

https://nodejs.org/

```
$ nvm install 6.2.0
$ nvm use 6.2.0
$ nvm alias default v6.2.0
```

## Angular CLI

```
$ https://cli.angular.io/
```

## 프로젝트 생성

```
$ ng new PROJECT_NAME
$ cd PROJECT_NAME
```

프로젝트 이름으로 `AppComponent` 파일과 클래스 등을 만들기 때문에, 저는 `application` 같은 이름으로 만들고 나중에 프로젝트 폴더 이름과 `package.json` 둘만 고칩니다.

## 서버 실행

```
$ ng serve
```

http://localhost:4200/

## 테스트 실행

```
$ ng test
```

## 배포용 빌드

```
$ ng build -prod
```

```
$ cd dist
$ php -S localhost:8000
```

http://localhost:8000/

