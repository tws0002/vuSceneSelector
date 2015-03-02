from PyQt4 import QtCore, QtGui
import os
import datetime


# Import Modules
if __name__ != '__main__':
	from core import Settings, History
	from ui import style, ListTemplate
	SETTINGS = Settings.SETTINGS


COLUMNS = ["date", "type", "shot", "task", "user", "value"]



	#                       #
	#                       #
#################################
	#                       #
	#      TableClass       #
	#                       #
#################################
	#                       #
	#                       #

class TableHistory(ListTemplate.TableTemplate):
	def __init__(self, window=None):
		super(TableHistory, self).__init__(window)
		self.window = window

		# Table Settings
		self.setColumnCount(len(COLUMNS))
		self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


		self.setColumnWidth(0, 110)
		self.setColumnWidth(1, 40)
		self.setColumnWidth(2, 60)
		self.setColumnWidth(3, 50)
		header = self.horizontalHeader()
		header.setStretchLastSection(True)

		#header.setResizeMode(QHeaderView.Stretch)
		#self.resizeRows()



		# General Settings:
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.mouseClickRight)

		self.setStyleSheet("background: #4d483d")
		self.refreshHistory()


	def refreshHistory(self):
		data = History.HISTORY.readData()

		self.clear()
		self.setRowCount(len(data))

		for r, dataItem in enumerate(data):

			# StatusLabel
			if dataItem["type"] == "Status":
				for status in SETTINGS["STATI"]:
					if status["value"] == dataItem["value"]:
						dataItem["value"] = status["label"]

			for c, key in enumerate(COLUMNS):
				value = dataItem[key]
				item = QtGui.QTableWidgetItem(value)
				item.setFlags(QtCore.Qt.ItemIsEnabled)	#ReadOnly
				self.setItem(r, c, item)

		self.resizeRows(header=False)
		return True



	#                       #
	#                       #
#################################
	#                       #
	#      Context-Menu     #
	#                       #
#################################
	#                       #
	#                       #
	def listCtxt_Refresh(self):
		self.refreshHistory()


	def ctxtShowMenue(self, QPos):
		self.ctxtMenue= QtGui.QMenu()
		self.ctxtMenue.setStyleSheet(style.STYLE)

		# Refresh
		ctxt_refreshList = self.ctxtMenue.addAction("Refresh List")
		ctxt_refreshList.setIconVisibleInMenu(True)
		ctxt_refreshList.setShortcut('F5')
		self.connect(ctxt_refreshList, QtCore.SIGNAL("triggered()"), self.listCtxt_Refresh)

		parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))
		self.ctxtMenue.move(parentPosition + QPos)
		self.ctxtMenue.show()




##############################################################################################
#
#
#		Mouse and Keyboard
#

	def mouseClickRight(self, QPos):
		self.ctxtShowMenue(QPos)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_F5:
			self.refreshHistory()




if __name__ == '__main__':
	pass


