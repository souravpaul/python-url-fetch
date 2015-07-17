import requests
import threading
from requests.exceptions import ConnectionError
import os

class urlFetch(threading.Thread):
	def __init__(self,url,threadID):
		threading.Thread.__init__(self)
		self.url=url
		self.threadID=threadID
	
	def run(self):
		self.fetchURL()

	#Fetching content with url and return response
	def getURLResponse(self,url):
		response=requests.get(url)
		response.encoding='ISO-8859-1'
		return response

	#Write URL content to a file
	def writeContents(self,fileName,response):
		fileName=fileName.replace(" ","")
		fileName=fileName.replace("https://","")
		fileName=fileName.replace("http://","")
		fileName=fileName.replace("www.","")
		fileName=fileName.replace("/","_")
		fileName='data/'+fileName
		fileObj=file(fileName,'wb+')
		for chunk in response.iter_content((1024 * 5)):
			fileObj.write(chunk)
		fileObj.close()
	
	#Controlling the fetching operation
	def fetchURL(self):
		url=self.url
		url=url.strip()
		#print self.threadID," -  Fetching started "
		try:
			response=self.getURLResponse(url)
			if response.status_code==200:
				self.writeContents(url,response)
				print self.threadID," ",url," - Success"
			else:
				print self.threadID," ",url," - Can\'t read Status Code:",response.status_code
		except ConnectionError as e:
			print self.threadID," ",url," - Failed: Connection Error"
		except Exception as e:
			print self.threadID," ",url," - Failed: SSLError ",e

#Read urls from a text files and return a list of urls
def readURLs(fileName):
	fileObj=file(fileName,'rb')
	urls=fileObj.readlines()
	fileObj.close()
	return urls

#read Url
urls=readURLs('urls.txt')

#Creating output content directory
if os.path.isdir('data')==False:
	os.mkdir('data',0755)

#Creating threads for url fetching operation and start
for count in range(len(urls)):
	urlFetch(urls[count],count).start()
