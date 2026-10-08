# Common Lisp와 cl-fast-ecs로 게임 만들기: 우주 잔해 시뮬레이션에서 던전 크롤러까지

원문: [Gamedev in Lisp. Part 1: ECS and Metalinguistic Abstraction](https://gitlab.com/lockie/cl-fast-ecs/-/wikis/tutorial-1)

원문: [Gamedev in Lisp. Part 2: Dungeons and Interfaces](https://gitlab.com/lockie/cl-fast-ecs/-/wikis/tutorial-2)

HN 토론: <https://news.ycombinator.com/item?id=41869460> (333점, 64개 댓글)

GN 토론: <https://news.hada.io/topic?id=17309>

## 소개

Common Lisp로 2D 게임을 만드는 연재 튜토리얼의 1편과 2편이다.
저자는 GitLab에서 `lockie`, itch.io에서 `awkravchuk`라는 이름을 쓰며,
연재의 중심인 ECS 매크로 라이브러리 cl-fast-ecs를 직접 만들었다.
2편에 쓰이는 A* 라이브러리 cl-astar와
Nuklear의 Common Lisp 바인딩 cl-liballegro-nuklear도 저자가 관리한다.
두 글은 cl-fast-ecs 저장소의 위키에 실려 있고,
1편은 itch.io의 cl-fast-ecs 개발 일지에도 같은 제목으로 올라왔다.

1편은 개발 환경을 갖추고,
행성 주위를 도는 우주 잔해 수천 개를 물리 시뮬레이션하는 데모를 만든다.
글을 쓸 당시 cl-fast-ecs는 0.4.0이었고,
저자는 하위 호환을 깨는 변경이 있을 수 있지만 컴포넌트와 시스템을 정의하는
매크로, 엔티티를 만드는 함수는 크게 바뀌지 않을 것이라고 적었다.
2편은 Tiled로 그린 던전 맵, 애니메이션, 키보드로 움직이는 캐릭터, A*로 길을 찾는
적, Nuklear로 그린 대화창을 갖춘 던전 크롤러를 만든다.
2편 결론에 따르면 이 게임은 약 500줄이고,
2023년 Spring Lisp Game Jam 출품작 Thoughtbound를 바탕으로 했다.
두 편의 완성 코드는 GitHub의 `lockie/ecs-tutorial-1`,
`lockie/ecs-tutorial-2` 저장소에 있다.

글이 내세우는 축은 두 가지다.
하나는 SICP가 말한 메타언어 추상화(metalinguistic abstraction),
즉 문제에 맞는 새 언어를 만들어 복잡성을 다루는 방식이고,
다른 하나는 CPU 캐시를 잘 쓰도록 데이터를
배치하는 ECS(Entity-Component-System) 패턴이다.
cl-fast-ecs는 매크로로 ECS용 작은 언어를 제공해 이 둘을 하나로 묶는다.

Lisp가 게임 개발에서 어떤 자리에 있는지는
`programming-languages/lisp-icing-or-cake.md`가
Lisp Game Jam 출품작을 놓고 다룬다.
Common Lisp를 고르는 이유는 `programming-languages/choosing-common-lisp.md`,
튜토리얼이 쓰는 컴파일러 SBCL은 `programming-languages/sbcl.md`에 정리되어 있다.
이 문서의 코드는 모두 원문에서 옮긴 것이며, 직접 실행해 보지는 않았다.

## 동작 방식

### 매크로가 만드는 작은 언어

Lisp 계열 언어는 코드가 중첩 리스트이므로,
컴파일 시점에 호출되어 코드 조각을 돌려주는 매크로로
언어 구조를 직접 늘릴 수 있다.
저자는 이를 DSL과 같은 개념이라고 하면서도,
Lisp 방언만이 이 기능을 언어 핵심에 단단히 통합했다고 주장한다.

cl-fast-ecs의 `define-component` 호출은 이름, 문서 문자열, 슬롯 목록뿐이다.
하지만 `macroexpand`로 펼쳐 보면 상당한 양의 코드가 나온다.
모든 엔티티의 컴포넌트 데이터를 담는 구조체 정의와 함께,
슬롯을 읽고 쓰는 함수, 컴포넌트를 붙이고 떼는 함수, 다른 엔티티로 복사하는 함수,
존재 여부를 묻는 술어, 슬롯을 이름으로 다루는 매크로가 생성된다.
매크로가 다른 매크로를 정의하는 셈이다.
2편에서 쓰는 `has-map-tile-prefab-p`, `make-position`, `with-animation-state`,
`assign-path`, `delete-path` 같은 이름은 모두 이렇게 생성된 것이다.

### ECS가 캐시를 쓰는 방식

1편은 폰 노이만 병목에서 출발한다.
CPU가 아무리 빨라도 메모리가 데이터를 대는 속도에 묶이고,
그 격차는 시간이 갈수록 벌어진다.
원문이 dzone.com을 출처로 든 2020년 데스크톱 기준 접근 시간은 다음과 같다.

| 위치              | 접근 시간 |
| ----------------- | --------- |
| 프로세서 레지스터 | 1ns 미만  |
| L1 캐시           | 1ns       |
| L2 캐시           | 3ns       |
| L3 캐시           | 13ns      |
| RAM               | 100ns     |

x86의 캐시 라인은 64바이트이므로 32비트 `float` 배열을 순서대로 읽으면
첫 접근 한 번에 뒤따르는 15개 원소가 함께 캐시에 올라온다.
나머지 15번은 100ns 대신 1ns가 걸리므로,
원문 계산으로는 배열 길이와 상관없이 약 14배 빨라진다.

ECS는 엔티티를 행, 컴포넌트를 열로 하는 표로 볼 수 있다.
대부분의 구현은 컴포넌트 슬롯 값을 평평한 1차원 배열에 두고 엔티티를
그 배열의 정수 인덱스로 쓴다.
시스템은 특정 컴포넌트 조합을 가진 엔티티를
모두 같은 방식으로 처리하는 루프이며,
배열을 차례로 훑기 때문에 공간 지역성을 얻는다.
이것이 ECS가 내세우는 두 목표 중 성능 쪽이고,
다른 하나는
실행 중에 컴포넌트를 붙이고 떼어 게임 객체의 구조를 바꾸는 유연성이다.

### cl-fast-ecs의 어휘

두 편에서 쓰는 cl-fast-ecs의 구성 요소를 모으면 다음과 같다.
1편은 `define-component`, `define-system`을,
2편은 `defcomponent`, `defsystem`을 쓴다.

| 구성 요소                           | 하는 일                                                         |
| ----------------------------------- | --------------------------------------------------------------- |
| `make-storage`                      | ECS 저장소 초기화, 하지 않으면 `ECS storage is not initialized` |
| `define-component` / `defcomponent` | 슬롯마다 이름, 기본값, `:type`, 선택적 `:documentation`         |
| 슬롯의 `:index`, `:unique`          | 슬롯 값으로 엔티티를 찾는 인덱스 함수 생성                      |
| 컴포넌트의 `:finalize`              | 컴포넌트가 지워질 때 호출되는 함수                              |
| `define-system` / `defsystem`       | 엔티티마다 실행할 본문과 옵션                                   |
| `:components-ro` / `:components-rw` | 읽기 전용, 읽기와 쓰기 대상 컴포넌트                            |
| `:components-no`                    | 이 컴포넌트가 있는 엔티티는 제외                                |
| `:arguments`                        | `run-systems`에 키워드로 넘긴 값을 이름으로 받음                |
| `:with`                             | 시스템 실행 초기에 한 번 계산하는 지역 변수                     |
| `:initially` / `:finally`           | 시스템 시작과 끝에 실행할 식                                    |
| `:after`                            | 다른 시스템 뒤에 실행                                           |
| `:when`                             | 조건이 참일 때만 실행                                           |
| `make-object`                       | 명세 리스트로 엔티티와 컴포넌트를 한 번에 생성                  |
| `make-entity` / `delete-entity`     | 엔티티 생성과 삭제                                              |
| `copy-entity`                       | 다른 엔티티로 컴포넌트 복사, `:except`로 제외 지정              |
| `spec-adjoin`                       | 명세에 없는 컴포넌트만 추가, 0.6.0에서 추가                     |
| `hook-up`, `*entity-deleting-hook*` | 엔티티 삭제 시 실행할 함수 등록                                 |
| `print-entity`                      | 엔티티의 컴포넌트를 `make-object` 명세 형식으로 출력            |
| `run-systems`                       | 등록된 시스템을 모두 실행                                       |

시스템 본문에서는 `position-x`, `image-width`처럼 `컴포넌트-슬롯` 형태의 변수로
현재 엔티티의 값을 읽고 쓰며, 현재 엔티티 자체는 `entity` 변수로 받는다.
`make-object`에 넘기는 명세는 다음 형태다.

```lisp
'((:component1 :slot1 "value1" :slot2 "value2")
  (:component2 :slot "value")
  ;; ...
 )
```

## 환경 준비

컴파일러는 SBCL이고 패키지 관리자는 Quicklisp다.
원문은 Ubuntu와 Debian, Fedora, Homebrew 명령을 함께 싣고 있다.

```sh
# for Ubuntu/Debian and their derivatives:
sudo apt-get install sbcl

# for Fedora:
sudo dnf install sbcl

# for MacOS with Homebrew:
brew install sbcl
```

`https://beta.quicklisp.org/quicklisp.lisp`를 받은 디렉터리에서
`sbcl --load quicklisp.lisp`를 실행하고, REPL에 다음 세 식을 넣는다.
두 번째 식은 게임 개발 패키지의 최신판을 담은 LuckyLambda 저장소를 추가한다.

```lisp
(quicklisp-quickstart:install)

(ql-dist:install-dist "http://dist.luckylambda.technology/releases/lucky-lambda.txt" :prompt nil)

(ql:add-to-init-file)
```

편집기는 VS Code와 Alive, IntelliJ IDEA와 SLT, Sublime Text와 Slyblime,
Vim과 Neovim의 Vlime, Emacs와 Sly를 제시하고,
설정이 번거로우면 Common Lisp용으로 꾸린 Emacs 배포판 Portacle을 권한다.
Windows에서는 MSYS2가 필요하다.

프로젝트 뼈대는 저자의 Python cookiecutter 템플릿으로 만든다.
백엔드는 liballegro, raylib, SDL2 중 고르는데,
원문은 Common Lisp에서 가장 덜 번거롭다는 이유로 기본값 liballegro를 고른다.

```sh
cookiecutter gh:lockie/cookiecutter-lisp-game
```

만든 디렉터리는 Quicklisp의 로컬 저장소에 링크한다.

```sh
# for UNIX-like OS:
ln -s $(pwd)/ecs-tutorial-1 $HOME/quicklisp/local-projects/
```

여기에 liballegro 개발 패키지, C 컴파일 환경(`gcc`, `pkg-config`, `make`),
C 코드 호출에 쓰는 `libffi`가 필요하다.
macOS에서는 `brew install allegro`, `brew install pkg-config`,
`brew install libffi`로 갖춘다.
그다음 `sbcl`에서 `(ql:quickload :ecs-tutorial-1)`을 실행하고
`(ecs-tutorial-1:main)`을 부르면 FPS 카운터만 있는 빈 창이 뜬다.

템플릿의 `src/main.lisp`에는 liballegro 초기화와 종료,
오류 처리, 메인 게임 루프를
담은 `%main` 콜백이 있다.
튜토리얼은 이 부분은 건드리지 않고 그
안에서 호출되는 `init`과 `update`만 고친다.
`cl-fast-ecs`는 `.asd` 파일의 `:depends-on`에 `#:cl-fast-ecs`를 더해 연결한다.

## 1편 구현하기: 우주 잔해 시뮬레이션

### 컴포넌트와 그리기 시스템

`init`에서 저장소를 초기화하고, 위치와 속도 컴포넌트를 정의한다.

```lisp
(defun init ()
  (ecs:make-storage))
```

```lisp
(ecs:define-component position
  "Determines the location of the object, in pixels."
  (x 0.0 :type single-float :documentation "X coordinate")
  (y 0.0 :type single-float :documentation "Y coordinate"))

(ecs:define-component speed
  "Determines the speed of the object, in pixels/second."
  (x 0.0 :type single-float :documentation "X coordinate")
  (y 0.0 :type single-float :documentation "Y coordinate"))
```

이미지 컴포넌트는 liballegro의 `ALLEGRO_BITMAP` C 포인터와 크기, 배율을 담는다.
첫 시스템 `draw-images`는 `position`과 `image`를 읽기만 하며,
`:initially`와 `:finally`에서 `al:hold-bitmap-drawing`을 켜고 꺼서 liballegro의
스프라이트 배칭을 쓴다.
모든 객체를 처리한 뒤에야 그래픽 API 호출이 일어나 CPU와 GPU 사이 통신을 아낀다.

```lisp
(ecs:define-component image
  "Stores ALLEGRO_BITMAP structure pointer, size and scaling information."
  (bitmap (cffi:null-pointer) :type cffi:foreign-pointer)
  (width 0.0 :type single-float)
  (height 0.0 :type single-float)
  (scale 1.0 :type single-float))

(ecs:define-system draw-images
  (:components-ro (position image)
   :initially (al:hold-bitmap-drawing t)
   :finally (al:hold-bitmap-drawing nil))
  (let ((scaled-width (* image-scale image-width))
        (scaled-height (* image-scale image-height)))
    (al:draw-scaled-bitmap image-bitmap 0 0
                           image-width image-height
                           (- position-x (* 0.5 scaled-width))
                           (- position-y (* 0.5 scaled-height))
                           scaled-width scaled-height 0)))
```

소행성 이미지는 OpenGameArt의 Asteroids
묶음에서 `small` 디렉터리를 `Resources`에
풀어 쓰고, 파일 이름을 `asteroid-images` 상수 목록으로 하드코딩한다.
`init`에서 이 이미지들을 읽어 무작위 위치에 객체 1000개를 만든다.
명세는 준인용(quasiquote)으로 조립한다.

```lisp
  (let ((asteroid-bitmaps
          (map 'list
               #'(lambda (filename)
                   (al:ensure-loaded
                    #'al:load-bitmap filename))
               asteroid-images)))
    (dotimes (_ 1000)
      (ecs:make-object `((:position
                          :x ,(float (random +window-width+))
                          :y ,(float (random +window-height+)))
                         (:image
                          :bitmap ,(alexandria:random-elt
                                    asteroid-bitmaps)
                          :width 64.0 :height 64.0)))))
