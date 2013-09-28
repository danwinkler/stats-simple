from ss_collect import *
import psutil
import requests

def web_response_time_collector(args):
	response = requests.get(args)
	return float(str(response.elapsed).split(":")[2])

collectors['web_response_time'] = web_response_time_collector