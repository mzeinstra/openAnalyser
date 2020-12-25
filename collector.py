import threading
import logging
import json

class Collector(object):
	collection = {}
	
	def __init__(self, collectionFile):
		self.lock = threading.Lock() 
		self.loadProgess(collectionFile)

	def append(self, dataset):
		logging.debug('Collector waiting for lock')
		self.lock.acquire()
		try:
			logging.debug('Collector acquired lock')
			for key in dataset:
				if key in self.collection:
					self.collection[key] += 1
				else:
					self.collection[key] = 1
			
		except:
			raise
		finally:
			self.lock.release()

	def loadProgess(self, fileName):
		try:
			f = open(fileName)
			self.collection = json.load(f)
		except IOError:
			print(filename + " not accessible, creating..")
			with open(fileName, 'w'): pass	
		finally:
			f.close()			
		
	def safeprogress(self):
		logging.info("Saving...")
		with open('collections.json', 'w') as json_file:
			json.dump(self.collection, json_file)
		print(self.collection)