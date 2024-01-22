import json
import requests
from time import gmtime, strftime
from IPfunc import *

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

  #debugging --> reset proxies, reconnect ip(?) , check server down
  #check rate limits
  
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
  file.seek(0)
  json.dump(file_data, file, indent = 4)
  file.truncate()
  file.close()

def query_assertion(response):
  code = response.status_code
  if(code == 200 or code == 202):
    return 0
  elif(code == 400):
    return 1 #bad request
  elif(code == 404):
    return 2 #not found?
  elif(code == 429):
    return 3 #rate limit
  elif(code == 500):
    return 4 #server error
