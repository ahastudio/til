# Pyccuracy - BDD-style Web Acceptance Testing framework

아샬이 예전에 썼던 BDD E2E 테스트 도구. 현재는 개발 중단됨.

<https://github.com/heynemann/pyccuracy>

## Example

### Log In

```txt
As a registered user
I want to log in
So that I can use this service fully

Scenario 1 - Log in
Given
    Load fixture "users.yaml"
    I go to "/logout"
    I go to "/login"
When
    I fill "username" textbox with "tester"
    I fill "password" textbox with "test"
    I click "submit" button and wait
Then
    I see that current page contains "Log out"

Scenario 2 - Wrong password
Given
    Load fixture "users.yaml"
    I go to "/logout"
    I go to "/login"
When
    I fill "username" textbox with "tester"
    I fill "password" textbox with "x"
    I click "submit" button and wait
Then
    I see that current page contains "Log in"
```

### Log out

```txt
As a registered user
I want to log out
So that I can use this service as a guest

Scenario 1 - Log out
Given
    Load fixture "users.yaml"
    I am logged in with username "tester" and password "test"
    I go to "/"
When
    I mouseover "setting" element
    I click "Log out" link and wait
Then
    I see "Log in" link
```

### Search

```txt
As a guest
I want to search with query text
So that I can find contents that have my insteresting issue

Scenario 1 - Search all contents
Given
    Load fixture "contents.yaml"
    I go to "/"
When
    I fill "q" textbox with "rap"
    I click "submit" button and wait
Then
    I see "Search" title
    I see that current page contains "All Contents (1)"
    I see that current page contains "How to <span>Rap</span>?"
```
