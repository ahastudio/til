# AnyPS5: PS5 실행 파일을 에뮬레이터 없이 Linux·Windows 프로그램으로 다시 링크하는 도구

<https://github.com/boykopovar/AnyPS5>

HN 토론: <https://news.ycombinator.com/item?id=49985664> (371점, 323개 댓글)

GN 토론: <https://news.hada.io/topic?id=34927>

## 소개

AnyPS5는 PS5용 실행 파일을
Linux와 Windows의 네이티브 프로그램으로 바꾸는 도구다.
저장소 설명은 PS5 실행 파일을 Linux와 Windows로 자동 포팅하는 도구이고,
README는 에뮬레이션도, 별도의 런타임 프로세스도 없다고 강조한다.
구성은 두 부분이다.
실행 파일을 대상 운영체제의 형식으로 바꾸는 리링커(relinker)와,
변환된 프로그램이 동적 링크로 불러 쓸 PS5 시스템 `prx` 라이브러리의 재구현이다.

만든 사람은 GitHub 계정 boykopovar이며,
프로필에는 벨라루스, 역공학과 프로토콜 분석, C++·C#·Python이 적혀 있다.
저장소는 2026년 8월 3일에 만들어졌고,
첫 이슈는 9월 24일, 첫 릴리스 v0.1.0과 v0.1.1은 9월 28일에 나왔다.
10월 11일 기준으로 별 2만 7천여 개, 포크 2,300여 개를 모았고,
같은 날 GitHub Trending 2위에 올랐다.
라이선스는 GPL 2.0 only다.

| 항목                | 10월 11일 기준 값                                  |
| ------------------- | -------------------------------------------------- |
| 언어                | C++ 대부분, Python·CMake 도구, 약간의 C와 어셈블리 |
| 기여자              | 213명                                              |
| 풀 리퀘스트         | 2,843개, 그중 병합 1,673개                         |
| 이슈                | 380개, 그중 열린 것 147개                          |
| 재구현한 라이브러리 | `core/libs/prx` 아래 디렉터리 120개                |
| 최신 릴리스         | v0.1.1 (9월 28일)                                  |

진척도 페이지는 시스템 라이브러리 86.04%(3,253개 중 2,799개),
GPU 셰이더 명령어 100%(1,166개 중 1,166개)를 보여 준다.
두 숫자 모두 분모를 잘 읽어야 한다.
라이브러리 쪽 분모는 PS5의 모든 시스템 함수가 아니라
프로젝트가 지금까지 `core/libs/prx`에 선언한 함수이고,
선언이 늘면 분모도 커진다고 README가 직접 밝힌다.
셰이더 쪽 분모는 AMD RDNA 1과 RDNA 2 명령어 목록이며,
디코더가 명령어를 알아보면 구현된 것으로 센다.
명령어의 의미가 하드웨어와 똑같이 동작한다는 뜻은 아니다.

검증된 게임 목록에는 아직 한 줄만 있다.

| 게임           | ID        | Windows           | Linux | GTX 1050 Ti / i5-7500 | Intel HD Graphics 620 / i5-7200 |
| -------------- | --------- | ----------------- | ----- | --------------------- | ------------------------------- |
| Dreaming Sarah | PPSA02929 | In game, playable | ?     | 60 FPS                | 36 FPS                          |

이슈 목록에는 Ghost of Yōtei, 007 First Light, Palworld, Silksong,
Ratchet & Clank: Rift Apart 같은 상용 타이틀을 띄우다 멈춘 지점을
하나씩 쫓는 글이 많다.
이것은 이 타이틀들이 돌아간다는 뜻이 아니라,
기여자들이 이 타이틀을 시작 지점부터 한 단계씩 통과시키는 중이라는 뜻이다.

정적 재컴파일로 고전 DOS 데모를 브라우저에서 돌리는 사례는
`game/demoscene-recomp.md`에 정리되어 있다.
AnyPS5는 원본과 대상의 CPU가 같아 명령어를 번역하지 않는다는 점에서 그와 다르다.

## 동작 방식

### CPU 쪽: 번역하지 않고 다시 링크한다

