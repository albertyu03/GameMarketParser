from QUERYfunc import *
from READfunc import *
from WRITEfunc import *
from ERRORthrow import *
from IPfunc import *
import traceback
import time

proxies = []

def mainQ():
  global proxies
  reset_proxies()
  proxies = get_proxies()

  reset_json(fileName='errors.json',hash='errors')
  reset_json()
  loopQ('jobs/misc.json', 4)
  loopQ("jobs/gem.json", 0)
  loopQ("jobs/ess.json", 1)
  loopQ("jobs/scarabs.json", 2)
  loopQ("jobs/fossilorb.json", 3)
  
def loopQ(jobFile, sheetInd):
  global proxies

  reset_json()
  print("start")
  cDict = []
  divValue = divCheck()
  queries = readQuery(fileName=jobFile)
  for QUERY in queries:
    if(checkErrors()):
        time.sleep(300)
        resetErrors()
    try:
     for qResult in query(QUERY, proxies):
      time.sleep(1)
      if(not checkErrors()):
        if(qResult['currency'] == 'divine'): #chaos conversion
          qResult['value'] = qResult['value'] * divValue
          qResult['currency'] = 'chaos'
        cDict.append(qResult)
      else:
        print("error caught")
    except Exception:
      traceback.print_exc()
      throwERROR(error='query fail', function='query', query=QUERY)
  if(cDict == []):
    return
  write_json(cDict)
  writeSheet(sheetInd)
  
