import ImportPackage as ImportPackage

virtual_switch = ImportPackage.AlphaSwitch()
virtual_switch.setup(port=25505, address="Your IP-Address")
virtual_switch.startLog()

for i in range(1024):
    virtual_switch.handleTraffic()
    print(virtual_switch.getNewestLog)