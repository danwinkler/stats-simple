import urllib, urllib2
import time
import json
import sys
import os

def run():
	global cfg
	global collectors
	global send_auth
	
	#OPEN CONFIGURATION FILE
	f = open( "node.cfg" )
	j = f.read()
	f.close()
	cfg = json.loads( j )
	
	get_plugins()

	import plugins
	collectors = plugins.ss_plugin.collectors
	send_auth = plugins.ss_plugin.send_auth

	server_reg()

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
				if( re["error"] == "WRONG_AUTH" ):
					sys.exit( "Authentication failed" )
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

def get_plugins():
	if not os.path.isdir( "plugins" ):
		os.mkdir( "plugins" )

	to_dl = ["__init__.py", "ss_plugin.py"]
	for val in cfg['data']:
		to_dl.append( val[1] + ".py" )

	if "auth" in cfg:
		for val in cfg['auth']:
			to_dl.append( val[0] + ".py" )

	for f in to_dl:
		t = do_post( "/plugins", { "file": f }, False )
		fh = open( "plugins" + os.sep + f, "w" )
		fh.write( t )
		fh.close()

def do_post( url, values, auth=True ):
	global cfg
	if auth and "auth" in cfg:
		values['auth'] = get_auth()
	url = cfg['server'] + url
	if( "://" not in url ):
		url = "http://" + url
	data = urllib.urlencode( values )
	req = urllib2.Request( url, data )
	response = urllib2.urlopen( req )
	return response.read()

def get_auth():
	global cfg
	auths = {}
	for val in cfg["auth"]:
		a = None
		if( len(val) == 1 ):
			a = send_auth[val[0]]()
		else:
			a = send_auth[val[0]](val[1])
		auths[val[0]] = a
	return json.dumps( auths )
	
def get_data():
	global cfg
	data = []
	for val in cfg['data']:
		try:
			d = None
			if( len(val) == 2 ):
				d = collectors[val[1]]()
			else:
				d = collectors[val[1]](val[2])
			data.append( { "name": val[0], "type": val[1], "data": d } )
		except KeyError as e:
			print "Incorrect data collector type in node.cfg: " + str( e )
	return data

run()
	