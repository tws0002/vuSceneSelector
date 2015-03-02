from PyQt4 import QtCore, QtGui

from core import Settings
SETTINGS = Settings.SETTINGS








class SearchBar(QtGui.QLineEdit):
	def __init__(self, parent=None):
		super(SearchBar, self).__init__(parent)
		self.parent = parent

		self.setToolTip("Search for Shots by Name")

	def setSelection2(self, name, setDefault=None):
		if not name:
			self.clear()
			self.setStyleSheet("")


	def focusInEvent(self, event):
		self.setStyleSheet("background: " + SETTINGS["COLOR_HOVER"])
		self.parent.changeGroup(self)





	# Dummyes to appear like a QListWidget
	def setCurrentRow(self, num):
		self.setStyleSheet("background: " + SETTINGS["COLOR_HOVER"])

	def count(self):
		if self.hasFocus():
			return 1
		return len(str(self.text()))

	def selectedItems(self):
		return [None] * self.count()

	def currentItem(self):
		return self



