![](https://cdn.discordapp.com/attachments/810456487729168415/1212791942379737210/NewAlphaLogoNEW.png?ex=65f31f83&is=65e0aa83&hm=7e9227058f23157a7face29c91cb5f55c48126205f040536966a6828ff6f4656&)

***An Easy to use Open-Source Virtual Networking Framework for Python. Including Switches and Clients/Servers.***

> [!NOTE] 
> This framework is still in _Beta_ and may have malfunctions. In this case we would be happy to receive feedback.
> 
> _Upcoming: **The Alpha Update**_

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
### Switch setup and traffic handling:
```python
switch = NewAlpha.AlphaSwitch()
switch.setup(port=25505, address="Your IP-Address") #Change Port and IP
while True:
    switch.handleTraffic()
```
In this example, we first create an instance of the _switch_ class, then set up the switch's address data with port and address arguments. Subsequently, we run a loop to continuously handle client requests.

### Switch logging system:
The logging system is particularly useful when you want to track packets on the network or when troubleshooting with data transmission and cannot find the problem. These are the methods for managing the log:
```python
... #Previous switch setup

switch.startLog() #Starts recording the traffic
switch.stopLog() #Stops recording the traffic
log_str = switch.getNewestLog #Returns the newest log (datatype: str)
log_list_of_str = switch.getFullLog #Returns the entire logging list (datatype: list containing str)
```
It's good to know that the log is stored as/in RAM.

### Client/Server setup:
```python
client = NewAlpha.AlphaClient()
client.setup(80880, "Your IP_Address") #Change Client's Port and IP
client.bridge(25505, "Switch IP_Address") #Enter the Switch Port and IP
client.registerSwitch()
```
As previously, we instantiate an object and then configure the address details of the client and the switch. We then register the client on the switch (optional but recommended).
### Client/Server response:
The virtual client/server has 3 types of response methods: _`frozenResponse()`_ , _`dynamicResponse()`_ and _`confirmationResponse`_.

***frozenResponse():***
```python
import threading

... #Previous client setup

def auto_respond():
  #key=request:value=response
  ruleset = {
  "Hi Flynn!":"Hi! How are you?" 
  }
  client.frozenResponse(ruleset)

auto_respond_thread = threading.Thread(target=auto_respond)
auto_respond_thread.start()
```
If you want to send messages while handling requests, you need threads. The _`frozenResponse()`_ method takes a set of rules as an argument to respond to a specific request with the correct answer. As the name suggests, the ruleset is frozen in a specific state, so there is no way to change it while the responding method processes it.

***dynamicResponse():***
```python
def auto_respond():
  while True:
    ... #Update ruleset for every new refresh/request
    client.dynamicResponse(ruleset=ruleset, refresh_time=1.0)

auto_respond_thread = threading.Thread(target=auto_respond)
auto_respond_thread.start()
```
Compared to the frozen response, the dynamic is able to change the ruleset every time the method is refreshed. Additionally, refresh_time requires a time argument, so the method waits for a specific amount of time for a request before it aborts. This is useful, for example, if you want to update the ruleset every second. _(Side info: the method additionally returns request, response, sender_port in exact that order)_

***confirmationResponse():***

```python
def auto_respond():
    while True:
        received_data, port = client.confirmationResponse("Got it, thanks!")
        print(received_data, port) #Can be used to build a chat-programm

auto_respond_thread = threading.Thread(target=auto_respond)
auto_respond_thread.start()
```
This method was specifically designed to enable dynamic context-based exchanges. What does that mean? In short, you could for example use it to create a chat application. If you want to respond to a request tailored to the message you receive, you can set up a system so you have enough time to respond. However, the method itself always responds with the save confirmation message.

### Client/Server request:
The following method is the only way to request packages to any recipient. You don't always have to send it directly to the switch, you can also use it to transfer data to other networks (Then no encoding of the message is required).

***request():***
```python
def send_package():
  encoded_message = client.encode_format("Hi Flynn!", 70770) #Message, ReceiverPort
  response, port, address = client.request(message=encoded_message)
```
Before sending a data packet, the message must be encoded/formatted using the encode_format() method. As mentioned before into the following form: `25505:Hi Flynn!:70770`.
## Benchmark
> Average Benchmark Results (for the constant package sending pause of 10ms).

| Clients-Amount | Package-Respond-Time | Latency-Drop-Time |
| :---:        |     :---:      |        :---:  |
| 5            | 13ms           |~700ms (<1s)   |
| 3            | 5ms            | ~670ms        |
| 2            | 1-2ms (<3ms)   | ~500ms        |

_Latency-Drop-Time explained: Worst case scenario when the switch has overlapping requests or is overloaded (Worst Package-Respond-Time)._

### Additional Informations:

`PackageMaxSize` = 4096 bytes of string (Maximum message size)

`PortsDigitsLength` = min/max 5 digits

`MaxPortsRange` = 10000 up to 65535 (Ports are only permitted in this range)
