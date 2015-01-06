import os
import shutil
import re
import imp


DEFAULT_PROJECT = os.path.dirname(__file__) + "/SettingsDefault_Project.py"
DEFAULT_USER 	= os.path.dirname(__file__) + "/SettingsDefault_User.py"



class SettingsFile(object):
	"""SubPart of the Settings, for OneFile"""
	def __init__(self, filename, mode="rw"):
		self.filename = filename
		self.mode = mode
		self.data = {}
		self.load()

	def __str__(self):
		return self.filename

	def __getitem__(self, attr):
		return self.data[attr]


	def load(self):
		# Load as Module
		name = os.path.splitext(os.path.basename(self.filename))[0]
		mod = imp.load_source(name, self.filename)

		for name in dir(mod):
			# Skip Magic
			if name.startswith("_"): continue

			# Create new Attribute
			self.data[name] = getattr(mod, name)



	def saveHelper_setOne(self, lines, varName, varValue):
		if type(varValue) in [str, unicode]:
			varValue = "'" + varValue + "'"

		# Get LineNumber
		for lineNum, line in enumerate(lines):
			# ReWrite the Line
			if re.sub("\s+", "", line).split("=")[0] == varName:
				lines[lineNum] = varName + " = " + str(varValue) + "\n"
				break;
		return lines

	def save(self):
		if "w" not in self.mode:
			return False

		# Read old Content
		lines = open(self.filename, 'r').readlines()

		for varName in self.data:
			lines = self.saveHelper_setOne(lines, varName, self.data[varName])

		# Save File
		out = open(self.filename, 'w')
		out.writelines(lines)
		out.close()



class Settings(object):
	def __init__(self):
		self.files = []

		# Load Defaults
		self.load(DEFAULT_PROJECT, "r")
		self.load(DEFAULT_USER, "r")


	def load(self, filename, mode="rw"):
		"""Load the Settings"""
		if not os.path.exists(filename):
			print "[SETTINGS ERROR] File gibts net!", filename
			if not "w" in mode:
				return False
			shutil.copy(DEFAULT_USER, filename)
		settingsFile = SettingsFile(filename, mode)
		self.files = [settingsFile] + self.files # Append at the Front


	def save(self):
		"""Save all SettingsFiles"""
		for settingsFile in self.files:
			settingsFile.save()


	def __getitem__(self, attr):
		for settingsFile in self.files:
			if attr in settingsFile.data:
				return settingsFile.data[attr]

		# Attribute not found...
		return None


	def __setitem__(self, attr, value):
		# Find corret SettingsFile and SetValue there
		for settingsFile in self.files:
			if attr in settingsFile.data:
				settingsFile.data[attr] = value
				return True
		return False



SETTINGS = Settings()

if __name__ == '__main__':
	#SETTINGS_GLOBAL = "/ln/Dev/017_KroetenliedPipeline/vuSceneSelector_Tests/pyQt_Tests/settings_v001.py"
	#SETTINGS_USER = "/ln/Dev/017_KroetenliedPipeline/vuSceneSelector_Tests/pyQt_Tests/settings_v002.py"

	s = Settings()
	#s.load(SETTINGS_GLOBAL)
	#s.load(SETTINGS_USER)

	#s["PROJECT_NAME"] = "JagonUser3"
	#s["projectRoot"] = "V:"
	#s.save()
	#print s["projectRoot"]
