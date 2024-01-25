import Database.Interface
import json

def getNationalLeaderboard(db: Database.Interface.DatabaseInterface, category: str, country: str) -> list[list[int|str]]:

    with open("Database/countries.json", "r") as f:
        countries = json.load(f)

    countryCode = None
    for testingCountry in countries:
        if country.lower() in countries[testingCountry]:
            countryCode = testingCountry.lower()
            countryName = countries[testingCountry][0].capitalize()
            break



    if not countryCode:
        return None, "invalid"

    pattern = countryCode+"%"


    return db.executeQuery("""
                    SELECT Runs.ID, Users.ID, Users.Name, Runs.Time, RunCategories.Placement, Runs.Date
                    FROM Runs
                    LEFT JOIN Users ON Runs.Runner = Users.ID
                    LEFT JOIN RunCategories on Runs.ID = RunCategories.RunID
                    WHERE RunCategories.Placement IS NOT NULL 
                    AND RunCategories.Category = ?
                    AND Nationality LIKE ?
                    ORDER BY RunCategories.Placement
                    """, (category, pattern)), countryName



def getContinentalLeaderboard(db: Database.Interface.DatabaseInterface, category: str, continent: str):
    result = db.executeQuery("""SELECT ID, Name FROM Continents WHERE LOWER(Name) = ?""", (continent.lower(),))
    if len(result) == 0:
        return None,"invalid"
    
    result = result[0]
    continentCode = result[0]
    continentName = result[1]
    if not continentCode:
        return None, "invalid"
    
    return db.executeQuery("""
                    SELECT Runs.ID, Users.ID, Users.Name, Runs.Time, RunCategories.Placement, Runs.Date, Countries.Name
                    FROM Runs
                    LEFT JOIN Users ON Runs.Runner = Users.ID
                    LEFT JOIN RunCategories on Runs.ID = RunCategories.RunID
                    LEFT JOIN Countries ON Users.Nationality = LOWER(Countries.CODE)
                    LEFT JOIN Continents ON Countries.Continent = Continents.ID
                    WHERE RunCategories.Placement IS NOT NULL 
                    AND RunCategories.Category = ?
                    AND LOWER(Continents.ID) = ?
                    ORDER BY RunCategories.Placement
                    """, (category, continentCode.lower())), continentName


def getNationalPlacement(db: Database.Interface.DatabaseInterface, runID: int, category: str):
    return db.getSingle("""
                           SELECT calculatedRank 
                           FROM (   
                                SELECT rc.RunID, RANK() OVER (ORDER BY MIN(r.Time) ASC) AS calculatedRank
                                FROM RunCategories AS rc
                                LEFT JOIN Runs AS r ON rc.RunID = r.ID
								LEFT JOIN Users AS u ON r.Runner = u.ID
                                WHERE rc.Category = ?
								AND u.Nationality = (
                                    SELECT iu.Nationality 
                                    FROM Runs ir
									LEFT JOIN Users iu ON ir.Runner = iu.ID
                                    WHERE ir.ID = ?                            
                                    )
								
                                GROUP BY r.Runner
                           ) 
                           
                           WHERE RunID = ? 
        """, (category, runID, runID))


def getContinentalPlacement(db: Database.Interface.DatabaseInterface, runID: int, category: str):
    return db.getSingle("""
                           SELECT calculatedRank 
                           FROM (   
                                SELECT rc.RunID, RANK() OVER (ORDER BY MIN(r.Time) ASC) AS calculatedRank
                                FROM RunCategories AS rc
                                LEFT JOIN Runs AS r ON rc.RunID = r.ID
								LEFT JOIN Users AS u ON r.Runner = u.ID
								LEFT JOIN Countries AS c ON u.Nationality = LOWER(c.Code)
                                WHERE rc.Category = ?
								AND c.Continent = (
                                    SELECT ic.Continent
                                    FROM Runs ir
									LEFT JOIN Users iu ON ir.Runner = iu.ID
									LEFT JOIN Countries ic ON iu.Nationality = LOWER(ic.Code)
                                    WHERE ir.ID = ?                        
                                    )
								
                                GROUP BY r.Runner
                           )
                           WHERE RunID = ? 
        """, (category, runID, runID))