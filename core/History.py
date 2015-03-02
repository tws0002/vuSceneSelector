import os
import getpass
import datetime
import cPickle as pickle
import win32security



TASK_FOLDER = "V:/090_Software/Intern/vuPipelineOverview_Settings/syncTasks/_OLD"




def getUser(filePath):
	try:
		sd = win32security.GetFileSecurity (filePath, win32security.OWNER_SECURITY_INFORMATION)
		owner_sid = sd.GetSecurityDescriptorOwner ()
		name, domain, type = win32security.LookupAccountSid (None, owner_sid)
		return name
	except:
		printError("Unknown User: " + filePath)
		return "Unknown"



class HistoryDB(object):
	"""docstring for HistoryDB"""
	def __init__(self):
		self.dataValues = []




	def getFileName(self):
		fileName = os.path.dirname(__file__)[:-4] + "ui" + os.sep + "data" + os.sep + "history.log"
		return fileName


	def parseLine(self, line):
		line = line.replace("\n", "")

		# Get Parts
		parts = line.split(" ")
		parts += [""]*10

		event = {}
		event["date"] = " ".join(parts[:2])
		event["type"] = parts[2]
		event["user"] = parts[3]
		event["shot"] = parts[4]
		event["task"] = parts[5]
		event["value"] = parts[6]
		return event



	def readData(self):
		with open(self.getFileName()) as f:
			content = f.readlines()
		data = [self.parseLine(line) for line in content]

		return sorted(data, reverse=True, key=lambda k: k['date'])





	@property
	def data(self):
		if not len(self.dataValues):
			self.dataValues = self.readData()
		return self.dataValues




	def addEvent(self, date, event, user, msg):
		print "date", date
		print "event", event
		print "user", user
		print "msg", msg


		msg = date + " " + event + " " + user + " " + msg + "\n"

		fileName = self.getFileName()
		with open(fileName, "a") as f:
			f.write(msg)


	def addEventStatus(self, shot, task, value):
		date = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
		user = getpass.getuser()

		msg = date + " Status " + user + " " + shot + " " + task + " " + value + "\n"

		fileName = self.getFileName()
		with open(fileName, "a") as f:
			f.write(msg)


	def readFromSyncTasks(self):
		for fileName in os.listdir(TASK_FOLDER):
			args = pickle.load(open( TASK_FOLDER + "/" + fileName, "r" ))

			shot  = args[0]
			task  = args[1].split("_")[0]
			event = args[1].split("_")[1]
			value = args[2] if event == "Status" else ""
			msg = shot + " " + task  + " " + value

			# Get Data
			date = os.path.getmtime(TASK_FOLDER + "/" + fileName)
			date = datetime.datetime.fromtimestamp(date)
			date = date.strftime("%Y.%m.%d %H:%M:%S")

			# Get User
			user = getUser(TASK_FOLDER + "/" + fileName)

			self.addEvent(date, event, user, msg)


HISTORY = HistoryDB()



if __name__ == '__main__':
	pass
	#db = HistoryDB()


	#for i in range(100):
	#	db.addEvent("02.06.2015 20:15", "Status", "vullmann", "Z_90100 COMP ip")



	# Read from syncTasks
	#HISTORY.readFromSyncTasks()

	#for item in HISTORY.data:
	#	print item