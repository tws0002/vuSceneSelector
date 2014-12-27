from PyQt4 import QtCore, QtGui
import os, sys

# Import Modules
from core import Settings, Index
from ui import style, ListTemplate
from sync import syncTasks
SETTINGS = Settings.SETTINGS

FOLDER_ICONS = os.path.dirname(__file__) + "/graphics/icons"




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
			HEADER_ICONS[task]["white"] = tex





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

		for status in SETTINGS["STATI"]:
			if status == "" and not SETTINGS["isAdmin"]:
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
		self.ctxtShowMenue(event.globalPos ())









class TableAssets(ListTemplate.TableTemplate, QtGui.QTableWidget):
	def __init__(self, window):
		super(TableAssets, self).__init__(window)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.parent = window


		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.mouseClickRight)

		createTaskIcons()


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


	def addRows(self, names, parent, selType):
		"""Add a Row, with one TextItem and Icons for the Tasks"""
		self.clear()

		# Get Tasks for TaskIcons
		tasks = Index.getTasks(selType)
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
				self.setCellWidget(i, j+1, TableAssetsIcon(self, item, task, parent, selType))

		self.resizeRows()
		return True


	def addNames(self, selType, selGrp=""):
		"""Get desired Names"""
		if selType == "":
			return

		self.interactive = False

		# Get Items
		if selGrp == "-- All --":
			names = Index.getNames(selType)
		elif selGrp == "-- Favorites --":
			names = [name for name in Index.getNames(selType) if name in SETTINGS["Favorites"]]
		else:
			Filter = [("VFX", "in", "Tags")]
			names = Index.getNames(selType, selGrp, Filter)

		# Add them!
		self.addRows(names, self.parent, selType)
		self.interactive = True



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


	def ctxt_openFolder(self):
		path = self.parent.sceneFolder
		if not os.path.exists(path):
			print "Path gibts nicht"
			return False
		else:
			os.system("explorer /e /select," + path.replace("/", "\\") + "\\")
			return True


	def mouseClickRight(self, pos):

		# Show Context Menue
		self.ctxtMenue = QtGui.QMenu()
		self.ctxtMenue.setStyleSheet(style.STYLE)

		ctxt_openFolder = self.ctxtMenue.addAction(folderIcon(), "Open Folder")
		ctxt_openFolder.setIconVisibleInMenu(True)
		self.connect(ctxt_openFolder, QtCore.SIGNAL("triggered()"), self.ctxt_openFolder)

		if self.parent.selName in SETTINGS["Favorites"]:
			ctxt_FravoritesRem = self.ctxtMenue.addAction(favIcon_ctxtFull(), "Remove from Favorites")
			ctxt_FravoritesRem.setIconVisibleInMenu(True)
			self.connect(ctxt_FravoritesRem, QtCore.SIGNAL("triggered()"), self.ctxt_FavoritesRem)
		else:
			ctxt_FravoritesAdd = self.ctxtMenue.addAction(favIcon_ctxtFull(), "Add to Favorites")
			ctxt_FravoritesAdd.setIconVisibleInMenu(True)
			self.connect(ctxt_FravoritesAdd, QtCore.SIGNAL("triggered()"), self.ctxt_FavoritesAdd)




		self.ctxtMenue.exec_(self.mapToGlobal(pos) + QtCore.QPoint(5,5))









class TableHeaderIcon(QtGui.QLabel):
	def __init__(self, task):
		super(TableHeaderIcon, self).__init__()

		self.task = task

		self.setText("")
		self.addIcon()
		#self.setToolTip(self.shot + "_" + self.task)

	def addIcon(self, status=None):
		"Set IconImage depending on the Text in that Cell"
		icon = HEADER_ICONS[self.task]["white"]
		self.setPixmap(icon)
		return True


class TableAssetsHeader(ListTemplate.TableTemplate, QtGui.QTableWidget):
	"""Seperate HeaderWidget, for easer use"""
	def __init__(self, window, table):
		super(TableAssetsHeader, self).__init__(window)
		self.table = table

		createHeaderIcons()


		self.setRowCount(1)
		self.setFixedHeight(14)
		self.setStyleSheet("border: 0px solid black")

		self.connect(self, QtCore.SIGNAL("cellClicked(int, int)"), self.cellClicked)

		# Adjust Size
		self.setColumnCount(1)

		#for i in range(self.columnCount()):
		#	self.setColumnWidth(i+1, 16+2)




		# Name
		"""
		for taskName in range(task):
			widget = QtGui.QLabel(str(i))
			self.setCellWidget(0, i, widget)
		"""


	def setType(self, selType):
		widget = QtGui.QLabel(selType)


		# Label
		self.setCellWidget(0, 0, widget)

		# Tasks:
		tasks = Index.getTasks(selType)
		tasks = [task for task in tasks if task not in SETTINGS["TASKS_WITHOUT_ICON"]]


		self.setColumnCount(len(tasks) + 1)
		# Adjust Size
		for i in range(self.columnCount()):
			self.setColumnWidth(i+1, 16+2)

		# Task Icons
		for i, task in enumerate(tasks):
			self.setCellWidget(0, i+1, TableHeaderIcon(task))

		self.resizeRows()



	def cellClicked(self, row, column):
		print "cellClicked", row, column
		self.table.sortOrder = 1  - self.table.sortOrder
		self.table.sortItems(column, self.table.sortOrder)










class WidgetAssets(QtGui.QWidget):
	def __init__(self, window):
		super(WidgetAssets, self).__init__()
		self.window = window


		# Items
		self.table = TableAssets(self.window)
		self.table.addNames("Shots", "A")
		self.tableHeader = TableAssetsHeader(self.window, self.table)
		self.tableHeader.setType("Shots")

		# Layout
		vBox = QtGui.QVBoxLayout()

		vBox.addWidget(self.tableHeader)
		vBox.addWidget(self.table)
		self.layout = vBox
		self.setLayout(vBox)




if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	w = WidgetAssets(None)
	w.setStyleSheet(style.STYLE)
	w.show()
	app.exec_()