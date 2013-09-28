from ss_collect import *
import psutil

def web_status_collector(args):
	nf = urllib.urlopen(args)
	start = time.time()
	page = nf.read()
	end = time.time()
	nf.close()
	return end-start

collectors['web_status'] = web_status_collector