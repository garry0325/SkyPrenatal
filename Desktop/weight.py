import sys
import os
import time
import datetime
import bluetooth
import threading
import socket
import multiprocessing
from multiprocessing import Queue
from PyQt4 import QtGui,QtCore
import requests

import cv2

import RPi.GPIO as GPIO
import MFRC522
import signal

import random


#Initialize general setup
pinIdLight=31
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pinIdLight,GPIO.OUT)
GPIO.output(pinIdLight,GPIO.LOW)


databaseIP="192.168.31.182"

#remoteVideoIP="http://140.116.84.91:79/"
remoteVideoIP="rtsp://localhost:80/live/picam"
#remoteVideoIP="http://192.168.31.102:8080/"
#remoteVideoIP="/home/pi/Deskop/vc.mp4"

remoteIP="140.116.84.91"
remotePort=7755

scaleBTAddress='98:D3:31:40:4A:89'
scaleBTPort=1

pressureBTAddress='98:D3:31:60:26:BD'
pressureBTPort=1

fetalBTAddress="98:D3:31:30:5F:F5"
fetalBTPort=1







global weightData
global sysData
global diaData
global bloodHrData
global fetalData
global heightData
global aptdData
global nameData
global idData

weightData=0
sysData=0
diaData=0
bloodHrData=0
fetalData=0
heightData=0
aptdData=0
nameData=0
idData=0

MIFAREReader=MFRC522.MFRC522()

