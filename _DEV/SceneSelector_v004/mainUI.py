from PyQt4 import QtCore, QtGui


import sys
sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules")
import klAssetNames, klTaskNames, klShotNames
from SceneSelector import core, utils



##############################################################################################
#
#
#		Settings
#

ROOT = "//bigfoot/kroetenlied/045_Production_Film/3D"
HEADER_IMG = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/SceneSelector/Header_SceneSelector_v003_vu.png"
TYPES = ["Assets", "Shots"]





##############################################################################################
#
#
#		PyQt-Stuff
#
class vuPipelineOverView(QtGui.QMainWindow):
	def __init__(self, parent=None):
		# Vars
		self.assetName = None
		self.taskName = None
		self.sceneFolder = None
		self.sceneFile = None
		self.sceneType = TYPES[0]



		#########################
		#						#
		#        Header         #
		#						#
		#########################
		header = QtGui.QLabel()
		header.setPixmap(QtGui.QPixmap(HEADER_IMG))




		#########################
		#						#
		#		DropDowns		#
		#						#
		#########################
		grpDropDowns = QtGui.QGroupBox("")
		gridDropDowns = QtGui.QGridLayout()
		grpDropDowns.setLayout(gridDropDowns)


		# Labels
		self.labelType = QtGui.QLabel("Type:")
		self.labelName = QtGui.QLabel("Asset:")
		self.labelTask = QtGui.QLabel("Task:")
		gridDropDowns.addWidget(self.labelType, 0, 0)
		gridDropDowns.addWidget(self.labelName, 0, 1)
		gridDropDowns.addWidget(self.labelTask, 0, 2)




		# DropDown Type
		self.dropDownType = QtGui.QListWidget()
		self.dropDownType.addItems(TYPES)
		#self.connect(self.dropDownType, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateDropDowns)
		gridDropDowns.addWidget(self.dropDownType, 1, 0)

		# DropDown AssetNames
		self.dropDownAssetNames = QtGui.QListWidget()
		self.dropDownAssetNames.addItems(klAssetNames.AssetNames)
		#self.connect(self.dropDownAssetNames, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateList)
		gridDropDowns.addWidget(self.dropDownAssetNames, 1, 1)

		# DropDown TaskNames
		self.dropDownTaskNames = QtGui.QListWidget()
		self.dropDownTaskNames.addItems(klTaskNames.tasksNames3D_Names)
		gridDropDowns.addWidget(self.dropDownTaskNames, 1, 2)





		#########################
		#						#
		#		SceneList		#
		#						#
		#########################
		self.sceneList = QtGui.QListWidget()
		self.sceneList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.sceneList, QtCore.SIGNAL("itemSelectionChanged()"), self.listClick_Left)
		self.connect(self.sceneList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.listDoubleClick)
		self.connect(self.sceneList, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.listClick_Right)
		gridDropDowns.addWidget(self.sceneList, 2, 0, 1, 3)


		#########################
		#						#
		#        Details        #
		#						#
		#########################
		gridDetails = QtGui.QGridLayout()
		grpDetails = QtGui.QGroupBox("Info:")
		grpDetails.setLayout(gridDetails)

		self.detailsSize = QtGui.QLabel("")
		self.detailsTime = QtGui.QLabel("")
		gridDetails.addWidget(self.detailsTime, 0, 1)
		gridDetails.addWidget(self.detailsSize, 1, 1)
		gridDetails.addWidget(QtGui.QLabel("Date:"), 0, 0)
		gridDetails.addWidget(QtGui.QLabel("Size:"), 1, 0)


		#########################
		#						#
		#         Main          #
		#						#
		#########################
		main_grid = QtGui.QGridLayout()
		main_grid.addWidget(header, 0, 0, 1, 3)
		main_grid.addWidget(grpDropDowns, 1, 0, 1, 3)
		main_grid.addWidget(grpDetails, 3, 0, 1, 1)

		mainWidget = QtGui.QWidget()
		mainWidget.setLayout(main_grid)

		QtGui.QMainWindow.__init__(self, parent)
		self.setWindowTitle("Kroetenlied - SceneSelector")
		self.setCentralWidget(mainWidget)

		# Update that shit
		self.updateList()


	def updateVars(self):
		#self.taskName = str(self.dropDownTaskNames.currentText())

		self.assetName = "Kroete"	#str(self.dropDownAssetNames.currentItem().text())
		self.taskName = "RIG"		#str(self.dropDownTaskNames.currentItem().text())


		if not self.assetName or not self.taskName:
			return

		if self.sceneType == TYPES[0]:
			self.sceneFolder = ROOT + "\\ASSETS\\Charakter\\"
			self.sceneFolder += klAssetNames.getNum(self.assetName) + "_" + self.assetName + "\\"
			self.sceneFolder += klTaskNames.getTaskNum(self.taskName) + "_" + klAssetNames.getCode(self.assetName) + "_" + self.taskName

		else:
			self.sceneFolder = ROOT + "\\SHOTS\\"
			self.sceneFolder += klTaskNames.getTaskNum(self.taskName) + "_" + self.taskName + "\\"
			self.sceneFolder += klShotNames.getCode(self.assetName) + "_" + self.taskName + "_" + klShotNames.getName(self.assetName)



	#                       #
	#                       #
