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

Settings_User = ""

#####################################################
#####################################################
##
##		Project Settings
##
##

# Project Settings
projectName = '<ProjectName>'
projectRoot = ""


# HelperFolders
_folderPipeline = projectRoot + "/090_Software/Intern"



# Types
Types = ['Assets', 'Shots']

Assets_GroupLabel = 'Group'
Assets_FolderTemplate	= projectRoot + '/045_Assets/%(NUM)s_%(NAME)s/%(TASK_NUM)s_%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_WORK'
Assets_FolderOUT 		= projectRoot + '/045_Assets/%(NUM)s_%(NAME)s/%(TASK_NUM)s_%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_OUT'

Shots_GroupLabel = 'Sequence'
Shots_FolderTemplate	= projectRoot + '/050_Shots/%(TASK_NUM)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_WORK'
Shots_FolderOUT			= projectRoot + '/050_Shots/%(TASK_NUM)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s/%(NAME)s_%(TASK_NAME)s_OUT'


# Tasks
COLOR_ICON_INACTIVE = '#3c3c3c'
COLOR_ICON_WAIT = '#aa6f6f'
COLOR_ICON_RED = '#ff4040'
COLOR_ICON_YELLOW = '#ffe100'
COLOR_ICON_GREENCLEAN = '#00ff00'
COLOR_ICON_GREEN = '#26802b'

STATI = []
STATI += [{"value": "",   "label": "inactive",    "color": COLOR_ICON_INACTIVE}]
STATI += [{"value": "0",  "label": "untouched",   "color": COLOR_ICON_RED}]
STATI += [{"value": "0.5","label": "in progress", "color": COLOR_ICON_YELLOW}]
STATI += [{"value": "1",  "label": "done",        "color": COLOR_ICON_GREEN}]

# TASKS_WITHOUT_ICON
TASKS_WITHOUT_ICON = ['SLAPCOMP', 'COOKIE', 'BS', 'BND']



# SyncMode
syncMode = 'Google'
syncFolder = "/ln/Jagon/090_Software/Intern/vuPipelineOverview_Settings/syncTasks"

# Pickel DatenBank
_folderSceneSelector = "/ln/Dev/017_KroetenliedPipeline/v04/v04_12/vuSceneSelector"


# Time to wait between 2 TimeStamp-Checks
REFRESH_INTERVALL = 0.01


# HEADER_IMG_SHOTS
Graphics_FolderHeaderImages = projectRoot + "/090_Software/Assets/Images/ShotThumbs/"
# ICON
Application_Icon = projectRoot + '/Icon_Jagon.png'

# COLOR_HOVER
COLOR_HOVER = '#953636'
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
MAYA_BATCH = '<folderPipeline>/startMaya.bat'
# EMPTY_SCENE
EMPTY_SCENE = '<folderPipeline>/vuPipelineOverview/vuSceneSelector/emptyScene.mb'
# NUKE_BATCH
NUKE_BATCH = '<folderPipeline>/startNuke9.bat'
# MUDBOX_BATCH
MUDBOX_BATCH = '"C:/ProgrammFiles/AutodeskMudbox2015/mudbox.exe"'
# HOUDINI_BATCH
HOUDINI_BATCH = '<folderPipeline>/startHoudini.bat'



# scanSubFolders
scanSubFolders = False

# fixedSize
fixedSize = False

# showShotTaskStatusIcons
showShotTaskStatusIcons = True


# ADMINS
ADMINS = ['vullmann']
isAdmin = True