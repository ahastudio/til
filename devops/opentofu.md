# OpenTofu

<https://opentofu.org/>

<https://github.com/opentofu/opentofu>

HN 토론: <https://news.ycombinator.com/item?id=37581132> (438점, 246개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/z7wuy3/opentofu>

## 소개

OpenTofu는 HashiCorp Terraform의 오픈소스 포크다.
2023년 HashiCorp가 Terraform의 라이선스를 BUSL(Business Source License)로 변경하자,
커뮤니티가 기존 MPL 2.0 기반 코드를 포크해 독립 프로젝트로 출발시켰다.
Linux Foundation 산하 OpenTF Foundation이 관리하며, CNCF(Cloud Native Computing Foundation) 프로젝트로 편입되었다.[^cube2222]

## 핵심 개념

**Provider** — AWS, GCP, Azure 등 클라우드나 서비스와 통신하는 플러그인이다.
각 Provider는 사용할 수 있는 리소스(Resource)와 데이터 소스(Data Source)를 정의한다.

**Resource** — 실제로 생성·관리할 인프라 구성 요소다.
EC2 인스턴스, S3 버킷, DNS 레코드 등이 Resource에 해당한다.

**State** — OpenTofu가 관리하는 인프라의 현재 상태를 기록하는 파일이다.
`.tfstate` 파일로 저장되며, 원격 백엔드(S3, GCS 등)에 두는 것이 권장된다.

**Module** — 재사용 가능한 구성 단위다.
관련 Resource를 묶어 하나의 모듈로 만들면 여러 환경에서 일관되게 쓸 수 있다.

**Plan / Apply** — `tofu plan`은 변경 사항을 미리 확인하고,
`tofu apply`는 실제로 인프라에 반영한다.

## 기본 사용법

### 설치

```bash
brew install opentofu
```

### 프로젝트 초기화

```bash
tofu init
```

Provider 플러그인을 내려받고 백엔드를 초기화한다.

### 구성 파일 예시

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-example-bucket"
}
```

OpenTofu는 Terraform과 HCL 구문 호환성을 유지한다.
기존 `.tf` 파일을 그대로 사용할 수 있다.

### 워크플로

```bash
tofu init     # 초기화
tofu plan     # 변경 사항 확인
tofu apply    # 적용
tofu destroy  # 인프라 삭제
```

## Terraform과의 차이

OpenTofu는 Terraform 1.5 기준으로 포크됐다.
이후 독자적인 기능을 추가하고 있다.

주요 차이점:

- **라이선스** — OpenTofu는 MPL 2.0, Terraform은 BUSL 1.1이다.[^edwintorok]
- **State 암호화** — OpenTofu 1.7부터 State 파일 자체를 암호화하는 기능을 내장했다.
- **Provider 함수** — Provider가 직접 함수를 제공하는 기능을 OpenTofu가 먼저 도입했다.
- **`tofu` CLI** — `terraform` 명령어 대신 `tofu`를 사용한다.

이름에 관해서는 재미있는 이야기가 있다.
Unicode에서 시스템이 문자를 렌더링하지 못할 때 나타나는 빈 사각형도 "tofu"라 불린다.[^msoad]
또한 보안 분야의 "Trust On First Use(TOFU)" 약어와도 겹친다.[^colindean]
`hk__2`는 OpenJDK나 OpenTTD처럼 "Open" 접두어가 붙으면 기존 프로젝트의 오픈소스 버전을 기대하게 되는데,
OpenTofu는 그런 경우가 아니라 혼동될 수 있다고 지적했다.[^hk__2]

## 인사이트

HashiCorp의 라이선스 변경은 오픈소스 커뮤니티가 얼마나 빠르게 대응할 수 있는지 보여준 사례다.
OpenTofu는 포크 시작 몇 달 만에 CNCF 프로젝트로 편입되며 생태계의 신뢰를 빠르게 쌓았다.
State 암호화처럼 보안 관점에서 유의미한 기능을 선제적으로 내놓으면서,
단순한 복제품이 아닌 독립적인 방향을 잡아가고 있다.

커뮤니티 신뢰 문제도 주목할 부분이다.
OpenTofu 팀은 BUSL 전환 이전부터 HashiCorp에 Terraform 지원 의사를 밝혔으나 거절당했다.[^hjr3]
`sverhagen`이 지적했듯, HashiCorp가 다시 오픈소스 라이선스로 돌아온다 해도
이미 잃어버린 신뢰를 회복할 수 있을지는 불분명하다.[^sverhagen]
`jzb`는 오픈소스 도구를 선택할 때 포크 권리가 신뢰의 실질적 근거임을 이번 사태가 보여줬다고 봤다.[^jzb]
역사적으로 더 열린 쪽이 결국 우위를 점해온 경향이 있다.[^sjamaan]

컨설턴트 입장에서는 여전히 이름 자체가 경영진 설득을 어렵게 만든다는 현실적인 지적도 있다.[^bshacklett]
인프라 코드 도구를 선택할 때 라이선스와 거버넌스 구조를 함께 고려해야 한다는 점을
이번 사태가 뚜렷하게 보여줬다.

---

[^cube2222]: <https://news.ycombinator.com/item?id=37581424>

[^edwintorok]: <https://lobste.rs/s/z7wuy3/opentofu#cxfcpf>

[^msoad]: <https://news.ycombinator.com/item?id=37581716>

[^colindean]: <https://lobste.rs/s/z7wuy3/opentofu#fjamqv>

[^hk__2]: <https://news.ycombinator.com/item?id=37582576>

[^hjr3]: <https://lobste.rs/s/z7wuy3/opentofu#gxpi6s>

[^sverhagen]: <https://news.ycombinator.com/item?id=37582456>

[^jzb]: <https://lobste.rs/s/z7wuy3/opentofu#mh2vjb>

[^sjamaan]: <https://lobste.rs/s/z7wuy3/opentofu#2qdfzt>

[^bshacklett]: <https://news.ycombinator.com/item?id=37585878>
