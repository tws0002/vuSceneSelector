from PyQt4 import QtGui, QtCore
import sys, os


WORKING_DIR = os.path.dirname(__file__)
FILENAME = WORKING_DIR + "/graphics/SplashScreen.png"


class SplashScreen(QtGui.QLabel):
	def __init__(self):
		#super(SplashScreen, self).__init__(None)
		super(SplashScreen, self).__init__(None, QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		#self.app = app
		#self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		pixmap = QtGui.QPixmap(FILENAME)
		self.setPixmap(pixmap)


		self.show()

		# Center
		frameGm = self.frameGeometry()
		screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
		centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())




	def close(self):
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)


	ss = SplashScreen()
	ss.show()

	app.exec_()
