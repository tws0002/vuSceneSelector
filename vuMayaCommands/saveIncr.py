import maya.cmds as cmds


import VersionControl, vuPipelineHelpers, mayaUtils


##############################################################################################
#
#
#		Settings
#

root = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules"
LOG_FILE = root + "/logFiles/logSaveIncr"
HEADER_PATH = root + "/vuMayaCommands/saveIncr_Header_v001.jpg"

##############################################################################################
#
#
#		Window
#

class SaveIncrWindow():
	def __init__(self):

		# Collect Variables: Paths
		fullPath = str(cmds.file(sceneName=True, q=True))
		self.rootFolder = "/".join(fullPath.split("/")[:-1])

		# Collect Variables: SceneName-Parts
		try:
			sceneName = fullPath.split("/")[-1]
			self.assetName = sceneName.split("_")[0]
			self.taskName = sceneName.split("_")[1]
			self.artist = vuPipelineHelpers.getArtist()
			self.sceneType = sceneName.split(".")[-1]
		except:
			mayaUtils.errorWindow_NamingConvention()
			return

		self.version = "v" + ("000" + str(VersionControl.getLatest(self.rootFolder, up=1, getNum=True)))[-3:]

		self.window = cmds.window("klPipeline_SaveIncr", title="Krotenlied-Pipeline: SaveScene+1", sizeable=False)

		# Header
		cmds.columnLayout(parent=self.window)
		cmds.image(image = HEADER_PATH)
		cmds.separator(h=5, vis=True, st='none')

		cmds.rowColumnLayout(parent=self.window, numberOfColumns=6)

		# Labels
		cmds.text( al="left", w=75, label='Name')
		cmds.text( al="left", w=50, label='Task')
		cmds.text( al="left", w=50, label='Version' )
		cmds.text( al="left", w=40, label='Artist')
		cmds.text( al="left", w=200, label='Comment')
		cmds.text( al="left", w=25, label='')

		# TextFields
		cmds.textField(ed=False, w=75, tx=self.assetName)
		cmds.textField(ed=False, w=50, tx=self.taskName)
		cmds.textField(ed=False, w=50, tx=self.version)
		cmds.textField(ed=False, w=40, tx=self.artist)
		self.textComment = cmds.textField(w=200, enterCommand=self.btnSave)
		cmds.textField(ed=False, w=25, tx="." + self.sceneType)

		# Button
		cmds.rowColumnLayout(parent=self.window, numberOfColumns=2)

		cmds.separator(w=300, h=20, vis=True, st='none')
		cmds.separator(st='none')
		cmds.separator(st='none')
		cmds.button(h=30, w=100, label='Save+1', command=self.btnSave)

		cmds.showWindow()
		cmds.setFocus(self.textComment)


	def btnSave(self, arg):
		comment = cmds.textField(self.textComment, tx=True, q=True)

		fileName = self.assetName + "_" + self.taskName + "_" + self.version + "_" + self.artist
		fileName += "_" + comment if comment else ""
		fileName += "." + self.sceneType
		print "Save as: " +  fileName
		vuPipelineHelpers.log(LOG_FILE, fileName + " || Path: " + self.rootFolder)

		cmds.file( rename=self.rootFolder + "/" + fileName)
		cmds.file( save=True, type="mayaAscii" if self.sceneType == "ma" else "mayaBinary")

		# Eval Deferred, becouse of pyQT/pySide eval-order issues
		cmds.evalDeferred('cmds.deleteUI("klPipeline_SaveIncr")')


##############################################################################################
#
#
#		Main
#

def saveIncr():
	SaveIncrWindow()