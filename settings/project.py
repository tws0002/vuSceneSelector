import getpass

PROJECT_NAME = "Kroetenlied"

# Folders
projectRoot = "//bigfoot/kroetenlied"
folderPipeline = projectRoot + "/060_Software/vuPipeline"

folder3D  = projectRoot + "/045_Production_Film/3D"
FOLDER_ASSETS = folder3D + "/ASSETS/Charakter"
FOLDER_SHOTS  = folder3D + "/SHOTS"


# Items:
import sys
sys.path.append(folderPipeline)
import Kroetenlied.klAssets as Assets
import Kroetenlied.klTasks  as Tasks
import Kroetenlied.klShots  as Shots
ASSET_GROUPS = ["Heros", "MusikKroeten"]



UI_STYLE = "dark"		# Avalible: [dark, light]
EMPTY_SCENE   = folderPipeline + "/vuSceneSelector/emptyScene.mb"
USER_SETTINGS = folderPipeline + "/vuSceneSelector/settings/" + "userSettings_" + getpass.getuser()


HEADER_IMG = folderPipeline + "/Graphics/SceneSelector_Header.png"
MAYA_BATCH = folderPipeline + "/startMaya.bat"
