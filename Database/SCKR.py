import Database.Interface
def getSCKRBoard(db: Database.Interface.DatabaseInterface, country: str = None, continent: str = None):
    if country:
        result = db.executeQuery("""SELECT Code, Name FROM Countries WHERE LOWER(Name) = ?""", (country.lower(),))
        if len(result) == 0:
            return None, "invalid"
        regionSelection = f"WHERE Users.Nationality = LOWER('{result[0][0]}')"
        regionName = result[0][1]

    elif continent:
        result = db.executeQuery("""SELECT ID, Name FROM Continents WHERE LOWER(Name) = ?""", (continent.lower(),))
        if len(result) == 0:
            return None, "invalid"
        regionSelection = f"WHERE Continents.ID = '{result[0][0]}'"
        regionName = result[0][1]

    else:
        regionSelection = ""
        regionName = ""
        
    return db.executeQuery(f"""
        SELECT Users.Name, ROUND(SUM(score), 2) as aggregate, Countries.Name
        FROM
        (
        SELECT 
        Runs.Runner as Runner,
        RunCategories.Category,
        (WR.time / MIN(Runs.time)) * 100 AS score
        FROM RunCategories
        LEFT JOIN Runs ON RunCategories.RunID = Runs.ID
        LEFT JOIN Categories ON RunCategories.Category = Categories.ID
        LEFT JOIN (
            SELECT
            c.ID as category,
            MIN(r.Time) as time
            FROM RunCategories rc
            LEFT JOIN Runs r on rc.RunID = r.ID
            LEFT JOIN Categories c on rc.Category = c.ID
            GROUP BY c.ID
        ) WR ON RunCategories.Category = WR.category
        WHERE Categories.Extension = 0
        GROUP BY Runner, RunCategories.Category
        ) as subquery
        LEFT JOIN Users ON subquery.Runner = Users.ID
        LEFT JOIN Countries ON Users.Nationality = LOWER(Countries.Code)
        LEFT JOIN Continents ON Countries.Continent = Continents.ID
        {regionSelection}
        GROUP BY Runner
        ORDER BY aggregate DESC
        """), regionName