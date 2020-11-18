import socket
import time
import sys

clientIP="192.168.31.73"
clientPort=8000

socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind((clientIP,clientPort))
socket.listen(1)
print "Listening..."
socketCon,(clientIP,clientPort)=socket.accept()
print "Connection accepted from %s at port %d"%(cleintIP,clientPort)
print "Receiving..."
while True:
    try:
        data=socketCon.recv(512)
        if len(data)>0:
            print data
            break
        else:
            continue
    except Exception:
        socket.close()

socket.close()
