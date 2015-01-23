from PyQt4 import QtCore, QtGui
import os, sys

# Import Modules
from core import Settings, Index
from ui import style, ListTemplate
from sync import syncTasks
SETTINGS = Settings.SETTINGS

FOLDER_ICONS = os.path.dirname(__file__).replace(os.sep, "/") + "/graphics/icons"
RV_EXE = "C:\\Program Files\\Tweak\\RV\\bin\\rv.exe"



def iconFromFile(filePath, size, color):
	tex = QtGui.QPixmap(filePath)
	tex.fill(color)
	tex.setAlphaChannel(QtGui.QPixmap(filePath))
	tex = tex.scaled(size, size, 0, 1)
	return tex


def favIcon():
	color = QtGui.QColor(204, 204, 204)
	tex = iconFromFile(FOLDER_ICONS + "/icon_favorite.png", 12, color)
	return QtGui.QIcon(tex)

def favIcon_ctxtFull():
	color = QtGui.QColor(155, 155, 155)
	tex = iconFromFile(FOLDER_ICONS + "/icon_favorite.png", 12, color)
	return QtGui.QIcon(tex)

def folderIcon():
	color = QtGui.QColor(155, 155, 155)
	tex = iconFromFile(FOLDER_ICONS + "/icon_folder.png", 12, color)
	return QtGui.QIcon(tex)

def iconRV():
	color = QtGui.QColor(155, 155, 155)
	tex = iconFromFile(FOLDER_ICONS + "/icon_rvPlayer.png", 12, color)
	return QtGui.QIcon(tex)


TASK_ICONS = {}
def createTaskIcons():
	global TASK_ICONS

	for Type in Index.getTypes():
		for task in Index.getTasks(Type):
			IMG = FOLDER_ICONS + "/task_" + task.upper() + ".png"

			if not os.path.isfile(IMG):
				#print "IMG not found: " + IMG
				IMG = FOLDER_ICONS + "/default.png"

			TASK_ICONS[task] = {}
			for status in SETTINGS["STATI"]:
				color = QtGui.QColor(status["color"])

				# Apply Color
				tex = iconFromFile(IMG, 14, color)
				TASK_ICONS[task][status["value"]] = tex


HEADER_ICONS = {}
def createHeaderIcons():
	global HEADER_ICONS

	for Type in Index.getTypes():
		for task in Index.getTasks(Type):
			IMG = FOLDER_ICONS + "/task_" + task.upper() + ".png"

			if not os.path.isfile(IMG):
				IMG = FOLDER_ICONS + "/default.png"

			HEADER_ICONS[task] = {}

			color = QtGui.QColor(SETTINGS["COLOR_TEXT_GREY"])
			tex = iconFromFile(IMG, 14, color)
			HEADER_ICONS[task]["grey"] = tex

			color = QtGui.QColor(SETTINGS["COLOR_ICON_YELLOW"])
			tex = iconFromFile(IMG, 14, color)
			HEADER_ICONS[task]["active"] = tex




