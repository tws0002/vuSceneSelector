from PyQt4 import QtCore, QtGui
import sys


class ListTemplate(QtGui.QListWidget):
	def __init__(self):
		super(ListTemplate, self).__init__()
		self.interactive = True
		self.connect(self, QtCore.SIGNAL("itemSelectionChanged()"), self.itemSelectionChanged)

	def setItems(self, items):
		self.interactive = False
		self.clear()
		self.addItems(items)
		self.interactive = True
		return True

	def setSelection2(self, name, setDefault=True):
		self.setCurrentRow(-1)

		if not name:
			return False
		item = self.findItems(name, QtCore.Qt.MatchExactly)

		self.interactive = False
		if item:
			item[0].setSelected(True)

		if setDefault:
			self.setCurrentRow(0)

		self.interactive = True
		return True




	def itemSelectionChanged_User(self):
		print "Override this!"

	def itemSelectionChanged(self):
		if not self.interactive:
			return True
		return self.itemSelectionChanged_User()




class TableItemTemplate(QtGui.QTableWidgetItem):
	def __init__(self, label):
		super(TableItemTemplate, self).__init__(label)


	# TODO:
	# Make Row-Hover-Effect
	def enterEvent(self, event):	print "enterEvent"
	def leaveEvent(self, event):	print "leaveEvent"


class TableTemplate(QtGui.QTableWidget):
	def __init__(self, window):
		super(TableTemplate, self).__init__()

		self.window = window
		self.sortOrder = 0
		self.interactive = True
		self.maximised = False

		self.verticalScrollBarVisible = False
		self.horizontalScrollBarVisible = False

		# Table Style
		self.verticalHeader().setVisible(False)
		self.horizontalHeader().setVisible(False)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setShowGrid(False)

		self.installEventFilter(self)
		self.connect(self, QtCore.SIGNAL("currentCellChanged(int, int, int, int)"), self.currentCellChanged)



	def resizeRows(self):
		"Rezise Rows after adding some Content"
		self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
		for r in range(self.rowCount()):
			self.setRowHeight(r, 17)

	def resizeColumns(self, auto=False):
		self.resizeColumnsToContents()
		self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)



	def setSelection2(self, value):
		for i in range(self.rowCount()):
			if self.item(i, 0).text() == value:
				self.interactive = False
				self.setCurrentCell(i, 0)
				self.interactive = True
				return True

		self.setCurrentCell(0, 0)
		return False


	def eventFilter(self, obj, event):
		if obj == self:
			if event.type() == event.KeyPress:
				if event.key() in [	QtCore.Qt.Key_Left,
									QtCore.Qt.Key_Right,
									QtCore.Qt.Key_Tab
									]:
					self.window.keyPressEvent(event)
					event.accept()
					return True
		return self.window.eventFilter(obj, event) if self.window else False



	def itemSelectionChanged_User(self):
		print "Override this!"

	def currentCellChanged(self, row, col, preRow, preCol):
		if not self.interactive:
			return
		return self.itemSelectionChanged_User()

	def resizeEvent(self, event):
		super(TableTemplate, self).resizeEvent(event)
		self.verticalScrollBarVisible = self.verticalScrollBar().isVisible()
		self.horizontalScrollBarVisible = self.horizontalScrollBar().isVisible()



class HeaderItemSort(QtGui.QLabel):
	"""QLabel, with Sorting Indicator"""
	def __init__(self, text):
		super(HeaderItemSort, self).__init__(text)
		self.text = text
		self.state = None
		self.setCursor(QtCore.Qt.PointingHandCursor)

	def update(self):
		text = self.text
		if self.state != None:
			text += " " + [u"\u25BC", u"\u25B2"][self.state]
		self.setText(text)

	def toogle(self, state):
		self.state = state
		self.update()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	w = ScrollIndicator(None)
	w.show()
	app.exec_()