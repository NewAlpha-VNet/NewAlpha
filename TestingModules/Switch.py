import ImportPackage

virtual_switch = ImportPackage.AlphaSwitch()
virtual_switch.setup(port=25505, address="192.168.56.1")
virtual_switch.startLog()

for i in range(1000):
    virtual_switch.handleTraffic()
    newlog = virtual_switch.getNewestLog
    print(newlog)
print(virtual_switch.getFullLog)