# 렌즈 없이 한 장으로 두 곳을 가리키는 QR 코드

원문: [Got me thinking… can it be done without the lens? This one seems to work!](https://mstdn.social/@isziaui/113874436953157913)

## 요약

2025년 1월 22일, Guy Dupont(`gvy_dvpont`)이 “같은 이야기에 대한 서로 다른 관점”이라는 발상을 갖고 놀아 봤다며 각도에 따라 다른 곳으로 보내는 QR 코드를 올렸다.
렌티큘러 렌즈 뒤에 세 개의 QR 코드를 두어 한 번에 하나씩만 보이게 만든 물건이었고, 손에 들고 살짝 기울이면 카메라 앱이 인식하는 코드가 바뀐다.

같은 날 밤, Christian Walther(`isziaui`)가 답글을 달았다.
생각하게 만들었다며, 렌즈 없이도 되지 않을까 하고 시도해 봤더니 이건 되는 것 같다는 짧은 문장과 함께 이미지 하나를 붙였다.
이미지 설명은 이렇게 적혀 있다.
“판독기가 무작위로 둘 중 하나를 잡도록 겹쳐 놓은 두 개의 QR 코드.”
평면 인쇄물 한 장이 `mstdn.social/@isziaui`와 `github.com/cwalther` 두 URL을 모두 담고 있다.

원리는 본인이 바로 이어서 설명했다.
각 픽셀의 절반은 한 코드에서, 나머지 절반은 다른 코드에서 온다.
판독기는 정렬 블록을 기준으로 픽셀이 있을 것으로 예상되는 위치의 중심에서 표본을 뜬다고 가정했고, 그래서 중요한 것은 모든 픽셀에 같은 마스크를 쓰는 것과 픽셀의 중심이 그 마스크의 경계 위에 놓이게 하는 것이다.
그러면 이미지가 조금만 움직여도 모든 표본이 한쪽 절반이나 다른 쪽 절반으로 함께 쏠린다.
세로줄이나 대각선 줄무늬보다 체커보드 마스크가 결과가 좋았고 오류 정정 수준은 가장 높은 H를 썼으며, 실험이 더 필요하다는 단서를 달았다.

반응은 즉각적이었다.
Dupont은 잠깐 걸렸지만 두 개를 다 잡았다며 깃허브와 마스토돈이냐고 물었고, 자기가 만든 것보다 40배는 멋지다고 했다.
Walther는 그저 상대가 자신을 낚아 끌어들인 한밤중의 빠른 실험일 뿐이라고 답했다.
이틀 뒤 Hackaday에 기사가 실렸고 Hacker News 1위에 올랐으며, 이후 1년 반 동안 같은 스레드에서 실험이 계속 이어졌다.

## 분석

### 규격의 구멍이 아니라 판독기 구현의 자유도를 노린 트릭이다

ISO/IEC 18004는 인코딩을 완전히 규정하지만, 카메라 이미지에서 모듈 격자를 어떻게 찾아 어느 지점에서 표본을 뜰지는 규정하지 않는다.
정렬 패턴과 타이밍 패턴을 어떻게 활용해 격자를 세우고 각 칸의 명암을 어떻게 판정할지는 구현자의 몫이다.
이 트릭이 겨냥한 것이 정확히 그 여백이다.

그래서 이 코드는 규격 위반이 아니다.
어느 각도에서 읽든 나오는 것은 완전히 유효한 QR 코드이며 체크섬도 통과한다.
`blueflow`가 짚었듯 체크섬은 같은 비트열 안에 들어 있으므로 데이터와 함께 통째로 바뀐다.[^blueflow]
두 개의 정답이 있는 상태이지 정답과 오답이 있는 상태가 아니다.

HN에서 `layer8`이 이 성질을 가장 정확하게 서술했다.
판독기는 대체로 카메라 이미지 위에 점 격자를 얹고 값을 표본화하는 방식으로 동작하는데, QR 사각형이 균일하지 않으면 카메라를 조금만 움직여도 그 사각형의 표본값이 달라진다.
사람이 카메라를 100% 고정할 수 없다는 사실과 센서 잡음까지 더해져 비트값은 계속 흔들리지만, 판독기는 QR 체크섬 검증을 통과하는 순간 만족하고 멈춘다.
비트 패턴을 뽑아내는 이미지 인식은 본질적으로 발견적이며, 인식이 성공했는지를 판정하는 것은 오직 체크섬뿐이라는 것이다.[^layer8-mech]
`hammock`은 이 설명을 듣고 자기가 생각했던 것보다 훨씬 비결정적이라고 반응했다.[^hammock]

### 오류 정정 여유를 모호성 예산으로 바꿔 쓴다

오류 정정 수준 H를 고른 것은 장식이 아니다.
두 코드가 다른 값을 갖는 모듈의 개수가 곧 한쪽 코드 입장에서의 오류 개수이므로, 정정 여유가 클수록 표본이 잘못 쏠려도 복구된다.
Walther가 나중에 `hacknorris`에게 되물은 문장이 이 구조를 드러낸다.
그 코드들이 유효한 코드인지 아니면 오류 정정에 의존하고 있는지 물으면서, 모호성이 오류 정정 여유를 갉아먹을 것이므로 오류를 더하는 것은 무엇이든 인식을 어렵게 만들 것 같다고 했다.[^isziaui-ecc]

여기서 한 가지 최적화 방향이 나온다.
두 코드가 다른 모듈의 수를 줄이면 여유를 덜 쓴다.
`xssfox`는 같은 생각을 하면서 근사 충돌을 찾아 서로 다른 비트 수를 줄이는 쪽을 노렸고, 30비트 차이를 무차별 대입으로 찾는 것은 꽤 쉬워 보인다고 했다.[^xssfox-collision]
Walther는 그것이 자기 할 일 목록에도 있다고 답했다.[^isziaui-todo]

며칠 뒤 Walther는 실험 결과를 표로 내놓았다.
두 URL에 대해 8개의 XOR 마스크를 각각 적용한 조합 8×8의 차이 개수를 모두 계산했더니, 두 코드에 같은 마스크를 쓸 때 차이가 가장 적었다.
두 URL이 충분히 비슷했기 때문이며, 원래 개념 증명에서도 생성기가 양쪽에 자동으로 마스크 6번을 골라 이미 그렇게 되어 있었으므로 이번에는 얻은 것이 없었다는 결론이다.
표 설명에는 대각선 위의 것들이 서로 다른 픽셀 수가 가장 적고, 두 개의 같은 마스크가 서로 상쇄되어 결과적으로 마스크를 벗긴 두 코드의 XOR이 되기 때문에 그것들이 모두 동일하다고 적혀 있다.[^isziaui-mask]

`xssfox`의 답이 더 실용적이었다.
같은 접두사를 쓰는 자기 방식에서는 접두사가 데이터의 큰 부분을 차지하므로 마스킹 패턴을 바꾸면 언제나 다른 비트가 더 많아질 뿐 도움이 될 수 없다는 것을 확인했고, 더 유용한 것은 체크섬이 거의 같아지도록 접미사를 무차별 대입하는 일이라고 했다.[^xssfox-prefix]
Walther는 공통 접두사가 아마 어차피 더 유용할 것이라면서, 자신이 굳이 다른 도메인을 고른 이유는 iOS 카메라 앱이 실시간 미리보기에서 도메인만 보여 주고 전체 내용을 보려면 한 번 눌러야 하기 때문이라고 밝혔다.[^isziaui-domain]

### 스레드 자체가 공개된 연구 노트가 되었다

이 실험에 논문도 저장소도 없다.
있는 것은 답글 사슬 하나뿐인데, 그 안에서 가설 제시, 반례 보고, 대안 구현, 정량 실험, 결과 부정이 모두 일어난다.
`xssfox`는 며칠 사이에 디더링 방식 버전을 만들어 올렸고 한쪽 코드에 확실히 치우치기는 하지만 각도를 조절해 둘 다 읽게 할 수 있었다고 보고했으며, Walther는 고르지 않은 크기 조정에도 불구하고 아주 잘 된다고 답했다.[^xssfox-dither][^isziaui-dither]

기여자들의 배경이 제각각이라는 점도 눈에 띈다.
`nemothorx`는 12년 전 자신이 했던 색 채널 기반 다중 QR 실험을 꺼내 왔다.
숫자 42를 “6x9”, “XLII”, “Forty-two” 세 가지로 표현한 QR 코드를 각각 RGB 채널에 넣어 합친 것인데, 자기 휴대폰은 QR 코드라는 것은 어렵지 않게 알아보지만 언제나 XLII 판본만 골라낸다고 했다.[^nemothorx]
Walther의 아이폰은 그것을 전혀 인식하지 못했고, 오른쪽 아래 정렬 점이 모든 채널에서 같아야 하지 않느냐는 지적으로 이어졌다.
`nemothorx`는 버전 1 코드라 21×21이고 오른쪽 아래 정렬 구획이 아예 없다고 답했으며[^nemothorx-v1], 결국 알파 채널에 네 번째 코드가 있다는 사실이 드러나면서 그것을 무시하니 인식된다는 결론이 났다.[^isziaui-alpha]
빨강은 “6x9”, 초록은 “XLII”, 파랑은 “Forty-two”, 알파는 “㊷”였고, 작성자 본인도 최종 이미지에서 어느 하나라도 판독 가능하다는 사실은 처음 알았다고 했다.[^nemothorx-alpha]

`vikxin`은 거리에 따라 다르게 읽히는 코드를 제안했다.
가까이서는 고주파 정보가 한 코드로 읽히고 멀어지면 저주파 정보로 대체되게 하는 방식으로, 대학 시절 QR 코드는 아니지만 비슷한 것을 해 봤다고 했다.[^vikxin]
`bornach`는 CMOS 센서를 미세한 디더 패턴에 겨눌 때 생기는 무아레를 이용하거나, 초점이 나갔을 때 혹은 어두운 곳에서 셔터 속도가 길어져 손떨림으로 흐려졌을 때 다른 코드가 보이게 하는 공간 주파수 활용을 제시하며 아인슈타인-먼로 착시를 예로 들었다.[^bornach]

## 비평

### 메커니즘 설명은 저자 본인이 추측이라고 밝힌 가설이다

이 코드가 왜 작동하는지에 대한 설명은 널리 인용되지만, 출처는 검증된 분석이 아니다.
`axoaxonic`이 이것을 네커 큐브나 두 얼굴과 꽃병 같은 양안정 지각(multistable perception)의 컴퓨터 비전판으로 보인다고 하자, Walther는 직접 선을 그었다.
표본 지점 이야기는 자기 추측일 뿐이며 판독기들이 실제로 어떻게 하는지 연구해 본 적이 없다는 것이다.[^isziaui-conjecture]

이 단서는 중요하다.
정렬 블록 기준으로 픽셀 중심에서 표본을 뜬다는 모형이 맞다면 체커보드가 최적이어야 할 이유가 설명되지만, 실제 판독기 다수는 단일 지점 표본이 아니라 이진화된 이미지에서 영역 평균이나 다른 휴리스틱을 쓴다.
`dascandy`가 가운데 9분의 1을 한 코드로, 둘러싼 9분의 8을 다른 코드로 채우면 중심 픽셀 값을 쓰느냐 사각형 평균을 쓰느냐에 따라 확실히 한쪽이 나올 것이라고 제안한 것은 바로 이 미확정 지점을 겨눈 것이다.[^dascandy]
그 실험이 실제로 수행되었다는 기록은 스레드에 없다.

검증 시도의 결과도 애매하다.
`axoaxonic`은 zbar-tools 디코더에 PNG를 그냥 넣어 봤더니 코드를 아예 검출하지 못했다고 보고했다.[^axoaxonic-zbar]
정지 이미지에서 검출조차 되지 않는다는 사실은 이 트릭이 판독 알고리즘의 성질이라기보다 실시간 카메라 파이프라인의 반복 시도라는 성질에 더 크게 기대고 있을 가능성을 시사한다.
`hadley`의 관찰이 그 방향을 뒷받침한다.
휴대폰을 가만히 들고 있었더니 정렬 표시에 강조 표시만 뜨고 아무 일도 일어나지 않다가, 다른 각도로 움직이기 시작하자 움직이는 동안 안정적으로 인식되었다는 것이다.[^hadley]
“각도에 따라 다른 코드”라는 설명은 사실 “흔들면 언젠가 하나가 걸린다”에 가까울 수 있다.

### 재현성이 기기와 소프트웨어에 따라 갈리는데 그 편차가 정리되지 않았다

이 실험의 결과 보고는 전부 일화다.
`ShakataGaNai`은 아이폰이 하나에 고정되는 경향이 있었고 휴대폰을 회전하면 한쪽이나 다른 쪽으로 가는 데 도움이 되는 듯했으며 몇 번은 마스토돈과 깃허브 링크 사이를 오갔다고 했다.[^shakata]
`mkl`의 갤럭시 노트 20은 대부분을 거부하고 QR 코드로 인식조차 하지 않았으며, 화면에서 아주 멀리 떨어져야 한 URL이 겨우 읽혔다.[^mkl]
`Lacey`의 휴대폰은 마스토돈 URL을 더 반겼고[^lacey], `stranger_frequencies`는 QR 스캐너 앱에서는 마스토돈 링크가 훨씬 자주 나오지만 기본 카메라 앱에서는 둘 다 비슷했다고 적으며 소프트웨어 디코더의 몫이 작지 않을 것이라고 했다.[^stranger]
`attie`는 아예 스크린샷 두 장을 붙였다.
구글 렌즈는 `github.com/cwalther`를, Dynamsoft Barcode Reader는 `mstdn.social/@isziaui`를 해독했다.[^attie]

문제는 이 편차가 트릭의 성능 지표로 정리되지 않는다는 점이다.
“각도를 바꾸면 다른 코드가 나온다”는 주장이 참인지 확인하려면 기기별로 각도 대비 판독 결과의 분포가 필요한데, 스레드에도 HN에도 그런 데이터는 없다.
`jdoe1337halo`가 직접 만든 대화형 생성기 사이트도 같은 문제에 부딪혔다.
그는 대각선 분할 방식을 설명하며 오류 정정 수준 H 덕분에 각도에 따라 어느 URL이든 읽힌다고 썼지만, `HenryBemis`는 안드로이드의 QR & Barcode Scanner와 아이폰 13 기본 카메라 양쪽에서 생성된 코드를 전혀 읽지 못했다고 보고했고 `Aachen`도 F-Droid의 스캐너에서 실패했다.[^jdoe][^henry][^aachen]
`jdoe1337halo`는 자기 아이폰 12 프로 맥스에서는 된다며 더 균등한 분할을 찾아보겠다고 답했다.[^jdoe2]

대각선 분할이 실패한 사실 자체는 유용한 신호다.
Walther도 처음에는 보기 좋아서 대각선을 시도했다가 어떤 이유에서인지 체커보드가 더 잘 되어 바꿨다고 밝혔다.[^isziaui-diagonal]
어떤 이유에서인지가 끝내 밝혀지지 않은 채 남아 있다는 점이 이 실험의 위치를 말해 준다.

### 공격 벡터 논쟁은 위협 모델을 세우지 못한 채 겉돌았다

HN 토론의 가장 긴 가지는 보안 응용 가능성이었는데, 결론 없이 끝났다.
`Normal_gaussian`은 공공장소의 화면이 현재 사용자에 대한 정보에 따라 눈에 띄게 달라 보이지 않으면서 QR 코드를 바꾸는 공격을 상상했다.
절반씩 섞은 코드를 만들고 카메라 기반 특성 평가 같은 외부 입력으로 목표를 정한 뒤, 원하는 쪽이 잡힐 확률이 높아지도록 색을 미세하게 조정하는 방식이다.[^normal-gaussian]

`t_mann`의 반박이 핵심을 찔렀다.
사용자를 다르게 대우하려고 QR 코드를 바꿀 필요조차 없으며, QR 코드의 압도적 다수 용도인 고정 URL로 보내 놓고 수집한 데이터에 따라 누구에게 무엇을 보여 줄지 서버에서 정하면 그만이고, 그것을 신경 쓸 사람들은 이미 오늘날 웹의 대부분이 그렇게 돌아간다는 사실을 절감하고 있다는 것이다.[^t-mann]
`Normal_gaussian`은 공격 벡터의 가치가 같은 목적을 이룰 다른 방법이 있다고 해서 사라지지는 않는다고 답하며, QR 코드가 URL 말고도 와이파이 자격 증명, 연락처, 통화, 문자, 이메일, 캘린더 일정을 담을 수 있고 앱 전용 URI는 기기를 떠나지도 않는다는 점을 들었다.[^normal-gaussian2]

이 응수는 옳지만 원래 공격 시나리오를 지탱하지 못한다.
그가 든 사례들, 곧 인구 집단별로 다른 피드백 양식을 보여 주거나 당첨 확률을 조작하는 시나리오는 어느 것도 와이파이 자격 증명이나 앱 URI와 무관하고 전부 서버에서 더 은밀하게 처리된다.
`michaelmior`가 한 줄로 정리했다.
화면을 소유하고 있다면 사용자를 원하는 어느 서버로든 보낼 수 있다는 것이다.[^michaelmior]

가장 설득력 있는 반론은 `daft_pink`의 것이었다.
기존 코드 위에 다른 QR 코드를 그냥 덮어 붙이는 것과 비교해 이것의 가치를 잘 모르겠으며, 전부를 가져올 수 있는데 왜 일부만 얻으려 하느냐는 것이다.[^daft-pink]
`notRobot`의 답이 사실상 정답이다.
멋지다는 것이 그 가치라는 것이다.[^notrobot]

물론 반쪽만 가로채는 것이 이득인 좁은 경우는 있다.
`Terr_`는 활동이 끊기지 않은 것처럼 보이게 해 진짜 소유자가 알아채지 못하게 하려면 100% 미만의 방문자만 잡는 것이 범죄에 유용할 수 있지만, 그것도 피싱 사이트가 일부를 원래 사이트로 되돌려 보내는 소프트웨어 방식이 더 쉬울 것이라고 했다.[^terr]
`post-it` 역시 광고 소유자가 와서 광고가 제대로 보이는지와 URL이 예상대로인지 확인하는 상황을 상정하며, 누군가 보고 있는 동안 눈치채지 못하게 바꿔치기할 수 있는 좁은 용도가 있을지 모른다고 했다.[^post-it]
한편 `michaelt`가 지적했듯 현실의 QR 공격은 이런 정교함이 필요 없다.
주차장의 휴대폰 결제 안내판에 자기 QR 코드를 덧붙여 놓고 신용카드 정보가 들어오기를 기다리면 된다.[^michaelt]

### 정작 진짜 결함으로 보이는 것은 다른 곳에서 발견되었는데 묻혔다

`nixpulvis`가 보고한 현상은 이 트릭보다 훨씬 심각하다.
iOS에서 이미지를 길게 누르면 `github.com`으로 간다고 표시되는데 미리보기 자체는 마스토돈 쪽이었다는 것이다.
QR 코드를 두 번 파싱해서 서로 다른 결과를 얻고 있다는 뜻이며, 길게 누를 때 뜨는 URL을 확인하는 사람이 얼마나 될지는 모르겠지만 사람들을 속이는 데 쓰일 수 있겠다고 했다.[^nixpulvis]
`noitpmeder`의 반응이 짧고 정확했다.
이건 익스플로잇처럼 들린다는 것이다.[^noitpmeder]

`russellbeattie`가 구조를 짚었다.
운영체제의 두 부분이 각각 자기 QR 파싱 코드를 쓰고 있을 수 있으며, 스마트 텍스트가 하나를 쓰고 이미징 시스템이 다른 하나를 쓰는 식으로 각각 미묘하게 다른 오류 정정 구현을 갖고 있는 듯하다는 것이다.
그는 의도적으로 오류를 넣은 표준 QR 코드로 같은 일을 일으키는 것도 가능할 것 같으며, 두 구현이 오류를 어떻게 다르게 정정하는지만 알아내면 되고, 누군가 챙겨 가기를 기다리는 버그 바운티를 발견한 것 같다고 덧붙였다.[^russellbeattie]

`layer8`은 이것을 더 일반적인 코드 냄새로 옮겼다.
두 호출이 반드시 같은 결과를 반환해야 하는 맥락에서 같은 함수나 게터를 두 번 부르는 전형적인 경우이며, 값을 한 번 받아 변수에 담고 그것을 쓰는 형태와 대비된다는 것이다.[^layer8-toctou]
`pas`가 보통 TOCTOU라고 부른다고 하자[^pas] `layer8`은 검사 대 사용이 아니라 일관성이 필요한 다중 사용 상황에서도 자주 본다고 답했다.[^layer8-multi]

여기서 지적할 것은 이 발견이 스레드 안에서 흩어진 채 끝났다는 사실이다.
미리보기에 보이는 URL과 실제로 열리는 URL이 갈릴 수 있다면, 그것은 예술적 장난이 아니라 사용자가 링크를 확인하는 유일한 수단이 무력화된다는 뜻이다.
`_august`는 자신의 iOS에서는 마스토돈 링크가 주 “열기” 링크로 뜨고 깃허브가 앱 링크로 함께 뜬다고 보고했는데[^august], 같은 운영체제에서 표시 결과가 갈린다는 사실 자체가 문제를 키운다.
이 실마리를 정식 보고로 밀고 간 사람이 있었다는 기록은 없다.

## 인사이트

### 사람이 확인할 수 없는 인터페이스에는 신뢰 표시를 붙일 자리가 없다

이 트릭이 불편하게 느껴지는 이유는 두 URL이 나온다는 사실 자체가 아니다.
사람이 그림을 아무리 들여다봐도 어느 쪽이 나올지 알 수 없다는 사실이다.
`http_error_418`이 정확히 그 지점을 짚었다.
훨씬 미묘하고 사악한데, 무슨 일이 일어나는지가 사람 눈에 명백하지 않기 때문이라는 것이다.[^http418]

이 문제에 대해 HN에서 나온 제안들은 모두 같은 방향을 가리킨다.
`the_arun`은 QR 코드가 대상 URL을 텍스트로도 함께 보여 줘야 사용자가 어디로 가는지 알 수 있으며 일종의 명시적 동의라고 했고[^the-arun], `jimjimwii`는 브라우저가 주소창에 URL을 보여 주는 것과 같다고 덧붙였다.[^jimjimwii]
`trebligdivad`는 더 나아가 판독기가 검사할 수 있는 사람이 읽을 수 있는 부착물을 정의하자고 제안했다.
URL의 루트를 QR 코드 위 특정 위치에 특정 표시와 함께 인쇄해 두면 판독기가 그것을 OCR로 읽어 인코딩된 URL과 일치하는지 검증할 수 있고, 루트만 넣으므로 코드 쪽에는 그 위치 고유의 복잡한 경로를 담을 수 있다는 것이다.[^trebligdivad]
`johnea`는 반대편 끝에서 결론을 냈다.
QR 코드는 단축 URL처럼 악용을 부르며, 본질적으로 읽을 수 없는 URL이라 어디로 보내질지도 몇 번 리다이렉트될지도 알 수 없으니 자신은 쓰지 않는다는 것이다.[^johnea]

주목할 대목은 이런 제안이 이미 부분적으로 구현되어 있고, 그 구현이 이 실험의 설계를 바꿨다는 점이다.
Walther가 두 URL의 도메인을 일부러 다르게 고른 이유가 iOS 카메라 앱이 실시간 미리보기에 도메인만 보여 주기 때문이었다는 진술을 다시 보라.[^isziaui-domain]
신뢰 표시가 도메인만 보여 준다는 사실이, 시연자에게는 “도메인이 다르면 전환이 눈에 띈다”는 연출 장치가 되었고 공격자에게는 “경로만 다르면 전환이 보이지 않는다”는 은신처가 된다.
같은 UI 결정이 시연과 공격에 정확히 대칭으로 작동한다.

여기서 나오는 결론은 QR 코드를 쓰지 말자는 것이 아니라, 미리보기의 축약이 곧 공격 표면이라는 것이다.
축약하지 않으면 사람이 읽지 않고, 축약하면 축약된 부분이 공격자의 자유 공간이 된다.
이 딜레마는 QR 코드만의 것이 아니라 브라우저 주소창의 하위 도메인 표시, 메일 클라이언트의 발신자 표시명, 결제 앱의 수취인 이름 표시가 모두 공유한다.
`chii`가 은행 앱이 수취인 이름을 보여 준다는 안전장치에 대해 소문자 l을 숫자 1로 바꾼 것 같은 유사한 이름으로 계좌를 만들면 그만이라고 답한 것이 같은 구조다.[^chii]

### 판독기의 비결정성이 이 실험으로 처음 대중에게 노출되었다

QR 코드는 결정적인 것처럼 취급된다.
찍으면 그 URL이 나온다는 것이 이 기술에 대한 사회적 계약이고, 그래서 결제와 승차권과 신분 확인에 쓰인다.
그러나 `layer8`의 설명이 드러내듯 실제 계약은 훨씬 약하다.
판독기는 체크섬을 통과하는 아무 해석이나 내놓는다.

평소에는 이 약함이 보이지 않는다.
정상적인 코드는 체크섬을 통과하는 해석이 하나뿐이기 때문이다.
이 실험은 그 해석을 둘로 만들어 시스템의 실제 보증 수준을 드러냈고, 그것이 사람들이 놀란 진짜 이유다.
`Joker_vD`가 QR 코드에는 체크섬이 있지 않느냐, 아니면 오류 정정이 들어 있느냐, 그래야만 한쪽 85%와 다른 쪽 15%가 섞인 것이 작동할 수 있을 것 같다고 물은 것은 정확히 이 계약을 확인하려는 질문이었다.[^jokervd]

이 노출의 두 번째 함의는 검증 도구가 없다는 것이다.
어떤 인쇄물의 QR 코드가 단일 해석만 갖는지 확인하려면 무엇을 실행해야 하는지 아무도 답하지 못했다.
`Normal_gaussian`은 핵심 라이브러리에서 “덜 최적인” 격자를 써서 대안이 되는 유효한 QR 코드를 찾는 방식으로 이것을 식별하는 일이 비교적 쉬울 것이라고 하면서도, API가 혼란스러워져 방어를 어렵게 만들고 기존 라이브러리가 널리 퍼져 있으니 오랫동안 공격으로 남을 것이라고 덧붙였다.[^normal-gaussian3]
이것이 이 실험이 남긴 가장 실용적인 숙제다.
생성기는 자기가 만든 코드가 모호하지 않은지 검사하지 않고, 판독기는 자기가 고른 해석이 유일한지 보고하지 않는다.
둘 중 하나만 있어도 이 트릭은 재미로만 남을 텐데, 어느 쪽도 없다.

인접 노트인 [QR 코드 생성 단계 해설](creating-step-by-step.md)에서 확인한 비대칭이 여기서 대가를 치른다.
인코딩은 규격에 빈틈없이 정의되어 있고 교육 자료도 넘치지만, 이미지에서 격자를 찾는 앞단은 규격에도 자료에도 비어 있다.
그 빈칸이 곧 이 트릭의 활동 공간이다.

### 취미 실험의 수명은 저자의 계획이 아니라 답글 사슬이 결정한다

Walther 본인은 이것을 한밤중의 빠른 실험, 자기 표현으로는 순간적인 헛생각이라고 불렀다.
HN 1위 소식을 전해 듣고 그는 사람들이 자기 진짜 프로젝트에도 이만큼만 관심을 가져 준다면 좋겠다며, 상대의 렌티큘러 쪽이 실용적으로도 훨씬 쓸모 있다고 했다.[^isziaui-brainfart]
Dupont의 답이 좋았다.
그 기분을 안다면서, 그래서 헛생각도 항상 공개해야 하며 무엇이 사람들을 자극할지 알 수 없고 그것이 다른 작업으로 시선을 끌어오는 깔때기 역할을 한다는 것이다.[^gvy-funnel]
Walther는 QR 코드에 자기 마스토돈 프로필을 넣은 것이 우연히도 팔로워 수를 늘리는 데 아주 효과적이었다고 인정했다.[^isziaui-followers]

이 스레드가 실제로 어떻게 이어졌는지가 그 주장의 증거다.
2025년 1월의 첫 실험에서 시작해 며칠 만에 `xssfox`의 디더링 판본과 마스크 실험 표가 나왔고, 2월에는 `rdnt`가 이것을 PCB에 인쇄해 모든 링크를 하나의 QR에 담은 명함을 만들고 싶다며 주말이 또 날아갔다고 했다.[^rdnt]
2026년 3월에는 `hacknorris`가 만드는 법을 물었고, Walther가 같은 크기의 QR 코드 두 개를 만들어 각 픽셀의 좌상단과 우하단 사분면에 하나를 나머지에 다른 하나를 보이게 겹치면 되며 자신은 체커보드 패턴으로 채운 레이어 마스크를 써서 포토샵으로 했을 것이라고 답했다.[^isziaui-howto]
`hacknorris`는 그날 바로 성공했고, 색 판본과 중앙에 이미지를 넣는 변형을 며칠에 걸쳐 시도했다.
2026년 7월에도 같은 스레드에서 리눅스가 도는 명함 이야기가 오갔다.[^hacknorris-card]

정작 저자 본인의 후속 작업도 멈추지 않았다.
2026년 5월에는 움직이는 부품 없이 시차만으로 네 방향에서 각각 다른 URL이 읽히는 원판을 3D 프린터로 만들었고, 골판지에 플로터로 그리는 방식은 너무 부정확해서 3D 프린팅으로 갔다고 밝혔다.
정렬 사각형이 나머지 평면보다 2mm 솟아 있는 구조다.[^isziaui-4way]
같은 달 말에는 모서리를 가리면 판독기가 다른 코드를 잡게 되는 판본을 올렸고 부스트 474회, 좋아요 759회를 받아 원래 실험을 넘어섰다.[^isziaui-corner]

18개월에 걸친 이 사슬에서 처음 계획된 것은 아무것도 없다.
Dupont이 렌티큘러를 만들지 않았다면 Walther는 시작하지 않았을 것이고, `xssfox`가 근사 충돌을 제안하지 않았다면 마스크 표는 없었을 것이며, `hacknorris`가 만드는 법을 묻지 않았다면 제작 절차는 어디에도 기록되지 않았을 것이다.
공개된 답글 사슬은 결과물을 보관하는 장소가 아니라 다음 실험을 생산하는 장치였다.

### 이 트릭의 진짜 가치는 공격이 아니라 판독기 다양성의 측정에 있다

HN 토론은 이것을 공격 도구로 볼지 장난감으로 볼지를 두고 갈렸지만, 세 번째 쓰임이 스레드 안에 이미 있었다.
`attie`가 구글 렌즈와 Dynamsoft를 나란히 찍어 올린 스크린샷이 그것이다.[^attie]
같은 이미지가 어느 판독기에서 어느 코드로 읽히는지가 그 판독기의 표본 추출 전략을 드러낸다.

이것은 사실상 QR 판독기용 지문 채취 기법이다.
체커보드에서 A가 나오고 대각선에서 B가 나오는 판독기와 그 반대인 판독기는 격자 정렬과 이진화 방식이 다르다는 뜻이며, 여러 마스크 형태를 조합한 시험지 한 장이면 미지의 판독기 구현을 분류할 수 있다.
`sschueller`가 안드로이드 기본 판독기들에서 애를 먹다가 연속 스캔을 켜서 각도를 바꾸며 결과가 바뀌는 것을 볼 수 있는 SDK 데모 앱을 찾아냈다고 한 것은[^sschueller] 이미 그런 측정 도구를 손에 쥔 것이나 마찬가지다.

이 관점이 실용적인 이유는 QR 코드가 안전 임계 영역으로 계속 들어가고 있기 때문이다.
결제, 탑승권, 의약품 일련번호, 신분 확인이 모두 판독기 구현에 의존하는데, 그 구현들이 서로 다르게 동작한다는 사실을 정량적으로 아는 사람이 없다.
`nroets`가 트빌리시의 주요 은행이 IBAN을 QR 코드로 공유하게 해 주므로 이론적으로는 이 트릭으로 돈을 훔칠 수 있다고 하면서도 수취인 이름 표시 같은 안전장치가 많다고 덧붙인 것은[^nroets], 안전장치가 판독기 바깥의 응용 계층에만 있다는 뜻이기도 하다.

그래서 이 실험에 이어질 만한 가장 값진 후속 작업은 더 화려한 모호 코드가 아니라 판독기 적합성 시험 모음이다.
모호한 코드 여러 종류를 표준화된 각도와 거리에서 제시하고 각 판독기의 응답 분포를 표로 만드는 일이다.
그런 표가 있었다면 이 스레드의 일화적 보고들이 데이터가 되었을 것이고, `nroets`가 상상한 위협도 이론이 아니라 수치로 평가되었을 것이다.
현재는 아이폰 하나, 갤럭시 하나, 구글 렌즈 하나의 인상만 남아 있다.

---

[^blueflow]: HN `blueflow`, <https://news.ycombinator.com/item?id=42812351>

[^layer8-mech]: HN `layer8`, <https://news.ycombinator.com/item?id=42814649>

[^hammock]: HN `hammock`, <https://news.ycombinator.com/item?id=42815063>

[^isziaui-ecc]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/116301105300028251>

[^xssfox-collision]: Mastodon `xssfox@cloudisland.nz`, <https://cloudisland.nz/@xssfox/113877544521983208>

[^isziaui-todo]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113877665164733798>

[^isziaui-mask]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113896462366412353>

[^xssfox-prefix]: Mastodon `xssfox@cloudisland.nz`, <https://cloudisland.nz/@xssfox/113896486173113698>

[^isziaui-domain]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113896629009825528>

[^xssfox-dither]: Mastodon `xssfox@cloudisland.nz`, <https://cloudisland.nz/@xssfox/113879693263140889>

[^isziaui-dither]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113879730265801317>

[^nemothorx]: Mastodon `nemothorx@teh.entar.net`, <https://teh.entar.net/@nemothorx/113881478615577388>

[^nemothorx-v1]: Mastodon `nemothorx@teh.entar.net`, <https://teh.entar.net/@nemothorx/113882387227967367>

[^isziaui-alpha]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113883056361417614>

[^nemothorx-alpha]: Mastodon `nemothorx@teh.entar.net`, <https://teh.entar.net/@nemothorx/113883205700551732>

[^vikxin]: Mastodon `vikxin@beach.city`, <https://beach.city/@vikxin/113877375887539269>

[^bornach]: Mastodon `bornach@fosstodon.org`, <https://fosstodon.org/@bornach/113888959500529342>

[^isziaui-conjecture]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113882245762430574>

[^dascandy]: Mastodon `dascandy@infosec.exchange`, <https://infosec.exchange/@dascandy/113908157751646173>

[^axoaxonic-zbar]: Mastodon `axoaxonic@synapse.cafe`, <https://synapse.cafe/@axoaxonic/113882363180719401>

[^hadley]: Mastodon `hadley@plush.city`, <https://plush.city/@hadley/113874739231872393>

[^shakata]: HN `ShakataGaNai`, <https://news.ycombinator.com/item?id=42809360>

[^mkl]: HN `mkl`, <https://news.ycombinator.com/item?id=42811875>

[^lacey]: Mastodon `Lacey@mastodon.gamedev.place`, <https://mastodon.gamedev.place/@Lacey/113878207277574967>

[^stranger]: Mastodon `stranger_frequencies`, <https://mstdn.social/@stranger_frequencies/113882201570343079>

[^attie]: Mastodon `attie@chaos.social`, <https://chaos.social/@attie/113877446353144416>

[^jdoe]: HN `jdoe1337halo`, <https://news.ycombinator.com/item?id=42811404>

[^henry]: HN `HenryBemis`, <https://news.ycombinator.com/item?id=42812061>

[^aachen]: HN `Aachen`, <https://news.ycombinator.com/item?id=42812202>

[^jdoe2]: HN `jdoe1337halo`, <https://news.ycombinator.com/item?id=42816574>

[^isziaui-diagonal]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113883126103665952>

[^normal-gaussian]: HN `Normal_gaussian`, <https://news.ycombinator.com/item?id=42809577>

[^t-mann]: HN `t_mann`, <https://news.ycombinator.com/item?id=42809802>

[^normal-gaussian2]: HN `Normal_gaussian`, <https://news.ycombinator.com/item?id=42809996>

[^michaelmior]: HN `michaelmior`, <https://news.ycombinator.com/item?id=42811665>

[^daft-pink]: HN `daft_pink`, <https://news.ycombinator.com/item?id=42809815>

[^notrobot]: HN `notRobot`, <https://news.ycombinator.com/item?id=42809819>

[^terr]: HN `Terr_`, <https://news.ycombinator.com/item?id=42815700>

[^post-it]: HN `post-it`, <https://news.ycombinator.com/item?id=42814904>

[^michaelt]: HN `michaelt`, <https://news.ycombinator.com/item?id=42812757>

[^nixpulvis]: HN `nixpulvis`, <https://news.ycombinator.com/item?id=42809601>

[^noitpmeder]: HN `noitpmeder`, <https://news.ycombinator.com/item?id=42809739>

[^russellbeattie]: HN `russellbeattie`, <https://news.ycombinator.com/item?id=42810939>

[^layer8-toctou]: HN `layer8`, <https://news.ycombinator.com/item?id=42814418>

[^pas]: HN `pas`, <https://news.ycombinator.com/item?id=42815136>

[^layer8-multi]: HN `layer8`, <https://news.ycombinator.com/item?id=42815896>

[^august]: HN `_august`, <https://news.ycombinator.com/item?id=42809899>

[^http418]: Mastodon `http_error_418@hachyderm.io`, <https://hachyderm.io/@http_error_418/113907426978025400>

[^the-arun]: HN `the_arun`, <https://news.ycombinator.com/item?id=42810641>

[^jimjimwii]: HN `jimjimwii`, <https://news.ycombinator.com/item?id=42811042>

[^trebligdivad]: HN `trebligdivad`, <https://news.ycombinator.com/item?id=42816010>

[^johnea]: HN `johnea`, <https://news.ycombinator.com/item?id=42817663>

[^chii]: HN `chii`, <https://news.ycombinator.com/item?id=42811148>

[^jokervd]: HN `Joker_vD`, <https://news.ycombinator.com/item?id=42812295>

[^normal-gaussian3]: HN `Normal_gaussian`, <https://news.ycombinator.com/item?id=42809598>

[^isziaui-brainfart]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113882251035829031>

[^gvy-funnel]: Mastodon `gvy_dvpont@mastodon.social`, <https://mastodon.social/@gvy_dvpont/113883116778992363>

[^isziaui-followers]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/113883154363325512>

[^rdnt]: Mastodon `rdnt@hachyderm.io`, <https://hachyderm.io/@rdnt/113947092431450677>

[^isziaui-howto]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/116291970679585576>

[^hacknorris-card]: Mastodon `hacknorris`, <https://mstdn.social/@hacknorris/116866934595739586>

[^isziaui-4way]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/116636531415929535>

[^isziaui-corner]: Mastodon `isziaui`, <https://mstdn.social/@isziaui/116664559669856869>

[^nroets]: HN `nroets`, <https://news.ycombinator.com/item?id=42811016>

[^sschueller]: HN `sschueller`, <https://news.ycombinator.com/item?id=42811433>

발단이 된 게시물: <https://mastodon.social/@gvy_dvpont/113873265010018431>

HN 토론 (546점, 76 댓글): <https://news.ycombinator.com/item?id=42809268>

Hackaday 기사: <https://hackaday.com/2025/01/23/this-qr-code-leads-to-two-websites-but-how/>

대화형 생성기: <https://dualqrcode.com>
