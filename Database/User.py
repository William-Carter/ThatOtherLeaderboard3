import Database.Interface
import Database.Run
import Helpers.durations
class User:
    def __init__(self, db: Database.Interface.DatabaseInterface, userID: int = None):
        """
        An object representing a user in the database. Can be used to access all attributes about the user.

        User.valid will be false if the specified user does not already exist.

        Parameters:
            db - The DatabaseInterface object used to interact with the database

            userID - the database ID of the user
        """
        self.db = db
        self.ID = userID
        self.valid = True

        
        results = self.db.executeQuery("SELECT * FROM Users WHERE ID = ?", (self.ID,))
        if len(results) == 0:
            self.valid = False
            return
        
        results = results[0]
        self.name = results[1]
        self.srcID = results[2]
        self.discordID = results[3]
        self.nationality = results[4]
            
        

    def initialise(self, name: str, srcID: str, nationality: str):
         self.ID = self.db.insertAndFetchRowID("""
                             INSERT INTO Users (Name, srcID, Nationality)
                             VALUES (?, ?, ?)
                             """, (name, srcID, nationality))  
         self.valid = True



    def getName(self) -> str:
        """
        Fetch the User's name

        Returns:
            The user's name, as a string
        """

        return self.db.getSingle("""SELECT Name FROM Users WHERE ID = ?""", (self.ID,))
    

    def setName(self, name) -> None:
        """Change the user's name in the database

        Parameters:
            name - The name to write
        """
        self.db.executeQuery("UPDATE Users SET Name = ? WHERE ID = ?", (name, self.ID))



    def getDiscordID(self) -> int:
        """
        Fetch the User's discord id

        Returns:
            The user's discord id, as an integer
        """

        return self.db.getSingle("SELECT discordID FROM Users WHERE ID = ?", (self.ID,))
    

    def updateDiscordID(self, discordID: int) -> None:
        """
        Update the user's stored discord ID

        Parameters:
            discordID - the new ID to store
        
        """

        self.db.executeQuery("UPDATE Users SET discordID = ? WHERE ID = ?", (discordID, self.ID))
    

    def getPersonalBests(self) -> list:
        """
        Fetch the user's personal best in all categories

        Returns:
            A list of lists. Each sublist contains: Run ID, Run Category, Run Extension Status, Run Time, Run Placement
        
        """
        
        return self.db.executeQuery("""
                                    SELECT Runs.ID, RunCategories.Category, Categories.Extension, MIN(Runs.Time), RunCategories.Placement
                                    FROM RunCategories
                                    LEFT JOIN Runs ON RunCategories.RunID = Runs.ID
                                    LEFT JOIN Categories on RunCategories.category = Categories.ID
                                    WHERE Runs.Runner = ?
                                    GROUP BY RunCategories.Category
                                    """, (self.ID,))
    

    def getRuns(self) -> list:
        return self.db.executeQuery("""
                             SELECT Runs.ID, RunCategories.Category, Runs.Time, Runs.Date
                             FROM RunCategories
                             LEFT JOIN RUns ON RunCategories.RunID = Runs.ID
                             WHERE Runs.Runner = ? AND RunCategories.SubmittedAs = 1
                             ORDER BY Runs.Date DESC
                             """, (self.ID,))
        


    def getGolds(self, category: str) -> list[list[any]]:
        """
        Get the user's gold splits for a given category

        Parameters:
            category - the given category

        Returns:
            A list of golds formatted as [levelName, time, comgoldEligible]
        """
        golds = self.db.executeQuery("""
                                        SELECT Maps.LevelName, Golds.Time, Golds.CGEligible
                                        FROM Golds
                                        LEFT JOIN Maps ON Golds.MapName = Maps.Map
                                        WHERE Golds.Runner = ?
                                        AND Category = ?
                                        ORDER BY Maps.MapOrder
                             """, (self.ID, category))
        
        return golds
    

    def getAverageRank(self, includeExtensions: bool = False) -> float|None:
        """
        Get the user's average rank
        
        Returns:
            The float average rank, rounded to two decimal places

            None if no the user has no runs
        """
        
        sum = 0
        count = 0
        pbs = self.getPersonalBests()
        for pb in pbs:
            if includeExtensions or (not pb[2]):
                count += 1
                sum += pb[4]

        if count == 0:
            return None
        return round(sum/count, 2)
    

    def getAMCEstimate(self) -> float:
        """
        Get the user's AMC estimate

        Returns:
            The sum of the user's inbounds, oob, legacy and glitchless times, if they have a time for each

            None if they don't have a time for one or more of the categories
        
        """

        output = self.db.executeQuery("""
                            SELECT SUM(Runs.Time), COUNT(Runs.ID), COUNT(Categories.ID)
                            FROM RunCategories
                            LEFT JOIN Runs ON RunCategories.RunID = Runs.ID
                            LEFT JOIN Categories ON RunCategories.Category = Categories.ID
                            WHERE RunCategories.Placement IS NOT NULL 
                            AND Categories.Extension = 0 
                            AND Runs.Runner = ?
            """, (self.ID,))[0]
        
        if output[1] < output[2]: # If the user doesn't have a time for every main cat
            return None
        return output[0]

    def getSCKR(self) -> list[list[str, float]]:
        return self.db.executeQuery("""
                                    SELECT Categories.ID, ROUND(((WRs.WR-Categories.Downtime)/(MIN(Runs.Time)-Categories.Downtime)*100), 2) as SCKR
                                    FROM RunCategories
                                    LEFT JOIN Runs ON RunCategories.RunID = Runs.ID
                                    LEFT JOIN Categories on RunCategories.category = Categories.ID
                                    LEFT JOIN (
                                        SELECT c.ID as category, MIN(Time) as WR
                                        FROM RunCategories rc
                                        LEFT JOIN Runs r ON rc.RunID = r.ID
                                        LEFT JOIN Categories c ON rc.Category = c.ID
                                        GROUP BY rc.Category
                                    ) WRs ON RunCategories.category = WRs.category
                                    WHERE Runs.Runner = ?
                                    AND Categories.Extension = 0
                                    GROUP BY RunCategories.Category
                                    """, (self.ID,))


    def getCountry(self) -> list[str, str]:
        """
        Get the user's country

        Returns:
            (countryID, countryName)
        """
        return self.db.executeQuery("""
                                      SELECT Countries.Code, Countries.Name
                                      FROM Users
                                      LEFT JOIN Countries ON Users.Nationality = Countries.Code
                                      WHERE Users.ID = ?
                                      """, (self.ID,))[0]
    

    def addRun(self, category: str, time: float, date: str) -> Database.Run.Run:
        newRun = Database.Run.Run(self.db)
        newRun.initialize(self.ID, time, category, date)
        return newRun
        
    def updateGolds(self, category: str, times: list[float]):
        """
        Updates the user's golds for a given category, accounting for comgold eligibility

        Parameters:
            category - the category for which to update the user's golds
            
            times - a list of numerical times for all 18 maps
        """


        maps = self.db.executeQuery("""
                                SELECT Map
                                FROM Maps
                                WHERE Advanced = 0
                                ORDER BY MapOrder
                             """)
        maps = [x[0] for x in maps]


        needsEligibility = {
            "oob": [
                "testchmb_a_00"
            ],
            "inbounds": [
                "testchmb_a_01",
                "testchmb_a_09",
                "testchmb_a_11",
            ]
        }

        if category in needsEligibility.keys():
            eligibilityList = needsEligibility[category]
        else:
            eligibilityList = []



        existingGolds = self.db.executeQuery("""
                                 SELECT MapName, CGEligible
                                 FROM Golds
                                 WHERE Runner = ?
                                 """, (self.ID,))
        
        existingEligibility = {x: None for x in maps}

        for gold in existingGolds:
            existingEligibility[gold[0]] = gold[1]


        sob = 0
        for index, time in enumerate(times):
            sob += time
            map = maps[index]
            if map in eligibilityList:
                cgoldEligible = 0
            else:
                cgoldEligible = 1

            if not existingEligibility[map] == None:
                cgoldEligible = existingEligibility[map]

            self.db.executeQuery("""
                                     INSERT OR REPLACE INTO Golds
                                     VALUES (?, ?, ?, ?, ?)
                                     """, (map, self.ID, float(time), cgoldEligible, category))
            
        return sob



def identifyUser(db: Database.Interface.DatabaseInterface, discordID: int = None, srcID: str = None, username: str = None) -> int|None: 
    """
    Returns the User ID of the specified person, or None if the specified person does not exist.
    
    """

    numOfIDTokensProvided = sum([1 for x in [username, srcID, discordID] if x is not None])

    if numOfIDTokensProvided == 0:
        raise TypeError("User object requires exactly one of username, srcID and discordID, but none were provided")

    if numOfIDTokensProvided > 1:
        raise TypeError("User object requires exactly one of username, srcID and discordID, but more than one was provided")
    

    if discordID:
        return db.getSingle("SELECT ID FROM Users WHERE discordID = ?", (discordID,))
    
    if srcID:
        return db.getSingle("SELECT ID FROM Users WHERE srcID = ?", (srcID,))
    
    if username:
        return db.getSingle("SELECT ID FROM Users WHERE LOWER(Name) = ?", (username.lower(),))

    
def getAllUsers(db: Database.Interface.DatabaseInterface) -> list[User]:
    return [User(db, x[0]) for x in db.executeQuery("SELECT ID FROM Users")]