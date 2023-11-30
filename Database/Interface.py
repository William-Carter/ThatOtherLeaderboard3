import sqlite3

class DatabaseInterface:
    def __init__(self, dbPath: str) -> None:
        """
        Parameters:
            dbPath - The absolute path to the sqlite .db file
        """
        self.dbPath = dbPath
        self.connection = None
        self.cursor = None

    def openConnection(self):
        """
        Open a connection to the database
        """
        self.connection = sqlite3.connect(self.dbPath)
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        """
        Close the connection to the database.
        """
        self.connection.commit()
        self.connection.close()
        self.connection = None
        self.cursor = None


    def executeQuery(self, query: str, args: list = ()) -> list[list[any]]|None:
        """
        Execute a query. Returns the output of result.fetchall()
        
        Parameters:
            query - the query to be executed
            
            args - the arguments to be passed to the query
        """

        self.openConnection()
        result = self.cursor.execute(query, args).fetchall()
        self.closeConnection()
        return result
    

    def insertAndFetchRowID(self, query: str, args: list = ()) -> int:
        """
        Execute an insertion query. Returns the ID of the inserted row.

        Parameters:
            query - the query to be executed

            args - the arguments to be passed to the query
        """
        self.openConnection()
        self.cursor.execute(query, args)
        result = self.cursor.lastrowid
        self.closeConnection()
        return result


    def getSingle(self, query: str, args: list = ()) -> any:
        """
        Returns the sole value returned by any given query. Will throw an error if more than one value returned.

        Parameters:
            query - the SELECT query to be executed
        """

        queryResults = self.executeQuery(query, args)

        if len(queryResults) == 0:
            return None

        if len(queryResults) > 1:
            raise Exception("More than one row selected by query!")
            
        
        if len(queryResults[0]) > 1:
            raise Exception("More than one column selected by query!")
            

        return queryResults[0][0]
        



