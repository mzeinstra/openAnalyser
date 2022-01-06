import json

fileName = "collections.json"
collection = {}
try:
	f = open(fileName)
	collection = json.load(f)
except IOError:
	collection = {}
finally:
	f.close()
	
headers = {}
for website in collection:
	if 'headers' in collection[website]:	
		for header in collection[website]['headers']:
			if header in headers:
				headers[header] += 1
			else:
				headers[header] = 1
		
#print(headers)
#for k, v in headers.items():
#    print ("{:<50} {:<15}".format(k, v))
	
interesting = {}
interestingHeaders = ["Set-Cookie", "X-Powered-By", "server", "X-Pingback", "x-powered-by", "X-Drupal-Cache", "X-Generator", "set-cookie", "X-Drupal-Dynamic-Cache", "X-Clacks-Overhead", "X-SERVER", "X-LiteSpeed-Cache", "Hummingbird-Cache", "X-Server", "X-Developer", "X-Shop-Id", "X-Served-by", "X-Served-By", "X-Server-Powered-By", "SERVER", "X-Litespeed-Cache", "X-Server-Id"]
for website in collection:
	if 'headers' in collection[website]:	
		for header in interestingHeaders:
			if header in collection[website]['headers']:
				if not header in interesting:
					interesting[header] = {}
				v = collection[website]['headers'][header].lower()
				if v in interesting[header]:
					interesting[header][v] += 1
				else:
					interesting[header][v] = 1

for key, data in interesting.items():
	for header, value in data.items():
		print (key, "\t", header, "\t", value, "\t")