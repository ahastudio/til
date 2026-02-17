# Dozer

Dozer is a Java Bean to Java Bean mapper that recursively copies data from one
object to another.

<https://dozermapper.github.io/>

<https://github.com/DozerMapper/dozer>

## Getting Started

<https://dozermapper.github.io/gitbook/documentation/gettingstarted.html>

### Gradle

```gradle
implementation 'com.github.dozermapper:dozer-core:6.5.0'
```

### Annotation Mappings

<https://dozermapper.github.io/gitbook/documentation/annotations.html>

### Models

```java
class User {
    @Getter
    private String username;
}
```

```java
@Setter
@Getter
class UserDTO {
    @Mapping("username")
    private String username;
}
```

### Mapping

```java
Mapper mapper = DozerBeanMapperBuilder.buildDefault();
```

```java
UserDTO userDTO = mapper.map(user, UserDTO.class);
```

```java
User user = mapper.map(userDTO, User.class);
```
