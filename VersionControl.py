import re	# for getVersion re.findall()
import os	# for getLatest os.listdir()


def incrVersion(fileName, up=1):
	# Replace Version(+0) with Verison(+x) or return Error
	return fileName.replace("_v" + str(getVersion(fileName, 0)), "_v" + str(getVersion(fileName, up))) if getVersion(fileName) else False


def getVersion(fileName, up=1, rType="str"):
	""" Return the Version of the FileName.
	It searches for "_v"

	Args:
		fileName (str):       The String, to be analyized
		up (int) [opt]:       The Amount the Version should be incremented
		rType (str) [opt]:    The ReturnType. "str" => Padded String (eg.: 0002), "int" => Integer (eg.: 2)

	Returns:
		the Version as String (or Int -> See Arg rType)

	Raises:
		returns False if no VersionString found
	"""

	vers = 0

	for namePart in fileName.split("_v")[1:]:				# Split "_v"
		if re.findall("\d+", namePart):						# Check if there are any Numbers in namePart
			vers = re.findall("\d+", namePart)[0]			# Resturn first Number if there is any
			break

	if not vers:											# Return Error
		return False
	else:
		# Add Up & ( KeepPadding as String or return Int)
		return ("0"*len(namePart) + str(int(vers) + up))[-len(vers):] if rType=="str" else eval(rType)(int(vers) + up)


def getLatest(root, up=0, baseName=None, getNum=False):
	"""Helps you finding the newest File in a Folder,
	depending on its version.
	Note: It searches for "_v"

	Args:
		root (str):                folder to search
		up (int) [opt]:            Optional increment of the version
		baseName (str) [opt]:      Optional filter. Only Files starting with this Name are analyized.
		getNum (bool) [opt]:       Optinal Flag. Will Return the Latest Version as Number

	Returns:
		the FileName with the highest VersionNumber
	"""

	#	TODO:
	#	Return Error if no File or VersionString found


	vers = 0
	latest = ""

	for fileName in os.listdir(root):

		# If BaseName angegeben aber fileName != startswith --> skip
		if baseName:
			if not fileName.startswith(baseName):
				continue

		curVer = getVersion(fileName, up=0, rType="int")

		if not curVer:
			continue

		# Get Hightest
		if curVer > vers:
			vers = curVer
			latest = fileName


	if getNum:
		return vers + up

	if up:
		return incrVersion(latest, up)
	else:
		return latest