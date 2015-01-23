import getpass
import sys

#####################################################
#####################################################
##
##		User Settings
##
##

selType = ''

ShotsGroup = ''
ShotsName = ''
ShotsTask = ''
ShotsScene = ''

AssetsGroup = ''
AssetsName = ''
AssetsTask = ''
AssetsScene = ''

UI_mainWindow = ''
UI_splitterSceneToDo = ''
UI_splitterLists = ''
UI_splitterVertical = ''

Favorites = []




#####################################################
#####################################################
##
##		Project Settings
##
##

# Project Settings
projectName = 'WirSindDieFlut'

projectRoot = 'F:'


# HelperFolders
_folderSoftware = projectRoot + "/070_Software/_Tools"
_folderPipeline = projectRoot + "/070_Software/_Tools"

Settings_User = _folderPipeline + '/vuSceneSelector_Settings/user_' + getpass.getuser() + '.py'

# Types
Types = ['Assets', 'Shots']

Assets_GroupLabel = 'Group'
Assets_FolderTemplate = projectRoot + '/030_ASSETS/%(NUM)s_%(NAME)s/%(TASK_NUM)s_%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_WORK'
Assets_FolderOUT = projectRoot + '/030_ASSETS/%(NUM)s_%(NAME)s/%(TASK_NUM)s_%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_OUT'

Shots_GroupLabel = 'Sequence'
Shots_FolderTemplate = projectRoot + '/040_SHOTS/%(TASK_NUM)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_WORK'
Shots_FolderOUT = projectRoot + '/040_SHOTS/%(TASK_NUM)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_OUT'



showOpenFootage = True
Shots_FolderOUT = projectRoot + '/040_SHOTS/%(TASK_NUM)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_OUT'


# Tasks
COLOR_ICON_INACTIVE = '#3c3c3c'
COLOR_ICON_WAIT = '#aa6f6f'
COLOR_ICON_RED = '#ff4040'
COLOR_ICON_YELLOW = '#ffe100'
COLOR_ICON_GREENCLEAN = '#00ff00'
COLOR_ICON_GREEN = '#26802b'
COLOR_ICON_REVIEW = '#0d8de7'

STATI = []
STATI += [{"value": "",   "label": "inactive",		"color": COLOR_ICON_INACTIVE}]
STATI += [{"value": "0",  "label": "untouched",		"color": COLOR_ICON_RED}]
STATI += [{"value": "0.5","label": "in progress",	"color": COLOR_ICON_YELLOW}]
STATI += [{"value": "0.75","label": "review", 		"color": COLOR_ICON_REVIEW}]
STATI += [{"value": "1",  "label": "done",			"color": COLOR_ICON_GREEN}]

# TASKS_WITHOUT_ICON
TASKS_WITHOUT_ICON = ['COOKIE', 'BS', 'BND']



###########################
#
#	Sync
#
#

# SyncMode
syncMode = 'Google'
syncFolder = _folderPipeline + '/vuSceneSelector_Settings/syncTasks'
syncGoogleSpreadSheet = "0Am0FadQHMJp1dFhCRVhkUjFRSDlyTkUzTkRZWVN2dmc"

headerInfosShots = ["KameraTyp", "ISO", "FPS", "Optik"]

# Time to wait between 2 TimeStamp-Checks
REFRESH_INTERVALL = 0.01



###########################
#
#	GRAPHICS
#
#

# HEADER_IMG_SHOTS
Graphics_FolderHeaderImages = "F:/070_SOFTWARE/data/ShotThumbs/"
# ICON
Application_Icon = 'F:/070_SOFTWARE/data/Icons/Icon_WSDF.png'

# COLOR_HOVER
COLOR_HOVER = '#1c6388'
# COLOR_ERROR_EMPTYLIST
COLOR_ERROR_EMPTYLIST = '#cc4747'

# COLOR_BACKGROUND
COLOR_BACKGROUND = '#444444'
# COLOR_SELECTION
COLOR_SELECTION = '#1c6388'
# COLOR_TEXT
COLOR_TEXT = '#c8c8c8'
# COLOR_TEXT_GREY
COLOR_TEXT_GREY = '#787878'
# COLOR_BORDER
COLOR_BORDER = '#272727'
# COLOR_LIST
COLOR_LIST = '#333333'





# MAYA_BATCH
MAYA_BATCH = _folderPipeline + '/startMaya.bat'
# EMPTY_SCENE
EMPTY_SCENE = _folderPipeline + '/vuPipelineOverview/vuSceneSelector/emptyScene.mb'
# NUKE_BATCH
NUKE_BATCH = _folderPipeline + '/startNuke9.bat'
# MUDBOX_BATCH
MUDBOX_BATCH = '"C:/ProgrammFiles/AutodeskMudbox2015/mudbox.exe"'
# HOUDINI_BATCH
HOUDINI_BATCH = _folderPipeline + '/startHoudini13.bat'
SYNTHEYES_BATCH = _folderPipeline + '/startSynthEyes.bat'




# scanSubFolders
scanSubFolders = False

# fixedSize
fixedSize = False

# showShotTaskStatusIcons
showShotTaskStatusIcons = True



# ADMINS
ADMINS = ['vullmann', 'plames', "mkeller"]
isAdmin = getpass.getuser() in ADMINS
