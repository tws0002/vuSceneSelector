
#######################################
#
#	Add Shots:
#	Template: ("A", "010", "ShotName"),
#

Shots = [
	("Z", "010", "RigTest01"),
	("Z", "020", "CookieTest01")
]




# Additional Arrays/Dicts
ShotSeq = []			# Array: Shot Sqeuence (A,B,C)
ShotNums = []			# Array: Numbers
ShotCodes = []			# Array: Codes (Seq + Num) eg. A010
ShotNames = []			# Array: Names.
ShotNamesCompl = []		# Array: Complete Names (incl Seq and Num).
ShotDict = {}			# Dict: All in All for Functions


for seq, num, name in Shots:
	if seq not in ShotSeq:
		ShotSeq.append(seq)
	ShotNums.append(num)
	ShotNames.append(name)

	shotCode = seq + num
	ShotCodes.append(shotCode)

	shotNameCompl = seq + num + "_" + name
	ShotNamesCompl.append(shotNameCompl)


	data = (seq, num, name, shotCode, shotNameCompl)
	for value in data:
		ShotDict[value] = data


def getSeq(value):
	return ShotDict[value][0]

def getNum(value):
	return ShotDict[value][1]

def getName(value):
	return ShotDict[value][2]

def getCode(value):
	return ShotDict[value][3]

def getNameCompl(value):
	return ShotDict[value][4]



# Debug
"""
print "ShotNames: " + str(ShotNames)
print "ShotNums: " + str(ShotNums)
print "ShotSeq: " + str(ShotSeq)
print "Shots: " + str(ShotDict)
"""


# TestShots
"""
	##############################
	("A", "010", "Muecke"),
	("A", "020", "Augenbewegung"),
	("A", "030", "Paychiater"),
	("A", "040", "spricht"),
	("A", "050", "Pendel"),
	("A", "060", "hypnotisiert"),
	("A", "070", "Beginn"),
	("A", "080", "Zunge"),
	("A", "090", "Richtung"),
	("A", "100", "Maschine"),
	("A", "110", "beleidigt"),
	("A", "120", "Gehen"),
	("A", "130", "Operationsbesteck"),
	("A", "140", "beleidigt"),
	("A", "150", "Streit"),
	("A", "160", "schmerzverzerrt"),
	("A", "170", "schiesst"),
	("A", "180", "zetert"),
	("A", "190", "Erkrankung"),
	("A", "200", "fliegt"),
	("A", "210", "versucht"),
	("A", "220", "Witz"),

	########################
	("B", "230", "Tansition"),

	########################
	("C", "240", "entdecktSumpf"),
	("C", "250", "entdecktChor"),
	("C", "260", "umschauen"),
	("C", "270", "Kind1"),
	("C", "280", "Anschlussbild"),
	("C", "290", "KroetenParade"),
	("C", "300", "SvobosBlick"),
	("C", "310", "SackAufWasser"),
	("C", "320", "SvoboMitTuete"),
	("C", "330", "zurueckAufKopf"),
	("C", "340", "Zupfer"),
	("C", "350", "singen"),

	########################
	("D", "360", "Psychiater"),
	("D", "370", "Ransprung"),
	("D", "380", "Abschlussbild"),
	########################
"""