from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib.error
from socket import timeout
import tldextract
import re
import traceback
import sys
import logging
import socket
import threading

from checker import Checker

class linkCrawler(threading.Thread):
	
	def __init__(self, backlog, stats, stop_event):
		self.backlog = backlog
		self.stats = stats
		self.isstopped = stop_event
		self.start()
		

	# Get all links
	def start(self):
		domain = self.backlog.pop()
		while domain != None:
			logging.info("Crawling: " + domain)
			self.analyse(domain)
			
			if not self.isstopped.is_set():
				domain = self.backlog.pop()
			else:
				domain = None
				print ("Stopping thread..")

	
	def getPage(self, url):
		page = None
		try: 
			page = urlopen("http://" + url, timeout=3)
		except urllib.error.URLError as e:
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
			logging.debug("an error occured")
		return page
	
	# Get all links
	def analyse(self, url):
		OSTools = []
		#START Crawler
		page = self.getPage(url)
		links = []
		if page != None:
			try:
				html = page.read().decode("utf-8")
				soup = BeautifulSoup(html, "html.parser")
			except Exception as e:
				logging.info("Failed to process " + url)
				soup = None
			except UnicodeDecodeError as e:
				logging.info("Failed to process (No UTF-8)" + url)
			if soup != None:
				#analyse contents
				PageChecker = Checker(soup)
				OSTools = PageChecker.checkAll()
			
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
	