```

템플릿은 `update`와 `render`를 나누지만,
ECS에서는 게임 코드가 시스템에 모이고 실행 순서도 시스템끼리 정하므로
`update`에서 `run-systems`만 부르면 된다.
`render`는 FPS 카운터만 맡는다.

```lisp
(defun update (dt)
  (unless (zerop dt)
    (setf *fps* (round 1 dt)))
  (ecs:run-systems :dt (float dt 0.0)))
```

`run-systems`는 키워드 인자를 받아 이름이 맞는 시스템에 넘긴다.
템플릿이 계산한 `dt`는 `double-float`이므로 `single-float`로 바꿔 넘긴다.

### 이동과 충돌

`move` 시스템은 `speed`를 읽고 `position`을 고친다.
그래서 `position`은 `:components-rw`에 둔다.

```lisp
(ecs:define-system move
  (:components-ro (speed)
   :components-rw (position)
   :arguments ((:dt single-float)))
  (incf position-x (* dt speed-x))
  (incf position-y (* dt speed-y)))
```

다음으로 화면 가운데에 행성을 둔다.
행성의 좌표, 크기, 질량은 `declaim`으로 `single-float` 타입을 선언한 전역 변수에
담는데, 타입 선언은 선택이지만 이 변수를 쓰는 코드의 성능에 도움이 된다.
행성에 닿은 소행성을 지우는 `crash-asteroids` 시스템은 행성을 타원으로 보고
타원 방정식으로 충돌을 판정한다.
행성 엔티티에는 슬롯 없는 태그 컴포넌트 `planet`을 붙이고,
시스템은 `:components-no`로 행성을 제외한다.

```lisp
(ecs:define-component planet
  "Tag component to indicate that entity is a planet.")

