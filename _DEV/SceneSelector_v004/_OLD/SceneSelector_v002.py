##############################################################################################
#
#
#		Info
#

# TODO:
# Fix ExploreFolder



from PyQt4 import QtCore, QtGui
import os
import datetime
import getpass

import sys
sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules")
import Kroetenlied_AssetNames, Kroetenlied_TaskNames

##############################################################################################
#
#
#		Settings
#
ROOT = "//bigfoot/kroetenlied/045_Production_Film/3D/ASSETS/Charakter"
MAYA_BATCH = "//bigfoot/kroetenlied/060_Software/vuPipeline/startMaya.bat"
HEADER_IMG = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules\SceneSelector/Header_SceneSelector_v003_vu.png"
LOG_FILE = "//bigfoot/kroetenlied/_User/Vincent/Pipeline/LogFile_SceneSelector.log"



##############################################################################################
#
#
#		Helper
#

def fileSize_HumanReadable(num):
	for x in ['bytes','KB','MB','GB']:
		if num < 1024.0 and num > -1024.0:
			return "%3.1f%s" % (num, x)
		num /= 1024.0
	return "%3.1f%s" % (num, 'TB')


def timeStamp_Format(time):
	return datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M:%S')


def log(event):
	lines = open(LOG_FILE, 'r').readlines()

	newLine = "\n"
	newLine += "Time: " + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	newLine += " || User: " + getpass.getuser()
	newLine += " || Event: " + event

	lines.append(newLine)
	out = open(LOG_FILE, 'w')
	out.writelines(lines)
	out.close()

##############################################################################################
#
#
#		Core
#


def findFiles(view):
	results = []


	if not view.fullFolder:
		return results

	if not os.path.exists(view.fullFolder):
		return

	for sceneFile in os.listdir(view.fullFolder):
		if os.path.isfile(view.fullFolder + "\\" + sceneFile):
			results.append(sceneFile)

	return sorted(results, reverse=True)


def updateDetails(view):
	if not view.sceneFileName:
		return False

	if not os.path.isfile(view.sceneFilePath):
		return False

	# Set Data
	view.detailsLastModi.setText(timeStamp_Format(os.path.getmtime(view.sceneFilePath)))
	view.detailsSize.setText(fileSize_HumanReadable(os.path.getsize(view.sceneFilePath)))


def openScene_Maya(view):
	log("OpenMaya: " + view.sceneFilePath)
	os.system(MAYA_BATCH + " " + view.sceneFilePath)


def listCtxt_ExploreFile(view):
	log("ExploreFile: " + view.sceneFilePath)
	os.system("explorer /select," + view.sceneFilePath.replace("/", "\\"))

def listCtxt_ExploreFolder(view):
	log("ExploreFolder: " + view.fullFolder)
	os.system("explorer /root," + view.fullFolder.replace("/", "\\"))

##############################################################################################
#
#
#		PyQt-Stuff
#

