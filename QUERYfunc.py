import os
import requests
import json
from READfunc import *
from ERRORthrow import *
import time
import random

currentNum=0
LEAGUE = "Affliction"
true = True
false = False
HEADERS = {
  "User-Agent": ""
}
proxy = {}
proxCount = 0
UserAgents = ["personal testing", "testing", "POEPuller 1.0", "testing requests", "essence sheet", "POMShark 1.3", "try agent", "Bless Sheet 3.2", "BarronQuery 1.7", "mapping data sheet"]
proxies = ["70.39.87.235:80", "104.160.187.130:80", "67.21.83.97:80", "107.173.88.106:80", "70.39.87.125:80", "67.21.83.175:80", "204.188.247.110:80", "23.95.55.112:80", "204.188.217.84:80", "70.39.75.40:80"]
def changeHeader():
  global proxCount
  global HEADERS, proxy
  HEADERS = {
    "User-Agent": UserAgents[proxCount]
  }
  proxy = {
    'http': proxies[proxCount],
    'https': proxies[proxCount]
  }
  proxCount += 1
  if(proxCount > 9):
    proxCount = 0



#take in query, call other func and return array of results
def query(QUERY):
  print(QUERY['nameSet'])
  changeHeader()
  link = "https://www.pathofexile.com/api/trade/" + QUERY["queryType"] + LEAGUE
  respPOST = requests.post(link, headers = HEADERS, json = QUERY["QUERY"], proxies=proxy)
  if("error" in respPOST.json()):
    print('throwing error in respPOST.json()', respPOST.json()['error'])
    throwERROR(error=respPOST.json()['error']['message'], function = 'query', query=link)
    return []

  RES = processPOST(respPOST, QUERY)
  return RES

#overhaul
def generateItemLink(respPOST, QUERY):
  result = respPOST.json()['result']
  link = "https://www.pathofexile.com/api/trade/fetch/"
  firstX = QUERY['firstX']
  num = QUERY['num'] 

  fulfilled = 0
  
  for i in range(firstX, firstX+num):
    if(not(i >= len(result))): #don't exceed length
      fulfilled = fulfilled + 1
      link = link + result[i] + ","

  link = link[:-1] + "?query=" + respPOST.json()['id']
  
  retRes = {
    "link": link,
    "fulfilled": fulfilled
  }
  return retRes    

#overhaul
def processPOST(respPOST, QUERY):
  type = QUERY['queryType']
  QUERY['firstX'] = QUERY['firstX'] - 1
  tempList = []
  returnList = []
  
  if(type == 'search/'): #item
    linkGen = generateItemLink(respPOST, QUERY)
    if(linkGen['fulfilled'] == 0):
      return []
    respGET = requests.get(linkGen['link'], headers=HEADERS,proxies=proxy).json()
    for item in respGET['result']:
      tempList.append(item)
  elif(type == 'exchange/'): #bulk
    for i in range(QUERY['firstX'],QUERY['firstX']+QUERY['num']):
      resValues = []
      try:
        resValues = list(respPOST.json()['result'].values())
      except:
        return []
      try:
        tempList.append(resValues[i])
      except:
        continue
  else: #invalid (other)
    throwERROR(error='bad queryType',function='processPOST',query=QUERY)
    return []

  counter = 0
  for item in tempList:
    #time.sleep(8)
    returnList.append(processGET(item, QUERY, QUERY['firstX']+counter))
    counter = counter + 1
  return returnList

def processGET(result, QUERY, firstX):
  #item: passes "result"
  #bulk: passes 
  name = QUERY['nameSet']
  type = QUERY['queryType']
  retData = {
    'nameSet': name + "+" + str(firstX+1), 
    'firstX': firstX+1,
    'time': strftime("%Y-%m-%d %H:%M:%S", gmtime())
  }
  if(type == 'search/'): #item
    cQuery = result['listing']
    retData['value'] = cQuery['price']['amount']
    retData['currency'] = cQuery['price']['currency']
  else: #bulk
    retData['value'] = result['listing']['offers'][0]['exchange']['amount'] / result['listing']['offers'][0]['item']['amount']
    retData['currency'] = result['listing']['offers'][0]['exchange']['currency']
  return retData
  
def queryECHECK(): #need to catch for empty query as well
  time.sleep(7)
  testQUERY = {"QUERY": {"query":{"status":{"option":"online"},"have":["chaos"],"want":["deafening-essence-of-zeal"],"minimum":1},"sort":{"have":"asc"},"engine":"new"}, "nameSet": "DeafeningZealMin1->C", "firstX": 1, "queryType": "exchange/"}
  link = "https://www.pathofexile.com/api/trade/" + testQUERY["queryType"] + LEAGUE
  try:
    respPOST = requests.post(link, headers = HEADERS, json = testQUERY["QUERY"], proxy=proxies)
    tq = processQRes(respPOST.json()['result'], name='test query')
    return False
  except:
    print("echeck failed")
    return True

#return ninja updated divine value
def divCheck():
  try:
    link = "https://poe.ninja/api/data/currencyoverview?league=" + LEAGUE + "&type=Currency&language=en"
    respPOST = requests.get(link).json()
    for item in respPOST['lines']:
      if(item['currencyTypeName'] == 'Divine Orb'):
        return (item['chaosEquivalent'])
  except:
    throwERROR(error='unable to fetch ninja div', function = 'divCheck()', query=link)
    return -1