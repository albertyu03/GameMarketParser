import os
import requests
import json
from READfunc import *
from QUERYfunc import *
import time
import random


def getLocalIP():
    ip = requests.get('https://api.ipify.org').text
    return ip

def reset_proxies():
    changes = requests.get("https://www.sharedproxies.com/api.php?m=thebroadestbarn%40gmail.com&s=c1483862c7fbe74f23ba4c625fb15d2b72129ec6&do=replacealldown")
    assert changes.status_code == 200

def get_proxies():
    resp = requests.get("https://www.sharedproxies.com/api.php?m=thebroadestbarn%40gmail.com&s=c1483862c7fbe74f23ba4c625fb15d2b72129ec6&do=getall")
    assert resp.status_code == 200
    return resp.text.splitlines()

def update_ip():
    currIP = getLocalIP()
    response = requests.get("https://www.sharedproxies.com/updateip-specify.php?m=thebroadestbarn%40gmail.com&s=c1483862c7fbe74f23ba4c625fb15d2b72129ec6&auto=on&num=1&ip="+currIP)
    assert response.status_code == 200
    print("waiting for update time!")
    time.sleep(120)




def troubleshootErr():
    return #stub
    '''
    print(getStatic())
    if(getStatic() != getLocalIP()):
        return "local IP does not match"
    for prox in getProxies():
        if(not checkProxy(prox)):
            return "prox is outdated"
    QUERY = {
            "QUERY": {
                "query": {
                    "status": {
                        "option": "online"
                    },
                    "have": [
                        "chaos"
                    ],
                    "want": [
                        "shrieking-essence-of-suffering"
                    ],
                    "minimum": 15
                },
                "sort": {
                    "have": "asc"
                },
                "engine": "new"
            },
            "nameSet": "shrieking-essence-of-suffering[chaosMIN30]",
            "firstX": 1,
            "queryType": "exchange/",
            "num": 3
    }
    if(QUERY(query) == []):
        return "trade down?"
    return "unknown"
    '''
    