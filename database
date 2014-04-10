import sqlite3

class database(object):

	def createDBIpAddress(self):
		self.engine = sqlite3.connect(':memory:')
		self.engine.execute('create table ip_list_table (id INTEGER NOT NULL PRIMARY KEY,ip_list_field0 VARCHAR(30), ip_list_field1 VARCHAR(30))');
	
	def createDBStatus(self):
		self.enginemsg = sqlite3.connect(':memory:', check_same_thread = False)
		self.enginemsg.execute('create table status_list_table (ids INTEGER NOT NULL PRIMARY KEY,status_list_field0 VARCHAR(30), status_list_field1 VARCHAR(30))');

	def createDBAppName(self):
		self.engineapp = sqlite3.connect(':memory:', check_same_thread = False)
		self.engineapp.execute('create table app_list_table (ids INTEGER NOT NULL PRIMARY KEY,app_list_field0 VARCHAR(30), app_list_field1 VARCHAR(30))');
	
	def createDBPkg(self):
		self.enginepkg = sqlite3.connect(':memory:', check_same_thread = False)
		self.enginepkg.execute('create table pkg_list_table (ids INTEGER NOT NULL PRIMARY KEY,pkg_list_field0 VARCHAR(30), pkg_list_field1 VARCHAR(30))');

	def setIpAddressTable(self):
		result =self.engine.execute('select * from ip_list_table');
		self.ipAddressResult=result	

	def setStatusTable(self):
		result =self.enginemsg.execute('select * from status_list_table');
		self.statusResult=result
	def setPkgTable(self):
		result =self.enginepkg.execute('select * from pkg_list_table');
		self.pkgResult=result

	def addNewRow(self,col0,col1):
		query = 'INSERT INTO ip_list_table (ip_list_field0, ip_list_field1) VALUES ("{0}", "{1}")'.format(col0,col1)
		self.engine.execute(query)
				
	def addNewStatusRow(self,col_status0,col_status1):
		query = 'INSERT INTO status_list_table (status_list_field0, status_list_field1) VALUES ("{0}", "{1}")'.format(col_status0,col_status1)
		self.enginemsg.execute(query)

	def addNewAppRow(self,col_app0,col_app1):
		query = 'INSERT INTO app_list_table (app_list_field0, app_list_field1) VALUES ("{0}", "{1}")'.format(col_app0,col_app1)
		self.engineapp.execute(query)

	def addNewPkgRow(self,col_pkg0,col_pkg1):
		query = 'INSERT INTO pkg_list_table (pkg_list_field0, pkg_list_field1) VALUES ("{0}", "{1}")'.format(col_pkg0,col_pkg1)
		self.enginepkg.execute(query)

	def deleteAllRow(self):
		query1 = 'DELETE FROM ip_list_table'
		self.engine.execute(query1)

	def deleteAllStatusRow(self):
		query1 = 'DELETE FROM status_list_table'
		self.enginemsg.execute(query1)
	
	def getIpAddressTable(self):
		return self.ipAddressResult

	def getStatusTable(self):
		return self.statusResult
	def getPkgTable(self):
		return self.pkgResult
