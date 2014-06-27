import os
import datetime
import getpass

##############################################################################################
#
#
#		Settings
#

LOG_FILE = "//bigfoot/kroetenlied/_User/Vincent/Pipeline/LogFile_SceneSelector.log"



def timeStamp_Format(time):
	return datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M:%S')


def getFile_LastModify(path):
	return timeStamp_Format(os.path.getmtime(path))

def getFile_FileSize(path):
	return fileSize_HumanReadable(os.path.getsize(path))

def getArtist():
	return getpass.getuser()[:2]


def fileSize_HumanReadable(bytes):
	for x in ['bytes','KB','MB','GB']:
		if bytes < 1024.0 and bytes > -1024.0:
			return "%3.1f %s" % (bytes, x)
		bytes /= 1024.0
	return "%3.1f %s" % (bytes, 'TB')


def log(event):
	# Stop Spaming!
	if getpass.getuser() == "vullmann":
		return

	# Read old File
	lines = open(LOG_FILE, 'r').readlines() if os.path.exists(LOG_FILE) else []

	# Gather Data
	time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	user = getpass.getuser() + " " * (12-len(getpass.getuser()))
	newLine = "Time: " + time + " || User: " + user + " || Event: " + event + "\n"

	# Add Data and write File
	lines.append(newLine)
	out = open(LOG_FILE, 'w')
	out.writelines(lines)
	out.close()

	return True