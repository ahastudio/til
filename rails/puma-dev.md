# Puma-dev: A fast, zero-config development server for OS X and Linux

더이상 관리되지 않는 Pow server의 대안.

<https://github.com/puma/puma-dev>

맥에서 설치:

```bash
# Puma-dev 설치
brew install puma/puma/puma-dev

# DNS 세팅 (관리자 권한 필요)
sudo puma-dev -setup

# Puma-dev 실행
puma-dev -install

# 도메인 폴더 생성
mkdir -p ~/.puma-dev

# 키체인 등록
open ~/Library/Application\ Support/io.puma.dev/cert.pem
```

맥에서 Puma-dev 서버 멈추기:

```bash
puma-dev -uninstall
```

Rails 프로젝트 등록:

```bash
cd /my/project/path

ln -s $PWD ~/.puma-dev/
```
