from PyQt4 import QtCore, QtGui
import os # for getcwd()
import sys
import datetime


rootDir = os.sep.join(__file__.split(os.sep)[:-2])
sys.path.append(rootDir)


from AdminUtils import vuFolderCreator
from core import Settings, Index

SETTINGS = Settings.SETTINGS
if SETTINGS["syncMode"] == "Google":
	from sync import syncGoogle as syncModule


##############################################################################################
#
#
#		PyQt-Stuff
#
class debugPage(QtGui.QWidget):
	def __init__(self, parent=None):
		super(debugPage, self).__init__(parent)

		#########################
		#						#
		#        Header         #
		#						#
		#########################
		main_grid = QtGui.QGridLayout()



		googleWidget = self.createInterface_SyncGoogle()
		main_grid.addWidget(googleWidget, 1, 0)

		folderCreator = vuFolderCreator.vuFolderCreator()
		main_grid.addWidget(folderCreator, 2, 0)


		spacerGrid = QtGui.QGridLayout()
		spacerGrid.addLayout(main_grid, 0, 0)
		spacerGrid.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding), 1, 1)

		self.setLayout(spacerGrid)


	def createInterface_SyncGoogle(self):

		# Create Widgets
		googleDocs_ButtonLoad = QtGui.QPushButton('Load', self)
		googleDocs_ButtonSave = QtGui.QPushButton('Save', self)

		googleDocs_ButtonLoad.setToolTip("Load from Google")
		googleDocs_ButtonSave.setToolTip("Save to Google")

		googleDocs_ButtonLoad.clicked.connect(self.googleDocs_ButtonLoad_clicked)
		googleDocs_ButtonSave.clicked.connect(self.googleDocs_ButtonSave_clicked)

		self.googleDocs_lastSync = QtGui.QLabel("Last Sync: 01.01.1875")
		self.googleDocs_lastSync.setAlignment(QtCore.Qt.AlignRight)

		# Layout
		googleBox = QtGui.QGridLayout()
		googleBox.addWidget(googleDocs_ButtonLoad, 0, 0)
		googleBox.addWidget(googleDocs_ButtonSave, 0, 1)
		googleBox.addWidget(self.googleDocs_lastSync, 2, 0, 1, 2)

		googleGrp = QtGui.QGroupBox("SyncGoogle")
		googleGrp.setLayout(googleBox)
		self.googleDocs_UpdateLastSync()

		return googleGrp


	def googleDocs_UpdateLastSync(self):
		Index.load()
		self.googleDocs_lastSync.setText("LastSync: " + Index.data["Overview"]["lastSync"])

	def googleDocs_ButtonSave_clicked(self):
		print "Google Save"

	def googleDocs_ButtonLoad_clicked(self):
		syncModule.load()

		# Set LastSync
		time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
		Index.load()
		Index.data["Overview"]["lastSync"] = time
		Index.save(Index.data)
		self.googleDocs_UpdateLastSync()


##############################################################################################
#
#
#		Main
#
#
if __name__ == "__main__":
	Index.load()
	Index.data["Overview"]["lastSync"] = "Test"
	Index.save(Index.data)
	"""
	app = QtGui.QApplication(sys.argv)
	page = debugPage()
	page.show()
	app.exec_()
	"""
