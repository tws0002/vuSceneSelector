import sys, os, shutil
import time
import cPickle as pickle
import datetime


WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-1])
sys.path.append(rootDir)

# Import Modules


# Settings
SETTINGS_PROJECT = os.getenv("SETTINGS_PROJECT")

if not SETTINGS_PROJECT:
	print "[ERROR] SETTINGS_PROJECT not set via Envoriment-Variable!"
	settings_Folder =  os.path.dirname(os.path.abspath(__file__)) + "/_ProjectSettings/"
	#SETTINGS_PROJECT = settings_Folder + "project_Jagon.py"
	SETTINGS_PROJECT = settings_Folder + "project_Kroetenlied.py"



from core import Settings
SETTINGS = Settings.SETTINGS
SETTINGS.load(SETTINGS_PROJECT, "r")

TASK_FOLDER = SETTINGS["syncFolder"]

syncMode = SETTINGS["syncMode"]
if syncMode == "Google":
	from sync import syncGoogle as syncModule
elif syncMode == "Shotgun":
	from sync import syncShotgun as syncModule


#####################################
#
#
#		Main
#


LAST_SYNC = datetime.datetime(year=1, month=1, day=1)

def getTaskFiles():
	files = [f for f in os.listdir(TASK_FOLDER) if os.path.isfile(TASK_FOLDER + "/" + f)]	# Get only Files
	return sorted(files)

def processUploads():
	files = getTaskFiles()

	if not len(files):
		return False

	else:
		for fileName in files:
			# Get Task-Values
			name, attr, value = pickle.load(open( TASK_FOLDER + "/" + fileName, "r" ))
			print "\n", fileName, name, attr, value

			# Call SyncModule
			if attr.endswith("_Status"):
				task = attr.split("_")[0]
				syncModule.setStatus(name, task, value)
			elif attr.endswith("_Todo"):
				task = attr.split("_")[0]
				syncModule.setTodo(name, task, value)

			# Delete Tasks
			shutil.move(TASK_FOLDER + "/" + fileName, TASK_FOLDER + "/_OLD/" + fileName)
		return True


DOWNLOAD_INTERVALL = datetime.timedelta(minutes=5)

def watch():
	processUploads()

	# Reload All?
	global LAST_SYNC
	timeSinceLastSync = datetime.datetime.now() - LAST_SYNC

	if timeSinceLastSync > DOWNLOAD_INTERVALL:
		if syncModule.load(force=False):

			# Make sure, there are no new Tasks
			if not len(getTaskFiles()):
				syncModule.save()
				LAST_SYNC = datetime.datetime.now()
			else:
				processUploads()


		else: # No need to sync
			LAST_SYNC = datetime.datetime.now()
	else:
		msg = "\rTime till next Download: " + str(DOWNLOAD_INTERVALL - timeSinceLastSync)
		sys.stdout.write(msg)
		sys.stdout.flush()




if __name__ == "__main__":
	pass
	#watch()
	#syncModule.setValue("Z_90100", "COMP_Status", 0)





