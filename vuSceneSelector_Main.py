#!/usr/bin/env python2.7






# Globals for Modules





from PyQt4 import QtCore, QtGui
import os
import sys
import time








def loadModules():
	WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
	sys.path.append(WORKING_DIR)

	# Settings
	SETTINGS_PROJECT = os.getenv("SETTINGS_PROJECT")
	if not SETTINGS_PROJECT:
		print "[ERROR] SETTINGS_PROJECT not set via Envoriment-Variable!"
		settings_Folder =  os.path.dirname(os.path.abspath(__file__)) + "/_ProjectSettings/"
		SETTINGS_PROJECT = settings_Folder + "project_Jagon.py"
		#SETTINGS_PROJECT = settings_Folder + "project_Kroetenlied.py"
		#SETTINGS_PROJECT = settings_Folder + "project_Flut.py"



	global SETTINGS
	from core import Settings
	SETTINGS = Settings.SETTINGS
	SETTINGS.load(SETTINGS_PROJECT, "r")
	SETTINGS.load(SETTINGS["Settings_User"])



	global ui
	import ui
	import ui.Header

	# Import Modules
	global Index
	from core import Index
	global syncTasks
	from sync import syncTasks

	global style
	from ui import style
	import ui.style
	import ui.ListTemplate
	import ui.ListsAssets
	import ui.ListScenes
	import ui.ListTasks
	import ui.ListHistory
	import ui.SearchBar
	import ui.Help
	import ui.ChangeLog

	global adminMainUI
	from adminUtils import adminMainUI






##############################################################################################
#
#
#		Settings
#

VERSION_MAJOR = "4"
VERSION_MINOR = "6.4"
VERSION = "v0." + VERSION_MAJOR + "." + VERSION_MINOR
DEBUG = os.getenv("DEBUG")

global SPLASH_SCREEN


class vuSplitterHandle(QtGui.QSplitterHandle):
	"""QSplitterHandle-Class to handle MouseHover-Effect"""
	def __init__(self, orientation, parent):
		super(vuSplitterHandle, self).__init__(orientation, parent)
		self.parent = parent
		self.parent.setStyleSheet(style.styleHandleNormal)

	def enterEvent(self, event):
		self.parent.setStyleSheet(style.styleHandleHover)

	def leaveEvent(self, event):
		self.parent.setStyleSheet(style.styleHandleNormal)


class vuSplitter(QtGui.QSplitter):
	"""QSplitter-Class to create custom SplitterHandles"""
	def __init__(self, orientation):
		super(vuSplitter, self).__init__(orientation)
		self.orientation = orientation

	def createHandle(self):
		return vuSplitterHandle(self.orientation, self)


class UpdateThread(QtCore.QThread):
	def __init__(self, parent):
		super(UpdateThread, self).__init__(parent)

		self.parent = parent
		self.running = True
		self.lastCheck = None
		self.startUpTime = os.stat(__file__).st_mtime

	def run(self):
		while self.running:
			# Index changed
			if os.stat(Index.DB_FILENAME).st_mtime != self.lastCheck:
				time.sleep(0.1)
				reload(Index)
				self.lastCheck = os.stat(Index.DB_FILENAME).st_mtime
				self.emit(QtCore.SIGNAL("thread_update()"))


			# Main Changed
			if self.startUpTime != os.stat(__file__).st_mtime:
				self.parent.header.warning.setText("Please Restart !!!")
				self.parent.header.warning.setVisible(True)

			time.sleep(SETTINGS["REFRESH_INTERVALL"])



