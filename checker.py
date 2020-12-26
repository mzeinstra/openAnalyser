from bs4 import BeautifulSoup
import re

class Checker():
	def __init__(self, soup, poweredByHeaders):
		self.Scripts = []
		self.Links = []
		self.Generators = []
		self.PoweredByHeaders = poweredByHeaders
		self.page = soup
		
		
		Links = self.page.find_all('script')
		for link in Links:
			if link.get('src') != None:
				self.Scripts.append(link.get('src')) 
		
		Links = self.page.find_all('link')
		for link in Links:
			if link.get('src') != None:
				self.Links.append(link.get('href'))
		
		generators = self.page.find_all('meta',attrs={'name':'generator'})
		for tag in generators:
			self.Generators.append(tag['content'])
		return
	
	def getGenerators(self):
		return self.Generators

	def checkScripts (self, occurances):
		for link in self.Scripts:
			for occurance in occurances:
				if re.search(occurance, link, re.IGNORECASE):
					return True
	
	def checkLinks (self, occurances):
		for link in self.Links:
			for occurance in occurances:
				if re.search(occurance, link, re.IGNORECASE):
					return True
					
	def checkGenerators (self, occurances):
		for link in self.Generators:
			for occurance in occurances:
				if re.search(occurance, link, re.IGNORECASE):
					return True
					
	def checkPoweredByHeader(self, occurances):
		for link in self.PoweredByHeaders:
			for occurance in occurances:
				if re.search(occurance, link, re.IGNORECASE):
					return True

	def checkAll(self):	
		OpenSourceTools = []
		
		#CMS
		if self.checkWordpress():
			OpenSourceTools.append("Wordpress")
			# also check for WooCommerce - ecommerce platform
			if self.checkWooCommerce():
				OpenSourceTools.append("WooCommerce")
		if self.checkTYPO3():
			OpenSourceTools.append("TYPO3")
		if self.checkPrestaShop():
			OpenSourceTools.append("PrestaShop")
		if self.checkDrupal():
			OpenSourceTools.append("Drupal")
		if self.checkJoombla():
			OpenSourceTools.append("Joombla")
		if self.checkPlone():
			OpenSourceTools.append("Plone")
		if self.checkConcrete5():
			OpenSourceTools.append("Concrete5")
		
		#Libraries
		if self.checkPHP():
			OpenSourceTools.append("PHP")
		if self.checkJQuery():
			OpenSourceTools.append("jQuery")
		if self.checkVUE():
			OpenSourceTools.append("VUE.js")
		if self.checkReact():
			OpenSourceTools.append("React.js")
		if self.checkGoogleFonts():
			OpenSourceTools.append("Google Fonts")
		return OpenSourceTools


	#### CHECKS ####
		
	def checkWordpress(self):
		occurances = ["wordpress", "wp-admin", "wp-content", "wp-embed","wp-includes", "wp-json"]
		if self.checkGenerators(occurances):
			return True
		if self.checkLinks(occurances):
			return True
		if self.checkScripts(occurances):
			return True
		return False
	
	def checkWooCommerce(self):
		occurances = ["WooCommerce"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
		return False
	
	def checkTYPO3(self):
		occurances = ["TYPO3"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	def checkPrestaShop(self):
		occurances = ["PrestaShop"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	def checkDrupal(self):
		occurances = ["Drupal"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	def checkJoombla(self):
		occurances = ["Joombla"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	def checkPlone(self):
		occurances = ["Plone"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	def checkConcrete5(self):
		occurances = ["concrete5"]
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	def checkContao(self):
		occurances("Contao Open Source CMS")
		if self.checkGenerators(occurances):
			return True
		if self.checkScripts(occurances):
			return True
	
	#Libraries
	def checkPHP(self):
		occurances = ["php"]
		if self.checkPoweredByHeader(occurances):
			return True

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
	
	def checkGoogleFonts(self):
		occurances = ["fonts.googleapis.com/"]
		if self.checkLinks(occurances):
			return True
		return False