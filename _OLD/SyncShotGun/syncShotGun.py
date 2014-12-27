import sys
sys.path.append("D:/Vincent/Dropbox/btSyncFolders/Dev/017_KroetenliedPipeline/v04/v04_08/")
from vuPipelineOverview.SyncShotGun.shotgun_api3 import shotgun


sys.path.append("N:/060_Software/Kroetenlied_Pipeline")
from Kroetenlied import Index


import os

# Shotgun Settings
SERVER_PATH = "http://ai.shotgunstudio.com"
SCRIPT_NAME = "test_Python"
SCRIPT_KEY = '1c87c13470d87c51c1a3275ddde9bfb9e9428bc345ed16772451b8df5c972deb'
os.environ["http_proxy"] = "http://quake:3128"
os.environ["https_proxy"] = "https://quake:3128"


projectID = 112
prjKroetenlied = {'type': 'Project', 'id': 112, 'name': 'Kroetenlied'}



# Mapping: LocalName -> Shotgun
mappingsLocal2ShotGun = {}
mappingsLocal2ShotGun["Heros"] = "Hero Character"
mappingsLocal2ShotGun["Kinder"] = None
mappingsLocal2ShotGun["MusikKroeten"] = "MusikKroete"
mappingsLocal2ShotGun["SetPraxis_3D"] = "3D Praxis"
mappingsLocal2ShotGun["SetSumpf_3D"] = "3D Sumpf"
mappingsLocal2ShotGun["Set_Praxis_Photoscan"] = "Set-Bau Praxis"
mappingsLocal2ShotGun["Set_Sumpf_Photoscan"] = "Set-Bau Sumpf"

mappingsLocal2ShotGun["GEO"] = "02_Model"
mappingsLocal2ShotGun["BS"] = None
mappingsLocal2ShotGun["TEX"] = "05_Textures"
mappingsLocal2ShotGun["RIG"] = "07_Rig"
mappingsLocal2ShotGun["COOKIE"] = "07_Rig-Blocking"
mappingsLocal2ShotGun["BND"] = None
mappingsLocal2ShotGun["SHD"] = "06_Shading"

mappingsLocal2ShotGun["FOTOS"] = "Fotos"
mappingsLocal2ShotGun["MASKS"] = "Masks"
mappingsLocal2ShotGun["SCAN"] = "Photoscan"
mappingsLocal2ShotGun["PROXY"] = "Cleanup"
mappingsLocal2ShotGun["SHD"] = "06_Shading"

mappingsShotGun2Local = {}
for localName in mappingsLocal2ShotGun:
	sgName = mappingsLocal2ShotGun[localName]
	mappingsShotGun2Local[sgName] = localName




##############################
#
#
#		Conncection
#
#

SG = None
def sg_connect():
	global SG
	if not SG:
		SG = shotgun.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy="quake:3128")
	return SG



##############################
#
#
#		Get Values
#
#

def getAssetID(assetName):
	'''Get AssetID by AssetName'''
	filters = [["code", "is", assetName]]
	asset = SG.find_one("Asset" ,filters)
	return asset["id"] if asset	else None


def getAssetTaskID(assetId, taskName):
	filters = [['entity', 'is', {'type':'Asset', 'id':assetId}], ['content', 'is', taskName]]
	task = SG.find_one("Task", filters)
	return task["id"] if task else None


"""
def getAssetsAll():
	'''Get all Assets'''
	assets = sg.find("Asset", [["project", "is", prjKroetenlied]], ["code", "sg_asset_group_1"])
	return assets
"""

def loadTaskStatus():
	''' Load All Tasks form ShotGun'''
	sg = sg_connect()

	tasks = sg.find("Task", [["project", "is", prjKroetenlied]], ["content", "entity", "sg_status_list"])
	for task in tasks:
		name = task["entity"]["name"].split("_")[1]
		taskNameSG = task["content"]
		status = task["sg_status_list"]

		if taskNameSG in mappingsShotGun2Local:
			taskName = mappingsShotGun2Local[taskNameSG]
			Type = Index.getType(name)
			print Type, name, taskName, status
			Index.setValue(Type, name, "status" + taskName, status)
	Index.save()



##############################
#
#
#		Set Values
#
#


def setAssetStatus(name, column, value):
	sg_connect()

	# Get Correct Names
	name = Index.getValue("Assets", name, "Num") + "_" + name
	name = "900_TestCharacter" # DEBUG LOCK!
	column = mappingsLocal2ShotGun[column]

	# Find ID-Values
	assetID = getAssetID(name)
	taskID  = getAssetTaskID(assetID, column)

	# Set Values
	SG.update("Task", taskID, {"sg_status_list":value})


def setStatus(Type, name, task, value):
	if Type == "Assets":
		setAssetStatus(name, task, value)


def setTodo(Type, name, task, value):
	print "setTodo: Done"


##############################
#
#
#		Set Values
#
#

def load():
	print "[SyncShotgun] Start loading Data..."
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"

	loadTaskStatus()
	#print "SG Load"


def save():
	print "[SyncShotgun] Start saving Data..."
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"


if __name__ == "__main__":
	load()
	pass