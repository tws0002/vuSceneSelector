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
TASKS_WITH_SUBFOLDERS = ["3D", "SIM", "LIGHT"]
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


def addAction_OpenRV(menu, name, path, folder=False):

	if folder:
		fullPath = path
	else:
		# Get First ImageFile in Folder
		fullPath = None
		for fileItem in scandir.scandir(path):
			if fileItem.is_file():
				base, ext = os.path.splitext(fileItem.name)
				if ext in FILTER_EXTENSIONS:
					fullPath = path + "/" + fileItem.name
					break;
		# Exit if there was no Image
		if not fullPath:
			return


	def clicked():
		print "Open RV: ", fullPath
		os.system('start "" "' + RV_EXE + '" ' + fullPath)

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

	# EXEPTION-Start
	if SETTINGS["projectName"] == "Kroetenlied" and task == "ANIM":
		path = path.replace("_OUT", "_PLAYBLAST")
	# EXEPTION-End

	return path


def getSequences(path, menu, task="", asSubMenu=True):
	foundSomething = False
	items = []
	if os.path.isdir(path):
		for fileItem in sorted(scandir.scandir(path), key=lambda x: x.name , reverse=True):
			foundSomething = True
			fileName  = fileItem.name

			if fileItem.is_dir(): # and self.folderFilter(fileName):
				items.append(fileItem)


		for fileItem in items:
			# Get Vars
			fileName = fileItem.name
			filePath  = path + "/" + fileName
			subFolders = []

			# Search for SubFolders:
			for subFileItem in scandir.scandir(filePath):
				if subFileItem.is_dir():
					subFolders.append(subFileItem)


			if len(subFolders):
				submenu = menu.addMenu(fileName)
				for subFileItem in sorted(subFolders, key=lambda x: x.name , reverse=True):
					subFileName = subFileItem.name
					addAction_OpenRV(submenu, subFileName, filePath + "/" + subFileName, folder=True)

			elif QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
				submenu = menu.addMenu(fileName)
				addAction_OpenRV(submenu, fileName, filePath)
				addAction_OpenFolder(submenu, fileName, filePath)
			else:
				addAction_OpenRV(menu, fileName, filePath)


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
		sequences = getSequences(path, menu, task=task, asSubMenu=False) #SETTINGS["taskList_showOpenFolder"])
		if not sequences:
			menu.addAction("no Versions found")

		menu.addSeparator()
		if task == "COMP":
			path = self.parent.sceneFolder + "/prerender"
			submenue_preRender = menu.addMenu("preRenders")
			getSequences(path, submenue_preRender, False)

		# Open Work
		addAction_OpenFolder(menu, "Open: " + task + "_WORK", self.parent.sceneFolder)
		addAction_OpenFolder(menu, "Open: " + task + "_OUT", getFolder_OUT(Type, shot, task))

		menu.exec_(event.globalPos())



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	menu = QtGui.QMenu()

	path = "/ln/Jagon/050_Shots/060_COMP/Z_90100_COMP/Z_90100_COMP_OUT"
	getSequences(path, menu)