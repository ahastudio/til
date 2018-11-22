# Java 8 사용하기

Docker Official Image packaging for Java (openJDK)

- <https://github.com/docker-library/openjdk>
- <https://hub.docker.com/_/java/>

## `Dockerfile` 예제

```dockerfile
FROM java:8-jdk

ADD . /webapp

WORKDIR /webapp

./gradlew assemble

CMD java -jar build/libs/application-0.0.0.war

EXPOSE 8080
```

## 이미지 빌드

```bash
docker build -t webapp .
```

## 컨테이너 실행

```bash
docker run -it -p 80:8080 webapp
```
