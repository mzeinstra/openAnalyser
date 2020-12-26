import threading
import logging
import os

class Stats(object):
	def __init__(self):
		self.lock = threading.Lock()  
		self.stats = {}
		self.stats['visited'] = 0
	
	def update(self, results):
		logging.debug('Waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Acquired lock')
			for tool in results:
				if tool in self.stats:
					self.stats[tool] = self.stats[tool] + 1
				else:
					self.stats[tool] = 1
			self.stats['visited'] = self.stats['visited'] + 1
		except:
			raise
		finally:
			self.lock.release()

	def getStats(self):
		logging.debug('Waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Acquired lock')
			return self.stats
		except:
			raise
		finally:
			self.lock.release()
	
	def printStats(self):
		logging.debug('Waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Acquired lock')
			os. system('clear')
			for stat in self.stats:
				print (stat + ": " + str(self.stats[stat]))
		except:
			raise
		finally:
			self.lock.release()