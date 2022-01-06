from bs4 import BeautifulSoup
import re

class Checker():
	def __init__(self, soup, SiteInfo):
		self.Scripts = []
		self.Links = []
		self.Generators = []
		self.SiteInfo = SiteInfo
		self.page = soup
		
		
		Links = self.page.find_all('script')
		for link in Links:
			if link.get('src') != None:
				self.Scripts.append(link.get('src')) 
		self.SiteInfo['scripts'] = self.Scripts
		
		Links = self.page.find_all('link')
		for link in Links:
			if link.get('src') != None:
				self.Links.append(link.get('href'))
		self.SiteInfo['links'] = self.Links
		
		generators = self.page.find_all('meta',attrs={'name':'generator'})
		for tag in generators:
			self.Generators.append(tag['content'])
		self.SiteInfo['generators'] = self.Generators
		return
	
	def getGenerators(self):
		return self.Generators

	def checkScripts (self, occurances):
		for link in self.Scripts:
			for occurance in occurances:
				if re.search(occurance, link, re.IGNORECASE):
					return True
	
	def checkLinks (self, occurances):
		if len(occurances) > 0 and len(self.Links) > 0:
			for link in self.Links:
				for occurance in occurances:
					if re.search(occurance, link, re.IGNORECASE):
						return True
		return False
					
	def checkGenerators (self, occurances):
		for link in self.Generators:
			for occurance in occurances:
				if re.search(occurance, link, re.IGNORECASE):
					return True
					
	def checkPoweredByHeader(self, occurances):
		if "X-Powered-By" in self.SiteInfo:
			if isinstance(self.SiteInfo['X-Powered-By'], str):
				if self.SiteInfo['X-Powered-By'] in occurances:
					return True
			elif isinstance(self.SiteInfo['X-Powered-By'], list):
				for link in self.SiteInfo['X-Powered-By']:
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
		if self.checkJQuery():
			OpenSourceTools.append("jQuery")
		if self.checkVUE():
			OpenSourceTools.append("VUE.js")
		if self.checkReact():
			OpenSourceTools.append("React.js")
		if self.checkGoogleFonts():
			OpenSourceTools.append("Google Fonts")
		#Keycloak
		#kc_session in setcookie
		
		#OS
		
		#Languages
		#ASP.net (asp.net in set-cookie headers names)
		
		if self.checkPHP():
			OpenSourceTools.append("PHP")
		#Laravel PHP framework
		#laravel is in setcookie
		
		
		
		#return found
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
		#concrete5 is also a part of set-cookie header name
	
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
		# Add check if set-cookie header contains phpsessid

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
		occurances = ["fonts.googleapis.com/","https://ajax.googleapis.com/ajax/libs/webfont/"]
		if self.checkScripts(occurances):
			return True
		return False