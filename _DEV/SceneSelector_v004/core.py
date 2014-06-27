import os
from SceneSelector import utils


##############################################################################################
#
#
#		Settings
#

MAYA_BATCH = "//bigfoot/kroetenlied/060_Software/vuPipeline/startMaya.bat"



def findFiles(path):
	results = []

	if not path:
		return results

	if not os.path.exists(path):
		return

	for sceneFile in os.listdir(path):
		if os.path.isfile(path + "\\" + sceneFile):
			results.append(sceneFile)

	return sorted(results, reverse=True)


def openScene_Maya(path):
	utils.log("OpenMaya: " + path)
	os.system(MAYA_BATCH + " " + path)


def listCtxt_ExploreFile(path):
	utils.log("ExploreFile: " + path)
	os.system("explorer /select," + path.replace("/", "\\"))


def listCtxt_ExploreFolder(path):
	utils.log("ExploreFolder: " + path)
	os.system("explorer /root," + path.replace("/", "\\"))