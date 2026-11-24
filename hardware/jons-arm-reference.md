# Jon's Arm Reference

<https://arm.jonpalmisc.com/>

HN 토론: <https://news.ycombinator.com/item?id=50617499> (1112점, 258개 댓글)

GN 토론: <https://news.hada.io/topic?id=37731>

## 소개

Jon's Arm Reference는 Armv8-A와 Armv9-A가 정의하는 AArch64 명령어 집합과 시스템 레지스터의 참조 문서를 보여 주는 사이트이다.
검색창에서 명령어나 레지스터를 찾을 수 있고, 기본 명령어, SIMD, SVE, SME 목록과
AArch64와 AArch32 레지스터 목록을 직접 훑을 수도 있다.
검색창은 WebAssembly로 동작하므로 WebAssembly가 꺼진 브라우저에서는 안내문이 나온다.
이 문서는 사이트의 첫 화면과 공지를 읽고 썼으며, 개별 명령어 페이지는 열지 않았다.

첫 화면 맨 위에는 공지가 있다.
운영자 Jon에 따르면 Arm의 변호사들이 사이트를 내리지 않으면 법적 조치를 하겠다고 알렸고,
사이트는 2026년 12월 4일에 종료된다.
Jon은 북마크와 링크가 계속 동작하게 할 방법을 찾아보겠다고 한다.
저장소나 별도 프로젝트 사이트는 확인하지 못했다.

## 분석

### 공지가 밝힌 사실과 밝히지 않은 사실

공지는 Arm이 요청한 사실과 종료일만 쓴다.
요구의 법적 근거는 공지에 없다.
HN에서 운영자 jonpalmisc는 Arm이 상표와 지식재산을 쓴다는 이유로 제거를 요구했고,
문서를 호스팅하면서 사이트의 쓸모를 지키는 것이 어렵다고 썼다.[^jonpalmisc]
이는 사이트 운영자 본인이 댓글로 밝힌 것이며 Arm의 서신 원문은 이 문서가 보지 못했다.

### 무엇이 쟁점인가

사이트의 내용은 Arm의 공식 문서를 바탕으로 한 참조 자료이다.
쟁점은 명령어 집합 자체를 서술하는 것과 Arm의 문서 문장과 구성을 그대로 옮기는 것이 같지 않다는 점이다.
이 구분의 법적 판단은 이 문서가 할 수 없다.

## 비평

### 저작권 문제로 보는 시각

HN의 CM30은 하드웨어를 문서화하는 것은 공정 이용이어야 하지 않느냐고 물었다.[^CM30]
sam1714는 내용이 Arm 설명서의 문장을 그대로 복사한 것이고 면책, 특허, 저작권, 수출 통제 문구가 빠져 있어
법적으로는 저작권 침해라고 답했다.[^sam1714]
mort96은 사이트가 클린룸 방식의 역공학 결과였다면 Arm이 할 말이 없었을 것이지만 그렇지 않다고 했다.[^mort96]
bloak은 진짜 제품을 가리키려고 상표를 쓰는 것은 보통 허가가 필요 없지만 다른 지식재산은 모르겠다고 했다.[^bloak]
이 문서는 이 해석을 검증하지 못했고 법적 결론은 내릴 수 없다.

### 변호사의 역할

chmod775는 회사의 법무가 사업을 아는 사람의 승인을 받아야 한다고 했고,
nostrademons는 변호사는 궁극적으로 법원 체계에 책임을 지므로 일반 회사에서 법무가 GC를 거쳐 CEO에게 보고한다고 반박했다.[^chmod775][^nostrademons]
mdnahas는 Arm의 유일한 상품이 지식재산이라 공격적인 변호사를 둔다고 보았고,[^mdnahas]
londons_explore는 맞는 대응은 상징적인 가격의 허가를 주는 것이었다고 했다.[^londons_explore]
HWR_14는 요구를 보낸 사람은 삭제 담당이고 상위 변호사에게 허가 계약을 문의해 볼 수 있다고 제안했다.[^HWR_14]

### 사이트의 가치와 대안

giancarlostoro는 Arm이 인수나 채용을 제안하지 않은 것이 안타깝다고 했고,[^giancarlostoro]
peterfirefly는 Arm의 문서 사이트를 싫어해서 이 사이트를 이제야 알게 된 것이 아쉽다고 했다.[^peterfirefly]
jnurmine은 developer.arm.com의 A-Profile 설명서 페이지에 기계가 읽을 수 있는 명령어와 레지스터 설명이 내려받기로 있다고 알렸다.[^jnurmine]
이 문서는 그 자료의 범위와 사용 조건을 확인하지 못했다.
미러를 만들자거나 토렌트를 배포하자는 제안도 있었는데,
이는 문제를 우회하자는 의견이며 같은 법적 위험이 따를 수 있다.

## 인사이트

### 가져갈 것

이 사례는 오래 쓰이던 개인 참조 사이트가 원 저작자의 문서를 가공한 것이라는 이유로 내려가는 경우이다.
참조 문서를 재구성하는 프로젝트는 원문 복사 범위, 상표 표시, 허가 여부를 처음부터 확인해야 한다는 점이 드러난다.
사이트를 쓰던 사람은 종료 전에 필요한 정보를 공식 문서나 기계 판독용 자료로 옮겨 두는 것이 안전하다.

### 확인할 관찰

1. 12월 4일 이후 사이트가 완전히 내려가는지, 링크 유지 방안이 나오는지.
2. 운영자와 Arm 사이의 허가 협의가 있는지.
3. 공식 자료에 이 사이트의 검색과 탐색 기능을 대신할 수단이 생기는지.

위 셋 모두 이 문서가 확인하지 못했다.

---

[^jonpalmisc]: <https://news.ycombinator.com/item?id=50618088>

[^CM30]: <https://news.ycombinator.com/item?id=50617690>

[^sam1714]: <https://news.ycombinator.com/item?id=50617714>

[^mort96]: <https://news.ycombinator.com/item?id=50625693>

[^bloak]: <https://news.ycombinator.com/item?id=50619484>

[^chmod775]: <https://news.ycombinator.com/item?id=50617833>

[^nostrademons]: <https://news.ycombinator.com/item?id=50618354>

[^mdnahas]: <https://news.ycombinator.com/item?id=50626665>

[^londons_explore]: <https://news.ycombinator.com/item?id=50618764>

[^HWR_14]: <https://news.ycombinator.com/item?id=50618954>

[^giancarlostoro]: <https://news.ycombinator.com/item?id=50618683>

[^peterfirefly]: <https://news.ycombinator.com/item?id=50623608>

[^jnurmine]: <https://news.ycombinator.com/item?id=50624350>
