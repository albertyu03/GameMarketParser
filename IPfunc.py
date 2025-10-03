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

def troubleshootErr():
    return #stub
    
    