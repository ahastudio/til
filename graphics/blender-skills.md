# Blender Agent Skills: 모델링부터 리깅, 베이크, 내보내기까지 22개 스킬로 에이전트가 Blender를 다루게 하는 모음

<https://github.com/EL4CTEO/blender-skills>

## 소개

Blender Agent Skills는 코딩 에이전트가 Blender 5.2 LTS 이상에서 3D 작업을 하도록 돕는 Agent Skills 모음이다.
대상 에이전트는 Claude Code, Codex, OpenCode, Gemini CLI, GitHub Copilot, Cursor다.
README는 모델링, UV, PBR, 베이크, 리깅, 애니메이션, 최적화, 내보내기, 렌더링, 시간대, 날씨, 시뮬레이션, QA까지 전체 3D 파이프라인을 스킬 22개가 다룬다고 소개하고, 모든 스크립트를 실제 Blender에서 시험했다고 적는다.

저장소는 2026년 10월 14일에 만들어졌고 MIT 라이선스다.
10월 14일에 스킬 20개로 0.1.0을 냈고, 10월 16일의 1.1.0에서 시간대(`blender-time-of-day`)와 날씨(`blender-weather-fx`) 스킬, 비교 페이지, 배너와 아이콘이 들어갔다.
이 글을 쓸 때 별은 413개, 포크는 38개, 열린 이슈는 0건이었고 마지막 푸시는 10월 19일이었다.
만들어진 지 닷새쯤 된 저장소라서 이슈나 사용 후기로 검증된 기간이 거의 없다.

## 설치와 사용

Claude Code에서는 플러그인으로 설치한다.

```text
/plugin marketplace add EL4CTEO/blender-skills
/plugin install blender-agent-skills@blender-agent-skills
```

다른 에이전트는 저장소를 클론한 뒤 설치 스크립트를 돌린다.

```bash
git clone https://github.com/EL4CTEO/blender-skills
./blender-skills/install/install.sh          # macOS / Linux
.\blender-skills\install\install.ps1         # Windows
```

설치 스크립트의 기본값은 사용자 범위(개인 스킬 디렉터리)이고 에이전트로는 Claude와 `.agents/skills`를 읽는 에이전트들이다.
기본은 심볼릭 링크이며 `--copy`로 복사할 수 있다.
옵션은 `--agent claude|codex|opencode|gemini|copilot|cursor|all`, 한 프로젝트에만 설치하는 `--project DIR`, 제거하는 `--uninstall`, 일부 스킬만 고르는 `--skills`다.

요구 사항은 Blender 5.2 이상이다.
선택 사항으로 Blender MCP 서버를 두면 에이전트가 열려 있는 Blender에서 작업하고, 없으면 에이전트가 Blender를 백그라운드로 실행한다.
사용은 평범한 요청 문장으로 한다.
README의 예는 Unreal용 게임 준비 상자를 베이크한 노멀과 LOD까지 만들어 달라는 요청, 캐릭터를 Rigify로 리깅해 Unity로 내보내라는 요청, 모델의 z-fighting과 떠 있는 부품을 검사한 뒤 Roblox용으로 내보내라는 요청, 거리를 비 오는 밤으로 만들어 달라는 요청이다.

## 스킬 구성

22개 스킬은 작업 단계별로 나뉜다.

