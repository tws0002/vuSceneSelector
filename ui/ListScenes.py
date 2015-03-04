from PyQt4 import QtCore, QtGui
import os
import datetime


# Import Modules
from core import Files, Settings
from ui import style, ListTemplate
SETTINGS = Settings.SETTINGS

FOLDER_ICONS = os.path.dirname(__file__).replace(os.sep, "/") + "/graphics/icons"

#################
#
#		Helpers


def createMayaDragAnDropScene(sceneFile):
	fileName = os.getenv("TMP") + "/TMP.ma"

	content = """requires maya "2014";
createNode transform -n "vuPipeline_Test";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".nts" -type "string" "%(sceneFile)s";""" % {"sceneFile":sceneFile.replace("\\", "/")}

	with open(fileName, 'w') as f:
		f.write(content)

	return fileName



def getFile_LastModify(path):
	time = os.path.getmtime(path)
	return datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M')


def fileSize_HumanReadable(bytes):
	for x in ['bytes','KB','MB','GB']:
		if bytes < 1024.0 and bytes > -1024.0:
			return "%3.1f %s" % (bytes, x)
		bytes /= 1024.0
	return "%3.1f %s" % (bytes, 'TB')


def getFile_FileSize(path):
	return fileSize_HumanReadable(os.path.getsize(path))


def createIcon(path):
	# Create Pixmap
	tex = QtGui.QPixmap(path)
	tex.fill(QtGui.QColor(155, 155, 155))
	tex.setAlphaChannel(QtGui.QPixmap(path))
	tex = tex.scaled(14, 14, 0, 1)

	# Create Icons
	icon = QtGui.QIcon(tex)
	return icon


def iconRefresh():
	return createIcon(FOLDER_ICONS + "/icon_refresh.png")

def iconOpenFolder():
	return createIcon(FOLDER_ICONS + "/icon_folder.png")



	#                       #
	#                       #
#################################
	#                       #
	#   TableHeaderClass    #
	#                       #
#################################
	#                       #
	#                       #

class TableScenesHeader(ListTemplate.TableTemplate):
	"""Seperate HeaderWidget, for easer use"""
	def __init__(self, window, table):
		super(TableScenesHeader, self).__init__(window)
		self.table = table

		self.setRowCount(1)
		self.setFixedHeight(14)
		self.setStyleSheet("border: 0px solid black")

		self.connect(self, QtCore.SIGNAL("cellClicked(int, int)"), self.cellClicked)
		self.connect(table, QtCore.SIGNAL("sortMe"), self.sortItems)

		# Adjust Size
		self.setColumnCount(3)



		widget = ListTemplate.HeaderItemSort("Scenes:")
		self.setCellWidget(0, 0, widget)
		widget.setStyleSheet(style.QLABEL_HOVER)
		widget = ListTemplate.HeaderItemSort("Date:")
		widget.setStyleSheet(style.styleTextGrey + style.QLABEL_HOVER)
		self.setCellWidget(0, 1, widget)
		widget = ListTemplate.HeaderItemSort("Size:")
		widget.setStyleSheet(style.styleTextGrey + style.QLABEL_HOVER)
		self.setCellWidget(0, 2, widget)

		self.resizeRows()

		# Fixed with, to easly match Header
		self.setColumnWidth(1, 117)
		self.setColumnWidth(2, 67)


	def sortItems(self):
		self.table.sortItems(self.table.sortColumn, self.table.sortOrder)

		for c in xrange(self.table.columnCount()):
			item = self.cellWidget(0, c)

			if c == self.table.sortColumn:
				item.toogle(self.table.sortOrder)
			else:
				item.toogle(None)



	def cellClicked(self, row, column):
		self.table.sortOrder = 1  - self.table.sortOrder
		self.table.sortColumn = column
		self.sortItems()






	#                       #
	#                       #
#################################
	#                       #
	#      TableClass       #
	#                       #
#################################
	#                       #
	#                       #

