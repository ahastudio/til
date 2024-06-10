# OPC (Open Platform Communications)

OPC Foundation: <https://opcfoundation.org/>

## 간단한 히스토리

참고: <https://opcfoundation.org/about/opc-foundation/history/>

- OPC Classic은 “OLE for Process Control”의 약자로 시작됨(1996년).
- OPC UA를 만들고, “Open Platform Communications”의 약자로 변경(2011년).

## OPC UA (Unified Architecture)

> The OPC Unified Architecture (UA), released in 2008, is a
> platform independent service-oriented architecture that integrates
> all the functionality of the individual OPC Classic specifications
> into one extensible framework.

<https://opcfoundation.org/about/opc-technologies/opc-ua/>

### UA Part 1: Overview and Concepts - 5 Overview

<https://reference.opcfoundation.org/Core/Part1/v105/docs/5>

![OPC UA target applications](https://reference.opcfoundation.org/api/image/get/6/image004.png)

### OPC UA 라이브러리

OPC UA는 OPC Classic보다 현대적이라,
라이브러리만 있으면 서버와 클라이언트 모두 개발 가능하다.

- Python: <https://github.com/FreeOpcUa/opcua-asyncio>
- Go: <https://github.com/gopcua/opcua>
- Node.js: <https://github.com/node-opcua/node-opcua>

## OPC Classic

플랫폼 독립적인 현대적인 통신 방식이 자리 잡기 전에 제안된 방식.
COM/DCOM을 이용해 통신한다.

> The OPC Classic specifications are based on Microsoft Windows technology
> using the COM/DCOM (Distributed Component Object Model) for the exchange
> of data between software components.

<https://opcfoundation.org/about/opc-technologies/opc-classic/>

- OPC DA (Data Access)
- OPC AE (Alarms & Events)
- OPC HDA (Historical Data Access)

### OpenOPC 2

개발이 중단된 OpenOPC를 완전히 리팩터링함.

OpenOPC Gateway Service를 경유해 Windows가 아닌 다른 환경(리눅스, 맥)에서도
OPC DA 클라이언트 프로그래밍을 하는 게 큰 강점.

> OpenOPC 2 is a Python Library for OPC DA.
> It is Open source and free for everyone.
> It allows you to use OPC Classic (OPC Data Access) in modern Python
> environments.
> OPC Classic is a pure Windows technology by design, but this library
> includes a Gateway Server that lets you use OPC Classic on any architecture
> (Linux, MacOS, Windows, Docker).
> So this Library creates a gateway between 2022 and the late 90ties.
> Like cruising into the sunset with Marty McFly in a Tesla.

<https://github.com/iterativ/openopc2>

OpenOPC Gateway Proxy에서 [Pyro 5](https://github.com/irmen/Pyro5)를 사용.

관련 코드:
<https://github.com/iterativ/openopc2/blob/develop/openopc2/gateway_proxy.py>

### OpenOPC for Python

파이썬용 OPC DA 클라이언트 라이브러리.
현재는 개발 중단됨.

- <https://openopc.sourceforge.net/>
- <https://github.com/sightmachine/OpenOPC>

### OPC DA in Go

Go로 프로그래밍할 수 있는 라이브러리도 제공하지만,
CLI에서 사용할 수 있는 도구를 바로 써먹기 좋다.

<https://github.com/konimarti/opc>

### Npde.js 라이브러리

- OPC DA 통신 라이브러리: <https://github.com/st-one-io/node-opc-da>
- DCOM 라이브러리: <https://github.com/st-one-io/node-dcom>

### OLE Automation

COM은 `IUnknown`만 구현하면 되지만, Automation은 `IDispatch`를 구현한다.

[Data Access Automation Interface Standard 버전 2.02 스펙 문서 (PDF)](https://www-bd.fnal.gov/controls/opc/OPC_DA_Auto_2.02_Specification.pdf)