PS5의 CPU는 AMD Zen 2 계열 x86-64이므로,
PC에서 같은 기계어를 그대로 실행할 수 있다.
AnyPS5가 바꾸는 것은 명령어가 아니라 실행 파일의 겉모양과 링크 정보다.
`docs/dev/ARCHITECTURE.md`가 그리는 흐름은 다음과 같다.

```text
input.elf + sce_module/*
  -> [--to-intel] AMD 전용 명령어를 Intel에서 도는 코드로 바꿈
  -> RelinkerPipeline: NID로 가져오기 목록을 읽고, syscall을 검사하고,
     쓰지 않는 NID를 거르고, SysV 동적 섹션을 만듦
  -> GuestModuleBuilder: 게임에 딸린 모듈도 변환
  -> LinuxElfPatcher / WindowsPePatcher
  -> app.elf 또는 app.exe + app0/sce_module/*

core/libs/prx/* (공유 라이브러리로 빌드)
  -> nid_patcher: 내보내는 함수 이름을 NID로 바꿈
  -> libs/*.prx

실행 시: 운영체제 로더가 NID를 기준으로 가져오기를 libs/*.prx에 연결
```

PS5 게임은 시스템 함수를 이름이 아니라 함수 이름에서 계산한 NID로 가져온다.
AnyPS5는 자기가 재구현한 라이브러리의 내보내기 이름을 빌드 뒤에 NID로 바꿔 두고,
리링커는 게임의 가져오기 목록을 Linux의 ELF 동적 섹션이나 Windows PE의 가져오기
형태로 다시 쓴다.
그러면 Linux의 `ld.so`나 Windows 로더가 평범한 공유 라이브러리를 연결하듯
게임과 재구현 라이브러리를 이어 준다.
별도의 에뮬레이터 프로세스가 없다는 README의 주장은 이 구조를 가리킨다.

리링커는 코드에서 직접 `syscall`을 부르는 명령어를 찾으면 변환을 멈춘다.
시스템 호출은 반드시 재구현 라이브러리를 거쳐야 하기 때문이다.
`--to-intel`은 Intel CPU에 없는 AMD 전용 명령어를 바꾸는 선택 단계이고,
`--to-rosetta`는 여기에 더해 Rosetta가 지원하지 않는 RDSEED, CLWB, RDPID를
RDRAND, NOP, 프로세서 0 반환으로 낮춘다.

### GPU 쪽: 셰이더는 실행 중에 SPIR-V로 다시 컴파일한다

CPU 코드와 달리 GPU 쪽은 그대로 실행할 수 없다.
게임이 제출한 명령 버퍼는 `libSceAgcDriver`가 받아 PM4 패킷을 해석하고,
상태와 드로우, 디스패치를 Vulkan으로 옮긴다.
셰이더는 RDNA 기계어를 디코드해 제어 흐름 그래프를 만들고,
중간 표현으로 번역하고 최적화한 뒤 SPIR-V로 내보낸다.
컴파일된 결과는 메모리와 디스크 캐시에 남아 다음 실행에서 다시 쓰인다.
`VK_EXT_graphics_pipeline_library`를 지원하는 장치에서는
파이프라인을 네 조각으로
나눠 빠르게 링크하고, 백그라운드에서 링크 타임 최적화를 거친 판으로 바꿔 끼운다.

정리하면 CPU 쪽은 재링크, GPU 쪽은 실행 중 번역이다.
에뮬레이터가 없다는 말은 CPU 쪽에서는 정확하지만,
GPU 쪽은 Wine 위의 DXVK나 vkd3d와 비슷하게 실행 중에 번역하는 계층이다.
HN에서 tancop은 코드를 확인해 보니 셰이더를 실행 중에 RDNA에서 SPIR-V로
다시 쓰고, 디스크 캐시가 이진 형식이라 DXIL을 번역하는 vkd3d보다 크게 느리지는
않을 것이라고 적었다.[^tancop]

### 실패 정책: 모르면 멈춘다

