import sys
import time
import bluetooth
import threading
import socket
from multiprocessing import Queue
from PyQt4 import QtGui,QtCore

import RPi.GPIO as GPIO
import MFRC522
import signal


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(31,GPIO.OUT)

remoteIP="192.168.31.180"
remotePort=8000

scaleBTAddress='98:D3:31:40:4A:89'
scaleBTPort=1

pressureBTAddress='98:D3:31:60:26:BD'
pressureBTPort=1


MIFAREReader=MFRC522.MFRC522()


class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window,self).__init__()
        self.setWindowTitle("Health Inspection Assistent")
        self.setGeometry(50,50,500,300)
        self.IDNoticeLabel=QtGui.QLabel(self)
        self.IDNoticeLabel.move(90,140)
        self.IDNoticeLabel.setFont(QtGui.QFont("",15))
        self.IDNoticeLabel.resize(350,30)
        self.IDNoticeLabel.setText("Place Your ID Card On Reader...")
        
        self.initialize()

    def initialize(self):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))

        

        
        self.nameStaticLabel=QtGui.QLabel(self)
        self.nameStaticLabel.move(300,10)
        self.nameLabel=QtGui.QLabel(self)
        self.nameLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.nameLabel.move(350,10)
        self.nameLabel.resize(150,30)
        self.birthStaticLabel=QtGui.QLabel(self)
        self.birthStaticLabel.move(315,30)
        self.birthLabel=QtGui.QLabel(self)
        self.birthLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.birthLabel.move(350,30)
        self.bloodStaticLabel=QtGui.QLabel(self)
        self.bloodStaticLabel.move(301,50)
        self.bloodLabel=QtGui.QLabel(self)
        self.bloodLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.bloodLabel.move(350,50)
        self.lastStaticLabel=QtGui.QLabel(self)
        self.lastStaticLabel.move(265,70)
        self.lastLabel=QtGui.QLabel(self)
        self.lastLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.lastLabel.move(350,70)
                                    
        self.weightStaticLabel=QtGui.QLabel(self)
        self.weightStaticLabel.move(10,10)        
        self.weightLabel=QtGui.QLabel(self)
        self.weightLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.weightLabel.move(80,10)
        self.pressureStaticLabel=QtGui.QLabel(self)
        self.pressureStaticLabel.move(10,30)
        self.pressureLabel=QtGui.QLabel(self)
        self.pressureLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.pressureLabel.move(80,30)

        print "UI done"
        
        #self.showFullScreen()
        self.show()

    def showLabels(self):
        self.nameStaticLabel.setText("Name: ")
        self.birthStaticLabel.setText("Age: ")
        self.bloodStaticLabel.setText("Blood: ")
        self.lastStaticLabel.setText("Last Check: ")
        self.weightStaticLabel.setText("Weight: ")
        self.pressureStaticLabel.setText("Blood Pressure: ")
        
        
        self.show()


    

    
def receiveBTData(MACAddress,port):
    while True:
        try:
            socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print "Connecting "+MACAddress+"..."
            socket.connect((MACAddress,port))
        except:
            print "Target not detected, reconnecting..."
            time.sleep(3)
            continue
        break
    print "Connected to Bluetooth device."

    weight="-1"
    while 1:
        data=socket.recv(1024)
        if len(data)>=3:
            print data
            if data.find('#') != -1:
                print "Sending "+weight+" to remote server "+remoteIP+"..."
                sendData(remoteIP,remotePort,weight)
                data=socket.recv(1024)
                data=socket.recv(1024)
                data=socket.recv(1024)
                break
            weight=data
            GUI.weightLabel.setText(weight+" KG")
            
        #time.sleep(1)
    socket.close()
    print "Bluetooth session ended."

def sendData(IPAddress,port,dataToSend):
    skt=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            skt.connect((IPAddress,port));
            print "Connected to remote server."
            break
        except Exception:
            print "Connection failed...Retry"
            time.sleep(5)
            continue
    first=0
    while True:
        skt.send(dataToSend)
        data=skt.recv(64)
        data=data[:data.find(chr(0))]
        if data==dataToSend and first==1:
            print "Data sent successfully."
            break
        first=1
    print "Internet session ended."
    skt.close()
    
def scanCard():
    data=[]
    block=1
    GPIO.output(31,GPIO.HIGH)
    while True:
        if block>6: break 
        #print "Start scanning card."
        (status,tagType)=MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL) #Scan for cards

        #if status==MIFAREReader.MI_OK:
            #print "Card detected."
        (status,uid)=MIFAREReader.MFRC522_Anticoll() #Get UID

        if status==MIFAREReader.MI_OK:
            if block==1:
                socketInternet.send("21")
                print "scaning..."
            GUI.IDNoticeLabel.setText("")
            GUI.showLabels()
            #print "UID: %s-%s-%s-%s" % (uid[0],uid[1],uid[2],uid[3])
            key=[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] #Default key for authentication
            MIFAREReader.MFRC522_SelectTag(uid) #Select the scanned tag
            status=MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid) #Authenticate
            
            if status==MIFAREReader.MI_OK:
                data=MIFAREReader.MFRC522_Read(block)
                MIFAREReader.MFRC522_StopCrypto1()
                if block==1: GUI.nameLabel.setText(toStr(data))
                if block==2: GUI.birthLabel.setText(toStr(data))
                if block==4: GUI.bloodLabel.setText(toStr(data))
                if block==5:
                    GUI.lastLabel.setText(toStr(data))
                    GPIO.output(31,GPIO.LOW)
                
                block=block+1
            else:
                print "Error Authenticate."

    print "Scanning end."

def toStr(data):
    return ''.join(chr(x) for x in data)

    


    
app=QtGui.QApplication(sys.argv)
GUI=Window()


tScanCard=threading.Thread(target=scanCard)
tScanCard.start()
    




#t=threading.Thread(target=receiveBTData,args=(scaleBTAddress,scaleBTPort,))
#t.start()

#b=threading.Thread(target=receiveBTData,args=(bloodBTAddress,bloodBTPort,))
#b.start()

sys.exit(app.exec_())
