#!/usr/bin/env python

#
# A script that waits for a specific service to be up and running before it returns
# ex: waitforservice -n google -u http://www.google.com -c 10 -s 2000
#     tries to get a 200 response from the given URL by trying it 10 times with 2s inbetween
#
# waitforservice -h
#     to get detailed commandline help
#
# author: Per Arneng
#

import argparse
import sys
import time
import urllib2
import re
import socket

PROGRAM_NAME="waitforservice"

def main():

	parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
	parser.add_argument('-n', '--name', nargs='?', type=str, required=True , help="the name of the service to wait for")
	parser.add_argument("-u", "--url", nargs='?', type=str, required=True, help="the url ex: tcp://<host>:<port> or http://...")
	parser.add_argument("-c", "--count", nargs='?', type=int, default=60, help="the nr of times to try. less than 1 means forever. default = 100")
	parser.add_argument("-s", "--sleep", nargs='?', type=int, default=1000, help="sleep time in ms between tries. default = 1s")

	args = parser.parse_args()

	triers = [
		URLTrier('tcp://([^:]+):([0-9]+)', try_tcp),
		URLTrier('http://.*', try_http)
	]

	trier = None
	for t in triers:
		if t.canHandle(args.url):
			trier = t

	if trier is None:
		log('no registred trier for url \'%s\'' % (args.url))
		sys.exit(1)

	alive = wait_for_service(args.name, args.url, trier, args.count, args.sleep)
	if alive:
		log('\'%s\' is alive and kicking' % (args.name,))
		sys.exit(0)
	else:
		log('gave up on \'%s\'' % (args.name,))
		sys.exit(1)

def wait_for_service(name, url, trier, count, sleep):

	log("waiting for service '%s' on url '%s'" % (name, url))

	alive = False
	i=0
	while True:

		target = ''
		if count > 0:
			target = ' of %s' % (count)
 
		log('trying \'%s\' attempt %s%s' % (name, i+1, target))

		result = trier.try_url(url)
		if result:
			alive = True
			break;

		i += 1
		if i == count:
			alive = False
			break;

		time.sleep(sleep / 1000.0)

	return alive

def try_http(url):
	try:
		request = urllib2.Request(url)
		request.get_method = lambda : 'HEAD'

		response = urllib2.urlopen(request)
		if response.getcode() == 200:
			return True
		else:
			log('\'%s\' returned http status code %s. waiting for 200' % (response.getcode()))
	except urllib2.URLError as e:
		log("error: %s" % (e))
		return False

def try_tcp(url, host, port):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(3) # 3s timeout
	result = sock.connect_ex((host, int(port)))
	if result == 0:
		sock.close()
		return True

	sock.close()
	return False

class URLTrier:

	def __init__(self, regex, method):
		self.regex = re.compile(regex)
		self.method = method

	def canHandle(self, url):
		return re.match(self.regex, url) is not None

	def try_url(self, url):
		return self.method(url, *self.regex.match(url).groups())

def log(str):
	print '%s: %s' % (PROGRAM_NAME, str)

if __name__ == "__main__":
	main()
