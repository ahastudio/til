# Heroku - Cloud Application Platform

<https://www.heroku.com/>

<https://www.heroku.com/home>

## Sleep

[App Sleeping on Heroku | Heroku](https://bit.ly/3tQJkAs)

### Kaffeine

> Kaffeine pings your Heroku app every 30 minutes so it will never go to sleep

[https://kaffeine.herokuapp.com/](https://bit.ly/32nfrwo)

## [Create React App](https://github.com/ahastudio/til/blob/main/react/create-react-app.md)

[Deploying React with Zero Configuration | Heroku](https://bit.ly/3rH4gY7)

[Adding Custom Environment Variables | Create React App](https://bit.ly/3KDtBuS)

`REACT_APP_ㅇㅇ` 환경 변수를 이용해 개발 환경과 실제 배포 환경을 분리한다. 개발
환경을 위해 `.env` 파일에 기본값을 넣어주고, Heroku 배포 환경을 위해 다음과 같이
환경 변수를 세팅한다.

```bash
# Heroku 환경 변수 설정
heroku config:set REACT_API_ㅇㅇ=어쩌고

# Heroku 환경 변수 확인
heroku config
```

참고: “The Twelve-Factor App([https://12factor.net/](https://bit.ly))”의
“[III. 설정](https://bit.ly/3rDZhHz)” 항목.
