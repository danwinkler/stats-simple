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
from email.mime.text import MIMEText

# Ugly but whatever
time_dict = { "hour": 60*60, "day": 60*60*24, "month": 60*60*24*30, "year": 60*60*24*365 }

f = open( "server.cfg" )
j = f.read()
f.close()
cfg = json.loads( j )


# Trigger Thread
def trigger_thread( args ):
	while True:
		for t in cfg['triggers']:
			ss_triggers.triggers[t]()
		email_on_alerts()
		time.sleep( 300 )

if "triggers" in cfg:
	thread.start_new_thread( trigger_thread, ("",) )

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='db.db')
app.install(plugin)

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
		return get_data(node,key,db)
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
    return template("index", { "user_select": json.dumps( screen == None ), "data": json.dumps( cfg["screens"][screen] ) if (screen!=None and screen in cfg["screens"]) else "[]", "root": cfg['webpath'] } )

@app.route('/custom/:screen')
def index(screen):
	arr = json.loads( screen )
	print arr
	screen = json.dumps( arr )
	return template("index", { "user_select": json.dumps( False ), "data": screen, "root": cfg['webpath'] } )

def email_on_alerts():
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	time_ago = time.time() - (60*60*24)
	unique_alerts_last_day = db.execute('SELECT DISTINCT name from alerts where time >= ?', (time_ago,) ).fetchall()
	for name_row in unique_alerts_last_day:
		#Find out if we've sent an email for this alert in the last day
		rows = db.execute('SELECT time FROM alerts where name = ? AND time >= ? AND sentmail=1', (name_row['name'], time_ago)).fetchall()
		if len( rows ) > 0:
			continue
		else:
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
	if( "username" in cfg['email'] ):
		s.login( cfg['email']['username'], cfg['email']['password'] )
	s.sendmail( cfg['email']['sender'], cfg['email']['receivers'], msg.as_string() )
	ssprint( "Sent mail: " + subject )
	s.quit()

def ssprint(text):
	print "Stats-Simple Server: " + text

app.run(host=cfg['host'], port=cfg['port'])