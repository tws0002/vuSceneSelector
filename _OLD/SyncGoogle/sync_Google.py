import sys
import os
import re
from PyQt4 import QtCore, QtGui


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(WORKING_DIR + "/libs")
import gdata.spreadsheet.service


sys.path.append("V:/090_Software/Intern")
from JagonIndex import Shots, Assets, Index
#sys.path.append("D:/Vincent/Dropbox/btSyncFolders/Dev/017_KroetenliedPipeline/vuSceneSelector_Jagon/libs")


# Settings
#SPREADSHEET_KEY = '0AiZru5nhPfrsdC1ySlpNcVFFLTNob04wTEY5aG1UcXc'
SPREADSHEET_KEY = "1Jyigwenkykobsq29sh-CSTxZKkpbEmlkUm6s7S9uZZI"
SHEET_ID_SHOTS = 1
SHEET_ID_ASSETS = 2
worksheet_id = 'od6'





def createService():
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"

	spr_client = gdata.spreadsheet.service.SpreadsheetsService()
	spr_client.email = 'vuPipelineFilmakademie@gmail.com'
	spr_client.password = 'filmaka2014'
	spr_client.ProgrammaticLogin()
	return spr_client



def findCell(spr_client, sheetID, nameCol, name, column):
	cells = spr_client.GetCellsFeed(SPREADSHEET_KEY, sheetID).entry

	titles = {}
	tarRow, tarCol = None, None

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


		if tarCol and tarRow:#
			print "CellFound: ", tarCol, tarRow
			return tarCol, tarRow


def setValue(Type, name, column, value):

	print "Start UpdateCell: Type: ", Type, " // name: ", name, " // column: ", column, " // value: ", value


	if Type == "Shots":
		sheetID = SHEET_ID_SHOTS
		nameCol = "ShotNameVFX"
	elif Type == "Assets":
		sheetID = SHEET_ID_ASSETS
		nameCol = "AssetName"

	spr_client = createService()
	tarCol, tarRow = findCell(spr_client, sheetID, nameCol, name, column)
	spr_client.UpdateCell(tarRow, tarCol, value, SPREADSHEET_KEY, sheetID)
	return False


def setStatus(Type, name, task, status):
	setValue(Type, name, "Status" + task, status)

def setTodo(Type, name, task, value):
	setValue(Type, name, "ToDo" + task, value)


def loadShots():
	# Get DB-Columns
	columnsDBStr = Index.getValue("Overview", "Shots", "Columns")

	columnsDB = {}
	for name in re.findall("\w+", columnsDBStr):
		columnsDB[name.lower()] = name

	spr_client = createService()
	for row in spr_client.GetListFeed(SPREADSHEET_KEY, SHEET_ID_SHOTS).entry:
		name = row.custom["shotnamevfx"].text

		# Skip empty Rows
		if name in [".", "", None]:
			continue

		# Skip non VFX-Shots
		#if not row.custom["tags"].text or "VFX" not in row.custom["tags"].text:
		#	print "Skip Shot:", name
		#	continue

		# Set Values
		for key in row.custom:
			if key in columnsDB:
				value = row.custom[key].text
				value = value if value else ""
				Index.setValue("Shots", name, columnsDB[key], value, False)
	Index.save()


def loadAssets(widget=None):
	# Get DB-Columns
	columnsDBStr = Index.getValue("Overview", "Assets", "Columns")

	columnsDB = {}
	for name in re.findall("\w+", columnsDBStr):

		#print name
		if name == "grp":
			columnsDB["assetgroup"] = name
		elif name == "Num":
			columnsDB["assetnum"] = name
		else:
			columnsDB[name.lower()] = name

	spr_client = createService()
	sheets = spr_client.GetWorksheetsFeed(SPREADSHEET_KEY)
	for sheet in sheets.entry:
		if sheet.title.text == "Assets":
			worksheet_id = sheet.id.text.split("/")[-1]
			for row in spr_client.GetListFeed(SPREADSHEET_KEY, worksheet_id).entry:
				name = row.custom["assetname"].text

				print "Assets", name

				# Skip empty Rows
				if name in [".", "", None]:
					continue


				# Set Values
				for key in row.custom:
					if key in columnsDB:
						value = row.custom[key].text
						value = value if value else ""
						Index.setValue("Assets", name, columnsDB[key], value, False)
			Index.save()
			return True


def load():
	print "[SyncGoogle] Start loading Data..."
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"

	loadShots()
	#loadAssets()

	#Assets.save(assets)
	return

def save(widget=None):
	print "[SyncGoogle] Start saving Data..."
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"

	reload(Shots)
	#save_GoogleShots(widget)
	#save_GoogleAssets(widget)




def addNewColumn():
	print "Hallo"
	Index.db.addColumn("Shots", "Tags")



if __name__ == "__main__":
	#save_Google()
	load()






	#columns = Index.db.getValue("Overview", "Shots", "Columns")
	#Index.db.setValue("Overview", "Shots", "Columns", columns + ",Tags", True)

	#print updateSingleCell("A_00300", "StatusTrack", "MehrTest")
	#print updateSingleCell("A_00200", "ToDoTrack", "TODo something here")
	#print "Start"
	#shots = load_GoogleShots()
	#print shots