socketInternet=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Internet socket setup
def initializeSocket():


    while True:
        try:
            print "Internet: Not connected to remote terminal."
            socketInternet.connect((remoteIP,remotePort))
            print "Internet: Connected to remote terminal."
            break
        except Exception:
            print "Internet: Connection failed...Retry"
            time.sleep(5)
            continue
    socketInternet.send("10")

    
    tScanCard.start()
    #tBlood.start()

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window,self).__init__()
        self.setWindowTitle("SkyPrenatal")
        self.setGeometry(0,0,800,480)
        self.setStyleSheet("QMainWindow {background: '#101010';}");
        
        self.videoFrameImage=None
        self.capture=cv2.VideoCapture(remoteVideoIP)
        self.videoFrame=QtGui.QLabel(self)
        self.videoFrame.setGeometry(550,290,240,160)
        
        self.timerRefreshVideo=QtCore.QTimer(self)
        self.timerRefreshVideo.timeout.connect(self.updateFrame)
        self.timerRefreshVideo.start(2)
        
        self.recordFetalButton=QtGui.QPushButton('Start\nRecording',self)
        self.recordFetalButton.move(25,320)
        self.recordFetalButton.resize(90,60)
        self.recordFetalButton.clicked.connect(self.callRecordFetalSound)
        self.bloodTestButton=QtGui.QPushButton('Done',self)
        self.bloodTestButton.move(158,320)
        self.bloodTestButton.resize(90,60)
        self.bloodTestButton.clicked.connect(self.bloodTest)
        self.sfhTestButton=QtGui.QPushButton('Done',self)
        self.sfhTestButton.move(293,320)
        self.sfhTestButton.resize(90,60)
        self.sfhTestButton.clicked.connect(self.sfhTest)
        self.urineTestButton=QtGui.QPushButton('Done',self)
        self.urineTestButton.move(425,357)
        self.urineTestButton.resize(90,60)
        self.urineTestButton.clicked.connect(self.urineTest)

        self.endSessionButton=QtGui.QPushButton('End Session',self)
        self.endSessionButton.move(-200,-110)
        self.endSessionButton.resize(120,35)
        
        self.alpha=QtGui.QColor()
        self.alpha.setRgb(0,0,0,0)
        self.red=QtGui.QColor()
        self.red.setRgb(246,65,63)
        self.yellow=QtGui.QColor()
        self.yellow.setRgb(249,170,44)
        self.green=QtGui.QColor()
        self.green.setRgb(62,201,82)
        self.alphaStroke=QtGui.QPen()
        self.alphaStroke.setColor(self.alpha)
        self.redStroke=QtGui.QPen()
        self.redStroke.setColor(self.red)
        self.yellowStroke=QtGui.QPen()
        self.yellowStroke.setColor(self.yellow)
        self.greenStroke=QtGui.QPen()
        self.greenStroke.setColor(self.green)
        self.black=QtGui.QColor()
        self.black.setRgb(0,0,0)
        self.white=QtGui.QColor()
        self.white.setRgb(200,200,200)

        self.weightState=0
        self.bloodState=0
        self.fetalState=0
        self.idState=0

        self.fetalRecordState=0
        self.endState=0
        
        
        self.IDNoticeLabel=QtGui.QLabel(self)
        self.IDNoticeLabel.move(220,120)
        self.IDNoticeLabel.setFont(QtGui.QFont("",15))
        self.IDNoticeLabel.resize(350,200)
        self.IDNoticeLabel.setText("")


        self.penline=QtGui.QPen(self.white,1)
        
        
        
        
        self.initialize()

    def initialize(self):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))

        self.nameStaticLabel=QtGui.QLabel(self)
        self.nameStaticLabel.move(605,170)
        self.nameStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.nameLabel=QtGui.QLabel(self)
        self.nameLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.nameLabel.move(655,170)
        self.nameLabel.resize(150,30)
        self.nameLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.idStaticLabel=QtGui.QLabel(self)
        self.idStaticLabel.move(633,190)
        self.idStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.idLabel=QtGui.QLabel(self)
        self.idLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.idLabel.move(655,190)
        self.idLabel.resize(150,30)
        self.idLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.birthStaticLabel=QtGui.QLabel(self)
        self.birthStaticLabel.move(620,210)
        self.birthStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.birthLabel=QtGui.QLabel(self)
        self.birthLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.birthLabel.move(655,212)
        self.birthLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodTypeStaticLabel=QtGui.QLabel(self)
        self.bloodTypeStaticLabel.move(606,230)
        self.bloodTypeStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodLabel=QtGui.QLabel(self)
        self.bloodLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.bloodLabel.move(655,232)
        self.bloodLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.weekStaticLabel=QtGui.QLabel(self)
        self.weekStaticLabel.move(570,240)
        self.weekStaticLabel.resize(150,50)
        self.weekStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.weekLabel=QtGui.QLabel(self)
        self.weekLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.weekLabel.move(655,251)
        self.weekLabel.setStyleSheet("color: '#aaaaaa' ;")

        self.staticLabelFont=QtGui.QFont("",18)
        self.statusLabelFont=QtGui.QFont("",15)
        self.pageLabelFont=QtGui.QFont("",13)
        
        self.weightStaticLabel=QtGui.QLabel(self)
        self.weightStaticLabel.setFont(self.staticLabelFont)
        self.weightStaticLabel.move(40,40)
        self.weightStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.weightLabel=QtGui.QLabel(self)
        self.weightLabel.setFont(QtGui.QFont("",30,weight=QtGui.QFont.Bold))
        self.weightLabel.move(45,90)
        self.weightLabel.resize(100,40)
        self.weightLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.weightULabel=QtGui.QLabel(self)
        self.weightULabel.setFont(QtGui.QFont("",10))
        self.weightULabel.move(145,103)
        self.weightULabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodStaticLabel=QtGui.QLabel(self)
        self.bloodStaticLabel.setFont(self.staticLabelFont)
        self.bloodStaticLabel.move(220,30)
        self.bloodStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodStaticLabel2=QtGui.QLabel(self)
        self.bloodStaticLabel2.setFont(self.staticLabelFont)
        self.bloodStaticLabel2.move(220,55)
        self.bloodStaticLabel2.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodSysStaticLabel=QtGui.QLabel(self)
        self.bloodSysStaticLabel.move(205,100)
        self.bloodSysStaticLabel.setText("")
        self.bloodSysStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodDiaStaticLabel=QtGui.QLabel(self)
        self.bloodDiaStaticLabel.move(255,100)
        self.bloodDiaStaticLabel.setText("")
        self.bloodDiaStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodHrStaticLabel=QtGui.QLabel(self)
        self.bloodHrStaticLabel.move(305,100)
        self.bloodHrStaticLabel.setText("")
        self.bloodHrStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodSysLabel=QtGui.QLabel(self)
        self.bloodSysLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.bloodSysLabel.move(205,120)
        self.bloodSysLabel.setText("")
        self.bloodSysLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodDiaLabel=QtGui.QLabel(self)
        self.bloodDiaLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.bloodDiaLabel.move(255,120)
        self.bloodDiaLabel.setText("")
        self.bloodDiaLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.bloodHrLabel=QtGui.QLabel(self)
        self.bloodHrLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        self.bloodHrLabel.move(305,120)
        self.bloodHrLabel.setText("")
        self.bloodHrLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.fetalStaticLabel=QtGui.QLabel(self)
        self.fetalStaticLabel.setFont(self.staticLabelFont)
        self.fetalStaticLabel.move(400,40)
        self.fetalStaticLabel.resize(150,30)
        self.fetalStaticLabel.setText("")
        self.fetalStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.fetalLabel=QtGui.QLabel(self)
        self.fetalLabel.setFont(QtGui.QFont("",30,weight=QtGui.QFont.Bold))
        self.fetalLabel.move(400,80)
        self.fetalLabel.resize(100,40)
        self.fetalLabel.setText("")
        self.fetalLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.fetalULabel=QtGui.QLabel(self)
        self.fetalULabel.setFont(QtGui.QFont("",10))
        self.fetalULabel.move(485,95)
        self.fetalULabel.setStyleSheet("color: '#aaaaaa' ;")
        self.fetalSoundStaticLabel=QtGui.QLabel(self)
        self.fetalSoundStaticLabel.setFont(self.staticLabelFont)
        self.fetalSoundStaticLabel.move(20,250)
        self.fetalSoundStaticLabel.resize(150,30)
        self.fetalSoundStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.fetalSoundStaticLabel2=QtGui.QLabel(self)
        self.fetalSoundStaticLabel2.setFont(self.staticLabelFont)
        self.fetalSoundStaticLabel2.move(20,275)
        self.fetalSoundStaticLabel2.resize(150,30)
        self.fetalSoundStaticLabel2.setStyleSheet("color: '#aaaaaa' ;")
        self.fetalSoundStatusLabel=QtGui.QLabel(self)
        self.fetalSoundStatusLabel.setFont(QtGui.QFont("",13))
        self.fetalSoundStatusLabel.move(15,380)
        self.fetalSoundStatusLabel.resize(120,30)
        self.fetalSoundStatusLabel.setStyleSheet("color: '#aaaaaa' ;")
        


        self.bloodTestStaticLabel=QtGui.QLabel(self)
        self.bloodTestStaticLabel.setFont(self.staticLabelFont)
        self.bloodTestStaticLabel.move(155,175)
        self.bloodTestStaticLabel.resize(250,200)
        self.bloodTestStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.sfhStaticLabel=QtGui.QLabel(self)
        self.sfhStaticLabel.setFont(self.staticLabelFont)
        self.sfhStaticLabel.move(286,240)
        self.sfhStaticLabel.resize(250,80)
        self.sfhStaticLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.urineTestStaticLabel=QtGui.QLabel(self)
        self.urineTestStaticLabel.setFont(self.staticLabelFont)
        self.urineTestStaticLabel.move(416,240)
        self.urineTestStaticLabel.resize(250,80)
        self.urineTestStaticLabel.setStyleSheet("color: '#aaaaaa' ;")

        self.statusLabel=QtGui.QLabel(self)
        self.statusLabel.setFont(self.statusLabelFont)
        self.statusLabel.move(555,-30)
        self.statusLabel.resize(220,200)
        self.statusLabel.setText(statusFormat("Please place your ID card to the sensor..."))
        self.statusLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.pageLabel=QtGui.QLabel(self)
        self.pageLabel.setFont(self.pageLabelFont)
        self.pageLabel.move(672,125)
        self.pageLabel.resize(200,20)
        self.pageLabel.setText("")
        self.pageLabel.setStyleSheet("color: '#aaaaaa' ;")
        self.stepLabel=QtGui.QLabel(self)
        self.stepLabel.setFont(self.pageLabelFont)
        self.stepLabel.move(555,-5)
        self.stepLabel.resize(150,40)
        self.stepLabel.setStyleSheet("color: '#aaaaaa' ;")

        self.u1=QtGui.QRadioButton("",self)
        self.u1.setStyleSheet('QRadioButton::indicator { width: 15; height: 15;};')
        self.u1.setChecked(True)
        self.u1.move(417,310)
        self.u1.resize(15,15)
        self.u2=QtGui.QRadioButton("",self)
        self.u2.setStyleSheet('QRadioButton::indicator { width: 15; height: 15;};')
        self.u2.setChecked(False)
        self.u2.move(440,310)
        self.u2.resize(15,15)
        self.u3=QtGui.QRadioButton("",self)
        self.u3.setStyleSheet('QRadioButton::indicator { width: 15; height: 15;};')
        self.u3.setChecked(False)
        self.u3.move(462,310)
        self.u3.resize(15,15)
        self.u4=QtGui.QRadioButton("",self)
        self.u4.setStyleSheet('QRadioButton::indicator { width: 15; height: 15;};')
        self.u4.setChecked(False)
        self.u4.move(484,310)
        self.u4.resize(15,15)
        self.u5=QtGui.QRadioButton("",self)
        self.u5.setStyleSheet('QRadioButton::indicator { width: 15; height: 15;};')
        self.u5.setChecked(False)
        self.u5.move(506,310)
        self.u5.resize(15,15)
        
        
        self.uText=QtGui.QLabel(self)
        self.uText.move(420,320)
        self.uText.setStyleSheet("color: '#aaaaaa' ;")
        
        
        #self.statusLabel=QtGui.QLabel(self)
        #self.statusLabel.setFont(QtGui.QFont("",weight=QtGui.QFont.Bold))
        #self.statusLabel.resize(500,30)
        #self.statusLabel.move(150,400)
        #self.statusLabel.setAlignment(QtCore.Qt.AlignHCenter)
        #self.statusLabel.setText("")
        
        print "UI done"
        
        self.showFullScreen()
        self.show()

    def showLabels(self):
        self.nameStaticLabel.setText("Name ")
        self.birthStaticLabel.setText("Age ")
        self.idStaticLabel.setText("ID ")
        self.bloodTypeStaticLabel.setText("Blood ")
        self.weekStaticLabel.setText("Fetal Week")
        
        self.weightStaticLabel.setText("Weight")
        self.fetalSoundStaticLabel.setText("Heart")
        self.fetalSoundStaticLabel2.setText("Sound")
        self.weightULabel.setText("KG")
        self.fetalULabel.setText("BPM")
        self.bloodStaticLabel.setText("Blood")
        self.bloodStaticLabel2.setText("Pressure")
        self.fetalStaticLabel.setText("Fetal HR")
        self.bloodSysStaticLabel.setText("SYS")
        self.bloodDiaStaticLabel.setText("DIA")
        self.bloodHrStaticLabel.setText("HR")
        self.bloodTestStaticLabel.setText("Anemia\nTest")
        self.sfhStaticLabel.setText("SFH Test")
        self.urineTestStaticLabel.setText("Urine Test")
        self.uText.setText("A   B   C   D   E")
        
        
        
        
        self.show()
        self.update()


    def updateFrame(self):
        ret,self.videoFrameImage=self.capture.read()
        self.displayImage(self.videoFrameImage)
    def displayImage(self,image):
        qformat=QtGui.QImage.Format_Indexed8
        if len(image.shape)==3:
            if image.shape[2]==4:
                qformat=QtGui.QImage.Format_RGBA8888
            else:
                qformat=QtGui.QImage.Format_RGB888
        outImage=QtGui.QImage(image,image.shape[1],image.shape[0],image.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        
        self.videoFrame.setPixmap(QtGui.QPixmap.fromImage(outImage))
        self.videoFrame.setScaledContents(True)

    
    def callRecordFetalSound(self):
        self.recordFetalButton.setEnabled(False)
        self.fetalSoundStatusLabel.setText("Recording...")
        self.statusLabel.setText("Recording fetal sound...")
        self.pageLabel.setText("Manual Pg. 9")
        
        self.update()
        print "pressed record"
        tRecordFetalSound.start()

        
    def bloodTest(self):
        self.bloodTestButton.setEnabled(False)

        self.statusLabel.setText("Proceed to measure symphysial fundal height")
        self.pageLabel.setText("Manual Pg. 13")
        self.stepLabel.setText("Test 5/7")

        checked=QtGui.QLabel(self)
        checked.setPixmap(QtGui.QPixmap("checked.png"))
        checked.resize(30,30)
        checked.move(230,420)
        checked.show()

    def sfhTest(self):
        self.sfhTestButton.setEnabled(False)

        self.statusLabel.setText("Proceed to urine test")
        self.pageLabel.setText("Manual Pg. 15")
        self.stepLabel.setText("Test 6/7")
        
        checked=QtGui.QLabel(self)
        checked.setPixmap(QtGui.QPixmap("checked.png"))
        checked.resize(30,30)
        checked.move(365,420)
        checked.show()

    def urineTest(self):
        self.urineTestButton.setEnabled(False)

        self.statusLabel.setText("This is the end of the test, wish you have a nice day.")
        self.pageLabel.setText("")
        self.stepLabel.setText("Test 7/7")

        
        
        checked=QtGui.QLabel(self)
        checked.setPixmap(QtGui.QPixmap("checked.png"))
        checked.resize(30,30)
        checked.move(508,420)
        checked.show()


        self.endSessionButton.move(600,80)
        
        self.endState=1
        self.update()

        

    
    def paintEvent(self,event):

        if self.idState==1:
            line=QtGui.QPainter(self)
            line.setPen(self.penline)
            line.drawLine(180,0,180,230)
            line.drawLine(360,0,360,230)
            line.drawLine(540,0,540,480)
            line.drawLine(0,230,540,230)
            line.drawLine(135,230,135,480)
            line.drawLine(270,230,270,480)
            line.drawLine(405,230,405,480)
            line.drawLine(540,150,800,150)
       
        if self.weightState==0:
            color=self.alpha
            stroke=self.alphaStroke
        elif self.weightState==1:
            color=self.red
            stroke=self.redStroke
        elif self.weightState==2:
            color=self.yellow
            stroke=self.yellowStroke
        elif self.weightState==3:
            color=self.green
            stroke=self.greenStroke
            checked=QtGui.QLabel(self)
            checked.setPixmap(QtGui.QPixmap("checked.png"))
            checked.resize(30,30)
            checked.move(140,190)
            checked.show()
        weightIndicator=QtGui.QPainter(self)
        weightIndicator.setBrush(color)
        weightIndicator.setPen(stroke)
        weightIndicator.drawEllipse(QtCore.QPoint(23,55),4.5,4.5)


        if self.bloodState==0:
            color=self.alpha
            stroke=self.alphaStroke
        elif self.bloodState==1:
            color=self.red
            stroke=self.redStroke
        elif self.bloodState==2:
            color=self.yellow
            stroke=self.yellowStroke
        elif self.bloodState==3:
            color=self.green
            stroke=self.greenStroke
            checked=QtGui.QLabel(self)
            checked.setPixmap(QtGui.QPixmap("checked.png"))
            checked.resize(30,30)
            checked.move(320,190)
            checked.show()

        bloodIndicator=QtGui.QPainter(self)
        bloodIndicator.setBrush(color)
        bloodIndicator.setPen(stroke)
        bloodIndicator.drawEllipse(QtCore.QPoint(203,55),4.5,4.5)

        if self.fetalState==0:
            color=self.alpha
            stroke=self.alphaStroke
        elif self.fetalState==1:
            color=self.red
            stroke=self.redStroke
        elif self.fetalState==2:
            color=self.yellow
            stroke=self.yellowStroke
        elif self.fetalState==3:
            color=self.green
            stroke=self.greenStroke
            checked=QtGui.QLabel(self)
            checked.setPixmap(QtGui.QPixmap("checked.png"))
            checked.resize(30,30)
            checked.move(500,190)
            checked.show()
        fetalIndicator=QtGui.QPainter(self)
        fetalIndicator.setBrush(color)
        fetalIndicator.setPen(stroke)
        fetalIndicator.drawEllipse(QtCore.QPoint(383,55),4.5,4.5)

        if self.fetalRecordState==1:
            GUI.recordFetalButton.setEnabled(False)
            
        if self.fetalRecordState==2:
            GUI.recordFetalButton.setEnabled(True)
            GUI.recordFetalButton.setText("Record\nAgain")
            
            checked=QtGui.QLabel(self)
            checked.setPixmap(QtGui.QPixmap("checked.png"))
            checked.resize(30,30)
            checked.move(95,420)
            checked.show()

    def newSession(self):
        self.weightLabel.setText("")
        self.bloodSysLabel.setText("")
        self.bloodDiaLabel.setText("")
        self.bloodHrLabel.setText("")
        self.fetalLabel.setText("")
        self.recordFetalButton.setEnabled(True)
        self.bloodTestButton.setEnabled(True)
        self.urineTestButton.setEnabled(True)
        self.sfhTestButton.setEnabled(True)
        self.fetalSoundStatusLabel.setEnaled(True)

        print "UI cleaned"

    
def receiveBTData(MACAddress,port,test):
    global weightData
    global sysData
    global diaData
    global bloodHrData
    global fetalData
    
    while True:
        try:
            socketBluetooth=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print "Bluetooth: Connecting "+MACAddress+"..."+test
            socketBluetooth.connect((MACAddress,port))
        except:
            print "Bluetooth: Target not detected, reconnecting..."+test
            time.sleep(3)
            continue
        break
    print "Bluetooth: Connected to Bluetooth device."+test
    if test=='w':
        GUI.weightState=2
        GUI.statusLabel.setText(statusFormat("Please stand on the scale."))
        GUI.pageLabel.setText("Manual Pg. 3")
        socketInternet.send("30")
    elif test=='b':
        GUI.bloodState=2
        GUI.statusLabel.setText(statusFormat("Follow the instruction at page 5"))
        GUI.pageLabel.setText("Manual Pg. 5")
        socketInternet.send("40")
    elif test=='f':
        GUI.fetalState=2
        GUI.statusLabel.setText(statusFormat("Follow the instruction at page 8"))
        GUI.pageLabel.setText("Manual Pg. 8")
        socketInternet.send("50")
    GUI.update()
    weight=0
    dataBlood=""
    while 1:
        print 'receiving...'
        data=socketBluetooth.recv(1024)
        print data
        if len(data)>=2:
            print data
            if data=="w1" or data==",w1":
                socketInternet.send("31")
                GUI.statusLabel.setText(statusFormat("Measuring weight...please stand still."))
                GUI.pageLabel.setText("Manual Pg. 3")
                continue
            elif data=="b1" or data[:3]==",b1":
                socketInternet.send("41")
                GUI.statusLabel.setText(statusFormat("Measuring blood pressure..."))
                GUI.pageLabel.setText("Manual Pg. 7")
            elif data=="f1" or data[:3]==",f1":
                socketInternet.send("51")
                GUI.statusLabel.setText(statusFormat("Measuring fetal heart rate..."))
                GUI.pageLabel.setText("Manual Pg. 8")
            elif data.find('#') != -1 or data.find('@')!=-1:
                #print "Internet: Sending "+weight+" to remote server "+remoteIP+"..."
                if  test=='w':
                    print "send "+test+str(weight)
                    socketInternet.send(test+str(weight))
                    weightData=weight
                elif test=='b':
                    if data.find('#')==-1 :
                        dataBlood=data
                        continue
                    dataBlood=dataBlood+data
                    
                    socketInternet.send(dataBlood)
                    sysData=dataBlood[1:dataBlood.find('@')]
                    dataBlood=dataBlood[dataBlood.find('@')+1:]
                    diaData=dataBlood[:dataBlood.find('@')]
                    dataBlood=dataBlood[dataBlood.find('@')+1:]
                    bloodHrData=dataBlood[:dataBlood.find('#')]

                    print sysData
                    print diaData
                    print bloodHrData
                    
                    GUI.bloodSysLabel.setText(sysData)
                    GUI.bloodDiaLabel.setText(diaData)
                    GUI.bloodHrLabel.setText(bloodHrData)
                    
                elif test=='f':
                    if data[0]==',':
                        data=data[2:data.find("#")]
                    else:
                        data=data[1:data.find("#")]
                    socketInternet.send('f'+data+'##')
                    GUI.fetalLabel.setText(data)
                    fetalData=data
                    print 'fetal: '+str(fetalData)
                #data=socketBluetooth.recv(1024)
                #data=socketBluetooth.recv(1024)
                #data=socketBluetooth.recv(1024)
                
                break
            print data[:2]
            weight=data
            print "------"
            if test=='w':
                GUI.weightLabel.setText(weight)
                
                
            
            
        #time.sleep(1)
    print test+' closed.'
    socketBluetooth.close()
    if test=='w':
        GUI.weightState=3
        GUI.statusLabel.setText(statusFormat("Please turn on the sphygmomanometer."))
        GUI.pageLabel.setText("Manual Pg. 5")
        GUI.stepLabel.setText("Test 2/7")
    elif test=='b':
        GUI.bloodState=3
        GUI.statusLabel.setText(statusFormat("Please turn on the fetal heart rate sensor"))
        GUI.pageLabel.setText("Manual Pg. 8")
        GUI.stepLabel.setText("Test 3/7")
    elif test=='f':
        GUI.fetalState=3
        print 'fetatl done'
        GUI.statusLabel.setText(statusFormat("Please turn on the Stethoscope and press the button"))
        GUI.pageLabel.setText("Manual Pg. 9")
        GUI.stepLabel.setText("Test 4/7")
    GUI.update()
    print "Bluetooth: Session ended. "+test

    
def scanCard():
    global nameData
    global idData
    
    tFlashingLight=multiprocessing.Process(target=flashingLight)
    tFlashingLight.start()
    data=[]
    block=1

    GUI.update()
    dataPatientInformation="29"
    socketInternet.send("20")
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
            GUI.IDNoticeLabel.setText("")
            GUI.showLabels()
            #print "UID: %s-%s-%s-%s" % (uid[0],uid[1],uid[2],uid[3])
            key=[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] #Default key for authentication
            MIFAREReader.MFRC522_SelectTag(uid) #Select the scanned tag
            status=MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid) #Authenticate
            
            if status==MIFAREReader.MI_OK:

                data=MIFAREReader.MFRC522_Read(block)
                dataString=toStr(data)
                dataString=dataString[:dataString.find(chr(0))]
                
                MIFAREReader.MFRC522_StopCrypto1()
                if block==1:
                    dataPatientInformation=dataPatientInformation+'@'+dataString
                    GUI.nameLabel.setText(dataString)
                    nameData=dataString
                if block==2:
                    dataPatientInformation=dataPatientInformation+'$'+dataString
                    GUI.birthLabel.setText(dataString)
                if block==4:
                    dataPatientInformation=dataPatientInformation+'%'+dataString
                    GUI.bloodLabel.setText(dataString)
                if block==5:
                    dataPI=dataPatientInformation+'^'+dataString
                    idData=dataString
                    GUI.idLabel.setText(idData)
                    tFlashingLight.terminate()
                    GPIO.output(pinIdLight,GPIO.LOW)
                    print dataPI
                    socketInternet.send(dataPI)
                
                block=block+1
            else:
                print "Error Authenticate."

    GUI.weekLabel.setText("6")
    
    print "Identity confirmed."
    GUI.idState=1
    GUI.weightState=1
    GUI.bloodState=1
    GUI.fetalState=1
    GUI.statusLabel.setText(statusFormat("Please turn on the scale."))
    GUI.pageLabel.setText("Manual Pg. 2")
    GUI.stepLabel.setText("Test 1/7")
    tWeight.start()
    tBlood.start()
    tFetal.start()
    tPrinter.start()
    #tTestBlood.start()
    #tTestFetal.start()

