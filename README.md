# NewAlpha Framework
An Easy to use Open-Source Virtual Networking Framework for Python. Including Switches and Clients/Servers.

> [!NOTE] 
> This framework is still in _beta_ and does not yet have all the features presented.
> 
> _Coming soon: **The Alpha Update**_

## Solution
Offers a comprehensive networking solution designed to simplify the process of building and managing network infrastructures. With its user-friendly interface and pre-built infrastructure, NewAlpha eliminates the complexity of setting up networking systems. Whether for IoT applications or communication between virtual machines, NewAlpha provides a seamless experience, enabling users to easily change network configurations or manage logging systems for package tracing.

## How it works
NewAlpha is based on the Socket library, and simplifies its use. Create a virtual switch that contains a logging system to track or observe data packets. Clients are then able connect to the switch via sockets and can request/respond to other clients or servers. The data packets are structured as follows: `sender_port : message/parameter/commands : receiver_port` or as a concrete example: `25505:Hello World!:80880`. 

***Detailed:***

Each packet contains three main components: the sender's port number, the message, parameter, or command being transmitted, and the receiver's port number. This format ensures clear identification of both the source and destination of each packet, along with the content being conveyed. For instance, a typical packet might appear as follows: '25505:Hello World!:80880,' where '25505' represents the sender's port, 'Hello World!' denotes the message or payload, and '80880' signifies the receiver's port. Every virtual object communicates with such structure.

## Usage and implementation
```cmd
pip install NewAlpha
```
```python
import NewAlpha
```
### Switch setup + run:
```python
virtual_switch = NewAlpha.VSwitch()
virtual_switch.setup(port=25505, address="Your IP-Address") #Change Port and IP
while True:
    virtual_switch.handle()
```
In this example, we first create an instance of the _switch_ class, then set up the switch's address data with port and address arguments. Subsequently, we run a loop to continuously handle client requests.
### Client/Server setup:
```python
client = NewAlpha.VClient()
client.setup(80880, "Your IP_Address") #Change Client's Port and IP
client.bridge(25505, "Switch IP_Address") #Enter the Switch Port and IP
client.connect_to_switch()
```
As previously, we instantiate an object and then configure the address details of the client and the switch. We then register the client on the switch (optional but recommended).
### Client/Server response:
The virtual client/server has 3 types of response methods: _`frozen_response()`, `dynamic_response()`_ and _`manual_response()`_ which is experimental (as of February 26, 2024) and therefore not really recommended for serious use.

***frozen_response():***
```python
import threading

... #Previous Client Setup

def auto_respond():
  #key=request:value=response
  ruleset = {
  "Hi Flynn!":"Hi! How are you?" 
  }
  client.frozen_response(ruleset)

auto_respond_thread = threading.Thread(target=auto_respond)
auto_respond_thread.start()
```
If you want to send messages while handling requests, you need threads. The _`frozen_response()`_ method takes a set of rules as an argument to respond to a specific request with the correct answer. As the name suggests, the ruleset is frozen in a specific state, so there is no way to change it while the responding method processes it.

***dynamic_response():***
```python
def auto_respond():
  while True:
    ... #Update ruleset for every new refresh/request
    client.dynamic_response(ruleset=ruleset, refresh_time=1.0)

auto_respond_thread = threading.Thread(target=auto_respond)
auto_respond_thread.start()
```
Compared to the frozen response, the dynamic is able to change the ruleset every time the method is refreshed. Additionally, refresh_time requires a time argument, so the method waits for a specific amount of time for a request before it aborts. This is useful, for example, if you want to update the ruleset every second. _(Side info: the method returns request, response, sender_port in exact that order)_

***manual_response():***

I will skip this method for this very reason as it is experimental and has a lot of changes pending. This documentation will be updated when the method has been tested and is working as planned. If you are still interested, you can take a look at the source code (currently dynamic response is the most advanced way to answer queries).

### Client/Server request:
For responses there is a manual_request() method, but also a send() method. The same as before. We skip the manual method because of the experimental status.

***send():***
```python
def send_single_message():
  encoded_message = client.encode_format("Hi Flynn!", 70770) #Message, ReceiverPort
  response, port, address = client.send(message=encoded_message)
```
Before sending a data packet, the message must be encoded/formatted using the encode_format() method.
## Benchmark
> Average Benchmark Results

| Clients-Amount | Package-Respond-Time | Latency-Drop-Time |
| :---:        |     :---:      |        :---:  |
| 5            | 13ms           |~700ms (<1s)   |
| 3            | 5ms            | ~670ms        |
| 2            | 1-2ms (<3ms)   | ~500ms        |

_Latency-Drop-Time explained: Worst case scenario when the switch has overlapping requests or is overloaded (Worst Package-Respond-Time)._
`PackageMaxSize` = 4096 bytes of string 
