import bluetooth
import socket
import time
import sys

serverIP="192.168.31.180"
serverPort=6000

socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

while True:
    try:
        socket.connect((serverIP,serverPort))
        print "Connected..."
        break
    except Exception:
        print "Connection failed...Retry"
        time.sleep(5)
        continue

data=socket.recv(1024)
print data
socket.send(sys.argv[1])
time.sleep(10)
socket.send("this is second send")


socket.close()
