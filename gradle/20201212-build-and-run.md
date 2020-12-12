# Gradle로 프로젝트 빌드하고 실행하기

Gradle을 이용해 프로젝트를 빌드하고 실행하는 방법을 정리했습니다.

## 프로젝트 만들고 확인하기

간단한 프로젝트를 만들어서 이걸 활용해 보겠습니다.

```bash
gradle init \
    --type java-application \
    --dsl groovy \
    --test-framework junit-jupiter \
    --project-name demo \
    --package com.example
```

Gradle로 빠르게 확인해 보겠습니다.

```bash
./gradlew run
```

잘 되는 걸 확인했으니 빌드 결과를 삭제하겠습니다.

```bash
./gradlew clean
```

준비가 잘 됐는지 확인하기 위해
Java 11부터 지원하는 방식으로 기본 코드를 실행해 보겠습니다.

```bash
cat app/src/main/java/com/example/App.java

java app/src/main/java/com/example/App.java
```

## `javac`로 컴파일하고 `java`로 실행하기

평범하게 컴파일하고 실행해 봅시다.

```bash
javac -d app/build/classes/java/main/ \
    app/src/main/java/com/example/App.java

ls -al app/build/classes/java/main/com/example/

java -classpath app/build/classes/java/main/ com.example.App
```

## `Gradle`로 빌드하고 `java`로 실행하기

Gradle을 이용해 Java 코드를 컴파일하고 실행해 봅시다.

```bash
./gradlew clean compileJava

ls -al app/build/classes/java/main/com/example/

java -classpath app/build/classes/java/main/ com.example.App
```

## 의존성 추가하기

간단히 Spring 의존성을 추가해 보겠습니다.

`app/build.gradle` 파일에 다음과 같이 의존성을 추가합니다.

```gradle
dependencies {
    // 기존 의존성을 일단 그대로 두고 아래를 추가합니다.

    // Use Spring framework
    implementation 'org.springframework:spring:5.3.2'
    implementation 'org.springframework:spring-context:5.3.2'
}
```

`app/src/main/java/com/example/App.java` 파일도 다음과 같이 변경합니다.

```java
package com.example;

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class App {
    public String getGreeting() {
        return "Hello World!";
    }

    public static void main(String[] args) {
        ApplicationContext context =
                new AnnotationConfigApplicationContext(App.class);

        App app = context.getBean("myApp", App.class);

        System.out.println(app.getGreeting());
    }

    @Bean
    public App myApp() {
        return new App();
    }
}
```

이번에도 Gradle로 빠르게 확인해 보겠습니다.

```bash
./gradlew run
```

## 의존성 JAR 파일 모아서 `javac`로 빌드하고 `java`로 실행하기

평범하게 컴파일해 봅시다.

```bash
javac -d app/build/classes/java/main/ \
    app/src/main/java/com/example/App.java
```

의존성 문제로 컴파일 에러가 발생합니다.

```txt
    app/src/main/java/com/example/App.java

app/src/main/java/com/example/App.java:3: error: package org.springframework.context does not exist
import org.springframework.context.ApplicationContext;
                                  ^
```

의존성을 `build/dependencies`로 모으기 위해
`app/build.gradle` 파일을 변경합니다.

```gradle
task copyDependencies(type: Copy) {
    from configurations.default
    into 'build/dependencies'
}
```

JAR 파일을 모아봅시다.

```bash
./gradlew clean copyDependencies

ls -al app/build/dependencies/
```

잘 모은 JAR 파일을 이용해 빌드하고 실행합니다.

```bash
javac -d app/build/classes/java/main/ \
    -classpath "app/build/dependencies/*" \
    app/src/main/java/com/example/App.java

ls -al app/build/classes/java/main/com/example/

java -classpath "app/build/classes/java/main/:app/build/dependencies/*" \
    com.example.App
```

## Gradle로 컴파일하고 `java`로 실행하기

JAR 파일 모은 걸 모두 지우고 다시 시작해 보겠습니다.

```bash
./gradlew clean

ls -al app/build
# => “ls: app/build: No such file or directory”
```

이제 `javac` 대신 Gradle로 컴파일해 봅시다.

```bash
./gradlew compileJava

ls -al app/build/classes/java/main/com/example/
```

평범하게 실행하면 실패합니다.

```bash
java -classpath app/build/classes/java/main/ com.example.App
# => “java.lang.NoClassDefFoundError: org/springframework/context/ApplicationContext”
```

일단 JAR를 모아서 실행해 봅시다.

```bash
./gradlew copyDependencies

java -classpath "app/build/classes/java/main/:app/build/dependencies/*" \
    com.example.App
```

## JAR 파일 만들기

Gradle을 이용해 애플리케이션을 class 파일이 아니라 JAR 파일을 만들 수 있습니다.

```bash
./gradlew clean jar

ls -al app/build/libs/
```

JAR 파일을 `classpath`로 잡아서 실행해 봅시다.

```bash
java -classpath "app/build/libs/app.jar" com.example.App
```