README는 지원하지 않거나 예상하지 못한 상태에서는 반드시 `std::runtime_error`를
던지고, 표준 오류에 내용을 찍은 뒤 프로세스를 끝낸다고 적는다.
`CONTRIBUTING.md`도 같은 원칙을 반복한다.
모든 함수는 해야 할 일을 정확히 하거나 예외를 던지고,
구현하지 않은 내보내기는 `NotImplemented_nid_no_patch(__func__)`를 부른다.
빠진 가져오기는 대체 동작으로 넘기지 말고,
시작 시점에 분명한 오류로 실패해야 한다.

예외는 하나다.
화면 UI에만 영향을 주고 타이틀을 진행시키는 데 꼭 필요할 때만
조용한 스텁을 허용하고,
그 목록을 `docs/dev/TechnicalDebt.md`의 Silent stubs 절에 남긴다.
지금 이 목록에는 UI 없이 버튼 1로 답하는 메시지 대화상자,
사용자가 취소한 것으로 답하는 로그인 대화상자,
헤드셋이 없다고 답하는 PS VR 계열,
네트워크에 닿지 않는 HTTP 라이브러리 등이 있다.

HN에서 wurstburst는 2분만 코드를 봐도 매핑했다는 함수 상당수가 그냥 성공을
돌려준다며 비율에 속지 말라고 경고했다.[^wurstburst]
저장소의 규칙은 그런 스텁을 목록으로 관리하라는 것이고,
진척도 집계도 `NotImplemented_nid_no_patch`를 부르는 함수만 미구현으로 센다.
조용한 스텁이 규칙대로 기록되어 있더라도 진척도 숫자에는 구현으로 잡힌다는 점은
두 말이 함께 맞을 수 있는 지점이다.

## 사용하기

### 변환

이 문서를 쓰면서 도구를 빌드하거나 실행하지는 않았다.
아래 내용은 `docs/user/USAGE.md`를 옮긴 것이다.

리링커의 입력은 SELF 컨테이너가 아닌 평범한 ELF 실행 파일이다.
코드도 첫 4바이트를 확인해 SELF면 `The input is a SELF container, not an ELF`
오류를 내고 멈춘다.
게임에 딸린 모듈은 실행 파일 옆의 `sce_module/`, `sce_modules/`,
`prx/` 중 하나에
둔다.

```text
source/
    input.elf
    sce_module/
        <bundled ELF modules>
```

```bash
# Linux ELF (출력 형식은 파일 이름과 무관하게 기본값이 Linux)
relinker source/input.elf app.elf

# Windows PE (.exe 확장자만으로는 Windows가 선택되지 않는다)
relinker --windows source/input.elf app.exe

# x86-64 Mach-O, Apple silicon에서는 Rosetta로 실행
relinker --macos --to-rosetta source/input.elf eboot
```

| 옵션              | 효과                                                        |
| ----------------- | ----------------------------------------------------------- |
| `--windows`       | Windows PE 실행 파일을 만든다                               |
| `--windows-gui`   | 콘솔 대신 GUI 서브시스템으로 만든다                         |
| `--to-intel`      | AMD 전용 명령어를 바꾼다. 바꿀 수 없는 명령어가 있으면 오류 |
| `unused-filter=1` | 제어 흐름 분석으로 쓰지 않는 PLT 외 가져오기를 거른다       |
| `unused-filter=2` | 엄격한 분석과 PLT 압축. 분석할 수 없는 경우는 오류          |
| `--registry`      | 가져오기 목록을 `<이름>.registry.json`으로 남긴다           |
| `--rpath <path>`  | 시스템 라이브러리 경로. 기본값 `$ORIGIN/libs`               |
| `--autorun`       | 변환 직후 실행하고 종료 코드를 출력한다                     |

`--help`는 없고, 인수 없이 실행하면 사용법을 찍고 오류로 끝난다.
`--skip-sce-module`, `--skip-syscall-check`,
`--lazy-binding` 등은 폐기 예정이며,
문서는 이 옵션으로 돌린 앱은 매우 불안정해 디버깅에만 쓰라고 적는다.

### 실행 배치

```text
app.elf (Linux) 또는 app.exe (Windows)
libs/
    *.prx          <- AnyPS5가 빌드한 시스템 라이브러리
app0/
    <app resources>
    sce_module/
        <converted modules>
```

