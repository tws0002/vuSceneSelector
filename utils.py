import os
import datetime
import getpass

##############################################################################################
#
#
#		Settings
#


from settings import project
LOG_FILE = project.folderPipeline + "/" + project.PROJECT_NAME + "/logFiles/logSceneSelector"


def timeStamp_Format(time):
	return datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M:%S')


def getFile_LastModify(path):
	return timeStamp_Format(os.path.getmtime(path))

def getFile_FileSize(path):
	return fileSize_HumanReadable(os.path.getsize(path))

def getArtist(short=True):
	return getpass.getuser()[:2] if short else getpass.getuser()


def fileSize_HumanReadable(bytes):
	for x in ['bytes','KB','MB','GB']:
		if bytes < 1024.0 and bytes > -1024.0:
			return "%3.1f %s" % (bytes, x)
		bytes /= 1024.0
	return "%3.1f %s" % (bytes, 'TB')


def log(event):
	logFile = LOG_FILE + "_" + getpass.getuser() + "_" + datetime.datetime.now().strftime("%Y_%m_%d") + ".log"

	# Stop Spaming!
	#if getpass.getuser() == "vullmann":
	#	return

	# Read old File
	lines = open(logFile, 'r').readlines() if os.path.exists(logFile) else []

	# Gather Data
	time = datetime.datetime.now().strftime("%H:%M:%S")
	newLine = time + " || Event: " + event + "\n"

	# Add Data and write File
	lines.append(newLine)
	out = open(logFile, 'w')
	out.writelines(lines)
	out.close()

	return True