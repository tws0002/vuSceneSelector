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
projectName = 'Kroetenlied'

projectRoot = 'N:'


# HelperFolders
_folderSoftware = projectRoot + "/060_Software"
_folderPipeline = projectRoot + "/060_Software/Kroetenlied_Pipeline"

Settings_User = _folderPipeline + '/vuSceneSelector_Settings/user_' + getpass.getuser() + '.py'

# Types
Types = ['Assets', 'Photoscan', 'Shots']

Asset_FolderTemplate		= projectRoot + "/045_Production_Film/3D/ASSETS/Charakter/%(NUM)s_%(NAME)s/%(TASK_NUM)s_%(CODE)s_%(TASK_NAME)s"
Shot_FolderTemplate		= projectRoot + "/045_Production_Film/3D/SHOTS/%(TASK_NUM)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s"

Asset_FolderOUT			= Asset_FolderTemplate		+ "/%(CODE)s_%(TASK_NAME)s_OUT"
Shot_FolderOUT			= Shot_FolderTemplate		+ "/%(CODE)s_%(TASK_NAME)s_PLAYBLAST"


# Tasks
COLOR_ICON_INACTIVE = '#3c3c3c'
COLOR_ICON_WAIT = '#aa6f6f'
COLOR_ICON_RED = '#ff4040'
COLOR_ICON_YELLOW = '#ffe100'
COLOR_ICON_GREENCLEAN = '#00ff00'
COLOR_ICON_GREEN = '#26802b'

STATI = []
STATI += [{"value": "hld", "label": "On Hold", 			"color": COLOR_ICON_INACTIVE}]
STATI += [{"value": "wtg", "label": "Waiting to Start", "color": COLOR_ICON_WAIT}]
STATI += [{"value": "rdy", "label": "Ready to Start",   "color": COLOR_ICON_RED}]
STATI += [{"value": "ip",  "label": "In Progress",      "color": COLOR_ICON_YELLOW}]
STATI += [{"value": "rev", "label": "Pending Review",   "color": COLOR_ICON_GREENCLEAN}]
STATI += [{"value": "fin", "label": "Final",            "color": COLOR_ICON_GREEN}]


# TASKS_WITHOUT_ICON
TASKS_WITHOUT_ICON = ['SLAPCOMP', 'COOKIE', 'BS', 'BND']



###########################
#
#	Sync
#
#

# SyncMode
syncMode = 'Shotgun'
syncFolder = _folderPipeline + '/vuSceneSelector_Settings/syncTasks'

# Time to wait between 2 TimeStamp-Checks
REFRESH_INTERVALL = 0.01



###########################
#
#	GRAPHICS
#
#

# HEADER_IMG_SHOTS
Graphics_FolderHeaderImages = _folderSoftware + '/Assets/Images/ShotThumbs/'
# ICON
Application_Icon = 'N:/060_Software/Kroetenlied_Pipeline/graphics/Icons/Kroetenlied_Icon.ico'

# COLOR_HOVER
#COLOR_HOVER = '#953636'
COLOR_HOVER = '#4d805e'
# COLOR_ERROR_EMPTYLIST
COLOR_ERROR_EMPTYLIST = '#cc4747'

# COLOR_BACKGROUND
COLOR_BACKGROUND = '#444444'
# COLOR_SELECTION
COLOR_SELECTION = COLOR_HOVER
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
EMPTY_SCENE = _folderPipeline + '/vuSceneSelector/_ProjectSettings/emptyScene.mb'
# NUKE_BATCH
NUKE_BATCH = _folderPipeline + '/startNuke9.bat'
# MUDBOX_BATCH
MUDBOX_BATCH = '"C:/ProgrammFiles/AutodeskMudbox2015/mudbox.exe"'
# HOUDINI_BATCH
HOUDINI_BATCH = _folderPipeline + '/startHoudini.bat'



# scanSubFolders
scanSubFolders = False

# fixedSize
fixedSize = False

# showShotTaskStatusIcons
showShotTaskStatusIcons = True



# ADMINS
ADMINS = ['vullmann', 'ksaleh', 'slanger']

isAdmin = getpass.getuser() in ADMINS
