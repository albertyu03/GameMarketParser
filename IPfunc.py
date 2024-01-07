import os
import requests
import json
from READfunc import *
from ERRORthrow import *
import time
import random


def getLocalIP():
    ip = requests.get('https://api.ipify.org').text
    return ip

def checkProxy(proxy):
    #stub
    return