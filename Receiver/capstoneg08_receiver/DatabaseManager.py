# -*- coding: utf-8 -*-
import pyodbc

class DatabaseManager():
    def __init__(self, databaseString):
        self.databaseConn = pyodbc.connect(databaseString)
        self.cursor = self.databaseConn.cursor()
    
    def storeData(self, volt, curr):   
        # store the data sample in the imports table
        sql = "INSERT INTO imports (Volt, Curr, Processed) VALUES (?, ?, ?);"
        self.cursor.execute(sql, volt, curr, 0)
        self.databaseConn.commit()
        
    def deleteTopRow(self, numRow):
        # delete the top numRow rows
        sql = "DELETE TOP (?) FROM imports;"
        self.cursor.execute(sql, numRow)
        self.databaseConn.commit()
        
        # get the last inserted row ImID
        sql = "SELECT MAX (ImID) FROM imports"
        self.cursor.execute(sql)
        lastRowInserted = self.cursor.fetchone()[0]
        if lastRowInserted is None:
            lastRowInserted = 0
        self.databaseConn.commit()
        
        # get the number to reseed the ImID to
        rowToReseedTo = lastRowInserted - numRow
        if rowToReseedTo < 0:
            rowToReseedTo = 0
      
        # reseed the ImID
        sql = "DBCC CHECKIDENT ('[imports]', RESEED, " +  str(rowToReseedTo) + ");"
        self.cursor.execute(sql) 
        self.databaseConn.commit()
        return
    
#===============================================================
# The classes beyond this point are only used for testing.
#===============================================================
        
    def createImportsTable(self):
        print("Creating Test Table.")
        self.cursor.execute('''
                   CREATE TABLE imports(
	                       ImID BIGINT IDENTITY NOT NULL,
	                       Instant DATETIME2 DEFAULT CURRENT_TIMESTAMP NOT NULL,
	                       Volt NVARCHAR(255) NOT NULL,
	                       Curr NVARCHAR(255) NOT NULL,
	                       Processed BIT DEFAULT 0 NOT NULL,
	                       PRIMARY KEY (ImID)
                   );''')
        self.databaseConn.commit() 

    def deleteImportsTable(self):
        # delete the all rows in the imports table
        self.cursor.execute('''
                   DELETE FROM imports;
                   DBCC CHECKIDENT ('[imports]', RESEED, 0);
                   ''')
        self.databaseConn.commit()
        
    def dropImportsTable(self):
        # delete the entire imports table
        self.cursor.execute('''
                   DROP TABLE imports;
                   ''')
        self.databaseConn.commit()
    
    def printImportsTable(self):
        # print the contents of the imports table
        sql = "SELECT * FROM imports"
        self.cursor.execute(sql)
        for row in self.cursor:
            print (row)
        self.databaseConn.commit()
