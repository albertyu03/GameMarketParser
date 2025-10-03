import json
def readBase(fileName):
    f = open(fileName, "r")
    queries = []
    while (True):
        line = f.readline()
        if (not line or line == "\n"):
            break
        currentLine = ""
        while (True):
            currentLine = currentLine + line
            line = f.readline()
            if (line == "\n" or not line):
                break
        queries.append(json.loads(currentLine))
    f.close()
    return queries

def readQuery(fileName):
  with open(fileName, 'r') as file:
    file_data = json.load(file)
    file.close()
    #print(file_data['queries'])
    return file_data['queries']

def readJSON(fileName="rinfo.json",folder="data/",hash="data"):
  with open(fileName, 'r') as file:
    file_data = json.load(file)
    file.close()
    return file_data[hash]
    