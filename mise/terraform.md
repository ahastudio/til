# Terraform 쿡북

<https://mise.jdx.dev/mise-cookbook/terraform.html>

인프라 명령이 항상 같은 작업 디렉터리를 가리키게 하려고 mise
태스크를 쓰는 방법을 정리한 공식 쿡북이다.
이 문서에서는 널리 알려진 Terraform이라는 이름으로 부르되,
실제 실행 도구는 OpenTofu로 구성한다.
OpenTofu는 Terraform의 오픈소스 포크이며 `devops/opentofu.md`에 따로 정리했다.

쿡북은 설정 파일이 `terraform/` 하위 디렉터리에 있고,
클라우드 자격 증명이 이미 환경에 설정되어 있다고 가정한다.
이런 구성에서는 `terraform -chdir=terraform plan` 같은 명령을 매번 입력해야
하는데, 아래 설정을 쓰면 mise 태스크로 대신 호출할 수 있다.

## OpenTofu로 구성하기

쿡북은 마지막에 OpenTofu로 바꾸는 방법을 알려 준다.
도구 선언을 `opentofu = "1"`로 바꾸고,
명령 이름 `terraform`을 `tofu`로 바꾸면 된다.
`terraform/` 디렉터리와 태스크 이름은 그대로 두거나 프로젝트에 맞게 바꿔도 된다.
여기서는 태스크 이름을 `terraform:*`로 유지해 익숙한 이름으로 부르고,
설명과 실행 명령은 OpenTofu를 가리키게 했다.

```toml
[tools]
opentofu = "1"

[tasks."terraform:init"]
description = "Initializes an OpenTofu working directory"
run = "tofu -chdir=terraform init"

[tasks."terraform:plan"]
description = "Generates an execution plan for OpenTofu"
depends = ["terraform:init"]
run = "tofu -chdir=terraform plan"

[tasks."terraform:apply"]
description = "Applies the changes required to reach the desired state of the configuration"
depends = ["terraform:init"]
interactive = true
run = "tofu -chdir=terraform apply"

[tasks."terraform:destroy"]
description = "Destroy OpenTofu-managed infrastructure"
depends = ["terraform:init"]
interactive = true
run = "tofu -chdir=terraform destroy"

[tasks."terraform:validate"]
description = "Validates the OpenTofu files"
depends = ["terraform:init"]
run = "tofu -chdir=terraform validate"

[tasks."terraform:format"]
description = "Formats the OpenTofu files"
run = "tofu -chdir=terraform fmt"

[tasks."terraform:format-check"]
description = "Check formatting without changing files"
run = "tofu -chdir=terraform fmt -check"

[tasks."terraform:check"]
description = "Check formatting and validate the configuration"
depends = ["terraform:format-check", "terraform:validate"]
```

## 사용 순서

먼저 `mise run terraform:check`로 형식과 설정을 검증하고,
이어서 `mise run terraform:plan`으로 제안된 변경을 확인한다.
`terraform:format`은 형식을 실제로 고쳐 쓰는 별도의 태스크다.
초기화는 선택한 태스크가 검사용이어도 프로바이더를 내려받고 의존성 잠금
파일을 갱신할 수 있다.

`terraform:apply`와 `terraform:destroy`는 확인 프롬프트를 그대로 유지한다.
`interactive = true`는 이 명령들이 터미널에 접근하게 해 준다.
이 구성은 계획 파일을 저장하지 않으므로,
`apply`는 승인을 묻기 전에 스스로 계획을 다시 계산한다.

## 자격 증명 파일

자격 증명을 로컬 dotenv 파일로 관리한다면
`env._.file`을 명시적으로 추가해야 한다.
평문 자격 증명 파일은 버전 관리에 올리지 않는다.
암호화해서 저장하는 방법은
mise의 [secrets 문서](https://mise.jdx.dev/environments/secrets/)를 참고한다.
