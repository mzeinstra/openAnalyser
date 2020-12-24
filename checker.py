from bs4 import BeautifulSoup
import re

class Checker():
	def __init__(self, soup):
		self.Scripts = []
		self.Links = []
		self.page = soup
		
		
		Links = self.page.find_all('script')
		for link in Links:
			if link.get('src') != None:
				self.Scripts.append(link.get('src')) 
		Links = self.page.find_all('link')
		for link in Links:
			if link.get('src') != None:
				self.Links.append(link.get('href'))
		return

	def checkScripts (self, occurances):
		for link in self.Scripts:
			for occurance in occurances:
				if link.find(occurance) != -1:
					return True
	
	def checkLinks (self, occurances):
		for link in self.Links:
			for occurance in occurances:
				if link.find(occurance) != -1:
					return True

	def checkAll(self):
		OpenSourceTools = []
		if self.checkWordpress():
			OpenSourceTools.append("Wordpress")
		if self.checkJQuery():
			OpenSourceTools.append("jQuery")
		if self.checkVUE():
			OpenSourceTools.append("VUE.js")
		if self.checkReact():
			OpenSourceTools.append("React.js")
		return OpenSourceTools


	#### CHECKS ####
		
	def checkWordpress(self):
		occurances = ["wordpress", "wp-admin", "wp-content", "wp-embed","wp-includes", "wp-json"]
		if self.checkLinks(occurances):
			return True
		if self.checkScripts(occurances):
			return True
		return False
	
	def checkJQuery(self):
		occurances = ["jquery"]	
		if self.checkLinks(occurances):
			return True
		if self.checkScripts(occurances):
			return True
		return False

	def checkVUE(self):
		occurances = ["vue.js","vue.min.js", "unpkg.com/vue"]	
		if self.checkScripts(occurances):
			return True
		return False
	
	def checkReact(self):
		occurances = ["unpkg.com/react", "react.js"]
		if self.checkScripts(occurances):
			return True
		return False