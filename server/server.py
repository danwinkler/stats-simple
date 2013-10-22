from bottle import route, run, template, request, static_file
from bottle.ext import sqlite
import bottle
import json
import time
import datetime
import thread
import sqlite3
import os
from triggers import *
import plugins
import smtplib
import time
from email.mime.text import MIMEText

# ----------------------------------
# --------------SETUP---------------
# ----------------------------------

# Ugly but whatever
time_dict = { "second": 1, "minute": 60, "hour": 60*60, "day": 60*60*24, "month": 60*60*24*30, "year": 60*60*24*365 }

f = open( "server.cfg" )
j = f.read()
f.close()
cfg = json.loads( j )

#Defaults
if "graph_width" not in cfg:
	cfg["graph_width"] = 420

if "graph_height" not in cfg:
	cfg["graph_height"] = 100


# Trigger Thread
def trigger_thread( args ):
	time.sleep( 1 ) #hackety hackety way to make sure that email_on_alerts is defined by the time this runs
	while True:
		for t in cfg['triggers']:
			ss_triggers.triggers[t]()
		if "email" in cfg:
			email_on_alerts()
		time.sleep( 300 )

if "triggers" in cfg:
	thread.start_new_thread( trigger_thread, ("",) )

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='db.db')
app.install(plugin)

# ---------------------------------
# -------------ROUTES--------------
# ---------------------------------

@app.post('/register')
def register(db):
	if not check_secret():
		ssprint( "Authentication Failed" )
		return json.dumps( { "error": "WRONG_AUTH" } )
	name = request.forms.name
	if not name:
		ssprint( "Client tried to register with no name set" )
		return json.dumps( { "error": "NO_NAME" } )
	row = db.execute('SELECT * from nodes where name=?', (name,)).fetchone()
	if row:
		ssprint( "Register Success: Already Registered: " + str(row['name']) )
		return json.dumps( { "success": "ALREADY_REGISTERED" } )
	else:
		db.execute('INSERT into nodes (name) VALUES (?)', (name,))
		ssprint( "Register Success: First time register: " + str( name ) )
		return json.dumps( { "success": "REGISTERED" } )

@app.post('/data')
def post_data(db):
	if not check_secret():
		return json.dumps( { "error": "WRONG_AUTH" } )
	name = request.forms.name
	if not name:
		return json.dumps( { "error": "NO_ID" } )
	row = db.execute('SELECT * from nodes where name=?', (name,)).fetchone()
	if not row:
		return json.dumps( { "error": "NO_REG" } )
	time = request.forms.time
	data = json.loads( request.forms.data )
	if not time:
		return json.dumps( { "error": "NO_TIME" } )
	if not data:
		return json.dumps( { "error": "NO_DATA" } )
	
	if hasattr( request.forms, 'notes' ):
		notes = json.loads( request.forms.notes )
		for note in notes:
			db.execute( 'INSERT into notes (node,note,time) VALUES (?,?,?)', (row['id'],note,int(time)) )

	for d in data:
		db.execute( 'INSERT into data (node,time,name,type,value) VALUES (?,?,?,?,?)', (row['id'],int(time),d['name'], d['type'],json.dumps( d['data'] )) )
	return json.dumps( { "success": "VALUES_ENTERED" } )

@app.post('/plugins')
def post_plugins():
	fh = open( "plugins" + os.sep + request.forms.file )
	t = fh.read()
	fh.close()
	return t

@app.get("/data/:node/:name/:time/:end")
def get_data(node,name,time,end,db):
	return "[]"
	
@app.get("/data/:node/:name/:start")
def get_data(node,name,start,db):
	timearr = start.split( ":" )
	if( timearr[0] == "forever" ):
		return get_data(node,name,db)
	time_ago = time.time() - (time_dict[timearr[0]] * int(timearr[1]))
	
	rows = db.execute('SELECT value, time from data where node=? AND name=? AND time >= ?', (int(node),name,time_ago) ).fetchall()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "value": json.loads( row['value'] ) } )
	return json.dumps( data )
	
@app.get("/data/:node/:name")
def get_data(node,name,db):
	rows = db.execute('SELECT value, time from data where node=? AND name=?', (int(node),name) ).fetchall()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "value": json.loads( row['value'] ) } )
	return json.dumps( data )

@app.get("/notes/:node/:start")
def get_notes(node,start,db):
	timearr = start.split( ":" )
	if( timearr[0] == "forever" ):
		return get_notes(node,db)
	time_ago = time.time() - (time_dict[timearr[0]] * int(timearr[1]))
	
	rows = db.execute('SELECT note, time from notes where node=? AND time >= ?', (int(node),time_ago) ).fetchall()
	notes = []
	for row in rows:
		notes.append( { "time": row['time'], "note": row['note'] } )
	return json.dumps( notes )

@app.get("/notes/:node")
def get_notes(node,db):
	rows = db.execute('SELECT note, time from notes where node=?', (int(node),) ).fetchall()
	notes = []
	for row in rows:
		notes.append( { "time": row['time'], "note": row['note'] } )
	return json.dumps( notes )

