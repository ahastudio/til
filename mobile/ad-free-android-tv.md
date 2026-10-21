# 광고 없는 Android TV: 런처와 YouTube 앱을 바꾸고 ADB로 정리하는 방법

원문: [An ad-free Android TV — Cretezy](https://cretezy.com/2026/ad-free-android-tv)

HN 토론: <https://news.ycombinator.com/item?id=50158942> (389점, 167개 댓글)

GN 토론: <https://news.hada.io/topic?id=35697>

## 소개

Cretezy는 2026년 10월 19일 글에서 Android TV의 광고를 없애는 설정을 정리했다.
문제로 든 것은 Google TV 홈 화면 맨 위의 큰 배너다.
Google이 다음에 볼 것으로 밀어 주는 콘텐츠를 보여 주며,
쓰지 않는 앱에서 온 것도 많다.
앱 전용(Apps only) 모드가 홈 화면을 앱만 남기도록 되어 있지만
배너는 남고 끄는 설정도 없다고 한다.

그가 고른 구성은 네 가지다.

| 도구                | 하는 일                                                          |
| ------------------- | ---------------------------------------------------------------- |
| Projectivy Launcher | 홈 화면을 대체해 앱만 보여 주고 많은 부분을 꾸밀 수 있다         |
| SmartTube           | YouTube 앱을 대체한다. 광고가 없고 SponsorBlock이 내장되어 있다  |
| Wholphin            | Jellyfin 클라이언트. 인터페이스와 설정 항목이 마음에 든다고 한다 |
| Button Mapper       | 리모컨의 YouTube 버튼이 SmartTube를 열게 바꾼다                  |

그는 이 구성을 Google TV가 든 Chromecast 두 대와 Hisense TV에 적용했고,
대부분의 Android TV 기기에서 될 것이라고 쓴다.
YouTube Premium은 제작자를 후원하려고
계속 내면서도 SmartTube를 훨씬 선호한다고 밝혔다.
글은 10월 20일 HN의 반응을 받아 Pi-hole과 Private DNS 방법,
런처와 Jellyfin 클라이언트의 대안,
추가 정리용 목록을 덧붙였다.

이 문서는 글의 순서를 따르되,
각 단계가 무엇을 바꾸는지와 되돌리는 방법을 함께 적는다.

## 동작 방식

이 설정의 핵심은 기기에서 Google의 홈 화면
앱을 쓰지 못하게 하고 다른 앱을 홈으로 지정하는 것이다.
Projectivy에는 현재 런처를 덮어쓰는 옵션이 있지만,
그렇게 하면 홈 키를 눌렀을 때 기본 홈 화면이 잠깐 번쩍인 뒤에 바뀐다.
그래서 글은 Projectivy를 홈 앱으로 지정하고,
기본 런처와 그것을 복원하는 패키지를 비활성화하는 방식을 쓴다.

여기에 모든 것이 ADB(Android Debug Bridge)로 이루어진다.
무선 디버깅으로 기기에 연결하고,
앱 설치와 패키지 비활성화와 접근성 서비스 설정을 명령으로 한다.
YouTube 공식 앱은 지우고,
리모컨의 YouTube 버튼은 Button Mapper가 SmartTube로 연결한다.

## 설정하기

### ADB 연결

개발자 옵션은 설정, 시스템, 정보에서 Android TV OS 빌드를 일곱 번 눌러 켠다.
그 안에서 무선 디버깅을 켜고 페어링 코드로 기기를 연결한다.

```bash
adb pair <ip>:<pairing-port> <code>
adb mdns services          # 연결 포트를 찾는다
adb connect <ip>:<connect-port>
D=<ip>:<connect-port>      # 아래 명령에서 쓸 변수
```

무선 디버깅은 Wi-Fi에서만 되므로, 글쓴이의 Hisense TV처럼 지원하지 않는 기기는
USB 디버깅을 켜고 `adb connect <ip>:5555`로 연결한다.

### 앱 설치

Projectivy와 Wholphin과 Button Mapper는 Play 스토어에 있다.
ADB로 Play 스토어에서 직접 설치할 수는 없지만
각 앱의 페이지를 TV에서 열게 할 수는 있다.

```bash
for p in com.spocky.projengmenu com.github.damontecres.wholphin flar2.homebutton; do
  adb -s $D shell am start -a android.intent.action.VIEW -d "market://details?id=$p"
  read -p "설치가 끝나면 Enter를 누르세요..."
done
```

SmartTube는 Play 스토어에 없어서 GitHub의 최신 릴리스에서 APK를 받아 설치한다.

```bash
curl -L -o smarttube.apk "$(curl -s https://api.github.com/repos/yuliskov/SmartTube/releases/latest \
  | grep -o '"browser_download_url": *"[^"]*_universal\.apk"' | cut -d'"' -f4)"
adb -s $D install smarttube.apk
```

이 문서가 확인한 바로는 이 저장소의 최신 릴리스(32.68)에
`_universal.apk` 자산이 실제로 있어서 명령의 패턴이 맞다.[^smarttube]
TV에서 Downloader 앱으로 직접 받아 설치하는 방법도 있다.

### 런처 교체

```bash
adb -s $D shell cmd package set-home-activity com.spocky.projengmenu/.ui.home.MainActivity
adb -s $D shell pm disable-user --user 0 com.google.android.apps.tv.launcherx
adb -s $D shell pm disable-user --user 0 com.google.android.tungsten.setupwraith
```

순서가 중요하다. 홈 앱을 먼저 지정해야 한다.
기기에 따라 `setupwraith`를 비활성화하면
저장된 Wi-Fi 네트워크를 잊어버릴 수 있으므로
다시 연결할 수 있게 리모컨을 가까이 둔다.
TV에서는 기본 런처가 HDMI 입력 전환을 맡을 수 있으니 바꾼 뒤에 확인해야 한다.

### YouTube 교체와 리모컨 연결

SmartTube를 설정한 뒤에 공식 앱을 지운다.

```bash
adb -s $D uninstall com.google.android.youtube.tv
# 펌웨어에 내장되어 DELETE_FAILED_INTERNAL_ERROR가 나면
adb -s $D shell pm uninstall --user 0 com.google.android.youtube.tv
```

Button Mapper와 Projectivy는 접근성 서비스가 켜져 있어야 한다.
아래 명령은 목록 전체를 바꾸므로 먼저 현재 값을 확인해 쓰던 것을 남겨야 한다.

```bash
adb -s $D shell settings get secure enabled_accessibility_services   # 먼저 확인
adb -s $D shell settings put secure enabled_accessibility_services \
  'flar2.homebutton/a.i:com.spocky.projengmenu/com.spocky.projengmenu.services.ProjectivyAccessibilityService'
adb -s $D shell settings put secure accessibility_enabled 1
```

Android가 접근성 서비스를 꺼 버리는 일이 있으므로,
Button Mapper에 `WRITE_SECURE_SETTINGS`를 주어 스스로 다시 켜게 하고
배터리 최적화에서 제외해 반응을 유지한다.

```bash
adb -s $D shell pm grant flar2.homebutton android.permission.WRITE_SECURE_SETTINGS
adb -s $D shell dumpsys deviceidle whitelist +flar2.homebutton
```

그다음 Button Mapper 앱에서 YouTube 버튼을 SmartTube에 연결한다.

### 정리

```bash
# 애니메이션을 0.75배속으로 줄여 더 빠르게 느껴지게 한다
for k in window_animation_scale transition_animation_scale animator_duration_scale; do
  adb -s $D shell settings put global $k 0.75
done

# 쓰지 않을 Google 앱과 서비스를 비활성화한다
for p in com.google.android.videos com.google.android.play.games \
  com.google.android.youtube.tvmusic com.google.android.tvrecommendations \
  com.google.android.feedback com.google.android.partnersetup; do
  adb -s $D shell pm disable-user --user 0 $p
done
```

쓰는 앱은 목록에서 빼고, 기기에 없는 패키지의 오류는 무시한다.
더 많이 덜어 내려면 cleanyourtv에 제조사 앱과 광고
서비스와 원격 측정까지 다룬 TV별 목록이 있다고 글은 소개한다.
TV라면 화면 설정에서 Filmmaker Mode 같은 중립 모드로 바꾸고
움직임 보정과 잡음 제거와 동적 대비를 끄라는 팁도 있다.

## 네트워크 차원의 차단

기본 런처를 그대로 쓰고 싶다면
`androidtvwatsonfe-pa.googleapis.com`을 Pi-hole이나 공유기 DNS에서 막으면
배너가 숨겨진다고 글은 쓴다.
다만 글은 이것을 알려진 바로는이라는 단서를 붙여 적었다.
장치를 다시 시작하거나 런처의 캐시를 지워야 적용될 수 있다.
HN의 nullify88도 같은 도메인을 로컬 DNS에서 127.0.0.1로 돌렸더니
Nvidia Shield의 Android 11에서 기본 런처의 광고가 사라졌다고 적었다.[^nullify88]

Pi-hole이 없다면 ADB가 연결된 상태에서
TV의 Private DNS를 광고 차단 DNS로 지정할 수 있다.

```bash
adb -s $D shell settings put global private_dns_mode hostname
adb -s $D shell settings put global private_dns_specifier dns.adguard-dns.com
```

DNS 차단은 광고와 추적 도메인을 기기 전체에서 막지만,
광고가 영상과 같은 도메인에서 오면 걸러 내지 못한다는 한계가 있다.
이는 이 문서의 설명이며 글이 말한 것은 아니다.

## 트레이드오프

### 시스템 앱을 끄면 같이 꺼지는 기능이 있다

기본 런처와 설정 마법사 패키지를 비활성화하면 홈 화면의 배너뿐 아니라
그 패키지들이 하던 일도 사라진다.
글이 직접 경고하는 것이 HDMI 입력 전환과 Wi-Fi 설정 유실이다.
HN의 celsoazevedo는 올해 초 비슷하게 설정했다가
끈 패키지 가운데 하나가 Chromecast 기능을 깨뜨려 결국 전부 원래대로 되돌렸다고
적었다.
다른 기기에서 영상을 띄우지 않는다면 문제가 없다는 단서도 붙였다.[^celsoazevedo]
어느 패키지가 원인인지는 댓글에 나오지 않는다.
따라서 글의 정리 단계를 적용한 뒤에는 쓰는 기능을 하나씩 시험해야 한다.

글은 모든 것이 `pm enable <package>`로 되돌려진다고 말한다.
YouTube만은 `cmd package install-existing`을 쓴다.
그러나 되돌릴 수 있는 것은 패키지 상태이지,
이미 일어난 설정 변경의 결과가 아니다.
Wi-Fi를 잊었다면 다시 입력해야 한다.

### 서드파티 APK와 높은 권한이 신뢰를 요구한다

SmartTube는 GitHub의 서드파티 앱이다.
이 문서가 본 저장소는 MIT 라이선스이고 별이 3만 5천 개 남짓이다.[^smarttube]
그래도 Play 스토어를 거치지 않으므로 검증 절차는 사용자 몫이고,
글의 설치 명령은 최신 릴리스를 그대로 받아 설치할 뿐 해시를 확인하지 않는다.
이 글의 설치 명령이 가져오는 릴리스는 이 문서를 쓴 날 갱신된 것이었으므로,
받은 파일이 믿을 만한지는 릴리스 페이지와 서명을 확인하는 편이 안전하다.

Button Mapper에 `WRITE_SECURE_SETTINGS`를 주는 것도 편의와 권한의 교환이다.
이 권한이 있으면 앱이 보안 설정을 스스로 바꿀 수 있어서
접근성 서비스를 되살릴 수 있지만,
앱이 침해되면 영향도 커진다.
글은 작업이 끝나면 ADB 디버깅을 꺼서
열린 포트로 다른 기기가 접속하지 못하게 하라고 권한다.

### AI 에이전트에게 맡기라는 권고

글에는 이 문서를 AI 에이전트에게 주고 설정을 안내받으라는 팁이 있다.
에이전트가 기기에 맞게 ADB 명령을 바꾸고 실행해 줄 수 있고,
승인하기 전에 각 명령을 검토하라는 단서가 붙는다.
HN의 netsharc은 이를 쉘 스크립트를 내려받아
바로 실행하는 방식에 빗대 농담했다.[^netsharc]
이 설정의 명령은 모두 시스템 패키지를 끄거나 권한을 주는 것이어서
단서의 검토 부분이 실제로는 가장 중요하다.

## 함정

- 접근성 서비스 설정은 목록을 통째로 바꾼다. 먼저
`settings get secure enabled_accessibility_services`로
현재 값을 확인해 남겨야 한다.
- 홈 앱을 지정하기 전에 기본 런처를 끄면
홈 화면이 사라진 채로 남을 수 있다. 글이 순서가 중요하다고 강조한 이유다.
- `dumpsys deviceidle whitelist`가 재부팅 뒤에도 유지되는지는
글이 말하지 않았다. 반응이 느려지면 다시 확인해야 한다.
- 기기 제조사와 Android 버전에 따라 패키지 이름이 다를 수
있다. 글의 목록은 Chromecast 두 대와 Hisense TV에서 쓴 것이다.
- 펌웨어 업데이트가 비활성화한 패키지를
되살리는지는 글에도 댓글에도 나오지 않았다.

## 체크리스트

- 변경 전에 쓰는 앱과 기능(HDMI 전환,
Chromecast 송출, 음성 검색)을 적어 두었는가
- 홈 앱 지정을 기본 런처 비활성화보다 먼저 했는가
- 접근성 서비스의 현재 목록을 확인하고 남겨야 할 항목을 포함했는가
- SmartTube APK의 출처와 릴리스를 확인했는가
- 비활성화한 패키지마다 되돌리는 명령을 기록해 두었는가
- 리모컨이 가까이 있는가(Wi-Fi 설정이 사라질 수 있다)
- 작업이 끝나고 무선 디버깅이나 USB 디버깅을 껐는가

## 기억할 원칙

### 광고를 없애는 일은 소유한 기기의 구성 요소를 하나씩 바꾸는 일이다

이 설정이 되는 근거는 TV가 일반 컴퓨터처럼 앱 단위로 교체할 수 있다는 점이다.
HN에서 aceazzameen은 같은 구성에 NetGuard를 더해 Google Play 접속을 아예 막고
앱을 갱신할 때만 잠깐 열어 둔다고 했다.[^aceazzameen]
이 방식은 광고뿐 아니라 갱신도 막으므로 보안 패치를 받지 못한다는 대가가 있다.
각 구성 요소가 광고 외에 무엇을 하는지 알아야 무엇을 잃는지가 보인다.

### 가장 확실한 방법은 처음부터 광고 없는 기기를 고르는 것이다

HN의 상당수 댓글은 이 설정 대신 스마트
기능이 없는 TV나 별도의 셋톱 기기를 권했다.
theshrike79는 인터넷에 연결하지 않은 LG OLED와 Apple TV를 권했고,[^theshrike79]
giancarlostoro는 단순한 TV를 팔았으면 좋겠다고 썼다.[^giancarlostoro]
이 선택은 설정의 수고를 없애지만 기기 값과 선택지가 달라진다.
Android TV를 이미 가진 사람에게는 이 글의 설정이 비용이 가장 적은 길이고,
새로 사는 사람에게는 처음부터 고르는 것이 낫다.

---

[^smarttube]: GitHub, [SmartTube](https://github.com/yuliskov/SmartTube)

[^nullify88]: <https://news.ycombinator.com/item?id=50163989>

[^celsoazevedo]: <https://news.ycombinator.com/item?id=50167838>

[^netsharc]: <https://news.ycombinator.com/item?id=50159939>

[^aceazzameen]: <https://news.ycombinator.com/item?id=50161241>

[^theshrike79]: <https://news.ycombinator.com/item?id=50163262>

[^giancarlostoro]: <https://news.ycombinator.com/item?id=50160377>
