import sys, os
from PyQt4 import QtCore, QtGui


import Help
FOLDER_ICONS = os.path.dirname(__file__).replace(os.sep, "/") + "/graphics/icons"


def iconFromFile(filePath, size, color):
	tex = QtGui.QPixmap(filePath)
	tex.fill(color)
	tex.setAlphaChannel(QtGui.QPixmap(filePath))
	tex = tex.scaled(size, size, 0, 1)
	return tex


class MenuBar(QtGui.QWidget):
	"""docstring for MenueBar"""
	def __init__(self, parent=None):
		super(MenuBar, self).__init__()
		self.parent = parent


		#settingsButton = QtGui.QLabel("O")


		helpButton = QtGui.QLabel("?")
		helpButton.mousePressEvent = self.mouseClicked_helpButton

		path = FOLDER_ICONS + "/icon_Help.png"
		tex = iconFromFile(path, 14, QtGui.QColor(204, 204, 204))
		helpButton.setPixmap(tex)


		# Layout
		self.layout = QtGui.QHBoxLayout()
		self.layout.setMargin(0)

		self.layout.addStretch()
		#self.layout.addWidget(settingsButton)
		self.layout.addWidget(helpButton)

		self.setLayout(self.layout)


	def mouseClicked_helpButton(self, event):
		reload(Help)
		Help.openMenu(event)





if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	window = MenuBar()
	window.show()
	app.exec_()