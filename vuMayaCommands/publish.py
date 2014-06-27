import maya.cmds as cmds
import klAssetNames, VersionControl, vuPipelineHelpers

##############################################################################################
#
#
#		Settings
#

root = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules"
LOG_FILE = root + "/logFiles/logPublish"


##############################################################################################
#
#
#		Main
#

def publishAsset():
	# Import Modules
	import shutil

	# Get SceneName and Root
	fullName = cmds.file(sceneName=True, q=True)
	paths = fullName.split("/")

	taskName = paths[-2].split("_")[2]
	assetCode = paths[-2].split("_")[1]
	assetName = klAssetNames.getName(assetCode)
	sceneType = fullName.split(".")[-1]

	outFolder =  "/".join(paths[:-1]) + "/" + assetCode + "_" + taskName + "_OUT"
	outName = assetName + "_" + taskName

	cmds.file( save=True, type="mayaAscii" if sceneType == "ma" else "mayaBinary")								# Save File
	shutil.copy2(fullName, outFolder + "/" + outName + "." + sceneType)		# Copy File to MASTER
	cmds.warning("[Kroentlied Pipeline] Published !")

	# Copy File to BackUp
	oldFolder = outFolder + "/" + assetCode + "_" + taskName + "_OUT_OLD"
	backup = VersionControl.getLatest(oldFolder, 1)

	if not backup:	# No Backup found yet
	    backup = outName + "_BackUp_v001." + sceneType

	shutil.copy2(fullName, oldFolder + "/" + backup)
	print "[Kroentlied Pipeline] PublishBackup: " + backup


	msg = "Published: " + outName + "." + sceneType + "\n"
	msg += "\n"
	msg += "BackUped as: " + backup
	vuPipelineHelpers.log(LOG_FILE, "Published: " + outName + "  ||   BackUp: " + backup + "   ||   OrigScene: " + fullName.split("/")[-1] + "   ||   Folder: " + outFolder)
	cmds.confirmDialog(title="Asset Published", message=msg, button="Close")
	return