(ecs:define-system crash-asteroids
  (:components-ro (position)
   :components-no (planet)
   :with ((planet-half-width planet-half-height)
          :of-type (single-float single-float)
          := (values (/ *planet-width* 2.0)
                     (/ *planet-height* 2.0))))
  (when (<= (+ (expt (/ (- position-x *planet-x*) planet-half-width) 2)
               (expt (/ (- position-y *planet-y*) planet-half-height) 2))
            1.0)
    (ecs:delete-entity entity)))
```

`:with`는 시스템 실행 초기에 한 번만 계산되는 지역 변수를 만든다.
여기서는 행성의 반지름 두 개를 엔티티마다 다시 나누지 않도록 미리 구한다.

### 중력

마지막으로 `acceleration` 컴포넌트와 가속도를 속도에 더하는 `accelerate` 시스템을 더하고,
만유인력과 뉴턴 제2법칙에서 유도한 가속도를 계산하는 `pull` 시스템을 정의한다.
중력 상수 G는 `*planet-mass*`에 이미 곱해져 있다고 보고,
소행성끼리의 인력은 무시한다.

```lisp
(ecs:define-system pull
  (:components-ro (position)
   :components-rw (acceleration))
  (let* ((distance-x (- *planet-x* position-x))
         (distance-y (- *planet-y* position-y))
         (angle (atan distance-y distance-x))
         (distance-squared (+ (expt distance-x 2) 
                              (expt distance-y 2)))
         (acceleration (/ *planet-mass* distance-squared)))
    (setf acceleration-x (* acceleration (cos angle))
          acceleration-y (* acceleration (sin angle)))))
