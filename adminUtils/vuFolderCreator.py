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

TASKS_SHOTS = []
TASKS_SHOTS += [("010", "TRACK")]
TASKS_SHOTS += [("020", "MATTEPAINT")]
TASKS_SHOTS += [("025", "3D")]
TASKS_SHOTS += [("030", "ANIM")]
TASKS_SHOTS += [("040", "SIM")]
#TASKS_SHOTS += [("045", "SFS")]
TASKS_SHOTS += [("050", "LIGHT")]
TASKS_SHOTS += [("055", "SLAPCOMP")]
TASKS_SHOTS += [("060", "COMP")]


templateShots = "%(ROOT_SHOTS)s/%(taskNum)s_%(taskName)s/%(shotName)s_%(taskName)s/%(shotName)s_%(taskName)s"



'''
templateAsset = """
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(taskNum)s_%(Name)s_%(taskName)s
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(taskNum)s_%(Name)s_%(taskName)s/%(Name)s_%(taskName)s_MASTER
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(taskNum)s_%(Name)s_%(taskName)s/%(Name)s_%(taskName)s_VERSIONS
%(ROOT_ASSETS)s/%(Num)s_%(Name)s/%(taskNum)s_%(Name)s_%(taskName)s/%(Name)s_%(taskName)s_WORK
"""
'''


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



def createShot(shotName, tasks):

	values = {}
	values["ROOT_SHOTS"] = ROOT_SHOTS
	values["shotName"]   = shotName

	for taskNum, taskName in tasks:
		values["taskNum"] = taskNum
		values["taskName"] = taskName

		template = templateShots % values
		createFolder(template + "_OUT")
		createFolder(template + "_WORK")

		if taskName == "COMP":
			createFolder(template + "_WORK/prerender")
		if taskName in ["SIM", "LIGHT"]:
			createFolder(template + "_WORK/rendercache")




class vuFolderCreator(QtGui.QWidget):
	def __init__(self, parent=None):
		super(vuFolderCreator, self).__init__()
		self.parent = parent

		self.nameRegEx = QtCore.QRegExp("[a-zA-Z]_[0-9]{5}")


		########################################
		#
		#	Widgets
		#

		self.uiName = QtGui.QLineEdit()
		self.uiName.textEdited.connect(self.checkValid)
		validator = QtGui.QRegExpValidator(self.nameRegEx, self.uiName)
		self.uiName.setValidator(validator)

		self.ui_ButtonCreateShot = QtGui.QPushButton("Create")
		self.ui_ButtonCreateShot.setEnabled(False)
		self.ui_ButtonCreateShot.clicked.connect(self.buttonClicked_CreateFolders)


		# Tasks
		n = 0
		numTasks = len(TASKS_SHOTS)
		layoutTasks = QtGui.QGridLayout()
		self.taskCheckboxes = []
		for taskNum, taskName in TASKS_SHOTS:
			chkbx = QtGui.QCheckBox(taskName)
			self.taskCheckboxes += [((taskNum, taskName), chkbx)]

			layoutTasks.addWidget(chkbx, n%4, (n - n%4) / 4)
			n += 1






		########################################
		#
		#	Layout
		#


		mainGrid = QtGui.QGridLayout()

		mainGrid.addWidget(QtGui.QLabel("Name:"), 0, 0)
		mainGrid.addWidget(self.uiName, 0, 1)
		mainGrid.addWidget(QtGui.QLabel("Tasks:"), 1, 0)
		mainGrid.addLayout(layoutTasks, 2, 0, 1, 2)
		mainGrid.addWidget(self.ui_ButtonCreateShot, 3, 3)

		mainGrp = QtGui.QGroupBox("Folder Creator:")
		mainGrp.setLayout(mainGrid)

		mainlayout = QtGui.QHBoxLayout()
		mainlayout.addWidget(mainGrp)
		mainlayout.setMargin(0)
		self.setLayout(mainlayout)




	def checkValid(self):
		nameValue = str(self.uiName.text())

		if self.nameRegEx.exactMatch(nameValue):
			self.ui_ButtonCreateShot.setEnabled(True)
		else:
			self.ui_ButtonCreateShot.setEnabled(False)



	def buttonClicked_CreateFolders(self):
		nameValue = str(self.uiName.text())

		tasks = [taskName for taskName, chkbx in self.taskCheckboxes if chkbx.isChecked()]
		createShot(nameValue, tasks)




if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	window = vuFolderCreator()
	window.show()
	app.exec_()

	#createShot("Z_90200", [("010", "SIM"), ("020", "LIGHT"), ("030", "COMP")])