| 스킬                           | 하는 일                                             |
| ------------------------------ | --------------------------------------------------- |
| `blender-core`                 | 시작점. 코드 실행, 작업 분배, 5.x API 규칙          |
| `blender-scene-setup`          | 단위, 이름 규칙, 컬렉션, 에셋 라이브러리            |
| `blender-hardsurface-modeling` | 베벨, 불리언, 가중 노멀                             |
| `blender-sculpting`            | 유기체 스컬프팅                                     |
| `blender-retopology-uv`        | 리토폴로지, UV, 텍셀 밀도                           |
| `blender-pbr-materials`        | 텍스처로 만드는 PBR 머티리얼                        |
| `blender-texture-baking`       | 노멀, AO, 곡률 맵과 ORM                             |
| `blender-geometry-nodes`       | 간단한 JSON으로 하는 절차적 모델링                  |
| `blender-character-rigging`    | Rigify, 스키닝, 게임 스켈레톤                       |
| `blender-facial-shapekeys`     | ARKit 52 블렌드셰이프, 비세임                       |
| `blender-animation`            | 액션, NLA, 모캡, 루트 모션                          |
| `blender-game-optimization`    | 예산, LOD, 드로 콜                                  |
| `blender-export-pipelines`     | Roblox, Unity, Unreal, Godot, 웹, USD               |
| `blender-rendering`            | Cycles와 EEVEE, 배치 렌더링                         |
| `blender-lighting-lookdev`     | 스튜디오 조명, HDRI, 턴테이블                       |
| `blender-simulation`           | 리지드 바디, 천, 유체                               |
| `blender-time-of-day`          | 골든아워, 밤, 안개와 분위기 조명                    |
| `blender-weather-fx`           | 비, 눈, 젖은 거리, 웅덩이, 번개                     |
| `blender-addon-development`    | Blender 확장                                        |
| `blender-pipeline-automation`  | 배치 작업과 파일 변환                               |
| `blender-asset-qa`             | z-fighting, 떠 있는 부품, 잘못된 노멀과 가중치 검출 |
| `blender-workflow-recipes`     | 에셋 전체를 만드는 절차서                           |

## 동작 방식

### 시작점과 분배

저장소의 `AGENTS.md`는 모든 Blender 작업을 `blender-core`의 `SKILL.md`에서 시작하라고 지시한다.
이 스킬이 작업을 알맞은 전문 스킬로 보내고, 코드를 실행하는 방법을 정의한다.
스킬을 설명하는 `description`은 400자 이하, 각 `SKILL.md`는 약 2,500토큰 이하로 유지한다는 규칙도 `AGENTS.md`에 있다.
`AGENTS.md`는 스크립트를 읽지 말고 실행하라고도 한다.
각 스크립트가 독스트링에 플래그를 설명하고 결과를 압축한 JSON 한 줄로 출력하기 때문이다.
전문 스킬의 `references/` 문서는 `SKILL.md`가 가리킬 때만 불러온다.

### 실행하는 두 가지 방법

`blender-core`는 실행 경로를 둘로 나눈다.
라이브 세션에서는 Blender MCP의 `execute_blender_code`로 작은 단계씩 실행하고 필요한 값만 출력한다.
MCP 호출마다 새 네임스페이스에서 실행되므로 매번 `import`를 다시 쓰고, 이미 불러온 모듈은 `sys.modules`에 남아 있어 비용이 작다.
셸이 있는 에이전트는 헤드리스로 돌린다.

```bash
python <skills_dir>/blender-core/scripts/run_in_blender.py --blend in.blend <script.py> -- --objects Chair --save out.blend
python <skills_dir>/blender-core/scripts/run_in_blender.py --expr "import bpy; print(len(bpy.data.objects))"
```

세션의 첫 호출은 `env_report.py`로 버전, 엔진, GPU, 애드온, 단위, 색 관리, 장면 개수를 확인한다.
모든 스크립트가 `run(**kw) -> dict`를 노출하고 `--` 뒤에 같은 형태의 플래그를 받는다.

### 규칙

`blender-core`의 규칙 가운데 눈에 띄는 것은 다음이다.
연산자(`bpy.ops`)보다 데이터 API를 쓴다. 연산자는 컨텍스트와 선택에 의존하고 많은 연산자가 백그라운드 모드에 없는 3D 뷰를 요구하기 때문이다.
노드는 이름이 아니라 `type`으로 찾는다. 이름은 현지화되기 때문이다.
적용하거나 제거한 모디파이어와 객체의 파이썬 참조는 해제된 뒤에 쓰지 않는다.
기본 이름(`Cube.001`)을 믿지 않고 객체 참조를 쥐고 명시적으로 이름을 붙인다.
1 단위를 1m로 두고 베벨, 리깅, 물리, 베이크, 내보내기 전에 회전과 스케일을 적용한다.
라이브 세션은 사용자의 작업이므로 공장 설정을 읽지 않고, 만들지 않은 데이터를 지우지 않으며, 파괴적인 일괄 편집 전에는 백업본을 저장한다.

