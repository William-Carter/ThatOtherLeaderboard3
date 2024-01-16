from typing import List
from strip_ansi import strip_ansi

def generateTable(inp: List[List[str]], padding: int = 4) -> str:
    """
    Generates a whitespace-padded table from the input data
    Inputs:
        inp - A two dimensional list, with the first dimension being the row and the second being the column
        padding - How many whitespace characters to leave between columns. Default 4.
    Outputs:4
        table - The final, whitespace-padded table.
    """

    # Establish the width required for each of the columns
    widths = []
    for i in range(len(inp[0])):
        columnWidth = 0
        for row in inp:
            localWidth = clen(row[i]) # ansi codes may be used, we don't want to include them in our length calculations
            if localWidth > columnWidth:
                columnWidth = localWidth

        widths.append(columnWidth)

    for i in range(len(widths)):
        widths[i] += padding


    table = ""
    for row in inp:
        for i in range(len(row)):
            table += row[i]+" "*(widths[i]-clen(row[i]))
        table += "\n"

    return table


def divideOutput(output, maxLength: int = 2000):
    outputList = []
    rows = output.split("\n")
    currentString = ""
    for row in rows:
        if len(currentString)+len(row) >= 2000:
            outputList.append(currentString)
            currentString = ""

        currentString += row

    outputList.append(currentString)
    return outputList


def codeBlock(inp: str | list):
    outp = []
    if type(inp) == str:
        return "```\n"+inp+"```"
    
    for item in inp:
        outp.append("```\n"+item+"```")

    return outp


def clen(item):
    stripped = strip_ansi(item)
    return len(stripped)



if __name__ == "__main__":
    testCode = "\u001b[1;33mpenis\u001b[0m"
    print(len(testCode))
    print(clen(testCode))