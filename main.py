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
from collector import Collector

def crawl():
	stats = Stats()
	backlog = Backlog('toParse.txt','parsed.txt')
	collector = Collector("collections.json")
	stop_event= threading.Event()
	threads = 25
	running = []
	try:		
		for x in range(threads):		
			t = threading.Thread(target=linkCrawler, args=(backlog,stats, collector, stop_event))
			t.daemon = True # die when the main thread dies
			t.start()
			running.append(t)
		
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
		collector.safeprogress()
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


        