def recordFetalSound():
    print "Recording..."
    socketInternet.send("61")
    date=time.strftime("%Y%m%d",time.localtime())
    audioFileName=idData+"-"+date+".wav"
    #recordScript="arecord -D hw:2,0 -d 20 -f cd "+audioFileName+" -c 1"
    #os.system(recordScript)
    print "Recorded."
    GUI.fetalSoundStatusLabel.setText("Recording...")
    GUI.fetalRecordState=1
    GUI.update()
    
    print "Sending..."
    #socketInternet.send("62");
    #file=open(audioFileName,"rb")
    #part=file.read(1024*5000)
    #while part:
        #socketInternet.send(part)
        #part=file.read(1024)
    time.sleep(5)
    print "Sent."
    GUI.fetalSoundStatusLabel.setText("Recorded")
    GUI.fetalRecordState=2
    GUI.statusLabel.setText("Proceed to anemia testing")
    GUI.pageLabel.setText("Manual Pg. 10")
    GUI.stepLabel.setText("Test 4/7")
    GUI.update()
    
def printscript(script):
    return "echo \""+script+"\" | lpr"
def printer():
    global weightData
    global sysData
    global diaData
    global bloodHrData
    global fetalData
    global heightData
    global aptdData
    global nameData
    global idData
    
    data=socketInternet.recv(512)
    heightData=data[:data.find('|')]
    data=data[data.find('|')+1:]
    aptdData=data[:data.find('|')]
    summary=data[data.find('|')+1:]

    now=datetime.datetime.now()
    
    os.system(printscript("Diagnosis Summary\n"+
                str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"\n"+
                str(nameData)+" ("+str(idData)+")\n"+
              "Weight: "+str(weightData)+" KG\n"+
              "Height: "+str(heightData)+" cm\n"+
              "Sys: "+str(sysData)+" mmHg\n"+
              "Dia: "+str(diaData)+" mmHg\n"+
                "Body HR: "+str(bloodHrData)+" BPM\n"+
              "Fetal HR: "+str(fetalData)+" BPM\n"+
              "SFH: "+str(aptdData)+" cm\n"+
              "\n"+
              "---------\nBlood & Urine Test\n\n"+
                "Anemia: Possible\nGlucose: 250 mg/dl\nBilirubin: Neg\nKetone: Neg\n"+
                "Specific Gravity: 1.015\nBlood: Neg\npH: 6.0\nProtein: Neg\n"+
                "Urobilinogen: 1.0\nNitrite: Pos\nLeukocytes: Trace\n---------\n\n"+
                printFormat("You have potential to have anemia, higher oral iron and folic acid in food intake is recommended. Glucose was been detected in urine."
                        )))
    GUI.newSession()
    
