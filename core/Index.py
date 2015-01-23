import os
import cPickle as pickle
import re
import time

DB_FILENAME = os.path.splitext(__file__)[0] + ".p"
DB_FILENAME = DB_FILENAME.replace("\\", os.sep)
data = None

def load():
	global data
	for i in range(20):
		try:
			with open( DB_FILENAME, "r" ) as dbFile:
				data = pickle.load(dbFile)
			return data
		except Exception, e:
			print "[INDEX-ERROR] Nr.:", i, e
			time.sleep(0.1)
			pass

def clear():
	print "[INDEX] Delte all Data!!!"
	global data
	data = {}
	data["Overview"] = {}
	data["items"] = {}
	#save(data)


def reWriteOverviewKroetenlied():
	#if not data: load()

	data["Overview"] = {}
	data["Overview"]["lastSync"] = ""
	data["Overview"]["Types"] = []

	# Get Tasks and add them
	data["Overview"]["Types"] += ["Asset", "Shot"]
	data["Overview"]["Asset"] = {}
	data["Overview"]["Asset"]["Tasks"] = []
	data["Overview"]["Asset"]["Tasks"] = [('010', 'GEO'), ('020', 'TEX'), ('030', 'RIG'), ('040', 'SHD')]
	data["Overview"]["Shot"] = {}
	data["Overview"]["Shot"]["Tasks"] = []
	data["Overview"]["Shot"]["Tasks"] = [("005", "BLOCK"), ('010', 'ANIM'), ('020', 'LIGHT'), ('030', 'COMP')]
	#save(data)


def reWriteOverviewJagon():
	if not data: load()

	data["Overview"] = {}
	data["Overview"]["lastSync"] = ""
	data["Overview"]["Types"] = []

	# Get Tasks and add them
	data["Overview"]["Types"] += ["Assets", "Shots"]
	data["Overview"]["Assets"] = {}
	data["Overview"]["Assets"]["Tasks"] = []
	data["Overview"]["Assets"]["Tasks"] = [('010', 'GEO'), ('020', 'TEX'), ('030', 'RIG'), ('040', 'SHD')]
	data["Overview"]["Shots"] = {}
	data["Overview"]["Shots"]["Tasks"] = []
	data["Overview"]["Shots"]["Tasks"] = [('010', 'TRACK'), ('020', 'MATTEPAINT'), ("025", "3D"), ('030', 'ANIM'), ("040", "SIM"), ("045", "SFS"), ("050", "LIGHT"), ("055", "SLAPCOMP"), ("060", "COMP")]
	#save(data)


def reWriteOverviewFlut():
	if not data: load()

	data["Overview"] = {}
	data["Overview"]["lastSync"] = ""
	data["Overview"]["Types"] = []

	# Get Tasks and add them
	data["Overview"]["Types"] += ["Assets", "Shots"]
	data["Overview"]["Assets"] = {}
	data["Overview"]["Assets"]["Tasks"] = []
	data["Overview"]["Assets"]["Tasks"] = [('010', 'GEO'), ('020', 'TEX'), ('030', 'RIG'), ('035', 'ANIM'), ('040', 'SHD')]
	data["Overview"]["Shots"] = {}
	data["Overview"]["Shots"]["Tasks"] = []
	data["Overview"]["Shots"]["Tasks"] = [('030', 'TRACK'), ('040', 'DMP'), ("050", "3D"), ('060', 'COMP')]
	#save(data)



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


def getArtists(filterType=None, filterShot=None):
	if not data: load()

	artists = []

	# Get ShotNames to query from
	if filterShot:
		names = [filterShot]
	else:
		names = getNames(filterType)

	# ShotNames to ArtistNames
	for name in names:
		value = getValue(name, "*_Artist")

		if type(value) == list:
			artists += [v for v in value if v != ""]
		elif type(value) == str and value != "":
			artists += [value]

	# Handle this somewhere else?
	"""
	tmp = []
	for name in artists:
		tmp += re.findall("\w+\s*\w+", name)
	"""
	#return []
	#return artists
	return sorted(list(set(artists)))





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


def getTasksByName(name):
	"""Used in fuActivty"""
	Type = getType(name)
	return getTasks(Type)


def getValue(name, attr):
	if not data: load()

	if "*" in attr:
		attrs = getAttrs(name, attr)

		tmp = []
		for attr in attrs:
			value = getValue(name, attr)

			if type(value) == list:
				tmp += value
			else:
				tmp += [value]

		return tmp
		#return [data["items"][name][attrName] for attrName in attrs]

		# Return as Dict?
		"""
		attrs = {}
		for attrName in getAttrs(name, attr):
			attrs[attrName] = getValue(name, attrName) #data["items"][name][attrName]
		return attrs
		"""

	if name in data["items"]:
		if attr in data["items"][name]:
			return data["items"][name][attr]

	print "[INDEX] Error", name, attr
	return None




########################
#
#	setValues
#
#


def save(data):
	#os.remove(DB_FILENAME)
	with open(DB_FILENAME, "w") as dbFile:
		pickle.dump(data, dbFile)



def setValue(name, attr, value, saveData=True):
	if not data: load()

	#print "SaveValue", attr, value, type(value)
	if value == None:
		value = ""

	if name in data["items"]:
		data["items"][name][attr] = value
	else:
		print "[INDEX] New Shot/Asset?", name
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
	if not data: load()

	#x = getValue("D530", "")
	#print x, type(x)
	#print data["items"]["F410"]
	#print getValue("F410", "Type")

	#print getNames()
	#print getTypes()
	#print getGroups("Shot")
	#print getGroups("Asset")

	#print data["items"]["A010"]
	#print data["items"]["Svobodan"]

	#reWriteOverview()

	#Tests()

	#shots = getNames(Filter=[("Martin", "in", "*_Artist")])
	#print len(shots), shots
	#print data["items"]["Z_90100"]["ANIM_Artist"]
	#print getValue("Z910", "*_Artist")

	#print getTypes()
	#print data["Overview"]
	#print getType("A010")

	#print getTasks("Shots")
	names = getNames()
	names = [name for name in names if "VFX" in getValue(name, "Tags")] # or name.endswith("MASTER")]
	print names
	"""
	for name in names:
		if getType(name) == "Shots" and "VFX" in getValue(name, "Tags"):
			print name
	"""

	#for artist in getArtists():
	#	print artist

	#print getValue("F_23720", "*_Artist")
	#print data["items"]["F_23720"]["3D_Artist"]
	#print getArtists(filterShot="E_18400")


	#print getValue("Z_90100", "*_Artist")


	#print getAttrs("*_Status")
