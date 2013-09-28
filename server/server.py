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
		return json.dumps( { "error": "WRONG_SECRET" } )
	name = request.forms.name
	if not name:
		return json.dumps( { "error": "NO_NAME" } )
	row = db.execute('SELECT * from nodes where name=?', (name,)).fetchone()
	if row:
		return json.dumps( { "success": "ALREADY_REGISTERED" } )
	else:
		db.execute('INSERT into nodes (name) VALUES (?)', (name,))
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
	for d in data:
		print 
		db.execute( 'INSERT into data (node,time,key,value) VALUES (?,?,?,?)', (row['id'],int(time),d,json.dumps( data[d] )) )
	return json.dumps( { "success": "VALUES_ENTERED" } )

@app.get("/data/:node/:key/:time/:end")
def get_data(node,key,time,end,db):
	return "[]"
	
@app.get("/data/:node/:key/:start")
def get_data(node,key,start,db):
	timearr = start.split( ":" )
	if( timearr[0] == "forever" ):
		return get_data(node,key,db)
	time_ago = time.time() - (time_dict[timearr[0]] * int(timearr[1]))
	
	rows = db.execute('SELECT value, time from data where node=? AND key=? AND time >= ?', (int(node),key,time_ago) ).fetchall()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "value": json.loads( row['value'] ) } )
	return json.dumps( data )
	
@app.get("/data/:node/:key")
def get_data(node,key,db):
	rows = db.execute('SELECT value, time from data where node=? AND key=?', (int(node),key) ).fetchall()
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

@app.get('/nodeinfo/:node')
def get_nodes(node, db):
	rows = db.execute('SELECT DISTINCT key from data where node=?', (node,)).fetchall()
	keys = []
	for row in rows:
		keys.append( row['key'] )
	return json.dumps( keys )

# :path is a bottle filter that matches strings with '/' in them
@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static/')

@app.route('/')
def index():
    return static_file("index.html", root='static/')

def check_secret():
	global cfg
	return request.forms.secret == cfg['secret']

host_arr = cfg['host'].split(":")
app.run(host=host_arr[0], port=int(host_arr[1]))