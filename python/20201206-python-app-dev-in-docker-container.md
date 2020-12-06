# Docker 컨테이너로 간단히 Python 개발 시작하기

## 문제

Mac OS X에서 [`pytest-watch`](https://github.com/joeyespo/pytest-watch)가 사용하는
[`watchdog`](https://github.com/gorakhargosh/watchdog)이
올바르게 작동하지 않는 상황을 발견했습니다.

```bash
# watchdog의 watchmedo 유틸리티 사용 준비
pip install pyyaml argh watchdog

# 아래의 명령을 실행하면 확장자가 .py인 파일을 고치면 어떤 파일이 바뀌었는지 파일명을 출력해야 합니다.
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='echo "${watch_src_path}"' \
    .
```

Continuous Testing을 위해 이 문제를 반드시 해결해야 합니다.
근본적인 원인을 찾아내서 해결하거나 Docker 등의 Container 기술을 활용해 문제를 회피할 수 있고,
여기서는 Docker Container를 이용해 이 문제를 회피하기로 했습니다.

## Docker로 Python 실행하기

간단히 Python 3.9를 Docker로 실행해 봅니다.

```bash
docker run --rm -it python:3.9 bash
```

잘 되는 걸 확인했으니 본격적인 환경 설정에 들어갑시다.

현재 폴더를 개발하는데 쓸 수 있도록
[volume](https://docs.docker.com/storage/volumes/)을 추가해 봅니다.
컨테이너 안에서는 `/work` 폴더를 사용하도록 하고, working directory로 지정합니다.

```bash
docker run --rm -it \
    -v $(pwd):/work \
    -w /work \
    python:3.9 bash
```

## Virtualenv

컨테이너가 실행될 때마다 기존에 설치한 패키지 등이 모두 사라지므로
현재 폴더에 패키지 등을 고스란히 남기기 위해
[`virtualenv`](https://github.com/pypa/virtualenv)를 사용하겠습니다.

컨테이너 안에서 다음과 같이 `virtualenv`를 설치하고 `venv` 폴더를 만듭니다.

```bash
pip install virtualenv
virtualenv venv
```

격리된 가상 환경을 사용하려면 다음과 같이 해야 합니다.

```bash
source venv/bin/activate
```

Docker 컨테이너를 실행하고 매번 이걸 실행하는 건 불편한 것 같습니다.

`_profile` 파일을 만들어서 컨테이너를 실행할 때 `.bashrc`로 사용하겠습니다.

```bash
echo "source venv/bin/activate" > _profile
```

```bash
docker run --rm -it \
    -v $(pwd)/_profile:/root/.bashrc \
    -v $(pwd):/work \
    -w /work \
    python:3.9 bash
```

## Continuous Test

이제 `pytest`와 `pytest-watch`를 설치하고 잘 작동하는지 확인합니다.

컨테이너 안에 다시 들억가서 설치해 봅시다.

```bash
pip install -U pip
pip install pytest pytest-watch
```

컨테이너에서 나갔다가 다시 컨텡이너에 들어가서 잘 되는지 확인합니다.

```bash
pytest

ptw
```

## 결론

`Dockerfile` 등으로 제대로 된 개발 환경을 구축하는 게 좋지만
가볍게 실험할 때는 너무 과하다는 생각을 지우기 어렵습니다.
그래서 다음과 같이 빠르게 개발 환경을 구축하고, 단계별로 다듬어 가면 좋을 것 같습니다.

```bash
# 계속 사용할 스크립트 파일을 만들어 줍니다.
echo -e "docker run --rm -it \\
    -v \$(pwd)/_profile:/root/.bashrc \\
    -v \$(pwd):/work \\
    -w /work \\
    python:3.9 bash" > dev.sh
chmod +x dev.sh

# Virtualenv를 위한 임시 세팅
echo "pip install virtualenv && virtualenv venv" > _profile
./dev.sh

# 컨테이너에서 바로 빠져나옵니다
exit
########################

# 제대로 된 환경 세팅
echo "source venv/bin/activate" > _profile

# 이제는 이 스크립트만 실행하면 됩니다.
./dev.sh
```