의존성 문제가 있으니 JAR 파일을 더 모아서 실행합시다.

```bash
./gradlew copyDependencies

cp app/build/dependencies/*.jar app/build/libs/

java -classpath "app/build/libs/*" com.example.App
```

## `tar` 압축 파일 만들기

Gradle엔 JAR 파일을 모아서 `tar` 파일을 만드는 기능이 있습니다.

```bash
./gradlew clean distTar

ls -al app/build/distributions/
```

압축을 풀어서 확인해 봅시다.
우리가 귀찮게 모았던 게 한꺼번에 해결된 상태죠?

```bash
tar -xf app/build/distributions/app.tar -C app/build/distributions/

ls -al app/build/distributions/

ls -al app/build/distributions/app/lib/
```

실행해 봅시다.

```bash
java -classpath "app/build/distributions/app/lib/*" com.example.App
```

## JAR 파일 살펴보기

자, 다시 JAR 파일로 돌아오죠.
깔끔하게 다시 기본 상태로 만듭시다.

```bash
./gradlew clean jar
```

`java`의 `-jar` 옵션으로 JAR 파일을 실행하면 Manifest 속성 문제가 발생합니다.

```bash
java -jar app/build/libs/app.jar
```

압축을 풀어서 확인해 봅시다.

```bash
mkdir -p app/build/libs/app

tar -xf app/build/libs/app.jar -C app/build/libs/app/

ls -al app/build/libs/app/

ls -al app/build/libs/app/com/example/

ls -al app/build/libs/app/META-INF/
```

Manifest 속성을 확인해 보면 Manifest 버전만 있다는 걸 알 수 있습니다.

```bash
cat app/build/libs/app/META-INF/MANIFEST.MF
```

`app/build.gradle`에 `jar` 작업에 대한 옵션을 추가합니다.

```gradle
jar {
    manifest {
        attributes 'Main-Class': 'com.example.App'
    }
}
```

다시 빌드하고 압축을 풀어서 확인해 봅시다.

```bash
./gradlew clean jar

mkdir -p app/build/libs/app

tar -xf app/build/libs/app.jar -C app/build/libs/app/

cat app/build/libs/app/META-INF/MANIFEST.MF
```

다시 실행해 보면 또 다시 의존성 문제가 발생합니다.

```bash
java -jar app/build/libs/app.jar
```

자, 이제 거의 다 왔어요. 힘냅시다!

## Fat JAR 파일 만들기

하나의 JAR 파일에 모든 걸 다 담은 걸 Fat JAR라고 합니다.

일단 기존에 만든 JAR 파일의 크기를 확인해 보죠.

```bash
ls -al app/build/libs/app.jar
# => 1252 bytes
```

`app/build.gradle`에 의존성 추가 설정을 추가합니다.

```gradle
jar {
    manifest {
        attributes 'Main-Class': 'com.example.App'
    }

    from {
        configurations.default.collect { it.isDirectory() ? it : zipTree(it) }
    }
}
```

Fat JAR 파일을 만듭니다.

```bash
./gradlew clean jar
```

Fat JAR 파일의 크기를 확인해 보면 확실히 커진 걸 알 수 있습니다.

```bash
ls -al app/build/libs/app.jar
# => 7079384 bytes
```

압축을 풀어서 확인해 봅시다.

```bash
mkdir -p app/build/libs/app

tar -xf app/build/libs/app.jar -C app/build/libs/app/

ls -al app/build/libs/app/

ls -al app/build/libs/app/org/springframework/
```

Fat JAR 파일을 실행하면 잘 되는 걸 확인할 수 있습니다.

```bash
java -jar app/build/libs/app.jar
```

## Fat JAR 만드는 작업 분리

평범한 JAR 파일과 Fat JAR 파일을 만드는 작업을 분리해 봅시다.
Fat JAR 파일을 만드는 작업을 `fatJar`라고 합시다.
`app/build.gradle` 파일의 관련 코드를 다음과 같이 변경합니다.

```gradle
# jar는 삭제하고 tasks.withType(Jar)로 공통 요소를 추출합니다.
tasks.withType(Jar) {
    manifest {
        attributes 'Main-Class': 'com.example.App'
    }
}

task fatJar(type: Jar) {
    archiveBaseName = 'fat-app'

    from sourceSets.main.output

    from {
        configurations.default.collect { it.isDirectory() ? it : zipTree(it) }
    }
}
```

`fatJar` 작업은 이렇게 써도 됩니다.

```gradle
task fatJar(type: Jar) {
    archiveBaseName = 'fat-app'

    with jar

    from {
        configurations.default.collect { it.isDirectory() ? it : zipTree(it) }
    }
}
```

빌드해서 둘을 비교해 봅시다.

```bash
./gradlew clean jar fatJar

ls -al app/build/libs/
```

Fat JAR를 실행합니다.

```bash
java -jar app/build/libs/fat-app.jar
```

## 소스 코드

[https://github.com/ahastudio/CodingLife/tree/main/20201212/java](https://j.mp/3ndnQaT)
