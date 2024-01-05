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
