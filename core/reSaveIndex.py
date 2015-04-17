import cPickle as pickle


FILENAME_OLD = "./index_old.p"
FILENAME_NEW = "./Index.p"


"""
# Entity-Template
Entity = {}
Entity["Name"] = ""
Entity["Type"] = ""		# Shot, Asset ?
Entity["Group"] = ""
Entity["Tasks"] = [""]
Entity["Path"] = ""		# ?


# Task-Template
Task = {}
Task["Step"] = "" 		# GEO, RIG, SIM, COMP, ect
Task["Status"] = "" 	# Float or String ?
Task["Todo"] = ""
Task["Artist"] = ""
"""

#oldData = pickle.load( open( FILENAME_OLD, "r" ) )


DATA = {}
DATA["Overview"] = {}
DATA["Overview"]["Types"] = ["Assets", "Shots"]
DATA["Overview"]["Assets"] = {}
DATA["Overview"]["Shots"] = {}
DATA["Overview"]["lastSync"] = "Never!"

DATA["Overview"]["Assets"]["Tasks"] = [("010", "GEO"), ("020", "TEX"), ("030", "RIG"), ("040", "SHD")]
DATA["Overview"]["Shots"]["Tasks"] = [("010", "TRACK"), ("020", "MATTEPAINT"), ("025", "3D"), ("030", "ANIM"), ("040", "SIM"), ("045", "SFS"), ("050", "LIGHT"), ("055", "SLAPCOMP"), ("060", "COMP")]


DATA["Overview"]["Shots"]["Tasks"] = [
											("000", "SOURCE"),
											("010", "DENOISE"),
											("020", "UNDISTORT"),
											("030", "TRACK"),
											("040", "DMP"),
											("050", "3D"),
											("060", "COMP")
											]


DATA["items"] = {}

"""
for Type in DATA["Overview"]["Types"]:
	for name in sorted(oldData[Type].keys()):
		old = oldData[Type][name]

		Entity = {}
		Entity["Type"] = Type
		Entity["Name"] = name
		Entity["Num"] = old["Num"]
		Entity["Code"] = name
		Entity["Group"] = old["grp"]

		Entity["Description"] 	= old["Description"]

		if Type == "Shots":
			Entity["Tags"] 			= old["Tags"]
			Entity["firstFrame"] 	= old["firstFrame"]
			Entity["lastFrame"] 	= old["lastFrame"]
			Entity["startHandle"] 	= old["startHandle"]
			Entity["endHandle"] 	= old["endHandle"]
			Entity["Lens"] 			= old["Lens"]
			Entity["Frames"] 		= old["Frames"]
			Entity["FPS"] 			= old["FPS"]

		# Create Tasks
		Entity["Tasks"] = {}
		for taskNum, taskName in DATA["Overview"][Type]["Tasks"]:
			#task = {}
			#task["Step"] = taskName
			Entity[taskName + "_Status"] = old["status" + taskName]
			Entity[taskName + "_Todo"] = old["todo" + taskName]
			Entity[taskName + "_Artist"] = ""
			#Entity["Tasks"][taskName] = task

		DATA["items"][name] = Entity
"""

DATA = []
newFile = open(FILENAME_NEW, "w")
pickle.dump(DATA, newFile)
newFile.close()




"""
# DEBUG: Check Tasks
for Type in DATA["Overview"]["Types"]:
	for taskNum, taskName, in DATA["Overview"][Type]["Tasks"]:
		print Type, taskNum + "_" + taskName
"""
