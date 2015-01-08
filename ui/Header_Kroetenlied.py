from PyQt4 import QtCore, QtGui
import math
import os, sys



WORKING_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
	path = os.sep.join(WORKING_DIR.split(os.sep)[:-1])
	sys.path.append(path)


# Import Modules
from core import Settings
SETTINGS = Settings.SETTINGS
from ui import style


FOLDER_GRAPHICS = os.sep.join(WORKING_DIR.split(os.sep)[:-1]) + "_Settings"







class Header(QtGui.QWidget):
	def __init__(self, parent=None):
		super(Header, self).__init__()
		#self.window = window

		# Header Image
		self.image = QtGui.QLabel("Test")
		self.image.setStyleSheet("border: 1px solid " + style.COLOR_BORDER)
		self.image.setPixmap(QtGui.QPixmap(FOLDER_GRAPHICS + "/Header_Kroetenlied.png"))


		#########################
		#						#
		#         Eyes          #
		#						#
		#########################
		view = QtGui.QGraphicsView()
		view.setStyleSheet("background: transparent");
		view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		scene = QtGui.QGraphicsScene(0, 0, 413, 143)
		view.setScene(scene)

		# Eyes
		brush = QtGui.QBrush(QtGui.QColor(31,30,12))
		pen = QtGui.QPen()
		pen.setStyle(QtCore.Qt.NoPen)
		r = 3
		self.eyeLeft = scene.addEllipse(-r, -r, 2*r, 2*r ,pen, brush)
		self.eyeRight = scene.addEllipse(-r, -r, 2*r, 2*r ,pen, brush)
		headerMouseHandler = QtGui.QLabel()
		headerMouseHandler.setFixedSize(413,143)
		headerMouseHandler.setStyleSheet("background: transparent");


		# Main Grid
		main_grid = QtGui.QGridLayout()
		self.setLayout(main_grid)
		main_grid.setContentsMargins(0,0,0,0)

		main_grid.addWidget(self.image, 0, 0)
		main_grid.addWidget(view, 0, 0)
		main_grid.addWidget(headerMouseHandler, 0, 0)
		main_grid.setColumnStretch(1,1)




		self.setMouseTracking(True)
		headerMouseHandler.setMouseTracking(True)
		#self.window.setMouseTracking(True)




	def setImage(self, path):
		pass

	def setText(self, selType, selName):
		pass


	def mouseMoveEvent(self, event):
		if QtGui.qApp.mouseButtons() != QtCore.Qt.RightButton:
			# Cal Position
			x = event.x() - 345
			y = event.y() - 57
			l = math.sqrt(x*x + y*y)
			x = (x/l * 7) + 345
			y = (y/l * 5) + 57
			self.eyeLeft.setPos(x,y)

		if QtGui.qApp.mouseButtons() != QtCore.Qt.LeftButton:
			x = event.x() - 399
			y = event.y() - 54
			l = math.sqrt(x*x + y*y)
			x = (x/l * 7) + 399
			y = (y/l * 5) + 54
			self.eyeRight.setPos(x,y)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	header = Header()
	header.show()

	app.exec_()

