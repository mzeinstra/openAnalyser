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

from checker import Checker

class linkCrawler(threading.Thread):
	
	def __init__(self, backlog, stats, collector, stop_event):
		self.backlog = backlog
		self.stats = stats
		self.collector = collector
		self.isstopped = stop_event
		self.http = urllib3.PoolManager()
		self.start()
		

	# Get all links
	def start(self):
		domain = self.backlog.pop()
		while not self.isstopped.is_set():
			if domain == None:
				sleep(5)
			else:
				logging.info("Crawling: " + domain)
				self.analyse(domain)		
			domain = self.backlog.pop()
		print ("Stopping thread..")		

	
	def getPage(self, url):
		page = None
		try: 
			page = self.http.request('GET', "http://" + url, timeout=2)
		except urllib3.exceptions.NewConnectionError as e:
			logging.info(e.reason)
		except timeout:
			logging.info("timeout: ", url)
		except socket.timeout as e:
			logging.info("timeout: ", url)
		except KeyboardInterrupt:
			raise
		except UnicodeDecodeError as e:
			logging.info("Failed to process (No UTF-8)" + url)
			logging.info(*sys.exc_info())
		except:
			logging.info("an error occured")
		return page
	
	# Get all links
	def analyse(self, url):
		OSTools = []
		#START Crawler
		page = self.getPage(url)
			
		links = []
		if page != None:
			poweredByHeaders = page.headers.get_all('x-powered-by')
			self.collector.append('x-powered-by', poweredByHeaders)
			try:
				soup = BeautifulSoup(page.data, "html.parser")
			except Exception as e:
				logging.info("Failed to process " + url)
				soup = None
			except UnicodeDecodeError as e:
				logging.info("Failed to process (No UTF-8)" + url)
			if soup != None:
				#analyse contents
				PageChecker = Checker(soup, poweredByHeaders)
				OSTools = PageChecker.checkAll()
				#Collect Meta Generator tag
				self.collector.append('generator-tag', PageChecker.getGenerators())
			
				#Next links
				links = []
				for link in soup.findAll('a', attrs={'href': re.compile("^http.://")}):
					#store links for next crawl
					link = link.get('href')
					if tldextract.extract(link).suffix == "nl":
						links.append(urlparse(link).netloc)
			
				for link in soup.findAll('img', attrs={'href': re.compile("^http.://")}):
					#store links for next crawl
					link = link.get('href')
					if tldextract.extract(link).suffix == "nl":
						links.append(urlparse(link).netloc)
		
		self.backlog.append(links)
		self.stats.update(OSTools)
		return

	def getCount(self):
		return self.getCountParsed() + self.getCountToParse()
		
	def getCountParsed(self):
		return len(self.parsed)
		
	def getCountToParse(self):
		return len(self.toParse)
	
	def getToParse(self):
		return self.toParse
	
	def getParsed(self):
		return self.parsed
	