문서는 오래된 튜토리얼과 LLM의 기억이 깨지는 5.x의 변경도 표로 정리한다.
`action.fcurves`는 채널백으로, `scene.node_tree`는 `scene.compositing_node_group`으로, `BLENDER_EEVEE_NEXT`는 `BLENDER_EEVEE`로, 본 레이어는 본 컬렉션으로, `bl_info` 애드온은 `blender_manifest.toml` 확장으로 바뀌었다고 한다.
이 표는 저장소의 서술이며 이 글에서 Blender 5.2로 검증한 것은 아니다.

### 끝나기 전의 검증

`blender-core`는 완료라고 말하기 전에 세 가지를 요구한다.
숫자로 보고한다(삼각형 수, 객체 수, 머티리얼 수, 치수, 쓴 파일).
형상을 바꿨다면 `blender-asset-qa`의 `qa_check.py`를 돌린다.
눈으로 확인한다(MCP의 `look`이나 헤드리스의 `review_shots.py`가 렌더링하는 컨택트 시트).

`blender-asset-qa`는 메시나 에셋을 만들거나 고친 모든 작업의 필수 검토 관문이다.
프로파일은 `game`(기본), `render`(관대), `print`(수밀 필요), `roblox`(메시당 삼각형 2만 이하, 수밀, n-gon 없음, 영향 본 4개 이하)가 있다.
검사 항목은 z-fighting, 뒷면이 맞붙은 면, 떠 있는 조각, 안쪽으로 뒤집힌 섬, 일관되지 않은 노멀, 비다양체 모서리, 열린 경계, 퇴화한 면, 중복 정점, n-gon, 적용되지 않은 스케일, UV 문제, 잘못된 스킨 가중치다.
`errors`를 모두 고치고 `"pass": true`가 나올 때까지 다시 돌리며, 경고는 고치거나 이유를 밝히고 받아들인다.
스크립트가 판단하지 못하는 것으로 실루엣과 비율, 셰이딩 아티팩트, 보이는 교차, 숨은 내부 지오메트리, 변형, 머티리얼 할당을 사람이 확인하라고 따로 적는다.

## 비교 페이지

README는 같은 모델과 같은 프롬프트로 스킬이 있을 때와 없을 때의 결과를 비교한 페이지를 연결한다.
페이지는 모델이 Opus 5.5(medium), Blender 5.2이고, 모든 결과가 프롬프트 한 번에 나온 것이며 후속 질문, 재시도, 손 편집이 없다고 밝힌다.
다섯 작업은 4K PBR 콘크리트 벽, 침대 위로 떨어지는 담요의 천 시뮬레이션, PBR 권총의 발사와 재장전, RTS 병사의 리깅과 걷기, 기존 에셋을 절반의 삼각형으로 다시 만들기다.

마지막 작업은 수치를 싣는다.
원본 `Nova.blend`는 삼각형 5,370개이고 목표는 2,685개다.

| 항목                      | 스킬 없음 | 스킬 있음          |
| ------------------------- | --------- | ------------------ |
| 삼각형 수                 | 2,685     | 2,665              |
| z-fighting 겹침 삼각형 쌍 | 22        | 0                  |
| 뒤집힌 또는 깨진 모서리   | 1 / 1     | 0 / 0              |
| UV 겹침                   | 34%       | 0.02%              |
| 베이크한 맵               | 노멀      | 노멀, AO, 곡률, ID |
| 전체 메시 검사            | 실패      | 통과               |

이 검사는 `blender-asset-qa`로 한 것이라고 페이지가 밝힌다.
두 결과 모두 색 텍스처가 격리된 폴더 밖에 있어 색을 유지하지 못했다는 설명도 있다.

## 개발과 검증

