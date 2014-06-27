import maya.cmds as cmds


DROP_IMG = "N:/060_Software/vuPipeline/PythonModules/SceneSelector/DropHere_v001_vu.png"

##############################################################################################
#
#
#		Window
#
import sys
from PySide import QtGui, QtCore


class dropWindow(QtGui.QLabel):

    def __init__(self):
        super(dropWindow, self).__init__()

        self.sceneFile = None

        self.setAcceptDrops(True)
        self.setPixmap(QtGui.QPixmap(DROP_IMG))
        self.setFixedSize(256, 256)
        self.setWindowTitle('Simple Drag & Drop')
        self.show()

    def dragEnterEvent(self, e):
        e.accept()
        print e.mimeData()
        return


        if e.mimeData().hasFormat('text/plain'):
            self.sceneFile = e.mimeData().text()
        else:
            e.ignore()

    def dropEvent(self, e):
        if self.sceneFile:
            cmds.file( self.sceneFile, o=True)


#ex = dropWindow()



import win32clipboard

# set clipboard data
win32clipboard.OpenClipboard()
win32clipboard.SetClipboardText('testing 123')
win32clipboard.CloseClipboard()

# get clipboard data
import win32clipboard
win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
print data


##############################################################################################
#
#
#		Main
#

#def tmp():
#	dropWindow()
import maya.cmds as cmds

import sys
sys.path.append("//bigfoot/kroetenlied/060_Software/vuPipeline/PythonModules/_DEV")
from SceneSelector import core

def SceneDragAndDrop():
    print ("-"*10 + "\n") * 10

    # Load Data
    values = core.loadData(None, True)
    sceneFile = values["OpenScene"]

    if sceneFile:
        # Open Scene
        print "Open: " + sceneFile
        cmds.file(sceneFile, o=True, f=True)

        # Store Data
        values["OpenScene"] = ""
        core.storeData(values)


def activateSceneDragAndDrop():
    cmds.scriptJob(ct=["readingFile", SceneDragAndDrop])


activateSceneDragAndDrop()