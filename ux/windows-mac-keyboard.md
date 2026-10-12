# Windows와 Mac의 키보드 차이: 한 코드베이스로 두 플랫폼을 지원할 때 알아야 할 것

원문: [Deeper dive: Keyboard differences between Windows and Macs – Unsung](https://unsung.aresluna.org/deeper-dive-keyboard-differences-between-windows-and-macs/)

HN 토론: <https://news.ycombinator.com/item?id=50015515> (331점, 271개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/m2ixv3/deeper_dive_keyboard_differences> (13점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35060>

## 소개

Google, Medium, Figma에서 UX 디자이너, 타이포그래퍼, 프런트엔드 개발자,
관리자로 일했고 키보드와 타이핑에 관한 책을 쓴 Marcin Wichary가 2026년 10월 8일
자신의 블로그 Unsung에 올린 글이다.
그는 여러 해 동안 Mac과 Windows의 키보드 처리 차이에서 함정과 이상한 점을 많이
배웠고, 특히 같은 코드베이스로 두 플랫폼을 함께 지원하는 웹 앱에 중요한 내용이라
한곳에 모아 두었다고 말한다.
글 첫머리에서 저자는 이 글이 참고 자료이며 재미있는 이야기는 들어 있지 않으니
지루하면 건너뛰어도 된다고 밝힌다.
블로그의 deeper dives와 reference 태그가 붙어 있다.

## 키 이름과 기호

### 같은 키, 다른 이름

| 동작                       | Windows      | Mac              |
| -------------------------- | ------------ | ---------------- |
| 커서 앞 글자 지우기        | Backspace    | ⌫ Delete         |
| 커서 뒤 글자 지우기        | Delete       | ⌦ Forward Delete |
| 본 키보드의 줄바꿈·확정 키 | ⏎ Enter      | ⏎ Return         |
| 숫자 키패드의 확정 키      | Numpad Enter | ⌤ Enter          |
| 앱이 쓰는 주 보조 키       | Ctrl         | ⌘ Command        |
| 두 번째 보조 키            | Alt          | ⌥ Option         |

그래서 플랫폼을 밝히지 않고 Delete라고 말하면 혼란스러울 수 있다고 저자는
지적한다.
Mac에서 숫자 키패드가 없는 키보드는 Fn+Return으로 Enter를 흉내 낼 수 있고,
예전에는 노트북에도 Enter 키가 따로 있었다.
대부분의 Mac 앱은 Return과 Enter를 똑같이 다룬다.
Photoshop은 Return으로 새 줄을 넣고 Enter로 확정하며 Cubase나 Pro Tools 같은
오래된 전문가용 앱도 둘을 다르게 쓰지만, 저자는 사라져 가는 전통으로 본다.
Windows에서 Fn+Enter로 Numpad Enter를 흉내 낼 수 있는지는 저자도 확신하지
못한다.
서드파티 키보드는 대체로 Backspace, Enter 같은 Windows 이름을 쓰고,
Mac 관례를 따르더라도 보조 키까지만 따른다.

### Mac은 기호, Windows는 단어

Apple은 키와 메뉴에 기호를 더 많이 쓰지만 일관되지는 않다.
⇧ Shift, ⌃ Control, ⌥ Option, ⌘ Command, ⏎ Return, ⌤ Enter, 🌐 Globe/Fn, ⇥ Tab,
⎋ Esc, ⌫ Delete, ⌦ Forward Delete, ⌧ Clear가 있고,
풀사이즈 키보드에는 ≣ Contextual Menu와 Page Up, Page Down, Home, End가 더 있다.
⎋은 메뉴에는 나오지만 키보드에는 인쇄되지 않는다.
요즘 Apple 키보드는 Page Up과 Page Down에 일반 화살표 ↑↓를,
Home과 End에 ⤒⤓를 쓰고, 그 대신 방향키는 ◀▶▲▼로 표시한다.
저자는 이를 Apple 키보드 디자이너의 이해하기 어려운 결정 중 하나로 꼽는다.
예전에는 미국 외 키보드에 기호가 더 많았지만 2026년 모델부터 모든 키보드에서
기호와 글자를 함께 쓰는 규칙이 통일되었고, 글자만 있는 키는 Esc 하나다.

Windows 키보드는 주로 단어를 쓰므로 공간이 좁으면 Ctrl, Bkspc, PrtSc, Del, PgUp,
Win 같은 줄임말이 나오고, 독일에서는 Ctrl이 Strg로 번역되기도 한다.
Windows 쪽으로 건너간 기호는 Shift의 ⇧, 미국 외 키보드의 Caps Lock 기호,
Enter의 ⏎, Backspace의 ←, Tab의 ⇥, Windows 키의 ⊞, 컨텍스트 메뉴 키의 ≣,
그리고 주로 기술적인 맥락에서 쓰는 Control의 ⌃ 정도다.
Backspace의 ←는 Mac ⌫ Delete와 다른 화살표다.
Apple이 큰 키보드에 컨텍스트 메뉴 키를 더할 무렵,
Microsoft는 그 키를 빼고 이모지 키, Office 키, Copilot 키를 차례로 넣었다는
대비도 짚는다.

### 단축키를 표기하는 방법

Windows는 메뉴에서 키 조합을 더하기 기호로 잇고, Mac은 기호를 그냥 붙여 쓴다.

| Windows      | Mac  |
| ------------ | ---- |
| Shift+A      | ⇧A   |
| Ctrl+Shift+G | ⌃⇧G  |
| Ctrl+F11     | ⌘F11 |
| Alt+Enter    | ⌥⏎   |

저자는 Chrome의 같은 메뉴를 두 플랫폼에서 나란히 보여 주고,
그러니 ⌃V가 Windows의 붙여넣기라는 식의 표현은 실제로는 쓰지 않는다고 덧붙인다.

## 보조 키와 문자 입력

### Mac에는 보조 키가 하나 더 있다

Windows의 Ctrl은 Mac의 ⌘에 대응한다.
그런데 Mac에도 Control 키가 있다.
원래 터미널 앱용이었지만 지금은 많은 GUI 앱이 Windows의 Ctrl보다 훨씬 덜 중요한
보조 키로 쓴다.
운영체제가 가져가는 Windows 키와 🌐 Globe/Fn 키를 빼면 앱이 쓸 수 있는 보조 키는
Windows가 Ctrl, Alt, Shift 셋이고 Mac은 ⌘, ⌥, ⌃, ⇧ 넷이다.
저자는 이를 숨 쉴 공간이 하나 더 있다고 표현한다.

일부 키보드는 플랫폼에 맞게 갈아 끼울 키캡을 주고,
일부는 한 키캡에 두 플랫폼의 이름을 모두 어색하게 인쇄하며,
많은 키보드는 Windows 이름만 쓴다.
저자는 Alt와 ⌥의 코드가 같고 ⌘과 ⊞의 코드가 같으므로 키캡만 바꾸는 것으로는
부족하고 키보드가 보내는 스캔 코드도 바꿔야 한다고 적는다.

### ⌥와 AltGr는 단축키가 아니라 글자 입력용이다

Mac 텍스트 필드에서는 ⌥와 글자 키를 함께 누르면 추가 문자가 나온다.
미국 영어 배열에서 ⌥Q는 œ, ⌥7은 ¶, ⌥⇧Q는 Œ, ⌥⇧7은 ‡다.
글자뿐 아니라 거의 모든 인쇄 키에 ⌥와 ⌥⇧ 조합이 숨어 있고, 일부는 데드 키이며,
배열마다 할당이 다르다.
저자는 폴란드어 배열을 예로 들어 차이가 크다는 것을 보여 주고,
영국 영어 키보드처럼 중요한 ⌥ 조합을 키에 인쇄한 실물도 있다고 소개한다.
그래서 텍스트 필드에서는 ⌥ 기반 단축키를 피하는 것이 좋다고 권한다.

Windows에는 이 기능이 없지만 미국 외 여러 배열에서 오른쪽 Alt가 AltGr로 동작해
비슷한 일을 한다.
폴란드어 키보드에서 AltGr+A는 ą, AltGr+C는 ć, AltGr+Shift+A는 Ą이고,
이런 조합이 15개 더 있다.
⌥와 다른 점은 Apple이 주는 다양한 타이포그래피 기호가 아니라 각 언어에 꼭 필요한
글자와 구두점에 쓰인다는 것이다.
그리고 레거시 이유와 AltGr 키가 없는 키보드를 위해 Ctrl+Alt 조합으로도 같은
글자를 입력할 수 있다(Ctrl+Alt+A는 ą).
따라서 Mac에서 ⌥ 단축키를 조심하듯 Windows에서는 Ctrl+Alt 단축키를 조심해야
한다.
Mac의 보조 키는 왼쪽과 오른쪽이 완전히 대칭인 반면 Windows는 Alt만 예외라는 점도
저자는 짚는다.

### 코드로 문자 입력하기와 길게 누르기

Windows는 Alt를 누른 채 숫자 키패드로 코드를 입력해 아무 문자나 넣을 수 있다.
Alt+0128은 €이고, Num Lock이 켜져 있어야 하며,
저자는 숫자 키패드 없이는 불가능하다고 본다.
Mac은 Unicode Hex Input 입력기를 추가해 전환한 뒤 ⌥20AC를 누르면 €가 나온다.
Mac은 iPhone에서 온 관례대로 키를 길게 누르면 자동 반복 대신 악센트가 붙은 문자
목록을 보여 주며, Windows에는 이 기능이 없다.

## 텍스트 필드와 이동

### Mac 텍스트 필드의 Control 단축키

Mac 앱과 웹 브라우저의 텍스트 필드는 Unix와 Linux의 표준 단축키 일부를 ⌃로
지원한다.

| 단축키 | 동작                                           |
| ------ | ---------------------------------------------- |
| ⌃A     | 줄 처음으로 이동                               |
| ⌃E     | 줄 끝으로 이동                                 |
| ⌃F     | 오른쪽(앞)으로 이동, ⌥를 함께 누르면 단어 단위 |
| ⌃B     | 왼쪽(뒤)으로 이동, ⌥를 함께 누르면 단어 단위   |
| ⌃N     | 아래 또는 다음 명령으로 이동                   |
| ⌃P     | 위 또는 이전 명령으로 이동                     |
| ⌃L     | 커서가 세로 가운데 오도록 스크롤               |
| ⌃H     | 앞 글자 삭제                                   |
| ⌃D     | 뒤 글자 삭제                                   |
| ⌃K     | 줄 끝까지 삭제(kill)                           |
| ⌃T     | 인접한 두 글자 맞바꾸기(transpose)             |
| ⌃O     | 새 줄을 넣되 커서는 옮기지 않음                |

많은 조합은 ⇧를 함께 눌러 선택을 넓힐 수 있다.
저자는 이를 아끼는 사용자가 소수지만 목소리가 크다고 적는다.
Windows는 지금도 Shift+Delete로 잘라내기, Ctrl+Insert로 복사,
Shift+Insert로 붙여넣기를 지원하는데, 얼마나 쓰이는지는 모르겠다고 한다.

### 방향키, Home/End, Page Up/Down

Mac의 단순 입력 필드에서 ↑와 ↓는 처음과 끝으로 가며 ⌘←→와 같다.
이것은 명령 기록이나 자동 완성 팝업과 자주 충돌한다.
저자에 따르면 Windows에는 이 관례가 없고 Home과 End가 같은 일을 한다.

| 키              | Windows                                           | Mac                                                                 |
| --------------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| PgUp/PgDn       | 텍스트 커서를 한 화면 위아래로 옮김               | 화면만 스크롤하고 커서는 그대로 둠(스크롤바 빈 곳을 누른 것과 비슷) |
| Home/End (보기) | 맨 위나 아래로 스크롤하고 커서가 있으면 함께 옮김 | 처음이나 끝으로 스크롤하되 커서는 옮기지 않음                       |
| Home/End (입력) | 커서를 입력 필드의 처음이나 끝으로 옮김           | 아무 일도 하지 않음, 대신 ⌘←→를 씀                                  |

두 플랫폼 모두 Fn+↑↓가 PgUp/PgDn, Fn+←→가 Home/End다.
저자는 Mac에서 ↑↓가 이미 PgUp/PgDn 기호로 쓰이는 상황에서 이 설명이 얼마나
헷갈리는지 묻는다.

### Tab과 메뉴 접근

Tab과 Shift+Tab으로 UI 요소 사이를 오가는 동작도 다르다.
Windows는 모든 상호작용 요소를 돌지만, Mac은 입력 필드처럼 키보드가 있어야
조작할 수 있는 요소로만 간다.
System Settings에서 Windows처럼 동작하게 바꾸는 옵션이 있지만 모든 곳에서 잘
지원되지는 않는다.
Windows에는 Alt와 글자 키로 메뉴와 보이는 컨트롤에 접근하는 전통이 있는데,
예전만큼 일관되지는 않다.

## 단축키 관례와 예약된 키

### 서로 다른 관례

| 동작      | Windows                                         | Mac |
| --------- | ----------------------------------------------- | --- |
| 다시 실행 | Ctrl+Y                                          | ⌘⇧Z |
| 새로 고침 | F5, 브라우저는 Ctrl+R도 지원하며 기본이 되는 중 | ⌘R  |

Windows에서는 전통적으로 운영체제와 앱이 기능 키를 단축키로 가져갔다.
Alt+F4로 앱 닫기, F1 도움말, F11 창 최대화,
브라우저의 F12 개발자 도구가 그 예다.
Mac 앱은 전통적으로 기능 키에 손대지 않고 사용자가 쓰도록 남겨 두었다.
다만 운영체제가 ⌃와 기능 키 조합 일부를 손쉬운 사용 기능에 쓰고,
요즘은 기능 키를 쓰는 앱도 가끔 보인다.
Windows 키보드는 F12까지지만 일부 Mac 키보드는 PC의 특수 키 세 개와 Num Lock,
Caps Lock, Scroll Lock 자리까지 가져가 F19까지 둔다.

### 운영체제와 브라우저가 먼저 가져가는 키

Windows 키는 운영체제 전용이고 Mac의 🌐 Fn/Globe 키도 마찬가지다.
저자는 사용자가 🌐 단축키를 만들 수 있는 곳을 하나 찾았지만 의도된 것인지는
확신하지 못한다고 덧붙인다.
그 밖에도 Mac의 ⌘⇥와 ⌘M, Windows의 Alt+Tab과 Ctrl+Shift+Escape처럼 사실상 쓸 수
없는 조합이 많고, 저자는 Apple과 Microsoft의 공식 단축키 목록을 참고하라고
권한다.

웹 앱은 운영체제뿐 아니라 브라우저와도 단축키를 다툰다.
⌘S나 ⌘P는 대개 가져올 수 있지만 브라우저와 플랫폼에 따라 손댈 수 없는 키가 있다.
Mac의 어떤 브라우저도 웹사이트가 ⌘Q, ⌘W, ⌘T를 가져가게 두지 않고, Safari는 ⌘R을,
Arc는 ⌘⇧C를 내주지 않는다.
저자는 이것이 완전한 목록이 아니라고 밝힌다.

### 잘 쓰이지 않는 키

100개가 넘는 키를 가진 Windows 키보드에는 덮어쓰기 입력에 아직 쓰이는 Insert,
이제 스크린숏에 쓰이는 Print Screen, Num Lock, Scroll Lock, Pause/Break가 있다.
Mac에는 거의 쓰이지 않다가 사라진 Help,
오른쪽 클릭과 같은 메뉴를 여는 ≣ Contextual Menu,
결정적인 백스페이스라 할 수 있지만 요즘은 Delete와 거의 다르지 않은 ⌧ Clear가
있다.
Mac에는 숫자 키패드의 방향키나 그것을 켜는 Num Lock이 한 번도 없었다.
반대로 1980년대에서 2000년대 사이 일부 Apple 키보드는
PC 호환성을 얻으려고 PC 쪽 이름을 인쇄했다.
Apple Extended Keyboard에는 Insert, Del, Print Screen, Scroll Lock, Pause,
Num Lock, Alt가 적혀 있었다.

## 구현하기

원문은 웹 앱을 염두에 두고 쓰였지만 코드는 담고 있지 않다.
아래는 원문의 권고를 브라우저의 `KeyboardEvent`로 옮겨 본 예시이며,
원문이 아니라 이 노트가 덧붙인 것이다.
직접 여러 브라우저에서 실행해 확인하지는 않았다.

```javascript
// 플랫폼 판별: userAgentData가 없으면 platform 문자열로 대신한다.
function isMac() {
  const p = navigator.userAgentData?.platform ?? navigator.platform ?? "";
  return /mac/i.test(p);
}

// 앱의 "주 보조 키": Mac은 ⌘(metaKey), 그 밖은 Ctrl(ctrlKey).
function hasPrimaryModifier(event) {
  return isMac() ? event.metaKey : event.ctrlKey;
}

// 글자 입력용 조합인지 판별한다.
// Mac의 ⌥, Windows의 AltGr과 Ctrl+Alt는 언어에 따라 글자를 만든다.
function mayProduceCharacter(event) {
  if (event.isComposing) return true; // IME 조합 중에는 손대지 않는다
  if (event.getModifierState("AltGraph")) return true;
  if (isMac()) return event.altKey && !event.metaKey && !event.ctrlKey;
  return event.ctrlKey && event.altKey;
}

function isEditable(target) {
  return target.isContentEditable ||
    ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName);
}

document.addEventListener("keydown", (event) => {
  // 텍스트 필드에서는 글자가 될 수 있는 조합을 가로채지 않는다.
  if (isEditable(event.target) && mayProduceCharacter(event)) return;

  // 다시 실행: Mac은 ⌘⇧Z, Windows는 Ctrl+Y와 Ctrl+Shift+Z를 함께 받는다.
  const key = event.key.toLowerCase();
  const redo = isMac()
    ? event.metaKey && event.shiftKey && key === "z"
    : event.ctrlKey && (key === "y" || (event.shiftKey && key === "z"));
  if (redo) {
    event.preventDefault();
    console.log("redo");
    return;
  }

  // 앞 글자 지우기와 항목 삭제를 혼동하지 않는다.
  // Mac의 Delete 키는 event.key가 "Backspace"로 들어온다.
  if (!isEditable(event.target) && event.key === "Delete") {
    console.log("delete selected item");
  }
});
```

`event.key`는 배열과 보조 키를 반영한 결과 글자이고,
`event.code`는 키의 물리적 위치다.
⌥나 AltGr 조합을 다룰 때 `event.key`는 이미 ą나 œ 같은 결과 글자로 바뀌어 있을
수 있으므로, 단축키를 위치로 정의할지 글자로 정의할지 먼저 정해야 한다.
메뉴에 단축키를 표시할 때는 Windows에서 `Ctrl+Shift+Z`,
Mac에서 `⌘⇧Z`처럼 원문이 정리한 표기 관례를 따라 플랫폼별로 문자열을 따로
만들어야 한다.

## 비평

### 키캡과 스캔 코드 대목은 위치와 이름을 섞는다

저자는 키캡만 바꾸면 부족하고 스캔 코드도 바꿔야 한다고 설명한다.
HN의 dotancohen은 Alt와 ⌥, ⌘과 ⊞는 키보드에서 같은 위치에 있으므로
키캡만 바꿔도 충분해 보인다고 반박했다[^dotancohen].
olyjohn도 PC 키보드를 Mac에 꽂으면 Windows 키가 ⌘이 되고 Alt가 ⌥이 되는 것이
기본이라며 글에 실린 예시 키보드가 틀렸다고 지적했다[^olyjohn].
이에 rahimnathwani는 Mac에 외장 PC 키보드를 꽂으면 거의 모두가 시스템 설정에서
Command와 Option을 맞바꾸지 않느냐고 답했다[^rahimnathwani].

두 반박은 서로 다른 문제를 말한다.
키 자리 기준으로 보면 같은 코드가 같은 자리에서 나오므로 키캡만 바꿔도 된다.
그러나 Mac 사용자는 ⌘을 스페이스 바 바로 옆에서 찾으므로,
그 자리에 Alt가 있는 PC 키보드에서는 키캡이 아니라 코드를 바꿔야 손가락 위치가
맞는다.
원문은 사용자가 기대하는 위치를 기준으로 썼지만 그 전제를 밝히지 않아,
위치와 이름 중 무엇을 맞추는지가 흐려졌다.

### Windows에 없다는 몇몇 단정은 더 확인이 필요하다

원문은 Mac 입력 필드에서 ↑↓가 처음과 끝으로 가는 관례가 Windows에는 없다고 썼다.
notpushkin은 자신이 기억하기로 Windows와 Linux에서도 그렇게 동작했다고
반박했다[^notpushkin].
같은 댓글에서 그는 Fn+↑↓가 PgUp/PgDn이라는 설명도 제조사에 따라 크게 다르고,
실제 Home/End 키가 있던 ThinkPad T420 시대 모델은 그 조합을 미디어 키에 썼다고
지적했다.

이런 차이는 사소해 보이지만 참고 자료라는 글의 성격을 생각하면 무게가 있다.
저자 스스로도 Fn+Enter, Alt 코드 입력, 🌐 단축키 같은 대목에서 확신이 없다고
밝혔다.
글을 단축키 설계의 근거로 쓰려면 각 항목을 대상 플랫폼과 기기에서 직접 확인해야
하고, 그 확인이 필요한 항목이 어디인지를 원문이 스스로 표시해 두었다고 읽는 편이
맞다.

### 웹 앱을 위한 글이지만 구현의 다음 단계는 비어 있다

저자는 웹 앱을 글의 주된 독자로 삼았지만,
정리는 사용자 관점의 동작 차이에서 멈춘다.
웹 앱이 실제로 받는 이벤트에서 Mac의 Delete가 무엇으로 들어오는지,
AltGr이 Ctrl과 Alt로 함께 보고되는지, IME 조합 중의 키 입력을 어떻게 걸러야
하는지는 다루지 않는다.
HN의 miki123211은 이 빈자리를 길게 메웠다[^miki123211].
AltGr=Ctrl+Alt 방식을 쓰는 Windows 배열에서는 오른쪽 Alt가 말 그대로 Ctrl+Alt로
매핑되어 왼쪽 Alt처럼 메뉴 막대를 열지 못한다고 했다.
Mac에서는 복사, 붙여넣기, 종료, 창 닫기를 메뉴 항목으로 구현하고 키 입력을 직접
처리하지 말라고 권했으며, 중국어와 일본어 사용자를 위한 IME 통합이 많은
프레임워크에서 빠져 있다고 지적했다.
Mac에서는 기능 키가 기본으로 미디어 키로 동작하고 Touch Bar 모델에는 기능 키가
아예 없으니 복잡한 단축키를 기능 키에 걸지 말라는 조언도 더했다.

## 함정

- Mac 사용자가 말하는 Delete는 Windows의 Backspace다. anilakar는 한 상용 프로젝트 관리 도구가 이 키를 항목 삭제에 써서, 텍스트 상자를 놓친 순간 작업 중이던 항목 전체가 지워졌다고 적었다[^anilakar].
- 텍스트 필드에서 ⌥나 Ctrl+Alt 단축키를 쓰면 어떤 언어 사용자에게는 글자 입력을 막는 셈이다. 미국 영어 배열에서만 시험하면 발견되지 않는다.
- 사용자의 손 기억은 플랫폼을 넘어 따라온다. slhck는 독일어 QWERTZ 배열에서 Mac에 익숙한 손으로 Windows에서 @를 치려다 Windows+L을 눌러 화면을 잠그고, 반대로 Windows 사용자는 Mac에서 AltGr+Q를 누르려다 앞에 떠 있는 앱을 종료하기 쉽다고 적었다[^slhck].
- 모든 앱이 같은 단축키를 쓴다고 가정하면 안 된다. pta2002는 포르투갈어로 설정된 Windows에서 메모장과 Office가 Ctrl+A를 Ctrl+T(Tudo)로, Ctrl+S를 Ctrl+G(Guardar)로 번역해 Microsoft 앱만 다른 단축키를 쓴다고 적었다[^pta2002].
- Shift+방향키로 선택을 넓히는 동작도 다르다. danhau는 Mac에서 선택이 늘어날지 줄어들지 동전 던지기 같다고 했고[^danhau], tpmoney는 Mac이 첫 번째 누름의 방향으로 선택의 기준점을 정한 뒤 반대 방향은 줄이는 방식이라고 설명했다[^tpmoney]. 원문은 이 차이를 다루지 않는다.
- 브라우저 관례가 운영체제 관례를 대체하고 있다. muststopmyths는 Windows MDI 앱에서 Ctrl+F4가 문서 창 하나를, Alt+F4가 앱 전체를 닫는 관례가 있었지만, 이제는 모든 앱이 운영체제가 아니라 웹 브라우저의 UI 관례를 따르는 것 같다고 적었다[^muststopmyths].
- 키를 재매핑한 사용자는 메뉴에 표시된 단축키와 실제로 눌러야 할 키가 어긋난다. grujicd는 Mac 키보드를 Windows처럼 바꾼 뒤 메뉴의 단축키를 볼 때마다 무엇을 눌러야 할지 몰라 단축키를 덜 쓰게 되었다며 이것을 새는 추상화라고 불렀다[^grujicd].

## 체크리스트

- 앱의 주 보조 키를 Mac에서는 ⌘, 그 밖에서는 Ctrl로 나누어 처리하는가?
- 텍스트 필드에서 Mac의 ⌥ 조합과 Windows의 AltGr, Ctrl+Alt 조합을 단축키로 가로채지 않는가?
- IME 조합 중인 키 입력을 단축키 처리에서 제외하는가?
- Mac의 Delete(Backspace) 키 하나로 항목 전체가 지워지는 경로가 없는가?
- 다시 실행을 Mac에서는 ⌘⇧Z, Windows에서는 Ctrl+Y로 받는가?
- ⌘Q, ⌘W, ⌘T처럼 브라우저가 내주지 않는 키에 기능을 걸지 않았는가?
- 메뉴와 툴팁의 단축키 표기를 Windows는 `Ctrl+Shift+G`, Mac은 `⌃⇧G`처럼 플랫폼별로 만드는가?
- 입력 필드에서 ↑↓를 명령 기록이나 자동 완성에 쓸 때, 처음과 끝으로 가는 Mac 기본 동작과 충돌하는 경우를 시험했는가?
- 미국 영어 외에 폴란드어, 독일어 같은 배열에서 단축키를 시험했는가?

## 기억할 원칙

### 키보드는 단축키 장치이기 전에 글자 입력 장치다

원문에서 가장 실용적인 경고는 ⌥와 AltGr에 관한 대목이다.
단축키를 설계하는 사람은 보조 키 조합을 빈 공간으로 보기 쉽지만,
어떤 언어 사용자에게 그 조합은 자기 이름의 글자를 치는 유일한 방법이다.
미국 영어 배열에서 아무 일도 하지 않는 조합이 다른 배열에서는 꼭 필요한 글자일
수 있다.
그래서 단축키를 고를 때는 그 조합이 비어 있는지보다,
누구에게 비어 있는지를 먼저 물어야 한다.

### Ctrl을 Command로 바꾸는 것은 시작일 뿐이다

두 플랫폼의 차이는 키 하나를 맞바꾸는 대응표로 끝나지 않는다.
키 이름, 표기, 보조 키의 개수, 이동 키의 의미,
운영체제와 브라우저가 먼저 가져가는 키가 모두 다르고,
사용자는 그 위에 각자의 재매핑과 손 기억을 얹는다.
한 코드베이스로 두 플랫폼을 지원한다면 키보드 처리를 플랫폼별 관례를 따르는
별도의 층으로 두고, 그 층을 실제 기기와 배열에서 시험해야 한다.

---

[^dotancohen]: <https://news.ycombinator.com/item?id=50026762>

[^olyjohn]: <https://news.ycombinator.com/item?id=50015597>

[^rahimnathwani]: <https://news.ycombinator.com/item?id=50015728>

[^notpushkin]: <https://news.ycombinator.com/item?id=50018095>

[^miki123211]: <https://news.ycombinator.com/item?id=50016586>

[^anilakar]: <https://news.ycombinator.com/item?id=50016304>

[^slhck]: <https://news.ycombinator.com/item?id=50020184>

[^pta2002]: <https://news.ycombinator.com/item?id=50017101>

[^danhau]: <https://news.ycombinator.com/item?id=50018172>

[^tpmoney]: <https://news.ycombinator.com/item?id=50023578>

[^muststopmyths]: <https://news.ycombinator.com/item?id=50019898>

[^grujicd]: <https://news.ycombinator.com/item?id=50017775>