class TableScenes(ListTemplate.TableTemplate):
	def __init__(self, window):
		super(TableScenes, self).__init__(window)
		self.window = window
		self.sortMode = "Name"
		self.sortColumn = 0
		self.sortOrder = 1

		# Table Settings
		self.setColumnCount(3)
		self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

		# General Settings:
		self.setDragEnabled(True)
		#self.setMouseTracking(True)
		self.doDrag = False
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.mouseClickRight)
		self.connect(self, QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.mouseClickDouble)


	def refreshList(self, path):
		self.interactive = False
		self.clear()

		files = Files.findFiles(path)

		if not files:
			self.setRowCount(0)
			self.interactive = True
			return False

		# prePare Table
		self.setRowCount(len(files))


		# Sort them
		if self.sortMode == "Name":
			files.sort()
		elif self.sortMode == "Date":
			files.sort(key=lambda item: os.path.getmtime(path + "/" + item))
		elif self.sortMode == "Size":
			files.sort(key=lambda item: os.path.getsize(path + "/" + item))



		i = 0
		for fileItem in files:
			# Scene
			sceneItem = ListTemplate.TableItemTemplate(fileItem)
			sceneItem.setFlags(sceneItem.flags() ^ QtCore.Qt.ItemIsEditable)
			self.setItem(i, 0, sceneItem)

			# Date
			newItem = ListTemplate.TableItemTemplate(getFile_LastModify(path + "/" + fileItem))
			newItem.setFlags(sceneItem.flags() ^ QtCore.Qt.ItemIsEditable)
			newItem.setTextColor(QtGui.QColor(style.COLOR_TEXT_GREY))
			newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
			self.setItem(i, 1, newItem)

			# Size
			newItem = ListTemplate.TableItemTemplate(getFile_FileSize(path + "/" + fileItem))
			newItem.setFlags(sceneItem.flags() ^ QtCore.Qt.ItemIsEditable)
			newItem.setTextColor(QtGui.QColor(style.COLOR_TEXT_GREY))
			newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
			self.setItem(i, 2, newItem)
			i +=1

		self.resizeRows()
		#self.resizeColumns(auto=True)
		self.emit(QtCore.SIGNAL("sortMe"))

		# Fixed with, to easly match Header
		self.setColumnWidth(1, 120)
		self.setColumnWidth(2, 70)

		self.interactive = True
		return True



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
		self.refreshList(self.window.sceneFolder)


	def listCtxt_OpenFolder(self):
		if self.window.selScene:
			rtn = Files.listCtxt_ExploreFile(self.window.sceneFolder + "/" + self.window.selScene)
		else:
			print "Folder: " + self.window.sceneFolder
			rtn = Files.listCtxt_ExploreFolder(self.window.sceneFolder)


	def ctxtShowMenue(self, QPos):
		self.ctxtMenue= QtGui.QMenu()
		self.ctxtMenue.setStyleSheet(style.STYLE)

		# Refresh
		ctxt_refreshList = self.ctxtMenue.addAction(iconRefresh(), "Refresh List")
		ctxt_refreshList.setIconVisibleInMenu(True)
		ctxt_refreshList.setShortcut('F5')
		self.connect(ctxt_refreshList, QtCore.SIGNAL("triggered()"), self.listCtxt_Refresh)

		# Show in Folder
		ctxt_showFolder = self.ctxtMenue.addAction(iconOpenFolder(), "Show in Folder")
		ctxt_showFolder.setIconVisibleInMenu(True)
		self.connect(ctxt_showFolder, QtCore.SIGNAL("triggered()"), self.listCtxt_OpenFolder)

		parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))
		self.ctxtMenue.move(parentPosition + QPos)
		self.ctxtMenue.show()




	def openScene(self, row):
		item = self.item(row, 0)
		selScene = str(item.text())
		rtn = Files.openScene(self.window.sceneFolder + "/" + selScene)


##############################################################################################
#
#
#		Mouse Clicks
#

	def mouseClickRight(self, QPos):
		self.ctxtShowMenue(QPos)

	def keyPressEnter(self):
		self.openScene(self.currentRow())

	def mouseClickDouble(self, row, col):
		self.openScene(row)


##############################################################################################
#
#
#		Mouse Drag
#


	def mouseMoveEvent(self, event):
		if not self.rowCount():
			return event.ignore()


		# Hover Effect
		row = self.row(self.itemAt(event.pos()))
		for r in range(self.rowCount()):
			for c in range(self.columnCount()):
				if r == row:
					self.item(r, c).setBackground(QtGui.QBrush(QtGui .QColor(style.COLOR_SELECTION)))
				else:
					self.item(r, c).setBackground(QtGui.QBrush(QtGui .QColor(style.COLOR_LIST)))


		# Update Data
		sceneFile = self.window.sceneFolder + "/" + self.window.selScene

		SETTINGS["OpenScene"] = sceneFile
		SETTINGS.save()

		# PrePare MineData
		data = QtCore.QMimeData()

		ext = os.path.splitext(sceneFile)[1]
		if ext == ".nk":
			url = QtCore.QUrl.fromLocalFile(sceneFile)
		elif ext == ".ma" or ext == ".mb":
			url = QtCore.QUrl.fromLocalFile(createMayaDragAnDropScene(sceneFile))
		else:
			err = "[Error] Unsupported FileType for DragAndDrop"
			return

		# Set Data
		data.setUrls([url])

		# Set Drag
		drag = QtGui.QDrag(self)
		drag.setMimeData(data)
		drag.exec_(QtCore.Qt.MoveAction)



	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_F5:
			self.refreshList(self.window.sceneFolder)
		else:
			super(TableScenes, self).keyPressEvent(event)