`libs/`에는 PS5 원본 `.prx`가 아니라 AnyPS5가 대상 운영체제용으로 빌드한
라이브러리를 넣는다.
원본 모듈을 Windows의 `libs/`에 넣으면 Windows가 DLL로 읽으려다 오류 193을 낸다.
게임 리소스는 `app0/`에 따로 넣어야 한다.

실행 환경을 바꾸는 환경 변수도 몇 개 있다.
`ANYPS5_LANGUAGE`는 콘솔 언어 번호를 정하며 한국어는 9다.
`ANYPS5_GPU`는 장치 이름의 일부로 GPU를 고르고,
`ANYPS5_SYSTEM_FONTS`는 시스템 글꼴 디렉터리를 바꾼다.
콘솔 글꼴이 없으면 Noto Sans 계열 대체 글꼴을 쓰고,
둘 다 없으면 그 글꼴로 그리는 텍스트가 나오지 않는다.
입력은 SDL이 인식하는 게임패드를 쓰고,
키보드와 마우스는 실행 파일 옆의 `anyps5-input.ini`로 다시 지정한다.

### 실행 전 점검: 가져오기 감사

```bash
relinker --registry source/input.elf app.elf
python3 tools/import_audit.py app.registry.json \
  app.libc.prx.guest.prx.registry.json \
  --libs build/core/libs/libs --modules source/sce_module
```

`tools/import_audit.py`는 게임이 가져오는 함수를 네 가지로 나눈다.
`implemented`는 구현되어 있음, `stub`은 불리는 순간 예외를 던짐,
`absent`는 어떤 라이브러리도 내보내지 않아 로더가 실패함,
`module`은 게임 자신의 모듈이 내보냄이다.
게임을 띄워 보기 전에 어디서 멈출지 미리 알 수 있는 가장 싼 방법이다.

## 빌드

리링커만 빌드하는 모드는 서브모듈, SDL, Vulkan, FFmpeg 없이
CMake와 C++20 컴파일러만 있으면 되고, Linux, Windows, macOS에서 돈다.

```bash
cmake -S . -B build-relinker -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DANYPS5_RELINKER_ONLY=ON -DBUILD_TESTING=ON
cmake --build build-relinker --parallel
ctest --test-dir build-relinker --output-on-failure
```

전체 빌드는 x86-64, CMake 3.22.1 이상, Ninja가 필요하고,
서브모듈로 SDL, Vulkan-Headers, SPIRV-Tools, glslang, FreeType, libjpeg-turbo,
FFmpeg 등을 소스에서 빌드한다.

```bash
git submodule update --init --recursive
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++
cmake --build build --parallel
# prx 라이브러리는 EXCLUDE_FROM_ALL이라 이 단계를 따로 돌려야 갱신된다
cmake --build build --target libs --parallel
```

Windows는 WinLibs의 MinGW-w64 GCC 15.2.0(`x86_64-ucrt-posix-seh`, `r7`) 하나만
지원한다.
직접 빌드한 Windows용 `libs/`에는 `libgcc_s_seh-1.dll`, `libstdc++-6.dll`,
`libwinpthread-1.dll`을 함께 두어야 하고, `PATH`에 있는 복사본은 찾지 않는다.
릴리스 압축 파일에는 이 DLL이 이미 들어 있다.

v0.1.1 릴리스는 리링커 실행 파일과 Linux·Windows용 `prx` 묶음을 올렸다.
다운로드 수는 Windows용 리링커가 16,633회, Windows `prx` zip이 20,904회로,
Linux용보다 몇 배 많다.

## 개발 방식

### 규칙이 촘촘한 저장소

`CONTRIBUTING.md`와 `docs/dev/CONVENTIONS.md`는 짧지만 단호하다.