##############################################################################################
#
#
#		PyQt-Stuff
#
class vuSceneSelector(QtGui.QWidget):
	def __init__(self):
		super(vuSceneSelector, self).__init__()


		# Variables for Interface
		self.selType = ""
		self.filterType = ""
		self.selGroup = ""
		self.selTask = ""
		self.selName = ""
		self.selScene = ""
		self.sceneFolder = ""	# Current Folder
		self.sceneFile = ""		# Current SceneFile

		self.interactive = False
		self.toDo_isDirty = False


		#########################
		#						#
		#        Header         #
		#						#
		#########################
		self.header = ui.Header.Header(self)


		#########################
		#						#
		#         lists         #
		#						#
		#########################
		#
		#	Type
		#
		self.labelType = QtGui.QLabel("Type:")
		self.listType = QtGui.QListWidget()

		gridType = QtGui.QGridLayout()
		gridType.setMargin(0)
		gridType.addWidget(self.labelType, 0, 0)
		gridType.addWidget(self.listType, 1, 0)

		widgetType = QtGui.QWidget()
		widgetType.setLayout(gridType)



		#########################
		#
		#	Sequence/Group
		#

		labelFilter = QtGui.QLabel("Group / Artist:")
		self.listFilter = ui.ListTemplate.ListTemplate()
		self.listFilter.addItems(["-- All --", "-- Favorites --"])

		x = 18
		self.listFilter.setMaximumHeight(x*2)
		self.listFilter.setMinimumHeight(x*2)

		gridFilter = QtGui.QGridLayout()
		gridFilter.setMargin(0)
		gridFilter.addWidget(labelFilter, 0, 0)
		gridFilter.addWidget(self.listFilter, 1, 0)

		widgetFilter = QtGui.QWidget()
		widgetFilter.setLayout(gridFilter)



		#########################
		#
		#	Sequence/Group
		#

		labelSeq = QtGui.QLabel("Group:")
		self.listSeq = ui.ListTemplate.ListTemplate()

		gridSeq = QtGui.QGridLayout()
		gridSeq.setMargin(0)
		gridSeq.addWidget(self.listSeq, 1, 0)

		widgetSeq = QtGui.QWidget()
		widgetSeq.setLayout(gridSeq)


		#########################
		#
		#	Artist
		#

		labelArtist = QtGui.QLabel("Artist:")
		self.listArtist = ui.ListTemplate.ListTemplate()

		gridArtist = QtGui.QGridLayout()
		gridArtist.setMargin(0)
		gridArtist.addWidget(self.listArtist, 1, 0)

		widgetArtist = QtGui.QWidget()
		widgetArtist.setLayout(gridArtist)


		#########################
		#
		#	ShotSearch
		#

		self.searchShot = ui.SearchBar.SearchBar(self)
		self.searchShot.textChanged.connect(self.searchShot_textChanged)




		#########################
		#
		#	Assets
		#

		self.tableAssets = ui.ListsAssets.TableAssets(self)
		self.labelAssets = ui.ListsAssets.TableAssetsHeader(self, self.tableAssets)

		gridAsset = QtGui.QGridLayout()
		gridAsset.setMargin(0)
		gridAsset.setRowStretch(1, 1)
		gridAsset.addWidget(self.labelAssets, 0, 0)
		gridAsset.addWidget(self.tableAssets, 1, 0, 2, 1)

		widgetAsset = QtGui.QWidget()
		widgetAsset.setLayout(gridAsset)


		#########################
		#
		#	Tasks
		#

		self.labelTask = QtGui.QLabel("Task:")
		self.listTasks = ui.ListTasks.ListTasks(self)

		gridTask = QtGui.QGridLayout()
		gridTask.setMargin(0)
		gridTask.addWidget(self.labelTask, 0, 0)
		gridTask.addWidget(self.listTasks, 1, 0)

		widgetTask = QtGui.QWidget()
		widgetTask.setLayout(gridTask)


		#########################
		#						#
		#		SceneList		#
		#						#
		#########################
		self.sceneList = ui.ListScenes.TableScenes(self)
		labelScenes = ui.ListScenes.TableScenesHeader(self, self.sceneList)

		gridScenes = QtGui.QGridLayout()
		gridScenes.setMargin(0)
		gridScenes.addWidget(labelScenes, 0, 0)
		gridScenes.addWidget(self.sceneList, 1, 0)

		widgetScenes = QtGui.QWidget()
		widgetScenes.setLayout(gridScenes)

		#########################
		#						#
		#        Text           #
		#						#
		#########################

		# ToDo
		labelToDo = QtGui.QLabel("ToDo:")
		self.toDo = QtGui.QTextEdit()
		self.toDo.setFocusPolicy(QtCore.Qt.FocusPolicy(QtCore.Qt.ClickFocus))

		# History
		self.history = ui.ListHistory.TableHistory()

		# StatusBar
		self.statusBar = QtGui.QLabel("Status")
		self.statusBar.setAlignment(QtCore.Qt.AlignRight)
		self.statusBar.hide()


		self.tabText = QtGui.QTabWidget()
		self.tabText.addTab(self.toDo, "ToDo")
		self.tabText.addTab(self.history, "History")


		gridText = QtGui.QGridLayout()
		gridText.setMargin(0)
		gridText.addWidget(self.tabText, 0 ,0 )
		gridText.addWidget(self.statusBar, 1, 0)


		widgetText = QtGui.QWidget()
		widgetText.setLayout(gridText)




		self.listWidgetsGroups = [self.listFilter, self.listSeq, self.searchShot, self.listArtist]


		#########################
		#						#
		#        Layout         #
		#						#
		#########################

		# Seq/Artist
		self.splitterGrpArtist = vuSplitter(QtCore.Qt.Vertical)
		self.splitterGrpArtist.addWidget(widgetSeq)
		self.splitterGrpArtist.addWidget(widgetArtist)

		gridGrpArtist = QtGui.QGridLayout()
		gridGrpArtist.setMargin(0)
		gridGrpArtist.addWidget(widgetFilter, 0, 0)
		gridGrpArtist.addWidget(self.searchShot, 1, 0)
		gridGrpArtist.addWidget(self.splitterGrpArtist, 2, 0)
		gridGrpArtist.setRowStretch(2,1)


		widgetGrpArtist = QtGui.QWidget()
		widgetGrpArtist.setLayout(gridGrpArtist)

		# Splitter Lists
		self.splitterLists = vuSplitter(QtCore.Qt.Horizontal)
		self.splitterLists.addWidget(widgetType)
		self.splitterLists.addWidget(widgetGrpArtist)
		self.splitterLists.addWidget(widgetAsset)
		self.splitterLists.addWidget(widgetTask)

		# Splitter Scene / ToDo
		self.splitterSceneToDo = vuSplitter(QtCore.Qt.Horizontal)
		self.splitterSceneToDo.addWidget(widgetScenes)
		self.splitterSceneToDo.addWidget(widgetText)

		# Splitter Vertical
		self.splitterVertical = vuSplitter(QtCore.Qt.Vertical)
		self.splitterVertical.addWidget(self.splitterLists)
		self.splitterVertical.addWidget(self.splitterSceneToDo)




		# Layout SceneSelector
		main_grid = QtGui.QGridLayout()
		main_grid.setMargin(5)
		main_grid.addWidget(self.header, 0, 0)
		main_grid.addWidget(self.splitterVertical, 1, 0)
		main_grid.setRowStretch(1, 1)

		# Add Hidden AdminPage
		sceneSelectorWidget = QtGui.QWidget()
		sceneSelectorWidget.setLayout(main_grid)

		adminPage = adminMainUI.debugPage()

		self.stackLayout = QtGui.QStackedLayout()
		self.stackLayout.addWidget(sceneSelectorWidget)
		self.stackLayout.addWidget(adminPage)
		self.setLayout(self.stackLayout)


		#########################
		#						#
		#         Main          #
		#						#
		#########################
		# Window Settings
		self.setWindowTitle(SETTINGS["projectName"] + " - SceneSelector " + VERSION)
		self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(SETTINGS["Application_Icon"])))
		self.setStyleSheet(style.STYLE)


		##############################
		#
		#		User CallBacks
		#

		self.connect(self.listType, QtCore.SIGNAL("itemSelectionChanged()"), self.changeType)
		self.listFilter.itemSelectionChanged_User	= self.changeGroupFilter
		self.listSeq.itemSelectionChanged_User		= self.changeGroupGroup
		self.listArtist.itemSelectionChanged_User	= self.changeGroupArtist
		self.tableAssets.itemSelectionChanged_User	= self.changeAsset
		self.listTasks.itemSelectionChanged_User	= self.changeTask
		self.sceneList.itemSelectionChanged_User	= self.changeScene
		self.connect(self.toDo, QtCore.SIGNAL("textChanged()"), self.saveToDoEvent)
		self.toDo.focusOutEvent = self.saveToDo

		##############################
		#
		#	Update Thread
		#
		self.updater = UpdateThread(self)
		self.connect(self.updater, QtCore.SIGNAL("thread_update()"), self.updateThread)
		self.updater.start()


		# Load and Apply Saved Data
		self.listType.addItems(Index.getTypes())
		self.loadValues()
		self.loadInterface()
		self.updateToDo()
		try:
			self.listType.setCurrentRow(Index.getTypes().index(self.selType))
		except:
			pass
		self.interactive = True

		self.show()
		SPLASH_SCREEN.close()

		if VERSION != SETTINGS["lastVersion"]:
			self.showChangeLog()
			SETTINGS["lastVersion"] = VERSION
			SETTINGS.save()



	def closeEvent(self, event):
		self.updater.running = False
		self.saveInterface()
		self.saveValues()
		self.saveToDo(None)


	def close(self, event=None):
		self.closeEvent(event)
		QtGui.QApplication.quit()





	#                       #
	#                       #
