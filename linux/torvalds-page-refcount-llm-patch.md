# Torvalds가 LLM의 도움을 받아 푼 페이지 참조 카운트 확장성 문제

## 소개

2026년 10월 13일 Linus Torvalds는 리눅스 커널 메일링 리스트에
“Improve page refcount scalability”라는 제목으로
열 개짜리 패치 시리즈를 소개했다.
여러 CPU가 같은 파일의 같은 부분을 반복해 읽을 때
페이지 캐시의 참조 카운트가 병목이 되는 문제를 다룬다.
그는 이 문제를 LLM의 도움을 받아 풀어 보기로 했다고 밝혔다.[^lwn-cover]

Tom's Hardware는 이를
Torvalds가 LLM의 도움을 받아 만든 첫 패치라고 보도했다.[^toms]
Threads 사용자 jsonjeong는 이 기사를 바탕으로 소식을 소개했다.[^jsonjeong-1]

## 문제

`read()`나 `pread()`로 페이지 캐시에서 데이터를 읽을 때,
커널은 폴리오(folio)의 참조 카운트를 올렸다가 내린다.
여러 CPU가 같은 폴리오를 동시에 읽으면
모든 CPU가 같은 캐시 라인에 쓰기를 하게 되어 경합이 생긴다.
Torvalds가 공개한 측정에서 64개 스레드의 초당 읽기 횟수는 1,330만 회에서 멈췄고,
읽기 한 번에 드는 사이클은 약 2만으로 불어났다.[^lwn-cover]

Matthew Wilcox는 2024년 2월 버퍼드 I/O의 확장성 한계를 다룬 논의에서
실제 사용자들이 이 영역의 확장성 문제를 겪는다고 보고했다.[^lwn-cover]

## 지난 시도

| 시기        | 시도                       | 결과                                  |
| ----------- | -------------------------- | ------------------------------------- |
| 2024년 2월  | Torvalds의 초안            | 작은 읽기를 스택 버퍼로 복사하는 방식 |
| 2025년 10월 | Kiryl Shutsemau의 수정판   | 같은 접근을 손봤지만 문제가 남음      |
| 2026년      | Ilya Gladyshev의 다른 접근 | 6판까지 나왔지만 근본적인 문제가 남음 |

Torvalds의 2024년 초안은 `filemap_read()`에서
폴리오 배치용 스택 공간 128바이트를 작은 읽기의 임시 버퍼로 쓰는 방식이었다.
그는 이 초안을 전혀 테스트하지 않았다고 적었다.[^lore-2024]
2026년 메일에서는 이 초안이 고장 났지만 거의 동작했기 때문에
사람들이 얼마나 고장 났는지 지적할 때까지
1년 반 동안 직접 써 왔다고 돌아봤다.[^lwn-cover]
Tom's Hardware는 그가 이 초안을 자기 노트북에서 썼다고 전했지만,[^toms]
메일에는 자기 환경에서 썼다고만 적혀 있다.

## 해법

패치는 자주 읽히는 폴리오를 알아보고,
그 폴리오를 해제할 때 RCU 유예 기간이 지날 때까지 미루도록 표시한다.
해제가 미뤄지므로 폴리오를 찾는 일뿐 아니라 데이터를 읽는 일까지
RCU로 보호되는 구간 안에서 할 수 있다.
사용자 공간으로 복사하다가 페이지 폴트가 나지 않는 빠른 경로에서는
참조 카운트를 아예 건드리지 않는다.
원래 초안과 달리 이중 버퍼링이 필요 없고,
초안의 여러 제약도 사라졌다.[^lwn-cover]

코드는 Torvalds의 공개 git 트리 `rcu-free-v3` 브랜치에 있다.
이전 판은 `noref-filemap-read-with-llm` 브랜치로 남아 있고,
맨 위의 빈 커밋에 배경 설명이 들어 있다.
Torvalds는 도구를 쓰지 않았다면 커밋 메시지를 이보다 짧게 썼을 것이라며
그래도 이 편이 나을 수 있다고 덧붙였다.
같은 실험에서 assoc-array 라이브러리의 버그를 고치는 시리즈도 만들었는데,
이쪽은 코드를 정리해 버그를 고치는 평범한 작업이어서
더 흥미로운 문제가 풀리지 않을 때를 대비한 것이었다고 한다.[^lwn-cover]

## 수치

다음은 `mm/filemap: read from the page cache without folio references`
커밋에 실린 측정이다.[^lwn-cover]

| 64개 스레드 | 초당 읽기 | 읽기당 사이클 | 읽기당 명령어 |
| ----------- | --------- | ------------- | ------------- |
| 적용 전     | 1,330만   | 19,857–19,939 | 1,094–1,101   |
| 적용 후     | 3억 400만 | 735–736       | 959           |

Torvalds의 Ryzen Threadripper에서 23배 빨라진 셈이다.
그러나 그는 모든 CPU가 한 페이지의 작은 부분을 반복해 읽는
매우 인위적인 경우이며, 실제 부하에서는 효과가 훨씬 작을 것이라고 분명히 했다.
그가 강조한 것은 공유 캐시 라인에 쓰기가 없어 거의 완벽하게 확장된다는 점이고,
RCU로 페이지 해제를 미루는 방식이 다른 곳에도 쓰일 수 있다는 점이다.[^lwn-cover]

## 리뷰

메일링 리스트의 반응은 수치를 인정하면서도 설계를 따지는 쪽이었다.

