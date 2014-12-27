#import re
import os
import cPickle as pickle


DB_FILENAME = os.path.splitext(__file__)[0] + ".p"
data = None

def load():
	global data
	data = pickle.load( open( DB_FILENAME, "r" ) )
	return data


def getFilter(parts):
	attr	= parts[2]
	op		= parts[1]
	value	= parts[0]


	if op == "==":
		def filterFunction(item):
			if not attr in item:
				return True
			else:
				return item[attr] == value
		return filterFunction

	if parts[1] == "in":
		def filterFunction(item):
			if (not attr in item):
				return True
			elif item[attr] in [None, ""]:
				return False
			else:
				return parts[0] in item[parts[2]]

	return filterFunction



########################
#
#	get Lists
#
#

def getTypes():
	if not data: load()
	return data["Overview"]["Types"]
	#return [tableName for tableName in db.getTables()][1:]



def getGroups(filterType=None):
	if not data: load()

	groups = []
	for name in data["items"]:
		item = data["items"][name]

		# Filter ?
		if filterType and item["Type"] != filterType:
			continue

		if item["Group"] not in groups:
			groups.append(item["Group"])
	return sorted(groups)




def getNames(filterType=None, filterGroup=None, Filter=[]):
	if not data: load()

	names = []
	for name in data["items"]:
		item = data["items"][name]

		# Filter by Type
		if filterType and item["Type"] != filterType:
			continue

		# Filter by Group
		if filterGroup and item["Group"] != filterGroup:
			continue

		# Cutsom Filter
		if False in [getFilter(f)(item) for f in Filter]:
			continue

		names.append(name)
	return sorted(names)


#print getNames(Filter=Filter)

########################
#
#	get Values
#
#

def getType(name):
	"""Obsolete ???"""
	if not data: load()
	return data["items"][name]["Type"]


def getTasks(filterType=None):		#, filterName=None, filterGrp=None ???
	if not data: load()

	if filterType not in getTypes():
		filterType = getType(filterType)

	# Get TaskTouple based on Type
	if filterType:
		taskTouples = data["Overview"][filterType]["Tasks"]
	else:
		taskTouples = []
		for Type in data["Overview"]["Types"]:
			taskTouples += data["Overview"][Type]["Tasks"]


	return [taskName for taskNum, taskName in taskTouples]


def getTaskNum(name):
	if not data: load()

	for Type in data["Overview"]["Types"]:
		for taskNum, taskName in data["Overview"][Type]["Tasks"]:
			if taskName == name:
				return taskNum


def getValue(name, attr):
	if not data: load()
	if name in data["items"]:
		return data["items"][name][attr]
	else:
		return None




########################
#
#	setValues
#
#
def save(data):
	dbFile = open(DB_FILENAME, "w")
	pickle.dump(data, dbFile)
	dbFile.close()


def setValue(name, attr, value, saveData=True):
	if not data: load()

	#print "SaveValue", attr, value, type(value)

	if name in data["items"]:
		data["items"][name][attr] = value
	else:
		print "[INDEX] New Shot?", name
		data["items"][name] = {}
		data["items"][name][attr] = value

	if saveData:
		save(data)



if __name__ == '__main__':
	pass
	load()

	#for name in sorted(data["items"].keys()):
	#	print name #["Z_90100"]["Description"]
	value = data["items"]["Z_90100"]["COMP_Todo"]
	print value, type(value)

	#k = str(data["items"].keys()[0]).replace("\n", "")
	#print k, type(k)
	#l = unicode("F_25430")
	#print l, type(l)
	#print l == str(k)
	#print data["items"]["F_25430"]
	#print getValue("Z_90200", "Tags")
	#shots = getNames("Shots", Filter=[("VFX", "in", "Tags"), ("C", "==", "Group")])
	#print len(shots), shots
	#setValue("Z_90100", "COMP_Todo", "Test123456")