class TableAssetsIcon(QtGui.QLabel):
	def __init__(self, table, shot, task, widget, Type):
		super(TableAssetsIcon, self).__init__()

		self.Type = Type
		self.shot = shot
		self.task = task
		self.parent = table
		self.widget = widget

		tmpStatus = Index.getValue(self.shot, self.task + "_Status")
		self.status = tmpStatus if tmpStatus else ""

		self.setText(self.status)
		self.addIcon()
		self.setToolTip(self.shot + "_" + self.task)


	def applyText(self):
		self.setText(self.status)
		Index.setValue(self.shot, self.task + "_Status", self.status)
		syncTasks.addTask(self.shot, self.task + "_Status", self.status)


	def getIcon(self, status=None):
		if status == None:
			status = self.status
		if status == "":
			status = SETTINGS["STATI"][0]["value"]
		return TASK_ICONS[self.task][status]


	def addIcon(self, status=None):
		"Set IconImage depending on the Text in that Cell"
		self.setPixmap(self.getIcon(status))
		return True


	def toogle(self):
		self.applyText()
		self.addIcon()


	def getToogleFunction(self, value):
		""""dynamicly create ToggleFuntion"""
		def toogleFunction():
			self.status = value
			self.toogle()
		return toogleFunction


	def ctxtShowMenue(self, QPos):
		if not SETTINGS["isAdmin"] and self.status == "":
			"""nonAdmins are not allowed to activate inactive Tasks"""
			self.setStyleSheet(self.origStyle)
			return


		self.ctxtMenue= QtGui.QMenu()
		self.ctxtMenue.setStyleSheet(style.STYLE)


		ctxt_headline = self.ctxtMenue.addAction(self.shot + "_" + self.task)
		ctxt_headline.setEnabled(False)
		ctxt_headline.hover = None
		self.ctxtMenue.addSeparator()

		for status in SETTINGS["STATI"]:

			if not SETTINGS["isAdmin"]:
				print status
				if status["value"] in ["", "1"]:
					continue

			ctxt_toogle = self.ctxtMenue.addAction(QtGui.QIcon(self.getIcon(status["value"])), status["label"])
			ctxt_toogle.setIconVisibleInMenu(True)
			self.connect(ctxt_toogle, QtCore.SIGNAL("triggered()"), self.getToogleFunction(status["value"]))

		self.ctxtMenue.exec_(QPos + QtCore.QPoint(5,5))
		self.setStyleSheet(self.origStyle)


	def mousePressEvent(self, event):
		self.widget.selName = self.shot
		self.origStyle = self.styleSheet()
		self.setStyleSheet("background-color: " + style.COLOR_SELECTION)
		self.ctxtShowMenue(event.globalPos())









