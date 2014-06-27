from PyQt4 import QtCore, QtGui


import sys
sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules")
import klAssetNames, klTaskNames, klShotNames

sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/_DEV")
from SceneSelector_v008 import core, utils, style



##############################################################################################
#
#
#		Settings
#

ROOT = "//bigfoot/kroetenlied/045_Production_Film/3D"
TYPES = ["Assets", "Shots"]


##############################################################################################
#
#
#		Helpers
#


def listRezise(listWidget, hMin, wMin, hMax=None, wMax=None):
	listWidget.setMinimumHeight(hMin)
	listWidget.setMaximumHeight(hMax if hMax else hMin)

	listWidget.setMinimumWidth(wMin)
	listWidget.setMaximumWidth(wMax if wMax else wMin)


def list_SetSelection(listWidget, name, setColor=True):
	item = listWidget.findItems(name, QtCore.Qt.MatchExactly)
	if item:
		listWidget.setCurrentItem(item[0])
		if setColor:
			listWidget.setStyleSheet("QListWidget {background: " + style.COLOR_LIST +"}")
		return True
	else:
		if setColor:
			listWidget.setStyleSheet("QListWidget {background: " + style.COLOR_ERROR_EMPTYLIST +"}")
		return False



##############################################################################################
#
#
#		PyQt-Stuff
#
class vuPipelineOverView(QtGui.QMainWindow):
	def __init__(self, parent=None):
		style.dark()

		# Vars
		self.sceneFolder = ""	# Current Folder
		self.sceneFile = ""		# Current SceneFile

		# Variables for Interface
		self.selType = ""
		self.selGroup = ""
		self.selTask = ""
		self.selName = ""
		self.selScene = ""

		# Dict to Store all CoreValues
		self.values = {
			"SceneType": "",
			"AssetGroup": "",
			"AssetTask": "",
			"AssetName": "",
			"AssetScene": "",
			"ShotSeq": "",
			"ShotTask": "",
			"ShotName": "",
			"ShotScene": "",
		}


		#########################
		#						#
		#        Header         #
		#						#
		#########################
		header = QtGui.QLabel()
		header.setPixmap(QtGui.QPixmap(style.HEADER_IMG))


		#########################
		#						#
		#         lists         #
		#						#
		#########################
		gridLists = QtGui.QGridLayout()

		# Labels
		self.labelType = QtGui.QLabel("Type:")
		self.labelName = QtGui.QLabel("Asset:")
		self.labelTask = QtGui.QLabel("Task:")
		self.labelSeq = QtGui.QLabel("Sequence:")
		self.labelScenes = QtGui.QLabel("Scenes:")


		# list Seq
		self.listType = QtGui.QListWidget()
		self.listSeq = QtGui.QListWidget()
		self.listTaskNames = QtGui.QListWidget()
		self.listAssetNames = QtGui.QListWidget()

		self.listType.addItems(TYPES)

		self.connect(self.listType, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.mouseClickLeft_List_Type)
		self.connect(self.listSeq, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.mouseClickLeft_List_Group)
		self.connect(self.listTaskNames, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.mouseClickLeft_List_Task)
		self.connect(self.listAssetNames, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.mouseClickLeft_List_Asset)

		widthSmall = 82
		widthWide = 150

		listRezise(self.listType, 172-(17*3), widthSmall)
		listRezise(self.listSeq, 172-(17*3), widthSmall)
		listRezise(self.listTaskNames, 172-(17*3), widthSmall)
		listRezise(self.listAssetNames, 172-(17*3), widthWide)

		gridLists.setRowStretch(3, 1)

		gridLists.addWidget(self.labelType, 0, 0)
		gridLists.addWidget(self.listType, 1, 0)

		gridLists.addWidget(self.labelSeq, 0, 1)
		gridLists.addWidget(self.listSeq, 1, 1)

		gridLists.addWidget(self.labelTask, 0, 3)
		gridLists.addWidget(self.listTaskNames, 1, 3)

		gridLists.addWidget(self.labelName, 0, 2)
		gridLists.addWidget(self.listAssetNames, 1, 2)


		gridScenes = QtGui.QGridLayout()

		#########################
		#						#
		#		SceneList		#
		#						#
		#########################
		self.sceneList = QtGui.QListWidget()
		self.sceneList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.sceneList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.mouseClickLeft_List_Scene)
		self.connect(self.sceneList, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.mouseClickRight_List_Scene)
		self.connect(self.sceneList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.mouseClickDouble_List_Scene)
		gridScenes.addWidget(self.sceneList, 0, 0)

		self.sceneList.setStyleSheet("QListWidget{background: #262626}")



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

		gridScenes.addWidget(grpDetails, 1, 0)


		#########################
		#						#
		#         Main          #
		#						#
		#########################
		main_grid = QtGui.QGridLayout()
		main_grid.addWidget(header, 0, 0)

		main_grid.addLayout(gridLists, 1, 0)
		main_grid.addWidget(self.labelScenes, 2, 0)
		main_grid.addLayout(gridScenes, 3, 0)

		main_grid.setRowStretch(3, 1)


		mainWidget = QtGui.QWidget()
		mainWidget.setLayout(main_grid)

		QtGui.QMainWindow.__init__(self, parent)
		self.setWindowTitle("Kroetenlied - SceneSelector")
		self.setCentralWidget(mainWidget)

		self.setStyleSheet(style.STYLE)

		if core.loadData(self):
			self.loadValues()
			self.updateLists()
		self.updateList_TextColor()


	def closeEvent(self, event):
		core.storeData(self.values)



	#                       #
	#                       #
