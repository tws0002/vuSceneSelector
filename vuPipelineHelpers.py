import getpass
import datetime
import os



def getArtist():
	return getpass.getuser()[:2]

def log(LOG_FILE, msg):
	logFile = LOG_FILE + "_" + getpass.getuser() + "_" + datetime.datetime.now().strftime("%Y_%m_%d") + ".log"

	lines = open(logFile, 'r').readlines() if os.path.exists(logFile) else []

	newLine = "\n"
	newLine += datetime.datetime.now().strftime("%H:%M:%S")
	newLine += " || Event: " + msg

	lines.append(newLine)
	out = open(logFile, 'w')
	out.writelines(lines)
	out.close()