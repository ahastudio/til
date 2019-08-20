# ModelMapper - Simple, Intelligent, Object Mapping

<http://modelmapper.org/>

<https://github.com/modelmapper/modelmapper>

## Getting Started

<http://modelmapper.org/getting-started/>

### Gradle

```gradle
implementation 'org.modelmapper:modelmapper:2.3.0'
```

### Models

```java
class User {
    @Setter
    @Getter
    private String username;
}
```

```java
@Setter
@Getter
class UserDTO {
    private String username;
}
```

### Mapping

```java
ModelMapper modelMapper = new ModelMapper();
```

```java
UserDTO userDTO = modelMapper.map(user, UserDTO.class);
```

```java
User user = modelMapper.map(userDTO, User.class);
```
