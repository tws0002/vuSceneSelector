import sqlite3
import cPickle as pickle
import os



ERROR = True
INFO = False
DEBUG = False

def printDebug(msg):
	if DEBUG:
		print "[Debug] " + str(msg)

def printInfo(msg):
	if INFO:
		print "[Info] " + str(msg)

def printError(msg):
	if ERROR:
		print "[Error] " + str(msg)


"""
def getFilter(filterDict):
	filterStr
	" WHERE (" +  + ")"
	return " AND ".join(filters)
"""




class Database(object):
	def __init__(self, fileName):
		self.fileName = fileName
		self.fileNamePickle = os.path.splitext(self.fileName)[0] + ".p"

		# Database Vars
		self.conn = None
		self.cursor = None
		self.connected = False
		self.loaded = False



		# Python Dict
		self.tables = {}

	##########################
	##########################
	##						##
	##       Connection     ##
	##						##
	##########################
	##########################

	def connectDatabase(self):
		if not self.connected:
			self.connected = True
			print "Reconnect DB"

			# Local DB
			self.conn = sqlite3.connect(self.fileName, 1)
			self.cursor = self.conn.cursor()


			# Create Python Dict for ReadAccess-Speed
			tables = [tableName[0] for tableName in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]
			for tableName in tables:
				self.tables[tableName] = {}

				for row in self.cursor.execute("SELECT * FROM " + tableName):

					newItem = {}
					for i, col in enumerate(self.cursor.description):
						newItem[col[0]] = row[i]
					self.tables[tableName][newItem["Name"]] = newItem



	def connectPickle(self):
		if not os.path.isfile(self.fileNamePickle):
			print "ERROR", "PickleFile not found"
			return False

		self.tables = pickle.load( open( self.fileNamePickle, "r" ) )
		return True


	def connect(self, force=False):
		self.connectDatabase()
		return True
		"""
		if force:
			if self.connected:
				self.close()


		if os.stat(self.fileNamePickle).st_mtime < os.stat(self.fileName).st_mtime or force:
			print "Reload Database"
			self.connectDatabase()
			self.commit(False)
			self.connectPickle()
		else:
			self.connectPickle()

		"""


	def closeConn(self):
		self.conn.close()
		self.connected = False


	def commit(self, close=True):
		self.conn.commit()
		if close:
			self.closeConn()

		# Save to Pickle
		print "Save DB to Pickle"
		pFile = open(self.fileNamePickle, "w")
		pickle.dump(self.tables, pFile)
		pFile.close()


	def close(self, save=True):
		if self.connected:
			if save:
				self.commit()
			else:
				self.closeConn()




	def createTable(self, tableName, columns):
		self.connect()

		cmd = "CREATE TABLE " + tableName
		cmd += " (" + ", ".join([row + " text" for row in columns]) + ")"

		self.cursor.execute(cmd)



	def deleteTable(self, tableName):
		self.connect()

		self.cursor.execute("DROP TABLE IF EXISTS " + tableName)


	def reCreateTable(self, tableName, columns):
		self.deleteTable(tableName)
		self.createTable(tableName, columns)

	##########################
	##########################
	##						##
	##       getValues      ##
	##						##
	##########################
	##########################

	def getTables(self):
		self.connect()
		return self.tables.keys()

	def getColumns(self, tableName):
		self.connect()

		#columns = []
		#for col in self.cursor.execute("PRAGMA table_info(" + tableName + ")"):
		#	columns.append(col[1])
		#return columns

		table = self.tables[tableName]
		return table[table.keys()[0]].keys()

	def getAllValues(self, tableName):
		self.connect()

		values = []
		for row in self.cursor.execute("SELECT * from " + tableName):
			values.append(row)
		return values



	##########################
	##########################
	##						##
	##       setValues      ##
	##						##
	##########################
	##########################

	def addRow(self, tableName, name):
		print "Add Row", tableName, name
		self.connect()

		columns = self.getColumns(tableName)
		values = [""] * len(columns)
		values[columns.index("Name")+1] = name # ???
		print values

		self.cursor.execute("INSERT INTO " + tableName + " VALUES ('" + "', '".join(values) + "')")
		self.tables[tableName][name] = {}
		self.tables[tableName][name]["Name"] = name

	def setValue(self, tableName, name, column, value, commit=True):
		self.connect(True)

		# Check if Row exists
		if not name in self.tables[tableName]:
			self.addRow(tableName, name)


		value = value.replace("'", "")

		# Save Values
		self.tables[tableName][name][column] = value
		self.cursor.execute("UPDATE " + tableName + " SET " + column +" = '" + value + "' WHERE (name='" + name + "')")

		if commit:
			self.commit()


	##########################
	##########################
	##						##
	##       getValues      ##
	##						##
	##########################
	##########################

	def getValues(self, tableName=None, column="", Filter=""):
		self.connect()

		if not tableName:
			tableName = self.getTables()[0]
		return [val[0] for val in self.cursor.execute("SELECT " + column + " FROM " + tableName + Filter)]


	def getValue(self, tableName=None, name="", column=""):
		self.connect()

		# Get Tables to look into
		if not tableName:
			tableName = self.getTables()[0]

		for val in self.cursor.execute("SELECT " + column + " FROM " + tableName + " WHERE name='" + name + "' LIMIT 1"):
			return val[0]




	def getUniqueValues(self, tableName, column=""):
		self.connect()

		return [grp[0] for grp in self.cursor.execute("SELECT DISTINCT " + column + " FROM " + tableName)]