저장소는 자체 검증 도구를 갖췄다.
`tools/validate_skills.py`는 규격, 토큰 예산, 링크, 스크립트 계약을 검사하고, `tools/run_tests.py`는 헤드리스 Blender 시험을 50개 돌린다.
공유 헬퍼 `_bpyx.py`는 `shared/`에서만 고치고 `tools/sync_shared.py`로 각 스킬의 `scripts/`에 복사하는 방식이다.

CI는 두 작업이다.
하나는 공유 헬퍼 동기화 확인, 스킬 검증, 트리거 검사, 설치 스크립트 시험이고, 다른 하나는 Blender 5.2.2를 내려받아 시험을 돌리는 것이다.
GitHub 호스트 러너에는 GPU가 없으므로 `BAS_SKIP_GPU=1`로 렌더 시험을 건너뛴다고 워크플로에 적혀 있다.
`tools/trigger_check.py`는 프롬프트 몇 십 개가 기대한 스킬을 상위 2개 안에 올리는지 설명문과의 토큰 겹침으로 점수 매기는 휴리스틱이고, 스크립트 주석이 실제 에이전트는 더 풍부한 매칭을 쓴다고 밝힌다.

## 함정

### Blender 5.2 이상에 묶여 있다

스킬의 규칙과 스크립트는 5.x의 변경을 전제로 한다.
5.2보다 오래된 Blender에서는 API 이름이 달라 스크립트가 실패할 수 있고, 새 버전이 나오면 표를 갱신해야 한다.
`blender-core`는 코드가 AttributeError나 KeyError로 실패할 때 변경 표를 불러오라고 안내한다.

### 설치 기본값은 개인 범위다

설치 스크립트의 기본 범위는 사용자 범위여서 모든 프로젝트에서 이 스킬이 후보로 잡힌다.
Blender와 무관한 프로젝트에서 쓰이지 않게 하려면 `--project DIR`로 한 프로젝트에만 설치하거나 `--skills`로 필요한 스킬만 고른다.
설치 방식은 심볼릭 링크가 기본이라 클론한 폴더를 옮기면 링크가 끊긴다.

### 라이브 세션에서 에이전트가 만지는 것은 열려 있는 작업이다

MCP로 연결하면 에이전트가 열려 있는 Blender 씬을 직접 바꾼다.
스킬은 만들지 않은 데이터를 지우지 말고 파괴적인 일괄 편집 전에 백업본을 저장하라고 규칙에 적지만, 이는 에이전트가 지키기를 기대하는 지시일 뿐 강제 장치가 아니다.
중요한 `.blend` 파일은 별도 복사본에서 작업하는 것이 안전하다.

### 렌더 시험은 CI에서 돌지 않는다

README는 모든 스크립트를 실제 Blender에서 시험했다고 하지만, CI에서는 GPU가 필요한 렌더 시험을 건너뛴다.
렌더링과 룩 개발 스킬이 자기 환경의 GPU에서 의도대로 동작하는지는 직접 확인해야 한다.

## 확인하기

도입 전에 작은 에셋으로 두 가지를 확인한다.
먼저 환경 보고를 돌려 Blender 버전과 실행 경로가 맞는지 본다.

```bash
python <skills_dir>/blender-core/scripts/run_in_blender.py --expr "import bpy; print(bpy.app.version_string)"
```

버전이 5.2 이상으로 나오는지 확인하고, 그다음 직접 만든 작은 메시에 QA 관문을 돌려 결과의 `pass`와 `errors`를 읽어 본다.

```bash
python <skills_dir>/blender-core/scripts/run_in_blender.py --blend your_asset.blend <skills_dir>/blender-asset-qa/scripts/qa_check.py -- --objects <객체이름> --profile game
```

`<skills_dir>`은 스킬을 설치한 디렉터리다.
이 명령은 저장소 문서의 사용 예를 따라 쓴 것이고 이 글을 쓰면서 Blender에서 실행하지는 않았다.

## 체크리스트

