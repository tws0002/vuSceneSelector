from PyQt4 import QtCore, QtGui
import sys
import math #for sqrt

HEADER_IMG = "I:/Vincent/Svobo_Eyes/Header_SceneSelector_v006_vu.png"


##############################################################################################
#
#
#		PyQt-Stuff
#
class testWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		self.window = QtGui.QMainWindow.__init__(self, parent)

		header = QtGui.QLabel()
		header.setPixmap(QtGui.QPixmap(HEADER_IMG))


		self.label = QtGui.QLabel("Test")


		# Graph and Scene
		scene = QtGui.QGraphicsScene(0, 0, 413, 143)
		view = QtGui.QGraphicsView()
		view.setStyleSheet("background: transparent");
		#view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
		view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		view.setScene(scene)

		# Eye
		brush = QtGui.QBrush(QtGui.QColor(200,200,200))
		pen = QtGui.QPen(QtCore.Qt.black, 1)
		r = 10
		#eye = scene.addEllipse(-r, -r, 2*r, 2*r ,pen, brush)
		#eye.setPos(344, 57)


		# Dot
		brush = QtGui.QBrush(QtGui.QColor(31,30,12))
		pen = QtGui.QPen()
		pen.setStyle(QtCore.Qt.NoPen)
		r = 3
		self.eyeLeft = scene.addEllipse(-r, -r, 2*r, 2*r ,pen, brush)
		self.eyeRight = scene.addEllipse(-r, -r, 2*r, 2*r ,pen, brush)



		# Main Layout
		main_grid = QtGui.QGridLayout()
		main_grid.setSpacing(300)
		main_grid.addWidget(self.label, 2, 1)
		main_grid.addWidget(header, 0, 1)
		main_grid.addWidget(view, 0, 1)


		mainWidget = QtGui.QWidget()
		mainWidget.setLayout(main_grid)
		self.setCentralWidget(mainWidget)



		# Set MouseTracking for EVERY Object ?!?
		self.setMouseTracking(True)
		view.setMouseTracking(True)
		self.label.setMouseTracking(True)
		header.setMouseTracking(True)
		mainWidget.setMouseTracking(True)


	def mouseMoveEvent(self, event):

		# Cal Position
		x = event.x() - 344
		y = event.y() - 57
		l = math.sqrt(x*x + y*y)
		x = (x/l * 5) + 344
		y = (y/l * 5) + 57
		self.eyeLeft.setPos(x,y)

		x = event.x() - 398
		y = event.y() - 54
		l = math.sqrt(x*x + y*y)
		x = (x/l * 6) + 398
		y = (y/l * 5) + 54
		self.eyeRight.setPos(x,y)




##############################################################################################
#
#
#		Main
#
#
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	form = testWindow()
	form.show()
	app.exec_()