import random
import ImportPackage as ImportPackage
import threading
import time

client = ImportPackage.AlphaClient()
client.setup(23456, "Your IP-Address")
client.bridge(25505, "Your IP-Address")
client.registerSwitch()

def requester():
    while True:
        time.sleep(0.01)

        random_choice = random.choice(["Hello Flynn!", "Bye Flynn!"])
        message = client.encode_format(random_choice, 34567)

        response, port = client.request(message=message)
        print(response, port)

ruleset = {
    "Bye Flynn!":"Have a great time!",
    "Hello Flynn!":"Hi, how are you?"
}

catcher = threading.Thread(target=client.frozenResponse, args=(ruleset, True))
thread_ = threading.Thread(target=requester)

thread_.start()
catcher.start()