@app.get('/nodes')
def get_nodes(db):
	rows = db.execute('SELECT id,name from nodes').fetchall()
	nodes = []
	for row in rows:
		nodes.append( { "id": row['id'], "name": row['name'] } )
	return json.dumps( nodes )
	
@app.get('/nodeid/:name')
def get_node_id(name,db):
	row = db.execute('SELECT id from nodes where name=?', (name,)).fetchone()
	return json.dumps( row['id'] )

@app.get('/typeof/:name')
def get_typeof(name, db):
	row = db.execute('SELECT DISTINCT name, type from data where name=?', (name,)).fetchone()
	return json.dumps( row['type'] )
	
@app.get('/nodeinfo/:node')
def get_nodes(node, db):
	rows = db.execute('SELECT DISTINCT name, type from data where node=?', (node,)).fetchall()
	names = []
	for row in rows:
		names.append( {"name": row['name'], "type":row['type']} )
	return json.dumps( names )

# :path is a bottle filter that matches strings with '/' in them
@app.route('/static/<filename:path>')
def server_static(filename):
	return static_file(filename, root='static/')

@app.route('/screen/:screen')
@app.route('/')
def index(screen=None):
	options = { 
		"user_select": json.dumps( screen == None ), 
		"data": json.dumps( cfg["screens"][screen] ) if (screen!=None and screen in cfg["screens"]) else "[]", 
		"cfg": parse_query_for_cfg(),
	}
	return template("index", options )

@app.route('/custom/:screen')
def index(screen):
	arr = json.loads( screen )
	print arr
	screen = json.dumps( arr )
	return template("index", { "user_select": json.dumps( False ), "data": screen, "cfg": parse_query_for_cfg() } )

# ---------------------------------
# --------HELPER FUNCTIONS---------
# ---------------------------------

def parse_query_for_cfg():
	global cfg
	pcfg = cfg.copy();
	if request.query.graph_width:
		pcfg['graph_width'] = request.query.graph_width
	if request.query.graph_height:
		pcfg['graph_height'] = request.query.graph_height
	return pcfg

def email_on_alerts():
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	time_ago = time.time() - (60*60*24)
	unique_alerts_last_day = db.execute('SELECT DISTINCT name from alerts where time >= ?', (time_ago,) ).fetchall()
	for name_row in unique_alerts_last_day:
		#Select all alerts from last day
		rows = db.execute('SELECT id, time, value, sentmail FROM alerts where name = ? AND time >= ?', (name_row['name'], time_ago)).fetchall()
		#If only one alert in the last day and we havent sent email for it
		if len( rows ) == 1 and rows[-1]['sentmail'] != 1:
			send_email( name_row['name'], datetime.datetime.fromtimestamp(int(rows[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S') + " " + rows[-1]['value'] )
			db.execute( "UPDATE alerts SET sentmail=1 where id=?", (rows[-1]['id'],))
		elif len( rows ) > 1:
			send_mail = True
			#look for continous block recently that we didnt send mail for
			for i in xrange( len( rows )-1, 0, -1 ):
				a = rows[i]
				b = rows[i-1]
				if a['sentmail']:
					send_mail = False
					break
				if a['time'] - b['time'] > 20*60:
					break
			if send_mail:
				#If we havent sent an email for this type of alert, send an email with all the alerts from the last day
				email_str = ""
				rows = db.execute('SELECT id, value, sentmail, time FROM alerts where name = ? AND time >= ?', (name_row['name'], time_ago)).fetchall()
				for row in rows:
					email_str += datetime.datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d %H:%M:%S')
					email_str += " " + row['value'] + "\n"
				send_email( name_row['name'], email_str )
				db.execute( "UPDATE alerts SET sentmail=1 where id=?", (rows[-1]['id'],))
	conn.commit()
	conn.close()

def check_secret():
	global cfg
	if not "auth" in cfg:
		return True

	auth = json.loads( request.forms.auth )
	for val in cfg['auth']:
		ret = None
		if len( val ) == 1:
			ret = plugins.ss_plugin.receive_auth[val[0]]()
		else:
			ret = plugins.ss_plugin.receive_auth[val[0]]( options=val[1], content=auth[val[0]] )
		if ret == False:
			return False;
	return True

def send_email(subject, content):
	global cfg
	msg = MIMEText( content )
	msg["Subject"] = "Stats-Simple Email Alert: " + subject
	msg["From"] = cfg['email']['sender']
	msg["To"] = ", ".join( cfg['email']['receivers'] )

	s = smtplib.SMTP( cfg['email']['host'], cfg['email']['port'] )
	if( "username" in cfg['email'] and "password" in cfg["email"]):
		s.login( cfg['email']['username'], cfg['email']['password'] )
	s.sendmail( cfg['email']['sender'], cfg['email']['receivers'], msg.as_string() )
	ssprint( "Sent mail: " + subject )
	s.quit()

def ssprint(text):
	print "Stats-Simple Server: " + text

# ----------------------------------
# ---------------RUN----------------
# ----------------------------------

if not 'auth' in cfg:
	ssprint( "WARNING: No authentication is setup." )
app.run(host=cfg['host'], port=cfg['port'])