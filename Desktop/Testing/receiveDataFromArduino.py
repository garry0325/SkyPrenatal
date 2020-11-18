import bluetooth


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
    data=socket.recv(64)
    data=data[:data.find('\n')]
    socket.close()
    return data

message=receiveDataFromArduino(sensorMACAddress,sensorPort)
print message
