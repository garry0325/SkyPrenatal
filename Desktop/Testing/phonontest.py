import sys
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon

app=QtGui.QApplication(sys.argv)
vp=Phonon.VideoPlayer()
vp.show()
media=Phonon.MediaSource('video.mp4')
vp.load(media)
vp.play()
sys.exit(app.exec_())
