import Database.Interface
import src.DownloadLeaderboard
import src.ImportUserInfo
import src.ImportRunInfo

db = Database.Interface.DatabaseInterface("Database/thatOtherLeaderboard.db")


src.DownloadLeaderboard.getRuns()
src.ImportUserInfo.ImportUserInfo(db)
src.ImportRunInfo.ImportRunInfo(db)