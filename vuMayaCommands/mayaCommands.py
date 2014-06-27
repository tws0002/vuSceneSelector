import maya.cmds as cmds
import getpass
#from vuPipeline import *	#versionControl
import vuPipeline
reload(vuPipeline)



class SaveIncrWindow():
	def __init__(self):
		# Settings:
		bgColor = [0.5, 0.5, 0.5]
		headerPath = "//bigfoot/kroetenlied/060_Software/maya_plugins/vuPipeline/ToolHeaders/mayaSaveIncr_v001.jpg"


		# Collect Variables
		fullName = cmds.file(sceneName=True, q=True)
		paths = fullName.split("/")
		assetCode = paths[-2].split("_")[1]

		self.rootFolder = "/".join(paths[:-1])
		self.taskName = paths[-2].split("_")[2]
		self.assetName = vuPipeline.assetNames.getFullName(assetCode)
		self.artist = getpass.getuser()[:2]
		self.version = "v" + ("000" + str(vuPipeline.versionControl.getLatest(self.rootFolder, up=1, getNum=True)))[-3:]

		self.window = cmds.window(title="Krotenlied-Pipeline: SaveScene+1")

		# Header
		cmds.columnLayout(parent=self.window)
		cmds.image(image = headerPath)
		cmds.separator(h=5, vis=True, st='none')

		cmds.rowColumnLayout(parent=self.window, numberOfColumns=6)

		# Labels
		cmds.text( al="left", w=75, label='Name')
		cmds.text( al="left", w=50, label='Task')
		cmds.text( al="left", w=50, label='Version' )
		cmds.text( al="left", w=50, label='Artist')
		cmds.text( al="left", w=200, label='Comment')
		cmds.text( al="left", w=25, label='')

		# TextFields
		cmds.textField(ed=False, w=75, tx=self.assetName)
		cmds.textField(ed=False, w=50, tx=self.taskName)
		cmds.textField(ed=False, w=50, tx=self.version)
		cmds.textField(ed=False, w=50, tx=self.artist)
		self.textComment = cmds.textField(w=200)
		cmds.textField(ed=False, w=25, tx=".ma")

		# Button
		cmds.rowColumnLayout(parent=self.window, numberOfColumns=2)

		cmds.separator(w=300, h=20, vis=True, st='none')
		cmds.separator(st='none')
		cmds.separator(st='none')
		cmds.button(h=30, w=100, label='Save+1', command=self.btnSave)

		cmds.showWindow()


	def btnSave(self, *args):
		comment = cmds.textField(self.textComment, tx=True, q=True)

		fileName = self.assetName + "_" + self.taskName + "_" + self.version + "_" + self.artist
		fileName += "_" + comment if comment else ""
		fileName += ".ma"
		print "Save as: " +  fileName

		cmds.file( rename=self.rootFolder + "/" + fileName)
		cmds.file( save=True, type='mayaAscii')
		cmds.deleteUI(self.window, window=True)


def saveIncr():
	SaveIncrWindow()


def publish():
	# Import Modules
	import shutil

	# Get SceneName and Root
	fullName = cmds.file(sceneName=True, q=True)
	paths = fullName.split("/")

	taskName = paths[-2].split("_")[2]
	assetCode = paths[-2].split("_")[1]
	assetName = vuPipeline.assetNames.getFullName(assetCode)

	outFolder =  "/".join(paths[:-1]) + "/" + assetCode + "_" + taskName + "_OUT"
	outName = assetName + "_" + taskName

	cmds.file( save=True, type='mayaAscii' )					# Save File
	shutil.copy2(fullName, outFolder + "/" + outName + ".ma")	# Copy File to MASTER
	cmds.warning("[Kroentlied Pipeline] Published !")

	# Copy File to BackUp
	oldFolder = outFolder + "/" + assetCode + "_" + taskName + "_OUT_OLD"
	backup = vuPipeline.versionControl.getLatest(oldFolder, 1)

	if not backup:	# No Backup found yet
	    backup = outName + "_BackUp_v001.ma"

	shutil.copy2(fullName, oldFolder + "/" + backup)
	print "[Kroentlied Pipeline] PublishBackup: " + backup
	return




def activateSceneDragAndDrop():
    sceneFile = r""
    print ("-"*10 + "\n") * 10
    cmds.file(sceneFile, o=True, f=True)

cmds.scriptJob(ct=["readingFile", test], runOnce=True))