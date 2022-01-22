# Heroku - Cloud Application Platform

<https://www.heroku.com/>

<https://www.heroku.com/home>

## [Create React App](https://github.com/ahastudio/til/blob/main/react/create-react-app.md)

[Deploying React with Zero Configuration | Heroku](https://blog.heroku.com/deploying-react-with-zero-configuration)

[Adding Custom Environment Variables | Create React App](https://create-react-app.dev/docs/adding-custom-environment-variables/)

`REACT_APP_ㅇㅇ` 환경 변수를 이용해
개발 환경과 실제 배포 환경을 분리하고,
다음과 같이 환경 변수를 세팅한다.

```bash
# Heroku 환경 변수 설정
heroku config:set REACT_API_ㅇㅇ=어쩌고

# Heroku 환경 변수 확인
heroku config
```
