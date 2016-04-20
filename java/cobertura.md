# Cobertura

Java Test Coverage Tool.

- https://plugins.gradle.org/plugin/net.saliman.cobertura
- https://github.com/stevesaliman/gradle-cobertura-plugin
- https://github.com/stevesaliman/gradle-cobertura-plugin/wiki

```gradle
buildscript {
    repositories {
        maven {
            url 'https://plugins.gradle.org/m2/'
        }
    }
    dependencies {
        classpath 'net.saliman:gradle-cobertura-plugin:2.3.1'
    }
}

apply plugin: 'net.saliman.cobertura'
```

```
$ ./gradlew cobertura
$ open build/reports/cobertura/index.html
```
