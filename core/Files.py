import os

from core import Settings
SETTINGS = Settings.SETTINGS


#FILE_BLACKLIST = [".nk~", ".autosave"]
FILE_WHITELIST = []
FILE_WHITELIST += [".sni"]				# Tracking
FILE_WHITELIST += [".lxo"]				# Modo
FILE_WHITELIST += [".mud", ".mra", ".psd"]	# Texturing
FILE_WHITELIST += [".hip", ".hipnc"]	# Houdni
FILE_WHITELIST += [".ma", ".mb"]		# Maya
FILE_WHITELIST += [".scn"]				# Softimage
FILE_WHITELIST += [".nk"]				# Nuke
FILE_WHITELIST += [".psz"]				# Nuke


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
		print "ERROR: No Path"
		return results

	if not os.path.exists(path):
		print "ERROR: Path doesnt exist"
		return

	if SETTINGS["scanSubFolders"]:
		for root, dirs, files in os.walk(path):
			for sceneFile in files:
				if os.path.splitext(sceneFile)[1] in FILE_WHITELIST:
					results.append((root + "/")[len(path)+1:] + sceneFile)


	else:
		for sceneFile in os.listdir(path):
			if os.path.isfile(path + "\\" + sceneFile):
				if os.path.splitext(sceneFile)[1] in FILE_WHITELIST:
					results.append(sceneFile)
	return sorted(results, reverse=True)



def openScene(path):
	ext = os.path.splitext(path)[1]

	print "[Core] openScenePath: " + path
	if ext == ".mb" or ext == ".ma":
		os.system(SETTINGS["MAYA_BATCH"] + " " + path)
		return "Open MayaScene: " + path

	if ext == ".nk":
		os.system(SETTINGS["NUKE_BATCH"] + " " + path)
		return "Open NukeScene: " + path

	if ext == ".mud":
		os.system(path)
		return "Open MudboxScene: " + path

	if ext == ".hipnc":
		os.system(SETTINGS["HOUDINI_BATCH"] + " " + path)
		return "Open HoudiniScene: " + path

	return "[ERROR] Dont know how to handle this file. Plase RightClick and select 'Show in Folder'"


def listCtxt_ExploreFile(path):
	if not os.path.exists(path):
		err = "[ERROR] File does not exists: " + path
		print err
		return err
	os.system("explorer /select," + path.replace("/", "\\"))


def listCtxt_ExploreFolder(path):
	if not os.path.exists(path):
		err = "[ERROR] Path does not exists: " + path
		print err
		return err
	os.system("explorer /e /select," + path.replace("/", "\\") + "\\")