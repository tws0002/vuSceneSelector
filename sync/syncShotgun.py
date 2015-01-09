import os, sys

WORKING_DIR = os.path.dirname(__file__)
rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-1])

sys.path.append(rootDir)
sys.path.append(rootDir + "/sync/libs")
from shotgun_api3 import shotgun


sys.path.append("N:/060_Software/Kroetenlied_Pipeline/Kroetenlied")
import klAssets as Assets


from core import Index


# Shotgun Settings
SERVER_PATH = "http://ai.shotgunstudio.com"
SCRIPT_NAME = "test_Python"
SCRIPT_KEY = '1c87c13470d87c51c1a3275ddde9bfb9e9428bc345ed16772451b8df5c972deb'
PROJECT_FILTER = ['project','is',{'type':'Project','id':122}]
PROJECT_FILTER = ["project","is",{'type':'Project','id':112, 'name': 'Kroetenlied'}]

FIELDS_ASSET = ["code", "description", "sg_asset_group_1", "sg_asset_type"]
FIELDS_SHOTS = ["code", "description"]


os.environ["http_proxy"] = "http://quake:3128"
os.environ["https_proxy"] = "https://quake:3128"







# Mapping: LocalName -> Shotgun
mappingsLocal2ShotGun = {}

"""
mappingsLocal2ShotGun["Heros"] = "Hero Character"
mappingsLocal2ShotGun["Kinder"] = None
mappingsLocal2ShotGun["MusikKroeten"] = "MusikKroete"
mappingsLocal2ShotGun["SetPraxis_3D"] = "3D Praxis"
mappingsLocal2ShotGun["SetSumpf_3D"] = "3D Sumpf"
mappingsLocal2ShotGun["Set_Praxis_Photoscan"] = "Set-Bau Praxis"
mappingsLocal2ShotGun["Set_Sumpf_Photoscan"] = "Set-Bau Sumpf"
"""
mappingsLocal2ShotGun["GEO"] = "02_Model"
mappingsLocal2ShotGun["BS"] = None
mappingsLocal2ShotGun["TEX"] = "05_Textures"
mappingsLocal2ShotGun["RIG"] = "07_Rig"
mappingsLocal2ShotGun["COOKIE"] = "07_Rig-Blocking"
mappingsLocal2ShotGun["BND"] = None
mappingsLocal2ShotGun["SHD"] = "06_Shading"

"""
mappingsLocal2ShotGun["FOTOS"] = "Fotos"
mappingsLocal2ShotGun["MASKS"] = "Masks"
mappingsLocal2ShotGun["SCAN"] = "Photoscan"
mappingsLocal2ShotGun["PROXY"] = "Cleanup"
mappingsLocal2ShotGun["SHD"] = "06_Shading"
"""


mappingsLocal2ShotGun["ANIM"] = "Animation"
mappingsLocal2ShotGun["LIGHT"] = "Lighting"
mappingsLocal2ShotGun["COMP"] = "Compositing"



mappingsShotGun2Local = {}
for localName in mappingsLocal2ShotGun:
	sgName = mappingsLocal2ShotGun[localName]
	mappingsShotGun2Local[sgName] = localName






##########################
#
#	Setup & Helpers
#
#

def sg_connect():
	return shotgun.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy="quake:3128")



##########################
#
#	SetValues
#
#

'''
def setValue(name, attr, value):
	"""Set any Value"""
	Type = Index.getType(name)
	nameCol = "ShotNameVFX" if Type == "Shots" else "AssetName"

	spr_client = createService()

	# Find Sheet, than Cell than Udate
	sheetID = findSheet(spr_client, Type)
	if sheetID:
		row, col = findCell(spr_client, sheetID, name, nameCol, attr)
		if row and col:
			spr_client.UpdateCell(row, col, value, SPREADSHEET_KEY, sheetID)
			print "[Sync] Value succesfully updated!"
		else:
			print "[SyncError] Cell not found"
	else:
		print "[SyncError] SheetID not found"


'''

