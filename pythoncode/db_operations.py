# module defines operations to use with sqlite3 database
import mysql.connector as mysql
import creds


class db_operations:
    # constructor with connection path to db
    def __init__(self, conn_path):
        self.connection = mysql.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")


    #constructor for localhost mysql database use personal creds.py file to access
    def __init__(self):
        self.connection = mysql.connect(user=creds.user, password=creds.pwd,
                                        host='127.0.0.1',
                                        database='spotifyDB')

        self.cursor = self.connection.cursor()
        print("connection made..")

    # function for bulk inserting records
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        self.connection.commit()
        print("query executed..")


    def executeQuery(self, query):
        self.cursor.execute(query)

    def executeManyQuery(self, query):
        self.cursor.executescript(query)
        self.connection.commit()

    def fetchRow(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def commitUpdate(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to return a single value from table
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    #function to return the cursor object
    def getCursor(self):
        return self.cursor;

    #function to rreturn connector object
    def getConnection(self):
        return self.connection

    # function to return a single attribute values from table
    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results

    # SELECT with named placeholders
    def name_placeholder_query(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # close connection
    def destructor(self):
        self.connection.close()