class vuPipelineOverView(QtGui.QMainWindow):
	def __init__(self, parent=None):
		# Vars
		self.assetName = None
		self.assetFolder = None
		self.taskName = None
		self.taskFolder = None
		self.fullFolder = None
		self.sceneFileName = None
		self.sceneFilePath = None


		QtGui.QMainWindow.__init__(self, parent)


		# Layout Start
		self.setWindowTitle("Kroetenlied - SceneSelector")
		main_grid = QtGui.QGridLayout()
		mainWidget = QtGui.QWidget()
		self.setCentralWidget(mainWidget)
		mainWidget.setLayout(main_grid)

		grp_assets = QtGui.QGroupBox("")
		grid_assets = QtGui.QGridLayout()
		grp_assets.setLayout(grid_assets)
		main_grid.addWidget(grp_assets, 1, 0, 1, 3)
		main_grid.setRowStretch(1, 1)
		grid_assets.setRowStretch(2, 1)


		header = QtGui.QLabel()
		header.setPixmap(QtGui.QPixmap(HEADER_IMG))
		main_grid.addWidget(header, 0, 0, 1, 3)


		#########################
		#						#
		#		DropDowns		#
		#						#
		#########################
		grid_assets.addWidget(QtGui.QLabel("Type:"), 0, 0)
		self.dropDownType = QtGui.QComboBox()
		self.dropDownType.addItems(["Assets", "Shots"])
		grid_assets.addWidget(self.dropDownType, 1, 0)
		self.connect(self.dropDownType, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateList)

		self.dropDownType.setEnabled (False)

		grid_assets.addWidget(QtGui.QLabel("Asset:"), 0, 1)
		self.dropDownAssetNames = QtGui.QComboBox()
		self.dropDownAssetNames.addItems(Kroetenlied_AssetNames.assetNamesFull)
		grid_assets.addWidget(self.dropDownAssetNames, 1, 1)
		self.connect(self.dropDownAssetNames, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateList)

		grid_assets.addWidget(QtGui.QLabel("Task:"), 0, 2)
		self.dropDownTaskNames = QtGui.QComboBox()
		self.dropDownTaskNames.addItems(Kroetenlied_TaskNames.tasksNames3D_Names)
		grid_assets.addWidget(self.dropDownTaskNames, 1, 2)
		self.connect(self.dropDownTaskNames, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateList)
		self.updateDropDowns()


		#########################
		#						#
		#		SceneList		#
		#						#
		#########################
		self.sceneList = QtGui.QListWidget()
		self.sceneList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.sceneList, QtCore.SIGNAL("itemSelectionChanged()"), self.listDetailsUpdate)
		self.connect(self.sceneList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.listDoubleClick)
		self.connect(self.sceneList, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.listRightClick)
		grid_assets.addWidget(self.sceneList, 2, 0, 1, 3)
		self.updateList()




		#########################
		#						#
		#		Details			#
		#						#
		#########################
		grp_details = QtGui.QGroupBox("Info:")
		grid_details = QtGui.QGridLayout()
		grp_details.setLayout(grid_details)
		main_grid.addWidget(grp_details, 3, 0, 1, 3)

		grid_details.addWidget(QtGui.QLabel("Date:"), 0, 0)
		self.detailsLastModi = QtGui.QLabel("")
		grid_details.addWidget(self.detailsLastModi, 0, 1)

		grid_details.addWidget(QtGui.QLabel("Size:"), 1, 0)
		self.detailsSize = QtGui.QLabel("")
		grid_details.addWidget(self.detailsSize, 1, 1)

		grid_details.addWidget(QtGui.QLabel("Size:"), 0, 2)
		self.detailsSize = QtGui.QLabel("")
		grid_details.addWidget(self.detailsSize, 0, 3)


	def updateVars(self, taskName, assetName):
		self.assetFolder = Kroetenlied_AssetNames.getAssetNum(assetName) + "_" + assetName
		self.taskFolder = Kroetenlied_TaskNames.getTaskNum(taskName) + "_" + Kroetenlied_AssetNames.getShortName(assetName) + "_" + taskName
		self.fullFolder = ROOT + "\\" + self.assetFolder + "\\" + self.taskFolder


	def listDetailsUpdate(self):
		if not self.sceneList.currentItem():
			return

		# Update Vars
		self.sceneFileName = str(self.sceneList.currentItem().text())
		self.sceneFilePath = str(self.fullFolder + "\\" + self.sceneFileName)

		updateDetails(self)


	def updateList(self):
		# Update Vars
		assetName = str(self.dropDownAssetNames.currentText())
		taskName = str(self.dropDownTaskNames.currentText())
		self.updateVars(taskName, assetName)
		#self.sceneFileName = None

		self.sceneList.clear()
		for sceneFile in findFiles(self):
			self.sceneList.addItem(sceneFile)

		self.listDetailsUpdate()


	def updateDropDowns(self):

		enableAssets = [False] * len(Kroetenlied_AssetNames.assetNamesFull)
		enableTasks = [False] * len(Kroetenlied_TaskNames.tasksNames3D_Names)


		for i, assetName in enumerate(Kroetenlied_AssetNames.assetNamesFull):
			for j, taskName in enumerate(Kroetenlied_TaskNames.tasksNames3D_Names):
				self.updateVars(taskName, assetName)
				if findFiles(self):
					enableAssets[i] = True;
					enableTasks[j] = True;

		for i, assetName in enumerate(Kroetenlied_AssetNames.assetNamesFull):
			if not enableAssets[i]:
				self.dropDownAssetNames.setItemData(i, QtCore.QVariant(0), QtCore.Qt.UserRole-1)

		for i, taskName in enumerate(Kroetenlied_TaskNames.tasksNames3D_Names):
			 if not enableTasks[i]:
				self.dropDownTaskNames.setItemData(i, QtCore.QVariant(0), QtCore.Qt.UserRole-1)


	def listDoubleClick(self, item):
		openScene_Maya(self)

	def listCtxt_OpenFolder(self):
		if self.sceneFileName:
			print "Some items in List"
			listCtxt_ExploreFile(self)	# Some Items in List
		else:
			print "Empty"
			listCtxt_ExploreFolder(self)		# Empty List


	def listRightClick(self, QPos):
		self.listMenu= QtGui.QMenu()

		# Show in Folder
		ctxt_showFolder = self.listMenu.addAction("Show in Folder")
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.listCtxt_OpenFolder)

		# Refresh
		ctxt_showFolder = self.listMenu.addAction("Refresh")
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.updateList)

		parentPosition = self.sceneList.mapToGlobal(QtCore.QPoint(0, 0))
		self.listMenu.move(parentPosition + QPos)
		self.listMenu.show()



if __name__ == "__main__":
	log("main")

	app = QtGui.QApplication(sys.argv)

	form = vuPipelineOverView()
	form.show()
	app.exec_()
