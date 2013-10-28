import urllib, urllib2
import time
import json
import sys
import os
import logging

import thread
import threading
import atexit
import signal
import platform

to_send = []
to_send_lock = threading.RLock()

shutdown = False

def run():
	global cfg
	global collectors
	global annotators
	global send_auth
	
	#OPEN CONFIGURATION FILE
	try:
		f = open( "node.cfg" )
		j = f.read()
		f.close()
	except Exception as e:
		print "Could not load node.cfg: " + str( e )

	try:
		cfg = json.loads( j )
	except Exception as e:
		print "Could not parse node.cfg: " + str( e )

	#set up logging
	if "log" in cfg:
		numeric_level = getattr(logging, cfg["log"].upper(), None)
		if not isinstance(numeric_level, int):
			print "Invalid log level, defaulting to INFO"
			numeric_level = logging.INFO
	else:
		numeric_level = logging.INFO
		
	logging.basicConfig( level=numeric_level, filename='node.log' )

	root = logging.getLogger()

	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	root.addHandler(ch)

	logging.info( "Starting node" )

	#setup plugins
	get_plugins()

	import plugins
	collectors = plugins.ss_plugin.collectors
	annotators = plugins.ss_plugin.annotators
	send_auth = plugins.ss_plugin.send_auth

	server_reg()
	
	#Start collection thread
	thread.start_new_thread( collect_thread, ("",) )

	#Every once in a while check out the data list and send one of the items in it
	while not shutdown:
		try:
			if len( to_send ) > 0:
				data = to_send[0]
				jre = do_post( "/data", data )
				re = json.loads( jre )
				if "error" in re:
					logging.error( re['error'] )
					if( re['error'] == "NO_REG" ):
						server_reg()
				elif "success" in re:
					logging.info( "Successfully sent data - " + str(data["time"]) )
					with to_send_lock:
						to_send.remove( to_send[0] )
			else:
				logging.debug( "Nothing to send" )
			time.sleep( 3 )
		except (urllib2.HTTPError, IOError) as e:
			logging.error( "Failed to send: " + str(e) )
			time.sleep( 3 )

def collect_thread( args ):
	while not shutdown:
		start_time = time.time()
		
		notes = get_notes()
		data = get_data()
		t = int(time.time())
		data = json.dumps( data )
		to_put = { "name": cfg['name'], "time": t, "data": data, "notes": json.dumps( notes ) }

		with to_send_lock:
			to_send.append( to_put )
		
		logging.info( "Collected Data - " + str(t) )
		end_sleep = start_time + cfg['interval']
		while time.time() < end_sleep and not shutdown:
			time.sleep( 1 )

def server_reg():
	while not shutdown:
		try:
			jre = do_post( "/register", { "name": cfg['name'], "group": cfg.get( "group", "" ) } )
			re = json.loads( jre )
			if "error" in re:
				if( re["error"] == "WRONG_AUTH" ):
					logging.critical( "Authentication failed" )
					sys.exit( "Authentication failed" )
				logging.error( re['error'] )
				time.sleep( 1 )
				continue
			elif 'success' in re:
				logging.info( re['success'] )
				break
			else:
				logging.error( "Bad response from server" )
				time.sleep( 1 )
		except (urllib2.HTTPError, IOError) as e:
			logging.error( "Failed to Connect, Will try again in 10 seconds: " + str(e) )
			time.sleep( 10 )

def get_plugins():
	if not os.path.isdir( "plugins" ):
		os.mkdir( "plugins" )

	to_dl = ["__init__.py", "ss_plugin.py"]
	for val in cfg['data']:
		to_dl.append( val[1] + ".py" )

	if "annotators" in cfg:
		for val in cfg['annotators']:
			to_dl.append( val[0] + ".py" )

	if "auth" in cfg:
		for val in cfg['auth']:
			to_dl.append( val[0] + ".py" )

	for f in to_dl:
		try:
			logging.info( "Downloading Plugin: " + f )
			t = do_post( "/plugins", { "file": f }, False )
			fh = open( "plugins" + os.sep + f, "w" )
			fh.write( t )
			fh.close()
		except Exception, e:
			logging.error( "Could not download plugin: " + f + " :: " + str(e) )

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
			if d != None:
				data.append( { "name": val[0], "type": val[1], "data": d } )
		except KeyError as e:
			logging.error( "Incorrect data collector type in node.cfg: " + str( e ) )
	return data

def get_notes():
	global cfg
	notes = []
	if "annotators" in cfg:
		for val in cfg['annotators']:
			try:
				a = None
				if( len(val) == 1 ):
					a = annotators[val[0]]()
				else:
					a = annotators[val[0]](val[1])
				for note in a:
					notes.append( note )
			except KeyError as e:
				logging.error( "Incorrect annotator type in node.cfg: " + str( e ) )
	return notes

def stop_threads():
	global shutdown
	if not shutdown:
		logging.info( "Setting Shutdown Flag" )
		shutdown = True

def signal_handler( signum, frame ):
	stop_threads()

atexit.register( stop_threads )
signal.signal( signal.SIGTERM, signal_handler )
signal.signal( signal.SIGINT, signal_handler )

run()
logging.info( "EXIT" )