#################################
	#                       #
	#      Context-Menu     #
	#                       #
#################################
	#                       #
	#                       #

	def listCtxt_Refresh(self):
		self.updateLists()

	def listCtxt_OpenFolder(self):
		if self.sceneFile:
			core.listCtxt_ExploreFile(self.sceneFile)
		else:
			core.listCtxt_ExploreFolder(self.sceneFolder)

	#                       #
	#                       #
#################################
	#                       #
	#        Updates        #
	#                       #
#################################
	#                       #
	#                       #

	def listDetails_Clear(self):
		self.detailsTime.setText("")
		self.detailsSize.setText("")
		return True


	def listDetails_Update(self):
		self.detailsTime.setText(utils.getFile_LastModify(self.sceneFile))
		self.detailsSize.setText(utils.getFile_FileSize(self.sceneFile))
		return True


	def updateValues(self):
		self.values["SceneType"] = self.selType

		if self.selType == TYPES[0]:
			self.values["AssetGroup"] = self.selGroup
			self.values["AssetTask"] = self.selTask
			self.values["AssetName"] = self.selName
			self.values["AssetScene"] = self.selScene

		elif self.selType == TYPES[1]:
			self.values["ShotSeq"] = self.selGroup
			self.values["ShotTask"] = self.selTask
			self.values["ShotName"] = self.selName
			self.values["ShotScene"] = self.selScene

		return True


	def loadValues(self):
		self.selType = self.values["SceneType"]

		if self.selType == TYPES[0]:
			self.selGroup = self.values["AssetGroup"]
			self.selTask = self.values["AssetTask"]
			self.selName = self.values["AssetName"]
			self.selScene = self.values["AssetScene"]

		elif self.selType == TYPES[1]:
			self.selGroup = self.values["ShotSeq"]
			self.selTask = self.values["ShotTask"]
			self.selName = self.values["ShotName"]
			self.selScene = self.values["ShotScene"]

		return True


	def updateLists(self):
		self.listType.clear()
		self.listSeq.clear()
		self.listTaskNames.clear()
		self.listAssetNames.clear()
		self.sceneList.clear()

		# SelType
		self.listType.addItems(TYPES)
		selType = self.values["SceneType"]
		list_SetSelection(self.listType, selType)


		# Seq + Task = Type Dependent:
		if selType  == TYPES[0]:
			self.listSeq.addItems(["Heros", "MusikKroeten"])
			self.listTaskNames.addItems(klTaskNames.tasksNames3D_Names)

			selGroup = self.values["AssetGroup"]
			selTask = self.values["AssetTask"]

		else:
			self.listSeq.addItems(klShotNames.ShotSeq)
			self.listTaskNames.addItems(klTaskNames.tasksNamesShots_Names)

			selGroup = self.values["ShotSeq"]
			selTask = self.values["ShotTask"]

		list_SetSelection(self.listSeq, selGroup)
		list_SetSelection(self.listTaskNames, selTask)


		# Assets + Shots = Seq Dependent
		if selType  == TYPES[0]:
			names = [name for name in klAssetNames.AssetNames if klAssetNames.getGrp(name) == selGroup]
			selName = self.values["AssetName"]
		elif selType == TYPES[1]:
			names = [name for name in klShotNames.ShotNamesCompl if klShotNames.getSeq(name) == selGroup]
			selName = self.values["ShotName"]

		self.listAssetNames.addItems(names)
		list_SetSelection(self.listAssetNames, selName)


		# Scenes = Asset/Shot Dependent
		if "" in [selType, selGroup, selTask, selName]:
			self.listDetails_Clear()
			return

		if selType  == TYPES[0]:
			self.sceneFolder = ROOT + "\\ASSETS\\Charakter\\"
			self.sceneFolder += klAssetNames.getNum(selName) + "_" + selName + "\\"
			self.sceneFolder += klTaskNames.getTaskNum(selTask) + "_" + klAssetNames.getCode(selName) + "_" + selTask
			selScene = self.values["AssetScene"]

		elif selType == TYPES[1]:
			self.sceneFolder = ROOT + "\\SHOTS\\"
			self.sceneFolder += klTaskNames.getTaskNum(selTask) + "_" + selTask + "\\"
			self.sceneFolder += klShotNames.getCode(selName) + "_" + selTask + "_" + klShotNames.getName(selName)
			selScene = self.values["ShotScene"]

		if self.sceneFolder:
			files = core.findFiles(self.sceneFolder)
			if files:
				self.sceneList.addItems(files)
			sceneSelected = list_SetSelection(self.sceneList, selScene,setColor=False)

		if sceneSelected:
			self.sceneFile = self.sceneFolder + "\\" + selScene
			self.listDetails_Update()
		else:
			self.sceneFile = ""
			self.listDetails_Clear()


	def updateList_ItemTextColor(self, listItem, selName, selTask):
		if self.selType  == TYPES[0]:
			sceneFolder = ROOT + "\\ASSETS\\Charakter\\"
			sceneFolder += klAssetNames.getNum(selName) + "_" + selName + "\\"
			sceneFolder += klTaskNames.getTaskNum(selTask) + "_" + klAssetNames.getCode(selName) + "_" + selTask

		elif self.selType == TYPES[1]:
			sceneFolder = ROOT + "\\SHOTS\\"
			sceneFolder += klTaskNames.getTaskNum(selTask) + "_" + selTask + "\\"
			sceneFolder += klShotNames.getCode(selName) + "_" + selTask + "_" + klShotNames.getName(selName)

		if not core.checkFiles(sceneFolder):
			listItem.setTextColor(QtGui.QColor(128,128,128))


	def updateList_TextColor(self):

		# Loop over Tasks
		if self.listAssetNames.currentItem():
			selName = str(self.listAssetNames.currentItem().text())
			for i in range(self.listTaskNames.count()):
				listItem = self.listTaskNames.item(i)
				selTask = str(listItem.text())

				self.updateList_ItemTextColor(listItem, selName, selTask)

		# Loop over Names
		if self.listTaskNames.currentItem():
			selTask = str(self.listTaskNames.currentItem().text())
			for i in range(self.listAssetNames.count()):
				listItem = self.listAssetNames.item(i)
				selName = str(listItem.text())

				self.updateList_ItemTextColor(listItem, selName, selTask)


