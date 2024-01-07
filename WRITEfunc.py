import pygsheets
import pandas as pd
import json
from time import gmtime, strftime
#authorization

def writeSheet(sheetIndex):
  gc = pygsheets.authorize(service_file='poe-data-script-1513fbd9081f.json')
  df = pd.DataFrame()
  df = createDF()
  sh = gc.open('test write')
  
  #select the first sheet 
  #sh.values_clear("Sheet4!A1:J1000")
  #0 = gem, 1 = ess, 2 = scarab, 3 = fossil/orb, 4 = misc
  wks = sh[sheetIndex]
  
  #update the first sheet with df, starting at cell B2. 
  wks.clear()
  wks.set_dataframe(df,(1,1))
  #print("test done 8")
  
def createDF():
  gc = pygsheets.authorize(service_file='poe-data-script-1513fbd9081f.json')
  df = pd.DataFrame()
  names = []
  timeUpdate = []
  values = []
  currency = []
  firstX = []
  filename = "results.json"
  file = open(filename, 'r')
  file_data = json.load(file)
  results = file_data['results']
  for items in results:
    #print(items)
    names.append(items['nameSet'])
    timeUpdate.append(items['time'])
    values.append(items['value'])
    currency.append(items['currency'])
    firstX.append(items['firstX'])
  df['name'] = names
  df['time'] = timeUpdate
  df['values'] = values
  df['currency'] = currency
  df['firstX'] = firstX
  return df


def write_json(new_data, filename='results.json', hash = 'results'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        for item in new_data:
          #print(item)
          file_data[hash].append(item)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        file.write(json.dumps(file_data))
    # python object to be appended

def reset_json(fileName = 'results.json', hash = 'results'):
  with open(fileName, 'r+') as file:
    try:
      file_data = json.load(file)
      file_data[hash].clear()
      #print(file_data)
      file.seek(0)
      json.dump(file_data, file, indent = 4)
      file.truncate()
    except:
      file.truncate(0)
      new_data = {
        hash: []
      }
      file.seek(0)
      file.write(json.dumps(new_data))
      file.truncate()
    file.close()
