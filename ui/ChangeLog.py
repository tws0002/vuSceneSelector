from PyQt4 import QtGui, QtCore
import time
import sys, os


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_PATH = os.path.dirname(WORKING_DIR) + "/ui/data/changeLog.html"


class ChangeLog(QtGui.QDialog):
	def __init__(self):
		super(ChangeLog, self).__init__()

		# Read Data
		with open(FILE_PATH, "r") as f:
			data = f.read()
		data = data.decode('string-escape').decode("utf-8")


		self.label = QtGui.QLabel()
		self.label.setText(data)
		self.label.setTextFormat(QtCore.Qt.RichText)

		scrollArea = QtGui.QScrollArea(self)
		scrollArea.setWidgetResizable(True)
		scrollArea.setWidget(self.label)

		# Layout
		layout = QtGui.QGridLayout()
		layout.addWidget(scrollArea, 0, 0)
		self.setLayout(layout)

		self.setWindowTitle("ChangeLog:")



if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	cl = ChangeLog()
	cl.show()
	app.exec_()
	"""

	with open(FILE_PATH, "r") as f:
		data = f.read().decode('string-escape').decode("utf-8")
	print type(data)
	"""



