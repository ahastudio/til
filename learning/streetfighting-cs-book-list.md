# “거리 싸움꾼 컴퓨터 과학자”용 도서 목록은 30여 권을 입문과 중급과 고급으로 나누고, 머신러닝과 양자와 보안과 가속기는 일부러 뺀다

원문: [Book list for streetfighting computer scientists](https://nick-black.com/dankwiki/index.php?title=Book_list_for_streetfighting_computer_scientists)

HN 토론: <https://news.ycombinator.com/item?id=50504718> (47점, 14개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/iyfprw/book_list_for_streetfighting_computer> (5점, 0개 댓글)

## 요약

nick-black.com의 개인 위키 dankwiki에 있는 2025년판 도서 목록이다.
이 문서는 페이지 전문을 읽었다. 책을 읽어 보지는 않았고 아래는 목록과 필자의 짧은 설명을 줄인 것이다.
필자의 문체는 욕설이 섞인 도발조여서 이 문서는 그 표현을 옮기지 않는다.

필자는 이 목록이 “프로그래머를 위한 최고의 책” 목록과 다르다고 밝힌다. Code Complete나 Clean Code 같은 책은 일하면서 알게 될 것이라고 본다.
읽을 가치는 책 속 내용을 알고 싶은 사람에게만 있다는 태도이다.

목록의 구성은 다음과 같다.

- 입문: Stepanov의 From Mathematics to Generic Programming과 The Elements of Programming, Gustedt의 Modern C, Hanson의 C Interfaces and Implementations, Stroustrup의 The C++ Programming Language, Josuttis의 C++ Move Semantics(필자는 이 책이 Rust를 어느 책보다 잘 정당화한다고 평한다), The Rust Programming Language. 필자는 C와 C++를 쓸 필요가 있느냐는 질문에 대체로 아니라고 하면서도, 대부분의 하드웨어에 구현되어 있고 중요한 모든 운영체제의 기본 API를 표현하는 공용어이므로 읽는다고 쓴다.
- 중급(“brawling”): Dijkstra의 A Discipline of Programming(필자가 쪽당 가장 아름다운 책이라고 함), Knuth의 The Art of Computer Programming(1권과 4B권), Warren의 Hacker’s Delight, Stevens와 Rago의 Advanced Programming in the UNIX Environment, Stevens의 UNIX Network Programming, SICP, Varghese의 Networking Algorithmics, McKusick의 FreeBSD 설계와 구현, Kerrisk의 The Linux Programming Interface, Communications Networks, Kleinrock의 Queueing Systems, Hennessy와 Paterson의 Computer Architecture, Kennedy의 Optimizing Compilers for Modern Architectures(구현에는 Muchnik도 함께), CLRS, Samet의 Metric and Multidimensional Data Structures, McKenney의 Is Parallel Programming Hard, Crochemore 외의 Algorithms on Strings, Parallel Computer Architecture, Computation Structures, The Anatomy of a High-Performance Microprocessor, Vazirani의 Approximation Algorithms, Motwani와 Raghavan의 Randomized Algorithms, Garey와 Johnson의 Computers and Intractability, Sipser의 Introduction to the Theory of Computation, Golub와 Van Loan의 Matrix Computations.
- 고급: Arora와 Barak의 Computational Complexity, Pierce의 Types and Programming Languages, Okasaki의 Purely Functional Data Structures, Van Roy와 Haridi의 Concepts, Techniques, and Models of Computer Programming, Barendregt의 The Lambda Calculus.
- 수학: Axler의 Linear Algebra Done Right와 Knuth의 Concrete Mathematics를 보라고 하고, 조합론과 확률·통계와 선형대수를 확실히 알아야 하며 미적분과 미분 방정식은 알아야 하지만 자주 적분하게 되지는 않는다고 쓴다.

마무리에서 필자는 머신러닝은 싫어해서, 양자는 아직 쓸모가 없어서, SIMT·가속기 책은 모두 형편없어서 넣지 않았고, 보안은 품질 보증의 하위 분야라서 뺐다고 쓴다. 링크가 없는 것은 게을러서라고 한다.
Roughgarden의 알고리즘 책과 Beej의 네트워킹 책은 좋다고 들었지만 아직 말할 수 없다고 하며, Stevens도 XDP나 io_uring 같은 현대의 빠른 네트워킹은 다루지 않는다고 덧붙인다.

## 분석

### 중심 주장은 도구가 바뀌어도 쓸모 있는 기초가 있다는 것이다

목록은 언어 사용법 책이 아니라 오래 가는 기초(알고리즘, 계산 복잡도, 운영체제, 네트워크, 컴퓨터 구조, 컴파일러, 수학)를 가리킨다.
필자가 일부러 뺀 영역(머신러닝, 가속기, 보안, 양자)이 이 기준의 경계를 보여 준다. 변화가 빠르거나 필자가 가치를 낮게 보는 영역은 목록에서 빠졌다.
이 기준은 필자의 취향이고 근거가 제시되지 않는다.

### 책 선택이 시스템 프로그래밍 쪽으로 기울어 있다

중급의 대부분이 UNIX와 네트워크와 구조와 병렬성이다.
이는 필자의 관심 영역(고성능 시스템과 터미널 도구)을 반영한 듯하나, 페이지는 이를 밝히지 않는다.

## 비평

### “컴퓨터 과학자”보다 “시스템 프로그래머”의 목록이라는 지적

HN의 한 댓글은 이 목록이 컴퓨터 과학자가 아니라 프로그래머를 위한 것이라고 했다. Knuth를 빼면 형식 언어와 오토마타(Hopcroft와 Ullman), 논리와 SAT, 범주론, 타입 이론 같은 것이 없다는 것이다.[^yegoblynqueenne]
답글은 고급 절의 TAPL과 람다 계산을 놓친 것이라고 반박했다.[^donaldpshimoda]
다른 댓글은 형식 방법의 지도를 약 250쪽에 주는 책(Monin의 Understanding Formal Methods)을 고급에 더해야 한다고 했다.[^rramadass]
목록의 형식 이론과 논리 비중이 낮다는 점은 맞지만, 계산 복잡도와 계산 이론과 타입 이론은 포함되어 있다.

### 필자가 다 읽었는지의 신뢰 문제

한 댓글은 30권이 넘고 CLRS는 1,000쪽이 넘는데 필자가 모두 처음부터 끝까지 읽었다고 믿으라는 것이냐고 했고, 추천 목록은 읽은 책의 상위 10%여야 신뢰할 수 있다고 했다. 책 하나를 추천하는 실험을 제안했다.[^0xdeafbead]
답글들은 Ousterhout의 A Philosophy of Software Design과 Knuth의 Literate Programming,[^williamadams]
Learn You a Haskell for Great Good를 꼽았다.[^rybosome]
다른 댓글은 책을 처음부터 끝까지 읽을 필요는 없다고 했고,[^specproc]
또 다른 댓글은 수년 동안 전업으로 공부해야 할 분량을 나열하는 것이 이상하다고 했다.[^franzferdinan]
페이지는 필자가 모두 읽었다고 주장하지 않는다. 필자가 아직 읽지 않았다고 밝히는 책(Roughgarden, Beej)도 있다.

### 농담에 대한 반응이 많았다

“거리 싸움”이라는 틀을 두고 하도켄을 가르쳐 주는 책, 호신술이나 응급 처치가 없다는 농담이 나왔다.[^bigttygothgf][^poulpy123]
한 댓글은 거리 싸움 수학을 이미 있는 자료로 가리켰다.[^ky3]
이는 책 내용과 무관한 반응이다.

### 시대 변화에 대한 의문

한 댓글은 이 책들을 좋아하지만 취업 시장이 나쁘고 “AI가 어차피 한다”는 환경에서는 주목받지 못할 것이라고 했다. 다만 AI가 한다는 말이 사실이 아니며 “거리 싸움꾼 컴퓨터 과학자”가 구조를 정하고 AI의 기여를 검토해야 한다고 덧붙였다.[^spwa4]
목록이 2025년판이라는 점과 필자가 머신러닝과 가속기를 뺀 점이 이 의문과 닿는다. 이 문서는 AI 시대에 이 목록의 가치가 어떻게 달라지는지 판단하지 못한다.

## 인사이트

### 이 목록에서 가져갈 사용법

30여 권을 모두 읽는 것이 아니라 영역별로 하나씩 골라 읽는 사용법이 현실적이다.
예컨대 시스템이라면 Stevens와 Rago와 Kerrisk, 알고리즘이라면 CLRS, 형식 사고라면 Dijkstra와 Sipser를 고를 수 있다.
HN에서 “책을 처음부터 끝까지 읽을 필요는 없다”는 댓글이 나온 것도 같은 사용법이다.
이는 이 문서의 제안이고 필자가 말한 것은 “내용을 알고 싶은 사람에게만 읽을 가치가 있다”는 것이다.

### 목록 밖에서 보이는 공백

필자가 빼 둔 영역과 스레드가 더한 책은 목록이 무엇을 우선하지 않는지를 보여 준다.
형식 방법과 논리, 소프트웨어 설계(Ousterhout), 문서화(Knuth의 Literate Programming)가 스레드에서 추가로 거론되었다.
필자도 페이지에서 현대 네트워킹(XDP, io_uring) 책의 부재를 인정한다.

### 확인할 관찰

이 목록의 가치를 가를 관찰은 세 가지이다.
다음 판에서 머신러닝과 가속기와 보안에 대한 입장이 바뀌는지,
스레드가 더한 책(형식 방법, 소프트웨어 설계)이 반영되는지,
필자가 아직 읽지 않았다고 한 책에 대한 평이 추가되는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^yegoblynqueenne]: <https://news.ycombinator.com/item?id=50505943>

[^donaldpshimoda]: <https://news.ycombinator.com/item?id=50506587>

[^rramadass]: <https://news.ycombinator.com/item?id=50506655>

[^0xdeafbead]: <https://news.ycombinator.com/item?id=50506206>

[^williamadams]: <https://news.ycombinator.com/item?id=50506675>

[^rybosome]: <https://news.ycombinator.com/item?id=50506455>

[^specproc]: <https://news.ycombinator.com/item?id=50506403>

[^franzferdinan]: <https://news.ycombinator.com/item?id=50506407>

[^bigttygothgf]: <https://news.ycombinator.com/item?id=50506476>

[^poulpy123]: <https://news.ycombinator.com/item?id=50506422>

[^ky3]: <https://news.ycombinator.com/item?id=50505986>

[^spwa4]: <https://news.ycombinator.com/item?id=50506362>