"""
"""








#Index.setValue("Shots", "Z_90100", "Lens", "50")


#items = {'Z_90100': {'FPS': '2', 'Manntage Prozent der Gesamtmanntage': '7,857142857', 'Thumb': 'Shotcount', 'StatusANIM': '0', 'Comp Mandays': '219,5', 'Description': 'TestShot f\xc3\xbcr Pipeline', 'Anim Mandays': '42,5', 'Tags': 'VFX', 'StatusLIGHT': '1', 'StatusMATTEPAINT': '0', 'ToDoTRACK': 'Test\nMultine for\nTableView', 'Last\nFrame': '1090', 'Manntage pro Shot': '72', 'StatusSFS': '0', 'SlapComp Mandays': '50,5', 'endHandle': '10', 'Status3D': '0', 'StatusCOMP': '0.5', '3D Mandays': '34', 'Sim Mandays': '48', 'Mattepaint Mandays': '25', 'ShotNameVFX': 'Z_90100', 'Tracking Mandays': '42,5', 'First\nFrame': '1006', 'Light Mandays': '45', 'startHandle': '20', 'StatusSLAPCOMP': '0', 'SFS Mandays': '8', 'Frames': '100', 'StatusSIM': '0'}}
#print "Columsn GoogleDocs", items

#titles = {'lastFrame': '14', 'Manntage pro Sequenz': '48', 'Manntage Prozent der Gesamtmanntage': '49', '24': 'statusCOMP', '26': 'todoTRACK', '27': 'todoMATTEPAINT', '20': 'statusSIM', '21': 'statusSFS', '22': 'statusLIGHT', 'mandaysLIGHT': '43', 'todoSLAPCOMP': '33', 'todoTRACK': '26', '29': 'todoANIM', '4': 'Thumb', '8': 'Lens', 'ShotNameVFX': '1', 'todoLIGHT': '32', 'mandaysANIM': '40', 'Frames': '12', 'statusSLAPCOMP': '23', 'mandaysSLAPCOMP': '44', 'status3D': '18', '3': 'Tags', '46': 'Anmerkungen Manntage', '7': 'Description', 'endHandle': '11', 'mandaysSFS': '42', '39': 'mandays3D', '38': 'mandaysMATTEPAINT', '33': 'todoSLAPCOMP', '32': 'todoLIGHT', '31': 'todoSFS', '30': 'todoSIM', '37': 'mandaysTRACK', '36': 'Difficulty', '34': 'todoCOMP', 'todo3D': '28', 'Thumb': '4', 'statusLIGHT': '22', 'todoSFS': '31', 'Anmerkungen Manntage': '46', 'mandaysMATTEPAINT': '38', 'firstFrame': '13', 'Tags': '3', '23': 'statusSLAPCOMP', 'Lens': '8', 'mandays3D': '39', '2': 'ShotNameSchnitt', '6': 'Mucki / Gustus Notes', 'statusMATTEPAINT': '17', 'statusSIM': '20', '11': 'endHandle', '10': 'startHandle', '13': 'firstFrame', '12': 'Frames', '14': 'lastFrame', '17': 'statusMATTEPAINT', '16': 'statusTRACK', '19': 'statusANIM', '18': 'status3D', 'Difficulty': '36', 'mandaysTRACK': '37', 'mandaysSIM': '41', 'statusSFS': '21', 'Description': '7', '48': 'Manntage pro Sequenz', '49': 'Manntage Prozent der Gesamtmanntage', 'Mucki / Gustus Notes': '6', '47': 'Manntage pro Shot', '44': 'mandaysSLAPCOMP', '45': 'mandaysCOMP', '42': 'mandaysSFS', '43': 'mandaysLIGHT', '40': 'mandaysANIM', '41': 'mandaysSIM', '1': 'ShotNameVFX', 'ShotNameSchnitt': '2', 'Manntage pro Shot': '47', '5': 'Original Filename', 'todoMATTEPAINT': '27', '9': 'FPS', '28': 'todo3D', 'statusTRACK': '16', 'todoSIM': '30', 'statusANIM': '19', 'todoCOMP': '34', 'Original Filename': '5', 'FPS': '9', 'todoANIM': '29', 'startHandle': '10', 'statusCOMP': '24', 'mandaysCOMP': '45'}
#print titles






"""
for column in columns:
	if column in titles:
		print column
print columns
"""
"""
print googleColumns

for name in items:
	item = items[name]
	print name

	for col in columns:
		if col in titles:
			print name, col, item[col]
"""
"""
"""

		#db.setValue("Shots", shotName, columns[key], value)
"""
"""






# Debug
"""
print "ShotNames: " + str(ShotNames)
print "ShotNums: " + str(ShotNums)
print "ShotSeq: " + str(ShotSeq)
print "Shots: " + str(Dict)
"""
