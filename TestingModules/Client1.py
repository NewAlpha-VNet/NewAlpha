import random
import ImportPackage
import threading
import time

client = ImportPackage.AlphaClient()
client.setup(34567, "192.168.56.1")
client.bridge(25505, "192.168.56.1")
client.registerSwitch()

def responder():
    while True:
        time.sleep(0.01)
        message = client.encode_format(random.choice(["Hello Flynn!", "Bye Flynn!"]), 23456)
        response, port, address = client.request(message=message)
        print(f"\n{port}\t{address}\n{response}")

ruleset = {
    "Bye Flynn!":"Have a great time!",
    "Hello Flynn!":"Hi, how are you?"
}

catcher = threading.Thread(target=client.frozenResponse, args=(ruleset,))
thread_ = threading.Thread(target=responder)

thread_.start()
catcher.start()