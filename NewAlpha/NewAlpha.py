"""
    NewAlpha
    --------
This module provides a pre-built network infrastructure for connecting multiple clients via a virtual switch.
Sockets are used to establish a connection that takes port and address as arguments.
-------
Following classes are essential:

- AlphaClient (Used to connect to other clients or switches)  
- AlphaSwitch (Used to manage data flows)
"""

import time
import socket
from typing import Union

class MissingAddressSetup(Exception):
    def __init__(self) -> None:
        self.message = "The Address and Port was not defined. Setup the address data using AlphaSwitch.setup(port, address) or AlphaClient.setup(port, address)"
        super().__init__(self.message)

class AlphaSwitch:
    """
    Virtual-Switch (used to manage data flows)

    Simple setup:
    >>> virtual_switch = AlphaSwitch()
    >>> while True:
    >>>     virtual_switch.handleTraffic()
    """
    switch_address: str = None 
    switch_port: int = 25505
    _startlog = False

    def __init__(self) -> None:
        self.transfer_count: int = 0 #Counts the amount of packages handled
        self.clients_data: dict = {} #Saves the address of every connected port (Port:Address)
        self.black_list: list = [] #Blacklist for non responding clients
        self.log: list = [] #Saved logs

    def setup(self, port: int = None, address: str = None) -> None:
        """Change the address data of the switch."""
        if port is not None: self.switch_port = port
        if address is not None: self.switch_address = address

    @classmethod
    def startLog(cls) -> None:
        """Start recording traffic and enable logging."""
        cls._startlog = True

    @classmethod
    def stopLog(cls) -> None:
        """Stop recording traffic and disable logging."""
        cls._startlog = False

    @property
    def getNewestLog(self) -> str:
        """Returns the newest recorded log."""
        return str(self.log[-1])
    
    @property
    def getFullLog(self) -> list:
        """Returns the entire logging history."""
        return self.log

    def handleTraffic(self) -> tuple[str, str, int, int, str]:
        """
        Handles/Manages all data flow from clients.
        Return order: (response, sender_address, sender_port, recipient_port, decoded_data)
        """
        if self.switch_address is None: raise MissingAddressSetup 

        port_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_socket.bind((self.switch_address, self.switch_port))
        port_socket.listen(1)

        switch_socket, address = port_socket.accept()
        start_handle_time = time.time()
        decoded_data = str(switch_socket.recv(4096).decode()) #Raw data (sPORT:Message:rPORT)

        sender_port, recipient_port, str_data = (
            int(decoded_data[:5]),
            int(decoded_data[-5:]),
            decoded_data[6:-6],
        )

        if sender_port not in (self.clients_data).keys(): 
            self.clients_data[int(sender_port)] = str(address[0]) #Add address for the port (Port:Address)

        sender_address = None
        if int(recipient_port) in (self.clients_data.keys()):
            sender_address: str = self.clients_data[sender_port]

            responded: int = 0
            response = None
            while responded < 2:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((sender_address, recipient_port))
                    client_socket.sendall(decoded_data.encode())
                    message_response = client_socket.recv(4096).decode()
                    client_socket.close()
                    response = f"{recipient_port}:{message_response}:{sender_port}" #Format response (sPort:Message:rPort) 
                    while recipient_port in self.black_list: self.black_list.remove(recipient_port) #Remove port from blacklist if port is responding
                    responded = 2
                except Exception:
                    responded+=1
                    time.sleep(0.25)

            if response is None: 
                response = f"{AlphaSwitch.switch_port}:$E5 [NoResponse] 'The client has been disconnected or traffic could be high? (request-timeout?)':{sender_port}"
                self.black_list.append(recipient_port) #Add to blacklist if not responding
                if sum(1 for black_list_port in self.black_list if black_list_port == recipient_port) == 3 and recipient_port in self.clients_data.keys(): del self.clients_data[recipient_port] #remove the port from connections if port isn't responding 3 times
        else: response = f"{AlphaSwitch.switch_port}:$E4 [NotFound] 'This client is not connected to the network.':{sender_port}"
        if int(recipient_port) == AlphaSwitch.switch_port and str_data != "@all": response = f"{AlphaSwitch.switch_port}:$R1 [Registered]:{sender_port}" #AlphaClient.registerSwitch() response
        if int(recipient_port) == AlphaSwitch.switch_port and str_data == "@all": response = f"{AlphaSwitch.switch_port}:{list(self.clients_data.keys())}:{sender_port}" #all connected ports response
        
        try: switch_socket.sendall(str(response).encode()) #return the respond from the recipient to original sender
        except ConnectionResetError: pass
        end_time = time.time()
        self.transfer_count += 1
        elapsed_time = round(end_time - start_handle_time, 5)

        switch_socket.close()
        port_socket.close()

        if AlphaSwitch._startlog: self.log.append(f"Package[{self.transfer_count}]: \t {decoded_data} \t -> ({elapsed_time}s) -> \t {response}") #Record log
        return (response, sender_address, sender_port, recipient_port, decoded_data)