class TableAssets(ListTemplate.TableTemplate, QtGui.QTableWidget):
	def __init__(self, window):
		super(TableAssets, self).__init__(window)

		self.parent = window
		self.names = []

		# Selection
		self.selType = ""
		self.selGroup = ""
		self.selArtist = ""

		# Filters
		self.FilterTasks = {}


		createTaskIcons()

		#self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		#self.verticalScrollBar().setStyleSheet("width: 0px")

		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.mouseClickRight)


	def resizeEvent(self, event):
		super(TableAssets, self).resizeEvent(event)
		self.emit(QtCore.SIGNAL("resizeSignal()"))

	"""
		if self.scrollIndicator:
			self.scrollIndicator.setVisible(self.verticalScrollBarVisible)
		if self.verticalScrollBarVisible:
			self.setStyleSheet("background-color: red")
		else:
			self.setStyleSheet("background-color: green")
	"""

	def FavoriteSet(self, item, value):
		if value:
			font = QtGui.QFont()
			font.setBold(True)
			icon = favIcon()
		else:
			font = QtGui.QFont()
			font.setBold(False)
			icon = QtGui.QIcon()

		item.setFont(font)
		item.setIcon(icon)


	def addRows(self, names, parent):
		"""Add a Row, with one TextItem and Icons for the Tasks"""
		self.clear()

		# Get Tasks for TaskIcons
		tasks = Index.getTasks(self.selType)
		tasks = [task for task in tasks if task not in SETTINGS["TASKS_WITHOUT_ICON"]]

		# Adjust Size
		self.setRowCount(len(names))
		self.setColumnCount(len(tasks) + 1)
		for i in range(self.columnCount()):
			self.setColumnWidth(i+1, 16+2)

		# Add Shots + Icons
		for i, item in enumerate(names):

			# Name
			newitem = QtGui.QTableWidgetItem(item)
			newitem.setFlags(newitem.flags() ^ QtCore.Qt.ItemIsEditable)
			self.setItem(i, 0, newitem)
			#self.setCellWidget(i, 0, newitem)

			if item in SETTINGS["Favorites"]:
				self.FavoriteSet(newitem, True)


			newitem.setToolTip(Index.getValue(item, "Description"))

			# Task Icons
			for j, task in enumerate(tasks):
				self.setCellWidget(i, j+1, TableAssetsIcon(self, item, task, parent, self.selType))

		self.resizeRows()
		return True

	"""
	def Filter(self):
		Filter = []

		for taskName in self.FilterTasks:
			print "FilterTasks", taskName

		if self.Type == "Shots":
			Filter += [("VFX", "in", "Tags")]

		return Filter
	"""

	def update(self):
		# Get Names
		if self.selType == "":
			return
		names = Index.getNames(self.selType)

		# Filter Names
		if self.selType == "Shots":
			names = [name for name in names if "VFX" in Index.getValue(name, "Tags") or name.endswith("MASTER")]

		if self.filterType == "global":
			# Global Filters
			if self.selGroup == "-- Favorites --":
				names = [name for name in names if name in SETTINGS["Favorites"]]

		elif self.filterType == "group":
			names = [name for name in names if self.selGroup == Index.getValue(name, "Group")]

		elif self.filterType == "artist":
			names = [name for name in names if self.selGroup in Index.getArtists(filterShot=name)]


		for taskName, value in self.FilterTasks.iteritems():
			if value:
				names = [name for name in names if Index.getValue(name, taskName + "_Status")]


		# Add them!
		self.interactive = False
		self.addRows(names, self.parent)
		self.resizeEvent(None)
		self.interactive = True


	def addNames(self, selType, selGroup="", filterType="global"):
		"""Get desired Names"""
		self.selType = selType
		self.filterType = filterType
		self.selGroup = selGroup

		self.update()


	######################
	######################
	##					##
	##					##
	##	Context Menue 	##
	##					##
	##					##
	######################
	######################


	def ctxt_FavoritesAdd(self):
		item = self.currentItem()
		self.FavoriteSet(item, True)

		# Save Setings:
		SETTINGS["Favorites"] = SETTINGS["Favorites"] + [self.parent.selName]


	def ctxt_FavoritesRem(self):
		item = self.currentItem()
		self.FavoriteSet(item, False)

		# Save Setings:
		favorites = SETTINGS["Favorites"]
		newFavs = []
		for fav in favorites:
			if fav != self.parent.selName:
				newFavs.append(fav)
		SETTINGS["Favorites"] = newFavs


	def getFootageFolder(self):
		return SETTINGS["FootageFolder"] % {"NAME": self.parent.selName}


	def ctxt_openFootageFolder(self):
		path = self.getFootageFolder()

		# Get Ueberfolder:
		path = "/".join(path.split("/")[:-1])

		os.system("explorer /e /select," + path.replace("/", "\\") + "\\")
		return True


	def ctxt_openFootageRV(self):
		path = self.getFootageFolder()
		os.system('start "" "' + RV_EXE + '" ' + path)
		return True


	def mouseClickRight(self, pos):

		# Show Context Menue
		self.ctxtMenue = QtGui.QMenu()
		self.ctxtMenue.setStyleSheet(style.STYLE)


		if self.parent.selName in SETTINGS["Favorites"]:
			ctxt_FravoritesRem = self.ctxtMenue.addAction(favIcon_ctxtFull(), "Remove from Favorites")
			ctxt_FravoritesRem.setIconVisibleInMenu(True)
			self.connect(ctxt_FravoritesRem, QtCore.SIGNAL("triggered()"), self.ctxt_FavoritesRem)
		else:
			ctxt_FravoritesAdd = self.ctxtMenue.addAction(favIcon_ctxtFull(), "Add to Favorites")
			ctxt_FravoritesAdd.setIconVisibleInMenu(True)
			self.connect(ctxt_FravoritesAdd, QtCore.SIGNAL("triggered()"), self.ctxt_FavoritesAdd)


		if SETTINGS["showOpenFootage"] and os.path.isdir(self.getFootageFolder()):
			self.ctxtMenue.addSeparator()

			# Open Footage Folder
			ctxt_openFootageFolder = self.ctxtMenue.addAction(folderIcon(), "open Footage Folder")
			ctxt_openFootageFolder.setIconVisibleInMenu(True)
			self.connect(ctxt_openFootageFolder, QtCore.SIGNAL("triggered()"), self.ctxt_openFootageFolder)

			# Open Footage RV
			ctxt_openFootageRV = self.ctxtMenue.addAction(iconRV(), "open Footage RV")
			ctxt_openFootageRV.setIconVisibleInMenu(True)
			self.connect(ctxt_openFootageRV, QtCore.SIGNAL("triggered()"), self.ctxt_openFootageRV)


		self.ctxtMenue.exec_(self.mapToGlobal(pos) + QtCore.QPoint(5,5))









