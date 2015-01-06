#import re
import os
import cPickle as pickle
import re

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

	if op == "in":
		def filterFunction(name):
			return value in getValue(name, attr)

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


	names = data["items"].keys()

	# Filter by Type
	if filterType:
		names = [name for name in names if getValue(name, "Type") == filterType]

	# Filter by Group
	if filterGroup:
		names = [name for name in names if getValue(name, "Group") == filterGroup]

	# CustomFilters, Keep only if All Filters return True
	names = [name for name in names if all([getFilter(f)(name) for f in Filter])]

	return sorted(names)


def getArtists(filterType=None):
	if not data: load()

	artists = []

	for name in getNames(filterType):
		artists += getValue(name, "*_Artist")

	# Handle this somewhere else?
	tmp = []
	for name in artists:
		tmp += re.findall("\w+", name)

	return sorted(list(set(tmp)))





########################
#
#	get Values
#
#

def getAttrs(name=None, expr=None):
	if not data: load()

	if expr:
		# Get Values
		regex = re.compile(expr.replace("*", ".+"))
		attrs = getAttrs(name)
		return [attr for attr in attrs if re.match(regex, attr)]

	if name:
		return data["items"][name].keys()
	else:
		attrs = []
		for name in getNames():
			for key in data["items"][name].keys():
				if key not in attrs:
					attrs.append(key)
		return attrs


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

	if "*" in attr:
		attrs = getAttrs(name, attr)
		return [getValue(name, attrName) for attrName in attrs]
		#return [data["items"][name][attrName] for attrName in attrs]

		# Return as Dict?
		"""
		attrs = {}
		for attrName in getAttrs(name, attr):
			attrs[attrName] = getValue(name, attrName) #data["items"][name][attrName]
		return attrs
		"""

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








def Tests():

	# DEBUG getValues
	#print getValues("")


	# DEBUG GetAttrs
	if False:
		print 52 == len(getAttrs()),						getAttrs()
		print 40 == len(getAttrs("Z_90100")),				getAttrs("Z_90100")
		print 13 == len(getAttrs(expr="*_Status")),			getAttrs(expr="*_Status")
		print  9 == len(getAttrs("Z_90100" ,"*_Status")),	getAttrs("Z_90100" ,"*_Status")


if __name__ == '__main__':
	pass
	load()

	Tests()

	#shots = getNames(Filter=[("Martin", "in", "*_Artist")])
	#print len(shots), shots

	print getArtists()

	#print getValue("Z_90100", "*_Artist")


	#print getValue("Z_90100", "*_Artist")


	#print getAttrs("*_Status")