#################################
	#                       #
	#        Updates        #
	#                       #
#################################
	#                       #
	#                       #

	def saveValues(self):
		# Save Selections
		SETTINGS["selType"] = self.selType
		SETTINGS[self.selType + "FilterType"] = self.filterType
		SETTINGS[self.selType + "Group"] = self.selGroup
		SETTINGS[self.selType + "Task"] = self.selTask
		SETTINGS[self.selType + "Name"] = self.selName
		SETTINGS[self.selType + "Scene"] = self.selScene

		SETTINGS.save()


	def saveToDoEvent(self):
		if self.interactive:
			self.toDo_isDirty = True
			self.statusBar.show()
			self.statusBar.setText("ToDo was changed.... need to Save")
			return True


	def saveToDo(self, event):
		if DEBUG:
			print "Do NOT save ToDo!"
			return True

		if not self.toDo_isDirty:
			print "No need to Save"
			return True

		if "" in [self.selType, self.selGroup, self.selTask, self.selName]:
			print "Cant Save ToDo"
			return True


		# Get Value
		valueUI = unicode(self.toDo.toPlainText())
		#valueUI = valueUI.encode('utf-8')


		# Save
		Index.setValue(self.selName, self.selTask + "_Todo", valueUI)
		syncTasks.addTask(self.selName, self.selTask + "_Todo", valueUI)

		self.toDo_isDirty = False
		self.statusBar.hide()
		return True


	def loadValues(self):
		"""Load Values from Dict, when Switching Type"""
		self.selType = SETTINGS["selType"]
		self.filterType = SETTINGS[self.selType + "FilterType"]
		self.selGroup = SETTINGS[self.selType + "Group"]
		self.selTask = SETTINGS[self.selType + "Task"]
		self.selName = SETTINGS[self.selType + "Name"]
		self.selScene = SETTINGS[self.selType + "Scene"]
		return True


	def saveInterface(self):
		SETTINGS["UI_mainWindow"] 			= self.saveGeometry().toBase64().data()
		SETTINGS["UI_splitterGrpArtist"] 	= self.splitterGrpArtist.saveState().toBase64().data()
		SETTINGS["UI_splitterLists"] 		= self.splitterLists.saveState().toBase64().data()
		SETTINGS["UI_splitterSceneToDo"] 	= self.splitterSceneToDo.saveState().toBase64().data()
		SETTINGS["UI_splitterVertical"] 	= self.splitterVertical.saveState().toBase64().data()


	def loadInterface(self):
		try:
			self.restoreGeometry				(QtCore.QByteArray().fromBase64(SETTINGS["UI_mainWindow"]))
			self.splitterLists.restoreState		(QtCore.QByteArray().fromBase64(SETTINGS["UI_splitterLists"]))
			self.splitterGrpArtist.restoreState	(QtCore.QByteArray().fromBase64(SETTINGS["UI_splitterGrpArtist"]))
			self.splitterVertical.restoreState	(QtCore.QByteArray().fromBase64(SETTINGS["UI_splitterVertical"]))
			self.splitterSceneToDo.restoreState	(QtCore.QByteArray().fromBase64(SETTINGS["UI_splitterSceneToDo"]))
		except:
			print "[WARNING] Couldn't load Interface"




	#                       #
	#                       #
