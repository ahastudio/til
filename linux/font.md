# Amazon Linux에 한글 폰트 설치

```bash
sudo yum update -y \
  && sudo yum install -y google-noto-sans-cjk-fonts \
  && fc-list | grep NotoSansCJK
```

VNC 서버를 띄운다면 재부팅 후

```bash
vncserver :1
```
