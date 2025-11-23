# `@Embeddable`

<https://en.wikibooks.org/wiki/Java_Persistence/Embeddables>

<https://www.baeldung.com/jpa-embedded-embeddable>

## ID

```java
class User {
    @EmbeddedId
    private UserId id;
}

@Embeddable
@Access(AccessType.FIELD)
record UserId(
    Long value
) {
}
```

## Nested Embedding

<https://wiki.eclipse.org/EclipseLink/Development/JPA_2.0/nested_embedding>

```java
class User {
    @Embedded
    private Pet role;
}

@Embeddable
@Access(AccessType.FIELD)
record Pet(
    @Embedded
    private Level level
) {
}

@Embeddable
@Access(AccessType.FIELD)
record Level(
    Integer value
) {
}
```