#################################
	#                       #
	#        Updates        #
	#                       #
#################################
	#                       #
	#                       #

	def updateGroups(self):
		"Update Groups-List"
		self.listSeq.setItems(Index.getGroups(self.selType))
		self.listArtist.setItems(Index.getArtists(self.selType))

		# TMP
		for i in xrange(self.listArtist.count()):
			item = self.listArtist.item(i)
			if item.text() == "Julian":
				font = QtGui.QFont()
				font.setStrikeOut(True)
				item.setFont(font)


		for listWidget in self.listWidgetsGroups:
			listWidget.setSelection2(self.selGroup, setDefault=False)


	def updateTasks(self):
		"Update Task-List"
		self.listTasks.setItems([task for task in Index.getTasks(self.selType) if task not in SETTINGS["TASKS_WITHOUT_PATH"]])
		self.listTasks.setSelection2(self.selTask)


	def updateAssets(self):
		"Update Asset/Shot-List"
		self.tableAssets.addNames(self.selType, self.selGroup, self.filterType)
		self.labelAssets.setType(self.selType)

		if not self.tableAssets.setSelection2(self.selName) and self.tableAssets.rowCount():
			self.selName = str(self.tableAssets.currentItem().text())


	def updateScenes(self):
		"Update SceneFolder + SceneList"
		try:
			Vars = {}
			Vars["TASK_NUM"] = Index.getTaskNum(self.selTask)
			Vars["TASK_NAME"] = self.selTask
			Vars["NUM"] = Index.getValue(self.selName, "Num")
			Vars["NAME"] = self.selName
			Vars["CODE"] = Index.getValue(self.selName, "Code")
			Vars["GRP"] = self.selGroup

			# TMP Exeptions
			Vars["GRP"] = Vars["GRP"].replace("Heros", "Charakter").replace("Kinder", "Charakter").replace("MusikKroeten", "Charakter")

			self.sceneFolder = SETTINGS[self.selType + "_FolderTemplate"] % Vars

			self.sceneList.refreshList(self.sceneFolder)
			if not self.sceneList.setSelection2(self.selScene):
				self.selScene = ""

		except Exception, e:
			pass



	def updateHeader(self):
		self.header.setImage(self.selName)

	def updateDesr(self):
		self.header.setText(self.selType, self.selName)



	def updateToDo(self):
		if self.toDo.hasFocus():
			return

		content = ""

		if not self.selName:
			return False
		if not self.selTask:
			return False

		value = Index.getValue(self.selName, self.selTask + "_Todo")
		#value = value.decode('utf-8')
		content = value if value else ""

		#valueUI = unicode(self.toDo.toPlainText())


		if DEBUG:
			content = ""
			content += "self.selType: " + str(self.selType) + "\n"
			content += "self.selGroup: " + str(self.selGroup) + "\n"
			content += "self.selTask: " + str(self.selTask) + "\n"
			content += "self.selName: " + str(self.selName) + "\n"
			content += "self.selScene: " + str(self.selScene) + "\n"
			content += "self.sceneFolder: " + str(self.sceneFolder) + "\n"
			content += "ToDo: " + unicode(value) + "\n"


		self.toDo.setText(content)
		self.toDo_isDirty = False
		self.statusBar.hide()


	def updateThread(self):
		if self.selType in ["", None]:
			return False

		self.interactive = False
		self.updateAssets()
		self.history.refreshHistory()
		self.updateToDo()
		self.interactive = True



