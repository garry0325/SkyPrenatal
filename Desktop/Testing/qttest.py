import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("window")
        self.home()


    def home(self):
        btn=QtGui.QPushButton("Quit",self)
        btn.clicked.connect(self.closeApplication)


        checkBox=QtGui.QCheckBox("Large Window",self)
        checkBox.stateChanged.connect(self.largeWindow)
        checkBox.move(150,200)
        

        self.progress=QtGui.QProgressBar(self)
        self.progress.setGeometry(200,80,250,20)


        dwn=QtGui.QPushButton("download",self)
        dwn.move(200,120)
        dwn.clicked.connect(self.download)

        self.styleChoice=QtGui.QLabel("motif ",self)
        comboBox=QtGui.QComboBox(self)
        comboBox.addItem("motif")
        comboBox.addItem("Windows")
        comboBox.addItem("cde")
        comboBox.addItem("Plastique")
        comboBox.addItem("Cleanlooks") 

        comboBox.move(50,250)
        self.styleChoice.move(50,150)
        comboBox.activated[str].connect(self.style_choice)

        
        
        self.show()


    def style_choice(self,text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))
        

    def download(self):
        self.completed=0

        while self.completed<100:
            self.completed+=0.01
            self.progress.setValue(self.completed)
            
            

    def closeApplication(self):
        choice=QtGui.QMessageBox.question(self, "Warning","Want to quit?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice==QtGui.QMessageBox.Yes:
            sys.exit()
        

    def largeWindow(self,state):
        if state==QtCore.Qt.Checked:
            self.setGeometry(50,50,1000,600)
        else:
            self.setGeometry(50,50,500,300)

app=QtGui.QApplication(sys.argv)
GUI=Window()
sys.exit(app.exec_())
