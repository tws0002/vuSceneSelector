import os
import shutil
import utils
from settings import project



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


def openScene(path):
	"""	This will start the Appliaction and opens the Scene	"""
	ext = os.path.splitext(path)[1]

	if ext == ".nk":
		os.system(project.NUKE_BATCH + " " + path)
	elif ext == ".ma" or ext == ".mb":
		os.system(project.MAYA_BATCH + " " + path)



def listCtxt_ExploreFile(path):
	utils.log("ExploreFile: " + path)
	os.system("explorer /select," + path.replace("/", "\\"))


def listCtxt_ExploreFolder(path):
	utils.log("ExploreFolder: " + path)
	os.system("explorer /root," + path.replace("/", "\\"))


def listCtxt_CreateNewFile(path):
	shutil.copy2(project.EMPTY_SCENE, path)


#########################
#						#
#       SaveData        #
#						#
#########################
def storeData(values):
	# Make it more UserFriendly
	content = str(values).replace(",", ",\n")

	f = open(project.USER_SETTINGS, 'w')
	f.writelines(content)
	f.close()


def loadData(view, rtnDict=False):
	if not os.path.isfile(project.USER_SETTINGS):
		return False

	content = eval(open(project.USER_SETTINGS, 'r').read())

	if rtnDict:
		return content
	else:
		view.values = content
		return True