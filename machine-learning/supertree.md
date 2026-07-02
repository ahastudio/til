# supertree - 인터랙티브 결정 트리 시각화

<https://github.com/mljar/supertree>

HN 토론: <https://news.ycombinator.com/item?id=41369231> (70점, 17개 댓글)

## 소개

`supertree`는 Jupyter, JupyterLab, Google Colab 안에서 결정 트리(Decision Tree)를
인터랙티브하게 시각화하는 Python 패키지다.
MLJAR Sp. z o.o.가 Apache 2.0 라이선스로 공개했으며, 610개 이상의 스타를 받았다.

노트북 안에서 트리를 확대·축소하고, 노드를 접고 펼치고,
특정 샘플이 트리를 통과하는 경로를 추적할 수 있다.
scikit-learn, XGBoost, LightGBM, ONNX로 학습한 모델을 모두 지원한다.

## 사용법

설치는 `pip install supertree` 한 줄로 끝난다.
사용법은 모델을 학습한 뒤 `SuperTree` 객체를 만들고 `show_tree()`를 호출하는 것이 전부다.

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from supertree import SuperTree

iris = load_iris()
model = DecisionTreeClassifier(max_depth=3)
model.fit(iris.data, iris.target)

super_tree = SuperTree(model, iris.data, iris.target, iris.feature_names, iris.target_names)
super_tree.show_tree()
```

랜덤 포레스트나 그래디언트 부스팅처럼 트리 앙상블을 사용하는 모델도 동일한 API로 다룬다.
`show_tree(2)`처럼 인덱스를 넘기면 앙상블 안의 특정 트리를 선택해서 볼 수 있다.

```python
from sklearn.ensemble import RandomForestRegressor
from supertree import SuperTree

model = RandomForestRegressor(n_estimators=100, max_depth=3, random_state=42)
model.fit(X, y)

