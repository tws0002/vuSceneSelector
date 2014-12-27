import os, sys
import datetime
import random, string
import cPickle as pickle


from core import Settings
SETTINGS = Settings.SETTINGS
TASK_FOLDER = SETTINGS["syncFolder"]





def getRandomString(length=10):
	return "".join([random.choice(string.ascii_letters + string.digits) for n in range(length)])


def getRandomFileName():
	# Get Vars:
	date = datetime.datetime.now().strftime("%Y_%m_%d")
	fileName = TASK_FOLDER + "/" + date + "_" + getRandomString() + ".vuSyncTask"

	if os.path.isfile(fileName):
		fileName = getRandomFileName()
	else:
		return fileName


def addTask(*args):
	fileName = getRandomFileName()

	pFile = open(fileName, "w")
	pickle.dump(args, pFile)
	pFile.close()


def getTasks():
	for fileName in os.listdir(TASK_FOLDER):
		args = pickle.load(open( TASK_FOLDER + "/" + fileName, "r" ))

		# Do this!
		#googleSync.setData()


#getTasks()

#for i in range(100):
#addTask("Z_90100", "COMP_Status", 0.5)