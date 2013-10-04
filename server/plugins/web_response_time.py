from ss_plugin import *
import psutil
import requests
import sys

def web_response_time_collector(args):
	try:
		response = requests.get(args, verify=False)
		return response.elapsed.total_seconds()
	except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.TooManyRedirects, requests.exceptions.Timeout) as e:
		return 0;
	except requests.exceptions.URLRequired:
		sys.exit( "Invalid URL for web_response_time" )

collectors['web_response_time'] = web_response_time_collector