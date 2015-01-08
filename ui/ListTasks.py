from PyQt4 import QtCore, QtGui
import os
import scandir

if __name__ == '__main__':
	import sys
	rootDir = os.sep.join(__file__.split(os.sep)[:-2])
	sys.path.append(rootDir)

# Import Modules
from core import Settings, Index
from ui import style, ListTemplate
SETTINGS = Settings.SETTINGS


FILTER_EXTENSIONS = (".exr", ".jpg", ".tif")
FILTER_FOLDER = ["asses", "logs", "main_logs"]
RV_EXE = "C:\\Program Files\\Tweak\\RV\\bin\\rv.exe"

FOLDER_ICONS = os.path.dirname(__file__).replace(os.sep, "/") + "/graphics/icons"


#############################
#
#	Context Menue Helpers
#
#

def createIcon(path):
	size = 12
	color = QtGui.QColor(155, 155, 155)

	tex = QtGui.QPixmap(path)
	tex.fill(color)
	tex.setAlphaChannel(QtGui.QPixmap(path))
	tex = tex.scaled(size, size, 0, 1)
	return QtGui.QIcon(tex)


def addAction_OpenRV(menu, name, path):
	def clicked():
		#print "Open RV" + path
		os.system('start "" "' + RV_EXE + '" ' + path)

	icon = createIcon(FOLDER_ICONS + "/icon_rvPlayer.png")

	action = menu.addAction(icon, name)
	action.setIconVisibleInMenu(True)
	action.connect(action, QtCore.SIGNAL("triggered()"), clicked)


def addAction_OpenFolder(submenu, fileName, filePath):
	def clicked():
		os.system("explorer /e /select, " + filePath.replace("/", "\\"))

	icon = createIcon(FOLDER_ICONS + "/icon_folder.png")
	action = submenu.addAction(icon, fileName)	#"Open Folder: " +
	action.setIconVisibleInMenu(True)
	action.connect(action, QtCore.SIGNAL("triggered()"), clicked)


#############################
#
#	Version Search
#
#

def getFolder_OUT(Type, name, task):
	Vars = {}
	Vars["TASK_NUM"] = Index.getTaskNum(task)
	Vars["TASK_NAME"] = task
	Vars["NUM"] = Index.getValue(name, "Num")
	Vars["NAME"] = name
	Vars["CODE"] = Index.getValue(name, "Code")
	path = SETTINGS[Type + "_FolderOUT"] % Vars
	return path


def getSequences(path, menu):
	foundSomething = False
	items = []
	if os.path.isdir(path):
		for fileItem in sorted(scandir.scandir(path), key=lambda x: x.name , reverse=True):
			foundSomething = True
			fileName  = fileItem.name
			filePath  = path + "/" + fileName

			if fileItem.is_dir(): # and self.folderFilter(fileName):
				items.append(fileItem)


		for fileItem in items:
			fileName = fileItem.name
			submenu = menu.addMenu(fileName)

			addAction_OpenRV(submenu, fileName, filePath)
			addAction_OpenFolder(submenu, fileName, filePath)
			submenu.addSeparator()


			for subFileItem in scandir.scandir(filePath):
				if subFileItem.is_dir() and subFileItem.name.lower() not in FILTER_FOLDER:
					subFileName = subFileItem.name
					addAction_OpenRV(submenu, subFileName, filePath + "/" + subFileName)
	else:
		print "Fould not found", path
	return foundSomething








def iconFromFile(filePath, size, color):
	tex = QtGui.QPixmap(filePath)
	tex.fill(color)
	tex.setAlphaChannel(QtGui.QPixmap(filePath))
	tex = tex.scaled(size, size, 0, 1)
	return tex

def createHeaderIcons():
	Icons = {}
	for Type in Index.getTypes():
		for task in Index.getTasks(Type):
			IMG = FOLDER_ICONS + "/task_" + task.upper() + ".png"

			if not os.path.isfile(IMG):
				IMG = FOLDER_ICONS + "/default.png"

			Icons[task] = {}

			color = QtGui.QColor(SETTINGS["COLOR_TEXT_GREY"])
			tex = iconFromFile(IMG, 14, color)
			Icons[task]["white"] = tex

	return Icons



#############################
#
#	Task-List
#
#

class ListTasks(ListTemplate.ListTemplate):
	def __init__(self, parent):
		super(ListTasks, self).__init__()
		self.parent = parent

		if SETTINGS["showIconsInTaskList"]:
			self.Icons = createHeaderIcons()


	def setItems(self, items):
		super(self.__class__, self).setItems(items)

		if SETTINGS["showIconsInTaskList"]:
			for item in [self.item(i) for i in xrange(self.count())]:
				name = str(item.text())
				icon = self.Icons[name]["white"]

				item.setIcon(QtGui.QIcon(icon))



	def contextMenuEvent(self, event):
		# Get Vars
		shot = self.parent.selName
		task = self.parent.selTask
		Type = self.parent.selType

		menu = QtGui.QMenu()
		menu.setStyleSheet(style.STYLE)

		path = getFolder_OUT(Type, shot, task)

		sequences = getSequences(path, menu)
		if not sequences:
			menu.addAction("no Versions found")
		menu.exec_(event.globalPos())



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	menu = QtGui.QMenu()

	path = "/ln/Jagon/050_Shots/060_COMP/Z_90100_COMP/Z_90100_COMP_OUT"
	getSequences(path, menu)