```

초기 조건을 행성 근처 위성이 부서진 상황으로 바꿔 잔해 5000개를 만들면,
잔해가 행성에 끌려 고리를 이룬다.
원문은 5000개 물리 시뮬레이션이 초당 60프레임 안에 들어가고,
보일러플레이트와 하드코딩을 포함한 전체 코드가 250줄이라고 밝힌다.

## 2편 구현하기: 던전 크롤러

### 맵을 ECS로 옮기는 이유

맵은 오픈소스 편집기 Tiled로 만들고 cl-tiled 라이브러리로 읽는다.
타일셋은 Dungeon Tileset II - Extended이며,
16×16 타일이 작아서 ImageMagick으로 두 배로 키운다.

```sh
convert dungeontileset-extended.png -filter box -resize 200% dungeontileset-extended2.png
```

cl-tiled는 맵을 CLOS 객체로 돌려주는데, REPL에서 살펴보기는 좋지만 게임에서
직접 쓰면 런타임 디스패치 비용이 든다.
1280×800 창을 32×32 타일로 채우면 40×25, 즉 타일이 최소 1000개다.
저자의 `cl-tiled-demo`에서는 12코어 Ryzen 5 3600 기준으로 맵 그리기를 켜면
FPS가 20,000에서 600으로 떨어진다.
한 프레임에 1.5ms 넘게 쓰는 셈이고, 레이어 하나짜리 맵에서 나온 수치다.
그래서 cl-tiled가 읽은 타일 데이터를 ECS 저장소로 옮긴다.

### 부모, 프리팹, 파이널라이저

모든 타일과 맵 관련 객체에 `parent` 컴포넌트를 붙이고,
`entity` 슬롯에 `children`이라는 인덱스를 건다.
엔티티 삭제 훅에서 이 인덱스로 자식을 찾아 지우면,
맵 엔티티 하나를 지울 때 딸린 객체가 모두 함께 지워진다.

```lisp
(ecs:defcomponent parent
  (entity -1 :type ecs:entity :index children))

(ecs:hook-up ecs:*entity-deleting-hook*
             (lambda (entity)
               (dolist (child (children entity))
                 (ecs:delete-entity child))))
```

인덱스는 오픈 어드레싱 해시 테이블 위에 만들어져 분할 상환 O(1)로 동작한다.
대신 기본 ECS 연산만큼 캐시 친화적이지 않고,
관계형 데이터베이스의 인덱스처럼 컴포넌트를 만들고 지울 때마다 갱신 비용이 든다.

같은 타일이 맵 여러 곳에 반복되므로, 타일셋의 타일은 프리팹(prefab) 엔티티로
한 번만 만들고 맵의 타일은 프리팹의 `image`를 복사해 쓴다.
프리팹에는 `position`이 없어서 그리기 시스템이 처리하지 않는다.
복사되는 것은 8바이트 포인터 하나다.
프리팹은 Tiled의 전역 타일 ID로 찾으므로 유일 인덱스를 건다.

```lisp
(ecs:defcomponent map-tile-prefab
  (gid 0 :type fixnum :index map-tile-prefab :unique t))
```

`:unique t`가 붙은 인덱스 함수는 목록 대신 엔티티 하나를 돌려준다.
`:missing-error-p nil`을 주면 오류 대신 `-1`을 돌려주고,
`entity-valid-p`는 현재 버전에서 값이 음수가 아닌지만 본다.

liballegro 이미지는 C 쪽 자원이라 Lisp GC가 풀지 못한다.
그래서 `image` 컴포넌트에 파이널라이저를 달되,
프리팹일 때만 비트맵을 해제해 같은 포인터를 공유하는 맵 타일에서 이중 해제가
일어나지 않게 한다.

```lisp
(ecs:defcomponent (image :finalize (lambda (entity &key bitmap)            ;; modify here
                                     (when (has-map-tile-prefab-p entity)  ;;
                                       (al:destroy-bitmap bitmap))))       ;;
  (bitmap (cffi:null-pointer) :type cffi:foreign-pointer))
