# 프랑스의 기가바이트 세금: 11 대 10으로 통과했지만 구독료 인상은 가정이다

원문: [Netflix, Steam, cloud : vos abonnements et téléchargements bientôt plus chers à cause d'une nouvelle taxe ? - Les Numériques](https://www.lesnumeriques.com/societe-numerique/netflix-steam-cloud-vos-abonnements-et-telechargements-bientot-plus-chers-a-cause-d-une-nouvelle-taxe-n264035.html)

HN 토론: <https://news.ycombinator.com/item?id=50310796> (115점, 93개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50315047> (102점, 131개 댓글)

## 요약

프랑스 매체 Les Numériques가 2026년 10월 30일 Guillaume Henri 기자의 이름으로 낸
기사다.
기사는 국민의회(Assemblée nationale)에서 2027년도 재정 법안(projet de loi de
finances)에 붙은 수정안 n° I-1358이 11표 대 10표로 통과했다고 전한다.
수정안은 사회당과 그 계열 의원 모임이 냈고, 프랑스 이용자에게 전달되는 데이터
양을 기준으로 기가바이트당 0.055유로의 부담금을 매긴다.
기사는 이 부담금으로 최대 100억 유로의 세수를 거둘 수 있다고 쓴다.
저자들은 이 비용이 사업자가 데이터를 최적화하고 압축하게 만드는 생태적 효과도
낸다고 내세운다.

운영 방식은 인터넷 접속 사업자(FAI, 인터넷 서비스 제공자)가 분기마다 각 사업자가
보낸 데이터 양을 측정하는 것이다.
측정은 규제 기관 Arcep와 재정 총국(DGFiP)의 공동 감독을 받는다.
콘텐츠 전송 네트워크(CDN)도 포함해 이용자 가까이에 놓인 중계 서버에서 나온
흐름까지 잰다.
대역폭을 많이 쓰지만 이윤이 낮은 서비스를 보호하려고 상한이 있어서, 부과액은
프랑스 매출의 15%나 전 세계 매출의 2%를 넘지 못한다.
수정안은 세금을 내는 쪽이 이용자가 아니라 콘텐츠 제공자라고 명시한다.

기사는 적용 대상이 될 수 있는 서비스를 일곱 범주로 나눠 보여 준다.
Netflix, YouTube, Disney+, Prime Video, Twitch, TikTok 같은 스트리밍과 방송
재방송 서비스가 첫째다.
Steam, Epic Games Store, PlayStation Network, Xbox Network처럼 설치 파일과
업데이트가 50~150기가바이트에 이르는 게임 상점이 둘째다.
Hugging Face와 GitHub 같은 AI 모델과 코드 저장소가 셋째이고, Google Drive,
OneDrive, iCloud, Dropbox와 AWS, Azure, Google Cloud 같은 클라우드와 동기화
서비스가 넷째다.
Instagram, Twitter, Discord, Teams, Zoom 같은 소셜 네트워크와 화상 회의 도구가
다섯째이고, Cloudflare, Akamai, Fastly 같은 CDN 사업자가 여섯째이며, Windows,
macOS, iOS와 Linux 배포판의 보안 패치 배포가 일곱째다.

기사는 소비자가 직접 과세 대상은 아니지만 부담금을 내는 기업이 사업 모델을 바꿀
수 있다고 쓴다.
요금을 올리거나, 프랑스 안 접속으로 가는 대역폭을 제한하거나, 용량이 큰 파일의
다운로드에 한도를 두는 방식이 가능하다는 것이다.
수정안은 간신히 통과했고 아직 상원의 심사를 받아야 하며, 최종 재정법에
들어가려면 행정부의 유보도 넘어야 한다고 기사는 맺는다.

## 분석

### 부담금은 매출이 아니라 전송량에 붙고 측정은 통신사가 맡는다

이 수정안의 구조는 세수를 기업의 이윤이 아니라 물리적 전송량에서 찾는다는 점에서
다른 디지털 과세와 다르다.
매출이나 이익에 붙는 세금은 서비스의 가치에 비례하지만, 이 부담금은 같은
매출이라도 더 많은 데이터를 보내는 사업자에게 더 많이 부과된다.
상한을 매출의 비율로 두는 것은 이 성질을 인정하는 장치로 읽힌다.
이윤이 낮은 서비스가 전송량 때문에 매출을 넘는 부담금을 내는 일을 막으려는
것이다.

측정을 통신사에게 맡긴 점도 특징이다.
KultureGeek은 통신사가 자신의 고객에게 전달되는 데이터 양을 재고, 데이터를
보내는 기업을 식별해 통합되고 익명화된 내역서를 세무 당국에 낸다고
전한다.[^kulturegeek]
같은 보도에 따르면 데이터의 내용이나 목적지에 대한 정보는 요구할 수
없다.[^kulturegeek]
이 설계는 세무 당국이 기업의 서버 기록을 직접 보지 않고 통신사의 측정을 근거로
삼는다는 뜻이다.
이는 이 문서의 해석이다.

### 정치적 무게는 통과 표수가 아니라 이후 절차에서 정해진다

수정안은 두 번째 시도에서 통과했다.
Univers Freebox에 따르면 재정 위원회가 10월 9일에 한 번 부결했고, 사회당 의원
Laurent Lhardit이 낸 수정안이 10월 30일에 국민의회 본회의에서
채택되었다.[^univers-freebox]
예산 담당 총괄 보고관과 정부가 모두 반대 의견을 냈고, 공공 회계 담당
장관(ministre de l'Action et des Comptes publics) David Amiel은 추정 세수 50억
유로의 거의 절반이 미국 대기업이 아닌 더 작은 사업자에게서 나올 수 있다고
경고했다.[^univers-freebox]
Lhardit은 TF1이 다섯 채널을 통신사의 인터넷 단말기(box)로 내보내는 경우 연간
20만~30만 유로의 부담금을 내게 된다고 예를 들었다.[^univers-freebox]

표결은 참석자 35명 중 찬성 11표, 반대 10표였고, KultureGeek은 찬성 11표의 내역을
사회당 5명, La France insoumise 2명, 녹색당 2명, 민주·공화 좌파(GDR) 2명으로
적었다.[^kulturegeek]
Univers Freebox는 Alloforfait를 인용해 투표 참여자가 35명이고 유효표가 21표라고
전한다.[^univers-freebox]
HN의 Sayrus는 잠재 투표자가 577명이라고 썼고, 이 숫자에 비추면 이 표는 전체 의원의 극히 일부가 낸 결과다.[^Sayrus]
이 사실이 의미하는 것은 이 표결이 수정안의 지지가 넓다는 증거가 아니라, 출석이
적은 본회의 시간대에서 소수가 이긴 결과일 수 있다는 점이다.
이는 이 문서의 추론이다.

### 기사의 목록은 법안이 지정한 대상이 아니라 적용될 수 있는 서비스다

기사는 일곱 범주의 목록을 “적용 범위에 들어갈 수 있는” 서비스로 소개한다.
수정안이 이 회사들을 이름으로 지정한 것이 아니라 전송량 기준에 따라 해당될 수
있는 서비스를 기자가 정리한 것이다.
이 구분이 중요한 이유는 목록의 일부가 무료로 배포되는 자원이기 때문이다.
기사는 Hugging Face와 GitHub가 파일당 수십 기가바이트를 “대개 무료로” 전송하고,
Linux 배포판의 패치 배포도 같은 범주에 든다고 쓴다.

## 비평

### 제목이 말하는 구독료 인상은 기사 본문이 말하는 가능성보다 훨씬 단정적이다

제목은 구독과 다운로드가 “곧 더 비싸진다”는 방향으로 읽힌다.
본문은 소비자가 직접 과세 대상이 아니고 기업이 비용을 전가할 수 있다고만 쓰며,
전가 방식으로 요금 인상, 프랑스 접속 대역폭 제한, 대용량 파일 다운로드 제한 세
가지를 든다.
인상이 얼마나 일어날지, 어느 서비스에서 일어날지에 대한 수치나 사업자의 발언은
기사에 없다.
KultureGeek은 한 Twitter 이용자가 월 500기가바이트를 쓰는 가구의 부담을 월
27.50유로, 연 330유로로 계산한 글을 전하면서, 이 계산이 가구에 청구되는 금액의
추정이 아니라고 바로 덧붙인다.[^kulturegeek]
500 × 0.055는 27.5이므로 산식은 맞지만 부담금이 가구가 아닌 콘텐츠 제공자에게
붙는다는 전제를 무시한 계산이다.

HN에서는 같은 오독이 반복되었다.
adrian_b는 하루 50기가바이트 트래픽이 평소이고 Mistral Large 모델 가중치를
내려받은 날에는 1테라바이트였다며, 이 세금이면 하루에 55유로를 내게 된다고
썼다.[^adrian_b]
Brybry는 수정안이 개인이 아니라 통신사 가입자에게 콘텐츠를 제공하는 회사에 붙는
세금이며 상한이 있고 아직 법이 아니라고 바로잡았다.[^Brybry]
embedding-shape는 왜 거주자의 다운로드로 가정하느냐고 물었다.[^embedding-shape]
기사의 제목이 이 오독을 막지 못했다는 점이 이 비평의 핵심이다.

### 세수 추정이 서로 다른 채 설명이 없다

Les Numériques는 최대 100억 유로를 쓴다.
Univers Freebox는 최대 50억 유로를 쓰고, 장관의 경고도 50억 유로를 기준으로
한다.[^univers-freebox]
두 숫자가 두 배 차이인데 기사는 어느 추정에서 나왔는지 밝히지 않는다.
이 문서는 수정안의 본문과 설명서를 직접 열어 보지 않았으므로 어느 쪽이 맞는지
판단하지 않는다.
다만 세금이 기업 부담과 소비자 전가 가능성을 논하는 기사라면, 규모가 두 배로
달라지는 숫자는 독자가 확인할 수 있게 출처를 밝혀야 한다.
세수 추정 근거가 공개되면 기사의 “100억 유로”가 정부 추정인지 수정안 제안자의
추정인지 가려진다.

### 상한 규정과 측정 방식이 한 문장으로 얼버무려져 있다

기사는 상한을 프랑스 매출의 15% 또는 전 세계 매출의 2%라고 쓰고, 둘 중 무엇이
적용되는지 말하지 않는다.
HN에서 malloryerik은 수정안 본문을 인용하며 같은 문구를 확인하고, 프랑스에서만 서비스하는 업체는 2% 상한을 적용받으므로 보호주의적 요소가 있을 수 있다고 썼다.[^malloryerik]
이는 그의 해석이고 그는 변호사가 아니라고 밝혔다.
ThrustVectoring은 Netflix가 프랑스 매출을 하나의 법인에 모으려고 별도 법인을
만들면 어떻게 되느냐고 물었다.[^ThrustVectoring]
기사는 이런 구조의 허점을 다루지 않는다.

측정도 의문이 남는다.
jonathanstrange는 무료 서비스는 품질이 떨어지거나 중단되거나 불법이 될 수 있다고
하면서, 네트워크 트래픽이 온갖 CDN과 임대 서버를 거치는데 누가 내야 하는지
어떻게 정할지가 쉽지 않아 보인다고 썼다.[^jonathanstrange]
기사는 통신사가 측정한다는 구조만 설명하고, 같은 콘텐츠가 여러 CDN을 거칠 때
발신 주체를 어떻게 식별하는지는 말하지 않는다.

## 인사이트

### 소수 출석 표결은 입법 가능성이 아니라 의제 설정의 신호다

HN에서 Sayrus는 이 수정안이 577명의 잠재 투표자 중 11 대 10으로 통과했으며 실제 예산에 들어갈 가능성은 매우 낮다고 썼다.[^Sayrus]
Rexxar는 정부와 상원이 반대할 가능성이 높고 예산 법안 전체가 국민의회에서 부결될
것으로 예상된다고 했다.[^Rexxar]
yaantc는 이를 출석이 적은 시간을 이용한 소수 집단의 입법 연출로 보고, 더 정확한
제목은 “35명이 있던 본회의에서 21명이 투표해 11명이 찬성했다”가 되어야 한다고
썼다.[^yaantc]

반대 방향의 관점도 있다.
nlitened는 미국 하원이 비만인 사람에게 더 높은 세금을 허용하는 법을 통과시켰을
때 “상원에서 막힐 테니 가짜 뉴스”라고 말할 수 없다고 했다.[^nlitened]
상원에서 폐기되더라도 하원을 통과했다는 사실이 이미 큰 뉴스라는 것이다.
두 관점은 같은 사건을 서로 다른 지표로 본다.
입법 결과를 보면 이 수정안은 가능성이 낮고, 의제 설정을 보면 한 번 부결된
아이디어가 3주 만에 본회의를 통과한 것이다.

이 문서의 추론으로, 독자가 취할 행동은 사업이나 구독 결정을 바꾸는 것이 아니라
상원 심사와 최종 재정법을 확인하는 것이다.
수정안이 상원에서 삭제되면 이 논의는 끝난다.
삭제되지 않고 남으면 그때 상한 규정과 측정 방식의 모호함이 실제 쟁점이 된다.

### 상한 구조는 법인 구조를 바꾸는 유인을 만든다

상한이 프랑스 매출의 15%와 전 세계 매출의 2% 중 하나라면, 매출 구조에 따라
부담금의 한도가 달라진다.
malloryerik이 지적했듯 프랑스에서만 서비스하는 업체에는 2%가 곧 상한이
된다.[^malloryerik]
ThrustVectoring의 질문은 이 구조가 법인 분리를 유인할 수 있음을 보여
준다.[^ThrustVectoring]
이는 둘 다 수정안의 정확한 문구를 확인하지 못한 상태의 추측이므로, 문구가
정해지기 전에는 결론을 낼 수 없다.

더 일반적인 교훈은 전송량 기준 부담금에 상한을 매출 비율로 두면 상한이 사실상
매출세가 된다는 점이다.
전송량이 상한 이내인 사업자에게는 전송량 과세가 적용되고, 상한을 넘는
사업자에게는 매출세가 적용된다.
두 세금이 한 규정 안에서 섞이면 사업자는 어느 쪽 기준에 걸리는지에 따라 행동이
달라진다.
이는 이 문서의 해석이다.

### 무료 배포 자원은 이 구조에서 가장 불리하다

기사가 든 범주 중 Hugging Face, GitHub, Linux 배포판의 패치 배포는 무료로
제공되는 자원이다.
이들의 매출은 전송량에 비해 작거나 없다.
상한이 매출 비율이라면, 매출이 없는 사업자의 상한은 영이 된다는 해석이
가능하지만 수정안 본문을 확인하지 않았으므로 이는 가설이다.
반대로 상한이 적용되지 않는다면 전송량 전체에 부담금이 붙는다.

HN에서 zeograd는 이 세금이 전문 콘텐츠 제공자, 특히 상위 20개 정도의 대형 플랫폼을 겨냥하며 최종 사용자, Tor 릴레이, 대기업이 아닌 콘텐츠 제공자는 범위 밖이라고 썼다.[^zeograd]
이는 그의 주장이고 이 문서가 수정안에서 확인한 것이 아니다.
wolvoleo는 일정한 부담은 타당할 수 있으나 금액을 한두 자릿수 낮추고 무료
콘텐츠를 예외로 해야 한다고 썼다.[^wolvoleo]
기사의 목록과 zeograd의 서술 사이의 간격이 이 수정안에서 무료 배포 자원이 어떻게
처리되는지가 열린 질문임을 보여 준다.

---

[^kulturegeek]: KultureGeek, [L'Assemblée nationale adopte la taxe au gigaoctet du Parti socialiste](https://kulturegeek.fr/news-362953/lassemblee-nationale-adopte-taxe-gigaoctet-parti-socialiste), 2026-10-30

[^univers-freebox]: Univers Freebox, [Netflix, YouTube, même TF1 bientôt taxés pour leur trafic sur les réseaux des opérateurs ? Les députés adoptent un amendement malgré les critiques et doutes](https://www.universfreebox.com/article/598917/netflix-youtube-meme-tf1-bientot-taxes-pour-leur-trafic-sur-les-reseaux-des-operateurs-les-deputes-adoptent-finalement-un-amendement-qui-pourrait-rapporter-5-milliards-deuros), 2026-10-30

[^adrian_b]: <https://news.ycombinator.com/item?id=50315262>

[^Brybry]: <https://news.ycombinator.com/item?id=50315706>

[^embedding-shape]: <https://news.ycombinator.com/item?id=50317677>

[^malloryerik]: <https://news.ycombinator.com/item?id=50311514>

[^ThrustVectoring]: <https://news.ycombinator.com/item?id=50311850>

[^jonathanstrange]: <https://news.ycombinator.com/item?id=50311532>

[^Sayrus]: <https://news.ycombinator.com/item?id=50311287>

[^Rexxar]: <https://news.ycombinator.com/item?id=50312721>

[^yaantc]: <https://news.ycombinator.com/item?id=50316036>

[^nlitened]: <https://news.ycombinator.com/item?id=50315610>

[^zeograd]: <https://news.ycombinator.com/item?id=50315695>

[^wolvoleo]: <https://news.ycombinator.com/item?id=50312755>
