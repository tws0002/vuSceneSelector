import string


#######################################
#
#	Add Shots:
#	Template: ("A", "010", "ShotName"),
#

Assets = [
	("010", "Heros", "Svo", "Svobodan"),
	("020", "Heros", "Krt", "Kroete"),
	("030", "Heros", "Psy", "Psychiater"),
	("040", "Heros", "Knd", "Kind"),
	("050", "Heros", "Mue", "Muecke"),
	("060", "Heros", "KrtP", "PsychiaterKroete"),

	("100", "MusikKroeten", "MukBase", "MusikKroeteBase"),
	("110", "MusikKroeten", "MukA", "MusikKroeteA"),
	("120", "MusikKroeten", "MukB", "MusikKroeteB"),
	("130", "MusikKroeten", "MukC", "MusikKroeteC"),
	("140", "MusikKroeten", "MukD", "MusikKroeteD"),
	("150", "MusikKroeten", "MukE", "MusikKroeteE"),
	("160", "MusikKroeten", "MukF", "MusikKroeteF"),
	("170", "MusikKroeten", "MukG", "MusikKroeteG"),
	("180", "MusikKroeten", "MukH", "MusikKroeteH"),
	("190", "MusikKroeten", "MukI", "MusikKroeteI"),
]





# Additional Arrays/Dicts
AssetNames = []			# Array: Names. eg.: Svobodan
AssetNums = []			# Array: Numbers
AssetCodes = []			# Array: ShortNames
AssetGroups = []		# Array: Groups
AssetDict = {}			# Dict: All in All for Functions


for num, grp, code, name in Assets:
	AssetNames.append(name)
	AssetNums.append(num)
	AssetCodes.append(code)

	if grp not in AssetGroups:
		AssetGroups.append(grp)

	AssetDict[num] = (num, grp, code, name)
	AssetDict[grp] = (num, grp, code, name)
	AssetDict[code] = (num, grp, code, name)
	AssetDict[name] = (num, grp, code, name)



def getNum(value):
	return AssetDict[value][0]

def getGrp(value):
	return AssetDict[value][1]

def getCode(value):
	return AssetDict[value][2]

def getName(value):
	return AssetDict[value][3]


#####################
#					#
#		DEBUG		#
#					#
#####################
"""
print "AssetNames: " + str(AssetNames)
print "AssetNums: " + str(AssetNums)
print "AssetCodes: " + str(AssetCodes)
print "AssetDict: " + str(AssetDict)
"""
print "AssetDict: \n" + str(AssetDict).replace("),", "),\n")