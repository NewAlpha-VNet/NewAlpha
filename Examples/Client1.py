import random
import NewAlpha
import threading
import time

client = NewAlpha.AlphaClient()
client.clientSetup(34567, "Your IP-Address")
client.bridge(25505, "Your IP-Address")
client.registerSwitch()

def requester():
    while True:
        time.sleep(0.01)

        random_choice = random.choice(["Hello Flynn!", "Bye Flynn!"])
        message = client.encode_format(random_choice, 23456)

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