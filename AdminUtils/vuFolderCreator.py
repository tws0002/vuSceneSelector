from PyQt4 import QtCore, QtGui
import os
import sys

try:
	sys.path.append("V:/090_Software/Intern")
	from JagonIndex import Shots, Assets, Tasks
except Exception, e:
	print e


try:
	sys.path.append("N:/060_Software/Kroetenlied_Pipeline")
	from Kroetenlied import klShots as Shots
	from Kroetenlied import klAssets as Assets
	from Kroetenlied import klTasks as Tasks
except Exception, e:
	print e



##############################################################################################
#
#
#		Settings
#

ROOT_ASSETS = "V:/045_Assets"
ROOT_SHOTS = "V:/050_Shots"

templateShots = """
%(ROOT_SHOTS)s/%(TaskNum)s_%(TaskName)s
%(ROOT_SHOTS)s/%(TaskNum)s_%(TaskName)s/%(Name)s_%(TaskName)s
%(ROOT_SHOTS)s/%(TaskNum)s_%(TaskName)s/%(Name)s_%(TaskName)s/%(Name)s_%(TaskName)s_OUT
%(ROOT_SHOTS)s/%(TaskNum)s_%(TaskName)s/%(Name)s_%(TaskName)s/%(Name)s_%(TaskName)s_WORK
"""

templateAsset = """
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(TaskNum)s_%(Name)s_%(TaskName)s
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(TaskNum)s_%(Name)s_%(TaskName)s/%(Name)s_%(TaskName)s_MASTER
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(TaskNum)s_%(Name)s_%(TaskName)s/%(Name)s_%(TaskName)s_VERSIONS
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(TaskNum)s_%(Name)s_%(TaskName)s/%(Name)s_%(TaskName)s_WORK
"""


##############################################################################################
#
#
#		Helpers
#

def createFolder(path):
	#return
	if not os.path.exists(path):
		print "CreateFolder: " + path
		os.makedirs(path)


def solveTemple(template):
	for line in template.split("\n")[1:-1]:
		createFolder(line)


def createAsset(Num, Name):
	#Num = Num
	#Name = Name

	for TaskNum, TaskName in Tasks.Asset:
		template = templateAsset % {
						"Num"	: Num,
						"Name"	: Name,
					"TaskNum"	: TaskNum,
					"TaskName"	: TaskName,
				"ROOT_ASSETS"	: ROOT_ASSETS
									}
		solveTemple(template)


class vuFolderCreator(QtGui.QWidget):
	def __init__(self, parent=None):
		super(vuFolderCreator, self).__init__()
		self.parent = parent


		self.ui_NumLabel = QtGui.QLabel("Num:")
		self.ui_NameLabel = QtGui.QLabel("Name:")

		self.ui_Num = QtGui.QLineEdit()
		self.ui_Name = QtGui.QLineEdit()

		self.ui_ButtonCreateAsset = QtGui.QPushButton("create Folders: Asset")
		self.ui_ButtonCreateAsset.setEnabled(False)


		self.ui_ButtonCreateAsset.clicked.connect(self.buttonClicked_CreateAsset)
		self.ui_Num.textEdited.connect(self.checkValid)
		self.ui_Name.textEdited.connect(self.checkValid)

		validator=QtGui.QRegExpValidator(QtCore.QRegExp("[0-9][0-9][0-9]"), self.ui_Num)
		self.ui_Num.setValidator(validator)

		validator=QtGui.QRegExpValidator(QtCore.QRegExp("^[a-zA-Z0-9]+$"), self.ui_Name)
		self.ui_Name.setValidator(validator)

		mainGrid = QtGui.QGridLayout()
		self.setLayout(mainGrid)

		mainGrid.addWidget(self.ui_NumLabel, 0, 0)
		mainGrid.addWidget(self.ui_NameLabel, 0, 1)
		mainGrid.addWidget(self.ui_Num, 1, 0)
		mainGrid.addWidget(self.ui_Name, 1, 1)
		mainGrid.addWidget(self.ui_ButtonCreateAsset, 1, 3)



	def checkValid(self):
		Num = str(self.ui_Num.text())
		Name = str(self.ui_Name.text())


		if len(Num) == 3 and Name:
			self.ui_ButtonCreateAsset.setEnabled(True)
		else:
			self.ui_ButtonCreateAsset.setEnabled(False)


	def buttonClicked_CreateAsset(self):
		Num = str(self.ui_Num.text())
		Name = str(self.ui_Name.text())

		if not Name:
			print "Enter a Name"
			return False

		if "_" in Name:
			print "Plaease check your Name!"


		createAsset(Num, Name)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	window = vuFolderCreator()
	window.show()
	app.exec_()