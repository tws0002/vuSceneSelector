from PyQt4 import QtCore, QtGui
import os, sys
import webbrowser


# Import Modules
if __name__ == '__main__':
	root_dir = os.sep.join(__file__.split(os.sep)[:-2])
	sys.path.append(root_dir)
from ui import style


FOLDER_GRAPHICS = os.path.dirname(__file__) + "/graphics"


IMG_NAMINGCONVENTION_ASSETS = "V:/090_Software/Assets/InfoGraphics/NamingConvention_v003_vu_InfoGraphicAssets.png"
IMG_NAMINGCONVENTION_SHOTS = "V:/090_Software/Assets/InfoGraphics/NamingConvention_v003_vu_InfoGraphicShots.png"


URL_SCENESELECTOR_ROOT			= "https://www.filmakademie.de/wiki/display/AISPD/vuSceneSelector"
URL_SCENESELECTOR_STEPBYSTEP	= URL_SCENESELECTOR_ROOT + "#vusceneselector-stepbystep"
URL_SCENESELECTOR_TIPPS			= URL_SCENESELECTOR_ROOT + "#vusceneselector-tipps"
URL_SCENESELECTOR_DOCU			= URL_SCENESELECTOR_ROOT + "#vusceneselector-docu"
URL_SCENESELECTOR_FAQ			= URL_SCENESELECTOR_ROOT + "#vusceneselector-faq"


URL_BUGREPORT = "http://issues.animationsinstitut.de/projects/vusceneselector/issues/new"


