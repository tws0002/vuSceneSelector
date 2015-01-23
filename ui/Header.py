from PyQt4 import QtCore, QtGui
import os
import shutil
import ftplib

# Import Modules
from core import Settings, Index
from ui import style, MenuBar
SETTINGS = Settings.SETTINGS


FOLDER_HEADER_IMAGES = SETTINGS["Graphics_FolderHeaderImages"]
INFOS = SETTINGS["headerInfosShots"]

WARNING_STYLE = """
border: 20px solid rgb(255,0,255);
font-size: 64px;
color: rgb(0,255,0);

background-color: transparent
"""


class Header(QtGui.QWidget):
	def __init__(self, window):
		super(Header, self).__init__(window)
		self.window = window

		# Header Image
		self.image = QtGui.QLabel()
		self.image.setStyleSheet("border: 1px solid " + style.COLOR_BORDER)
		self.image.mousePressEvent = self.imageClicked

		self.warning = QtGui.QLabel("Please Restart")
		self.warning.setStyleSheet(WARNING_STYLE)
		self.warning.setAlignment(QtCore.Qt.AlignCenter)
		self.warning.setVisible(False)

		self.imageLayout = QtGui.QGridLayout()
		self.imageLayout.addWidget(self.image, 0, 0)
		self.imageLayout.addWidget(self.warning, 0, 0)



		self.grpInfo = QtGui.QGroupBox("")
		self.grpInfo.setStyleSheet("padding-top: 0px")
		self.grpInfoLayout = QtGui.QVBoxLayout()
		self.grpInfoLayout.setSpacing(0)
		self.grpInfo.setLayout(self.grpInfoLayout)



		# ShotName: Widgets
		self.descrValueName = QtGui.QLabel()

		# FrameRange: Widgets
		self.descrLabelFrameRange = QtGui.QLabel("FrameRange:")
		self.descrValueFrameHandleStart = QtGui.QLabel()
		self.descrValueFrameRange = QtGui.QLabel()
		self.descrValueFrameHandleEnd = QtGui.QLabel()
		self.descrValueFrameHandleStart.setStyleSheet(style.styleTextGrey)
		self.descrValueFrameHandleEnd.setStyleSheet(style.styleTextGrey)

		# FrameRange: Layout
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.descrLabelFrameRange)
		hbox.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
		hbox.addWidget(self.descrValueFrameHandleStart)
		hbox.addWidget(self.descrValueFrameRange)
		hbox.addWidget(self.descrValueFrameHandleEnd)
		self.grpInfoLayout.addLayout(hbox)


		# Add InfoWidgets
		self.valueWidgets = {}
		for attr in INFOS:
			# Widgets
			label = QtGui.QLabel(attr + ":")
			#label.setStyleSheet("border: 1px solid red")
			valueWidget = QtGui.QLabel("")
			self.valueWidgets[attr] = valueWidget

			hbox = QtGui.QHBoxLayout()
			hbox.addWidget(label)
			hbox.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
			hbox.addWidget(valueWidget)

			# add to Layout
			self.grpInfoLayout.addLayout(hbox)




		# Description Text
		grpDescr = QtGui.QGroupBox("")
		grpDescr.setStyleSheet("padding-top: 0px")
		gridDescr = QtGui.QGridLayout()
		grpDescr.setLayout(gridDescr)

		self.descr = QtGui.QLabel()
		self.descr.setWordWrap(True)

		gridDescr.addWidget(self.descr, 0, 0)
		gridDescr.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding), 3,  1)



		# Main Grid
		self.main_grid = QtGui.QGridLayout()
		#self.main_grid.setSpacing(1)
		self.main_grid.setMargin(0)
		self.setLayout(self.main_grid)
		self.decrIsHidden = False

		self.main_grid.addLayout(self.imageLayout, 0, 0, 3, 1)

		self.main_grid.addWidget(self.descrValueName, 0, 1)
		self.main_grid.addWidget(MenuBar.MenuBar(), 0, 2)
		self.main_grid.addWidget(self.grpInfo, 1, 1, 1, 2)
		self.main_grid.addWidget(grpDescr, 2, 1, 1, 2)







	def setImage(self, selName):
		path = FOLDER_HEADER_IMAGES + selName + ".png"
		if not os.path.exists(path):
			print "updateHeader: ShotThumb not found. " + str(path)
			path = FOLDER_HEADER_IMAGES + "/__default.png"

		img = QtGui.QPixmap(path)
		img = img.scaled(512, 215, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
		self.image.setPixmap(img)



	def setText_Assets(self, selName):
		# Hide/Show
		self.grpInfo.setVisible(False)
		self.descrValueName.setText("<b>" + selName + "</b>")


	def setText_Shots(self, selName):
		# Hide/Show
		self.grpInfo.setVisible(True)

		# ShotName
		self.descrValueName.setText("<b>" + selName + "</b>")

		for attr in INFOS:
			valueWidget = self.valueWidgets[attr]
			valueWidget.setText(Index.getValue(selName, attr))


		# FrameRange
		starthandle = Index.getValue(selName, "startHandle")
		endhandle = Index.getValue(selName, "endHandle")
		startFrame = Index.getValue(selName, "firstFrame")
		endFrame = Index.getValue(selName, "lastFrame")

		# Convert to Ints
		starthandleInt = int(starthandle) if starthandle != "" else 0
		endhandleInt = int(endhandle) if endhandle != "" else 0
		startFrameInt = int(startFrame) if startFrame != "" else 0
		endFrameInt = int(endFrame) if endFrame != "" else 0


		self.descrValueFrameHandleStart.setText("(" + str(startFrameInt - starthandleInt) + ") ")
		self.descrValueFrameRange.setText(startFrame + " - " + endFrame)
		self.descrValueFrameHandleEnd.setText(" (" + str(endFrameInt + endhandleInt) + ")")




	def setText(self, selType, selName):
		if selName == "":
			for label in [	self.descrValueName, self.descrValueNameSchnitt,
							self.descrValueFrameHandleStart, self.descrValueFrameRange, self.descrValueFrameHandleEnd,
							self.descrValueFPS, self.descrValueLens, self.descr]:
				label.setText("")
			return False

		if selType == "Assets":
			self.setText_Assets(selName)
		else:
			self.setText_Shots(selName)
		self.descr.setText(Index.getValue(selName, "Description"))



	def popup_ImageChange(self):
		selName = self.window.selName
		title = "Select image for " + selName

		fileName = QtGui.QFileDialog.getOpenFileName(self, title, "V:", "png's (*.png)")
		if fileName:
			print "Copy!"
			print "Source: " + fileName
			print "Target: " + FOLDER_HEADER_IMAGES + selName + ".png"

			shutil.copy(fileName, FOLDER_HEADER_IMAGES + selName + ".png")
			self.setImage(selName)

			# Connect to FTP
			HOST = "quake"
			PORT = 12021
			ftp = ftplib.FTP()
			ftp.connect(HOST, PORT)
			ftp.login("f009cffa@julianweiss.com", "XhvFnJcvJV3eXW3N")

			# Upload File
			file = open(fileName,'rb')
			ftp.storbinary("STOR " + selName + ".png", file)
			file.close()
			ftp.quit()
			print "Image Uploaded"




	def imageClicked(self, event):
		if SETTINGS["isAdmin"]:
			if event.button() == QtCore.Qt.RightButton:
				self.popup_ImageChange()
