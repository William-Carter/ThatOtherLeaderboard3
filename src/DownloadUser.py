import requests

def DownloadUser(srcID: str):
    runnerJson = requests.get(f"https://speedrun.com/api/v1/users/{srcID}").json()
    return runnerJson