import sys
import os
from PyQt4 import QtCore, QtGui


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(WORKING_DIR + "/libs")
import gdata.spreadsheet.service


sys.path.append("V:/090_Software/Intern")
from JagonIndex import Shots, Assets
#sys.path.append("D:/Vincent/Dropbox/btSyncFolders/Dev/017_KroetenliedPipeline/vuSceneSelector_Jagon/libs")


# Settings
SPREADSHEET_KEY = '0AiZru5nhPfrsdC1ySlpNcVFFLTNob04wTEY5aG1UcXc'
SHEET_ID_SHOTS = 1
SHEET_ID_ASSETS = 2
worksheet_id = 'od6'



def updateProgress(widget, label, pMin, pMax, pValue):
	widget.updateProgress(label, pMin, pMax, pValue)


def createService():
	email = 'vuPipelineFilmakademie@gmail.com'
	password = 'filmaka2014'
	spr_client = gdata.spreadsheet.service.SpreadsheetsService()
	spr_client.email = email
	spr_client.password = password
	spr_client.ProgrammaticLogin()
	return spr_client


def save_GoogleShots(widget=None):
	spr_client = createService()

	rows = spr_client.GetListFeed(SPREADSHEET_KEY, SHEET_ID_SHOTS).entry
	numRows = len(rows)
	for i, row in enumerate(rows):

		shotName = row.custom["shotnamevfx"].text

		if shotName == ".":
			continue

		print "processing Shot: (" + str(i) + "/" + str(numRows) + ") " + shotName
		if widget:
			updateProgress(widget, "Save Shot: " + shotName, 0, len(rows), i)

		# Get Old Data
		oldShot = {}
		newShot = {}
		for key in row.custom:

			# Get OldValue (online)
			oldValue = row.custom[key].text

			if oldValue:
				oldValue = row.custom[key].text
			else:
				oldValue = ""
			oldShot[key] = oldValue

			# Get NewValue (local)
			#print "ShotName: " + shotName
			#print "Key: " + key

			newValue = Shots.shots[shotName][key]
			newShot[key] = newValue


			# Compare
			if oldValue != newValue:
				pass
				#print "Key: " + key + " "*(20-len(key)) + " (old) " + str(oldValue) + " != " + str(newValue) + " (new)"


		# Hacked fixes!

		# Upload?
		if newShot != oldShot:
			print "Upload Shot: " + shotName + "\n\n"
			newShot["thumb"] = '=image("http://download.julianweiss.com/Jagon_Breakdownthumbs/' + shotName + '.png")'
			spr_client.UpdateRow(row, newShot)
		else:
			print "Skip Shot: " + shotName

		#for shot in shots:
		#print "--- All Shots Uploaded --- "

def save_GoogleAssets(widget=None):
	spr_client = createService()

	rows = spr_client.GetListFeed(SPREADSHEET_KEY, SHEET_ID_ASSETS).entry
	numRows = len(rows)
	for i, row in enumerate(rows):

		shotName = row.custom["assetname"].text

		if shotName == ".":
			continue

		print "processing Asset: (" + str(i) + "/" + str(numRows) + ") " + shotName
		if widget:
			updateProgress(widget, "Save Asset: " + shotName, 0, len(rows), i)

		# Get Old Data
		oldShot = {}
		newShot = {}
		for key in row.custom:

			# Get OldValue (online)
			oldValue = row.custom[key].text

			if oldValue:
				oldValue = row.custom[key].text
			else:
				oldValue = ""
			oldShot[key] = oldValue


			newValue = Assets.assets[shotName][key]
			newShot[key] = newValue

		# Upload?
		if newShot != oldShot:
			print "Upload Asset: " + shotName + "\n\n"
			newShot["thumb"] = '=image("http://download.julianweiss.com/Jagon_Breakdownthumbs/' + shotName + '.png")'
			spr_client.UpdateRow(row, newShot)
		else:
			print "Skip Asset: " + shotName

		#for shot in shots:
		#print "--- All Shots Uploaded --- "

def load_GoogleShots(widget=None):
	spr_client = createService()

	# Shots
	shots = {}
	rows = spr_client.GetListFeed(SPREADSHEET_KEY, SHEET_ID_SHOTS).entry
	for i, row in enumerate(rows):
		shotName = row.custom["shotnamevfx"].text

		if shotName == ".":
			continue

		if widget:
			updateProgress(widget, "Load Shot: " + shotName, 0, len(rows), i)

		shots[shotName] = {}

		print "---------- New Row: " + shotName + " -----------"
		for key in row.custom:

			value = row.custom[key].text

			# Convert Value
			if value:
				shots[shotName][key] = value
			else:
				shots[shotName][key] = ""

	return shots


def load_GoogleAssets(widget=None):
	spr_client = createService()
	assets = {}
	rows = spr_client.GetListFeed(SPREADSHEET_KEY, 2).entry
	for row in rows:
		assetName = row.custom["assetname"].text

		if assetName == ".":
			continue

		if widget:
			updateProgress(widget, "Load Asset: " + shotName, 0, len(rows), i)

		print "---------- New Row: " + assetName + " -----------"
		assets[assetName] = {}
		for key in row.custom:
			assets[assetName][key] = row.custom[key].text

	return assets


def load(widget=None):
	print "[SyncGoogle] Start loading Data..."
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"

	shots = load_GoogleShots(widget)
	Shots.save(shots)

	assets = load_GoogleAssets()
	Assets.save(assets)

	updateProgress(widget, "Done!", 0, 28, -3)
	return

def save(widget=None):
	print "[SyncGoogle] Start saving Data..."
	os.environ["http_proxy"] = "http://quake:3128"
	os.environ["https_proxy"] = "https://quake:3128"

	reload(Shots)
	save_GoogleShots(widget)
	save_GoogleAssets(widget)

	if widget:
		updateProgress(widget, "Done!", 0, 19935, -25)


def test():
	print "SyncGoogle Test"

if __name__ == "__main__":

	os.environ["http_proxy"] = "http://quake:3128"
  	os.environ["https_proxy"] = "https://quake:3128"
	#save_Google()
	#load()


	if len(sys.argv) != 1:
		if sys.argv[1] == "save":
			save()

		if sys.argv[1] == "load":
			load()

# Debug
"""
print "ShotNames: " + str(ShotNames)
print "ShotNums: " + str(ShotNums)
print "ShotSeq: " + str(ShotSeq)
print "Shots: " + str(Dict)
"""