- Matthew Wilcox는 수치가 설득력 있다고 하면서도
  새 페이지 플래그 `PG_rcu_free`가 마음에 들지 않는다며
  페이지 타입(`PGTY_rcu`)을 쓰자고 제안했다.[^willy]
  Torvalds는 해제가 예약된 폴리오가 그보다 훨씬 전부터
  사용자 공간에 매핑되어 있을 수 있어
  페이지 타입으로는 안 된다고 답했다.[^linus-reply]
- Kiryl Shutsemau는 `filemap_read_rcu_batch()`에서
  폴리오가 다른 폴리오로 바뀐 뒤 파일 크기가 늘어나면
  쓰이지 않은 데이터를 읽을 수 있는 경쟁 조건을 찾아 보고했다.[^kiryl-race]
- Kiryl Shutsemau는 플래그를 64비트 전용으로 두자고 제안했고,
  David Hildenbrand도
  이 기능을 64비트로 한정하는 것이 합리적이라고 했다.[^kiryl-64][^hildenbrand]

## AI 정책과의 관계

이 패치는 커널이 AI 도구 사용을 밝히라는 요구를 거둔 시기와 겹친다.
The Register에 따르면 2025년 7월에 생겨 2026년 1월 공식 문서에 들어간
`Assisted-by` 태그 요구는 메인테이너 서밋의 합의로 폐기되었다.[^register]
Torvalds는 도구를 금지하는 규칙을 만들지 않겠다며,
기대하는 것은 사람들이 최선을 다하고
자기가 하는 일을 이해하는 것이라고 했다.[^register]
정책 논쟁의 자세한 경과는
[Torvalds: “X에 AI를 쓰지 말라”는 규칙은 어리석다](torvalds-ai-tool-rules.md)에 정리했다.

Torvalds 스스로 밝힌 대로 이번 실험은
LLM 사용이 큰 주제였던 올해 메인테이너 서밋을 앞두고 시작되었다.[^lwn-cover]
Threads 사용자 jsonjeong는 문제를 깊이 아는 사람이 AI를 쓰면 속도가 남고,
모르는 사람이 쓰면 리뷰할 일이 남는다고 정리했다.[^jsonjeong-5]

## 정리

이 패치에서 LLM이 맡은 몫은 공개된 자료로는 가늠할 수 없다.
메일에 드러난 것은 문제를 2년 넘게 붙들고 있던 사람이 LLM을 써서 다시 풀었고,
그 결과가 곧바로 메모리 관리 메인테이너들의 리뷰를 받아
경쟁 조건과 플래그 설계 문제를 지적받았다는 사실이다.
23배라는 수치보다 이 리뷰 과정이 커널이 말하는
“자기가 하는 일을 이해하는” 도구 사용의 실제 모습에 가깝다.

---

[^lwn-cover]: LWN.net, [Improve page refcount scalability](https://lwn.net/ml/all/CAHk-=wjLjgfwgSZ1RDk4YdNFcV0ntosMO5AmBoHD76Zb3HFY7Q@mail.gmail.com/), 2026-10-13

[^toms]: Tom's Hardware, [Linus Torvalds posts his first AI-assisted patch to the Linux kernel, synthetic test clocks 23x performance leap](https://www.tomshardware.com/software/linux/linus-torvalds-posts-his-first-llm-assisted-patch-to-the-linux-kernel-after-issuing-clear-pro-ai-directives-the-bossman-makes-use-of-ai-tooling-himself), 2026-10-16

[^lore-2024]: lore.kernel.org, [Re: \[LSF/MM/BPF TOPIC\] Measuring limits and enhancing buffered IO](https://lore.kernel.org/all/CAHk-=wjOogaW0yLoUqQ0WfQ=etPA4cOFLy56VYCnHVU_DOMLrg@mail.gmail.com/), 2024-02-26

[^willy]: LWN.net, [Re: Improve page refcount scalability (Matthew Wilcox)](https://lwn.net/ml/all/as6ckC9NJVB8JBuV@casper.infradead.org/), 2026-10-13

[^linus-reply]: LWN.net, [Re: Improve page refcount scalability (Linus Torvalds)](https://lwn.net/ml/all/CAHk-=wiHMFdA9CE4qu7W9vUh=CBrH5w9RMjf2kx=U5BJobrrZA@mail.gmail.com/), 2026-10-13

[^kiryl-race]: LWN.net, [Re: Improve page refcount scalability (Kiryl Shutsemau)](https://lwn.net/ml/all/as6vBoWQGglxXxb0@thinkstation/), 2026-10-13

[^kiryl-64]: LWN.net, [Re: Improve page refcount scalability (Kiryl Shutsemau)](https://lwn.net/ml/all/as9af-Jd_rVZvMlC@thinkstation/), 2026-10-14

[^hildenbrand]: LWN.net, [Re: Improve page refcount scalability (David Hildenbrand)](https://lwn.net/ml/all/4c8f620c-3b98-46b8-bcd8-d73210214deb@kernel.org/), 2026-10-14

[^register]: The Register, [Linux kernel devs drop obligatory confession of AI tool usage](https://www.theregister.com/ai-and-ml/2026/10/14/linux-kernel-devs-drop-obligatory-confession-of-ai-tool-usage/5303140), 2026-10-14

[^jsonjeong-1]: jsonjeong(Threads), [리누스 토발즈(Linus Torvalds)는 2024년 초 직접 짠 수정안을 자기 노트북에서 계속 써왔음.](https://www.threads.com/@jsonjeong/post/Den27mHDnUC), 2026-10-18

[^jsonjeong-5]: jsonjeong(Threads), [그래도 커널 안 찬반 진영의 다툼은 계속됨.](https://www.threads.com/@jsonjeong/post/Den2_p9DgvH), 2026-10-18
