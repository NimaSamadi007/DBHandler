import sqlite3
import numpy as np
import re

class DBHandler:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cur = self.db.cursor()

    # read all columnss include the first column
    def ReadData(self, tableName):  
        sql = "SELECT * FROM " + tableName
        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.db.commit()
        return data

    # read parameters such as sampling frequency. except first column ( id ) all columns returned
    def ReadParameters(self, tableName):
        sql = "SELECT * FROM " + tableName
        self.cur.execute(sql)
        data = self.cur.fetchall()
        columns = [des[0] for des in self.cur.description]
        self.db.commit()
        return dict(zip(columns[1:],data[-1][1:]))

    #read one column, none NULL value Returned
    def ReadColumn(self, tableName, column):
        self.cur.execute("SELECT " + column + " FROM " + tableName + " WHERE " + column + " NOT NULL")
        rows = self.cur.fetchall()
        col = [row[0] for row in rows]
        self.db.commit()
        return np.array(list(map(float, col)))

    # read last row and returned column names which corresponding row value is 1
    def ReadChannelLabels(self, tableName):
        self.cur.execute("SELECT * FROM " + tableName )
        rows = self.cur.fetchall()
        lastCol = rows[-1]
        columns = [des[0] for des in self.cur.description]
        output = []
        for i in range(1, len(columns)):
            if lastCol[i] == '1' or lastCol[i] == 1:
                output.append(columns[i])
        self.db.commit()
        return output

    # reading channel coordinates
    def ReadChannelCoordinates(self, tableName):
        channels = []
        coord = []
        self.cur.execute("SELECT * FROM " + tableName )
        data = (self.cur.fetchall())[-1]
        columns = [des[0] for des in self.cur.description]
        num = 0
        for i in range(1, len(columns)):
            if (i - 1) % 3 == 0:
                label = columns[i]
                val = re.search("[Pp]osition", label)
                channels.append(label[0: (val.span())[0]])
                X = data[i]
            elif (i - 1) % 3 == 1:
                Y = data[i]                
            elif (i - 1) % 3 == 2:
                Z = data[i]
            if num == 2:
                num = 0
                coord.append([X, Y, Z])
            else:
                num += 1
        return dict(zip(channels, coord))

    # convert data to numpy, except first couluimn
    @staticmethod
    def Data2Numpy(data):
        return np.array([list(map(float, list(row[1:]))) for row in data])

    # create table, 'successful' also had to be
    def CreateTable(self, tableName, columnName):
        self.cur.execute("DROP TABLE IF EXISTS " + tableName)
        self.cur.execute("CREATE TABLE " + tableName +  ' (id INTEGER PRIMARY KEY, ' + ' VARCHAR(255), '.join(columnName) + ' VARCHAR(255))')
        self.db.commit()

    # writing matrix, columnName has 3 element
    def WriteMatrix(self, tableName, columnName, matrix):
        if len(columnName) == 3:
            columnSQL = '(' + ', '.join(columnName[0:2]) + ')'
            # M, N values:
            M, N = matrix.shape
            self.cur.execute( """ INSERT INTO """ + tableName + columnSQL + """
                VALUES( """ + str(M) + ',' + str(N) +')')
            # flatting data
            data = np.matrix.flatten(matrix)
            columnSQL = '(' + columnName[2] + ')'
            # Data write:
            for i in range(len(data)):
                sql = """ INSERT INTO """ + tableName + columnSQL + """
                    VALUES( """ + str(data[i]) + ')'
                self.cur.execute(sql)
            self.db.commit()
        else:
            raise ValueError("Columns should have three elements") 
    
    # just write one column, data is a list - coulumnName is a string
    def WriteCol(self, tableName, columnName, data):
        for i in range(len(data)):
            sql = """ INSERT INTO """ + tableName + ' (' + columnName + ')' + """
                VALUES( """ + str(data[i]) + ')'
            self.cur.execute(sql)
        self.db.commit()

    # write row:
    def WriteRow(self, tableName, columnName, row):
        self.cur.execute("INSERT INTO " + tableName + '(' + ', '.join(columnName) + ") VALUES (" + ', '.join(row) + ')')
        self.db.commit()

    # first run this, to initiate successfulness
    def InitateSuccess(self, tableName):
        self.cur.execute("INSERT INTO " + tableName + "(successful) VALUES (0)" )
        self.db.commit()

    # second run this, to finalize successfulness
    def UpdateSuccess(self, tableName):
        self.cur.execute("UPDATE " + tableName + " SET successful = 1 WHERE successful = 0")
        self.db.commit()

    # closing database
    def CloseDB(self):
        self.db.close()
