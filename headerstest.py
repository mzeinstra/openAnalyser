from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib3
from socket import timeout
import tldextract
import re
import traceback
import sys
import logging
import socket
import threading
from time import sleep

from collector import Collector
from checker import Checker

http = urllib3.PoolManager()
page = http.request('GET', "http://opennederland.nl", timeout=2)
print(page)
print("-------------------------------------------------------")
print(page.headers)
print("-------------------------------------------------------")
print(page.headers.keys())
print("-------------------------------------------------------")
print(page.headers.items())
print("-------------------------------------------------------")
t = page.headers.items()
print("-------------------------------------------------------")
d = dict((x, y) for x, y in t)
print (d)
print("-------------------------------------------------------")
if "X-Powered-By" in d:
	print ("print " + d['X-Powered-By'])