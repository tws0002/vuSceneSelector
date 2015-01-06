import os
import ConfigParser
reload(ConfigParser)


DEFAULT_PROJECT = os.path.dirname(__file__) + "/defaultConfig_Project.ini"
DEFAULT_USER 	= os.path.dirname(__file__) + "/defaultConfig_User.ini"



class ConfigParser_Edit(ConfigParser.ConfigParser):
	'''CustomVersion of ConfigParser, with some modifications... :-O'''
	def __init__(self):
		ConfigParser.ConfigParser.__init__(self)
		self.read(DEFAULT_USER)
		self.read(DEFAULT_PROJECT)


	def __getitem__(self, option):
		for section in self.sections():
			if self.has_option(section, option):
				return self.get(section, option)
		return None

	def __setitem__(self, option, value):
		for section in self.sections():
			if self.has_option(section, option):
				self.set(section, option, value)
				return True
		return False



#SETTINGS = Settings()
Config = ConfigParser_Edit()


if __name__ == '__main__':
	pass

	#print Config.get("User", "Favorites")
	#print Config["Favorites"]
	#print Config.get("UserSelections", "selType")
	#print Config["selType"]


	#print Config.get("Project", "Assets_FolderTemplate")



	#print ConfigParser.__file__


	with open(DEFAULT_USER, "w") as f:
		Config.write(f)


	#SETTINGS_GLOBAL = "/ln/Dev/017_KroetenliedPipeline/vuSceneSelector_Tests/pyQt_Tests/settings_v001.py"
	#SETTINGS_USER = "/ln/Dev/017_KroetenliedPipeline/vuSceneSelector_Tests/pyQt_Tests/settings_v002.py"

	#s = Settings()

	#s.load(SETTINGS_GLOBAL)
	#s.load(SETTINGS_USER)

	#s["PROJECT_NAME"] = "JagonUser3"
	#s["projectRoot"] = "V:"
	#s.save()
	#print s["projectRoot"]
