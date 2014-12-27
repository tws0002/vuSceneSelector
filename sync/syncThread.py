import sys, os, shutil
import time
import cPickle as pickle

WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
rootDir = os.sep.join(WORKING_DIR.split(os.sep)[:-1])
sys.path.append(rootDir)

# Import Modules


# Settings
projectRoot = 'V:' if sys.platform.startswith("win") else '/ln/Jagon'
settings_Folder = projectRoot + "/090_Software/Intern/vuPipelineOverview_Settings/"
SETTINGS_PROJECT = settings_Folder + "project_Jagon.py"



from core import Settings
SETTINGS = Settings.SETTINGS
SETTINGS.load(SETTINGS_PROJECT, "r")

TASK_FOLDER = SETTINGS["syncFolder"]

syncMode = SETTINGS["syncMode"]
if syncMode == "Google":
	from sync import syncGoogle as syncModule



#####################################
#
#
#		Main
#


def watch():
	for fileName in os.listdir(TASK_FOLDER):
		if os.path.isdir(TASK_FOLDER + "/" + fileName):
			continue


		# Get Task-Values
		name, attr, value = pickle.load(open( TASK_FOLDER + "/" + fileName, "r" ))
		print fileName, name, attr, value


		# DEBUG
		if not name.startswith("Z"):
			return

		if attr.endswith("_Status"):
			task = attr.split("_")[0]
			syncModule.setStatus(name, task, value)
		elif attr.endswith("_Todo"):
			task = attr.split("_")[0]
			syncModule.setTodo(name, task, value)

		# Call SyncModule
		#syncModule.setValue(values)

		# Delete Tasks
		shutil.move(TASK_FOLDER + "/" + fileName, TASK_FOLDER + "/_OLD/" + fileName)


if __name__ == "__main__":
	watch()
	#syncModule.setValue("Z_90100", "COMP_Status", 0)