##############################################################################################
#
#
#		User Changes
#

	def changeType(self):

		self.saveInterface()

		self.saveValues()
		#self.saveToDo()

		# Set Vars
		item = self.listType.currentItem()
		self.selType = str(item.text())
		SETTINGS["selType"] = self.selType

		# Change UI
		#self.labelAssets.setText(self.selType) # TODO: Fix this?!
		#self.labelSeq.setText(SETTINGS[self.selType + "_GroupLabel"])

		# Update all the other Lists
		self.loadValues()
		self.updateGroups()
		self.updateTasks()
		self.updateAssets()
		self.updateDesr()
		self.updateHeader()
		self.updateToDo()
		self.updateScenes()

		if DEBUG:	self.updateToDo()
		return


	def changeGroup(self, widget):
		# Set Vars
		self.selGroup = str(widget.currentItem().text())

		# Clear Selection on others
		self.interactive = False
		for listWidget in self.listWidgetsGroups:
			if listWidget != widget:
				listWidget.setSelection2(None)
		self.interactive = True


		# Update other Widgets
		self.updateAssets()
		#self.updateDesr()
		#self.updateHeader()
		#self.updateToDo()
		#self.updateScenes()
		if DEBUG:	self.updateToDo()

	def changeGroupFilter(self):
		if self.interactive:
			self.filterType = "global"
			self.changeGroup(self.listFilter)

	def changeGroupGroup(self):
		if self.interactive:
			self.filterType = "group"
			self.changeGroup(self.listSeq)

	def changeGroupArtist(self):
		if self.interactive:
			self.filterType = "artist"
			self.changeGroup(self.listArtist)

	def searchShot_textChanged(self, text):
		if self.interactive:
			self.filterType = "search"
			self.changeGroup(self.searchShot)


	def changeTask(self):
		# Set Vars
		self.selTask = str(self.listTasks.currentItem().text())

		# Update other Widgets
		self.updateToDo()
		self.updateScenes()
		if DEBUG:	self.updateToDo()


	def changeAsset(self):
		# Set Vars
		self.selName = str(self.tableAssets.currentItem().text())

		# Update other Widgets
		self.updateToDo()
		self.updateDesr()
		self.updateHeader()
		self.updateScenes()
		if DEBUG:	self.updateToDo()


	def changeScene(self):
		# Set Vars
		row = self.sceneList.currentRow()
		item = self.sceneList.item(row, 0)
		self.selScene = str(item.text())

		# Update other Widgets
		if DEBUG:	self.updateToDo()




