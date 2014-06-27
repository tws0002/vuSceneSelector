import maya.cmds as cmds

def test():

	# Get Paths
	fullPath = str(cmds.file(sceneName=True, q=True))
	rootFolder = "/".join(fullPath.split("/")[:-1])

	# Get SceneName-Parts
	sceneName = fullPath.split("/")[-1]
	assetName = sceneName.split("_")[0]
	taskName = sceneName.split("_")[1]
	artist = sceneName.split("_")[3]
	sceneType = sceneName.split(".")[-1]

	print "assetName: " + assetName
	print "taskName: " + taskName
	print "artist: " + artist
	print "sceneType: " + sceneType