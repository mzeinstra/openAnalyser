import threading
import logging
import json

class Collector(object):
	collection = {}
	
	def __init__(self, collectionFile):
		self.lock = threading.Lock() 
		self.collectionFile = collectionFile
		if collectionFile != None:
			self.loadProgess()
		

	def append(self, site, dataset):
		logging.debug('Collector waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Collector acquired lock')
			self.collection[site] = dataset
		except:
			raise
		finally:
			self.lock.release()

	def loadProgess(self):
		try:
			f = open(self.collectionFile)
			self.collection = json.load(f)
		except IOError:
			self.collection = {}
		finally:
			f.close()			
		
	def safeprogress(self):
		if self.collectionFile == None:
			print("Safe not possible, no known location")
			logging.info("Safe not possible, no known location")
		else:
			logging.info("Saving... Collections")
			with open(self.collectionFile, 'w') as json_file:
				json.dump(self.collection, json_file)
	
	def getCollection(self):
		logging.debug('Collector waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Collector acquired lock')
			return self.collection
		except:
			raise
		finally:
			self.lock.release()
	