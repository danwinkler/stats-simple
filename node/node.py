import urllib, urllib2
import time
import json
import sys
import psutil
import os

def run():
	global cfg
	global collectors
	
	#OPEN CONFIGURATION FILE
	f = open( "node.cfg" )
	j = f.read()
	f.close()
	cfg = json.loads( j )
	
	server_reg()

	get_collectors()

	import datacollectors
	collectors = datacollectors.ss_collect.collectors

	#Every interval send data
	while True:
		try:
			data = get_data()
			jre = do_post( "/data", { "name": cfg['name'], "time": int(time.time()), "data": json.dumps( data ) } )
			re = json.loads( jre )
			if "error" in re:
				print re['error']
				if( re['error'] == "NO_REG" ):
					server_reg()
			elif "success" in re:
				print "Successfully sent data"
			time.sleep( cfg['interval'] )
		except (urllib2.HTTPError, IOError) as e:
			print "Failed to send: " + str(e)
			time.sleep( cfg['interval'] )

def server_reg():
	while True:
		try:
			jre = do_post( "/register", { "name": cfg['name'] } )
			re = json.loads( jre )
			if "error" in re:
				if( re["error"] == "WRONG_SECRET" ):
					sys.exit( "Secret in node.cfg does not match server's secret" )
				print re['error']
				continue
			elif 'success' in re:
				print re['success']
				break
			else:
				print "Bad response from server"
		except (urllib2.HTTPError, IOError) as e:
			print "Failed to Connect, Will try again in 10 seconds: " + str(e)
			time.sleep( 10 )

def get_collectors():
	if not os.path.isdir( "datacollectors" ):
		os.mkdir( "datacollectors" )

	to_dl = ["__init__.py", "ss_collect.py"]
	for val in cfg['data']:
		to_dl.append( val[1] + ".py" )

	for f in to_dl:
		t = do_post( "/datacollectors", { "file": f } )
		if "WRONG_SECRET" in t:
			continue
		fh = open( "datacollectors" + os.sep + f, "w" )
		fh.write( t )
		fh.close()

def do_post( url, values ):
	global cfg
	values['secret'] = cfg['secret']
	url = cfg['server'] + url
	if( "://" not in url ):
		url = "http://" + url
	data = urllib.urlencode( values )
	req = urllib2.Request( url, data )
	response = urllib2.urlopen( req )
	return response.read()
	
def get_data():
	try:
		global cfg
		data = []
		for val in cfg['data']:
			d = None
			if( len(val) == 2 ):
				d = collectors[val[1]]()
			else:
				d = collectors[val[1]](val[2])
			data.append( { "name": val[0], "type": val[1], "data": d } )
		return data
	except KeyError as e:
		sys.exit( "Incorrect data collector type in node.cfg: " + str(e) )
	
run()
	