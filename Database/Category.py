import Database.Interface
import json


def doCategoryPropagation(baseCategory: str) -> list[str]:
    """
    Identify all the categories a run is valid for, given the category it was submitted as
    """
    
    with open("Database/CategoryPropagation.json", "r") as f:
        graph = json.load(f)



    visited = set()
    stack = [baseCategory]
    reachableNodes = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            reachableNodes.add(node)
            stack.extend(graph[node])

    return list(reachableNodes)



def getCategoryName(db: Database.Interface.DatabaseInterface, categoryID: str) -> str:
    return db.getSingle("SELECT Name FROM Categories WHERE ID = ?", (categoryID,))



def getCategoryList(db: Database.Interface.DatabaseInterface, includeExtensions = False) -> list[list[str]]:
    return db.executeQuery("""
                    SELECT ID, Name
                    FROM Categories
                    WHERE Extension <= ?
                    """, (int(includeExtensions),))