class AlphaClient:
    """
    Virtual-Client (used to connect to other clients or switches). Use cases:
    - Server
    - Client 
    """
    def __init__(self) -> None:
        self.address_: str = None #Client address
        self.port_: int = 14606 #Client port

        self.switch_address: str = None #Bridged switch address
        self.switch_port: int = 25505 #Bridged switch port

        self.flag_: bool = False #Thread kill flag

    def setup(self, port: int = None, address: str = None) -> None:
        """Set/Change the address data of the client."""
        if port is not None: self.port_ = port
        if address is not None: self.address_ = address

    def bridge(self, port: int = None, address: str = None) -> None:
        """Specify the address data of the switch for the connection."""
        if port is not None: self.switch_port = port
        if address is not None: self.switch_address = address

    def responseFlag(self) -> None: 
        """Kills the auto-response thread by using a flag."""
        self.flag_ = True

    @staticmethod
    def __sending_data__(port: int, address: str, data: str) -> Union[str, None]:
        for i in range(3):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((address, port))
                client_socket.sendall(data.encode())
                response: str = str(client_socket.recv(4096).decode()) #Raw data (sPort:Message:rPort)
                client_socket.close()
                return response
            except Exception: time.sleep(0.5)
        return None

    def registerSwitch(self) -> None:
        """Establishes a connection to the switch in advance so that the switch can register the client."""
        if self.address_ is None or self.switch_address is None: raise MissingAddressSetup
        self.__sending_data__(port=self.switch_port, address=self.switch_address, data=f"{self.port_}:Register:{self.switch_port}")

    def request(self, message: str, not_switch_port: int = None, not_switch_address: str = None) -> tuple[str, int]:
        """
        @specific
        
        Requests a data packet and returns the response from the request recipient (can be used for data trading).
        Return order: (response_data, sender_port, recipient_port)
        """
        if self.address_ is None or self.switch_address is None: raise MissingAddressSetup
        if not_switch_port is None: not_switch_port = self.switch_port 
        if not_switch_address is None: not_switch_address = self.switch_address

        decoded_data = self.__sending_data__(port=not_switch_port, address=not_switch_address, data=message) #Raw data (sPort:Message:rPort)

        if decoded_data is not None:
            sender_port, recipient_port, str_data = (
                int(decoded_data[:5]),
                decoded_data[-5:],
                decoded_data[6:-6],
            )

            return (str_data, sender_port)
        else:
            return (None, None)
        
    def encode_format(self, message: str, port: int = None) -> str: 
        """
        Encode the message into the correct format so that the data can be further processed and sent.
        Format: 'SENDER_PORT:MESSAGE:RECIPIENT_PORT'
        """
        if port is None: port = self.switch_port
        return f"{self.port_}:{message}:{port}" #Format response (sPort:Message:rPort) 
    
    def frozenResponse(self, ruleset: dict, flag: bool = True) -> None:
        """
        Automatically handles the client's response based on a specific predefined set of rules (dict).
        
        ruleset = {
            request:response
            (key):(value)
        }
        """
        if self.address_ is None or self.switch_address is None: raise MissingAddressSetup
        while not (flag and self.flag_):
            try:
                port_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port_socket.bind((self.address_, self.port_))
                port_socket.listen(1)

                switch_socket, address = port_socket.accept()
                decoded_data = str(switch_socket.recv(4096).decode()) #Raw data (sPort:Message:rPort)

                str_data = decoded_data[6:-6] #Message only from raw data
                if str_data in ruleset.keys(): response = ruleset[str_data] #set response to value from ruleset key
                else: response = None
                
                switch_socket.sendall(str(response).encode())
                switch_socket.close()
                port_socket.close()
            except Exception: pass
    
    def dynamicResponse(self, dyn_ruleset: dict, refresh_time: float) -> tuple[str, str, int]:
        """
        Handles the client's response based on a specific dynamically changeable ruleset (dict).
        
        ruleset = {
            request:response
            (key):(value)
        }
        """
        if self.address_ is None or self.switch_address is None: raise MissingAddressSetup
        try:
            port_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port_socket.settimeout(refresh_time)
            port_socket.bind((self.address_, self.port_))
            port_socket.listen(1)

            switch_socket, address = port_socket.accept()
            decoded_data = str(switch_socket.recv(4096).decode()) #Raw data (sPort:Message:rPort)

            sender_port = int(decoded_data[:5])
            str_data = decoded_data[6:-6]  #Message only from raw data
            if str_data in dyn_ruleset.keys(): response = dyn_ruleset[str_data]  #set response to value from dyn_ruleset key
            else: response = None
            
            switch_socket.sendall(str(response).encode())
            switch_socket.close()
            port_socket.close()
            return (str(str_data), str(response), sender_port)
        except Exception: return (None, None, None)

    def confirmationResponse(self, confirmation_message: str) -> tuple[str, int]:
        """
        Returns the received request data and responds with a arrival confirmation.
        Return order: (Message, Sender_Port)
        """
        if self.address_ is None or self.switch_address is None: raise MissingAddressSetup
        while True:
            try:
                port_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port_socket.bind((self.address_, self.port_))
                port_socket.listen(1)

                switch_socket, address = port_socket.accept()
                decoded_data = str(switch_socket.recv(4096).decode()) #Raw data (sPort:Message:rPort)

                if decoded_data is not None:
                    sender_port, recipient_port, str_data = (
                    int(decoded_data[:5]),
                    decoded_data[-5:],
                    decoded_data[6:-6],
                )
                
                switch_socket.sendall(confirmation_message.encode())
                switch_socket.close()
                port_socket.close()

                return (str_data, sender_port)
            except Exception: pass