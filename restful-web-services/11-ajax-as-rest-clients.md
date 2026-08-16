# 11장 REST 클라이언트로서의 Ajax 애플리케이션

《RESTful Web Services》(Leonard Richardson, Sam Ruby, O'Reilly 2007) 11장 정리.

## 개요

저자는 Ajax를 다소 도발적으로 정의합니다.
“Ajax 애플리케이션이란 웹 브라우저 안에서 실행되는 웹 서비스 클라이언트다.”

이 정의를 기준으로 삼으면 무엇이 Ajax이고 무엇이 아닌지 쉽게 구별됩니다.
브라우저 안에서 도는 자바스크립트 폼 검증기나 플래시 그래픽 데모는 프로그래밍 방식으로 HTTP 요청을 보내지 않으므로 Ajax가 아닙니다.
반대로 명령줄에서 도는 독립 실행형 클라이언트는 웹 서비스 클라이언트이긴 하지만 브라우저 안에서 실행되지 않으므로 역시 Ajax가 아닙니다.

Gmail은 누구나 Ajax라고 인정하는 사례입니다.
로그인하면 브라우저가 배경에서 mail.google.com의 웹 서비스에 요청을 보내고, 받은 데이터로 현재 페이지를 갱신하는 것을 확인할 수 있습니다.
이것이 바로 웹 서비스 클라이언트가 하는 일입니다.
Gmail의 웹 서비스에는 공개된 이름이 없고 Gmail 페이지 외의 클라이언트를 위해 만들어지지도 않았지만, 그럼에도 엄연한 웹 서비스입니다.
libgmail 같은 라이브러리가 비공식 non-Ajax 클라이언트로 이 서비스에 접근한다는 사실이 그 증거입니다.
웹에 올라와 있다면 그것은 웹 서비스입니다.

이 장은 2장에서 다룬 클라이언트 프로그래밍을 이어받아, 브라우저 환경에서 실행되는 웹 서비스 클라이언트의 특별한 능력과 요구사항에 집중합니다.
자바스크립트의 XMLHttpRequest 클래스와 브라우저의 DOM을 다루고, 보안 설정이 어떤 클라이언트를 브라우저에서 실행할 수 있는지를 어떻게 좌우하는지 살펴봅니다.

## AJAX에서 Ajax로

원래 AJAX는 Asynchronous JavaScript And XML(비동기 자바스크립트와 XML)의 두문자어였습니다.
그러나 이 두문자어는 폐기되었고 지금은 그냥 Ajax라는 하나의 단어가 되었습니다.
프로그래머들이 갑자기 두문자어를 싫어하게 된 것이 아니라, 그 두문자어가 말하는 내용이 반드시 참은 아니었기 때문입니다.
Ajax는 자바스크립트나 XML을 꼭 필요로 하지 않는 하나의 아키텍처 스타일입니다.

AJAX의 JavaScript는 실제로는 HTTP 요청을 보내는 브라우저 측 언어라면 무엇이든 가리킵니다.
보통은 자바스크립트지만, 브라우저가 해석할 수 있는 언어라면 무엇이든 될 수 있습니다.
플래시 안에서 도는 ActionScript, 애플릿 안에서 도는 Java, 인터넷 익스플로러의 VBScript 같은 브라우저 전용 언어도 가능합니다.

AJAX의 XML은 실제로는 웹 서비스가 보내는 표현 형식이라면 무엇이든 가리킵니다.
브라우저 측이 이해할 수 있는 형식이라면 무엇이든 됩니다.
보통은 XML인데, 브라우저가 파싱하기 쉽고 웹 서비스가 XML 표현을 즐겨 제공하기 때문입니다.
그러나 JSON도 매우 흔하며, HTML이나 평문, 이미지 파일처럼 브라우저가 처리하거나 브라우저 측 스크립트가 파싱할 수 있는 것이라면 무엇이든 될 수 있습니다.

그래서 AJAX 해커들은 매번 “JavaScript가 꼭 자바스크립트를 뜻하는 것은 아니고 XML이 XML이 아닐 수도 있다”고 설명하는 대신 그냥 Ajax 해커가 되기로 했습니다.
저자가 이 책에서 Ajax를 이야기할 때 주로 자바스크립트와 XML로 설명하지만, 그것은 특정 기술이 아니라 하나의 애플리케이션 아키텍처를 이야기하는 것입니다.

## Ajax 아키텍처

Ajax 아키텍처는 대략 다음과 같이 동작합니다.

1. 브라우저를 조작하는 사용자가 애플리케이션의 메인 URI를 요청합니다.
2. 서버가 스크립트가 삽입된 웹 페이지를 제공합니다.
3. 브라우저가 웹 페이지를 렌더링하고, 스크립트를 실행하거나 사용자가 키보드나 마우스로 스크립트의 동작을 촉발하기를 기다립니다.
4. 스크립트가 서버의 어떤 URI로 비동기 HTTP 요청을 보냅니다. 사용자는 요청이 처리되는 동안 다른 일을 할 수 있으며, 요청이 일어나고 있다는 사실조차 모를 수 있습니다.
5. 스크립트가 HTTP 응답을 파싱하고 그 데이터로 사용자의 화면을 수정합니다. DOM 메서드로 원래 HTML 페이지의 태그 구조를 바꾸는 것일 수도, 플래시나 자바 애플릿 내부의 표시 내용을 바꾸는 것일 수도 있습니다.

사용자 관점에서는 GUI가 스스로 바뀐 것처럼 보입니다.

이 아키텍처는 클라이언트 측 GUI 애플리케이션의 구조와 매우 닮았고, 실제로 그것과 같습니다.
브라우저가 (초기 HTML 파일에 기술된 대로) GUI 요소를 제공하고, (자바스크립트 이벤트를 통해) 이벤트 루프를 제공합니다.
사용자가 이벤트를 촉발하면 어딘가에서 데이터를 가져와 GUI 요소를 그에 맞게 바꿉니다.
Ajax 애플리케이션이 데스크톱 애플리케이션처럼 동작한다고 칭찬받는 까닭이 바로 이 동일한 아키텍처에 있습니다.

일반 웹 애플리케이션은 같은 GUI 요소를 가지되 더 단순한 이벤트 루프를 가집니다.
모든 클릭이나 폼 전송이 화면 전체를 새로 고치게 만듭니다.
브라우저는 새 HTML 페이지를 받아 완전히 새로운 GUI 요소 집합을 구성합니다.
반면 Ajax 애플리케이션에서는 GUI가 조금씩 바뀔 수 있어 대역폭을 아끼고 최종 사용자에게 주는 심리적 부담을 줄입니다.
애플리케이션이 갑작스럽게 덜컹거리며 바뀌지 않고 점진적으로 변하는 것처럼 보입니다.

단점은 모든 애플리케이션 상태가 동일한 URI, 즉 최종 사용자가 처음 방문한 URI를 갖는다는 점입니다.
주소 지정 가능성(addressability)과 무상태성(statelessness)이 파괴됩니다.
그 아래의 웹 서비스는 주소 지정이 가능하고 무상태일 수 있지만, 최종 사용자는 더 이상 특정 상태를 북마크할 수 없고 브라우저의 “뒤로” 버튼도 제대로 작동하지 않습니다.
이렇게 되면 애플리케이션은, 단일 URI만 노출하는 SOAP+WSDL 웹 서비스가 웹 위에 있지 않은 것과 마찬가지로, 더 이상 웹 위에 있지 않습니다.
이 문제를 어떻게 다룰지는 뒤에서 논의합니다.

## del.icio.us 예제

2장에서 저자는 REST-RPC 혼성 서비스인 del.icio.us 소셜 북마킹 API를 대상으로 여러 언어의 클라이언트를 보여주었습니다.
여기서는 자바스크립트로 작성된 클라이언트를 시연하기 위해 그 원래 서비스를 다시 꺼냅니다.
이 프로그램은 브라우저 안에서 도는 웹 서비스 클라이언트이므로 Ajax 애플리케이션입니다.
단순하지만 이 장에서 논의하는 Ajax의 장점과 문제를 거의 전부 끌어냅니다.

애플리케이션의 첫 부분은 평범한 HTML로 구현된 사용자 인터페이스입니다.

```html
<form onsubmit="callDelicious(); return false;">
Username: <input id="username" type="text" /><br />
Password: <input id="password" type="password" /><br />
<input type="submit" value="Fetch del.icio.us bookmarks" />
</form>

<div id="message"></div>
<ul id="links"></ul>
```

사용자 인터페이스는 어디도 가리키지 않는 HTML 폼과, 아무것도 담고 있지 않은 태그(div와 ul)로 이루어집니다.
이 태그들을 자바스크립트 함수로 조작하게 됩니다.
첫 번째 함수는 setMessage로, 주어진 문자열을 div 태그에 넣습니다.

```javascript
function setMessage(newValue) {
  message = document.getElementById("message");
  message.firstChild.textContent = newValue;
}
```

이 폼이 “어디도 가리키지 않는다”는 말은 정확하지 않습니다.
일반 HTML 폼처럼 action 속성을 갖지는 않지만 onsubmit 이벤트 핸들러를 갖습니다.
따라서 최종 사용자가 전송 버튼을 클릭하면 브라우저가 자바스크립트 함수 callDelicious를 호출합니다.
브라우저의 페이지 요청 루프 대신 자바스크립트 프로그램의 GUI 유사 이벤트 루프를 쓰는 것입니다.

callDelicious 함수는 자바스크립트 라이브러리 XMLHttpRequest를 사용해 사용자의 최근 북마크를 가져오는 URI에서 데이터를 받아옵니다.
먼저 몇 가지 준비 작업이 필요합니다.
요청을 보내도 되는지 브라우저에서 권한을 얻고, 사용자가 HTML 폼에 입력한 데이터를 모읍니다.

```javascript
function callDelicious() {
  // 요청을 보내도 되는지 브라우저에서 권한을 얻는다.
  try {
    if (netscape.security.PrivilegeManager.enablePrivilege)
      netscape.security.PrivilegeManager.enablePrivilege("UniversalBrowserRead");
  } catch (e) {
    alert("죄송합니다. 브라우저 보안 설정이 이 프로그램의 실행을 허용하지 않습니다.");
    return;
  }

  // 사용자가 입력한 계정 정보를 가져온다.
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  // 목록에서 기존 링크를 모두 제거한다.
  var links = document.getElementById("links");
  while (links.firstChild)
    links.removeChild(links.firstChild);
  setMessage("잠시 기다려 주세요...");
```

이제 HTTP 요청을 보낼 차례입니다.

```javascript
  // 요청을 보낸다.
  request = new XMLHttpRequest();
  request.open("GET", "https://api.del.icio.us/v1/posts/recent", true,
               username, password);
  request.onreadystatechange = populateLinkList;
  request.send(null);
}
```

세 번째 함수 populateLinkList는 request.onreadystatechange에 대입되어 콜백 함수로 등록됩니다.
api.del.icio.us가 요청을 처리하는 동안 사용자는 다른 브라우저 창에서 웹 서핑을 계속할 수 있고, 요청이 완료되면 브라우저가 populateLinkList를 호출해 응답을 처리합니다.
콜백 함수 없이도 자바스크립트 프로그래밍은 가능하지만 그것은 나쁜 방법입니다.
콜백이 없으면 XMLHttpRequest 객체가 HTTP 요청을 수행하는 동안 브라우저가 응답하지 않게 되어 비동기라 할 수 없습니다.

populateLinkList의 임무는 del.icio.us 서비스가 보낸 XML 문서를 파싱하는 것입니다.
응답은 북마크 목록을 나타내는 표현이며, populateLinkList는 각 북마크를 (전에는 비어 있던) ul 목록 태그의 항목으로 바꿉니다.

```javascript
// HTTP 요청이 완료되면 호출된다.
function populateLinkList() {
  if (request.readyState != 4) // 요청이 아직 완료되지 않았다.
    return;

  setMessage("요청이 완료되었습니다.");

  if (netscape.security.PrivilegeManager.enablePrivilege)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalBrowserRead");

  // 표현에서 "post" 태그를 찾는다.
  posts = request.responseXML.getElementsByTagName("post");
  setMessage(posts.length + "개의 링크를 찾았습니다:");

  // XML 문서의 모든 "post" 태그에 대해...
  for (var i = 0; i < posts.length; i++) {
    post = posts[i];

    // ...적절한 URI로 연결되는 링크를 만든다.
    var link = document.createElement("a");
    var description = post.getAttribute("description");
    link.setAttribute("href", post.getAttribute("href"));
    link.appendChild(document.createTextNode(description));

    // 링크를 "li" 태그에 넣고...
    var listItem = document.createElement("li");
    // ..."li" 태그를 "ul" 태그의 자식으로 만든다.
    listItem.appendChild(link);
    links.appendChild(listItem);
  }
}
```

## Ajax의 장점

이 클라이언트를 실행해 보면 브라우저 환경에서 오는 좋은 기능들을 느낄 수 있습니다.
가장 눈에 띄는 것은, 2장의 예제와 달리 이 애플리케이션에는 GUI가 있다는 점입니다.
GUI 프로그래밍치고는 상당히 쉬운 편입니다.
겉보기에는 알쏭달쏭한 document 자료 구조를 조작할 뿐인 메서드 호출이 실제로는 사용자가 보는 화면을 바꿉니다.
document는 사용자가 브라우저에서 렌더링된 상태로 보는 바로 그것입니다.
브라우저가 document의 변경을 GUI 레이아웃 변경으로 알아서 바꿔 주므로, 전통적 GUI 프로그램에서 보이는 위젯 생성과 레이아웃 명세 작업이 필요 없습니다.

이 클라이언트는 del.icio.us 서비스의 XML 응답을 명시적으로 파싱하지 않습니다.
브라우저에는 XML 파서가 내장되어 있고, XMLHttpRequest는 웹 서비스 응답으로 들어온 XML 문서를 자동으로 DOM 객체로 파싱합니다.
그 DOM 객체는 XMLHttpRequest.responseXML 멤버를 통해 접근합니다.
브라우저용 DOM 표준이 이 객체의 API를 정의하므로 자식들을 순회하거나 getElementsByTagName 같은 메서드로 검색하거나 XPath 표현식으로 조회할 수 있습니다.

더 미묘한 장점도 있습니다.
사용자 이름과 비밀번호를 입력하지 않고 전송 버튼을 누르면, 브라우저가 HTTP 기본 인증(basic auth)이 필요한 페이지에 접근할 때 늘 띄우는 것과 동일한 계정 입력 대화상자가 나타납니다.
이는 HTTP 기본 인증을 요구하는 URI를 브라우저에서 방문하는 것과 정확히 같은 일을 하기 때문입니다.
다만 URL 링크를 클릭하는 대신 Ajax 애플리케이션에서 동작을 촉발해 그렇게 하고 있을 뿐입니다.

브라우저는 단연 가장 널리 쓰이는 HTTP 클라이언트이며 HTTP의 까다로운 경우들을 처리하도록 만들어져 있습니다.
HTML 폼에서 두 텍스트 필드를 모두 없애더라도, 실제 브라우저가 기본 인증 정보를 수집하는 자체 사용자 인터페이스를 갖고 있으므로 이 Ajax 애플리케이션은 여전히 동작합니다.

## Ajax의 단점

다양한 브라우저가 쓰이는 탓에, 애플리케이션이 모든 브라우저에서 동작하기를 바란다면 완전히 새로운 예외 상황들을 다뤄야 합니다.
이런 예외를 우회하는 코드 라이브러리와 코드 조각은 뒤에서 소개합니다.

이 프로그램을 실행하면 8장 끝에서 다룬 문제, 즉 “최종 사용자가 왜 이 웹 서비스 클라이언트를 신뢰해야 하는가?”라는 문제와 마주칩니다.
사용자는 자신의 브라우저에게는 del.icio.us 계정 정보를 맡기겠지만, 이 프로그램은 사용자의 브라우저가 아닙니다.
브라우저를 이용해 HTTP 요청을 보내는 웹 서비스 클라이언트이며, 그 요청 안에서 무슨 짓을 하고 있을지 알 수 없습니다.
만약 이것이 api.del.icio.us에서 직접 제공된 공식 웹 페이지라면 브라우저는 그 페이지가 자신이 온 서버로 웹 서비스 호출을 하도록 신뢰할 것입니다.
그러나 이것은 사용자의 하드디스크에 있는 파일에서 온 페이지이면서 넓은 웹을 향해 요청을 보내려 합니다.
브라우저가 보기에 이는 매우 수상한 행동입니다.

보안 관점에서 이것은 다른 언어로 작성된 독립 실행형 del.icio.us 클라이언트와 다르지 않습니다.
그런데 사실 독립 실행형 클라이언트를 신뢰할 진짜 이유도 없습니다.
우리는 그냥 그것들이 안전하다고 가정할 뿐입니다.
브라우저는 신뢰할 수 없는 웹 페이지를 끊임없이 불러오므로, 그런 페이지가 자바스크립트로 할 수 있는 일을 제한하는 보안 모델을 갖고 있습니다.
낯선 사람들이 늘 당신의 홈 디렉터리에 실행 파일을 던져 넣는다면, 그것을 실행하기 전에 두 번은 생각하게 될 것입니다.

그래서 저자는 netscape.security.PrivilegeManager.enablePrivilege를 호출해, 외부 도메인으로 HTTP 요청을 보내도 되는지, 그리고 외부 도메인에서 온 데이터에 브라우저의 XML 파서를 써도 되는지를 “UniversalBrowserRead” 권한으로 요청했습니다.
이런 호출을 넣더라도 브라우저는 이 위험한 동작을 받아들일지 묻는 보안 메시지를 띄우기 쉽습니다.
이 메시지들은 HTML 폼을 전송할 때 나오는 대수롭지 않은 경고와는 달리 훨씬 심각한 경고입니다.
게다가 이는 파일이 (아마도 신뢰되는) 사용자 파일 시스템에 있을 때의 이야기입니다.
같은 Ajax 애플리케이션을 oreilly.com에서 제공하려 한다면 브라우저는 api.del.icio.us로 HTTP 요청을 보내는 것을 결코 허용하지 않을 것입니다.

그렇다면 왜 실제 Ajax 애플리케이션에서는 이런 문제를 늘 겪지 않을까요?
지금 대부분의 Ajax 애플리케이션이 자신이 접근하는 웹 서비스와 같은 도메인 이름에서 제공되기 때문입니다.
이것이 자바스크립트 웹 서비스 클라이언트와 다른 언어로 작성된 클라이언트의 근본적 차이입니다.
자바스크립트 클라이언트는 보통 서버와 같은 사람이 작성하고 같은 도메인에서 제공됩니다.

브라우저의 보안 모델이 남의 웹 서비스를 대상으로 하는 XMLHttpRequest 애플리케이션을 완전히 막는 것은 아니지만 어렵게 만듭니다.
브라우저에 따르면 경고 없이 실행하기에 충분히 안전한 Ajax 애플리케이션은 자신이 제공된 그 도메인에만 요청을 보내는 것뿐입니다.
장 끝에서 외부 웹 서비스를 소비하는 Ajax 클라이언트를 작성하는 방법을 보여주지만, 그 기법들은 상당 부분 편법에 의존한다는 점을 유의해야 합니다.

## REST가 더 잘 맞는다

Ajax 애플리케이션은 웹 서비스 클라이언트인데, 왜 하필 RESTful 웹 서비스의 클라이언트여야 할까요?
대부분의 Ajax 애플리케이션은 애플리케이션을 만든 바로 그 사람들이 만든 웹 서비스를 소비합니다.
브라우저 보안 모델이 다른 방식을 어렵게 만들기 때문입니다.
한 클라이언트만 쓰는 서비스라면 완전한 RESTful이든 리소스 지향/RPC 혼성이든 무슨 상관일까요?
WSDL 파일을 XMLHttpRequest로 RPC SOAP 호출을 하는 자바스크립트 라이브러리로 바꿔 주는 프로그램조차 있는데 말입니다.

일반적으로 애플리케이션의 두 부분 사이의 인터페이스는 중요합니다.
RESTful 아키텍처가 더 나은 웹 서비스를 만든다면, 서비스를 소비하는 사람이 당신 자신뿐이라도 그 이점을 누리게 됩니다.
게다가 애플리케이션이 유용한 일을 한다면, 웹 사이트가 유용한 정보를 노출하면 사람들이 스크린 스크래핑을 하듯이, 사람들이 당신의 웹 서비스를 알아내 자기만의 클라이언트를 작성할 것입니다.
당신만 쓸 수 있도록 서비스를 일부러 난독화하려는 게 아니라면 리소스 지향 아키텍처가 최선의 설계입니다.

Ajax 애플리케이션이 소비하는 웹 서비스가 RESTful해야 하는 이유는 거의 모든 웹 서비스가 RESTful해야 하는 이유, 즉 주소 지정 가능성, 무상태성 등과 같습니다.
여기서 유일한 차이는 Ajax 클라이언트가 브라우저 안에 내장되어 있다는 점인데, 브라우저 환경은 오히려 REST를 지지하는 논거를 강화합니다.
SOAP, WSDL 같은 부류는 브라우저 안에서 훨씬 더 다루기 버거워 보입니다.
설령 REST 패러다임이 분산 프로그래밍의 일반 플랫폼으로 적합하지 않다고 회의하더라도, 최소한 브라우저와 웹 서버 사이의 통신에는 적합해야 합니다.

브라우저 밖에서는 인간 웹의 인터페이스인 GET과 POST만으로 스스로를 제한할 수도 있습니다.
많은 클라이언트 라이브러리가 HTTP의 기본 기능만 지원합니다.
그러나 모든 Ajax 애플리케이션은 유능한 HTTP 클라이언트 안에서 실행됩니다.
거의 모든 브라우저가 XMLHttpRequest에 다섯 가지 기본 HTTP 메서드에 대한 접근을 제공하며, 모두 요청 헤더와 본문을 자유롭게 지정할 수 있게 합니다.

게다가 Ajax 호출은 최종 사용자의 다른 웹 브라우징과 같은 환경에서 일어납니다.
클라이언트가 프록시를 거쳐 HTTP 요청을 보내야 한다면 사용자가 이미 프록시를 설정해 두었다고 가정할 수 있습니다.
Ajax 요청은 브라우저의 다른 요청과 동일한 쿠키와 기본 인증 헤더를 당신의 도메인으로 보냅니다.
따라서 웹 사이트와 Ajax 서비스에 대개 같은 인증 메커니즘과 사용자 계정을 쓸 수 있습니다.

Ajax 아키텍처의 4단계와 5단계, 즉 “URI를 GET한다”와 “URI에서 얻은 데이터로 화면을 수정한다”는 리소스 지향 아키텍처와 잘 맞습니다.
Ajax 애플리케이션은 수많은 리소스에 관한 정보를 집계하고, 리소스 상태가 바뀔 때 GUI를 점진적으로 바꿀 수 있습니다.
서버가 애플리케이션 상태를 전혀 유지하지 않으면 브라우저의 애플리케이션 상태를 서버와 맞출 필요가 없다는 것이 한 가지 예입니다.

## 요청 만들기

이제 가장 흔한 Ajax 클라이언트 언어인 자바스크립트의 기술적 세부를 살펴봅니다.
주요 브라우저는 모두 XMLHttpRequest라는 자바스크립트 HTTP 클라이언트 라이브러리를 구현합니다.
프록시, HTTPS, 리다이렉트 같은 까다로운 경계 사례를 브라우저 환경이 처리하므로 그 인터페이스는 단순합니다.

HTTP 요청을 만들려면 XMLHttpRequest 객체를 생성해야 합니다.
겉보기에 단순한 이 작업이 실제로는 브라우저 간 차이의 주요 지점 중 하나입니다.
다음 생성자는 파이어폭스 같은 모질라 계열 브라우저에서 동작합니다.

```javascript
request = new XMLHttpRequest();
```

두 번째 단계는 요청 정보를 담아 XMLHttpRequest.open 메서드를 호출하는 것입니다.
앞의 두 인자를 제외한 나머지는 모두 선택 사항입니다.

```javascript
request.open([HTTP 메서드], [URI], true, [기본 인증 사용자 이름], [기본 인증 비밀번호]);
```

세 번째 인자만 설명이 필요합니다.
이 인자는 브라우저가 요청을 비동기로 수행할지(사용자가 진행 중 다른 일을 할 수 있게), 아니면 동기로 수행할지(서버 응답을 받아 파싱할 때까지 브라우저 전체를 잠금)를 제어합니다.
브라우저를 잠그는 것은 결코 좋은 사용자 경험이 아니므로 아무리 단순한 애플리케이션이라도 권장하지 않습니다.
따라서 요청이 완료될 때 호출될 핸들러 함수를 설정해야 합니다.

```javascript
request.onreadystatechange = [핸들러 함수 이름];
```

HTTP 요청 헤더를 지정하려면 setRequestHeader를 씁니다.

```javascript
request.setRequestHeader([헤더 이름], [헤더 값]);
```

그런 다음 send를 호출해 요청을 서버로 보냅니다.
POST나 PUT 요청이면 보낼 엔티티 본문을 send의 인자로 넘기고, 그 외의 요청이면 null을 넘깁니다.

```javascript
request.send([엔티티 본문]);
```

모든 것이 순조로우면 onreadystatechange에 설정한 핸들러 함수가 요청의 생애 동안 네 번 호출되고, 그때마다 request.readyState 값이 달라집니다.
우리가 기다리는 값은 마지막 값인 4로, 요청이 완료되어 이제 응답을 조작할 때가 되었음을 뜻합니다.
readyState가 4가 아니면 핸들러 함수에서 그냥 반환합니다.

XMLHttpRequest는 그 아래의 브라우저 코드로 요청을 수행합니다.
주요 브라우저는 가장 완성도 높은 HTTP 클라이언트 구현 축에 들기 때문에, 2장에서 소개한 HTTP 클라이언트 기능 표에서 XMLHttpRequest도 꽤 좋은 점수를 받습니다.
쿠키, 프록시, 인증은 Ajax 애플리케이션에서도 일반 웹 접근에서와 마찬가지로 대체로 잘 작동합니다.

## 응답 처리하기

결국 요청이 완료되면 브라우저가 핸들러 함수를 마지막으로 호출합니다.
이 시점에 XMLHttpRequest 인스턴스는 새롭고 흥미로운 능력을 얻습니다.

- status 속성은 요청의 숫자 상태 코드를 담습니다.
- responseXML 속성은 응답 문서를 미리 파싱한 DOM 객체를 담습니다. 단, 응답이 XML로 제공되고 브라우저가 그것을 파싱할 수 있어야 합니다. HTML은 XHTML이라도, 문서가 application/xml이나 application/xhtml+xml 같은 XML 미디어 타입으로 제공되지 않는 한 responseXML로 파싱되지 않습니다.
- responseText 속성은 응답 문서를 가공되지 않은 문자열로 담습니다. JSON이나 그 밖의 비XML 형식일 때 유용합니다.
- getResponseHeader 메서드에 HTTP 헤더 이름을 넘기면 그 헤더의 값을 찾아 줍니다.

브라우저는 문서를 자료 구조로 바꾸는 트리 방식 파싱 전략의 전형입니다.
자바스크립트 안에서 웹 서비스 요청을 하면 responseXML 속성이 응답 문서를 트리로 제공합니다.
표준화된 DOM 조작 메서드로 그 표현에 접근할 수 있습니다.

DOM 인터페이스는 XMLHttpRequest 인터페이스와 달리 매우 복잡하여 여기서 전부 다루지는 않습니다.
공식 표준(<http://www.w3.org/DOM>), 모질라 DOM 레퍼런스, 또는 Danny Goodman의 《Dynamic HTML: The Definitive Reference》(O'Reilly) 같은 책을 참고하기 바랍니다.
getElementById 같은 메서드로 트리를 탐색하고 evaluate로 XPath 질의를 실행할 수 있습니다.

그런데 또 하나의 트리형 자료 구조가 있습니다.
바로 최종 사용자의 브라우저에 표시되는 HTML 문서입니다.
Ajax 애플리케이션에서 이 문서는 사용자 인터페이스이며, XML 웹 서비스 표현에서 데이터를 추출할 때 쓰는 것과 동일한 DOM 메서드로 조작합니다.
Ajax 애플리케이션은 웹 서비스가 보낸 원시 데이터와 최종 사용자가 보는 HTML GUI 사이를 잇는 접착제 역할을 합니다.
여기서 유용한 DOM 메서드는 앞서 예제에서 쓴 createTextNode와 createElement입니다.

## JSON

JSON은 2장에서 간단히, 9장에서 권장 표현 형식의 하나로 다뤘습니다.
JSON은 자바스크립트에서 왔으므로 Ajax 장에서 실제로 동작하는 모습을 보입니다.
예제로 야후의 이미지 검색 웹 서비스를 호출하는 Ajax 클라이언트를 살펴봅니다.

```javascript
function formatImages(result) {
  var images = document.getElementById("images");
  items = result["ResultSet"]["Result"];
  document.getElementById("message").firstChild.textContent =
    items.length + " baby elephant pictures:";
  for (var i = 0; i < items.length; i++) {
    image = items[i];
    // 링크를 만든다.
    var link = document.createElement("a");
    link.setAttribute("href", image["ClickUrl"]);
    // 링크 안에 썸네일 이미지를 넣는다.
    var img = document.createElement("img");
    var thumbnail = image["Thumbnail"];
    img.setAttribute("src", thumbnail["Url"]);
    img.setAttribute("width", thumbnail["Width"]);
    img.setAttribute("height", thumbnail["Height"]);
    img.setAttribute("title", image["Height"]);
    link.appendChild(img);
    images.appendChild(link);
  }
}
```

```html
<script type="text/javascript"
  src="http://api.search.yahoo.com/ImageSearchService/V1/imageSearch?appid=restbook&query=baby+elephant&output=json&callback=formatImages">
</script>
```

이 HTML 파일을 열면 야후 이미지 검색이 제공하는 아기 코끼리 사진을 볼 수 있고, 브라우저 보안 경고는 보이지 않습니다.
del.icio.us 예제는 다른 도메인으로 XMLHttpRequest를 보내도 되는지 브라우저에 물어야 했고, 그마저도 브라우저가 엄격한 규칙을 강제했습니다.
그러나 이 클라이언트는 그냥 웹 서비스 호출을 합니다.
XMLHttpRequest를 통해 호출하지 않기 때문입니다.
이것은 JavaScript on Demand(JoD)라는 기법을 씁니다.
JoD는 웹 서비스에서 맞춤 생성된 자바스크립트를 가져오는 방식으로 브라우저의 보안 정책을 우회합니다.
모든 JSON 자료 구조는 유효한 자바스크립트 프로그램이므로, JSON 표현을 제공하는 웹 서비스와 특히 잘 맞습니다.

## REST의 이점을 독차지하지 말라

Ajax 애플리케이션이 REST의 모든 이점을 자기가 독차지하고 최종 사용자에게는 아무것도 남기지 않기 쉽습니다.
Gmail이 좋은 예입니다.
Gmail의 Ajax 애플리케이션은 주소 지정이 가능하고 무상태인 웹 서비스를 쓰는 덕을 크게 봅니다.
그러나 사용자 경험 측면에서 최종 사용자에게 보이는 것은 끊임없이 바뀌는 하나의 HTML 페이지뿐입니다.
검색이나 특정 이메일 메시지를 북마크하고 싶으면 Gmail의 평범한 HTML 인터페이스에서 시작해야 합니다.

보통 브라우저의 뒤로, 앞으로 버튼은 애플리케이션 상태 사이를 오가게 해 줍니다.
이는 웹이 무상태이기 때문에 가능합니다.
그러나 전형적인 Ajax 애플리케이션을 쓰기 시작하면 뒤로 버튼이 고장 납니다.
버튼을 눌러도 애플리케이션 상태에서 뒤로 가는 것이 아니라, Ajax 애플리케이션을 쓰기 시작하기 전에 있던 페이지로 갑니다.

근본 원인은 Ajax 애플리케이션에 세련된 겉모습을 주는 바로 그것입니다.
Ajax 애플리케이션은 최종 사용자를 HTTP 요청-응답 주기에서 떼어 놓습니다.
Ajax 애플리케이션의 URI를 방문하는 순간 사용자는 웹을 떠납니다.
그때부터는 배경에서 HTTP 요청을 대신 보내고 그 데이터를 GUI에 다시 접어 넣는 GUI 애플리케이션을 쓰는 것입니다.
그 GUI 애플리케이션이 마침 웹 브라우징에 쓰는 소프트웨어 안에서 돌고 있을 뿐입니다.
그러나 Ajax 애플리케이션도 REST의 이점을 사용자 인터페이스에 녹여 넣어 사용자에게 돌려줄 수 있습니다.
이는 브라우저의 기능 일부를 애플리케이션 안에서 다시 발명하라고 요청하는 셈입니다.

가장 좋은 예는 Ajax 열풍을 시작한 Google Maps입니다.
언뜻 Google Maps는 Gmail만큼이나 주소 지정이 안 되는 것처럼 보입니다.
maps.google.com을 방문하면 큰 축척의 지도가 나오고, Ajax로 확대하거나 지구 어디로든 이동해도 주소 표시줄의 URI는 결코 바뀌지 않습니다.

그러나 Google Maps는 Ajax를 이용해 현재 위치에 대한 “퍼머링크(permalink)”를 유지합니다.
이 URI는 주소 표시줄이 아니라 HTML 문서의 a 태그 안에 보관됩니다.
그것은 지구의 한 구획을 식별하는 데 필요한 위도, 경도, 지도 축척 등 모든 정보를 담고 있으며, Ajax 애플리케이션으로 들어가는 새로운 진입점입니다.
이 링크는 Google Maps에서 브라우저 주소 표시줄에 해당합니다.

사용자가 지도를 이동할 때마다 이 a 태그를 최신 상태로 유지하는 추가 DOM 작업 덕분에 모든 지도의 모든 지점이 웹 위에 있게 됩니다.
어떤 지점이든 북마크하고 블로그에 쓰고 이메일로 돌려 볼 수 있습니다.
그런 URI를 방문한 사람은 미국 본토 중심의 화면이 아니라 정확한 지점에서 Google Maps 애플리케이션에 진입합니다.
Ajax가 파괴한 주소 지정 가능성을 좋은 애플리케이션 설계로 되살린 덕분에 Google Sightseeing 같은 커뮤니티가 자라날 수 있었습니다.

당신의 Ajax 애플리케이션도 브라우저의 뒤로, 앞으로 버튼 기능을 재현해 무상태성을 되돌려 줄 수 있습니다.
브라우저의 동작을 노예처럼 그대로 따를 필요는 없습니다.
핵심은, 사용자가 실수하거나 길을 잃었을 때 복잡한 작업을 처음부터 다시 하지 않고 애플리케이션 상태를 앞뒤로 오갈 수 있게 하는 것입니다.

## 브라우저 간 문제와 Ajax 라이브러리

브라우저가 관여하는 일이 늘 그렇듯 클라이언트마다 XMLHttpRequest 지원 수준이 다르고, 늘 그렇듯 인터넷 익스플로러가 대표적인 예외입니다.
사실 이는 조금 불공평한데, XMLHttpRequest는 마이크로소프트가 발명했고 인터넷 익스플로러가 Ajax를 처음 지원한 브라우저였기 때문입니다.
그러나 인터넷 익스플로러 7이 나오기 전까지 Ajax는 XMLHttp라는 ActiveX 컨트롤, 즉 윈도우 전용 기술로 구현되어 있었습니다.

크로스 플랫폼 모질라 프로젝트는 XMLHttp 컨트롤의 API를 채택하되, 자바스크립트에서 직접 인스턴스화할 수 있는 클래스로 구현했습니다.
다른 브라우저들도 이 방식을 따랐고, 이제 (새 인터넷 익스플로러를 포함해) 모든 최신 브라우저가 XMLHttpRequest 이름을 씁니다.
그러나 구버전 인터넷 익스플로러가 여전히 사용자 기반의 큰 부분을 차지하므로 브라우저 간 문제는 여전히 골칫거리입니다.

다음은 겉으로는 ActiveX 컨트롤일 수 있어도 항상 XMLHttpRequest처럼 동작하는 객체를 만드는 자바스크립트 함수입니다.
Bret Taylor가 작성했습니다.

```javascript
function createXMLHttpRequest() {
  if (typeof XMLHttpRequest != "undefined") {
    return new XMLHttpRequest();
  } else if (typeof ActiveXObject != "undefined") {
    return new ActiveXObject("Microsoft.XMLHTTP");
  } else {
    throw new Error("XMLHttpRequest not supported");
  }
}
```

이 함수는 XMLHttpRequest 생성자를 그대로 대체할 수 있습니다.
`request = new XMLHttpRequest();` 대신 `request = createXMLHttpRequest();`라고 쓰면 됩니다.

주요 브라우저 간 문제가 두 가지 더 있습니다.
첫째, 사파리 브라우저는 PUT과 DELETE 메서드를 지원하지 않습니다.
사파리에서 서비스에 접근할 수 있게 하려면 클라이언트가 오버로드된 POST로 PUT과 DELETE 요청을 흉내 내게 해야 합니다.
둘째, 마이크로소프트 인터넷 익스플로러는 성공한 응답을 무기한 캐싱합니다.
그래서 리소스가 실제로 바뀌었는데도 바뀌지 않은 것처럼 사용자에게 보입니다.
가장 좋은 해결책은 표현과 함께 적절한 ETag 응답 헤더를 보내거나 Cache-Control로 캐싱을 아예 끄는 것입니다.

Ajax는 자바스크립트 애플리케이션의 매우 중요한 영역이므로, 일부 자바스크립트 라이브러리는 브라우저 간 차이를 감추는 래퍼를 포함합니다.
이들은 웹 서비스 클라이언트 구축 도구라기보다 자바스크립트용 표준 라이브러리에 가까우므로 자세히 다루지는 않고, 인기 있는 두 라이브러리인 Prototype과 Dojo로 간단한 HTTP 요청을 만드는 법만 보입니다.

### Prototype

Prototype은 HTTP 요청을 위해 세 가지 클래스를 도입합니다.

- Ajax.Request는 브라우저 간 문제를 처리하고 요청의 성공이나 실패 시 서로 다른 자바스크립트 함수를 호출할 수 있는 XMLHttpRequest 래퍼입니다. 실제 XMLHttpRequest 객체는 Request 객체의 transport 멤버로 접근하므로 responseXML은 request.transport.responseXML을 통해 얻습니다.
- Ajax.Updater는 Request의 서브클래스로, HTTP 요청을 하고 응답 문서를 DOM의 지정한 요소에 삽입합니다.
- Ajax.PeriodicalUpdater는 같은 HTTP 요청을 일정 간격으로 반복하며 매번 DOM 요소를 갱신합니다.

Prototype으로 구현한 del.icio.us 클라이언트는 원본과 대부분 같고, XMLHttpRequest 생성자가 있던 부분만 바뀝니다.
onFailure 훅으로 인증 실패 같은 오류를 사용자에게 알린다는 점에 주목합니다.

```javascript
var request = new Ajax.Request("https://api.del.icio.us/v1/posts/recent",
  {method: 'get', onSuccess: populateLinkList,
   onFailure: reportFailure});

function reportFailure() {
  setMessage("오류가 발생했습니다: " + request.transport.status);
}
```

Prototype은 XMLHttpRequest를 단순화하는 과정에서 일부 기능을 감춥니다.
요청 헤더를 설정하거나 기본 인증용 사용자 이름과 비밀번호를 지정할 수 없습니다.
그래서 Prototype을 쓰더라도 앞서 소개한 크로스 브라우저 래퍼 같은 코드 조각을 곁에 두고 싶을 수 있습니다.
한편 Prototype 구현은 사용자 이름과 비밀번호 텍스트 필드가 아예 필요 없고 버튼만 있으면 됩니다.
브라우저가 어차피 사용자에게 del.icio.us 계정 정보를 물어보기 때문입니다.

### Dojo

Dojo 라이브러리는 XMLHttpRequest에 관한 브라우저 간 차이뿐 아니라, XMLHttpRequest와 브라우저에게 HTTP 요청을 보내게 하는 다른 방법들 사이의 차이까지 감추는 통일된 API를 제공합니다.
이 “전송(transport)”에는 JoD처럼 HTML 태그를 이용하는 편법도 포함됩니다.
XMLHttpRequest의 변종들은 모두 dojo.io.XMLHttp 전송 클래스에 담기며, 모든 전송에서 실제 HTTP 요청을 하는 것은 bind 메서드입니다.

```javascript
dojo.require("dojo.io.*");

dojo.io.bind({ url: "https://api.del.icio.us/v1/posts/recent",
  load: populateLinkList, error: reportFailure });

function reportFailure(type, error) {
  setMessage("오류가 발생했습니다: " + error.message);
}
```

오류 처리 함수는 number와 message 멤버를 가진 dojo.io.Error 객체를 받습니다.
첫 번째 인자는 항상 “error”이므로 무시해도 됩니다.
성공 처리 함수의 첫 번째 인자도 항상 “load”이므로 무시할 수 있고, 두 번째 인자는 Dojo의 DOM 조작 인터페이스입니다.
XMLHttpRequest 인터페이스를 대신 쓰고 싶으면 그 인자도 무시하면 됩니다.

## 브라우저 보안 모델 뒤엎기

브라우저는 도메인 A에서 찾은 코드로 도메인 B에 HTTP 요청을 보내지 못하게 하는 일반 규칙을 강제합니다.
저자는 이 규칙이 지나치게 엄격하다고 보고, 이를 우회하는 두 가지 방법인 요청 프록시(request proxying)와 JoD를 소개합니다.
동시에 이 편법들이 어떻게 Ajax 프로그래머로 하여금 외부 서버의 행위에 대한 책임까지 떠안게 만들어 위험에 빠뜨리는지도 보입니다.
이 기법들은 브라우저의 의도를 실현하기는커녕 뒤엎기 때문에 편법으로 여겨져 마땅합니다.
이들은 브라우저가 그냥 도메인 A의 자바스크립트로 도메인 B에 요청하게 허용했을 때보다 오히려 최종 사용자를 덜 안전하게 만들기도 합니다.

자바스크립트 애플리케이션에서 외부 웹 서비스 호출 권한을 얻는 안전한 방법은 다음을 호출해 권한을 요청하는 것입니다.

```javascript
netscape.security.PrivilegeManager.enablePrivilege("UniversalBrowserRead");
```

(안전하지 않은 방법도 있는데, 사용자에게 보안 설정을 크게 낮춘 인터넷 익스플로러를 쓰게 하는 것입니다.)

스크립트가 디지털 서명되어 있으면 클라이언트의 브라우저가 당신의 신원 정보를 사용자에게 보여줍니다.
사용자는 당신을 신뢰할지 결정하고, 신뢰한다면 필요한 웹 서비스 호출 권한을 줍니다.
이는 8장에서 언급한, 신뢰받지 못하는 웹 서비스 클라이언트가 사용자의 신뢰를 얻으려는 기법과 비슷합니다.
차이는 여기서는 신뢰받지 못하는 클라이언트가 사용자의 신뢰받는 브라우저 안에서 돈다는 점입니다.

이 안전한 방법에는 두 가지 문제가 있습니다.
첫째, netscape.security.PrivilegeManager라는 이름에서 짐작할 수 있듯 모질라, 파이어폭스, 넷스케이프 계열 브라우저에서만 동작합니다.
둘째, 서명된 스크립트를 실제로 마련하기가 꽤 고통스럽습니다.
서명된 스크립트를 마련하고 나면 HTML 파일이 서명된 자바 아카이브 파일에 담기고, 애플리케이션은 웹을 벗어나게 됩니다.
검색 엔진이 HTML 페이지를 수집하지 못하고, `jar:http://www.example.com/ajax-app.jar!/index.html` 같은 기묘한 jar: URI로만 주소를 지정할 수 있습니다.

그럼에도 저자는 이것이 올바른 해법이라고 말합니다.
이는 아직 미성숙한 분야이며, 최근까지 웹 서비스가 이런 문제를 진지하게 고민할 만큼 널리 쓰이지 않았습니다.
아래에서 설명하는 편법들은 잠재적으로 위험하지만, 그 발명자들은 해를 끼칠 뜻이 없었고 브라우저 내 웹 서비스 클라이언트의 거대한 가능성에 대한 열의로만 움직였습니다.
과제는 보안을 희생하거나 복잡성을 과도하게 더하거나 Ajax 애플리케이션을 웹의 시야 밖으로 밀어내지 않으면서 같은 기능을 얻는 방법을 찾는 것입니다.
W3C가 “Enabling Read Access for Web Resources”라는 이름으로 이 문제를 다루고 있습니다.

자바스크립트에 다시 초점을 맞추지만, 자바 애플릿과 플래시도 외부 서버로 데이터를 보내지 못하게 하는 보안 모델 아래에서 실행됩니다.
아래에 설명하는 요청 프록시 편법은 서버 측 작업을 수반하므로 어떤 종류의 Ajax 애플리케이션에도 통합니다.
반면 이름 그대로 JoD 편법은 자바스크립트 전용입니다.

### 요청 프록시

당신이 example.com이라는 사이트를 운영하며 yahoo.com에 XMLHttpRequest 요청을 하려는 Ajax 애플리케이션을 제공한다고 합시다.
당연히 클라이언트의 브라우저가 불평할 것입니다.
그런데 만약 클라이언트가 yahoo.com에 요청을 아예 하지 않는다면 어떨까요?
클라이언트는 example.com으로 요청하고, 당신은 그 요청을 받아 클라이언트 몰래 yahoo.com에 동일한 요청을 대신 보내는 것입니다.

이것이 요청 프록시 편법으로, 야후의 문서 “Use a Web Proxy for Cross-Domain XMLHttpRequest Calls”에 잘 설명되어 있습니다.
당신의 서버 URI 공간의 일부를 떼어 다른 서버의 URI 공간을 흉내 내게 합니다.
그 공간의 URI로 요청이 오면 그것을 변형 없이 외부 서버로 보내고, 응답을 곧장 클라이언트에게 되돌립니다.
클라이언트가 보기에는 당신이 남의 웹 서비스를 제공하는 것처럼 보이지만, 실제로는 남의 HTTP 응답에서 도메인 이름을 지우고 당신의 도메인으로 바꾸는 것뿐입니다.

Apache에 mod_proxy가 설치되어 있다면 가장 간단한 방법은 Apache 설정에서 프록시를 세우는 것입니다.
mod_ssl도 설치되어 있다면 SSLProxyEngine을 켜서 HTTPS 요청을 프록시할 수 있고, HTTP 서버에서도 HTTPS 요청을 프록시할 수 있습니다.
다만 이렇게 하면 연결의 보안이 깨집니다.
데이터는 프록시와 목적지 사이에서는 안전하지만 당신의 사이트와 최종 사용자 사이에서는 안전하지 않으므로, 이렇게 한다면 그 사실을 사용자에게 알려야 합니다.

del.icio.us Ajax 애플리케이션을 example.com에서 동작하게 하려면, <https://example.com/apis/delicious/v1/> 아래의 모든 URI가 <https://api.del.icio.us/v1/>로 투명하게 전달되도록 프록시를 세울 수 있습니다.
가장 간단한 방법은 ProxyPass 지시자입니다.

```text
SSLProxyEngine On
ProxyRequests Off # 오픈 프록시로 동작하지 않는다.
ProxyPass /apis/delicious/v1 https://api.del.icio.us/v1/
```

더 유연한 방법은 [P] 플래그를 붙인 rewrite 규칙으로, 정규 표현식의 힘을 빌려 URI 공간을 외부 사이트의 URI 공간에 대응시킵니다.

```text
SSLProxyEngine On
ProxyRequests Off # 오픈 프록시로 동작하지 않는다.
RewriteEngine On
RewriteRule ^apis/delicious/v1/(.*)$ https://api.del.icio.us/v1/$1 [P]
```

이렇게 설정하면 브라우저 보안 경고 없이 자기 도메인에서 Ajax 애플리케이션을 제공할 수 있습니다.
요청 URI만 <https://api.del.icio.us/v1/posts/recent>에서 <https://example.com/apis/delicious/v1/posts/recent>로 바꾸면 됩니다.

대부분의 Apache 설치에는 mod_proxy가 없습니다.
오픈 HTTP 프록시가 스패머 등 자취를 감추려는 자들이 즐겨 쓰는 도구이기 때문입니다.
웹 서버에 내장 프록시 지원이 없다면 투명 프록시 역할을 하는 작은 웹 서비스를 직접 작성해 서버에서 돌릴 수 있습니다.
이 서비스는 받은 모든 HTTP 요청을 헤더까지 그대로 대응하는 외부 URI로 전달합니다.
야후는 yahoo.com 웹 서비스에 하드코딩된 샘플 프록시 서비스를 PHP로 제공하므로 이를 본떠 만들 수 있습니다.

프록시가 제대로 설정되고 웹의 아주 작은 일부에 대해서만 프록시하더라도 당신과 사용자에게는 위험이 따릅니다.
Ajax 클라이언트를 위한 프록시를 세우면 사용자의 눈에는 그 외부 사이트가 하는 일에 대한 책임을 당신이 지는 것처럼 보입니다.
프록시 편법은 당신을 상대 사이트에서 벌어지는 나쁜 일의 희생양으로 만듭니다.
상대가 제공하는 것이 당신에게서 온 것처럼 꾸미는 셈이기 때문입니다.
그 웹 서비스가 죽거나 사용자를 속이거나 개인 정보를 오용하면 마치 당신이 그런 것처럼 보입니다.
Ajax 애플리케이션에서 사용자는 당신의 GUI 인터페이스만 봅니다.
브라우저가 배경에서 HTTP 요청을 한다는 것도, 자기 요청이 다른 도메인으로 프록시된다는 것도 사용자는 알지 못합니다.
브라우저가 그 사실을 알았다면 개입해 막았을 것입니다.

프록시 편법은 클라이언트가 하는 요청에 대한 희생양으로도 당신을 세웁니다.
클라이언트가 어떤 웹 서비스 요청을 하든 그 원인이 당신인 것처럼 보이며, 서비스의 성격에 따라 당신은 곤란이나 법적 위험에 처할 수 있습니다.
별도의 인가를 요구하는 웹 서비스라면 이 문제는 덜합니다.

### JavaScript on Demand

이 편법의 기반은 HTML의 script 태그가 반드시 하드코딩된 자바스크립트 코드를 담을 필요는 없다는 사실입니다.
script 태그는 다른 URI의 코드를 가리키는 src 속성만 가질 수도 있습니다.
브라우저는 script 태그를 만나면 src 속성의 URI를 불러와 그 내용을 코드로 실행합니다.
앞서 JSON 예제에서 이를 이미 보았습니다.

src 속성은 전통적으로 C의 #include나 Ruby의 require처럼 다른 URL에서 자바스크립트 라이브러리를 불러오는 데 쓰입니다.

```html
<script type="text/javascript" src="http://www.json.org/json.js"></script>
```

여기서 src 속성의 URI가 원래 HTML 파일과 같은 서버에 있을 필요는 없습니다.
브라우저 보안 모델이 이를 위험하다고 보지 않는 이유는, 저자가 짐작하기로는, 사람들이 보안 함의를 진지하게 고민하기 시작하기 전에 이미 src 속성이 널리 쓰이고 있었기 때문입니다.

이제 아기 코끼리 이미지 검색 예제로 돌아가 보면 다음 줄이 있습니다.

```html
<script type="text/javascript"
  src="http://api.search.yahoo.com/ImageSearchService/V1/imageSearch?appid=restbook&query=baby+elephant&output=json&callback=formatImages" />
```

이 긴 URI는 json.js처럼 독립된 자바스크립트 라이브러리로 해석되지 않습니다.
브라우저에서 방문하면 이 URI의 표현이 맞춤 생성된 자바스크립트 조각임을 알 수 있습니다.
야후는 개발자 문서에서 이런 리소스의 표현이 자바스크립트 코드 조각, 구체적으로는 URI에 명시된 콜백 함수(여기서는 formatImages)에 자료 구조를 유일한 인자로 넘겨 호출하는 조각임을 약속합니다.
결과 표현은 대략 다음과 같습니다.

```javascript
formatImages({"ResultSet":{"totalResultsAvailable":"27170", ...}})
```

클라이언트가 HTML 페이지를 불러오면 그 URI를 가져와 본문을 자바스크립트로 실행하고, 그 과정에서 formatImages 메서드가 호출됩니다.
우리 애플리케이션에는 좋지만 브라우저에는 그리 좋지 않습니다.
보안 관점에서 이것은 XMLHttpRequest로 야후 서비스에서 데이터를 가져와 결과에 formatImages를 호출하는 코드와 다를 바 없습니다.
HTTP 요청이 HTML 태그를 처리하는 부수 효과로 일어나게 만들어 브라우저 보안 모델을 우회하는 것입니다.

JoD는 HTML 페이지에 삽입된 스크립트와 `<script src=“...”>`로 포함된 스크립트의 전통적 역할을 뒤바꿉니다.
브라우저는 그저 HTML 페이지의 코드가 나중에 호출할 자바스크립트 라이브러리인 줄 알고 웹 서비스 URI를 요청합니다.
그러나 라이브러리 함수는 지역에 정의된 formatImages이고, 그 함수를 호출하는 애플리케이션 코드는 외부 사이트에서 옵니다.

URI에 콜백을 지정하지 않으면 JSON 자료 구조만 담긴 “자바스크립트” 파일을 받습니다.
이 파일을 script 태그에 포함해도 아무 일도 일어나지 않지만, 프로그래밍 가능한 HTTP 클라이언트로 가져와 데이터로 파싱할 수 있습니다.

```javascript
{"ResultSet":{"totalResultsAvailable":"27170", ...}}
```

#### script 태그를 동적으로 작성하기

지금까지 든 JoD 예제는 하드코딩된 script 태그를 가집니다.
웹 서비스 리소스 URI가 고정되어 있어, 사용자가 아기 코끼리 대신 아기 펭귄을 보고 싶어도 방법이 없습니다.

그러나 자바스크립트로 할 수 있는 일 중 하나는 현재 HTML 페이지를 나타내는 DOM 객체에 완전히 새로운 태그를 더하는 것이며, script도 그런 HTML 태그의 하나입니다.
자바스크립트로 맞춤 script 태그를 문서에 써 넣으면 브라우저가 스크립트 처리의 부수 효과로 그 src 속성의 URI를 불러옵니다.
src URI가 외부 도메인을 가리켜도 브라우저는 이를 허용합니다.
따라서 자바스크립트로 자바스크립트를 더 제공하는 어떤 URI에든 요청해 그것을 실행할 수 있습니다.

이것은 동작하지만 편법 위에 얹은 편법이자 보안 문제 위에 얹은 보안 문제입니다.
사실 보안 관점에서는 XMLHttpRequest로 외부 사이트에서 데이터를 가져오는 것보다 나쁩니다.
XMLHttpRequest는 기껏해야 HTTP 요청을 하고 XML을 트리형 자료 구조로 파싱할 뿐입니다.
반면 JoD는 HTTP 요청을 하고 한 번도 본 적 없는 자바스크립트 코드를 마치 원래 프로그램의 일부인 양 실행합니다.

당신과 사용자는 호출하는 서비스에 완전히 좌우됩니다.
악의적인 웹 서비스는 원하는 대로 동작하는 자바스크립트 대신, 당신의 도메인이 그 사용자에 대해 설정한 쿠키를 훔치는 자바스크립트를 제공할 수도 있습니다.
약속한 코드를 실행하면서 성가신 광고 팝업 창을 만들 수도 있고, 무엇이든 할 수 있습니다.
게다가 Ajax가 HTTP 요청-응답 주기를 사용자에게 감추므로 그 책임이 당신의 사이트에 있는 것처럼 보입니다.

야후 같은 유명 사이트는 (크래킹당하지 않는 한) 신뢰할지 몰라도 “Mallory의 웹 서비스 가게”는 신뢰하지 않을 것이고, 그 점 자체가 문제입니다.
웹의 좋은 점 하나는 신뢰하지 않고 허락받지 않고 상대가 다 틀렸다고 생각하는 Mallory에게도 안전하게 링크를 걸 수 있다는 것입니다.
일반적인 웹 서비스 클라이언트는 Mallory의 서비스를 호출하고, 속임수가 있는지 표현을 살펴본 뒤에 행동할 수 있습니다.
그러나 클라이언트가 실행 가능한 코드를 받고, 웹 서비스가 그 코드를 자동 실행하는 편법으로 요청받으면, 당신은 맹목적 신뢰에 기대는 처지로 전락합니다.

JoD는 보안 관점에서 미심쩍을 뿐 아니라 REST 관점에서도 형편없는 전술입니다.
불구가 된 클라이언트를 강요하기 때문입니다.
XMLHttpRequest는 HTTP의 모든 기능을 지원하지만 JoD로는 GET 요청만 할 수 있습니다.
요청 헤더를 보낼 수도, 응답 코드나 헤더를 볼 수도 없고, 자바스크립트 코드 외의 표현 형식을 다룰 수도 없습니다.
받는 표현은 무엇이든 즉시 자바스크립트로 실행됩니다.

src 속성에 새 객체를 참조하는 기본 기법 자체는, 맞춤 생성된 자바스크립트가 아니라 다른 리소스를 가져오는 데 쓰면 더 안전합니다.
script만 브라우저에 표현을 불러오게 하는 HTML 태그가 아닙니다.
img와 frame도 유용합니다.
Google Maps는 지도 타일 이미지를 가져올 때 XMLHttpRequest 호출이 아니라 img 태그를 씁니다.
Google의 자바스크립트 코드가 HTTP 요청을 직접 하는 것이 아니라, img 태그를 만들고 브라우저가 부수 효과로 이미지를 요청하게 두는 것입니다.

#### 라이브러리 지원

Jason Levitt은 JoD를 쉽게 해 주는 JSONscriptRequest라는 자바스크립트 클래스를 작성했습니다.
이 클래스는 XMLHttpRequest와 비슷하게 동작하되 HTTP 기능을 더 적게 지원하고, 서버가 XML 표현을 보낼 것으로 기대하는 대신 자바스크립트 조각을 기대합니다.

이미지 검색 애플리케이션의 동적 구현은 다음과 같은 callYahoo 함수를 정의합니다.
이 함수는 사용자가 HTML 폼에서 전송 버튼을 누를 때 촉발됩니다.

```javascript
function callYahoo() {
  var query = document.getElementById("query").value;
  var uri = "http://api.search.yahoo.com/ImageSearchService/V1/imageSearch" +
            "?query=" + escape(query) +
            "&appid=restbook&output=json&callback=formatImages";
  alert(uri);

  var request = new JSONscriptRequest(uri);
  request.buildScriptTag();
  request.addScriptTag();
}
```

리소스 URI를 JSONscriptRequest 객체에 넘기면 addScriptTag 메서드가 새 script 태그를 DOM에 끼워 넣습니다.
브라우저가 그 새 태그를 처리하면 외부 URI로 GET 요청을 보내고 표현으로 제공된 자바스크립트를 실행합니다.
URI 질의 문자열에 callback=formatImages를 지정했으므로 야후는 복잡한 자료 구조에 formatImages 함수를 호출하는 자바스크립트를 제공합니다.
이 Ajax 애플리케이션은 어디서든 제공할 수 있고, 브라우저 경고 없이 야후 이미지 검색으로 무엇이든 검색할 수 있습니다.

Dojo 라이브러리는 이 편법을 쓰는 dojo.io.SrcScript 전송 클래스를 제공해 script 편법을 쉽게 만듭니다.
또한 iframe 태그를 이용하는 비슷한 편법을 쓰는 dojo.io.IframeIO 클래스도 제공합니다.
이 편법 역시 서버의 협조가 필요하지만, 응답 문서를 자동으로 코드로 실행하지 않는다는 장점이 있습니다.

## 핵심 정리

Ajax의 본질은 특정 기술이 아니라 아키텍처입니다.
브라우저 안에서 실행되는 웹 서비스 클라이언트라면 JavaScript나 XML을 쓰지 않더라도 Ajax이며, 그래서 두문자어 AJAX가 그냥 단어 Ajax로 바뀌었습니다.

Ajax 아키텍처는 클라이언트 측 GUI 애플리케이션과 같은 구조를 가져 데스크톱 앱처럼 매끄럽게 동작합니다.
그러나 그 대가로 모든 애플리케이션 상태가 하나의 URI를 공유하게 되어 주소 지정 가능성과 무상태성이 파괴되기 쉽습니다.
Gmail이 이를 잃은 예라면 Google Maps는 a 태그에 퍼머링크를 유지해 되살린 예로, 좋은 설계로 REST의 이점을 사용자에게 돌려줄 수 있음을 보여줍니다.

XMLHttpRequest는 open, onreadystatechange, setRequestHeader, send로 요청을 만들고, readyState가 4가 되면 status, responseXML, responseText, getResponseHeader로 응답을 처리합니다.
브라우저는 XML을 자동으로 DOM 트리로 파싱하며, 같은 DOM 메서드로 응답 데이터와 화면 HTML을 모두 조작합니다.
JSON은 자바스크립트 자료 구조가 곧 유효한 프로그램이라는 성질 덕분에 이 환경에 특히 잘 맞습니다.

Ajax가 소비하는 서비스도 주소 지정 가능성과 무상태성 등의 이유로 RESTful해야 하며, 유능한 HTTP 클라이언트인 브라우저 환경은 오히려 REST의 논거를 강화합니다.
브라우저 간 차이(구버전 IE의 ActiveX, 사파리의 PUT/DELETE 미지원, IE의 무기한 캐싱)는 크로스 브라우저 래퍼와 ETag/Cache-Control, Prototype이나 Dojo 같은 라이브러리로 다룹니다.

브라우저의 동일 출처 정책(same-origin policy)은 도메인 A의 코드가 도메인 B로 요청하는 것을 막습니다.
이를 우회하는 요청 프록시와 JoD는 모두 편법이며, 특히 JoD는 외부 코드를 무조건 실행하므로 XMLHttpRequest보다 위험하고 GET만 가능해 REST 관점에서도 불구가 된 클라이언트를 강요합니다.
프록시든 JoD든 외부 서버의 행위와 클라이언트의 요청에 대한 책임을 Ajax 프로그래머에게 떠넘기므로, 안전한 정공법은 서명된 스크립트로 명시적 권한을 얻는 것이지만 이 역시 브라우저 호환성과 설정 부담이라는 대가가 따릅니다.