- Blender가 5.2 이상이고 실행 경로(MCP 또는 헤드리스)가 정해져 있는가?
- 설치 범위를 사용자 전체로 할지 한 프로젝트로 할지 정했는가?
- 중요한 `.blend` 파일을 별도 복사본에서 작업하고 있는가?
- 형상을 바꾼 뒤 `qa_check.py`의 `pass`와 `errors`를 확인했는가?
- 경고를 고치거나 받아들인 이유를 보고서에 적었는가?
- 실루엣, 셰이딩, 변형 같은 사람이 봐야 하는 항목을 직접 확인했는가?
- 렌더링과 룩 개발 스킬을 쓸 환경에 GPU가 있는가?

## 비평

### 비교 시험은 작업당 한 번이고 판정 도구가 스킬의 일부다

비교 페이지는 다섯 작업을 프롬프트 한 번씩만 돌렸고, 반복 실행의 분산을 보여 주지 않는다.
같은 프롬프트라고 하지만 문구가 같지 않다.
스킬 없음은 어떤 스킬도 쓰지 말고 다른 폴더를 엿보지 말라고 하고, 스킬 있음은 기존 스킬 20개를 쓰라고 하며, 다섯 작업 사이에도 스킬 수가 20, 20+, 22로 적혀 있다.

가장 숫자가 분명한 마지막 작업은 `blender-asset-qa`로 두 결과를 검사한다.
이 검사는 스킬 모음의 일부이고 스킬이 완료 전에 그 검사를 돌리라고 요구하므로, 스킬 있음 쪽이 같은 검사에서 높게 나오는 것은 어느 정도 예상되는 결과다.
스킬 없음 쪽 결과가 z-fighting 22쌍과 UV 겹침 34%인 것은 사실일 수 있지만, 이것이 스킬 없이도 같은 검사를 했을 때 에이전트가 얼마나 고쳤을지를 알려 주지는 않는다.
다섯 작업의 시각 비교는 저자가 고른 한 번의 결과이며 일반화할 수 있는 수치가 아니다.

### 토큰 효율은 설계 규칙이지 측정된 결과가 아니다

README와 홍보 글은 스킬이 토큰 효율적이라고 말하고, 저장소는 `SKILL.md`를 약 2,500토큰 이하로 유지하게 하는 검사를 둔다.
이는 스킬 하나의 크기에 대한 상한이다.
실제 작업에서 에이전트가 `blender-core`와 전문 스킬, 참조 문서, 스크립트 결과를 얼마나 읽는지를 비교 작업의 토큰 사용량으로 측정한 수치는 없다.
스킬이 없을 때 에이전트가 시행착오로 쓰는 토큰과 비교하면 오히려 절약일 수 있지만, 이 저장소는 그 비교를 싣지 않는다.

### 트리거 검사가 보여 주는 것은 설명문의 구분력이다

`trigger_check.py`는 프롬프트와 설명문의 단어 겹침으로 기대한 스킬이 상위 2개 안에 오는지 본다.
이는 설명문을 고칠 때의 회귀 방지 수단으로는 유용하지만, 실제 에이전트가 어느 스킬을 고르는지와는 다른 이야기다.
스크립트 스스로도 실제 에이전트는 더 풍부한 매칭을 쓴다고 인정한다.
스킬 22개의 설명문이 서로 겹치는 영역(내보내기, 최적화, 리깅과 애니메이션)에서 에이전트가 올바른 스킬을 부르는지는 사용해 보며 확인해야 한다.

## 기억할 원칙

### 에이전트에게 끝났다고 말할 조건을 숫자로 준다

이 저장소의 `blender-core`가 완료 전에 요구하는 것은 숫자(삼각형, 치수, 파일), 자동 검사, 눈으로 보는 확인이다.
에이전트에게 잘 만들었는지 묻지 않고 확인할 수 있는 근거를 제시하게 하는 방식은 3D 밖의 작업에도 적용된다.

### 지식이 쉽게 낡는 영역은 변경 표를 스킬 안에 둔다

에이전트는 오래된 튜토리얼의 API를 기억한다.
5.x에서 바뀐 이름을 한 표로 모아 두고 코드가 실패했을 때만 불러오게 하는 구조는, 버전이 빨리 바뀌는 도구의 스킬을 설계할 때 그대로 쓸 수 있다.
