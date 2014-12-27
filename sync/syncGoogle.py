import os, sys

WORKING_DIR = os.path.dirname(__file__)
rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-1])

sys.path.append(rootDir)
sys.path.append(rootDir + "/sync/libs")
import gdata.spreadsheet.service

from core import Index

SPREADSHEET_KEY = "1Jyigwenkykobsq29sh-CSTxZKkpbEmlkUm6s7S9uZZI"



##########################
#
#	Setup & Helpers
#
#

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
		status = row["status" + task.lower()].text
		artist = row["artist" + task.lower()].text
		todo   = row["todo"   + task.lower()].text

		# Set Values
		Index.setValue(name, task + "_Status", status if status else "", saveData=False)
		Index.setValue(name, task + "_Artist", artist if artist else "", saveData=False)
		Index.setValue(name, task + "_Todo",   todo   if todo   else "", saveData=False)
	return True


ATTRS_SHOT = ["Tags", "firstFrame", "lastFrame", "startHandle", "endHandle", "Lens", "Frames", "FPS", "Description"]
def row2shot(row):
	name = row["shotnamevfx"].text
	if not name:
		return False
	print "[SYNC-GOOGLE] Load Shots", name

	Index.setValue(name, "Type", "Shots", saveData=False)
	Index.setValue(name, "Group", name.split("_")[0], saveData=False)
	Index.setValue(name, "Num", name.split("_")[1], saveData=False)
	Index.setValue(name, "Code", name, saveData=False)

	for attr in ATTRS_SHOT:
		value = row[attr.lower()].text
		Index.setValue(name, attr, value if value else "", saveData=False)

	row2tasks(name, row)

	# Save
	#Index.save(Index.data)
	return True

ATTRS_ASSET = ["Description"]
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




def load():
	loadAssets()
	loadShots()
	Index.save(Index.data)


if __name__ == '__main__':
	pass
	#setValue("Z_90100", "ToDoCOMP", "Test123")
	#setValue("Adler", "ToDoRIG", "Test123")
	#loadAssets()
	#loadShots()
	#row2shot(None)