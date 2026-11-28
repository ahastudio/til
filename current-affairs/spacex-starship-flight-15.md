# SpaceX Starship 15차 비행

원문: [Starship Flight 15](https://www.spacex.com/launches/starship-flight-15)

HN 토론: <https://news.ycombinator.com/item?id=50500963> (1068점, 710개 댓글)

GN 토론: <https://news.hada.io/topic?id=36865>

## 요약

SpaceX의 발사 안내 페이지가 비행 뒤 결과 설명으로 바뀐 것이다.
페이지의 모든 서술은 SpaceX의 설명이다.

페이지가 전하는 경과는 이렇다.
2026년 11월 13일 금요일 Starship이 텍사스 Starbase에서 15번째 비행으로 이륙했고, 11월 14일 토요일 Starbase로 돌아와 “모든 것을 바꿨다”고 쓴다.
Super Heavy 부스터는 Pad 2에서 엔진 33기로 상승했고, 핫 스테이징 뒤 Starship은 엔진 6기로 우주를 향해 갔다.
부스터는 방향 전환 기동을 하고 부스트백 연소를 위해 계획된 33기 중 32기를 다시 점화했다.
부스트백 연소는 연료 질량 부족으로 일찍 끝났고 원인은 조사 중이라고 한다.
부스터의 유도·항법·제어가 자동 중단을 일으켜 해상의 대체 착륙 지점으로 스스로 방향을 돌렸고, 착륙 연소를 마치고 걸프 위에서 정지 비행하며 엔진을 껐다. 연소가 끝나자 비행 종단 시스템이 작동했다고 한다.

우주선은 정상 상승 연소 뒤 짧은 관성 비행을 거쳐 엔진 1기를 다시 점화해 궤도에 진입했고, Starlink V3 위성 26기를 배치했다.
모든 위성과 교신이 되었고 궤도를 높이기 시작했다고 한다.
이후 긴 관성 비행 동안 20시간 넘게 시스템을 감시한 뒤 비행 관제팀이 귀환을 준비했다.
해수면용 엔진 1기를 다시 점화해 궤도 이탈 연소를 했고, 대기권을 지나 텍사스 동해안으로 돌아와 걸프 위에서 마지막 기동을 한 뒤 22.5시간 전에 떠난 발사장에 접근했다.
구름을 뚫고 엔진 3기가 착륙 전환을 위해 점화했고, 천천히 내려와 발사탑 Mechzilla의 팔이 닫히며 Starship을 처음으로 포획했다고 쓴다.

## 분석

### 이번 비행의 새로운 점은 궤도에서 돌아온 상단의 회수이다

페이지가 강조하는 것은 두 가지이다.
상단이 궤도에서 22.5시간을 보내고 출발한 발사장으로 돌아왔다는 것, 그리고 발사탑이 그것을 잡았다는 것이다.
HN의 한 댓글은 이를 로켓 역사에서 상단이 궤도에서 돌아와 안전하게 똑바로 착륙한 첫 사례라고 정리하고, 우주왕복선은 똑바로 착륙하지 않았고 외부 탱크는 재사용되지 않았다는 단서를 붙였다.[^motionlessveloc]
답글들은 왕복선의 고체 로켓 부스터가 낙하산으로 바다에 내려 회수·재사용되었다고 바로잡았다.[^mmustapic][^echoangle]
“첫 번째”라는 주장은 정의에 따라 달라지고, 페이지는 “Starship을 처음으로 포획했다”고만 쓴다.

### 기술의 요점은 복잡도를 지상으로 옮긴 것이다

한 댓글은 우주선에서 하드웨어를 크게 줄이고 복잡도를 지상으로 옮긴 점을 지적했고,[^panick21_]
답글은 지상 쪽은 상용 용접 인력이 한 번 싸게 지어 둘 수 있고, 왕복선 시대의 문제는 정비에 대규모 전문 인력이 필요했던 것이라고 했다.[^fedpost]
다른 댓글은 발사탑 팔이 느리고 무거운데도 하강 궤적을 정확히 제어해 손상 없이 붙잡는 점이 인상적이라고 했다.[^generuso]
이는 모두 댓글의 평가이고 페이지에는 설계 논거가 없다.

## 비평

### 부스터는 목표를 달성하지 못했다

페이지는 부스터가 계획된 엔진 33기 중 32기만 다시 점화했고 부스트백이 연료 질량 부족으로 일찍 끝났다고 적는다.
HN에서 한 사용자가 부스터를 왜 잡으려 하지 않았느냐고 물었고, 답글은 슬라이트 엔진 성능 부족으로 부스터가 계획한 위치에 닿지 못해 자동 중단으로 걸프에 갔다고 설명했다.[^narishma][^darmok]
다른 댓글은 일론 머스크가 엔진 성능 부족이 연료 여유 부족을 낳았고 이후 비행에 개선을 넣을 것이라고 했다고 전했다.[^thinkcontext]
다른 댓글은 부스터 포획과 재비행은 이미 이루어졌고 완전한 기능 가운데 증명되지 않은 부분은 우주선 재사용뿐이라고 정리했다.[^consensus1]

### “모든 것을 바꿨다”는 말은 열을 막는 방열판의 검사 결과에 달려 있다

한 댓글은 방열판이 버티면 모든 것이 바뀌고 다음 단계는 같은 우주선을 다시 날리는 것이라고 했다.[^small_model]
답글은 재비행 때 정비 없이 날 수 있는지가 마지막 목표이고 검사 결과가 공개되기를 기다린다고 했고,[^modeless]
다른 답글은 신속한 재사용이라는 목표를 못 이루더라도 타일 교체가 새 상단을 짓는 것보다 훨씬 싸므로 새 시대에 들어섰다고 했다.[^bryanlarsen]
페이지는 방열판의 상태를 말하지 않는다.
따라서 “바꿨다”는 표현은 발사탑 포획이라는 시연에 대한 선언이고, 재사용 경제성에 대한 증거가 아니다.

### 재사용의 경제성을 의심하는 질문이 있다

한 댓글은 재사용 단계가 로켓 방정식의 대가를 두 번 치르는 것 같다고 했고, 답글은 방정식은 건조 질량과 연료를 포함한 질량의 비율에 관한 것이어서 대가를 두 번 치르는 것이 아니라고 반박했다.[^cwkoss][^blackenedgem]
한 댓글은 우주왕복선과 비교해 Starship이 부분 재사용이 아닌 완전 재사용이고 고체 부스터가 없으며 궤도선이 측면이 아니라 위에 얹힌다고 해 설계상 사고 요인을 피한다고 했다.[^gmoromisato]
답글은 왕복선이 그렇게 된 이유(NASA와 국방부라는 여러 주인)를 Starship은 겪지 않는다고 덧붙였고,[^bumby]
다른 답글은 부스터에 날개가 있고 발사장으로 돌아오는 원안이 있었다는 주장의 출처를 물었다.[^n_u]

### 일부 숫자는 페이지가 아니라 댓글에서 나온다

한 댓글은 우주선이 약 260km 궤도에 올라 약 50톤을 배치했다고 했고,[^m4rtink]
다른 댓글은 50톤이 배치되었으니 가격이 크게 내려갈 것이라고 했다.[^vl]
페이지는 위성 26기를 배치했다고만 쓰고 총질량을 적지 않는다.
GeekNews의 사전 안내 글을 옮긴 HN 의견에는 약 52톤이 공표 탑재 능력 100톤의 절반 수준이라는 말이 있었으나 이는 GN⁺가 모은 HN 의견이다.

## 인사이트

### 한 번의 포획에서 읽을 수 있는 것과 없는 것

읽을 수 있는 것은 궤도에서 돌아온 상단의 궤적 제어와 발사탑 포획이 한 번 이루어졌다는 사실이다.
읽을 수 없는 것은 재비행에 필요한 정비 비용과 시간, 부스터의 연료 여유 문제의 원인, 탑재 질량이다.
한 댓글은 놀라운 업적이라면서도 다시 날려야 한다는 점을 짚었고,[^bahmboo]
반응 가운데 다른 한 줄은 이것이 아폴로 11호에 비견되느냐는 질문과 그것과 거의 닮지 않았다는 답이었다.[^somebudyelse][^jtarii]
평가의 기준을 시연의 성공이 아니라 반복 가능성에 두는 편이 안전하다.

### 이 글이 보여 주는 정보의 비대칭

이 문서의 근거는 사업자의 서술과 구경꾼의 댓글이다.
방열판 사진과 정비 기록, 부스터 문제의 조사 결과는 공개되어야 독립적으로 평가할 수 있다.
한 댓글은 방열판 검사 결과를 공개하기를 바란다고 했다.[^modeless]

### 확인할 관찰

이 비행의 의미를 가를 관찰은 세 가지이다.
방열판 검사 결과와 정비 없이 재비행이 이루어지는지,
부스트백 연소가 일찍 끝난 원인이 공개되는지,
다음 비행에서 부스터와 우주선을 함께 포획하는지이다.

---

[^motionlessveloc]: <https://news.ycombinator.com/item?id=50501115>

[^mmustapic]: <https://news.ycombinator.com/item?id=50501250>

[^echoangle]: <https://news.ycombinator.com/item?id=50501307>

[^panick21_]: <https://news.ycombinator.com/item?id=50501050>

[^fedpost]: <https://news.ycombinator.com/item?id=50501558>

[^generuso]: <https://news.ycombinator.com/item?id=50503539>

[^narishma]: <https://news.ycombinator.com/item?id=50501007>

[^darmok]: <https://news.ycombinator.com/item?id=50501030>

[^thinkcontext]: <https://news.ycombinator.com/item?id=50502150>

[^consensus1]: <https://news.ycombinator.com/item?id=50501348>

[^small_model]: <https://news.ycombinator.com/item?id=50501743>

[^modeless]: <https://news.ycombinator.com/item?id=50501867>

[^bryanlarsen]: <https://news.ycombinator.com/item?id=50502981>

[^cwkoss]: <https://news.ycombinator.com/item?id=50501071>

[^blackenedgem]: <https://news.ycombinator.com/item?id=50501104>

[^gmoromisato]: <https://news.ycombinator.com/item?id=50502268>

[^bumby]: <https://news.ycombinator.com/item?id=50503439>

[^n_u]: <https://news.ycombinator.com/item?id=50504481>

[^m4rtink]: <https://news.ycombinator.com/item?id=50502503>

[^vl]: <https://news.ycombinator.com/item?id=50502176>

[^bahmboo]: <https://news.ycombinator.com/item?id=50501811>

[^somebudyelse]: <https://news.ycombinator.com/item?id=50501297>

[^jtarii]: <https://news.ycombinator.com/item?id=50502567>
