import os
import requests
import json
from ip_utils import *
from query import *
import time
import random


def getLocalIP():
    ip = requests.get('https://api.ipify.org').text
    return ip

def troubleshootErr():
    return #stub
    
    