tasksNums = {}
tasksAll = None
tasksNames3D = []
tasksNames3D_Names = []
taskNamesPhotoscan = []
tasksNamesShots = []
tasksNamesShots_Names = []


tasksNames3D.append(("010", "GEO"))
tasksNames3D.append(("015", "BS"))
tasksNames3D.append(("020", "TEX"))
tasksNames3D.append(("030", "RIG"))
tasksNames3D.append(("040", "COOKIE"))
tasksNames3D.append(("050", "BND"))
tasksNames3D.append(("060", "SHD"))

taskNamesPhotoscan.append(("010", "FOTOS"))
taskNamesPhotoscan.append(("020", "MASKS"))
taskNamesPhotoscan.append(("030", "PHOTOSCAN"))
taskNamesPhotoscan.append(("040", "CLEANUP"))
taskNamesPhotoscan.append(("050", "SHD"))

tasksNamesShots.append(("010", "ANIM"))
tasksNamesShots.append(("020", "LIGHT"))
tasksNamesShots.append(("030", "COMP"))


for taskNum, task in tasksNames3D:
	tasksNames3D_Names.append(task)

#for taskNum, task in taskNamesPhotoscan:
#	taskAll.append(taskNum + "_" + task)

for taskNum, task in tasksNamesShots:
	tasksNamesShots_Names.append(task)

# Fill all Arrays/Dicts
for num, task in (tasksNames3D + tasksNamesShots):		#taskNamesPhotoscan
	tasksNums[task] = num


def getTaskNum(name):
	return tasksNums[name]