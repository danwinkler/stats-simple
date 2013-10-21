try:
	from ss_plugin import *
	import sys
	import logging
	import re
	import urllib2

	def web_correct_response_collector(args):
		try:
			response = urllib2.urlopen('http://docker-registry.appsoma.com:5000')
			html = response.read()
			return 1 if re.search( args, html ) else 0
		except Exception as e:
			logging.error( "web_correct_response: " + str(e) )
			return 0

	collectors['web_correct_response'] = web_correct_response_collector
except Exception, e:
	print "Could not load web_correct_response.py: " + str(e)