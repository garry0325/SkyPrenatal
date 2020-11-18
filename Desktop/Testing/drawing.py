import sys
from PyQt4 import QtGui,QtCore

#red 246,65,63
#ylw 249,170,44
#grn 62,201,82

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window,self).__init__()
        self.setWindowTitle("Health Inspection Assistent")
        self.setGeometry(50,50,500,300)

        self.red=QtGui.QColor()
        self.red.setRgb(246,65,63)
        self.yellow=QtGui.QColor()
        self.yellow.setRgb(249,170,44)
        self.green=QtGui.QColor()
        self.green.setRgb(62,201,82)

        self.redStroke=QtGui.QPen()
        self.redStroke.setColor(self.red)
        self.yellowStroke=QtGui.QPen()
        self.yellowStroke.setColor(self.yellow)
        self.greenStroke=QtGui.QPen()
        self.greenStroke.setColor(self.green)
        
        self.initialize()

    def initialize(self):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))

        self.nameStaticLabel=QtGui.QLabel(self)
        self.nameStaticLabel.move(300,10)

        
        #self.painter.drawRect(100,100,100,100)

        self.show()
        
    def paintEvent(self,event):
        
        
        
        weightIndicator=QtGui.QPainter(self)
        weightIndicator.setBrush(self.red)
        weightIndicator.setPen(self.redStroke)
        weightIndicator.drawEllipse(QtCore.QPoint(10,20),3.5,3.5)

        bloodIndicator=QtGui.QPainter(self)
        bloodIndicator.setBrush(self.green)
        bloodIndicator.setPen(self.greenStroke)
        bloodIndicator.drawEllipse(QtCore.QPoint(10,45),3.5,3.5)
        
        










    
app=QtGui.QApplication(sys.argv)
GUI=Window()


sys.exit(app.exec_())