- 코드 주석은 기술 부채 표시(사람만 추가), `#endif` 끝, 네임스페이스 끝에만 허용한다.
- 셰이더 명령어 의미를 바꾸는 PR은 출처를 밝힌다. 하드웨어에서 측정했거나, ISA 절, LLVM, ACO, Mesa 파일 중 정확한 근거가 있어야 한다.
- 근거로 정해지지 않는 경우는 예외를 던지고, 하드웨어로 확인하지 않은 동작은 기술 부채에 기록한다.
- 특정 타이틀이 필요로 하는 동작이 아니라 함수의 일반 동작을 구현한다.
- 게임이 직접 들고 오는 엔진이나 미들웨어 모듈(Cohtml, FMOD 등)은 재구현하지 않는다.
- 각 테스트는 CI에서 30초 안에 끝나야 한다.
- PR에는 AI 도움을 받았는지 적고, 작성자가 모든 줄에 책임진다.

셰이더 의미를 확인하는 도구도 저장소에 있다.
`tools/hw-oracle/`은 몇 줄의 RDNA 어셈블리를 로컬 AMD GPU에서 돌려,
레인마다 하드웨어가 계산한 값을 돌려준다.
문서는 PS5 GPU를 gfx1013으로 적고, 다른 RDNA2 GPU(gfx103x)가
gfx10.1 전용 명령 몇 개를 빼면 같은 인코딩을 쓴다고 설명한다.
문서가 흐릿한 명령어는 실제 하드웨어 결과로 모델을 맞추고,
측정한 값을 테스트의 기대값으로 고정한다.

`docs/dev/TechnicalDebt.md`는 25만 바이트가 넘는다.
모르는 함수 시그니처, 콘솔에서 확인하지 못한 동작, 조용한 스텁,
FreeBSD libthr나 shadPS4, KytyPS5 같은 참고 구현에서 가져온 가정이
하나씩 출처와 함께 적혀 있다.

### 에이전트가 쓴 코드가 대부분이다

최근 PR 300개는 10월 10일 오후부터 11일 사이 하루 남짓 동안 열렸다.
이 가운데 템플릿의 AI-assisted 칸을 채운 265개 중 261개가 yes였고,
no는 1개였다.
Claude Code나 Codex로 준비했다고 밝힌 PR이 많고,
병합 커밋에는 `codex/`로 시작하는 브랜치 이름이 흔하다.
이슈 번호와 PR 번호가 공유되는 GitHub에서, 10월 11일 기준 번호는 3,290을 넘었다.

PR의 빌드 정책도 이 속도에 맞춰져 있다.
PR이 열리면 규약 검사와, 이미 `main`에 커밋이 있는 작성자에 한해
리링커 테스트가 자동으로 돈다.
전체 Linux·Windows 빌드는 쓰기 권한이 있는 협업자가 수동으로 시작할 때만 돈다.
규약 검사는 PR 코드를 실행하지 않고 Git 객체만 읽는다.
낯선 기여자가 하루 수백 개 PR을 올리는 저장소가 CI를 지키는 방법이다.

HN에서 pitched는 활동량과 AI를 많이 쓴 흔적을 보면
에이전트가 부팅될 때까지 쉬지 않을 테니,
출시 직후 무언가 돌아가는 것을 의심하지 않는다고 적었다.[^pitched]
bananaboy는 흥미로운 기술 문제지만 요즘은 AI로 풀기 때문에 그 문제에 대해
배우는 것이 없다고 맞받았다.[^bananaboy]

## 법적 경계

### 저장소가 밝힌 범위

README의 고지문은 이 프로젝트가 상호운용성, 연구, 보존, 호환성을 위한 것이라고
말한다.
저작권이 있는 소프트웨어, 펌웨어, 암호 키, 독점 라이브러리를 포함하지도,
배포하지도, 요구하지도 않으며,
쓰는 바이너리를 법과 라이선스에 맞게 얻고 쓰는 책임은 사용자에게 있다고 적는다.
코드도 이 경계에 맞춰져 있다.
리링커는 암호화된 SELF를 받지 않고 오류로 거절하며,
복호화 기능은 저장소에 없다.
`libs/`에 원본 PS5 시스템 모듈이 아니라 자체 재구현을 넣으라고 문서가 명시하고,
글꼴도 콘솔에서 꺼낸 파일이 없으면 공개 라이선스 대체 글꼴을 쓰는 구조다.

### 일반적으로 알려진 사실

