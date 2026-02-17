# Amazon EC2에 Docker 설치

```bash
sudo yum update -y

sudo amazon-linux-extras install -y docker

sudo service docker start

sudo usermod -a -G docker ec2-user
# → 이후 SSH 재접속
```

참고:
[Docker basics for Amazon ECS - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
