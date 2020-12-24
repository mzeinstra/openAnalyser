import sys, traceback
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib.error
from socket import timeout
import tldextract
import re
import curses
import logging
import threading
from time import sleep


from crawler import linkCrawler
from checker import Checker
from stats import Stats
from backlog import Backlog

def crawl():
	stats = Stats()
	backlog = Backlog('toParse.txt','parsed.txt')
	stop_event= threading.Event()
	threads = 25
	running = []
	try:
		if backlog.count() == 0:
			print("No domains to parse found, starting with opennederland.nl")
			backlog.append(["opennederland.nl"])
			sleep(1) # don't know how to wait for backlog to finish
		
		
		while len(running) <= threads:
			print (len(running))
			print (threads)
			if backlog.count() > 0:		
				print("Starting new thread nr." +str(len(running)+1))
				t = threading.Thread(target=linkCrawler, args=(backlog,stats,stop_event))
				t.daemon = True # die when the main thread dies
				t.start()
				running.append(t)
			else:
				print("No available domains. Waiting...")
				sleep(1)
		print ("Threads running: " + str(len(running)+1))
		
		while True:
			stats.printStats()
			sleep(5)
	except KeyboardInterrupt:
		print ("Shutdown requested...exiting")
		stop_event.set()
		main_thread = threading.currentThread()
		for t in threading.enumerate():
			if t is not main_thread:
				t.join()
		stats.printStats()
		backlog.safeprogress()
	except Exception:
		traceback.print_exc(file=sys.stdout)
	

def main():
	crawl()

if __name__ == "__main__":
	try:
		logging.basicConfig(filename='log.log', level=logging.INFO)
		logging.info('Started')	
		main()
	finally:
		logging.info('Finished')



def getPage(link):
	page = ""
	try: page = urlopen("http://" + link)
	except urllib.error.URLError as e:
		logging.debug(e.reason)
	except timeout:
		logging.info("timeout: ", link)
	except KeyboardInterrupt:
		raise
	return page

def analyse(page):
	PageChecker = Checker(page)
	print(PageChecker.checkAll())


        