class TableHeaderIcon(QtGui.QLabel):
	def __init__(self, task):
		super(TableHeaderIcon, self).__init__()

		self.task = task
		self.active = False
		self.icon = None
		self.setCursor(QtCore.Qt.PointingHandCursor)

		self.setText("")
		self.addIcon()


	def update(self):
		self.setPixmap(self.icon)

	def enterEvent(self, event):
		icon = HEADER_ICONS[self.task]["active"]
		self.setPixmap(icon)


	def leaveEvent(self, event):
		self.update()


	def addIcon(self, status=None):
		"Set IconImage depending on the Text in that Cell"

		if self.active:
			self.icon = HEADER_ICONS[self.task]["active"]
			return True
		else:
			self.icon = HEADER_ICONS[self.task]["grey"]

		self.update()
		return True



	def toogle(self):
		self.active = not self.active
		self.addIcon()



class TableAssetsHeader(ListTemplate.TableTemplate, QtGui.QTableWidget):
	"""Seperate HeaderWidget, for easer use"""
	def __init__(self, window, table):
		super(TableAssetsHeader, self).__init__(window)
		self.table = table
		self.tasks = []

		createHeaderIcons()

		# Adjust Size/Style
		self.setRowCount(1)
		self.setColumnCount(1)
		self.setFixedHeight(14)
		self.setStyleSheet("border: 0px solid black")

		self.cellClicked.connect(self.cellClicked_User)

		# ScrolBar Handling
		self.connect(self.table, QtCore.SIGNAL("resizeSignal()"), self.resize)
		self.verticalScrollBar().setVisible(False)



	def resize(self):
		if self.table.verticalScrollBarVisible:
			self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		else:
			self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


	def cellClicked_User(self, row, col):
		if col:
			# Task-Icon
			item = self.cellWidget(row, col)
			item.toogle()

			self.table.FilterTasks[item.task] = item.active
			self.table.update()

		else:
			# Clicked on Label --> Sorting
			self.table.sortOrder = 1  - self.table.sortOrder
			self.table.sortItems(col, self.table.sortOrder)

			item = self.cellWidget(row, col)
			item.toogle(self.table.sortOrder)


	def setType(self, selType):
		#widget = QtGui.QLabel(selType)
		widget = ListTemplate.HeaderItemSort(selType)
		widget.setToolTip("Click to Sort")

		# Label
		self.setCellWidget(0, 0, widget)

		# Tasks:
		tasks = Index.getTasks(selType)
		tasks = [task for task in tasks if task not in SETTINGS["TASKS_WITHOUT_ICON"]]
		self.table.FilterTasks = {task:False for task in tasks}

		self.setColumnCount(len(tasks) + 1)

		# Task Icons
		for i, task in enumerate(tasks):
			# Adjust Size
			self.setColumnWidth(i+1, 16+2)
			# Add Widgets
			self.setCellWidget(0, i+1, TableHeaderIcon(task))

		self.resizeRows()





if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	w = WidgetAssets(None)
	w.setStyleSheet(style.STYLE)
	w.show()
	app.exec_()