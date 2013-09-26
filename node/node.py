import urllib, urllib2
import time
import json
import sys
import psutil

def run():
	global cfg
	
	#OPEN CONFIGURATION FILE
	f = open( "node.cfg" )
	j = f.read()
	f.close()
	cfg = json.loads( j )

	#REGISTER WITH SERVER
	jre = do_post( "/register", { "name": cfg['name'] } )

	re = json.loads( jre )
	if "error" in re:
		sys.exit( re['error'] )
	if not re['success']:
		sys.exit( "Node could not register with server" )

	#Every interval send data
	while True:
		data = get_data()
		jre = do_post( "/data", { "name": cfg['name'], "time": int(time.time()), "data": json.dumps( data ) } )
		re = json.loads( jre )
		if "error" in re:
			print re['error']
		time.sleep( cfg['interval'] )

def do_post( url, values ):
	global cfg
	values['secret'] = cfg['secret']
	url = "http://" + cfg['server'] + url
	data = urllib.urlencode( values )
	req = urllib2.Request( url, data )
	response = urllib2.urlopen( req )
	return response.read()
	
def get_data():
	global cfg
	data = {}
	for val in cfg['data']:
		if val == "cpu_percent":
			data['cpu_percent'] = psutil.cpu_percent( interval=1, percpu=True )
	return data
run()
	