def getEntityID(sg, Type, name):
	filters = [["code", "is", name]]
	name = sg.find_one(Type ,filters)
	return name["id"] if name	else None


def getTaskID(sg, Type, shotName, taskName):
	shotID = getEntityID(sg, Type, shotName)

	filters = [['entity', 'is', {'type':Type, 'id':shotID}], ['content', 'is', taskName]]
	task = sg.find_one("Task", filters)
	return task["id"] if task else None


def setStatus(name, task, value):
	Type = Index.getType(name)

	if Type == "Asset":
		name = Index.getValue(name, "Num") + "_" + name

	sg = sg_connect()
	taskID = getTaskID(sg, Type, name, mappingsLocal2ShotGun[task])
	print "setStatus", name, task, value, taskID
	sg.update("Task", taskID, {"sg_status_list":value})


def setTodo(name, task, value):
	Type = Index.getType(name)

	sg = sg_connect()
	taskID = getTaskID(sg, Type, name, mappingsLocal2ShotGun[task])
	sg.update("Task", taskID, {"sg_description":value})


##########################
#
#	GetValues
#
#


def createAsset(asset):
	name = asset["code"].split("_")[-1]

	print "[SYNC-SHOTGUN] Load Assets", name

	Index.setValue(name, "Type",	"Asset", saveData=False)
	Index.setValue(name, "Group",	asset["sg_asset_group_1"], saveData=False)

	Index.setValue(name, "Code",		Assets.getCode(name), saveData=False)
	Index.setValue(name, "Num",			asset["code"].split("_")[0], saveData=False)
	Index.setValue(name, "Description",	asset["description"], saveData=False)
	return True


def createShot(shot):
	name = shot["code"].split("_")[-1]
	print "[SYNC-SHOTGUN] Load Shot", name


	Index.setValue(name, "Type",	"Shot", saveData=False)
	Index.setValue(name, "Group",	name[0], saveData=False)
	Index.setValue(name, "Code",	name, saveData=False)

	Index.setValue(name, "Num",			shot["code"][1:], saveData=False)
	Index.setValue(name, "Description",	shot["description"], saveData=False)
	return True


def loadAssets():
	sg = sg_connect()
	filters = [PROJECT_FILTER]

	print "[SYNC-SHOTGUN] Load Assets -- start --"
	for asset in sg.find("Asset", filters, FIELDS_ASSET):
		createAsset(asset)

	print "[SYNC-SHOTGUN] Load Shots -- start --"
	for shot in sg.find("Shot", filters, FIELDS_SHOTS):
		createShot(shot)



def loadTasks():
	''' Load All Tasks form ShotGun'''
	sg = sg_connect()

	tasks = sg.find("Task", [PROJECT_FILTER], ["content", "entity", "sg_status_list", "sg_description", "task_assignees"])

	for task in tasks:
		name = task["entity"]["name"].split("_")[-1]
		taskNameSG = task["content"]

		status	= task["sg_status_list"]
		descr	= task["sg_description"]
		artists	= [artist["name"] for artist in task["task_assignees"]]

		if taskNameSG in mappingsShotGun2Local:
			taskName = mappingsShotGun2Local[taskNameSG]
			Index.setValue(name, taskName + "_Todo", descr)
			Index.setValue(name, taskName + "_Status", status)
			Index.setValue(name, taskName + "_Artist", artists)



def load():
	Index.clear()
	loadAssets()

	loadTasks()

	Index.reWriteOverview()
	Index.save(Index.data)


if __name__ == '__main__':
	pass
	#load()
	#setStatus("Z910", "ANIM", "fin")
	setStatus("TestCharacter", "SHD", "ip")
	#setTodo("Z910", "ANIM", "Test123")

	#print ("Svobodan")

	#setValue("Z_90100", "ToDoCOMP", "Test123")
	#setValue("Adler", "ToDoRIG", "Test123")
	#loadAssets()
	#loadShots()
	#row2shot(None)