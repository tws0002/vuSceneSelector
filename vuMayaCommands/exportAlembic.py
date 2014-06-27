import maya.cmds as cmds
from datetime import datetime

import klAssetNames
##############################################################################################
#
#
#		Settings
#

HEADER_PATH = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/vuMayaCommands/exportAlembic_Header_v001.jpg"
LOG_FILE = "//bigfoot/kroetenlied/_User/Vincent/Pipeline/LogFile_AlembicExport.log"


def formatTime(inSec):
	minutes, seconds = divmod(inSec,60)
	return str(int(minutes)) + " min " + str(int(seconds)) + " sec"


##############################################################################################
#
#
#		Core
#

def buildJob(assetName, folder, shotCode):

    # Get GeoNames for Export
    objNames = cmds.ls("*:" + assetName + "_GEO:*", g=True, l=True)
    objList = []
    for name in objNames:
        parent = cmds.listRelatives(name, p=True)[0]
        if not parent in objList:
            objList.append(parent)
    exportNames = ",".join(objList)


    # Get Variables
    #objNames = ",".join(cmds.ls(sl=True))
    #objNames = "Kroete_BND_OUT:Kroete_GEO:m_kroeteBody_geo"

    # Contruct Job-String
    job = ""

    # Time
    job += "in=" + str(cmds.playbackOptions(q=True,min=True)) + ";"
    job += "out=" + str(cmds.playbackOptions(q=True,max=True)) + ";"
    job += "step=1;"
    job += "substep=2;"

    # Objs and FilePath
    job += "filename=" + folder + "\\" + shotCode + "_" + assetName + ".abc" + ";"
    job += "objects=" + exportNames + ";"

    # Options
    job += "globalspace=1;"
    job += "withouthierarchy=1;"
    job += "purepointcache=0;"
    job += "ogawa=0;"
    job += "uvs=0;"
    job += "normals=0;"
    job += "facesets=0;"
    job += "useInitShadGrp=0;"
    job += "dynamictopology=0;"
    job += "transformcache=0;"

    return job


##############################################################################################
#
#
#		Window
#

class AlembicExportWindow():
	def __init__(self):

		nameSpaces = cmds.namespaceInfo(lon=True)

		self.Characters = []
		for nameSpace in nameSpaces:
			assetName = nameSpace.split("_")[0]
			if assetName in klAssetNames.AssetNames:
				self.Characters.append(assetName)


		self.window = cmds.window(
						title="Krotenlied-Pipeline: Alembic Export",
						sizeable = False,
						minimizeButton = False,
						maximizeButton = False)

		# Header
		cmds.columnLayout(parent=self.window)
		cmds.image(image = HEADER_PATH)
		cmds.separator(h=5, vis=True, st='none')

		mainLayout = cmds.rowColumnLayout(parent=self.window, numberOfColumns=1)


		# Check Boxes
		cmds.frameLayout("Characters", collapsable=False, w=198, p=mainLayout)
		cmds.rowColumnLayout(numberOfColumns=2)
		self.checkBoxes = []
		for char in self.Characters:
			cmds.separator(w=40, st=None, vis=True)
			checkBox = cmds.checkBox(label=char, changeCommand=self.checkCheckBoxes, value=True)

			self.checkBoxes.append(checkBox)


		# Button
		cmds.separator(h=20, vis=True, st='none', p=mainLayout)
		self.buttonExport = cmds.button(h=30, w=100, label="Export Selected", command=self.btnExport, p=mainLayout)

		self.checkCheckBoxes()
		cmds.showWindow()


	def checkCheckBoxes(self, *args):
		for checkBox in self.checkBoxes:
			if cmds.checkBox(checkBox, q=True, v=True):
				cmds.button(self.buttonExport, e=True, enable=True)
				return True

		cmds.button(self.buttonExport, e=True, enable=False)
		return False


	def btnExport(self, *args):
		# Collect Variables:
		paths = str(cmds.file(sceneName=True, q=True)).split("/")[:-1]
		shotCode = paths[-1].split("_")[0]
		folder = "/".join(paths) + "/" + shotCode + "_ANIM_CACHE"

		# Build Jobs
		msg = "Exported AlembicCaches for:\n"
		jobs = []
		for i, charName in enumerate(self.Characters):
			if cmds.checkBox(self.checkBoxes[i], q=True, v=True):
				msg += charName + "\n"
				jobs.append(buildJob(charName, folder, shotCode))


		# Export
		timeA = datetime.now()
		cmds.ExocortexAlembic_export(j= jobs)
		timeB = datetime.now()

		# Confirm Dialog
		msg += "\nExportTime: " + formatTime((timeB - timeA).total_seconds())
		cmds.confirmDialog(title="I'am done", message=msg, button="Close")
		cmds.deleteUI(self.window, window=True)