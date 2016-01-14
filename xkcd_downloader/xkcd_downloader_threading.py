# Imports from standard library
import sys
import threading
from time import time

# Import from module download that is in the same directory
import download


class Downloader(threading.Thread):
	def __init__(self, directory, urlrange, id):
		threading.Thread.__init__(self)
		self.directory = directory
		self.urlrange = urlrange
		self.id = id
		
	def run(self):
		for i in range(self.urlrange, 0, -4):
			print("Downloading image number {} in thread {}".format(i, self.id))
			url = "http://xkcd.com/" + str(i)
			print("url: {}".format(url))
			try:
				download.getlink(url, self.directory, i)
				print("Downloaded\n")
			except Exception as e:
				url = url[0:-5]
			

def main():
	"""
		Main function
	"""
	try:
		ts = time()
		print("Start")
		url = "http://xkcd.com/1629/"
		directory = download.setupdir()
		url1 = int(url[-5:-1])
		url2 = url1 - 1
		url3 = url1 - 2
		url4 = url1 - 3
		
		
		threads = []

		thread1 = Downloader(directory, url1, 1)
		thread2 = Downloader(directory, url2, 2)
		thread3 = Downloader(directory, url3, 3)
		thread4 = Downloader(directory, url4, 4)
		
		thread1.start()
		thread2.start()
		thread3.start()
		thread4.start()
		
		threads.append(thread1)
		threads.append(thread2)
		threads.append(thread3)
		threads.append(thread4)

		for t in threads:
			t.join()
		
		print("We are done!")		
		print("Time taken: {}s".format(time() - ts))
			
	except KeyboardInterrupt:
		print("\n\n--------\nGoodbye\n--------\n")
		sys.exit(0)
		
	
if __name__ == "__main__":
	main()