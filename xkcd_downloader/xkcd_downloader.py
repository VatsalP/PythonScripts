import sys
from time import time

import download

def main():
	try:
		ts = time()
		print("Start")
		url = "http://xkcd.com/1629/"
		directory = download.setupdir()
		urlrange = int(url[-5:-1])
		url = url[0:-5]
					
		for i in range(urlrange, 0, -1):
			print("Downloading image number {}".format(i))
			url = "http://xkcd.com/" + str(i)
			print("url: {}".format(url))
			try:
				download.getlink(url, directory, i)
				print("Downloaded\n")
			except Exception as e:
				url = url[0:-5]
				
		print("Time taken: {}s".format(time() - ts))
			
	except KeyboardInterrupt:
		print("\n\n--------\nGoodbye\n--------\n")
		sys.exit(0)
		
	
if __name__ == "__main__":
	main()