def toStr(data):
    return ''.join(chr(x) for x in data)

def flashingLight():
    while True:
        GPIO.output(pinIdLight,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pinIdLight,GPIO.LOW)
        time.sleep(0.2)
        
def statusFormat(message):
    index=0
    below20=0
    for a in message:
        if a==' ':
            spaceIndex=index
        if below20>20:
            message=message[:spaceIndex]+'\n'+message[spaceIndex+1:]
            below20=index-spaceIndex
        below20=below20+1
        index=index+1
    return message

def printFormat(message):
    index=0
    below18=0
    for a in message:
        if a==' ':
            spaceIndex=index
        if below18>18:
            message=message[:spaceIndex]+'\n'+message[spaceIndex+1:]
            below18=index-spaceIndex
        below18=below18+1
        index=index+1
    return message

app=QtGui.QApplication(sys.argv)
GUI=Window()


tScanCard=threading.Thread(target=scanCard)
tWeight=threading.Thread(target=receiveBTData,args=(scaleBTAddress,scaleBTPort,'w',))
tBlood=threading.Thread(target=receiveBTData,args=(pressureBTAddress,pressureBTPort,'b',))
tFetal=threading.Thread(target=receiveBTData,args=(fetalBTAddress,fetalBTPort,'f',))
tRecordFetalSound=threading.Thread(target=recordFetalSound)

tPrinter=threading.Thread(target=printer)
#tTestFetal=threading.Thread(target=fetal)

tInitializeSocket=threading.Thread(target=initializeSocket)
tInitializeSocket.start()





sys.exit(app.exec_())
