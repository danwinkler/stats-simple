from bottle import route, run, template, request, static_file
from bottle.ext import sqlite
import bottle
import json
import time

# Ugly but whatever
time_dict = { "hour": 60*60, "day": 60*60*24, "month": 60*60*24*30, "year": 60*60*24*365 }

f = open( "server.cfg" )
j = f.read()
f.close()
cfg = json.loads( j )

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='db.db')
app.install(plugin)

@app.post('/register')
def register(db):
	if not check_secret():
		ssprint( "Client sent incorrect secret" )
		return json.dumps( { "error": "WRONG_SECRET" } )
	name = request.forms.name
	if not name:
		ssprint( "Client tried to register with no name set" )
		return json.dumps( { "error": "NO_NAME" } )
	row = db.execute('SELECT * from nodes where name=?', (name,)).fetchone()
	if row:
		ssprint( "Register Success: Already Registered: " + str(row['id']) )
		return json.dumps( { "success": "ALREADY_REGISTERED" } )
	else:
		db.execute('INSERT into nodes (name) VALUES (?)', (name,))
		ssprint( "Register Success: First time register: " + str(row['id']) )
		return json.dumps( { "success": "REGISTERED" } )

@app.post('/data')
def post_data(db):
	if not check_secret():
		return json.dumps( { "error": "WRONG_SECRET" } )
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

@app.route('/screens/:screen')
@app.route('/')
def index(screen=None):
    return template("index", { "user_select": json.dumps( screen == None ), "data": json.dumps( cfg["screens"][screen] ) if screen!=None else "[]", "root": cfg['webpath'] } )

def check_secret():
	global cfg
	return request.forms.secret and request.forms.secret == cfg['secret']

def ssprint(text):
	print "Stats-Simple Server: " + text

app.run(host=cfg['host'], port=cfg['port'])