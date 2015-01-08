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




"""
def createService():
	# TODO: Only at FilmAK
	if sys.platform.startswith("win"):
		os.environ["http_proxy"] = "http://quake:3128"
		os.environ["https_proxy"] = "https://quake:3128"

	spr_client = gdata.spreadsheet.service.SpreadsheetsService()
	spr_client.email = 'vuPipelineFilmakademie@gmail.com'
	spr_client.password = 'filmaka2014'
	spr_client.ProgrammaticLogin()
	return spr_client


def findSheet(spr_client, Type):
	sheets = spr_client.GetWorksheetsFeed(SPREADSHEET_KEY)
	for sheet in sheets.entry:
		if sheet.title.text == Type:
			return sheet.id.text.split("/")[-1]
	return None


def findCell(spr_client, sheetID, name, nameCol, column):
	titles = {}
	tarRow, tarCol = None, None

	cells = spr_client.GetCellsFeed(SPREADSHEET_KEY, sheetID).entry
	for cell in cells:
		col = cell.cell.col
		row = cell.cell.row
		val = cell.cell.text

		if row == "1":
			# Store Title/ColNum-Dict
			titles[val] = col

			# Find TargetColNum
			if val == column:
				tarCol = col

		else:
			# Find Target RowNum
			if col == titles[nameCol] and val == name:
				tarRow = row


		if tarCol and tarRow:
			print "CellFound: ", tarCol, tarRow
			return (tarRow, tarCol)
	return False, False
"""

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

def setStatus(name, task, value):
	"""Wrapper to avoid mapping of ColumNames"""
	setValue(name, "Status" + task.upper(), value)

def setTodo(name, task, value):
	"""Wrapper to avoid mapping of ColumNames"""
	setValue(name, "ToDo" + task.upper(), value)
'''


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

	tasks = sg.find("Task", [PROJECT_FILTER], ["content", "entity", "sg_status_list"])

	for task in tasks:
		name = task["entity"]["name"].split("_")[-1]
		taskNameSG = task["content"]
		status = task["sg_status_list"]

		if taskNameSG in mappingsShotGun2Local:
			taskName = mappingsShotGun2Local[taskNameSG]
			Index.setValue(name, taskName + "_Todo", "")
			Index.setValue(name, taskName + "_Status", status)



def load():
	Index.clear()
	loadAssets()

	loadTasks()

	Index.reWriteOverview()
	Index.save(Index.data)


if __name__ == '__main__':
	pass
	load()

	#print ("Svobodan")

	#setValue("Z_90100", "ToDoCOMP", "Test123")
	#setValue("Adler", "ToDoRIG", "Test123")
	#loadAssets()
	#loadShots()
	#row2shot(None)