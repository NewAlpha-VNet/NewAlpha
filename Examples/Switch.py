import NewAlpha

virtual_switch = NewAlpha.AlphaSwitch()
virtual_switch.switchSetup(port=25505, address="Your IP-Address")
virtual_switch.startLog()

while True:
    virtual_switch.handleTraffic()
    print(virtual_switch.getNewestLog)