여기부터는 저장소가 아니라 일반 사실과 HN 토론에서 나온 이야기다.
PS5 게임은 콘솔에서 암호화된 형태로 배포되므로,
AnyPS5에 넣을 평범한 ELF를 얻으려면 그 게임을 돌릴 수 있는 콘솔에서 복호화한
덤프가 필요하다.
HN에서 kristofferR은 게임을 복호화해 꺼내려면 현재 펌웨어의 익스플로잇이 있어야
한다고 설명했다.[^kristofferR]
이 도구의 실제 쓸모는 결국 그 앞 단계에 달려 있다는 뜻이다.

콘솔 에뮬레이터나 변환 도구 자체가 곧 불법인 것은 아니지만,
닌텐도가 Yuzu를 상대로 소송을 걸어 개발을 중단시킨 일처럼
플랫폼 회사가 법적 압력을 넣은 전례는 있다.
HN 첫머리에서 someperson은 Yuzu와 Ryujinx처럼 법적 위협으로 내려갈 수 있으니
이런 프로젝트는 로컬 클론을 남겨 두는 것이 좋다고 적었다.[^someperson]
기술적 수단을 우회하는 행위나 플랫폼 이용 약관 위반은
도구의 합법성과 별개로 따져야 할 문제이며,
나라마다 판단이 다르다.
이 문서는 법적 판단을 하지 않는다.

## 트레이드오프

### 재링크는 빠르지만 CPU 차이를 숨길 곳이 없다

명령어를 번역하지 않으니 CPU 코드는 사실상 원래 속도로 돈다.
대신 PS5와 호스트 CPU가 다른 지점은 정적으로 해결해야 한다.
Zen 2에는 있지만 Intel에는 없는 명령어가 있으면 `--to-intel`로 미리 바꿔야 하고,
바꿀 수 없는 명령어를 만나면 오류로 끝난다.
JIT 번역기라면 실행 중에 만난 문제를 그 자리에서 처리할 수 있지만,
재링크 방식은 변환 시점에 보이지 않는 경로를 다룰 수 없다.
게임이 직접 `syscall`을 쓰면 변환을 거부하는 것도 같은 이유다.

### 시스템 라이브러리 재구현은 분모가 계속 커진다

AnyPS5가 하는 일의 대부분은 Sony의 시스템 라이브러리를 다시 만드는 것이다.
문서가 없는 API의 시그니처를 타이틀이 실제로 넘기는 인자로 추론하고,
shadPS4나 KytyPS5, SharpProspero 같은 다른 프로젝트의 가정을 빌려 오며,
그 가정을 기술 부채로 남긴다.
타이틀이 하나 더 시작될 때마다 새 함수가 발견되므로
진척도 비율은 올라가기도 하고 내려가기도 한다.
86%라는 숫자는 끝이 얼마나 가까운지가 아니라 지금 아는 범위 안의 채움 비율이다.
HN에서 bathtub365도 제출 제목의 87%가 README의 단서를 빼먹은 큰 사실 오류라고
지적했다.[^bathtub365]

### 멈추는 정책은 디버깅을 돕지만 실행 가능한 게임을 줄인다

모르는 상태에서 즉시 멈추면 잘못된 동작이 조용히 퍼지지 않고,
에이전트나 사람이 다음에 고칠 지점이 정확히 드러난다.
이슈 목록이 타이틀마다 시작 지점에서 멈추는 순서를 기록하는 형태인 것도
이 덕분이다.
반대로 에뮬레이터들이 흔히 쓰는 일단 성공을 돌려주고 넘어가는 방식보다
실제로 끝까지 돌아가는 게임 수는 적을 수밖에 없다.
검증된 게임이 한 개뿐인 이유 일부는 이 정책에 있다.
UI 전용 조용한 스텁만 예외로 둔 것은 그 사이의 절충이다.

### GPU 의미를 맞추는 비용은 하드웨어마다 다시 든다

