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
    private String username;
}
```

```java
class UserDTO {
    private String username;
}
```

### Mapping

```java
ModelMapper modelMapper = new ModelMapper();

modelMapper.getConfiguration()
        .setFieldMatchingEnabled(true)
        .setFieldAccessLevel(Configuration.AccessLevel.PRIVATE);
```

```java
UserDTO userDTO = modelMapper.map(user, UserDTO.class);
```

```java
User user = modelMapper.map(userDTO, User.class);
```

## Converter

```java
modelMapper.addConverter(
        context -> FieldUtils.getField(
                context.getSource(), "value", Integer.class),
        Level.class, Integer.class);
```
