import os
import shutil
from pathlib import Path

"""
Time taken to downalod 1629 image:
Single thread: 86 minutes
Two Threads: 42 minutes
Three Threads: 21.5 minutes
"""

import requests
from bs4 import BeautifulSoup

def setupdir():
	"""
	Checks for directory named images
	in the working directory.
	And makes the directory if it doesn't exists.
	"""
	dir = Path('images')
	if not dir.exists():
		dir.mkdir()
	return dir
	
def getlink(url, directory, number):
	"""
	Fetches the link from xkcd image using bs4.
	And calls the function downloadlink()
	"""
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'lxml')
	reqimg = soup.findAll('img')[1].get('src')
	name = str(number) + "-" + reqimg[23:]
	reqimg = "http:" + reqimg
	downloadlink(reqimg, directory, name)
	
def downloadlink(url, directory, name):
	"""
	Gets the image and saves it to the appropriate name
	"""
	download_path = Path(directory).resolve()
	download_path = download_path / os.path.basename(name)
	response = requests.get(url, stream=True)
	with open(str(download_path), 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)

