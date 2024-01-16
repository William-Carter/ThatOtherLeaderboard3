def seconds(timeString):
    parts = timeString.split(":")
    total = 0
    weight = 1
    try:
        for i in range(len(parts)):
            total += float(parts[-(i+1)])*weight
            weight *= 60
        return total
    except:
        return False

def formatted(timeNum: float) -> str:
    minutes = int(timeNum // 60)
    sms = round(timeNum % 60, 3)
    result = str(sms)
    if minutes:
        
        if sms < 10: 
            result = str(minutes)+":0"+result # Get 5:04.5 instead of 5:4.5

        else:
            result = str(minutes)+":"+result

    result = result+('0'*(3-len(result.split(".")[-1]))) # Add trailing zeroes
    return result

def correctToTick(timeNum: float) -> float:
    return round(round((timeNum/0.015), 0)*0.015, 3)

def formatLeaderBoardPosition(position: int, colorCode: bool = False):
    suffix = "th"
    cases = {"1": "st",
                "2": "nd",
                "3": "rd",
                }
    if not ("0"+str(position))[-2] == "1":
        case = str(position)[-1]
        if case in cases.keys():
            suffix = cases[case]

    color = ""
    returnColor = ""
    if colorCode:
        match position:
            case 1:
                color = "\u001b[1;33m"
            case 2:
                color = "\u001b[1;30m"
            case 3:
                color = "\u001b[1;32m"

        returnColor = "\u001b[0m"
        

    return color+str(position)+suffix+returnColor


def numberLeaderboard(leaderboard: list[list]):
    """
    Apply 
    """


if __name__ == "__main__":
    tests = [
        "43",
        "60",
        "74",
        "43.5",
        "60.3",
        "74.9",
        "1:00",
        "1:02",
        "1:00.525",
        "15:33.120",
        "01:00",
        "01:00.3",
        "01:00.374",
        "1:09:32",
        "1:09:32.375"
    ]
    for test in tests:
        print(test, ", ", seconds(test))


    tests = [
        43,
        63.34,
    ]
    for test in tests:
        print(test, ", ", formatted(test))
