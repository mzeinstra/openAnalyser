import threading
import logging

class Backlog(object):
	def __init__(self, toParseList, parsedList):
		self.lock = threading.Lock() 
		self.toParse = self.loadProgess(toParseList)
		self.parsed = self.loadProgess(parsedList)
	
	def pop(self):
		logging.debug('Backlog waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Backlog acquired lock')
			if len(self.toParse) > 0:
				url = self.toParse.pop(0)
				if url not in self.parsed:
					self.parsed.append(url)
				return url
			else:
				return None
		except:
			raise
		finally:
			self.lock.release()

	def append(self, urls):
		logging.debug('Backlog waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Backlog acquired lock')
			added = 0
			duplicates = 0
			for url in urls:
				if url not in self.toParse and url not in self.parsed:
					self.toParse.append(url)
					added += 1
				else:
					duplicates += 1
		except:
			raise
		finally:
			self.lock.release()

	
	def loadProgess(self, fileName):
		# define an empty list
		returnList = []
		try:
			f = open(fileName, 'r')
			# open file and read the content in a list
			for line in f:
				# remove linebreak which is the last character of the string
				currentLink = line[:-1]
				# add item to the list
				returnList.append(currentLink)
			f.close()
		except IOError:
			#create file for storing progress
			print(filename + " not accessible, creating..")
			with open(fileName, 'w'): pass
		finally:
			return returnList
			
	def count(self):
		logging.debug('Backlog.count waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Backlog.count acquired lock')
			return len(self.toParse)
		except:
			raise
		finally:
			self.lock.release()
	
		
		
	def safeprogress(self):
		logging.info("Saving...")
		with open('toParse.txt', 'w') as filehandle:
			for listitem in self.toParse:
				filehandle.write('%s\n' % listitem)
		with open('parsed.txt', 'w') as filehandle:
			for listitem in self.parsed:
				filehandle.write('%s\n' % listitem)