import sqlite3


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

		# Database Vars
		self.conn = None
		self.cursor = None
		self.connected = False



		# Python Dict
		self.tables = {}

	##########################
	##########################
	##						##
	##       Connection     ##
	##						##
	##########################
	##########################

	def connect(self):
		if not self.connected:
			print "Reconnect DB"

			# Local DB
			self.conn = sqlite3.connect(self.fileName, 1)
			self.cursor = self.conn.cursor()

			# Memory DB
			# self.conn = sqlite3.connect(":memory:")
			# self.cursor = self.conn.cursor()
			# self.cursor.execute("ATTACH DATABASE '" + self.fileName +"' AS localDB")
			#self.cursor.execute("CREATE TABLE " + tableName[0] +" AS SELECT * FROM localDB." + tableName[0])

			tables = [tableName[0] for tableName in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]
			for tableName in tables[:2]:
				self.tables[tableName] = {}

				for row in self.cursor.execute("SELECT * FROM " + tableName):
					for i, col in enumerate(self.cursor.description):
						self.tables[tableName][col[0]] = row[i]
			#self.conn.close()

			self.connected = True



	def commit(self):
		self.conn.commit()
		self.conn.close()
		self.connected = False


	def close(self):
		if self.connected:
			self.commit()




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
		return [tableName[0] for tableName in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]

	def getColumns(self, tableName):
		self.connect()

		columns = []
		for col in self.cursor.execute("PRAGMA table_info(" + tableName + ")"):
			columns.append(col[1])
		return columns

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
		self.connect()

		columns = self.getColumns(tableName)
		values = [""] * len(columns)
		values[columns.index("Name")] = name

		self.cursor.execute("INSERT INTO " + tableName + " VALUES ('" + "', '".join(values) + "')")


	def setValue(self, tableName, name, column, value):
		self.connect()

		# Check if Row exists
		oldValueFound = False

		for oldValue in self.cursor.execute("SELECT * FROM " + tableName + " WHERE (name='" + name + "')"):
			oldValueFound = True

		if not oldValueFound:
			self.addRow(tableName, name)

		value = value.replace("'", "")

		#print "UPDATE " + tableName + " SET " + column +" = '" + value + "' WHERE (name='" + name + "')"
		self.cursor.execute("UPDATE " + tableName + " SET " + column +" = '" + value + "' WHERE (name='" + name + "')")


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
