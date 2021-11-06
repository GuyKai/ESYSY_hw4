from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
from pprint import pprint
import threading
import struct
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr
            
class NotifyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
 
    def handleNotification(self, cHandle, data):
        try:
            print("Rev Data<{}>:{}".format(hex(cHandle),data))
            
        except:
            print("responsse_msg")
        
        
def notify(dev):
    while True:
        #print(flag)
        if flag :
            dev.waitForNotifications(0.1)
            #print('...')
        pass


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(5.0) # scan period
n=0
for dev in devices:
    print "%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr,dev.addrType, dev.rssi)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print " %s = %s" % (desc, value)
        
number = input('Enter your device number: ')
print('Device', number)
print(devices[number].addr)
    
print "Connecting..."
dev = Peripheral(devices[number].addr, 'random')
print ("Connected")

dev.withDelegate(NotifyDelegate())

ch1 = dev.getCharacteristics(uuid=UUID(0xa001))[0]
ch1_handle = ch1.getHandle()
ch1_notify_handle = ch1_handle + 1
ch2 = dev.getCharacteristics(uuid=UUID(0xa002))[0]
ch2_handle = ch2.getHandle()
ch2_notify_handle = ch2_handle + 1
print("Enable Notify")
#dev.writeCharacteristic(ch1_notify_handle, struct.pack('<bb',0x01,0x00))
dev.writeCharacteristic(ch2_notify_handle, struct.pack('<bb',0x01,0x00))
print("writing request sent")
dev.waitForNotifications(3)

global flag
flag = True

t = threading.Thread(target = notify ,args=(dev,))
t.setDaemon(True)
t.start()


while True :
    
    operation = raw_input('operation')
    flag = False
    time.sleep(0.1)
    #print(flag)
    print(operation)
    

    if operation == "finish":
        break

    elif operation == "read":
        try:
            testService = dev.getServiceByUUID(UUID(0xa000))
            for ch in testService.getCharacteristics():
                print str(ch)
            char = raw_input("which char?(EX:a001)")
            char = int(char,16)
                   
            ch = dev.getCharacteristics(uuid=UUID(char))[0]
            if (ch.supportsRead()):
                print ch.read()

        except:
            print("error")

    elif operation == "ledon":
        try:                  
            ch = dev.getCharacteristics(uuid=UUID(0xa003))[0]
            ch_handle = ch.getHandle()
            dev.writeCharacteristic(ch_handle, "\x01")
            print("LED_ON")
            
        except:
            print("error")
            
    elif operation == "ledoff":
        try:                  
            ch = dev.getCharacteristics(uuid=UUID(0xa003))[0]
            ch_handle = ch.getHandle()
            dev.writeCharacteristic(ch_handle, "\x00")
            print("LED_OFF")
                
        except:
            print("error")
    
    else:
        print("read/ledon/ledoff/finsih")
                
    
        
    print("done")
    flag = True

dev.disconnect()



