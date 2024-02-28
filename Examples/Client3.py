import ImportPackage as ImportPackage

client = ImportPackage.AlphaClient()
client.setup(23456, "Your IP-Address")
client.bridge(25505, "Your IP-Address")
client.registerSwitch()

while True:
    received_data, port = client.confirmationResponse("Got it, thanks!")
    print(received_data, port)