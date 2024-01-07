import json
from time import gmtime, strftime

filename = 'errors.json'

def throwERROR(error='default error', function='default func', query='no query pass'):
  newEXCEP = {
    'error': error,
    'function': function,
    'query': query,
    'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())
  }
  file = open(filename, 'r+')
  file_data = json.load(file)
  file_data["errors"].append(newEXCEP)
  file.seek(0)
  json.dump(file_data, file, indent = 4)
  file.close()

def checkErrors():
  file = open(filename, 'r')
  file_data = json.load(file)
  if(len(file_data['errors']) > 0):
    file.close()
    return True
  file.close()
  return False

def resetErrors():
  file = open(filename, 'r+')
  file_data = json.load(file)
  file_data['errors'].clear()
  #print(file_data)
  file.seek(0)
  json.dump(file_data, file, indent = 4)
  file.truncate()
  file.close()
  