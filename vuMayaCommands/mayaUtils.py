import maya.cmds as cmds

root = "//bigfoot/kroetenlied/060_Software/vuPipeline/"
IMG_NAMING_CONVENTION = root + "Kroetenlied_NamingConvention_v002_vu_small.jpg"
IMG_FOLDERSTRUKTURE = root + "Kroetenlied_FolderStruct_Overview_v002_small.jpg"

def errorWindow_NamingConvention():
	print "Something went wrong...."

	for image in [IMG_NAMING_CONVENTION, IMG_FOLDERSTRUKTURE]:
		cmds.window(title="Read this !!!", sizeable=False)
		cmds.columnLayout()
		cmds.image(image = image)
		cmds.showWindow()