##############################################################################################
#
#
#		Interaction Helpers
#


	def switchFocus(self, orig, direction):
		filters = [self.listFilter, self.searchShot, self.listSeq, self.listArtist]
		for filterList in filters:
			if len(filterList.selectedItems()):
				currentFilterList = filterList
				break;


		lists = [self.listType, currentFilterList, self.tableAssets, self.listTasks, self.sceneList]


		if orig not in lists + filters:
			return False

		if orig in lists and direction in ["L", "R"]:
			n = lists.index(orig)

			if direction == "L":
				lists[n-1].setFocus()
			elif direction == "R":
				lists[(n+1) % len(lists)].setFocus()


		elif orig in filters and direction in ["UP", "DOWN"]:
			n = filters.index(orig)

			if direction == "UP":
				targetList = filters[n-1]
				targetList.setCurrentRow(targetList.count() - 1)
				targetList.setFocus()

			elif direction == "DOWN":
				targetList = filters[(n+1)%len(filters)]
				targetList.setCurrentRow(0)
				targetList.setFocus()



	def showHelp(self):
		ui.Help.showHelp()

	def showChangeLog(self):
		cl = ui.ChangeLog.ChangeLog()
		cl.setStyleSheet(style.STYLE)
		cl.label.setStyleSheet("background-color: " + SETTINGS["COLOR_LIST"])
		cl.exec_()


	def keyPressEvent(self, event):
		# Left Key
		if event.key() == QtCore.Qt.Key_Left:
			self.switchFocus(self.focusWidget(), "L")

		# Right or Tab Key
		elif event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Tab]:
			self.switchFocus(self.focusWidget(), "R")

		# Right or Tab Key
		elif event.key() == QtCore.Qt.Key_Up:
			self.switchFocus(self.focusWidget(), "UP")
		elif event.key() == QtCore.Qt.Key_Down:
			self.switchFocus(self.focusWidget(), "DOWN")


		# Enter
		elif event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
			self.sceneList.keyPressEnter()

		elif event.key() == QtCore.Qt.Key_F1:
			self.showHelp()

		elif event.key() == QtCore.Qt.Key_F2:
			self.showChangeLog()

		elif event.key() == QtCore.Qt.Key_F8:
			self.close()
			os.system("python2.7 " + sys.argv[0])

		elif event.key() == QtCore.Qt.Key_F12:
			if SETTINGS["isAdmin"]:
				self.stackLayout.setCurrentIndex(1 - self.stackLayout.currentIndex())


	def mouseMoveEvent(self, event):
		self.header.mouseMoveEvent(event)


##############################################################################################
#
#
#		Main
#
#
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	from ui import SplashScreen
	global SPLASH_SCREEN
	SPLASH_SCREEN = SplashScreen.SplashScreen()

	loadModules()

	window = vuSceneSelector()



	#window.show()
	app.exec_()