##############################################################################################
#
#
#		Mouse Clicks
#

	def mouseClickLeft_List_Type(self, item):
		# Set Vars
		self.selType = str(item.text())
		self.values["SceneType"] = self.selType
		self.loadValues()
		self.updateLists()
		self.updateList_TextColor()

		# Change UI
		self.labelName.setText(self.selType)
		self.labelSeq.setText("Groups:") if self.selType == TYPES[0] else self.labelSeq.setText("Sequence:")


	def mouseClickLeft_List_Task(self, item):
		self.selTask = str(item.text())
		self.updateValues()
		self.updateLists()
		self.updateList_TextColor()


	def mouseClickLeft_List_Group(self, item):
		self.selGroup = str(item.text())
		self.updateValues()
		self.updateLists()


	def mouseClickLeft_List_Asset(self, item):
		self.selName = str(item.text())
		self.updateValues()
		self.updateLists()
		self.updateList_TextColor()


	def mouseClickLeft_List_Scene(self, item):
		self.selScene = str(item.text())
		self.updateValues()
		self.sceneFile = self.sceneFolder + "\\" + self.selScene
		self.listDetails_Update()


	def mouseClickRight_List_Scene(self, QPos):
		self.ctxtMenue= QtGui.QMenu()

		# Refresh
		ctxt_showFolder = self.ctxtMenue.addAction("Refresh List")
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.listCtxt_Refresh)

		# Show in Folder
		ctxt_showFolder = self.ctxtMenue.addAction("Show in Folder")
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.listCtxt_OpenFolder)

		parentPosition = self.sceneList.mapToGlobal(QtCore.QPoint(0, 0))
		self.ctxtMenue.move(parentPosition + QPos)
		self.ctxtMenue.show()


	def mouseClickDouble_List_Scene(self, item):
		core.openScene_Maya(self.sceneFile)


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



"""
	def listHelper_AutoSelect(self):
		return
		for listWidget in [self.listSeq, self.listAssetNames, self.listTaskNames, self.sceneList]:
			if not listWidget.currentItem() and listWidget.count() == 1:
				listWidget.setCurrentItem(listWidget.item(0))
				self.checkList(listWidget)
"""