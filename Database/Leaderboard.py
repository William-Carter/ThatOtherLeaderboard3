import Database.Interface
import Database.Run

def updatePlacements(db: Database.Interface.DatabaseInterface, categories: list[str]) -> None:
    """
    Refresh the stored placements for every run in the provided categories

    Parameters:
        categories - A list of category IDs to update the leaderboards for
    
    """


    for category in categories:
        db.executeQuery("""
                        WITH RankedRuns AS (
                            SELECT rc.RunID, MIN(r.Time) AS MinTime, RANK() OVER (ORDER BY MIN(r.Time) ASC) AS calculatedRank
                            FROM RunCategories AS rc
                            LEFT JOIN Runs AS r ON rc.RunID = r.ID
                            WHERE rc.Category = ?
                            GROUP BY r.Runner
                        )

                        UPDATE RunCategories AS rc
                        SET Placement = (SELECT calculatedRank FROM RankedRuns WHERE RunID = rc.RunID)
                        WHERE rc.Category = ?
""", (category, category))

def getLeaderboard(db: Database.Interface.DatabaseInterface, category) -> list[list[int|str]]:
    """
    Get a full leaderboard for a given category

    Parameters:
        db - the DatabaseInterface object to work with

        category - the category you want the leaderboard for

    Returns:
        A list containing [Run ID, User ID, User name, Run Time, Run Placement, Run Date]
    
    """

    return db.executeQuery("""
                    SELECT Runs.ID, Users.ID, Users.Name, Runs.Time, RunCategories.Placement, Runs.Date
                    FROM Runs
                    LEFT JOIN Users ON Runs.Runner = Users.ID
                    LEFT JOIN RunCategories on Runs.ID = RunCategories.RunID
                    WHERE RunCategories.Placement IS NOT NULL AND RunCategories.Category = ?
                    ORDER BY RunCategories.Placement
                    """, (category,))


def getAMCBoard(db: Database.Interface.DatabaseInterface):
    return db.executeQuery("""
                    SELECT Name, AMCTotal
                    FROM (
                        SELECT Name, ROUND(SUM(fastestRun), 3) AS AMCTotal, COUNT(DISTINCT CATEGORY) AS numberOfCategories
                        FROM (
                            SELECT Users.ID AS ID, Users.Name AS Name, RunCategories.Category, MIN(TIME) AS fastestRun
                            FROM RunCategories
                            LEFT JOIN Runs ON RunCategories.RunID = Runs.ID
                            LEFT JOIN Users ON Runs.Runner = Users.ID
                            LEFT JOIN Categories ON RunCategories.Category = Categories.ID
                            WHERE Categories.Extension = 0
                            GROUP BY Users.ID, RunCategories.Category
                        ) AS fastestRunsForRunners
                        GROUP BY ID
                    ) AS subquery
                    WHERE numberOfCategories = (SELECT COUNT(DISTINCT ID) FROM Categories WHERE extension = 0)
                    ORDER BY AMCTotal

""")

def getSweepers(db: Database.Interface.DatabaseInterface, cutoff: int):
    return db.executeQuery("""
                        SELECT name, avgRank, maxplacement
                        FROM (
                            
                            SELECT u.Name as name, COUNT(rc.Placement) as numOfCats, AVG(rc.Placement) as avgRank, MAX(rc.placement) as maxplacement
                            FROM RunCategories rc
                            LEFT JOIN Runs r ON rc.RunID = r.ID
                            LEFT JOIN Users u ON r.Runner = u.ID
                            LEFT JOIN Categories c ON rc.Category = c.ID
                            WHERE rc.Placement <= ?
                            AND c.Extension = 0
                            GROUP BY r.Runner
                            )
                        WHERE numOfCats = (SELECT COUNT(DISTINCT ID) FROM Categories WHERE extension = 0)
                        ORDER BY avgRank
""", (cutoff,))