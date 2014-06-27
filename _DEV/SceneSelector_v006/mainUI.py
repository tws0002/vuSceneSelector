from PyQt4 import QtCore, QtGui


import sys
sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/_DEV")
sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules")
import klAssetNames, klTaskNames, klShotNames
from SceneSelector_v005 import core, utils



##############################################################################################
#
#
#		Settings
#

ROOT = "//bigfoot/kroetenlied/045_Production_Film/3D"
HEADER_IMG = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/SceneSelector/Header_SceneSelector_v003_vu.png"
TYPES = ["Assets", "Shots"]


COLOR_SELECTION = "#1a803c"
COLOR_HOVER = "#4d805e"
COLOR_ERROR_EMPTYLIST = "#cc4747"

style = """
QPushButton
{
	background: #FFF;
	padding: 3px;
	border-width: 1px;
	border-color: #828790;
	border-style: solid;
}

QPushButton::hover
{
	background: #4d805e;
}

QGroupBox
{
	border-width: 1px;
	border-color: #828790;
	border-style: solid;
}

QListWidget:item:selected:active
{
	background: #1a803c;
}

QListWidget:item:hover
{
	color: white;
	background: #4d805e;
}

QListWidget:item:selected:!disabled {
	background: #1a803c;
}"""


class PushButton(QtGui.QPushButton):
	def __init__(self, parent=None):
		QtGui.QPushButton.__init__(self, parent)
		self.setMouseTracking(True)

	def enterEvent(self, event):
		self.origStyle = self.styleSheet()
		self.setStyleSheet("QPushButton {background: " + COLOR_HOVER + "}")

	def leaveEvent(self, event):
		self.setStyleSheet(self.origStyle)




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
		self.seq = None
		self.oldAssetName = None
		self.oldTaskName = None
		self.oldSeq = None
		self.oldSceneFile = None

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
		header.setScaledContents(True)


		#########################
		#						#
		#		DropDowns		#
		#						#
		#########################
		gridLeft = QtGui.QGridLayout()


		# Buttons
		self.btnAssets = PushButton("Assets")
		self.btnShots = PushButton("Shots")
		self.btnAssets.clicked.connect(self.btnClick_Assets)
		self.btnShots.clicked.connect(self.btnClick_Shots)

		gridLeft.addWidget(self.btnAssets, 0, 0)
		gridLeft.addWidget(self.btnShots, 0, 1)


		# Labels
		self.labelType = QtGui.QLabel("Type:")
		self.labelName = QtGui.QLabel("Asset:")
		self.labelTask = QtGui.QLabel("Task:")
		self.labelSeq = QtGui.QLabel("Sequence:")

		gridLeft.addWidget(self.labelTask, 1, 0)
		gridLeft.addWidget(self.labelName, 1, 1)
		gridLeft.addWidget(self.labelSeq, 3, 0)


		# DropDown TaskNames
		self.dropDownTaskNames = QtGui.QListWidget()
		self.dropDownTaskNames.addItems(klTaskNames.tasksNames3D_Names)
		self.connect(self.dropDownTaskNames, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.listClick_Left_Task)
		gridLeft.addWidget(self.dropDownTaskNames, 2, 0)
		self.dropDownTaskNames.setMaximumWidth(100)

		# DropDown TaskNames
		self.dropDownSeq = QtGui.QListWidget()
		self.dropDownSeq.addItems(["A","B","C","D","E"])
		self.connect(self.dropDownSeq, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.listClick_Left_Seq)
		gridLeft.addWidget(self.dropDownSeq, 4, 0)
		self.dropDownSeq.setMaximumWidth(100)

		# DropDown AssetNames
		self.dropDownAssetNames = QtGui.QListWidget()
		self.dropDownAssetNames.addItems(klAssetNames.AssetNames)
		self.connect(self.dropDownAssetNames, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.listClick_Left_Asset)
		gridLeft.addWidget(self.dropDownAssetNames, 2, 1, 3, 1)

		self.dropDownAssetNames.setMaximumWidth(100)


		gridLeft.setRowStretch(2, 1)
		gridLeft.setRowStretch(4, 1)


		gridRight = QtGui.QGridLayout()

		#########################
		#						#
		#		SceneList		#
		#						#
		#########################
		self.sceneList = QtGui.QListWidget()
		self.sceneList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.sceneList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.listClick_Left_Scene)
		self.connect(self.sceneList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.listDoubleClick)
		self.connect(self.sceneList, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.listClick_Right)
		gridRight.addWidget(self.sceneList, 0, 0)


		#########################
		#						#
		#        Details        #
		#						#
		#########################
		gridDetails = QtGui.QGridLayout()
		grpDetails = QtGui.QGroupBox("")
		grpDetails.setLayout(gridDetails)

		self.detailsSize = QtGui.QLabel("")
		self.detailsTime = QtGui.QLabel("")
		gridDetails.addWidget(self.detailsTime, 1, 0)
		gridDetails.addWidget(self.detailsSize, 1, 1)
		gridDetails.addWidget(QtGui.QLabel("Date:"), 0, 0)
		gridDetails.addWidget(QtGui.QLabel("Size:"), 0, 1)


		gridRight.addWidget(grpDetails, 1, 0)



		#########################
		#						#
		#         Main          #
		#						#
		#########################
		main_grid = QtGui.QGridLayout()
		main_grid.addWidget(header, 0, 0, 1,2)
		main_grid.addLayout(gridLeft, 1, 0)
		main_grid.addLayout(gridRight, 1, 1)


		mainWidget = QtGui.QWidget()
		mainWidget.setLayout(main_grid)

		QtGui.QMainWindow.__init__(self, parent)
		self.setWindowTitle("Kroetenlied - SceneSelector")
		self.setCentralWidget(mainWidget)

		# Update that shit
		#self.updateList()

		self.btnClick_Assets()
		self.setStyleSheet(style)
		self.gridLeft = gridLeft



	#                       #
	#                       #