#################################
	#                       #
	#        Updates        #
	#                       #
#################################
	#                       #
	#                       #
	def updateDropDowns(self):
		self.sceneType = self.dropDownType.currentText()

		self.dropDownAssetNames.clear()
		self.dropDownTaskNames.clear()

		if self.sceneType == TYPES[0]:
			self.labelName.setText("Asset:")
			self.dropDownAssetNames.addItems(klAssetNames.AssetNames)
			self.dropDownTaskNames.addItems(klTaskNames.tasksNames3D_Names)
		else:
			self.labelName.setText("Shot:")
			self.dropDownAssetNames.addItems(klShotNames.ShotNamesCompl)
			self.dropDownTaskNames.addItems(klTaskNames.tasksNamesShots_Names)

		self.updateList()

	def updateList(self):
		# Clear List and Details
		self.sceneList.clear()
		self.listDetails_Clear()
		self.sceneFile = None

		# Update Vars
		self.updateVars()

		# ReFill List
		for sceneFile in core.findFiles(self.sceneFolder):
			self.sceneList.addItem(sceneFile)


	def listDetails_Clear(self):
		self.detailsTime.setText("")
		self.detailsSize.setText("")
		return True


	def listDetails_Update(self):
		self.detailsTime.setText(utils.getFile_LastModify(self.sceneFile))
		self.detailsSize.setText(utils.getFile_FileSize(self.sceneFile))






	#                       #
	#                       #
#################################
	#                       #
	#      Context-Menu     #
	#                       #
#################################
	#                       #
	#                       #
	def listCtxt_OpenFolder(self):
		if self.sceneFile:
			core.listCtxt_ExploreFile(self.sceneFile)
		else:
			core.listCtxt_ExploreFolder(self.sceneFolder)


	################
	# List Clicks
	#
	def listClick_Left(self):
		self.sceneFile = self.sceneFolder + "/" + str(self.sceneList.currentItem().text())
		self.listDetails_Update()

	def listClick_Right(self, QPos):
		self.ctxtMenue= QtGui.QMenu()

		# Refresh
		ctxt_showFolder = self.ctxtMenue.addAction("Refresh List")
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.updateList)

		# Show in Folder
		ctxt_showFolder = self.ctxtMenue.addAction("Show in Folder")
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.listCtxt_OpenFolder)

		parentPosition = self.sceneList.mapToGlobal(QtCore.QPoint(0, 0))
		self.ctxtMenue.move(parentPosition + QPos)
		self.ctxtMenue.show()


	def listDoubleClick(self, item):
		core.openScene_Maya(self.sceneFilePath)


##############################################################################################
#
#
#		Main
#
#
if __name__ == "__main__":
	utils.log("main")

	app = QtGui.QApplication(sys.argv)

	form = vuPipelineOverView()
	form.show()
	app.exec_()