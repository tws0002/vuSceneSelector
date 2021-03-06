import os, sys
import re

WORKING_DIR = os.path.dirname(__file__)
rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-1])

sys.path.append(rootDir)
sys.path.append(rootDir + "/sync/libs")
import gdata.spreadsheet.service

from core import Index
LAST_SYNC = None


# Settings
SETTINGS_PROJECT = os.getenv("SETTINGS_PROJECT")
if not SETTINGS_PROJECT:
	print "[ERROR] SETTINGS_PROJECT not set via Envoriment-Variable!"
	settings_Folder =  rootDir + "/_ProjectSettings/"
	#SETTINGS_PROJECT = settings_Folder + "project_Jagon.py"
	SETTINGS_PROJECT = settings_Folder + "project_Flut.py"
	#SETTINGS_PROJECT = settings_Folder + "project_Kroetenlied.py"
	#SETTINGS_PROJECT = "F:/070_SOFTWARE/_Tools/vuSceneSelector_Settings/project_Flut.py"



from core import Settings
SETTINGS = Settings.SETTINGS
SETTINGS.load(SETTINGS_PROJECT, "r")
SETTINGS.load(SETTINGS["Settings_User"])


SPREADSHEET_KEY = SETTINGS["syncGoogleSpreadSheet"]

ATTRS_SHOT  = ["Description"] + SETTINGS["headerInfosShots"] + ["startHandle", "endHandle", "Frames", "firstFrame", "lastFrame"]
ATTRS_ASSET = ["Description"]

if SETTINGS["projectName"] == "Jagon":
	ATTRS_SHOT += ["Tags"]


SHEETNAMES = {}
if SETTINGS["projectName"] == "Jagon":
	SHEETNAMES["Shots"] = "Shots"
	SHEETNAMES["Assets"] = "Assets"
else:
	SHEETNAMES["Shots"] = "WSDF_Shots"
	SHEETNAMES["Assets"] = "WSDF_Assets"


##########################
#
#	Setup & Helpers
#
#
import socket
domain = socket.getfqdn()
IS_AKA = domain.endswith(".medianet.animationsinstitut.de")

def createService():
	if IS_AKA:
		os.environ["http_proxy"] = "http://quake:3128"
		os.environ["https_proxy"] = "https://quake:3128"

	spr_client = gdata.spreadsheet.service.SpreadsheetsService()
	spr_client.email = 'vuPipelineFilmakademie@gmail.com'
	spr_client.password = 'filmaka2014'
	spr_client.ProgrammaticLogin()
	return spr_client


def findSheet(spr_client, Type):
	sheetName = SHEETNAMES[Type]
	sheets = spr_client.GetWorksheetsFeed(SPREADSHEET_KEY)
	for sheet in sheets.entry:
		if sheet.title.text == sheetName:
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


##########################
#
#	SetValues
#
#


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



##########################
#
#	GetValues
#
#

def row2tasks(name, row):
	for task in Index.getTasks(name):
		# Get Values
		artistValue = row["artist" + task.lower()].text
		artist = re.findall("\w+\s*\w+", artistValue) if artistValue else None


		status = row["status" + task.lower()].text
		todo   = row["todo"   + task.lower()].text
		mandays= row["mandays"+ task.lower()].text

		# Set Values
		Index.setValue(name, task + "_Status", status  if status  else "", saveData=False)
		Index.setValue(name, task + "_Artist", artist  if artist  else "", saveData=False)
		Index.setValue(name, task + "_Todo",   todo    if todo    else "", saveData=False)
		Index.setValue(name, task + "_Mandays",mandays if mandays else "", saveData=False)
	return True



def row2shot(row):
	name = row["shotnamevfx"].text

	if not name:
		return False

	# Exeption for Shots != Jagon
	print "[SYNC-GOOGLE] Load Shots", name

	Index.setValue(name, "Type", "Shots", saveData=False)
	Index.setValue(name, "Group", re.findall("[A-Za-z]+", name)[0], saveData=False)
	Index.setValue(name, "Num", re.findall("\d+", name)[0],         saveData=False)
	Index.setValue(name, "Code", name, saveData=False)


	for attr in ATTRS_SHOT:
		value = row[attr.lower()].text
		Index.setValue(name, attr, value if value else "", saveData=False)

	# WSDF
	if SETTINGS["projectName"] == "WirSindDieFlut":
		Index.setValue(name, "Tags", "VFX", saveData=False)

	row2tasks(name, row)
	return True



def row2asset(row):
	name = row["assetname"].text
	if not name:
		return False
	print "[SYNC-GOOGLE] Load Assets", name

	Index.setValue(name, "Type",	"Assets", saveData=False)
	Index.setValue(name, "Group",	row["assetgroup"].text, saveData=False)
	Index.setValue(name, "Num",		row["assetnum"].text, saveData=False)
	Index.setValue(name, "Code",	name, saveData=False)

	for attr in ATTRS_ASSET:
		value = row[attr.lower()].text
		Index.setValue(name, attr, value if value else "", saveData=False)

	row2tasks(name, row)
	return True


def loadShots():
	print "[SYNC-GOOGLE] Load Shots -- start --"
	Type = "Shots"
	spr_client = createService()

	# Find Sheet, than Cell than Udate
	sheetID = findSheet(spr_client, Type)

	for row in spr_client.GetListFeed(SPREADSHEET_KEY, sheetID).entry:
		if row.custom["shotnamevfx"].text:
			row2shot(row.custom)
	print "[SYNC-GOOGLE] Load Shots -- done --"


def loadAssets():
	print "[SYNC-GOOGLE] Load Assets -- start --"
	Type = "Assets"
	spr_client = createService()

	# Find Sheet, than Cell than Udate
	sheetID = findSheet(spr_client, Type)

	for row in spr_client.GetListFeed(SPREADSHEET_KEY, sheetID).entry:
		if row.custom["assetname"].text:
			row2asset(row.custom)
	print "[SYNC-GOOGLE] Load Assets -- done --"




def save():
	print "[SYNC-GOOGLE]", "SaveData!"
	Index.save(Index.data)


def load(force=True):
	oldData = Index.load()

	# Write Data
	Index.clear()
	if SETTINGS["projectName"] == "Jagon":
		Index.reWriteOverviewJagon()
	else:
		Index.reWriteOverviewFlut()
	loadAssets()
	loadShots()

	# Save
	if force:
		save()
		return True

	if oldData["items"] != Index.data["items"]:
		return Index.data

	return False




if __name__ == '__main__':
	pass
	load()
	#setValue("Z_90100", "ToDoCOMP", "Test123")
	#setValue("Adler", "ToDoRIG", "Test123")
	#loadAssets()
	#loadShots()
	#row2shot(None)