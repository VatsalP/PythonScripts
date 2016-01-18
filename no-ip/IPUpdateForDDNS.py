#!/usr/bin/env python
"""
	IP update script for ddns of no-ip.com
	
	Usage: IPUpdateForDDNS.py [-h] username password hostname
	Syncs your current IP with you no-ip host or domain

	positional arguments:
		username    username at no-ip
		password    password at no-ip
		hostname    hostname at no-ip

	optional arguments:
		-h, --help  show this help message and exit
"""
import argparse
import logging
from time import strftime

import requests

def main():
	try:
		#####################################################
		#	 		Parsing of command line options			#
		#####################################################
		parser = argparse.ArgumentParser(
			description='Syncs your current IP with you no-ip host or domain'
			)
		parser.add_argument('username', type=str, 
			help='username at no-ip'
			)
		parser.add_argument('password', type=str, 
			help='password at no-ip'
			)
		parser.add_argument('hostname', type=str, 
			help='hostname at no-ip'
			)
		args = parser.parse_args()
		username = args.username
		password = args.password
		dname = args.hostname
		
		
		#####################################################
		#	 Creation of log file and finding the public	#
		#####################################################
		logging.basicConfig(filename='no-ip.log',level=logging.INFO)
		ip = requests.get('https://api.ipify.org').text
		timestring = strftime('%X %x %Z')
		logging.info(" {}: Your Public IP is: {}".format(timestring, ip))
		
		
		#####################################################
		#	 		Updating and logging the result			#
		#####################################################
		url = "http://{}:{}@dynupdate.no-ip.com/nic/update?hostname={}&myip={}".format(username, password, dname, ip)
		r = requests.get(url)
		timestring = strftime('%X %x %Z')
		logging.info(" {}: {}".format(timestring, r.text))
		
	except Exception as e:
		timestring = strftime('%X %x %Z')
		exception = "Exception: " + str(e) + " at " + timestring
		logging.error(exception)
	
if __name__ == '__main__':
	main()