"""
class HelpPage(QtGui.QDialog):
	def __init__(self, widget=None):
		super(HelpPage, self).__init__(widget)

		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setStyleSheet(style.STYLE)
		self.setWindowTitle("vuSceneSelector Help")
		self.setWindowIcon(QtGui.QIcon(FOLDER_GRAPHICS + "/elements/icon_Help.png"))

		# Intro Text
		uiText_Info = QtGui.QLabel("Bei Problemen oder Anregungen,\nvereinbaren sie bitte vorab telefonisch einen Beratungstermin\noder kommen zu unseren Sprechzeiten in A1.06 vorbei.\nWir freuen uns auf ihren Besuch.")


		# General Stuff
		uiBtn_NamingConventionAssets = QtGui.QPushButton("Naming Convention:\nAssets")
		uiBtn_NamingConventionShots = QtGui.QPushButton("Naming Convention:\nShots")
		uiBtn_FolderStruckture = QtGui.QPushButton("Folder Strutkure")
		uiBtn_WorkflowOutputs = QtGui.QPushButton("Workflow: OutPuts")
		uiBtn_NamingConventionAssets.clicked.connect(self.uiBtn_NamingConventionAssets_clicked)
		uiBtn_NamingConventionShots.clicked.connect(self.uiBtn_NamingConventionShots_clicked)
		uiBtn_FolderStruckture.clicked.connect(self.uiBtn_FolderStruckture_clicked)
		uiBtn_WorkflowOutputs.clicked.connect(self.uiBtn_WorkflowOutputs_clicked)

		layoutGeneral = QtGui.QHBoxLayout()
		layoutGeneral.addWidget(uiBtn_NamingConventionAssets)
		layoutGeneral.addWidget(uiBtn_NamingConventionShots)
		layoutGeneral.addWidget(uiBtn_FolderStruckture)
		layoutGeneral.addWidget(uiBtn_WorkflowOutputs)
		grpGeneral = QtGui.QGroupBox("General Pipeline Info:")
		grpGeneral.setLayout(layoutGeneral)



		# vuSceneSelector
		uiBtn_sceneSelectorStepByStep = QtGui.QPushButton("Step by Step\nTutorial")
		uiBtn_sceneSelectorLogos = QtGui.QPushButton("Icons\nWTF?")

		uiBtn_sceneSelectorStepByStep.clicked.connect(self.uiBtn_vuSceneSelectorStepByStep_clicked)
		uiBtn_sceneSelectorLogos.clicked.connect(self.uiBtn_vuSceneSelectorLogos_clicked)

		layoutSceneSelector = QtGui.QHBoxLayout()
		layoutSceneSelector.addWidget(uiBtn_sceneSelectorStepByStep)
		layoutSceneSelector.addWidget(uiBtn_sceneSelectorLogos)
		grpSceneSelector = QtGui.QGroupBox("about vuSceneSelector:")
		grpSceneSelector.setLayout(layoutSceneSelector)



		# DDC: Nuke
		uiBtn_nukeJWrite = QtGui.QPushButton("jWrite")
		layoutNuke = QtGui.QHBoxLayout()
		layoutNuke.addWidget(uiBtn_nukeJWrite)
		grpNuke = QtGui.QGroupBox("DCC-Tools: Nuke")
		grpNuke.setLayout(layoutNuke)

		# Layout
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(uiText_Info)
		mainLayout.addWidget(grpGeneral)
		mainLayout.addWidget(grpSceneSelector)
		mainLayout.addWidget(grpNuke)
		self.setLayout(mainLayout)


	def show_PopupImage(self, path):
		image = QtGui.QLabel()
		image.setPixmap(QtGui.QPixmap(path))

		layout = QtGui.QHBoxLayout()
		layout.addWidget(image)

		popup = QtGui.QDialog(self)
		popup.setLayout(layout)

		popup.setStyleSheet(style.STYLE)
		popup.setWindowTitle("vuSceneSelector Help")
		popup.setWindowIcon(QtGui.QIcon(FOLDER_GRAPHICS + "/elements/icon_Help.png"))

		popup.exec_()



	def show_PopupLogos(self):
		layout = QtGui.QVBoxLayout()


		for selType in ["Assets", "Shots"]:
			tasks = project.Tasks.getTasks(selType)

			taskLayout = QtGui.QGridLayout()

			for i, task in enumerate(tasks):

				# Create Icon
				IMG = project.GRAPHICS + "/Icons/" + task.lower() + ".png"

				if not os.path.isfile(IMG):
					IMG = project.GRAPHICS + "/Icons/default.png"

				tex = QtGui.QPixmap(16, 16)
				#tex.fill(QtGui.QColor(128, 128, 128))
				tex.fill(QtGui.QColor(155, 155, 155))
				tex.setAlphaChannel(QtGui.QPixmap(IMG))
				#tex = tex.scaled(14, 14, 0, 1)
				label = QtGui.QLabel()
				label.setPixmap(tex)
				label.setFixedSize(16, 16)

				taskLayout.addWidget(label, i , 0)
				taskLayout.addWidget(QtGui.QLabel(task), i , 1)

			grpTask = QtGui.QGroupBox(selType + ":")
			grpTask.setLayout(taskLayout)
			layout.addWidget(grpTask)




		popup = QtGui.QDialog()
		popup.setLayout(layout)

		popup.setStyleSheet(style.STYLE)
		popup.setWindowTitle("vuSceneSelector Help")
		popup.setWindowIcon(QtGui.QIcon(FOLDER_GRAPHICS + "/elements/icon_Help.png"))
		popup.exec_()




	# User Interaction
	def uiBtn_NamingConventionAssets_clicked(self):
		self.show_PopupImage(IMG_NAMINGCONVENTION_ASSETS)

	def uiBtn_NamingConventionShots_clicked(self):
		self.show_PopupImage(IMG_NAMINGCONVENTION_SHOTS)

	def uiBtn_FolderStruckture_clicked(self):
		print "uiBtn_FolderStruckture_clicked"

	def uiBtn_WorkflowOutputs_clicked(self):
		print "uiBtn_WorkflowOutputs_clicked"


	def uiBtn_vuSceneSelectorStepByStep_clicked(self):
		self.show_WebSite(URL_SCENESELECTOR_STEPBYSTEP)

	def uiBtn_vuSceneSelectorLogos_clicked(self):
		reload(style)
		self.show_PopupLogos()




def showHelp(widget):
	dialog = HelpPage(widget)
	dialog.exec_()
"""


def show_WebSite(url):
	webbrowser.open(url,new=2)


def openMenu(event=None):
	ctxtMenue= QtGui.QMenu()
	ctxtMenue.setSeparatorsCollapsible(True)
	ctxtMenue.setStyleSheet(style.STYLE)

	#action = ctxtMenue.addAction("Quick Help")

	action = ctxtMenue.addAction("WikiPage")
	action.connect(action, QtCore.SIGNAL("triggered()"), lambda: show_WebSite(URL_SCENESELECTOR_ROOT))
	action.setShortcut('F1')

	ctxtMenue.addSeparator()

	action = ctxtMenue.addAction("BugReport")
	action.connect(action, QtCore.SIGNAL("triggered()"), lambda: show_WebSite(URL_BUGREPORT))
	action.setShortcut('Strg+Alt+Del+F4+L')




	ctxtMenue.exec_(event.globalPos())


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	window = HelpPage()
	window.show()
	app.exec_()







# To Add:
#
"""
General:
- Naming Convention
- Folder Strukture
- Output Workflow

vuSceneSelector:
- Was die Logos bedeuten
- Basic Usage:
	- Step by Step: selecting Scenes, wie komme ich zum Shot, was tun wnen fertig, wie starten
	- Drag And Drop

Nuke:
"""