from PyQt4 import QtGui, QtCore
import time
import sys, os


WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-2])



class SplashScreen(QtGui.QWidget):
	def __init__(self, app):
		super(SplashScreen, self).__init__(None, QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.app = app
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		img = rootDir.replace(os.sep, "/") + "/vuPipelineOverview/vuSceneSelector/graphics/SplashScreen.png"
		self.pixMap = QtGui.QPixmap(img)


		self.msg = "Starting!"
		self.msgList = [self.msg]
		self.resize(self.pixMap.size())
		self.show()

		self.n = 0


	def paintEvent(self, e):
		p = QtGui.QPainter()
		p.begin(self)

		p.drawPixmap(self.pixMap.rect(), self.pixMap)


		pen = p.pen()
		pen.setColor(QtGui.QColor(QtCore.Qt.white))
		p.setPen(pen)

		p.drawText(QtCore.QRectF(28, 105, 565, 230), self.msg)
		p.end()


	def setMsg(self, msg):
		self.n += 1
		self.msgList.append(msg)


		self.msg = "\n".join(self.msgList[-10:])
		self.update()

	def close(self):
		self.hide()

splashScreen = None


def show(app):
	global splashScreen
	splashScreen = SplashScreen(app)


def hide():
	global splashThread
	splashScreen.close()


def update(msg):
	splashScreen.setMsg(msg)
	QtGui.QApplication.processEvents()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	show(app)
	#app.exec_()


	for i in range(100):
		time.sleep(0.05)
		update("Step: " + str(i) + " of 100 --------------------------------------")
	hide()
"""
"""