import bluetooth
import time

sensorMACAddress='98:D3:31:40:4A:89' #Sensor MAC Address
sensorPort=1 #Typically 1

def receiveDataFromArduino(MACAddress,port):
    
    while True:
        try:
            socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print "connecting..."
            socket.connect((MACAddress,port))
        except:
            print "Target not detected, reconnecting..."
            continue
        break
    print "receiving..."
    while 1:
        data=socket.recv(64)
        if len(data)>3:
            print data+"\n"
        time.sleep(1)
        

receiveDataFromArduino(sensorMACAddress,sensorPort)
#message=receiveDataFromArduino(sensorMACAddress,sensorPort)
#print message