#################################
	#                       #
	#        Updates        #
	#                       #
#################################
	#                       #
	#                       #

	def updateVars(self):
		if self.dropDownAssetNames.currentItem():
			self.assetName = str(self.dropDownAssetNames.currentItem().text())

		if self.dropDownTaskNames.currentItem():
			self.taskName = str(self.dropDownTaskNames.currentItem().text())

		if self.dropDownSeq.currentItem():
			self.seq = str(self.dropDownSeq.currentItem().text())



		if not self.assetName or not self.taskName or not self.seq:
			return

		if self.sceneType == TYPES[0]:
			self.sceneFolder = ROOT + "\\ASSETS\\Charakter\\"
			self.sceneFolder += klAssetNames.getNum(self.assetName) + "_" + self.assetName + "\\"
			self.sceneFolder += klTaskNames.getTaskNum(self.taskName) + "_" + klAssetNames.getCode(self.assetName) + "_" + self.taskName

		else:
			self.sceneFolder = ROOT + "\\SHOTS\\"
			self.sceneFolder += klTaskNames.getTaskNum(self.taskName) + "_" + self.taskName + "\\"
			self.sceneFolder += klShotNames.getCode(self.assetName) + "_" + self.taskName + "_" + klShotNames.getName(self.assetName)



	def updateList(self):
		# Clear List and Details
		self.sceneList.clear()
		self.listDetails_Clear()
		self.sceneFile = None

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

	def updateList_Assets(self):
		selSequence = self.dropDownSeq.currentItem()
		if selSequence:
			if self.sceneType == "Assets":
				if selSequence.text() == "Heros":
					assets = [assetName for assetName in klAssetNames.AssetNames if not assetName.startswith("Musik")]
				else:
					assets = [assetName for assetName in klAssetNames.AssetNames if assetName.startswith("Musik")]

				self.dropDownAssetNames.clear()
				self.dropDownAssetNames.addItems(assets)


	def listClick_Left(self):
		# Update Vars
		self.updateVars()

		# Check Lists
		check = True
		for listWidget in [self.dropDownTaskNames, self.dropDownSeq, self.dropDownAssetNames]:
			if listWidget.currentItem():
				listWidget.setStyleSheet("QListWidget {background: white}")
			else:
				listWidget.setStyleSheet("QListWidget {background: " + COLOR_ERROR_EMPTYLIST +"}")
				check = False

		if check:
			self.updateList()
		else:
			self.sceneList.clear()


	def listClick_Left_Task(self, item):
		self.listClick_Left()

	def listClick_Left_Seq(self, item):
		self.updateList_Assets()
		self.listClick_Left()

	def listClick_Left_Asset(self, item):
		self.listClick_Left()


	def listClick_Left_Scene(self, item):
		self.sceneFile = self.sceneFolder + "/" + str(item.text())
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

		print "RIGHT: self.oldSceneFile: " + str(self.oldSceneFile)


	def listDoubleClick(self, item):
		core.openScene_Maya(self.sceneFilePath)



	def listRezise(self, listWidget):
		#listWidget.setMaximumHeight(listWidget.count() * 17 + 4)
		listWidget.setMinimumHeight(listWidget.count() * 17 + 4)



	def btnHelper_ClearLists(self):
		self.dropDownAssetNames.clear()
		self.dropDownTaskNames.clear()
		self.dropDownSeq.clear()


	def btnHelper_RestoreData(self):
		# Swap Variables
		self.seq, self.oldSeq = self.oldSeq, self.seq
		self.taskName, self.oldTaskName = self.oldTaskName, self.taskName
		self.assetName, self.oldAssetName = self.oldAssetName, self.assetName
		tmpSceneFile = self.oldSceneFile
		self.oldSceneFile = self.sceneFile

		if self.seq:
			item = self.dropDownSeq.findItems(self.seq, QtCore.Qt.MatchExactly)
			if item:
				self.dropDownSeq.setCurrentItem(item[0])

		if self.taskName:
			item = self.dropDownTaskNames.findItems(self.taskName, QtCore.Qt.MatchExactly)
			if item:
				self.dropDownTaskNames.setCurrentItem(item[0])

		# Update Asset-List
		self.updateList_Assets()
		if self.assetName:
			item = self.dropDownAssetNames.findItems(self.assetName, QtCore.Qt.MatchExactly)
			if item:
				self.dropDownAssetNames.setCurrentItem(item[0])

		# Update Lists / Update Scene-List
		self.listClick_Left()

		if tmpSceneFile:
			self.sceneFile = tmpSceneFile
			item = self.sceneList.findItems(self.sceneFile.split("/")[-1], QtCore.Qt.MatchExactly)	#TODO: Fix .split
			if item:
				self.sceneList.setCurrentItem(item[0])
				self.listDetails_Update()


	def btnClick_Assets(self):
		self.sceneType = "Assets"

		# Update Button Colors
		self.btnShots.setStyleSheet('QPushButton {background: white}')
		self.btnAssets.setStyleSheet("QPushButton {background: " + COLOR_SELECTION + "}")
		self.btnAssets.origStyle = "QPushButton {background: " + COLOR_SELECTION + "}"

		self.labelName.setText("Asset:")
		self.labelSeq.setText("Groups:")

		self.btnHelper_ClearLists()

		self.dropDownTaskNames.addItems(klTaskNames.tasksNames3D_Names)
		self.dropDownSeq.addItems(["Heros", "MusikKroeten"])

		self.btnHelper_RestoreData()

		self.listRezise(self.dropDownTaskNames)
		self.listRezise(self.dropDownSeq)


	def btnClick_Shots(self):
		self.sceneType = "Shots"

		# Update Button Colors
		self.btnAssets.setStyleSheet('QPushButton {background: white}')
		self.btnShots.setStyleSheet("QPushButton {background: " + COLOR_SELECTION + "}")
		self.btnShots.origStyle = "QPushButton {background: " + COLOR_SELECTION + "}"

		self.labelName.setText("Shots:")
		self.labelSeq.setText("Sequence:")

		self.btnHelper_ClearLists()

		self.dropDownAssetNames.addItems(klShotNames.ShotNamesCompl)
		self.dropDownTaskNames.addItems(klTaskNames.tasksNamesShots_Names)
		self.dropDownSeq.addItems(klShotNames.ShotSeq)

		self.btnHelper_RestoreData()

		self.listRezise(self.dropDownTaskNames)
		self.listRezise(self.dropDownSeq)







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