셰이더를 SPIR-V로 옮긴 뒤 실제로 실행하는 것은 NVIDIA, AMD, Intel의 각기 다른
Vulkan 드라이버다.
열린 이슈에는 NVIDIA에서만 장치를 잃는 경우,
Intel UHD 770에서만 실패하는 셰이더 테스트,
`/dev/udmabuf` 권한이 없으면 GPU 쓰기가 실패하는 Linux 설정 문제가 섞여 있다.
하드웨어 오라클로 RDNA의 의미를 측정해도,
그 의미를 다른 회사 GPU에서 똑같이 재현하는 일은 드라이버마다 따로 남는다.

## 함정

- Windows에서 직접 메모리는 게임이 할당하는 순간 전부 커밋된다(타이틀당 최대 13,824 MiB). 설치 메모리와 페이지 파일을 합친 커밋 한도가 부족하면 할당 단계에서 예외가 난다.
- Linux에서 NVIDIA 독점 드라이버가 아닌 경우 `/dev/udmabuf` 읽기·쓰기 권한이 필요하다. 권한이 없으면 메모리가 복사로 처리되고 일부 GPU 쓰기가 `BDA access failed`로 실패한다.
- `cmake --build build`만 돌리면 `prx` 라이브러리가 갱신되지 않는다. `libs` 타깃을 따로 빌드하지 않으면 이전 바이너리로 테스트하게 되어 수정이 아무 효과가 없어 보인다.
- Windows 백신이 테스트가 임시 디렉터리에 만드는 실행 파일을 격리해 `optional_plt` 등 몇몇 테스트가 실패할 수 있다.
- 비 ASCII 문자가 들어간 디렉터리에서 변환이 실패하던 Windows 이슈가 있었다. 경로는 ASCII로 두는 편이 안전하다.
- README는 Linux와 Windows만 말하지만 `--macos` 출력 옵션은 이미 있다. 다만 리링커 전용 빌드는 macOS 게임 실행을 제공하지 않고, 기술 부채 문서도 macOS 메모리 경로가 아직 트리에 없다고 적는다.
- 스토리지 이미지 결과를 늦게 쓰는 구조 때문에, 메모리를 재사용하는 타이틀에서 새 데이터가 덮어써질 수 있다. `APS5_STORE_AT_FLIP=1`이 우회책이지만 프레임마다 쓰기 비용이 든다.

## 기억할 원칙

### 진척도 숫자는 분모부터 읽는다

AnyPS5의 86%와 100%는 둘 다 사실이지만, 둘 다 독자가 처음 떠올리는 질문,
즉 PS5 게임이 얼마나 돌아가느냐에 대한 답이 아니다.
하나는 지금까지 발견한 함수 중 채운 비율이고,
다른 하나는 디코더가 알아보는 명령어의 비율이다.
가장 정직한 지표는 한 줄짜리 호환성 표다.
저장소가 README에 분모를 직접 밝혀 둔 것은 좋은 습관이지만,
제목과 기사로 옮겨지는 순간 그 단서는 쉽게 사라진다.

### 에이전트를 많이 쓸수록 실패를 시끄럽게 만들어야 한다

이 저장소는 하루 수백 개의 AI 보조 PR을 받으면서도,
모르면 멈추고, 근거를 밝히고, 가정은 기록하라는 규칙을 기계적으로 검사한다.
조용히 성공을 돌려주는 코드는 에이전트가 테스트를 통과시키기 가장 쉬운
지름길이기도 하다.
예외를 기본값으로 삼고 예외의 예외를 목록으로 관리하는 방식은,
사람이 모든 줄을 읽을 수 없는 속도에서
무엇이 아직 거짓인지를 보이게 하는 장치다.
이 해석은 저장소 문서가 직접 말한 것이 아니라,
규칙과 PR 흐름을 함께 놓고 본 판단이다.

---

[^tancop]: <https://news.ycombinator.com/item?id=50010838>

[^wurstburst]: <https://news.ycombinator.com/item?id=49992607>

[^pitched]: <https://news.ycombinator.com/item?id=49986578>

[^bananaboy]: <https://news.ycombinator.com/item?id=49987067>

[^kristofferR]: <https://news.ycombinator.com/item?id=49987579>

[^someperson]: <https://news.ycombinator.com/item?id=49985765>

[^bathtub365]: <https://news.ycombinator.com/item?id=49986887>