```

맵 타일은 프리팹을 복사하고 위치만 더해 만든다.

```lisp
(defun load-tile (entity tile x y)
  (let ((prefab (map-tile-prefab (tiled:tile-gid tile))))
    (ecs:copy-entity prefab
                     :destination entity
                     :except '(:map-tile-prefab))
    (make-position entity :x (float x)
                          :y (float y))))
```

그리기 시스템은 1편보다 단순하다.
2편은 liballegro를 따라 이미지 위치를 왼쪽 위 모서리로 본다.

```lisp
(ecs:defsystem render-images
  (:components-ro (position image)
   :initially (al:hold-bitmap-drawing t)
   :finally (al:hold-bitmap-drawing nil))
  (al:draw-bitmap image-bitmap position-x position-y 0))
```

Tiled의 레이어 순서는 그리기 순서로 이어진다.
`tiled:map-layers`가 편집기와 같은 순서로 레이어를 돌려주고,
`make-entity`는 엔티티를 증가하는 번호로 만들며,
시스템은 오래된 엔티티부터 처리하기 때문이다.

### 애니메이션

애니메이션 프레임은 프리팹에 `animation-frame` 컴포넌트로 붙이고,
`sequence` 슬롯에 `sequence-frames` 인덱스를
걸어 한 애니메이션의 프레임 목록을 바로 얻는다.
시퀀스 이름은 키워드라서 포인터 비교만으로 같은지 알 수 있다.
맵 위의 애니메이션 타일은 현재 상태를 `animation-state`에 둔다.

```lisp
(ecs:defsystem update-animations
  (:components-rw (animation-state image)
   :arguments ((dt single-float)))
  (incf animation-state-elapsed dt)
  (when (> animation-state-elapsed animation-state-duration)
    (let+ (((&values nframes rest-time) (floor animation-state-elapsed
                                               animation-state-duration))
           (sequence-frames (sequence-frames animation-state-sequence))
           ((&values &ign nframe) (truncate (+ animation-state-frame nframes)
                                            (length sequence-frames)))
           (frame (nth nframe sequence-frames)))
      (setf animation-state-elapsed rest-time
            animation-state-frame nframe
            animation-state-duration (animation-frame-duration frame)
            image-bitmap (image-bitmap frame)))))
```

`floor`로 나눈 몫 `nframes`는
렉 때문에 `dt`가 프레임 길이보다 길 때
여러 프레임을 한꺼번에 넘기기 위한 값이고,
나머지 `rest-time`은 다음 프레임에 이월된다.
`instantiate-animation`은 `elapsed`를 0과 `duration` 사이 난수로 시작해
같은 애니메이션이 맵 곳곳에서 똑같이 깜빡이지 않게 한다.

### 캐릭터와 장애물

`character` 컴포넌트는 속도와 목표 지점을 담는다.
목표의 초기값은 `float-features`의 `single-float-nan`이다.
0으로 두면 새로 만든 캐릭터가 모두 왼쪽 위 모서리로 달려가기 때문이다.

```lisp
(ecs:defcomponent character
  (speed 0.0 :type single-float)
  (target-x single-float-nan :type single-float)
  (target-y single-float-nan :type single-float))
```

플레이어 표시는 태그 컴포넌트에 `bit` 타입 슬롯
하나를 넣고 유일 인덱스를 거는 요령을 쓴다.
전역 변수 없이 `(player-entity 1)`로 플레이어를 O(1)에 찾을 수 있다.
저자는 이 조회가 메모리 참조 한두 번이 아니라 최소 여섯 번이 든다고 인정한다.

```lisp
(ecs:defcomponent player
  (player 1 :type bit :index player-entity :unique t))
```

벽을 통과하지 않게 하려면 좌표로 그 칸의 모든 객체를 찾아야 한다.
맵에 레이어가 여럿이라 한 칸에 타일이 여러 장 겹치기 때문이다.
좌표를 정수로 잘라 64비트 정수 하나에 묶는 `tile-hash`를 만들고,
이를 기본값으로 하는 인덱스 슬롯을 `position`에 더한다.

```lisp
(defun tile-hash (x y)
   (let ((x* (truncate x))
         (y* (truncate y)))
     (logior (ash x* 32) y*)))

(ecs:defcomponent position
  (x 0.0 :type single-float)
  (y 0.0 :type single-float)
  (tile-hash (tile-hash x y) :type fixnum :index tiles))  ;; here
```

```lisp
(defun tile-obstacle-p (x y)
  (loop :for entity :of-type ecs:entity :in (tiles (tile-hash x y))
        :thereis (and (has-map-tile-p entity)
                      (map-tile-obstacle entity))))
```

`control-player` 시스템은 W, A, S, D 입력으로 목표를 정하고,
이동 방향에 따라 캐릭터 사각형의 모서리가 닿는 칸이 장애물이면
목표를 현재 위치로 되돌린다.

### 편집기에서 컴포넌트 불러오기

Tiled의 사용자 정의 타입(custom type)을 컴포넌트로,
그 멤버를 슬롯으로 대응시킨다.
벽 타일에 `map-tile` 타입의 `map-tile` 속성을 달고 `obstacle`을 체크하면,
다음 함수가 이를 `((:map-tile :obstacle t))` 같은 명세로 바꾼다.

```lisp
(defun properties->spec (properties)
  (when properties
    (loop :for component :being :the :hash-key
          :using (hash-value slots) :of properties
          :when (typep slots 'hash-table)
          :collect (list* (make-keyword (string-upcase component))
                          (loop :for name :being :the :hash-key
                                :using (hash-value value) :of slots
                                :nconcing (list
                                           (make-keyword (string-upcase name))
                                           value))))))
```

같은 함수를 오브젝트 레이어에도 쓰면,
플레이어와 적을 코드 대신 편집기에서 배치할 수 있다.
`character`와 `player` 타입을 만들어 타일 오브젝트에 달면,
`load-map`이 오브젝트마다 엔티티를 만들고
`load-tile`로 프리팹 데이터를 복사한다.
저자는 이렇게 ECS로 맵 객체를 다루면 데이터 주도 프로그래밍에 가까워진다고 보고,
Mike Acton의 CppCon 2014 발표 Data-Oriented Design and C++를 권한다.

### 적과 A* 경로 찾기

적은 `enemy` 컴포넌트에 시야 거리와 공격 거리를 둔다.
공격 거리에 들어오면 즉사하는 소울라이크 규칙이라,
`*should-quit*` 전역 변수를 메인 루프가
확인하게 하고 “You died” 메시지 상자를 띄운다.

적이 벽을 통과하지 않게 하려고 저자의 cl-astar를 쓴다.
A*는 Lisp로 구현된 로봇 Shakey 프로젝트에서 나왔다는 일화도 소개한다.
경로는 점의 배열인데, 슬롯에 배열을 두면 cl-fast-ecs가
`values will be boxed; consider using separate entities instead`라고 경고한다.
그래서 경로의 점 하나하나를 엔티티로 만들고 `traveller` 인덱스로 묶는다.

```lisp
(ecs:defcomponent path-point
  (x 0.0 :type single-float)
  (y 0.0 :type single-float)
  (traveller -1 :type ecs:entity :index path-points))

(ecs:defcomponent path
  (destination-x 0.0 :type single-float)
  (destination-y 0.0 :type single-float))
```

```lisp
(ecs:defsystem follow-path
  (:components-ro (enemy path position)
   :components-rw (character))
  "Follows path previously calculated by A* algorithm."
  (if-let (first-point (first (path-points entity :count 1)))
    (with-path-point (point-x point-y) first-point
      (if (and (approx-equal position-x point-x)
               (approx-equal position-y point-y))
          (ecs:delete-entity first-point)
          (setf character-target-x point-x
                character-target-y point-y)))
    (delete-path entity)))
```

경로 찾기 함수는 cl-astar의 `define-path-finder` 매크로로 정의한다.
월드 크기, 좌표를 배열 인덱스로 바꾸는 `indexer`, 도착 판정, 8방향 이웃 열거,
장애물이면 `most-positive-single-float`를 돌려주는 정확한 비용,
옥타일 거리 휴리스틱, 찾은 경로를 엔티티로 만드는 처리 함수를 인자로 넘기면
이 문제에 맞춘 `find-path` 함수가 생성된다.
경로 점에도 `parent`를 달아, 캐릭터가 지워지면 경로 점도 함께 지워진다.

### Nuklear로 만든 인터페이스

게임 화면은 liballegro가 만든 그래픽 컨텍스트이므로 Qt나 GTK는 쓸 수 없다.
저자는 순수 C 라이브러리 Nuklear와 자신이 관리하는 cl-liballegro-nuklear를 쓰고,
그 안의 선언형 DSL로 창을 정의한다.

```lisp
(ui:defwindow narrative (&key text)
    (:x (truncate +window-width+ 4) :y (truncate +window-height+ 4)
     :w (truncate +window-width+ 2) :h (truncate +window-height+ 2))
  (ui:layout-space (:height (truncate +window-height+ 4) :format :dynamic)
    (ui:layout-space-push :x 0.05 :y 0.15 :w 0.9 :h 1.2)
    (ui:label-wrap text)
    (ui:layout-space-push :x 0.5 :y 1.4 :w 0.4 :h 0.35)
    (ui:button-label "Ok"
      t)))
```

Nuklear는 즉시 모드(immediate mode) 라이브러리라
매 프레임 모든 위젯을 다시 그리고 처리한다.
그래서 버튼 클릭을 콜백이 아니라 반환값으로 확인한다.
`ui:button-label`은 눌린 프레임에만 본문의 값 `t`를 돌려준다.

맵에 놓인 이야기 오브젝트는 `narrative` 컴포넌트로 표현하고,
`active` 슬롯에 인덱스를 걸어 열린 창이 있는지 바로 알아낸다.
창이 열려 있는 동안 이동 시스템을 멈추는 데에는 `:when` 옵션을 쓴다.

```lisp
(ecs:defcomponent narrative
  (text "" :type string)
  (shown nil :type boolean)
  (active nil :type boolean :index active-narratives))
```

```lisp
(ecs:defsystem move-characters
  (:components-rw (position character)
   :components-ro (size)
   :when (null (active-narratives t))   ;; here
   :arguments ((dt single-float)))
   ;; ...
```

승리 조건은 `narrative`와 함께 붙는 태그 컴포넌트 `win`이다.
`show-narrative` 시스템은 창을 닫을 때 `has-win-p`로 확인해 게임을 끝낸다.

## 트레이드오프

### 인덱스는 ECS 밖으로 한 발 나가는 장치다

저자가 직접 짚듯 인덱스는 ECS 패턴에 흔한 기능이 아니다.
부모와 자식, 프리팹 조회, 칸별 객체 조회, 경로 점, 열린 창 확인까지
2편의 핵심 동작은 거의 모두 인덱스에 기대고 있다.
인덱스가 없으면 이 질문들은 모두 엔티티 전체를 훑는 O(n)이 된다.

비용은 두 군데서 나온다.
해시 테이블 조회는 평평한 배열을 훑는 것만큼 캐시에 우호적이지 않고,
인덱스가 걸린 컴포넌트는 만들고 지울 때마다 인덱스를 갱신해야 한다.
`position`에 `tile-hash` 인덱스를 건 결정은 특히 무겁다.
위치는 가장 흔한 컴포넌트이고, 원문이 슬롯 기본값으로만 해시를 계산하므로
캐릭터가 움직인 뒤에도 해시가 따라 갱신되는지는 원문에 나오지 않는다.
원문의 장애물 검사는 움직이지 않는 맵 타일만
대상으로 하니 문제가 드러나지 않을 뿐이다.
이 부분은 원문이 다루지 않은 빈틈에 대한 해석이다.

### 모든 타일을 엔티티로 두는 단순함

원문은 타일 하나하나를 엔티티로 두는 방식이 유일한 정답이 아니라고 밝힌다.
많은 ECS 지지자가 이를 권하지 않으며,
정적 타일을 로딩 시점에 버퍼 하나로 그려 두고 한 번에 그리는 방법도 있다.
저자는 코드가 복잡해지고 새 문제가 생긴다는 이유로 단순한 쪽을 골랐다.

그 대가는 엔티티 수다.
40×25 레이어 하나에 1000개이고 레이어가 늘면 곱절로 늘며,
프리팹, 애니메이션 프레임, 경로 점까지 모두 엔티티다.
대신 타일이 장애물인지, 애니메이션인지 같은 속성을 다른 객체와 똑같이 컴포넌트로
다룰 수 있고, 편집기에서 단 속성이 그대로 컴포넌트가 된다.
이 균일함이 2편에서 기능을 쉽게 붙일 수 있었던 근거다.

### 배열을 엔티티로 쪼개면 순서가 암묵적 계약이 된다

경로를 엔티티로 쪼개는 것은 슬롯 배열이 상자에
담겨 캐시를 망치는 일을 피하려는 선택이다.
하지만 그러면 점의 순서는 엔티티 번호 순서에 기대게 된다.
원문은 인덱스가 엔티티를 오름차순으로
돌려주므로 생성 순서가 유지된다고 설명한다.

레이어 그리기 순서, 애니메이션 프레임 순서, 플레이어를 맵 뒤에 그리는 것도
모두 같은 가정 위에 있다.
원문의 엔티티 번호는 증가하는 순서로 만들어진다고 하지만,
지워진 엔티티 번호를 다시 쓰는지는 원문에 나오지 않는다.
경로를 다시 찾을 때마다 점을 지우고 새로 만드는 코드에서 번호가 재사용된다면
순서 가정이 깨질 수 있다.
이는 원문에서 확인하지 못한 부분이므로, 직접 쓰기 전에 cl-fast-ecs 문서에서
확인해야 할 지점이다.

### ECS가 맞는 문제와 아닌 문제

1편 HN 토론에서 raytopia는 컴포넌트 부분을 빼고 배열과 루프만 취하면 분기가
줄어 더 단순하고 빠르지 않겠냐고 물었다.[^raytopia]
meheleventyone은 ECS가 빛나는 곳은 동질적인 엔티티가 아주 많은 경우이고,
그래서 데모가 거대 도시나 수천 명의 병력,
파티클 같은 것뿐이라고 답했다.[^meheleventyone]
그는 엔티티가 이질적이면 게임플레이 코드에서 이점이 빨리 사라지고,
그래서 아키타입 같은 개념으로 메모리를 다시 짜게 된다고 덧붙였다.
creshal은 ECS가 게임 개발사에서 늦게 나온 생각이며,
한 사람이 모든 것을 추적할 수 없을 만큼 큰 게임과 범용 엔진이 생기면서 의미가
커졌다고 봤다.[^creshal]

이 지적은 두 편의 대비와 맞물린다.
1편의 소행성 5000개는 같은 컴포넌트를 가진
동질적 객체라 ECS의 성능 논리가 그대로 통한다.
2편의 던전에는 타일, 프리팹, 캐릭터, 이야기 오브젝트, 경로 점이 섞여 있고,
여기서 버티게 해 준 것은 캐시보다 인덱스와 데이터 주도 구성이었다.
2편이 증명한 것은 ECS의 성능보다 조직 방식으로서의
가치에 가깝다는 것이 이 문서의 해석이다.

## 함정

1편에서 `move` 시스템을 더하고 `dt`를 넘기지
않으면 시스템 안에서 다음 오류가 난다.
`run-systems`가 이름으로 인자를 찾아
넘기므로 누락이 컴파일 시점에 잡히지 않는다.

```text
The value
  NIL
is not of type
  NUMBER
   [Condition of type TYPE-ERROR]
```

시스템은 자신이 받는 컴포넌트를 가진 모든 엔티티를 처리한다.
1편에서 `crash-asteroids`를 처음 정의하면 행성도 `position`을 가지므로
첫 실행에서 행성이 지워진다.
태그 컴포넌트와 `:components-no`가 필요한 이유다.

Tiled에서 애니메이션 첫 프레임에 `sequence` 문자열 속성을 빠뜨리면 애니메이션이
`NIL`이라는 이름으로 로드되고,
`The value NIL is not of type FIXNUM` 같은 오류가 난다.
속성 이름과 컴포넌트 이름이 같아야 한다는 규칙도 같은 성격의 함정이다.

메인 Quicklisp 저장소의 cl-fast-ecs는 오래되어
`copy-entity`나 `spec-adjoin`이 없을 수 있다.
그때는 Lucky Lambda 저장소의 최신판을 써야 한다.

1편 시점의 liballegro는 macOS에서 16비트 색 PNG를 잘못 표시하는 버그가 있어,
Homebrew로 ImageMagick을 설치하고 이미지를 8비트로 바꿔야 했다.

```bash
mogrify -depth 8 *.png
```

Tiled는 타일의 좌표는 왼쪽 위 모서리로,
오브젝트의 좌표는 왼쪽 아래 모서리로 저장한다.
그래서 오브젝트를 읽을 때 높이만큼 `y`를 빼야 하고,
장애물로 쓸 오브젝트는 X와 Y를 직접 입력해 격자에 맞춰야 한다.

저자는 2편의 장애물 검사가 완벽하지 않다고 스스로 밝힌다.
위치를 왼쪽 위 모서리로 잡은 탓에 `control-player`의 조건이 커졌고,
다른 캐릭터의 행동을 구현할 때 사소한 이상이 생긴다.
캐릭터 칸의 중심을 위치로 쓰면 수학이 단순해지지만,
`load-map`을 고치고 캐릭터용 그리기 시스템을 따로 둬야 한다.

환경 준비의 무게도 함정이다.
2편 HN 토론에서 xixixao는 튜토리얼은 훌륭하지만 1편의 준비 과정이
Common Lisp, Python, C로 이어지는 여러 단계라는 점이 CL이 젊은 프로그래머에게
인기가 없는 이유를 보여준다고 했다.[^xixixao]
wwfn은 그 단계 과다 문제의 일부를 겨냥한 시도로 CIEL을 소개했다.[^wwfn]
실제로 1편은 SBCL, Quicklisp, LuckyLambda 저장소, IDE 확장, Python cookiecutter,
liballegro, C 툴체인, `libffi`를 모두 요구한다.

## 확인하기

매크로가 무엇을 만드는지는 `macroexpand`로 본다.
출력이 대문자인 것은 기본 `readtable-case` 설정 때문이다.

```lisp
(macroexpand
 '(ecs:define-component position
   "Determines the location of the object, in pixels."
   (x 0.0 :type single-float :documentation "X coordinate")
   (y 0.0 :type single-float :documentation "Y coordinate")))
```

시스템이 어떤 기계어로 컴파일됐는지는 `disassemble`로 본다.
원문은 템플릿의 `package.sh`가 만든 릴리스 빌드에서 `move` 시스템이 외부 함수
호출 없이 210바이트이고, 엔티티를 처리하는 루프 본문이 명령어 17개라고 보고한다.

```lisp
(disassemble (ecs:system-ref :move))
```

로드된 엔티티의 내용은 실행 중인 REPL에서 `print-entity`로 확인한다.
2편은 ID 65인 벽 타일의 프리팹을 다음처럼 조회해,
`map-tile` 컴포넌트의 `obstacle`이 `T`로 들어왔는지 확인한다.

```lisp
(ecs:print-entity (ecs-tutorial-2::map-tile-prefab (1+ 65)))
```

이 모든 확인은 프로그램을 끄지 않고 할 수 있다.
1편은 `crash-asteroids`를 REPL에 보내는 즉시 실행 중인 시뮬레이션의 동작이
바뀌는 것을 보여주고, 2편은 창을 띄운 채 `narrative` 함수를 다시 정의하며
레이아웃을 맞추는 방법을 권한다.
템플릿에 포함된 livesupport 라이브러리 덕분에 Lisp가 입력을 기다릴 때만이 아니라
실행 중 어느 때든 코드를 바꿀 수 있다.

## 기억할 원칙

### 문제에 맞춘 언어는 성능과 표현력을 함께 가져온다

cl-fast-ecs와 cl-astar는 같은 설계를 공유한다.
범용 함수에 인자를 넘기는 대신, 매크로가 문제의 제약에 맞춘 코드를 생성한다.
cl-astar HN 토론에서 whartung은 핵심 알고리즘이 함수가 아니라 매크로라서,
범용 알고리즘이 아니라 정의한 제약에 딱 맞는 구현이 나오고,
컴파일러가 최적화할 여지가 커진다고 짚었다.[^whartung]
같은 매크로가 최적화된 Common Lisp 코드에 따라붙는
타입 선언 같은 잡음도 감춘다고 덧붙였다.
1편의 210바이트 `move` 시스템이 이 원칙의 결과물이다.

다만 성능 주장은 비교 대상을 확인하며 읽어야 한다.
같은 토론에서 1xtrm0은 cl-astar가 앞선다고 비교한 C++ 구현이
Stack Overflow 답변 두 개이고,
하나는 휴리스틱 없는 비효율적 BFS라서 대표성이 없다고 지적했다.[^1xtrm0]
튜토리얼의 수치도 마찬가지다.
5000개가 60FPS에 들어간다는 것과 210바이트
기계어는 구조가 효율적이라는 근거이지,
다른 언어나 엔진과 비교한 측정은 아니다.

메타언어 추상화가 Lisp만의 것이라는 주장도 조금 걸러 들을 만하다.
1편 HN 토론에서 lebuffon은 Lisp만 DSL을 언어 핵심에 통합했다는 문장에,
킬로바이트 메모리 시절 Forth가 이미 DSL로 게임을 만들었다고 반박했다.[^lebuffon]
Lobste.rs에서 sjamaan은 Lisp 기반 게임의 예로 Naughty Dog의 Jak and Daxter와
Crash Bandicoot을 들었다.[^sjamaan]
edoput은 이 구조가 CLOS와 통합되기를 바란다고 했는데,[^edoput]
2편이 성능을 위해 cl-tiled의 CLOS 객체를 ECS로 옮겼다는 점을 생각하면
둘 사이의 긴장은 아직 풀리지 않은 문제다.

### 게임 상태를 실행 중에 고칠 수 있으면 개발 루프가 바뀐다

두 편 내내 반복되는 지시는 수정한 폼을
실행 중인 Lisp 프로세스에 보내라는 것이다.
2편은 전체 시스템을 다시 로드하는 것보다
몇 개 함수와 컴포넌트 정의를 보내는 것이
훨씬 빠르고, 변경에서 결과까지의 짧은 루프가 게임 개발에서 매우 중요하다고 쓴다.
새 라이브러리를 의존성에 추가할 때처럼 전체 재로드를 피할 수 없는 경우만 예외다.

ECS는 이 방식과 잘 맞는다.
상태는 저장소의 배열에 있고 동작은 이름 붙은 시스템에 있으므로,
시스템 하나를 다시 정의해도 상태는 그대로 남는다.
`player` 컴포넌트를 다른 캐릭터로 옮겨 조작 대상을 바꿀 수 있다는 2편의 예도
같은 성질에서 나온다.

2편 HN 토론에서 maxwelljoslyn은
이 글을 모든 기술 튜토리얼이 따라야 할 모범이라고 평가했다.[^maxwelljoslyn]
1편을 읽지 않고,
몇 년 전 몇 달 써 본 Common Lisp 경험만으로도 따라갈 수 있었다는 것이다.
반면 1편 토론의 timwaagh는 게임 개발 입문이라면 디자인 패턴 논의보다
화면에 무언가를 그리는 법부터 나와야 한다고 불평했다.[^timwaagh]
두 반응의 차이는 이 연재가 게임 만들기 입문이라기보다,
게임을 소재로 언어를 설계하는 방식을 가르치는 글이라는 점을 보여준다.

---

[^raytopia]: <https://news.ycombinator.com/item?id=39574726>

[^meheleventyone]: <https://news.ycombinator.com/item?id=39575058>

[^creshal]: <https://news.ycombinator.com/item?id=39581023>

[^xixixao]: <https://news.ycombinator.com/item?id=41872897>

[^wwfn]: <https://news.ycombinator.com/item?id=41874142>

[^whartung]: <https://news.ycombinator.com/item?id=41147470>

[^1xtrm0]: <https://news.ycombinator.com/item?id=41146546>

[^lebuffon]: <https://news.ycombinator.com/item?id=39580730>

[^sjamaan]: <https://lobste.rs/s/3wbr9z/gamedev_lisp_part_1_ecs_metalinguistic#c_svlgor>

[^edoput]: <https://lobste.rs/s/3wbr9z/gamedev_lisp_part_1_ecs_metalinguistic#c_ym77p5>

[^maxwelljoslyn]: <https://news.ycombinator.com/item?id=41872271>

[^timwaagh]: <https://news.ycombinator.com/item?id=39581063>
