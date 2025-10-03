import os
import requests
import json
from read import *
from error_log import *
import time
import random

LEAGUE = "Mercenaries"
staticIP = "" # old hosted ip 
HEADERS = {
  "User-Agent": ""
}
proxy = {}
c_count = 0
UserAgents = ["personal testing"]
proxies = [] # if proxies are needed
HEADER_NUM = 1

def changeHeader():
  global c_count
  HEADERS = {
    "User-Agent": UserAgents[c_count]
  }
  proxy = {
    'http': proxies[c_count],
    'https': proxies[c_count]
  }
  c_count += 1
  if(c_count > HEADER_NUM):
    c_count = 0
  return


#take in query, call other func and return array of results
def query(QUERY, prox=[]):
  global proxies
  proxies = prox

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