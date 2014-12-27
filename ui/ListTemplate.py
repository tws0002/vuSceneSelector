from PyQt4 import QtCore, QtGui


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

	def setSelection2(self, name):
		item = self.findItems(name, QtCore.Qt.MatchExactly)

		self.interactive = False
		if item:
			item[0].setSelected(True)
		else:
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

				elif event.key() == QtCore.Qt.Key_Space:
					self.keyPress_Maximise(event)
					event.accept()
					return True
		return self.window.eventFilter(obj, event) if self.window else False



	def keyPress_Maximise(self, event):
		parent = QtGui.QApplication.instance().activeWindow()

		print str(parent.sizeHint().width())


		if not self.maximised:
			self.maximised = True
			parent.labelShotInfo.hide()
			parent.grpInfo.hide()
			parent.grpDescr.hide()
			parent.main_grid.addWidget(parent.header, 0, 0 ,3, 2)

			# Resize
			self.origWidth = parent.width()
			#parent.updateGeometry()
			#parent.sizeHint().width()
			#parent.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)
			#parent.resize(0, 0)


		else:
			self.maximised = False
			parent.labelShotInfo.show()
			parent.grpInfo.show()
			parent.grpDescr.show()
			parent.main_grid.addWidget(parent.header, 0, 0 ,3, 1)

			parent.resize(self.origWidth, parent.height())
			#parent.layout().setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)




		return
		if not self.maximised:
			self.maximised = True
			parent.mainLayout.removeWidget(parent.mainWidget)
			parent.mainLayout.addWidget(self)

		else:
			self.maximised = False
			parent.mainLayout.removeWidget(self)
			parent.mainLayout.addWidget(parent.mainWidget)


	def itemSelectionChanged_User(self):
		print "Override this!"

	def currentCellChanged(self, row, col, preRow, preCol):
		if not self.interactive:
			return
		return self.itemSelectionChanged_User()