from PyQt4 import QtGui, QtCore
import time
import sys, os


#WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
#rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-2])
FILE_PATH = "D:/Vincent/Dropbox/btSyncFolders/Dev/017_KroetenliedPipeline/vuSceneSelector/v0.4.3_DEV/vuSceneSelector/_ProjectSettings/changeLog.py"



class ChangeLog(QtGui.QDialog):
	def __init__(self):
		super(ChangeLog, self).__init__()

		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

		# Read Data
		with open(FILE_PATH, "r") as f:
			data = f.read()
		#data = data.replace("\n", "</br>")
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



