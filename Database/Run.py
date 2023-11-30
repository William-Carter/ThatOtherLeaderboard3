import Database.Interface
import Database.User
import Database.Category

class Run:
    def __init__(self, db: Database.Interface.DatabaseInterface, id: int = None):
        self.db = db
        self.id = id
        self.valid = True # True if the run is an accessible run (has an entry in the db)

        if (not self.id) or (not db.getSingle("SELECT ID FROM Runs WHERE ID = ?", (self.id,))):
            self.valid = False

        else:
            runnerID = db.getSingle("SELECT Runner FROM Runs WHERE ID = ?", (self.id,))
            self.runner = Database.User.User(self.db, runnerID)


        
    def initialize(self, runner: int, time: float, category: str, date: str = None) -> None:
        """
        Initialize a run by inserting a row into the Runs table, as well as corresponding rows in RunCategories

        Parameters:
            runner - the ID of the runner who performed the run
            time - the duration of the run
            category - the category the run was performed for, will propagate to other categories
            date - the date the run was performed
        
        """

        runID = self.db.insertAndFetchRowID("""
                             INSERT INTO Runs (Runner, Time, Date)
                             VALUES (?, ?, ?)
                             """, (runner, time, date))
        
        
        categories = Database.Category.doCategoryPropagation(category)
        categories.remove(category) # We need to insert the original category separately to mark "SubmittedAs" correctly


        # Insert the original category with SubmittedAs set to 1
        self.db.executeQuery("""
                INSERT INTO RunCategories (RunID, Category, SubmittedAs)
                VALUES (?, ?, 1)
                """, (runID, category))
        
        # Insert the rest with it set to 0
        for propagatedCategory in categories:
            self.db.executeQuery("""
                INSERT INTO RunCategories (RunID, Category, SubmittedAs)
                VALUES (?, ?, 0)
                """, (runID, propagatedCategory))
            
        self.id = runID
        self.runner = runner
        self.valid = True




def runExists(db: Database.Interface.DatabaseInterface, runnerID: int, category: str, time: float) -> bool:
    """
    Check whether a run is already tracked in the database

    Parameters:
        runnerID - the database ID of the runner
        category - the category to check in
        time - the duration of the run

    Returns:
        True if it exists, False otherwise
    """

    if not db.executeQuery("""
                        SELECT ID
                        FROM Runs
                        RIGHT JOIN RunCategories ON Runs.ID = RunCategories.RunID 
                        WHERE Runs.Runner = ? AND runs.time = ? AND RunCategories.Category = ?
                        
                        """, (runnerID, time, category)):
        return False
    
    return True