super_tree = SuperTree(model, X, y)
super_tree.show_tree(2)
```

## 지원 라이브러리

scikit-learn, LightGBM, XGBoost, ONNX 네 개 라이브러리를 지원한다.
scikit-learn 쪽은 `DecisionTreeClassifier`, `RandomForestClassifier`,
`GradientBoostingClassifier`를 비롯한 분류·회귀 트리 계열 클래스를 폭넓게 다루고,
LightGBM과 XGBoost는 각각 `LGBMClassifier`/`LGBMRegressor`/`Booster`,
`XGBClassifier`/`XGBRegressor`/`XGBRFClassifier`/`XGBRFRegressor`/`Booster`를 지원한다.

내부적으로 `SuperTree.__init__`은 전달받은 모델의 클래스 이름을
사전에 정의된 `valid_model_classes` 목록과 대조해 즉시 검증한다.
목록에 없는 클래스면 `TypeError`를 던지고, 학습되지 않은 모델도 같은 방식으로 걸러낸다.

## 분석

### 검증 로직이 지원 범위의 실제 경계를 규정한다

README는 “지원 라이브러리”를 산문으로 나열하지만,
실제 지원 여부를 결정하는 것은 `model_loader.py`가 아니라
`supertree.py`의 `valid_model_classes` 리스트다.
이 리스트에 클래스 이름이 문자열로 하드코딩되어 있고,
`model.__class__.__name__`이 이 목록에 없으면 그 자리에서 예외가 발생한다.

이 구조는 “지원”이라는 말의 의미를 상당히 좁게 만든다.
스스로 서브클래싱한 커스텀 트리 모델이나,
scikit-learn API를 흉내 내는 서드파티 구현체는
동일한 인터페이스를 제공하더라도 클래스 이름이 다르면 즉시 거부당한다.
즉 이 라이브러리의 호환성은 인터페이스 기반이 아니라 이름 기반이다.
이는 사용이 간편해지는 대신, 생태계가 조금만 벗어나도 확장이 막히는 대가를 치른다.

### 노트북에 HTML을 직접 주입하는 방식은 시각화 라이브러리의 오래된 타협이다

`_render_tree_html`은 D3.js 기반 HTML을 문자열로 조립한 뒤
IPython의 `display(HTML(...))`을 통해 노트북 출력 셀에 직접 밀어 넣는다.
트리 구조는 파이썬에서 JSON으로 직렬화되어 `combined_data_str`로 HTML 안에 삽입되고,
`supertree.min.js`가 그 데이터를 읽어 D3 시각화를 그린다.

이 방식은 matplotlib이 정적 이미지를 그리는 것과 근본적으로 다른 선택이다.
Python 커널과 브라우저 렌더링 엔진(D3.js) 사이의 경계를 HTML 문자열 주입으로 넘나든다.
Jupyter 위젯 생태계에서 이 패턴은 드물지 않다.
Plotly, Bokeh 같은 인터랙티브 시각화 라이브러리들도 유사한 방식을 쓴다.
`supertree`가 `ipywidgets`를 선택적으로 지원하는 `widgets=True` 옵션을 별도로 둔 것은,
정적 HTML 주입만으로는 상태 유지(트리 인덱스 전환 등)가 어렵다는 한계를 인식한 결과로 보인다.

### 트리별 시각화 전용 라이브러리라는 좁은 포지셔닝이 강점이 된다

`supertree`는 범용 ML 시각화 도구가 아니라 결정 트리라는 단일 자료구조에 집중한다.
`treedata.py`, `node.py` 같은 파일 이름에서 드러나듯, 내부 설계도 트리 순회와
샘플 경로 추적이라는 단일 목적에 맞춰져 있다.

이 좁은 포지셔닝은 범용 도구 대비 뚜렷한 이점을 만든다.
scikit-learn의 `plot_tree`나 `export_graphviz`는 정적 이미지만 제공하고,
트리가 깊어지면 가독성이 급격히 떨어진다.
`supertree`는 확대·축소와 노드 접기·펼치기로 이 문제를 정면으로 해결한다.
동시에 트리 시각화 하나에만 집중했기 때문에, 4개 라이브러리·10여 개 모델 클래스라는
비교적 좁은 지원 범위를 유지하면서도 완성도를 높일 수 있었다.

## 비평

### “지원”의 기준이 API 호환성이 아니라 클래스 이름 일치다

README의 “Supported Libraries” 절은 사용자에게 광범위한 호환성을 암시한다.
그러나 실제 구현은 `model.__class__.__name__ not in valid_model_classes`라는
문자열 비교 한 줄로 지원 여부를 결정한다.
이는 scikit-learn API 규약을 따르는 모델이라도 클래스 이름이 다르면 지원 대상에서 제외됨을 뜻한다.

예를 들어 imbalanced-learn의 `BalancedRandomForestClassifier`나
scikit-learn 호환 트리 기반 모델을 감싼 래퍼 클래스들은
내부적으로 동일한 트리 구조(`tree_` 속성 등)를 노출하더라도
클래스 이름이 목록에 없으면 곧바로 `TypeError`를 만난다.
README에는 이 제약이 명시되어 있지 않고, “지원하지 않는 모델이 있으면 알려달라”는
안내 문구만 있다.
이는 사용자가 실제로 오류를 마주치기 전까지 지원 범위의 실체를 알 수 없다는 뜻이다.

### `ModelLoader`의 존재는 라이브러리가 자신의 한계를 알고 있다는 증거다

`model_loader.py`의 `ModelLoader` 클래스는 `index`, `feature`, `impurity`, `threshold`,
`class_distribution`, `predicted_class`, `samples`, `is_leaf`,
`left_child_index`, `right_child_index`라는 정해진 키를 가진 딕셔너리 리스트를 받아
트리 구조를 수동으로 구성할 수 있게 해준다.

이 클래스가 존재한다는 사실 자체가, 4개 라이브러리 지원만으로는
실제 사용자들의 요구를 충족하지 못한다는 것을 라이브러리 저자들이 이미 알고 있다는 뜻이다.
그러나 README의 “Articles” 섹션과 “Quick Start” 절 어디에도
`ModelLoader`의 사용법이나 존재 자체가 언급되지 않는다.
탈출구는 마련해 두었지만 문서화는 하지 않은 셈이며,
이는 지원되지 않는 모델을 만난 사용자가 스스로 소스 코드를 뒤지기 전까지
이 우회로를 발견할 수 없다는 뜻이다.

이 문서화 공백은 `ModelLoader`에 국한되지 않는다.
Show HN 스레드에서도 한 사용자가 왼쪽·오른쪽 분기 결과에
`target1`과 `target2`가 같은 원 안에 함께 표시되는 이유를 묻는 질문을 남겼고[^kirvyteo],
메인테이너는 명확한 답변 대신 "문서를 작업 중"이라며 이슈를 새로 등록해 달라고 답했다.
2024년 당시 이미 제기된 문서 부족 문제가, 지금 확인한 README에서도
`ModelLoader`처럼 여전히 설명되지 않은 채 남아 있는 셈이다.

### 지금의 Apache 2.0 라이선스는 상업용 라이선스 논쟁 끝에 도달한 결과다

현재 저장소의 `LICENSE.txt`는 Apache 2.0 전문을 담고 있지만,
2024년 8월 Show HN 게시 당시에는 사정이 달랐다.
당시 저장소에는 `supertree-commercial-license.pdf`라는 별도 파일이 함께 있었고,
한 댓글 작성자는 이를 두고 "무료 오픈소스 라이브러리라더니 결국 돈을 내야 하는 것 아니냐"고
지적했다[^pajeets].
이에 대해 다른 사용자는 저장소의 README가 애초에 이 프로젝트를
"상업용 소프트웨어"라고 명시하고 있었다며,
개인 용도는 무료이고 상업적 사용에만 별도 라이선스를 요구하는 구조 자체는
지속 가능한 오픈소스 자금 조달 전략으로서 합리적이라고 반박했다[^zahlman].

메인테이너는 직접 댓글을 달아 이 라이선스 정책의 배경을 설명했다.
이전에 MIT 라이선스로 공개한 AutoML 패키지(`mljar-supervised`)가
수익화하기 매우 어려웠고, 패키지를 계속 유지·개발하려면 자금이 필요하다는 것이었다[^pplonski86].
당시 상업용 라이선스 가격은 연 499달러로 책정되어 있었으나,
다른 사용자는 라이선스 문서에 적힌 가격 안내 URL이 404 오류를 반환하고
회사 웹사이트에도 `supertree`가 정식 제품으로 등록되어 있지 않다는 점을 지적했다[^zahlman2].

지금 시점에서 저장소를 확인하면 이 상업용 라이선스 파일은 더 이상 존재하지 않고,
Apache 2.0 라이선스 하나로 통일되어 있다.
즉 이 프로젝트는 출시 직후 이중 라이선스 모델을 시도했다가,
가격 체계를 제대로 정착시키지 못한 채 완전한 오픈소스 라이선스로 선회한 것으로 보인다.
README나 CHANGELOG 어디에도 이 전환 과정에 대한 설명은 없다.

### 버전 1.0.0이 의미하는 안정성 약속과 실제 API 표면의 크기가 어긋난다

`pyproject.toml`은 버전을 `1.0.0`으로 명시하고 있다.
시맨틱 버저닝 관례에서 메이저 버전 1.0은 통상 API 안정성에 대한 약속을 뜻한다.
그러나 `show_tree`와 `save_html` 두 메서드만 보아도
`which_tree`, `which_iteration`, `start_depth`, `max_samples`, `show_sample`, `widgets`라는
6개의 선택적 파라미터가 얽혀 있고, 각 파라미터의 타입과 범위를 개별적으로 검증하는
방어적 코드가 반복된다.

이런 구조는 API가 이미 여러 차례의 요구사항 추가를 거치며 확장되어 왔음을 시사한다.
1.0이라는 버전 번호가 붙었다면, 이 파라미터 조합이 이후로도 유지된다는 뜻인지,
아니면 여전히 실험적으로 계속 변경될 여지가 있는지 README만으로는 판단할 수 없다.
CHANGELOG나 버저닝 정책에 대한 언급이 없다는 점은,
프로덕션 파이프라인에 이 라이브러리를 고정 버전으로 들여오려는 사용자에게
불확실성을 남긴다.

## 인사이트

### 이름 기반 검증은 생태계가 확장될 때 유지보수 부채로 되돌아온다

`valid_model_classes`라는 하드코딩된 문자열 리스트로 지원 모델을 판별하는 방식은
지금 당장은 단순하고 명확하지만, ML 생태계가 계속 새로운 모델 클래스를 만들어내는 한
이 리스트는 계속 늘어나야 하는 운명에 처한다.
CatBoost, 새로운 버전의 XGBoost가 추가하는 클래스, PyTorch 기반 트리 부스팅 라이브러리 등이
등장할 때마다 유지보수자는 이 목록에 이름을 추가하는 PR을 반복해서 받아야 한다.

이 패턴은 소프트웨어 역사에서 낯설지 않다.
초기 웹 브라우저들이 `User-Agent` 문자열로 브라우저를 식별하려다
브라우저 종류가 늘어날수록 문자열 매칭 로직이 기하급수적으로 복잡해진 사례와 구조적으로 닮았다.
결국 웹 생태계는 기능 감지(feature detection)로 전환했다.
`supertree`도 장기적으로는 `model.__class__.__name__` 비교 대신
`tree_` 속성이나 `predict` 메서드 존재 여부 같은 덕 타이핑(duck typing) 방식으로
전환해야 확장성 문제에서 자유로워질 것이다.
현재 구조를 그대로 유지한다면, 지원 모델이 늘어날수록
“이 모델이 왜 안 되지?”라는 이슈가 유지보수자에게 반복해서 쌓이는 구조적 부채가 예약되어 있다.

### 노트북 중심 시각화 도구의 성공은 배포 환경의 파편화라는 대가를 수반한다

`supertree`가 HTML을 직접 노트북 셀에 주입하는 방식으로 동작한다는 것은,
이 도구의 가치가 온전히 Jupyter 계열 실행 환경에 묶여 있음을 뜻한다.
Colab, JupyterLab, 클래식 Jupyter에서는 잘 동작하지만,
VS Code의 노트북 확장, 정적 사이트로 변환된 노트북(nbconvert),
또는 완전히 다른 실행 환경(스크립트, 파이프라인 로그)에서는
동일한 인터랙티브 경험을 보장할 수 없다.
`save_html`이라는 별도 메서드가 존재하는 이유도 결국 이 파편화 문제에 대한 대응책이다.

이는 인터랙티브 시각화 라이브러리 전반이 마주하는 근본적인 트레이드오프를 드러낸다.
정적 이미지(matplotlib, `export_graphviz`)는 어디서나 동일하게 보이지만 상호작용이 없고,
인터랙티브 HTML/JS 기반 도구는 풍부한 경험을 제공하지만 실행 환경에 종속된다.
데이터 과학 팀이 시각화 도구를 선택할 때, 이 트레이드오프는 종종
“데모에서는 근사하지만 프로덕션 리포트에는 못 쓴다”는 형태의 불만으로 되돌아온다.
`supertree`의 설계는 전자를 포기하고 후자의 몰입감을 선택한 것이며,
이 선택이 어떤 조직에는 맞고 어떤 조직에는 맞지 않을지는 최종 산출물이
누구에게 어떤 형태로 전달되어야 하는지에 달려 있다.

### 좁은 도메인에 집중한 시각화 도구가 범용 프레임워크의 부속 기능보다 오래 살아남는 경우가 많다

scikit-learn 같은 범용 ML 프레임워크도 `plot_tree`라는 자체 트리 시각화 기능을 제공한다.
그럼에도 `supertree` 같은 독립 프로젝트가 610개의 스타를 모으며 존재한다는 사실은,
범용 프레임워크에 곁다리로 붙은 기능과 하나의 목적에 집중한 독립 도구 사이의
품질 격차를 보여주는 사례다.

범용 프레임워크의 부속 기능은 언제나 우선순위에서 밀린다.
scikit-learn 메인테이너 입장에서 `plot_tree`의 확대·축소, 노드 접기 기능을 정교하게 다듬는 일은
전체 프로젝트의 자원 배분에서 상대적으로 낮은 우선순위를 차지할 수밖에 없다.
반면 `supertree`처럼 시각화 하나만 파는 프로젝트는 그 기능 자체가 존재 이유이므로
개선 속도와 완성도에서 이점을 가진다.

이 구조는 이미 커뮤니티에서 반복적으로 검증된 패턴이다.
Plotly, Altair, Seaborn 모두 범용 시각화 라이브러리(matplotlib)의 한계를 딛고
특정 사용 사례에 집중해 성장했다.
`supertree`는 이 패턴을 “결정 트리 시각화”라는 더 좁은 틈새에 적용한 사례이며,
ML 툴체인에서 앞으로도 “프레임워크에 곁들여진 기능” 대신
“단일 문제에 집중한 독립 도구”가 계속 등장할 가능성을 시사한다.

---

[^pajeets]: <https://news.ycombinator.com/item?id=41410802>
[^zahlman]: <https://news.ycombinator.com/item?id=41410895>
[^pplonski86]: <https://news.ycombinator.com/item?id=41411056>
[^zahlman2]: <https://news.ycombinator.com/item?id=41410953>
[^kirvyteo]: <https://news.ycombinator.com/item?id=41442877>
