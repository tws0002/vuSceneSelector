import os
import shutil
from SceneSelector_v010 import utils


##############################################################################################
#
#
#		Settings
#

PROJECT_ROOT = "//bigfoot/kroetenlied"
PIPELINE_FOLDER = PROJECT_ROOT + "/060_Software/vuPipeline"

MAYA_BATCH = PIPELINE_FOLDER + "/startMaya.bat"
PATH_SETTINGS_USER = PIPELINE_FOLDER + "/PythonModules/SceneSelector/userSettings/" + utils.getArtist(short=False)
EMPTY_SCENE = "//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/SceneSelector/emptyScene.mb"

def checkFiles(path):
	if not os.path.exists(path):
		return False

	for sceneFile in os.listdir(path):
		if os.path.isfile(path + "\\" + sceneFile):
			return True
	return False

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


def listCtxt_CreateNewFile(path):
	shutil.copy2(EMPTY_SCENE, path)



#########################
#						#
#       SaveData        #
#						#
#########################
def storeData(values):
	# Make it more UserFriendly
	content = str(values).replace(",", ",\n")

	f = open(PATH_SETTINGS_USER, 'w')
	f.writelines(content)
	f.close()


def loadData(view, rtnDict=False):
	if not os.path.isfile(PATH_SETTINGS_USER):
		return False

	content = eval(open(PATH_SETTINGS_USER, 'r').read())

	if rtnDict:
		return content
	else:
		view.values = content
		return True




